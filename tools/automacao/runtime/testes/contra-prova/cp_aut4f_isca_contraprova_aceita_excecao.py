#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova): afirma o FALSO — um crash conta como prova no controle negativo.

R-5 do parecer CIC-5R: o runner de contra-prova aceitava qualquer `exit == 1`, e o
arcabouco converte EXCECAO INESPERADA em exit 1 — metade do controle negativo nao
provava nada. Se esta isca PASSAR, o crash voltou a contar como "reprovou como devia".
"""
import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut4f-isca-contraprova-aceita-excecao",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: crash (excecao inesperada) conta como prova — TEM de reprovar",
    "esperado": "reprovar",
}


def _runner():
    caminho = os.path.join(C.RUNTIME, "roda_testes_runtime.py")
    spec = importlib.util.spec_from_file_location("isca_runner", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def corpo():
    runner = _runner()
    saida_crash = ("RESULTADO|REPROVOU|isca|x|excecao inesperada: Traceback "
                   "(most recent call last)")
    # A afirmacao FALSA: reprovar por EXCECAO conta como prova.
    _estado, falhou = runner.classificar_contra_prova(1, saida_crash)
    C.arc.igual(falhou, False,
                "R-5: um crash deveria contar como prova (AFIRMACAO FALSA — a isca TEM de "
                "reprovar)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
