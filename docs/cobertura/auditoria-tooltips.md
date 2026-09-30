# Auditoria de conteudo das tooltips de skill (RV-8b)

> `python tools/audit_tooltips.py nature` — 39 skills, Bard e demais intocaveis fora.


| checagem | achados |
|---|---:|
| A · causa dano e não diz o **tipo** de dano | 0 |
| B · causa dano e não tem **valor dinâmico** | 0 |
| C · efeito em **área** sem menção de área no texto | 0 |
| D · descrição **curta/vazia** (candidata a flavor) | 0 |
| E2 · famílias por **nome** com abertura divergente (precisa) | 1 |
| E · famílias por **fecho** com abertura divergente (candidatas) | 2 |
| G · placeholder `[N]` apontando para **expressão inexistente** | 0 |
| H · `*N` (dano) fora do alcance da fórmula | 0 |
| H · `*N` **não verificável** (dano vem de status — escopo aberto) | 0 |

> Nem todo achado é defeito: D costuma ser skill que **não deve ser explicada**
> (flavor) e H-não-verificável é lacuna do CENSO, não do jogo. A auditoria
> levanta, a revisão decide.


## A · Sem tipo de dano (0)

Nenhum.


## B · Sem valor dinâmico (0)

Nenhum.


## C · Area sem texto de area (0)

Nenhum.


## D · Descricao curta/vazia (0)

Nenhum.


## G · Placeholder [N] fora do alcance das expressões (0)

Nenhum.


## H · Placeholder *N fora do alcance da fórmula de dano (0)

Nenhum.


## H · *N não verificável (dano vem de status) (0)

Nenhum.


## E2 · Famílias por NOME com abertura divergente (1)

Skills que compartilham a primeira palavra do nome deveriam abrir a descrição do mesmo jeito. **É aqui que vale a regra do padrão da maioria** — e a maioria costuma estar no próprio nome:


**Shapeshift \*** — aberturas: {'shapeshift': 2, 'gain': 1}

| skill | arvore | descricao |
|---|---|---|
| Shapeshift Dire Werewolf | Nature | Shapeshift into a @Dire Werewolf@. Basic attack and abilities are further empowered. Increases @Max Health@ by |
| Shapeshift Dragonkin | Nature | Gain the ability to shapeshift into a powerful elemental @Dragonkin@. Empowers basic attack, grants new abilit |
| Shapeshift Werewolf | Nature | Shapeshift into a @Werewolf@. Empowers your basic attack and gain new abilities. Increases @Max Health@ by 10% |

## E · Famílias por FECHO divergentes — candidatas (2)

Mesmo fecho de frase, abertura diferente. Lista frouxa de propósito: quase tudo aqui são templates diferentes que por acaso terminam igual.


**…lasts turns** — aberturas: {'summon': 1, 'calls': 1, 'causes': 1}

| skill | arvore | descricao |
|---|---|---|
| Brambles | Nature | Summon brambles to block 4 hexes. Attackers will take physical damage when striking the brambles. Lasts 4 turn |
| Rainstorm | Nature | Calls down a magical rain that increases potency of Mana using abilities by 50% for allies within the area. La |
| Venomous Skin | Nature | Causes the skin of a target ally to secrete poison. Attacking enemies receive 3 stacks of {STA=Poisoned}. Last |

**…increases by** — aberturas: {'shapeshift': 2, 'gain': 1}

| skill | arvore | descricao |
|---|---|---|
| Shapeshift Dire Werewolf | Nature | Shapeshift into a @Dire Werewolf@. Basic attack and abilities are further empowered. Increases @Max Health@ by |
| Shapeshift Dragonkin | Nature | Gain the ability to shapeshift into a powerful elemental @Dragonkin@. Empowers basic attack, grants new abilit |
| Shapeshift Werewolf | Nature | Shapeshift into a @Werewolf@. Empowers your basic attack and gain new abilities. Increases @Max Health@ by 10% |
