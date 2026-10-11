# KIT-03F-Parte01: Correções C8 (runner) e C4 (isolamento)

## C8: run-isolation-tests.sh

### Problema
- `set -euo pipefail` + `((TOTAL++))` na linha 59 causa saída com status 1 quando TOTAL=0
- `skip()` do Teste 6 incrementa `PASSED` indevidamente
- Exit code não reflete skips/falhas

### Correções
1. Trocar `((TOTAL++))` por `TOTAL=$((TOTAL+1))` (e demais contadores similares)
2. `skip()` deve incrementar `SKIPPED` e retornar 0 sem afetar `PASSED`
3. `resumo_final()` deve verificar `SKIPPED > 0 || FAIL > 0` e sair com status != 0

### Arquivo: scratch/kit/run-isolation-tests.sh
