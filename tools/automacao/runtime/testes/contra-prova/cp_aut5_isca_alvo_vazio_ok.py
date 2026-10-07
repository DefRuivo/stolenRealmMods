#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova) — A2 (COR-AUT4R, forma REAL): afirma o FALSO — o objeto
ATIVO cujo campo-alvo `texto_renderizado` foi MEDIDO VAZIO (`""`) "fecha" o
criterio (`CONFIRMADA`).

O artefato REAL do probe emite `""` (nao `null`): `GetParsedText()` devolve
`string.Empty` (medido no `lib/Unity.TextMeshPro.dll`) e `Trunc` so devolve `null`
para entrada `null`. Se esta isca PASSA, vazio conta como LIDO e a lacuna some.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut5-isca-alvo-vazio-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: alvo VAZIO ('', forma REAL do probe) fecha CONFIRMADA — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    fx = C.fixture("probe-saida-exemplo")
    plano = C.fixture("plano-exemplo")
    ctx = {"sessao": fx["sessao"], "hash_fonte": fx["hash_fonte"]}
    obs = {k: v for k, v in fx["observacoes"][0].items() if k not in ("sessao", "hash_fonte")}
    obs["texto_renderizado"] = ""                 # forma REAL do artefato
    anexada = col.anexar_contexto([obs], ctx)
    res, cod = col.consolidar(plano, anexada, "runtime", contexto=ctx,
                              alvos=["texto_renderizado"])
    # A afirmacao FALSA: o alvo medido vazio "fecha" o criterio.
    C.arc.igual(res["status"], "CONFIRMADA",
                "alvo vazio deveria fechar (AFIRMACAO FALSA — a isca tem de reprovar)")
    C.arc.igual(cod, 0, "exit 0 com alvo vazio (AFIRMACAO FALSA)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
