#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do clone FORA do Content (RSTV-11b): a ISCA do REFLOW.

O que este arquivo faz aqui: ele existe para o runner ter o que reprovar. A regra do plano
(`docs/PLANO-DE-TESTES.md`) e que todo teste seja MOSTRADO REPROVANDO — e a unica forma de mostrar isso
num teste que le o FONTE vivo e rodar as MESMAS checagens contra um fonte com o defeito plantado.

O DEFEITO: o `Content` [680573] tem `VerticalLayoutGroup` + `ContentSizeFitter` (RSTV-10, secao 4).
Clonar o `AcceptButton` para DENTRO dele REFLUI o painel inteiro e re-dimensiona o `ContentSizeFitter`.
Aqui o clone volta a nascer em `contentRt` (o pai do AcceptButton), em memoria, sem tocar em arquivo.
As checagens de `tools/testes/regras_rstv11b.py` TEM de reprovar pelo reflow, e o modelo puro tem de
mostrar o painel refluindo no defeito e NAO refluindo na implementacao (filho direto da janela). Este
arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv11b_botao_janela_levelup.py`, ao lado.
"""
import regras_rstv11b as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv11b-clone-no-content",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-11b: com o clone DENTRO do Content (reflow do painel), o fonte e o "
                  "modelo tem de REPROVAR"),
}


def corpo():
    src_janela = reg.fonte(reg.caminho_janela())
    src_patches = reg.fonte(reg.caminho_patches())

    # 1) A ISCA NO FONTE: o clone dentro do Content tem de ser pego pelas checagens.
    com_defeito = reg.fonte_com_clone_no_content(src_janela)
    if com_defeito == src_janela:
        raise arc.Falhou("o plantio do defeito nao encontrou a ancora "
                         "(`Instantiate(original.gameObject, janela.transform)`): a isca nao esta lendo "
                         "o trecho certo")
    falhas = reg.falhas_do_botao_da_janela(com_defeito, src_patches)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM num fonte com o clone dentro do Content: a verificacao "
                         "do reflow nao vale nada")
    if not any("Content" in f or "reflui" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pelo reflow: %s" % " | ".join(falhas))

    # 2) A ISCA NO MODELO: o clone no Content REFLUI; o clone na janela NAO.
    if reg.reflui_painel(dict(reg.CENARIO_CLONE_JANELA)):
        raise arc.Falhou("o modelo disse que o clone na JANELA reflui: a regra implementada nao esta de pe")
    if not reg.reflui_painel(dict(reg.CENARIO_CLONE_CONTENT)):
        raise arc.Falhou("o modelo NAO fez o clone no Content refluir: a isca nao reproduz o defeito")

    # Chegou aqui: o defeito FOI pego (fonte e modelo). Esta isca reprova de proposito, dizendo o motivo.
    raise arc.Falhou("isca: o 'clone dentro do Content (reflow do painel)' foi pego pelo fonte e pelo "
                     "modelo (esperado) - fonte: %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
