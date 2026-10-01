#!/usr/bin/env bash
# ============================================================================
# Gera o pacote .zip com os mods para enviar a amigos.
#
# O amigo NÃO precisa programar nada: ele só copia as pastas para
# BepInEx\plugins\ (as instruções vão dentro do zip, em LEIA-ME.txt).
#
# Uso:
#   bash tools/pack-for-friends.sh                  # pacote padrão (amigos)
#   bash tools/pack-for-friends.sh BetterTooltips      # só um mod
#   bash tools/pack-for-friends.sh BetterTooltips BetterFont BetterStats
#
# Saída: dist/StolenRealm-Mods-<AAAA-MM-DD>.zip
# ============================================================================
set -euo pipefail
cd "$(dirname "$0")/.."

# Mods que fazem sentido para amigos. O RoguelikeDebugger fica de fora de
# propósito (é ferramenta de desenvolvimento: enche o log com milhares de
# linhas).
if [ "$#" -gt 0 ]; then
  MODS=("$@")
else
  MODS=(BetterTooltips BetterStats BetterFont)
fi

STAGE="dist/_stage/StolenRealm-Mods"
rm -rf dist/_stage
mkdir -p "$STAGE/BepInEx/plugins" dist

# PKG-6: o pacote distribuido sai da build de RELEASE (a mesma que o
# tools/pack-thunderstore.py empacota). O caminho da DLL segue a configuracao, como o
# $(Configuration) do MSBuild. Para empacotar Debug: CONFIG=Debug bash tools/pack-for-friends.sh
CONFIG="${CONFIG:-Release}"

echo "== compilando (config $CONFIG) =="
FAIL=0
for m in "${MODS[@]}"; do
  if [ ! -f "$m/$m.csproj" ]; then
    echo "  !! projeto '$m' não encontrado — pulando"
    continue
  fi
  printf "  %-18s " "$m"
  # -c $CONFIG: build de Release (a que vira pacote).
  # -p:DeployToBepInEx=false: NÃO copia para o perfil do r2modman — gerar pacote não
  #   pode sobrescrever a DLL que está instalada e em teste.
  # -clp:ErrorsOnly: só erro no log de build; -v q: sem ruído de warnings
  if LC_ALL=C dotnet build "$m/$m.csproj" -c "$CONFIG" -p:DeployToBepInEx=false \
     --nologo -v q -clp:ErrorsOnly > "dist/_stage/_b_$m.log" 2>&1 \
     && ! grep -aq "error CS" "dist/_stage/_b_$m.log"; then
    echo "ok"
  else
    echo "FALHOU"
    grep -a "error CS" "dist/_stage/_b_$m.log" | head -5 || true
    FAIL=1
  fi
done
if [ "$FAIL" -ne 0 ]; then
  echo
  echo "Compilação falhou — pacote NÃO gerado."
  exit 1
fi

echo "== montando o pacote =="
INCLUIDOS=()
for m in "${MODS[@]}"; do
  [ -f "$m/$m.csproj" ] || continue
  DLL="$m/bin/$CONFIG/netstandard2.1/$m.dll"
  if [ ! -f "$DLL" ]; then
    echo "  !! DLL não encontrada: $DLL"
    FAIL=1
    continue
  fi
  mkdir -p "$STAGE/BepInEx/plugins/$m"
  cp "$DLL" "$STAGE/BepInEx/plugins/$m/"
  INCLUIDOS+=("$m")
  echo "  + $m/$m.dll"
done
if [ "$FAIL" -ne 0 ]; then
  echo
  echo "Faltou DLL — pacote NÃO gerado."
  exit 1
fi

cp docs/LEIA-ME.txt "$STAGE/LEIA-ME.txt"
rm -f dist/_stage/_b_*.log

DATA="$(date +%F)"
ZIP="dist/StolenRealm-Mods-$DATA.zip"
rm -f "$ZIP"

# Compress-Archive: o PowerShell 5 (que já vem no Windows) dá conta do zip.
STAGE_WIN="$(cygpath -w "$STAGE")"
ZIP_WIN="$(cygpath -w "$ZIP")"
powershell.exe -NoProfile -Command "Compress-Archive -Path '$STAGE_WIN' -DestinationPath '$ZIP_WIN' -Force" >/dev/null

rm -rf dist/_stage

echo
echo "PRONTO -> $ZIP"
echo "Mods no pacote: ${INCLUIDOS[*]}"
ls -la "$ZIP"
