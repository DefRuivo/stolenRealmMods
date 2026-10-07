#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova): afirma o FALSO — campo EXTRA declarado alvo e ausente "fecha" ok.

S-3 do parecer CIC-5R (e R1 da rodada 2): `normalizar_observacao` so acumulava lacuna
para campo in CAMPOS, entao um extra (`shader_suportado`, que a B2 trouxe por design)
declarado alvo e ausente saia `ok: true`, `lacunas: []`. Se esta isca PASSAR, o alvo
declarado voltou a nao ser cobrado.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut4f-isca-campo-extra-ausente-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: campo EXTRA alvo e ausente fecha ok — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    fx = C.fixture("probe-saida-exemplo")
    ctx = {"sessao": fx["sessao"], "hash_fonte": fx["hash_fonte"]}
    obs = dict(col.anexar_contexto(fx["observacoes"], ctx)[0])
    obs["shader_suportado"] = None                      # extra declarado alvo e AUSENTE
    n = col.normalizar_observacao(obs, "runtime", alvos=["shader_suportado"])
    # A afirmacao FALSA: o extra alvo ausente nao penaliza.
    C.arc.igual(n["ok"], True,
                "S-3: campo EXTRA alvo e ausente deveria fechar ok (AFIRMACAO FALSA — a isca "
                "TEM de reprovar)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
