#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O hover dos nos da janela read-only resolve 'dano'/'[N]' contra o personagem do MODAL — RSTV-26.

O QUE ISTO TRAVA
----------------
Na janela read-only (botao 'Skills' do modal 'Remove Skill Trees'), o hover mostrava o dano como
'*0' LITERAL: o overload `ShowSkillTooltip(SkillTreeItem)` resolve contra `TooltipCharacter`, que e'
`GameLogic.CurrentlySelectedCharacter` — NULL na tela Party Select (onde vive o modal). O motor so
resolve os placeholders DENTRO de `if (character != null)`.

AS 3 REGRAS (viram checagem)
----------------------------
1. o hover le `ReadOnlySession.Target` (o personagem do MODAL) e o passa EXPLICITO:
   `ShowSkillTooltip(Item.SkillInfo, <alvo>, showCanLevelDetail: false)`;
2. o alvo passa por `if (<alvo> != null)` e o `else` cai no comportamento ANTIGO (sem crash);
3. `showCanLevelDetail: false` mantem o read-only de verdade (sem 'Skill Point Cost'/'Select To Learn').

DE ONDE VEM O ESPERADO
----------------------
Regras em `tools/testes/regras_rstv26.py`; fonte lido AO VIVO do mod (nunca copia). O que NAO se
prova aqui (so o dono confirma, em tela): o numero aparecer no lugar do '*0' no modal.
"""
import regras_rstv26 as reg

import arcabouco as arc

META = {
    "nome": "rstv26-tooltip-personagem",
    "categoria": "pura",
    "requer": [],
    "descricao": ("RSTV-26: o hover da janela read-only passa o personagem do MODAL "
                  "(ReadOnlySession.Target) ao ShowSkillTooltip, com `showCanLevelDetail: false`; o "
                  "motor resolve o '*N'/'[N]' contra ele (sem o TooltipCharacter null) e o alvo null "
                  "cai no comportamento antigo — o defeito SEM o alvo explicito republica o '*0'"),
}


def corpo():
    src_tab = reg.fonte(reg.caminho_tab())
    arc.exigir(len(src_tab) > 1000,
               "o fonte SkillTreesTab.cs veio vazio/curto: a leitura mudou de lugar?")

    # 1) A CORRECAO: o hover passa o personagem do modal ao motor, com o guard e o fallback.
    falhas = reg.falhas_do_hover(src_tab)
    arc.exigir(not falhas, "o hover regrediu em %d ponto(s): %s" % (len(falhas), " | ".join(falhas)))

    # 2) O MODELO PURO: na tela Party Select o TooltipCharacter e' null.
    #    SEM o alvo explicito (o defeito) o '*0' fica LITERAL; COM ele, resolve.
    arc.exigir(not reg.placeholders_resolvidos(None, None),
               "o modelo diz que sem alvo explicito E sem TooltipCharacter o '*0' seria resolvido — "
               "o modelo do defeito nao reproduz nada")
    arc.exigir(reg.placeholders_resolvidos("Raven", None),
               "o modelo diz que com o alvo explicito (personagem do modal) o '*0' NAO seria "
               "resolvido — a correcao nao teria efeito")
    arc.igual(reg.personagem_do_motor(None, "Raven"), "Raven",
              "o motor sem alvo explicito cai no TooltipCharacter")
    arc.igual(reg.personagem_do_motor("Raven", "Outro"), "Raven",
              "o alvo explicito VENCE o TooltipCharacter do motor")

    # 3) O MODELO PURO do read-only: com `showCanLevelDetail: false` NAO sai 'Skill Point Cost'.
    arc.exigir(not reg.mostra_custo(False, True),
               "o modelo mostra 'Skill Point Cost' mesmo com `showCanLevelDetail: false`")
    arc.exigir(reg.mostra_custo(True, True),
               "o modelo NUNCA mostra o custo: a checagem nao prova que `showCanLevelDetail` importa")
    arc.exigir(not reg.mostra_custo(True, False),
               "o modelo mostra custo com a arvore INATIVA (o motor exige `IsNotNullAndIsActive`)")

    # 4) PROVA DE FOGO: o hover de volta no overload de 1 argumento (o defeito original) REPROVA.
    defeito = reg.fonte_com_defeito(src_tab)
    arc.exigir(defeito != src_tab,
               "o plantio 'hover antigo' nao encontrou a ancora (ReadOnlySession.Target -> fallback): "
               "a checagem nao le o trecho certo")
    falhas_defeito = reg.falhas_do_hover(defeito)
    arc.exigir(len(falhas_defeito) >= 1 and any("ReadOnlySession.Target" in f or "resolvidos" in f
                                                or "ShowSkillTooltip(Item.SkillInfo" in f
                                                for f in falhas_defeito),
               "as checagens PASSARAM (ou reprovaram por outro motivo) com o hover ANTIGO: %s"
               % " | ".join(falhas_defeito))

    print("RSTV-26: o hover da janela read-only le o personagem do MODAL (ReadOnlySession.Target) e o "
          "passa EXPLICITO ao ShowSkillTooltip (showCanLevelDetail: false), resolvendo o '*N'/'[N]' "
          "contra ele — na Party Select o TooltipCharacter e' null e o '*0' sairia LITERAL; o alvo "
          "null cai no comportamento antigo e o defeito plantado REPROVA.")


if __name__ == "__main__":
    arc.main(META, corpo)
