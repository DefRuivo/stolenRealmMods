#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUT-4 — a observacao tem procedencia e nunca maquia AUSENTE como OK.

Regras provadas aqui:
  * toda observacao carrega procedencia (runtime | fixture);
  * fixture NUNCA vira evidencia de runtime (evidencia_runtime=false + rotulo);
  * procedencia=runtime exige sessao e hash de fonte nao vazios;
  * campo AUSENTE/INDETERMINADO nunca conta como OK.
"""
import comum as C

META = {
    "nome": "aut4-observacao",
    "categoria": "pura",
    "requer": [],
    "descricao": "procedencia obrigatoria, runtime exige hash/sessao, AUSENTE nunca e OK",
}

CAMPOS = ("objeto", "texto_bruto", "texto_renderizado", "fonte", "material", "shader",
          "keywords", "cores", "geometria", "owners", "personagem")


def corpo():
    col = C.coletor()
    fx = C.fixture("observacao-fixture-exemplo")

    # fixture: aceita, mas marcada como NAO-evidencia
    n = col.normalizar_observacao(fx["observacao"], procedencia="fixture",
                                  rotulo_fixture=fx["rotulo_fixture"])
    C.arc.igual(n["evidencia_runtime"], False, "fixture nao e evidencia de runtime")
    C.arc.igual(n["rotulo_fixture"], fx["rotulo_fixture"], "rotulo da fixture preservado")
    C.arc.igual(n["ok"], False, "fixture nunca fecha OK")
    for campo in CAMPOS:
        C.arc.exigir(campo in n["campos"], "campo %r ausente do schema normalizado" % campo)

    # runtime completo: precisa de sessao + hash_fonte e fecha ok se nao ha lacuna
    obs_rt = dict(fx["observacao"])
    obs_rt["sessao"] = "2026-10-05T15:00:00"
    obs_rt["hash_fonte"] = "a" * 64
    rt = col.normalizar_observacao(obs_rt, procedencia="runtime")
    C.arc.igual(rt["evidencia_runtime"], True, "runtime e evidencia")
    C.arc.exigir(rt["ok"], "observacao completa de runtime fecha ok")

    # runtime sem hash -> recusa (evidencia fabricada)
    try:
        col.normalizar_observacao({"sessao": "s", "objeto": "X"}, procedencia="runtime")
    except col.ObservacaoInvalida:
        pass
    else:
        C.arc.exigir(False, "runtime sem hash_fonte foi aceito")

    # campo AUSENTE declarado OK -> recusa
    try:
        col.normalizar_observacao({"texto_bruto": "AUSENTE", "status": "OK"},
                                  procedencia="fixture", rotulo_fixture="x")
    except col.ObservacaoInvalida:
        pass
    else:
        C.arc.exigir(False, "AUSENTE marcado como OK foi aceito")

    # fixture sem rotulo -> recusa, nao da para distinguir de runtime
    try:
        col.normalizar_observacao(fx["observacao"], procedencia="fixture")
    except col.ObservacaoInvalida:
        pass
    else:
        C.arc.exigir(False, "fixture sem rotulo foi aceita")


if __name__ == "__main__":
    C.arc.main(META, corpo)
