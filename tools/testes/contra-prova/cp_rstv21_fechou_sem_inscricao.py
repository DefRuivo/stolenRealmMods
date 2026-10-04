#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do RSTV-21R: a ISCA DO HOSPEDEIRO QUE NAO SE INSCREVE NO AVISO.

O DEFEITO: `SkillTreesTab.AbrirJanela` deixa de inscrever `AoFecharJanela` no aviso
(`SkillTreesWindow.Fechou = AoFecharJanela`). O `Fechar` ate' dispara o aviso, mas ninguem o escuta:
o `_modoJanela` nunca e' largado.

A inscricao e' removida, em memoria, e as checagens TEM de reprovar pela INSCRICAO.

Este arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv21_janela_propria.py`, ao lado.
"""
import regras_rstv21 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv21-fechou-sem-inscricao",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-21R: com o `AbrirJanela` sem inscrever `AoFecharJanela` no aviso, as "
                  "checagens tem de REPROVAR (o hospedeiro nunca largaria o `_modoJanela`)"),
}


def corpo():
    src_tab = reg.fonte(reg.caminho_tab())
    src_janela = reg.fonte(reg.caminho_janela())

    com_defeito = reg.fonte_sem_inscrever_fechou(src_tab)
    if com_defeito == src_tab:
        raise arc.Falhou("o plantio do defeito nao encontrou `SkillTreesWindow.Fechou = AoFecharJanela`: "
                         "a isca nao esta lendo o trecho certo")

    falhas = reg.falhas_do_fechamento(com_defeito, src_janela)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM com o `AbrirJanela` sem se inscrever no aviso: a "
                         "verificacao nao vale nada")
    if not any("INSCREVE" in f or "inscreve" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pela inscricao no aviso: %s"
                         % " | ".join(falhas))

    raise arc.Falhou("isca: o hospedeiro fora do aviso foi pego (esperado) - fonte: %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
