#!/usr/bin/env bash
# roda_testes_kit08.sh - KIT-08: suite offline do visualizador + contra-prova
# (defeitos plantados TEM de reprovar o conjunto EXATO de testes). NAO abre o
# jogo, NAO acessa rede, NAO instala/deploy/publica.
#
#   bash tools/automacao/kit08/roda_testes_kit08.sh
#
# exit 0 = verde (suite OK + contra-prova verde); 1 = vermelho; 2 = erro de
# infraestrutura (layout/python). Nenhuma ausencia de etapa e declarada verde.
set -u

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAIZ="$(cd "$AQUI/../../.." && pwd)"
RAIZ="$(cd "$RAIZ" && { pwd -W 2>/dev/null || pwd; })"
MODULO="$RAIZ/tools/automacao/kit08/visualizador.py"
SUITE="$RAIZ/tools/automacao/kit08/teste_visualizador_kit08.py"
CONTRA_PROVA="$RAIZ/tools/automacao/kit08/contra_prova_kit08.py"
PY="${PYTHON:-python}"

if [ ! -f "$MODULO" ] || [ ! -f "$SUITE" ] || [ ! -f "$CONTRA_PROVA" ]; then
  echo "ERRO KIT-08: layout inesperado em $RAIZ (modulo/suite/contra-prova ausente)"
  exit 2
fi
if ! command -v "$PY" >/dev/null 2>&1; then
  echo "ERRO KIT-08: interpretador '$PY' nao encontrado (defina PYTHON=...)"
  exit 2
fi
cd "$RAIZ" || exit 2

echo "============================================================"
echo " KIT-08 - suite do visualizador (autor)"
echo "============================================================"
"$PY" "$SUITE"
rc_suite=$?

echo
echo "============================================================"
echo " KIT-08 - contra-prova (defeito plantado TEM de reprovar exato)"
echo "============================================================"
"$PY" "$CONTRA_PROVA"
rc_cp=$?

echo
if [ "$rc_suite" -eq 0 ] && [ "$rc_cp" -eq 0 ]; then
  echo "VEREDITO KIT-08: VERDE (exit 0)"
  exit 0
fi
echo "VEREDITO KIT-08: VERMELHO (suite=$rc_suite, contra-prova=$rc_cp)"
exit 1
