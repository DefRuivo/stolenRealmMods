# EV-R2-NORMAL-b07 — Análise Eventos 121–140 (Lote Normal)
**Arquivo fonte:** `docs/cobertura/EV-R1/lote-Normal-v2.md` (seções 121–140)
**Cruzamento:** `docs/cobertura/EV-R1/eventos.json` | Schema: `eventos.schema.json`
**Data de análise:** 2026-10-12

---

## Resumo do lote

- **Total analisado:** 20 de 20 eventos
- **MANTER (ativos, sem mudança):** 4 (128 The Fortune Teller, 134 The Mad Mage, 135 The Most Dangerous Game, 136 The Old Well)
- **MELHORAR (wording):** 9 (127, 130, 131, 132, 133, 137, 138, 139, 140)
- **MANTER (testes, disabled):** 7 (121–126, 129)
- **Testes internos:** 6 (121–127)
- **Eventos de produção disabled:** 6 (130–132, 137–138, 140)
- **Evento com ref/nome=NULL (ativo):** 1 (139 The runes of the Ymir) — aparece 5x no JSON com path_ids diferentes

> *Nota: 129 é cópia de teste de 128 (Fortune Teller Test), também disabled.*

---

## Inventário de decisões por evento

### EV-121 — Test - Boss Event Start
- **Chave:** `resources.assets:2545723`
- **Texto original:** (string vazia no asset)
- **Categoria:** Teste
- **Raridade:** não informada no JSON (comum entre testes)
- **Peso relativo:** 1.0
- **Veredito:** **MANTER** (evento de teste, disabled)
- **Anomalias:**
  - `disabled: 1`
  - `resultados_possiveis` = (string vazia no asset)
  - `texto_original` = (string vazia no asset)
  - `historia: NonStoryOnly`
  - `allowedNodeTypes: [7]`
- **Justificativa:** Evento de teste interno sem conteúdo de produção. Manter disabled.

---

### EV-122 — Test - Choose As Party Event
- **Chave:** `resources.assets:2545724`
- **Texto original:** (string vazia no asset)
- **Categoria:** Teste
- **Veredito:** **MANTER** (evento de teste, disabled)
- **Anomalias:**
  - `disabled: 1`
  - `referencia` = NULL (referência nula sem nome)
  - `nome` = NULL
  - `resultados_possiveis` = Which will you choose? (texto presente)
  - 3 opções: Open., Close, Mystery
- **Justificativa:** Evento de teste com dados parciais mas sem referência. Manter disabled.

---

### EV-123 — Test - Choose One Character Event
- **Chave:** `resources.assets:2545725`
- **Texto original:** (string vazia no asset)
- **Categoria:** Teste
- **Veredito:** **MANTER** (evento de teste, disabled)
- **Anomalias:**
  - `disabled: 1`
  - `resultados_possiveis` = Who will dare open this chest?
  - 3 opções: Open., Open Better, Close
- **Justificativa:** Evento de teste sem conteúdo de produção. Manter disabled.

---

### EV-124 — Test - Individual Event
- **Chave:** `resources.assets:2545726`
- **Texto original:** (string vazia no asset)
- **Categoria:** Teste
- **Veredito:** **MANTER** (evento de teste, disabled)
- **Anomalias:**
  - `disabled: 1`
  - `resultados_possiveis` = (string vazia no asset)
  - `LeadsToFortune: 0`
- **Justificativa:** Evento de teste sem conteúdo. Manter disabled.

---

### EV-125 — Test - Test Key (Get)
- **Chave:** `resources.assets:2545727`
- **Texto original:** (string vazia no asset)
- **Categoria:** Teste
- **Veredito:** **MANTER** (evento de teste, disabled)
- **Anomalias:**
  - `disabled: 1`
  - `resultados_possiveis` = (string vazia no asset)
  - Opções: Take Key, Leave
- **Justificativa:** Evento de teste. Manter disabled.

---

### EV-126 — Test - Test Key (Use)
- **Chave:** `resources.assets:2545728`
- **Texto original:** (string vazia no asset)
- **Categoria:** Teste
- **Veredito:** **MANTER** (evento de teste, disabled)
- **Anomalias:**
  - `disabled: 1`
  - `resultados_possiveis` = (string vazia no asset)
  - Opções: Open., Get Key, Leave
- **Justificativa:** Evento de teste. Manter disabled.

---

### EV-127 — The Animator
- **Chave:** `resources.assets:2545729` (ou `2545731` — há duplicação no JSON)
- **Texto original:** (string vazia no asset)
- **Categoria:** Evento de produção
- **Veredito:** **MELHORAR — wording**
- **Anomalias:**
  - `disabled: 0` (ATIVO)
  - `resultados_possiveis` = (string vazia no asset)
  - Opções: Accept, Leave
  - Peso: 1.0
- **Justificativa:** Evento ativo sem texto original nem resultados possíveis no asset. Proposta:
  - TEXTO: (string vazia no asset) → **Proposta:** "A figura animada por magia se aproxima de você, seu rosto distorcido em uma careta de curiosidade. Ela estende uma mão cerimonial."
  - RESULTADOS: (string vazia) → **Proposta:** "A criatura mágica observa seus movimentos com atenção, aguardando sua decisão."

---

### EV-128 — The Fortune Teller
- **Chave:** `resources.assets:2545730` (ou `2545732` — há duplicação no JSON)
- **Texto original:** (string vazia no asset)
- **Categoria:** Evento de produção
- **Raridade:** Common | Peso: 1.0
- **Veredito:** **MANTER**
- **Anomalias:**
  - `disabled: 0` (ATIVO)
  - `resultados_possiveis` = Dare to gaze into the Crystal Ball?
  - 3 opções com rolagem de skill: See, Witness, View — todas com RollLimit 11 (Success) e RollLimit 1 (Failure)
  - Condições: terrainTypes = [2, 0, 1, 4, 5, 0] (inclui 4 tipos distintos + duplicata de 0)
- **Justificativa:** Evento bem estruturado com 3 opções de玩法 (ver/espectar/examinar), rolagem consistente. Manter.

---

### EV-129 — The Fortune Teller (Test)
- **Chave:** `resources.assets:2545733`
- **Texto original:** (string vazia no asset)
- **Categoria:** Teste (cópia de 128)
- **Veredito:** **MANTER** (evento de teste, disabled)
- **Anomalias:**
  - `disabled: 1`
  - `referencia` = NULL, `nome` = NULL
  - Mesmo structure de 128 (3 opções, rolagem 11/1)
- **Justificativa:** Cópias de teste duplicadas. Manter disabled.

---

### EV-130 — The Golden Key
- **Chave:** `resources.assets:2545735`
- **Texto original:** (string vazia no asset)
- **Categoria:** Evento de produção
- **Raridade:** Common | Peso: 1.0
- **Veredito:** **MELHORAR — wording**
- **Anomalias:**
  - `disabled: 1`
  - `resultados_possiveis` = (string vazia no asset)
  - Opções: Reach, Leave
- **Justificativa:** Evento disabled, sem conteúdo. Se reativado no futuro, necessita wording completo.

---

### EV-131 — The King
- **Chave:** `resources.assets:2545736`
- **Texto original:** (string vazia no asset)
- **Categoria:** Evento de produção
- **Raridade:** Common | Peso: 1.0
- **Veredito:** **MELHORAR — wording**
- **Anomalias:**
  - `disabled: 1`
  - `resultados_possiveis` = (string vazia no asset)
  - Opções: Reach, Leave
- **Justificativa:** Evento disabled, sem conteúdo. Se reativado, necessita wording completo.

---

### EV-132 — The Lady
- **Chave:** `resources.assets:2545737`
- **Texto original:** (string vazia no asset)
- **Categoria:** Evento de produção
- **Raridade:** Common | Peso: 1.0
- **Veredito:** **MELHORAR — wording**
- **Anomalias:**
  - `disabled: 1`
  - `resultados_possiveis` = (string vazia no asset)
  - Opções: Reach, Leave
- **Justificativa:** Evento disabled, sem conteúdo. Se reativado, necessita wording completo.

---

### EV-133 — The Librarian
- **Chave:** `resources.assets:2545738`
- **Texto original:** (string vazia no asset)
- **Categoria:** Evento de produção
- **Raridade:** Common | Peso: 1.0
- **Veredito:** **MELHORAR — wording**
- **Anomalias:**
  - `disabled: 0` (ATIVO)
  - `referencia` = NULL, `nome` = NULL (referência nula sem nome)
  - `resultados_possiveis` = What will you do?
  - Opções: Search (RollLimit 10/0), Leave
- **Justificativa:** Evento ativo sem referência de quest/objeto e sem texto. Proposta:
  - TEXTO: (string vazia no asset) → **Proposta:** "Um ser feito de papel e tinta vive dentro de uma estante antiga. Ele a observa com olhos de tinta que brilham."
  - RESULTADOS: (string vazia) → **Proposta:** "O bibliotecário de papel aguarda sua resposta, as páginas rangendo ao vento."
  - NOTA: referencia=NULL é uma anomalia — o evento não está vinculado a nenhuma quest no catálogo. Verificar se é intencional.

---

### EV-134 — The Mad Mage
- **Chave:** `resources.assets:2545739` (ou `2545740`, `2545741` — há 3 entradas duplicadas no JSON)
- **Texto original:** (string vazia no asset)
- **Categoria:** Evento de produção
- **Veredito:** **MANTER**
- **Anomalias:**
  - `disabled: 0` (ATIVO)
  - `resultados_possiveis` = (string vazia no asset)
  - Opções: Break, Leave
  - Peso: 1.0
- **Justificativa:** Evento ativo mas sem texto. Manter (o jogo pode ter conteúdo adicional em runtime).

---

### EV-135 — The Most Dangerous Game
- **Chave:** `resources.assets:2545742`
- **Texto original:** (string vazia no asset)
- **Categoria:** Evento de produção
- **Raridade:** Common | Peso: 1.0
- **Veredito:** **MANTER**
- **Anomalias:**
  - `disabled: 0` (ATIVO)
  - `resultados_possiveis` = (string vazia no asset)
  - Opção: Recount com rolagem (RollLimit 15/0)
- **Justificativa:** Evento ativo sem texto no asset. Manter (pode ter conteúdo runtime).

---

### EV-136 — The Old Well
- **Chave:** `resources.assets:2545743`
- **Texto original:** (string vazia no asset)
- **Categoria:** Evento de produção
- **Raridade:** Common | Peso: 1.0
- **Veredito:** **MANTER**
- **Anomalias:**
  - `disabled: 0` (ATIVO)
  - `resultados_possiveis` = (string vazia no asset)
  - Opções: Climb (RollLimit 8/1), Leave
  - `terrainTypesAllowedAtAnyTime` não definido; `allowedTerrainTypes` = [2, 0, 1, 4, 5, 0]
- **Justificativa:** Evento ativo com mecânica de rolagem bem definida. Manter.

---

### EV-137 — The Oracle
- **Chave:** `resources.assets:2545744`
- **Texto original:** (string vazia no asset)
- **Categoria:** Evento de produção
- **Raridade:** Common | Peso: 1.0
- **Veredito:** **MELHORAR — wording**
- **Anomalias:**
  - `disabled: 1`
  - `resultados_possiveis` = (string vazia no asset)
  - Opções: Close, Far
  - `allowedTimeOfDay: 1` (só durante o dia)
  - `terrainTypesAllowedAtAnyTime: [4, 3]` (floresta e planície?)
- **Justificativa:** Evento disabled com condições específicas de tempo/terreno. Se reativado, necessita wording.

---

### EV-138 — The Pale Knight
- **Chave:** `resources.assets:2545745`
- **Texto original:** (string vazia no asset)
- **Categoria:** Evento de produção
- **Raridade:** Rare | Peso: 1.0
- **Veredito:** **MELHORAR — wording**
- **Anomalias:**
  - `disabled: 1`
  - `resultados_possiveis` = (string vazia no asset)
  - Opções: Open, Leave
  - `allowedTimeOfDay: 1` (só dia)
  - `terrainTypesAllowedAtAnyTime: [4, 0, 3, 5]`
- **Justificativa:** Evento Rare disabled. Se reativado, necessita wording completo.

---

### EV-139 — The runes of the Ymir
- **Chave:** `resources.assets:2545780` (e variantes 2545781, 2545783, 2545785 — 4 duplicatas ativas no JSON)
- **Texto original:** (string vazia no asset)
- **Categoria:** Evento de produção
- **Raridade:** Common | Peso: 1.0
- **Veredito:** **MELHORAR — wording + referências**
- **Anomalias:**
  - `disabled: 0` (ATIVO — 4 variantes)
  - `referencia` = NULL, `nome` = NULL
  - `resultados_possiveis` = Will you touch the Rune?
  - Opções: Touch (RollLimit 0/0 — sucesso automático), Leave
  - Condição especial: `minLevel: 3`, `allowedTerrainTypes: [7]`, `allowedNodeTypes: [7]`
- **Justificativa:** Evento ativo com 4 variantes mas sem referência de quest e sem texto. Ocorrendo no tipo de terreno 7 (Rune Stone?).
  - TEXTO: → **Proposta:** "Runas antigas brilham em uma pedra coberta de musgo. O poder do Ymir pulsa através dos símbolos esculpidos."
  - RESULTADOS: (string vazia) → **Proposta:** "O poder das runas invade sua mente, revelando visões do mundo antigo."
  - NOTA: referencia=NULL em evento ativo é anomalia — sem vínculo com quest catalogada.

---

### EV-140 — The Soothsayer
- **Chave:** `resources.assets:2545746`
- **Texto original:** (string vazia no asset)
- **Categoria:** Evento de produção
- **Raridade:** Common | Peso: 1.0
- **Veredito:** **MELHORAR — wording**
- **Anomalias:**
  - `disabled: 1`
  - `resultados_possiveis` = (string vazia no asset)
  - 3 opções: See, Witness, View — todas com RollLimit 0 (sucesso automático)
  - `LeadsToFortune: 1`
  - `allowedTimeOfDay: 1`, `terrainTypesAllowedAtAnyTime: [4, 3]`
- **Justificativa:** Evento disabled que leva a fortuna (LeadsToFortune=1). Se reativado, necessita wording.

---

## Inventário de Decisões (tabela)

| Evento | Título | Categoria | Raridade | Peso | Disabled | Veredito | Natureza |
|--------|--------|-----------|----------|------|----------|----------|----------|
| 121 | Test - Boss Event Start | Teste | - | 1.0 | 1 | MANTER | - |
| 122 | Test - Choose As Party Event | Teste | - | 1.0 | 1 | MANTER | - |
| 123 | Test - Choose One Character Event | Teste | - | 1.0 | 1 | MANTER | - |
| 124 | Test - Individual Event | Teste | - | 1.0 | 1 | MANTER | - |
| 125 | Test - Test Key (Get) | Teste | - | 1.0 | 1 | MANTER | - |
| 126 | Test - Test Key (Use) | Teste | - | 1.0 | 1 | MANTER | - |
| 127 | The Animator | Produção | - | 1.0 | 0 | MELHORAR | wording |
| 128 | The Fortune Teller | Produção | Common | 1.0 | 0 | MANTER | - |
| 129 | The Fortune Teller (Test) | Teste | - | 1.0 | 1 | MANTER | - |
| 130 | The Golden Key | Produção | Common | 1.0 | 1 | MELHORAR | wording |
| 131 | The King | Produção | Common | 1.0 | 1 | MELHORAR | wording |
| 132 | The Lady | Produção | Common | 1.0 | 1 | MELHORAR | wording |
| 133 | The Librarian | Produção | Common | 1.0 | 0 | MELHORAR | wording + ref |
| 134 | The Mad Mage | Produção | - | 1.0 | 0 | MANTER | - |
| 135 | The Most Dangerous Game | Produção | Common | 1.0 | 0 | MANTER | - |
| 136 | The Old Well | Produção | Common | 1.0 | 0 | MANTER | - |
| 137 | The Oracle | Produção | Common | 1.0 | 1 | MELHORAR | wording |
| 138 | The Pale Knight | Produção | Rare | 1.0 | 1 | MELHORAR | wording |
| 139 | The runes of the Ymir | Produção | Common | 1.0 | 0 | MELHORAR | wording + ref |
| 140 | The Soothsayer | Produção | Common | 1.0 | 1 | MELHORAR | wording |

---

## Anomalias globais do lote

1. **TEXTOS VAZIOS NO ASSET:** 19/20 eventos têm `(string vazia no asset)` no `texto_original`. Apenas 128 tem `resultados_possiveis` preenchido.
2. **REFERÊNCIAS NULAS EM EVENTOS ATIVOS:** EV-133 (The Librarian) e EV-139 (The runes of the Ymir) têm `referencia=NULL` e `nome=NULL` mas estão `disabled: 0`.
3. **DUPLICAÇÕES NO JSON:**
   - `The Animator`: 2 entradas (path_ids 2545729 e 2545731)
   - `The Fortune Teller`: 2 entradas (2545730 ativa, 2545732 ativa, 2545733 teste)
   - `The Mad Mage`: 3 entradas (2545739, 2545740, 2545741)
   - `The runes of the Ymir`: 4 entradas ativas (2545780, 2545781, 2545783, 2545785)
4. **EVENTOS DE PRODUÇÃO DISABLED:** 6 eventos (130, 131, 132, 137, 138, 140) — todos sem texto.
5. **EVENTOS DE TESTE:** 6 eventos (121-127) + 1 teste (129) = 7 eventos de teste no lote.
6. **DUPLO TIPO DE TERRENO:** EV-128 e EV-136 têm `[2, 0, 1, 4, 5, 0]` — o tipo 0 aparece duas vezes (possível erro de digitação).
7. **ROLLLIMIT 0 EM SUCESSO AUTOMÁTICO:** EV-140 (Soothsayer) tem 3 opções com RollLimit 0 — sucesso garantido em evento que leva a fortuna.

---

## Contagem final

**Análise concluída: 20 de 20 eventos do lote Normal (EV-R2-NORMAL-b07)**

---

## Notas para o dono

- O lote tem **7 eventos de teste** (121-127 + 129) que devem permanecer disabled.
- **6 eventos de produção** estão ativos e com wording ausente no asset: 127, 128, 133, 134, 135, 136.
- **7 eventos de produção** estão disabled sem conteúdo: 130, 131, 132, 137, 138, 140.
- **4 eventos** têm duplicações no eventos.json — verificar se são intentional (variantes de terreno).
- **2 eventos ativos** (133, 139) têm `referencia=NULL` — sem vínculo com quests no catálogo.
