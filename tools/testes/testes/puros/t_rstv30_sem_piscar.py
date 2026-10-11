#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RSTV-30 (parte 2 de 2): O BOTAO NAO PODE PISCAR — o caso plantado do dono.

O DEFEITO (o que o dono viu, em jogo)
-------------------------------------
"o botao de skills nem sempre esta visivel, quando alguem toma alguma acao o botao some e depois
reaparece, tambem ele nao aparece enquanto estamos fora de combate".

A causa: a VISIBILIDADE do clone era CONSEQUENCIA do portao da run (`RunButton.Mirror` chamava `Hide`
quando `RunTargets.GateOk` recusava), e o portao lia estado de BATALHA — `AnyActingCharactersInBattle`,
`AnyMovingCharactersInBattle`, `IsPlayerTurnAndReady` e uma whitelist de `GUIState`. Qualquer animacao
de qualquer personagem fechava o portao e o botao desaparecia.

O CONSERTO (RSTV-30): separar as duas coisas.
  * VISIBILIDADE = HUD. O clone mora na barra de baixo, entao aparece e some junto com o HUD inteiro
    (`GUIManager.Update` l.120485); nenhuma guarda de estado esconde o botao;
  * CLIQUE = a regra NATIVA do jogo (`skillsBtn.interactable`, l.120491) E o portao — quando recusa,
    o botao continua na tela, sem clique, com o motivo no log.

Este teste roda o MODELO PURO dos dois lados:
  1. no CENARIO DO DONO (outro personagem agindo/movendo, turno do inimigo) a regra ANTIGA esconde o
     botao e a NOVA mantem; e o clique libera na nova;
  2. na SEQUENCIA de uma rodada de combate a visibilidade ANTIGA alterna (o piscar, medido em numero
     de transicoes) e a NOVA nao muda NUNCA;
  3. no MAPA-MUNDO e na CIDADE (fora de combate) o botao esta visivel e clicavel nos dois modelos —
     o conserto da RSTV-13 nao regride;
  4. a ISCA: a regra antiga tem de FALHAR no mesmo cenario onde a nova passa (sem isso, o teste
     passaria por construcao).

DE ONDE VEM O ESPERADO
----------------------
As regras vivem em `tools/testes/regras_rstv30.py` (transcricao dos dois portoes e das duas
visibilidades, com os campos citados do decompilado). O fonte VIVO e' conferido no
`t_rstv30_barra_de_baixo.py`; a isca externa e'
`tools/testes/contra-prova/cp_rstv30_visibilidade_por_estado.py`.
"""
import regras_rstv30 as reg

import arcabouco as arc

META = {
    "nome": "rstv30-sem-piscar",
    "categoria": "pura",
    "requer": [],
    "descricao": ("RSTV-30: a visibilidade do botao e' a do HUD (nao pisca quando outro personagem "
                  "age, nao some fora de combate) e o portao decide so' o clique — a regra antiga "
                  "reprova no mesmo cenario"),
}


def corpo():
    # 1) O CENARIO DO DONO: alguem agindo, turno do inimigo, HUD na tela.
    cenario = dict(reg.CENARIO_OUTRO_AGINDO)

    arc.exigir(reg.visivel_agora(cenario),
               "no cenario do dono (outro personagem agindo) o botao NAO esta visivel — e' "
               "exatamente o defeito relatado")
    arc.exigir(not reg.visivel_antes(cenario),
               "a regra ANTIGA manteve o botao visivel nesse cenario: a isca nao reproduz o piscar "
               "que o dono viu (ela passaria por construcao)")
    arc.exigir(reg.clicavel_agora(cenario),
               "no cenario do dono o botao podia estar visivel mas NAO pode ser clicado — a "
               "animacao de outro personagem nao bloqueia nada aqui")

    # 2) O PIScar MEDIDO: a visibilidade antiga alterna ao longo da rodada; a nova nao muda nunca.
    antes = reg.visibilidades(reg.visivel_antes)
    agora = reg.visibilidades(reg.visivel_agora)
    t_antes = reg.transicoes(reg.visivel_antes)
    t_agora = reg.transicoes(reg.visivel_agora)

    arc.igual(t_agora, 0,
              "com a regra nova a visibilidade MUDA %d vez(es) ao longo da rodada (serie %s) — o "
              "botao nao pode piscar" % (t_agora, agora))
    arc.exigir(t_antes >= 3,
               "a regra antiga so' alternou %d vez(es) (serie %s) — menos do que o piscar que o dono "
               "relatou; a sequencia do teste nao esta reproduzindo o defeito" % (t_antes, antes))
    arc.exigir(all(agora),
               "a regra nova escondeu o botao em algum estado da rodada (serie %s)" % agora)

    # 3) FORA DE COMBATE (mapa/cidade): visivel e clicavel nos dois modelos — a RSTV-13 nao regride.
    for nome in ("mapa", "meu turno", "meu turno de novo"):
        parcial = {n: p for n, p in reg.SEQUENCIA_DE_TURNO}.get(nome)
        estado = dict(reg.PADRAO)
        if parcial:
            estado.update(parcial)
        else:
            arc.exigir(False, "a sequencia de turno perdeu o estado %r" % nome)
        arc.exigir(reg.visivel_agora(estado), "no estado %r o botao nao esta visivel" % nome)
        arc.exigir(reg.clicavel_agora(estado), "no estado %r o botao nao e clicavel" % nome)

    # 4) OS PORTOES DE DANO REAL continuam valendo (o conserto nao afrouxou seguranca): mira e ping
    #    fecham o CLIQUE, mas NAO escondem o botao.
    for campo, rotulo in (("mira", "mira de skill ativa"), ("ping", "modo de apontar o hex"),
                          ("janela", "janela de UI aberta"), ("spawn", "posicionamento inicial")):
        estado = dict(reg.PADRAO)
        estado["em_batalha"] = True
        estado["spawn"] = False
        estado[campo] = True
        arc.exigir(not reg.portao_agora(estado), "o portao deixou de recusar com %s" % rotulo)
        arc.exigir(reg.visivel_agora(estado),
                   "com %s o botao foi ESCONDIDO — o portao so' pode deixar o botao sem clique" % rotulo)
        arc.exigir(not reg.clicavel_agora(estado), "com %s o botao ainda estava clicavel" % rotulo)

    # 5) O nivel-up continua LIBERANDO o clique (RSTV-8), mesmo com a janela aberta.
    levelup = dict(reg.PADRAO)
    levelup["levelup"] = True
    levelup["janela"] = True
    arc.exigir(reg.portao_agora(levelup), "o level-up deixou de liberar o clique (RSTV-8 regrediu)")
    arc.exigir(reg.visivel_agora(levelup), "no level-up o botao do HUD deixou de estar visivel pelo HUD")

    print("cenario do dono: ANTES escondia (piscava %d vez(es) na rodada), AGORA mantem visivel e "
          "clicavel (0 transicoes); guardas de dano real seguem fechando so' o clique" % t_antes)


if __name__ == "__main__":
    arc.main(META, corpo)
