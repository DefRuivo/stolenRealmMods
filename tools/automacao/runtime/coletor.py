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
    prints existentes, com bytes>0 e POSTERIORES ao lancamento) e com o
    instrumento declarando status de conclusao (A1/A4).
  * ARVORE VIGIADA (AUD-1/L1): o rollback nao olha so os nomes do contrato — varre
    `BepInEx/plugins/**` e `BepInEx/config/**` inteiros (o BepInEx varre `plugins/`
    RECURSIVAMENTE: arquivo que nasce ali vira mod carregado), entao arquivo criado
    pela rodada num caminho NAO previsto tambem entra em `criados` e volta. Depois do
    rollback o driver CONFERE a restauracao (`verificar_sem_residuo`): residuo =>
    status RESIDUO / exit != 0, nunca "rodada limpa".
  * o fechamento do jogo e em DUAS ETAPAS (AUD-1/L2): primeiro o fechamento
    GRACIOSO (`CloseMainWindow()` — funciona em rodada sem usuario, onde `taskkill`
    e bloqueado) e so depois o FORCADO por PID; sem medicao dos PIDs a decisao de
    encerrar e RECUSADA (fail-closed).
  * o `LogOutput.log` e arquivado ANTES do lancamento (`backup_do_log`) porque um
    boot TRUNCA o log; o registro do backup (bytes/sha256) e o rollback restauram o
    original byte a byte.

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
# AUD-1/L1: alem dos nomes do contrato, a rodada VIGIA estas arvores inteiras.
# O BepInEx varre `plugins/` RECURSIVAMENTE (memoria do projeto: arquivo que nasce
# ali vira mod carregado), entao "arquivo criado durante a coleta" nao e so o que o
# contrato previu. `config/` guarda os `.cfg` que o probe pode criar sozinho.
ARVORES_VIGIADAS = (os.path.join("BepInEx", "plugins"), os.path.join("BepInEx", "config"))
# AUD-1/L2: prazo do fechamento gracioso antes de cair no forcado por PID.
ESPERA_FECHAMENTO_GRACIOSO_S = 5.0
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

# ------------------------------------------------------------------ detector
# t_a5994af0: o DETECTOR DE AUSENCIA/INDETERMINADO tem um vocabulario FECHADO. A
# pergunta que ele responde nao e "deu certo?", e sim "eu TENHO uma leitura valida?".
# Sem leitura valida nao existe CONFIRMADA: os quatro veredictos negativos abaixo sao
# terminais e nenhum deles carrega exit 0 nem `dados_sinteticos=True`.
VEREDITO_CONFIRMA = "CONFIRMADA"
VEREDITO_NAO_EXERCITADO = "NAO_EXERCITADO"
VEREDITO_AUSENTE = "AUSENTE"
VEREDITO_NO = "NO"
VEREDITO_INCOMPLETO = "INCOMPLETO"
VEREDITOS_NEGATIVOS = (VEREDITO_NO, VEREDITO_AUSENTE,
                       VEREDITO_NAO_EXERCITADO, VEREDITO_INCOMPLETO)

# Traducao status-do-driver -> veredicto-do-detector. TUDO que nao e conclusao
# declarada cai em INCOMPLETO: plano invalido, fixture, residuo, erro, indeterminado
# e — principalmente — status ausente ("silencio nao e aprovacao").
_STATUS_PARA_VEREDITO = {
    "CONCLUIDO": VEREDITO_CONFIRMA,
    "CONFIRMADA": VEREDITO_CONFIRMA,
    "NAO_EXERCITADO": VEREDITO_NAO_EXERCITADO,
    "AUSENTE": VEREDITO_AUSENTE,
    "NO": VEREDITO_NO,
    "INCOMPLETO": VEREDITO_INCOMPLETO,
    "INDETERMINADO": VEREDITO_INCOMPLETO,
    "ERRO": VEREDITO_INCOMPLETO,
    "FIXTURE": VEREDITO_INCOMPLETO,
    "PLANO_INVALIDO": VEREDITO_INCOMPLETO,
    "RESIDUO": VEREDITO_INCOMPLETO,
}


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


def decidir_autorizacao(autorizado, jogo_disponivel, confirmacao=None, frente_ativa=False):
    """Decide se a rodada pode coletar. Default: NAO_EXERCITADO, sem dado sintetico.

    `frente_ativa=True` declara que OUTRA frente ja esta controlando o jogo: a regra
    "uma unica frente por vez" e uma trava, nao uma recomendacao — a rodada sai
    NAO_EXERCITADO mesmo autorizada.
    """
    base = {"dados_sinteticos": False, "observacoes": [], "screenshot": None}
    if frente_ativa:
        base.update({"status": "NAO_EXERCITADO", "pode_coletar": False, "modo": "frente-duplicada",
                     "motivo": "OUTRA frente ja controla o jogo: uma unica frente por vez "
                               "(NAO_EXERCITADO, jamais dado fabricado)"})
        return base
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


def caminhos_vigiados(perfil_dir, explicitos=()):
    """AUD-1/L1: o que a rodada VIGIA = os nomes do contrato + as arvores inteiras.

    `snapshot_arquivos` de lista fechada nao enxerga o arquivo que o probe cria num
    caminho que o contrato nao previu — e o BepInEx varre `plugins/` RECURSIVAMENTE:
    arquivo que nasce ali vira mod carregado. Vigiar `BepInEx/plugins/**` e
    `BepInEx/config/**` inteiros e o que faz "inclusive arquivos criados durante a
    coleta" ser verdade em vez de intencao.
    """
    rels = {str(r) for r in (explicitos or ())}
    for sub in ARVORES_VIGIADAS:
        base = os.path.join(perfil_dir, sub)
        if not os.path.isdir(base):
            continue
        for pasta, _dirs, arquivos in os.walk(base):
            for nome in arquivos:
                rels.add(os.path.relpath(os.path.join(pasta, nome), perfil_dir))
    return sorted(rels)


def backup_do_log(caminho_log, destino_dir, nome="log-anterior.log"):
    """Arquiva o `LogOutput.log` ANTES do lancamento e o REMOVE do perfil.

    Um boot TRUNCA o log (`File.Create`), entao o log anterior e o unico jeito de
    saber o que havia antes — e o rollback devolve o original a partir do backup.
    Devolve o REGISTRO do backup (origem/existia/bytes/sha256) para o manifesto:
    ausencia de log e declarada, nunca inventada.
    """
    registro = {"origem": caminho_log, "existia": os.path.isfile(caminho_log)}
    if registro["existia"]:
        os.makedirs(destino_dir, exist_ok=True)
        destino = os.path.join(destino_dir, nome)
        shutil.copy2(caminho_log, destino)
        registro["backup"] = destino
        registro["bytes"] = os.path.getsize(destino)
        registro["sha256"] = _sha256(destino)
        os.remove(caminho_log)
        registro["acao"] = ("arquivado como %s e removido do perfil (o boot desta "
                            "rodada passa a ser o unico log lido)" % nome)
    else:
        registro["acao"] = "nao havia log anterior: nada a arquivar"
    return registro


def montar_manifest_da_rodada(out_dir, perfil_dir, relativos, antes, depois, backups=None):
    """Auditoria da rodada: (a) artefatos de evidencia, (b) arquivos tocados, (c) backups.

    (a) varre o `out_dir` e descreve cada artefato por bytes/sha256; (b) confronta o
    estado ANTES/DEPOIS de cada arquivo vigiado do perfil e o CLASSIFICA
    (criado/modificado/removido/intocado) — inclusive o que a rodada criou num
    caminho nao previsto; (c) nomeia o backup que permite restaurar cada arquivo.
    Nada e inventado: o que esta em disco e medido, o que falta e declarado ausente.
    """
    artefatos = []
    for pasta, _dirs, arquivos in os.walk(out_dir):
        for nome in sorted(arquivos):
            caminho = os.path.join(pasta, nome)
            item = {"arquivo": os.path.relpath(caminho, out_dir)}
            try:
                item["bytes"] = os.path.getsize(caminho)
                item["sha256"] = _sha256(caminho)
            except OSError as erro:
                item["erro"] = str(erro)
            artefatos.append(item)
    arquivos_perfil = []
    for rel in sorted(set(list(antes or {})) | set(list(depois or {}))):
        de_antes = (antes or {}).get(rel)
        de_depois = (depois or {}).get(rel)
        if de_antes is None and de_depois is not None:
            estado = "criado"
        elif de_antes is not None and de_depois is None:
            estado = "removido"
        elif de_antes != de_depois:
            estado = "modificado"
        else:
            estado = "intocado"
        arquivos_perfil.append({"arquivo": rel, "estado": estado,
                                "sha256_antes": de_antes, "sha256_depois": de_depois,
                                "backup": (backups or {}).get(rel)})
    return {
        "esquema": ESQUEMA, "perfil": perfil_dir, "out_dir": out_dir,
        "artefatos": sorted(artefatos, key=lambda i: i["arquivo"]),
        "total_artefatos": len(artefatos),
        "arquivos_vigiados": arquivos_perfil,
        "criados": [i["arquivo"] for i in arquivos_perfil if i["estado"] == "criado"],
        "modificados": [i["arquivo"] for i in arquivos_perfil if i["estado"] == "modificado"],
        "removidos": [i["arquivo"] for i in arquivos_perfil if i["estado"] == "removido"],
    }


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


# ------------------------------------------------- identidade do resultado (t_a5994af0)

def identificacao_do_resultado(*, dll_probe=None, hash_fonte=None, configuracao=None,
                               cenario=None, observado=None, esperado=None,
                               evidencia=None, lacunas=None):
    """Bloco de IDENTIDADE: todo veredito diz QUAL instrumento mediu, com QUE
    configuracao, em QUE cenario, o que OBSERVOU x o que ESPERAVA, qual a EVIDENCIA
    (artefato em disco) e quais LACUNAS sobraram.

    Sem este bloco um "NO" nao e auditavel: nao da para saber de qual build/fonte,
    com qual config, em qual cenario a negativa saiu. O hash de fonte e o sha256 da
    DLL do probe (medido em disco, nunca "compila igual").
    """
    ident = {
        "dll_sha256": None,
        "hash_fonte": str(hash_fonte).strip() or None if hash_fonte else None,
        "configuracao": configuracao if configuracao is not None else None,
        "cenario": cenario if cenario is not None else None,
        "observado": observado if observado is not None else None,
        "esperado": esperado if esperado is not None else None,
        "evidencia": evidencia if evidencia is not None else None,
        "lacunas": sorted(str(l) for l in (lacunas or [])),
    }
    if dll_probe and os.path.isfile(dll_probe):
        ident["dll_sha256"] = _sha256(dll_probe)
        if not ident["hash_fonte"]:
            ident["hash_fonte"] = ident["dll_sha256"]
    return ident


def veredito_do_status(status):
    """Traduz o status do driver para o vocabulario do detector.

    Status DESCONHECIDO — inclusive `None` (silencio) — NAO confirma: vira INCOMPLETO
    ("silencio nao e aprovacao"). So `CONCLUIDO`/`CONFIRMADA` viram CONFIRMADA.
    """
    return _STATUS_PARA_VEREDITO.get(str(status or "").strip().upper(), VEREDITO_INCOMPLETO)


def _esperados_do_cenario(plano, cenario=None):
    """Expectativas DECLARADAS do plano: `{campo: valor_esperado}`.

    Aceita no topo (`plano["esperado"]`) e em cada cenario (`cenarios[i]["esperado"]`),
    como `campos_alvo` (S-2: nenhum cenario pode ser descartado em silencio). Sem
    expectativa declarada nao ha o que NEGAR: o detector so pode confirmar/declarar
    ausencia/lacuna.
    """
    if not isinstance(plano, dict):
        return {}
    if cenario is not None:
        for c in plano.get("cenarios") or []:
            if isinstance(c, dict) and c.get("nome") == cenario:
                return dict(c.get("esperado") or {})
        return {}
    esperado = dict(plano.get("esperado") or {})
    for c in plano.get("cenarios") or []:
        if isinstance(c, dict) and isinstance(c.get("esperado"), dict):
            esperado.update(c["esperado"])
    return esperado


def decidir_com_jogo_aberto(*, jogo_aberto, probe_carregado, reiniciar_autorizado=False):
    """Rodada com o jogo JA ABERTO: so LE o que a instrumentacao JA CARREGADA entrega.

    Com o jogo aberto NAO se instala probe. Se o probe nao esta carregado nesta sessao,
    nao ha o que ler: a rodada declara REINICIO NECESSARIO e sai NAO_EXERCITADO. O
    driver NUNCA promete hot-reload (`hot_reload: False` sempre) — trocar a DLL exigiria
    reiniciar o jogo, e reiniciar o jogo exige autorizacao explicita do dono.
    """
    base = {"jogo_aberto": bool(jogo_aberto), "probe_carregado": bool(probe_carregado),
            "hot_reload": False, "reiniciar_autorizado": bool(reiniciar_autorizado),
            "reinicio_necessario": False, "dados_sinteticos": False}
    if not jogo_aberto:
        base.update({"status": "NAO_EXERCITADO", "pode_ler": False,
                     "motivo": "nao ha jogo aberto: nada a ler — sem jogo nao se inventa leitura"})
        return base
    if not probe_carregado:
        base.update({"status": "NAO_EXERCITADO", "pode_ler": False, "reinicio_necessario": True,
                     "motivo": "o probe NAO esta carregado nesta sessao: exigiria REINICIAR o jogo "
                               "para carregar a instrumentacao (nao ha hot-reload); reiniciar exige "
                               "autorizacao explicita do dono"})
        return base
    base.update({"status": "PRONTO_PARA_LER", "pode_ler": True,
                 "motivo": "jogo aberto COM o probe carregado: a rodada so LE — nao instala, nao "
                           "reinicia, nao encerra"})
    return base


# --------------------------------------------------- detector que sabe dizer NAO

def detectar_leitura(observacoes=None, plano=None, *, exercitado=True, procedencia="runtime",
                     contexto=None, alvos=None, status_probe=None, fase=None, provas=None,
                     reinicio_necessario=False, cenario=None, configuracao=None,
                     dll_probe=None, hash_fonte=None, evidencia=None, motivo=None):
    """DETECTOR DE AUSENCIA/INDETERMINADO — o detector que SABE DIZER NAO.

    Devolve `(resultado, exit_code)` com o veredito num vocabulario FECHADO:
    `CONFIRMADA` | `NO` | `AUSENTE` | `NAO_EXERCITADO` | `INCOMPLETO`. As regras sao
    aplicadas nesta ordem (a primeira que casa manda):

      1. `reinicio_necessario` ou `exercitado=False`  -> NAO_EXERCITADO (exit 2)
         (sem rodada/sem instrumentacao carregada: nada foi lido)
      2. provas de execucao incompletas / instrumento em estado terminal de falha /
         instrumento sem status de conclusao          -> INCOMPLETO (exit 1)
      3. nenhuma observacao / nenhum campo-alvo lido   -> AUSENTE (exit 1)
      4. leitura VALIDA e a expectativa declarada NAO casa -> NO (exit 1)
         (NO exige leitura: campo nao lido NAO vira NO, vira AUSENTE)
      5. lacuna (alvo declarado nao lido)              -> INCOMPLETO (exit 1)
      6. so entao                                      -> CONFIRMADA (exit 0)

    INVARIANTE: sem leitura valida NENHUM caminho devolve CONFIRMADA, e
    `dados_sinteticos` e sempre `False` — o detector nunca fabrica dado. Todo resultado
    carrega o bloco `identificacao` (hash de fonte/DLL, configuracao, cenario,
    observado/esperado, evidencia e lacunas).
    """
    observacoes = list(observacoes or [])
    if alvos is None:
        alvos = _alvos_do_plano(plano)
    else:
        alvos = validar_alvos(alvos)
    esperados = _esperados_do_cenario(plano, cenario)
    ident = identificacao_do_resultado(
        dll_probe=dll_probe, hash_fonte=hash_fonte, configuracao=configuracao,
        cenario=(cenario if cenario is not None
                 else (plano.get("nome") if isinstance(plano, dict) else None)),
        observado=len(observacoes), esperado=(esperados or None), evidencia=evidencia)

    def _fecha(veredito, codigo, texto, lacunas=(), observado=None, esperado=None,
               normalizadas=None, ident_extra=None):
        resultado = {
            "esquema": ESQUEMA,
            "detector": "ausencia/indeterminado",
            "veredito": veredito,
            "status": veredito,              # compatibilidade com os status do driver
            "negativo": veredito in VEREDITOS_NEGATIVOS,
            "incompleto": veredito != VEREDITO_CONFIRMA,
            "dados_sinteticos": False,       # NUNCA fabrica
            "hot_reload": False,             # nunca promete hot-reload
            "motivo": texto,
            "lacunas": sorted(str(l) for l in lacunas),
            "observado": observado,
            "esperado": esperado if esperado is not None else (esperados or None),
            "observacoes": normalizadas or [],
            "identificacao": dict(ident, **(ident_extra or {})),
        }
        return resultado, codigo

    if reinicio_necessario:
        return _fecha(VEREDITO_NAO_EXERCITADO, EXIT_NAO_RODOU,
                      "a instrumentacao necessaria NAO esta carregada: a rodada exige REINICIO "
                      "(sem hot-reload — nada e prometido, nada e lido)", ident_extra={"reinicio": True})
    if str(procedencia or "").strip().lower() == "fixture":
        # FIXTURE nao prova runtime: mesmo com a expectativa casando, o veredito NUNCA
        # confirma. A leitura rotulada e material de teste, nao evidencia de jogo.
        return _fecha(VEREDITO_INCOMPLETO, EXIT_NAO_RODOU,
                      "procedencia 'fixture': fixture rotulada NAO prova runtime (nunca confirma)")
    if not exercitado:
        return _fecha(VEREDITO_NAO_EXERCITADO, EXIT_NAO_RODOU,
                      motivo or "a leitura NAO foi exercitada (sem autorizacao/sem acesso ao jogo): "
                                "NAO_EXERCITADO, nenhum dado fabricado")
    if provas is not None and not provas.get("ok"):
        return _fecha(VEREDITO_INCOMPLETO, EXIT_FALHOU,
                      "provas de execucao incompletas: %s" % "; ".join(provas.get("faltas") or []))
    st = str(status_probe or "").strip().upper()
    fa = str(fase or "").strip().lower()
    if st in STATUS_PROBE_FALHA or fa in FASES_PROBE_FALHA:
        return _fecha(VEREDITO_INCOMPLETO, EXIT_FALHOU,
                      "estado terminal de falha do instrumento (%s / %s): nao confirma desfecho"
                      % (st or "sem status", fa or "sem fase"))
    # t_a5994af0 (AUT-4R rodada 1): o status de conclusao e OBRIGATORIO — ausente/vazio
    # NAO pode passar. Antes, o curto-circuito `if st and ...` deixava `status` ausente
    # ou "" escapar para CONFIRMADA, contradizendo esta regra 2, o irmao
    # `consolidar_probe` (que trata silencio como INCOMPLETO) e `veredito_do_status(None)`.
    # "silencio nao e aprovacao": sem status declarado o detector NAO confirma.
    if st not in STATUS_PROBE_OK:
        return _fecha(VEREDITO_INCOMPLETO, EXIT_FALHOU,
                      "o instrumento nao declarou status de conclusao (%r): silencio nao e "
                      "aprovacao" % st)
    if not observacoes:
        return _fecha(VEREDITO_AUSENTE, EXIT_FALHOU,
                      "nenhuma observacao foi lida: AUSENTE (o objeto nao foi lido — nao 'passou')")

    normalizadas = [
        normalizar_observacao(
            o, procedencia,
            rotulo_fixture=(o.get("rotulo_fixture") if isinstance(o, dict) else None),
            contexto=contexto, alvos=alvos)
        for o in observacoes
    ]
    alvos_efetivos = set(alvos) if alvos is not None else set(CAMPOS)
    lidos = sorted({c for n in normalizadas for c in alvos_efetivos
                    if n["campos"].get(c, {}).get("estado") == "PRESENTE"})
    lacunas = sorted({l for n in normalizadas for l in n["lacunas"]})
    if not lidos:
        return _fecha(VEREDITO_AUSENTE, EXIT_FALHOU,
                      "nenhum campo-alvo foi lido (vazios/AUSENTES: %s): AUSENTE"
                      % ", ".join(sorted(alvos_efetivos)),
                      lacunas=lacunas, observado="AUSENTE", normalizadas=normalizadas)

    negados = []
    for campo, valor in sorted(esperados.items()):
        valores = [n["campos"].get(campo, {}).get("valor") for n in normalizadas
                   if n["campos"].get(campo, {}).get("estado") == "PRESENTE"]
        if not valores:
            return _fecha(VEREDITO_AUSENTE, EXIT_FALHOU,
                          "a expectativa de %r nao foi lida: AUSENTE (nao da para dizer NO sobre "
                          "campo que o probe nao leu)" % campo,
                          lacunas=sorted(set(lacunas) | {campo}), normalizadas=normalizadas)
        if not any(v == valor for v in valores):
            negados.append((campo, valor, valores))
    if negados:
        return _fecha(VEREDITO_NO, EXIT_FALHOU,
                      "leitura VALIDA e a expectativa NAO casa: NO (%s)"
                      % "; ".join("%s esperado %r, lido %r" % (c, e, v) for c, e, v in negados),
                      lacunas=lacunas, observado=[v for _c, _e, v in negados],
                      esperado={c: e for c, e, _v in negados}, normalizadas=normalizadas)
    if lacunas:
        return _fecha(VEREDITO_INCOMPLETO, EXIT_FALHOU,
                      "ha lacuna: alvo(s) nao lido(s) %s — AUSENTE/INDETERMINADO nunca e OK"
                      % ", ".join(lacunas), lacunas=lacunas, normalizadas=normalizadas)
    observado_final = {}
    for n in normalizadas:
        for c in lidos:
            if n["campos"].get(c, {}).get("estado") == "PRESENTE":
                observado_final.setdefault(c, []).append(n["campos"][c]["valor"])
    return _fecha(VEREDITO_CONFIRMA, EXIT_OK,
                  "leitura valida e a expectativa declarada casa" if esperados
                  else "leitura valida (sem expectativa declarada: nada a negar)",
                  observado=observado_final, normalizadas=normalizadas)


# ------------------------------------------------------------------ driver

def planejar_rodada(plano, autorizado, jogo_disponivel, confirmacao=None, perfil_dir=None,
                    frente_ativa=False):
    """Plano completo da rodada (instalar/ler/remover). Offline devolve NAO_EXERCITADO."""
    plano = validar_plano(plano)
    decisao = decidir_autorizacao(autorizado, jogo_disponivel, confirmacao,
                                  frente_ativa=frente_ativa)
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


def verificar_sem_residuo(raiz, relativos, antes, dirs_antes=None):
    """AUD-1: prova de RESTAURACAO EXATA (pos-rollback), sem efeito residual.

    Confronta o estado AGORA com o estado de ANTES e nomeia cada divergencia:
    arquivo criado que sobrou (`residuos`), restaurado com hash diferente
    (`divergentes`), removido que nao voltou (`faltando`) e diretorio criado pela
    rodada que sobrou (`dirs_residuo`). `limpo` so e True com as quatro listas
    vazias — e o driver usa isso para nao apresentar rodada suja como limpa.
    """
    agora = snapshot_arquivos(raiz, caminhos_vigiados(raiz, relativos))
    dirs_agora = snapshot_dirs(raiz, caminhos_vigiados(raiz, relativos))
    antes = antes or {}
    residuos = sorted(k for k in agora if k not in antes)
    divergentes = sorted(k for k in agora if k in antes and agora[k] != antes[k])
    faltando = sorted(k for k in antes if k not in agora)
    dirs_residuo = sorted(set(dirs_agora) - set(dirs_antes or ()))
    return {
        "limpo": not (residuos or divergentes or faltando or dirs_residuo),
        "residuos": residuos, "divergentes": divergentes, "faltando": faltando,
        "dirs_residuo": dirs_residuo, "vigiados_agora": sorted(agora),
    }


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


def comandos_de_fechamento(pid):
    """AUD-1/L2: como fechar UM PID, em ORDEM — o GRACIOSO primeiro.

    `taskkill` e bloqueado em rodada sem usuario (memoria do projeto) e matar por
    imagem atinge TODAS as instancias; por isso o primeiro caminho e pedir ao jogo
    que feche a propria janela (`CloseMainWindow()`) e o forcado por PID fica como
    FALLBACK, so quando o processo continua vivo. Puro: devolve os comandos, nao os
    executa.
    """
    pid = int(pid)
    return [
        {"modo": "gracioso",
         "argv": ["powershell", "-NoProfile", "-NonInteractive", "-Command",
                  "(Get-Process -Id %d -ErrorAction SilentlyContinue).CloseMainWindow()" % pid],
         "motivo": "fecha a janela principal (CloseMainWindow) — nao depende de taskkill"},
        {"modo": "forcado", "argv": ["taskkill", "/F", "/PID", str(pid)],
         "motivo": "fallback: SO o PID que nasceu nesta rodada"},
    ]


def _pid_vivo(pid):
    """True/False se o PID existe agora; None quando NAO deu para medir.

    A duvida e da MEDICAO (tasklist ausente/sem permissao), nunca da decisao: quem
    nao mediu nao decide encerrar nada por conta propria.
    """
    try:
        proc = subprocess.run(["tasklist", "/FI", "PID eq %d" % int(pid), "/FO", "CSV", "/NH"],
                              stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                              universal_newlines=True, timeout=30)
    except Exception:
        return None
    if proc.returncode != 0:
        return None
    for linha in (proc.stdout or "").splitlines():
        campos = [c.strip().strip('"') for c in linha.split(",")]
        if len(campos) >= 2:
            try:
                if int(campos[1]) == int(pid):
                    return True
            except ValueError:
                continue
    return False


def encerrar_processos(plano_encerramento, executar=None, pid_vivo=None,
                       espera_s=ESPERA_FECHAMENTO_GRACIOSO_S, dormir=time.sleep):
    """AUD-1/L2: executa a decisao de `planejar_encerramento` — gracioso -> forcado.

    RECUSA (ou nada a encerrar) nao executa NADA: fail-closed. Para cada PID tenta o
    gracioso, espera `espera_s` e SO escala para o forcado se o processo continuar
    vivo (vivo=False para). `executar`/`pid_vivo`/`dormir` sao injetaveis para o
    teste provar a ORDEM e o fallback sem fechar processo nenhum.
    """
    acoes = []
    if not isinstance(plano_encerramento, dict):
        return acoes
    if plano_encerramento.get("recusado") or not plano_encerramento.get("pids"):
        return acoes
    aplicar = executar or (lambda argv: subprocess.run(
        argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30))
    medir = pid_vivo or _pid_vivo
    for pid in plano_encerramento["pids"]:
        registro = {"pid": pid, "tentativas": [], "fechado": None}
        for comando in comandos_de_fechamento(pid):
            tentativa = {"modo": comando["modo"], "argv": comando["argv"], "ok": False}
            try:
                aplicar(comando["argv"])
                tentativa["ok"] = True
            except Exception as erro:
                tentativa["erro"] = "%s: %s" % (type(erro).__name__, erro)
            registro["tentativas"].append(tentativa)
            if comando["modo"] == "gracioso" and espera_s:
                dormir(espera_s)
            vivo = medir(pid)
            registro["fechado"] = (vivo is False)
            if vivo is False:
                break                      # ja saiu: nao escala para o forcado
        acoes.append(registro)
    return acoes


def executar_rodada(plano, *, perfil_dir, out_dir, dll_probe, autorizado=False,
                    jogo_disponivel=False, confirmacao=None, steam=None, comando_lancamento=None,
                    appid=APPID, hash_fonte=None, orcamento=120, timeout_s=180, poll_s=0.5,
                    encerrar_imagem=None, fechar_executar=None, pid_vivo=None,
                    pids_medir=None, frente_ativa=False):
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

    AUD-1/L1: a rodada VIGIA `BepInEx/plugins/**` e `BepInEx/config/**` inteiros
    (`caminhos_vigiados`) — arquivo criado pelo probe em caminho nao previsto entra
    em `criados` e volta no rollback; `resultado["manifest"]` descreve artefatos,
    estado antes/depois de cada arquivo vigiado e os backups; e
    `resultado["restauracao"]` prova (pos-rollback) que o perfil voltou EXATO — se
    sobrar residuo, o status vira `RESIDUO`/exit != 0, nunca "rodada limpa".

    AUD-1/L2: o jogo e fechado em DUAS ETAPAS (`encerrar_processos`): gracioso
    (`CloseMainWindow`) e, so se o PID continuar vivo, forcado por PID. `pid_vivo`/
    `fechar_executar`/`pids_medir` sao injetaveis para o teste exercitar a ordem e o
    fallback offline, sem fechar processo nenhum.
    """
    # R-2 (CIC-5R): o GATE vem ANTES de normalizar caminhos. Com `os.path.abspath`
    # antes de `decidir_autorizacao`, `--executar` sem `--perfil` estourava
    # `TypeError` (exit 1) em vez do NAO_EXERCITADO/exit 2 prometido pelo default.
    decisao = decidir_autorizacao(autorizado, jogo_disponivel, confirmacao,
                                  frente_ativa=frente_ativa)
    resultado = {"esquema": ESQUEMA, "rotina": "execucao-runtime", "decisao": decisao,
                 "perfil": perfil_dir, "out_dir": out_dir, "passos": [],
                 "efeitos_colaterais": [], "exit_code": EXIT_NAO_RODOU}

    def _fechar(res, codigo):
        """Fecha o resultado com IDENTIDADE + veredito do detector (t_a5994af0).

        Todo resultado do caminho executavel identifica hash de fonte/DLL, configuracao,
        cenario, observado/esperado, evidencia e lacunas — e traz o veredito no
        vocabulario do detector (nunca CONFIRMADA sem status de conclusao). O driver
        NUNCA promete hot-reload: `hot_reload` e sempre False.
        """
        veredito = veredito_do_status(res.get("status"))
        consolidado = res.get("consolidado") or {}
        res["detector"] = {"veredito": veredito, "negativo": veredito in VEREDITOS_NEGATIVOS,
                           "dados_sinteticos": False, "hot_reload": False}
        res["hot_reload"] = False
        res["identificacao"] = identificacao_do_resultado(
            dll_probe=(dll_probe if isinstance(dll_probe, str) and os.path.isfile(dll_probe) else None),
            hash_fonte=(hash_fonte if isinstance(hash_fonte, str) else None),
            configuracao=res.get("configuracao"),
            cenario=(plano.get("nome") if isinstance(plano, dict) else None),
            observado=(len(consolidado.get("observacoes") or []) or None),
            esperado=(_esperados_do_cenario(plano) or None),
            evidencia=res.get("out_dir"),
            lacunas=(consolidado.get("lacunas") or []))
        res["exit_code"] = codigo
        return res, codigo

    if not decisao["pode_coletar"]:
        resultado["status"] = "NAO_EXERCITADO"
        resultado["motivo"] = decisao["motivo"]
        return _fechar(resultado, EXIT_NAO_RODOU)
    sem_destino = [nome for nome, valor in (("perfil_dir", perfil_dir), ("out_dir", out_dir))
                   if not str(valor or "").strip()]
    if sem_destino:
        # Autorizado, mas sem destino explicito: NAO adivinha. O perfil do dono NUNCA
        # e default de uma rodada que instala probe.
        resultado["status"] = "NAO_EXERCITADO"
        resultado["motivo"] = ("rodada autorizada sem %s explicito: sem destino nao ha rodada "
                               "(nunca o perfil do dono por acidente)" % ", ".join(sem_destino))
        return _fechar(resultado, EXIT_NAO_RODOU)
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
        return _fechar(resultado, EXIT_NAO_RODOU)
    if not (dll_probe and os.path.isfile(dll_probe)):
        resultado["status"] = "NAO_EXERCITADO"
        resultado["motivo"] = "DLL do probe nao encontrada: %r" % (dll_probe,)
        return _fechar(resultado, EXIT_NAO_RODOU)

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

    # AUD-1/L1: vigia o contrato MAIS as arvores inteiras — arquivo que o probe criar
    # num caminho nao previsto entra em `criados` (e o BepInEx varre plugins/ recursivo).
    vigiados_antes = caminhos_vigiados(perfil_dir, alvos_rel)
    antes = snapshot_arquivos(perfil_dir, vigiados_antes)
    dirs_antes = snapshot_dirs(perfil_dir, vigiados_antes)   # A5: existencia de diretorios
    bkdir = os.path.join(out_dir, "rollback-backup")
    os.makedirs(bkdir, exist_ok=True)
    backups = {}
    for rel in sorted(antes):
        bkp = os.path.join(bkdir, rel)       # espelha a arvore (sem colisao de basename)
        os.makedirs(os.path.dirname(bkp), exist_ok=True)
        try:
            shutil.copy2(os.path.join(perfil_dir, rel), bkp)
            backups[rel] = bkp
        except OSError:
            pass                             # sem backup: o rollback declara "sem-backup"

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
        configuracao = derivar_config(perfil_dir, out_dir, True, hash_fonte=hash_fonte,
                                      orcamento=orcamento, sessao=sessao_rodada,
                                      demostrar=exigir_ida_volta, marcador=marcador_ida_volta)
        resultado["configuracao"] = configuracao      # t_a5994af0: a config entra na IDENTIDADE
        texto_cfg = escrever_cfg(caminho_cfg, configuracao)
        with open(os.path.join(out_dir, "cfg-instalado.cfg"), "w", encoding="utf-8") as fh:
            fh.write(texto_cfg)
        resultado["passos"].append("3. arquivar o LogOutput.log anterior (um boot trunca o log)")
        resultado["backup_log"] = backup_do_log(caminho_log, out_dir)
        resultado["passos"].append("4. lancar pelos argumentos de doorstop")
        resultado["lancamento"] = {"argv": cmd, "stub": eh_stub}
        # R-4: fotografa os PIDs da imagem ANTES do lancamento — so os que nascerem
        # depois podem ser encerrados (o dono pode ter o jogo aberto).
        if encerrar_imagem:
            pids_antes_imagem = (pids_medir or pids_da_imagem)(encerrar_imagem)
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
            if encerrar_imagem:
                medir_imagem = pids_medir or pids_da_imagem
                plano_enc = planejar_encerramento(encerrar_imagem, pids_antes_imagem,
                                                  medir_imagem(encerrar_imagem))
                # AUD-1/L2: gracioso primeiro; forcado por PID so se o processo continuar vivo.
                plano_enc["acoes"] = encerrar_processos(plano_enc, executar=fechar_executar,
                                                        pid_vivo=pid_vivo)
                resultado["encerramento"] = plano_enc
        vigiados_depois = caminhos_vigiados(perfil_dir, alvos_rel)
        depois = snapshot_arquivos(perfil_dir, vigiados_depois)
        dirs_depois = snapshot_dirs(perfil_dir, vigiados_depois)      # A5
        plano_rb = planejar_rollback(antes, depois, dirs_antes, dirs_depois)
        try:
            acoes = executar_rollback(perfil_dir, plano_rb, backups,
                                      preservar=plano_rb["dirs_pre_existentes"])
        except Exception as erro:
            # AUD-1: o rollback FALHOU (arquivo travado / sem permissao). Nao derrubar
            # o driver: registra o erro e deixa a PROVA de restauracao acusar — o
            # veredito vira RESIDUO/exit != 0, nunca "rodada limpa".
            acoes = []
            resultado["rollback_erro"] = "%s: %s" % (type(erro).__name__, erro)
        resultado["rollback"] = {"plano": plano_rb, "acoes": acoes}
        # AUD-1: PROVA pos-rollback de que o perfil voltou ao estado de antes.
        resultado["restauracao"] = verificar_sem_residuo(
            perfil_dir, caminhos_vigiados(perfil_dir, alvos_rel), antes, dirs_antes)
        resultado["manifest"] = montar_manifest_da_rodada(out_dir, perfil_dir,
                                                          vigiados_depois, antes, depois,
                                                          backups)
        resultado["efeitos_colaterais"] = [a for a in acoes if a["acao"] != "sem-backup"]

    # AUD-1: restauracao NAO exata => a rodada NAO pode ser apresentada como limpa.
    restauracao = resultado.get("restauracao") or {}
    if restauracao and not restauracao.get("limpo"):
        sujeira = ((restauracao.get("residuos") or []) + (restauracao.get("divergentes") or [])
                   + (restauracao.get("faltando") or []) + (restauracao.get("dirs_residuo") or []))
        resultado["status"] = "RESIDUO"
        resultado["motivo"] = ("restauracao NAO exata: efeito residual no perfil (%s)"
                               % "; ".join(str(x) for x in sujeira))
        codigo = EXIT_FALHOU

    resultado["exit_code"] = codigo
    return _fechar(resultado, codigo)


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
    # t_a5994af0: detector de ausencia/indeterminado e a trava da frente unica.
    ap.add_argument("--detectar", action="store_true",
                    help="com --saida-probe: julga com o DETECTOR (veredito CONFIRMADA/NO/AUSENTE/"
                         "NAO_EXERCITADO/INCOMPLETO) em vez de so consolidar")
    ap.add_argument("--frente-ativa", action="store_true",
                    help="declara que OUTRA frente ja controla o jogo: a rodada NAO age (uma frente por vez)")
    ap.add_argument("--jogo-aberto", action="store_true",
                    help="o jogo JA esta aberto: com jogo aberto so se LE instrumentacao ja carregada")
    ap.add_argument("--probe-carregado", action="store_true",
                    help="com --jogo-aberto: o probe JA esta carregado nesta sessao "
                         "(sem ele a rodada declara REINICIO NECESSARIO, sem hot-reload)")
    args = ap.parse_args(argv)

    with open(args.plano, encoding="utf-8") as fh:
        plano = json.load(fh)

    try:
        if args.jogo_aberto:
            resultado = decidir_com_jogo_aberto(jogo_aberto=True,
                                                probe_carregado=args.probe_carregado)
            codigo = EXIT_OK if resultado["pode_ler"] else EXIT_NAO_RODOU
        elif args.detectar:
            # O detector julga a saida do probe: sem leitura nao ha o que julgar e o
            # caminho sai NAO_EXERCITADO (nunca um veredito inventado).
            #
            # LACUNA DECLARADA (AUT-4R rodada 1): este lane LE um artefato JA EXISTENTE e
            # NAO passa `provas`: nem `provas.ok` nem a atualidade da sessao sao checados
            # aqui (a prova de execucao — sessao desta rodada + log + prints — so existe no
            # caminho `--executar`, onde o driver GERA a sessao e o lancamento). O QUE ESTE
            # LANE GARANTE: o status de conclusao do instrumento e OBRIGATORIO — ausente/
            # vazio sai INCOMPLETO/exit 1 ("silencio nao e aprovacao", alinhado com
            # consolidar_probe). Quem precisar da prova de execucao usa `--executar`.
            if not args.saida_probe:
                resultado = {"esquema": ESQUEMA, "detector": "ausencia/indeterminado",
                             "veredito": VEREDITO_NAO_EXERCITADO, "status": VEREDITO_NAO_EXERCITADO,
                             "negativo": True, "dados_sinteticos": False, "hot_reload": False,
                             "motivo": "--detectar exige --saida-probe: sem leitura nao ha o que julgar",
                             "observacoes": []}
                codigo = EXIT_NAO_RODOU
            else:
                saida = carregar_saida_probe(args.saida_probe)
                contexto = {"sessao": saida.get("sessao"), "hash_fonte": saida.get("hash_fonte")}
                resultado, codigo = detectar_leitura(
                    anexar_contexto(saida.get("observacoes") or [], contexto), plano,
                    contexto=contexto, alvos=args.alvos, status_probe=saida.get("status_probe"),
                    fase=saida.get("fase"), dll_probe=args.dll_probe,
                    evidencia=args.saida_probe)
        elif args.saida_probe:
            resultado, codigo = consolidar_probe(args.saida_probe, plano, alvos=args.alvos)
        elif args.executar:
            resultado, codigo = executar_rodada(plano, perfil_dir=args.perfil, out_dir=args.out_dir,
                                                dll_probe=args.dll_probe, autorizado=args.autorizado,
                                                jogo_disponivel=args.jogo_disponivel,
                                                confirmacao=args.confirmar_coleta, steam=args.steam,
                                                timeout_s=args.timeout,
                                                encerrar_imagem=args.encerrar_imagem,
                                                frente_ativa=args.frente_ativa)
        elif args.procedencia and args.observacoes:
            obs = []
            for caminho in args.observacoes:
                with open(caminho, encoding="utf-8") as fh:
                    obs.append(json.load(fh))
            resultado, codigo = consolidar(plano, obs, args.procedencia)
        else:
            rodada, codigo = planejar_rodada(plano, args.autorizado, args.jogo_disponivel,
                                             args.confirmar_coleta,
                                             frente_ativa=args.frente_ativa)
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
