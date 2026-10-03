#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do RSTV-18: a ISCA da escala 1.0 (sem o 'Skill Item Container' nativo).

O que este arquivo faz aqui: existe para o runner ter o que reprovar. A regra do plano
(`docs/PLANO-DE-TESTES.md`) e que todo teste seja MOSTRADO REPROVANDO — e a forma de mostrar isso num
teste que le o FONTE vivo e rodar as MESMAS checagens contra um fonte com o defeito plantado.

O DEFEITO: a escala do container dos nos em 1.0 — exatamente o layout que o dono viu (no de 46px em
vez de ~78px). O texto do fonte troca `EscalaDoContainerDeNos = 1.7f` por `= 1.0f`, em memoria, e as
checagens de `tools/testes/regras_rstv18.py` TEM de reprovar. Este arquivo tem de sair REPROVOU
(exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv18_escala_nos.py`, ao lado.
"""
import regras_rstv18 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv18-escala-1",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-18: com a escala do container dos nos em 1.0 (sem o frame nativo), "
                  "as checagens tem de REPROVAR (o no cairia para 27u)"),
}


def corpo():
    src = reg.fonte(reg.caminho_aba())

    # 1) A ISCA NO FONTE: a escala 1.0 plantada tem de ser pega.
    com_defeito = reg.fonte_com_escala_1(src)
    if com_defeito == src:
        raise arc.Falhou("o plantio do defeito nao encontrou a ancora "
                         "(`EscalaDoContainerDeNos = 1.7f`): a isca nao esta lendo o trecho certo")
    falhas = reg.falhas_dos_nos(com_defeito)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM num fonte com o container em escala 1.0: a verificacao "
                         "nao vale nada")
    if not any("escala" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pela escala: %s" % " | ".join(falhas))

    # 2) A ISCA NO MODELO: o no com o container e maior que sem ele.
    if not (reg.no_efetivo(1.7) > reg.no_efetivo(1.0)):
        raise arc.Falhou("o modelo NAO distingue com/sem o container: a isca nao reproduz a diferenca")

    # Chegou aqui: o defeito FOI pego. Esta isca reprova de proposito, dizendo o motivo.
    raise arc.Falhou("isca: a escala 1.0 (no de %.1fu) foi pega pela checagem - fonte: %s"
                     % (reg.no_efetivo(1.0), falhas[0]))


if __name__ == "__main__":
    arc.main(META, corpo)
