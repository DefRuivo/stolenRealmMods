# Varredura de tokens das tooltips — resultado

> Gerado por `python tools/scan_tokens.py` • 2280 entradas varridas.

**Regra extraída do código** (`Tooltip.ApplyDescriptionExpressions`): em descrição de skill/status/powerup, `[` sem dígito devolve `Parsing Error with:` **no lugar do tooltip inteiro**, e `[NN]` (2+ dígitos) faz o jogo ler só o primeiro dígito e usar a expressão errada.


## Veredito

**Nenhum caso nas categorias de expressão** (skills, status, powerups). Ou seja: os `[...]` que aparecem no censo **não são** placeholders vazando — cada um pertence a um pipeline que o jogo resolve.


### Classe A — `[` sem dígito (quebra o tooltip)

Nenhum caso.


### Classe B — índice de 2+ dígitos (valor errado)

Nenhum caso.


## Esperado (não é bug): categorias de template

`itens` e `afixos` usam `Localize(...).Replace("[token]", valor)` — os colchetes ali são tokens nomeados trocados pelo próprio chamador. **102 ocorrências**, todas esperadas.

<details><summary>ver a lista</summary>

| categoria | entrada | detalhe | descricao |
|---|---|---|---|
| afixos | Abyss | indice `[15]` com 2+ digitos | Shadow skill damage increased by [15]% |
| afixos | Apprentice | indice `[12]` com 2+ digitos | Weapon damage increased by [12]% |
| afixos | Artificer | indice `[24]` com 2+ digitos | Weapon damage increased by [24]% |
| afixos | Artisan | indice `[16]` com 2+ digitos | Weapon damage increased by [16]% |
| afixos | Avalanche | indice `[15]` com 2+ digitos | Cold skill damage increased by [15]% |
| afixos | Barbs | indice `[16]` com 2+ digitos |  +[16] Physical Damage Return. |
| afixos | Behemoth | indice `[25]` com 2+ digitos | Weapon damage increased by [25]% Movement points lowered by 1 |
| afixos | Brilliant | indice `[12]` com 2+ digitos | Intelligence increased by [12] |
| afixos | Butchery | indice `[45]` com 2+ digitos | Critical Hit Damage and Healing increased by [45]% |
| afixos | Caretaker's | indice `[10]` com 2+ digitos | Summon Health increased by [10]% |
| afixos | Carnage | indice `[35]` com 2+ digitos | Critical Hit Damage and Healing increased by [35]% |
| afixos | Colossus | indice `[30]` com 2+ digitos | Weapon damage increased by [30]% Movement points lowered |
| afixos | Conflagration | indice `[12]` com 2+ digitos | Fire skill damage increased by [12]% |
| afixos | Death Hunter | indice `[12]` com 2+ digitos | Summon Health increased by [12]% |
| afixos | Dexterous | indice `[15]` com 2+ digitos | Dexterity increased by [15] |
| afixos | Doctor | indice `[12]` com 2+ digitos | Holy power increased by [12]% |
| afixos | Enduring | indice `[12]` com 2+ digitos | Vitality increased by [12] |
| afixos | Evisceration | indice `[55]` com 2+ digitos | Critical Hit Damage and Healing increased by [55]% |
| afixos | Exceptional | indice `[10]` com 2+ digitos | +[10] to Weapon Damage |
| afixos | Exquisite | indice `[20]` com 2+ digitos | +[20] to Weapon Damage |
| afixos | Feral | indice `[10]` com 2+ digitos | Summon Damage increased by [10]% |
| afixos | Gargantuan | indice `[50]` com 2+ digitos | Armor increased by [50]% Movement points lowered 1 |
| afixos | Ghostly | indice `[15]` com 2+ digitos | Reflex increased by [15] |
| afixos | Giant | indice `[15]` com 2+ digitos | Weapon damage increased by [15]% Movement points lowered |
| afixos | Glacial | indice `[10]` com 2+ digitos | +[10] Damage to Cold |
| afixos | Glacier | indice `[12]` com 2+ digitos | Cold skill damage increased by [12]% |
| afixos | Goliath | indice `[20]` com 2+ digitos | Weapon damage increased by [20]% Movement points lowered |
| afixos | Gore | indice `[15]` com 2+ digitos | Critical Hit Damage and Healing increased by [15]% |
| afixos | Hallowed | indice `[10]` com 2+ digitos | +[10] added Healing. |
| afixos | Herculean | indice `[15]` com 2+ digitos | Might increased by [15] |
| afixos | Hulk | indice `[30]` com 2+ digitos | Armor increased by [30]% Movement points lowered 1 |
| afixos | Immortal | indice `[15]` com 2+ digitos | Vitality increased by [15] |
| afixos | Incorporeal | indice `[12]` com 2+ digitos | Reflex increased by [12] |
| afixos | Inferno | indice `[15]` com 2+ digitos | Fire skill damage increased by [15]% |
| afixos | Ingenious | indice `[15]` com 2+ digitos | Intelligence increased by [15] |
| afixos | Journeyman | indice `[20]` com 2+ digitos | Weapon damage increased by [20]% |
| afixos | Keeper's | indice `[12]` com 2+ digitos | Summon Health increased by [12]% |
| afixos | Leviathan | indice `[60]` com 2+ digitos | Armor increased by [60]% Movement points lowered 1 |
| afixos | Lich | indice `[12]` com 2+ digitos | Summon Damage increased by [12]% |
| afixos | Mammoth | indice `[20]` com 2+ digitos | Armor increased by [20]% Movement points lowered 1 |
| afixos | Mangler | indice `[12]` com 2+ digitos | Physical damage increased by [12]% |
| afixos | Master | indice `[28]` com 2+ digitos | Weapon damage increased by [28]% |
| afixos | Masterwork | indice `[30]` com 2+ digitos | +[30] to Weapon Damage |
| afixos | Mighty | indice `[12]` com 2+ digitos | Might increased by [12] |
| afixos | Monstrosity | indice `[40]` com 2+ digitos | Armor increased by [40]% Movement points lowered 1 |
| afixos | Necromancer | indice `[10]` com 2+ digitos | Summon Damage increased by [10]% |
| afixos | Perfected | indice `[40]` com 2+ digitos | +[40] to Weapon Damage |
| afixos | Primal | indice `[12]` com 2+ digitos | Summon Damage increased by [12]% |
| afixos | Pulverizer | indice `[15]` com 2+ digitos | Physical damage increased by [15]% |
| afixos | Savior | indice `[15]` com 2+ digitos | Holy power increased by [15]% |
| afixos | Scorching | indice `[10]` com 2+ digitos | +[10] Damage to Fire |
| afixos | Serrated | indice `[10]` com 2+ digitos | +[10] Damage to Physical |
| afixos | Shadows | indice `[12]` com 2+ digitos | Shadow skill damage increased by [12]% |
| afixos | Slaughter | indice `[25]` com 2+ digitos | Critical Hit Damage and Healing increased by [25]% |
| afixos | Sorcerer | indice `[12]` com 2+ digitos | Elemental skill damage increased by [12]% |
| afixos | Spikes | indice `[12]` com 2+ digitos |  +[12] Physical Damage Return. |
| afixos | Storms | indice `[15]` com 2+ digitos | Lightning skill damage increased by [15]% |
| afixos | Swift | indice `[12]` com 2+ digitos | Dexterity increased [12] |
| afixos | Thorns | indice `[20]` com 2+ digitos |  +[20] Physical Damage Return. |
| afixos | Thunder | indice `[12]` com 2+ digitos | Lightning skill damage increased by [12]% |
| afixos | Thunderstruck | indice `[10]` com 2+ digitos | +[10] Damage to Lightning |
| afixos | Titan | indice `[35]` com 2+ digitos | Weapon damage increased by [35]% Movement points lowered |
| afixos | Umbral | indice `[10]` com 2+ digitos | +[10] Damage to Shadow |
| afixos | Undertaker | indice `[10]` com 2+ digitos | Summon Health increased by [10]% |
| afixos | Wizard | indice `[15]` com 2+ digitos | Elemental skill damage increased by [15]% |
| itens | Abaddon | `[l` - sem digito depois do `[` | 20% chance to cast Level [level value] {SKL=Raise Servant of Abaddon} on enemy death. |
| itens | Ancient Sword | `[l` - sem digito depois do `[` | 10% chance to cast Level [level value] {SKL=Curse} when striking. |
| itens | Anthulk Shell | `[l` - sem digito depois do `[` | 25% Chance when hit to cast Level [level value] {SKL=Ankheg Spines}. |
| itens | Cold Steel Axe | `[l` - sem digito depois do `[` | 10% chance to cast Level [level value] {SKL=Ice Lance} on striking. |
| itens | Demon Skull | `[l` - sem digito depois do `[` | 10% chance when struck to cast Level [level value] {SKL=Burning Ground}. |
| itens | Dragon Fist | `[l` - sem digito depois do `[` | 5% chance to cast Level [level value] {SKL=Thunder Bolt} when hitting an enemy with any ability.  5% |
| itens | Earthshaker | `[l` - sem digito depois do `[` | 10% chance to cast Level [level value] {SKL=Stunning Slam} on striking. |
| itens | Ember King's Might | `[l` - sem digito depois do `[` | 15% chance to cast Level [level value] {SKL=Detonate} on striking. |
| itens | Ember King's Will | `[l` - sem digito depois do `[` | The wearer gains Level [level value] {SKL=Aura of Flame}. |
| itens | Emberstone Staff | `[l` - sem digito depois do `[` | 20% chance to cast Level [level value] {SKL=Burning Ground} when hitting with any ability. |
| itens | Fallen Cleric Robes | `[l` - sem digito depois do `[` | 10% chance on hit to cast Level [level value] {SKL=Consumption} |
| itens | Flame Vestments | `[l` - sem digito depois do `[` | Gain Level [level value] {SKL=Enchant Fire}. |
| itens | Foe-Crusher | `[l` - sem digito depois do `[` | 10% chance to cast Level [level value] {SKL=Slam} on striking. |
| itens | Forgemaster's Links | `[l` - sem digito depois do `[` | The wearer gains Level [level value] {SKL=Fire Shield}. |
| itens | Frost Mantle | `[l` - sem digito depois do `[` | Gain Level [level value] {SKL=Enchant Cold}. |
| itens | Gilded Kite Shield | `[l` - sem digito depois do `[` | 10% chance upon getting hit to cast Level [level value] {SKL=Shield of Light}. |
| itens | Hailstone Staff | `[l` - sem digito depois do `[` | 15% chance to cast Level [level value] {SKL=Frost Nova} when hitting with any ability. |
| itens | Harvester | `[l` - sem digito depois do `[` | 20% chance to cast Level [level value] {SKL=Reaper's Scythe} on striking. |
| itens | Ice King's Axe | `[l` - sem digito depois do `[` | 20% chance to cast Level [level value] {SKL=Breath of Winter} on striking. |
| itens | Ivory Aegis | `[l` - sem digito depois do `[` | 10% chance when hit to cast Level [level value] {SKL=Mass Cure}. |
| itens | Mjolnir | `[l` - sem digito depois do `[` | 10% chance to cast Level [level value] {SKL=Thunder Bolt} on striking. |
| itens | Phantom Piercer | `[l` - sem digito depois do `[` | 10% chance to cast Level [level value] {SKL=Reaper's Scythe} on striking. |
| itens | Phoenix Claymore | `[l` - sem digito depois do `[` | Grants the passive {SKL=Glory}. Gain Level [level value] {SKL=Enchant Fire} while holding this weapo |
| itens | Rockbreaker | `[l` - sem digito depois do `[` | 15% chance to cast Level [level value] {SKL=Fracture} when striking. |
| itens | Ruby Sword | `[l` - sem digito depois do `[` | 10% chance to apply Level [level value] {SKL=Immolate} on hit. |
| itens | Sapphire Sword | `[l` - sem digito depois do `[` | 10% chance to cast Level [level value] {SKL=Frost Shard} on hit. |
| itens | Shadow Stalker Bow | `[l` - sem digito depois do `[` | 10% chance to cast Level [level value] {SKL=Spectral Chains} on striking. 10% chance to cast Level [ |
| itens | Silver Kite Shield | `[l` - sem digito depois do `[` | 10% chance to cast Level [level value] {SKL=Blinding Light} when struck. |
| itens | Sunstone Necklace | `[l` - sem digito depois do `[` | 10% chance to cast Level [level value] {SKL=Blinding Light} when hitting with any ability. |
| itens | Sunstone Ring | `[l` - sem digito depois do `[` | 10% chance to cast Level [level value] {SKL=Blinding Light} when hitting with any ability. |
| itens | Thunder Robes | `[l` - sem digito depois do `[` | Gain Level [level value] {SKL=Enchant Lightning}. |
| itens | Thunderforce | `[l` - sem digito depois do `[` | 15% Chance to cast Level [level value] {SKL=Chain Lightning} when striking with this weapon. |
| itens | Thunderstone Staff | `[l` - sem digito depois do `[` | 10% chance to proc a Level [level value] {SKL=Thunder Bolt} when hitting with any ability. |
| itens | Topaz Sword | `[l` - sem digito depois do `[` | 8% chance on striking to cast Level [level value] {SKL=Shock}. |
| itens | Warmachine Gauntlet | `[l` - sem digito depois do `[` | 10% chance to cast Level [level value] {SKL=Meteor} when Striking. |
| itens | Westarch Defender | `[l` - sem digito depois do `[` | 10% chance to cast Level [level value] {SKL=Howl} when struck. |
| itens | Will to Survive | `[l` - sem digito depois do `[` | Gain Armor and Magic Armor equal to 2x your Might. 10% chance upon getting hit to cast Level [level  |

</details>

