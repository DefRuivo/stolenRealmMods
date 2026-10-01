#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) do TST-2: a MESMA regra do `t_shrine_excesso_agregado.py`, com o
DEFEITO DA DWA-2 plantado.

O que este arquivo faz aqui: e a isca. A regra do plano (docs/PLANO-DE-TESTES.md) e
que todo teste tem de ser MOSTRADO REPROVANDO - e a unica forma de mostrar isso e
ter, versionado, um teste que reprova de verdade, PELO MOTIVO CERTO.

O DEFEITO (reportado pelo dono, 30/09): a deduplicacao do RV-46 (que esta CERTA para
efeito de atributo de personagem) passou a valer para TUDO, e o efeito da `Dwarven
Aura` NAO e atributo - e CHANCE DE GATILHO. O motor avalia o gatilho UMA VEZ POR
STATUS VIVO (`Character.SkillTriggers`, decompilado l.33489-33508, e
`ProcessSkillTriggers`, l.40953-40959, rolando a chance em l.41211-41216), entao com
DOIS Dwarven Shrines no alcance a linha tem de trazer DOIS itens `Stun chance +40%`
(duas rolagens). Contando UMA instancia, a segunda rolagem some da linha.

Este arquivo tem de sair REPROVOU (exit 1). O "conserto" e o teste da suite,
`testes/puros/t_shrine_excesso_agregado.py`, que e o mesmo cenario com a regra TIPADA
(a lista desduplicada para ATRIBUTO e por instancia para GATILHO).
"""
import arcabouco as arc
import regras_shrine as reg

META = {
    "nome": "contra-prova-shrine-gatilho-uma-instancia",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: o gatilho repetido contado UMA vez (a Dwarven que nao stackava)",
}


def corpo():
    ent = reg.entrada_do_caso()
    esp = reg.esperado_do_caso()
    ctx = reg.contexto(ent)
    cena = reg.por_id(ent["agregado"])["dwarven-x2"]
    alvo = reg.por_id(esp["agregado"])["dwarven-x2"]
    bonus = ctx["bonus"][cena["bonus_id"]]

    # >>> BLOCO-DO-DEFEITO
    # A regra ANTERIOR a DWA-2: a lista viva desduplicada vale para QUALQUER efeito (RV-46 aplicado
    # ao gatilho) - a aura repetida entra UMA vez e a segunda rolagem de chance nao aparece.
    unicas, _stacks, _repeticoes = reg.vivas_desduplicadas(cena)
    itens = []
    for aura in unicas:
        itens.append(reg.ROTULO_SEM_ATRIBUTO[aura] + " "
                     + reg.com_sinal(reg.escala(ctx["auras"][aura][""], bonus)) + "%")
    # <<< BLOCO-DO-DEFEITO

    arc.igual(itens, alvo["itens"],
              "o Dwarven com DOIS shrines: o motor rola a chance UMA VEZ POR INSTANCIA"
              " - a lista tem de trazer DOIS itens")


if __name__ == "__main__":
    arc.main(META, corpo)
