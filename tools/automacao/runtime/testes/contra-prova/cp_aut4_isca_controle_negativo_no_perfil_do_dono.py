#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova): afirma o FALSO — o controle negativo PODE usar o perfil do dono.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE. Se ele PASSAR, a trava
`exigir_perfil_isolado` deixou de proteger o perfil do dono e a frente poderia instalar/
medir no perfil real sem autorizacao.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comum as C  # noqa: E402

sys.path.insert(0, C.RUNTIME)
import controle_negativo as cn  # noqa: E402

META = {
    "nome": "cp-aut4-isca-controle-negativo-no-perfil-do-dono",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: afirma que o perfil do dono pode ser usado no controle negativo — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    dono = os.path.join(os.path.abspath(os.sep), "perfil-do-dono-falso")
    raiz_isolada = os.path.join(dono, "area-isolada")

    aceitou = None
    try:
        aceitou = cn.exigir_perfil_isolado(dono, dono, None, perfil_dono=dono)
    except cn.PerfilNaoIsolado as erro:
        # A TRAVA viva recusou: a isca TEM de reprovar — e por ASSERT, nao por excecao.
        C.arc.exigir(False, "a trava RECUSOU o perfil do dono (guarda viva): a isca TEM de "
                            "reprovar — RESULTADO|REPROVOU| — %s" % erro)
        return
    perfil, _out = aceitou
    # A afirmacao FALSA: "o controle negativo pode rodar no perfil do dono".
    C.arc.igual(cn._dentro(perfil, dono), True,
                "o perfil do dono deveria ser aceito como destino (AFIRMACAO FALSA)")
    C.arc.igual(cn._dentro(raiz_isolada, dono), True,
                "a raiz isolada dentro do dono deveria ser aceita (AFIRMACAO FALSA)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
