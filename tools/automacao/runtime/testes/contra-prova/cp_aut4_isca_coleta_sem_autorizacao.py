#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova): afirma o FALSO — sem autorizacao a coleta acontece.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE. Se ele PASSA,
a trava de default-offline esta furada.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut4-isca-coleta-sem-autorizacao",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: afirma que desautorizado pode coletar — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    d = col.decidir_autorizacao(autorizado=False, jogo_disponivel=True)
    # A afirmacao FALSA: sem autorizacao a coleta acontece.
    C.arc.igual(d["pode_coletar"], True, "desautorizado deveria poder coletar (AFIRMACAO FALSA)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
