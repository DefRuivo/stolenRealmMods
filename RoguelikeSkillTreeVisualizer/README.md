# RoguelikeSkillTreeVisualizer

Adds a **`Skills`** button that opens the game's **native skill tree**, read-only, on the
character you chose. **No skill point is spent. No gameplay change.**

- **GUID:** `com.gumatos.roguelikeskilltreevisualizer`
- **Version:** 0.3.3
- **Works with:** Stolen Realm v1.3.1 (Roguelike mode only).
- **Needs:** BepInEx 5 (r2modman installs it for you).
- **Status:** implemented; the read-only window was **checked in game** by the author. The run
  button's new spot on the bottom bar (RSTV-30) still awaits an in-game pass.

## What the button does

- On the **Remove Skill Trees** modal (opened from the Roguelike party screen) a square
  **`Skills`** button sits in the top-right corner of the title; it opens the read-only
  tree of **the character that modal is showing**.
- In a **run** the same button sits in the HUD's **bottom bar**, in the same row as the native
  **inventory** (`Character Btn`) and **skills** (`Skills Tree Btn`) buttons, in the measured free
  gap before the control that **rotates the skill bar** (`Skillbar Index Controls`). It is **always
  on screen while the run HUD is** — the run gate decides only whether the click may open (see
  *When the button has no click*).
- In the **level-up window** a third `Skills` button sits in the top-right corner of the window
  while it is showing the skill choice (it is hidden on the items, attributes and currency
  stages), so the tree can be read without leaving the level-up.
- The **F10 shortcut** (configurable) opens the same read-only tree, including from the
  party screen — no button is needed there.
- Opens the tree of **the right character**: the modal's character, or the character
  selected at that moment in a run — level and gear are read at click time, never cached.
- Inside the tree you can **navigate, zoom, change tab and read tooltips** with your
  character's real numbers. Learned skills are lit; the rest are grey.

> **Removed in RSTV-29 (06/10):** there used to be a `Skills` button injected on the
> **Select Party** screen next to `Choose Powerups`. It is **gone**; the modal button above
> covers that screen, and the F10 shortcut still works there.

## What it does not do

- **Does not spend skill points** — the footer shows `0 points available`.
- **Does not learn or remove skills** — clicking a node is blocked and `Respec Build` is
  hidden.
- **Does not touch** `Accept Party`, the Current Party, the Powerups or the Roguelike
  rules. No game file is modified.
- **Does not mix players** — each player sees only their own characters.

The mod does not rebuild the skill tree: it picks the right character and hands it to the
game's own system.

## When the button has no click

In a run the button **stays on screen** with the HUD (it lives in the bottom bar): it is the HUD
that decides whether it is visible. What the run gate decides is whether the **click** may open —
while any of these is true the button is visible but **has no click**, and the log says why:

- you are **aiming** a skill, or in ping mode;
- another window is already open (inventory, options…);
- the battle is in its **initial placement**;
- the game's own rule disables the `Skills` button of the HUD (state outside town / world map /
  cutscene / battle, or the game is hiding the character buttons).

## Configuration

File: `BepInEx/config/com.gumatos.roguelikeskilltreevisualizer.cfg`.

| Section | Key | Default | What it does |
|---|---|---|---|
| `Geral` | `AtivarBotao` | `true` | **Master switch** for the `Skills` buttons: `false` = no button at all (run HUD, level-up window **and** modal). |
| `Geral` | `AtivarBotaoNaRun` | `true` | `false` = no button in the run HUD (the F10 shortcut still works). |
| `Geral` | `AtivarBotaoNaRemocao` | `true` | `false` = no button on the *Remove Skill Trees* modal. |
| `Geral` | `AtalhoSkillTree` | `true` | `false` = disables the keyboard shortcut. |
| `Geral` | `TeclaAtalhoSkillTree` | `F10` | The shortcut key (any Unity `KeyCode`). |

## Install

**r2modman (recommended):** install this package in the Stolen Realm profile — the DLL
goes to `BepInEx\plugins\RoguelikeSkillTreeVisualizer\`.

**Manual:** install BepInEx 5 x64 (or press "Start modded" once in r2modman to create
the folders), then copy the `RoguelikeSkillTreeVisualizer` folder to:

```text
%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\
```

The file must end up as
`...\plugins\RoguelikeSkillTreeVisualizer\RoguelikeSkillTreeVisualizer.dll`. The mod only
works in **Roguelike mode**; you do not need to enter a match to see the modal button.

## Uninstall

1. Close the game.
2. Delete the mod folder in `BepInEx/plugins/RoguelikeSkillTreeVisualizer/`. Nothing is
   created outside it.
3. Optional: delete `BepInEx/config/com.gumatos.roguelikeskilltreevisualizer.cfg`.

Uninstalling leaves nothing behind and does not affect your save.

## Build from source

```powershell
cd RoguelikeSkillTreeVisualizer
dotnet build -p:DeployToBepInEx=false
```

Output: `bin\Debug\netstandard2.1\RoguelikeSkillTreeVisualizer.dll`. The reference DLLs
come from the game and are **never distributed**. The deploy is **opt-in** (DEPLOY-2): a bare
`dotnet build` installs **nothing** — the `DeployToBepInEx` target runs only with
`-p:DeployToBepInEx=true`, which copies the DLL into
`<r2modman profile>\BepInEx\plugins\RoguelikeSkillTreeVisualizer\` on the machine that built it.

---

## Português (BR)

Adiciona um botão **`Skills`** que abre a árvore de skills **nativa do jogo** em modo
**somente leitura**, no personagem em foco: no cabeçalho do modal *Remove Skill Trees*, no canto da
**janela de level-up** (enquanto ela mostra a escolha de skill) e, na run, **na barra de baixo do
HUD** — na mesma linha dos botões nativos de inventário e de skills, no vão livre antes do controle
que **rotaciona a barra de skills** (RSTV-30). Na run ele **fica na tela enquanto o HUD aparece**; o
portão da run decide só o **clique**. O atalho **F10** abre a mesma árvore, inclusive na tela de
party. **Nenhum ponto é gasto** e nada que persista muda.

> **Removido na RSTV-29 (06/10):** existia também um botão `Skills` na tela *Select Party*,
> ao lado do `Choose Powerups`. Ele **não existe mais** — o botão do modal cobre aquela tela
> e o atalho F10 continua funcionando ali.
