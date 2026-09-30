# Ficha de revisao — arvore **Shadow** (41 skills)

> Gerado por `tools/verify_tree.py`. Junta o TEXTO da tooltip com o que o jogo
> CALCULA. A ultima linha de cada ficha (`conferir`) lista o que **nao** tem par no
> codigo — e o que precisa de olho humano ou triangulacao externa, nao veredito.


## T1 Blind

`corrigido`


**Texto:** Deals *0 shadow damage.  Applies {STA=Blind} for 1 turn.


**expr:** `Source.SpellPower() * 1.1f * Source.DamageModShadow`


**acao `Blind`:** `TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') * 1.1f`


**status `Blind`:** efeitos=`Blind:Set:1` classe=buff


> Blind.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Call of the Grave · **PASSIVA**

`pendente`


**Texto:** Deal 20% additional damage to enemies below 50% health.


**attr:** `CallOfTheGrave:Set:1,`


**conferir:** 20%, 50% — sem par no codigo dumpado


## T1 Ghost Armor

`corrigido`


**Texto:** Completely negates the next attack.  Lasts until hit. 


**acao `Ghost Armor`:** `Target['GhostArmorValue'] = 1`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Necromancer I · **PASSIVA**

`pendente`


**Texto:** Summons deal 10% more damage and have 10% more health.


**attr:** `SummonDamageMod:Base:10, SummonHealthMod:Base:10,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Raise Skeletal Archer

`corrigido`


**Texto:** Summon a skeletal archer to fight by your side.


**acao `Raise Skeletal Archer`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Raise Undead Ranger

`revisado`


**Texto:** Raise an Undead Ranger to fight by your side.


**acao `[Necronomicon] Raise Undead Ranger`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Shadow Breath

`pendente`


**Texto:** Breathe out a stream of shadow energy dealing *0 shadow damage to all enemies in range.


**expr:** `Source.SpellPower('Shadow') * 1.6f * Source.DamageModShadow`


**acao `Shadow Breath`:** `TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') * 1.6f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Tainted Touch

`corrigido`


**Texto:** Reaches out to the target with dark energy dealing *0 shadow damage. @Life Steals@ for 12%.  @Life Steal@ heals you for a percentage of your @max health@ each time you hit. Reduced for area of effect and no ap cost abilities.


**expr:** `Source.SpellPower() * 1.2f * Source.DamageModShadow`


**acao `Tainted Touch`:** `TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') * 1.2f; SourceStored['HealingForced'] = (Source['MaxHealth'] * .12f)`


**conferir:** 12% — sem par no codigo dumpado


## T2 Abyssal Night

`pendente`


**Texto:** Hurls an orb of dark energy dealing *0 shadow damage to all targets in range.


**expr:** `Source.SpellPower('Shadow') * 2.3f * Source.DamageModShadow`


**acao `Dragonkin Shadow Orb`:** `TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') * 2.1f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Curse

`pendente`


**Texto:** Curse the target lowering @All resistances@ by 20% and @Healing Received@ by 50%.


**acao `Curse`:** `-`


**status `Curse`:** efeitos=`ResistPhysical:Base:-20, ResistCold:Base:-20, ResistFire:Base:-20, ResistLightning:Base:-20, ResistDivine:Base:-20, HealingReceivedBonus:Base:-50` classe=debuff


> @All resistances@ lowered by 20%. Healing received lowered by 50%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Dark Pact · **PASSIVA**

`pendente`


**Texto:** Increase the effectiveness of your damage and healing skills by 30%.   Maximum health reduced by 20%.


**attr:** `DamageMod:Base:30, MaxHealth:Percentage:-20,`


**conferir:** 20% — sem par no codigo dumpado


## T2 Haunt

`pendente`


**Texto:** Deals *0 shadow damage to the target every turn for 3 turns. @Life Steals@ for 6%.   @Life Steal@ heals you for a percentage of your @max health@ each time you hit. Reduced for area of effect and no ap cost abilities.


**expr:** `Source.SpellPower() * .5f * Source.DamageModShadow`


**acao `Haunt`:** `-`


**conferir:** 6% — sem par no codigo dumpado


## T2 Necromancer II · **PASSIVA**

`pendente`


**Texto:** Summons deal an additional 15% more damage and have an additional 15% more health.


**attr:** `SummonDamageMod:Base:15, SummonHealthMod:Base:15,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Poison Cloud

`corrigido`


**Texto:** The caster creates an poison gas cloud applies @4@ stacks of {STA=Poisoned} within 2 hexes of the selected target.


**expr:** `Source.SpellPower() * .5f * Source.DamageModShadow`


**acao `Poison Cloud - Player`:** `-`


**status `Poisoned`:** efeitos=`HealingReceivedBonus:Base:-1, PoisonDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Poisoned", "TargetStored[\"ShadowDamage\"] = Source.SpellPower(\"Shadow\") * .1f")), ContagionLevel:Base:Source["ContagionSource"] > 0 ? 1 : 0` classe=debuff


> Target takes [1] shadow damage each turn. Reduces healing taken by [0]%.


**conferir:** 2 hex — sem par no codigo dumpado


## T2 Spectral Chains

`pendente`


**Texto:** Deals *0 shadow damage and applies {STA=Immobilized} for 1 turn.


**expr:** `Source.SpellPower() * .7f * Source.DamageModShadow`


**acao `Spectral Chains`:** `TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') * .7f`


**status `Immobilized`:** efeitos=`Rooted:Set:1` classe=buff


> Cannot move.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Thirst I · **PASSIVA**

`corrigido`


**Texto:** Increases @Life Steal@ by 4%.  @Life Steal@ heals you for a percentage of your @max health@ each time you hit. Reduced for area of effect and no ap cost abilities.


**attr:** `LifeOnHit:Base:4,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Vengeful Shadows · **PASSIVA**

`pendente`


**Texto:** Grants [0] Return Shadow Damage.


**attr:** `DamageReturnedFlatShadow:Base:Source.GetFlatDamageValue * 3,`


**expr:** `Source.GetFlatDamageValue * 3`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Consumption

`pendente`


**Texto:** Devour the life force of all enemies within 2 hexes dealing *0 Shadow Damage and giving you 10% @Maximum Health@ for each enemy effected.


**acao `Consumption`:** `TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') * .7f`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** 10%, 2 hex — sem par no codigo dumpado


## T3 Hunger · **PASSIVA**

`corrigido`


**Texto:** Grants 10% @mana steal@.  Sacrifices 10% maximum health per turn.


**conferir:** 10% — sem par no codigo dumpado


## T3 Mana Drain

`pendente`


**Texto:** Removes 20% of the target's max mana and restores 20% of the caster's max mana.


**acao `Purge`:** `TargetStored['ManaDamage'] = Target.MaxMana * .2f; SourceStored['ManaDamage'] = Source.MaxMana * -.2f`


**conferir:** 20% — sem par no codigo dumpado


## T3 Raise Skeletal Warrior

`corrigido`


**Texto:** Summon a skeletal warrior to fight by your side.


**acao `Raise Skeletal Warrior`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Raise Undead Berserker

`pendente`


**Texto:** Raise an Undead Berserker to fight by your side.


**acao `[Necronomicon] Raise Undead Berserker`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Reaper's Toll · **PASSIVA**

`pendente`


**Texto:** Every enemy that dies heals you for 10% of your maximum health.


**conferir:** 10% — sem par no codigo dumpado


## T3 Soul Crush

`corrigido`


**Texto:** Crush the target's soul dealing *0 @Shadow Damage@ increased by your Max Health. 


**expr:** `Source.SpellPower('Shadow') + (Source['MaxHealth'] *.05f)`


**acao `Soul Fracture`:** `TargetStored['ShadowDamage'] = (Source['MaxHealth'] *.2f)`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Thirst II · **PASSIVA**

`corrigido`


**Texto:** Increases @Life Steal@ by 6%.  @Life Steal@ heals you for a percentage of your @max health@ each time you hit. Reduced for area of effect and no ap cost abilities.


**attr:** `LifeOnHit:Base:6,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Dark Ritual

`pendente`


**Texto:** Target cannot drop below 1 hp while active.


**acao `Dark Ritual`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Exorcism

`corrigido`


**Texto:** Deals *0 shadow damage and removes a random benefical status from the target. If a status is removed, the target suffers an additional *0 shadow damage.


**expr:** `Source.SpellPower('Shadow') * 1f * Source.DamageModShadow`


**acao `Exorcism`:** `TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') * 1f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Leech Dexterity · **PASSIVA**

`pendente`


**Texto:** Damage caused steals [0] points of @Dexterity@. Lasts the entire battle. Stacks up to 10 times.


**expr:** `2 * (.1f * Source.Level)`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Leech Intelligence · **PASSIVA**

`pendente`


**Texto:** Damage caused steals [0] points of @Intelligence@. Lasts the entire battle. Stacks up to 10 times.


**expr:** `2 * (.1f * Source.Level)`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Leech Might · **PASSIVA**

`pendente`


**Texto:** Damage caused steals [0] points of @Might@. Lasts the entire battle. Stacks up to 10 times.


**expr:** `2 * (.1f * Source.Level)`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Soul Link

`pendente`


**Texto:** All damage and healing dealt to one target is also dealt to the linked target.


**acao `Soul Link`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Vampiric Aura

`corrigido`


**Texto:** Allies within Vampiric Aura @Life Steal@ for 5%.  @Life Steal@ heals you for a percentage of your @max health@ each time you hit. Reduced for area of effect and no ap cost abilities.


**acao `Vampiric Aura`:** `-`


**status `Vampiric Aura`:** efeitos=`LifeSteal:Base:50` classe=buff


> @Life steal@ increased.


**conferir:** 5% — sem par no codigo dumpado


## T5 Child of the Abyss · **PASSIVA**

`pendente`


**Texto:** Increases @Max Health@ by 100%. Can no longer be healed by any means other than life steal.


**attr:** `MaxHealth:Percentage:100, ChildOfTheAbyss:Set:1,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Coin of Chaos

`sem-explicacao`


**Texto:** Flip the Coin of Chaos!


**acao `Coin Flip`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Endless Night · **PASSIVA**

`pendente`


**Texto:** Gain 2% of your maximum health as @Additional Shadow Damage@.   Current Shadow Damage Increase: [0].


**attr:** `DamageFlatShadow:Base:Source["MaxHealth"] * .02f,`


**expr:** `Source['MaxHealth'] * .02f`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** 2% — sem par no codigo dumpado


## T5 Lich Lord · **PASSIVA**

`pendente`


**Texto:** Removes the AP cost from all summoning skills.


**attr:** `LichLord:Set:1,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Raise Iron Golem

`corrigido`


**Texto:** Raise a Mighty Iron Golem to fight for you.


**acao `Raise Iron Golem`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Raise Skeletal Mage

`corrigido`


**Texto:** Summon a skeletal mage to fight by your side.


**acao `Raise Skeletal Mage`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Raise Undead Wizard

`corrigido`


**Texto:** Raise a Undead Wizard to fight by your side.


**acao `[Necronomicon] Raise Undead Wizard`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Reaper's Scythe

`pendente`


**Texto:** Deals *0 shadow damage for every 10% health missing from the target.


**expr:** `Source.SpellPower('Shadow') * 1f * Source.DamageModShadow`


**danoExpr:** `TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') * 1f`


**acao `Reaper's Scythe`:** `TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') * 10.0f *  Target.HealthRatioInverse`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Soul Exchange

`corrigido`


**Texto:** Swaps the life force of both you and a target, dealing *0 @Shadow Damage@ based on your missing Health. @Lifesteals@ 100%.  @Life Steal@ heals you for a percentage of your @max health@ each time you hit. Reduced for area of effect abilities.


**expr:** `(Source.SpellPower('Shadow') * (Source.HealthRatioInverse *.008f))`


**acao `Soul Exchange`:** `TargetStored['ShadowDamage'] = (((Source.MaxHealth - Source.Health) * .35f) + Source.SpellPower('Shadow')); SourceStored['HealingForced'] = (Source['MaxHealth'])`


**conferir:** 100% — sem par no codigo dumpado

