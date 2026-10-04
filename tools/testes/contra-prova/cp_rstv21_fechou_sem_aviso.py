#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do RSTV-21R: a ISCA DO `Fechar` QUE NAO AVISA.

O DEFEITO: `SkillTreesWindow.Fechar` e' o FUNIL dos dois caminhos de fechamento (o botao Close e o
`Atualizar` quando o dono sai de cena). Se ele deixa de disparar o aviso `Fechou`, o hospedeiro
(`SkillTreesTab.AoFecharJanela`) nunca e' chamado: o `_modoJanela` fica PENDURADO `true` e a sessao
read-only nao e' encerrada — o defeito do RSTV-21A.

Aqui o disparo `Fechou();` e' removido, em memoria, e as checagens de `tools/testes/regras_rstv21.py`
TEM de reprovar.

Este arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv21_janela_propria.py`, ao lado.
"""
import regras_rstv21 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv21-fechou-sem-aviso",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-21R: com o `Fechar` sem disparar o aviso `Fechou`, as checagens tem de "
                  "REPROVAR (o `_modoJanela` ficaria pendurado em qualquer fechamento)"),
}


def corpo():
    src_tab = reg.fonte(reg.caminho_tab())
    src_janela = reg.fonte(reg.caminho_janela())

    com_defeito = reg.fonte_sem_aviso_no_fechar(src_janela)
    if com_defeito == src_janela:
        raise arc.Falhou("o plantio do defeito nao encontrou o disparo `Fechou()`: a isca nao esta "
                         "lendo o trecho certo")

    falhas = reg.falhas_do_fechamento(src_tab, com_defeito)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM com o `Fechar` sem disparar `Fechou()`: a verificacao "
                         "nao vale nada")
    if not any("Fechou()" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pelo disparo do aviso: %s"
                         % " | ".join(falhas))

    # O MODELO: sem o aviso, o modo janela fica pendurado depois do fechamento.
    if reg.modo_janela_apos_fechar(True, False) is not True:
        raise arc.Falhou("o modelo nao deixa o modo PENDURADO sem o reset: a isca nao reproduz o defeito")
    if not reg.reset_ao_fechar_ok(False, True, True) is False:
        raise arc.Falhou("o modelo da corrente aceita o reset sem o `Fechar` avisar")

    raise arc.Falhou("isca: o `Fechar` sem o aviso `Fechou` foi pego (esperado) - fonte: %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
