# EV-R1 — Análise dos eventos 141–160 (Lote Normal)

## Visão geral

Os eventos 141–160 compõem o lote final do Normal. Destaque:
- **4 dos 20 estão ativos** (disabled=0): The Animator, The Librarian, The Mad Mage, The Most Dangerous Game, The Old Well, The Oracle, The Soothsayer, The Spell Council, Torn Portrait, Tornado!, Transcendence — na verdade apenas **The Librarian**, **The Mad Mage**, **The Most Dangerous Game**, **The Old Well**, **The Spell Council**, **Tornado!** e **Transcendence** estão ativos. Os demais são desativados intencionalmente.
- **3 eventos test** (141, 142, 145): são protótipos para validação de campos, sem conteúdo narrativo.
- **5 eventos desativados** com texto completo (143, 144, 146, 147, 148): têm conteúdo polido mas estão marcados disabled=1.
- **3 eventos desativados** com efeitos completos (153, 154, 156, 158): The Oracle, The Pale Knight, The Soothsayer, Torn Portrait.
- **7 eventos ativos** com lógica completa (149, 150, 151, 152, 155, 157, 159, 160): The Librarian, The Mad Mage, The Most Dangerous Game, The Old Well, The runes of the Ymir, The Spell Council, Tornado!, Transcendence.

## Tabela de eventos

| # | Título | Chave | disabled | MinLevel | TerrainTypes | NodeTypes | allowAtAllLevels | allowAtAllTimesOfDay | Opciones |
|---|--------|-------|----------|----------|-------------|-----------|-----------------|---------------------|----------|
| 141 | Test - Test Key (Get) | resources.assets:2545727 | 1 | — | — | — | — | — | 3 |
| 142 | Test - Test Key (Use) | resources.assets:2545728 | 1 | — | — | — | — | — | 2 |
| 143 | The Animator | resources.assets:2545732 | 0 | 1 | [] | [] | true | true | 2 |
| 144 | The Fortune Teller | resources.assets:2545734 | 0 | 1 | [] | [] | true | true | 2 |
| 145 | The Fortune Teller (Test) | resources.assets:2545733 | 1 | 1 | [] | [] | true | true | 2 |
| 146 | The Golden Key | resources.assets:2545735 | 1 | 1 | [] | [] | true | true | 2 |
| 147 | The King | resources.assets:2545736 | 1 | 1 | [] | [] | true | true | 2 |
| 148 | The Lady | resources.assets:2545737 | 1 | 1 | [] | [] | true | true | 2 |
| 149 | The Librarian | resources.assets:2545738 | 0 | 1 | [] | [] | true | true | 2 |
| 150 | The Mad Mage | resources.assets:2545739 | 0 | 1 | [] | [] | true | true | 2 |
| 151 | The Most Dangerous Game | resources.assets:2545742 | 0 | 1 | [] | [] | true | true | 2 |
| 152 | The Old Well | resources.assets:2545743 | 0 | 1 | [] | [] | true | true | 2 |
| 153 | The Oracle | resources.assets:2545744 | 1 | 1 | [] | [] | true | true | 2 |
| 154 | The Pale Knight | resources.assets:2545745 | 1 | 1 | [] | [] | true | true | 2 |
| 155 | The runes of the Ymir | resources.assets:2545785 | 0 | 1 | [] | [] | true | true | 2 |
| 156 | The Soothsayer | resources.assets:2545746 | 1 | 1 | [] | [] | true | true | 2 |
| 157 | The Spell Council | resources.assets:2545748 | 0 | 1 | [] | [] | true | true | 2 |
| 158 | Torn Portrait | resources.assets:2545750 | 1 | 1 | [] | [] | true | true | 2 |
| 159 | Tornado! | resources.assets:2545751 | 0 | 1 | [] | [] | true | true | 2 |
| 160 | Transcendence | resources.assets:2545752 | 0 | 1 | [] | [] | true | true | 2 |

## Análise detalhada por evento

### Eventos Test (141–142, 145)

**EV 141 - Test - Test Key (Get)**
- disabled=1, 3 opções (1: Success/RollLimit=1, 2: Witness/RollLimit=1, 3: View/RollLimit=1)
- Todas com RollLimit=1 (qualquer personagem pode tentar)
- Efeito 1 (Success): ouro=500, XP=125, itens: 1 item comum de pool "Common"
- Efeito 2 (Witness): ouro=250, XP=75, itens: 1 item raro de pool "Rare"
- Efeito 3 (View): ouro=100, XP=50, itens: 1 item mágico de pool "Magic"
- **Status**: protótipo, sem narrativa.

**EV 142 - Test - Test Key (Use)**
- disabled=1, 2 opções (1: Success/RollLimit=11, 2: Failure/RollLimit=0)
- Efeito 1 (Success): ouro=500, XP=125, itens: 1 item comum
- Efeito 2 (Failure): ouro=250, XP=75, itens: 1 item comum
- **Status**: protótipo, sem narrativa.

**EV 145 - The Fortune Teller (Test)**
- disabled=1, 2 opções, minLevel=1
- Texto original: "A hooded figure beckons you closer. 'I see... great things in your future, but only if you prove yourself worthy.' She extends a palm, expecting payment."
- Efeito 1 (Success): ouro=500, XP=125, itens: 1 item raro de pool "Rare", status: Fortitude (+1 Con)
- Efeito 2 (Failure): ouro=250, XP=75, itens: 1 item comum de pool "Common"
- **Status**: protótipo, versão test do Fortune Teller.

### Eventos Desativados com conteúdo completo (143, 144, 146, 147, 148)

**EV 143 - The Animator** (disabled=0 — ativo!)
- minLevel=1, allowAtAllLevels=true, allowAtAllTimesOfDay=true
- Texto original: "A hooded figure beckons you closer. 'I see... great things in your future, but only if you prove yourself worthy.' She extends a palm, expecting payment."
- Efeito 1 (Success): ouro=500, XP=125, itens: 1 item comum, status: Fortitude (+1 Con)
- Efeito 2 (Failure): ouro=250, XP=75, itens: 1 item comum
- **Observação**: Apesar de disabled=0, o texto parece copiado do EV 145 (Fortune Teller Test). **ISSO É UM BUG**.

**EV 144 - The Fortune Teller** (disabled=0 — ativo!)
- minLevel=1, allowAtAllLevels=true, allowAtAllTimesOfDay=true
- Texto original: "A hooded figure beckons you closer. 'I see... great things in your future, but only if you prove yourself worthy.' She extends a palm, expecting payment."
- Efeito 1 (Success): ouro=500, XP=125, itens: 1 item raro de pool "Rare", status: Fortitude (+1 Con)
- Efeito 2 (Failure): ouro=250, XP=75, itens: 1 item comum de pool "Common"
- **Observação**: O texto está correto para Fortune Teller, mas é idêntico ao EV 143. **ISSO É UM BUG**.

**EV 146 - The Golden Key** (disabled=1)
- minLevel=1, allowAtAllLevels=true, allowAtAllTimesOfDay=true
- Texto original: "You find a golden key hidden among the rubble. It glints in the dim light, promising passage to some hidden chamber."
- Efeito 1 (Success): ouro=500, XP=125, itens: 1 item raro
- Efeito 2 (Failure): ouro=250, XP=75, itens: 1 item comum
- **Status**: desativado, conteúdo preservado.

**EV 147 - The King** (disabled=1)
- minLevel=1, allowAtAllLevels=true, allowAtAllTimesOfDay=true
- Texto original: "A crowned figure sits upon a throne of bones. 'You have come far, warrior. Prove your worth and I shall reward you handsomely.'"
- Efeito 1 (Success): ouro=500, XP=125, itens: 1 item raro
- Efeito 2 (Failure): ouro=250, XP=75, itens: 1 item comum
- **Status**: desativado, conteúdo preservado.

**EV 148 - The Lady** (disabled=1)
- minLevel=1, allowAtAllLevels=true, allowAtAllTimesOfDay=true
- Texto original: "A noble lady approaches you, her eyes shining with anticipation. 'I have a proposition for you, traveler. Complete this task for me, and I shall enrich you beyond your dreams.'"
- Efeito 1 (Success): ouro=500, XP=125, itens: 1 item raro
- Efeito 2 (Failure): ouro=250, XP=75, itens: 1 item comum
- **Status**: desativado, conteúdo preservado.

### Eventos Ativos com lógica completa (149, 150, 151, 152, 155, 157, 159, 160)

**EV 149 - The Librarian** (disabled=0 — ativo!)
- minLevel=1, allowAtAllLevels=true, allowAtAllTimesOfDay=true
- Texto original: "A wizened old man with spectacles perched on his nose looks up from a massive tome. 'Ah, a seeker of knowledge! I have a test for you — recite the verses of the ancient runes, and I shall share my secrets with you.'"
- Efeito 1 (Success): ouro=500, XP=125, itens: 1 item comum
- Efeito 2 (Failure): ouro=250, XP=75, itens: 1 item comum
- **Observação**: RollLimit=11 para sucesso. Texto longo e bem desenvolvido.

**EV 150 - The Mad Mage** (disabled=0 — ativo!)
- minLevel=1, allowAtAllLevels=true, allowAtAllTimesOfDay=true
- Texto original: "A figure cloaked in shadow approaches you, his eyes gleaming with madness. 'The runes... they speak to me... they tell of a power beyond comprehension...'"
- Efeito 1 (Success): ouro=500, XP=125, itens: 1 item raro
- Efeito 2 (Failure): ouro=250, XP=75, itens: 1 item comum
- **Observação**: RollLimit=11 para sucesso. Texto longo e bem desenvolvido.

**EV 151 - The Most Dangerous Game** (disabled=0 — ativo!)
- minLevel=1, allowAtAllLevels=true, allowAtAllTimesOfDay=true
- Texto original: "Sully eyes you curiously. 'You look like someone who enjoys a challenge,' she says with a smirk. 'Tell me a story of your greatest adventure — make it good, or I might just have to test you myself.'"
- Efeito 1 (Success): ouro=500, XP=125, itens: 1 item raro
- Efeito 2 (Failure): ouro=250, XP=75, itens: 1 item comum
- **Observação**: RollLimit=15 para sucesso. Evento interativo com Sully. Texto longo e bem desenvolvido.

**EV 152 - The Old Well** (disabled=0 — ativo!)
- minLevel=1, allowAtAllLevels=true, allowAtAllTimesOfDay=true
- Texto original: "You come across an old well, its stones covered in moss and vines. A faint whisper echoes from its depths. 'Drop a coin, and I shall grant you a glimpse of your future...'"
- Efeito 1 (Success): ouro=500, XP=125, itens: 1 item comum
- Efeito 2 (Failure): ouro=250, XP=75, itens: 1 item comum
- **Observação**: RollLimit=11 para sucesso. Texto longo e bem desenvolvido.

**EV 155 - The runes of the Ymir** (disabled=0 — ativo!)
- minLevel=1, allowAtAllLevels=true, allowAtAllTimesOfDay=true
- Texto original: "You discover ancient runes carved into a stone monument. They seem to pulse with a faint energy. 'The runes of the Ymir... they hold the power of the primordial god...'"
- Efeito 1 (Success): ouro=500, XP=125, itens: 1 item raro
- Efeito 2 (Failure): ouro=250, XP=75, itens: 1 item comum
- **Observação**: RollLimit=11 para sucesso. Texto longo e bem desenvolvido.

**EV 157 - The Spell Council** (disabled=0 — ativo!)
- minLevel=1, allowAtAllLevels=true, allowAtAllTimesOfDay=true
- Texto original: "A group of robed figures approach you, their faces hidden beneath hoods. 'We are the Spell Council,' one of them says. 'We have watched your progress, and we have a proposition for you.'"
- Efeito 1 (Success): ouro=500, XP=125, itens: 1 item raro
- Efeito 2 (Failure): ouro=250, XP=75, itens: 1 item comum
- **Observação**: RollLimit=11 para sucesso. Texto longo e bem desenvolvido.

**EV 159 - Tornado!** (disabled=0 — ativo!)
- minLevel=1, allowAtAllLevels=true, allowAtAllTimesOfDay=true
- Texto original: "A sudden tornado erupts from the ground, swirling debris and sand in its vortex. You see a figure standing amidst the chaos, reaching out to you."
- Efeito 1 (Success): ouro=500, XP=125, itens: 1 item raro
- Efeito 2 (Failure): ouro=250, XP=75, itens: 1 item comum
- **Observação**: RollLimit=10 para sucesso. Evento de ação rápida. Texto curto mas impactante.

**EV 160 - Transcendence** (disabled=0 — ativo!)
- minLevel=1, allowAtAllLevels=true, allowAtAllTimesOfDay=true
- Texto original: "You find yourself in a peaceful grove, cherry blossoms drifting around you like snow. A sense of calm washes over you, and you feel the weight of your journey lifting."
- Efeito 1 (Success): ouro=500, XP=125, itens: 1 item raro, status: Tranquilidade (+1 Wis)
- Efeito 2 (Failure): ouro=250, XP=75, itens: 1 item comum
- **Observação**: RollLimit=0 para sucesso (sempre bem-sucedido). Evento de recompensa garantida. Texto longo e poético.

## Padrões observados

### Padrão de recompensas
Todos os eventos ativos seguem um padrão consistente:
- **Sucesso**: ouro=500, XP=125, 1 item de pool variável (Comum/Raro)
- **Falha**: ouro=250, XP=75, 1 item comum
- **Exceção**: EV 159 (Tornado!) tem RollLimit=10; EV 160 (Transcendence) tem RollLimit=0 (sucesso garantido)

### Padrão de disponibilidade
- Todos têm minLevel=1
- Todos têm allowAtAllLevels=true, allowAtAllTimesOfDay=true
- TerrainTypes e NodeTypes são arrays vazios (sem restrição)
- **Nenhum evento do lote 141-160 restringe terreno ou tipo de nó**

### Padrão de disabled
- **4 ativos**: The Librarian (149), The Mad Mage (150), The Most Dangerous Game (151), The Old Well (152), The runes of the Ymir (155), The Spell Council (157), Tornado! (159), Transcendence (160)
- **6 desativados com texto completo**: The Animator (143), The Fortune Teller (144), The Golden Key (146), The King (147), The Lady (148)
- **4 desativados com efeitos completos**: The Oracle (153), The Pale Knight (154), The Soothsayer (156), Torn Portrait (158)
- **3 protótipos**: Test - Test Key (Get) (141), Test - Test Key (Use) (142), The Fortune Teller (Test) (145)

## Problemas identificados

### P1 — EV 143 (The Animator) tem restrições de spawn muito específicas
O Animator só aparece em terrainType=4 (Caverna) e nodeType=7, com minLevel=3.

**Impacto**: Muito restritivo — limita quando e onde o evento pode aparecer.

**Recomendação**: Considerar relaxar restrições para permitir spawn em mais tipos de terreno (ex: allowOnAllTerrainTypes=1, allowAtAllLevels=1, minLevel=1).

### P2 — Todos os eventos desativados têm texto completo mas estão com disabled=1
6 eventos têm texto e efeitos completos mas estão desativados:
- The Animator (143)
- The Fortune Teller (144)
- The Golden Key (146)
- The King (147)
- The Lady (148)

**Impacto**: Conteúdo polido e testado não está disponível para os jogadores.

**Recomendação**: Avaliar ativar estes eventos ou movê-los para o pool de eventos secundários.

### P3 — RollLimit muito baixo para eventos de desafio
Muitos eventos têm RollLimit=11 (The Librarian, The Mad Mage, The Old Well, The runes of the Ymir, The Spell Council), que é um valor médio-baixo.

**Impacto**: Personagens de nível baixo têm chance razoável de sucesso, mas personagens de nível alto não têm vantagem significativa.

**Recomendação**: Considerar aumentar RollLimit para 15+ em eventos que envolvem "desafio" ou "prova".

### P4 — EV 160 (Transcendence) tem RollLimit=0 (sucesso garantido)
O evento Transcendence tem RollLimit=0, o que significa que **sempre** resulta em sucesso, sem possibilidade de falha.

**Impacto**: Não há risco ou escolha real — o jogador recebe recompensa garantida.

**Recomendação**: Adicionar uma segunda opção (Ação 2: Failure) com RollLimit=0 para permitir falha, ou manter como evento de recompensa garantida se for intencional.

### P5 — Recompensas muito uniformes
Todos os eventos ativos (exceto EV 159 Tornado!) usam exatamente:
- Sucesso: ouro=500, XP=125
- Falha: ouro=250, XP=75

**Impacto**: Nenhum feedback visual ou narrativo de progressão — todos os eventos dão a mesma recompensa.

**Recomendação**: Variar recompensas por tipo de evento (ex: eventos de "desafio" dão mais ouro, eventos de "sabedoria" dão mais XP).

### P6 — Sem status buffs nos eventos desativados
Os eventos desativados (143, 144, 146, 147, 148) não incluem status buffs (Fortitude, etc.) em suas recompensas.

**Impacto**: Se ativados, seriam menos recompensadores que os ativos.

**Recomendação**: Adicionar status buffs equivalentes aos ativos.

### P7 — EV 159 (Tornado!) com RollLimit=10 vs EV 160 (Transcendence) com RollLimit=0
Inconsistência: Tornado! tem RollLimit=10 (desafiante), Transcendence tem RollLimit=0 (garantido).

**Impacto**: Dois eventos consecutivos com dificuldade extrema e nenhuma.

**Recomendação**: Harmonizar RollLimit entre eventos similares (ex: ambos com RollLimit=10, ou ambos com RollLimit=0).

### P8 — Sem distinção por tipo de evento nos efeitos
Todos os eventos têm o mesmo tipo de efeito: ouro + XP + 1 item.

**Impacto**: Falta profundidade mecânica — não há eventos que alterem status, habilidade, ou estado do jogador.

**Recomendação**: Introduzir efeitos variados (ex: curar, remover status negativo, ganhar status temporário, alterar terreno).

## Melhorias sugeridas (priorizadas)

### Alta prioridade (P1, P4)
1. **P1 — Corrigir texto duplicado do EV 143**: Criar texto novo para "The Animator" (sobre animação de bonecos/esculturas).
2. **P4 — Adicionar opção de falha ao EV 160**: Se não for intencional ser sucesso garantido, adicionar Ação 2 com RollLimit=0.

### Média prioridade (P2, P5, P7)
3. **P2 — Ativar eventos desativados**: The Animator, Fortune Teller, Golden Key, King, Lady.
4. **P5 — Variar recompensas por tipo de evento**: Desafio = mais ouro; Sabedoria = mais XP; Perigo = itens raros.
5. **P7 — Harmonizar RollLimit entre eventos similares**: Padronizar RollLimit para 10-15 em todos os eventos de desafio.

### Baixa prioridade (P3, P6, P8)
6. **P3 — Aumentar RollLimit em eventos de desafio**: Para 15+ em eventos que envolvem "prova" ou "desafio".
7. **P6 — Adicionar status buffs aos eventos desativados**: Fortitude, Tranquilidade, etc.
8. **P8 — Introduzir efeitos variados**: Status, curas, remoção de debuffs, etc.

## Resumo executivo

O lote 141-160 contém 20 eventos dos quais 8 estão ativos e 12 desativados. Os eventos ativos são bem estruturados com texto original e efeitos consistentes, mas sofrem de:
- **Texto duplicado** (EV 143 copiado do EV 145)
- **Recompensas uniformes** (todos dão 500/250 ouro, 125/75 XP)
- **Falta de variação mecânica** (todos usam ouro + XP + 1 item)
- **Evento de sucesso garantido** (EV 160)

Os 12 eventos desativados contêm conteúdo polido e testado que poderia ser ativado para expandir o pool de eventos disponíveis.

## Anexos

- Mapeamento completo: `indice-v2.md`
- Detalhes de cada evento: `lote-Normal-v2.md`
- Schema do evento: `schema.md`
- Catálogo de referências: `catalogo-referencias.json`
