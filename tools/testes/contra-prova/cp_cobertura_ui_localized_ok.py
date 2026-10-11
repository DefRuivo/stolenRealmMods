#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metade OK da contra-prova do instrumento de cobertura (INT-R1-C5).

Mesmo cenario da isca (`cp_cobertura_ui_localized_isca.py`), com a leitura CERTA:
remover uma entrada real do `TextFixes` produz exatamente UMA violacao do tipo
`entrada-removida`, e o fonte intacto continua verde (controle positivo). Passa (exit 0).
"""
import os
import sys

import arcabouco as arc

META = {
    "nome": "contra-prova-cobertura-ui-localized-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "leitura certa: entrada real removida -> 1 violacao 'entrada-removida'; fonte intacto -> verde",
}

RAIZ = arc.raiz_do_repo()
sys.path.insert(0, os.path.join(RAIZ, "tools"))
import cobertura_ui_localized as C  # noqa: E402


def corpo():
    indice, _ = C.carregar_censo()
    tabelas = C.carregar_tabelas()
    chave = next(k for k in tabelas["TextFixes"] if k in indice)

    mutadas = dict(tabelas)
    mutadas["TextFixes"] = {k: v for k, v in tabelas["TextFixes"].items() if k != chave}

    viol = C.verificar_baseline({"cobrados": {chave: "TextFixes"}}, mutadas)
    arc.igual(len(viol), 1, "a trava tinha de acusar exatamente uma violacao: %s" % viol)
    arc.igual(viol[0]["tipo"], "entrada-removida", "tipo da violacao")
    arc.igual(viol[0]["chave"], chave, "chave da violacao")
    arc.igual(C.verificar_baseline({"cobrados": {chave: "TextFixes"}}, tabelas), [],
              "controle positivo: fonte intacto tem de ficar verde")


if __name__ == "__main__":
    arc.main(META, corpo)
