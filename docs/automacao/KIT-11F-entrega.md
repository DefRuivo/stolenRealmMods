# KIT-11F — correcao do executor (permissoes, frente unica, encerramento e rollback)

Cartao: `t_2a38d1d3` (KIT-11F), assignee `default`, run 656, workspace `C:/dev/stolen-realm`
(`workspace_kind=dir`). Origem: parecer independente **REPROVADO** KIT-11R (`t_79c1525f`, run 653),
com F1–F9 sobre o fonte `sha 65284edd…` entregue por `t_f2129aea` (run 649).
Escopo: ferramenta Python offline. **Nao** e DoD de mod; nenhum jogo, save, perfil, probe, deploy,
instalacao, publicacao, UI, runtime ou gate humano foi exercitado.

## ENTREGA (arquivos vivos)

| Arquivo | bytes | sha256 |
|---|---:|---|
| `tools/automacao/kit11/executor.py` | 38156 | `bf03f81b018157b4c73194df6ace95f00998fb77594047fd92eca0fe57fac3e9` |
| `tools/automacao/kit11/test_kit11_executor.py` | 42426 | `c2ac94f3107e52d8cb8c0a565c962c94803f0473eb61e92670ec5bff3b6e1d88` |

Os dois arquivos sao **UNTRACKED** (`git status` -> `?? tools/automacao/kit11/`): nenhum arquivo
versionado foi modificado, nenhum `git add/commit/push`. Dependencias compartilhadas NAO foram
tocadas — hashes identicos aos do revisor:
`runtime/coletor.py` = `159ff2aa4ffd1d57c26c1722340a3f23d33c73db75450d7ff7d02ab0dd4f7f3d`,
`runtime/controle_acesso.py` = `379d680f190c752efed29088d226f48d829b2dfbbd16d5360423f22fb9f9e457`,
`tools/testes/arcabouco.py` = `08b4dd51c1d2bd851cf0d5d2b2f038dbe3f1094ab4c625ed63a7a4dc97c20afb`.
Fonte antigo preservado byte a byte em `scratch/kit/KIT-11-executor-original.py`
(`sha 65284edd…`). Sem hotspot: nenhum arquivo compartilhado aparece na correcao.

## ACEITE — suite do revisor IMUTAVEL, fonte antigo x corrigido

Suite do revisor preservada sem uma linha alterada: `scratch/kit/KIT-11R-run653/test_kit11_review.py`
e copia em `scratch/kit/KIT-11F-run656/test_kit11_review.py`
— sha256 `cdd8b12a4cbb641b206cbd87ca534695a292109c4962f46e0cf06ee6e4a22143` (identico ao do parecer).

| Execucao | Comando | Resultado | exit | log |
|---|---|---|---:|---|
| Fonte ANTIGO | `python test_kit11_review.py` (sandbox-old) | `Ran 36 tests` / `FAILED (failures=24)` | **1** | `logs/review-old.log` |
| Fonte CORRIGIDO | `python test_kit11_review.py` (sandbox-new) | `Ran 36 tests` / `OK` (36/36) | **0** | `logs/review-new.log` |

Os **24 negativos** que reprovavam passam somente com guards reais — nao por enfraquecimento:
`mutacoes_reviewer.py` aplica **18 mutacoes** ao fonte corrigido, roda a suite IMUTAVEL contra cada
mutante e exige o reprovamento dos testes correspondentes, fechando **cobertura de 25/25**
`test_neg_*` (os 24 vermelhos no fonte antigo + `test_neg_missing_file_not_green`, que ja era o
controle verde). Baseline do corrigido: 0 reprovados. Log `logs/reviewer-mutations.log`,
resultado `reviewer-mutations.json`, driver `mutacoes_reviewer.py`
(`sha 38b2369d97861d3182712b67457982f1adad83bf111b32004fe2fb2278be8cb0`), exit **0**.

## Suite propria (ampliada) e isca que MUTA o fonte

`tools/automacao/kit11/test_kit11_executor.py`: 33 testes, `0 falha(s)`, exit **0**
(`logs/author-new.log`). Contra o **fonte antigo** a mesma suite reprova **22 de 33**, exit **1**
(`logs/author-old.log`) — a suite discrimina.

A isca deixou de ser `AssertionError` incondicional (achado F9): `--isca` aplica **18 mutacoes
seletivas por substituicao textual** no fonte do executor, roda a suite contra cada mutante e
exige que o teste-regressao correspondente REPROVE. Mutante que passa verde = carimbo para aquele
guard -> a isca reprova. Resultado: `18 mutacao(oes), 0 nao aplicada(s), 0 falha(s)`, exit **0**
(`logs/author-isca.log`).

Casos derivados acrescidos (alem dos 12 originais): setup/rollback com excecao injetada que liberam
a frente, encerramento por propriedade/autorizacao/liveness, cancelamento na ultima leitura,
preservacao de diretorio vazio e de `dir_backup` preexistentes, polling limitado ao deadline,
frente obrigatoria e **corrida concorrente real** (2 threads + barreira), CLI com exits 0/1/2 e
veredito lido do arquivo `--saida`. Nenhuma fixture se apresenta como jogo/runtime:
`runtime_exercitado=False` em todas as execucoes.

## CLI (processo real, exits distintos)

`cli_provas.py` roda o executor como subprocesso e le o veredito do ARQUIVO: 6/6, exit **0**
(`logs/cli-provas.log`, `cli-proofs.json`).

| Caso | Fonte antigo | Fonte corrigido |
|---|---|---|
| observacao negada (`observacao_autorizada=false`) | `OBSERVADO` / exit **0** (defeito F1) | `NAO_EXERCITADO` / exit **2** |
| observacao satisfeita | — | `OBSERVADO` / exit **0** |
| timeout por passo | — | `FALHOU` / exit **1** |
| sem `--estado` | — | exit **2** (fail-closed, nada executado) |
| plano ilegivel | — | exit **2** |

## PARECER POR ACHADO (F1–F9)

| # | Achado do KIT-11R | Correcao aplicada no fonte corrigido | Prova |
|---|---|---|---|
| F1 | obs negada ainda lia; override `'false'` virava `True`; `requer_acao` nao booleano aceito | `_booleano()` estrito em validacao E em override; sem obs nao ha leitura, retorna `NAO_EXERCITADO` (exit 2); NAO_EXERCITADO nao adquire frente nem faz backup; separados observar/agir/encerrar | `neg-obs-nao-autorizada-nao-le`, `neg-override-string-nao-vira-true`, `neg-requer-acao-nao-booleano`, CLI (a) |
| F2 | `bool('false')` gerava satisfeito; JSON malformado estourava | `_satisfeito_estrito()` booleano em `_consultar` **e** em `FonteDeArquivo`; JSON/estado invalido viram `ConfigInvalida` com diagnostico estruturado; leitura sem side-effect | `neg-satisfeito-string-nao-vira-verde`, `neg-fonte-arquivo-string-nao-vira-verde`, `neg-json-quebrado-estruturado` |
| F3 | timeout ausente/None/NaN/inf aceito; `sleep(5)` sob deadline 0.02 | `timeout_s` obrigatorio, finito e > 0; `intervalo_s` validado (finito >= 0); espera = `min(intervalo_s, restante)` | `neg-timeout-obrigatorio-finito`, `neg-poll-limitado-ao-deadline` |
| F4 | 2 acquires concorrentes no mesmo lock; frente opcional na API e ausente na CLI | aquisicao atomica `O_CREAT\|O_EXCL`; retomada de lock morto re-le e so remove o que leu como morto; frente **obrigatoria** (default `caminho_frente_padrao()`) e `--frente` na CLI | `neg-frente-obrigatoria`, `neg-frente-atomica-concorrente` |
| F5 | delta de PID encerrava PID externo; obs nao autorizada fechava; liveness `None` escalava `taskkill` | encerramento so de PIDs PROPRIOS (`pids_criados`), com autorizacao de ACAO; sem medicao/liveness `None` -> RECUSA sem comandos | `pos-encerra-so-o-proprio`, `neg-pid-externo-nunca-fechado`, `neg-encerramento-sem-autorizacao-de-acao`, `neg-liveness-desconhecida-nao-forca` |
| F6 | `finally` trocava CONCLUIDO/TIMEOUT/CANCELADO por ROLLBACK/ENCERRAMENTO | cleanup e FASES isoladas que nao tocam `res["estado"]`; erros vao para `res["cleanup_erros"]`; `_fecha` mapeia o estado terminal | `neg-cleanup-preserva-veredito` (OBSERVADO/FALHOU/CANCELADO) |
| F7 | diretorio vazio preexistente removido; `dir_backup` do chamador apagado inteiro | `snapshot_dirs` antes/depois vao para `planejar_rollback`/`executar_rollback`; backup em subdiretorio PROPRIO (`dir_backup_proprio`); `verificar_sem_residuo` registrado | `neg-rollback-preserva-preexistentes` |
| F8 | excecao de setup/rollback vazava lock; cancelamento na ultima leitura ignorado | setup DENTRO do `try`; cleanup em blocos `try` independentes; liberacao da frente sempre; cancelamento rechecado depois de cada leitura e na corrida | `neg-setup-excecao-libera-frente`, `neg-rollback-excecao-libera-frente`, `neg-cancelamento-na-ultima-leitura` |
| F9 | isca incondicional; suite do autor verde com 24 violacoes; `controle_acesso` citado e nao usado; doc afirmava `request_review` | isca = 18 mutacoes seletivas; suite ampliada para 33 testes cobrindo F1–F9; `controle_acesso.ACOES_ATIVAS` REUSADO como trava de acao ativa; adendo documental (sem apagar historico) em `KIT-11-entrega-final.md` | `--isca` exit 0; `neg-acao-ativa-proibida-controle-acesso`; adendo |
| C4/F5 | — | observacao nao concede encerramento **nem** com observacao autorizada | `neg-sem-medicao-recusa-encerramento` |

Veredito do implementer por achado: **F1–F9 corrigidos e provados offline**, com dois pontos de
LIMITE declarados abaixo.

## LIMITES HONESTOS (nao mascarados)

- **Navegacao real / clique fisico / janela / pixels / UIUX**: NAO_EXERCITADO. Continua qualificado
  em KIT-14 (apos KIT-G2). Nada aqui abre jogo, instala probe, carrega save ou publica.
- **Runtime em jogo**: NAO_EXERCITADO. A fonte nos testes e STUB ou arquivo JSON; nenhuma fixture
  foi promovida a jogo/runtime (`runtime_exercitado=False` em todas as execucoes).
- **Desempenho / leitura bloqueante real**: nao medido.
- **Contrato mudado (declarado, sem enfraquecer teste)**: (a) `timeout_s` passou de OPCIONAL para
  **OBRIGATORIO, finito e > 0**; (b) a frente passou de OPCIONAL para **OBRIGATORIA** (default
  `tempfile.gettempdir()/kit11-frente-unica.lock`, sobrescrevivel por `--frente`); (c) o
  encerramento passou a exigir **propriedade + autorizacao de acao + liveness mensuravel**; (d) o
  plano que so observa e tem `observacao_autorizada=false` agora termina em
  **`NAO_EXERCITADO`/exit 2**. Em cada caso a expectativa do revisor foi mapeada para o contrato
  explicito e provada por teste (nenhum negativo foi afrouxado — 25/25 seguem capturando mutante).
- **Suite runtime global** (que le o perfil do dono) NAO foi rodada: fora do escopo offline.
- **Travas do repo** (`check_segredos`, `check_padroes_segredo`, `check_dupes`, `audita_docs`)
  rodadas com exit 0 cada (`logs/*.log`), mas cobrem **versionados**; os arquivos desta correcao
  estao UNTRACKED e nao foram adicionados.
- **Gate humano / DoD / publicacao**: NAO_EXERCITADO. Esta correcao NAO e aceite de produto;
  KIT-12/13/14 continuam dependentes de reconferencia independente.

## PROXIMO PASSO NATIVO

Revisao independente **no proprio cartao** `t_2a38d1d3` via `kanban_request_review`
(implementer = esta instancia/run 656; reviewer = instancia separada). Nenhum cartao R duplicado foi
criado. Handoff nativo com resumo/metadata/hashes. Se a revisao pedir mudanca, `request_changes`
volta para o implementer neste mesmo cartao.

Provas: `scratch/kit/KIT-11F-run656/` e o pacote `scratch/kit/KIT-11F-run656-evidencias.zip`.
