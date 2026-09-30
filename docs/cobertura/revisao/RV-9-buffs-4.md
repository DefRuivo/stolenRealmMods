# RV-9 - Buffs: arquivo de trabalho (393 entradas)

Gerado do `status.csv`. **Descricoes COMPLETAS** (ja errei com texto truncado, RV-8c).
`dur` = duracao em turnos e `maxStk` = cap de stacks (campos `Duration`/`MaxStacks` do asset, l.319141/319149);
`VAR` = existem assets HOMONIMOS com valores diferentes - nesse caso confira por ASSET, nao por nome.

> ATENCAO: o nome NAO identifica o status. Assets homonimos tem papeis diferentes.

## Negating Tonic  [Common]
- efeitos: `MagicArmor:Base:50`
- dur=5 | maxStk=100
- descricao (completa): Magic armor increased by 50.
- ja no mod: nao

## Nullifying Tonic  [Common]
- efeitos: `MagicArmor:Base:100`
- dur=5 | maxStk=100
- descricao (completa): Magic armor increased by 100.
- ja no mod: nao

## Obsidian Plating  [Common]
- efeitos: `DamageReduction:Base:75`
- dur=1 | maxStk=10
- descricao (completa): Damage taken reduced by 75%.
- ja no mod: nao

## Oculus Gem  [Rare]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): Teleports you randomly when struck. 4 turn cooldown.  <i><color=#808080>Where you'll go, nobody knows!</i></color>
- ja no mod: nao

## Oil of Acceleration  [Common]
- efeitos: `TurnFreeMovementPoints:Base:5`
- dur=5 | maxStk=100
- descricao (completa): Movement Points increased by 5.
- ja no mod: nao

## Oil of Alacrity  [Common]
- efeitos: `TurnFreeMovementPoints:Base:4`
- dur=5 | maxStk=100
- descricao (completa): Movement Points increased by 4.
- ja no mod: nao

## Oil of Momentum  [Common]
- efeitos: `TurnFreeMovementPoints:Base:2`
- dur=5 | maxStk=100
- descricao (completa): Movement Points increased by 2.
- ja no mod: nao

## Oil of Movement  [Common]
- efeitos: `TurnFreeMovementPoints:Base:1`
- dur=5 | maxStk=100
- descricao (completa): Movement Points increased by 1.
- ja no mod: nao

## Oil of Speed  [Common]
- efeitos: `TurnFreeMovementPoints:Base:3`
- dur=5 | maxStk=100
- descricao (completa): Movement Points increased by 3.
- ja no mod: nao

## One Punch Monk  [Common]
- efeitos: `DamageMod:Base:Target.UsingIgnoreCostAction ? 0 : 200`
- dur=1 | maxStk=100
- descricao (completa): Your next ability has its damage or healing tripled.
- ja no mod: nao

## Otherworldly Tether  [Common]
- efeitos: `Invincible:Set:1`
- dur=10 | maxStk=10
- descricao (completa): The Dead One's tether to this world wanes.  Lasts [0] more round(s).
- ja no mod: nao

## Overcharge  [Common]
- efeitos: `(vazio)`
- dur=2 | maxStk=10
- descricao (completa): Adds *0 lightning damage to your next basic attack.  Can stack up to 10 times.
- ja no mod: nao

## Overflowing Energy  [Rare]
- efeitos: `IntelligenceBase:Base:{3,15}, ManaCostMod:Base:{4,20}, ManaPowerMod:Base:{8,40}`
- dur=0 | maxStk=1
- descricao (completa): Increases @Mana Costs@ by {4,20}%, power of all @Mana Abilites@ by {8,40}% and @Intelligence@ by {3,15}.  <i><color=#808080>The energies of a Mana Spring swell within you!</i></color>
- ja no mod: nao

## Overgrow  [Common]
- efeitos: `DamageMod:Base:25, MaxHealth:Percentage:25, ModelScaleMultiplier:Base:25`
- dur=3 | maxStk=1
- descricao (completa): Increases Damage Dealt and Max Health by 25%.
- ja no mod: nao

## Overload  [Common]
- efeitos: `CritChance:Set:100`
- dur=1 | maxStk=100
- descricao (completa): Critical Hit Chance set to 100%.
- ja no mod: nao

## Overwhelming Power  [Common]
- efeitos: `DamageMod:Base:100`
- dur=2 | maxStk=100
- descricao (completa): Increases the damage or healing of your next skill by 100%.
- ja no mod: nao

## Pain Suppression  [Common]
- efeitos: `DamageReduction:Base:50`
- dur=VAR | maxStk=VAR
- descricao (completa): Damage Reduction increased by 50%.
- ja no mod: nao

## Patient Hunter  [Common]
- efeitos: `DamageMod:Base:10, RangeTypeAdderRanged:Base:1`
- dur=1 | maxStk=5
- descricao (completa): Damage increased by 10%, Range increased by 1 per stack.
- ja no mod: nao

## Perfect Rage  [Common]
- efeitos: `DamageMod:Base:{50,100}, ModelScaleMultiplier:Base:20, AiControlledPlayer:Set:1`
- dur=VAR | maxStk=VAR
- descricao (completa): Cannot control your character. Increases damage by [0]%. Grants enrage.
- ja no mod: nao

## Perfect Rage  [Mythic]
- efeitos: `(vazio)`
- dur=VAR | maxStk=VAR
- descricao (completa): Grants the skill Perfect Rage.  <i><color=#808080>"Rage, like fire, in our veins does ignite, A storm within, both destroyer and might."</i></color>
- ja no mod: nao

## Phoenix Feather  [Rare]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): Brings you back with 20% Health. 1 charge per Quest.  <i><color=#808080>"The glowing feather of a Phoenix."</color></i>
- ja no mod: nao

## Physical Thorns  [Common]
- efeitos: `DamageReturnedFlatPhysical:Base:{1,300}`
- dur=3 | maxStk=1
- descricao (completa): Reflects [0] physical damage back to attackers.
- ja no mod: nao

## Point Blank  [Common]
- efeitos: `DamageMod:Base:50`
- dur=VAR | maxStk=VAR
- descricao (completa): Ranged spells deal damage the closer you are. Calculates how much ranged you have and the closer you are from your max range the more damage you deal.
- ja no mod: nao

## Point Blank  [Mythic]
- efeitos: `PerHexRangeDamageInverseBonus:Base:{3, 12}`
- dur=VAR | maxStk=VAR
- descricao (completa): Your ranged damage is increased by [0]% for every hex less than your max range you use.  <i><color=#808080>"Hardest shot in all the land!"</color></i>
- ja no mod: nao

## Poison Thorns  [Common]
- efeitos: `(vazio)`
- dur=2 | maxStk=100
- descricao (completa): Attackers take 2 stacks of poison.
- ja no mod: nao

## Poison Weapon  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Attacks apply @1@ stack of poison.
- ja no mod: nao

## Polished  [Uncommon]
- efeitos: `Armor:Base:{15,250}, MagicArmor:Base:{15,250}`
- dur=0 | maxStk=1
- descricao (completa): Increases @Armor@ and @Magic Armor@ by {15,250}.
- ja no mod: nao

## Potion of Avoidance  [Common]
- efeitos: `ReflexBase:Base:20`
- dur=5 | maxStk=100
- descricao (completa): Reflex increased by 20.
- ja no mod: nao

## Potion of Brawn  [Common]
- efeitos: `MightBase:Base:10`
- dur=5 | maxStk=100
- descricao (completa): Might increased by 10.
- ja no mod: nao

## Potion of Celerity  [Common]
- efeitos: `DexterityBase:Base:20`
- dur=5 | maxStk=100
- descricao (completa): Dexterity increased by 20.
- ja no mod: nao

## Potion of Dexterity  [Common]
- efeitos: `DexterityBase:Base:30`
- dur=5 | maxStk=100
- descricao (completa): Dexterity increased by 30.
- ja no mod: SIM

## Potion of Dexterity  [Common]
- efeitos: `DexterityBase:Base:50`
- dur=5 | maxStk=100
- descricao (completa): Dexterity increased by 50.
- ja no mod: nao

## Potion of Dexterity  [Common]
- efeitos: `DexterityBase:Base:10`
- dur=5 | maxStk=100
- descricao (completa): Dexterity increased by 10.
- ja no mod: nao

## Potion of Dexterity  [Common]
- efeitos: `DexterityBase:Base:40`
- dur=5 | maxStk=100
- descricao (completa): Dexterity increased by 40.
- ja no mod: nao

## Potion of Dodging  [Common]
- efeitos: `ReflexBase:Base:40`
- dur=5 | maxStk=100
- descricao (completa): Reflex increased by 40.
- ja no mod: nao

## Potion of Eluding  [Common]
- efeitos: `ReflexBase:Base:10`
- dur=5 | maxStk=100
- descricao (completa): Reflex increased by 10.
- ja no mod: nao

## Potion of Endurance  [Common]
- efeitos: `VitalityBase:Base:20`
- dur=5 | maxStk=100
- descricao (completa): Vitality increased by 20.
- ja no mod: nao

## Potion of Evasion  [Common]
- efeitos: `ReflexBase:Base:50`
- dur=5 | maxStk=100
- descricao (completa): Reflex increased by 50.
- ja no mod: nao

## Potion of Fire Protection  [Common]
- efeitos: `ImmunityHeat:Set:1, ResistFire:Base:30`
- dur=5 | maxStk=100
- descricao (completa): Fire resistance increased by 30%.   Immune to Heat.
- ja no mod: nao

## Potion of Force  [Common]
- efeitos: `MightBase:Base:40`
- dur=5 | maxStk=100
- descricao (completa): Might increased by 40.
- ja no mod: nao

## Potion of Fortitude  [Common]
- efeitos: `VitalityBase:Base:40`
- dur=5 | maxStk=100
- descricao (completa): Vitality increased by 40.
- ja no mod: nao

## Potion of Frost Protection  [Common]
- efeitos: `ImmunityChilled:Set:1, ResistCold:Base:30`
- dur=5 | maxStk=100
- descricao (completa): Cold resistance increased by 30%.   Immune to Chilled.
- ja no mod: nao

## Potion of Intelligence  [Common]
- efeitos: `IntelligenceBase:Base:40`
- dur=5 | maxStk=100
- descricao (completa): Intelligence increased by 40.
- ja no mod: nao

## Potion of Life  [Common]
- efeitos: `VitalityBase:Base:50`
- dur=5 | maxStk=100
- descricao (completa): Vitality increased by 50.
- ja no mod: nao

## Potion of Lightning Protection  [Common]
- efeitos: `ImmunityShocked:Set:1, ResistLightning:Base:30`
- dur=5 | maxStk=100
- descricao (completa): Lightning resistance increased by 30%.   Immune to Shocked.
- ja no mod: nao

## Potion of Might  [Common]
- efeitos: `MightBase:Base:30`
- dur=5 | maxStk=100
- descricao (completa): Might increased by 30.
- ja no mod: nao

## Potion of Mind  [Common]
- efeitos: `IntelligenceBase:Base:50`
- dur=5 | maxStk=100
- descricao (completa): Intelligence increased by 50.
- ja no mod: nao

## Potion of Physical Protection  [Common]
- efeitos: `ImmunityBleeding:Set:1, ResistPhysical:Base:30`
- dur=5 | maxStk=100
- descricao (completa): Physical resistance increased by 30%.   Immune to Bleed.
- ja no mod: nao

## Potion of Power  [Common]
- efeitos: `MightBase:Base:50`
- dur=5 | maxStk=100
- descricao (completa): Might increased by 50.
- ja no mod: nao

## Potion of Reason  [Common]
- efeitos: `IntelligenceBase:Base:20`
- dur=5 | maxStk=100
- descricao (completa): Intelligence increased by 20.
- ja no mod: nao

## Potion of Recovery  [Common]
- efeitos: `HealthPerTurnPercent:Base:8, ManaPerTurnPercent:Base:8`
- dur=5 | maxStk=100
- descricao (completa): Recover 8% of Max Health and Mana per turn.
- ja no mod: nao

## Potion of Recovery  [Common]
- efeitos: `HealthPerTurnPercent:Base:15`
- dur=5 | maxStk=100
- descricao (completa): Recover 15% of Max Health per turn.
- ja no mod: nao

## Potion of Recovery  [Common]
- efeitos: `ManaPerTurnPercent:Base:15`
- dur=5 | maxStk=100
- descricao (completa): Recover 15% of Max Mana per turn.
- ja no mod: nao

## Potion of Reflex  [Common]
- efeitos: `ReflexBase:Base:30`
- dur=5 | maxStk=100
- descricao (completa): Reflex increased by 30.
- ja no mod: nao

## Potion of Strength  [Common]
- efeitos: `MightBase:Base:20`
- dur=5 | maxStk=100
- descricao (completa): Might increased by 20.
- ja no mod: nao

## Potion of Thought  [Common]
- efeitos: `IntelligenceBase:Base:30`
- dur=5 | maxStk=100
- descricao (completa): Intelligence increased by 30.
- ja no mod: nao

## Potion of Vigor  [Common]
- efeitos: `VitalityBase:Base:5`
- dur=5 | maxStk=100
- descricao (completa): Vitality increased by 5.
- ja no mod: nao

## Potion of Vitality  [Common]
- efeitos: `VitalityBase:Base:30`
- dur=5 | maxStk=100
- descricao (completa): Vitality increased by 30.
- ja no mod: nao

## Potion of Wits  [Common]
- efeitos: `IntelligenceBase:Base:10`
- dur=5 | maxStk=100
- descricao (completa): Intelligence increased by 10.
- ja no mod: nao

## Power Globule  [Common]
- efeitos: `DamageMod:Base:10, SummonDamageMod:Base:10`
- dur=3 | maxStk=100
- descricao (completa): Increases damage and summon damage by 10%
- ja no mod: nao

## Prepared  [Common]
- efeitos: `DropQuantityMod:Base:20, GoldMod:Base:20`
- dur=0 | maxStk=100
- descricao (completa): Item and gold drops are increased by 20%.
- ja no mod: nao

## Prismatic Tonic  [Common]
- efeitos: `MagicArmor:Base:800`
- dur=5 | maxStk=100
- descricao (completa): Magic armor increased by 800.
- ja no mod: nao

## Protection Flask  [Common]
- efeitos: `Armor:Base:100`
- dur=5 | maxStk=100
- descricao (completa): Armor increased by 100.
- ja no mod: nao

## Quick Draw  [Common]
- efeitos: `QuickDraw:Set:1`
- dur=1 | maxStk=100
- descricao (completa): Your next 3 basic attacks have no AP cost.
- ja no mod: nao

## Rage  [Common]
- efeitos: `DamageMod:Base:15, DamageReduction:Base:-15, MaxHealth:Percentage:15, ModelScaleMultiplier:Base:10`
- dur=3 | maxStk=100
- descricao (completa): Increases damage dealt and max life by 15%. Increases damage received by 15%.
- ja no mod: nao

## Rage of the Dwarf King  [Common]
- efeitos: `DamageMod:Base:30, ModelScaleMultiplier:Base:10`
- dur=3 | maxStk=1
- descricao (completa): Increases damage dealt by 30%.
- ja no mod: nao
