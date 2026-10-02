#!/usr/bin/env bash
# =============================================================================
# release-check.sh — checklist automatizado de validacao de release
# -----------------------------------------------------------------------------
# Roda TODOS os passos automatizaveis na ordem certa e no final diz
# APROVADO ou REPROVADO, apontando qual passo falhou.
#
# Uso (da raiz do repo ou de qualquer subpasta):
#     bash tools/release-check.sh                        # FLUXO NORMAL (nao escreve nada)
#     bash tools/release-check.sh --instalar-no-perfil    # MODO EXPLICITO (instala + ciclo)
#
# DEPLOY-2 (01/10/2026) — O DEPLOY E OPT-IN: quem nao pediu, nao instala.
#   O padrao do deploy mora na RAIZ (Directory.Build.props): DeployToBepInEx=false.
#   Todo alvo de deploy dos .csproj (DeployToBepInEx, DeployToScripts) exige
#   Condition="'$(DeployToBepInEx)' == 'true'". Num `dotnet build` comum a propriedade
#   fica VAZIA -> a condicao e FALSA -> o alvo NAO roda: nenhuma DLL chega ao perfil.
#   Isso vale para o build cru, para o `-c Release` e para o passo 3 deste script.
#
# REL-3 (01/10/2026) — HISTORICO. O conserto anterior so mexia no script: compilar com
#   -p:DeployToBepInEx=false sobre uma Condition "'$(DeployToBepInEx)' != 'false'".
#   Como num build comum a propriedade vinha VAZIA, a condicao era VERDADEIRA e o alvo
#   RODAVA: a flag nao desligava nada e o build cru instalava no perfil (foi assim que a
#   DLL das 14:41 chegou la com o jogo aberto). A revisao DEPLOY-1R refutou aquela
#   entrega e DEPLOY-2 fechou o defeito de verdade: (1) opt-in nos .csproj via
#   Directory.Build.props; (2) os dois furaos da guarda (Condition lida como XML, alvos
#   de QUALQUER nome); (3) o alvo DeployToScripts do ReloadProbe, que escrevia no perfil
#   com nome proprio e sem Condition, passou a respeitar o MESMO opt-in. O ciclo em jogo
#   segue no modo explicito --instalar-no-perfil, que agora instala passando
#   -p:DeployToBepInEx=true.
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
#   2. PATCHES    — tools/check_patches.py (trava TRV-1: as 5 regras de robustez dos
#                   patches Harmony, lidas dos .cs SEM compilar — sem parametro
#                   posicional, assinatura por TIPO, Prefix/Postfix em try/catch,
#                   marcador de boot e aplicador gancho a gancho)
#                   ABORTA NA HORA (exit 1): o parametro posicional do Harmony
#                   COMPILA sem um aviso sequer, entao nem o build nem o ciclo
#                   denunciam — foi um `ref __3` no argumento errado que encheu o log
#                   com 112 NullReferenceException por frame e travou uma batalha.
#   3. BUILD      — dotnet build de todos os <Mod>/<Mod>.csproj SEM o opt-in
#                   (0 erros CS; NAO instala no perfil). Antes de buildar, a guarda
#                   tools/check_deploy_optin.py confere que TODO alvo de deploy dos
#                   .csproj escreve no perfil SO com -p:DeployToBepInEx=true.
#   4. CHAVES     — tools/check_fix_keys.py (chave dos textos existe no censo)
#   5. DUPLICADAS — tools/check_dupes.py    (trava INC-1: chave repetida derruba
#                   o mod INTEIRO com TypeInitializationException)
#   6. NOTAS      — tools/check_notas_redundantes.py (nota que repete o texto)
#   7. COMPARTILH.— tools/check_chave_compartilhada.py --estrito  (TRAVA BUG-32:
#                   a MESMA chave em TextFixes E TextAppends = a entrada de
#                   TextAppends nunca roda e a nota nao existe em jogo, em
#                   silencio. As SUSPEITAS de texto compartilhado NESTA MESMA
#                   ferramenta seguem aviso: dependem de decisao humana.)
#   8. CICLO      — SO no modo --instalar-no-perfil: scratch/test-cycle.sh
#                   (abre/fecha o jogo) + analise do LogOutput.log: 0
#                   TypeInitializationException, 0 ArgumentException, 0 '[Error'.
#                   No fluxo normal este passo NAO RODA: ele abre o jogo e so
#                   prova algo com a DLL nova NO PERFIL.
#   9. HUMANO     — lista do que so um humano confere em jogo (nao automatizavel)
#
# O mesmo miolo de repositorio roda no CI (.github/workflows/validate.yml), na
# mesma ordem: 1 segredos, 2 versoes, 3 patches, 4 chaves, 5 duplicadas, 6 notas, 7 chave
# compartilhada --estrito, 8 pacotes, 9 auditoria dos docs.
#
# Notas de projeto:
#   * NAO usa `set -e`: o relatorio final TEM que aparecer mesmo com falha.
#     Por isso os passos 0, 1 e 2 ABORTAM na hora (exit 1); do 3 em diante tudo
#     acumula e chega ao RESUMO FINAL, mesmo reprovado.
#   * Nunca toca Assembly-CSharp.dll; backup de DLL nunca vai para plugins/.
#   * DEPLOY-2: buildar SEM -p:DeployToBepInEx=true NAO instala — o padrao e false
#     (Directory.Build.props) e os alvos exigem "== 'true'". O passo 3 ainda passa
#     -p:DeployToBepInEx=false (cinto e suspensorio) e o UNICO caminho que pede o
#     opt-in e o modo explicito --instalar-no-perfil (que anuncia antes de fazer).
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

# ------------------------------- modo de operacao ----------------------------
# REL-3: por padrao este script NAO ESCREVE NADA no ambiente do dono. O unico
# caminho que instala a DLL no perfil do r2modman (e abre o jogo) e o modo
# explicito abaixo, e ele tem de ser pedido PELO NOME. Nao ha passo numerado do
# fluxo normal que leve a ele.
INSTALAR_NO_PERFIL=0
for arg in "$@"; do
  case "$arg" in
    --instalar-no-perfil) INSTALAR_NO_PERFIL=1 ;;
    --help|-h) sed -n '2,80p' "${BASH_SOURCE[0]}" | sed 's/^#\s\?//'; exit 0 ;;
    *) echo "opcao desconhecida: $arg"
       echo "uso: bash tools/release-check.sh [--instalar-no-perfil]"
       exit 2 ;;
  esac
done

# --------------------------- acumulador de falhas ----------------------------
CHECKS=()   # "STATUS|NOME|DETALHE"
FALHAS=()
passo_ok()       { CHECKS+=("OK|$1|$2"); }
passo_fail()     { CHECKS+=("FALHA|$1|$2"); FALHAS+=("$1"); }
passo_pendente() { CHECKS+=("PENDENTE|$1|$2"); }   # nao rodou: nao reprova, mas nao se disfarca de OK

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
if [ "$INSTALAR_NO_PERFIL" -eq 1 ]; then
  echo " MODO         : --instalar-no-perfil  *** VAI ESCREVER NO PERFIL DO DONO ***"
else
  echo " MODO         : fluxo normal (verificacao SEM escrever no perfil do dono)"
fi
linha

# ------------------------- anuncio do modo explicito -------------------------
# REL-3: o modo que instala DIZ EM VOZ ALTA o que vai fazer, antes de fazer.
if [ "$INSTALAR_NO_PERFIL" -eq 1 ]; then
  echo
  echo "##############################################################################"
  echo "#  MODO EXPLICITO: --instalar-no-perfil"
  echo "#"
  echo "#  ESTE MODO ESCREVE NO AMBIENTE DO DONO. Ele vai:"
  echo "#    1. ENCERRAR o jogo (taskkill \"Stolen Realm.exe\") se estiver aberto;"
  echo "#    2. compilar COM -p:DeployToBepInEx=true (o opt-in que faz os alvos"
  echo "#       DeployToBepInEx (plugins) e DeployToScripts (scripts) COPIAREM para o perfil):"
  echo "#         $(cygpath -u "$PLUGINS_DIR")/<Mod>/"
  echo "#    3. ABRIR o jogo (ciclo) e ler o LogOutput.log."
  echo "#"
  echo "#  O fluxo normal (sem esta opcao) nao faz NADA disso: o passo 3 builda SEM"
  echo "#  o opt-in e o passo 8 nao roda."
  echo "##############################################################################"
  echo
fi

# =============================== PREPARO =====================================
# REL-3: so o modo explicito precisa fechar o jogo — so ele escreve no perfil.
# No fluxo normal o jogo do dono NUNCA e encerrado por este script.
echo
if [ "$INSTALAR_NO_PERFIL" -eq 1 ]; then
  echo "== PREPARO (modo explicito): o jogo sera encerrado para a DLL poder ser copiada =="
  if taskkill /F /IM "Stolen Realm.exe" >/dev/null 2>&1; then
    echo "   instancia anterior do jogo encerrada"
  else
    echo "   nenhuma instancia rodando"
  fi
else
  echo "== PREPARO: dispensado — o fluxo normal NAO instala nada (o jogo pode ficar aberto) =="
fi

# ================================ 0. SEGREDOS ================================
echo
echo "== PASSO 0/9 — SEGREDOS =="
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
# build abaixo e o ciclo (quando o modo explicito instala) testariam codigo novo
# achando que e o velho - e o pacote sairia com versao errada.
echo
echo "== PASSO 1/9 — VERSOES (check_versoes.py: csproj = manifest = Plugin.cs) =="
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

# ================================ 2. PATCHES =================================
# Trava TRV-1 (tools/check_patches.py): as 5 regras de robustez dos patches Harmony lidas dos
# .cs SEM compilar. ABORTA NA HORA (exit 1), como os passos 0 e 1, por um motivo proprio: o
# parametro posicional do Harmony COMPILA sem um aviso sequer (o build abaixo passaria) e o
# ciclo do jogo so veria a consequencia - foi um `ref __3` apontando para o argumento errado
# que encheu o log com 112 NullReferenceException por frame e travou uma batalha. Gancho
# reprovado aqui nao chega a ser instalado no perfil pelo build.
echo
echo "== PASSO 2/9 — PATCHES (trava TRV-1: 5 regras de robustez do Harmony) =="
SAIDA_PATCHES="$($PYTHON tools/check_patches.py 2>&1)"; rc_patches=$?
printf '%s\n' "$SAIDA_PATCHES" | sed 's/^/   /'
if [ "$rc_patches" -eq 0 ]; then
  det_patches=$(printf '%s\n' "$SAIDA_PATCHES" | grep -aoE '[0-9]+ achado\(s\) que REPROVAM \| [0-9]+ aviso\(s\)' | head -1)
  passo_ok "2. PATCHES" "${det_patches:-nenhum achado que reprova}"
elif [ "$rc_patches" -eq 1 ]; then
  echo
  echo "  [FALHA] 2. patch reprovado pela TRV-1 — release travada"
  echo "   >>> BLOQUEIO DE RELEASE (TRV-1) <<<"
  echo "   Os achados acima apontam arquivo:linha. Um parametro posicional do Harmony"
  echo "   (`ref __3`) aponta para o argumento ERRADO quando a assinatura do jogo muda, e o"
  echo "   defeito COMPILA: so aparece em jogo, como NullReferenceException em serie (112 por"
  echo "   frame no caso que originou esta trava). Sem o marcador de boot '... carregado.' o"
  echo "   teste de ciclo nao tem como saber que o plugin subiu — o silencio parece sucesso,"
  echo "   e patch sem try/catch inunda o log a cada quadro."
  echo "   Correcao: use o NOME do parametro, declare a assinatura por TIPO (typeof/nameof),"
  echo "   mantenha Prefix/Postfix em try/catch e logue a linha de carregamento no Plugin.cs."
  echo "   Nada foi buildado e nada foi instalado no perfil: conserte e rode de novo."
  exit 1
else
  passo_fail "2. PATCHES" "check_patches.py NAO RODOU (exit $rc_patches) — trava TRV-1 nao verificada"
fi

# ================================= 3. BUILD ==================================
# DEPLOY-2: o build DESTE passo nao escreve no perfil do dono. O deploy e OPT-IN
# (Directory.Build.props define DeployToBepInEx=false; cada alvo de deploy exige
# Condition="'$(DeployToBepInEx)' == 'true'"). Aqui buildamos SEM o opt-in e ainda
# passamos -p:DeployToBepInEx=false por cinto e suspensorio. Antes de buildar, a
# guarda tools/check_deploy_optin.py le os .csproj como XML e reprova qualquer alvo
# que escreva no perfil sem o opt-in — de QUALQUER nome e em QUALQUER numero de
# linhas. Um projeto que ignore o opt-in nao e buildado. So o modo explicito
# --instalar-no-perfil pede -p:DeployToBepInEx=true — e isso esta anunciado la em cima.
echo
echo "== PASSO 3/9 — BUILD (0 erros CS; SEM escrever no perfil) =="

mapfile -t PROJETOS < <(find . -maxdepth 2 -name '*.csproj' \
                          -not -path '*/bin/*' -not -path '*/obj/*' \
                        | sed 's|^\./||' | sort)
if [ "${#PROJETOS[@]}" -eq 0 ]; then
  passo_fail "3. BUILD" "nenhum .csproj encontrado"
  echo "   ERRO: nenhum .csproj encontrado na raiz do repo"
else
  echo "   projetos descobertos: ${#PROJETOS[@]} -> ${PROJETOS[*]}"

  # DEPLOY-2: o padrao do opt-in mora na RAIZ (Directory.Build.props). Sem o arquivo a
  # propriedade ficaria vazia e o alvo (Condition "== 'true'") nao rodaria de qualquer
  # forma, mas o contrato tem de estar DECLARADO — a ausencia e reportada, nao silenciada.
  if [ -f Directory.Build.props ]; then
    echo "   padrao do opt-in: Directory.Build.props presente (DeployToBepInEx=false)"
  else
    echo "   AVISO: Directory.Build.props ausente na raiz — o padrao do opt-in nao esta declarado"
  fi

  # DEPLOY-2: o opt-in e o que instala. No modo explicito ele e pedido pelo nome.
  FLAG_DEPLOY="-p:DeployToBepInEx=false"
  if [ "$INSTALAR_NO_PERFIL" -eq 1 ]; then
    FLAG_DEPLOY="-p:DeployToBepInEx=true"
    echo "   deploy no perfil: SIM — modo --instalar-no-perfil (opt-in -p:DeployToBepInEx=true)"
  else
    echo "   deploy no perfil: NAO — fluxo normal (opt-in ausente; -p:DeployToBepInEx=false)"
  fi

  # A GUARDA (DEPLOY-2): nenhum alvo de deploy pode escrever no perfil sem o opt-in.
  # Le os .csproj como XML DE VERDADE, nao a primeira linha da tag:
  #   - furo A fechado: tag multi-linha e Condition em outra linha sao lidas certo;
  #   - furo B fechado: vale para alvos de QUALQUER nome (DeployToBepInEx,
  #     DeployToScripts, ...), desde que escrevam no perfil.
  SAIDA_DEPLOY="$($PYTHON tools/check_deploy_optin.py 2>&1)"; rc_deploy=$?
  printf '%s\n' "$SAIDA_DEPLOY" | sed 's/^/   /'

  if [ "$rc_deploy" -ne 0 ]; then
    passo_fail "3. BUILD" "alvo de deploy SEM o opt-in explicito — NADA foi buildado"
    echo "   [FALHA] a guarda achou alvo(s) que escrevem no perfil do r2modman e nao"
    echo "   exigem o opt-in (Condition com DeployToBepInEx == 'true'). Com a Condition"
    echo "   antiga (\"!= 'false'\") a propriedade vinha VAZIA num build comum, a condicao"
    echo "   era VERDADEIRA e o build cru COPIAVA a DLL para o perfil (REL-3/DEPLOY-1R)."
    echo "   Nada foi buildado: conserte o .csproj e rode de novo."
  else
    ERROS_TOTAL=0
    PROJS_FALHOS=0
    DETALHES_BUILD=""

    # DEPLOY-2: em vez de AFIRMAR que o perfil ficou intacto, MEDE. Fotografa o
    # perfil antes do build e confere depois: se um byte mudar num build SEM opt-in,
    # o passo REPROVA — a mensagem para de poder mentir.
    SNAP_PERFIL_ANTES=""
    if [ "$INSTALAR_NO_PERFIL" -eq 0 ]; then
      SNAP_PERFIL_ANTES="$(find "$(cygpath -u "$PERFIL")" -type f -printf '%P|%s|%T@\n' 2>/dev/null | sort)"
    fi

    for p in "${PROJETOS[@]}"; do
      nome="$(basename "$p" .csproj)"
      out="$TMPD/build-$nome.log"
      # shellcheck disable=SC2086  # FLAG_DEPLOY e uma lista de flags, nao um caminho
      ( LC_ALL=C dotnet build "$p" $FLAG_DEPLOY --nologo -v q -clp:ErrorsOnly >"$out" 2>&1 )
      rc=$?
      ncs=$(grep -ac 'error CS' "$out" || true); ncs=${ncs:-0}
      if [ "$ncs" -gt 0 ] || [ "$rc" -ne 0 ]; then
        printf '   [FALHA] %-18s %s erro(s) CS (exit %s)\n' "$nome" "$ncs" "$rc"
        grep -aE 'error [A-Z]+[0-9]+' "$out" | head -10 | sed 's/^/           /'
        PROJS_FALHOS=$((PROJS_FALHOS + 1))
      elif [ "$INSTALAR_NO_PERFIL" -eq 1 ]; then
        printf '   [ ok  ] %-18s 0 erro(s) CS (exit 0, opt-in: DLL COPIADA para o perfil)\n' "$nome"
      else
        printf '   [ ok  ] %-18s 0 erro(s) CS (exit 0, sem opt-in: nenhum alvo de deploy roda)\n' "$nome"
      fi
      ERROS_TOTAL=$((ERROS_TOTAL + ncs))
      DETALHES_BUILD="$DETALHES_BUILD $nome=$ncs"
    done

    # Medicao pos-build: o perfil tinha de ficar IDENTICO num build SEM opt-in.
    PERFIL_MUDOU=""
    if [ "$INSTALAR_NO_PERFIL" -eq 0 ]; then
      SNAP_PERFIL_DEPOIS="$(find "$(cygpath -u "$PERFIL")" -type f -printf '%P|%s|%T@\n' 2>/dev/null | sort)"
      if [ "$SNAP_PERFIL_DEPOIS" != "$SNAP_PERFIL_ANTES" ]; then
        PERFIL_MUDOU="sim"
        echo "   [FALHA] o perfil do dono MUDOU durante um build SEM opt-in:"
        diff <(printf '%s\n' "$SNAP_PERFIL_ANTES") <(printf '%s\n' "$SNAP_PERFIL_DEPOIS") \
          | sed 's/^/             /'
      fi
    fi

    if [ -n "$PERFIL_MUDOU" ]; then
      passo_fail "3. BUILD" "build sem opt-in ESCREVEU no perfil do dono — investigue antes de seguir"
    elif [ "$PROJS_FALHOS" -eq 0 ]; then
      if [ "$INSTALAR_NO_PERFIL" -eq 1 ]; then
        passo_ok "3. BUILD" "${#PROJETOS[@]} projetos, $ERROS_TOTAL erros CS (opt-in: DLLs instaladas no perfil)"
      else
        passo_ok "3. BUILD" "${#PROJETOS[@]} projetos, $ERROS_TOTAL erros CS (perfil medido intacto; nenhum alvo de deploy rodou)"
      fi
    else
      passo_fail "3. BUILD" "$PROJS_FALHOS/${#PROJETOS[@]} projeto(s) com falha, $ERROS_TOTAL erros CS"
    fi
  fi
fi

# =============================== 4. CHAVES ===================================
echo
echo "== PASSO 4/9 — CHAVES (check_fix_keys.py: chave de texto existe no censo?) =="
SAIDA_CHAVES="$($PYTHON tools/check_fix_keys.py 2>&1)"; rc=$?
printf '%s\n' "$SAIDA_CHAVES" | sed 's/^/   /'
if [ "$rc" -ne 0 ]; then
  passo_fail "4. CHAVES" "check_fix_keys.py NAO RODOU (exit $rc)"
else
  N_EXTRA=$(printf '%s\n' "$SAIDA_CHAVES" | grep -aoE 'chaves extraidas: [0-9]+' | grep -oE '[0-9]+' | head -1)
  N_CENSO=$(printf '%s\n' "$SAIDA_CHAVES" | grep -aoE 'no censo *: [0-9]+' | grep -oE '[0-9]+' | head -1)
  N_FORA=$(printf '%s\n' "$SAIDA_CHAVES" | grep -aoE 'fora do censo: [0-9]+' | grep -oE '[0-9]+' | head -1)
  N_EXTRA=${N_EXTRA:-?}; N_CENSO=${N_CENSO:-?}; N_FORA=${N_FORA:-0}
  if [ "$N_FORA" != "0" ] && [ "$N_FORA" != "?" ]; then
    echo "   AVISO (nao reprova): $N_FORA chave(s) fora do censo — pode ser texto de UI/loading"
    echo "   ainda nao coberto pelo censo (ver docs/cobertura/README.md)."
  fi
  passo_ok "4. CHAVES" "$N_EXTRA chaves extraidas, $N_CENSO no censo, $N_FORA fora"
fi

# ============================= 5. DUPLICADAS =================================
echo
echo "== PASSO 5/9 — DUPLICADAS (trava INC-1: chave repetida = jogo sem o mod) =="
SAIDA_DUP="$($PYTHON tools/check_dupes.py 2>&1)"; rc=$?
printf '%s\n' "$SAIDA_DUP" | sed 's/^/   /'
if [ "$rc" -eq 1 ]; then
  passo_fail "5. DUPLICADAS" "chave duplicada — INC-1, NAO INSTALAR NADA"
  echo
  echo "   >>> BLOQUEIO DE RELEASE (INC-1) <<<"
  echo "   Chave repetida em Dictionary<string,string> = ArgumentException no"
  echo "   construtor estatico do LocalizePatch = TypeInitializationException e"
  echo "   NENHUMA tabela do mod carrega. Regra: UMA entrada por TEXTO, nunca por skill."
elif [ "$rc" -ne 0 ]; then
  passo_fail "5. DUPLICADAS" "check_dupes.py NAO RODOU (exit $rc) — trava INC-1 nao verificada"
else
  det_dup=$(printf '%s\n' "$SAIDA_DUP" | grep -aoE 'TextFixes[[:space:]]+[0-9]+ entradas \| duplicadas: [a-z]+' | head -1)
  passo_ok "5. DUPLICADAS" "${det_dup:-nenhuma duplicada}"
fi

# ======================= 6. NOTAS REDUNDANTES ================================
echo
echo "== PASSO 6/9 — NOTAS REDUNDANTES (a nota repete o texto que ja estava la?) =="
SAIDA_NOTAS="$($PYTHON tools/check_notas_redundantes.py 2>&1)"; rc=$?
printf '%s
' "$SAIDA_NOTAS" | sed 's/^/   /'
if [ "$rc" -eq 1 ]; then
  passo_fail "6. NOTAS" "nota redundante/duplicada — o jogador le a mesma frase duas vezes"
  echo
  echo "   >>> REVISAR ANTES DE PUBLICAR <<<"
  echo "   Uma nota existe para dizer o que o texto NAO diz. Familias: nota == chave (a frase"
  echo "   aparece DUPLICADA na tela), nota contida na chave, nota que ecoa o texto, e nota de"
  echo "   Armor onde Armor e FONTE de dano e nao mitigacao. As regras que impedem o ultimo caso"
  echo "   estao no codigo (ArmorValueSourceRegex) - se aparecer caso aqui, a regra falhou."
  echo "   Relatorio: docs/cobertura/revisao/RV-15-notas-redundantes.md"
elif [ "$rc" -ne 0 ]; then
  passo_fail "6. NOTAS" "check_notas_redundantes.py NAO RODOU (exit $rc) — nao verificada"
else
  det_notas=$(printf '%s
' "$SAIDA_NOTAS" | grep -aoE 'notas analisadas [.]+ [0-9]+' | head -1)
  passo_ok "6. NOTAS" "${det_notas:-0 casos}"
fi

# ======================= 7. CHAVE COMPARTILHADA ==============================
echo
echo "== PASSO 7/9 — CHAVE COMPARTILHADA (trava BUG-32: chave nas DUAS tabelas) =="
SAIDA_COMP="$($PYTHON tools/check_chave_compartilhada.py --estrito 2>&1)"; rc_comp=$?
printf '%s\n' "$SAIDA_COMP" | sed 's/^/   /'
if [ "$rc_comp" -eq 1 ]; then
  N_AMBAS=$(printf '%s\n' "$SAIDA_COMP" | grep -aoE 'chave nas DUAS tabelas \(TextFixes\+TextAppends\) [.]+ [0-9]+' | grep -oE '[0-9]+$' | head -1)
  passo_fail "7. COMPARTILH." "${N_AMBAS:-1} chave(s) nas DUAS tabelas — BUG-32, release travada"
  echo
  echo "   >>> BLOQUEIO DE RELEASE (BUG-32) <<<"
  echo "   A MESMA chave existe em TextFixes e em TextAppends. O lookup e if/else if"
  echo "   na mesma chave, entao a entrada de TextAppends NUNCA roda: a nota nao"
  echo "   existe em jogo, em silencio, sem erro nenhum no log. NAO e opiniao."
  echo "   Correcao: UMA entrada por texto — fundir o valor da TextAppends no valor"
  echo "   da TextFixes (a que executa hoje) e apagar a duplicada."
elif [ "$rc_comp" -ne 0 ]; then
  passo_fail "7. COMPARTILH." "check_chave_compartilhada.py NAO RODOU (exit $rc_comp) — trava BUG-32 nao verificada"
else
  N_SUSP=$(printf '%s\n' "$SAIDA_COMP" | grep -aoE 'SUSPEITAS[^:]*: [0-9]+' | grep -oE '[0-9]+' | head -1)
  N_SUSP=${N_SUSP:-0}
  if [ "$N_SUSP" != "0" ]; then
    echo
    echo "   AVISO (nao reprova): $N_SUSP suspeita(s) de chave compartilhada - a nota pode"
    echo "   estar mentindo para outro dono do texto. A decisao e humana (mecanica citada)."
    echo "   Revisar: docs/cobertura/revisao/BUG-32-chaves-compartilhadas.md"
  fi
  passo_ok "7. COMPARTILH." "0 chave nas duas tabelas; $N_SUSP suspeita(s) (aviso humano)"
fi

# ============================== 8. CICLO =====================================
# REL-3: este passo ABRE o jogo do dono e so prova alguma coisa sobre ESTE codigo
# com a DLL recem-buildada NO PERFIL. As duas coisas sao efeito colateral no
# ambiente dele — por isso o ciclo NAO e um passo do fluxo normal: ele roda
# apenas no modo explicito --instalar-no-perfil, que instalou a DLL no passo 3 e
# anunciou isso em voz alta antes de comecar.
echo
echo "== PASSO 8/9 — CICLO DO JOGO + ANALISE DO LOG =="
if [ "$INSTALAR_NO_PERFIL" -eq 0 ]; then
  echo "   NAO RODA no fluxo normal. O ciclo abre o jogo e, para provar algo sobre este"
  echo "   codigo, exige a DLL recem-buildada NO PERFIL — as duas coisas agem no ambiente"
  echo "   do dono. O fluxo normal nao fez nem uma nem outra (o passo 3 nao instalou)."
  echo "   Para instalar a DLL no perfil e rodar o ciclo de verdade, de proposito:"
  echo "     bash tools/release-check.sh --instalar-no-perfil"
  passo_pendente "8. CICLO" "NAO RODOU no fluxo normal (abre o jogo e exige a DLL no perfil) — use --instalar-no-perfil"
else
echo "   $ bash scratch/test-cycle.sh $SEGUNDOS_CICLO \"$PADRAO_CICLO\""
SAIDA_CICLO="$(bash scratch/test-cycle.sh "$SEGUNDOS_CICLO" "$PADRAO_CICLO" 2>&1)"; rc_ciclo=$?
printf '%s\n' "$SAIDA_CICLO" | sed 's/^/   | /'

# --- analise do log ---------------------------------------------------------
if [ ! -f "$LOG" ]; then
  echo "   ERRO: log nao existe: $LOG"
  passo_fail "8. CICLO" "sem log — o jogo nao chegou a subir"
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
    passo_ok "8. CICLO" "$N_CARR plugins ok, 0 TIE, 0 ArgException, 0 [Error"
  else
    passo_fail "8. CICLO" "TIE=$N_TIE ArgEx=$N_ARG [Error=$N_ERR plugins=$N_CARR BT=$BT_OK (exit test-cycle=$rc_ciclo)"
    [ "$N_TIE" -gt 0 ] && grep -a -m3 -B1 'TypeInitializationException' "$LOG" | sed 's/^/        /'
    [ "$N_ERR" -gt 0 ] && grep -a -m3 '^\[Error' "$LOG" | sed 's/^/        /'
  fi
fi

# garante que o jogo ficou fechado — so importa se ESTE modo abriu o jogo
taskkill /F /IM "Stolen Realm.exe" >/dev/null 2>&1 || true
fi

# ============================== 9. HUMANO ====================================
echo
echo "== PASSO 9/9 — PASSO HUMANO (NAO automatizavel: exige jogo aberto e olho humano) =="
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
  elif [ "$st" = "PENDENTE" ]; then
    printf '  [PEND.]  %-14s %s\n' "$nome" "$det"
  else
    printf '  [FALHA]  %-14s %s\n' "$nome" "$det"
  fi
done
printf '  [HUMANO] %-14s %s\n' "9. HUMANO" "conferencia visual em jogo (ver itens 5.1-5.5 acima) — sempre pendente"
echo
if [ "${#FALHAS[@]}" -eq 0 ]; then
  if [ "$INSTALAR_NO_PERFIL" -eq 1 ]; then
    echo "  CONCLUSAO: APROVADO na automacao (segredos, versoes, patches, build, chaves, duplicadas, notas, chave compartilhada, ciclo em jogo)"
    echo "             MODO --instalar-no-perfil: as DLLs FORAM COPIADAS para o perfil do dono"
    echo "             (opt-in -p:DeployToBepInEx=true, pedido pelo nome) e o jogo foi aberto e fechado."
  else
    echo "  CONCLUSAO: APROVADO na automacao (segredos, versoes, patches, build, chaves, duplicadas, notas, chave compartilhada)"
    echo "             O perfil do dono NAO foi tocado: o passo 3 rodou SEM o opt-in"
    echo "             (-p:DeployToBepInEx=false), a guarda confirmou que todo alvo de deploy"
    echo "             exige -p:DeployToBepInEx=true e o perfil foi MEDIDO antes/depois (identico)."
    echo "             8. CICLO NAO RODOU (nao reprova, mas nao conta como aprovado): ele abre o"
    echo "             jogo e exige a DLL nova NO PERFIL. Para essa prova: --instalar-no-perfil."
  fi
  echo "             LEMBRETE: o release so esta COMPLETO depois dos passos humanos 5.1-5.5."
  RC=0
else
  echo "  CONCLUSAO: REPROVADO — passo(s) com falha: ${FALHAS[*]}"
  for f in "${FALHAS[@]}"; do
    case "$f" in
      "2. PATCHES")    echo "             >> BLOQUEIO TRV-1: um gancho aceita argumento por POSICAO — corrija antes de instalar." ;;
      "3. BUILD")      if [ "$INSTALAR_NO_PERFIL" -eq 1 ]; then
                         echo "             >> build quebrou no modo explicito: confira em plugins/ qual DLL ficou velha."
                       else
                         echo "             >> build quebrou: NADA foi instalado no perfil (o fluxo normal nao instala)."
                       fi ;;
      "4. CHAVES")     echo "             >> revisar a saida do check_fix_keys.py acima (chave fora do censo falha em silencio)." ;;
      "5. DUPLICADAS") echo "             >> BLOQUEIO INC-1: nao instale nem distribua nada ate as duplicadas sumirem." ;;
      "7. COMPARTILH.") echo "             >> BLOQUEIO BUG-32: chave nas DUAS tabelas = entrada de TextAppends morta." ;;
      "8. CICLO")      echo "             >> ler as linhas de erro do log acima antes de qualquer release." ;;
    esac
  done
  echo "             Nada deve ser distribuido/instalado enquanto o veredito for REPROVADO."
  RC=1
fi
linha
exit "$RC"
