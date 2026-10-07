#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova): afirma o FALSO — sem autorizacao a rodada EXECUTA.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE. Se ele PASSA,
o caminho executavel esta furado: desautorizado estaria agindo (instalando probe,
lancando processo, tocando em disco).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut5-isca-sem-autorizacao-executa",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: afirma que desautorizado executa — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    plano = C.fixture("plano-exemplo")
    r, _ = col.executar_rodada(plano, perfil_dir="perfil-inexistente", out_dir="out-inexistente",
                               dll_probe="dll-inexistente", autorizado=False,
                               jogo_disponivel=False)
    # A afirmacao FALSA: desautorizado libera a execucao.
    C.arc.igual(r["status"], "AUTORIZADO", "desautorizado deveria executar (AFIRMACAO FALSA)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
