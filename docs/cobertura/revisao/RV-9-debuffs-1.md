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
