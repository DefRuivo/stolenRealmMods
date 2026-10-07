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
    /// O ALVO do clique DURANTE A RUN e o PORTAO QUE DECIDE SE O CLIQUE PODE ABRIR.
    ///
    /// RSTV-30 (06/10, pedido do dono em jogo) — O QUE MUDOU AQUI
    /// ---------------------------------------------------------
    /// Este portao deixou de decidir a VISIBILIDADE do botao: ele decide so se o clique pode
    /// ABRIR. O botao vive na barra de baixo do HUD (`RunButton`, RSTV-30), entao quem manda na
    /// presenca dele e o proprio HUD (o JOGO desliga o HUD inteiro no menu, na janela de evento,
    /// no level-up, na loja e em `ChoosingCharacter`/`CreatingCharacter` — `GUIManager.Update`
    /// l.120485). Enquanto o portao escondia o botao, o dono via o defeito: "o botao some e depois
    /// reaparece" quando qualquer personagem agia, e "nao aparece enquanto estamos fora de combate".
    ///
    /// GUARDAS QUE SAIRAM NA RSTV-30 (com o defeito que cada uma causava — guarda sem justificativa
    /// e defeito, nao seguranca):
    ///   * `StateAllowed` (whitelist InBattle/InWorldMap/InTown) — o JOGO ja desliga o HUD inteiro
    ///     fora desses estados (l.120485) e a regra nativa do botao 'Skills' do HUD (l.120491)
    ///     cobre exatamente esse conjunto; a whitelist so escondia o botao em estados em que o HUD
    ///     esta visivel (`GUIState.ChoosingCharacter` — o log de 06/10 16:59 mostra o botao
    ///     escondido exatamente por ela);
    ///   * `Root.IsPlayerTurnAndReady` — fica no ULTIMO valor do combate anterior (`GameLogic`
    ///     l.111904 seta false no fim do turno), ou seja, escondia o botao fora do turno do jogador
    ///     (o "nao aparece fora de combate" do dono) sem proteger nada: abrir o menu de personagem
    ///     no turno do inimigo e permitido pelo proprio jogo (o botao nativo continua clicavel);
    ///   * `Root.AnyActingCharactersInBattle` e `Root.AnyMovingCharactersInBattle` — eram a causa
    ///     DIRETA do piscar: qualquer personagem agindo/movendo fechava o portao e o botao sumia.
    ///     Nao protegiam nada: a unica escrita do caminho de abertura (definir
    ///     `GameLogic.CurrentlySelectedCharacter` quando NENHUM esta selecionado) nao cancela
    ///     animacao nenhuma, e o jogo deixa abrir o inventario durante elas.
    ///
    /// GUARDAS QUE FICARAM, cada uma com a justificativa de DANO REAL que ela evita (RSTV-30):
    ///   * GUARDA 1 (tecnica) `GUIManager.instance` — sem o manager nao ha estado de UI para ler;
    ///   * GUARDA 2 (escopo) `Root.PlayingRoguelike` — o botao e da RUN; a campanha tem o proprio
    ///     botao nativo de skills, que ESCREVE pontos (nao duplicar uma superficie de escrita);
    ///   * GUARDA 3 (dano real) `GUIManager.PingModeActive` — abrir aqui cancela o apontar o hex;
    ///   * GUARDA 4 (dano real) `UIWindowManager.AnyUIWindowOpen` — nao empilhar janelas: o
    ///     caminho de abertura ABRE o inventario (`SkillTreesTab.Abrir`), e abrir por cima de uma
    ///     janela ja aberta deixa a UI em estado que nao e o do jogo;
    ///   * GUARDA 5 (dano real, SO em batalha) `HexCellManager.CurrentState == PlayerState.Action`
    ///     — a MIRA de skill: escrever `GameLogic.CurrentlySelectedCharacter` durante a mira forca
    ///     `CurrentState = Movement` (l.110065) e CANCELA o apontar hex;
    ///   * GUARDA 6 (dano real, SO em batalha) `Root.SpawnPlacementActive` — o posicionamento
    ///     inicial da batalha: a abertura mexe no personagem selecionado justamente quando o jogo
    ///     esta posicionando o time.
    ///
    /// Contexto do alvo, provado no decompilado:
    ///   - `CurrentCharacterUI.pingBtn` (l.329889) -> `ButtonPressedPing()` (l.330452) ->
    ///     `GUIManager.TogglePingMode()` (l.120930);
    ///   - `HexCellManager.CurrentState` (l.123371, enum `PlayerState` l.160171 = Waiting/Movement/Action):
    ///     `Action` e o MODO DE MIRA — por isso a mira e uma guarda;
    ///   - `PlayerMovement.ProcessLeftMouseClick` (l.158281) trata o clique no hex; o branch de ACAO
    ///     (l.158397-158400) NAO checa `GUIManager.PointerOverUIObject` (o de movimento checa, l.158288).
    ///
    /// Lado seguro: em qualquer duvida (inclusive excecao ao ler o estado do jogo) o portao RECUSA —
    /// e o clique que nao abre; o botao continua na tela e o motivo vai para o log — ver `RunButton`.
    /// </summary>
    internal static class RunTargets
    {

        // RSTV-7: o fallback e reavaliado 10x por segundo pelo `RunButton.Mirror`. Sem esta guarda,
        // um estado estavel "sem personagem selecionado" re-logaria a MESMA linha a cada 0,1 s — o
        // mesmo defeito de frequencia do log do motivo do botao (avisar UMA vez por motivo). Guarda
        // o alvo de fallback ja avisado; rearma quando o jogo volta a ter personagem selecionado.
        private static string _fallbackLogado;

        /// <summary>
        /// RSTV-30: a MESMA lista que o JOGO usa para habilitar os botoes de personagem do HUD
        /// (`GUIManager.Update` l.120491: `CurrentGuiState` em InTown/InWorldMap/InCutscene/InBattle).
        /// Ela substitui a antiga `StateAllowed` (whitelist do mod, removida na RSTV-30): e a mesma
        /// ideia, mas lida do jogo — e quem usa e o ATALHO de teclado, que nao tem botao nativo para
        /// espelhar. Nos outros estados o HUD inteiro esta desligado (l.120485).
        /// </summary>
        internal static bool EstadoPermiteMenuDePersonagem(GUIState estado)
        {
            return estado == GUIState.InTown || estado == GUIState.InWorldMap ||
                   estado == GUIState.InCutscene || estado == GUIState.InBattle;
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
        /// O portao do CLIQUE (RSTV-30): devolve true quando abrir a arvore AGORA e seguro. Ele NAO
        /// decide mais se o botao aparece — a visibilidade e do HUD, que e dono da barra de baixo em
        /// que o clone mora (ver o cabecalho da classe). Cada guarda carrega a sua justificativa (o
        /// dano real que evita) e cada motivo e uma frase pronta para o log (nada de "estado
        /// invalido" generico).
        /// </summary>
        internal static bool GateOk(out string motivo)
        {
            motivo = null;
            try
            {
                // GUARDA 1 (tecnica) — `GUIManager.instance`. Justificativa: e nele que moram TODAS
                // as outras leituras deste portao (ping, janela, GUIState); sem ele nao ha estado de
                // UI para ler.
                GUIManager gui = GUIManager.instance;
                if (gui == null)
                {
                    motivo = "GUIManager.instance ausente";
                    return false;
                }

                // GUARDA 2 (escopo) — `Root.PlayingRoguelike`. Justificativa: o botao e da RUN. Na
                // campanha o HUD tem o botao nativo de skill tree, que ESCREVE pontos
                // (`SkillTreeManager.AcceptSkillChanges`, l.177650) — duplicar aquela superficie com
                // uma que so LE deixaria duas coisas diferentes com a mesma cara no mesmo lugar.
                if (!Roguelike)
                {
                    motivo = "fora do modo Roguelike (Root.PlayingRoguelike=false)";
                    return false;
                }

                // RSTV-8 - LEVEL-UP: a janela do RoguelikeManager esta ABERTA e ele reescreveu o
                // `GameLogic.CurrentlySelectedCharacter` para o personagem SENDO NIVELADO
                // (OpenSkillSelectWindow: l.168929 define; l.168932 guarda em
                // `CurrentRoguelikeSkillSelectingCharacter`; o Close devolve o antigo: l.169094-169097).
                // Isso NAO e motivo para esconder o botao: o nivel-up e EXATAMENTE quando o jogador
                // quer consultar a arvore. O que NAO se perde e a ORIGEM do alvo: `Resolve` le o
                // personagem nivelado do PROPRIO manager, nunca do `CurrentlySelectedCharacter` (que
                // e justamente o que o manager troca).
                if (LevelUpAberto())
                {
                    return true;
                }

                // ------------------------------------------------------------------------------
                // RSTV-13/RSTV-30 — QUAIS GUARDAS VALEM EM CADA ESTADO (mapa x batalha)
                //
                // Os portoes que sobraram descrevem UMA BATALHA EM ANDAMENTO (mira de skill,
                // posicionamento inicial) e por isso moram DENTRO do ramo `InBattle`: aplicados ao
                // MAPA-MUNDO eles esconderiam o botao justamente enquanto o jogador passeia — o
                // sintoma que o dono relatou. As guardas de turno/animacao que existiam aqui foram
                // REMOVIDAS na RSTV-30 (o defeito de cada uma esta no cabecalho da classe): eram elas
                // que faziam o botao piscar quando qualquer personagem agia.
                // ------------------------------------------------------------------------------

                // GUARDA 3 (dano real, universal) — modo de apontar o hex.
                // Justificativa: abrir a arvore ESCREVE `GameLogic.CurrentlySelectedCharacter`
                // (`SkillTreeReadOnly`: define o alvo quando o jogo nao tem nenhum selecionado) e
                // escrever esse campo durante a mira forca `CurrentState = Movement` (l.110065),
                // CANCELANDO o apontar o hex que o jogador tinha comecado.
                if (gui.PingModeActive)
                {
                    motivo = "modo de apontar o hex ligado (GUIManager.PingModeActive)";
                    return false;
                }

                // GUARDA 4 (dano real, universal) — qualquer janela de UI aberta (inventario, pause,
                // event window...). Justificativa: o caminho de abertura ABRE O INVENTARIO
                // (`SkillTreesTab.Abrir`, a aba de todas as arvores) e o poe em
                // `UIWindowManager.OpenedWindows`; abrir por cima de uma janela que o jogo ja abriu
                // deixa a UI num estado que nao e o do jogo (o inventario aparece sem o jogo te-lo
                // pedido, com o `CurrentGuiState`/`InMenus` do estado anterior).
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

                if (gui.CurrentGuiState == GUIState.InBattle)
                {
                    // GUARDA 5 (dano real, SO em batalha) — mira de skill ativa.
                    // Justificativa: mesma familia da GUARDA 3, no modo `Action` do
                    // `HexCellManager.CurrentState` (l.123371): o clique no hex na mira NAO checa
                    // `PointerOverUIObject` (l.158397-158400) e a abertura cancela o apontar.
                    HexCellManager hcm = HexCellManager.instance;
                    if (hcm != null && hcm.CurrentState == PlayerState.Action)
                    {
                        motivo = "mira de skill ativa (HexCellManager.CurrentState=Action): abrir aqui cancelaria o apontar hex";
                        return false;
                    }

                    // GUARDA 6 (dano real, SO em batalha) — posicionamento inicial da batalha.
                    // Justificativa: e a fase em que o JOGO esta posicionando o time e mexendo no
                    // personagem selecionado (`Root.SpawnPlacementActive`, l.112152 liga /
                    // l.112165 desliga); a abertura tambem mexe nesse campo, entao ela espera.
                    if (root.SpawnPlacementActive)
                    {
                        motivo = "posicionamento inicial em andamento (Root.SpawnPlacementActive)";
                        return false;
                    }
                }

                return true;
            }
            catch (Exception e)
            {
                // Lado seguro: NAO abrir. O pior caso e o jogador nao ver a arvore agora — e o
                // botao continua na tela (RSTV-30: quem e escondido por engano era o defeito).
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
