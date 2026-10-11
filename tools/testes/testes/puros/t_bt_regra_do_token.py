#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""REGRA DO TOKEN `[N]` (TST-3, cenario 3) - nenhuma NOTA pode carregar o token de expressao.

O QUE ESTE TESTE PRENDE
-----------------------
O pipeline de expressoes do jogo (`ApplyDescriptionExpressions`, o `[N]`) roda DEPOIS do
`Localize`. Se a NOTA do mod traz o token `[N]`, o motor o interpreta como INDICE de expressao
(o RV-8a provou que a gramatica le UM digito) - o numero que o mod escreveu some ou vira outra
coisa. Regra do projeto, declarada no proprio C# (`AtributoPercentualPatch.NotaDoCalculo`
l.299-301 e as guardas de ConvercaoAtributo/Hunger/BerserkersBlood/ReaperToll).

O CORPUS de notas que o teste varre:
  * TODO valor de `TextAppends` (uma entrada de TextAppends E uma nota);
  * os blocos `<color=#C8B090>...</color>` FUNDIDOS nos valores de `TextFixes`
    (`MarcadorCorDeExplicacao` l.426).

Nenhum pode casar o regex `\\[\\d+\\]`. A varredura NAO e vazia (exige notas encontradas), e a
isca `cp_bt_token_isca.py` prova que o detector MORDE uma nota plantada com `[0]`.
"""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "bt-regra-do-token",
    "categoria": "pura",
    "requer": [],
    "descricao": "nenhuma nota (valor de TextAppends + bloco C8B090 fundido no TextFixes) carrega o token [N]; a isca plantada morde",
}


def corpo():
    real = R.le_fonte()
    R.pin(real, "MarcadorCorDeExplicacao = \"C8B090\"", "o marcador de nota do nivel 2")

    corpus = R.notas_das_tabelas(real)
    arc.exigir(len(corpus) > 100,
               "a varredura de notas tem de ver o corpus real (viu %d); se isso caiu, o parser "
               "ou o marcador mudou e o teste virou decoracao" % len(corpus))

    achados = R.violacoes_do_token("real")
    arc.igual(achados, [], "nota com token [N] nas tabelas de verdade: %s" % achados)

    # A isca (nota plantada com [0]) e vista pela MESMA regra - o detector nao e vazio.
    plantado = R.violacoes_do_token("plantado")
    arc.exigir(len(plantado) >= 1 and "[0]" in plantado[0][2],
               "o detector nao mordeu a nota plantada com [0]: %s" % plantado)

    print("%d notas varridas, 0 com token [N]; a nota plantada com [0] foi mordida"
          % len(corpus))


if __name__ == "__main__":
    arc.main(META, corpo)
