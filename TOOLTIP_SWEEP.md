# Varredura de Tooltips — Stolen Realm (BetterTooltips)

## RV-7 — Life Steal em triangulação (em andamento)

**Status das fontes:**
- Patch notes MAIS RECENTES (v1.3.1, 15/09/2026): sem mudanças em Life Steal → vale o rework do **v0.22**: "Player Life Steal reworked: Now heals a percentage of the player's **Max Health** when hitting. Reduced for AOE." (antes disso era % do dano causado)
- Localização ATUAL do jogo: "Life Steal **heals you for a percentage of your Max Health** each time you hit. Reduced for area of effect abilities." ✓
- Código (`Character.ApplyAction`): o bloco de lifesteal calcula `vida perdida do ALVO × LifeSteal% × multiplicador de nível` (base = dano) — conflita com as fontes oficiais
- **Teste empírico instrumentado**: `[LifeSteal]` + `[Dmg]` no RoguelikeDebugger — uma batalha decide
- Texto do glossário = redação oficial do jogo (pendente do resultado empírico)

## Regra de fonte de verdade

Patch notes oficiais são fonte da verdade; usar sempre a versão **mais recente** (atual: v1.3.1 — 15/09/2026). Divergência entre fontes → código observado vence.

## RV-8 — Auditoria completa de correção (pós-Life Steal) — CONCLUÍDA ✓

Método: 4 camadas de verificação — (1) chaves exatas no banco de localização atual, (2) código atual, (3) notas v1.3.1 completas, (4) dumps ao vivo do build instalado.

| Grupo | Verificação | Status |
|---|---|---|
| Powerups (todas as chaves) | varredura resources.assets | ✓ presentes no build atual |
| Efeitos por atributo (Might/Dex/Int/Vit/Reflex) | batem com `ShowMainStatTooltip` atual | ✓ |
| Skill Tree Removal | `MinimumTreesRemaining=4` + lock nível 1 no código atual | ✓ (frase final é edição do usuário) |
| Treasure/Gold/Damage/Movement/Range/Summon | notas v1.3.1 completas | ✓ nada invalidado |
| Armor (cap) | dinâmico — lê `maxArmorReductionPercent` ao vivo (99% desde v0.22; wiki diz 80% = desatualizada) | ✓ correto por construção |
| Resistência negativa | fórmula atual | ✓ |
| Chaves BT-6/7/8 (status/skills/itens) | dumps coletados do build instalado | ✓ atuais por construção |
| **Life Steal** | **era o único erro — corrigido e confirmado empiricamente** | ✓ |





> **Objetivo**: tooltip informativo e detalhado para TODA mecânica/spell/item — explicando COMO funciona de fato, não só traduzindo ou estendendo o texto.
> **Regra de ouro**: mecânica SEMPRE confirmada no código (ILSpy/Cecil) + log de validação (RoguelikeDebugger) ANTES de escrever o texto. Zero invenção.
> **Legenda de status**: 🔍 investigar · ✅ mecânica verificada · ✍️ texto escrito · ✔️ validado em jogo

## Metodologia de revisão externa (RV-x)

Cada fase, após os textos escritos, passa por revisão contra a comunidade:

1. **Fontes**: Wiki oficial/Fandom, Discord oficial do jogo, Reddit (r/StolenRealm etc.), patch notes (Steam), guias Steam, mods open-source no Thunderstore/GitHub.
2. **Triangulação**: nenhum comentário único da internet vale por si. Uma afirmação só entra se:
   - for corroborada por ≥2 fontes independentes, E
   - fizer sentido com as demais informações conhecidas, E
   - for coerente com o comportamento observado no código/teste do jogo.
3. **Divergência**: o código do jogo vence. Marcar a divergência na tabela com nota.
4. **Saída**: tabela por tooltip com status de revisão (✔️ confirmado por múltiplas fontes · ⚠️ fonte única/divergente · ✖️ contradiz o código) e as fontes citadas.

## Resultados RV-1 (primeira passada — 28/09)

Fontes usadas: Fandom Wiki (Power ups, Roguelike, Character Attributes), Prima Games, guia Steam, código decompilado. Regra aplicada: ≥2 fontes independentes + coerência com código; código vence.

| Powerup | Status | Fontes/notas |
|---|---|---|
| Might/Dex/Int/Vit/Reflex | ✔️ | Ladder 3/6/9/12/15: Fandom ✓. Efeitos por ponto: Fandom Character Attributes + código (GlobalSettings) — estrutura idêntica. **Divergência**: wiki v0.13.1 diz range +1/25 Int máx. 5; código atual diz máx. 3 → seguimos o código |
| Attribute Points | ✔️ | Prima ("attribute points per level +1") + código |
| Damage and Healing | ✔️ | Prima ("damage + healing") + código (DamageMod base) |
| Damage Reduction | ⚠️ | Código (camada multiplicativa). Comunidade sem detalhe específico; nenhuma contradição |
| Movement | ✔️ | Prima ("move more than once per turn") + código (FreeMovementPoints) |
| Range | ✔️ | Prima ("hit enemies further") + código |
| Skill Options | ✔️ | Fandom Roguelike ("1 de 4 skills, até 6 com powerups" = +1/+2) + código |
| Resists | ✔️ | Guia Steam ("Heat reduz resistências em 5%/stack"; "Guardian dá resistência física %") + código (dano × (1-Resist/100)) |
| Gold Find | ✔️ | Prima ("find more gold") + código (GoldMod × ouro) |
| Treasure Find | ✔️ | Prima ("increasing the probability of encountering treasures" — chance, NÃO raridade) + código (drop chance × mod; raridade inalterada). Nenhuma fonte comunitária alega mudança de raridade |
| Summon Damage & Health | ⚠️ | Código (SummonDamageMod/SummonHealthMod). Comunidade sem detalhe; sem contradição |
| Skill Tree Removal | ⚠️ | Código (mín. 4 árvores; só nível 1 — texto do próprio jogo). Comunidade sem detalhe |

Nenhuma fonte comunitária **contradiz** qualquer texto publicado. Itens ⚠️ podem ganhar segunda passada se/quando a comunidade documentar.

---

## Fase 1 — Tooltips do menu: Powerups do Roguelike (BT-5)

Fonte: janela de powerup (`Tooltip.ShowRoguelikePowerupTooltip` → `Localize(RoguelikePowerupLevel.Description)`).
Inventário completo extraído do banco de localização (19 powerups, 70 chaves):

| # | Powerup | Níveis | Status | Notas da mecânica (a verificar) |
|---|---|---|---|---|
| 1 | Might | +3/+6/+9/+12/+15 | ✅✍️ | efeitos por ponto espelhados do tooltip de stats (valores dinâmicos do GlobalSettings) |
| 2 | Dexterity | +3/+6/+9/+12/+15 | ✅✍️ | idem (crit rating/damage, movimento) |
| 3 | Intelligence | +3/+6/+9/+12/+15 | ✅✍️ | idem (mana, range, summon health) |
| 4 | Vitality | +3/+6/+9/+12/+15 | ✅✍️ | idem (max health) |
| 5 | Reflex | +3/+6/+9/+12/+15 | ✅✍️ | idem (dodge, counter/opportunity attacks) |
| 6 | Attribute Points | +1/+2/+3 por nível | ✅✍️ | `AdditionalRoguelikeAttributesPointsPerLevel` → +N pontos por level-up |
| 9 | Movement | +1/+2 | ✅✍️ | atributo `FreeMovementPoints` → movimento por turno |
| 10 | Range | +1/+2 | ✅✍️ | alimenta `RangeTypeAdderRanged` apenas (dump: Melee=0, Ranged=2 no Lv2) — texto diz "ranged attacks" |
| 11 | Skill Options | +1/+2 | ✅✍️ | `AdditionalRoguelikeSkillOptions` → mais opções de skill no level-up |
| 7 | Damage and Healing | +5/10/15/20/25% | ✅✍️ | soma no `DamageMod` base → todos os tipos + cura (fórmula `(1+(DM+tipo+ManaPower)/100)×(1+AP/100)`) |
| 8 | Damage Reduction | +4/8/12/16/20% | ✅✍️✔️ | camada multiplicativa `(1-(DR+Resilience+Cover)/100)`; empírico: DR=20 no Lv5 (sessão com -5 era debuff transiente em combate) |
| 12 | Resist Cold | +10/15/20% | ✅✍️ | `dano × (1-Resist/100)` por elemento (camada multiplicativa) |
| 13 | Resist Fire | +10/15/20% | ✅✍️ | idem |
| 14 | Resist Lightning | +10/15/20% | ✅✍️ | idem |
| 15 | Resist Physical | +10/15/20% | ✅✍️ | idem |
| 16 | Increased Gold Find | +10/20/30/40/50% | ✅✍️ | `GoldMod` somado à party × ouro (batalha/quest/evento) — validar em jogo |
| 17 | Treasure Find | +20/40/60/80/100% | ✅✍️✔️ | `DropQuantityMod` × chance de drop; NÃO afeta raridade |
| 18 | Summon Damage & Health | +5/10/15/20/25% | ✅✍️ | atributos `SummonDamageMod`/`SummonHealthMod` |
| 19 | Skill Tree Removal | +1..+8 | ✅✍️ | remove árvores do pool de escolhas (mín. 4 restam); só nível 1 |

**Plano BT-5**: um powerup por vez — investigar mecânica no código → escrever explicação → validar.

---

## Fase 2 — Efeitos/status + Spells/Skills (BT-6 e BT-7)

**Inventário completo coletado** (28/09, dump do RoguelikeDebugger): **600 statuses** — 497 Normal, 83 Fortune, 14 Quest, 6 QuestItem (lista em `STATUS_INVENTORY.md`) — e **453 skills** em 14 árvores (lista em `SKILL_INVENTORY.md`).

### BT-6 (statuses) — implementada
- 6a: statuses de atributo → efeitos por ponto dinâmicos
- 6b: statuses de resistência → mecânica de resistência negativa
- 6c: fortunes de atributo → efeitos por ponto
- 6d: quest/questitem → avaliados, sem mudança

### BT-7 (skills) — implementada
- 7a: glossário Stealth (crit 100%) e Marked Prey (+10% dano tomado/stack)
- 7b: glossário Enrage (imune a movement impairing/knockback), Life Steal (cura % do dano)
- 7c: varredura das 453 descrições — 31 curtas avaliadas; Chaos já explica o dano aleatório; Helping/Hurting são caóticas por design
- **REGRA: nada de Bard/música** (Crescendo, Harmony, Songs removidos do glossário — Bard chega na próxima atualização do jogo)
- Pendências anotadas: summon scaling (verificar em runtime, RD-1); "AP cost" vs "Action" (RV-6); Coin of Chaos (críptica por design)

Candidatos já mapeados no código (a inventariar por completo):
- `Tooltip.ShowActionStatusTooltip` (ActionStatusInfo → AttributeEffects)
- `ActionStatusTooltip`, `Tooltip.GetLocalizedDurationText`
- `SkillTooltip`, `SkillInfo` (skills com PassiveActionStatuses)
- `Character.ApplyAction` / `ApplyActionMeasured` (cálculo de dano/efeitos)

## Fase 3 — Equipamentos/Itens (BT-8)

**Inventários completos** (28/09): **905 itens base** (`ITEM_INVENTORY.md`) e **285 afixos** (`ITEM_MOD_INVENTORY.md` — 192 prefixos, 90 sufixos, 3 EndGame).

Implementado:
- **Armor** (32 afixos): nota dinâmica com a fórmula do código — `dano - Armor/N` com cap `maxArmorReductionPercent` (valores do GlobalSettings)
- **Resist** (27 afixos): sufixo da mecânica de resistência (reuso da BT-6b)
- **Lifesteal** (1 afixo): coberto automaticamente pela regra de glossário Life Steal
- Guardas anti-colisão: só textos com verbo de modificação; "Summon resistance" excluído (não é resistência de dano)

Pendências: validação visual; RV-4 (revisão externa).

Candidatos já mapeados:
- `ItemTooltip`, `Item.get_ItemName`, `ItemMod.GetDescription`
- `CraftingRecipe.GetDescription`, `ItemSearch.*` (busca de itens)
- Template de nome: `[item prefix] [item name] [item suffix]`

---

## Textos já publicados (BetterTooltips)

| Texto | Conteúdo | Evidência |
|---|---|---|
| `+ X% increased Treasure Find` (5 níveis) | "Increases the chance for enemies to drop items. Does not affect item rarity. Stacks with your party." | código (`LootTable.GetLoot`, `GetWorldLoot`, `GetCharacterLootDropModifier`) + log (`[Loot]`) |
| `+ X% increased Gold Find` (5 níveis) | "Increases the gold you earn. Stacks with your party." | código (`ApplyGoldModifiers`) — validação pendente |
| Tooltips Shops/Potions | correção de espaçamento | observado em jogo |
