# RV-9 — Triagem dos números (grupo `Normal`, beneficio=Debuff)

Gerado por `tools/check_status_numeros.py`. **Isto é triagem, não veredito**: o script
não julga se o texto está certo — separa quem cita um número que **não existe em efeito
nenhum** do asset, que é onde o defeito ou a omissão costuma estar.

## Números

| o que | quantos |
|---|---|
| status no grupo | 133 |
| todo número da descrição tem par nos efeitos | 114 |
| com número sem par — conferir | **13** |

> Falsos positivos esperados: **duração** ("for 2 turns") não mora nos efeitos — mora no
> campo de duração; percentuais podem vir de `StatusPower`. Conferir sempre o texto
> COMPLETO antes de decidir (lição do RV-8c: uma nota redundante no `Meteor`).

## Fila de triagem

| status | tipo | número sem par | descrição | efeitos |
|---|---|---|---|---|
| `Anthulk Venom` | Common | 10 | The target takes [0] increased flat physical damage. Stacks up to 10 times. | DamageFlatPhysicalTarget:Base:ActionStatus.GetFlatDamageVa |
| `Brain Freeze` | Common | 8 | Deals 8% of the targets Max Health in cold damage each time the target perform |  |
| `Chaos Curse` | Common | 50 | Cursed to take damage. Each element has a @50%@ chance to deal *0 damage every | TargetStored['ColdDamage'] = Source.GetRollResult(50) ? So |
| `Chilled` | Common | 2 | Movement points reduced by one per stack.  Lasts 2 turns.  Five stacks of Chil | TurnFreeMovementPoints:Base:Target.CanBeEffectedByChilled  |
| `Crystal Bite` | Common | 5 | Target takes *0 shadow damage each turn, increases damage taken by 10% and red | DamageReduction:Base:-10, TurnFreeMovementPoints:Base:-1 |
| `Disappointment` | Common | 2,4 | The disappointment of <color=#EE4B2B><b>Shawn</b></color> follows your every m | DamageMod:Base:-20 |
| `Faerie Swarm` | Common | 1 | Target takes *0 physical damage and 1 stack of {STA=Bleeding} per turn. | TargetStored['PhysicalDamage'] = Source.SpellPower('Physic |
| `Haunt` | Common | 8 | Deals *0 damage. Lifesteals for 8%. | TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') |
| `Heat` | Common | 10 | Elemental resistance reduced by 5% per stack.  Lasts [0] turns.  Can stack up  | ResistCold:Base:-5, ResistFire:Base:-5, ResistLightning:Ba |
| `Petrification` | Common | 5 | Each stack lowers @movement@ by 1 and increases @Damage Taken@ by 20%. When yo | TurnFreeMovementPoints:Base:-1, DamageReduction:Base:-20 |
| `Shocked` | Common | 3 | Incoming critical strike damage increased by 10% per stack.  Lasts 3 turns.  C | CritDamageTarget:Base:10 |
| `Spore Cloud` | Common | 5 | Decreases damage dealt by 10% and movement by 1. Stacks up to 5 times. | DamageMod:Base:-10, TurnFreeMovementPoints:Base:-1 |
| `The Bad Bloom` | Common | 2 | Enemies gain 2 stacks of poison. |  |
