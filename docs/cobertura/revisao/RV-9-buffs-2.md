# RV-9 - Buffs: arquivo de trabalho (393 entradas)

Gerado do `status.csv`. **Descricoes COMPLETAS** (ja errei com texto truncado, RV-8c).
`dur` = duracao em turnos e `maxStk` = cap de stacks (campos `Duration`/`MaxStacks` do asset, l.319141/319149);
`VAR` = existem assets HOMONIMOS com valores diferentes - nesse caso confira por ASSET, nao por nome.

> ATENCAO: o nome NAO identifica o status. Assets homonimos tem papeis diferentes.

## Dexterity  [Common]
- efeitos: `DexterityBase:Base:Mathf.Round(1f+(0.2f*IslandLevel))`
- dur=0 | maxStk=100
- descricao (completa): Dexterity increased by [0].
- ja no mod: nao

## Diamond Protection  [Common]
- efeitos: `DamageReduction:Base:25`
- dur=2 | maxStk=10
- descricao (completa): Damage taken reduced by 25%.
- ja no mod: nao

## Dodging Strikes  [Common]
- efeitos: `DodgeChance:Base:8`
- dur=2 | maxStk=100
- descricao (completa): Dodge chance increased by 8%.
- ja no mod: nao

## Dragon Claw Talisman  [Rare]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): Summons a @level@ {1,30} Red Dragon Whelp to fight for you.  <i><color=#808080>"The magically preserved claw of a Dragonling."</i></color>
- ja no mod: nao

## Drop of Shadow  [Mythic]
- efeitos: `DamageModShadow:Base:{10,40}`
- dur=0 | maxStk=1
- descricao (completa): Shadow damage you deal applies @Sludge@. Increase @Shadow Damage@ by {10,40}%.  <i><color=#808080>"It's stickier than you imagined."</color></i>
- ja no mod: nao

## Dwarf Rage!  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): (vazia)
- ja no mod: nao

## Dwarven Aura  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Your attacks have a [0]% chance to stun the target.
- ja no mod: nao

## Dwarven Force Generator  [Rare]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): All Teleport (Relocate, Teleport Self, Teleport Other, Escape) spells deal *0 physical damage on entry within 1 hex and knockback 2 hexes.  <i><color=#808080>Crafted by Durn Spellbeard, widely known for his legendary entrances.</i></color>
- ja no mod: nao

## Ebony Dragon Scale  [Mythic]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): Gain the ability to shapeshift into a Black Dragonkin.  <i><color=#808080>"The scale emanates a palpable aura of malevolence, a taint that seems to claw at the very air around it."</color></i>
- ja no mod: nao

## Elemental Equilibrium  [Mythic]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): Dealing damage with a specific element will grant you a buff that increases all elemental damage. Stacks for each element.  <i><color=#808080>"Who defines sanity, after all? Is it the crowd of sheep who mindlessly follow the whims of their shepherd, their dull lives dictated by rules and norms? Or is it the lone wolf, who, by daring to break free from the pack, is deemed insane?"</color></i>
- ja no mod: nao

## Elemental Equilibrium: Cold  [Common]
- efeitos: `DamageFlatCold:Base:GetFlatDamageValue*3f, DamageFlatFire:Base:GetFlatDamageValue*3f, DamageFlatLightning:Base:GetFlatDamageValue*3f`
- dur=3 | maxStk=100
- descricao (completa): Adds [0] damage to elemental attacks.
- ja no mod: nao

## Elemental Equilibrium: Fire  [Common]
- efeitos: `DamageFlatCold:Base:GetFlatDamageValue*3f, DamageFlatFire:Base:GetFlatDamageValue*3f, DamageFlatLightning:Base:GetFlatDamageValue*3f`
- dur=3 | maxStk=100
- descricao (completa): Adds [0] damage to elemental attacks.
- ja no mod: nao

## Elemental Equilibrium: Lightning  [Common]
- efeitos: `DamageFlatCold:Base:GetFlatDamageValue*3f, DamageFlatFire:Base:GetFlatDamageValue*3f, DamageFlatLightning:Base:GetFlatDamageValue*3f`
- dur=3 | maxStk=100
- descricao (completa): Adds [0] damage to elemental attacks.
- ja no mod: nao

## Elemental Power  [Rare]
- efeitos: `DamageModCold:Base:{5,25}, DamageModFire:Base:{5,25}, DamageModLightning:Base:{5,25}`
- dur=0 | maxStk=1
- descricao (completa): Increases @Elemental Damage@ by {5,25}%.
- ja no mod: nao

## Elemental Protection  [Common]
- efeitos: `ResistCold:Base:15, ResistFire:Base:15, ResistLightning:Base:15`
- dur=VAR | maxStk=VAR
- descricao (completa): @Elemental resistance@ increased by 15%.
- ja no mod: nao

## Elixir of the Scarlet Ox  [Legendary]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): Grants Elixir of the Scarlet Ox: Grants 1 additional Action Point and 3 Movement Points. Applies Exhaustion. 1 charge.  <i><color=#808080>"Bestows upon you wings.  Metaphorically of course."</color></i>
- ja no mod: nao

## Elusive  [Common]
- efeitos: `DodgeChance:Base:25`
- dur=3 | maxStk=100
- descricao (completa): Dodge Chance increased by 25%
- ja no mod: nao

## Emblem of the Iron Fortress  [Mythic]
- efeitos: `DamageReturnedFlatPhysical:Base:Source["Armor"] * {.03f, .03f}, Armor:Base:{10, 250}`
- dur=0 | maxStk=1
- descricao (completa): Grants {10,250} Armor. 3% of your Armor is added as physical damage return.  <i><color=#808080>The Iron Fortress, an indomitable monolith of enduring strength, stood resolute and unyielding for hundreds of years, its towering parapets and impenetrable defenses the silent testament to countless civilizations that had crumbled in their futile attempts to conquer it.</color></i>
- ja no mod: nao

## Emerald Protection  [Common]
- efeitos: `DamageReduction:Base:25`
- dur=2 | maxStk=10
- descricao (completa): Damage taken reduced by 25%.
- ja no mod: nao

## Empowered Blood   [Common]
- efeitos: `DamageMod:Base:50`
- dur=2 | maxStk=100
- descricao (completa): Increases damage dealt by 50%.  Gained from fallen allies.
- ja no mod: nao

## Enchant Cold  [Common]
- efeitos: `(vazio)`
- dur=VAR | maxStk=VAR
- descricao (completa): Skills have a chance to deal [0] additional cold damage.
- ja no mod: nao

## Enchant Cold  [Common]
- efeitos: `(vazio)`
- dur=VAR | maxStk=VAR
- descricao (completa): Skills have a chance to deal *0 additional cold damage.
- ja no mod: nao

## Enchant Fire  [Common]
- efeitos: `(vazio)`
- dur=VAR | maxStk=VAR
- descricao (completa): Skills have a chance to deal [0] additional fire damage.
- ja no mod: nao

## Enchant Fire  [Common]
- efeitos: `(vazio)`
- dur=VAR | maxStk=VAR
- descricao (completa): Skills have a chance to deal *0 additional fire damage.
- ja no mod: nao

## Enchant Holy  [Common]
- efeitos: `(vazio)`
- dur=VAR | maxStk=VAR
- descricao (completa): Skills have a chance to deal [0] additional holy damage.
- ja no mod: nao

## Enchant Holy  [Legendary]
- efeitos: `(vazio)`
- dur=VAR | maxStk=VAR
- descricao (completa): Grants @level@ {1,30} Enchant Holy.  <i><color=#808080>Brandish your weapon in glorious light.</i></color>
- ja no mod: nao

## Enchant Lightning  [Common]
- efeitos: `(vazio)`
- dur=VAR | maxStk=VAR
- descricao (completa): Skills have a chance to deal [0] additional lightning damage.
- ja no mod: nao

## Enchant Lightning  [Common]
- efeitos: `(vazio)`
- efeitosDano: `Target['EnchantLightningMagedrawValue'] = Source.SpellPower('Lightning') * .2f`
- dur=VAR | maxStk=VAR
- descricao (completa): Skills have a chance to deal *0 additional lightning damage.
- ja no mod: nao

## Enchant Shadow  [Common]
- efeitos: `(vazio)`
- dur=VAR | maxStk=VAR
- descricao (completa): Skills have a chance to deal [0] additional shadow damage.
- ja no mod: nao

## Enchant Shadow  [Legendary]
- efeitos: `(vazio)`
- dur=VAR | maxStk=VAR
- descricao (completa): Grants @level@ {1,30} Enchant Shadow.  <i><color=#808080>Wreathe your weapon in darkest shadow.</i></color>
- ja no mod: nao

## Enchanted Pumpkin  [Legendary]
- efeitos: `HealthPerTurn:Base:12 * (1 + ((StatusLevel - 1) * (0.23))), ManaPerTurn:Base:12 * (1 + ((StatusLevel - 1) * (0.23)))`
- dur=0 | maxStk=1
- descricao (completa): Gain [0] Health and Mana each turn.  <i><color=#808080>There is an intoxicating aroma about it. It smells of autumn nights and whispered tales around a fire, of ancient magic and timeless tales.</color></i>
- ja no mod: nao

## Enchanted Whetstone  [Rare]
- efeitos: `WeaponDamageMod:Base:{10, 40}`
- dur=0 | maxStk=1
- descricao (completa): Weapon damage increased by {10,40}%  <i><color=#808080>Captain Henry Irons would be proud!</color></i>
- ja no mod: nao

## Endurance  [Rare]
- efeitos: `MaxHealth:Base:{5, 500}`
- dur=0 | maxStk=1
- descricao (completa): Increases @Max Health@ by {5, 500}.
- ja no mod: nao

## Enduring Evasion  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Dodging incoming attacks.
- ja no mod: nao

## Energy Aura  [Common]
- efeitos: `ManaCostMod:Base:Mathf.Round(-50 * (1 + (Target["ShrineEffectBonus"] / 100)))`
- dur=3 | maxStk=100
- descricao (completa): Decreases the cost of mana using abilities by [0]%.
- ja no mod: nao

## Enraged  [Common]
- efeitos: `ImmunityMovementImpairing:Set:1, ImmunityChilledEffect:Set:1, ImmunityDisabled:Set:1, ImmunityFrozen:Set:1, ImmunityKnockback:Set:1, ImmunitySlow:Set:1, ImmunityStunned:Set:1`
- dur=2 | maxStk=100
- descricao (completa): Immune to all movement impairing effects and knockback.
- ja no mod: nao

## Ethereal  [Rare]
- efeitos: `ResistPhysical:Base:{10,50}, ResistCold:Base:{-5,-25}, ResistFire:Base:{-5,-25}, ResistLightning:Base:{-5,-25}`
- dur=0 | maxStk=1
- descricao (completa): Increases @Physical Resistance@ by {10,50}%. Reduces @Elemental Resistance@ by {5,25}%.
- ja no mod: nao

## Evasion  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Dodging incoming attacks.
- ja no mod: nao

## Evasive Movement  [Common]
- efeitos: `OpportunityAttackImmunity:Set:1`
- dur=0 | maxStk=100
- descricao (completa): Grants immunity to opportunity attacks.
- ja no mod: nao

## Everlasting Sacrifice  [Mythic]
- efeitos: `DamageModHealing:Base:{50,100}`
- dur=0 | maxStk=1
- descricao (completa): @Holy Power@ increased by {50,100}%. Take 20% of your Max Health in Holy Damage each turn.
- ja no mod: nao

## Evolution  [Common]
- efeitos: `DamageMod:Base:5`
- dur=1 | maxStk=10
- descricao (completa): Damage increased by 5% per stack.  Can stack up to 10 times.
- ja no mod: nao

## Evolution  [Common]
- efeitos: `MaxHealth:Percentage:5`
- dur=1 | maxStk=10
- descricao (completa): Max Health increased by 5% per stack.  Can stack up to 10 times.
- ja no mod: nao

## Explosive  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Explodes on death
- ja no mod: nao

## Eye Drops  [Common]
- efeitos: `ImmunityBlind:Set:1`
- dur=2 | maxStk=100
- descricao (completa): Immune to Bleeding.
- ja no mod: nao

## Fate  [Common]
- efeitos: `MightBase:Base:10000, VitalityBase:Base:100, IntelligenceBase:Base:100, ImmunityDisabled:Set:1, ImmunityRooted:Set:1, Armor:Base:0, MagicArmor:Base:0, Recovery:Base:0, SummonDamageMod:Base:500, SummonHealthMod:Base:500, ImmunityPoisoned:Set:1, ImmunityBleeding:Set:1, DarkRitual:Set:1`
- dur=2 | maxStk=100
- descricao (completa): Potential realized.
- ja no mod: nao

## Fever  [Common]
- efeitos: `Fever:Set:1`
- dur=1 | maxStk=100
- descricao (completa): Mana costs now take from health instead.
- ja no mod: nao

## Fire Shield  [Common]
- efeitos: `ResistFire:Base:10`
- dur=3 | maxStk=100
- descricao (completa): @Fire resistance@ increased by 10%.   Attackers take *0 fire damage.
- ja no mod: nao

## Fire Thorns  [Common]
- efeitos: `DamageReturnedFlatFire:Base:{1,300}`
- dur=3 | maxStk=1
- descricao (completa): Reflects [0] fire damage back to attackers.
- ja no mod: nao

## Fizzled  [Common]
- efeitos: `(vazio)`
- dur=1 | maxStk=100
- descricao (completa): Fizzled.
- ja no mod: nao

## Flame Shrine Aura  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Attackers take Fire Damage.
- ja no mod: nao

## Forbidden Power  [Common]
- efeitos: `ManaCostMod:Base:50, ManaPowerMod:Base:50`
- dur=0 | maxStk=100
- descricao (completa): All mana costs increased by 50%. Power of mana costing abilities increased by 50%.
- ja no mod: nao

## Fortified Flask  [Common]
- efeitos: `Armor:Base:200`
- dur=5 | maxStk=100
- descricao (completa): Armor increased by 200.
- ja no mod: nao

## Fortitude  [Uncommon]
- efeitos: `VitalityBase:Base:{4,20}`
- dur=0 | maxStk=1
- descricao (completa): @Vitality@ increased by {4,20}.
- ja no mod: nao

## Freezing  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Freezes all enemies on death
- ja no mod: nao

## Frenzy  [Common]
- efeitos: `(vazio)`
- dur=1 | maxStk=100
- descricao (completa): Action Points Increase by 1.
- ja no mod: nao

## Frost Armor  [Common]
- efeitos: `ResistCold:Base:10`
- dur=3 | maxStk=100
- descricao (completa): @Cold resistance@ increased by 10%.  Attackers take *0 cold damage.
- ja no mod: nao

## Frost Thorns  [Common]
- efeitos: `DamageReturnedFlatCold:Base:{1,300}`
- dur=3 | maxStk=1
- descricao (completa): Reflects [0] cold damage back to attackers.
- ja no mod: nao

## Frozen Lich Heart  [Mythic]
- efeitos: `DamageModColdToFrozen:Base:{100, 200}, ImmunityChilled:Set:1 * (1 + ((StatusLevel - 1) * (0.23)))`
- dur=0 | maxStk=1
- descricao (completa): Your cold damage is increased by [0]% against targets that are frozen. Grants immunity to chilled.  <i><color=#808080>The Frozen Heart of the Lich, pulsating with a masterful power of ice and the chill of a thousand winters, imbued its holder with a profound affinity for the cold, such that even in the harshest blizzards they would find a comfortable sanctuary.</color></i>
- ja no mod: nao

## Fury  [Common]
- efeitos: `DamageMod:Base:Mathf.Round(25 * (1 + (Target["ShrineEffectBonus"] / 100))), DamageReduction:Base:Mathf.Round(-25 * (1 + (Target["ShrineEffectBonus"] / 100)))`
- dur=3 | maxStk=100
- descricao (completa): Damage increased by [0]%. Damage taken increased by [0]%.
- ja no mod: nao

## Ghost Armor  [Common]
- efeitos: `(vazio)`
- dur=2 | maxStk=1
- descricao (completa): Absorbs the next attack.
- ja no mod: nao

## Giant  [Common]
- efeitos: `DamageMod:Base:25, MaxHealth:Percentage:25, ModelScaleMultiplier:Base:25`
- dur=3 | maxStk=100
- descricao (completa): Damage and Health increased by 25% Size increased by 25%
- ja no mod: nao

## Gift to the Conquered  [Rare]
- efeitos: `MightBase:Base:{3,15}, DexterityBase:Base:{3,15}, IntelligenceBase:Base:{3,15}, VitalityBase:Base:{3,15}, ReflexBase:Base:{3,15}`
- dur=0 | maxStk=1
- descricao (completa): @All Stats@ increased by {3,15}.  <i><color=#808080>"To kneel is not to surrender, but to acknowledge a power greater than oneself."</i></color>
- ja no mod: nao

## Glory  [Common]
- efeitos: `Invincible:Set:1`
- dur=1 | maxStk=100
- descricao (completa): Immune to damage.
- ja no mod: nao

## Glory of the Conqueror  [Rare]
- efeitos: `CritChance:Base:{4,12}`
- dur=0 | maxStk=1
- descricao (completa): @Critical Hit Chance@ increased by {4,12}%.   <i><color=#808080>"The path to glory does not lie in submission. It begins with defiance."</i></color>
- ja no mod: nao

## Grace of the Rogue  [Rare]
- efeitos: `ReflexBase:Base:{5,25}`
- dur=0 | maxStk=1
- descricao (completa): @Reflex@ increased by {5,25}.  <i><color=#808080>"No matter the odds, there is always a way, always a chance, if only one has the will to seize it."</i></color>
- ja no mod: nao

## Greater Heal  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['Healing'] = Target['MaxHealth']`
- dur=0 | maxStk=100
- descricao (completa): Healed.
- ja no mod: nao
