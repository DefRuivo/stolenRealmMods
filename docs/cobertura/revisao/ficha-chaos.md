# Ficha de revisao — arvore **Chaos** (33 skills)

> Gerado por `tools/verify_tree.py`. Junta o TEXTO da tooltip com o que o jogo
> CALCULA. A ultima linha de cada ficha (`conferir`) lista o que **nao** tem par no
> codigo — e o que precisa de olho humano ou triangulacao externa, nao veredito.


## T1 Chaos Crash

`pendente`


**Texto:** Hurls a bolt of chaos dealing damage to a single target. Every damage type has a 50% chance to deal *0 damage.


**danoExpr:** `TargetStored['PhysicalDamage'] = Source.SpellPower() * 0.5f`


**acao `Chaos Crash`:** `TargetStored['ColdDamage'] = Source.GetRollResult(50) ? Source.SpellPower('Cold') * 0.5f : 0; TargetStored['HolyDamage'] = Source.GetRollResult(50) ? Source.SpellPower('Light') * 0.5f : 0; TargetStore`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Chaos Curse

`pendente`


**Texto:** Curses the target to take damage. Each element has a @50%@ chance to deal *0 damage every turn.


**danoExpr:** `TargetStored['PhysicalDamage'] = Source.SpellPower() * 0.13f`


**acao `Chaos Curse`:** `-`


**conferir:** 50% — sem par no codigo dumpado


## T1 Disruption I · **PASSIVA**

`pendente`


**Texto:** 4% chance to negate all damage when taking damage.


**attr:** `IgnoreDamageChance:Base:4,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Omnism I · **PASSIVA**

`pendente`


**Texto:** Increases the effectiveness of shrines by 8%.


**attr:** `ShrineEffectBonus:Base:8,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Sustenance I · **PASSIVA**

`pendente`


**Texto:** Consuming any Globule heals you for 8% of max life and mana.


**conferir:** 8% — sem par no codigo dumpado


## T1 Switcheroo

`pendente`


**Texto:** Swap places with an @Enemy@, @Ally@, or @Object@.


**acao `Switcheroo`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Telekinesis

`pendente`


**Texto:** Moves any @Object@ within 8 hexes.


**acao `Telekinesis`:** `-`


**conferir:** 8 hex — sem par no codigo dumpado


## T2 Chaos Cut

`pendente`


**Texto:** Summons a whirling blade of chaos in a line. Every damage type has a 50% chance to deal *0 damage.


**danoExpr:** `TargetStored['PhysicalDamage'] = Source.SpellPower() * 0.4f`


**acao `Chaos Cut`:** `TargetStored['ColdDamage'] = Source.GetRollResult(50) ? Source.SpellPower('Cold') * 0.4f : 0; TargetStored['HolyDamage'] = Source.GetRollResult(50) ? Source.SpellPower('Light') * 0.4f : 0; TargetStore`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Displacement · **PASSIVA**

`pendente`


**Texto:** Teleport randomly when taking damage.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Disruption II · **PASSIVA**

`pendente`


**Texto:** 6% chance to negate all damage when taking damage.


**attr:** `IgnoreDamageChance:Base:6,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Helping

`sem-explicacao`


**Texto:** Offer your chaotic assistance to the target ally. Results may vary greatly...


**expr:** `Source.SpellPower() * .15f * Source.DamageModFire`


**acao `Helping`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Hurting

`sem-explicacao`


**Texto:** Chaotically harm the target enemy. Results may vary greatly...


**acao `Hurting`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Magic Hat I

`pendente`


**Texto:** Produce a random barrel on the target hex.


**expr:** `Source.SpellPower() * .15f * Source.DamageModFire`


**acao `Magic Hat I`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Omnism II · **PASSIVA**

`pendente`


**Texto:** Increases the effectiveness of shrines by an additional 12%.


**attr:** `ShrineEffectBonus:Base:20,`


**conferir:** 12% — sem par no codigo dumpado


## T2 Sustenance II · **PASSIVA**

`pendente`


**Texto:** Consuming any Globule heals you for 20% of max life and mana.


**conferir:** 20% — sem par no codigo dumpado


## T3 Affinity · **PASSIVA**

`pendente`


**Texto:** Each time you deal damage or healing with a specific element gain a stacking buff that increases your damage or healing with that element by 2%. Stacks. Lasts the duration of battle.


**conferir:** 2% — sem par no codigo dumpado


## T3 Aid · **PASSIVA**

`sem-explicacao`


**Texto:** Healing an ally has a 10% chance to apply Helping.


**conferir:** 10% — sem par no codigo dumpado


## T3 Chaos Cloud

`pendente`


**Texto:** Summons a cloud of chaos that strikes 3 times. At every strike each damage type has a @50%@ chance to deal *0 damage.


**danoExpr:** `TargetStored['PhysicalDamage'] = Source.SpellPower() * 0.18f`


**acao `Chaos Cloud`:** `TargetStored['ColdDamage'] = Source.GetRollResult(50) ? Source.SpellPower('Cold') * 0.18f : 0; TargetStored['HolyDamage'] = Source.GetRollResult(50) ? Source.SpellPower('Light') * 0.18f : 0; TargetSto`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Disperse

`pendente`


**Texto:** Teleports all enemies within 3 hexes of you to any random hex 4 to 8 hexes from you. Applies a 1 turn slow.


**expr:** `Source.SpellPower() * 1.2f * Source.DamageModLightning`


**acao `Disperse`:** `-`


**conferir:** 3 hex, 8 hex — sem par no codigo dumpado


## T3 Harm · **PASSIVA**

`sem-explicacao`


**Texto:** Damaging an Enemy has a 10% chance to apply Hurting.


**conferir:** 10% — sem par no codigo dumpado


## T3 Magic Hat II

`pendente`


**Texto:** Produce a random Shrine on the target hex. The shrine is destructable and moveable.


**expr:** `Source.SpellPower() * .15f * Source.DamageModFire`


**acao `Magic Hat II`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Variety I · **PASSIVA**

`pendente`


**Texto:** Each turn gain two random buffs that increase the damage of a random element by @40@% this turn. 


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Benevolence

`sem-explicacao`


**Texto:** Applies @Helping@ to all allies.


**acao `Benevolence`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Chaos Touch

`sem-explicacao`


**Texto:** Enchant an ally with a random chaos modifier.


**acao `Chaos Touch`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Fabricate · **PASSIVA**

`pendente`


**Texto:** When you consume a globule you have a 50% chance to spawn a random globule within a 6 hex area of you.


**conferir:** 50%, 6 hex — sem par no codigo dumpado


## T4 Magic Hat III

`pendente`


**Texto:** Produce a random Globule on the target hex.


**expr:** `Source.SpellPower() * .15f * Source.DamageModFire`


**acao `Magic Hat III`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Malevolence

`sem-explicacao`


**Texto:** Applies @Hurting@ to all enemies.


**acao `Malevolence`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Touch of Chaos

`sem-explicacao`


**Texto:** Enchant an ally with a random Chaos Modifier.


**acao `Touch of Chaos`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Variety II · **PASSIVA**

`pendente`


**Texto:** Each turn gain two random buffs that increase the damage of a specfic element by 60% this turn. 


**conferir:** 60% — sem par no codigo dumpado


## T5 Chaos Crush

`pendente`


**Texto:** Call down chaos to crush your enemies. Deals between *0 and *1 damage within 2 hexes. Always hits with all damage types.


**expr:** `Source.SpellPower() * 1.6f * Source.DamageModFire; Source.SpellPower() * .25f * Source.DamageModFire`


**danoExpr:** `TargetStored['PhysicalDamage'] = Source.SpellPower() * 1.2f; TargetStored['PhysicalDamage'] = Source.SpellPower() * 6f`


**acao `Chaos Crush`:** `-`


**conferir:** 2 hex — sem par no codigo dumpado


## T5 Perturb · **PASSIVA**

`pendente`


**Texto:** Each time a damage or healing skill is cast, it receives a random effectiveness modifier from 50% up to 250%. 


**attr:** `FickleFlame:Set:1,`


**conferir:** 250%, 50% — sem par no codigo dumpado


## T5 Replicate

`pendente`


**Texto:** Creates a clone of yourself that can cast your abilities. The Replicate Clone explodes for damage on death, each element has a @50%@ chance to deal *0 damage.


**danoExpr:** `TargetStored['PhysicalDamage'] = Source.SpellPower() * 0.5f`


**acao `Replicate`:** `-`


**conferir:** 50% — sem par no codigo dumpado


## T5 Reverberate · **PASSIVA**

`pendente`


**Texto:** When you take a @Free Action@ or @Action@ you have a 33% chance explode in chaos dealing all types of damage and healing.


**conferir:** 33% — sem par no codigo dumpado

