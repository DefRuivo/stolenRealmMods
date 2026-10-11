# INT-R1-C4 — parte 02: a migração (os 7 pontos, a equivalência medida, o escopo pelo número)

Cartão `t_84ca88d4`. Continuação de `INT-R1-C4-parte01.md` (reconhecimento).

## 1. A prova de EQUIVALÊNCIA dos dois primitivos (medida no build do jogo)

Não é suposição: as duas pontas foram lidas.

**Ponta do jogo** — `lib/UnityEngine.CoreModule.dll`, tipo `UnityEngine.Object`
(SHA-256 do DLL: `80d43e5f8d52964e3ec0ac514076c3e2ee032af8d9c0c3ef511dfdd9067eee8e`):

```
public static Object Instantiate(Object original, Transform parent)
{
    return Instantiate(original, parent, instantiateInWorldSpace: false);
}
```

Comando: `ilspycmd -t UnityEngine.Object "C:/dev/stolen-realm/lib/UnityEngine.CoreModule.dll"`
(saída literal em `docs/automacao/INT-R1-C4-evidencias/07-ilspy-equivalencia.txt`).
Ou seja: **o overload de DOIS argumentos que o mod usava já é `worldPositionStays = false`.**

**Ponta da API** — `api/Plugin/Ui/UIFactory.cs:28-36`:

```
public static GameObject Clone(GameObject template, Transform parent, string? name = null)
{
    UiFamily.Require(Family, true);
    ...
    var clone = UnityEngine.Object.Instantiate(template, parent, false);
    if (!string.IsNullOrEmpty(name)) clone.name = name;
    return clone;
}
```

Mesmo `Instantiate(template, parent, false)`, mais o nome. O par que o mod escrevia era
`Object.Instantiate(molde, pai)` + `clone.name = NOME` — **o mesmo efeito, na mesma ordem**.

`UIFactory.BindClick` (`api/Plugin/Ui/UIFactory.cs:71-78`) faz
`go.GetComponent<Button>().onClick.AddListener(onClick)`; o mod chamava
`botao.onClick.AddListener(new UnityAction(X))`. **O mesmo `AddListener`, no mesmo evento.**

## 2. Os 7 pontos migrados (arquivo:linha DEPOIS da migração)

| # | Arquivo:linha | Antes (escrito à mão) | Agora |
|---|---|---|---|
| 1 | `RunButton.cs:191` | `Instantiate(molde.gameObject, parent)` + `clone.name = ButtonName` | `RstvApiUi.Clonar(molde.gameObject, parent, ButtonName)` |
| 2 | `RemovalWindowSkillsButton.cs:232` | `Instantiate(molde.gameObject, pai)` + `clone.name = ButtonName` | `RstvApiUi.Clonar(molde.gameObject, pai, ButtonName)` |
| 3 | `SkillTreesTab.cs:1334` | `Instantiate(molde, _barraDeClasses.transform)` + `botao.name = "RstvClassButton_" + tipo` | `RstvApiUi.Clonar(molde, _barraDeClasses.transform, "RstvClassButton_" + tipo)` |
| 4 | `SkillTreesWindow.cs:435` | `Instantiate(molde, cabecalho)` + `clone.gameObject.name = TitleName` | `RstvApiUi.Clonar(molde.gameObject, cabecalho, TitleName).GetComponent<TextMeshProUGUI>()` |
| 5 | `SkillTreesWindow.cs:547` | `Instantiate(molde.gameObject, cabecalho)` (nome aplicado depois, no caminho comum) | `RstvApiUi.Clonar(molde.gameObject, cabecalho, null)` |
| 6 | `RemovalWindowSkillsButton.cs:280` | `botao.onClick.AddListener(new UnityAction(OnClick))` | `RstvApiUi.LigarClique(botao.gameObject, new UnityAction(OnClick))` |
| 7 | `SkillTreesTab.cs:1386` | `bt.onClick.AddListener(new UnityAction(delegate { TrocarClasse(capturado); }))` | `RstvApiUi.LigarClique(bt.gameObject, new UnityAction(delegate { TrocarClasse(capturado); }))` |

Nota do ponto 4: `RstvApiUi.Clonar` devolve o `GameObject` clonado; o
`.GetComponent<TextMeshProUGUI>()` lê do clone **o mesmo componente** que
`Instantiate<T>(molde, cabecalho)` devolvia (o clone é uma cópia do GameObject do molde).

## 3. A ponte: `RoguelikeSkillTreeVisualizer/RstvApiUi.cs` (novo)

* `AsegurarVinculo()` fecha o vínculo **preguiçosamente** (`UiFamily.Bind(typeof(GUIManager).Assembly,
  hosts, allowMutation: true)`) e é idempotente; sem vínculo, a operação **lança** em vez de injetar UI
  pela metade (fail-closed, o desenho da API).
* Hospedeiro entregue: `GuiManager = GUIManager.instance` (o único que a família `UIFactory` poderia
  consultar). `CurrentCharacterUI`/`SkillTreeManager`/`MenuTabManager` ficam nulos **de propósito** —
  as famílias que dependem deles não são usadas nesta entrega, e `Clone`/`BindClick` não consultam
  hospedeiro nenhum (`api/Plugin/Ui/UIFactory.cs:28-36, 71-78`).
* A família `UI` da API **entra por essa ponte e por mais nenhum arquivo** (regra do teste).

## 4. Os pontos NÃO migrados, e por quê (medido, não estimado)

| Ponto | Por que ficou como estava |
|---|---|
| `LevelUpWindowButton.cs:163` | o literal `Instantiate(original.gameObject, janela.transform)` é **preso pelo aceite anterior** `tools/testes/regras_rstv11b.py:214` (o clone mora na JANELA, nunca no `Content`) |
| `SkillTreesTab.cs:236` | preso por `regras_rstv16.py:69` (clone da aba nativa) |
| `SkillTreesTab.cs:1770` | preso por `regras_rstv18.py:136` (clone do nó de skill) |
| `RunButton.cs:232`, `LevelUpWindowButton.cs:194`, `SkillTreesTab.cs:271`, `SkillTreesWindow.cs:589` | `.onClick.AddListener` direto é preso por `regras_rstv12.py:233`, `regras_rstv16.py:74`, `regras_rstv11b.py:243`, `regras_rstv21.py:598`, `regras_rstv30.py:426` |
| rotulagem (`label.text`, TMP) | `UIFactory.SetText` só cobre `UnityEngine.UI.Text` e falha fechado em TextMeshPro (`api/Plugin/Ui/UIFactory.cs:81-87`); trocar seria mudar comportamento |
| `Transform.Find` + tratamento de nulo | `UIFactory.FindChild` **lança** quando o filho não existe (`UIFactory.cs:62-68`); o mod reaproveita o clone existente |
| `ActionBarUI`/`SkillTreeUI`/`MenuUI` | registram o pedido e mandam o hospedeiro nativo reconstruir (`RefreshSkillBar`/`UpdateSkillTreeItems`/`RefreshSelected`); **não criam** o elemento visual (`api/README.md:256-262`) — o mod cria a partir do prefab nativo |
| `NativeUiHelpers.ClearClickListeners`/`DisableLocalizers` | não existem na família `UI` (21 assinaturas, nenhuma equivalente) |

## 5. O escopo provado PELO NÚMERO (código efetivo, sem comentário)

`tools/testes/regras_int_r1_c4.py` (`INSTANTIATE_ESPERADO`, `ADD_LISTENER_ESPERADO`,
`CLONAR_ESPERADO`, `CLIQUE_ESPERADO`) fixa a contagem por arquivo:

| Arquivo | `UnityEngine.Object.Instantiate` | `.onClick.AddListener` | `RstvApiUi.Clonar(` | `RstvApiUi.LigarClique(` |
|---|---|---|---|---|
| `RunButton.cs` | 0 | 1 (preso, RSTV-30/12) | 1 | 0 |
| `RemovalWindowSkillsButton.cs` | 0 | 0 | 1 | 1 |
| `SkillTreesTab.cs` | 2 (presos, RSTV-16/18) | 1 (preso, RSTV-16) | 1 | 1 |
| `SkillTreesWindow.cs` | 0 | 1 (preso, RSTV-21) | 2 | 0 |
| `LevelUpWindowButton.cs` | 1 (preso, RSTV-11b) | 1 (preso, RSTV-11b) | 0 | 0 |
| `RstvApiUi.cs` (a ponte) | 0 | 0 | 0 | 0 |

Qualquer `Instantiate`/`AddListener` a mais (ou a menos) **reprova o teste**: é o que impede o diff de
crescer sem decisão e o que prova que a migração não reabriu um aceite anterior.

## 6. Dependência explícita da API

* `RoguelikeSkillTreeVisualizer.csproj`: `<Reference Include="RealmApi">` (aponta para
  `..\api\Plugin\bin\Release\netstandard2.1\RealmApi.dll`) e `<Reference Include="RealmApi.Core">`
  (`..\api\Core\bin\Release\netstandard2.0\RealmApi.Core.dll`), **as duas com `<Private>false</Private>`**
  — a API é pacote próprio; a DLL não sai junto com o mod (senão o processo carregaria duas cópias).
* `Plugin.cs`: `[BepInDependency(ApiGuid, ApiVersionMinima)]` com
  `ApiGuid = "com.gumatos.realmapi"` e `ApiVersionMinima = "0.1.0"` (versão da família `UI`,
  `api/README.md:4`). É dependência **hard** (padrão do BepInEx): sem a API, o RSTV não carrega.
* `README.md` do mod: seção **Requirements** (EN) e bloco em **PT-BR** dizendo o que acontece sem a API.
* **`manifest.json` NÃO ganhou a dependência de propósito**: o pacote da API ainda não está publicado
  na Thunderstore, e `tools/check_dependencias.py` **recusa** o pacote inteiro quando a versão
  dependida não está publicada (`No matching package found for reference`, arquivo
  `tools/check_dependencias.py:9,250`). Medido: `python tools/check_dependencias.py` -> exit 0 hoje
  ("todas as dependencias resolvem"). Declarar a dependência no manifest é **follow-up** para quando
  a API for publicada; a dependência de runtime já está declarada no código.
* Pré-requisito de build: as duas DLLs da API precisam existir (build da API antes do mod):
  `dotnet build api/Core/RealmApi.Core.csproj -c Release && dotnet build api/Plugin/RealmApi.csproj -c Release`.

## 7. Build (Release, sem deploy)

```
dotnet build RoguelikeSkillTreeVisualizer/RoguelikeSkillTreeVisualizer.csproj -c Release -p:DeployToBepInEx=false
```

Medido: **`0 Erro(s)`, `1 Aviso(s)`**, `RoguelikeSkillTreeVisualizer.dll` gerado em
`bin/Release/netstandard2.1/`. O único aviso é `MSB3277` (conflito de versões de `System.Net.Http`
entre o ref pack netstandard2.1 e o `Assembly-CSharp` do jogo) e é **PRÉ-EXISTENTE e independente
desta entrega**: o build do `BetterTooltips` (que NÃO referencia a API) emite o mesmo aviso.
Saída literal: `docs/automacao/INT-R1-C4-evidencias/03-build-release.txt`.

## 8. Diff (limitado à plumbing de UI)

`git diff --stat -- RoguelikeSkillTreeVisualizer`:

```
 Plugin.cs                              | 14 ++++++++++++++
 RemovalWindowSkillsButton.cs           | 10 +++++++---
 RoguelikeSkillTreeVisualizer.csproj    | 18 ++++++++++++++++++
 RunButton.cs                           |  8 ++++++--
 SkillTreesTab.cs                       |  9 ++++++---
 SkillTreesWindow.cs                    | 11 ++++++++---
 6 files changed, 59 insertions(+), 11 deletions(-)
```

Mais UM arquivo novo: `RstvApiUi.cs` (a ponte). `Patches.cs` (os ganchos, onde mora a guarda do
commit) **não aparece no diff** — o teste exige isso por estrutura. Diff completo:
`docs/automacao/INT-R1-C4-evidencias/02-diff-completo.txt`.

## 9. NAO_EXERCITADO nesta parte

* Runtime em jogo: nada foi chamado dentro do jogo. O `UiFamily.Bind` real em processo BepInEx, a
  composição visual do clone e o clique do botão **NÃO_EXERCITADOS** (a validação visual é do dono).
* O vínculo com hospedeiro nulo para as outras três famílias: o comportamento "família indisponível
  falha fechado" é da API e está medido lá (`api/docs/smoke-result.json`), não aqui.
