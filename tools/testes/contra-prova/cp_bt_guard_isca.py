#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) do cenario 5 - O GUARD ANTES DO INDEXADOR.

O DEFEITO PLANTADO: indexar SEM o guard (`modo="sem_guarda"`). Um atributo que nao existe no
motor faz o indexador LANCAR. A isca acredita que "o atributo inexistente e pulado" (0) e
REPROVA citando a explosao no indexador.

A metade que PASSA e `cp_bt_guard_ok.py`.
"""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "contra-prova-bt-guard",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: sem o guard antes da indexacao, atributo inexistente explode no indexador do motor",
}


def corpo():
    viol = R.violacoes_do_guard("sem_guarda")
    arc.igual(viol, [], "atributo inexistente tinha de ser pulado, mas: %s" % viol)


if __name__ == "__main__":
    arc.main(META, corpo)
