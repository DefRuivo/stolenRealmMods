#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova): afirma o FALSO — a espera de estado queima o teto INTEIRO.

R-3 do parecer CIC-5R: o catch do probe grava `status=ERRO` SEM setar `fase`. Se esta
isca PASSAR, a espera voltou a parar so pela `fase` e um erro do instrumento custa o
timeout inteiro.
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut4f-isca-espera-queima-teto",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: status=ERRO sem fase queima o teto da espera — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    with tempfile.TemporaryDirectory(prefix="isca-r3-") as raiz:
        caminho_log = os.path.join(raiz, "LogOutput.log")      # ausente de proposito
        caminho_json = os.path.join(raiz, "aut4probe.json")
        with open(caminho_json, "w", encoding="utf-8") as fh:
            json.dump({"fase": "lendo-objetos", "status": "ERRO"}, fh)
        estado = col._esperar_estado(caminho_log, caminho_json, 0.6, 0.05)
    # A afirmacao FALSA: a espera queima o teto inteiro com `status=ERRO`.
    C.arc.exigir(estado["segundos"] >= 0.5,
                 "R-3: status=ERRO deveria queimar o teto da espera (AFIRMACAO FALSA — a "
                 "isca TEM de reprovar); parou em %.3f s" % estado["segundos"])


if __name__ == "__main__":
    C.arc.main(META, corpo)
