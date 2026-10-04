#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do RSTV-21: a ISCA da JANELA QUE NAO SEGUE O DONO.

O DEFEITO: a raiz da janela e `DontDestroyOnLoad` (reusada entre aberturas). Se o `Atualizar` NAO
olhar o dono (`DonoVivo`), a janela fica ABERTA por cima da proxima tela depois que o jogador fecha o
modal 'Remove Skill Trees' — o Canvas overlay e' acima de tudo e nao some sozinho.

Aqui o `Atualizar` e' reescrito, em memoria, para nao checar o dono, e as checagens de
`tools/testes/regras_rstv21.py` TEM de reprovar.

Este arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv21_janela_propria.py`, ao lado.
"""
import regras_rstv21 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv21-janela-sem-dono",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-21: com o `Atualizar` sem olhar o dono, as checagens tem de REPROVAR "
                  "(a janela ficaria pendurada na proxima tela)"),
}


def corpo():
    src = reg.fonte(reg.caminho_janela())

    com_defeito = reg.fonte_sem_dono_no_atualizar(src)
    if com_defeito == src:
        raise arc.Falhou("o plantio do defeito nao encontrou a ancora (`!DonoVivo()`): a isca nao "
                         "esta lendo o trecho certo")

    falhas = reg.falhas_da_janela(com_defeito)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM com o `Atualizar` sem olhar o dono: a verificacao "
                         "nao vale nada")
    if not any("DonoVivo" in f or "dono" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pelo dono: %s" % " | ".join(falhas))

    # A isca no MODELO: com o dono fora de cena a janela TEM de ser fechada.
    if not reg.deve_fechar(True, False) or reg.janela_visivel(True, False):
        raise arc.Falhou("o modelo nao fecha a janela com o dono fora: a isca nao reproduz o defeito")

    raise arc.Falhou("isca: a janela sem o dono no `Atualizar` foi pega pelo fonte e pelo modelo "
                     "(esperado) - fonte: %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
