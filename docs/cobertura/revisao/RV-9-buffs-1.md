# RV-9 - Buffs: arquivo de trabalho (393 entradas)

Gerado do `status.csv`. **Descricoes COMPLETAS** (ja errei com texto truncado, RV-8c).
`dur` = duracao em turnos e `maxStk` = cap de stacks (campos `Duration`/`MaxStacks` do asset, l.319141/319149);
`VAR` = existem assets HOMONIMOS com valores diferentes - nesse caso confira por ASSET, nao por nome.

> ATENCAO: o nome NAO identifica o status. Assets homonimos tem papeis diferentes.

## 
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
