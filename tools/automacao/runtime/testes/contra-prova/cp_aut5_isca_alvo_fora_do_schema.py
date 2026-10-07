#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova) — A2: afirma o FALSO — um alvo fora do schema (typo) e
simplesmente descartado e o cenario "fecha" `CONFIRMADA`.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE. Se ele PASSA,
qualquer alvo pode ser silenciosamente descartado (achado A2 da AUT-4R2).
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut5-isca-alvo-fora-do-schema",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: alvo typo fecha CONFIRMADA — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    fx = C.fixture("probe-saida-exemplo")
    plano = C.fixture("plano-exemplo")
    ctx = {"sessao": fx["sessao"], "hash_fonte": fx["hash_fonte"]}
    obs = col.anexar_contexto(fx["observacoes"], ctx)
    try:
        res, cod = col.consolidar(plano, obs, "runtime", contexto=ctx, alvos=["field_typo"])
    except col.PlanoInvalido:
        # O correto e RECUSAR o plano: a isca reprova aqui (que e o que o runner exige).
        C.arc.exigir(False, "plano com alvo fora do schema foi recusado (a isca TEM de reprovar)")
        return
    # A afirmacao FALSA: o alvo typo nao invalida nada e o desfecho fecha.
    C.arc.igual(res["status"], "CONFIRMADA",
                "alvo fora do schema deveria fechar (AFIRMACAO FALSA — a isca tem de reprovar)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
