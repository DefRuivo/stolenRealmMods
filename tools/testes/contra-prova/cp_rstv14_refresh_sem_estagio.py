#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do ciclo do botao da janela (RSTV-14), defeito 2: o Refresh SEM ESTAGIO.

O DEFEITO: o `Refresh()` deixa de olhar `rok.CurLevelUpStage == LevelUpStage.Skills` e passa a decidir
so pela janela. O clone continua VISIVEL no estagio de ATRIBUTOS — exatamente o "botao voando no
level up attributes" relatado pelo dono. Este arquivo reinjeta o defeito no texto da janela (em
memoria, sem tocar em arquivo) e as checagens de `regras_rstv14.py` TEM de reprovar. Este arquivo tem
de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv14_botao_ciclo_levelup.py`, ao lado.
"""
import regras_rstv14 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv14-refresh-sem-estagio",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-14: com o `Refresh()` deixando de olhar o ESTAGIO do level-up, as "
                  "checagens do ciclo do botao tem de REPROVAR (o clone 'voaria' em attributes)"),
}


def corpo():
    src_janela = reg.fonte(reg.caminho_janela())
    src_host = reg.fonte(reg.caminho_host())

    # 1) A ISCA NO FONTE: o Refresh sem o estagio tem de ser pego.
    sem_estagio = reg.fonte_refresh_sem_estagio(src_janela)
    if sem_estagio == src_janela:
        raise arc.Falhou("o plantio 'sem estagio' nao encontrou a ancora (`rok.CurLevelUpStage == "
                         "LevelUpStage.Skills`): a isca nao esta lendo o trecho certo")
    falhas = reg.falhas_do_ciclo(sem_estagio, src_host)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM com o Refresh sem estagio: a verificacao do conserto "
                         "nao vale nada")
    if not any("LevelUpStage.Skills" in f or "estagio" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram, mas nao pelo estagio ausente: %s"
                         % " | ".join(falhas))

    # 2) A ISCA NO MODELO: com a janela ativa, a regra antiga mantem o clone no estagio de atributos.
    atributos = dict(reg.CENARIO, estagio="attributes")
    if reg.mostrar(atributos):
        raise arc.Falhou("a regra nova mostrou o clone no estagio de atributos (o conserto nao esta "
                         "de pe)")
    if not reg.mostrar_sem_estagio(atributos):
        raise arc.Falhou("a regra antiga escondeu o clone no estagio de atributos: a isca nao "
                         "reproduz o defeito do dono")

    raise arc.Falhou("isca: o 'Refresh sem estagio' foi pego pelo fonte e pelo modelo (esperado) - "
                     "fonte: %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
