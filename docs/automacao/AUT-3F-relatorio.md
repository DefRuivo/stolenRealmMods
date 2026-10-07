# AUT-3F — correção dos 4 achados da revisão AUT-3R (t_7d66d0b7)

Implementação do conserto dos 4 achados **ALTERAÇÕES NECESSÁRIAS** da `AUT-3R-revisao.md`,
com TDD (RED antes / GREEN depois), contra-provas reais e bancada completa reexecutada em
**cópia isolada**. HEAD `f526fe9b71f5` @ `ci-validate-test`. Nenhum deploy, install, jogo,
save, commit/push ou publicação. Nenhum kanban mutado.

## Resumo dos 4 consertos

| # | Achado AUT-3R | Correção | Prova |
|---|---|---|---|
| 1 | Builds herdam `USERPROFILE/APPDATA/LOCALAPPDATA` reais; deploy contido só pela flag; builds rodam ANTES de `check_deploy_optin` | `montar_env_isolado` + `propriedades_isolamento` (env e props MSBuild do build apontam p/ sandbox); `preflight_deploy` roda `check_deploy_optin` **ANTES** de qualquer build, `gate_builds` **FAIL-CLOSED** (sem OK não builda); cache NuGet real preservado via `NUGET_PACKAGES` | `t_aut3_isolamento` (3+3+3 checagens) + contra-prova real com csproj sem Condition |
| 2 | `guarda_repo` não hasheia untracked recursivo (`git status -z` colapsa `tools/automacao/` e `docs/automacao/`): 78 arquivos, **0** desses | `lista_repo` = `git ls-files -z` + `git ls-files -z --others --exclude-standard` (recursivo, não colapsa); `comparar_snapshot` reporta criado/removido/alterado; exclusão **explícita** só dos outputs do runner (`AUT-3-resultado.json`, `AUT-3-resumo.md`) + `scratch/` (área externa) | `t_aut3_isolamento` (5+4+2 checagens); bancada real: **78 → 457 arquivos**, 28 de `tools/automacao` e 8 de `docs/automacao` agora hasheados |
| 3 | `--sem-build`/`--sem-suite`/`suite_jogo` omitida mantinham **VERDE**; `AUT-REUSE` era `OK_OFFLINE` hardcoded | `estados_fases` injeta `NAO_EXERCITADO` por fase pulada (nunca verde); `montar_cobertura` marca `M*` pulado como `NAO_EXERCITADO` (não `REPROVADO`); `AUT-REUSE` **derivado** de prova (alvos de reuso presentes + suite OK), sem OK hardcoded | `t_aut3_isolamento` (12+1+3+2) + `t_aut3_runner` (novo critério → `NAO_EXERCITADO`) |
| 4 | `check_segredos.py:52` e `check_padroes_segredo.mascara` imprimem 14 chars do token; runner gravaria o prefixo em `detalhe` | scanners imprimem apenas `<REDACTED: N chars>` / `<REDACTED> (N chars, entropia X)`; `aut3_lib.sanitiza` limpa toda captura antes de serializar (`_detalhe`), sem esconder exit/estado | `t_aut3_segredos` (12) + `t_aut3_lib` (`sanitiza`) |

## TDD — RED antes / GREEN depois

### RED (contra o código original)
```
python tools/automacao/offline/testes/t_aut3_lib.py       -> AttributeError: module 'aut3_lib' has no attribute 'sanitiza' (exit 1)
python tools/automacao/offline/testes/t_aut3_isolamento.py-> AttributeError: module 'bancada_aut3' has no attribute 'montar_env_isolado' (exit 1)
python tools/automacao/offline/testes/t_aut3_segredos.py  -> AttributeError: module 'aut3_lib' has no attribute 'sanitiza' (exit 1)
```
O teste novo do guarda também **pegou um defeito real durante a GREEN**: `lista_repo` devolvia
vazio porque `git ls-files` (sem `-z`) era splitado em NUL — o teste `untracked RECURSIVO entra`
ficou `REPROVOU` até a correção (`git ls-files -z`).

### GREEN (código entregue)
```
python tools/automacao/offline/testes/t_aut3_lib.py        exit=0  total: 25 | falhas: 0
python tools/automacao/offline/testes/t_aut3_isolamento.py exit=0  total: 46 | falhas: 0
python tools/automacao/offline/testes/t_aut3_segredos.py   exit=0  total: 12 | falhas: 0
python tools/automacao/offline/testes/t_aut3_runner.py     exit=0  total: 7  | falhas: 0
```
Sem regressão na suíte principal (inalterada por este trabalho):
```
python tools/testes/roda_testes.py --puros --json        exit=0  {'PASSOU': 85}
python tools/testes/roda_testes.py --contra-prova --json exit=0  {'PROVA_OK': 49, 'PASSOU': 14}
```

### Contra-provas dos 4 consertos (defeito plantado → correção)
- **(1)** `test_preflight_fail_closed_real`: csproj `DeployToBepInEx` **sem** `Condition` →
  `preflight_deploy` = `REPROVOU` e `gate_builds` = **False** (não builda); com a `Condition`
  → exit 0 e gate `True`.
- **(2)** `test_lista_repo_recursiva`/`test_comparar_snapshot`: dir novo não colapsa; detecta
  criado/removido/alterado; output autorizado e `scratch/` ficam fora; ignorado (`.gitignore`) fica fora.
- **(3)** `test_estados_fases`: cada fase pulada → `NAO_EXERCITADO` e `veredito != VERDE`;
  `test_aut_reuse_derivado`: sem os alvos de reuso → `NAO_EXERCITADO`, com eles → `OK_OFFLINE`.
- **(4)** `t_aut3_segredos` roda os scanners REAIS numa cópia com token FALSO: exit 1,
  **nem o valor nem os 14 chars** aparecem na saída, `<REDACTED>` presente; após remover o token, exit 0.

## Bancada completa em cópia isolada (rodada real, 6 builds)

A cópia do repo foi feita em `$SCRATCH/bench/repo` (sem `scratch/`, 45 MB, com `.git`, `bin/Release`
e `dist/`). O PathMap foi **ancorado no repo REAL** por uma âncora separada (`--ancora`), de modo que
a DLL do sandbox embute o caminho real — **sem** apontar `--repo` para o repo real (isolamento preservado).

```
python tools/automacao/offline/bancada_aut3.py \
    --repo <scratch>/bench/repo --ancora C:/dev/stolen-realm \
    --trabalho <scratch>/bench/trabalho --jogo
exit = 0  (BENCH_EXIT=0)  ->  VERDE
```

- **Builds 6/6 OK**, `-c Release -p:DeployToBepInEx=false`, `fonte = Release = perfil` por sha, e
  **idênticos à entrega AUT-3**:

  | mod | sha (sandbox=Release=perfil) |
  |---|---|
  | BetterCombatText | `06dae5aa7b5e` |
  | BetterFont | `2c07f5e959af` |
  | BetterStats | `5a3c001ad424` |
  | BetterTooltips | `270f311b0f7b` |
  | RoguelikeDebugger | `99c156799380` |
  | RoguelikeSkillTreeVisualizer | `454587a031a3` |

- **Isolamento registrado no JSON**: `USERPROFILE/APPDATA/LOCALAPPDATA` sob `.../bench/trabalho/isolamento/*`
  (+ props MSBuild `-p:USERPROFILE=…`, `-p:APPDATA=…`, `-p:LOCALAPPDATA=…`); `NUGET_PACKAGES` =
  `C:\Users\Pichau\.nuget\packages` (cache real preservado).
- **`preflight_deploy`**: `OK` (7 alvos de deploy, todos com `Condition`), `bloqueou=False`.
- **Guarda de repo**: `arquivos=457`, `criados=[] removidos=[] alterados=[]` → **intacto**.
  (Era 78 na entrega; agora inclui 28 de `tools/automacao` e 8 de `docs/automacao`, e exclui o
  output `AUT-3-resultado.json` explicitamente.)
- **Guarda de perfil**: 28 arquivos hasheados, `intacto=True`; conferido de forma independente
  antes/depois com `sha256sum` **byte a byte** (28/28 idênticos) no perfil real.
- **Checagens 11/11 OK** (inclui `check_segredos`, `check_deploy_optin`, `pacotes_preflight`, `audita_docs`).
- **Suíte**: 85 puros · 49 `PROVA_OK` + 14 PASSOU (contra-prova) · 1 jogo.
- **Contra-provas 5/5 `PROVA_OK`**.
- **Cobertura** (matriz AUT-2, sha `8503010272d7`): `OK_OFFLINE 8 · PARCIAL 0 · NAO_EXERCITADO 12 · REPROVADO 0`.

## Verificação de ausência de efeito colateral (repo/perfil REAL)

| leitura | antes | depois |
|---|---|---|
| `AUT-3-resultado.json` sha256 | `9c1aa58244ed…` | OK (byte a byte) |
| `AUT-3-resumo.md` sha256 | `89f0fe669672…` | OK (byte a byte) |
| `AUT-3-relatorio.md` sha256 | `0efe68d2c733…` | OK (byte a byte) |
| perfil BepInEx (plugins+config) | 28 arquivos | 28 idênticos |
| `git status --porcelain \| wc -l` | 82 | 82 |
| HEAD | `f526fe9b71f5` | `f526fe9b71f5` |
| processos `dotnet`/jogo | 0 | 0 (build-server encerrado com `dotnet build-server shutdown`) |

Os `docs/automacao/AUT-3-*` do repo real **não foram sobrescritos** (a bancada escreveu apenas na cópia).

## Arquivos tocados (hashes sha256)

```
tools/automacao/offline/aut3_lib.py                   d6075ce636bce480a17ec56fce921bed4dba953976d799e38f8ae2f9f42440f5
tools/automacao/offline/bancada_aut3.py               627c91e3fe64809860ed130e1ff7c55220e2891504c4f8af6be9fb72653fd99f
tools/automacao/offline/contra_provas.py              01e62e200ad2e46a2280beba776e5c1f2a2727a712ac8c0c183779bc6a5b57c6  (inalterado)
tools/automacao/offline/testes/t_aut3_lib.py          66c06a2a9e06f43d46ec54cc58543e5116ca4eff36c09bf68061ffbb6446c50c
tools/automacao/offline/testes/t_aut3_isolamento.py   7c83e58cb5b820a32d7414eaa0760b623c95adea52e6159b52dfc6a839e2d5a1  (novo)
tools/automacao/offline/testes/t_aut3_segredos.py     6b612da927d874e1788ae2685150c78e82ca9386ed140d2efb5d6c43e33ba577  (novo)
tools/automacao/offline/testes/t_aut3_runner.py       68b3e89bb594c09880be37db03486ebc73369a794950f5da75f3668cc31620f9
tools/check_segredos.py                               7c888e7cbd2b5cff0b23c41c16ecd8fe6778776601793df1c846a2900303d091
tools/check_padroes_segredo.py                        2f9265e2ad933e9a228565129af0510cb7e39d181320e9b012cc27277aa236bd
docs/automacao/AUT-3F-relatorio.md                    (este relatório)
```

## Lacunas / não coberto (não é OK)

- **Runtime de jogo** segue fora do escopo offline: `T-RSTV21/25B/26`, `S-RV-26…34`, `BUG34`
  permanecem `NAO_EXERCITADO` (exigem jogo/dono — AUT-4/6). `T-RSTV25B` continua INDETERMINADO.
- **Publicação online** não verificada (AUT-3F não publica).
- **`--sem-build` agora reprova por artefato ausente**: no sandbox sem build, `pacotes_preflight`
  não acha as DLLs e sai `REPROVOU` — o veredito é não-verde (correto), mas o rótulo é `REPROVADO`,
  não `INCOMPLETO`. Não enfraquece a trava; fica registrado para o revisor.
- O isolamento redireciona `LOCALAPPDATA`, então caches do MSBuild são recriados no sandbox
  (builds um pouco mais lentos); o cache NuGet real é reaproveitado (`NUGET_PACKAGES`).
- A cópia da bancada é um snapshot do repo no momento do run (HEAD `f526fe9`); alterações de
  terceiros depois disso não entram.
- Nenhuma mudança em `tools/testes/**` nem nas travas existentes; `roda_testes.py` segue com os
  mesmos 85 puros + 49/14.

> AUT-3F não substitui aceite humano nem publicação do DoD. Não marcar done — o pai faz a revisão
> independente por outro agente.
