#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do portao por estado (RSTV-13): a ISCA.

O DEFEITO: o portao de batalha (`Root.SpawnPlacementActive`, e com ele os de turno/animacao) valendo
em QUALQUER estado — inclusive passeando no MAPA-MUNDO. E o comportamento pre-RSTV-13 que produziu o
sintoma (5) do dono. Este arquivo reinjeta o portao FORA do ramo `if (estado == GUIState.InBattle)`
no texto do fonte (em memoria, sem tocar em arquivo) e as checagens de `regras_rstv13.py` TEM de
reprovar. Este arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv13_gate_mapa.py`, ao lado.
"""
import regras_rstv13 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv13-batalha-no-mapa",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-13: com o portao de batalha valendo no MAPA (fora do ramo "
                  "InBattle), o fonte e o modelo tem de REPROVAR"),
}


def corpo():
    src = reg.fonte()

    # 1) A ISCA NO FONTE: o portao de batalha reinjetado FORA do ramo tem de ser pego.
    com_defeito = reg.fonte_com_batalha_no_mapa(src)
    if com_defeito == src:
        raise arc.Falhou("o plantio do defeito nao encontrou o ramo `%s`: a isca nao esta lendo o "
                         "trecho certo" % reg.RAMO_DE_BATALHA)
    falhas = reg.falhas_do_gate_por_estado(com_defeito)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM num fonte com o portao de batalha valendo no mapa: "
                         "a verificacao do conserto nao vale nada")
    if not any("BATALHA" in f and "MAPA" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pelo portao valendo no MAPA: %s"
                         % " | ".join(falhas))

    # 2) A ISCA NO MODELO: o cenario de mapa que a regra NOVA libera tem de ser BLOQUEADO pela ANTIGA.
    mapa = dict(reg.CENARIO)
    for campo, _ in reg.GATES_DE_BATALHA:
        mapa[campo] = False
    if not reg.portao_por_estado("map", mapa):
        raise arc.Falhou("a regra nova NAO liberou o mapa (o conserto nao esta de pe)")
    if reg.portao_com_batalha_no_mapa("map", mapa):
        raise arc.Falhou("a regra antiga liberou o mapa: a isca nao reproduz o defeito do dono")

    # Chegou aqui: o defeito FOI pego. Esta isca reprova de proposito, dizendo o motivo.
    raise arc.Falhou("isca: o 'portao de batalha valendo no mapa' foi pego pelo fonte e pelo modelo "
                     "(esperado) - fonte: %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
