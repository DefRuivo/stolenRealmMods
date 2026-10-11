#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) do instrumento de cobertura - INT-R1-C5.

O DEFEITO PLANTADO: a isca acredita que **remover uma entrada real da tabela nao afeta
a trava** (leitura de quem confia no "o build passou, entao esta tudo bem"). Com uma
entrada real fora do `TextFixes`, a trava tem de REPROVAR - e a isca, que exige lista
vazia de violacoes, reprova CITANDO o defeito (`entrada-removida`).

A metade que PASSA e `cp_cobertura_ui_localized_ok.py` (mesmo cenario com a leitura certa).
"""
import os
import sys

import arcabouco as arc

META = {
    "nome": "contra-prova-cobertura-ui-localized",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: com uma entrada real removida, a trava REPROVA (quem acha que 'nao afeta nada' esta mentindo)",
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
    arc.igual(viol, [], "a entrada real %r foi removida, mas a trava nao acusou: %s" % (chave, viol))
    arc.igual(C.verificar_baseline({"cobrados": {chave: "TextFixes"}}, tabelas), [],
              "controle positivo: com o fonte intacto a trava tem de ficar verde")


if __name__ == "__main__":
    arc.main(META, corpo)
