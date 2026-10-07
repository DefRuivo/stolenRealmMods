#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova): afirma o FALSO — `--executar` sem `--perfil` estoura TypeError.

R-2 do parecer CIC-5R. O default honesto e NAO_EXERCITADO/exit 2 (o gate decide ANTES
de normalizar caminho). Se esta isca PASSAR, o caminho executavel voltou a estourar
antes de decidir — e a promessa "default nao age" quebrou.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut4f-isca-cli-sem-perfil-estoura",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: --executar sem --perfil estoura antes do gate — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    plano = C.fixture("plano-exemplo")
    try:
        col.executar_rodada(plano, perfil_dir=None, out_dir=None, dll_probe=__file__,
                            autorizado=True, jogo_disponivel=True, confirmacao="coleta")
    except TypeError:
        # A guarda viva recusou ANTES de normalizar o caminho: a isca TEM de reprovar,
        # e por ASSERT (nao por excecao — R-5 do CIC-5R).
        C.arc.exigir(False, "R-2: o gate recusou ANTES do abspath (guarda viva): a isca TEM "
                            "de reprovar")
    # A afirmacao FALSA: sem --perfil o caminho estoura antes do gate.
    C.arc.exigir(False, "R-2: --executar sem --perfil deveria estourar TypeError "
                        "(AFIRMACAO FALSA — a isca TEM de reprovar)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
