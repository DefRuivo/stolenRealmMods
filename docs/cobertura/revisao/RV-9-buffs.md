# RV-9 - Buffs: arquivo de trabalho (393 entradas)

Gerado do `status.csv`. **Descricoes COMPLETAS** (ja errei com texto truncado, RV-8c).
`dur` = duracao em turnos e `maxStk` = cap de stacks (campos `Duration`/`MaxStacks` do asset, l.319141/319149);
`VAR` = existem assets HOMONIMOS com valores diferentes - nesse caso confira por ASSET, nao por nome.

> ATENCAO: o nome NAO identifica o status. Assets homonimos tem papeis diferentes.

---

## Affinity: Cold  [Common]
- efeitos: `DamageModCold:Base:2`
- dur=1 | maxStk=1000
- descricao (completa): Increases @Cold Damage@ dealt by [0]%.
- ja no mod: nao

## Affinity: Fire  [Common]
- efeitos: `DamageModFire:Base:2`
- dur=1 | maxStk=1000
- descricao (completa): Increases @Fire Damage@ dealt by [0]%.
- ja no mod: nao

## Affinity: Holy  [Common]
- efeitos: `DamageModHealing:Base:2`
- dur=1 | maxStk=1000
- descricao (completa): Increases @Holy Damage@ and @Healing@ dealt by [0]%.
- ja no mod: nao

## Affinity: Lightning  [Common]
- efeitos: `DamageModLightning:Base:2`
- dur=1 | maxStk=1000
- descricao (completa): Increases @Lightning Damage@ dealt by [0]%.
- ja no mod: nao

## Affinity: Physical  [Common]
- efeitos: `DamageModPhysical:Base:2`
- dur=1 | maxStk=1000
- descricao (completa): Increases @Physical Damage@ dealt by [0]%.
- ja no mod: nao

## Affinity: Shadow  [Common]
- efeitos: `DamageModShadow:Base:2`
- dur=1 | maxStk=1000
- descricao (completa): Increases @Shadow Damage@ dealt by [0]%.
- ja no mod: nao

## Ancestral Protection  [Legendary]
- efeitos: `Armor:Base:{20,300}, MagicArmor:Base:{20,300}`
- dur=0 | maxStk=1
- descricao (completa): Grants a 10% chance to cast @Level@ {1,30} Avenging Ancestors on an enemy that strikes you. Grants {20,300} Armor and Magic Armor.  <i><color=#808080>"You do not walk this world alone. With every step you take, you tread upon the footprints of your ancestors. They have blazed the trail before you, weathering storms you cannot fathom, crossing paths you cannot see."</i></color>
- ja no mod: nao

## Angered  [Common]
- efeitos: `DamageReduction:Base:-15, DamageMod:Base:25, MaxHealth:Percentage:15, ModelScaleMultiplier:Base:15`
- dur=3 | maxStk=100
- descricao (completa): Increases damage dealt by 25%. Increases max life and damage taken by 15%.
- ja no mod: nao

## Anthulk Carapace  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=1
- descricao (completa): 50% chance to cast Anthulk Spines when struck.
- ja no mod: nao

## Antidote  [Common]
- efeitos: `ImmunityPoisoned:Set:1`
- dur=2 | maxStk=100
- descricao (completa): Immune to poisoned.
- ja no mod: nao

## Ascendancy  [Common]
- efeitos: `MightBase:Percentage:20, DexterityBase:Percentage:20, VitalityBase:Percentage:20, IntelligenceBase:Percentage:20, ReflexBase:Percentage:20`
- dur=5 | maxStk=100
- descricao (completa): Increases target ally's stats by 20%.  Lasts 5 turns.
- ja no mod: nao

## Aura Of Frost  [Common]
- efeitos: `(vazio)`
- dur=2 | maxStk=100
- descricao (completa): Deals *0 cold damage per turn while in the aura.
- ja no mod: SIM

## Avenging Ancestors  [Legendary]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): Grants a 10% chance to cast @Level@ {1,30} Avenging Ancestors on an enemy that strikes you.
- ja no mod: nao

## Ball Lightning  [Mythic]
- efeitos: `BallLightningAmount:Base:ActionStatus.GetFlatDamageValue * 15 * Target.DamageModLightning`
- dur=0 | maxStk=1
- descricao (completa): Dealing lightning damage grants a stack of Overcharge: Each stack adds <color=#CBB396>[0]</color> lightning damage to your next basic attack.  <i><color=#808080>In fury, the sky roars, a tempest untamed, Lightning cracks, an ephemeral fire, wild and unchained.</color></i>
- ja no mod: nao

## Battle Fury  [Common]
- efeitos: `DamageMod:Base:30, ModelScaleMultiplier:Base:10`
- dur=3 | maxStk=1
- descricao (completa): Increases damage dealt by 30%.
- ja no mod: nao

## Berserking  [Common]
- efeitos: `DamageMod:Base:Source.HealthRatioInverse * 100, MaxHealth:Percentage:25`
- dur=3 | maxStk=100
- descricao (completa): Maximum health increased by 25% Deals more damage at lower health
- ja no mod: nao

## Bless  [Common]
- efeitos: `MaxHealth:Percentage:10, MaxMana:Percentage:10, DamageMod:Base:10`
- dur=3 | maxStk=100
- descricao (completa): @Maximum health@ and @maximum mana@ increased by 10%.  @Damage dealt@ increased by 10%.
- ja no mod: nao

## Blessing of the Mountain  [Common]
- efeitos: `(vazio)`
- dur=VAR | maxStk=VAR
- descricao (completa): Taking damage grants a stack of Thunder Charged.
- ja no mod: nao

## Blessing of the Mountain  [Mythic]
- efeitos: `StatusResistImpairment:Base:{50, 50}, MaxHealth:Percentage:{15,30}`
- dur=VAR | maxStk=VAR
- descricao (completa): Grants a 50% chance to resist any control effects.  Increases @Max Health@ by {15,30}%.  <i><color=#808080>Enough is enough!</i></color>
- ja no mod: nao

## Blessing of the Seraph  [Common]
- efeitos: `Recovery:Base:10`
- dur=VAR | maxStk=VAR
- descricao (completa): Recover 5% Max Health and Mana per turn.
- ja no mod: nao

## Blessing of the Seraph  [Rare]
- efeitos: `HealthPerTurn:Base:12 * (1 + ((StatusLevel - 1) * (0.23)))`
- dur=VAR | maxStk=VAR
- descricao (completa): @Health Recovery@ increased by [0].  <i><color=#808080>"In this realm of wild and woe, No good springs forth unless you sow."</i></color>
- ja no mod: nao

## Blood Frenzy  [Common]
- efeitos: `DamageMod:Base:25, LifeSteal:Base:25, ModelScaleMultiplier:Base:10`
- dur=2 | maxStk=1
- descricao (completa): Increases damage dealt and life steal by 25%.
- ja no mod: nao

## Blood Link  [Common]
- efeitos: `SoulLink:Set:1`
- dur=1 | maxStk=1
- descricao (completa): The Council's health pool is shared.
- ja no mod: nao

## Bloodied Bargain  [Mythic]
- efeitos: `DamageModPhysical:Base:{8,40}`
- dur=0 | maxStk=1
- descricao (completa): Increases @Physical Damage@ by {8,40}%. Physical damage you deal applies 1 stack of @Bleeding@.  <i><color=#808080>A price in blood must be paid, just be sure you're not the one to pay it.</color></i>
- ja no mod: nao

## Boar Charm  [Rare]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): Allows you to summon a @level@ {1,30} Wild Boar to fight for you.  <i><color=#808080>The boar you rescued follows you.</i></color>
- ja no mod: nao

## Bolstering Ballad  [Common]
- efeitos: `VitalityBase:Base:5 * Source.GetNumStatuses("BRD_Crescendo_Ballad"), Armor:Base:5 * Source.GetNumStatuses("BRD_Crescendo_Ballad"), MagicArmor:Base:5 * Source.GetNumStatuses("BRD_Crescendo_Ballad")`
- dur=1 | maxStk=1
- descricao (completa): Vitality, Armor and Magic Armor increased by [0].
- ja no mod: nao

## Bone Collector  [Common]
- efeitos: `MaxHealth:Percentage:6, DamageMod:Base:6`
- dur=1 | maxStk=100
- descricao (completa): @Maximum health@ and @Damage Dealt@ increased by 6% per stack.
- ja no mod: nao

## Bottled Anger  [Common]
- efeitos: `DamageMod:Base:20, DamageReduction:Base:-10`
- dur=5 | maxStk=100
- descricao (completa): Damage increased by 20%. Damage taken increased by 10%.
- ja no mod: nao

## Bottled Fury  [Common]
- efeitos: `DamageMod:Base:40, DamageReduction:Base:-20`
- dur=5 | maxStk=100
- descricao (completa): Damage increased by 40%. Damage taken increased by 20%.
- ja no mod: nao

## Bottled Irritation  [Common]
- efeitos: `DamageMod:Base:10, DamageReduction:Base:-5`
- dur=5 | maxStk=100
- descricao (completa): Damage increased by 10%. Damage taken increased by 5%.
- ja no mod: nao

## Bottled Rage  [Common]
- efeitos: `DamageMod:Base:30, DamageReduction:Base:-15`
- dur=5 | maxStk=100
- descricao (completa): Damage increased by 30%. Damage taken increased by 15%.
- ja no mod: nao

## Bottled Wrath  [Common]
- efeitos: `DamageMod:Base:50, DamageReduction:Base:-25`
- dur=5 | maxStk=100
- descricao (completa): Damage increased by 50%. Damage taken increased by 25%.
- ja no mod: nao

## Break The Ice  [Common]
- efeitos: `DamageMod:Base:100`
- dur=3 | maxStk=100
- descricao (completa): Your first attack in battle deals 100% additional damage.
- ja no mod: nao

## Brilliance  [Uncommon]
- efeitos: `IntelligenceBase:Base:{4,20}`
- dur=0 | maxStk=1
- descricao (completa): @Intelligence@ increased by {4,20}.
- ja no mod: nao

## Bristlethorn Vines  [Common]
- efeitos: `TurnFreeMovementPoints:Base:-1, DamageReturnedFlatPhysical:Base:3 * IslandLevel`
- dur=0 | maxStk=100
- descricao (completa): Movement reduced by 1. Physical return damage increased by [1].
- ja no mod: nao

## Burning Demon Hearts  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): (vazia)
- ja no mod: nao

## Call of the Reaper  [Rare]
- efeitos: `DamageMod:Base:{6,30}, DamageReduction:Base:{-10, -10}`
- dur=0 | maxStk=1
- descricao (completa): Increases @Damage@ by {6,30}%. Increases @Damage Taken@ by 10%.  <i><color=#808080>"Judge not a life until its final breath, for the Reaper's touch brings truth to death."</i></color>
- ja no mod: nao

## Caution  [Common]
- efeitos: `DodgeChance:Base:5`
- dur=0 | maxStk=100
- descricao (completa): Dodge Chance increased by  [0]%.
- ja no mod: nao

## Celerity  [Uncommon]
- efeitos: `DexterityBase:Base:{4,20}`
- dur=0 | maxStk=1
- descricao (completa): @Dexterity@ increased by {4,20}.
- ja no mod: nao

## Champion of Blood  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=1
- descricao (completa): Striking enemies heals the Countess for 10% of her Max Health
- ja no mod: nao

## Chaos Coin  [Mythic]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): <i><color=#808080>Will you flip the Coin of Chaos?</i></color>   Grants the skill @Coin Flip@
- ja no mod: nao

## Chromatic Tonic  [Common]
- efeitos: `MagicArmor:Base:400`
- dur=5 | maxStk=100
- descricao (completa): Magic armor increased by 400.
- ja no mod: nao

## Claw of the Anthulk  [Mythic]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): Your weapon attacks apply level {1,30} Anthulk Venom: Increases the Physical Damage the target takes by GetFlatDamageDealt(.5, Physical) per stack.  <i><color=#808080>"The venomous claw of a mature Anthulk."</i></color>
- ja no mod: nao

## Combo Breaker  [Common]
- efeitos: `ManaPowerMod:Base:10`
- dur=1 | maxStk=100
- descricao (completa): Damage and healing from non basic skills increased by 10%.
- ja no mod: nao

## Conqueror Aura  [Common]
- efeitos: `CritChance:Base:Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100)))`
- dur=3 | maxStk=100
- descricao (completa): Critical hit chance increased by [0]%.
- ja no mod: nao

## Control Resistance  [Common]
- efeitos: `StatusResistImpairment:Base:43 + (Source.NumPartyCharacters * 7)`
- dur=2 | maxStk=100
- descricao (completa): Has a [0]% chance to resist any control effects.
- ja no mod: nao

## Counter Melody  [Common]
- efeitos: `ImmunityMovementImpairing:Set:1, ImmunityChilledEffect:Set:1, ImmunityDisabled:Set:1, ImmunityFrozen:Set:1, ImmunityKnockback:Set:1, ImmunitySlow:Set:1, ImmunityStunned:Set:1`
- dur=1 | maxStk=100
- descricao (completa): Immune to Crowd Control effects.
- ja no mod: nao

## Courage of the Ymir  [Mythic]
- efeitos: `ExtraTurnActionPoints:Base:(Source.HasWeaponType("Sword_1H")`
- dur=0 | maxStk=1
- descricao (completa): Increases your @Action Points@ by @1@. If you are using a One-Handed Sword, Axe, Hammer, Gun, or Wand.  <i><color=#808080>You carry the Speed of the Ymir!</color></i>
- ja no mod: nao

## Crash and Flow  [Common]
- efeitos: `DamageMod:Base:10`
- dur=1 | maxStk=5
- descricao (completa): Damage and healing increased by 10%.  Caused by recently dodging.
- ja no mod: nao

## Crescendo of Ballad  [Common]
- efeitos: `(vazio)`
- dur=1 | maxStk=999999
- descricao (completa): Crescendo of Bolstering Ballad. Each stack increases the power of the song.
- ja no mod: nao

## Crescendo of Recovery  [Common]
- efeitos: `(vazio)`
- dur=1 | maxStk=999999
- descricao (completa): Crescendo of Rhythm of Recovery. Each stack increases the power of the song.
- ja no mod: nao

## Crescendo of Refrain  [Common]
- efeitos: `(vazio)`
- dur=1 | maxStk=999999
- descricao (completa): Crescendo of Resonating Refrain. Each stack increases the power of the song.
- ja no mod: nao

## Crescendo of Swiftness  [Common]
- efeitos: `(vazio)`
- dur=1 | maxStk=999999
- descricao (completa): Crescendo of Song of Swiftness. Each stack increases the power of the song.
- ja no mod: nao

## Crescendo of Valor  [Common]
- efeitos: `(vazio)`
- dur=1 | maxStk=999999
- descricao (completa): Crescendo of Verse of Valor. Each stack increases the power of the song.
- ja no mod: nao

## Crystal Ball  [Rare]
- efeitos: `PerHexRangeDamageBonus:Base:{.5,1.5}, RangeTypeAdderRanged:Base:{1,3}`
- dur=0 | maxStk=1
- descricao (completa): Gain {.5,1.5}% bonus damage for every hex between you and your target. Skill range increased by {1,3}.  <i><color=#808080>It doesn't show the future but a clearer picture of the present.</color></i>
- ja no mod: nao

## Curse of the Reaper  [Rare]
- efeitos: `LifeOnHit:Base:{6,6}, MaxHealth:Percentage:{-15, -15}`
- dur=0 | maxStk=1
- descricao (completa): Increases @Life Steal@ by 6%. Reduces @Max Life@ by 15%.  <i><color=#808080>"A thirst so deep, it blurs the lines, Til we're but marionettes of our own designs."</i></color>
- ja no mod: nao

## Cursed Coin  [Common]
- efeitos: `DarkRitual:Set:1`
- dur=VAR | maxStk=VAR
- descricao (completa): Health cannot drop below 1.
- ja no mod: nao

## Cursed Coin  [Legendary]
- efeitos: `(vazio)`
- dur=VAR | maxStk=VAR
- descricao (completa): The first time your health is brought below @1@ instead receive @Cursed Coin@: Health cannot drop below 1. Lasts 2 turns. Applies Ritual Sickness. 1 charge per Quest.  <i><color=#808080>"Cursed life is still life."</color></i>
- ja no mod: nao

## Dark Clones  [Common]
- efeitos: `Invincible:Set:1`
- dur=2 | maxStk=10
- descricao (completa): Invulnerable while Dark Clones are alive.
- ja no mod: nao

## Dark Discoveries  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): Locate and destroy the runaway experiments.
- ja no mod: nao

## Dark Ritual  [Common]
- efeitos: `DarkRitual:Set:1`
- dur=1 | maxStk=1
- descricao (completa): Health cannot drop below 1.
- ja no mod: nao

## Deal with a Devil  [Common]
- efeitos: `GoldMod:Base:50, DropQuantityMod:Base:50, ExperienceMod:Base:50`
- dur=0 | maxStk=100
- descricao (completa): <i><color=#808080>You've made a deal with a devil!</i></color>   Increases experience, item drops, and gold gained by 50%.
- ja no mod: nao

## Decay Shrine Aura  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Take [0]% of your Max Health in Shadow Damage per turn.
- ja no mod: nao

## Defense Flask  [Common]
- efeitos: `Armor:Base:50`
- dur=5 | maxStk=100
- descricao (completa): Armor increased by 50.
- ja no mod: nao

## Destructive  [Common]
- efeitos: `DamageMod:Base:50`
- dur=3 | maxStk=100
- descricao (completa): Damage increased by 50%
- ja no mod: nao

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

## Growing Hatred  [Common]
- efeitos: `ExtraTurnActionPoints:Base:1, ModelScaleMultiplier:Base:25`
- dur=20 | maxStk=2
- descricao (completa): Grants 1 additional Action Point. Increases Damage Taken by 25%.
- ja no mod: nao

## Guardian Aura  [Common]
- efeitos: `DamageReduction:Base:Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100)))`
- dur=3 | maxStk=100
- descricao (completa): Reduces Damage taken by [0]%.
- ja no mod: nao

## Guardian Flask  [Common]
- efeitos: `Armor:Base:800`
- dur=5 | maxStk=100
- descricao (completa): Armor increased by 800.
- ja no mod: nao

## Guardian Shield  [Common]
- efeitos: `DamageReduction:Base:50`
- dur=1 | maxStk=100
- descricao (completa): Damage taken decreased by 50%.
- ja no mod: nao

## Guile of the Rogue  [Rare]
- efeitos: `DexterityBase:Base:{5,25}`
- dur=0 | maxStk=1
- descricao (completa): @Dexterity@ increased by {5,25}.  <i><color=#808080>"Justice is not always a path of righteousness walked in the light. Sometimes, it is a road shrouded in darkness, a route navigated by the quiet flicker of rebellion."</i></color>
- ja no mod: nao

## Harmonize  [Common]
- efeitos: `(vazio)`
- dur=1 | maxStk=100
- descricao (completa): Your actions spread Harmony to nearby allies.
- ja no mod: nao

## Harmony  [Common]
- efeitos: `DexterityBase:Base:1`
- dur=2 | maxStk=1000
- descricao (completa): Harmony: +1 Dexterity per stack.
- ja no mod: nao

## Harmony  [Common]
- efeitos: `IntelligenceBase:Base:1`
- dur=2 | maxStk=1000
- descricao (completa): Harmony: +1 Intelligence per stack.
- ja no mod: nao

## Harmony  [Common]
- efeitos: `MightBase:Base:1`
- dur=2 | maxStk=1000
- descricao (completa): Harmony: +1 Might per stack.
- ja no mod: nao

## Harmony  [Common]
- efeitos: `ReflexBase:Base:1`
- dur=2 | maxStk=1000
- descricao (completa): Harmony: +1 Reflex per stack.
- ja no mod: nao

## Harmony  [Common]
- efeitos: `VitalityBase:Base:1`
- dur=2 | maxStk=1000
- descricao (completa): Harmony: +1 Vitality per stack.
- ja no mod: nao

## Heal  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['Healing'] = Source.SpellPower('Light') * 1.0f`
- dur=0 | maxStk=100
- descricao (completa): Healed.
- ja no mod: nao

## Holy Ground  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['Healing'] = Target.TeamIndex == 1 ? Target.FodderHealthAtLevel * .3f : Source.SpellPower('Light') * 1f`
- dur=3 | maxStk=100
- descricao (completa): Targets in holy ground receive healing.
- ja no mod: nao

## Holy Ground  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['Healing'] = Source.SpellPower() * .75f`
- dur=3 | maxStk=100
- descricao (completa): Targets in holy ground are healed *0 per turn.
- ja no mod: nao

## Holy Ground  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['HolyDamage'] = Source.SpellPower() * .75f`
- dur=3 | maxStk=100
- descricao (completa): Taking *0 Holy Damage per turn while in Holy Ground.
- ja no mod: nao

## Honor of the Ymir  [Mythic]
- efeitos: `PerHexRangeDamageBonus:Base:Source.HasWeaponType("Staff")`
- dur=0 | maxStk=1
- descricao (completa): Every hex between you and your target increases damage dealt by an additional @12%@ when wielding a Staff, Bow, or Two Handed Gun.  <i><color=#808080>You carry the Speed of the Ymir!</color></i>
- ja no mod: nao

## Horn of Devotion  [Legendary]
- efeitos: `ShrineEffectBonus:Base:{50,100}`
- dur=0 | maxStk=1
- descricao (completa): Increases the effect of Shrines by {50,100}%.  <i><color=#808080>"Given to great warriors to aid them in battle."</i></color>
- ja no mod: nao

> **Nota RV-24 (30/09/2026) — a cadeia do `ShrineEffectBonus`:** este é o item e, ao lado dele, os
> tiers de `Omnism` (`I` = **8**, `II` = **20**), que são as fontes do bônus. Os tiers **NÃO somam**
> (8 + 20 = 28 está **errado**): a `Omnism II` **substitui** a `Omnism I` (`SkillsThatReplace`), o
> total é **20** — teste do próprio jogo, `20f` (decompilado l.183505) — e o "an additional 12%" do
> texto é só a diferença 8 → 20. Fonte corrigida, aura por aura: `docs/cobertura/revisao/RV-19-shrines.md`.
> (Nota acrescentada: o relatório em si é registro histórico e não foi reescrito.)

## Hunger  [Common]
- efeitos: `ManaOnHit:Base:10`
- efeitosDano: `TargetStored['ShadowDamage'] = Target.MaxHealth * .1f`
- dur=3 | maxStk=1
- descricao (completa): Grants 10% @mana steal@.  Sacrifices 10% maximum health per turn.
- ja no mod: nao

## Hunger for Vengeance  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): (vazia)
- ja no mod: nao

## Hunger of Ksvaldir  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['ShadowDamage'] = Target.MaxHealth * .1f`
- dur=3 | maxStk=1
- descricao (completa): Sacrifices 10% maximum health per turn.
- ja no mod: nao

## Ice Crystal  [Mythic]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): <i><color=#808080>The magic crystal emanates cold.</color></i>  Allows you to summon a @level@ {1,30} Ice Golem to fight for you. Benefits from your @Cold Damage@.
- ja no mod: nao

## Immunity  [Common]
- efeitos: `Invincible:Set:1, ImmunityMovementImpairing:Set:1, ImmunityDisabled:Set:1, ImmunitySlow:Set:1`
- dur=10 | maxStk=10
- descricao (completa): Can only be harmed by destroying Soul Fetishes.  Immune to movement imparing effects.
- ja no mod: nao

## Improvise  [Common]
- efeitos: `(vazio)`
- dur=1 | maxStk=100
- descricao (completa): Songs no longer clear each other's Crescendo.
- ja no mod: nao

## Incalculable Rage  [Common]
- efeitos: `ExtraTurnActionPoints:Base:1, TurnFreeMovementPoints:Base:-6, ModelScaleMultiplier:Base:20`
- dur=3 | maxStk=1
- descricao (completa): Grants 1 additional Action Points. Lowers movement points by 6.
- ja no mod: nao

## Increased Armor  [Common]
- efeitos: `Armor:Base:5 * Source.Level, MagicArmor:Base:5 * Source.Level`
- dur=2 | maxStk=100
- descricao (completa): @Armor@ and @Magic Armor@ increased by [0].
- ja no mod: nao

## Increased Damage and Healing by 10%  [Common]
- efeitos: `DamageMod:Base:10`
- dur=2 | maxStk=100
- descricao (completa): Increases Damage and Healing by 10%.
- ja no mod: nao

## Increased Damage and Healing by 100%  [Common]
- efeitos: `DamageMod:Base:100`
- dur=2 | maxStk=100
- descricao (completa): Increases Damage and Healing by 100%.
- ja no mod: nao

## Increased Damage and Healing by 1000%  [Common]
- efeitos: `DamageMod:Base:1000`
- dur=5 | maxStk=100
- descricao (completa): Increases Damage and Healing by 1000%.
- ja no mod: nao

## Increased Damage and Healing by 25%  [Common]
- efeitos: `DamageMod:Base:25`
- dur=2 | maxStk=100
- descricao (completa): Increases Damage and Healing by 25%.
- ja no mod: nao

## Indestructible  [Common]
- efeitos: `Armor:Percentage:10, MagicArmor:Percentage:10, DamageReturnedMod:Base:10`
- dur=1 | maxStk=10
- descricao (completa): @Armor@, @Magic Armor@, and @Return Damage@ increased by 10% per stack.
- ja no mod: nao

## Inner Warmth  [Common]
- efeitos: `ImmunityFrozen:Set:1`
- dur=1 | maxStk=100
- descricao (completa): Cannot be frozen.  Caused by being recently frozen.
- ja no mod: nao

## Inspiration  [Common]
- efeitos: `ResistPhysical:Base:1, ResistCold:Base:1, ResistFire:Base:1, ResistLightning:Base:1, ResistDivine:Base:1`
- dur=2 | maxStk=1000
- descricao (completa): Inspiration: +1% to all Resistance per stack.
- ja no mod: nao

## Inspiration  [Common]
- efeitos: `ResistPhysical:Base:2, ResistCold:Base:2, ResistFire:Base:2, ResistLightning:Base:2, ResistDivine:Base:2`
- dur=2 | maxStk=1000
- descricao (completa): Inspiration: +2% to all Resistance per stack.
- ja no mod: nao

## Inspiring Aura  [Common]
- efeitos: `DamageMod:Base:60`
- dur=4 | maxStk=100
- descricao (completa): Damage increased by 60%.
- ja no mod: nao

## Intelligence  [Common]
- efeitos: `IntelligenceBase:Base:Mathf.Round(1f+(0.2f*IslandLevel))`
- dur=0 | maxStk=100
- descricao (completa): Intelligence increased by [0].
- ja no mod: nao

## Invincible  [Common]
- efeitos: `Invincible:Set:1`
- dur=1 | maxStk=100
- descricao (completa): Cannot take damage.
- ja no mod: nao

## Invincible  [Common]
- efeitos: `Invincible:Set:1`
- dur=1 | maxStk=100
- descricao (completa): Invincible.
- ja no mod: nao

## Ivory Dragon Scale  [Mythic]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): Gain the ability to shapeshift into a White Dragonkin.  <i><color=#808080>"Imbued with a gentle radiance, it serves as a testament to the enduring strength of the forces of light"</i></color>
- ja no mod: nao

## Lady of the Well  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): Search the Forest at night for the Lady of the Well, vanquish her, and bring her <quest>Shadow-Drenched Heart</quest> to The Paladin.
- ja no mod: nao

## Leech Dexterity  [Common]
- efeitos: `DexterityBase:Base:2 * (.1f * Target.Level)`
- dur=2 | maxStk=10
- descricao (completa): [0] @dexterity@ absorbed per stack.  Stacks up to 10 times.
- ja no mod: nao

## Leech Intelligence  [Common]
- efeitos: `IntelligenceBase:Base:2 * (.1f * Target.Level)`
- dur=2 | maxStk=10
- descricao (completa): [0] @intelligence@ absorbed per stack.  Stacks up to 10 times.
- ja no mod: nao

## Leech Might  [Common]
- efeitos: `MightBase:Base:2 * (.1f * Target.Level)`
- dur=2 | maxStk=10
- descricao (completa): [0] @might@ absorbed per stack.  Stacks up to 10 times.
- ja no mod: nao

## Legacy of the Mad Mage  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): What have you unleashed upon the world?
- ja no mod: nao

## Lesser Heal  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['Healing'] = Source.SpellPower('Light') * .5f`
- dur=0 | maxStk=100
- descricao (completa): Healed.
- ja no mod: nao

## Lightning Shield  [Common]
- efeitos: `ResistLightning:Base:10`
- dur=3 | maxStk=100
- descricao (completa): @Lightning resistance@ increased by 10%.   Attackers take *0 lightning damage.
- ja no mod: nao

## Lingering Light  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['Healing'] = Source.SpellPower('Light') * .4f`
- dur=3 | maxStk=100
- descricao (completa): Restores *0 health per turn.
- ja no mod: nao

## Living Armor  [Common]
- efeitos: `Armor:Base:3.5f * Source.Level, MagicArmor:Base:3.5f * Source.Level`
- efeitosDano: `TargetStored['Healing'] = Source.SpellPower('Light') * .5f`
- dur=3 | maxStk=100
- descricao (completa): @armor@ and @magic armor@ increased by [0].   Regenerate *0 of @health@ each turn.
- ja no mod: nao

## March of the Warrior  [Rare]
- efeitos: `TurnFreeMovementPoints:Base:{1,4, dr}`
- dur=0 | maxStk=1
- descricao (completa): @Movement Points@ increased by [0].  <i><color=#808080>"Your courage must not be reckless, but calculated. Do not fear death; for it is an eventual certainty. "</i></color>
- ja no mod: nao

## Mark of the Alpha  [Mythic]
- efeitos: `SummonDamageMod:Base:{5,25}, SummonHealthMod:Base:{5,25}`
- dur=0 | maxStk=1
- descricao (completa): <i><color=#808080>"Look at me, I'm the alpha now!</i></color>   Changes your @Nature Summons@ into @Pack Summons@. Increases Summon Damage and Health by {5,25}%
- ja no mod: nao

## Martial Prowess  [Rare]
- efeitos: `DamageModPhysical:Base:{5,20}`
- dur=0 | maxStk=1
- descricao (completa): Increases @Physical Damage@ by {5,20}%.
- ja no mod: nao

## Masochism  [Common]
- efeitos: `DamageMod:Base:2`
- dur=1 | maxStk=100
- descricao (completa): Damage or healing increased by 2%.
- ja no mod: nao

## Masochism  [Common]
- efeitos: `DamageMod:Base:5`
- dur=1 | maxStk=100
- descricao (completa): Damage or healing increased by 5%.
- ja no mod: nao

## Master of Rage  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): Slay the nearby Wendigo.
- ja no mod: nao

## Master of the Blade  [Mythic]
- efeitos: `DamageModPhysical:Base:{8,40}`
- dur=0 | maxStk=1
- descricao (completa): <i><color=#808080>A true master of the blade.</color></i>  Increases @Physical Damage@ by {8,40}%. Physical damage you deal applies 1 stack of @Bleeding@.
- ja no mod: nao

## Might  [Common]
- efeitos: `MightBase:Base:Mathf.Round(1f+(0.2f*IslandLevel))`
- dur=0 | maxStk=100
- descricao (completa): Might increased by [0].
- ja no mod: SIM

## Might of the Conqueror  [Common]
- efeitos: `CritChance:Set:100`
- dur=4 | maxStk=100
- descricao (completa): Your next action has 100% Critical Hit Chance.
- ja no mod: nao

## Might of the Iceclaw  [Common]
- efeitos: `DamageMod:Base:50, ModelScaleMultiplier:Base:15`
- dur=4 | maxStk=100
- descricao (completa): Damage increased by 50%.
- ja no mod: nao

## Might of the Warrior  [Rare]
- efeitos: `MightBase:Base:{5,25}`
- dur=0 | maxStk=1
- descricao (completa): @Might@ increased by {5,25}.  <i><color=#808080>"Your strength lays in your conviction, your unyielding belief that this fight is right. The blade you wield is an extension of this conviction, a physical manifestation of your oath."</i></color>
- ja no mod: nao

## Miniature  [Common]
- efeitos: `TurnFreeMovementPoints:Base:3, ExtraTurnActionPoints:Base:1, MaxHealth:Percentage:-25, DamageMod:Base:-25, ModelScaleMultiplier:Base:-25`
- dur=3 | maxStk=100
- descricao (completa): Movement increased by 3 Action Points increased by 1 Max Health reduced by 25% Damage reduced by 25%
- ja no mod: nao

## Mirror Shard  [Legendary]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): Summon a Dark clone of yourself but it fights for you.   <i><color=#808080>You hold a shard of your shattered reflection!</color></i>
- ja no mod: nao

## Molten Crystal  [Mythic]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): <i><color=#808080>The magic crystal emanates heat.</color></i>  Allows you to summon a @level@ {1,30} Molten Golem to fight for you. Benefits from your @Fire Damage@.
- ja no mod: nao

## Molten Plating  [Common]
- efeitos: `DamageReduction:Base:60`
- dur=1 | maxStk=10
- descricao (completa): Damage taken reduced by 60%.
- ja no mod: nao

## Momentum  [Common]
- efeitos: `DamageMod:Base:Target["MomentumValue"]`
- dur=1 | maxStk=100
- descricao (completa): Damage or healing of your next action is increased by [0]%.
- ja no mod: nao

## Muse  [Common]
- efeitos: `ManaCostMod:Base:-10`
- dur=1 | maxStk=1
- descricao (completa): Mana costs reduced.
- ja no mod: nao

## Necromantic  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Summons a Skeletal Warrior on death
- ja no mod: nao

## Necronomicon  [Mythic]
- efeitos: `SummonDamageMod:Base:{5,25}, SummonHealthMod:Base:{5,25}`
- dur=0 | maxStk=1
- descricao (completa): <i><color=#808080>You carry the Necronomicon!</i></color>   Changes your @Skeletal Summons@ into something... stronger. Increases Summon Damage and Health by {5,25}%
- ja no mod: nao

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

## Test Event Status - Test Key  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): A key
- ja no mod: nao

## Test Fortune  [Mythic]
- efeitos: `DamageModColdToFrozen:Base:100 * (1 + ((StatusLevel - 1) * (0.23)))`
- dur=0 | maxStk=1
- descricao (completa): (vazia)
- ja no mod: nao

## The Animator - Quest Accept  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): (vazia)
- ja no mod: nao

## The Good Bloom  [Common]
- efeitos: `(vazio)`
- efeitosDano: `TargetStored['Healing'] = Source.SpellPower() * .4f; TargetStored['ManaDamage'] = Source.SpellPower() * -.4f`
- dur=3 | maxStk=100
- descricao (completa): Heals for *0 @health@ and @mana@.
- ja no mod: nao

## The Heart of Iron  [Mythic]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): <i><color=#808080>You bear the Heart of Iron!</i></color>   Allows you to raise a @level@ {1,30} Iron Golem to fight for you. Benefits from your @Physical Damage@.
- ja no mod: nao

## The Mad Mage - Part 1  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): (vazia)
- ja no mod: nao

## The Mad Mage - Part 2  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): (vazia)
- ja no mod: nao

## The Mad Mage - Part 4  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): (vazia)
- ja no mod: nao

## The Mad Mage - Part 5  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): (vazia)
- ja no mod: nao

## The True King  [Mythic]
- efeitos: `DamageModHealing:Base:{6,30}, ManaCostModLight:Base:{-10000, -10000}`
- dur=0 | maxStk=1
- descricao (completa): Light Spells no longer cost mana to cast. @Holy Power@ increased by {6,30}%.  <i><color=#808080>"The light is your birth right."</color></i>
- ja no mod: nao

## Thunder Charged  [Common]
- efeitos: `ModelScaleMultiplier:Base:10`
- dur=2 | maxStk=8
- descricao (completa): The next damage you deal causes a Thunder Bolt to strike your target. Stacks.
- ja no mod: nao

## Thunder Crystal  [Mythic]
- efeitos: `(vazio)`
- dur=0 | maxStk=1
- descricao (completa): <i><color=#808080>Energy hums within this magic crystal.</color></i>  Allows you to summon a @level@ {1,30} Thunder Golem to fight for you. Benefits from your @Lightning Damage@.
- ja no mod: nao

## Titan Bloom  [Common]
- efeitos: `DamageMod:Base:15, MaxHealth:Percentage:15, ModelScaleMultiplier:Base:10`
- dur=3 | maxStk=5
- descricao (completa): Increases Max Health and Damage by [0]%. Stacks.
- ja no mod: nao

## Tome of Tadashi  [Legendary]
- efeitos: `DodgeChance:Base:{2,10}`
- dur=0 | maxStk=1
- descricao (completa): Grants spells that can allow the user to escape death. Grants {2,10}% Dodge Chance.  <i><color=#808080>"Living is more than just staying alive, but staying alive can certainly help."</i></color>
- ja no mod: nao

## Touch of Flame  [Rare]
- efeitos: `DamageFlatFire:Base:ActionStatus.GetFlatDamageValue`
- dur=0 | maxStk=1
- descricao (completa): Increases @Fire Damage@ by GetFlatDamageValue().
- ja no mod: nao

## Touch of Frost  [Rare]
- efeitos: `DamageFlatCold:Base:ActionStatus.GetFlatDamageValue`
- dur=0 | maxStk=1
- descricao (completa): Increases @Cold Damage@ by GetFlatDamageValue().
- ja no mod: nao

## Touch of Thunder  [Rare]
- efeitos: `DamageFlatLightning:Base:ActionStatus.GetFlatDamageValue`
- dur=0 | maxStk=1
- descricao (completa): Increases @Lightning Damage@ by GetFlatDamageValue().
- ja no mod: nao

## Toxic  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Applies @2@ @poison@ when striking Applies @2@ @poison@ when struck
- ja no mod: nao

## Tranquility of the Forest  [Common]
- efeitos: `Recovery:Base:5+(5*0.2*IslandLevel)-(5*0.2)`
- dur=0 | maxStk=100
- descricao (completa): Recovery increased by [0].
- ja no mod: nao

## Transcendence  [Common]
- efeitos: `Invincible:Set:1`
- dur=VAR | maxStk=VAR
- descricao (completa): Cannot take damage.
- ja no mod: nao

## Transcendence  [Mythic]
- efeitos: `MaxHealth:Multiplicative:{.5,.65}`
- dur=VAR | maxStk=VAR
- descricao (completa): Reduces @Max Health@ by {50,35}%. Grants 4 charges of Transcendence per battle.  <i><color=#808080>You've transcended the material plane.</i></color>
- ja no mod: nao

## Treasure of Moltendunn  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): (vazia)
- ja no mod: nao

## Trial of the Ymir  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): A greater challenge looms ahead.
- ja no mod: nao

## Trophy Hunter  [Common]
- efeitos: `DamageMod:Base:10`
- dur=1 | maxStk=100
- descricao (completa): @Damage Dealt@ increased by 10% per stack.
- ja no mod: nao

## Uncanny Evasion  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Dodging incoming attacks.
- ja no mod: nao

## Uncanny Evasion  [Common]
- efeitos: `CounterAttackDamageMod:Base:50`
- dur=3 | maxStk=100
- descricao (completa): Increases Counter Attack damage by 50%.
- ja no mod: nao

## Undying  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Applies Dark Ritual on death
- ja no mod: nao

## Unholy Sacrifice  [Mythic]
- efeitos: `DamageModShadow:Base:{6,30}`
- dur=0 | maxStk=1
- descricao (completa): Grants the skill @Unholy Sacrifice@. Increases @Shadow Damage@ by {6,30}%.
- ja no mod: nao

## Unyielding Contender  [Common]
- efeitos: `Armor:Percentage:50, MagicArmor:Percentage:50, MaxHealth:Percentage:50`
- dur=2 | maxStk=100
- descricao (completa): Grants 50% increased Armor, Magic Armor, and Max Health.
- ja no mod: nao

## Vampire Lord Aura  [Common]
- efeitos: `LifeSteal:Base:50`
- dur=4 | maxStk=100
- descricao (completa): @Life steal@ increased by 50%.
- ja no mod: nao

## Vampiric  [Common]
- efeitos: `LifeOnHit:Base:10`
- dur=3 | maxStk=100
- descricao (completa): Life Steal increased by 10%
- ja no mod: nao

## Vampiric Aura  [Common]
- efeitos: `LifeOnHit:Base:5`
- dur=4 | maxStk=100
- descricao (completa): @Life Steal@ increased by 5%.
- ja no mod: nao

## Vampiric Aura  [Common]
- efeitos: `LifeSteal:Base:20`
- dur=4 | maxStk=100
- descricao (completa): @Life steal@ increased by 20%.
- ja no mod: nao

## Vampiric Aura  [Common]
- efeitos: `LifeOnHit:Base:5`
- dur=4 | maxStk=100
- descricao (completa): @Life steal@ increased by 5%.
- ja no mod: nao

## Vampiric Aura  [Common]
- efeitos: `LifeSteal:Base:50`
- dur=4 | maxStk=100
- descricao (completa): @Life steal@ increased.
- ja no mod: nao

## Vampirism  [Mythic]
- efeitos: `LifeOnHit:Base:{12,12}, ChildOfTheAbyss:Set:{1,1}, DamageMod:Base:{35,35}, ResistFire:Base:{-25,-25}`
- dur=0 | maxStk=1
- descricao (completa): Increases @Life Steal@ by @12@% and @Damage@ by @35@%.  Gain the ability to shapeshift into a @Vampire Bat@.  Decreases @Fire Resistance@ by @25@%. Can no longer heal from anything but lifesteal.  <i><color=#808080>"A vampire not evil, a paradox in twilight's gleam, Cleansing the world, in a dark redemption's dream."</i></color>
- ja no mod: nao

## Variety: Fire I  [Common]
- efeitos: `DamageModFire:Base:40`
- dur=1 | maxStk=100
- descricao (completa): Increases @Fire Damage@ dealt by 40%.
- ja no mod: nao

## Variety: Fire II  [Common]
- efeitos: `DamageModFire:Base:100`
- dur=1 | maxStk=100
- descricao (completa): Increases @Fire Damage@ dealt by 100%.
- ja no mod: nao

## Variety: Frost I  [Common]
- efeitos: `DamageModCold:Base:40`
- dur=1 | maxStk=100
- descricao (completa): Increases @Cold Damage@ dealt by 40%.
- ja no mod: nao

## Variety: Frost II  [Common]
- efeitos: `DamageModCold:Base:100`
- dur=1 | maxStk=100
- descricao (completa): Increases @Cold Damage@ dealt by 100%.
- ja no mod: nao

## Variety: Holy I  [Common]
- efeitos: `DamageModHealing:Base:40`
- dur=1 | maxStk=100
- descricao (completa): Increases @Holy Power@ by 40%.
- ja no mod: nao

## Variety: Holy II  [Common]
- efeitos: `DamageModHealing:Base:100`
- dur=1 | maxStk=100
- descricao (completa): Increases @Holy Power@ by 100%.
- ja no mod: nao

## Variety: Lightning I  [Common]
- efeitos: `DamageModLightning:Base:40`
- dur=1 | maxStk=100
- descricao (completa): Increases @Lightning Damage@ dealt by 40%.
- ja no mod: nao

## Variety: Lightning II  [Common]
- efeitos: `DamageModLightning:Base:100`
- dur=1 | maxStk=100
- descricao (completa): Increases @Lightning Damage@ dealt by 100%.
- ja no mod: nao

## Variety: Physical I  [Common]
- efeitos: `DamageModPhysical:Base:40`
- dur=1 | maxStk=100
- descricao (completa): Increases @Physical Damage@ dealt by 40%.
- ja no mod: nao

## Variety: Physical II  [Common]
- efeitos: `DamageModPhysical:Base:100`
- dur=1 | maxStk=100
- descricao (completa): Increases @Physical Damage@ dealt by 100%.
- ja no mod: nao

## Variety: Shadow I  [Common]
- efeitos: `DamageModShadow:Base:40`
- dur=1 | maxStk=100
- descricao (completa): Increases @Shadow Damage@ dealt by 40%.
- ja no mod: nao

## Variety: Shadow II  [Common]
- efeitos: `DamageModShadow:Base:100`
- dur=1 | maxStk=100
- descricao (completa): Increases @Shadow Damage@ dealt by 100%.
- ja no mod: nao

## Vengeful  [Common]
- efeitos: `(vazio)`
- dur=VAR | maxStk=VAR
- descricao (completa): Gains increased damage for each ally killed
- ja no mod: nao

## Vengeful  [Common]
- efeitos: `DamageMod:Base:15, ModelScaleMultiplier:Base:5`
- dur=VAR | maxStk=VAR
- descricao (completa): Increases damage dealt by 15%.
- ja no mod: nao

## Venomous Skin  [Common]
- efeitos: `(vazio)`
- dur=3 | maxStk=100
- descricao (completa): Attackers are infected with 3 stacks of poison.
- ja no mod: nao

## Verse of Valor  [Common]
- efeitos: `MightBase:Base:5 * Source.GetNumStatuses("BRD_Crescendo_Valor")`
- dur=1 | maxStk=1
- descricao (completa): Might increased by [0].
- ja no mod: SIM

## Vitality  [Common]
- efeitos: `VitalityBase:Base:Mathf.Round(1f+(0.2f*IslandLevel))`
- dur=0 | maxStk=100
- descricao (completa): Vitality increased by [0].
- ja no mod: nao

## Warding Tonic  [Common]
- efeitos: `MagicArmor:Base:200`
- dur=5 | maxStk=100
- descricao (completa): Magic armor increased by 200.
- ja no mod: nao

## Warrior Aura  [Common]
- efeitos: `DamageMod:Base:Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100)))`
- dur=3 | maxStk=100
- descricao (completa): Damage increased by [0]%.
- ja no mod: nao

## Well Fed:  Experience  [Common]
- efeitos: `ExperienceMod:Base:50`
- dur=0 | maxStk=100
- descricao (completa): Experience gained increased by 50%.
- ja no mod: nao

## Well Fed: Stats  [Common]
- efeitos: `MightBase:Percentage:10, DexterityBase:Percentage:10, IntelligenceBase:Percentage:10, VitalityBase:Percentage:10, ReflexBase:Percentage:10`
- dur=0 | maxStk=100
- descricao (completa): Stats increased by 10%.
- ja no mod: nao

## Well Fed: Treasure  [Common]
- efeitos: `GoldMod:Base:50, DropQuantityMod:Base:50`
- dur=0 | maxStk=100
- descricao (completa): Increases item drops and gold gained by 50%.
- ja no mod: nao

## Will of the Shaman  [Rare]
- efeitos: `ManaPerTurn:Base:12 * (1 + ((StatusLevel - 1) * (0.23)))`
- dur=0 | maxStk=1
- descricao (completa): @Mana Recovery@ increased by [0].  <i><color=#808080>"Unseen yet felt, the spirit dances like a flame in the wind, a whisper of the unseen world that echoes in our hearts.
- ja no mod: nao

## Wrath of the Righteous  [Mythic]
- efeitos: `DamageModHealing:Base:{6,30}`
- dur=VAR | maxStk=VAR
- descricao (completa): Healing skills in the Light tree can now deal damage to enemies as well as heal allies. @Holy Power@ increased by {6,30}%.  <i><color=#808080>"The light of vengence burns brightly!"</color></i>
- ja no mod: nao

## Wrath of the Righteous  [Common]
- efeitos: `(vazio)`
- dur=VAR | maxStk=VAR
- descricao (completa): Search the Castle for <b>The Jester</b>, and bring an end to his evil.
- ja no mod: nao

## Ymir Rune, Courage  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): (vazia)
- ja no mod: nao

## Ymir Rune, Honor  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): (vazia)
- ja no mod: nao

## Ymir Rune, Strength  [Common]
- efeitos: `(vazio)`
- dur=0 | maxStk=100
- descricao (completa): (vazia)
- ja no mod: nao

