# Changelog — BetterCombatText

> Publication dates use ISO 8601 (BRT, UTC−03:00); undated older headings do not assert a release date.
> CHG-REV documentation audit: 2026-10-16. These repository corrections do not modify previously published ZIPs.

## 0.1.6 — Unreleased

- **Names now match the game's cap height, case and (almost) width (BF-STYLE-3b/3c).** Paired combat
  captures show the game draws enemy names in upper case, so two opt-in keys were added and enabled by
  default for the enemy-name surface only: `CaixaAlta` (`FontStyles.UpperCase`) and `EspacamentoExtra`
  (`characterSpacing`).
- Clean paired runs (no concurrent change to the owner's profile, 13 captures, 1920x1080):
  cap height **18 px = 18 px** in all three names. Total advance measured with `EspacamentoExtra=0`:
  246.2 vs 251.8 px (Goblin Marauder), 99.3 vs 107.7 (Knight), 79.2 vs 78.5 (Briar); with `=22` it
  overshoots (326.1 / 133.6 / 107.7). The shipped default **2** is the least-squares fit between those
  two measured points — it is an interpolation, not itself a measured capture.
- Earlier calibration done on lower-case renders (spacing 22) was wrong: upper case widens the glyphs and
  most of that tracking became unnecessary.

## 0.1.5 — Unreleased

- **Enemy-name styling calibrated against the real render (BF-STYLE-3).** Default outline for combat enemy
  names moved from `_OutlineWidth 0.22` / `_OutlineSoftness 0.05` to **0.35 / 0.10**, and the default
  underlay shadow is now **off** for that surface. Evidence: the paired combat capture (13 pairs, same
  scenario, `PlayerInfoWindow`/`StatusIcon` handlers) measured cap height **18 px in both conditions** for
  three different names, where the previous defaults rendered heavier than the game's own Trajan styling.
- New opt-in keys on the TMP style sections: `HerdarGeometria` (use the original material's outline/shadow/
  `_FaceDilate` instead of the configured numbers; colour and alpha still come from the cfg) and
  `DilatarFace` (writes `_FaceDilate`, previously not exposed). Both default to the old behaviour.
- Known limit, measured: Times New Roman is narrower than the game's Trajan for these names (advance
  ~12.3 px vs ~18.0 px per glyph at 1080p). Matching the original width would require `characterSpacing`,
  which this mod does not expose yet.

## 0.1.4 — Unreleased

- Added the README source/contribution block linking to https://github.com/DefRuivo/stolenRealmMods for source code, issues, contributions and forks.
- Documentation release: no new combat-text styling behaviour. The plugin reports the new package version.

## 0.1.3 — 2026-10-16

**Documentation and dependency metadata release; the visual code is unchanged.** The DLL differs from 0.1.2 only in the version literal it reports.

- **Dependency metadata:** `manifest.json` **stopped declaring** `DefRuivo_StolenRealmMods-BetterFont-1.0.3`. The mod does not reference BetterFont: the only mention in the code is an explanatory comment (`Plugin.cs:101`) and the visual integration is optional — that is why the mandatory dependency was removed in the DEP-REV dependency audit (2026-10-16). A package that requires BetterFont makes the manager install a mod this one does not need.
- **README aligned:** the *Needs* line and the *Together with BetterFont* section said that BetterFont was mandatory and that "this package's dependency points at that version". Both now say what the manifest says since DEP-REV: only BepInEx, with BetterFont as an optional integration.

## 0.1.2 — 2026-10-07

**Visual code unchanged; package documentation and dependency changed.** No new visual behaviour is added over 0.1.1; the source bump itself only changes the version literal, while the package also changes the README and BetterFont dependency.

- **Dependency metadata:** `BetterFont-1.0.2` → `BetterFont-1.0.3` in `manifest.json` (commit `0d33ef3`). The dependency change does not change this mod's gameplay/visual code, but this was not a documentation-only package change.
- **The build instructions were wrong about the deploy.** They said that a bare `dotnet build` would also copy the mod into the mod-manager profile. That is no longer true: the deploy is **opt-in** — a bare `dotnet build` installs **nothing**, and only `-p:DeployToBepInEx=true` copies the DLL into `<profile>\BepInEx\plugins\BetterCombatText\`.
- **The README described the wrong outline for the enemy names.** It said "soft outline/halo, default black at 10% alpha". That was true of the first release, not of 0.1.1: since then the enemy name gets a **hard, opaque black outline** (`LarguraContorno` 0.22, `SuavidadeContorno` 0.05, `AlfaContorno` 0.95), the **10% is the buff/debuff label**, and the enemy name's shadow is short and visible (`AlfaSombra` 0.75, offset ±0.35, softness 0.05), with `Fundo` proposing the polarity subject to the font-brightness veto (a light letter receives a dark shadow and vice versa, not just when `Fundo = auto`). The table of surfaces and the configuration section now state the real defaults.
- **Still not verified on screen.** The visual result of this mod has never been confirmed in game — a startup diagnostic proved the effect is *possible* on those texts, but nobody has confirmed it on the screen. This release does **not** change that, and the README and the package description keep saying it.

## 0.1.1 — hard/opaque black outline (UI/UX) + adaptive shadow by contrast

The enemy name (quality colour) gained a **HARD, OPAQUE black outline** (`_OutlineWidth` 0.22, `_OutlineSoftness` 0.05 — it was 0.50, the defect that blurred the outline until it disappeared, `_OutlineColor` alpha 0.95) and the **shadow** became a conservative short offset (`_Underlay` offset ±0.35 — it was ±2, outside the shader's ±1 range — alpha 0.75, softness 0.05). The adaptive shadow picks the side by the **contrast with the FONT** (light font → dark shadow, and vice versa). UI/UX review: the fill colour **does not change** — it is the rarity language (`QualityColors[EnemyType]`).

### BCT-5 — 2026-10-02 — the shadow CONTRASTS with the FONT (historical step incorporated into 0.1.1)

**Defect reported by the owner:** the shadow of the enemy name was still "the same colour as the font".
Investigation closed with three findings:

1. **The profile `.cfg` had a WRONG value (the cause of "same colour").** The line
   `CorSombraClara = CBB396` of `BepInEx/config/com.gumatos.bettercombattext.cfg` was inherited from an
   old build: `#CBB396` is the game's **own text colour** (`highlightedColor`/
   `specialDescColor`) and the common colour of the enemy name. BepInEx **does not rewrite a key that already
   exists** when the code default changes — so the new BCT-4 default (`FFFFFF`) never reached the
   installation, and the "light bucket" stayed switched on the font's own colour. (The profile DLL
   **was** the most recent one — sha256 identical to `bin/Release`; the problem was not the build.)
2. **The BCT-4 threshold had a hole.** `UsaSombraClara` only flipped the bucket when the chosen colour
   was within `ContrasteMinimo` (0.2) of the letter. The beige `#CBB396` against the white `#FFFFFF`
   differs by **0.283** — it passed, and the LIGHT letter of the name received the LIGHT shadow (light over light).
   With the inherited `CBB396` the same hole hit the **white** letter (`CharacterNameColor =
   Color.white`), which got the beige.
3. **The alpha was low.** `alfaSombra = 0.35` on the Names: the dark shadow at 35% over the field
   came out translucent and blended with the glyph itself.

**THE RULE (BCT-5) — the letter dictates the SIDE:**

- The shadow must be on the **opposite side** of the font luminance: **LIGHT letter → DARK shadow
  `#000000`; DARK letter → LIGHT shadow `#FFFFFF`**. No threshold: the SIDE decides (the BCT-4 threshold
  stays only as a net against a badly configured bucket).
- `Fundo` keeps **proposing** the polarity (BCT-3), but takes the **LETTER'S VETO** when it puts the
  shadow on the same side as the font. That was what the owner was reporting: with a dark background and a light
  letter, the shadow came out light — "the same colour as the font". Now the letter `#CBB396` (enemy name) gets the
  **DARK** shadow.
- **Palette colours:** the light shadow is white `#FFFFFF` (`physicalColor` of the game fixture) and the
  dark one is neutral black `#000000` (the same tone as the default outline). No invented hex.
- **Visibility:** `alfaSombra` of the Names goes from **0.35 → 0.65**.
- **Fix in the profile:** `CorSombraClara  CBB396 → FFFFFF` and `AlfaSombra 0.35 → 0.65` (section
  `2. Nomes de inimigos (combate)`) of the r2modman `.cfg` (backup in `.bak-bct5`). With the veto, the
  inherited value stopped being a trap, but the file is the message the owner reads.
- **Tested invariant:** for EVERY colour of the palette × EVERY `Fundo`, the shadow comes out on the opposite side of the
  letter and contrasts with it. New checks: `t_bct_sombra_polaridade_fonte.py` (section 14 of
  `regras_bct.py`) + the minimum alpha. Proven by failing:
  `tools/testes/bct5-polaridade-fonte-prova-reprovando.log` (the "veto torn out" and the "alpha 0.35"
  FAIL for the right reason; the source is restored byte by byte).

### BCT-4 — 2026-10-02 — contrast with the letter (historical step, incorporated and superseded by BCT-5 in 0.1.1)

**Defect reported by the owner:** the enemy name shadow became invisible/"blob". The log of 02/10
(l.3359) closes the account: `cor da LETRA no alvo='#CBB396' (luminância 0.717 → letra CLARA); sombra que
FICOU no material=_UnderlayColor '#CBB396 alfa=0.35'`. The LIGHT shadow was `#CBB396` — the **SAME
colour as the enemy letter** (which is the game's `highlightedColor`). Shadow equal to the letter = zero
contrast.

- **The BCT-3 rule assumed a DARK LETTER.** It chose the colour only by the BACKGROUND ("dark background →
  light shadow `#CBB396`") without looking at the LETTER — but the enemy name's letter is LIGHT and is
  `#CBB396`: the shadow came out identical to the letter.
- **The new LAW (BCT-4):** the shadow must **contrast with the LETTER** (the glyph is touching it)
  **and with the BACKGROUND** (the shadow falls on it). The POLARITY still comes from the BACKGROUND (BCT-3) and the
  `auto` still comes from the LETTER (BCT-2); what changes is that, if the colour of the chosen bucket **does not
  contrast with the LETTER** (luminance difference < `ContrasteMinimo` = 0.2), **the bucket FLIPS**.
- **The LIGHT shadow becomes PURE WHITE (`#FFFFFF`).** `#CBB396` was the game's own text colour
  (and the common colour of the enemy name). With the letter `#CBB396` on a dark background: shadow
  `#FFFFFF` — contrast with the beige of the letter (0.28 ≥ 0.2) **and** visible on the dark field. Key
  `CorSombraClara` (default `FFFFFF`; whoever prefers the `#CBB396` back edits the `.cfg`).
- **Tested invariant:** for EVERY colour of the game palette × EVERY value of `Fundo`, the chosen shadow
  contrasts with the letter (≥ 0.2). The old rule violated exactly in the reported case.
- **Diagnostics:** the target line now prints the contrast threshold together with the letter colour and the
  `_UnderlayColor` that stayed in the material.
- **Tests:** `tools/testes/testes/puros/t_bct_sombra_contraste_letra.py` (new) + section 14 of
  `regras_bct.py`; `t_bct_sombra_visivel_fundo_escuro.py` and `t_bct_sombra_adaptativa.py`
  updated (the light shadow is now `#FFFFFF`). Proven by failing:
  `tools/testes/bct4-contraste-prova-reprovando.log`.

### R2 — it is NOT the BCT: the "thick shadow" of "Select Attributes" belongs to BetterFont

The owner also reported that the section label of the **level-up window** ("Select Attributes",
`RoguelikeManager.SectionLabelText`, l.168605) came out with a "very thick shadow". Investigation
closed (prefab + log + code):

- **The BCT does not touch that screen.** It patches 7 methods of 7 types (enemy name, status
  labels, dice text, tooltip, health number) — none of them is `RoguelikeManager` — and it writes
  ALWAYS to the PER-COMPONENT material (`fontMaterial`). There is no path to reach the
  `SectionLabelText`. The lock on that: `tools/testes/testes/puros/t_bct_sem_vazamento_no_levelup.py`.
- **The root cause is BetterFont.** The PREFAB read with UnityPy (`Roguelike Manager` [680571] →
  `Label` [680588] → the TMP that the `SectionLabelText` field points to): the material in use is the
  `Regular Font (Minion Pro Regular) SDF Material`, with `_UnderlayColor` black **alpha 0.5**,
  `_UnderlaySoftness`/`_UnderlayDilate`/`_UnderlayOffsetX`/`_UnderlayOffsetY` = **0** and the keyword
  **`UNDERLAY_ON` OFF** (`m_ValidKeywords == []`) — an **INERT** shadow, which the game does NOT
  draw. BetterFont's `CopiarEstilo` decides "shadow in use" by `_UnderlayColor.a > 0.001`
  (the alpha is 0.5) **without looking at the keyword**, turns `UNDERLAY_ON` on in the new material and copies the values:
  the shadow the game never drew starts appearing — the reported "very thick shadow". The
  `AcceptButtonText` of the same prefab shows the same pattern with the `Title Font (Trajan Pro Regular)
  SDF Material` (alpha 0.906).
- **Fix in BetterFont (BF-5), already implemented in `27b5e69`:** shadow recognition
  started using `SombraDesenhada`, observing the keyword or offset/dilate instead of the alpha alone.
  This investigation is not a code change in the BCT and is not a pending future fix.

### BCT-3 — 2026-10-02 — background and colour diagnostics (historical step, incorporated and superseded by BCT-4/5 in 0.1.1)

**Defect reported by the owner:** "sees NO shadow at all on the enemy names" (dark battle
field). Investigation closed and fix:

- **The shadow WAS being written — the defect was the COLOUR.** The log of 02/10 has
  `[Nomes (combate)] APLICADO ... sombra=on` (l.3270) and does **not** have the warning `sem-underlay`
  (which the mod prints when the shader does not expose `_UnderlaySoftness`): therefore the `temUnderlay` branch
  ran and `_UnderlayColor` was written. `sombra=on` is only the config key — it proved
  nothing about the colour.
- **The letter is LIGHT, the background is DARK.** `PlayerInfoWindow.playerName.color` =
  `CharacterNameColor` (= `#` + `GetEnemyQualityColor(EnemyType)`) or `Color.white`
  (l.156815/156849/156850); `BossHealthbar.BossName` uses the prefab colour (l.26641). By the
  BCT-2 rule (shadow from the luminance **of the letter**), light letter → shadow **`#000000`**:
  black over the dark field = **zero contrast**, the shadow exists and does not show.
- **THE RULE CHANGES (recorded):** a drop shadow only shows when it contrasts with what is
  **behind** it — the BACKGROUND, not the letter. New key `Fundo` per surface
  (`escuro` / `claro` / `auto`):
  - `escuro` → **LIGHT** shadow `#CBB396` (the one that shows on the battle field);
  - `claro` → **DARK** shadow `#000000`;
  - `auto` → the BCT-2 rule (luminance of the LETTER), **preserved** for whoever does not declare a background.
  The surface **`2. Nomes de inimigos (combate)` is born with `Fundo = escuro`** (the owner confirmed
  the dark field). The other surfaces (dice, labels, tooltip) stay on `auto` — **no
  behaviour change** in what was already approved. It is a new key in the `.cfg`; the colour rule of
  BCT-2 stays alive in `auto` mode.
- **Colour diagnostics in the log (new):** the startup diagnostic and the target detail now
  print the **LETTER colour** of the target (`#RRGGBB`, alpha and luminance) and the shadow colour that
  **stayed in the material** (`_UnderlayColor`). Before, only `sombra=on` (the config key) came out — it was
  through that gap that "the shadow does not appear" stayed without a number to check.
- **Tests:** `tools/testes/testes/puros/t_bct_sombra_visivel_fundo_escuro.py` + section 13 of
  `regras_bct.py` — the `escuro` background giving a light shadow to the light letter (the fix), the `auto`
  preserving the BCT-2 rule, the per-surface defaults and the rule in the source. Proven by
  failing: with the background of the NAMES back on `auto` and with the rule no longer linking a dark
  background to the light shadow (`tools/testes/bct3-sombra-visivel-prova-reprovando.log`).

### BCT-2 — 2026-10-02 — adaptive shadow (historical step, incorporated and superseded by BCT-3/4/5 in 0.1.1)

The shadow stops being **fixed and equal to the outline** and starts **following the letter colour**.

- **The rule.** The REAL colour of the letter is read from the component itself (`TMP_Text.color` on TMP and
  `UI.Text.color` on the legacy path) and the luminance is Unity's `Color.grayscale`
  (`0.299R + 0.587G + 0.114B`):
  - **DARK letter** (luminance **< 0.5**) → **LIGHT** shadow `CBB396` (the game's
    `specialDescColor`/`highlightedColor`);
  - **LIGHT letter** (luminance **>= 0.5**) → **DARK** shadow `000000` (the neutral black from
    before).
  In the game palette (read from the prefab, `tools/testes/fixtures/cores-do-jogo.entrada.json`) only the
  `shadowColor` #F000FF (~0.395, dark magenta) falls into the light shadow; fire #FF5353 (~0.527),
  cold #00D7FF (~0.609), lightning #EFFF00 (~0.867), healing #6BFF6F (~0.762), mana #66A8FF
  (~0.620) and physical #FFFFFF (1.000) fall into the dark shadow.
- **RE-EVALUATION WITHOUT RE-INSTANTIATING.** The idempotency guard by InstanceID **continues** (the
  material is never re-instantiated). But the game may **REUSE** the same component while swapping the
  colour (the die that becomes fire and then cold): on every call the mod **re-reads the colour** and, if the **bucket**
  flips, updates **ONLY the shadow colour** — `_UnderlayColor` on TMP, `Shadow.effectColor` on the
  legacy path — without `new Material`/`AddComponent`. A reused text no longer keeps the shadow of the
  first colour.
- **CFG-1 — THREE NEW keys in section `1. Geral`** (no existing key was touched):
  - `SombraAdaptativa` (bool, default **true**) — `false` goes back to the previous **FIXED** behaviour (shadow = outline
    colour, independent of the letter);
  - `CorSombraClara` (string, default **`CBB396`**) — shadow of the dark letter;
  - `CorSombraEscura` (string, default **`000000`**) — shadow of the light letter.
- **Tests:** `tools/testes/testes/puros/t_bct_sombra_adaptativa.py` + section 12 of
  `regras_bct.py` — the pure rule (colour → luminance → bucket → hex) reading the palette from the fixture, the
  three keys, the colour read and the **reuse** (bucket that flips) in the idempotency model. Proven by
  failing: with the "fixed shadow that ignores luminance" and with the re-evaluation torn out
  (`tools/testes/bct2-sombra-prova-reprovando.log`).

### Metadata of the same 0.1.1 — dependency/documentation (commit `69c4a56`)

- **Thunderstore dependency: `DefRuivo_StolenRealmMods-BetterFont-1.0.1` -> `1.0.2`.** The 1.0.1
  is published and immutable, and its material gate **refused the material of the combat texts**
  (different shader variant: the targets use `TextMeshPro/Distance Field Overlay` and
  `Distance Field (Surface)`; the serif font comes out with `Mobile/Distance Field`) — with both mods
  on, the combat texts stayed on the **original font**. The fix is **BetterFont 1.0.2**
  (a different variant became a best-effort copy, property by property with `HasProperty`). Without
  bumping this reference, the manager would install 1.0.1 next to this mod and the defect would continue
  in the field. The `DEP_EXTRAS` rule of `tools/audita_docs.py` requires exactly this: whoever declares another
  mod of this repo points at the version it has TODAY in the manifest.
- **Send order (do not invert):** first **BetterFont 1.0.2**; then this **0.1.1**. The Thunderstore
  upload **resolves** every reference (`PackageReferenceValidator(resolve=True)`) and refuses the
  one that does not exist with `No matching package found for reference` — the version declared here needs to
  be live before.
- **Doc fixed:** the README (section "Together with BetterFont" and the Portuguese summary) claimed that
  the combat texts "may keep the original font" with both mods on. That described the
  behaviour of BetterFont 1.0.1, not of this version: with **BetterFont 1.0.2** the combat text
  gets **the serif and the halo/shadow**.

## 0.1.0

First published version.

- **The owner's real icon**, replacing the placeholder (`bc4e5d6`, 2026-09-30); source art preserved in `docs/img/bettercombattext-icon-fonte.png`.
- **Hook applier fixed before the first publication**: the hook class filter copied from RoguelikeSkillTreeVisualizer required `[HarmonyPrefix]`/`[HarmonyPostfix]` **on the method** and this mod declares its **9 hooks through Harmony's naming convention** (a `Postfix` method) — it would have skipped the 9 silently. The filter now requires only `[HarmonyPatch]` **on the TYPE** (the same set that `PatchAll()` processed) and the hooks are applied **one by one**, with a log per hook and a summary with the real count.
- **Cheaper startup diagnostic**: the scene scan went from 2s to 5s and **stops at the first target that appears in the scene** (its own key in the `.cfg`), instead of always scanning every surface.

- **Soft outline/halo on the combat text**: `_OutlineWidth` + `_OutlineSoftness` outline (high = blurred halo, the requested "radial shading") with **black at 10% alpha** by default, plus an optional `_Underlay` diffuse shadow (offset, dilate, softness).
- **Targets, each with its own on/off switch in the `.cfg`**:
  - **Enemy names in combat** — `BossHealthbar.BossName` (boss bar) and `PlayerInfoWindow.playerName` (the hover window over the enemy). Both `TextMeshProUGUI` → soft halo.
  - **Buff and debuff labels/stacks in combat** — `StatusIcon.stackCount` ("x3") and `StatusIcon.turnCount`. They are **legacy** `UnityEngine.UI.Text`, without distance field: they get a hard outline (`Outline`), shadow and **bold**. A soft halo is **impossible** there (recorded in the README and in the startup log).
  - **Dice text in the events** — `DiceVisualSetup.DiceNumbers` (the number on the die face), `DiceRoller.TargetText/ResultText/ModifierValueText`. `TextMeshPro`/`TextMeshProUGUI` → soft halo. Its own group, independent of combat.
  - **Status tooltip (buff name)** — **off by default**: the buff name only appears in the game's generic tooltip, whose component (`Tooltip.Title`/`Description`) is the same as the skill/item/powerup tooltips; turning it on spreads the halo over every tooltip.
  - **Health number over the units** — extra, **off by default**, outside the original request.
- **Material safety**: the effect is applied to a **per-component copy of the material** (`TMP_Text.fontMaterial`, which internally does `new Material(shared)` — confirmed in the IL of `TextMeshProUGUI.GetMaterial`). `fontSharedMaterial` is never written, so the whole interface does **not** get the outline.
- **Fail-safe**: everything in `try/catch`; if the shader is not distance field (`_OutlineWidth` missing), the mod **does not change** that material and logs the reason. Harmony patches are **per method type** with `__instance` — no positional `ref __N` parameter — and they are applied **one by one** (`CreateClassProcessor(...).Patch()` per hook class, with one log line per hook and a summary with the **real count**): a hook that fails does not take down the others, and the log says which one it was.
- **Diagnostics in the log**: per surface, the mod records the object, the component, the TMP font, the shared source material, the shader and whether it is SDF; plus a scene inventory (`N TMP_Text`, `M` legacy `TextMesh`) and the font materials in use with a count. It has its own key in the `.cfg` (`1. Geral` > `DiagnosticoNoArranque`, default `true`; `false` = no scene scan) and the scan **stops by itself at the first target that appears in the scene**.
- **Startup diagnostics executed in the game**: what is confirmed is **technical feasibility**, read from the diagnostic itself — all TMP targets use `TextMeshPro/Distance Field` variants (`Overlay`, `(Surface)`, `Distance Field`) with `_OutlineWidth` present (soft halo feasible); the dice number is `TextMeshPro` (140 faces across 7 `DiceVisualSetup`, 0 legacy `TextMesh`); and the stack labels are legacy `UnityEngine.UI.Text` (124 `StatusIcon`).
- **Visual effect: NOT CONFIRMED** — it depends on the owner seeing it in game (opening a combat/event and looking). The diagnostic proves the halo is possible, not that it appears or that it looks good; there is no before/after log nor a screenshot in the repository.
- **With the mod OFF (`Ativar = false`) the game runs original**: it is an early-return in `Awake` — no hook is applied (the log shows only the "OFF in config" line) and no target is touched.
- **Coexistence with BetterFont**: with both on, the combat texts get **the serif and the effect** (halo/shadow) from **BetterFont 1.0.2** — a different shader variant is no longer a refusal there. On **1.0.1** they stayed with the **original font** (the BetterFont gate refused the material of the combat texts; that was the defect BF-2 fixed). BetterFont swaps the font and re-applies to the per-component material the effect that was already on that text; when that effect cannot be reproduced (face texture, bevel, glow), that text stays **untouched** — the safe choice, not a defect, and the reason comes out named in the BetterFont log. Cosmetic, nothing breaks.
- **Turning everything off in 1 line**: `Ativar = false` in section `1. Geral` — no patch is applied and the game runs original.
- **No gameplay change** and no touching of any game file. No Bard/music.

### Historical dependency decision (0.1.0 package)

> This block describes the old manifest. The **published** 0.1.2 package declares `DefRuivo_StolenRealmMods-BetterFont-1.0.3` (section at the top). The repository manifest, **not yet published**, stopped declaring BetterFont as a mandatory dependency: the code does not reference it and the integration is optional (DEP-REV dependency audit, 2026-10-16). The install README still says the opposite and needs to be aligned when preparing the new version.

- `dependencies`: `BepInEx-BepInExPack-5.4.2305` + **`DefRuivo_StolenRealmMods-BetterFont-1.0.1`** — this is where the styling of the combat texts comes back; the reference points at the **new** version so the manager does not install the same package in two versions (same GUID = error in BepInEx).
- **The dependency is ONE-WAY — `BetterCombatText 0.1.0` → `BetterFont 1.0.1` — and only that.** `BetterFont` 1.0.1 declares **only** the BepInExPack; the mod pointing at the other end is this one. The mutual dependency (the two declaring each other) was swapped for this single direction in commit `ac0210f`.
- **Why the mutual dependency cannot be published (proven in the Thunderstore code):** on upload the platform **resolves** each reference (`DependencyField` uses `PackageReferenceValidator(resolve=True)`) and **refuses** the reference that does not exist, with `No matching package found for reference`. With both sides referencing each other, each side pointed at an **unreleased** version (the `BetterFont 1.0.1` and this `0.1.0`, neither of them live) — there was no valid send order: whoever went up first failed. It is not a style preference, it is the upload refusing.
- **Send order that works:** first `BetterFont 1.0.1` (with no dependency back), then this `0.1.0` declaring `BetterFont 1.0.1` — the same order recorded in [`release/mods.json`](../release/mods.json).
- **Historical hypothesis, not a future release:** on 2026-09-30 a BetterFont 1.0.2 with a dependency back was considered. That was **not** adopted: 1.0.2 and 1.0.3 exist and the current BetterFont manifest still declares only BepInEx. There is no future version promised by this note.
