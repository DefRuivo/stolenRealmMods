# RV-9 — Triagem dos números (grupo `Normal`)

Gerado por `tools/check_status_numeros.py`. **Isto é triagem, não veredito**: o script
não julga se o texto está certo — separa quem cita um número que **não existe em efeito
nenhum** do asset, que é onde o defeito ou a omissão costuma estar.

## Números

| o que | quantos |
|---|---|
| status no grupo | 457 |
| todo número da descrição tem par nos efeitos | 363 |
| com número sem par — conferir | **39** |

> Falsos positivos esperados: **duração** ("for 2 turns") não mora nos efeitos — mora no
> campo de duração; percentuais podem vir de `StatusPower`. Conferir sempre o texto
> COMPLETO antes de decidir (lição do RV-8c: uma nota redundante no `Meteor`).

## Fila de triagem

| status | tipo | número sem par | descrição | efeitos |
|---|---|---|---|---|
| `Anthulk Carapace` | Common | 50 | 50% chance to cast Anthulk Spines when struck. |  |
| `Anthulk Venom` | Common | 10 | The target takes [0] increased flat physical damage. Stacks up to 10 times. | DamageFlatPhysicalTarget:Base:ActionStatus.GetFlatDamageVa |
| `Ascendancy` | Common | 5 | Increases target ally's stats by 20%.  Lasts 5 turns.  | MightBase:Percentage:20, DexterityBase:Percentage:20, Vita |
| `Blessing of the Seraph` | Common | 5 | Recover 5% Max Health and Mana per turn. | Recovery:Base:10 |
| `Brain Freeze` | Common | 8 | Deals 8% of the targets Max Health in cold damage each time the target perform |  |
| `Champion of Blood` | Common | 10 | Striking enemies heals the Countess for 10% of her Max Health |  |
| `Chaos Curse` | Common | 50 | Cursed to take damage. Each element has a @50%@ chance to deal *0 damage every | TargetStored['ColdDamage'] = Source.GetRollResult(50) ? So |
| `Chilled` | Common | 2 | Movement points reduced by one per stack.  Lasts 2 turns.  Five stacks of Chil | TurnFreeMovementPoints:Base:Target.CanBeEffectedByChilled  |
| `Crystal Bite` | Common | 5 | Target takes *0 shadow damage each turn, increases damage taken by 10% and red | DamageReduction:Base:-10, TurnFreeMovementPoints:Base:-1 |
| `Deal with a Devil` | Common | 808080 | <i><color=#808080>You've made a deal with a devil!</i></color>   Increases exp | GoldMod:Base:50, DropQuantityMod:Base:50, ExperienceMod:Ba |
| `Disappointment` | Common | 2,4 | The disappointment of <color=#EE4B2B><b>Shawn</b></color> follows your every m | DamageMod:Base:-20 |
| `Evolution` | Common | 10 | Damage increased by 5% per stack.  Can stack up to 10 times. | DamageMod:Base:5 |
| `Evolution` | Common | 10 | Max Health increased by 5% per stack.  Can stack up to 10 times. | MaxHealth:Percentage:5 |
| `Faerie Swarm` | Common | 1 | Target takes *0 physical damage and 1 stack of {STA=Bleeding} per turn. | TargetStored['PhysicalDamage'] = Source.SpellPower('Physic |
| `Freeze Earth` | Common | 1 | Applies 1 stack of Chilled. |  |
| `Frenzy` | Common | 1 | Action Points Increase by 1. |  |
| `Haunt` | Common | 8 | Deals *0 damage. Lifesteals for 8%. | TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') |
| `Heat` | Common | 10 | Elemental resistance reduced by 5% per stack.  Lasts [0] turns.  Can stack up  | ResistCold:Base:-5, ResistFire:Base:-5, ResistLightning:Ba |
| `Hunger of Ksvaldir` | Common | 10 | Sacrifices 10% maximum health per turn. | TargetStored['ShadowDamage'] = Target.MaxHealth * .1f |
| `Leech Dexterity` | Common | 10 | [0] @dexterity@ absorbed per stack.  Stacks up to 10 times. | DexterityBase:Base:2 * (.1f * Target.Level) |
| `Leech Intelligence` | Common | 10 | [0] @intelligence@ absorbed per stack.  Stacks up to 10 times. | IntelligenceBase:Base:2 * (.1f * Target.Level) |
| `Leech Might` | Common | 10 | [0] @might@ absorbed per stack.  Stacks up to 10 times. | MightBase:Base:2 * (.1f * Target.Level) |
| `Overcharge` | Common | 10 | Adds *0 lightning damage to your next basic attack.  Can stack up to 10 times. |  |
| `Petrification` | Common | 5 | Each stack lowers @movement@ by 1 and increases @Damage Taken@ by 20%. When yo | TurnFreeMovementPoints:Base:-1, DamageReduction:Base:-20 |
| `Poison Thorns` | Common | 2 | Attackers take 2 stacks of poison. |  |
| `Poison Weapon` | Common | 1 | Attacks apply @1@ stack of poison. |  |
| `Quick Draw` | Common | 3 | Your next 3 basic attacks have no AP cost. | QuickDraw:Set:1 |
| `Rage Unleashed` | Common | 808080 | @Damage@ dealt and taken increased by @50@%.  <i><color=#808080>"You have give | DamageMod:Base:50, DamageReduction:Base:-50 |
| `Raise Skeletal Lackey` | Common | 50 | Max Health, Damage, Armor, and Dodge Chance reduced by 50%. | MaxHealth:Multiplicative:.5, DamageMod:Multiplicative:.5,  |
| `Resonating Refrain` | Common | 4 | Deals [0] physical damage in a 4 hex area whenever you act. |  |
| `Ruby of Rancor` | Common | 25,100,3 | 3 extra Action Points granted. Mana Costs reduced by {25,100}%. Die at the end | ManaCostMod:Set:{-25,-100} |
| `Shocked` | Common | 3 | Incoming critical strike damage increased by 10% per stack.  Lasts 3 turns.  C | CritDamageTarget:Base:10 |
| `Spore Cloud` | Common | 5 | Decreases damage dealt by 10% and movement by 1. Stacks up to 5 times. | DamageMod:Base:-10, TurnFreeMovementPoints:Base:-1 |
| `Stealth` | Common | 100 | Invisible.  Attacking from Stealth has 100% critical hit chance. | Hidden:Set:1, UntargetableByEnemies:Set:1 |
| `Stealth` | Common | 100 | Invisible. Attacking from Stealth has 100% critical hit chance. | Hidden:Set:1, UntargetableByEnemies:Set:1 |
| `Stoney Visage` | Common | 1 | Enemies gain 1 stack of Petrification when hitting Medusa. |  |
| `The Bad Bloom` | Common | 2 | Enemies gain 2 stacks of poison. |  |
| `Toxic` | Common | 2 | Applies @2@ @poison@ when striking Applies @2@ @poison@ when struck |  |
| `Venomous Skin` | Common | 3 | Attackers are infected with 3 stacks of poison. |  |
