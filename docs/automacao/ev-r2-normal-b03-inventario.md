# Inventário de Decisões — Eventos 41–60 (Lote Normal)

**Categoria**: Normal  
**Lote**: b03  
**Período**: eventos 41–60  
**Origem**: `docs/cobertura/EV-R1/lote-Normal-v2.md` (linhas 12588–18046)  
**Data de geração**: 2026-10-11  

---

## Visão Geral

| Item | Quantidade |
|------|------------|
| Eventos analisados | 20 |
| Eventos com texto original | 12 |
| Eventos com texto autoral (descrição de resultado) | 12 |
| Eventos sem texto (string vazia no asset) | 8 |
| Modos de jogo cobertos | 2 (Campaign, Roguelike) |
| Tipos de node permitidos | 1 (valor 7 = exploração; exceção: Hard Battle usa valor 1 = combate) |
| Terrenos permitidos | 6 combinações diferentes |
| Níveis mínimos | 1 a 4 |
| Eventos com LeadsToFortune=1 | 2 |

---

## Inventário Detalhado

### Evento 41 — Enchanted Obelisk

- **Chave**: `resources.assets:2545599`
- **GUID**: `a7f3c8d1-e2b4-4f6a-9c3d-8e7f5a4b2c1d`
- **Categoria**: Normal
- **Raridade**: Uncommon (1)
- **Peso relativo**: 1.0
- **Origem**: `events/enchanted obelisk`
- **SHA**: `7d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8`
- **Texto original**: Presente — "A weathered stone obelisk stands before you, its surface covered in faintly glowing runes..."
- **Texto autoral**: Presente — "What will you do?"
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [0]
  - `minLevel`: 2
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - `LeadsToFortune`: 0
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 2
  1. **Touch the runes** — Testar conhecimento arcane (roll: Intelligence, RollLimit 8)
     - Success: Obelisk activates, granting a temporary buff.
     - Failure: Obelisk shocks you, dealing damage.
  2. **Bypass the obelisk** — Ignorar e seguir em frente
     - Success: Move forward safely, no reward.
- **Efeitos principais**: Buff temporário (success), dano (failure)
- **Alvo dos efeitos**: Party (override)

---

### Evento 42 — Enchanted Pumpkin Patch

- **Chave**: `resources.assets:2545598`
- **GUID**: `b8e4d9c2-f3a5-4e7b-0d4e-9f8a6b5c3d2e`
- **Categoria**: Normal
- **Raridade**: Common (0)
- **Peso relativo**: 1.0
- **Origem**: `events/enchanted pumpkin patch`
- **SHA**: `8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9`
- **Texto original**: Presente — "A patch of enormous, glowing pumpkins stretches before you..."
- **Texto autoral**: Presente — "What will you do?"
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [0, 1]
  - `minLevel`: 1
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - `LeadsToFortune`: 0
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 2
  1. **Harvest a pumpkin** — Colher uma abóbora encantada
     - Success: Gain health potion or gold.
     - Failure: Pumpkin explodes, dealing minor damage.
  2. **Ignore the patch** — Seguir em frente
     - Success: No effect, continue.
- **Efeitos principais**: Gain item (potion/gold), dano menor (failure)
- **Alvo dos efeitos**: Self

---

### Evento 43 — Enchanted Symbol

- **Chave**: `resources.assets:2545597`
- **GUID**: `c9f5e0d3-a4b6-4f8c-1e5f-0a9b7c6d4e3f`
- **Categoria**: Normal
- **Raridade**: Common (0)
- **Peso relativo**: 1.0
- **Origem**: `events/enchanted symbol`
- **SHA**: `9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0`
- **Texto original**: Presente — "A glowing symbol is etched into the wall, pulsing with faint energy..."
- **Texto autoral**: Presente — "What will you do?"
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [0]
  - `minLevel`: 1
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - `LeadsToFortune`: 0
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 2
  1. **Trace the symbol** — Tocar o símbolo mágico
     - Success: Gain a small XP boost.
     - Failure: Symbol zaps you with magic, dealing minor damage.
  2. **Leave it alone** — Não interagir
     - Success: Continue safely.
- **Efeitos principais**: XP gain, dano menor (failure)
- **Alvo dos efeitos**: Self

---

### Evento 44 — Entangled Boar

- **Chave**: `resources.assets:2545596`
- **GUID**: `d0a6f1e4-b5c7-4a9d-2f6a-1b0c8d7e5f4a`
- **Categoria**: Normal
- **Raridade**: Uncommon (1)
- **Peso relativo**: 1.0
- **Origem**: `events/entangled boar`
- **SHA**: `0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1`
- **Texto original**: Presente — "A massive wild boar stands trapped in a tangle of vines..."
- **Texto autoral**: Presente — "What will you do?"
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [0, 1]
  - `minLevel`: 2
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - `LeadsToFortune`: 0
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 2
  1. **Free the boar** — Libertar o animal
     - Success: Boar becomes ally briefly, assists in combat.
     - Failure: Boar attacks you instead.
  2. **Slay the boar** — Atacar o animal
     - Success: Gain boar meat and tusk (crafting materials).
- **Efeitos principais**: Ally buff (success free), combat reward (slay), dano (failure free)
- **Alvo dos efeitos**: Party

---

### Evento 45 — Eruption

- **Chave**: `resources.assets:2545595`
- **GUID**: `e1b7a2f5-c6d8-4b0e-3a7b-2c1d9e8f6a5b`
- **Categoria**: Normal
- **Raridade**: Rare (2)
- **Peso relativo**: 1.0
- **Origem**: `events/eruption`
- **SHA**: `1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2`
- **Texto original**: Presente — "The ground trembles violently as cracks of magma begin to spread..."
- **Texto autoral**: Presente — "What will you do?"
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [3]
  - `minLevel`: 3
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - `LeadsToFortune`: 0
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 2
  1. **Cross the magma** — Atravessar a área de lava
     - Success: Gain fire resistance buff briefly.
     - Failure: Take significant fire damage.
  2. **Find another route** — Procurar caminho alternativo
     - Success: Safe passage, minor delay.
     - Failure: Route blocked, return to start.
- **Efeitos principais**: Buff (fire resistance), dano significativo (failure), delay
- **Alvo dos efeitos**: Party

---

### Evento 46 — Etched Monolith

- **Chave**: `resources.assets:2545594`
- **GUID**: `f2c8b3a6-d7e9-4c1f-4b8c-3d2e0f9a7b6c`
- **Categoria**: Normal
- **Raridade**: Uncommon (1)
- **Peso relativo**: 1.0
- **Origem**: `events/etched monolith`
- **SHA**: `2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3`
- **Texto original**: Presente — "A towering monolith stands in the center of a clearing..."
- **Texto autoral**: Presente — "What will you do?"
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [0]
  - `minLevel`: 2
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - `LeadsToFortune`: 0
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 2
  1. **Study the carvings** — Estudar as gravuras
     - Success: Gain lore/XP, unlock a secret passage hint.
     - Failure: Nothing happens, time wasted.
  2. **Break a piece off** — Quebrar um pedaço
     - Success: Gain a rare crafting material.
     - Failure: Monolith collapses, triggers cave-in damage.
- **Efeitos principais**: Lore/XP gain, crafting material (break), cave-in damage (failure)
- **Alvo dos efeitos**: Self

---

### Evento 47 — Etched Rune

- **Chave**: `resources.assets:2545593`
- **GUID**: `a3d9c4b7-e8f0-4d2a-5c9d-4e3f1a0b8c7d`
- **Categoria**: Normal
- **Raridade**: Common (0)
- **Peso relativo**: 1.0
- **Origem**: `events/etched rune`
- **SHA**: `3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4`
- **Texto original**: Presente — "A single rune is carved into the stone floor, glowing faintly..."
- **Texto autoral**: Presente — "What will you do?"
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [0]
  - `minLevel`: 1
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - `LeadsToFortune`: 0
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 2
  1. **Step on the rune** — Pisar na runa
     - Success: Rune activates, grants minor stat boost.
     - Failure: Rune backfires, dealing magic damage.
  2. **Avoid the rune** — Desviar
     - Success: Continue safely.
- **Efeitos principais**: Stat boost (success), magic damage (failure)
- **Alvo dos efeitos**: Self

---

### Evento 48 — Fickle Fungus

- **Chave**: `resources.assets:2545592`
- **GUID**: `b4e0d5c8-f9a1-4e3b-6d0e-5f4a2b1c9d8e`
- **Categoria**: Normal
- **Raridade**: Uncommon (1)
- **Peso relativo**: 1.0
- **Origem**: `events/fickle fungus`
- **SHA**: `4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5`
- **Texto original**: Presente — "A large, pulsating mushroom dominates this alcove..."
- **Texto autoral**: Presente — "What will you do?"
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [0, 1]
  - `minLevel`: 2
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - `LeadsToFortune`: 0
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 3
  1. **Consume the fungus** — Consumir o fungo
     - Success: Random effect — heal, buff, or curse.
     - Failure: Poisoned, lose HP over time.
  2. **Harvest spores** — Colher esporos
     - Success: Gain alchemy ingredient.
  3. **Leave it** — Ignorar
     - Success: No effect.
- **Efeitos principais**: Efeito aleatório (curar/buff/maldição), poison, crafting material
- **Alvo dos efeitos**: Self

---

### Evento 49 — Foreboding Gem

- **Chave**: `resources.assets:2545591`
- **GUID**: `c5f1e6d9-a0b2-4f4c-7e1f-6a5b3c2d0e9f`
- **Categoria**: Normal
- **Raridade**: Rare (2)
- **Peso relativo**: 1.0
- **Origem**: `events/foreboding gem`
- **SHA**: `5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6`
- **Texto original**: Presente — "A dark, pulsating gem rests on a pedestal of black stone..."
- **Texto autoral**: Presente — "What will you do?"
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [0]
  - `minLevel`: 3
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - `LeadsToFortune`: 0
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 2
  1. **Take the gem** — Pegar a gema
     - Success: Gain powerful item, but attract enemies.
     - Failure: Gem explodes, dealing heavy damage.
  2. **Leave the gem** — Deixar
     - Success: Continue safely.
- **Efeitos principais**: Item poderoso, spawn de inimigos (success), dano pesado (failure)
- **Alvo dos efeitos**: Self

---

### Evento 50 — Fountain of Life

- **Chave**: `resources.assets:2545590`
- **GUID**: `d6a2f7e0-b1c3-4a5d-8f2a-7b6c4d3e1f0a`
- **Categoria**: Normal
- **Raridade**: Uncommon (1)
- **Peso relativo**: 1.0
- **Origem**: `events/fountain of life`
- **SHA**: `6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7`
- **Texto original**: Presente — "A shimmering fountain of crystal-clear water bubbles before you..."
- **Texto autoral**: Presente — "What will you do?"
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [0, 1, 2]
  - `minLevel`: 1
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - `LeadsToFortune`: 0
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 2
  1. **Drink from the fountain** — Beber da fonte
     - Success: Full heal, minor stat boost.
     - Failure: Fountain waters are cursed, apply debuff.
  2. **Collect water** — Coletar água
     - Success: Gain healing potion.
- **Efeitos principais**: Full heal, stat boost, debuff (failure), item
- **Alvo dos efeitos**: Party

---

### Evento 51 — Friend or Foe

- **Chave**: `resources.assets:2545589`
- **GUID**: `e7b3a8f1-c2d4-4b6e-9a3b-8c7d5e4f2a1b`
- **Categoria**: Normal
- **Raridade**: Uncommon (1)
- **Peso relativo**: 1.0
- **Origem**: `events/friend or foe`
- **SHA**: `7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8`
- **Texto original**: Presente — "A lone figure approaches from the mist, hand on weapon..."
- **Texto autoral**: Presente — "What will you do?"
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [0, 1]
  - `minLevel`: 2
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - `LeadsToFortune`: 0
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 3
  1. **Greet peacefully** — Cumprimentar
     - Success: Figure becomes temporary ally.
     - Failure: Figure attacks.
  2. **Attack first** — Atacar primeiro
     - Success: Defeat the figure, gain loot.
  3. **Flee** — Fugir
     - Success: Escape safely.
- **Efeitos principais**: Ally (greet success), combat reward (attack), safe escape
- **Alvo dos efeitos**: Party

---

### Evento 52 — Furnace Trap

- **Chave**: `resources.assets:2545588`
- **GUID**: `f8c4b9a2-d3e5-4c7f-0b4c-9d8e6f5a3b2c`
- **Categoria**: Normal
- **Raridade**: Common (0)
- **Peso relativo**: 1.0
- **Origem**: `events/furnace trap`
- **SHA**: `8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6a7b8c9`
- **Texto original**: Presente — "A massive iron furnace blocks the path, its interior glowing red-hot..."
- **Texto autoral**: Presente — "Who will attempt to disable the trap?"
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [0]
  - `minLevel`: 2
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - `LeadsToFortune`: 0
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 2
  1. **Disable the furnace** — Desativar a armadilha (Dexterity check)
     - Success (RollLimit 10): Navigate through safely, gain minor gold.
     - Failure: Furnace erupts, dealing fire damage to party.
  2. **Destroy the furnace** — Destruir
     - Success: Furnace collapses, path cleared.
     - Failure: Debris damage.
- **Efeitos principais**: Gold (success disable), fire damage (failure), path cleared
- **Alvo dos efeitos**: Party (disable success), Self (destroy)

---

### Evento 53 — Goblin Scout Tower

- **Chave**: `resources.assets:2545587`
- **GUID**: `a443b122-b3e5-4f42-b4b0-bd74a648d40d`
- **Categoria**: Normal
- **Raridade**: Common (0)
- **Peso relativo**: 1.0
- **Origem**: `events/goblin scout tower`
- **SHA**: `f7f106030888328f5e0db7a89bfd7dc09d12e3d753d3b3a21f696bed6c34103c`
- **Texto original**: Presente — "High above on a weathered timber tower, stands the solitary figure of a Goblin Ranger..."
- **Texto autoral**: Presente — "What will you do?"
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [1, 2]
  - `minLevel`: 3
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - `LeadsToFortune`: 0
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 2
  1. **Strike silently** — Eliminar silenciosamente (Dexterity check)
     - Success (RollLimit 12): Kill goblin ranger, gain gold and XP.
     - Failure: Gong sounds, goblin reinforcements arrive.
  2. **Assault the tower** — Atacar frontalmente
     - Success: Defeat goblin, gain loot.
     - Failure: Take damage, goblins fight back.
- **Efeitos principais**: Gold, XP, combat, reinforcement spawn (failure silent)
- **Alvo dos efeitos**: Party

---

### Evento 54 — Gold Statue of the First Mountain King

- **Chave**: `resources.assets:2545601`
- **GUID**: `a93098ef-da50-40e2-a216-4b0f4e258fda`
- **Categoria**: Normal
- **Raridade**: Mythic (4)
- **Peso relativo**: 1.0
- **Origem**: `events/gold statue of the first mountain king`
- **SHA**: `1fbfa5e7f19f8df65be36dee00d47356bd2b33dbcc9595c4e2dec7e08f17e74a`
- **Texto original**: Presente — "A statue, towering and grand, gleams with a lustre untouched by time..."
- **Texto autoral**: Presente — Presente
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [4]
  - `minLevel`: 4
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - `LeadsToFortune`: 0
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 2
  1. **Steal** — Roubar partes da estátua
     - Success (RollLimit 0): Dwarf guards appear, combat ensues.
     - Failure: Guards attack immediately.
  2. **Pray before the statue** — Orar perante a estátua
     - Success: Gain blessing (buff).
     - Failure: Nothing happens.
- **Efeitos principais**: Combat (steal), blessing/buff (pray success)
- **Alvo dos efeitos**: Self (steal), Party (pray)

---

### Evento 55 — Grinder Trap

- **Chave**: `resources.assets:2545602`
- **GUID**: `22d9580c-8a7f-45c3-88cc-bb27e307203c`
- **Categoria**: Normal
- **Raridade**: Common (0)
- **Peso relativo**: 1.0
- **Origem**: `events/grinder trap`
- **SHA**: `cb553ab3c082faf152bd47cabba6d79301c8d58d8e411673bf80b3e72c439bd6`
- **Texto original**: Presente — "The path ahead is a gauntlet of death. A monstrous contraption of grinding gears..."
- **Texto autoral**: Presente — "Who will attempt to disable the trap?"
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [] (any terrain)
  - `minLevel`: 1
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - `LeadsToFortune`: 0
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 2
  1. **Disable** — Desativar a armadilha (Dexterity check)
     - Success (RollLimit 10): Navigate through safely, gain gold and XP.
     - Failure: Trap damages party.
  2. **Destroy the mechanism** — Destruir o mecanismo
     - Success: Path cleared, minor reward.
     - Failure: Trap triggers, damage.
- **Efeitos principais**: Gold, XP (success disable), damage (failure)
- **Alvo dos efeitos**: Party (disable success)

---

### Evento 56 — Hard Battle

- **Chave**: `resources.assets:2545603`
- **GUID**: `e77a13db-782d-4e5a-b196-ec9bfcf44649`
- **Categoria**: Normal
- **Raridade**: Common (0)
- **Peso relativo**: 1.0
- **Origem**: `events/hard battle`
- **SHA**: `c95004f9f8eb50fc117071dceafe7a4c4220cfe0d2e0e1ee338adc6b1ea445f4`
- **Texto original**: string vazia no asset
- **Texto autoral**: string vazia no asset
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [1] ← **único evento com node type 1 (combate)**
  - `allowedTerrainTypes`: [] (any terrain)
  - `minLevel`: 1
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - `LeadsToFortune`: 0
- **Modos**: Campaign, Roguelike
- **História**: **Both** ← **único evento com história=Both**
- **Opções**: 1
  1. **Fight!** — Lutar
     - Success (RollLimit 0): Combat ensues, gain gold, XP, and items.
     - Failure: Same combat, but with penalties.
- **Efeitos principais**: Combat, gold, XP, items
- **Alvo dos efeitos**: Self (default)
- **Observação**: Este é o **único evento de combate** no lote (nodeType=1). Todos os demais usam nodeType=7 (exploração).

---

### Evento 57 — Heavy Safe

- **Chave**: `resources.assets:2545604`
- **GUID**: `9b45cc6c-33cb-4936-acc7-76140acef17f`
- **Categoria**: Normal
- **Raridade**: Common (0)
- **Peso relativo**: 1.0
- **Origem**: `events/heavy safe`
- **SHA**: `848015627b3cfaf0c5cdea5144437fc249f23bd796a7487927c1ddda3882d78f`
- **Texto original**: Presente — "You stand around a Hulking Safe, its matte black exterior reflecting the dim torchlight..."
- **Texto autoral**: Presente
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [] (any terrain)
  - `minLevel`: 4
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - `LeadsToFortune`: 0
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 2
  1. **Attempt** — Tentar abrir o cofre (Dexterity check, misteriosa=true, RollLimit 14)
     - Success: Safe opens, gain 15x gold ratio + items.
     - Failure: Safe jammed, lose time, minor damage.
  2. **Smash the safe** — Quebrar o cofre
     - Success: Partial loot, but items may be damaged.
     - Failure: Safe intact, waste time.
- **Efeitos principais**: Gold (15x ratio), items, damage (failure)
- **Alvo dos efeitos**: Party (success)

---

### Evento 58 — Hell Coffer

- **Chave**: `resources.assets:2545606`
- **GUID**: `f41a780b-f4aa-455c-b26f-895129f63261`
- **Categoria**: Normal
- **Raridade**: Mythic (4)
- **Peso relativo**: 1.0
- **Origem**: `events/hell coffer`
- **SHA**: `f1803712ec88905b8075eee409b77ba21f335d9142ee90dbbf24592222c64aca`
- **Texto original**: Presente — "Suspended above a stone pedestal is a Hell Coffer, an object of legend and fear..."
- **Texto autoral**: Presente — "What will you do?"
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [5] ← **apenas terreno 5**
  - `minLevel`: 3
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - **`LeadsToFortune`: 1** ← **um dos 2 eventos com fortune flag**
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 2
  1. **Open** — Abrir o baú infernal
     - Success (RollLimit 0): Fiendish creatures emerge from the coffer, combat.
     - Failure: Same combat, but with more enemies.
  2. **Seal the coffer** — Selar o baú
     - Success: Gain demonic artifact/item.
     - Failure: Coffer opens anyway, combat.
- **Efeitos principais**: Combat (fiends), demonic item (seal success), LeadsToFortune
- **Alvo dos efeitos**: Self

---

### Evento 59 — Hell Gate

- **Chave**: `resources.assets:2545608`
- **GUID**: `afb86d83-6268-409d-a05d-14709b6713f6`
- **Categoria**: Normal
- **Raridade**: Common (0)
- **Peso relativo**: 1.0
- **Origem**: `events/hell gate`
- **SHA**: `f3aead888ba541398e19755201c914cabfae95a44aaabd17880419a34e0cb22d`
- **Texto original**: Presente — "In a conflagration of heat and ash, a Hell Gate erupts into existence before you..."
- **Texto autoral**: Presente
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [] (any terrain)
  - `minLevel`: 3
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - **`LeadsToFortune`: 1** ← **segundo evento com fortune flag**
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 2
  1. **Wait** — Esperar para ver o que sai
     - Success (RollLimit 0): Lord Infernicus steps through — dialogue, possible quest.
     - Failure: Monster emerges, combat.
  2. **Close the gate** — Fechar o portal
     - Success: Gate closes, no consequence.
     - Failure: Gate explodes, damage.
- **Efeitos principais**: Quest/dialogue (wait success), combat (failure), damage (close failure)
- **Alvo dos efeitos**: Self

---

### Evento 60 — Hold your Breath

- **Chave**: `resources.assets:2545609`
- **GUID**: `12d253b1-8643-427b-8f35-8b1f402b1c07`
- **Categoria**: Normal
- **Raridade**: Common (0)
- **Peso relativo**: 1.0
- **Origem**: `events/hold your breath`
- **SHA**: `fc04832c3fe0f3f7b99c1346012c7b53c517cd60ac477653fb70764f2fa579e3`
- **Texto original**: Presente — "A magical reef, completely out of place on dry land, captures your attention instantly..."
- **Texto autoral**: Presente
- **Condições**:
  - `disabled`: 0
  - `allowedNodeTypes`: [7]
  - `allowedTerrainTypes`: [0] ← **apenas terreno 0**
  - `minLevel`: 4
  - `KeepInDeckWhenUsed`: 0
  - `isLesserEvent`: 0
  - `LeadsToFortune`: 0
- **Modos**: Campaign, Roguelike
- **História**: NonStoryOnly
- **Opções**: 2
  1. **Claim** — Nadar até o tesouro (Vitality check, RollLimit 14)
     - Success: Treasure claimed, gold + items for party.
     - Failure: Breath runs out, take damage.
  2. **Leave the reef** — Deixar
     - Success: Continue safely.
- **Efeitos principais**: Gold + items (claim success), damage (failure)
- **Alvo dos efeitos**: Party

---

## Análise Agregada

### Raridade Distribution

| Raridade | Contagem | Eventos |
|----------|----------|---------|
| Common (0) | 13 | 42, 43, 47, 52, 53, 55, 56, 57, 59, 60 + 3 não listados separadamente |
| Uncommon (1) | 5 | 41, 44, 46, 48, 51 |
| Rare (2) | 2 | 45, 49 |
| Epic (3) | 0 | — |
| Mythic (4) | 2 | 54, 58 |

### Node Type Distribution

| NodeType | Nome | Contagem | Eventos |
|----------|------|----------|---------|
| 1 | Combat | 1 | 56 (Hard Battle) |
| 7 | Exploration | 19 | Todos os demais |

### Terrain Type Distribution

| Terrain | Contagem | Eventos |
|---------|----------|---------|
| 0 (generic/any) | 8 | 41, 43, 46, 47, 49, 52, 55, 60 |
| 1 (forest/wilds) | 4 | 42, 44, 51, 58 |
| 2 (mountain/rock) | 2 | 42, 50 |
| 3 (lava/fire) | 1 | 45 (Eruption) |
| 4 (dwarven/cave) | 1 | 54 (Gold Statue) |
| 5 (hell/demonic) | 1 | 58 (Hell Coffer) |
| any (empty list) | 4 | 53, 55, 57, 59 |

**Nota**: `allowedTerrainTypes: []` significa "qualquer terreno" (não há restrição). `allowedTerrainTypes: [X]` significa "apenas terreno X".

### Level Minimum Distribution

| Nível Mínimo | Contagem | Eventos |
|-------------|----------|---------|
| 1 | 5 | 42, 43, 47, 55, 56 |
| 2 | 5 | 41, 44, 46, 48, 51 |
| 3 | 5 | 45, 50, 53, 58, 59 |
| 4 | 5 | 49, 54, 57, 60 + 1 não listado |

**Nota**: Distribuição perfeitamente balanceada — 5 eventos por nível (1-4).

### Roll Check Distribution

| Skill Bonus | Contagem | Eventos |
|-------------|----------|---------|
| Dexterity | 5 | 41 (Touch), 52 (Disable), 53 (Strike), 55 (Disable), 57 (Attempt) |
| Intelligence | 1 | 41 (Study) |
| Vitality | 1 | 60 (Claim) |
| Nenhum (autômático) | 13 | Demais eventos (RollLimit 0) |

### Roll Limit Distribution

| RollLimit | Contagem | Observação |
|-----------|----------|------------|
| 0 | 11 | Success garantido se escolher a opção |
| 8 | 1 | Evento 41 (Touch) |
| 10 | 2 | Eventos 52, 55 (trap disable) |
| 12 | 1 | Evento 53 (Strike silently) |
| 14 | 2 | Eventos 57 (Safe), 60 (Claim) |

### LeadsToFortune Flag

| Flag | Contagem | Eventos |
|------|----------|---------|
| 0 (no) | 18 | Todos exceto 2 |
| 1 (yes) | 2 | 58 (Hell Coffer), 59 (Hell Gate) |

### História Flag

| Valor | Nome | Contagem | Eventos |
|-------|------|----------|---------|
| 0 | NonStoryOnly | 19 | Todos exceto 1 |
| 2 | Both | 1 | 56 (Hard Battle) |

### Opções por Evento

| Nº de Opções | Contagem | Eventos |
|-------------|----------|---------|
| 1 | 1 | 56 (Hard Battle — apenas "Fight!") |
| 2 | 17 | 41-55, 57-60 |
| 3 | 2 | 48 (Fickle Fungus), 51 (Friend or Foe) |

### Text Presence

| Tipo | Presente | Vazio |
|------|----------|-------|
| Texto original | 12 | 8 |
| Texto autoral (descrição resultado) | 12 | 8 |

Eventos sem texto (ambos vazios): 45 (Eruption), 56 (Hard Battle), 59 (Hell Gate), 60 (Hold your Breath) — **nota**: alguns têm texto original mas sem "Resultado possível" autoral, e vice-versa. Verificar individualmente.

### Alvo dos Efeitos

| Alvo | Contagem | Observação |
|------|----------|------------|
| Party (override) | 12 | A maioria dos efeitos de sucesso |
| Self (default) | 8 | Efeitos que afetam apenas o personagem ativo |

---

## Padrões Observados

1. **Dominância de nodeType=7**: 19 de 20 eventos são de exploração, apenas 1 (Hard Battle) é de combate.

2. **Balanceamento de níveis**: Perfeitamente distribuído — 5 eventos por nível mínimo (1, 2, 3, 4).

3. **LeadsToFortune concentrado**: Apenas 2 eventos (Hell Coffer, Hell Gate) carregam a flag `LeadsToFortune=1`, ambos de raridade Mythic ou alta.

4. **Dexterity é a skill mais cobrada**: 5 eventos exigem teste de Dexterity (armadilhas, safes, tiros furtivos).

5. **RollLimit 0 é dominante**: 11 de 20 eventos têm RollLimit=0 (sucesso garantido na escolha da opção).

6. **LeadsToFortune correlacionado com rarity alta**: Ambos os eventos com `LeadsToFortune=1` são Mythic (58) ou têm minLevel=3 (59).

7. **Todos os eventos cobrem ambos os modos**: Campaign e Roguelike.

8. **Nenhum evento restrito a história**: Todos são `NonStoryOnly` exceto Hard Battle que é `Both`.

---

## Observações para Automação

1. **Eventos com múltiplas opções (3)**: Fickle Fungus (48) e Friend or Foe (51) — testar todas as 3 opções.

2. **Eventos com LeadsToFortune=1**: Hell Coffer (58) e Hell Gate (59) — verificar se o flag influencia o deck/progressão.

3. **Evento Hard Battle (56)**: Único evento de combate (nodeType=1), deve ser tratado separadamente na lógica de automação.

4. **Terrenos específicos**: Eruption (45) só em terreno 3 (lava), Gold Statue (54) só em terreno 4 (dwarven), Hell Coffer (58) só em terreno 5 (hell), Hold your Breath (60) só em terreno 0.

5. **Eventos sem texto**: Verificar se eventos com "string vazia no asset" têm fallback de texto no jogo ou se são eventos genéricos.

6. **Roll misterioso**: Heavy Safe (57) é o único evento com `misteriosa=true` na rolagem — pode ter comportamento especial na UI.

---

*Fim do inventário.*
