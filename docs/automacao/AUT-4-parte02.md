# AUT-4 — parte 02: Fase A (offline), pré-voo e a rodada r1 (falha honesta)

> Cartão `t_b8b9822e` · worker `default` · run 622 · 2026-10-09, 18:4x–18:5x BRT.
> Continua `AUT-4-parte01.md`. Nada aqui é aceite humano: são medições e execuções reais.
> Nesta rodada **nenhum** documento de preparação (`AUT-4-preparacao.md`, `AUT-4-estado.json`,
> `AUT-4-runbook-rodada-autorizada.md`), nenhum arquivo de mod e nenhum arquivo do jogo foi editado.

## 1. Fase A — suíte offline NO ESTADO ATUAL do disco (execução real)

Ambiente hermético (`USERPROFILE`/`APPDATA`/`LOCALAPPDATA` redirecionados para pasta de trabalho).

| comando | resultado real |
|---|---|
| `python tools/automacao/runtime/roda_testes_runtime.py` | **VERDE, exit 0 — 15/15** |
| `... --contra-prova` | **VERDE, exit 0 — 31/31**, todas por `RESULTADO|REPROVOU|`, **zero** por “exceção inesperada” |

Hashtes reconferidos por `sha256sum` nesta rodada (não lidos do JSON de estado) — **todos casam**:

| artefato | sha256 |
|---|---|
| `AUT4Probe/AUT4ProbePlugin.cs` | `48afd3c41cf3ba97c93e5fc2d6b02ca58298939bf4b2a51f0ccd159ec96e3e94` |
| `AUT4Probe/bin/Release/AUT4Probe.dll` | `407c5c63d9d70df3ea03c6232717060ce3b0b9567bacdb553a6043238d519bc7` |
| `coletor.py` | `adb48dca024120db91b65e28b8842b7f303ca1725359cdaf4deab5530ae1dd46` |
| `roda_testes_runtime.py` | `7906c1692bf349aff006039f73bbc8c59ef4e2a7a588210c348227be4dfb157e` |
| `controle_negativo.py` | `053c0026f97c8541294c81e9d0011df4f3d970756f6ab8bc1d96a98fa9296659` |
| `lib/Assembly-CSharp.dll` (**do jogo**) | `8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a` (**intacta**) |

## 2. Fase B — pré-voo (medido)

| item | medido | resultado |
|---|---|---|
| processo do jogo | `tasklist \| grep -i stolen` → vazio | **FECHADO** (não foi preciso declarar reinício) |
| frente única | `bash scratch/kit/front-unica.sh check` → “lock disponivel”, exit 0; depois `acquire` → **lock OK (holder PID 978)** | nenhuma outra frente controla o jogo |
| raiz isolada | `scratch/aut4-runtime-iso` (**fora** de `…\profiles\Default\BepInEx`) | containment OK |
| cópia do BepInEx | `core/` do dono → `<iso>/BepInEx/core` (**18 arquivos**), `plugins/` e `config/` **vazios** | só o probe será carregado |
| loader do jogo | `E:\…\Stolen Realm\winhttp.dll` + `doorstop_config.ini` presentes | porta de doorstop disponível |

**Impressão do dono ANTES (prova de isolamento), função `hash_tree` (`rel|bytes|mtime` → sha256):**

```
perfil_plugins=6eae7a3c1b38dbc9a3574961138d7797cf3df8127229dd4ebff9ab76543ef9df
perfil_core=b159420072809cd904fcedc954ca863437e3ea1adb02af05f0a6b84f3066b535
perfil_log=9bedadac295116a9bf1b2bc48648600f5535296d1ce24b71ad08bed10772fee2
saves_hash=04ef12fa9df8926faad47d8969386efa3bc450cc3603a3372115cdf2a684a365
```

(Arquivo: `docs/automacao/AUT-4-evidencias/antes.txt`.)

## 3. Rodada r1 — o `--perfil` errado: o instrumento **não** foi carregado, e o resultado foi honesto

**Erro de configuração meu (do worker), registrado de propósito:** passei
`--perfil …/scratch/aut4-runtime-iso/BepInEx`. O contrato do driver compõe o preloader como
`<perfil_dir>/BepInEx/core/BepInEx.Preloader.dll`, então o alvo de doorstop virou
`…/aut4-runtime-iso/BepInEx/**BepInEx**/core/BepInEx.Preloader.dll` — caminho inexistente. O jogo
**subiu** (o `steam -applaunch` funciona), mas **sem BepInEx nenhum**: não houve log, não houve JSON,
não houve leitura.

Resultado real do driver (`docs/automacao/AUT-4-evidencias/r1-falha/resultado-r1.json`):

| campo | valor |
|---|---|
| `status` | **`NAO_EXERCITADO`** |
| `exit_code` | **2** |
| `motivo` | `o probe nao deixou saida ({'log_ok': False, 'json_ok': False, 'fase': None, 'status': None, 'segundos': 240.194})` |
| `observacoes` | **vazias** (zero leitura) |
| `dados_sinteticos` | **`false`** |
| `hot_reload` | **`false`** |
| `encerramento` | PID 27420, `modo=por-pid`, tentativa **graciosa** (`CloseMainWindow`) → `fechado: true` |
| `restauracao` | `{"limpo": true, "residuos": [], "divergentes": [], "faltando": []}` |
| perfil/saves do dono | **idênticos** ao “antes” (diff vazio) |

**Por que isto é evidência útil e não um acidente perdido:** é a **prova em runtime** do critério
do cartão “*caminho sem acesso autorizado ao jogo retorna incompleto, **jamais** dados fabricados*”.
Sem instrumentação, o driver **não inventou** nada: devolveu `NAO_EXERCITADO`, exit 2, observações
vazias e `dados_sinteticos=false`; esperou o teto, **fechou só o PID que ele mesmo abriu** (gracioso)
e fez rollback limpo. É também o primeiro exercício **em jogo** do caminho de encerramento por PID.

O conserto foi de parâmetro, não de código: `--perfil` tem de ser a **raiz** do perfil (a pasta que
contém `BepInEx/`). Nenhuma linha do instrumento foi alterada para isso — e os hashes §1 continuam
valendo nas rodadas seguintes (conferidos de novo no `cfg-instalado.cfg` de cada rodada).
