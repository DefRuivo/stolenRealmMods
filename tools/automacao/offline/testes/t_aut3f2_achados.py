#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUT-3F2 (t_2eb1c5db) - testes de COMPORTAMENTO dos 3 achados da AUT-3FR.

Cobre, por comportamento (nao por leitura do relatorio do autor):

  A1. guarda de repo FAIL-CLOSED: quando o git nao responde (dir nao-repo, git
      ausente, timeout) a listagem NAO pode virar {} + "intacto"; o CLI real tem
      de sair NAO-zero registrando NAO_EXERCITADO/REPROVADO, SEM traceback, e
      build nao pode seguir com guarda cega. Repo git VALIDO e VAZIO (exit 0,
      stdout vazio) NAO e erro.
  A2. sanitiza: bloco PEM INTEIRO (inclusive truncado na captura) e atribuicao
      generica (api_key/password/secret/token) quoted/unquoted, preservando o
      contexto; sanitizar ANTES de truncar (nenhum fragmento).
  A3. os testes usam area de trabalho scratch (BH_AGENT_WORKSPACE / TMPDIR /
      LOCALAPPDATA/hermes/cache/scratch), nunca a Temp local do Windows por
      padrao, e propagam TMP/TEMP/TMPDIR.

Credenciais 100% FICTICIAS, montadas por concatenacao.
Uso:  python tools/automacao/offline/testes/t_aut3f2_achados.py
Exit: 0 = tudo passou; 1 = reprovou; 2 = nao consegui rodar.
"""
import contextlib
import io
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.dirname(AQUI)
REPO = os.path.dirname(os.path.dirname(os.path.dirname(LIB_DIR)))
sys.path.insert(0, LIB_DIR)

import aut3_lib      # noqa: E402
import bancada_aut3  # noqa: E402

PY = sys.executable
BANCADA = os.path.join(LIB_DIR, "bancada_aut3.py")
RESULTADOS = []
ARQ_TESTES = ["t_aut3_lib.py", "t_aut3_isolamento.py", "t_aut3_segredos.py",
              "t_aut3_runner.py", "t_aut3f2_achados.py"]
B = "A1b2C3d4E5f6G7h8" + "I9j0K1l2M3n4O5p6" + "Q7r8"   # 40 chars alfanumericos (falso)


def checar(nome, cond, detalhe=""):
    RESULTADOS.append((nome, bool(cond), detalhe))
    print("RESULTADO|%s|%s|%s" % ("PASSOU" if cond else "REPROVOU", nome, detalhe))
    return bool(cond)


def _git(repo, *args):
    return aut3_lib.run_cmd(["git"] + list(args), cwd=repo, timeout=60)


def _repo_git(tmp):
    os.makedirs(tmp, exist_ok=True)
    r = _git(tmp, "init", "-q")
    if r["exit_code"] != 0:
        raise RuntimeError("git init falhou: %s" % (r["stderr"] or r["stdout"]))
    _git(tmp, "config", "user.email", "t@t")
    _git(tmp, "config", "user.name", "t")
    return tmp


# =============================== A1: guarda =================================

def test_a1_nao_repo_levanta(tmp):
    """Dir que NAO e repo: a guarda tem de LEVANTAR (fail-closed), nao devolver {}."""
    nao_repo = os.path.join(tmp, "nao_repo")
    os.makedirs(nao_repo)
    with open(os.path.join(nao_repo, "solto.txt"), "w", encoding="utf-8") as fh:
        fh.write("solto\n")
    levantou = False
    try:
        bancada_aut3.snapshot_repo(nao_repo)
    except bancada_aut3.GuardaGitIndisponivel:
        levantou = True
    checar("A1 dir nao-repo -> GuardaGitIndisponivel (nao {})", levantou)
    # a funcao antiga devolvia {} e o guarda dizia intacto -> agora nunca.
    levantou_lista = False
    try:
        bancada_aut3.lista_repo(nao_repo)
    except bancada_aut3.GuardaGitIndisponivel:
        levantou_lista = True
    checar("A1 lista_repo em nao-repo tambem falha alto", levantou_lista)


def test_a1_git_ausente(tmp):
    """git que nao roda (comando inexistente) -> erro_lancamento -> NAO_EXERCITADO
    e o helper de guarda LEVANTA (fail-closed). Mock so do run_cmd (inevitavel:
    o Windows resolve `git` por App Paths e ignora o PATH)."""
    repo = _repo_git(os.path.join(tmp, "repo_git_ok"))
    # (real) comando inexistente => erro de lancamento, nunca verde
    r_real = aut3_lib.run_cmd(["git-inexistente-aut3f2", "ls-files"], cwd=repo, timeout=30)
    checar("A1 comando git inexistente -> erro_lancamento", bool(r_real.get("erro_lancamento")),
           str(r_real.get("erro_lancamento"))[:80])
    checar("A1 comando git inexistente -> NAO_EXERCITADO",
           aut3_lib.avalia(r_real, 0) == aut3_lib.NAO_EXERCITADO)
    # (mock) run_cmd reportando git ausente => snapshot_repo LEVANTA
    orig = aut3_lib.run_cmd

    def fake(argv, cwd=None, timeout=300, env=None):
        if argv and argv[0] == "git":
            return {"comando": list(argv), "cwd": cwd, "exit_code": None, "segundos": 0.0,
                    "timeout": False, "erro_lancamento": "FileNotFoundError: git ausente",
                    "stdout": "", "stderr": ""}
        return orig(argv, cwd=cwd, timeout=timeout, env=env)

    aut3_lib.run_cmd = fake
    try:
        levantou = False
        try:
            bancada_aut3.snapshot_repo(repo)
        except bancada_aut3.GuardaGitIndisponivel:
            levantou = True
        checar("A1 git ausente (run_cmd) -> GuardaGitIndisponivel", levantou)
    finally:
        aut3_lib.run_cmd = orig


def test_a1_repo_valido_vazio_nao_e_erro(tmp):
    """Repo git VALIDO e VAZIO (exit 0, stdout vazio) NAO e erro: {} e intacto."""
    vazio = _repo_git(os.path.join(tmp, "repo_vazio"))
    try:
        lista = bancada_aut3.lista_repo(vazio)
        snap = bancada_aut3.snapshot_repo(vazio)
        ok = lista == [] and snap == {}
    except bancada_aut3.GuardaGitIndisponivel as erro:
        ok = False
        checar("A1 repo vazio nao levanta", False, str(erro))
        return
    checar("A1 repo git valido+vazio -> [] / {} (nao erro)", ok)
    checar("A1 comparar({},{}) intacto coerente", bancada_aut3.comparar_snapshot(snap, snap)["intacto"] is True)


def _rodar_cli(repo, trabalho, env=None, extra=None):
    cmd = [PY, BANCADA, "--repo", repo, "--trabalho", trabalho,
           "--sem-build", "--sem-suite", "--sem-contra-provas", "--sem-sandbox", "--jogo"]
    if extra:
        cmd += extra
    return aut3_lib.run_cmd(cmd, cwd=REPO, timeout=300, env=env)


def _prep_repo_fake(tmp, nome):
    d = os.path.join(tmp, nome)
    os.makedirs(os.path.join(d, "docs", "automacao"))
    return d


def test_a1_cli_real_nao_repo(tmp):
    """CLI REAL contra dir sem .git: exit NAO-zero, repo_intacto null, sem traceback."""
    repo = _prep_repo_fake(tmp, "cli_nao_repo")
    trabalho = os.path.join(tmp, "cli_nao_repo_trab")
    r = _rodar_cli(repo, trabalho)
    saida = (r["stdout"] or "") + (r["stderr"] or "")
    checar("A1 CLI nao-repo exit != 0", r["exit_code"] not in (0, None), "exit=%s" % r["exit_code"])
    checar("A1 CLI nao-repo: repo_intacto NAO e true (null)",
           '"repo_intacto": null' in (r["stdout"] or ""), (r["stdout"] or "").strip()[-160:])
    checar("A1 CLI nao-repo: sem Traceback opaco", "Traceback" not in saida)
    checar("A1 CLI nao-repo: veredito != VERDE", '"veredito": "VERDE"' not in saida,
           (r["stdout"] or "")[:120])


def test_a1_cli_real_git_ausente(tmp):
    """CLI REAL (processo de verdade) com run_cmd simulando git ausente: exit
    NAO-zero, repo_intacto null, sem traceback. O mock e so do run_cmd - o CLI
    roda inteiro num subprocesso real."""
    repo = _prep_repo_fake(tmp, "cli_sem_git")
    trabalho = os.path.join(tmp, "cli_sem_git_trab")
    wrapper = (
        "import sys; sys.path.insert(0, %r);"
        "import aut3_lib, bancada_aut3;"
        "_orig = aut3_lib.run_cmd\n"
        "def fake(argv, cwd=None, timeout=300, env=None):\n"
        "    if argv and argv[0] == 'git':\n"
        "        return {'comando': list(argv), 'cwd': cwd, 'exit_code': None, 'segundos': 0.0,\n"
        "                'timeout': False, 'erro_lancamento': 'FileNotFoundError: git ausente',\n"
        "                'stdout': '', 'stderr': ''}\n"
        "    return _orig(argv, cwd=cwd, timeout=timeout, env=env)\n"
        "aut3_lib.run_cmd = fake\n"
        "sys.argv = %r\n"
        "sys.exit(bancada_aut3.main())\n"
    ) % (LIB_DIR, [BANCADA, "--repo", repo, "--trabalho", trabalho,
                   "--sem-build", "--sem-suite", "--sem-contra-provas", "--sem-sandbox", "--jogo"])
    r = aut3_lib.run_cmd([PY, "-c", wrapper], cwd=REPO, timeout=300)
    saida = (r["stdout"] or "") + (r["stderr"] or "")
    checar("A1 CLI git ausente exit != 0", r["exit_code"] not in (0, None), "exit=%s" % r["exit_code"])
    checar("A1 CLI git ausente: repo_intacto null", '"repo_intacto": null' in (r["stdout"] or ""),
           (r["stdout"] or "").strip()[-140:])
    checar("A1 CLI git ausente: sem Traceback", "Traceback" not in saida)


def test_a1_falha_na_leitura_depois(tmp):
    """Falha na leitura DEPOIS (mock so aqui): nao pode virar intacto nem verde."""
    repo = _prep_repo_fake(tmp, "cli_depois")
    trabalho = os.path.join(tmp, "cli_depois_trab")
    os.makedirs(trabalho, exist_ok=True)
    cham = {"n": 0}
    orig = bancada_aut3.snapshot_repo

    def fake(_repo):
        cham["n"] += 1
        if cham["n"] == 1:
            return {"a.txt": "hash-fake"}
        raise bancada_aut3.GuardaGitIndisponivel("depois: git sumiu no meio")

    bancada_aut3.snapshot_repo = fake
    argv0 = list(sys.argv)
    buf = io.StringIO()
    try:
        sys.argv = [BANCADA, "--repo", repo, "--trabalho", trabalho,
                    "--sem-build", "--sem-suite", "--sem-contra-provas", "--sem-sandbox", "--jogo"]
        with contextlib.redirect_stdout(buf):
            rc = bancada_aut3.main()
    finally:
        bancada_aut3.snapshot_repo = orig
        sys.argv = argv0
    import json
    with open(os.path.join(repo, "docs", "automacao", "AUT-3-resultado.json"),
              encoding="utf-8") as fh:
        res = json.load(fh)
    checar("A1 falha depois: exit NAO-zero", rc not in (0, None), "rc=%s" % rc)
    checar("A1 falha depois: guarda_repo.intacto NAO e True",
           res["guarda_repo"]["intacto"] is not True, repr(res["guarda_repo"]["intacto"]))
    checar("A1 falha depois: guarda_repo registra erro",
           bool(res["guarda_repo"].get("erro")), repr(res["guarda_repo"].get("erro"))[:120])
    checar("A1 falha depois: sem traceback no stdout", "Traceback" not in buf.getvalue())


# ============================== A2: sanitiza ================================

def test_a2_pem_bloco_inteiro(tmp):
    """Bloco PEM INTEIRO (corpo base64) some, nao so o cabecalho."""
    corpo = "MIIEowIBAAKCAQEA" + B + B
    bloco = "-----BEGIN " + "RSA" + " PRIVATE KEY" + "-----" + chr(10) + corpo
    limpo = aut3_lib.sanitiza("falhou: " + bloco + " (fim)")
    checar("A2 PEM: corpo base64 NAO sobrevive", corpo not in limpo)
    checar("A2 PEM: cabecalho NAO sobrevive", "BEGIN RSA PRIVATE KEY" not in limpo)
    checar("A2 PEM: rodaape NAO sobrevive", "END RSA PRIVATE KEY" not in limpo)
    checar("A2 PEM: preserva contexto", "falhou:" in limpo and "(fim)" in limpo)
    checar("A2 PEM: marca REDACTED", "REDACTED" in limpo)
    # truncado numa captura: sem o rodape
    trunc = "erro: " + "-----BEGIN " + "OPENSSH" + " PRIVATE KEY" + "-----\n%s" % corpo
    limpo2 = aut3_lib.sanitiza(trunc)
    checar("A2 PEM truncado: corpo NAO sobrevive", corpo not in limpo2)
    checar("A2 PEM truncado: preserva o prefixo de contexto", limpo2.startswith("erro:"))


def test_a2_atribuicao_generica(tmp):
    """api_key/password/secret/token em assignment quoted e unquoted."""
    casos = [
        ("api_key_quoted", "api_key = \"%s\"" % B, "api_key"),
        ("password_unquoted", "password = %s" % B, "password"),
        ("secret_dois_pontos", "secret: '%s'" % B, "secret"),
        ("json_api_key", "\"api_key\": \"%s\"" % B, "api_key"),
        ("token_assign", "token=%s" % B, "token"),
        ("client_secret", "client_secret = %s" % B, "client_secret"),
    ]
    for nome, texto, rotulo in casos:
        limpo = aut3_lib.sanitiza("ctx " + texto + " end")
        checar("A2 %s: valor removido" % nome, B not in limpo, limpo)
        checar("A2 %s: rotulo preservado" % nome, rotulo in limpo, limpo)
        checar("A2 %s: contexto preservado" % nome, "ctx" in limpo and "end" in limpo)
        checar("A2 %s: REDACTED" % nome, "REDACTED" in limpo)
    checar("A2 texto normal intacto", aut3_lib.sanitiza("nada de segredo aqui") == "nada de segredo aqui")


def test_a2_sanitiza_antes_de_truncar(tmp):
    """_detalhe sanitiza ANTES de truncar: nenhum fragmento do token escapa."""
    texto = "tss_" + B + "Y" * 570          # 614 chars; corte de 600 comecaria no token
    d = bancada_aut3._detalhe(texto, limite=600)
    checar("A2 _detalhe: valor do token nao aparece", B not in d)
    checar("A2 _detalhe: SUFIXO do token nao aparece (sanitiza antes de cortar)",
           B[-14:] not in d, d[:40])
    d2 = bancada_aut3._detalhe("api_key = %s" % B, limite=600)
    checar("A2 _detalhe: assignment nao vaza", B not in d2)


# =============================== A3: scratch ================================

def test_a3_area_trabalho(tmp):
    """area_trabalho() existe, cria a base e NAO e a Temp local do Windows."""
    checar("A3 aut3_lib.area_trabalho existe", hasattr(aut3_lib, "area_trabalho"))
    if not hasattr(aut3_lib, "area_trabalho"):
        return
    base = aut3_lib.area_trabalho()
    norm = base.replace("\\", "/").lower()
    cand = [os.environ.get("BH_AGENT_WORKSPACE"), os.environ.get("TMPDIR"),
            os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes", "cache", "scratch")]
    cand = [c.replace("\\", "/").lower() for c in cand if c]
    checar("A3 area_trabalho e um diretorio existente", os.path.isdir(base), base)
    checar("A3 area_trabalho sob uma base segura", any(norm == c or norm.startswith(c + "/") for c in cand),
           "%s vs %s" % (norm, cand))
    tempwin = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Temp").replace("\\", "/").lower()
    checar("A3 area_trabalho != Temp local do Windows (LOCALAPPDATA/Temp)",
           norm != tempwin, "%s == %s" % (norm, tempwin))


def test_a3_fallback_localappdata(tmp):
    """Sem BH_AGENT_WORKSPACE/TMPDIR -> LOCALAPPDATA/hermes/cache/scratch."""
    if not hasattr(aut3_lib, "area_trabalho"):
        checar("A3 fallback (area_trabalho ausente)", False)
        return
    guardado = {k: os.environ.get(k) for k in
                ("BH_AGENT_WORKSPACE", "TMPDIR", "TEMP", "TMP", "LOCALAPPDATA")}
    try:
        for k in ("BH_AGENT_WORKSPACE", "TMPDIR"):
            os.environ.pop(k, None)
        os.environ["LOCALAPPDATA"] = tmp
        base = aut3_lib.area_trabalho()
        esperado = os.path.join(tmp, "hermes", "cache", "scratch")
        checar("A3 fallback LOCALAPPDATA/hermes/cache/scratch",
               base.replace("\\", "/") == esperado.replace("\\", "/"), base)
        checar("A3 exporta TMP/TEMP/TMPDIR p/ a base",
               os.environ.get("TMP") == base and os.environ.get("TMPDIR") == base
               and os.environ.get("TEMP") == base)
    finally:
        for k, v in guardado.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v


def test_a3_arquivos_de_teste_usam_scratch(tmp):
    """Os t_aut3_*.py usam TemporaryDirectory(dir=...) - nunca a Temp local."""
    import re as _re
    for nome in ARQ_TESTES:
        caminho = os.path.join(AQUI, nome)
        if not os.path.isfile(caminho):
            checar("A3 %s existe" % nome, False)
            continue
        with open(caminho, encoding="utf-8") as fh:
            texto = fh.read()
        chamadas = _re.findall(r'tempfile\.TemporaryDirectory\s*\(([^)]*)\)', texto)
        sem_dir = [a for a in chamadas if "dir" not in a]
        checar("A3 %s: TemporaryDirectory sempre com dir=" % nome,
               bool(chamadas) and not sem_dir, "sem dir: %s" % sem_dir)


def _guarda(fn, tmp):
    """Roda um teste; excecao inesperada vira REPROVOU (nunca derruba o arquivo)."""
    try:
        fn(tmp)
    except Exception as erro:  # noqa: BLE001 - relatorio, nao engolir
        checar("erro inesperado em %s" % fn.__name__, False, "%s: %s" % (type(erro).__name__, erro))


def main():
    base = aut3_lib.area_trabalho() if hasattr(aut3_lib, "area_trabalho") else None
    with tempfile.TemporaryDirectory(prefix="t-aut3f2-", **({"dir": base} if base else {})) as tmp:
        _guarda(test_a1_nao_repo_levanta, tmp)
        _guarda(test_a1_git_ausente, tmp)
        _guarda(test_a1_repo_valido_vazio_nao_e_erro, tmp)
        _guarda(test_a1_cli_real_nao_repo, tmp)
        _guarda(test_a1_cli_real_git_ausente, tmp)
        _guarda(test_a1_falha_na_leitura_depois, tmp)
        _guarda(test_a2_pem_bloco_inteiro, tmp)
        _guarda(test_a2_atribuicao_generica, tmp)
        _guarda(test_a2_sanitiza_antes_de_truncar, tmp)
        _guarda(test_a3_area_trabalho, tmp)
        _guarda(test_a3_fallback_localappdata, tmp)
        _guarda(test_a3_arquivos_de_teste_usam_scratch, tmp)
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
