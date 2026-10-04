#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do RSTV-21: a ISCA DO `Mostrar` QUE NAO CONSTROI O PAINEL.

O DEFEITO: o `Mostrar` deixa de chamar `ConstruirPainel()` quando `_painel == null`. A checagem
antiga verificava que o painel nasce sob a janela (via `ConstruirPainelNaJanela`), mas NAO que o
`Mostrar` exige o `ConstruirPainel` — entao o painel nunca nasceria e a janela abriria VAZIA sem a
checagem reclamar. A checagem nova amarra `Mostrar` -> `ConstruirPainel()` e TEM de reprovar.

Este arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv21_janela_propria.py`, ao lado.
"""
import regras_rstv21 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv21-mostrar-sem-construir",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-21: com o `Mostrar` sem chamar `ConstruirPainel()` (o painel nunca "
                  "nasceria), as checagens tem de REPROVAR"),
}


def corpo():
    src = reg.fonte(reg.caminho_tab())

    com_defeito = reg.fonte_sem_construir_no_mostrar(src)
    if com_defeito == src:
        raise arc.Falhou("o plantio 'Mostrar sem ConstruirPainel' nao encontrou a guarda "
                         "`_painel == null` com a chamada: a isca nao esta lendo o trecho certo")

    # SANIDADE DA ISCA: o `ConstruirPainel` continua existindo — o que some e a CHAMADA no `Mostrar`.
    if "private static void ConstruirPainel()" not in com_defeito:
        raise arc.Falhou("a isca nao reproduz o caso: o proprio `ConstruirPainel` sumiu, nao so a "
                         "chamada no `Mostrar`")

    falhas = reg.falhas_do_desvio_do_hospedeiro(com_defeito)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM com o `Mostrar` sem `ConstruirPainel()`: a "
                         "verificacao nao vale nada")
    if not any("Mostrar" in f and "ConstruirPainel" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pelo `Mostrar`: %s" % " | ".join(falhas))

    raise arc.Falhou("isca: o `Mostrar` sem `ConstruirPainel()` foi pego (esperado) - fonte: %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
