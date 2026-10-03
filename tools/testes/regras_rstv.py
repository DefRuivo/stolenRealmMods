#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rstv.py - RSTV-8: o PORTAO do botao da Skill Tree da RUN, lido do FONTE vivo.

POR QUE ESTA BIBLIOTECA EXISTE (o defeito que ela trava)
--------------------------------------------------------
O dono NUNCA viu o botao "Skills" no HUD da run. O log da sessao mostra o botao injetado
("RSTV-5: botao 'Skills' injetado no HUD ... a direita do Ping Button") e, logo depois, escondido
com o motivo "RoguelikeManager ativo (level-up/reroll pendente): ele troca o personagem
selecionado sozinho". O dono testou DURANTE o level-up — exatamente quando queria consultar a
arvore.

O `RunTargets.GateOk` (RoguelikeSkillTreeVisualizer/RunTargets.cs) escondia o botao com

    if (RoguelikeManager.IsNotNullAndIsActive) { motivo = "..."; return false; }

mas `IsNotNullAndIsActive` (decompilado l.168661) so diz que o manager foi CARREGADO: o
GameObject dele fica ativo durante a run inteira depois do primeiro level-up (o `LoadReference`
instancia o prefab, l.168005-168014). Quem diz que a JANELA do level-up esta aberta agora e o
filho `SkillSelectWindow.activeSelf` (l.168597; o proprio jogo usa esse criterio em
`GUIManager.Update` l.120492 e no `SkillSelectActive` l.230294).

O QUE ESTAS REGRAS TRAVAM
-------------------------
1. o portao NAO esconde o botao por o manager estar ativo/carregado (o defeito);
2. quando a JANELA do level-up esta aberta, o portao LIBERA o botao:
       if (LevelUpAberto()) { return true; }
   O level-up e um menu MODAL. Os portoes de run (mira, ping, janela de UI, spawn, turno,
   animacao) descrevem a RUN em andamento, que o menu suspendeu; a janela do level-up ainda
   convive com o PostBattleManager em `UIWindowManager.OpenedWindows` (o `OpenWindow` dele e
   l.332398), entao o portao de "janela aberta" bloquearia o proprio level-up se valesse aqui.
3. TODOS os outros portoes continuam no fonte (nenhum foi removido): mira (PlayerState.Action),
   ping (PingModeActive), janela (AnyUIWindowOpen), spawn (SpawnPlacementActive), turno
   (IsPlayerTurnAndReady), acting/moving (AnyActingCharactersInBattle/MovingCharactersInBattle),
   alem dos basicos (GUIManager, Roguelike, GUIState whitelist);
4. o ALVO do level-up sai do PROPRIO RoguelikeManager, nunca do `CurrentlySelectedCharacter`
   que ele troca: `CurrentRoguelikeSkillSelectingCharacter` (l.168726, definido junto com a
   janela em l.168932) e, como fallback, `CharactersWaitingForLevelUp[0].Character`
   (l.168655/168863-168866). O `Resolve` confere `Character.Owned`.

O `modelo_do_portao` (abaixo) e uma TRANSCRICAO PURA do portao — um booleano por campo — para
mostrar o COMPORTAMENTO das duas regras no mesmo cenario: a regra NOVA LIBERA durante o level-up
e a regra ANTIGA (`portao_antigo`, o defeito plantado) NAO libera. E a isca embutida, como em
`regras_bf`: sem ela, o teste passaria por construcao.

COMO O ESPERADO E OBTIDO
------------------------
O fonte e lido AO VIVO de `RoguelikeSkillTreeVisualizer/RunTargets.cs` (nao uma copia: a
expectativa fica amarrada ao que sera compilado). Os CAMPOS do portao sao LIDOS do corpo efetivo
de `GateOk` (sem comentario) e o teste exige que o modelo puro tenha exatamente esses campos.
O plantio do defeito (`fonte_com_o_defeito`) NAO toca em arquivo nenhum: devolve o texto.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import recorte as rec

# Declaracoes exatas lidas do fonte. Se um nome mudar, a checagem REPROVA dizendo qual sumiu.
GATE_OK = "internal static bool GateOk(out string motivo)"
RESOLVE = "internal static Character Resolve(out string motivo)"
LEVEL_UP_ABERTO = "private static bool LevelUpAberto()"
ALVO_LEVEL_UP = "private static Character AlvoDoLevelUp()"

# Campo do modelo puro -> trecho que PROVA o campo no corpo efetivo de `GateOk`.
# Os nomes sao os campos do CENARIO do modelo; `campos_do_modelo()` devolve as chaves.
CAMPOS = (
    ("gui", "GUIManager.instance"),
    ("roguelike", "!Roguelike"),
    ("estado", "StateAllowed"),
    ("levelup", "LevelUpAberto"),
    ("mira", "PlayerState.Action"),
    ("ping", "PingModeActive"),
    ("janela", "AnyUIWindowOpen"),
    ("spawn", "SpawnPlacementActive"),
    ("em_batalha", "GUIState.InBattle"),
    ("turno", "IsPlayerTurnAndReady"),
    ("acting", "AnyActingCharactersInBattle"),
    ("moving", "AnyMovingCharactersInBattle"),
)

# Cenario REAL do level-up: o menu esta aberto, tudo o mais esta no estado normal da run.
# `janela` e True de proposito: a janela do level-up (e o PostBattleManager) estao em
# OpenedWindows — e e justamente por isso que a regra nova curto-circuita ANTES do portao de
# janela. Fora do level-up, `janela=False` continua bloqueando (o teste prova).
CENARIO_LEVELUP = {
    "gui": True,
    "roguelike": True,
    "estado": True,
    "levelup": True,
    "mira": True,
    "ping": True,
    "janela": True,
    "spawn": True,
    "em_batalha": False,
    "turno": True,
    "acting": True,
    "moving": True,
}

# RSTV-13 — os portoes que SO existem numa BATALHA em andamento. `IsPlayerTurnAndReady` fica no
# ultimo valor do combate anterior (l.111904) e `SpawnPlacementActive` so existe no setup da
# batalha (l.112152/l.112165); `mira`/`acting`/`moving` idem. Aplicados ao MAPA-MUNDO eles
# escondem o botao quando o jogador passeia — por isso moram dentro do ramo `InBattle`.
CAMPOS_DE_BATALHA = ("mira", "spawn", "turno", "acting", "moving")


def caminho_do_fonte():
    return os.path.join(arc.raiz_do_repo(), "RoguelikeSkillTreeVisualizer", "RunTargets.cs")


def fonte():
    """O fonte vivo do mod (nao uma copia: a expectativa fica amarrada ao que sera compilado)."""
    with open(caminho_do_fonte(), encoding="utf-8") as fh:
        return fh.read()


def _efetivo(src):
    """O codigo SEM comentario de linha/bloco (a citacao num comentario nao e codigo)."""
    return rec.codigo_efetivo(src)


def _corpo(src, assinatura):
    """Corpo `{...}` de um metodo do fonte EFETIVO (sem comentario), por casamento de chaves."""
    return rec.corpo_do_metodo(_efetivo(src), assinatura)


def campos_do_portao(src):
    """Os campos do portao presentes no corpo efetivo de `GateOk` (nomes de `CAMPOS` ja OK)."""
    gate = _corpo(src, GATE_OK)
    return [nome for nome, trecho in CAMPOS if trecho in gate]


def campos_do_modelo():
    """Os campos que o modelo puro usa (as chaves do cenario). Fonte UNICA do nome dos campos."""
    return list(CENARIO_LEVELUP.keys())


# ------------------------------------------------------------------ modelo puro ---

def portao_novo(c):
    """Transcricao PURA da regra NOVA (RSTV-8 + RSTV-13): cada chave e um portao (`True` = NAO bloqueia).

    Ordem identica a do `GateOk`: basicos -> LEVEL-UP libera -> ping/janela (universais) ->
    mira/spawn/turno/animacao (SO em batalha, RSTV-13).
    """
    if not c["gui"]:
        return False
    if not c["roguelike"]:
        return False
    if not c["estado"]:
        return False
    if c["levelup"]:
        return True
    if not c["ping"]:
        return False
    if not c["janela"]:
        return False
    if c["em_batalha"]:
        # RSTV-13: no MAPA (`em_batalha=False`) estes portoes NAO valem — o botao aparece.
        if not c["mira"]:
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


def portao_antigo(c):
    """Transcricao PURA do DEFEITO (o `IsNotNullAndIsActive` plantado): o manager ativo ESCONDE.

    E a isca: o MESMO cenario de level-up que a regra nova LIBERA tem de NAO liberar aqui.
    """
    if not c["gui"]:
        return False
    if not c["roguelike"]:
        return False
    if not c["estado"]:
        return False
    if c["levelup"]:            # o manager carregado/ativo -> esconder (o defeito)
        return False
    if not c["mira"]:
        return False
    if not c["ping"]:
        return False
    if not c["janela"]:
        return False
    if not c["spawn"]:
        return False
    if c["em_batalha"]:
        if not c["turno"]:
            return False
        if not c["acting"]:
            return False
        if not c["moving"]:
            return False
    return True


# ------------------------------------------------------------------ checagens ---

def _falta(texto, trecho, rotulo):
    return None if trecho in texto else "faltou %s (%r)" % (rotulo, trecho)


def falhas_da_fonte(src):
    """Defeitos do portao encontrados no fonte. Lista vazia = o conserto esta de pe."""
    falhas = []

    # ------------------------------------------------------------ 1) GateOk existe
    gate = _corpo(src, GATE_OK)
    if gate is None:
        return ["nao achei %s no fonte" % GATE_OK]

    # --------------------------------------------------- 2) o defeito NAO voltou
    if "IsNotNullAndIsActive" in gate:
        falhas.append("o portao voltou a esconder por `RoguelikeManager.IsNotNullAndIsActive` "
                      "(o manager CARREGADO nao e o level-up aberto — o defeito do RSTV-8)")

    # ----------------------------------------------------- 3) o level-up LIBERA
    if "if (LevelUpAberto())" not in gate:
        falhas.append("GateOk nao chama `LevelUpAberto()` para liberar durante o level-up")
    if "return true;" not in gate:
        falhas.append("GateOk nao tem o `return true;` do ramo de level-up")

    # ------------------------------------------- 4) os OUTROS portoes continuam
    for nome, trecho in CAMPOS:
        if nome in ("levelup",):
            continue
        if trecho not in gate:
            falhas.append("o portao %r saiu do GateOk (trecho %r)" % (nome, trecho))

    # ----------------------------------- 5) LevelUpAberto le a JANELA (nao o manager)
    aberto = _corpo(src, LEVEL_UP_ABERTO)
    if aberto is None:
        falhas.append("nao achei %s no fonte" % LEVEL_UP_ABERTO)
    else:
        for trecho, rotulo in (("SkillSelectWindow", "o filho SkillSelectWindow"),
                               ("activeSelf", "o activeSelf da janela")):
            falta = _falta(aberto, trecho, rotulo)
            if falta:
                falhas.append("LevelUpAberto nao le %s" % rotulo)

    # ------------------------ 6) o alvo do level-up sai do PROPRIO manager
    alvo = _corpo(src, ALVO_LEVEL_UP)
    if alvo is None:
        falhas.append("nao achei %s no fonte" % ALVO_LEVEL_UP)
    else:
        if "CurrentRoguelikeSkillSelectingCharacter" not in alvo:
            falhas.append("AlvoDoLevelUp nao le `CurrentRoguelikeSkillSelectingCharacter` "
                          "(o campo canonico do personagem sendo nivelado)")
        if "CharactersWaitingForLevelUp" not in alvo:
            falhas.append("AlvoDoLevelUp nao tem o fallback `CharactersWaitingForLevelUp`")

    # ---------------------------------------- 7) Resolve usa o alvo e confere Owned
    resolve = _corpo(src, RESOLVE)
    if resolve is None:
        falhas.append("nao achei %s no fonte" % RESOLVE)
    else:
        if "AlvoDoLevelUp" not in resolve:
            falhas.append("Resolve nao consulta `AlvoDoLevelUp` (o alvo cairia no "
                          "CurrentlySelectedCharacter, que o manager troca)")
        if "Owned" not in resolve:
            falhas.append("Resolve nao confere `Character.Owned`")

    return falhas


# ------------------------------------------------------------ plantio do defeito ---

_ANCORA_LEVELUP = (
    "                if (LevelUpAberto())\n"
    "                {\n"
    "                    return true;\n"
    "                }"
)

_DEFEITO_MANAGER_ATIVO = (
    "                if (RoguelikeManager.IsNotNullAndIsActive)\n"
    "                {\n"
    "                    motivo = \"RoguelikeManager ativo (level-up/reroll pendente): ele troca o "
    "personagem selecionado sozinho\";\n"
    "                    return false;\n"
    "                }"
)


def fonte_com_o_defeito(src=None):
    """O MESMO fonte com o defeito ANTIGO reinjetado: esconder quando o manager esta ativo.

    Nao mexe em arquivo nenhum: devolve o texto. E a isca (`cp_rstv8_levelup_escondido.py`)
    que usa isto para provar que as checagens reprovam de verdade.
    """
    texto = fonte() if src is None else src
    if _ANCORA_LEVELUP not in texto:
        return texto
    return texto.replace(_ANCORA_LEVELUP, _DEFEITO_MANAGER_ATIVO, 1)
