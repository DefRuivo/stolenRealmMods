#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do RSTV-16: a ISCA da ABA FORA DO ARRAY PUBLICO (o "Tabbing broke").

O DEFEITO (ponto 8 dos revisores): a aba existe na tela mas NAO entra em `MenuTabManager.MenuTabs`.
`GetNextActiveTab` (l.140700) faz `Array.IndexOf(MenuTabs, SelectedMenuTab)` — fora do array a aba nao
e encontrada e o jogo loga "Tabbing broke". Aqui o append ao array e substituido por `MenuTab[] novo =
antigo;` no texto do fonte, em memoria, e as checagens de `tools/testes/regras_rstv16.py` TEM de reprovar.

Este arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv16_aba_arvores.py`, ao lado.
"""
import regras_rstv16 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv16-aba-fora-do-array",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-16: com a aba FORA do array publico MenuTabs, as checagens tem de "
                  "REPROVAR (a isca le a barra de abas sem a 4a aba no array)"),
}


def corpo():
    src_tab = reg.fonte(reg.caminho_aba())

    com_defeito = reg.fonte_com_aba_fora_do_array(src_tab)
    if com_defeito == src_tab:
        raise arc.Falhou("o plantio do defeito nao encontrou a ancora (`MenuTabs = novo`): a isca nao "
                         "esta lendo o trecho certo")
    falhas = reg.falhas_da_aba(com_defeito)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM com a aba fora do MenuTabs: a verificacao nao vale nada")
    if not any("MenuTabs" in f or "array" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pelo array publico: %s"
                         % " | ".join(falhas))

    # A isca no MODELO: a 4a aba fora do array nao e' achavel pelo GetNextActiveTab.
    if reg.aba_no_array(reg.ABAS[:-1], 3):
        raise arc.Falhou("o modelo achou a 4a aba fora do array: a isca nao reproduz o defeito")

    raise arc.Falhou("isca: a aba fora do array publico foi pega pelo fonte e pelo modelo (esperado) - "
                     "fonte: %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
