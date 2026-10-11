# Changelog — RoguelikeLevelProgression

## 0.1.0

**Primeira versão.** Mod novo (nenhum arquivo de mod existente foi alterado), standalone
BepInEx 5 + Harmony, sem ModAPI, sem BetterStats/RSTV.

### Gameplay

- **Teto 20 removido no modo Roguelike (singleplayer).** A comparação
  `character.Level < settings.RoguelikeMaxLevel` do bloco de resultado de batalha
  (`Root.SendGameCompleteFromServer`) passa a ser `Policy.CanAdvance(Character, RoguelikeSettings)`.
  O patch é **estrutural**: reconhece a janela pelas assinaturas dos membros
  (`Character::get_Level`, `GlobalSettingsManager::get_instance`,
  `GlobalSettingsManager::roguelikeManager`, `RoguelikeSettings::RoguelikeMaxLevel`, `bge`),
  exige **exatamente uma** correspondência e preserva labels/exception blocks; não há índice de
  local nem offset de IL chumbado. `bge` → `brfalse` para o **mesmo destino**, então uma recusa
  da política pula **prêmio e lista** juntos.
- **Um nível por vitória**, com os atributos vanilla derivados de `Level` e skills/itens
  enquanto elegíveis.
- **XP estendido depois do 20, linear e O(1)**, derivado de `F20`/`D20` lidos do próprio jogo
  (`Character.GetExperienceFloorForLevel(20)`/`(21)`); em `L = 20` e `L = 21` a extensão coincide
  com o vanilla por construção. A inversa é analítica (sem laço sem limite) e as consultas de
  XP dos 5 conversores estáticos só valem dentro de um escopo explícito por personagem —
  campanha e IA ficam intactas. Mirror de XP legado limitado ao nível 20 para personagem
  estendido (o `ExperienceLevel` real continua sendo a fonte e segue sendo salvo).
- **Recompensas com pool esgotado.** Pool de skills vazio: o estágio é pulado **depois** de
  gravar um recibo durável (S) e o S é subtraído da contagem da fila; se o recibo não gravar, o
  estágio **não** é pulado (a recompensa não é consumida). Pool de itens vazio: o fallback
  `null` é bloqueado e o fluxo segue para atributos. Reroll com `forcedTier` sem opção é
  cancelado (a skill original é preservada). A ordem `LevelUpSequenceOrder` compartilhada **não**
  é alterada.
- **Sidecar v1** em `Paths.ConfigPath/com.gumatos.roguelikelevelprogression/receipts/<guid>.json`
  (`schema_version`, `character_guid`, `run_id`, `preset_guid`, `skipped_skill_receipts[]`),
  gravação atômica (temporário + replace + backup `.bak`), dedupe por ordinal. A run só é
  resetada **depois** de um `SyncCharacterToPreset` válido; preset nulo não reseta; ledger
  corrompido/ilegível não consome recompensa.
- **Multiplayer:** branch vanilla mantido, com aviso de que saves/ledger estendidos não são
  suportados nesta versão.

### Banco de provas (harness isolado)

- Harness `tests/RoguelikeLevelProgression.Harness` (net6.0) que compila os **fontes reais** do
  mod e exercita: o transpiler real sobre a **IL real** da `Assembly-CSharp.dll` de referência
  (hash `8bb4a7c5…7855a`), com 12 contraprovas (janela única, remoção do `get_Level`, `bgE`→`brfalse`
  com o mesmo destino, labels preservados, recusa em ambiguidade/alvo inseguro/cauda de prêmio
  ausente, ausência de mutação parcial); a matriz da política (19→20, 20→21, 29→30, 30→31,
  guardas de IA/campanha/multiplayer/modo/teto voluntário/limite de representação/alvo ausente);
  a curva de XP (monotonia, inversa, precisão, orçamento em `long`); o ledger (reload,
  dedupe, corrompido, schema desconhecido, identidade divergente, falha de escrita **sem**
  consumir recompensa, reset só com preset válido, backup atômico); e as guardas de escopo das
  entradas estáticas dos patches.
- 91 verificações PASS, 0 FAIL, 14 itens `NAO_EXERCITADO` declarados com motivo (aplicação real
  dos patches no Harmony, jogo aberto, save/reload do dono, multiplayer, `F20`/`D20`
  serializados reais, UI em runtime).

### Correções encontradas pela bancada

- **`ReceiptLedgerStore.Save`: a criação do diretório estava fora do `try`.** Uma falha de
  disco/permissão escapava como `IOException` cru em vez de `LedgerWriteException`, ou seja, a
  falha de gravação podia atravessar o fluxo de recompensa em vez de ser tratada como "não
  consumir a recompensa". Passou para dentro do `try` — exercitado por teste real.
- **Resolução de membros sem `AccessTools`.** Os alvos passaram a ser resolvidos por reflexão
  direta (`Patches/Reflect.cs`): o inicializador estático do `AccessTools` do HarmonyX quebra em
  runtimes modernos (`MethodInvoker.GetHandler(null)`, porque `Exception::PrepForRemoting`/
  `FixRemotingException` não existem fora do Mono antigo) e isso é uma dependência de
  inicialização que o mod não precisa. Alvo ausente continua devolvendo `null` → fail-closed.
- **Planos de patch guardam `MethodInfo`** em vez de `HarmonyMethod` (a criação do
  `HarmonyMethod` acontece só na hora de aplicar), o que tornou a resolução dos 20 alvos
  exercitável na bancada.
