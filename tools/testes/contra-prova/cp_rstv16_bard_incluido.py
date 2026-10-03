#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do RSTV-16: a ISCA do BARD INCLUIDO na aba.

O que este arquivo faz aqui: existe para o runner ter o que reprovar. A regra do plano
(`docs/PLANO-DE-TESTES.md`) e que todo teste seja MOSTRADO REPROVANDO — e a forma de mostrar isso num
teste que le o FONTE vivo e rodar as MESMAS checagens contra um fonte com o defeito plantado.

O DEFEITO: a premissa falsa do cartao — "Bard aparece". O dono corrigiu (Bard nao esta no jogo). Aqui o
bloco `if (tipo == SkillType.Bard) continue;` e removido do texto do fonte, em memoria, e as checagens
de `tools/testes/regras_rstv16.py` TEM de reprovar. Este arquivo tem de sair REPROVOU (exit 1) — se ele
PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv16_aba_arvores.py`, ao lado.
"""
import regras_rstv16 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv16-bard-incluido",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-16: com o filtro do Bard removido, as checagens tem de REPROVAR (a isca "
                  "le a aba vendo o Bard entrar na lista)"),
}


def corpo():
    src_tab = reg.fonte(reg.caminho_aba())

    # 1) A ISCA NO FONTE: o filtro do Bard removido tem de ser pego.
    com_defeito = reg.fonte_com_bard_incluido(src_tab)
    if com_defeito == src_tab:
        raise arc.Falhou("o plantio do defeito nao encontrou a ancora "
                         "(`if (tipo == SkillType.Bard)`): a isca nao esta lendo o trecho certo")
    falhas = reg.falhas_da_aba(com_defeito)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM num fonte que inclui o Bard: a verificacao nao vale nada")
    if not any("Bard" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pelo Bard: %s" % " | ".join(falhas))

    # 2) A ISCA NO MODELO: a lista implementada exclui o Bard; a defeituosa inclui.
    if "Bard" in reg.classes_da_aba(reg.TIPOS_ASSET):
        raise arc.Falhou("o modelo implementado incluiu o Bard — o conserto nao esta de pe")
    if "Bard" not in reg.classes_com_bard(reg.TIPOS_ASSET):
        raise arc.Falhou("o modelo defeituoso NAO incluiu o Bard: a isca nao reproduz o defeito")

    # Chegou aqui: o defeito FOI pego. Esta isca reprova de proposito, dizendo o motivo.
    raise arc.Falhou("isca: o Bard incluido foi pego pelo fonte e pelo modelo (esperado) - fonte: %s"
                     % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
