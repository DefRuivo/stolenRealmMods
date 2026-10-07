#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIC-4R3 - CASO NEGATIVO OBRIGATORIO (revisor).

Em COPIA fora do repo:
  1. copia fiel do modulo do produto (65c0f3b2) -> copia/tooltips_shrines_copia.py
  2. copia NEUTRALIZADA (guarda do achado A + autenticacao do achado B desligadas)
     -> copia/tooltips_shrines_neutro.py
  3. imprimE sha256 dos dois e a prova textual da neutralizacao
Uso: python neutro.py [--produto CAMINHO] [--saida DIR]
"""
import argparse
import hashlib
import os
import sys

DEF_PRODUTO = r"C:\dev\stolen-realm\tools\automacao\cenarios\tooltips_shrines.py"
DEF_SAIDA = r"C:\Users\Pichau\AppData\Local\hermes\kanban\workspaces\t_9f5f2a53\bench\copia"

A_DE = '        if estado == "OK" and tooltip is None:'
A_PARA = '        if False:  # NEUTRALIZADO CIC-4R3 - achado A (exigencia da 2a superficie) desligada'
B_DE = '    if not contra or feed.get("procedencia") != "runtime":'
B_PARA = ('    return (None, None)  # NEUTRALIZADO CIC-4R3 - achado B (autenticacao da contra-prova) '
          'desligada\n' + B_DE)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--produto", default=DEF_PRODUTO)
    ap.add_argument("--saida", default=DEF_SAIDA)
    a = ap.parse_args()
    os.makedirs(a.saida, exist_ok=True)
    fonte = open(a.produto, encoding="utf-8").read()
    copia = os.path.join(a.saida, "tooltips_shrines_copia.py")
    neutro = os.path.join(a.saida, "tooltips_shrines_neutro.py")
    open(copia, "w", encoding="utf-8", newline="").write(fonte)
    n = fonte
    assert A_DE in n, "bloco do achado A nao encontrado"
    assert B_DE in n, "bloco do achado B nao encontrado"
    n = n.replace(A_DE, A_PARA, 1).replace(B_DE, B_PARA, 1)
    open(neutro, "w", encoding="utf-8", newline="").write(n)
    print("PRODUTO  %s  %s" % (sha(a.produto), a.produto))
    print("COPIA    %s  %s  (copia fiel: %s)"
          % (sha(copia), copia, "IDENTICA" if sha(copia) == sha(a.produto) else "DIFERE"))
    print("NEUTRO   %s  %s" % (sha(neutro), neutro))
    print("--- linhas neutralizadas (grep) ---")
    for i, ln in enumerate(n.splitlines(), 1):
        if "NEUTRALIZADO CIC-4R3" in ln:
            print("%s:%d: %s" % (os.path.basename(neutro), i, ln))
    return 0


if __name__ == "__main__":
    sys.exit(main())
