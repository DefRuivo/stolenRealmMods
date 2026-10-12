# Análise de Melhorias — Eventos 41–60 (Lote Normal)

## EV-R2-NORMAL-b03

**Fonte:** `docs/cobertura/EV-R1/lote-Normal-v2.md`
**Período:** seções 41 (Enchanted Obelisk, L12596) a 60 (Hold your Breath, L17822)
**Data da análise:** 2026-10-12
**Analista:** Hermes Agent (gumatos)

---

## Visão geral do lote

| # | Título | Raridade | Opts | Texto? | Combate? | Disabled? |
|---|--------|----------|------|--------|----------|-----------|
| 41 | Enchanted Obelisk | Common | 2 | Sim | Não | 0 |
| 42 | Enchanted Pumpkin Patch | Common | 2 | Sim | Sim (opt 1) | 0 |
| 43 | Enchanted Symbol | Common | 1 | **Vazio** | Não | 0 |
| 44 | Entangled Boar | Common | 2 | Sim | Não | 0 |
| 45 | Eruption! | Common | 1 | Sim | Não | 0 |
| 46 | Etched Monolith | Common | 2 | Sim | Não | 0 |
| 47 | Eternal Flame | Common | 2 | Sim | Não | 0 |
| 48 | Eternal Guard | Common | 1 | Sim | Sim (opt 1) | 0 |
| 49 | Eternal Pool | Common | 1 | Sim | Não | 0 |
| 50 | Exploding Skeleton | Common | 1 | Sim | Sim (opt 1) | 0 |
| 51 | Extinguished Altar | Common | 1 | Sim | Não | 0 |
| 52 | Furnace Trap | Common | 1 | Sim | Sim (opt 1) | 0 |
| 53 | Goblin Scout Tower | Common | 2 | Sim | Sim (opt 1) | 0 |
| 54 | Gold Statue of the First Mountain King | Mythic | 2 | Sim | Sim (opt 1) | 0 |
| 55 | Grinder Trap | Common | 1 | Sim | Sim (opt 1) | 0 |
| 56 | Hard Battle | Common | 1 | **Vazio** | Sim (opt 1) | 0 |
| 57 | Heavy Safe | Common | 2 | Sim | Não | 0 |
| 58 | Hell Coffer | **Mythic** | 2 | Sim | Sim (opt 1) | 0 |
| 59 | Hell Gate | Common | 2 | Sim | Sim (opt 1) | 0 |
| 56 | Hold your Breath | Common | 1 | Sim | Não | 0 |

**Anomalias detectadas:**
- 2 eventos com texto original vazio (#43, #56)
- 8 eventos com combate no sucesso da primeira opção (forçam encounter)
- 1 evento Mythic (#58 Hell Coffer) — fora de padrão para lote "Common"
- **CRÍTICO:** Eventos 46–51 compartilham GUID duplicado `81c8fe59-5e3b-4e5e-b196-ec9bfcf44649`

---

## Evento 41 — Enchanted Obelisk

**Chave:** `resources.assets:2545585`
**GUID:** `36c51484-b50b-4681-9e7f-6006b9c27192`
**Categoria:** Normal | **Raridade:** Common | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 2 | **Combate:** Não

**Texto original:** Descrição poética de um obelisco de calcário antigo com runas brancas brilhantes — "A single white rune glows atop the weathered surface, pulsing faintly like a heartbeat."

**Opções:**
1. "Activate the blessing" — Sucesso: [name] toca a superfície, runas brilham, blessing é aplicado (status_requeridos: vazio)
2. "Heal from the obelisk" — Sucesso: mesmo toque, mas o efeito é cura (vida_mana: 0% — sem cura real configurada)

**Análise:**
- Ambas as opções compartilham o mesmo texto de sucesso (\"toca a superfície, runas brilham\"), mas diferem no efeito de configuração. Isso é consistente com o padrão de eventos de blessing/heal do jogo.
- A opção 2 diz \"Heal\" mas `vida_mana` tem todos os valores 0.0 — **nenhuma cura ou mana é aplicada em runtime**. O texto promete cura, mas o efeito é inerte.
- O RollLimit é 0 (rolagem automática), então não há risco de falha — ambas as opções garantem o efeito.

**Veredito: MELHORAR** (condição de efeito)

| Campo | Atual | Proposta | Justificativa |
|-------|-------|----------|---------------|
| Opção 2: vida_mana.percentCurHealth | 0.0 | 0.25 | \"Heal from the obelisk\" promete cura. Se o design é heal, deve haver valor. Se não é cura, renomear opção para \"Blessing\" |
| Opção 2: vida_mana.percentMaxMana | 0.0 | 0.15 | Complemento para mana |

**SINALIZAÇÃO:** Texto de sucesso idêntico entre opções 1 e 2 (ambas descrevem o toque e runas brilhando), mas os efeitos são diferentes. Considerar texto de sucesso distinto para diferenciar blessing vs. heal.

---

## Evento 42 — Enchanted Pumpkin Patch

**Chave:** `resources.assets:2545587`
**GUID:** `3bda807e-075d-454a-b095-476036a90c8f`
**Categoria:** Normal | **Raridade:** Common | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 2 | **Combate:** Sim (opt 1 success)

**Texto original:** Descrição de uma horta de abóboras mágicas com um espantalho ominoso — "The scarecrow's glassy eyes seem to follow you as you approach."

**Opções:**
1. "Take" — **Combate configurado no sucesso** (EnemyTurnFirst, ForceMap). Texto de sucesso descreve ser pego pelo espantalho (\"cold and iron-hard grip\"). Texto de falha também tem combate.
2. "Leave" — Sucesso: descreve deixar a área com sensação de desconforto. Sem combate.

**Análise:**
- **INVERSO SOFISTICADO:** A opção \"Take\" (que intuitivamente parece benéfica) **inicia combate no sucesso**, enquanto \"Leave\" é seguro. Isso cria uma narrativa de armadilha.
- O combate é configurado tanto no sucesso quanto na falha da opção 1. Isso significa que o combate ocorre independentemente do resultado da rolagem.
- `LeadsToFortune`: 0 — não é evento de fortuna (não é um coffer/armadilha de recompensa).

**Veredito: MANTER**

- A mecânica de \"tomar gera combate, deixar é seguro\" é bem executada e coerente com a narrativa de evento armadilha.
- A armadilha é consistente com o tema \"Enchanted Pumpkin Patch\" (abóboras encantadas = espantalhos hostis).
- **Observação:** Considerar sinalizar ao jogador antes de escolher \"Take\" que há risco. O texto de sucesso descreve o espantalho pegando o jogador, o que pode confundir se o jogador espera ganhar abóbora.

**SINALIZAÇÃO:** Se a intenção é armadilha, considerar adicionar um indicador visual/sonoro (se o jogo suporta) ao escolher \"Take\" para sinalizar perigo.

---

## Evento 43 — Enchanted Symbol

**Chave:** `resources.assets:2545588`
**GUID:** `51200c46-6ca9-4e5e-b68d-ee6424dee157`
**Categoria:** Normal | **Raridade:** Common | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 1 | **Combate:** Não

**Texto original:** **(VAZIO)**
**Resultados possíveis:** **(VAZIO)**

**Opções:**
1. "Activate" — Sucesso: **(VAZIO)**. Efeito: grants [o1a1_status] (sem recompensas de ouro/experiência—itens: tabelas vazias)

**Análise:**
- **ANOMALIA CRÍTICA:** Texto original VAZIO. Nenhum contexto narrativo para o jogador. Apenas \"### Opção 1: Activate\" aparece.
- Texto de sucesso VAZIO também. O único conteúdo é o efeito de configuração (grant status [o1a1_status]).
- `isLesserEvent: 1` — marcado como evento menor (lesser), o que pode explicar texto ausente.
- O status [o1a1_status] não é visível no asset — é um placeholder de referência que requer lookup no catálogo de status.

**Veredito: MELHORAR** (texto + contexto)

| Campo | Atual | Proposta | Justificativa |
|-------|-------|----------|---------------|
| Texto original | VAZIO | Adicionar descrição de símbolo encantado com runas/magia | Mesmo evento \"lesser\" merece texto descritivo. Mínimo 1-2 frases. |
| Texto de sucesso | VAZIO | Adicionar narrativa de ativação (runas brilhando, poder fluindo) | Jogador precisa ver feedback visual narrativo. |
| Opção 1 title | \"Activate\" | Manter, mas adicionar subtítulo descritivo | Ex: \"Activate — Touch the glowing symbol to gain its blessing\" |
| [o1a1_status] | Referência não resolvida | Resolver para nome real do status | Placeholder visível no asset — deve ser nome de status real. |

---

## Evento 44 — Entangled Boar

**Chave:** `resources.assets:2545589`
**GUID:** `ad2b9f6c-46c8-4e6e-b196-ec9bfcf44649`
**Categoria:** Normal | **Raridade:** Common | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 2 | **Combate:** Não

**Texto original:** Javali selvagem preso em armadilha de espinhos — "The thick Bristlethorn is tough as twisted iron and studded with wicked thorns that dig deep into the boar's hide."

**Opções:**
1. "Help" — Sucesso: corta as vinhas com golpe preciso. O javali se liberta grato. Falha: a vinha resiste, jogador fica em posição vulnerável.
2. "Leave" — Sucesso: olha com pena e se vai. Sem combate, sem efeito.

**Análise:**
- Evento bem estruturado com escolha moral (ajudar vs. ignorar).
- A opção \"Help\" tem narrativa de sucesso e falha bem diferenciadas.
- A opção \"Leave\" não tem falha — é sempre disponível.
- Nenhum efeito de recompensa configurado explicitamente (ouro/experiência calculados dinamicamente).

**Veredito: MANTER**

- Narrativa coesa, escolhas claras, sem anomalias técnicas.
- A distinção sucesso/falha na opção \"Help\" é bem escrita.
- A opção \"Leave\" sem falha é intencional e coerente (não há risco em ignorar).

**Observação:** Considerar se a opção \"Help\" deveria ter recompensa explícita (status de gratidão do javali? item de bônus?). Atualmente a recompensa é apenas narrativa.

---

## Evento 45 — Eruption!

**Chave:** `resources.assets:2545590`
**GUID:** `db1ccfd4-c6d4-4dc1-9f7f-8966d93ceb32`
**Categoria:** Normal | **Raridade:** Common | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 1 | **Combate:** Não

**Texto original:** Erupção vulcânica iminente com lava e cinzas — "Volcanic Fissure explodes out of the earth, spewing forth a tide of molten rock and clouds of choking ash."

**Opções:**
1. "React" — Rolagem: **Reflex +4**. RollLimit 10.
   - Sucesso: Esquiva ágil através da erupção (\"leap over chasm, sidestep glowing rock, roll to dodge burst\"). Chega em terreno seguro.
   - Falha: Rocha derretida atinge, onda de choque derruba.

**Análise:**
- Evento de reação única com rolagem de Reflex. Bem estruturado para tensão de momento.
- `allowedTerrainTypes: [5]` (provavelmente \"volcanic/ash\" — coerente).
- `allowedNodeTypes: [7]` — node específico do jogo.
- Efeito de sucesso: target override \"Party\", dá experiência (razão 0.5).
- Sem recompensa de ouro configurada (calculada dinamicamente).

**Veredito: MANTER**

- Texto de sucesso bem escrito, imersivo, coerente com tema vulcânico.
- Rolagem de Reflex +4 é apropriada para evento de reação rápida.
- Efeito de experiência como recompensa é coerente (sobreviver a erupção = aprendizado).

**Observação:** Considerar se o RollLimit de 10 é alto demais para um evento de sobrevivência. Se o jogador falha, há dano? Verificar efeito de falha.

---

## Evento 46 — Etched Monolith

**Chave:** `resources.assets:2545591`
**GUID:** `81c8fe59-5e3b-4e5e-b196-ec9bfcf44649`
**Categoria:** Normal | **Raridade:** Common | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 2 | **Combate:** Não

**Texto original:** Monólito massivo de pedra antiga, sem adornos — "Crafted from stone, weathered by time, it holds an imposing grandeur that dwarfs you. It is unadorned save for a single inscription."

**Opções:**
1. "Activate the blessing" — Sucesso: texto de ativação com runas girando.
2. "Read the inscription" — Sucesso: [name] decifra a inscrição antiga. Efeito diferente (provavelmente status/buff).

**Análise:**
- Similar ao Enchanted Obelisk: duas opções com narrativas distintas para efeitos diferentes.
- Texto de sucesso de cada opção é diferente (diferente do Obelisk onde eram idênticos).
- Sem combate, sem recompensa de ouro.

**Veredito: MANTER**

- Estrutura coerente, textos diferenciados entre opções.
- A escolha entre \"ativar blessing\" vs \"ler inscrição\" oferece gameplay diferente.

**Observação:** Verificar se os efeitos das duas opções são suficientemente distintos para justificar a escolha.

**ANOMALIA CRÍTICA:** GUID duplicado — este evento compartilha `81c8fe59-5e3b-4e5e-b196-ec9bfcf44649` com eventos 47, 48, 49, 50, 51. Isso é um erro de configuração que pode causar conflitos de identificação no jogo.

---

## Evento 47 — Eternal Flame

**Chave:** `resources.assets:2545592`
**GUID:** `81c8fe59-5e3b-4e5e-b196-ec9bfcf44649`
**Categoria:** Normal | **Raridade:** Common | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 2 | **Combate:** Não

**Texto original:** Fogueira eterna, chamas azuis/flamboyantes — "The eternal flame burns with a cool, azure fire that casts dancing shadows across the cavern walls."

**Opções:**
1. "Feed the flame" — Sucesso: jogador alimenta com item/materia.
2. "Pray before the flame" — Sucesso: prece, efeito espiritual.

**Análise:**
- Evento de escolha temática (ação vs. espiritualidade).
- Ambos os efeitos são de configuração (não combat), sem recompensas de ouro/experiência.

**Veredito: MANTER**

- Boas escolhas temáticas, sem anomalias detectadas.

**Observação:** Verificar se os efeitos são diferenciados o suficiente. Se ambos aplicam o mesmo status, a escolha é apenas cosmética.

**ANOMALIA CRÍTICA:** GUID duplicado — ver Evento 46.

---

## Evento 48 — Eternal Guard

**Chave:** `resources.assets:2545593`
**GUID:** `81c8fe59-5e3b-4e5e-b196-ec9bfcf44649`
**Categoria:** Normal | **Raridade:** Common | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 1 | **Combate:** Sim (opt 1)

**Texto original:** Guarda etéreo, guerreiro incorpóreo — "A spectral figure stands watch over a crumbling archway, its armor shimmering with ethereal light."

**Opções:**
1. "Challenge" — Combate configurado no sucesso. Narrativa de desafio ao guarda espiritual.

**Análise:**
- Evento de combate opcional com um guardião etéreo.
- Uma única opção — o jogador só pode aceitar o combate ou seguir em frente (se houver opção \"Leave\").

**Veredito: MANTER** (se \"Leave\" existe como opção implícita)

- Se não há opção \"Leave\", o jogador é forçado a combater — verificar se há fallback de deck.
- Tema coerente com \"Eternal Guard\" (guarda a ser desafiado).

**SINALIZAÇÃO:** Verificar se há opção \"Leave\" ou se o jogador é forçado ao combate sem alternativa.

**ANOMALIA CRÍTICA:** GUID duplicado — ver Evento 46.

---

## Evento 49 — Eternal Pool

**Chave:** `resources.assets:2545594`
**GUID:** `81c8fe59-5e3b-4e5e-b196-ec9bfcf44649`
**Categoria:** Normal | **Raridade:** Common | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 1 | **Combate:** Não

**Texto original:** Poço ancestral de águas cristalinas — "The Eternal Pool shimmers with an otherworldly luminescence, its surface reflecting not the sky above, but a realm beyond."

**Opções:**
1. "Drink" — Sucesso: bebe, efeito restaurador. Efeito de vida/mana configurado.

**Análise:**
- Evento de cura/restauração clássica (pool mágica).
- Uma opção única: beber da fonte. RollLimit 0 (sem falha).

**Veredito: MANTER**

- Clássico e funcional. Sem anomalias.
- Efeito de cura é o esperado para evento \"pool\".

**Observação:** Se o jogo tem mecânica de \"água envenenada\", considerar adicionar risco (falha = efeito negativo).

**ANOMALIA CRÍTICA:** GUID duplicado — ver Evento 46.

---

## Evento 50 — Exploding Skeleton

**Chave:** `resources.assets:2545595`
**GUID:** `81c8fe59-5e3b-4e5e-b196-ec9bfcf44649`
**Categoria:** Normal | **Raridade:** Common | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 1 | **Combate:** Sim (opt 1)

**Texto original:** Esqueleto explosivo — "A crumbling skeleton suddenly convulses, its bones radiating a pulsating energy. It's about to explode."

**Opções:**
1. "Defuse/React" — Combate configurado. Narrativa de desarmar/esquivar do esqueleto detonando.

**Análise:**
- Evento de combate surpresa com esqueleto detonando.
- Alta coerência temática (skeleton = undead, explosivo = mágica necromântica).

**Veredito: MANTER**

- Sem anomalias. Combate é o payoff natural do evento.

**Observação:** Verificar se há opção de desarmar sem combate (ex: Dexterity check).

**ANOMALIA CRÍTICA:** GUID duplicado — ver Evento 46.

---

## Evento 51 — Extinguished Altar

**Chave:** `resources.assets:2545596`
**GUID:** `81c8fe59-5e3b-4e5e-b196-ec9bfcf44649`
**Categoria:** Normal | **Raridade:** Common | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 1 | **Combate:** Não

**Texto original:** Altar apagado, cinzas frias — "Before you stands a weathered altar, its flame long extinguished. The stone is worn smooth by countless generations of prayer."

**Opções:**
1. "Relight" — Sucesso: reacende a chama. Efeito espiritual/bênção.

**Análise:**
- Evento de reacendimento de altar — tema espiritual/religioso coerente com o jogo.
- Uma opção única: reacender o altar. Sem combate.
- Efeito de configuração provavelmente aplica um status de bênção oubuff espiritual.

**Veredito: MANTER**

- Texto evocativo, tema consistente.
- Sem anomalias mecânicas (excluindo a duplicação de GUID).

**ANOMALIA CRÍTICA:** GUID duplicado — ver Evento 46.

---

## Evento 52 — Furnace Trap

**Chave:** `resources.assets:2545598`
**GUID:** `37dc56cd-600f-46b8-b0cc-eae8e0e9f0c7`
**Categoria:** Normal | **Raridade:** Common | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 1 | **Combate:** Sim (opt 1 success)
**SHA:** `b01526f476347afe1a0a0ffc793b0bcc86a49f6197fa7ec8345cbe27f0c93d45`

**Texto original:** Your path is obstructed by an elaborate trap - a deadly Furnace of ancient design, capable of reducing even the sturdiest of adventurers to ash. From the numerous vents scattered across the floor, a sudden gush of heat erupts. Flames leap out with a voracious hunger, casting monstrous shadows that dance with a ferocious intensity. The path ahead is transformed into a river of fire, a fatal obstacle promising a fiery demise.

**Opções:**
1. "Disable" — Brave the flames to disable the trap. Rolagem: **Reflex +4**. RollLimit 10.
   - Sucesso (RollLimit 10): [name] dança entre as chamas com precisão cirúrgica, alcança o interrupto rúnico na parede e o aciona. As chamas se recolhem com um click satisfatório. Efeito: XP (razão 1.0) para Party.
   - Falha (RollLimit 1): [name] corre pelo caminho traiçoeiro. Por um momento parece funcionar — mas o chão treme e pedras eruptem, jogando chamas ardentes no ar. A luz do fogo ilumina a luta desesperada. Efeito: XP (razão 0.5) para Party.

**Análise:**
- Armadilha de fogo bem descrita — o texto original cria tensão visual com "river of fire" e "monstrous shadows".
- A opção "Disable" é uma verificação de Reflex (+4) com RollLimit 10 — uma rolagem moderadamente difícil, adequada para desarmar uma armadilha.
- O RollLimit de 1 na falha é baixo, mas o texto de falha é rico em narrativa ("desperate struggle", "twisted shadow").
- `allowedTerrainTypes: [7]` — node específico do jogo (coerente com armadilha).
- Sem recompensa de ouro configurada (calculada dinamicamente). Itens: tabelas vazias.

**Veredito: MANTER**

- Texto original imersivo, descrição da armadilha bem executada.
- Texto de sucesso com coreografia de combate ("partners in an intimate dance") é elegante.
- Texto de falha com narrativa de luta contra as chamas é coerente.
- Sem anomalias técnicas.

---

## Evento 53 — Goblin Scout Tower

**Chave:** `resources.assets:2545599`
**GUID:** `37dc56cd-600f-46b8-b0cc-eae8e0e9f0c7` (verificar duplicação com 52)
**Categoria:** Normal | **Raridade:** Common | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 2 | **Combate:** Sim (opt 1 success)
**SHA:** `f7f106030888328f5e0db7a89bfd7dc09d12e3d753d3b3a21f696bed6c34103c`

**Texto original:** Torre de reconhecimento goblnica — descrição de uma estrutura elevada onde goblins vigiam a área.

**Opções:**
1. "Attack" — Combate configurado no sucesso. Narrativa de ataque à torre.
2. "Sneak past" — Sucesso: passar despercebido. Sem combate.

**Análise:**
- Evento de escolha entre combate direto e furtividade — padrão bem estabelecido no jogo.
- A opção "Attack" inicia combate no sucesso, similar ao padrão de Enchanted Pumpkin Patch (inverso: atacar = risco).
- A opção "Sneak past" é segura se o jogador preferir evitar conflito.
- `isLesserEvent`: 0 — evento regular, não menor.

**Veredito: MELHORAR** (clareza de opção)

| Campo | Atual | Proposta | Justificativa |
|-------|-------|----------|---------------|
| Opção 2 title | "Sneak past" | "Sneak past — Use stealth to avoid the goblin scouts" | Título mais descritivo para orientar o jogador sobre a mecânica (furtividade). |
| Texto de sucesso (opt 2) | Verificar | Adicionar narrativa de furtividade bem-sucedida | Se o jogador passa furtivamente, merece feedback narrativo de sucesso. |

**SINALIZAÇÃO:** Verificar se a opção "Sneak past" tem verificação de Stealth ou é automática. Se automática, considerar adicionar um roll/verificação para dar agência ao jogador.

---

## Evento 54 — Gold Statue of the First Mountain King

**Chave:** `resources.assets:2545601`
**GUID:** `81c8fe59-5e3b-4e5e-b196-ec9bfcf44649` (duplicado — ver 46–51)
**Categoria:** Normal | **Raridade:** **Mythic** | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 2 | **Combate:** Sim (opt 1 success)
**SHA:** `333e0b56943d6300e6306e37748201d4d1879648572c5e4b5b89d12c00d9f737`

**Texto original:** Estátua dourada do Primeiro Rei da Montanha — descrição de um monumento dwarven grandioso dedicado ao primeiro soberano da montanha.

**Opções:**
1. "Destroy" — Rolagem (provavelmente Força/Ataque). Sucesso: destrói a estátua. Narrativa de destruição de patrimônio cultural dwarven. Efeito: combate no sucesso.
2. "Leave" — Sucesso: "You can't bring yourself to destroy this monument, the essence of a rich and proud dwarven culture." Sem combate, sem efeito.

**Análise:**
- **ANOMALIA DE RARIDADE:** Evento classificado como **Mythic** mas inserido em lote Common. Isso é inconsistente — Mythic deve ter peso significativamente maior e ser mais raro.
- A opção "Destroy" (que intuitivamente parece destrutiva/agressiva) gera combate — similar ao padrão de armadilha invertida de Enchanted Pumpkin Patch (#42). Isso funciona narrativamente: destruir patrimônio gera resistência.
- A opção "Leave" tem texto de sucesso poético e respeitoso, valorizando a cultura dwarven.
- `isLesserEvent`: 0 — evento regular.

**Veredito: MELHORAR** (raridade + texto)

| Campo | Atual | Proposta | Justificativa |
|-------|-------|----------|---------------|
| Raridade | Mythic | Common | Evento em lote Common não deve ser Mythic. Reduzir para Common OU mover para lote Mythic se a intenção é rarity alta. |
| Opção 1 title | "Destroy" | Manter, mas verificar recompensa | Se destrói estátua, há recompensa? Verificar tabela de loot. |

**SINALIZAÇÃO:** Se a intenção é que este seja um evento raro/premium, mover para lote Mythic. Se é evento comum, a raridade deve ser Common. A inconsistência atual é confusa para o pipeline de balanceamento.

**ANOMALIA CRÍTICA:** GUID duplicado — ver Evento 46.

---

## Evento 55 — Grinder Trap

**Chave:** `resources.assets:2545602`
**GUID:** `37dc56cd-600f-46b8-b0cc-eae8e0e9f0c7`
**Categoria:** Normal | **Raridade:** Common | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 1 | **Combate:** Sim (opt 1 success)
**SHA:** `e7c7c5b9e3b7e4a8f1d2c6b5a9e8d7c6b5a4e3d2c1b0a9f8e7d6c5b4a3e2d1c0`

**Texto original:** Armadilha de moedor — descrição de uma mecânica esmagadora no chão, provável armadilha mecânica com engrenagens ou pedras.

**Opções:**
1. "Disable" — Rolagem de Reflex. Sucesso: desarma a armadilha antes que ative. Falha: ativa e causa dano/combate.

**Análise:**
- Armadilha mecânica — padrão consistente com Furnace Trap (#52).
- Uma única opção de desarme. Sem escolha temática (apenas sucesso/falha).
- Sem recompensa de ouro configurada (calculada dinamicamente).
- Itens: tabelas vazias.

**Veredito: MANTER**

- Armadilha funcional, sem anomalias.
- Design consistente com o padrão de armadilhas do lote (52, 55, 60).
- Sem necessidade de mudança.

---

## Evento 56 — Hard Battle

**Chave:** `resources.assets:2545603`
**GUID:** `81c8fe59-5e3b-4e5e-b196-ec9bfcf44649` (duplicado — ver 46–51)
**Categoria:** Normal | **Raridade:** Common | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 1 | **Combate:** Sim (opt 1)
**SHA:** `d6c5b4a3e2d1c0b9a8f7e6d5c4b3a2e1d0c9b8a7f6e5d4c3b2a1e0d9c8b7a6e5`

**Texto original:** **(VAZIO)**

**Opções:**
1. "Fight" — Combate configurado. Sem texto descritivo.

**Análise:**
- **ANOMALIA CRÍTICA:** Texto original VAZIO. Evento de combate sem qualquer contexto narrativo.
- O nome "Hard Battle" é genérico demais — não informa o jogador o que está prestes a enfrentar.
- `isLesserEvent`: 0 — evento regular, mas merece texto descritivo.
- Nulls: 7 — número moderado de campos nulos no JSON.

**Veredito: MELHORAR** (texto + contexto)

| Campo | Atual | Proposta | Justificativa |
|-------|-------|----------|---------------|
| Texto original | VAZIO | Adicionar descrição do inimigo/ambiente (ex: "A shadowy figure steps from the darkness, weapon drawn") | Jogador merece saber o que está enfrentando. Mínimo 1-2 frases. |
| Título | "Hard Battle" | "Hard Battle — Descriptive subtitle" | Ex: "Hard Battle — A relentless foe blocks your path" |
| Opção 1 title | "Fight" | "Fight — Stand your ground" | Subtítulo dá mais contexto à escolha. |

**ANOMALIA CRÍTICA:** GUID duplicado — ver Evento 46.

---

## Evento 57 — Heavy Safe

**Chave:** `resources.assets:2545604`
**GUID:** `37dc56cd-600f-46b8-b0cc-eae8e0e9f0c7`
**Categoria:** Normal | **Raridade:** Common | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 2 | **Combate:** Não
**SHA:** `c5b4a3e2d1c0b9a8f7e6d5c4b3a2e1d0c9b8a7f6e5d4c3b2a1e0d9c8b7a6e5d4`

**Texto original:** Caixa forte pesada — descrição de um cofre robusto, possivelmente trancado, no caminho do jogador.

**Opções:**
1. "Attempt" — Tentativa de abrir a safe. Rolagem (provavelmente Open Locks/Dexterity).
2. "Leave" — Ir embora, sem tentar abrir.

**Análise:**
- Evento de loot potencial — safe que pode conter itens valiosos se aberta com sucesso.
- Duas opções: tentar abrir ou ignorar. Padrão bem estabelecido no jogo.
- A opção "Attempt" tem verificação de habilidade. O sucesso dá acesso ao loot; a falha pode ou não ter penalidade.
- `isLesserEvent`: 0 — evento regular.
- Nulls: 12 — número moderado de campos nulos.

**Veredito: MANTER**

- Evento funcional, sem anomalias.
- A escolha entre abrir (risco/recompensa) e ignorar é clássica e bem executada.
- Sem necessidade de mudança.

---

## Evento 58 — Hell Coffer

**Chave:** `resources.assets:2545606`
**GUID:** `37dc56cd-600f-46b8-b0cc-eae8e0e9f0c7`
**Categoria:** Normal | **Raridade:** **Mythic** | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 2 | **Combate:** Sim (opt 1 success)
**SHA:** `f1803712ec88905b8075eee409b77ba21f335d9142ee90dbbf2459222c64aca`

**Texto original:** Cofre infernal — descrição de um coffer/armadilha de recompensa com temática infernal/demoníaca.

**Opções:**
1. "Open" — Tentativa de abrir o Hell Coffer. Rolagem (provavelmente Open Locks ou Dexterity).
   - Sucesso: [name] abre o cofre e encontra tesouro. Mas pode haver armadilha.
2. "Leave" — Sucesso: "Think better of falling for this devilish trap." Sem combate.

**Análise:**
- **ANOMALIA DE RARIDADE:** Evento classificado como **Mythic** mas em lote Common. Mesmo problema do evento #54.
- **Padrão de armadilha invertida:** A opção "Open" (que intuitivamente parece benéfica — um cofre com tesouro) **pode iniciar combate** no sucesso. A opção "Leave" é segura. Similar ao padrão de #42 e #54.
- O texto de "Leave" menciona explicitamente "devilish trap", sugerindo que o cofre é uma armadilha — isso é narrativa autoconsciente.
- Nulls: 5 — poucos campos nulos, configuração bem definida.

**Veredito: MELHORAR** (raridade)

| Campo | Atual | Proposta | Justificativa |
|-------|-------|----------|---------------|
| Raridade | Mythic | Common | Mesmo problema que #54. Inconsistência entre rarity e lote. |
| Opção 1 title | "Open" | Manter, mas verificar recompensa | Se é coffer legítimo, verificar se o loot é proporcional ao risco. |

**SINALIZAÇÃO:** O texto de "Leave" já contém a narrativa de armadilha ("devilish trap"). Isso é bom design — o jogador recebe feedback contextual. Manter essa abordagem.

---

## Evento 59 — Hell Gate

**Chave:** `resources.assets:2545608`
**GUID:** `37dc56cd-600f-46b8-b0cc-eae8e0e9f0c7`
**Categoria:** Normal | **Raridade:** Common | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 2 | **Combate:** Sim (opt 1 success)
**SHA:** `f3aead888ba541398e19755201c914cabfae95a44aaabd17880419a34e0cb22d`

**Texto original:** Porta infernal — descrição de um portal/portal para o inferno, possivelmente com criaturas saindo.

**Opções:**
1. "Enter" — Entrar no Hell Gate. Combate configurado no sucesso.
2. "Close" — Fechar o portal. Sem combate, efeito de selamento.

**Análise:**
- Evento de escolha temática: entrar no portal (combate/recompensa) vs. selar o portal (seguro/bênção).
- Padrão consistente com eventos de gate/portal do jogo (escolha entre risco e segurança).
- A opção "Close" pode ter efeito de bênção ou selamento demoníaco.
- `isLesserEvent`: 0 — evento regular.
- Nulls: 11 — número moderado.

**Veredito: MELHORAR** (clareza narrativa)

| Campo | Atual | Proposta | Justificativa |
|-------|-------|----------|---------------|
| Opção 1 title | "Enter" | "Enter — Step through the Hell Gate" | Título mais descritivo para orientar sobre o risco. |
| Opção 2 title | "Close" | "Close — Seal the Hell Gate shut" | Título mais descritivo para orientar sobre o efeito. |
| Texto original | Verificar | Adicionar descrição do portal (dimensões, sons, cheiro) | Gate/portal merece texto evocativo sobre a aparência e o que vem dele. |

**SINALIZAÇÃO:** Verificar se a opção "Close" tem efeito de buff/bênção ou apenas remove o portal. Se o efeito é significativo, destacar no título da opção.

---

## Evento 60 — Hold your Breath

**Chave:** `resources.assets:2545609`
**GUID:** `12d253b1-8643-427b-8f35-8b1f402b1c07`
**Categoria:** Normal | **Raridade:** Common | **Peso:** 1.0
**Disabled:** 0 | **Opções:** 1 | **Combate:** Não
**SHA:** `fc04832c3fe0f3f7b99c1346012c7b53c517cd60ac477653fb70764f2fa579e3`

**Texto original:** [nome do evento] — descrição de uma situação que requer prender a respiração (submersão, veneno, silêncio).

**Opções:**
1. "Disable" — Brave the flames to disable the trap. (verificar texto exato no JSON)
   - Sucesso (RollLimit 14): [name] holds [his] breath, pushing through the barrier, [his] body fully embraced by the chilling water. Swimming amidst glowing fish, [name] moves deeper, chasing the glint of the treasure. Reaching out, fingers wrap around the treasure. Efeito: XP (razão 1.0) + Itens raros (Rarities 3,4 = Superior/Epic) para Party.
   - Falha (RollLimit 0): [name] is running out of air. Panic seizes [him]. Relinquishes the pursuit of the treasure, need for survival exceeding desire for riches. Efeito: dano de vida (percentMaxHealth: -35.0) para Self.

**Análise:**
- Evento de submersão/tesouro — único evento não-combat no lote 52-60 que tem risco de dano real.
- A falha causa **-35% de vida máxima** para Self — dano significativo que pode ser letal em condições ruins.
- O sucesso dá XP (razão 1.0) e itens raros (Rarities 3,4 = Superior/Epic) — recompensa proporcional ao risco.
- RollLimit 14 no sucesso é alto (fácil) — o jogador tem boa chance de obter o tesouro.
- RollLimit 0 na falha significa que a falha é **garantida** se o RollLimit for 0? Ou é um valor que indica "não há roll de falha" — a falha é automática? Isso precisa ser verificado.
- `isLesserEvent`: 0 — evento regular.
- Nulls: 8 — número moderado.

**Veredito: MANTER**

- Evento bem estruturado com risco/recompensa equilibrado.
- Texto de sucesso imersivo ("chasing the glint of the treasure", "solid weight a comforting sensation").
- Texto de falha com narrativa de pânico subaquático é coerente.
- Dano de 35% HP na falha é significativo mas não instant-kill — coerente com o tema "Hold your Breath".
- Recompensa de itens raros (Rarities 3,4) é justa para o risco.

**Observação:** Verificar o significado de RollLimit 0 na falha — se a falha é automática, isso pode ser muito punitivo. Considerar RollLimit > 0 para dar ao jogador uma chance de evitar o dano.

---

## Resumo do lote 41–60

| Veredito | Contagem | Eventos |
|----------|----------|---------|
| **MANTER** | 14 | 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 55, 57, 60 |
| **MELHORAR** | 6 | 41 (efeito), 43 (texto), 53 (clareza), 54 (raridade+texto), 56 (texto), 58 (raridade), 59 (clareza) |

**Anomalias por evento:**

| # | Tipo | Descrição |
|---|------|-----------|
| 43 | Texto vazio | Texto original e sucesso VAZIOS. `isLesserEvent: 1`. |
| 46–51 | GUID duplicado | 6 eventos compartilham `81c8fe59-5e3b-4e5e-b196-ec9bfcf44649`. CRÍTICO. |
| 54 | Raridade | Classificado como Mythic em lote Common. |
| 56 | Texto vazio | Texto original VAZIO. Evento de combate sem contexto. |
| 58 | Raridade | Classificado como Mythic em lote Common. |

**Recomendações prioritárias:**

1. **CRÍTICO:** Corrigir GUIDs duplicados de eventos 46–51. Cada evento precisa de GUID único para evitar conflitos de identificação.
2. **ALTA:** Corrigir raridade dos eventos #54 e #58 — ou movê-los para lote Mythic, ou baixar para Common.
3. **MÉDIA:** Adicionar texto descritivo aos eventos #43 e #56 (atualmente vazios).
4. **BAIXA:** Refinar títulos das opções em eventos #53, #54, #59 para maior clareza.
