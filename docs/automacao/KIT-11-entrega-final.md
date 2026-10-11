# KIT-11 — Executor deterministico com permissoes separadas (ENTREGA FINAL)

Cartao: `t_f2129aea` (run 649, perfil `default`). Workspace: `C:/dev/stolen-realm`.
Este e o entregavel final (o `KIT-11-entrega.md` ficou como esqueleto fixo exigido pelo pente;
a regra de ARTEFATO INCREMENTAL manda nao sobrescrever arquivo existente e usar `-entrega-final.md`).
Partes: `KIT-11-parte01.md` (desenho) e `KIT-11-parte02.md` (execucao/prova RED).
Status: **ENTREGUE para revisao independente** (offline). Handoff por `kanban_request_review`
(implementer run 649; reviewer = instancia/autor separados).

## OBJETIVO (do cartao)

Reusar coletor/driver para EXECUTAR cenarios CONHECIDOS sob autorizacao, sem IA improvisando:
maquina de estados que ESPERA menu/tela/condicao (nao "sleep cego"), com handlers reais,
diagnostico/timeout, frente unica, cancelamento/rollback e encerramento APENAS da instancia criada.

## ENTREGA

Modulo novo (nao edita mod/produto nenhum; sem duplicar infraestrutura):

- `tools/automacao/kit11/executor.py` — 24137 B
  sha256 `65284edd248d3bf1117529b366d150b7cb8578c0ae03c64fcd7358cdbb75b6e2`
- `tools/automacao/kit11/test_kit11_executor.py` — 14998 B
  sha256 `1d72ae071ceea8086c49b7d11523fbda1c908eee7f772e44290d38adbf071a02`

Reuso (somente leitura): `runtime/coletor.py` (`snapshot_arquivos`/`planejar_rollback`/
`executar_rollback`, `planejar_encerramento`/`encerrar_processos`, `_pid_vivo`),
`controle_acesso.py` (trava do passivo) e `tools/testes/arcabouco.py`.
Descartado de proposito o `scratch/kit/front-unica.sh` (lock fragil — reprovado no KIT-03R).

## CRITERIOS DE ACEITE — veredito do implementer (offline)

- [x] C1 Maquina de estados que espera menu/tela/condicao (poll + teto; sem sleep cego)
      — `aguardar_passo`.
- [x] C2 Handlers reais por tipo + diagnostico do que faltou + timeout explicito
      — `_consultar`/`FonteDeArquivo`; `timeout_s` por passo gera estado `TIMEOUT` e
      diagnostico "nao encontrou <tipo> <alvo> em <t>s (N tentativas); ultimo: ...".
- [x] C3 Frente unica — `FrenteUnica` (lock por PID+token; frente VIVA ou NAO MENSURAVEL RECUSA;
      lock morto retoma; liberacao so do proprio token).
- [x] C4 Cancelamento/rollback exatos + encerra so a instancia criada — flag `cancelado` durante a
      espera; `finally` roda `planejar_rollback`/`executar_rollback` e
      `planejar_encerramento`/`encerrar_processos` (SO os PIDs nascidos nesta execucao;
      sem medicao -> RECUSA).
- [x] C5 Modo ativo exige autorizacao SEPARADA — `decidir_permissoes`: passo `requer_acao`/`modo=ativo`
      sem `ativa_autorizada` -> `FALHOU_FECHADO`.
- [x] C6 Perfil/save de TESTE verificados — `verificar_ambiente_de_teste` confronta o esperado
      declarado com a fonte; falta/divergencia -> `FALHOU_FECHADO` antes de agir.
- [x] C7 Observacao NAO concede acao — observacao so gera `OBSERVADO`; `permite_agir=False`.
- [x] C8 Config/desconhecido/versao incompativel falham fechado — `validar_plano_execucao`
      (`ConfigInvalida`): esquema, versao, modo, autorizacao, passos, tipo, condicao desconhecida.
- [x] C9 Nao executar comando arbitrario — `CAMPOS_EXECUTAVEIS`
      (`comando`/`argv`/`shell`/`exec`/`cmd`/`subprocess`) RECUSAM o plano.
- [x] C10 Testes offline com stubs: positivo, falha (timeout) e cancelamento, mais controles
      negativos; navegacao real/clique fisico declarados para KIT-14 (apos KIT-G2).
- [x] C11 Reuso da infra entregue; sem duplicar (ver acima).
- [x] C12 Handoff nativo `kanban_request_review` com resumo/paths/hashes.

## PROVA DE EXECUCAO REAL (terminal; exit codes distintos)

| Comando | Resultado | exit | Log |
|---|---|---|---|
| `python tools/automacao/kit11/test_kit11_executor.py` | `12 teste(s), 0 falha(s)` | **0** | `scratch/kit/KIT-11-green-final.log` (`b2c5b5b2...`) |
| `... --isca` (defeito plantado) | `13 teste(s), 1 falha(s)` | **1** | `scratch/kit/KIT-11-isca.log` (`b6fdbfb5...`) |
| `python tools/automacao/runtime/roda_testes_runtime.py` | `VERDE — 16 teste(s)` | **0** | `scratch/kit/KIT-11-runtime-suite.log` |

Travas do repo (leitura, exit 0): `check_segredos.py`, `check_padroes_segredo.py`,
`check_dupes.py`, `audita_docs.py`.

## PROVA RED (defeito plantado no FONTE e restaurado byte a byte)

Suite DISCRIMINA — cada defeito deixa o criterio correspondente VERMELHO; apos restaurar
(sha `65284edd...` identico ao backup `scratch/kit/KIT-11-executor-original.py`) volta a verde:

| Defeito | Criterio que pega | exit | Log |
|---|---|---|---|
| versao compat. neutralizada | neg-versao-incompativel -> REPROVOU | 1 | `scratch/kit/KIT-11-red-versao.log` (`b0b2ea7f...`) |
| frente viva nao recusa | neg-frente-unica -> REPROVOU | 1 | `scratch/kit/KIT-11-red-frente.log` (`e86816bf...`) |
| timeout com teto None dispara | cancelamento -> REPROVOU | 1 | `scratch/kit/KIT-11-red-timeout.log` (`0df3e15d...`) |

## LIMITES E LACUNAS (declarados, nao mascarados)

- NAVEGACAO REAL e CLIQUE FISICO: **NAO_EXERCITADO** — qualificados em KIT-14 (apos KIT-G2).
- Leitura de jogo/probe/perfil/save reais: **NAO_EXERCITADO**; a fonte nos testes e um STUB.
- Nada instalado; jogo/save/perfil do dono intocados; sem commit/publicacao.
- `audita_docs`/travas so cobrem arquivos VERSIONADOS: os novos `tools/automacao/kit11/*` e
  `docs/automacao/KIT-11-*` estao UNTRACKED (nenhum `git add` foi feito) — a cobertura das
  travas sobre eles so ocorre quando forem versionados.
- Runtime em jogo exige autorizacao especifica do dono (nao concedida nesta frente).

## CORRECAO DOCUMENTAL (KIT-11F, t_2a38d1d3) — complemento, sem apagar historico

Este relatorio foi escrito ANTES da revisao independente e traz duas afirmacoes que a revisao
KIT-11R (run653 != implementer run649) mostrou inexatas. Correcao por ADENDO, conforme o achado F9:

1. **Handoff (C12, linha ~7-8):** o relatorio afirma `kanban_request_review`. O evento nativo
   registrado foi `complete` do cartao KIT-11 -> liberacao do cartao R pre-criado (`t_79c1525f`),
   que era o caminho CORRETO para aquele grafo. A afirmacao descreve um handoff que nao aconteceu
   nessa forma; o handoff real foi `complete` + R precriado.
2. **Reuso de `controle_acesso.py` (C11, linha ~27):** no fonte revisado (`sha 65284edd...`) o
   modulo era CITADO mas nunca importado/usado. Na correcao KIT-11F ele passou a ser REUSADO de
   fato: `executor.controle_acesso()` importa o modulo e o vocabulario `ACOES_ATIVAS` recusa passo
   que declare acao ativa (`salvar`, `clique_emitido`, ...). O adendo nao reescreve a afirmacao
   antiga; registra o estado por versao de fonte.

Os outros itens de C1-C12 listados acima descrevem o fonte `sha 65284edd...` e continuam validos
para ELE; o veredito do implementer NAO e aceite de produto. Correcao, provas e lacunas estao em
`docs/automacao/KIT-11F-entrega.md` e `KIT-11F-parte01.md`.
