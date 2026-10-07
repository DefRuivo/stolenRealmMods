#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUT-4 — CONTROLE NEGATIVO: os casos invalidados TEM de falhar.

Le `casos-invalidos.entrada.json` e exige que o coletor RECUSE cada um. Se
qualquer caso invalido passar, este teste REPROVA — e o defeito e do coletor
(aceitou evidencia invalida), nao do dado.
"""
import comum as C

META = {
    "nome": "aut4-controle-negativo",
    "categoria": "pura",
    "requer": [],
    "descricao": "todo caso invalidado (sem procedencia, runtime sem hash, AUSENTE como OK) e recusado",
}


def corpo():
    col = C.coletor()
    dado = C.fixture("casos-invalidos")
    casos = dado["casos"]
    C.arc.exigir(casos, "a fixture de controle negativo esta vazia")

    for caso in casos:
        nome = caso["nome"]
        proc = caso.get("procedencia")
        try:
            col.normalizar_observacao(
                caso["observacao"], procedencia=proc,
                rotulo_fixture=caso.get("rotulo_fixture"))
        except col.ObservacaoInvalida as erro:
            # recusou: exigir que a recusa seja pelo motivo declarado
            C.arc.exigir(caso["espera_erro"].lower() in str(erro).lower(),
                         "caso %r recusado, mas por motivo '%s' (esperava conter %r)"
                         % (nome, erro, caso["espera_erro"]))
            continue
        except Exception as erro:
            C.arc.exigir(False, "caso %r levantou %s, esperava ObservacaoInvalida"
                         % (nome, type(erro).__name__))
        C.arc.exigir(False, "CONTROLE NEGATIVO FALHOU: o caso invalidado %r foi ACEITO" % nome)


if __name__ == "__main__":
    C.arc.main(META, corpo)
