# Ficha de revisao — arvore **Lightning** (30 skills)

> Gerado por `tools/verify_tree.py`. Junta o TEXTO da tooltip com o que o jogo
> CALCULA. A ultima linha de cada ficha (`conferir`) lista o que **nao** tem par no
> codigo — e o que precisa de olho humano ou triangulacao externa, nao veredito.


## T1 Dazzling Darts

`pendente`


**Texto:** Shoots 3 darts of electricity each dealing *0 lightning damage.


**expr:** `Source.SpellPower() * .4f * Source.DamageModLightning`


**acao `Dazzling Darts`:** `TargetStored['LightningDamage'] = Source.SpellPower('Lightning') * .4f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Lightning Breath

`pendente`


**Texto:** Breath lightning dealing *0 lightning damage to all enemies in a cone. 


**expr:** `Source.SpellPower() * .5f * Source.DamageModLightning`


**acao `Lightning Breath`:** `TargetStored['LightningDamage'] = Source.SpellPower('Lightning') * 1.6f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Lightning Shield

`pendente`


**Texto:** Increases @Lightning Resistance@ by 10%. Attackers take *0 lightning damage.


**expr:** `Source.SpellPower() * .15f * Source.DamageModLightning`


**acao `Lightning Shield`:** `TargetStored['LightningDamage'] = Source.SpellPower('Lightning') * .15f`


**conferir:** 10% — sem par no codigo dumpado


## T1 Shock

`pendente`


**Texto:** Reaches out and shocks the target dealing *0 lightning damage. Applies {STA=Disabled} to the target.


**expr:** `Source.SpellPower() * .6f * Source.DamageModLightning`


**acao `Shock`:** `TargetStored['LightningDamage'] = Source.SpellPower('Lightning') * .6f`


**status `Disabled`:** efeitos=`Disabled:Set:1` classe=buff


> Cannot perform actions.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Storm Borne · **PASSIVA**

`pendente`


**Texto:** Increases @lightning resistance@ by 10%.


**attr:** `ResistLightning:Base:10,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Storm Weathered I · **PASSIVA**

`pendente`


**Texto:** Increase all @elemental resistances@ by 5%.


**attr:** `ResistCold:Base:5, ResistFire:Base:5, ResistLightning:Base:5,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Stormbringer I · **PASSIVA**

`pendente`


**Texto:** Increases @critical hit chance@ by 5%.


**attr:** `CritChance:Base:5,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Discharge

`pendente`


**Texto:** Deals *0 lightning damage within 3 hexes of the caster. 


**expr:** `Source.SpellPower() * .9f * Source.DamageModLightning`


**acao `Discharge`:** `TargetStored['LightningDamage'] = Source.SpellPower('Lightning') * .9f`


**conferir:** 3 hex — sem par no codigo dumpado


## T2 Enchant Lightning

`pendente`


**Texto:** Enchants the target's weapon to add *0 lightning damage to attacks. 


**expr:** `Source.SpellPower() * .15f * Source.DamageModLightning`


**danoExpr:** `TargetStored['LightningDamage'] = Source.SpellPower('Lightning') * .15f`


**acao `Enchant Lightning`:** `Target['EnchantLightningValue'] = Source.GetCustomActionDamage('Enchant Lightning', 'TargetStored[\'LightningDamage\'] = Source.SpellPower(\'Lightning\') * .15f')`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Gathering Storm · **PASSIVA**

`pendente`


**Texto:** Increases @maximum mana@ by 20%.


**attr:** `MaxMana:Percentage:20,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Storm Weathered II · **PASSIVA**

`pendente`


**Texto:** Increase all @elemental resistances@ by an additional 8%.


**attr:** `ResistCold:Base:8, ResistFire:Base:8, ResistLightning:Base:8,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Stormbringer II · **PASSIVA**

`pendente`


**Texto:** Increases @critical hit chance@ by an additional 8%.


**attr:** `CritChance:Base:8,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Teleport Self

`corrigido`


**Texto:** Teleports the caster to the target location in a flash of lightning.  Unaffected by increased range modifiers.


**acao `Teleport Self`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Twister

`revisado`


**Texto:** Summons a raging tempest that deals *0 lightning damage in a line.  Targets hit are {STA=Crippled} for 2 turns.


**expr:** `Source.SpellPower() * 1.2f * Source.DamageModLightning`


**acao `Twister`:** `TargetStored['LightningDamage'] = Source.SpellPower('Lightning') * 1.2f`


**status `Crippled`:** efeitos=`TurnFreeMovementPoints:Base:-1` classe=debuff


> Reduces @Movement Points@ by @1@ per stack.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Aura of Lightning

`pendente`


**Texto:** Each time an action is made by an enemy within the aura they suffer *0 lightning damage. 


**expr:** `Source.SpellPower() * .4f * Source.DamageModLightning`


**acao `Aura of Lightning`:** `TargetStored['LightningDamage'] = Source.SpellPower('Lightning') * .4f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Chain Lightning

`pendente`


**Texto:** Conjures a lightning bolt that chains up to 5 enemies near the target dealing *0 lightning damage to each target.  


**expr:** `Source.SpellPower() * .8f * Source.DamageModLightning`


**acao `Chain Lightning`:** `TargetStored['LightningDamage'] = Source.SpellPower('Lightning') * .8f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Mana Shield · **PASSIVA**

`pendente`


**Texto:** 90% of the damage taken is lost in mana instead of health.


**attr:** `ManaShield:Base:90,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Storm Brewing · **PASSIVA**

`pendente`


**Texto:** Each stack of @shocked@ you've applied increases your @critical hit chance@ by 1%.


**attr:** `CritChance:Base:Source.GetNumStatusesCaused("GL-Shocked") * 1,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Teleport Other

`corrigido`


**Texto:** Teleports the target to the location of your choosing in a flash of lightning.  Unaffected by increased range modifiers.


**acao `Teleport Other`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Thunder Bolt

`pendente`


**Texto:** Summon lightning from the sky to strike an area dealing *0 lightning damage. 


**expr:** `Source.SpellPower() * 1.1f * Source.DamageModLightning`


**acao `Thunder Bolt`:** `TargetStored['LightningDamage'] = Source.SpellPower('Lightning') * 1.1f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Heavy Rains · **PASSIVA**

`pendente`


**Texto:** Each point of @intelligence@ now grants .1% @critical hit chance@ and 1% @critical hit damage@.


**attr:** `CritDamage:Base:Source["Intelligence"] * 1, CritChance:Base:Source["Intelligence"] * .1f,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Overload

`pendente`


**Texto:** Gives the target 100% Critical Hit Chance for 1 turn. 


**acao `Overload`:** `-`


**conferir:** 100% — sem par no codigo dumpado


## T4 Recharge · **PASSIVA**

`pendente`


**Texto:** You have a 33% chance to completely refund the mana cost spent while using abilities. When mana is refunded this way, a random ability will have its cooldown lowered by 1.


**attr:** `Recharge:Set:1,`


**conferir:** 33% — sem par no codigo dumpado


## T4 Shocking Shackles

`corrigido`


**Texto:** Deals *0 lightning damage.  Applies {STA=Stunned}.


**expr:** `Source.SpellPower('Lightning') * 1f * Source.DamageModLightning`


**acao `Shocking Shackles`:** `TargetStored['LightningDamage'] = Source.SpellPower('Lightning') * 2f`


**status `Stunned`:** efeitos=`Rooted:Set:1, Disabled:Set:1` classe=buff


> Stunned.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Static Field

`pendente`


**Texto:** Averages all the current health percentages of targets within 3 hexes and redistributes them to be even. 


**acao `Static Field`:** `TargetStored['LightningDamage'] = Target.LastHealthRatio > SelectedCell.GetAverageHealthRatioInRange(2) ? Target['Health'] -  Target['MaxHealth'] * Mathf.Max(.3f, SelectedCell.GetAverageHealthRatioInR`


**conferir:** 3 hex — sem par no codigo dumpado


## T4 Thunder Storm

`pendente`


**Texto:** Summon a thunderstorm over a large area that deals *0 lightning damage every turn to enemies within it's range.


**expr:** `Source.SpellPower('Lightning') * .9f * Source.DamageModLightning`


**acao `Thunder Storm`:** `TargetStored['LightningDamage'] = Source.SpellPower('Lightning') * .9f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Conduit · **PASSIVA**

`pendente`


**Texto:** Gain an additional action each turn.


**attr:** `ExtraTurnActionPoints:Base:1,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Energy Cannon

`pendente`


**Texto:** Deals *0 lightning damage in a 6 hex line 10 times.


**expr:** `Source.SpellPower() * .2f * Source.DamageModLightning`


**acao `Energy Cannon`:** `TargetStored['LightningDamage'] = Source.SpellPower('Lightning') * .2f`


**conferir:** 6 hex — sem par no codigo dumpado


## T5 Thunder Struck · **PASSIVA**

`pendente`


**Texto:** Your lightning damage has a 10% chance to conjure a thunderbolt on a random enemy dealing *0 lightning damage within 2 hexes of its blast.


**expr:** `Source.SpellPower('Lightning') * 1.1f * Source.DamageModLightning`


**conferir:** 10%, 2 hex — sem par no codigo dumpado


## T5 Thunder Wrath

`corrigido`


**Texto:** Summons 4 thunder bolts targeting enemies at random within a 10 hex radius.  Each bolt deals *0 lightning damage to foes within 3 hexes of its blast.


**expr:** `Source.SpellPower('Lightning') * 1.0f * Source.DamageModLightning`


**acao `Thunder Wrath`:** `TargetStored['LightningDamage'] = Source.SpellPower('Lightning') * 1.0f`


**conferir:** 10 hex, 3 hex — sem par no codigo dumpado

