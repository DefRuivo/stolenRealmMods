#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) do cenario 2 - SUBSTITUICAO SEGURA.

O DEFEITO PLANTADO: trocar por SUBSTRING (`modo="contem"`), em vez de exigir o texto exibido
igual ao ingles original. A isca acredita que a substituicao "esta segura" (0 violacao) e
REPROVA citando o caso `chave como substring` / `mesmo comeco, texto diferente`.

A metade que PASSA e `cp_bt_substituicao_ok.py`.
"""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "contra-prova-bt-substituicao",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: trocar por substring deixa de ser seguro - texto localizado, substring e mesmo-comeco sao trocados",
}


def corpo():
    viol = R.violacoes_da_substituicao(R.le_fonte(), modo="contem")
    arc.igual(viol, [], "a substituicao segura divergiu (o defeito plantado aparece): %s" % viol)


if __name__ == "__main__":
    arc.main(META, corpo)
