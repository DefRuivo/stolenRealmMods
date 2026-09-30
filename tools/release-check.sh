#!/usr/bin/env bash
# =============================================================================
# release-check.sh — checklist automatizado de validacao de release
# -----------------------------------------------------------------------------
# Roda TODOS os passos automatizaveis na ordem certa e no final diz
# APROVADO ou REPROVADO, apontando qual passo falhou.
#
# Uso (da raiz do repo ou de qualquer subpasta):
#     bash tools/release-check.sh
#
# Passos:
#   0. SEGREDOS   — tools/check_segredos.py (nenhum token versionado)
#                   ABORTA NA HORA (exit 1): token no que seria publicado e o
#                   unico defeito em que nada mais importa.
#   1. VERSOES    — tools/check_versoes.py (PKG-2: <Version> do .csproj ==
#                   version_number do manifest.json == versao do Plugin.cs)
#                   ABORTA NA HORA (exit 1): com a versao divergente o log do
#                   BepInEx mente sobre a build carregada, e os passos CAROS
#                   abaixo (build/deploy e ciclo do jogo) testariam codigo novo
#                   achando que e o velho.
#   2. BUILD      — dotnet build de todos os <Mod>/<Mod>.csproj (0 erros CS)
#   3. CHAVES     — tools/check_fix_keys.py (chave dos textos existe no censo)
#   4. DUPLICADAS — tools/check_dupes.py    (trava INC-1: chave repetida derruba
#                   o mod INTEIRO com TypeInitializationException)
#   5. NOTAS      — tools/check_notas_redundantes.py (nota que repete o texto)
#   6. COMPARTILH.— tools/check_chave_compartilhada.py --estrito  (TRAVA BUG-32:
#                   a MESMA chave em TextFixes E TextAppends = a entrada de
#                   TextAppends nunca roda e a nota nao existe em jogo, em
#                   silencio. As SUSPEITAS de texto compartilhado NESTA MESMA
#                   ferramenta seguem aviso: dependem de decisao humana.)
#   7. CICLO      — scratch/test-cycle.sh (abre/fecha o jogo) + analise do
#                   LogOutput.log: 0 TypeInitializationException,
#                   0 ArgumentException, 0 linhas '[Error'
#   8. HUMANO     — lista do que so um humano confere em jogo (nao automatizavel)
#
# O mesmo miolo de repositorio roda no CI (.github/workflows/validate.yml), na
# mesma ordem: 1 segredos, 2 versoes, 3 chaves, 4 duplicadas, 5 notas, 6 chave
# compartilhada --estrito, 7 pacotes, 8 auditoria dos docs.
#
# Notas de projeto:
#   * NAO usa `set -e`: o relatorio final TEM que aparecer mesmo com falha.
#     Por isso so os passos 0 e 1 ABORTAM na hora (exit 1); do 2 em diante tudo
#     acumula e chega ao RESUMO FINAL, mesmo reprovado.
#   * Nunca toca Assembly-CSharp.dll; backup de DLL nunca vai para plugins/.
#   * O <Mod>.csproj tem o Target DeployToBepInEx: buildar JA INSTALA a DLL no
#     perfil do r2modman (por isso o preparo fecha o jogo antes do build).
# =============================================================================
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RAIZ="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$RAIZ" || { echo "nao consegui entrar em $RAIZ"; exit 2; }

# ------------------------------ configuracao ---------------------------------
PYTHON="${PYTHON:-}"
if [ -z "$PYTHON" ]; then
  if command -v python  >/dev/null 2>&1; then PYTHON=python
  elif command -v python3 >/dev/null 2>&1; then PYTHON=python3
  else PYTHON=python; fi
fi

APPID=1330000
STEAM="${STEAM:-/c/Program Files (x86)/Steam/steam.exe}"
PERFIL="${APPDATA:-$HOME/AppData/Roaming}/r2modmanPlus-local/StolenRealm/profiles/Default/BepInEx"
LOG="${BEPINEX_LOG_OVERRIDE:-$(cygpath -u "$PERFIL")/LogOutput.log}"
PLUGINS_DIR="$(cygpath -u "$PERFIL")/plugins"
SEGUNDOS_CICLO="${SEGUNDOS_CICLO:-12}"
PADRAO_CICLO="${PADRAO_CICLO:-Better Tooltips carregado}"

# --------------------------- acumulador de falhas ----------------------------
CHECKS=()   # "STATUS|NOME|DETALHE"
FALHAS=()
passo_ok()   { CHECKS+=("OK|$1|$2"); }
passo_fail() { CHECKS+=("FALHA|$1|$2"); FALHAS+=("$1"); }

TMPD="$(mktemp -d 2>/dev/null || echo "${TMPDIR:-/tmp}/release-check.$$")"
mkdir -p "$TMPD"
trap 'rm -rf "$TMPD"' EXIT

linha() { printf '=%.0s' $(seq 1 78); printf '\n'; }

echo
linha
echo " RELEASE-CHECK — $(date '+%Y-%m-%d %H:%M:%S')"
echo " raiz do repo : $RAIZ"
echo " jogo         : E:\\SteamLibrary\\steamapps\\common\\Stolen Realm (AppID $APPID)"
echo " log BepInEx  : $LOG"
echo " python       : $($PYTHON --version 2>&1)"
linha

# =============================== PREPARO =====================================
# O build copia a DLL para plugins\ (Target DeployToBepInEx). Com o jogo aberto
# a copia falha (arquivo em uso) e o build "passa" no compilador mas nao instala.
echo
echo "== PREPARO: garantir que o jogo esta fechado antes do build/deploy =="
if taskkill /F /IM "Stolen Realm.exe" >/dev/null 2>&1; then
  echo "   instancia anterior do jogo encerrada"
else
  echo "   nenhuma instancia rodando"
fi

# ================================ 0. SEGREDOS ================================
echo
echo "== PASSO 0/8 — SEGREDOS =="
if $PYTHON tools/check_segredos.py; then
  echo "  [ OK ] 0. nenhum token nos arquivos versionados"
  passo_ok "0. SEGREDOS" "nenhum token nos arquivos versionados"
else
  echo "  [FALHA] 0. credencial no que seria publicado - release travada"
  exit 1
fi

# ================================ 1. VERSOES =================================
# Trava PKG-2, e nao precisa de build nem de DLL: a versao tem de ser a MESMA no
# <Version> do .csproj (fonte), no version_number do manifest.json e no Plugin.cs
# (o [BepInPlugin(...)] ou a const Version). ABORTA NA HORA, como o passo 0:
# versao divergente faz o log do BepInEx mentir sobre a build carregada, entao o
# build abaixo (que JA INSTALA a DLL no perfil) e o ciclo testariam codigo novo
# achando que e o velho - e o pacote sairia com versao errada.
echo
echo "== PASSO 1/8 — VERSOES (check_versoes.py: csproj = manifest = Plugin.cs) =="
SAIDA_VERSOES="$($PYTHON tools/check_versoes.py 2>&1)"; rc_versoes=$?
printf '%s\n' "$SAIDA_VERSOES" | sed 's/^/   /'
if [ "$rc_versoes" -eq 0 ]; then
  det_versoes=$(printf '%s\n' "$SAIDA_VERSOES" | grep -aoE 'os [0-9]+ mods batem nos tres lugares' | head -1)
  passo_ok "1. VERSOES" "${det_versoes:-csproj = manifest = Plugin.cs}"
else
  echo
  if [ "$rc_versoes" -eq 2 ]; then
    echo "  [FALHA] 1. versao AUSENTE num lugar obrigatorio - release travada"
  else
    echo "  [FALHA] 1. versao DIVERGE entre csproj/manifest/Plugin.cs - release travada"
  fi
  echo "   >>> BLOQUEIO DE RELEASE (PKG-2) <<<"
  echo "   O <Version> do .csproj e a FONTE; manifest.json e Plugin.cs sao ESPELHOS."
  echo "   Conserto (a mao, ou de uma vez para todos os mods):"
  echo "     python tools/pack-thunderstore.py --sincronizar-versao"
  echo "   Nada foi buildado e nada foi instalado no perfil: corrija a versao e"
  echo "   rode o release-check de novo."
  exit 1
fi

# ================================= 2. BUILD ==================================
echo
echo "== PASSO 2/8 — BUILD (todos os .csproj de mod na raiz) =="

mapfile -t PROJETOS < <(find . -maxdepth 2 -name '*.csproj' \
                          -not -path '*/bin/*' -not -path '*/obj/*' \
                        | sed 's|^\./||' | sort)
if [ "${#PROJETOS[@]}" -eq 0 ]; then
  passo_fail "2. BUILD" "nenhum .csproj encontrado"
  echo "   ERRO: nenhum .csproj encontrado na raiz do repo"
else
  echo "   projetos descobertos: ${#PROJETOS[@]} -> ${PROJETOS[*]}"
  ERROS_TOTAL=0
  PROJS_FALHOS=0
  DETALHES_BUILD=""
  for p in "${PROJETOS[@]}"; do
    nome="$(basename "$p" .csproj)"
    out="$TMPD/build-$nome.log"
    ( LC_ALL=C dotnet build "$p" --nologo -v q -clp:ErrorsOnly >"$out" 2>&1 )
    rc=$?
    ncs=$(grep -ac 'error CS' "$out" || true); ncs=${ncs:-0}
    if [ "$ncs" -gt 0 ] || [ "$rc" -ne 0 ]; then
      printf '   [FALHA] %-18s %s erro(s) CS (exit %s)\n' "$nome" "$ncs" "$rc"
      grep -aE 'error [A-Z]+[0-9]+' "$out" | head -10 | sed 's/^/           /'
      PROJS_FALHOS=$((PROJS_FALHOS + 1))
    else
      printf '   [ ok  ] %-18s 0 erro(s) CS (exit 0, deploy do csproj executado)\n' "$nome"
    fi
    ERROS_TOTAL=$((ERROS_TOTAL + ncs))
    DETALHES_BUILD="$DETALHES_BUILD $nome=$ncs"
  done
  if [ "$PROJS_FALHOS" -eq 0 ]; then
    passo_ok "2. BUILD" "${#PROJETOS[@]} projetos, $ERROS_TOTAL erros CS"
  else
    passo_fail "2. BUILD" "$PROJS_FALHOS/${#PROJETOS[@]} projeto(s) com falha, $ERROS_TOTAL erros CS"
  fi
fi

# =============================== 3. CHAVES ===================================
echo
echo "== PASSO 3/8 — CHAVES (check_fix_keys.py: chave de texto existe no censo?) =="
SAIDA_CHAVES="$($PYTHON tools/check_fix_keys.py 2>&1)"; rc=$?
printf '%s\n' "$SAIDA_CHAVES" | sed 's/^/   /'
if [ "$rc" -ne 0 ]; then
  passo_fail "3. CHAVES" "check_fix_keys.py NAO RODOU (exit $rc)"
else
  N_EXTRA=$(printf '%s\n' "$SAIDA_CHAVES" | grep -aoE 'chaves extraidas: [0-9]+' | grep -oE '[0-9]+' | head -1)
  N_CENSO=$(printf '%s\n' "$SAIDA_CHAVES" | grep -aoE 'no censo *: [0-9]+' | grep -oE '[0-9]+' | head -1)
  N_FORA=$(printf '%s\n' "$SAIDA_CHAVES" | grep -aoE 'fora do censo: [0-9]+' | grep -oE '[0-9]+' | head -1)
  N_EXTRA=${N_EXTRA:-?}; N_CENSO=${N_CENSO:-?}; N_FORA=${N_FORA:-0}
  if [ "$N_FORA" != "0" ] && [ "$N_FORA" != "?" ]; then
    echo "   AVISO (nao reprova): $N_FORA chave(s) fora do censo — pode ser texto de UI/loading"
    echo "   ainda nao coberto pelo censo (ver docs/cobertura/README.md)."
  fi
  passo_ok "3. CHAVES" "$N_EXTRA chaves extraidas, $N_CENSO no censo, $N_FORA fora"
fi

# ============================= 4. DUPLICADAS =================================
echo
echo "== PASSO 4/8 — DUPLICADAS (trava INC-1: chave repetida = jogo sem o mod) =="
SAIDA_DUP="$($PYTHON tools/check_dupes.py 2>&1)"; rc=$?
printf '%s\n' "$SAIDA_DUP" | sed 's/^/   /'
if [ "$rc" -eq 1 ]; then
  passo_fail "4. DUPLICADAS" "chave duplicada — INC-1, NAO INSTALAR NADA"
  echo
  echo "   >>> BLOQUEIO DE RELEASE (INC-1) <<<"
  echo "   Chave repetida em Dictionary<string,string> = ArgumentException no"
  echo "   construtor estatico do LocalizePatch = TypeInitializationException e"
  echo "   NENHUMA tabela do mod carrega. Regra: UMA entrada por TEXTO, nunca por skill."
elif [ "$rc" -ne 0 ]; then
  passo_fail "4. DUPLICADAS" "check_dupes.py NAO RODOU (exit $rc) — trava INC-1 nao verificada"
else
  det_dup=$(printf '%s\n' "$SAIDA_DUP" | grep -aoE 'TextFixes[[:space:]]+[0-9]+ entradas \| duplicadas: [a-z]+' | head -1)
  passo_ok "4. DUPLICADAS" "${det_dup:-nenhuma duplicada}"
fi

# ======================= 5. NOTAS REDUNDANTES ================================
echo
echo "== PASSO 5/8 — NOTAS REDUNDANTES (a nota repete o texto que ja estava la?) =="
SAIDA_NOTAS="$($PYTHON tools/check_notas_redundantes.py 2>&1)"; rc=$?
printf '%s
' "$SAIDA_NOTAS" | sed 's/^/   /'
if [ "$rc" -eq 1 ]; then
  passo_fail "5. NOTAS" "nota redundante/duplicada — o jogador le a mesma frase duas vezes"
  echo
  echo "   >>> REVISAR ANTES DE PUBLICAR <<<"
  echo "   Uma nota existe para dizer o que o texto NAO diz. Familias: nota == chave (a frase"
  echo "   aparece DUPLICADA na tela), nota contida na chave, nota que ecoa o texto, e nota de"
  echo "   Armor onde Armor e FONTE de dano e nao mitigacao. As regras que impedem o ultimo caso"
  echo "   estao no codigo (ArmorValueSourceRegex) - se aparecer caso aqui, a regra falhou."
  echo "   Relatorio: docs/cobertura/revisao/RV-15-notas-redundantes.md"
elif [ "$rc" -ne 0 ]; then
  passo_fail "5. NOTAS" "check_notas_redundantes.py NAO RODOU (exit $rc) — nao verificada"
else
  det_notas=$(printf '%s
' "$SAIDA_NOTAS" | grep -aoE 'notas analisadas [.]+ [0-9]+' | head -1)
  passo_ok "5. NOTAS" "${det_notas:-0 casos}"
fi

# ======================= 6. CHAVE COMPARTILHADA ==============================
echo
echo "== PASSO 6/8 — CHAVE COMPARTILHADA (trava BUG-32: chave nas DUAS tabelas) =="
SAIDA_COMP="$($PYTHON tools/check_chave_compartilhada.py --estrito 2>&1)"; rc_comp=$?
printf '%s\n' "$SAIDA_COMP" | sed 's/^/   /'
if [ "$rc_comp" -eq 1 ]; then
  N_AMBAS=$(printf '%s\n' "$SAIDA_COMP" | grep -aoE 'chave nas DUAS tabelas \(TextFixes\+TextAppends\) [.]+ [0-9]+' | grep -oE '[0-9]+$' | head -1)
  passo_fail "6. COMPARTILH." "${N_AMBAS:-1} chave(s) nas DUAS tabelas — BUG-32, release travada"
  echo
  echo "   >>> BLOQUEIO DE RELEASE (BUG-32) <<<"
  echo "   A MESMA chave existe em TextFixes e em TextAppends. O lookup e if/else if"
  echo "   na mesma chave, entao a entrada de TextAppends NUNCA roda: a nota nao"
  echo "   existe em jogo, em silencio, sem erro nenhum no log. NAO e opiniao."
  echo "   Correcao: UMA entrada por texto — fundir o valor da TextAppends no valor"
  echo "   da TextFixes (a que executa hoje) e apagar a duplicada."
elif [ "$rc_comp" -ne 0 ]; then
  passo_fail "6. COMPARTILH." "check_chave_compartilhada.py NAO RODOU (exit $rc_comp) — trava BUG-32 nao verificada"
else
  N_SUSP=$(printf '%s\n' "$SAIDA_COMP" | grep -aoE 'SUSPEITAS[^:]*: [0-9]+' | grep -oE '[0-9]+' | head -1)
  N_SUSP=${N_SUSP:-0}
  if [ "$N_SUSP" != "0" ]; then
    echo
    echo "   AVISO (nao reprova): $N_SUSP suspeita(s) de chave compartilhada - a nota pode"
    echo "   estar mentindo para outro dono do texto. A decisao e humana (mecanica citada)."
    echo "   Revisar: docs/cobertura/revisao/BUG-32-chaves-compartilhadas.md"
  fi
  passo_ok "6. COMPARTILH." "0 chave nas duas tabelas; $N_SUSP suspeita(s) (aviso humano)"
fi

# ============================== 7. CICLO =====================================
echo
echo "== PASSO 7/8 — CICLO DO JOGO + ANALISE DO LOG =="
echo "   $ bash scratch/test-cycle.sh $SEGUNDOS_CICLO \"$PADRAO_CICLO\""
SAIDA_CICLO="$(bash scratch/test-cycle.sh "$SEGUNDOS_CICLO" "$PADRAO_CICLO" 2>&1)"; rc_ciclo=$?
printf '%s\n' "$SAIDA_CICLO" | sed 's/^/   | /'

# --- analise do log ---------------------------------------------------------
if [ ! -f "$LOG" ]; then
  echo "   ERRO: log nao existe: $LOG"
  passo_fail "7. CICLO" "sem log — o jogo nao chegou a subir"
else
  N_TIE=$(grep -ac 'TypeInitializationException' "$LOG" || true); N_TIE=${N_TIE:-0}
  N_ARG=$(grep -ac 'ArgumentException' "$LOG" || true);           N_ARG=${N_ARG:-0}
  N_ERR=$(grep -ac '^\[Error' "$LOG" || true);                    N_ERR=${N_ERR:-0}

  mapfile -t CARREGADOS < <(grep -aoE '^\[Info[[:space:]]*:[[:space:]]*BepInEx\][[:space:]]*Loading \[[^]]+\]' "$LOG" \
                            | sed -E 's/.*Loading \[([^]]+)\]/\1/')
  N_CARR=${#CARREGADOS[@]}
  N_DECL=$(grep -aoE '[0-9]+ plugins to load' "$LOG" | grep -oE '[0-9]+' | head -1); N_DECL=${N_DECL:-?}

  echo "   --- log: $LOG ---"
  printf '   TypeInitializationException : %s  (exigido 0)\n' "$N_TIE"
  printf '   ArgumentException           : %s  (exigido 0)\n' "$N_ARG"
  printf '   linhas iniciando com [Error : %s  (exigido 0)\n' "$N_ERR"
  printf '   plugins carregados          : %s (o BepInEx declarou %s)\n' "$N_CARR" "$N_DECL"
  for pl in "${CARREGADOS[@]}"; do printf '         * %s\n' "$pl"; done

  BT_OK=0
  if grep -aq 'Better Tooltips carregado' "$LOG"; then
    echo "   'Better Tooltips carregado' presente no log: SIM"
    BT_OK=1
  else
    echo "   'Better Tooltips carregado' presente no log: NAO"
  fi

  if [ "$N_TIE" -eq 0 ] && [ "$N_ARG" -eq 0 ] && [ "$N_ERR" -eq 0 ] && [ "$N_CARR" -gt 0 ] && [ "$BT_OK" -eq 1 ]; then
    passo_ok "7. CICLO" "$N_CARR plugins ok, 0 TIE, 0 ArgException, 0 [Error"
  else
    passo_fail "7. CICLO" "TIE=$N_TIE ArgEx=$N_ARG [Error=$N_ERR plugins=$N_CARR BT=$BT_OK (exit test-cycle=$rc_ciclo)"
    [ "$N_TIE" -gt 0 ] && grep -a -m3 -B1 'TypeInitializationException' "$LOG" | sed 's/^/        /'
    [ "$N_ERR" -gt 0 ] && grep -a -m3 '^\[Error' "$LOG" | sed 's/^/        /'
  fi
fi

# garante que o jogo ficou fechado
taskkill /F /IM "Stolen Realm.exe" >/dev/null 2>&1 || true

# ============================== 8. HUMANO ====================================
echo
echo "== PASSO 8/8 — PASSO HUMANO (NAO automatizavel: exige jogo aberto e olho humano) =="
cat <<'HUMANO'
   Estes itens NAO podem ser checados por script — nenhum deles aparece no log.
   O release NAO esta completo enquanto um humano nao conferir, em jogo:

   [ ] 5.1 Tooltips: a COR e a FONTE das explicacoes dentro dos tooltips de skill
            (claro/escuro em fundo claro e escuro; tamanho/legibilidade da fonte).
   [ ] 5.2 Tooltips: o TEXTO no FIM do tooltip (a linha final subscreve certo,
            sem corte, sem texto faltando, sem ingles sobrando).
   [ ] 5.3 Ficha de personagem (BetterStats): os NUMEROS dos stats batem com o
            que o jogo calcula de verdade (comparar valor exibido x real).
   [ ] 5.4 Renderizacao geral (BetterFont): acentuacao/glifos sem quadrados,
            sem corte de linha e sem sobreposicao nos textos alterados.
   [ ] 5.5 Uma partida real: abrir inventario, subir de nivel, passar um ataque
            e conferir que nada quebrou em combate (o ciclo automatico so abre
            o jogo e le o log — nao joga).

   Enquanto esses 5 itens nao forem marcados, o veredito abaixo e apenas
   "APROVADO na automacao", nunca "release pronto".
HUMANO

# ============================== RESUMO FINAL =================================
echo
linha
echo " RESUMO FINAL"
linha
for c in "${CHECKS[@]}"; do
  st="${c%%|*}"; resto="${c#*|}"; nome="${resto%%|*}"; det="${resto#*|}"
  if [ "$st" = "OK" ]; then
    printf '  [ OK ]   %-14s %s\n' "$nome" "$det"
  else
    printf '  [FALHA]  %-14s %s\n' "$nome" "$det"
  fi
done
printf '  [HUMANO] %-14s %s\n' "8. HUMANO" "conferencia visual em jogo (ver itens 5.1-5.5 acima) — sempre pendente"
echo
if [ "${#FALHAS[@]}" -eq 0 ]; then
  echo "  CONCLUSAO: APROVADO (verificacao automatizada: segredos, versoes, build, chaves, duplicadas, notas, chave compartilhada, ciclo)"
  echo "             LEMBRETE: o release so esta COMPLETO depois dos passos humanos 5.1-5.5."
  echo "             Nada foi instalado a mao: o build dos .csproj ja deployou as DLLs."
  RC=0
else
  echo "  CONCLUSAO: REPROVADO — passo(s) com falha: ${FALHAS[*]}"
  for f in "${FALHAS[@]}"; do
    case "$f" in
      "2. BUILD")      echo "             >> build quebrou: a DLL antiga continua em plugins/ — o ciclo testou codigo velho." ;;
      "3. CHAVES")     echo "             >> revisar a saida do check_fix_keys.py acima (chave fora do censo falha em silencio)." ;;
      "4. DUPLICADAS") echo "             >> BLOQUEIO INC-1: nao instale nem distribua nada ate as duplicadas sumirem." ;;
      "6. COMPARTILH.") echo "             >> BLOQUEIO BUG-32: chave nas DUAS tabelas = entrada de TextAppends morta." ;;
      "7. CICLO")      echo "             >> ler as linhas de erro do log acima antes de qualquer release." ;;
    esac
  done
  echo "             Nada deve ser distribuido/instalado enquanto o veredito for REPROVADO."
  RC=1
fi
linha
exit "$RC"
