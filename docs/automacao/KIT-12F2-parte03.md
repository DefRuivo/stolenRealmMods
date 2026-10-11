# KIT-12F2 — provas reais (parte 03)

Base de evidencias: `C:/dev/stolen-realm/scratch/kit/KIT-12F2-run675/`.
Todos os comandos por terminal, com stdout+stderr e exits preservados. Sem code_execution.

Diretorios:
- `rev674/` — copia da sandbox do revisor com o oraculo IMUTAVEL e o produto CORRIGIDO.
- `baseline-oracle/` — mesma copia, com o produto do baseline (sha `7785d8...`) restaurado do ZIP
  de evidencias do revisor — prova de continuidade do alvo.
- O ZIP do revisor (`KIT-12R-run674-evidencias.zip`) contem `integracao.py` == `7785d8...`, o que
  liga a sandbox de baseline a prova selada.

## 1. Orcamento independente do revisor (test_review_kit12.py, IMUTAVEL)

| Rodada | comando | resultado | exit | arquivo |
|---|---|---|---|---|
| Baseline | `python test_review_kit12.py` (baseline-oracle) | Ran 17: 11 OK / **6 FAIL**, ERROR0/skip0 | 1 | `oracle-baseline.txt` |
| Corrigido | `python test_review_kit12.py` (rev674) | Ran 17: **17 OK**, ERROR0/skip0 | 0 | `oracle-fix.txt` |

Os 6 FAIL do baseline: `test_missing_required_config_never_green`,
`test_report_dependency_missing_never_green`, `test_report_dependency_throw_never_green`,
`test_requested_probe_missing_not_silently_green`,
`test_malformed_observations_integer_closed`, `test_commands_sanitized_all_states`.

Nenhum arquivo do oraculo foi editado (sha inalterado `cf5966527ac0...`).

## 2. Suite do autor e isca (travas do produto)

| comando | resultado | exit | arquivo |
|---|---|---|---|
| `python tools/automacao/kit12/test_kit12_integracao.py` | Ran 30 OK | 0 | `suite.txt` |
| `python tools/automacao/kit12/test_kit12_integracao.py --isca` | 14/14 mutacoes discriminadas; controle restaurado exit0 | 0 | `isca.txt` |

## 3. CLI real (prove_ciclo.py)

| comando | resultado | exit | arquivo |
|---|---|---|---|
| `python tools/automacao/kit12/prove_ciclo.py --out .../cli2` | `PROVA\|PASSOU`; etapas 2->1->2->2->2->2->3 | 0 | `cli.txt`, `cli2/prova.json` |

Fluxo: 1-fixture=2 INCOMPLETO, 2-defeito=1 REPROVADO, 3-correcao=2, 3b-coleta-hash-de-outros-bytes=2,
3d-envelope-incoerente=2, 3c-coleta-hash-dos-arquivos-fonte=2, 4-verificar-apos-mudanca-de-config=3.
Avaliador REAL (sem mock) nesses passos.

## 4. Controles proprios do revisor reproduzidos (review_controls.py, copiado para `rev674/`)

11 mutacoes plantadas contra o oraculo, cada uma 3 fases (controle-antes / mutado / restaurado).
Identico ao baseline do revisor:

- 10 mutacoes discriminam `0->1->0` (`offline_control`, `chain_removed`,
  `collection_foreign_ignored`, `criterion_foreign_ignored`, `technical_to_owner`,
  `progress_disabled`, `random_report`, `invalidation_disabled`, `verify_disabled`,
  `empty_approves`).
- `fixture_rebaixamento` = `0->0->0`, **redundante** — a PRIMEIRA mutacao fixture continua
  documentada e NAO contada como discriminante (KIT-10 ja rebaixava fixture). Historico preservado.

Comparacao programatica `own-mutants.json` (baseline) x `rev674/own-mutants.json`: **11/11 iguais**
(mesma fase/exits/discriminacao). Nenhuma prova do revisor foi sobrescrita — a sandbox do revisor
foi restaurada ao baseline e os controles rodaram numa copia.

## 5. Sondas IRMAS (probes_kit12f2.py) — 38/38 OK

Cobrem o que o oraculo nao cobre, com controle positivo e negativo em cada fronteira:

- F1R: positivo config-presente aprova; ausente exit2 + lacuna nomeada + 0 OK; MULTIPLAS configs
  com uma ausente exit2 e 0 OK; `configs=[]` nao gera lacuna (opcional nao vira obrigatoria).
- F3R: `--probe-dll` inexistente exit2 + lacuna instrumento; declarado sem `--probe-dll` continua
  aprovando (limite declarado permitido); medido coerente positivo; medido divergente rebaixa.
- F4R: `observacoes` inteiro / nulo / objeto / string / lista-com-lixo / ausente -> todos exit2,
  `coleta.erro` preenchido, 0 OK, SEM excecao.
- F5R: saneamento nos QUATRO estados (OK/REPROVADO/NAO_EXERCITADO/INDETERMINADO) — residuo vazio e
  as 9 propostas preservadas em cada um; confirmado por `subprocess` instrumentado que NADA do
  conteudo proposto foi executado.

Resultado: `probes-resultado.json` (`total=38, falhas=0`), saida `probes.txt`.

## 6. Travas do repo (rodadas apos a correcao)

`check_segredos`, `check_padroes_segredo`, `check_dupes`, `audita_docs` -> exit0 cada
(`gate-*.txt`). Nenhum `git add/commit/push`.

## 7. O que NAO foi exercitado (nao maquiado)

Jogo/AUT-4 runtime novo, probe instalado, perfil/save do dono, UI/UX/pixels, build C#, preflight
de deploy, instalacao/publicacao, gates KIT-G1..G4 e aceite humano/DoD: **NAO_EXERCITADO**.
Os positivos APROVADO_OFFLINE usam avaliador OFFLINE injetado como controle da costura — NAO
provam runtime. Dividas F3/F4 historicas do pai (REPROVADO incoerente; `--verificar` sem `--config`
= falso INVALIDADO fail-closed) permanecem DIVIDA SEPARADA, nao tocadas aqui.
