# Ficha de revisao — arvore **Light** (36 skills)

> Gerado por `tools/verify_tree.py`. Junta o TEXTO da tooltip com o que o jogo
> CALCULA. A ultima linha de cada ficha (`conferir`) lista o que **nao** tem par no
> codigo — e o que precisa de olho humano ou triangulacao externa, nao veredito.


## T1 Blessed By Light I · **PASSIVA**

`pendente`


**Texto:** Mana costs reduced by 10%.


**attr:** `ManaCostMod:Base:-10,`


**conferir:** 10% — sem par no codigo dumpado


## T1 Breath of Life

`pendente`


**Texto:** Breathe out a stream of holy light dealing *0 holy damage to all enemies and healing *0 to all allies in range.


**expr:** `Source.SpellPower('Light') * 1.6f * Source.DamageModLight`


**acao `Dragonkin Holy Breath`:** `TargetStored['HolyDamage'] = Source.SpellPower('Light') * 1.6f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Cure

`pendente`


**Texto:** Restores target's health by *0.


**expr:** `Source.SpellPower() * 1.5f * Source.DamageModHealing`


**acao `Cure`:** `TargetStored['Healing'] = Source.SpellPower('Light') * 1.5f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Elemental Protection

`pendente`


**Texto:** Increases target's @elemental resistance@ by 15%. 


**acao `Elemental Protection`:** `-`


**conferir:** 15% — sem par no codigo dumpado


## T1 Empowered Light I · **PASSIVA**

`pendente`


**Texto:** Increases Holy Power and Healing Received by 10%.


**attr:** `DamageModHealing:Base:10, HealingReceivedBonus:Base:10,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T1 Healing Hand

`pendente`


**Texto:** The caster reaches out in aid healing 30% of target's maximum health.


**acao `Healing Hand`:** `TargetStored['Healing'] = Target['MaxHealth'] * .3f`


**conferir:** 30% — sem par no codigo dumpado


## T1 Regenerate

`pendente`


**Texto:** Target restores *0 health per turn. 


**expr:** `Source.SpellPower() * .5f * Source.DamageModHealing`


**acao `Regenerate`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Bless

`corrigido`


**Texto:** Bless all allies within 5 hexes.  Increases @damage@, @maximum health@, and @maximum Mana@ by 10%.


**acao `Bless`:** `-`


**status `Bless`:** efeitos=`MaxHealth:Percentage:10, MaxMana:Percentage:10, DamageMod:Base:10` classe=buff


> @Maximum health@ and @maximum mana@ increased by 10%.  @Damage dealt@ increased by 10%.


**conferir:** 5 hex — sem par no codigo dumpado


## T2 Blessed By Light II · **PASSIVA**

`pendente`


**Texto:** Mana costs reduced by an additional 15%.


**attr:** `ManaCostMod:Base:-15,`


**conferir:** 15% — sem par no codigo dumpado


## T2 Blinding Light

`pendente`


**Texto:** Summons a radiant light applying {STA=Blind} to the target dealing *0 Holy damage.


**expr:** `Source.SpellPower() * .8f * Source.DamageModHealing`


**acao `Blinding Light`:** `TargetStored['HolyDamage'] = Source.SpellPower('Holy') * .8f`


**status `Blind`:** efeitos=`Blind:Set:1` classe=buff


> Blind.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Celestial Light

`pendente`


**Texto:** Expel a powerful celestial light blinding enemies and dealing *0 holy damage to all enemies and healing *1 to all allies in range.


**danoExpr:** `TargetStored['HolyDamage'] = Source.SpellPower('Light') * 2f; TargetStored['Healing'] = Source.SpellPower('Light') * 2.3f`


**acao `Dragonkin Holy Blast`:** `TargetStored['HolyDamage'] = Source.SpellPower('Light') * 2f`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Empowered Light II · **PASSIVA**

`pendente`


**Texto:** Increases Holy Power and Healing Received by an additional 15%.


**attr:** `DamageModHealing:Base:15, HealingReceivedBonus:Base:15,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Glory · **PASSIVA**

`pendente`


**Texto:** The first time you receive fatal damage in battle you are revived with 1 health and become immune to all damage for 1 turn.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Kindred Spirit · **PASSIVA**

`pendente`


**Texto:** All healing you do to others also heals you for 20% of the amount healed.


**attr:** `HealingReturned:Base:20,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T2 Seal of Protection

`pendente`


**Texto:** Decreases damage taken by 10% for you and allies within 3 hexes.


**acao `Seal of Protection`:** `-`


**conferir:** 10%, 3 hex — sem par no codigo dumpado


## T2 Shield of Light

`pendente`


**Texto:** Calls down a shield that protects the target absorbing *0 damage. 


**expr:** `Source.SpellPower() * 1.6f * Source.DamageModHealing`


**danoExpr:** `TargetStored['Healing'] = Source.SpellPower('Light') * 1.6f`


**acao `Shield Of Light`:** `Target['ShieldOfLightValue'] = Source.GetCustomActionDamage('Shield Of Light', 'TargetStored[\'Healing\'] = Source.SpellPower(\'Light\') * 1.6f')`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Light's Beckon

`pendente`


**Texto:** Teleport any target on the battlefield within 3 hexes of your character.


**acao `Light's Beckon`:** `-`


**conferir:** 3 hex — sem par no codigo dumpado


## T3 Light's Brilliance · **PASSIVA**

`pendente`


**Texto:** Increase @intelligence@ by 20%.


**attr:** `IntelligenceBase:Percentage:20,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Light's Celerity · **PASSIVA**

`pendente`


**Texto:** Increase @dexterity@ by 20%.


**attr:** `DexterityBase:Percentage:20,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Light's Endurance · **PASSIVA**

`pendente`


**Texto:** Increase @vitality@ by 20%.


**attr:** `VitalityBase:Percentage:20,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Light's Intuition · **PASSIVA**

`pendente`


**Texto:** Increase @reflex@ by 20%.


**attr:** `ReflexBase:Percentage:20,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Light's Strength · **PASSIVA**

`pendente`


**Texto:** Increase @might@ by 20%.


**attr:** `MightBase:Percentage:20,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Mass Cure

`pendente`


**Texto:** Restores *0 health to all allies within 2 hexes of target.


**expr:** `Source.SpellPower() * 1.8f * Source.DamageModHealing`


**acao `Mass Cure`:** `TargetStored['Healing'] = Source.SpellPower('Light') * 1.8f`


**conferir:** 2 hex — sem par no codigo dumpado


## T3 Purify

`pendente`


**Texto:** Removes all negative statuses from the target. Can be used when Disabled.


**acao `Purify`:** `-`


**status `Disabled`:** efeitos=`Disabled:Set:1` classe=buff


> Cannot perform actions.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T3 Seal of Might

`pendente`


**Texto:** Increase damage of all allies within 3 hexes by 30%.


**acao `Seal of Might`:** `-`


**conferir:** 3 hex, 30% — sem par no codigo dumpado


## T4 Divine Intervention

`pendente`


**Texto:** Restores the target to full health.


**acao `Divine Intervention`:** `TargetStored['Healing'] = Target['MaxHealth']`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Holy Ground

`pendente`


**Texto:** Consecrate an area of ground to heal allies that stand upon it. Heals *0 per turn for 3 turns. 


**expr:** `Source.SpellPower() * .75f * Source.DamageModHealing`


**acao `Holy Ground`:** `-`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Lingering Light · **PASSIVA**

`pendente`


**Texto:** Any target you heal with Cure, Regenerate, Healing Hand, Mass Cure, or Divine Intervention also receives an additional healing over time effect restoring *0 health for 3 turns.


**expr:** `Source.SpellPower() * .4f * Source.DamageModHealing`


**status `Regenerate`:** efeitos=`-` classe=indefinido


> Restores *0 health per turn.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Quickening · **PASSIVA**

`corrigido`


**Texto:** Every time one of your Light skills is cast on an ally, one of the ally's spells has it's cooldown lowered by 1 turn.  This effect can only happen once per turn.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 Shield of Retribution

`pendente`


**Texto:** Conjures a shield imbued with holy flame absorbing *0 damage. Upon shield depletion, it explodes and deals *0 holy damage to all foes in a 3 hex radius.


**expr:** `Source.SpellPower() * 3f * Source.DamageModHealing`


**danoExpr:** `TargetStored['Healing'] = Source.SpellPower('Healing') * 3f`


**acao `Shield Of Retribution`:** `Target['ShieldOfRetributionValue'] = Source.GetCustomActionDamage('Shield Of Retribution', 'TargetStored[\'Healing\'] = Source.SpellPower(\'Healing\') * 3f'); Target['ShieldOfRetributionStartValue'] =`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T4 The Good Doctor · **PASSIVA**

`pendente`


**Texto:** Reduces the cooldown of all Light spells by 1.


**attr:** `CooldownModLight:Base:-1,`


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Ascendancy

`revisado`


**Texto:** Increases the target allies' stats by 20%.


**acao `Ascendancy`:** `-`


**conferir:** 20% — sem par no codigo dumpado


## T5 Redemption · **PASSIVA**

`corrigido`


**Texto:** Redeem the soul of the first character to die in your party.  The target's health and mana are fully restored.  Does not affect summoned creatures.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Salvation · **PASSIVA**

`corrigido`


**Texto:** Any target you heal with Cure, Regenerate, Healing Hand, Mass Cure, or Divine Intervention also receives {STA=Salvation}.  Lasts 3 turns.


**status `Regenerate`:** efeitos=`-` classe=indefinido


> Restores *0 health per turn.


**status `Salvation`:** efeitos=`MaxHealth:Percentage:10` classe=buff


> @Maximum health@ increased by 10% per stack.


**conferir:** tudo o que o texto afirma tem par no codigo — ok


## T5 Seal of Salvation

`pendente`


**Texto:** All allies within 3 hexes of you heal for *0 per turn. 


**expr:** `Source.SpellPower() * 1f * Source.DamageModHealing`


**acao `Seal of Salvation`:** `-`


**conferir:** 3 hex — sem par no codigo dumpado


## T5 Wrath of the  Righteous · **PASSIVA**

`pendente`


**Texto:** Healing skills in the Light tree can now deal damage to enemies as well as heal allies.


**conferir:** tudo o que o texto afirma tem par no codigo — ok

