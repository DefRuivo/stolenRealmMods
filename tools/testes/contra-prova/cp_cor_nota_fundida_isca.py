#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) da trava de COR das notas fundidas — o FURO do COR-2.

O QUE ESTE ARQUIVO FAZ AQUI: e a isca. A regra do plano (docs/PLANO-DE-TESTES.md) e que
todo teste tem de ser MOSTRADO REPROVANDO — e a unica forma de mostrar isso e ter,
versionado, um teste que reprova de verdade, PELO MOTIVO CERTO.

O DEFEITO PLANTADO (achado da REV-50, fechado pelo COR-2): a trava
`tools/check_notas_redundantes.py` conferia a cor das notas fundidas so no formato de DUAS
quebras (`\\n\\n<color=#...>`). Das 21 entradas de `TextFixes` com cor ela olhava 11 e
IGNORAVA 10 — e DUAS DAS 12 NOTAS DE SHRINE moravam nas ignoradas (`Recover [0]% of max
mana/health each turn`, formato de UMA quebra). Trocar a cor de uma nota fundida passava em
silencio. Esta isca espera o comportamento ANTIGO (`esperado: reprovar` no META + o
`ESPERADO = 0` do bloco): como a trava de HOJE pega a troca (exit 1), este arquivo REPROVA.

Este arquivo tem de sair REPROVOU (exit 1). O "conserto" e o
`cp_cor_nota_fundida_ok.py`, ao lado — os dois sao o MESMO teste fora do bloco
`BLOCO-DO-DEFEITO` (quem confere isso e `testes/puros/t_trava_cor_notas_fundidas.py`).
"""
import arcabouco as arc
import regras_cor as reg

META = {
    "nome": "contra-prova-cor-nota-fundida",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: a trava de cor DEIXA PASSAR a troca de cor numa nota fundida (formato de UMA quebra)",
}


# >>> BLOCO-DO-DEFEITO
ESPERADO = 0  # a versao do COR-1 (so `\n\n`) nao via esta nota: DEIXA PASSAR.
# <<< BLOCO-DO-DEFEITO


def corpo():
    print(reg.corpo_da_isca_da_trava(ESPERADO))


if __name__ == "__main__":
    arc.main(META, corpo)
