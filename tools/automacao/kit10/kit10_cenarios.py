#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kit10_cenarios.py - KIT-10: completar os cenarios de tooltips, shrines, estilo e atributos.

OBJETIVO (cartao `t_bbad760d`)
------------------------------
Depois do RSTV (KIT-09), a cobertura por CENARIO da camada de verificacao ainda tinha buracos.
Este modulo os completa REUSANDO a infraestrutura ja entregue - nunca a reimplementando:

  * `tools/automacao/cenarios/tooltips_shrines.py` (CIC-4, `t_6dc6484b`) - avaliador de
    tooltips/shrines por personagem (feed x tooltip, eixo Target/Source, regressao BUG-34);
  * `tools/automacao/estilo/estilo_atributos.py` (AUT-7, `t_674c5976`) - estilo (BetterFont,
    BetterCombatText), atributos (BetterStats) e dump (RoguelikeDebugger), offline + runtime;
  * `tools/checa_shrines.py` - leitura dos marcadores `[Shrine RV-23]` do log;
  * `tools/testes/regras_shrine.py` - o ORACULO do shrine (escala/dano/eixo/efeito de gatilho);
  * `tools/testes/regras_debugger.py` + `tools/testes/regras_bct.py` - contrato do dump e
    superficies do BetterCombatText.

O QUE ESTE MODULO ACRESCENTA (os cenarios que faltavam)
-------------------------------------------------------
`avaliar(observacoes, identidade)` devolve, no contrato do ciclo
(`docs/automacao/CICLO-VALIDACAO-escopo.md`, v1):

  1. TODOS os criterios do CIC-4 (reuso literal, `tooltips_shrines.avaliar`);
  2. TODOS os criterios do AUT-7 (reuso literal, `estilo_atributos.avaliar`) - e por eles que
     BetterStats `SavedMap`/final, BetterFont/BetterCombatText e o contrato do Debugger entram;
  3. os aspectos que faltavam, com o esperado independente e controle negativo por aspecto:

     A. `KIT-10/shrines/contexto-dano-fonte-receptor` - relaciona tooltip/contexto/dano e o
        eixo FONTE x RECEPTOR: num ground effect o dano das auras de PERIGO leem
        `Source["ShrineEffectBonus"]` = personagem VAZIO do shrine (bonus 0), enquanto as auras
        de BUFF leem `Target[...]` = o bonus do RECEPTOR. Esperado do ORACULO (`regras_shrine`).
        Defeito pego: o bonus do jogador REINJETADO em `Source` (o defeito do RV-34) -> REPROVADO.
        KIT-10F (F8): NaN/inf/bool/string invalida em QUALQUER medicao numerica NUNCA fecham OK.
     B. `KIT-10/shrines/worship-dobro-preservado` - o comportamento CONFIRMADO: para as auras de
        GATILHO (Dwarven/Decay/Flame) a INSTANCIA repetida CONTA (o motor avalia o gatilho uma vez
        por status vivo - DWA-2), e para as auras de ATRIBUTO ela conta UMA vez (RV-46). O cenario
        PRESERVA o "dobro" do gatilho; o controle negativo e o dobro REMOVIDO -> REPROVADO.
        (Regra do cartao: "nao remover dobro para tornar teste verde".)
        KIT-10F (F9): so aura CANONICA com `instancias` INTEIRA POSITIVA MEDIDA vale; sem gatilho
        repetido (>=2) o "dobro" NAO foi exercitado -> lacuna declarada (nunca OK por vacuidade).
     C. `KIT-10/estilo/por-evento-nao-boot` - BetterFont/BetterCombatText: a superficie de estilo
        tem de ser lida no EVENTO (level-up/combate/status), nunca do PREFAB de boot; um alvo de
        superficie canonica lido em `estagio=boot` -> REPROVADO.
     D. `KIT-10/debugger/sem-truncar` - o contrato do dump (RoguelikeDebugger): `desc=` por
        ULTIMO, nenhum valor com `|` e a `DESC` ancorada NO FIM (descricao truncada -> REPROVADO).
        Reusa `regras_debugger.contrato_da_linha`/`confere_linha` - nada de regex digitada.
        KIT-10F (F10): confere TODA linha DECLARADA do dump (nao filtra o defeito antes de
        avaliar) e reprova `|` DENTRO do `desc`.
     E. `KIT-10/atributos/base-vs-final` - KIT-10F (F12): adaptacao OFFLINE MINIMA que confronta o
        texto `base (final)` do BetterStats com os valores MEDIDOS independentes (`saved_map` base
        pura x `atributos_final` do motor) por atributo+personagem - o esperado NUNCA sai do
        display. Sem esses campos a coleta real fica NAO_EXERCITADO (lacuna TECNICA declarada).

RUNTIME AUSENTE NAO RECEBE OK
-----------------------------
Todo criterio passa pelo fechamento do AUT-7 (`estilo_atributos._fecha`): sem identidade
suficiente (`fonte_sha` + `dll_sha`), sem cadeia (`sessao`/hash confrontado) ou com procedencia
`fixture`, o melhor estado possivel e `NAO_EXERCITADO` (`prova_runtime=False`). Um DEFEITO
plantado, porem, continua `REPROVADO` mesmo em fixture - e assim que o controle negativo prova
que a regra pega o defeito.

O QUE ESTE MODULO NAO FAZ
-------------------------
Nao abre o jogo, nao instala probe, nao compila, nao carrega save, nao publica e NAO altera mod
nem gameplay. E OFFLINE e so decide sobre o que recebe.

CLI
---
    python tools/automacao/kit10/kit10_cenarios.py --observacoes obs.json \
        [--identidade '{"fonte_sha":"...","dll_sha":"..."}'] [--json] [--out saida.json]

Exit: 0 = todos OK COM prova runtime; 1 = algum REPROVADO; 2 = sem prova runtime ou algum
      NAO_EXERCITADO/INDETERMINADO (nunca verde por fixture).
"""

import argparse
import importlib.util
import json
import math
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(os.path.dirname(AQUI))
REPO = os.path.dirname(TOOLS)
TESTES = os.path.join(TOOLS, "testes")
for _p in (TESTES, TOOLS):
    if _p not in sys.path:
        sys.path.insert(0, _p)

ESQUEMA = "KIT-10/cenarios/1"
TAREFA = "t_bbad760d"
TAREFA_CIC4 = "t_6dc6484b"
TAREFA_AUT7 = "t_674c5976"

OK, REPROVADO, NAO_EXERCITADO, INDETERMINADO = (
    "OK", "REPROVADO", "NAO_EXERCITADO", "INDETERMINADO")
EXIT_OK, EXIT_REPROVADO, EXIT_INCOMPLETO = 0, 1, 2

# Superficies/estagios que provam leitura POR EVENTO (achado C). "boot"/"prefab" NAO valem:
# o prefab de boot e o mesmo objeto para todos os eventos e nao carrega o efeito aplicado.
ESTAGIOS_DE_EVENTO = ("level-up", "combate", "dano", "status", "evento")
ESTAGIOS_DE_BOOT = ("boot", "prefab", "menu", "startup")

MOD_PADRAO = "BetterTooltips"

_CACHE = {}


# ------------------------------------------------------------------ reuso (import por caminho)

def _carregar(nome, caminho):
    if nome in _CACHE:
        return _CACHE[nome]
    if not os.path.isfile(caminho):
        _CACHE[nome] = None
        return None
    spec = importlib.util.spec_from_file_location(nome, caminho)
    modulo = importlib.util.module_from_spec(spec)
    sys.modules[nome] = modulo
    spec.loader.exec_module(modulo)
    _CACHE[nome] = modulo
    return modulo


def cic4():
    """`tooltips_shrines.py` (CIC-4) - importado, nunca reescrito."""
    return _carregar("kit10_cic4", os.path.join(TOOLS, "automacao", "cenarios", "tooltips_shrines.py"))


def aut7():
    """`estilo_atributos.py` (AUT-7) - importado, nunca reescrito."""
    return _carregar("kit10_aut7", os.path.join(TOOLS, "automacao", "estilo", "estilo_atributos.py"))


def regras_shrine():
    return _carregar("kit10_regras_shrine", os.path.join(TESTES, "regras_shrine.py"))


def regras_debugger():
    return _carregar("kit10_regras_debugger", os.path.join(TESTES, "regras_debugger.py"))


def regras_bct():
    return _carregar("kit10_regras_bct", os.path.join(TESTES, "regras_bct.py"))


# ------------------------------------------------------------------ observacoes

def _lista(observacoes):
    if isinstance(observacoes, dict):
        v = observacoes.get("observacoes")
        if isinstance(v, list):
            return [o for o in v if isinstance(o, dict)]
        return [observacoes] if observacoes else []
    if isinstance(observacoes, list):
        return [o for o in observacoes if isinstance(o, dict)]
    return []


def _campo(obs, nome):
    """Le um campo nas duas formas reais (probe cru / coletor normalizado)."""
    est = aut7()
    if est is not None:
        return est._campo(obs, nome)
    campos = obs.get("campos")
    if isinstance(campos, dict) and isinstance(campos.get(nome), dict):
        return campos[nome].get("valor")
    return obs.get(nome)


def _tipo(obs):
    """Tipo do cenario KIT-10 de uma observacao (`tipo`/`cenario`)."""
    return str(_campo(obs, "tipo") or obs.get("tipo") or obs.get("cenario") or "").strip().lower()


# --------------------------------------------------- validacao de medicao numerica (F8/F9)
# Regra do cartao (KIT-10F): MEDICAO AUSENTE e MEDICAO INVALIDA sao estados DISTINTOS.
#   * ausente (None)  -> (None, None)  -> LACUNA de coleta (NAO_EXERCITADO, nunca OK);
#   * invalida        -> (None, "<motivo>") -> DEFEITO (REPROVADO, nunca OK).
# `abs(float('NaN') - esperado) > 1e-9` e False, entao NaN/inf NAO podem depender de comparacao:
# a finitude e o TIPO tem de ser validados EXPLICITAMENTE antes de qualquer conta.

def _numero_finito(valor):
    """(float|None, problema|None): medicao numerica finita. NaN/inf/bool/string invalida = problema."""
    if valor is None:
        return None, None
    if isinstance(valor, bool):
        return None, "booleano"
    if isinstance(valor, str):
        s = valor.strip()
        if not s:
            return None, None
        try:
            f = float(s)
        except ValueError:
            return None, "string nao numerica"
    elif isinstance(valor, (int, float)):
        f = float(valor)
    else:
        return None, "tipo %s" % type(valor).__name__
    if not math.isfinite(f):
        return None, "nao finito (NaN/inf)"
    return f, None


def _inteiro_contagem(valor, minimo):
    """(int, problema|None): CONTAGEM inteira MEDIDA. Sem default, sem coercao, sem truncamento.

    F9 (KIT-10F): `instancias` de aura viva exige inteiro >= 1 medido (minimo=1); itens observados
    exigem inteiro >= 0 (minimo=0). Ausente, booleano, fracionario, nao finito, string nao numerica
    ou abaixo do minimo = problema (a medicao NAO prova a contagem). O primeiro item e sempre um
    `int` (0 quando ha problema) para o chamador so precisar checar o segundo.
    """
    if valor is None or isinstance(valor, bool):
        return 0, "ausente ou booleano"
    if isinstance(valor, str):
        s = valor.strip()
        if not s:
            return 0, "vazio"
        try:
            f = float(s)
        except ValueError:
            return 0, "string nao numerica"
    elif isinstance(valor, (int, float)):
        f = float(valor)
    else:
        return 0, "tipo %s" % type(valor).__name__
    if not math.isfinite(f):
        return 0, "nao finito"
    if f != int(f):
        return 0, "fracionario (%r): truncar esconderia o defeito" % (valor,)
    if int(f) < minimo:
        return 0, "abaixo do minimo %d" % minimo
    return int(f), None


# --------------------------------------------- propagacao da marca de FIXTURE do envelope (F11)

def _declara_fixture(obs):
    """True se ESTE dict declara procedencia fixture/sintetica (envelope OU observacao).

    F11 (KIT-10F): a marca de fixture nao pode SUMIR ao extrair `observacoes` de um envelope.
    Fonte hash/DLL hash/evidencia coerentes NAO anulam uma declaracao explicita de fixture.
    """
    if not isinstance(obs, dict):
        return False
    if str(obs.get("procedencia") or "").strip().lower() == "fixture":
        return True
    if obs.get("rotulo_fixture") is True or obs.get("sintetico") is True:
        return True
    if obs.get("evidencia_runtime") is False:
        return True
    return False


def _marcar_fixture(obs):
    """COPIA da observacao com a marca de fixture (nunca altera o dict do dono)."""
    copia = dict(obs)
    copia["rotulo_fixture"] = True
    if not str(copia.get("procedencia") or "").strip():
        copia["procedencia"] = "fixture"
    return copia



def _criterio(cid, obs, estado, esperado, observado, motivo, evidencia=None, extra=None):
    est = aut7()
    proc = est._procedencia(obs) if est is not None else "execucao"
    mod = (obs or {}).get("mod") or MOD_PADRAO
    c = {
        "id": cid, "mod": mod, "estado": estado, "classe": "runtime" if proc == "runtime" else "offline",
        "procedencia": proc, "prova_runtime": False, "esperado": esperado, "observado": observado,
        "evidencia": list(evidencia or []), "motivo": motivo, "tarefa_origem": TAREFA,
    }
    if extra:
        c.update(extra)
    return c


def _fechar(criterio, obs, identidade, defeito):
    """Aplica o fechamento do AUT-7: defeito fica REPROVADO; sem cadeia, no maximo NAO_EXERCITADO.

    Uma lacuna JA declarada pelo aspecto (campos ausentes, sem `estagio`...) NAO e promovida a OK
    pelo fechamento - so o caminho com TODOS os dados passa pela cadeia. E o fechamento que
    rebaixa um OK estrutural para NAO_EXERCITADO quando falta a cadeia de runtime.
    """
    est = aut7()
    if defeito:
        criterio["estado"] = REPROVADO
        criterio["prova_runtime"] = False
        return criterio
    ev = est._evidencia_obs(obs) if (est is not None and obs) else []
    if ev:
        criterio["evidencia"] = ev
    if criterio.get("estado") != OK:
        criterio["prova_runtime"] = False
        if criterio.get("estado") == NAO_EXERCITADO:
            criterio.setdefault("tipo_pendencia", "coleta_tecnica")
            criterio.setdefault("autorizacao_necessaria", False)
        return criterio
    if est is None:
        criterio["estado"] = NAO_EXERCITADO
        criterio["motivo"] = str(criterio.get("motivo", "")) + \
            " | fechamento indisponivel (estilo_atributos.py ausente)"
        return criterio
    estado, prova, problema = est._fecha(OK, obs or {}, identidade or {})
    if estado != OK:
        criterio["estado"] = estado
        criterio["motivo"] = str(criterio.get("motivo", "")) + \
            " | fechamento: " + (problema or "sem prova de runtime")
        criterio["tipo_pendencia"] = "coleta_tecnica"
        criterio["autorizacao_necessaria"] = False
    else:
        criterio["estado"] = OK
    criterio["prova_runtime"] = bool(prova)
    return criterio


# ------------------------------------------------------------------ A. contexto/dano/fonte-receptor

def _asp_contexto_dano(observacoes, identidade):
    """Tooltip (buff) x contexto (ground effect) x dano: o eixo decide DE QUEM e o bonus."""
    rs = regras_shrine()
    criterios = []
    if rs is None:
        return [_criterio("KIT-10/shrines/contexto-dano-fonte-receptor/indisponivel", None,
                          NAO_EXERCITADO, "oraculo regras_shrine.py + tabelas geradas", None,
                          "oraculo/tabelas do shrine indisponiveis: rode tools/gera_shrines_esperado.py")]
    try:
        pct, minimo1 = rs.percentuais()
        auras = rs.auras_da_tabela()
    except Exception as erro:  # noqa: BLE001
        return [_criterio("KIT-10/shrines/contexto-dano-fonte-receptor/indisponivel", None,
                          NAO_EXERCITADO, "tabelas geradas do shrine", "erro: %s" % erro,
                          "tabela gerada ausente/ilegivel (%s)" % type(erro).__name__)]

    for obs in observacoes:
        if _tipo(obs) != "contexto_dano":
            continue
        cid = "KIT-10/shrines/contexto-dano-fonte-receptor/%s" % (obs.get("objeto") or "caso")
        # F6 (KIT-10R2): `receptor_bonus` ausente virava 0 silenciosamente e o criterio fechava OK
        # declarando ler o eixo `Target` do RECEPTOR - mas com bonus 0 os eixos `Source` e `Target`
        # dao o MESMO valor, entao o eixo (o ponto do aspecto A) NAO foi exercitado. Guardamos o
        # campo CRU para distinguir AUSENTE de 0 medido, e exigimos bonus NAO-NULO para valer.
        receptor_campo = _campo(obs, "receptor_bonus")
        receptor = float(receptor_campo) if receptor_campo is not None else 0.0
        receptor_exercitado = receptor_campo is not None and abs(receptor) > 1e-9
        fonte = _campo(obs, "fonte_bonus")
        aura_dano = _campo(obs, "aura_dano")
        tipo_alvo = str(_campo(obs, "tipo_alvo") or "").lower()
        mh = _campo(obs, "maxhealth")
        dano = _campo(obs, "dano_observado")
        aura_buff, atributo = _campo(obs, "aura_buff"), _campo(obs, "atributo")
        contrib = _campo(obs, "contrib_observada")

        # F8 (KIT-10F): medicao numerica EXIGE tipo e FINITUDE. NaN/inf/bool/string invalida NUNCA
        # fecham OK: sao DEFEITO (valor presente, porem nao comparavel), estado distinto da medicao
        # AUSENTE (lacuna -> NAO_EXERCITADO). `abs(float(x) - esperado) > 1e-9` e False para NaN, o
        # que deixava o defeito passar como 0/igual. A guarda roda ANTES das comparacoes e preserva
        # intactos os ramos de ausencia (fonte/dano/contrib/receptor) e o RED das guardas antigas.
        formato = []
        for nome_campo, bruto in (("fonte_bonus", fonte), ("receptor_bonus", receptor_campo),
                                  ("maxhealth", mh), ("dano_observado", dano),
                                  ("contrib_observada", contrib)):
            _val, problema = _numero_finito(bruto)
            if problema is not None:
                formato.append("`%s`=%r nao e um numero finito valido (%s)" % (nome_campo, bruto, problema))
        if formato:
            criterios.append(_fechar(_criterio(
                cid, obs, REPROVADO,
                {"medicoes_numericas": "regras_shrine (RV-19/RV-30) - toda medicao de dano/bonus "
                                       "tem de ser numero FINITO; NaN/inf/bool/string invalida "
                                       "nunca fecham OK (fonte: regras_shrine / shrines-percentuais.csv)"},
                {"campos_invalidos": formato},
                "medicao presente porem INVALIDA (nao comparavel): " + "; ".join(formato)),
                obs, identidade, True))
            continue

        if not (aura_dano and tipo_alvo and mh is not None and (aura_dano, tipo_alvo) in pct):
            criterios.append(_fechar(_criterio(
                cid, obs, NAO_EXERCITADO,
                "aura de perigo da tabela de percentuais + MaxHealth + tipo do alvo", 
                {"aura_dano": aura_dano, "tipo_alvo": tipo_alvo, "maxhealth": mh},
                "campo ausente/fora da tabela (lacuna TECNICA de coleta: NAO e OK)"), obs, identidade, False))
            continue

        defeito, lacunas = [], []
        # (1) a FONTE do ground effect e o personagem VAZIO do shrine: bonus 0 (RV-30). Um
        # `fonte_bonus` != 0 e o defeito do `Source` injetado (RV-34) - o que "dobrava" o dano.
        if fonte is None:
            # F7 (KIT-10R2): campo NAO MEDIDO nao pode ser rotulado FALHOU. Ausente = lacuna de
            # coleta (NAO_EXERCITADO); o defeito RV-34 so e acusavel com o valor medido.
            lacunas.append("`fonte_bonus` ausente: o bonus da FONTE do ground effect NAO foi "
                           "medido (lacuna TECNICA de coleta - NAO e OK); o defeito do `Source` "
                           "injetado (RV-34) so e acusavel com o valor medido")
        elif abs(float(fonte)) > 1e-9:
            defeito.append("a FONTE do ground effect nao e o personagem vazio do shrine "
                           "(fonte_bonus=%r != 0): e o defeito do `Source` injetado (RV-34)" % (fonte,))
        esp_dano = rs.dano(float(mh), pct[(aura_dano, tipo_alvo)],
                           rs.bonus_do_eixo("Source", receptor), minimo1[aura_dano])
        if dano is None:
            # F5 (KIT-10R2): `dano_observado` AUSENTE nao entrava em guarda nenhuma e o conjunto
            # fechava OK/prova_runtime=True afirmando que o dano "bate com o oraculo" SEM nenhuma
            # medicao. Sem dano medido NAO ha criterio de dano - vira lacuna (NAO_EXERCITADO).
            lacunas.append("`dano_observado` ausente: o dano do ground effect NAO foi medido "
                           "(lacuna TECNICA de coleta - NAO e OK)")
        elif abs(float(dano) - esp_dano) > 1e-9:
            # o dano do ground effect NAO pode escalar com o bonus do jogador
            esp_jogador = rs.dano(float(mh), pct[(aura_dano, tipo_alvo)], receptor, minimo1[aura_dano])
            if receptor and abs(float(dano) - esp_jogador) < 1e-9:
                defeito.append("o dano do ground effect escalou com o bonus do RECEPTOR (%g) - "
                               "o eixo da aura de PERIGO e `Source` (bonus 0), nao o do jogador"
                               % receptor)
            else:
                defeito.append("dano observado=%s e esperado=%s (eixo Source, bonus 0)"
                               % (dano, esp_dano))

        # F6 (KIT-10R2): o eixo `Target` do RECEPTOR so e exercitado com `receptor_bonus` MEDIDO e
        # != 0 (com 0, `Source` e `Target` coincidem). Ausente ou 0 = eixo NAO exercitado (lacuna).
        if not receptor_exercitado:
            lacunas.append("`receptor_bonus` %s: o eixo `Target` do RECEPTOR NAO foi exercitado "
                           "(lacuna TECNICA de coleta - NAO e OK)"
                           % ("ausente" if receptor_campo is None
                              else "= 0 (os eixos `Source` e `Target` coincidem)"))

        esp_contrib = None
        if not aura_buff:
            # O criterio cobre TAMBEM a tooltip do RECEPTOR (eixo `Target`): sem `aura_buff` essa
            # metade NAO foi medida e nao pode fechar OK afirmando uma leitura que nao houve
            # (mesma classe de "runtime ausente nao recebe OK").
            lacunas.append("`aura_buff` ausente: a tooltip de BUFF do RECEPTOR (eixo `Target`) NAO "
                           "foi medida (lacuna TECNICA de coleta - NAO e OK)")
        elif not atributo or aura_buff not in auras or atributo not in (auras[aura_buff] or {}):
            # F3 (KIT-10R): buff declarado FORA da tabela (ou sem atributo) nao media a tooltip e
            # ainda devolvia OK. Tooltip nao medida NAO e OK - vira NAO_EXERCITADO.
            lacunas.append("a tooltip do buff foi declarada (aura_buff=%r, atributo=%r) mas nao "
                           "esta na tabela de esperados do shrine: a tooltip do RECEPTOR NAO "
                           "foi medida (lacuna TECNICA de coleta - NAO e OK)"
                           % (aura_buff, atributo))
        else:
            base = auras[aura_buff][atributo]
            esp_contrib = rs.escala(base, rs.bonus_do_eixo("Target", receptor))
            if contrib is None:
                lacunas.append("o buff '%s/%s' tem esperado independente, mas `contrib_observada` "
                               "esta ausente: a tooltip do RECEPTOR NAO foi medida (lacuna "
                               "TECNICA de coleta - NAO e OK)" % (aura_buff, atributo))
            elif not receptor_exercitado:
                # Sem `receptor_bonus` MEDIDO o esperado da tooltip dependeria de um valor NAO
                # medido: acusar defeito aqui seria rotular como FALHOU um campo nao medido (mesma
                # classe do F7). A lacuna do eixo `Target` ja foi registrada acima.
                pass
            elif abs(float(contrib) - esp_contrib) > 1e-9:
                defeito.append("a tooltip de BUFF do receptor deveria ler o bonus DELE (%g): "
                               "observado=%s esperado=%s" % (receptor, contrib, esp_contrib))

        esperado = {
            "dano_ground_effect": {"valor": esp_dano, "eixo": "Source", "bonus_da_fonte": 0.0,
                                   "fonte": "regras_shrine.dano + shrines-percentuais.csv (RV-30/RV-19 §4.2)"},
            "tooltip_buff_do_receptor": (
                {"valor": esp_contrib, "eixo": "Target", "bonus_do_receptor": receptor,
                 "fonte": "regras_shrine.escala + shrines-esperado.csv (%s/%s)" % (aura_buff, atributo)}
                if esp_contrib is not None else None),
        }
        observado = {"aura_dano": aura_dano, "tipo_alvo": tipo_alvo, "maxhealth": mh,
                     "dano": dano, "fonte_bonus": fonte, "receptor_bonus": receptor,
                     "aura_buff": aura_buff, "atributo": atributo, "contrib": contrib,
                     "lacunas": lacunas}
        if defeito:
            estado, motivo = REPROVADO, "; ".join(defeito)
        elif lacunas:
            estado, motivo = NAO_EXERCITADO, "; ".join(lacunas)
        else:
            estado, motivo = OK, ("dano do ground effect bate com o oraculo no eixo `Source` "
                                  "(bonus 0) e a tooltip de buff le o bonus do RECEPTOR "
                                  "(eixo `Target`)")
        criterios.append(_fechar(_criterio(
            cid, obs, estado, esperado, observado, motivo), obs, identidade, bool(defeito)))
    return criterios


# ------------------------------------------------------------------ B. worship / dobro preservado

def _asp_worship_dobro(observacoes, identidade):
    """Comportamento CONFIRMADO: instancia repetida de aura de GATILHO conta (DWA-2); de atributo, 1x."""
    rs = regras_shrine()
    criterios = []
    if rs is None:
        return [_criterio("KIT-10/shrines/worship-dobro-preservado/indisponivel", None,
                          NAO_EXERCITADO, "oraculo regras_shrine.py", None, "oraculo indisponivel")]
    for obs in observacoes:
        if _tipo(obs) != "worship_dobro":
            continue
        cid = "KIT-10/shrines/worship-dobro-preservado/%s" % (obs.get("objeto") or "caso")
        vivas = _campo(obs, "vivas") or []
        itens = _campo(obs, "itens_observados") or {}
        if not isinstance(itens, dict):
            itens = {}
        if not isinstance(vivas, list) or not vivas:
            criterios.append(_fechar(_criterio(
                cid, obs, NAO_EXERCITADO, "lista de auras vivas com `instancias` por aura", None,
                "sem `vivas` (lacuna TECNICA de coleta: NAO e OK)"), obs, identidade, False))
            continue
        canonicas = set(getattr(rs, "AURAS_DA_FAMILIA", ()) or ())
        try:
            canonicas |= set(rs.auras_da_tabela().keys())
        except Exception:  # noqa: BLE001 - tabela ausente nao invalida a familia da fonte
            pass
        esperado, observado, defeito, faltando, invalido = {}, {}, [], [], []
        exercitou_dobro = False
        for viva in vivas:
            aura = viva.get("aura")
            # F9 (KIT-10F): a AURA tem de ser CANONICA. Uma aura invencivel ("Inventada") nao e
            # membro da familia (RV-19 §2) e nao pode virar "1 esperado / 1 observado -> OK".
            if not aura or str(aura) not in canonicas:
                invalido.append("aura %r nao e uma aura canonica da familia (RV-19 §2 / "
                                "ShrineKeys): o efeito dela NAO foi provado" % (aura,))
                continue
            # F9 (KIT-10F): `instancias` e contagem INTEIRA MEDIDA - sem `default 1`, sem
            # `max(1, int(...))` (que zerava/truncava) e sem aceitar booleano/fracao. Sem a
            # contagem medida o "dobro" do gatilho NAO foi exercitado.
            n, problema_n = _inteiro_contagem(viva.get("instancias"), 1)
            if problema_n is not None:
                invalido.append("aura '%s' sem `instancias` inteiro positivo MEDIDO (%s): "
                                "default/coercao/truncamento NAO provam a contagem"
                                % (aura, problema_n))
                continue
            if rs.efeito_de_gatilho(aura) and n > 1:
                exercitou_dobro = True
            # Regra confirmada (regras_shrine.efeito_de_gatilho): gatilho conta POR INSTANCIA,
            # atributo conta UMA vez. O cenario PRESERVA o dobro do gatilho.
            esperado[aura] = n if rs.efeito_de_gatilho(aura) else 1
            got = itens.get(aura)
            observado[aura] = got
            if got is None:
                # F2 (KIT-10R): aura VIVA sem item observado era ignorada com `continue`, e o
                # conjunto saia com defeito=[] -> OK/prova_runtime=True. Nao medido NAO e OK.
                faltando.append(aura)
                continue
            n_itens, problema_itens = _inteiro_contagem(got, 0)
            if problema_itens is not None:
                invalido.append("aura '%s': `itens_observados`=%r nao e uma contagem inteira "
                                "valida (%s)" % (aura, got, problema_itens))
                continue
            observado[aura] = n_itens
            if n_itens != esperado[aura]:
                if rs.efeito_de_gatilho(aura) and n_itens == 1 and n > 1:
                    defeito.append("aura de GATILHO '%s' com %d instancias virou %d item: o "
                                   "'dobro' foi REMOVIDO (o motor avalia o gatilho por status vivo "
                                   "- DWA-2); comportamento confirmado NAO pode ser apagado para "
                                   "tornar o teste verde" % (aura, n, n_itens))
                else:
                    defeito.append("'%s': esperado %d item(ns) (regra confirmada) e observado %s"
                                   % (aura, esperado[aura], got))
        if defeito:
            estado, motivo = REPROVADO, "; ".join(defeito)
        elif invalido:
            # F9 (KIT-10F): aura/contagem INVALIDA ou NAO MEDIDA -> lacuna TECNICA (NAO_EXERCITADO).
            estado, motivo = NAO_EXERCITADO, "; ".join(invalido)
        elif faltando:
            estado, motivo = NAO_EXERCITADO, (
                "aura(s) viva(s) %s sem item em `itens_observados`: o numero de itens NAO foi "
                "medido (lacuna TECNICA de coleta: runtime ausente NAO recebe OK)"
                % ", ".join(sorted(str(a) for a in faltando)))
        elif not exercitou_dobro:
            # F9 (KIT-10F): sem um gatilho REPETIDO (>= 2 instancias medidas) o "dobro" NAO foi
            # exercitado - o aspecto vira lacuna declarada, nunca OK por vacuidade.
            estado, motivo = NAO_EXERCITADO, (
                "nenhuma aura de GATILHO com instancia repetida (>=2) MEDIDA: sem gatilho repetido "
                "o 'dobro' NAO foi exercitado (lacuna TECNICA de coleta - NAO e OK)")
        else:
            estado, motivo = OK, (
                "cada aura conta o numero de itens que a regra confirmada manda (gatilho por "
                "instancia; atributo 1x) - o dobro do gatilho preservado")
        criterios.append(_fechar(_criterio(
            cid, obs, estado,
            {"itens_por_aura": esperado, "regra": "regras_shrine.efeito_de_gatilho (DWA-2) + RV-46"},
            {"itens_observados": observado, "vivas": vivas, "sem_observacao": sorted(
                str(a) for a in faltando)},
            motivo), obs, identidade, bool(defeito)))
    return criterios


# ------------------------------------------------------------------ C. estilo por evento (nao boot)

def _asp_por_evento(observacoes, identidade):
    """BetterFont/BetterCombatText: superficie de estilo lida no EVENTO, nunca no prefab de boot."""
    est, bct = aut7(), regras_bct()
    criterios = []
    if est is None or bct is None:
        return [_criterio("KIT-10/estilo/por-evento-nao-boot/indisponivel", None, NAO_EXERCITADO,
                          "avaliador AUT-7 + regras_bct.py", None, "modulos de estilo indisponiveis")]
    sup = list(bct.SUPERFICIES_DO_BCT)
    for obs in observacoes:
        if _tipo(obs) != "estilo_evento":
            continue
        alvo = "%s %s" % (_campo(obs, "objeto") or obs.get("objeto") or "",
                          _campo(obs, "componente") or "")
        superficies = est._superficies_no_alvo(alvo, sup)
        cid = "KIT-10/estilo/por-evento-nao-boot/%s" % (obs.get("objeto") or "caso")
        if not superficies:
            criterios.append(_fechar(_criterio(
                cid, obs, NAO_EXERCITADO,
                "alvo de uma superficie canonica do BCT: %s" % ", ".join(sup),
                {"alvo": alvo}, "alvo sem superficie canonica reconhecida (por TOKEN, nunca "
                "substring) - lacuna TECNICA de coleta: NAO e OK"), obs, identidade, False))
            continue
        estagio = str(_campo(obs, "estagio") or "").strip().lower()
        evento_id = _campo(obs, "evento_id")
        defeito = []
        if estagio in ESTAGIOS_DE_BOOT:
            defeito.append("superficie '%s' lida em estagio=%r: o prefab de boot e o mesmo objeto "
                           "para todos os eventos e nao carrega o efeito aplicado - a leitura tem de "
                           "ser do EVENTO" % (superficies[0], estagio))
        elif estagio not in ESTAGIOS_DE_EVENTO:
            # F1 (KIT-10R): a whitelist tem de valer em TODOS os ramos. Sem ela um estagio inventado
            # (ex.: "banana") + `evento_id` caia no ramo final e fechava OK/prova_runtime=True.
            criterios.append(_fechar(_criterio(
                cid, obs, NAO_EXERCITADO,
                "`estagio` de EVENTO (%s) + `evento_id` independente" % ", ".join(ESTAGIOS_DE_EVENTO),
                {"estagio": estagio, "evento_id": evento_id},
                ("sem `estagio` declarado: nao da para provar leitura por evento (lacuna TECNICA)"
                 if not estagio else
                 "estagio=%r fora da whitelist de EVENTO (%s): leitura por evento NAO provada "
                 "(lacuna TECNICA de coleta - NAO e OK)" % (estagio, ", ".join(ESTAGIOS_DE_EVENTO)))),
                obs, identidade, False))
            continue
        elif not evento_id:
            criterios.append(_fechar(_criterio(
                cid, obs, NAO_EXERCITADO,
                "`evento_id` independente (leitura idempotente por evento)",
                {"estagio": estagio, "evento_id": evento_id},
                "estagio de evento sem `evento_id`: sem identidade de evento a leitura pode ser "
                "repetida no mesmo quadro (lacuna TECNICA)"), obs, identidade, False))
            continue
        criterios.append(_fechar(_criterio(
            cid, obs, REPROVADO if defeito else OK,
            "leitura de estilo do EVENTO (%s) no alvo '%s', com `evento_id`; NUNCA do prefab de boot"
            % ("/".join(ESTAGIOS_DE_EVENTO), superficies[0]),
            {"alvo": alvo, "superficies": superficies, "estagio": estagio, "evento_id": evento_id},
            "; ".join(defeito) if defeito else
            "superficie canonica lida no evento (%s), nao no prefab de boot" % estagio),
            obs, identidade, bool(defeito)))
    return criterios


# ------------------------------------------------------------------ D. debugger sem truncar

def _asp_debugger_sem_truncar(observacoes, identidade):
    """RoguelikeDebugger: o contrato do dump, com a descricao NAO truncada."""
    rd = regras_debugger()
    criterios = []
    if rd is None:
        return [_criterio("KIT-10/debugger/sem-truncar/indisponivel", None, NAO_EXERCITADO,
                          "regras_debugger.py + tools/census.py", None, "regras do dump indisponiveis")]
    try:
        censo = rd.carrega_censo()
    except Exception as erro:  # noqa: BLE001
        return [_criterio("KIT-10/debugger/sem-truncar/indisponivel", None, NAO_EXERCITADO,
                          "tools/census.py", "erro: %s" % erro, "censo indisponivel")]
    for obs in observacoes:
        if _tipo(obs) != "debugger_dump":
            continue
        cid = "KIT-10/debugger/sem-truncar/%s" % (obs.get("objeto") or "caso")
        texto = _campo(obs, "log_texto") or ""
        linhas_declaradas = str(texto).splitlines()
        linhas = [ln for ln in linhas_declaradas if censo.LINE.match(ln)]
        if not linhas:
            criterios.append(_fechar(_criterio(
                cid, obs, NAO_EXERCITADO, "linha de dump reconhecida pelo censo (desc= por ultimo)",
                {"linhas": len(linhas_declaradas)},
                "nenhuma linha `[Categoria] '...' |` reconhecida no log (lacuna TECNICA de coleta: "
                "NAO e OK)"), obs, identidade, False))
            continue
        defeito, falhas = [], []
        # F10 (KIT-10F): confere TODA linha DECLARADA do log, nao so as que o censo reconhece. Uma
        # entrada declarada do dump que o parser real NAO reconhece nao pode ser DESCARTADA antes de
        # avaliar (era o defeito que sumia: `[Status] Foo | desc="sumiu"`, sem as aspas do `'nome'`).
        # Linhas que nao sao do dump (sem `desc=`) seguem NEUTRAS.
        for ln in linhas_declaradas:
            if censo.LINE.match(ln):
                falhas += rd.contrato_da_linha(censo, ln)
                _cat, _nome, _campos, desc, f2 = rd.confere_linha(censo, ln)
                falhas += f2
                if desc is None:
                    falhas.append("a `desc=` nao ancorou no FIM da linha: a descricao foi TRUNCADA")
                elif "|" in desc:
                    # F10 (KIT-10F): `contrato_da_linha` PULA o campo `desc` (regras_debugger
                    # l.167-168). Um `|` DENTRO da descricao trunca o valor em silencio e NAO pode
                    # passar - conferido aqui, como o AUT-7 ja faz.
                    falhas.append("o valor do campo 'desc' tem '|' - o FIELD trunca em silencio")
            elif "desc=" in ln:
                # F10 (KIT-10F): linha DECLARADA dump (tem `desc=`) que o parser real NAO reconhece.
                falhas.append("linha declarada dump nao reconhecida pelo parser real (o `'nome'` do "
                              "`LINE` mudou): a entrada defeituosa foi descartada antes de avaliar")
        for f in falhas:
            defeito.append(f)
        criterios.append(_fechar(_criterio(
            cid, obs, REPROVADO if defeito else OK,
            "dump com `desc=` por ULTIMO, sem `|` em nenhum valor e `desc` ancorada no fim "
            "(fonte: regras_debugger.contrato_da_linha/confere_linha -> tools/census.py)",
            {"linhas_declaradas": len(linhas_declaradas), "linhas_reconhecidas": len(linhas),
             "falhas": sorted(set(falhas))},
            "; ".join(sorted(set(defeito))) if defeito else
            "contrato do dump respeitado e a descricao nao truncada"), obs, identidade, bool(defeito)))
    return criterios


# ------------------------------------------------------------------ E. atributos base x final (F12)

# Contrato OFFLINE (KIT-10F, achado F12) - adaptacao MINIMA e LOCAL; NAO substitui o probe.
#
# Forma CRUA (probe AUT-4, campos planos):
#   {"tipo": "atributos_base_final", "mod": "BetterStats", "objeto": "Attributes_Text",
#    "personagem": "<quem teve os valores MEDIDOS>", "personagem_display": "<quem esta na TELA>",
#    "atributo": "Strength", "texto_renderizado": "10 (15)",
#    "saved_map": {"Strength": 10},        # base PURA investida (NAO `character[nome]`)
#    "atributos_final": {"Strength": 15}}  # valor FINAL do motor
# Forma NORMALIZADA (coletor CIC-5): os mesmos nomes dentro de `campos: {nome: {"valor": ...}}`
# (lida por `_campo`/AUT-7). O `esperado` sai SEMPRE de `saved_map`/`atributos_final` MEDIDOS,
# NUNCA do `texto_renderizado` (o display e o OBSERVADO, nao a fonte).
# LACUNA TECNICA declarada: o probe/coletor ATUAL nao emite `saved_map`/`atributos_final`/
# `personagem_display`; sem eles o aspecto fica NAO_EXERCITADO (nao se edita probe/mod aqui).

def _asp_atributos_base_final(observacoes, identidade):
    """BetterStats: o texto `base (final)` tem de bater com os numeros MEDIDOS (SavedMap x motor)."""
    esperado_base = ("na ficha/level-up o texto sai `base (final)`, com a base do valor PURO do "
                     "SavedMap e o final do motor; `character[nome]` NAO serve como base "
                     "(fonte: BetterStats BS-1a / AUT-7)")
    criterios = []
    for obs in observacoes:
        if _tipo(obs) not in ("atributos_base_final", "atributos"):
            continue
        cid = "KIT-10/atributos/base-vs-final/%s" % (obs.get("objeto") or "caso")
        atributo = _campo(obs, "atributo")
        texto = _campo(obs, "texto_renderizado")
        personagem = _campo(obs, "personagem")
        personagem_display = _campo(obs, "personagem_display")
        saved = _campo(obs, "saved_map")
        final = _campo(obs, "atributos_final")
        faltando = [n for n, v in (("atributo", atributo), ("texto_renderizado", texto),
                                   ("personagem", personagem),
                                   ("personagem_display", personagem_display),
                                   ("saved_map", saved), ("atributos_final", final)) if not v]
        if faltando:
            criterios.append(_fechar(_criterio(
                cid, obs, NAO_EXERCITADO, esperado_base,
                {"faltando": faltando},
                "campos do contrato de atributos ausentes (%s): sem os valores MEDIDOS "
                "independentes (SavedMap base x final do motor) o display NAO pode ser confrontado "
                "(lacuna TECNICA de coleta - NAO e OK)" % ", ".join(faltando)), obs, identidade, False))
            continue
        if not isinstance(saved, dict) or not isinstance(final, dict) or atributo not in saved \
                or atributo not in final:
            criterios.append(_fechar(_criterio(
                cid, obs, NAO_EXERCITADO, esperado_base,
                {"atributo": atributo, "saved_map": saved, "atributos_final": final},
                "`saved_map`/`atributos_final` nao trazem o atributo %r: leitura independente "
                "ausente (lacuna TECNICA de coleta - NAO e OK)" % (atributo,)),
                obs, identidade, False))
            continue
        base, p_base = _numero_finito(saved.get(atributo))
        fim, p_fim = _numero_finito(final.get(atributo))
        if p_base is not None or p_fim is not None:
            criterios.append(_fechar(_criterio(
                cid, obs, REPROVADO, esperado_base,
                {"saved_map": saved.get(atributo), "atributos_final": final.get(atributo)},
                "valor MEDIDO invalido (base=%r:%s final=%r:%s): NaN/inf/bool/string invalida nunca "
                "fecham OK" % (saved.get(atributo), p_base, final.get(atributo), p_fim)),
                obs, identidade, True))
            continue
        if base is None or fim is None:
            criterios.append(_fechar(_criterio(
                cid, obs, NAO_EXERCITADO, esperado_base,
                {"saved_map": saved.get(atributo), "atributos_final": final.get(atributo)},
                "valor MEDIDO de %r ausente/vazio na leitura independente (lacuna TECNICA de "
                "coleta - NAO e OK)" % (atributo,)), obs, identidade, False))
            continue
        if str(personagem).strip() != str(personagem_display).strip():
            criterios.append(_fechar(_criterio(
                cid, obs, REPROVADO, esperado_base,
                {"personagem_medido": personagem, "personagem_display": personagem_display},
                "TROCA de personagem: os valores foram medidos em %r e a tela lida e de %r - o "
                "display nao pode ser confrontado com o numero de outro personagem"
                % (personagem, personagem_display)), obs, identidade, True))
            continue
        m = re.search(r"(-?\d+)\s*\(\s*(-?\d+)\s*\)", str(texto))
        if not m:
            criterios.append(_fechar(_criterio(
                cid, obs, NAO_EXERCITADO, esperado_base,
                {"texto_renderizado": texto},
                "nenhum texto `base (final)` na observacao: o display NAO foi lido "
                "(lacuna TECNICA de coleta - NAO e OK)"), obs, identidade, False))
            continue
        disp_base, disp_final = int(m.group(1)), int(m.group(2))
        esp_base, esp_final = int(round(base)), int(round(fim))
        defeito = []
        if disp_base != esp_base:
            defeito.append("a BASE exibida (%d) nao e o valor PURO medido do SavedMap (%d)"
                           % (disp_base, esp_base))
        if disp_final != esp_final:
            defeito.append("o FINAL exibido (%d) nao e o valor medido do motor (%d)"
                           % (disp_final, esp_final))
        criterios.append(_fechar(_criterio(
            cid, obs, REPROVADO if defeito else OK,
            {"base_pura": saved.get(atributo), "final_motor": final.get(atributo),
             "atributo": atributo, "personagem": personagem,
             "fonte": esperado_base},
            {"display_base": disp_base, "display_final": disp_final, "texto": texto},
            "; ".join(defeito) if defeito else
            "o texto `base (final)` bate com os valores MEDIDOS (SavedMap puro x final do motor)"),
            obs, identidade, bool(defeito)))
    return criterios


_ASPECTOS = (
    ("KIT-10/shrines/contexto-dano-fonte-receptor", _asp_contexto_dano),
    ("KIT-10/shrines/worship-dobro-preservado", _asp_worship_dobro),
    ("KIT-10/estilo/por-evento-nao-boot", _asp_por_evento),
    ("KIT-10/debugger/sem-truncar", _asp_debugger_sem_truncar),
    ("KIT-10/atributos/base-vs-final", _asp_atributos_base_final),
)


# ------------------------------------------------------------------ API do contrato v1

def avaliar(observacoes, identidade=None):
    """Criterios do CIC-4 + AUT-7 (reuso literal) + os aspectos novos do KIT-10.

    F11 (KIT-10F): a marca de FIXTURE do ENVELOPE (ou da propria observacao) e propagada
    failclosed a cada observacao antes de avaliar - o envelope NAO pode perder
    `procedencia`/`rotulo_fixture`/`sintetico`/`evidencia_runtime`. A propagacao usa COPIA:
    o input do dono fica intacto.
    """
    ident = identidade if isinstance(identidade, dict) else {}
    obs = _lista(observacoes)
    env_fixture = _declara_fixture(observacoes)
    obs = [_marcar_fixture(o) if (env_fixture or _declara_fixture(o)) else o for o in obs]

    criterios = []

    c4 = cic4()
    if c4 is not None:
        try:
            criterios += c4.avaliar(obs, ident)
        except Exception as erro:  # noqa: BLE001
            criterios.append(_criterio("KIT-10/reuso/cic4-indisponivel", None, NAO_EXERCITADO,
                                       "avaliador CIC-4 (tooltips_shrines.py)", "erro: %s" % erro,
                                       "reuso do CIC-4 falhou (%s)" % type(erro).__name__))

    e7 = aut7()
    if e7 is not None:
        try:
            criterios += e7.avaliar(obs, ident)
        except Exception as erro:  # noqa: BLE001
            criterios.append(_criterio("KIT-10/reuso/aut7-indisponivel", None, NAO_EXERCITADO,
                                       "avaliador AUT-7 (estilo_atributos.py)", "erro: %s" % erro,
                                       "reuso do AUT-7 falhou (%s)" % type(erro).__name__))

    for cid, fn in _ASPECTOS:
        try:
            criterios += [c for c in (fn(obs, ident) or []) if isinstance(c, dict)]
        except Exception as erro:  # noqa: BLE001
            criterios.append(_criterio(cid + "/indisponivel", None, INDETERMINADO,
                                       "avaliar sem excecao",
                                       "erro: %s: %s" % (type(erro).__name__, erro),
                                       "observacao malformada derrubou o aspecto (id preservado)"))
    return criterios


def resumo(criterios):
    cont = {OK: 0, REPROVADO: 0, NAO_EXERCITADO: 0, INDETERMINADO: 0}
    for c in criterios:
        cont[c["estado"]] = cont.get(c["estado"], 0) + 1
    provados = sum(1 for c in criterios if c.get("prova_runtime"))
    return {"total": len(criterios), **cont, "com_prova_runtime": provados}


def exit_de(criterios):
    cont = resumo(criterios)
    if cont.get(REPROVADO):
        return EXIT_REPROVADO
    if cont.get(NAO_EXERCITADO) or cont.get(INDETERMINADO):
        return EXIT_INCOMPLETO
    if not cont.get("com_prova_runtime"):
        return EXIT_INCOMPLETO
    return EXIT_OK


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
    ap = argparse.ArgumentParser(description="KIT-10 - cenarios de tooltips/shrines/estilo (offline).")
    ap.add_argument("--observacoes", required=True)
    ap.add_argument("--identidade", default=None)
    ap.add_argument("--fonte-sha", default=None)
    ap.add_argument("--dll-sha", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--json", action="store_true")
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

    criterios = avaliar(observacoes, ident)
    cont = resumo(criterios)
    codigo = exit_de(criterios)
    saida = {"esquema": ESQUEMA, "tarefa_origem": TAREFA,
             "identidade_suficiente": bool(ident.get("fonte_sha") and ident.get("dll_sha")),
             "resumo": cont, "exit_code": codigo, "criterios": criterios}
    texto = json.dumps(saida, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(texto + "\n")
    if args.json:
        print(texto)
        return codigo
    print("=" * 78)
    print("KIT-10 - cenarios de tooltips/shrines/estilo (offline)")
    print("  observacoes: %s" % args.observacoes)
    print("  identidade suficiente: %s" % saida["identidade_suficiente"])
    print("=" * 78)
    for c in criterios:
        if not c["id"].startswith("KIT-10/"):
            continue
        m = {"OK": "[OK]     ", "REPROVADO": "[REPROV] ", "NAO_EXERCITADO": "[NAO-EX] ",
             "INDETERMINADO": "[INDET]  "}.get(c["estado"], "[?]      ")
        print("  %s %-58s %s" % (m, c["id"], c["motivo"]))
    print("\n== RESULTADO ==")
    print("  " + ", ".join("%s=%d" % (k, cont[k]) for k in (OK, REPROVADO, NAO_EXERCITADO, INDETERMINADO)))
    print("  com prova runtime: %d  · exit=%d" % (cont["com_prova_runtime"], codigo))
    return codigo


if __name__ == "__main__":
    sys.exit(main())
