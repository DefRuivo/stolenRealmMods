#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (metade OK) do cenario 6 - a regra de HOJE (rv17): ordem + linha + idempotencia."""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "contra-prova-bt-composicao-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "o MESMO teste da isca com a regra de HOJE (rv17): corpo->notas->aura, 1 linha em branco, idempotente",
}


def corpo():
    texto, conteudos = R.material_da_composicao()
    defeitos = R.defeitos_da_composicao(texto, conteudos, modo="rv17")
    arc.igual(defeitos, [], "a composicao rv17 divergiu: %s" % defeitos)


if __name__ == "__main__":
    arc.main(META, corpo)
