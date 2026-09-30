# RV-8b — lote **Shadow** (41 skills) · revisado em 29/09

> Primeiro lote da revisão de conteúdo das skills. Método: ler a descrição **exata** do
> asset (do `skills.csv`), comparar com as tags/tier/dano do próprio asset e corrigir
> só o que é objetivamente defeito de texto. **Nenhuma afirmação de mecânica foi
> alterada** — mecânica exige verificação no código + triangulação externa.

## 1. Corrigido (4) — `status = corrigido` no `skills.csv`

Gramática e espaçamento. Nenhum muda o sentido, então não precisaram de triangulação.

| Skill | Antes | Depois |
|---|---|---|
| `Poison Cloud` | "creates **an** poison gas cloud **applies**" | "creates **a** poison gas cloud **that applies**" |
| `Raise Undead Wizard` | "Raise **a** Undead Wizard" | "Raise **an** Undead Wizard" |
| `Ghost Armor` | "attack.**··**Lasts until hit.**·**" (espaço duplo + espaço no fim) | "attack. Lasts until hit." |
| `Soul Crush` | "…Max Health.**·**" (espaço no fim) | "…Max Health." |

As chaves foram conferidas por `python tools/check_fix_keys.py`: **53 das 55** chaves das
tabelas do mod existem no censo; as 2 de fora são dicas de loading (uma delas já
confirmada disparando no log). As 4 novas estão entre as que casam.

## 2. Padronizado pela MAIORIA (5) — `status = corrigido`

Regra do projeto (29/09): quando skills irmãs divergem na redação, vale o **padrão da
maioria** — e a maioria costuma estar no próprio **nome** da skill. Levantado por
`tools/audit_tooltips.py`, checagem **E2** (famílias pelo nome):

| Skill | Antes | Depois |
|---|---|---|
| `Raise Skeletal Archer` | "**Summon** a skeletal archer…" | "**Raise** a skeletal archer…" |
| `Raise Skeletal Mage` | "**Summon** a skeletal mage…" | "**Raise** a skeletal mage…" |
| `Raise Skeletal Warrior` | "**Summon** a skeletal warrior…" | "**Raise** a skeletal warrior…" |
| `Raise Iron Golem` | "…to fight **for you**." | "…to fight **by your side**." |
| `Shapeshift Dragonkin` | "**Gain the ability to shapeshift into** a powerful elemental…" | "**Shapeshift into** a powerful elemental…" |

Contagem que fundamenta a decisão: no `Raise *`, **4** descrições com "Raise" contra **3**
com "Summon" — e **os 6 nomes começam com "Raise"**. No fecho, 6 usam "by your side" contra
1 "for you". No `Shapeshift *`, 3 contra 1.

> Nota: somando **todo o jogo**, "Summon" ganha (9 contra 4) — as 6 skills de invocação da
> Nature usam "Summons a X to fight for you". Apliquei a maioria **dentro da família/tema**
> porque é ela que o jogador vê lado a lado, e porque o nome da skill ("Raise …") é o sinal
> mais forte. Se preferir o padrão global, é uma linha por skill.

## 2b. Não devem ser explicadas — `status = sem-explicacao` (3)

Por escolha de design, estas ficam como estão: **saíram da auditoria** (não são pendência).

| Skill | Árvore | Texto |
|---|---|---|
| `Coin of Chaos` | Shadow | "Flip the Coin of Chaos!" |
| `Harm` | Chaos | "Damaging an Enemy has a 10% chance to apply Hurting." |
| `Aid` | Chaos | "Healing an ally has a 10% chance to apply Helping." |

## 3. Inconsistência de DADOS encontrada (não dá pra corrigir num mod de texto)

`Raise Skeletal Archer` e `Raise Undead Ranger` **não têm a tag `Beneficial`**, enquanto
os outros quatro invocadores têm (`Beneficial,Ranged`). A tag vem do asset e afeta como
o tooltip é montado/colorido — um mod de texto não alcança isso. **Confirmar no jogo** se
a diferença aparece; se aparecer, é caso pra (a) reportar ao dev ou (b) um mod próprio.

## 4. O que falta para fechar o RV-8b

Duas coisas, nesta ordem:

1. **Enriquecer o dump de skills.** O censo de hoje traz nome, tipo, tier, dano, tags e
   descrição — mas **não** as `DescriptionExpressions`, `ActionsGranted` e
   `AttributeEffects`. Sem elas não dá pra conferir se os **números** do texto batem com
   o que o código calcula (que é o coração da revisão de conteúdo).
2. **Triangular os 37 restantes** com ≥2 fontes externas (wiki, patch notes mais recentes,
   guias Steam, Discord) e marcar `revisado` no `skills.csv`. Os 37 seguem `pendente`
   de propósito — foram lidos, mas ler não é revisar.

## 5. Auditoria de conteúdo — o "está bem explicado?"

`tools/audit_tooltips.py` roda 5 checagens sobre **todas** as 420 skills revisáveis (Bard e
flavor fora). Primeira passada completa:

| checagem | achados | leitura |
|---|---:|---|
| A · causa dano e não diz o **tipo** de dano | **0** | todo skill de dano declara o tipo |
| B · causa dano e não tem **valor dinâmico** | **0** | todo skill de dano usa `*N`/`[N]` |
| C · efeito em **área** sem menção de área | **0** | — |
| D · descrição curta/vazia | **1** | sobrou só `Light's Strength` (curta, mas mecânica) |
| E2 · famílias por **nome** divergentes | **2** | `Raise *` e `Shapeshift *` → corrigidas na seção 2 |
| E · famílias por **fecho** (candidatas) | **35** | lista frouxa: quase tudo são templates diferentes que só terminam parecido |

A leitura disso é o achado mais importante do lote: **o problema das tooltips não é falta de
informação mecânica** — tipo de dano, valor dinâmico e área estão sempre declarados. O
problema é **consistência de redação entre skills irmãs**. É exatamente onde a regra do
padrão da maioria morde, e é ali que os próximos lotes devem gastar energia.

A checagem E2 só é precisa depois de um filtro: agrupar pelo nome junta skills que só
compartilham um substantivo (`Aura *`, `Fire *`, `Ice *`). O filtro exige que a palavra do
nome seja um **verbo que alguma descrição ecoa** — aí sobram as famílias de verdade.
