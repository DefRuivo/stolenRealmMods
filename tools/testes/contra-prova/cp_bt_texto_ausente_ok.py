#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (metade OK) do cenario 4 - a regra de HOJE (snapshot + try/catch)."""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "contra-prova-bt-texto-ausente-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "o MESMO teste da isca com a regra de HOJE: texto intacto + falha declarada",
}


def corpo():
    viol = R.violacoes_do_funil("seguro")
    arc.igual(viol, [], "o texto do jogo tinha de ficar intacto, mas: %s" % viol)


if __name__ == "__main__":
    arc.main(META, corpo)
