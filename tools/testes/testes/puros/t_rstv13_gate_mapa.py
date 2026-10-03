#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RSTV-13: o botao APARECE no MAPA-MUNDO e a seguranca continua EM BATALHA.

O DEFEITO DO DONO (sintoma 5)
-----------------------------
"Passeando no mapa o botao nao aparece." O log de 02/10 mostra o botao do HUD escondido por
"nao e o turno do jogador (Root.IsPlayerTurnAndReady=false)" e "posicionamento inicial em andamento
(Root.SpawnPlacementActive)" — portoes que descrevem UMA BATALHA. No mapa eles nao valem:
`IsPlayerTurnAndReady` fica no ultimo valor do combate anterior (l.111904) e `SpawnPlacementActive`
so existe no setup da batalha (l.112152/112165). O conserto move os portoes de batalha para DENTRO
do ramo `if (estado == GUIState.InBattle)` do `RunTargets.GateOk`.

Este teste confere:
  1. NO FONTE: os portoes universais (ping/janela) estao fora do ramo de batalha e os de batalha
     (mira/spawn/turno/acting/moving) estao DENTRO dele (`falhas_do_gate_por_estado` vazia);
  2. O MODELO PURO: no MAPA o botao aparece mesmo com todos os portoes de batalha "fechados"; em
     BATALHA cada um deles bloqueia;
  3. A ISCA embutida: a regra ANTIGA (batalha valendo no mapa) BLOQUEIA o mesmo cenario de mapa que
     a regra nova libera;
  4. PROVA DE FOGO NO FONTE: com o portao de batalha reinjetado FORA do ramo, a MESMA checagem
     reprova PELO MOTIVO CERTO.

DE ONDE VEM O ESPERADO
----------------------
As regras vivem em `tools/testes/regras_rstv13.py`, lidas do fonte VIVO; a isca externa e
`tools/testes/contra-prova/cp_rstv13_batalha_no_mapa.py`.
"""
import regras_rstv13 as reg

import arcabouco as arc

META = {
    "nome": "rstv13-gate-mapa",
    "categoria": "pura",
    "requer": [],
    "descricao": ("RSTV-13: no MAPA-MUNDO os portoes de batalha (turno/spawn/mira/animacao) nao "
                  "escondem o botao; em BATALHA cada um continua bloqueando, e o defeito "
                  "'batalha valendo no mapa' reprova"),
}


def corpo():
    src = reg.fonte()
    arc.exigir(len(src) > 3000, "RunTargets.cs veio vazio/curto: a leitura mudou de lugar?")

    # 1) O FONTE: os portoes estao do lado certo do ramo de batalha.
    falhas = reg.falhas_do_gate_por_estado(src)
    arc.exigir(not falhas, "o portao por estado regrediu em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))

    # 2) MODELO PURO — no MAPA o botao APARECE mesmo com todos os portoes de batalha fechados.
    mapa = dict(reg.CENARIO)
    for campo, _ in reg.GATES_DE_BATALHA:
        mapa[campo] = False
    arc.exigir(reg.portao_por_estado("map", mapa),
               "no MAPA o portao ainda bloqueia (portoes de batalha valendo fora da batalha)")
    arc.exigir(reg.portao_por_estado("town", mapa),
               "na CIDADE (InTown) o portao ainda bloqueia")
    # ...e nao e frouxidao: os portoes UNIVERSAIS continuam bloqueando no mapa.
    for campo, _ in reg.GATES_UNIVERSAIS:
        bloqueado = dict(mapa)
        bloqueado[campo] = False
        arc.exigir(not reg.portao_por_estado("map", bloqueado),
                   "o portao universal %r deixou de bloquear no mapa" % campo)

    # 3) MODELO PURO — em BATALHA cada portao de batalha continua bloqueando.
    batalha = dict(reg.CENARIO, **{campo: True for campo, _ in reg.GATES_DE_BATALHA})
    arc.exigir(reg.portao_por_estado("battle", batalha),
               "o cenario de batalha com tudo aberto tinha de liberar")
    for campo, _ in reg.GATES_DE_BATALHA:
        bloqueado = dict(batalha)
        bloqueado[campo] = False
        arc.exigir(not reg.portao_por_estado("battle", bloqueado),
                   "o portao de batalha %r deixou de bloquear EM BATALHA" % campo)

    # 4) A ISCA: a regra ANTIGA bloqueia o MESMO cenario de mapa que a regra nova libera.
    arc.exigir(reg.portao_por_estado("map", mapa),
               "a regra nova NAO liberou o mapa (o conserto nao esta de pe)")
    arc.exigir(not reg.portao_com_batalha_no_mapa("map", mapa),
               "a regra ANTIGA liberou o mapa: a isca nao reproduz o defeito do dono")

    # 5) PROVA DE FOGO NO FONTE: com o portao de batalha FORA do ramo, a MESMA checagem reprova.
    com_defeito = reg.fonte_com_batalha_no_mapa(src)
    arc.exigir(com_defeito != src,
               "o plantio do defeito nao encontrou o ramo `%s`: a checagem nao le o trecho certo"
               % reg.RAMO_DE_BATALHA)
    falhas_defeito = reg.falhas_do_gate_por_estado(com_defeito)
    arc.exigir(len(falhas_defeito) >= 1,
               "as checagens PASSARAM num fonte com o portao de batalha valendo no mapa: elas nao "
               "pegam o defeito")
    arc.exigir(any("BATALHA" in f and "MAPA" in f for f in falhas_defeito),
               "a checagem reprovou o defeito, mas nao pelo portao valendo no MAPA: %s"
               % " | ".join(falhas_defeito))

    print("mapa LIBERA os portoes de batalha; batalha continua bloqueando por mira/spawn/turno/"
          "acting/moving; o defeito 'batalha valendo no mapa' reprova no fonte e no modelo")


if __name__ == "__main__":
    arc.main(META, corpo)
