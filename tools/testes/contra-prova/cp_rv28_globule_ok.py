#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (metade OK) do RV-28 blindagem - a regra de HOJE.

O MESMO teste da isca (`cp_rv28_globule_soma_a_mao.py`), sobre o FONTE VIVO: a % sai da lista ATIVA
do jogo e nao ha soma a mao nenhuma.
"""
import arcabouco as arc
import regras_rv28_globule as R

META = {
    "nome": "contra-prova-rv28-globule-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "o MESMO teste da isca com a regra de HOJE: as guardas do fonte vivo passam",
}


def corpo():
    viol = R.guardas_do_globule(R.le_fonte())
    arc.igual(viol, [], "as guardas do fonte vivo divergiram: %s" % viol)


if __name__ == "__main__":
    arc.main(META, corpo)
