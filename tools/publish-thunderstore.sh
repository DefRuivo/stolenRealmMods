#!/usr/bin/env bash
# Publica os pacotes do Thunderstore. NAO guarda credencial em lugar nenhum.
#
# Uso:
#   bash tools/publish-thunderstore.sh                 # DRY-RUN: mostra o que subiria, nao sobe
#   bash tools/publish-thunderstore.sh --go            # sobe de verdade
#   bash tools/publish-thunderstore.sh --go OnlyName   # sobe um mod especifico
#
# O token vem de, nesta ordem: variavel TCLI_AUTH_TOKEN, arquivo apontado por
# THUNDERSTORE_TOKEN_FILE, ou ~/.thunderstore-token. Nunca do repositorio.
set -u
cd "$(dirname "$0")/.." || exit 1
RAIZ="$(pwd)"
API="https://thunderstore.io/api/experimental/package/upload/"

GO=0; SO=""
for a in "$@"; do
  case "$a" in
    --go) GO=1 ;;
    -*) echo "opcao desconhecida: $a"; exit 2 ;;
    *) SO="$a" ;;
  esac
done

# --- 1) de onde vem o token -------------------------------------------------
TOKEN="${TCLI_AUTH_TOKEN:-}"
if [ -z "$TOKEN" ]; then
  ARQ="${THUNDERSTORE_TOKEN_FILE:-$HOME/.thunderstore-token}"
  case "$ARQ" in
    "$RAIZ"/*) echo "!! o arquivo de token esta DENTRO do repositorio: $ARQ"; echo "   mova para fora antes de continuar."; exit 1 ;;
  esac
  [ -f "$ARQ" ] || { echo "!! token nao encontrado. Defina TCLI_AUTH_TOKEN ou crie ~/.thunderstore-token"; exit 1; }
  TOKEN="$(cat "$ARQ")"
fi
case "$TOKEN" in
  tss_*) ;;
  *) echo "!! isso nao parece um token do Thunderstore (comeca com 'tss_')"; exit 1 ;;
esac

# --- 2) trava de segredo: nada de credencial no que vai a publico -----------
echo "== trava de segredo =="
python tools/check_segredos.py || { echo "!! abortado pela trava de segredo"; exit 1; }

# --- 3) trava de release ----------------------------------------------------
if [ "${PULAR_RELEASE_CHECK:-0}" != "1" ]; then
  echo
  echo "== trava de release (tools/release-check.sh) =="
  bash tools/release-check.sh || { echo "!! release-check falhou; nada foi publicado"; exit 1; }
fi

# --- 4) empacotar -----------------------------------------------------------
echo
echo "== empacotando =="
rm -rf dist/tmp-pub && mkdir -p dist/tmp-pub
if [ -n "$SO" ]; then python tools/pack-thunderstore.py "$SO"; else python tools/pack-thunderstore.py; fi || exit 1

# --- 5) subir ---------------------------------------------------------------
echo
echo "== envio =="
FALHOU=0
for z in dist/gumatos-*.zip; do
  [ -f "$z" ] || continue
  nome="$(basename "$z")"
  if [ "$GO" != "1" ]; then
    echo "   [DRY-RUN] subiria: $nome ($(stat -c %s "$z") bytes) -> $API"
    continue
  fi
  printf '   subindo %-46s ' "$nome"
  RESP="$(curl -s -w '\n%{http_code}' --max-time 300 -H "Authorization: Bearer $TOKEN" -F "file=@$z" "$API")"
  CODE="$(printf '%s' "$RESP" | tail -1)"
  CORPO="$(printf '%s' "$RESP" | sed '$d')"
  if [ "$CODE" = "200" ]; then
    URL="$(printf '%s' "$CORPO" | python -c "import sys,json;d=json.load(sys.stdin);print(d.get('package_version',{}).get('full_name','?')+' v'+str(d.get('package_version',{}).get('version_number','?')))" 2>/dev/null || echo '?')"
    echo "OK  $URL"
  else
    echo "FALHOU (HTTP $CODE)"
    printf '%s' "$CORPO" | head -c 300 | sed 's/^/        /'
    echo
    FALHOU=1
  fi
done

rmdir dist/tmp-pub 2>/dev/null
echo
if [ "$GO" != "1" ]; then
  echo "== DRY-RUN terminou. Nada foi publicado. Use --go para publicar de verdade. =="
elif [ "$FALHOU" = "1" ]; then
  echo "== ATENCAO: houve falha em pelo menos um pacote (veja acima). =="
  exit 1
else
  echo "== publicado. Confira em https://thunderstore.io/c/stolen-realm/ =="
fi
