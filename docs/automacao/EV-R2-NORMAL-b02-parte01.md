# EV-R2-NORMAL-b02-parte01 - Propostas de melhoria: Eventos 21-40 (Lote Normal)

Arquivo gerado em 2026-10-12
Fonte: docs/cobertura/EV-R1/lote-Normal-v2.md (eventos 21-40)
Status: PROPOSTA para aprovacao do dono

---

## Resumo

Análise de 20 eventos normais (EVT 21-40). Problemas encontrados:

- **3 eventos com `texto` vazio** (EVT 21, 24, 37): sem narrativa principal — o jogador vê "O quê?"
- **2 eventos com `disabled: 1`** (EVT 22, 31): nunca aparecem no jogo
- **6 eventos com 1 única opção** (EVT 21, 24, 28, 35, 37, 40): sem escolha real — decisão forçada
- **5 eventos sem texto de resultado** (EVT 25, 27, 29, 32, 34): o jogador faz algo mas não há narrativa de consequência
- **6 eventos com rolagem não-0 mas sem ação de failure** (EVT 26, 27, 28, 36, 38, 39): se o jogador erra a rolagem, nada acontece — resultado indeterminado

---

## Evento por Evento

---

### EVT 21: Boss Fight - Roland

**Chave:** `resources.assets:2545402` | **Categoria:** Normal — **RARIDADE: Boss** — **Peso: 0.1**
**Terrain:** [7: Snowy Mountain Peak] | **MinLevel:** 6 | **LeadsToFortune: 0**

**Problema:**
- `texto` = (vazio). O jogador é jogado numa boss fight sem saber por quê.
- 1 única opção ("FIGHT") sem alternativa — não é escolha.
- Ações: apenas Success (RollLimit 15). Sem Failure — se o jogador erra, o jogo não define o que acontece.
- Efeitos: XP para party, dano 20% HP/MP para self. Mas sem narrativa de vitória ou derrota.

**O que falta:**
- Texto de narrativa principal (ex: "Roland emerges from the blizzard, his axe raised...")
- Texto de resultado para Success (ex: "You defeat Roland! He drops...")
- Texto de resultado para Failure (ex: "Roland's strike is too powerful...")
- Opção alternativa: "RETREAT" ou "BARGAIN" (ex: pagar ouro para escapar)

**Proposta de melhoria:**
- Adicionar texto base: introduzir o confronto com Roland
- Adicionar texto de Success (vitória) e Failure (derrota)
- Adicionar opção 2: "Retreat" — perde ouro e volta ao mapa, ou "Bribe" — paga ouro para escapar
- Se mantido 1 opção, adicionar ação Failure explícita

**Impacto:** Alto — eventos Boss são marcos da jornada, não devem aparecer sem contexto.

---

### EVT 22: Brawler's Brew

**Chave:** `resources.assets:2545403` | **Categoria:** Normal — **RARIDADE: Common (0)** — **Peso: 1.0**
**Terrain:** [3: Underground Cave] | **MinLevel:** 3 | **LeadsToFortune: 0**
**disabled: 1** — evento DESLIGADO no asset.

**Problema:**
- Evento desativado (`disabled: 1`). Nunca aparece no jogo.
- 3 opções (DRINK, SELL, LEAVE) com narrativas bem escritas e efeitos de status/ouro.
- Opção 2 (SELL) tem `status_requeridos: [5]` — requer status "Brawler's Blessing" ativo.
- Efeitos variados: status de buff, consumo de item, ouro.

**O que falta:**
- N/A (evento desativado propositalmente — pode ser intenção ou bug)

**Proposta de melhoria:**
- Verificar se `disabled: 1` é intencional. Se sim, ignorar.
- Se for bug, reativar (`disabled: 0`) e manter as 3 opções — estão bem implementadas.

**Impacto:** Baixo/Médio — depende da intenção do desenvolvedor.

---

### EVT 23: Cursed Coin Toss

**Chave:** `resources.assets:2545404` | **Categoria:** Normal — **RARIDADE: Common (0)** — **Peso: 1.0**
**Terrain:** [0: Plains, 3: Underground Cave, 9: Dwarven Depths] | **MinLevel:** 1 | **LeadsToFortune: 1**

**Problema:**
- `texto` = (vazio). Sem narrativa de introdução.
- 3 opções de escolha (HEADS, TAILS, WALK AWAY) bem estruturadas.
- Opções 1 e 2 têm rolagem com Intelligence +3, RollLimit 10 — **mas sem ação Failure**.
- Opção 3 (WALK AWAY) tem RollLimit 0 sem rolagem — apenas perde o ouro da aposta.
- Texto de resultado presente para Success de todas as opções, mas não para Failure.

**O que falta:**
- Texto base de introdução (ex: "You spot a hooded figure flipping a tarnished coin...")
- Texto de Failure para as opções HEADS/TAILS (ex: "The coin lands on its edge... you lose your gold")
- Texto de resultado mais detalhado para WALK AWAY

**Proposta de melhoria:**
- Adicionar texto base curto: introduzir a cena
- Adicionar ação Failure (RollLimit 0, sem rolagem) para HEADS e TAILS: perde a aposta
- Expanding texto de WALK AWAY para mais imersivo

**Impacto:** Médio — evento de apostas perde a tensão sem narrativa de introdução e sem consequences de derrota.

---

### EVT 24: Carved Rune

**Chave:** `resources.assets:2545405` | **Categoria:** Normal — **RARIDADE: Common (0)** — **Peso: 1.0**
**Terrain:** [3: Underground Cave, 8: Dark Forest, 9: Dwarven Depths] | **MinLevel:** 3 | **LeadsToFortune: 1**

**Problema:**
- `texto` = (vazio). Sem narrativa principal.
- 1 única opção ("READ") — não é escolha.
- Opção tem rolagem com Intelligence +3, RollLimit 10 — **mas sem ação Failure**.
- Texto de Success presente e bem escrito, mas sem Failure.
- Efeitos: itens de rarezas Uncommon/Very Rare — loot significativo.

**O que falta:**
- Texto base de introdução (ex: "You discover a stone tablet covered in ancient dwarven runes...")
- Texto de Failure (ex: "The runes glow menacingly... you feel a strange energy pull you back")
- Opção alternativa (ex: "IGNORE" — passa direto sem efeito)

**Proposta de melhoria:**
- Adicionar texto base curto
- Adicionar ação Failure para a rolagem
- Adicionar opção 2: "Ignore" — sem efeito, segue viagem

**Impacto:** Médio — evento de loot com apenas 1 opção é linear demais para um evento de 2 raridades diferentes.

---

### EVT 25: Challenger's Gong

**Chave:** `resources.assets:2545406` | **Categoria:** Normal — **RARIDADE: Common (0)** — **Peso: 1.0**
**Terrain:** [7: Snowy Mountain Peak] | **MinLevel:** 1 | **LeadsToFortune: 1**

**Problema:**
- `opcoes[0].texto` = (vazio no asset). O jogador vê apenas o título da opção sem contexto.
- 2 opções: STRIKE (Success) e IGNORE (sem efeito).
- Opção 1 tem RollLimit 0 — não há rolagem.
- Texto de resultado de STRIKE presente, mas curto.

**O que falta:**
- Texto da opção STRIKE (ex: "Ring the gong and challenge the mountain spirits.")
- Texto de Failure se adicionada rolagem futura
- Expansão do texto de resultado para incluir a recompensa

**Proposta de melhoria:**
- Adicionar texto descritivo para a opção STRIKE
- Manter estrutura atual (2 opções simples) — já é funcional
- Considerar adicionar efeito de buff para STRIKE para dar mais peso à escolha

**Impacto:** Baixo — estrutura já existe, só precisa de texto.

---

### EVT 26: Cursed Chest

**Chave:** `resources.assets:2545407` | **Categoria:** Normal — **RARIDADE: Rare (2)** — **Peso: 1.0**
**Terrain:** [3: Underground Cave, 4: Mountain Pass, 8: Dark Forest, 9: Dwarven Depths] | **MinLevel:** 3 | **LeadsToFortune: 0**

**Problema:**
- 2 opções: OPEN e IGNORE. Boa estrutura de escolha.
- Opção 1 (OPEN) tem rolagem Intelligence +3, RollLimit 12 — **mas sem ação Failure**.
- Opção 2 (IGNORE) tem RollLimit 0 — sem efeito, mas não tem texto de narrativa.
- Texto de Success para OPEN presente, mas curto. Sem Failure.

**O que falta:**
- Texto de Failure para OPEN (ex: "You pry open the chest and a cloud of decay engulfs you!")
- Texto descritivo para a opção IGNORE
- Texto de resultado mais imersivo para Success

**Proposta de melhoria:**
- Adicionar ação Failure para OPEN: dano de status/veneno
- Adicionar texto para IGNORE
- Manter estrutura — 2 opções já é bom para um evento de chest

**Impacto:** Médio — chest de rareza rara sem Failure é "tudo ou nada" sem risco narrativo.

---

### EVT 27: Cursed Mimic Chest

**Chave:** `resources.assets:2545408` | **Categoria:** Normal — **RARIDADE: Rare (2)** — **Peso: 1.0**
**Terrain:** [3: Underground Cave, 4: Mountain Pass, 8: Dark Forest, 9: Dwarven Depths] | **MinLevel:** 4 | **LeadsToFortune: 1**

**Problema:**
- 2 opções: OPEN e IGNORE. Boa estrutura.
- Opção 1 (OPEN) tem rolagem Intelligence +3, RollLimit 0 — sem rolagem real.
- Opção 2 (IGNORE) tem RollLimit 0.
- Texto de Success presente para OPEN, mas sem Failure.
- Efeito de OPEN: inicia combate com Cursed Mimic (boss fight).

**O que falta:**
- Se RollLimit=0 mas há `bonus: [Intelligence+3]`, há ambiguidade: a rolagem é usada?
- Texto de Failure se a rolagem for implementada
- Texto de resultado mais detalhado para o combate

**Proposta de melhoria:**
- Clarificar: se RollLimit=0 e Intelligence é bonus mas sem limite, a rolagem é irrelevante
- Ou definir RollLimit > 0 e adicionar ação Failure (ex: "You're too slow — the mimic bites you!")
- Manter estrutura de 2 opções

**Impacto:** Médio — ambiguidade na configuração de rolagem.

---

### EVT 28: Cursed Clock

**Chave:** `resources.assets:2545409` | **Categoria:** Normal — **RARIDADE: Common (0)** — **Peso: 1.0**
**Terrain:** [3: Underground Cave] | **MinLevel:** 3 | **LeadsToFortune: 0**

**Problema:**
- 1 única opção ("PULL AWAY") — sem escolha.
- Opção tem rolagem Might +0, RollLimit 8 — **mas sem ação Failure**.
- Texto de Success bem escrito, mas sem Failure.
- Efeitos: ouro e XP.

**O que falta:**
- Opção alternativa (ex: "SURRENDER" — perde status/ouro mas escapa)
- Texto de Failure para PULL AWAY

**Proposta de melhoria:**
- Adicionar opção 2: "Surrender" — perde um pouco de ouro/XP mas escapa do encanto
- Adicionar ação Failure para PULL AWAY

**Impacto:** Médio — evento hipnótico com 1 opção é linear demais.

---

### EVT 29: Cursed Tome

**Chave:** `resources.assets:2545410` | **Categoria:** Normal — **RARIDADE: Common (0)** — **Peso: 1.0**
**Terrain:** [3: Underground Cave, 4: Mountain Pass, 8: Dark Forest, 9: Dwarven Depths] | **MinLevel:** 3 | **LeadsToFortune: 1**

**Problema:**
- 2 opções: READ e CLOSE. Boa estrutura.
- Opção 1 (READ) tem rolagem Intelligence +3, RollLimit 10 — **mas sem ação Failure**.
- Opção 2 (CLOSE) tem RollLimit 0.
- `LeadsToFortune: 1` — mas sem Fortuna visível nos efeitos (sem item especial).
- Texto de Success presente, curto. Sem Failure.

**O que falta:**
- Texto de Failure para READ (ex: "The words twist in your mind... you gain a debuff!")
- Texto de resultado mais detalhado para READ Success
- Verificar LeadsToFortune: deve gerar item especial?

**Proposta de melhoria:**
- Adicionar ação Failure para READ: efeito de debuff (ex: "Confused" status)
- Se LeadsToFortune=1, garantir que Success dá item especial
- Manter estrutura de 2 opções

**Impacto:** Médio — livro amaldiçoado sem risco de ler errado perde a temática.

---

### EVT 30: Dark Discoveries

**Chave:** `resources.assets:2545411` | **Categoria:** Normal — **RARIDADE: Common (0)** — **Peso: 1.0**
**Terrain:** [8: Dark Forest] | **MinLevel:** 3 | **LeadsToFortune: 0**

**Problema:**
- 2 opções: ACCEPT e REFUSE. Boa estrutura.
- Nenhuma opção tem rolagem (RollLimit 0, bonus: []) — decisão pura.
- Texto de Success para ACCEPT presente, curto. Sem texto para REFUSE.
- Efeitos de ACCEPT: itens e status.

**O que falta:**
- Texto descritivo para a opção REFUSE
- Texto de resultado para REFUSE (ex: "You decline. The Necromancer's eyes narrow...")
- O REFUSE deveria ter alguma consequência (ex: perder reputação, ou o Necromancer fica hostil)

**Proposta de melhoria:**
- Adicionar consequência para REFUSE (não deixar "sem efeito")
- Adicionar texto para REFUSE
- Considerar rolagem sutil no ACCEPT para dar risco

**Impacto:** Baixo/Médio — decisão binária sem rolagem é aceitável se as consequências forem claras.

---

### EVT 31: Dead Adventurer

**Chave:** `resources.assets:2545412` | **Categoria:** Normal — **RARIDADE: Common (0)** — **Peso: 1.0**
**Terrain:** [0: Plains, 3: Underground Cave, 8: Dark Forest, 9: Dwarven Depths] | **MinLevel:** 1 | **LeadsToFortune: 1**
**disabled: 1** — evento DESLIGADO no asset.

**Problema:**
- Evento desativado (`disabled: 1`).
- 1 opção: REACH — dá status [o1a1_status].
- Texto de Success presente, curto.

**O que falta:**
- N/A (evento desativado)

**Proposta de melhoria:**
- Verificar se `disabled: 1` é intencional
- Se reativar, considerar adicionar opção 2: "IGNORE" — sem efeito

**Impacto:** Baixo — depende de intenção do dev.

---

### EVT 32: Desecrated Statue of the First Mountain King

**Chave:** `resources.assets:2545413` | **Categoria:** Normal — **RARIDADE: Common (0)** — **Peso: 1.0**
**Terrain:** [9: Dwarven Depths] | **MinLevel:** 3 | **LeadsToFortune: 0**

**Problema:**
- 2 opções: ACCEPT e DECLINE. Boa estrutura.
- Nenhuma opção tem rolagem (RollLimit 0, bonus: []) — decisão pura.
- Texto de Accept presente, curto. Sem texto para Decline.
- Aceitar gera um quest/objetivo (ajudar o Rei Montanha).

**O que falta:**
- Texto de resultado para DECLINE (ex: "You turn away. The statue's eyes follow you...")
- Texto de Accept mais detalhado

**Proposta de melhoria:**
- Adicionar consequência para DECLINE (ex: a statue insulta você, ou bloqueia um caminho)
- Manter estrutura atual — decisão pura é aceitável para quests

**Impacto:** Baixo — estrutura já boa.

---

### EVT 33: Disturbing Diner

**Chave:** `resources.assets:2545414` | **Categoria:** Normal — **RARIDADE: Common (0)** — **Peso: 1.0**
**Terrain:** [3: Underground Cave, 8: Dark Forest] | **MinLevel:** 1 | **LeadsToFortune: 0**

**Problema:**
- 3 opções: CRUSTY COCKROACH, SOUP OF DOOM, TENTACLE DELIGHT. Boa estrutura.
- Cada opção tem rolagem com Vitality +2, RollLimit 0 — sem rolagem real.
- Texto de Success para cada opção presente e bem escrito.
- Sem Failure em nenhuma opção.

**O que falta:**
- Se RollLimit=0 mas Vitality é bonus, há ambiguidade
- Texto de Failure para cada opção (ex: "The food is too gross — you lose HP!")
- Se RollLimit=0 intencionalmente, remover `bonus: [Vitality]` para clareza

**Proposta de melhoria:**
- Definir claramente: se não há rolagem, remover `bonus: [Vitality]`
- OU definir RollLimit > 0 e adicionar Failure para cada opção
- Manter as 3 opções — diversidade de escolha é boa

**Impacto:** Médio — ambiguidade de rolagem + 3 opções sem Failure.

---

### EVT 34: Disturbing Statue

**Chave:** `resources.assets:2545415` | **Categoria:** Normal — **RARIDADE: Common (0)** — **Peso: 1.0**
**Terrain:** [8: Dark Forest] | **MinLevel:** 1 | **LeadsToFortune: 0**

**Problema:**
- 2 opções: CRAFT e IGNORE. Boa estrutura.
- Opção 1 (CRAFT) tem rolagem Intelligence +3, RollLimit 10 — **mas sem ação Failure**.
- Opção 2 (IGNORE) tem RollLimit 0.
- Efeito de CRAFT: forja item com atributo bônus.

**O que falta:**
- Texto de Failure para CRAFT (ex: "The metal shatters — you waste your materials")
- Texto descritivo para IGNORE
- Texto de resultado mais detalhado para CRAFT Success

**Proposta de melhoria:**
- Adicionar ação Failure para CRAFT: perde materiais
- Manter 2 opções — estrutura boa para evento de crafting

**Impacto:** Médio — crafting sem risco de falhar é sempre benéfico (pode ser intenção).

---

### EVT 35: Dwarven Sentry Wall

**Chave:** `resources.assets:2545416` | **Categoria:** Normal — **RARIDADE: Common (0)** — **Peso: 1.0**
**Terrain:** [4: Mountain Pass, 9: Dwarven Depths] | **MinLevel:** 1 | **LeadsToFortune: 0**

**Problema:**
- 1 única opção ("ACT") — sem escolha.
- Opção tem rolagem Intelligence +3, RollLimit 10 — **mas sem ação Failure**.
- Texto de Success bem escrito.
- Efeitos: XP e itens.

**O que falta:**
- Opção alternativa (ex: "FIGHT" — combate com sentinela, ou "BRI BE" — paga ouro)
- Texto de Failure para ACT

**Proposta de melhoria:**
- Adicionar opção 2: "Fight" — combate com sentinela (mais risco, mais recompensa)
- Ou: "Bribe" — perde ouro, passa sem rolagem
- Adicionar ação Failure para ACT

**Impacto:** Médio — sentinela dwarf com 1 opção é linear demais.

---

### EVT 36: Dwarven Tomb

**Chave:** `resources.assets:2545417` | **Categoria:** Normal — **RARIDADE: Common (0)** — **Peso: 1.0**
**Terrain:** [9: Dwarven Depths, 4: Mountain Pass] | **MinLevel:** 1 | **LeadsToFortune: 1**

**Problema:**
- 2 opções: LOOT e LEAVE. Boa estrutura.
- Opção 1 (LOOT) tem rolagem Might +0, RollLimit 16 — **mas sem ação Failure**.
- Opção 2 (LEAVE) tem RollLimit 0.
- `LeadsToFortune: 1` — dá item especial no Success.

**O que falta:**
- Texto de Failure para LOOT (ex: "The tomb collapses! You barely escape...")
- Texto descritivo para LEAVE
- Texto de resultado mais detalhado para LOOT Success

**Proposta de melhoria:**
- Adicionar ação Failure para LOOT: dano por desmoronamento
- Manter 2 opções — boa estrutura para evento de tomb

**Impacto:** Médio — tomb sem Failure é "loot gratuito".

---

### EVT 37: Dwarven Tribute

**Chave:** `resources.assets:2545418` | **Categoria:** Normal — **RARIDADE: Common (0)** — **Peso: 1.0**
**Terrain:** [0: Plains, 3: Underground Cave, 8: Dark Forest, 9: Dwarven Depths] | **MinLevel:** 1 | **LeadsToFortune: 0**

**Problema:**
- `texto` = (vazio). Sem narrativa principal.
- 1 única opção ("PAY") — sem escolha.
- Opção tem rolagem Intelligence +3, RollLimit 10 — **mas sem ação Failure**.
- Texto de Success presente, curto.
- Efeito: dá item ao矮人, recebe ouro de volta.

**O que falta:**
- Texto base de introdução
- Texto de Failure
- Opção alternativa (ex: "STEAL" — risco alto, ou "IGNORE")

**Proposta de melhoria:**
- Adicionar texto base
- Adicionar ação Failure para PAY
- Adicionar opção 2: "Steal" (rolagem mais difícil, mais risco)

**Impacto:** Médio — evento de tributo dwarf sem contexto é confuso.

---

### EVT 38: Dwarven Forge

**Chave:** `resources.assets:2545419` | **Categoria:** Normal — **RARIDADE: Common (0)** — **Peso: 1.0**
**Terrain:** [3: Underground Cave, 9: Dwarven Depths] | **MinLevel:** 3 | **LeadsToFortune: 1**

**Problema:**
- 2 opções: FORGE e BUY. Boa estrutura.
- Opção 1 (FORGE) tem rolagem Intelligence +3, RollLimit 10 — **mas sem ação Failure**.
- Opção 2 (BUY) tem rolagem Intelligence +3, RollLimit 10 — **mas sem ação Failure**.
- Ambas dão itens de forja (diferentes raridades/preços).
- `LeadsToFortune: 1`.

**O que falta:**
- Texto de Failure para FORGE (ex: "The forge rejects your attempt!")
- Texto de Failure para BUY (ex: "The merchant refuses — you lack the knowledge!")
- Texto de resultado mais detalhado para ambas

**Proposta de melhoria:**
- Adicionar Failure para ambas as opções
- Manter 2 opções — boa estrutura de escolha (craft vs compra)

**Impacto:** Médio — forge sem Failure é sempre benéfico.

---

### EVT 39: Dwarven Market

**Chave:** `resources.assets:2545420` | **Categoria:** Normal — **RARIDADE: Common (0)** — **Peso: 1.0**
**Terrain:** [9: Dwarven Depths] | **MinLevel:** 3 | **LeadsToFortune: 0**

**Problema:**
- 3 opções: BUY, SELL, LEAVE. Boa estrutura.
- Opção 1 (BUY) tem rolagem Intelligence +3, RollLimit 10 — **mas sem ação Failure**.
- Opção 2 (SELL) tem rolagem Intelligence +3, RollLimit 10 — **mas sem ação Failure**.
- Opção 3 (LEAVE) tem RollLimit 0.
- Todas têm efeitos de itens/ouro.
- `LeadsToFortune: 1` no evento mas sem Fortuna visível.

**O que falta:**
- Texto de Failure para BUY e SELL
- Texto de resultado mais detalhado para cada opção
- Verificar LeadsToFortune

**Proposta de melhoria:**
- Adicionar Failure para BUY e SELL
- Manter 3 opções — estrutura já excelente para mercado

**Impacto:** Médio — mercado sem Failure de rolagem pode ser explorado.

---

### EVT 40: Enchanted Axe

**Chave:** `resources.assets:2545421` | **Categoria:** Normal — **RARIDADE: Common (0)** — **Peso: 1.0**
**Terrain:** [0: Plains, 3: Underground Cave, 8: Dark Forest, 9: Dwarven Depths] | **MinLevel:** 1 | **LeadsToFortune: 0**

**Problema:**
- 1 única opção ("DISRUPT") — sem escolha.
- Opção tem rolagem Dexterity +1, RollLimit 10 — **mas sem ação Failure**.
- Texto de Success presente, curto.
- Efeito: XP e ouro.

**O que falta:**
- Opção alternativa (ex: "SMASH" — combate com a axa encantada, ou "PASS" — desvia)
- Texto de Failure

**Proposta de melhoria:**
- Adicionar opção 2: "Smash" — combate direto com a axa (mais risco)
- Ou: "Pass" — contorna sem rolagem
- Adicionar ação Failure para DISRUPT

**Impacto:** Baixo/Médio — evento simples, 1 opção é aceitável se o contexto for adicionado.

---

## Resumo Estatístico

| Problema | Quantidade | Eventos |
|----------|-----------|---------|
| `texto` vazio | 3 | 21, 24, 37 |
| `disabled: 1` | 2 | 22, 31 |
| 1 única opção | 6 | 21, 24, 28, 35, 37, 40 |
| Sem texto de resultado | 5 | 25, 27, 29, 32, 34 |
| Rolagem sem Failure | 6 | 26, 27, 28, 36, 38, 39 |

## Prioridades de Correção

1. **Alta:** EVT 21 (Boss Roland) — sem texto, sem Failure, sem escolha. Evento crítico do jogo.
2. **Alta:** EVT 24 (Carved Rune) — sem texto, sem Failure, 1 opção, loot raro.
3. **Alta:** EVT 27 (Cursed Mimic Chest) — ambiguidade de rolagem, sem Failure.
4. **Média:** EVT 22, 31 — verificar se `disabled: 1` é intencional.
5. **Média:** EVT 23, 28, 29, 35, 37, 40 — eventos com 1 opção e/ou sem Failure.
6. **Baixa:** EVT 25, 26, 30, 32, 33, 34, 36, 38, 39 — estrutura boa, só precisa de textos/Failures.

## Observações Gerais

- **LeadsToFortune sem Fortuna:** EVT 29, 36, 38, 39 marcados com `LeadsToFortune: 1` mas sem item especial visível. Verificar se a fortuna é aplicada em lógica não documentada.
- **Rolagem sem Failure:** 6 eventos têm `RollLimit > 0` e `bonus` mas nenhuma ação Failure. Isso significa que o jogador pode falhar a rolagem sem consequência — o que quebra a tensão do evento.
- **Terrenos:** Eventos 21-40 cobrem terrenos variados: Plains, Underground Cave, Mountain Pass, Dark Forest, Dwarven Depths, Snowy Mountain Peak. Boa distribuição.
- **Raridades:** A maioria é Common. EVT 21 é Boss (peso 0.1). EVT 26 e 27 são Rare. Bom mix.
