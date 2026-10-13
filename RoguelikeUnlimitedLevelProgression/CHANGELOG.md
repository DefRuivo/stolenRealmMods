# Changelog — RoguelikeUnlimitedLevelProgression

## Não publicado — identidade do pacote (13/10/2026)

- Nome definitivo: `RoguelikeUnlimitedLevelProgression`; nome de exibição:
  `Roguelike Unlimited Level Progression`.
- Projeto, assembly, namespace, pacote e harness acompanham o nome definitivo.
  GUID/Harmony owner e diretório de recibos: `com.gumatos.roguelikeunlimitedlevelprogression`.
- Ícone `RU` 256x256, com a mesma cor e moldura. Versão permanece **0.1.1**;
  nenhuma lógica de gameplay mudou e a publicação continua bloqueada.
- Como o mod não foi publicado, não há migração de configuração/recibos locais.
  As evidências de rodadas anteriores permanecem imutáveis com a identidade da época.

## 0.1.1

**Correção de perda silenciosa de nível salvo ao carregar (R3-01, achado ALTO da revisão LEVEL-R3).**

### Correções

- **`Character.Load(int)` rebaixava o nível salvo.** O clamp de carga
  `ExperienceLevel = Mathf.Min(MaxLevel, CharacterSaveFile.ExperienceLevel)` usa exatamente a
  propriedade `Character.MaxLevel` que este mod patcheia, e roda **antes** de `ExperienceLevel` ser
  atribuído — nesse instante `Character.Level` ainda é ~1 e não protege o nível salvo. Com um teto
  voluntário `Progression.MaxLevel = N` (≥ 21) um save acima de `N` era rebaixado a `N`; e o caminho
  de fallback (grupo não aplicado / rede indisponível / backend indisponível) devolvia o teto
  vanilla **30**, truncando saves acima de 30. O valor clampado era persistido
  (`CharacterSaveFile.ExperienceLevel`), ou seja, a perda era silenciosa e durável.
  Correção: enquanto o personagem não está carregado (`IsLoaded == false`) o getter patcheado nunca
  devolve valor abaixo de `CharacterSaveFile.ExperienceLevel` — em **todos** os caminhos, inclusive
  o fallback vanilla. Fora da carga o comportamento não muda; campanha/IA/out-of-scope continuam
  vanilla. O caminho de `GiveExperience` continua sem rebater abaixo do nível atual.
- Cobertura nova na bancada (12 verificações, suite `loadclamp`): âncora estrutural na IL real de
  `Character.Load(int)` (janela única `Mathf.Min(get_MaxLevel, CharacterSaveFile.get_ExperienceLevel)`
  → `set_ExperienceLevel`), prova de que o getter do clamp é o mesmo alvo do postfix, e reprodução
  do clamp com o par (MaxLevel efetivo, nível salvo) — verde com a correção e **vermelha** com o
  defeito replantado.

### Compatibilidade

- Sem mudança de comportamento para campanha, IA, multiplayer ou personagens já carregados.
  Configuração, GUID e decisões de escopo da 0.1.0 permanecem intactas.

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
- **Sidecar v1** em `Paths.ConfigPath/com.gumatos.roguelikeunlimitedlevelprogression/receipts/<guid>.json`
  (`schema_version`, `character_guid`, `run_id`, `preset_guid`, `skipped_skill_receipts[]`),
  gravação atômica (temporário + replace + backup `.bak`), dedupe por ordinal. A run só é
  resetada **depois** de um `SyncCharacterToPreset` válido; preset nulo não reseta; ledger
  corrompido/ilegível não consome recompensa.
- **Multiplayer:** branch vanilla mantido, com aviso de que saves/ledger estendidos não são
  suportados nesta versão.

### Banco de provas (harness isolado)

- Harness `tests/RoguelikeUnlimitedLevelProgression.Harness` (net6.0) que compila os **fontes reais** do
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
