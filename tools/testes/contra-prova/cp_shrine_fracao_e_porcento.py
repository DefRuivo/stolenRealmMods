#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) do TST-2: a MESMA regra do `t_shrine_excesso_formatacao.py`, com o
DEFEITO DE FORMATO plantado (o formato anterior ao RV-45).

O DEFEITO: o numero saia do float CRU, formatado com `ToString("0.#")` - a fracao
do equipamento aparecia na tela (`(total +53.4%)`, o print do dono) e o rotulo
ficava `+53.4%%` quando a etiqueta ja terminava em `%`. A convencao do jogo e a da
FICHA (`Mathf.Ceil` + inteiro, `ShrineAuraPatch.cs` l.950 `InteiroDoJogo`) e o
sinal e lido DEPOIS do arredondamento (l.924 `ComSinal`).

Os dois defeitos do plano aparecem juntos aqui: "valor fracionario do equipamento
(convencao do Ceil do jogo)" e "UM sinal de porcentagem (nunca dois)".

Este arquivo tem de sair REPROVOU (exit 1). O "conserto" e o teste da suite,
`testes/puros/t_shrine_excesso_formatacao.py`.
"""
import arcabouco as arc
import regras_shrine as reg

META = {
    "nome": "contra-prova-shrine-formato",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: o inteiro da ficha virou o float cru com dois sinais de porcentagem",
}

PREFIXO_DO_ATRIBUTO = {
    "DodgeChance": "Dodge",
    "CritChance": "Crit Chance",
    "DamageMod": "Damage",
}


def corpo():
    esp = reg.esperado_do_caso()
    alvo = reg.por_id(esp["formatacao"])["equipamento-fracionario"]

    # >>> BLOCO-DO-DEFEITO
    # O rotulo do formato anterior ao RV-45: valor CRU (com a fracao do equipamento) e
    # um "%" acrescentado por cima da etiqueta, que ja termina em "%".
    valor = alvo["valor"]
    rotulo = PREFIXO_DO_ATRIBUTO[alvo["atributo"]] + " " + ("+" if valor >= 0 else "\u2212") \
        + ("%g" % valor) + "%%"
    # <<< BLOCO-DO-DEFEITO

    arc.igual(rotulo, alvo["rotulo"],
              "a borda do equipamento (53.4): a convencao do Ceil do jogo da 54 e UM sinal de %")


if __name__ == "__main__":
    arc.main(META, corpo)
