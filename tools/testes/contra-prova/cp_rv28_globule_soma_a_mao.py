#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) do RV-28 blindagem - a SOMA A MAO das tiers.

O DEFEITO PLANTADO: `pct += 8f + 20f;` no lugar de `pct += daSkill;` — a soma classica do projeto
(8 + 20 = 28), que ignora o que o JOGO tem ativo em `Character.Skills`. A isca acredita que o
defeito esta limpo e REPROVA citando a checagem que mordeu.

A metade que PASSA e `cp_rv28_globule_ok.py`.
"""
import arcabouco as arc
import regras_rv28_globule as R

META = {
    "nome": "contra-prova-rv28-globule-soma-a-mao",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: somar tier I + tier II a mao (28) no lugar da % da lista ATIVA do jogo",
}


def corpo():
    viol = R.violacoes_da_isca("B: soma a mao tier I + tier II (28)")
    arc.igual(viol, [], "a soma a mao tinha de ser aceita, mas: %s" % viol)


if __name__ == "__main__":
    arc.main(META, corpo)
