#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do RSTV-21: a ISCA do CLIQUE DE VOLTA NO INVENTARIO (o defeito original).

O DEFEITO (log de 03/10): o `onClick` do botao 'Skills' do modal 'Remove Skill Trees' chama
`SkillTreesTab.Abrir` — que abre o INVENTARIO (`CharacterMenusManager.OpenCharacterMenu`). Na tela de
PARTY SELECT o inventario NAO abre (o personagem nao esta em `AllMyCharacters`), o pedido cai no teto
de 5 s e o clique morre em silencio: "o inventario nao abriu em 5 s ... o pedido foi descartado".

Aqui o clique e' revertido, em memoria, para `Abrir` no texto do fonte e as checagens de
`tools/testes/regras_rstv21.py` TEM de reprovar.

Este arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv21_janela_propria.py`, ao lado.
"""
import regras_rstv21 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv21-clique-volta-inventario",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-21: com o clique do modal de volta em `SkillTreesTab.Abrir` (o "
                  "inventario), as checagens tem de REPROVAR"),
}


def corpo():
    src = reg.fonte(reg.caminho_remocao())

    com_defeito = reg.fonte_com_volta_ao_inventario(src)
    if com_defeito == src:
        raise arc.Falhou("o plantio do defeito nao encontrou a ancora do clique "
                         "(`SkillTreesTab.AbrirJanela(...)`): a isca nao esta lendo o trecho certo")

    falhas = reg.falhas_do_clique_do_modal(com_defeito)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM com o clique de volta no inventario: a verificacao "
                         "nao vale nada")
    if not any("Abrir(" in f or "inventario" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pelo caminho do inventario: %s"
                         % " | ".join(falhas))

    # A isca no MODELO: o DEFEITO (todo hospedeiro abre o inventario) tem de divergir da regra
    # correta (o modo janela NAO abre) — se nao divergir, a isca nao prova nada.
    defeito_abre = reg.abre_inventario(reg.host_com_inventario_sempre(True))
    regra_abre = reg.abre_inventario(reg.host_escolhido(True))
    if not defeito_abre:
        raise arc.Falhou("o modelo do defeito NAO abre o inventario: a isca nao reproduz o defeito")
    if defeito_abre == regra_abre:
        raise arc.Falhou("o modelo do defeito nao difere da regra correta: a isca nao prova nada")

    raise arc.Falhou("isca: o clique de volta no inventario foi pego pelo fonte e pelo modelo "
                     "(esperado) - fonte: %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
