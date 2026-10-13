# Análise de Eventos — Lote Normal (141–160)

Lote EV-R2-NORMAL-b08 — Parte 141 (primeiro bloco: eventos 141–145)

**Contagem:** Analisei 5 de 20 eventos do lote Normal v2, b08.

---

## Evento 141 — The Spell Council
- **Chave:** `resources.assets:2545748` — GUID: `c4c61a86-8016-45fd-ba38-418f361b24cc`
- **Categoria:** Normal — raridade: Common (0) — peso relativo: 1.0
- **Origem:** `events/the spell council returns`
- **disabled:** 0

### Texto original
> The <blue><b><incr>Spell Council</incr></b></blue> has returned in force, aware that you allowed the Mad Mage to remain free. Powerful elemental magic crackles around them as they prepare for battle. "So, you have chosen oblivion."

### Resultados possíveis (texto autoral)
(string vazia no asset)

### Opções
| # | Título | Texto da opção | Ação — Success |
|---|--------|----------------|----------------|
| 1 | Fight | "Whose oblivion will be determined." | (string vazia no asset) — combate contra o Spell Council |

### Condições
- `allowedNodeTypes: [7]` (nó de combate)
- `requiredStatusesToSpawn`: `[2545520]` — exige status prévio
- `LeadsToFortune: 1`
- Modos: Campaign + Roguelike

### Veredito: MELHORAR — wording
**Problema:** Texto da opção "Fight" ("Whose oblivion will be determined.") é ambíguo e pouco imersivo. Não conecta com o texto original do evento. O "Resultado possível" está vazio — deveria descrever o desfecho do confronto.

**Proposta — Texto da Opção 1:**
```
"Face the Spell Council."
```

**Proposta — Resultado possível:**
```
"Defeat the council or be consumed by their elemental fury."
```

**Justificativa:** O evento tem narrativa forte (retorno do Spell Council, menção ao Mad Mage) mas a opção de combate não reflete o tom. A proposta mantém a brevidade de um evento de combate, mas dá contexto.

---

## Evento 142 — Torn Portrait
- **Chave:** `resources.assets:2545750` — GUID: `3d676a9b-bdd4-48ba-9893-37e3f8d9031b`
- **Categoria:** Normal — raridade: Common (0) — peso relativo: 1.0
- **Origem:** `events/torn portrait`
- **disabled:** 1

### Texto original
> The yearning ghost extends her hand pleading for help.

### Resultados possíveis (texto autoral)
(string vazia no asset)

### Opções
| # | Título | Texto da opção | Ação — Success |
|---|--------|----------------|----------------|
| 1 | Reach | "You reach out to the ghost. Gain [o1a1_status]." | "You reach out, but your hand passes through cold air. Memories flood your mind and longing fills your heart. You gain [o1a1_status]." |

### Condições
- `disabled: 1` — evento desativado
- `LeadsToFortune: 1`
- `allowedNodeTypes: [7]`

### Veredito: MANTER (com observação)
**Problema:** `disabled: 1` — evento desativado. O texto é mínimo (1 linha). O evento 157 (Wooden Coffin) tem texto idêntico ("The yearning ghost extends her hand pleading for help.") — possível duplicação de asset entre eventos.

**Observação:** O `disabled: 1` é intencional? O evento funciona mas tem texto curto demais para um evento de escolha. Recomendo reavaliar se o `disabled` é por erro de conteúdo ou intenção de remover.

**Nota de duplicação:** O evento 157 (Wooden Coffin) repete o mesmo texto e opções. Verificar se não houve cópia acidental de asset.

---

## Evento 143 — Tornado!
- **Chave:** `resources.assets:2545751` — GUID: `cebeebab-3728-45fa-aab6-cdab1f351041`
- **Categoria:** Normal — raridade: Common (0) — peso relativo: 1.0
- **Origem:** `events/tornado!`
- **disabled:** 0

### Texto original
> A <blue><b><incr>Tornado</incr></b></blue>, a monstrous titan of air and fury, touches down with a ferocity that makes the very earth beneath you shudder. It is a terrifying spectacle, an embodiment of nature's raw, uncontrollable power.
>
> The world becomes a maelic whirlwind of chaos. The tornado's winds howl like banshees, pulling at you with the inexorable force of a monstrous vortex. Debris spins in a deadly dance around the twister's base, and you know you have but moments to react.

### Resultados possíveis (texto autoral)
> You have only a moment to react!

### Opções
| # | Título | Texto da opção |
|---|--------|----------------|
| 1 | React | "Grab onto whatever you can and hold on tight." |

### Condições
- `allowedTerrainTypes: [8, 7, 6, 1, 2, 0]` — praticamente todos os terrenos (8 = Tundra, 7 = Desert, 6 = Snow, etc.)
- `LeadsToFortune: 0`

### Veredito: MELHORAR — wording
**Problema:** O evento é um combate contra um tornado mas só tem 1 opção ("React"). Sem falha possível — `RollLimit: 10` mas sem opção de Failure separada. O nome "Tornado!" com ponto de exclamação é inconsistente com a convenção de nomenclatura de outros eventos.

**Proposta — Título:**
```
"Tornado"  (remover ponto de exclamação)
```

**Proposta — Opção 2:**
```
Dodging — "You try to outrun the storm's path."
```
Com um `RollLimit` menor e efeito de dano ao party (`alvo.override: Party`) em caso de falha.

**Justificativa:** Eventos de combate com apenas 1 opção e sem falha são menos interativos. Adicionar uma segunda opção com risco de falha aumenta o engajamento. A convenção do jogo usa títulos sem pontuação exclamativa.

---

## Evento 144 — Transcendence
- **Chave:** `resources.assets:2545752` — GUID: `1a9b1d33-3893-4c82-8093-6f4f234d13a5`
- **Categoria:** Normal — raridade: Common (0) — peso relativo: 1.0
- **Origem:** `events/transcendence`
- **disabled:** 0

### Texto original
> Underneath a majestic cherry blossom tree, an old man stands, wreathed in a shower of falling blossoms. His eyes are closed, his face calm and peaceful, reflecting an inner tranquility that seems to permeate the very air around him.
>
> [Texto longo — ~15 parágrafos de diálogo e descrição]
>
> "Rest here, warrior. Set aside your worldly concerns. In the silence of the heart, free from the clamor of material pursuits, you will find your true purpose."

### Resultados possíveis (texto autoral)
(string vazia no asset)

### Opções
| # | Título | Texto da opção | Efeito |
|---|--------|----------------|--------|
| 1 | Meditate | "You calm your mind seeking wisdom." | Gain status "Transcendence" — Reduces Max Health by 50–65%, grants 4 charges per battle. Duração: Permanent. Tipo: Fortune. |
| 2 | Leave | "You quite like your earthly possessions. You leave unable to give up the world." | Sem efeito |

### Condições
- `allowedTerrainTypes: [7]` (Desert apenas)
- `minLevel: 3`
- `allowAtAllLevels: 0`
- `LeadsToFortune: 1`

### Veredito: MELHORAR — wording da Opção 1
**Problema:** A recompensa do status "Transcendence" é extremamente punitiva: reduz Max Health em 50–65%. O texto do evento é poético e inspirador ("find your true purpose"), mas a recompensa é quase uma penalidade disfarçada. Isso cria dissonância entre narrativa e mecânica.

**Proposta — Texto da Opção 1:**
```
"Meditate" — "You calm your mind seeking wisdom."
```
*(mantido — já está adequado)*

**Proposta — Resultado possível:**
```
"Gain inner peace... but at a cost."
```

**Justificativa:** Manter a narrativa intacta, mas tornar a consequência mais evidente no texto descritivo. O jogador deve ser informado de que a sabedoria tem um preço antes de aceitar. Alternativamente, revisar o efeito do status — considere reduzir a penalidade ou tornar o efeito mais equilibrado (ex: bônus de dano em troca de -25% HP).

**Nota de balanceamento:** Um status permanente que reduz 50–65% do Max Health é quase sempre uma penalidade. Se é intencional como "trade-off", o texto deveria avisar claramente. Se é erro, ajustar `expressao: "{.5,.65}"` para um valor positivo.

---

## Evento 145 — Treasure Chest
- **Chave:** `resources.assets:2545753` — GUID: `5f13a738-5671-4b7b-8982-706fd39a742e`
- **Categoria:** Normal — raridade: **Mythic (4)** — peso relativo: 1.0
- **Origem:** `events/treasure chest - roguelike`
- **disabled:** 0

### Texto original
> A massive ornate chest gleams in front of you.

### Resultados possíveis (texto autoral)
(string vazia no asset)

### Opções
| # | Título | Texto da opção |
|---|--------|----------------|
| 1 | Open | (string vazia no asset) |

### Condições
- `allowedNodeTypes: [3]` (nó de tesouro)
- `modos: [Roguelike]` — apenas Roguelike
- `historia: Both`
- `minLevel: 4`
- `allowAtAllLevels: 0`
- `LeadsToFortune: 0`

### Veredito: MELHORAR — wording
**Problema:** Texto do evento é genérico ("A massive ornate chest gleams in front of you."). A opção "Open" não tem texto descritivo. Eventos Mythic merecem mais cuidado.

**Proposta — Texto original:**
```
"A massive ornate chest gleams before you, its surface etched with ancient runes that pulse with faint golden light."
```

**Proposta — Texto da Opção 1:**
```
"Open the chest carefully."
```

**Proposta — Resultado possível:**
```
"Open the chest — fortune or trap awaits."
```

**Justificativa:** Adicionar detalhes visuais (runas, brilho) reforça a raridade Mythic. O texto da opção deve incentivar a cautela — coerente com a mecânica de loot do Roguelike.

---

[continua no próximo arquivo: parte 142 — eventos 146–150]
