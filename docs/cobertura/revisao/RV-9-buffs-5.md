# RV-9 - Buffs: arquivo de trabalho (393 entradas)

Gerado do `status.csv`. **Descricoes COMPLETAS** (ja errei com texto truncado, RV-8c).
`dur` = duracao em turnos e `maxStk` = cap de stacks (campos `Duration`/`MaxStacks` do asset, l.319141/319149);
`VAR` = existem assets HOMONIMOS com valores diferentes - nesse caso confira por ASSET, nao por nome.

> ATENCAO: o nome NAO identifica o status. Assets homonimos tem papeis diferentes.

## Rage Unleashed  [Common]
- efeitos: `DamageMod:Base:50, DamageReduction:Base:-50`
- dur=0 | maxStk=100
- descricao (completa): @Damage@ dealt and taken increased by @50@%.  <i><color=#808080>"You have given into your rage!"</i></color>
- ja no mod: nao

## Rainstorm  [Common]
- efeitos: `ManaPowerMod:Base:50`
- dur=3 | maxStk=100
- descricao (completa): Increases the power of mana using abilities by 50%.
- ja no mod: nao

## Rally  [Common]
- efeitos: `TurnFreeMovementPoints:Base:3`
- efeitosDano: `Target['FreeMovementPoints'] = Target['FreeMovementPoints'] + 3`
- dur=1 | maxStk=100
- descricao (completa): Increases @movement points@ by 3.
- ja no mod: nao

## Rampage  [Common]
- efeitos: `ExtraTurnActionPoints:Base:1, ModelScaleMultiplier:Base:15, DamageMod:Base:50, DamageReduction:Base:-50`
- dur=3 | maxStk=1
- descricao (completa): Increases damage dealt and taken by 50%. Grants 1 additional Action Point
- ja no mod: nao

## Rampaging  [Common]
- efeitos: `DamageMod:Base:50, ResistCold:Base:-25, ResistFire:Base:-25, ResistLightning:Base:-25, ResistPhysical:Base:-25, CanEnrage:Set:1`
- dur=3 | maxStk=100
- descricao (completa): Increased damage by 50% All resistances lowered by 25% Control Resistance
- ja no mod: nao

## Ranged Precision  [Common]
- efeitos: `PerHexRangeDamageBonus:Base:1`
- dur=0 | maxStk=100
- descricao (completa): Every hex between you and your target increases damage dealt by an additional 1%.
- ja no mod: nao

## Ready to Explode!  [Common]
- efeitos: `(vazio)`
- dur=1 | maxStk=1
- descricao (completa): Will explode next turn.
- ja no mod: nao

## Reaper Aura  [Common]
- efeitos: `LifeOnHit:Base:Mathf.Round(8 * (1 + (Target["ShrineEffectBonus"] / 100)))`
- dur=3 | maxStk=100
- descricao (completa): Lifesteal increased by [0]%.
- ja no mod: nao

## Regenerate  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['HolyDamage'] = Source.SpellPower('Light') * .5f`
- dur=3 | maxStk=100
- descricao (completa): Deals *0 holy damage per turn.
- ja no mod: nao

## Regenerate  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['Healing'] = Source.SpellPower('Light') * .5f`
- dur=3 | maxStk=100
- descricao (completa): Restores *0 health per turn.
- ja no mod: nao

## Regenerating  [Common]
- efeitos: `HealthPerTurnPercent:Base:10`
- dur=3 | maxStk=100
- descricao (completa): Gain 10% @Max Health@ regen per turn.
- ja no mod: nao

## Resilient  [Common]
- efeitos: `ResistCold:Base:25, ResistFire:Base:25, ResistLightning:Base:25, ResistPhysical:Base:25, ResistDivine:Base:25`
- dur=3 | maxStk=100
- descricao (completa): All Resistances increased by 25%
- ja no mod: nao

## Resonating Refrain  [Common]
- efeitos: `(vazio)`
- dur=1 | maxStk=1
- descricao (completa): Deals [0] physical damage in a 4 hex area whenever you act.
- ja no mod: nao

## Rhythm of Recovery  [Common]
- efeitos: `HealthPerTurnPercent:Base:5 * Source.GetNumStatuses("BRD_Crescendo_Recovery"), ManaPerTurnPercent:Base:5 * Source.GetNumStatuses("BRD_Crescendo_Recovery")`
- dur=1 | maxStk=1
- descricao (completa): Regain [0]% of Life and Mana each turn.
- ja no mod: nao

## Rogue Aura  [Common]
- efeitos: `DodgeChance:Base:Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100)))`
- dur=3 | maxStk=100
- descricao (completa): Increases dodge chance by [0]%.
- ja no mod: nao

## Ruby of Rancor  [Common]
- efeitos: `ManaCostMod:Set:{-25,-100}`
- dur=VAR | maxStk=VAR
- descricao (completa): 3 extra Action Points granted. Mana Costs reduced by {25,100}%. Die at the end of your turn.
- ja no mod: nao

## Ruby of Rancor  [Mythic]
- efeitos: `(vazio)`
- dur=VAR | maxStk=VAR
- descricao (completa): Grants 1 charge of Ruby of Rancor: Grants 3 extra Action Points and reduces Mana Costs. Die at the end of your turn.  <i><color=#808080>The gem seems to hum in your grasp, as if resonating with your heartbeat, its pulses syncing with your own.</color></i>
- ja no mod: nao

## Ruby Protection  [Common]
- efeitos: `DamageReduction:Base:25`
- dur=2 | maxStk=10
- descricao (completa): Damage taken reduced by 25%.
- ja no mod: nao

## Ruby Rancor  [Common]
- efeitos: `ExtraTurnActionPoints:Set:1`
- dur=2 | maxStk=10
- descricao (completa): Grants an additional Action Point.
- ja no mod: nao

## Rune of Refreshment  [Mythic]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): Reset all cooldowns. Cost 75% of Max Mana. 1 charge per battle.  <i><color=#808080>A tremendous sacrifice is required to power this inert rune.</color></i>
- ja no mod: nao

## Salvation  [Common]
- efeitos: `MaxHealth:Percentage:10`
- dur=3 | maxStk=100
- descricao (completa): @Maximum health@ increased by 10% per stack.
- ja no mod: nao

## Sandstone Plating  [Common]
- efeitos: `DamageReduction:Base:50`
- dur=1 | maxStk=10
- descricao (completa): Damage taken reduced by 50%.
- ja no mod: nao

## Scroll of Monster Summoning  [Legendary]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): Summons a random @level@ {1,30} Monster to fight for you.  <i><color=#808080>"Something on this list has to be useful..."</i></color>
- ja no mod: nao

## Seal of Might  [Common]
- efeitos: `DamageMod:Base:30`
- dur=4 | maxStk=100
- descricao (completa): Damage increased by 30%.
- ja no mod: nao

## Seal of Protection  [Common]
- efeitos: `DamageReduction:Base:10`
- dur=4 | maxStk=100
- descricao (completa): Decreases damage taken by 10%.
- ja no mod: nao

## Seal of Salvation  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['Healing'] = Source.SpellPower() * 1f`
- dur=4 | maxStk=100
- descricao (completa): Restores *0 health per turn.
- ja no mod: nao

## Seraph Aura  [Common]
- efeitos: `HealthPerTurnPercent:Base:Mathf.Round(10 * (1 + (Target["ShrineEffectBonus"] / 100)))`
- dur=3 | maxStk=100
- descricao (completa): Recover [0]% of maximum health each turn.
- ja no mod: nao

## Shadow-Drenched Heart  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): (vazia)
- ja no mod: nao

## Shaman Aura  [Common]
- efeitos: `ManaPerTurnPercent:Base:Mathf.Round(10 * (1 + (Target["ShrineEffectBonus"] / 100)))`
- dur=3 | maxStk=100
- descricao (completa): Recover [0]% of maximum mana each turn.
- ja no mod: nao

## Shapeshift: Black Dragonkin  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Shapeshifted into a Black Dragonkin. Basic attack empowered. Gain new abilities. Armor and Damage Reduction increased.
- ja no mod: nao

## Shapeshift: Blue Dragonkin  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Shapeshifted into a Blue Dragonkin. Basic attack empowered. Gain new abilities. Armor and Cold Resistance increased.
- ja no mod: nao

## Shapeshift: Dire Werewolf  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Shapeshifted into a Dire Werewolf. Basic attack empowered. Gain new abilities. Max Health increased by [0]%.
- ja no mod: nao

## Shapeshift: Green Dragonkin  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Shapeshifted into a Green Dragonkin. Basic attack empowered. Gain new abilities. Armor and Lightning Resistance increased.
- ja no mod: nao

## Shapeshift: Red Dragonkin  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Shapeshifted into a Red Dragonkin. Basic attack empowered. Gain new abilities. Armor and Cold Resistance increased.
- ja no mod: nao

## Shapeshift: Vampire Bat  [Common]
- efeitos: `TurnFreeMovementPoints:Base:4`
- efeitosDano: `Target['FreeMovementPoints'] = Target['FreeMovementPoints'] + 4`
- dur=1 | maxStk=100
- descricao (completa): Shapeshifted into a Vampire Bat. Gain new abilities. @Movement@ increased. Immune to @attacks of opportunity@.
- ja no mod: nao

## Shapeshift: Werewolf  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Shapeshifted into a Werewolf. Basic attack empowered. Gain new abilities. Max Health increased by [0]%.
- ja no mod: nao

## Shapeshift: White Dragonkin  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Shapeshifted into a White Dragonkin. Basic attack empowered. Gain new abilities. Armor and Damage Reduction increased.
- ja no mod: nao

## Sharpened  [Uncommon]
- efeitos: `DamageFlatPhysical:Base:ActionStatus.GetFlatDamageValue`
- dur=0 | maxStk=1
- descricao (completa): Increases @Physical Damage@ by GetFlatDamageValue().
- ja no mod: nao

## Shield Flask  [Common]
- efeitos: `Armor:Base:400`
- dur=5 | maxStk=100
- descricao (completa): Armor increased by 400.
- ja no mod: nao

## Shield of Light  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Shielded from [0] damage.
- ja no mod: nao

## Shield of Retribution  [Common]
- efeitos: `ShieldOfRetribution:Base:Source.SpellPower("Light") * 3f * Source.DamageModHealing`
- dur=3 | maxStk=100
- descricao (completa): Shielded from [0] damage.
- ja no mod: nao

## Shield of the Guardian  [Rare]
- efeitos: `ResistPhysical:Base:{4,12}, ResistCold:Base:{4,12}, ResistFire:Base:{4,12}, ResistLightning:Base:{4,12}, ResistDivine:Base:{4,12}`
- dur=0 | maxStk=1
- descricao (completa): Increases all @Resistances@ by {4,12}%  <i><color=#808080>"To protect what is most important. Both heart and home."</i></color>
- ja no mod: nao

## Silver Signet  [Legendary]
- efeitos: `AdditionalWeaponDamage:Base:Source["Armor"] * {.01f, .01f}, Armor:Base:{8, 200}`
- dur=0 | maxStk=1
- descricao (completa): Grants {8,200} Armor. 1% of your Armor is added as Additional Weapon Damage.  <i><color=#808080>"Be both the storm and the mountain, in war's tumultuous dance, Blend the fury of offense, with defense's steadfast stance."</i></color>
- ja no mod: nao

## Slightly Petrified  [Uncommon]
- efeitos: `TurnFreeMovementPoints:Base:{-1, -1}, Armor:Base:{8,200}`
- dur=0 | maxStk=1
- descricao (completa): @Armor@ increased by {8,200}. @Movement@ reduced by @1@.
- ja no mod: nao

## Smoke Bomb  [Common]
- efeitos: `DodgeChance:Base:50`
- dur=1 | maxStk=100
- descricao (completa): @Dodge chance@ increased by 50%.
- ja no mod: nao

## Smoke Cloud  [Common]
- efeitos: `DodgeChance:Base:50`
- dur=1 | maxStk=100
- descricao (completa): @Dodge chance@ increased by 50%.
- ja no mod: nao

## Song of Swiftness  [Common]
- efeitos: `DexterityBase:Base:5 * Source.GetNumStatuses("BRD_Crescendo_Swiftness"), ReflexBase:Base:5 * Source.GetNumStatuses("BRD_Crescendo_Swiftness")`
- dur=1 | maxStk=1
- descricao (completa): Dexterity and Reflex increased by [0].
- ja no mod: nao

## Soul Link  [Common]
- efeitos: `SoulLink:Set:1`
- dur=1 | maxStk=1
- descricao (completa): All damage and healing dealt to one target is also dealt to the linked target.
- ja no mod: nao

## Soul of Fire  [Common]
- efeitos: `HealingReceivedBonus:Base:-5`
- dur=VAR | maxStk=VAR
- descricao (completa): Healing received reduced by 5% per stack.
- ja no mod: nao

## Soul of Fire  [Mythic]
- efeitos: `DamageModFire:Base:{6,30}, SoulOfFire:Set:{1, 1}`
- dur=VAR | maxStk=VAR
- descricao (completa): Gain {6,30}% Increased Fire Damage. Your stacks of Heat now reduce Healing Received by 5% per stack.  <i><color=#808080>The burning soul of Lord Infernicus!</color></i>
- ja no mod: nao

## Spectral Binding  [Common]
- efeitos: `Invincible:Set:1`
- dur=10 | maxStk=10
- descricao (completa): Will leave when finished playing with you.
- ja no mod: nao

## Stasis  [Common]
- efeitos: `Rooted:Set:1, Armor:Base:15 * Source.Level, MagicArmor:Base:15 * Source.Level`
- dur=1 | maxStk=100
- descricao (completa): @Armor@ and @Magic Armor@ increased by [0].   Immobilized.
- ja no mod: nao

## Stealth  [Common]
- efeitos: `Hidden:Set:1, UntargetableByEnemies:Set:1`
- dur=VAR | maxStk=VAR
- descricao (completa): Invisible.  Attacking from Stealth has 100% critical hit chance.
- ja no mod: nao

## Stealth  [Common]
- efeitos: `Hidden:Set:1, UntargetableByEnemies:Set:1`
- dur=VAR | maxStk=VAR
- descricao (completa): Invisible. Attacking from Stealth has 100% critical hit chance.
- ja no mod: nao

## Strength  [Common]
- efeitos: `MightBase:Base:{4,20}`
- dur=0 | maxStk=1
- descricao (completa): @Might@ increased by {4,20}.
- ja no mod: nao

## Strength of the Ymir  [Mythic]
- efeitos: `CanDualWieldTwoHanded:Set:1 * (1 + ((StatusLevel - 1) * (0.23))), StrengthOfYmirDamageReduction:Base:Target.IsDualWielding2H ? {50,35} : 0`
- dur=0 | maxStk=1
- descricao (completa): Allows you to wield Two-handed Axes, Swords, and Hammers in one hand. Weapon Damage is lowered by {50,35}% if you choose to do so.  <i><color=#808080>You carry the Might of the Ymir!</color></i>
- ja no mod: nao

## Swan Song  [Common]
- efeitos: `Invincible:Set:1`
- dur=1 | maxStk=100
- descricao (completa): Invincible.
- ja no mod: nao

## Swiftness  [Common]
- efeitos: `TurnFreeMovementPoints:Base:1`
- dur=0 | maxStk=100
- descricao (completa): Movement increased by [0].
- ja no mod: nao

## Sword of the Guardian  [Rare]
- efeitos: `DamageMod:Base:{5, 20}`
- dur=0 | maxStk=1
- descricao (completa): Increases @Damage@ by {5, 20}%.  <i><color=#808080>"To strike down those who would harm. In defense of the defenseless."</i></color>
- ja no mod: nao

## Taste for Blood  [Rare]
- efeitos: `LifeOnHit:Base:{4, 4}`
- dur=0 | maxStk=1
- descricao (completa): Increases @Life Steal@ by 4%.  <i><color=#808080>"Everyone needs to eat."</i></color>
- ja no mod: nao

## Teleporting  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Teleports randomly when struck
- ja no mod: nao

## Tempered Rage  [Common]
- efeitos: `DamageMod:Base:15, Armor:Percentage:15, MagicArmor:Percentage:15, ModelScaleMultiplier:Base:10`
- dur=3 | maxStk=100
- descricao (completa): Increases Damage, Armor, and Magic Armor by 15%.
- ja no mod: nao

## Tenacity of the Forest  [Common]
- efeitos: `VitalityBase:Base:5+(5*0.2*IslandLevel)-(5*0.2)`
- dur=0 | maxStk=100
- descricao (completa): Vitality increased by [0].
- ja no mod: nao

## Test Event Status - Boss Event  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): A key
- ja no mod: nao

## Test Event Status - Critical Success  [Common]
- efeitos: `MightBase:Percentage:-5, DexterityBase:Percentage:-5, IntelligenceBase:Percentage:-5, VitalityBase:Percentage:-5, ReflexBase:Percentage:-5`
- dur=0 | maxStk=100
- descricao (completa): Critical Success
- ja no mod: nao

## Test Event Status - Success  [Common]
- efeitos: `MightBase:Percentage:-5, DexterityBase:Percentage:-5, IntelligenceBase:Percentage:-5, VitalityBase:Percentage:-5, ReflexBase:Percentage:-5`
- dur=0 | maxStk=100
- descricao (completa): Success
- ja no mod: SIM
