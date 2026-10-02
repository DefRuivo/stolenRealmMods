#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (metade OK) do FORMATO das notas (RV-17) — o MESMO teste da isca, sem o defeito.

Aqui a regra e a de HOJE (`"rv17"`): TODAS as notas, na ordem, e o separador consumido inteiro. O
resultado esperado e 0 defeito de formato — este arquivo PASSA.

O par com `cp_formato_notas_isca.py` e o que transforma "o formato esta fechado" em prova
executavel: a isca reprova pelo motivo certo e esta metade passa (quem confere os dois e
`testes/puros/t_formato_notas.py`, que exige tambem que os dois arquivos sejam o MESMO teste fora do
bloco `BLOCO-DO-DEFEITO`).
"""
import arcabouco as arc
import regras_formato as fmt

META = {
    "nome": "contra-prova-formato-notas-ok",
    "categoria": "pura",
    "requer": [],
    "descricao": "o MESMO teste da isca com a regra de HOJE (todas as notas, a linha em branco inteira): o formato fecha",
}


# >>> BLOCO-DO-DEFEITO
REGRA = "rv17"          # todas as notas, na ordem, e a linha em branco INTEIRA consumida.
DEFEITOS_ESPERADOS = 0  # o formato de hoje nao quebra nada.
# <<< BLOCO-DO-DEFEITO


def corpo():
    print(fmt.corpo_da_contra_prova(REGRA, DEFEITOS_ESPERADOS))


if __name__ == "__main__":
    arc.main(META, corpo)
