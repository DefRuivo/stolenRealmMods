#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PKG-5: a ORDEM de envio sai correta - BetterFont 1.0.2 ANTES de BetterCombatText 0.1.1.

O QUE ESTE TESTE GARANTE
------------------------
O caso REAL do repositorio: o `BetterCombatText 0.1.1` declara
`DefRuivo_StolenRealmMods-BetterFont-1.0.2`, mas a 1.0.2 ainda NAO esta no ar (a ultima
publicada e a 1.0.1). A resolucao e VALIDA porque o BetterFont 1.0.2 sai no MESMO lote - e
o `resolver` tem de devolver a ordem com o BetterFont antes do BetterCombatText. E a ordem
que o pipeline precisa (o upload resolve cada referencia na hora).

A contra-prova e embutida, e e a mao dupla do caso real: se o BetterFont 1.0.2 tambem
declarasse depender do BetterCombatText 0.1.1 (ambos ineditos), o resolver tem de REPROVAR
com ciclo - porque ai nao existe ordem valida. O mesmo par de mods, com a direcao invertida,
muda o veredito de OK para CICLO.
"""
import os
import sys

import arcabouco as arc

sys.path.insert(0, os.path.join(arc.raiz_do_repo(), "tools"))
import check_dependencias as cd  # noqa: E402

META = {
    "nome": "pkg5-ordem-envio",
    "categoria": "pura",
    "requer": [],
    "descricao": ("BetterCombatText 0.1.1 -> BetterFont 1.0.2 (inedita) resolve com "
                  "BetterFont ANTES; a direcao invertida entre as duas ineditas reprova"),
}

BEPINEX = cd.DEPENDENCIA_OBRIGATORIA
TEAM = "DefRuivo_StolenRealmMods"


def corpo():
    font = {"nome": "BetterFont", "versao": "1.0.2", "deps": [BEPINEX]}
    bct = {"nome": "BetterCombatText", "versao": "0.1.1",
           "deps": [BEPINEX, "%s-BetterFont-1.0.2" % TEAM]}
    # a ultima versao do BetterFont NO AR e a 1.0.1; a 1.0.2 e nova e sai neste lote.
    no_ar = {BEPINEX, "%s-BetterFont-1.0.1" % TEAM}

    r = cd.resolver([font, bct], no_ar, {"BetterFont", "BetterCombatText"})
    arc.igual(r["problemas"], [], "o caso real (BetterFont 1.0.2 novo) tem de resolver")
    arc.exigir("BetterFont" in r["ordem"] and "BetterCombatText" in r["ordem"],
               "a ordem nao traz os dois mods: %s" % r["ordem"])
    arc.exigir(r["ordem"].index("BetterFont") < r["ordem"].index("BetterCombatText"),
               "BetterFont tem de sair ANTES do BetterCombatText: %s" % r["ordem"])

    # --- CONTRA-PROVA: a mao dupla real (inverter a direcao) entre as DUAS ineditas reprova.
    font_mao_dupla = {"nome": "BetterFont", "versao": "1.0.2",
                      "deps": [BEPINEX, "%s-BetterCombatText-0.1.1" % TEAM]}
    r2 = cd.resolver([font_mao_dupla, bct], no_ar, {"BetterFont", "BetterCombatText"})
    arc.exigir(r2["ciclo"], "a direcao invertida entre as duas versoes ineditas NAO virou ciclo")
    arc.igual(sorted(r2["ciclo"]), ["BetterCombatText", "BetterFont"],
              "o ciclo tem de nomear os dois mods do caso real")

    print("ordem do caso real: %s -> %s | invertendo a direcao: ciclo %s"
          % (r["ordem"][0], r["ordem"][-1], r2["ciclo"]))


if __name__ == "__main__":
    arc.main(META, corpo)
