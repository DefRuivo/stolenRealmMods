#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova) — A6 (COR-AUT4R): afirma o FALSO — uma rodada que PEDE a
demonstracao de tooltip confirma com uma autodeclaracao `{conferiu: true}` que
NAO traz de volta o MARCADOR gerado pelo driver.

O marcador unico (`AUT4-IDA-E-VOLTA-<sessao>`) e o que amarra a prova de
ida-e-volta a ESTA rodada; sem ele (ou com outro) a prova nao conferiu. Se esta
isca PASSA, a exigencia aceita autodeclaracao sem o marcador — o defeito A6 da
COR-AUT4R segue vivo.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE.
"""
import os
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import comum as C  # noqa: E402
import t_aut4_execucao as T  # noqa: E402

META = {
    "nome": "cp-aut5-isca-ida-volta-sem-marcador",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: ida-e-volta `conferiu:true` SEM o marcador do driver confirma — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    plano = T._plano(demostrar=True)
    with tempfile.TemporaryDirectory(prefix="isca-a6m-") as raiz:
        dll = T._dll_falsa(raiz)
        # o stub emite `ida_e_volta` com `conferiu: true` mas SEM o marcador do driver.
        r, cod, _, _, _ = T._rodar(col, plano, raiz, "isca6m", dll,
                                   flags=("--ida-volta-sem-marcador",))
        # A afirmacao FALSA: sem o marcador do driver a rodada ainda confirma.
        C.arc.igual(r["status"], "CONCLUIDO",
                    "sem o marcador do driver deveria confirmar (AFIRMACAO FALSA — isca TEM de reprovar)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
