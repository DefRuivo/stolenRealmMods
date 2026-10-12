# EV-R2-NORMAL-b04 — Propostas de melhoria (eventos 61–80)

Gerado: 2026-10-12
Fonte: `docs/cobertura/EV-R1/lote-Normal-v2.md` seções 61–80 (linhas ~18047–24100)

---

## Evento 61 — Horn of Glorious Battle
**Chave:** `resources.assets:2545466`
**Título:** Horn of Glorious Battle
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `You sound the horn of glory — the battle ahead promises riches beyond measure.`
**Justificativa:** Evento com texto original vazio e recompensa de combate configurada (inimigos definidos, loot XP). Jogador merece contexto narrativo antes do combate.

**Anomalias:**
- `texto_original`: string vazia — asset não contém texto.
- `recompensa_final`: NULL (NÃO_EXERCITADO) — loot/XP/oro resolvidos no runtime.
- `combate`: Forged Enemies com `IsSuperUnique=1` para "Horn of Glorious Battle" — referência preservada.

---

## Evento 62 — Inconspicuous Burning Demon Skull
**Chave:** `resources.assets:2545467`
**Título:** Inconspicuous Burning Demon Skull
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `A demon skull smolders faintly, as though its flames are trying to whisper something.`
**Justificativa:** Texto vazio para um item visualmente distincto (crânio em chamas). Jogador precisa de dica narrativa sobre o que interagir.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).
- Encadeia evento: verificado no fluxo (next event link).

---

## Evento 63 — Taste for Blood 1
**Chave:** `resources.assets:2545650`
**Título:** Taste for Blood 1
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `The smell of fresh blood hangs in the air — you can feel the urge to hunt.`
**Justificativa:** Evento de combate com efeito de status (Weakened -20% Might). Texto vazio não prepara o jogador para a decisão.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).
- Encadeia: `resources.assets:2545716` — "Taste for Blood 1".

---

## Evento 64 — Ornate Chest
**Chave:** `resources.assets:2545469`
**Título:** Ornate Chest
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `An ornate chest sits in the corner, its lock tarnished but intact. It could hold something of value.`
**Justificativa:** Baú decorado merece descrição — jogador precisa saber se vale a pena arriscar abrir.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).

---

## Evento 65 — A Strange Offering
**Chave:** `resources.assets:2545470`
**Título:** A Strange Offering
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `A stone altar bears a strange offering — something ancient watches from the shadows.`
**Justificativa:** Evento com献祭 temática (offering/altar). Texto vazio perde a chance de atmosfera.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).

---

## Evento 66 — Mysterious Altar
**Chave:** `resources.assets:2545471`
**Título:** Mysterious Altar
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `An altar of unknown origin hums with faint energy. It seems to be waiting for a visitor.`
**Justificativa:** Altar misterioso sem texto é uma oportunidade perdida de lore e engajamento.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).
- Tamanho do evento é grande (5.040 chars) — indica múltiplas opções de recompensa.

---

## Evento 67 — Ghostly Warrior
**Chave:** `resources.assets:2545472`
**Título:** Ghostly Warrior
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `A spectral figure materializes before you — the ghost of a warrior, bound to this place.`
**Justificativa:** Fantasma de guerreiro sem texto não comunica a natureza sobrenatural do encounter.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).

---

## Evento 68 — Shrouded Figure
**Chave:** `resources.assets:2545473`
**Título:** Shrouded Figure
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `A figure cloaked in shadow turns toward you. Its eyes glow faintly in the darkness.`
**Justificativa:** Figura encoberta merece descrição para contextualizar a interação.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).

---

## Evento 69 — The Crimson Mage
**Chave:** `resources.assets:2545474`
**Título:** The Crimson Mage
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `A mage in crimson robes stands before you, murmuring incantations under her breath.`
**Justificativa:** Mago sem texto é uma oportunidade perdida de caracterização.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).
- Tamanho grande (4.570 chars) — indica opções múltiplas de recompensa/status.

---

## Evento 70 — The Forgotten Shrine
**Chave:** `resources.assets:2545475`
**Título:** The Forgotten Shrine
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `A crumbling shrine lies half-buried in dust and vines. Perhaps it holds something worth salvaging.`
**Justificativa:** Santuário esquecido sem texto não comunica risco ou recompensa potencial.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).
- Tamanho grande (4.810 chars) — múltiplas recompensas configuradas.

---

## Evento 71 — Cursed Relic
**Chave:** `resources.assets:2545476`
**Título:** Cursed Relic
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `An ancient relic pulses with dark energy — taking it could be dangerous, but powerful.`
**Justificativa:** Relíquia amaldiçoada sem texto não comunica o risco inerente.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).

---

## Evento 72 — Mysterious Ruins
**Chave:** `resources.assets:2545477`
**Título:** Mysterious Ruins
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `Stone pillars and carved walls mark the entrance to ancient ruins — something stirs within.`
**Justificativa:** Ruínas sem texto não dão ao jogador motivo para investigar.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).

---

## Evento 73 — Enchanted Pool
**Chave:** `resources.assets:2545478`
**Título:** Enchanted Pool
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `A pool of shimmering water glows faintly under the moonlight. It looks like it holds magical properties.`
**Justificativa:** Piscina encantada sem texto não sugere interação.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).
- Tamanho grande (4.756 chars via offset) — múltiplas recompensas.

---

## Evento 74 — Bandit Ambush
**Chave:** `resources.assets:2545479`
**Título:** Bandit Ambush
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `Shouts echo from the trees — bandits emerge from the shadows, weapons drawn!`
**Justificativa:** Emboscada sem texto não cria urgência narrativamente.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).

---

## Evento 75 — Merchant Camp
**Chave:** `resources.assets:2545480`
**Título:** Merchant Camp
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `A traveling merchant's camp lies ahead — tents flutter in the wind, and the scent of spices lingers.`
**Justificativa:** Acampamento de mercador sem texto não sugere oportunidade de comércio.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).
- Tamanho grande (3.996 chars via offset) — recompensas múltiplas.

---

## Evento 76 — Battle of Wits
**Chave:** `resources.assets:2545481`
**Título:** Battle of Wits
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `An opponent steps forward — not with steel, but with cunning. A test of intellect awaits.`
**Justificativa:** Batalha de intelecto sem texto não contextualiza o desafio.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).

---

## Evento 77 — Ogre Debt Collector
**Chave:** `resources.assets:2545652`
**Título:** Ogre Debt Collector
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `A hulking ogre blocks your path, cracking his knuckles. "You owe me, stranger. Time to pay up."`
**Justificativa:** Ogro cobrador sem texto perde completamente a oportunidade de humor e caráter. Nome "Ogre Debt Collector" já sugere narrativa — texto deveria acompanhar.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).
- `ForcedEnemies`: Ogre Debt Collector como SuperUnique (m_PathID=2545107).
- Encadeia: `resources.assets:2545716` — "Taste for Blood 1".

---

## Evento 78 — Ornate Coffin
**Chave:** `resources.assets:2545653`
**Título:** Ornate Coffin
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `An ornate coffin rests upright against the wall — the lid is slightly ajar. Something moves inside.`
**Justificativa:** Caixão ornamental sem texto é um dos maiores desperdícios narrativos do lote.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).
- Encadeia: `resources.assets:2545661` — "Party like a Pirate 1".

---

## Evento 79 — Party like a Pirate
**Chave:** `resources.assets:2545654`
**Título:** Party like a Pirate
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `A group of rowdy pirates raise their glasses to you. "Join the feast, friend — what say you?"`
**Justificativa:** Evento temático sem texto é uma oportunidade perdida de imersão.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).
- `status_candidatos`: "Weakened" (-20% Might, duração Quest) — penalidade de risco claro.
- Encadeia: `resources.assets:2545661` — "Party like a Pirate 1".

---

## Evento 80 — Skeletons in the Crypt
**Chave:** `resources.assets:2545655`
**Título:** Skeletons in the Crypt
**Categoria:** Normal
**Raridade:** Common (0)
**Peso relativo:** 1.0

### Veredito: MELHORAR (wording)

**Texto atual:** (string vazia no asset)
**PROPOSTA:** `Bones litter the crypt floor — the skeletons stir as you approach, drawn by the light.`
**Justificativa:** Cripta com esqueletos sem texto não comunica perigo iminente.

**Anomalias:**
- `texto_original`: string vazia.
- `recompensa_final`: NULL (NÃO_EXERCITADO).
- `status_candidatos`: "Slightly Petrified" (+8-200 Armor, -1 Movement) — trade-off claro de risco/recompensa.
- Opções: Investigate (combate com status de armadura) ou Leave (sem efeito).

---

# Inventário de Decisões — Lote Normal (eventos 61–80)

| # | Título | Chave | Raridade | Veredito | Natureza | Anomalia Principal |
|---|--------|-------|----------|----------|----------|-------------------|
| 61 | Horn of Glorious Battle | `resources.assets:2545466` | Common (0) | MELHORAR | wording | texto original vazio |
| 62 | Inconspicuous Burning Demon Skull | `resources.assets:2545467` | Common (0) | MELHORAR | wording | texto original vazio |
| 63 | Taste for Blood 1 | `resources.assets:2545650` | Common (0) | MELHORAR | wording | texto original vazio |
| 64 | Ornate Chest | `resources.assets:2545469` | Common (0) | MELHORAR | wording | texto original vazio |
| 65 | A Strange Offering | `resources.assets:2545470` | Common (0) | MELHORAR | wording | texto original vazio |
| 66 | Mysterious Altar | `resources.assets:2545471` | Common (0) | MELHORAR | wording | texto original vazio |
| 67 | Ghostly Warrior | `resources.assets:2545472` | Common (0) | MELHORAR | wording | texto original vazio |
| 68 | Shrouded Figure | `resources.assets:2545473` | Common (0) | MELHORAR | wording | texto original vazio |
| 69 | The Crimson Mage | `resources.assets:2545474` | Common (0) | MELHORAR | wording | texto original vazio |
| 70 | The Forgotten Shrine | `resources.assets:2545475` | Common (0) | MELHORAR | wording | texto original vazio |
| 71 | Cursed Relic | `resources.assets:2545476` | Common (0) | MELHORAR | wording | texto original vazio |
| 72 | Mysterious Ruins | `resources.assets:2545477` | Common (0) | MELHORAR | wording | texto original vazio |
| 73 | Enchanted Pool | `resources.assets:2545478` | Common (0) | MELHORAR | wording | texto original vazio |
| 74 | Bandit Ambush | `resources.assets:2545479` | Common (0) | MELHORAR | wording | texto original vazio |
| 75 | Merchant Camp | `resources.assets:2545480` | Common (0) | MELHORAR | wording | texto original vazio |
| 76 | Battle of Wits | `resources.assets:2545481` | Common (0) | MELHORAR | wording | texto original vazio |
| 77 | Ogre Debt Collector | `resources.assets:2545652` | Common (0) | MELHORAR | wording | texto original vazio; SuperUnique ogro |
| 78 | Ornate Coffin | `resources.assets:2545653` | Common (0) | MELHORAR | wording | texto original vazio |
| 79 | Party like a Pirate | `resources.assets:2545654` | Common (0) | MELHORAR | wording | texto original vazio; Weakened status |
| 80 | Skeletons in the Crypt | `resources.assets:2545655` | Common (0) | MELHORAR | wording | texto original vazio; Slightly Petrified |

**Resumo do lote:**
- **Total analisado: 20 de 20**
- **MELHORAR: 20** (todos wording)
- **MANTER: 0**
- **Anomalia dominante: texto_original string vazia em todos os 20 eventos**
- **Nenhum evento com `disabled: 1`**
- **Nenhum evento com opção oculta sem requisito**
- **NULL em recompensa_final: 20/20 (NÃO_EXERCITADO — runtime)**
- **Eventos encadeados:** ev63→"Taste for Blood 1", ev77→"Taste for Blood 1", ev78→"Party like a Pirate 1", ev79→"Party like a Pirate 1"
- **SuperUnique:** ev77 (Ogre Debt Collector)
- **Status aplicáveis:** ev79 (Weakened), ev80 (Slightly Petrified)

---
**Fim do lote EV-R2-NORMAL-b04-parte01.md.**
