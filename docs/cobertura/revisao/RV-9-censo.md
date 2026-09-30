# RV-9 — Censo dos status (buffs e debuffs)

Gerado por `tools/censo_status.py`. **Alvo do pedido:** revisar todos os buffs e
debuffs e seus tooltips, **na mesma linha de formato das skills** (o processo completo
está descrito no RV-9 do `KANBAN.md`).

## Onde estamos

| grupo | entradas | pendentes |
|---|---|---|
| `Normal` | 457 | 457 |
| `Fortune` | 83 | 83 |
| `Quest` | 14 | 14 |
| `QuestItem` | 6 | 6 |

**Pendentes no grupo `Normal` (buffs/debuffs): 457 de 457.**

> O corte **buff x debuff** ainda não está no CSV: depende do `BenefitType` do status
> (em investigação por agente). Enquanto isso o agrupamento é pelo `tipo` do asset.
> Quando o campo for dumpado, este censo ganha a coluna e a fila é reordenada:
> **Harmful (debuffs) → Beneficial (buffs) → Quest/Fortune/resto**.

## Fila de trabalho — DEBUFFS PRIMEIRO (primeiros 60 pendentes)

| nome | tipo | raridade | efeitos | revise |
|---|---|---|---|---|
| `Aged` | Debuff | Common | MightBase:Percentage:-10, DexterityBase:Percentage:-10 | ⬜ |
| `Anthulk Venom` | Debuff | Common | DamageFlatPhysicalTarget:Base:ActionStatus.GetFlatDamageValue * .5f | ⬜ |
| `Anthulk Venom` | Debuff | Mythic | DamageFlatPhysicalTarget:Base:ActionStatus.GetFlatDamageValue * .5f | ⬜ |
| `Aura of Flame` | Debuff | Common |  | ⬜ |
| `Aura of Flame` | Debuff | Common | TargetStored['FireDamage'] = Source.SpellPower('Fire') * .4f | ⬜ |
| `Aura of Frost` | Debuff | Common | TargetStored['ColdDamage'] = Source.SpellPower('Cold') * .4f | ⬜ |
| `Aura of Lightning` | Debuff | Common |  | ⬜ |
| `Battered` | Debuff | Common | Armor:Percentage:-25, MagicArmor:Percentage:-25 | ⬜ |
| `Bleeding` | Debuff | Common | ResistPhysical:Base:-5, BleedingDamage:Base:Mathf.Max(1, Source.GetCus | ⬜ |
| `Blind` | Debuff | Common | Blind:Set:1 | ⬜ |
| `Blind` | Debuff | Common | Blind:Set:1 | ⬜ |
| `Blood Boil` | Debuff | Common | TargetStored['ShadowDamage'] = Source.SpellPower('Shadow') * .4f | ⬜ |
| `Blood Howl` | Debuff | Common | LifeOnHitTarget:Base:4 | ⬜ |
| `Brain Freeze` | Debuff | Common |  | ⬜ |
| `Brain Freeze` | Debuff | Common |  | ⬜ |
| `Bruised` | Debuff | Common | MaxHealth:Percentage:-10 | ⬜ |
| `Burning Ground` | Debuff | Common | TargetStored['FireDamage'] = Target.TeamIndex == 1 ? Target.FodderHeal | ⬜ |
| `Burning Ground` | Debuff | Common | TargetStored['FireDamage'] = Source.SpellPower('Fire') * .5f | ⬜ |
| `Chaos Curse` | Debuff | Common | TargetStored['ColdDamage'] = Source.GetRollResult(50) ? Source.SpellPo | ⬜ |
| `Chi Strike` | Debuff | Common | DamageMod:Base:-20 | ⬜ |
| `Chilled` | Debuff | Common | TurnFreeMovementPoints:Base:Target.CanBeEffectedByChilled ? (Target.Ch | ⬜ |
| `Confused` | Debuff | Common | IntelligenceBase:Percentage:-20 | ⬜ |
| `Consumption` | Debuff | Common | MaxHealth:Percentage:-20 | ⬜ |
| `Consumption` | Debuff | Common | MaxHealth:Percentage:10 | ⬜ |
| `Consumption` | Debuff | Common | MaxHealth:Percentage:-10 | ⬜ |
| `Contagion` | Debuff | Common | HealingReceivedBonus:Base:-1 | ⬜ |
| `Corrosive Bite` | Debuff | Common | ResistPhysical:Base:-10, ResistCold:Base:-10, ResistFire:Base:-10, Res | ⬜ |
| `Corrupted Consumables I` | Debuff | Common | ConsumableCooldown:Base:1 | ⬜ |
| `Corrupted Consumables II` | Debuff | Common | ConsumableCooldown:Base:2 | ⬜ |
| `Corrupted Consumables III` | Debuff | Common | ConsumableCooldown:Base:3 | ⬜ |
| `Crippled` | Debuff | Common | TurnFreeMovementPoints:Base:-1 | ⬜ |
| `Crystal Bite` | Debuff | Common | DamageReduction:Base:-10, TurnFreeMovementPoints:Base:-1 | ⬜ |
| `Curse` | Debuff | Common | ResistPhysical:Base:-20, ResistCold:Base:-20, ResistFire:Base:-20, Res | ⬜ |
| `Curse of Death` | Debuff | Common |  | ⬜ |
| `Curse of Elements` | Debuff | Common | ResistCold:Base:-25, ResistFire:Base:-25, ResistLightning:Base:-25 | ⬜ |
| `Curse of Frailty` | Debuff | Common | ResistPhysical:Base:-25 | ⬜ |
| `Curse of Ruin` | Debuff | Common | MightBase:Percentage:-15, DexterityBase:Percentage:-15, IntelligenceBa | ⬜ |
| `Curse of Sorrow` | Debuff | Common | HealingReceivedBonus:Base:-50 | ⬜ |
| `Curse of Weakness` | Debuff | Common | DamageMod:Base:-25 | ⬜ |
| `Cursed` | Debuff | Common |  | ⬜ |
| `Cursed` | Debuff | Common | MightBase:Percentage:-10, DexterityBase:Percentage:-10, IntelligenceBa | ⬜ |
| `Cursed Bite` | Debuff | Common | HealingReceivedBonus:Base:-50 | ⬜ |
| `Damage` | Debuff | Common | TargetStored['FireDamage'] = Source.SpellPower('Fire') * 0.3f; TargetS | ⬜ |
| `Damage Reduced by 20%` | Debuff | Common | DamageMod:Base:-20 | ⬜ |
| `Damage Reduced by 5%` | Debuff | Common | DamageMod:Base:-5 | ⬜ |
| `Damage Reduced by 50%` | Debuff | Common | DamageMod:Base:-50 | ⬜ |
| `Death` | Debuff | Common | Target.Kill() | ⬜ |
| `Decaying` | Debuff | Common | MaxHealth:Percentage:-25 | ⬜ |
| `Dire Bite` | Debuff | Common | HealingReceivedBonus:Base:-100 | ⬜ |
| `Dire Howl` | Debuff | Common | LifeOnHitTarget:Base:6 | ⬜ |
| `Disabled` | Debuff | Common | Disabled:Set:1 | ⬜ |
| `Disappointment` | Debuff | Common | DamageMod:Base:-20 | ⬜ |
| `Diseased` | Debuff | Common | MaxHealth:Percentage:-15 | ⬜ |
| `Dispelling Fracture` | Debuff | Common | ResistPhysical:Base:-20, ResistCold:Base:-20, ResistFire:Base:-20, Res | ⬜ |
| `Dreadful Dissonance` | Debuff | Common | Feared:Set:1, Disabled:Set:1 | ⬜ |
| `Enfeebled` | Debuff | Common | DamageMod:Base:-20 | ⬜ |
| `Exhaustion` | Debuff | Common | RecentlyHasted:Set:1 | ⬜ |
| `Faerie Swarm` | Debuff | Common | TargetStored['PhysicalDamage'] = Source.SpellPower('Physical') * .4f | ⬜ |
| `Fatigued` | Debuff | Common | DexterityBase:Percentage:-20 | ⬜ |
| `Focused Strike` | Debuff | Common | DamageReduction:Base:-20 | ⬜ |

## Como o veredito entra

Os mesmos quatro estados das skills, na coluna `revisao` do `status.csv`:
- `revisado` — conferido no asset/código, texto de pé;
- `corrigido` — o texto mudou (entra no `TextFixes`);
- `sem-explicacao` — omissão **por design** (ex.: os sorteios do Chaos);
- `intocavel` — não se mexe (ex.: árvore Bard).

Status **não** estão no dicionário de localização: são campos brutos do asset, então a
correção é em **runtime (Harmony)**, não em tabela de texto.
