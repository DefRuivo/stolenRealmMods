# LEVEL-R2 — relatorio 02: implementacao e execucao

Task: `t_918314e9` · worktree `C:/dev/stolen-realm/.worktrees/level-r2` (branch `wt/t_918314e9`)
Fontes normativos: `LEVEL-R1-parte05.md` / `LEVEL-R1-parte06.md` (06 prevalece) do pacote do pai
`t_8d6efbf5` (`LEVEL-R1-entrega.zip`, sha256 `2cfe27a6…c69e`), extraido em scratch fora do worktree.
Modelo desta rodada: `deepseek-flash` / provider `deepseek`.

## 1. O que esta entregue

Mod NOVO em `RoguelikeLevelProgression/` (nenhum arquivo de outro mod, da arvore WIP ou do jogo
foi alterado; nada foi instalado, nenhum save/perfil do dono foi tocado, `Assembly-CSharp.dll`
nao foi modificada). 2988 linhas de C# em 15 arquivos + `csproj`, `manifest.json`, `README.md`,
`CHANGELOG.md`.

- `Plugin.cs` — `com.gumatos.roguelikelevelprogression`, nome de exibicao
  `Roguelike Level Progression`, 0.1.0; config `General.Enabled` / `Progression.MaxLevel` /
  `Rewards.RewardQueryLevel` / `Diagnostics.Verbose`.
- `Core/` (puro, sem UnityEngine): `XpCurve` (extensao linear pos-20 sobre F20/D20),
  `PolicyCore` (decisao + teto efetivo), `LedgerDocument` (sidecar v1), `MiniJson`.
- `Runtime/`: `XpBackend` (le F20/D20 do proprio jogo), `Policy` (faixa "jogo" da politica),
  `ExtensionScope`/`GameState`/`Log`, `ReceiptLedgerStore` (gravacao atomica), `LedgerService`
  (cache, recibos, reset de run).
- `Patches/`: `BattleResultTranspiler` (nucleo do patch critico, matcher estrutural),
  `GameplayPatches` (transpiler + MaxLevel + mirror legado + 5 conversores + escopos),
  `RewardPatches` (consultas de recompensa, contagem da fila, estagios, reroll, preset sync),
  `UiPatches` (barra de XP / "Max"), `PatchRegistry` (tudo-ou-nada + rollback),
  `Reflect` (resolucao de membros por reflexao direta — ver §5).
- `tests/RoguelikeLevelProgression.Harness/` — harness isolado (net6.0) descrito em §3.

## 2. Build real

```
dotnet build RoguelikeLevelProgression/RoguelikeLevelProgression.csproj -p:DeployToBepInEx=false
dotnet build RoguelikeLevelProgression/RoguelikeLevelProgression.csproj -c Release -p:DeployToBepInEx=false
```

Ambos: **0 Erro(s)** (exit 0). Unico aviso: `MSB3277` (conflito de versao de
`System.Net.Http` entre a `lib` externa e o `NETStandard.Library.Ref` 2.1) — pre-existente na
convencao de referencias do repo, nao afeta a DLL gerada. DLL Release:
`RoguelikeLevelProgression.dll`, 57344 bytes, sha256 `30c628587358…e3585`.
O target de deploy so roda com `-p:DeployToBepInEx=true`; nada foi copiado para o perfil do r2modman.

## 3. Harness: como o codigo REAL foi exercitado

Decisao de projeto do harness (`tests/…/Program.cs`, `IlLoader.cs`): ele **compila os fontes
reais do mod** (`<Compile Include="..\..\RoguelikeLevelProgression\{Core,Runtime,Patches}\*.cs">`
+ `Plugin.cs`) e referencia a `lib` externa como somente-leitura. Nada de reimplementar a regra
em Python: quem decide e o proprio codigo do plugin.

Leitura de IL: o leitor do MonoMod usado pelo Harmony (`PatchProcessor.GetOriginalInstructions`)
lanca `NotSupportedException: Body-less method` neste host .NET 6 (SPIKE da rodada anterior,
reconfirmado), e o `AccessTools` do HarmonyX nem inicializa aqui. Por isso `IlLoader` le a IL
**real** de `Root.SendGameCompleteFromServer` da `Assembly-CSharp.dll` de referencia com
`System.Reflection` (metadados + `MethodBody.GetILAsByteArray`, tokens resolvidos por
`Module.ResolveMethod/ResolveField`, opcodes pela tabela de `OpCodes`) e monta objetos
`HarmonyLib.CodeInstruction` **reais** com labels `System.Reflection.Emit.Label` reais — a mesma
estrutura que o Harmony entrega ao transpiler. O hash da DLL e conferido dentro do harness
(`assembly.sha256_matches_spec`), e o leitor ainda confere que o metodo-alvo nao tem branch com
alvo fora da lista (`il.no_dangling_branch_targets`).

Contraprovas do transpiler (todas sobre IL real, com o scanner do harness independente do codigo
do mod): janela unica; `get_Level` retirada e `Character` mantido no stack; `get_instance` e
`roguelikeManager` preservados; `ldfld RoguelikeMaxLevel` virando `call Policy.CanAdvance`; `bge.s`
→ `brfalse.s` para o **mesmo** destino; cauda de premio (`GiveExperience` + `List<Character>::Add`)
antes da instrucao rotulada (premio E lista pulados juntos); label injetado na instrucao
substituida sendo copiado; recusa explicita quando a instrucao removida tem labels; recusa quando
a cauda de premio some; 0 correspondencias quando o membro e trocado ou quando o operando de
branch nao e `Label`; recusa em ambiguidade (2 janelas); recusa sem `Policy.CanAdvance`; entrada
real `BattleResultPatches.Transpiler(...)` reescrevendo a IL; e nenhuma mutacao parcial em falha.

## 4. Resultado da rodada final

Comando (o `BEPCORE`/`MANAGED` sao apenas diretorios de busca de dependencias, leitura):

```
dotnet tests/RoguelikeLevelProgression.Harness/bin/Debug/net6.0/RlpHarness.dll \
  "<worktree>/docs/automacao/LEVEL-R2-evidencias" \
  "C:/dev/stolen-realm/lib" \
  "%APPDATA%/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/core" \
  "E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/Managed"
```

**exit 0 — PASS=91, FAIL=0, NAO_EXERCITADO=14.** Evidencia integral:
`docs/automacao/LEVEL-R2-evidencias/rodada-final-01.txt` (+ `.json`),
sha256 `ad38e891…be28` / `d5a9a501…cccd`.

Cobertura por item de aceite do cartao:

| aceite | onde | resultado |
| --- | --- | --- |
| 19→20, 20→21, 29→30, 30→31 | `policy.advance_*`, `policy.cap20_removed_for_rogue` | PASS |
| guardas (IA, campanha, multiplayer, modo, mod desligado) | `policy.*_out_of_scope`, `patches.scope_inactive_*` | PASS |
| derrota/ownership/AI/campanha | `policy.ai_out_of_scope`, `policy.campaign_out_of_scope`, `gamestate.no_network_means_multiplayer` | PASS |
| duas vitorias sem duplicacao | `policy.two_victories_both_advance` + `ledger.ordinal_dedupe` + `ledger.sequential_records_get_distinct_ordinals` | PASS |
| skills normal/esgotada/excluida/reroll | ledger (recibo durável) e `registry.all_targets_resolve_on_real_dll` para os alvos; fluxo de janela/botoes NAO_EXERCITADO (precisa do jogo) | PASS parcial |
| itens vazios (fallback null) | alvo `GetItemChoices` resolvido; guarda de lista vazia NAO_EXERCITADA (precisa de `RoguelikeManager` real) | PASS parcial |
| ledger reload/corrompido/writefailure/reset | `ledger.*` (18 verificacoes) | PASS |
| config menor preserva level | `policy.lower_config_preserves_level` | PASS |
| roundtrip/inversa XP | `xp.*`, `xpbackend.*` | PASS |
| UI sem Max falso/NaN | `policy.effective_max_level_*` (PolicyCore) | PASS parcial |
| alvo ausente rollback | `policy.missing_targets_refuse` + `registry.all_targets_resolve_on_real_dll` (sem alvo ausente na DLL real) | PASS |

Os 14 itens `NAO_EXERCITADO` estao listados com motivo no proprio relatorio do harness (aplicacao
real dos patches no Harmony, jogo aberto, niveis 21..31 em jogo, mirror/save legado, pools de
skill/item, UI em runtime, multiplayer real, save/perfil do dono, parametros serializados de XP,
ciclo de vida do BepInEx). **Nenhum PASS foi fabricado**: onde a bancada nao alcanca, o item e
declarado NAO_EXERCITADO.

## 5. Decisoes e desvios declarados

1. **Resolucao de membros sem `AccessTools`** (`Patches/Reflect.cs`). O cctor do `AccessTools`
   (HarmonyX) chama `MethodInvoker.GetHandler(null)` quando `Exception::PrepForRemoting`/
   `FixRemotingException` nao existem — o que ocorre em qualquer runtime fora do Mono antigo do
   jogo. Alem de bloquear a bancada, isso e uma dependencia de inicializacao desnecessaria: todos
   os alvos do mod sao buscas simples por nome/assinatura. `Reflect` faz a mesma busca
   (tipo + tipos-base, publico/nao-publico, instancia/estatico) e devolve `null` para alvo
   ausente, preservando o fail-closed. Sem hardcode e sem "tolerancia parcial".
2. **Planos de patch guardam `MethodInfo`** e o `HarmonyMethod` e criado somente em `ApplyAll`
   (antes de aplicar). Isso torna a resolucao dos 20 alvos exercitavel fora do jogo, sem mudar o
   comportamento em jogo.
3. **Seams de teste explicitamente marcados** (nao usados pelo mod em producao):
   `XpBackend.PrimeForTests` (+ `ResetForTests` ja existente) e
   `LedgerService.{ReceiptCountByGuid,TryRecordSkippedSkillByGuid,OnPresetSyncSuccessByGuid}`
   — as versoes por `Character` delegam para elas, entao o caminho exercitado e o **mesmo** codigo.
   `PatchRegistry.TryBuildPlans` foi extraido de `ApplyAll` para que a resolucao de alvos seja
   testavel.
4. **Patch critico** implementado exatamente como a parte06 pede: mantem `Character` + settings no
   stack, retira `get_Level`, troca o load do campo de cap por
   `call bool Policy.CanAdvance(Character, RoguelikeSettings)` e converte `bge(.s)` em
   `brfalse(.s)` para o MESMO destino; exige 1 match estrutural; sem local/offset chumbado;
   labels/exception blocks preservados. Grupo de gameplay tudo-ou-nada com
   `Harmony.UnpatchID(guid)` — nada de tolerancia parcial.
5. **Nao removemos** o teto 30 do item/fortune, nao mexemos em `LevelUpSequenceOrder` compartilhado,
   nao inventamos skill/ouro, nao forcamos conquista, nao alteramos campanha, nao tocamos Bard/musica.

## 6. Defeito encontrado pela bancada (corrigido)

`ReceiptLedgerStore.Save` criava o diretorio **fora** do `try`: uma falha de disco/permissao
escapava como `IOException` cru em vez de `LedgerWriteException`, ou seja, a falha de gravacao
podia atravessar o fluxo de recompensa em vez de ser tratada como "nao consumir a recompensa".
Corrigido (criacao do diretorio dentro do `try`) e coberto pelos testes
`ledger.write_failure_does_not_consume`, `ledger.write_failure_repeatable` e
`ledger.retry_after_failure_succeeds`.

## 7. O que NAO foi feito nesta fase

Publicacao/instalacao/execucao real no jogo (fora do escopo do cartao), integracao na arvore
WIP/main e push. Nenhum corpus integral nem DLL de jogo/referencia entra no pacote de revisao.
