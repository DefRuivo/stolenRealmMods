#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do RSTV-21: a ISCA da SIMETRIA QUEBRADA DO TOOLTIP.

Duas quebras, uma de cada lado da simetria `ElevarTooltip` (guarda) -> `RestaurarTooltip` (devolve):

  (a) `ElevarTooltip` NAO guarda os valores antigos (ordem/override) do canvas do tooltip — o
      `RestaurarTooltip` deixaria de ter o que devolver; e
  (b) `RestaurarTooltip` virando no-op — o canvas do tooltip do jogo continuaria com a ordenacao
      alterada depois de fechar a janela.

A checagem antiga so olhava a PRESENCA dos nomes `RestaurarTooltip`/`overrideSorting` e passava nos
dois casos. A checagem nova exige a SIMETRIA e TEM de reprovar.

Este arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv21_janela_propria.py`, ao lado.
"""
import regras_rstv21 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv21-tooltip-assimetrico",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-21: com o `ElevarTooltip` sem guardar os valores antigos OU o "
                  "`RestaurarTooltip` virado no-op, as checagens tem de REPROVAR"),
}


def corpo():
    src = reg.fonte(reg.caminho_janela())

    # (a) ElevarTooltip NAO guarda os valores antigos.
    sem_guarda = reg.fonte_sem_guardar_tooltip(src)
    if sem_guarda == src:
        raise arc.Falhou("o plantio 'ElevarTooltip sem guardar' nao encontrou as atribuicoes dos "
                         "valores antigos: a isca nao esta lendo o trecho certo")
    falhas_guarda = reg.falhas_da_janela(sem_guarda)
    if not any("guarda" in f or "ElevarTooltip" in f for f in falhas_guarda):
        raise arc.Falhou("as checagens PASSARAM (ou reprovaram por outro motivo) com o "
                         "`ElevarTooltip` sem guardar os valores antigos: %s" % " | ".join(falhas_guarda))

    # (b) RestaurarTooltip virado no-op.
    noop = reg.fonte_com_restaurar_noop(src)
    if noop == src:
        raise arc.Falhou("o plantio 'RestaurarTooltip no-op' nao encontrou as atribuicoes que "
                         "devolvem os valores antigos: a isca nao esta lendo o trecho certo")
    falhas_noop = reg.falhas_da_janela(noop)
    if not any("RestaurarTooltip" in f or "devolve" in f for f in falhas_noop):
        raise arc.Falhou("as checagens PASSARAM (ou reprovaram por outro motivo) com o "
                         "`RestaurarTooltip` virado no-op: %s" % " | ".join(falhas_noop))

    raise arc.Falhou("isca: as duas quebras de simetria do tooltip foram pegas (esperado) - "
                     "fonte: %s" % falhas_noop[0])


if __name__ == "__main__":
    arc.main(META, corpo)
