#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova) — A2: afirma o FALSO — o objeto INATIVO cujo campo-alvo
(`texto_renderizado`) NAO foi lido "fecha" o criterio (`CONFIRMADA`).

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE. Se ele PASSA, o
fallback declarado do inativo esta sendo usado como satisfacao do criterio — o alvo
deixa de governar o veredito (achado A2 da AUT-4R2).
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut5-isca-alvo-nao-lido-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: alvo NAO_APLICAVEL fecha CONFIRMADA — TEM de reprovar",
    "esperado": "reprovar",
}

ALVOS_COM_RENDER = ["objeto", "texto_bruto", "texto_renderizado", "fonte", "material",
                    "shader", "keywords", "cores", "geometria", "owners"]


def corpo():
    col = C.coletor()
    fx = C.fixture("probe-saida-exemplo")
    plano = C.fixture("plano-exemplo")
    ctx = {"sessao": fx["sessao"], "hash_fonte": fx["hash_fonte"]}
    obs = col.anexar_contexto([fx["observacoes"][1]], ctx)     # a INATIVA (rendered = null)
    res, cod = col.consolidar(plano, obs, "runtime", contexto=ctx, alvos=ALVOS_COM_RENDER)
    # A afirmacao FALSA: o alvo nao lido nao impede o desfecho.
    C.arc.igual(res["status"], "CONFIRMADA",
                "alvo nao lido deveria fechar (AFIRMACAO FALSA — a isca tem de reprovar)")
    C.arc.igual(cod, 0, "exit 0 com alvo nao lido (AFIRMACAO FALSA)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
