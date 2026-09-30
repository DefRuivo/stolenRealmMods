using System;
using System.Collections.Generic;
using Burst2Flame;
using HarmonyLib;
using UnityEngine;

namespace RoguelikeSkillTreeVisualizer
{
    // ---------------------------------------------------------------------------------------------
    // RSTV-2a — injecao do botao
    //
    // Ancora: `CharacterChoiceManager.OpenCharacterChoiceManager()` (l.208278) — o gancho publico e
    // idempotente por abertura de tela (a tela e resetada antes por ResetCharacterChoice, l.208219).
    // NAO usar o `Update()` da tela (l.208231) como gancho: ele roda todo frame e ja mexe em
    // `acceptBtn` (l.208235) e `roguelikePowerupButton` (l.208236).
    //
    // Assinatura declarada por TIPO (array vazio = metodo sem parametros). Nunca por indice (__1/__2):
    // foi um `ref` amarrado no slot errado que derrubou o jogo com 112 NullReferenceException.
    // ---------------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(CharacterChoiceManager), nameof(CharacterChoiceManager.OpenCharacterChoiceManager), new Type[0])]
    internal static class CharacterChoiceOpenPatch
    {
        private static bool _firstCallLogged;

        [HarmonyPostfix]
        private static void Postfix(CharacterChoiceManager __instance)
        {
            try
            {
                if (!_firstCallLogged)
                {
                    _firstCallLogged = true;
                    Plugin.Log.LogInfo("RSTV-2: gancho da tela Select Party ATIVO (OpenCharacterChoiceManager).");
                }

                RstvHost.Ensure();
                SelectPartyButton.Ensure(__instance);
            }
            catch (Exception e)
            {
                Plugin.Log.LogError("RSTV: falha no postfix de OpenCharacterChoiceManager: " + e);
            }
        }
    }

    // ---------------------------------------------------------------------------------------------
    // RSTV-2b — rastreio de "o ultimo personagem que EU adicionei a party"
    //
    // Ancora: `CharacterChoiceManager.ToggleSelectedCharacter(int)` (l.208425). Entrada na party:
    // `character.SelectedForBattle = true` + `ControllerPlayerId` (l.208470-208471); saida:
    // `SelectedForBattle = false` (l.208434). O jogo NAO guarda ordem de adicao (l.140373/140418),
    // entao a ordem e registrada AQUI. So personagens `Owned` entram (l.32261) — regra do README:
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
    // `AcceptSkillChanges` (l.172494) e quem escreve no personagem (RemoveSkills/AddSkills,
    // l.172525-172526) e tambem quem FECHA a janela (SetActive(false), l.172533) + toca o som.
    // Por isso NAO se usa Prefix devolvendo false: isso deixaria a janela presa. O prefixo devolve
    // o estado interno ao snapshot do personagem ANTES do original rodar — assim o original calcula
    // uma lista de remocao VAZIA e nao encontra nada para adicionar, executando so o fechamento.
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
                // (l.172518-172525) e depois adiciona `SkillsToAdd`. Aqui `SkillsOnEnter` vira a UNIAO
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
    // `Initialize` (l.172380) e publico e o jogo pode chama-lo de novo se
    // `GameLogic.CurrentlySelectedCharacter` mudar com a arvore aberta (l.108162-108164), o que
    // trocaria o contexto exibido e o numero de pontos. Com a sessao ativa, reafirmamos o snapshot
    // do personagem alvo e 0 pontos (o gate do clique e `CanLevel`, l.322961).
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
    // `RespecButton.SetActive(active)` (l.172867) e o gate de permissao de escrita pronto do jogo
    // (active = !creatingMode && character != null && AllMyCharacters.Contains(character),
    // l.172824). Sem ele nao ha como entrar em `BeginRespec` (l.172663), que e o que habilita
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
    // `SkillTreeItem.ToggleAddToSkillToAddList()` (l.171967) e a UNICA via de clique (compra,
    // descompra, desaprender). Em read-only o clique e bloqueado por inteiro; hover, zoom, abas e
    // tooltips (l.171780 / l.171992) continuam funcionando. Com `unspentPoints = 0` o proprio
    // `CanLevel` (l.322961) ja negaria a compra — este prefixo e a garantia extra.
    // ---------------------------------------------------------------------------------------------
    [HarmonyPatch(typeof(SkillTreeItem), nameof(SkillTreeItem.ToggleAddToSkillToAddList), new Type[0])]
    internal static class SkillTreeItemTogglePatch
    {
        private static bool _firstBlockLogged;

        [HarmonyPrefix]
        private static bool Prefix(SkillTreeItem __instance)
        {
            bool readOnly;
            try
            {
                readOnly = ReadOnlySession.Active;
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
    // `ResetSkillPoints()` (l.173274) e publico, sem parametro e sem guarda nenhuma (nem
    // `creatingMode`, nem `InRespecMode`): e o candidato natural ao `resetButton` serializado
    // (l.172057, ao lado de `acceptButton`/`closeButton`, cujo onClick tambem so existe no prefab).
    // Ele chama `Character.ResetSkills()`, que ZERA `SavedMap[...]` de TODAS as skills do
    // personagem e ENFILEIRA o save dele (l.37474-37480) — nao passa pelo `AcceptSkillChanges`,
    // entao a higienizacao de la nao cobriria esse clique. Em read-only ele e bloqueado aqui.
    // Fechar a janela NAO passa por este metodo (ver `OnDisable`, l.172897), entao bloquear nao
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
                // ENFILEIRA o save dele (l.37474-37480): e irreversivel. Se nao der para saber se
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
    // Fechamento da janela nativa (botao fechar, Esc do interceptor, troca de personagem).
    // `OnDisable` roda no `SetActive(false)` que o proprio `AcceptSkillChanges` faz (l.172533): e o
    // sinal exato de que a sessao read-only acabou. `OnDisable` e privado — patch por nome.
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
    // RSTV-5 (1/3) — injecao do botao no HUD da run
    //
    // Ancora: `CurrentCharacterUI.InitSingleton()` (l.209626, PUBLICO e chamado pelo proprio jogo
    // assim que o prefab do HUD e instanciado — l.132940 e l.133228: `CurrentCharacterUI.Instance =
    // ...GetComponent<CurrentCharacterUI>(); CurrentCharacterUI.Instance.InitSingleton();`). E
    // idempotente por instancia (o botao so e criado uma vez por HUD).
    //
    // NAO usar o `Update()`/`UIUpdate()` do HUD (l.209655): roda todo frame e mexe em
    // `endTurnButton` (l.209761) e `fleeBattleButton` (l.209758). Quem chama `RunButton.Mirror()` e o
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
    // `PlayerMovement.ProcessLeftMouseClick(HexCell)` (l.153277) e o caminho do clique no hex (chamado
    // de `ProcessUpdateInputs`, l.153024, que so checa `GUIManager.InMenus`). O branch de MOVIMENTO
    // respeita `PointerOverUIObject` (l.153342), mas o de ACAO NAO: l.153393-153397 so chama
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
}
