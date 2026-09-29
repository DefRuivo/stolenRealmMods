#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Confere as chaves das tabelas do BetterTooltips contra o censo (RV-7).

Por que existe: as tabelas `TextFixes`/`TextAppends` casam por texto EXATO. Uma chave
com um espaco a mais, ou escrita de memoria em vez de copiada do asset, NUNCA dispara -
e falha em silencio (o log so aparece quando muda algo). Este script le as chaves do
codigo-fonte e diz quais delas existem no censo.

Atencao ao ler o resultado: "nao achada no censo" NAO e erro por si. O censo do RV-7
cobre so skills/status/itens/afixos/powerups; textos de UI e dicas de loading (ex.: a
frase das lojas) ainda nao estao la - ver a secao "O que este censo AINDA nao cobre"
em docs/cobertura/README.md.

Uso: python tools/check_fix_keys.py
"""
import csv
import glob
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COBERTURA = os.path.join(RAIZ, "docs", "cobertura")
FONTE = os.path.join(RAIZ, "BetterTooltips", "Patches", "LocalizePatch.cs")
DICIONARIOS = ["TextFixes", "TextAppends"]

# par chave/valor: "chave", "valor"  (com escapes no meio)
PAR = re.compile(r'"((?:[^"\\]|\\.)*)"\s*,\s*"((?:[^"\\]|\\.)*)"')


def desescapa(s):
    return s.replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")


def blocos(txt):
    for nome in DICIONARIOS:
        i = txt.find(nome + " = new Dictionary<string, string>")
        if i < 0:
            continue
        j = txt.find("};", i)
        if j > i:
            yield nome, txt[i:j]


def main():
    if not os.path.isfile(FONTE):
        print("fonte nao encontrada: %s" % FONTE)
        return 1
    txt = open(FONTE, encoding="utf-8").read()

    universo = set()
    for arq in glob.glob(os.path.join(COBERTURA, "*.csv")):
        with open(arq, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                for col in ("descricao", "nome"):
                    v = r.get(col)
                    if v:
                        universo.add(v)

    chaves = []
    for nome, bloco in blocos(txt):
        for m in PAR.finditer(bloco):
            chaves.append((nome, desescapa(m.group(1))))

    ok = [(n, k) for n, k in chaves if k in universo]
    nao = [(n, k) for n, k in chaves if k not in universo]
    print("chaves extraidas: %d" % len(chaves))
    print("  no censo   : %d" % len(ok))
    print("  fora do censo: %d" % len(nao))

    if nao:
        print("\nFORA DO CENSO (texto de UI/loading, ou chave errada - conferir):")
        for n, k in nao:
            print("  [%-11s] %r" % (n, k[:95]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
