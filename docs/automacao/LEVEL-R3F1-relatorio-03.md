# LEVEL-R3F1 — relatório 03: reprodução, pacote de revisão e pendências

Task: `t_021bdd67` · worktree `C:/dev/stolen-realm/.worktrees/level-r2` (branch `wt/t_918314e9`).
Arquivo **novo** (não sobrescreve nenhum relatório anterior).

## 1. Como reproduzir (sem abrir o jogo, sem instalar nada)

Pré-requisitos: .NET SDK 6 (host atual: 6.0.428), a `lib` comum do repositório em
`C:/dev/stolen-realm/lib` (somente leitura) e acesso de LEITURA a dois diretórios que só servem
para resolver dependências de assemblies (`MonoMod.Utils`, `Facepunch.Steamworks.Win64`):

- `%APPDATA%/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/core`
- `E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/Managed`

```
cd C:/dev/stolen-realm/.worktrees/level-r2

# 1) build do mod (deploy e opt-in: nada e instalado sem -p:DeployToBepInEx=true)
dotnet build RoguelikeLevelProgression/RoguelikeLevelProgression.csproj -c Release -p:DeployToBepInEx=false

# 2) build + execucao do harness isolado
dotnet build tests/RoguelikeLevelProgression.Harness/RoguelikeLevelProgression.Harness.csproj
dotnet tests/RoguelikeLevelProgression.Harness/bin/Debug/net6.0/RlpHarness.dll \
  "C:/dev/stolen-realm/.worktrees/level-r2/docs/automacao/LEVEL-R3F1-evidencias" \
  "C:/dev/stolen-realm/lib" \
  "%APPDATA%/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/core" \
  "E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/Managed"
```

Saída esperada: `RESUMO: PASS=103 FAIL=0 NAO_EXERCITADO=14`, exit 0. O harness grava
`harness-results.txt`/`.json` no diretório de `argv[0]`; a rodada final está preservada em
`LEVEL-R3F1-evidencias/rodada-final-01.*`. O harness confere sozinho o sha256 da
`Assembly-CSharp.dll` de referência.

Contra-prova (defeito replantado) — reverter a correção e rodar de novo:

```
git checkout -- RoguelikeLevelProgression/Core/PolicyCore.cs RoguelikeLevelProgression/Runtime/Policy.cs
dotnet build tests/RoguelikeLevelProgression.Harness/RoguelikeLevelProgression.Harness.csproj
dotnet tests/…/RlpHarness.dll "<dir>" lib <BepInEx/core> <Managed>
# esperado: exit 1, PASS=100 FAIL=3, os 3 FAIL sendo loadclamp.* (downgrade no clamp de carga)
```

Evidência da contra-prova: `LEVEL-R3F1-evidencias/defeito-replantado-01.*`.

## 2. Pacote de revisão

`docs/automacao/LEVEL-R3F1-pacote-revisao.zip` (sha256 em
`docs/automacao/LEVEL-R3F1-pacote-revisao.sha256.txt`). Conteúdo: fontes do mod (`.cs`, `.csproj`,
`manifest.json`, `README.md`, `CHANGELOG.md`), o harness (`Program.cs`, `IlLoader.cs`, `.csproj`),
os relatórios 01/02/03 desta correção, `LEVEL-R3F1-hashes.txt` e as evidências (rodada final +
contra-prova). **Não contém** DLL de jogo, DLL de referência, corpus decompilado, `bin/`, `obj/`
nem nada do perfil/save do dono. `LEVEL-R3F1-pacote-revisao-MANIFEST.json` lista cada membro com
bytes + sha256 e declara `contains_game_dll_or_full_decompiled_corpus: false`.

## 3. Versão

Bump para **0.1.1** nos quatro espelhos da convenção do repo:
`RoguelikeLevelProgression.csproj` (`<Version>`), `manifest.json` (`version_number`),
`Plugin.cs` (`PluginVersion` = literal de `[BepInPlugin]`) e `README.md` (`Version:`). O
`CHANGELOG.md` ganhou a seção 0.1.1 descrevendo R3-01 e a correção. GUID
(`com.gumatos.roguelikelevelprogression`), configuração, escopo e todas as demais decisões de
LEVEL-R2 ficaram intocados.

## 4. O que mudou desde o commit `cd8e4ce`

- `RoguelikeLevelProgression/Core/PolicyCore.cs` — 3 entradas novas em `AdvanceInputs`
  (`VanillaMaxLevel`, `IsLoading`, `SavedLoadLevel`) e piso de carga em `EffectiveMaxLevel`.
- `RoguelikeLevelProgression/Runtime/Policy.cs` — `EffectiveMaxLevel` (getter) lê o nível salvo em
  carga e roteia o fallback pela mesma decisão única.
- `tests/RoguelikeLevelProgression.Harness/Program.cs` — suíte `loadclamp` (12 verificações).
- `RoguelikeLevelProgression/{README.md,CHANGELOG.md,manifest.json,RoguelikeLevelProgression.csproj}`
  e `Plugin.cs` — bump 0.1.1 + documentação.
- `docs/automacao/LEVEL-R3F1-*.md`, `LEVEL-R3F1-hashes.txt`, pacote, evidências.

## 5. Pendências / riscos que a revisão deve atacar

1. **Runtime não exercitado.** Aplicação real dos patches no Harmony, jogo aberto, carregar um save
   real do dono, níveis 21..31 em jogo e multiplayer real seguem `NAO_EXERCITADO` (restrição
   explícita do cartão). A prova é offline: IL real + decisão real do mod.
2. **`Character.CharacterSaveFile` durante `Load`.** O piso lê o campo em carga; a revisão deve
   confirmar na IL/decompilado que ele já está atribuído antes do clamp (está: `Load` o usa em
   IL_088b imediatamente antes do `Mathf.Min`).
3. **R3-02/R3-03/R3-04 não resolvidos.** Constante numérica de XP (`FloatSafeXpCeiling`), matriz
   por-leitor dos 39 leitores de XP e a guarda de item nulo sem teste continuam como a revisão
   R3 os classificou (MEDIO/BAIXO, sem perda de dado). Fora do escopo deste cartão corretivo.
4. **Sem certificação de gameplay.** Sucesso offline não é certificação de comportamento em jogo.
