#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PKG-5: MAO DUPLA entre versoes INEDITAS tem de REPROVAR, com motivo.

O QUE ESTE TESTE GARANTE
------------------------
O caso que a REV-10 mapeou e que nenhuma ordem de envio conserta: A declara depender de
B-1.0.0 e B declara depender de A-1.0.0, e NENHUM dos dois esta no ar. A Thunderstore nao
aceita os dois: cada upload resolveria uma referencia que ainda nao existe. O `resolver`
tem de acusar CICLO e dizer por que - nao basta reprovar em silencio.

A contra-prova e embutida: no MESMO par, se UMA das pontas ja estiver publicada, deixa de
ser ciclo (a ordem existe) e o veredito vira OK. Se os dois casos dessem o mesmo resultado,
o detector de ciclo nao estaria funcionando.
"""
import os
import sys

import arcabouco as arc

sys.path.insert(0, os.path.join(arc.raiz_do_repo(), "tools"))
import check_dependencias as cd  # noqa: E402

META = {
    "nome": "pkg5-mao-dupla-reprova",
    "categoria": "pura",
    "requer": [],
    "descricao": ("A->B e B->A, ambos ineditos, reprova como CICLO com motivo; publicar "
                  "uma das pontas desfaz o ciclo"),
}

BEPINEX = cd.DEPENDENCIA_OBRIGATORIA


def corpo():
    mao_dupla = [
        {"nome": "A", "versao": "1.0.0", "deps": [BEPINEX, "T-B-1.0.0"]},
        {"nome": "B", "versao": "1.0.0", "deps": [BEPINEX, "T-A-1.0.0"]},
    ]

    r = cd.resolver(mao_dupla, {BEPINEX}, {"A", "B"})
    arc.exigir(r["ciclo"], "o resolver NAO acusou ciclo num par de versoes ineditas "
                           "mutuamente dependentes (a mao dupla passou)")
    arc.igual(sorted(r["ciclo"]), ["A", "B"], "o ciclo tem de nomear os DOIS lados")
    ciclo_problemas = [p for p in r["problemas"] if "CICLO" in p or "MAO DUPLA" in p]
    arc.exigir(ciclo_problemas, "ha ciclo mas nenhum problema o explica: %s" % r["problemas"])
    arc.exigir("ordem" in ciclo_problemas[0] or "resolve" in ciclo_problemas[0],
               "o motivo nao diz que NENHUMA ordem resolve: %s" % ciclo_problemas[0])

    # --- CONTRA-PROVA: publicar UMA ponta (T-A-1.0.0 no ar) desfaz o ciclo.
    uma_publicada = cd.resolver(mao_dupla, {BEPINEX, "T-A-1.0.0"}, {"A", "B"})
    arc.igual(uma_publicada["ciclo"], [], "com uma ponta publicada nao ha mais ciclo")
    arc.igual(uma_publicada["problemas"], [], "com uma ponta publicada a ordem existe")
    # com T-A-1.0.0 no ar, o que sobrou e A dependendo do B-1.0.0 INEDITO -> o B sai antes.
    arc.exigir(uma_publicada["ordem"].index("B") < uma_publicada["ordem"].index("A"),
               "com T-A-1.0.0 no ar, o B (de quem o A depende) tem de sair antes do A: %s"
               % uma_publicada["ordem"])

    print("mao dupla inedita reprova (ciclo %s); com T-A-1.0.0 no ar resolve na ordem %s"
          % (r["ciclo"], uma_publicada["ordem"]))


if __name__ == "__main__":
    arc.main(META, corpo)
