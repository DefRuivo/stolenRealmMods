#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (metade OK) do cenario 1 - o MESMO teste da isca com o fonte REAL.

Aqui o fonte e o `LocalizePatch.cs` de verdade (chaves unicas nas duas tabelas, sem cruzamento):
a expectativa "esta limpo" confere e este arquivo PASSA.
"""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "contra-prova-bt-uma-entrada-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "o MESMO teste da isca sobre o LocalizePatch.cs real: chaves unicas, sem chave nas duas tabelas",
}


def corpo():
    real = R.le_fonte()
    acusacoes = []
    dup_fix = R.chaves_duplicadas(real, "TextFixes")
    dup_app = R.chaves_duplicadas(real, "TextAppends")
    if dup_fix:
        acusacoes.append("check_dupes TextFixes: %r" % dup_fix)
    if dup_app:
        acusacoes.append("check_dupes TextAppends: %r" % dup_app)
    cross = R.chaves_nas_duas_tabelas(real)
    if cross:
        acusacoes.append("chave nas duas tabelas: %r" % cross)
    codigo, saida = R.roda_chave_compartilhada(R.LOCALIZE)
    if codigo != 0:
        acusacoes.append("--estrito reprovou o real (exit %d): %s"
                         % (codigo, saida.strip().splitlines()[-1:]))
    arc.igual(acusacoes, [], "o LocalizePatch.cs real acusou: %s" % acusacoes)


if __name__ == "__main__":
    arc.main(META, corpo)
