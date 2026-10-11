# KIT-16 — Isolar persistentDataPath e save no harness de runtime (parte 01)

Cartao: t_2886b6de · run 700 · profile default · inicio 2026-10-10 13:29 (-03:00)
Workspace: C:\Users\Pichau\AppData\Local\hermes\kanban\workspaces\t_2886b6de (scratch)
Repo: C:/dev/stolen-realm

## OBJETIVO DO CARTAO (resumo)

Fechar a lacuna que travou o KIT-14 (t_a1f38855, run699, block_loop_detected):
o isolamento do KIT-03 cobre o **BepInEx** (perfil r2modman), mas o **diretorio de
dados do jogo (persistentDataPath/save)** continua sendo o REAL do dono — uma
rodada ponta a ponta escreveria no save pessoal.

## ESTADO INICIAL MEDIDO (nao presumido)

- Jogo do dono: FECHADO (`Get-Process 'Stolen Realm'` = 0).
- Steam: RODANDO (1 processo `steam`) — o jogo e lancado por ele.
- Perfil BepInEx do dono: `%APPDATA%\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx`
  (core/ config/ patchers/ plugins/ scripts/ + LogOutput.log 2.654.556 B).
- Diretorio de dados do jogo: `%USERPROFILE%\AppData\LocalLow\Burst2Flame Entertainment\Stolen Realm`
  (contem Character0..16.json, GlobalSaveData.json, QuestSave*, TransmogList.json,
  ItemStash.json, FullBody*.png, Headshot*.png, Player.log, Player-prev.log,
  `Unity/`, `backtrace/`, `CrossPromo/`, steam_autocloud.vdf).
- Diretorio do jogo (instalacao): `E:\SteamLibrary\steamapps\common\Stolen Realm`
  com `doorstop_config.ini` + `winhttp.dll` (Doorstop instalado NO jogo, apontando
  `target_assembly=BepInEx\core\BepInEx.Preloader.dll` — caminho RELATIVO).

## PROVA POR LEITURA DE CODIGO (nao por palpite) — Fase 1 do cartao

`FileSystem` (decompilado de `lib\Assembly-CSharp.dll`, ja produzido no KIT-14
em `scratch/kit/KIT-14-run699/compiled-FileSystem.txt`, exit 0):

    public static class FileSystem {
        private const string MountName = "SaveData";
        private static string _cachedPersistentDataPath;
        public static string persistentDataPath => _cachedPersistentDataPath ?? Application.persistentDataPath;
        ...
    }

`GlobalSaveDataManager` (mesmo dump, `compiled-GlobalSaveDataManager.txt`, exit 0):

    public string Filename => Path.Combine(FileSystem.persistentDataPath, "GlobalSaveData.json");
    public string BackupFilename => Filename + ".backup";
    public string TempFilename => Filename + ".temp";

=> O alvo e MESMO `Application.persistentDataPath`. No Windows o player Unity
resolve isso para `%USERPROFILE%\AppData\LocalLow\<CompanyName>\<ProductName>`,
que e exatamente a pasta acima. Confirmado tambem por evidencia material: e ali
que os `Character*.json` / `GlobalSaveData.json` do dono estao.

**Ponto critico descoberto:** `FileSystem` **cacheia** o valor num campo estatico
privado `_cachedPersistentDataPath`. Existe portanto um ponto de interceptacao
gerenciado (reflection/Harmony) ANTES do primeiro uso — registrado como opcao,
nao como mecanismo eleito (ver parte 02).

## SEGUNDO LOCAL DE DADOS DESCOBERTO (nao e diretorio: e o REGISTRO)

O jogo grava **PlayerPrefs** em `HKCU\Software\Burst2Flame Entertainment\Stolen Realm`
(medido com `reg.exe query ... /s`, exit 0; ~30 valores: resolucao/fullscreen,
`unity.cloud_userid_*`, `unity.player_sessionid_*`, `MixpanelId_*`,
`backtrace-machine-id_*`, Curvy_*). Tambem existe `HKCU\Software\Unity\UnityStandalone`.

Isso e um local de dados REAL do jogo que NAO e um caminho de arquivo e portanto
NAO e coberto por junction/symlink de diretorio. Este cartao vai DECLARAR esse
escopo explicitamente (isolar ou declarar NAO_EXERCITADO) em vez de ignorar.

## PLANO (na ordem do cartao)

1. Fase 1 (feita em parte): inventario dos caminhos de dados — persistencia em
   arquivo (LocalLow) + registro (PlayerPrefs) + varredura dirigida no codigo
   decompilado por `persistentDataPath` / `PlayerPrefs` / `Directory.CreateDirectory`.
2. Fase 2: snapshot SHA256 **por arquivo** (conteudo) do diretorio real do dono.
3. Fase 3: mecanismo de isolamento provado. Candidato principal: **junction NTFS**
   no caminho exato que o jogo resolve (`LocalLow\...\Stolen Realm` -> copia
   descartavel), com o diretorio real renomeado para backup ao lado (rename, sem
   copia destrutiva) e restauracao por rename inverso. Requisito: BepInEx tambem
   isolado (reuso KIT-03).
4. Fase 4: restauracao + hashes antes/depois identicos (evidencia registrada).
5. Fase 5: execucao real no ambiente isolado mostrando o hash do diretorio REAL
   inalterado. Se algum passo nao puder ser exercitado, declarar NAO_EXERCITADO
   com a prova do bloqueio — proibido dado sintetico.

## REUSO (nao reimplementar)

- `scratch/kit/runtime-isolado.sh` (KIT-03G1): isola BepInEx (copia), log, PID por
  CloseMainWindow, snapshot de saves por CONTEUDO via `tree_snapshot.py`, rollback.
- `scratch/kit/tree_snapshot.py`: snapshot/comparar de bytes (sha256 por arquivo).
- `scratch/kit/front-unica.sh`: lock de frente runtime unica.
- `scratch/kit/snapshot.sh`, `scratch/kit/isolacao.sh`: utilitarios de KIT-03F.

## LIMITES DESTE CARTAO

Sem publicacao; sem deploy no perfil do dono; sem tocar no perfil/save do dono sem
snapshot previo; sem abrir o jogo fora do ambiente isolado.

## CHECKPOINTS

- parte01 (este arquivo): objetivo + estado inicial medido + prova de codigo do
  alvo + descoberta do registro (PlayerPrefs) + plano.
