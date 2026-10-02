# Escala — o que a tooltip não diz (RV-8b-2i)

> Gerado por `python tools/check_scaling.py`. Le as fórmulas de cada skill e cruza com as palavras do texto.


> Desde o PARSER-1 (01/10) a lista "já resolvido pelo mod" lê o parser ÚNICO (`tools/tabelas.py`). O regex antigo varria o arquivo inteiro e colhia 4 chaves FANTASMA de inicializadores fora dos blocos (302 no lugar de 298); DUAS casavam com o censo, ou seja a lista antiga tinha 2 casos FALSOS. A contagem caiu para o número real: é MAIS ESTRITO — ganho, não perda.


## Fontes de escala encontradas

| fonte | skills que usam | precisa estar no texto? |
|---|---:|---|
| Attack Power (dano de arma, cresce com Might) | 70 | — |
| Spell Power de Lightning | 16 | — |
| Spell Power de Cold | 16 | — |
| Spell Power de Fire | 12 | — |
| Spell Power de Shadow | 11 | — |
| NIVEL do personagem | 8 | — |
| Spell Power de Light | 5 | — |
| atributo MaxHealth | 5 | — |
| vida maxima | 5 | — |
| NIVEL do personagem (curva Flat Damage) | 5 | — |
| Spell Power de Physical | 3 | — |
| ultimo tipo de dano sofrido | 2 | — |
| atributo Armor | 2 | — |
| aliados em 1 hexes | 2 | — |
| Spell Power de Holy | 1 | — |
| invocacoes ativas | 1 | — |
| atributo EnchantColdValue | 1 | — |
| atributo Intelligence | 1 | — |
| seu MAIOR atributo | 1 | — |
| NIVEL do ALVO | 1 | — |
| Spell Power de Healing | 1 | — |
| atributo ActionPoints | 1 | — |
| atributo Health | 1 | — |
| atributo Might | 1 | — |

## O que FALTA no texto (é aqui que vale adicionar)

Nada: toda skill que escala cobrada pelo critério já diz com o que escala.


## Já resolvido pelo mod (o censo é o estado ANTES)


**NIVEL do ALVO** — `Perfected Soul` (Monk)


**NIVEL do personagem** — `Invulnerable Winter` (Cold), `Leech Dexterity` (Shadow), `Leech Intelligence` (Shadow), `Leech Might` (Shadow), `Living Armor` (Nature), `Perfected Soul` (Monk), `Shapeshift Dragonkin` (Nature), `Stasis` (Cold)


**NIVEL do personagem (curva Flat Damage)** — `Huntsman I` (Ranger), `Huntsman II` (Ranger), `Thorns I` (Nature), `Thorns II` (Nature), `Vengeful Shadows` (Shadow)

