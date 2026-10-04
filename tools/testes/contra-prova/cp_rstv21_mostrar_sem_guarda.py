#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do RSTV-21: a ISCA DO `Mostrar` SEM A GUARDA IMEDIATAMENTE ANTES DA CHAMADA.

O DEFEITO (achado da RSTV-21TR): a checagem antiga exigia os DOIS tokens SOLTOS — `ConstruirPainel()`
e `_painel == null` — em qualquer lugar do corpo do `Mostrar`. So que o `Mostrar` tem DOIS
`if (_painel == null)`: o PRIMEIRO envolve `ConstruirPainel();` (montar o painel se ele ainda nao
existe) e o SEGUNDO apenas SAI do metodo se `_painel` continuar nulo depois da construcao. Remover
a guarda SO da chamada, deixando:

    ConstruirPainel();

    if (_painel == null)
    {
        return;
    }

mantinha os dois tokens presentes (o SEGUNDO `if` satisfazia o `_painel == null`) e a checagem
PASSAVA — embora o painel fosse reconstruido a cada `Mostrar` (perda de estado). A checagem NOVA
amarra o PAR (`if (_painel == null)` IMEDIATAMENTE antes de `ConstruirPainel();`) e TEM de reprovar.

Este arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv21_janela_propria.py`, ao lado.
"""
import regras_rstv21 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv21-mostrar-sem-guarda",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-21: com o `Mostrar` chamando `ConstruirPainel()` sem a guarda "
                  "`if (_painel == null)` imediatamente antes da chamada (mas com o SEGUNDO `if`, "
                  "para outro proposito), as checagens tem de REPROVAR"),
}


def corpo():
    src = reg.fonte(reg.caminho_tab())

    com_defeito = reg.fonte_com_mostrar_sem_guarda(src)
    if com_defeito == src:
        raise arc.Falhou("o plantio 'Mostrar sem a guarda antes da chamada' nao encontrou o par "
                         "`if (_painel == null) { ConstruirPainel(); }`: a isca nao esta lendo o "
                         "trecho certo")

    # SANIDADE DA ISCA: a mutacao remove SO a guarda IMEDIATAMENTE antes da chamada. Os DOIS
    # tokens (`ConstruirPainel()` e o `_painel == null` do SEGUNDO `if`) CONTINUAM presentes — e
    # exatamente isso que enganava a checagem antiga. Se algum sumir, a isca deixou de reproduzir
    # a lacuna.
    if "ConstruirPainel()" not in com_defeito or "_painel == null" not in com_defeito:
        raise arc.Falhou("a isca nao reproduz o caso: sumiu a CHAMADA `ConstruirPainel()` ou o "
                         "token solto `_painel == null` (o SEGUNDO `if`) — ela nao prova a lacuna "
                         "da checagem antiga")

    falhas = reg.falhas_do_desvio_do_hospedeiro(com_defeito)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM com o `Mostrar` sem a guarda antes de "
                         "`ConstruirPainel()` (o token solto do SEGUNDO `if` ainda engana): a "
                         "verificacao nao vale nada")
    if not any("Mostrar" in f and "ConstruirPainel" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pelo `Mostrar`: %s" % " | ".join(falhas))

    raise arc.Falhou("isca: o `Mostrar` sem a guarda imediatamente antes de `ConstruirPainel()` "
                     "foi pego (esperado) - fonte: %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
