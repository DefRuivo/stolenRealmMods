#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rstv30.py - RSTV-30: o botao da run mudou para a BARRA DE BAIXO e nao pode PISCAR.

OS DOIS DEFEITOS DO DONO (sessao de 06/10, em jogo)
---------------------------------------------------
1. "o botao de skills nem sempre esta visivel, quando alguem toma alguma acao o botao some e depois
   reaparece";
2. "ele nao aparece enquanto estamos fora de combate".

A causa NAO era falta de injecao: o log da sessao mostra o botao injetado e, logo depois, ESCONDIDO
pelas guardas do `RunTargets.GateOk` ("GUIState ... fora da whitelist da run", "nao e o turno do
jogador", "algum personagem esta executando acao"). A visibilidade era CONSEQUENCIA do portao, e o
portao olhava o estado da batalha — entao o botao piscava a cada animacao e sumia fora do turno.

O CONSERTO (o que estas regras travam)
--------------------------------------
A. CASA NOVA (posicao): o clone deixa a linha do `Ping Button` e passa a morar na BARRA DE BAIXO, no
   container NATIVO dos botoes de inventario e de skills (`ui.skillsBtn.transform.parent` no runtime;
   `Skillbar Buttons` [526621] no prefab `Current Character UI` [556345]), no vao livre medido entre
   a linha e o `Skillbar Index Controls` [526618] (os `Up`/`Down` que chamam
   `Skillbar.IncrementSkillbarIndex`). Nada de posicao chutada: `ColocarNaLinha` MEDE
   (`GetWorldCorners` + `InverseTransformPoint`) a borda do molde, a borda direita dos nativos e a
   borda esquerda do vizinho da direita, e escreve no log cada numero usado.
B. SEM EMPURRAR NINGUEM: o clone entra com `LayoutElement.ignoreLayout = true` — o
   `HorizontalLayoutGroup` do container (medido: LIGADO no prefab) nao reflui por causa dele, e
   nenhum botao nativo muda de tamanho ou de lugar.
C. VISIBILIDADE = HUD (o fim do piscar): quem manda na presenca do botao e o proprio HUD (o clone e
   filho da barra de baixo). O portao deixou de esconder: ele decide SO o `interactable`
   (`AplicarClique`), junto com a regra NATIVA do jogo para o botao 'Skills'
   (`CurrentCharacterUI.skillsBtn.interactable`, `GUIManager.Update` l.120491). Recusando, o botao
   continua na tela e o motivo vai para o log.
D. GUARDAS COM JUSTIFICATIVA: sairam `StateAllowed` (whitelist), `IsPlayerTurnAndReady`,
   `AnyActingCharactersInBattle` e `AnyMovingCharactersInBattle`; cada guarda que ficou tem, no
   fonte, o marcador `GUARDA n` e a linha `Justificativa:` com o dano real que ela evita — guarda sem
   justificativa e' defeito, nao seguranca.
E. UM SO' REFERENCIAL NA CONTA DE POSICAO (RSTV-30F, achado da revisao RSTV-30R): `ColocarNaLinha`
   media a borda direita dos nativos com `container.InverseTransformPoint` (espaco LOCAL do
   container, cuja ORIGEM e' o PIVOR/centro) e o limite do vizinho da direita com
   `pai.InverseTransformPoint`, subtraindo a borda ESQUERDA do container — dois numeros de origens
   diferentes. Com os numeros do prefab o `vao` saia ~74.6 px em vez de ~19.0 e o clone ia parar
   DEPOIS do rotador da barra de skills (o oposto do pedido do dono). O limite passou a ser medido
   com `container.InverseTransformPoint`, o MESMO referencial de `fimDosNativos`, e a checagem 3b
   abaixo REPROVA qualquer outro receptor de `InverseTransformPoint` dentro do metodo.

COMO O ESPERADO E OBTIDO
------------------------
O fonte e' lido AO VIVO do repositorio (`RoguelikeSkillTreeVisualizer/{RunButton,RunTargets,
NativeUiHelpers}.cs`); o MODELO PURO transcreve o portao de antes e o de agora, a visibilidade de
antes e a de agora, e a conta de posicao do `ColocarNaLinha`, para mostrar o COMPORTAMENTO nos dois
lados: no cenario do dono ("outro personagem age") a regra antiga ESCONDE e a nova MANTEM, e numa
sequencia de turnos a visibilidade antiga alterna (pisca) enquanto a nova nao muda nunca.

O que estas regras NAO provam: nao executam o C# do mod (pediria a `lib/` do jogo e um harness) nem
medem em tela — a ligacao com o motor e' a ESTRUTURA do fonte (recorte por casamento de chaves) e as
medidas do prefab documentadas em `docs/RSTV-30-botao-na-barra-de-baixo.md`. Quem confirma a TELA e'
o dono (conferencia visual obrigatoria pelo DoD).
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import recorte as rec

MOD = "RoguelikeSkillTreeVisualizer"
ARQUIVO_RUN = "RunButton.cs"
ARQUIVO_TARGETS = "RunTargets.cs"
ARQUIVO_HELPERS = "NativeUiHelpers.cs"

# Assinaturas exatas lidas do fonte. Se um nome mudar, a checagem REPROVA dizendo qual sumiu.
ENSURE_INTERNAL = "private static void EnsureInternal(CurrentCharacterUI ui)"
MIRROR = "internal static void Mirror()"
APLICAR_CLIQUE = "private static void AplicarClique()"
ESPELHAR = "private static void EspelharVisibilidade()"
COLOCAR = ("private static void ColocarNaLinha(Transform container, RectTransform moldeRt, "
           "RectTransform novo, out string medidas)")
GATE_OK = "internal static bool GateOk(out string motivo)"

# ---------------------------------------------------------------- guardas do portao ---

# RSTV-30 — o que SAIU do portao (id, trecho que prova, defeito que causava). Qualquer um deles de
# volta no fonte REPROVA: foi exatamente a volta de um destes que o dono relatou.
GUARDAS_REMOVIDAS = (
    ("estado", "StateAllowed",
     "whitelist de GUIState escondia o botao em estado em que o HUD esta na tela"),
    ("turno", "IsPlayerTurnAndReady",
     "escondia o botao fora do turno do jogador (\"nao aparece fora de combate\")"),
    ("acting", "AnyActingCharactersInBattle",
     "escondia o botao quando outro personagem agia (o PISCAR do dono)"),
    ("moving", "AnyMovingCharactersInBattle",
     "escondia o botao quando outro personagem andava (o PISCAR do dono)"),
)

# RSTV-30 — cada guarda que FICOU precisa, no FONTE COM COMENTARIOS, do marcador `<rotulo>` e da
# linha `Justificativa:` com o campo que ela le, DENTRO do proprio bloco `if` da guarda (recorte
# estrutural — ver `_bloco_da_guarda`).
JUSTIFICATIVAS = (
    ("GUARDA 1 (tecnica)", "GUIManager.instance"),
    ("GUARDA 2 (escopo)", "Roguelike"),
    ("GUARDA 3 (dano real", "PingModeActive"),
    ("GUARDA 4 (dano real", "AnyUIWindowOpen"),
    ("GUARDA 5 (dano real", "PlayerState.Action"),
    ("GUARDA 6 (dano real", "SpawnPlacementActive"),
)

# Trechos que provam CADA pedaco do conserto (RSTV-30). Ausencia = reprova.
PROVAS_DA_FONTE = (
    (ARQUIVO_RUN, "ui.skillsBtn", "o molde do clone e o botao NATIVO da barra de baixo (skillsBtn)"),
    (ARQUIVO_RUN, "molde.transform.parent", "o container do clone e MEDIDO (pai do botao nativo)"),
    (ARQUIVO_RUN, "ignoreLayout = true", "o clone nao entra no fluxo do LayoutGroup do container"),
    (ARQUIVO_RUN, "GetWorldCorners", "a posicao sai de medicao (getWorldCorners)"),
    (ARQUIVO_RUN, "InverseTransformPoint", "a posicao sai de medicao (espaco local do container)"),
    (ARQUIVO_RUN, "NativeUiHelpers.ClearClickListeners(button)", "o onClick serializado e descartado"),
    (ARQUIVO_RUN, "EspelharVisibilidade()", "a visibilidade e espelhada do nativo/HUD"),
    (ARQUIVO_RUN, "AplicarClique()", "o clique e decidido em um lugar so"),
)

# O que NAO pode existir em nenhum .cs do mod (codigo efetivo, sem comentario):
#  * a receita antiga de layout (encolher a linha do original) — RSTV-30 trocou por medicao;
#  * a whitelist de estado que o portao usava.
CODIGO_PROIBIDO = (
    ("ApplySquareLayout", "a receita de layout que ENCOLHIA o botao nativo (RSTV-5/RSTV-9)"),
    ("StateAllowed", "a whitelist de GUIState que escondia o botao (removida na RSTV-30)"),
)

# ---------------------------------------------------------------- estado/cenario ---

# ESTADO DO JOGO no momento do defeito relatado, com os campos que o portao lia. Todos os nomes sao
# os do motor (`Root`/`GUIManager`); nada inventado.
CENARIO_OUTRO_AGINDO = {
    "hud_ativo": True,         # o HUD da run esta na tela (GUIManager.Update l.120485)
    "nativo_clicavel": True,   # skillsBtn.interactable (l.120491)
    "roguelike": True,
    "ping": False,
    "janela": False,
    "levelup": False,
    "em_batalha": True,
    "mira": False,
    "spawn": False,
    "estado_permitido": True,  # GUIState na whitelist antiga
    "meu_turno": False,        # o inimigo esta jogando
    "agindo": True,            # alguem esta executando acao (o piscar)
    "movendo": True,
}

# A SEQUENCIA de uma rodada de combate (o que o dono ve num turno). Usada para MEDIR o piscar: a
# visibilidade do modelo antigo alterna; a do novo nao muda nunca.
SEQUENCIA_DE_TURNO = (
    ("mapa", {"hud_ativo": True, "nativo_clicavel": True, "roguelike": True, "em_batalha": False,
              "estado_permitido": True, "meu_turno": False, "agindo": False, "movendo": False}),
    ("setup da batalha", {"hud_ativo": True, "nativo_clicavel": False, "roguelike": True,
                          "em_batalha": True, "estado_permitido": True, "meu_turno": False,
                          "agindo": False, "movendo": False, "spawn": True}),
    ("meu turno", {"hud_ativo": True, "nativo_clicavel": True, "roguelike": True, "em_batalha": True,
                   "estado_permitido": True, "meu_turno": True, "agindo": False, "movendo": False}),
    ("eu agindo", {"hud_ativo": True, "nativo_clicavel": True, "roguelike": True, "em_batalha": True,
                   "estado_permitido": True, "meu_turno": True, "agindo": True, "movendo": False}),
    ("inimigo agindo", {"hud_ativo": True, "nativo_clicavel": True, "roguelike": True,
                        "em_batalha": True, "estado_permitido": True, "meu_turno": False,
                        "agindo": True, "movendo": False}),
    ("inimigo andando", {"hud_ativo": True, "nativo_clicavel": True, "roguelike": True,
                         "em_batalha": True, "estado_permitido": True, "meu_turno": False,
                         "agindo": False, "movendo": True}),
    ("meu turno de novo", {"hud_ativo": True, "nativo_clicavel": True, "roguelike": True,
                           "em_batalha": True, "estado_permitido": True, "meu_turno": True,
                           "agindo": False, "movendo": False}),
)

PADRAO = {
    "hud_ativo": True, "nativo_clicavel": True, "roguelike": True, "ping": False, "janela": False,
    "levelup": False, "em_batalha": False, "mira": False, "spawn": False, "estado_permitido": True,
    "meu_turno": True, "agindo": False, "movendo": False,
}

# ---------------------------------------------------------------- medidas do prefab ---
# LIDAS do prefab do HUD (`resources.assets`, `Current Character UI` [556345] ->
# `Skillbar Layout PC` [526615] -> `Skillbar Buttons` [526621]) e CONVERTIDAS para o referencial em
# que o CODIGO trabalha: o espaco LOCAL do container, cuja ORIGEM e' o PIVOR dele (centro,
# `pivot (0.5,0.5)`) — e' o que `container.InverseTransformPoint` devolve. Procedencia item a item
# em `docs/RSTV-30-botao-na-barra-de-baixo.md` secao 3.
#
# A CONVERSAO (a travessia que faltava no `ColocarNaLinha` antes da RSTV-30F): um valor medido no
# espaco do PAI a partir da BORDA ESQUERDA do container passa para o espaco local somando
# `rect.xMin` (= `canto_esquerdo`). E' a MESMA travessia que o codigo ja fazia em `centro`
# (`novo.anchoredPosition = centro - cantoEsquerdo`).
PREFAB = {
    # --- leituras cruas do prefab (no referencial em que foram medidas) ---
    "largura_do_container": 111.30,   # `Skillbar Buttons`.sd.x
    "vao_do_prefab": 23.0,            # vao livre real = 134.3 - 111.3
    "limite_medido_na_borda_esquerda": 134.3,  # esquerda do rotador - esquerda do container
    # --- os MESMOS numeros no espaco LOCAL do container (origem no pivor) ---
    "canto_esquerdo": -55.65,         # rect.xMin = -largura_do_container/2
    "fim_dos_nativos": 55.65,         # borda direita dos 4 nativos (= +largura_do_container/2)
    "limite_do_vizinho": 78.65,       # esquerda do `Skillbar Index Controls` (= fim + vao)
    # --- tamanho de um botao nativo ---
    "largura_nativa": 27.02,
    "altura_nativa": 35.0,
}

# A folga de respiro nas duas bordas do vao — espelha a constante `RunButton.Margem` (2f). Nao e'
# medida do prefab: e' decisao do mod.
MARGEM = 2.0

# A PROVA (nomes de campo do prefab, lidos por UnityPy): `Skillbar Index Controls` [526618]
# ap.x=149.15 sd.x=21.70 -> borda esquerda 138.30; `Skillbar Buttons` ap.x=59.65 sd.x=111.30 ->
# borda esquerda 4.00; 138.30 - 4.00 = 134.30 (a partir da borda esquerda); 134.30 - 111.30 = 23.00
# de vao real. Os 4 botoes nativos (27.02 + espacamento ~1.07) preenchem o container, logo a borda
# direita dos nativos, no espaco local, e' +55.65.


# ------------------------------------------------------------------ caminhos/leitura ---

def _dir_mod():
    return os.path.join(arc.raiz_do_repo(), MOD)


def fonte(nome):
    """O fonte VIVO do mod (nao uma copia: a expectativa fica amarrada ao que sera compilado)."""
    with open(os.path.join(_dir_mod(), nome), encoding="utf-8") as fh:
        return fh.read()


def fontes():
    """{nome_do_arquivo: conteudo} de TODOS os .cs do mod."""
    pasta = _dir_mod()
    return {nome: fonte(nome) for nome in sorted(os.listdir(pasta)) if nome.endswith(".cs")}


def _corpo(src, assinatura):
    """O corpo do metodo COM comentarios (o recorte e por casamento de chaves, nao por janela)."""
    return rec.corpo_do_metodo(src, assinatura)


def _corpo_efetivo(src, assinatura):
    """O corpo do metodo SEM comentarios (para checar CODIGO, nao citacao)."""
    return rec.corpo_do_metodo(rec.codigo_efetivo(src), assinatura)


# ------------------------------------------------------------------ modelo puro ---

def portao_agora(c):
    """Transcricao PURA do `GateOk` DEPOIS da RSTV-30 (`True` = o clique pode abrir).

    Ordem do fonte: GUARDA 1 (GUIManager) -> 2 (Roguelike) -> level-up libera -> 3 (ping) ->
    4 (janela) -> [em batalha] 5 (mira) e 6 (posicionamento).
    """
    if not c.get("gui", True):
        return False
    if not c["roguelike"]:
        return False
    if c.get("levelup"):
        return True
    if c["ping"]:
        return False
    if c["janela"]:
        return False
    if not c["em_batalha"]:
        return True
    if c["mira"]:
        return False
    if c.get("spawn"):
        return False
    return True


def portao_antes(c):
    """Transcricao PURA do portao ANTES da RSTV-30 — a isca (as guardas removidas valendo).

    Ordem do fonte antigo: basics -> whitelist -> level-up -> ping -> janela -> [batalha]
    mira, posicionamento, turno, agindo, movendo.
    """
    if not c.get("gui", True):
        return False
    if not c["roguelike"]:
        return False
    if not c["estado_permitido"]:
        return False
    if c.get("levelup"):
        return True
    if c["ping"]:
        return False
    if c["janela"]:
        return False
    if not c["em_batalha"]:
        return True
    if c["mira"]:
        return False
    if c.get("spawn"):
        return False
    if not c["meu_turno"]:
        return False
    if c["agindo"]:
        return False
    if c["movendo"]:
        return False
    return True


def visivel_agora(c):
    """RSTV-30: a visibilidade e' a do HUD — e' ele que decide se a barra de baixo esta na tela."""
    return bool(c["hud_ativo"])


def visivel_antes(c):
    """O DEFEITO: a visibilidade era CONSEQUENCIA do portao (`Hide` quando ele recusava)."""
    return bool(c["hud_ativo"]) and portao_antes(c)


def clicavel_agora(c):
    """RSTV-30: o clique e' a regra NATIVA do jogo (l.120491) E o portao — e so' isso."""
    return bool(c["hud_ativo"]) and bool(c["nativo_clicavel"]) and portao_agora(c)


def clicavel_antes(c):
    """O clique de antes era o mesmo portao (a diferenca estava em quem decidia a PRESENCA)."""
    return bool(c["hud_ativo"]) and bool(c["nativo_clicavel"]) and portao_antes(c)


def estados(sequencia=None):
    """A lista de estados da rodada (dict completo, com os defaults do PADRAO)."""
    saida = []
    for _nome, parcial in (sequencia or SEQUENCIA_DE_TURNO):
        estado = dict(PADRAO)
        estado.update(parcial)
        saida.append(estado)
    return saida


def transicoes(funcao, sequencia=None):
    """QUANTAS VEZES a visibilidade MUDA ao longo da rodada — a medida do piscar."""
    valores = [funcao(estado) for estado in estados(sequencia)]
    return sum(1 for a, b in zip(valores, valores[1:]) if a != b)


def visibilidades(funcao, sequencia=None):
    return [funcao(estado) for estado in estados(sequencia)]


# ------------------------------------------------------------------ posicao ---

def posicao(fim_dos_nativos, limite, largura_molde, margem=2.0):
    """Transcricao PURA de `RunButton.ColocarNaLinha` (passos 4 e 5): devolve (largura, centro).

    A largura nunca passa do vao livre (`limite - fim - 2*margem`), entao nem o ultimo botao nativo
    nem o vizinho da direita sao invadidos; o centro e' o mais a direita possivel que ainda deixa a
    `margem` de respiro.
    """
    vao = limite - fim_dos_nativos - (2.0 * margem)
    largura = min(largura_molde, vao)
    if largura < 1.0:
        largura = 1.0
    centro = limite - margem - (largura / 2.0)
    menor = fim_dos_nativos + margem + (largura / 2.0)
    if centro < menor:
        centro = menor
    return largura, centro


def bordas(centro, largura):
    return centro - (largura / 2.0), centro + (largura / 2.0)


def invade(esq, direita, outra_esq, outra_direita):
    """Ha' sobreposicao entre [esq, direita] e [outra_esq, outra_direita]?"""
    return esq < outra_direita and outra_esq < direita


def converte_para_o_local(valor_a_partir_da_borda_esquerda, canto_esquerdo):
    """A travessia que FALTAVA no `ColocarNaLinha` (RSTV-30F).

    Um valor medido no espaco do PAI a partir da BORDA ESQUERDA do container passa para o espaco
    LOCAL (origem no PIVOR) somando `rect.xMin` — exatamente o que o codigo ja' fazia em `centro`
    (`novo.anchoredPosition = centro - cantoEsquerdo`).
    """
    return valor_a_partir_da_borda_esquerda + canto_esquerdo


def par_de_referenciais_misturados(prefab=None):
    """O par EXATO que o `ColocarNaLinha` alimentava ANTES da RSTV-30F (a isca do achado).

    `fimDosNativos` ficava no espaco LOCAL (origem no pivor) e o `limite` era medido a partir da
    BORDA ESQUERDA do container. Devolve `(fim, limite, largura_molde)` naquele estado misturado —
    o modelo puro, alimentado com ele, tem de REPROVAR (o clone cai depois do rotador).
    """
    p = prefab or PREFAB
    return p["fim_dos_nativos"], p["limite_medido_na_borda_esquerda"], p["largura_nativa"]


# ------------------------------------------------------------------ checagens ---

def falhas_da_fonte(arquivos):
    """Defeitos do conserto da RSTV-30 no FONTE. Lista vazia = o conserto esta de pe."""
    falhas = []

    run = arquivos.get(ARQUIVO_RUN)
    targets = arquivos.get(ARQUIVO_TARGETS)
    if run is None:
        return ["nao achei %s no mod" % ARQUIVO_RUN]
    if targets is None:
        return ["nao achei %s no mod" % ARQUIVO_TARGETS]

    # --------------------------------------------------------- 1) as provas do conserto
    for arquivo, trecho, rotulo in PROVAS_DA_FONTE:
        texto = arquivos.get(arquivo)
        if texto is None or trecho not in texto:
            falhas.append("%s: faltou %s (%r)" % (arquivo, rotulo, trecho))

    # ---------------------------------- 2) o clone mora no container NATIVO, sem empurrar
    ensure = _corpo_efetivo(run, ENSURE_INTERNAL)
    if ensure is None:
        falhas.append("nao achei %s em %s" % (ENSURE_INTERNAL, ARQUIVO_RUN))
    else:
        if "EscolherMolde" not in ensure:
            falhas.append("EnsureInternal nao escolhe o molde pelo metodo `EscolherMolde`")
        if "molde.transform.parent" not in ensure:
            falhas.append("EnsureInternal nao mede o container (pai do botao nativo molde)")
        if "ignoreLayout = true" not in ensure:
            falhas.append("EnsureInternal nao marca `ignoreLayout = true` — o LayoutGroup do "
                          "container voltaria a refluir a linha (empurraria os botoes nativos)")
        if "ColocarNaLinha" not in ensure:
            falhas.append("EnsureInternal nao chama `ColocarNaLinha` (a posicao deixaria de ser "
                          "medida)")
        if "ClearClickListeners(button)" not in ensure or ".onClick.AddListener" not in ensure:
            falhas.append("EnsureInternal nao limpa o onClick serializado ANTES de instalar o nosso")
        elif ensure.find("ClearClickListeners(button)") > ensure.find(".onClick.AddListener"):
            falhas.append("EnsureInternal instala o listener ANTES de limpar o evento — a "
                          "persistente do molde (`ButtonPressedSkillTree`) sobrevive no clone")

    # ------------------------------- 3) a posicao e MEDIDA (nao ha literal de posicao no codigo)
    colocar = _corpo_efetivo(run, COLOCAR)
    if colocar is None:
        falhas.append("nao achei %s em %s" % (COLOCAR, ARQUIVO_RUN))
    else:
        for trecho, rotulo in (("GetWorldCorners", "GetWorldCorners"), ("InverseTransformPoint", "InverseTransformPoint")):
            if trecho not in colocar:
                falhas.append("ColocarNaLinha nao mede com `%s`" % rotulo)
        for numero in literais_de_posicao(colocar):
            falhas.append("ColocarNaLinha tem o literal de posicao %s no codigo — posicao chutada "
                          "(a posicao tem de sair das medidas)" % numero)

        # 3b) UM SO' REFERENCIAL (RSTV-30F). `fimDosNativos` sai de `container.InverseTransformPoint`
        #     => espaco LOCAL do container, cuja ORIGEM e' o PIVOR. O limite da direita tem de sair
        #     do MESMO espaco: medi-lo com `pai.InverseTransformPoint` e comparar com a borda
        #     ESQUERDA do container mistura as duas origens. No prefab isso empurrava o clone ~55.7 px
        #     para a direita (o vao saia 74.6 em vez de 19.0) e o botao caia DEPOIS do rotador.
        receptores = set(re.findall(r"([A-Za-z_][A-Za-z0-9_]*)\.InverseTransformPoint", colocar))
        for receptor in sorted(receptores):
            if receptor != "container":
                falhas.append("ColocarNaLinha mede `InverseTransformPoint` no espaco de `%s` em vez "
                              "do container — o limite da direita volta a misturar referenciais "
                              "(RSTV-30F: o botao caia a direita do rotador da barra de skills)"
                              % receptor)

    # ------------------------------------------ 4) a VISIBILIDADE nao passa pelo portao
    mirror = _corpo_efetivo(run, MIRROR)
    if mirror is None:
        falhas.append("nao achei %s em %s" % (MIRROR, ARQUIVO_RUN))
    else:
        if "RunTargets.GateOk" in mirror:
            falhas.append("Mirror chama `RunTargets.GateOk` — o portao voltou a decidir a "
                          "PRESENCA do botao (era o piscar do dono)")
        for trecho, rotulo in (("EspelharVisibilidade()", "EspelharVisibilidade"),
                               ("AplicarClique()", "AplicarClique")):
            if trecho not in mirror:
                falhas.append("Mirror nao chama `%s`" % rotulo)

    clique = _corpo_efetivo(run, APLICAR_CLIQUE)
    if clique is None:
        falhas.append("nao achei %s em %s" % (APLICAR_CLIQUE, ARQUIVO_RUN))
    else:
        if "RunTargets.GateOk" not in clique:
            falhas.append("AplicarClique nao consulta o portao da run")
        if "interactable" not in clique:
            falhas.append("AplicarClique nao aplica o resultado no `interactable`")
        if "_mold.interactable" not in clique:
            falhas.append("AplicarClique nao espelha a regra NATIVA do jogo "
                          "(`skillsBtn.interactable`, GUIManager.Update l.120491)")

    espelhar = _corpo_efetivo(run, ESPELHAR)
    if espelhar is None:
        falhas.append("nao achei %s em %s" % (ESPELHAR, ARQUIVO_RUN))
    elif "_mold.gameObject.activeSelf" not in espelhar:
        falhas.append("EspelharVisibilidade nao espelha o botao nativo")

    # -------------------------------------- 5) as guardas: removidas fora, justificadas dentro
    gate = _corpo_efetivo(targets, GATE_OK)
    if gate is None:
        falhas.append("nao achei %s em %s" % (GATE_OK, ARQUIVO_TARGETS))
    else:
        for gid, trecho, defeito in GUARDAS_REMOVIDAS:
            if trecho in gate:
                falhas.append("a guarda %r voltou ao portao (%r) — %s" % (gid, trecho, defeito))

    faltando = justificativas_faltando(targets)
    falhas.extend(faltando)

    # --------------------------------------- 6) o codigo proibido nao existe em lugar nenhum
    for nome, texto in arquivos.items():
        efetivo = rec.codigo_efetivo(texto)
        for trecho, motivo in CODIGO_PROIBIDO:
            if trecho in efetivo:
                falhas.append("%s ainda usa `%s` no codigo efetivo — %s" % (nome, trecho, motivo))

    return falhas


def literais_de_posicao(codigo):
    """Literais numericos de POSICAO (com casa decimal) no codigo — `0f`/`1f`/`2f` nao contam.

    A conta legitima usa `0f`, `1f` (ancoras), `1f` (piso de largura), `0.5f` (metade da largura) e a
    `Margem`. Qualquer outro literal decimal seria posicao digitada a mao — e o pedido do dono era
    explicitamente "nada de posicao chutada".
    """
    permitidos = {"0f", "1f", "0.5f", "0.0f"}
    achados = []
    for m in re.finditer(r"\b\d+\.\d+f\b", codigo):
        if m.group(0) not in permitidos:
            achados.append(m.group(0))
    return achados


def _bloco_da_guarda(gate, i):
    """O trecho da guarda a partir do marcador: do comentario ate' o `}` do `if` DELA.

    O recorte e' ESTRUTURAL (casamento de chaves via `recorte.bloco_apos`), nao uma janela de
    caracteres: o `{` procurado e' o proprio `if (...)` da guarda logo depois do comentario. Um
    marcador sem `if` de verdade logo em seguida cai no `arc.Falhou` do recorte — que e' o que
    queremos (guarda citada sem corpo nao vale).
    """
    faixa = rec.faixa_bloco_apos(gate, i)
    bloco = gate[i:faixa[1] + 1]
    arc.exigir(len(bloco) <= 1500,
               "o trecho da guarda em %d tem %d caracteres: o `if` logo depois do marcador nao e' "
               "dela (guarda sem corpo proprio)" % (i, len(bloco)))
    return bloco


def justificativas_faltando(src_targets):
    """As guardas que FICARAM no portao e a justificativa ao lado delas, no FONTE COM COMENTARIOS."""
    gate = _corpo(src_targets, GATE_OK)
    faltando = []
    for marcador, trecho in JUSTIFICATIVAS:
        i = gate.find(marcador)
        if i < 0:
            faltando.append("o portao nao tem o marcador %r — guarda sem justificativa no codigo" % marcador)
            continue
        bloco = _bloco_da_guarda(gate, i)
        if "Justificativa" not in bloco:
            faltando.append("%s nao traz a linha `Justificativa:` ao lado (guarda sem justificativa)" % marcador)
        if trecho not in bloco:
            faltando.append("%s nao nomeia o campo que protege (%r)" % (marcador, trecho))
    return faltando


# ------------------------------------------------------------ plantio do defeito ---

_ANCORA_VISIBILIDADE = """                EspelharVisibilidade();
                AplicarClique();"""

_DEFEITO_VISIBILIDADE = """                string porqueNao;
                if (!RunTargets.GateOk(out porqueNao))
                {
                    Hide(porqueNao, true);
                    return;
                }

                EspelharVisibilidade();
                AplicarClique();"""


def fonte_com_visibilidade_por_estado(src_run):
    """O MESMO RunButton.cs com a VISIBILIDADE presa ao portao (o defeito do dono), em memoria.

    Nao mexe em arquivo nenhum: e' a isca (`cp_rstv30_visibilidade_por_estado.py`) que prova que as
    checagens reprovam quando o portao volta a esconder o botao.
    """
    if _ANCORA_VISIBILIDADE not in src_run:
        return src_run
    return src_run.replace(_ANCORA_VISIBILIDADE, _DEFEITO_VISIBILIDADE, 1)


_ANCORA_GUARDA = """                    // GUARDA 6 (dano real, SO em batalha) — posicionamento inicial da batalha.
                    // Justificativa: e a fase em que o JOGO esta posicionando o time e mexendo no
                    // personagem selecionado (`Root.SpawnPlacementActive`, l.112152 liga /
                    // l.112165 desliga); a abertura tambem mexe nesse campo, entao ela espera.
                    if (root.SpawnPlacementActive)
                    {
                        motivo = "posicionamento inicial em andamento (Root.SpawnPlacementActive)";
                        return false;
                    }"""

_DEFEITO_GUARDA = _ANCORA_GUARDA + """

                    if (root.AnyActingCharactersInBattle)
                    {
                        motivo = "algum personagem esta executando acao (Root.AnyActingCharactersInBattle)";
                        return false;
                    }"""


def fonte_com_guarda_de_volta(src_targets):
    """O MESMO RunTargets.cs com a guarda do PISCAR de volta (`AnyActingCharactersInBattle`)."""
    if _ANCORA_GUARDA not in src_targets:
        return src_targets
    return src_targets.replace(_ANCORA_GUARDA, _DEFEITO_GUARDA, 1)


_ANCORA_JUSTIFICATIVA = """                // GUARDA 3 (dano real, universal) — modo de apontar o hex.
                // Justificativa: abrir a arvore ESCREVE `GameLogic.CurrentlySelectedCharacter`
                // (`SkillTreeReadOnly`: define o alvo quando o jogo nao tem nenhum selecionado) e
                // escrever esse campo durante a mira forca `CurrentState = Movement` (l.110065),
                // CANCELANDO o apontar o hex que o jogador tinha comecado.
                if (gui.PingModeActive)"""


def fonte_sem_justificativa(src_targets):
    """O MESMO RunTargets.cs com a justificativa da GUARDA 3 apagada (guarda sem justificativa)."""
    if _ANCORA_JUSTIFICATIVA not in src_targets:
        return src_targets
    return src_targets.replace(_ANCORA_JUSTIFICATIVA, "                // GUARDA 3 (dano real, universal) — modo de apontar o hex.\n                if (gui.PingModeActive)", 1)
