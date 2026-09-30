# Ficha de revisao — arvore **Thief** (38 skills)

> Gerado por `tools/verify_tree.py`. Junta o TEXTO da tooltip com o que o jogo
> CALCULA. A ultima linha de cada ficha (`conferir`) lista o que **nao** tem par no
> codigo — e o que precisa de olho humano ou triangulacao externa, nao veredito.


## T1 Ambush I · **PASSIVA**

`pendente`


**Texto:** Deal 16% @increased damage@ when an enemy has no allies within 3 hexes.


**attr:** `Ambush:Base:16,`


**conferir:** 3 hex — sem par no codigo dumpado


## T1 Cripple

`corrigido`


**Texto:** Deals *0 weapon damage.  Applies {STA=Slow} for 1 turn.


**expr:** `Source.AttackPower * .7f`


**acao `Cripple`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * .7f`


**status `Slow`:** efeitos=`MovementCostPerHexMod:Set:100` classe=buff


> Movement costs doubled.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Dagger Throw

`pendente`


**Texto:** Throw a dagger dealing *0 weapon damage.


**expr:** `Source.AttackPower * .7f * Source.DamageModPhysical`


**acao `Dagger Throw`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * .7f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Death Dealer I · **PASSIVA**

`pendente`


**Texto:** Increase @Critical Hit Damage and Healing@ by 16%.


**attr:** `CritDamage:Base:16,`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Escape

`corrigido`


**Texto:** Teleport to the target area.  Unaffected by increased range modifiers.


**acao `Escape`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Fencer's Finesse I · **PASSIVA**

`pendente`


**Texto:** Increases @dodge chance@ by 5%.


**attr:** `DodgeChance:Base:5,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Poison Weapon

`pendente`


**Texto:** Attacks now apply 1 stack of {STA=Poisoned}.


**acao `Poison Weapon`:** `-`


**status `Poisoned`:** efeitos=`HealingReceivedBonus:Base:-1, PoisonDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Poisoned", "TargetStored[\"ShadowDamage\"] = Source.SpellPower(\"Shadow\") * .1f")), ContagionLevel:Base:Source["ContagionSource"] > 0 ? 1 : 0` classe=debuff


> Target takes [1] shadow damage each turn. Reduces healing taken by [0]%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Swiftness · **PASSIVA**

`pendente`


**Texto:** Increases your @movement points@ by 1.


**attr:** `TurnFreeMovementPoints:Base:1,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Ambush II · **PASSIVA**

`pendente`


**Texto:** Deal an additional 24% @increased damage@ when an enemy has no allies within 3 hexes.


**attr:** `Ambush:Base:24,`


**conferir:** 3 hex — sem par no codigo dumpado


## T2 Deadly Dagger

`corrigido`


**Texto:** Throw a dagger dealing *0 weapon damage.  Deals 50% additional @critical hit damage@.


**expr:** `Source.AttackPower * .8f * Source.DamageModPhysical`


**acao `Deadly Dagger Throw`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * .8f; SourceStored['AdditionalCritDamage'] = 50`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Death Dealer II · **PASSIVA**

`pendente`


**Texto:** Increase @Critical Hit Damage and Healing@ by an additional 24%.


**attr:** `CritDamage:Base:24,`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Evasion

`pendente`


**Texto:** Gain 100% @dodge chance@ for the next attack.


**acao `Evasion`:** `Target['EvasionCharges'] = 1`


**conferir:** 100% — sem par no codigo dumpado


## T2 Fencer's Finesse II · **PASSIVA**

`pendente`


**Texto:** Increases @dodge chance@ by an additional 8%.


**attr:** `DodgeChance:Base:8,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Gouge

`corrigido`


**Texto:** Deals *0 weapon damage.  Applies 2 stacks of {STA=Bleeding}.


**expr:** `Source.AttackPower * .8f * Source.DamageModPhysical`


**acao `Gouge`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * .8f`


**status `Bleeding`:** efeitos=`ResistPhysical:Base:-5, BleedingDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Bleeding", "TargetStored[\"PhysicalDamage\"] = Source.AttackPower * .05f"))` classe=debuff


> Target takes [1] physical damage for each hex they move. Reduces Physical Resistance by [0]%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Hide In Shadows

`pendente`


**Texto:** Grants {STA=Stealth} for 2 turns. 


**acao `Hide In Shadows`:** `-`


**status `Stealth`:** efeitos=`Hidden:Set:1, UntargetableByEnemies:Set:1` classe=buff


> Invisible. Attacking from Stealth has 100% critical hit chance.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Maim

`corrigido`


**Texto:** Deals *0 weapon damage.  Applies {STA=Disabled} for 1 turn.


**expr:** `Source.AttackPower * .8f * Source.DamageModPhysical`


**acao `Maim`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * .8f`


**status `Disabled`:** efeitos=`Disabled:Set:1` classe=buff


> Cannot perform actions.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Poisoned Dagger

`corrigido`


**Texto:** Throw a poisoned dagger dealing *0 weapon damage.  Applies 2 stacks of {STA=Poisoned}.


**expr:** `Source.AttackPower * .8f * Source.DamageModPhysical`


**acao `Poisoned Dagger Throw`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * .8f`


**status `Poisoned`:** efeitos=`HealingReceivedBonus:Base:-1, PoisonDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Poisoned", "TargetStored[\"ShadowDamage\"] = Source.SpellPower(\"Shadow\") * .1f")), ContagionLevel:Base:Source["ContagionSource"] > 0 ? 1 : 0` classe=debuff


> Target takes [1] shadow damage each turn. Reduces healing taken by [0]%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Shroud · **PASSIVA**

`pendente`


**Texto:** Applies {STA=Stealth} at the start of each battle.


**status `Stealth`:** efeitos=`Hidden:Set:1, UntargetableByEnemies:Set:1` classe=buff


> Invisible. Attacking from Stealth has 100% critical hit chance.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 En Garde · **PASSIVA**

`pendente`


**Texto:** Increases your maximum amount of Counter Attacks per turn by 2.


**attr:** `CounterAttacksPerTurn:Base:2,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Enduring Evasion

`pendente`


**Texto:** Gain 100% @dodge chance@ for the next 2 attacks.


**acao `Enduring Evasion`:** `Target['EvasionCharges'] = 2`


**conferir:** 100% — sem par no codigo dumpado


## T3 Fade · **PASSIVA**

`pendente`


**Texto:** Whenever an enemy dies, you have a 50% chance to gain {STA=Stealth} for 1 turn. 


**status `Stealth`:** efeitos=`Hidden:Set:1, UntargetableByEnemies:Set:1` classe=buff


> Invisible. Attacking from Stealth has 100% critical hit chance.


**conferir:** 50% — sem par no codigo dumpado


## T3 Fight Dirty · **PASSIVA**

`pendente`


**Texto:** Your attacks apply 2 stacks of {STA=Poisoned}.


**status `Poisoned`:** efeitos=`HealingReceivedBonus:Base:-1, PoisonDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Poisoned", "TargetStored[\"ShadowDamage\"] = Source.SpellPower(\"Shadow\") * .1f")), ContagionLevel:Base:Source["ContagionSource"] > 0 ? 1 : 0` classe=debuff


> Target takes [1] shadow damage each turn. Reduces healing taken by [0]%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Garrote

`pendente`


**Texto:** Deals *0 weapon damage. Applies {STA=Disabled} to the target for 1 turn and applies 3 stacks of {STA=Bleeding}.


**expr:** `Source.AttackPower * 1f * Source.DamageModPhysical`


**acao `Garrote`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1f`


**status `Bleeding`:** efeitos=`ResistPhysical:Base:-5, BleedingDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Bleeding", "TargetStored[\"PhysicalDamage\"] = Source.AttackPower * .05f"))` classe=debuff


> Target takes [1] physical damage for each hex they move. Reduces Physical Resistance by [0]%.


**status `Disabled`:** efeitos=`Disabled:Set:1` classe=buff


> Cannot perform actions.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Hidden Blade · **PASSIVA**

`pendente`


**Texto:** Increases @Critical Hit Damage@ for your basic attack by 75%. 


**attr:** `CritDamageTreeBasic:Base:75,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Steal Action

`corrigido`


**Texto:** Steals the target's action granting 1 additional action this turn. Applies {STA=Disabled} to the target for 1 turn.  Applies {STA=Exhaustion}.


**acao `Steal Action`:** `Source['ActionPoints'] = Source['ActionPoints'] + (Source['RecentlyHasted'] == 0 ? 1 : 0)`


**status `Disabled`:** efeitos=`Disabled:Set:1` classe=buff


> Cannot perform actions.


**status `Exhaustion`:** efeitos=`RecentlyHasted:Set:1` classe=buff


> Cannot receive additional actions points.  Caused by receiving additional action points this turn.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Steal Status

`pendente`


**Texto:** Steals a random positive status from the target.


**acao `Steal Status`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Uncanny Evasion

`pendente`


**Texto:** Gain 100% @dodge chance@ for the next attack. Increases @Counter Attack Damage@ by 50% for 1 turn.


**acao `Uncanny Evasion`:** `Target['EvasionCharges'] = 1`


**conferir:** 100%, 50% — sem par no codigo dumpado


## T4 Calculated Risk · **PASSIVA**

`pendente`


**Texto:** When you are hit you have a 100% chance to cast @evasion@. 1 turn cooldown.


**conferir:** 100% — sem par no codigo dumpado


## T4 Contaminated Wound · **PASSIVA**

`pendente`


**Texto:** Increases the duration of {STA=Poisoned} and {STA=Bleeding} effects you've applied by 2 turns.


**attr:** `ContaminatedWound:Set:1,`


**status `Bleeding`:** efeitos=`ResistPhysical:Base:-5, BleedingDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Bleeding", "TargetStored[\"PhysicalDamage\"] = Source.AttackPower * .05f"))` classe=debuff


> Target takes [1] physical damage for each hex they move. Reduces Physical Resistance by [0]%.


**status `Poisoned`:** efeitos=`HealingReceivedBonus:Base:-1, PoisonDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Poisoned", "TargetStored[\"ShadowDamage\"] = Source.SpellPower(\"Shadow\") * .1f")), ContagionLevel:Base:Source["ContagionSource"] > 0 ? 1 : 0` classe=debuff


> Target takes [1] shadow damage each turn. Reduces healing taken by [0]%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Gore

`pendente`


**Texto:** Deals *0 weapon damage. Applies {STA=Disabled} for 1 turn. 


**expr:** `Source.AttackPower * 1.6f * Source.DamageModPhysical`


**acao `Gore`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1.6f`


**status `Disabled`:** efeitos=`Disabled:Set:1` classe=buff


> Cannot perform actions.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Master Assassin · **PASSIVA**

`pendente`


**Texto:** Always deal the maximum damage within a damage range. 


**attr:** `MasterAssassin:Set:1,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Rupture

`pendente`


**Texto:** Deals *0 weapon damage. Applies {STA=Disabled} for 1 turn and applies 6 stacks of {STA=Bleeding}.


**expr:** `Source.AttackPower * 1f * Source.DamageModPhysical`


**acao `Rupture`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1f`


**status `Bleeding`:** efeitos=`ResistPhysical:Base:-5, BleedingDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Bleeding", "TargetStored[\"PhysicalDamage\"] = Source.AttackPower * .05f"))` classe=debuff


> Target takes [1] physical damage for each hex they move. Reduces Physical Resistance by [0]%.


**status `Disabled`:** efeitos=`Disabled:Set:1` classe=buff


> Cannot perform actions.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Shadow Walk

`corrigido`


**Texto:** Teleport through the shadows. Applies {STA=Stealth} for this turn.  Unaffected by increased range modifiers.


**acao `Shadow Walk`:** `-`


**status `Stealth`:** efeitos=`Hidden:Set:1, UntargetableByEnemies:Set:1` classe=buff


> Invisible. Attacking from Stealth has 100% critical hit chance.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Smoke Bomb

`pendente`


**Texto:** Increases @dodge chance@ by 50% for friendly characters in smoke.


**acao `Smoke Bomb`:** `-`


**conferir:** 50% — sem par no codigo dumpado


## T5 Deathblow

`pendente`


**Texto:** Deals *1 weapon damage. Critical hits deal an additional 200% @Critical Hit Damage@.


**expr:** `Source.AttackPower * 2f * Source.DamageModPhysical`


**acao `Deathblow`:** `SourceStored['AdditionalCritDamage'] = 200; TargetStored[Source.WeaponDamageType] = Source.AttackPower * 2f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Sleight of Hand

`pendente`


**Texto:** Steal all of the target's beneficial statuses while giving the target all your negative statuses. 


**acao `Sleight of Hand`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Soft Step · **PASSIVA**

`corrigido`


**Texto:** Moving 5 hexes in a row grants {STA=Stealth} for your current turn.  Your character no longer takes attacks of opportunity.  


**attr:** `OpportunityAttackImmunity:Set:1,`


**status `Stealth`:** efeitos=`Hidden:Set:1, UntargetableByEnemies:Set:1` classe=buff


> Invisible. Attacking from Stealth has 100% critical hit chance.


**conferir:** 5 hex — sem par no codigo dumpado


## T5 Tricks of the Trade · **PASSIVA**

`pendente`


**Texto:** Reduces the cooldown of all abilities by 1.


**attr:** `CooldownMod:Base:-1,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok

