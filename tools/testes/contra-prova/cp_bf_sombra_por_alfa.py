#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA da sombra fantasma do BetterFont (BF-5): a ISCA.

O que este arquivo faz aqui: ele existe para o runner ter o que reprovar. A regra do plano
(`docs/PLANO-DE-TESTES.md`) e que todo teste seja MOSTRADO REPROVANDO - e a unica forma de
mostrar isso num teste que le o FONTE vivo e rodar a MESMA checagem contra um fonte com o defeito
plantado EM MEMORIA.

O DEFEITO: o do BF-5. O `CopiarEstilo` decide "sombra em uso" por `_UnderlayColor.a > 0.001`
(sem olhar o keyword `UNDERLAY_ON`), liga o `UNDERLAY_ON` no material novo e faz aparecer a
sombra INERTE do 'Select Attributes' (o prefab traz preto alfa 0.5 com a keyword desligada e
offset/dilate zero - a "sombra muito grossa" que o jogo nunca desenhou).

`falhas_da_sombra_inerte` TEM de acusar. Este arquivo tem de sair REPROVOU (exit 1) - se ele
PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_bf_sombra_inerte.py`, ao lado.
"""
import regras_bf_estilo as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-bf-sombra-por-alfa",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca do BF-5: com a sombra ligada por `_UnderlayColor.a > 0` reinjetada, a "
                 "checagem tem de REPROVAR",
}


def corpo():
    src = reg.fonte()

    com_defeito = reg.defeito_sombra_por_alfa(src)
    if com_defeito == src:
        raise arc.Falhou("o plantio do defeito nao achou onde agir (`bool sombraAtiva = ...`): "
                         "a isca nao esta exercitando nada")

    falhas = reg.falhas_da_sombra_inerte(com_defeito)
    if not falhas:
        raise arc.Falhou("a checagem PASSOU num fonte com a sombra ligada por "
                         "`_UnderlayColor.a > 0.001` (keyword desligada): o defeito do BF-5 nao "
                         "e pego - a verificacao do conserto nao vale nada")

    # Chegou aqui: o defeito FOI pego. Esta isca reprova de proposito, dizendo o motivo.
    raise arc.Falhou("isca: o defeito do BF-5 (alfa decidindo a sombra) foi pego pela checagem "
                     "(esperado) - %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
