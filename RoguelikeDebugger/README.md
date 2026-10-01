> **Development tool — NOT a player mod.** It does not improve the game on screen. It
> exists to investigate Stolen Realm's internal mechanics while the other mods are built.

# RoguelikeDebugger

Writes the game's internal data to `LogOutput.log`, so a mechanic can be checked in the
code instead of guessed. **No gameplay change.**

- **GUID:** `com.gumatos.roguelikedebugger`
- **Version:** 0.1.1
- **Works with:** Stolen Realm v1.3.1.
- **Needs:** BepInEx 5 (r2modman installs it for you).

## What it does

**Logs only. No gameplay change.** It writes to `LogOutput.log`:

- **Skills** — the game's skill inventory (name, description, actions granted, attribute
  effects, triggers) and the action properties (range, targets, number of hits, cooldown,
  charges, status applied).
- **Status** — the buff/debuff inventory, with their attribute effects and description.
- **Items** — type, rarity, optional description, attributes, armour ratio and consumable
  action — plus the affixes.
- **Powerups** — one line per level.
- **Loot, gold and experience** — the roll decisions, the modifiers applied and the
  values granted.

The dump is **huge**: it writes thousands of lines per game start and makes the log hard
to read for anyone who just wants to play.

## What it does not do

- **No gameplay or save change** — the only output is text in `LogOutput.log`.
- **Does not improve the game on screen** — it is an investigation tool, not a player mod.
- **Sends no data anywhere** — everything stays in the local log, on your machine.

## Install

This package only makes sense for someone who is going to **develop or investigate**.

**r2modman (recommended):** install this package in the Stolen Realm profile — the DLL
goes to `BepInEx\plugins\RoguelikeDebugger\`.

**Manual:** install BepInEx 5 x64 (or press "Start modded" once in r2modman to create
the folders), then copy the `RoguelikeDebugger` folder to:

```text
%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\
```

The file must end up as `...\plugins\RoguelikeDebugger\RoguelikeDebugger.dll`. Open the
game once (the dump comes out on start; no need to enter a match) and read the log — it
is **overwritten on every game start**.

## Uninstall

Delete the folder `BepInEx\plugins\RoguelikeDebugger\` (or untick the package in r2modman)
and open the game again. No game file was ever changed.

## Build from source

```powershell
cd RoguelikeDebugger
dotnet build
```

Output: `bin\Debug\netstandard2.1\RoguelikeDebugger.dll`. The reference DLLs come from the
game and are **never distributed**.

---

## Português (BR)

**Ferramenta de desenvolvimento, não é mod de jogador.** Em vez de melhorar a tela, ela
despeja os dados internos do jogo (skills, status, itens, loot, ouro, experiência) no
`LogOutput.log` para conferir mecânicas no código. **Não altera gameplay** e não envia
nada para fora: tudo fica no log local. O dump é enorme — enche o log de milhares de
linhas a cada boot.
