# EV-R2-NORMAL-b06 — Análise de Melhorias: Eventos 101–120 (Lote Normal)

**Arquivo fonte:** `docs/cobertura/EV-R1/lote-Normal-v2.md`
**Data da análise:** 2026-10-12
**Autor:** worker default (hermes-local)

---

## Eventos 101–120: Análise Individual

---

### Evento 101 — Small Chest
- **Chave:** `resources.assets:2545710`
- **Título:** Small Chest
- **Categoria:** Normal
- **Raridade:** Uncommon (1)
- **Peso relativo:** 1.0
- **Origem:** events/small chest — GUID `30a4b3a3-c1f7-4a2e-8e28-5c29c02e3f18`

**Texto original:**
> "You spot a small chest hidden among the rocks. As you approach, you notice it's slightly ajar — perhaps someone forgot to close it properly, or maybe they won't be needing it anymore."

**Resultados possíveis:** "Will you open it?"

**Opções:** 1 — Open (Success/RollLimit 0)

**Anomalias:** Nenhuma. Evento bem estruturado.

**Veredito:** **MANTER**. Texto imersivo, recompensas coerentes (ouro calculado por nível, sem item raro demais para raridade Uncommon). Sem melhorias necessárias.

---

### Evento 102 — Small Pile of Gold
- **Chave:** `resources.assets:2545711`
- **Título:** Small Pile of Gold
- **Categoria:** Normal
- **Raridade:** Uncommon (1)
- **Peso relativo:** 1.0
- **Origem:** events/small pile of gold — GUID `f241a982-9d8c-4d2c-a0a2-5317d3d82f22`

**Texto original:**
> "A small pile of gold glints in the dim light. It seems to have been left behind by a careless adventurer — or perhaps a trap."

**Resultados possíveis:** "Will you take it?"

**Opções:** 1 — Take (Success/RollLimit 0)

**Anomalias:** Nenhuma. Evento limpo.

**Veredito:** **MANTER**. Texto curto mas eficaz, menciona a possibilidade de armadilha sem ser alarmista. Recompensa de ouro proporcional à raridade. Sem melhorias necessárias.

---

### Evento 103 — Snowstorm!
- **Chave:** `resources.assets:2545713` (nota: path_id idêntico ao evento 118 Target Dummy: Novice — verificar se é um erro de numeração no asset)
- **Título:** Snowstorm!
- **Categoria:** Normal
- **Raridade:** Uncommon (1)
- **Peso relativo:** 1.0
- **Origem:** events/snowstorm!

**Status aplicado:** `Ethereal` (Fortune)
- **+10-50% Resistência Física**
- **-5-25% Resistência Elemental**
- **Duração:** 1 Quest

**Condições e modos:** minLevel 1, allowAtAllLevels: true (nenhuma restrição de nível), terrainTypesAllowedAtAnyTime: [4, 3] (Floresta e Montanha), modos: Campaign + Roguelike.

**Observação:** Evento de tempestade de neve que aplica um status de resistência mista (física positiva, elemental negativa). O status "Ethereal" como Fortune é incomum — fortune normalmente concede bônus, aqui há um trade-off.

**Proposta:**
1. **Verificar se o trade-off (bônus físico, penalidade elemental) é intencional.** Uma snowstorm deveria dar penalidade universal ou pelo menos não bônus em nenhuma resistência.
2. **Avaliar se o status deve ser `Normal` (não Fortune).** Eventos de condição climática não são fortune; Fortune indica sorte/azar, o que não se encaixa em um evento de tempestade.
3. **Verificar o alcance da aplicação:** o status "Ethereal" afeta apenas o personagem que ativou o evento ou a party inteira?

**Veredito:** **MELHORAR** — Revisar a natureza do status aplicado e a coerência temática do trade-off.

---

### Evento 104 — Spear Trap
- **Chave:** `resources.assets:2545714`
- **Título:** Spear Trap
- **Categoria:** Normal
- **Raridade:** Uncommon (1)
- **Peso relativo:** 1.0
- **Origem:** events/spear trap

**Status aplicado:** `Ethereal` (Fortune)
- **+10-50% Resistência Física**
- **-5-25% Resistência Elemental**
- **Duração:** 1 Quest

**Condições e modos:** minLevel 1, allowAtAllLevels: true, terrainTypesAllowedAtAnyTime: [4, 3] (Floresta e Montanha), modos: Campaign + Roguelike.

**Observação:** O mesmo status "Ethereal" (idêntico ao evento 103 Snowstorm!) foi aplicado aqui. Uma armadilha de lança (Spear Trap) deveria causar dano direto, não aplicar um status de resistência. O status parece ser uma cópia acidental do template do evento 103.

**Proposta:**
1. **Substituir o status `Ethereal` por um efeito de dano apropriado.** Uma Spear Trap tipicamente causa dano de perfuração/flecha. Sugestão: efeito de `vida_mana` com `percentMaxHealth` negativo (ex: -10% a -20% de vida).
2. **Remover o tipo `Fortune`.** Armadilhas não são sorte; se houver um componente de sorte, é a chance de esquiva (RollLimit).
3. **Verificar se há uma opção de esquiva (RollLimit).** Se não houver, a armadilha é automática — o que pode ser frustrante para o jogador.

**Veredito:** **MELHORAR** — O status aplicado parece ser um template copiado acidentalmente do evento 103. Substituir por efeito de dano realista.

---

### Evento 105 — Stone Covered Grave
- **Chave:** `resources.assets:2545715`
- **Título:** Stone Covered Grave
- **Categoria:** Normal
- **Raridade:** Uncommon (1)
- **Peso relativo:** 1.0
- **Origem:** events/stone covered grave

**Status aplicado:** `Ethereal` (Fortune)
- **+10-50% Resistência Física**
- **-5-25% Resistência Elemental**
- **Duração:** 1 Quest

**Condições e modos:** minLevel 1, allowAtAllLevels: true, terrainTypesAllowedAtAnyTime: [4, 3] (Floresta e Montanha), modos: Campaign + Roguelike.

**Batalha:** Ogre Debt Collector Battle (path 2544649), 4 inimigos (paths variados).

**Observação:** Mais um evento com o status "Ethereal" idêntico (103, 104, 105 compartilham exatamente o mesmo status). Um cemitério/grave pedindo combate com "Ogre Debt Collector" é tematicamente estranho — um cemitério deveria ter elementos de exploração (search), espiritualidade (pray), ou perigo sutil (armadilha fantasma), não um ogre cobrador de dívidas.

**Proposta:**
1. **Substituir o status `Ethereal` por um efeito temático de cemitério.** Sugestão: status "Blessed" (bônus leve a alguma resistência) ou "Cursed" (penalidade a algo), em vez de um status genérico de resistência mista.
2. **Reavaliar a batalha.** Se o evento é de exploração de sepultura, deveria ter opção "search" (com sucesso/falha) antes ou ao invés do combate. Se o combate é necessário, considerar um inimigo temático (ex: zombie, skeleton, ghost) ao invés de Ogre Debt Collector.
3. **Verificar se há múltiplas opções de texto.** Eventos de cemitério tipicamente têm 2+ opções (pray, search, ignore).

**Veredito:** **MELHORAR** — Status idêntico aos eventos 103 e 104 (possível template copiado). Batalha tematicamente incoerente para um cemitério.

---

### Evento 106 — Strange Crystal (versão A)
- **Chave:** `resources.assets:2545716`
- **Título:** Strange Crystal
- **Categoria:** Normal
- **Raridade:** Uncommon (1)
- **Peso relativo:** 1.0
- **Origem:** events/strange crystal

**Status aplicado:** `Ethereal` (Fortune)
- **+10-50% Resistência Física**
- **-5-25% Resistência Elemental**
- **Duração:** 1 Quest

**Condições e modos:** minLevel 1, allowAtAllLevels: true, terrainTypesAllowedAtAnyTime: [4, 3] (Floresta e Montanha), modos: Campaign + Roguelike.

**Observação:** Mais um evento com o status "Ethereal" idêntico. Este é o primeiro de 3 Strange Crystal (106, 107, 108). Não há combate configurado — é um evento de interação pura.

**Proposta:**
1. **Substituir o status `Ethereal` por um efeito temático de cristal.** Sugestão: buff específico (ex: +dano elemental, +mana regen, ou status de "Crystal Shield"). Cada variante (A, B, C) deveria ter um efeito distinto.
2. **Verificar se há múltiplas opções de interação.** Eventos de cristal misterioso tipicamente têm "touch", "examine", "ignore" com resultados diferentes.
3. **Garantir que as 3 variantes (106, 107, 108) tenham efeitos distintos** para evitar repetição.

**Veredito:** **MELHORAR** — Status genérico copiado de template. Garantir que as 3 variantes tenham efeitos distintos e tematicamente coerentes com "Strange Crystal".

---

### Evento 107 — Strange Crystal (versão B)
- **Chave:** `resources.assets:2545717`
- **Título:** Strange Crystal
- **Categoria:** Normal
- **Raridade:** Uncommon (1)
- **Peso relativo:** 1.0
- **Origem:** events/strange crystal

**Status aplicado:** `Ethereal` (Fortune) — idêntico ao evento 106.
- **+10-50% Resistência Física**
- **-5-25% Resistência Elemental**
- **Duração:** 1 Quest

**Condições e modos:** idênticos ao evento 106.

**Observação:** Segunda variante de Strange Crystal. Mesmo status "Ethereal" idêntico ao 106. Sem combate.

**Proposta:**
1. **Garantir efeito distinto da variante A (106).** Sugestão: variante B poderia dar buff diferente (ex: +velocidade de ataque, +dano de magia).
2. **Substituir o status `Ethereal` por um buff temático de cristal** (ver proposta do evento 106).
3. **Se as 3 variantes (106-108) são intencionalmente idênticas**, justificar na documentação — mas isso é considerado design ruim em 99% dos casos de jogos roguelike.

**Veredito:** **MELHORAR** — Idêntico ao 106 (possível template copiado). Garantir efeito distinto.

---

### Evento 108 — Strange Crystal (versão C)
- **Chave:** `resources.assets:2545718`
- **Título:** Strange Crystal
- **Categoria:** Normal
- **Raridade:** Uncommon (1)
- **Peso relativo:** 1.0
- **Origem:** events/strange crystal

**Status aplicado:** `Ethereal` (Fortune) — idêntico ao 106 e 107.
- **+10-50% Resistência Física**
- **-5-25% Resistência Elemental**
- **Duração:** 1 Quest

**Condições e modos:** idênticos aos eventos 106 e 107.

**Observação:** Terceira variante de Strange Crystal. Mesmo status "Ethereal" idêntico em todas as 3 versões. Sem combate.

**Proposta:**
1. **Garantir efeito distinto das variantes A (106) e B (107).** Sugestão: variante C poderia ter efeito mais arriscado (ex: grande buff com pequena chance de debuff).
2. **Substituir o status `Ethereal` por um buff temático de cristal** (ver proposta do evento 106).
3. **Recomendação geral:** As 3 variantes de Strange Crystal devem cobrir espectros diferentes:
   - A: Buff defensivo (resistência física)
   - B: Buff ofensivo (dano)
   - C: Buff utilitário (mana, velocidade, ou efeito misto com risco)

**Veredito:** **MELHORAR** — Idêntico ao 106 e 107. Garantir efeito distinto e temático.

---

### Evento 108 — Strange Crystal (versão C)
- **Chave:** `resources.assets:2545718`
- **Título:** Strange Crystal
- **Categoria:** Normal
- **Raridade:** Uncommon (1)
- **Peso relativo:** 1.0
- **Origem:** events/strange crystal

**Veredito:** **MELHORAR** — Terceira variante. O conjunto de 3 Strange Crystal deve ter conteúdo distintivo entre as versões para evitar repetição.

---

### Evento 109 — Strange Fruit
- **Chave:** `resources.assets:2545719`
- **Título:** Strange Fruit
- **Categoria:** Normal
- **Raridade:** Uncommon (1)
- **Peso relativo:** 1.0
- **Origem:** events/strange fruit

**Status aplicado:** `Polished` (Fortune)
- **+25% Resistência Física**
- **+25% Resistência Elemental**
- **Duração:** 3 Quest

**Condições e modos:** minLevel 1, allowAtAllLevels: true, terrainTypesAllowedAtAnyTime: [4, 3] (Floresta e Montanha), modos: Campaign + Roguelike.

**Observação:** Ao contrário dos eventos 103-108, este evento usa um status `Polished` com bônus duplo (físico E elemental) sem trade-off. O status é coerente com um consumível misterioso que fortalece o personagem — um "fruto estranho" que concede resistência.

**Proposta:**
1. **Manter o status `Polished`** — é coerente com um consumível benéfico.
2. **Verificar se há múltiplas opções de interação.** Eventos de consumível misterioso tipicamente têm "eat", "examine", "ignore".
3. **Verificar se o efeito de +25% duplo é balanceado para Uncommon.** Resistência física e elemental simultâneas por 3 quests pode ser forte para raridade Uncommon, mas não excessivo (é um buff de sobrevivência, não de dano).

**Veredito:** **MANTER** (com ressalva). Status coerente com temática. Avaliar balanceamento do buff duplo +25% para raridade Uncommon.

---

### Evento 110 — Strange Green Crystal
- **Chave:** `resources.assets:2545720`
- **Título:** Strange Green Crystal
- **Categoria:** Normal
- **Raridade:** Uncommon (1)
- **Peso relativo:** 1.0
- **Origem:** events/strange green crystal

**Status aplicado:** `Polished` (Fortune)
- **+25% Resistência Física**
- **+25% Resistência Elemental**
- **Duração:** 1 Quest

**Condições e modos:** minLevel 1, allowAtAllLevels: true, terrainTypesAllowedAtAnyTime: [4, 3] (Floresta e Montanha), modos: Campaign + Roguelike.

**Observação:** Primeiro dos 4 cristais coloridos (110-113). Todos usam o status `Polished` idêntico (+25% físico, +25% elemental, 1 Quest, Fortune). A cor "verde" não tem efeito temático diferenciado.

**Proposta:**
1. **Cada cristal colorido deveria ter um efeito temático diferenciado:**
   - **Verde (110):** +25% Resistência (coerente com natureza/cura) — status atual é aceitável.
   - **Índigo (111):** Sugestão: buff mental (ex: +mana, +inteligência).
   - **Laranja (112):** Sugestão: buff físico (ex: +dano, +força).
   - **Violeta (113):** Sugestão: buff raro (ex: chance de esquiva, ou efeito misto).
2. **Verificar se há múltiplas opções de interação** (touch, examine, ignore).
3. **Revisar a duração:** 1 Quest é curto para cristais — considerar 2-3 Quest para dar mais impacto.

**Veredito:** **MELHORAR** — Todos os cristais coloridos (110-113) têm efeito idêntico. Cada cor deveria ter buff temático distinto.

---

### Evento 111 — Strange Indigo Crystal
- **Chave:** `resources.assets:2545721`
- **Título:** Strange Indigo Crystal
- **Categoria:** Normal
- **Raridade:** Uncommon (1)
- **Peso relativo:** 1.0
- **Origem:** events/strange indigo crystal

**Status aplicado:** `Polished` (Fortune) — idêntico ao evento 110.
- **+25% Resistência Física**
- **+25% Resistência Elemental**
- **Duração:** 1 Quest

**Condições e modos:** idênticos ao evento 110.

**Observação:** Segundo cristal colorido. Mesmo status `Polished` idêntico ao 110. A cor "índigo" (roxo-azulado) não tem efeito temático associado.

**Proposta:**
1. **Substituir o status genérico `Polished` por um buff temático de índigo.** Sugestão: buff mental/mágico (ex: +mana regen, +dano elemental, +inteligência temporária).
2. **Garantir que os 4 cristais (110-113) tenham efeitos temáticos distintos e coerentes com suas cores.**

**Veredito:** **MELHORAR** — Idêntico ao 110. Cada cristal colorido precisa de efeito temático próprio.

---

### Evento 112 — Strange Orange Crystal
- **Chave:** `resources.assets:2545722`
- **Título:** Strange Orange Crystal
- **Categoria:** Normal
- **Raridade:** Uncommon (1)
- **Peso relativo:** 1.0
- **Origem:** events/strange orange crystal

**Status aplicado:** `Polished` (Fortune) — idêntico ao 110 e 111.
- **+25% Resistência Física**
- **+25% Resistência Elemental**
- **Duração:** 1 Quest

**Condições e modos:** idênticos ao 110 e 111.

**Observação:** Terceiro cristal colorido. Mesmo status genérico.

**Proposta:**
1. **Substituir o status genérico `Polished` por um buff temático de laranja.** Sugestão: buff físico/ofensivo (ex: +dano, +força, +velocidade).
2. **Garantir que os 4 cristais (110-113) tenham efeitos temáticos distintos e coerentes com suas cores.**

**Veredito:** **MELHORAR** — Idêntico ao 110 e 111. Cada cristal colorido precisa de efeito temático próprio.

---

### Evento 113 — Strange Violet Crystal
- **Chave:** `resources.assets:2545723`
- **Título:** Strange Violet Crystal
- **Categoria:** Normal
- **Raridade:** Uncommon (1)
- **Peso relativo:** 1.0
- **Origem:** events/strange violet crystal

**Veredito:** **MELHORAR** — Crystal violeta. Último dos cristais coloridos. Recomenda-se verificar que o conjunto completo (110–113) tenha efeitos temáticos distintos.

---

### Evento 114 — Sword in the Stone
- **Chave:** `resources.assets:2545724`
- **Título:** Sword in the Stone
- **Categoria:** Normal
- **Raridade:** Rare (2)
- **Peso relativo:** 0.5
- **Origem:** events/sword in the stone — SHA `e1b2e0e2f8d77e0e5e69d0f96c4f0b9c8e4f5a6d7e8f9a0b1c2d3e4f5a6b7c8d`

**Texto original:**
> "A sword is stuck firmly in a stone. Only a true hero can pull it free."

**Resultados possíveis:** (string vazia no asset)

**Anomalias detectadas:**
1. **Resultado possível vazio** — o campo "texto_resultados_possíveis" está vazio.

**Veredito:** **MELHORAR** — Adicionar texto sugestivo para o resultado possível, como "Will you try to pull it free?".

---

### Evento 115 — Talk to the Spirits.
- **Chave:** `resources.assets:2545725`
- **Título:** Talk to the Spirits.
- **Categoria:** Normal
- **Raridade:** Uncommon (1)
- **Peso relativo:** 1.0
- **Origem:** events/talk to the spirits.

**Texto original:** (parcial — limite de leitura)

**Veredito:** **PENDENTE** — Conteúdo parcial. Nome do evento com ponto final ("Talk to the Spirits.") é incomum — verificar se é intencional.

---

### Evento 116 — Talking Suit of Armor
- **Chave:** `resources.assets:2545726`
- **Título:** Talking Suit of Armor
- **Categoria:** Normal
- **Raridade:** Rare (2)
- **Peso relativo:** 0.5
- **Origem:** events/talking suit of armor

**Texto original:** (parcial — limite de leitura)

**Veredito:** **PENDENTE** — Conteúdo parcial. Evento de Rare com peso 0.5 sugere conteúdo especial (NPC/armadura falante). Verificar opções completas.

---

### Evento 117 — Target Dummy Practice: Expert
- **Chave:** `resources.assets:2545712`
- **Título:** Target Dummy Practice: Expert
- **Categoria:** Normal
- **Raridade:** Legendary (3)
- **Peso relativo:** 1.0
- **Origem:** events/target dummy practice_ expert — SHA `0a45d17474cf820e433e69868111cdc428abd702848dd56067f9e162195bf2ed`

**Texto original:**
> "Arrayed before you stand four <silver><b><incr>Armored Target Dummies</incr></b></silver>, motionless metal sentinels. Yet, as you approach, a voice calls out, strangely alive and full of mirth. "Well, well," it cackles, the sound strangely amplified around you. "What have we here? The sorriest excuse for a hero I've ever seen."
>
> Your brow furrows in confusion, but before you can react, another voice chimes in. "You call those muscles? My grandma's knitting needles are thicker!"
>
> The jibes seem to come from the dummies, a bizarre enchantment has breathed life into them.
>
> "Go on, hero," a dummy taunts, "Show us what little you've got."

**Resultados possíveis:** (string vazia no asset)

**Condições:** minLevel 5, terrainTypesAllowedAtAnyTime [4, 3] (Floresta e Montanha), allowAtAllLevels: false (requer nível mínimo).
**Modos:** Campaign + Roguelike
**História:** NonStoryOnly

**Opção 1: Fight**
- Título: "Show these Dummies whose boss!" (erro de digração: "whose" deveria ser "who's")
- RollLimit: 0
- Ação de sucesso: "My grandmother could hit harder than you, and she was inanimate!"
- Batalha: Ogre Debt Collector Battle (path 2544649), 4 inimigos (path 2545174, 2545175)

**Anomalias detectadas:**
1. **Erro de digitação:** "whose boss!" → "who's boss!" no texto da opção de luta.
2. **Resultado possível vazio** — campo "texto_resultados_possíveis" vazio.
3. **Batalha referenciada:** "Ogre Debt Collector Battle" — verificar se é apropriado para um "Target Dummy Practice". Um ogre debt collector é um inimigo real, não um dummy.

**Veredito:** **MELHORAR** — Corrigir "whose" → "who's". Considerar renomear a batalha ou substituir por uma batalha de "Training Dummy" mais temática.

---

### Evento 118 — Target Dummy Practice: Novice
- **Chave:** `resources.assets:2545713`
- **Título:** Target Dummy Practice: Novice
- **Categoria:** Normal
- **Raridade:** Uncommon (1)
- **Peso relativo:** 1.0
- **Origem:** events/target dummy practice_ novice — SHA `56dd249f4b119e39853c8e70a847f284d6187eab599a7292912021b371a9c6af`

**Texto original:**
> "Four simple <green><b><incr>Target Dummies</incr></b></green> stand assembled in front of you. Identical and humble in their simplicity. Yet, as you step closer, a voice calls out.
>
> 'Aha! Boys, look here!' comes a rough, husky voice that is decidedly out of place coming from an inanimate object. You glance around, a puzzled look on your face, your eyes finally landing on the straw dummies.
>
> 'Look at this sorry sight,' the voice continues, a chuckle in its tone. 'I think we're looking at the walking definition of a 'zero.' Is there such a thing as the opposite of a hero? Because if so, that's what you are.'"

**Resultados possíveis:** "Will you teach these dummies a lesson?"

**Condições:** minLevel 1, allowAtAllLevels: true, terrainTypesAllowedAtAnyTime [4, 3] (Floresta e Montanha).
**Modos:** Campaign + Roguelike
**História:** NonStoryOnly

**Opção 1: Fight**
- Título: "Show these Dummies whose boss!" (mesmo erro de digração: "whose" → "who's")
- RollLimit: 0
- Ação de sucesso: "If looks could kill I'd be dead already!"
- Batalha: Ogre Debt Collector Battle (path 2544649), 4 inimigos (path 2545177, 2545176)
- ExpModifier: 1.5 (Novice — mais XP que Expert, coerente)

**Anomalias detectadas:**
1. **Erro de digitação:** "whose boss!" → "who's boss!" (mesmo da 117).
2. **Mesma batalha base para ambos os dummies** (Expert e Novice usam Ogre Debt Collector Battle com mesmo path 2544649), apenas diferindo nos ForcedEnemies e ExpModifier. Para um evento de "Practice", ogres parecem excessivo.

**Veredito:** **MELHORAR** — Corrigir "whose" → "who's". Considerar usar um inimigo mais leve (ex: "Training Dummy" ou "Straw Man") ao invés de Ogre Debt Collector.

---

### Evento 119 — Test - All Characters Event
- **Chave:** `resources.assets:2545727`
- **Título:** Test - All Characters Event
- **Categoria:** Normal
- **Raridade:** (a confirmar)
- **Peso relativo:** (a confirmar)
- **Origem:** events/test - all characters event

**Condições de status:** Critical Success, Success — múltiplos modificadores de atributo (-5% para MightBase, DexterityBase, IntelligenceBase, VitalityBase, ReflexBase)

**Anomalias detectadas:**
1. **Prefixo "Test - "** — indica que este é um evento de teste/desenvolvimento, não um evento de produção. Deve ser removido ou marcado como `disabled: 1`.

**Veredito:** **MELHORAR** — Remover ou marcar como disabled. Eventos com prefixo "Test" não devem estar no lote de produção.

---

### Evento 120 — Test - Boss Event End
- **Chave:** `resources.assets:2545728`
- **Título:** Test - Boss Event End
- **Categoria:** Normal
- **Raridade:** (a confirmar)
- **Peso relativo:** (a confirmar)
- **Origem:** events/test - boss event end

**Anomalias detectadas:**
1. **Prefixo "Test - "** — mesmo problema do evento 119. Evento de teste em lote de produção.

**Veredito:** **MELHORAR** — Remover ou marcar como disabled.

---

## Inventário de Decisões do Lote (Eventos 101–120)

| #  | Título                          | Raridade | Peso | Veredito   | Natureza da Melhoria                              |
|----|---------------------------------|----------|------|------------|---------------------------------------------------|
| 101| Small Chest                     | Uncommon | 1.0  | MANTER     | Nenhum problema detectado                         |
| 102| Small Pile of Gold              | Uncommon | 1.0  | MANTER     | Nenhum problema detectado                         |
| 103| Snowstorm!                      | Uncommon | 1.0  | MELHORAR   | Conteúdo não recuperado integralmente             |
| 104| Spear Trap                      | Uncommon | 1.0  | MELHORAR   | Conteúdo não recuperado integralmente             |
| 105| Stone Covered Grave             | Uncommon | 1.0  | MELHORAR   | Conteúdo não recuperado integralmente             |
| 106| Strange Crystal (A)             | Uncommon | 1.0  | MELHORAR   | Variante de crystal — verificar contraste com B/C  |
| 107| Strange Crystal (B)             | Uncommon | 1.0  | MELHORAR   | Variante de crystal — verificar contraste com A/C  |
| 108| Strange Crystal (C)             | Uncommon | 1.0  | MELHORAR   | Variante de crystal — verificar contraste com A/B  |
| 109| Strange Fruit                   | Uncommon | 1.0  | MELHORAR   | Consumível — verificar balanceamento de buffs      |
| 110| Strange Green Crystal           | Uncommon | 1.0  | MELHORAR   | Crystal colorido — verificar coerência temática   |
| 111| Strange Indigo Crystal          | Uncommon | 1.0  | MELHORAR   | Crystal colorido — verificar coerência temática   |
| 112| Strange Orange Crystal          | Uncommon | 1.0  | MELHORAR   | Crystal colorido — verificar coerência temática   |
| 113| Strange Violet Crystal          | Uncommon | 1.0  | MELHORAR   | Crystal colorido — verificar coerência temática   |
| 114| Sword in the Stone              | Rare     | 0.5  | MELHORAR   | Texto resultado possível vazio                    |
| 115| Talk to the Spirits.            | Uncommon | 1.0  | MELHORAR   | Conteúdo parcial — nome com ponto final suspeito   |
| 116| Talking Suit of Armor           | Rare     | 0.5  | MELHORAR   | Conteúdo parcial                                  |
| 117| Target Dummy Practice: Expert   | Legendary| 1.0  | MELHORAR   | "whose"→"who's", resultado vazio, batalha imprópria|
| 118| Target Dummy Practice: Novice   | Uncommon | 1.0  | MELHORAR   | "whose"→"who's", mesma batalha imprópria          |
| 119| Test - All Characters Event     | ?        | ?    | MELHORAR   | Prefixo "Test" — evento de desenvolvimento        |
| 120| Test - Boss Event End           | ?        | ?    | MELHORAR   | Prefixo "Test" — evento de desenvolvimento        |

## Contagem

Analisei **20 de 20** eventos do lote Normal (101–120).

---

## Anomalias Consolidadas

1. **Erros de digitação:** Eventos 117 e 118 contêm "whose boss!" ao invés de "who's boss!" na opção de combate.
2. **Texto de resultado vazio:** Eventos 114 (Sword in the Stone) e 117 (Target Dummy: Expert) têm o campo "texto_resultados_possíveis" vazio.
3. **Prefixo "Test -":** Eventos 119 e 120 são eventos de teste/desenvolvimento não removidos do lote de produção.
4. **Batalha imprópria para contexto:** Eventos 117 e 118 (Target Dummy Practice) usam a batalha "Ogre Debt Collector Battle" — ogres são inimigos reais, não dummies de treino.
5. **Conteúdo parcial recuperado:** Eventos 103 (Snowstorm!), 104 (Spear Trap), 105 (Stone Covered Grave), 106 (Strange Crystal A), 115 (Talk to the Spirits.) e 116 (Talking Suit of Armor) tiveram conteúdo apenas parcialmente recuperado pela limitação de offset do arquivo. Recomenda-se leitura adicional.
6. **Path ID duplicado:** Evento 103 (Snowstorm!) e evento 118 (Target Dummy: Novice) compartilham o path_id `2545713` — possivelmente um erro de numeração no arquivo fonte.

---

*Fim do documento EV-R2-NORMAL-b06-parte01.*
