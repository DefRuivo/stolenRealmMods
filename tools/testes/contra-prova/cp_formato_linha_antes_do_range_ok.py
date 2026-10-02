#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (metade OK) da LINHA EM BRANCO ANTES DO `Range` (BANCADA-2) — o MESMO teste da isca.

Aqui `LIBERADAS` e o conjunto do BANCADA-2 (`fmt.linhas_do_jogo()`): so a PRIMEIRA linha de custo de
cada caminho (o `AP Cost` da skill, o `Duration Type` do status) vem depois da linha em branco do
jogo. Com ele, a linha em branco antes do `Range` e a sobra ORFA que o checador VE — este arquivo
PASSA.

O par com `cp_formato_linha_antes_do_range_isca.py` e o que transforma "o checador ve a borda" em
prova executavel: a isca reprova pelo motivo certo (a borda era cega com o bloco inteiro) e esta
metade passa (quem confere os dois e `testes/puros/t_formato_notas.py`, que exige tambem que sejam o
MESMO teste fora do bloco `BLOCO-DO-DEFEITO`).
"""
import arcabouco as arc
import regras_formato as fmt

META = {
    "nome": "contra-prova-formato-linha-antes-do-range-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "o MESMO teste da isca com a regra de HOJE (so a PRIMEIRA linha de custo de cada caminho): o checador VE a linha em branco antes do `Range`",
}


# >>> BLOCO-DO-DEFEITO
LIBERADAS = fmt.linhas_do_jogo()   # o BANCADA-2: so a PRIMEIRA linha de custo de cada caminho.
# <<< BLOCO-DO-DEFEITO


def corpo():
    print(fmt.corpo_da_contra_prova_da_linha_antes_do_range(LIBERADAS))


if __name__ == "__main__":
    arc.main(META, corpo)
