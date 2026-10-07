# AUT-3FR — revisão independente da AUT-3F (t_ee77c9fa)

Revisor **não-autor** (subagente independente). HEAD revisado: `f526fe9b71f5` @ `ci-validate-test`.
Escopo: os **4 consertos** de `docs/automacao/AUT-3F-relatorio.md` + **bancada FULL em cópia** +
**contra-provas novas** (mini projeto MSBuild real, guarda do git, sanitização com credenciais
fictícias variadas). Nada de deploy, jogo, save, install, commit, push ou publicação. Kanban **não
mutado**; nenhuma tarefa marcada `done`. Produto (`tools/**`, csproj) **não editado** por esta revisão.

Método: execução REAL em cópia isolada (`--repo <cópia> --ancora C:/dev/stolen-realm`), com
`TMP`/`TEMP`/`TMPDIR` apontados para o scratch desta rodada. Evidências em
`C:/Users/Pichau/AppData/Local/hermes/cache/scratch/aut3fr/`
(`aut3fr-evidencia.json` sha256 `ae82ac840d5d…`, `result_full.json` `045719d7e255…`).

## Hashes da entrega (conferem com o declarado na AUT-3F)

| arquivo | sha256 (4 primeiros · comprimento) | bate? |
|---|---|---|
| aut3_lib.py | `d6075ce636bc…f5` | SIM |
| bancada_aut3.py | `627c91e3fe64…9f` | SIM |
| contra_provas.py | `01e62e200ad2…c6` | SIM |
| testes/t_aut3_lib.py | `66c06a2a9e06…0c` | SIM |
| testes/t_aut3_isolamento.py | `7c83e58cb5b8…a1` | SIM |
| testes/t_aut3_segredos.py | `6b612da927d8…77` | SIM |
| testes/t_aut3_runner.py | `68b3e89bb594…f9` | SIM |
| tools/check_segredos.py | `7c888e7cbd2b…91` | SIM |
| tools/check_padroes_segredo.py | `2f9265e2ad93…bd` | SIM |

Cada sha256 completo está em `AUT-3F-relatorio.md` e foi reconferido byte a byte no disco.

## Veredito por requisito

| # | requisito | veredito | prova |
|---|---|---|---|
| 1 | Env + props MSBuild redirecionam `USERPROFILE/APPDATA/LOCALAPPDATA`; `NUGET_PACKAGES` real; preflight **antes** do build e **fail-closed** | **OK** | FULL: `isolamento.env` ⇒ 3 dirs sob o scratch + `NUGET_PACKAGES=C:\Users\Pichau\.nuget\packages`; `isolamento.props` = 3 `-p:…`; `preflight_deploy` estado `OK`,`bloqueou=False`. Contra-prova real (mini csproj sem `Condition`): preflight `REPROVOU` (exit 1) e `gate_builds=False` (não builda); com a `Condition` ⇒ `OK`/`True` |
| 2 | Guarda de repo **recursiva** (`ls-files -z` track+untracked) detecta criado/removido/alterado; exclusões não excessivas | **OK (com ACHADO A1)** | `guarda_repo=458 arquivos`, `intacto`, inclui 28 de `tools/automacao` e 9 de `docs/automacao` (o furo da AUT-3R era **0** desses). Repro `fix2_git.py`: dir novo aninhado entra; criado/removido(`git rm`)/alterado detectados; ignorado fora; exclusão só dos 2 outputs do runner + `scratch/` |
| 3 | Fases puladas **nunca** viram VERDE — pelo **CLI real**, não só helper | **OK** | `fix3_fases.py` (CLI real em cópia): `--sem-build`⇒`REPROVADO` exit **1**; `--sem-suite`⇒`INCOMPLETO` exit **2**; sem `--jogo`⇒`INCOMPLETO` exit **2**; `--sem-contra-provas`⇒`INCOMPLETO` exit **2**; `qualquer_verde=False`. `AUT-REUSE` **derivado** de prova (sem `OK_OFFLINE` hardcoded) |
| 4 | Scanners reais e JSON/saída **sem prefixo** de credencial; prefixos reais não vazam | **OK (com LIMITE A2)** | `fix4_segredos.py`: `check_segredos.py` e `check_padroes_segredo.py` sobre arquivo com **16 credenciais fictícias** variadas ⇒ exit 1, `vaza_prefixo=[]` (**nada** do valor/prefixo14), `<REDACTED>` presente. `aut3_lib.sanitiza` cobre 13 formatos (tss/ghp/gho/github_pat/sk/AIza/glpat/npm/xox/AKIA/Basic/x-access-token (valor mascarado)der); `_detalhe` sanitiza a captura antes de serializar |
| 5 | Suítes do implementador não poluem pasta temporária do Windows (requisito scratch) | **ACHADO A3** | `t_aut3_*.py` usam `TemporaryDirectory()` **sem `dir=`** ⇒ `gettempdir()` default = `C:\Users\Pichau\AppData\Local\Temp`; honram `TMP` quando setado (usei scratch) |

**Bancada FULL em cópia — OK.** Reproduzida duas vezes:
`python tools/automacao/offline/bancada_aut3.py --repo <scratch>/copy_repo --ancora C:/dev/stolen-realm --trabalho <scratch>/bench_full --jogo`
⇒ `BENCH_EXIT=0`, **VERDE**; 6/6 builds `-c Release -p:DeployToBepInEx=false`; `fonte=Release=perfil`
por sha, **idênticos à entrega** (`06dae5aa…`, `2c07f5e9…`, `5a3c001a…`, `270f311b…`, `99c15679…`, `454587a0…`);
11/11 checagens `OK`; suíte `85 puros · 49 PROVA_OK + 14 PASSOU · 1 jogo`; 5/5 contra-provas `PROVA_OK`;
cobertura `OK_OFFLINE 8 · PARCIAL_OFFLINE 0 · NAO_EXERCITADO 12 · REPROVADO 0`; `preflight OK`;
`guarda_perfil intacto` (28).

**Snapshot independente (não usa o produto AUT-3) — OK.** `snapshot_aut3fr.py` (walk + sha256) antes/depois:
repo real **4010 arquivos**, perfil BepInEx **51 arquivos** ⇒ **0 criados / 0 removidos / 0 alterados** em
ambos; `snap_antes.json` e `snap_depois.json` **byte-idênticos** (`0f395a659c67…`). As mudanças manuais do dono
(82 entradas de `git status --porcelain`, incluindo `BetterTooltips/Patches/LocalizePatch.cs` etc.) **preservadas**.
`docs/automacao/AUT-3-*` originais intactos: `AUT-3-resultado.json` `9c1aa58244ed…`, `AUT-3-resumo.md`
`89f0fe669672…`, `AUT-3-relatorio.md` `0efe68d2c733…` (conferem com a AUT-3F).

## Achados (fora dos 4 consertos — para o pai decidir)

**A1 · médio · a guarda de repo é FAIL-OPEN quando o git falha.**
`lista_repo`/`snapshot_repo` usam `git ls-files -z …`; `_git_lista_z` **ignora** `exit_code` e `stderr`.
Em dir **não-repo**: `git ls-files -z` ⇒ exit **128**, stdout vazio ⇒ `lista_repo=[]` ⇒ `snapshot_repo={}`
⇒ `comparar_snapshot({},{}) = intacto=True`. Idem se o `git` não existir (`erro_lancamento` preenchido,
stdout vazio). Ou seja, **o guarda afirma "intacto" sem ter lido nada**. Se o git falhar desde o início
(repo sem `.git` / git ausente), a bancada pode sair **VERDE com o guarda cego**. Se falhar no meio
(entre antes/depois), o resultado é falso **REPROVADO** (removidos=tudo) — seguro, mas enganoso.
Repro: `scratch/aut3fr/fix2_git.py` + `ev_fix2.json` (`guarda_em_nao_repo_intacto=true`,
`git_em_nao_repo_exit=128`, `git_inexistente_erro_lancamento=true`).
Sugestão: marcar o guarda `NAO_EXERCITADO`/`REPROVADO` quando a listagem do git falhar (exit≠0 ou
`erro_lancamento`), em vez de "intacto".

**A2 · baixo · `aut3_lib.sanitiza` é a 2ª linha de defesa e tem 2 furos.**
(a) **PEM**: só o cabeçalho `-----BEGIN … PRIVATE KEY-----` é redigido; o **corpo base64 sobrevive**
(`corpo_pem_sobrevive=true`). (b) **Atribuição genérica** (`api_key = …`, `password = …`, `secret: …`)
**não** é coberta por `sanitiza`, embora `check_padroes_segredo.py` a detecte como FORMATO. Hoje **não há
vazamento**: os scanners imprimem só rótulo/contagem/`<REDACTED>`, e o FULL não contém segredo — o furo só
morde se um stdout capturado trouxer esse formato cru. Repro: `scratch/aut3fr/fix4_segredos.py` + `ev_fix4.json`.

**A3 · baixo · testes do implementador usam a pasta temporária do Windows.**
Os 4 `t_aut3_*.py` chamam `TemporaryDirectory()` **sem `dir=`**; default `C:\Users\Pichau\AppData\Local\Temp`.
Contraria a exigência de "área de trabalho scratch". Limpam ao sair, então o impacto é de isolamento/reprodutibilidade.
Repro: `python -c "import tempfile;print(tempfile.gettempdir())"` sem override.

## O que esta revisão NÃO prova (não canonizar)

- **VERDE offline ≠ runtime ≠ DoD.** Permanecem 12 critérios `NAO_EXERCITADO` (runtime de jogo:
  `T-RSTV21/25B/26`, `S-RV-26…34`, `BUG34`) e `T-RSTV25B INDETERMINADO` (LogOutput do próximo boot).
  Publicação online fora do AUT-3. Isso confirma o que a própria AUT-3F declara.
- A cópia é um snapshot no HEAD `f526fe9b71f5`; alterações posteriores de terceiros não entram.
- A fix3 mostra `--sem-build` saindo `REPROVADO` (exit 1, artefato ausente em `pacotes_preflight`) e não
  `INCOMPLETO` — não-verde nos dois casos; rótulo registrado, sem enfraquecer a trava.

## Conclusão

Os **quatro consertos** da AUT-3F: **APROVADOS**. Nenhuma contra-prova nova conseguiu refutá-los; o
isolamento bloqueia antes do build e contém a escrita mesmo com a `Condition` perdida; o guarda de repo é
recursivo e detecta criado/removido/alterado; fases puladas nunca ficam verdes pelo CLI real; scanners e
runner não imprimem prefixo de credencial. Fica **um ACHADO médio (A1, fail-open da guarda em falha do
git)** e **dois baixos (A2, A3)** — endurecer antes de canonizar. Nada aqui aprova runtime, publicação
ou o DoD; a decisão é do pai/dono.
