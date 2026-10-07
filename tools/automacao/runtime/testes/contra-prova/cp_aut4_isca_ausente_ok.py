#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova): afirma o FALSO — um campo AUSENTE vale OK.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE. Se ele PASSA,
o coletor esta aceitando AUSENTE como valor medido — o que invalida tudo.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut4-isca-ausente-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: afirma que AUSENTE e OK — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    try:
        n = col.normalizar_observacao({"texto_bruto": "AUSENTE", "status": "OK"},
                                      procedencia="fixture", rotulo_fixture="isca")
    except col.ObservacaoInvalida as erro:
        # A GUARDA viva recusou ANTES da afirmacao falsa: a isca TEM de reprovar — e
        # por ASSERT, nao por excecao (R-5 do CIC-5R: crash nao e prova).
        C.arc.exigir(False, "o coletor recusou AUSENTE-como-OK (guarda viva): a isca TEM de "
                            "reprovar — %s" % erro)
    # A afirmacao FALSA: "AUSENTE conta como OK".
    C.arc.igual(n["ok"], True, "AUSENTE deveria ser OK (AFIRMACAO FALSA — a isca tem de reprovar)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
