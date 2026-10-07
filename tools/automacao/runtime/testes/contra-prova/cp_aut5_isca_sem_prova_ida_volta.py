#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova) — A6: afirma o FALSO — um plano que PEDE a demonstracao de
tooltip (`demostrar_tooltip`) confirma a rodada mesmo sem NENHUMA prova de
ida-e-volta no artefato.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE. Se ele PASSA, o
criterio do aceite ("prova reproduzivel de leitura ida-e-volta") nao tem instrumento
nem exigencia (achado A6 da AUT-4R2).
"""
import os
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import comum as C  # noqa: E402
import t_aut4_execucao as T  # noqa: E402

META = {
    "nome": "cp-aut5-isca-sem-prova-ida-e-volta",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: plano que pede ida-e-volta confirma sem a prova — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    plano = T._plano(demostrar=True)
    with tempfile.TemporaryDirectory(prefix="isca-a6-") as raiz:
        dll = T._dll_falsa(raiz)
        # o stub NAO emite `ida_e_volta` (nenhuma prova de leitura ida-e-volta)
        r, cod, _, _, _ = T._rodar(col, plano, raiz, "isca6", dll)
        # A afirmacao FALSA: sem a prova de ida-e-volta a rodada ainda confirma.
        C.arc.igual(r["status"], "CONCLUIDO",
                    "sem prova de ida-e-volta deveria confirmar (AFIRMACAO FALSA — isca TEM de reprovar)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
