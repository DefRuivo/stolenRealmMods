#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do roteamento do clique (RSTV-12): a ISCA do clique que cai no ORIGINAL.

O DEFEITO (log de 02/10): o clone herda o `Button.onClick` SERIALIZADO do botao molde e o
`RemoveAllListeners()` NAO o remove — ele limpa so a lista de runtime (`InvokableCallList.Clear()`),
e a persistente ainda roda ANTES da nossa (`PrepareInvoke()`). Resultado: o botao 'Skills' do HUD
PINGA (o `ButtonPressedPing` liga o modo ping e o portao recusa a abertura) e o da janela do level-up
lanca 11 `NullReferenceException` no `ConfirmLevelUpSelection` antes de o nosso listener rodar.

Este arquivo NAO conserta nada: ele planta a limpeza ANTIGA em memoria (sem tocar em arquivo) e
exige que as checagens de `tools/testes/regras_rstv12.py` REPROVEM pelo motivo certo e que o MODELO
mostre o clique caindo no original. Tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada
e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv12_onclick_roteamento.py`, ao lado.
"""
import regras_rstv12 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv12-clique-no-original",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-12: com a limpeza antiga (RemoveAllListeners), o onClick persistente "
                  "do prefab continua e o clique NAO abre a arvore — o fonte e o modelo tem de REPROVAR"),
}


def corpo():
    src_run = reg.fonte(reg.caminho_run())
    src_janela = reg.fonte(reg.caminho_janela())
    src_select = reg.fonte(reg.caminho_select())

    # 1) A ISCA NO FONTE (nos DOIS clones): a limpeza antiga tem de ser pega pelas checagens.
    antigo_run = reg.fonte_com_limpeza_antiga(src_run)
    antigo_janela = reg.fonte_com_limpeza_antiga(src_janela)
    if antigo_run == src_run or antigo_janela == src_janela:
        raise arc.Falhou("o plantio 'limpeza antiga' nao encontrou a ancora (`%s`): a isca nao esta "
                         "lendo o trecho certo" % reg.CHAMADA_HELPER)

    falhas = reg.falhas_do_roteamento(antigo_run, antigo_janela, src_select)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM nos dois clones com a limpeza antiga: a verificacao "
                         "nao vale nada (o clique cai no original e ninguem percebe)")

    # 2) A ISCA NO HELPER: voltar a `RemoveAllListeners()` no helper tem de reprovar tambem.
    helper_antigo = reg.fonte_com_helper_antigo(src_select)
    if helper_antigo == src_select:
        raise arc.Falhou("o plantio 'helper antigo' nao encontrou a ancora (`%s`)" % reg.TROCA_INSTANCIA)
    falhas_helper = reg.falhas_do_roteamento(src_run, src_janela, helper_antigo)
    if not falhas_helper:
        raise arc.Falhou("as checagens PASSARAM com o helper voltando a `RemoveAllListeners()`: a "
                         "checagem nao protege a troca da instancia do evento")

    # 3) A ISCA NO MODELO: com a limpeza antiga, os DOIS botoes caem no original (nao abrem).
    if reg.resultado_do_clique(reg.LIMPEZA_ANTIGA, reg.PERFIL_PING) != "pingou":
        raise arc.Falhou("o modelo NAO reproduziu o HUD PINGANDO sob o defeito")
    if reg.resultado_do_clique(reg.LIMPEZA_ANTIGA, reg.PERFIL_ACCEPT) != "levelup-nre":
        raise arc.Falhou("o modelo NAO reproduziu o NullReferenceException do level-up sob o defeito")
    if reg.resultado_do_clique(reg.LIMPEZA_NOVA, reg.PERFIL_PING) != "abriu" or \
       reg.resultado_do_clique(reg.LIMPEZA_NOVA, reg.PERFIL_ACCEPT) != "abriu":
        raise arc.Falhou("a regra implementada NAO abre nos dois botoes: o conserto nao esta de pe")

    # Chegou aqui: o defeito FOI pego no fonte (clones e helper) e no modelo. Esta isca reprova de
    # proposito, dizendo o motivo.
    raise arc.Falhou("isca: o 'clique que cai no onClick persistente' foi pego no fonte (clones e "
                     "helper) e no modelo (pingou / levelup-nre) - fonte: %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
