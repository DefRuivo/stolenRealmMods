#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RSTV-27 - bancada reproduzivel da CONTRA-PROVA do rodape da tooltip read-only.

NAO e' teste da suite (nome sem `t_`/`cp_`: o runner ignora e CONTA) — e' a bancada que produz a
evidencia registrada em `tools/testes/rstv27-rodape-prova-reprovando.log`.

O que ela faz, do zero:
  1. COPIA um mini-repo para um SANDBOX FORA do repo (raiz com `docs/PLANO-DE-TESTES.md`, os dois
     fontes do mod e `tools/testes/`): e' o sandbox que o `arcabouco.raiz_do_repo` acha, entao o
     runner roda contra a COPIA — o repo nao e' tocado em nenhum momento;
  2. roda o teste da suite (`t_rstv27_rodape_personagem.py`) na copia -> tem de PASSAR (exit 0);
  3. planta, UM POR VEZ, cada defeito do conserto na copia (hover sem armar o alvo, gancho sem
     preenchimento, gancho sem fallback, gancho sobrescrevendo o valor do jogo), roda e exige
     REPROVOU (exit 1), restaurando byte a byte (sha256 conferido) entre as rodadas;
  4. confere que os arquivos do REPO continuam com o mesmo sha256 do inicio.

Uso:  python tools/testes/prova-sandbox-rstv27.py [--sandbox CAMINHO]
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
TESTE = "tools/testes/testes/puros/t_rstv27_rodape_personagem.py"


def sha(caminho):
    with open(caminho, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def monta_sandbox(destino):
    """Mini-repo: docs/PLANO-DE-TESTES.md + os dois fontes + tools/testes inteiro."""
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


def planta(caminho, guarda, sandbox, marca, fn):
    """Planta o defeito, roda o teste, restaura byte a byte (sha256 conferido)."""
    antes = sha(caminho)
    with open(caminho, encoding="utf-8") as fh:
        src = fh.read()
    novo = fn(src)
    if novo == src:
        print("  [%s] ANCHORA NAO ACHADA: o plantio nao mudou o fonte (prova INVALIDA)" % marca)
        return None, None
    with open(caminho, "w", encoding="utf-8", newline="") as fh:
        fh.write(novo)
    rc, linhas = roda_teste(sandbox)
    shutil.copyfile(os.path.join(guarda, os.path.basename(caminho)), caminho)
    print("  [%s] exit=%d%s" % (marca, rc, " (esperado 1)" if rc == 1 else " <-- ATENCAO"))
    for l in linhas[:1]:
        print("      " + l[:200])
    print("      restaurado byte a byte: %s (%s)" % (sha(caminho) == antes, sha(caminho)[:16]))
    return rc, sha(caminho) == antes


def sem_fallback(src):
    return re.sub(r"if\s*\(\s*alvo\s*==\s*null\s*\)\s*\{[^{}]*?return\s*;\s*\}\s*", "", src, count=1)


def sobrescreve_o_jogo(src):
    return re.sub(r"if\s*\(\s*__result\s*!=\s*null\s*\)\s*\{[^{}]*\}\s*", "", src, count=1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sandbox", default=os.path.join(tempfile.gettempdir(), "rstv27-sandbox"))
    args = ap.parse_args()

    sandbox = monta_sandbox(os.path.abspath(args.sandbox))
    tab = os.path.join(sandbox, "RoguelikeSkillTreeVisualizer", "SkillTreesTab.cs")
    patches = os.path.join(sandbox, "RoguelikeSkillTreeVisualizer", "Patches.cs")
    guarda = os.path.join(sandbox, "_restore")
    os.makedirs(guarda, exist_ok=True)
    shutil.copyfile(tab, os.path.join(guarda, "SkillTreesTab.cs"))
    shutil.copyfile(patches, os.path.join(guarda, "Patches.cs"))

    print("RSTV-27 - CONTRA-PROVA EM SANDBOX FORA DO REPO")
    print("repo (NAO e' tocado): %s" % RAIZ_REPO)
    print("sandbox:              %s" % sandbox)
    print("teste:                %s" % TESTE)
    print()

    sha_repo_antes = {f: sha(os.path.join(RAIZ_REPO, f)) for f in FONTES}

    print("[FONTE DE VERDADE] a copia do conserto, no sandbox")
    for nome, caminho in (("SkillTreesTab.cs", tab), ("Patches.cs", patches)):
        print("  %-18s sha256 %s" % (nome, sha(caminho)))
    rc0, linhas0 = roda_teste(sandbox)
    print("  [sem defeito] exit=%d%s" % (rc0, " (esperado 0)" if rc0 == 0 else " <-- ATENCAO"))
    for l in linhas0[:1]:
        print("      " + l[:200])
    print()

    rodadas = [planta(tab, guarda, sandbox, "(a) hover sem armar o alvo do modal",
                      lambda s: s.replace("TooltipCharacterRodapePatch.ComAlvo(alvo);", "", 1))]
    print()
    rodadas.append(planta(patches, guarda, sandbox, "(b) gancho sem preenchimento",
                          lambda s: s.replace("__result = alvo;", "", 1)))
    print()
    rodadas.append(planta(patches, guarda, sandbox, "(c) gancho sem o fallback", sem_fallback))
    print()
    rodadas.append(planta(patches, guarda, sandbox, "(d) gancho sobrescrevendo o valor do jogo",
                          sobrescreve_o_jogo))
    print()

    sha_repo_depois = {f: sha(os.path.join(RAIZ_REPO, f)) for f in FONTES}
    intacto = sha_repo_antes == sha_repo_depois
    print("[REPO INTACTO] %s" % intacto)
    for f, h in sha_repo_depois.items():
        print("  %s %s" % (h[:16], f))
    print()

    ok = (rc0 == 0 and all(rc == 1 and restaurado for rc, restaurado in rodadas) and intacto)
    if ok:
        print("VEREDITO: PROVA OK - sem defeito PASSA (exit 0); os %d defeitos plantados REPROVAM "
              "(exit 1); cada um restaurado byte a byte; o repo nao foi tocado." % len(rodadas))
        return 0
    print("VEREDITO: PROVA FALHOU - ver as rodadas acima.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
