#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) do TST-2: a MESMA regra do `t_shrine_excesso_agregado.py`, com o
DEFEITO DO DWARVEN SUMIDO plantado.

O DEFEITO (o comportamento anterior ao RV-46): so as auras cujo efeito e um
atributo de PERSONAGEM viravam item. O `Dwarven Aura` (chance de stun) nao tem
atributo, entao uma area so com ele mostrava a linha `Your active shrine auras:`
VAZIA - a lista se apresentava como completa e a aura viva sumia calada (regra do
dono, 30/09: nenhuma aura viva pode sair em silencio, `ShrineAuraPatch.cs` l.1359
e l.1435).

Este arquivo tem de sair REPROVOU (exit 1). O "conserto" e o teste da suite,
`testes/puros/t_shrine_excesso_agregado.py` (cena `dwarven-so`).
"""
import arcabouco as arc
import regras_shrine as reg

META = {
    "nome": "contra-prova-shrine-dwarven",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: a aura viva sem atributo de personagem (Dwarven) nao vira item e some da lista",
}

# As etiquetas das auras SEM atributo de personagem (o defeito as descarta). Vem do
# proprio modulo das regras - o mesmo mapa do `RotuloSemAtributo` do mod.
ETIQUETAS_SEM_ATRIBUTO = tuple(reg.ROTULO_SEM_ATRIBUTO.values())


def corpo():
    ent = reg.entrada_do_caso()
    esp = reg.esperado_do_caso()
    ctx = reg.contexto(ent)
    cena = reg.por_id(ent["agregado"])["dwarven-so"]
    alvo = reg.por_id(esp["agregado"])["dwarven-so"]

    # >>> BLOCO-DO-DEFEITO
    # So as auras COM atributo de personagem viram item (o codigo anterior ao RV-46):
    # a aura sem atributo nao entra na lista e nada no log a substitui.
    itens = [i for i in reg.agregar(cena, ctx)["itens"]
             if not i.startswith(ETIQUETAS_SEM_ATRIBUTO)]
    # <<< BLOCO-DO-DEFEITO

    arc.igual(itens, alvo["itens"],
              "a cena so tem o Dwarven vivo: a linha TEM de trazer o item proprio `Stun chance`")


if __name__ == "__main__":
    arc.main(META, corpo)
