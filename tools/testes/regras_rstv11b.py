#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rstv11b.py - RSTV-11b: o botao DENTRO da janela do level-up e o FIM do re-parent da RSTV-9.

O QUE ESTA BIBLIOTECA TRAVA (lida do FONTE vivo, nunca de copia)
----------------------------------------------------------------
A RSTV-9 resolvia o level-up RE-PARENTEANDO o clone do HUD para dentro do `SkillSelectWindow`. O
prefab (RSTV-10) mostrou o furo: o `SkillSelectWindow` [680553] e TELA CHEIA (anchor 0,0..1,1) —
o "canto superior direito" do re-parent caia no canto da TELA, nao no do painel. O painel visivel e
o filho `Content` [680573] (~293x536 px, `VerticalLayoutGroup` + `ContentSizeFitter`). A proposta C
(vencedora) cria um botao PROPRIO da janela, filho DIRETO do `SkillSelectWindow` — FORA do `Content`,
para nao refluir o painel.

1. `LevelUpWindowButton.Ensure(RoguelikeManager rok)` e IDEMPOTENTE POR JANELA: o postfix de
   `OpenSkillSelectWindow` roda de novo a cada personagem da fila de level-up, sobre o MESMO
   `SkillSelectWindow`. A 2a chamada e NO-OP (`_janela == janela && _button != null`).
2. O clone nasce como filho DIRETO de `janela.transform` (o `SkillSelectWindow`) e NAO de `contentRt`.
   O `Content` e usado so para MEDIR o canto (o alvo da ancora e o painel, nao a tela). Clonar para
   dentro do `Content` reflui o painel inteiro — o defeito que a isca planta.
3. O clone e o `AcceptButton` [503691] como molde: herda o `Button.onClick` SERIALIZADO (que chama
   `ConfirmLevelUpSelection` = escrita). O `RemoveAllListeners()` NAO o remove (limpa so a lista de
   runtime — RSTV-12); a limpeza troca a INSTANCIA do evento (`SelectPartyButton.ClearClickListeners`)
   e so entao instala o listener proprio (`RunButton.OpenForTarget`). O rotulo "Accept/Next" e escrito
   no ORIGINAL pelo `CurLevelUpStage`
   (l.168718); o clone tem o proprio `Text`, desligado dos localizadores (`DisableLocalizers`) e
   reescrito para `Skills` (`OptionsManager.Localize`).
4. Todo caminho de falha escreve o MOTIVO no log (`Fail`).
5. `Patches.cs` ganha o postfix de `RoguelikeManager.OpenSkillSelectWindow` -> `LevelUpWindowButton.Ensure`.
6. `RunButton.OpenForTarget()` e o corpo UNICO de abertura da run (extraido do antigo `OnClick`), REUSADO
   pelo botao do HUD, pelo botao da janela e pelo atalho (`SkillTreeShortcut`). A maquinaria da RSTV-9
   (`HomeInLevelUp`/`HomeInRow`/`CaptureHome`, `_home*`, `LadoMinimoLevelUp`/`MargemLevelUp`) foi
   REMOVIDA do `RunButton`.

COMO O ESPERADO E OBTIDO
------------------------
Os fontes sao lidos AO VIVO (`RoguelikeSkillTreeVisualizer/{LevelUpWindowButton,RunButton,SkillTreeShortcut,Patches}.cs`).
Os CORPOS de metodo saem por casamento de chaves (`recorte.corpo_do_metodo`) e a checagem usa o texto SEM
comentario (`recorte.codigo_efetivo`): uma citacao num comentario nao e codigo.

Os MODELOS PUROS (abaixo) transcrevem o comportamento campo a campo: o `Ensure` (1a chamada CRIA, 2a
chamada com o mesmo botao vivo vira NO-OP) e o REFLOW do painel (filho no `Content` reflui; filho na
janela nao). As funcoes de PLANTIO DO DEFEITO devolvem o MESMO fonte com o defeito reinjetado, em
memoria — e a isca (`cp_rstv11b_...py`) que prova que as checagens reprovam de verdade.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import recorte as rec

# Assinaturas exatas lidas do fonte. Se um nome mudar, a checagem REPROVA dizendo qual sumiu.
ENSURE = "internal static void Ensure(RoguelikeManager rok)"
ENSURE_INTERNAL = "private static void EnsureInternal(RoguelikeManager rok)"
RUN_ENSURE_INTERNAL = "private static void EnsureInternal(CurrentCharacterUI ui)"
ANCHOR = "internal static void AnchorToContentCorner(RectTransform rt, RectTransform janela, RectTransform content)"
FAIL = "private static void Fail(string motivo, bool aviso)"
OPEN_FOR_TARGET = "internal static void OpenForTarget()"
CLASSE_DO_GANCHO = "internal static class RoguelikeManagerOpenSkillSelectWindowPatch"

# A guarda de idempotencia: a 2a chamada (mesma janela, botao vivo) e no-op. O texto EXATO e o que a
# checagem exige — o defeito plantado troca o `if` e por isso e pego.
GUARDA_IDEMPOTENTE = "if (_janela == janela && _button != null)"

# Trechos que PROVAM o caminho da RSTV-9 no `RunButton` — todos tem de ter SUMIDO.
RESTOS_DA_RSTV9 = (
    "HomeInLevelUp",
    "HomeInRow",
    "CaptureHome",
    "_homeParent",
    "_naJanelaDoLevelUp",
    "LadoMinimoLevelUp",
    "MargemLevelUp",
)

# ------------------------------------------------------------------ caminhos ---

def _dir_mod():
    return os.path.join(arc.raiz_do_repo(), "RoguelikeSkillTreeVisualizer")


def caminho_janela():
    return os.path.join(_dir_mod(), "LevelUpWindowButton.cs")


def caminho_run():
    return os.path.join(_dir_mod(), "RunButton.cs")


def caminho_atalho():
    return os.path.join(_dir_mod(), "SkillTreeShortcut.cs")


def caminho_patches():
    return os.path.join(_dir_mod(), "Patches.cs")


def fonte(caminho):
    """O fonte vivo do mod (nao uma copia: a expectativa fica amarrada ao que sera compilado)."""
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def _efetivo(src):
    return rec.codigo_efetivo(src)


def _corpo(src, assinatura):
    return rec.corpo_do_metodo(_efetivo(src), assinatura)


# ------------------------------------------------------------- modelo do Ensure ---
# Campo a campo, como o `EnsureInternal`. `botao_vivo`/`mesma_janela` SAO o estado que a idempotencia
# olha: um clone VIVO da MESMA janela nao pode ser recriado.

CENARIO_ENSURE_INICIAL = {
    "ligado": True,          # Plugin.RunBotaoLigado
    "janela_ok": True,       # rok.SkillSelectWindow != null
    "accept_ok": True,       # rok.AcceptButton != null (o molde)
    "content_ok": True,      # o pai do AcceptButton (Content) e RectTransform (medicao do canto)
    "botao_vivo": False,     # ainda nao ha clone desta janela
    "mesma_janela": True,    # identidade da SkillSelectWindow
}

CRIA = "cria"
NOOP = "noop"
FALHA = "falha"


def ensure_avaliado(m):
    """Transcricao PURA do `EnsureInternal`: devolve CRIA, NOOP ou FALHA.

    A ORDEM e a do fonte: config -> janela -> molde -> content -> idempotencia. A idempotencia so
    depois de o estado estar sao (nao ha no-op "por acidente" de um estado invalido).
    """
    if not m["ligado"]:
        return FALHA
    if not m["janela_ok"]:
        return FALHA
    if not m["accept_ok"]:
        return FALHA
    if not m["content_ok"]:
        return FALHA
    if m["botao_vivo"] and m["mesma_janela"]:
        return NOOP
    return CRIA


def ensure_sem_idempotencia(m):
    """O DEFEITO plantado: o `Ensure` ignora o clone VIVO da mesma janela -> cria um SEGUNDO botao.

    E o comportamento da 2a chamada (proximo personagem da fila) sem a guarda de idempotencia.
    """
    mu = dict(m)
    mu["botao_vivo"] = False
    return ensure_avaliado(mu)


def campos_do_ensure():
    """As chaves do cenario (fonte unica do nome dos campos do modelo)."""
    return list(CENARIO_ENSURE_INICIAL.keys())


# ------------------------------------------------------------- modelo do reflow ---
# O painel reflui se e so se o clone nasce DENTRO do `Content` (que tem VerticalLayoutGroup +
# ContentSizeFitter). Filho direto do `SkillSelectWindow` nao reflui (ele nao tem layout group).

CENARIO_CLONE_JANELA = {"pai": "janela"}   # a implementacao: filho direto do SkillSelectWindow
CENARIO_CLONE_CONTENT = {"pai": "content"}  # o defeito: filho do Content


def reflui_painel(m):
    """True se um filho nesse pai reflui o painel do level-up. O `Content` reflui; a janela nao."""
    return m["pai"] == "content"


def campos_do_reflow():
    return list(CENARIO_CLONE_JANELA.keys())


# ------------------------------------------------------------------ checagens ---

def _falta(texto, trecho, rotulo):
    return None if trecho in texto else "faltou %s (%r)" % (rotulo, trecho)


def falhas_do_botao_da_janela(src_janela, src_patches):
    """Defeitos do botao da janela encontrados no FONTE. Lista vazia = a regra esta de pe."""
    falhas = []

    ensure = _corpo(src_janela, ENSURE)
    if ensure is None:
        return ["nao achei %s no LevelUpWindowButton.cs" % ENSURE]

    interno = _corpo(src_janela, ENSURE_INTERNAL)
    if interno is None:
        return ["nao achei %s no LevelUpWindowButton.cs" % ENSURE_INTERNAL]

    # ------------------------------------------------ 1) liga/desliga e a janela do prefab
    if "Plugin.RunBotaoLigado" not in interno:
        falhas.append("EnsureInternal nao respeita o config (`Plugin.RunBotaoLigado`)")
    if "rok.SkillSelectWindow" not in interno:
        falhas.append("EnsureInternal nao le `rok.SkillSelectWindow` (a janela que o jogo liga/desliga)")
    if "rok.AcceptButton" not in interno:
        falhas.append("EnsureInternal nao le `rok.AcceptButton` (o molde do clone)")

    # ------------------------------------------ 2) IDEMPOTENTE por janela (a 2a chamada e no-op)
    if GUARDA_IDEMPOTENTE not in interno:
        falhas.append("EnsureInternal nao tem a guarda de idempotencia `%s` — o postfix roda de novo "
                      "a cada personagem da fila e criaria um SEGUNDO botao" % GUARDA_IDEMPOTENTE)

    # ------------------------- 3) o clone e filho DIRETO da janela, NUNCA do Content (sem reflow)
    if "Instantiate(original.gameObject, janela.transform)" not in interno:
        falhas.append("o clone NAO nasce como filho direto da janela "
                      "(`Instantiate(original.gameObject, janela.transform)`) — clonar dentro do "
                      "Content reflui o painel (RSTV-10, secao 4)")
    if "Instantiate(original.gameObject, contentRt)" in interno:
        falhas.append("o clone nasce DENTRO do Content — o VerticalLayoutGroup/ContentSizeFitter "
                      "reflui o painel inteiro (o defeito que a isca planta)")

    # ---------------------------------------------- 4) rotulo limpo + localizacao desligada
    if "DisableLocalizers(clone)" not in interno:
        falhas.append("EnsureInternal nao desliga os localizadores do clone "
                      "(`DisableLocalizers(clone)`) — o rotulo seria reescrito pelo jogo")
    rotulo = _corpo(src_janela, "private static void EnsureLabel(GameObject clone)")
    if rotulo is None or "OptionsManager.Localize(Label)" not in rotulo:
        falhas.append("o rotulo do clone nao e escrito com `OptionsManager.Localize(Label)`")

    # -------------------- 5) onClick SERIALIZADO limpo + o listener UNICO (RunButton.OpenForTarget)
    # RSTV-12: o `RemoveAllListeners()` NAO limpa o listener PERSISTENTE (serializado no prefab):
    # ele esvazia so a lista de runtime (`InvokableCallList.Clear()`) e o persistente roda ANTES do
    # nosso. A limpeza passou a trocar a INSTANCIA do evento (`SelectPartyButton.ClearClickListeners`),
    # que descarta junto a lista serializada.
    if "SelectPartyButton.ClearClickListeners(button)" not in interno:
        falhas.append("EnsureInternal nao descarta o onClick SERIALIZADO do AcceptButton "
                      "(`SelectPartyButton.ClearClickListeners`) — o `ConfirmLevelUpSelection` "
                      "(avanco de level-up = ESCRITA) continuaria no clone")
    if "RemoveAllListeners()" in interno:
        falhas.append("EnsureInternal voltou a usar `RemoveAllListeners()` — ele limpa so a lista de "
                      "runtime e NAO o listener persistente do prefab (RSTV-12: o conserto exige a "
                      "troca da instancia do evento)")
    if "AddListener(new UnityAction(RunButton.OpenForTarget))" not in interno:
        falhas.append("o onClick do clone nao aponta para `RunButton.OpenForTarget` (o corpo unico da run)")

    # ------------------------------------ 6) ancorado no canto do PAINEL Content (nao da tela)
    if "AnchorToContentCorner(" not in interno:
        falhas.append("EnsureInternal nao ancora o clone pelo canto do Content (`AnchorToContentCorner`)")
    ancora = _corpo(src_janela, ANCHOR)
    if ancora is None:
        falhas.append("nao achei %s no LevelUpWindowButton.cs" % ANCHOR)
    else:
        for trecho, rotulo_c in (
            ("content.GetWorldCorners", "o rect de mundo do painel Content"),
            ("janela.InverseTransformPoint", "a conversao para o espaco local da janela"),
            ("SetAsLastSibling", "o ultimo irmao (desenha/clica por cima)"),
        ):
            falta = _falta(ancora, trecho, rotulo_c)
            if falta:
                falhas.append("AnchorToContentCorner nao usa %s" % rotulo_c)

    # ------------------------------------------------- 7) cada falha escreve o MOTIVO no log
    if _corpo(src_janela, FAIL) is None:
        falhas.append("nao achei o `Fail` do botao da janela (sem log de motivo)")
    if _efetivo(src_janela).count("Fail(") < 5:
        falhas.append("ha menos de 5 caminhos de falha com log de motivo no LevelUpWindowButton")

    # ----------------------------------------- 8) o gancho: postfix do OpenSkillSelectWindow
    gancho = _corpo_da_classe(src_patches, CLASSE_DO_GANCHO)
    atributo = _linha_antes(src_patches, CLASSE_DO_GANCHO)
    if "typeof(RoguelikeManager)" not in atributo or "OpenSkillSelectWindow" not in atributo:
        falhas.append("o gancho nao e `[HarmonyPatch(typeof(RoguelikeManager), ...OpenSkillSelectWindow...)]` "
                      "(a linha antes da classe e %r)" % atributo)
    if "[HarmonyPostfix]" not in gancho:
        falhas.append("o gancho do botao da janela nao tem [HarmonyPostfix]")
    if "LevelUpWindowButton.Ensure" not in gancho:
        falhas.append("o postfix nao chama `LevelUpWindowButton.Ensure`")

    return falhas


def falhas_da_reuniao(src_run, src_atalho):
    """Defeitos da extracao do `OpenForTarget` e da aposentadoria da RSTV-9. Lista vazia = de pe."""
    falhas = []

    # ------------------------------------------ 1) OpenForTarget existe e e o corpo unico da run
    abrir = _corpo(src_run, OPEN_FOR_TARGET)
    if abrir is None:
        return ["nao achei %s no RunButton.cs" % OPEN_FOR_TARGET]

    for trecho, rotulo in (
        ("RunTargets.GateOk", "o portao 4 (RunTargets.GateOk)"),
        ("RunTargets.Resolve", "o alvo resolvido na hora (RunTargets.Resolve)"),
        ("SkillTreesTab.Abrir(alvo, ReadOnlyContext.Run)", "a abertura read-only (agora a aba do inventario, RSTV-16)"),
    ):
        if trecho not in abrir:
            falhas.append("OpenForTarget nao faz %s (trecho %r)" % (rotulo, trecho))

    # -------------------------------- 2) o botao do HUD e o atalho passam a REUSAR o corpo unico
    interno = _corpo(src_run, RUN_ENSURE_INTERNAL)
    if interno is None or "new UnityAction(OpenForTarget)" not in interno:
        falhas.append("o botao do HUD nao aponta para `OpenForTarget` (duplicaria o corpo)")
    if "RunButton.OpenForTarget" not in _corpo(src_atalho, "private static void Abrir(KeyCode tecla)"):
        falhas.append("o atalho (SkillTreeShortcut.Abrir) nao reusa `RunButton.OpenForTarget` "
                      "(o ramo da run continuaria duplicado)")

    # ---------------------------------- 3) a maquinaria da RSTV-9 saiu do RunButton (aposentada)
    efetivo_run = _efetivo(src_run)
    for trecho in RESTOS_DA_RSTV9:
        if trecho in efetivo_run:
            falhas.append("o RunButton ainda tem `%s` — o re-parent da RSTV-9 nao foi aposentado" % trecho)
    if "private static void OnClick" in efetivo_run:
        falhas.append("o antigo `OnClick` do RunButton ainda existe (deveria ser o `OpenForTarget`)")

    return falhas


# ------------------------------------------------------------ utilidades de recorte ---

def _corpo_da_classe(src, marcador):
    efetivo = _efetivo(src)
    i = efetivo.find(marcador)
    arc.exigir(i >= 0, "nao achei %r no fonte" % marcador)
    faixa = rec.faixa_bloco_apos(efetivo, i)
    return efetivo[i:faixa[1] + 1]


def _linha_antes(src, marcador):
    efetivo = _efetivo(src)
    i = efetivo.find(marcador)
    arc.exigir(i >= 0, "nao achei %r no fonte" % marcador)
    linhas = [linha.strip() for linha in efetivo[:i].splitlines() if linha.strip()]
    return linhas[-1] if linhas else ""


# ------------------------------------------------------------ plantio dos defeitos ---

_ANCORA_IDEMPOT = GUARDA_IDEMPOTENTE
_DEFEITO_SEM_IDEMPOT = "if (false && _janela == janela && _button != null)"

_ANCORA_JANELA = "Instantiate(original.gameObject, janela.transform)"
_DEFEITO_NO_CONTENT = "Instantiate(original.gameObject, contentRt)"


def fonte_sem_idempotencia(src=None):
    """O MESMO fonte com a guarda de idempotencia MORTA (`if (false && ...)`).

    Nao mexe em arquivo nenhum: devolve o texto. Prova que a checagem pega o SEGUNDO botao.
    """
    texto = fonte(caminho_janela()) if src is None else src
    if _ANCORA_IDEMPOT not in texto:
        return texto
    return texto.replace(_ANCORA_IDEMPOT, _DEFEITO_SEM_IDEMPOT, 1)


def fonte_com_clone_no_content(src=None):
    """O MESMO fonte com o clone dentro do Content (o defeito do reflow), em vez da janela."""
    texto = fonte(caminho_janela()) if src is None else src
    if _ANCORA_JANELA not in texto:
        return texto
    return texto.replace(_ANCORA_JANELA, _DEFEITO_NO_CONTENT, 1)
