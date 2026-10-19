# Changelog — RoguelikeDebugger

> A **development** tool, not a player mod.
> Publication dates use ISO 8601 (BRT, UTC−03:00); undated older headings do not assert a release date.
> CHG-REV documentation audit: 2026-10-16. These repository corrections do not modify previously published ZIPs.

## 0.1.4 — in preparation (2026-10-19)

- **Source and contributions:** the README now links to the source repository, so users can report issues, contribute or make a fork: https://github.com/DefRuivo/stolenRealmMods.
- Bumped the project, manifest, plugin attribute and README version together; rebuilt the Release package. No intentional gameplay or instrumentation change in this bump.

## 0.1.3 — 2026-10-16

- **Dump provenance (DBG-R2, commit `097f950`, 2026-10-11):** a `DBG-PROV-V1` header before the patches with the game/DLL identity and hashes; OPEN/PARTIAL state with the hooks really applied; footer CLOSED in `Application.quitting`. Measurement failures are explicit, not estimated values. Without a footer there is no proof of a normal shutdown; a boot census does not prove absence across every asset/preset/localization.
- **RealmApi optional:** the identity is probed by reflection; without the API or with hooks disabled, the tool keeps measuring locally. It did not become a mandatory dependency.
- **Explicit read mode:** the new provenance classifies the Flame matrix that **already existed**: it uses `Game.EvalVoid` and records expressions in `MissingExpressions`; therefore a session with that matrix is marked as **active** reading, not strict passive observation. It does not change character attributes, but it is not literally just text in the log.
- **Version:** 0.1.2 -> **0.1.3** in the four places that carry it (the `<Version>` of the `.csproj`, the `version_number` of `manifest.json`, the `[BepInPlugin(...)]` literal and the README version line). These changes were in the source identified as 0.1.2 and were **not** in the DLL published on 2026-10-07; 0.1.3 is the package that carries them, with the DLL rebuilt from the current source.

## 0.1.2 — 2026-10-07

**No intentional gameplay change; the dump and the instrumentation changed.** The matrix is not strict passive observation: it calls `Game.EvalVoid`, records expressions in `MissingExpressions` and restores `Game.CurrentGameFunctionParameters`, without changing character attributes. This version carries the RD-2/RD-2F dump, the instrumentation of an open investigation and the public text in English.

- **The status dump no longer truncates per field (RD-2F).** There used to be a SINGLE `try/catch` around the whole loop: an exception in any field (the new fields read `IEffectInfo[]` arrays by reflection) aborted the loop and **the rest of the statuses vanished from the log silently**. Now every field goes out under a guard and the failure becomes a **marker in the field itself** (`!erro:<Tipo>`) — that line and every following one still print normally. The loop also iterates over a **COPY** of the list (an insertion during the iteration had the same effect). The size cut (`90`/`110` chars) is gone for good: it was cutting the mechanics.
- **New fields in `[Status]` (RD-2):** `expr` (`DescriptionExpressions`), `danoExpr` (`DamageExpressionOverrides`), `refAcao`/`refStatus` (`TooltipDamageInfoRefAction`/`RefStatus`), `tick` (`TickTargets` + `ActionsOnTick*` + `StatusEffectsOnTick*`) and `auraSts` (`AuraSourceStatus`/`AuraTriggerStatus`). Inside the status `trigEf`: `~alvos=` (the `SkillTrigger.Targets` field), `~acoes=` (the trigger actions **with their effects** — a trigger action never enters the `[Action]` inventory), `~chances=` and `~cd=`. It was `~alvos=` that answered section 7 of RV-19: `Flame Shrine Aura` fires with `Targets="Cell.IsCurrentHex(Target)"` (`TriggerType=1`) and `Decay Shrine Aura` with `"Cell.IsCurrentHex(Source)"` (`TriggerType=4`) — the proc does **not** go through the tick path.
- **Measurement of those fields on the game asset** (offline reader, **not** in game): 421 of the 424 readable `ActionStatusInfo`; `expr` in 138, `refAcao`/`refStatus` in 19/7, `StatusEffectsOnTick` in 6, `auraSts` in 40 and `TickTargets`/`ActionsOnTick*` in **0**.
- **Instrumentation `[FlameRV49]` (RV-49) — NOT EXERCISED IN GAME.** When the proc of a danger shrine aura (Decay/Flame) fires, the log gains the evaluated expression, **whom the engine put in `Source` and in `Target`**, the resolved percentage, the final damage and a **matrix** that re-evaluates the same expression with `ShrineEffectBonus` pinned at 0 / 8 / 20 / 100 (Omnism I/II, Horn of Devotion). It is diagnostic instrumentation for a question that is still open: no character is changed (the matrix uses fresh dictionaries and returns `Game.CurrentGameFunctionParameters` to its previous value). Filter: only the expression that mentions `ShrineEffectBonus` produces a line.
- **Build instructions (DEPLOY-2):** the deploy into the r2modman profile became **explicit opt-in** — `dotnet build` alone **installs nothing any more**; installing is `-p:DeployToBepInEx=true`.
- **Public text in English:** the README is now in English (with the final section in Portuguese, as in the other mods) and the **listing description**, which came out in Portuguese in 0.1.1, now comes out in English. The README states what has still **not** been exercised in game.

### What this version does NOT prove

- **RD-2/RD-2F validation status at release time:** the 0.1.2 package notes only recorded offline asset inspection, not a complete in-game matrix. Subsequent boot logs do contain the new fields; that does not establish execution of the FlameRV49 proc matrix or close RV-49. This documentary audit does not reopen the game.

## 0.1.1

**Hook applier fix: the published 0.1.0 loaded the tool and applied no hook at all — no dump came out.**

- Replacing `PatchAll()` with **hook-by-hook application** came with a hook class filter that required `[HarmonyPrefix]`/`[HarmonyPostfix]` **on the method**. This mod declares its 10 hooks through Harmony's **naming convention** (a `Postfix` method in each class of `Patches/`), which Harmony accepts exactly like the attribute — the filter rejected all 10 classes: the tool **loaded, logged "loaded." and dumped nothing** (the silence looking like success; it was the A-1 defect from REV-2, in 4 mods).
- The filter now requires only `[HarmonyPatch]` **on the TYPE** — the same set of classes that `PatchAll()` processed. Measured by invoking the real filter from the built DLL: **10 of 10 patch classes accepted and 10 hook methods inside** (before: 0 of 10). Across the project, the 4 affected mods went from 0/14 to **14/14** patch classes accepted.
- **Hooks applied one by one** (same hardening, same release): `CreateClassProcessor(...).Patch()` per hook class, one log line per hook and a summary with the **real count** — a hook that fails does not take down the other nine.
- **Final icon** (the owner's art in `docs/img/roguelikedebugger-icon-fonte.png`, 1254x1254): resized to the **256x256** Thunderstore requires and embedded in the package. Out goes the 946-byte **placeholder** with the initials that the packer used to generate (`--gerar-icones`), which was what the zip was shipping. The source art stays versioned in `docs/img/` — the repository keeps both.

### Dump: effects by CONCRETE TYPE (RV-8b-0g)

- The `Effects` arrays (of status and of action) are `IEffectInfo[]`, an empty interface: the `e as GeneralEffect` cast the dump used to read the `Action` returns `null` for every element of another type, and the data disappeared from the dump (2 entries of the tooltip census came out `indeterminado` because of that). Now:
  - new fields `nEfeitosTot` / `efTipos` (status and action): array size and **concrete type + fields of each element**, read by reflection;
  - `nAttrEf` / `attrTipos` (status and skill) and `consEf` (item) for the `AttributeEffects` and the consumable action;
  - `nTrig` / `trigEf` in `[Status]`: the status triggers (type, effects, condition, status) — they did not come out before;
  - a summary line per category, `[Efeitos] resumo (...): total= | porTipo= | naoGeneralEffect=`.
  - `desc=` is still last and no value contains `|` or quotes: the old format does not change.
- **The version went up (0.1.0 → 0.1.1) because of the applier fix above:** the 0.1.0 that was live carries the defect and a published Thunderstore version is immutable. This new dump is the same one that was in "Unreleased".

### Historical RD-2 preparation note — 2026-10-01 (not a second release)

Commit `51a4aa5` recorded those fields when the source still said 0.1.1, with the sentence "the version does NOT change / dump not released yet". That stopped describing the state of the distribution: `88232fe` consolidated them into 0.1.2, published on 2026-10-07. The list and the limits of the offline measurement are in the 0.1.2 section above; they are not attributed to 0.1.1 again.

## 0.1.0

First published version.

- **Dump of the game's internal data into `LogOutput.log`** (logs only, no gameplay change):
  - **Skills**: inventory with name, description, description expressions, granted actions, attribute effects and triggers.
  - **Actions** (`[ActionProps]` / `[Trigger]`): type, targets, maximum range, knockback, number of hits, cooldown, charges, usage conditions, chances and applied statuses.
  - **Statuses**: inventory of buffs/debuffs with attribute effects and description.
  - **Items and affixes**: type, rarity, optional description, attributes, armor ratio and consumable action.
  - **Powerups**: roguelike inventory, one line per level.
  - **Loot, gold and experience**: the rolls, the modifiers applied and the values granted.
- It is the source of the coverage CSVs in `docs/cobertura/` used by the other mods of the project.
- **Do not distribute to friends**: it fills the log with thousands of lines on every boot.
