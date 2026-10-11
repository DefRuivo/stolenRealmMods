#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rstv27_valor.py - RSTV-27 pelo VALOR: o RODAPE da tooltip de skill ativa
(mana / cooldown / alcance) tem de mostrar os numeros DERIVADOS DO ALVO DO MODAL, nunca a
base do overload sem personagem.

O DEFEITO (medido, nao declarado)
---------------------------------
`Tooltip.ShowSkillTooltip(SkillInfo, Character, ...)` monta o rodape com um local PROPRIO
(`tooltipCharacter = TooltipCharacter`, get-only = `GameLogic.instance.CurrentlySelectedCharacter`,
null na Party Select) e le' o rodape dele: `GetManaCost(tooltipCharacter)`,
`GetActionCooldown(tooltipCharacter)`, `GetSimpleRange(tooltipCharacter, Targets[0])`. O argumento
que a RSTV-26 passa alcanca o CORPO e nao esse trecho.

Os DOIS caminhos do motor divergem em NUMERO (decompilado do `ActionInfo`,
lib/Assembly-CSharp.dll) - e a divergencia e' o que este teste prende:

  * mana      `GetManaCost(Character)` aplica `ManaCostMod`, `ManaCostMod<SkillType>` e a escala por
              nivel, e devolve `Ceil`; `GetManaCost()` e' `Floor(manaCostBase * ratio)` - so' a base;
  * cooldown  `GetActionCooldown(Character)` avalia o `Cooldown` com `Source = character` e soma
              `CooldownMod` (+`CooldownMod<SkillType>`), com piso 1; `GetActionCooldown()` avalia com
              parametros default e nao soma nada;
  * alcance   `GetSimpleRange(Character, TargetInfo)` soma `RangeAdderMelee`/`RangeAdderRanged` e
              aplica o teto de cego; `GetSimpleRange(TargetInfo)` devolve `SimpleRange` cru.

OS NUMEROS ESPERADOS vem de `tools/testes/fixtures/rstv27-rodape-valor.esperado.json`, GERADO pelo
oraculo C# `tools/testes/fixtures/geradores/oraculo_rstv27` (o caminho de conta do motor transcrito do
decompilado) a partir do CENARIO versionado `.../rstv27-rodape-valor.entrada.json`. Nada e' somado a mao:
o Python NAO recalcula mana/cooldown/alcance - ele so' escolhe QUAL dos dois caminhos o rodape usa (que
e' exatamente o erro do defeito) e compara o NUMERO.

O QUE ESTE MODULO MODELiza
--------------------------
  * `armado_do_fonte(src_tab)`   - o hover do RSTV arma o alvo do MODAL (`ReadOnlySession.Target`) em
                                   volta da montagem da tooltip? (fonte VIVA do mod, nunca copia)
  * `gancho_do_fonte(src_patches)` - o postfix do getter PREENCHE o null (com o valor do jogo vencendo e
                                   o fallback)? Devolve as flags do corpo do `Postfix`, uma por regra.
  * `personagem_do_rodape(...)`  - transcricao do gancho: devolve QUEM o rodape consulta.
  * `rodape(...)`                - transcricao do TERNARIO do rodape: `tooltipCharacter == null ?
                                   <sem personagem> : <com personagem>`, campo a campo.

Limite declarado: nao executa o C# do mod nem o do jogo (pediria um harness do Unity). A ligacao com o
motor e' a transcricao citada (oraculo C#) + o decompilado + o FONTE VIVO lido aqui. O numero REAL na
tela e' o gate do DoD, nao deste teste.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import regras_rstv27 as reg

# Os campos do rodape presos por este teste (a ordem e' a do decompilado: range, blast, mana, cooldown).
CAMPOS = ("mana", "cooldown", "alcance")

# As sub-strings EXATAS do conserto, lidas da fonte viva (se um nome mudar, a checagem REPROVA).
CLASSE_GANCHO = "TooltipCharacterRodapePatch"
VAR_ESTADO = "_alvoDoModal"


# --------------------------------------------------------------- fonte viva ---

def fonte_hover():
    return reg.fonte(reg.caminho_tab())


def fonte_gancho():
    return reg.fonte(reg.caminho_patches())


# --------------------------------------------------- flags do conserto (fonte) ---

def armado_do_fonte(src_tab):
    """True se o hover ARMA o alvo do MODAL em volta da montagem da tooltip.

    Exige as duas coisas juntas: a chamada `TooltipCharacterRodapePatch.ComAlvo(<alvo>)` E o `<alvo>` ser
    o MESMO personagem passado como argumento ao `ShowSkillTooltip` (armar outro nao adianta).
    """
    corpo = reg.corpo_do_hover(src_tab)
    m = re.search(r"TooltipCharacterRodapePatch\.ComAlvo\(\s*(\w+)\s*\)", corpo)
    if not m:
        return False
    armado = m.group(1)
    m2 = re.search(r"ShowSkillTooltip\(\s*Item\.SkillInfo\s*,\s*(\w+)\s*,", corpo)
    return bool(m2) and m2.group(1) == armado


def gancho_do_fonte(src_patches):
    """As flags do POSTFIX do getter, uma por regra do conserto (lidas do corpo do `Postfix`).

    * `valor_do_jogo_vence` - `if (__result != null) return;` (o gancho so' PREENCHE um null);
    * `le_o_alvo`           - `<var> = _alvoDoModal;` (o gancho le o alvo armado);
    * `fallback`            - `if (<var> == null) return;` (sem alvo do modal nada muda);
    * `preenche`            - `__result = <var>;` (o preenchimento em si);
    * `fail_safe`           - try/catch no corpo.
    """
    flags = {"valor_do_jogo_vence": False, "le_o_alvo": False, "fallback": False,
             "preenche": False, "fail_safe": False, "var": None}
    try:
        corpo = reg.corpo_do_postfix(src_patches)
    except arc.Falhou:
        return flags
    if not corpo:
        return flags
    flags["valor_do_jogo_vence"] = bool(
        re.search(r"if\s*\(\s*__result\s*!=\s*null\s*\)\s*\{?\s*return\s*;", corpo))
    m = re.search(r"(\w+)\s*=\s*" + re.escape(VAR_ESTADO) + r"\s*;", corpo)
    if m:
        flags["le_o_alvo"] = True
        flags["var"] = m.group(1)
    flags["preenche"] = bool(re.search(r"__result\s*=\s*\w+\s*;", corpo))
    if flags["var"]:
        flags["fallback"] = bool(re.search(
            r"if\s*\(\s*" + re.escape(flags["var"]) + r"\s*==\s*null\s*\)\s*\{?\s*return\s*;", corpo))
    flags["fail_safe"] = bool(re.search(r"\btry\b", corpo) and re.search(r"\bcatch\b", corpo))
    return flags


# ------------------------------------------------------- modelos puros (a SAIDA) ---

def personagem_do_rodape(jogo, alvo_do_modal, gancho):
    """QUEM o rodape consulta depois do postfix - transcricao do corpo do gancho.

    `jogo`  = o que o getter do JOGO devolveu (`TooltipCharacter`; null na Party Select).
    `alvo_do_modal` = o que `_alvoDoModal` vale NESTA montagem: o alvo armado pelo hover
    (`ReadOnlySession.Target`) se o hover armou, senao None.
    `gancho` = as flags do postfix (`gancho_do_fonte`).

    O gancho e' um postfix do GETTER: ele roda em TODA leitura, inclusive fora da nossa tooltip. A
    transcricao segue o corpo de `Patches.cs`, linha a linha:

        if (__result != null) return;      -> o valor do JOGO vence (inventario intacto)
        Character alvo = _alvoDoModal;     -> le' o alvo armado
        if (alvo == null) return;          -> FALLBACK (sem alvo, nada muda)
        __result = alvo;                   -> PREENCHE o null
    """
    resultado = jogo
    if resultado is not None and gancho["valor_do_jogo_vence"]:
        return resultado
    alvo = alvo_do_modal if gancho["le_o_alvo"] else None
    if alvo is None:
        if gancho["fallback"]:
            return resultado
        # Sem o FALLBACK o gancho escreveria `__result = alvo;` (= null) por CIMA do valor do jogo:
        # fora da nossa tooltip o rodape perderia o personagem que o motor ja' tinha resolvido.
        return None if gancho["preenche"] else resultado
    if not gancho["preenche"]:
        return resultado
    return alvo


def rodape(tooltip_character, sem_personagem, por_personagem):
    """A MONTAGEM do rodape - transcricao do ternario do `Tooltip.ShowSkillTooltip`, campo a campo.

    No motor cada campo e' `tooltipCharacter == null ? <overload SEM personagem> : <overload COM
    personagem>`. Aqui os dois lados vem do ESPERADO (oraculo C#) e a funcao escolhe o lado - que e'
    exatamente o que o defeito erra.
    """
    def campo(nome):
        if tooltip_character is None:
            return sem_personagem[nome]
        return por_personagem[tooltip_character][nome]

    return dict((nome, campo(nome)) for nome in CAMPOS)
