#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova): afirma o FALSO — a observacao do probe (sem hash por item)
vale runtime mesmo sem passar pela costura do topo.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE. Se ele PASSA, a
costura B1 esta furada: um JSON do probe sem `hash_fonte` por observacao estaria
sendo aceito como evidencia.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut5-isca-topo-sem-hash-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: observacao crua do probe (sem hash/sessao) aceita — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    fx = C.fixture("probe-saida-exemplo")
    # A afirmacao FALSA: a observacao do probe (sessao/hash so no topo) e aceita crua.
    try:
        n = col.normalizar_observacao(fx["observacoes"][0], procedencia="runtime")
    except col.ObservacaoInvalida as erro:
        # A costura B1 esta VIVA e recusou antes da afirmacao falsa: a isca TEM de
        # reprovar — e por ASSERT, nao por excecao (R-5 do CIC-5R: crash nao e prova).
        C.arc.exigir(False, "o coletor recusou a observacao sem hash/sessao (B1 viva): a isca "
                            "TEM de reprovar — %s" % erro)
    C.arc.exigir(n["ok"], "observacao sem hash deveria ser OK (AFIRMACAO FALSA — a isca tem de reprovar)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
