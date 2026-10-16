# Análise de Eventos — Lote Normal (141–160)

Lote EV-R2-NORMAL-b08 — Parte 144 (quarto bloco: eventos 156–160)

**Contagem:** Analisei 20 de 20 eventos do lote Normal v2, b08.

---

## Evento 156 — Witch's Pyre
- **Chave:** `resources.assets:2545776` — GUID: `25028950-77c6-46ed-ba01-36f25d817793`
- **Categoria:** Normal — raridade: **Common (0)** — peso relativo: 1.0
- **Origem:** `events/witch's pyre`
- **disabled:** 0

### Texto original
> A smoldering pyre blazes amidst the damp moss and hanging vines of the swamp, its feral light casting long, twisted shadows across the gloom. The sight is as fascinating as it is harrowing.
>
> The fire dances and writhes, a serpent set ablaze, consuming all that is offered to it. All, save for the spectral figure at its heart. The witch, it seems, is not affected by the flames. She is as still as stone, a chilling silhouette amidst the raging inferno.
>
> Your gaze locks with the witch's, and you find yourself entrapped by her stare. Her eyes, gleaming coals in the firelight, seem to bore into your very soul.
>
> Was it your imagination, or has she been staring at you all along?

### Resultados possíveis (texto autoral)
> What will you do?

### Opções
| # | Título | Texto da opção | Efeito |
|---|--------|----------------|--------|
| 1 | Stay | "Watch as the Pyre burns low." | "You stay rooted on the spot, watching the pyre burn low, the witch's image fading with the dying embers. The blaze offers no warmth... Glistening in the firelight on your palm is not the clear liquid of sweat, but the deep, haunting crimson of blood." |
| 2 | Run | "You've lost your nerve." | "Doubts and fear swirl within you, overwhelming your senses until your legs move on their own accord. You are fleeing. Fleeing from the horrifying spectacle, the witch's laughter ringing in your ears." |

### Condições
- `allowedNodeTypes: [7]` (combate)
- `minLevel: 3`
- `allowedTerrainTypes: [1]` (Swamp)
- `LeadsToFortune: 0`
- `allowOnAllTimeOfDay: 1`

### Veredito: MELHORAR — wording
**Problema 1:** O evento é atmosférico e bem escrito (3 parágrafos de descrição), mas as opções são curtas demais ("Stay" e "Run"). O texto narrativo é rico, mas as opções não aproveitam o tom sombrio.

**Problema 2:** Ambos os resultados são "Sucesso" (RollLimit 0) — sem risco de falha. Isso é aceitável para um evento de escolha narrativa, mas o texto da opção "Run" ("You've lost your nerve") tem tom negativo que conflita com o tom do evento (a fuga é uma escolha legítima, não fraqueza).

**Proposta — Texto da Opção 1:**
```
"Stay" — "Watch the pyre burn low and witness the witch's fate."
```

**Proposta — Texto da Opção 2:**
```
"Flee" — "The witch's gaze is too much. Turn and run."
```

**Justificativa:** "Run" é um comando; "Flee" é mais evocativo. O texto de "Stay" deve sugerir que há algo a ser visto (o destino da bruxa). O texto de "Flee" remove a conotação negativa de "lost your nerve".

---

## Evento 157 — Wooden Coffin
- **Chave:** `resources.assets:2545777` — GUID: `b2a823dc-b6c0-48e4-934a-ab7f9a8034ed`
- **Categoria:** Normal — raridade: **Common (0)** — peso relativo: 1.0
- **Origem:** `events/wooden coffin`
- **disabled:** 1

### Texto original
> The yearning ghost extends her hand pleading for help.

### Resultados possíveis (texto autoral)
> (string vazia no asset)

### Opções
| # | Título | Texto da opção | Efeito |
|---|--------|----------------|--------|
| 1 | Reach | (string vazia no asset) | "You reach out, but your hand passes through cold air. Memories flood your mind and longing fills your heart. You gain [o1a1_status]." |
| 2 | Leave | (string vazia no asset) | "You leave, but the ghost's disappointment haunts your dreams." |

### Condições
- `allowedNodeTypes: [0]`
- `minLevel: 3`
- `allowedTerrainTypes: [8, 7, 6, 1, 2, 0]`
- `LeadsToFortune: 1`

### Veredito: MELHORAR — texto ausente
**Problema 1:** Texto original é mínimo (1 linha) — idêntico ao evento 142 (Torn Portrait). Duplicação de asset.

**Problema 2:** Opções "Reach" e "Leave" sem texto descritivo. O efeito é rico ("memories flood your mind"), mas o jogador não vê isso antes de escolher.

**Proposta — Texto original:**
```
"A wooden coffin lies half-buried in the earth. A translucent figure reaches out from within — a ghost, her expression one of desperate longing."
```

**Proposta — Texto da Opção 1:**
```
"Reach" — "Reach out to the spectral figure."
```

**Proposta — Texto da Opção 2:**
```
"Leave" — "Leave the ghost to her rest."
```

**Proposta — Resultado possível:**
```
"Reach into the coffin — or turn away from the ghost's plea."
```

**Justificativa:** O texto original precisa de contexto. O ghost "extending her hand" é evocativo mas sem cenário. A proposta coloca o jogador num contexto (caixão semi-enterrado) e dá um propósito às opções.

**Nota de duplicação:** O evento 142 (Torn Portrait) tem o MESMO texto original. Verificar se é duplicação acidental de asset ou se dois eventos diferentes deveriam ter textos distintos.

---

## Evento 158 — Wrath of the Righteous (Part 2)
- **Chave:** `resources.assets:2545778` — GUID: `5c2dd0f8-93c0-47f3-b621-0b8f0d42f50f`
- **Categoria:** Normal — raridade: **Common (0)** — peso relativo: 1.0
- **Origem:** `events/wrath of the righteous - part 2`
- **disabled:** 0

### Texto original
> Through the arched passageways and shadowed halls of this castle, you find yourself standing before a figure who appears to be hewn from radiance itself. A <gold><b><incr>Paladin</incr></b></gold>, clad in armor of brilliant light, that casts the dreary surroundings into stark relief. His presence is a beacon of hope in the midst of such an accursed place.
>
> "This kingdom," he begins, gesturing to the darkened tapestries and ominous statues lining the corridors, "was once a place of joy, a place where valor met prosperity and nobility met humility. But now..." His gaze falls, his expression sorrowful. The luminous light surrounding him seems to dim, the sadness is almost palpable. "Now, this castle is but a mockery of its past, its people cursed, its glory lost."
>
> [Texto longo — ~10 parágrafos]
>
> "At the heart of it all is <rainb><b><incr>The Jester</incr></b></rainb>, our former king transformed into a vile demon. He is the embodiment of the darkness that has seeped into the heart of our kingdom, the puppet master who pulls the strings of this grim performance."
>
> "Will you aid us, adventurer? Will you deliver us from the grip of this monstrous farce, and bring an end to our torment?"

### Resultados possíveis (texto autoral)
> (string vazia no asset)

### Opções
| # | Título | Texto da opção | Efeito |
|---|--------|----------------|--------|
| 1 | Accept | "Vow to vanquish this evil." | "The old paladin reaches forward, his armored hand heavy with years of servitude, and clasps you in a grip firm with gratitude and resolve. 'Let this end.'" |
| 2 | Decline | "Tis a noble quest, but you cannot accept it now." | "The paladin nods, the radiance around him dimming slightly. His face remains stoic, but there is a quiet sadness in his gaze that speaks volumes. 'I understand, wanderer... We all have our paths to follow, our obligations to meet.'" |

### Condições
- `allowedNodeTypes: [7]` (combate)
- `minLevel: 3`
- `allowedTerrainTypes: [4, 1, 3]`
- `LeadsToFortune: 1`
- `allowOnAllTimeOfDay: 1`

### Veredito: MANTER
**Problema:** Nenhum problema estrutural significativo. Texto original é extenso (~10 parágrafos), bem escrito, com narrativa forte (Paladin, The Jester como vilão). As duas opções (Accept/Decline) têm texto narrativo rico e coerente. Não há efeitos mecânicos — é puramente narrativo.

**Observação:** O evento 159 é uma variação com o mesmo NPC (Paladin) mas missões diferentes. Verificar se "The Lady of the Well" e "The Jester" são parte da mesma questline ou eventos independentes. Se são a mesma questline, garantir consistência nos nomes próprios.

---

## Evento 159 — Wrath of the Righteous
|- **Chave:** `resources.assets:2545779` — GUID: `78693713-6487-460a-bd29-2337c1eff6fa`
|- **Categoria:** Normal — raridade: **Common (0)** — peso relativo: 1.0
|- **Origem:** `events/wrath of the righteous`
|- **disabled:** 1 ⚠️

### Texto original
> A noble <gold><b><incr>Paladin<gold></b></incr> stands before you, wreathed in holy light.
>
> "Hold, travelers. This once glorious kingdom and it's citizens have been twisted into monstrous versions of themselves. Their foolish King allowed evil to take hold of his court."
>
> "I have spent my life seeking an end to it's corruption, to undo what this treacherous King has done, but there is one I cannot vanquish."
>
> "<violet><b><incr>The Lady of the Well</violet></b></incr> was once a princess fair and true. Now she is the very shadow of evil, terrorizing the forests at night."
>
> "Bring me her Shadow-drenched Heart, and we will bring an end to this evil for good."

### Resultados possíveis (texto autoral)
> Will you accept the Paladin's quest?

### Opções
| # | Título | Texto da opção | Efeito |
|---|--------|----------------|--------|
| 1 | Accept | "Vow to vanquish this evil." | "The paladin clasps your hand. 'Let this end.'" |
| 2 | Decline | "Tis' a noble quest, but you cannot accept it now." | "The paladin nods... 'I understand, wanderer.'" |

### Condições
|- `disabled: 1` ⚠️
|- `allowedNodeTypes: [7]`
|- `minLevel: 15` (nota: requer nível 15, não 3)
|- `allowedTerrainTypes: [3, 2]` (Forest + Swamp, não Desert)
|- `LeadsToFortune: 0` (nota: não leva a tesouro, diferente do evento 158)

### Veredito: MELHORAR + REVISAR disabled
**Problema 1:** `disabled: 1` — evento desativado. O texto é significativamente menor que o evento 158 (apenas 4 parágrafos vs ~10). Parece ser uma versão alternativa/early do mesmo NPC.

**Problema 2:** Erro de digitação: "it's corruption" e "it's citizens" (deveria ser "its" sem apóstrofo).

**Problema 3:** Tag de cor mal formada: `<gold><b><incr>Paladin<gold></b></incr>` — falta o `>` após `<gold>` no fechamento. Deveria ser `<gold><b><incr>Paladin</incr></b></gold>`.

**Proposta — Correção de tag:**
```
"<gold><b><incr>Paladin</incr></b></gold>"
```

**Proposta — Correção de gramática:**
```
"This once glorious kingdom and its citizens have been twisted..."
"undo what this treacherous King has done..." (ok — "it's" aqui está correto)
```

**Observação sobre disabled:** O evento 158 é mais detalhado e parece ser a versão preferida. O evento 159 (`disabled: 1`) tem a mesma temática (Paladin, reino amaldiçoado) mas missões diferentes. Verificar se o disabled é intencional (substituído pelo 158) ou um erro de configuração.

---

## Evento 160 — Yours or Mine
- **Chave:** `resources.assets:2545786` — GUID: `1ba0288d-5a22-4ead-b273-67bf8ae36a81`
- **Categoria:** Normal — raridade: **Common (0)** — peso relativo: 1.0
- **Origem:** `events/yours or mine`
- **disabled:** 1 ⚠️

### Texto original
> On approach, you find the enemy quite distracted. A thief's dream!

### Resultados possíveis (texto autoral)
> What will you do?

### Opções
| # | Título | Texto da opção |
|---|--------|----------------|
| 1 | Steal | "Covertly take as many valuables as you can." |
| 2 | Fight | "Straightforward battle is the best way to handle any situation." |

### Condições
- `disabled: 1` ⚠️
- `allowedNodeTypes: [0]`
- `minLevel: 3`
- `allowedTerrainTypes: []` (todos)
- `LeadsToFortune: 0`
- `allowOnAllTimeOfDay: 1`

### Veredito: MELHORAR + REVISAR disabled
**Problema 1:** `disabled: 1` — evento desativado. O texto é extremamente curto (1 linha). Não há informações sobre o inimigo nem sobre as consequências das escolhas.

**Problema 2:** O evento parece ser um combate contra um inimigo distraído, com opção de ataque surpresa (Steal) ou combate direto (Fight). Mas não há textos de resultado — apenas os títulos.

**Proposta — Texto original:**
```
"An enemy camp lies ahead, their guard asleep and their valuables scattered about. A thief's dream — or a warrior's opportunity."
```

**Proposta — Texto da Opção 1:**
```
"Steal" — "Sneak in and take as many valuables as you can before they wake."
```

**Proposta — Texto da Opção 2:**
```
"Fight" — "Charge in while they're distracted."
```

**Proposta — Resultado possível:**
```
"Strike while they're distracted — steal their riches or defeat them in combat."
```

**Justificativa:** O nome "Yours or Mine" sugere um confronto sobre propriedade. A proposta conecta o "thief's dream" do texto original com a mecânica de combate. Adicionar contexto sobre o inimigo (acampamento, guardas adormecidos) justifica as opções.

**Observação sobre disabled:** Verificar se o disabled é intencional (evento incompleto) ou se deve ser habilitado com texto revisado.

---

## Resumo do Lote (141–160)

| Evento | Nome | disabled | Texto original | Opções | Veredito |
|--------|------|----------|----------------|--------|----------|
| 141 | The Spell Council | 0 | Bom | 1 | MELHORAR wording |
| 142 | Torn Portrait | **1** | Mínimo (1 linha) | 1 | MANTER c/ obs (duplicação + disabled) |
| 143 | Tornado! | 0 | Bom | 1 | MELHORAR wording + estrutura |
| 144 | Transcendence | 0 | Excelente | 2 | MELHORAR wording + balanceamento |
| 145 | Treasure Chest | 0 (Mythic) | Genérico | 1 | MELHORAR wording |
| 146 | Treasure Chest | 0 (Uncommon) | Genérico | 2 | MELHORAR wording |
| 147 | Treasure Chest | 0 (Common) | Genérico | 1 | MELHORAR wording |
| 148 | Treasure Goblin Den | 0 (raro) | **VAZIO** | 1 | MELHORAR (texto ausente) |
| 149 | Treasure Hoard | 0 | **VAZIO** | 1 | MELHORAR (texto ausente) |
| 150 | Treasure Hunter | 0 | Bom | 2 | MELHORAR wording da opção |
| 151 | Unidentified Remains | 0 | Bom | 2 | MANTER |
| 152 | Weapon Chest | 0 (Uncommon) | **VAZIO** | 1 | MELHORAR (texto ausente) |
| 153 | Weapon Chest | 0 (Uncommon) | **VAZIO** | 1 | MANTER c/ obs (duplicação) |
| 154 | What Lurks | 0 | Bom | 2 | MELHORAR estrutura da opção |
| 155 | Witch's Cauldron | 0 | Excelente | 2 | MELHORAR naming das opções |
| 156 | Witch's Pyre | 0 | Excelente | 2 | MELHORAR wording |
| 157 | Wooden Coffin | **1** | Mínimo (1 linha) | 2 | MELHORAR OU REMOVER (disabled + texto ausente) |
| 158 | Wrath of the Righteous | 0 | Excelente | 2 | MANTER |
| 159 | Wrath of the Righteous | **1** | Médio (~5 parágrafos) | 2 | MELHORAR + REVISAR disabled |
| 160 | Yours or Mine | **1** | Curto (2 frases) | 2 | MELHORAR + REVISAR disabled |

### Padrões identificados
1. **Textos vazios:** 4 eventos (148, 149, 152, 153) com TODOS os campos de texto vazios. Prioridade alta.
2. **Textos mínimos (1 linha):** 3 eventos (142, 157, 160) com texto original de apenas uma frase.
3. **Duplicação de asset:** Eventos 142/157 compartilham o mesmo texto original ("The yearning ghost extends her hand pleading for help."). Evento 152/153 compartilham o mesmo efeito de status.
4. **Eventos disabled:** 4 eventos (142, 157, 159, 160) com `disabled: 1`. Verificar se é intencional.
5. **Mythic sem destaque:** Evento 145 é o único Mythic do lote mas tem texto genérico.
6. **Tags HTML malformadas:** Evento 159 tem `<gold><b><incr>Paladin<gold></b></incr>` (tag aberta sem fechar).
7. **Erro gramatical:** Evento 159 tem "it's corruption" (deveria ser "its").

### Prioridades de ação
1. **Alta:** Textos vazios (148, 149, 152, 153) — sem texto, o jogador não tem contexto.
2. **Média:** Duplicações (142/157, 152/153) e eventos disabled (142, 157, 159, 160) — requer verificação de intenção.
3. **Baixa:** Wording de eventos existentes — melhorias cosméticas e de consistência.

---

[continua no próximo arquivo: parte 145 — próximos blocos de eventos]
