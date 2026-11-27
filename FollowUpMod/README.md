# FollowUpMod

- **Version:** 0.1.0
- **Author:** gumatos
- **Tested on:** Stolen Realm 1.4.9, Steam public build 26878331, Roguelike co-op host and guest.

FollowUpMod raises the character you pick for a co-op Roguelike party up to the party's level. A level-1 character joining a group already at level 15 enters at level 15 and receives the native level rewards (skill, item and attribute choices). Characters **above** the party level are left alone: whether they are accepted stays the game's own rule, with the original level tolerance - the mod never lowers a character.

The promotion belongs to that party session only. While the character is promoted, its file is not written: the level, the skills and the items granted in that group stay in memory, and when the session ends the character is back to where it was. Other characters in the party keep saving normally.

## Install and configure

Install through r2modman, or copy `plugins/FollowUpMod/` into `BepInEx/plugins/`. Every player who wants the adjustment must have the mod, and all copies must be the same version; the host publishes the party rule into the Steam lobby so a host without the mod simply keeps the original behaviour. Only Roguelike co-op is affected - campaign and Hardcore keep the original rules.

There is no configuration to change. Open `BepInEx/LogOutput.log` and look for `FollowUpMod 0.1.0 ativo: 4/4 patches` after boot; the gate line `FU: gate nivel=... grupoMin=... aceito=...` shows what was decided for each character you pick.

If the party level is above the game ceiling (20 without other mods), the character is promoted up to the ceiling and the log says `ceiling_limited`. The gate log line `FU: gate nivel=... ancora=... minimo=... promove=...` shows both the party level and the lowest member level.

## Build

From the repository root, with the game installed and `lib/` present:

```bash
dotnet build FollowUpMod/FollowUpMod.csproj -c Release -p:DeployToBepInEx=false
```

## Português (BR)

Ajusta o personagem escolhido ao nível mínimo do grupo de co-op Roguelike e entrega as recompensas nativas de nível (habilidade, item e atributo). Personagens acima do mínimo continuam recusados, como no original. O nível promovido não é gravado no save: ao sair do grupo o personagem volta ao nível de antes.
