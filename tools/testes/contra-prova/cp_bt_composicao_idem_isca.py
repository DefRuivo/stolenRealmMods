#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) do cenario 6 - COMPOSICAO DA TOOLTIP: a IDEMPOTENCIA.

O DEFEITO PLANTADO: anexar SEM extrair (`modo="sem_tirar"`). Passar o prefixo de novo DUPLICA
a nota e a linha. A isca acredita que "a composicao esta conforme" (0 defeito) e REPROVA
citando a violacao de IDEMPOTENCIA.

A metade que PASSA e `cp_bt_composicao_ok.py`.
"""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "contra-prova-bt-composicao-idem",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: anexar sem extrair - a 2a passada duplica a nota e a linha (sem idempotencia)",
}


def corpo():
    _texto, conteudos = R.material_da_composicao()
    defeitos = R.defeitos_da_composicao("Corpo do jogo.", conteudos, modo="sem_tirar")
    arc.igual(defeitos, [], "a composicao rv17 tinha de estar conforme, mas: %s" % defeitos)


if __name__ == "__main__":
    arc.main(META, corpo)
