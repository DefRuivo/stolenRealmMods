#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do RSTV-21R: a ISCA DO BOTAO CLOSE QUE NAO CHAMA O `Fechar`.

O DEFEITO: o botao Close (caminho (a) de fechamento) deixa de chamar `Fechar`
(`onClick.AddListener(new UnityAction(Fechar))`). O clique do X nao passa pelo funil do aviso: a
janela pode ate' desligar por outro caminho, mas o `_modoJanela` NAO e' largado nesse caminho.

A conexao do botao e' trocada, em memoria, e as checagens TEM de reprovar pelo caminho do BOTAO.

Este arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv21_janela_propria.py`, ao lado.
"""
import regras_rstv21 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv21-botao-fechar-sem-fechar",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-21R: com o botao Close sem chamar `Fechar`, as checagens tem de "
                  "REPROVAR (o caminho do botao nao largaria o `_modoJanela`)"),
}


def corpo():
    src_tab = reg.fonte(reg.caminho_tab())
    src_janela = reg.fonte(reg.caminho_janela())

    com_defeito = reg.fonte_botao_fechar_sem_fechar(src_janela)
    if com_defeito == src_janela:
        raise arc.Falhou("o plantio do defeito nao encontrou o `AddListener(new UnityAction(Fechar))`: "
                         "a isca nao esta lendo o trecho certo")

    falhas = reg.falhas_do_fechamento(src_tab, com_defeito)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM com o botao Close sem chamar `Fechar`: a verificacao "
                         "nao vale nada")
    if not any("botao Close" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pelo caminho do botao: %s"
                         % " | ".join(falhas))

    raise arc.Falhou("isca: o botao Close fora do funil `Fechar` foi pego (esperado) - fonte: %s"
                     % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
