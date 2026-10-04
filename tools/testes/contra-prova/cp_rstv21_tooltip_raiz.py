#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do RSTV-21/22: a ISCA do TOOLTIP SEM REPARENT (o tooltip atras do fundo).

O DEFEITO (bug REAL de 03/10, relatado pelo dono como "botao morto"/tooltip ilegivel): o `ElevarTooltip`
erguia o canvas RAIZ da UI ('GUI Manager', que contém o modal) via `overrideSorting` e o jogo INTEIRO
passava a desenhar ACIMA da janela do mod. A solucao RSTV-22 e REPARENTAR o tooltip para DENTRO da
janela (`gui.tooltip.transform.SetParent`), sem tocar em ordenacao nenhuma.

Aqui o reparent e' removido, em memoria, e as checagens de `tools/testes/regras_rstv21.py` TEM de
reprovar (o tooltip ficaria desenhado atras do fundo escuro, ilegivel).

Este arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv21_janela_propria.py`, ao lado.
"""
import regras_rstv21 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv21-tooltip-raiz",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-22: com o ElevarTooltip SEM reparentar o tooltip para dentro da janela, "
                  "as checagens tem de REPROVAR (o tooltip ficaria atras do fundo, ilegivel)"),
}


def corpo():
    src = reg.fonte(reg.caminho_janela())

    com_defeito = reg.fonte_com_tooltip_raiz(src)
    if com_defeito == src:
        raise arc.Falhou("o plantio do defeito nao encontrou a ancora (o `SetParent` do reparent): a "
                         "isca nao esta lendo o trecho certo")

    falhas = reg.falhas_da_janela(com_defeito)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM com o ElevarTooltip sem reparentar o tooltip: a "
                         "verificacao nao vale nada")
    if not any("REPARENTA" in f or "SetParent" in f or "tooltip" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pelo reparent: %s"
                         % " | ".join(falhas))

    raise arc.Falhou("isca: o tooltip sem reparent foi pego pela checagem (esperado) - fonte: %s"
                     % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
