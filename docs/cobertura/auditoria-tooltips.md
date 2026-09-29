# Auditoria de conteudo das tooltips de skill (RV-8b)

> `python tools/audit_tooltips.py` — 417 skills, Bard e demais intocaveis fora.


| checagem | achados |
|---|---:|
| A · causa dano e não diz o **tipo** de dano | 0 |
| B · causa dano e não tem **valor dinâmico** | 0 |
| C · efeito em **área** sem menção de área no texto | 0 |
| D · descrição **curta/vazia** (candidata a flavor) | 1 |
| E2 · famílias por **nome** com abertura divergente (precisa) | 2 |
| E · famílias por **fecho** com abertura divergente (candidatas) | 35 |

> Nem todo achado é defeito: D costuma ser skill que **não deve ser explicada**
> (flavor) e A/B podem ser texto gerado por expressão. A auditoria levanta, a
> revisão decide.


## A · Sem tipo de dano (0)

Nenhum.


## B · Sem valor dinâmico (0)

Nenhum.


## C · Area sem texto de area (0)

Nenhum.


## D · Descricao curta/vazia (1)

| arvore | skill | descricao |
|---|---|---|
| Light | Light's Strength | Increase @might@ by 20%. |

## E2 · Famílias por NOME com abertura divergente (2)

Skills que compartilham a primeira palavra do nome deveriam abrir a descrição do mesmo jeito. **É aqui que vale a regra do padrão da maioria** — e a maioria costuma estar no próprio nome:


**Raise \*** — aberturas: {'raise': 4, 'summon': 3}

| skill | arvore | descricao |
|---|---|---|
| Raise Iron Golem | Shadow | Raise a Mighty Iron Golem to fight for you. |
| Raise Skeletal Archer | Shadow | Summon a skeletal archer to fight by your side. |
| Raise Skeletal Mage | Shadow | Summon a skeletal mage to fight by your side. |
| Raise Skeletal Warrior | Shadow | Summon a skeletal warrior to fight by your side. |
| Raise Undead Berserker | Shadow | Raise an Undead Berserker to fight by your side. |
| Raise Undead Ranger | Shadow | Raise an Undead Ranger to fight by your side. |
| Raise Undead Wizard | Shadow | Raise a Undead Wizard to fight by your side. |

**Shapeshift \*** — aberturas: {'shapeshift': 3, 'gain': 1}

| skill | arvore | descricao |
|---|---|---|
| Shapeshift Dire Werewolf | Nature | Shapeshift into a @Dire Werewolf@. Basic attack and abilities are further empowered. Increases @Max Health@ by |
| Shapeshift Dragonkin | Nature | Gain the ability to shapeshift into a powerful elemental @Dragonkin@. Empowers basic attack, grants new abilit |
| Shapeshift Vampire Bat | Innate | Shapeshift into a @Vampire Bat@. Gain new abilities. @Movement@ increased. Immune to @attacks of opportunity@. |
| Shapeshift Werewolf | Nature | Shapeshift into a @Werewolf@. Empowers your basic attack and gain new abilities. Increases @Max Health@ by 10% |

## E · Famílias por FECHO divergentes — candidatas (35)

Mesmo fecho de frase, abertura diferente — é aqui que se aplica a regra do **padrão da maioria** (a maioria costuma estar no próprio nome da skill):


**…in range** — aberturas: {'hurls': 2, 'breathe': 2, 'expel': 1, 'slash': 2, 'creates': 1}

| skill | arvore | descricao |
|---|---|---|
| Abyssal Night | Shadow | Hurls an orb of dark energy dealing *0 shadow damage to all targets in range. |
| Breath of Life | Light | Breathe out a stream of holy light dealing *0 holy damage to all enemies and healing *0 to all allies in range |
| Celestial Light | Light | Expel a powerful celestial light blinding enemies and dealing *0 holy damage to all enemies and healing *1 to  |
| Fireball | Fire | Hurls a ball of flame dealing *0 fire damage to all targets in range. |
| Holy Slash | Basic | Slash nearby targets dealing *0 holy damage to all enemies and healing *1 to all allies in range. |
| Shadow Breath | Shadow | Breathe out a stream of shadow energy dealing *0 shadow damage to all enemies in range. |
| Shadow Claw | Basic | Slash nearby targets dealing *0 shadow damage to all enemies in range. |
| The Bad Bloom | Nature | Creates a magic flower that applies 2 stacks of {STA=Poisoned} per turn to enemies in range. |

**…within hexes** — aberturas: {'deal': 2, 'deals': 1, 'decreases': 1, 'moves': 1}

| skill | arvore | descricao |
|---|---|---|
| Ambush I | Thief | Deal 16% @increased damage@ when an enemy has no allies within 3 hexes. |
| Ambush II | Thief | Deal an additional 24% @increased damage@ when an enemy has no allies within 3 hexes. |
| Quaking Fist | Monk | Deals *0 physical damage to all foes within 3 hexes.  |
| Seal of Protection | Light | Decreases damage taken by 10% for you and allies within 3 hexes. |
| Telekinesis | Chaos | Moves any @Object@ within 8 hexes. |

**…your character** — aberturas: {'continually': 1, 'deals': 2, 'teleport': 1}

| skill | arvore | descricao |
|---|---|---|
| Aura of Flame | Fire | Continually deals *0 fire damage to enemies within 3 hexes of your character. |
| Aura Of Frost | Cold | Deals *0 cold damage to enemies that start their turns within 3 hexes of your character. |
| Detonate | Fire | Deals *0 fire damage to all foes within 2 hexes of your character. |
| Light's Beckon | Light | Teleport any target on the battlefield within 3 hexes of your character. |

**…lightning damage** — aberturas: {'each': 1, 'shoots': 1, 'increases': 1, 'summon': 1}

| skill | arvore | descricao |
|---|---|---|
| Aura of Lightning | Lightning | Each time an action is made by an enemy within the aura they suffer *0 lightning damage.  |
| Dazzling Darts | Lightning | Shoots 3 darts of electricity each dealing *0 lightning damage. |
| Lightning Shield | Lightning | Increases @Lightning Resistance@ by 10%. Attackers take *0 lightning damage. |
| Thunder Bolt | Lightning | Summon lightning from the sky to strike an area dealing *0 lightning damage.  |

**…per turn** — aberturas: {'each': 1, 'every': 2, 'grants': 1, 'call': 1, 'your': 1, 'target': 1, 'all': 1}

| skill | arvore | descricao |
|---|---|---|
| Avatar of Flame | Fire | Each stack of @heat@ now applies [0] fire damage to the target per turn. |
| Executioner | Warrior | Every enemy slain on your turn grants 1 additonal AP.  Can only grant up to 1 additional AP per turn. |
| Hunger | Shadow | Grants 10% @mana steal@.  Sacrifices 10% maximum health per turn. |
| Meteor | Fire | Call down a ball of fire to smash your enemies. Deals *0 fire damage within 2 hexes. Fire remains on the impac |
| Quick Hands | Ranger | Your basic attack has a 50% chance to strike twice.  Can only trigger once per turn. |
| Quickening | Light | Every time one of your Light skills is cast on an ally, one of the ally's spells has it's cooldown lowered by  |
| Regenerate | Light | Target restores *0 health per turn.  |
| Seal of Salvation | Light | All allies within 3 hexes of you heal for *0 per turn.  |

**…current bonus** — aberturas: {'of': 3, 'grants': 1, 'increases': 1}

| skill | arvore | descricao |
|---|---|---|
| Battle Ready | Warrior | 1% of your @Armor@ value is added to your character as @Additional Weapon Damage@.  Current Bonus: [0] |
| Diamond Ice | Cold | 1% of your @Armor@ value is added to your character as @Additional Cold Damage@.  Current Bonus: [0] |
| Invulnerable Winter | Cold | @Intelligence@ grants [0] @Armor@ and @Magic Armor@ per point.  Current Bonus: [1] |
| Perfected Soul | Monk | Increases all attributes by [0]. In addition, 10% of your highest attribute value is added to all other attrib |
| Weapon of Choice | Monk | 3% of your total attribute value is added to your character as @Additional Weapon Damage@.   Current Bonus: [0 |

**…increases by** — aberturas: {'increases': 2, 'shapeshift': 2, 'gain': 1}

| skill | arvore | descricao |
|---|---|---|
| Berserker's Rage | Warrior | Increases @Damage dealt@ and @damage received@ by 25%. Increases @Max Life@ by 15%. |
| Rage | Warrior | Increases @Damage dealt@ and @Max Life@ by 15%.  Increases @damage received@ by 15%. |
| Shapeshift Dire Werewolf | Nature | Shapeshift into a @Dire Werewolf@. Basic attack and abilities are further empowered. Increases @Max Health@ by |
| Shapeshift Dragonkin | Nature | Gain the ability to shapeshift into a powerful elemental @Dragonkin@. Empowers basic attack, grants new abilit |
| Shapeshift Werewolf | Nature | Shapeshift into a @Werewolf@. Empowers your basic attack and gain new abilities. Increases @Max Health@ by 10% |

**…stacks of** — aberturas: {'deals': 6, 'your': 1, 'all': 1, 'hurls': 2, 'throw': 1, 'conjure': 1}

| skill | arvore | descricao |
|---|---|---|
| Bleeding Shot | Ranger | Deals *0 weapon damage.  Applies 2 stacks of {STA=Bleeding}. |
| Entangle | Nature | Deals *0 physical damage and applies {STA=Immobilized} for 1 turn and @2@ stacks of {STA=Poisoned}. |
| Fight Dirty | Thief | Your attacks apply 2 stacks of {STA=Poisoned}. |
| Fire Starter | Fire | All enemies now start the battle with 4 stacks of @Heat@.  |
| Frozen Orb | Cold | Hurls a ball of Ice dealing *0 cold damage to all targets in range. Applies 5 stacks of {STA=Chilled} |
| Garrote | Thief | Deals *0 weapon damage. Applies {STA=Disabled} to the target for 1 turn and applies 3 stacks of {STA=Bleeding} |
| Gouge | Thief | Deals *0 weapon damage.  Applies 2 stacks of {STA=Bleeding}. |
| Mass Entangle | Nature | Deals *0 physical damage and applies {STA=Immobilized} for 1 turn and @3@ stacks of {STA=Poisoned}. |
| Poisoned Dagger | Thief | Throw a poisoned dagger dealing *0 weapon damage.  Applies 2 stacks of {STA=Poisoned}. |
| Rupture | Thief | Deals *0 weapon damage. Applies {STA=Disabled} for 1 turn and applies 6 stacks of {STA=Bleeding}. |
| Sun Fire | Fire | Hurls a ball of flame dealing *0 fire damage to all targets in range. Applies 10 stacks of {STA=Heat} |
| Thunder Blast | Innate | Conjure a storm of lightning dealing *0 lightning damage to all targets in range. Applies 10 stacks of {STA=Sh |

**…and by** — aberturas: {'bless': 1, 'curse': 1, 'increases': 5}

| skill | arvore | descricao |
|---|---|---|
| Bless | Light | Bless all allies within 5 hexes.  Increases @damage@, @maximum health@, and @maximum Mana@ by 10%. |
| Curse | Shadow | Curse the target lowering @All resistances@ by 20% and @Healing Received@ by 50%. |
| Opportunist | Warrior | Increases damage of @opportunity attacks@ and @counter attacks@ by 25%. |
| Speed | Monk | Increases @Dexterity@ and @Reflex@ by 15%. |
| Strength | Monk | Increases @Might@ and @Vitality@ by 15%. |
| Survivalist I | Ranger | Increases @all resistance@ and @dodge chance@ by 3%. |
| Tempered Rage | Warrior | Increases @Damage@, @Armor@, and @Magic Armor@ by 15%. |

**…reduced by** — aberturas: {'mana': 1, 'gain': 1, 'summoning': 1, 'increase': 1, 'damage': 1}

| skill | arvore | descricao |
|---|---|---|
| Blessed By Light I | Light | Mana costs reduced by 10%. |
| Bounty Hunter's Mark | Ranger | Gain 15% @increased damage@ and 8% @critical hit chance@ against the target.  If the target dies while Bounty  |
| Call of the Wild | Nature | Summoning skill cooldowns reduced by 1. |
| Dark Pact | Shadow | Increase the effectiveness of your damage and healing skills by 30%.   Maximum health reduced by 20%. |
| Take Cover | Ranger | Damage you take from enemies further than 2 hexes from you is reduced by 35%. |

**…an additional** — aberturas: {'mana': 1, 'max': 2, 'increases': 7, 'increase': 5, 'deals': 1, 'your': 1, 'each': 2, 'for': 1, 'every': 1}

| skill | arvore | descricao |
|---|---|---|
| Blessed By Light II | Light | Mana costs reduced by an additional 15%. |
| Contemplation II | Monk | Max Mana increased by an additional 15%. |
| Crystalize II | Cold | Increases @Physical Resistance@ by an additional 10%. |
| Death Dealer II | Thief | Increase @Critical Hit Damage and Healing@ by an additional 24%. |
| Deathblow | Thief | Deals *1 weapon damage. Critical hits deal an additional 200% @Critical Hit Damage@. |
| Empowered Light II | Light | Increases Holy Power and Healing Received by an additional 15%. |
| Endurance II | Monk | Max Health increased by an additional 15%. |
| Fencer's Finesse II | Thief | Increases @dodge chance@ by an additional 8%. |
| Frostbite II | Cold | Your stacks of @Chilled@ now reduce the targets damage by an additional 3%. |
| Fuel for the Flames II | Fire | Increase the mana cost of all skills by an additional 30% and increase the power of mana using skills by an ad |
| Guardian II | Warrior | Increase @Physical Resistance@ by an additional 10%. |
| Hot Head II | Fire | Increases Damage and Healing by an additional 12%.  |
| Momentum II | Monk | Each hex moved grants a stack of Momentum increasing the damage or healing of your next ability by an addition |
| Momentum III | Monk | Each hex moved grants a stack of Momentum increasing the damage or healing of your next ability by an addition |
| Omnism II | Chaos | Increases the effectiveness of shrines by an additional 12%. |
| Pack Hunter I | Nature | For every ally within 1 hex of you gain an additional 12% @increased Damage@. |
| Precision II | Ranger | Increase @critical hit chance@ by an additional 6%. Increase @critical hit damage@ by an additional 24%. |
| Ranger's Gift II | Ranger | Every hex between you and your target increases damage dealt by an additional 3%. |
| Storm Weathered II | Lightning | Increase all @elemental resistances@ by an additional 8%. |
| Stormbringer II | Lightning | Increases @critical hit chance@ by an additional 8%. |
| Survivalist II | Ranger | Increases @all resistance@ and @dodge chance@ by an additional 5%. |

**…for turn** — aberturas: {'deals': 7, 'strike': 2, 'whenever': 1, 'the': 2, 'gives': 1, 'kicks': 1, 'deal': 1, 'gain': 1}

| skill | arvore | descricao |
|---|---|---|
| Blind | Shadow | Deals *0 shadow damage.  Applies {STA=Blind} for 1 turn. |
| Chi Strike | Monk | Strike an enemy dealing *0 weapon damage.  Reduces the targets damage dealt by 20% for 1 turn. |
| Cripple | Thief | Deals *0 weapon damage.  Applies {STA=Slow} for 1 turn. |
| Cyclone Kick | Monk | Deals *0 physical damage. Pulls enemies within 4 hexes towards you. Targets are crippled for 1 turn.  |
| Fade | Thief | Whenever an enemy dies, you have a 50% chance to gain {STA=Stealth} for 1 turn.  |
| Glory | Light | The first time you receive fatal damage in battle you are revived with 1 health and become immune to all damag |
| Gore | Thief | Deals *0 weapon damage. Applies {STA=Disabled} for 1 turn.  |
| Maim | Thief | Deals *0 weapon damage.  Applies {STA=Disabled} for 1 turn. |
| Overload | Lightning | Gives the target 100% Critical Hit Chance for 1 turn.  |
| Pain Suppression | Monk | The target's Damage Reduction is increased by 50% for 1 turn. |
| Paralyzing Strike | Monk | Strike an enemy dealing *0 weapon damage.  Stuns the target for 1 turn. |
| Spectral Chains | Shadow | Deals *0 shadow damage and applies {STA=Immobilized} for 1 turn. |
| Stunning Kick | Monk | Kicks the target dealing *0 physical damage and stunning them for 1 turn. |
| Stunning Slam | Warrior | Deals *0 weapon damage and applies {STA=Stunned} to all enemies within a line for 1 turn. |
| Sweeping Kick | Monk | Deal *0 physical damage to all enemies within 1 hex. Knocks back all enemies up to 3 hexes. Targets are crippl |
| Uncanny Evasion | Thief | Gain 100% @dodge chance@ for the next attack. Increases @Counter Attack Damage@ by 50% for 1 turn. |

**…holy damage** — aberturas: {'summons': 1, 'heals': 2}

| skill | arvore | descricao |
|---|---|---|
| Blinding Light | Light | Summons a radiant light applying {STA=Blind} to the target dealing *0 Holy damage. |
| Staff Attack | Basic | Heals target ally for *0.    When targeting an enemy, deals *0 Holy Damage. |
| Unarmed Attack | Basic | Heals target ally for *0.    When targeting an enemy, deals *0 Holy Damage. |

**…cost abilities** — aberturas: {'increases': 3, 'deals': 2, 'swing': 1, 'reaches': 1, 'allies': 1}

| skill | arvore | descricao |
|---|---|---|
| Blood Drinker | Warrior | Increases basic attack damage by 50%. Basic attacks now @Life steal@ for 5%.  @Life Steal@ heals you for a per |
| Haunt | Shadow | Deals *0 shadow damage to the target every turn for 3 turns. @Life Steals@ for 6%.   @Life Steal@ heals you fo |
| Life Cleave | Warrior | Swing in a 180 degree arc striking all foes for *0 weapon damage.  Lifesteals for 10% per target hit.  @Life S |
| Sunder | Warrior | Deals *0 weapon damage. Ignores all armor and resists. Cannot be dodged. @Life Steals@ for 25%.  @Life Steal@  |
| Tainted Touch | Shadow | Reaches out to the target with dark energy dealing *0 shadow damage. @Life Steals@ for 12%.  @Life Steal@ heal |
| Thirst I | Shadow | Increases @Life Steal@ by 4%.  @Life Steal@ heals you for a percentage of your @max health@ each time you hit. |
| Thirst II | Shadow | Increases @Life Steal@ by 6%.  @Life Steal@ heals you for a percentage of your @max health@ each time you hit. |
| Vampiric Aura | Shadow | Allies within Vampiric Aura @Life Steal@ for 5%.  @Life Steal@ heals you for a percentage of your @max health@ |

**…for turns** — aberturas: {'howl': 2, 'deals': 5, 'grants': 1, 'consecrate': 1, 'incapacitates': 1, 'any': 1, 'infects': 3, 'tranquilizes': 1, 'summons': 1}

| skill | arvore | descricao |
|---|---|---|
| Blood Howl | Innate | Howl causing *0 physical damage to all enemies within 2 hexes.  Applies a debuff that causes all attackers to  |
| Cursed Bite | Innate | Deals *0 weapon damage and lowers target's @Healing@ received by 50% for 2 turns. |
| Dire Bite | Innate | Deals *0 weapon damage and lowers target's @Healing@ received by 50% for 2 turns. |
| Dire Howl | Innate | Howl causing *0 physical damage to all enemies within 2 hexes.  Applies a debuff that causes all attackers to  |
| Dispelling Fracture | Warrior | Deals *0 weapon damage, removes 1 random benefical status from the target and lowers the target's @Resistance@ |
| Fracture | Warrior | Deals *0 weapon damage.  Lowers targets @Resistance@ by 20% for 2 turns. |
| Hide In Shadows | Thief | Grants {STA=Stealth} for 2 turns.  |
| Holy Ground | Light | Consecrate an area of ground to heal allies that stand upon it. Heals *0 per turn for 3 turns.  |
| Incapacitate | Monk | Incapacitates the target applying {STA=Sleep} for 2 turns. |
| Lingering Light | Light | Any target you heal with Cure, Regenerate, Healing Hand, Mass Cure, or Divine Intervention also receives an ad |
| Mortal Fracture | Warrior | Deals *0 weapon damage and lowers target's @Resistance@ by 20% and @Healing@ received by 50% for 2 turns. |
| Rage Spores | Nature | Infects enemies and allies with Rage Spores that increase @damage dealt@ and reduce @damage reduction@ by 25%  |
| Sleep Spores | Nature | Infects enemies with Sleep Spores applying {STA=Sleep} for 2 turns. |
| Stun Spores | Nature | Infects enemies with Stunning Spores applying {STA=Stun} for 1 turns. |
| Tranquilizing Shot | Ranger | Tranquilizes the target applying {STA=Sleep} for 2 turns. |
| Twister | Lightning | Summons a raging tempest that deals *0 lightning damage in a line.  Targets hit are {STA=Crippled} for 2 turns |

**…turn applies** — aberturas: {'sacrifice': 1, 'target': 1, 'all': 1, 'steals': 1}

| skill | arvore | descricao |
|---|---|---|
| Bloodlet | Warrior | Sacrifice 15% of your maximum health in exchange for an additonal action this turn.  Applies {STA=Exhaustion}. |
| Haste | Fire | Target gains an additional action this turn. Applies {STA=Exhaustion}. |
| Mass Haste | Fire | All allies gain an additional action this turn. Applies {STA=Exhaustion}. |
| Steal Action | Thief | Steals the target's action granting 1 additional action this turn. Applies {STA=Disabled} to the target for 1  |

**…to times** — aberturas: {'every': 1, 'deals': 1, 'dash': 1, 'damage': 3, 'patient': 1, 'creates': 1}

| skill | arvore | descricao |
|---|---|---|
| Bone Collector | Warrior | Every enemy slain grants 6% @maximum health@ and @Increased Damage@.  Lasts the duration of the battle.  Stack |
| Chain Frost | Cold | Deals *0 cold damage.  Bounces between enemies within 4 hexes up to 10 times. |
| Dashing Strikes | Monk | Dash to an enemy dealing *0 weapon damage then quickly dash to an enemy within 2 hexes to strike again. Strike |
| Leech Dexterity | Shadow | Damage caused steals [0] points of @Dexterity@. Lasts the entire battle. Stacks up to 10 times. |
| Leech Intelligence | Shadow | Damage caused steals [0] points of @Intelligence@. Lasts the entire battle. Stacks up to 10 times. |
| Leech Might | Shadow | Damage caused steals [0] points of @Might@. Lasts the entire battle. Stacks up to 10 times. |
| Patient Hunter | Ranger | Patient Hunter gives 10% @increased damage@ and 1 @skill range@ per stack.  A stack is applied at the end of e |
| Titan Bloom | Nature | Creates a magic mushroom that increases the @Max Health@ and @Damage@ of allies within its aura by [0]%. Stack |

**…lasts turns** — aberturas: {'summon': 2, 'dash': 1, 'calls': 1, 'any': 1, 'causes': 1}

| skill | arvore | descricao |
|---|---|---|
| Brambles | Nature | Summon brambles to block 4 hexes. Attackers will take physical damage when striking the brambles. Lasts 4 turn |
| Dodging Strikes | Monk | Dash to an enemy dealing *0 weapon damage then quickly dash to an enemy within 2 hexes to strike again. Strike |
| Ice Wall | Cold | Summon pillars of ice to block 4 hexes blocking enemy's line of sight. Attackers take cold damage.  Lasts 4 tu |
| Rainstorm | Nature | Calls down a magical rain that increases potency of Mana using abilities by 50% for allies within the area. La |
| Salvation | Light | Any target you heal with Cure, Regenerate, Healing Hand, Mass Cure, or Divine Intervention also receives {STA= |
| Venomous Skin | Nature | Causes the skin of a target ally to secrete poison. Attacking enemies receive 3 stacks of {STA=Poisoned}. Last |

**…damage by** — aberturas: {'deals': 1, 'each': 1, 'your': 1}

| skill | arvore | descricao |
|---|---|---|
| Branching Shot | Ranger | Deals *0 weapon damage. Bounces to enemies within 3 hexes. Each bounce increases its damage by 50%. |
| Cold Heart | Cold | Each stack of chilled you've applied increases your cold damage by 5%. |
| Frostbite I | Cold | Your stacks of @chilled@ now reduce the targets damage by 2%. |

**…increased by** — aberturas: {'the': 1, 'max': 2, 'while': 2, 'physical': 2}

| skill | arvore | descricao |
|---|---|---|
| Break The Ice | Cold | The first time you deal damage or healing in battle, it's effectiveness is increased by 100%. |
| Contemplation I | Monk | Max Mana increased by 10%. |
| Dual-Wield Mastery | Warrior | While dual-wielding, @dodge chance@ increased by 5%, @critical hit chance@ increased by 5%, and @critical hit  |
| Endurance I | Monk | Max Health increased by 10%. |
| Huntsman I | Ranger | Physical damage increased by [0]. |
| Huntsman II | Ranger | Physical damage increased by [0]. |
| Two-Handed Mastery | Warrior | While a two handed weapon is equipped all damage is increased by 20%.  |

**…a cone** — aberturas: {'conjures': 1, 'breath': 2}

| skill | arvore | descricao |
|---|---|---|
| Breath of Winter | Cold | Conjures the breath of a frost dragon dealing *0 cold damage to all enemies in a cone.  |
| Fire Breath | Innate | Breath fire dealing *0 fire damage to all enemies in a cone.  |
| Lightning Breath | Lightning | Breath lightning dealing *0 lightning damage to all enemies in a cone.  |

**…when disabled** — aberturas: {'removes': 3, 'heals': 1}

| skill | arvore | descricao |
|---|---|---|
| Cauterize | Fire | Removes all negative statuses from friendly target but inflicts 10% of target's maximum health as fire damage. |
| Purify | Light | Removes all negative statuses from the target. Can be used when Disabled. |
| Soul Cleanse | Monk | Removes all negative status effects from target ally. Each status effect removed heals the target for 10% of t |
| Warrior's Boon | Warrior | Heals 25% of your maximum health and removes all negative statuses. Can be used when Disabled. |

**…each target** — aberturas: {'conjures': 1, 'hurls': 1, 'hurl': 1}

| skill | arvore | descricao |
|---|---|---|
| Chain Lightning | Lightning | Conjures a lightning bolt that chains up to 5 enemies near the target dealing *0 lightning damage to each targ |
| Fire Storm | Fire | Hurls fire balls at 3 different targets dealing *0 fire damage within 2 hexes of each target. |
| Frozen Spikes | Cold | Hurl 5 shards of ice dealing *0 cold damage to each target. |

**…deal damage** — aberturas: {'summons': 2, 'hurls': 1, 'creates': 1}

| skill | arvore | descricao |
|---|---|---|
| Chaos Cloud | Chaos | Summons a cloud of chaos that strikes 3 times. At every strike each damage type has a @50%@ chance to deal *0  |
| Chaos Crash | Chaos | Hurls a bolt of chaos dealing damage to a single target. Every damage type has a 50% chance to deal *0 damage. |
| Chaos Cut | Chaos | Summons a whirling blade of chaos in a line. Every damage type has a 50% chance to deal *0 damage. |
| Replicate | Chaos | Creates a clone of yourself that can cast your abilities. The Replicate Clone explodes for damage on death, ea |

**…cold damage** — aberturas: {'the': 2, 'envelopes': 1, 'impale': 1}

| skill | arvore | descricao |
|---|---|---|
| Chilling Strike | Cold | The caster's hand becomes imbued with frost thrusting it at the target dealing *0 cold damage. |
| Frost Armor | Cold | Envelopes the caster in frost granting 10% @Cold Resistance@.   Attackers take *0 cold damage. |
| Frost Shard | Cold | Impale your target on a shard of ice dealing *0 cold damage. |
| Ice Lance | Cold | The caster hurls a razor-like shard of ice piercing foes in a line dealing *0 cold damage.  |

**…each turn** — aberturas: {'gain': 1, 'faeries': 1, 'deals': 1, 'conjure': 1, 'burns': 1, 'envelopes': 1}

| skill | arvore | descricao |
|---|---|---|
| Conduit | Lightning | Gain an additional action each turn. |
| Faerie Swarm | Nature | Faeries swarm the target clawing and biting for *0 physical damage and applying 1 stack of {STA=Bleeding}  eac |
| Frost Breath | Innate | Deals *0 cold damage each turn. |
| Ice Storm | Cold | Conjure a massive ice storm dealing *0 cold damage to affected enemies each turn. |
| Immolate | Fire | Burns the target for *0 fire damage each turn. |
| Living Armor | Nature | Envelopes the target in living vines that increase @armor@ and @magic armor@ by [0] and causes the target to r |

**…lasts turn** — aberturas: {'dodging': 1, 'gain': 2}

| skill | arvore | descricao |
|---|---|---|
| Crash and Flow | Monk | Dodging an attack increases your damage dealt by 10%. Stacks 5. Lasts 1 turn. |
| Masochism I | Monk | Gain a stack of Masochism each time you take damage. Each stack increases the damage/healing you deal by 2%. L |
| Masochism II | Monk | Gain a stack of Masochism each time you take damage. Each stack increases the damage/healing you deal by an ad |

**…the target** — aberturas: {'intense': 1, 'deals': 2, 'reaches': 1, 'encases': 1, 'steals': 1}

| skill | arvore | descricao |
|---|---|---|
| Deep Freeze | Cold | Intense frost encircles your foe applying 5 stacks of {STA=Chilled} on the target. |
| Dispelling Shot | Ranger | Deals *0 weapon damage. Removes 1 random benefical status from the target. |
| Reaper's Scythe | Shadow | Deals *0 shadow damage for every 10% health missing from the target. |
| Shock | Lightning | Reaches out and shocks the target dealing *0 lightning damage. Applies {STA=Disabled} to the target. |
| Stasis | Cold | Encases the friendly target in a dome of ice granting [0] Armor and Magic Armor for the duration. Immobilizes  |
| Steal Status | Thief | Steals a random positive status from the target. |

**…taking damage** — aberturas: {'teleport': 1, 'chance': 2}

| skill | arvore | descricao |
|---|---|---|
| Displacement | Chaos | Teleport randomly when taking damage. |
| Disruption I | Chaos | 4% chance to negate all damage when taking damage. |
| Disruption II | Chaos | 6% chance to negate all damage when taking damage. |

**…range modifiers** — aberturas: {'teleport': 2, 'jump': 1, 'teleports': 2}

| skill | arvore | descricao |
|---|---|---|
| Escape | Thief | Teleport to the target area.  Unaffected by increased range modifiers. |
| Relocate | Ranger | Jump to the target area.  Unaffected by increased range modifiers. |
| Shadow Walk | Thief | Teleport through the shadows. Applies {STA=Stealth} for this turn.  Unaffected by increased range modifiers. |
| Teleport Other | Lightning | Teleports the target to the location of your choosing in a flash of lightning.  Unaffected by increased range  |
| Teleport Self | Lightning | Teleports the caster to the target location in a flash of lightning.  Unaffected by increased range modifiers. |

**…all enemies** — aberturas: {'slash': 3, 'applies': 2}

| skill | arvore | descricao |
|---|---|---|
| Flame Slash | Basic | Slash nearby targets dealing *0 fire damage to all enemies. |
| Ice Slash | Basic | Slash nearby targets dealing *0 cold damage to all enemies. |
| Malevolence | Chaos | Applies @Hurting@ to all enemies. |
| Mass Freeze | Cold | Applies {STA=Frozen} to all enemies. |
| Thunder Slash | Basic | Slash nearby targets dealing *0 lightning damage to all enemies. |

**…physical damage** — aberturas: {'kicks': 1, 'grants': 2}

| skill | arvore | descricao |
|---|---|---|
| Force Kick | Monk | Kicks the target dealing *0 physical damage and knocking the target back up to 5 hexes.   Any enemy hit by the |
| Thorns I | Nature | Grants [0] Return Physical Damage. |
| Thorns II | Nature | Grants an additional [0] Return Physical Damage. |

**…and mana** — aberturas: {'put': 1, 'when': 1, 'consuming': 2}

| skill | arvore | descricao |
|---|---|---|
| Meditation | Monk | Put the target ally into a meditative state restoring 20% of max health and mana.  |
| Natural Selection | Nature | When an Ally or an Enemy dies gain 5% of your max Health and Mana. |
| Sustenance I | Chaos | Consuming any Globule heals you for 8% of max life and mana. |
| Sustenance II | Chaos | Consuming any Globule heals you for 20% of max life and mana. |

**…for you** — aberturas: {'summons': 6, 'raise': 1}

| skill | arvore | descricao |
|---|---|---|
| Nature Summoning I | Nature | Summons a Raven, Coyote, or Raccoon to fight for you. |
| Nature Summoning II | Nature | Summons a Stag, Wolf, or Boar to fight for you. |
| Nature Summoning III | Nature | Summons a Bear, Moose, or Panther to fight for you. |
| Pack Summoning I | Nature | Summons a Timber Wolf to fight for you |
| Pack Summoning II | Nature | Summons a Tundra Wolf to fight for you. |
| Pack Summoning III | Nature | Summons a Dire Wolf to fight for you. |
| Raise Iron Golem | Shadow | Raise a Mighty Iron Golem to fight for you. |

**…your side** — aberturas: {'summon': 3, 'raise': 3}

| skill | arvore | descricao |
|---|---|---|
| Raise Skeletal Archer | Shadow | Summon a skeletal archer to fight by your side. |
| Raise Skeletal Mage | Shadow | Summon a skeletal mage to fight by your side. |
| Raise Skeletal Warrior | Shadow | Summon a skeletal warrior to fight by your side. |
| Raise Undead Berserker | Shadow | Raise an Undead Berserker to fight by your side. |
| Raise Undead Ranger | Shadow | Raise an Undead Ranger to fight by your side. |
| Raise Undead Wizard | Shadow | Raise a Undead Wizard to fight by your side. |
