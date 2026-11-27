# BetterPortuguese

- **Version:** 0.2.7
- **Author:** gumatos
- **Tested on:** Stolen Realm 1.4.9, Steam public build 26878331.
- **Requires:** BepInEx 5.

BetterPortuguese corrects Brazilian Portuguese text in the game without changing damage, loot, progression, or saves. It preserves the game's current text when the original no longer matches the recorded baseline.

## Install and configure

Install through r2modman in your Stolen Realm profile, or copy `plugins/BetterPortuguese/` into `BepInEx/plugins/`. Launch modded and set the game's language to Brazilian Portuguese.

The config file is `BepInEx/config/com.gumatos.betterportuguese.cfg`:

```ini
[Geral]
Ativo = true
Conjunto = Corrigido
IntegracaoMods = true
Diagnostico = false
```

- `Corrigido` enables the corrected text; `Original` leaves the game’s current text in place for this mod.
- `Ativo = false` disables the overlay. `IntegracaoMods = false` disables optional mod integration only.
- `Diagnostico = true` helps identify skipped text. Other languages keep their own text.

Both snapshots are embedded in the DLL; no separate data files are needed. The source data and its extraction details are available in the repository. No other mod is required. This is a localization update, not a fix for post-battle behavior.

## Uninstall or build

Disable the mod in r2modman or remove only `BepInEx/plugins/BetterPortuguese/`. To build from source with the local game references, use `dotnet build BetterPortuguese/BetterPortuguese.csproj -c Release -p:DeployToBepInEx=false`. Do not distribute game reference DLLs.

## Português (BR)

Corrige textos do jogo em PT-BR. Use `Conjunto = Corrigido` para as correções ou `Conjunto = Original` para voltar aos textos atuais do jogo. Não altera mecânicas nem partidas salvas.
