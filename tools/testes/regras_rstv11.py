#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rstv11.py - RSTV-11a: o ATALHO de teclado e o Z-ORDER da arvore no level-up, lidos do FONTE vivo.

O QUE ESTA BIBLIOTECA EXISTE PARA TRAVAR
----------------------------------------
PARTE 1 - o atalho (proposta D). O gancho e o POSTFIX de `KeybindManager.Update` (l.133297). O jogo
sai desse metodo por `return` cedo em tres lugares (l.133335 desabilitado/remap, l.133374 foco de
texto/EventWindow/estados de menu, l.133449 janela de UI aberta) - e o postfix roda INCLUSIVE nesses
returns. Ou seja, o gancho sozinho NAO herda guarda nenhuma: quem decide se a tecla pode agir e o
HANDLER (`SkillTreeShortcut`), que REPLICA os guards. Sem isso, o F10 dispararia durante o CHAT (o
defeito plantado por `fonte_com_atalho_sem_guard`).

O despacho espelha o `RunButton.OnClick` (RunButton.cs l.568): tela Select Party ativa ->
`SkillTreeReadOnly.Open(PartyTargets.Resolve(), PartyScreen)`; senao `StateAllowed` + o portao ja
validado (`RunTargets.GateOk`) + `RunTargets.Resolve` != null -> `Open(alvo, Run)`. A tecla e CRUA
(`Input.GetKeyDown`, config `TeclaAtalhoSkillTree`), NUNCA a acao 10 nativa
(`GetButtonDownAndSwitchToPlayerCharacter(10)`, l.133500), que abriria a janela vanilla junto.

PARTE 2 - o z-order. `SkillTreeReadOnly.ZOrderReference(Run)` devolvia SEMPRE
`CurrentCharacterUI.Instance.transform`; no level-up esse HUD esta `SetActive(false)` (o jogo o
desliga em `GUIManager.Update`, l.120492) - uma referencia DESLIGADA nao eleva nada. O conserto:
quando `RunTargets.JanelaDoLevelUpAberta()`, a referencia passa a ser o `RoguelikeManager`
(`Instance` l.168659; fallback `ForcedInstance` l.168673), que continua ativo. O defeito plantado por
`fonte_com_zorder_preso` volta a devolver o HUD dentro do level-up.

COMO O ESPERADO E OBTIDO
------------------------
Os fontes sao lidos AO VIVO (`RoguelikeSkillTreeVisualizer/{SkillTreeShortcut,Patches,Plugin,SkillTreeReadOnly}.cs`)
- nao copias: a expectativa fica amarrada ao que sera compilado. Os CORPOS de metodo saem por
casamento de chaves (`recorte.corpo_do_metodo`, sem janela de caracteres) e a checagem de codigo usa
o texto SEM comentario (`recorte.codigo_efetivo`) - uma citacao num comentario nao e codigo.

A UNICA leitura que NAO e literal do cartao, e por que
------------------------------------------------------
O guard de estado do jogo (l.133374) bloqueia tambem `GUIState.ChoosingCharacter` - que e o estado
EXATO da tela "Select Party" (`OpenCharacterChoiceManager` o escreve, l.328705). Bloquear ali
tornaria MORTO o ramo de despacho da tela de party que o proprio cartao pede ("se CharacterChoiceManager
ativo -> Open(PartyTargets.Resolve(), PartyScreen)"). O cartao e internamente contraditorio nesse
ponto; a regra implementada (e travada aqui) resolve a contradicao pelo comportamento ESPECIFICO
(despacho de party) em vez do resumo generico dos guards: `CreatingCharacter`/`InMainMenu` continuam
bloqueando, `ChoosingCharacter` e atendido pelo ramo de party. O guard de janela (l.133449) leva a
MESMA excecao de level-up do portao da RSTV-8 - sem ela, a tecla nao funcionaria justamente durante o
level-up, contradizendo o "level-up liberado pela RSTV-8".
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import recorte as rec

# Assinaturas exatas lidas do fonte. Se um nome mudar, a checagem REPROVA dizendo qual sumiu.
HANDLE_ATALHO = "internal static void Handle(KeybindManager kb)"
LIBERADO = "private static bool Liberado(KeybindManager kb, out string motivo)"
FOCO_DE_TEXTO = "private static bool FocoDeTexto()"
ABRIR = "private static void Abrir(KeyCode tecla)"
CLASSE_DO_GANCHO = "internal static class KeybindManagerUpdatePatch"
ASSINATURA_DO_GANCHO = '[HarmonyPatch(typeof(KeybindManager), "Update", new Type[0])]'

# ---------------------------------------------------------------- modelos puros ---
#
# O atalho, campo a campo. `True` = a condicao esta satisfeita (o caminho esta livre).
CENARIO_ATALHO_RUN = {
    "ligado": True,             # Plugin.AtalhoLigado
    "tecla_pressionada": True,  # Input.GetKeyDown(TeclaAtalhoSkillTree)
    "keybinds_ativos": True,    # !KeybindManager.DisableKeybinds
    "sem_remap": True,          # !OptionsManager.CurrentlyBindingControls
    "sem_foco_de_texto": True,  # !FocoDeTexto() (o guard de CHAT do defeito plantado)
    "sem_event_window": True,   # !EventWindow.IsNotNullAndIsActive
    "estado_permitido": True,   # GUIState fora de CreatingCharacter/InMainMenu
    "tela_party": False,        # !CharacterChoiceManager.IsNotNullAndIsActive
    "tem_alvo_party": True,     # PartyTargets.Resolve() != null (so no ramo de party)
    "sem_janela_aberta": True,  # !AnyUIWindowOpenOtherThan(RoguelikeManager.Instance)
    "level_up": False,          # RunTargets.JanelaDoLevelUpAberta() (excecao do guard de janela)
    "portao_ok": True,          # RunTargets.GateOk(out motivo)
    "tem_alvo_run": True,       # RunTargets.Resolve(out motivo) != null
}

# O cenario do DEFEITO plantado: o chat aberto NAO e guardado.
CENARIO_CHAT_ABERTO = dict(CENARIO_ATALHO_RUN, sem_foco_de_texto=False)

# O level-up: a janela modal esta aberta (o guard de janela dispararia sem a excecao da RSTV-8).
CENARIO_ATALHO_LEVELUP = dict(CENARIO_ATALHO_RUN, level_up=True, sem_janela_aberta=False)

# A tela "Select Party": o estado e ChoosingCharacter e o CharacterChoiceManager esta ativo.
CENARIO_ATALHO_PARTY = dict(CENARIO_ATALHO_RUN, tela_party=True, level_up=False)


def _despacho(c):
    """O trecho comum do despacho: o ramo de party e o ramo da run.

    Devolve "PartyScreen", "Run" ou None (nao abre). NAO contem os guards do jogo - eles sao
    aplicados por `atalho_novo`/`atalho_sem_guard`/`atalho_sem_portao`, que sao as regras comparadas.
    """
    if c["tela_party"]:
        return "PartyScreen" if c["tem_alvo_party"] else None

    if not c["sem_janela_aberta"] and not c["level_up"]:
        return None
    if not c["portao_ok"]:
        return None
    if not c["tem_alvo_run"]:
        return None
    return "Run"


def atalho_novo(c):
    """A regra IMPLEMENTADA: config -> guards replicados do jogo (remap/chat/evento/estado) -> despacho."""
    if not c["ligado"]:
        return None
    if not c["tecla_pressionada"]:
        return None
    if not c["keybinds_ativos"]:
        return None
    if not c["sem_remap"]:
        return None
    if not c["sem_foco_de_texto"]:
        return None
    if not c["sem_event_window"]:
        return None
    if not c["estado_permitido"]:
        return None
    return _despacho(c)


def atalho_sem_guard(c):
    """O DEFEITO plantado: o gancho age sem replicar o guard de foco de texto (chat).

    Com o chat aberto, esta regra ABRE enquanto a implementada NAO - e a prova de que o guard de chat
    e o que separa o comportamento certo do errado.
    """
    c = dict(c)
    c["sem_foco_de_texto"] = True     # o defeito: a tecla ignora o chat
    return atalho_novo(c)


def atalho_sem_portao(c):
    """O DEFEITO plantado 2: o ramo da run abre sem o portao ja validado (RunTargets.GateOk)."""
    c = dict(c)
    c["portao_ok"] = True
    return atalho_novo(c)


def campos_do_atalho():
    """As chaves do cenario (fonte unica do nome dos campos do modelo)."""
    return list(CENARIO_ATALHO_RUN.keys())


# ------------------------------------------------------------------------ leitura ---

def _dir_mod():
    return os.path.join(arc.raiz_do_repo(), "RoguelikeSkillTreeVisualizer")


def caminho_atalho():
    return os.path.join(_dir_mod(), "SkillTreeShortcut.cs")


def caminho_patches():
    return os.path.join(_dir_mod(), "Patches.cs")


def caminho_plugin():
    return os.path.join(_dir_mod(), "Plugin.cs")


def fonte(caminho=None):
    """O fonte vivo do mod (nao uma copia: a expectativa fica amarrada ao que sera compilado)."""
    with open(caminho or caminho_atalho(), encoding="utf-8") as fh:
        return fh.read()


def _efetivo(src):
    """O codigo SEM comentario de linha/bloco (a citacao num comentario nao e codigo)."""
    return rec.codigo_efetivo(src)


def _corpo(src, assinatura):
    """Corpo `{...}` de um metodo do fonte EFETIVO (sem comentario), por casamento de chaves."""
    return rec.corpo_do_metodo(_efetivo(src), assinatura)


def _corpo_da_classe(src, marcador):
    """Do marcador ATE o fim do bloco `{...}` da classe."""
    efetivo = _efetivo(src)
    i = efetivo.find(marcador)
    arc.exigir(i >= 0, "nao achei %r no fonte" % marcador)
    faixa = rec.faixa_bloco_apos(efetivo, i)
    return efetivo[i:faixa[1] + 1]


def _linha_antes(src, marcador):
    """A ULTIMA linha nao vazia do codigo efetivo ANTES do marcador (sem janela de caracteres).

    E o atributo que precede a declaracao (ex.: `[HarmonyPatch(typeof(KeybindManager), "Update", ...)]`).
    """
    efetivo = _efetivo(src)
    i = efetivo.find(marcador)
    arc.exigir(i >= 0, "nao achei %r no fonte" % marcador)
    linhas = [linha.strip() for linha in efetivo[:i].splitlines() if linha.strip()]
    return linhas[-1] if linhas else ""


def _chamada(codigo, marcador):
    """A chamada inteira (marcador + parenteses balanceados, literais respeitados) — sem janela fixa."""
    i = codigo.find(marcador)
    arc.exigir(i >= 0, "nao achei a chamada %r" % marcador)
    j = codigo.find("(", i)
    arc.exigir(j >= 0, "o marcador %r nao abre chamada" % marcador)
    nivel, p = 0, j
    while p < len(codigo):
        c = codigo[p]
        if c in "\"'":
            p = rec.fim_do_literal(codigo, p)
            continue
        if c == "(":
            nivel += 1
        elif c == ")":
            nivel -= 1
            if nivel == 0:
                return codigo[i:p + 1]
        p += 1
    raise arc.Falhou("a chamada %r nao fecha os parenteses — o fonte foi cortado?" % marcador)


# ------------------------------------------------------------------ checagens ---

def falhas_do_atalho(src, src_patches, src_plugin):
    """Defeitos do atalho encontrados no FONTE. Lista vazia = a regra esta de pe."""
    falhas = []

    # ------------------------------------------------------- 1) o gancho e o postfix
    atributo = _linha_antes(src_patches, CLASSE_DO_GANCHO)
    gancho = _corpo_da_classe(src_patches, CLASSE_DO_GANCHO)
    if ASSINATURA_DO_GANCHO not in atributo:
        falhas.append("o gancho nao e `%s` (a ancora do jogo mudou; a linha antes da classe e %r)"
                      % (ASSINATURA_DO_GANCHO, atributo))
    if "[HarmonyPostfix]" not in gancho:
        falhas.append("o gancho do atalho nao tem [HarmonyPostfix] — ele nao rodaria nos early-returns")
    if "SkillTreeShortcut.Handle" not in gancho:
        falhas.append("o gancho nao chama `SkillTreeShortcut.Handle`")

    # ----------------------------------------- 2) o handler existe e le a tecla CRUA
    handle = _corpo(src, HANDLE_ATALHO)
    if handle is None:
        return ["nao achei %s no SkillTreeShortcut.cs" % HANDLE_ATALHO]
    if "Input.GetKeyDown" not in handle:
        falhas.append("Handle nao le a tecla crua (`Input.GetKeyDown`) — sem config de tecla")
    if "Plugin.TeclaAtalho" not in handle:
        falhas.append("Handle nao usa a tecla do config (`Plugin.TeclaAtalho`)")
    if "Plugin.AtalhoLigado" not in handle:
        falhas.append("Handle nao respeita o liga/desliga do config (`Plugin.AtalhoLigado`)")

    # A acao 10 nativa nao pode estar no CODIGO (o comentario que a cita nao conta): ela abriria a
    # janela vanilla de skill tree junto.
    efetivo = _efetivo(src)
    if "GetButtonDownAndSwitchToPlayerCharacter" in efetivo or "VirtualInput" in efetivo:
        falhas.append("o atalho toca a acao NATIVA (VirtualInput/GetButtonDownAndSwitchToPlayerCharacter) "
                      "— abriria a janela vanilla de skill tree junto")

    # ------------------------------------------ 3) os guards do jogo sao REPLICADOS
    liberado = _corpo(src, LIBERADO)
    if liberado is None:
        falhas.append("nao achei %s (os guards do jogo nao sao replicados)" % LIBERADO)
    else:
        for trecho, rotulo in (
            ("DisableKeybinds", "o guard de keybinds desabilitados (l.133335)"),
            ("CurrentlyBindingControls", "o guard de REMAP de tecla (l.133335)"),
            ("if (FocoDeTexto())", "de foco de texto/chat (l.133374)"),
            ("EventWindow.IsNotNullAndIsActive", "o guard da janela de evento (l.133374)"),
        ):
            if trecho not in liberado:
                falhas.append("o guard %s saiu do Liberado (trecho %r)" % (rotulo, trecho))

        # ESTADOS: os de menu continuam bloqueados; `ChoosingCharacter` NAO entra na lista (e o estado
        # da tela Select Party, atendida pelo ramo de party — veja o docstring deste modulo).
        if "GUIState.CreatingCharacter" not in liberado or "GUIState.InMainMenu" not in liberado:
            falhas.append("o guard de estado (l.133374) nao bloqueia CreatingCharacter/InMainMenu")
        if "GUIState.ChoosingCharacter" in liberado:
            falhas.append("o guard de estado bloqueia `ChoosingCharacter` — isso torna MORTO o ramo da "
                          "tela Select Party (o estado dela e exatamente ChoosingCharacter)")

    # O foco de texto cobre o CHAT e os campos das janelas do jogo (l.133374).
    foco = _corpo(src, FOCO_DE_TEXTO)
    if foco is None:
        falhas.append("nao achei %s no SkillTreeShortcut.cs (o guard de chat nao tem corpo)" % FOCO_DE_TEXTO)
    else:
        for trecho, rotulo in (
            ("MessageWindowManager", "o chat (MessageWindowManager)"),
            ("TextInputIsFocused", "o TextInputIsFocused"),
            ("InventoryManager", "o inventario"),
            ("ItemStashManager", "a mochila"),
            ("FortuneWindow", "a janela fortune"),
            ("DebugWindow", "o debug window"),
        ):
            if trecho not in foco:
                falhas.append("FocoDeTexto nao cobre %s (trecho %r)" % (rotulo, trecho))

    # ------------------------------------ 4) o DESPACHO espelha o caminho do botao
    abrir = _corpo(src, ABRIR)
    if abrir is None:
        falhas.append("nao achei %s no SkillTreeShortcut.cs" % ABRIR)
    else:
        for trecho, rotulo in (
            ("CharacterChoiceManager.IsNotNullAndIsActive", "o teste da tela Select Party"),
            ("PartyTargets.Resolve()", "o alvo de party (PartyTargets.Resolve)"),
            ("ReadOnlyContext.PartyScreen", "o contexto PartyScreen"),
            ("RunTargets.StateAllowed", "a whitelist de estado da run"),
            # RSTV-11b: o ramo da RUN deixou de DUPLICAR o antigo `RunButton.OnClick` (GateOk ->
            # Resolve -> Open(alvo, Run)); agora delega ao corpo UNICO `RunButton.OpenForTarget`, o
            # MESMO do botao do HUD e do botao da janela do level-up.
            ("RunButton.OpenForTarget", "o despacho unico da run (RunButton.OpenForTarget, RSTV-11b)"),
        ):
            if trecho not in abrir:
                falhas.append("o despacho nao usa %s (trecho %r)" % (rotulo, trecho))

        # ORDEM: o ramo de party vem ANTES do ramo da run (senao a tela Select Party nunca e atendida).
        i_party = abrir.find("CharacterChoiceManager.IsNotNullAndIsActive")
        i_run = abrir.find("RunTargets.StateAllowed")
        if i_party < 0 or i_run < 0 or i_party > i_run:
            falhas.append("o ramo da TELA SELECT PARTY nao vem antes do ramo da run no Abrir")

        # O guard de JANELA (l.133449) leva a excecao de level-up do portao (RSTV-8): sem ela a tecla
        # nao funcionaria durante o level-up.
        if "AnyUIWindowOpenOtherThan" not in abrir:
            falhas.append("o guard de janela (l.133449, AnyUIWindowOpenOtherThan) saiu do despacho")
        if "RunTargets.JanelaDoLevelUpAberta()" not in abrir:
            falhas.append("o guard de janela nao tem a excecao de LEVEL-UP (RSTV-8) — a tecla ficaria "
                          "bloqueada justamente quando o jogador mais quer a arvore")

    # ------------------------------------------------- 5) config: ligado + tecla F10
    efetivo_plugin = _efetivo(src_plugin)
    bind_ligado = _chamada(efetivo_plugin, "AtalhoSkillTree = Config.Bind(")
    bind_tecla = _chamada(efetivo_plugin, "TeclaAtalhoSkillTree = Config.Bind(")
    if "true" not in bind_ligado:
        falhas.append("`AtalhoSkillTree` nao nasce `true` (o padrao do mod e ligado)")
    if "KeyCode.F10" not in bind_tecla:
        falhas.append("`TeclaAtalhoSkillTree` nao nasce `KeyCode.F10`")
    if "internal static KeyCode TeclaAtalho" not in efetivo_plugin:
        falhas.append("nao achei o acesso `Plugin.TeclaAtalho` no Plugin.cs")
    if "internal static bool AtalhoLigado" not in efetivo_plugin:
        falhas.append("nao achei o acesso `Plugin.AtalhoLigado` no Plugin.cs")

    return falhas


# ------------------------------------------------------------ plantio dos defeitos ---

_ANCORA_CHAT = "if (FocoDeTexto())"
_DEFEITO_SEM_CHAT = "if (false && FocoDeTexto())"


def fonte_com_atalho_sem_guard(src=None):
    """O MESMO fonte com o DEFEITO reinjetado: o guard de CHAT deixa de ser um ramo VIVO.

    A troca e no proprio `if` (nao no corpo): a checagem exige o trecho EXATO `if (FocoDeTexto())`, e
    e por isso que o defeito e pego. Nao mexe em arquivo nenhum: devolve o texto.
    """
    texto = fonte() if src is None else src
    if _ANCORA_CHAT not in texto:
        return texto
    return texto.replace(_ANCORA_CHAT, _DEFEITO_SEM_CHAT, 1)
