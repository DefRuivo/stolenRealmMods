#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testes de isolamento, guarda de repo e veredito da bancada AUT-3 (AUT-3F).

Cobrem TRES dos quatro achados da AUT-3R que nao se respondem so com build:

  1. isolamento dos builds (USERPROFILE/APPDATA/LOCALAPPDATA + props MSBuild) e a
     guarda de opt-in FAIL-CLOSED antes de qualquer build;
  2. snapshot do repo com tracked+untracked RECURSIVOS e deteccao de
     criado/removido/alterado, excluindo SO os outputs autorizados;
  3. veredito: fase pulada (--sem-build / --sem-suite / suite_jogo omitida)
     NUNCA vira VERDE, e criterio runtime nao declarado nao vira OK.

O quarto achado (prefixo de credencial) fica em t_aut3_segredos.py.

Uso:  python tools/automacao/offline/testes/t_aut3_isolamento.py
Exit: 0 = tudo passou; 1 = alguma verificacao reprovou; 2 = nao consegui rodar.
"""
import os
import shutil
import sys
import tempfile
import types

AQUI = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.dirname(AQUI)
sys.path.insert(0, LIB_DIR)
REPO_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(LIB_DIR)))

import aut3_lib      # noqa: E402
import bancada_aut3  # noqa: E402

RESULTADOS = []
PY = sys.executable


def checar(nome, cond, detalhe=""):
    RESULTADOS.append((nome, bool(cond), detalhe))
    print("RESULTADO|%s|%s|%s" % ("PASSOU" if cond else "REPROVOU", nome, detalhe))
    return bool(cond)


def _git(repo, *args):
    r = aut3_lib.run_cmd(["git"] + list(args), cwd=repo, timeout=60)
    return r


def _repo_de_teste(tmp):
    """Cria um repo git minimo com tracked, untracked recursivo, e um ignorado."""
    os.makedirs(tmp, exist_ok=True)
    r = _git(tmp, "init", "-q")
    if r["exit_code"] != 0:
        raise RuntimeError("git init falhou: %s" % (r["stderr"] or r["stdout"]))
    _git(tmp, "config", "user.email", "t@t")
    _git(tmp, "config", "user.name", "t")
    with open(os.path.join(tmp, ".gitignore"), "w", encoding="utf-8") as fh:
        fh.write("bin/\n__pycache__/\n")
    with open(os.path.join(tmp, "a.txt"), "w", encoding="utf-8") as fh:
        fh.write("rastreado\n")
    os.makedirs(os.path.join(tmp, "tools", "automacao", "offline"), exist_ok=True)
    with open(os.path.join(tmp, "tools", "automacao", "offline", "x.py"), "w", encoding="utf-8") as fh:
        fh.write("novo\n")
    os.makedirs(os.path.join(tmp, "docs", "automacao"), exist_ok=True)
    with open(os.path.join(tmp, "docs", "automacao", "AUT-3-resultado.json"), "w", encoding="utf-8") as fh:
        fh.write("{}\n")
    os.makedirs(os.path.join(tmp, "scratch"), exist_ok=True)
    with open(os.path.join(tmp, "scratch", "suja.txt"), "w", encoding="utf-8") as fh:
        fh.write("fora do nosso escopo\n")
    os.makedirs(os.path.join(tmp, "bin"), exist_ok=True)
    with open(os.path.join(tmp, "bin", "ignorado.txt"), "w", encoding="utf-8") as fh:
        fh.write("ignorado pelo .gitignore\n")
    _git(tmp, "add", ".gitignore", "a.txt")
    return tmp


# --------------------------- 1. isolamento dos builds -----------------------

def test_env_isolado(tmp):
    base = os.path.join(tmp, "iso")
    env = bancada_aut3.montar_env_isolado(base)
    checar("USERPROFILE isolado sob a base",
           env.get("USERPROFILE", "").replace("\\", "/").startswith(base.replace("\\", "/")),
           env.get("USERPROFILE", ""))
    checar("APPDATA isolado sob a base",
           env.get("APPDATA", "").replace("\\", "/").startswith(base.replace("\\", "/")))
    checar("LOCALAPPDATA isolado sob a base",
           env.get("LOCALAPPDATA", "").replace("\\", "/").startswith(base.replace("\\", "/")))
    real = os.environ.get("USERPROFILE", "")
    checar("nao aponta para o USERPROFILE real",
           bool(real) and env.get("USERPROFILE") != real)

    # cache NuGet real PRESERVADO (sem ele o restore pode falhar dentro do isolamento)
    fake_user = os.path.join(tmp, "userfake")
    fake_nuget = os.path.join(fake_user, ".nuget", "packages")
    os.makedirs(fake_nuget, exist_ok=True)
    env2 = bancada_aut3.montar_env_isolado(os.path.join(tmp, "iso2"), real=fake_user)
    checar("NUGET_PACKAGES preserva o cache real quando existe",
           env2.get("NUGET_PACKAGES", "").replace("\\", "/") == fake_nuget.replace("\\", "/"),
           env2.get("NUGET_PACKAGES", ""))


def test_props_isolamento(tmp):
    base = os.path.join(tmp, "isop")
    props = bancada_aut3.propriedades_isolamento(base)
    texto = " ".join(props).replace("\\", "/")
    checar("props contem -p:USERPROFILE", any(p.startswith("-p:USERPROFILE=") for p in props))
    checar("props contem -p:APPDATA", any(p.startswith("-p:APPDATA=") for p in props))
    checar("props contem -p:LOCALAPPDATA", any(p.startswith("-p:LOCALAPPDATA=") for p in props))
    checar("props ancoram na base", base.replace("\\", "/") in texto)


def test_gate_fail_closed(tmp):
    ruim = aut3_lib.run_cmd([PY, "-c", "import sys; sys.exit(1)"])
    bom = aut3_lib.run_cmd([PY, "-c", "import sys; sys.exit(0)"])
    checar("opt-in reprovado -> NAO builda (fail-closed)",
           bancada_aut3.gate_builds(ruim) is False)
    checar("opt-in OK -> pode buildar", bancada_aut3.gate_builds(bom) is True)


# ------------------------- 2. snapshot tracked+untracked --------------------

def test_lista_repo_recursiva(tmp):
    repo = _repo_de_teste(os.path.join(tmp, "repo"))
    rels = [p.replace("\\", "/") for p in bancada_aut3.lista_repo(repo)]
    checar("tracked entra", "a.txt" in rels)
    checar("untracked RECURSIVO entra (dir novo nao colapsa)",
           "tools/automacao/offline/x.py" in rels)
    checar("output autorizado (AUT-3-resultado.json) fica FORA",
           "docs/automacao/AUT-3-resultado.json" not in rels)
    checar("scratch/ fica FORA (area de trabalho externa)",
           all(not p.startswith("scratch/") for p in rels))
    checar("arquivo ignorado fica fora (--exclude-standard)",
           all(not p.startswith("bin/") for p in rels))


def test_comparar_snapshot(tmp):
    antes = {"a": "1", "b": "2", "c": "3"}
    depois = {"a": "1", "b": "X", "d": "4"}
    comp = bancada_aut3.comparar_snapshot(antes, depois)
    checar("detecta ALTERADO", comp["alterados"] == ["b"])
    checar("detecta CRIADO", comp["criados"] == ["d"])
    checar("detecta REMOVIDO", comp["removidos"] == ["c"])
    checar("nao intacto quando muda", comp["intacto"] is False)
    igual = bancada_aut3.comparar_snapshot({"a": "1"}, {"a": "1"})
    checar("intacto quando igual", igual["intacto"] is True)


def test_snapshot_repo_hash(tmp):
    repo = _repo_de_teste(os.path.join(tmp, "repo2"))
    snap = bancada_aut3.snapshot_repo(repo)
    checar("snapshot hasheia o untracked recursivo",
           snap.get("tools\\automacao\\offline\\x.py") is not None
           or snap.get("tools/automacao/offline/x.py") is not None)
    checar("snapshot NAO tem o output autorizado",
           all("AUT-3-resultado" not in k for k in snap))


# ----------------------------- 3. veredito/fases ----------------------------

def test_estados_fases():
    def args(**kw):
        base = dict(sem_build=False, sem_suite=False, sem_sandbox=False,
                    sem_contra_provas=False, jogo=True)
        base.update(kw)
        return types.SimpleNamespace(**base)

    checar("sem fases puladas -> nenhum estado extra",
           bancada_aut3.estados_fases(args()) == [])
    for nome, kw in (("--sem-build", dict(sem_build=True)),
                     ("--sem-suite", dict(sem_suite=True)),
                     ("suite_jogo omitida (sem --jogo)", dict(jogo=False)),
                     ("--sem-contra-provas", dict(sem_contra_provas=True)),
                     ("--sem-sandbox", dict(sem_sandbox=True))):
        est = bancada_aut3.estados_fases(args(**kw))
        so_nao = bool(est) and all(e["estado"] == aut3_lib.NAO_EXERCITADO for e in est)
        checar("%s -> NAO_EXERCITADO" % nome, so_nao, str(est))
        checar("%s nunca VERDE" % nome, aut3_lib.veredito(est) != "VERDE")


def test_criterio_runtime_nao_declarado(tmp):
    matriz = {"cobertura": [
        {"id": "M1", "mod": "BetterFont"},
        {"id": "X-FUTURO-RUNTIME", "mod": "RoguelikeSkillTreeVisualizer"},
        {"id": "AUT-REUSE", "mod": "transversal"},
    ]}
    repo = os.path.join(tmp, "cov")
    os.makedirs(os.path.join(repo, "docs", "automacao"))
    import json
    with open(os.path.join(repo, "docs", "automacao", "AUT-2-matriz.json"), "w",
              encoding="utf-8") as fh:
        json.dump(matriz, fh)
    builds = [{"mod": "BetterFont", "estado": "OK", "fonte_dll_provada": True, "sha_sandbox": "abcd"}]
    cob = bancada_aut3.montar_cobertura(repo, builds, [], [])
    por_id = {i["id"]: i for i in cob["itens"]}
    checar("M1 build provado -> OK_OFFLINE", por_id["M1"]["estado"] == "OK_OFFLINE")
    checar("criterio NAO declarado nao vira OK", por_id["X-FUTURO-RUNTIME"]["estado"] == "NAO_EXERCITADO")
    checar("AUT-REUSE sem prova de reuso -> NAO_EXERCITADO",
           por_id["AUT-REUSE"]["estado"] == "NAO_EXERCITADO",
           por_id["AUT-REUSE"]["estado"])


def test_builds_pulados_nao_reprovam(tmp):
    """--sem-build: M* e NAO_EXERCITADO (fase pulada), nao REPROVADO."""
    matriz = {"cobertura": [{"id": "M1", "mod": "BetterFont"}]}
    repo = os.path.join(tmp, "cov2")
    os.makedirs(os.path.join(repo, "docs", "automacao"))
    import json
    with open(os.path.join(repo, "docs", "automacao", "AUT-2-matriz.json"), "w",
              encoding="utf-8") as fh:
        json.dump(matriz, fh)
    cob = bancada_aut3.montar_cobertura(repo, [], [], [], fases_puladas={"builds"})
    checar("M* com build pulado -> NAO_EXERCITADO",
           cob["itens"][0]["estado"] == "NAO_EXERCITADO", cob["itens"][0]["estado"])


def test_aut_reuse_derivado(tmp):
    """AUT-REUSE so e OK_OFFLINE se os alvos de REUSO existirem e a suite tiver rodado."""
    import json
    matriz = {"cobertura": [{"id": "AUT-REUSE", "mod": "transversal"}]}
    repo = os.path.join(tmp, "reuse")
    os.makedirs(os.path.join(repo, "docs", "automacao"))
    os.makedirs(os.path.join(repo, "tools", "testes"))
    with open(os.path.join(repo, "docs", "automacao", "AUT-2-matriz.json"), "w",
              encoding="utf-8") as fh:
        json.dump(matriz, fh)
    suites = [{"id": "suite_puros", "estado": "OK", "testes": []}]
    sem = bancada_aut3.montar_cobertura(repo, [], [], suites)
    checar("sem os arquivos de reuso -> NAO_EXERCITADO",
           sem["itens"][0]["estado"] == "NAO_EXERCITADO")
    with open(os.path.join(repo, "tools", "testes", "roda_testes.py"), "w", encoding="utf-8") as fh:
        fh.write("# alvo de reuso\n")
    with open(os.path.join(repo, "tools", "checa_shrines.py"), "w", encoding="utf-8") as fh:
        fh.write("# alvo de reuso\n")
    com = bancada_aut3.montar_cobertura(repo, [], [], suites)
    checar("com reuso provado -> OK_OFFLINE", com["itens"][0]["estado"] == "OK_OFFLINE",
           com["itens"][0]["estado"])


def test_detalhe_sanitizado(tmp):
    tok = "tss_" + "A1b2C3d4E5f6G7h8I9j0K1l2"
    d = bancada_aut3._detalhe("erro: %s no arquivo" % tok)
    checar("_detalhe NAO vaza o token", tok not in d)
    checar("_detalhe marca REDACTED", "<REDACTED>" in d)
    checar("_detalhe preserva o contexto de falha", "no arquivo" in d)


CSPROJ_RUIM = """<Project Sdk="Microsoft.NET.Sdk">
  <Target Name="DeployToBepInEx" AfterTargets="Build">
    <Copy SourceFiles="$(TargetPath)" DestinationFolder="$(USERPROFILE)\\AppData\\Roaming\\r2modmanPlus-local\\X\\" />
  </Target>
</Project>
"""
CSPROJ_BOM = """<Project Sdk="Microsoft.NET.Sdk">
  <Target Name="DeployToBepInEx" AfterTargets="Build" Condition="'$(DeployToBepInEx)' == 'true'">
    <Copy SourceFiles="$(TargetPath)" DestinationFolder="$(USERPROFILE)\\AppData\\Roaming\\r2modmanPlus-local\\X\\" />
  </Target>
</Project>
"""


def test_preflight_fail_closed_real(tmp):
    """CONTRA-PROVA real: csproj de deploy SEM Condition -> preflight REPROVA e gate NAO builda."""
    repo = os.path.join(tmp, "pf")
    os.makedirs(os.path.join(repo, "tools"))
    shutil.copyfile(os.path.join(REPO_RAIZ, "tools", "check_deploy_optin.py"),
                    os.path.join(repo, "tools", "check_deploy_optin.py"))
    alvo = os.path.join(repo, "X", "X.csproj")
    os.makedirs(os.path.dirname(alvo))
    with open(alvo, "w", encoding="utf-8") as fh:
        fh.write(CSPROJ_RUIM)
    r = bancada_aut3.preflight_deploy(repo)
    checar("preflight REPROVA csproj sem opt-in", aut3_lib.avalia(r, 0) == aut3_lib.REPROVOU,
           "exit=%s" % r["exit_code"])
    checar("FAIL-CLOSED: csproj sem opt-in NAO builda", bancada_aut3.gate_builds(r) is False)
    with open(alvo, "w", encoding="utf-8") as fh:
        fh.write(CSPROJ_BOM)
    r2 = bancada_aut3.preflight_deploy(repo)
    checar("preflight APROVA csproj com opt-in", bancada_aut3.gate_builds(r2) is True,
           "exit=%s" % r2["exit_code"])


def main():
    with tempfile.TemporaryDirectory(prefix="t-aut3-iso-", dir=aut3_lib.area_trabalho()) as tmp:
        test_env_isolado(tmp)
        test_props_isolamento(tmp)
        test_gate_fail_closed(tmp)
        test_lista_repo_recursiva(tmp)
        test_comparar_snapshot(tmp)
        test_snapshot_repo_hash(tmp)
        test_estados_fases()
        test_criterio_runtime_nao_declarado(tmp)
        test_builds_pulados_nao_reprovam(tmp)
        test_aut_reuse_derivado(tmp)
        test_detalhe_sanitizado(tmp)
        test_preflight_fail_closed_real(tmp)
    falhas = [n for n, ok, _ in RESULTADOS if not ok]
    print()
    print("total: %d | falhas: %d" % (len(RESULTADOS), len(falhas)))
    if falhas:
        print("REPROVADAS: %s" % ", ".join(falhas))
        return 1
    print("TUDO OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
