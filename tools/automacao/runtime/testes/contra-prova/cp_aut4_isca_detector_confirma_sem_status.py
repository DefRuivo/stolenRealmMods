#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova) — AUT-4R rodada 1: afirma o FALSO — um artefato com LEITURA VALIDA
(expectativa casando) mas SEM status de conclusao (chave `status` ausente ou vazia) ainda
CONFIRMA pelo caminho `--detectar`.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE. Se ele PASSA, o detector
esta confirmando "silencio" — o oposto do irmao `consolidar_probe` e de
`veredito_do_status(None/"")`, que tratam status ausente como INCOMPLETO
("silencio nao e aprovacao").

Reproducao do defeito (o curto-circuito antigo em `detectar_leitura`):
    status ausente/vazio -> `if st and ...` era False -> o silencio passava para CONFIRMADA.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut4-isca-detector-confirma-sem-status",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: leitura valida SEM status de conclusao confirma no --detectar — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    fx = C.fixture("cenarios-negativos")
    plano = dict(C.fixture("plano-exemplo"))
    plano["campos_alvo"] = list(fx["campos_alvo"])
    plano["esperado"] = dict(fx["expectativa"])
    obs = dict(fx["observacao_valida"])
    ctx = dict(fx["contexto"])

    for status in (None, ""):
        r, codigo = col.detectar_leitura(observacoes=[dict(obs)], plano=plano,
                                         contexto=ctx, status_probe=status)
        # A afirmacao FALSA: sem status de conclusao o detector confirma (o "silencio" passa).
        C.arc.igual(r["veredito"], col.VEREDITO_CONFIRMA,
                    "leitura valida SEM status de conclusao (%r) deveria CONFIRMAR "
                    "(AFIRMACAO FALSA — a isca TEM de reprovar)" % (status,))
        C.arc.igual(codigo, 0, "sem status de conclusao deveria dar exit 0 (AFIRMACAO FALSA)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
