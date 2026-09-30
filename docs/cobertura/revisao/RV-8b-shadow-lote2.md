# RV-8b — lote 2 da Shadow (os 12 itens "conferir")

> Fechamento dos itens que a bancada marcou como "sem par no código dumpado".
> Bancada nova para achar os números: **`tools/analisa_conferir.py <arvore>`** — lê a
> ficha e imprime, por skill, o `attr`, as expressões, as ações (com efeitos e ação
> referenciada), os gatilhos e os status aplicados. O número que faltava quase sempre
> está num desses lugares que o `verify_tree` não olha.

## Fechados (9) — com a prova

| skill | o texto afirma | onde o código confirma |
|---|---|---|
| `Call of the Grave` | 20% contra inimigos abaixo de 50% de vida | `source["CallOfTheGrave"] > 0f && target.HealthRatio <= 0.5f ? 20 : 0` |
| `Tainted Touch` | Life Steal 12% | `SourceStored['HealingForced'] = Source['MaxHealth'] * .12f` |
| `Dark Pact` | +30% dano/cura, −20% vida | `DamageMod:Base:30, MaxHealth:Percentage:-20` |
| `Mana Drain` | 20% da mana do alvo / 20% da sua | `Target.MaxMana * .2f` + `Source.MaxMana * -.2f` |
| `Hunger` | 10% mana steal, 10% vida por turno | status `Hunger`: `ManaOnHit:Base:10` + `Target.MaxHealth * .1f` |
| `Endless Night` | 2% da vida como dano sombrio extra | `DamageFlatShadow:Base:Source["MaxHealth"] * .02f` |
| `Soul Exchange` | lifesteal 100%, dano pela vida faltante | `HealingForced = Source['MaxHealth']` + `((MaxHealth − Health) * .35f) + SpellPower('Shadow')` |
| `Reaper's Toll` | 10% da vida quando um inimigo morre | **teste do próprio jogo**: `Assert(caster.Health − hp <= max * 0.1f + 1.5f)` |
| `Consumption` | 10% de vida máxima por inimigo | **teste do próprio jogo**: `AssertPercentIncrease("MaxHealth", max, …, 10 * Stacks)` → "granted N x 10% max health" |

**O teste do próprio jogo é fonte de primeira quando existe.** Foi ele que decidiu dois
casos que o asset não resolve: `Reaper's Toll` (não tem `attr`, nem ação, nem gatilho — a
mecânica é do código) e `Consumption` (o +10% no caster vem de um status separado,
`SHD_Status_Consumption_S`, que o dump de skills não liga à skill).

## Abertos (3) — com o motivo

### `Haunt` — três números diferentes na mesma mecânica
- o texto da skill diz **6%**;
- o texto do status `Haunt` diz "Lifesteals for **8%**";
- o código faz `Source['MaxHealth'] * .025f` = **2,5%**.

O código é o que acontece, então o 6% do texto está errado — mas o **texto do status
também** está (8% contra 2,5%). É inconsistência de **dados** do jogo, não só de redação:
corrigir a tooltip esconderia metade do problema.

### `Vampiric Aura` — o texto diz 5%, o status concede 50
O status `Vampiric Aura` tem `LifeSteal:Base:50`, e a unidade é **porcento**: o status
`Vampire Lord Aura`, com o **mesmo 50**, diz na própria descrição "Life steal increased by
50%" (e `Blood Frenzy`, com 25, diz 25%). Seriam **10×** de diferença.
**Ressalva que impede o conserto automático:** o atributo genérico `LifeSteal` não é o que
move o lifesteal no build atual (os valores reais vivem em `LifeSteal`+`SkillType`, achado
já verificado) — então não dá para afirmar que 5% é o efeito real e 50 o nominal.

### `Poison Cloud` — "within 2 hexes" não está em campo público da ação
O `[ActionProps]` traz `range=8` (alcance do cast) e `blast` vazio. A área de 2 hexes mora
no asset de **terreno/efeito de chão**, que o dump não visita — a mesma limitação de
`Consumption` (que fechou no 10%, mas cujo "within 2 hexes" também não é verificável),
`Volley` e `Rainstorm`. O que **está** confirmado: as **4 stacks de `Poisoned`** — a ação
aplica `Poisoned` quatro vezes.

## Números

Censo depois do lote: **265 pendente · 88 corrigido · 58 revisado · 31 intocavel ·
9 sem-explicacao**.

## Reconferir

```bash
python tools/verify_tree.py shadow        # regera a ficha
python tools/analisa_conferir.py shadow   # imprime o código por trás de cada item
```
