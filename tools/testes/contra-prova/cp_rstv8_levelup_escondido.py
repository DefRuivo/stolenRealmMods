#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do portao da run (RSTV-8): a ISCA.

O que este arquivo faz aqui: ele existe para o runner ter o que reprovar. A regra do plano
(`docs/PLANO-DE-TESTES.md`) e que todo teste seja MOSTRADO REPROVANDO — e a unica forma de
mostrar isso num teste que le o FONTE vivo e rodar as MESMAS checagens contra um fonte com o
defeito plantado.

O DEFEITO: o que o dono sofreu — o portao escondendo o botao durante o level-up porque o
`RoguelikeManager` esta carregado/ativo (`if (RoguelikeManager.IsNotNullAndIsActive) return
false;`). Este arquivo reinjeta essa regra no texto do fonte (em memoria, sem tocar em arquivo) e
as checagens de `tools/testes/regras_rstv.py` TEM de reprovar. Este arquivo tem de sair REPROVOU
(exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv8_gate_levelup.py`, ao lado.
"""
import regras_rstv as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv8-levelup-escondido",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca do RSTV-8: com o 'esconder no level-up' reinjetado, o fonte e o modelo tem de REPROVAR",
}


def corpo():
    src = reg.fonte()

    # 1) A ISCA NO FONTE: o defeito antigo reinjetado tem de ser pego pelas checagens.
    com_defeito = reg.fonte_com_o_defeito(src)
    if com_defeito == src:
        raise arc.Falhou("o plantio do defeito nao encontrou a ancora (`if (LevelUpAberto())`): "
                         "a isca nao esta lendo o trecho certo")
    falhas = reg.falhas_da_fonte(com_defeito)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM num fonte com o 'esconder no level-up' plantado: "
                         "a verificacao do conserto nao vale nada")
    if not any("IsNotNullAndIsActive" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pelo `IsNotNullAndIsActive`: %s"
                         % " | ".join(falhas))

    # 2) A ISCA NO MODELO: o cenario real de level-up que a regra NOVA libera tem de ser
    #    BLOQUEADO pela regra ANTIGA — a prova comportamental do defeito do dono.
    cenario = dict(reg.CENARIO_LEVELUP)
    if reg.portao_antigo(cenario):
        raise arc.Falhou("a regra antiga liberou o level-up: a isca nao reproduz o defeito")
    if not reg.portao_novo(cenario):
        raise arc.Falhou("a regra nova NAO liberou o level-up (o conserto nao esta de pe)")

    # Chegou aqui: os dois defeitos FORAM pegos. Esta isca reprova de proposito, dizendo o motivo.
    raise arc.Falhou("isca: o 'esconder no level-up' foi pego pelo fonte e pelo modelo (esperado) - "
                     "fonte: %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
