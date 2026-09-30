# Ficha de revisao — arvore **Cold** (31 skills)

> Gerado por `tools/verify_tree.py`. Junta o TEXTO da tooltip com o que o jogo
> CALCULA. A ultima linha de cada ficha (`conferir`) lista o que **nao** tem par no
> codigo — e o que precisa de olho humano ou triangulacao externa, nao veredito.


## T1 Chilling Strike

`pendente`


**Texto:** The caster's hand becomes imbued with frost thrusting it at the target dealing *0 cold damage.


**expr:** `Source.SpellPower() * 1.5f * Source.DamageModCold`


**acao `Chilling Strike`:** `TargetStored['ColdDamage'] = Source.SpellPower('Cold') * 1.5f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Crystalize I · **PASSIVA**

`pendente`


**Texto:** Increases @Physical Resistance@ by 5%.


**attr:** `ResistPhysical:Base:5,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Freeze Earth

`pendente`


**Texto:** Freezes the ground in the target area applying 1 stack of Chilled to enemies that enter.


**acao `Freeze Earth`:** `-`


**status `Chilled`:** efeitos=`TurnFreeMovementPoints:Base:Target.CanBeEffectedByChilled ? (Target.ChilledEffectHalved ? -.5f : -1) : 0, DamageMod:Base:-(Source["ChilledDamageReduction"]), MaxHealth:Percentage:Source["Frostbite"] == 1 ? -5 : 0, Armor:Percentage:Source["InvulnerableWinter"] == 1 ? 5 : 0, MagicArmor:Percentage:Source["InvulnerableWinter"] == 1 ? 5 : 0` classe=debuff


> Movement points reduced by one per stack.  Lasts 2 turns.  Five stacks of Chilled freezes the target.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Frost Armor

`pendente`


**Texto:** Envelopes the caster in frost granting 10% @Cold Resistance@.   Attackers take *0 cold damage.


**expr:** `Source.SpellPower() * .15f * Source.DamageModCold`


**acao `Frost Armor`:** `TargetStored['ColdDamage'] = Source.SpellPower('Cold') * .15f`


**conferir:** 10% — sem par no codigo dumpado


## T1 Frost Borne · **PASSIVA**

`pendente`


**Texto:** Increases @cold resistance@ by 10%


**attr:** `ResistCold:Base:10,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Frost Shard

`pendente`


**Texto:** Impale your target on a shard of ice dealing *0 cold damage.


**expr:** `Source.SpellPower() * .9f * Source.DamageModCold`


**acao `Frost Shard`:** `TargetStored['ColdDamage'] = Source.SpellPower('Cold') * 1.3f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Frostbite I · **PASSIVA**

`pendente`


**Texto:** Your stacks of @chilled@ now reduce the targets damage by 2%.


**attr:** `ChilledDamageReduction:Base:2,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Break The Ice · **PASSIVA**

`pendente`


**Texto:** The first time you deal damage or healing in battle, it's effectiveness is increased by 100%.


**conferir:** 100% — sem par no codigo dumpado


## T2 Crystalize II · **PASSIVA**

`pendente`


**Texto:** Increases @Physical Resistance@ by an additional 10%.


**attr:** `ResistPhysical:Base:10,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Deep Freeze

`pendente`


**Texto:** Intense frost encircles your foe applying 5 stacks of {STA=Chilled} on the target.


**acao `Frozen Chains`:** `-`


**status `Chilled`:** efeitos=`TurnFreeMovementPoints:Base:Target.CanBeEffectedByChilled ? (Target.ChilledEffectHalved ? -.5f : -1) : 0, DamageMod:Base:-(Source["ChilledDamageReduction"]), MaxHealth:Percentage:Source["Frostbite"] == 1 ? -5 : 0, Armor:Percentage:Source["InvulnerableWinter"] == 1 ? 5 : 0, MagicArmor:Percentage:Source["InvulnerableWinter"] == 1 ? 5 : 0` classe=debuff


> Movement points reduced by one per stack.  Lasts 2 turns.  Five stacks of Chilled freezes the target.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Enchant Cold

`pendente`


**Texto:** Enchants the target's weapon to add *0 cold damage to attacks. 


**expr:** `Source.SpellPower() * .15f * Source.DamageModCold`


**danoExpr:** `TargetStored['ColdDamage'] = Source.SpellPower('Cold') * .15f`


**acao `Enchant Cold`:** `TargetStored['ColdDamage'] = Source['EnchantColdValue']`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Frost Nova

`pendente`


**Texto:** The caster creates a wave of frozen energy dealing *0 cold damage within 2 hexes of the selected target.


**expr:** `Source.SpellPower() * 1f * Source.DamageModCold`


**acao `Frost Nova`:** `TargetStored['ColdDamage'] = Source.SpellPower('Cold') * 1f`


**conferir:** 2 hex — sem par no codigo dumpado


## T2 Frostbite II · **PASSIVA**

`pendente`


**Texto:** Your stacks of @Chilled@ now reduce the targets damage by an additional 3%.


**attr:** `ChilledDamageReduction:Base:3,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Frozen Orb

`corrigido`


**Texto:** Hurls a ball of Ice dealing *0 cold damage to all targets in range. Applies 5 stacks of {STA=Chilled}


**expr:** `Source.SpellPower() * 1.1f * Source.DamageModFire`


**acao `Dragonkin Frozen Orb`:** `TargetStored['ColdDamage'] = Source.SpellPower('Cold') * 2f`


**status `Chilled`:** efeitos=`TurnFreeMovementPoints:Base:Target.CanBeEffectedByChilled ? (Target.ChilledEffectHalved ? -.5f : -1) : 0, DamageMod:Base:-(Source["ChilledDamageReduction"]), MaxHealth:Percentage:Source["Frostbite"] == 1 ? -5 : 0, Armor:Percentage:Source["InvulnerableWinter"] == 1 ? 5 : 0, MagicArmor:Percentage:Source["InvulnerableWinter"] == 1 ? 5 : 0` classe=debuff


> Movement points reduced by one per stack.  Lasts 2 turns.  Five stacks of Chilled freezes the target.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Ice Lance

`pendente`


**Texto:** The caster hurls a razor-like shard of ice piercing foes in a line dealing *0 cold damage. 


**expr:** `Source.SpellPower() * 1.2f * Source.DamageModCold`


**acao `Ice Lance`:** `TargetStored['ColdDamage'] = Source.SpellPower('Cold') * 1.2f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Aura Of Frost

`pendente`


**Texto:** Deals *0 cold damage to enemies that start their turns within 3 hexes of your character.


**expr:** `Source.SpellPower() * .4f * Source.DamageModCold`


**acao `Aura Of Frost`:** `-`


**conferir:** 3 hex — sem par no codigo dumpado


## T3 Breath of Winter

`pendente`


**Texto:** Conjures the breath of a frost dragon dealing *0 cold damage to all enemies in a cone. 


**expr:** `Source.SpellPower() * 1.6f * Source.DamageModCold`


**acao `Breath of Winter`:** `TargetStored['ColdDamage'] = Source.SpellPower('Cold') * 1.6f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Cold Heart · **PASSIVA**

`pendente`


**Texto:** Each stack of chilled you've applied increases your cold damage by 5%.


**attr:** `DamageModCold:Base:Source.GetNumStatusesCaused("GL-ChilledStatus") * 5,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Diamond Ice · **PASSIVA**

`corrigido`


**Texto:** 1% of your @Armor@ value is added to your character as @Additional Cold Damage@.  Current Bonus: [0]


**attr:** `DamageFlatCold:Base:Source["Armor"] * .01f,`


**expr:** `Source['Armor'] * .01f`


**conferir:** 1% — sem par no codigo dumpado


## T3 Frozen Spikes

`pendente`


**Texto:** Hurl 5 shards of ice dealing *0 cold damage to each target.


**expr:** `Source.SpellPower() * .2f * Source.DamageModCold`


**acao `Frozen Spikes`:** `TargetStored['ColdDamage'] = Source.SpellPower('Cold') * .2f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Ice Wall

`corrigido`


**Texto:** Summon pillars of ice to block 4 hexes blocking enemy's line of sight. Attackers take cold damage.  Lasts 4 turns.


**acao `Ice Wall New`:** `-`


**conferir:** 4 hex — sem par no codigo dumpado


## T4 Brain Freeze

`pendente`


**Texto:** Deals *0 cold damage each time the target performs an action.


**acao `Brain Freeze`:** `TargetStored['ColdDamage'] = Source.SpellPower('Cold') * 1f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Frozen Core · **PASSIVA**

`pendente`


**Texto:** Each stack of @chilled@ now reduces the target's maxium health by 5%.


**attr:** `Frostbite:Set:1,`


**conferir:** 5% — sem par no codigo dumpado


## T4 Ice Storm

`pendente`


**Texto:** Conjure a massive ice storm dealing *0 cold damage to affected enemies each turn.


**expr:** `Source.SpellPower('Cold') * .9f * Source.DamageModCold`


**acao `Ice Storm`:** `TargetStored['ColdDamage'] = Source.SpellPower('Cold') * .9f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Invulnerable Winter · **PASSIVA**

`corrigido`


**Texto:** @Intelligence@ grants [0] @Armor@ and @Magic Armor@ per point.  Current Bonus: [1]


**attr:** `Armor:Base:Source["Intelligence"] * (1 + (.14f * Source.Level)), MagicArmor:Base:Source["Intelligence"] * (1 + (.14f * Source.Level)),`


**expr:** `1 + (.14f *Source.Level); Source['Intelligence'] * (1 + (.14f * Source.Level))`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Stasis

`pendente`


**Texto:** Encases the friendly target in a dome of ice granting [0] Armor and Magic Armor for the duration. Immobilizes the target.


**expr:** `15 * Source.Level`


**acao `Stasis`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Chain Frost

`corrigido`


**Texto:** Deals *0 cold damage.  Bounces between enemies within 4 hexes up to 10 times.


**expr:** `Source.SpellPower() * .5f * Source.DamageModCold`


**acao `Chain Frost`:** `TargetStored['ColdDamage'] = Source.SpellPower() * .5f`


**conferir:** 4 hex — sem par no codigo dumpado


## T5 Icefall · **PASSIVA**

`pendente`


**Texto:** When enemies are frozen by you they release a @frost nova@. 


**attr:** `Icefall:Set:1,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Mass Freeze

`pendente`


**Texto:** Applies {STA=Frozen} to all enemies.


**acao `Mass Freeze`:** `-`


**status `Frozen`:** efeitos=`Rooted:Set:1, Disabled:Set:1, ImmunityChilled:Set:1` classe=buff


> Cannot move or perform actions.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Master Of Ice · **PASSIVA**

`pendente`


**Texto:** Each turn you freeze an enemy, you gain an additional action.


**attr:** `MasterOfIce:Set:1,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Shatter

`pendente`


**Texto:** Summons a blast of frozen energy dealing *0 cold damage plus an additional *0 per stack of @Chilled@ on targets in a 4 hex radius.


**expr:** `Source.SpellPower('Cold') * .7f * Source.DamageModCold`


**danoExpr:** `TargetStored['ColdDamage'] =  (Source.SpellPower('Cold') * .7f)`


**acao `Shatter`:** `TargetStored['ColdDamage'] = (Target.NumChilledStacks + 1) * (Source.SpellPower('Cold') * .7f)`


**conferir:** 4 hex — sem par no codigo dumpado

