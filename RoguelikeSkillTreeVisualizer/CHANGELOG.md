# Changelog — RoguelikeSkillTreeVisualizer

`RSTV-nn` codes are the change identifiers used across this mod's notes; an `F` suffix marks a fix
that came out of a review.

## 0.3.3 — right numbers in the read-only window, the party screen loses its button, the run button moves home

**In one sentence:** the read-only tree now shows damage, expressions and the tooltip footer
(mana / cooldown / range / duration) with the numbers of **the character the window is showing**,
and the run button left the hex-marker button's row for the HUD's **bottom bar**, where it stays
visible as long as the HUD does.

- **RSTV-26 — the literal `*0` and `[N]` are gone.** Hovering a node in the window opened from the
  *Remove Skill Trees* modal showed every damage as `*0` and every expression as `[N]`, unresolved.
  Cause: that window lives on the party screen, where the game's own character context is **null** —
  and the game only resolves `*N`/`[N]` when it has a character. The mod now hands it **the
  character the modal is showing**; when there is no such target the window falls back to the old
  behaviour (nothing breaks).
- **RSTV-27 — the tooltip footer belongs to the character in view.** The same null character sent
  the footer (mana / cooldown / range / duration) to the wrong character. The footer now reads the
  **same** target as the window and **follows a change of the character in view**.
- **RSTV-29 — the `Skills` button on the Select Party screen was REMOVED** (the author's decision,
  in game, 06/10). That screen is served by the *Remove Skill Trees* modal button and by the
  shortcut. See RSTV-29 below.
- **RSTV-30 — the run button moved to the bottom bar and stopped blinking.** It left the row of the
  button that marks the hex and joined the row of the native inventory and skills buttons; as a
  child of that bar it appears and disappears **with the HUD** — the hide-and-reappear on every
  character action is gone. The run gate now decides only whether the **click** may open. See
  RSTV-30 below.
- **Version:** 0.3.2 -> **0.3.3** in the four places that carry it (the project file, the manifest,
  the plugin version behind `[BepInPlugin(...)]` and the README version line).

### RSTV-30 — the run button moved to the bottom bar and no longer blinks

**What the author asked for (06/10, in game):** the skills button was not always visible — when
anyone took an action it disappeared and came back, and it did not show outside combat; instead of
being rendered next to the button that marks the hex, it should be rendered on the **bottom bar, on
the left, next to the inventory and skills buttons and before the control that rotates the skill
bar**.

- **New home.** The button is now a child of the game's own container of the inventory and skills
  buttons, in the free gap measured before the control that rotates the skill bar. The position is
  **measured at runtime** and the clone is excluded from the container's layout group, so **no
  native button moves, shrinks or is covered**.
- **Reference-frame fix (RSTV-30F, found in review).** The placement arithmetic mixed two reference
  frames, so the measured gap came out about 75 px instead of about 19 px and the button landed
  **after** the control it was supposed to sit before — the opposite of the request. Both edges are
  now measured in the same frame and the arithmetic is pinned by a test.
- **Looks.** The clone uses the **native button of that same row** (the skills button): same
  background, sprite, states and the game's own skill-tree icon. The unspent-points badge is
  switched off.
- **Visibility = the HUD.** The button is no longer hidden by game state. As a child of the bottom
  bar it comes and goes **with the HUD**; the game itself turns the whole HUD off in menus, event
  windows, level-up, the shop and character choice/creation. That hide-and-reappear was what the
  author saw whenever any character acted.
- **The gate decides only the CLICK.** The run gate refuses only where opening would cause **real
  harm** (hex or skill aiming, an open UI window, the battle's initial placement) and the click is
  also crossed with the game's own rule for the HUD's skills button. When it refuses, the button
  **stays on screen** and the reason goes to the log.
- **Guards removed**, each with the defect it caused: the game-state allow-list, the "it is the
  player's turn and the game is ready" check and the "someone is acting / moving in battle" checks —
  these were what hid the button during another character's action and outside combat. The guards
  that stayed carry, in the code, a numbered marker and a justification line naming the real harm
  they prevent.

### RSTV-29 — the `Skills` button on the Select Party screen was removed

**The author's decision (06/10, in game):** remove the button from the party-select screen and keep
only the one that opens with the *Skill Tree removal* window. That screen's surface is gone
entirely; the *Remove Skill Trees* modal button and the shortcut cover it.

- **What is not in the build any more:** the button on the party screen, its hooks into the game's
  party-screen manager, its mirror in the mod's own per-frame updater and its boot log line (a log
  line announcing a feature that no longer exists).
- **Config `AtivarBotao`:** it is now the **master switch of the buttons that remain** (the run HUD,
  the level-up window and the modal). The per-surface keys `AtivarBotaoNaRun` and
  `AtivarBotaoNaRemocao` still work on their own.
- **What did not change:** the *Remove Skill Trees* modal button, the run HUD button and the
  keyboard shortcut, which still opens the read-only tree, including from the party screen.

#### RSTV-29F — findings of the independent review

- **The master switch was kept, with its reach made explicit.** `AtivarBotao=false` turns off the
  three remaining buttons at once; a single surface is switched off with its own key. The reach is
  written in the config description and in the README, which previously omitted the level-up window
  button. Note: an old config file with `false` therefore also loses the run HUD and the modal
  buttons (the author's own profile uses `true`).
- **The log no longer names the wrong key.** With the master switch off and a per-surface key on,
  the messages name the key that **actually** switched it off.
- **The absence is now pinned by the property, not by a name.** The test that guarantees the
  party-screen button stays gone no longer settles for the class name and one spelling: it looks for
  any hook in the source that points at the game's party-screen methods, in any form of writing, and
  the escape route that the reviewer measured now fails.

## 0.3.2 — its own read-only window on the modal's `Skills` button, plus a UI/UX revision

The `Skills` button of the *Remove Skill Trees* modal was **dead** on the party-select screen: the
click called the inventory path, which does not open there, and the request died at the five-second
ceiling without showing anything.

The click now opens a **read-only window of the mod's own** showing **all** skill trees — the same
classes and the same tree as the game's own "All Trees" tab — without depending on the inventory.
The character the modal is showing is passed in as the target, the read-only session keeps blocking
every write, and the window follows the modal's lifecycle (closing the modal closes the window; its
root survives scene loads and is reused between openings).

- **Readable tooltip.** The window is its own canvas above everything, but the skill tooltip lives
  on the game's **root** UI canvas: raising the tooltip canvas either hid the whole window (when it
  grabbed the root canvas) or did nothing (there was no nested canvas to raise). The final solution
  **re-parents** the game's tooltip **inside** the window while it is open and hands it back to the
  game when it closes — hovering a node shows the complete tooltip, above the dark background.
- **Native look.** Background, frame, title and close button clone the modal's own prefabs instead
  of a flat colour and a menu-style row; and the class bar — when the game's own tree manager is not
  loaded, which happens in a scene without that tab — builds each class button from the class
  **icon** asset plus its name, in the native 64×64 layout. Positioning pass (04/10): a fixed 13 px
  font with auto-sizing off (it was overflowing and wrapping names such as "Lightning" onto a second
  line over the icon), ending with the icon above and the name as a one-line caption below it.
- **Window design revision (04/10, measured pixel by pixel).**
  - **Prerequisite lines now appear.** They used to be positioned at the midpoint, kept a zero
    rotation (so they stood vertically beside the nodes) and stopped short of the target. They are
    now built inside the **node container**, rotated to the actual segment angle and sized to the
    exact world distance, so requirements read correctly again.
  - **The tree is centred in the available area** (not in the window): the container is placed by
    the bounding box of the nodes, with a top clamp (no node invades the class bar) and a scale
    clamp (wide classes shrink to fit the frame).
  - **Class bar:** icon and caption spacing retuned, caption in a 15 px font with wrapping off, and
    the selection highlight lowered from alpha 0.22 to 0.12 for a comfortable contrast against the
    label.
  - **Header:** 64u tall, a 56u Close button inset 22u from the edge, a 2 px divider under the title
    and a 48u base margin, symmetric with the top.
  - **Tooltip and hover:** the tooltip gained a black outline (it no longer disappears on the dark
    background) and the node under the mouse a **gold outline** on its icon.
  - **Class subtitle:** the title reads `All Skill Trees — <class>` and follows the selected class.

## 0.3.1 — `Skills` button on the *Remove Skill Trees* modal

New **Skills** button in the top-right corner of the *Remove Skill Trees* modal (party-select
screen), opening the read-only skill-tree viewer for the character that modal is showing.

## 0.3.0 — "All Skill Trees" tab, button and shortcut, native scale and position

- **RSTV-13 — the HUD's `Skills` button appears again while walking the world map.** The run gate
  applied battle-only gates (skill aiming, initial placement, the turn, someone acting or moving) in
  **every** game state, so on the map they hid the button exactly while the player was walking
  through it. The battle gates now live inside the battle branch; on the map and in town only the
  universal ones apply (hex-marking mode, an open UI window, no target). Safety **in battle** is
  unchanged — each gate still blocks there.
- **RSTV-14 — the button inside the level-up window follows the window's lifecycle.** It was created
  once and never re-evaluated, so it stayed visible — stuck to the old corner of the panel — when
  the game switched the level-up to its attributes stage without closing the window. It is now
  refreshed every frame and shown only in the skills stage of the window that is actually open,
  re-anchored when that stage comes back; it is never injected while the window is closed.
- **Tests for RSTV-13/14** cover the gate across game states and the level-up lifecycle, and each
  defect they describe was planted in the real sources, caught with the right reason, and the
  sources restored byte-for-byte.

## 0.2.0

**RSTV-5 — the `Skills` button now exists DURING A RUN**, anchored in the HUD next to the button
that marks the hex, on the same row. The window is the **same native skill tree**, in the same
read-only mode.

- **Button in the run HUD:** a clone of the native hex-marker button, injected once when the game
  builds the HUD and mirrored by the mod's own updater — **never** in the HUD's own per-frame
  update, which touches the end-turn button.
- **Target resolved on click:** the character **selected at that moment**; with nobody selected, the
  **first local character of the party** (documented fallback). Level and gear are read at click
  time, never cached.
- **Safety gate (always on, even with the button enabled):** the button **hid itself and refused to
  open**, with the reason in the log, during skill aiming, hex-marking mode, another character's
  turn, someone acting or moving, the initial placement, a pending level-up, an open UI window, or a
  game state outside battle / world map / town. In doubt — including on an exception while reading
  the state — it did not open.

### Safety work in 0.2.0 (each with the engine line cited in the code)

1. **Lifecycle** — the guard became "the native instance is still active" plus a game-state
   allow-list for the run context, instead of "the party screen is open" (during a run that screen
   is off and the tree would close on the next frame).
2. **Writing the game's selected character** — only written when harmless: when the target already
   **is** the selected one, or when nobody is selected. The previous value is saved and restored on
   close. With **another** character selected the opening is **refused** — otherwise the game would
   mark a party leader, lock the camera, force the map out of aiming and announce the turn to
   another character.
3. **Single cancel-interceptor slot** — the mod photographs whoever held the slot before opening
   and gives that delegate back on close, so `Esc` stops being swallowed when the top window is not
   ours; the inventory on top still closes with `Esc`.
4. **Button gate** — see above.
5. **Hex click** — the window registers itself as open UI (which makes the game's input update
   return early, before the click reaches the map) **and** a hook consumes the click while the
   session is active. A safety net removes the registration if the window closes from outside, so
   battle input never stays dead.
6. **Character or state change** — if the game swaps the selected character or leaves battle /
   world map / town, the session is **closed** (no read-only window with the wrong context).

### Config

- `AtivarBotaoNaRun` (default `true`): switches **only** the run button. The gate above applies even
  when it is `true`.
- `AjustarZOrder` (default `true`): adjusts the sibling order so the tree stays above the HUD in a
  run. Turn it off if the game's tooltip appears behind the tree.

### Other changes in 0.2.0

- **Hooks:** 8 -> **10**; the boot count became `10/10 hooks, 10 game methods`.
- **Diagnostics:** the run button says **why** it is hidden (throttled to one line per reason every
  5 s) and announces when it is back; opening logs the row geometry, the clone's target graphic and
  how many inherited graphics were switched off.

### RSTV-12 — the button clicks reach the mod, not the prefab's own click

The log showed two symptoms: the HUD button **pinged** instead of opening the tree, and the level-up
one fired the game's confirmation path and threw (11 null references, one per frame). Root cause
read from the engine: a Unity click event keeps **two** listener lists — the ones serialized into
the prefab and the ones added by script — and the usual "remove all listeners" call empties **only**
the script list. Worse, the serialized list runs **first**, so if it throws, the mod's own listener
never runs at all.

- **Fix:** the mod replaces the whole click **event instance** on the clone, discarding the
  serialized list together with it, and installs its listener on the clean event. Applied to all
  three clones (run HUD, level-up window and the party screen, which still existed then).
- **Not** an overlap/raycast problem (the log showed the mod's own handler being called on the HUD
  clone) and **not** a component rebind (the game's button controller only changes colours).

### RSTV-11b — the `Skills` button exists inside the level-up window

- The HUD clone's earlier re-parenting approach was **retired**: the HUD button no longer changes
  home. Instead, when the game opens the level-up window, the mod clones the window's accept button
  as a **direct** child of the full-screen window — **outside** the scrolling content panel, which
  has a layout group and a size fitter, so a child inside it would reflow the whole panel. The
  button is born in the top-right corner of the visible panel, with the prefab's serialized click
  cleared (it called the game's own confirmation, a write) and pointing at the mod's shared open
  routine.
- The injection is **idempotent per window**: the hook runs again for each queued level-up
  character, over the same window, and does not create a second button.
- **RSTV-11b also unified the open routine.** `OpenForTarget()` was extracted and is now shared by
  the HUD button, the level-up button and the F10 shortcut, which used to duplicate the same body.
  The re-parenting machinery was removed from the run button.

### History: RSTV-8 and RSTV-9

- **RSTV-8 — the run button stops being hidden during level-up.** The gate hid the button whenever
  the game's roguelike manager was active, but "active" means "the manager was **loaded**" — its
  object stays active for the whole run after the first level-up. The real window is the level-up
  window's own active state, the same criterion the game uses. The button is now **released** during
  level-up, and the target comes from the level-up manager itself (with a documented fallback),
  never from the character the game currently has selected.
- **RSTV-9 — rendering the button during level-up (superseded by RSTV-11b).** The finding was that
  during level-up the game switches the **whole HUD off**, and the HUD clone is a child of it — so
  letting the gate through was necessary, but the button still did not render. The interim solution
  re-parented the clone into the level-up window, at the top-right corner and drawn last so it takes
  clicks, and gave it back to the hex-marker row when the window closed, restoring the original
  geometry. **RSTV-11b retired that re-parenting** in favour of a button of its own inside the
  window; the entry stays here as history. The normal case — the party screen, and the run on the
  world map and in battle — was never touched by it.

## 0.1.0

First version.

- **`Skills` button on the Roguelike party-select screen:** square, on the same row as *Choose
  Powerups* and glued to its right. A clone of the **native** button (same sprite and states); the
  *Choose Powerups* width shrinks only as much as needed, the row **does not grow** and *Accept
  Party* does not change size.
- **Opens the game's NATIVE skill tree** (the same one as *Campaign -> Change Skills*) with the
  character's **real** context: level, gear, attributes and the state of the skills. The game's own
  window is reused — the mod does **not** reimplement the tree.
- **Really read-only:** tooltips (with the right character's numbers), zoom, tab switching and
  requirements keep working; **nothing is learned, removed or spent**. Clicking a node is blocked,
  *Respec Build* is hidden and the footer shows `0 points available`.
- **Button target:** the **last character you added** to the party, resolved **on click**, so level
  and gear are always current and never cached. Each player uses their own; an empty local party
  disables the button.
- **Config:** `Geral -> AtivarBotao` in
  `BepInEx/config/com.gumatos.roguelikeskilltreevisualizer.cfg` (default `true`). It only ever
  **switches the button off** — whoever does not open the file sees no difference.
- **Diagnostics:** every hook is applied and logged **individually** (one failing hook does not take
  the others down, where before it was all-or-nothing); the boot summary carries the **real count**;
  and if the button is not injected, the log says **why** (native button missing, no rectangle
  transform, an exception, the config switched off) with the state of the screen.

### Static-audit fixes (against the game's decompiled code, without running the game)

- **Second write point closed:** the game's own "reset skill points" entry point calls a full skill
  reset — which zeroes the character's skills and queues a save — **without** passing through the
  sanitised write path. It got its own hook and is blocked in read-only mode.
- **Orphan tree:** if the party screen closed from outside with the tree open, nothing in the game
  closed the tree manager — the tree would stay over the map with `Esc` still intercepted. The
  mod's updater now closes the tree when the party screen is no longer open.
- Deliberately unchanged (it needs an in-game test, tracked in the README's *known risks*): the
  internal skill-dependency check with no caller in the assembly, the reset and close buttons that
  are wired only in the prefab, and the single cancel-interceptor slot.

### Implementation notes

- The game has **no** native read-only mode: the guarantee comes from **sanitising the write point
  before it runs**, not from blocking it. If that sanitisation fails, the mod does not let the
  original run and closes the window itself — zero writes in any state.
- No game file is modified; uninstalling is deleting the mod folder.
- Declared compatibility: Stolen Realm **v1.3.1**.
- Icon: the author's art resized to 256×256. The 1254×1254 original is **not** versioned in the
  repository.
