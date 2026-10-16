# Changelog — RealmApi

> Dates use ISO 8601 (BRT, UTC−03:00). Implementation/audit dates are not publication dates.
> CHG-REV documentation audit: 2026-10-16. No publication performed.

## 0.1.0 — initial version in preparation (revised on 2026-10-16)

- Base implemented in commit `097f950` (2026-10-11); the manifest and the distribution changelog were prepared locally, still without a commit of their own when this audit was captured. Its own, independent identity: `com.gumatos.realmapi`, namespace `Gumatos.RealmApi`, three assemblies of its own (`RealmApi.dll`, `RealmApi.Core.dll`, `RealmApi.Hooks.dll`).
- `RealmAccess.ReadProperty` offers an explicit reflective read of a public property, with no cache of Unity objects. The catalog resolves exact signatures; the installation checks owner/postfix, undoes a partial installation on failure and removes only its own owner. The plugin keeps the hooks during the destruction of the host and discards the installation in `Application.quitting`, not in `OnDestroy`.
- AppID 1330000, Steam build 25240684 and Unity 2022.3.62f2 are documented identity of the inspected target, not three additional checks of the runtime gate. There is no general implementation of detailed combat, enemies, quests or persistence just because those domains appear in the inventory.

- UI family implemented in `Gumatos.RealmApi.UI`: `UIFactory`, `ActionBarUI`, `SkillTreeUI`, `MenuUI` and `TooltipHelper`. Explicit binding through `UiFamily.Bind`, requirement resolution by signature, thread guard and a separate mutation opt-in (`allowMutation: true`).
- Helpers to clone native UI, wire clicks, copy layout, change UGUI text/icon and destroy objects. `AddButton`/`AddTab` register requests and ask the host to rebuild; they do not create the complete visual element. TextMeshPro and full tooltip filling are not covered.
- Four observational hooks: `game.awake`, `ui.skill-tree.updated`, `ui.localized` and `combat.turn-started`. A notification bus with disposable subscription and isolation of subscriber failures.
- Hooks disabled by default (`Safety.EnableHooks=false`). Even with the opt-in, installation by the plugin requires the game version `1.3.1` and the SHA-256 of `Assembly-CSharp.dll` to equal the declared identity; missing or divergent values refuse the installation. This gate protects the plugin hooks, it is not a global lock of the UI family.
- Existing consumers in the project code: RoguelikeSkillTreeVisualizer (RSTV, `UIFactory.Clone` and `UIFactory.BindClick`), RoguelikeDebugger (optional probe of the identity by reflection, keeping local mode without the API) and the observational bridge RealmApi → KitSdk (separate adapter, explicitly wired by the host). These consumers are not included in this package.
- Offline validation recorded in `api/docs/smoke-result.json` (2026-10-11): smoke suite with 62 tests and zero failures; public UI signatures checked by metadata. That is an earlier result, not a new execution by the CHG-REV audit. It does not replace validation inside the game process: BepInEx/Unity runtime, gameplay, saves, multiplayer and visual composition remain unexercised in this preparation.
- Metadata and package page prepared as a Mod, category `mods` of the `stolen-realm` community. Official 256×256 icon provided by the author (`api/icon.png`, 107.728 bytes, SHA-256 `2b6673512d4250db…`), replacing the previous placeholder.

This entry describes the current implementation, not a completed publication. The project packer already assembles the package with `RealmApi.dll`, `RealmApi.Core.dll` and `RealmApi.Hooks.dll` together in `plugins/RealmApi/`, generating `dist/gumatos-RealmApi-0.1.0.zip`. No installation or publication is authorized by this changelog.
