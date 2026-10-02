#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) da QUEBRA DO JOGO (BANCADA-1) — a bancada que NAO reproduzia o jogo.

O DEFEITO PLANTADO: a bancada montava os custos com UMA quebra (`texto.rstrip("\\n") + "\\n" + custo`).
O `ShowSkillTooltip` escreve DUAS (l.1470 `original += "\\n"` + l.1536 `original + "\\n" + "AP Cost: ..."`),
ou seja UMA LINHA EM BRANCO antes do `AP Cost`. Com UMA quebra o texto da bancada NAO e o texto do
jogo: falta a linha em branco que o jogador ve na tooltip vanilla.

Esta isca acredita na regra ANTIGA (`QUEBRAS_DA_BANCADA = 1`). Como o jogo escreve 2, ela REPROVA
citando `MOTIVO_DA_QUEBRA` — e e isso que prova que o caso SEPARA os dois mundos: se ela passasse, o
teste nao estaria provando nada sobre a divergencia.

O conserto e o `cp_formato_quebra_do_jogo_ok.py`, ao lado — os dois sao o MESMO teste fora do bloco
`BLOCO-DO-DEFEITO` (quem confere isso e `testes/puros/t_formato_notas.py`).
"""
import arcabouco as arc
import regras_formato as fmt

META = {
    "nome": "contra-prova-formato-quebra-do-jogo",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: a bancada de ANTES do BANCADA-1 (custos com UMA quebra) nao reproduz o texto do jogo",
}


# >>> BLOCO-DO-DEFEITO
QUEBRAS_DA_BANCADA = 1   # a bancada antiga: os custos entravam com UMA quebra.
# <<< BLOCO-DO-DEFEITO


def corpo():
    print(fmt.corpo_da_contra_prova_da_quebra(QUEBRAS_DA_BANCADA))


if __name__ == "__main__":
    arc.main(META, corpo)
