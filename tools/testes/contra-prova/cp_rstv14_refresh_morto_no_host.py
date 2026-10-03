#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do ciclo do botao da janela (RSTV-14), defeito 1: o Refresh MORTO no host.

O DEFEITO: o `RstvHost.Update` deixa de chamar `LevelUpWindowButton.Refresh()`. Sem a reavaliacao
por quadro, o clone nao segue o ciclo da janela — fica visivel no estagio de ATRIBUTOS (o "voando"
do dono). Este arquivo reinjeta o defeito no texto do host (em memoria, sem tocar em arquivo) e as
checagens de `regras_rstv14.py` TEM de reprovar. Este arquivo tem de sair REPROVOU (exit 1) — se ele
PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv14_botao_ciclo_levelup.py`, ao lado.
"""
import regras_rstv14 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv14-refresh-morto-no-host",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-14: com o `Refresh()` morto no `RstvHost.Update`, as checagens do "
                  "ciclo do botao tem de REPROVAR"),
}


def corpo():
    src_janela = reg.fonte(reg.caminho_janela())
    src_host = reg.fonte(reg.caminho_host())

    # 1) A ISCA NO FONTE: a chamada do Refresh removida tem de ser pega.
    sem_refresh = reg.fonte_sem_refresh_no_host(src_host)
    if sem_refresh == src_host:
        raise arc.Falhou("o plantio 'sem Refresh no host' nao encontrou a ancora (`%s`): a isca nao "
                         "esta lendo o trecho certo" % reg.CHAMADA_NO_HOST)
    falhas = reg.falhas_do_ciclo(src_janela, sem_refresh)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM com o Refresh morto no host: a verificacao do "
                         "conserto nao vale nada")
    if not any("nao chama" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram, mas nao pela chamada ausente do Refresh: %s"
                         % " | ".join(falhas))

    # 2) A ISCA NO MODELO: o estagio de atributos que a regra NOVA esconde, a ANTIGA mantem visivel.
    atributos = dict(reg.CENARIO, estagio="attributes")
    if reg.mostrar(atributos):
        raise arc.Falhou("a regra nova mostrou o clone no estagio de atributos (o conserto nao esta "
                         "de pe)")
    if not reg.mostrar_sem_estagio(atributos):
        raise arc.Falhou("a regra antiga escondeu o clone no estagio de atributos: a isca nao "
                         "reproduz o defeito do dono")

    raise arc.Falhou("isca: o 'Refresh morto no host' foi pego pelo fonte e pelo modelo (esperado) "
                     "- fonte: %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
