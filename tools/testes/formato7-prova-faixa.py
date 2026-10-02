#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""formato7-prova-faixa.py - a prova do primitivo de FAIXA do `recorte.py`, nos DOIS SENTIDOS.

Roda fora da suite (nome sem `t_`/`cp_`: o runner o CONTA como ignorado, nao como teste). E a
bancada reproduzivel que produziu `formato7-prova-faixa.log`. O que ele mede:

  1. EQUIVALENCIA NO FONTE REAL: o consumidor da regra 2 do `check_patches` por TEXTO
     (`cp.trecho_do_patch`) e o consumidor por FAIXA dao o MESMO trecho — sem edicao e depois de
     um retoque INOFENSIVO de 2200 chars.
  2. O FURO QUE A FAIXA FECHA: com uma COPIA do bloco dentro de um literal antes do bloco, a
     reconstrucao por texto (`codigo.index(bloco, pos) + len(bloco)`) para ANTES do bloco de
     verdade e a faixa acha o bloco certo.
  3. FALHA ALTA: as duas formas levantam `arc.Falhou` com chaves que nao fecham.

    python tools/testes/formato7-prova-faixa.py | tee tools/testes/formato7-prova-faixa.log
"""
import importlib.util
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import arcabouco as arc        # noqa: E402
import recorte as rec          # noqa: E402

RAIZ = arc.raiz_do_repo()
CAMINHO_CP = os.path.join(RAIZ, "tools", "check_patches.py")
FONTE_REAL = os.path.join(RAIZ, "BetterTooltips", "Patches", "ShrineAuraPatch.cs")
PADRAO_TIPO = r"\b(typeof|nameof)\s*\("


def modulo_do_check():
    spec = importlib.util.spec_from_file_location("check_patches_f7p", CAMINHO_CP)
    cp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cp)
    rec_, arcmod = cp.carregar_recorte()
    return cp, rec_, arcmod


def trecho_por_faixa(codigo, pos):
    ini, fim = rec.faixa_bloco_apos(codigo, pos)
    return codigo[pos:fim + 1]


def trecho_por_texto(codigo, pos):
    bloco = rec.bloco_apos(codigo, pos)
    return codigo[pos:codigo.index(bloco, pos) + len(bloco)]


def retoque(tamanho):
    linhas, n = [], 0
    while n < tamanho:
        linhas.append("\n    private static int _rastro%d = 0;" % len(linhas))
        n += len(linhas[-1])
    return "".join(linhas)


def atributo_bare(codigo):
    for m in re.finditer(r"\[HarmonyPatch\b", codigo):
        fim = codigo.find("]", m.start())
        if not re.search(PADRAO_TIPO, codigo[m.start():fim + 1]):
            return m
    return None


COM_COPIA = 'if (x) log("{ a(); }"); { a(); } fim\n'
BLOCO = "{ a(); }"
QUEBRADO = "[HarmonyPatch]\nclass P\n{\n    private static void X()\n    {\n        return;\n"


def main():
    cp, rec_, arcmod = modulo_do_check()
    with open(FONTE_REAL, encoding="utf-8") as fh:
        codigo, _, _ = cp.separar(fh.read())
    m = atributo_bare(codigo)
    pos = m.start()

    print("=== 1. EQUIVALENCIA NO FONTE REAL (%s, ancora em %d) ===" % (FONTE_REAL, pos))
    for rotulo, texto in (("sem edicao", codigo),
                          ("retoque inofensivo de 2200", None)):
        if texto is None:
            abertura = codigo.find("{", pos)
            texto = codigo[:abertura + 1] + retoque(2200) + codigo[abertura + 1:]
        t_texto = cp.trecho_do_patch(texto, pos, rec_, arcmod)
        t_faixa = trecho_por_faixa(texto, pos)
        ini, fim = rec.faixa_bloco_apos(texto, pos)
        print("  [%s]" % rotulo)
        print("    comprimento: texto=%d  faixa=%d  |  iguais? %s  |  termina em `}`? %s"
              % (len(t_texto), len(t_faixa), t_texto == t_faixa, texto[fim] == "}"))
        print("    acha a assinatura por TIPO pelos DOIS caminhos? %s"
              % (bool(re.search(PADRAO_TIPO, t_texto)) and bool(re.search(PADRAO_TIPO, t_faixa))))
        arc.exigir(t_texto == t_faixa and texto[fim] == "}", "as duas rotas divergiram em %r" % rotulo)

    print("=== 2. O FURO DA RECONSTRUCAO POR TEXTO (copia do bloco num literal) ===")
    p = COM_COPIA.find("if (x)")
    faixa = rec.faixa_bloco_apos(COM_COPIA, p)
    ini_texto = COM_COPIA.index(BLOCO, p)
    print("  bloco=%r  |  faixa=%r (fim do bloco de verdade)  |  index por texto=%d (a COPIA)"
          % (BLOCO, faixa, ini_texto))
    print("    trecho por texto = %r" % trecho_por_texto(COM_COPIA, p))
    print("    trecho por faixa = %r" % trecho_por_faixa(COM_COPIA, p))
    arc.exigir(ini_texto != faixa[0] and len(trecho_por_texto(COM_COPIA, p)) <= faixa[0],
               "a copia nao enganou o `index`: o furo nao esta reproduzido")

    print("=== 3. FALHA ALTA (chaves que nao fecham) ===")
    for rotulo, acao in (("bloco_apos", lambda: rec.bloco_apos(QUEBRADO, 0)),
                         ("faixa_bloco_apos", lambda: rec.faixa_bloco_apos(QUEBRADO, 0)),
                         ("consumidor por texto", lambda: cp.trecho_do_patch(QUEBRADO, 0, rec_, arcmod)),
                         ("consumidor por faixa", lambda: trecho_por_faixa(QUEBRADO, 0))):
        try:
            acao()
        except (arc.Falhou, arcmod.Falhou) as erro:
            print("  %-22s -> FALHOU ALTO: %s" % (rotulo, str(erro)[:70]))
        else:
            print("  %-22s -> NAO falhou alto (defeito!)" % rotulo)
            raise SystemExit(1)

    print("FORMATO-7: texto e faixa dao o mesmo recorte; a faixa fecha o furo da copia no "
          "literal; as duas falham alto — nos dois sentidos.")


if __name__ == "__main__":
    main()
