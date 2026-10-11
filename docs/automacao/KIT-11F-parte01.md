# KIT-11F — parte 01: inventario, leitura previa e execucao real

Cartao `t_2a38d1d3` (KIT-11F), run 656, perfil `default`. Workspace `C:/dev/stolen-realm`
(`workspace_kind=dir`). Data local inicial medida no cartao; escopo autorizado: OFFLINE.

## 1. Inventario ANTES de editar (leitura obrigatoria do parecer)

Lido integralmente antes de qualquer edicao:

| Fonte | sha256 | Papel |
|---|---|---|
| `docs/automacao/KIT-11R-revisao.md` | — | parecer REPROVADO, F1–F9 (entrada desta tarefa) |
| `tools/automacao/kit11/executor.py` (529 linhas) | `65284edd…` | fonte a corrigir |
| `tools/automacao/kit11/test_kit11_executor.py` (340 linhas) | `1d72ae07…` | suite do autor (12 testes) |
| `scratch/kit/KIT-11R-run653/test_kit11_review.py` (313 linhas) | `cdd8b12a…` | suite do revisor (36 testes; IMUTAVEL) |
| `scratch/kit/KIT-11R-run653/test_mutations.py` | `9ed78c5f…` | driver de mutacoes do revisor |
| `tools/automacao/runtime/coletor.py` | `159ff2aa…` | dependencia compartilhada (reuso, nao editar) |
| `tools/automacao/runtime/controle_acesso.py` | `379d680f…` | dependencia compartilhada (trava dura) |
| `docs/automacao/KIT-11-entrega-final.md` | — | relatorio do implementer (com as afirmacoes F9) |
| `git status --short`, `git log` | — | estado do repo (36 modificados, 246 untracked, branch `ci-validate-test`) |

Alteracoes manuais do dono no repo: **preservadas**; nenhum arquivo versionado foi tocado nesta
tarefa (`tools/automacao/kit11/` inteiro esta UNTRACKED). Nenhum `git add -A`/`commit`/`push`.

## 2. Leitura do contrato que os testes exigem (antes de escrever codigo)

A suite do revisor e a fonte de aceite. Cada negativo aponta um guard concreto:

- `timeout_s` tem de ser OBRIGATORIO e finito (neg: missing/None/NaN/inf) — o fonte antigo aceitava
  ausencia e nao finitos.
- Frente: `test_neg_lock_required` exige que `executar()` SEM `frente` ainda registre frente; e
  `test_neg_lock_atomic` sincroniza 2 threads em `os.path.exists` e exige **1** sucesso.
- `test_neg_preexisting_backup_preserved` roda com `dir_backup` PRÉ-existente e **sem**
  `area_trabalho`: o fonte antigo apagava o diretorio do chamador.
- `test_neg_setup_exception_releases_lock` / `test_neg_cleanup_exception_releases_lock` chamam
  `executar` direto e exigem o lock removido mesmo com `OSError` injetado.
- `run_ex` transforma QUALQUER excecao nao tratada em falha de teste -> toda falha tem de virar
  resultado ESTRUTURADO.

Consequencias de projeto: (a) validacao estrita com `_booleano`/`_timeout_finito`; (b) frente
obrigatoria com lock atomico `O_CREAT|O_EXCL`; (c) cleanup em fases isoladas; (d) 25 negativos
cobertos por mutacao (nao apenas "passando").

## 3. Confronto das suites: o conflito de contrato (declarado, nao escondido)

A suite do AUTOR (12 testes) afirmava o comportamento DEFEITUOSO em dois pontos e por isso precisou
ser ATUALIZADA — nao para "passar", mas para o contrato novo e explicito:

1. `passo()` criava passos com `timeout_s=None` -> o contrato novo exige timeout finito obrigatorio.
2. `t_encerra_so_instancia_criada` exigia fechar o **delta** de PIDs (`{100,200}` -> `[200]`), que e
   exatamente o achado **F5**. Reescrito como `pos-encerra-so-o-proprio` (PIDs PROPRIOS), mantendo o
   controle do PID externo em `neg-pid-externo-nunca-fechado`.

Nenhum negativo do revisor foi alterado ou afrouxado: a suite do revisor e byte-identica
(`sha cdd8b12a…` reconferido antes e depois de cada execucao).

## 4. Execucao real (comandos, hashes, exits)

Sandbox desta rodada: `scratch/kit/KIT-11F-run656/` com `sandbox-old/` (fonte `65284edd…` + runtime
copiado) e `sandbox-new/` (fonte `bf03f81b…` + runtime copiado), ambas **sem** `.git`, remotos,
credenciais ou perfil do dono.

| # | Comando | Resultado | exit | log |
|---|---|---|---:|---|
| 1 | `python test_kit11_review.py` em `sandbox-old/` | 36 testes, **24 FAIL**, 12 OK | **1** | `logs/review-old.log` |
| 2 | `python test_kit11_review.py` em `sandbox-new/` | 36 testes, **0 FAIL** | **0** | `logs/review-new.log` |
| 3 | `python tools/automacao/kit11/test_kit11_executor.py` | 33 testes, 0 falha | **0** | `logs/author-new.log` |
| 4 | `python .../test_kit11_executor.py` no fonte antigo (sandbox-old) | 33 testes, **22 falhas** | **1** | `logs/author-old.log` |
| 5 | `python .../test_kit11_executor.py --isca` | 18 mutacoes, 0 nao aplicada, 0 falha | **0** | `logs/author-isca.log` |
| 6 | `python scratch/kit/KIT-11F-run656/mutacoes_reviewer.py` | 18 mutacoes, cobertura 25/25 negativos, baseline 0 | **0** | `logs/reviewer-mutations.log` |
| 7 | `python scratch/kit/KIT-11F-run656/cli_provas.py` | 6 casos, 0 falha | **0** | `logs/cli-provas.log` |
| 8 | `python tools/check_segredos.py` | OK | **0** | `logs/check_segredos.log` |
| 9 | `python tools/check_padroes_segredo.py` | OK | **0** | `logs/check_padroes_segredo.log` |
| 10 | `python tools/check_dupes.py` | OK | **0** | `logs/check_dupes.log` |
| 11 | `python tools/audita_docs.py` | OK | **0** | `logs/audita_docs.log` |

Exits 0/1/**2** sao distintos e conferidos no CLI (`logs/cli-provas.log`): `NAO_EXERCITADO` sai 2,
`FALHOU_FECHADO`/`FALHOU` saem 1, `PASSOU`/`OBSERVADO` saem 0.

## 5. Ordem real de trabalho (com um tropeco registrado)

1. Comparacao do fonte vivo com a copia do revisor: hashes IDENTICOS -> a suite IMUTAVEL de fato
   roda contra o fonte que o revisor julgou.
2. Reescrita do executor (per-achado) + reescrita da suite do autor (contrato novo + F1–F9 + isca).
3. **Tropeco**: `test_neg_preexisting_backup_preserved` reprovou na primeira rodada do corrigido —
   o `rmtree(dir_backup)` ainda rodava quando NAO havia backup a criar (diretorio do chamador sem
   `area_trabalho`). Corrigido com a flag `dir_backup_proprio` (so remove o que a execucao criou).
   So depois disso a suite do revisor ficou 36/36.
4. **Tropeco**: uma mutacao da isca (coercao de `observacao_autorizada`) nao era capturada porque a
   ancora apontava para a linha errada (`obs` em vez de `ativa`). A isca acusou o furo: mutante
   verde -> `--isca` exit 1. Ancora corrigida para a linha realmente decisiva.
5. CLI: a primeira versao do driver copiava o executor para um diretorio temporario e o modulo
   perdia `runtime/controle_acesso.py` da sua resolucao relativa (`FALHOU_FECHADO` em tudo).
   Corrigido rodando o executor NO LUGAR (layout preservado). O erro apareceu no veredito, nao numa
   mensagem de sucesso — exatamente o que o aceite pede.

## 6. Estados e vereditos publicos (novos/alterados)

Adicionados: estado `NAO_EXERCITADO` e veredito `NAO_EXERCITADO` (exit 2). `ROLLBACK`/`ENCERRAMENTO`
deixam de ser estados: viraram NOMES DE FASE de cleanup (nao substituem o resultado terminal).
`res["cleanup_erros"]` registra falha de cada fase sem esconder nem mascarar a causa.

## 7. O que NAO foi feito

Nao foram tocados: `coletor.py`, `controle_acesso.py`, `arcabouco.py` (hashes conferidos iguais),
mods/produto, `Assembly-CSharp`, Bard/gameplay, jogo/save/perfil, politica/modelo/cron/prioridade,
KIT-12/13/14 (consumidores). Sem build, sem preflight, sem deploy, sem publicacao. Sem gate humano.
