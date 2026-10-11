#!/usr/bin/env bash
# roda_testes_kit05.sh - KIT-05: roda a suite offline do pipeline de observacao
# passiva e o controle negativo (defeito plantado). NAO abre o jogo.
#
#   bash tools/automacao/kit05/roda_testes_kit05.sh
#
# exit 0 = verde (suite OK + contra-prova por regra e por teste verdes);
# 1 = vermelho; 2 = erro de infraestrutura (layout/python). Nenhuma ausencia
# de etapa e declarada verde.
set -u

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# F7: raiz pelo PROPRIO LAYOUT (tools/automacao/kit05 -> raiz), sem `git rev-parse`
# e sem ascender ao repo do dono. Podem ser usados paths ABSOLUTOS (o python
# nativo nao recebe conversao de path do MSYS).
RAIZ="$(cd "$AQUI/../../.." && pwd)"
# Caminho NATIVO (Windows) para o python nativo: o MSYS nao converte argumentos.
RAIZ="$(cd "$RAIZ" && { pwd -W 2>/dev/null || pwd; })"
MODULO="$RAIZ/tools/automacao/runtime/observacao_passiva.py"
SUITE="$RAIZ/tools/automacao/kit05/teste_observacao_passiva.py"
CONTRA_PROVA="$RAIZ/tools/automacao/kit05/contra_prova_kit05.py"
PY="${PYTHON:-python}"

if [ ! -f "$MODULO" ] || [ ! -f "$SUITE" ] || [ ! -f "$CONTRA_PROVA" ]; then
  echo "ERRO KIT-05F: layout inesperado em $RAIZ (fonte/suite/contra-prova ausente)"
  exit 2
fi
if ! command -v "$PY" >/dev/null 2>&1; then
  echo "ERRO KIT-05F: interpretador '$PY' nao encontrado (defina PYTHON=...)"
  exit 2
fi
cd "$RAIZ" || exit 2

echo "============================================================"
echo " KIT-05F - suite de observacao passiva (autor)"
echo "============================================================"
"$PY" "$SUITE"
rc_suite=$?

echo
echo "============================================================"
echo " KIT-05F - contra-prova por regra (defeito plantado TEM de reprovar)"
echo "============================================================"
"$PY" "$CONTRA_PROVA"
rc_cp_regras=$?

echo
echo "============================================================"
echo " KIT-05F - contra-prova por teste (cada teste sozinho TEM de reprovar)"
echo "============================================================"
"$PY" "$CONTRA_PROVA" --individual
rc_cp_testes=$?

echo
if [ "$rc_suite" -eq 0 ] && [ "$rc_cp_regras" -eq 0 ] && [ "$rc_cp_testes" -eq 0 ]; then
  echo "VEREDITO KIT-05F: VERDE (exit 0)"
  exit 0
fi
echo "VEREDITO KIT-05F: VERMELHO (suite=$rc_suite, contra-prova-regras=$rc_cp_regras, contra-prova-testes=$rc_cp_testes)"
exit 1
