#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA, METADE 2/2: o MESMO teste do `cp_defeito_soma_aura.py`,
com o defeito TIRADO.

Mesma formula, mesma conta, mesma comparacao - a unica diferenca e de ONDE vem o
valor esperado: ali foi digitado a mao (40); aqui vem da fixture gerada pelo
oraculo em C# (44), que passa pelo mesmo caminho de conta do motor.

Este arquivo tem de sair PASSOU (exit 0). O par (reprova -> passa) mostrado pelo
runner `--contra-prova` e a prova de fogo do arcabouco: se o runner nao reprovar
a metade defeituosa, ele nao serve para nada; se nao aprovar esta, ele reprova
tudo por acidente.

Fora do bloco marcado com BLOCO-DO-DEFEITO os dois arquivos sao identicos.
"""
import arcabouco as arc

META = {
    "nome": "contra-prova-corrigido",
    "categoria": "pura",
    "requer": [],
    "esperado": "passar",
    "descricao": "o mesmo teste com o valor vindo do motor: tem de PASSAR",
}


def escala_aura(base, bonus):
    """Mathf.Round(BASE * (1 + bonus/100)) - fator e produto em FLOAT, como o motor."""
    fator = arc.f32(1.0 + arc.f32(arc.f32(bonus) / arc.f32(100.0)))
    produto = arc.f32(arc.f32(base) * fator)
    return int(round(produto))


# >>> BLOCO-DO-DEFEITO
def _valor_do_motor():
    esperado = arc.ler_json("soma-aura", "esperado")  # fixture gerada pelo oraculo em C#
    return {r["id"]: r["valor"] for r in esperado["resultados"]}["worship-omnism2"]


VALOR_ESPERADO = _valor_do_motor()
# <<< BLOCO-DO-DEFEITO


def corpo():
    obtido = escala_aura(20, 120)  # Worship (+100) + Omnism II (+20)
    arc.igual(obtido, VALOR_ESPERADO, "worship-omnism2 (base 20, bonus 120)")


if __name__ == "__main__":
    arc.main(META, corpo)
