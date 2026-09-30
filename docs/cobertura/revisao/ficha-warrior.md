# Ficha de revisao — arvore **Warrior** (39 skills)

> Gerado por `tools/verify_tree.py`. Junta o TEXTO da tooltip com o que o jogo
> CALCULA. A ultima linha de cada ficha (`conferir`) lista o que **nao** tem par no
> codigo — e o que precisa de olho humano ou triangulacao externa, nao veredito.


## T1 Bash

`corrigido`


**Texto:** Deals *0 weapon damage.  Knocks the target back up to 3 hexes.


**expr:** `Source.AttackPower * 1.2f * Source.DamageModPhysical`


**acao `Bash`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1.2f`


**conferir:** 3 hex — sem par no codigo dumpado


## T1 Challenger · **PASSIVA**

`pendente`


**Texto:** For every enemy within 1 hex of your character gain 5% to @Armor@ and @magic armor@.


**attr:** `Armor:Percentage:5 * Source.NumEnemiesWithin(1), MagicArmor:Percentage:5 * Source.NumEnemiesWithin(1),`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Double Edge

`pendente`


**Texto:** Deals *0 weapon damage to the target and 15% of the damage back to you. 


**expr:** `Source.AttackPower * 1.8f * Source.DamageModPhysical`


**acao `Double Edge`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1.8f; SourceStored['DamageReturned'] = 15`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Fracture

`corrigido`


**Texto:** Deals *0 weapon damage.  Lowers targets @Resistance@ by 20% for 2 turns.


**expr:** `Source.AttackPower * .7f * Source.DamageModPhysical`


**acao `Fracture`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * .7f`


**conferir:** 20% — sem par no codigo dumpado


## T1 Guardian I · **PASSIVA**

`pendente`


**Texto:** Increase @Physical Resistance@ by 5%.


**attr:** `ResistPhysical:Base:5,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Rage

`corrigido`


**Texto:** Increases @Damage dealt@ and @Max Life@ by 15%.  Increases @damage received@ by 15%.


**acao `Rage`:** `-`


**conferir:** 15% — sem par no codigo dumpado


## T1 Wanderer · **PASSIVA**

`pendente`


**Texto:** Increase @movement points@ by 1.


**attr:** `TurnFreeMovementPoints:Base:1,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Warmonger I · **PASSIVA**

`pendente`


**Texto:** Increase all Damage and Healing by 8%. 


**attr:** `DamageMod:Base:8,`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Berserker's Rage

`pendente`


**Texto:** Increases @Damage dealt@ and @damage received@ by 25%. Increases @Max Life@ by 15%.


**acao `Berserker's Rage`:** `-`


**conferir:** 15%, 25% — sem par no codigo dumpado


## T2 Bloodlet

`corrigido`


**Texto:** Sacrifice 15% of your maximum health in exchange for an additonal action this turn.  Applies {STA=Exhaustion}.


**acao `Bloodlet`:** `TargetStored['PhysicalDamage'] = Target['MaxHealth'] * .15f; Target['ActionPoints'] = Target['ActionPoints'] + (Target['RecentlyHasted'] == 0 ? 1 : 0)`


**status `Exhaustion`:** efeitos=`RecentlyHasted:Set:1` classe=buff


> Cannot receive additional actions points.  Caused by receiving additional action points this turn.


**conferir:** 15% — sem par no codigo dumpado


## T2 Charge

`pendente`


**Texto:** Charges to the target and deals *0 weapon damage to all enemies in your path.


**expr:** `Source.AttackPower * .7f * Source.DamageModPhysical`


**acao `Charge`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Cleave

`pendente`


**Texto:** Swing in a 180 degree arc striking all foes for *0 weapon damage.


**expr:** `Source.AttackPower * 1.5f * Source.DamageModPhysical`


**acao `Cleave`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1.5f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Dispelling Fracture

`corrigido`


**Texto:** Deals *0 weapon damage, removes 1 random benefical status from the target and lowers the target's @Resistance@ by 20% for 2 turns.


**expr:** `Source.AttackPower * .8f * Source.DamageModPhysical`


**acao `Threatening Fracture`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * .8f`


**conferir:** 20% — sem par no codigo dumpado


## T2 Guardian II · **PASSIVA**

`pendente`


**Texto:** Increase @Physical Resistance@ by an additional 10%.


**attr:** `ResistPhysical:Base:10,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Into the Fray · **PASSIVA**

`pendente`


**Texto:** For every enemy within 3 hexes of your character gain 3% @increased Damage@ and 3% @Maximum Health@.


**attr:** `DamageMod:Base:3 * Source.NumEnemiesWithin(3), MaxHealth:Percentage:3 * Source.NumEnemiesWithin(3),`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Mortal Fracture

`pendente`


**Texto:** Deals *0 weapon damage and lowers target's @Resistance@ by 20% and @Healing@ received by 50% for 2 turns.


**expr:** `Source.AttackPower * .8f * Source.DamageModPhysical`


**acao `Mortal Fracture`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * .8f`


**conferir:** 20%, 50% — sem par no codigo dumpado


## T2 Opportunist · **PASSIVA**

`pendente`


**Texto:** Increases damage of @opportunity attacks@ and @counter attacks@ by 25%.


**attr:** `OpportunityAttackDamageMod:Base:25, CounterAttackDamageMod:Base:25,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Tempered Rage

`pendente`


**Texto:** Increases @Damage@, @Armor@, and @Magic Armor@ by 15%.


**acao `Tempered Rage`:** `-`


**conferir:** 15% — sem par no codigo dumpado


## T2 Warmonger II · **PASSIVA**

`pendente`


**Texto:** Increase all Damage and Healing by 12%. 


**attr:** `DamageMod:Base:12,`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Battle Ready · **PASSIVA**

`corrigido`


**Texto:** 1% of your @Armor@ value is added to your character as @Additional Weapon Damage@.  Current Bonus: [0]


**attr:** `AdditionalWeaponDamage:Base:Source["Armor"] * .01f,`


**expr:** `Source['Armor'] * .01f`


**conferir:** 1% — sem par no codigo dumpado


## T3 Beserker's Blood · **PASSIVA**

`pendente`


**Texto:**  For every 1% of health missing, gain 1% increased damage.


**attr:** `DamageMod:Base:Source.HealthRatioInverse * 100,`


**conferir:** 1% — sem par no codigo dumpado


## T3 Bleeding Cleave

`corrigido`


**Texto:** Swing in a 180 degree arc striking all foes for *0 weapon damage.  Applies 2 stacks of {STA=Bleeding} on all targets hit. 


**expr:** `Source.AttackPower * 1f * Source.DamageModPhysical`


**acao `Bleeding Cleave`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1f`


**status `Bleeding`:** efeitos=`ResistPhysical:Base:-5, BleedingDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Bleeding", "TargetStored[\"PhysicalDamage\"] = Source.AttackPower * .05f"))` classe=debuff


> Target takes [1] physical damage for each hex they move. Reduces Physical Resistance by [0]%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Dual-Wield Mastery · **PASSIVA**

`pendente`


**Texto:** While dual-wielding, @dodge chance@ increased by 5%, @critical hit chance@ increased by 5%, and @critical hit damage@ is increased by 20%.


**attr:** `DodgeChance:Base:Source.IsDualWielding ? 5 : 0, CritChance:Base:Source.IsDualWielding ? 5 : 0, CritDamage:Base:Source.IsDualWielding ? 20 : 0,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Howl

`corrigido`


**Texto:** Deals *0 physical damage.  Enemies within 2 hexes deal 20% less damage.


**expr:** `Source.AttackPower * .7f * Source.DamageModPhysical`


**acao `Howl`:** `TargetStored['PhysicalDamage'] = Source.AttackPower * .7f`


**conferir:** 2 hex, 20% — sem par no codigo dumpado


## T3 Life Cleave

`corrigido`


**Texto:** Swing in a 180 degree arc striking all foes for *0 weapon damage.  Lifesteals for 10% per target hit.  @Life Steal@ heals you for a percentage of your @max health@ each time you hit. Reduced for area of effect and no ap cost abilities.


**expr:** `Source.AttackPower * 1.5f * Source.DamageModPhysical`


**acao `Life Cleave`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1.5f; SourceStored['LifeOnHit'] = 10`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Shield Mastery · **PASSIVA**

`pendente`


**Texto:** Increases @All Stats@ from shields by 50%


**attr:** `ShieldMastery:Set:1,`


**conferir:** 50% — sem par no codigo dumpado


## T3 Slam

`pendente`


**Texto:** Deals *0 weapon damage to all enemies within a line.


**expr:** `Source.AttackPower * 1.6f * Source.DamageModPhysical`


**acao `Slam`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1.6f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Two-Handed Mastery · **PASSIVA**

`pendente`


**Texto:** While a two handed weapon is equipped all damage is increased by 20%. 


**attr:** `DamageMod:Base:Source.WieldingTwoHanded ? 20 : 0,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Warrior's Boon

`pendente`


**Texto:** Heals 25% of your maximum health and removes all negative statuses. Can be used when Disabled.


**acao `Warrior's Boon`:** `TargetStored['Healing'] = Target['MaxHealth'] * .25f`


**status `Disabled`:** efeitos=`Disabled:Set:1` classe=buff


> Cannot perform actions.


**conferir:** 25% — sem par no codigo dumpado


## T4 Blood Drinker · **PASSIVA**

`corrigido`


**Texto:** Increases basic attack damage by 50%. Basic attacks now @Life steal@ for 5%.  @Life Steal@ heals you for a percentage of your @max health@ each time you hit. Reduced for area of effect and no ap cost abilities.


**attr:** `DamageModBasic:Base:50, LifeOnHitBasic:Base:5,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Bone Collector · **PASSIVA**

`corrigido`


**Texto:** Every enemy slain grants 6% @maximum health@ and @Increased Damage@.  Lasts the duration of the battle.  Stacks up to 5 times.


**conferir:** 6% — sem par no codigo dumpado


## T4 Crushing Slam

`pendente`


**Texto:** Deals *0 weapon damage to all enemies within a line.


**expr:** `Source.AttackPower * 2.4f * Source.DamageModPhysical`


**acao `Crushing Slam`:** `TargetStored[Source.WeaponDamageType] = (Source.AttackPower * 2.4f)`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Executioner · **PASSIVA**

`corrigido`


**Texto:** Every enemy slain on your turn grants 1 additonal AP.  Can only grant up to 1 additional AP per turn.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Stunning Slam

`pendente`


**Texto:** Deals *0 weapon damage and applies {STA=Stunned} to all enemies within a line for 1 turn.


**expr:** `Source.AttackPower * 1.8f * Source.DamageModPhysical`


**acao `Stunning Slam`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1.8f`


**status `Stunned`:** efeitos=`Rooted:Set:1, Disabled:Set:1` classe=buff


> Stunned.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Vitality Break

`pendente`


**Texto:** Consumes 50% of your @current health@ to deal *0 weapon damage. Damage is increased by how much health is consumed. 


**acao `Vitality Break`:** `TargetStored[Source.WeaponDamageType] = (Source['Health'] * .4f); Source['Health'] = Source['Health'] / 2`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** 50% — sem par no codigo dumpado


## T5 Colossus · **PASSIVA**

`pendente`


**Texto:** Damage you deal splashes to enemies within 1 hex for 50% of the damage dealt.


**attr:** `Colossus:Set:1,`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** 50% — sem par no codigo dumpado


## T5 Indestructible · **PASSIVA**

`pendente`


**Texto:** Getting hit increases @armor@, @magic armor@, and @return damage@ by 10% per stack. Stacks 10 times.


**conferir:** 10% — sem par no codigo dumpado


## T5 Sunder

`corrigido`


**Texto:** Deals *0 weapon damage. Ignores all armor and resists. Cannot be dodged. @Life Steals@ for 25%.  @Life Steal@ heals you for a percentage of your @max health@ each time you hit. Reduced for area of effect and no ap cost abilities.


**expr:** `Source.AttackPower * 2f * Source.DamageModPhysical`


**acao `Sunder`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 2f; SourceStored['HealingForced'] = (Source['MaxHealth'] * .25f)`


**conferir:** 25% — sem par no codigo dumpado


## T5 Unyielding Contender

`pendente`


**Texto:** Grants 50% increased Armor, Magic Armor, and Max Health for 2 turns. Grants Enrage. Usable while stunned.


**acao `Unyielding Contender`:** `-`


**conferir:** 50% — sem par no codigo dumpado

