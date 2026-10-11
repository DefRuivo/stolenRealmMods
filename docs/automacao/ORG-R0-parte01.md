# ORG-R0 — Checkpoint de seguranca do repositorio (parte 01)

Cartao: `t_071b445f` (ORG-R0). Repositorio: `C:/dev/stolen-realm`. Branch: `ci-validate-test`.
Data da execucao: 11/10/2026. HEAD de partida (ultimo commit antes do checkpoint): `d82894ebe95d97f26b7989a848372c691dcb8ef6`
("CI: audita_docs - declara a natureza das citacoes no relatorio REL-BT-014", de 07/10).

OBJETIVO (copiado do cartao): versionar TODO o estado atual do repositorio, sem reorganizar, sem deletar e sem
rodar build, antes de qualquer mexida de organizacao (ORG-R1/ORG-R2). Este e o unico cartao da frente autorizado
a um `git add` amplo.

## 1. O que existia antes do checkpoint

`git status --porcelain=v1 | wc -l` = 565 linhas:

| estado | linhas |
|---|---|
| `??` (untracked) | 517 |
| ` M` (modificado, nao staged) | 48 |

Essas 565 linhas correspondem a **801 arquivos** depois de expandir as pastas untracked
(`git add -A -n` → 801 caminhos).

## 2. Comando usado (staging)

```
git add -A -- . ':(exclude)nul' ':(exclude).worktrees'
```

`git add -A` amplo aqui e a EXCECAO justificada da regra "um commit por frente": o alvo deste cartao e
preservar TUDO como esta, inclusive as edicoes em andamento do dono. As duas exclusoes estao justificadas
na secao 4. Resultado: `add_rc=0`, `git diff --cached --name-only | wc -l` = 801. Em seguida este proprio
artefato foi para o indice (`git add -- docs/automacao/ORG-R0-parte01.md`), totalizando 802 arquivos no commit.

## 3. Inventario do que entrou (contagem por diretorio)

### 3.1 Por diretorio de 1o nivel

| diretorio | novos (A) | modificados (M) | total | tamanho |
|---|---|---|---|---|
| `docs/` | 533 | 3 | 536 | 109,10 MB |
| `tools/` | 189 | 35 | 224 | 2,56 MB |
| `api/` | 29 | 0 | 29 | 0,35 MB |
| `RoguelikeSkillTreeVisualizer/` | 1 | 7 | 8 | 0,23 MB |
| `RoguelikeDebugger/` | 1 | 1 | 2 | 0,03 MB |
| `scripts/` | 1 | 0 | 1 | 0,01 MB |
| `.github/` | 0 | 1 | 1 | 0,01 MB |
| raiz (`README.md`) | 0 | 1 | 1 | 0,04 MB |
| **TOTAL** | **754** | **48** | **802** | **112,3 MB** |

A linha de `docs/` inclui este proprio arquivo (`docs/automacao/ORG-R0-parte01.md`): dos 802 arquivos do commit,
**801 sao o estado herdado do dono** (753 A + 48 M, o que o `git add -A` stageou) e **1 e este artefato
incremental** (o `git add` dele foi feito em seguida, antes do commit). Contagens conferidas por
`git show --name-status --format= HEAD | awk '{print $1}' | sort | uniq -c` → `754 A` / `48 M` / `0 D`.

### 3.2 Detalhe dos dois diretorios grandes (2o nivel)

| caminho | novos (A) |
|---|---|
| `docs/automacao/` | 500 |
| `docs/cobertura/` | 31 |
| `tools/automacao/` | 116 |
| `tools/testes/` | 69 |
| `tools/` (raiz, 4 arquivos soltos) | 4 |

### 3.3 Arquivos novos acima de 1 MB (12 arquivos; os maiores do checkpoint)

| bytes | caminho |
|---|---|
| 45.598.179 | `docs/cobertura/EV-R1/EV-R1-entrega.zip` |
| 27.834.612 | `docs/cobertura/EV-R1/catalogo-referencias.json` |
| 14.343.841 | `docs/cobertura/EV-R1/eventos.json` |
| 2.956.196 | `docs/cobertura/EV-R1/eventos-originais.json` |
| 2.764.203 | `docs/automacao/AUT-4-evidencias/r2-incompleto/01-ui.png` |
| 2.744.135 | `docs/automacao/AUT-4-evidencias/r4-confirmada-log/01-ui.png` |
| 2.506.159 | `docs/automacao/AUT-4-evidencias/r3-confirmada/02-final.png` |
| 2.506.147 | `docs/automacao/AUT-4-evidencias/r3-confirmada/01-ui.png` |
| 1.924.497 | `docs/cobertura/EV-R1/revisao-por-evento.md` |
| 1.853.674 | `docs/cobertura/EV-R1/revisao-por-evento-v2.md` |
| 1.342.507 | `docs/cobertura/EV-R1/lote-Normal.md` |
| 1.292.757 | `docs/cobertura/EV-R1/lote-Normal-v2.md` |

Observacao para o ORG-R1: 109 dos 112,3 MB estao em `docs/` — praticamente tudo em `docs/cobertura/EV-R1/`
(94 MB no total, com o zip de 45,6 MB e os JSONs de 27,8 MB / 14,3 MB). Sao entregaveis: o cartao proibe
deletar entregavel; a decisao sobre versionar ou nao esse peso e do ORG-R1.

### 3.4 Os 48 arquivos modificados (incluidos como estavam)

`.github/workflows/validate.yml`, `README.md`, `RoguelikeDebugger/Plugin.cs`,
`RoguelikeSkillTreeVisualizer/{Plugin.cs, README.md, RemovalWindowSkillsButton.cs, RoguelikeSkillTreeVisualizer.csproj, RunButton.cs, SkillTreesTab.cs, SkillTreesWindow.cs}`,
`docs/automacao/{AUT-4-estado.json, AUT-4-preparacao.md, AUT-4-runbook-rodada-autorizada.md}`, e 34 arquivos sob
`tools/` (automacao/cenarios, automacao/runtime/AUT4Probe, automacao/runtime/coletor.py, automacao/runtime/testes,
checa_shrines.py, check_padroes_segredo.py, check_segredos.py, dados/shrines-esperado.csv, fixtures, gera_shrines_esperado.py,
release-check.sh, testes/**). Lista completa: `git diff --cached --name-only --diff-filter=M` no commit do checkpoint.

## 4. O que ficou FORA do checkpoint (2 itens) — e por que

| caminho | motivo da exclusao | prova |
|---|---|---|
| `nul` | Nome reservado do Windows (dispositivo `NUL`). O git NAO consegue indexar esse arquivo: `git add -n -- nul` → `error: short read while indexing nul` / `error: nul: failed to insert into database` / `fatal: adding files failed` (rc=128). O arquivo nao foi tocado (nem renomeado, nem apagado). Conteudo: 102 bytes de erro de shell (`dir: cannot access '/b': No such file or directory ...`), residuo de um redirecionamento acidental em 08/10. | `git status --porcelain=v1` segue mostrando `?? nul`; `ls -la nul` = 102 bytes |
| `.worktrees/` | Worktree git EMBUTIDO (`.worktrees/level-r2/.git` e arquivo de worktree). Um `git add` nele produziria um **gitlink** (`git add -n .worktrees` → `warning: adding embedded git repository ... add '.worktrees/level-r2/'`), isto e, um pseudo-submodulo nao declarado: o clone externo nao levaria o conteudo e o registro ficaria quebrado. Nada se perde: e o MESMO repositorio no branch `level-r2`, cujo conteudo ja esta no object store de `C:/dev/stolen-realm`. | `find . -maxdepth 4 -name .git` lista somente `./.git` e `./.worktrees/level-r2/.git` |

Ambos seguem intactos no disco e aparecem como untracked depois do commit. A decisao sobre eles (`.gitignore`
para `.worktrees/`, remocao do `nul`) e do ORG-R1/ORG-R2.

## 5. LIMITES respeitados

- Nada foi reorganizado, movido ou renomeado.
- Nada foi deletado (nem `nul`, nem `.worktrees/level-r2`, nem qualquer entregavel).
- Nenhum build foi executado (`dotnet`, `release-check.sh` e testes do repo NAO rodaram).
- Nenhum push: o checkpoint existe so no repositorio local, no branch `ci-validate-test`.
- As edicoes em andamento do dono foram preservadas exatamente como estavam no disco (o `git add` le o disco,
  nao altera nenhum arquivo-fonte).

## 6. Commit de checkpoint

Mensagem usada: `checkpoint: estado antes da organizacao do repositorio — 11/10/2026` (com corpo explicando a
excecao do `git add` amplo, os 801 arquivos, as 2 exclusoes e o HEAD de partida).
O hash do commit nao pode constar deste arquivo (ele proprio faz parte do commit); consulte
`git log -1 --format=%H` no branch `ci-validate-test` apos o checkpoint.

Para desfazer o checkpoint (sem perder nada do disco):
`git reset --soft d82894ebe95d97f26b7989a848372c691dcb8ef6` (volta ao estado de 565 linhas de status).
