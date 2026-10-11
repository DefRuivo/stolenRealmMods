#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (metade OK) do cenario 3 - as notas das tabelas de verdade, sem token."""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "contra-prova-bt-token-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "o MESMO teste da isca sobre as tabelas de verdade: nenhuma nota carrega [N]",
}


def corpo():
    achados = R.violacoes_do_token("real")
    arc.igual(achados, [], "nota com token [N] nas tabelas de verdade: %s" % achados)


if __name__ == "__main__":
    arc.main(META, corpo)
