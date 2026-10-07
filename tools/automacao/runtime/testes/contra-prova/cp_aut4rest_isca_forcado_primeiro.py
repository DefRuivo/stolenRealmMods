#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova): afirma o FALSO — o forcado (taskkill) vem ANTES do gracioso.

AUD-1/L2: em rodada sem usuario o `taskkill` e bloqueado, entao o fechamento tem de
ser GRACIOSO primeiro (`CloseMainWindow`) com o forcado como fallback. Se esta isca
PASSAR, o driver voltou a preferir o forcado — o caminho que nao funciona headless.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut4rest-isca-forcado-primeiro",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: fechar o jogo pelo forcado ANTES do gracioso — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    comandos = col.comandos_de_fechamento(4242)
    # A afirmacao FALSA: a primeira tentativa e o forcado por taskkill.
    C.arc.igual(comandos[0]["modo"], "forcado",
                "AUD-1/L2: o primeiro comando deveria ser o FORCADO "
                "(AFIRMACAO FALSA — a isca TEM de reprovar)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
