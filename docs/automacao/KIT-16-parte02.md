# KIT-16 — parte 02: varredura do codigo e ELECAO do mecanismo de isolamento

run 700 · 2026-10-10 · continua de `KIT-16-parte01.md`

## A. VARREDURA DIRIGIDA NO CODIGO DECOMPILADO (Fase 1 — prova, nao palpite)

Comando real (exit 0, 37 s):

    ilspycmd -o scratch/kit/KIT-16-run700/dump lib/Assembly-CSharp.dll

Saida: `scratch/kit/KIT-16-run700/dump/Assembly-CSharp.decompiled.cs` (17.815.971 B).

Ocorrencias de `persistentDataPath` no codigo do jogo: **31**. TODOS os consumidores
resolvem para o MESMO diretorio (`Application.persistentDataPath`), direta ou via
`FileSystem.persistentDataPath`:

| linha | consumidor | caminho escrito |
|---|---|---|
| 106729 | `FileSystem.persistentDataPath` | `_cachedPersistentDataPath ?? Application.persistentDataPath` |
| 24126 | `SaveLogsToDevice` | `<pdp>/logs.txt` |
| 32495/32499/32501/32503 | `Character` save | `Character{N}.json`, `Headshot{N}.png`, `HeadshotGrayscale{N}.png`, `FullBody{N}.png` |
| 44999/446895 | `GlobalSaveDataManager` | `GlobalSaveData.json` (+ `.backup`, `.temp`) |
| 446907/446919 | quest saves | `QuestSaveCampaign.json`, `QuestSaveRoguelike.json` |
| 132708 | `ItemStash` | `ItemStash.json` |
| 325061 | `TransmogList` | `TransmogList.json` |
| 108514 | `PlayerPrefsFilename` | `<pdp>/PlayerPrefs` (arquivo proprio do jogo) |
| 110380 | `LoadMaps` | `<pdp>/SaveFile.db` |
| 92792 | Cross-Promo cache | `<pdp>/CrossPromo/…` |
| 264973 / 268036 | multiplayer | `<pdp>/<name>` |
| 266349 / 266471 | multiplayer | `mpsnap_*.json`, `mpfp_*.json` |
| 207157/207205/268186/266774 | listagem de saves | `Directory.GetFiles(pdp, "Character*.json")` |
| 172020/172021 | screenshot | `<pdp>/Screenshot <n>.png` |
| 451413 | hash de identidade | `Application.persistentDataPath` concatenado |
| 409867/410488/410504/410507 | PolyFew (asset de terceiro) | export OBJ |
| 106729 | (o proprio `FileSystem`) | — |

`_cachedPersistentDataPath` e **declarado e nunca atribuido** dentro do
`Assembly-CSharp.dll` (unica ocorrencia: declaracao + leitura) => na pratica
`FileSystem.persistentDataPath == Application.persistentDataPath` sempre.

`Application.dataPath` / `streamingAssetsPath` sao usados (linhas 24101-24104,
92798, 110825, 134183, 409865-410416) mas apontam para a INSTALACAO
(`E:\…\Stolen Realm\Stolen Realm_Data`), nao para dados de usuario.

**Conclusao da Fase 1:** existe UM unico diretorio de dados em arquivo —
`Application.persistentDataPath` — e todos os arquivos de save/log/config do jogo
estao sob ele. Isolar esse caminho isola tudo que e arquivo.

## B. SEGUNDO LOCAL (nao-arquivo): o REGISTRO

`PlayerPrefs` (285 ocorrencias no codigo) no Windows Player da Unity grava em
`HKCU\Software\Burst2Flame Entertainment\Stolen Realm` — **medido** com
`reg.exe query "HKCU\Software\Burst2Flame Entertainment" /s` (exit 0), ~30 valores,
incluindo `unity.player_sessionid_*`, `unity.cloud_userid_*`, `MixpanelId_*`,
resolucao/fullscreen. Tambem existe `HKCU\Software\Unity\UnityStandalone`.

Nao e diretorio: junction/symlink NAO o cobre. Tratamento eleito para este cartao:
snapshot do ramo (`reg export`) + restauracao (`reg delete` + `reg import`) com
hash do export antes/depois — mecanismo real e exercitavel offline. O que NAO for
exercitado sera declarado NAO_EXERCITADO.

## C. ELECAO DO MECANISMO DE REDIRECIONAMENTO (com porque)

| candidato | cobre | risco | veredito |
|---|---|---|---|
| **junction NTFS no caminho exato** (`LocalLow\Burst2Flame Entertainment\Stolen Realm` -> copia descartavel), com o diretorio real renomeado ao lado | **TUDO** que o processo escreve ali, inclusive codigo NATIVO da Unity (Player.log, crash dumps) e consumidores gerenciados que ignoram `FileSystem` | exige renomear (reversivel) a pasta real por alguns minutos; interacao com Steam Cloud (secao D) | **ELETO** |
| reflexo/`Harmony` em `Application.persistentDataPath` / `FileSystem` | so chamadas GERENCIADAS | Player.log e demais escritas NATIVAS continuariam indo para a pasta REAL (buraco real de isolamento) | REJEITADO como primario; registrado como alternativa |
| `FileSystem._cachedPersistentDataPath` por reflection | so `FileSystem` | 15+ consumidores usam `Application.persistentDataPath` direto (tabela A) — cobertura parcial | REJEITADO |
| variavel de ambiente / flag de linha de comando da Unity | — | o Player Windows da Unity nao expoe override de `persistentDataPath` (nenhuma flag documentada); nao foi encontrado no codigo do jogo | descartado |
| segunda conta/maquina Windows | tudo | nao disponivel nesta frente | descartado (lacuna declarada) |

Justificativa do junction: `Application.persistentDataPath` no Player Windows
resolve para um caminho **fixo** derivado do perfil do usuario
(`%USERPROFILE%\AppData\LocalLow\<Company>\<Product>`); o junction substitui esse
caminho no nivel do sistema de arquivos, de modo que toda a I/O (gerenciada e
nativa) segue o link. Verificado que NENHUM componente do caminho
(`AppData\Local`, `LocalLow`, `Burst2Flame Entertainment`, `Stolen Realm`) e
reparse point hoje — o unico link sera o criado pelo harness.

## D. RISCO DECLARADO: STEAM CLOUD

Medido em `C:\Program Files (x86)\Steam\userdata\37602317\config\localconfig.vdf`
(exit 0): app `1330000` tem `"cloud" { "last_sync_state" "synchronized" }` e
`"autocloud" { "lastlaunch" ... "lastexit" ... }` => **Steam Cloud esta ativo**
para o app e a pasta de dados esta sincronizada.

Consequencia: se a rodada alterar arquivos sob o alvo e o Steam sincronizar, o
estado na nuvem pode divergir do save real do dono. Mitigacoes aplicadas:
1. a pasta real e restaurada **byte a byte** (hashes) — inclusive
   `steam_autocloud.vdf`, que faz parte do snapshot;
2. o harness MEDE e REGISTRA exatamente quais arquivos a rodada criou/alterou
   na area isolada (diff de conteudo) — sem isso, "sincronizou" seria suposicao;
3. o risco residual (Cloud ter recebido conteudo de teste) fica **declarado** no
   fechamento, com a lista medida, para decisao do dono. Nao sera escondido.

## E. O QUE O HARNESS VAI ENTREGAR

`scratch/kit/kit16-save-isolado.sh` com subcomandos:
`status` (somente leitura) · `preparar` (snapshot + copia + junction) ·
`verificar` · `restaurar` (desfaz junction + rename inverso + compara hashes) ·
`run` (preparar -> lancar jogo -> esperar -> encerrar por PID -> restaurar).

Reuso (nao reimplementado): `tree_snapshot.py` (sha256 por arquivo),
`front-unica.sh` (frente runtime unica), `runtime-isolado.sh` (isolamento do
BepInEx/log/PID — o KIT-16 cobre o que ele NAO cobria: `persistentDataPath`).

## F. PROXIMOS PASSOS

parte03: escrita do script + prova offline do mecanismo (junction real, escrita
real por processo real, restauracao com hashes identicos, controle negativo).
parte04: rodada real com o jogo na area isolada (ou declaracao NAO_EXERCITADO com
a prova do bloqueio).
