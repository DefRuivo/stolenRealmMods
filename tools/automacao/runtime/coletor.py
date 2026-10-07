#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""coletor.py - AUT-4: coletor/driver de coleta runtime por objetos Unity (OPT-IN).

O QUE E
-------
A camada de CONTRATO e ORQUESTRACAO da coleta runtime do AUT-4. Ela NAO abre o
jogo: prepara a rodada, decide se ela esta autorizada, normaliza as observacoes
lidas do objeto vivo e monta manifest/rollback. O probe C# (`AUT4Probe/`) e quem
le do jogo, quando a rodada for autorizada.

SEGURANCA (por que o default e offline)
---------------------------------------
  * `decidir_autorizacao` so libera coleta com autorizacao E confirmacao E jogo;
    qualquer falta devolve NAO_EXERCITADO — nunca dado fabricado.
  * toda observacao carrega PROCEDENCIA; `fixture` nunca vira evidencia de
    runtime (`evidencia_runtime=false` basta, sem precisar de rotulo) e `runtime`
    exige sessao+hash. O ROTULO DO ARTEFATO tem precedencia sobre a intencao do
    chamador (A3).
  * campo AUSENTE/INDETERMINADO/NAO_EXERCITADO/Vazio NUNCA conta como OK — e campo
    ALVO (`campos_alvo`) nao lido e LACUNA, nao "fecha" (A2). O artefato REAL do
    probe emite `""`/`{}`/`[]` para "nao lido" (`GetParsedText()` -> string.Empty):
    vazio e NAO LIDO.
  * `planejar_rollback` enxerga tambem os arquivos que o probe CRIOU (o .cfg que
    nasce sozinho na 1a execucao), nao so a pasta do probe — e DIRETORIO que ja
    existia no perfil nao e removido (A5).
  * a rodada so CONCLUI com as tres provas de execucao (sessao DESTA rodada no JSON
    e mais novo que o lancamento; log com chainloader + linha de vida do probe;
    prints existentes, com bytes>0 e POSTERIORES ao lancamento) e com o instrumento
    declarando status de conclusao (A1/A4).

Reuso: le as fixtures no formato do CAP-1 / `capprobe.json`; nao reconstroi nada
de `scratch/cap1/`. O QUE AINDA NAO ESTA PROVADO: nada disto foi exercitado em
jogo — esta rodada e preparacao/teste OFFLINE (ver docs/automacao/AUT-4-*.md).
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import uuid

ESQUEMA = "AUT-4/1"
PROCEDENCIAS = ("runtime", "fixture")
EXIT_OK, EXIT_FALHOU, EXIT_NAO_RODOU = 0, 1, 2


class _MarcaMapeado(object):
    """Sentinel de IDENTIDADE do dict ja mapeado (COR-AUT4-F4).

    Um JSON de artefato NUNCA carrega este objeto em memoria (ele nao e um tipo JSON e
    uma copia/`deepcopy` devolve a MESMA instancia): entao ele distingue, sem chave
    forjavel, o dict que o proprio mapeador do coletor produziu de um dict cru do
    probe/artefato. Ver `_mapear_saida_probe`.
    """

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

    def __repr__(self):
        return "<mapeado-pelo-coletor>"


_CHAVE_MAPEADO = "_cor_aut4_mapeado"
_MARCA_MAPEADO = _MarcaMapeado()

# Campos canonicos da observacao de UM objeto vivo (o que a rodada runtime le).
CAMPOS = ("objeto", "caminho", "ativo_na_hierarquia", "texto_bruto", "texto_renderizado",
          "fonte", "material", "shader", "keywords", "cores", "geometria", "owners",
          "personagem")

# Campos que o probe REAL emite mas o schema antigo DESCARTAVA (B2 da AUT-4R):
# atravessam a costura como informacao (nunca viram lacuna).
CAMPOS_EXTRAS = ("componente", "visivel_na_tela", "shader_suportado", "tamanho_fonte",
                 "nota_texto_renderizado")
# Campos de GUARDA do RSTV (AUT5-F1, `t_dd95f8d9`): o probe passa a emitir por
# observacao o snapshot do personagem (`snapshot_antes`/`snapshot_depois` com
# `skills`/`pontos`), o reparent/restauracao do tooltip (`tooltip_pai_antes`/
# `_depois`, `tooltip_indice_antes`/`_depois`) e a anti-duplicacao
# (`janelas_duplicadas`). Entram como EXTRAS porque so existem nas observacoes
# que os emitem: quem classifica AUSENCIA e o avaliador de cenarios
# (`tools/automacao/cenarios/rstv.py`), POR CAPACIDADE — campo AUSENTE/None
# atravessa como estado AUSENTE e NUNCA vira OK (`_fecha` exige o par completo).
CAMPOS_RSTV = ("snapshot_antes", "snapshot_depois", "tooltip_pai_antes",
               "tooltip_pai_depois", "tooltip_indice_antes", "tooltip_indice_depois",
               "janelas_duplicadas")
CAMPOS_EXTRAS = CAMPOS_EXTRAS + CAMPOS_RSTV
CAMPOS_TODOS = CAMPOS + CAMPOS_EXTRAS

# Porta de lancamento (default explicito; a rodada de teste SUBSTITUI por um stub).
STEAM_PADRAO = r"C:\Program Files (x86)\Steam\steam.exe"
APPID = "1330000"
PRELOADER_REL = os.path.join("BepInEx", "core", "BepInEx.Preloader.dll")
PROBE_REL_PADRAO = os.path.join("BepInEx", "plugins", "AUT4Probe", "AUT4Probe.dll")
CFG_REL_PADRAO = os.path.join("BepInEx", "config", "com.gumatos.aut4probe.cfg")
LOG_REL_PADRAO = os.path.join("BepInEx", "LogOutput.log")
# Fases do JSON do probe que ja autorizam encerrar a espera (com teto de tempo).
FASES_TERMINAIS = ("concluido", "nao-exercitado", "sem_ui", "erro", "orcamento_estourado")

# A1 (AUT-4R2): as provas de EXECUCAO. O driver GERA a sessao e a injeta no `.cfg`;
# a evidencia so vale se trouxer ESSA sessao, for mais nova que o lancamento, o log
# da rodada tiver o fim do chainloader E a linha de vida do probe, e os prints
# existirem com bytes>0. Qualquer falta => NAO_EXERCITADO/INDETERMINADO, exit != 0.
CHAINLOADER_OK = "Chainloader startup complete"
HEARTBEAT_PROBE = "AUT4 PROBE:"

# A4 (AUT-4R2): estados do instrumento. So com status de CONCLUSAO o desfecho pode
# ser CONFIRMADA; estado terminal de falha (ou silencio) rebaixa o resultado.
STATUS_PROBE_OK = ("CONCLUIDO", "OK")
STATUS_PROBE_FALHA = ("NAO_EXERCITADO", "SEM_UI", "ERRO", "ORCAMENTO_ESTOURADO")
FASES_PROBE_FALHA = ("nao-exercitado", "sem-ui", "sem_ui", "erro",
                     "orcamento-estourado", "orcamento_estourado")
# R-3 (CIC-5R): a espera de estado para por ESTADO TERMINAL — `fase` OU `status`.
# O catch do probe (AUT4ProbePlugin.cs) grava `status=ERRO` SEM setar `fase` (quem
# escreve `fase=concluido` e o Finalizar(), que o catch nao chama): parar so pela
# `fase` fazia a espera queimar o teto INTEIRO num erro do instrumento (medido:
# 0,622 s de 0,6 s com `status=ERRO`, contra 0,018 s com `fase=erro`).
STATUS_TERMINAIS_ESPERA = STATUS_PROBE_OK + STATUS_PROBE_FALHA

# A6 (AUT-4R2): chaves da porta OPT-IN de ida-e-volta (leitura reproduzivel).
CFG_CHAVES = ("Autorizado", "OutDir", "OrcamentoSegundos", "Navegar", "PerfilDir",
              "HashFonte", "MaxTextos", "Sessao", "DemostrarTooltip", "MarcadorIdaEVolta")

# Rotulos que NUNCA podem ser maquiados como valor medido.
AUSENTES = ("AUSENTE", "NAO EXERCITADO", "NÃO EXERCITADO", "NAO_EXERCITADO",
            "INDETERMINADO", "INDETERMINATE", "-")


class PlanoInvalido(ValueError):
    """O plano de coleta nao cumpre o contrato."""


class ObservacaoInvalida(ValueError):
    """A observacao nao pode ser aceita como evidencia."""


def validar_alvos(alvos):
    """A2 (AUT-4R2): `campos_alvo` GOVERNA o veredito — logo tem de nomear campos
    que o coletor sabe medir. Alvo fora do schema e TYPO/ilusao de criterio: recusa
    o plano em vez de descartar o alvo em silencio (era o falso CONFIRMADA).
    """
    if alvos is None:
        return None
    lista = list(alvos)
    invalidos = [str(a) for a in lista
                 if not str(a).strip() or str(a) not in CAMPOS_TODOS]
    if invalidos:
        raise PlanoInvalido("campos_alvo fora do schema: %s (validos: %s)"
                            % (", ".join(invalidos), ", ".join(CAMPOS_TODOS)))
    return lista


# --------------------------------------------------------------------- plano

def validar_plano(plano):
    """Valida e normaliza o plano de coleta. Levanta PlanoInvalido se faltar algo."""
    if not isinstance(plano, dict):
        raise PlanoInvalido("plano nao e um objeto")
    if plano.get("esquema") != ESQUEMA:
        raise PlanoInvalido("esquema ausente ou errado: esperado %r, veio %r"
                            % (ESQUEMA, plano.get("esquema")))
    aut = plano.get("autorizacao")
    if not isinstance(aut, dict):
        raise PlanoInvalido("plano sem o bloco 'autorizacao'")
    if not isinstance(aut.get("coleta_autorizada"), bool):
        raise PlanoInvalido("autorizacao sem 'coleta_autorizada' booleano")
    cenarios = plano.get("cenarios")
    if not isinstance(cenarios, list) or not cenarios:
        raise PlanoInvalido("plano sem 'cenarios' (lista nao vazia)")
    norm = []
    for i, c in enumerate(cenarios):
        if not isinstance(c, dict):
            raise PlanoInvalido("cenario %d nao e um objeto" % i)
        if not c.get("nome"):
            raise PlanoInvalido("cenario %d sem 'nome'" % i)
        alvos = c.get("alvos")
        if not isinstance(alvos, list) or not alvos:
            raise PlanoInvalido("cenario %r sem 'alvos' (lista nao vazia)" % c.get("nome"))
        # A2: campos_alvo precisa nomear campo medivel (topo OU cenario).
        if c.get("campos_alvo") is not None:
            validar_alvos(c.get("campos_alvo"))
        norm.append(dict(c))
    if plano.get("campos_alvo") is not None:
        validar_alvos(plano.get("campos_alvo"))
    saida = dict(plano)
    saida["cenarios"] = norm
    return saida


def decidir_autorizacao(autorizado, jogo_disponivel, confirmacao=None):
    """Decide se a rodada pode coletar. Default: NAO_EXERCITADO, sem dado sintetico."""
    base = {"dados_sinteticos": False, "observacoes": [], "screenshot": None}
    if not autorizado:
        base.update({"status": "NAO_EXERCITADO", "pode_coletar": False, "modo": "offline",
                     "motivo": "coleta NAO autorizada (default do repositorio): nenhuma "
                               "leitura, PNG ou navegacao sera feita"})
        return base
    if not jogo_disponivel:
        base.update({"status": "NAO_EXERCITADO", "pode_coletar": False,
                     "modo": "autorizado-sem-jogo",
                     "motivo": "autorizado, mas SEM acesso ao jogo: nada a coletar "
                               "(NAO_EXERCITADO, jamais dado fabricado)"})
        return base
    if confirmacao != "coleta":
        base.update({"status": "NAO_EXERCITADO", "pode_coletar": False,
                     "modo": "autorizado-sem-confirmacao",
                     "motivo": "autorizado e com jogo, mas sem confirmacao explicita da "
                               "rodada ('%s')" % confirmacao})
        return base
    base.update({"status": "AUTORIZADO", "pode_coletar": True, "modo": "runtime",
                 "motivo": "coleta autorizada e confirmada: uma frente runtime por vez"})
    return base


# --------------------------------------------------------------- observacao

def _estado_do_campo(valor):
    """Classifica UM valor medido como PRESENTE ou AUSENTE (nao lido).

    COR-AUT4-F2 (A2): VAZIO e NAO LIDO, nunca PRESENTE. O artefato REAL do probe
    emite `""` onde o schema antigo esperava `null` — `GetParsedText()` devolve
    `string.Empty` (medido no `lib/Unity.TextMeshPro.dll`; nunca null) e `Trunc`
    so devolve `null` para entrada `null` — e o mesmo probe tambem emite `{}` (sem
    material nao ha keywords/cores) e `[]` (funil sem owner Harmony). Um valor
    vazio nao prova leitura: alvo VAZIO tem de virar LACUNA.
    """
    if valor is None:
        return "AUSENTE"
    if isinstance(valor, str):
        if valor.strip().upper() in AUSENTES or not valor.strip():
            return "AUSENTE"
        return "PRESENTE"
    if isinstance(valor, (list, tuple, set, frozenset, dict)) and len(valor) == 0:
        return "AUSENTE"
    return "PRESENTE"


def normalizar_observacao(obs, procedencia, rotulo_fixture=None, contexto=None, alvos=None):
    """Normaliza UMA observacao de objeto vivo, com procedencia obrigatoria.

    `contexto` traz `sessao`/`hash_fonte` do TOPO do JSON do probe (B1): o probe
    guarda os dois SO no topo, entao a costura os injeta aqui sem os repetir em
    cada item. `alvos` limita o conjunto de campos que contam como LACUNA quando
    ausentes (B3): campo fora do alvo nao penaliza, e objeto INATIVO declara o
    fallback em vez de virar OK visual falso.
    """
    if procedencia not in PROCEDENCIAS:
        raise ObservacaoInvalida(
            "procedencia invalida/ausente: %r (esperado 'runtime' ou 'fixture')" % (procedencia,))
    if not isinstance(obs, dict):
        raise ObservacaoInvalida("observacao nao e um objeto")

    contexto = contexto or {}
    sessao = obs.get("sessao") or contexto.get("sessao")
    hash_fonte = obs.get("hash_fonte") or contexto.get("hash_fonte")

    if procedencia == "runtime":
        faltando = [c for c, v in (("sessao", sessao), ("hash_fonte", hash_fonte))
                    if not str(v or "").strip()]
        if faltando:
            raise ObservacaoInvalida(
                "procedencia=runtime exige %s nao vazio (sem hash de fonte/sessao a "
                "evidencia nao identifica a build medida)" % ", ".join(faltando))
    else:
        if not rotulo_fixture:
            raise ObservacaoInvalida(
                "fixture exige 'rotulo_fixture' — sem ele nao da para distinguir fixture de runtime")

    # A2: alvo fora do schema e PLANO INVÁLIDO — nunca "fecha" por engano.
    validar_alvos(alvos)
    alvos_efetivos = set(alvos) if alvos is not None else set(CAMPOS)
    inativa = obs.get("ativo_na_hierarquia") is False or bool(obs.get("nota_texto_renderizado"))
    campos = {}
    lacunas = []
    nao_aplicaveis = []
    for campo in CAMPOS_TODOS:
        valor = obs.get(campo)
        estado = _estado_do_campo(valor)
        item = {"estado": estado, "valor": valor, "alvo": campo in alvos_efetivos}
        # Fallback DECLARADO do objeto INATIVO: o TMP so preenche o mesh com o
        # objeto ativo, entao `texto_renderizado` vazio NAO e lacuna — fica
        # marcado (NAO pode ser apresentado como leitura renderizada).
        if (campo == "texto_renderizado" and estado == "AUSENTE" and inativa
                and _estado_do_campo(obs.get("texto_bruto")) == "PRESENTE"):
            estado = "NAO_APLICAVEL"
            item["estado"] = estado
            item["fallback"] = "texto_bruto"
            item["motivo"] = (obs.get("nota_texto_renderizado") or
                              "objeto INATIVO: GetParsedText() vazio; vale o texto_bruto")
            nao_aplicaveis.append(campo)
        # A2: alvo PEDIDO e nao lido (AUSENTE ou o fallback NAO_APLICAVEL) e LACUNA.
        # O fallback do inativo e INFORMACAO declarada, nunca satisfacao do criterio.
        if campo in alvos_efetivos and estado in ("AUSENTE", "NAO_APLICAVEL"):
            lacunas.append(campo)
        campos[campo] = item

    declarou_ok = (str(obs.get("status", "")).strip().upper() == "OK") or (obs.get("ok") is True)
    if declarou_ok and lacunas:
        raise ObservacaoInvalida(
            "campo AUSENTE/INDETERMINADO nao pode ser OK (lacuna(s): %s)" % ", ".join(lacunas))

    return {
        "esquema": ESQUEMA,
        "procedencia": procedencia,
        "evidencia_runtime": procedencia == "runtime",
        "rotulo_fixture": rotulo_fixture if procedencia == "fixture" else None,
        "sessao": sessao,
        "hash_fonte": hash_fonte,
        "campos": campos,
        "lacunas": lacunas,
        "nao_aplicaveis": nao_aplicaveis,
        "alvos": sorted(alvos_efetivos),
        "ok": procedencia == "runtime" and not lacunas,
    }


def resultado_nao_exercitado(motivo, plano=None):
    """Resultado honesto do caminho sem jogo: NAO_EXERCITADO, zero observacao."""
    return {
        "esquema": ESQUEMA,
        "status": "NAO_EXERCITADO",
        "motivo": motivo,
        "dados_sinteticos": False,
        "screenshot": None,
        "observacoes": [],
        "plano": (plano or {}).get("nome") if isinstance(plano, dict) else None,
    }


# ------------------------------------------------------------ manifest/rollback

def _sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def montar_manifest(raiz, arquivos):
    """Manifest dos artefatos: nome, bytes e sha256 (a prova de qual arquivo saiu)."""
    artefatos = []
    for nome in arquivos:
        caminho = nome if os.path.isabs(nome) else os.path.join(raiz, nome)
        item = {"arquivo": os.path.basename(caminho), "bruto": nome}
        try:
            item["bytes"] = os.path.getsize(caminho)
            item["sha256"] = _sha256(caminho)
        except OSError as erro:
            item["erro"] = str(erro)
        artefatos.append(item)
    return {"esquema": ESQUEMA, "raiz": raiz, "total": len(artefatos), "artefatos": artefatos}


def planejar_rollback(antes, depois, dirs_antes=None, dirs_depois=None):
    """Classifica o que o probe CRIOU/MUDOU/REMOVEU — inclusive arquivo nascido sozinho.

    A5 (AUT-4R2): a comparacao de ARQUIVOS nao basta — um DIRETORIO que ja existia
    (pasta vazia do probe, por exemplo) nao pode ser removido no rollback. `dirs_*`
    traz o estado de EXISTENCIA dos diretorios ANTES/DEPOIS; os pre-existentes ficam
    declarados em `dirs_pre_existentes` e sao PRESERVADOS.
    """
    criados = sorted(k for k in depois if k not in antes)
    modificados = sorted(k for k in depois if k in antes and antes[k] != depois[k])
    removidos = sorted(k for k in antes if k not in depois)
    conjunto_antes = set(dirs_antes or ())
    conjunto_depois = set(dirs_depois or ())
    return {
        "criados": criados, "modificados": modificados, "removidos": removidos,
        "dirs_criados": sorted(conjunto_depois - conjunto_antes),
        "dirs_pre_existentes": sorted(conjunto_antes & conjunto_depois),
        "extra": False,
        "acao": {"criados": "REMOVER (nao existiam antes)",
                 "modificados": "RESTAURAR o conteudo original",
                 "removidos": "REPOR o arquivo original",
                 "dirs_criados": "REMOVER se ficarem vazios (nasceram na rodada)",
                 "dirs_pre_existentes": "PRESERVAR (ja existiam antes da rodada)"},
    }


# ------------------------------------------------------------------ consolidacao

def _alvos_do_plano(plano):
    """Campos-alvo do plano: a UNIAO de `campos_alvo` do topo e de TODOS os cenarios.

    A2: o alvo e validado contra o schema — alvo inexistente/typo e PlanoInvalido.

    S-2 (CIC-5R): antes so o topo ou o `cenarios[0]` eram lidos — com 2+ cenarios, os
    requisitos por campo do 2o em diante eram silenciosamente descartados (e, se
    `campos_alvo` existisse SO no 2o, o plano voltava a mirar os 13 campos de todo
    TMP_Text). Agora o alvo declarado por QUALQUER cenario governa o veredito.
    """
    if not isinstance(plano, dict):
        return None
    alvos = []
    vistos = set()

    def _acrescentar(lista):
        for alvo in validar_alvos(lista) or []:
            if alvo not in vistos:
                vistos.add(alvo)
                alvos.append(alvo)

    if plano.get("campos_alvo"):
        _acrescentar(plano.get("campos_alvo"))
    cenarios = plano.get("cenarios")
    if isinstance(cenarios, list):
        for cenario in cenarios:
            if isinstance(cenario, dict) and cenario.get("campos_alvo"):
                _acrescentar(cenario.get("campos_alvo"))
    return alvos or None


def consolidar(plano, observacoes, procedencia, contexto=None, alvos=None):
    """Consolida o resultado. Devolve (resultado, exit_code)."""
    if procedencia == "fixture":
        return {
            "esquema": ESQUEMA,
            "status": "FIXTURE",
            "evidencia_runtime": False,
            "veredito": "NAO PROVA RUNTIME: fixture rotulada — nunca apresentar como "
                        "resultado de jogo",
        }, EXIT_NAO_RODOU
    if procedencia != "runtime":
        raise ObservacaoInvalida("consolidar exige procedencia 'runtime' ou 'fixture'")

    if alvos is None:
        alvos = _alvos_do_plano(plano)
    else:
        alvos = validar_alvos(alvos)
    normalizadas = [normalizar_observacao(o, "runtime", contexto=contexto, alvos=alvos)
                    for o in (observacoes or [])]
    if not normalizadas:
        return resultado_nao_exercitado("sem observacoes de runtime (sem jogo autorizado)", plano), EXIT_NAO_RODOU

    incompletos = [n for n in normalizadas if n["lacunas"]]
    nao_aplicaveis = sorted({c for n in normalizadas for c in n["nao_aplicaveis"]})
    veredito = ("HA LACUNA: a coleta nao fecha — AUSENTE/INDETERMINADO nunca e OK."
                if incompletos else "DESFECHO CONFIRMADO nas observacoes medidas.")
    if nao_aplicaveis:
        veredito += (" Nota: %s marcado(s) NAO_APLICAVEL (fallback inativo declarado) — "
                     "NAO e leitura renderizada." % ", ".join(nao_aplicaveis))
    resultado = {
        "esquema": ESQUEMA,
        "status": "INCOMPLETO" if incompletos else "CONFIRMADA",
        "evidencia_runtime": True,
        "observacoes": normalizadas,
        "lacunas": sorted({c for n in incompletos for c in n["lacunas"]}),
        "nao_aplicaveis": nao_aplicaveis,
        "veredito": veredito,
    }
    return resultado, (EXIT_FALHOU if incompletos else EXIT_OK)


# ------------------------------------------------------------------ driver

def planejar_rodada(plano, autorizado, jogo_disponivel, confirmacao=None, perfil_dir=None):
    """Plano completo da rodada (instalar/ler/remover). Offline devolve NAO_EXERCITADO."""
    plano = validar_plano(plano)
    decisao = decidir_autorizacao(autorizado, jogo_disponivel, confirmacao)
    rodada = {
        "esquema": ESQUEMA,
        "decisao": decisao,
        "perfil": perfil_dir,
        "passos": [],
        "manifest_previsto": {
            "artefatos": ["aut4probe.json", "01-ui.png", "NN-*.png"],
            "rollback": ["pasta plugins/AUT4Probe (REMOVER — criada pela rodada)",
                         "com.gumatos.aut4probe.cfg (REMOVER se nao existia; RESTAURAR se existia)",
                         "LogOutput.log (ARQUIVAR antes de lancar; um boot trunca o log)"],
        },
    }
    if not decisao["pode_coletar"]:
        rodada["resultado"] = resultado_nao_exercitado(decisao["motivo"], plano)
        rodada["exit_code"] = EXIT_NAO_RODOU
        return rodada, EXIT_NAO_RODOU
    rodada["passos"] = [
        "1. arquivar LogOutput.log e remover para o boot desta rodada ser o unico lido",
        "2. compilar e INSTALAR o probe (instrumento) em plugins/AUT4Probe",
        "3. lancar o jogo com os ARGUMENTOS de doorstop do perfil (nao o .exe direto)",
        "4. esperar ESTADO (UI com texto renderizado) — nao sleep cego — com teto de tempo",
        "5. ler dos objetos vivos (TMP/material/cor/geometria/owners) + PNG pela API do Unity",
        "6. consolidar manifest e rollback EXATO (inclusive arquivos criados pelo probe)",
    ]
    rodada["exit_code"] = EXIT_OK
    return rodada, EXIT_OK


# ------------------------------------------------- costura probe -> coletor (B1/B2)

def _mapear_saida_probe(dados):
    """Mapeia o JSON do probe (ou um dict ja mapeado) para as chaves do coletor.

    Idempotente: quem ja passou por aqui traz `status_probe`; um dict cru no formato
    do probe traz `status`. Aceitar os dois evita que o caminho de API/CLI escape do
    vinculo de status (A4).

    COR-AUT4-F4 — a PRESENCA de `evidencia_runtime` e derivada INTERNAMENTE do que o
    coletor VIU no JSON de entrada (`"evidencia_runtime" in dados`), NUNCA da chave
    `evidencia_runtime_presente` que o PROPRIO artefato carrega. Antes, um artefato
    com `evidencia_runtime: "false"` (forma errada) E `evidencia_runtime_presente:
    false` (ou `0`) declarava "sem evidencia" e CONFIRMAVA como runtime: o artefato
    governava o proprio veredito.

    IDEMPOTENCIA (pitfall): o dict JA MAPEADO volta a passar por aqui e SEMPRE traz a
    chave `evidencia_runtime` (com `None` quando o probe real NAO a emite). Derivar a
    presenca de novo de `"evidencia_runtime" in dados` transformaria o caminho
    legitimo 'chave ausente = runtime' em FIXTURE na 2a passagem. Para nao depender
    de NENHUM valor que o artefato possa forjar, o dict mapeado carrega o marcador de
    IDENTIDADE `_MARCA_MAPEADO` (um objeto em memoria, NAO serializavel para JSON):
    so o mapeador do coletor o apresenta. Se — e so se — o marcador esta presente por
    IDENTIDADE, a presenca derivada na 1a passagem e preservada.
    """
    if not isinstance(dados, dict):
        raise ObservacaoInvalida("saida do probe nao e um objeto JSON")
    if dados.get(_CHAVE_MAPEADO) is _MARCA_MAPEADO:
        presente = bool(dados.get("evidencia_runtime_presente"))
    else:
        presente = "evidencia_runtime" in dados
    return {
        "esquema": dados.get("esquema", ESQUEMA),
        "status_probe": dados.get("status_probe", dados.get("status")),
        "fase": dados.get("fase"),
        "sessao": dados.get("sessao"),
        "hash_fonte": dados.get("hash_fonte"),
        "procedencia": dados.get("procedencia"),
        "rotulo_fixture": dados.get("rotulo_fixture"),
        "evidencia_runtime": dados.get("evidencia_runtime"),
        # COR-AUT4-F4: presenca derivada da entrada crua (chave ausente = runtime).
        "evidencia_runtime_presente": presente,
        _CHAVE_MAPEADO: _MARCA_MAPEADO,
        "observacoes": dados.get("observacoes") or [],
        "manifest": dados.get("manifest"),
        "rollback": dados.get("rollback"),
        "owners_harmony": dados.get("owners_harmony"),
        "mods_carregados": dados.get("mods_carregados"),
        "prints": dados.get("prints") or [],
        "ida_e_volta": dados.get("ida_e_volta"),
    }


def carregar_saida_probe(caminho):
    """Le o `aut4probe.json` REAL do probe. Topo e observacoes ficam separados."""
    with open(caminho, encoding="utf-8") as fh:
        dados = json.load(fh)
    return _mapear_saida_probe(dados)


def anexar_contexto(observacoes, contexto):
    """B1: injeta `sessao`/`hash_fonte` do TOPO em cada observacao.

    O probe guarda os dois SO no topo; sem esta costura
    `normalizar_observacao(..., 'runtime')` RECUSA a evidencia.
    """
    saida = []
    for o in observacoes or []:
        copia = dict(o)
        for chave in ("sessao", "hash_fonte"):
            if not str(copia.get(chave) or "").strip():
                valor = str((contexto or {}).get(chave) or "").strip()
                if valor:
                    copia[chave] = (contexto or {}).get(chave)
        saida.append(copia)
    return saida


def consolidar_probe(caminho_ou_saida, plano, alvos=None, procedencia=None):
    """Costura completa: carrega a saida do probe, injeta o topo e consolida.

    A procedencia e AUTO-DETECTADA e o ROTULO DO PROPRIO ARTEFATO tem PRECEDENCIA
    (A3 da AUT-4R2, reforcado na COR-AUT4-F2 e endurecido na COR-AUT4-F3): um JSON que
    se declara fixture (`procedencia: fixture`, ou `evidencia_runtime` com qualquer
    forma NAO-runtime) NUNCA e consolidado como runtime — nem quando o chamador passa
    `procedencia='runtime'`. Sai `FIXTURE` (exit 2), como manda a regra
    "fixture nao prova runtime".

    COR-AUT4-F3 — FORMA de `evidencia_runtime`: o probe C# REAL nao emite essa chave,
    entao a AUSENCIA dela (ou o bool `True` legitimo) e o caminho runtime. Qualquer
    outra forma PRESENTE — bool `False`, a string "false"/"0", o inteiro 0, `null`,
    ou valor nao-canonico — e declaracao NAO-runtime (ou ilegivel) e RECUSA como
    fixture: nunca vira runtime/CONFIRMADA. Antes (`is False`) string "false"/0/null
    escapavam do `is False` e um artefato com a FORMA ERRADA confirmava.

    A4 (AUT-4R2): o `status`/`fase` do instrumento entra no VEREDITO. Estado terminal
    de falha (ERRO/SEM_UI/ORCAMENTO_ESTOURADO/NAO_EXERCITADO) — ou a AUSENCIA de
    status de conclusao — rebaixa o resultado e o exit != 0.
    """
    saida = (carregar_saida_probe(caminho_ou_saida)
             if isinstance(caminho_ou_saida, (str, bytes, os.PathLike))
             else _mapear_saida_probe(caminho_ou_saida))
    declarada = str(saida.get("procedencia") or "").strip().lower()
    rotulo = saida.get("rotulo_fixture")
    # A3 (COR-AUT4-F2) + COR-AUT4-F3 + COR-AUT4-F4: `evidencia_runtime` e uma
    # DECLARACAO opcional do artefato. Runtime so vale com a chave AUSENTE (o probe C#
    # real nao emite a chave) ou o bool `True` legitimo. QUALQUER outra forma
    # PRESENTE — bool `False`, a string "false"/"0"/"False", o inteiro 0, `null`, ou
    # valor nao-canonico — e declaracao NAO-runtime (ou ilegivel) e RECUSA como
    # fixture. COR-AUT4-F4: a PRESENCA (`evidencia_runtime_presente`) NAO vem do
    # artefato — e derivada INTERNAMENTE da entrada crua por `_mapear_saida_probe`
    # (um artefato com a forma errada + `presente: false`/`0` governava o proprio
    # veredito e confirmava).
    declarada_ev = bool(saida.get("evidencia_runtime_presente"))
    ev_valor = saida.get("evidencia_runtime")
    declara_runtime = (not declarada_ev) or (ev_valor is True)
    rotulado_fixture = (declarada == "fixture" or not declara_runtime)
    if rotulado_fixture:
        procedencia = "fixture"
        if declarada == "fixture":
            rotulo_declarado = rotulo or declarada
        elif ev_valor is False:
            rotulo_declarado = "evidencia_runtime=false"
        else:
            rotulo_declarado = ("evidencia_runtime=%r nao e o bool False nem o bool True: "
                                "forma nao-canonica, recusada como fixture" % (ev_valor,))
        nota_precedencia = ("o proprio artefato se declara fixture (%s): o rotulo tem "
                            "precedencia sobre a intencao do chamador" % rotulo_declarado)
    else:
        nota_precedencia = None
        if procedencia is None:
            procedencia = "runtime"
    contexto = {"sessao": saida.get("sessao"), "hash_fonte": saida.get("hash_fonte")}
    observacoes = saida.get("observacoes") or []
    if procedencia == "fixture":
        resultado, codigo = consolidar(plano, observacoes, "fixture", contexto=contexto, alvos=alvos)
        if isinstance(resultado, dict) and nota_precedencia:
            resultado["motivo"] = nota_precedencia
    else:
        resultado, codigo = consolidar(plano, anexar_contexto(observacoes, contexto), "runtime",
                                       contexto=contexto, alvos=alvos)
        # A4: o instrumento PRECISA declarar conclusao; falha (ou silencio) rebaixa.
        status_probe = str(saida.get("status_probe") or "").strip().upper()
        fase_probe = str(saida.get("fase") or "").strip().lower()
        if isinstance(resultado, dict):
            resultado["status_probe_declarou"] = status_probe or None
            resultado["fase_probe_declarou"] = fase_probe or None
        if status_probe in STATUS_PROBE_FALHA or fase_probe in FASES_PROBE_FALHA:
            resultado = dict(resultado)
            resultado["status"] = "ERRO" if status_probe == "ERRO" else "INCOMPLETO"
            resultado["motivo"] = ("estado terminal de falha do instrumento (%s / %s): "
                                   "nao confirma desfecho"
                                   % (status_probe or "sem status", fase_probe or "sem fase"))
            codigo = EXIT_FALHOU
        elif status_probe not in STATUS_PROBE_OK:
            resultado = dict(resultado)
            resultado["status"] = "INCOMPLETO"
            resultado["motivo"] = ("o instrumento nao declarou status de conclusao (%r): "
                                   "silencio nao e aprovacao" % (status_probe or "",))
            codigo = EXIT_FALHOU
    if isinstance(resultado, dict):
        resultado["saida_probe"] = {
            "status": saida.get("status_probe"), "fase": saida.get("fase"),
            "sessao": saida.get("sessao"), "hash_fonte": saida.get("hash_fonte"),
            "total": len(observacoes),
        }
    return resultado, codigo


# ------------------------------------------------- config derivada (sem credencial)

def derivar_config(perfil_dir, out_dir, autorizado, hash_fonte="", dll_probe=None,
                   navegar=False, orcamento=120, max_textos=400, sessao="", demostrar=False,
                   marcador=""):
    """Deriva o `.cfg` do probe. NAO gera credencial nenhuma.

    `HashFonte` sai do sha256 da DLL quando nao informado; `Navegar` e sempre false
    por default (a rodada minima nao navega). `Autorizado` DERIVA da autorizacao da
    rodada — nunca e fixado true aqui. `Sessao` e a identidade da RODADA, gerada pelo
    driver (A1): a evidencia do probe so pertence a esta rodada se trouxer esta chave.
    `DemostrarTooltip`/`MarcadorIdaEVolta` sao a porta OPT-IN de ida-e-volta (A6).
    """
    if not hash_fonte and dll_probe and os.path.isfile(dll_probe):
        hash_fonte = _sha256(dll_probe)
    return {
        "Autorizado": bool(autorizado),
        "OutDir": out_dir,
        "OrcamentoSegundos": int(orcamento),
        "Navegar": bool(navegar),
        "PerfilDir": perfil_dir or "",
        "HashFonte": hash_fonte or "",
        "MaxTextos": int(max_textos),
        "Sessao": sessao or "",
        "DemostrarTooltip": bool(demostrar),
        "MarcadorIdaEVolta": marcador or "",
    }


def escrever_cfg(caminho, config):
    """Escreve o `.cfg` no formato do BepInEx (`Chave = valor` sob `[Geral]`)."""
    linhas = ["[Geral]", ""]
    for chave in CFG_CHAVES:
        valor = config.get(chave)
        if isinstance(valor, bool):
            valor = "true" if valor else "false"
        linhas.append("%s = %s" % (chave, valor))
    texto = "\n".join(linhas) + "\n"
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write(texto)
    return texto


# ------------------------------------------------------- rollback executavel

def snapshot_arquivos(raiz, relativos):
    """sha256 de cada arquivo relativo que EXISTE. A AUSENCIA da chave e o que
    `planejar_rollback` le como "nao existia antes" (nao usar valor None)."""
    snap = {}
    for rel in relativos:
        caminho = os.path.join(raiz, rel)
        if os.path.isfile(caminho):
            snap[rel] = _sha256(caminho)
    return snap


def snapshot_dirs(raiz, relativos):
    """A5: quais DIRETORIOS (ancestrais dos arquivos vigiados) ja EXISTEM antes.

    Sem isto o rollback nao sabe distinguir "pasta que a rodada criou" de "pasta
    que ja estava no perfil" — e removia as duas.
    """
    candidatos = set()
    for rel in relativos:
        pasta = os.path.dirname(rel)
        while pasta:
            candidatos.add(pasta)
            pasta = os.path.dirname(pasta)
    return {d for d in candidatos if os.path.isdir(os.path.join(raiz, d))}


def _remover_dirs_vazios(raiz, caminho, preservar=()):
    """Remove diretorios vazios criados pela rodada; PARA nos pre-existentes (A5)."""
    raiz = os.path.abspath(raiz)
    caminho = os.path.abspath(caminho)
    intocaveis = set()
    for p in (preservar or ()):
        p = os.path.abspath(p) if os.path.isabs(p) else os.path.abspath(os.path.join(raiz, p))
        intocaveis.add(p)
    while caminho.startswith(raiz) and caminho != raiz:
        if caminho in intocaveis:
            break
        try:
            if os.path.isdir(caminho) and not os.listdir(caminho):
                os.rmdir(caminho)
            else:
                break
        except OSError:
            break
        caminho = os.path.dirname(caminho)


def executar_rollback(raiz, plano_rb, backups, preservar=None):
    """Executa o rollback EXATO: remove o que nasceu, restaura o que mudou/sumiu.

    A5: `preservar` recebe os diretorios pre-existentes (`dirs_pre_existentes`) e
    eles NUNCA sao removidos, mesmo que fiquem vazios.
    """
    preservar = preservar if preservar is not None else plano_rb.get("dirs_pre_existentes") or []
    acoes = []
    for rel in plano_rb.get("criados", []):
        caminho = os.path.join(raiz, rel)
        if os.path.isfile(caminho):
            os.remove(caminho)
            acoes.append({"acao": "removido", "arquivo": rel})
            _remover_dirs_vazios(raiz, os.path.dirname(caminho), preservar)
    for rel in list(plano_rb.get("modificados", [])) + list(plano_rb.get("removidos", [])):
        caminho = os.path.join(raiz, rel)
        bkp = (backups or {}).get(rel)
        if bkp and os.path.isfile(bkp):
            os.makedirs(os.path.dirname(caminho), exist_ok=True)
            shutil.copy2(bkp, caminho)
            acoes.append({"acao": "restaurado", "arquivo": rel})
        else:
            acoes.append({"acao": "sem-backup", "arquivo": rel})
    # diretorios que a rodada criou e ficaram vazios tambem voltam (exatos).
    for rel in plano_rb.get("dirs_criados", []):
        _remover_dirs_vazios(raiz, os.path.join(raiz, rel), preservar)
    return acoes


# --------------------------------------------------- atualidade (fonte/dll/manifest)

def provar_atualidade(perfil_dir, out_dir, hash_fonte, saida_probe=None, arquivos=None):
    """Prova que FONTE/DLL/SESSAO e MANIFEST descrevem os bytes ATUAIS.

    O sha do PRÓPRIO `aut4probe.json` dentro do manifest do probe e AUTO-REFERENTE
    (calculado antes de o arquivo fechar) — nao serve de prova; o manifest do driver
    (hash dos bytes em disco) e o autoritativo. Nao abre cascata: so impede o falso
    OK de quem usa o manifest.
    """
    dll = os.path.join(perfil_dir, PROBE_REL_PADRAO)
    dll_sha = _sha256(dll) if os.path.isfile(dll) else None
    probe_hash = (saida_probe or {}).get("hash_fonte")
    motivos = []
    if not str(hash_fonte or "").strip():
        motivos.append("cfg sem HashFonte")
    if dll_sha is None:
        motivos.append("DLL do probe ausente no perfil")
    elif hash_fonte and dll_sha != hash_fonte:
        motivos.append("DLL instalada difere do HashFonte do cfg")
    if not str(probe_hash or "").strip():
        motivos.append("saida do probe sem hash_fonte (sessao nao identificada)")
    elif hash_fonte and probe_hash != hash_fonte:
        motivos.append("hash_fonte da saida (%s) difere do HashFonte (%s)"
                       % (str(probe_hash)[:12], str(hash_fonte)[:12]))
    manifest = None
    if arquivos:
        manifest = montar_manifest(out_dir, arquivos)
        for art in manifest["artefatos"]:
            art["auto_referente"] = art["arquivo"] == "aut4probe.json"
            art["autoritativo"] = not art["auto_referente"]
    sessao_ok = bool(str((saida_probe or {}).get("sessao") or "").strip())
    manifest_ok = bool(manifest) and all("erro" not in a for a in manifest["artefatos"])
    return {
        "dll_sha": dll_sha, "hash_fonte": hash_fonte, "probe_hash_fonte": probe_hash,
        "fonte_ok": not motivos, "sessao_ok": sessao_ok, "manifest": manifest,
        "manifest_ok": manifest_ok, "motivos": motivos,
    }


# -------------------------------------------- provas de execucao (A1) e ida-e-volta (A6)

def sessao_da_rodada(quando=None):
    """A1: identidade da rodada GERADA pelo driver (vai para o `.cfg`, volta no JSON)."""
    carimbo = time.strftime("%Y%m%d-%H%M%S", time.localtime(quando))
    return "AUT4-%s-%s" % (carimbo, uuid.uuid4().hex[:8])


def _demostrar_do_plano(plano):
    """A6: o plano pede a demonstracao de tooltip (ida-e-volta)? Topo ou QUALQUER cenario.

    (Mesma raiz do S-2: ler so o `cenarios[0]` descartava em silencio um pedido
    declarado no 2o cenario.)
    """
    if not isinstance(plano, dict):
        return False
    if plano.get("demostrar_tooltip") is not None:
        return bool(plano.get("demostrar_tooltip"))
    cenarios = plano.get("cenarios")
    if isinstance(cenarios, list):
        return any(isinstance(c, dict) and bool(c.get("demostrar_tooltip")) for c in cenarios)
    return False


def provas_de_execucao(caminho_json, caminho_log, saida, sessao_rodada, lancamento_epoca,
                       out_dir=None):
    """A1: as TRES provas independentes de que ESTA rodada leu o jogo.

    (a) a evidencia e DESTA rodada: traz a sessao gerada pelo driver E o JSON e mais
        novo que o lancamento (um `aut4probe.json` anterior nao vale);
    (b) o log DESTA rodada (o driver apaga o anterior antes de lancar) tem o fim do
        chainloader E a linha de vida do probe;
    (c) `prints` nao vazio, cada arquivo existindo, com bytes>0 E POSTERIOR ao
        lancamento desta rodada (o `out_dir` e reusado: PNG de rodada anterior nao
        vale — A1-c da COR-AUT4R).

    `ok` so e True com as tres. Cada falta entra em `faltas` (motivo legivel).
    """
    saida = saida or {}
    ev = {
        "sessao_rodada": sessao_rodada,
        "sessao_evidencia": saida.get("sessao"),
        "sessao_confere": bool(sessao_rodada) and str(saida.get("sessao") or "") == str(sessao_rodada),
        "lancamento_epoca": lancamento_epoca,
        "json_mtime": None,
        "json_mais_novo": False,
        "log_chainloader": False,
        "log_probe": False,
        "prints": [],
        "prints_ok": False,
    }
    try:
        ev["json_mtime"] = os.path.getmtime(caminho_json)
    except OSError:
        ev["json_mtime"] = None
    ev["json_mais_novo"] = bool(ev["json_mtime"] is not None and lancamento_epoca is not None
                                and ev["json_mtime"] + 1e-3 >= lancamento_epoca)
    texto = ""
    if os.path.isfile(caminho_log):
        try:
            with open(caminho_log, encoding="utf-8", errors="replace") as fh:
                texto = fh.read()
        except OSError:
            texto = ""
    ev["log_chainloader"] = CHAINLOADER_OK in texto
    ev["log_probe"] = HEARTBEAT_PROBE in texto
    for item in saida.get("prints") or []:
        caminho = (str(item) if os.path.isabs(str(item))
                   else os.path.join(out_dir or "", str(item)))
        try:
            existe = os.path.isfile(caminho)
            bytes_ = os.path.getsize(caminho) if existe else 0
            mtime = os.path.getmtime(caminho) if existe else None
        except OSError:
            existe, bytes_, mtime = False, 0, None
        # A1-c (COR-AUT4-F2): o out_dir e REUSADO por desenho; um PNG de rodada
        # ANTERIOR nao prova ESTA rodada. O print tem de ser POSTERIOR ao lancamento.
        fresco = bool(existe and mtime is not None and lancamento_epoca is not None
                      and mtime + 1e-3 >= lancamento_epoca)
        ev["prints"].append({"arquivo": str(item), "existe": bool(existe), "bytes": bytes_,
                             "mtime": mtime, "posterior_ao_lancamento": fresco})
    ev["prints_ok"] = bool(ev["prints"]) and all(
        p["existe"] and p["bytes"] > 0 and p["posterior_ao_lancamento"] for p in ev["prints"])
    faltas = []
    if not ev["sessao_confere"]:
        faltas.append("a evidencia nao traz a sessao desta rodada (%r != %r)"
                      % (ev["sessao_evidencia"], sessao_rodada))
    if not ev["json_mais_novo"]:
        faltas.append("o JSON da evidencia nao e mais novo que o lancamento desta rodada")
    if not ev["log_chainloader"]:
        faltas.append("o log desta rodada nao tem o fim do chainloader")
    if not ev["log_probe"]:
        faltas.append("o log desta rodada nao tem a linha de vida do probe")
    if not ev["prints_ok"]:
        faltas.append("sem print valido (print ausente, inexistente, bytes=0 ou ANTERIOR a esta rodada)")
    ev["faltas"] = faltas
    ev["ok"] = not faltas
    return ev


# ------------------------------------------------------------------ execucao

def _esperar_estado(caminho_log, caminho_json, timeout_s, poll_s):
    """Espera por ESTADO (log chainloader + JSON do probe), com teto — nao sleep cego.

    R-3 (CIC-5R): a parada e por ESTADO TERMINAL — `fase` terminal OU `status`
    terminal. O catch do probe grava `status=ERRO` SEM setar `fase`, entao parar so
    pela `fase` fazia a espera queimar o teto INTEIRO num erro do instrumento.
    """
    inicio = time.monotonic()
    estado = {"log_ok": False, "json_ok": False, "fase": None, "status": None, "segundos": 0.0}
    while time.monotonic() - inicio <= timeout_s:
        if not estado["log_ok"] and os.path.isfile(caminho_log):
            try:
                with open(caminho_log, encoding="utf-8", errors="replace") as fh:
                    estado["log_ok"] = "Chainloader startup complete" in fh.read()
            except OSError:
                pass
        if os.path.isfile(caminho_json):
            try:
                with open(caminho_json, encoding="utf-8") as fh:
                    dados = json.load(fh) or {}
                fase = dados.get("fase")
                status = str(dados.get("status") or "").strip().upper()
                estado["json_ok"] = True
                estado["fase"] = fase
                estado["status"] = status
                if (str(fase or "").strip().lower() in FASES_TERMINAIS
                        or status in STATUS_TERMINAIS_ESPERA):
                    break
            except (OSError, ValueError):
                pass
        time.sleep(poll_s)
    estado["segundos"] = round(time.monotonic() - inicio, 3)
    return estado


def pids_da_imagem(imagem):
    """R-4 (CIC-5R): PIDs ATUAIS de uma imagem do Windows, ou `None` se nao der medir.

    `taskkill /F /IM <imagem>` mata TODAS as instancias da imagem — inclusive a que o
    dono ja tinha aberta. Para encerrar SO o que a rodada lancou, o driver fotografa
    os PIDs ANTES de lancar e encerra apenas os NOVOS, por PID. Se a medicao falhar
    (tasklist ausente/sem permissao), devolve `None` e o encerramento por imagem e
    RECUSADO (fail-closed), nunca aplicado às cegas.
    """
    try:
        proc = subprocess.run(["tasklist", "/FI", "IMAGENAME eq %s" % imagem, "/FO", "CSV", "/NH"],
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                              universal_newlines=True, timeout=30)
    except Exception:
        return None
    if proc.returncode != 0:
        return None
    pids = set()
    for linha in (proc.stdout or "").splitlines():
        campos = [c.strip().strip('"') for c in linha.split(",")]
        if len(campos) < 2 or campos[0].lower() != str(imagem).lower():
            continue
        try:
            pids.add(int(campos[1]))
        except ValueError:
            continue
    return pids


def planejar_encerramento(imagem, pids_antes, pids_depois):
    """Decide QUEM encerrar: so os PIDs que NASCERAM depois do lancamento (R-4).

    `pids_antes`/`pids_depois` = `None` significa "nao deu para medir" => RECUSA
    (matar por imagem atingiria todas as instancias). Puro: nao mata nada, so decide
    — o efeito fica em `executar_rodada`, para o teste exercitar a decisao sem tocar
    em processo nenhum.
    """
    if not imagem:
        return {"imagem": None, "modo": "nenhum", "recusado": False, "pids": []}
    if pids_antes is None or pids_depois is None:
        return {"imagem": imagem, "modo": "recusado", "recusado": True, "pids": [],
                "motivo": ("nao foi possivel medir os PIDs da imagem antes/depois do lancamento: "
                           "encerrar por imagem mataria TODAS as instancias (inclusive a que o "
                           "dono ja tinha aberta) — RECUSADO")}
    novos = sorted(pids_depois - pids_antes)
    return {"imagem": imagem, "modo": "por-pid" if novos else "nada-a-encerrar",
            "recusado": False, "pids_antes": sorted(pids_antes),
            "pids_depois": sorted(pids_depois), "pids": novos,
            "motivo": ("encerra SO os PIDs que nasceram nesta rodada; o Popen do lancador e o "
                       "steam.exe, NAO o jogo (no Windows o jogo e processo a parte)")}


def executar_rodada(plano, *, perfil_dir, out_dir, dll_probe, autorizado=False,
                    jogo_disponivel=False, confirmacao=None, steam=None, comando_lancamento=None,
                    appid=APPID, hash_fonte=None, orcamento=120, timeout_s=180, poll_s=0.5,
                    encerrar_imagem=None):
    """CAMINHO EXECUTAVEL: instala o probe no perfil INDICADO (isolado), escreve o
    `.cfg` derivado, lanca pelos ARGUMENTOS de doorstop, espera ESTADO (log + JSON
    novos) e faz o rollback EXATO no `finally`.

    Default NAO AGE: sem `autorizado`+`jogo_disponivel`+`confirmacao=='coleta'` a
    funcao retorna NAO_EXERCITADO ANTES de tocar em qualquer arquivo ou processo —
    e o GATE vem antes de normalizar caminhos (R-2 do CIC-5R): `--executar` sem
    `--perfil`/`--out-dir` tambem sai NAO_EXERCITADO/exit 2, nunca `TypeError`.
    `comando_lancamento` substitui explicitamente a porta (o teste usa um STUB no
    lugar do caminho absoluto do Steam).

    R-4 (CIC-5R): `encerrar_imagem` NAO mata mais por imagem. O `Popen` encerrado no
    `finally` e o LANCADOR (steam.exe), nao o jogo (no Windows o jogo e processo a
    parte); e `taskkill /F /IM <imagem>` mataria TODAS as instancias da imagem —
    inclusive a que o dono ja tinha aberta. Agora o driver fotografia os PIDs da
    imagem ANTES de lancar e encerra SO os PIDs NOVOS; se nao der para medir, o
    encerramento e RECUSADO e registrado em `resultado["encerramento"]`.
    """
    # R-2 (CIC-5R): o GATE vem ANTES de normalizar caminhos. Com `os.path.abspath`
    # antes de `decidir_autorizacao`, `--executar` sem `--perfil` estourava
    # `TypeError` (exit 1) em vez do NAO_EXERCITADO/exit 2 prometido pelo default.
    decisao = decidir_autorizacao(autorizado, jogo_disponivel, confirmacao)
    resultado = {"esquema": ESQUEMA, "rotina": "execucao-runtime", "decisao": decisao,
                 "perfil": perfil_dir, "out_dir": out_dir, "passos": [],
                 "efeitos_colaterais": [], "exit_code": EXIT_NAO_RODOU}
    if not decisao["pode_coletar"]:
        resultado["status"] = "NAO_EXERCITADO"
        resultado["motivo"] = decisao["motivo"]
        return resultado, EXIT_NAO_RODOU
    sem_destino = [nome for nome, valor in (("perfil_dir", perfil_dir), ("out_dir", out_dir))
                   if not str(valor or "").strip()]
    if sem_destino:
        # Autorizado, mas sem destino explicito: NAO adivinha. O perfil do dono NUNCA
        # e default de uma rodada que instala probe.
        resultado["status"] = "NAO_EXERCITADO"
        resultado["motivo"] = ("rodada autorizada sem %s explicito: sem destino nao ha rodada "
                               "(nunca o perfil do dono por acidente)" % ", ".join(sem_destino))
        return resultado, EXIT_NAO_RODOU
    perfil_dir = os.path.abspath(perfil_dir)
    out_dir = os.path.abspath(out_dir)
    resultado["perfil"] = perfil_dir
    resultado["out_dir"] = out_dir
    # A2 (secundario da COR-AUT4R): o plano e validado ANTES de instalar/lancar —
    # um `campos_alvo` invalido barra a rodada SEM tocar no perfil, com o MESMO
    # desfecho do caminho CLI (PLANO_INVALIDO/exit 2). Antes, o defeito so era
    # detectado depois de instalar o probe, escrever o .cfg e lancar.
    try:
        plano = validar_plano(plano)
    except PlanoInvalido as erro:
        resultado["status"] = "PLANO_INVALIDO"
        resultado["motivo"] = "%s: %s" % (type(erro).__name__, erro)
        return resultado, EXIT_NAO_RODOU
    if not (dll_probe and os.path.isfile(dll_probe)):
        resultado["status"] = "NAO_EXERCITADO"
        resultado["motivo"] = "DLL do probe nao encontrada: %r" % (dll_probe,)
        return resultado, EXIT_NAO_RODOU

    dll_probe = os.path.abspath(dll_probe)
    hash_fonte = hash_fonte or _sha256(dll_probe)
    os.makedirs(out_dir, exist_ok=True)

    # A1: a identidade da RODADA e do driver (vai para o cfg e tem de voltar no JSON).
    sessao_rodada = sessao_da_rodada()
    resultado["sessao_rodada"] = sessao_rodada
    # A6: porta opt-in de ida-e-volta (declarada no plano; marcador gerado aqui).
    exigir_ida_volta = _demostrar_do_plano(plano)
    marcador_ida_volta = ("AUT4-IDA-E-VOLTA-%s" % sessao_rodada) if exigir_ida_volta else ""

    caminho_log = os.path.join(perfil_dir, LOG_REL_PADRAO)
    caminho_cfg = os.path.join(perfil_dir, CFG_REL_PADRAO)
    caminho_dll = os.path.join(perfil_dir, PROBE_REL_PADRAO)
    caminho_json = os.path.join(out_dir, "aut4probe.json")
    preloader = os.path.join(perfil_dir, PRELOADER_REL)
    alvos_rel = [PROBE_REL_PADRAO, CFG_REL_PADRAO, LOG_REL_PADRAO]

    antes = snapshot_arquivos(perfil_dir, alvos_rel)
    dirs_antes = snapshot_dirs(perfil_dir, alvos_rel)     # A5: existencia de diretorios
    bkdir = os.path.join(out_dir, "rollback-backup")
    os.makedirs(bkdir, exist_ok=True)
    backups = {}
    for rel in alvos_rel:
        if antes.get(rel) is not None:
            bkp = os.path.join(bkdir, rel.replace(os.sep, "__").replace("/", "__"))
            shutil.copy2(os.path.join(perfil_dir, rel), bkp)
            backups[rel] = bkp

    eh_stub = bool(comando_lancamento)
    cmd = (list(comando_lancamento) if comando_lancamento else [steam or STEAM_PADRAO])
    cmd = cmd + ["-applaunch", appid, "--doorstop-enabled", "true",
                 "--doorstop-target-assembly", preloader]
    proc = None
    pid = None
    pids_antes_imagem = None       # R-4: fotografia dos PIDs da imagem ANTES de lancar
    codigo = EXIT_FALHOU
    try:
        resultado["passos"].append("1. instalar o probe no perfil isolado")
        os.makedirs(os.path.dirname(caminho_dll), exist_ok=True)
        shutil.copy2(dll_probe, caminho_dll)
        resultado["passos"].append("2. escrever o cfg derivado (Autorizado/HashFonte/PerfilDir/Navegar=false/Sessao)")
        texto_cfg = escrever_cfg(caminho_cfg, derivar_config(perfil_dir, out_dir, True,
                                                             hash_fonte=hash_fonte,
                                                             orcamento=orcamento,
                                                             sessao=sessao_rodada,
                                                             demostrar=exigir_ida_volta,
                                                             marcador=marcador_ida_volta))
        with open(os.path.join(out_dir, "cfg-instalado.cfg"), "w", encoding="utf-8") as fh:
            fh.write(texto_cfg)
        resultado["passos"].append("3. arquivar o LogOutput.log anterior (um boot trunca o log)")
        if os.path.isfile(caminho_log):
            shutil.copy2(caminho_log, os.path.join(out_dir, "log-anterior.log"))
            os.remove(caminho_log)
        resultado["passos"].append("4. lancar pelos argumentos de doorstop")
        resultado["lancamento"] = {"argv": cmd, "stub": eh_stub}
        # R-4: fotografa os PIDs da imagem ANTES do lancamento — so os que nascerem
        # depois podem ser encerrados (o dono pode ter o jogo aberto).
        if encerrar_imagem and not eh_stub:
            pids_antes_imagem = pids_da_imagem(encerrar_imagem)
        lancamento_epoca = time.time()          # A1: o JSON desta rodada tem de ser mais novo
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        pid = proc.pid
        resultado["lancamento"]["pid"] = pid
        resultado["lancamento"]["epoca"] = lancamento_epoca
        with open(os.path.join(out_dir, "lancamento.txt"), "w", encoding="utf-8") as fh:
            fh.write("argv=%s\npid=%s\nsessao=%s\n" % (json.dumps(cmd), pid, sessao_rodada))
        resultado["passos"].append("5. esperar ESTADO (log chainloader + JSON do probe), com teto")
        estado = _esperar_estado(caminho_log, caminho_json, timeout_s, poll_s)
        resultado["estado"] = estado
        resultado["passos"].append("6. ler a saida do probe, PROVAR a execucao e provar a atualidade")
        saida = carregar_saida_probe(caminho_json) if os.path.isfile(caminho_json) else None
        if os.path.isfile(caminho_json):
            shutil.copy2(caminho_json, os.path.join(out_dir, "aut4probe-consumido.json"))
        atualidade = provar_atualidade(perfil_dir, out_dir, hash_fonte, saida,
                                       arquivos=["aut4probe.json"] if saida else None)
        resultado["atualidade"] = atualidade
        provas = provas_de_execucao(caminho_json, caminho_log, saida, sessao_rodada,
                                    lancamento_epoca, out_dir=out_dir)
        resultado["provas_execucao"] = provas
        if saida is None:
            resultado["status"] = "NAO_EXERCITADO"
            resultado["motivo"] = "o probe nao deixou saida (%r)" % (estado,)
            codigo = EXIT_NAO_RODOU
        elif not provas["sessao_confere"] or not provas["json_mais_novo"]:
            # A1: a evidencia NAO e desta rodada (JSON anterior/estranho) — nada a confirmar.
            resultado["status"] = "NAO_EXERCITADO"
            resultado["motivo"] = ("sem evidencia DESTA rodada: %s" % "; ".join(provas["faltas"]))
            codigo = EXIT_NAO_RODOU
        elif not provas["ok"]:
            # A1: a rodada aconteceu mas nao completou as provas (log/print) — nao confirma.
            resultado["status"] = "INDETERMINADO"
            resultado["motivo"] = ("provas de execucao incompletas: %s" % "; ".join(provas["faltas"]))
            codigo = EXIT_FALHOU
        else:
            consolidado, codigo = consolidar_probe(saida, plano, alvos=_alvos_do_plano(plano))
            resultado["consolidado"] = consolidado
            # A6: quando o plano PEDE a demonstracao, a prova de ida-e-volta e exigida.
            if exigir_ida_volta:
                ida_volta = saida.get("ida_e_volta") or {}
                # A6 (COR-AUT4-F2): o marcador gerado pelo driver e OBRIGATORIO —
                # `conferiu: true` sem o marcador (ou com outro) NAO conferiu. E o
                # marcador unico que amarra a prova de ida-e-volta a ESTA rodada.
                conferiu = (bool(ida_volta.get("conferiu"))
                            and str(ida_volta.get("marcador") or "") == str(marcador_ida_volta))
                provas["ida_e_volta_ok"] = conferiu
                provas["ida_e_volta"] = ida_volta
                if not conferiu:
                    provas["faltas"].append("sem prova de ida-e-volta (marcador nao lido de volta)")
                    provas["ok"] = False
            else:
                provas["ida_e_volta_ok"] = None
            if not provas["ok"]:
                resultado["status"] = "INDETERMINADO"
                resultado["motivo"] = ("provas de execucao incompletas: %s"
                                       % "; ".join(provas["faltas"]))
                codigo = EXIT_FALHOU
            elif not atualidade["fonte_ok"]:
                resultado["status"] = "INDETERMINADO"
                resultado["motivo"] = "fonte/dll/sessao nao atuais: %s" % "; ".join(atualidade["motivos"])
                codigo = EXIT_FALHOU
            elif consolidado.get("status") == "CONFIRMADA":
                resultado["status"] = "CONCLUIDO"
                codigo = EXIT_OK
            else:
                # INCOMPLETO/ERRO do desfecho (A2/A4) atravessa, nunca vira CONCLUIDO.
                resultado["status"] = ("ERRO" if consolidado.get("status") == "ERRO"
                                       else "INCOMPLETO")
                codigo = EXIT_FALHOU
    except Exception as erro:  # erro de execucao: reverter e relatar, nunca OK
        resultado["status"] = "ERRO"
        resultado["motivo"] = "%s: %s" % (type(erro).__name__, erro)
        codigo = EXIT_FALHOU
    finally:
        # R-4 (CIC-5R): o `Popen` abaixo e o LANCADOR (steam.exe), NAO o jogo — no
        # Windows o jogo e processo a parte (recebe o `--doorstop`). Encerrar a
        # IMAGEM por `taskkill /F /IM` mataria TODAS as instancias da imagem,
        # inclusive a que o dono ja tinha aberta; por isso so encerramos os PIDs que
        # NASCERAM nesta rodada, e RECUSAMOS quando nao da para medi-los.
        if proc is not None:
            try:
                if proc.poll() is None:
                    proc.terminate()
                    try:
                        proc.wait(timeout=10)
                    except Exception:
                        proc.kill()
            except Exception:
                pass
            if encerrar_imagem and not eh_stub:
                plano_enc = planejar_encerramento(encerrar_imagem, pids_antes_imagem,
                                                  pids_da_imagem(encerrar_imagem))
                resultado["encerramento"] = plano_enc
                for alvo_pid in plano_enc["pids"]:
                    try:
                        subprocess.run(["taskkill", "/F", "/PID", str(alvo_pid)],
                                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                       timeout=30)
                    except Exception:
                        pass
        depois = snapshot_arquivos(perfil_dir, alvos_rel)
        dirs_depois = snapshot_dirs(perfil_dir, alvos_rel)      # A5
        plano_rb = planejar_rollback(antes, depois, dirs_antes, dirs_depois)
        acoes = executar_rollback(perfil_dir, plano_rb, backups,
                                  preservar=plano_rb["dirs_pre_existentes"])
        resultado["rollback"] = {"plano": plano_rb, "acoes": acoes}
        resultado["efeitos_colaterais"] = [a for a in acoes if a["acao"] != "sem-backup"]

    resultado["exit_code"] = codigo
    return resultado, codigo


# ------------------------------------------------------------------ CLI

def main(argv=None):
    ap = argparse.ArgumentParser(description="AUT-4 coletor/driver (opt-in, default offline).")
    ap.add_argument("--plano", required=True, help="arquivo do plano de coleta (JSON)")
    ap.add_argument("--out", help="grava o resultado neste arquivo (JSON)")
    ap.add_argument("--autorizado", action="store_true",
                    help="a rodada foi autorizada pelo dono (default: NAO)")
    ap.add_argument("--jogo-disponivel", action="store_true",
                    help="ha acesso ao jogo agora (default: NAO)")
    ap.add_argument("--confirmar-coleta", default=None, metavar="coleta",
                    help="confirmacao explicita da rodada (valor literal 'coleta')")
    ap.add_argument("--procedencia", choices=PROCEDENCIAS, default=None,
                    help="consolida observacoes de --observacoes com esta procedencia")
    ap.add_argument("--observacoes", action="append", default=[],
                    help="arquivo de observacao (repetivel); usado com --procedencia")
    # Costura probe->coletor e caminho executavel (rodada futura autorizada).
    ap.add_argument("--saida-probe", metavar="aut4probe.json",
                    help="consome a saida REAL do probe (injeta sessao/hash do topo e consolida)")
    ap.add_argument("--alvos", nargs="*", default=None,
                    help="campos-alvo do cenario (default: os do plano)")
    ap.add_argument("--executar", action="store_true",
                    help="executa a rodada (instala/lanca/espera/reverte). Exige --autorizado, "
                         "--jogo-disponivel e --confirmar-coleta coleta; sem isso NAO age.")
    ap.add_argument("--perfil", help="perfil ISOLADO onde instalar o probe (nao o do dono sem autorizacao)")
    ap.add_argument("--out-dir", help="pasta de saida da rodada (JSON/PNG/evidencia)")
    ap.add_argument("--dll-probe", help="DLL do probe a instalar (sha vira o HashFonte do cfg)")
    ap.add_argument("--steam", default=STEAM_PADRAO, help="caminho do lancador (default: steam.exe)")
    ap.add_argument("--timeout", type=int, default=180, help="teto da espera de estado, em segundos")
    ap.add_argument("--encerrar-imagem", default=None,
                    help="fecha o jogo por imagem SO em rodada real (nunca contra stub)")
    args = ap.parse_args(argv)

    with open(args.plano, encoding="utf-8") as fh:
        plano = json.load(fh)

    try:
        if args.saida_probe:
            resultado, codigo = consolidar_probe(args.saida_probe, plano, alvos=args.alvos)
        elif args.executar:
            resultado, codigo = executar_rodada(plano, perfil_dir=args.perfil, out_dir=args.out_dir,
                                                dll_probe=args.dll_probe, autorizado=args.autorizado,
                                                jogo_disponivel=args.jogo_disponivel,
                                                confirmacao=args.confirmar_coleta, steam=args.steam,
                                                timeout_s=args.timeout,
                                                encerrar_imagem=args.encerrar_imagem)
        elif args.procedencia and args.observacoes:
            obs = []
            for caminho in args.observacoes:
                with open(caminho, encoding="utf-8") as fh:
                    obs.append(json.load(fh))
            resultado, codigo = consolidar(plano, obs, args.procedencia)
        else:
            rodada, codigo = planejar_rodada(plano, args.autorizado, args.jogo_disponivel,
                                             args.confirmar_coleta)
            resultado = rodada
    except (PlanoInvalido, ObservacaoInvalida) as erro:
        # A2/A3: plano ou observacao fora do contrato NAO pode "rodar" nem virar OK:
        # sai um resultado declarado e exit 2 (nada foi exercitado).
        resultado = {"esquema": ESQUEMA, "status": "PLANO_INVALIDO",
                     "motivo": "%s: %s" % (type(erro).__name__, erro),
                     "dados_sinteticos": False, "observacoes": []}
        codigo = EXIT_NAO_RODOU

    texto = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(texto)
    print(texto)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
