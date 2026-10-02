# BetterStats

Shows your attributes as **`base (combined)`** on the character sheet and on the
level-up screen: the raw value you invested and the final value with powerups, gear and
skills. **No gameplay change.**

- **GUID:** `com.gumatos.betterstats`
- **Version:** 1.0.1
- **Works with:** Stolen Realm v1.3.1.
- **Needs:** BepInEx 5 (r2modman installs it for you).

## What it does

The game shows one final number per attribute (Might, Dexterity, Vitality, Intelligence,
Reflex). That hides how much came from **points invested** and how much came from
**powerups, gear and skills** — the part you need when deciding where to invest.

The mod shows both:

```text
Might        12 (18)
             ^^   ^^
             |    +-- final value (powerups, gear and skills applied)
             +-- raw value (points invested)
```

- Works on the **Attributes** panel of the character/inventory screen and on the
  roguelike **level-up** screen.
- Also fixes the layout of that value column, which used to overflow the panel.

## What it does not do

- **No gameplay change** — no attribute, damage or cost changes; it only formats text.
- **No game file is modified** (nor the save) and nothing is left behind.
- **No number is invented** — the raw value comes from the character, the combined value
  from the game's final attributes.
- **No other screens are changed.**

## Install

**r2modman (recommended):** install this package in the Stolen Realm profile — the DLL
goes to `BepInEx\plugins\BetterStats\`.

**Manual:** install BepInEx 5 x64 (or press "Start modded" once in r2modman to create
the folders), then copy the `BetterStats` folder to:

```text
%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\
```

The file must end up as `...\plugins\BetterStats\BetterStats.dll`.

## Uninstall

Delete the folder `BepInEx\plugins\BetterStats\` (or untick the package in r2modman) and
open the game again. No game file was ever changed.

## Build from source

```powershell
cd BetterStats
dotnet build -p:DeployToBepInEx=false
```

Output: `bin\Debug\netstandard2.1\BetterStats.dll`. The reference DLLs come from the game
and are **never distributed**. The flag keeps the build local: **without it the
`DeployToBepInEx` target also copies the DLL into
`<r2modman profile>\BepInEx\plugins\BetterStats\` on the machine that built it** — a bare
`dotnet build` installs.

---

## Português (BR)

Mostra os atributos como **`base (combinado)`** na ficha de personagem e na tela de level
up: o valor puro investido e o valor final com powerups, equipamento e skills. Também
corrige o alinhamento da coluna de valores. **Não altera gameplay.** Instalação,
desinstalação e build estão nas seções em inglês acima.
