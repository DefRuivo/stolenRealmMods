# RealmApi — API de modding própria para Stolen Realm

Módulo `api/` do repositório do projeto. Nome do plugin: **RealmApi**. Namespace: `Gumatos.RealmApi`.
GUID BepInEx: `com.gumatos.realmapi`. Versão da API: **0.1.0**.

É um mod **próprio**: código escrito neste repositório, publicado sob MIT (`api/LICENSE`), sem copiar
código de terceiros e sem redistribuir nenhum assembly do jogo. A superfície pública de um pacote
público de API de terceiros foi apenas **inspecionada por metadados** para planejar a reconstrução; o
inventário resultante guardado em `api/docs/contract-inventory.json` é **anonimizado** (nomes de
namespace/host substituídos por `Gumatos.RealmApi.ContractReference.*`), não é código e não é suporte
prometido.

## Versão alvo do jogo (obrigatória, fail-closed)

Os cinco campos abaixo compõem a **identidade declarada** do alvo. O gate de runtime (`ApiIdentity.Matches`,
`api/Core/Contracts.cs:24-26`) verifica **apenas dois** deles em execução: `Application.version` (≈ Versão do jogo)
e SHA-256 do `Assembly-CSharp.dll`. Os demais (Steam AppID, Build Steam, Unity) são **identidade documentada do alvo**
e são usados na etapa de atualização (`api/docs/target-game.json`) — **não são comparados em runtime**.
`BepInProcess("Stolen Realm.exe")` casa o nome do executável, não o AppID.

| Campo | Valor | Verificado em runtime? | Como foi medido |
|---|---|---|---|
| Steam AppID | `1330000` | **NÃO** (identidade documentada) | manifest Steam do jogo |
| Versão do jogo | `1.3.1` | **SIM** (`Application.version`) | `PlayerSettings` em `<jogo>/Stolen Realm_Data/globalgamemanagers` |
| Build Steam | `25240684` | **NÃO** (identidade documentada) | `buildid` em `appmanifest_1330000.acf` |
| Unity | `2022.3.62f2` | **NÃO** (identidade documentada) | cabeçalho do `globalgamemanagers` |
| Assembly-CSharp SHA-256 | `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a` | **SIM** (`sha256sum`) | `sha256sum lib/Assembly-CSharp.dll` (igual ao `Managed/Assembly-CSharp.dll` do jogo) |

Os valores vivem em `Gumatos.RealmApi.ApiIdentity` (`api/Core/Contracts.cs`). Detalhe e reprodutibilidade:
`api/docs/target-game.json`. **Se a versão (`Application.version`) ou o SHA-256 do `Assembly-CSharp`
divergirem, a API não instala hook nenhum**
(`ApiIdentity.Matches` compara apenas esses dois campos e recusa quando ausentes ou diferentes).

## Estrutura

```
api/
  Core/      RealmApi.Core.csproj   -> identidade, HookDescriptor, catálogo de hooks, Signal<T>, RealmAccess,
                                       notificação; e a familia UI sem UnityEngine (UiFamily/UiOperations/Skills.SkillTree)
  Hooks/     RealmApi.Hooks.csproj  -> HookInstallation (Harmony) sobre o catálogo
  Plugin/    RealmApi.csproj        -> RealmApiPlugin (BepInEx), gate de identidade + config EnableHooks;
                                       e os 5 tipos publicos da familia UI (namespace Gumatos.RealmApi.UI)
  Smoke/     RealmApi.Smoke.csproj  -> suíte de fumaca offline (net472, Harmony real no CLR)
  tools/Inspect/Inspect.csproj      -> inventário por metadados (Mono.Cecil), 4 comandos (surface|targets|plugin|ui)
  tools/check_ui_contract.py        -> conferidor superfície implementada x inventário (familia UI)
  docs/                             -> evidências medidas (ver docs/README.md)
```

## Como usar

Consumidor: referencie `RealmApi.Core.dll` (e, se precisar instalar hooks, `RealmApi.Hooks.dll`; para a
família UI, `RealmApi.dll`, que é onde os 5 tipos públicos dela vivem). A parte de **hooks** observa e **não**
muda resultado nem argumentos do jogo — todo postfix é observacional. A família **UI**, ao contrário, **muta**
UI (ver a seção dela abaixo).

```csharp
// 1) Observar os pontos do catálogo. Executa na thread do hook; o retorno é a assinatura.
IDisposable sub = RealmHooks.Observed.Subscribe(n =>
{
    // n.HookId      -> "combat.turn-started", "ui.localized", ...
    // n.Instance    -> instância do objeto quando o alvo não é estático (pode ser null)
    // n.Arguments   -> cópia da lista de argumentos (não é cópia profunda de objetos Unity)
    // n.Result      -> valor de retorno, quando o alvo devolve valor
});

// 2) Leitura pontual de propriedade, sem reflection espalhada no seu mod:
object? valor = RealmAccess.ReadProperty(assembly, "Burst2Flame.Game", "Instance");
```

Hooks implementados na base **0.1.0** (`HookCatalog.All`, quatro apenas):

| HookId | Alvo | Forma |
|---|---|---|
| `game.awake` | `Burst2Flame.Game::Awake` | postfix void, instância |
| `ui.skill-tree.updated` | `SkillTreeManager::UpdateSkillTreeItems` | postfix void, instância |
| `ui.localized` | `OptionsManager::Localize` (estático) | postfix com `__result` (string) |
| `combat.turn-started` | `GameLogic::StartNewTurn` | postfix void, instância |

As famílias do inventário fora dos quatro hooks acima e da família **UI** (combate detalhado, inimigos,
quests, dados persistentes) **não estão implementadas** — não há stub silencioso e não há promessa de
compatibilidade.

## Família UI (API-R1-I2) — comportamental, por vinculo explicito

`Gumatos.RealmApi.UI` tem os 5 tipos do inventário com as **assinaturas exatas** (`UIFactory`, `ActionBarUI`,
`SkillTreeUI`, `MenuUI`, `TooltipHelper`; 21 assinaturas em 5 tipos, incluindo o overload duplo de `Clone`).
Ela é **diferente em natureza** dos hooks: `AddButton`, `AddTab`, `BindClick`, `SetText`, `Clone`, `Destroy`
etc. **MUTAM** a UI do jogo. Por isso ela não passa pelo barramento observacional (`RealmHooks.Observed`),
não é postfix Harmony, e vive atrás de três travas explícitas:

1. **Vínculo explícito.** `UiFamily.Bind(assemblyDoJogo, hosts, allowMutation)` resolve, por metadados
   exatos (mesma regra do `HookDescriptor.Resolve`), os **17 requisitos** da família contra o assembly do
   jogo: alvo ausente -> `MissingMemberException`; assinatura divergente -> `MissingMethodException`;
   hospedeiro de tipo errado -> `ArgumentException`. Um vínculo só é publicado quando **todos** os
   requisitos resolvem: não existe vínculo parcial e um `Bind` que falha não altera o vínculo vigente.
   Chamar qualquer método das 5 famílias sem vínculo -> `InvalidOperationException`.
2. **Opt-in de mutação.** Sem `allowMutation:true` no `Bind`, todo método que muta lança. São leitura
   (`HasTab`, `FindChild`) os que não exigem o opt-in, mas ainda exigem vínculo e thread.
3. **Thread.** O vínculo grava o thread (o main thread do Unity) e usar a família de outro thread lança:
   UI do Unity não é thread-safe.

```csharp
// Estado de verdade do jogo que o consumidor entrega (o que ele achou na cena); a API NÃO adivinha onde
// o jogo guarda cada coisa. Hospedeiro ausente = aquela família falha fechado.
var hosts = new UiHosts {
    GuiManager = guiManagerDoJogo,             // UIFactory + TooltipHelper
    CurrentCharacterUi = currentCharacterUi,   // ActionBarUI
    SkillTreeManager = skillTreeManager,       // SkillTreeUI
    MenuTabManager = menuTabManager            // MenuUI
};
UiFamily.Bind(assemblyDoJogo, hosts, allowMutation: true);
try {
    UIFactory.SetText(botaoNativo, "Meu texto");         // muta
    ActionBarUI.AddButton("meu-botao", icone, AoClicar); // muta
    bool tem = SkillTreeUI.HasTab(SkillTree.Fire);       // leitura
} finally { UiFamily.Unbind(); }   // zera vínculo e o estado das 5 famílias
```

Tabela de alvos (todos medidos em `lib/Assembly-CSharp.dll`, verificados a cada execução do smoke pelo teste
`actual-game-ui-requirements-metadata`):

| Tipo | Alvo no jogo (assinatura exata) | O que a API faz |
|---|---|---|
| `TooltipHelper` | `Tooltip::HideTooltip()`, via `GUIManager::instance` + campo `GUIManager::tooltip` | `HideTooltip` delega **1:1** ao membro nativo |
| `ActionBarUI` | `CurrentCharacterUI::Instance`/`ActiveSkillbar`, `Skillbar::HasAvailableSlot()`, `Skillbar::RefreshSkillBar()` | prova slot livre no hospedeiro, registra o botão, pede a reconstrução da barra |
| `SkillTreeUI` | `SkillTreeManager::IsNotNullAndIsActive`, `SkillTreeManager::UpdateSkillTreeItems()` | prova a árvore ativa, registra a aba, pede a reconstrução |
| `MenuUI` | `MenuTabManager::RefreshSelected()` | registra a aba e pede a reconstrução |
| `UIFactory` | `GUIManager::instance` | clona/copia layout/liga clique/texto/ícone/destrói sobre os objetos nativos do Unity |

**Por que os 5 tipos vivem em `RealmApi.dll` e não em `Core`.** Medido: `Core` é `netstandard2.0` e os
assemblies Unity do alvo são `netstandard2.1` — a referência direta falha (`CS1705`) e um processo net472
não carrega nem o `UnityEngine.CoreModule` (`FileNotFoundException: netstandard, Version=2.1.0.0`).
Assinar os 5 tipos com tipos Unity (como o inventário exige) só é possível num projeto netstandard2.1, que é
o do plugin. Foi por isso que **não** foi criado projeto novo (o aceite fala em 5 projetos Release): o que dá
para exercitar offline (vínculo, guardas, estado, delegação) ficou em `Core`; as assinaturas Unity ficaram em
`RealmApi.dll`. A conformidade das 21 assinaturas é provada por metadados, não por execução
(`api/tools/check_ui_contract.py` -> `api/docs/ui-contract-diff.json`, veredito `CONFORME`, com controle
negativo que falha se a comparação passar por omissão).

## Config e segurança

No `BepInEx/config`, seção `Safety`:

- `EnableHooks` (padrão **false**): hooks desabilitados até um smoke em jogo ser explicitamente autorizado.
  Com `false` o plugin só registra em log e não instala nada.
- Com `true`, o plugin ainda exige que versão (`Application.version`) **e** SHA-256 do `Assembly-CSharp`
  do processo atual batam com a tabela acima; qualquer divergência vira `LogError` e **zero hooks**.

## Como construir

Pré-requisitos:

- **.NET SDK 6.0** (medido: `6.0.428`).
- **DLLs de referência em `lib/`** (`Assembly-CSharp.dll`, `0Harmony.dll`, `BepInEx.dll`, `UnityEngine.dll`,
  `UnityEngine.CoreModule.dll`). Usadas pelo plugin (`RealmApi.csproj`) e pelo Core/Hooks.
- **BepInEx Core** (perfil r2modman): `$(USERPROFILE)/AppData/Roaming/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/core`.
  Smoke (`RealmApi.Smoke.csproj`) e Inspect (`Inspect.csproj`) leem DLLs de lá por meio da propriedade
  `BepInExCoreDir` (default: mesmo caminho; pode ser sobrescrita via `-p:BepInExCoreDir=<caminho>`).
  Smoke consome: `0Harmony.dll`, `Mono.Cecil.dll`, `MonoMod.RuntimeDetour.dll`, `MonoMod.Utils.dll`,
  `BepInEx.dll`. Inspect consome: `Mono.Cecil.dll`.
- **UnityEngine*.dll**: vêm de `lib/`, **não** do BepInEx Core.

```bash
dotnet build api/Core/RealmApi.Core.csproj  -c Release
dotnet build api/Hooks/RealmApi.Hooks.csproj -c Release
dotnet build api/Plugin/RealmApi.csproj      -c Release
dotnet build api/Smoke/RealmApi.Smoke.csproj -c Release
dotnet build api/tools/Inspect/Inspect.csproj -c Release
```

> **Nota:** para construir Smoke/Inspect sem o perfil r2modman instalado, passe `-p:BepInExCoreDir=<caminho-para-core>`
> apontando para uma pasta contendo as DLLs listadas acima.


**Nada é instalado por padrão.** `api/Plugin/RealmApi.csproj` tem um alvo de deploy `DeployToBepInEx`
(API-R1-I1) que segue a regra de opt-in da raiz (`Directory.Build.props`): construir **sem**
`-p:DeployToBepInEx=true` não copia arquivo nenhum para o perfil `r2modman`; com a flag, copia os **três**
assemblies que o plugin precisa, na mesma pasta (`RealmApi.dll`, `RealmApi.Core.dll`, `RealmApi.Hooks.dll`).
Ensaio do deploy em pasta isolada, comando de instalação, critérios de sucesso/falha e rollback estão em
`docs/automacao/API-R1-runbook-runtime.md`. Medido nesta rodada: o build padrão (sem a flag) não alterou
um byte do perfil — impressão digital antes/depois em `docs/automacao/API-R1-I1-evidencias/`.

## Como rodar a suíte de fumaça (offline)

```bash
api/Smoke/bin/Release/net472/RealmApi.Smoke.exe \
  C:/dev/stolen-realm/lib/Assembly-CSharp.dll \
  C:/dev/stolen-realm/api/Plugin/bin/Release/netstandard2.1/RealmApi.dll
```

Resultado medido nesta entrega: `Ran 62 tests; failures: 0`, exit 0 (`api/docs/smoke-result.json`, saída
literal em `api/docs/smoke-output.txt`). A base tinha 25; a API-R1-I2 acrescentou 37, sendo 5 casos por tipo
da família UI (`target-present`, `target-absent`, `member-absent`, `signature-divergent`,
`unbound-fails-closed`) mais delegação real em CLR, opt-in de mutação, thread, hospedeiro ausente/errado,
`Bind` atômico e o teste `actual-game-ui-requirements-metadata` (17 requisitos conferidos no
`Assembly-CSharp` instalado).

Ela responde as três perguntas do aceite: **carrega?** (Core/Hooks carregam e a identidade é conferida),
**expõe?** (catálogo resolve tipo+assinatura exata e o atributo do plugin casa), **hooks respondem?**
(postfixes Harmony reais disparam, isolam assinantes, preservam o owner de terceiros e são removidos
deixando zero patch) — e, para a família UI, **o alvo existe?** (vinculo fail-closed, delegação e guardas).
Os alvos Unity do smoke são **fixtures artificiais** com as mesmas assinaturas: provam a mecânica no CLR,
**não** provam comportamento do jogo. O CLR do smoke (net472) não carrega `RealmApi.dll` (netstandard2.1);
por isso os 5 tipos públicos são conferidos por metadados (`Inspect ui` + `api/tools/check_ui_contract.py`) e o smoke
só checa presença/ausência de stub por metadados (`ui-public-surface-in-plugin-metadata`).

## Como atualizar quando o jogo mudar

Ordem fixa; cada passo tem um comando reprodutível.

1. **Reconferir a identidade.** Rode `sha256sum lib/Assembly-CSharp.dll` e compare com
   `ApiIdentity.AssemblySha256`; confira `buildid` no `appmanifest_1330000.acf` e a versão em
   `globalgamemanagers`. Atualize `api/docs/target-game.json` e `ApiIdentity` **só** se o alvo mudou de verdade.
   Enquanto os três valores não casarem, o plugin recusa instalar — isso é intencional.
2. **Regerar a superfície.** `dotnet run --project api/tools/Inspect/Inspect.csproj -c Release -- targets lib/Assembly-CSharp.dll > api/docs/game-targets.json`.
   O comando lê **metadados** (Mono.Cecil); ele não executa o assembly do jogo.
3. **Recomparar.** Para cada `HookDescriptor` do catálogo, confirme que o tipo existe, que o método tem
   assinatura idêntica e que a forma do postfix continua suportada (`IsStatic`/`ReturnType`). O smoke já
   cobre isso por metadados (`actual-game-hook-metadata`). Para a **família UI**, o mesmo passo é o teste
   `actual-game-ui-requirements-metadata`, que resolve os 17 requisitos de `UiRequirements.All` contra o
   `Assembly-CSharp` medido.
4. **Ajustar o código próprio.** Se um alvo mudou de nome/assinatura, corrija o `HookCatalog` (hooks) ou
   `UiRequirements` (`api/Core/Ui/UiFamily.cs`, família UI) e, se a semântica do ponto mudou, o hook ou o
   método correspondente. Se o ponto desapareceu, **remova-o** do catálogo e registre a remoção em
   `docs/automacao/API-R1-*.md` — não invente um alvo alternativo silencioso.
5. **Reconstruir e rodar o smoke.** Os cinco `dotnet build` acima e a suíte; exigência: `failures: 0`.
6. **Reconferir a conformidade da família UI.** Regere a superfície implementada e rode o conferidor:
   `dotnet run --project api/tools/Inspect/Inspect.csproj -c Release --no-build -- ui api/Plugin/bin/Release/netstandard2.1/RealmApi.dll api/Core/bin/Release/netstandard2.0/RealmApi.Core.dll > api/docs/ui-contract.json`
   e depois `python api/tools/check_ui_contract.py` (exigência: `CONFORME`, exit 0, com o controle negativo
   acusando problema — se o controle negativo passar, a comparação não vale).
7. **Regravar as evidências.** Atualize `api/docs/target-game.json`, `api/docs/smoke-result.json`,
   `api/docs/smoke-output.txt` e `api/docs/ui-contract-diff.json` com a nova rodada. Números estimados não
   entram aqui.
8. **Runtime só com autorização.** Smoke em jogo (BepInEx real) é um ato separado e explicitamente
   autorizado pelo dono; até lá o resultado fica declarado como NÃO exercitado.

## Como contribuir

- Um hook novo = um método no catálogo + um teste de metadados + um caso no smoke real de dispatch.
  Se a forma exigida não for `void` (instância) nem `string` (estático), isso é uma **extensão de forma**
  e precisa de decisão de arquitetura antes do código.
- Um **membro novo da família UI** = um `UiRequirement` no catálogo (`api/Core/Ui/UiFamily.cs`) + o método no
  tipo público com a assinatura do inventário + um caso no smoke. Membro que **muta** UI precisa entrar na
  lista que exige `allowMutation:true`; membro que só lê não entra. A conformidade de assinatura é conferida
  por `api/tools/check_ui_contract.py`, que falha em divergência de nome, tipo, retorno, ordem/tipo/nome de
  parâmetro e opcionalidade — não é revisão por leitura.
- Não altere o `Assembly-CSharp.dll` e não o redistribua. Nunca referencie o assembly do jogo no código
  do plugin (o smoke tem o teste `no-game-assembly-dependency` para impedir essa regressão).
- Nada de patches de modificação de comportamento nesta base: a API 0.1.0 é observacional. Qualquer
  cancelamento/substituição de argumentos é uma frente separada.
- Toda afirmação em documento deste módulo precisa vir com caminho de arquivo, contagem ou comando
  reproduzível; o que não for exercitável se declara `NÃO_EXERCITADO` com o motivo.
- Idioma: português (padrão do repositório).

## NÃO exercitado nesta entrega

- Carregamento pelo BepInEx no processo do jogo, gameplay, turnos/saves/multiplayer.
- **Identidade em runtime: NÃO_EXERCITADO.** `ApiIdentity.Matches` (compara `Application.version` +
  SHA-256 do `Assembly-CSharp`) nunca rodou no processo real do jogo — o smoke offline verifica metadados,
  não o runtime Unity. A igualdade de versão só será exercitada quando um smoke em jogo autorizado for
  rodado.
- Instalação no perfil `r2modman`: **NÃO_EXERCITADO** — o alvo de deploy existe e está condicionado ao
  opt-in (ver `docs/automacao/API-R1-runbook-runtime.md`), mas nada foi copiado para o perfil: nesta rodada
  a impressão digital do perfil (caminho/bytes/mtime/sha256 de `plugins/` e `config/`) é idêntica antes e
  depois do build (`docs/automacao/API-R1-I1-evidencias/01` e `04`, hash do conjunto igual nas duas).
- As famílias do inventário fora dos quatro hooks acima e da família **UI**.
- **Família UI — runtime**: nada foi chamado dentro do jogo. `NÃO_EXERCITADO`: (a) composição visual real
  (`UnityEngine.Object.Instantiate`, `Transform.Find`, `Image.sprite`, `Text.text`, `LayoutGroup`, `Destroy`)
  roda só em fixtures metadados; (b) o preenchimento nativo do tooltip (`Tooltip::ShowTooltip` do jogo, 13
  parâmetros) — a entrega resolve o alvo, guarda o pedido e torna o tooltip visível; (c) `AddButton`/`AddTab`
  criam o **registro** e pedem a reconstrução ao hospedeiro nativo (`RefreshSkillBar`/`UpdateSkillTreeItems`/
  `RefreshSelected`), mas a criação visual do elemento a partir de um prefab nativo não é feita aqui;
  (d) `SetText`/`SetIcon` cobrem `UnityEngine.UI.Text`/`Image` — **TextMeshPro** (que o jogo usa muito) fica
  fora desta entrega e falha fechado com `MissingComponentException`; (e) a obtenção **ao vivo** de cada
  hospedeiro (onde o jogo guarda `CurrentCharacterUI`/`MenuTabManager`/`SkillTreeManager` na cena) é do
  consumidor via `UiHosts` — a API não adivinha esse caminho.
- Publicação em Thunderstore: ato separado e explicitamente autorizado; **não** foi feito.

## Licença e limites

MIT (`api/LICENSE`), autor Gumatos. Não inclui e não redistribui assemblies do jogo nem de terceiros.
