# Changelog — BetterPortuguese

> Dates use ISO 8601 (BRT, UTC−03:00). Preparation dates are not publication dates.
> CHG-REV documentation audit: 2026-10-16. No publication performed.
> BP-6 packaging: 2026-10-17 (BRT). Release package built and pre-flighted; nothing published.

## 0.1.0 — in preparation (implementation recorded on 2026-10-13)

- Independent BetterPortuguese project, GUID com.gumatos.betterportuguese; no game assets edited.
- Two complete Original/Corrigido snapshots, embedded and accompanied by auditable copies/hashes in the package.
- Corrigido is the default; Original mode returns the game's localization exactly as recorded in the snapshot.
- **Dataset:** 1,314 owner-approved corrections applied (text edits to existing entries plus `addEntry` for records the game left empty). The offline suite asserts that count and the packager recomputes it as `contentState`; per-file SHA-256 lives in `plugins/BetterPortuguese/Data/manifest.json`, not in this changelog.
- Only owner-approved corrections are applied, and approval is not the same thing as runtime proof. The in-game acceptance run recorded so far exercised an earlier, 14-correction build (`BetterPortuguese.dll` SHA-256 `2fc17bf4ed46300a4973c63d8ee6f892a7bf5bbcb6ec6ec138bc394062ac05b4`); **the in-game round for this 0.1.0 package is pending**. Approval, build, packing and runtime validation are separate gates, and a green build never authorizes publication.
- Strict parser, diff/approval validation, ordinal lookup, full baseline and clones on override. An approved `addEntry` can create one neutral value for a record the game left empty, keeping that record's functional tokens/tags; populated lists, gender variants and removals are refused.
- Main-thread configuration/queue, runtime .cfg reading, targeted UI refresh and safe failure/capped logging.
- Separate, empty mod registry; no approved translations/adapters in this snapshot.
- **Icon:** the local artwork changed after `917c20a`; this does not modify the snapshots or imply editorial approval.
- Debug/Release and offline core/API/resource/Harmony test bench. Nothing published in this delivery; publication requires the owner's explicit go-ahead.
