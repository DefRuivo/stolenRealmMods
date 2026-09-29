#!/usr/bin/env bash
# Ciclo automatizado de teste: abre o jogo modded, espera o plugin carregar,
# lê o LogOutput.log e fecha o jogo — sem intervenção manual.
#
# Uso:   bash test-cycle.sh [SEG_APOS_PLUGIN] [PADRAO_GREP]
# Ex.:   bash test-cycle.sh 20 "QoL fonte|Roguelike QoL"
set -u

STEAM="/c/Program Files (x86)/Steam/steam.exe"
APPID=1330000
PRELOADER="%USERPROFILE%\AppData\Roaming\r2modmanPlus-local\StolenRealm\profiles\Default\BepInEx\core\BepInEx.Preloader.dll"
LOG="/c/Users/<user>/AppData/Roaming/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/LogOutput.log"
WAIT_AFTER="${1:-20}"
PATTERN="${2:-QoL fonte|Roguelike QoL}"

echo "[1/5] encerrando instância anterior (se houver)..."
if taskkill /F /IM "Stolen Realm.exe" >/dev/null 2>&1; then
  echo "  instância anterior encerrada"
else
  echo "  nenhuma instância rodando"
fi

echo "[2/5] limpando log antigo"
rm -f "$LOG"

echo "[3/5] lançando via Steam -applaunch $APPID"
"$STEAM" -applaunch "$APPID" "--doorstop-enabled" "true" "--doorstop-target-assembly" "$PRELOADER" >/dev/null 2>&1 &

echo "[4/5] aguardando o plugin carregar (até 90s)..."
LOADED=0
for i in $(seq 1 90); do
  if [ -f "$LOG" ] && grep -aq "Roguelike QoL carregado" "$LOG"; then
    echo "  plugin carregado após ~${i}s"
    LOADED=1
    break
  fi
  sleep 1
done
if [ "$LOADED" -ne 1 ]; then
  echo "  ATENÇÃO: plugin não carregou em 90s. Últimas linhas do log:"
  tail -20 "$LOG" 2>/dev/null || echo "  (log ainda não existe)"
fi

echo "  aguardando +${WAIT_AFTER}s para o font sweep rodar..."
sleep "$WAIT_AFTER"

echo "[5/6] capturando screenshot da tela..."
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:/dev/stolen-realm/scratch/shot.ps1" -Path "C:/dev/stolen-realm/scratch/shot.png" 2>&1 | tail -1

echo "[6/6] linhas relevantes do log:"
grep -aE "$PATTERN" "$LOG" 2>/dev/null | sort | uniq -c | sort -rn | head -40 || echo "  (nenhuma linha casou)"

echo "--- encerrando o jogo ---"
if taskkill /F /IM "Stolen Realm.exe" >/dev/null 2>&1; then
  echo "  jogo encerrado."
else
  echo "  jogo já não estava rodando."
fi
