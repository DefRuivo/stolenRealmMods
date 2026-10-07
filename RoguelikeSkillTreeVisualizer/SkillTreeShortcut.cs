using System;
using Burst2Flame;
using UnityEngine;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// RSTV-11a — PARTE 1: o ATALHO de teclado que abre a mesma visualizacao read-only das arvores.
    /// RSTV-16: a visualizacao passou a ser a ABA "All Skill Trees" do inventario — o atalho abre o
    /// INVENTARIO nela (`OpenCharacterMenu` + `SelectButtonAndInvoke`), nao mais a janela separada.
    ///
    /// O gancho e o postfix de `KeybindManager.Update` (l.133297, privado, sem parametro). O postfix
    /// roda INCLUSIVE nos `return` cedo do jogo, entao ele nao decide nada sozinho: TODA a decisao
    /// mora aqui, e os guards do jogo sao REPLICADOS explicitamente (nada de assumir que o jogo ja
    /// filtrou):
    ///
    ///   l.133335  `DisableKeybinds` / `OptionsManager.CurrentlyBindingControls`  -> remap de tecla;
    ///   l.133374  foco de texto (chat/inventario/mochila/fortune/debug) e `EventWindow`;
    ///   l.133449  `UIWindowManager.AnyUIWindowOpenOtherThan(RoguelikeManager.Instance)`.
    ///
    /// DUAS DIFERENCAS DELIBERADAS em relacao a transcricao literal, e o porque de cada uma:
    ///
    ///  1. `GUIState.ChoosingCharacter` NAO bloqueia: e o estado EXATO da tela "Select Party"
    ///     (`OpenCharacterChoiceManager` o escreve, l.328705), que este atalho atende pelo ramo de
    ///     despacho PROPRIO da tela de party (RSTV-29 removeu o BOTAO daquela tela; o atalho — RSTV-11a
    ///     — continua abrindo a arvore read-only ali). Bloquear aqui tornaria morto esse ramo.
    ///     `CreatingCharacter`/`InMainMenu` continuam bloqueando (nao ha alvo nem sessao read-only
    ///     valida neles).
    ///  2. O guard de janela (l.133449) leva a MESMA excecao de LEVEL-UP do portao da RSTV-8
    ///     (`RunTargets.JanelaDoLevelUpAberta`): durante o level-up o jogo mantem a janela modal
    ///     aberta e o portao da RSTV-8 LIBERA de proposito — sem a excecao, a tecla nao funcionaria
    ///     justamente quando o jogador mais quer consultar a arvore, contradizendo o "level-up
    ///     liberado pela RSTV-8" do proprio cartao.
    ///
    /// O despacho espelha o `RunButton.OpenForTarget`:
    ///   1. tela Select Party ativa -> `SkillTreesTab.Abrir(PartyTargets.Resolve(), PartyScreen)`;
    ///   2. senao, `StateAllowed` + o PORTAO ja validado (`RunTargets.GateOk`) +
    ///      `RunTargets.Resolve` != null -> `RunButton.OpenForTarget()` (a aba nova).
    ///
    /// NAO usa a acao 10 nativa (`VirtualInput.GetButtonDownAndSwitchToPlayerCharacter(10)`, l.133500,
    /// que chama `CharacterMenusManager.ToggleSkillTreeMenu`): a tecla e lida CRUA
    /// (`Input.GetKeyDown`) e nao abre a janela vanilla junto.
    /// </summary>
    internal static class SkillTreeShortcut
    {
        /// <summary>Borda do gancho: chamada pelo postfix de `KeybindManager.Update`.</summary>
        internal static void Handle(KeybindManager kb)
        {
            try
            {
                if (!Plugin.AtalhoLigado)
                {
                    return;
                }

                KeyCode tecla = Plugin.TeclaAtalho;
                if (tecla == KeyCode.None)
                {
                    return;
                }

                if (!Input.GetKeyDown(tecla))
                {
                    return;
                }

                string motivo;
                if (!Liberado(kb, out motivo))
                {
                    Plugin.Log.LogInfo("RSTV-11: atalho " + tecla + " IGNORADO — " + motivo + ".");
                    return;
                }

                Abrir(tecla);
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha ao tratar o atalho da skill tree: " + e);
            }
        }

        /// <summary>
        /// Guards REPLICADOS do `KeybindManager.Update` — devolve false (com o motivo) quando a tecla
        /// nao pode agir agora. Lidos antes de qualquer trabalho: a tecla nao pode disparar durante
        /// chat, remap, janela de evento ou menu sem alvo.
        /// </summary>
        private static bool Liberado(KeybindManager kb, out string motivo)
        {
            motivo = null;

            // ---- guard 1 (l.133335): keybinds desligados pelo jogo / remap de tecla em andamento ----
            if (kb == null)
            {
                motivo = "KeybindManager ainda nao existe";
                return false;
            }

            if (kb.DisableKeybinds)
            {
                motivo = "keybinds desabilitados pelo jogo (KeybindManager.DisableKeybinds)";
                return false;
            }

            OptionsManager opcoes = OptionsManager.instance;
            if (opcoes == null || opcoes.CurrentlyBindingControls)
            {
                motivo = "remap de tecla em andamento (OptionsManager.CurrentlyBindingControls)";
                return false;
            }

            // ---- guard 2 (l.133374): foco de texto (chat) e janela de evento ----
            if (FocoDeTexto())
            {
                motivo = "campo de texto em foco (chat/inventario/mochila/fortune)";
                return false;
            }

            if (EventWindow.IsNotNullAndIsActive)
            {
                motivo = "janela de evento aberta (EventWindow)";
                return false;
            }

            // ---- guard 2 (l.133374), parte de `GUIState` ----
            GUIManager gui = GUIManager.instance;
            if (gui == null)
            {
                motivo = "GUIManager.instance ausente";
                return false;
            }

            GUIState estado = gui.CurrentGuiState;
            if (estado == GUIState.CreatingCharacter || estado == GUIState.InMainMenu)
            {
                motivo = "GUIState " + estado + " (menu sem alvo para a arvore)";
                return false;
            }

            return true;
        }

        /// <summary>
        /// Transcricao do guard de FOCO DE TEXTO do jogo (l.133374), com o mesmo curto-circuito: cada
        /// bloco so chega ao `Instance` quando o `IsNotNullAndIsActive` manda — e o `DebugWindow` tem o
        /// proprio teste de nulo. Excecao aqui e lado SEGURO: sem saber, a tecla nao dispara (o pior
        /// caso e o jogador usar o botao do HUD em vez da tecla).
        /// </summary>
        private static bool FocoDeTexto()
        {
            try
            {
                MessageWindowManager chat = MessageWindowManager.instance;
                if (chat != null && chat.TextInputIsFocused)
                {
                    return true;
                }

                if (ItemStashManager.IsNotNullAndIsActive &&
                    LoadableUIWindow<ItemStashManager>.Instance.StashInventory.TextInputIsFocused)
                {
                    return true;
                }

                if (ItemStashManager.IsNotNullAndIsActive &&
                    LoadableUIWindow<ItemStashManager>.Instance.PlayerInventory.TextInputIsFocused)
                {
                    return true;
                }

                DebugWindow depurador = DebugWindow.Instance;
                if (depurador != null && depurador.AllItemsInventory.TextInputIsFocused)
                {
                    return true;
                }

                if (InventoryManager.IsNotNullAndIsActive &&
                    LoadableUIWindow<InventoryManager>.Instance.Inventory.TextInputIsFocused)
                {
                    return true;
                }

                if (FortuneWindow.IsNotNullAndIsActive &&
                    LoadableUIWindow<FortuneWindow>.Instance.TextInputIsFocused)
                {
                    return true;
                }

                return false;
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-11: nao deu para ler o foco de texto (" + e.Message +
                                      ") — atalho bloqueado por seguranca.");
                return true;
            }
        }

        /// <summary>
        /// O despacho (RSTV-16): tela Select Party -> `SkillTreesTab.Abrir(PartyTargets.Resolve(),
        /// PartyScreen)`; senao -> o caminho da run pelo MESMO corpo do botao (RSTV-11b:
        /// `RunButton.OpenForTarget`, que ja faz o portao da RSTV-5/8 + o alvo resolvido na hora). Antes o
        /// atalho duplicava o `OnClick`; hoje ele abre a ABA "All Skill Trees" do inventario.
        /// </summary>
        private static void Abrir(KeyCode tecla)
        {
            // O host do mod e garantido aqui: o `SkillTreesTab.Tick` (que vive no Update do host) e quem
            // seleciona a aba pendente depois que o inventario termina de abrir (a abertura e assincrona).
            // `Ensure` e idempotente.
            RstvHost.Ensure();

            // 1) TELA SELECT PARTY — caminho PROPRIO do atalho desde a RSTV-29: alvo pelo PartyTargets (a
            //    ordem de adicao LOCAL) e contexto PartyScreen (o botao injetado na tela foi removido).
            CharacterChoiceManager telaParty = CharacterChoiceManager.IsNotNullAndIsActive
                ? CharacterChoiceManager.Instance
                : null;
            if (telaParty != null)
            {
                Character alvoParty = PartyTargets.Resolve();
                if (alvoParty == null)
                {
                    Plugin.Log.LogWarning("RSTV-11: atalho " + tecla + " na tela Select Party sem alvo " +
                                          "(nenhum personagem SEU na party) — nada foi aberto.");
                    return;
                }

                Plugin.Log.LogInfo("RSTV-16: atalho " + tecla + " -> aba 'All Skill Trees' do inventario para '" +
                                   alvoParty.CharacterName + "' (caminho da tela Select Party).");
                SkillTreesTab.Abrir(alvoParty, ReadOnlyContext.PartyScreen);
                return;
            }

            // 2) RUN — espelha o OnClick do RunButton: a MESMA lista de estados que o JOGO usa para
            //    habilitar os botoes de personagem do HUD (RSTV-30: `EstadoPermiteMenuDePersonagem`
            //    le a regra de `GUIManager.Update` l.120491, no lugar da whitelist propria que o mod
            //    tinha), o PORTAO ja validado e o alvo resolvido na hora. A tecla nao inventa caminho
            //    nenhum de escrita.
            GUIManager gui = GUIManager.instance;
            if (gui == null)
            {
                Plugin.Log.LogWarning("RSTV-11: atalho " + tecla + " ignorado — GUIManager.instance ausente.");
                return;
            }

            if (!RunTargets.EstadoPermiteMenuDePersonagem(gui.CurrentGuiState))
            {
                Plugin.Log.LogWarning("RSTV-11: atalho " + tecla + " ignorado — GUIState " +
                                      gui.CurrentGuiState + " nao permite abrir o menu de personagem " +
                                      "(InTown/InWorldMap/InCutscene/InBattle).");
                return;
            }

            // ---- guard 3 (l.133449): nao empilhar a arvore sobre OUTRA janela ----
            // A excecao do LEVEL-UP e a mesma do portao (RSTV-8): a janela modal do level-up esta
            // aberta e o portao LIBERA de proposito nesse momento.
            UIWindowManager wm = UIWindowManager.Instance;
            if (!RunTargets.JanelaDoLevelUpAberta() && wm != null &&
                wm.AnyUIWindowOpenOtherThan(RoguelikeManager.Instance))
            {
                Plugin.Log.LogWarning("RSTV-11: atalho " + tecla + " ignorado — ja existe uma janela de UI " +
                                      "aberta (UIWindowManager.OpenedWindows).");
                return;
            }

            // O despacho da RUN e o MESMO corpo do botao: a RSTV-11b extraiu o `OnClick` para
            // `RunButton.OpenForTarget` (portao 4 + alvo resolvido na hora + Open(alvo, Run)). Assim o
            // atalho, o botao do HUD e o botao da janela do level-up abrem por UM caminho so.
            Plugin.Log.LogInfo("RSTV-11: atalho " + tecla + " -> despacho da run (RunButton.OpenForTarget).");
            RunButton.OpenForTarget();
        }
    }
}
