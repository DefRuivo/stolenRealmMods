#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rstv16.py - RSTV-16: a aba "All Skill Trees" no INVENTARIO e a aposentadoria da janela separada.

O QUE ESTA BIBLIOTECA TRAVA (lida do FONTE vivo, nunca de copia)
----------------------------------------------------------------
Decisao do dono (02/10): em vez da janela read-only SEPARADA (RSTV-2/5/15) empilhada por cima de tudo,
o mod passa a acrescentar uma ABA na barra do inventario (`CharacterMenusManager` / `MenuTabManager`) com
TODAS as arvores, menos a do BARD (nao esta no jogo).

1. A ABA (`SkillTreesTab.Ensure`): clone de `menu.TabSkillTree` como IRMAO, relabel por
   `OptionsManager.Localize`, `SetAsLastSibling`, onClick com a INSTANCIA do evento trocada
   (`SelectPartyButton.ClearClickListeners` — RSTV-12: o `RemoveAllListeners()` nao remove a persistente)
   e o handler e `SkillTreesTab.SelecionarEMostrar`. O array PUBLICO `MenuTabManager.MenuTabs` passa a
   INCLUIR a aba (`GetNextActiveTab` usa `Array.IndexOf`; fora dele o jogo loga "Tabbing broke").
   IDEMPOTENTE por NOME; `Initialize()` nunca e chamado as cegas (dispara `SelectFirstActiveButton`).
   PONTO 8: o handler chama `SelectButton` (so marca); `SelectButtonAndInvoke` fica no caminho
   programatico, que abre o inventario PRIMEIRO.

2. O CONTEUDO (`SkillTreesTab.Popular`): a FONTE certa NAO e `SkillsByTreeDict` (l.443327/443341, filtra
   so Tier/Disabled/FullReleaseMode e OMITE `DontIncludeInTree` e o DLC). A regra canonica e a de
   `RefreshAvailableSkillTrees` (l.170100-170118): `Game.Instance.Skills` com o predicado
   `!Disabled && !DontIncludeInTree && FullReleaseModeEnabled(skill)`, e a classe precisa de
   `SteamManager.MeetsDLCRequirements(type)`; `Basic`/`Innate` nao sao arvores. O layout e
   REIMPLEMENTADO (formula de `PopulateTree`, l.177739) — NAO se chama `PopulateTree`/`ProcessDependencyLines`
   (dependem do `skillTreeShowers[]` do Instance). A fileira de classes reusa o `SkillTreeTab` nativo
   (icone+nome, l.178841) via `tabHolder` (l.177223), mostrando UMA arvore por vez.

3. O READ-ONLY NAO E AUTOMATICO (premissa falsa do cartao): a `SkillTreeManager` e PRE-CARREGADA
   (`LoadingScreen.LoadStateBasedResources`, l.136586-136596) e `Instance` NAO e nulo — as guardas
   `if (Instance == null) return;` nao disparam. Quem barra e `ReadOnlySession.Active` (mantida viva
   enquanto a aba esta visivel) e o `SkillTreesTab.Aberto`, no prefixo `SkillTreeItemTogglePatch`.

4. A APOSENTADORIA: `SkillTreeReadOnly.cs` nao tem mais `ZOrder`/`EnsureAbove`/`ZOrderReference`/
   `LifecycleBlock`/`GraceSeconds` (a vida passa a ser a do sistema de abas) e o config `AjustarZOrder`
   saiu do `Plugin.cs`. Ficam: `RunTargets.GateOk`/`Resolve`, o corpo `RunButton.OpenForTarget`, o
   `Patches.cs` read-only e o gancho de `CloseSkillTreeMenu`.

COMO O ESPERADO E OBTIDO
------------------------
Fontes lidos AO VIVO (`RoguelikeSkillTreeVisualizer/{SkillTreesTab,RunButton,SkillTreeShortcut,Patches,
Plugin,SkillTreeReadOnly}.cs`). Corpos por casamento de chaves (`recorte.corpo_do_metodo`) e checagem
sobre o texto SEM comentario (`recorte.codigo_efetivo`). Os MODELOS PUROS (abaixo) transcrevem o
comportamento de `MenuTabManager` (a 4a aba; `SelectButtonAndInvoke` troca o conteudo, `SelectButton`
so realca) e o FILTRO de classes (11 menos Bard/Basic/Innate). As funcoes de PLANTIO devolvem o MESMO
fonte com o defeito reinjetado, em memoria — e a isca `cp_rstv16_*` que prova que as checagens reprovam.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import recorte as rec

# Assinaturas exatas lidas do fonte. Se um nome mudar, a checagem REPROVA dizendo qual sumiu.
ENSURE = "internal static void Ensure(CharacterMenusManager menu)"
ABRIR = "internal static void Abrir(Character alvo, ReadOnlyContext contexto)"
CLICAR = "internal static void SelecionarEMostrar()"
POPULAR = "internal static void Popular(SkillType tipo)"
TIPOS = "internal static List<SkillType> TiposDaAba()"
TICK = "internal static void Tick()"
CLASSE_GANCHO = "internal static class CharacterMenusManagerOpenWindowPatch"
CLASSE_CLIQUE = "internal static class SkillTreeItemTogglePatch"
CLASSE_FECHAMENTO = "internal static class CharacterMenusManagerCloseSkillTreePatch"

# Trechos que PROVAM o desenho, no codigo EFETIVO.
MARCAS_DA_ABA = (
    ("Instantiate(menu.TabSkillTree.gameObject", "o clone da aba nativa Skill Tree"),
    ("TabName", "o nome que torna a injecao IDEMPOTENTE"),
    ("OptionsManager.Localize(TabLabel)", "o relabel da aba"),
    ("SetAsLastSibling", "o SetSiblingIndex (ultimo irmao)"),
    ("ClearClickListeners(botao)", "a troca da INSTANCIA do onClick (RSTV-12)"),
    ("AddListener(new UnityAction(SelecionarEMostrar))", "o handler proprio da aba"),
    ("GetComponentInChildren<MenuTabManager>(true)", "o acesso ao MenuTabManager"),
    ("MenuTabs = novo", "a aba ENTRA no array publico MenuTabs"),
)

RESTOS_DA_JANELA_SEPARADA = (
    "ZOrder",
    "EnsureAbove",
    "ZOrderReference",
    "LifecycleBlock",
    "GraceSeconds",
)


# ------------------------------------------------------------------ caminhos ---

def _dir_mod():
    return os.path.join(arc.raiz_do_repo(), "RoguelikeSkillTreeVisualizer")


def caminho_aba():
    return os.path.join(_dir_mod(), "SkillTreesTab.cs")


def caminho_run():
    return os.path.join(_dir_mod(), "RunButton.cs")


def caminho_atalho():
    return os.path.join(_dir_mod(), "SkillTreeShortcut.cs")


def caminho_patches():
    return os.path.join(_dir_mod(), "Patches.cs")


def caminho_plugin():
    return os.path.join(_dir_mod(), "Plugin.cs")


def caminho_readonly():
    return os.path.join(_dir_mod(), "SkillTreeReadOnly.cs")


def fonte(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def _efetivo(src):
    return rec.codigo_efetivo(src)


def _corpo(src, assinatura):
    return rec.corpo_do_metodo(_efetivo(src), assinatura)


def _corpo_da_classe(src, marcador):
    efetivo = _efetivo(src)
    i = efetivo.find(marcador)
    arc.exigir(i >= 0, "nao achei %r no fonte" % marcador)
    faixa = rec.faixa_bloco_apos(efetivo, i)
    return efetivo[i:faixa[1] + 1]


# ------------------------------------------------------------- modelos puros ---
#
# A LISTA DE CLASSES. A regra IMPLEMENTADA espelha `RefreshAvailableSkillTrees` (l.170113): fora
# Bard (decisao do dono), Basic/Innate (nao sao arvores), e as que falham DLC/predicado de skill.
TIPOS_ASSET = ["Fire", "Lightning", "Cold", "Warrior", "Light", "Ranger",
               "Shadow", "Thief", "Basic", "Innate", "Monk", "Nature", "Chaos", "Bard"]

NAO_ARVORES = ("Basic", "Innate")


def classes_da_aba(tipos, dlc_ok=None, com_skill=None):
    """A regra IMPLEMENTADA: tira Bard, tira Basic/Innate, exige DLC e skill visivel.

    `dlc_ok`/`com_skill` sao os predicados do jogo, por tipo (default: tudo visivel). O Chaos cai
    aqui pelo `FullReleaseModeEnabled`/DLC, como no jogo.
    """
    saida = []
    for t in tipos:
        if t == "Bard":
            continue
        if t in NAO_ARVORES:
            continue
        if dlc_ok is not None and not dlc_ok.get(t, True):
            continue
        if com_skill is not None and not com_skill.get(t, True):
            continue
        if t not in saida:
            saida.append(t)
    return saida


def classes_com_bard(tipos, dlc_ok=None, com_skill=None):
    """O DEFEITO plantado: a lista NAO filtra o Bard (o cartao dizia que Bard aparecia)."""
    saida = classes_da_aba(tipos, dlc_ok, com_skill)
    if "Bard" in tipos and "Bard" not in saida:
        saida.append("Bard")
    return saida


#
# A BARRA DE ABAS. `ABAS` e o array publico `MenuTabs` com a 4a aba (a nossa). `SelectButtonAndInvoke`
# (l.140765) MARCA e INVOCA o onClick -> o CONTEUDO muda; `SelectButton` (l.140744) so realca.

ABAS = ["Character", "SkillTree", "Fortunes", "AllSkillTrees"]
CONTEUDO_INICIAL = "Character"


def conteudo_apos_clique(clique, usar_invoke=True, conteudo_atual=CONTEUDO_INICIAL):
    """O conteudo DEPOIS de clicar na aba `clique` (indice em `ABAS`).

    Implementado (`SelectButtonAndInvoke`): marca + invoca -> conteudo = a aba.
    Defeito (`SelectButton` sozinho): so realca -> o conteudo NAO muda.
    """
    if not usar_invoke:
        return conteudo_atual
    return ABAS[clique]


def aba_no_array(abas, indice):
    """`GetNextActiveTab` faz `Array.IndexOf(MenuTabs, SelectedMenuTab)` (l.140702): fora do array,
    o jogo nao acha a aba e loga "Tabbing broke". A 4a aba TEM de estar no array."""
    return 0 <= indice < len(abas)


# ------------------------------------------------------------------ checagens ---

def falhas_da_aba(src_tab):
    """Defeitos da aba nova no FONTE. Lista vazia = o desenho esta de pe."""
    falhas = []

    ensure = _corpo(src_tab, ENSURE)
    if ensure is None:
        return ["nao achei %s no SkillTreesTab.cs" % ENSURE]

    # 1) A injecao: clone + idempotencia + relabel + onClick limpo + array publico
    efetivo_tab = _efetivo(src_tab)
    for trecho, rotulo in MARCAS_DA_ABA:
        if trecho not in efetivo_tab:
            falhas.append("a injecao da aba nao faz %s (trecho %r)" % (rotulo, trecho))
    if "RemoveAllListeners()" in efetivo_tab:
        falhas.append("SkillTreesTab usa `RemoveAllListeners()` — ele nao remove o onClick PERSISTENTE "
                      "do prefab (RSTV-12 exige trocar a instancia do evento)")
    if "Initialize()" in ensure:
        falhas.append("Ensure chama `Initialize()` do MenuTabManager — ele dispara "
                      "`SelectFirstActiveButton` e trocaria a aba selecionada (ponto 8)")
    if "Procurar(" not in efetivo_tab:
        falhas.append("a injecao nao tem a busca por NOME (`Procurar`) — a reinjecao criaria uma 2a aba")

    # 2) O onClick da aba MARCA sem re-invocar (SelectButton), e o caminho programatico usa o invoke.
    clicar = _corpo(src_tab, CLICAR)
    if clicar is None:
        falhas.append("nao achei %s no SkillTreesTab.cs" % CLICAR)
    else:
        if "SelectButton(_aba)" not in clicar:
            falhas.append("SelecionarEMostrar nao marca a aba com `SelectButton(_aba)` (o clique do "
                          "jogador nao passa pelo SelectButtonAndInvoke)")
        if "SelectButtonAndInvoke" in clicar:
            falhas.append("SelecionarEMostrar usa `SelectButtonAndInvoke` — o handler re-invocaria o "
                          "proprio onClick (ponto 8: no handler e `SelectButton`)")

    abrir = _corpo(src_tab, ABRIR)
    if abrir is None:
        falhas.append("nao achei %s no SkillTreesTab.cs" % ABRIR)
    else:
        if "OpenCharacterMenu()" not in abrir:
            falhas.append("Abrir nao abre o inventario PRIMEIRO (`menu.OpenCharacterMenu()`)")
        if "SelectButtonAndInvoke" not in _efetivo(src_tab):
            falhas.append("Abrir/Plugar nao usa `SelectButtonAndInvoke` no caminho programatico — so "
                          "realcar nao troca o CONTEUDO (l.140765)")

    # 3) O CONTEUDO: fonte certa + predicado nativo + layout proprio + fileira nativa
    popular = _corpo(src_tab, POPULAR)
    if popular is None:
        falhas.append("nao achei %s no SkillTreesTab.cs" % POPULAR)
    else:
        if "SkillsByTreeDict" in popular:
            falhas.append("Popular usa `SkillsByTreeDict` — a fonte errada: ela OMITE `DontIncludeInTree` "
                          "e o DLC (l.443341). Use `Game.Instance.Skills` (ponto 2)")
        if "jogo.Skills" not in popular and "Game.Instance.Skills" not in popular:
            falhas.append("Popular nao le a lista de skills (`Game.Instance.Skills`) — a fonte canonica "
                          "de `RefreshAvailableSkillTrees` (l.170113)")
        for trecho, rotulo in (("s.Disabled", "o filtro `Disabled`"),
                               ("s.DontIncludeInTree", "o filtro `DontIncludeInTree` (que o SkillsByTreeDict omitia)"),
                               ("FullReleaseModeEnabled", "o `FullReleaseModeEnabled`")):
            if trecho not in popular:
                falhas.append("Popular nao aplica %s (trecho %r)" % (rotulo, trecho))
        if "PopulateTree(" in popular or "ProcessDependencyLines(" in popular:
            falhas.append("Popular chama `PopulateTree`/`ProcessDependencyLines` — sao metodos de "
                          "INSTANCIA e dependem do `skillTreeShowers[]` (ponto 3: reimplementar o layout)")
        if "anchoredPosition" not in popular:
            falhas.append("Popular nao posiciona o no (`anchoredPosition`) — o layout de `PopulateTree` "
                          "(l.177765) nao foi transcrito")

    tipos = _corpo(src_tab, TIPOS)
    if tipos is None:
        falhas.append("nao achei %s no SkillTreesTab.cs" % TIPOS)
    else:
        if "SkillType.Bard" not in tipos:
            falhas.append("TiposDaAba NAO exclui o Bard (decisao do dono: nao esta no jogo)")
        if "SkillType.Basic" not in tipos or "SkillType.Innate" not in tipos:
            falhas.append("TiposDaAba nao exclui `Basic`/`Innate` (nao sao arvores — l.170113)")
        if "MeetsDLCRequirements" not in tipos:
            falhas.append("TiposDaAba nao exige `MeetsDLCRequirements` (o DLC da classe — l.170113)")
    if "TemSkillsVisiveis" not in efetivo_tab:
        falhas.append("nao ha o predicado por classe (`TemSkillsVisiveis`) de RefreshAvailableSkillTrees")

    # 4) NAO se seta `SkillTreeManager.Instance` (o layout e desacoplado)
    if "SkillTreeManager.Instance =" in efetivo_tab or "LoadableUIWindow<SkillTreeManager>.Instance =" in efetivo_tab:
        falhas.append("SkillTreesTab ESCREVE `SkillTreeManager.Instance` — o layout tem de ser "
                      "desacoplado do manager")

    # 5) A fileira de classes reusa o SkillTreeTab nativo (ponto 7)
    if "SkillTreeTab" not in efetivo_tab or "tabHolder" not in efetivo_tab:
        falhas.append("a fileira de classes nao reusa o `SkillTreeTab` nativo via `tabHolder` "
                      "(ponto 7)")

    # 6) A Underline e ajustada/restaurada (ponto 5)
    if "Underline" not in efetivo_tab or "sizeDelta" not in efetivo_tab:
        falhas.append("a `Underline` das abas nao e ajustada/restaurada (ponto 5)")

    return falhas


def falhas_do_readonly_e_atalho(src_tab, src_run, src_atalho, src_patches):
    """O read-only pela SESSAO e o atalho abrindo a aba. Lista vazia = de pe."""
    falhas = []

    # 1) O read-only NAO depende de guarda de null: depende da sessao.
    efetivo_tab = _efetivo(src_tab)
    if "ReadOnlySession.Begin" not in efetivo_tab:
        falhas.append("SkillTreesTab nao abre a SESSAO read-only (`ReadOnlySession.Begin`) — a "
                      "SkillTreeManager e pre-carregada e o clique cairia no corpo real (ponto 1)")
    eu = _corpo_da_classe(src_patches, CLASSE_CLIQUE)
    if "SkillTreesTab.Aberto" not in eu and "ReadOnlySession.Active" not in eu:
        falhas.append("o `SkillTreeItemTogglePatch` nao barra o clique pela sessao/aba "
                      "(ReadOnlySession.Active / SkillTreesTab.Aberto)")

    # 2) O corpo unico da run continua sendo o `RunButton.OpenForTarget`, agora abrindo a ABA.
    abrir_run = _corpo(src_run, "internal static void OpenForTarget()")
    if abrir_run is None:
        return falhas + ["nao achei `RunButton.OpenForTarget()` no RunButton.cs"]
    for trecho, rotulo in (("RunTargets.GateOk", "o portao"),
                           ("RunTargets.Resolve", "o alvo resolvido na hora"),
                           ("SkillTreesTab.Abrir(", "a abertura da ABA (o mod nao abre mais a janela nativa)")):
        if trecho not in abrir_run:
            falhas.append("OpenForTarget nao faz %s (trecho %r)" % (rotulo, trecho))

    abrir_atalho = _corpo(src_atalho, "private static void Abrir(KeyCode tecla)")
    if abrir_atalho is None:
        falhas.append("nao achei o `SkillTreeShortcut.Abrir` no SkillTreeShortcut.cs")
    else:
        if "SkillTreesTab.Abrir(" not in abrir_atalho:
            falhas.append("o ramo da tela Select Party do atalho nao abre a ABA (`SkillTreesTab.Abrir`)")
        if "RunButton.OpenForTarget" not in abrir_atalho:
            falhas.append("o ramo da run do atalho nao reusa `RunButton.OpenForTarget`")

    return falhas


def falhas_da_aposentadoria(src_readonly, src_plugin, src_run, src_patches):
    """A janela separada foi APOSENTADA e os alicerces ficaram? Lista vazia = de pe."""
    falhas = []

    efetivo_ro = _efetivo(src_readonly)
    for trecho in RESTOS_DA_JANELA_SEPARADA:
        if trecho in efetivo_ro:
            falhas.append("SkillTreeReadOnly.cs ainda tem `%s` — a janela separada nao foi aposentada" % trecho)

    fecha = _corpo(src_readonly, "internal static void Close()")
    if fecha is None:
        falhas.append("nao achei o `Close()` da sessao read-only (nao da para provar que a sessao termina)")
    elif "End()" not in fecha:
        falhas.append("o `Close()` da sessao read-only NAO chama `End()` — o estado read-only ficaria vivo")

    if "AjustarZOrder" in _efetivo(src_plugin):
        falhas.append("Plugin.cs ainda tem `AjustarZOrder` — o config da janela separada nao foi retirado")

    # Os alicerces que FICAM (MANTER do cartao)
    if "CharacterMenusManager.CloseSkillTreeMenu" not in _efetivo(src_patches):
        falhas.append("Patches.cs perdeu o gancho de `CloseSkillTreeMenu` (o sinal de fechamento que "
                      "o cartao manda MANTER)")
    gancho = _corpo_da_classe(src_patches, CLASSE_GANCHO)
    if "SkillTreesTab.Ensure" not in gancho:
        falhas.append("o postfix de `CharacterMenusManager.OpenWindow` nao chama `SkillTreesTab.Ensure` "
                      "(a reinjecao idempotente da aba)")
    return falhas


# ------------------------------------------------------------ plantio de defeitos ---

_ANCORA_BARD = """                    if (tipo == SkillType.Bard)
                    {
                        continue;
                    }

"""
_DEFEITO_BARD = ""

_ANCORA_ARRAY = """                MenuTab[] novo = new MenuTab[antigo.Length + 1];
                Array.Copy(antigo, novo, antigo.Length);
                novo[antigo.Length] = nova;
                mgr.MenuTabs = novo;"""
_DEFEITO_ARRAY = """                // DEFEITO: a aba fica FORA do array publico MenuTabs (GetNextActiveTab -> "Tabbing broke")
                MenuTab[] novo = antigo;"""

_ANCORA_PREDICADO = """                if (s == null || s.SkillType != tipo || s.Disabled || s.DontIncludeInTree)"""
_DEFEITO_PREDICADO = """                if (s == null || s.SkillType != tipo)"""


def fonte_com_bard_incluido(src=None):
    """O MESMO fonte com o FILTRO do Bard removido (a premissa falsa do cartao), em memoria."""
    texto = fonte(caminho_aba()) if src is None else src
    if _ANCORA_BARD not in texto:
        return texto
    return texto.replace(_ANCORA_BARD, _DEFEITO_BARD, 1)


def fonte_com_aba_fora_do_array(src=None):
    """O MESMO fonte com a aba FORA do array publico MenuTabs (ponto 8: "Tabbing broke")."""
    texto = fonte(caminho_aba()) if src is None else src
    if _ANCORA_ARRAY not in texto:
        return texto
    return texto.replace(_ANCORA_ARRAY, _DEFEITO_ARRAY, 1)


def fonte_com_predicado_fraco(src=None):
    """O MESMO fonte sem `Disabled`/`DontIncludeInTree` (o defeito do SkillsByTreeDict)."""
    texto = fonte(caminho_aba()) if src is None else src
    if _ANCORA_PREDICADO not in texto:
        return texto
    return texto.replace(_ANCORA_PREDICADO, _DEFEITO_PREDICADO, 1)
