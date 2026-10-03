#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O LEVEL-UP DA RUN LIBERA O BOTAO DA SKILL TREE (RSTV-8).

O QUE ESTE TESTE GARANTE
------------------------
O dono nunca viu o botao "Skills" no HUD da run: o log da sessao mostra o botao INJETADO e, logo
depois, ESCONDIDO com o motivo "RoguelikeManager ativo (level-up/reroll pendente)". O portao
`RunTargets.GateOk` escondia o botao com `if (RoguelikeManager.IsNotNullAndIsActive) return false`,
mas isso significa "o manager foi CARREGADO" — o que e verdade durante a run inteira depois do
primeiro level-up (o `LoadReference` instancia o prefab, l.168005-168014). A JANELA do level-up e
o filho `SkillSelectWindow.activeSelf` (l.168597; o proprio jogo usa esse criterio em
`GUIManager.Update` l.120492 e no `SkillSelectActive` l.230294).

Este teste le o `RoguelikeSkillTreeVisualizer/RunTargets.cs` VIVO (nao uma copia) e confere:

  1. o portao NAO esconde mais por `IsNotNullAndIsActive` e o ramo `if (LevelUpAberto()) return
     true;` esta la (o level-up e o menu modal onde o jogador quer a arvore);
  2. TODOS os outros portoes continuam no fonte (mira, ping, janela, spawn, turno, animacao,
     alem dos basicos) — o conserto foi cirurgico, nao removeu nenhum;
  3. o alvo do level-up sai do PROPRIO RoguelikeManager
     (`CurrentRoguelikeSkillSelectingCharacter`, com fallback `CharactersWaitingForLevelUp`),
     nunca do `CurrentlySelectedCharacter` que o manager troca, e o `Resolve` confere `Owned`;
  4. o MODELO PURO do portao: o cenario de level-up e LIBERADO pela regra nova e BLOQUEADO pela
     regra antiga (a isca embutida), e fora do level-up cada portao continua bloqueando;
  5. os CAMPOS do portao lidos do fonte baterem com os campos do modelo puro (nome por nome).

DE ONDE VEM O ESPERADO
----------------------
As regras vivem em `tools/testes/regras_rstv.py`, transcritas do proprio conserto; a isca
`tools/testes/contra-prova/cp_rstv8_levelup_escondido.py` reinjeta o defeito ANTIGO no fonte e
MOSTRA as checagens reprovando. Sem essa metade, uma checagem que passa por construcao seria
decoracao. O que NAO se prova aqui (e so o dono confirma, em tela): o botao aparecer durante o
level-up — e a RSTV-9 cuida da APARENCIA, porque o HUD inteiro fica desligado nesse momento
(`GUIManager.Update`, l.120492: `CurrentCharacterUI.gameObject.SetActive(false)` enquanto o
`SkillSelectWindow` esta ativo).
"""
import regras_rstv as reg

import arcabouco as arc

META = {
    "nome": "rstv8-gate-levelup",
    "categoria": "pura",
    "requer": [],
    "descricao": "RSTV-8: o level-up libera o botao pelo SkillSelectWindow, o alvo sai do manager e o defeito antigo reprova",
}


def corpo():
    src = reg.fonte()
    arc.exigir(len(src) > 3000, "RunTargets.cs veio vazio/curto: a leitura mudou de lugar?")

    # 1) O FONTE: o conserto esta de pe e o defeito nao voltou.
    falhas = reg.falhas_da_fonte(src)
    arc.exigir(not falhas, "o portao da run regrediu em %d ponto(s): %s" % (len(falhas), " | ".join(falhas)))

    # 2) OS CAMPOS DO FONTE X OS DO MODELO: um portao que sumir do fonte (ou do modelo) acusa aqui.
    campos = reg.campos_do_portao(src)
    faltando = [nome for nome, _ in reg.CAMPOS if nome not in campos]
    arc.exigir(not faltando, "o GateOk perdeu portao(oes) que o modelo puro ainda tem: %s" % faltando)
    arc.igual(set(campos), set(reg.campos_do_modelo()),
              "os campos do portao no fonte e no modelo puro divergiram")

    # 3) O COMPORTAMENTO NO LEVEL-UP: a regra NOVA libera; a ANTIGA (o defeito) nao libera.
    cenario = dict(reg.CENARIO_LEVELUP)
    arc.exigir(reg.portao_novo(cenario),
               "a regra NOVA nao liberou o botao no cenario de level-up (SkillSelectWindow aberto)")
    arc.exigir(not reg.portao_antigo(cenario),
               "a regra ANTIGA liberou o botao no level-up: a isca nao reproduz o defeito do dono")

    # 4) FORA DO LEVEL-UP o conserto NAO afrouxou nada: cada portao continua bloqueando.
    sem_levelup = dict(cenario)
    sem_levelup["levelup"] = False
    # Universais: bloqueiam em QUALQUER estado permitido (mapa ou batalha).
    for campo in ("gui", "roguelike", "estado", "ping", "janela"):
        bloqueado = dict(sem_levelup)
        bloqueado[campo] = False
        arc.exigir(not reg.portao_novo(bloqueado),
                   "o portao %r deixou de bloquear fora do level-up" % campo)

    # RSTV-13: os portoes de BATALHA bloqueiam EM BATALHA...
    batalha = dict(sem_levelup)
    batalha["em_batalha"] = True
    for campo in reg.CAMPOS_DE_BATALHA:
        bloqueado = dict(batalha)
        bloqueado[campo] = False
        arc.exigir(not reg.portao_novo(bloqueado),
                   "o portao de batalha %r deixou de bloquear" % campo)

    # ...e NAO bloqueiam fora dela (o MAPA-MUNDO) — o botao APARECE enquanto o jogador passeia.
    for campo in reg.CAMPOS_DE_BATALHA:
        no_mapa = dict(sem_levelup)
        no_mapa[campo] = False
        arc.exigir(reg.portao_novo(no_mapa),
                   "o portao de batalha %r voltou a bloquear no MAPA (RSTV-13)" % campo)

    # 5) PROVA DE FOGO NO FONTE: com o defeito antigo reinjetado, a MESMA checagem reprova.
    com_defeito = reg.fonte_com_o_defeito(src)
    arc.exigir(com_defeito != src,
               "o plantio do defeito antigo nao encontrou onde agir: a checagem nao le o trecho certo")
    falhas_defeito = reg.falhas_da_fonte(com_defeito)
    arc.exigir(len(falhas_defeito) >= 1,
               "as checagens PASSARAM num fonte COM o 'esconder no level-up': elas nao pegam o defeito")
    arc.exigir(any("IsNotNullAndIsActive" in f for f in falhas_defeito),
               "a checagem reprovou o defeito, mas nao pelo `IsNotNullAndIsActive`: %s"
               % " | ".join(falhas_defeito))

    print("level-up LIBERA pela regra nova; a antiga REPROVA; %d campo(s) do portao conferido(s) no fonte"
          % len(campos))


if __name__ == "__main__":
    arc.main(META, corpo)
