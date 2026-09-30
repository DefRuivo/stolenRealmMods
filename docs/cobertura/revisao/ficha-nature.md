# Ficha de revisao — arvore **Nature** (39 skills)

> Gerado por `tools/verify_tree.py`. Junta o TEXTO da tooltip com o que o jogo
> CALCULA. A ultima linha de cada ficha (`conferir`) lista o que **nao** tem par no
> codigo — e o que precisa de olho humano ou triangulacao externa, nao veredito.


## T1 Adaptation I · **PASSIVA**

`pendente`


**Texto:** Gain a 6% resistance to the last type of damage taken.


**attr:** `ResistPhysical:Base:Source.LastDamageTypeTaken == 1 ? 6 : 0, ResistFire:Base:Source.LastDamageTypeTaken == 2 ? 6 : 0, ResistCold:Base:Source.LastDamageTypeTaken == 3 ? 6 : 0, ResistLightning:Base:Source.LastDamageTypeTaken == 4 ? 6 : 0, ResistDivine:Base:Source.LastDamageTypeTaken == 5`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Beast Master I · **PASSIVA**

`pendente`


**Texto:** Summons deal 10% more damage and have 10% more health. 


**attr:** `SummonDamageMod:Base:10, SummonHealthMod:Base:10,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Brambles

`pendente`


**Texto:** Summon brambles to block 4 hexes. Attackers will take physical damage when striking the brambles. Lasts 4 turns.


**acao `Brambles`:** `-`


**conferir:** 4 hex — sem par no codigo dumpado


## T1 Entangle

`pendente`


**Texto:** Deals *0 physical damage and applies {STA=Immobilized} for 1 turn and @2@ stacks of {STA=Poisoned}.


**acao `Entangle`:** `TargetStored['PhysicalDamage'] = Source.SpellPower('Physical') * .3f`


**status `Immobilized`:** efeitos=`Rooted:Set:1` classe=buff


> Cannot move.


**status `Poisoned`:** efeitos=`HealingReceivedBonus:Base:-1, PoisonDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Poisoned", "TargetStored[\"ShadowDamage\"] = Source.SpellPower(\"Shadow\") * .1f")), ContagionLevel:Base:Source["ContagionSource"] > 0 ? 1 : 0` classe=debuff


> Target takes [1] shadow damage each turn. Reduces healing taken by [0]%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Faerie Swarm

`corrigido`


**Texto:** Faeries swarm the target clawing and biting for *0 physical damage and applying 1 stack of {STA=Bleeding}  each turn.


**expr:** `Source.SpellPower('Physical') * .4f * Source.DamageModPhysical`


**acao `Faerie Swarm`:** `-`


**status `Bleeding`:** efeitos=`ResistPhysical:Base:-5, BleedingDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Bleeding", "TargetStored[\"PhysicalDamage\"] = Source.AttackPower * .05f"))` classe=debuff


> Target takes [1] physical damage for each hex they move. Reduces Physical Resistance by [0]%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Nature Summoning I

`pendente`


**Texto:** Summons a Raven, Coyote, or Raccoon to fight for you.


**acao `Nature Summoning I`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Pack Hunter I · **PASSIVA** · ⚠ **nome repetido** (2 variantes — confira o `attr` pelo `skid` em `skills-detalhe.csv`)

`pendente`


**Texto:** For every ally within 1 hex of you gain 8% @increased Damage@.


**attr:** `DamageMod:Base:12 * Source.NumAlliesWithin(1),`


**conferir:** 8% — sem par no codigo dumpado


## T1 Pack Summoning I

`pendente`


**Texto:** Summons a Timber Wolf to fight for you


**acao `Nature Summoning I  [Pack Summoning]`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Thorns I · **PASSIVA**

`pendente`


**Texto:** Grants [0] Return Physical Damage.


**attr:** `DamageReturnedFlatPhysical:Base:Source.GetFlatDamageValue * 1.2f,`


**expr:** `Source.GetFlatDamageValue * 1.2f`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Adaptation II · **PASSIVA**

`pendente`


**Texto:** Gain an additional 9% resistance to the last type of damage taken.


**attr:** `ResistPhysical:Base:Source.LastDamageTypeTaken == 1 ? 9 : 0, ResistFire:Base:Source.LastDamageTypeTaken == 2 ? 9 : 0, ResistCold:Base:Source.LastDamageTypeTaken == 3 ? 9 : 0, ResistLightning:Base:Source.LastDamageTypeTaken == 4 ? 9 : 0, ResistDivine:Base:Source.LastDamageTypeTaken == 5`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Beast Master II · **PASSIVA**

`pendente`


**Texto:** Summons deal an additional 15% more damage and have an additional 15% more health. 


**attr:** `SummonDamageMod:Base:15, SummonHealthMod:Base:15,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Living Armor

`pendente`


**Texto:** Envelopes the target in living vines that increase @armor@ and @magic armor@ by [0] and causes the target to regenerate *0 @health@ each turn.


**expr:** `3.5f * Source.Level`


**acao `Living Armor`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Pack Hunter I · **PASSIVA** · ⚠ **nome repetido** (2 variantes — confira o `attr` pelo `skid` em `skills-detalhe.csv`)

`pendente`


**Texto:** For every ally within 1 hex of you gain an additional 12% @increased Damage@.


**attr:** `DamageMod:Base:12 * Source.NumAlliesWithin(1),`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 The Bad Bloom

`pendente`


**Texto:** Creates a magic flower that applies 2 stacks of {STA=Poisoned} per turn to enemies in range.


**acao `The Bad Bloom`:** `-`


**status `Poisoned`:** efeitos=`HealingReceivedBonus:Base:-1, PoisonDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Poisoned", "TargetStored[\"ShadowDamage\"] = Source.SpellPower(\"Shadow\") * .1f")), ContagionLevel:Base:Source["ContagionSource"] > 0 ? 1 : 0` classe=debuff


> Target takes [1] shadow damage each turn. Reduces healing taken by [0]%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Thorns II · **PASSIVA**

`pendente`


**Texto:** Grants an additional [0] Return Physical Damage.


**attr:** `DamageReturnedFlatPhysical:Base:Source.GetFlatDamageValue * 1.8f,`


**expr:** `Source.GetFlatDamageValue * 1.8f`


**status `Damage`:** efeitos=`-` classe=indefinido


> Damaged.  


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Venomous Skin

`pendente`


**Texto:** Causes the skin of a target ally to secrete poison. Attacking enemies receive 3 stacks of {STA=Poisoned}. Lasts 3 turns.


**expr:** `Source.SpellPower() * .15f * Source.DamageModFire`


**acao `Venomous Skin`:** `-`


**status `Poisoned`:** efeitos=`HealingReceivedBonus:Base:-1, PoisonDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Poisoned", "TargetStored[\"ShadowDamage\"] = Source.SpellPower(\"Shadow\") * .1f")), ContagionLevel:Base:Source["ContagionSource"] > 0 ? 1 : 0` classe=debuff


> Target takes [1] shadow damage each turn. Reduces healing taken by [0]%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Bristles · **PASSIVA**

`pendente`


**Texto:** Summons gain 50% of your return damage.


**attr:** `Bristles:Set:1,`


**conferir:** 50% — sem par no codigo dumpado


## T3 Contagion · **PASSIVA**

`pendente`


**Texto:** Your poison damage spreads to enemy targets within 1 hex of the poisoned enemy.


**attr:** `ContagionSource:Set:1,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Nature Summoning II

`pendente`


**Texto:** Summons a Stag, Wolf, or Boar to fight for you.


**acao `Nature Summoning II`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Pack Summoning II

`pendente`


**Texto:** Summons a Tundra Wolf to fight for you.


**acao `Nature Summoning II  [Pack Summoning]`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Shapeshift Werewolf

`pendente`


**Texto:** Shapeshift into a @Werewolf@. Empowers your basic attack and gain new abilities. Increases @Max Health@ by 10%.


**acao `Shapeshift Werewolf`:** `-`


**conferir:** 10% — sem par no codigo dumpado


## T3 Skin Walker · **PASSIVA**

`pendente`


**Texto:** Reduces the cooldown of Shapeshifting skills by 2.


**attr:** `CooldownModShapeshifting:Base:-2,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Stun Spores

`pendente`


**Texto:** Infects enemies with Stunning Spores applying {STA=Stun} for 1 turns.


**expr:** `Source.SpellPower() * .5f * Source.DamageModShadow`


**acao `Stun Spores`:** `-`


**status `Stun`:** *nao esta no censo de status*


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 The Good Bloom

`pendente`


**Texto:** Creates a magic blossom that regenerates *0 of @health@ and @mana@ per turn. This effect stacks. 


**acao `The Good Bloom`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Call of the Wild · **PASSIVA**

`pendente`


**Texto:** Summoning skill cooldowns reduced by 1.


**attr:** `CooldownModSummon:Base:-1,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Circle of Life · **PASSIVA**

`pendente`


**Texto:** When an enemy dies, you have a 50% chance to spawn a Good Bloom or Bad Bloom.


**conferir:** 50% — sem par no codigo dumpado


## T4 Mass Entangle

`pendente`


**Texto:** Deals *0 physical damage and applies {STA=Immobilized} for 1 turn and @3@ stacks of {STA=Poisoned}.


**acao `Mass Entangle`:** `TargetStored['PhysicalDamage'] = Source.SpellPower('Physical') * .6f`


**status `Immobilized`:** efeitos=`Rooted:Set:1` classe=buff


> Cannot move.


**status `Poisoned`:** efeitos=`HealingReceivedBonus:Base:-1, PoisonDamage:Base:Mathf.Max(1, Source.GetCustomActionDamage("GL-Poisoned", "TargetStored[\"ShadowDamage\"] = Source.SpellPower(\"Shadow\") * .1f")), ContagionLevel:Base:Source["ContagionSource"] > 0 ? 1 : 0` classe=debuff


> Target takes [1] shadow damage each turn. Reduces healing taken by [0]%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Natural Selection · **PASSIVA**

`pendente`


**Texto:** When an Ally or an Enemy dies gain 5% of your max Health and Mana.


**conferir:** 5% — sem par no codigo dumpado


## T4 Rage Spores

`pendente`


**Texto:** Infects enemies and allies with Rage Spores that increase @damage dealt@ and reduce @damage reduction@ by 25% for 2 turns.


**expr:** `Source.SpellPower() * .5f * Source.DamageModShadow`


**acao `Rage Spores`:** `-`


**status `Rage Spores`:** efeitos=`DamageMod:Base:25, DamageReduction:Base:-25` classe=buff


> Increases damage dealt and received by 25%.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Rainstorm

`pendente`


**Texto:** Calls down a magical rain that increases potency of Mana using abilities by 50% for allies within the area. Lasts 2 turns.


**acao `Rainstorm`:** `-`


**conferir:** 50% — sem par no codigo dumpado


## T4 Sleep Spores

`pendente`


**Texto:** Infects enemies with Sleep Spores applying {STA=Sleep} for 2 turns.


**expr:** `Source.SpellPower() * .5f * Source.DamageModShadow`


**acao `Sleep Spores`:** `-`


**status `Sleep`:** efeitos=`Rooted:Set:1, Disabled:Set:1, DamageReduction:Base:-50` classe=indefinido


> Asleep.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Ecosystem · **PASSIVA**

`pendente`


**Texto:** Every summon active increases the @Max Life@, @Damage@ and @Healing@ of you and your summons by 5%.


**attr:** `DamageMod:Base:Source.SummonCount * 5f, MaxHealth:Percentage:Source.SummonCount * 5f, SummonDamageMod:Base:Source.SummonCount * 5f, SummonHealthMod:Base:Source.SummonCount * 5f,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Evolution · **PASSIVA**

`pendente`


**Texto:** Getting hit increases max health by 5% stacking 10x. Hitting increases damage by 5% stacking 10x. Only one of the buffs can be active at a time.


**conferir:** 5% — sem par no codigo dumpado


## T5 Mind Blossom

`corrigido`


**Texto:** Charm the enemy target for 1 turn.  Cannot target bosses.


**acao `Mind Blossom`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Nature Summoning III

`pendente`


**Texto:** Summons a Bear, Moose, or Panther to fight for you.


**acao `Nature Summoning III`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Pack Summoning III

`pendente`


**Texto:** Summons a Dire Wolf to fight for you.


**acao `Nature Summoning III  [Pack Summoning]`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Shapeshift Dire Werewolf

`pendente`


**Texto:** Shapeshift into a @Dire Werewolf@. Basic attack and abilities are further empowered. Increases @Max Health@ by 20%.


**acao `Shapeshift Greater Werewolf`:** `-`


**conferir:** 20% — sem par no codigo dumpado


## T5 Shapeshift Dragonkin

`corrigido`


**Texto:** Gain the ability to shapeshift into a powerful elemental @Dragonkin@. Empowers basic attack, grants new abilities, and resistance based on the color you choose. Increases @Armor@ by [0].


**expr:** `10 * Source.Level`


**acao `Shapeshift Red Dragonkin`:** `-`


**acao `Shapeshift Blue Dragonkin`:** `-`


**acao `Shapeshift Green Dragonkin`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Titan Bloom

`pendente`


**Texto:** Creates a magic mushroom that increases the @Max Health@ and @Damage@ of allies within its aura by [0]%. Stacks up to 5 times.


**expr:** `15`


**acao `Titan Bloom`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok

