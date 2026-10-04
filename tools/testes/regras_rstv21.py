#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rstv21.py - RSTV-21: o botao 'Skills' do modal 'Remove Skill Trees' abre uma JANELA
read-only PROPRIA (todas as arvores), sem depender do inventario.

O DEFEITO QUE ESTA BIBLIOTECA TRAVA (log do jogo, 03/10 - evidencia)
--------------------------------------------------------------------
O botao 'Skills' injetado no CABECALHO do modal 'Remove Skill Trees' aparecia e, ao clicar, NAO
abria nada:

    RSTV-20: clique no botao Skills do modal -> Raven (nivel 2) na aba All Trees do inventario.
    RSTV-16: abrindo o inventario (CharacterMenusManager.OpenCharacterMenu) ...
    RSTV-16: o inventario nao abriu em 5 s (CharacterMenusManager seguiu inativo) - o pedido foi
    descartado.

Causa: o `onClick` chamava `SkillTreesTab.Abrir`, que abre o INVENTARIO e so entao seleciona a aba.
O modal vive na tela de PARTY SELECT, onde `CharacterMenusManager.OpenCharacterMenu` NAO abre (o
personagem nao esta em `AllMyCharacters`) - o pedido caia no teto de 5 s e morria em silencio.

O QUE A RSTV-21 FAZ (as regras viram checagem)
----------------------------------------------
1. A ABERTURA: `SkillTreesTab.AbrirJanela(alvo, contexto, dono)` e o caminho do modal. Ele NAO
   chama `OpenCharacterMenu` nem `SelectButtonAndInvoke` — abre a JANELA PROPRIA
   (`SkillTreesWindow.Garantir`), inicia a sessao read-only e MOSTRA o painel (`Mostrar`).
   O `Abrir` do inventario (RSTV-16) NAO muda: o botao da tela Party, o HUD e o F12 seguem nele.
2. A JANELA (`SkillTreesWindow.cs`): raiz propria `DontDestroyOnLoad` com `Canvas` em
   `RenderMode.ScreenSpaceOverlay` ACIMA do canvas do jogo (`sortingOrder`), `GraphicRaycaster` e
   `CanvasScaler` COPIADO do jogo (mesma escala da UI). Fundo que CONSOME o clique (nada atras e
   acionado por engano). O fundo, a moldura, o titulo e o botao fechar nascem dos MOLDES NATIVOS do
   proprio modal (`Fade`/`PanelBackground`/`TitleText`/`CancelButton`) — nada de cor solida feia.
3. O CICLO DE VIDA: a janela segue o DONO (a janela do jogo que pediu a visao). `DonoVivo` exige o
   dono em cena; `Atualizar` FECHA a janela quando o dono sai (o jogador fechou o modal) — a raiz e
   `DontDestroyOnLoad` e nao pode ficar pendurada na proxima tela.
4. O TOOLTIP: a janela e um Canvas PROPRIO acima de tudo, mas o tooltip de skill vive no noh
   'Tooltips / Popups' do GUI Manager (Canvas proprio, ordem 0 — medido no prefab `level1`). Sem
   mover o tooltip para DENTRO da janela (`gui.tooltip.transform.SetParent` + `SetAsLastSibling`)
   o hover do noh mostraria um tooltip ILEGIVEL atras do fundo. O pai/indice antigos sao guardados
   e o tooltip e DEVOLVIDO ao jogo no fechar (`RestaurarTooltip`).
5. O READ-ONLY: na JANELA nao existe nenhum caminho de ESCRITA no personagem. A sessao read-only e
   aberta (`ReadOnlySession.Begin`) e o `SkillTreeItemTogglePatch` barra o clique (RSTV-16); nenhum
   arquivo novo toca `SkillsToAdd`/`AcceptSkillChanges`/`ResetSkillPoints`/`SavedMap`.
6. O HOSPEDEIRO do painel muda: `ConstruirPainel` desvia para `ConstruirPainelNaJanela` quando
   `_modoJanela`, `DeviaEstarVisivel` passa a valer pela janela, o `Tick` chama
   `SkillTreesWindow.Atualizar`, a `Underline` (que e da barra de abas) NAO e mexida no modo janela,
   e a fileira de classes deixa de exigir o `CharacterMenusManager` vivo.

COMO O ESPERADO E OBTIDO
------------------------
Fontes lidos AO VIVO (`RoguelikeSkillTreeVisualizer/{SkillTreesTab,SkillTreesWindow,
RemovalWindowSkillsButton}.cs`), recorte ESTRUTURAL por chaves (`recorte.corpo_do_metodo`) e texto
SEM comentario (`recorte.codigo_efetivo`). Os MODELOS PUROS transcrevem as duas decisoes:
`host_escolhido`/`abre_inventario` (o modo janela NAO abre inventario) e
`janela_visivel`/`deve_fechar` (a janela segue o dono). Os plantios devolvem o MESMO fonte com o
defeito reinjetado, em memoria — a isca `cp_rstv21_*` prova que as checagens reprovam.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import recorte as rec

# Assinaturas exatas lidas do fonte. Se um nome mudar, a checagem REPROVA dizendo qual sumiu.
ABRIR_JANELA = "internal static void AbrirJanela(Character alvo, ReadOnlyContext contexto, Transform dono)"
ABRIR_ABA = "internal static void Abrir(Character alvo, ReadOnlyContext contexto)"
DEVIA_ESTAR_VISIVEL = "private static bool DeviaEstarVisivel()"
TICK = "internal static void Tick()"
AJUSTAR_UNDERLINE = "private static void AjustarUnderline(bool ligado)"
SAIR_DO_MODO_JANELA = "private static void SairDoModoJanela()"
GARANTIR = "internal static RectTransform Garantir(Transform dono)"
ATUALIZAR = "internal static void Atualizar()"
DONO_VIVO = "internal static bool DonoVivo()"
FECHAR = "internal static void Fechar()"
ELEVAR_TOOLTIP = "private static void ElevarTooltip()"
RESTAURAR_TOOLTIP = "private static void RestaurarTooltip()"
ON_CLICK_MODAL = "private static void OnClick()"
SELECIONAR_E_MOSTRAR = "internal static void SelecionarEMostrar()"
MOSTRAR = "private static void Mostrar()"
CONSTRUIR_PAINEL = "private static void ConstruirPainel()"
CONSTRUIR = "private static RectTransform Construir(Transform dono)"


# RSTV-21R: o AVISO de fechamento da janela. `SkillTreesWindow.Fechou` e' disparado pelo `Fechar` (o
# funil do botao Close E do `Atualizar`); o hospedeiro (`SkillTreesTab`) se inscreve nele para largar o
# modo janela. Sem o disparo/inscricao/reset, o `_modoJanela` fica pendurado depois do fechamento.
FECHOU_CAMPO = "internal static Action Fechou;"
AO_FECHAR_JANELA = "private static void AoFecharJanela()"
MONTAR_BOTAO_FECHAR = "private static void MontarBotaoFechar(RectTransform cabecalho, Button molde, TextMeshProUGUI moldeTexto)"

# O nome do GameObject do FUNDO da janela: e a Image DELE que tem de consumir o clique (a moldura
# tambem tem `raycastTarget = true`, entao o texto solto nao prova nada).
BACKDROP_NOME = "RstvWindowBackdrop"

# APIs de ESCRITA no personagem: proibidas em TODO arquivo tocado pela RSTV-21.
ESCRITAS_PROIBIDAS = (
    "SkillsToAdd",
    "SkillsRemoved",
    "AcceptSkillChanges",
    "ResetSkillPoints",
    "SavedMap",
    "AddSkills(",
    "RemoveSkills(",
    "BeginRespec",
)

CANVAS_MARCAS = (
    ("RenderMode.ScreenSpaceOverlay", "o Canvas em OVERLAY proprio (acima do canvas do jogo)"),
    ("DontDestroyOnLoad", "a raiz DontDestroyOnLoad (reusada entre aberturas)"),
    ("GraphicRaycaster", "o GraphicRaycaster (a janela recebe clique/projecao)"),
    ("CanvasScaler", "o CanvasScaler copiado do jogo (mesma escala da UI)"),
    ("sortingOrder", "a ordenacao ACIMA do canvas do jogo"),
)


# ------------------------------------------------------------------ caminhos ---

def _dir_mod():
    return os.path.join(arc.raiz_do_repo(), "RoguelikeSkillTreeVisualizer")


def caminho_tab():
    return os.path.join(_dir_mod(), "SkillTreesTab.cs")


def caminho_janela():
    return os.path.join(_dir_mod(), "SkillTreesWindow.cs")


def caminho_remocao():
    return os.path.join(_dir_mod(), "RemovalWindowSkillsButton.cs")


def fonte(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def _efetivo(src):
    return rec.codigo_efetivo(src)


def _corpo(src, assinatura):
    return rec.corpo_do_metodo(_efetivo(src), assinatura)


# ------------------------------------------------------------------ amarras ---
# Helpers que AMARRAM uma decisao a uma variavel/relacao do fonte, em vez de procurar um texto solto.
# Sao eles que impedem a checagem de "passar" pelo token errado (a moldura no lugar do fundo, o nome
# do metodo no lugar do comportamento).


def _var_imagem_do_fundo(corpo):
    """O nome da variavel que guarda a `Image` do FUNDO (`RstvWindowBackdrop`), ou None.

    O FUNDO e montado por `new GameObject("RstvWindowBackdrop", ..., typeof(Image))` e a Image vem
    de `<fundo>.GetComponent<Image>()`. E essa variavel (nao a `Image` da moldura) que tem de
    consumir o clique.
    """
    m = re.search(r'(\w+)\s*=\s*new GameObject\(\s*"' + re.escape(BACKDROP_NOME) + r'"', corpo)
    if not m:
        return None
    mimg = re.search(r'(\w+)\s*=\s*' + re.escape(m.group(1)) + r'\.GetComponent<Image>\(\)', corpo)
    return mimg.group(1) if mimg else None


def _fundo_consome_clique(corpo):
    """True/False/None: a Image do FUNDO tem `raycastTarget = true`? None = nao achei o fundo."""
    m = re.search(r'(\w+)\s*=\s*new GameObject\(\s*"' + re.escape(BACKDROP_NOME) + r'"', corpo)
    if not m:
        return None
    fundo = re.escape(m.group(1))
    img = _var_imagem_do_fundo(corpo)
    if img is not None:
        return bool(re.search(r'\b' + re.escape(img) + r'\.raycastTarget\s*=\s*true\b', corpo))
    # Forma encadeada (sem variavel intermediaria): `<fundo>.GetComponent<Image>().raycastTarget`.
    return bool(re.search(fundo + r'\.GetComponent<Image>\(\)\.raycastTarget\s*=\s*true\b', corpo))


def _campos_do_tooltip(elevar):
    """(campo_pai, campo_sibling) que o `ElevarTooltip` GUARDA, ou (None, None).

    No reparent (RSTV-22), o `ElevarTooltip` guarda o PAI antigo (`tooltip.parent`) e o INDICE
    (`tooltip.GetSiblingIndex()`) antes de mover o tooltip para dentro da janela.
    """
    m_pai = re.search(r'(\w+)\s*=\s*tooltip\.parent\b', elevar or "")
    m_sib = re.search(r'(\w+)\s*=\s*tooltip\.GetSiblingIndex\(\)', elevar or "")
    return (m_pai.group(1) if m_pai else None, m_sib.group(1) if m_sib else None)


def _tooltip_simetrico(elevar, restaurar):
    """True se o `ElevarTooltip` guarda o pai/indice antigos E o `RestaurarTooltip` os DEVOLVE.

    Devolve (ok, motivo): a checagem prende a SIMETRIA (guardar -> devolver), nao a mera presenca
    dos nomes. Um `RestaurarTooltip` virado no-op ou um `ElevarTooltip` que nao guarda reprovam.
    """
    if elevar is None:
        return False, "nao achei o `ElevarTooltip`"
    pai, sib = _campos_do_tooltip(elevar)
    if not pai or not sib:
        return False, ("`ElevarTooltip` nao guarda o PAI/INDICE antigos do tooltip "
                       "(tooltip.parent / tooltip.GetSiblingIndex) — o ajuste nao teria como ser "
                       "desfeito ao fechar")
    if restaurar is None:
        return False, "nao ha `RestaurarTooltip` — o tooltip ficaria preso na janela depois de fechar"
    if not re.search(r'SetParent\s*\(\s*' + re.escape(pai) + r'\b', restaurar):
        return False, ("`RestaurarTooltip` nao devolve o tooltip ao PAI guardado por `ElevarTooltip` "
                       "(`SetParent(%s)`) — o tooltip ficaria preso na janela" % pai)
    return True, None


def _constroi_painel_sob_guarda(mostrar):
    """True se o `Mostrar` chama `ConstruirPainel()` DENTRO do ramo `if (_painel == null)`.

    Amarra o PAR (guarda -> chamada), NAO os dois tokens soltos. O `Mostrar` tem DOIS
    `if (_painel == null)`: o PRIMEIRO envolve `ConstruirPainel();` (montar o painel se ele ainda
    nao existe) e o SEGUNDO apenas SAI do metodo se `_painel` continuar nulo depois da construcao.
    Exigir o token `_painel == null` em QUALQUER lugar do corpo era satisfeito pelo SEGUNDO `if`:
    bastava remover a guarda SO da chamada (deixando `ConstruirPainel();` solto) que a checagem
    continuava verde, embora o painel fosse reconstruido a cada `Mostrar` (perda de estado). A
    regex exige o `if (_painel == null)` IMEDIATAMENTE antes da chamada, com a chamada como
    primeiro statement do ramo guardado (com ou sem chaves).
    """
    if not mostrar:
        return False
    return bool(re.search(
        r'if\s*\(\s*_painel\s*==\s*null\s*\)\s*(?:\{\s*)?ConstruirPainel\s*\(\s*\)\s*;',
        mostrar))


def _condicao_do_if(texto, pos_if):
    """O texto entre os parenteses do `if` que comeca em `pos_if` (casamento de parenteses).

    O `DonoVivo()` tem parenteses PROPRIOS dentro da condicao; uma janela `[^)]*` pararia no
    primeiro `)` e cortaria o resto. Aqui a condicao sai do CASAMENTO dos parenteses.
    """
    i = texto.find("(", pos_if)
    if i < 0:
        return None
    nivel = 0
    for j in range(i, len(texto)):
        c = texto[j]
        if c == "(":
            nivel += 1
        elif c == ")":
            nivel -= 1
            if nivel == 0:
                return texto[i + 1:j]
    return None


def _ramo_do_if(texto, pos_if):
    """O corpo do `if`: o bloco `{ ... }` do ramo, ou o statement unico ate o `;`."""
    i = texto.find("(", pos_if)
    if i < 0:
        return None
    nivel, fim = 0, None
    for j in range(i, len(texto)):
        c = texto[j]
        if c == "(":
            nivel += 1
        elif c == ")":
            nivel -= 1
            if nivel == 0:
                fim = j
                break
    if fim is None:
        return None
    k = fim + 1
    while k < len(texto) and texto[k].isspace():
        k += 1
    if k < len(texto) and texto[k] == "{":
        return rec.bloco_balanceado(texto, k)
    ponto = texto.find(";", k)
    return texto[k:ponto + 1] if ponto >= 0 else texto[k:]


def _fecha_quando_dono_sai(atualizar):
    """(ok, motivo): o `Atualizar` fecha a janela SO quando a raiz esta ligada E o dono SAIU.

    O ACHADO da RSTV-21CR: prender a polaridade so pela PRESENCA do token `DonoVivo()` era oco —
    inverter `!DonoVivo()` -> `DonoVivo()` passava em BRANCO. Aqui a o `if` que leva ao `Fechar()`
    tem de exigir `!DonoVivo()` (dono FORA de cena) NA MESMA condicao que a raiz ligada
    (`_root.activeSelf`) e nao nula (`_root != null`). Sem a negacao, `Fechar()` roda com o modal
    ABERTO e a janela (`DontDestroyOnLoad`) fica PENDURADA quando ele fecha — os dois lados do
    defeito. Sem `_root.activeSelf`, o gatilho dispara com a janela ja fechada.
    """
    if not atualizar:
        return False, "nao achei o `Atualizar`"
    for m in re.finditer(r'\bif\s*\(', atualizar):
        cond = _condicao_do_if(atualizar, m.start())
        if cond is None or "DonoVivo" not in cond:
            continue
        ramo = _ramo_do_if(atualizar, m.start())
        if ramo is None or not re.search(r'\bFechar\s*\(\s*\)', ramo):
            continue
        if not re.search(r'!\s*DonoVivo\s*\(\s*\)', cond):
            return False, (
                "`Atualizar` chama `Fechar()` com o dono VIVO — a POLARIDADE do gatilho esta "
                "invertida (`DonoVivo()` em vez de `!DonoVivo()`): a janela fecharia com o modal "
                "ABERTO e ficaria pendurada quando o DONO saisse de cena")
        if not re.search(r'_root\s*!=\s*null', cond):
            return False, (
                "`Atualizar` fecha pelo dono mas SEM exigir a raiz montada (`_root != null`) — o "
                "gatilho nao esta preso a janela")
        if not re.search(r'_root\.activeSelf', cond):
            return False, (
                "`Atualizar` fecha pelo dono mas SEM exigir a raiz LIGADA (`_root.activeSelf`) — "
                "com a janela ja fechada o dono fora de cena dispararia o fechamento de novo")
        return True, None
    return False, (
        "`Atualizar` nao tem nenhum `if` que leve o DONO FORA de cena (`!DonoVivo()`) ao `Fechar()` "
        "— a janela nao se fecharia quando o dono saisse e ficaria pendurada na proxima tela")



# ------------------------------------------------------------- modelos puros ---
#
# A DECISAO DO HOSPEDEIRO. O modo janela NAO abre o inventario; o modo aba (RSTV-16) abre.
# Era exatamente a confusao dos dois que produzia o clique morto do modal.

HOST_JANELA = "janela"
HOST_ABA = "aba"


def host_escolhido(modo_janela):
    """O hospedeiro da visao: a JANELA propria (modal, sem inventario) ou a ABA do inventario."""
    return HOST_JANELA if modo_janela else HOST_ABA


def abre_inventario(host):
    """So o hospedeiro ABA abre o `CharacterMenusManager`. A janela propria NAO abre nada do menu."""
    return host == HOST_ABA


def host_com_inventario_sempre(modo_janela):
    """O DEFEITO: qualquer hospedeiro abre o inventario (a causa raiz do clique morto)."""
    return HOST_ABA


#
# O CICLO DE VIDA DA JANELA: ela so esta visivel com a raiz ligada E o DONO vivo; e se o dono
# sai de cena, ela tem de ser FECHADA (a raiz e DontDestroyOnLoad).


def janela_visivel(raiz_ativa, dono_vivo):
    return bool(raiz_ativa) and bool(dono_vivo)


def deve_fechar(raiz_ativa, dono_vivo):
    """O `Atualizar`: raiz ligada + dono FORA de cena => fechar."""
    return bool(raiz_ativa) and not bool(dono_vivo)


#
# O RESET DO MODO JANELA (RSTV-21R): a janela avisa quando FECHA (o botao Close OU o `Atualizar` vendo o
# dono sair) e o hospedeiro larga o `_modoJanela` nesse aviso. Sem o reset o flag fica PENDURADO em
# `true` ate um ponto de entrada chamar `SairDoModoJanela` — foi o defeito da RSTV-21A.


def modo_janela_apos_fechar(modo_janela_ativo, reset_ao_fechar):
    """O `_modoJanela` depois que a janela FECHOU: com o reset volta a False; sem ele fica PENDURADO."""
    return False if reset_ao_fechar else bool(modo_janela_ativo)


def modo_janela_sem_reset(modo_janela_ativo):
    """O DEFEITO do RSTV-21A: a janela fecha e ninguem larga o modo — o flag fica pendurado `true`."""
    return bool(modo_janela_ativo)


def reset_ao_fechar_ok(callback_inscrito, fechar_avisa, reseta_no_aviso):
    """A CORRENTE INTEIRA do reset: (1) o `Fechar` AVISA, (2) o hospedeiro esta INSCRITO e (3) o aviso
    ZERA o `_modoJanela`. Faltando um elo, o modo nao e largado em ALGUM caminho de fechamento."""
    return bool(callback_inscrito) and bool(fechar_avisa) and bool(reseta_no_aviso)


# ------------------------------------------------------------------ checagens ---

def falhas_do_abrirjanela(src_tab):
    """O caminho do modal: abre a JANELA, nunca o inventario. Lista vazia = de pe."""
    falhas = []

    abrir_janela = _corpo(src_tab, ABRIR_JANELA)
    if abrir_janela is None:
        return ["nao achei %s no SkillTreesTab.cs" % ABRIR_JANELA]

    for trecho, rotulo in (
            ("SkillTreesWindow.Garantir(", "criar/garantir a JANELA propria (SkillTreesWindow.Garantir)"),
            ("IniciarSessaoReadOnly(", "abrir a SESSAO read-only"),
            ("Mostrar(", "mostrar o painel (Mostrar)"),
            ("_modoJanela = true", "entrar no modo JANELA (_modoJanela = true)"),
    ):
        if trecho not in abrir_janela:
            falhas.append("AbrirJanela nao faz %s (trecho %r)" % (rotulo, trecho))

    # O PONTO CENTRAL: o caminho do modal NAO pode abrir o inventario nem selecionar a aba.
    if "OpenCharacterMenu" in abrir_janela:
        falhas.append("AbrirJanela chama `OpenCharacterMenu` — o caminho do modal NAO pode abrir o "
                      "inventario (era exatamente o clique morto na tela de Party Select)")
    if "SelectButtonAndInvoke" in abrir_janela:
        falhas.append("AbrirJanela usa `SelectButtonAndInvoke` — a janela propria nao tem aba")

    # O `Abrir` do inventario (RSTV-16) continua existindo e continua abrindo o menu.
    abrir_aba = _corpo(src_tab, ABRIR_ABA)
    if abrir_aba is None:
        falhas.append("nao achei %s no SkillTreesTab.cs (o caminho do inventario nao pode sumir)" % ABRIR_ABA)
    elif "OpenCharacterMenu()" not in abrir_aba:
        falhas.append("`Abrir` perdeu o `menu.OpenCharacterMenu()` — a aba do inventario (RSTV-16) "
                      "regrediu")

    return falhas


def falhas_do_desvio_do_hospedeiro(src_tab):
    """O painel passa a ter DOIS hospedeiros e a vida da visao muda com o modo. Lista vazia = de pe."""
    falhas = []
    efetivo = _efetivo(src_tab)

    if "ConstruirPainelNaJanela" not in efetivo:
        falhas.append("nao ha `ConstruirPainelNaJanela` — o painel nao sabe nascer sob a janela propria")
    if "SkillTreesWindow.Conteudo" not in efetivo:
        falhas.append("o painel nao usa a area de conteudo da janela (`SkillTreesWindow.Conteudo`)")

    construir = _corpo(src_tab, CONSTRUIR_PAINEL)
    if construir is None:
        falhas.append("nao achei o `ConstruirPainel`")
    elif "ConstruirPainelNaJanela()" not in construir or "_modoJanela" not in construir:
        falhas.append("`ConstruirPainel` nao desvia para a janela quando `_modoJanela`")

    devia = _corpo(src_tab, DEVIA_ESTAR_VISIVEL)
    if devia is None:
        falhas.append("nao achei o `DeviaEstarVisivel`")
    elif "_modoJanela" not in devia or "SkillTreesWindow.Aberta" not in devia:
        falhas.append("`DeviaEstarVisivel` nao le a janela no modo janela (SkillTreesWindow.Aberta)")

    tick = _corpo(src_tab, TICK)
    if tick is None:
        falhas.append("nao achei o `Tick`")
    elif "SkillTreesWindow.Atualizar()" not in tick:
        falhas.append("`Tick` nao chama `SkillTreesWindow.Atualizar()` — a janela nao se fecharia "
                      "quando o dono sai de cena")

    ajuste = _corpo(src_tab, AJUSTAR_UNDERLINE)
    if ajuste is None:
        falhas.append("nao achei o `AjustarUnderline`")
    elif "_modoJanela" not in ajuste:
        falhas.append("`AjustarUnderline` mexe na Underline das abas mesmo no modo janela")

    if _corpo(src_tab, SAIR_DO_MODO_JANELA) is None:
        falhas.append("nao ha `SairDoModoJanela` — trocar de host (janela -> aba) nao desmontaria o painel")
    else:
        # A troca de host so acontece se os DOIS pontos de entrada que ASSUMEM a visao (o `Abrir` do
        # inventario e o `SelecionarEMostrar` do clique da aba) CHAMAREM `SairDoModoJanela()`. Sem a
        # chamada, o painel da janela ficaria preso no host errado quando a aba retomasse a visao.
        for assinatura, rotulo in ((ABRIR_ABA, "`Abrir`"),
                                   (SELECIONAR_E_MOSTRAR, "`SelecionarEMostrar`")):
            chamador = _corpo(src_tab, assinatura)
            if chamador is None:
                falhas.append("nao achei %s (ponto de entrada que tem de sair do modo janela)" % rotulo)
            elif "SairDoModoJanela()" not in chamador:
                falhas.append("%s nao chama `SairDoModoJanela()` — a visao da janela nao seria "
                              "desmontada quando a aba assume (o painel ficaria preso no host errado)"
                              % rotulo)

    # O `Mostrar` so garante o painel se CONSTRUIR quando ele ainda nao existe: sem a chamada a
    # `ConstruirPainel()` o painel NUNCA nasceria (`_painel` continuaria nulo e a janela abriria vazia).
    # E a chamada tem de estar SOB a guarda `if (_painel == null)` — os DOIS tokens soltos nao bastam:
    # o metodo tem um SEGUNDO `if (_painel == null)` (para sair se o painel veio nulo), entao so o
    # PAR guarda->chamada prova que o painel nao e reconstruido a cada `Mostrar`.
    mostrar = _corpo(src_tab, MOSTRAR)
    if mostrar is None:
        falhas.append("nao achei o `Mostrar`")
    elif "ConstruirPainel()" not in mostrar:
        falhas.append("`Mostrar` nao chama `ConstruirPainel()` — com `_painel == null` o painel nunca "
                      "seria montado (a janela abriria vazia)")
    elif not _constroi_painel_sob_guarda(mostrar):
        falhas.append("`Mostrar` chama `ConstruirPainel()` SEM a guarda `if (_painel == null)` "
                      "IMEDIATAMENTE antes da chamada — o painel seria reconstruido a cada Mostrar "
                      "(perderia estado)")

    return falhas


def falhas_da_janela(src_janela):
    """A janela propria e o ciclo de vida dela. Lista vazia = de pe."""
    falhas = []
    efetivo = _efetivo(src_janela)

    for trecho, rotulo in CANVAS_MARCAS:
        if trecho not in efetivo:
            falhas.append("a janela nao tem %s (trecho %r)" % (rotulo, trecho))

    # O FUNDO da janela — e NAO a moldura — tem de CONSUMIR o clique (senao o modal atras seria
    # acionado por engano). A moldura TAMBEM tem `raycastTarget = true`, entao o texto solto
    # `"raycastTarget = true"` nao prova nada: a checagem amarra a Image DO FUNDO (`RstvWindowBackdrop`).
    corpo_construir = _corpo(src_janela, CONSTRUIR)
    fundo_consome = _fundo_consome_clique(corpo_construir) if corpo_construir else None
    if fundo_consome is None:
        falhas.append("a janela nao monta o FUNDO (%r) — sem ele nada barra o clique que atravessa "
                      "a janela" % BACKDROP_NOME)
    elif not fundo_consome:
        fundo_img = _var_imagem_do_fundo(corpo_construir) or "GetComponent<Image>()"
        falhas.append("o FUNDO da janela (%r) nao consome o clique (`%s.raycastTarget = true`) — o "
                      "modal atras poderia ser acionado por um clique na janela"
                      % (BACKDROP_NOME, fundo_img))

    garantir = _corpo(src_janela, GARANTIR)
    if garantir is None:
        falhas.append("nao achei o `Garantir`")
    elif "Conteudo" not in garantir and "_conteudo" not in garantir:
        falhas.append("`Garantir` nao devolve a area de conteudo da janela")

    dono = _corpo(src_janela, DONO_VIVO)
    if dono is None:
        falhas.append("nao achei o `DonoVivo`")
    elif "activeInHierarchy" not in dono:
        falhas.append("`DonoVivo` nao exige o dono EM CENA (`activeInHierarchy`) — a janela ficaria "
                      "pendurada depois que o modal fecha")

    atualizar = _corpo(src_janela, ATUALIZAR)
    if atualizar is None:
        falhas.append("nao achei o `Atualizar`")
    else:
        # A POLARIDADE (ACHADO da RSTV-21CR): nao basta `DonoVivo()`/`Fechar()` aparecerem no corpo.
        # O `if` que leva ao `Fechar()` tem de exigir `!DonoVivo()` NA MESMA condicao que a raiz
        # ligada — senao inverter a polaridade (fechar com o dono VIVO) passava em branco.
        ok, motivo = _fecha_quando_dono_sai(atualizar)
        if not ok:
            falhas.append(motivo)

    fechar = _corpo(src_janela, FECHAR)
    if fechar is None:
        falhas.append("nao achei o `Fechar`")
    elif "SetActive(false)" not in fechar:
        falhas.append("`Fechar` nao desliga a raiz (`SetActive(false)`)")

    elevar = _corpo(src_janela, ELEVAR_TOOLTIP)
    if elevar is None or "GUIManager" not in elevar:
        falhas.append("`ElevarTooltip` nao resolve o tooltip pelo `GUIManager`")

    # BUG DE 03/10 (a janela ficava INVISIVEL): a 1a versao dava `overrideSorting` no canvas RAIZ da UI
    # ('GUI Manager', que contém o modal) e o jogo INTEIRO passava a desenhar acima da janela — o clique
    # rodava, a janela era montada no log e nada aparecia. A solucao certa e REPARENTAR o tooltip para
    # DENTRO da janela (`gui.tooltip.transform.SetParent`), sem tocar em ordenacao nenhuma.
    if elevar is not None:
        if "overrideSorting" in elevar:
            falhas.append("`ElevarTooltip` ainda da `overrideSorting` — erguer o canvas RAIZ esconde a "
                          "janela atras do modal (o bug 'botao morto' de 03/10)")
        if "SetParent" not in elevar:
            falhas.append("`ElevarTooltip` nao REPARENTA o tooltip para dentro da janela (SetParent) — "
                          "sem isso ele fica atras do fundo")

    if "RestaurarTooltip" not in efetivo:
        falhas.append("nao ha `RestaurarTooltip` — a ordenacao do tooltip do jogo ficaria alterada "
                      "depois de fechar a janela")
    else:
        # A SIMETRIA: nao basta `ElevarTooltip`/`RestaurarTooltip` existirem. O `ElevarTooltip` tem
        # de GUARDAR os valores antigos e o `RestaurarTooltip` tem de os DEVOLVER — um "restaurar"
        # virado no-op (ou um elevar que nao guarda) passaria na checagem por mera presenca de nome.
        restaurar = _corpo(src_janela, RESTAURAR_TOOLTIP)
        simetrico, motivo = _tooltip_simetrico(elevar, restaurar)
        if not simetrico:
            falhas.append(motivo)
    if "RestaurarTooltip()" not in (fechar or ""):
        falhas.append("`Fechar` nao restaura o canvas do tooltip")

    return falhas


def falhas_do_fechamento(src_tab, src_janela):
    """RSTV-21R: o `_modoJanela` e LARGADO nos DOIS caminhos de fechamento da janela.

    (a) o botao Close (`MontarBotaoFechar` -> `new UnityAction(Fechar)`), e
    (b) o `Atualizar`, quando o DONO sai de cena.

    Os DOIS passam pelo mesmo funil, `SkillTreesWindow.Fechar`, que dispara o aviso `Fechou`; o
    `AbrirJanela` INSCREVE `AoFecharJanela` nesse aviso e `AoFecharJanela` zera `_modoJanela`. Faltando
    qualquer elo, o flag fica PENDURADO depois do fechamento (o defeito do RSTV-21A). Lista vazia = de pe.
    """
    falhas = []

    # --- LADO DA JANELA: o campo do aviso, o disparo no `Fechar` e o elo do `Atualizar`. ---
    if FECHOU_CAMPO not in _efetivo(src_janela):
        falhas.append("a janela nao tem o AVISO de fechamento (`%s`) — o hospedeiro nunca saberia que "
                      "ela fechou, e o `_modoJanela` ficaria pendurado" % FECHOU_CAMPO)

    fechar = _corpo(src_janela, FECHAR)
    if "Fechou()" not in fechar:
        falhas.append("`Fechar` NAO dispara o aviso `Fechou()` — nenhum dos dois caminhos de fechamento "
                      "(botao Close nem dono fora) largaria o `_modoJanela`")
    elif not re.search(r'if\s*\(\s*fechou\b[^)]*Fechou\s*!=\s*null\s*\)', fechar):
        falhas.append("`Fechar` dispara `Fechou()` sem exigir que a janela tenha fechado de VERDADE (a "
                      "guarda do flag `fechou`) — o hospedeiro largaria o modo com a janela ainda aberta")

    # (a) O BOTAO CLOSE: o clique tem de chamar o MESMO `Fechar` (o funil do aviso).
    botao = _corpo(src_janela, MONTAR_BOTAO_FECHAR)
    if not re.search(r'AddListener\s*\(\s*new\s+UnityAction\s*\(\s*Fechar\s*\)\s*\)', botao):
        falhas.append("o botao Close nao chama `Fechar` (`onClick.AddListener(new UnityAction(Fechar))`) "
                      "— o caminho do botao nao passaria pelo aviso e o `_modoJanela` ficaria pendurado")

    # (b) O DONO SAI DE CENA: o `Atualizar` tem de levar o caso ao `Fechar` (o funil do aviso).
    #     O gatilho tem de ser a POLARIDADE CERTA (`!DonoVivo()` na raiz ligada): prender so os
    #     tokens `DonoVivo()`/`Fechar()` deixava a inversao passar em branco (ACHADO da RSTV-21CR).
    atualizar = _corpo(src_janela, ATUALIZAR)
    ok, motivo = _fecha_quando_dono_sai(atualizar)
    if not ok:
        falhas.append("%s — o caminho do dono nao passaria pelo aviso" % motivo)

    # --- LADO DO HOSPEDEIRO: a INSCRICAO no aviso e o RESET do `_modoJanela`. ---
    abrir = _corpo(src_tab, ABRIR_JANELA)
    if not re.search(r'SkillTreesWindow\.Fechou\s*=\s*AoFecharJanela\s*;', abrir):
        falhas.append("`AbrirJanela` nao se INSCREVE no aviso (`SkillTreesWindow.Fechou = "
                      "AoFecharJanela`) — o `_modoJanela` nao seria largado quando a janela fechasse")
    if re.search(r'SkillTreesWindow\.Fechou\s*\+=', abrir):
        falhas.append("`AbrirJanela` ACUMULA handlers (`Fechou += ...`) em vez de ASSUMIR um unico "
                      "(`Fechou = ...`) — handlers de aberturas antigas disparariam junto")

    ao_fechar = _corpo(src_tab, AO_FECHAR_JANELA)
    if "_modoJanela = false" not in ao_fechar:
        falhas.append("`AoFecharJanela` NAO zera o `_modoJanela` — o flag ficaria PENDURADO depois do "
                      "fechamento (o defeito do RSTV-21A)")
    if "DestruirPainel()" not in ao_fechar:
        falhas.append("`AoFecharJanela` nao desmonta o painel (`DestruirPainel()`) — o painel da janela "
                      "ficaria preso no host")
    if "ReadOnlySession.End()" not in ao_fechar:
        falhas.append("`AoFecharJanela` nao encerra a sessao read-only (`ReadOnlySession.End()`)")
    if not re.search(r'if\s*\(\s*!\s*_modoJanela\s*\)\s*\{?\s*return\s*;', ao_fechar):
        falhas.append("`AoFecharJanela` nao tem a GUARDA de reentrada (`if (!_modoJanela) return`) — o "
                      "fechamento vindo do proprio `SairDoModoJanela` reentraria no aviso")

    return falhas


def falhas_do_clique_do_modal(src_remocao):
    """O onClick do botao do modal chama a JANELA, nao o `Abrir` do inventario. Lista vazia = de pe."""
    falhas = []

    efetivo = _efetivo(src_remocao)
    if "AbrirJanela" not in efetivo:
        falhas.append("o botao do modal nao chama `SkillTreesTab.AbrirJanela`")

    clique = _corpo(src_remocao, ON_CLICK_MODAL)
    if clique is None:
        return falhas + ["nao achei o `OnClick` do botao do modal"]

    if "SkillTreesTab.AbrirJanela(" not in clique:
        falhas.append("o clique nao abre pela JANELA (`SkillTreesTab.AbrirJanela`)")
    if "ReadOnlyContext.RemocaoDeArvores" not in clique:
        falhas.append("o clique perdeu o contexto `ReadOnlyContext.RemocaoDeArvores`")
    if "SkillTreesTab.Abrir(" in clique:
        falhas.append("o clique voltou a chamar `SkillTreesTab.Abrir` (o inventario) — e o clique "
                      "morto da tela de Party Select")

    return falhas


def falhas_de_escrita(srcs):
    """Nenhum arquivo da RSTV-21 pode ter caminho de ESCRITA no personagem. Lista vazia = de pe."""
    falhas = []
    for nome, src in srcs:
        efetivo = _efetivo(src)
        for proibido in ESCRITAS_PROIBIDAS:
            if proibido in efetivo:
                falhas.append("%s toca `%s` — a RSTV-21 e somente leitura de verdade" % (nome, proibido))
    return falhas


# ------------------------------------------------------------ plantio de defeitos ---

_ANCORA_CLIQUE = "                SkillTreesTab.AbrirJanela(alvo, ReadOnlyContext.RemocaoDeArvores, janela.transform);"
_DEFEITO_CLIQUE = "                SkillTreesTab.Abrir(alvo, ReadOnlyContext.RemocaoDeArvores);"

_ANCORA_ABRIR_JANELA = """                IniciarSessaoReadOnly();
                Mostrar();"""
_DEFEITO_ABRIR_JANELA = """                CharacterMenusManager.Instance.OpenCharacterMenu();
                IniciarSessaoReadOnly();
                Mostrar();"""

_ANCORA_CANVAS = "            UnityEngine.Object.DontDestroyOnLoad(root);"
_DEFEITO_CANVAS = "            // DEFEITO: sem raiz propria (a janela morreria com a cena)"

_ANCORA_ATUALIZAR = "                if (_root != null && _root.activeSelf && !DonoVivo())"
_DEFEITO_ATUALIZAR = "                if (_root != null && _root.activeSelf)"

_ANCORA_TOOLTIP_SETPARENT = "                tooltip.SetParent(_root.transform, true);"
_DEFEITO_TOOLTIP_SETPARENT = "                // DEFEITO: tooltip sem reparent (fica atras do fundo)"


def fonte_com_volta_ao_inventario(src=None):
    """A MESMA fonte do botao do modal, com o clique de volta no `Abrir` (o defeito original)."""
    texto = fonte(caminho_remocao()) if src is None else src
    if _ANCORA_CLIQUE not in texto:
        return texto
    return texto.replace(_ANCORA_CLIQUE, _DEFEITO_CLIQUE, 1)


def fonte_com_inventario_no_abrirjanela(src=None):
    """A MESMA fonte do SkillTreesTab, com o inventario voltando ao `AbrirJanela`."""
    texto = fonte(caminho_tab()) if src is None else src
    if _ANCORA_ABRIR_JANELA not in texto:
        return texto
    return texto.replace(_ANCORA_ABRIR_JANELA, _DEFEITO_ABRIR_JANELA, 1)


def fonte_sem_raiz_propria(src=None):
    """A MESMA fonte da janela, sem a raiz `DontDestroyOnLoad` (o canvas proprio)."""
    texto = fonte(caminho_janela()) if src is None else src
    if _ANCORA_CANVAS not in texto:
        return texto
    return texto.replace(_ANCORA_CANVAS, _DEFEITO_CANVAS, 1)


def fonte_sem_dono_no_atualizar(src=None):
    """A MESMA fonte da janela, com o `Atualizar` SEM olhar o dono (a janela nao se fecharia)."""
    texto = fonte(caminho_janela()) if src is None else src
    if _ANCORA_ATUALIZAR not in texto:
        return texto
    return texto.replace(_ANCORA_ATUALIZAR, _DEFEITO_ATUALIZAR, 1)


def fonte_com_polaridade_invertida_no_atualizar(src=None):
    """A MESMA janela com o gatilho do `Atualizar` de POLARIDADE INVERTIDA (`DonoVivo()` no lugar
    de `!DonoVivo()`): o `Fechar` roda com o dono VIVO — a janela fecharia com o modal ABERTO e
    ficaria pendurada quando ele fechasse (a raiz e `DontDestroyOnLoad`).

    E o defeito que a checagem antiga, por PRESENCA do token `DonoVivo()`, nao via (ACHADO da
    RSTV-21CR): a inversao passava em BRANCO.
    """
    texto = fonte(caminho_janela()) if src is None else src
    return _substituir_no_metodo(texto, ATUALIZAR,
                                 r'!\s*DonoVivo\s*\(\s*\)', 'DonoVivo()')


def fonte_sem_active_self_no_atualizar(src=None):
    """A MESMA janela com o `Atualizar` deixando de exigir a raiz LIGADA (`_root.activeSelf`): o
    gatilho passa a valer so pelo dono fora de cena, mesmo com a janela ja fechada.

    Tambem e o defeito que a checagem antiga, por token, nao via (ACHADO da RSTV-21CR).
    """
    texto = fonte(caminho_janela()) if src is None else src
    return _substituir_no_metodo(texto, ATUALIZAR,
                                 r'_root\.activeSelf\s*&&\s*', '')


def fonte_com_tooltip_raiz(src=None):
    """A MESMA fonte da janela, com o `ElevarTooltip` SEM reparentar o tooltip (fica atras do fundo) —
    o defeito de 03/10 que escondia a janela atras do modal."""
    texto = fonte(caminho_janela()) if src is None else src
    if _ANCORA_TOOLTIP_SETPARENT not in texto:
        return texto
    return texto.replace(_ANCORA_TOOLTIP_SETPARENT, _DEFEITO_TOOLTIP_SETPARENT, 1)


# --- plantios das LACUNAS DE COBERTURA do RSTV-21 (fundo / tooltip / entradas / Mostrar) ---------
# Cada um devolve o MESMO fonte com a mutacao reinjetada, em memoria. A prova de fogo do
# `t_rstv21_janela_propria.py` e as iscas `cp_rstv21_*` exigem que a checagem correspondente REPROVE.


def fonte_com_fundo_sem_raycast(src=None):
    """A MESMA janela com a Image do FUNDO deixando de consumir o clique — a MOLDURA continua com
    `raycastTarget = true` (era isto que a checagem antiga, por texto solto, nao via)."""
    texto = fonte(caminho_janela()) if src is None else src
    img = _var_imagem_do_fundo(_corpo(texto, CONSTRUIR) or "")
    if not img:
        return texto
    novo, n = re.subn(re.escape(img) + r'\.raycastTarget[ \t]*=[ \t]*true',
                      img + ".raycastTarget = false", texto, count=1)
    return novo if n else texto


def fonte_sem_guardar_tooltip(src=None):
    """A MESMA janela com o `ElevarTooltip` SEM guardar o PAI/INDICE antigos do tooltip — o
    `RestaurarTooltip` nao teria para onde devolver."""
    texto = fonte(caminho_janela()) if src is None else src
    pai, sib = _campos_do_tooltip(_corpo(texto, ELEVAR_TOOLTIP) or "")
    if not pai or not sib:
        return texto
    padrao = (r'(?m)^([ \t]*)' + re.escape(pai) + r'[ \t]*=[^\n]*;[ \t]*\r?\n'
              r'[ \t]*' + re.escape(sib) + r'[ \t]*=[^\n]*;')
    novo, n = re.subn(padrao, r'\1// DEFEITO: nao guarda o pai/indice antigos do tooltip',
                      texto, count=1)
    return novo if n else texto


def fonte_com_restaurar_noop(src=None):
    """A MESMA janela com o `RestaurarTooltip` virado no-op (nao devolve o tooltip ao jogo)."""
    texto = fonte(caminho_janela()) if src is None else src
    pai, sib = _campos_do_tooltip(_corpo(texto, ELEVAR_TOOLTIP) or "")
    if not pai or not sib:
        return texto
    padrao = (r'(?m)^([ \t]*)[^\n]*SetParent[ \t]*\([ \t]*' + re.escape(pai) +
              r'\b[^\n]*;')
    novo, n = re.subn(padrao, r'\1// DEFEITO: no-op (nao devolve o tooltip ao jogo)',
                      texto, count=1)
    return novo if n else texto


def _sem_sair_do_modo(texto, assinatura):
    """Remove a 1a chamada `SairDoModoJanela()` DEPOIS de `assinatura` (o ponto de entrada)."""
    i = texto.find(assinatura)
    if i < 0:
        return texto
    j = texto.find("SairDoModoJanela();", i)
    if j < 0:
        return texto
    return texto[:j] + "// DEFEITO: nao sai do modo janela" + texto[j + len("SairDoModoJanela();"):]


def fonte_sem_sair_do_modo_no_abrir(src=None):
    """A MESMA SkillTreesTab com o `Abrir` (inventario) SEM chamar `SairDoModoJanela()`."""
    texto = fonte(caminho_tab()) if src is None else src
    return _sem_sair_do_modo(texto, ABRIR_ABA)


def fonte_sem_sair_do_modo_no_selecionar(src=None):
    """A MESMA SkillTreesTab com o `SelecionarEMostrar` (clique da aba) SEM `SairDoModoJanela()`."""
    texto = fonte(caminho_tab()) if src is None else src
    return _sem_sair_do_modo(texto, SELECIONAR_E_MOSTRAR)


def fonte_sem_construir_no_mostrar(src=None):
    """A MESMA SkillTreesTab com o `Mostrar` SEM `ConstruirPainel()` (o painel nunca nasceria)."""
    texto = fonte(caminho_tab()) if src is None else src
    novo, n = re.subn(
        r'(?m)^([ \t]*)if[ \t]*\(_painel == null\)[ \t]*\r?\n[ \t]*\{[ \t]*\r?\n'
        r'[ \t]*ConstruirPainel\(\);[ \t]*\r?\n[ \t]*\}',
        r'\1// DEFEITO: Mostrar nao constroi o painel', texto, count=1)
    return novo if n else texto


def fonte_com_mostrar_sem_guarda(src=None):
    """A MESMA SkillTreesTab com o `Mostrar` chamando `ConstruirPainel()` SOLTO — a guarda
    `if (_painel == null)` IMEDIATAMENTE antes da chamada e removida, MAS o SEGUNDO
    `if (_painel == null) { return; }` (para sair se o painel veio nulo) CONTINUA no metodo.

    E exatamente o caso que a checagem antiga, por TOKEN SOLTO, nao pegava: os dois pedacos de
    texto (`ConstruirPainel()` e `_painel == null`) seguem presentes — o segundo satisfazia o
    `_painel == null` — embora o painel fosse reconstruido a cada `Mostrar` (perda de estado).
    """
    texto = fonte(caminho_tab()) if src is None else src
    novo, n = re.subn(
        r'(?m)^([ \t]*)if[ \t]*\(_painel == null\)[ \t]*\r?\n'
        r'[ \t]*\{[ \t]*\r?\n'
        r'[ \t]*ConstruirPainel\(\);[ \t]*\r?\n'
        r'[ \t]*\}',
        r'\1ConstruirPainel();', texto, count=1)
    return novo if n else texto



# --- plantios do FECHAMENTO (RSTV-21R): cada um reinjeta UMA quebra da corrente do reset -----------


def _substituir_no_metodo(texto, assinatura, padrao, troca):
    """Troca a 1a ocorrencia de `padrao` SO dentro do corpo do metodo `assinatura` (por chaves)."""
    i = texto.find(assinatura)
    if i < 0:
        return texto
    abre = texto.find("{", i)
    if abre < 0:
        return texto
    ini, fim = rec.faixa_bloco_balanceado(texto, abre)
    bloco = texto[ini:fim + 1]
    novo, n = re.subn(padrao, troca, bloco, count=1)
    if not n:
        return texto
    return texto[:ini] + novo + texto[fim + 1:]


def fonte_sem_aviso_no_fechar(src=None):
    """A MESMA janela com o `Fechar` SEM disparar o aviso `Fechou` (nenhum caminho largaria o modo)."""
    texto = fonte(caminho_janela()) if src is None else src
    return _substituir_no_metodo(texto, FECHAR,
                                 r'(?m)^([ \t]*)Fechou\(\);',
                                 r'\1// DEFEITO: Fechar nao avisa o fechamento')


def fonte_botao_fechar_sem_fechar(src=None):
    """A MESMA janela com o botao CLOSE sem chamar `Fechar` (o caminho do botao nao passa pelo aviso)."""
    texto = fonte(caminho_janela()) if src is None else src
    return _substituir_no_metodo(
        texto, MONTAR_BOTAO_FECHAR,
        r'(?m)^([ \t]*)componente\.onClick\.AddListener\(new UnityAction\(Fechar\)\);',
        r'\1// DEFEITO: botao Close sem o Fechar')


def fonte_sem_inscrever_fechou(src=None):
    """A MESMA SkillTreesTab com o `AbrirJanela` SEM se inscrever no aviso de fechamento."""
    texto = fonte(caminho_tab()) if src is None else src
    return _substituir_no_metodo(
        texto, ABRIR_JANELA,
        r'(?m)^([ \t]*)SkillTreesWindow\.Fechou[ \t]*=[ \t]*AoFecharJanela[ \t]*;',
        r'\1// DEFEITO: AbrirJanela nao se inscreve no aviso de fechamento')


def fonte_ao_fechar_sem_reset(src=None):
    """A MESMA SkillTreesTab com o `AoFecharJanela` SEM zerar o `_modoJanela` (o defeito do RSTV-21A)."""
    texto = fonte(caminho_tab()) if src is None else src
    return _substituir_no_metodo(
        texto, AO_FECHAR_JANELA,
        r'(?m)^([ \t]*)_modoJanela[ \t]*=[ \t]*false[ \t]*;',
        r'\1// DEFEITO: AoFecharJanela nao zera o _modoJanela')
