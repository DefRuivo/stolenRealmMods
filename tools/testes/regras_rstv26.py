#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rstv26.py - RSTV-26: o hover dos nos na janela read-only mostrava '*0' LITERAL.

O DEFEITO (relato do dono, 04/10)
---------------------------------
Na janela read-only (botao 'Skills' do modal 'Remove Skill Trees'), TODAS as skills mostravam o
dano como '*0' literal no hover. Causa raiz no decompilado (`Tooltip`):

  * o hover chama `gui.tooltip.ShowSkillTooltip(Item)` (SkillTreeItem);
  * esse overload delega para `ShowSkillTooltip(skillInfo, TooltipCharacter, showCanLevelDetail: true)`;
  * `Tooltip.TooltipCharacter` = `GameLogic.CurrentlySelectedCharacter`, que e' NULL na tela Party
    Select (onde vive o modal);
  * `ShowSkillTooltip(SkillInfo, Character, ...)` so resolve o '*N' (GetDamageString) e o '[N]'
    (ApplyDescriptionExpressions) DENTRO do bloco `if (character != null)`.

Com `character` null o '*0' (e o '[N]'/'@atributo@') saem CRUS.

O QUE A RSTV-26 FAZ (as regras viram checagem)
----------------------------------------------
1. O hover LE o personagem do MODAL (`ReadOnlySession.Target`, o mesmo do AcceptSkillChanges e do
   `Initialize` da janela) e o passa EXPLICITO ao motor:
   `ShowSkillTooltip(Item.SkillInfo, <alvo>, showCanLevelDetail: false)`.
2. O alvo passa o guard de null: `if (<alvo> != null)` -> chama com o personagem; `else` cai no
   comportamento ANTIGO (`ShowSkillTooltip(Item)`), sem crash.
3. `showCanLevelDetail: false` mantem o read-only de verdade: o bloco 'Skill Point Cost'/'Select To
   Learn'/'Learned' so roda com ele (E com a `SkillTreeManager` viva).

COMO O ESPERADO E OBTIDO
------------------------
Fonte lido AO VIVO (`RoguelikeSkillTreeVisualizer/SkillTreesTab.cs`), recorte ESTRUTURAL por chaves
(`recorte.corpo_do_metodo`) sobre o texto SEM comentario (`recorte.codigo_efetivo`) — a citacao do
overload num comentario nao e' codigo. Os MODELOS PUROS transcrevem a decisao do motor
(`personagem_do_motor`/`placeholders_resolvidos`) e do bloco de custo (`mostra_custo`). O plantio
`fonte_com_defeito` devolve o MESMO fonte com o hover ANTIGO — a isca prova que a checagem reprova.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import recorte as rec

# Assinatura EXATA lida do fonte. Se um nome mudar, a checagem REPROVA dizendo qual sumiu.
ASSINATURA_HOVER = "public void OnPointerEnter(PointerEventData eventData)"

_ANCORA_INICIO = "Character alvo = ReadOnlySession.Target;"
_ANCORA_FALLBACK = "gui.tooltip.ShowSkillTooltip(Item);"
_DEFEITO = "gui.tooltip.ShowSkillTooltip(Item);"


# ------------------------------------------------------------------ caminhos ---

def _dir_mod():
    return os.path.join(arc.raiz_do_repo(), "RoguelikeSkillTreeVisualizer")


def caminho_tab():
    return os.path.join(_dir_mod(), "SkillTreesTab.cs")


def fonte(caminho=None):
    caminho = caminho_tab() if caminho is None else caminho
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def _efetivo(src):
    return rec.codigo_efetivo(src)


def corpo_do_hover(src):
    """O corpo INTEIRO do `RstvSkillHover.OnPointerEnter`, sem comentario."""
    return rec.corpo_do_metodo(_efetivo(src), ASSINATURA_HOVER)


# ------------------------------------------------------- modelos puros (decisao) ---

def personagem_do_motor(passou_alvo, tooltip_character):
    """O `character` que o `ShowSkillTooltip` recebe: o EXPLICITO, se houver; senao o TooltipCharacter.

    Transcreve o motor: o overload de 1 argumento passa `TooltipCharacter`; o de 3 passa o alvo
    explicito do chamador.
    """
    return passou_alvo if passou_alvo is not None else tooltip_character


def placeholders_resolvidos(passou_alvo, tooltip_character):
    """True se o '*N'/'[N]' sao resolvidos — o motor exige `character != null` (Tooltip)."""
    return personagem_do_motor(passou_alvo, tooltip_character) is not None


def mostra_custo(show_can_level_detail, skill_tree_ativa):
    """O bloco 'Skill Point Cost'/'Select To Learn' so roda com `showCanLevelDetail` E a arvore viva."""
    return bool(show_can_level_detail) and bool(skill_tree_ativa)


# ------------------------------------------------------------------- checagens ---

def falhas_do_hover(src):
    """A LISTA de falhas do hover. Vazia = correto (RSTV-26)."""
    corpo = corpo_do_hover(src)
    falhas = []

    # 1) O hover tem de LER o personagem do MODAL (ReadOnlySession.Target).
    if not re.search(r"\bReadOnlySession\.Target\b", corpo):
        falhas.append("o hover nao le `ReadOnlySession.Target` (o personagem do modal): o '*0' volta")

    # 2) A chamada com o alvo explicito: ShowSkillTooltip(Item.SkillInfo, <var>, showCanLevelDetail: false).
    m = re.search(r"ShowSkillTooltip\(\s*Item\.SkillInfo\s*,\s*(\w+)\s*,\s*"
                  r"showCanLevelDetail:\s*false\s*\)", corpo)
    if not m:
        falhas.append("nao ha `ShowSkillTooltip(Item.SkillInfo, <alvo>, showCanLevelDetail: false)`: "
                      "o '*0'/'[N]' nao seriam resolvidos contra o personagem do modal "
                      "(ou o read-only mostraria 'Skill Point Cost')")
    else:
        alvo = m.group(1)
        # Amarra a DECISAO: a variavel passada ao motor tem de vir de ReadOnlySession.Target.
        if not re.search(r"\b" + re.escape(alvo) + r"\s*=\s*ReadOnlySession\.Target\b", corpo):
            falhas.append("a variavel `%s` passada ao ShowSkillTooltip nao vem de "
                          "`ReadOnlySession.Target`" % alvo)
        # O guard de null: sem ele um alvo null iria para a chamada de 3 argumentos.
        if not re.search(r"if\s*\(\s*" + re.escape(alvo) + r"\s*!=\s*null\s*\)", corpo):
            falhas.append("falta o guard `if (%s != null)` antes de passar o alvo ao motor" % alvo)

    # 3) O FALLBACK (alvo null -> comportamento antigo) tem de existir: `ShowSkillTooltip(Item)`.
    if not re.search(r"else\s*\{?\s*" + re.escape("gui.tooltip.ShowSkillTooltip(Item)"), corpo):
        falhas.append("falta o fallback `ShowSkillTooltip(Item)` no `else` (alvo null -> sem crash)")

    return falhas


def fonte_com_defeito(src=None):
    """O MESMO fonte com o hover ANTIGO (o overload de 1 argumento) — o DEFEITO do RSTV-26."""
    texto = fonte() if src is None else src
    i = texto.find(_ANCORA_INICIO)
    j = texto.find(_ANCORA_FALLBACK, i + 1 if i >= 0 else 0)
    if i < 0 or j < 0:
        return texto
    fim = texto.find("}", j)
    if fim < 0:
        return texto
    return texto[:i] + _DEFEITO + texto[fim + 1:]
