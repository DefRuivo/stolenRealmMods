#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova): afirma o FALSO — o detector CONFIRMA uma leitura VAZIA.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE. Se ele PASSAR, o
detector esta confirmando o que nao leu — e todo "CONFIRMADA" da frente deixa de valer.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut4-isca-detector-confirma-leitura-vazia",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: afirma que o detector CONFIRMA uma leitura vazia — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    fx = C.fixture("cenarios-negativos")
    plano = dict(C.fixture("plano-exemplo"))
    plano["campos_alvo"] = list(fx["campos_alvo"])

    r, codigo = col.detectar_leitura(observacoes=[], plano=plano,
                                     contexto=dict(fx["contexto"]))
    if r["veredito"] == col.VEREDITO_CONFIRMA:
        # A GUARDA viva morreu: a isca TEM de reprovar mesmo assim (por ASSERT, nao crash).
        C.arc.exigir(False, "o detector CONFIRMOU leitura vazia (guarda morta): a isca TEM de "
                            "reprovar — RESULTADO|REPROVOU|")
    # A afirmacao FALSA: "sem leitura nenhuma o detector confirma".
    C.arc.igual(r["veredito"], col.VEREDITO_CONFIRMA,
                "leitura vazia deveria CONFIRMAR (AFIRMACAO FALSA — a isca tem de reprovar)")
    C.arc.igual(codigo, 0, "leitura vazia deveria dar exit 0 (AFIRMACAO FALSA)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
