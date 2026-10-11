#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rstv27.py - RSTV-27: o RODAPE da tooltip (mana/cooldown/alcance/duracao) lia o
`TooltipCharacter`, que e' NULL na tela Party Select.

O DEFEITO (achado da verificacao do RSTV-26, 05/10)
---------------------------------------------------
O conserto do RSTV-26 passa o personagem do MODAL como ARGUMENTO do `ShowSkillTooltip`, e isso resolve
o CORPO da tooltip (o '*N' do dano e o '[N]' das expressoes). O RODAPE nao usa esse argumento:

  * `Tooltip.ShowSkillTooltip(SkillInfo, Character, bool, bool, bool)` monta um local PROPRIO,
    `tooltipCharacter = TooltipCharacter` (DLL real do jogo, `ilspycmd -il`: IL_0c46), e le' TODO o
    rodape dele — `GetManaCost`, `GetActionCooldown`, `GetSimpleRange`, `GetSimpleBlastRange` e a
    duracao (`Game.Eval` de `Duration`/`GroundDuration`);
  * `Tooltip.TooltipCharacter` e' propriedade GET-ONLY = `GameLogic.CurrentlySelectedCharacter`
    (`get_TooltipCharacter`, code size 35 na DLL) — NULL na tela Party Select, onde vive o modal
    "Remove Skill Trees". E' a MESMA causa do '*0' da RSTV-26, num caminho que o argumento nao alcanca.

O rodape com personagem null cai nos overloads SEM personagem — conferido no decompilado da DLL
(`ActionInfo`), os dois caminhos DIVERGEM:

  * mana: `GetManaCost(Character)` aplica `ManaCostMod` + `ManaCostMod<SkillType>` + a escala por nivel
    (`manaScalePerLevelPercentage`); `GetManaCost()` = `manaCostBase x ManaCostRatio`, so' a base
    -> diverge em QUALQUER personagem com modificador ou nivel > 1;
  * cooldown: `GetActionCooldown(Character)` avalia a expressao `Cooldown` com `Source = character` e
    soma `CooldownMod`; `GetActionCooldown()` avalia com `default(GameFunctionParameters)`
    -> diverge em cooldown por expressao ou com modificador;
  * alcance: `GetSimpleRange(Character, TargetInfo)` soma `RangeAdderMelee`/`RangeAdderRanged` e
    aplica o teto de cego; `GetSimpleRange(TargetInfo)` devolve `SimpleRange` cru
    -> diverge em personagem com alcance somado.

AS REGRAS (viram checagem)
--------------------------
1. o hover do RSTV (`RstvSkillHover.OnPointerEnter`, SkillTreesTab.cs) ARMA o alvo do MODAL
   (`TooltipCharacterRodapePatch.ComAlvo(alvo)`, com `alvo = ReadOnlySession.Target`) SO' em volta da
   montagem da tooltip e DESARMA no `finally` (`SemAlvo()`): o mesmo alvo que a RSTV-26 passa como
   argumento vai TAMBEM ao rodape;
2. o gancho (Patches.cs) e' um POSTFIX de `Tooltip.get_TooltipCharacter` que so' PREENCHE o null, com
   as tres regras, nesta ORDEM: o valor do JOGO vence (`if (__result != null) return;`), sem alvo
   armado nao mexe (FALLBACK = comportamento do jogo) e o preenchimento e' `__result = alvo;`;
3. o metodo do gancho e' FAIL-SAFE (try/catch) e os setters `ComAlvo`/`SemAlvo` existem no gancho.

A SAIDA QUE ESTAS REGRAS PRENDEM
--------------------------------
`personagem_do_rodape` + `valor_do_rodape` NAO checam "existe a chamada": eles devolvem o VALOR que o
rodape mostra. O primeiro decide QUEM o motor consulta (transcricao do gancho: o valor do jogo vence,
null + alvo armado -> alvo do modal, sem alvo -> null) e o segundo devolve os numeros DAQUELE
personagem (`CASO` separa o valor de BASE do valor do personagem). Com o conserto, na Party Select
(singleton null) o rodape vale o alvo do modal; com o defeito, vale a BASE e a checagem REPROVA.
`CASO` e' um CASO sintetico (a procedencia dos numeros e' a MECANICA lida da DLL: os dois caminhos
divergem); os numeros de JOGO saem em jogo, no DoD.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import recorte as rec

# Assinaturas EXATAS lidas do fonte. Se um nome mudar, a checagem REPROVA dizendo qual sumiu.
ASSINATURA_HOVER = "public void OnPointerEnter(PointerEventData eventData)"
ASSINATURA_POSTFIX = "private static void Postfix(ref Character __result)"
CLASSE_GANCHO = "internal static class TooltipCharacterRodapePatch"

# As ancoras do conserto (o texto que o plantio do defeito tira).
ANCORA_ARMADO = "TooltipCharacterRodapePatch.ComAlvo(alvo);"
ANCORA_PREENCHIMENTO = "__result = alvo;"
FILTRO_TOOLTIP = "get_TooltipCharacter"

# O CASO do rodape (sintetico - ver o cabecalho): o que o motor devolve SEM personagem (`base`) e o
# que ele devolve PARA CADA personagem (modificadores + escala de nivel).
CAMPOS = ("mana", "cooldown", "alcance", "duracao")
CASO = {
    "base": {"mana": 4, "cooldown": 3, "alcance": 2, "duracao": 2},
    "Raven": {"mana": 2, "cooldown": 5, "alcance": 3, "duracao": 3},
    "Outro": {"mana": 5, "cooldown": 1, "alcance": 1, "duracao": 4},
}


# ------------------------------------------------------------------ caminhos ---

def _dir_mod():
    return os.path.join(arc.raiz_do_repo(), "RoguelikeSkillTreeVisualizer")


def caminho_tab():
    return os.path.join(_dir_mod(), "SkillTreesTab.cs")


def caminho_patches():
    return os.path.join(_dir_mod(), "Patches.cs")


def fonte(caminho=None):
    caminho = caminho_tab() if caminho is None else caminho
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def _efetivo(src):
    return rec.codigo_efetivo(src)


def corpo_do_hover(src):
    """O corpo INTEIRO do `RstvSkillHover.OnPointerEnter`, sem comentario."""
    return rec.corpo_do_metodo(_efetivo(src), ASSINATURA_HOVER)


def corpo_do_postfix(src_patches):
    """O corpo INTEIRO do `Postfix` do gancho, sem comentario.

    Isola o metodo de PATCH (o `Postfix` do `TooltipCharacterRodapePatch`) do resto de `Patches.cs`,
    que tem 15 ganchos: um `__result` de outro gancho nao pode entrar nesta conta.
    """
    efetivo = _efetivo(src_patches)
    i = efetivo.find(CLASSE_GANCHO)
    arc.exigir(i >= 0, "nao achei a classe `%s` em Patches.cs" % CLASSE_GANCHO)
    return rec.corpo_do_metodo(efetivo[i:], ASSINATURA_POSTFIX)


def bloco_do_gancho(src_patches):
    """O bloco `{ ... }` da classe do gancho (por CASAMENTO DE CHAVES) - sem comentario.

    Isola o que o gancho declara (estado, setters, o `Postfix`) do resto de `Patches.cs` (15
    ganchos): um `__result` ou um `if (x == null)` de outro gancho nao pode entrar nesta conta.
    O atributo `[HarmonyPatch(...)]` fica FORA do bloco (a ancora e' a declaracao da classe), por
    isso quem o confere le a vizinhanca da ancora.
    """
    efetivo = _efetivo(src_patches)
    i = efetivo.find(CLASSE_GANCHO)
    arc.exigir(i >= 0, "nao achei a classe `%s` em Patches.cs" % CLASSE_GANCHO)
    return rec.texto_da_faixa(efetivo, rec.faixa_bloco_apos(efetivo, i))



# ------------------------------------------------------- modelos puros (a SAIDA) ---

def personagem_do_rodape(resultado_do_jogo, alvo_do_modal):
    """QUEM o rodape consulta depois do postfix.

    Transcricao do gancho: o valor do JOGO vence (nunca e' sobrescrito); com ele null, o alvo do modal
    armado PREENCHE; sem alvo armado nada muda (o motor cai no overload SEM personagem).
    """
    if resultado_do_jogo is not None:
        return resultado_do_jogo
    return alvo_do_modal


def valor_do_rodape(personagem, caso=None):
    """Os numeros do rodape: os DO personagem; sem personagem, o de BASE (o defeito)."""
    caso = CASO if caso is None else caso
    if personagem is None:
        return dict(caso["base"])
    return dict(caso[personagem])


# ------------------------------------------------------------------- checagens ---

def falhas_do_armado(src_tab):
    """A LISTA de falhas do ARMADO do alvo no hover. Vazia = correto (RSTV-27)."""
    corpo = corpo_do_hover(src_tab)
    falhas = []

    m = re.search(r"TooltipCharacterRodapePatch\.ComAlvo\(\s*(\w+)\s*\)", corpo)
    if not m:
        falhas.append("o hover NAO arma o alvo do modal (`TooltipCharacterRodapePatch.ComAlvo(<alvo>)`): "
                      "o rodape continua lendo o `TooltipCharacter` null na Party Select")
        return falhas

    armado = m.group(1)

    # O alvo armado e' o MESMO passado como argumento ao ShowSkillTooltip (o do RSTV-26).
    m2 = re.search(r"ShowSkillTooltip\(\s*Item\.SkillInfo\s*,\s*(\w+)\s*,\s*"
                   r"showCanLevelDetail:\s*false\s*\)", corpo)
    if not m2:
        falhas.append("nao ha `ShowSkillTooltip(Item.SkillInfo, <alvo>, showCanLevelDetail: false)` no "
                      "hover: sem essa chamada nao ha o que armar")
    elif m2.group(1) != armado:
        falhas.append("o alvo armado (`%s`) nao e' o mesmo passado ao ShowSkillTooltip (`%s`): o rodape "
                      "receberia OUTRO personagem" % (armado, m2.group(1)))

    # O estado tem de cercar a NOSSA chamada: `ComAlvo(...); try { ShowSkillTooltip(...); } finally { SemAlvo(); }`.
    if not re.search(r"TooltipCharacterRodapePatch\.ComAlvo\(\s*\w+\s*\)\s*;\s*try\s*\{[^{}]*"
                     r"ShowSkillTooltip\([^;]*\)\s*;\s*\}\s*finally\s*\{\s*"
                     r"TooltipCharacterRodapePatch\.SemAlvo\(\s*\)\s*;", corpo):
        falhas.append("o alvo nao fica armado SO' em volta da montagem da tooltip "
                      "(`ComAlvo` -> `try { ShowSkillTooltip(...) }` -> `finally { SemAlvo() }`): o "
                      "estado vazaria para as outras tooltips do jogo")

    return falhas


def falhas_do_gancho(src_patches):
    """A LISTA de falhas do GANCHO (postfix do getter). Vazia = correto (RSTV-27)."""
    efetivo = _efetivo(src_patches)
    falhas = []

    # (a) O atributo: postfix do getter `Tooltip.get_TooltipCharacter` — a propriedade e' get-only, e o
    # filtro por NOME do metodo do jogo e' a assinatura (nunca por indice `__N`).
    i = efetivo.find(FILTRO_TOOLTIP)
    if i < 0:
        falhas.append("Patches.cs nao tem gancho no `%s`: o rodape nao tem como receber o alvo do modal "
                      "(a propriedade e' get-only, nao ha argumento para passar)" % FILTRO_TOOLTIP)
    else:
        j = efetivo.rfind("[HarmonyPatch", 0, i)
        k = efetivo.find(CLASSE_GANCHO, i)
        trecho = efetivo[j:k + len(CLASSE_GANCHO)] if (j >= 0 and k >= 0) else ""
        if not re.search(r"\[HarmonyPatch\(\s*typeof\(Tooltip\)\s*,\s*\"%s\"\s*\)\]" % FILTRO_TOOLTIP,
                         trecho):
            falhas.append("o gancho nao declara `[HarmonyPatch(typeof(Tooltip), \"%s\")]` (assinatura "
                          "por TIPO + nome do metodo, nunca por indice)" % FILTRO_TOOLTIP)
        if not re.search(r"\]\s*" + re.escape(CLASSE_GANCHO), trecho):
            falhas.append("o atributo do getter nao esta declarado na classe `%s` (o gancho do rodape "
                          "tem de ser ESTA classe)" % CLASSE_GANCHO)

    corpo = corpo_do_postfix(src_patches)
    bloco = bloco_do_gancho(src_patches)

    # (b) O estado: um campo unico, armado e desarmado pelos setters (o hover usa os dois).
    if len(re.findall(r"_alvoDoModal", bloco)) < 3:
        falhas.append("o estado `_alvoDoModal` nao aparece no gancho como campo + leitura + zeragem "
                      "(e' ele que carrega o alvo do modal)")
    if not re.search(r"internal static void ComAlvo\(\s*Character\s+\w+\s*\)\s*\{[^{}]*"
                     r"_alvoDoModal\s*=\s*\w+\s*;", bloco):
        falhas.append("falta o setter `ComAlvo(Character)` gravando `_alvoDoModal` (e' ele que o hover "
                      "chama para armar o alvo do modal)")
    if not re.search(r"internal static void SemAlvo\(\s*\)\s*\{[^{}]*_alvoDoModal\s*=\s*null\s*;",
                     bloco):
        falhas.append("falta o setter `SemAlvo()` zerando `_alvoDoModal` (o DESARME/FALLBACK)")

    # (c) O valor do JOGO vence: sai do gancho sem tocar em `__result`.
    m_jogo = re.search(r"if\s*\(\s*__result\s*!=\s*null\s*\)\s*\{?\s*return\s*;", corpo)
    if not m_jogo:
        falhas.append("o gancho NAO devolve o valor do jogo (`if (__result != null) return;`): ele "
                      "sobrescreveria um personagem que o jogo ja' resolveu (regressao no inventario)")

    # (d) O FALLBACK: sem alvo armado, sai sem mexer (comportamento antigo).
    m_alvo = re.search(r"(\w+)\s*=\s*_alvoDoModal\s*;", corpo)
    if not m_alvo:
        falhas.append("o gancho nao LE o alvo armado (`<var> = _alvoDoModal;`)")
    else:
        var = m_alvo.group(1)
        if not re.search(r"if\s*\(\s*" + re.escape(var) + r"\s*==\s*null\s*\)\s*\{?\s*return\s*;", corpo):
            falhas.append("falta o FALLBACK `if (%s == null) return;` (sem alvo do modal o jogo tem de "
                          "seguir como sempre foi)" % var)
        # (e) O PREENCHIMENTO, com a var lida do estado.
        if not re.search(r"__result\s*=\s*" + re.escape(var) + r"\s*;", corpo):
            falhas.append("o gancho nao PREENCHE (`__result = %s;`): o rodape continuaria com o null" % var)
        # (f) A ORDEM: o valor do jogo (c) -> a leitura do alvo (d) -> o preenchimento (e).
        if m_jogo and re.search(r"__result\s*=\s*" + re.escape(var) + r"\s*;", corpo):
            if not (corpo.find("__result != null") < corpo.find("_alvoDoModal")
                    < corpo.find("__result = " + var)):
                falhas.append("a ORDEM do gancho esta errada: o valor do jogo tem de ser conferido ANTES "
                              "do alvo e o preenchimento DEPOIS dele")

    # (g) FAIL-SAFE: uma excecao aqui nao pode derrubar o hover.
    if not (re.search(r"\btry\b", corpo) and re.search(r"\bcatch\b", corpo)):
        falhas.append("o `Postfix` nao tem try/catch (fail-safe): uma excecao no gancho derrubaria o hover")

    return falhas


# --------------------------------------------------------- plantio do defeito ---

def _sem_trecho(texto, trecho):
    """O MESMO texto com UM trecho a menos — o plantio do defeito (nao acha -> devolve igual)."""
    return texto.replace(trecho, "", 1)


def hover_sem_armado(src=None):
    """O hover SEM a chamada que arma o alvo do modal (o defeito: o rodape volta a ler o null)."""
    texto = fonte(caminho_tab()) if src is None else src
    return _sem_trecho(texto, ANCORA_ARMADO)


def gancho_sem_preenchimento(src=None):
    """O gancho SEM `__result = alvo;` (existe, mas nunca preenche: o defeito silencioso)."""
    texto = fonte(caminho_patches()) if src is None else src
    return _sem_trecho(texto, ANCORA_PREENCHIMENTO)


def gancho_sobrescreve(src=None):
    """O gancho SEM a guarda do valor do jogo (sobrescreveria o que o jogo ja' resolveu)."""
    texto = fonte(caminho_patches()) if src is None else src
    return re.sub(r"if\s*\(\s*__result\s*!=\s*null\s*\)\s*\{[^{}]*\}\s*", "", texto, count=1)


def gancho_sem_fallback(src=None):
    """O gancho SEM `if (alvo == null) return;` (sem alvo do modal ele preencheria null)."""
    texto = fonte(caminho_patches()) if src is None else src
    novo = re.sub(r"if\s*\(\s*alvo\s*==\s*null\s*\)\s*\{[^{}]*?return\s*;\s*\}\s*",
                  "", texto, count=1)
    if novo == texto:
        novo = re.sub(r"if\s*\(\s*alvo\s*==\s*null\s*\)\s*\{\s*return;\s*\}", "", texto, count=1)
    return novo
