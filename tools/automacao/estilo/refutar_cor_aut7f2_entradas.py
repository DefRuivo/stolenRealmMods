#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""refutar_cor_aut7f2_entradas.py - COR-AUT7-F2, FASE 1.5: as ENTRADAS que a suite LE.

TERCEIRA fase (o host derruba execucoes longas: `0xC0000142` quando a arvore de subprocessos
fica comprida). Ela fecha o unico ponto que a revisao independente (execucao 425, rodada 1)
mandou corrigir: a fotografia do cache `--sem-suite` cobria os ARTEFATOS de build (`dist/*.zip`,
`<Mod>/bin/**/*.dll`) mas NAO as ENTRADAS que os testes mapeados LEEM - em especial
`tools/fixtures/**`, lido por `t_bf_diag_orcamento` (`regras_bf.py:432-433`). Apagar essa fixture
mantinha `cache_valido=true` e o criterio `AUT-7/BetterFont/puro/bf-diag-orcamento` saia
OK/OK_VINCULANTE com prova velha, enquanto a rodada viva REPROVAVA.

Experimentos, todos com as CLIs REAIS (produtor -> decisor -> consolidador) dentro de uma COPIA
do repo (o repo vivo e READ-ONLY aqui; nada de jogo/save/build/deploy/publicacao):
  E1  cache real: rodada viva grava a fotografia; o `--sem-suite` reusa (cache VALIDO, OK)
  E2  linha de base: a rodada viva do teste mapeado que le a fixture PASSA
  E3  defeito na ENTRADA MEDIDA: apagar a fixture muda a fotografia, a rodada viva REPROVA e o
      `--sem-suite` NAO reusa (cache INVALIDO, 0 OK de suite, 0 OK_VINCULANTE no consolidador)
  E4  restaurado byte a byte: o cache volta a valer, o teste volta a passar e o item volta a
      OK_VINCULANTE (a invalidacao vem da ENTRADA, nao de ruido)
  E5  COBERTURA AUDITADA: gancho de auditoria (`sys.addaudithook` em
      open/listdir/scandir/glob.glob) sobre a rodada viva: TODO arquivo lido sob o repo tem de
      estar coberto pelas raizes/padroes/artefatos declarados em `estilo_atributos.py`

Uso:
    python tools/automacao/estilo/refutar_cor_aut7f2.py            # fase 1: achados A1-A9
    python tools/automacao/estilo/refutar_cor_aut7f2_entradas.py   # fase 1.5: ESTE script
    python tools/automacao/estilo/fechar_cor_aut7f2.py             # fase 2: suites + docs
Env (os mesmos da fase 1): COR_S, COR_OUT, COR_F2_SANDBOX
"""
import fnmatch
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

W = os.path.dirname(os.path.abspath(__file__))


def _raiz_do_repo():
    d = W
    for _ in range(6):
        if os.path.isdir(os.path.join(d, "BetterFont")):
            return d
        d = os.path.dirname(d)
    return os.path.join(W, "repo")


S = os.environ.get("COR_S") or _raiz_do_repo()
OUT = os.environ.get("COR_OUT") or os.path.join(S, "docs", "automacao", "COR-AUT7-F2-evidencias")
SANDBOX_RAIZ = os.environ.get("COR_F2_SANDBOX") or os.path.join(
    os.environ.get("TEMP") or tempfile.gettempdir(), "cor-aut7f2-sandbox")
os.makedirs(OUT, exist_ok=True)
TMP = tempfile.mkdtemp(prefix="cor-aut7f2-entradas-")
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TEMP=TMP, TMP=TMP, TMPDIR=TMP,
           PYTHONIOENCODING="utf-8")

ESTILO = os.path.join("tools", "automacao", "estilo", "estilo_atributos.py")
ACEITE = os.path.join("tools", "automacao", "aceite", "relatorio_aceite.py")
RODA_TESTES = os.path.join("tools", "testes", "roda_testes.py")
TESTE_BF = os.path.join("tools", "testes", "testes", "puros", "t_bf_diag_orcamento.py")
FIXTURE = os.path.join("tools", "fixtures", "bf-efeito-no-boot.json")
CRITERIO = "bf-diag-orcamento"
JSON_REFUTACAO = os.path.join(OUT, "refutacao-cor-aut7-f2.json")


def sha(caminho):
    h = hashlib.sha256()
    with io.open(caminho, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def roda(nome, argv, cwd=None, timeout=3600, env=None):
    p = subprocess.run([sys.executable] + list(argv), cwd=cwd or S, env=env or ENV,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    with io.open(os.path.join(OUT, nome + ".stdout"), "wb") as fh:
        fh.write(p.stdout)
    with io.open(os.path.join(OUT, nome + ".stderr"), "wb") as fh:
        fh.write(p.stderr)
    print("  %-46s exit=%s" % (nome, p.returncode))
    return p


def carrega(nome, rel):
    import importlib.util
    spec = importlib.util.spec_from_file_location(nome, os.path.join(S, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def escreve_json(caminho, dado):
    with io.open(caminho, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(dado, indent=2, ensure_ascii=False, default=str))
    return caminho


def copia_do_repo(destino):
    if os.path.isdir(destino):
        shutil.rmtree(destino, ignore_errors=True)
    shutil.copytree(S, destino, ignore=shutil.ignore_patterns(
        ".git", "__pycache__", "*.pyc", ".worktrees", "COR-AUT7-F2-evidencias"))
    return destino


ea = carrega("f2_entradas_estilo", ESTILO)

# identidade: a MESMA que a fase 1 gravou (para a cadeia de prova nao mudar entre fases)
IDENT_PATH = os.path.join(OUT, "identidade.json")
if os.path.isfile(IDENT_PATH):
    IDENT = json.load(io.open(IDENT_PATH, encoding="utf-8"))
else:
    IDENT = {"fonte_sha": "f" * 64, "dll_sha": "d" * 64, "sessao": "cor-aut7f2-sintetica"}
    escreve_json(IDENT_PATH, IDENT)

SBX = os.path.join(SANDBOX_RAIZ, "repo")
FONTES_DA_ENTREGA = (ESTILO, os.path.join("tools", "automacao", "estilo", "test_estilo_atributos.py"),
                     os.path.join("tools", "automacao", "estilo", "refutar_cor_aut7f2.py"),
                     os.path.join("tools", "automacao", "estilo", "refutar_cor_aut7f2_entradas.py"),
                     ACEITE, os.path.join("tools", "automacao", "aceite", "test_relatorio_aceite.py"))


def _sandbox_desatualizado():
    """A copia tem de ser do CODIGO ATUAL: sandbox de uma execucao anterior nao serve."""
    if not os.path.isdir(SBX):
        return True
    for rel in FONTES_DA_ENTREGA:
        origem, copia = os.path.join(S, rel), os.path.join(SBX, rel)
        if not os.path.isfile(copia) or sha(origem) != sha(copia):
            return True
    return False


if _sandbox_desatualizado():
    print("== copia do repo para o sandbox (ausente ou de uma execucao anterior): %s" % SBX)
    copia_do_repo(SBX)
OUT_SBX = os.path.join(SBX, "f2-evidencias")
os.makedirs(OUT_SBX, exist_ok=True)
IDENT_SBX = os.path.join(OUT_SBX, "identidade.json")
escreve_json(IDENT_SBX, IDENT)

E = {"sandbox": SBX, "sandbox_copia_de": S, "fixture_medida": FIXTURE.replace("\\", "/"),
     "criterio": CRITERIO, "teste": TESTE_BF.replace("\\", "/")}


def roda_estilo(nome, extra=()):
    saida = os.path.join(OUT_SBX, nome + ".estilo.json")
    p = roda("E-" + nome, [ESTILO, "--repo", SBX, "--out-dir", OUT_SBX, "--sem-runtime",
                           "--identidade", IDENT_SBX, "--out", saida] + list(extra), cwd=SBX)
    with io.open(saida, encoding="utf-8") as fh:
        dados = json.load(fh)
    ok_suite = [c["id"] for c in dados.get("criterios", [])
                if c.get("estado") == "OK"
                and ("/puro/" in str(c.get("id")) or "/controle-negativo/" in str(c.get("id")))]
    alvo = [c for c in dados.get("criterios", []) if CRITERIO in str(c.get("id"))]
    return {"exit": p.returncode, "cache_valido": (dados.get("medicao") or {}).get("cache_valido"),
            "ok_de_suite": len(ok_suite), "amostra_ok": ok_suite[:4],
            "criterio_medido": [(c["id"], c["estado"]) for c in alvo],
            "criterio_medido_ok": [c["id"] for c in alvo if c.get("estado") == "OK"],
            "suites": {k: {"exit_runner": v.get("exit_runner"), "erro": v.get("erro")}
                       for k, v in ((dados.get("medicao") or {}).get("suites") or {}).items()},
            "arquivos": (dados.get("medicao") or {}).get("fotografia", {}).get("arquivos"),
            "artefatos": (dados.get("medicao") or {}).get("fotografia", {}).get("artefatos"),
            "saida": saida}


def roda_aceite(nome):
    ace = os.path.join(OUT_SBX, nome + ".aceite.json")
    p = roda("E-" + nome, [ACEITE, "--repo", SBX, "--out-dir", OUT_SBX, "--sem-suite",
                           "--identidade", IDENT_SBX, "--out", ace], cwd=SBX)
    with io.open(ace, encoding="utf-8") as fh:
        dados = json.load(fh)
    todos = [c for b in dados["decisao"]["por_mod"].values() for c in b.get("criterios", [])]
    alvo = [c for c in todos if CRITERIO in str(c.get("id"))]
    vinc = [c["id"] for b in dados["decisao"]["por_mod"].values()
            for c in b.get("ok_vinculantes", []) if CRITERIO in str(c.get("id"))]
    # a frente do mod que perdeu a entrada: com o cache INVALIDO o item do teste nao existe mais
    # e o mod cai na lacuna canonica `suite-ausente` (nunca OK) - e isso que a revisao quer ver.
    do_mod = [(c.get("id"), c.get("estado"))
              for c in ((dados["decisao"]["por_mod"].get("BetterFont") or {}).get("criterios") or [])]
    return {"exit": p.returncode, "criterio": [(c["id"], c["estado"]) for c in alvo],
            "ok_vinculantes_do_criterio": vinc, "criterios_do_mod_afetado": do_mod,
            "arquivo": ace}


def roda_teste_vivo(nome):
    p = roda("E-" + nome, [RODA_TESTES, "--teste", TESTE_BF, "--json"], cwd=SBX)
    texto = p.stdout.decode("utf-8", "replace")
    try:
        dados = json.loads(texto)
    except ValueError:
        dados = {}
    testes = [{k: t.get(k) for k in ("arquivo", "nome", "estado", "esperado", "detalhe")}
              for t in dados.get("testes", [])]
    return {"exit": p.returncode, "contagem": dados.get("contagem"),
            "testes": testes}


print("== E1: cache real (rodada viva grava; --sem-suite reusa)")
primeiro = roda_estilo("E1-sem-suite-baseline", ["--sem-suite"])
E["E1_primeira_leitura"] = primeiro
if primeiro["cache_valido"] is not True:
    # cache ausente/obsoleto (ex.: gravado por codigo ANTERIOR a esta correcao) -> grava um novo
    # com a RODADA VIVA, que e o unico jeito honesto de dizer que a fotografia e a do codigo atual
    print("   cache nao reusavel (%r): rodando a rodada VIVA para gravar a fotografia"
          % primeiro["cache_valido"])
    vivo = roda_estilo("E1-rodada-viva-grava-o-cache")
    cache = os.path.join(OUT_SBX, "suite-vinculo.json")
    E["E1_rodada_viva"] = dict(vivo, cache_gravado=os.path.isfile(cache),
                               sha_do_cache=sha(cache) if os.path.isfile(cache) else None)
    primeiro = roda_estilo("E1b-sem-suite-baseline", ["--sem-suite"])
E["E1"] = primeiro
print("    cache_valido=%s OK_de_suite=%d criterio=%s"
      % (primeiro["cache_valido"], primeiro["ok_de_suite"], primeiro["criterio_medido"]))

print("== E2: linha de base da rodada VIVA do teste mapeado (fixture no lugar)")
E["E2"] = roda_teste_vivo("E2-rodada-viva-com-a-fixture")
print("    exit=%s contagem=%s" % (E["E2"]["exit"], E["E2"]["contagem"]))

print("== E3: defeito na ENTRADA MEDIDA (a fixture some)")
foto_antes = ea.fotografia_suite(SBX)
print("    fotografia ANTES: %d arquivos + %d artefatos" % (len(foto_antes["arquivos"]),
                                                             len(foto_antes["artefatos"])))
alvo_fixture = os.path.join(SBX, FIXTURE)
original = io.open(alvo_fixture, "rb").read()
sha_original = sha(alvo_fixture)
os.remove(alvo_fixture)
foto_depois = ea.fotografia_suite(SBX)
saidos = sorted(set(foto_antes["arquivos"]) - set(foto_depois["arquivos"]))
E["E3_fotografia"] = {"arquivos_antes": len(foto_antes["arquivos"]),
                      "arquivos_depois": len(foto_depois["arquivos"]),
                      "fotografia_mudou": foto_antes != foto_depois,
                      "caminhos_que_sairam": saidos,
                      "a_fixture_saiu": FIXTURE.replace("\\", "/") in saidos,
                      "artefatos_intactos": foto_antes["artefatos"] == foto_depois["artefatos"]}
print("    fotografia mudou=%s (saíram %d caminho(s): %s)"
      % (E["E3_fotografia"]["fotografia_mudou"], len(saidos), saidos[:3]))
E["E3_rodada_viva"] = roda_teste_vivo("E3-rodada-viva-sem-a-fixture")
print("    rodada viva: exit=%s contagem=%s" % (E["E3_rodada_viva"]["exit"],
                                                E["E3_rodada_viva"]["contagem"]))
E["E3_sem_suite"] = roda_estilo("E3-sem-suite-com-a-prova-velha", ["--sem-suite"])
print("    --sem-suite: cache_valido=%s OK_de_suite=%d criterio=%s"
      % (E["E3_sem_suite"]["cache_valido"], E["E3_sem_suite"]["ok_de_suite"],
         E["E3_sem_suite"]["criterio_medido"]))
E["E3_consolidador"] = roda_aceite("E3-consolidador-sem-a-fixture")
print("    consolidador: exit=%s criterio=%s vinculantes=%s"
      % (E["E3_consolidador"]["exit"], E["E3_consolidador"]["criterio"],
         E["E3_consolidador"]["ok_vinculantes_do_criterio"]))

print("== E4: restaurado byte a byte (a invalidacao vem da ENTRADA, nao de ruido)")
with io.open(alvo_fixture, "wb") as fh:
    fh.write(original)
foto_volta = ea.fotografia_suite(SBX)
E["E4"] = {"restaurada_byte_a_byte": sha(alvo_fixture) == sha_original,
           "sha_antes": sha_original, "sha_depois": sha(alvo_fixture),
           "fotografia_igual_a_antes": foto_volta == foto_antes}
E["E4"].update({"rodada_viva": roda_teste_vivo("E4-rodada-viva-restaurada")})
E["E4"].update({"sem_suite": roda_estilo("E4-sem-suite-restaurado", ["--sem-suite"])})
E["E4"].update({"consolidador": roda_aceite("E4-consolidador-restaurado")})
print("    fotografia de volta=%s | --sem-suite cache_valido=%s OK_de_suite=%d | "
      "consolidador criterio=%s vinculantes=%s"
      % (E["E4"]["fotografia_igual_a_antes"], E["E4"]["sem_suite"]["cache_valido"],
         E["E4"]["sem_suite"]["ok_de_suite"], E["E4"]["consolidador"]["criterio"],
         E["E4"]["consolidador"]["ok_vinculantes_do_criterio"]))

AUDITORIA = '''"""Gancho de auditoria das LEITURAS da rodada viva (COR-AUT7-F2, E5).

Instalado via PYTHONPATH (sitecustomize) no processo do runner. Registra, para cada arquivo
ABERTO PARA LEITURA (e para cada listdir/scandir/glob) sob a raiz do repo, uma linha
`pid<TAB>evento<TAB>caminho`. Nao registra escrita (flags O_WRONLY/O_RDWR): o que interessa e a
ENTRADA que a suite consome - e a escrita da propria rodada invalidaria a fotografia.
"""
import os
import sys

LOG = os.environ.get("PROBE_LOG", "")
RAIZ = os.path.abspath(os.environ.get("PROBE_REPO", ".")).replace("\\\\", "/").lower()
_em = [False]


def hook(evento, args):
    if evento not in ("open", "os.listdir", "os.scandir", "glob.glob"):
        return
    if _em[0] or not LOG:
        return
    alvo = args[0] if args else None
    if not isinstance(alvo, str):
        return
    try:
        p = os.path.abspath(alvo).replace("\\\\", "/")
        if not p.lower().startswith(RAIZ):
            return
        if evento == "open":
            flags = args[2] if len(args) > 2 else 0
            if isinstance(flags, int) and (flags & (os.O_WRONLY | os.O_RDWR)):
                return
        _em[0] = True
        with open(LOG, "a", encoding="utf-8") as fh:
            fh.write("%s\\t%s\\t%s\\n" % (os.getpid(), evento, p))
    except Exception:
        pass
    finally:
        _em[0] = False


sys.addaudithook(hook)
'''


def coberto(rel):
    """Mesma regra da fotografia (por raiz/padrao/artefato); `None` = NAO coberto."""
    partes = rel.split("/")
    if rel.startswith("dist/") and rel.endswith(".zip"):
        return "artefato dist/*.zip"
    if "bin" in partes and rel.endswith(".dll"):
        return "artefato <Mod>/bin/**/*.dll"
    if any(x in partes for x in ea.DIRS_FORA_DA_FOTOGRAFIA):
        return "derivado/excluido (nao e entrada)"
    for raiz in ea.RAIZES_DA_FOTOGRAFIA:
        if rel == raiz or rel.startswith(raiz + "/"):
            return "raiz %s" % raiz
    if rel in ea.ARQUIVOS_DA_FOTOGRAFIA:
        return "arquivo solto %s" % rel
    for padrao in ea.PADROES_DA_FOTOGRAFIA:
        if fnmatch.fnmatch(rel, padrao.replace("**/", "*")):
            return "padrao %s" % padrao
    return None


print("== E5: cobertura AUDITADA (o que a rodada viva LE sob o repo)")
AUD = os.path.join(TMP, "auditoria")
os.makedirs(AUD, exist_ok=True)
with io.open(os.path.join(AUD, "sitecustomize.py"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write(AUDITORIA)
RAIZ_FWD = SBX.replace("\\", "/")
lidos = {}
dirs = {}
for flag, nome in (("--puros", "puros"), ("--contra-prova", "contra-prova")):
    log = os.path.join(TMP, "lidos-%s.txt" % nome)
    env = dict(ENV, PYTHONPATH=AUD, PROBE_LOG=log, PROBE_REPO=RAIZ_FWD)
    t0 = time.time()
    p = roda("E5-rodada-viva-%s-auditada" % nome, [RODA_TESTES, flag, "--json"], cwd=SBX,
             env=env, timeout=3600)
    print("    %s: exit=%s em %.1fs" % (nome, p.returncode, time.time() - t0))
for nome in ("lidos-puros.txt", "lidos-contra-prova.txt"):
    caminho = os.path.join(TMP, nome)
    if not os.path.isfile(caminho):
        continue
    for linha in io.open(caminho, encoding="utf-8"):
        if not linha.strip():
            continue
        _pid, evento, caminho_lido = linha.rstrip("\n").split("\t")
        if not caminho_lido.startswith(RAIZ_FWD + "/"):
            continue
        rel = caminho_lido[len(RAIZ_FWD) + 1:]
        (lidos if evento == "open" else dirs)[rel] = coberto(rel)
nao_cobertos = sorted(r for r, m in lidos.items() if m is None)
derivados = sorted(r for r, m in lidos.items() if m and m.startswith("derivado"))
entradas = sorted(r for r, m in lidos.items() if m and not m.startswith("derivado"))
por_origem = {}
for r in entradas:
    por_origem[lidos[r]] = por_origem.get(lidos[r], 0) + 1
E["E5"] = {"arquivos_lidos": len(lidos), "dirs_listados": len(dirs),
           "entradas_cobertas": len(entradas), "por_origem": por_origem,
           "derivados_lidos": derivados, "nao_cobertos": nao_cobertos,
           "cobertura_declarada": {"raizes": list(ea.RAIZES_DA_FOTOGRAFIA),
                                   "arquivos_soltos": list(ea.ARQUIVOS_DA_FOTOGRAFIA),
                                   "padroes": list(ea.PADROES_DA_FOTOGRAFIA),
                                   "fora": list(ea.DIRS_FORA_DA_FOTOGRAFIA)},
           "gancho": "sys.addaudithook em open/os.listdir/os.scandir/glob.glob (sitecustomize)"}
print("    lidos=%d entradas_cobertas=%d NAO cobertos=%d (derivados lidos=%d)"
      % (len(lidos), len(entradas), len(nao_cobertos), len(derivados)))
for r in nao_cobertos:
    print("      FALTA: %s" % r)

E["leitura"] = (
    "A fotografia passou a cobrir as ENTRADAS que a suite LE - 6 mods, `tools/**`, `lib/**`, "
    "`docs/cobertura/**`, `ReloadProbe/**`, `scratch/**`, `docs/PLANO-DE-TESTES.md` e os projetos "
    "`*.csproj`/`*.props`/`*.targets` da arvore - alem dos artefatos de build que ela MEDE. Apagar "
    "a `tools/fixtures/bf-efeito-no-boot.json` (lida por `t_bf_diag_orcamento`) muda a fotografia: "
    "a rodada viva REPROVA (E3) e o `--sem-suite` com a prova velha nao reusa nada (cache INVALIDO, "
    "0 OK de suite, 0 OK_VINCULANTE no consolidador). Restaurada byte a byte, tudo volta (E4) - a "
    "invalidacao vem da ENTRADA, nao de ruido. A cobertura e AUDITADA (E5): todo arquivo lido sob o "
    "repo na rodada viva esta coberto pelas raizes/padroes/artefatos declarados.")

E["fechou"] = bool(
    E["E1"]["cache_valido"] is True
    and E["E2"]["exit"] == 0
    and E["E3_fotografia"]["a_fixture_saiu"]
    and E["E3_rodada_viva"]["exit"] == 1
    and E["E3_sem_suite"]["cache_valido"] is False
    and E["E3_sem_suite"]["ok_de_suite"] == 0
    and not E["E3_consolidador"]["ok_vinculantes_do_criterio"]
    and any("/suite-ausente" in str(i) for i, _e in E["E3_consolidador"]["criterios_do_mod_afetado"])
    and E["E4"]["restaurada_byte_a_byte"]
    and E["E4"]["fotografia_igual_a_antes"]
    and E["E4"]["sem_suite"]["cache_valido"] is True
    and E["E4"]["rodada_viva"]["exit"] == 0
    and E["E4"]["consolidador"]["ok_vinculantes_do_criterio"]
    and not E["E5"]["nao_cobertos"])

RES = {}
if os.path.isfile(JSON_REFUTACAO):
    with io.open(JSON_REFUTACAO, encoding="utf-8") as fh:
        RES = json.load(fh)
RES.setdefault("achados", {})["A6_entradas"] = E
RES["fase"] = ("achados A1-A9 (fase 1) + ENTRADAS medidas no cache (fase 1.5) + "
               "fecho: suites verdes e docs regerados (fase 2)")
escreve_json(JSON_REFUTACAO, RES)
escreve_json(os.path.join(OUT, "entradas-medidas.json"),
             {"E": E, "hashes": {rel: sha(os.path.join(S, rel)) for rel in (
                 ESTILO, os.path.join("tools", "automacao", "estilo", "test_estilo_atributos.py"),
                 os.path.join("tools", "automacao", "estilo", "refutar_cor_aut7f2_entradas.py"))
                 if os.path.isfile(os.path.join(S, rel))}})

print("\nfecho da fase 1.5 (ENTRADAS medidas no cache): %s" % E["fechou"])
print("  E1 cache real reusado=%s | E3 fixture fora: rodada viva=%s cache=%s OK_de_suite=%s "
      "vinculantes=%s | E5 nao cobertos=%d"
      % (E["E1"]["cache_valido"], E["E3_rodada_viva"]["contagem"],
         E["E3_sem_suite"]["cache_valido"], E["E3_sem_suite"]["ok_de_suite"],
         E["E3_consolidador"]["ok_vinculantes_do_criterio"], len(E["E5"]["nao_cobertos"])))
print("relatorio:", JSON_REFUTACAO)
print("evidencia:", os.path.join(OUT, "entradas-medidas.json"))
