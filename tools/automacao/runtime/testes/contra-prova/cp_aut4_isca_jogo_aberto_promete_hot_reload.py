#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova): afirma o FALSO — com o jogo aberto existe HOT-RELOAD.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE. Se ele PASSAR, o driver
esta prometendo carregar a instrumentacao SEM reiniciar o jogo — exatamente a promessa que
o contrato proibe (sem instrumentacao carregada nao ha o que ler).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut4-isca-jogo-aberto-promete-hot-reload",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: afirma que jogo aberto sem probe ainda LE (hot-reload) — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    decisao = col.decidir_com_jogo_aberto(jogo_aberto=True, probe_carregado=False)
    if decisao["pode_ler"]:
        C.arc.exigir(False, "o driver declarou que LE sem instrumentacao carregada (guarda morta): "
                            "a isca TEM de reprovar — RESULTADO|REPROVOU|")
    # A afirmacao FALSA: "com o jogo aberto eu carrego o probe em quente e leio".
    C.arc.igual(decisao["hot_reload"], True,
                "deveria existir hot-reload (AFIRMACAO FALSA — a isca tem de reprovar)")
    C.arc.igual(decisao["status"], "PRONTO_PARA_LER",
                "sem o probe carregado deveria estar PRONTO_PARA_LER (AFIRMACAO FALSA)")
    C.arc.igual(decisao["reinicio_necessario"], False,
                "nao deveria exigir reinicio (AFIRMACAO FALSA)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
