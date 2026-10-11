#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) do cenario 6 - COMPOSICAO DA TOOLTIP: a ORDEM.

O DEFEITO PLANTADO: anexar a linha de auras ANTES das notas (`modo="aura_antes"`). A isca
acredita que "a composicao esta conforme" (0 defeito) e REPROVA citando o defeito de ORDEM.

A metade que PASSA e `cp_bt_composicao_ok.py`.
"""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "contra-prova-bt-composicao-ordem",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: anexar a aura antes das notas - a linha de auras deixa de ser a ULTIMA coisa anexada",
}


def corpo():
    texto, conteudos = R.material_da_composicao()
    defeitos = R.defeitos_da_composicao(texto, conteudos, modo="aura_antes")
    arc.igual(defeitos, [], "a composicao rv17 tinha de estar conforme, mas: %s" % defeitos)


if __name__ == "__main__":
    arc.main(META, corpo)
