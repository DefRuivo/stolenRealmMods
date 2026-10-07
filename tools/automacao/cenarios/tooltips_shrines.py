#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tooltips_shrines.py - CIC-4: avaliador EXECUTAVEL de tooltips/shrines POR PERSONAGEM.

O QUE ESTE MODULO E (e o que NAO e)
-----------------------------------
A camada de CENARIO/ADAPTADOR do ciclo (CIC-1) para as tooltips de shrine do BetterTooltips
(AUT-6, `t_775eb4ae`). Ele traduz o formato REAL da observacao do AUT-4 para CRITERIOS do
contrato v1 do ciclo (`docs/automacao/CICLO-VALIDACAO-escopo.md`):

    avaliar(observacoes, identidade) -> lista de criterios

Cada criterio traz id, mod, estado (OK/REPROVADO/NAO_EXERCITADO/INDETERMINADO), classe
(offline/runtime), procedencia (execucao/runtime/fixture), prova_runtime, esperado, observado,
evidencia (caminhos), motivo e tarefa_origem.

Este modulo NAO abre jogo, NAO instala probe, NAO compila, NAO commita e NAO publica. Ele e
OFFLINE e so decide sobre o que recebe. **Fixture testa o avaliador; fixture NAO prova
runtime** (`prova_runtime=False`, exit 2 no CLI).

REUSO (nada de formula copiada do mod)
--------------------------------------
* `tools/checa_shrines.py` (conferencia ja existente) faz a LEITURA dos marcadores
  `[Shrine RV-23]` do log (`coleta`), expoe `esperado_buff` para o valor esperado por
  (aura, atributo, bonus) e os regexes dos itens (`RE_ITEM`/`RE_ITEM_MANA`/...). Aqui ele e
  importado como modulo - a formula do mod NAO e reescrita.
* `tools/testes/regras_shrine.py` (o ORACULO Python, segunda implementacao que tem de bater
  com o oraculo C# `oraculo_excesso_shrine`) fornece `escala()` e `dano()` para os casos sem
  atributo de personagem (Dwarven) e para as duas auras de PERIGO (Decay/Flame).
* O ESPERADO e sempre RASTREAVEL: sai da tabela gerada `tools/dados/shrines-esperado.csv` /
  `shrines-percentuais.csv` (fonte: censo `docs/cobertura/status.csv` e `resources.assets`,
  via `tools/gera_shrines_esperado.py`) e a linha cita `arquivo:linha` / `assets@offset`.

CENARIOS (o que este avaliador cobre)
-------------------------------------
1. **Dois personagens (receptor/source) na MESMA aura.** A linha "Your active shrine auras:"
   e POR PERSONAGEM: a mesma aura viva conta UMA vez para CADA personagem e usa o bonus
   DAQUELE personagem - nunca e somada/contada entre personagens. O esperado de cada um sai
   da tabela (e o eixo `Target` = o bonus de quem RECEBE).
2. **Feed vs tooltip.** O valor que o mod emite no FEED/linha azul (marcador de log
   `RV-31 acumulado`) e o valor DESENHADO na tooltip (texto renderizado lido do objeto pelo
   AUT-4) tem de bater entre si E com o esperado independente. Se so houver uma das duas
   superficies, o que faltar sai NAO_EXERCITADO (nunca OK).
   **COR-CIC4 (achados A/B do parecer CIC-4R2):** a segunda superficie e CONTRA-PROVA e tem de
   estar AUTENTICADA. Sem a observacao da TOOLTIP o criterio do FEED sai `NAO_EXERCITADO`
   (nunca OK) e a TOOLTIP so vale como contra-prova se passar a MESMA cadeia da rodada
   (`sessao` + hash confrontado com a identidade + evidencia do artefato lido) **e** vier da
   MESMA sessao do FEED; fixture, outra build ou outra sessao fecham a COMPARACAO
   (`observado.feed_vs_tooltip` diz o que se mediu), mas nao fecham o CRITERIO (o estado diz o
   que se provou). Em rodada de FIXTURE a contra-prova de fixture continua valendo - ela testa
   o AVALIADOR e nunca fecha OK com `prova_runtime=True`.
3. **Regressao BUG-34 (Armor).** O aceite humano do BUG-34 (05/10, KANBAN l.508) NAO e
   reaberto: o unico criterio e de REGRESSAO - a nota de Armor NAO pode voltar a vazar para o
   feed ("Increased Armor Applied" limpo). Um vazamento e REPROVADO de regressao, nao a
   reabertura do diagnostico.

ADAPTACAO PEQUENA E LACUNA DE RUNTIME (declaradas, sem inventar emissao)
------------------------------------------------------------------------
O coletor AUT-4 le OBJETOS VIVOS (tooltip/TMP) - ele NAO emite as linhas de marcador
`[Shrine RV-23]`, que sao o LOG do proprio mod lido por `checa_shrines`. Por isso o adaptador
aceita DUAS formas de observacao, ambas reais:

  (a) observacao AUT-4 normalizada/consolidada (`campos.texto_renderizado`,
      `campos.personagem`, `lacunas`) -> superficie TOOLTIP;
  (b) `feed`: o texto do log com os marcadores `[Shrine RV-23]` -> superficie FEED
      (mesmo material que `tools/checa_shrines.py` ja consome).

Nada aqui afirma que o coletor emite o feed: quando a rodada runtime nao entregar a
superficie necessaria, o criterio sai NAO_EXERCITADO com o proximo passo TECNICO (coletar/
logar), nunca um pedido humano de tarefa automatizavel.

CONTRATO DE PROVA RUNTIME (endurecido - correcoes #8/#9 + R-1)
-------------------------------------------------------------
* Um criterio de runtime SO fecha OK com a CADEIA COMPLETA e CONFRONTADA: identidade
  suficiente (fonte_sha+dll_sha), `sessao`, o hash de build declarado pela observacao
  (`hash_fonte`/`hash_dll` = sha256 da **DLL** do coletor CIC-5 -> chave canonica `dll_sha`;
  `fonte_sha`/`dll_sha` explicitos tambem contam) confrontado com a identidade/manifest, e
  EVIDENCIA do artefato REALMENTE LIDO. Hash divergente => INDETERMINADO; hash que a identidade
  nao conhece => NAO_EXERCITADO; o rotulo `runtime` sozinho NUNCA aprova; rotulo
  ausente/desconhecido vira `execucao` (nunca runtime por default). **`hash_fonte` casa com
  `dll_sha`, NUNCA com `fonte_sha`** (R-1 do CIC-5R; mesmo alias do CIC-3).
* `evidencia` sai do artefato lido (caminhos declarados pela observacao / `objeto` que
  existe no repo); o CSV do esperado NAO entra como evidencia da observacao e nenhum
  caminho e inventado. Sem artefato lido, o criterio e NAO_EXERCITADO (nunca OK).
* Lacuna de coleta/campo/identidade e TECNICA e NAO mascara o runtime: o criterio mantem
  `classe=runtime`/`procedencia=runtime` com `autorizacao_necessaria=False` e
  `tipo_pendencia=coleta_tecnica` -> o `decisao.py`, sem sinal humano explicito, roteia para
  falhas_automaticas (fila de agente), nunca para autorizacao humana por default. So as
  lacunas de FONTE do esperado (tabela/oraculo ausente) ficam offline/execucao.
* `procedencia` usa o enum do contrato (`execucao`/`runtime`/`fixture`); `offline` NAO existe.
  Fixture permanece fixture (`prova_runtime=False`) mesmo com todos os valores combinando.

USO
---
    python tools/automacao/cenarios/tooltips_shrines.py \
        --observacoes tools/automacao/cenarios/shrines-observacoes.exemplo.json \
        --identidade '{"fonte_sha":"...","dll_sha":"..."}' [--json] [--out saida.json]

Exit: 0 = todos OK **com prova runtime**; 1 = algum REPROVADO; 2 = sem prova runtime ou
      algum NAO_EXERCITADO/INDETERMINADO (nunca verde por fixture).
"""

import argparse
import importlib.util
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(os.path.dirname(AQUI))
REPO = os.path.dirname(TOOLS)
MOD_PADRAO = "BetterTooltips"
TAREFA_PADRAO = "t_775eb4ae"
ESQUEMA = "CIC-4/shrines/1"
CASOS_PADRAO = os.path.join(AQUI, "shrines-casos.json")

EXIT_OK, EXIT_REPROVADO, EXIT_INCOMPLETO = 0, 1, 2

# Identidade minima para aceitar uma observacao de RUNTIME (contrato v1). Faltando qualquer
# uma, o criterio NUNCA vira OK - vira NAO_EXERCITADO, com o motivo nomeando a lacuna.
IDENTIDADE_CAMPOS = ("fonte_sha", "dll_sha")

# Enum do contrato (decisao.py, CIC-2): 'offline' NAO existe - criterio sem jogo sai 'execucao'.
PROCEDENCIAS = ("execucao", "runtime", "fixture")

# Chave canonica da identidade por campo da observacao. O COLETOR CIC-5 grava `hash_fonte` =
# sha256 da **DLL** do probe (nao da fonte do repo) -> ele entra sob `dll_sha` (mesmo alias do
# CIC-3; ver CIC-5R R-1). `hash_dll` idem. `fonte_sha`/`dll_sha` explicitos tambem contam.
_ALIAS_HASH = (("hash_fonte", "dll_sha"), ("hash_dll", "dll_sha"))

# Fontes do ESPERADO (tabelas geradas) - artefato REALMENTE lido pelo modulo para a tabela.
EVIDENCIA_ESPERADO = os.path.join("tools", "dados", "shrines-esperado.csv")
EVIDENCIA_PERCENTUAIS = os.path.join("tools", "dados", "shrines-percentuais.csv")

# Rotulos que NUNCA sao valor medido (mesma regra do AUT-4).
AUSENTES = ("AUSENTE", "NAO EXERCITADO", "NÃO EXERCITADO", "NAO_EXERCITADO",
            "INDETERMINADO", "INDETERMINATE", "-")

MARCA_LINHA = "Your active shrine auras:"
# A nota de Armor do BUG-34 e identificada pelo fragmento estavel do texto (`BuildArmorNote`,
# LocalizePatch.cs 2259) - a regressao e "essa nota reapareceu no FEED".
MARCA_NOTA_ARMOR = "blocks damage"


# --------------------------------------------------------------- carregadores (reuso)

_CACHE = {}


def _carregar_modulo(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def checa():
    """`tools/checa_shrines.py` (a CONFERENCIA existente) como modulo. Reuso, nao copia."""
    if "checa" not in _CACHE:
        _CACHE["checa"] = _carregar_modulo("checa_shrines_cic4", os.path.join(TOOLS, "checa_shrines.py"))
    return _CACHE["checa"]


def regras():
    """`tools/testes/regras_shrine.py` (o ORACULO) como modulo. Reuso, nao copia."""
    if "regras" not in _CACHE:
        testes = os.path.join(TOOLS, "testes")
        if testes not in sys.path:
            sys.path.insert(0, testes)
        import regras_shrine
        _CACHE["regras"] = regras_shrine
    return _CACHE["regras"]


# --------------------------------------------------------------- identidade

def identidade_suficiente(identidade):
    """(suficiente, faltando): runtime nunca OK sem `fonte_sha` E `dll_sha` (contrato v1)."""
    identidade = identidade or {}
    faltando = [c for c in IDENTIDADE_CAMPOS if not str(identidade.get(c) or "").strip()]
    return (not faltando), faltando


# --------------------------------------------------------------- adaptacao da observacao

def _valor_de_campo(campos, nome):
    """Extrai o valor de um campo AUT-4 (`{estado, valor}`) tratando AUSENTE como ausente."""
    campo = (campos or {}).get(nome)
    valor = campo.get("valor") if isinstance(campo, dict) else campo
    if valor is None:
        return None
    if isinstance(valor, str) and valor.strip().upper() in AUSENTES:
        return None
    return valor


def _nome_personagem(valor):
    if isinstance(valor, dict):
        return valor.get("nome") or valor.get("char") or valor.get("character")
    if isinstance(valor, str):
        return valor
    return None


def _adaptar_um(obs, rotulo):
    """Traduz UMA observacao (AUT-4 real OU shrine-obs explicita) para a forma canonica.

    Devolve None se o item nao for um dict. Nao inventa campo nenhum: o que nao vier, fica
    None e o criterio correspondente sai como NAO_EXERCITADO.
    """
    if not isinstance(obs, dict):
        return None
    campos = obs.get("campos") or {}
    personagem = obs.get("personagem")
    if personagem is None:
        personagem = _valor_de_campo(campos, "personagem")
    texto = obs.get("texto_renderizado")
    if texto is None:
        texto = _valor_de_campo(campos, "texto_renderizado")
    if not texto:
        texto = obs.get("texto_bruto") or _valor_de_campo(campos, "texto_bruto")
    feed = obs.get("feed") or obs.get("log") or obs.get("linha_feed")

    procedencia = obs.get("procedencia")
    if procedencia is None:
        procedencia = _valor_de_campo(campos, "procedencia")
    if isinstance(procedencia, str) and procedencia.strip().lower() in PROCEDENCIAS:
        procedencia = procedencia.strip().lower()
    elif obs.get("evidencia_runtime") is True:
        procedencia = "runtime"
    elif obs.get("evidencia_runtime") is False or obs.get("rotulo_fixture"):
        procedencia = "fixture"
    else:
        # Rotulo ausente/desconhecido NUNCA vira runtime: a prova exige a CADEIA
        # (sessao + hash_fonte/DLL confrontados), nao um rotulo auto-declarado (#8).
        procedencia = "execucao"

    return {
        "rotulo": rotulo,
        "personagem": _nome_personagem(personagem),
        "aura": obs.get("aura"),
        "bonus": obs.get("bonus"),
        "texto_renderizado": texto if isinstance(texto, str) else None,
        "feed": feed if isinstance(feed, str) else None,
        "alvos": obs.get("alvos") or [],
        "procedencia": procedencia,
        "hash_fonte": obs.get("hash_fonte") or _valor_de_campo(campos, "hash_fonte"),
        "hash_dll": obs.get("hash_dll") or _valor_de_campo(campos, "hash_dll"),
        "fonte_sha": obs.get("fonte_sha"),
        "dll_sha": obs.get("dll_sha"),
        "sessao": obs.get("sessao") or _valor_de_campo(campos, "sessao"),
        "config_sha": obs.get("config_sha") or _valor_de_campo(campos, "config_sha"),
        "rotulo_fixture": obs.get("rotulo_fixture"),
        "evidencia": [str(x) for x in (obs.get("evidencia") or [])],
        "lacunas": [str(x) for x in (obs.get("lacunas") or [])],
        "objeto": obs.get("objeto") or _valor_de_campo(campos, "objeto"),
    }


def adaptar(observacoes):
    """Normaliza a lista inteira. Aceita: AUT-4 normalizada, AUT-4 consolidada (flatten) ou
    shrine-obs explicita. `observacoes` pode ser a propria lista ou um dict consolidado."""
    if isinstance(observacoes, dict):
        observacoes = [observacoes]
    saida = []
    for i, obs in enumerate(observacoes or []):
        if (isinstance(obs, dict) and obs.get("campos") is None
                and isinstance(obs.get("observacoes"), list)):
            for j, sub in enumerate(obs["observacoes"]):
                a = _adaptar_um(sub, "observacoes[%d].observacoes[%d]" % (i, j))
                if a:
                    saida.append(a)
            continue
        a = _adaptar_um(obs, "observacoes[%d]" % i)
        if a:
            saida.append(a)
    return saida


# --------------------------------------------------------------- leitura (feed + tooltip)

def _parse_feed(feed):
    """Le os marcadores `[Shrine RV-23]` com a CONFERENCIA existente (checa_shrines.coleta)."""
    try:
        return checa().coleta(feed)
    except Exception:
        return None


def _itens_do_texto(texto):
    """Itens de uma linha renderizada 'Your active shrine auras: <itens>.' (tooltip)."""
    if not texto:
        return []
    pos = texto.find(MARCA_LINHA)
    if pos < 0:
        return []
    corpo = texto[pos + len(MARCA_LINHA):]
    corpo = re.sub(r"</?color[^>]*>", "", corpo).strip()
    if corpo.endswith("."):
        corpo = corpo[:-1]
    return [x.strip() for x in corpo.split(";") if x.strip()]


def _item_do_atributo(texto, atributo):
    """(bruto, contrib, total) do item do `atributo` no texto renderizado, ou None."""
    ch = checa()
    for bruto in _itens_do_texto(texto):
        m = ch.RE_ITEM.match(bruto)
        if m and ch.ROTULO_ATRIBUTO.get(m.group("label")) == atributo:
            return (bruto, ch.sinal(m.group("s")) * float(m.group("v")),
                    ch.sinal(m.group("ts")) * float(m.group("tv")))
        mm = ch.RE_ITEM_MANA.match(bruto)
        if mm and atributo == "ManaCostMod":
            v = float(mm.group("v"))
            if mm.group("dir") == "reduced by":
                v = -v
            return (bruto, v, ch.sinal(mm.group("ts")) * float(mm.group("tv")))
    return None


# --------------------------------------------------------------- esperado independente

def _linha_tabela(tabela, aura, atributo, bonus):
    for r in tabela:
        if (r["aura"] == aura and r["atributo"] == atributo
                and abs(float(r["caso_bonus"]) - float(bonus)) < 1e-9):
            return r
    return None


def _esperado_atributo(tabela, aura, atributo, bonus):
    """Valor esperado da AURA (contribuicao) + fonte rastreavel. None se nao houver linha."""
    linha = _linha_tabela(tabela, aura, atributo, bonus)
    if linha is None:
        return None
    return {
        "valor": float(linha["contribuicao_esperada"]),
        "fonte": "tools/dados/shrines-esperado.csv (%s/%s bonus=%s) <- %s"
                 % (aura, atributo or "(sem atributo)", linha["caso_bonus"], linha["fonte_base"]),
        "eixo": linha.get("eixo"),
    }


def _esperado_perigo(aura, tipo, maxhealth):
    """Esperado do dano de Decay/Flame pelo ORACULO (regras_shrine), eixo `Source` (bonus 0)."""
    pct, minimo1 = regras().percentuais()
    chave = (aura, tipo.lower())
    if chave not in pct:
        return None
    # RV-30: as duas de PERIGO leem `Source[...]` e no ground effect o Source e o shrine (bonus 0).
    valor = regras().dano(maxhealth, pct[chave], regras().BONUS_DA_FONTE, minimo1[aura])
    return {
        "valor": float(valor),
        "fonte": "tools/dados/shrines-percentuais.csv (%s/%s) + regras_shrine.dano (eixo Source=0)"
                 % (aura, tipo),
        "eixo": "Source",
    }


def _itens_em(observados):
    """Todos os textos renderizados/feed das observacoes adaptadas."""
    return [o for o in observados if o.get("texto_renderizado") or o.get("feed")]


# --------------------------------------------------------------- criterios

def _crit(caso, pid, estado, esperado, observado, motivo, procedencia, prova_runtime,
          evidencia, classe="runtime", extra=None):
    crit = {
        "id": "%s/%s" % (caso["id"], pid) if pid else caso["id"],
        "mod": caso.get("mod", MOD_PADRAO),
        "estado": estado,
        "classe": classe,
        "procedencia": procedencia,
        "prova_runtime": bool(prova_runtime),
        "esperado": esperado,
        "observado": observado,
        "evidencia": [str(x) for x in (evidencia or [])],
        "motivo": motivo,
        "tarefa_origem": caso.get("tarefa_origem", TAREFA_PADRAO),
    }
    if estado in ("NAO_EXERCITADO", "INDETERMINADO"):
        # Lacuna de coleta/campo/identidade e TECNICA: fila de agente, NAO autorizacao humana
        # por default (CICLO-VALIDACAO-escopo.md, Correcoes funcionais). `decisao.py` roteia
        # classe offline+procedencia execucao para falhas_automaticas.
        crit["autorizacao_necessaria"] = False
        crit["tipo_pendencia"] = "coleta_tecnica"
    if extra:
        crit.update(extra)
    return crit


def _classe_de(procedencia):
    """classe coerente com a procedencia: runtime exige classe runtime (decisao.py CIC-2)."""
    return "runtime" if procedencia == "runtime" else "offline"


def _chain_extra(obs, ident_kwargs):
    """Campos da CADEIA de runtime para o criterio (contrato positivo): `sessao` da observacao +
    `fonte_sha`/`dll_sha`/`config_sha` DA IDENTIDADE da rodada, para o `decisao.py` reconferir
    contra a identidade/manifest em vez de acreditar no rotulo. O `hash_fonte` da observacao NAO
    vira `fonte_sha`: ele e a cadeia da DLL (alias `dll_sha`, R-1 do CIC-5R)."""
    if obs.get("procedencia") != "runtime":
        return {}
    extra = {}
    if obs.get("sessao"):
        extra["sessao"] = obs["sessao"]
    if ident_kwargs.get("fonte_sha"):
        extra["fonte_sha"] = ident_kwargs["fonte_sha"]
    if ident_kwargs.get("dll_sha"):
        extra["dll_sha"] = ident_kwargs["dll_sha"]
    if ident_kwargs.get("config_sha"):
        extra["config_sha"] = ident_kwargs["config_sha"]
    return extra


def _hashes_identidade(ident_kwargs):
    """Hashes que a IDENTIDADE da rodada conhece (chaves canonicas)."""
    conhecidos = {}
    for chave in ("fonte_sha", "dll_sha", "config_sha"):
        valor = ident_kwargs.get(chave)
        if isinstance(valor, str) and valor.strip():
            conhecidos[chave] = valor.strip()
    return conhecidos


def _hashes_obs(obs):
    """Hashes que a OBSERVACAO declara, sob as chaves canonicas da identidade.

    O coletor CIC-5 grava `hash_fonte` = sha256 da **DLL** do probe -> ele entra sob `dll_sha`
    (mesmo alias do CIC-3; R-1 do CIC-5R). `hash_dll` idem; `fonte_sha`/`dll_sha`/`config_sha`
    explicitos tambem contam."""
    d = {}
    for alias, canonico in _ALIAS_HASH:
        valor = obs.get(alias)
        if isinstance(valor, str) and valor.strip():
            d[canonico] = valor.strip()
    for chave in ("fonte_sha", "dll_sha", "config_sha"):
        valor = obs.get(chave)
        if isinstance(valor, str) and valor.strip():
            d[chave] = valor.strip()
    return d


def _cadeia_runtime(obs, ident_kwargs):
    """Confere a CADEIA da observacao contra a identidade/manifest da coleta.

    Devolve (estado, motivo) quando NAO fecha, ou (None, None). Regras duras: rotulo runtime
    sozinho nao aprova; exige identidade suficiente (fonte_sha+dll_sha), `sessao`, o hash de build
    declarado pela observacao (`hash_fonte`/`hash_dll` = cadeia da DLL; explicitos `*_sha`)
    confrontado com a identidade — hash divergente => INDETERMINADO, nao-confirmado =>
    NAO_EXERCITADO — e a EVIDENCIA do artefato lido. `hash_fonte` casa com `dll_sha`, NUNCA com
    `fonte_sha` (R-1 do CIC-5R)."""
    if not ident_kwargs["suficiente"]:
        return ("NAO_EXERCITADO",
                "identidade insuficiente (falta %s): observacao de runtime NAO aprova sem "
                "fonte_sha/dll_sha (automatizavel: anexar a identidade da rodada)"
                % ", ".join(ident_kwargs["faltando"]))
    if not str(obs.get("sessao") or "").strip():
        return ("NAO_EXERCITADO", "runtime sem sessao: cadeia de coleta incompleta")
    declarados = _hashes_obs(obs)
    if not declarados:
        return ("NAO_EXERCITADO",
                "rotulo runtime SEM hash da build: o rotulo sozinho nao amarra aos bytes - a "
                "observacao so aprova com o hash (hash_fonte/DLL) confrontado com a identidade")
    conhecidos = _hashes_identidade(ident_kwargs)
    divergentes = sorted(k for k, v in declarados.items() if k in conhecidos and conhecidos[k] != v)
    if divergentes:
        return ("INDETERMINADO",
                "observacao de OUTRA build (hash %s difere da identidade da rodada)"
                % ", ".join(divergentes))
    nao_confirmados = sorted(k for k in declarados if k not in conhecidos)
    if nao_confirmados:
        return ("NAO_EXERCITADO",
                "hash declarado que a identidade/manifest nao conhece (%s): cadeia incompleta"
                % ", ".join(nao_confirmados))
    if not _evidencia_obs(obs):
        return ("NAO_EXERCITADO",
                "runtime sem evidencia de artefato lido: nao aprovar por rotulo - anexar o "
                "arquivo (log/objeto) realmente lido")
    return (None, None)


def _decisao_runtime(obs, ident_kwargs):
    """(estado, prova_runtime, motivo) para um valor que BATEU. Nunca OK sem a cadeia completa."""
    if obs["procedencia"] == "fixture":
        return ("OK", False,
                "fixture: avalia o avaliador; NAO prova runtime (a decisao separa fixture "
                "de prova - CICLO-VALIDACAO-escopo.md, contrato v1)")
    if obs["procedencia"] != "runtime":
        return ("NAO_EXERCITADO", False,
                "observacao sem rotulo de runtime confiavel (procedencia=%r): rotulo ausente/"
                "desconhecido NUNCA vira runtime (prova exige cadeia, nao rotulo)"
                % obs["procedencia"])
    estado, motivo = _cadeia_runtime(obs, ident_kwargs)
    if estado:
        return (estado, False, motivo)
    return ("OK", True, "valor bateu com o esperado independente e a cadeia de runtime fecha "
                        "(sessao/hash/manifest/evidencia confrontados com a identidade)")


def _achar_tooltip(adaptadas, nome):
    """A observacao da superficie TOOLTIP (texto renderizado) DAQUELE personagem, ou None."""
    for o in adaptadas:
        if o.get("personagem") == nome and o.get("texto_renderizado"):
            return o
    return None


def _contra_prova_autenticada(contra, feed, ident_kwargs, nome):
    """A superficie de CONTRA-PROVA (TOOLTIP) passa a MESMA cadeia da superficie observada?

    Achado B do CIC-4R2: uma tooltip `fixture`, de OUTRA build ou de OUTRA sessao fechava a
    comparacao (`feed_vs_tooltip=IGUAL`) sem autenticar nada. Devolve (estado, motivo) quando a
    contra-prova NAO autentica, ou (None, None) quando autentica - ou quando a rodada nao se
    declara runtime: em rodada de FIXTURE a contra-prova de fixture testa o AVALIADOR, nao o
    campo (e nunca fecha OK com `prova_runtime=True`).
    """
    if not contra or feed.get("procedencia") != "runtime":
        return (None, None)
    if contra.get("procedencia") != "runtime":
        return ("NAO_EXERCITADO",
                "contra-prova (TOOLTIP) de '%s' NAO autenticada: procedencia=%r - o criterio "
                "'feed vs tooltip' so fecha com a segunda superficie da MESMA rodada de runtime "
                "(fixture/rotulo nao prova campo; automatizavel: coletar a tooltip na rodada)"
                % (nome, contra.get("procedencia")))
    estado, motivo = _cadeia_runtime(contra, ident_kwargs)
    if estado:
        return (estado, "contra-prova (TOOLTIP) de '%s' sem cadeia valida: %s" % (nome, motivo))
    sess_feed = str(feed.get("sessao") or "").strip()
    sess_contra = str(contra.get("sessao") or "").strip()
    if sess_feed and sess_contra and sess_feed != sess_contra:
        return ("INDETERMINADO",
                "contra-prova (TOOLTIP) de '%s' e da sessao %r e o FEED e da sessao %r: "
                "superficies de rodadas diferentes nao provam o mesmo ciclo"
                % (nome, sess_contra, sess_feed))
    return (None, None)


# --------------------------------------------------------------- casos

def _casos(caminho):
    if not os.path.isfile(caminho):
        return {"casos": [], "erro": "casos ausentes: %s" % caminho}
    with open(caminho, encoding="utf-8") as fh:
        return json.load(fh)


def _feed_de(adaptadas):
    """Lista de (adaptada, parse) para toda observacao que traga o FEED do log."""
    saida = []
    for o in adaptadas:
        if not o.get("feed"):
            continue
        p = _parse_feed(o["feed"])
        if p is not None:
            saida.append((o, p))
    return saida


def _achar_acumulado(parses, aura, nome, bonus):
    for o, p in parses:
        for a in p.get("acumulado", []):
            if (a["char"] == nome and abs(a["bonus"] - float(bonus)) < 1e-9
                    and aura in a["auras"]):
                return o, a
    return None, None


def _achar_flame(parses, aura, nome_alvo, tipo, bonus):
    for o, p in parses:
        for f in p.get("flame", []):
            if (f["nome"] == nome_alvo and abs(f["bonus"] - float(bonus)) < 1e-9
                    and f["tipo"].lower() == (tipo or "").lower()):
                return o, f
    return None, None


def _evidencia_obs(obs):
    """Evidencia a partir do ARTEFATO REALMENTE LIDO (#9): os caminhos declarados pela observacao
    e, se `objeto` resolver para um arquivo existente, ele tambem. NUNCA inventa caminho nem usa
    a tabela do esperado no lugar do artefato da observacao."""
    if not obs:
        return []
    ev = [str(x) for x in (obs.get("evidencia") or [])]
    obj = obs.get("objeto")
    if isinstance(obj, str):
        obj = obj.strip()
        if obj and os.path.isfile(os.path.join(REPO, obj)) and obj not in ev:
            ev.append(obj)
    return ev


def _evidencia_de(caso, obs):
    """Evidencia do criterio: com observacao -> o artefato dela; sem observacao -> a propria tabela
    gerada (que o modulo le para o esperado), nunca um caminho fingido de runtime."""
    if obs is None:
        return [EVIDENCIA_ESPERADO]
    return _evidencia_obs(obs)


# --------------------------------------------------------------- avaliacao por tipo

def _caso_atributo(caso, adaptadas, parses, tabela, ident_kwargs):
    """Aura de ATRIBUTO de personagem: um criterio por (personagem, atributo, bonus)."""
    criterios = []
    pers = caso.get("personagens") or []
    for p in pers:
        nome, bonus = p["nome"], p["bonus"]
        pid = "%s/bonus=%s" % (p.get("id", nome), bonus)
        esperado = _esperado_atributo(tabela, caso["aura"], caso["atributo"], bonus)
        obs, acum = _achar_acumulado(parses, caso["aura"], nome, bonus)
        if esperado is None:
            criterios.append(_crit(caso, pid, "NAO_EXERCITADO", None, None,
                                   "sem linha na tabela gerada para esta aura/atributo/bonus "
                                   "(fonte ausente: NAO e OK; proximo passo TECNICO = gerar "
                                   "tabela)", "execucao", False, [EVIDENCIA_ESPERADO],
                                   classe="offline",
                                   extra={"personagem": nome, "tipo_pendencia": "fonte_esperado"}))
            continue
        if acum is None:
            criterios.append(_crit(caso, pid, "NAO_EXERCITADO", esperado, None,
                                   "sem observacao do personagem '%s' bonus=%s no FEED/tooltip "
                                   "(lacuna TECNICA de coleta: NAO e OK; proximo passo TECNICO = "
                                   "coletar)" % (nome, bonus), "runtime", False,
                                   _evidencia_de(caso, obs), classe="runtime",
                                   extra={"personagem": nome, "tipo_pendencia": "coleta_tecnica"}))
            continue
        item = None
        for it in acum["itens"]:
            if it["atributo"] == caso["atributo"]:
                item = it
                break
        if item is None:
            criterios.append(_crit(caso, pid, "NAO_EXERCITADO", esperado, None,
                                   "FEED sem o item do atributo %s para '%s' (campo ausente: "
                                   "lacuna TECNICA de coleta, NAO e OK)"
                                   % (caso["atributo"], nome), obs["procedencia"], False,
                                   _evidencia_de(caso, obs),
                                   classe=_classe_de(obs["procedencia"]),
                                   extra={"personagem": nome, "tipo_pendencia": "coleta_tecnica"}))
            continue
        observado = {"contrib": item["contrib"], "total": item["total"],
                     "grandeza": "contribuicao das auras (RV-44)", "superficie_feed": obs["rotulo"]}
        ev = _evidencia_de(caso, obs)
        # (1) o valor do FEED bate com o esperado independente?
        if abs(item["contrib"] - esperado["valor"]) > 1e-9:
            criterios.append(_crit(caso, pid, "REPROVADO", esperado, observado,
                                   "contribuicao do FEED difere do esperado independente "
                                   "(dif=%+g)" % (item["contrib"] - esperado["valor"]),
                                   obs["procedencia"], False, ev, classe=_classe_de(obs["procedencia"]),
                                   extra={"personagem": nome}))
            continue
        # (2) a segunda superficie e CONTRA-PROVA (COR-CIC4, achados A/B do CIC-4R2): ela tem de
        # EXISTIR, estar AUTENTICADA (mesma cadeia/sessao da rodada) e BATER com o FEED.
        tooltip = _achar_tooltip(adaptadas, nome)
        if tooltip is not None:
            observado["superficie_tooltip"] = tooltip["rotulo"]
            par = _item_do_atributo(tooltip["texto_renderizado"], caso["atributo"])
            ev = ev + _evidencia_obs(tooltip)
            if par is None:
                observado["feed_vs_tooltip"] = "TOOLTIP_SEM_ITEM"
                criterios.append(_crit(caso, pid, "NAO_EXERCITADO", esperado, observado,
                                       "tooltip renderizada sem o item do atributo %s (campo "
                                       "ausente na leitura do objeto: lacuna TECNICA)"
                                       % caso["atributo"], tooltip["procedencia"], False, ev,
                                       classe=_classe_de(tooltip["procedencia"]),
                                       extra={"personagem": nome,
                                              "tipo_pendencia": "coleta_tecnica"}))
                continue
            if abs(par[1] - item["contrib"]) > 1e-9 or abs(par[2] - item["total"]) > 1e-9:
                observado["feed_vs_tooltip"] = "DIVERGE"
                criterios.append(_crit(caso, pid, "REPROVADO", esperado, observado,
                                       "FEED e TOOLTIP divergem no personagem '%s' "
                                       "(feed contrib=%g total=%g | tooltip contrib=%g total=%g)"
                                       % (nome, item["contrib"], item["total"], par[1], par[2]),
                                       tooltip["procedencia"], False, ev,
                                       classe=_classe_de(tooltip["procedencia"]),
                                       extra={"personagem": nome, "feed_vs_tooltip": "DIVERGE"}))
                continue
            observado["feed_vs_tooltip"] = "IGUAL"
        else:
            observado["superficie_tooltip"] = None
            observado["feed_vs_tooltip"] = "SEM_TOOLTIP"
        # (3) o estado: a cadeia do FEED primeiro (defeito de cadeia e mais grave que a ausencia
        # da contra-prova e nao pode ser mascarado por ela), depois a EXIGENCIA da segunda
        # superficie autenticada (achados A/B: sem ela NAO ha OK).
        estado, prova, motivo = _decisao_runtime(obs, ident_kwargs)
        if estado == "OK" and tooltip is None:
            estado, prova = "NAO_EXERCITADO", False
            motivo = ("sem a superficie TOOLTIP do personagem '%s' bonus=%s: o criterio e "
                      "'feed vs tooltip' e faltou a segunda superficie - NAO_EXERCITADO, nunca "
                      "OK (lacuna TECNICA de coleta: ler a tooltip renderizada na rodada)"
                      % (nome, bonus))
        if estado == "OK":
            estado_contra, motivo_contra = _contra_prova_autenticada(tooltip, obs, ident_kwargs,
                                                                     nome)
            if estado_contra:
                estado, prova, motivo = estado_contra, False, motivo_contra
        extra = {"personagem": nome}
        extra.update(_chain_extra(obs, ident_kwargs))
        criterios.append(_crit(caso, pid, estado, esperado, observado, motivo,
                               obs["procedencia"], prova, ev,
                               classe=_classe_de(obs["procedencia"]), extra=extra))
    return criterios


def _caso_sem_atributo(caso, adaptadas, parses, tabela, ident_kwargs):
    """Aura de GATILHO sem atributo de personagem (Dwarven): item proprio 'Stun chance +N%'."""
    criterios = []
    for p in caso.get("personagens") or []:
        nome, bonus = p["nome"], p["bonus"]
        pid = "%s/bonus=%s" % (p.get("id", nome), bonus)
        esperado = _esperado_atributo(tabela, caso["aura"], "", bonus)
        obs, acum = _achar_acumulado(parses, caso["aura"], nome, bonus)
        if esperado is None:
            criterios.append(_crit(caso, pid, "NAO_EXERCITADO", None, None,
                                   "sem linha na tabela gerada para a aura sem atributo "
                                   "(fonte ausente: NAO e OK)", "execucao", False,
                                   [EVIDENCIA_ESPERADO], classe="offline",
                                   extra={"personagem": nome, "tipo_pendencia": "fonte_esperado"}))
            continue
        if acum is None:
            criterios.append(_crit(caso, pid, "NAO_EXERCITADO", esperado, None,
                                   "sem observacao de '%s' bonus=%s (lacuna TECNICA de coleta: "
                                   "NAO e OK)" % (nome, bonus), "runtime", False,
                                   _evidencia_de(caso, obs), classe="runtime",
                                   extra={"personagem": nome, "tipo_pendencia": "coleta_tecnica"}))
            continue
        v = acum["sem_atributo"].get("Stun chance")
        if v is None:
            criterios.append(_crit(caso, pid, "NAO_EXERCITADO", esperado, None,
                                   "FEED sem o item proprio 'Stun chance' (campo ausente: "
                                   "lacuna TECNICA, NAO e OK)", obs["procedencia"], False,
                                   _evidencia_de(caso, obs),
                                   classe=_classe_de(obs["procedencia"]),
                                   extra={"personagem": nome, "tipo_pendencia": "coleta_tecnica"}))
            continue
        observado = {"valor": v, "grandeza": "chance de stun do asset", "superficie_feed": obs["rotulo"]}
        ev = _evidencia_de(caso, obs)
        if abs(v - esperado["valor"]) > 1e-9:
            criterios.append(_crit(caso, pid, "REPROVADO", esperado, observado,
                                   "chance de stun do FEED difere do esperado (dif=%+g)"
                                   % (v - esperado["valor"]), obs["procedencia"], False, ev,
                                   classe=_classe_de(obs["procedencia"]),
                                   extra={"personagem": nome}))
            continue
        estado, prova, motivo = _decisao_runtime(obs, ident_kwargs)
        extra = {"personagem": nome}
        extra.update(_chain_extra(obs, ident_kwargs))
        criterios.append(_crit(caso, pid, estado, esperado, observado, motivo,
                               obs["procedencia"], prova, ev,
                               classe=_classe_de(obs["procedencia"]), extra=extra))
    return criterios


def _caso_perigo(caso, adaptadas, parses, tabela, ident_kwargs):
    """Aura de PERIGO (Flame/Decay): dano por alvo; esperado = oraculo (eixo Source=0)."""
    criterios = []
    for alvo in caso.get("alvos") or []:
        nome_alvo, tipo, bonus = alvo["nome"], alvo["tipo"], alvo["bonus"]
        pid = "%s/bonus=%s" % (nome_alvo, bonus)
        obs, f = _achar_flame(parses, caso["aura"], nome_alvo, tipo, bonus)
        if f is None:
            criterios.append(_crit(caso, pid, "NAO_EXERCITADO", None, None,
                                   "sem observacao do alvo '%s' tipo=%s bonus=%s no FEED "
                                   "(lacuna TECNICA de coleta: NAO e OK)"
                                   % (nome_alvo, tipo, bonus), "runtime", False,
                                   [EVIDENCIA_PERCENTUAIS], classe="runtime",
                                   extra={"alvo": nome_alvo, "tipo": tipo,
                                          "tipo_pendencia": "coleta_tecnica"}))
            continue
        esperado = _esperado_perigo(caso["aura"], tipo, f["mh"])
        if esperado is None:
            criterios.append(_crit(caso, pid, "NAO_EXERCITADO", None, {"dano": f["dano"]},
                                   "tipo '%s' do alvo nao esta na tabela de percentuais "
                                   "(fonte ausente: NAO e OK)" % tipo, "execucao", False,
                                   [EVIDENCIA_PERCENTUAIS], classe="offline",
                                   extra={"alvo": nome_alvo, "tipo": tipo,
                                          "tipo_pendencia": "fonte_esperado"}))
            continue
        ev = _evidencia_obs(obs)
        observado = {"dano": f["dano"], "maxhealth": f["mh"], "tipo": f["tipo"],
                     "grandeza": "dano por alvo (RV-34)", "superficie_feed": obs["rotulo"]}
        if abs(f["dano"] - esperado["valor"]) > 1e-9:
            criterios.append(_crit(caso, pid, "REPROVADO", esperado, observado,
                                   "dano do FEED difere do oraculo (dif=%+g)"
                                   % (f["dano"] - esperado["valor"]), obs["procedencia"], False,
                                   ev, classe=_classe_de(obs["procedencia"]),
                                   extra={"alvo": nome_alvo, "tipo": tipo}))
            continue
        estado, prova, motivo = _decisao_runtime(obs, ident_kwargs)
        extra = {"alvo": nome_alvo, "tipo": tipo}
        extra.update(_chain_extra(obs, ident_kwargs))
        criterios.append(_crit(caso, pid, estado, esperado, observado, motivo,
                               obs["procedencia"], prova, ev,
                               classe=_classe_de(obs["procedencia"]), extra=extra))
    return criterios


def _caso_regressao_feed(caso, adaptadas, ident_kwargs):
    """BUG-34 (Armor) - SO regressao. O aceite humano (05/10) nao e reaberto."""
    esperado = {
        "valor": "feed SEM a nota de Armor (%r ausente em %r)" % (MARCA_NOTA_ARMOR, caso.get("texto_limpo", "")),
        "fonte": "KANBAN.md BUG-34 (aceite humano 05/10) + BetterTooltips/Patches/LocalizePatch.cs"
                 " BuildArmorNote/SendMessageWindowMessage",
    }
    marcador = caso.get("marcador", caso.get("texto_limpo", ""))
    relevantes = [o for o in adaptadas
                  if (o.get("texto_renderizado") or o.get("feed"))
                  and (not marcador or marcador in (o.get("texto_renderizado") or o.get("feed") or ""))]
    if not relevantes:
        return [_crit(caso, None, "NAO_EXERCITADO", esperado, None,
                      "sem observacao do FEED (lacuna TECNICA de coleta: NAO e OK)", "runtime",
                      False, [], classe="runtime",
                      extra={"regressao_de": "BUG-34", "reabre_bug": False,
                             "tipo_pendencia": "coleta_tecnica"})]
    obs = relevantes[0]
    texto = obs.get("texto_renderizado") or obs.get("feed") or ""
    observado = {"texto": texto[:400], "superficie": obs["rotulo"]}
    if MARCA_NOTA_ARMOR in texto:
        return [_crit(caso, None, "REPROVADO", esperado, observado,
                      "REGRESSAO do BUG-34: a nota de Armor voltou ao FEED - nao reabre o "
                      "diagnostico (aceite humano de 05/10 segue valido), so aponta a regressao",
                      obs["procedencia"], False, _evidencia_obs(obs),
                      classe=_classe_de(obs["procedencia"]),
                      extra={"regressao_de": "BUG-34", "reabre_bug": False})]
    estado, prova, motivo = _decisao_runtime(obs, ident_kwargs)
    extra = {"regressao_de": "BUG-34", "reabre_bug": False}
    extra.update(_chain_extra(obs, ident_kwargs))
    return [_crit(caso, None, estado, esperado, observado,
                  "regressao OK: a nota de Armor NAO voltou ao FEED (%s)" % motivo,
                  obs["procedencia"], prova, _evidencia_obs(obs),
                  classe=_classe_de(obs["procedencia"]), extra=extra)]


TIPOS = {
    "atributo": _caso_atributo,
    "sem_atributo": _caso_sem_atributo,
    "perigo": _caso_perigo,
    "regressao_feed": _caso_regressao_feed,
}


# --------------------------------------------------------------- API do contrato v1

def avaliar(observacoes, identidade=None, casos=None):
    """Contrato v1 do ciclo: lista de criterios a partir das observacoes + identidade.

    `observacoes`: lista no formato REAL do AUT-4 (normalizada/consolidada) OU shrine-obs
                   explicita; `identidade`: dict com `fonte_sha`/`dll_sha` (podem faltar -
                   nunca OK sem identidade suficiente).
    """
    ident = identidade or {}
    suficiente, faltando = identidade_suficiente(ident)
    ident_kwargs = {"suficiente": suficiente, "faltando": faltando,
                    "fonte_sha": ident.get("fonte_sha"), "dll_sha": ident.get("dll_sha"),
                    "config_sha": ident.get("config_sha")}
    if casos is None:
        casos = _casos(CASOS_PADRAO)
    tabela = checa().carrega_esperado(os.path.join(TOOLS, "dados", "shrines-esperado.csv"))
    if tabela is None:
        raise RuntimeError("tabela gerada ausente: tools/dados/shrines-esperado.csv "
                           "(rode tools/gera_shrines_esperado.py)")

    adaptadas = adaptar(observacoes)
    parses = _feed_de(adaptadas)

    criterios = []
    for caso in casos.get("casos", []):
        fn = TIPOS.get(caso.get("tipo"))
        if fn is None:
            criterios.append(_crit(caso, None, "NAO_EXERCITADO", None, None,
                                   "tipo de caso desconhecido: %r" % caso.get("tipo"),
                                   "execucao", False, [], classe="offline"))
            continue
        if caso.get("tipo") == "regressao_feed":
            criterios.extend(fn(caso, adaptadas, ident_kwargs))
        elif caso.get("tipo") == "perigo":
            criterios.extend(fn(caso, adaptadas, parses, tabela, ident_kwargs))
        else:
            criterios.extend(fn(caso, adaptadas, parses, tabela, ident_kwargs))
    return criterios


def resumo(criterios):
    cont = {"OK": 0, "REPROVADO": 0, "NAO_EXERCITADO": 0, "INDETERMINADO": 0}
    for c in criterios:
        cont[c["estado"]] = cont.get(c["estado"], 0) + 1
    provados = sum(1 for c in criterios if c.get("prova_runtime"))
    return {"total": len(criterios), **cont, "com_prova_runtime": provados}


def exit_de(criterios):
    cont = resumo(criterios)
    if cont.get("REPROVADO"):
        return EXIT_REPROVADO
    if cont.get("NAO_EXERCITADO") or cont.get("INDETERMINADO"):
        return EXIT_INCOMPLETO
    if not cont.get("com_prova_runtime"):
        # tudo OK, mas so fixture: NUNCA verde (fixture nao prova runtime).
        return EXIT_INCOMPLETO
    return EXIT_OK


# --------------------------------------------------------------- CLI

def _carrega_json_arg(valor):
    if valor is None:
        return None
    if os.path.isfile(valor):
        with open(valor, encoding="utf-8") as fh:
            return json.load(fh)
    try:
        return json.loads(valor)
    except ValueError as erro:
        raise SystemExit("FALHA(2): --identidade nao e arquivo nem JSON: %s" % erro)


def main(argv=None):
    ap = argparse.ArgumentParser(description="CIC-4 avaliador de tooltips/shrines (offline).")
    ap.add_argument("--observacoes", required=True,
                    help="arquivo JSON com a lista de observacoes (ou 1 consolidada)")
    ap.add_argument("--identidade", default=None,
                    help="JSON/dict com fonte_sha e dll_sha (arquivo ou string)")
    ap.add_argument("--fonte-sha", default=None)
    ap.add_argument("--dll-sha", default=None)
    ap.add_argument("--casos", default=CASOS_PADRAO)
    ap.add_argument("--out", default=None)
    ap.add_argument("--json", action="store_true", help="imprime so o JSON de criterios")
    args = ap.parse_args(argv)

    if not os.path.isfile(args.observacoes):
        print("FALHA(2): observacoes ausentes: %s" % args.observacoes)
        return EXIT_INCOMPLETO
    with open(args.observacoes, encoding="utf-8") as fh:
        observacoes = json.load(fh)

    ident = _carrega_json_arg(args.identidade) or {}
    if args.fonte_sha:
        ident["fonte_sha"] = args.fonte_sha
    if args.dll_sha:
        ident["dll_sha"] = args.dll_sha

    casos = _casos(args.casos)
    criterios = avaliar(observacoes, ident, casos)
    cont = resumo(criterios)
    codigo = exit_de(criterios)

    saida = {"esquema": ESQUEMA, "tarefa_origem": TAREFA_PADRAO,
             "identidade_suficiente": identidade_suficiente(ident)[0],
             "resumo": cont, "exit_code": codigo, "criterios": criterios}
    texto = json.dumps(saida, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(texto + "\n")
    if not args.json:
        print("=" * 78)
        print("CIC-4 tooltips/shrines - avaliador por personagem")
        print("  observacoes: %s" % args.observacoes)
        print("  identidade suficiente: %s" % identidade_suficiente(ident)[0])
        print("=" * 78)
        for c in criterios:
            marca = {"OK": "[OK]     ", "REPROVADO": "[REPROV] ",
                     "NAO_EXERCITADO": "[NAO-EX] ", "INDETERMINADO": "[INDET]  "}.get(c["estado"], "[?]      ")
            print("  %s %-44s %s" % (marca, c["id"], c["motivo"]))
        print("\n== RESULTADO ==")
        print("  " + ", ".join("%s=%d" % (k, cont[k]) for k in
                               ("OK", "REPROVADO", "NAO_EXERCITADO", "INDETERMINADO")))
        print("  com prova runtime: %d  · exit=%d" % (cont["com_prova_runtime"], codigo))
    if args.json:
        print(texto)
    return codigo


if __name__ == "__main__":
    sys.exit(main())
