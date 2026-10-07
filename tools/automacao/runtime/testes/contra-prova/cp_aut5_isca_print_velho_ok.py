#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova) — A1-c (COR-AUT4R): afirma o FALSO — um PNG de rodada
ANTERIOR, que ficou no `out_dir` REUSADO, satisfaz a prova (c) de execucao.

O `out_dir` e reusado por desenho; a rodada de hoje NAO produziu imagem (o stub
lista o caminho do print mas nao grava arquivo novo), mas existe um `01-ui.png`
velho no mesmo caminho. Se esta isca PASSA, a prova (c) nao amarra o artefato a
ESTA rodada — o defeito A1-c da COR-AUT4R segue vivo.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE.
"""
import os
import sys
import tempfile
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import comum as C  # noqa: E402
import t_aut4_execucao as T  # noqa: E402

META = {
    "nome": "cp-aut5-isca-print-velho-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: PNG de rodada ANTERIOR no out_dir confirma a rodada — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    plano = T._plano()
    with tempfile.TemporaryDirectory(prefix="isca-a1c-") as raiz:
        dll = T._dll_falsa(raiz)
        # PNG VELHO no out_dir que a rodada vai reusar (mtime 1h atras).
        out_previsto = os.path.join(raiz, "out-isca1c")
        os.makedirs(out_previsto, exist_ok=True)
        png_velho = os.path.join(out_previsto, "01-ui.png")
        with open(png_velho, "wb") as fh:
            fh.write(b"\x89PNG\r\n\x1a\n" + b"7" * 64)
        os.utime(png_velho, (time.time() - 3600.0, time.time() - 3600.0))
        # a rodada de hoje lista o print mas NAO grava imagem nova (`--print-velho`).
        r, cod, _, _, _ = T._rodar(col, plano, raiz, "isca1c", dll, flags=("--print-velho",))
        # A afirmacao FALSA: o PNG velho faz a rodada confirmar.
        C.arc.igual(r["status"], "CONCLUIDO",
                    "PNG de rodada anterior deveria confirmar (AFIRMACAO FALSA — isca TEM de reprovar)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
