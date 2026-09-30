# RV-9 — Debuffs: arquivo de trabalho (133 entradas)

Gerado do `status.csv` (coluna `beneficio`, vinda de `IsBeneficial`/`IsHarmful` sobre `SkillTags`).
**Descricoes COMPLETAS** — ja errei uma vez escrevendo nota sobre texto truncado (o `Meteor` do RV-8c).

> ATENCAO: existem ASSETS HOMONIMOS com papeis diferentes (`Holy Ground`, `Aura of Flame`, `Cursed`,
> `Taunted`, `Consumption`...). O nome NAO identifica o status - analise por asset, como no `Crippled` x `Slow`.

## Heat  [Common]
- efeitos: `ResistCold:Base:-5, ResistFire:Base:-5, ResistLightning:Base:-5`
- efeitosDano: `TargetStored['FireDamage'] = Source['AvatarOfFlame'] == 1 ?  Source.SpellPower('Fire') * .2f : 0`
- descricao (completa): Elemental resistance reduced by 5% per stack.  Lasts [0] turns.  Can stack up to 10 times.
- ja no mod: nao

## Howl  [Common]
- efeitos: `Feared:Set:1, Disabled:Set:1`
- descricao (completa): Causes you to run as far away as possible from the source of fear and leaves you unable to cast actions.
- ja no mod: nao

## Howl  [Common]
- efeitos: `DamageMod:Base:-20`
- descricao (completa): Damage dealt reduced by 20%.
- ja no mod: nao

## Ice Storm  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['ColdDamage'] = Source.SpellPower('Cold') * .9f`
- descricao (completa): Deals *0 cold damage to enemies in range.
- ja no mod: nao

## Immobilized  [Common]
- efeitos: `Rooted:Set:1`
- descricao (completa): Cannot move.
- ja no mod: nao

## Immolate  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['FireDamage'] = Source.SpellPower('Fire') * .5f`
- descricao (completa): Target takes *0 fire damage per turn.
- ja no mod: nao

## Into the Fray  [Common]
- efeitos: `MightBase:Percentage:2 * Target.NumEnemiesWithin(5), VitalityBase:Percentage:2 * Target.NumEnemiesWithin(5)`
- descricao (completa): Gain 2% @might@ and @vitality@ for every enemy within 5 hexes of your character.
- ja no mod: nao

## Lesser Damage  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['FireDamage'] = Source.SpellPower('Fire') * 0.15f; TargetStored['HolyDamage'] = Source.SpellPower('Light') * 0.15f; TargetStored['LightningDamage'] = Source.SpellPower('Lightning') * 0.15f; TargetStored['ColdDamage'] = Source.SpellPower('Cold') * 0.15f; TargetStored['PhysicalDamage'] = Source.SpellPower('Physical') * 0.15f; TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') * 0.15f`
- descricao (completa): Damaged.
- ja no mod: nao

## Lethal Life I  [Common]
- efeitos: `HealthPerTurnPercent:Base:-10`
- descricao (completa): Lose 10% of your Max Health at the start of each turn.
- ja no mod: nao

## Lethal Life II  [Common]
- efeitos: `HealthPerTurnPercent:Base:-15`
- descricao (completa): Lose 15% of your Max Health at the start of each turn.
- ja no mod: nao

## Lethal Life III  [Common]
- efeitos: `HealthPerTurnPercent:Base:-20`
- descricao (completa): Lose 20% of your Max Health at the start of each turn.
- ja no mod: nao

## Marked for Death  [Common]
- efeitos: `DamageReduction:Base:-50`
- descricao (completa): Damage Taken increased by 50%.
- ja no mod: nao

## Mass Haunt  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') * .5f`
- descricao (completa): Deals *0 damage.
- ja no mod: nao

## Meteor  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['FireDamage'] = Source.SpellPower('Fire') * .6f`
- descricao (completa): Targets in burning ground receive *0 fire damage.
- ja no mod: nao

## Mind Exhaustion  [Common]
- efeitos: `IntelligenceBase:Percentage:-5`
- descricao (completa): Intelligence reduced by 5%
- ja no mod: nao

## Missing Soul  [Common]
- efeitos: `MaxHealth:Percentage:-20, MaxMana:Percentage:-20`
- descricao (completa): Something important is missing from you. Max Health and Mana reduced by 20%.
- ja no mod: nao

## Mortal Fracture  [Common]
- efeitos: `ResistCold:Base:-20, ResistFire:Base:-20, ResistLightning:Base:-20, ResistPhysical:Base:-20, ResistDivine:Base:-20, HealingReceivedBonus:Base:-50`
- descricao (completa): @Resistances@ lowered by 20%. Reduces healing received by 50%.
- ja no mod: nao

## Mortally Wounded  [Common]
- efeitos: `HealingReceivedBonus:Base:-25`
- descricao (completa): Reduces @Healing Received@ by @25%@ per stack.
- ja no mod: nao

## Muddled Movement I  [Common]
- efeitos: `TurnFreeMovementPoints:Base:-1`
- descricao (completa): Movement Points reduced by 1.
- ja no mod: nao

## Muddled Movement II  [Common]
- efeitos: `TurnFreeMovementPoints:Base:-2`
- descricao (completa): Movement Points reduced by 2.
- ja no mod: nao

## Muddled Movement III  [Common]
- efeitos: `TurnFreeMovementPoints:Base:-3`
- descricao (completa): Movement Points reduced by 3.
- ja no mod: nao

## Petrification  [Common]
- efeitos: `TurnFreeMovementPoints:Base:-1, DamageReduction:Base:-20`
- descricao (completa): Each stack lowers @movement@ by 1 and increases @Damage Taken@ by 20%. When you reach 5 stacks you become @Petrified@ which consumes all Petrification stacks.
- ja no mod: nao

## Petrify  [Common]
- efeitos: `Rooted:Set:1, Disabled:Set:1, DamageReduction:Base:-100`
- descricao (completa): Stunned.  Damage Taken increased by 100%.
- ja no mod: nao

## Poisoned  [Common]
- efeitos: `HealingReceivedBonus:Base:-1, PoisonDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Poisoned", "TargetStored[\"ShadowDamage\"] = Source.SpellPower(\"Shadow\") * .1f")), ContagionLevel:Base:Source["ContagionSource"] > 0 ? 1 : 0`
- descricao (completa): Target takes [1] shadow damage each turn. Reduces healing taken by [0]%.
- ja no mod: nao

## Rage Spores  [Common]
- efeitos: `DamageMod:Base:25, DamageReduction:Base:-25`
- descricao (completa): Increases damage dealt and received by 25%.
- ja no mod: nao

## Reduced Resistances I  [Common]
- efeitos: `ResistCold:Base:-10, ResistFire:Base:-10, ResistLightning:Base:-10, ResistPhysical:Base:-10`
- descricao (completa): All Resistances reduced by 10%
- ja no mod: nao

## Reduced Resistances II  [Common]
- efeitos: `ResistCold:Base:-20, ResistFire:Base:-20, ResistLightning:Base:-20, ResistPhysical:Base:-20`
- descricao (completa): All Resistances reduced by 20%
- ja no mod: nao

## Reduced Resistances III  [Common]
- efeitos: `ResistCold:Base:-30, ResistFire:Base:-30, ResistLightning:Base:-30, ResistPhysical:Base:-30`
- descricao (completa): All Resistances reduced by 30%
- ja no mod: nao

## Restrained  [Common]
- efeitos: `ReflexBase:Percentage:-20`
- descricao (completa): Reduces @Reflex@ by @20%@ per stack.
- ja no mod: nao

## Restricted Range I  [Common]
- efeitos: `RangeTypeAdderRanged:Base:-2`
- descricao (completa): Range is reduced by 2 Hexes.
- ja no mod: nao

## Restricted Range II  [Common]
- efeitos: `RangeTypeAdderRanged:Base:-4`
- descricao (completa): Range is reduced by 4 Hexes.
- ja no mod: nao

## Restricted Range III  [Common]
- efeitos: `RangeTypeAdderRanged:Base:-6`
- descricao (completa): Range is reduced by 6 Hexes.
- ja no mod: nao

## Ritual Sickness  [Common]
- efeitos: `DarkRitualedRecently:Set:1`
- descricao (completa): Cannot have Dark Ritual cast on you
- ja no mod: nao

## Savage Scorn  [Common]
- efeitos: `DamageReduction:Base:-20`
- descricao (completa): Damage taken increased by 20%.
- ja no mod: nao
