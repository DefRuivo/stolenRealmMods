#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) do cenario 4 - TEXTO DO JOGO AUSENTE OU INESPERADO.

O DEFEITO PLANTADO: o funil SEM guarda (`modo="cru"`). A excecao de uma expressao que nao
avalia ESCAPA do patch e o texto do jogo pode sair pela metade. A isca acredita que "o texto
ficou intacto" (0 violacao) e REPROVA citando a excecao que escapou.

A metade que PASSA e `cp_bt_texto_ausente_ok.py`.
"""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "contra-prova-bt-texto-ausente",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: sem o snapshot+try/catch, a expressao que nao avalia ESCAPA e o texto do jogo nao fica intacto",
}


def corpo():
    viol = R.violacoes_do_funil("cru")
    arc.igual(viol, [], "o texto do jogo tinha de ficar intacto, mas: %s" % viol)


if __name__ == "__main__":
    arc.main(META, corpo)
