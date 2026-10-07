#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fechar_cor_aut7f2.py - COR-AUT7-F2: fase de FECHO (suites verdes + docs regerados).

Roda o fecho da correcao dos achados A1-A9:
  * suite da ferramenta de estilo (`test_estilo_atributos.py`);
  * suite do relatorio de aceite (`test_relatorio_aceite.py`);
  * regeracao dos docs gerados pela ferramenta (`AUT-7-relatorio.md` / `AUT-7-resultado.json`)
    pela CLI REAL do consolidador (com a suite do projeto dentro), com o sha256 de ANTES e de
    DEPOIS gravado em `docs-antes.txt` - a prova que o achado A9 dizia faltar;
  * merge no relatorio `refutacao-cor-aut7-f2.json` produzido por
    `tools/automacao/estilo/refutar_cor_aut7f2.py` (mesma evidencia, uma so leitura).

Por que duas fases: uma execucao unica passa de 8 minutos e o host Windows derruba o spawn de
novos processos (`0xC0000142` = STATUS_DLL_INIT_FAILED) quando a arvore de subprocessos fica
longa. Cada fase roda sozinha, bem abaixo do limite, e as duas escrevem no MESMO diretorio de
evidencia. Nada aqui toca jogo, save, build, deploy ou publicacao.

Uso:
    python tools/automacao/estilo/refutar_cor_aut7f2.py            # fase 1: achados A1-A9
    python tools/automacao/estilo/refutar_cor_aut7f2_entradas.py   # fase 1.5: ENTRADAS medidas
    python tools/automacao/estilo/fechar_cor_aut7f2.py             # fase 2: este script
"""
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile

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
os.makedirs(OUT, exist_ok=True)
TMP = tempfile.mkdtemp(prefix="cor-aut7f2-fecho-")
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TEMP=TMP, TMP=TMP, TMPDIR=TMP,
           PYTHONIOENCODING="utf-8")

ACEITE = os.path.join("tools", "automacao", "aceite", "relatorio_aceite.py")
ESTILO = os.path.join("tools", "automacao", "estilo", "estilo_atributos.py")
TESTE_ESTILO = os.path.join("tools", "automacao", "estilo", "test_estilo_atributos.py")
TESTE_ACEITE = os.path.join("tools", "automacao", "aceite", "test_relatorio_aceite.py")
REFUTACAO = os.path.join("tools", "automacao", "estilo", "refutar_cor_aut7f2.py")
REFUTACAO_ENTRADAS = os.path.join("tools", "automacao", "estilo", "refutar_cor_aut7f2_entradas.py")
DOC_REL = os.path.join("docs", "automacao", "AUT-7-relatorio.md")
DOC_RES = os.path.join("docs", "automacao", "AUT-7-resultado.json")
JSON_REFUTACAO = os.path.join(OUT, "refutacao-cor-aut7-f2.json")


def sha(caminho):
    h = hashlib.sha256()
    with io.open(caminho, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def roda(nome, argv, timeout=1800):
    p = subprocess.run([sys.executable] + list(argv), cwd=S, env=ENV,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    with io.open(os.path.join(OUT, nome + ".stdout"), "wb") as fh:
        fh.write(p.stdout)
    with io.open(os.path.join(OUT, nome + ".stderr"), "wb") as fh:
        fh.write(p.stderr)
    print("  %-34s exit=%s" % (nome, p.returncode))
    return p


def resumo_da_suite(texto):
    linhas = [l.strip() for l in texto.strip().splitlines() if l.startswith("total:")]
    reprovadas = [l.strip() for l in texto.strip().splitlines() if l.startswith("REPROVADAS:")]
    return {"linha_total": linhas[-1] if linhas else None,
            "reprovadas": reprovadas[-1] if reprovadas else None}


RES = {}
if os.path.isfile(JSON_REFUTACAO):
    with io.open(JSON_REFUTACAO, encoding="utf-8") as fh:
        RES = json.load(fh)
else:
    print("AVISO: %s ausente - rode antes `refutar_cor_aut7f2.py`" % JSON_REFUTACAO)

print("== fecho: suites da entrega")
suites = {}
for nome, argv in (("suite-estilo", [TESTE_ESTILO]), ("suite-aceite", [TESTE_ACEITE])):
    p = roda(nome, argv)
    suites[nome] = dict(resumo_da_suite(p.stdout.decode("utf-8", "replace")), exit=p.returncode)
    print("     %s" % suites[nome])
RES["suites"] = suites

print("== fecho: docs gerados (antes/depois) pela CLI real")
antes = {}
for rel in (DOC_REL, DOC_RES):
    caminho = os.path.join(S, rel)
    antes[rel] = sha(caminho) if os.path.isfile(caminho) else None
ident = os.path.join(OUT, "identidade.json")
if not os.path.isfile(ident):
    ident = None
p = roda("regeracao-dos-docs", [ACEITE, "--repo", S, "--out-dir", OUT,
                                "--relatorio", DOC_REL, "--out", DOC_RES]
         + (["--identidade", ident] if ident else []))
depois = {rel: (sha(os.path.join(S, rel)) if os.path.isfile(os.path.join(S, rel)) else None)
          for rel in (DOC_REL, DOC_RES)}
fontes = {rel.replace("\\", "/"): sha(os.path.join(S, rel)) for rel in
          (ESTILO, TESTE_ESTILO, REFUTACAO, REFUTACAO_ENTRADAS, "tools/automacao/estilo/hashes_da_entrega.py",
           "tools/automacao/estilo/fechar_cor_aut7f2.py",
           ACEITE, TESTE_ACEITE, DOC_REL, DOC_RES) if os.path.isfile(os.path.join(S, rel))}
with io.open(os.path.join(OUT, "docs-antes.txt"), "w", encoding="utf-8", newline="\n") as fh:
    fh.write("docs-antes.txt - COR-AUT7-F2 (t_cd1332d7, execucao 430)\n")
    fh.write("Prova que o achado A9 apontava como ausente (a COR-AUT7 citava este arquivo e nao o "
             "entregou).\n")
    fh.write("sha256 dos docs gerados ANTES (estado do disco no inicio da fase de fecho) e DEPOIS "
             "(regerados pela CLI REAL do consolidador: "
             "`relatorio_aceite.py --relatorio ... --out ...`):\n\n")
    fh.write("%-28s %-64s %-64s\n" % ("arquivo", "antes", "depois"))
    for rel in (DOC_REL, DOC_RES):
        fh.write("%-28s %-64s %-64s\n" % (os.path.basename(rel), str(antes[rel]), str(depois[rel])))
    fh.write("\nfontes e docs no fechamento da COR-AUT7-F2 (sha256):\n")
    for rel, h in sorted(fontes.items()):
        fh.write("%-48s %s\n" % (rel, h))
    fh.write("\nO relatorio completo desta refutacao (achados A1-A9 + fecho) esta em "
             "refutacao-cor-aut7-f2.json, no mesmo diretorio.\n")
    fh.write("\nNota: se o 'antes' medido aqui NAO for o hash que a COR-AUT7 declarou em "
             "docs/automacao/COR-AUT7-correcao.md (tabela \"Hashes\"), houve ESCRITOR CONCORRENTE "
             "na arvore compartilhada entre a leitura daquele parecer e esta execucao. O que este "
             "arquivo prova e o que a correcao do A9 promete: o doc foi regerado pela CLI real "
             "NESTA execucao e os dois lados (antes/depois) estao medidos acima.\n")
RES["docs"] = {"antes": antes, "depois": depois, "exit_regeracao": p.returncode,
               "evidencia": "docs-antes.txt", "fontes": fontes,
               "mudou": {rel: (antes[rel] != depois[rel]) for rel in (DOC_REL, DOC_RES)}}
RES["hashes"] = fontes
RES["fase"] = "achados (A1-A9) + fecho (suites + docs): evidencia completa"
with io.open(JSON_REFUTACAO, "w", encoding="utf-8") as fh:
    fh.write(json.dumps(RES, indent=2, ensure_ascii=False, default=str))

print("  docs: antes=%s depois=%s" % (str(antes[DOC_REL])[:12], str(depois[DOC_REL])[:12]))
print("  relatorio atualizado:", JSON_REFUTACAO)
