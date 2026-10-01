# BetterFont

Replaces the game's interface font with a **serif** one (Times New Roman; Georgia or
Liberation Serif as fallback), keeping the colour, outline and shadow of the text.
**No gameplay change.**

- **GUID:** `com.gumatos.betterfont`
- **Version:** 1.0.2
- **Works with:** Stolen Realm v1.3.1.
- **Needs:** BepInEx 5 (r2modman installs it for you).

## What it does

- Swaps the font of **every text in the game**, including screens that open later
  (level up, tooltips, options) and the **combat texts** (enemy names, dice numbers).
- **Keeps the text style:** before swapping, it copies the face colour, outline and
  shadow from the material the text was using into a per-text copy of the new font's
  material.
- **A different shader variant is not a refusal.** The serif font is built on
  `TextMeshPro/Mobile/Distance Field` while the game's combat texts use
  `TextMeshPro/Distance Field Overlay` / `Distance Field (Surface)`; the style
  properties exist in both, so the copy is best-effort property by property and the log
  says what the new variant does not expose.
- Keeps the **original font as a fallback**, so icons and symbols that Times New Roman
  lacks still render (no empty boxes).
- Works with `timeScale = 0`, which is the case of the game menus.

## What it does not do

- **No gameplay change** — no value, damage, rule or balance is touched.
- **No game file is modified** and nothing is left behind when you remove the mod.
- **No text is translated or rewritten** — only the font face changes; the content stays
  the game's own.

## Together with other mods

Any mod that applies a material effect (outline/halo, shadow) to a text gets the same
treatment: BetterFont swaps the font and re-applies the effect on the new per-text
material. With **BetterCombatText** installed the combat texts get **both**: the serif
face and the halo/shadow it had applied. No mod needs to know the other, and there is no
required order between them.

Only when the material carries an effect the copy cannot reproduce is that text left
**untouched** — the safe choice — and the reason is written by name in the log
(`[diag] PULADO (...)`, with `Diagnostico/LogDiagnosticoEstilo = true`). There are **five**
reasons to refuse, and they are the five the code refuses on:

1. a real face texture (`_FaceTex`) — the copy never transports textures;
2. a real bevel texture (`_BumpMap`) — same reason;
3. the `GLOW_ON`/`BEVEL_ON` keywords — glow and bevel are not transported;
4. an outline or shadow **in use** that the new material does not expose
   (`_OutlineWidth`/`_UnderlaySoftness`) — the case of a bitmap font;
5. the serif font has no material yet.

On top of those, any exception raised while checking also refuses (the doubt falls on the safe
side). The check reads the **effect present in the material**, not the kind of text: a text
nobody classified is protected too.

## Configuration

File: `BepInEx\config\com.gumatos.betterfont.cfg`.

| Section | Key | Default | What it does |
|---|---|---|---|
| `Estilo` | `PreservarEstilo` | `true` | Copies colour/outline/shadow from the old material into the new per-text material. |
| `Estilo` | `PularTextosEstilizados` | `false` | `false`: also swap the font of texts that carry their own material (or a different shader variant), re-applying their effects. `true`: leave those texts fully untouched (old look, no serif). |
| `Diagnostico` | `LogDiagnosticoEstilo` | `false` | Logs, per text, what was copied, what could not be copied, what is deliberately left out and the shader variant before/after. With this on, the sweep also prints one line with the new font's material and which properties it exposes. |

The `.cfg` is read on game start: change it and reopen the game.

**A key that is missing from the `.cfg` is not a special case.** BepInEx creates the
entry with the default above (`false` for `PularTextosEstilizados`) and the new path
applies. There is one different case: if reading/creating the entry **fails** (a config
file the mod cannot parse), the safe getter takes over and `PularTextosEstilizados` is
treated as `true` — the conservative behaviour, with the error written in the log.

## Install

**r2modman (recommended):** install this package in the Stolen Realm profile — the DLL
goes to `BepInEx\plugins\BetterFont\`.

**Manual:** install BepInEx 5 x64 (or press "Start modded" once in r2modman to create
the folders), then copy the `BetterFont` folder to:

```text
%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\plugins\
```

The file must end up as `...\plugins\BetterFont\BetterFont.dll`.

## Uninstall

Delete the folder `BepInEx\plugins\BetterFont\` (or untick the package in r2modman) and
open the game again. The original font is back on the next start — no game file was ever
changed.

## Build from source

```powershell
cd BetterFont
dotnet build
```

Output: `bin\Debug\netstandard2.1\BetterFont.dll`. The reference DLLs come from the game
and are **never distributed**.

---

## Português (BR)

Troca a fonte da interface por uma **serifada** (Times New Roman; Georgia ou Liberation
Serif se faltar), preservando cor, contorno e sombra do texto. **Não altera gameplay.**

Os **textos de combate** (nome do inimigo, número do dado) também ganham a serifa: uma
variante de shader diferente (a fonte serifada é `Mobile/Distance Field`; esses textos usam
`Distance Field Overlay`/`(Surface)`) **não** é motivo de recusa — as propriedades de estilo
existem nas duas e a cópia é feita uma a uma. Com o **BetterCombatText** instalado, o texto
de combate fica com **a serifa e o halo/sombra** que ele aplicou. Só um efeito que a cópia
não reproduz mantém aquele texto intocado — são **cinco** motivos de recusa (textura de face,
bevel, `GLOW_ON`/`BEVEL_ON`, contorno/sombra que o material novo não expõe e a fonte serifada
ainda sem material; a lista completa está em inglês acima) — com o motivo
escrito no log (ligue `LogDiagnosticoEstilo`). Instalação, configuração e desinstalação
estão nas seções em inglês acima.
