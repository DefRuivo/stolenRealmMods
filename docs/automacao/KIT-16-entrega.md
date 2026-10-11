# KIT-16 — ENTREGA: isolamento do `persistentDataPath`/save no harness de runtime

> Cartao `t_2886b6de` · perfil `default` · **run 700** · 2026-10-10 (BRT, UTC-03:00)
> Papel: **implementacao** (nao e aceite humano, nao e publicacao do DoD).
> Partes: `KIT-16-parte01.md` (alvo provado por codigo), `KIT-16-parte02.md`
> (varredura + eleicao do mecanismo + riscos), `KIT-16-parte03.md` (harness +
> prova offline + controle negativo), este arquivo (rodada real + fechamento).

---

## 1. O que este cartao fecha

O KIT-14 se bloqueou (`block_loop_detected`, 10/10 13:21) porque o isolamento do
KIT-03 cobre o **BepInEx** (perfil r2modman), mas o **diretorio de dados do jogo**
(`Application.persistentDataPath`) continuava sendo o REAL do dono — uma rodada
ponta a ponta escreveria no save pessoal.

**Entregue:** mecanismo de redirecionamento **exercitado em jogo**, harness no
`scratch/kit/`, evidencia de hashes antes/depois do diretorio real e declaracao
explicita do que foi e do que **nao** foi exercitado.

## 2. O alvo, provado por leitura de codigo (nao por palpite)

`scratch/kit/KIT-16-run700/dump/Assembly-CSharp.decompiled.cs` (ilspycmd, exit 0,
17.815.971 B, sha256 `873a2d1d…` — ver §8): 31 ocorrencias de `persistentDataPath`,
todas resolvendo para o MESMO diretorio; `FileSystem.persistentDataPath =>
_cachedPersistentDataPath ?? Application.persistentDataPath` e
`_cachedPersistentDataPath` nunca e atribuido. Logo, isolar o caminho
`%USERPROFILE%\AppData\LocalLow\Burst2Flame Entertainment\Stolen Realm` isola
**todos** os arquivos do jogo (save, log, cache, screenshots, multiplayer).
O jogo tambem grava `PlayerPrefs` no **registro**
(`HKCU\Software\Burst2Flame Entertainment\Stolen Realm`) — que nao e diretorio.

## 3. Mecanismo eleito (e o porque)

**Junction NTFS no caminho exato** -> copia descartavel; o diretorio real e
**renomeado ao lado** (rename no mesmo volume, nao apagado) durante a rodada e
volta por rename inverso. Escolhido porque cobre tambem a I/O **nativa** da Unity
(`Player.log`, analytics, crash dumps), que um patch Harmony/reflection nas APIs
gerenciadas **nao** cobriria (comparacao em `KIT-16-parte02.md` §C).

Ordem executada em toda rodada: snapshot sha256-por-arquivo -> copia -> export do
registro -> rename -> junction -> [jogo] -> `RemoveDirectoryW` do link -> rename
inverso -> comparacao de conteudo -> restore do registro.

## 4. O QUE FOI EXERCITADO — rodada REAL em jogo (3x, exit 0 nas 3)

Comandos reais: `SECONDS_GAME=90|150|60 EVID_DIR=... bash scratch/kit/kit16-save-isolado.sh run`
(13:37:21, 13:38:54, 13:42:0x BRT; PIDs 26332 / 23356 / 10096, lancados via
`steam.exe -applaunch 1330000` e encerrados por `CloseMainWindow` **por PID**).

| # | o que o jogo ESCREVEU na area isolada (diff de conteudo medido) | dir REAL depois | registro depois |
|---|---|---|---|
| 1 | `Player.log`, `Player-prev.log` | **byte a byte identico** ao snapshot antes | identico |
| 2 | `Player.log`, `Player-prev.log` + 4 arquivos novos de `Unity/…/Analytics/ArchivedEvents/179165034500002.*` (4 antigos removidos) | **byte a byte identico** | identico |
| 3 | `Player.log`, `Player-prev.log` + `…/ArchivedEvents/179165054100002.*` | **byte a byte identico** | identico |

Leitura: o jogo **resolveu o `persistentDataPath` para o junction** — escreveu ali
arquivos que so o proprio jogo escreve (o `Player.log` e o log **nativo** do
player Unity, e os eventos de Analytics sao da Unity). O diretorio real voltou
**identico** nas 3 rodadas (comparacao de CONTEUDO, sha256 por arquivo).

**BepInEx isolado tambem foi exercitado em jogo** (reuso KIT-03): o marcador
`ReloadProbe v1 carregado.` apareceu no `LogOutput.log` da **copia isolada** em
t+16 s / t+7 s / t+7 s, e o log preservado
(`run-real-3/LogOutput-isolado.txt`, 855 B) mostra `BepInEx 5.4.23.5`, `1 plugin to
load`, `Loading [Reload Probe 1.0.0]` e **zero** ocorrencias do caminho do perfil
do dono (`r2modmanPlus-local` = 0). Isso prova, pela primeira vez **em jogo**, dois
pontos que o KIT-03 deixou `NAO_EXERCITADO`:
1. `steam.exe -applaunch <appid> --doorstop-enabled true --doorstop-target-assembly <copia>`
   **funciona** (Doorstop 4.5.0 le os argumentos de CLI);
2. `--doorstop-mono-dll-search-path-override <copia>/core` e necessario — o
   Doorstop 4 NAO adiciona o diretorio do target ao search path do Mono por padrao.
   O `runtime-isolado.sh` (KIT-03) **nao** passava esse argumento.

**Fim do ciclo (medicao independente, fora do harness):**

    python tree_snapshot.py comparar \
      scratch/kit/KIT-16-run700/run-real-3/antes.manifest \
      "C:/Users/Pichau/AppData/LocalLow/Burst2Flame Entertainment/Stolen Realm"
    -> {"total_antes":111,"total_depois":111,"novos":[],"removidos":[],
        "alterados":[],"igual":true}   exit 0

Estado pos-rodada: o caminho real e `real` (nao junction), **nenhum** residuo
`*.kit16-real`; o `LogOutput.log` do perfil do dono permanece com mtime de
**10/10 00:03** (antes das rodadas) — o perfil do dono nao foi usado nem escrito.

## 5. O QUE FOI EXERCITADO — offline

- **Prova do mecanismo em FIXTURE** (`kit16-save-isolado.sh fixture`, exit 0):
  escrita por processo real atraves do junction apareceu na copia isolada; diff
  classificou `novos [Character99.json, CrossPromo/c.txt]` e `alterados
  [GlobalSaveData.json]`; restauracao identica ao snapshot.
- **Controle negativo** (`kit16-controle-negativo.sh`, exit 0, 3/3):
  NC-A junction ausente -> `verificar` exit 1 ("nao e junction");
  NC-B conteudo do dono alterado -> `restaurar` exit 1 ("DIVERGE do snapshot antes");
  NC-C ciclo limpo -> exit 0. O verde do NC-C **nao e tautologico**: o mesmo
  comparador reprova em NC-B.

## 6. O QUE **NAO** FOI EXERCITADO (declaracao explicita)

- **Escrita/leitura de SAVE pelo jogo** (`Character*.json`, `GlobalSaveData.json`,
  `SaveFile.db`): nas 3 rodadas o jogo **nao** tocou nesses arquivos (ficou em
  boot/menu; nenhuma navegacao, nenhum save carregado). O redirecionamento do
  caminho esta provado; a escrita de save pelo jogo **nao**.
- **Navegacao de UI, clique fisico, PNG, relatorio, Runner ativo, mods de gameplay
  carregados**: NAO_EXERCITADO (objeto do KIT-14).
- **Desempenho (FPS/frame/memoria/disco)**: NAO_EXERCITADO (dispensa B do dono).
- **Segunda instalacao/conta/ambiente**: NAO_EXERCITADO (lacuna declarada).
- **Patch Harmony/reflection como mecanismo**: implementado? NAO — registrado como
  alternativa rejeitada (§3), nao foi construido nem testado.
- **Suite `runtime-isolado.sh run` do KIT-03**: continua NAO_EXERCITADA naquele
  modo (o KIT-16 lancou com os mesmos argumentos + o override de search path).

## 7. RISCOS RESIDUAIS (medidos, nao supostos)

1. **Steam Cloud ativo** para o app 1330000 (`localconfig.vdf`, userdata 37602317:
   `"cloud" {"last_sync_state" "synchronized"}`). As rodadas registraram
   `autocloud lastexit` (1791650601) => o Steam **viu** o app rodar e sair e
   sincronizou. O que a rodada mudou na area isolada: **apenas** `Player.log`,
   `Player-prev.log` e eventos de `Unity/…/Analytics`. Os arquivos de SAVE tinham
   conteudo **identico** ao do dono (copia). Portanto o conteudo de save na nuvem
   nao mudou materialmente; logs/analytics podem ter sido reenviados. O estado
   local volta identico (inclusive `steam_autocloud.vdf`, que faz parte do
   snapshot). Desligar o Cloud exigiria editar a configuracao do Steam do dono —
   o cartao nao faz isso. **Decisao do dono se quiser zerar esse risco.**
2. **Registro (PlayerPrefs)**: restaurado por `reg delete` + `reg import` e
   conferido identico pelo sha256 do export antes/depois nas rodadas reais. Ainda
   assim, e um ramo GLOBAL do usuario — se o dono tiver o jogo aberto em paralelo,
   nao ha isolamento (por isso o harness recusa com o jogo aberto).
3. **`Player.log` do dono fica "velho"**: a rotacao do log aconteceu na area
   isolada, entao o `Player.log` do diretorio real continua sendo o da sessao
   anterior do dono (restaurado por hash). Sem perda de dados; apenas a sessao de
   teste nao aparece no log pessoal.

## 8. ARTEFATOS (caminhos, bytes, sha256) — nada sobrescrito

Harness (novos):

    scratch/kit/kit16-save-isolado.sh        23134  3a571db3298dd6b4c999445df390aa5745b2f4da157c0666bb6365c3815b93da
    scratch/kit/kit16-junction.ps1            2379  41e942e458186949c04146090a1426634020592b01a08727524db718787896a2
    scratch/kit/kit16-controle-negativo.sh    4283  5b710dadbe33abe1038e88f401856d5606c1a9bca2af1144eeaf4d6556878bc8

Docs (novos): `KIT-16-parte01.md` 5267 `bceab0c4…`, `KIT-16-parte02.md` 6834
`3db4895b…`, `KIT-16-parte03.md` 4507 `08be2951…`, este `KIT-16-entrega.md`.

Evidencias (novas) em `scratch/kit/KIT-16-run700/`:

    run-real/preparar.json                     777  1f45e0beb9555daf01d9aa1ab9293d1346bf389dcf3630c7edfa27901c877c0f
    run-real/verificar-diff.json               366  3c1bc875b5f1b8d3549b2d5d1fecdf87f40ca34112b367b22cbea1c38d67bc2c
    run-real/restauracao.json                  283  c89066dd06cd991c5692745eecd1515a21c29df497a699e00c85fd0c3dc6b956
    run-real/registro.json                     175  9b58613364c273b186711873c3e1d3709051596254d6b801654cd6fc26baed8d
    run-real-2/verificar-diff.json            1196  0b110da9c1b3339947914dda7f4397ebe68ff919d3d2421358f8c626009e1b79
    run-real-3/verificar-diff.json            1196  7cad7fcfeae1369c73a1b3a67eb5a2d159ab7e6d9558a2e0b0c60a67ae2f9c7a
    run-real-3/LogOutput-isolado.txt           855  640966e58fb7c44bc0cbde7835a796d4bb21c41d8f3f98ced60a0c39c21786f4
    run-real-3/antes.manifest                10856  62e0aeea556478d34d16af59d93a0d1370ac275bf5c6d69246c9401a27c3ac61
    run-real-3/antes.sha256                     65  e1cb2dce50c26bb69a6fac9411b89794d7e38f907689e88d6e143abe289c4d60
    run-real-3/restauracao.json                283  c9994aac76793a3038debeaa26f8c6a837b7ace31d71cd06b2eae83c44791c0c
    controle-negativo/resultado.json           109  58fede59189eb5f883ac2f07f4339433895479b3f5d773c7593a72459fae909f
    controle-negativo/nc-a/verificar-com-junction-ausente.txt  641  fbcb0cd6…
    controle-negativo/nc-b/restaurar-com-drift.txt             930  7f5a79f8…
    controle-negativo/nc-c/ciclo-limpo.txt                    3302  ad563693…
    dump/Assembly-CSharp.decompiled.cs                    17815971  (varredura ilspycmd, exit 0)

## 9. RUNBOOK PARA O KIT-14 (como usar)

    cd /c/dev/stolen-realm/scratch/kit
    # 1. jogo do dono FECHADO e frente livre (o harness recusa se nao estiver)
    bash kit16-save-isolado.sh status
    # 2. rodada isolada completa (dados + BepInEx do KIT-03 + registro):
    EVID_DIR=<dir-de-prova> SECONDS_GAME=120 bash kit16-save-isolado.sh run
    # 3. se algo falhar no meio: restaurar (recusa com o jogo aberto)
    bash kit16-save-isolado.sh restaurar
    # 4. limpar a area isolada depois de restaurar
    bash kit16-save-isolado.sh limpar

Variaveis uteis: `REAL_DIR` (alvo), `ISO_ROOT`, `EVID_DIR`, `SECONDS_GAME`,
`MARCADOR`/`PROBE_MARCADOR`, `APPID`, `STEAM`, `REG_PATH`, `GAME_RUNNING_OVERRIDE`.

**Saida para o consumidor (KIT-14):** o ambiente de dados descartavel agora pode
ser criado por comando e restaurado por comando, com prova de hash. O KIT-14 deve
chamar `preparar` **antes** de instalar/lancar e `restaurar` **depois** de
encerrar por PID, dentro da mesma frente unica.

## 10. PRESERVACAO

- Perfil do dono (r2modman/BepInEx): nao usado nem escrito (LogOutput com mtime
  anterior as rodadas); `AUT4Probe` continua ausente dele.
- `lib/Assembly-CSharp.dll`, produto, mods, `KANBAN.md`, politica/modelos/crons:
  intocados. Nenhum `git add`/commit/push.
- Sem build C#/deploy/publicacao. Nada instalado no perfil do dono.
