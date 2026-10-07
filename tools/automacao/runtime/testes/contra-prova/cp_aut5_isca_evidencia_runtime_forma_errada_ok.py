#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova) — A3/COR-AUT4-F3: afirma o FALSO — um artefato que traz a
FORMA ERRADA de `evidencia_runtime` (a STRING "false" ou o inteiro 0, em vez do
bool JSON `false`) NAO satisfaz `is False` e por isso e consolidado como RUNTIME
(`CONFIRMADA`, campo invertido para `true`).

E a mesma classe de defeito que a COR-AUT4-F2 fechou (forma de dado que o jogo nao
produz passando como valida): a forma errada confirma em vez de ser recusada.

Se esta isca PASSA, um artefato com `evidencia_runtime: "false"` (string) ou `0`
CONFIRMA — o defeito da COR-AUT4-F3 segue vivo. Com a correcao (`is False` cru ->
recusa de qualquer forma nao-canonica) ela REPROVA.

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
    "nome": "cp-aut5-isca-evidencia-runtime-forma-errada-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: evidencia_runtime como STRING \"false\"/inteiro 0 vira runtime/CONFIRMADA "
                 "— TEM de reprovar",
    "esperado": "reprovar",
}

ALVOS = ["objeto", "texto_bruto", "fonte", "material", "shader", "keywords",
         "cores", "geometria", "owners"]


def corpo():
    col = C.coletor()
    fx = C.fixture("probe-saida-exemplo")
    plano = C.fixture("plano-exemplo")
    # A FORMA ERRADA de verdade: o probe C# grava o bool; nenhum artefato real traz
    # a STRING "false" nem o inteiro 0 — e justamente por isso a trava tem de recusar.
    for forma in ("false", 0, "0"):
        artefato = {k: v for k, v in fx.items() if k not in ("procedencia", "rotulo_fixture")}
        artefato["evidencia_runtime"] = forma
        fd, caminho = tempfile.mkstemp(prefix="isca-a3f3-", suffix=".json")
        os.close(fd)
        with open(caminho, "w", encoding="utf-8") as fh:
            json.dump(artefato, fh, ensure_ascii=False)
        res, cod = col.consolidar_probe(caminho, plano, alvos=ALVOS)
        # A afirmacao FALSA: a forma errada de "nao-runtime" vira runtime e confirma.
        C.arc.igual(res["status"], "CONFIRMADA",
                    "evidencia_runtime=%r deveria virar runtime (AFIRMACAO FALSA — a isca "
                    "TEM de reprovar)" % (forma,))
        C.arc.igual(res.get("evidencia_runtime"), True,
                    "o campo declarado com a forma errada %r deveria ser invertido para true "
                    "(AFIRMACAO FALSA)" % (forma,))
        C.arc.igual(cod, 0, "exit 0 com a forma errada %r (AFIRMACAO FALSA)" % (forma,))


if __name__ == "__main__":
    C.arc.main(META, corpo)
