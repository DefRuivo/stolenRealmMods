#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PKG-5: dependencia para versao JA PUBLICADA tem de PASSAR (sem exigir ordem).

O QUE ESTE TESTE GARANTE
------------------------
O outro lado da regra: se a versao referida JA esta no ar, a resolucao e verdadeira
sozinha - nao depende de ordem de envio, e o `resolver` nao pode reprovar. Vale para um
pacote EXTERNO (`TimeStub-Foo-1.2.3`) e para um mod DESTE repositorio apontando para uma
versao antiga que continua publicada (`BetterFont 1.0.1`): a Thunderstore aceita as duas
(a restricao de "so a versao de hoje" e do `valida_pacotes.py`, nao da resolucao).

A contra-prova e embutida: trocar a versao publicada por uma INEXISTENTE tem de desligar o
"passa" e acender o problema - senao este teste estaria so confirmando um resolver que
nunca reprova.
"""
import os
import sys

import arcabouco as arc

sys.path.insert(0, os.path.join(arc.raiz_do_repo(), "tools"))
import check_dependencias as cd  # noqa: E402

META = {
    "nome": "pkg5-dep-publicada-passa",
    "categoria": "pura",
    "requer": [],
    "descricao": ("dependencia para versao ja publicada resolve sem ordem (externa e de mod "
                  "deste repo); trocar por versao inexistente reprova"),
}

BEPINEX = cd.DEPENDENCIA_OBRIGATORIA
TEAM = "DefRuivo_StolenRealmMods"


def corpo():
    entradas = [
        {"nome": "MeuMod", "versao": "2.0.0",
         "deps": [BEPINEX, "TimeStub-Foo-1.2.3", "%s-BetterFont-1.0.1" % TEAM]},
    ]
    publicadas = {BEPINEX, "TimeStub-Foo-1.2.3", "%s-BetterFont-1.0.1" % TEAM}

    ok = cd.resolver(entradas, publicadas, {"MeuMod"})
    arc.igual(ok["problemas"], [], "versao publicada (externa e do repo) tem de resolver")
    arc.igual(ok["ciclo"], [], "sem dependencia mutua nao ha ciclo")
    arc.exigir(ok["resolvidas"] and all("ja publicada" in r for r in ok["resolvidas"]),
               "as tres dependencias deviam resolver por 'ja publicada': %s" % ok["resolvidas"])

    # --- CONTRA-PROVA: sem a versao do BetterFont no ar, o mesmo manifest reprova.
    sem_publicada = cd.resolver(entradas, {BEPINEX, "TimeStub-Foo-1.2.3"}, {"MeuMod"})
    arc.exigir(sem_publicada["problemas"],
               "tirar a versao publicada do conjunto NAO reprovou - o teste nao discrimina")

    print("3 dependencias publicadas resolvem sem ordem; sem a versao no ar: %d problema(s)"
          % len(sem_publicada["problemas"]))


if __name__ == "__main__":
    arc.main(META, corpo)
