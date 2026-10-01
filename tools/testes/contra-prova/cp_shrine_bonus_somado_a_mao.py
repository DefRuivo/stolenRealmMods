#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) do TST-2: a MESMA regra do `t_shrine_excesso_bonus.py`, com o
defeito classico plantado (invariante 1: "todo numero e o do MOTOR - nada somado a mao").

O DEFEITO: somar TODAS as fontes listadas do `ShrineEffectBonus`. Com `Omnism I`
(+8) e `Omnism II` (+20) conhecidas ao mesmo tempo, a soma a mao da **28** - mas o
motor DESCARTA a `Omnism I` (ela esta na lista `SkillsThatReplace` da II) e o
`ShrineEffectBonus` fica **20**. O proprio teste de integracao do jogo asserta o
delta de 20f (`LearnAndExpectAttributeDelta(..., "CHAOS_2_P1_Omnism II",
"ShrineEffectBonus", 20f)`, decompilado l.183505; RV-19 §3).

Este arquivo tem de sair REPROVOU (exit 1). O "conserto" e o teste da suite,
`testes/puros/t_shrine_excesso_bonus.py`.
"""
import arcabouco as arc
import regras_shrine as reg

META = {
    "nome": "contra-prova-shrine-bonus",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: soma as duas tiers a mao (28) - o motor substitui a Omnism I (20)",
}


def corpo():
    esp = reg.esperado_do_caso()
    alvo = reg.por_id(esp["bonus_total"])["omnism1-omnism2"]

    # >>> BLOCO-DO-DEFEITO
    # A soma a mao: percorre as fontes SEM aplicar a substituicao do RV-19 §3.
    total = sum(reg.FONTES[fonte] for fonte in ["Omnism I", "Omnism II"])
    # <<< BLOCO-DO-DEFEITO

    arc.igual(total, alvo["total"],
              "Omnism I + Omnism II: o motor desconta a I (20), o defeito soma as duas (28)")


if __name__ == "__main__":
    arc.main(META, corpo)
