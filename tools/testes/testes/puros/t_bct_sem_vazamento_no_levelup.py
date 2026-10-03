#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O BCT NAO VAZA PARA A JANELA DO LEVEL-UP (R2) - a trava do "Select Attributes".

O DEFEITO RELATADO (dono, 02/10)
--------------------------------
O rotulo de secao da janela de level-up ("Select Attributes") ficou com "sombra muito grossa".
Esse texto e o `RoguelikeManager.SectionLabelText` (decompilado l.168605), escrito pelo setter
`RoguelikeManager.CurLevelUpStage` (l.168711). O dono perguntou: o BCT esta aplicando a mais, o
BetterFont transportou efeito, ou e o estilo original do jogo?

A CAUSA RAIZ (fechada com o PREFAB + o log)
-------------------------------------------
1. NAO E O BCT. O BCT patcheia 7 metodos de 7 tipos (nome de inimigo, rotulos de status, texto do
   dado, tooltip, numero de vida) — nenhum deles e o `RoguelikeManager`, e o mod so escreve no
   material POR COMPONENTE devolvido por `fontMaterial` (nunca no compartilhado). Nao ha caminho
   para alcancar o SectionLabelText.
2. E O BETTERFONT. Lido o prefab com UnityPy (`Roguelike Manager` [680571] -> `Label` [680588] ->
   o TMP que o campo `SectionLabelText` aponta): o material em uso e
   'Regular Font (Minion Pro Regular) SDF Material' com `_UnderlayColor` = preto **alfa 0.5**,
   `_UnderlaySoftness`/`_UnderlayDilate`/`_UnderlayOffsetX/Y` = **0** e o keyword **`UNDERLAY_ON`
   DESLIGADO** (`m_ValidKeywords == []`) — ou seja, uma sombra INERTE: o jogo NAO a desenha. O
   `CopiarEstilo` do BetterFont decide "sombra em uso" por `_UnderlayColor.a > 0.001` (o alfa e
   0.5) SEM olhar o keyword, LIGA o `UNDERLAY_ON` no material novo e copia os valores: a sombra
   que o jogo nunca desenhava passa a aparecer — a "sombra muito grossa". (O `AcceptButtonText`
   do mesmo prefab expoe o mesmo padrao com o 'Title Font (Trajan Pro Regular) SDF Material'.)

Esta secao e a TRAVA do lado do BCT: o mod nao pode ganhar gancho (nem citar) a janela do
level-up. Um gancho ali seria o vazamento; um BCT sem ele prova que o conserto de contraste (BCT-4)
e a unica coisa que este mod mudou no texto de combate.

COMO ESTE TESTE E PROVADO REPROVANDO
------------------------------------
`defeito_gancho_no_levelup` planta um `[HarmonyPatch(typeof(RoguelikeManager), ...)]` no Patches.cs
EM MEMORIA e `falhas_do_vazamento_no_levelup` tem de acusar a janela do level-up.
"""
import regras_bct as reg

import arcabouco as arc

META = {
    "nome": "bct-sem-vazamento-no-levelup",
    "categoria": "pura",
    "requer": [],
    "descricao": "R2: o BCT fica nas 7 superficies dele e NAO patcheia nem cita a janela do "
                 "level-up (RoguelikeManager/SectionLabelText) - a sombra do 'Select Attributes' "
                 "e do BetterFont (underlay inerte com o keyword desligado), nao do BCT",
}


def corpo():
    patches = reg.fonte(reg.PATCHES)
    fontes = reg.fontes()

    # O CONTROLE POSITIVO primeiro: o leitor de tipos TEM de achar as 7 superficies do mod.
    tipos = reg.tipos_dos_ganchos(patches)
    arc.exigir(tipos, "nao achei nenhum [HarmonyPatch(typeof(...))] em Patches.cs: o leitor nao "
                      "esta lendo (uma ausencia de vazamento assim nao prova nada)")
    for t in reg.SUPERFICIES_DO_BCT:
        arc.exigir(t in tipos, "o leitor nao achou a superficie '%s' que o mod TEM" % t)

    # 1) O ALCANCE: o mod toca so os tipos que patcheia; a janela do level-up NAO esta entre eles.
    alcance = reg.ModeloDeAlcanceDoBct(tipos)
    for t in reg.TIPOS_DO_LEVELUP:
        arc.exigir(not alcance.toca(t), "o BCT NAO pode tocar '%s' (janela do level-up)" % t)
    arc.exigir(alcance.toca("BossHealthbar"), "o BCT TEM de tocar a superficie dele (controle)")

    # 2) A TRAVA no FONTE (ganchos + citacoes).
    falhas = reg.falhas_do_vazamento_no_levelup(patches, fontes)
    arc.exigir(not falhas, "o BCT vazou para a janela do level-up: %s" % " | ".join(falhas))

    # 3) CONTRA-PROVA: o gancho plantado no Patches.cs REPROVA, e o motivo acusa o RoguelikeManager.
    com_defeito = reg.defeito_gancho_no_levelup(patches)
    arc.exigir(com_defeito != patches, "o plantio do defeito nao achou onde agir")
    tipos_defeito = reg.tipos_dos_ganchos(com_defeito)
    arc.exigir("RoguelikeManager" in tipos_defeito,
               "o plantio do defeito nao pos o gancho no RoguelikeManager")
    falhas_defeito = reg.falhas_do_vazamento_no_levelup(com_defeito, fontes)
    arc.exigir(falhas_defeito, "as checagens PASSARAM com o gancho do level-up plantado: o teste "
                               "nao vigia nada")
    arc.exigir(any("RoguelikeManager" in f for f in falhas_defeito),
               "o defeito nao foi acusado no ponto certo: %s" % " | ".join(falhas_defeito))

    print("sem vazamento: o BCT patcheia %d tipo(s) (%s) e NENHUM deles e o RoguelikeManager da "
          "janela do level-up; o gancho plantado no level-up reprova; a sombra do 'Select "
          "Attributes' e do BetterFont (underlay inerte com o keyword desligado)"
          % (len(tipos), ", ".join(tipos)))


if __name__ == "__main__":
    arc.main(META, corpo)
