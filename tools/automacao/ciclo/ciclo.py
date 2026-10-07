#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIC-1 - orquestrador do ciclo alteracao -> validacao -> fila -> revalidacao.

Reusa a bancada offline AUT-3 como MOTOR de validacao (nao reimplementa build,
suite nem conferidores) e acrescenta o que faltava para fechar o ciclo:

  * IDENTIDADE de fonte real (sha256 dos bytes atuais do repo) e das DLLs; a
    identidade so e SUFICIENTE com fonte_sha E dll_sha (mesmo criterio da
    decisao.py) -- sem isso nada vira OK;
  * RESULTADO VALIDO SO PARA OS BYTES ATUAIS -- o REUSO de um AUT-3 confronta
    o SNAPSHOT de fonte que ele proprio carrega (`guarda_repo.sha_antes` /
    `estados_separados.fonte`) contra os bytes de agora; snapshot ausente ou
    divergente => INCOMPLETO/nova rodada, nunca falso verde; o reuso tambem
    confronta `ciclo_identidade.dll_sha`, gravado SOMENTE na execucao original.
    AUT-3 legado sem esse vinculo exige nova rodada; nunca recebe hash retroativo.
    Mudanca de fonte ou DLL DURANTE a rodada invalida a captura;
  * FILA DE CORRECAO DECLARATIVA para o supervisor/agentes: cada falha vira um
    item com criterio, mod, CAUSA (ou `causa_desconhecida` explicito), evidencia
    e tarefa de origem; NAO ha execucao automatica de comando de correcao;
  * LIMITE DE TENTATIVAS e deteccao de SEM PROGRESSO (mesma fonte + mesmas
    falhas) -> ESCALADO com motivo, apontando o supervisor TECNICO (nunca o dono);
  * ESTADO/EXIT/RESUMO/FILA incorporam as falhas_automaticas da decisao.py, SEM
    APROVADO paralelo a falha automatica, e sem esconder erro de consolidacao.
  * integracao OPCIONAL com decisao.py (CIC-2): usa quando existir, opera com
    resultado estruturado minimo quando ainda nao houver modulo. Nao espera,
    nao faz polling de outro agente.

Uso tipico (o supervisor chama UMA vez por rodada; a correcao e ato humano/agente
externo e exige NOVA rodada):

    python tools/automacao/ciclo/ciclo.py --repo <repo> --trabalho <scratch> \\
        --resultado <saida.json>

Reusa resultado AUT-3 ja gerado (sem copia, sem build) -- modo barato para
revalidar a regressao afetada; o snapshot do AUT-3 tem de conferir com os bytes
atuais ou a rodada sai INCOMPLETO:

    python tools/automacao/ciclo/ciclo.py --repo <repo> --resultado <saida.json> \\
        --aut3-resultado <AUT-3-resultado.json>

Verifica se um resultado guardado ainda corresponde aos bytes atuais:

    python tools/automacao/ciclo/ciclo.py --repo <repo> --verificar <saida.json>

Exit: 0 = APROVADO_OFFLINE · 1 = REPROVADO/ESCALADO · 2 = INCOMPLETO ·
      3 = INVALIDADO_POR_MUDANCA_DE_FONTE.  So a stdlib. NUNCA instala, abre o
jogo, carrega save, commita, faz push ou publica.
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
# tools/automacao/ciclo -> raiz do repositorio
RAIZ_PADRAO = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
BANCADA_REL = os.path.join("tools", "automacao", "offline", "bancada_aut3.py")
PY = sys.executable

ESQUEMA = "CIC-1/1"
TAREFA = "t_2c3e8182"
LIMITE_PADRAO = 5

# Fonte de verdade = arvore de trabalho (tracked + untracked) MENOS o que NAO e
# fonte nem prova: area de trabalho externa e pacotes gerados.
EXCLUIDOS_FONTE = ("scratch/", "dist/")
# Outputs do PROPRIO runner AUT-3 (mudam durante a rodada e sao excluidos do
# guarda do AUT-3) e o proprio doc desta entrega.
EXCLUIDOS_EXTRA = (
    "docs/automacao/AUT-3-resultado.json",
    "docs/automacao/AUT-3-resumo.md",
)
# Universo do SNAPSHOT AUT-3: mesma lista do guarda da bancada (tracked +
# untracked, menos scratch/ e os outputs do runner) + dist/ (artefato de build
# que a copia isolada nao carrega e cuja ausencia nao e divergencia de fonte).
UNIVERSO_SNAPSHOT = EXCLUIDOS_FONTE + EXCLUIDOS_EXTRA

OK = "OK"
REPROVADO = "REPROVADO"
NAO_EXERCITADO = "NAO_EXERCITADO"
INDETERMINADO = "INDETERMINADO"

ESTADO_APROVADO = "APROVADO_OFFLINE"
ESTADO_REGRESSAO = "APROVADO_REGRESSAO"
ESTADO_REPROVADO = "REPROVADO"
ESTADO_ESCALADO = "ESCALADO"
ESTADO_INCOMPLETO = "INCOMPLETO"
ESTADO_INVALIDADO = "INVALIDADO_POR_MUDANCA_DE_FONTE"

DESTINO_SUPERVISOR = "supervisor"
DESTINO_CICLO = "ciclo"

# AUT-3 -> mapa de estado do contrato do ciclo.
_MAPA_AUT3 = {"OK": OK, "REPROVOU": REPROVADO, "NAO_EXERCITADO": NAO_EXERCITADO,
              "REPROVADO": REPROVADO}

MODS = ["BetterCombatText", "BetterFont", "BetterStats", "BetterTooltips",
        "RoguelikeDebugger", "RoguelikeSkillTreeVisualizer"]


# ==========================================================================
# infraestrutura minima (stdlib) -- hash, tempo, subprocesso
# ==========================================================================

def agora():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def sha256_bytes(dados):
    return hashlib.sha256(dados).hexdigest()


def sha256_file(caminho):
    if not caminho or not os.path.isfile(caminho):
        return None
    h = hashlib.sha256()
    try:
        with open(caminho, "rb") as fh:
            for bloco in iter(lambda: fh.read(1 << 20), b""):
                h.update(bloco)
    except OSError:
        return None
    return h.hexdigest()


def sha256_mapa(mapa):
    """sha256 canonico de um {chave: sha256} (ordem estavel, separador fixo)."""
    itens = "\n".join("%s\t%s" % (k, (mapa.get(k) or "")) for k in sorted(mapa or {}))
    return sha256_bytes(itens.encode("utf-8"))


def area_trabalho():
    """Base segura para a copia isolada -- Hermes scratch, nunca a Temp do Windows."""
    candidatos = [os.environ.get("HERMES_KANBAN_WORKSPACE"), os.environ.get("BH_AGENT_WORKSPACE"), os.environ.get("TMPDIR")]
    local = os.environ.get("LOCALAPPDATA")
    if local:
        candidatos.append(os.path.join(local, "hermes", "cache", "scratch"))
    for cand in candidatos:
        if cand and os.path.isdir(cand):
            return cand
    base = candidatos[-1] if candidatos[-1] else os.path.abspath(".")
    os.makedirs(base, exist_ok=True)
    return base


def _sanitiza(texto):
    """Reusa o sanitizador VETADO da bancada offline antes de serializar captura.

    Nunca gravar prefixo/valor de credencial no resultado (mesma regra do AUT-3).
    """
    if not texto:
        return texto or ""
    try:
        offline = os.path.join(os.path.dirname(AQUI), "offline")
        if offline not in sys.path:
            sys.path.insert(0, offline)
        import aut3_lib  # noqa: E402
        return aut3_lib.sanitiza(texto)
    except Exception:
        return texto


def run_cmd(argv, cwd=None, timeout=1800, env=None):
    """Roda um comando e devolve o resultado CRU (sem julgar)."""
    import time as _t
    ambiente = dict(os.environ)
    ambiente.setdefault("PYTHONIOENCODING", "utf-8")
    ambiente.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    if env:
        ambiente.update(env)
    inicio = _t.monotonic()
    try:
        proc = subprocess.run(argv, cwd=cwd, env=ambiente, timeout=timeout,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True, encoding="utf-8", errors="replace")
        return dict(comando=list(argv), cwd=cwd, exit_code=proc.returncode,
                    segundos=round(_t.monotonic() - inicio, 3), timeout=False,
                    erro_lancamento=None, stdout=proc.stdout or "", stderr=proc.stderr or "")
    except subprocess.TimeoutExpired:
        return dict(comando=list(argv), cwd=cwd, exit_code=None,
                    segundos=round(_t.monotonic() - inicio, 3), timeout=True,
                    erro_lancamento="timeout apos %ss" % timeout, stdout="", stderr="")
    except OSError as erro:
        return dict(comando=list(argv), cwd=cwd, exit_code=None,
                    segundos=round(_t.monotonic() - inicio, 3), timeout=False,
                    erro_lancamento="%s: %s" % (type(erro).__name__, erro), stdout="", stderr="")


# ==========================================================================
# identidade de fonte / DLL -- "resultado valido apenas bytes atuais"
# ==========================================================================

def lista_arquivos_repo(repo, excluidos=EXCLUIDOS_FONTE):
    """Arquivos tracked + untracked recursivos (como o guarda do AUT-3).

    FAIL-CLOSED: se o git nao responder, levanta -- sem lista nao ha identidade,
    e sem identidade nada pode ser aprovado.
    """
    r1 = subprocess.run(["git", "ls-files", "-z"], cwd=repo,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    r2 = subprocess.run(["git", "ls-files", "-z", "--others", "--exclude-standard"], cwd=repo,
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if r1.returncode != 0 or r2.returncode != 0:
        raise RuntimeError("git ls-files indisponivel em %s (exit %s/%s)"
                           % (repo, r1.returncode, r2.returncode))
    rels = set()
    for r in (r1, r2):
        rels |= {p for p in r.stdout.decode("utf-8", "replace").split("\0") if p}
    return sorted(p for p in rels if not _excluido(p, excluidos))


def _excluido(rel, excluidos):
    rel = (rel or "").replace("\\", "/")
    return any(rel == e or rel.startswith(e) for e in (excluidos or ()))


def inventario_fonte(repo, excluidos=EXCLUIDOS_FONTE + EXCLUIDOS_EXTRA):
    """{rel: sha256} da fonte atual. Fail-closed se o git nao responder."""
    return {rel: sha256_file(os.path.join(repo, rel)) for rel in lista_arquivos_repo(repo, excluidos)}


def identidade(repo, excluidos=EXCLUIDOS_FONTE + EXCLUIDOS_EXTRA):
    """dict de identidade do contrato: fonte_sha + dll_sha (+ detalhe rastreavel)."""
    inv = inventario_fonte(repo, excluidos)
    fonte_sha = sha256_mapa(inv)
    dlls = {}
    for mod in MODS:
        rel = "%s/bin/Release/netstandard2.1/%s.dll" % (mod, mod)
        h = sha256_file(os.path.join(repo, rel))
        if h:
            dlls[mod] = h
    return {
        "fonte_sha": fonte_sha,
        "fonte_arquivos": len(inv),
        "dll_sha": sha256_mapa(dlls) if dlls else None,
        "dlls": {m: h[:12] for m, h in dlls.items()},
    }


def identidade_suficiente(ident):
    """Identidade so e suficiente com fonte_sha E dll_sha -- igual a decisao.py.

    Sem qualquer das duas nao ha como amarrar o resultado aos bytes/DLL atuais:
    NUNCA OK. (Antes deste conserto o ciclo aprovava so com fonte_sha, enquanto a
    decisao.py reprovava -- APROVADO paralelo a falha automatica.)
    """
    if not isinstance(ident, dict):
        return False
    return bool(ident.get("fonte_sha")) and bool(ident.get("dll_sha"))


# ==========================================================================
# snapshot de fonte do AUT-3 -- "reuso NAO assina log velho com fonte nova"
# ==========================================================================

def snapshot_fonte(repo):
    """{rel: sha12} do universo de fonte do AUT-3 (o que o guarda hasheia)."""
    inv = inventario_fonte(repo, UNIVERSO_SNAPSHOT)
    return {rel: (sha or "")[:12] for rel, sha in inv.items()}


def snapshot_aut3(aut3):
    """{rel: sha} que o AUT-3 REGISTROU como fonte relevante.

    Fonte: `guarda_repo.sha_antes` (snapshot do guarda) e, por reforco,
    `estados_separados.fonte` (fonte relevante declarada). Vazio/ausente =>
    snapshot insuficiente.
    """
    snap = {}
    gr = (aut3 or {}).get("guarda_repo") or {}
    for k, v in (gr.get("sha_antes") or {}).items():
        if isinstance(v, str) and v.strip():
            snap[str(k)] = v.strip()
    for k, v in (((aut3 or {}).get("estados_separados") or {}).get("fonte") or {}).items():
        if isinstance(v, str) and v.strip():
            snap.setdefault(str(k), v.strip())
    return snap


def confrontar_snapshot(aut3, repo):
    """O snapshot do AUT-3 corresponde aos bytes ATUAIS do repo?

    Devolve (ok, motivo, detalhe). Ausencia/insuficiencia OU divergencia
    (alterado/removido/criado) => False. Nunca deixar um resultado antigo valer
    para uma fonte que ja mudou.
    """
    bruto = snapshot_aut3(aut3)
    snap = {k: v for k, v in bruto.items() if not _excluido(k, UNIVERSO_SNAPSHOT)}
    if not snap:
        return False, ("AUT-3 sem snapshot de fonte utilizavel (guarda_repo.sha_antes/"
                       "estados_separados.fonte vazios): resultado NAO prova os bytes atuais; "
                       "nova rodada necessaria"), {"motivo": "snapshot_ausente"}
    atual = inventario_fonte(repo, UNIVERSO_SNAPSHOT)
    if not atual:
        return False, "universo da fonte atual vazio: impossivel confrontar o snapshot", {}
    alt, rem = [], []
    for rel, esperado in snap.items():
        valor = atual.get(rel)
        if valor is None:
            rem.append(rel)
        elif (valor or "")[:len(esperado)] != esperado:
            alt.append(rel)
    cri = sorted(rel for rel in atual if rel not in snap)
    det = dict(n_snapshot=len(snap), n_atual=len(atual),
               alterados=sorted(alt)[:20], removidos=sorted(rem)[:20], criados=cri[:20],
               alterados_total=len(alt), removidos_total=len(rem), criados_total=len(cri))
    if alt or rem or cri:
        return False, ("snapshot do AUT-3 diverge dos bytes atuais: %d alterado(s), %d removido(s), "
                       "%d criado(s) (snapshot=%d, atual=%d); resultado NAO prova a fonte atual, "
                       "nova rodada necessaria"
                       % (len(alt), len(rem), len(cri), len(snap), len(atual))), det
    return True, "", det


# ==========================================================================
# copia isolada + execucao REAL da bancada AUT-3
# ==========================================================================

# Pesado / derivado / do dono: NAO entra na copia. .git e bin/ ENTRAM -- .git
# porque o guarda do AUT-3 usa git ls-files (sem .git o guarda falha fechado) e
# bin/ porque a prova fonte->DLL compara a DLL do sandbox com a DLL da copia.
IGNORAR_COPIA = ("scratch", "obj", "__pycache__", ".vs", ".git-rewrite")


def _forcar_remocao(func, caminho, exc_info):
    """Torna o arquivo gravavel e tenta de novo (objetos .git sao read-only no Windows)."""
    try:
        os.chmod(caminho, 0o777)
        func(caminho)
    except OSError:
        pass


def _remover_arvore(caminho):
    if sys.version_info >= (3, 12):
        shutil.rmtree(caminho, onexc=_forcar_remocao)
    else:
        shutil.rmtree(caminho, onerror=_forcar_remocao)


def copiar_repo(origem, destino):
    origem = os.path.realpath(origem)
    destino = os.path.realpath(destino)
    if os.path.commonpath([origem, destino]) in (origem, destino):
        raise OSError("copia deve ser externa e disjunta da origem")
    if os.path.isdir(destino):
        _remover_arvore(destino)

    def ignorar(dirpath, nomes):
        return [n for n in nomes if n in IGNORAR_COPIA]

    shutil.copytree(origem, destino, ignore=ignorar, symlinks=False)
    return destino


def rodar_aut3(copia, ancora, trabalho, jogo=True, sem_build=False, timeout=1800):
    """Executa a bancada AUT-3 REAL na copia, ancorada no repo de origem.

    --ancora origem preserva o PathMap (DLL byte-identica ao build do repo real).
    """
    cmd = [PY, BANCADA_REL.replace("\\", "/"), "--repo", copia, "--ancora", ancora,
           "--trabalho", os.path.join(trabalho, "aut3")]
    if jogo:
        cmd.append("--jogo")
    if sem_build:
        cmd.append("--sem-build")
    return run_cmd(cmd, cwd=copia, timeout=timeout)


def rodar_regressao_aut3(copia, ancora, selecionadas):
    """Regressao delimitada: executa as definicoes reais de CHECAGENS do AUT-3.

    Nao e FULL nem prova de build/runtime. Nao reusa verde de rodada anterior.
    Cada execucao mede snapshot e guardas e persiste stdout/exit reais.
    """
    offline = os.path.join(copia, "tools", "automacao", "offline")
    sys.dont_write_bytecode = True
    sys.path.insert(0, offline)
    spec = importlib.util.spec_from_file_location("ciclo_aut3_motor", os.path.join(offline, "bancada_aut3.py"))
    motor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(motor)
    ids = set(selecionadas)
    conhecidas = {c["id"] for c in motor.CHECAGENS}
    if ids - conhecidas:
        raise ValueError("checagem AUT-3 desconhecida: %s" % sorted(ids - conhecidas))
    motor.CHECAGENS = [c for c in motor.CHECAGENS if c["id"] in ids]
    antes = motor.snapshot_repo(copia)
    perfil_antes = motor.snapshot_perfil()
    checagens = motor.rodar_checagens(copia)
    depois = motor.snapshot_repo(copia)
    guarda = motor.comparar_snapshot(antes, depois)
    guarda.update(sha_antes={k: (v or "")[:12] for k, v in antes.items()},
                  sha_depois={k: (v or "")[:12] for k, v in depois.items()})
    perfil_intacto = perfil_antes == motor.snapshot_perfil()
    veredito = motor.aut3_lib.veredito(checagens)
    if not guarda["intacto"] or not perfil_intacto:
        veredito = "REPROVADO"
    dados = dict(esquema="AUT-3/1", repo=copia, ancora=ancora,
                 escopo=dict(tipo="regressao", criterios=sorted(ids), full=False),
                 veredito=veredito, builds=[], builds_executados=0, limite_builds=6,
                 suite=[], contra_provas=[], checagens=checagens, fases_puladas=[],
                 guarda_repo=guarda, guarda_perfil=dict(intacto=perfil_intacto))
    destino = caminho_resultado_aut3(copia)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as fh:
        json.dump(dados, fh, ensure_ascii=False, indent=2)
    return dados


def caminho_resultado_aut3(copia):
    return os.path.join(copia, "docs", "automacao", "AUT-3-resultado.json")


def resultado_reescrito(mtime_antes, mtime_depois):
    """O resultado AUT-3 foi REESCRITO nesta rodada?

    False quando o arquivo ja existia com o MESMO mtime (veio de copia: log velho)
    ou quando nao existe. Nunca deixar um resultado antigo virar falso verde.
    """
    if mtime_depois is None:
        return False
    if mtime_antes is None:
        return True
    return mtime_depois != mtime_antes


def carregar_json(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return json.load(fh)


# ==========================================================================
# serializacao da rodada: duas instancias na MESMA area externa se destroem
# ==========================================================================

def _pid_vivo(pid):
    try:
        pid = int(pid)
    except (TypeError, ValueError):
        return False
    if pid <= 0:
        return False
    if os.name == "nt":
        import ctypes
        SYNCHRONIZE = 0x00100000
        handle = ctypes.windll.kernel32.OpenProcess(SYNCHRONIZE, 0, pid)
        if handle:
            ctypes.windll.kernel32.CloseHandle(handle)
            return True
        return False
    try:
        os.kill(pid, 0)
    except OSError:
        return False
    return True


def tomar_lock(base):
    """Toma o lock da area externa. Devolve (caminho, None) ou (None, motivo).

    Duas rodadas na mesma area se destroem: uma apaga `aut3/sandbox` e o
    `ciclo-copia` da outra, e a rodada sobrevivente reprova por sandbox vazio
    (FALSO VERMELHO por ambiente, nao por defeito). Lock obsoleto (pid morto) e
    retomado -- nunca trava a area para sempre.
    """
    caminho = os.path.join(base, "ciclo.lock")
    os.makedirs(base, exist_ok=True)
    for _ in range(2):
        try:
            fd = os.open(caminho, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            dono = 0
            try:
                with open(caminho, encoding="utf-8") as fh:
                    dono = int((fh.read() or "0").strip() or 0)
            except (OSError, ValueError):
                dono = 0
            if dono and _pid_vivo(dono):
                return None, ("outra rodada do ciclo esta ativa na area externa (%s, pid %s): nao "
                              "concorrer na mesma area; use --trabalho distinto" % (caminho, dono))
            try:
                os.remove(caminho)
            except OSError:
                return None, "lock obsoleto em %s nao pode ser removido" % caminho
            continue
        os.write(fd, str(os.getpid()).encode("utf-8"))
        os.close(fd)
        return caminho, None
    return None, "nao consegui tomar o lock da rodada em %s" % caminho


def liberar_lock(caminho):
    try:
        if caminho and os.path.isfile(caminho):
            os.remove(caminho)
    except OSError:
        pass


def carregar_aut3(caminho):
    """Le o resultado do AUT-3 e devolve (dict, None) ou (None, erro)."""
    if not caminho or not os.path.isfile(caminho):
        return None, "resultado AUT-3 ausente: %s" % caminho
    try:
        dados = carregar_json(caminho)
    except (ValueError, OSError) as erro:
        return None, "resultado AUT-3 ilegivel: %s" % erro
    if not isinstance(dados, dict) or "veredito" not in dados:
        return None, "resultado AUT-3 sem veredito (formato inesperado)"
    return dados, None


# ==========================================================================
# criterios <- AUT-3 ; fila <- criterios
# ==========================================================================

def _criterio(cid, mod, estado, classe, procedencia, esperado, observado,
              evidencia, motivo, extra=None, causa=None, tarefa=None):
    c = dict(id=cid, mod=mod or "transversal", estado=estado, classe=classe,
             procedencia=procedencia, esperado=esperado, observado=observado,
             evidencia=list(evidencia or []), motivo=motivo or "",
             causa=causa or None,
             tarefa_origem=(tarefa or "desconhecido"))
    if extra:
        c.update(extra)
    return c


def _estado_aut3(item):
    return _MAPA_AUT3.get(item.get("estado"), item.get("estado") or INDETERMINADO)


def _script_do_comando(comando):
    """Extrai o .py do comando AUT-3 ('<py.exe> tools/x.py --flag' -> 'tools/x.py')."""
    for tok in reversed(str(comando or "").replace("\\", "/").split()):
        if tok.endswith(".py"):
            return tok
    return None


def _evidencia(repo, candidatos):
    """Evidencia = caminhos REAIS (o contrato exige caminhos, nao o comando).

    Com `repo` informado, so entram caminhos que existem (o que decisao.py/CIC-2
    reconfere). Sem `repo`, devolve os candidatos relativos como estao.
    """
    out = []
    for cand in candidatos:
        if not cand:
            continue
        if repo is None or os.path.isfile(os.path.join(repo, cand)):
            out.append(cand)
    return out


def _baixar_ok(criterios, motivo):
    """Nenhum OK pode sobreviver quando a prova NAO vale (identidade/snapshot)."""
    for c in criterios:
        if c["estado"] == OK:
            c["estado"] = NAO_EXERCITADO
            anterior = str(c.get("motivo") or "")
            c["motivo"] = motivo + (" | antes: " + anterior if anterior else "")


def criterios_aut3(aut3, ident, repo=None, snapshot_ok=True, snapshot_motivo="",
                   evidencia_resultado=None):
    """Traduz o resultado AUT-3 em criterios do contrato do ciclo.

    Escopo: builds, conferidores, suites, contra-provas, guarda de perfil/repo,
    fases puladas e a cobertura AUT-2 (residual de runtime). `evidencia` sao
    CAMINHOS reais; o comando vai no campo `comando`. NAO marca OK nada sem
    identidade suficiente nem com snapshot divergente.
    """
    criterios = []
    suf = identidade_suficiente(ident)

    def dll_de(mod):
        return "%s/bin/Release/netstandard2.1/%s.dll" % (mod, mod)

    def csproj_de(mod):
        return "%s/%s.csproj" % (mod, mod) if mod else None

    for b in aut3.get("builds", []):
        mod = b.get("mod")
        est = _estado_aut3(b)
        motivo = "" if est == OK else (b.get("erro_lancamento") or "build nao passou")
        proven = bool(b.get("fonte_dll_provada"))
        criterios.append(_criterio(
            "build_" + str(mod), mod, est, "offline", "execucao",
            "build Release 0 erros", "exit=%s sha=%s" % (b.get("exit_code"), b.get("sha_sandbox")),
            _evidencia(repo, [dll_de(mod)]), motivo,
            extra={"fonte_dll_provada": proven, "comando": b.get("comando")},
            causa=csproj_de(mod)))
        # A prova fonte->DLL e um criterio proprio: sem ela o offline fica INCOMPLETO
        # (nunca vira REPROVADO se o build em si passou).
        criterios.append(_criterio(
            "fonte_dll_" + str(mod), mod, OK if proven else NAO_EXERCITADO,
            "offline", "execucao", "fonte=Release=perfil por sha256",
            "provada" if proven else "nao provada",
            _evidencia(repo, [dll_de(mod)]),
            "" if proven else "hash do sandbox difere de Release/perfil",
            causa=csproj_de(mod)))

    for c in aut3.get("checagens", []):
        est = _estado_aut3(c)
        motivo = str(c.get("detalhe") or "")[-400:] if est != OK else ""
        criterios.append(_criterio(
            str(c.get("id")), c.get("mod"), est, "offline",
            "execucao", str(c.get("desc") or ""), "exit=%s" % c.get("exit_code"),
            _evidencia(repo, [_script_do_comando(c.get("comando"))]), motivo,
            extra={"comando": c.get("comando"), "classe_aut3": c.get("classe"),
                   "arquivo_causa": c.get("arquivo")},
            causa=c.get("arquivo")))

    for s in aut3.get("suite", []):
        est = _estado_aut3(s)
        motivo = str(s.get("detalhe") or "")[-400:] if est != OK else ""
        criterios.append(_criterio(
            str(s.get("id")), "transversal", est, "offline",
            "execucao", str(s.get("desc") or ""), "exit=%s contagem=%s" % (s.get("exit_code"), s.get("contagem")),
            _evidencia(repo, [_script_do_comando(s.get("comando"))]), motivo,
            extra={"comando": s.get("comando"), "classe_aut3": s.get("classe")}))

    for p in aut3.get("contra_provas", []):
        ok = p.get("veredito") == "PROVA_OK"
        criterios.append(_criterio(
            str(p.get("id")), "transversal", OK if ok else REPROVADO, "offline", "execucao",
            "defeito reprova e correcao aprova", "defeito=%s correcao=%s"
            % (p.get("exit_com_defeito"), p.get("exit_apos_correcao")),
            _evidencia(repo, [p.get("arquivo"), _script_do_comando(p.get("comando"))]),
            "" if ok else str(p.get("detalhe") or "contra-prova nao fechou"),
            causa=p.get("arquivo")))

    guarda = {
        "guarda_perfil": aut3.get("guarda_perfil", {}).get("intacto"),
        "guarda_repo": aut3.get("guarda_repo", {}).get("intacto"),
    }
    ev_guarda = [evidencia_resultado] if evidencia_resultado else []
    for nome, intacto in guarda.items():
        if intacto is True:
            if ev_guarda:
                est, motivo = OK, ""
            else:
                # Guarda lida como intacta mas SEM artefato de evidencia persistido:
                # um OK sem evidencia seria reprovado pela decisao (label nao basta).
                est, motivo = NAO_EXERCITADO, (
                    "guarda lida como intacta, mas a rodada nao persistiu artefato de evidencia; "
                    "sem arquivo existente o OK nao e vinculante -> nova rodada")
        elif intacto is False:
            est, motivo = REPROVADO, "guarda %s VIOLADO" % nome
        else:
            est, motivo = INDETERMINADO, "guarda %s nao pode ser lida (fail-closed)" % nome
        criterios.append(_criterio(nome, "transversal", est, "offline", "execucao",
                                   "intacto", str(intacto),
                                   ev_guarda, motivo))

    for fase in aut3.get("fases_puladas", []) or []:
        criterios.append(_criterio("fase:" + str(fase), "transversal", NAO_EXERCITADO,
                                   "offline", "execucao", "fase exercitada", "pulada",
                                   [], "fase nao exercitada nesta rodada → NAO e OK"))

    # Cobertura da matriz AUT-2: os itens de RUNTIME saem NAO_EXERCITADO -- sao o
    # RESIDUAL que sobra para AUT-4/5/6 e o olho humano. Nao podem sumir do ciclo.
    _mapa_cob = {
        "OK_OFFLINE": (OK, "offline", "execucao"),
        "PARCIAL_OFFLINE": (NAO_EXERCITADO, "offline", "execucao"),
        "REPROVADO": (REPROVADO, "offline", "execucao"),
        "NAO_EXERCITADO": (NAO_EXERCITADO, "runtime", "runtime"),
    }
    for it in (aut3.get("cobertura") or {}).get("itens", []) or []:
        estado, classe, proc = _mapa_cob.get(
            it.get("estado"), (INDETERMINADO, "offline", "execucao"))
        mod = it.get("mod")
        ev = []
        if estado == OK:
            cand = [dll_de(mod)] if (mod and str(it.get("id", "")).startswith("M")) \
                else ["tools/testes/roda_testes.py"]
            ev = _evidencia(repo, cand)
        criterios.append(_criterio(
            "cobertura:" + str(it.get("id")), mod, estado, classe, proc,
            "criterio AUT-2 coberto", str(it.get("estado")),
            ev, it.get("evidencia_aut3") or it.get("motivo") or "",
            tarefa=it.get("tarefa_origem")))

    # (1) identidade insuficiente -> NENHUM OK sobrevive (nunca falso verde).
    if not suf:
        _baixar_ok(criterios, "sem identidade de fonte suficiente (fonte_sha/dll_sha)")
    # (2) snapshot divergente/ausente -> o AUT-3 reusado NAO prova os bytes atuais.
    if snapshot_ok is False:
        _baixar_ok(criterios, snapshot_motivo or "AUT-3 reusado nao corresponde aos bytes atuais")
        criterios.append(_criterio(
            "reuso_snapshot_aut3", "transversal", NAO_EXERCITADO, "offline", "execucao",
            "AUT-3 amarra os bytes atuais", "snapshot divergente", [],
            snapshot_motivo or "snapshot do AUT-3 nao confere com a fonte atual"))

    if aut3.get("veredito") == "INCOMPLETO" and not any(c["estado"] == NAO_EXERCITADO for c in criterios):
        criterios.append(_criterio("aut3_incompleto", "transversal", NAO_EXERCITADO,
                                   "offline", "execucao", "AUT-3 VERDE", aut3.get("veredito"),
                                   [], "AUT-3 saiu INCOMPLETO"))
    return criterios


def criterios_reprovados(criterios):
    return [c for c in criterios if c["estado"] == REPROVADO]


def criterios_nao_exercitados(criterios):
    return [c for c in criterios if c["estado"] in (NAO_EXERCITADO, INDETERMINADO)]


def montar_fila(criterios, ident):
    """Fila de correcao DECLARATIVA. Nada aqui e executado automaticamente.

    Roteamento honesto: `caminhos` aponta a CAUSA quando conhecida; quando nao,
    `causa_desconhecida=True` e o roteamento e explicitamente "desconhecido" (nunca
    finge que o defeito pertence a uma tarefa por omissao).
    """
    fila = []
    for c in criterios:
        if c["estado"] != REPROVADO:
            continue
        causa = c.get("causa") or None
        evidencia = list(c.get("evidencia") or [])
        if causa:
            instrucao = ("corrigir a CAUSA em %s e reenviar ao ciclo (nova rodada); "
                         "o ciclo NAO executa comando de correcao" % causa)
        else:
            instrucao = ("causa NAO identificada pela evidencia (%s): localizar o arquivo-fonte "
                         "responsavel no mod %s e reenviar ao ciclo (nova rodada); "
                         "o ciclo NAO executa comando de correcao"
                         % (", ".join(evidencia) or "sem evidencia", c.get("mod")))
        fila.append({
            "id": "corr:" + str(c["id"]),
            "criterio": c["id"],
            "mod": c.get("mod"),
            "classe": c.get("classe"),
            "falha": c.get("motivo") or c.get("observado") or "REPROVADO",
            "causa": causa,
            "causa_desconhecida": not bool(causa),
            "caminhos": [causa] if causa else [],
            "evidencia": evidencia,
            "roteamento": "causa" if causa else "desconhecido",
            "tarefa_origem": c.get("tarefa_origem") or "desconhecido",
            "requer_nova_rodada": True,
            "execucao_automatica": False,
            "fonte_sha": (ident or {}).get("fonte_sha"),
            "instrucao": instrucao,
            "origem": "criterio",
        })
    return fila


def fila_da_decisao(decisao, fila_base, ident):
    """Acrescenta a fila as falhas_automaticas que a decisao apontou e o criterio
    do ciclo ainda nao cobria (ex.: OK sem evidencia, hash nao confirmado)."""
    ja = set(str(f.get("criterio")) for f in (fila_base or []))
    out = []
    for f in (decisao.get("falhas_automaticas") or []):
        cid = str(f.get("id") or "<sem-id>")
        if cid in ja:
            continue
        ja.add(cid)
        out.append({
            "id": "corr:" + cid,
            "criterio": cid,
            "mod": f.get("mod"),
            "classe": f.get("classe"),
            "falha": f.get("motivo_decisao") or f.get("motivo") or "FALHA_AUTOMATICA",
            "causa": None,
            "causa_desconhecida": True,
            "caminhos": [],
            "evidencia": list(f.get("evidencia") or f.get("problemas") or []),
            "roteamento": "desconhecido",
            "tarefa_origem": f.get("tarefa_origem") or "desconhecido",
            "severidade": f.get("severidade"),
            "requer_nova_rodada": True,
            "execucao_automatica": False,
            "fonte_sha": (ident or {}).get("fonte_sha"),
            "instrucao": ("falha apontada pela decisao (%s): corrigir a causa e reenviar ao ciclo "
                          "(nova rodada)" % cid),
            "origem": "decisao",
        })
    return out


# ==========================================================================
# decisao.py (CIC-2) -- OPCIONAL: usa quando existir, nunca espera
# ==========================================================================

def carregar_decisao():
    """Carrega decisao.py. Devolve (modulo, erro, presente).

    `presente` distingue AUSENCIA (modulo ainda nao entregue -- fallback legitimo)
    de FALHA de carregamento (modulo existe e quebrou -- NUNCA esconder).
    """
    caminho = os.path.join(AQUI, "decisao.py")
    if not os.path.isfile(caminho):
        return None, "decisao.py ausente (CIC-2 nao entregue) -- ciclo segue com resultado minimo", False
    try:
        spec = importlib.util.spec_from_file_location("ciclo_decisao", caminho)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as erro:  # modulo presente e quebrado: reportar, nao silenciar
        return None, "decisao.py nao pode ser carregado: %s: %s" % (type(erro).__name__, erro), True
    if not hasattr(mod, "consolidar"):
        return None, "decisao.py sem consolidar()", True
    return mod, None, True


def decisao_minima(criterios, ident, fila):
    """Estrutura minima do contrato quando decisao.py ainda nao existe.

    nao exercitado (inclusive lacuna tecnica runtime) e falha AUTOMATIZAVEL --
    pronto_para_decisao nunca fica True convivendo com falha automatica.
    """
    por_mod = {}
    for c in criterios:
        por_mod.setdefault(c.get("mod") or "transversal", []).append(
            {"criterio": c["id"], "estado": c["estado"], "classe": c["classe"]})
    falhas = [dict(f) for f in (fila or [])]
    for c in criterios:
        # Lacuna tecnica runtime tambem pertence ao agente, nao some no fallback.
        # O minimo e conservador: roteiro residual especializado cabe ao CIC-2.
        if c["estado"] in (NAO_EXERCITADO, INDETERMINADO):
            falhas.append(dict(id=c["id"], mod=c.get("mod"), classe=c.get("classe"),
                               motivo_decisao=c.get("motivo") or "criterio nao exercitado",
                               severidade="NAO_EXERCITADO",
                               evidencia=list(c.get("evidencia") or []),
                               tarefa_origem=c.get("tarefa_origem")))
        elif c["estado"] == REPROVADO:
            falhas.append(dict(id=c["id"], mod=c.get("mod"), classe=c.get("classe"),
                               motivo_decisao=c.get("motivo") or "REPROVADO",
                               severidade="REPROVADO",
                               evidencia=list(c.get("evidencia") or []),
                               tarefa_origem=c.get("tarefa_origem")))
    return {
        "por_mod": por_mod,
        "falhas_automaticas": falhas,
        "pendencias_humanas": [],
        "pendencias_nao_exercitadas": [c["id"] for c in criterios
                                       if c["estado"] in (NAO_EXERCITADO, INDETERMINADO)],
        "pronto_para_decisao": bool(not falhas and identidade_suficiente(ident)),
        "motivo_pronto_para_decisao": (
            "NAO: identidade insuficiente (fonte_sha/dll_sha)" if not identidade_suficiente(ident)
            else ("NAO: %d falha(s) automatica(s) volta(m) ao ciclo" % len(falhas) if falhas
                  else "SIM: automacao sem falhas automaticas; nada foi ao dono")),
        "aceite_humano": None,
        "publicacao": None,
        "origem_decisao": "minima_no_ciclo",
        "nota": "decisao.py ausente; consolidacao minima do contrato (nao bloqueia o ciclo)",
    }


def consolidar_decisao(criterios, ident, fila, modulo, erro, presente=False):
    """Consolida a decisao. Devolve (decisao, aviso).

    `aviso` so e preenchido quando o modulo EXISTIA mas nao consolidou: isso e
    falha tecnica e NAO pode passar calada pelo fallback.
    """
    if modulo is not None:
        try:
            saida = modulo.consolidar(criterios, ident)
            if isinstance(saida, dict):
                saida.setdefault("origem_decisao", "decisao.py")
                return saida, None
            erro = "consolidar() nao devolveu dict"
        except Exception as ex:  # opcional nunca derruba a rodada, mas reporta
            erro = "consolidar() falhou: %s: %s" % (type(ex).__name__, ex)
    d = decisao_minima(criterios, ident, fila)
    aviso = None
    if presente:
        aviso = erro or "decisao.py presente nao consolidou"
        d["nota"] = "%s | FALHA TECNICA decisao.py: %s" % (d.get("nota", ""), aviso)
    elif erro:
        d["nota"] = "%s | %s" % (d.get("nota", ""), erro)
    return d, aviso


# ==========================================================================
# rodada: tentativas, sem progresso, invalidacao, escalonamento
# ==========================================================================

def carregar_anterior(resultado_path):
    if resultado_path and os.path.isfile(resultado_path):
        try:
            prev = carregar_json(resultado_path)
            if isinstance(prev, dict) and prev.get("esquema") == ESQUEMA:
                return prev
        except (ValueError, OSError):
            return None
    return None


def _chaves_fila(fila):
    return sorted(str(f.get("criterio")) for f in (fila or []))


def avaliar_tentativas(prev, ident, fila):
    """Numero da rodada, sem-progresso e invalidacao da rodada anterior."""
    if not prev:
        return dict(numero=1, limite=None, sem_progresso=False, sem_progresso_seguidas=0,
                    invalidou_anterior=False, motivo_sem_progresso="")
    pident = prev.get("identidade") or {}
    mesa = _chaves_fila((prev.get("fila_correcao") or []))
    atuais = _chaves_fila(fila)
    mesma_fonte = pident.get("fonte_sha") == (ident or {}).get("fonte_sha")
    mesmas_falhas = mesa == atuais
    sem_progresso = bool(atuais) and mesma_fonte and mesmas_falhas
    seguidas = (prev.get("tentativas", {}).get("sem_progresso_seguidas") or 0)
    seguidas = seguidas + 1 if sem_progresso else 0
    numero = (prev.get("tentativas", {}).get("numero") or 0) + 1
    motivo = ""
    if sem_progresso:
        motivo = ("mesma fonte (%s) e mesmas falhas (%s) da rodada %s: nenhuma correcao mudou os bytes"
                  % ((ident or {}).get("fonte_sha", "")[:12], ", ".join(atuais) or "vazio",
                     prev.get("tentativas", {}).get("numero")))
    return dict(numero=numero, limite=None, sem_progresso=sem_progresso,
                sem_progresso_seguidas=seguidas,
                invalidou_anterior=not mesma_fonte, motivo_sem_progresso=motivo)


def avaliar_escalonamento(tem_falha, tent, limite):
    """Escalona ao SUPERVISOR TECNICO (nunca ao dono) por limite ou sem progresso.

    Devolve (escalar, motivo, destino). `motivo` so e preenchido quando escala --
    nunca um motivo de escalonamento convivendo com escala=False.
    """
    if not tem_falha:
        return False, "", DESTINO_CICLO
    numero = (tent.get("numero") or 1)
    seguidas = (tent.get("sem_progresso_seguidas") or 0)
    if numero > limite:
        return True, ("limite de tentativas excedido (%d > %d) com falhas pendentes: escalar ao "
                      "supervisor tecnico (supervisor/agente; NAO ao dono) com a fila de correcao"
                      % (numero, limite)), DESTINO_SUPERVISOR
    if seguidas >= limite:
        return True, ("sem progresso por %d rodada(s) (limite %d): a mesma fonte e as mesmas falhas se "
                      "repetem; escalar ao supervisor tecnico (supervisor/agente; NAO ao dono)"
                      % (seguidas, limite)), DESTINO_SUPERVISOR
    return False, "", DESTINO_CICLO


def avaliar_invalidacao(fonte_antes, fonte_depois):
    """Mudanca de fonte durante a rodada invalida a captura (nunca falso verde)."""
    if not fonte_antes or not fonte_depois:
        return True, "identidade de fonte ausente antes/depois da rodada"
    if fonte_antes != fonte_depois:
        return True, ("fonte mudou durante a rodada (antes=%s depois=%s); captura invalidada"
                      % (fonte_antes[:12], fonte_depois[:12]))
    return False, ""


def verificar_resultado(resultado, ident_atual):
    """Um resultado guardado ainda vale para os bytes atuais?"""
    if not isinstance(resultado, dict):
        return False, "resultado invalido"
    antiga = (resultado.get("identidade") or {}).get("fonte_sha")
    atual = (ident_atual or {}).get("fonte_sha")
    if not antiga:
        return False, "resultado sem identidade de fonte"
    if not atual:
        return False, "identidade atual indisponivel"
    if antiga != atual:
        return False, ("fonte mudou desde a rodada (resultado=%s atual=%s): aprovacao anterior INVALIDADA"
                       % (antiga[:12], atual[:12]))
    dll_antiga = (resultado.get("identidade") or {}).get("dll_sha")
    dll_atual = (ident_atual or {}).get("dll_sha")
    if not dll_antiga or not dll_atual or dll_antiga != dll_atual:
        return False, "DLL mudou ou identidade DLL ausente: resultado INVALIDADO"
    return True, "resultado corresponde aos bytes atuais de fonte e DLL"


# ==========================================================================
# verificacao isolada (modo --verificar)
# ==========================================================================

def _executar_verificacao(repo, caminho_resultado):
    try:
        ident = identidade(repo)
    except RuntimeError as erro:
        ident = {"fonte_sha": None, "erro": str(erro)}
    resultado = None
    if os.path.isfile(caminho_resultado):
        try:
            resultado = carregar_json(caminho_resultado)
        except (ValueError, OSError):
            resultado = None
    ok, motivo = verificar_resultado(resultado, ident)
    saida = dict(esquema=ESQUEMA, modo="verificar", repo=repo,
                 identidade_atual={"fonte_sha": ident.get("fonte_sha"),
                                   "dll_sha": ident.get("dll_sha")},
                 resultado=os.path.abspath(caminho_resultado),
                 valido=ok, motivo=motivo)
    print(json.dumps(saida, ensure_ascii=False, indent=2))
    return 0 if ok else 3


# ==========================================================================
# fluxo principal
# ==========================================================================

def _resumo_curto(aut3):
    if not aut3:
        return None
    return dict(veredito=aut3.get("veredito"),
                builds_executados=aut3.get("builds_executados"),
                limite_builds=aut3.get("limite_builds"),
                fases_puladas=aut3.get("fases_puladas"))


def _resultado_bloqueado(args, base, motivo):
    """Rodada que nao pode comecar (area ocupada) NAO vira verde: INCOMPLETO/2."""
    resultado = dict(
        esquema=ESQUEMA, tarefa=TAREFA, gerado_em=agora(),
        repo=os.path.abspath(args.repo), seletor=dict(jogo=not args.sem_jogo, sem_build=args.sem_build),
        escopo=dict(tipo="nao_iniciada", full=None),
        identidade={}, identidade_depois={}, invalido=False, motivo_invalidacao="",
        aut3_meta=dict(modo="bloqueado", erro=motivo), aut3_resumo=None,
        reuso=dict(modo="bloqueado", snapshot_ok=None, snapshot_motivo="", snapshot_detalhe={}),
        criterios=[], falhas_automaticas=[], pendencias=[], pendencias_offline=[],
        pendencias_runtime=[], fila_correcao=[],
        tentativas=dict(numero=1, limite=LIMITE_PADRAO, sem_progresso=False,
                        sem_progresso_seguidas=0, invalidou_anterior=False, motivo_sem_progresso=""),
        escala=False, motivo_escalacao="", destino_escalonamento=DESTINO_CICLO,
        decisao=dict(falhas_automaticas=[], pendencias_humanas=[], pronto_para_decisao=False,
                     origem_decisao="nao_iniciada"),
        estado=ESTADO_INCOMPLETO, erro=motivo, area=base,
        historico=[], limites=dict(nota="rodada nao iniciada: area externa ocupada (lock do ciclo)"),
    )
    saida = os.path.abspath(args.resultado) if args.resultado else None
    if saida:
        os.makedirs(os.path.dirname(saida) or ".", exist_ok=True)
        with open(saida, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(resultado, fh, ensure_ascii=False, indent=2)
    _imprimir(resultado)
    return _exit(ESTADO_INCOMPLETO)


def rodada(args):
    """Serializa a rodada na area externa (lock) e delega ao corpo."""
    base = os.path.abspath(args.trabalho) if args.trabalho else area_trabalho()
    lock = None
    if not args.aut3_resultado:
        lock, erro_lock = tomar_lock(base)
        if erro_lock:
            return _resultado_bloqueado(args, base, erro_lock)
    try:
        return _rodada_no_corpo(args, base)
    finally:
        liberar_lock(lock)


def _rodada_no_corpo(args, base):
    repo = os.path.abspath(args.repo)
    resultado_path = os.path.abspath(args.resultado) if args.resultado else None
    seletor = dict(jogo=(not args.sem_jogo), sem_build=args.sem_build)

    # ---- identidade ANTES (fonte de verdade = bytes atuais do repo) ----
    try:
        ident_antes = identidade(repo)
    except RuntimeError as erro:
        ident_antes = {"fonte_sha": None, "erro": str(erro)}
    prev = carregar_anterior(resultado_path)

    aut3 = None
    aut3_meta = {}

    if args.aut3_resultado:
        aut3, erro = carregar_aut3(os.path.abspath(args.aut3_resultado))
        aut3_meta.update(modo="reuso", resultado_aut3=os.path.abspath(args.aut3_resultado), erro=erro)
    else:
        caso = os.path.join(base, "ciclo-copia")
        # bancada_aut3 recria <trabalho>/aut3/sandbox com shutil.rmtree sem tratar
        # read-only; no Windows isso CRASHA se o sandbox anterior ficou. Limpamos
        # aqui (com tratamento) para a rodada nao morrer por sobra da anterior.
        sobra_sandbox = os.path.join(base, "aut3", "sandbox")
        if os.path.isdir(sobra_sandbox):
            try:
                _remover_arvore(sobra_sandbox)
            except OSError:
                pass
        copia = None
        try:
            copia = copiar_repo(repo, caso)
        except OSError as erro:
            aut3_meta.update(modo="copia", erro="nao consegui copiar o repo: %s" % erro)
        if copia and getattr(args, "checagem", None):
            try:
                aut3 = rodar_regressao_aut3(copia, repo, args.checagem)
                aut3_meta.update(modo="regressao", copia=copia,
                                 resultado_aut3=caminho_resultado_aut3(copia))
            except Exception as erro:
                aut3_meta.update(modo="regressao", erro="regressao AUT-3 falhou: %s" % erro)
        elif copia:
            respath = caminho_resultado_aut3(copia)
            mtime_antes = os.path.getmtime(respath) if os.path.isfile(respath) else None
            ancora = os.path.abspath(args.ancora) if getattr(args, "ancora", None) else repo
            r = rodar_aut3(copia, ancora, base, jogo=seletor["jogo"], sem_build=seletor["sem_build"])
            aut3_meta.update(modo="execucao", copia=copia, comando=" ".join(r["comando"]),
                             ancora=ancora,
                             exit_code=r["exit_code"], resultado_aut3=respath,
                             bancada_stdout_tail=_sanitiza((r.get("stdout") or "")[-600:]),
                             bancada_stderr_tail=_sanitiza((r.get("stderr") or "")[-600:]))
            if r.get("erro_lancamento"):
                aut3_meta["erro"] = "AUT-3 nao lancou: %s" % r["erro_lancamento"]
            # GUARDA DE RESULTADO STALE: o resultado tem de ter sido REESCRITO nesta
            # rodada. Se o arquivo veio da copia (mtime inalterado), NAO vale -- e o
            # mesmo "log velho" que o ciclo existe para proibir (nunca falso verde).
            mtime_depois = os.path.getmtime(respath) if os.path.isfile(respath) else None
            if not resultado_reescrito(mtime_antes, mtime_depois):
                aut3_meta["erro"] = ("resultado AUT-3 STALE: '%s' nao foi reescrito pela rodada "
                                     "(mtime inalterado); ignorado para nao dar falso verde" % respath)
                aut3 = None
            else:
                aut3, erro2 = carregar_aut3(respath)
                if aut3 is None:
                    aut3_meta["erro"] = "AUT-3 nao gerou resultado (%s); stdout/stderr tail: %s" % (
                        erro2, (r.get("stdout", "") + r.get("stderr", ""))[-600:])

    # ---- identidade DEPOIS (no repo): invalidacao por concorrencia ----
    try:
        ident_depois = identidade(repo)
    except RuntimeError as erro:
        ident_depois = {"fonte_sha": None, "erro": str(erro)}

    # Vinculo gravado APENAS numa execucao nova, nunca no reuso. O AUT-3 cru
    # legado nao conhece as DLLs ignoradas pelo git: sem este vinculo persistido
    # ele exige nova rodada (nao se hasheia a DLL atual para reassinar log velho).
    if aut3 is not None and not args.aut3_resultado:
        aut3["ciclo_identidade"] = dict(ident_antes)
        prova_path = aut3_meta.get("resultado_aut3")
        if prova_path:
            with open(prova_path, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(aut3, fh, ensure_ascii=False, indent=2)

    invalidado, motivo_invalidacao = avaliar_invalidacao(
        ident_antes.get("fonte_sha"), ident_depois.get("fonte_sha"))
    if not invalidado and ident_antes.get("dll_sha") != ident_depois.get("dll_sha"):
        invalidado, motivo_invalidacao = True, "DLL mudou durante a rodada: captura invalidada"

    # ---- SNAPSHOT do AUT-3 x bytes ATUAIS (correcao do falso verde no reuso) ----
    reuso = dict(modo=aut3_meta.get("modo"), snapshot_ok=None,
                 snapshot_motivo="", snapshot_detalhe={})
    if aut3 is not None:
        snap_ok, snap_motivo, snap_det = confrontar_snapshot(aut3, repo)
        if args.aut3_resultado:
            prova_ident = aut3.get("ciclo_identidade")
            prova_ident = prova_ident if isinstance(prova_ident, dict) else {}
            snap_det = dict(snap_det)
            dll_prova = prova_ident.get("dll_sha")
            dll_atual = ident_antes.get("dll_sha")
            dll_ok = bool(dll_prova and dll_atual and dll_prova == dll_atual)
            snap_det["dll_prova"] = dll_prova or ""
            snap_det["dll_atual"] = dll_atual or ""
            snap_det["dll_ok"] = dll_ok
            if not dll_ok:
                snap_ok = False
                snap_motivo = (snap_motivo + " | " if snap_motivo else "") + (
                    "DLL da prova original ausente ou divergente dos bytes atuais; "
                    "nova rodada necessaria (reuso nao reassina prova antiga)")
            if prova_ident.get("fonte_sha") and prova_ident["fonte_sha"] != ident_antes.get("fonte_sha"):
                snap_ok = False
                snap_motivo = (snap_motivo + " | " if snap_motivo else "") + (
                    "identidade de fonte original diverge dos bytes atuais; nova rodada necessaria")
        reuso.update(snapshot_ok=snap_ok, snapshot_motivo=snap_motivo, snapshot_detalhe=snap_det)
        ev_resultado = aut3_meta.get("resultado_aut3")
        ev_resultado = os.path.abspath(ev_resultado) if ev_resultado and os.path.isfile(ev_resultado) else None
        if not ev_resultado and os.path.isfile(os.path.join(repo, "docs", "automacao", "AUT-3-resultado.json")):
            ev_resultado = os.path.join(repo, "docs", "automacao", "AUT-3-resultado.json")
        criterios = criterios_aut3(aut3, ident_antes, repo=repo,
                                   snapshot_ok=snap_ok, snapshot_motivo=snap_motivo,
                                   evidencia_resultado=ev_resultado)
    else:
        # Sem resultado AUT-3 nao ha criterios: rodada NAO_EXERCITADA (incompleta).
        criterios = [_criterio("aut3_resultado", "transversal", NAO_EXERCITADO,
                               "offline", "execucao", "resultado AUT-3 valido", "ausente",
                               [], aut3_meta.get("erro") or "AUT-3 nao produziu resultado")]

    # ---- fila base <- criterios ; decisao ; fila complementar <- decisao ----
    fila_base = montar_fila(criterios, ident_antes)
    decisao_mod, decisao_erro, decisao_presente = carregar_decisao()
    ident_decisao = dict(ident_antes or {})
    ident_decisao["raiz"] = repo  # para decisao.py resolver os caminhos de evidencia
    decisao, decisao_aviso = consolidar_decisao(criterios, ident_decisao, fila_base,
                                                decisao_mod, decisao_erro, decisao_presente)
    if decisao_aviso:
        # FALHA TECNICA visivel: nao esconder no fallback.
        criterios.append(_criterio("decisao_consolidacao", "transversal", REPROVADO,
                                   "offline", "execucao", "decisao.py consolida",
                                   "falhou", [], decisao_aviso))
        decisao.setdefault("falhas_automaticas", []).append(
            dict(id="decisao_consolidacao", mod="transversal", motivo_decisao=decisao_aviso,
                 severidade=REPROVADO, evidencia=[], tarefa_origem="desconhecido"))
    fila = list(fila_base) + fila_da_decisao(decisao, fila_base, ident_antes)

    tent = avaliar_tentativas(prev, ident_antes, fila)
    limite = args.limite if args.limite else LIMITE_PADRAO
    tent["limite"] = limite

    falhas_decisao = list(decisao.get("falhas_automaticas") or [])
    tem_reprov = bool(criterios_reprovados(criterios)) or \
        any((f.get("severidade") == REPROVADO) for f in falhas_decisao)
    tem_falha = tem_reprov or bool(falhas_decisao) or bool(criterios_reprovados(criterios))
    escalar, motivo_escalacao, destino = avaliar_escalonamento(tem_falha, tent, limite)

    # ---- estado final: incorpora decisao + identidade DLL (sem APROVADO paralelo) ----
    pend = criterios_nao_exercitados(criterios)
    pend_offline = [c for c in pend if c.get("classe") != "runtime"]
    pend_runtime = [c for c in pend if c.get("classe") == "runtime"]
    if invalidado:
        estado = ESTADO_INVALIDADO
    elif escalar:
        estado = ESTADO_ESCALADO
    elif tem_reprov:
        estado = ESTADO_REPROVADO
    elif tem_falha or pend_offline or aut3 is None:
        estado = ESTADO_INCOMPLETO
    elif not identidade_suficiente(ident_antes):
        estado = ESTADO_INCOMPLETO
    else:
        # offline todo exercitado; o que sobra e residual de RUNTIME (AUT-4/5/6 + humano).
        estado = ESTADO_REGRESSAO if (aut3.get("escopo") or {}).get("full") is False else ESTADO_APROVADO

    resultado = dict(
        esquema=ESQUEMA, tarefa=TAREFA, gerado_em=agora(), repo=repo,
        seletor=seletor,
        escopo=(aut3 or {}).get("escopo") or dict(tipo="full", full=True),
        identidade=ident_antes, identidade_depois=ident_depois,
        invalido=invalidado, motivo_invalidacao=motivo_invalidacao,
        aut3_meta=aut3_meta,
        aut3_resumo=_resumo_curto(aut3),
        reuso=reuso,
        criterios=criterios,
        falhas_automaticas=falhas_decisao,
        pendencias=pend,
        pendencias_offline=pend_offline,
        pendencias_runtime=pend_runtime,
        fila_correcao=fila,
        tentativas=dict(numero=tent["numero"], limite=limite,
                        sem_progresso=tent["sem_progresso"],
                        sem_progresso_seguidas=tent["sem_progresso_seguidas"],
                        invalidou_anterior=tent["invalidou_anterior"],
                        motivo_sem_progresso=tent["motivo_sem_progresso"]),
        escala=escalar, motivo_escalacao=motivo_escalacao, destino_escalonamento=destino,
        decisao=decisao, decisao_erro=decisao_aviso,
        estado=estado,
        historico=_historico(prev, ident_antes, estado, fila),
        limites=dict(nota="AUT-3 offline; nao abre jogo, nao instala, nao publica, nao commita; "
                          "builds Release -p:DeployToBepInEx=false em copia isolada (max 6/rodada)"),
    )

    if resultado_path:
        os.makedirs(os.path.dirname(resultado_path) or ".", exist_ok=True)
        with open(resultado_path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(resultado, fh, ensure_ascii=False, indent=2)

    _imprimir(resultado)
    return _exit(estado)


def _historico(prev, ident, estado, fila):
    hist = list((prev or {}).get("historico") or [])
    if prev:
        hist.append(dict(numero=(prev.get("tentativas") or {}).get("numero"),
                         fonte_sha=(prev.get("identidade") or {}).get("fonte_sha", "")[:12],
                         estado=prev.get("estado"), falhas=len(prev.get("fila_correcao") or [])))
    return hist[-20:]


def _exit(estado):
    return {ESTADO_APROVADO: 0, ESTADO_REGRESSAO: 0, ESTADO_REPROVADO: 1, ESTADO_ESCALADO: 1,
            ESTADO_INCOMPLETO: 2, ESTADO_INVALIDADO: 3}.get(estado, 2)


def _imprimir(r):
    dec = r.get("decisao") or {}
    resumo = dict(esquema=r["esquema"], estado=r["estado"],
                  escopo=r.get("escopo"),
                  fonte_sha=(r["identidade"] or {}).get("fonte_sha", "")[:12],
                  dll_sha=(r["identidade"] or {}).get("dll_sha") or "",
                  aut3=(r.get("aut3_resumo") or {}).get("veredito"),
                  reuso_snapshot_ok=r.get("reuso", {}).get("snapshot_ok"),
                  invalido=r["invalido"],
                  tentativa=r["tentativas"]["numero"], limite=r["tentativas"]["limite"],
                  sem_progresso=r["tentativas"]["sem_progresso"],
                  falhas=len(r["fila_correcao"]),
                  falhas_automaticas=len(dec.get("falhas_automaticas") or []),
                  pendencias_offline=len(r["pendencias_offline"]),
                  pendencias_runtime=len(r["pendencias_runtime"]),
                  pendencias_humanas=len(dec.get("pendencias_humanas") or []),
                  pronto=dec.get("pronto_para_decisao"),
                  motivo_pronto=dec.get("motivo_pronto_para_decisao"),
                  escala=r.get("escala"),
                  motivo_escalacao=r.get("motivo_escalacao", ""),
                  decisao=dec.get("origem_decisao"))
    print(json.dumps(resumo, ensure_ascii=False, indent=2))


def main():
    ap = argparse.ArgumentParser(description="CIC-1 - orquestrador do ciclo de validacao/revalidacao.")
    ap.add_argument("--repo", default=RAIZ_PADRAO, help="repositorio de ORIGEM (bytes atuais)")
    ap.add_argument("--trabalho", default=None, help="area externa para a copia isolada (padrao: scratch Hermes)")
    ap.add_argument("--ancora", default=None,
                    help="repo REAL cujo caminho a DLL embute via PathMap (padrao: --repo); use "
                         "quando --repo for um congelamento byte-exato do repo real")
    ap.add_argument("--resultado", default=None, help="onde gravar/ler o resultado do ciclo (JSON)")
    ap.add_argument("--aut3-resultado", default=None,
                    help="reusa um resultado AUT-3 ja gerado (nao faz copia nem build; exige snapshot coerente)")
    ap.add_argument("--checagem", action="append", help="regressao delimitada: ID de CHECAGENS AUT-3 (repetivel); nao aprova FULL")
    ap.add_argument("--verificar", default=None,
                    help="verifica se um resultado guardado ainda corresponde aos bytes atuais")
    ap.add_argument("--sem-jogo", action="store_true", help="nao inclui a suite --jogo do AUT-3")
    ap.add_argument("--sem-build", action="store_true",
                    help="seleciona a regressao afetada: pula os 6 builds (usa suite+conferidores)")
    ap.add_argument("--limite", type=int, default=0, help="limite de tentativas antes de escalar (padrao %d)" % LIMITE_PADRAO)
    args = ap.parse_args()
    if args.checagem and (args.aut3_resultado or args.sem_build or args.sem_jogo):
        ap.error("--checagem nao combina com reuso nem seletores FULL")
    if args.limite < 0:
        ap.error("--limite deve ser positivo")

    if args.verificar:
        return _executar_verificacao(os.path.abspath(args.repo), args.verificar)
    return rodada(args)


if __name__ == "__main__":
    sys.exit(main())
