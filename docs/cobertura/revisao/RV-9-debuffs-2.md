# RV-9 — Debuffs: arquivo de trabalho (133 entradas)

Gerado do `status.csv` (coluna `beneficio`, vinda de `IsBeneficial`/`IsHarmful` sobre `SkillTags`).
**Descricoes COMPLETAS** — ja errei uma vez escrevendo nota sobre texto truncado (o `Meteor` do RV-8c).

> ATENCAO: existem ASSETS HOMONIMOS com papeis diferentes (`Holy Ground`, `Aura of Flame`, `Cursed`,
> `Taunted`, `Consumption`...). O nome NAO identifica o status - analise por asset, como no `Crippled` x `Slow`.

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
