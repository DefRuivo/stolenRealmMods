# Ficha de revisao — arvore **Monk** (36 skills)

> Gerado por `tools/verify_tree.py`. Junta o TEXTO da tooltip com o que o jogo
> CALCULA. A ultima linha de cada ficha (`conferir`) lista o que **nao** tem par no
> codigo — e o que precisa de olho humano ou triangulacao externa, nao veredito.


## T1 Chi Strike

`corrigido`


**Texto:** Strike an enemy dealing *0 weapon damage.  Reduces the targets damage dealt by 20% for 1 turn.


**expr:** `Source.AttackPower * 1.2f * Source.DamageModPhysical`


**acao `Chi Strike`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1.2f`


**conferir:** 20% — sem par no codigo dumpado


## T1 Contemplation I · **PASSIVA**

`pendente`


**Texto:** Max Mana increased by 10%.


**attr:** `MaxMana:Percentage:10,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Endurance I · **PASSIVA**

`pendente`


**Texto:** Max Health increased by 10%.


**attr:** `MaxHealth:Percentage:10,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Front Kick

`pendente`


**Texto:** Kicks the target dealing *0 physical damage and knocking the target back up to 3 hexes.   Any enemy hit by the target also receives *0 damage.


**expr:** `Source.AttackPower * 1.5f * Source.DamageModPhysical`


**acao `Front Kick`:** `TargetStored['PhysicalDamage'] = Source.AttackPower * 1.5f`


**conferir:** 3 hex — sem par no codigo dumpado


## T1 Incapacitate

`pendente`


**Texto:** Incapacitates the target applying {STA=Sleep} for 2 turns.


**acao `Incapacitate`:** `-`


**status `Sleep`:** efeitos=`Rooted:Set:1, Disabled:Set:1, DamageReduction:Base:-50` classe=indefinido


> Asleep.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Masochism I · **PASSIVA**

`pendente`


**Texto:** Gain a stack of Masochism each time you take damage. Each stack increases the damage/healing you deal by 2%. Lasts 1 turn. 


**status `Masochism`:** efeitos=`DamageMod:Base:5` classe=buff


> Damage or healing increased by 5%.


**conferir:** 2% — sem par no codigo dumpado


## T1 Momentum I · **PASSIVA**

`pendente`


**Texto:** Each hex moved grants a stack of Momentum increasing the damage or healing of your next ability by 2%.


**status `Momentum`:** efeitos=`DamageMod:Base:Target["MomentumValue"]` classe=buff


> Damage or healing of your next action is increased by [0]%.


**conferir:** 2% — sem par no codigo dumpado


## T2 Contemplation II · **PASSIVA**

`pendente`


**Texto:** Max Mana increased by an additional 15%.


**attr:** `MaxMana:Percentage:15,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Endurance II · **PASSIVA**

`pendente`


**Texto:** Max Health increased by an additional 15%.


**attr:** `MaxHealth:Percentage:15,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Focused Strike

`pendente`


**Texto:** Strike an enemy dealing *0 weapon damage. Applies a debuff that increases the damage this target takes from all sources for 2 turns by 20%.


**expr:** `Source.AttackPower * 1.4f * Source.DamageModPhysical`


**acao `Focused Strike`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1.4f`


**conferir:** 20% — sem par no codigo dumpado


## T2 Force Kick

`pendente`


**Texto:** Kicks the target dealing *0 physical damage and knocking the target back up to 5 hexes.   Any enemy hit by the target also receives *0 physical damage.


**expr:** `Source.AttackPower * 1.7f * Source.DamageModPhysical`


**acao `Force Kick`:** `TargetStored['PhysicalDamage'] = Source.AttackPower * 1.7f`


**conferir:** 5 hex — sem par no codigo dumpado


## T2 Masochism II · **PASSIVA**

`pendente`


**Texto:** Gain a stack of Masochism each time you take damage. Each stack increases the damage/healing you deal by an additional 3%. Lasts 1 turn. 


**status `Masochism`:** efeitos=`DamageMod:Base:5` classe=buff


> Damage or healing increased by 5%.


**conferir:** 3% — sem par no codigo dumpado


## T2 Momentum II · **PASSIVA**

`pendente`


**Texto:** Each hex moved grants a stack of Momentum increasing the damage or healing of your next ability by an additional 3%. 


**status `Momentum`:** efeitos=`DamageMod:Base:Target["MomentumValue"]` classe=buff


> Damage or healing of your next action is increased by [0]%.


**conferir:** 3% — sem par no codigo dumpado


## T2 Pain Suppression

`pendente`


**Texto:** The target's Damage Reduction is increased by 50% for 1 turn.


**acao `Pain Suppression`:** `-`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** 50% — sem par no codigo dumpado


## T2 Paralyzing Strike

`corrigido`


**Texto:** Strike an enemy dealing *0 weapon damage.  Stuns the target for 1 turn.


**expr:** `Source.AttackPower * 1.4f * Source.DamageModPhysical`


**acao `Paralyzing Strike`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1.4f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Stunning Kick

`pendente`


**Texto:** Kicks the target dealing *0 physical damage and stunning them for 1 turn.


**expr:** `Source.AttackPower * 1.5f * Source.DamageModPhysical`


**acao `Stunning Kick`:** `TargetStored['PhysicalDamage'] = Source.AttackPower * 1.5f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Combo Breaker · **PASSIVA**

`pendente`


**Texto:** Basic attacks grant Combo Breaker. Combo Breaker gives your next non basic attack ability 10% damage and healing per stack. Stacks are consumed on use. 


**status `Combo Breaker`:** efeitos=`ManaPowerMod:Base:10` classe=buff


> Damage and healing from non basic skills increased by 10%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Dashing Strikes

`pendente`


**Texto:** Dash to an enemy dealing *0 weapon damage then quickly dash to an enemy within 2 hexes to strike again. Strikes up to 4 times.


**expr:** `Source.AttackPower * 1.5f * Source.DamageModPhysical`


**acao `Dashing Strikes`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1.5f`


**conferir:** 2 hex — sem par no codigo dumpado


## T3 Falcon Dash

`pendente`


**Texto:** Dash to the target area and dealing *0 weapon damage to affected area.


**expr:** `Source.AttackPower * 1.0f * Source.DamageModPhysical`


**acao `Falcon Dash`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * .8f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Meditation

`pendente`


**Texto:** Put the target ally into a meditative state restoring 20% of max health and mana. 


**acao `Meditation`:** `TargetStored['Healing'] = Target['MaxHealth'] * .2f; TargetStored['ManaDamage'] = -(Target['MaxMana'] * .2f)`


**conferir:** 20% — sem par no codigo dumpado


## T3 Momentum III · **PASSIVA**

`pendente`


**Texto:** Each hex moved grants a stack of Momentum increasing the damage or healing of your next ability by an additional 5%. 


**status `Momentum`:** efeitos=`DamageMod:Base:Target["MomentumValue"]` classe=buff


> Damage or healing of your next action is increased by [0]%.


**conferir:** 5% — sem par no codigo dumpado


## T3 Sweeping Kick

`revisado`


**Texto:** Deal *0 physical damage to all enemies within 1 hex. Knocks back all enemies up to 3 hexes. Targets are crippled for 1 turn. 


**expr:** `Source.AttackPower * 1.6f * Source.DamageModPhysical`


**acao `Sweeping Kick`:** `TargetStored['PhysicalDamage'] = Source.AttackPower * 1.6f`


**conferir:** 3 hex — sem par no codigo dumpado


## T3 Weapon of Choice · **PASSIVA**

`pendente`


**Texto:** 3% of your total attribute value is added to your character as @Additional Weapon Damage@.   Current Bonus: [0]


**attr:** `AdditionalWeaponDamage:Base:Source.SumOfAllAttributes * .03f,`


**expr:** `(Source['Might'] + Source['Dexterity'] + Source['Intelligence'] + Source['Vitality'] + Source['Reflex']) * .03f`


**conferir:** 3% — sem par no codigo dumpado


## T3 Willpower · **PASSIVA**

`pendente`


**Texto:** Every 10% of your max health you are missing increases damage reduction by 4%.


**attr:** `DamageReduction:Base:Math.Round(Source.HealthRatioInverse, 1) * 40,`


**conferir:** 10%, 4% — sem par no codigo dumpado


## T4 Body and Soul · **PASSIVA**

`pendente`


**Texto:** Intelligence now gives 5 Magic Armor per point and Vitality now gives 5 Armor per point.


**attr:** `Armor:Base:Source["Vitality"] * 5, MagicArmor:Base:Source["Intelligence"] * 5,`


**status `Intelligence`:** efeitos=`IntelligenceBase:Base:Mathf.Round(1f+(0.2f*IslandLevel))` classe=buff


> Intelligence increased by [0].


**status `Vitality`:** efeitos=`VitalityBase:Base:Mathf.Round(1f+(0.2f*IslandLevel))` classe=buff


> Vitality increased by [0].


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Crash and Flow · **PASSIVA**

`pendente`


**Texto:** Dodging an attack increases your damage dealt by 10%. Stacks 5. Lasts 1 turn.


**conferir:** 10% — sem par no codigo dumpado


## T4 Cyclone Kick

`revisado`


**Texto:** Deals *0 physical damage. Pulls enemies within 4 hexes towards you. Targets are crippled for 1 turn. 


**expr:** `Source.AttackPower * 1.6f * Source.DamageModPhysical`


**acao `Cyclone Kick`:** `TargetStored['PhysicalDamage'] = Source.AttackPower * 1.6f`


**conferir:** 4 hex — sem par no codigo dumpado


## T4 Dodging Strikes

`corrigido`


**Texto:** Dash to an enemy dealing *0 weapon damage then quickly dash to an enemy within 2 hexes to strike again. Strikes up to 4 times.  Each time you strike a target it increases your dodge chance by 8%.  Lasts 2 turns. 


**expr:** `Source.AttackPower * 1.8f * Source.DamageModPhysical`


**acao `Dodging Strikes`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1.8f`


**conferir:** 2 hex, 8% — sem par no codigo dumpado


## T4 Power Strikes

`corrigido`


**Texto:** Dash to an enemy dealing *0 weapon damage then quickly dash to an enemy within 2 hexes to strike again. Strikes up to 4 times.  Each time you hit increases the damage of Power Strikes by 50%.


**expr:** `Source.AttackPower * 1.8f * Source.DamageModPhysical`


**acao `Power Strikes`:** `TargetStored[Source.WeaponDamageType] = (Source.AttackPower * 1.8f) * (1 + (ChainCount * .5f))`


**conferir:** 2 hex, 50% — sem par no codigo dumpado


## T4 Soul Cleanse

`pendente`


**Texto:** Removes all negative status effects from target ally. Each status effect removed heals the target for 10% of their max health.   Can be used when Disabled.


**acao `Soul Cleanse`:** `-`


**status `Disabled`:** efeitos=`Disabled:Set:1` classe=buff


> Cannot perform actions.


**conferir:** 10% — sem par no codigo dumpado


## T4 Speed · **PASSIVA**

`pendente`


**Texto:** Increases @Dexterity@ and @Reflex@ by 15%.


**attr:** `DexterityBase:Percentage:15, ReflexBase:Percentage:15,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Strength · **PASSIVA**

`pendente`


**Texto:** Increases @Might@ and @Vitality@ by 15%.


**attr:** `MightBase:Percentage:15, VitalityBase:Percentage:15,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Many Sided Strike

`corrigido`


**Texto:** Hit enemies in the target area 5x randomly.  Deals *0 weapon damage per hit. 


**expr:** `Source.AttackPower * .8f * Source.DamageModPhysical`


**acao `Many Sided Strike`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * .8f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 One Punch Monk · **PASSIVA**

`pendente`


**Texto:** The first damaging or healing ability you use on your turn has its effectiveness tripled, after which you are unable to use any more damaging or healing abilities that turn.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Perfected Soul · **PASSIVA**

`corrigido`


**Texto:** Increases all attributes by [0]. In addition, 10% of your highest attribute value is added to all other attributes.  Current Bonus: [1]


**attr:** `Might:Base:Source.HighestStatName != "MightBase" ? Source[Source.HighestStatName] * .1f : 0, Dexterity:Base:Source.HighestStatName != "DexterityBase" ? Source[Source.HighestStatName] * .1f : 0, Vitality:Base:Source.HighestStatName != "VitalityBase" ? Source[Source.HighestStatName] * .1f : 0, Intelligence:Base:Source.HighestStatName != "IntelligenceBase" ? Source[Source.HighestStatName] * .1f : 0, Reflex:Base:Source.HighestStatName != "ReflexBase" ? Source[Source.HighestStatName] * .1f : 0, Might:Base:Source.Level, Dexterity:Base:Source.Level, Intelligence:Base:Source.Level, Vitality:Base:Source.Level, Reflex:Base:Source.Level,`


**expr:** `Target.Level; Source.HighestStatValue * 0.1f`


**conferir:** 10% — sem par no codigo dumpado


## T5 Quaking Fist

`pendente`


**Texto:** Deals *0 physical damage to all foes within 3 hexes. 


**expr:** `Source.AttackPower * 2.5f * Source.DamageModPhysical`


**acao `Quaking Fist`:** `TargetStored['PhysicalDamage'] = Source.AttackPower * 2.5f`


**conferir:** 3 hex — sem par no codigo dumpado

