#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rstv13.py - RSTV-13: QUAIS PORTOES VALEM NO MAPA x NA BATALHA (lido do FONTE vivo).

O DEFEITO QUE ESTA BIBLIOTECA TRAVA
-----------------------------------
O dono relatou o sintoma (5): "passeando no mapa o botao nao aparece". O log da sessao de 02/10
mostra o botao do HUD escondido, entre outros, por "nao e o turno do jogador
(Root.IsPlayerTurnAndReady=false)" e "posicionamento inicial em andamento (Root.SpawnPlacementActive)"
— portoes que descrevem UMA BATALHA EM ANDAMENTO. Aplicados ao MAPA-MUNDO eles escondem o botao
justamente enquanto o jogador passeia:

  * `IsPlayerTurnAndReady` fica no ULTIMO valor do combate anterior (`GameLogic` l.111904 seta false
    no fim do turno) — no mapa ele nao quer dizer nada;
  * `SpawnPlacementActive` so existe no setup da batalha (`Root` l.112152 liga, l.112165 desliga);
  * `mira` (`HexCellManager.CurrentState == PlayerState.Action`), `AnyActingCharactersInBattle` e
    `AnyMovingCharactersInBattle` idem: sao conceitos de batalha.

O QUE ESTAS REGRAS TRAVAM
-------------------------
1. NO FONTE, o `RunTargets.GateOk` tem os portoes de batalha DENTRO do ramo
   `if (estado == GUIState.InBattle)` e os UNIVERSAIS (ping/janela) FORA dele. A checagem e
   estrutural: divide o corpo EFETIVO de `GateOk` no marcador do ramo de batalha e exige que cada
   trecho esteja do lado certo — um portao de batalha que voltar para o lado "de fora" (o defeito)
   REPROVA, dizendo QUAL portao.
2. O MODELO PURO: no mapa (`estado != battle`) os portoes de batalha NAO bloqueiam (o botao
   APARECE); em batalha cada um deles continua bloqueando (a seguranca nao foi afrouxada).

COMO O ESPERADO E OBTIDO
------------------------
O fonte e lido AO VIVO de `RoguelikeSkillTreeVisualizer/RunTargets.cs` (nao uma copia). O plantio do
defeito (`fonte_com_batalha_no_mapa`) devolve o MESMO texto com o portao de batalha reinjetado FORA
do ramo — e a isca (`cp_rstv13_batalha_no_mapa.py`) que prova que as checagens reprovam de verdade.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import recorte as rec

# Assinatura exata lida do fonte. Se o nome mudar, a checagem REPROVA dizendo qual sumiu.
GATE_OK = "internal static bool GateOk(out string motivo)"

# O marcador do ramo de batalha. Tudo ANTES dele e o lado "universal"; tudo DEPOIS, o "de batalha".
RAMO_DE_BATALHA = "if (estado == GUIState.InBattle)"

# Portoes UNIVERSAIS: valem em qualquer estado permitido (InBattle/InWorldMap/InTown).
# Campo -> trecho que PROVA o portao no corpo de `GateOk`.
GATES_UNIVERSAIS = (
    ("ping", "PingModeActive"),
    ("janela", "AnyUIWindowOpen"),
)

# Portoes DE BATALHA (RSTV-13): so existem numa batalha em andamento. Campo -> trecho.
GATES_DE_BATALHA = (
    ("mira", "PlayerState.Action"),
    ("spawn", "SpawnPlacementActive"),
    ("turno", "IsPlayerTurnAndReady"),
    ("acting", "AnyActingCharactersInBattle"),
    ("moving", "AnyMovingCharactersInBattle"),
)

# ------------------------------------------------------------------ caminhos ---

def caminho_do_fonte():
    return os.path.join(arc.raiz_do_repo(), "RoguelikeSkillTreeVisualizer", "RunTargets.cs")


def fonte():
    """O fonte vivo do mod (nao uma copia: a expectativa fica amarrada ao que sera compilado)."""
    with open(caminho_do_fonte(), encoding="utf-8") as fh:
        return fh.read()


def _gate(src):
    return rec.corpo_do_metodo(rec.codigo_efetivo(src), GATE_OK)


# ------------------------------------------------------------------ modelo puro ---
# Os MESMOS campos do `GateOk`, mas por ESTADO. `True` = a condicao esta satisfeita (NAO bloqueia).

ESTADOS = ("battle", "map", "town")

CENARIO = {
    "gui": True,
    "roguelike": True,
    "estado_ok": True,     # GUIState na whitelist (InBattle/InWorldMap/InTown)
    "levelup": False,
    "ping": True,
    "janela": True,
    "mira": True,
    "spawn": True,
    "turno": True,
    "acting": True,
    "moving": True,
}

EM_BATALHA = "battle"


def portao_por_estado(estado, c):
    """Transcricao PURA do `GateOk` (RSTV-13): devolve True se o botao PODE aparecer nesse estado."""
    if not c["gui"]:
        return False
    if not c["roguelike"]:
        return False
    if not c["estado_ok"]:
        return False
    if c["levelup"]:
        return True
    if not c["ping"]:
        return False
    if not c["janela"]:
        return False
    if estado == EM_BATALHA:
        for campo in ("mira", "spawn", "turno", "acting", "moving"):
            if not c[campo]:
                return False
    return True


def portao_com_batalha_no_mapa(estado, c):
    """O DEFEITO (pre-RSTV-13): os portoes de batalha valem em QUALQUER estado, inclusive no mapa.

    E a isca embutida: o MESMO cenario de mapa que a regra nova LIBERA tem de NAO liberar aqui.
    """
    if not c["gui"]:
        return False
    if not c["roguelike"]:
        return False
    if not c["estado_ok"]:
        return False
    if c["levelup"]:
        return True
    if not c["mira"]:
        return False
    if not c["ping"]:
        return False
    if not c["janela"]:
        return False
    if not c["spawn"]:
        return False
    if not c["turno"]:
        return False
    if not c["acting"]:
        return False
    if not c["moving"]:
        return False
    return True


def campos_do_modelo():
    """As chaves do cenario (fonte unica do nome dos campos)."""
    return list(CENARIO.keys())


# ------------------------------------------------------------------ checagens ---

def _divisao(src):
    """(fora, dentro): o corpo EFETIVO de `GateOk` dividido no `if (estado == GUIState.InBattle)`.

    `fora` = o trecho UNIVERSAL (antes do ramo); `dentro` = o ramo de batalha ate o fim do metodo.
    FALHA ALTO se o ramo de batalha nao existe (sem ele nao ha como separar mapa de batalha).
    """
    gate = _gate(src)
    i = gate.find(RAMO_DE_BATALHA)
    arc.exigir(i >= 0,
               "o `GateOk` NAO tem o ramo `%s` — sem ele nao da para separar os portoes de mapa e "
               "de batalha" % RAMO_DE_BATALHA)
    return gate[:i], gate[i:]


def falhas_do_gate_por_estado(src):
    """Defeitos do portao por estado no FONTE. Lista vazia = o conserto esta de pe."""
    falhas = []

    if GATE_OK not in rec.codigo_efetivo(src):
        return ["nao achei %s no fonte" % GATE_OK]

    fora, dentro = _divisao(src)

    # 1) Os portoes UNIVERSAIS tem de estar no lado de FORA (valem no mapa tambem).
    for nome, trecho in GATES_UNIVERSAIS:
        if trecho not in fora:
            falhas.append("o portao universal %r (trecho %r) saiu do lado comum do GateOk — ele "
                          "deixaria de valer no mapa" % (nome, trecho))

    # 2) Os portoes DE BATALHA tem de estar no lado de DENTRO (o ramo InBattle) e NAO fora.
    for nome, trecho in GATES_DE_BATALHA:
        if trecho in fora:
            falhas.append("o portao de BATALHA %r (trecho %r) esta FORA do ramo `%s` — ele volta a "
                          "esconder o botao no MAPA-MUNDO (o sintoma do dono)"
                          % (nome, trecho, RAMO_DE_BATALHA))
        elif trecho not in dentro:
            falhas.append("o portao de BATALHA %r (trecho %r) sumiu do GateOk — a seguranca em "
                          "batalha foi afrouxada" % (nome, trecho))

    return falhas


# ------------------------------------------------------------ plantio do defeito ---

_ANCORA_RAMO = "                if (estado == GUIState.InBattle)\n                {\n"

# O defeito ANTIGO: o `SpawnPlacementActive` (e os outros portoes de batalha) valiam em QUALQUER
# estado, inclusive passeando no mapa. Reinjetado FORA do ramo de batalha.
_DEFEITO_SPAWN_FORA = (
    "                if (root.SpawnPlacementActive)\n"
    "                {\n"
    "                    motivo = \"posicionamento inicial em andamento (Root.SpawnPlacementActive)\";\n"
    "                    return false;\n"
    "                }\n"
    "\n"
) + _ANCORA_RAMO


def fonte_com_batalha_no_mapa(src=None):
    """O MESMO fonte com o portao de batalha reinjetado FORA do ramo `InBattle` (o defeito).

    Nao mexe em arquivo nenhum: devolve o texto. E a isca que prova que a checagem pega o portao
    de batalha valendo no mapa.
    """
    texto = fonte() if src is None else src
    if _ANCORA_RAMO not in texto:
        return texto
    return texto.replace(_ANCORA_RAMO, _DEFEITO_SPAWN_FORA, 1)
