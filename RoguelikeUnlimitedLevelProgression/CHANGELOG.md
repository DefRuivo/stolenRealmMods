# Changelog — RoguelikeUnlimitedLevelProgression

> Dates use ISO 8601 (BRT, UTC−03:00). Implementation/audit dates are not publication dates.
> CHG-REV documentation audit: 2026-10-16. This mod remains unpublished.

## 0.1.1 — in preparation (revised on 2026-10-16)

### Lifecycle and diagnostics (RLP-1/RLP-2) — package rebuilt from the current source on 2026-10-16

- **Root cause:** `Plugin.OnDestroy` itself called `UnpatchSelf()` and turned off `GameplayGroupApplied` when the game destroyed the chainloader host on the first scene. The boot announced the patches, but the plugin removed them before use; it was not proof that the structural window or the engine guards were wrong.
- **Fix:** `OnDestroy` preserves patches and session state, recording the lifecycle and the ownership of the targets. Removal on install failure/rollback remains explicit in `Awake`/`PatchRegistry`; it was not eliminated globally.
- **Instrumentation:** Harmony ownership checked in Awake/OnDestroy/first hook/post-battle, plus refusal reasons and effective policy entries. Reading the existing log on 2026-10-16 records `gameplay=20/20` after OnDestroy and `politica: allow=True ... nivel=20 capVanilla=20`. That proves retention of the patches and passage through the policy, and does not replace the whole save/reload, rewards and multiplayer matrix.
- **Post-battle failsafe:** a separate, best-effort prefix in `PostBattleManager.OpenPostBattleMenu`; it only tries to grant victory advancement to eligible controlled characters still absent from the vanilla list, using the same `Policy.CanAdvance`. It does not duplicate the advancement of those already in the list and does not replace the critical transpiler. It is existing local implementation, not the root cause of the patches disappearing.

### Package identity — 2026-10-13 (commit `941e3c3`)

- Definitive name: `RoguelikeUnlimitedLevelProgression`; display name:
  `Roguelike Unlimited Level Progression`.
- Project, assembly, namespace, package and harness follow the definitive name.
  GUID/Harmony owner and receipts directory: `com.gumatos.roguelikeunlimitedlevelprogression`.
- Distribution icon 256×256 added in `8cabbe5`; the RU icon entered in the rename `941e3c3`. The local art was replaced again after that commit and must not be described as the old monogram without re-auditing. The version remains **0.1.1**; the rename itself changed no gameplay and did not publish the mod.
- `lib/` paths of the project/harness resolved from the checkout root (`06564ce`, 2026-10-12); boot marker fixed to `carregado.` (`931bcc4`, 2026-10-12).
- Since the mod was not published, there is no config/receipt migration.
  The evidence from earlier rounds remains immutable with the identity of its time.

### Load protection — 2026-10-11 (commit `d1de4ea`)
**Fix for the silent loss of the saved level on load (R3-01, HIGH finding of the LEVEL-R3 review).**

### Historical R3-01 fixes

- **`Character.Load(int)` demoted the saved level.** The load clamp
  `ExperienceLevel = Mathf.Min(MaxLevel, CharacterSaveFile.ExperienceLevel)` uses exactly the
  `Character.MaxLevel` property that this mod patches, and runs **before** `ExperienceLevel` is
  assigned — at that instant `Character.Level` is still ~1 and does not protect the saved level. With a voluntary cap
  `Progression.MaxLevel = N` (≥ 21) a save above `N` was demoted to `N`; and the
  fallback path (group not applied / network unavailable / backend unavailable) returned the vanilla cap
  **30**, truncating saves above 30. The clamped value was persisted
  (`CharacterSaveFile.ExperienceLevel`), that is, the loss was silent and durable.
  Fix: while the character is not loaded (`IsLoaded == false`) the patched getter never
  returns a value below `CharacterSaveFile.ExperienceLevel` — on **every** path, including
  the vanilla fallback. Outside the load path behaviour does not change; campaign/AI/out-of-scope remain
  vanilla. The `GiveExperience` path still does not bounce below the current level.
- New coverage on the bench (12 checks, `loadclamp` suite): a structural anchor in the real IL of
  `Character.Load(int)` (single window `Mathf.Min(get_MaxLevel, CharacterSaveFile.get_ExperienceLevel)`
  → `set_ExperienceLevel`), proof that the clamp getter is the same target as the postfix, and a reproduction
  of the clamp with the pair (effective MaxLevel, saved level) — green with the fix and **red** with the
  defect re-planted.

### Compatibility

- No behaviour change for campaign, AI, multiplayer or already-loaded characters.
  The configuration, GUID and scope decisions of 0.1.0 remain intact.

## 0.1.0

**First implementation in preparation (commit `cd8e4ce`, 2026-10-11), never published.** A new mod (no existing mod file was changed), standalone
BepInEx 5 + Harmony, no ModAPI, no BetterStats/RSTV.

### Gameplay

- **Level 20 cap removed in Roguelike mode (singleplayer).** The comparison
  `character.Level < settings.RoguelikeMaxLevel` of the battle result block
  (`Root.SendGameCompleteFromServer`) becomes `Policy.CanAdvance(Character, RoguelikeSettings)`.
  The patch is **structural**: it recognises the window by the member signatures
  (`Character::get_Level`, `GlobalSettingsManager::get_instance`,
  `GlobalSettingsManager::roguelikeManager`, `RoguelikeSettings::RoguelikeMaxLevel`, `bge`),
  requires **exactly one** match and preserves labels/exception blocks; there is no local
  index or hard-coded IL offset. `bge` → `brfalse` to the **same destination**, so a refusal
  by the policy skips **reward and list** together.
- **One level per victory**, with the vanilla attributes derived from `Level` and skills/items
  while eligible.
- **XP extended past 20, linear and O(1)**, derived from `F20`/`D20` read from the game itself
  (`Character.GetExperienceFloorForLevel(20)`/`(21)`); at `L = 20` and `L = 21` the extension coincides
  with vanilla by construction. The inverse is analytic (no unbounded loop) and the XP queries of
  the 5 static converters only hold inside an explicit per-character scope —
  campaign and AI remain intact. The legacy XP mirror is limited to level 20 for an extended
  character (the real `ExperienceLevel` remains the source and keeps being saved).
- **Rewards with an exhausted pool.** Empty skill pool: the stage is skipped **after**
  writing a durable receipt (S) and the S is subtracted from the queue count; if the receipt does not
  write, the stage is **not** skipped (the reward is not consumed). Empty item pool: the `null`
  fallback is blocked and the flow moves on to attributes. A reroll with `forcedTier` and no option is
  cancelled (the original skill is preserved). The shared `LevelUpSequenceOrder` order is **not**
  changed.
- **Sidecar v1** in `Paths.ConfigPath/com.gumatos.roguelikeunlimitedlevelprogression/receipts/<guid>.json`
  (`schema_version`, `character_guid`, `run_id`, `preset_guid`, `skipped_skill_receipts[]`),
  atomic write (temporary + replace + `.bak` backup), dedupe by ordinal. The run is only
  reset **after** a valid `SyncCharacterToPreset`; a null preset does not reset; a
  corrupted/unreadable ledger does not consume a reward.
- **Multiplayer:** the vanilla branch is kept, with a warning that extended saves/ledger are not
  supported in this version.

### Historical validation baseline (0.1.0 harness snapshot; not the current total)

- Harness `tests/RoguelikeUnlimitedLevelProgression.Harness` (net6.0) that compiles the **real sources** of the
  mod and exercises: the real transpiler over the **real IL** of the reference `Assembly-CSharp.dll`
  (hash `8bb4a7c5…7855a`), with 12 counterproofs (single window, removal of `get_Level`, `bgE`→`brfalse`
  with the same destination, preserved labels, refusal on ambiguity/unsafe target/missing reward
  tail, absence of partial mutation); the policy matrix (19→20, 20→21, 29→30, 30→31,
  guards for AI/campaign/multiplayer/mode/voluntary cap/representation limit/missing target);
  the XP curve (monotonicity, inverse, precision, budget in `long`); the ledger (reload,
  dedupe, corrupted, unknown schema, divergent identity, write failure **without**
  consuming a reward, reset only with a valid preset, atomic backup); and the scope guards of the
  static patch entries.
- 91 PASS checks, 0 FAIL, 14 `NAO_EXERCITADO` items declared with a reason (real application
  of the patches in Harmony, game open, owner's save/reload, multiplayer, serialized real
  `F20`/`D20`, UI at runtime).

### Fixes found by the bench

- **`ReceiptLedgerStore.Save`: the directory creation was outside the `try`.** A disk/permission
  failure escaped as a raw `IOException` instead of `LedgerWriteException`, that is, the
  write failure could cross the reward flow instead of being treated as "do not
  consume the reward". It moved inside the `try` — exercised by a real test.
- **Member resolution without `AccessTools`.** The targets are now resolved by direct reflection
  (`Patches/Reflect.cs`): HarmonyX's `AccessTools` static initializer breaks on
  modern runtimes (`MethodInvoker.GetHandler(null)`, because `Exception::PrepForRemoting`/
  `FixRemotingException` do not exist outside old Mono) and that is an initialization
  dependency the mod does not need. A missing target still returns `null` → fail-closed.
- **Patch plans keep `MethodInfo`** instead of `HarmonyMethod` (the `HarmonyMethod`
  is created only at apply time), which made the resolution of the 20 targets
  exercisable on the bench.
