# RV-9 — Debuffs: arquivo de trabalho (133 entradas)

Gerado do `status.csv` (coluna `beneficio`, vinda de `IsBeneficial`/`IsHarmful` sobre `SkillTags`).
**Descricoes COMPLETAS** — ja errei uma vez escrevendo nota sobre texto truncado (o `Meteor` do RV-8c).

> ATENCAO: existem ASSETS HOMONIMOS com papeis diferentes (`Holy Ground`, `Aura of Flame`, `Cursed`,
> `Taunted`, `Consumption`...). O nome NAO identifica o status - analise por asset, como no `Crippled` x `Slow`.

---

## Aged  [Common]
- efeitos: `MightBase:Percentage:-10, DexterityBase:Percentage:-10`
- descricao (completa): You have been magically aged! Might and Dexterity are reduced by 10%.
- ja no mod: nao

## Anthulk Venom  [Common]
- efeitos: `DamageFlatPhysicalTarget:Base:ActionStatus.GetFlatDamageValue * .5f`
- descricao (completa): The target takes [0] increased flat physical damage. Stacks up to 10 times.
- ja no mod: nao

## Anthulk Venom  [Mythic]
- efeitos: `DamageFlatPhysicalTarget:Base:ActionStatus.GetFlatDamageValue * .5f`
- descricao (completa): The target takes [0] increased flat physical damage. Stacks up to 5 times.
- ja no mod: nao

## Aura of Flame  [Common]
- efeitos: `(vazio)`
- descricao (completa): *0 fire damage dealt to enemies within the aura.
- ja no mod: nao

## Aura of Flame  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['FireDamage'] = Source.SpellPower('Fire') * .4f`
- descricao (completa): [0] fire damage dealt to enemies within the aura.
- ja no mod: nao

## Aura of Frost  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['ColdDamage'] = Source.SpellPower('Cold') * .4f`
- descricao (completa): Deals *0 cold damage per turn while in the aura.
- ja no mod: nao

## Aura of Lightning  [Common]
- efeitos: `(vazio)`
- descricao (completa): *0 lightning damage dealt to enemies within the aura each time they perform an action.
- ja no mod: nao

## Battered  [Common]
- efeitos: `Armor:Percentage:-25, MagicArmor:Percentage:-25`
- descricao (completa): Reduces @Armor@ and @Magic Armor@ by @25%@ per stack.
- ja no mod: nao

## Bleeding  [Common]
- efeitos: `ResistPhysical:Base:-5, BleedingDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Bleeding", "TargetStored[\"PhysicalDamage\"] = Source.AttackPower * .05f"))`
- descricao (completa): Target takes [1] physical damage for each hex they move. Reduces Physical Resistance by [0]%.
- ja no mod: nao

## Blind  [Common]
- efeitos: `Blind:Set:1`
- descricao (completa): Skill range is reduced to 1 hex.
- ja no mod: nao

## Blind  [Common]
- efeitos: `Blind:Set:1`
- descricao (completa): Blind.
- ja no mod: nao

## Blood Boil  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') * .4f`
- descricao (completa): Target takes *0 shadow damage per turn.
- ja no mod: nao

## Blood Howl  [Common]
- efeitos: `LifeOnHitTarget:Base:4`
- descricao (completa): Attackers lifesteal for [0]%.
- ja no mod: nao

## Brain Freeze  [Common]
- efeitos: `(vazio)`
- descricao (completa): Deals 8% of the targets Max Health in cold damage each time the target performs an action.
- ja no mod: nao

## Brain Freeze  [Common]
- efeitos: `(vazio)`
- descricao (completa): *0 cold damage is applied to the target when they perform an action.
- ja no mod: nao

## Bruised  [Common]
- efeitos: `MaxHealth:Percentage:-10`
- descricao (completa): Reduces @Max Health@ by @10%@ per stack.
- ja no mod: nao

## Burning Ground  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['FireDamage'] = Target.TeamIndex == 1 ? Target.FodderHealthAtLevel * .3f : Source.SpellPower('Fire') * .5f`
- descricao (completa): Targets in burning ground receive fire damage.
- ja no mod: nao

## Burning Ground  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['FireDamage'] = Source.SpellPower('Fire') * .5f`
- descricao (completa): Targets in burning ground receive *0 fire damage.
- ja no mod: nao

## Chaos Curse  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['ColdDamage'] = Source.GetRollResult(50) ? Source.SpellPower('Cold') * 0.13f : 0; TargetStored['FireDamage'] = Source.GetRollResult(50) ? Source.SpellPower('Fire') * 0.13f : 0; TargetStored['LightningDamage'] = Source.GetRollResult(50) ? Source.SpellPower('Lightning') * 0.13f : 0; TargetStored['PhysicalDamage'] = Source.GetRollResult(50) ? Source.SpellPower('Physical') * 0.13f : 0; TargetStored['ShadowDamage'] = Source.GetRollResult(50) ? Source.SpellPower('Shadow') * 0.13f : 0; TargetStored['HolyDamage'] = Source.GetRollResult(50) ? Source.SpellPower('Light') * 0.13f : 0`
- descricao (completa): Cursed to take damage. Each element has a @50%@ chance to deal *0 damage every turn.
- ja no mod: nao

## Chi Strike  [Common]
- efeitos: `DamageMod:Base:-20`
- descricao (completa): Your damage dealt is reduced by 20%
- ja no mod: nao

## Chilled  [Common]
- efeitos: `TurnFreeMovementPoints:Base:Target.CanBeEffectedByChilled ? (Target.ChilledEffectHalved ? -.5f : -1) : 0, DamageMod:Base:-(Source["ChilledDamageReduction"]), MaxHealth:Percentage:Source["Frostbite"] == 1 ? -5 : 0, Armor:Percentage:Source["InvulnerableWinter"] == 1 ? 5 : 0, MagicArmor:Percentage:Source["InvulnerableWinter"] == 1 ? 5 : 0`
- descricao (completa): Movement points reduced by one per stack.  Lasts 2 turns.  Five stacks of Chilled freezes the target.
- ja no mod: nao

## Confused  [Common]
- efeitos: `IntelligenceBase:Percentage:-20`
- descricao (completa): Reduces @Intelligence@ by @20%@ per stack.
- ja no mod: nao

## Consumption  [Common]
- efeitos: `MaxHealth:Percentage:-20`
- descricao (completa): @Maximum health@ reduced by 20%.
- ja no mod: nao

## Consumption  [Common]
- efeitos: `MaxHealth:Percentage:10`
- descricao (completa): Max Health increased by 10%.
- ja no mod: nao

## Consumption  [Common]
- efeitos: `MaxHealth:Percentage:-10`
- descricao (completa): @Maximum health@ reduced by 10%.
- ja no mod: nao

## Contagion  [Common]
- efeitos: `HealingReceivedBonus:Base:-1`
- efeitosDano: `TargetStored['ShadowDamage'] = Source['ContagionLevel']`
- descricao (completa): Target takes [1] shadow damage each turn. Reduces healing taken by [0]%.
- ja no mod: nao

## Corrosive Bite  [Common]
- efeitos: `ResistPhysical:Base:-10, ResistCold:Base:-10, ResistFire:Base:-10, ResistLightning:Base:-10`
- descricao (completa): Lowers All Resistance by 10% per stack.
- ja no mod: nao

## Corrupted Consumables I  [Common]
- efeitos: `ConsumableCooldown:Base:1`
- descricao (completa): Consumable Cooldown increased by 1.
- ja no mod: nao

## Corrupted Consumables II  [Common]
- efeitos: `ConsumableCooldown:Base:2`
- descricao (completa): Consumable Cooldown increased by 2.
- ja no mod: nao

## Corrupted Consumables III  [Common]
- efeitos: `ConsumableCooldown:Base:3`
- descricao (completa): Consumable Cooldown increased by 3.
- ja no mod: nao

## Crippled  [Common]
- efeitos: `TurnFreeMovementPoints:Base:-1`
- descricao (completa): Reduces @Movement Points@ by @1@ per stack.
- ja no mod: nao

## Crystal Bite  [Common]
- efeitos: `DamageReduction:Base:-10, TurnFreeMovementPoints:Base:-1`
- efeitosDano: `TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') * .3f`
- descricao (completa): Target takes *0 shadow damage each turn, increases damage taken by 10% and reduces movement by 1. Stacks up to 5 times.
- ja no mod: nao

## Curse  [Common]
- efeitos: `ResistPhysical:Base:-20, ResistCold:Base:-20, ResistFire:Base:-20, ResistLightning:Base:-20, ResistDivine:Base:-20, HealingReceivedBonus:Base:-50`
- descricao (completa): @All resistances@ lowered by 20%. Healing received lowered by 50%.
- ja no mod: nao

## Curse of Death  [Common]
- efeitos: `(vazio)`
- descricao (completa): Cursed to die when this status expires.
- ja no mod: nao

## Curse of Elements  [Common]
- efeitos: `ResistCold:Base:-25, ResistFire:Base:-25, ResistLightning:Base:-25`
- descricao (completa): Reduces Elemental resistances by 25%.
- ja no mod: nao

## Curse of Frailty  [Common]
- efeitos: `ResistPhysical:Base:-25`
- descricao (completa): Reduces Physical resistance by 25%.
- ja no mod: nao

## Curse of Ruin  [Common]
- efeitos: `MightBase:Percentage:-15, DexterityBase:Percentage:-15, IntelligenceBase:Percentage:-15, VitalityBase:Percentage:-15, Recovery:Percentage:-15`
- descricao (completa): All stats reduced by 15%
- ja no mod: nao

## Curse of Sorrow  [Common]
- efeitos: `HealingReceivedBonus:Base:-50`
- descricao (completa): Healing is reduced by 50%.
- ja no mod: nao

## Curse of Weakness  [Common]
- efeitos: `DamageMod:Base:-25`
- descricao (completa): Damage reduced by 25%.
- ja no mod: nao

## Cursed  [Common]
- efeitos: `(vazio)`
- descricao (completa): Applies Curse on striking and when struck
- ja no mod: nao

## Cursed  [Common]
- efeitos: `MightBase:Percentage:-10, DexterityBase:Percentage:-10, IntelligenceBase:Percentage:-10, VitalityBase:Percentage:-10, ReflexBase:Percentage:-10`
- descricao (completa): Reduces @All Stats@ by @10%@ per stack.
- ja no mod: nao

## Cursed Bite  [Common]
- efeitos: `HealingReceivedBonus:Base:-50`
- descricao (completa): Reduces healing received by 50%.
- ja no mod: nao

## Damage  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['FireDamage'] = Source.SpellPower('Fire') * 0.3f; TargetStored['HolyDamage'] = Source.SpellPower('Light') * 0.3f; TargetStored['LightningDamage'] = Source.SpellPower('Lightning') * 0.3f; TargetStored['ColdDamage'] = Source.SpellPower('Cold') * 0.3f; TargetStored['PhysicalDamage'] = Source.SpellPower('Physical') * 0.3f; TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') * 0.3f`
- descricao (completa): Damaged.
- ja no mod: nao

## Damage Reduced by 20%  [Common]
- efeitos: `DamageMod:Base:-20`
- descricao (completa): Damage reduced by 20%.
- ja no mod: nao

## Damage Reduced by 5%  [Common]
- efeitos: `DamageMod:Base:-5`
- descricao (completa): Damage reduced by 5%.
- ja no mod: nao

## Damage Reduced by 50%  [Common]
- efeitos: `DamageMod:Base:-50`
- descricao (completa): Damage reduced by 50%.
- ja no mod: nao

## Death  [Common]
- efeitos: `(vazio)`
- efeitosDano: `Target.Kill()`
- descricao (completa): Death.
- ja no mod: nao

## Decaying  [Common]
- efeitos: `MaxHealth:Percentage:-25`
- descricao (completa): Max Health reduced by 25%.
- ja no mod: nao

## Dire Bite  [Common]
- efeitos: `HealingReceivedBonus:Base:-100`
- descricao (completa): Reduces healing received by 100%.
- ja no mod: nao

## Dire Howl  [Common]
- efeitos: `LifeOnHitTarget:Base:6`
- descricao (completa): Attackers lifesteal for [0]%.
- ja no mod: nao

## Disabled  [Common]
- efeitos: `Disabled:Set:1`
- descricao (completa): Cannot perform actions.
- ja no mod: nao

## Disappointment  [Common]
- efeitos: `DamageMod:Base:-20`
- descricao (completa): The disappointment of <color=#EE4B2B><b>Shawn</b></color> follows your every move. You swiftly leave to escape. Damage and healing done are reduced by 20%.
- ja no mod: nao

## Diseased  [Common]
- efeitos: `MaxHealth:Percentage:-15`
- descricao (completa): Maximum health reduced by 15%.
- ja no mod: nao

## Dispelling Fracture  [Common]
- efeitos: `ResistPhysical:Base:-20, ResistCold:Base:-20, ResistFire:Base:-20, ResistLightning:Base:-20, ResistDivine:Base:-20`
- descricao (completa): @Resistance@ lowered by 20%.
- ja no mod: nao

## Dreadful Dissonance  [Common]
- efeitos: `Feared:Set:1, Disabled:Set:1`
- descricao (completa): Feared.
- ja no mod: nao

## Enfeebled  [Common]
- efeitos: `DamageMod:Base:-20`
- descricao (completa): Reduces @Damage@ by @20%@ per stack.
- ja no mod: nao

## Exhaustion  [Common]
- efeitos: `RecentlyHasted:Set:1`
- descricao (completa): Cannot receive additional actions points.  Caused by receiving additional action points this turn.
- ja no mod: nao

## Faerie Swarm  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['PhysicalDamage'] = Source.SpellPower('Physical') * .4f`
- descricao (completa): Target takes *0 physical damage and 1 stack of {STA=Bleeding} per turn.
- ja no mod: nao

## Fatigued  [Common]
- efeitos: `DexterityBase:Percentage:-20`
- descricao (completa): Reduces Dexterity by @20%@ per stack.
- ja no mod: nao

## Focused Strike  [Common]
- efeitos: `DamageReduction:Base:-20`
- descricao (completa): Increases damage received by 20%.
- ja no mod: nao

## Fracture  [Common]
- efeitos: `ResistPhysical:Base:-20, ResistCold:Base:-20, ResistFire:Base:-20, ResistLightning:Base:-20, ResistDivine:Base:-20`
- descricao (completa): @Resistance@ lowered by 20%.
- ja no mod: nao

## Fractured Foot  [Common]
- efeitos: `TurnFreeMovementPoints:Base:-2`
- descricao (completa): Decreases movement points by 2.
- ja no mod: nao

## Frostbitten  [Common]
- efeitos: `ResistCold:Base:-25`
- descricao (completa): Reduces @Cold Resistance@ by @25%@ per stack.
- ja no mod: nao

## Frozen  [Common]
- efeitos: `Rooted:Set:1, Disabled:Set:1, ImmunityChilled:Set:1`
- descricao (completa): Cannot move or perform actions.
- ja no mod: nao

## Gore  [Common]
- efeitos: `HealingReceivedBonus:Base:-50`
- descricao (completa): Reduces healing received by 50%.
- ja no mod: nao

## Greater Damage  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['FireDamage'] = Source.SpellPower('Fire') * 0.6f; TargetStored['HolyDamage'] = Source.SpellPower('Light') * 0.6f; TargetStored['LightningDamage'] = Source.SpellPower('Lightning') * 0.6f; TargetStored['ColdDamage'] = Source.SpellPower('Cold') * 0.6f; TargetStored['PhysicalDamage'] = Source.SpellPower('Physical') * 0.6f; TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') * 0.6f`
- descricao (completa): Damaged.
- ja no mod: nao

## Haunt  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') * .5f; SourceStored['HealingForced'] = (Source['MaxHealth'] * .025f)`
- descricao (completa): Deals *0 damage. Lifesteals for 8%.
- ja no mod: nao

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

