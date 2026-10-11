# API-R1-I2 (INT-R1-C1) — familia UI na API propria — parte 01

Cartao: `t_9fa61e7e`. Worktree: `C:/dev/stolen-realm/.worktrees/t_9fa61e7e` (branch `wt/t_9fa61e7e`, base `d82894e`).
Escopo: implementar na API propria (`api/`, `Gumatos.RealmApi`) a familia **UI** do inventario. Sem RSTV, sem perfil, sem jogo.

## 1. Contrato a implementar (fonte: `api/docs/contract-inventory.json`)

Comando reprodutivel (le o inventario, nao executa nada):

    python -c "import json;d=json.load(open('api/docs/contract-inventory.json',encoding='utf-8'));[print(t['name'],[m['signature'] for m in t['methods']]) for t in d['types'] if '.UI.' in t['name']]"

Resultado medido (5 tipos, 20 membros — **21 assinaturas**, `Clone` tem 2 overloads):

| Tipo do inventario | Metodos |
|---|---|
| `...ContractReference.UI.UIFactory` | `Clone(GameObject,string)`, `Clone(GameObject,Transform,string)`, `CloneComponent(Component,string)`, `CopyRectLayout(RectTransform,RectTransform,Vector2)`, `FindChild(Transform,string)`, `BindClick(GameObject,UnityAction)`, `SetText(GameObject,string)`, `SetIcon(GameObject,Sprite,string)`, `DisableAllText(GameObject)`, `DisableChildLayouts(GameObject)`, `Destroy(GameObject)` — todos `static` |
| `...UI.ActionBarUI` | `AddButton(string,Sprite,Action)`, `RemoveButton(string)`, `UpdateIcon(string,Sprite)` — todos `static` |
| `...UI.SkillTreeUI` | `HasTab(SkillTree)->bool`, `AddTab(string,SkillTree)`, `RemoveTab(SkillTree)` — todos `static` |
| `...UI.MenuUI` | `AddTab(string,Action<GameObject>,Action)`, `RemoveTab(string)` — todos `static` |
| `...UI.TooltipHelper` | `ShowTooltip(string,string,Sprite)`, `HideTooltip()` — todos `static` |

Dependencia de tipo: `SkillTreeUI` usa `...ContractReference.Skills.SkillTree`, que no inventario e um **enum**
de 13 membros: `Chaos, Cold, Custom, Fire, Innate, Light, Lightning, Monk, Nature, Ranger, Shadow, Thief, Warrior`.

Diferenca verificada contra o corpo do cartao: o cartao lista 9 metodos de `UIFactory`; o inventario tem **11**
(existe tambem `DisableAllText` e o segundo overload de `Clone`). O inventario e a fonte — implementei 11.

## 2. Mapeamento de namespace (decisao)

O inventario e anonimizado: o comando `Inspect surface` (`api/tools/Inspect/Program.cs:15-18`) troca o nome do
assembly de origem por `Gumatos.RealmApi.ContractReference`. Portanto o namespace real de origem e o prefixo
`ContractReference` e, nesta API propria, o mesmo tipo vive em `Gumatos.RealmApi.*`:

| Inventario (anonimizado) | Nossa API |
|---|---|
| `Gumatos.RealmApi.ContractReference.UI.UIFactory` | `Gumatos.RealmApi.UI.UIFactory` |
| `Gumatos.RealmApi.ContractReference.UI.ActionBarUI` | `Gumatos.RealmApi.UI.ActionBarUI` |
| `Gumatos.RealmApi.ContractReference.UI.SkillTreeUI` | `Gumatos.RealmApi.UI.SkillTreeUI` |
| `Gumatos.RealmApi.ContractReference.UI.MenuUI` | `Gumatos.RealmApi.UI.MenuUI` |
| `Gumatos.RealmApi.ContractReference.UI.TooltipHelper` | `Gumatos.RealmApi.UI.TooltipHelper` |
| `Gumatos.RealmApi.ContractReference.Skills.SkillTree` | `Gumatos.RealmApi.Skills.SkillTree` |

Nada de API nova: o enum `Skills.SkillTree` entra **apenas** porque a assinatura de `AddTab`/`RemoveTab`/`HasTab`
o exige. Os outros tipos de `Skills` do inventario (`ActionBuilder`, `SkillBuilder`, ...) ficam fora — nao estao
no escopo fechado.

## 3. Alvos existem no jogo? (medido, nao estimado)

A familia UI **nao** existe no `Assembly-CSharp.dll` — ela e codigo da propria API de terceiros, nao um wrapper
de hook. Medido:

    grep -ac 'UIFactory'   lib/Assembly-CSharp.dll   -> 0
    grep -ac 'ActionBarUI' lib/Assembly-CSharp.dll   -> 0
    (idem TooltipHelper, SkillTreeUI, MenuUI)

Mas cada tipo tem um **hospedeiro real** no jogo, medido por `ilspycmd -t <Tipo> lib/Assembly-CSharp.dll`:

| Nossa familia | Hospedeiro no jogo (verificado) |
|---|---|
| `TooltipHelper` | `GUIManager.instance` (prop. estatica, `GUIManager.cs:429`) -> campo `public Tooltip tooltip` (`:156`) -> `Tooltip.HideTooltip()` (`Tooltip.cs:2196`) |
| `ActionBarUI` | `CurrentCharacterUI.Instance` (prop. estatica, `CurrentCharacterUI.cs:114`) -> `Skillbar.ActiveSkillbar`/`ProcessSkillbarButtonsParent()` (`:157`,`:678`) |
| `SkillTreeUI` | `SkillTreeManager` (`UpdateSkillTreeItems`, `SwitchSelectedTree`, ...) e `LoadableUIWindow<SkillTreeManager>.Instance` (`CurrentCharacterUI.cs:437`) |
| `MenuUI` | `MenuTabManager` (`SelectButtonAndInvoke`, `RefreshSelected`; alcancado em `OptionsManager.cs:178`) e `MenuTab` |
| `UIFactory` | `GUIManager.instance` (hospedeiro da arvore de UI) |

Isso fixa a regra arquitetural (secao 4): a familia UI e **composicao com alvo declarado**, nao observacao.

## 4. Decisao de arquitetura (declarada aqui e no README)

1. **A familia UI e comportamental.** `AddButton`/`AddTab`/`BindClick`/`SetText` MUTAM UI. Nasce *separada* do
   barramento observacional `RealmHooks.Observed` — nao publica evento, nao e postfix Harmony.
2. **Vinculo explicito e fail-closed.** `UiFamily.Bind(assembly, allowMutation:false)` resolve, por metadados
   exatos (mesma regra de `HookDescriptor.Resolve`, `api/Core/Contracts.cs:46-54`), o(s) membro(s) alvo de cada
   um dos 5 tipos no assembly do jogo:
   - alvo ausente -> `MissingMemberException`;
   - assinatura divergente -> `MissingMethodException`;
   - chamada sem vinculo -> `InvalidOperationException` (nunca no-op silencioso);
   - vinculo parcial nao existe: **um** alvo que falhe derruba o `Bind` inteiro e nao deixa nada vinculado.
3. **Mutacao e opt-in.** Com `allowMutation:false` (padrao), os 3 metodos mutantes e os mutantes de
   `UIFactory`/`SkillTreeUI`/`MenuUI` lancam `InvalidOperationException`. Isolamento declarado: familia
   observacional (hooks) x familia comportamental (UI).
4. **Thread.** `Bind` grava o `ManagedThreadId` do thread que vinculou (o thread principal do Unity) e todo
   metodo da familia exige esse thread; fora dele -> `InvalidOperationException` (UI do Unity nao e thread-safe).
5. **Sem Unity no caminho de guarda.** Todas as guardas (vinculo, opt-in, thread, argumento nulo) lancam
   *antes* de qualquer chamada a `UnityEngine`; o smoke offline exercita essas guardas e a delegacao 1:1 em
   CLR, e **nao** executa a composicao Unity — que fica declarada `NAO_EXERCITADO`.

## 5. Prova de conformidade de assinatura (planejada)

Comando novo e reprodutivel no `Inspect` (`ui <dll>`) + conferidor que compara a superficie implementada com a
do inventario, com o mapa da secao 2. Evidencia vai para `api/docs/ui-contract.json` e `api/docs/ui-contract-diff.json`.
Divergencia de nome/parametro/tipo = falha, nao aviso.
