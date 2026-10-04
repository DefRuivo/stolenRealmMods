#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do RSTV-21: a ISCA do FUNDO QUE DEIXOU DE CONSUMIR O CLIQUE.

O DEFEITO: o FUNDO da janela (`RstvWindowBackdrop`) para de consumir o clique
(`fundoImg.raycastTarget = false`) enquanto a MOLDURA continua com `raycastTarget = true`. A
checagem ANTIGA (`"raycastTarget = true" in efetivo`) passava mesmo assim — o trecho da moldura a
satisfazia. A checagem nova amarra a Image DO FUNDO e TEM de reprovar.

Este arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv21_janela_propria.py`, ao lado.
"""
import regras_rstv21 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv21-fundo-sem-raycast",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-21: com o FUNDO da janela sem consumir o clique (a moldura ainda com "
                  "`raycastTarget = true`), as checagens tem de REPROVAR"),
}


def corpo():
    src = reg.fonte(reg.caminho_janela())

    com_defeito = reg.fonte_com_fundo_sem_raycast(src)
    if com_defeito == src:
        raise arc.Falhou("o plantio 'fundo sem raycast' nao encontrou a Image do FUNDO "
                         "(`RstvWindowBackdrop`): a isca nao esta lendo o trecho certo")

    # SANIDADE DA ISCA: a moldura AINDA tem `raycastTarget = true` (era isso que enganava a
    # checagem antiga por texto solto).
    if "raycastTarget = true" not in com_defeito:
        raise arc.Falhou("a isca nao reproduz o caso: a moldura tambem perdeu o `raycastTarget = true`")

    falhas = reg.falhas_da_janela(com_defeito)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM com o FUNDO sem consumir o clique: a verificacao "
                         "nao vale nada")
    if not any("FUNDO" in f or "RstvWindowBackdrop" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pelo FUNDO: %s" % " | ".join(falhas))

    raise arc.Falhou("isca: o FUNDO sem consumir o clique foi pego (esperado) - fonte: %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
