#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (metade OK) do cenario 5 - a regra de HOJE (guard antes do indexador)."""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "contra-prova-bt-guard-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "o MESMO teste da isca com a regra de HOJE: o guard pula o atributo inexistente antes de indexar",
}


def corpo():
    viol = R.violacoes_do_guard("com_guarda")
    arc.igual(viol, [], "atributo inexistente tinha de ser pulado, mas: %s" % viol)


if __name__ == "__main__":
    arc.main(META, corpo)
