# RV-8b-2e — fechamento dos abertos da Nature

> 9 skills da Nature estavam **abertas** na ficha: o texto afirmava porcentagem ou
> alcance em hex, e isso não vive em `AttributeEffects` — então o dump da época não
> tinha onde conferir. Com o `RV-8b-0f` (`[ActionProps]` + `[Trigger]`), **6 fecharam**
> e 3 continuam abertas por limite do dump, com o motivo escrito.

## Como cada uma fechou

| skill | o que o texto afirma | o que o código diz | status |
|---|---|---|---|
| `Brambles` | "block **4 hexes**" | a ação tem **4 entradas de alvo**, cada uma excluindo as anteriores (`Cell != TargetedCells[0..2] && Cell.IsEmpty`) → 4 hexes | `revisado` |
| `Pack Hunter I` (T1) | "for every ally **within 1 hex** … **8%**" | `DamageMod:Base:8 * Source.NumAlliesWithin(1)` — as duas coisas na mesma expressão | `revisado` |
| `Bristles` | "summons gain **50%** of your return damage" | `SummonMaster["Bristles"] > 0 ? SummonMaster["DamageReturnedFlatCold"] * .5f : 0f` (idem Fire e Lightning) | `revisado` |
| `Circle of Life` | "**50%** chance" | `cond=Source.IsEnemy(Target) && Source.GetRollResult(50)` | `revisado` |
| `Natural Selection` | "gain **5%** of your max Health and Mana" | `Natural Succession Proc`: `SourceStored['Healing'] = Source.MaxHealth * .05f; SourceStored['ManaDamage'] = Source.MaxMana * -.05f` | `revisado` |
| `Evolution` | "**5%** stacking **10x**" | status `Evolution`: `DamageMod:Base:5` e `MaxHealth:Percentage:5`, descrição "Can stack up to 10 times" | `revisado` |

As duas gatilho do `Evolution` (`OnHittingDamaging` e `OnGettingHitDamaging`) batem com
os dois casos do texto ("Getting hit" / "Hitting"), e o `Natural Selection` usa
`AfterAnyCharacterDeath` + `Source != Target`, que é literalmente "an Ally or an Enemy".

## O que continua aberto, e por quê

| skill | afirma | onde o valor deve estar |
|---|---|---|
| `Shapeshift Werewolf` | "Max Health by **10%**" | no **asset do personagem shapeshiftado** — o status `Shapeshift: Werewolf` vem com `efeitos` vazio e o assembly não tem o número |
| `Shapeshift Dire Werewolf` | "Max Health by **20%**" | idem |
| `Rainstorm` | "potency … by **50%** … within the area. Lasts **2 turns**" | a ação não aplica status: é **terreno/aura**. `Rainstorm` não existe no assembly |

Fechar essas três pede um habilitador novo (despejar o `CharacterInfo` do shapeshift e o
objeto de terreno). Não é bug do jogo — é limite do que eu leio hoje. As três ficam
**abertas**, não "corrigidas sem prova".

## Buraco de dump que este lote revelou

A ação concedida por um **gatilho** não está em `ActionsGranted`, então nunca entrava no
inventário de ações: `Natural Succession Proc` **não existe no assembly** (é asset) e
estava invisível — justamente onde mora o 5% que a tooltip promete. O dump agora registra
as ações dos gatilhos e o `[Trigger]` passou a trazer `status` e `chancesStatus`.

## Reconferir

```bash
bash scratch/test-cycle.sh 30 "Debugger"
python scratch/analisa_nature.py     # imprime texto, gatilhos e ação de cada uma das 9
```
