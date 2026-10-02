#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) da LINHA EM BRANCO ANTES DO `Range` (BANCADA-2) — o afrouxamento do BANCADA-1.

O DEFEITO PLANTADO: o checador do BANCADA-1 liberava o BLOCO INTEIRO de custo do caminho da skill
(`AP Cost`, `Range`, `Blast Radius`, `Mana Cost`, `Cooldown`). Mas o `ShowSkillTooltip` so escreve a
linha em branco antes da PRIMEIRA linha de custo de cada caminho (o `AP Cost` — l.1470 + l.1536); as
seguintes vem com UMA quebra cada (l.1558/1565/1572). Com o bloco inteiro liberado, a forma
`descricao \\n\\n AP Cost \\n\\n Range` — que o jogo NUNCA escreve — passava em silencio.

Esta isca acredita na regra do BANCADA-1 (`LIBERADAS` = o bloco inteiro): o texto plantado PASSA
limpo, a borda era CEGA, e o teste REPROVA citando `MOTIVO_DA_LINHA_ANTES_DO_RANGE`. E e isso que
prova que o caso SEPARA os dois mundos.

O conserto e o `cp_formato_linha_antes_do_range_ok.py`, ao lado — os dois sao o MESMO teste fora do
bloco `BLOCO-DO-DEFEITO` (quem confere isso e `testes/puros/t_formato_notas.py`).
"""
import arcabouco as arc
import regras_formato as fmt

META = {
    "nome": "contra-prova-formato-linha-antes-do-range",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: o checador do BANCADA-1 (o bloco INTEIRO de custo liberado) ACEITA a linha em branco antes do `Range`",
}


# >>> BLOCO-DO-DEFEITO
LIBERADAS = fmt.linhas_do_jogo_do_bloco_inteiro()   # o afrouxamento do BANCADA-1: todo o bloco.
# <<< BLOCO-DO-DEFEITO


def corpo():
    print(fmt.corpo_da_contra_prova_da_linha_antes_do_range(LIBERADAS))


if __name__ == "__main__":
    arc.main(META, corpo)
