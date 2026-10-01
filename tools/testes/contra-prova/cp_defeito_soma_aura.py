#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA, METADE 1/2: o MESMO teste do `cp_corrigido_soma_aura.py`,
com UM defeito plantado.

O que este arquivo faz aqui: e a isca. Ele existe para o runner ter o que
reprovar. A regra do plano (docs/PLANO-DE-TESTES.md) e que todo teste tem de ser
MOSTRADO REPROVANDO - e a unica forma de mostrar isso e ter, versionado, um teste
que reprova de verdade, pelo motivo certo.

O DEFEITO (o classico do projeto, invariante 1: "todo numero exibido e o do
MOTOR - nada somado a mao"): o valor esperado foi DIGITADO, somando 20 da base
com os +20 do Omnism II e esquecendo os +100 do Worship. O motor da 44; aqui se
espera 40. Este arquivo tem de sair REPROVOU (exit 1).

Nao consertar este arquivo: o "conserto" e o `cp_corrigido_soma_aura.py`,ao lado.
Fora do bloco marcado com BLOCO-DO-DEFEITO os dois sao o MESMO arquivo (o teste
`t_prova_de_fogo.py` confere isso por comparacao de texto).
"""
import arcabouco as arc

META = {
    "nome": "contra-prova-defeito",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca da prova de fogo: tem de REPROVAR (numero somado a mao)",
}


def escala_aura(base, bonus):
    """Mathf.Round(BASE * (1 + bonus/100)) - fator e produto em FLOAT, como o motor."""
    fator = arc.f32(1.0 + arc.f32(arc.f32(bonus) / arc.f32(100.0)))
    produto = arc.f32(arc.f32(base) * fator)
    return int(round(produto))


# >>> BLOCO-DO-DEFEITO
VALOR_ESPERADO = 40  # DEFEITO PLANTADO: 20 (base) + 20 (Omnism II) somado a mao;
                     # esquece os +100 do Worship. O motor da 44.
# <<< BLOCO-DO-DEFEITO


def corpo():
    obtido = escala_aura(20, 120)  # Worship (+100) + Omnism II (+20)
    arc.igual(obtido, VALOR_ESPERADO, "worship-omnism2 (base 20, bonus 120)")


if __name__ == "__main__":
    arc.main(META, corpo)
