# BetterTooltips

Rewrites the game's skill and status tooltips so they stop **leaving out what matters**,
and fixes small text defects. **No gameplay change.**

- **GUID:** `com.gumatos.bettertooltips`
- **Version:** 0.1.1
- **Works with:** Stolen Realm v1.3.1.
- **Needs:** BepInEx 5 (r2modman installs it for you).

## What it does

The game's tooltips sometimes leave out the half that decides the fight: which attribute
feeds the number, the stack limit, the duration, who is affected, the trigger, the number
of hits. The text is not wrong — it is **incomplete**.

The mod completes it:

- Every game text passes through one place before it is shown; the mod compares that text
  with a table of fixes and mechanic notes.
- The missing explanation is **added at the end of the tooltip**, in the game's own
  special text colour, so it stands apart from the official text.
- Plain mistakes (spelling, punctuation, double spaces) are fixed directly.

Every note is based on the **game's own code**, not on opinion — and where the game cannot
be observed at that moment, the note says what is assumed.

## Shrine auras

The game's shrine tooltips always showed the **base** value, even for a character with
the bonus that multiplies the aura. The mod does the maths with the **real bonus of the
character in focus** — the *Shrine Effect Bonus* (**Omnism I/II**, the **Worship** perk
and the **Horn of Devotion**). A base `20%` becomes the number you actually receive.

It also adds a line listing **every shrine aura the character is receiving right now**,
with two numbers per aura: what the auras give you, and your total in that attribute
(the same number shown on the character sheet).

> **The number is raw**, before any damage reduction: armour, resistance and later
> mitigation are not counted. When there is no proof (character outside the aura, an
> attribute missing from the build), the original text is left **untouched** and the log
> says why — the mod does not guess.

## Verification

The numbers were written against the game's code and data, and the Worship doubling was
**measured in game**. The final visual check of the new lines on screen had **not** been
done at the last revision — if a line does not match what you see, that is where to
report it.

## What it does not do

- **No gameplay change** — no value, damage, cost or rule changes; it only rewrites text.
- **No game file is modified** (nor the save) and nothing is left behind.
- **Does not reveal the Chaos draw** — that is on purpose: the tree's fun is not knowing.
- **Does not show a number without proof** — it keeps the original text instead.
- **Does not apply mitigation** — the number is the raw formula result.

## Install

**r2modman (recommended):** install this package in the Stolen Realm profile — the DLL
goes to `BepInEx\plugins\BetterTooltips\`.

**Manual:** install BepInEx 5 x64 (or press "Start modded" once in r2modman to create
the folders), then copy the `BetterTooltips` folder to:

```text
%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\
```

The file must end up as `...\plugins\BetterTooltips\BetterTooltips.dll`.

## Uninstall

Delete the folder `BepInEx\plugins\BetterTooltips\` (or untick the package in r2modman)
and open the game again. No game file was ever changed.

## Build from source

```powershell
cd BetterTooltips
dotnet build -p:DeployToBepInEx=false
```

Output: `bin\Debug\netstandard2.1\BetterTooltips.dll`. The reference DLLs come from the
game and are **never distributed**. The flag keeps the build local: **without it the
`DeployToBepInEx` target also copies the DLL into
`<r2modman profile>\BepInEx\plugins\BetterTooltips\` on the machine that built it** — a bare
`dotnet build` installs.

---

## Português (BR)

Reescreve os tooltips de skills e status para pararem de **omitir o que decide**: qual
atributo alimenta o número, limite de stacks, duração, quem é afetado, o gatilho, o número
de golpes. Acrescenta a explicação que falta no fim do tooltip, na cor especial do jogo,
e corrige erros simples de texto. As auras de shrine passam a mostrar o número com o
**seu** bônus real. **Não altera gameplay.**
