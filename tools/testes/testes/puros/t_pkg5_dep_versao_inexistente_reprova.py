#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PKG-5: dependencia apontando para versao INEXISTENTE tem de REPROVAR.

O QUE ESTE TESTE GARANTE
------------------------
A regra que a Thunderstore aplica no upload (`PackageReferenceValidator(resolve=True)` ->
`No matching package found for reference`): uma dependencia `namespace-nome-versao` cuja
versao nao existe no ar NAO pode passar. O `resolver` do `tools/check_dependencias.py` e
chamado com a lista de "ja publicadas" injetada (PURO, sem rede): o caso bom (versao
publicada) tem de resolver sem problema - senao o detector estaria reprovando tudo -, e o
caso com `TimeStub-Foo-9.9.9` tem de reprovar NOMEANDO a referencia.

A contra-prova e embutida: o MESMO conjunto de dependencias, so trocando a referencia boa
por uma inexistente, tem de mudar o veredito de OK para REPROVADO. Se as duas situacoes
dessem o mesmo resultado, a regra nao estaria discriminando nada.
"""
import os
import sys

import arcabouco as arc

sys.path.insert(0, os.path.join(arc.raiz_do_repo(), "tools"))
import check_dependencias as cd  # noqa: E402

META = {
    "nome": "pkg5-dep-versao-inexistente-reprova",
    "categoria": "pura",
    "requer": [],
    "descricao": ("dependencia para versao que nao existe NAO resolve (No matching package "
                  "found); a mesma dependencia numa versao publicada resolve"),
}

BEPINEX = cd.DEPENDENCIA_OBRIGATORIA


def _casa(problemas, trecho):
    return [p for p in problemas if trecho in p]


def corpo():
    # --- caso BOM: a dependencia extra aponta para uma versao PUBLICADA -> resolve.
    bom = cd.resolver(
        [{"nome": "MeuMod", "versao": "1.0.0", "deps": [BEPINEX, "TimeStub-Foo-1.2.3"]}],
        {BEPINEX, "TimeStub-Foo-1.2.3"})
    arc.igual(bom["problemas"], [], "dep numa versao publicada tem de resolver")
    arc.exigir(not bom["ciclo"], "nao ha ciclo num caso sem dependencia mutua")

    # --- caso RUIM: a versao referida nao existe em lugar nenhum -> REPROVA.
    ruim = cd.resolver(
        [{"nome": "MeuMod", "versao": "1.0.0", "deps": [BEPINEX, "TimeStub-Foo-9.9.9"]}],
        {BEPINEX})
    arc.exigir(ruim["problemas"],
               "o resolver PASSOU uma dependencia para versao inexistente - e o defeito "
               "que a REV-10 achou (upload recusado com 'No matching package found')")
    arc.exigir(_casa(ruim["problemas"], "TimeStub-Foo-9.9.9"),
               "o motivo NAO nomeia a referencia inexistente: %s" % ruim["problemas"])
    arc.exigir(_casa(ruim["problemas"], "No matching package found"),
               "o motivo nao cita o erro da Thunderstore: %s" % ruim["problemas"])

    # --- CONTRA-PROVA: a unica diferenca e a versao; o veredito TEM de divergir.
    arc.exigir(bom["problemas"] != ruim["problemas"],
               "o detector deu o MESMO veredito para a versao publicada e para a inexistente")

    print("versao publicada resolve (%d problema(s)); versao inexistente reprova: %s"
          % (len(bom["problemas"]), ruim["problemas"][0]))


if __name__ == "__main__":
    arc.main(META, corpo)
