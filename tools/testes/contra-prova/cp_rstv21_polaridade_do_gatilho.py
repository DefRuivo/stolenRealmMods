#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do RSTV-21: a POLARIDADE e a GUARDA do gatilho do `Atualizar` (o caminho (b)).

O DEFEITO (ACHADO da RSTV-21CR): a checagem antiga prendia o caminho (b) so pela PRESENCA dos
tokens `DonoVivo()` e `Fechar()`. Isso deixava passar em BRANCO duas mutacoes:

  R1. inverter `!DonoVivo()` -> `DonoVivo()` no `Atualizar`: o `Fechar` rodaria com o modal
      ABERTO e a janela (`DontDestroyOnLoad`) ficaria PENDURADA quando o dono saisse;
  R2. remover `_root.activeSelf` da condicao: o gatilho dispararia com a janela ja fechada.

Aqui as DUAS mutacoes sao plantadas, em memoria, e as checagens endurecidas (`falhas_da_janela` E
`falhas_do_fechamento`) TEM de reprovar as duas — pelo motivo do gatilho.

Este arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv21_janela_propria.py`, ao lado.
"""
import regras_rstv21 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv21-polaridade-do-gatilho",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-21: com o gatilho do `Atualizar` de polaridade INVERTIDA "
                  "(`DonoVivo()` no lugar de `!DonoVivo()`) ou sem exigir `_root.activeSelf`, as "
                  "checagens do fonte tem de REPROVAR"),
}


def _motivo_do_gatilho(falhas):
    return any(("dono" in f) or ("DonoVivo" in f) or ("polaridade" in f) or ("activeSelf" in f)
               for f in falhas)


def corpo():
    src_tab = reg.fonte(reg.caminho_tab())
    src_janela = reg.fonte(reg.caminho_janela())

    for rotulo, plantio in (
            ("polaridade invertida (!DonoVivo -> DonoVivo)",
             reg.fonte_com_polaridade_invertida_no_atualizar),
            ("sem _root.activeSelf", reg.fonte_sem_active_self_no_atualizar),
    ):
        com_defeito = plantio(src_janela)
        if com_defeito == src_janela:
            raise arc.Falhou("o plantio '%s' nao encontrou a ancora no `Atualizar`: a isca nao esta "
                             "lendo o trecho certo" % rotulo)

        falhas = reg.falhas_da_janela(com_defeito)
        if not falhas:
            raise arc.Falhou("`falhas_da_janela` PASSOU com o gatilho '%s': a checagem nao prende a "
                             "polaridade/guarda do `Atualizar` (o defeito do RSTV-21CR)" % rotulo)
        if not _motivo_do_gatilho(falhas):
            raise arc.Falhou("`falhas_da_janela` reprovou '%s', mas nao pelo gatilho: %s"
                             % (rotulo, " | ".join(falhas)))

        falhas = reg.falhas_do_fechamento(src_tab, com_defeito)
        if not falhas:
            raise arc.Falhou("`falhas_do_fechamento` PASSOU com o gatilho '%s': o caminho (b) nao "
                             "prenderia a polaridade/guarda do `Atualizar`" % rotulo)
        if not _motivo_do_gatilho(falhas):
            raise arc.Falhou("`falhas_do_fechamento` reprovou '%s', mas nao pelo gatilho: %s"
                             % (rotulo, " | ".join(falhas)))

    raise arc.Falhou("isca: a polaridade invertida e a guarda sem `_root.activeSelf` foram pegas "
                     "pelos DOIS lados do caminho (b) (esperado)")


if __name__ == "__main__":
    arc.main(META, corpo)
