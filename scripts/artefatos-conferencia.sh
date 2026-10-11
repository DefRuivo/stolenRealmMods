#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# RSTV-29D-S0 -- Medicao REPRODUZIVEL dos artefatos citados na secao 0 de
# docs/CONFERENCIA-DONO-06-10.md.
#
# O que faz: LE (nunca escreve) o sha256 e o mtime das DLLs INSTALADAS no
# perfil do r2modman e das DLLs ja buildadas em <Mod>/bin/<Config>/ no repo,
# imprime a tabela da secao 0 pronta para colar e, em seguida, confere os
# MARCADORES citados na secao 0 (literais dentro das DLLs instaladas).
#
# NAO instala, NAO builda, NAO abre o jogo, NAO commita: so le o que ja esta
# no disco. (O hash do bin/<Config> e lido do arquivo existente, nao rebuildado.)
#
# Uso:
#   bash scripts/artefatos-conferencia.sh
#   bash scripts/artefatos-conferencia.sh > tabela.md     # capturar a tabela
#
# Reprodutibilidade: rodar duas vezes da saida BYTE-IDENTICA em stdout. O
# carimbo de data sai em stderr, de proposito, para nao sujar a comparacao.
#
# Variaveis de ambiente:
#   PERFIL_BEPINEX=<dir>   pasta plugins/ do perfil (padrao: o perfil Default)
#   RAIZ_REPO=<dir>        raiz do repo (padrao: a pasta acima deste script)
# ---------------------------------------------------------------------------
set -uo pipefail

RAIZ_REPO="${RAIZ_REPO:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
PERFIL_BEPINEX="${PERFIL_BEPINEX:-$APPDATA/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx/plugins}"

# mod | pasta no perfil | nome da DLL | pasta do mod no repo
MODS=(
  "BetterTooltips|BetterTooltips|BetterTooltips.dll|BetterTooltips"
  "RoguelikeSkillTreeVisualizer|RoguelikeSkillTreeVisualizer|RoguelikeSkillTreeVisualizer.dll|RoguelikeSkillTreeVisualizer"
  "RoguelikeDebugger|RoguelikeDebugger|RoguelikeDebugger.dll|RoguelikeDebugger"
)

# sha256 sem escape de nome de arquivo (o stdin nao imprime o caminho):
# 'sha256sum < arquivo' devolve "<hash>  -" e o cut pega os 12 primeiros.
sha12() { sha256sum < "$1" 2>/dev/null | cut -c1-12; }
# mtime no mesmo formato do documento (dd/mm HH:MM:SS, hora local):
mtime_curto() { date -r "$1" '+%d/%m %H:%M:%S' 2>/dev/null; }
mtime_iso() { date -r "$1" '+%Y-%m-%d %H:%M:%S %z' 2>/dev/null; }
epoch() { stat -c '%Y' "$1" 2>/dev/null; }

# Acha a DLL de um mod em <Mod>/bin/<Config>/<tfm>/<dll> (ou direto em bin/<Config>/).
achar_build() {
  local moddir="$1" dll="$2" cfg="$3" cand
  for cand in "$RAIZ_REPO/$moddir/bin/$cfg"/*/"$dll" "$RAIZ_REPO/$moddir/bin/$cfg/$dll"; do
    [ -f "$cand" ] && { printf '%s\n' "$cand"; return 0; }
  done
  return 1
}

# .cs do mod do mais novo para o mais antigo (fora de bin/ e obj/).
fontes_ordenadas() {
  find "$RAIZ_REPO/$1" -name '*.cs' -not -path '*/bin/*' -not -path '*/obj/*' \
    -printf '%T@ %p\n' 2>/dev/null | sort -rn | cut -d' ' -f2-
}

# As 2 fontes mais novas do mod, formatadas para a coluna "Fonte mais nova no repo".
fontes_novas() {
  local p saida=""
  while IFS= read -r p; do
    [ -n "$saida" ] && saida="$saida · "
    saida="$saida\`$(basename "$p")\` $(mtime_curto "$p")"
  done < <(fontes_ordenadas "$1" | head -2)
  printf '%s' "$saida"
}

echo "| Mod | DLL do perfil | sha256 (12 primeiros) | Fonte mais nova no repo | Veredito |"
echo "|---|---|---|---|---|"

for linha in "${MODS[@]}"; do
  IFS='|' read -r nome pasta_perfil dll moddir <<<"$linha"
  dll_perfil="$PERFIL_BEPINEX/$pasta_perfil/$dll"

  if [ ! -f "$dll_perfil" ]; then
    printf '| %s | AUSENTE | — | %s | **NÃO MEDÍVEL** (não existe no perfil) |\n' \
      "$nome" "$(fontes_novas "$moddir")"
    continue
  fi

  h_perfil="$(sha12 "$dll_perfil")"
  dia_perfil="$(date -r "$dll_perfil" '+%d/%m')"
  hora_perfil="$(date -r "$dll_perfil" '+%H:%M:%S')"

  # Com qual bin/<Config>/ do repo a DLL instalada bate byte a byte?
  veredito="INSTALADA, mas **DIVERGENTE** de todo bin/ do repo"
  for cfg in Release Debug; do
    b="$(achar_build "$moddir" "$dll" "$cfg" || true)"
    if [ -n "$b" ] && [ "$(sha12 "$b")" = "$h_perfil" ]; then
      veredito="**INSTALADA** (byte-idêntica à build $cfg)"
      break
    fi
  done

  # A fonte do repo e mais nova que a DLL instalada? => a mudanca nao esta instalada.
  p_novo="$(fontes_ordenadas "$moddir" | head -1)"
  if [ -n "$p_novo" ] && [ "$(stat -c '%Y' "$p_novo")" -gt "$(stat -c '%Y' "$dll_perfil")" ]; then
    veredito="$veredito · fonte do repo **MAIS NOVA** que a DLL instalada (mudança não instalada)"
  fi

  printf '| %s | %s **%s** | `%s` | %s | %s |\n' \
    "$nome" "$dia_perfil" "$hora_perfil" "$h_perfil" "$(fontes_novas "$moddir")" "$veredito"
done

# ---------------------------------------------------------------------------
# Prova com caminho: cada artefato medido, por extenso (sha256 completo + mtime).
# ---------------------------------------------------------------------------
echo
echo '```'
for linha in "${MODS[@]}"; do
  IFS='|' read -r nome pasta_perfil dll moddir <<<"$linha"
  dll_perfil="$PERFIL_BEPINEX/$pasta_perfil/$dll"
  if [ -f "$dll_perfil" ]; then
    echo "# PERFIL  $(sha256sum < "$dll_perfil" | awk '{print $1}')  $(mtime_iso "$dll_perfil")  $dll_perfil"
  else
    echo "# PERFIL  AUSENTE  $dll_perfil"
  fi
  for cfg in Release Debug; do
    b="$(achar_build "$moddir" "$dll" "$cfg" || true)"
    if [ -n "$b" ]; then
      echo "# $cfg  $(sha256sum < "$b" | awk '{print $1}')  $(mtime_iso "$b")  $b"
    fi
  done
done
echo '```'

# ---------------------------------------------------------------------------
# Marcadores citados na secao 0: literais DENTRO das DLLs instaladas.
# Os literais .NET ficam em UTF-16LE no heap #US, entao a busca e por bytes
# UTF-16 (o mesmo que a decompilacao enxerga) -- nao por ASCII.
# ---------------------------------------------------------------------------
echo
if command -v python >/dev/null 2>&1; then
  python - "$PERFIL_BEPINEX" \
    "BetterTooltips|Your active shrine auras:" \
    "BetterTooltips|Consuming any Globule heals you for" \
    "BetterTooltips|CorDaLinhaDeAuras" \
    "BetterTooltips|In the aura now (raw damage it takes as the attacker" \
    "BetterTooltips|damage per turn while in the aura." \
    "RoguelikeSkillTreeVisualizer|RSTV DIAG: botao 'Skills'" \
    "RoguelikeDebugger|[FlameRV49]" \
    "RoguelikeDebugger|BOOT " \
    "RoguelikeDebugger|PROC Source=" \
    "RoguelikeDebugger|PROC Target=" \
    "RoguelikeDebugger|PCT de " \
    "RoguelikeDebugger|DANO final[" \
    "RoguelikeDebugger|MATRIZ '" \
    "RoguelikeDebugger|CRU " <<'PY'
import os, sys
sys.stdout.reconfigure(newline='\n')          # stdout sem CRLF (Windows)
raiz, entradas = sys.argv[1], sys.argv[2:]
print('| Marcador (citado na seção 0) | DLL do perfil | Ocorrências | Veredito |')
print('|---|---|---|---|')
for e in entradas:
    mod, marcador = e.split('|', 1)
    caminho = os.path.join(raiz, mod, mod + '.dll')
    if not os.path.isfile(caminho):
        print('| `%s` | %s | — | **NAO MEDIVEL** (DLL ausente) |' % (marcador, mod))
        continue
    with open(caminho, 'rb') as fh:
        dado = fh.read()
    # Literal de string .NET vive em UTF-16LE (heap #US); nome de campo/classe
    # vive em UTF-8 (heap #Strings). Contamos os dois: o marcador esta na DLL
    # se aparecer em qualquer um deles.
    n = dado.count(marcador.encode('utf-16-le')) + dado.count(marcador.encode('utf-8'))
    veredito = 'PRESENTE' if n else '**AUSENTE**'
    print('| `%s` | %s | %d | %s |' % (marcador, mod, n, veredito))
PY
else
  echo "_Marcadores NAO MEDIDOS: 'python' nao esta no PATH desta maquina._"
fi

# Carimbo de execucao vai para stderr: stdout fica byte-identico entre rodadas.
{
  echo "medido em $(date '+%Y-%m-%d %H:%M:%S %z')"
  echo "repo:   $RAIZ_REPO"
  echo "perfil: $PERFIL_BEPINEX"
} >&2
