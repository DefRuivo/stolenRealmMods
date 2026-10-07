#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova) — A3 (COR-AUT4R): afirma o FALSO — um artefato que declara
`evidencia_runtime: false` SOZINHO (sem `procedencia` e sem `rotulo_fixture`) e
consolidado como RUNTIME e o proprio campo declarado e INVERTIDO para `true`.

Se esta isca PASSA, a declaracao "isto NAO e evidencia de runtime" e ignorada e o
artefato vira CONFIRMADA — o defeito A3 da COR-AUT4R segue vivo.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE.
"""
import json
import os
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut5-isca-evidencia-runtime-false-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: evidencia_runtime=false sozinho vira runtime/CONFIRMADA — TEM de reprovar",
    "esperado": "reprovar",
}

ALVOS = ["objeto", "texto_bruto", "fonte", "material", "shader", "keywords",
         "cores", "geometria", "owners"]


def corpo():
    col = C.coletor()
    fx = C.fixture("probe-saida-exemplo")
    plano = C.fixture("plano-exemplo")
    # artefato SEM procedencia e SEM rotulo_fixture: so declara evidencia_runtime=false.
    artefato = {k: v for k, v in fx.items() if k not in ("procedencia", "rotulo_fixture")}
    artefato["evidencia_runtime"] = False
    fd, caminho = tempfile.mkstemp(prefix="isca-a3f2-", suffix=".json")
    os.close(fd)
    with open(caminho, "w", encoding="utf-8") as fh:
        json.dump(artefato, fh, ensure_ascii=False)
    res, cod = col.consolidar_probe(caminho, plano, alvos=ALVOS)
    # A afirmacao FALSA: o artefato que NEGA runtime vira runtime e confirma.
    C.arc.igual(res["status"], "CONFIRMADA",
                "evidencia_runtime=false deveria virar runtime (AFIRMACAO FALSA — isca TEM de reprovar)")
    C.arc.igual(res.get("evidencia_runtime"), True,
                "o campo declarado deveria ser invertido para true (AFIRMACAO FALSA)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
