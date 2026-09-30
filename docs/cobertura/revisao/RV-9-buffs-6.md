# RV-9 - Buffs: arquivo de trabalho (393 entradas)

Gerado do `status.csv`. **Descricoes COMPLETAS** (ja errei com texto truncado, RV-8c).
`dur` = duracao em turnos e `maxStk` = cap de stacks (campos `Duration`/`MaxStacks` do asset, l.319141/319149);
`VAR` = existem assets HOMONIMOS com valores diferentes - nesse caso confira por ASSET, nao por nome.

> ATENCAO: o nome NAO identifica o status. Assets homonimos tem papeis diferentes.

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

