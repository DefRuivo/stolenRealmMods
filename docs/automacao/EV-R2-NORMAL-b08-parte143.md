# Análise de Eventos — Lote Normal (141–160)

Lote EV-R2-NORMAL-b08 — Parte 143 (terceiro bloco: eventos 151–155)

**Contagem:** Analisei 15 de 20 eventos do lote Normal v2, b08.

---

## Evento 151 — Unidentified Remains
- **Chave:** `resources.assets:2545767` — GUID: `61dc097d-ac3d-4a63-a07e-725900b48d3f`
- **Categoria:** Normal — raridade: **Common (0)** — peso relativo: 1.0
- **Origem:** `events/unidentified remains`
- **disabled:** 0

### Texto original
> Skeletal remains, unceremoniously scattered, speak of a fate long forgotten. The bones are dry and brittle, tattered fragments of clothing still clinging to them. The skull, half-buried in the sand, stares blankly, an empty testimony of an unknown life cut short.

### Resultados possíveis (texto autoral)
> What will you do?

### Opções
| # | Título | Texto da opção |
|---|--------|----------------|
| 1 | Search | "You kneel and search the remains." |

### Efeitos
| # | Resultado | Texto | Efeito |
|---|-----------|-------|--------|
| 1 | Success (RollLimit 10) | "As you sift through the soil, your fingertips brush against something metallic..." | Ouro: +25–78 (100%); Mana: +8–25 (100%) |
| 2 | Failure (RollLimit 0) | "Your search yields nothing. It appears that this unfortunate soul has been laid to rest devoid of any possessions or artifacts. It is a sobering reminder of the harsh realities of life." | Sem efeito |

### Condições
- `allowedNodeTypes: [0]`
- `minLevel: 3`
- `allowedTerrainTypes: [7, 0, 1, 2]`
- `LeadsToFortune: 0`

### Veredito: MANTER
**Problema:** Nenhum problema estrutural significativo. Texto original é bem escrito (3 parágrafos, narrativa forte). Opção de sucesso/falha bem balanceada (RollLimit 10 para sucesso, 0 para falha — falha automática se não rolar). Texto de falha é melancólico e coerente com o tema.

**Observação:** O RollLimit 10 é alto, garantindo sucesso na maioria dos casos. Se for intencional (loot confiável), está adequado. Se quiser mais risco, reduzir para RollLimit 5.

---

## Evento 152 — Weapon Chest
- **Chave:** `resources.assets:2545770` — GUID: `5a1f026d-cc6c-44c4-8552-2dd3e605bf66`
- **Categoria:** Normal — raridade: **Uncommon (1)** — peso relativo: 1.0
- **Origem:** `events/weapon chest - roguelike`
- **disabled:** 0

### Texto original
> (string vazia no asset)

### Resultados possíveis (texto autoral)
> (string vazia no asset)

### Opções
| # | Título | Texto da opção | Efeito |
|---|--------|----------------|--------|
| 1 | Open | (string vazia no asset) | Status "Weapon Chest" — Chance de 50%: dano de arma +50% por 5 turnos |

### Condições
- `allowedNodeTypes: [3]`
- `minLevel: 3`
- `allowedTerrainTypes: [8, 7, 6, 1, 2, 0]`
- `LeadsToFortune: 0`
- `modos: [Roguelike]`

### Veredito: MELHORAR — texto ausente
**Problema:** Todos os campos de texto vazios. Evento de loot de status (bônus de dano) sem contexto narrativo.

**Proposta — Texto original:**
```
"An old weapon chest sits in the dust, its lid cracked open. Inside, a gleaming blade catches your eye — clearly forged with care."
```

**Proposta — Texto da Opção 1:**
```
"Take the enchanted weapon."
```

**Proposta — Resultado possível:**
```
"Claim a magical weapon from the chest."
```

**Justificativa:** Um weapon chest deve evocar a imagem de uma arma mágica. A proposta conecta o loot (bônus de dano) com a narrativa.

---

## Evento 153 — Weapon Chest
- **Chave:** `resources.assets:2545771` — GUID: `168a9bb6-ae30-4104-b523-2e401721d680`
- **Categoria:** Normal — raridade: **Uncommon (1)** — peso relativo: 1.0
- **Origem:** `events/weapon chest`
- **disabled:** 0

### Texto original
> (string vazia no asset)

### Resultados possíveis (texto autoral)
> (string vazia no asset)

### Opções
| # | Título | Texto da opção | Efeito |
|---|--------|----------------|--------|
| 1 | Open | (string vazia no asset) | Status "Weapon Chest" — Chance de 50%: dano de arma +50% por 5 turnos |

### Condições
- `allowedNodeTypes: [3]`
- `minLevel: 3`
- `allowedTerrainTypes: [7, 0, 2]`
- `LeadsToFortune: 0`

### Veredito: MANTER COM OBSERVAÇÃO
**Problema:** Mesmo efeito do evento 152 (mesmo status, mesmo bônus). Possível duplicação de asset. O evento 152 é exclusivo do Roguelike; este parece ser de campaign.

**Observação:** Verificar se os dois efeitos de status são realmente idênticos. Se sim, considerar unificar em um único asset reutilizado. Se diferentes, o texto deve refletir essa diferença.

---

## Evento 154 — What Lurks
- **Chave:** `resources.assets:2545773` — GUID: `d9869d80-80e1-47e3-b3bc-0e85cd0dab64`
- **Categoria:** Normal — raridade: **Common (0)** — peso relativo: 1.0
- **Origem:** `events/what lurks`
- **disabled:** 0

### Texto original
> In the parched, wind-swept land of Wyrmrest Desert, a great monstrosity mars the horizon. The grotesque corpse of a colossal ogre, every inch of its leathery hide etched with deep, bloody gashes. Even from a distance, the stench of death washes over you, a fetid miasma that permeates the air, replacing the usual dry desert scent with a noxious, gut-churning odor.

### Resultados possíveis (texto autoral)
> (string vazia no asset)

### Opções
| # | Título | Texto da opção | Efeito |
|---|--------|----------------|--------|
| 1 | Investigate | "Give in to your curiosity and examine the Ogre closer." | Success: "Suddenly, a movement catches your eye. The ogre's enormous form jerks, then begins sinking into the sand. A giant, armored claw reaches up from the earth, pulling the lifeless bulk down with alarming strength... An armored behemoth erupts from the sand..." |
| 2 | Flee | "You've lost your nerve." | Success: "Without another glance at the deceased ogre, you turn and run, each stride kicking up small clouds of desert sand." |

### Condições
- `allowedNodeTypes: [7]` (combate)
- `minLevel: 3`
- `allowedTerrainTypes: [1]` (Swamp)
- `LeadsToFortune: 0`
- `allowOnAllTimeOfDay: 1`

### Veredito: MELHORAR — wording + estrutura
**Problema 1:** "Investigate" é sucesso (RollLimit 0 = combate inevitável). "Flee" também é sucesso (RollLimit 0 = fuga garantida). Não há falha — o jogador decide se quer lutar ou fugir, ambos com 100% de sucesso. Isso é aceitável, mas a opção "Flee" deveria ter um RollLimit baixo para permitir fuga falha (combate obrigatório).

**Problema 2:** Texto do resultado de "Flee" usa "You've lost your nerve" como título mas o texto narrativo é neutro.

**Proposta — Texto da Opção 2:**
```
"Flee" — "You've lost your nerve. Try to slip away unnoticed."
```

**Proposta — Efeito de Flee:**
```
"Success (RollLimit 2): You manage to escape. (90% chance)"
"Failure (RollLimit 0): The behemoth spots you! Combat ensues."
```

**Justificativa:** Eventos de combate com opção de fuga são mais interessantes quando a fuga é incerta. Um RollLimit baixo (2) permite que a maioria escape, mas há risco — coerente com a tensão narrativa do evento.

---

## Evento 155 — Witch's Cauldron
- **Chave:** `resources.assets:2545774` — GUID: `25e5d830-d905-49f6-8141-49be866c6056`
- **Categoria:** Normal — raridade: **Common (0)** — peso relativo: 1.0
- **Origem:** `events/witch's cauldron`
- **disabled:** 0

### Texto original
> In the heart of the Sunken Swamp, you find a small clearing where an <green><b><incr>Ancient Hag</incr></b></green> squats, her skeletal figure hunched over a bubbling cauldron. The container hisses and sputters, spewing a sickly green concoction that spatters onto the surrounding soil, instantly shriveling any plant life it touches.
>
> The putrid odor is nearly unbearable. It permeates the air, a malodorous blend of swamp water, rot, and something undefinably sour. As the smell reaches you, a wave of revulsion washes over you, your stomach lurches in protest. You can taste the bile rising in your throat.
>
> You try to turn away but you cannot. Your hand, seemingly of its own volition, stretches out towards the cauldron. You try to pull back, to wrench your hand away from the vile brew, but it moves as if bewitched, resisting your will. Your fingers skim the surface of the seething liquid, scooping up a handful. You watch in wide-eyed horror as your possessed hands bring the potion to your lips.
>
> The hag cackles in delight, her voice a rasping echo that bounces off the gnarled tree trunks. Her eyes, two pinpricks of cruel light in her wrinkled visage, gleam with mirth and malice.

### Resultados possíveis (texto autoral)
> (string vazia no asset)

### Opções
| # | Título | Texto da opção | Efeito |
|---|--------|----------------|--------|
| 1 | Resist | "Fight against the witch's enchantment." | Success (RollLimit 12): "You kick over the cauldron. The foul mixture sizzles... the hag is gone. You stagger back, gasping... relief washes over you." Efeito: Dano ao party (50% chance), dano de 2–5 HP |
| 2 | Fail | (não listado explicitamente) | "You find yourself powerless to resist. Your mouth opens, and the foul brew slips down your throat... rotten flesh, soured milk, and moldy earth." Efeito: HP -30% (sempre) |

### Condições
- `allowedNodeTypes: [7]` (combate)
- `minLevel: 3`
- `allowedTerrainTypes: [1]` (Swamp)
- `LeadsToFortune: 0`
- `allowOnAllTimeOfDay: 1`

### Veredito: MELHORAR — wording + estrutura
**Problema 1:** A opção "Fail" não tem texto descritivo próprio — apenas o título "Fail" é usado pelo sistema para a rolagem. O jogador deveria ver algo antes de decidir.

**Problema 2:** A opção "Resist" tem RollLimit 12 (93.75% de sucesso), tornando a falha rara. O efeito de falha é devastador (-30% HP permanente). A dissonância é aceitável (alta barreira para um efeito grave), mas o texto deveria avisar.

**Proposta — Texto da Opção 1:**
```
"Resist" — "Fight against the witch's enchantment — but resist with all your might."
```

**Proposta — Texto da Opção 2 (em vez de "Fail"):**
```
"Submit" — "Let the enchantment take hold. The hag offers no choice."
```
Com RollLimit 2 (87.5% falha = cair na armadilha, 12.5% sucesso = resistir).

**Justificativa:** Trocar "Fail" por "Submit" dá agência ao jogador (é uma escolha, não uma falha automática). A rolagem inversa (alta chance de falhar a resistência) cria tensão — o jogador sabe que há risco grave. O RollLimit 12 de "Resist" já é suficiente para a maioria dos casos, então a falha é rara mas possível.

---

[continua no próximo arquivo: parte 144 — eventos 156–160]
