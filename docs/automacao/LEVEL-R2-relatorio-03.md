# LEVEL-R2 — relatorio 03: reproducao, pacote de revisao e pendencias para a R3

Task: `t_918314e9` · worktree `C:/dev/stolen-realm/.worktrees/level-r2` (branch `wt/t_918314e9`)
Este arquivo e **novo** (nao sobrescreve nenhum relatorio anterior: 01 = baseline da rodada),
no mesmo espirito do 02: evidencias reais, sem PASS fabricado.

## 1. Como reproduzir (sem abrir o jogo, sem instalar nada)

Pre-requisitos: .NET SDK 6 (a bancada usa 6.0.428), a `lib` comum do repositorio em
`C:/dev/stolen-realm/lib` (somente leitura) e acesso de LEITURA a dois diretorios que so servem
para resolver dependencias de assemblies (`MonoMod.Utils` e `Facepunch.Steamworks.Win64`):

- `%APPDATA%/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/core`
- `<jogo>/Stolen Realm_Data/Managed`

```
cd C:/dev/stolen-realm/.worktrees/level-r2

# 1) build do mod (deploy e opt-in; nada e instalado sem -p:DeployToBepInEx=true)
dotnet build RoguelikeLevelProgression/RoguelikeLevelProgression.csproj -p:DeployToBepInEx=false

# 2) build + execucao do harness isolado
dotnet build tests/RoguelikeLevelProgression.Harness/RoguelikeLevelProgression.Harness.csproj
dotnet tests/RoguelikeLevelProgression.Harness/bin/Debug/net6.0/RlpHarness.dll \
  "C:/dev/stolen-realm/.worktrees/level-r2/docs/automacao/LEVEL-R2-evidencias" \
  "C:/dev/stolen-realm/lib" \
  "%APPDATA%/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/core" \
  "E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/Managed"
```

Saida esperada: `RESUMO: PASS=91 FAIL=0 NAO_EXERCITADO=14` e exit code 0 (exit 1 se qualquer
verificacao falhar). O harness grava `harness-results.txt` e `harness-results.json` no diretorio
passado em `argv[0]`; a rodada final esta preservada em `LEVEL-R2-evidencias/rodada-final-01.*`
(arquivos `harness-results.*` sao o buffer mutavel do harness, nao o registro da rodada).

O harness confere sozinho o sha256 da `Assembly-CSharp.dll` de referencia
(`8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a`): com outra DLL os testes de
IL/transpiler falham de proposito em vez de dar falso verde.

## 2. Pacote de revisao

`docs/automacao/LEVEL-R2-pacote-revisao.zip` (sha256 registrado em
`docs/automacao/LEVEL-R2-pacote-revisao.sha256.txt`, gerado no momento do empacotamento).
Conteudo: fontes do mod (`.cs`, `.csproj`, `manifest.json`, `README.md`, `CHANGELOG.md`),
o harness (`Program.cs`, `IlLoader.cs`, `.csproj`), os relatorios 01/02/03, `LEVEL-R2-hashes.txt`
e as evidencias da rodada final. **Nao contem** DLL de jogo, DLL de referencia, corpus
decompilado integral, `bin/`, `obj/` nem qualquer coisa do perfil/save do dono.

## 3. Pendencias e riscos que a revisao independente (R3) deve atacar

1. **Aplicacao real dos patches no Harmony (NAO_EXERCITADO).** Neste host .NET 6 o leitor de IL
   do MonoMod lanca `NotSupportedException: Body-less method` e o `AccessTools` nem inicializa
   (`MethodInvoker.GetHandler(null)`), entao `harmony.CreateProcessor(...).Patch()` nao roda aqui.
   O que foi provado: os 20 alvos resolvem na DLL real
   (`registry.all_targets_resolve_on_real_dll`), o transpiler real reescreve a IL real, e o
   grupo e tudo-ou-nada por construcao. O que NAO foi provado: a aplicacao efetiva + o rollback
   efetivo dentro do jogo.
2. **`Progression.MaxLevel` voluntario e save.** O teto voluntario foi exercitado na politica
   (`policy.voluntary_cap`, `policy.lower_config_preserves_level`: reduzir a config **nao**
   rebaixa o nivel ja salvo). Falta a prova em save real.
3. **Recibos e fila no jogo.** `RewardQueryPatches.PostfixNeededCount` (subtracao de S na
   contagem) e `LedgerService.IdentityOf(Character)` precisam de `Character` real
   (`CharacterSaveFile.Guid`, `CharacterPresetFileGuid`, `OwnerID`). A bancada exercitou o mesmo
   caminho de load/cache/dedupe/rollback por guid. Verificar em jogo: pool de skill esgotado,
   pool de item vazio, reroll sem opcao e o reset de run so depois de `SyncCharacterToPreset`.
4. **F20/D20 reais.** Os parametros serializados de XP (`ExperienceBasePerLevel`,
   `ExperienceExponentialGainPerLevel`, `ExperienceOffset`, `NumStatsPerNewLevel`) seguem
   ilegiveis por asset (parser em EOF, desde a R1). Em runtime o mod le
   `Character.GetExperienceFloorForLevel(20)`/`(21)`; a matematica foi provada com o par
   informado. Verificar em jogo se a extensao casa exatamente com o vanilla em 20→21.
5. **UI.** `InventoryManagerPatches`/`SkillbarPatches` precisam de instancias Unity e textos TMP;
   na bancada so as guardas de escopo e o teto efetivo (`PolicyCore.EffectiveMaxLevel`, sem
   NaN/Inf e nunca abaixo do nivel atual) foram exercitados.
6. **Multiplayer.** O branch vanilla foi provado na politica (`IsMultiplayer=true` → comparacao
   vanilla) e `GameState.IsMultiplayer()` sem rede devolve `true` (fail-closed = nao amplia),
   mas nao foi testado em partida real.
7. **Decisao de projeto a auditar:** a troca de `AccessTools` por `Reflect` (§5 do relatorio 02).
   O comportamento em jogo deve ser o mesmo (alvo ausente → `null` → fail-closed); a revisao deve
   conferir assinaturas/ambiguidade dos 20 alvos resolvidos.

## 4. Declaracao final

Todos os itens acima estao marcados como `NAO_EXERCITADO` na evidencia da rodada final com o
motivo. Nenhuma verificacao foi inventada, nenhum resultado foi copiado de execucao nao feita, e
o unico desvio de especificacao (resolucao de membros sem `AccessTools`) esta justificado por
medicao (falha de inicializacao do proprio `AccessTools` neste host) e registrado aqui e no
`CHANGELOG.md`.
