#!/usr/bin/env bash
# =============================================================================
# roda.sh — atalho do runner de testes (tools/testes/roda_testes.py).
#
# Existe por um motivo so: escolher o python certo (Windows/no repo costuma ser
# `python`; runner de CI costuma ser `python3`) sem obrigar ninguem a lembrar.
# Todo argumento passa direto para o runner.
#
#     bash tools/testes/roda.sh              # roda TUDO (puros + jogo)
#     bash tools/testes/roda.sh --puros      # so o que roda no CI
#     bash tools/testes/roda.sh --contra-prova
#
# Aceita PYTHON=<caminho> para forcar o interpretador.
#
# ARMADILHA (Windows): o `cd ... && pwd` do MSYS devolve `/c/dev/...`, e o
# python.exe NATIVO nao entende esse caminho (a conversao de path do MSYS esta
# desligada neste shell). Por isso o script entra na raiz do repo e chama o
# runner por caminho RELATIVO, em vez de montar um caminho absoluto em bash.
# =============================================================================
set -u

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAIZ="$(cd "$DIR/../.." && pwd)"

PY="${PYTHON:-}"
if [ -z "$PY" ]; then
  if command -v python  >/dev/null 2>&1; then PY=python
  elif command -v python3 >/dev/null 2>&1; then PY=python3
  else
    echo "roda.sh: nao achei 'python' nem 'python3' no PATH (exporte PYTHON=<caminho>)" >&2
    exit 2
  fi
fi

cd "$RAIZ" || { echo "roda.sh: nao consegui entrar em $RAIZ" >&2; exit 2; }
exec "$PY" "tools/testes/roda_testes.py" "$@"
