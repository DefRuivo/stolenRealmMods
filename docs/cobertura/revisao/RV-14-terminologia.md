# RV-14 — Consistência de terminologia no jogo

Gerado por `tools/check_terminologia.py`. Para cada conceito, a **distribuição das
variantes** nos cinco corpora do censo. Onde há mais de uma em uso, a **maioria** é o
padrão a seguir (regra do projeto, a mesma que fechou o caso `Crippled` × `Slow`).

> Limite honesto: a lista de conceitos é **curada à mão** — não existe thesaurus do
> vocabulário do jogo. Conceito novo entra quando a revisão encontra.

| conceito | variante | total | skills | status | itens | afixos | powerups |

|---|---|---|---|---|---|---|---|
|  | `slow\w*` | 8 | 3 | 5 | 0 | 0 | 0 |
| lentidao (cripple x slow) | `crippl\w*` | 6 | 5 | 1 | 0 | 0 | 0 |
|  | `disabl\w*` | 21 | 10 | 10 | 1 | 0 | 0 |
| atordoamento (stun x rooted+disabled) | `stunn?\w*` | 17 | 11 | 5 | 1 | 0 | 0 |
|  | `root\w*` | 12 | 0 | 11 | 1 | 0 | 0 |
|  | `chill\w*` | 20 | 9 | 9 | 1 | 1 | 0 |
| congelamento (frozen x chilled) | `frozen` | 13 | 7 | 6 | 0 | 0 | 0 |
| vida maxima (max health x maximum health) | `max health` | 58 | 24 | 29 | 4 | 1 | 0 |
|  | `maximum health` | 24 | 12 | 12 | 0 | 0 | 0 |
| dano recebido (taken x received) | `damage taken` | 40 | 4 | 31 | 5 | 0 | 0 |
|  | `damage received` | 4 | 2 | 2 | 0 | 0 | 0 |
|  | `damage this target takes` | 1 | 1 | 0 | 0 | 0 | 0 |
| cura (healing x holy power) | `healing` | 117 | 43 | 43 | 7 | 14 | 10 |
|  | `holy power` | 13 | 2 | 5 | 1 | 5 | 0 |
|  | `holy` | 45 | 13 | 22 | 4 | 6 | 0 |
| resistencia sagrada (divine x holy) | `divine` | 6 | 3 | 0 | 0 | 3 | 0 |
|  | `movement` | 66 | 5 | 33 | 6 | 18 | 4 |
| pontos de movimento (movement points x movement) | `movement points?` | 40 | 2 | 15 | 5 | 18 | 0 |
|  | `stacks?` | 167 | 70 | 80 | 16 | 1 | 0 |
| empilhamento (per stack x stacks) | `per stack` | 48 | 5 | 43 | 0 | 0 | 0 |
|  | `for \d+ turns?` | 101 | 49 | 0 | 52 | 0 | 0 |
| duracao (lasts x for N turns) | `lasts` | 22 | 16 | 6 | 0 | 0 | 0 |
|  | `all resistances?` | 15 | 5 | 9 | 0 | 1 | 0 |
| escopo de atributos (all stats x all attributes) | `all stats` | 9 | 1 | 5 | 0 | 3 | 0 |
|  | `all attributes` | 1 | 1 | 0 | 0 | 0 | 0 |
| alcance (range x reach) | `range` | 46 | 22 | 18 | 0 | 2 | 4 |
|  | `reach` | 3 | 2 | 1 | 0 | 0 | 0 |
|  | `critical` | 41 | 21 | 14 | 0 | 6 | 0 |
| acerto critico (crit x critical) | `crit` | 4 | 0 | 1 | 0 | 3 | 0 |
| area (aura x area x within) | `aura` | 47 | 8 | 38 | 1 | 0 | 0 |
|  | `area` | 26 | 25 | 1 | 0 | 0 | 0 |
|  | `within the area` | 1 | 1 | 0 | 0 | 0 | 0 |

**Conceitos com mais de uma variante em uso: 14 de 14.** Cada linha desses é
candidata a padronização pela maioria — nunca por gosto.

## Como fechar um caso

1. Conte as variantes aqui (é o "a maioria escreve como?").
2. Confirme qual delas o **motor** usa de fato (nome do status/atributo no decompilado).
3. Se o motor e a maioria coincidem, alinhe os textos minoritários.
4. Se o motor contradiz a maioria (caso `Cripple` → status `Slow`), registre a contradição
   e NÃO mexa: foi a decisão tomada para o `Crippled` × `Slow`.


---

## VEREDITO POR CONCEITO (fechado 29/09)

Metodo de fechamento, na ordem que o projeto exige:

1. **Contar** as variantes no censo (`tools/check_terminologia.py`).
2. **Conferir no MOTOR** o que o jogo realmente usa (chaves do `resources.assets`).
3. Alinhar o texto minoritario **somente** quando a maioria e o motor concordam.
4. Motor contra a maioria = **NAO MEXER** e registrar o precedente.

| conceito | veredito | quem decidiu |
|---|---|---|
| `maximum health` / `max life` -> **`max health`** | APLICADO (13 + 5) | motor: Max Health 147 x Maximum Health 45 x Max Life 22 |
| `maximum mana` -> **`max mana`** | APLICADO (3) | motor: Max Mana 30 x Maximum Mana 22 |
| `damage received` -> **`damage taken`** | APLICADO (3) | censo: 40 x 4 |
| `Divine Resistance` -> **`Holy Resistance`** | APLICADO (3 afixos Angel/God/Saint) | completa o RV-13; campo interno continua Divino |
| `Crit` -> ~~`Critical`~~ | **RECUSADO** | motor: 27 `Crit Damage` + 6 `Crit Chance` contra ZERO `Critical ...` |
| `all attributes` -> `all stats` | ja tratado | o texto ja tinha entrada no mod |
| `Stunned.` (descricao circular) | ja tratado | o lote 1 de debuffs ja tinha posto nota |
| `disabled` x `rooted` x `stunned` | NAO SAO SINONIMOS | status distintos no censo |
| `chilled` x `frozen` | NAO SAO SINONIMOS | status distintos (motor: 82 x 53 chaves) |
| `healing` x `holy power` | NAO SAO SINONIMOS | Holy Power e o modificador da arvore Light |
| `movement` x `movement points` | **AMBOS OFICIAIS** | motor: Movement 170 x Movement Points 64 |
| `reach` x `range` | FALSO POSITIVO | as 3 ocorrencias sao NOMES e o VERBO, nao o substantivo |
| `aura` x `area` | NAO SAO SINONIMOS | Aura e um tipo de efeito, nao outro nome para area |
| `per stack` x `stacks` | sem variante real | um e o modificador, o outro o substantivo |
| `for N turns` x `lasts` | sem variante real | contextos diferentes, ambos corretos |

### As 4 licoes que ficam

1. **Variante de PALAVRA nao e conceito.** O instrumento conta palavras: nome proprio de skill/status
   (`Burning Reach`, `Mythic Reach`) e verbo ("when you reach 5 stacks") entram na conta e viram ruido.
   Antes de padronizar, ler as ocorrencias - nunca decidir pelo numero do relatorio.
2. **O motor tem a palavra final.** Contagem textual alta nao vale nada sozinha: o caso `Crit` tinha
   41 x 4 no censo e 0 x 27 no motor. E o 2o precedente depois de `Crippled` x `Slow`.
3. **Checar o motor inclui checar as CHAVES do `resources.assets`**, nao so o decompilado - foi la que
   apareceram as 147 chaves `Max Health` e o zero de `Critical`.
4. **`TextFixes` e `TextAppends` sao mutuamente exclusivos** (`if/else if` na mesma chave): um texto
   corrigido NUNCA recebe nota, e vice-versa. Antes de inserir em uma tabela, procurar a chave exata na
   OUTRA - foi assim que a guarda evitou chave dupla no `Stunned.` e no `Perfected Soul` (INC-1).

### Guarda nova no script

O `tools/check_terminologia.py` **pula toda linha de skill/status da arvore BARD** (31 linhas puladas na
1a rodada): a arvore Bard e intocavel por decisao de projeto ate a proxima atualizacao do jogo.

### Pendencia honesta

Os rotulos **`Holy` x `Divine`** so podem ser conferidos na **ficha de personagem** (fora do menu de
status): o motor tem 3 chaves `Divine Resistance` e ZERO `Holy Resistance`, mas a decisao do usuario
(RV-13) e padronizar em Holy. **Verificacao visual humana** em sessao de jogo.
