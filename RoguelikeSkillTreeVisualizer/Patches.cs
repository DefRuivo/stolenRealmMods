using System;
using System.Collections.Generic;
using Burst2Flame;
using HarmonyLib;
using UnityEngine;

namespace RoguelikeSkillTreeVisualizer
{
    // ---------------------------------------------------------------------------------------------
    // RSTV-29 (06/10, decisao do dono em jogo) — a tela Select Party deixou de ter botao
    //
    // Ate a RSTV-28 havia DOIS ganchos que existiam SO' para injetar o clone 'Skills' na tela Select
    // Party: `CharacterChoiceManager.OpenCharacterChoiceManager` (o ponto original da RSTV-2a) e
    // `CharacterChoiceManager.OpenWindow` (a reinjecao da RSTV-28, que cobria o caminho do 'Continue'
    // — `GUIManager.CurrentGuiState` -> `OpenWindow`, l.120035). O dono decidiu REMOVER aquela
    // superficie: o botao da tela de escolha de grupo nao existe mais e o `SelectPartyButton.cs` foi
    // apagado. Sem superficie para injetar, os dois ganchos nao tem o que fazer — mante-los so' para
    // garantir o `RstvHost` seria codigo morto anunciando uma feature que nao existe.
    //
    // O `RstvHost` continua sendo criado (de forma preguicosa, ja' com cena viva) pelos ganchos das
    // superficies que RESTAM — `CharacterMenusManager.OpenWindow` (aba do inventario),
    // `CurrentCharacterUI.InitSingleton` (HUD da run) e `RoguelikeSkillTreeRemovalWindow.Open` (modal
    // 'Remove Skill Trees') — e pelo `SkillTreeShortcut`; todos chamam `RstvHost.Ensure()`, que e'
    // idempotente.
    //
    // O que sobrou da tela Select Party no mod e' so' o `CharacterChoiceTogglePatch` (abaixo), que
    // alimenta o `PartyTargets` do ATALHO de teclado (RSTV-11a) — feature que NAO foi removida.
    // ---------------------------------------------------------------------------------------------

    // ---------------------------------------------------------------------------------------------
    // RSTV-2b — rastreio de "o ultimo personagem que EU adicionei a party"
    //
    // Ancora: `CharacterChoiceManager.ToggleSelectedCharacter(int)` (l.328850). Entrada na party:
    // `character.SelectedForBattle = true` + `ControllerPlayerId` (l.328895-328896); saida:
    // `SelectedForBattle = false` (l.328859). O jogo NAO guarda ordem de adicao (l.145277/145322),
    // entao a ordem e registrada AQUI. So personagens `Owned` entram (l.33151) — regra do README:
    // cada jogador usa os seus, e o que outro jogador adiciona nao muda o meu contexto.
    // ---------------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(CharacterChoiceManager), nameof(CharacterChoiceManager.ToggleSelectedCharacter), new[] { typeof(int) })]
    internal static class CharacterChoiceTogglePatch
    {
        // O postfix roda depois do metodo original (o campo `selectedCharacterChoiceItem` ja mudou),
        // entao o personagem tocado e capturado no prefixo. Sem reentrancia: o metodo nao tem
        // await/coroutine.
        private static Character _subject;
        private static bool _firstCallLogged;

        [HarmonyPrefix]
        private static void Prefix(CharacterChoiceManager __instance)
        {
            try
            {
                _subject = __instance != null && __instance.selectedCharacterChoiceItem != null
                    ? __instance.selectedCharacterChoiceItem.Character
                    : null;
            }
            catch (Exception)
            {
                _subject = null;
            }
        }

        [HarmonyPostfix]
        private static void Postfix(CharacterChoiceManager __instance, int controllerPlayerId)
        {
            try
            {
                if (!_firstCallLogged)
                {
                    _firstCallLogged = true;
                    Plugin.Log.LogInfo("RSTV-2: gancho de adicao/remocao da party ATIVO (ToggleSelectedCharacter, controllerPlayerId=" +
                                       controllerPlayerId + ").");
                }

                Character subject = _subject;
                _subject = null;
                if (subject == null || !PartyTargets.IsLocal(subject))
                {
                    return;
                }

                if (subject.SelectedForBattle)
                {
                    PartyTargets.NoteAddition(subject);
                    Plugin.Log.LogInfo("RSTV-2: '" + subject.CharacterName + "' entrou na MINHA party — novo alvo do botao.");
                }
                else
                {
                    PartyTargets.NoteRemoval(subject);
                    Character next = PartyTargets.Resolve();
                    Plugin.Log.LogInfo("RSTV-2: '" + subject.CharacterName + "' saiu da minha party — alvo agora: " +
                                       (next != null ? next.CharacterName : "(nenhum)"));
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha no postfix de ToggleSelectedCharacter: " + e);
            }
        }
    }

    // ---------------------------------------------------------------------------------------------
    // RSTV-2d (1/4) — o caminho principal que persiste (o outro e `ResetSkillPoints`, 5/5 abaixo)
    //
    // `AcceptSkillChanges` (l.177650) e quem escreve no personagem (RemoveSkills/AddSkills,
    // l.177681-177682) e tambem quem FECHA a janela (SetActive(false), l.177686-177689) + toca o som.
    // Por isso NAO se usa Prefix devolvendo false: isso deixaria a janela presa. O prefixo devolve
    // o estado interno ao snapshot do personagem ANTES do original rodar — assim o original calcula
    // uma lista de remocao VAZIA e nao encontra nada para adicionar, executando so o fechamento.
    //
    // RSTV-5 / INDETERMINADO da RSTV-3 (CONFIRMADO lendo o prefab): o X (`closeButton`) e o `Accept
    // Button` do `Skill Tree Window` (path_id 490739) sao UnityEvent serializados que chamam ESTE
    // metodo — `AcceptSkillChanges(closeMenu: true)` (m_Mode=Bool / m_BoolArgument=1, lidos do raw
    // dos MonoBehaviour 2763658 e 2641390). A string `CloseSkillTreeMenu` NAO existe em nenhum asset
    // do jogo, entao o X NAO passa por `CharacterMenusManager.Instance` (sem NRE por instancia nula).
    // Prova: `docs/cobertura/revisao/RSTV-5-confirmacao-prefab.md`.
    // ---------------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(SkillTreeManager), nameof(SkillTreeManager.AcceptSkillChanges), new[] { typeof(bool) })]
    internal static class SkillTreeManagerAcceptSkillChangesPatch
    {
        // Devolve bool (e nao void) por causa do caminho de FALHA: se a higienizacao nao puder ser
        // feita, nao da para deixar o original rodar com o estado real (isso seria o unico caminho
        // capaz de gravar). Nesse caso a janela e fechada por aqui e o original nao roda: zero
        // escrita, e o log diz que foi o mod quem fechou.
        [HarmonyPrefix]
        private static bool Prefix(SkillTreeManager __instance, bool closeMenu)
        {
            try
            {
                if (!ReadOnlySession.Active || __instance == null)
                {
                    return true;
                }

                // Na criacao de personagem o original desvia para PresetManager.RefreshChosenSkills:
                // nao mexer nesse caminho (a nossa sessao nunca e aberta nesse estado).
                if (GUIManager.instance != null && GUIManager.instance.CurrentGuiState == GUIState.CreatingCharacter)
                {
                    return true;
                }

                Character target = ReadOnlySession.Target;
                __instance.SkillsToAdd.Clear();
                __instance.SkillsRemoved.Clear();

                // `AcceptSkillChanges` calcula o que remover como
                // `GameLogic.CurrentlySelectedCharacter.SkillsFromPoints` MENOS `SkillsOnEnter`
                // (l.177674-177681) e depois adiciona `SkillsToAdd`. Aqui `SkillsOnEnter` vira a UNIAO
                // das skills do alvo com as do personagem que o jogo tem como selecionado — assim a
                // lista de remocao fica vazia e nada e adicionado, seja qual for o personagem que o
                // jogo use nessa conta. Garantia: zero escrita, em qualquer estado.
                __instance.SkillsOnEnter.Clear();
                HashSet<SkillInfo> union = new HashSet<SkillInfo>();
                if (target != null)
                {
                    union.UnionWith(target.SkillsFromPoints);
                }

                Character gameSelected = GameLogic.instance != null ? GameLogic.instance.CurrentlySelectedCharacter : null;
                if (gameSelected != null && gameSelected != target)
                {
                    union.UnionWith(gameSelected.SkillsFromPoints);
                }

                __instance.SkillsOnEnter.AddRange(union);

                Plugin.Log.LogInfo("RSTV-2: commit higienizado (read-only, closeMenu=" + closeMenu +
                                   ") — nenhuma escrita no personagem (" + union.Count + " skills no snapshot).");
                return true;
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha ao higienizar AcceptSkillChanges — o original NAO vai rodar " +
                                    "(zero escrita); fechando a janela para nao prender a UI: " + e);

                try
                {
                    ReadOnlySession.Close();
                }
                catch (Exception fechamento)
                {
                    Plugin.Log.LogError("RSTV: e o fechamento de emergencia tambem falhou: " + fechamento.Message);
                }

                return false;
            }
        }
    }

    // ---------------------------------------------------------------------------------------------
    // RSTV-2d (2/5) — rede de seguranca do estado interno
    //
    // `Initialize` (l.177536) e publico e o jogo pode chama-lo de novo se
    // `GameLogic.CurrentlySelectedCharacter` mudar com a arvore aberta (l.110071-110073), o que
    // trocaria o contexto exibido e o numero de pontos. Com a sessao ativa, reafirmamos o snapshot
    // do personagem alvo e 0 pontos (o gate do clique e `CanLevel`, l.444990).
    // ---------------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(SkillTreeManager), nameof(SkillTreeManager.Initialize), new[] { typeof(List<SkillInfo>), typeof(int), typeof(bool) })]
    internal static class SkillTreeManagerInitializePatch
    {
        [HarmonyPostfix]
        private static void Postfix(SkillTreeManager __instance, bool creating)
        {
            try
            {
                if (!ReadOnlySession.Active || __instance == null || creating)
                {
                    return;
                }

                Character target = ReadOnlySession.Target;
                if (target == null)
                {
                    return;
                }

                bool changed = __instance.startingUnspentPoints != 0 ||
                               __instance.SkillsToAdd.Count > 0 ||
                               __instance.SkillsRemoved.Count > 0 ||
                               __instance.SkillsOnEnter.Count != target.SkillsFromPoints.Count;

                __instance.SkillsToAdd.Clear();
                __instance.SkillsRemoved.Clear();
                __instance.SkillsOnEnter.Clear();
                __instance.SkillsOnEnter.AddRange(target.SkillsFromPoints);
                __instance.startingUnspentPoints = 0;
                __instance.RefreshRespecFooter();

                if (changed)
                {
                    __instance.UpdateCurrentTree();
                    Plugin.Log.LogInfo("RSTV-2: estado interno reafirmado (read-only) depois de um Initialize do jogo.");
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha ao reafirmar o modo somente leitura — fechando a arvore " +
                                    "para nao deixar uma janela interativa em estado desconhecido: " + e);

                try
                {
                    ReadOnlySession.Close();
                }
                catch (Exception fechamento)
                {
                    Plugin.Log.LogError("RSTV: e o fechamento de emergencia tambem falhou: " + fechamento.Message);
                }
            }
        }
    }

    // ---------------------------------------------------------------------------------------------
    // RSTV-2d (3/5) — tirar o UNICO gate de escrita que ja existe no jogo
    //
    // `RespecButton.SetActive(active)` (l.178023) e o gate de permissao de escrita pronto do jogo
    // (active = !creatingMode && character != null && AllMyCharacters.Contains(character),
    // l.177980). Sem ele nao ha como entrar em `BeginRespec` (l.177819), que e o que habilita
    // desaprender (`UnlearnCommittedSkill`).
    // ---------------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(SkillTreeManager), nameof(SkillTreeManager.RefreshRespecFooter), new Type[0])]
    internal static class SkillTreeManagerRespecFooterPatch
    {
        [HarmonyPostfix]
        private static void Postfix(SkillTreeManager __instance)
        {
            try
            {
                if (ReadOnlySession.Active && __instance != null && __instance.RespecButton != null &&
                    __instance.RespecButton.activeSelf)
                {
                    __instance.RespecButton.SetActive(false);
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha ao esconder o RespecButton: " + e);
            }
        }
    }

    // ---------------------------------------------------------------------------------------------
    // RSTV-2d (4/5) — clique no no da arvore
    //
    // `SkillTreeItem.ToggleAddToSkillToAddList()` (l.177123) e a UNICA via de clique (compra,
    // descompra, desaprender). Em read-only o clique e bloqueado por inteiro; hover, zoom, abas e
    // tooltips (l.176936 / l.177148) continuam funcionando. Com `unspentPoints = 0` o proprio
    // `CanLevel` (l.444990) ja negaria a compra — este prefixo e a garantia extra.
    // ---------------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(SkillTreeItem), nameof(SkillTreeItem.ToggleAddToSkillToAddList), new Type[0])]
    internal static class SkillTreeItemTogglePatch
    {
        private static bool _firstBlockLogged;

        [HarmonyPrefix]
        private static bool Prefix(SkillTreeItem __instance)
        {
            // RSTV-16: o read-only NAO e mais "automatico pela guarda de null do SkillTreeItem" — a
            // `SkillTreeManager` e PRE-CARREGADA (l.136586-136596) e `Instance` NAO e nulo. Quem barra
            // e a SESSAO (`ReadOnlySession.Active`, mantida viva enquanto a aba esta visivel) e o
            // estado da propria aba (`SkillTreesTab.Aberto`). A higienizacao do `AcceptSkillChanges`
            // continua sendo a segunda camada.
            bool readOnly;
            try
            {
                readOnly = ReadOnlySession.Active || SkillTreesTab.Aberto;
            }
            catch (Exception)
            {
                // Sem saber se a sessao esta ativa, o seguro e DEIXAR o jogo agir (a higienizacao do
                // AcceptSkillChanges continua sendo a garantia de que nada e gravado).
                return true;
            }

            if (!readOnly)
            {
                return true;
            }

            // O bloqueio NAO depende do log: o `return false` fica FORA do try, senao uma falha ao
            // montar a mensagem deixaria o clique passar em pleno modo somente leitura.
            try
            {
                if (!_firstBlockLogged)
                {
                    _firstBlockLogged = true;
                    string name = __instance != null && __instance.SkillInfo != null
                        ? __instance.SkillInfo.SkillName
                        : "?";
                    Plugin.Log.LogInfo("RSTV-2: clique na arvore BLOQUEADO (read-only) — primeira skill clicada: " +
                                       name + ".");
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV: nao deu para logar o bloqueio do clique (o clique continua bloqueado): " +
                                      e.Message);
            }

            return false;
        }
    }

    // ---------------------------------------------------------------------------------------------
    // RSTV-2d (5/5) — o OUTRO caminho que persiste, e o unico que NAO passa por AcceptSkillChanges
    //
    // `ResetSkillPoints()` (l.178430) e publico, sem parametro e sem guarda nenhuma (nem
    // `creatingMode`, nem `InRespecMode`): e o candidato natural ao `resetButton` serializado
    // (l.177213, ao lado de `acceptButton`/`closeButton`, cujo onClick tambem so existe no prefab).
    // Ele chama `Character.ResetSkills()`, que ZERA `SavedMap[...]` de TODAS as skills do
    // personagem e ENFILEIRA o save dele (l.38366-38372) — nao passa pelo `AcceptSkillChanges`,
    // entao a higienizacao de la nao cobriria esse clique. Em read-only ele e bloqueado aqui.
    // Fechar a janela NAO passa por este metodo (ver `OnDisable`, l.178053), entao bloquear nao
    // prende a UI.
    // ---------------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(SkillTreeManager), nameof(SkillTreeManager.ResetSkillPoints), new Type[0])]
    internal static class SkillTreeManagerResetSkillPointsPatch
    {
        private static bool _firstBlockLogged;

        [HarmonyPrefix]
        private static bool Prefix()
        {
            try
            {
                if (!ReadOnlySession.Active)
                {
                    return true;
                }

                if (!_firstBlockLogged)
                {
                    _firstBlockLogged = true;
                    Plugin.Log.LogInfo("RSTV-2: ResetSkillPoints BLOQUEADO (read-only) — nada foi zerado no personagem.");
                }
            }
            catch (Exception e)
            {
                // SEGURANCA — o lado seguro aqui e MANTER o bloqueio (nunca liberar o original).
                // `ResetSkillPoints()` ZERA o SavedMap de TODAS as skills do personagem e
                // ENFILEIRA o save dele (l.38366-38372): e irreversivel. Se nao der para saber se
                // a sessao e read-only (a leitura de `ReadOnlySession.Active` lancou), rodar o
                // original poderia apagar a arvore durante uma VISUALIZACAO — perda grande e sem
                // volta. Bloqueando, o pior caso e o jogador nao resetar os pontos nesta chamada,
                // que e perda pequena e reversivel. Por isso a excecao NUNCA devolve true.
                Plugin.Log.LogError("RSTV: falha ao avaliar o bloqueio de ResetSkillPoints — " +
                                    "mantendo o reset BLOQUEADO por seguranca: " + e);
                return false;
            }

            return false;
        }
    }

    // ---------------------------------------------------------------------------------------------
    // RSTV-16 — a injecao/reinjecao da aba "All Skill Trees" no inventario
    //
    // Ancora: `CharacterMenusManager.OpenWindow()` (override l.49371-49375 — chamado pelo proprio jogo
    // sempre que o menu de personagem abre; e o `base.OpenWindow()` + `OpenMenuManager()` que ligam o
    // menu-pai). O `Ensure` e IDEMPOTENTE por nome: se a aba ja esta no array publico `MenuTabs` (ou
    // como filho da barra), e no-op. NAO se usa o `Initialize()` do MenuTabManager aqui: ele dispara
    // `SelectFirstActiveButton` (l.140669) e trocaria a aba selecionada.
    // ---------------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(CharacterMenusManager), nameof(CharacterMenusManager.OpenWindow), new Type[0])]
    internal static class CharacterMenusManagerOpenWindowPatch
    {
        private static bool _firstCallLogged;

        [HarmonyPostfix]
        private static void Postfix(CharacterMenusManager __instance)
        {
            try
            {
                if (!_firstCallLogged)
                {
                    _firstCallLogged = true;
                    Plugin.Log.LogInfo("RSTV-16: gancho da aba do inventario ATIVO (CharacterMenusManager.OpenWindow).");
                }

                RstvHost.Ensure();
                SkillTreesTab.Ensure(__instance);
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV-16: falha no postfix de CharacterMenusManager.OpenWindow: " + e);
            }
        }
    }

    // ---------------------------------------------------------------------------------------------
    // Fechamento da janela nativa da CAMPANHA (botao fechar, Esc, troca de personagem).
    // `OnDisable` roda no `SetActive(false)` que o proprio `AcceptSkillChanges` faz (l.177689): e o
    // sinal de que a sessao read-only acabou quando a arvore de campanha sai de cena.
    // ---------------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(SkillTreeManager), "OnDisable", new Type[0])]
    internal static class SkillTreeManagerOnDisablePatch
    {
        [HarmonyPostfix]
        private static void Postfix(SkillTreeManager __instance)
        {
            try
            {
                if (ReadOnlySession.Active)
                {
                    ReadOnlySession.End();
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha no postfix de OnDisable: " + e);
            }
        }
    }

    // ---------------------------------------------------------------------------------------------
    // RSTV-15 — o fechamento da arvore do ROGUELIKE (o sinal do ciclo de vida)
    //
    // A `SkillTreeManagerRoguelike` (l.178449) NAO tem `OnDisable` proprio — quem a DESLIGA e
    // `CharacterMenusManager.CloseSkillTreeMenu()` (l.49264, `SetActive(false)` em l.49272). O
    // `CloseSkillTreeMenu` e chamado por `CloseMenuManager` (l.49364, o caminho do Esc/aba/CloseWindow)
    // e por `OpenCharacterMenu`/`OpenFortuneMenu` (l.49160/49307): em TODOS eles a nossa janela sai de
    // cena. E o sinal EXATO de que a sessao read-only acabou — sem ele, o `Tick` so descobriria o
    // fechamento pela rede de seguranca (tolerancia de 8 s), deixando o modo read-only preso.
    //
    // NAO e um metodo de ABERTURA: `OpenSkillTreeMenu` (l.49217) fecha inventario/fortuna
    // (`CloseCharacterMenu`/`CloseFortuneMenu`, l.49228-49229), NUNCA a arvore — abrir a arvore nao
    // passa por aqui.
    // ---------------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(CharacterMenusManager), nameof(CharacterMenusManager.CloseSkillTreeMenu), new Type[0])]
    internal static class CharacterMenusManagerCloseSkillTreePatch
    {
        [HarmonyPostfix]
        private static void Postfix()
        {
            try
            {
                if (ReadOnlySession.Active)
                {
                    ReadOnlySession.End();
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha no postfix de CharacterMenusManager.CloseSkillTreeMenu: " + e);
            }
        }
    }

    // ---------------------------------------------------------------------------------------------
    // RSTV-5 (1/3) — injecao do botao no HUD da run
    //
    // Ancora: `CurrentCharacterUI.InitSingleton()` (l.330051, PUBLICO e chamado pelo proprio jogo
    // assim que o prefab do HUD e instanciado — l.136635 e l.136923: `CurrentCharacterUI.Instance =
    // ...GetComponent<CurrentCharacterUI>(); CurrentCharacterUI.Instance.InitSingleton();`). E
    // idempotente por instancia (o botao so e criado uma vez por HUD).
    //
    // NAO usar o `Update()`/`UIUpdate()` do HUD (l.330080): roda todo frame e mexe em
    // `endTurnButton` (l.330186) e `fleeBattleButton` (l.330183). Quem chama `RunButton.Mirror()` e o
    // `RstvHost.Update` do mod.
    // ---------------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(CurrentCharacterUI), nameof(CurrentCharacterUI.InitSingleton), new Type[0])]
    internal static class CurrentCharacterUIInitPatch
    {
        private static bool _firstCallLogged;

        [HarmonyPostfix]
        private static void Postfix(CurrentCharacterUI __instance)
        {
            try
            {
                if (!_firstCallLogged)
                {
                    _firstCallLogged = true;
                    Plugin.Log.LogInfo("RSTV-5: gancho do HUD da run ATIVO (CurrentCharacterUI.InitSingleton).");
                }

                RstvHost.Ensure();
                RunButton.Ensure(__instance);
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha no postfix de CurrentCharacterUI.InitSingleton: " + e);
            }
        }
    }

    // ---------------------------------------------------------------------------------------------
    // RSTV-5 (2/3 / blindagem 5) — o clique do hex no branch de ACAO nao checa PointerOverUIObject
    //
    // `PlayerMovement.ProcessLeftMouseClick(HexCell)` (l.158281) e o caminho do clique no hex (chamado
    // de `ProcessUpdateInputs`, l.158003, que so checa `GUIManager.InMenus`). O branch de MOVIMENTO
    // respeita `PointerOverUIObject` (l.158288), mas o de ACAO NAO: l.158397-158400 so chama
    // `ExecuteAction(cell, CurrentAction)`. Com a arvore aberta, um clique que atravessasse a janela
    // executaria a acao. O prefixo abaixo consome o clique enquanto a sessao read-only esta ativa.
    //
    // NAO e metodo de FECHAMENTO (bloquear fechamento prenderia a janela) e NAO e o unico guarda: a
    // camada 1 e a janela registrada em `UIWindowManager.OpenedWindows` (=> `GUIManager.InMenus`).
    // ---------------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(PlayerMovement), "ProcessLeftMouseClick", new[] { typeof(HexCell) })]
    internal static class PlayerMovementProcessLeftMouseClickPatch
    {
        private static bool _firstBlockLogged;

        [HarmonyPrefix]
        private static bool Prefix()
        {
            try
            {
                if (!ReadOnlySession.Active)
                {
                    return true;
                }

                if (!_firstBlockLogged)
                {
                    _firstBlockLogged = true;
                    Plugin.Log.LogInfo("RSTV-5: clique no hex CONSUMIDO enquanto a arvore read-only esta " +
                                       "aberta (o branch de Action NAO checa PointerOverUIObject).");
                }
            }
            catch (Exception e)
            {
                // LADO SEGURO ESCOLHIDO: DEIXAR O JOGO AGIR. A leitura de `ReadOnlySession.Active` e um
                // campo estatico (nao pode falhar de verdade); se ela falhasse e este prefixo devolvesse
                // false, o clique do hex MORRERIA PARA SEMPRE (sem sessao nenhuma aberta, sem nada para
                // fechar) — e so reiniciando o jogo. Executar uma acao, no pior caso, e reversivel; um
                // input morto permanentemente nao e. Por isso aqui a excecao devolve true.
                Plugin.Log.LogError("RSTV: falha ao avaliar o bloqueio do clique do hex — deixando o " +
                                    "jogo tratar o clique: " + e);
                return true;
            }

            return false;
        }
    }

    // ---------------------------------------------------------------------------------------------
    // RSTV-11a (PARTE 1) — o ATALHO de teclado (proposta D)
    //
    // Ancora: `KeybindManager.Update` (l.133297 — PRIVADO e SEM parametro; a assinatura e declarada
    // por TIPO com array vazio, como os outros ganchos por nome). O POSTFIX roda INCLUSIVE nos
    // `return` cedo do jogo (l.133335 desabilitado/remap, l.133374 foco de texto/EventWindow, l.133449
    // janela de UI aberta) — por ISSO quem decide se a tecla pode agir e o handler
    // (`SkillTreeShortcut`), que replica esses guards; aqui nao ha guarda nenhuma de proposito, o
    // gancho e so a borda.
    //
    // NAO confundir com a acao 10 nativa: `VirtualInput.GetButtonDownAndSwitchToPlayerCharacter(10)`
    // (l.133500) chama `CharacterMenusManager.ToggleSkillTreeMenu` e abriria a janela vanilla junto.
    // A tecla do mod e lida CRUA (`Input.GetKeyDown`), config no `Plugin` — padrao F10.
    // ---------------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(KeybindManager), "Update", new Type[0])]
    internal static class KeybindManagerUpdatePatch
    {
        [HarmonyPostfix]
        private static void Postfix(KeybindManager __instance)
        {
            try
            {
                SkillTreeShortcut.Handle(__instance);
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha no gancho do atalho (KeybindManager.Update): " + e);
            }
        }
    }

    // ---------------------------------------------------------------------------------------------
    // RSTV-11b — o botao DENTRO da janela do level-up (proposta C)
    //
    // Ancora: `RoguelikeManager.OpenSkillSelectWindow(CharacterLevelUpInfo, bool)` (l.168921, PUBLICO)
    // — o metodo que MONTA e LIGA a janela do level-up (`SkillSelectWindow.SetActive(true)`,
    // l.168941). Ele roda uma vez por abertura da janela, inclusive a cada personagem da fila
    // (`ConfirmLevelUpSelection`, l.168998, reabre para `CharactersWaitingForLevelUp[0]`) sobre o
    // MESMO `SkillSelectWindow`. Por isso o `Ensure` e IDEMPOTENTE POR JANELA: a 2a chamada e no-op.
    //
    // O botao e filho DIRETO do `SkillSelectWindow` [680553] e NAO de `Content` [680573]: o Content
    // tem `VerticalLayoutGroup` + `ContentSizeFitter`, e um filho ali reflui o painel inteiro
    // (RSTV-10, secao 4). O `SkillSelectWindow` nao tem LayoutGroup.
    // ---------------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(RoguelikeManager), nameof(RoguelikeManager.OpenSkillSelectWindow), new[] { typeof(CharacterLevelUpInfo), typeof(bool) })]
    internal static class RoguelikeManagerOpenSkillSelectWindowPatch
    {
        private static bool _firstCallLogged;

        [HarmonyPostfix]
        private static void Postfix(RoguelikeManager __instance)
        {
            try
            {
                if (!_firstCallLogged)
                {
                    _firstCallLogged = true;
                    Plugin.Log.LogInfo("RSTV-11b: gancho da janela do level-up ATIVO (RoguelikeManager.OpenSkillSelectWindow).");
                }

                LevelUpWindowButton.Ensure(__instance);
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha no postfix de OpenSkillSelectWindow: " + e);
            }
        }
    }

    // ---------------------------------------------------------------------------------------------
    // RSTV-20 — o botao no CABECALHO do modal "Remove Skill Trees"
    //
    // Ancora: `RoguelikeSkillTreeRemovalWindow.Open(Character)` (l.170723, PUBLICO) — o metodo que o
    // jogo chama a cada abertura do modal (`CharacterChoiceManager.OpenSkillTreeRemovalWindow`,
    // l.328674, e o `CharacterChoiceItem`, l.328374). Ele roda de novo a cada re-abertura sobre a
    // MESMA janela; por isso `RemovalWindowSkillsButton.Ensure` e IDEMPOTENTE por instancia (acha o
    // clone por NOME e so reafirma rotulo/estado — nunca cria um segundo botao).
    //
    // NAO usar o `Update()` privado do modal (l.170686, roda todo quadro e mexe no Style/portrait):
    // o gancho de abertura e o `Open`, e o alvo e lido do `CurrentCharacter` na hora do clique.
    //
    // Assinatura declarada por TIPO + `nameof` (nunca por indice `__N`), como os outros ganchos.
    // ---------------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(RoguelikeSkillTreeRemovalWindow), nameof(RoguelikeSkillTreeRemovalWindow.Open), new[] { typeof(Character) })]
    internal static class RoguelikeSkillTreeRemovalWindowOpenPatch
    {
        private static bool _firstCallLogged;

        [HarmonyPostfix]
        private static void Postfix(RoguelikeSkillTreeRemovalWindow __instance)
        {
            try
            {
                if (!_firstCallLogged)
                {
                    _firstCallLogged = true;
                    Plugin.Log.LogInfo("RSTV-20: gancho do modal 'Remove Skill Trees' ATIVO " +
                                       "(RoguelikeSkillTreeRemovalWindow.Open).");
                }

                RstvHost.Ensure();
                RemovalWindowSkillsButton.Ensure(__instance);
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha no postfix de RoguelikeSkillTreeRemovalWindow.Open: " + e);
            }
        }
    }

    // ---------------------------------------------------------------------------------------------
    // RSTV-27 — o RODAPE da tooltip (mana/cooldown/alcance/duracao) ainda lia o `TooltipCharacter`
    //
    // O DEFEITO (achado da verificacao do RSTV-26, 05/10): o conserto do RSTV-26 passa o personagem do
    // MODAL como ARGUMENTO do `ShowSkillTooltip`, e isso alimenta so' o CORPO da tooltip — o dano
    // (`GetDamageString`) e as expressoes (`ApplyDescriptionExpressions`). O RODAPE NAO usa esse
    // argumento: o metodo monta um local proprio, `tooltipCharacter = TooltipCharacter` (IL_0c46 na
    // `ShowSkillTooltip(SkillInfo, Character, bool, bool, bool)` da DLL real do jogo), e le' TODO o
    // rodape dele — `GetManaCost`, `GetActionCooldown`, `GetSimpleRange`, `GetSimpleBlastRange` e a
    // duracao (`Game.Eval` de `Duration` / `GroundDuration`). `Tooltip.TooltipCharacter` e' propriedade
    // GET-ONLY que devolve `GameLogic.CurrentlySelectedCharacter` — NULL na tela Party Select, onde
    // vive o modal "Remove Skill Trees" (a MESMA causa do '*0' da RSTV-26). Com ele null o rodape cai
    // nos overloads SEM personagem (`GetManaCost()`, ...) e a duracao em `Duration[0]` cru: numeros de
    // BASE, sem os modificadores do personagem que o jogador esta vendo.
    //
    // O CONSERTO: o hover do RSTV (`RstvSkillHover.OnPointerEnter`, SkillTreesTab.cs) passa o alvo do
    // modal TAMBEM a esses campos, por um estado explicito armado SO' em volta da montagem da tooltip
    // (`ComAlvo`/`SemAlvo`, em `try`/`finally`), e este POSTFIX do getter PREENCHE o valor quando — e
    // so' quando — o jogo devolve null. As tres regras do conserto:
    //   * o valor do JOGO vence: `__result != null` sai do gancho sem tocar em nada (no inventario,
    //     onde o jogo TEM personagem selecionado, nada muda — nenhuma regressao);
    //   * FALLBACK: sem alvo do modal armado, sai do gancho e o jogo segue exatamente como antes;
    //   * a troca vale SO' enquanto a NOSSA chamada esta armada: nenhuma outra tooltip do jogo passa a
    //     ler o personagem do modal.
    // O gancho e' FAIL-SAFE (try/catch): uma excecao aqui nao pode derrubar o hover.
    //
    // POR QUE UM GANCHO NO GETTER (e nao no chamador): a propriedade e' GET-ONLY e o `Tooltip` e' do
    // jogo (a `Assembly-CSharp` nao se modifica). O caminho do RSTV-26 (personagem como ARGUMENTO) nao
    // alcanca esse local. Precedente no repo: o RoguelikeDebugger ja' patcheia getters (`Game.get_Skills`
    // etc.) e o censo gerado em jogo prova que esses ganchos pegam.
    //
    // Assinatura por TIPO + nome do metodo do jogo (nunca por indice `__N`), como os outros ganchos.
    // ---------------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(Tooltip), "get_TooltipCharacter")]
    internal static class TooltipCharacterRodapePatch
    {
        /// <summary>
        /// O personagem do MODAL enquanto a tooltip do RSTV esta sendo montada. null fora dessa janela:
        /// e' o FALLBACK que mantem o comportamento do jogo quando nao ha alvo do modal.
        /// </summary>
        private static Character _alvoDoModal;

        private static bool _primeiroPreenchimentoLogado;

        /// <summary>Arma o alvo do modal para a montagem da tooltip do RSTV (RSTV-27).</summary>
        internal static void ComAlvo(Character alvo)
        {
            _alvoDoModal = alvo;
        }

        /// <summary>Desarma o alvo (fim da montagem): volta ao comportamento do jogo.</summary>
        internal static void SemAlvo()
        {
            _alvoDoModal = null;
        }

        [HarmonyPostfix]
        private static void Postfix(ref Character __result)
        {
            try
            {
                if (__result != null)
                {
                    // O valor do JOGO vence — o gancho so' PREENCHE um null (por isso e' postfix).
                    return;
                }

                Character alvo = _alvoDoModal;
                if (alvo == null)
                {
                    // FALLBACK: sem alvo do modal (fora da nossa tooltip) nada muda.
                    return;
                }

                __result = alvo;

                if (!_primeiroPreenchimentoLogado)
                {
                    _primeiroPreenchimentoLogado = true;
                    Plugin.Log.LogInfo("RSTV-27: rodape da tooltip resolvido pelo personagem do MODAL " +
                                       "(TooltipCharacter era null) — alvo=" +
                                       (alvo.CharacterName ?? "?") + ".");
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning("RSTV-27: falha no postfix de Tooltip.TooltipCharacter: " + e.Message);
            }
        }
    }
}
