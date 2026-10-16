# RealmApi

Modding API for Stolen Realm, with UI helpers and optional observational hooks.
It is a base for other mods; it does not add playable content on its own.

- **Version:** 0.1.0
- **Author:** gumatos
- **Category:** Mods (`mods`, `stolen-realm` community)
- **BepInEx GUID:** `com.gumatos.realmapi`
- **Namespace:** `Gumatos.RealmApi`
- **License:** MIT

> **Pre-release in preparation.** The implementation was exercised offline, not validated inside the game
> process in this delivery. The hooks ship disabled. The packer already assembles the ZIP with the three
> assemblies together in `plugins/RealmApi/`; this page does not announce a published package.

## What it does

- Provides a documented, versioned surface for other mods of this repository: one place for the
  generic UI plumbing (cloning a native game object, wiring a button click) and for reading game
  properties by reflection.
- Ships an **observational hook catalog** (`HookCatalog`) that *observes* four game points and never
  changes results or arguments: every postfix is observational.
- Ships an **UI family** (`Gumatos.RealmApi.UI`) that can *mutate* the game UI behind explicit binding
  and opt-in (see *UI family* below).
- Publishes a notification bus with disposable subscription and isolation of subscriber failures.

## What it does not do

- It does not add playable content on its own: it is a base for other mods.
- It does not implement the inventory domains outside the four hooks above and the **UI** family
  (detailed combat, enemies, quests, persistent data) — there is no silent stub and no compatibility
  promise.
- It does not cover TextMeshPro or the full filling of a tooltip (both are listed as not exercised below).
- It does not discover, on its own, where the game keeps each host: the live host for each UI family is
  supplied by the consumer through `UiHosts`.

## For players: installation planned after release

Install only when a mod you use asks for this dependency and there is a released version.
Declared requirement: `BepInEx-BepInExPack-5.4.2305`. Use the Stolen Realm community mod manager.
The complete package must place the three files together:

```text
BepInEx/plugins/RealmApi/
  RealmApi.dll
  RealmApi.Core.dll
  RealmApi.Hooks.dll
```

Do not copy `RealmApi.dll` alone: the plugin depends on Core and Hooks. Avoid old copies in any
subfolder of `plugins`, because BepInEx also looks for them recursively. To remove it, uninstall through
the manager and review the mods that depend on the API; in a manual installation, remove only the
`RealmApi` folder. Do not keep DLL backups inside `plugins`.

Configuration file: `BepInEx/config/com.gumatos.realmapi.cfg`, section `Safety`:

```ini
[Safety]
EnableHooks = false
```

`false` is the default: the plugin registers that the hooks are disabled and does not install them. Enable
it only in an authorized in-game test. With `true`, the plugin still requires the exact version and hash of
the target listed below. Check `BepInEx/LogOutput.log` for the reason of a refusal, instead of disabling
the checks.

**That gate controls the hooks installed by the plugin, not the whole UI family.** A consumer can bind
the UI and authorize mutations explicitly, even with `EnableHooks=false`.

The official 256×256 icon (art provided by the author) ships with the package as `icon.png`. The
preparation of this version neither installed into the profile nor published the package.

## Target game version (mandatory, fail-closed)

The five fields below make up the **declared identity** of the target. The runtime gate (`ApiIdentity.Matches`,
`api/Core/Contracts.cs:24-26`) checks **only two** of them at execution time: `Application.version` (≈ game version)
and the SHA-256 of `Assembly-CSharp.dll`. The others (Steam AppID, Steam Build, Unity) are **documented identity of the target**
and are used in the update step (`api/docs/target-game.json`) — **they are not compared at runtime**.
`BepInProcess("Stolen Realm.exe")` matches the executable name, not the AppID.

| Field | Value | Checked at runtime? | How it was measured |
|---|---|---|---|
| Steam AppID | `1330000` | **NO** (documented identity) | game Steam manifest |
| Game version | `1.3.1` | **YES** (`Application.version`) | `PlayerSettings` in `<game>/Stolen Realm_Data/globalgamemanagers` |
| Steam Build | `25240684` | **NO** (documented identity) | `buildid` in `appmanifest_1330000.acf` |
| Unity | `2022.3.62f2` | **NO** (documented identity) | header of `globalgamemanagers` |
| Assembly-CSharp SHA-256 | `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a` | **YES** (`sha256sum`) | `sha256sum lib/Assembly-CSharp.dll` (same as the game's `Managed/Assembly-CSharp.dll`) |

The values live in `Gumatos.RealmApi.ApiIdentity` (`api/Core/Contracts.cs`). Detail and reproducibility:
`api/docs/target-game.json`. **If the version (`Application.version`) or the SHA-256 of the `Assembly-CSharp`
diverge, the API installs no hook at all**
(`ApiIdentity.Matches` compares only those two fields and refuses when they are missing or different).

## Existing consumers in the project

These are concrete uses in the code, not a claim that the published versions of the consumers already
carry those integrations:

- **RoguelikeSkillTreeVisualizer (RSTV):** uses `UIFactory.Clone` and `UIFactory.BindClick` through an
  explicit binding. TextMeshPro and specific visual assembly stay inside the mod itself.
- **RoguelikeDebugger:** probes `ApiIdentity` by reflection, optionally; it keeps a local identity
  without the API or with the hooks off.
- **RealmApi → KitSdk bridge:** a separate observational adapter, explicitly created by the host
  with a bus, producer state, session and diagnostics. It does not discover the API and does not install hooks.

These consumers do not ship with this package. The API does not depend on them to load.

## For mod authors

The following sections detail the surface and its limits. Paths `api/`, `lib/` and `docs/` are
references to the [repository](https://github.com/DefRuivo/stolenRealmMods/tree/main/api) tree,
not files promised inside the ZIP. Inspection and smoke tools also live in the repository;
the runtime package needs only the three assemblies of its own plus the distribution metadata.

## How to use

Consumer: reference `RealmApi.Core.dll` (and, if you need to install hooks, `RealmApi.Hooks.dll`; for the
UI family, `RealmApi.dll`, which is where its 5 public types live). The **hooks** part observes and does **not**
change a result or an argument of the game — every postfix is observational. The **UI** family, on the contrary, **mutates**
the UI (see its own section below).

```csharp
// 1) Observe the catalog points. Runs on the hook thread; the return value is the subscription.
IDisposable sub = RealmHooks.Observed.Subscribe(n =>
{
    // n.HookId      -> "combat.turn-started", "ui.localized", ...
    // n.Instance    -> object instance when the target is not static (may be null)
    // n.Arguments   -> copy of the argument list (not a deep copy of Unity objects)
    // n.Result      -> return value, when the target returns a value
});

// 2) One-off property read, without reflection spread across your mod:
object? valor = RealmAccess.ReadProperty(assembly, "Burst2Flame.Game", "Instance");
```

Hooks implemented in the **0.1.0** base (`HookCatalog.All`, four only):

| HookId | Target | Shape |
|---|---|---|
| `game.awake` | `Burst2Flame.Game::Awake` | void postfix, instance |
| `ui.skill-tree.updated` | `SkillTreeManager::UpdateSkillTreeItems` | void postfix, instance |
| `ui.localized` | `OptionsManager::Localize` (static) | postfix with `__result` (string) |
| `combat.turn-started` | `GameLogic::StartNewTurn` | void postfix, instance |

The inventory families outside the four hooks above and the **UI** family (detailed combat, enemies,
quests, persistent data) **are not implemented** — there is no silent stub and no promise of
compatibility.

## UI family (API-R1-I2) — behavioural, through explicit binding

`Gumatos.RealmApi.UI` has the 5 inventory types with the **exact signatures** (`UIFactory`, `ActionBarUI`,
`SkillTreeUI`, `MenuUI`, `TooltipHelper`; 21 signatures across 5 types, including the double `Clone` overload).
It is **different in nature** from the hooks: `AddButton`, `AddTab`, `BindClick`, `SetText`, `Clone`, `Destroy`
etc. **MUTATE** the game UI. That is why it does not go through the observational bus (`RealmHooks.Observed`),
it is not a Harmony postfix, and it lives behind three explicit locks:

1. **Explicit binding.** `UiFamily.Bind(assemblyDoJogo, hosts, allowMutation)` resolves, by exact
   metadata (the same rule as `HookDescriptor.Resolve`), the **17 requirements** of the family against the
   game assembly: missing target -> `MissingMemberException`; divergent signature -> `MissingMethodException`;
   host of the wrong type -> `ArgumentException`. A binding is only published when **all** the
   requirements resolve: there is no partial binding and a `Bind` that fails does not change the current binding.
   Calling any method of the 5 families without a binding -> `InvalidOperationException`.
2. **Mutation opt-in.** Without `allowMutation:true` in `Bind`, every method that mutates throws. The
   read-only ones (`HasTab`, `FindChild`) are the ones that do not require the opt-in, but they still require a binding and the thread.
3. **Thread.** The binding records the thread (the Unity main thread) and using the family from another thread throws:
   Unity UI is not thread-safe.

```csharp
// True state of the game that the consumer supplies (what it found in the scene); the API does NOT guess where
// the game keeps each thing. Missing host = that family fails closed.
var hosts = new UiHosts {
    GuiManager = guiManagerDoJogo,             // UIFactory + TooltipHelper
    CurrentCharacterUi = currentCharacterUi,   // ActionBarUI
    SkillTreeManager = skillTreeManager,       // SkillTreeUI
    MenuTabManager = menuTabManager            // MenuUI
};
UiFamily.Bind(assemblyDoJogo, hosts, allowMutation: true);
try {
    UIFactory.SetText(botaoNativo, "Meu texto");         // mutates
    ActionBarUI.AddButton("meu-botao", icone, AoClicar); // mutates
    bool tem = SkillTreeUI.HasTab(SkillTree.Fire);       // read
} finally { UiFamily.Unbind(); }   // clears the binding and the state of the 5 families
```

Target table (all measured in `lib/Assembly-CSharp.dll`, verified on every smoke run by the test
`actual-game-ui-requirements-metadata`):

| Type | Game target (exact signature) | What the API does |
|---|---|---|
| `TooltipHelper` | `Tooltip::HideTooltip()`, through `GUIManager::instance` + field `GUIManager::tooltip` | `HideTooltip` delegates **1:1** to the native member |
| `ActionBarUI` | `CurrentCharacterUI::Instance`/`ActiveSkillbar`, `Skillbar::HasAvailableSlot()`, `Skillbar::RefreshSkillBar()` | proves a free slot on the host, registers the button, asks for the bar to be rebuilt |
| `SkillTreeUI` | `SkillTreeManager::IsNotNullAndIsActive`, `SkillTreeManager::UpdateSkillTreeItems()` | proves the tree is active, registers the tab, asks for a rebuild |
| `MenuUI` | `MenuTabManager::RefreshSelected()` | registers the tab and asks for a rebuild |
| `UIFactory` | `GUIManager::instance` | clones/copies layout/wires click/text/icon/destroys over the native Unity objects |

**Why the 5 types live in `RealmApi.dll` and not in `Core`.** Measured: `Core` is `netstandard2.0` and the
target's Unity assemblies are `netstandard2.1` — the direct reference fails (`CS1705`) and a net472 process
does not even load `UnityEngine.CoreModule` (`FileNotFoundException: netstandard, Version=2.1.0.0`).
Signing the 5 types with Unity types (as the inventory requires) is only possible in a netstandard2.1 project, which is
the plugin's. That is why **no** new project was created (the acceptance criteria speak of 5 Release projects): what
can be exercised offline (binding, guards, state, delegation) stayed in `Core`; the Unity signatures stayed in
`RealmApi.dll`. Conformance of the 21 signatures is proven by metadata, not by execution
(`api/tools/check_ui_contract.py` -> `api/docs/ui-contract-diff.json`, verdict `CONFORME`, with a negative control
that fails if the comparison passes by omission).

## Config and safety

In `BepInEx/config`, section `Safety`:

- `EnableHooks` (default **false**): hooks disabled until an in-game smoke is explicitly authorized.
  With `false` the plugin only writes to the log and installs nothing.
- With `true`, the plugin still requires that the version (`Application.version`) **and** the SHA-256 of the `Assembly-CSharp`
  of the current process match the table above; any divergence becomes a `LogError` and **zero hooks**.

## How to build

Prerequisites:

- **.NET SDK 6.0** (measured: `6.0.428`).
- **Reference DLLs in `lib/`** (`Assembly-CSharp.dll`, `0Harmony.dll`, `BepInEx.dll`, `UnityEngine.dll`,
  `UnityEngine.CoreModule.dll`). Used by the plugin (`RealmApi.csproj`) and by Core/Hooks.
- **BepInEx Core** (r2modman profile): `$(USERPROFILE)/AppData/Roaming/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/core`.
  Smoke (`RealmApi.Smoke.csproj`) and Inspect (`Inspect.csproj`) read DLLs from there through the property
  `BepInExCoreDir` (default: the same path; it can be overridden with `-p:BepInExCoreDir=<path>`).
  Smoke consumes: `0Harmony.dll`, `Mono.Cecil.dll`, `MonoMod.RuntimeDetour.dll`, `MonoMod.Utils.dll`,
  `BepInEx.dll`. Inspect consumes: `Mono.Cecil.dll`.
- **UnityEngine*.dll**: they come from `lib/`, **not** from BepInEx Core.

```bash
dotnet build api/Core/RealmApi.Core.csproj  -c Release
dotnet build api/Hooks/RealmApi.Hooks.csproj -c Release
dotnet build api/Plugin/RealmApi.csproj      -c Release
dotnet build api/Smoke/RealmApi.Smoke.csproj -c Release
dotnet build api/tools/Inspect/Inspect.csproj -c Release
```

> **Note:** to build Smoke/Inspect without the r2modman profile installed, pass `-p:BepInExCoreDir=<path-to-core>`
> pointing at a folder containing the DLLs listed above.


**Nothing is installed by default.** `api/Plugin/RealmApi.csproj` has a deploy target `DeployToBepInEx`
(API-R1-I1) that follows the opt-in rule of the root (`Directory.Build.props`): building **without**
`-p:DeployToBepInEx=true` copies no file at all into the `r2modman` profile; with the flag, it copies the **three**
assemblies the plugin needs, into the same folder (`RealmApi.dll`, `RealmApi.Core.dll`, `RealmApi.Hooks.dll`).
A deploy rehearsal into an isolated folder, the install command, the success/failure criteria and the rollback are in
`docs/automacao/API-R1-runbook-runtime.md`. Measured in this round: the default build (without the flag) did not change
a byte of the profile — a fingerprint before/after in `docs/automacao/API-R1-I1-evidencias/`.

## How to run the smoke suite (offline)

```bash
api/Smoke/bin/Release/net472/RealmApi.Smoke.exe \
  C:/dev/stolen-realm/lib/Assembly-CSharp.dll \
  C:/dev/stolen-realm/api/Plugin/bin/Release/netstandard2.1/RealmApi.dll
```

Result measured in this delivery: `Ran 62 tests; failures: 0`, exit 0 (`api/docs/smoke-result.json`, literal
output in `api/docs/smoke-output.txt`). The base had 25; API-R1-I2 added 37, 5 of them cases per type
of the UI family (`target-present`, `target-absent`, `member-absent`, `signature-divergent`,
`unbound-fails-closed`) plus real delegation in the CLR, the mutation opt-in, thread, missing/wrong host,
atomic `Bind` and the test `actual-game-ui-requirements-metadata` (17 requirements checked against the
installed `Assembly-CSharp`).

It answers the three questions of the acceptance criteria: **does it load?** (Core/Hooks load and the identity is checked),
**does it expose?** (the catalog resolves type+exact signature and the plugin attribute matches), **do the hooks respond?**
(real Harmony postfixes fire, isolate subscribers, preserve third-party owners and are removed
leaving zero patch) — and, for the UI family, **does the target exist?** (fail-closed binding, delegation and guards).
The Unity targets of the smoke are **artificial fixtures** with the same signatures: they prove the mechanics in the CLR,
they do **not** prove game behaviour. The smoke CLR (net472) does not load `RealmApi.dll` (netstandard2.1);
that is why the 5 public types are checked by metadata (`Inspect ui` + `api/tools/check_ui_contract.py`) and the smoke
only checks presence/absence of a stub by metadata (`ui-public-surface-in-plugin-metadata`).

## How to update when the game changes

Fixed order; every step has a reproducible command.

1. **Re-check the identity.** Run `sha256sum lib/Assembly-CSharp.dll` and compare it with
   `ApiIdentity.AssemblySha256`; check `buildid` in `appmanifest_1330000.acf` and the version in
   `globalgamemanagers`. Update `api/docs/target-game.json` and `ApiIdentity` **only** if the target really changed.
   While version and hash do not match, the plugin refuses to install hooks — that is intentional.
2. **Regenerate the surface.** `dotnet run --project api/tools/Inspect/Inspect.csproj -c Release -- targets lib/Assembly-CSharp.dll > api/docs/game-targets.json`.
   The command reads **metadata** (Mono.Cecil); it does not execute the game assembly.
3. **Re-compare.** For every `HookDescriptor` of the catalog, confirm that the type exists, that the method has an
   identical signature and that the shape of the postfix is still supported (`IsStatic`/`ReturnType`). The smoke already
   covers that by metadata (`actual-game-hook-metadata`). For the **UI family**, the same step is the test
   `actual-game-ui-requirements-metadata`, which resolves the 17 requirements of `UiRequirements.All` against the
   measured `Assembly-CSharp`.
4. **Adjust your own code.** If a target changed name/signature, fix the `HookCatalog` (hooks) or
   `UiRequirements` (`api/Core/Ui/UiFamily.cs`, UI family) and, if the semantics of the point changed, the hook or the
   corresponding method. If the point disappeared, **remove it** from the catalog and record the removal in
   `docs/automacao/API-R1-*.md` — do not invent a silent alternative target.
5. **Rebuild and run the smoke.** The five `dotnet build` commands above and the suite; requirement: `failures: 0`.
6. **Re-check the conformance of the UI family.** Regenerate the implemented surface and run the checker:
   `dotnet run --project api/tools/Inspect/Inspect.csproj -c Release --no-build -- ui api/Plugin/bin/Release/netstandard2.1/RealmApi.dll api/Core/bin/Release/netstandard2.0/RealmApi.Core.dll > api/docs/ui-contract.json`
   and then `python api/tools/check_ui_contract.py` (requirement: `CONFORME`, exit 0, with the negative control
   reporting a problem — if the negative control passes, the comparison is worthless).
7. **Re-record the evidence.** Update `api/docs/target-game.json`, `api/docs/smoke-result.json`,
   `api/docs/smoke-output.txt` and `api/docs/ui-contract-diff.json` with the new round. Estimated numbers do not
   belong here.
8. **Runtime only with authorization.** An in-game smoke (real BepInEx) is a separate act, explicitly
   authorized by the owner; until then the result stays declared as NOT exercised.

## How to contribute

- A new hook = one method in the catalog + one metadata test + one case in the real dispatch smoke.
  If the required shape is neither `void` (instance) nor `string` (static), that is a **shape extension**
  and needs an architecture decision before the code.
- A **new member of the UI family** = one `UiRequirement` in the catalog (`api/Core/Ui/UiFamily.cs`) + the method in the
  public type with the inventory signature + one case in the smoke. A member that **mutates** the UI must enter the
  list that requires `allowMutation:true`; a member that only reads does not. Signature conformance is checked
  by `api/tools/check_ui_contract.py`, which fails on a divergence of name, type, return, order/type/name of
  parameter and optionality — it is not a review by reading.
- Do not change `Assembly-CSharp.dll` and do not redistribute it. Never reference the game assembly in the plugin
  code (the smoke has the test `no-game-assembly-dependency` to prevent that regression).
- No behaviour-modifying patches in the hooks of this base: the 0.1.0 hooks are
  observational. The UI family is behavioural and may mutate the interface with a binding and the opt-in;
  cancelling/substituting arguments from the hooks is a separate front.
- Every statement in a document of this module must come with a file path, a count or a reproducible
  command; whatever is not exercisable declares itself `NAO_EXERCITADO` with the reason.
- Language: the package pages (this README and the CHANGELOG) are in English, with a short Portuguese section at the
  end of this README — the same shape as the other packages of this project. Internal documentation under `docs/`
  stays in Portuguese.

## NOT exercised in this delivery

- Loading by BepInEx inside the game process, gameplay, turns/saves/multiplayer.
- **Runtime identity: NAO_EXERCITADO.** `ApiIdentity.Matches` (which compares `Application.version` +
  the SHA-256 of `Assembly-CSharp`) never ran inside the real game process — the offline smoke checks metadata,
  not the Unity runtime. Version equality will only be exercised when an authorized in-game smoke is
  run.
- Installation into the `r2modman` profile: **NAO_EXERCITADO** — the deploy target exists and is conditioned on the
  opt-in (see `docs/automacao/API-R1-runbook-runtime.md`), but nothing was copied into the profile: in this round
  the profile fingerprint (path/bytes/mtime/sha256 of `plugins/` and `config/`) is identical before and
  after the build (`docs/automacao/API-R1-I1-evidencias/01` and `04`, the hash of the set equal in both).
- The inventory families outside the four hooks above and the **UI** family.
- **UI family — runtime**: nothing was called inside the game. `NAO_EXERCITADO`: (a) real visual
  composition (`UnityEngine.Object.Instantiate`, `Transform.Find`, `Image.sprite`, `Text.text`, `LayoutGroup`, `Destroy`)
  runs only on metadata fixtures; (b) the native filling of the tooltip (`Tooltip::ShowTooltip` of the game, 13
  parameters) — the delivery resolves the target, stores the request and makes the tooltip visible; (c) `AddButton`/`AddTab`
  create the **registration** and ask the native host to rebuild (`RefreshSkillBar`/`UpdateSkillTreeItems`/
  `RefreshSelected`), but the visual creation of the element from a native prefab is not done here;
  (d) `SetText`/`SetIcon` cover `UnityEngine.UI.Text`/`Image` — **TextMeshPro** (which the game uses a lot) is
  outside this delivery and fails closed with `MissingComponentException`; (e) obtaining each host **live**
  (where the game keeps `CurrentCharacterUI`/`MenuTabManager`/`SkillTreeManager` in the scene) is up to the
  consumer through `UiHosts` — the API does not guess that path.
- Publication to Thunderstore: a separate act, explicitly authorized; it was **not** done.

## License and limits

MIT (`api/LICENSE`), author Gumatos. It does not include and does not redistribute game or third-party assemblies.

---

## Português (BR)

> Esta seção é o resumo curto em português; a página do pacote (o resto deste README e o CHANGELOG) está em
> inglês, na mesma forma das outras páginas deste projeto. A documentação interna em `docs/` continua em português.

**O que é.** API de modding para Stolen Realm: uma base para outros mods, com helpers de interface e hooks
observacionais opcionais. Ela **não adiciona conteúdo jogável sozinha**.

**O que ela NÃO faz.** Não implementa os domínios do inventário fora dos quatro hooks e da família **UI**
(combate detalhado, inimigos, quests, dados persistentes); não cobre TextMeshPro nem o preenchimento completo
de tooltip; e não descobre sozinha onde o jogo guarda cada hospedeiro de UI (isso é do consumidor, via `UiHosts`).

**Versão alvo do jogo (fail-closed).** O gate de runtime (`ApiIdentity.Matches`) compara **apenas** a versão
(`Application.version` = `1.3.1`) e o SHA-256 do `Assembly-CSharp.dll`
(`8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a`). AppID `1330000`, Build Steam `25240684` e
Unity `2022.3.62f2` são identidade **documentada** do alvo, não comparadas em runtime. Se versão ou hash
divergirem, a API **não instala hook nenhum**.

**Instalar (previsto para depois da liberação).** Instale só quando um mod que você usa pedir esta dependência e
houver versão liberada. Requisito declarado: `BepInEx-BepInExPack-5.4.2305`. O pacote completo põe os **três**
assemblies juntos em `BepInEx/plugins/RealmApi/`: `RealmApi.dll`, `RealmApi.Core.dll` e `RealmApi.Hooks.dll`.
Não copie apenas o `RealmApi.dll` e não deixe cópias antigas em subpastas de `plugins` (o BepInEx procura
recursivamente).

**Desinstalar.** Desinstale pelo gerenciador e revise os mods que dependem da API; na instalação manual, retire
somente a pasta `RealmApi`.

**Configuração.** `BepInEx/config/com.gumatos.realmapi.cfg`, seção `Safety`: `EnableHooks = false` por padrão.
Com `true`, o plugin ainda exige a versão e o hash exatos do alvo; toda divergência vira `LogError` e **zero
hooks**. Esse portão controla os hooks do plugin, não a família UI inteira.

**Compilar.** .NET SDK 6.0 (`6.0.428`) e as DLLs de referência em `lib/`; os cinco `dotnet build -c Release` de
`api/` estão listados acima. **Nada é instalado por padrão**: só `-p:DeployToBepInEx=true` copia os três
assemblies para o perfil do r2modman.

**Não exercitado nesta entrega.** Carregamento pelo BepInEx no processo do jogo, gameplay, saves, multiplayer,
identidade em runtime, instalação no perfil `r2modman` e a família UI em runtime — tudo declarado
`NAO_EXERCITADO` com motivo na seção acima. Nenhuma publicação foi feita.
