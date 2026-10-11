#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rstv13.py - RSTV-13 (atualizado pela RSTV-30): QUAIS GUARDAS VALEM NO MAPA x NA BATALHA.

O DEFEITO QUE ESTA BIBLIOTECA TRAVA
-----------------------------------
O dono relatou o sintoma (5): "passeando no mapa o botao nao aparece". O log da sessao de 02/10
mostra o botao do HUD escondido, entre outros, por "nao e o turno do jogador
(Root.IsPlayerTurnAndReady=false)" e "posicionamento inicial em andamento (Root.SpawnPlacementActive)"
— guardas que descrevem UMA BATALHA EM ANDAMENTO. Aplicadas ao MAPA-MUNDO elas escondem o botao
justamente enquanto o jogador passeia.

O QUE A RSTV-30 MUDOU AQUI
--------------------------
A RSTV-13 tirou do lado "universal" as guardas de batalha. A RSTV-30 foi alem: `turno`, `acting` e
`moving` deixaram de existir como guarda (elas faziam o botao piscar quando qualquer personagem agia
— o defeito relatado em 06/10) e o portao deixou de decidir a VISIBILIDADE (ele decide so' o CLIQUE).
Sobraram DUAS guardas de batalha, as de DANO REAL: a mira de skill e o posicionamento inicial.

O QUE ESTAS REGRAS TRAVAM
-------------------------
1. NO FONTE, o `RunTargets.GateOk` tem as guardas de batalha DENTRO do ramo
   `if (gui.CurrentGuiState == GUIState.InBattle)` e as UNIVERSAIS (ping/janela) FORA dele. A
   checagem e' estrutural: divide o corpo EFETIVO de `GateOk` no marcador do ramo de batalha e exige
   que cada trecho esteja do lado certo — uma guarda de batalha que voltar para o lado "de fora" (o
   defeito) REPROVA, dizendo QUAL guarda;
2. O MODELO PURO: no mapa (`estado != battle`) as guardas de batalha NAO bloqueiam o clique; em
   batalha cada uma delas continua bloqueando (a seguranca nao foi afrouxada);
3. as guardas que a RSTV-30 REMOVEU (`IsPlayerTurnAndReady`, `AnyActingCharactersInBattle`,
   `AnyMovingCharactersInBattle`) NAO podem reaparecer em lugar nenhum do portao.

COMO O ESPERADO E OBTIDO
------------------------
O fonte e' lido AO VIVO de `RoguelikeSkillTreeVisualizer/RunTargets.cs` (nao uma copia). O plantio do
defeito (`fonte_com_batalha_no_mapa`) devolve o MESMO texto com a guarda de batalha reinjetada FORA
do ramo — e' a isca (`cp_rstv13_batalha_no_mapa.py`) que prova que as checagens reprovam de verdade.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import recorte as rec

# Assinatura exata lida do fonte. Se o nome mudar, a checagem REPROVA dizendo qual sumiu.
GATE_OK = "internal static bool GateOk(out string motivo)"

# O marcador do ramo de batalha. Tudo ANTES dele e' o lado "universal"; tudo DEPOIS, o "de batalha".
RAMO_DE_BATALHA = "if (gui.CurrentGuiState == GUIState.InBattle)"

# Guardas UNIVERSAIS: valem em qualquer estado em que o HUD esta' na tela.
# Campo -> trecho que PROVA a guarda no corpo de `GateOk`.
GATES_UNIVERSAIS = (
    ("ping", "PingModeActive"),
    ("janela", "AnyUIWindowOpen"),
)

# Guardas DE BATALHA (RSTV-13 + RSTV-30): so' existem numa batalha em andamento e sao as de DANO
# REAL (a RSTV-30 removeu turno/acting/moving). Campo -> trecho.
GATES_DE_BATALHA = (
    ("mira", "PlayerState.Action"),
    ("spawn", "SpawnPlacementActive"),
)

# Guardas que a RSTV-30 REMOVEU do portao: presentes em QUALQUER lugar do `GateOk` = regressao.
GATES_REMOVIDOS = (
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
    "levelup": False,
    "ping": True,
    "janela": True,
    "mira": True,
    "spawn": True,
}

EM_BATALHA = "battle"


def portao_por_estado(estado, c):
    """Transcricao PURA do `GateOk` (RSTV-13 + RSTV-30): devolve True se o CLIQUE pode abrir."""
    if not c["gui"]:
        return False
    if not c["roguelike"]:
        return False
    if c["levelup"]:
        return True
    if not c["ping"]:
        return False
    if not c["janela"]:
        return False
    if estado == EM_BATALHA:
        for campo in ("mira", "spawn"):
            if not c[campo]:
                return False
    return True


def portao_com_batalha_no_mapa(estado, c):
    """O DEFEITO (pre-RSTV-13): as guardas de batalha valem em QUALQUER estado, inclusive no mapa.

    E' a isca embutida: o MESMO cenario de mapa que a regra nova LIBERA tem de NAO liberar aqui.
    """
    if not c["gui"]:
        return False
    if not c["roguelike"]:
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
    return True


def campos_do_modelo():
    """As chaves do cenario (fonte unica do nome dos campos)."""
    return list(CENARIO.keys())


# ------------------------------------------------------------------ checagens ---

def _divisao(src):
    """(fora, dentro): o corpo EFETIVO de `GateOk` dividido no ramo de batalha.

    `fora` = o trecho UNIVERSAL (antes do ramo); `dentro` = o ramo de batalha ate' o fim do metodo.
    FALHA ALTO se o ramo de batalha nao existe (sem ele nao ha como separar mapa de batalha).
    """
    gate = _gate(src)
    i = gate.find(RAMO_DE_BATALHA)
    arc.exigir(i >= 0,
               "o `GateOk` NAO tem o ramo `%s` — sem ele nao da' para separar as guardas de mapa e "
               "de batalha" % RAMO_DE_BATALHA)
    return gate[:i], gate[i:]


def falhas_do_gate_por_estado(src):
    """Defeitos do portao por estado no FONTE. Lista vazia = o conserto esta' de pe."""
    falhas = []

    if GATE_OK not in rec.codigo_efetivo(src):
        return ["nao achei %s no fonte" % GATE_OK]

    fora, dentro = _divisao(src)

    # 1) As guardas UNIVERSAIS tem de estar no lado de FORA (valem no mapa tambem).
    for nome, trecho in GATES_UNIVERSAIS:
        if trecho not in fora:
            falhas.append("a guarda universal %r (trecho %r) saiu do lado comum do GateOk — ela "
                          "deixaria de valer no mapa" % (nome, trecho))

    # 2) As guardas DE BATALHA tem de estar no lado de DENTRO (o ramo InBattle) e NAO fora.
    for nome, trecho in GATES_DE_BATALHA:
        if trecho in fora:
            falhas.append("a guarda de BATALHA %r (trecho %r) esta' FORA do ramo `%s` — ela volta a "
                          "segurar o clique no MAPA-MUNDO (o sintoma do dono)"
                          % (nome, trecho, RAMO_DE_BATALHA))
        elif trecho not in dentro:
            falhas.append("a guarda de BATALHA %r (trecho %r) sumiu do GateOk — a seguranca em "
                          "batalha foi afrouxada" % (nome, trecho))

    # 3) As guardas que a RSTV-30 removeu nao podem voltar em lugar NENHUM do portao.
    gate = _gate(src)
    for nome, trecho in GATES_REMOVIDOS:
        if trecho in gate:
            falhas.append("a guarda %r (%r) VOLTOU ao GateOk — era ela que fazia o botao piscar "
                          "quando qualquer personagem agia (RSTV-30)" % (nome, trecho))

    return falhas


# ------------------------------------------------------------ plantio do defeito ---

_ANCORA_RAMO = "                if (gui.CurrentGuiState == GUIState.InBattle)\n                {\n"

# O defeito ANTIGO: a guarda de batalha (`Root.SpawnPlacementActive`) valendo em QUALQUER estado,
# inclusive passeando no mapa. Reinjetada FORA do ramo de batalha.
_DEFEITO_SPAWN_FORA = (
    "                if (root.SpawnPlacementActive)\n"
    "                {\n"
    "                    motivo = \"posicionamento inicial em andamento (Root.SpawnPlacementActive)\";\n"
    "                    return false;\n"
    "                }\n"
    "\n"
) + _ANCORA_RAMO


def fonte_com_batalha_no_mapa(src=None):
    """O MESMO fonte com a guarda de batalha reinjetada FORA do ramo `InBattle` (o defeito).

    Nao mexe em arquivo nenhum: devolve o texto. E' a isca que prova que a checagem pega a guarda de
    batalha valendo no mapa.
    """
    texto = fonte() if src is None else src
    if _ANCORA_RAMO not in texto:
        return texto
    return texto.replace(_ANCORA_RAMO, _DEFEITO_SPAWN_FORA, 1)
