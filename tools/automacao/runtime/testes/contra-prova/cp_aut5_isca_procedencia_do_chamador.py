#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova) — A3: afirma o FALSO — o chamador dizer `procedencia='runtime'`
maquia um artefato ROTULADO como fixture e ele fecha `CONFIRMADA`.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE. Se ele PASSA, um
fixture rotulado pode ser apresentado como leitura de jogo (achado A3 da AUT-4R2).
"""
import json
import os
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut5-isca-procedencia-do-chamador",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: 'runtime' do chamador vence o rotulo do artefato — TEM de reprovar",
    "esperado": "reprovar",
}

ALVOS = ["objeto", "texto_bruto", "fonte", "material", "shader", "keywords",
         "cores", "geometria", "owners"]


def corpo():
    col = C.coletor()
    fx = C.fixture("probe-saida-exemplo")
    plano = C.fixture("plano-exemplo")
    fd, caminho = tempfile.mkstemp(prefix="isca-a3-", suffix=".json")
    os.close(fd)
    with open(caminho, "w", encoding="utf-8") as fh:
        json.dump(fx, fh, ensure_ascii=False)      # procedencia: fixture, rotulo declarado
    res, cod = col.consolidar_probe(caminho, plano, alvos=ALVOS, procedencia="runtime")
    # A afirmacao FALSA: a intencao do chamador transforma fixture rotulada em runtime.
    C.arc.igual(res["status"], "CONFIRMADA",
                "fixture rotulada deveria virar runtime (AFIRMACAO FALSA — a isca tem de reprovar)")
    C.arc.igual(res.get("evidencia_runtime"), True, "fixture deveria virar evidencia_runtime (FALSO)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
