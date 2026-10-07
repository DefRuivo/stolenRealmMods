#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova): afirma o FALSO — o alvo do 2o cenario e silenciosamente ignorado.

S-2 do parecer CIC-5R: `_alvos_do_plano` lia so o topo ou o `cenarios[0]`. Se esta isca
PASSAR, os requisitos por campo dos cenarios 2+ voltaram a ser descartados.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut4f-isca-alvos-2o-cenario-ignorado",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: o campos_alvo do 2o cenario e ignorado — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    plano = dict(C.fixture("plano-exemplo"))
    plano.pop("campos_alvo", None)
    plano["cenarios"] = [
        {"nome": "primeiro", "alvos": ["Tooltip.Title"], "campos_alvo": ["material"]},
        {"nome": "segundo", "alvos": ["Tooltip.Description"], "campos_alvo": ["tamanho_fonte"]},
    ]
    alvos = col._alvos_do_plano(plano) or []
    # A afirmacao FALSA: o alvo declarado no 2o cenario NAO governa o veredito.
    C.arc.exigir("tamanho_fonte" not in alvos,
                 "S-2: o campos_alvo do 2o cenario deveria ser ignorado (AFIRMACAO FALSA — a "
                 "isca TEM de reprovar)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
