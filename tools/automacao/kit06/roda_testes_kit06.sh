#!/usr/bin/env bash
# roda_testes_kit06.sh - KIT-06: roda a suite offline do plano de controle, a
# contra-prova por regra (defeito plantado TEM de reprovar) e o autoteste do
# discriminador. NAO abre o jogo, NAO instala probe, NAO toca no perfil do dono.
#
#   bash tools/automacao/kit06/roda_testes_kit06.sh
#
# exit 0 = verde; 1 = vermelho; 2 = erro de infraestrutura (layout/python).
# Nenhuma ausencia de etapa e declarada verde.
set -u

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Raiz pelo PROPRIO LAYOUT (tools/automacao/kit06 -> raiz), sem `git rev-parse`.
RAIZ="$(cd "$AQUI/../../.." && pwd)"
# Caminho NATIVO (Windows) para o python nativo: o MSYS nao converte argumentos.
RAIZ="$(cd "$RAIZ" && { pwd -W 2>/dev/null || pwd; })"
MODULO="$RAIZ/tools/automacao/runtime/controle_acesso.py"
SUITE="$RAIZ/tools/automacao/kit06/teste_controle_acesso.py"
CONTRA_PROVA="$RAIZ/tools/automacao/kit06/contra_prova_kit06.py"
PY="${PYTHON:-python}"

if [ ! -f "$MODULO" ] || [ ! -f "$SUITE" ] || [ ! -f "$CONTRA_PROVA" ]; then
  echo "ERRO KIT-06: layout inesperado em $RAIZ (fonte/suite/contra-prova ausente)"
  exit 2
fi
if ! command -v "$PY" >/dev/null 2>&1; then
  echo "ERRO KIT-06: interpretador '$PY' nao encontrado (defina PYTHON=...)"
  exit 2
fi
cd "$RAIZ" || exit 2

echo "============================================================"
echo " KIT-06 - suite do plano de controle (autor)"
echo "============================================================"
"$PY" "$SUITE"
rc_suite=$?

echo
echo "============================================================"
echo " KIT-06 - contra-prova por regra (defeito plantado TEM de reprovar)"
echo "============================================================"
"$PY" "$CONTRA_PROVA"
rc_cp=$?

echo
echo "============================================================"
echo " KIT-06 - autoteste do discriminador estrito"
echo "============================================================"
"$PY" "$CONTRA_PROVA" --autoteste
rc_auto=$?

echo
if [ "$rc_suite" -eq 0 ] && [ "$rc_cp" -eq 0 ] && [ "$rc_auto" -eq 0 ]; then
  echo "VEREDITO KIT-06: VERDE (exit 0)"
  exit 0
fi
echo "VEREDITO KIT-06: VERMELHO (suite=$rc_suite, contra-prova=$rc_cp, autoteste=$rc_auto)"
exit 1
