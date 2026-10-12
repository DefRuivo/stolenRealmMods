# KIT-14G-SEG2 — parte02: a rodada de 3 boots foi TENTADA; bancada pronta, bloqueio de HANDLE identificado

Cartão `t_139f714f`. Rodada `default/run885`, 11/10/2026 18:38–18:50 (BRT). Esta parte **não** fecha o
aceite. Ela entrega: (1) a bancada da rodada da §5 do cartão, executada e validada até o ponto em que
o ambiente do dono permite; (2) o **diagnóstico exato do bloqueio** que impede a montagem do ambiente
isolado; (3) a receita de retomada. Nada aqui é apresentado como medido em jogo — §7 declara o não
exercitado.

## 1. O que a rodada fez (e o que parou)

Boot `F-marcadores` (rota `Play;Roguelike;Accept`, probe só, `CliqueFisico=false`,
`CliqueFisicoEstavel=0`, `SilencioAposClique=false`, janela 150 s) foi lançado pela bancada nova
`scratch/kit/KIT-14G-SEG2-run885/roda-seg2.py`. Sequência medida (`F-marcadores-commands.json`):

| passo | resultado |
|---|---|
| guardas (0 jogo, sem junction/backup, raiz isolada ausente) | OK |
| identidade (fonte `beaf965a…` / DLL `7f9a4cf1…` repo = sandbox) | OK |
| `cloud_start` (app 1330000 `cloudenabled=[0]`) | OK |
| `front-check` / `front-acquire` | exit 0 / exit 0 |
| `bepinex-preparar` (perfil BepInEx isolado) | exit 0 |
| `dados-preparar` (`kit16-save-isolado.sh preparar`) | **exit 2 — ver §2** |
| limpeza: `bepinex-rollback` / `front-release` | exit 0 / exit 0 |

O jogo **não** foi lançado. O `finally` blindado do driver rodou inteiro: `game_closed=true`, frente
liberada, perfil BepInEx isolado removido.

## 2. O erro exato (comando e saída)

`kit16-save-isolado.sh preparar` fez 1/5 snapshot (107 linhas, `\c51394a2…`), 2/5 cópia (106
arquivos), 3/5 export do registro (exit 0) e parou em 4/5:

```
[18:41:45] 4/5 rename do diretorio REAL -> C:\Users\Pichau/AppData/LocalLow/Burst2Flame Entertainment/Stolen Realm.kit16-real (rename, sem apagar nada)
mv: cannot move 'C:\Users\Pichau/AppData/LocalLow/Burst2Flame Entertainment/Stolen Realm' to 'C:\Users\Pichau/AppData/LocalLow/Burst2Flame Entertainment/Stolen Realm.kit16-real': Device or resource busy
[18:41:46] ERRO: rename falhou
```

Evidência bruta: `scratch/kit/KIT-14G-SEG2-run885/F-marcadores-result-preparo.json`
(`error: "RuntimeError: dados-preparar exit 2"`) e o `dados-preparar.stderr.log` citado acima.

Fonte provável do erro: `scratch/kit/kit16-save-isolado.sh:226` (`mv "$REAL_DIR" "$BAK_DIR" || die
"rename falhou"`). O mesmo bloqueio já havia aparecido mais cedo hoje (11/10 14:14) na tentativa de
sessão do clique físico (`Move-Item:54`).

## 3. Onde está o bloqueio (medido, não suposto)

Sondas READ-ONLY (nenhuma renomeia, nenhuma encerra processo), em
`scratch/kit/KIT-14G-SEG2-run885/probe-*.ps1|log`, `quem-segura*.ps1|log`:

| sonda | resultado |
|---|---|
| `CreateFileW(<dir real>, DELETE, share=READ+WRITE)` | **FALHOU err=32** (ERROR_SHARING_VIOLATION) |
| `CreateFileW(<dir real>, DELETE, share=READ+WRITE+DELETE)` | **FALHOU err=32** |
| mesma sonda 30× a cada 3 s (`probe-repetido.log`) | **bloqueado 30/30** — não é transitório |
| `CreateFileW(LocalLow, DELETE, share=RWD)` | OK (livre) |
| `CreateFileW('Burst2Flame Entertainment', DELETE, share=RWD)` | OK (livre) |
| 88 arquivos na raiz do save (DELETE/share=RWD) | **0 bloqueados** |
| 10 subdiretórios da árvore (DELETE/share=RWD) | **0 bloqueados** |

⇒ O bloqueio é um handle sobre o **objeto DIRETÓRIO** `…\Stolen Realm` — não sobre os saves (nenhum
arquivo travado), não sobre a pasta-mãe, não sobre subpastas. Um rename de diretório exige que o
objeto diretório não esteja aberto; é exatamente isso que o `mv` reporta como "Device or resource
busy".

Consulta à **Restart Manager** (`quem-segura2.ps1`): `RmStartSession=0`,
`RmRegisterResources=0`, `RmGetList` → **rc=5 (ERROR_ACCESS_DENIED)** — sem elevação a RM não enumera
o dono do handle.

## 4. CULPADO IDENTIFICADO: o workspace do VS Code do dono

Sysinternals `handle64.exe` (baixado só para a consulta, removido depois; saída preservada em
`handle64-evidence.txt`):

```
Code.exe           pid: 30552  ... 518: C:\Users\Pichau\AppData\LocalLow\Burst2Flame Entertainment\Stolen Realm
Code.exe           pid: 30552  ... 540: C:\Users\Pichau\AppData\LocalLow\Burst2Flame Entertainment\Stolen Realm
Code.exe           pid: 25708  ...  58: C:\Users\Pichau\AppData\LocalLow\Burst2Flame Entertainment\Stolen Realm
Code.exe           pid: 23792  ...  58: C:\Users\Pichau\AppData\LocalLow\Burst2Flame Entertainment\Stolen Realm
Code.exe           pid: 15252  ...  58: C:\Users\Pichau\AppData\LocalLow\Burst2Flame Entertainment\Stolen Realm
dotnet.exe         pid: 24788  ...  58: C:\Users\Pichau\AppData\LocalLow\Burst2Flame Entertainment\Stolen Realm
Microsoft.CodeAnalysis.LanguageServer.exe pid: 24116 ... 58: C:\Users\Pichau\AppData\LocalLow\Burst2Flame Entertainment\Stolen Realm
```

A causa está no próprio repositório: `biblioteca-de-terceiros.code-workspace` lista a pasta de saves como
**pasta do workspace** (linha 4):

```json
"path": "../../Users/Pichau/AppData/LocalLow/Burst2Flame Entertainment/Stolen Realm"
```

Correlação de tempo (BRT), coerente com a causa:

| quando | o que |
|---|---|
| 10/10 19:36 | boots A/B do run714 **funcionaram** (o rename passou) — VS Code ainda não estava aberto |
| 11/10 03:07:13 | abre o VS Code (`Code.exe` mais antigo vivo: pid 9444) |
| 11/10 14:14 | primeira recusa de rename (`Move-Item:54`) — depois do VS Code |
| 11/10 18:41 | `dados-preparar exit 2` desta rodada |

Residual honesto: o `handle64` lista o handle, mas **não** expõe o modo de compartilhamento, então não
é possível provar *por esse binário* que é exatamente aquele handle que nega DELETE. O que está
provado: (a) o caminho exato está aberto por processos do VS Code; (b) o objeto diretório nega DELETE
de forma persistente; (c) a pasta-mãe, os 88 arquivos e as 10 subpastas estão livres; (d) a linha do
tempo fecha com a abertura do VS Code. Conjunto forte; não é uma prova única e definitiva.

## 5. Ação mínima do dono (nenhuma delas exige reboot)

1. **Fechar a janela do VS Code** que tem o workspace `biblioteca-de-terceiros.code-workspace` aberto
   (é o caminho mais garantido: solta todos os handles das 4 pastas do workspace).
2. Ou, mantendo o VS Code aberto, **remover a pasta da linha 4** de
   `biblioteca-de-terceiros.code-workspace` (a pasta de saves) e recarregar a janela.
3. Ou acrescentar às configurações do workspace `"files.watcherExclude": {"**/AppData/LocalLow/**":
   true}` e recarregar — impede o watcher de segurar a pasta (menos garantido que (1)/(2), porque o
   Explorer/FileService do VS Code também abre pastas do workspace).

Depois de qualquer uma delas, a retomada é um comando (ver §6) — o operador não precisa montar nada à
mão.

## 6. Receita de retomada (bancada pronta, sem trabalho novo)

```bash
cd C:/dev/stolen-realm/scratch/kit/KIT-14G-SEG2-run885
python roda-seg2.py F-marcadores 0 0 0 150     # controle: reproduz a morte + ultimo marco
python roda-seg2.py F-silencio   0 0 1 150     # discriminador: instrumento x inicio da run
python roda-seg2.py F-gate       1 10 0 150    # candidato a correcao (gate de clique fisico)
```

Cada boot exige que `scratch/kit/KIT-14G-SEG2-run885/<label>/` **não** exista (a bancada recusa reuso
de raiz isolada). A bancada confere sozinha: 0 processos do jogo, sem junction/backup pendente,
identidade fonte/DLL repo = sandbox (`beaf965a…` / `7f9a4cf1…`), cloud do app 1330000 OFF, frente
única. Ao fim de cada boot ela grava `*-identity.json`, `*-pos-estado.json`, `*-eventlog.json` e
compara o save do dono com o **snapshot imediato da própria rodada**.

**Mudança declarada na bancada (uma só):** o guard de dados de produção. O guard histórico
(`production_diff()` contra o manifesto do KIT-16 de 10/10) hoje dá `equal=False` — o dono jogou
(`before=111, after=106, 4 novos, 9 removidos, 8 alterados`; medido nesta rodada e registrado em
`F-marcadores-identity.json.baseline_producao`), e o driver abortaria **antes** de qualquer boot. A
investigação deste mesmo cartão (`KIT14G-SEG2-investigacao-parte04.md` §4) manda substituir a
comparação histórica por **snapshot imediato por rodada**; é o que a bancada faz: tira o manifesto do
save real segundos antes do boot (`*-antes-manifesto-imediato.manifest`) e o re-mede no fim
(`*-depois-manifesto.manifest`), comparando byte a byte. A proteção durante a rodada não mudou (rename
+ junction + restauração por conteúdo do `kit16-save-isolado.sh`). O baseline histórico continua sendo
medido e registrado, só não bloqueia mais a rodada.

## 7. NÃO EXERCITADO (sem número inventado)

* **nenhum boot chegou a abrir o jogo** — a montagem do ambiente isolado parou no rename; portanto o
  ponto exato do `c0000005`, o `F-silencio` e o `F-gate` seguem **não medidos**. O aceite **não** está
  fechado;
* **não** foi feita nenhuma tentativa de soltar o handle do VS Code (nem fechar, nem `handle -c`, nem
  matar processo): fechar o editor do dono é ação dele; o autorizador mandou **não forçar** e declarar
  o bloqueio;
* **não** foi tocado o perfil real, o save real, o registro, o Cloud, nem feito deploy/commit;
* a atribuição "é o handle do VS Code que nega o DELETE" é **correlação forte, não prova única** (§4);
* o `handle64.exe` não ficou na árvore — só a saída.

## 8. Estado do ambiente do dono (medido ao fim)

| item | estado |
|---|---|
| processos do jogo | 0 |
| `…\LocalLow\Burst2Flame Entertainment\Stolen Realm` | diretório normal (não junction), íntegro |
| backup `Stolen Realm.kit16-real` | não existe |
| save real vs snapshot imediato desta rodada | **106/106 arquivos, 0 novos, 0 removidos, 0 alterados** (`F-marcadores-pos-estado.json`) |
| frente única | liberada (`front-release exit 0`) |
| perfil BepInEx isolado | removido (`bepinex-rollback exit 0`) |
| cópia isolada dos dados | removida junto com o diretório do boot (126 MB; nenhum dado pessoal ficou em `scratch/`) |
| `cloud_end_before_restore` | `cloudenabled=[0]` |

## 9. Evidência desta rodada (hash ao lado do arquivo)

`scratch/kit/KIT-14G-SEG2-run885/`: `roda-seg2.py` (bancada), `F-marcadores-identity.json`,
`F-marcadores-pos-estado.json`, `F-marcadores-result-preparo.json`, `F-marcadores-commands.json`,
`F-marcadores-config-declarada.json`, `F-marcadores-{antes,depois}-manifesto*.manifest`,
`F-marcadores-eventlog.json`, `probe-*.ps1|log`, `quem-segura*.ps1|log`, `handle64-evidence.txt`,
`F-marcadores-expanded.py`.

Hashe desta rodada: bancada `roda-seg2.py` = `c1a89218…` (sha256 completo no
`F-marcadores-identity.json.fonte_modulo_sha256`); fonte do instrumento `beaf965a…`; DLL `7f9a4cf1…`.
