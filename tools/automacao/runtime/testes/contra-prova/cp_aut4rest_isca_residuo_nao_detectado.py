#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova): afirma o FALSO — residuo no perfil conta como restauracao.

AUD-1: se o arquivo criado pela rodada FICAR no perfil, a rodada NAO pode ser
apresentada como limpa. Se esta isca PASSAR, `verificar_sem_residuo` deixou de
detectar efeito residual (era o defeito: rollback "exato" sem prova pos-rollback).
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut4rest-isca-residuo-nao-detectado",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: residuo no perfil passa por 'limpo' — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    with tempfile.TemporaryDirectory(prefix="cp-aut4rest-res-") as perfil:
        antes = {}
        dirs_antes = set()
        residuo = os.path.join(perfil, "BepInEx", "plugins", "mod", "sobrou.dll")
        os.makedirs(os.path.dirname(residuo))
        with open(residuo, "wb") as fh:
            fh.write(b"residuo-de-verdade")
        # A afirmacao FALSA: um perfil com residuo continua "limpo".
        r = col.verificar_sem_residuo(perfil, [], antes, dirs_antes)
        C.arc.igual(r["limpo"], True,
                    "AUD-1: com arquivo criado sobrando, a restauracao deveria ser 'limpa' "
                    "(AFIRMACAO FALSA — a isca TEM de reprovar)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
