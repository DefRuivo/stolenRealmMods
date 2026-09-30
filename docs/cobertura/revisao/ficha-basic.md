# Ficha de revisao — arvore **Basic** (15 skills)

> Gerado por `tools/verify_tree.py`. Junta o TEXTO da tooltip com o que o jogo
> CALCULA. A ultima linha de cada ficha (`conferir`) lista o que **nao** tem par no
> codigo — e o que precisa de olho humano ou triangulacao externa, nao veredito.


## T0 Melee Attack · ⚠ **nome repetido** (4 variantes — confira o `attr` pelo `skid` em `skills-detalhe.csv`)

`pendente`


**Texto:** Deals *0 weapon damage to target. 


**expr:** `Source.AttackPower * 1f * Source.DamageModBasic`


**acao `Melee Attack Healing`:** `TargetStored[Source.WeaponDamageType] = Source.BasicAttackPower`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T0 Melee Attack · ⚠ **nome repetido** (4 variantes — confira o `attr` pelo `skid` em `skills-detalhe.csv`)

`pendente`


**Texto:** Deals *0 weapon damage to target 3 times.  Applies {STA=Bleeding} on hit.


**expr:** `Source.AttackPower * 1f * Source.DamageModBasic`


**acao `Melee Attack Healing`:** `TargetStored[Source.WeaponDamageType] = Source.BasicAttackPower`


**status `Bleeding`:** efeitos=`ResistPhysical:Base:-5, BleedingDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Bleeding", "TargetStored[\"PhysicalDamage\"] = Source.AttackPower * .05f"))` classe=debuff


> Target takes [1] physical damage for each hex they move. Reduces Physical Resistance by [0]%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T0 Melee Attack · ⚠ **nome repetido** (4 variantes — confira o `attr` pelo `skid` em `skills-detalhe.csv`)

`pendente`


**Texto:** Deals *0 weapon damage to target 2 times.  Applies {STA=Bleeding} on hit.


**expr:** `Source.AttackPower * 1f * Source.DamageModBasic`


**acao `Melee Attack Healing`:** `TargetStored[Source.WeaponDamageType] = Source.BasicAttackPower`


**status `Bleeding`:** efeitos=`ResistPhysical:Base:-5, BleedingDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Bleeding", "TargetStored[\"PhysicalDamage\"] = Source.AttackPower * .05f"))` classe=debuff


> Target takes [1] physical damage for each hex they move. Reduces Physical Resistance by [0]%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T0 Melee Attack · ⚠ **nome repetido** (4 variantes — confira o `attr` pelo `skid` em `skills-detalhe.csv`)

`pendente`


**Texto:** Deals *0 weapon damage to target.   When targeting an ally, heals for *0.


**expr:** `Source.AttackPower * 1f * Source.DamageModBasic`


**acao `Melee Attack Healing`:** `TargetStored[Source.WeaponDamageType] = Source.BasicAttackPower`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T0 Ranged Attack · ⚠ **nome repetido** (2 variantes — confira o `attr` pelo `skid` em `skills-detalhe.csv`)

`pendente`


**Texto:** Deals *0 weapon damage to target. 


**expr:** `Source.AttackPower * 1f * Source.DamageModBasic`


**acao `Ranged Attack Healing`:** `TargetStored[Source.WeaponDamageType] = Source.BasicAttackPower`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T0 Ranged Attack · ⚠ **nome repetido** (2 variantes — confira o `attr` pelo `skid` em `skills-detalhe.csv`)

`pendente`


**Texto:** Deals *0 weapon damage to target.   When targeting an ally, heals for *0.


**expr:** `Source.AttackPower * 1f * Source.DamageModBasic`


**acao `Ranged Attack Healing`:** `TargetStored[Source.WeaponDamageType] = Source.BasicAttackPower`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T0 Staff Attack · ⚠ **nome repetido** (2 variantes — confira o `attr` pelo `skid` em `skills-detalhe.csv`)

`pendente`


**Texto:** Deals *0 weapon damage to target. 


**expr:** `Source.AttackPower * 1f * Source.DamageModBasic`


**acao `Staff Attack Healing`:** `TargetStored['Healing'] = Source.BasicAttackPower`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T0 Staff Attack · ⚠ **nome repetido** (2 variantes — confira o `attr` pelo `skid` em `skills-detalhe.csv`)

`pendente`


**Texto:** Heals target ally for *0.    When targeting an enemy, deals *0 Holy Damage.


**expr:** `Source.AttackPower * 1f * Source.DamageModBasic`


**acao `Staff Attack Healing`:** `TargetStored['Healing'] = Source.BasicAttackPower`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T0 Unarmed Attack · ⚠ **nome repetido** (2 variantes — confira o `attr` pelo `skid` em `skills-detalhe.csv`)

`pendente`


**Texto:** Deals *0 weapon damage to target. 


**expr:** `Source.AttackPower * .5f * Source.DamageModBasic`


**acao `Unarmed Attack Healing`:** `TargetStored['Healing'] = Source.BasicAttackPower`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T0 Unarmed Attack · ⚠ **nome repetido** (2 variantes — confira o `attr` pelo `skid` em `skills-detalhe.csv`)

`pendente`


**Texto:** Heals target ally for *0.    When targeting an enemy, deals *0 Holy Damage.


**expr:** `Source.AttackPower * .5f * Source.DamageModBasic`


**acao `Unarmed Attack Healing`:** `TargetStored['Healing'] = Source.BasicAttackPower`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Flame Slash

`pendente`


**Texto:** Slash nearby targets dealing *0 fire damage to all enemies.


**expr:** `Source.SpellPower() * .5f * Source.DamageModFire`


**acao `Flame Slash`:** `TargetStored['FireDamage'] = Source.AttackPower * 1.2f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Holy Slash

`pendente`


**Texto:** Slash nearby targets dealing *0 holy damage to all enemies and healing *1 to all allies in range.


**danoExpr:** `TargetStored['HolyDamage'] = Source.AttackPower * 1.2f; TargetStored['Healing'] = Source.AttackPower * 1.5f`


**acao `Dragonkin Holy Slash`:** `TargetStored['HolyDamage'] = Source.AttackPower * 1.2f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Ice Slash

`pendente`


**Texto:** Slash nearby targets dealing *0 cold damage to all enemies.


**expr:** `Source.SpellPower() * .5f * Source.DamageModFire`


**acao `Frost Slash`:** `TargetStored['ColdDamage'] = Source.AttackPower * 1.2f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Shadow Claw

`pendente`


**Texto:** Slash nearby targets dealing *0 shadow damage to all enemies in range.


**expr:** `Source.SpellPower('Shadow') * 1.6f * Source.DamageModShadow`


**acao `Shadow Slash`:** `TargetStored['ShadowDamage'] = Source.AttackPower * 1.2f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Thunder Slash

`pendente`


**Texto:** Slash nearby targets dealing *0 lightning damage to all enemies.


**expr:** `Source.SpellPower() * .5f * Source.DamageModFire`


**acao `Thunder Slash`:** `TargetStored['LightningDamage'] = Source.AttackPower * 1.2f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok

