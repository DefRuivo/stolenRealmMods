#!/usr/bin/env bash
# roda_testes_kit07.sh - KIT-07: suite offline do exportador + testes adicionais
# do KIT-07F + contra-prova (defeitos plantados). NAO abre o jogo e NAO faz upload.
#
#   bash tools/automacao/kit07/roda_testes_kit07.sh
#
# exit 0 = verde (suite OK + testes adicionais OK + contra-prova por defeito e por
# teste verdes); 1 = vermelho; 2 = erro de infraestrutura (layout/python). Nenhuma
# ausencia de etapa e declarada verde.
set -u

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# raiz pelo PROPRIO LAYOUT (tools/automacao/kit07 -> raiz), sem `git rev-parse`.
RAIZ="$(cd "$AQUI/../../.." && pwd)"
RAIZ="$(cd "$RAIZ" && { pwd -W 2>/dev/null || pwd; })"
MODULO="$RAIZ/tools/automacao/kit07/exportador.py"
SUITE="$RAIZ/tools/automacao/kit07/teste_exportador_kit07.py"
SUITE_F="$RAIZ/tools/automacao/kit07/teste_exportador_kit07f.py"
CONTRA_PROVA="$RAIZ/tools/automacao/kit07/contra_prova_kit07.py"
PY="${PYTHON:-python}"

if [ ! -f "$MODULO" ] || [ ! -f "$SUITE" ] || [ ! -f "$SUITE_F" ] || [ ! -f "$CONTRA_PROVA" ]; then
  echo "ERRO KIT-07: layout inesperado em $RAIZ (modulo/suite/suite-F/contra-prova ausente)"
  exit 2
fi
if ! command -v "$PY" >/dev/null 2>&1; then
  echo "ERRO KIT-07: interpretador '$PY' nao encontrado (defina PYTHON=...)"
  exit 2
fi
cd "$RAIZ" || exit 2

echo "============================================================"
echo " KIT-07 - suite do exportador (autor)"
echo "============================================================"
"$PY" "$SUITE"
rc_suite=$?

echo
echo "============================================================"
echo " KIT-07F - testes adicionais (nomes/PNG, colisao, canonicos,"
echo "          limites em bytes de saida, I/O da CLI, log selecionado)"
echo "============================================================"
"$PY" "$SUITE_F"
rc_suite_f=$?

echo
echo "============================================================"
echo " KIT-07 - contra-prova por defeito (defeito plantado TEM de reprovar)"
echo "============================================================"
"$PY" "$CONTRA_PROVA"
rc_cp_regras=$?

echo
echo "============================================================"
echo " KIT-07 - contra-prova por teste (cada alvo sozinho TEM de reprovar)"
echo "============================================================"
"$PY" "$CONTRA_PROVA" --individual
rc_cp_testes=$?

echo
if [ "$rc_suite" -eq 0 ] && [ "$rc_suite_f" -eq 0 ] && [ "$rc_cp_regras" -eq 0 ] && [ "$rc_cp_testes" -eq 0 ]; then
  echo "VEREDITO KIT-07: VERDE (exit 0)"
  exit 0
fi
echo "VEREDITO KIT-07: VERMELHO (suite=$rc_suite, suite-F=$rc_suite_f, contra-prova-defeitos=$rc_cp_regras, contra-prova-testes=$rc_cp_testes)"
exit 1
