#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova) — t_ef6e8a29: afirma o FALSO — um runbook com HASH VELHO
(ou sem uma chave do `.cfg`) continua "conforme" a trava do disco.

Se esta isca PASSAR, `t_aut4_runbook.py` virou decoracao: o operador leria um
runbook que declara a identidade de OUTRA build — exatamente o defeito A7 que o
`t_aut4_estado_docs.py` trava para o estado, so que no documento que o dono le
antes de autorizar a rodada em jogo.
"""
import importlib.util
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut4-isca-runbook-hash-velho",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: runbook com hash velho / chave de cfg faltando passaria — TEM de reprovar",
    "esperado": "reprovar",
}


def _teste():
    caminho = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "t_aut4_runbook.py")
    spec = importlib.util.spec_from_file_location("t_aut4_runbook_isca", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def corpo():
    T = _teste()
    hashes = T.hashes_do_disco()
    chaves = T.cfg_chaves()
    n_testes, n_iscas = T.contagens()
    with open(os.path.join(C.dir_docs(), T.RUNBOOK), encoding="utf-8") as fh:
        bom = fh.read()

    # (1) HASH VELHO: troca o sha256 da DLL do probe por um antigo (ex.: o de uma
    # build anterior do MESMO fonte — a DLL nao e reproduzivel byte a byte).
    dll_velho = "0" * 64
    torto = bom.replace(hashes["DLL do probe"], dll_velho)
    C.arc.igual(T.checar(torto, hashes, chaves, n_testes, n_iscas), [],
                "runbook com hash de DLL VELHO deveria passar (AFIRMACAO FALSA — a isca "
                "TEM de reprovar)")

    # (2) CHAVE DE CFG FALTANDO: apaga a porta OPT-IN de ida-e-volta do documento.
    torto2 = bom.replace("DemostrarTooltip", "DEMOSTRAR_REMOVIDO")
    C.arc.igual(T.checar(torto2, hashes, chaves, n_testes, n_iscas), [],
                "runbook sem a chave DemostrarTooltip deveria passar (AFIRMACAO FALSA — a "
                "isca TEM de reprovar)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
