#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do portao de material do BetterFont (BF-2): a ISCA.

O que este arquivo faz aqui: ele existe para o runner ter o que reprovar. A regra do plano
(`docs/PLANO-DE-TESTES.md`) e que todo teste seja MOSTRADO REPROVANDO - e a unica forma de
mostrar isso num teste que le o FONTE vivo e rodar as MESMAS checagens contra um fonte com o
defeito plantado.

O DEFEITO: o do BF-1, o que a revisao independente refutou - o gate recusando por VARIANTE DE
SHADER (o material dos textos de combate usa `Distance Field Overlay`, a fonte serifada usa
`Mobile/Distance Field`), e o gate voltando a olhar a classificacao do texto em vez do efeito
presente no material. Sao os dois defeitos que este arquivo reinjeta, e as checagens de
`tools/testes/regras_bf.py` TEM de reprovar nos dois. Este arquivo tem de sair REPROVOU
(exit 1) - se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_bf_gate_material.py`, ao lado.
"""
import regras_bf

import arcabouco as arc

META = {
    "nome": "contra-prova-bf-gate-shader",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca do BF-2: com a recusa por shader do BF-1 reinjetada, as checagens tem de REPROVAR",
}


def corpo():
    src = regras_bf.fonte()

    # Defeito 1 (o achado da revisao): recusa por variante de shader.
    com_defeito = regras_bf.fonte_com_o_defeito_do_bf1(src)
    falhas = regras_bf.falhas_da_fonte(com_defeito)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM num fonte com a recusa por shader do BF-1 plantada: "
                         "a verificacao do conserto nao vale nada")

    # Defeito 2: o portao condicionado a classificacao do texto (o texto NAO estilizado
    # cuja fonte traz _FaceTex/glow ficava desprotegido).
    com_gate_antigo = regras_bf.fonte_com_o_defeito_do_gate(src)
    falhas_gate = regras_bf.falhas_da_fonte(com_gate_antigo)
    if not falhas_gate:
        raise arc.Falhou("as checagens PASSARAM num fonte com o portao condicionado a 'estilizado': "
                         "o defeito 2 nao e pego")

    # Chegou aqui: os defeitos FORAM pegos. Esta isca reprova de proposito, dizendo o motivo.
    raise arc.Falhou("isca: os dois defeitos do BF-1 foram pegos pelas checagens (esperado) - "
                     "shader: %s | gate: %s" % (falhas[0], falhas_gate[0]))


if __name__ == "__main__":
    arc.main(META, corpo)
