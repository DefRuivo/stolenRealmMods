# RoguelikeSkillTreeVisualizer

Adds a **`Skills`** button that opens the game's **native skill tree**, read-only, on the
character you chose. **No skill point is spent. No gameplay change.**

- **GUID:** `com.gumatos.roguelikeskilltreevisualizer`
- **Version:** 0.3.1
- **Works with:** Stolen Realm v1.3.1 (Roguelike mode only).
- **Needs:** BepInEx 5 (r2modman installs it for you).
- **Status:** implemented; **not yet checked in game** by the author.

## What the button does

- On the **Select Party** screen it appears as a square **`Skills`** button next to
  **`Choose Powerups`**. The row does not grow: `Choose Powerups` shrinks just enough.
- In a **run** the same button appears next to the HUD's **Ping Button**. It only shows
  when opening is safe (see *When the button hides*).
- Opens the tree of **the right character**: on the party screen, the last one **you**
  added; in a run, the character selected at that moment — level and gear are read at
  click time, never cached.
- Inside the tree you can **navigate, zoom, change tab and read tooltips** with your
  character's real numbers. Learned skills are lit; the rest are grey.

## What it does not do

- **Does not spend skill points** — the footer shows `0 points available`.
- **Does not learn or remove skills** — clicking a node is blocked and `Respec Build` is
  hidden.
- **Does not touch** `Accept Party`, the Current Party, the Powerups or the Roguelike
  rules. No game file is modified.
- **Does not mix players** — each player sees only their own characters.

The mod does not rebuild the skill tree: it picks the right character and hands it to the
game's own system.

## When the button hides

In a run the button disappears (and refuses to open) while any of these is true — when in
doubt, it does not open:

- you are **aiming** a skill, or in ping mode;
- it is not your turn, or someone is acting/moving;
- a level-up or reroll is pending;
- another window is already open (inventory, options…);
- the game is not in battle, world map or town.

## Configuration

File: `BepInEx/config/com.gumatos.roguelikeskilltreevisualizer.cfg`.

| Section | Key | Default | What it does |
|---|---|---|---|
| `Geral` | `AtivarBotao` | `true` | `false` = no button on the party screen. |
| `Geral` | `AtivarBotaoNaRun` | `true` | `false` = no button in the run HUD. |
| `Geral` | `AjustarZOrder` | `true` | Keeps the tree above the HUD in a run. Turn it off if the game tooltip appears behind the tree. |

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
works in **Roguelike mode**; you do not need to enter a match to see the party button.

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
come from the game and are **never distributed**. The flag keeps the build local: **without it
the `DeployToBepInEx` target also copies the DLL into
`<r2modman profile>\BepInEx\plugins\RoguelikeSkillTreeVisualizer\` on the machine that built
it** — a bare `dotnet build` installs.

---

## Português (BR)

Adiciona um botão **`Skills`** que abre a árvore de skills **nativa do jogo** em modo
**somente leitura**, no personagem escolhido: na tela *Select Party*, ao lado do
`Choose Powerups`; na run, ao lado do Ping Button do HUD (e só quando é seguro abrir).
**Nenhum ponto é gasto** e nada que persista muda. O mod ainda **não foi conferido em
jogo** pelo autor.
