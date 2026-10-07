#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova) — A4: afirma o FALSO — o probe terminar com `status: ERRO`
(ou SEM_UI / ORCAMENTO_ESTOURADO / NAO_EXERCITADO) ainda consolida `CONFIRMADA`.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE. Se ele PASSA, o
estado terminal de falha do instrumento esta sendo ignorado no veredito (achado A4
da AUT-4R2).
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut5-isca-status-erro-confirma",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: probe com status ERRO consolida CONFIRMADA — TEM de reprovar",
    "esperado": "reprovar",
}

ALVOS = ["objeto", "texto_bruto", "texto_renderizado", "fonte", "material", "shader",
         "keywords", "cores", "geometria", "owners"]


def corpo():
    col = C.coletor()
    fx = C.fixture("probe-saida-exemplo")
    plano = C.fixture("plano-exemplo")
    obs = [{k: v for k, v in fx["observacoes"][0].items() if k not in ("sessao", "hash_fonte")}]
    saida = {"esquema": "AUT-4/1", "procedencia": "runtime", "status": "ERRO", "fase": "erro",
             "sessao": fx["sessao"], "hash_fonte": fx["hash_fonte"],
             "observacoes": obs, "prints": []}
    res, cod = col.consolidar_probe(saida, plano, alvos=ALVOS)
    # A afirmacao FALSA: o erro terminal do instrumento nao muda o veredito.
    C.arc.igual(res["status"], "CONFIRMADA",
                "probe em ERRO deveria confirmar (AFIRMACAO FALSA — a isca tem de reprovar)")
    C.arc.igual(cod, 0, "exit 0 com o instrumento em ERRO (AFIRMACAO FALSA)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
