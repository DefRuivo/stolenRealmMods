#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova): afirma o FALSO — o backup do log nao deixa registro.

AUD-1: um boot TRUNCA o `LogOutput.log`, entao o backup e a unica memoria do que
havia antes; sem bytes/sha256 no registro nao ha manifesto nem prova da restauracao.
Se esta isca PASSAR, `backup_do_log` voltou a copiar o log sem registrar nada.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import comum as C  # noqa: E402

META = {
    "nome": "cp-aut4rest-isca-backup-log-sem-registro",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: backup do log sem bytes/sha256 — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    with tempfile.TemporaryDirectory(prefix="cp-aut4rest-bkp-") as raiz:
        log = os.path.join(raiz, "BepInEx", "LogOutput.log")
        os.makedirs(os.path.dirname(log))
        with open(log, "wb") as fh:
            fh.write(b"LOG-DO-DONO\n")
        registro = col.backup_do_log(log, raiz)
        # A afirmacao FALSA: o registro do backup nao declara o conteudo arquivado.
        C.arc.igual(registro.get("sha256"), None,
                    "AUD-1: o backup do log deveria sair SEM sha256 declarado "
                    "(AFIRMACAO FALSA — a isca TEM de reprovar)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
