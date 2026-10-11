#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prova-sandbox-rstv27-valor.py - a bancada reproduzivel da CONTRA-PROVA do teste de VALOR do RSTV-27.

NAO e' teste da suite (nome sem `t_`/`cp_`: o runner ignora e CONTA) - e' a bancada que produz a
evidencia registrada em `tools/testes/rstv27-valor-prova-reprovando.log`.

O que ela faz, do zero:
  1. COPIA um mini-repo para um SANDBOX FORA do repo (raiz com `docs/PLANO-DE-TESTES.md`, os dois
     fontes do mod e `tools/testes/` inteiro, fixtures incluidas): e' o sandbox que o
     `arcabouco.raiz_do_repo` acha, entao o runner roda contra a COPIA - o repo nao e' tocado;
  2. roda o teste `t_rstv27_rodape_valor.py` na copia COM o conserto -> tem de PASSAR (exit 0);
  3. REVERTE o conserto na copia, de duas formas (a PRE-FIX do cartao), uma por vez, e roda:
       (a) hover sem armar o alvo do modal  -> REPROVAR (exit 1);
       (b) gancho (postfix) sem preencher   -> REPROVAR (exit 1);
     restaurando byte a byte (sha256 conferido) entre as rodadas;
  4. confere que os arquivos do REPO continuam com o mesmo sha256 do inicio.

Uso:  python tools/testes/prova-sandbox-rstv27-valor.py [--sandbox CAMINHO]
Exit: 0 = PROVA OK | 1 = PROVA FALHOU | 2 = nao consegui montar o sandbox
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ_REPO = os.path.dirname(os.path.dirname(AQUI))          # tools/testes -> raiz
FONTES = ["RoguelikeSkillTreeVisualizer/SkillTreesTab.cs",
          "RoguelikeSkillTreeVisualizer/Patches.cs"]
TESTE = "tools/testes/testes/puros/t_rstv27_rodape_valor.py"

ANCORA_ARMADO = "TooltipCharacterRodapePatch.ComAlvo(alvo);"
ANCORA_PREENCHIMENTO = "__result = alvo;"


def sha(caminho):
    with open(caminho, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def monta_sandbox(destino):
    """Mini-repo: docs/PLANO-DE-TESTES.md + os dois fontes + tools/testes inteiro (com fixtures)."""
    if os.path.isdir(destino):
        shutil.rmtree(destino)
    os.makedirs(os.path.join(destino, "docs"))
    os.makedirs(os.path.join(destino, "RoguelikeSkillTreeVisualizer"))
    shutil.copyfile(os.path.join(RAIZ_REPO, "docs", "PLANO-DE-TESTES.md"),
                    os.path.join(destino, "docs", "PLANO-DE-TESTES.md"))
    for fonte in FONTES:
        shutil.copyfile(os.path.join(RAIZ_REPO, fonte), os.path.join(destino, fonte))
    shutil.copytree(os.path.join(RAIZ_REPO, "tools", "testes"),
                    os.path.join(destino, "tools", "testes"),
                    ignore=shutil.ignore_patterns("__pycache__"))
    return destino


def roda_teste(sandbox):
    r = subprocess.run([sys.executable, "tools/testes/roda_testes.py", "--teste", TESTE],
                       cwd=sandbox, capture_output=True, text=True, encoding="utf-8")
    saida = (r.stdout or "") + (r.stderr or "")
    linhas = [l.strip() for l in saida.splitlines() if "PASSOU" in l or "REPROVOU" in l]
    return r.returncode, linhas


def roda_estado(sandbox, guarda, caminho, marca, fn, esperado):
    """Planta o defeito, roda o teste, restaura byte a byte (sha256 conferido)."""
    antes = sha(caminho)
    with open(caminho, encoding="utf-8") as fh:
        src = fh.read()
    novo = fn(src)
    if novo == src:
        print("  [%s] ANCORA NAO ACHADA: o plantio nao mudou o fonte (prova INVALIDA)" % marca)
        return None, None
    with open(caminho, "w", encoding="utf-8", newline="") as fh:
        fh.write(novo)
    rc, linhas = roda_teste(sandbox)
    shutil.copyfile(os.path.join(guarda, os.path.basename(caminho)), caminho)
    ok = rc == esperado
    print("  [%s] exit=%d%s" % (marca, rc, " (esperado %d)" % esperado if ok else " <-- ATENCAO"))
    for l in linhas[:1]:
        print("      " + l[:600])
    restaurado = sha(caminho) == antes
    print("      restaurado byte a byte: %s (%s)" % (restaurado, sha(caminho)[:16]))
    return rc, restaurado


def sem_armado(src):
    return src.replace(ANCORA_ARMADO, "", 1)


def sem_preenchimento(src):
    return src.replace(ANCORA_PREENCHIMENTO, "", 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sandbox", default=os.path.join(tempfile.gettempdir(), "rstv27-valor-sandbox"))
    args = ap.parse_args()

    sandbox = monta_sandbox(os.path.abspath(args.sandbox))
    tab = os.path.join(sandbox, "RoguelikeSkillTreeVisualizer", "SkillTreesTab.cs")
    patches = os.path.join(sandbox, "RoguelikeSkillTreeVisualizer", "Patches.cs")
    guarda = os.path.join(sandbox, "_restore")
    os.makedirs(guarda, exist_ok=True)
    shutil.copyfile(tab, os.path.join(guarda, "SkillTreesTab.cs"))
    shutil.copyfile(patches, os.path.join(guarda, "Patches.cs"))

    print("RSTV-27 (VALOR) - CONTRA-PROVA EM SANDBOX FORA DO REPO")
    print("repo (NAO e' tocado): %s" % RAIZ_REPO)
    print("sandbox:              %s" % sandbox)
    print("teste:                %s" % TESTE)
    print()

    sha_repo_antes = {f: sha(os.path.join(RAIZ_REPO, f)) for f in FONTES}

    print("[FONTE DE VERDADE] a copia do conserto, no sandbox")
    for nome, caminho in (("SkillTreesTab.cs", tab), ("Patches.cs", patches)):
        print("  %-18s sha256 %s" % (nome, sha(caminho)))
    rc0, linhas0 = roda_teste(sandbox)
    print("  [COM o conserto] exit=%d%s" % (rc0, " (esperado 0)" if rc0 == 0 else " <-- ATENCAO"))
    for l in linhas0[:1]:
        print("      " + l[:220])
    print()

    print("[PRE-FIX] revertendo o conserto na copia, um defeito por vez")
    rodadas = [roda_estado(sandbox, guarda, tab, "(a) hover sem armar o alvo do modal", sem_armado, 1)]
    print()
    rodadas.append(roda_estado(sandbox, guarda, patches, "(b) postfix sem preencher", sem_preenchimento, 1))
    print()

    sha_repo_depois = {f: sha(os.path.join(RAIZ_REPO, f)) for f in FONTES}
    intacto = sha_repo_antes == sha_repo_depois
    print("[REPO INTACTO] %s" % intacto)
    for f, h in sha_repo_depois.items():
        print("  %s %s" % (h[:16], f))
    print()

    ok = (rc0 == 0 and all(rc == 1 and restaurado for rc, restaurado in rodadas) and intacto)
    if ok:
        print("VEREDITO: PROVA OK - COM o conserto PASSA (exit 0); cada defeito revertido (PRE-FIX) "
              "REPROVA (exit 1) pelo VALOR; cada um restaurado byte a byte; o repo nao foi tocado.")
        return 0
    print("VEREDITO: PROVA FALHOU - ver as rodadas acima.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
