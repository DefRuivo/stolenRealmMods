#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) da trava de COR — o FURO do COMENTARIO DE BLOCO (FIX-4, achado da REV-55).

O DEFEITO PLANTADO: a trava `tools/check_notas_redundantes.py` passou a pular o comentario de
LINHA dentro do `{` no COR-2 (o formato 'chave em linha propria', ex. `Shapeshift Dragonkin`),
mas NAO pulava o comentario de BLOCO (`/* ... */`) ANTES da chave: a entrada sumia da varredura
(os blocos de nota caíam de 25 para 24) e a troca de cor nela passava em silencio. Esta isca
espera o comportamento ANTIGO (`esperado: reprovar` no META + o `ESPERADO = 0` do bloco): como a
trava de HOJE pega a troca (exit 1), este arquivo REPROVA.

Este arquivo tem de sair REPROVOU (exit 1). O "conserto" e o `cp_cor_comentario_bloco_ok.py`, ao
lado — os dois sao o MESMO teste fora do bloco `BLOCO-DO-DEFEITO` (quem confere isso e
`testes/puros/t_trava_cor_notas_fundidas.py`).
"""
import arcabouco as arc
import regras_cor as reg

META = {
    "nome": "contra-prova-cor-comentario-bloco",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: a trava de cor DEIXA PASSAR a troca numa entrada com COMENTARIO DE BLOCO dentro da chave",
}


# >>> BLOCO-DO-DEFEITO
ESPERADO = 0  # o parser so pulava comentario de LINHA: a entrada com `/* ... */` ficava invisivel.
# <<< BLOCO-DO-DEFEITO


def corpo():
    print(reg.corpo_da_isca_do_comentario_de_bloco(ESPERADO))


if __name__ == "__main__":
    arc.main(META, corpo)
