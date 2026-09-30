using System;
using System.Collections.Generic;
using Burst2Flame;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>De onde o botao da Skill Tree foi aberto. O ciclo de vida (SkillTreeReadOnly.Tick) e
    /// diferente para cada um: a tela Select Party fecha por fora, a run nao.</summary>
    internal enum ReadOnlyContext
    {
        PartyScreen,
        Run
    }

    /// <summary>
    /// RSTV-5: alvo do botao DURANTE A RUN e o PORTAO DE SEGURANCA (o coracao desta etapa).
    ///
    /// Contexto provado no decompilado:
    ///   - `CurrentCharacterUI.pingBtn` (l.209464) -> `ButtonPressedPing()` (l.210027) ->
    ///     `GUIManager.TogglePingMode()` (l.119299). Hierarquia: GUI Manager -> In Game GUI -> Ping Button
    ///     (irmaos: End Turn Button, End Turn Button Backup, Flee Button, Ping Button, Resume Turn Button).
    ///   - `HexCellManager.CurrentState` (l.121740, enum `PlayerState` l.155162 = Waiting/Movement/Action):
    ///     `Action` e o MODO DE MIRA. Escrever `GameLogic.CurrentlySelectedCharacter` durante a mira forca
    ///     `CurrentState = Movement` (l.108156) e CANCELA o apontar hex — por isso a mira e um portao.
    ///   - `PlayerMovement.ProcessLeftMouseClick` (l.153277) trata o clique no hex; o branch de ACAO
    ///     (l.153393-153397) NAO checa `GUIManager.PointerOverUIObject` (o de movimento checa, l.153342).
    ///
    /// O portao e conservador de proposito: em qualquer duvida (inclusive excecao ao ler o estado do
    /// jogo) o botao fica escondido/desabilitado e o motivo vai para o log — ver `RunButton`.
    /// </summary>
    internal static class RunTargets
    {
        /// <summary>GUIStates em que a janela pode existir durante a run (whitelist do RSTV-5).</summary>
        private static readonly GUIState[] AllowedStates =
        {
            GUIState.InBattle,
            GUIState.InWorldMap,
            GUIState.InTown
        };

        internal static bool StateAllowed(GUIState state)
        {
            for (int i = 0; i < AllowedStates.Length; i++)
            {
                if (AllowedStates[i] == state)
                {
                    return true;
                }
            }

            return false;
        }

        /// <summary>
        /// `Root` dentro de `Character`/`GameLogic` e uma propriedade PRIVADA (shadow do tipo); o caminho
        /// publico e via NetworkingManager (l.144636, `NetworkManager : NetworkObserver&lt;Root&gt;`) — mesmo
        /// padrao usado no RoguelikeDebugger deste repositorio.
        /// </summary>
        internal static Root GameRoot()
        {
            try
            {
                NetworkingManager nm = NetworkingManager.Instance;
                if (nm == null || nm.NetworkManager == null)
                {
                    return null;
                }

                return nm.NetworkManager.Root;
            }
            catch (Exception)
            {
                return null;
            }
        }

        /// <summary>Modo Roguelike? `Root.PlayingRoguelike` (l.140736) e o mesmo campo que a tela Select
        /// Party usa para ligar o `roguelikePowerupButton` (l.108236).</summary>
        internal static bool Roguelike
        {
            get
            {
                try
                {
                    Root root = GameRoot();
                    return root != null && root.PlayingRoguelike;
                }
                catch (Exception)
                {
                    return false;
                }
            }
        }

        /// <summary>
        /// PORTAO 4 — o botao so aparece/quando pode abrir se TODAS estas condicoes fecharem.
        /// Cada motivo e uma frase pronta para o log (nada de "estado invalido" generico).
        /// </summary>
        internal static bool GateOk(out string motivo)
        {
            motivo = null;
            try
            {
                GUIManager gui = GUIManager.instance;
                if (gui == null)
                {
                    motivo = "GUIManager.instance ausente";
                    return false;
                }

                if (!Roguelike)
                {
                    motivo = "fora do modo Roguelike (Root.PlayingRoguelike=false)";
                    return false;
                }

                GUIState estado = gui.CurrentGuiState;
                if (!StateAllowed(estado))
                {
                    motivo = "GUIState " + estado + " fora da whitelist da run (InBattle/InWorldMap/InTown)";
                    return false;
                }

                // Level-up pendente: o RoguelikeManager reescreve o personagem selecionado por conta
                // propria (l.163711-163713: guarda `storedCurrentlySelectedCharacter` e troca a selecao).
                if (RoguelikeManager.IsNotNullAndIsActive)
                {
                    motivo = "RoguelikeManager ativo (level-up/reroll pendente): ele troca o personagem selecionado sozinho";
                    return false;
                }

                HexCellManager hcm = HexCellManager.instance;
                if (hcm != null && hcm.CurrentState == PlayerState.Action)
                {
                    motivo = "mira de skill ativa (HexCellManager.CurrentState=Action): abrir aqui cancelaria o apontar hex";
                    return false;
                }

                if (gui.PingModeActive)
                {
                    motivo = "modo de apontar o hex ligado (GUIManager.PingModeActive)";
                    return false;
                }

                // Qualquer janela de UI aberta (inventario, pause, event window...) => nao empilhar.
                UIWindowManager wm = UIWindowManager.Instance;
                if (wm != null && wm.AnyUIWindowOpen)
                {
                    motivo = "ja existe uma janela de UI aberta (UIWindowManager.OpenedWindows)";
                    return false;
                }

                Root root = GameRoot();
                if (root == null)
                {
                    motivo = "Root ausente (NetworkingManager/NetworkManager nulos)";
                    return false;
                }
                if (root.SpawnPlacementActive)
                {
                    motivo = "posicionamento inicial em andamento (Root.SpawnPlacementActive)";
                    return false;
                }

                if (estado == GUIState.InBattle)
                {
                    // Checagens de TURNO/animation: so fazem sentido em batalha. Fora dela
                    // `IsPlayerTurnAndReady` fica no ultimo valor do combate anterior (l.110300 seta false
                    // no fim do turno) e bloquearia o botao no mapa do mundo inteiro.
                    if (!root.IsPlayerTurnAndReady)
                    {
                        motivo = "nao e o turno do jogador (Root.IsPlayerTurnAndReady=false)";
                        return false;
                    }

                    if (root.AnyActingCharactersInBattle)
                    {
                        motivo = "algum personagem esta executando acao (Root.AnyActingCharactersInBattle)";
                        return false;
                    }

                    if (root.AnyMovingCharactersInBattle)
                    {
                        motivo = "algum personagem esta em movimento (Root.AnyMovingCharactersInBattle)";
                        return false;
                    }
                }

                return true;
            }
            catch (Exception e)
            {
                // Lado seguro: NAO abrir. O pior caso e o jogador nao ver a arvore agora.
                motivo = "falha ao avaliar o estado do jogo (" + e.GetType().Name + ": " + e.Message + ")";
                return false;
            }
        }

        /// <summary>
        /// Alvo do clique DURANTE A RUN, resolvido NA HORA (nunca cacheado):
        ///   1. o personagem selecionado no jogo, se for seu (`Character.Owned`, l.32261);
        ///   2. FALLBACK DOCUMENTADO: se o jogo nao tem ninguem selecionado (`CurrentlySelectedCharacter == null`),
        ///      o PRIMEIRO personagem local da party. O jogo nao guarda "ultimo selecionado", e sem
        ///      selecao nenhuma o tooltip da arvore leria o contexto errado.
        /// Devolve null (com o motivo) quando nao ha alvo — nunca "o ultimo global".
        /// </summary>
        internal static Character Resolve(out string motivo)
        {
            motivo = null;
            try
            {
                GameLogic gl = GameLogic.instance;
                if (gl == null)
                {
                    motivo = "GameLogic.instance ausente";
                    return null;
                }

                Character selecionado = gl.CurrentlySelectedCharacter;
                if (selecionado != null)
                {
                    if (!selecionado.Owned)
                    {
                        motivo = "'" + selecionado.CharacterName + "' e de outro jogador (Owned=false)";
                        return null;
                    }

                    return selecionado;
                }

                Character fallback = FirstOwned(LocalParty());
                if (fallback == null)
                {
                    motivo = "nenhum personagem SEU na party e nenhum selecionado no jogo";
                    return null;
                }

                Plugin.Log.LogInfo("RSTV-5: o jogo esta sem personagem selecionado — usando o fallback " +
                                   "documentado '" + fallback.CharacterName + "' (primeiro personagem local da party).");
                return fallback;
            }
            catch (Exception e)
            {
                motivo = "falha ao resolver o alvo (" + e.GetType().Name + ": " + e.Message + ")";
                return null;
            }
        }

        /// <summary>
        /// Party LOCAL (nunca a do outro jogador): `MyPartyCharacters` e, se ela ainda nao estiver
        /// montada, `MyPartyCharactersUnaccepted` — a mesma lista usada pelo `PartyTargets`.
        /// </summary>
        private static List<Character> LocalParty()
        {
            NetworkingManager nm = NetworkingManager.Instance;
            if (nm == null)
            {
                return null;
            }

            List<Character> party = nm.MyPartyCharacters;
            if (party != null && party.Count > 0)
            {
                return party;
            }

            return nm.MyPartyCharactersUnaccepted;
        }

        private static Character FirstOwned(List<Character> lista)
        {
            if (lista == null)
            {
                return null;
            }

            for (int i = 0; i < lista.Count; i++)
            {
                Character c = lista[i];
                if (c != null && c.Owned)
                {
                    return c;
                }
            }

            return null;
        }
    }
}
