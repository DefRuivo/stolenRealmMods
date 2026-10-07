#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova): afirma o FALSO — o encerramento derruba TODAS as instancias.

R-4 do parecer CIC-5R: `taskkill /F /IM <imagem>` matava todas as instancias da
imagem, inclusive a que o dono ja tinha aberta. Se esta isca PASSAR, o driver voltou a
encerrar por imagem em vez de SO os PIDs que nasceram nesta rodada.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut4f-isca-encerrar-por-imagem-mata-todas",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: encerrar por imagem derruba todas as instancias — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    # A afirmacao FALSA: a rodada encerra TODAS as instancias da imagem (as de antes
    # inclusive). O driver correto encerra SO o PID que nasceu (300).
    decisao = col.planejar_encerramento("Stolen Realm.exe", {100, 200}, {100, 200, 300})
    C.arc.igual(decisao["pids"], [100, 200, 300],
                "R-4: deveria encerrar TODAS as instancias da imagem (AFIRMACAO FALSA — a "
                "isca TEM de reprovar)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
