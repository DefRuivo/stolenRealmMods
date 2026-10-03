#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) do TST-2: a MESMA regra do `t_shrine_excesso_agregado.py`, com o
DEFEITO DO PRINT DO DONO plantado.

O que este arquivo faz aqui: e a isca. A regra do plano (docs/PLANO-DE-TESTES.md) e
que todo teste tem de ser MOSTRADO REPROVANDO - e a unica forma de mostrar isso e
ter, versionado, um teste que reprova de verdade, PELO MOTIVO CERTO.

O DEFEITO (achado em jogo em 30/09, RV-46): a linha `Your active shrine auras:`
somava a contribuicao de CADA ENTRADA da lista viva. Cada (re)entrada na area do
ground effect cria um status NOVO, entao a MESMA aura aparecia 3x e a linha saiu
`Dodge +120%` - com a aura valendo 40 (o numero que a linha branca do shrine
mostra). A conta certa usa a lista DESDUPLICADA (AurasUnicas, ShrineAuraPatch.cs
1296 · `AurasUnicas()`): `Dodge +40% (total +57%)`.

Este arquivo tem de sair REPROVOU (exit 1). O "conserto" e o teste da suite,
`testes/puros/t_shrine_excesso_agregado.py`, que e o mesmo cenario sem o defeito.
"""
import arcabouco as arc
import regras_shrine as reg

META = {
    "nome": "contra-prova-shrine-instancias",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: conta CADA INSTANCIA da aura viva (o defeito do `Dodge +120%`)",
}


def corpo():
    ent = reg.entrada_do_caso()
    esp = reg.esperado_do_caso()
    ctx = reg.contexto(ent)
    cena = reg.por_id(ent["agregado"])["rogue-x3-stacks-1"]
    alvo = reg.por_id(esp["agregado"])["rogue-x3-stacks-1"]

    # >>> BLOCO-DO-DEFEITO
    # A conta percorre a LISTA VIVA (as 3 instancias) em vez da desduplicada: e o
    # codigo anterior ao RV-46.
    contribuicao = 0
    for viva in cena["vivas"]:
        for _ in range(viva["instancias"]):
            contribuicao += reg.escala(ctx["auras"][viva["aura"]]["DodgeChance"],
                                       ctx["bonus"]["worship"])
    # <<< BLOCO-DO-DEFEITO

    arc.igual(reg.item("DodgeChance", contribuicao, 57), alvo["itens"][0],
              "rogue-x3 (o DEFEITO DO PRINT): a aura repetida 3x na lista viva")


if __name__ == "__main__":
    arc.main(META, corpo)
