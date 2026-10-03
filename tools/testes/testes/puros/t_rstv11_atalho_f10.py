#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O ATALHO DE TECLADO (F10) abre a skill tree read-only sem disparar no chat nem no remap (RSTV-11a).

O DEFEITO QUE ISTO TRAVA
------------------------
O gancho e o POSTFIX de `KeybindManager.Update` (decompilado l.133297). O jogo sai desse metodo por
`return` cedo em tres lugares:

    l.133335  if (DisableKeybinds || OptionsManager.instance.CurrentlyBindingControls) return;   // remap
    l.133374  if (... TextInputIsFocused ... || EventWindow.IsNotNullAndIsActive
                   || currentGuiState == ChoosingCharacter/CreatingCharacter/InMainMenu) return;  // chat/menus
    l.133449  if (UIWindowManager.Instance.AnyUIWindowOpenOtherThan(RoguelikeManager.Instance)) return;

O postfix roda INCLUSIVE nesses returns — o gancho sozinho NAO herda guarda nenhuma. Sem o handler
replicar os guards, a TECLA DISPARARIA DURANTE O CHAT. E o defeito plantado por
`regras_rstv11.fonte_com_atalho_sem_guard` (a isca `cp_rstv11_atalho_sem_guard_de_chat.py`).

O CONSERTO (o que este teste trava)
-----------------------------------
`RoguelikeSkillTreeVisualizer/SkillTreeShortcut.cs` (chamado pelo gancho):

  1. a tecla vem do CONFIG (`Plugin.TeclaAtalhoSkillTree`, padrao `KeyCode.F10`) e e lida CRUA
     (`Input.GetKeyDown`) — nao usa a acao 10 nativa (`GetButtonDownAndSwitchToPlayerCharacter(10)`,
     l.133500), que abriria a janela vanilla `ToggleSkillTreeMenu` junto;
  2. antes de agir, os guards do jogo sao REPLICADOS: remap (DisableKeybinds/CurrentlyBindingControls),
     foco de texto (chat e os campos de inventario/mochila/fortune) e a janela de evento;
  3. o despacho espelha o `RunButton.OnClick` (l.568): tela Select Party ativa -> alvo do `PartyTargets`
     no contexto `PartyScreen`; senao `StateAllowed` + `RunTargets.GateOk` + `RunTargets.Resolve` no
     contexto `Run`;
  4. o guard de janela (l.133449) leva a MESMA excecao de LEVEL-UP do portao da RSTV-8 — sem ela, a
     tecla nao funcionaria justamente durante o level-up.

DE ONDE VEM O ESPERADO
----------------------
As regras vivem em `tools/testes/regras_rstv11.py`; os fontes sao lidos AO VIVO
(`SkillTreeShortcut.cs`, `Patches.cs`, `Plugin.cs`), nunca copias: a expectativa fica amarrada ao que
sera compilado. A unica leitura que NAO e literal do cartao (o `ChoosingCharacter` como estado da
tela Select Party, atendida pelo ramo de party) esta justificada no docstring do `regras_rstv11`.

PROVA DE FOGO: com o guard de chat morto no fonte, as MESMAS checagens reprovam pelo motivo certo
(adaptado do padrao da RSTV-9). O que NAO se prova aqui (e so o dono confirma, em tela): o F10 abrir
a arvore de verdade com o jogo rodando.
"""
import regras_rstv11 as reg

import arcabouco as arc

META = {
    "nome": "rstv11-atalho-f10",
    "categoria": "pura",
    "requer": [],
    "descricao": ("RSTV-11a: o atalho (F10 por padrao, configuravel) replica os guards do "
                  "KeybindManager e so abre pelo despacho do botao; o defeito 'sem guard de chat' reprova"),
}


def corpo():
    src = reg.fonte(reg.caminho_atalho())
    src_patches = reg.fonte(reg.caminho_patches())
    src_plugin = reg.fonte(reg.caminho_plugin())
    arc.exigir(len(src) > 3000 and len(src_patches) > 3000 and len(src_plugin) > 3000,
               "os fontes vieram vazios/curtos: a leitura mudou de lugar?")

    # 1) O FONTE: gancho (postfix na ancora certa), guards replicados, despacho e config.
    falhas = reg.falhas_do_atalho(src, src_patches, src_plugin)
    arc.exigir(not falhas, "o atalho regrediu em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))

    # 2) O CASO NORMAL: no estado saudavel da run, a tecla abre pelo ramo da run.
    arc.igual(reg.atalho_novo(dict(reg.CENARIO_ATALHO_RUN)), "Run",
              "atalho no estado saudavel da run")

    # 3) O GUARD DE CHAT (o defeito nomeado no cartao): chat aberto -> NAO abre; o defeito ABRE.
    chat = dict(reg.CENARIO_CHAT_ABERTO)
    arc.igual(reg.atalho_novo(chat), None,
              "com o chat aberto o atalho NAO pode abrir (guard l.133374)")
    arc.exigir(reg.atalho_sem_guard(chat) is not None,
               "o defeito plantado (sem guard de chat) NAO abre com o chat aberto: a isca nao "
               "reproduz o defeito e o teste estaria passando por construcao")

    # 4) A MESMA FAMILIA DE GUARD: remap, keybinds desabilitados, janela de evento e menus sem alvo.
    arc.igual(reg.atalho_novo(dict(reg.CENARIO_ATALHO_RUN, sem_remap=False)), None,
              "durante o remap de tecla (l.133335)")
    arc.igual(reg.atalho_novo(dict(reg.CENARIO_ATALHO_RUN, keybinds_ativos=False)), None,
              "com os keybinds desabilitados pelo jogo (l.133335)")
    arc.igual(reg.atalho_novo(dict(reg.CENARIO_ATALHO_RUN, sem_event_window=False)), None,
              "com a janela de evento aberta (l.133374)")
    arc.igual(reg.atalho_novo(dict(reg.CENARIO_ATALHO_RUN, estado_permitido=False)), None,
              "em estado de menu sem alvo (CreatingCharacter/InMainMenu)")

    # 5) A JANELA (l.133449) e a EXCECAO DE LEVEL-UP (RSTV-8): bloqueia com outra janela; abre no level-up.
    arc.igual(reg.atalho_novo(dict(reg.CENARIO_ATALHO_RUN, sem_janela_aberta=False)), None,
              "com outra janela de UI aberta (guard l.133449)")
    arc.igual(reg.atalho_novo(dict(reg.CENARIO_ATALHO_LEVELUP)), "Run",
              "no LEVEL-UP a tecla abre (a excecao da RSTV-8 no guard de janela)")

    # 6) A TELA SELECT PARTY: o ramo de party abre (mesmo caminho do botao da RSTV-2); sem alvo, nao.
    arc.igual(reg.atalho_novo(dict(reg.CENARIO_ATALHO_PARTY)), "PartyScreen",
              "na tela Select Party, contexto PartyScreen")
    arc.igual(reg.atalho_novo(dict(reg.CENARIO_ATALHO_PARTY, tem_alvo_party=False)), None,
              "tela Select Party sem nenhum personagem SEU na party")

    # 7) O PORTAO (o segundo defeito plantado): sem `GateOk`, a regra NAO abre e o defeito ABRE.
    sem_portao = dict(reg.CENARIO_ATALHO_RUN, portao_ok=False)
    arc.igual(reg.atalho_novo(sem_portao), None, "sem o portao fechado (RunTargets.GateOk)")
    arc.exigir(reg.atalho_sem_portao(sem_portao) is not None,
               "o defeito 'sem portao' NAO abre sem o portao: a isca esta errada")

    # 8) PROVA DE FOGO NO FONTE: com o guard de chat morto, as MESMAS checagens reprovam pelo motivo certo.
    com_defeito = reg.fonte_com_atalho_sem_guard(src)
    arc.exigir(com_defeito != src,
               "o plantio do defeito nao encontrou a ancora (`if (FocoDeTexto())`): a checagem nao le "
               "o trecho certo")
    falhas_defeito = reg.falhas_do_atalho(com_defeito, src_patches, src_plugin)
    arc.exigir(len(falhas_defeito) >= 1,
               "as checagens PASSARAM num fonte com o guard de chat morto: elas nao pegam o defeito")
    arc.exigir(any("foco de texto" in f or "chat" in f for f in falhas_defeito),
               "a checagem reprovou o defeito, mas nao pelo guard de chat: %s" % " | ".join(falhas_defeito))

    print("atalho: guards replicados (chat/remap/evento) e despacho pelo portao; com o chat aberto a "
          "regra nova NAO abre e o defeito (sem guard) ABRE")


if __name__ == "__main__":
    arc.main(META, corpo)
