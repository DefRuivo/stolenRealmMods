#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do RSTV-21R: a ISCA DO `AoFecharJanela` QUE NAO ZERA O `_modoJanela`.

O DEFEITO (o do RSTV-21A, achado da revisao RSTV-21AR): a CORRENTE inteira existe — o botao Close e
o `Atualizar` chamam `Fechar`, o `Fechar` dispara `Fechou`, o `AbrirJanela` inscreve `AoFecharJanela`
— mas o `AoFecharJanela` NAO zera o `_modoJanela`. O aviso roda e o flag fica PENDURADO `true`: a
proxima abertura/aba le estado mentiroso.

O `_modoJanela = false;` do `AoFecharJanela` e' removido, em memoria, e as checagens TEM de reprovar
pelo RESET.

Este arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv21_janela_propria.py`, ao lado.
"""
import regras_rstv21 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv21-ao-fechar-sem-reset",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-21R: com o `AoFecharJanela` sem zerar o `_modoJanela`, as checagens "
                  "tem de REPROVAR (o flag ficaria pendurado depois do fechamento)"),
}


def corpo():
    src_tab = reg.fonte(reg.caminho_tab())
    src_janela = reg.fonte(reg.caminho_janela())

    com_defeito = reg.fonte_ao_fechar_sem_reset(src_tab)
    if com_defeito == src_tab:
        raise arc.Falhou("o plantio do defeito nao encontrou `_modoJanela = false;` no `AoFecharJanela`: "
                         "a isca nao esta lendo o trecho certo")

    falhas = reg.falhas_do_fechamento(com_defeito, src_janela)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM com o `AoFecharJanela` sem zerar o `_modoJanela`: a "
                         "verificacao nao vale nada")
    if not any("zera" in f or "PENDURADO" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pelo reset do `_modoJanela`: %s"
                         % " | ".join(falhas))

    # O MODELO do defeito: o flag fica pendurado no valor antigo.
    if reg.modo_janela_sem_reset(True) is not True:
        raise arc.Falhou("o modelo do defeito nao reproduz o flag pendurado")

    raise arc.Falhou("isca: o `AoFecharJanela` sem o reset foi pego (esperado) - fonte: %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
