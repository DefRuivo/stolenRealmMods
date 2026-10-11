#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (metade OK) do cenario 2 - a regra de HOJE (lookup exato)."""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "contra-prova-bt-substituicao-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "o MESMO teste da isca com a regra de HOJE (so troca o exibido == original em ingles)",
}


def corpo():
    viol = R.violacoes_da_substituicao(R.le_fonte(), modo="estrito")
    arc.igual(viol, [], "a substituicao segura divergiu: %s" % viol)


if __name__ == "__main__":
    arc.main(META, corpo)
