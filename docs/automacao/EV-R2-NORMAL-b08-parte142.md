# Análise de Eventos — Lote Normal (141–160)

Lote EV-R2-NORMAL-b08 — Parte 142 (segundo bloco: eventos 146–150)

**Contagem:** Analisei 10 de 20 eventos do lote Normal v2, b08.

---

## Evento 146 — Treasure Chest
- **Chave:** `resources.assets:2545754` — GUID: `c56088e3-a42c-4a7d-8fba-7f8d67f71468`
- **Categoria:** Normal — raridade: **Uncommon (1)** — peso relativo: 1.0
- **Origem:** `events/treasure chest`
- **disabled:** 0

### Texto original
> A massive ornate chest gleams in front of you.

### Resultados possíveis (texto autoral)
(string vazia no asset)

### Opções
| # | Título | Texto da opção |
|---|--------|----------------|
| 1 | Open | Open the chest. |

### Efeitos
| # | Resultado | Texto | Efeito |
|---|-----------|-------|--------|
| 1 | Success (RollLimit 0) | (string vazia) | Nenhuma mudança de HP/mana/ouro |
| 2 | Failure (RollLimit 0) | Mimic! A grotesque, gaping maw reveals itself. Not a chest, but a Mimic. | Dano ao party, combat start vs Mimic |

### Condições
- `allowedNodeTypes: [3]`
- `minLevel: 3`
- `allowedTerrainTypes: [7, 0, 2]`
- `LeadsToFortune: 0`

### Veredito: MELHORAR — wording
**Problema:** Evento com 2 resultados (success/failure) mas o texto original é genérico e o texto de falha (Mimic) é apenas nos efeitos. O jogador não tem indício de armadilha.

**Proposta — Texto original:**
```
"A massive ornate chest gleams in front of you, its surface marked with faint scratches as if something has tried to break in from the inside."
```

**Proposta — Texto da Opção 1:**
```
"Open the chest with caution."
```

**Proposta — Resultado possível:**
```
"Open the chest — treasure or trap."
```

**Justificativa:** O Mimic é um trope clássico de RPG — adicionar pistas no texto do asset aumenta a imersão e prepara o jogador para a possibilidade de armadilha.

---

## Evento 147 — Treasure Chest
- **Chave:** `resources.assets:2545755` — GUID: `2f299791-cd08-44b0-bf28-a4079a82b841`
- **Categoria:** Normal — raridade: **Common (0)** — peso relativo: 1.0
- **Origem:** `events/treasure chest`
- **disabled:** 0

### Texto original
> A massive ornate chest gleams in front of you.

### Resultados possíveis (texto autoral)
(string vazia no asset)

### Opções
| # | Título | Texto da opção |
|---|--------|----------------|
| 1 | Open | Open the chest. |

### Efeitos
| # | Resultado | Texto | Efeito |
|---|-----------|-------|--------|
| 1 | Success (RollLimit 0) | (string vazia) | Ouro: +15–33; Mana: +10–30 |

### Condições
- `allowedNodeTypes: [3]`
- `minLevel: 3`
- `allowedTerrainTypes: [8, 7, 6, 1, 2, 0]`
- `LeadsToFortune: 0`

### Veredito: MELHORAR — wording
**Problema:** Mesmo problema do evento 146 — texto genérico, sem texto nos resultados. Mas neste caso é um loot puro (ouro + mana), sem armadilha.

**Proposta — Texto original:**
```
"A large ornate chest sits in your path, its lid slightly ajar. It looks sturdy, if well-used."
```

**Proposta — Texto da Opção 1:**
```
"Open the chest."
```

**Proposta — Resultado possível:**
```
"Open the chest — a cache of gold and mana."
```

**Justificativa:** Para um evento de loot comum, o texto não precisa ser longo. "Lid slightly ajar" sugere que alguém já tentou abrir — sem ser armadilha.

---

## Evento 148 — Treasure Goblin Den
- **Chave:** `resources.assets:2545757` — GUID: `8a1f25eb-680d-458e-a1c6-a288a86c6cdc`
- **Categoria:** Normal — raridade: **Common (0)** — peso relativo: 0.066 (muito raro)
- **Origem:** `events/treasure goblin den`
- **disabled:** 0

### Texto original
> (string vazia no asset)

### Resultados possíveis (texto autoral)
> (string vazia no asset)

### Opções
| # | Título | Texto da opção | Efeito |
|---|--------|----------------|--------|
| 1 | Open | (string vazia no asset) | Ouro: +5–12, Mana: +3–11 (distribuição: 80/20) |

### Condições
- `allowedNodeTypes: [3]`
- `minLevel: 3`
- `allowedTerrainTypes: [8, 7, 6, 1, 2, 0]`
- `LeadsToFortune: 0`

### Veredito: MELHORAR — texto ausente
**Problema:** **TODOS os campos de texto estão vazios** — texto original, resultados possíveis, texto da opção. É o evento mais raro do lote (peso 0.066) mas sem conteúdo narrativo.

**Proposta — Texto original:**
```
"You stumble upon a hidden cave filled with glittering gold coins and scattered gems. A treasure goblin's lair — the creature was likely just passing through."
```

**Proposta — Texto da Opção 1:**
```
"Raid the treasure goblin's den."
```

**Proposta — Resultado possível:**
```
"Claim the goblin's hidden cache."
```

**Justificativa:** Com peso relativo 0.066, este evento aparece raramente. Merece um texto que justifique sua raridade — o goblin "apenas passou por aqui". A proposta conecta o loot com a lore do jogo.

---

## Evento 149 — Treasure Hoard
- **Chave:** `resources.assets:2545758` — GUID: `fa55726b-edc2-4e35-b044-13bec3f0c4bc`
- **Categoria:** Normal — raridade: **Common (0)** — peso relativo: 1.0
- **Origem:** `events/treasure hoard`
- **disabled:** 0

### Texto original
> (string vazia no asset)

### Resultados possíveis (texto autoral)
> (string vazia no asset)

### Opções
| # | Título | Texto da opção | Efeito |
|---|--------|----------------|--------|
| 1 | Open | (string vazia no asset) | Ouro: +16–50; Mana: +5–16 (distribuição: 80/20) |

### Condições
- `allowedNodeTypes: [3]`
- `minLevel: 3`
- `allowedTerrainTypes: [7, 0, 1, 2, 0]`
- `LeadsToFortune: 0`

### Veredito: MELHORAR — texto ausente
**Problema:** Mesmo evento 148 — todos os campos de texto vazios. Diferença mecânica: loot maior (ouro 16–50 vs 5–12).

**Proposta — Texto original:**
```
"The air smells of old gold and damp stone. Before you lies a hoard fit for a dragon — stacks of coins, jeweled goblets, and enchanted trinkets piled high against the cavern wall."
```

**Proposta — Texto da Opção 1:**
```
"Take the treasure hoard."
```

**Proposta — Resultado possível:**
```
"Claim the ancient treasure hoard."
```

**Justificativa:** "Hoards" sugerem algo maior que um simples baú. A proposta conecta com a temática de "dragon's hoard" — um tesouro antigo acumulado.

---

## Evento 150 — Treasure Hunter
- **Chave:** `resources.assets:2545759` — GUID: `252cb65e-0e91-4d55-bf03-2a05cffa9d3c`
- **Categoria:** Normal — raridade: **Common (0)** — peso relativo: 1.0
- **Origem:** `events/treasure hunter`
- **disabled:** 0

### Texto original
> Your path crosses with another adventurer, a treasure hunter of sorts. He is an older man, his eyes gleaming with an avid curiosity that belies his age, hunched over what seems to be a collection of parchment and maps spread out on a makeshift wooden table.
>
> "Hero!" he greets, his voice coarse but spirited. "You appear just in time. I am on the verge of a great discovery. The Treasure of Moltendunn, the spoils of a legendary kingdom, lost for countless generations. This map," he points at the worn parchment, "may just hold the key."

### Resultados possíveis (texto autoral)
> Help him decipher the map.

### Opções
| # | Título | Texto da opção |
|---|--------|----------------|
| 1 | Help | "You'd better be able to read that thing." |

### Efeitos
| # | Resultado | Texto | Efeito |
|---|-----------|-------|--------|
| 1 | Success (RollLimit 8) | "Intrigued, you hunch over the map... Your finger traces a hidden path leading to a point yet unexplored. 'Here!' you exclaim..." | Ouro: +21–66; Mana: +8–24 (80/20) |
| 2 | Failure (RollLimit 0) | "The old treasure hunter's face falls... 'Ah well, it was worth a try. Some puzzles require more time to unravel.'" | Sem efeito |

### Condições
- `allowedNodeTypes: [0]`
- `minLevel: 5`
- `allowedTerrainTypes: [7, 0, 1, 2]`
- `LeadsToFortune: 0`

### Veredito: MELHORAR — wording da Opção 1
**Problema:** A opção "Help" tem o texto "You'd better be able to read that thing." — tom sarcástico/suspeito que conflita com o texto original, onde o treasure hunter é entusiástico e amigável ("Hero!", "voice coarse but spirited").

**Proposta — Texto da Opção 1:**
```
"Help him decipher the map."
```

**Proposta — Resultado possível:**
```
"Help decipher the map — or fail to find the treasure's location."
```

**Justificativa:** O texto original estabelece o treasure hunter como um NPC simpático e entusiástico. A opção sarcástica quebra a imersão. Uma opção neutra/positiva alinha com o tom.

---

[continua no próximo arquivo: parte 143 — eventos 151–155]
