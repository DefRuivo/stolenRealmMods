#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) do cenario 3 - REGRA DO TOKEN `[N]`.

O DEFEITO PLANTADO: uma NOTA ("Cada stack concede +[0] Max Health por acerto.") carrega o
token `[0]`, que o pipeline de expressoes do jogo interpretaria. A isca acredita que "nenhuma
nota tem token" (0) e REPROVA citando `[0]`.

A metade que PASSA e `cp_bt_token_ok.py`.
"""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "contra-prova-bt-token",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: uma nota com [0] e aceita - o pipeline de expressoes do jogo interpretaria o token",
}


def corpo():
    achados = R.violacoes_do_token("plantado")
    arc.exigir(not achados,
               "nenhuma nota podia ter o token [N]; achei: %s" % [
                   (origem, nota, toks) for origem, nota, toks in achados])


if __name__ == "__main__":
    arc.main(META, corpo)
