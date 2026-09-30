# RV-9 — Debuffs: arquivo de trabalho (133 entradas)

Gerado do `status.csv` (coluna `beneficio`, vinda de `IsBeneficial`/`IsHarmful` sobre `SkillTags`).
**Descricoes COMPLETAS** — ja errei uma vez escrevendo nota sobre texto truncado (o `Meteor` do RV-8c).

> ATENCAO: existem ASSETS HOMONIMOS com papeis diferentes (`Holy Ground`, `Aura of Flame`, `Cursed`,
> `Taunted`, `Consumption`...). O nome NAO identifica o status - analise por asset, como no `Crippled` x `Slow`.

## Self Awareness  [Common]
- efeitos: `MaxHealth:Percentage:-20, CritChance:Base:10`
- descricao (completa): Max Health is reduced by 20%. Crit Chance is increased by 10%.
- ja no mod: nao

## Self Doubt  [Common]
- efeitos: `MaxMana:Percentage:-20, DodgeChance:Base:10`
- descricao (completa): Max Mana is reduced by 20%. Dodge Chance is increased by 10%.
- ja no mod: nao

## Severely Burned  [Common]
- efeitos: `ResistFire:Base:-25`
- descricao (completa): Reduces @Fire Resistance@ by @25%@ per stack.
- ja no mod: nao

## Shapeshift: Box  [Common]
- efeitos: `DamageReduction:Base:-100, Rooted:Set:1, Silenced:Set:1`
- descricao (completa): Shapeshifted into a box. Damage taken increased by 100%.
- ja no mod: nao

## Shocked  [Common]
- efeitos: `CritDamageTarget:Base:10`
- descricao (completa): Incoming critical strike damage increased by 10% per stack.  Lasts 3 turns.  Can stack up to 10 times.
- ja no mod: nao

## Shocked  [Common]
- efeitos: `ResistLightning:Base:-25`
- descricao (completa): Reduces @Lightning Resistance@ by @25%@ per stack.
- ja no mod: nao

## Shocking Aura  [Common]
- efeitos: `(vazio)`
- descricao (completa): *0 lightning damage dealt to enemies within the aura each time they perform an action.
- ja no mod: nao

## Sleep  [Common]
- efeitos: `Rooted:Set:1, Disabled:Set:1, DamageReduction:Base:-50`
- descricao (completa): Cannot move or perform actions and damage taken increased by 50%.  Can be awakened by getting attacked.
- ja no mod: nao

## Sleep  [Common]
- efeitos: `Rooted:Set:1, Disabled:Set:1, DamageReduction:Base:-50`
- descricao (completa): Asleep.
- ja no mod: nao

## Slow  [Common]
- efeitos: `MovementCostPerHexMod:Set:100`
- descricao (completa): Movement costs doubled.
- ja no mod: nao

## Slowed  [Common]
- efeitos: `CooldownMod:Base:1, CooldownModBasic:Base:-1`
- descricao (completa): @Cooldowns@ increased by @1@ turn.
- ja no mod: nao

## Sludge  [Common]
- efeitos: `TurnFreeMovementPoints:Base:-1, DamageMod:Base:-5, RangeTypeAdderRanged:Base:-1`
- descricao (completa): Lowers movement and range by 1 and lowers Damage by 5% per stack.
- ja no mod: nao

## Sludge Bolt  [Common]
- efeitos: `TurnFreeMovementPoints:Base:-1, DamageMod:Base:-10, RangeTypeAdderRanged:Base:-1`
- descricao (completa): Lowers movement and range by 1 and lowers Damage by 10% per stack.
- ja no mod: nao

## Smashed  [Common]
- efeitos: `MightBase:Percentage:-15, DexterityBase:Percentage:-15, IntelligenceBase:Percentage:-15, VitalityBase:Percentage:-15, ReflexBase:Percentage:-15`
- descricao (completa): Breathing hurts quite a bit. All stats reduced by 15%
- ja no mod: nao

## Smelt  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['FireDamage'] = Source.SpellPower('Fire') * .6f`
- descricao (completa): Target takes *0 fire damage per turn.
- ja no mod: nao

## Soul Fire  [Common]
- efeitos: `HealingReceivedBonus:Base:-50`
- descricao (completa): Healing Received reduced by 50%.
- ja no mod: nao

## Soul Fracture  [Common]
- efeitos: `MaxHealth:Percentage:-25, MaxMana:Percentage:-25`
- descricao (completa): @Maximum health@ and @maximum mana@ lowered by 25%.
- ja no mod: nao

## Spectral Mark  [Common]
- efeitos: `DamageReduction:Base:-50`
- descricao (completa): Damage taken increased by 50%.
- ja no mod: nao

## Spore Cloud  [Common]
- efeitos: `DamageMod:Base:-10, TurnFreeMovementPoints:Base:-1`
- descricao (completa): Decreases damage dealt by 10% and movement by 1. Stacks up to 5 times.
- ja no mod: nao

## Stunned  [Common]
- efeitos: `Rooted:Set:1, Disabled:Set:1`
- descricao (completa): Cannot move or perform actions.
- ja no mod: nao

## Stunned  [Common]
- efeitos: `Rooted:Set:1, Disabled:Set:1`
- descricao (completa): Stunned.
- ja no mod: nao

## Sundered  [Common]
- efeitos: `ResistPhysical:Base:-25`
- descricao (completa): Reduces @Physical Resistance@ by @25%@ per stack.
- ja no mod: nao

## Taunted  [Common]
- efeitos: `Taunted:Set:1`
- descricao (completa): Taunted.
- ja no mod: nao

## Taunted  [Common]
- efeitos: `DamageMod:Base:-20, Taunted:Set:1`
- descricao (completa): Forced to attack the taunter. Damage reduced by 20%.
- ja no mod: nao

## Test Event Status - Critical Failure  [Common]
- efeitos: `MightBase:Percentage:-5, DexterityBase:Percentage:-5, IntelligenceBase:Percentage:-5, VitalityBase:Percentage:-5, ReflexBase:Percentage:-5`
- descricao (completa): Critical Failure
- ja no mod: nao

## Test Event Status - Failure  [Common]
- efeitos: `MightBase:Percentage:-5, DexterityBase:Percentage:-5, IntelligenceBase:Percentage:-5, VitalityBase:Percentage:-5, ReflexBase:Percentage:-5`
- descricao (completa): Failure
- ja no mod: nao

## The Bad Bloom  [Common]
- efeitos: `(vazio)`
- descricao (completa): Enemies gain 2 stacks of poison.
- ja no mod: nao

## Torn Soul  [Common]
- efeitos: `MightBase:Percentage:-5, DexterityBase:Percentage:-5, IntelligenceBase:Percentage:-5, VitalityBase:Percentage:-5, ReflexBase:Percentage:-5`
- descricao (completa): All stats reduced by 5%
- ja no mod: nao

## Visually Impaired  [Common]
- efeitos: `RangeTypeAdderRanged:Base:-3`
- descricao (completa): Reduces @Range@ by @3@ per stack.
- ja no mod: nao

## Weakened  [Common]
- efeitos: `MightBase:Percentage:-20`
- descricao (completa): Reduces @Might@ by 20% per stack.
- ja no mod: nao

## Wilting  [Common]
- efeitos: `Recovery:Percentage:-30`
- descricao (completa): Recovery reduced by 30%.
- ja no mod: nao

## You Are Smart  [Common]
- efeitos: `IntelligenceBase:Percentage:1000`
- descricao (completa): Intelligence increased.
- ja no mod: nao

