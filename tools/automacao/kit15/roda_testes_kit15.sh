#!/usr/bin/env bash
# roda_testes_kit15.sh - KIT-15: suite offline + contra-prova do pacote instalavel.
# NAO abre o jogo, NAO instala no perfil do dono, NAO publica, NAO usa rede.
#
#   bash tools/automacao/kit15/roda_testes_kit15.sh      (repositorio do autor)
#   bash tools/roda_testes_kit15.sh                      (pacote distribuido)
#
# KIT-15F/F8: a suite/contra-prova sao localizadas ao lado DESTE script, nao por um caminho
# fixo de repositorio (`tools/automacao/kit15`). Assim o mesmo script funciona no layout do
# autor e no layout DISTRIBUIDO (tools/ + components/ + docs/).
#
# exit 0 = verde (suite OK + contra-prova com todos os defeitos recusados);
# 1 = vermelho; 2 = erro de infraestrutura (layout/interpretador). Nenhuma ausencia e verde.
set -u

AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AQUI="$(cd "$AQUI" && { pwd -W 2>/dev/null || pwd; })"
RAIZ="$(cd "$AQUI/.." && { pwd -W 2>/dev/null || pwd; })"
SUITE="$AQUI/teste_kit15.py"
CONTRA="$AQUI/contra_prova_kit15.py"
PY="${PYTHON:-python}"

if [ ! -f "$SUITE" ] || [ ! -f "$CONTRA" ]; then
  echo "ERRO KIT-15: layout inesperado em $AQUI (suite/contra-prova ausente)"
  exit 2
fi
if ! command -v "$PY" >/dev/null 2>&1; then
  echo "ERRO KIT-15: interpretador '$PY' nao encontrado (defina PYTHON=...)"
  exit 2
fi
cd "$RAIZ" || exit 2

echo "============================================================"
echo " KIT-15 - suite do pacote (autor)"
echo "============================================================"
"$PY" "$SUITE"
rc_suite=$?

echo
echo "============================================================"
echo " KIT-15 - contra-prova (defeitos plantados TEM de reprovar)"
echo "============================================================"
"$PY" "$CONTRA"
rc_contra=$?

echo
echo "============================================================"
if [ "$rc_suite" -eq 0 ] && [ "$rc_contra" -eq 0 ]; then
  echo " KIT-15 RESULTADO|VERDE|suite=$rc_suite contra-prova=$rc_contra"
  exit 0
fi
if [ "$rc_suite" -eq 2 ] || [ "$rc_contra" -eq 2 ]; then
  echo " KIT-15 RESULTADO|ERRO-INFRA|suite=$rc_suite contra-prova=$rc_contra"
  exit 2
fi
echo " KIT-15 RESULTADO|VERMELHO|suite=$rc_suite contra-prova=$rc_contra"
exit 1
