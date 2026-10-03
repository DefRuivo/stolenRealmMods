#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do RSTV-19: a ISCA da posicao CRUA (o (0, 26.7) no centro da AREA).

O que este arquivo faz aqui: existe para o runner ter o que reprovar. A regra do plano
(`docs/PLANO-DE-TESTES.md`) e que todo teste seja MOSTRADO REPROVANDO — e a forma de mostrar isso num
teste que le o FONTE vivo e rodar as MESMAS checagens contra um fonte com o defeito plantado.

O DEFEITO: o container posicionado no centro da AREA (o `(0, 26.7)` cru), sem compensar que a area
fica ~64.25u abaixo do centro da janela — exatamente o layout que o dono viu (os nos no rodape,
cortados). O texto do fonte troca a linha do `DeslocamentoDoCentroDaArea(area) + YDoContainerDeNos`
pela posicao crua, em memoria, e as checagens de `tools/testes/regras_rstv19.py` TEM de reprovar.
Este arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv19_posicao_nos.py`, ao lado.
"""
import regras_rstv19 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv19-container-no-rodape",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-19: com o container no centro da AREA (o (0, 26.7) cru), as "
                  "checagens tem de REPROVAR (os nos caem no rodape e sao cortados)"),
}


def corpo():
    src = reg.fonte(reg.caminho_aba())

    # 1) A ISCA NO FONTE: a posicao crua plantada tem de ser pega.
    com_defeito = reg.fonte_sem_deslocamento(src)
    if com_defeito == src:
        raise arc.Falhou("o plantio do defeito nao encontrou a ancora "
                         "(`DeslocamentoDoCentroDaArea(area) + YDoContainerDeNos`): a isca nao esta "
                         "lendo o trecho certo")
    falhas = reg.falhas_da_posicao(com_defeito)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM num fonte com o container no centro da AREA: a "
                         "verificacao nao vale nada")
    if not any("rodape" in f or "DeslocamentoDoCentroDaArea" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pela posicao: %s"
                         % " | ".join(falhas))

    # 2) A ISCA NO MODELO: sem a compensacao o fundo do no cai no/abaixo do rodape.
    ms, mi, ac = 6.0, 8.0, 84.0
    centro_sem = reg.centro_do_container(False, ms, mi, ac)
    folga = min(reg.folga_acima_do_rodape(centro_sem, vp, 1.7, mi)
                for vp in (reg.VP_LOG, reg.VP_PADRAO))
    if folga >= reg.MARGEM_MINIMA:
        raise arc.Falhou("o modelo do defeito deu folga %.1fu (>= %.0fu): a isca nao reproduz o "
                         "corte no rodape" % (folga, reg.MARGEM_MINIMA))

    # Chegou aqui: o defeito FOI pego. Esta isca reprova de proposito, dizendo o motivo.
    raise arc.Falhou("isca: a posicao crua no centro da AREA (fundo do no a %.1fu do rodape, menos "
                     "que meio no) foi pega pela checagem - fonte: %s" % (folga, falhas[0]))


if __name__ == "__main__":
    arc.main(META, corpo)
