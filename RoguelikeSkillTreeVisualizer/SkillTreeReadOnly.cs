using System;
using System.Collections.Generic;
using System.Linq;
using Burst2Flame;
using UnityEngine;

namespace RoguelikeSkillTreeVisualizer
{
    /// <summary>
    /// RSTV-2c/2d: abre a Skill Tree NATIVA (`SkillTreeManager`, l.172045 — a mesma do
    /// Campaign -> Change Skills) para o personagem da party, em modo SOMENTE LEITURA.
    ///
    /// A abertura segue o caminho real do jogo (CharacterMenusManager.OpenSkillTreeMenu,
    /// l.48471-48482):
    ///   1. `LoadableUIWindow&lt;SkillTreeManager&gt;.LoadInstanceReference(prefab, placeholder)` +
    ///      espera `Instance != null` (l.48471-48480);
    ///   2. `Instance.Initialize(SkillsFromPoints, unspentPoints, creating)` (l.48481 / l.172380);
    ///   3. `Instance.gameObject.SetActive(true)` (l.48482).
    ///
    /// O contexto do personagem NAO entra por parametro: `SkillTreeManager` e o `Tooltip` leem
    /// `GameLogic.instance.CurrentlySelectedCharacter` (l.172823, l.172388 e o `TooltipCharacter`
    /// do tooltip, l.213124 — e por ele que o tooltip calcula custo de mana, alcance, dano e
    /// "ObtainedByItem/Status"). Por isso o setter e chamado ANTES de abrir; ele e publico
    /// (l.108082) e recusa personagem nao-Owned (l.108117-108120), o que casa com a regra do mod
    /// (so personagens do proprio jogador).
    ///
    /// NUNCA chamar `CharacterMenusManager.CloseSkillTreeMenu()` (l.48490): ele chama
    /// `AcceptSkillChanges(closeMenu: true)` e ESCRITA. O fechamento e feito pelo proprio botao da
    /// janela nativa (que passa por AcceptSkillChanges -> o prefixo de higienizacao em Patches.cs).
    /// </summary>
    internal static class SkillTreeReadOnly
    {
        private static Character _pendingTarget;
        private static float _pendingSince;
        private static ReadOnlyContext _pendingContext;
        private const float PendingTimeout = 15f;

        /// <summary>Botao da tela Select Party (RSTV-2).</summary>
        internal static void Open(Character target)
        {
            Open(target, ReadOnlyContext.PartyScreen);
        }

        internal static void Open(Character target, ReadOnlyContext context)
        {
            try
            {
                OpenInternal(target, context);
            }
            catch (Exception e)
            {
                _pendingTarget = null;
                ReadOnlySession.End();
                ReadOnlySession.RestoreSelection();
                Plugin.Log.LogError("RSTV: falha ao abrir a skill tree read-only: " + e);
            }
        }

        private static void OpenInternal(Character target, ReadOnlyContext context)
        {
            if (target == null)
            {
                Plugin.Log.LogWarning("RSTV: pedido de abrir a arvore sem personagem — nada a fazer.");
                return;
            }

            if (GameLogic.instance == null)
            {
                Plugin.Log.LogError("RSTV: GameLogic.instance ausente — sem ele a arvore mostraria o " +
                                    "personagem errado; abertura cancelada.");
                return;
            }

            // Reabertura com uma sessao viva (clique duplo, dois cliques no mesmo frame): fechar ANTES
            // de decidir o alvo, senao a decisao seria tomada com o personagem que a sessao antiga
            // escreveu — e o `Close()` logo abaixo devolveria a selecao ao valor de antes, deixando a
            // arvore nova com o contexto de tooltip errado.
            if (ReadOnlySession.Active)
            {
                Plugin.Log.LogInfo("RSTV-5: ja havia uma sessao read-only aberta — fechando antes de reabrir.");
                ReadOnlySession.Close();
            }

            // 1) contexto REAL do personagem (nivel, equipamento, atributos, status atuais)
            //    RSTV-5 / blindagem 2: isso SO acontece quando e inofensivo — ver SelectTargetInGame.
            if (!SelectTargetInGame(target, context))
            {
                return;
            }

            SkillTreeManager instance = LoadableUIWindow<SkillTreeManager>.Instance;
            if (instance == null)
            {
                _pendingTarget = target;
                _pendingContext = context;
                _pendingSince = Time.realtimeSinceStartup;
                ReferenceLoader loader = ReferenceLoader.Instance;
                if (loader == null)
                {
                    Plugin.Log.LogError("RSTV: ReferenceLoader ausente — nao da para carregar a skill tree.");
                    _pendingTarget = null;
                    ReadOnlySession.RestoreSelection();
                    return;
                }

                Plugin.Log.LogInfo("RSTV-2: SkillTreeManager ainda nao existia — carregando a instancia nativa.");
                LoadableUIWindow<SkillTreeManager>.LoadInstanceReference(
                    loader.SkillTreeManager.gameObject, loader.SkillTreeManagerPlaceholder);
                return;
            }

            Finish(target, context, instance);
        }

        /// <summary>
        /// BLINDAGEM 2 — `GameLogic.CurrentlySelectedCharacter` (setter l.108082).
        ///
        /// O setter NAO e um simples "campo": para um personagem DIFERENTE do atual ele marca
        /// `IsPartyLeader` (l.108121-108128), trava a camera (`CameraController.LockedOnTarget = true`,
        /// l.108133), FORCA `HexCellManager.CurrentState = Movement` (l.108156 — isso CANCELA a mira de
        /// skill no meio do apontar hex), chama `NotifyPlayerOfTheirTurn` (l.108179) e ainda roda
        /// `AcceptSkillChanges()` da arvore que estiver aberta (l.108137).
        ///
        /// Mas: `if (value != null &amp;&amp; currentlySelectedCharacter == value) return;` (l.108097) — escrever o
        /// MESMO personagem nao faz NADA. Entao:
        ///   1. igual ao alvo  -> escrever e um no-op: nao precisamos escrever (zero efeito colateral);
        ///   2. null           -> escrever e inofensivo (a metade perigosa do setter so roda com um
        ///                        personagem anterior != null); guardamos o anterior e restauramos no fim;
        ///   3. outro personagem -> NUNCA escrever: a arvore mostraria o contexto errado de tooltip
        ///                        (`Tooltip.TooltipCharacter`, l.213124) e os efeitos colaterais acima
        ///                        cairiam em cima de outro personagem. A abertura e RECUSADA com o motivo.
        /// </summary>
        private static bool SelectTargetInGame(Character target, ReadOnlyContext context)
        {
            GameLogic gl = GameLogic.instance;
            Character atual = gl.CurrentlySelectedCharacter;

            if (atual == target)
            {
                Plugin.Log.LogInfo("RSTV-5: o jogo JA tem '" + target.CharacterName + "' como personagem " +
                                   "selecionado — nenhuma escrita em GameLogic.CurrentlySelectedCharacter " +
                                   "(o setter retorna cedo, l.108097: sem mexer na camera, sem forcar " +
                                   "HexCellManager.CurrentState=Movement e sem NotifyPlayerOfTheirTurn).");
                return true;
            }

            if (atual != null)
            {
                Plugin.Log.LogWarning("RSTV-5: abertura RECUSADA — o jogo tem '" + atual.CharacterName +
                                      "' selecionado e o alvo e '" + target.CharacterName + "'; escrever " +
                                      "aqui forcaria Movement (cancela a mira), mexeria em IsPartyLeader/" +
                                      "camera e o tooltip da arvore leria o contexto errado. " +
                                      "Troque de personagem no jogo e clique de novo. contexto=" + context + ".");
                return false;
            }

            // atual == null: o setter nao tem personagem anterior para "desmontar" — e o caminho barato.
            ReadOnlySession.NoteSelectionToRestore(atual, target);
            gl.CurrentlySelectedCharacter = target;
            Plugin.Log.LogInfo("RSTV-5: nenhum personagem estava selecionado — definindo '" + target.CharacterName +
                               "' como selecionado (valor anterior guardado e devolvido no fechamento).");
            return true;
        }

        /// <summary>
        /// Chamado todo frame pelo `RstvHost`.
        ///
        /// BLINDAGEM 1 — a guarda de ciclo de vida deixou de ser "a tela Select Party esta aberta":
        /// durante a RUN essa tela esta desligada, e a guarda antiga fecharia a arvore NO FRAME
        /// SEGUINTE. Agora o criterio e "a instancia nativa da arvore continua ativa" +
        /// whitelist de GUIState (InBattle/InWorldMap/InTown) para o contexto da run; a checagem da
        /// tela de party continua valendo SO para o contexto de party (o jogo fecha aquela tela por
        /// fora — GUIState em l.118416, l.133307, l.215520 — e nada fecharia a arvore).
        ///
        /// BLINDAGEM 6 — se o jogo trocar o personagem selecionado (ou sair dos estados da run),
        /// a sessao e fechada: uma janela read-only com o contexto errado nao pode ficar aberta.
        /// </summary>
        internal static void Tick()
        {
            if (ReadOnlySession.Active)
            {
                string bloqueio = LifecycleBlock();
                if (bloqueio != null)
                {
                    Plugin.Log.LogInfo("RSTV-5: fechando a skill tree read-only — " + bloqueio +
                                       " (nada foi gravado no personagem).");
                    ReadOnlySession.Close();
                    return;
                }
            }
            else
            {
                // Rede de seguranca: sem sessao ativa, a nossa janela NAO pode continuar registrada em
                // UIWindowManager.OpenedWindows (senao o jogo fica para sempre com "InMenus" = input de
                // batalha morto). Barato: uma checagem por segundo.
                ReadOnlySession.CleanupIdleRegistration();
            }

            if (_pendingTarget == null)
            {
                return;
            }

            SkillTreeManager instance = LoadableUIWindow<SkillTreeManager>.Instance;
            if (instance != null)
            {
                Character target = _pendingTarget;
                ReadOnlyContext context = _pendingContext;
                _pendingTarget = null;
                Finish(target, context, instance);
                return;
            }

            if (Time.realtimeSinceStartup - _pendingSince > PendingTimeout)
            {
                _pendingTarget = null;
                Plugin.Log.LogError("RSTV: timeout esperando o SkillTreeManager carregar (15s).");
                ReadOnlySession.RestoreSelection();
            }
        }

        /// <summary>
        /// Devolve o motivo para FECHAR a sessao agora, ou null para continuar. A leitura falhar e
        /// motivo para fechar (falha-segura): uma janela read-only em estado desconhecido e pior que
        /// uma janela fechada.
        /// </summary>
        private static string LifecycleBlock()
        {
            try
            {
                SkillTreeManager instance = LoadableUIWindow<SkillTreeManager>.Instance;
                if (instance == null || instance.gameObject == null || !instance.gameObject.activeSelf)
                {
                    return "a instancia nativa da arvore nao esta mais ativa (instance==null ou janela inativa)";
                }

                GUIManager gui = GUIManager.instance;
                if (gui == null)
                {
                    return "GUIManager.instance ausente";
                }

                if (ReadOnlySession.Context == ReadOnlyContext.PartyScreen)
                {
                    if (!PartyScreenIsOpen())
                    {
                        return "a tela Select Party fechou";
                    }
                }
                else if (!RunTargets.StateAllowed(gui.CurrentGuiState))
                {
                    return "o jogo saiu dos estados permitidos da run (GUIState=" + gui.CurrentGuiState +
                           "; a whitelist e InBattle/InWorldMap/InTown)";
                }

                Character alvo = ReadOnlySession.Target;
                Character atual = GameLogic.instance != null ? GameLogic.instance.CurrentlySelectedCharacter : null;
                if (alvo != null && atual != alvo)
                {
                    return "o jogo trocou o personagem selecionado ('" +
                           (atual != null ? atual.CharacterName : "nenhum") + "' agora, a sessao era de '" +
                           alvo.CharacterName + "')";
                }

                return null;
            }
            catch (Exception e)
            {
                return "falha ao avaliar o ciclo de vida da janela (" + e.GetType().Name + ": " + e.Message + ")";
            }
        }

        /// <summary>
        /// A tela Select Party ainda esta aberta? Mesmo teste que o proprio jogo usa
        /// (`CharacterChoiceManager.IsNotNullAndIsActive`, l.208163-208167) e o mesmo objeto que o
        /// `CloseWindow()` do jogo desliga (`SetActive(false)`, l.208602-208607). Lido de forma
        /// barata, sem carregar instancia nenhuma: `Instance` e um auto-property (l.208155).
        /// </summary>
        private static bool PartyScreenIsOpen()
        {
            CharacterChoiceManager screen = CharacterChoiceManager.Instance;
            return screen != null && screen.gameObject != null && screen.gameObject.activeSelf;
        }

        private static void Finish(Character target, ReadOnlyContext context, SkillTreeManager instance)
        {
            try
            {
                if (target == null || instance == null)
                {
                    return;
                }

                // BLINDAGEM 3: fotografar QUEM tinha o slot unico de `UIWindowManager.CancelInterceptor`
                // (l.215982) ANTES de qualquer coisa. O `OnEnable` do SkillTreeManager instala o
                // interceptor DELE (l.172890) durante o `SetActive(true)` da linha abaixo — fotografar
                // depois so veria o delegate do proprio jogo.
                ReadOnlySession.CaptureInterceptorOwner();

                ReadOnlySession.Begin(target, context);

                // Ativa ANTES de inicializar: `Initialize` busca as abas com
                // `tabHolder.GetComponentsInChildren<SkillTreeTab>()` (l.172394), que ignora filhos
                // inativos — com a janela desligada as abas nao seriam encontradas.
                instance.gameObject.SetActive(true);
                instance.Initialize(target.SkillsFromPoints.ToList(), 0, false);
                ZOrder.EnsureAbove(instance.transform, ZOrderReference(context));

                // BLINDAGEM 5 (camada 1): registrar a janela no OpenedWindows do jogo. `GUIManager.InMenus`
                // (l.118297) passa a devolver true, e `PlayerMovement.ProcessUpdateInputs` (l.152986)
                // retorna ANTES de chamar o `ProcessLeftMouseClick` — ou seja, o clique do hex nao
                // chega mais ao branch de Action que NAO checa PointerOverUIObject (l.153393-153397).
                ReadOnlySession.RegisterAsOpenWindow(instance);

                ReadOnlySession.InstallCancelInterceptor();

                Plugin.Log.LogInfo("RSTV: skill tree read-only aberta para '" + target.CharacterName +
                                   "' (nivel " + target.Level + ", " + target.SkillsFromPoints.Count +
                                   " skills, 0 pontos, contexto=" + context + "). ativaNaHierarquia=" +
                                   instance.gameObject.activeInHierarchy);
            }
            catch (Exception e)
            {
                ReadOnlySession.End();
                ReadOnlySession.RestoreSelection();
                try
                {
                    if (instance != null)
                    {
                        instance.gameObject.SetActive(false);
                    }
                }
                catch (Exception)
                {
                    // a janela ja pode ter sido destruida
                }

                Plugin.Log.LogError("RSTV: falha ao abrir a skill tree: " + e);
            }
        }

        /// <summary>
        /// Referencia de z-order por contexto: na tela de party e o proprio `CharacterChoiceManager`
        /// (comportamento antigo, inalterado); na run e o HUD (`CurrentCharacterUI`) — a arvore e outro
        /// ramo da hierarquia do canvas e pode ter sido autorada ANTES dele. Desligavel por config
        /// (`AjustarZOrder`) porque mexer em indice de irmao e a unica parte que pode reordenar o
        /// tooltip do jogo em relacao a arvore — o log diz o que foi feito.
        /// </summary>
        private static Transform ZOrderReference(ReadOnlyContext context)
        {
            try
            {
                if (context == ReadOnlyContext.PartyScreen)
                {
                    return CharacterChoiceManager.Instance != null
                        ? CharacterChoiceManager.Instance.transform
                        : null;
                }

                if (!Plugin.AjustarZOrder)
                {
                    Plugin.Log.LogInfo("RSTV-5: AjustarZOrder=false no config — a arvore da run fica no " +
                                       "indice de irmao em que o prefab a posicionou.");
                    return null;
                }

                CurrentCharacterUI hud = CurrentCharacterUI.Instance;
                return hud != null ? hud.transform : null;
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV: nao deu para resolver a referencia de z-order: " + e.Message);
                return null;
            }
        }
    }

    /// <summary>
    /// Sessao de somente leitura. `Active` e o sinal consultado pelos patches (bloqueio do clique
    /// na arvore, higienizacao do commit e esconderijo do RespecButton).
    /// </summary>
    internal static class ReadOnlySession
    {
        internal static bool Active { get; private set; }
        internal static Character Target { get; private set; }
        internal static ReadOnlyContext Context { get; private set; }

        private static Func<bool> _interceptor;
        private static Func<bool> _interceptorAnterior;
        private static bool _interceptorFotografado;

        // Blindagem 2: para devolver `GameLogic.CurrentlySelectedCharacter` ao valor de antes.
        private static Character _selectionAnterior;
        private static Character _selectionAlvo;

        private static float _nextIdleCheck;

        internal static void Begin(Character target, ReadOnlyContext context)
        {
            Active = true;
            Target = target;
            Context = context;
            Plugin.Log.LogInfo("RSTV: modo somente leitura ATIVO (contexto=" + context + ").");
        }

        internal static void End()
        {
            if (!Active)
            {
                return;
            }

            Active = false;
            RemoveCancelInterceptor();
            UnregisterAsOpenWindow();
            RestoreSelection();
            Target = null;
            ZOrder.Restore();
            Plugin.Log.LogInfo("RSTV: modo somente leitura encerrado (nada foi gravado no personagem).");
        }

        // -----------------------------------------------------------------------------------------
        // Blindagem 2 — devolver o personagem selecionado que o mod escreveu (se escreveu)
        // -----------------------------------------------------------------------------------------

        /// <summary>Guarda o valor ANTERIOR e o alvo que estamos escrevendo. Chamado SO no caminho de
        /// escrita (quando o jogo nao tinha ninguem selecionado) — ver `SkillTreeReadOnly`.</summary>
        internal static void NoteSelectionToRestore(Character anterior, Character alvo)
        {
            _selectionAnterior = anterior;
            _selectionAlvo = alvo;
        }

        /// <summary>
        /// Devolve `GameLogic.CurrentlySelectedCharacter` ao valor de antes, no mesmo padrao do proprio
        /// jogo (`RoguelikeManager` guarda `storedCurrentlySelectedCharacter` em l.163711 e devolve em
        /// l.163942-163945). Idempotente: so age uma vez por escrita.
        ///
        /// Seguranca: so devolve se o jogo AINDA estiver no nosso alvo — se o jogador trocou de
        /// personagem no meio, quem manda e o jogador (nunca sobrescrever a escolha dele).
        /// </summary>
        internal static void RestoreSelection()
        {
            Character alvo = _selectionAlvo;
            if (alvo == null)
            {
                return;
            }

            _selectionAlvo = null;
            try
            {
                GameLogic gl = GameLogic.instance;
                if (gl == null)
                {
                    return;
                }

                if (gl.CurrentlySelectedCharacter != alvo)
                {
                    Plugin.Log.LogInfo("RSTV-5: personagem selecionado mudou depois da abertura — nao " +
                                       "devolvo o valor anterior (a escolha do jogador manda).");
                    return;
                }

                gl.CurrentlySelectedCharacter = _selectionAnterior;
                Plugin.Log.LogInfo("RSTV-5: personagem selecionado devolvido ao valor de antes da abertura (" +
                                   (_selectionAnterior != null ? _selectionAnterior.CharacterName : "nenhum") + ").");
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha ao devolver o personagem selecionado: " + e.Message);
            }
            finally
            {
                _selectionAnterior = null;
            }
        }

        // -----------------------------------------------------------------------------------------
        // Blindagem 3 — o slot UNICO de CancelInterceptor
        // -----------------------------------------------------------------------------------------

        /// <summary>
        /// Fotografa quem tinha o slot ANTES de a gente abrir a janela (o `OnEnable` do SkillTreeManager
        /// instala o interceptor dele no `SetActive(true)`, l.172890; o `InventoryManager` e o
        /// `CharacterMenusManager` disputam o mesmo slot, l.125301 e l.172890).
        /// </summary>
        internal static void CaptureInterceptorOwner()
        {
            try
            {
                _interceptorAnterior = UIWindowManager.CancelInterceptor;
                _interceptorFotografado = true;
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV: nao deu para fotografar o CancelInterceptor anterior: " + e.Message);
                _interceptorAnterior = null;
                _interceptorFotografado = false;
            }
        }

        /// <summary>
        /// Enquanto a janela nativa esta aberta, Esc/B (`UIWindowManager.Update`, l.216020) fecharia a
        /// tela que esta ATRAS da arvore, deixando a arvore orfa. Este interceptor consome o cancel e
        /// fecha a arvore.
        /// </summary>
        internal static void InstallCancelInterceptor()
        {
            try
            {
                if (!_interceptorFotografado)
                {
                    // sem fotografia (nao passou pelo CaptureInterceptorOwner): fotografa agora, para
                    // nunca sobrescrever um slot alheio com "null"
                    CaptureInterceptorOwner();
                }

                _interceptor = OnCancelPressed;
                UIWindowManager.CancelInterceptor = _interceptor;

                if (_interceptorAnterior != null)
                {
                    Plugin.Log.LogInfo("RSTV-5: o slot unico de CancelInterceptor estava ocupado — o " +
                                       "delegate anterior foi guardado e sera DEVOLVIDO no fechamento " +
                                       "(nao deixamos mais `null` no lugar dele).");
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha ao instalar o interceptor de Esc: " + e.Message);
            }
        }

        internal static void RemoveCancelInterceptor()
        {
            try
            {
                if (_interceptor != null && UIWindowManager.CancelInterceptor == _interceptor)
                {
                    // BLINDAGEM 3: DEVOLVE o delegate anterior em vez de `null`. Devolvendo o do proprio
                    // SkillTreeManager, o `OnDisable` dele (l.172899) ainda reconhece o slot como seu e
                    // faz a limpeza normal — o slot nao fica preso nem fica com um interceptor morto.
                    UIWindowManager.CancelInterceptor = _interceptorAnterior;
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV: falha ao remover o interceptor de Esc: " + e.Message);
            }
            finally
            {
                _interceptor = null;
                _interceptorAnterior = null;
                _interceptorFotografado = false;
            }
        }

        // -----------------------------------------------------------------------------------------
        // Blindagem 5 (camada 1) — a janela registrada no OpenedWindows do jogo
        // -----------------------------------------------------------------------------------------

        /// <summary>
        /// Entra na MESMA lista que o jogo usa (`UIWindowManager.OpenedWindows`, l.215980): com ela
        /// nao-vazia, `GUIManager.InMenus` (l.118297) e true e `PlayerMovement.ProcessUpdateInputs`
        /// (l.152986) retorna antes do clique do hex. Fazemos a insercao a mao (e nao `OpenWindow()`)
        /// de proposito: `OpenWindow` respeita `UIWindow_Ignore` e dispara `OnCloseEvent` no fechamento
        /// (l.215951/215961), coisas do prefab que este mod nao controla.
        /// </summary>
        internal static void RegisterAsOpenWindow(SkillTreeManager instance)
        {
            try
            {
                UIWindowManager wm = UIWindowManager.Instance;
                if (wm == null || instance == null)
                {
                    Plugin.Log.LogWarning("RSTV-5: UIWindowManager (ou a janela) ausente — a janela NAO " +
                                          "foi registrada em OpenedWindows; o prefixo do clique do hex " +
                                          "continua segurando a camada 2.");
                    return;
                }

                List<UIWindow> lista = wm.OpenedWindows;
                if (lista == null || lista.Contains(instance))
                {
                    return;
                }

                lista.Add(instance);
                if (PauseMenu.instance != null)
                {
                    PauseMenu.instance.UpdateButtonStates();
                }

                Plugin.Log.LogInfo("RSTV-5: janela registrada em UIWindowManager.OpenedWindows — " +
                                   "GUIManager.InMenus=true, logo o clique do hex NAO chega ao " +
                                   "ProcessLeftMouseClick enquanto a arvore estiver aberta.");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-5: falha ao registrar a janela em OpenedWindows (" + e.Message +
                                      ") — seguindo com o prefixo do clique do hex (camada 2).");
            }
        }

        private static void UnregisterAsOpenWindow()
        {
            try
            {
                SkillTreeManager instance = LoadableUIWindow<SkillTreeManager>.Instance;
                UnregisterAsOpenWindow(instance);
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-5: falha ao tirar a janela de OpenedWindows: " + e.Message);
            }
        }

        private static void UnregisterAsOpenWindow(SkillTreeManager instance)
        {
            try
            {
                if (instance == null)
                {
                    return;
                }

                UIWindowManager wm = UIWindowManager.Instance;
                List<UIWindow> lista = wm != null ? wm.OpenedWindows : null;
                if (lista == null || !lista.Contains(instance))
                {
                    return;
                }

                lista.Remove(instance);
                if (PauseMenu.instance != null)
                {
                    PauseMenu.instance.UpdateButtonStates();
                }

                Plugin.Log.LogInfo("RSTV-5: janela retirada de UIWindowManager.OpenedWindows (input " +
                                   "de batalha devolvido ao jogo).");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-5: falha ao retirar a janela de OpenedWindows: " + e.Message);
            }
        }

        /// <summary>
        /// Rede de seguranca: se a sessao NAO esta ativa e a janela nao esta na tela, ela nao pode
        /// continuar em `OpenedWindows` (o jogo ficaria com "InMenus" para sempre, sem input de batalha).
        /// Uma checagem por segundo — `UIWindowManager.Instance` cai num `FindObjectOfType` quando nao
        /// existe, e isso nao pode rodar todo frame.
        /// </summary>
        internal static void CleanupIdleRegistration()
        {
            try
            {
                if (Time.realtimeSinceStartup < _nextIdleCheck)
                {
                    return;
                }

                _nextIdleCheck = Time.realtimeSinceStartup + 1f;

                SkillTreeManager instance = LoadableUIWindow<SkillTreeManager>.Instance;
                if (instance == null || instance.gameObject == null || instance.gameObject.activeSelf)
                {
                    return;
                }

                UIWindowManager wm = UIWindowManager.Instance;
                List<UIWindow> lista = wm != null ? wm.OpenedWindows : null;
                if (lista == null || !lista.Contains(instance))
                {
                    return;
                }

                Plugin.Log.LogWarning("RSTV-5: a janela estava em OpenedWindows sem sessao read-only — " +
                                      "retirando (senao o input de batalha ficaria morto).");
                UnregisterAsOpenWindow(instance);
            }
            catch (Exception)
            {
                // rede de seguranca: nunca derruba o Update do host
            }
        }

        internal static void Close()
        {
            SkillTreeManager instance = LoadableUIWindow<SkillTreeManager>.Instance;
            End();
            try
            {
                UnregisterAsOpenWindow(instance);

                if (instance != null)
                {
                    instance.SkillsToAdd.Clear();
                    instance.SkillsRemoved.Clear();
                    instance.gameObject.SetActive(false);
                }

                if (GUIManager.instance != null && GUIManager.instance.tooltip != null)
                {
                    GUIManager.instance.tooltip.HideTooltip();
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha ao fechar a skill tree read-only: " + e.Message);
            }
        }

        private static bool OnCancelPressed()
        {
            if (!Active)
            {
                return false;
            }

            try
            {
                if (!PodeConsumirEsc())
                {
                    return false;
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV: falha ao checar a janela do topo antes do Esc (" + e.Message +
                                      ") — fechando a arvore mesmo assim.");
            }

            Plugin.Log.LogInfo("RSTV-5: Esc/B consumido — fechando a skill tree read-only.");
            Close();
            return true;
        }

        /// <summary>
        /// BLINDAGEM 3 (parte 2): o Esc so e consumido se a janela do TOPO (`OpenedWindows`, l.215939
        /// e o mesmo criterio que o proprio jogo usa em l.172924) for a nossa ou a `CharacterMenusManager`
        /// (na campanha a arvore vive DENTRO dela). Com qualquer outra no topo (mochila, opcoes...), o
        /// mod devolve `false` e deixa quem esta por cima tratar o Esc — antes o mod sempre consumia.
        /// </summary>
        private static bool PodeConsumirEsc()
        {
            UIWindowManager wm = UIWindowManager.Instance;
            if (wm == null)
            {
                return true;
            }

            List<UIWindow> lista = wm.OpenedWindows;
            if (lista == null || lista.Count == 0)
            {
                return true;
            }

            UIWindow topo = lista[lista.Count - 1];
            if (topo == null)
            {
                return true;
            }

            SkillTreeManager nossa = LoadableUIWindow<SkillTreeManager>.Instance;
            if (nossa != null && topo == nossa)
            {
                return true;
            }

            if (topo == CharacterMenusManager.Instance)
            {
                return true;
            }

            // A tela Select Party tambem pode estar no topo no fluxo da tela de party (o jogo
            // registra essa tela em OpenedWindows) — nao roubar o Esc dela seria uma REGRESSAO.
            if (topo == CharacterChoiceManager.Instance)
            {
                return true;
            }

            Plugin.Log.LogInfo("RSTV-5: Esc NAO consumido — a janela do topo e '" + topo.GetType().Name +
                               "' (nao e a nossa, nem a CharacterMenusManager, nem a tela de party); " +
                               "quem tratar o Esc e ela.");
            return false;
        }
    }

    /// <summary>
    /// A janela nativa e instanciada sob `ReferenceLoader.SkillTreeManagerPlaceholder` (l.162628),
    /// que e outro ramo da hierarquia do canvas; a tela de party pode ter sido autorada DEPOIS dele.
    /// Sem reordenar, a arvore desenharia ATRAS do Select Party. Aqui so mexemos em indices de irmao
    /// (nunca em parentesco/ancoras, que mudaria o layout) e restauramos no fechamento.
    /// </summary>
    internal static class ZOrder
    {
        private static Transform _movedBranch;
        private static int _movedBranchOldIndex = -1;

        internal static void EnsureAbove(Transform above, Transform reference)
        {
            try
            {
                Restore();
                if (above == null || reference == null)
                {
                    return;
                }

                Transform common = CommonAncestor(above, reference);
                if (common == null)
                {
                    return;
                }

                Transform branchAbove = BranchUnder(common, above);
                Transform branchReference = BranchUnder(common, reference);
                if (branchAbove == null || branchReference == null)
                {
                    return;
                }

                if (branchAbove.GetSiblingIndex() < branchReference.GetSiblingIndex())
                {
                    _movedBranch = branchAbove;
                    _movedBranchOldIndex = branchAbove.GetSiblingIndex();
                    branchAbove.SetAsLastSibling();
                    Plugin.Log.LogInfo("RSTV-2: z-order — ramo '" + branchAbove.name + "' estava em " +
                                       _movedBranchOldIndex + " (atras de '" + branchReference.name +
                                       "', " + branchReference.GetSiblingIndex() + "); movido para o fim.");
                }

                if (above.parent == reference.parent && above.GetSiblingIndex() < reference.GetSiblingIndex())
                {
                    above.SetAsLastSibling();
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV: nao deu para garantir o z-order da arvore: " + e.Message);
            }
        }

        internal static void Restore()
        {
            try
            {
                if (_movedBranch != null && _movedBranchOldIndex >= 0)
                {
                    _movedBranch.SetSiblingIndex(_movedBranchOldIndex);
                }
            }
            catch (Exception)
            {
                // a cena pode ter sido descarregada; nada a restaurar
            }
            finally
            {
                _movedBranch = null;
                _movedBranchOldIndex = -1;
            }
        }

        private static Transform CommonAncestor(Transform a, Transform b)
        {
            HashSet<Transform> chain = new HashSet<Transform>();
            for (Transform t = a; t != null; t = t.parent)
            {
                chain.Add(t);
            }

            for (Transform t = b; t != null; t = t.parent)
            {
                if (chain.Contains(t))
                {
                    return t;
                }
            }

            return null;
        }

        private static Transform BranchUnder(Transform ancestor, Transform node)
        {
            Transform current = node;
            while (current != null && current.parent != ancestor)
            {
                current = current.parent;
            }

            return current;
        }
    }
}
