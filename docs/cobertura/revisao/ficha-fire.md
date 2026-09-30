# Ficha de revisao — arvore **Fire** (32 skills)

> Gerado por `tools/verify_tree.py`. Junta o TEXTO da tooltip com o que o jogo
> CALCULA. A ultima linha de cada ficha (`conferir`) lista o que **nao** tem par no
> codigo — e o que precisa de olho humano ou triangulacao externa, nao veredito.


## T1 Burning Reach · **PASSIVA**

`corrigido`


**Texto:** Increase the range of all non-melee abilites by 1 hex. 


**attr:** `RangeTypeAdderRanged:Base:1,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Fire Borne · **PASSIVA**

`pendente`


**Texto:** Increases @fire resistance@ by 10%.


**attr:** `ResistFire:Base:10,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Fire Shield

`corrigido`


**Texto:** Wreaths the target in flame granting 10% @fire resistance@.  Attackers take *0 fire damage.


**expr:** `Source.SpellPower() * .15f * Source.DamageModFire`


**acao `Fire Shield`:** `TargetStored['FireDamage'] = Source.SpellPower('Fire') * .15f`


**conferir:** 10% — sem par no codigo dumpado


## T1 Fireblast

`pendente`


**Texto:** Hurls a bolt of fire dealing *0 fire damage to a single target. 


**expr:** `Source.SpellPower() * 1.5f * Source.DamageModFire`


**acao `Fireblast`:** `TargetStored['FireDamage'] = Source.SpellPower('Fire') * 1.5f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Hot Head I · **PASSIVA**

`pendente`


**Texto:** Increase all Damage and Healing by 8%. 


**attr:** `DamageMod:Base:8,`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Immolate

`pendente`


**Texto:** Burns the target for *0 fire damage each turn.


**expr:** `Source.SpellPower() * .5f * Source.DamageModFire`


**acao `Immolate`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Burning Ground

`pendente`


**Texto:** Ignite an area in flames. Enemies take *0 fire damage each turn they remain on burning ground.


**expr:** `Source.SpellPower() * .5f * Source.DamageModFire`


**acao `Burning Ground`:** `-`


**status `Ignite`:** efeitos=`-` classe=indefinido


> Targets in burning ground receive *0 fire damage.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Cauterize

`pendente`


**Texto:** Removes all negative statuses from friendly target but inflicts 10% of target's maximum health as fire damage. Can be used when Disabled.


**acao `Cauterize`:** `TargetStored['FireDamage'] = Mathf.Min(Target.Health - 1, Target['MaxHealth'] * .1f)`


**status `Disabled`:** efeitos=`Disabled:Set:1` classe=buff


> Cannot perform actions.


**conferir:** 10% — sem par no codigo dumpado


## T2 Enchant Fire

`pendente`


**Texto:** Enchants the target's weapon to add *0 fire damage to attacks. 


**expr:** `Source.SpellPower() * .15f * Source.DamageModFire`


**danoExpr:** `TargetStored['FireDamage'] = Source.SpellPower('Fire') * .15f`


**acao `Enchant Fire`:** `Target['EnchantFireValue'] = Source.GetCustomActionDamage('Enchant Fire', 'TargetStored[\'FireDamage\'] = Source.SpellPower(\'Fire\') * .15f')`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Fire Starter · **PASSIVA**

`pendente`


**Texto:** All enemies now start the battle with 4 stacks of @Heat@. 


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Fireball

`pendente`


**Texto:** Hurls a ball of flame dealing *0 fire damage to all targets in range.


**expr:** `Source.SpellPower() * 1.1f * Source.DamageModFire`


**acao `Fireball`:** `TargetStored['FireDamage'] = Source.SpellPower('Fire') * 1.1f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Hot Head II · **PASSIVA**

`pendente`


**Texto:** Increases Damage and Healing by an additional 12%. 


**attr:** `DamageMod:Base:12,`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Sun Fire

`corrigido`


**Texto:** Hurls a ball of flame dealing *0 fire damage to all targets in range. Applies 10 stacks of {STA=Heat}


**expr:** `Source.SpellPower() * 1.1f * Source.DamageModFire`


**acao `Dragonkin Sun Fire`:** `TargetStored['FireDamage'] = Source.SpellPower('Fire') * 2.2f`


**status `Heat`:** efeitos=`ResistCold:Base:-5, ResistFire:Base:-5, ResistLightning:Base:-5` classe=debuff


> Elemental resistance reduced by 5% per stack.  Lasts [0] turns.  Can stack up to 10 times.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Aura of Flame

`pendente`


**Texto:** Continually deals *0 fire damage to enemies within 3 hexes of your character.


**expr:** `Source.SpellPower() * .4f * Source.DamageModFire`


**acao `Aura Of Flame`:** `-`


**conferir:** 3 hex — sem par no codigo dumpado


## T3 Detonate

`pendente`


**Texto:** Deals *0 fire damage to all foes within 2 hexes of your character.


**expr:** `Source.SpellPower() * 1.6f * Source.DamageModFire`


**acao `Detonate`:** `TargetStored['FireDamage'] = Source.SpellPower('Fire') * 1.6f`


**conferir:** 2 hex — sem par no codigo dumpado


## T3 Fuel for the Flames I · **PASSIVA**

`pendente`


**Texto:** Increase the mana cost of all skills by 20% and increase the power of mana using skills by 40%.


**attr:** `ManaCostMod:Base:20, ManaPowerMod:Base:40,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Haste

`pendente`


**Texto:** Target gains an additional action this turn. Applies {STA=Exhaustion}.


**acao `Haste`:** `Target['ActionPoints'] = Target['ActionPoints'] + (Target['RecentlyHasted'] == 0 ? 1 : 0)`


**status `Exhaustion`:** efeitos=`RecentlyHasted:Set:1` classe=buff


> Cannot receive additional actions points.  Caused by receiving additional action points this turn.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Kindling · **PASSIVA**

`pendente`


**Texto:** Gain an additional action the first turn of battle. Applies {STA=Exhaustion}.


**attr:** `StartAPMod:Base:1,`


**status `Exhaustion`:** efeitos=`RecentlyHasted:Set:1` classe=buff


> Cannot receive additional actions points.  Caused by receiving additional action points this turn.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Lasting Flame · **PASSIVA**

`pendente`


**Texto:** @Heat@ lasts 2 addtional turns.


**attr:** `HeatDurationMod:Base:2,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Rune of Exploding

`pendente`


**Texto:** Place a rune on the selected hex. After 1 turn, it detonates dealing *0 fire damage to all enemies within 1 hex.


**acao `Rune of Exploding`:** `TargetStored['FireDamage'] = Source.SpellPower('Fire') * 2f`


**conferir:** 1 hex — sem par no codigo dumpado


## T4 Fever · **PASSIVA**

`pendente`


**Texto:** Mana costs are now paid in Health instead.


**attr:** `HealthAsManaCost:Set:100,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Fissure

`pendente`


**Texto:** Open the earth in a line spawning deadly fissures that deal *0 fire damage.


**expr:** `Source.SpellPower() * 2f * Source.DamageModFire`


**acao `Fissure`:** `TargetStored['FireDamage'] = Source.SpellPower('Fire') * 2f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Flash Fire · **PASSIVA**

`pendente`


**Texto:** Reduces the cooldown of all fire spells by 1. 


**attr:** `CooldownModFire:Base:-1,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Fuel for the Flames II · **PASSIVA**

`pendente`


**Texto:** Increase the mana cost of all skills by an additional 30% and increase the power of mana using skills by an additional 60%.


**attr:** `ManaCostMod:Base:30, ManaPowerMod:Base:60,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Meteor

`pendente`


**Texto:** Call down a ball of fire to smash your enemies. Deals *0 fire damage within 2 hexes. Fire remains on the impacted area dealing *1 fire damage per turn.


**expr:** `Source.SpellPower() * 1.6f * Source.DamageModFire; Source.SpellPower() * .25f * Source.DamageModFire`


**danoExpr:** `TargetStored['FireDamage'] = Source.SpellPower('Fire') * 1f; TargetStored['FireDamage'] = Source.SpellPower('Fire') * .6f`


**acao `Meteor`:** `TargetStored['FireDamage'] = Source.SpellPower('Fire') * 1.6f`


**conferir:** 2 hex — sem par no codigo dumpado


## T4 Overwhelming Power

`pendente`


**Texto:** Increases the damage of your next damaging action by 100%.


**acao `Overwhelming Power`:** `-`


**conferir:** 100% — sem par no codigo dumpado


## T5 Avatar of Flame · **PASSIVA**

`pendente`


**Texto:** Each stack of @heat@ now applies [0] fire damage to the target per turn.


**attr:** `AvatarOfFlame:Set:1,`


**expr:** `Source.GetCustomActionDamage('GL-HeatStatus', 'TargetStored[\'FireDamage\'] = Source.SpellPower(\'Fire\') * .2f')`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Fickle Flame · **PASSIVA**

`pendente`


**Texto:** Each time a damage or healing skill is cast, it receives a random effectiveness modifier from 50% up to 250%. 


**attr:** `FickleFlame:Set:1,`


**conferir:** 250%, 50% — sem par no codigo dumpado


## T5 Fire Storm

`pendente`


**Texto:** Hurls fire balls at 3 different targets dealing *0 fire damage within 2 hexes of each target.


**expr:** `Source.SpellPower() * 1.1f * Source.DamageModFire`


**acao `Fire Storm`:** `TargetStored['FireDamage'] = Source.SpellPower('Fire') * 1.1f`


**conferir:** 2 hex — sem par no codigo dumpado


## T5 Flame Lash · **PASSIVA**

`pendente`


**Texto:** Your fire spells deal 10% more damage per stack of heat on targets.


**attr:** `IncreasedFireDamagePerTargetHeatStack:Base:10,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Mass Haste

`pendente`


**Texto:** All allies gain an additional action this turn. Applies {STA=Exhaustion}.


**acao `Mass Haste`:** `Target['ActionPoints'] = Target['ActionPoints'] + (Target['RecentlyHasted'] == 0 ? 1 : 0)`


**status `Exhaustion`:** efeitos=`RecentlyHasted:Set:1` classe=buff


> Cannot receive additional actions points.  Caused by receiving additional action points this turn.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Meteor Shower

`pendente`


**Texto:** Summon a rain of meteors to bombard enemies within 4 hexes of the target location. Deals *0 fire damage 3 times.


**expr:** `Source.SpellPower('Fire') * .7f * Source.DamageModFire`


**acao `Meteor Shower`:** `TargetStored['FireDamage'] = Source.SpellPower('Fire') * .7f`


**conferir:** 4 hex — sem par no codigo dumpado

