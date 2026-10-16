# KIT-03F - Parte 03: correções aplicadas e provas de execução

Data: 2026-10-09 (rodada offline, sandbox; nada instalado, jogo fechado, perfil intocado)

## Correções (por achado da revisão KIT-03R)

| Achado | Arquivo | Correção | Prova |
|--------|---------|----------|-------|
| C8 (GRAVE) | `run-isolation-tests.sh` | contadores por atribuição; `skip` = SKIP (não PASS); exit fiel | 6/6 testes, exit 0 |
| C4 (GRAVE) | `isolacao.sh` | `prove-isolation` com containment real e exit != 0 na falha | positivo exit 0 / plantado exit 1 |
| C5 (GRAVE) | `front-unica.sh` | lock 1 linha + sentinela vivo; 2º acquire recusado; `--force` funciona | 2º acquire exit 1 |
| C3 | `snapshot.sh` | rollback por diff + hashes conferidos + falha se não exato | criado fora da lista removido |
| C2/C6 | `detect-env.sh` | caminhos via `$(dirname $0)`/`KITS_DIR`; JSON em `$KITS_DIR`; Player.log LocalLow; cadeia CIC corrigida | roda de qualquer cwd |
| C6 | `isolacao.sh` | removido `<PERFIL-DO-DONO>/...` | grep vazio |
| C1 | `KIT-03-entrega.md` | hashes reais, caminhos que existem, histórico preservado | seção "Correção KIT-03F" |
| C9/C10 | `run-isolation-tests.sh`, novo `build-preflight.sh` | Teste 6 aponta para `tools/automacao/...` e REUSA o harness; pre-flight de build isolado | harness VERDE (15 testes) |

Novos scripts: `scratch/kit/controle-negativo-kit.sh` (4 defeitos plantados) e
`scratch/kit/build-preflight.sh` (build em cópia isolada com `-p:DeployToBepInEx=false`).

Detalhe da verificação final em `scratch/kit/negativo/FINAL-verificacao.txt`.

> **Nota REPO-PRIV-1 (identidade):** neste documento, `%USERPROFILE%` (Windows) e `$HOME` (bash) — e, onde o texto fala do caminho fixo em si, `<PERFIL-DO-DONO>` — substituem o caminho do perfil do dono que antes aparecia literalmente. Os dois primeiros sao variaveis de ambiente reais: expanda-as no seu shell. Nenhum deles e caminho literal.
