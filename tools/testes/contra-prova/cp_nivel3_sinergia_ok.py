#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (metade ok) do NIV3-1 — o MESMO teste da isca, com a regra corrigida.

Aqui a regra e a do NIV3-1 (`"com-sinergia"`): o bloco de nivel 3 e recolhido pelo MARCADOR e volta no
fim, depois das notas, e a linha de auras continua por ULTIMO quando as duas existem. O resultado
esperado e 0 defeito de formato — este arquivo PASSA.

O par com `cp_nivel3_sinergia_isca.py` transforma "a correcao funciona" em prova executavel: a isca
reprova pelo motivo certo e esta metade passa (quem confere os dois e
`testes/puros/t_nivel3_sinergia.py`, que exige tambem que os dois arquivos sejam o MESMO teste fora do
bloco `BLOCO-DO-DEFEITO`).
"""
import arcabouco as arc
import regras_nivel3 as n3

META = {
    "nome": "contra-prova-nivel3-sinergia-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "o MESMO teste da isca com a regra do NIV3-1 (a sinergia recolhida pelo marcador): o formato fecha",
}


# >>> BLOCO-DO-DEFEITO
REGRA = "com-sinergia"   # o prefixo recolhe o bloco de sinergia pelo marcador e o devolve por ultimo.
DEFEITOS_ESPERADOS = 0   # a regra corrigida nao quebra nada.
# <<< BLOCO-DO-DEFEITO


def corpo():
    print(n3.corpo_da_contra_prova(REGRA, DEFEITOS_ESPERADOS))


if __name__ == "__main__":
    arc.main(META, corpo)
