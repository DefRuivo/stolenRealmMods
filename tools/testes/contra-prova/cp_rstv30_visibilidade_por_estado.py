#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA da RSTV-30: a ISCA — a VISIBILIDADE presa ao portao (o piscar do dono).

O DEFEITO: ate a RSTV-29 o `RunButton.Mirror` escondia o botao sempre que `RunTargets.GateOk`
recusava — e o portao lia estado de batalha (turno, animacao, whitelist). Resultado em jogo: o botao
sumia quando qualquer personagem agia e nao aparecia fora do turno do jogador.

Este arquivo reinjeta o defeito no TEXTO do fonte (em memoria, sem tocar em arquivo) e roda as MESMAS
checagens de `regras_rstv30.py`, nos dois lados:

  * o fonte, pelo `falhas_da_fonte`;
  * o modelo puro: a regra ANTIGA (`visivel_antes`) tem de esconder o botao no cenario do dono e
    PISCAR ao longo da rodada.

Este arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e' a checagem.

Nao consertar este arquivo: o "conserto" e' o `t_rstv30_barra_de_baixo.py` / `t_rstv30_sem_piscar.py`.
"""
import regras_rstv30 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv30-visibilidade-por-estado",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca da RSTV-30: com a visibilidade presa ao portao (Hide quando ele recusa), o "
                  "fonte e o modelo tem de REPROVAR"),
}


def corpo():
    arquivos = reg.fontes()
    run = arquivos.get(reg.ARQUIVO_RUN, "")

    # 1) A ISCA NO FONTE: o defeito reinjetado no Mirror tem de ser pego pela checagem certa.
    com_defeito = reg.fonte_com_visibilidade_por_estado(run)
    if com_defeito == run:
        raise arc.Falhou("o plantio do defeito nao encontrou o trecho do Mirror no RunButton.cs: a "
                         "isca nao esta lendo o conserto")
    falhas = reg.falhas_da_fonte(dict(arquivos, **{reg.ARQUIVO_RUN: com_defeito}))
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM num fonte com a visibilidade presa ao portao: a "
                         "verificacao do conserto nao vale nada")
    if not any("Mirror chama `RunTargets.GateOk`" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram, mas nao pelo portao decidindo a presenca do "
                         "botao: %s" % " | ".join(falhas))

    # 2) A ISCA NO MODELO: o cenario do dono tem de ser ESCONDIDO pela regra antiga e a visibilidade
    #    antiga tem de PISCAR ao longo da rodada (e a nova, nao).
    if not reg.visivel_agora(reg.CENARIO_OUTRO_AGINDO):
        raise arc.Falhou("a regra nova NAO manteve o botao visivel no cenario do dono (o conserto "
                         "nao esta de pe)")
    if reg.visivel_antes(reg.CENARIO_OUTRO_AGINDO):
        raise arc.Falhou("a regra ANTIGA manteve o botao visivel no cenario do dono: a isca nao "
                         "reproduz o piscar")
    if reg.transicoes(reg.visivel_antes) < 3:
        raise arc.Falhou("a visibilidade antiga nao alternou o bastante ao longo da rodada (%d "
                         "transicoes): o modelo nao reproduz o defeito"
                         % reg.transicoes(reg.visivel_antes))
    if reg.transicoes(reg.visivel_agora) != 0:
        raise arc.Falhou("a visibilidade NOVA alternou ao longo da rodada: o conserto esta quebrado")

    # Chegou aqui: o defeito FOI pego. Esta isca reprova de proposito, dizendo o motivo.
    raise arc.Falhou("isca: a 'visibilidade presa ao portao' foi pega pelo fonte e pelo modelo "
                     "(esperado) — fonte: %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
