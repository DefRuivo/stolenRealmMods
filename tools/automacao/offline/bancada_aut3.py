#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUT-3 - bancada de revisao estatica e regressao SEM tocar no perfil.

UM COMANDO roda a revisao offline aplicavel por mod e pelas dependencias reais:
builds sem deploy, a suite, os conferidores estaticos (duplicatas, chaves, notas,
versoes, patches, segredos, dependencias, pacotes, docs) e as contra-provas em
copia isolada. Nada escreve no perfil do dono: os conferidores que REESCREVEM
docs rodam dentro de um SANDBOX (copia descartavel do repo) e o perfil e medido
por hash antes/depois.

    python tools/automacao/offline/bancada_aut3.py

Exit:  0 = VERDE (tudo OK)  ·  1 = REPROVADO  ·  2 = INCOMPLETO (algo nao
exercitado). Erro de comando/build nunca vira verde, e "nao exercitado" e um
estado separado de OK. AUT-3 NAO substitui aceite humano nem publicacao.

Opcoes: --repo DIR (padrao: raiz deste repositorio) · --ancora DIR (repo REAL cujo
        caminho a DLL embute; padrao = --repo) · --trabalho DIR (sandbox)
        --sem-build · --sem-suite · --sem-contra-provas · --jogo (roda tambem a
        suite que precisa da lib/ do jogo) · --manter-sandbox · --sem-sandbox
        (modo somente-leitura, sem copia: os conferidores que escrevem docs sao
        PULADOS e saem como NAO_EXERCITADO)

AUT-3F: os builds rodam com USERPROFILE/APPDATA/LOCALAPPDATA isolados (env +
propriedades MSBuild) e a guarda de opt-in roda FAIL-CLOSED ANTES de qualquer
build. Rodar em copia isolada sem perder a ancora do PathMap:
    python bancada_aut3.py --repo <copia> --ancora <repo REAL> --jogo --trabalho <scratch>
"""
import argparse
import datetime
import json
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import aut3_lib  # noqa: E402
import contra_provas as cp  # noqa: E402

PY = sys.executable
MODS = ["BetterCombatText", "BetterFont", "BetterStats", "BetterTooltips",
        "RoguelikeDebugger", "RoguelikeSkillTreeVisualizer"]
IGNORAR_COPIA = ("scratch", "bin", "obj", "__pycache__", ".vs", ".git-rewrite")
MAX_BUILDS = 6

# AUT-3F: outputs do PROPRIO runner, excluidos EXPLICITAMENTE do guarda de repo
# (em vez de excluir pastas inteiras). scratch/ e area de trabalho externa.
EXCLUIDOS_GUARDA = {
    "docs/automacao/AUT-3-resultado.json",
    "docs/automacao/AUT-3-resumo.md",
}
PREFIXOS_EXCLUIDOS_GUARDA = ("scratch/",)
ISOLAMENTO_DIRS = ("userprofile", "appdata", "localappdata")


class GuardaGitIndisponivel(RuntimeError):
    """A listagem do git nao pode ser obtida (fail-closed).

    AUT-3F2 (A1): antes, `_git_lista_z` ignorava exit/stderr/timeout e devolvia [].
    Num dir sem `.git` (ou com o git ausente) o guarda de repo afirmava "intacto"
    TECNICAMENTE CEGO - podendo sair VERDE sem ter lido nada. Agora a listagem
    FALHA ALTO e o runner registra NAO_EXERCITADO/REPROVADO (nunca intacto/VERDE).
    """

# classe: puro | estrutura | build | pacote | docs
CHECAGENS = [
    dict(id="check_dupes", classe="estrutura", mod="BetterTooltips", escritas_docs=False,
         desc="chave duplicada nas tabelas do LocalizePatch", cmd=[PY, "tools/check_dupes.py"], esperado=0),
    dict(id="check_chave_compartilhada", classe="estrutura", mod="BetterTooltips", escritas_docs=False,
         desc="chave de texto compartilhada / nota que mente para outro dono",
         cmd=[PY, "tools/check_chave_compartilhada.py", "--estrito"], esperado=0),
    dict(id="check_notas_redundantes", classe="estrutura", mod="BetterTooltips", escritas_docs=True,
         desc="notas redundantes/duplicadas (REESCREVE docs/cobertura/revisao -> sandbox)",
         cmd=[PY, "tools/check_notas_redundantes.py"], esperado=0),
    dict(id="check_fix_keys", classe="estrutura", mod="BetterTooltips", escritas_docs=False,
         desc="chaves de TextFixes/TextAppends contra o censo", cmd=[PY, "tools/check_fix_keys.py"], esperado=0),
    dict(id="check_segredos", classe="estrutura", mod="transversal", escritas_docs=False,
         desc="nenhuma credencial no que seria publicado", cmd=[PY, "tools/check_segredos.py"], esperado=0),
    dict(id="check_versoes", classe="pacote", mod="transversal", escritas_docs=False,
         desc="csproj = manifest = Plugin.cs = README", cmd=[PY, "tools/check_versoes.py"], esperado=0),
    dict(id="check_patches", classe="estrutura", mod="transversal", escritas_docs=False,
         desc="5 regras de robustez dos patches Harmony", cmd=[PY, "tools/check_patches.py"], esperado=0),
    dict(id="check_dependencias", classe="pacote", mod="transversal", escritas_docs=False,
         desc="toda dependencia de manifest resolve", cmd=[PY, "tools/check_dependencias.py", "--local"], esperado=0),
    dict(id="check_deploy_optin", classe="estrutura", mod="transversal", escritas_docs=False,
         desc="nenhum alvo escreve no perfil sem opt-in", cmd=[PY, "tools/check_deploy_optin.py"], esperado=0),
    dict(id="pacotes_preflight", classe="pacote", mod="transversal", escritas_docs=False,
         desc="pre-flight Thunderstore (artefato x fonte, nada e zipado)",
         cmd=[PY, "tools/pack-thunderstore.py", "--so-conferir"], esperado=0),
    dict(id="audita_docs", classe="docs", mod="transversal", escritas_docs=False,
         desc="doc x disco (contagens, ferramentas, versoes, links)", cmd=[PY, "tools/audita_docs.py"], esperado=0),
]

# Cobertura da matriz AUT-2 que NAO se exercita offline (runtime de jogo).
RUNTIME = {
    "T-RSTV21": "janela read-only abre/navega/fecha e publicacao — exige jogo/dono",
    "T-RSTV25B": "precisa do LogOutput.log do proximo boot (INDETERMINADO)",
    "T-RSTV26": "hover com numeros resolvidos — revalidacao visual em jogo",
    "S-RV-26": "tooltip de shrine em jogo; RV-49 trava numeros das auras de PERIGO",
    "S-RV-27": "tooltip de shrine em jogo; RV-49 trava numeros das auras de PERIGO",
    "S-RV-28": "tooltip de shrine em jogo; RV-49 trava numeros das auras de PERIGO",
    "S-RV-29": "aura viva x fora da aura — leitura em jogo",
    "S-RV-30": "aura de perigo com Source=null — medicao em jogo",
    "S-RV-31": "agregado por atributo — leitura em jogo",
    "S-RV-33": "flame/decay por alvo — leitura em jogo",
    "S-RV-34": "defeito do proprio mod superado por RV-30 — revalidacao em jogo",
    "BUG34": "aceite humano ja dado (KANBAN l.506); regressao de feed exige jogo",
}


def _sha12(h):
    return (h or "--------")[:12]


def _sha256_curto(caminho):
    return _sha12(aut3_lib.sha256_file(caminho))


def raiz_do_repo():
    return os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))


def perfil_bepinex():
    up = os.environ.get("USERPROFILE", "")
    return os.path.join(up, "AppData", "Roaming", "r2modmanPlus-local", "StolenRealm",
                        "profiles", "Default", "BepInEx")


def snapshot_perfil():
    base = perfil_bepinex()
    snap = {}
    for pasta in ("plugins", "config"):
        raiz = os.path.join(base, pasta)
        for dirpath, _, arquivos in os.walk(raiz):
            for nome in sorted(arquivos):
                p = os.path.join(dirpath, nome)
                snap[os.path.relpath(p, base).replace("\\", "/")] = aut3_lib.sha256_file(p)
    return snap


def git(repo, *args):
    r = aut3_lib.run_cmd(["git"] + list(args), cwd=repo, timeout=120)
    return r["stdout"].strip()


def paths_status(repo):
    """Caminhos do `git status --porcelain -z` (robusto a espaco no nome)."""
    r = aut3_lib.run_cmd(["git", "status", "--porcelain", "-z"], cwd=repo, timeout=120)
    caminhos = []
    for bruto in r["stdout"].split("\0"):
        if len(bruto) > 3:
            caminhos.append(bruto[3:])
    return caminhos


def snapshot_por_rel(repo, caminhos):
    return {p: aut3_lib.sha256_file(os.path.join(repo, p))
            for p in caminhos if os.path.isfile(os.path.join(repo, p))}


def _detalhe(*partes, limite=600):
    """Junta/SANITIZA/trunca a captura ANTES de serializar.

    AUT-3F: sem prefixo de token no que serializa.
    AUT-3F2 (A2): sanitiza ANTES de truncar - cortar primeiro deixaria fragmento
    do segredo na janela final (um sufixo de token que a regex nao casaria mais).
    """
    texto = "".join(p or "" for p in partes)
    return aut3_lib.sanitiza(texto)[-limite:]


def _excluido_guarda(rel):
    rel = (rel or "").replace("\\", "/")
    return rel in EXCLUIDOS_GUARDA or rel.startswith(PREFIXOS_EXCLUIDOS_GUARDA)


def _git_lista_z(repo, *args):
    """Lista NUL-separada do git, FAIL-CLOSED (AUT-3F2/A1).

    Levanta GuardaGitIndisponivel quando a listagem NAO pode ser feita: comando
    ausente (erro_lancamento), timeout, ou exit != 0 (ex.: diretorio que nao e
    repo). Repo git VALIDO e VAZIO (exit 0, stdout vazio) NAO e erro -> [].
    """
    r = aut3_lib.run_cmd(["git"] + list(args), cwd=repo, timeout=120)
    rotulo = "git " + " ".join(args)
    if r.get("timeout"):
        raise GuardaGitIndisponivel("%s: timeout" % rotulo)
    if r.get("erro_lancamento"):
        raise GuardaGitIndisponivel("%s: %s" % (rotulo, r["erro_lancamento"]))
    if r.get("exit_code") != 0:
        cauda = (r.get("stderr") or r.get("stdout") or "").strip().replace("\n", " ")[:160]
        raise GuardaGitIndisponivel("%s: exit %s (%s)" % (rotulo, r.get("exit_code"), cauda))
    return [p for p in (r.get("stdout") or "").split("\0") if p]


def lista_repo(repo):
    """Arquivos TRACKED + UNTRACKED recursivos (--others --exclude-standard).

    Dir novo NAO colapsa (era o furo da AUT-3R: `git status` devolvia a PASTA
    `tools/automacao/` e o guarda nao hasheava nenhum arquivo dela). Exclui SO os
    outputs autorizados do runner e a area externa (scratch/).
    """
    rels = set(_git_lista_z(repo, "ls-files", "-z")) | set(
        _git_lista_z(repo, "ls-files", "-z", "--others", "--exclude-standard"))
    return sorted(p for p in rels if not _excluido_guarda(p))


def snapshot_repo(repo):
    return {p: aut3_lib.sha256_file(os.path.join(repo, p)) for p in lista_repo(repo)}


def comparar_snapshot(antes, depois):
    """Criado / removido / alterado entre dois snapshots {rel: sha}."""
    antes, depois = antes or {}, depois or {}
    criados = sorted(set(depois) - set(antes))
    removidos = sorted(set(antes) - set(depois))
    alterados = sorted(k for k in (set(antes) & set(depois)) if antes[k] != depois[k])
    return dict(criados=criados, removidos=removidos, alterados=alterados,
                intacto=not (criados or removidos or alterados))


def montar_env_isolado(base, real=None):
    """Ambiente dos builds: USERPROFILE/APPDATA/LOCALAPPDATA redirecionados p/ `base`.

    Preserva as FERRAMENTAS (PATH herdado) e o CACHE NuGet real (NUGET_PACKAGES):
    sem o cache o restore pode falhar dentro do isolamento. So o que escreveria no
    ambiente do dono vai para o sandbox.
    """
    real = real if real is not None else os.environ.get("USERPROFILE", "")
    perfil = os.path.join(base, "userprofile")
    env = {
        "USERPROFILE": perfil,
        "APPDATA": os.path.join(base, "appdata"),
        "LOCALAPPDATA": os.path.join(base, "localappdata"),
        "HOME": perfil,
        "DOTNET_CLI_HOME": perfil,
        "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
        "DOTNET_CLI_TELEMETRY_OPTOUT": "1",
        "DOTNET_NOLOGO": "1",
    }
    nuget = os.path.join(real, ".nuget", "packages") if real else ""
    if nuget and os.path.isdir(nuget):
        env["NUGET_PACKAGES"] = nuget
    for d in ISOLAMENTO_DIRS:
        os.makedirs(os.path.join(base, d), exist_ok=True)
    return env


def propriedades_isolamento(base):
    """Propriedades MSBuild que apontam o destino do deploy para o isolamento.

    Defesa em PROFUNDIDADE: mesmo se um csproj perder a Condition, $(USERPROFILE)
    resolve para dentro do sandbox - nunca para o perfil do dono.
    """
    def prop(nome, sub):
        return "-p:%s=%s" % (nome, os.path.join(base, sub).replace("\\", "/"))
    return [prop("USERPROFILE", "userprofile"), prop("APPDATA", "appdata"),
            prop("LOCALAPPDATA", "localappdata")]


def gate_builds(preflight_resultado):
    """FAIL-CLOSED: builda SO quando a guarda de opt-in rodou e passou (exit==0)."""
    return aut3_lib.avalia(preflight_resultado, 0) == aut3_lib.OK


def preflight_deploy(sb):
    """check_deploy_optin ANTES de qualquer build (o opt-in tem de valer ANTES de a
    primeira compilacao encostar em $USERPROFILE)."""
    return aut3_lib.run_cmd([PY, "tools/check_deploy_optin.py"], cwd=sb, timeout=120)


def estados_fases(args, sem_sandbox=None):
    """Fase nao exercitada vira NAO_EXERCITADO: 'pulado' NUNCA conta como verde."""
    ss = args.sem_sandbox if sem_sandbox is None else sem_sandbox
    itens = []
    if args.sem_build or ss:
        itens.append(dict(estado=aut3_lib.NAO_EXERCITADO, fase="builds",
                          motivo="--sem-build" if args.sem_build else "--sem-sandbox"))
    if args.sem_suite:
        itens.append(dict(estado=aut3_lib.NAO_EXERCITADO, fase="suite", motivo="--sem-suite"))
    if not getattr(args, "jogo", False):
        itens.append(dict(estado=aut3_lib.NAO_EXERCITADO, fase="suite_jogo",
                          motivo="suite_jogo omitida (rode com --jogo)"))
    if args.sem_contra_provas or ss:
        itens.append(dict(estado=aut3_lib.NAO_EXERCITADO, fase="contra_provas",
                          motivo="--sem-contra-provas" if args.sem_contra_provas else "--sem-sandbox"))
    return itens


def copiar_sandbox(repo, destino):
    def ignorar(dirpath, nomes):
        return [n for n in nomes if n in IGNORAR_COPIA]
    shutil.copytree(repo, destino, ignore=ignorar, symlinks=False)


def construir_sandbox(repo, trabalho):
    sb = os.path.join(trabalho, "sandbox")
    if os.path.isdir(sb):
        shutil.rmtree(sb)
    copiar_sandbox(repo, sb)
    return sb


def rodar_builds(sb, repo, ancora, iso, verboso=False):
    """Builds Release sem deploy, ISOLADOS (env + props MSBuild) e ancorados no repo REAL.

    `repo` = onde o artefato de referencia vive (bin/Release a comparar); `ancora` =
    caminho que a DLL embute via PathMap (o repo REAL) - separados para que a copia
    isolada nao quebre a prova por hash fonte->DLL.
    """
    env = montar_env_isolado(iso)
    props = propriedades_isolamento(iso)
    resultados = []
    for mod in MODS:
        csproj = os.path.join(sb, mod, mod + ".csproj")
        cmd = (["dotnet", "build", csproj.replace("\\", "/"), "-c", "Release",
                "-p:DeployToBepInEx=false", "-p:PathMap=%s=%s" % (sb, ancora)]
               + props + ["--nologo", "-v", "quiet"])
        r = aut3_lib.run_cmd(cmd, cwd=sb, timeout=600, env=env)
        dll_sb = os.path.join(sb, mod, "bin", "Release", "netstandard2.1", mod + ".dll")
        dll_repo = os.path.join(repo, mod, "bin", "Release", "netstandard2.1", mod + ".dll")
        dll_perfil = os.path.join(perfil_bepinex(), "plugins", mod, mod + ".dll")
        h_sb, h_repo, h_perf = (aut3_lib.sha256_file(dll_sb), aut3_lib.sha256_file(dll_repo),
                                aut3_lib.sha256_file(dll_perfil))
        # FONTE->DLL so e provado quando o build do sandbox BATE com o Release e com o perfil.
        fonte_provada = bool(h_sb) and h_sb == h_repo and h_sb == h_perf
        resultados.append(dict(
            id="build_" + mod, mod=mod, estado=aut3_lib.avalia(r, 0),
            comando=" ".join(cmd), cwd="<sandbox>", exit_code=r["exit_code"],
            segundos=r["segundos"], timeout=r["timeout"], erro_lancamento=r["erro_lancamento"],
            sha_sandbox=_sha12(h_sb), sha_release=_sha12(h_repo), sha_perfil=_sha12(h_perf),
            fonte_dll_provada=fonte_provada,
            stderr_tail="" if aut3_lib.avalia(r, 0) == "OK" else _detalhe(r["stderr"] or r["stdout"], limite=400),
        ))
    return resultados


def rodar_checagens(sb, sem_sandbox=False):
    resultados = []
    for c in CHECAGENS:
        if sem_sandbox and c["escritas_docs"]:
            resultados.append(dict(c, estado="NAO_EXERCITADO", exit_code=None, segundos=0.0,
                                   timeout=False, erro_lancamento=None, stdout="",
                                   detalhe="reescreve docs curados e o modo --sem-sandbox nao cria copia"))
            continue
        r = aut3_lib.run_cmd(c["cmd"], cwd=sb, timeout=300)
        estado = aut3_lib.avalia(r, c["esperado"])
        resultados.append(dict(
            id=c["id"], classe=c["classe"], mod=c["mod"], desc=c["desc"],
            escritas_docs=c["escritas_docs"], comando=" ".join(c["cmd"]), cwd="<sandbox>",
            exit_code=r["exit_code"], segundos=r["segundos"], timeout=r["timeout"],
            erro_lancamento=r["erro_lancamento"], estado=estado,
            detalhe="" if estado == "OK" else _detalhe(r["stdout"], r["stderr"]),
        ))
    return resultados


def rodar_suite(sb, com_jogo, sem_sandbox=False):
    if sem_sandbox:
        return [dict(id="suite_puros", classe="puro", estado="NAO_EXERCITADO", exit_code=None,
                     comando="roda_testes --puros", segundos=0.0, timeout=False,
                     erro_lancamento=None, detalhe="--sem-sandbox")]
    saida = [dict(id="suite_puros", classe="puro", desc="suite de logica pura (CI)",
                  cmd=[PY, "tools/testes/roda_testes.py", "--puros", "--json"]),
             dict(id="suite_contra_prova", classe="estrutura",
                  desc="prova de fogo do runner (iscas tem de REPROVAR)",
                  cmd=[PY, "tools/testes/roda_testes.py", "--contra-prova", "--json"])]
    if com_jogo:
        saida.append(dict(id="suite_jogo", classe="estrutura",
                          desc="testes que precisam da lib/ do jogo (sem abrir o jogo)",
                          cmd=[PY, "tools/testes/roda_testes.py", "--jogo", "--json"]))
    resultados = []
    for item in saida:
        r = aut3_lib.run_cmd(item["cmd"], cwd=sb, timeout=900)
        estado = aut3_lib.avalia(r, 0)
        try:
            parsed = json.loads(r["stdout"])
        except ValueError:
            parsed = None
        resultados.append(dict(
            id=item["id"], classe=item["classe"], desc=item["desc"],
            comando=" ".join(item["cmd"]), cwd="<sandbox>", exit_code=r["exit_code"],
            segundos=r["segundos"], timeout=r["timeout"], erro_lancamento=r["erro_lancamento"],
            estado=estado, contagem=(parsed or {}).get("contagem"),
            testes=(parsed or {}).get("testes"),
            detalhe="" if estado == "OK" else _detalhe(r["stdout"], r["stderr"]),
        ))
    return resultados


def comparar_estados(repo):
    """Fonte (9 alteracoes) · Release · perfil · pacote — SEPARADOS, so por hash."""
    alterados = [p for p in paths_status(repo) if not p.startswith("scratch/")]
    def h(rel):
        return _sha12(aut3_lib.sha256_file(os.path.join(repo, rel)))
    fonte = {rel: h(rel) for rel in alterados if rel.endswith((".cs", ".csproj", ".json", ".md"))}
    release = {}
    pacote = {}
    for mod in MODS:
        dll_rel = "%s/bin/Release/netstandard2.1/%s.dll" % (mod, mod)
        release[mod] = h(dll_rel)
        zipdll = None
        dist = os.path.join(repo, "dist")
        if os.path.isdir(dist):
            for nome in sorted(os.listdir(dist)):
                if nome.endswith(".zip") and mod in nome:
                    import zipfile
                    try:
                        with zipfile.ZipFile(os.path.join(dist, nome)) as z:
                            alvo = [n for n in z.namelist() if n.endswith("plugins/%s/%s.dll" % (mod, mod))]
                            if alvo:
                                zipdll = aut3_lib.sha256_bytes(z.read(alvo[0]))
                    except (OSError, zipfile.BadZipFile):
                        zipdll = None
        pacote[mod] = dict(sha_zip=_sha12(zipdll), zip_igual_release=(zipdll == aut3_lib.sha256_file(
            os.path.join(repo, dll_rel))) if zipdll else None)
    return {"fonte": fonte, "release": release, "pacote": pacote}


def montar_cobertura(repo, builds, checagens, suites, estados=None, fases_puladas=None):
    fases_puladas = set(fases_puladas or ())
    matriz = os.path.join(repo, "docs", "automacao", "AUT-2-matriz.json")
    if not os.path.isfile(matriz):
        return {"erro": "matriz AUT-2 ausente"}
    with open(matriz, encoding="utf-8") as fh:
        m = json.load(fh)
    bmod = {b["mod"]: b for b in builds}
    pacote = (estados or {}).get("pacote", {})
    itens = []
    for c in m.get("cobertura", []):
        cid = c["id"]
        if cid in RUNTIME:
            itens.append(dict(id=cid, mod=c.get("mod"), estado="NAO_EXERCITADO",
                              evidencia_aut3="", motivo=RUNTIME[cid]))
            continue
        if cid.startswith("M") and cid[1:].isdigit():
            mod = c.get("mod")
            b = bmod.get(mod)
            zip_info = pacote.get(mod) or {}
            zip_rel = ("zip %s do Release" % ("=" if zip_info.get("zip_igual_release") else "!=")
                       if zip_info.get("sha_zip") else "zip ausente")
            if b and b["estado"] == "OK" and b.get("fonte_dll_provada"):
                est = "OK_OFFLINE"
                ev = "build Release 0 erros; fonte->DLL = Release = perfil (%s); %s" % (b["sha_sandbox"], zip_rel)
            elif b and b["estado"] == "OK":
                est = "PARCIAL_OFFLINE"
                ev = "build 0 erros; divergencia fonte/release/perfil: %s/%s/%s" % (
                    b["sha_sandbox"], b["sha_release"], b["sha_perfil"])
            elif b is None and "builds" in fases_puladas:
                est, ev = "NAO_EXERCITADO", "fase de build NAO exercitada nesta rodada"
            else:
                est, ev = "REPROVADO", "build nao passou"
            itens.append(dict(id=cid, mod=mod, estado=est, evidencia_aut3=ev,
                              motivo="publicacao online e validacao em jogo seguem FORA do AUT-3"))
            continue
        if cid == "T-RSTV6":
            rstv = [t for s in suites for t in (s.get("testes") or []) if "rstv" in (t.get("arquivo") or "").lower()]
            estados = {t["estado"] for t in rstv}
            # isca de contra-prova (PROVA_OK) e verde: ela REPROVA de proposito.
            verde = bool(rstv) and estados <= {"PASSOU", "PROVA_OK"}
            est = "OK_OFFLINE" if verde else ("NAO_EXERCITADO" if not rstv else "REPROVADO")
            itens.append(dict(id=cid, mod=c.get("mod"), estado=est,
                              evidencia_aut3="%d testes rstv na suite: %s" % (len(rstv), sorted(estados)),
                              motivo="" if est == "OK_OFFLINE" else "bateria nao verde/no suite"))
            continue
        if cid == "AUT-REUSE":
            # AUT-3F: nada de OK hardcoded - o reuso so e PROVADO se os alvos
            # existirem de fato e a suite tiver rodado.
            alvos = {rel: os.path.isfile(os.path.join(repo, rel))
                     for rel in ("tools/testes/roda_testes.py", "tools/checa_shrines.py")}
            suite_ok = any(s.get("id") in ("suite_puros", "suite_contra_prova")
                           and s.get("estado") == "OK" for s in suites)
            if all(alvos.values()) and suite_ok:
                est = "OK_OFFLINE"
                ev = "reuso PROVADO: roda_testes.py + checa_shrines.py presentes; suite OK"
            else:
                faltas = [k for k, v in alvos.items() if not v]
                if not suite_ok:
                    faltas.append("suite (puros/contra-prova) nao OK")
                est = "NAO_EXERCITADO"
                ev = "sem prova de reuso: %s" % "; ".join(faltas)
            itens.append(dict(id=cid, mod="transversal", estado=est, evidencia_aut3=ev,
                              motivo="CAP-1 exige sessao de jogo autorizada (fora do AUT-3)"))
            continue
        itens.append(dict(id=cid, mod=c.get("mod"), estado="NAO_EXERCITADO",
                          evidencia_aut3="", motivo="criterio nao coberto pelas checagens offline do AUT-3"))
    return dict(matriz_sha=_sha12(aut3_lib.sha256_file(matriz)), itens=itens,
                resumo={e: sum(1 for i in itens if i["estado"] == e)
                        for e in ("OK_OFFLINE", "PARCIAL_OFFLINE", "NAO_EXERCITADO", "REPROVADO")})


def main():
    ap = argparse.ArgumentParser(description="Bancada offline AUT-3 (sem deploy, sem jogo).")
    ap.add_argument("--repo", default=raiz_do_repo())
    ap.add_argument("--ancora", default=None,
                    help="repo REAL cujo caminho a DLL embute via PathMap (padrao: --repo)")
    ap.add_argument("--trabalho", default=None)
    ap.add_argument("--sem-build", action="store_true")
    ap.add_argument("--sem-suite", action="store_true")
    ap.add_argument("--sem-contra-provas", action="store_true")
    ap.add_argument("--jogo", action="store_true", help="inclui a suite que precisa da lib/ do jogo")
    ap.add_argument("--manter-sandbox", action="store_true")
    ap.add_argument("--sem-sandbox", action="store_true", help="modo somente-leitura (pula quem escreve docs)")
    args = ap.parse_args()

    repo = os.path.abspath(args.repo)
    ancora = os.path.abspath(args.ancora) if args.ancora else repo
    trabalho = os.path.abspath(args.trabalho) if args.trabalho else tempfile.mkdtemp(prefix="aut3-")
    os.makedirs(trabalho, exist_ok=True)
    iso = os.path.join(trabalho, "isolamento")
    inicio = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    perfil_antes = snapshot_perfil()
    # AUT-3F2 (A1): guarda de repo FAIL-CLOSED. Se o git nao responde, a leitura
    # "antes" NAO vira {} + intacto: registra o erro, nao builda e nao sai verde.
    repo_antes = None
    guarda_repo_erros = []
    try:
        repo_antes = snapshot_repo(repo)
    except GuardaGitIndisponivel as erro:
        guarda_repo_erros.append("antes: %s" % erro)

    sem_sandbox = args.sem_sandbox
    sb = repo if sem_sandbox else construir_sandbox(repo, trabalho)
    if not sem_sandbox:
        os.environ["AUT3_SANDBOX"] = sb

    # (3) Fase nao exercitada -> NAO_EXERCITADO (nunca verde).
    fases = estados_fases(args, sem_sandbox=sem_sandbox)
    fases_puladas = {f["fase"] for f in fases}

    # (A1) guarda cega NAO builda: sem a leitura do repo, falta a prova de "nao
    # escrevi no repo". A fase de build sai como NAO_EXERCITADO (fail-closed).
    if guarda_repo_erros:
        fases_puladas.add("builds")
        fases_puladas.add("guarda_repo_indisponivel")

    # (1) Opt-in FAIL-CLOSED ANTES de qualquer build.
    preflight = None
    builds = []
    env_iso = montar_env_isolado(iso)
    props_iso = propriedades_isolamento(iso)
    if "builds" not in fases_puladas:
        preflight = preflight_deploy(sb)
        if gate_builds(preflight):
            builds = rodar_builds(sb, repo, ancora, iso)
        else:
            # csproj sem Condition escreveria no perfil: NAO builda (fail-closed).
            fases_puladas.add("optin_bloqueou")

    checagens = rodar_checagens(sb, sem_sandbox=sem_sandbox)
    suites = [] if "suite" in fases_puladas else rodar_suite(sb, args.jogo, sem_sandbox=sem_sandbox)
    contras = [] if "contra_provas" in fases_puladas else cp.executar(sb)

    estados = [dict(estado=b["estado"]) for b in builds] + \
              [dict(estado=c["estado"]) for c in checagens] + \
              [dict(estado=s["estado"]) for s in suites] + \
              [dict(estado="OK" if p["veredito"] == "PROVA_OK" else "REPROVOU") for p in contras] + \
              [dict(estado=f["estado"]) for f in fases]
    if "guarda_repo_indisponivel" in fases_puladas:
        estados.append(dict(estado=aut3_lib.NAO_EXERCITADO))
    if "optin_bloqueou" in fases_puladas:
        estados.append(dict(estado=aut3_lib.REPROVOU))
    veredito = aut3_lib.veredito(estados)

    perfil_depois = snapshot_perfil()
    repo_depois = None
    try:
        repo_depois = snapshot_repo(repo)
    except GuardaGitIndisponivel as erro:
        guarda_repo_erros.append("depois: %s" % erro)

    if repo_antes is None or repo_depois is None:
        # leitura ausente: INDETERMINADO - nunca "intacto" (AUT-3F2/A1).
        comparacao = dict(criados=[], removidos=[], alterados=[], intacto=None)
        repo_intacto = None
    else:
        comparacao = comparar_snapshot(repo_antes, repo_depois)
        repo_intacto = comparacao["intacto"]
    perfil_intacto = perfil_antes == perfil_depois
    if not perfil_intacto or repo_intacto is False:
        veredito = "REPROVADO"

    estados_cobertura = comparar_estados(repo)
    cobertura = montar_cobertura(repo, builds, checagens, suites, estados_cobertura,
                                 fases_puladas=fases_puladas)
    repo_arquivos = None if repo_antes is None else len(repo_antes)
    sha_repo_antes = {} if repo_antes is None else {k: _sha12(v) for k, v in repo_antes.items()}
    sha_repo_depois = {} if repo_depois is None else {k: _sha12(v) for k, v in repo_depois.items()}
    resultado = dict(
        esquema="AUT-3/1", tarefa="t_49075ea4",
        titulo="AUT-3 bancada de revisao estatica e regressao (sem tocar no perfil)",
        gerado_em=inicio, repo=repo,
        git=dict(head=git(repo, "rev-parse", "HEAD"), branch=git(repo, "rev-parse", "--abbrev-ref", "HEAD")),
        nota_metodo=("Execucao REAL e offline: builds Release sem deploy dentro de um sandbox "
                     "(copia do repo) com PathMap sandbox->ancora (repo REAL), ambiente "
                     "USERPROFILE/APPDATA/LOCALAPPDATA isolado e opt-in FAIL-CLOSED antes de "
                     "buildar; conferidores estaticos e suite no sandbox; contra-provas em "
                     "copia isolada. Perfil so medido por hash. NAO abre jogo, NAO instala, "
                     "NAO publica, NAO commita."),
        veredito=veredito,
        ancora=ancora,
        isolamento=dict(base=iso,
                        env={k: v for k, v in env_iso.items()
                             if k in ("USERPROFILE", "APPDATA", "LOCALAPPDATA", "NUGET_PACKAGES")},
                        props=list(props_iso)),
        preflight_deploy=(None if preflight is None else
                          dict(estado=aut3_lib.avalia(preflight, 0), exit_code=preflight["exit_code"],
                               bloqueou=("optin_bloqueou" in fases_puladas),
                               detalhe=_detalhe(preflight["stdout"], preflight["stderr"]))),
        fases_puladas=sorted(fases_puladas),
        guarda_perfil=dict(intacto=perfil_intacto, arquivos=len(perfil_antes),
                           sha_antes={k: _sha12(v) for k, v in perfil_antes.items()},
                           sha_depois={k: _sha12(v) for k, v in perfil_depois.items()}),
        guarda_repo=dict(intacto=repo_intacto, arquivos=repo_arquivos,
                         criados=comparacao["criados"], removidos=comparacao["removidos"],
                         alterados=comparacao["alterados"], erro=guarda_repo_erros,
                         sha_antes=sha_repo_antes, sha_depois=sha_repo_depois),
        estados_separados=estados_cobertura,
        builds=builds, checagens=checagens, suite=suites, contra_provas=contras,
        cobertura=cobertura,
        nao_exercitados=[c["id"] for c in checagens if c["estado"] == "NAO_EXERCITADO"] +
                         [s["id"] for s in suites if s["estado"] == "NAO_EXERCITADO"] +
                         ["fase:" + f["fase"] for f in fases] +
                         [i["id"] for i in cobertura.get("itens", []) if i["estado"] == "NAO_EXERCITADO"],
        builds_executados=len(builds), limite_builds=MAX_BUILDS,
    )
    saida_json = os.path.join(repo, "docs", "automacao", "AUT-3-resultado.json")
    with open(saida_json, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(resultado, fh, ensure_ascii=False, indent=2)
    escrever_resumo(resultado, os.path.join(repo, "docs", "automacao", "AUT-3-resumo.md"))

    if not args.manter_sandbox and not sem_sandbox:
        shutil.rmtree(trabalho, ignore_errors=True)

    print(json.dumps(dict(veredito=veredito, builds=len(builds), checagens=len(checagens),
                          suite=len(suites), contra_provas=len(contras),
                          perfil_intacto=perfil_intacto, repo_intacto=repo_intacto,
                          cobertura=cobertura.get("resumo")), ensure_ascii=False, indent=2))
    return {"VERDE": 0, "REPROVADO": 1, "INCOMPLETO": 2}.get(veredito, 2)


def escrever_resumo(r, caminho):
    linhas = ["# AUT-3 — resumo legivel da bancada offline", "",
              "- gerado: %s" % r["gerado_em"],
              "- git: %s @ %s" % (r["git"]["branch"], r["git"]["head"][:12]),
              "- **veredito: %s**" % r["veredito"],
              "- perfil intacto: **%s** (%d arquivos hasheados)" % (r["guarda_perfil"]["intacto"], r["guarda_perfil"]["arquivos"]),
              "- repo intacto: **%s**" % r["guarda_repo"]["intacto"],
              "- fases puladas: **%s**" % (", ".join(r.get("fases_puladas") or []) or "nenhuma"),
              "- builds: %d/%d (Release, -p:DeployToBepInEx=false)" % (r["builds_executados"], r["limite_builds"]), ""]
    if r["guarda_repo"].get("erro"):
        linhas.append("- guarda de repo NAO exercitada (fail-closed): %s"
                      % "; ".join(r["guarda_repo"]["erro"]))
        linhas.append("")
    linhas += ["## Builds (fonte -> DLL por hash)", "",
               "| mod | estado | fonte=Release=perfil | sha | exit |", "|---|---|---|---|---|"]
    for b in r["builds"]:
        linhas.append("| %s | %s | %s | %s | %s |" % (b["mod"], b["estado"],
                      "SIM" if b.get("fonte_dll_provada") else "NAO", b["sha_sandbox"],
                      b["exit_code"]))
    linhas += ["", "## Conferidores estaticos", "", "| id | classe | escritas_docs | estado | exit | s |",
               "|---|---|---|---|---|---|"]
    for c in r["checagens"]:
        linhas.append("| %s | %s | %s | %s | %s | %s |" % (c["id"], c["classe"],
                      "SIM" if c["escritas_docs"] else "nao", c["estado"], c["exit_code"], c["segundos"]))
    linhas += ["", "## Suite", ""]
    for s in r["suite"]:
        cont = s.get("contagem") or {}
        linhas.append("- **%s** (%s): exit=%s, %s" % (s["id"], s["classe"], s["exit_code"],
                      ", ".join("%s=%s" % (k, v) for k, v in sorted(cont.items()))))
    linhas += ["", "## Contra-provas (copia isolada)", "",
               "| id | familia | defeito exit | apos correcao |", "|---|---|---|---|"]
    for p in r["contra_provas"]:
        linhas.append("| %s | %s | %s | %s |" % (p["id"], p["familia"], p["exit_com_defeito"], p["exit_apos_correcao"]))
    linhas += ["", "## Cobertura alinhada a matriz AUT-2", "",
               "matriz sha %s · %s" % (r["cobertura"].get("matriz_sha"), r["cobertura"].get("resumo")), "",
               "| id | mod | estado AUT-3 | evidencia/motivo |", "|---|---|---|---|"]
    for i in r["cobertura"].get("itens", []):
        linhas.append("| %s | %s | %s | %s |" % (i["id"], i.get("mod"), i["estado"],
                      i.get("evidencia_aut3") or i.get("motivo")))
    linhas += ["", "## Nao exercitado (NAO e OK)", "",
               "- " + "\n- ".join(sorted(set(str(x) for x in r["nao_exercitados"]))), "",
               "> AUT-3 nao substitui aceite humano nem publicacao do DoD."]
    with open(caminho, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(linhas) + "\n")


if __name__ == "__main__":
    sys.exit(main())
