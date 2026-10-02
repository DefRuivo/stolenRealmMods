#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (metade OK) da QUEBRA DO JOGO (BANCADA-1) — o MESMO teste da isca, sem o defeito.

Aqui `QUEBRAS_DA_BANCADA` e o numero da LEITURA (`fmt.quebras_da_leitura()`, que sai da fixture
`formato-notas.entrada.json` — a contagem dos escapes do proprio trecho do decompilado). Com ele, o
texto que a bancada monta e IGUAL ao texto do jogo: as duas quebras da l.1470 + l.1536, a mesma
linha em branco antes do `AP Cost`. Este arquivo PASSA.

O par com `cp_formato_quebra_do_jogo_isca.py` e o que transforma "a bancada reproduz o jogo" em
prova executavel: a isca reprova pelo motivo certo e esta metade passa (quem confere os dois e
`testes/puros/t_formato_notas.py`, que exige tambem que sejam o MESMO teste fora do bloco
`BLOCO-DO-DEFEITO`).
"""
import arcabouco as arc
import regras_formato as fmt

META = {
    "nome": "contra-prova-formato-quebra-do-jogo-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "o MESMO teste da isca com a regra de HOJE (as quebras da LEITURA do decompilado): a bancada reproduz o jogo",
}


# >>> BLOCO-DO-DEFEITO
QUEBRAS_DA_BANCADA = fmt.quebras_da_leitura()   # o numero que a LEITURA do decompilado manda usar.
# <<< BLOCO-DO-DEFEITO


def corpo():
    print(fmt.corpo_da_contra_prova_da_quebra(QUEBRAS_DA_BANCADA))


if __name__ == "__main__":
    arc.main(META, corpo)
