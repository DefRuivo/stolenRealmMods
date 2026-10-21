# Changelog — BetterTooltips

> Publication dates use ISO 8601 (BRT, UTC−03:00); undated older headings do not assert a release date.
> CHG-REV documentation audit: 2026-10-16. These repository corrections do not modify previously published ZIPs.

## 0.1.6 — Unreleased

- **Absolute per-turn value on shrine auras that regenerate (owner request, 21/10).** The active-shrine line
  used to show only the percentage (`Vida por turno +10% (total +10%)`). It now appends the actual amount
  for the current character: `= N de vida por turno` (and the same for mana). The number is
  `MaxHealth x total% / 100` using the SAME total already shown, so shrine/gear bonuses are already in it;
  with no readable base the suffix is omitted instead of guessing.
- BetterPortuguese's adapter is pinned to this version (`ModCatalog.BetterTooltipsVersion`), so both were
  bumped together: 0.1.5 -> 0.1.6.

## 0.1.5 — Unreleased

- Added the README source/contribution block linking to https://github.com/DefRuivo/stolenRealmMods for source code, issues, contributions and forks.
- Documentation release: no new tooltip behaviour. The plugin reports the new package version; the existing RV-49 display decision remains open.

## 0.1.4 — 2026-10-07 — the Armor note stops leaking into the combat feed

**What a player sees:** the explanation of how Armor works also showed up in the **combat feed**
(the line `Increased Armor Applied`); it now appears **only** inside item/skill tooltips. The two
**danger** shrine auras (Decay/Flame) keep the number the previous version showed — see the note on
**RV-49** below, which is **still open** and is **not** closed by this file.

- **BUG-34 — the Armor/Resistance note no longer leaks into the combat feed.** The note went into the
  funnel that localises **every** text in the game, and the feed builds its line from a template
  (`[status] Applied`) — the mod was guarding only the status NAME, not the template. The mod now knows
  **where** the text came from (tooltip body × feed) and the note goes **only** into the tooltip body. The
  legitimate tooltip notes still apply.
- **RV-30 (correction) — danger auras (Decay/Flame): the number shown does not include the bonus.**
  The mod used to write the focused character into the slot where those two auras' formula reads the
  *Shrine Effect Bonus*. The correction stops writing there, and the number those lines show is now
  evaluated **without** the bonus. **Whether that is the right number is an OPEN decision (RV-49), not
  a settled fact.** The owner confirmed the *doubling* seen in game is correct, and a later reading of
  the damage path (`t_d02f9212`, 06/10) found that slot holds the bonus of the character **who has the
  aura** (`UseTriggerSource = 0`) — which is exactly where the doubling comes from. What decides
  whether the tooltip should show the number **with** or **without** that bonus is an in-game
  measurement (`docs/CONFERENCIA-DONO-06-10.md` §4.1), **not** this text.
- **NOT A FACT — kept on the record for correction (REL-BT-014, 07/10).** Three statements an earlier
  draft of this file made are wrong and must not be read as approved:
  - "the doubling was a **defect of this mod**" — **wrong**: the owner confirmed the doubling is
    **correct** and the game's own damage path produces it (see RV-30 above);
  - "the danger auras scale with the **shrine's** bonus, not yours" — **wrong**: in the damage path the
    action's `Source` is the character **the aura is on**, not the shrine's empty character;
  - "there is **no** player *Worship* perk" — this may only be said as **"not found in the code and
    data we read"**: the word's only located trace is an *enemy* CharacterInfo, `T2_Worshiper`. An
    absence in the censuses/code is **not** an absence in the game's assets, so it is not evidence
    against the doubling.
- **BUG-34 has the owner's in-game acceptance (registered 05/10 and 06/10).** It is **not** reopened
  here, and no new acceptance is requested for it.
- **RV-28 (hardening) — the Sustenance healing number can no longer bring the tooltip down.** To compute
  the globules' healing the mod reads the maximum health and mana of the character in focus; outside a
  player context (inspection, shop, the shrine's empty character) that attribute **does not exist** and
  the engine read **threw**. The attribute is now checked **before** the read: without it, the tooltip
  stays **as the game wrote it** and the log says why (nothing is estimated).
- **Hook robustness (TRV-1).** The synergy line read the game method's arguments by **position**; one of
  them is a `float`, and read as an object it brought the game down with 112 exceptions per frame. The
  hooks now read the arguments **by name** — if the game renames something, the hook is refused with the
  name in the log, instead of silently reading the wrong slot.
- **Documentation (RV-48 / TX-1) — corrected 07/10.** The older note stated that there is **no**
  player `Worship` perk (the term having zero occurrences in the game's code; the only trace being an
  *enemy*, `T2_Worshiper`). It may only be stated as **"not found in the code and data we read"** —
  zero occurrences in the code is not proof of absence in the assets — and the owner confirmed the
  *doubling* registered in game is **correct**. **No displayed number changed because of this.**
- **Version:** 0.1.3 -> **0.1.4** in the four places (`<Version>` in the `.csproj`, `version_number` in the
  `manifest.json`, the literal in `[BepInPlugin(...)]` in `Plugin.cs`, and the `- **Version:**` line in the
  `README.md`).

### RV-48 — 2026-10-03 — documentation retraction (corrected 2026-10-07)

The original investigation did not find a player `Worship` perk in the code/data it inspected; it found an enemy `T2_Worshiper`. That is not proof that no such player asset exists. The original claim that the doubling was a defect introduced by this mod and that the damage path used the shrine's bonus was also withdrawn: the owner confirmed the doubling, and the later damage-path reading found `Source` to be the character carrying the aura. RV-30 stopped injecting `Source` in the tooltip evaluator; that code change alone does not settle the number the tooltip should display. RV-49 remains open. This paragraph replaces the repeated false claims, not the owner's acceptance of BUG-34.

## 0.1.3 — enemy passives with values + absolute Armor/Magic Armor (BT-18..20)

**Enemy passives (BT-18/19):** the tooltip of passives (`SpecialEffect`) now shows what was missing —
Regenerating (20% of Max Health per turn), Teleporting (does not trigger while rooted/stunned), Cursed
(only a harmful skill without Curse), Vengeful (death of an ally). **Redemptive** gets an honest
qualitative note (the healing comes from the skill cast on death; the exact number waits for an in-game
measurement).

**Absolute Armor/Magic Armor (BT-20):** flat-conversion skills (eg **Body and Soul** = Vitality×5 → Armor,
Intelligence×5 → Magic Armor) show the value computed with the current stats. Skills whose value already
appears through the engine's token (Invulnerable Winter) stay out.

## 0.1.2 — dynamic value in passives + log marker for the shrine auras

- **Other changes already present by this source series (not future features):** DWA-2 (`46fde11`, 2026-09-30) keeps Dwarven trigger chances **per live instance**, rather than applying the attribute-aura deduplication to them. CHL-1 (`c5eeb5c`) adds the status/skill interaction note using the caster's actual value. The three-colour/note-order fixes (`d586f28`) keep level-2 text distinct from the level-3 note and place notes at the tooltip end; the synergy ordering and weapon notes are recorded in `716ca22`. These were missing from this history; they are not newly added by CHG-REV.

The passives (**Reaper's Toll**, **Hunger**, **Berserker's Blood**) and the **% attribute** skills now
show the **computed dynamic** value (BT-10..BT-13). The log marker for the shrine auras also publishes the
**floor** and the **raw** value (MAN-2/REV-47, log only — no text the player sees changes).

### MAN-2 / REV-47 — 2026-10-02 — floor/raw log fields (incorporated in 0.1.2)

Fix of **two holes in the log/dump marker** for the shrine auras (findings 3 and 1 of REV-47).
**LOG marks only**: no text the player sees, no formula and no number convention
(the sheet integer of RV-45, the single sign of 46acd97) change — the displayed number is still the engine's.

- **The FLOOR was invisible.** `MarcaTeto`/`TetoDoAtributo` (`ShrineAuraPatch.cs`) only looked at the `HasMax`:
  an attribute with a FLOOR (`HasMin`/`MinValue`) **never produced a line**, and from the log one could prove
  NEITHER side — `ManaCostMod` looked like "no ceiling at all" (the data only showed up when the asset was read
  by hand). The marker now looks at `HasMin`/`MinValue` and emits its own line
  `RV-46 piso '<atributo>': MinValue=<valor> total=...% cru=...% no-piso=sim|nao`. In the asset,
  `ManaCostMod` has `HasMin` with MinValue **−75** (`resources.assets` @1519616544) and no `HasMax`.
- **The RAW value did not exist.** The marker printed only the total **already clamped** — with **TWO**
  `Guardian Aura` the `Damage taken` read `total=+50%` (the `MaxValue`) and the raw value (90) had to be
  **inferred** from the sum per instance proved in RV-46. The field `cru=` was added next to `total` in both
  limit lines, and the value **is not estimated**: it is the number the engine computes BEFORE the clamp,
  through its public path (`GetAttributeValueByMethod` + `SavedMap` + `CalculateAttribute`) — the patch
  replicates the logic of `Character.CalculateAttributeViaSweeps` (PRIVATE in the decompiled source, NOT
  called by the patch); without a reading, the field simply is not emitted.

No Harmony changed (still the single prefix in `ApplyDescriptionExpressions`, `ref __2`); all the new work
is read-only code inside try/catch. `tools/checa_shrines.py` now reads the `cru=` (optional, for a log from
an older build) and the floor line, showed both in the section `LIMITES DO ATRIBUTO NO LOG` and uses the
floor (as it already used the ceiling) in the ADITIVIDADE block.

### RV-46 — 2026-09-30 — historical changes shipped in 0.1.1 (not an unreleased entry)

> Attribute-aura deduplication remains in use, but DWA-2 (`46fde11`) subsequently retained every live Dwarven trigger instance. The statement below that each aura counts once describes the original RV-46 step, not a universal rule for all effects in the current code. The old launch-day wording mixed timezones; this audit does not assert an unverified historical publication day.

Fix of **two defects** in the `Your active shrine auras:` line. **No damage formula, no formatting
convention (the Ceil of RV-45, the single sign of 46acd97) and none of the 12 text notes changed** — what
changed was WHICH number goes into each item and WHICH auras become an item.

- **RV-46 — the auras' contribution was MULTIPLIED (`Dodge +120%` with the aura worth 40).** Proven cause:
  `AurasVivas` returns ALL `Character.ActionStatuses` entries matching the family and the contribution was
  summed per ENTRY — and the live list carries the **SAME aura repeated**, because every (re)entry into the
  area of the ground effect creates a NEW status (`GroundEffect.AddGroundEffectedPlayer`) and the engine
  only removes `Infinite` statuses (the shrine aura is not one). In the owner's game log (30/09) the same
  hover shows the list with `Rogue Aura` **three** times and `aura=+120%`, with the `RV-44 soma` saying
  `stacks=1` in each instance: 3 × 40. **It was not a stack.** Fix: the contribution counts **each aura
  ONCE** (`AurasUnicas`) — 40, which is the number on the shrine's own white line and what the engine
  evaluates in the asset's expression. **The total is still the engine's** (`Character[atributo]`): it stops
  at 75 because the game's attributes have a CEILING (`CharacterAttribute.HasMax`; `DodgeChance`
  **MaxValue 75** and `DamageReduction` **MaxValue 50** in the asset) and the engine clamps the total there
  (`Character.GetAttribute`). The repeats and the ceiling go to the LOG (`instancias=[Nome xN]`,
  `RV-46 teto`), never into the number.
- **RV-46 — live aura outside the list: the Dwarven did not appear.** Cause: the items come out per
  CHARACTER attribute and the Dwarven effect **is not an attribute** — the value lives in the **trigger
  chance** (`OnHittingDamaging` -> `Stunned`, `SkillTriggers[].ActionStatusChanceEquations`): in the asset
  (`Dwarven Totem Aura Status`, `resources.assets` @1517115056) the formula
  `Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100)))` appears 2× (@1517115395, next to the
  description, and @1517115647, inside the trigger) and the value with bonus 100 is 40 — the same as the
  shrine's white line. Fix: its own item **`Stun chance +40%`**, evaluated by the engine with the focused
  character. By the same rule the other two of the 12 auras without a character attribute came in: Decay
  (`Shadow damage per turn N`) and Flame (`Fire damage to attackers: …`).
- **Rule that stays (owner, 30/09):** the line is called "Your active shrine auras" and presents itself as
  COMPLETE — a live aura that does not become an item goes to the LOG with the reason (`RV-46 AVISO`),
  never silently.
- **Mechanical check:** `tools/checa_shrines.py` now reads the `instancias=` field, the items without an
  attribute and the `RV-46 teto`; the **Dwarven case stopped being `NAO-VER`** (it compares the item with the
  `contribuicao_esperada` column of the table) and a hover with several auras (the owner's screenshot) became
  checkable. Counter-proof in `tools/fixtures/shrines-rv46-dedupe.log` (exit 0).

## 0.1.1

Fix of **text/label** in the shrine tooltips (RV-43). **No number, formula or calculation logic changed in
THESE text fixes** — the independent audit confirmed 9/9 of the buff-aura values (plus Flame and Decay).
**The 0.1.1 that is live carries more than a label:** RV-44 (bullet below) and RV-46 (section above) went
into this SAME version and changed WHICH number goes into the line — the version did not go up again; the
sentence "no calculation changed" grew old and holds only for the text fixes.

- **RV-43 — the `Fury` note was the only one of the 9 shrine auras without the base and without the bonus
  chain.** Cause: the key `Damage increased by [0]%. Damage taken increased by [0]%. ` was in `TextAppends`
  with the old `RV-9` note (just the healing sentence) — it did not say it is a shrine aura, it gave no base
  and did not cite the *Shrine Effect Bonus*. Fix: the note became `Base 25% damage and +25% damage taken. The value shown already includes the Shrine Effect Bonus (Omnism I/II in Chaos; the Worshiper's Worship perk, +100% effect from Shrines; Horn of Devotion).` and the **healing sentence stayed** (it was not
  false: the engine adds `DamageMod` to healing) — the note now also covers the shrine. **Correction of the historical wording:** that draft cited a player `Worship` perk without locating such an asset. TX-1 (`95ca3f3`) removed that citation; the current note does not cite it. Failure to locate it is not proof of universal absence. The 25/25 base comes from the asset (`status.csv:205`:
  `DamageMod:Base:Mathf.Round(25 * (1 + Target["ShrineEffectBonus"]/100))` and the `DamageReduction`
  mirrored at -25). The key stays **only** in `TextAppends`: the game's original text did not change, so
  nothing migrated to `TextFixes` (the same key in both tables brings the mod down — INC-1;
  `check_chave_compartilhada.py --estrito` = 0).
- **RV-43 — the `ManaCostMod` label (Energy Coil) broke with a POSITIVE total.** Cause: `Format` did
  `"Mana Costs reduced by " + (-v)`, assuming a negative total. Real POSITIVE sources of the same attribute
  exist — `Forbidden Power` `ManaCostMod:Base:50` (`status.csv:191`) and `Fuel for the Flames I/II` +20/+30
  (`skills.csv:178-179`): a Fire character with +70 inside the Energy Coil (-50) has a total of **+20** and
  the line printed `Mana Costs reduced by -20%`. Fix: total <= 0 = `Mana Costs reduced by |v|`; total > 0 =
  `Mana Costs increased by v`.
- **RV-43 — the same class of sign in the other attributes (a latent defect).** Cause: `DamageMod`,
  `CritChance`, `DodgeChance`, `LifeOnHit`, `HealthPerTurnPercent` and `ManaPerTurnPercent` built a fixed
  `+` and would print `+ -X%` with a negative total. Fix: all of them go through the same sign helper (`+`
  for positive/zero, `−` for negative), in the format of the unknown-attribute label. **The text for a
  positive total — today's correct behaviour — did not change.**
- **RV-43 — the `Flame Shrine` note contradicted itself.** Cause: the note stated that the maximum health
  used was not that of whoever is inside the aura, but the per-target list uses exactly the occupant's
  `MaxHealth` — the mod projects each occupant AS IF it were the attacker, because on hover one does not know
  who will attack (an explicit hypothesis, accepted by the owner). Fix: the clause now reads `the number is the projection of THIS character as the attacker - if this character attacked` and the contradictory
  sentence came out; the scale, the "before the reductions" mark and the origin of the bonus stayed as they
  were.
- **RV-44 — the `Your active shrine auras:` line showed the character's TOTAL, not what the auras deliver.**
  Cause (proved in the code): the item came straight from the engine's indexer, `Character[atributo]`
  (`ShrineAuraPatch.cs`, `AcumuladoShrines` — it was `float valor = receptor[nome];`), which is the sheet's
  final total (base + gear + skills + auras). On a 25% aura the line said the character's total, which on
  screen reads as "the aura gives 50%". Owner's screenshots (30/09): Goblin Battle Standard (Fury) without
  `Worship` -> shrine tooltip `25%` / line `Damage +50%` and `Damage taken +5%`; with `Worship` -> `50%` /
  `Damage +75%` and `Damage taken +30%`; Rogue Shrine with `Worship` -> tooltip `40%` / line `Dodge +57%`.
  Fix: each item became **`<what the auras deliver> (total <the character's total>%)`** —
  `Damage +25% (total +50%)`, `Damage taken +25% (total +5%)`, `Dodge +40% (total +57%)` —, with the
  contribution coming from the **real `AttributeEffects` of each LIVE aura** (the SAME expression the shrine
  tooltip shows: `Mathf.Round(20 * (1 + Target["ShrineEffectBonus"]/100))` etc., evaluated by the engine),
  and **two auras on the same attribute add their contributions** (Warrior + Fury on `Damage`), never the
  sheet's total. The total stays in parentheses, read from the indexer: it is the sheet's number (BetterStats).
  **No aura formula, text or note changed** — the Rogue note (`Increases dodge chance by [0]%.` ->
  `Base 20%. The value shown already includes the Shrine Effect Bonus (...)`) is the same as in 0.1.1 and
  remains correct on screen. Fallback: with no separable contribution (a `Multiplicative`/`Set` effect — the
  family has none: the 9 buff auras, all the ones that have `AttributeEffects`, are `Base`), the item comes
  out with the total, as before. **Correction of the old RV-48 retraction:** the "with/without `Worship`" labels belong to the original report, not proof of a located player asset. The claim that the 100 bonus/doubling was caused by a defect in this mod was withdrawn; the owner confirmed the doubling and the damage path reads the aura carrier as `Source`. See 0.1.4; RV-49 remains open.
- **Version:** 0.1.0 -> **0.1.1** in the three places (`<Version>` in the `.csproj`, `version_number` in the
  `manifest.json`, the literal in `[BepInPlugin(...)]` in the `Plugin.cs`).

## 0.1.0

First published version.

- **Rewrites skill and status tooltips that were incomplete**: when the official text hides something that
  changes the player's decision (which attribute the number depends on, stack limit, duration, who is
  affected, trigger, number of hits), the missing explanation is added at the end of the tooltip.
- **Fixes objective text defects** — spelling (`benefical`, `additonal`), punctuation and double spaces — via
  a correction table matched by the exact text.
- The mechanic note goes in the **game's own special text colour** and is positioned **after the costs and the
  range**, at the end of the tooltip body.
- **No gameplay change whatsoever**: the mod only rewrites strings in the localisation funnel
  (`OptionsManager.Localize`).

### Dynamic shrine numbers — historical evolution, not all current 0.1.0 behaviour

- The shrine family has twelve keys, not twelve attribute-buff auras: nine carry attribute effects, Dwarven carries a trigger chance, and Decay/Flame are danger auras. The tooltip evaluator uses the focused character where supported; uncertain context leaves the original text intact and logs why.
- The original `Your active shrine auras:` block read character totals. RV-44 separated aura contribution from the final total; RV-46 added deduplication and the missing non-attribute effects; DWA-2 retained every live Dwarven trigger instance. The current rule is therefore not universally "one item per attribute" or "each aura once".
- Decay adds a raw damage projection based on maximum health; Flame lists projections for characters in the aura as possible attackers. These are **before damage reduction**, not predictions of the final mitigated damage. RV-30 stopped injecting the focused character into the danger-aura `Source` slot when evaluating tooltip expressions.
- **Correction of the old causal claim:** the damage path uses the character carrying the aura as `Source`; the owner confirmed the doubling. It must not be called a defect of the mod or attributed to the shrine's own bonus. Whether the tooltip projection should include that bonus remains RV-49, not a conclusion of this changelog. A player `Worship` asset was not located in the inspected corpus; that does not prove its universal absence.
- `Sustenance I/II` adds healing information to globules and to the six potion-pickup descriptions, not to potion inventory items just because they share a title. It reads the active `Character.Skills` and the engine's expressions; the data-backed tier cases are I = 8% and II = 20%. The older 28% example was a hypothetical list containing both tiers, not a validated player outcome; the RV-28 matrix in `573596d` records 8/16 and 20/40 for the 100/200 pools, not 28/56.
- Missing character/attribute or an expression that cannot be evaluated leaves the game's text in place. The maximum-health/mana existence guard was hardened in `573596d` and belongs to the 0.1.4 history above.

### Not in this mod

- No gameplay formula or mitigation is applied by this mod; the changes are presentation/context for tooltips.
- The Chaos tree's deliberately hidden random outcome is not revealed.
- BUG-34's recorded acceptance is preserved. The danger-aura display decision RV-49 remains separate and open; a code/asset audit is not a new visual acceptance.
