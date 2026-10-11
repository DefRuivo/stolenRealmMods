#!/usr/bin/env bash
# ORG-R3: shim legado; a implementacao mantida fica em tools/.
# Encaminha todos os argumentos e preserva o codigo de saida, sem ciclo duplicado.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" || exit 2
exec bash "$SCRIPT_DIR/../tools/test-cycle.sh" "$@"
