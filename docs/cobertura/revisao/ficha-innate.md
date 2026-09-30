# Ficha de revisao — arvore **Innate** (10 skills)

> Gerado por `tools/verify_tree.py`. Junta o TEXTO da tooltip com o que o jogo
> CALCULA. A ultima linha de cada ficha (`conferir`) lista o que **nao** tem par no
> codigo — e o que precisa de olho humano ou triangulacao externa, nao veredito.


## T1 Blood Howl

`corrigido`


**Texto:** Howl causing *0 physical damage to all enemies within 2 hexes.  Applies a debuff that causes all attackers to lifesteal for [1]% against this target for 2 turns.


**expr:** `Source.AttackPower * .8f * Source.DamageModPhysical; 4`


**acao `Blood Howl`:** `TargetStored['PhysicalDamage'] = Source.AttackPower * 1.1f`


**status `Howl`:** efeitos=`DamageMod:Base:-20` classe=debuff


> Damage dealt reduced by 20%.


**conferir:** 2 hex — sem par no codigo dumpado


## T1 Dire Howl

`corrigido`


**Texto:** Howl causing *0 physical damage to all enemies within 2 hexes.  Applies a debuff that causes all attackers to lifesteal for [1]% against this target for 2 turns.


**expr:** `Source.AttackPower * 1.2f * Source.DamageModPhysical; 6`


**acao `Greater Blood Howl`:** `TargetStored['PhysicalDamage'] = Source.AttackPower * 1.6f`


**status `Howl`:** efeitos=`DamageMod:Base:-20` classe=debuff


> Damage dealt reduced by 20%.


**conferir:** 2 hex — sem par no codigo dumpado


## T1 Dismiss Shapeshift

`pendente`


**Texto:** Dismiss your active shapeshift.


**acao `Dismiss Shapeshift`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Fire Breath

`pendente`


**Texto:** Breath fire dealing *0 fire damage to all enemies in a cone. 


**expr:** `Source.SpellPower() * .5f * Source.DamageModFire`


**acao `Fire Breath`:** `TargetStored['FireDamage'] = Source.SpellPower('Fire') * 1.6f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Frost Breath

`pendente`


**Texto:** Deals *0 cold damage each turn.


**expr:** `Source.SpellPower() * .5f * Source.DamageModCold`


**acao `Frost Breath`:** `TargetStored['ColdDamage'] = Source.SpellPower('Cold') * 1.6f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Move Object

`pendente`


**Texto:** Transport a movable object in the battlefield.


**acao `Move Object`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Cursed Bite

`pendente`


**Texto:** Deals *0 weapon damage and lowers target's @Healing@ received by 50% for 2 turns.


**expr:** `Source.AttackPower * 1.7f * Source.DamageModPhysical`


**acao `Cursed Bite`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1.7f`


**conferir:** 50% — sem par no codigo dumpado


## T2 Dire Bite

`pendente`


**Texto:** Deals *0 weapon damage and lowers target's @Healing@ received by 50% for 2 turns.


**expr:** `Source.AttackPower * 1.7f * Source.DamageModPhysical`


**acao `Greater Cursed Bite`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 2.2f`


**conferir:** 50% — sem par no codigo dumpado


## T2 Thunder Blast

`pendente`


**Texto:** Conjure a storm of lightning dealing *0 lightning damage to all targets in range. Applies 10 stacks of {STA=Shocked}.


**expr:** `Source.SpellPower() * 1.1f * Source.DamageModFire`


**acao `Dragonkin Thunder Blast`:** `TargetStored['LightningDamage'] = Source.SpellPower('Lightning') * 2.1f`


**status `Shocked`:** efeitos=`ResistLightning:Base:-25` classe=debuff


> Reduces @Lightning Resistance@ by @25%@ per stack.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Shapeshift Vampire Bat

`pendente`


**Texto:** Shapeshift into a @Vampire Bat@. Gain new abilities. @Movement@ increased. Immune to @attacks of opportunity@.


**acao `Shapeshift Box`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok

