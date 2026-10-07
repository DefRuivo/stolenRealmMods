# BetterCombatText

Makes combat text easier to read: an **outline** around the letters on enemy names and
buff/debuff labels, plus the **dice text** in roll events. **No gameplay change.**

- **GUID:** `com.gumatos.bettercombattext`
- **Version:** 0.1.2
- **Works with:** Stolen Realm v1.3.1.
- **Needs:** BepInEx 5 and **BetterFont**.

## What it does

Each surface is switched on/off **independently** in the `.cfg`. The effect always uses a
**per-text copy of the material** — never the shared one — so the rest of the interface
does not get an outline.

| Surface | What it gets (defaults) |
|---|---|
| Enemy names in combat | hard, opaque black outline (`LarguraContorno` 0.22, `SuavidadeContorno` 0.05, `AlfaContorno` 0.95) + short shadow |
| Buff/debuff labels in combat | hard black outline at 10% + shadow + bold (see *What it does not do*) |
| Dice text in roll events | soft outline/halo at 35% + shadow |
| Health number (extra, **off** by default) | soft outline/halo |

The **shadow color follows the background**, because a shadow only shows when it contrasts
with what is behind it: on a dark background (the battlefield) it is the light `#CBB396`;
on a light background it is `#000000`. That is the `Fundo` key per surface — the enemy
names ship with `Fundo = escuro`, and the BCT-2 rule (shadow by the **letter's** brightness)
is kept when a surface leaves `Fundo = auto`. Without this, a bright enemy name on the dark
battlefield got a black shadow — invisible.

## What it does not do

- **The visual effect is not confirmed.** A startup diagnostic proved the effect is
  *possible* on those texts (their material supports a soft outline), but nobody has
  looked at the screen with the mod on. It needs an eye in game — there is no
  before/after screenshot in the repository.
- **Buff/debuff labels do not get a soft halo.** The `xN` labels and the turn counter are
  the old Unity text (`UnityEngine.UI.Text`), not TextMeshPro: a soft outline does not
  exist there. On those the mod applies what exists — a hard outline, a shadow and bold.
  A soft halo there would mean replacing the components in the game's prefab, a big and
  risky change.

## Together with BetterFont

BetterFont swaps the interface font for a serif one and re-applies the effect on the new
per-text material. The combat texts run on a **different shader variant** than the serif
font uses; since **BetterFont 1.0.2** that is not a refusal any more (the style properties
exist in both), so with both mods on those texts get **both**: the serif face and the
halo/shadow applied here. The dependency of this package points at that version.

Only an effect the copy cannot reproduce — a real face texture, bevel, glow — leaves a
text **untouched**, the safe choice, with the reason named in BetterFont's log. To force
all styled texts to stay exactly as they were, set `PularTextosEstilizados = true` in
BetterFont's `.cfg` (its 1.0.1 behaviour).

## How to configure

File: `BepInEx\config\com.gumatos.bettercombattext.cfg` (edit in Notepad).

- **Turn everything off in one line:** section `1. Geral`, `Ativar = false`. The mod then
  applies nothing — the game runs fully original.
- **Stronger/lighter outline:** `LarguraContorno` (thickness) and `AlfaContorno`
  (opacity). The default is **per surface** — `0.10` on the buff/debuff labels, `0.35` on
  the dice text, `0.95` on the enemy names.
- **Softer or harder halo:** `SuavidadeContorno` — high = soft, `0` = hard.
- **Soft shadow:** `Sombra` + `SombraOffsetX` / `SombraOffsetY` / `SombraSuavidade` /
  `AlfaSombra`.
- **Shadow colour (`Fundo`):** the background behind the text — `escuro` (dark: shadow is the
  light `#CBB396`), `claro` (light: shadow is `#000000`) or `auto` (follow the letter's
  brightness). Enemy names default to `escuro`.
- **Font size:** `TamanhoFonteExtra` — `0` = leave the size alone (default).
- **Dice only:** section `4. Eventos (texto do dado)` > `Ativar = false`.
- Added on start: `1. Geral` > `DiagnosticoNoArranque` (default `true`) checks the scene
  every 5s (from 20s in, giving up at 240s) and logs the font/material/shader of the
  targets as soon as one appears in the scene — read-only, nothing is changed. Since BCT-3 it
  also logs the **letter colour** of each target (`#RRGGBB`, alpha, luminance) and the shadow
  colour that ended up in the material.
- Changed the `.cfg`? **Restart the game** — the values are read on start.

## Install

**r2modman (recommended):** install this package in the Stolen Realm profile — the DLL
goes to `BepInEx\plugins\BetterCombatText\`.

**Manual:** install BepInEx 5 x64 (or press "Start modded" once in r2modman to create
the folders), then copy the `BetterCombatText` folder to:

```text
%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\
```

The file must end up as `...\plugins\BetterCombatText\BetterCombatText.dll`.

## Uninstall

Delete the folder `BepInEx\plugins\BetterCombatText\` (or untick the package in r2modman)
and open the game. The text is back to the original on the next start — no game file was
ever changed. (Without uninstalling: `Ativar = false` in the `.cfg`.)

## Build from source

```powershell
cd BetterCombatText
dotnet build -p:DeployToBepInEx=false
```

Output: `bin\Debug\netstandard2.1\BetterCombatText.dll`. The reference DLLs come from the
game and are **never distributed**. The deploy is **opt-in** (DEPLOY-2): a bare
`dotnet build` installs **nothing** — the `DeployToBepInEx` target runs only with
`-p:DeployToBepInEx=true`, which copies the DLL into
`<r2modman profile>\BepInEx\plugins\BetterCombatText\` on the machine that built it.

---

## Português (BR)

Deixa o **texto de combate** mais legível: **nomes de inimigos** com contorno duro e sombra automática, **rótulos de buff/debuff** com contorno/halo a 10%, mais o **texto do dado** nos eventos
de rolagem. Cada superfície liga/desliga no `.cfg`. **Não altera gameplay.**

A **cor da sombra segue o FUNDO** (chave `Fundo` por superfície), porque a sombra só aparece
quando contrasta com o que está atrás dela: no fundo escuro do campo de batalha ela é a clara
`#CBB396` — o preto `#000000` sumia ali (era o defeito relatado: "não vejo sombra nos nomes").
Os nomes de inimigo já saem com `Fundo = escuro`; quem deixa `auto` mantém a regra antiga
(pela luminância da letra). O diagnóstico de arranque agora imprime a **cor da letra** de cada
alvo e a cor de sombra que ficou no material.

Dois pontos honestos: o **efeito visual ainda não foi confirmado** (ninguém olhou a tela
com o mod ligado), e os **rótulos de buff/debuff não ganham halo suave** (são o texto
legado do Unity; ali entra contorno duro + sombra + negrito). Com o **BetterFont 1.0.2**
(ou mais novo) instalado, os textos de combate ficam com **a serifa e o halo** — variante
de shader diferente deixou de ser recusa no BetterFont nessa versão. Na **1.0.1** eles
mantinham a **fonte original**, porque o portão do BetterFont recusava o material dos
textos de combate.
