# Ficha de revisao — arvore **Ranger** (40 skills)

> Gerado por `tools/verify_tree.py`. Junta o TEXTO da tooltip com o que o jogo
> CALCULA. A ultima linha de cada ficha (`conferir`) lista o que **nao** tem par no
> codigo — e o que precisa de olho humano ou triangulacao externa, nao veredito.


## T1 Crippling Shot

`corrigido`


**Texto:** Deals *0 weapon damage.  Applies {STA=Slow}.


**expr:** `Source.AttackPower * .7f * Source.DamageModPhysical`


**acao `Crippling Shot`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * .7f`


**status `Slow`:** efeitos=`MovementCostPerHexMod:Set:100` classe=buff


> Movement costs doubled.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Eagle Eye · **PASSIVA**

`revisado`


**Texto:** Increase the range of all ranged skills by 1 hex.


**attr:** `RangeTypeAdderRanged:Base:1,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Huntsman I · **PASSIVA**

`revisado`


**Texto:** Physical damage increased by [0].


**attr:** `DamageFlatPhysical:Base:Source.GetFlatDamageValue * 1.2f,`


**expr:** `Source.GetFlatDamageValue * 1.2f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Rally

`pendente`


**Texto:** Increases movement of all allies within 4 hexes by 3.


**acao `Rally`:** `-`


**conferir:** 4 hex — sem par no codigo dumpado


## T1 Summon Raven

`revisado`


**Texto:** Summon a Raven to fight your enemies. 


**acao `Animal Companion Raven`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Survivalist I · **PASSIVA**

`revisado`


**Texto:** Increases @all resistance@ and @dodge chance@ by 3%.


**attr:** `ResistPhysical:Base:3, ResistCold:Base:3, ResistFire:Base:3, ResistLightning:Base:3, DodgeChance:Base:3,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Tracker's Mark

`corrigido`


**Texto:** Gain 15% @increased damage@ and 8% @critical hit chance@ on the target.  If the target dies while Tracker's Mark is active, the cooldown is reset.


**acao `Tracker's Mark`:** `-`


**status `Tracker's Mark`:** efeitos=`CritChanceTarget:Base:8, DamageReduction:Base:-15` classe=buff


> Chance of suffering critical strikes increased by 8%. Damage taken increased by 15%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Tranquilizing Shot

`revisado`


**Texto:** Tranquilizes the target applying {STA=Sleep} for 2 turns.


**acao `Tranquilizing Shot`:** `-`


**status `Sleep`:** efeitos=`Rooted:Set:1, Disabled:Set:1, DamageReduction:Base:-50` classe=indefinido


> Asleep.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Bleeding Shot

`corrigido`


**Texto:** Deals *0 weapon damage.  Applies 2 stacks of {STA=Bleeding}.


**expr:** `Source.AttackPower * .8f * Source.DamageModPhysical`


**acao `Bleeding Shot`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * .8f`


**status `Bleeding`:** efeitos=`ResistPhysical:Base:-5, BleedingDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Bleeding", "TargetStored[\"PhysicalDamage\"] = Source.AttackPower * .05f"))` classe=debuff


> Target takes [1] physical damage for each hex they move. Reduces Physical Resistance by [0]%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Bounty Hunter's Mark

`corrigido`


**Texto:** Gain 15% @increased damage@ and 8% @critical hit chance@ against the target.  If the target dies while Bounty Hunter's Mark is active, all cooldowns are reduced by 1.


**acao `Bounty Hunter's Mark`:** `-`


**status `Bounty Hunter's Mark`:** efeitos=`CritChanceTarget:Base:8, DamageReduction:Base:-15` classe=buff


> Chance of suffering critical strikes increased by 8%. Damage taken increased by 15%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Disengage · **PASSIVA**

`revisado`


**Texto:** You can move 1 additional hex each turn and no longer take opportunity attacks. 


**attr:** `TurnFreeMovementPoints:Base:1, OpportunityAttackImmunity:Set:1,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Huntsman II · **PASSIVA**

`revisado`


**Texto:** Physical damage increased by [0].


**attr:** `DamageFlatPhysical:Base:Source.GetFlatDamageValue * 1.8f,`


**expr:** `Source.GetFlatDamageValue * 1.8f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Pinning Shot

`corrigido`


**Texto:** Deals *0 weapon damage.  Applies {STA=Immobilized}.


**expr:** `Source.AttackPower * .8f * Source.DamageModPhysical`


**acao `Pinning Shot`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * .8f`


**status `Immobilized`:** efeitos=`Rooted:Set:1` classe=buff


> Cannot move.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Precision I · **PASSIVA**

`revisado`


**Texto:** Increase @critical hit chance@ by 4%. Increase @critical hit damage@ by 16%.


**attr:** `CritChance:Base:4, CritDamage:Base:16,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Relocate

`corrigido`


**Texto:** Jump to the target area.  Unaffected by increased range modifiers.


**acao `Relocate`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Stalker's Mark

`corrigido`


**Texto:** Gain 25% @increased damage@ and 12% @critical hit chance@ against the target.  If the target dies while Stalker's Mark is active, the cooldown is reset.


**acao `Stalker's Mark`:** `-`


**status `Stalker's Mark`:** efeitos=`CritChanceTarget:Base:12, DamageReduction:Base:-25` classe=buff


> Chance of suffering critical strikes increased by 12%. Damage taken increased by 25%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Survivalist II · **PASSIVA**

`revisado`


**Texto:** Increases @all resistance@ and @dodge chance@ by an additional 5%.


**attr:** `ResistPhysical:Base:5, ResistCold:Base:5, ResistFire:Base:5, ResistLightning:Base:5, DodgeChance:Base:5,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Blasting Shot

`corrigido`


**Texto:** Deals *0 weapon damage to all targets in area.  Targets are knocked back 3 hexes. 


**expr:** `Source.AttackPower * 1f * Source.DamageModPhysical`


**acao `Blasting Shot`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1f`


**conferir:** 3 hex — sem par no codigo dumpado


## T3 Long Shot

`corrigido`


**Texto:** Deals *0 weapon damage.  Every hex between you and your target increases the damage of by 10%. 


**expr:** `Source.AttackPower * 1f * Source.DamageModPhysical`


**danoExpr:** `TargetStored[Source.WeaponDamageType] = (Source.AttackPower * 1f)`


**acao `Long Shot`:** `TargetStored[Source.WeaponDamageType] = (Source.AttackPower * 1f) *  (1 + ((Source.Cell.Distance(Target.Cell) - 1) * .1f))`


**conferir:** 10% — sem par no codigo dumpado


## T3 Patient Hunter · **PASSIVA**

`corrigido`


**Texto:** Patient Hunter gives 10% @increased damage@ and 1 @skill range@ per stack.  A stack is applied at the end of each turn.  Making any movement removes all stacks of Patient Hunter.  Stacks up to 5 times.


**status `Patient Hunter`:** efeitos=`DamageMod:Base:10, RangeTypeAdderRanged:Base:1` classe=buff


> Damage increased by 10%, Range increased by 1 per stack.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Precision II · **PASSIVA**

`revisado`


**Texto:** Increase @critical hit chance@ by an additional 6%. Increase @critical hit damage@ by an additional 24%.


**attr:** `CritChance:Base:6, CritDamage:Base:24,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Quick Hands · **PASSIVA**

`corrigido`


**Texto:** Your basic attack has a 50% chance to strike twice.  Can only trigger once per turn.


**conferir:** 50% — sem par no codigo dumpado


## T3 Ranger's Gift I · **PASSIVA**

`revisado`


**Texto:** Every hex between you and your target increases damage dealt by 2%.


**attr:** `PerHexRangeDamageBonus:Base:2,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Summon Wolf

`revisado`


**Texto:** Summon a wolf to fight your enemies.


**acao `Animal Companion Wolf`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Volley

`corrigido`


**Texto:** Shoot up to 5 enemies near the target area dealing *0 weapon damage per target.  The arrow can chain to targets within 3 hexes of the last target hit.


**expr:** `Source.AttackPower * 1.6f * Source.DamageModPhysical`


**acao `Volley`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1.6f`


**conferir:** 3 hex — sem par no codigo dumpado


## T4 Called Shot

`corrigido`


**Texto:** Deals *0 weapon damage. Every hex between you and your target increases the damage of by 10%.  Called Shot cannot be dodged or blocked.


**expr:** `Source.AttackPower * 1.2f * Source.DamageModPhysical; Source.AttackPower * .075f * Source.DamageModPhysical`


**danoExpr:** `TargetStored[Source.WeaponDamageType] = (Source.AttackPower * 1.2f)`


**acao `Called Shot`:** `TargetStored[Source.WeaponDamageType] = (Source.AttackPower * 1.2f) *  (1 + ((Source.Cell.Distance(Target.Cell) - 1) * .1f))`


**conferir:** 10% — sem par no codigo dumpado


## T4 Dispelling Shot

`corrigido`


**Texto:** Deals *0 weapon damage. Removes 1 random benefical status from the target.


**expr:** `Source.AttackPower * 1f * Source.DamageModPhysical`


**acao `Dispelling Shot`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 1f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Endless Quiver · **PASSIVA**

`revisado`


**Texto:** Reduces all Ranger cooldowns by 1.


**attr:** `CooldownModRanger:Base:-1,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Piercing Shot

`revisado`


**Texto:** Deals *0 weapon damage in a line.


**expr:** `Source.AttackPower * 2f * Source.DamageModPhysical`


**acao `Piercing Shot`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 2f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Quick Draw

`revisado`


**Texto:** Your next 3 basic attacks have no AP cost. Applies {STA=Exhaustion}.


**acao `Quick Draw`:** `-`


**status `Exhaustion`:** efeitos=`RecentlyHasted:Set:1` classe=buff


> Cannot receive additional actions points.  Caused by receiving additional action points this turn.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Ranger's Gift II · **PASSIVA**

`revisado`


**Texto:** Every hex between you and your target increases damage dealt by an additional 3%.


**attr:** `PerHexRangeDamageBonus:Base:3,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Sniper Shot

`corrigido`


**Texto:** Deals *0 weapon damage.  Every hex between you and your target increases the damage of by 15%. 


**expr:** `Source.AttackPower * 1f * Source.DamageModPhysical; Source.AttackPower * .15f * Source.DamageModPhysical`


**danoExpr:** `TargetStored[Source.WeaponDamageType] = (Source.AttackPower * 1f)`


**acao `Sniper Shot`:** `TargetStored[Source.WeaponDamageType] = (Source.AttackPower * 1f) *  (1 + ((Source.Cell.Distance(Target.Cell) - 1) * .15f))`


**conferir:** 15% — sem par no codigo dumpado


## T4 Take Cover · **PASSIVA**

`revisado`


**Texto:** Damage you take from enemies further than 2 hexes from you is reduced by 35%.


**attr:** `TakeCover:Set:1,`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** 2 hex, 35% — sem par no codigo dumpado


## T5 Animal Companion Grizzly

`revisado`


**Texto:** Summon a grizzly to fight your enemies.


**acao `Animal Companion Grizzly`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Branching Shot

`revisado`


**Texto:** Deals *0 weapon damage. Bounces to enemies within 3 hexes. Each bounce increases its damage by 50%.


**expr:** `Source.AttackPower * 2f * Source.DamageModPhysical; Source.AttackPower * .5f * Source.DamageModPhysical`


**acao `Branching Shot`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * (2f + (ChainCount * 1f))`


**conferir:** 3 hex, 50% — sem par no codigo dumpado


## T5 Cupid Shot

`corrigido`


**Texto:** Charm the enemy target for 1 turn.  Cannot target bosses.


**acao `Cupid Shot`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Force Shot

`corrigido`


**Texto:** Deals *0 weapon damage in a line and knocks targets back up to 4 hexes.  Any enemy hit by the target also receives [1] damage.


**expr:** `Source.AttackPower * 3f * Source.DamageModPhysical; Source.AttackPower * 3f * Source.DamageModPhysical`


**acao `Impaling Shot`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 3f`


**conferir:** 4 hex — sem par no codigo dumpado


## T5 Marked Prey · **PASSIVA**

`corrigido`


**Texto:** Attacks now apply {STA=Marked Prey}.  All stacks are removed at the end of your turn.


**status `Marked Prey`:** efeitos=`DamageReduction:Base:-10` classe=debuff


> Damage taken increased by 10% per stack.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Mythic Reach · **PASSIVA**

`revisado`


**Texto:** All ranged abilities get an additional 5 hex range.


**attr:** `RangeTypeAdderRanged:Base:5,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Slaying Shot

`revisado`


**Texto:** Deals *0 weapon damage. Ignores all armor and resists. Cannot be dodged.


**expr:** `Source.AttackPower * 3.5f * Source.DamageModPhysical`


**acao `Slaying Shot`:** `TargetStored[Source.WeaponDamageType] = Source.AttackPower * 4f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok

