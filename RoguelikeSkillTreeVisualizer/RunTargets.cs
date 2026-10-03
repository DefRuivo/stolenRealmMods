using System;
using System.Collections.Generic;
using Burst2Flame;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>De onde o botao/atalho abriu a visualizacao. RSTV-16: a vida da sessao read-only passou
    /// a ser a do SISTEMA DE ABAS do inventario (SkillTreesTab); o contexto e so para o log e para os
    /// patches saberem por qual caminho a sessao nasceu.</summary>
    internal enum ReadOnlyContext
    {
        PartyScreen,
        Run,
        Inventario,

        /// <summary>RSTV-20: o botao do CABECALHO do modal "Remove Skill Trees" — a sessao nasce para
        /// o personagem do proprio modal.</summary>
        RemocaoDeArvores
    }

    /// <summary>
    /// RSTV-5: alvo do botao DURANTE A RUN e o PORTAO DE SEGURANCA (o coracao desta etapa).
    ///
    /// Contexto provado no decompilado:
    ///   - `CurrentCharacterUI.pingBtn` (l.329889) -> `ButtonPressedPing()` (l.330452) ->
    ///     `GUIManager.TogglePingMode()` (l.120930). Hierarquia: GUI Manager -> In Game GUI -> Ping Button
    ///     (irmaos: End Turn Button, End Turn Button Backup, Flee Button, Ping Button, Resume Turn Button).
    ///   - `HexCellManager.CurrentState` (l.123371, enum `PlayerState` l.160171 = Waiting/Movement/Action):
    ///     `Action` e o MODO DE MIRA. Escrever `GameLogic.CurrentlySelectedCharacter` durante a mira forca
    ///     `CurrentState = Movement` (l.110065) e CANCELA o apontar hex — por isso a mira e um portao.
    ///   - `PlayerMovement.ProcessLeftMouseClick` (l.158281) trata o clique no hex; o branch de ACAO
    ///     (l.158397-158400) NAO checa `GUIManager.PointerOverUIObject` (o de movimento checa, l.158288).
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

        // RSTV-7: o fallback e reavaliado 10x por segundo pelo `RunButton.Mirror`. Sem esta guarda,
        // um estado estavel "sem personagem selecionado" re-logaria a MESMA linha a cada 0,1 s — o
        // mesmo defeito de frequencia do log do motivo do botao (avisar UMA vez por motivo). Guarda
        // o alvo de fallback ja avisado; rearma quando o jogo volta a ter personagem selecionado.
        private static string _fallbackLogado;

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
        /// publico e via NetworkingManager (l.149654, `NetworkManager : NetworkObserver&lt;Root&gt;` l.149542) — mesmo
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

        /// <summary>Modo Roguelike? `Root.PlayingRoguelike` (l.145640) e o mesmo campo que a tela Select
        /// Party usa para ligar o `roguelikePowerupButton` (l.328661).</summary>
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
        /// RSTV-8: o LEVEL-UP esta com a janela ABERTA agora?
        ///
        /// `RoguelikeManager.IsNotNullAndIsActive` (l.168661) so diz que o manager foi CARREGADO —
        /// o GameObject dele fica ativo durante a run inteira depois do primeiro level-up (o
        /// `LoadReference` instancia o prefab, l.168005-168014). A janela de verdade e o FILHO
        /// `SkillSelectWindow` (l.168597), o mesmo criterio que o proprio jogo usa em
        /// `GUIManager.Update` (l.120492, para esconder o HUD) e no `SkillSelectActive` (l.230294).
        /// `Instance` e auto-property publica (l.168659): nada aqui carrega instancia nova.
        /// </summary>
        private static bool LevelUpAberto()
        {
            try
            {
                RoguelikeManager rok = RoguelikeManager.Instance;
                return rok != null && rok.SkillSelectWindow != null && rok.SkillSelectWindow.activeSelf;
            }
            catch (Exception)
            {
                // Lado seguro: nao afirmar level-up sem conseguir ler o manager.
                return false;
            }
        }

        /// <summary>
        /// Expõe o MESMO criterio de `LevelUpAberto` para quem precisa TRATAR o level-up como uma
        /// exceção: o atalho de teclado (RSTV-11a, guard de janela) e a referencia de z-order
        /// (RSTV-11a PARTE 2, no level-up o HUD/CurrentCharacterUI esta desligado). Nao duplica o
        /// criterio: delega para `LevelUpAberto`, a fonte unica (a RSTV-8 e dona do portao). O
        /// `RunButton` NAO usa mais este metodo — o botao do level-up e proprio da janela
        /// (`LevelUpWindowButton`, RSTV-11b), que aposentou o re-parent da RSTV-9.
        /// </summary>
        internal static bool JanelaDoLevelUpAberta()
        {
            return LevelUpAberto();
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

                // RSTV-8 - LEVEL-UP: a janela do RoguelikeManager esta ABERTA e ele reescreveu o
                // `GameLogic.CurrentlySelectedCharacter` para o personagem SENDO NIVELADO
                // (OpenSkillSelectWindow: l.168929 define; l.168932 guarda em
                // `CurrentRoguelikeSkillSelectingCharacter`; o Close devolve o antigo: l.169094-169097).
                // Isso NAO e motivo para esconder o botao: o level-up e EXATAMENTE quando o jogador
                // quer consultar a arvore. A janela do level-up ainda convive com o PostBattleManager
                // em `UIWindowManager.OpenedWindows` (o `OpenWindow` dele e l.332398), entao os portoes
                // abaixo - que descrevem a RUN em andamento (mira, ping, janela, spawn, turno,
                // animacao) - ficam SUSPENSOS neste menu modal. O que NAO se perde e a ORIGEM do alvo:
                // `Resolve` le o personagem nivelado do PROPRIO manager, nunca do
                // `CurrentlySelectedCharacter` (que e justamente o que o manager troca).
                if (LevelUpAberto())
                {
                    return true;
                }

                // ------------------------------------------------------------------------------
                // RSTV-13 — QUAIS PORTOES VALEM EM CADA ESTADO (mapa x batalha)
                //
                // Os portoes abaixo descrevem UMA BATALHA EM ANDAMENTO (mira de skill, animacao,
                // turno, posicionamento inicial). Aplicados ao MAPA-MUNDO eles escondem o botao
                // justamente enquanto o jogador passeia — o sintoma do dono. `IsPlayerTurnAndReady`
                // fica no ULTIMO valor do combate anterior (l.111904 seta false no fim do turno) e
                // `SpawnPlacementActive` so existe no setup da batalha (l.112152 liga, l.112165
                // desliga). Por isso os portoes de batalha moram DENTRO do ramo `InBattle`; no mapa
                // (`InWorldMap`) e na cidade (`InTown`) valem apenas os que descrevem a JANELA
                // (ping, UI aberta) e o alvo — o botao APARECE no mapa-mundo.
                // ------------------------------------------------------------------------------

                // Universal (InBattle/InWorldMap/InTown): modo de apontar o hex.
                if (gui.PingModeActive)
                {
                    motivo = "modo de apontar o hex ligado (GUIManager.PingModeActive)";
                    return false;
                }

                // Universal: qualquer janela de UI aberta (inventario, pause, event window...) => nao empilhar.
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

                if (estado == GUIState.InBattle)
                {
                    // Daqui para baixo: portoes que SO existem em batalha (RSTV-13).

                    HexCellManager hcm = HexCellManager.instance;
                    if (hcm != null && hcm.CurrentState == PlayerState.Action)
                    {
                        motivo = "mira de skill ativa (HexCellManager.CurrentState=Action): abrir aqui cancelaria o apontar hex";
                        return false;
                    }

                    if (root.SpawnPlacementActive)
                    {
                        motivo = "posicionamento inicial em andamento (Root.SpawnPlacementActive)";
                        return false;
                    }

                    // `IsPlayerTurnAndReady` fica no ultimo valor do combate anterior (l.111904 seta
                    // false no fim do turno) e bloquearia o botao no mapa do mundo inteiro.
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
        /// RSTV-8: o personagem SENDO NIVELADO, lido do PROPRIO RoguelikeManager — nunca do
        /// `CurrentlySelectedCharacter`, que e justamente o que o manager reescreve enquanto a
        /// janela esta aberta (l.168929 define; l.169094-169097 devolve no Close).
        ///
        ///   1. `CurrentRoguelikeSkillSelectingCharacter` (l.168726): o campo canonico do level-up,
        ///      definido junto com a janela (l.168932) e zerado no Close (l.169084);
        ///   2. FALLBACK: `CharactersWaitingForLevelUp[0].Character` (l.168655/168863-168866) — o
        ///      primeiro da fila e o que a janela esta mostrando.
        ///
        /// Devolve null quando nao ha level-up aberto (o fluxo normal do `Resolve` segue).
        /// </summary>
        private static Character AlvoDoLevelUp()
        {
            try
            {
                if (!LevelUpAberto())
                {
                    return null;
                }

                RoguelikeManager rok = RoguelikeManager.Instance;
                Character nivelando = rok.CurrentRoguelikeSkillSelectingCharacter;
                if (nivelando != null)
                {
                    return nivelando;
                }

                List<CharacterLevelUpInfo> fila = rok.CharactersWaitingForLevelUp;
                if (fila != null && fila.Count > 0 && fila[0] != null)
                {
                    return fila[0].Character;
                }

                return null;
            }
            catch (Exception)
            {
                return null;
            }
        }

        /// <summary>
        /// Alvo do clique DURANTE A RUN, resolvido NA HORA (nunca cacheado):
        ///   0. RSTV-8: se a janela do LEVEL-UP esta aberta, o personagem SENDO NIVELADO, lido do
        ///      proprio RoguelikeManager (ver `AlvoDoLevelUp`) — nao do `CurrentlySelectedCharacter`;
        ///   1. o personagem selecionado no jogo, se for seu (`Character.Owned`, l.33151);
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

                // RSTV-8: durante o level-up o alvo e o personagem SENDO NIVELADO, lido do manager
                // (nao do CurrentlySelectedCharacter, que o manager troca ao abrir a janela).
                Character nivelando = AlvoDoLevelUp();
                if (nivelando != null)
                {
                    _fallbackLogado = null;

                    if (!nivelando.Owned)
                    {
                        motivo = "'" + nivelando.CharacterName +
                                 "' esta em level-up mas e de outro jogador (Owned=false)";
                        return null;
                    }

                    return nivelando;
                }

                Character selecionado = gl.CurrentlySelectedCharacter;
                if (selecionado != null)
                {
                    // Voltou a ter selecao: rearma o aviso do fallback (a proxima vez que o jogo
                    // ficar sem selecao volta a valer uma linha).
                    _fallbackLogado = null;

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

                // Uma linha por motivo: so avisa quando o alvo de fallback MUDA (o chamador roda
                // 10x por segundo).
                if (_fallbackLogado != fallback.CharacterName)
                {
                    _fallbackLogado = fallback.CharacterName;
                    Plugin.Log.LogInfo("RSTV-5: o jogo esta sem personagem selecionado — usando o fallback " +
                                       "documentado '" + fallback.CharacterName + "' (primeiro personagem local da party).");
                }

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
