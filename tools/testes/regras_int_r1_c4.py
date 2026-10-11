#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_int_r1_c4.py - INT-R1-C4: a plumbing de UI GENERICA do RSTV vem da familia `UI` da API.

O QUE ESTE CARTAO FEZ (e o que estas regras travam)
---------------------------------------------------
O mod escrevia a mao a plumbing de UI generica (clonar um objeto nativo, ligar o clique do botao).
A API propria (`api/`, projeto `Gumatos.RealmApi`) tem uma familia `UI` com assinatura para isso,
implementada no cartao provedor INT-R1-C1 (`t_9fa61e7e`). Este cartao e o CONSUMIDOR: onde a API
cobre o mesmo efeito de forma EXATAMENTE equivalente, o mod passa a chamar a API.

A EQUIVALENCIA (medida, nao suposta)
------------------------------------
* `UIFactory.Clone(template, parent, name)` faz `Object.Instantiate(template, parent, false)` e
  nomeia o clone. O overload de 2 argumentos do jogo (`Instantiate(Object, Transform)`), lido do
  `lib/UnityEngine.CoreModule.dll` DESTE build, cai em `instantiateInWorldSpace: false`: o mesmo
  efeito, na mesma ordem, com o mesmo argumento.
* `UIFactory.BindClick(go, action)` faz `go.GetComponent<Button>().onClick.AddListener(action)`.
  O mesmo `AddListener` que o mod chamava (a troca da INSTANCIA do evento continua sendo do mod,
  porque a API nao expoe esse primitivo — RSTV-12).
Procedencia: `docs/automacao/INT-R1-C4-parte02.md` (com o comando do decompilador).

ESCOPO FECHADO (o diff e' so' isso)
-----------------------------------
5 CLONES e 2 CLIQUES migram. Eles sao os pontos que (a) a API cobre de forma equivalente e (b) NAO
sao o texto preso por um aceite anterior do RSTV. Os pontos PRESOS ficam como estavam — e o
teste exige que continuem presos (senao a migracao teria reaberto um aceite):

| Ponto preso | Literal no fonte | Regra que prende |
|---|---|---|
| `LevelUpWindowButton.cs` | `Instantiate(original.gameObject, janela.transform)` | `regras_rstv11b.py:214` |
| `SkillTreesTab.cs` (aba) | `Instantiate(menu.TabSkillTree.gameObject` | `regras_rstv16.py:69` |
| `SkillTreesTab.cs` (noh) | `Instantiate(gui.skillTreeItemActivePrefab, paiDeNos)` | `regras_rstv18.py:136` |
| `RunButton.cs`/`SkillTreesWindow.cs` | `.onClick.AddListener(new UnityAction(...))` | `regras_rstv12.py:233`, `regras_rstv21.py:598`, `regras_rstv30.py:426` |

O que a API NAO cobre de forma equivalente e portanto NAO foi migrado (com motivo medido em
`docs/automacao/INT-R1-C4-parte01.md` secao 6): texto TMP (`SetText` so' cobre UGUI `Text`),
busca que falha fechado (`FindChild` lanca onde o mod trata o nulo), `ActionBarUI`/`SkillTreeUI`/
`MenuUI` (registram e mandam o hospedeiro reconstruir; nao CRIA o elemento visual) e o
`ClearClickListeners`/`DisableLocalizers` (nao existem na familia).

O RISCO CONHECIDO (item 4 do cartao)
------------------------------------
Fechar o viewer nativo COMMITA (`CharacterMenusManager.CloseSkillTreeMenu` -> l.48494
`AcceptSkillChanges(closeMenu: true)`; e l.108137 no levantamento RSTV-1). O ponto de observacao
desse risco na API e' o hook `ui.skill-tree.updated`
(`SkillTreeManager::UpdateSkillTreeItems`, `api/Core/Contracts.cs:62`). A defesa do mod contra esse
commit NAO esta na plumbing de UI: esta nos ganchos (`Patches.cs`, patch de
`SkillTreeManager.AcceptSkillChanges`). Estas regras exigem que (a) a guarda continue no lugar e
(b) o arquivo dos ganchos NAO cite a familia `UI`/a ponte — assim fica provado, por ESTRUTURA, que
a migracao nao abriu caminho novo para dentro da janela que commita. A observacao EM JOGO pelo hook
esta declarada NAO_EXERCITADA (runtime fora do escopo deste cartao).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import recorte as rec

MOD = "RoguelikeSkillTreeVisualizer"
ARQUIVO_PONTE = "RstvApiUi.cs"
ARQUIVO_GANCHOS = "Patches.cs"
ARQUIVO_PLUGIN = "Plugin.cs"
ARQUIVO_CSPROJ = "RoguelikeSkillTreeVisualizer.csproj"
ARQUIVO_README = "README.md"

CAMINHO_CONTRATOS_API = os.path.join("api", "Core", "Contracts.cs")

# ---------------------------------------------------------------- assinaturas da ponte ---
# As assinaturas EXATAS da ponte do mod. Se um nome mudar, a checagem REPROVA dizendo qual sumiu.
PONTE_VINCULO = "internal static void AsegurarVinculo()"
PONTE_CLONAR = "internal static GameObject Clonar(GameObject molde, Transform pai, string nome)"
PONTE_CLIQUE = "internal static void LigarClique(GameObject alvo, UnityAction acao)"

VINCULO_EXATO = "UiFamily.Bind(typeof(GUIManager).Assembly, hosts, allowMutation: true)"

# ---------------------------------------------------------------- os pontos MIGRADOS ---
# (arquivo, chamada EXATA que tem de existir no codigo EFETIVO, o que ela substituiu)
CLONES_MIGRADOS = (
    ("RunButton.cs",
     "RstvApiUi.Clonar(molde.gameObject, parent, ButtonName)",
     "Instantiate(molde.gameObject, parent) + clone.name = ButtonName"),
    ("RemovalWindowSkillsButton.cs",
     "RstvApiUi.Clonar(molde.gameObject, pai, ButtonName)",
     "Instantiate(molde.gameObject, pai) + clone.name = ButtonName"),
    ("SkillTreesTab.cs",
     'RstvApiUi.Clonar(molde, _barraDeClasses.transform, "RstvClassButton_" + tipo)',
     "Instantiate(molde, _barraDeClasses.transform) + botao.name"),
    ("SkillTreesWindow.cs",
     "RstvApiUi.Clonar(molde.gameObject, cabecalho, TitleName)",
     "Instantiate(molde, cabecalho) + clone.gameObject.name = TitleName"),
    ("SkillTreesWindow.cs",
     "RstvApiUi.Clonar(molde.gameObject, cabecalho, null)",
     "Instantiate(molde.gameObject, cabecalho) (o nome e' aplicado no caminho comum)"),
)

CLIQUES_MIGRADOS = (
    ("RemovalWindowSkillsButton.cs",
     "RstvApiUi.LigarClique(botao.gameObject, new UnityAction(OnClick))",
     "botao.onClick.AddListener(new UnityAction(OnClick))"),
    ("SkillTreesTab.cs",
     "RstvApiUi.LigarClique(bt.gameObject, new UnityAction(delegate { TrocarClasse(capturado); }))",
     "bt.onClick.AddListener(new UnityAction(delegate { TrocarClasse(capturado); }))"),
)

# ------------------------------------------ os pontos PRESOS por aceite ANTERIOR (nao migrados) ---
# (arquivo, literal que TEM de continuar no codigo efetivo, a regra que o prende)
PRESOS_POR_ACEITE = (
    ("LevelUpWindowButton.cs", "Instantiate(original.gameObject, janela.transform)",
     "regras_rstv11b.py:214 (RSTV-11b: o clone mora na janela, nunca no Content)"),
    ("SkillTreesTab.cs", "Instantiate(menu.TabSkillTree.gameObject",
     "regras_rstv16.py:69 (RSTV-16: o clone da aba nativa)"),
    ("SkillTreesTab.cs", "Instantiate(gui.skillTreeItemActivePrefab, paiDeNos)",
     "regras_rstv18.py:136 (RSTV-18: o clone do noh de skill)"),
    ("RunButton.cs", "NativeUiHelpers.ClearClickListeners(button)",
     "regras_rstv30.py:116/426 e regras_rstv12.py (a troca da INSTANCIA do evento)"),
)

# ---------------------------------------------------------------- CONTAGENS do escopo ---
# Quantas vezes a forma ANTIGA pode aparecer, por arquivo, DEPOIS da migracao. O numero e' o
# ESCOPO: `Instantiate` direto so' nos pontos presos; `AddListener` direto so' nos presos; a ponte
# nao tem nenhum dos dois (ela DELEGA — se ela passasse a fazer a chamada crua, a migracao sumiria).
INSTANTIATE_ESPERADO = {
    "LevelUpWindowButton.cs": 1,   # preso (RSTV-11b)
    "SkillTreesTab.cs": 2,         # presos (RSTV-16 e RSTV-18)
}
ADD_LISTENER_ESPERADO = {
    "LevelUpWindowButton.cs": 1,   # preso (RSTV-11b/12)
    "RunButton.cs": 1,             # preso (RSTV-30/12)
    "SkillTreesTab.cs": 1,         # preso (RSTV-16)
    "SkillTreesWindow.cs": 1,      # preso (RSTV-21)
}
CLONAR_ESPERADO = {
    "RunButton.cs": 1,
    "RemovalWindowSkillsButton.cs": 1,
    "SkillTreesTab.cs": 1,
    "SkillTreesWindow.cs": 2,
}
CLIQUE_ESPERADO = {
    "RemovalWindowSkillsButton.cs": 1,
    "SkillTreesTab.cs": 1,
}

# ---------------------------------------------------------------- dependencia da API ---
GUID_API = "com.gumatos.realmapi"
VERSAO_MINIMA_API = "0.1.0"

# O GUID e a versao minima na MESMA declaracao (nao em duas constantes soltas): e' o par que o
# BepInEx le na hora de decidir carregar.
DEPENDENCIA_EXATA = "[BepInDependency(ApiGuid, ApiVersionMinima)]"

# A guarda do COMMIT (risco conhecido do cartao): o patch do mod no caminho que grava.
GUARDA_DO_COMMIT = "SkillTreeManager.AcceptSkillChanges"

# O ponto de OBSERVACAO que a API oferece para essa janela (prova do contrato no provedor).
HOOK_DA_JANELA = '"ui.skill-tree.updated", "SkillTreeManager", "UpdateSkillTreeItems"'

# A PROVA DO CONTRATO (cartao: "Prova do contrato: api/docs/contract-inventory.json (familia UI, 5
# tipos)"): o inventario e ANONIMIZADO (`Gumatos.RealmApi.ContractReference.*`) e o veredito da
# superficie implementada contra ele e o de `api/docs/ui-contract-diff.json`.
NOMESPACE_UI_DO_INVENTARIO = "Gumatos.RealmApi.ContractReference.UI."
TIPOS_UI_NO_INVENTARIO = 5
VEREDITO_CONFORME = "CONFORME"


# ------------------------------------------------------------------ caminhos/leitura ---

def dir_do_mod():
    return os.path.join(arc.raiz_do_repo(), MOD)


def dir_da_api():
    return os.path.join(arc.raiz_do_repo(), "api")


def fonte(nome):
    """O fonte VIVO do mod (nao uma copia: a expectativa fica amarrada ao que sera compilado)."""
    with open(os.path.join(dir_do_mod(), nome), encoding="utf-8") as fh:
        return fh.read()


def fontes_do_mod():
    """{nome_do_arquivo: conteudo} de TODOS os `.cs` do mod."""
    pasta = dir_do_mod()
    return {nome: fonte(nome) for nome in sorted(os.listdir(pasta)) if nome.endswith(".cs")}


def efetivo(texto):
    """O CODIGO (sem comentario) — citacao de comentario nao conta como uso de API."""
    return rec.codigo_efetivo(texto)


def conta(texto_efetivo, trecho):
    return texto_efetivo.count(trecho)


def fonte_da_api(relativo):
    with open(os.path.join(arc.raiz_do_repo(), relativo), encoding="utf-8") as fh:
        return fh.read()


# ------------------------------------------------------------------ checagens ---

def falhas_da_migracao(arquivos):
    """Defeitos da migracao no FONTE do mod. Lista vazia = a migracao esta de pe.

    Cada falha nomeia o arquivo e o ponto: o teste nao pode reprovar por motivo generico.
    """
    falhas = []

    ponte = arquivos.get(ARQUIVO_PONTE)
    if ponte is None:
        return ["nao achei %s no mod (a ponte para a familia `UI` da API nao existe)" % ARQUIVO_PONTE]

    efetivos = {nome: efetivo(texto) for nome, texto in arquivos.items()}

    # ------------------------------------------------ 1) os pontos MIGRADOS usam a API
    for arquivo, chamada, substituiu in CLONES_MIGRADOS + CLIQUES_MIGRADOS:
        texto = efetivos.get(arquivo)
        if texto is None:
            falhas.append("nao achei %s no mod" % arquivo)
            continue
        if chamada not in texto:
            falhas.append("%s: o ponto que substituiu `%s` nao chama a familia UI da API "
                          "(esperado `%s`)" % (arquivo, substituiu, chamada))

    # ------------------------------------------------ 2) os pontos PRESOS continuam presos
    for arquivo, literal, regra in PRESOS_POR_ACEITE:
        texto = efetivos.get(arquivo)
        if texto is None:
            falhas.append("nao achei %s no mod" % arquivo)
            continue
        if literal not in texto:
            falhas.append("%s: o literal preso por aceite anterior sumiu (`%s` — %s). A migracao "
                          "NAO podia reabrir aquele aceite" % (arquivo, literal, regra))

    # ------------------------------------------------ 3) a CONTAGEM (o escopo e' o numero)
    for arquivo, esperado in INSTANTIATE_ESPERADO.items():
        obtido = conta(efetivos.get(arquivo, ""), "UnityEngine.Object.Instantiate")
        if obtido != esperado:
            falhas.append("%s: `UnityEngine.Object.Instantiate` aparece %d vez(es) no codigo "
                          "efetivo; o escopo desta migracao preve %d (os pontos presos)"
                          % (arquivo, obtido, esperado))
    for arquivo, texto in sorted(efetivos.items()):
        esperado = ADD_LISTENER_ESPERADO.get(arquivo, 0)
        obtido = conta(texto, ".onClick.AddListener")
        if obtido != esperado:
            falhas.append("%s: `.onClick.AddListener` direto aparece %d vez(es); o esperado e %d "
                          "(os pontos presos — os migrados passam por `UIFactory.BindClick`)"
                          % (arquivo, obtido, esperado))
        esperado = CLONAR_ESPERADO.get(arquivo, 0)
        obtido = conta(texto, "RstvApiUi.Clonar(")
        if obtido != esperado:
            falhas.append("%s: `RstvApiUi.Clonar(` aparece %d vez(es); o esperado e %d"
                          % (arquivo, obtido, esperado))
        esperado = CLIQUE_ESPERADO.get(arquivo, 0)
        obtido = conta(texto, "RstvApiUi.LigarClique(")
        if obtido != esperado:
            falhas.append("%s: `RstvApiUi.LigarClique(` aparece %d vez(es); o esperado e %d"
                          % (arquivo, obtido, esperado))

    # ------------------------------------------------ 4) a PONTE: vinculo + delegacao
    if efetivo(ponte).count("UiFamily.Bind(") != 1:
        falhas.append("%s: esperava UM `UiFamily.Bind(` (o vinculo da familia UI); achei %d"
                      % (ARQUIVO_PONTE, efetivo(ponte).count("UiFamily.Bind(")))
    if VINCULO_EXATO not in efetivo(ponte):
        falhas.append("%s: o vinculo nao e' o exigido pela API (`%s`)" % (ARQUIVO_PONTE, VINCULO_EXATO))
    if "allowMutation: true" not in efetivo(ponte):
        falhas.append("%s: a familia UI MUTA a UI do jogo — sem `allowMutation: true` a API lanca "
                      "(e o mod ficaria sem clone/clique)" % ARQUIVO_PONTE)

    efetivo_ponte = efetivo(ponte)
    for assinatura, delegacao in ((PONTE_CLONAR, "UIFactory.Clone("),
                                  (PONTE_CLIQUE, "UIFactory.BindClick(")):
        corpo = rec.corpo_do_metodo(efetivo_ponte, assinatura)
        if corpo is None:
            falhas.append("%s: nao achei o corpo de `%s`" % (ARQUIVO_PONTE, assinatura))
            continue
        if "AsegurarVinculo();" not in corpo:
            falhas.append("%s: `%s` NAO fecha o vinculo antes de usar a API (a chamada cairia em "
                          "`InvalidOperationException`)" % (ARQUIVO_PONTE, assinatura))
        if delegacao not in corpo:
            falhas.append("%s: `%s` nao delega para `%s` — a ponte estaria reimplementando a "
                          "plumbing a mao" % (ARQUIVO_PONTE, assinatura, delegacao))
        if "UnityEngine.Object.Instantiate" in corpo or ".onClick.AddListener" in corpo:
            falhas.append("%s: `%s` voltou a escrever a plumbing A MAO (Instantiate/AddListener "
                          "dentro da ponte)" % (ARQUIVO_PONTE, assinatura))

    # A familia UI da API so' entra pela ponte (um lugar so').
    for nome, texto in sorted(efetivos.items()):
        if nome == ARQUIVO_PONTE:
            continue
        for marcador in ("UIFactory.", "UiFamily.", "UiHosts"):
            if marcador in texto:
                falhas.append("%s: usa `%s` fora da ponte %s — a familia UI da API tem de entrar "
                              "por um lugar so'" % (nome, marcador, ARQUIVO_PONTE))

    # ------------------------------------------------ 5) o risco conhecido (commit)
    ganchos = efetivos.get(ARQUIVO_GANCHOS)
    if ganchos is None:
        falhas.append("nao achei %s no mod" % ARQUIVO_GANCHOS)
    else:
        if GUARDA_DO_COMMIT not in ganchos:
            falhas.append("%s: a guarda do COMMIT do viewer nativo sumiu (`%s`) — o risco conhecido "
                          "(fechar o viewer grava, l.48494/108137) ficou aberto"
                          % (ARQUIVO_GANCHOS, GUARDA_DO_COMMIT))
        for marcador in ("RstvApiUi", "UIFactory.", "UiFamily."):
            if marcador in ganchos:
                falhas.append("%s: os GANCHOS citam `%s` — a plumbing de UI da API nao pode entrar "
                              "no arquivo que guarda o caminho que GRAVA" % (ARQUIVO_GANCHOS, marcador))

    return falhas


def falhas_da_dependencia(arquivos, csproj, readme):
    """A dependencia explicita da API: build (csproj), runtime (BepInDependency) e README."""
    falhas = []

    if "<Reference Include=\"RealmApi\">" not in csproj:
        falhas.append("%s: nao referencia `RealmApi` (os 5 tipos publicos da familia UI)" % ARQUIVO_CSPROJ)
    if "<Reference Include=\"RealmApi.Core\">" not in csproj:
        falhas.append("%s: nao referencia `RealmApi.Core` (o vinculo `UiFamily`)" % ARQUIVO_CSPROJ)
    if csproj.count("<Private>false</Private>") < 2:
        falhas.append("%s: as referencias da API tem de ser `Private=false` — a API e' um pacote "
                      "proprio; copiar a DLL para a pasta do mod duplicaria a API no processo"
                      % ARQUIVO_CSPROJ)

    plugin = efetivo(arquivos.get(ARQUIVO_PLUGIN, ""))
    if DEPENDENCIA_EXATA not in plugin:
        falhas.append("%s: falta a dependencia explicita `%s`" % (ARQUIVO_PLUGIN, DEPENDENCIA_EXATA))
    if ('ApiGuid = "%s"' % GUID_API) not in plugin:
        falhas.append("%s: a constante `ApiGuid` nao e' `%s`" % (ARQUIVO_PLUGIN, GUID_API))
    if ('ApiVersionMinima = "%s"' % VERSAO_MINIMA_API) not in plugin:
        falhas.append("%s: a constante `ApiVersionMinima` nao e' `%s`" % (ARQUIVO_PLUGIN, VERSAO_MINIMA_API))

    if GUID_API not in readme:
        falhas.append("%s (do mod): o README nao nomeia a dependencia (`%s`) — quem instala tem de "
                      "saber o que precisa" % (ARQUIVO_README, GUID_API))
    for marcador in ("RealmApi", "BepInDependency"):
        if marcador not in readme:
            falhas.append("%s (do mod): o README nao explica a dependencia (`%s` ausente)"
                          % (ARQUIVO_README, marcador))

    return falhas


def falhas_do_ponto_de_observacao():
    """O ponto de observacao do risco conhecido tem de existir na API (o provedor)."""
    falhas = []
    if not os.path.exists(os.path.join(arc.raiz_do_repo(), CAMINHO_CONTRATOS_API)):
        return ["nao achei %s (o catalogo de hooks da API)" % CAMINHO_CONTRATOS_API]
    texto = fonte_da_api(CAMINHO_CONTRATOS_API)
    if HOOK_DA_JANELA not in texto:
        falhas.append("%s: o hook `ui.skill-tree.updated` -> `SkillTreeManager::UpdateSkillTreeItems` "
                      "nao esta no catalogo da API — a janela que COMMITA ficaria sem ponto de "
                      "observacao" % CAMINHO_CONTRATOS_API)
    return falhas


def falhas_da_prova_do_contrato(dir_docs=None):
    """O contrato da familia `UI` que a ponte consome: o inventario (5 tipos) e o veredito da API.

    O cartao manda provar o contrato em `api/docs/contract-inventory.json` (familia `UI`, 5 tipos).
    O inventario e' ANONIMIZADO (`Gumatos.RealmApi.ContractReference.*`), e a conformidade da
    superficie implementada contra ele e' o veredito de `api/docs/ui-contract-diff.json` (produzido
    por `api/tools/check_ui_contract.py`, com controle negativo). Aqui se confere o TAMANHO da
    familia no inventario e o veredito — nao se refaz a conferencia de assinatura do provedor.

    `dir_docs` existe para a ISCA: o teste aponta para uma copia com o veredito trocado e exige a
    reprovacao.
    """
    import json

    base = dir_docs or os.path.join(arc.raiz_do_repo(), "api", "docs")
    cam_inv = os.path.join(base, "contract-inventory.json")
    cam_diff = os.path.join(base, "ui-contract-diff.json")
    for cam in (cam_inv, cam_diff):
        if not os.path.exists(cam):
            return ["nao achei %s (a prova do contrato da familia UI)" % cam]

    falhas = []
    with open(cam_inv, encoding="utf-8") as fh:
        inventario = json.load(fh)
    tipos = [t for t in inventario["types"] if t["name"].startswith(NOMESPACE_UI_DO_INVENTARIO)]
    if len(tipos) != TIPOS_UI_NO_INVENTARIO:
        falhas.append("o inventario tem %d tipo(s) na familia UI; o contrato fala em %d "
                      "(%s)" % (len(tipos), TIPOS_UI_NO_INVENTARIO,
                                ", ".join(sorted(t["name"].rsplit(".", 1)[-1] for t in tipos))))

    with open(cam_diff, encoding="utf-8") as fh:
        diff = json.load(fh)
    if diff.get("verdict") != VEREDITO_CONFORME:
        falhas.append("o veredito da conformidade da familia UI nao e `%s` (veio %r) — a superficie "
                      "implementada pela API divergiu do inventario"
                      % (VEREDITO_CONFORME, diff.get("verdict")))
    if diff.get("problems"):
        falhas.append("a conformidade da familia UI traz %d problema(s): %r"
                      % (len(diff["problems"]), diff["problems"][:3]))
    return falhas


# ------------------------------------------------------------ plantio dos defeitos ---
# Cada funcao devolve o MESMO fonte com UM defeito plantado, EM MEMORIA. O teste exige que a
# checagem correspondente REPROVE — sem isso, a checagem poderia estar passando por acidente.

def fonte_com_ponto_antigo(nome, texto):
    """O ponto MIGRADO volta a chamar a plumbing a mao (o defeito que esta entrega conserta)."""
    if nome == "RunButton.cs":
        return texto.replace(
            "clone = RstvApiUi.Clonar(molde.gameObject, parent, ButtonName);",
            "clone = UnityEngine.Object.Instantiate(molde.gameObject, parent);\n"
            "                clone.name = ButtonName;", 1)
    if nome == "SkillTreesWindow.cs":
        return texto.replace(
            "botao = RstvApiUi.Clonar(molde.gameObject, cabecalho, null);",
            "botao = UnityEngine.Object.Instantiate(molde.gameObject, cabecalho);", 1)
    if nome == "RemovalWindowSkillsButton.cs":
        return texto.replace(
            "RstvApiUi.LigarClique(botao.gameObject, new UnityAction(OnClick));",
            "botao.onClick.AddListener(new UnityAction(OnClick));", 1)
    return texto


def fonte_sem_optin_de_mutacao(ponte):
    """A ponte vincula SEM `allowMutation` (a API lanca em todo metodo que muta).

    O plantio e' na CHAMADA (por `VINCULO_EXATO`), nunca no texto: a primeira ocorrencia de
    `allowMutation: true` no arquivo esta num COMENTARIO de documentacao — trocar aquela deixaria o
    codigo de pe e a isca provaria nada.
    """
    return ponte.replace(VINCULO_EXATO, VINCULO_EXATO.replace(": true", ": false"), 1)


def fonte_ponte_que_faz_a_mao(ponte):
    """A ponte para de delegar e volta a chamar o Unity direto (a migracao viraria fachada falsa)."""
    return ponte.replace("return UIFactory.Clone(molde, pai, nome);",
                         "return UnityEngine.Object.Instantiate(molde, pai);", 1)


def fonte_sem_dependencia(plugin):
    """O plugin perde a declaracao explicita da dependencia da API."""
    return plugin.replace(DEPENDENCIA_EXATA + "\n", "", 1)


def fonte_ganchos_com_a_ponte(ganchos):
    """Os GANCHOS passam a usar a ponte (a plumbing entrou no arquivo que guarda o caminho que grava).

    O plantio e' CODIGO (nao comentario): a checagem le o texto EFETIVO, e um comentario citando a
    ponte nao e' uso — plantar um comentario provaria nada.
    """
    return ganchos.replace(
        "namespace RoguelikeSkillTreeVisualizer\n{",
        "namespace RoguelikeSkillTreeVisualizer\n{\n"
        "    internal static class UsoIndevidoDaPonte\n"
        "    {\n"
        "        internal static bool Deve = RstvApiUi.Vinculada;\n"
        "    }\n", 1)


def fonte_readme_sem_dependencia(readme):
    """O README deixa de documentar a dependencia."""
    return readme.replace(GUID_API, "com.gumatos.outracoisa")
