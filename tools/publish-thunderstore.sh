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
#
# QUEM PODE SUBIR: `release/mods.json` (PKG-API-1)
# ------------------------------------------------
# O pipeline (.github/workflows/publish.yml) SEMPRE leu esse ledger; este publicador
# local NAO lia - ele subia o que estivesse em `dist/`, inclusive versao antiga e mod
# TRAVADO (publicar:false). Agora o passo 0 le o MESMO ledger e o MESMO empacotador
# (`tools/pack-thunderstore.py`), imprime o estado de cada pacote e SO os `publicar:true`
# entram no plano de envio. TRAVADO e "sem entrada no ledger" aparecem como TRAVADO e
# nao sao empacotados nem enviados.
#
# O token so e' EXIGIDO quando ha envio (`--go`). No dry-run ele continua sendo validado
# se estiver disponivel, mas a ausencia dele nao aborta mais um run que nao envia nada -
# era o que impedia de ver o plano de envio numa maquina sem credencial.
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

mkdir -p dist
PLANO="dist/.plano-publicacao"

# --- 0) LEDGER: quem esta liberado ------------------------------------------
# Le `release/mods.json` (a decisao humana) e `--listar-caminhos` do empacotador (a
# descoberta de pacote) - as duas fontes que o pipeline usa. Escreve o plano de envio em
# $PLANO, no formato `nome|zip|versao`, e imprime a tabela de estado. A versao sai do
# `<Version>` do .csproj, a mesma fonte unica do PKG-2.
echo "== ledger (release/mods.json + tools/pack-thunderstore.py) =="
python - "$SO" "$PLANO" <<'PY' || exit 1
import json, re, subprocess, sys

escolha = (sys.argv[1] or '').strip()
plano_path = sys.argv[2]

def morre(msg):
    print('!! ' + msg)
    sys.exit(1)

with open('release/mods.json', encoding='utf-8') as fh:
    dados = json.load(fh)
mods = dados.get('mods') or []
nomes_json = [m.get('nome') for m in mods]

p = subprocess.run([sys.executable, 'tools/pack-thunderstore.py', '--listar-caminhos'],
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
if p.returncode != 0:
    morre('tools/pack-thunderstore.py --listar-caminhos saiu %d: %s'
          % (p.returncode, p.stdout.decode('utf-8', 'replace').strip()))
caminhos = {c['nome']: c for c in json.loads(p.stdout.decode('utf-8'))}

fantasmas = [n for n in nomes_json if n not in caminhos]
if fantasmas:
    morre('release/mods.json lista mod(s) que o empacotador NAO conhece: %s. A lista de mods '
          'tem uma fonte so (tools/pack-thunderstore.py --listar-nomes).'
          % ', '.join(fantasmas))

def versao(csproj):
    with open(csproj, encoding='utf-8', errors='replace') as fh:
        achado = re.search(r'<Version>([^<]+)</Version>', fh.read())
    return achado.group(1).strip() if achado else None

print('  %-34s %-9s %s' % ('pacote', 'estado', 'detalhe'))
liberados, travados, sem_ledger = [], [], []
for m in mods:
    nome = m.get('nome')
    if m.get('publicar') is True:
        liberados.append(nome)
        print('  %-34s %-9s %s' % (nome, 'LIBERADO', 'publicar:true'))
    else:
        travados.append(nome)
        motivo = (m.get('motivo') or 'sem motivo registrado').replace('\n', ' ')
        print('  %-34s %-9s %s' % (nome, 'TRAVADO', motivo))
for nome in sorted(caminhos):
    if nome not in nomes_json:
        sem_ledger.append(nome)
        print('  %-34s %-9s %s' % (nome, 'TRAVADO',
                                   'sem entrada em release/mods.json - nunca e enviado'))
print()
print('  liberados: %d | travados no ledger: %d | sem entrada no ledger: %d'
      % (len(liberados), len(travados), len(sem_ledger)))

plano = []
for nome in liberados:
    v = versao(caminhos[nome]['csproj'])
    if not v:
        morre('PKG-2: %s sem <Version> no .csproj - nao da para saber qual pacote subiria.'
              % caminhos[nome]['csproj'])
    plano.append('%s|dist/gumatos-%s-%s.zip|%s' % (nome, nome, v, v))
with open(plano_path, 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(plano) + ('\n' if plano else ''))

if not liberados:
    print('  Nada a fazer: nenhum mod com publicar:true em release/mods.json.')
    sys.exit(0)
if escolha and escolha not in liberados:
    if escolha in travados or escolha in sem_ledger:
        morre('%s esta TRAVADO em release/mods.json e nao sera publicado. Motivo: %s'
              % (escolha, next((m.get('motivo') for m in mods if m.get('nome') == escolha),
                               'sem entrada em release/mods.json')))
    morre('%s nao existe em release/mods.json (opcoes: %s)'
          % (escolha, ', '.join(nomes_json)))
print('  pedido   : %s' % (escolha or 'todos os liberados'))
print('  vao subir: %s' % ', '.join(p.split('|')[0] for p in plano))
PY

NOMES_LIBERADOS=()
if [ -s "$PLANO" ]; then
  while IFS='|' read -r nome _zip _versao; do
    [ -n "$nome" ] || continue
    NOMES_LIBERADOS+=("$nome")
  done < "$PLANO"
fi
if [ "${#NOMES_LIBERADOS[@]}" = "0" ]; then
  echo "== nada liberado para publicar (publicar:true) - encerrando. =="
  exit 0
fi

# --- 1) de onde vem o token -------------------------------------------------
TOKEN="${TCLI_AUTH_TOKEN:-}"
ARQ="${THUNDERSTORE_TOKEN_FILE:-$HOME/.thunderstore-token}"
if [ -z "$TOKEN" ]; then
  case "$ARQ" in
    "$RAIZ"/*) echo "!! o arquivo de token esta DENTRO do repositorio: $ARQ"; echo "   mova para fora antes de continuar."; exit 1 ;;
  esac
  if [ -f "$ARQ" ]; then TOKEN="$(cat "$ARQ")"; fi
fi
if [ -n "$TOKEN" ]; then
  case "$TOKEN" in
    tss_*) ;;
    *) echo "!! isso nao parece um token do Thunderstore (completa com 'tss_')"; exit 1 ;;
  esac
elif [ "$GO" = "1" ]; then
  echo "!! token nao encontrado. Defina TCLI_AUTH_TOKEN ou crie $ARQ"; exit 1
else
  echo
  echo "aviso: sem token no ambiente. DRY-RUN NAO ENVIA NADA, entao o plano acima vale"
  echo "       igual - o token e' exigido so no envio de verdade (--go)."
fi

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
echo "== empacotando (so os LIBERADOS: quem manda e' o ledger) =="
rm -rf dist/tmp-pub && mkdir -p dist/tmp-pub
if [ -n "$SO" ]; then
  python tools/pack-thunderstore.py "$SO"
else
  python tools/pack-thunderstore.py "${NOMES_LIBERADOS[@]}"
fi || exit 1

# --- 5) subir ---------------------------------------------------------------
echo
echo "== envio =="
FALHOU=0
while IFS='|' read -r nome z versao; do
  [ -n "$nome" ] || continue
  [ -f "$z" ] || { echo "   [FALTA] $nome: $z nao existe (nao empacotou neste run)"; FALHOU=1; continue; }
  if [ "$GO" != "1" ]; then
    echo "   [DRY-RUN] subiria: $(basename "$z") ($(stat -c %s "$z") bytes) -> $API"
    continue
  fi
  printf '   subindo %-46s ' "$(basename "$z")"
  RESP="$(curl -s -w '\n%{http_code}' --max-time 300 -H "Authorization: Bearer ***" -F "file=@$z" "$API")"
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
done < "$PLANO"

rmdir dist/tmp-pub 2>/dev/null
rm -f "$PLANO"
echo
if [ "$GO" != "1" ]; then
  echo "== DRY-RUN terminou. Nada foi publicado. Use --go para publicar de verdade. =="
elif [ "$FALHOU" = "1" ]; then
  echo "== ATENCAO: houve falha em pelo menos um pacote (veja acima). =="
  exit 1
else
  echo "== publicado. Confira em https://thunderstore.io/c/stolen-realm/ =="
fi
