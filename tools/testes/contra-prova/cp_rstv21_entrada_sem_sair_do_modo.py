#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do RSTV-21: a ISCA DOS PONTOS DE ENTRADA QUE NAO SAEM DO MODO JANELA.

O DEFEITO: `SairDoModoJanela` continua EXISTINDO (a checagem antiga so olhava a presenca do metodo),
mas os pontos de entrada que ASSUMEM a visao deixam de chama-lo:

  (a) o `Abrir` do inventario (RSTV-16), e
  (b) o `SelecionarEMostrar` (o clique da aba).

Sem a chamada, quando a aba retoma a visao o painel da janela ficaria preso no host errado. A
checagem nova exige que AMBOS chamem `SairDoModoJanela()` e TEM de reprovar.

Este arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv21_janela_propria.py`, ao lado.
"""
import regras_rstv21 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv21-entrada-sem-sair-do-modo",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-21: com o `Abrir` OU o `SelecionarEMostrar` sem chamar "
                  "`SairDoModoJanela()`, as checagens tem de REPROVAR"),
}


def corpo():
    src = reg.fonte(reg.caminho_tab())

    # (a) Abrir sem SairDoModoJanela.
    abrir_sem = reg.fonte_sem_sair_do_modo_no_abrir(src)
    if abrir_sem == src:
        raise arc.Falhou("o plantio 'Abrir sem SairDoModoJanela' nao encontrou a chamada: a isca "
                         "nao esta lendo o trecho certo")
    falhas_abrir = reg.falhas_do_desvio_do_hospedeiro(abrir_sem)
    if not any("SairDoModoJanela" in f and "`Abrir`" in f for f in falhas_abrir):
        raise arc.Falhou("as checagens PASSARAM (ou reprovaram por outro motivo) com o `Abrir` sem "
                         "`SairDoModoJanela()`: %s" % " | ".join(falhas_abrir))

    # (b) SelecionarEMostrar sem SairDoModoJanela.
    sel_sem = reg.fonte_sem_sair_do_modo_no_selecionar(src)
    if sel_sem == src:
        raise arc.Falhou("o plantio 'SelecionarEMostrar sem SairDoModoJanela' nao encontrou a "
                         "chamada: a isca nao esta lendo o trecho certo")
    falhas_sel = reg.falhas_do_desvio_do_hospedeiro(sel_sem)
    if not any("SairDoModoJanela" in f and "SelecionarEMostrar" in f for f in falhas_sel):
        raise arc.Falhou("as checagens PASSARAM (ou reprovaram por outro motivo) com o "
                         "`SelecionarEMostrar` sem `SairDoModoJanela()`: %s" % " | ".join(falhas_sel))

    raise arc.Falhou("isca: os dois pontos de entrada sem `SairDoModoJanela()` foram pegos "
                     "(esperado) - fonte: %s" % falhas_sel[0])


if __name__ == "__main__":
    arc.main(META, corpo)
