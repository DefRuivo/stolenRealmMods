using System.Collections.Generic;
using System;
using HarmonyLib;

namespace FollowUpMod
{
    /// <summary>
    /// Adequa o nivel ANTES do toggle nativo comparar os niveis. Nao bloqueia nada: a
    /// aceitacao/recusa continua sendo a regra do jogo original (MaxLevelVariance).
    /// Atributo explicito (tipo + nome + assinatura): com apenas o tipo, o processor do
    /// Harmony nao encontra o alvo e "patch aplicado" passa a mentir.
    /// </summary>
    [HarmonyPatch(typeof(CharacterChoiceManager), "ToggleSelectedCharacter", new[] { typeof(int) })]
    internal static class SelectionGatePatch
    {
        [HarmonyPrefix]
        [HarmonyPriority(Priority.First)]
        private static void Prefix(CharacterChoiceManager __instance) => SelectionGate.Prepare(__instance);

        [HarmonyPostfix]
        private static void Postfix(CharacterChoiceManager __instance)
        {
            // Auto-cura: o prefixo promove para passar pela comparacao nativa. Se o personagem
            // NAO ficou selecionado (o jogador removeu, ou o jogo recusou por outro motivo),
            // o nivel volta ao original - sem isso, quem so passou pela tela ficava devendo
            // atributos/skills/itens de uma promocao que nao valeu.
            try
            {
                var c = __instance != null && __instance.selectedCharacterChoiceItem != null
                    ? __instance.selectedCharacterChoiceItem.Character
                    : null;
                if (c != null && !c.SelectedForBattle && SessionGuard.IsPromoted(c))
                {
                    int antes = (int)c.Level;
                    if (SessionGuard.RestoreOne(c))
                    {
                        int removidos = PromotionService.ClearPendingLevels(c);
                        PromotionService.Forget(c);
                        Diag.Write("fila de niveis limpa de " + c.CharacterName + ": " + removidos + " entrada(s)");
                        Diag.Write("desfez promocao de " + c.CharacterName + " (" + antes + "->" + c.Level + ")");
                        FollowUpModPlugin.Log.LogInfo("FU: " + c.CharacterName + " nao ficou na party; nivel " + antes + "->" + c.Level
                            + " desfeito; fila de niveis limpa=" + removidos);
                    }
                }
            }
            catch (Exception ex) { Diag.Write("pos-gate falhou: " + ex.GetType().Name); }

            if (NetworkingManager.Instance == null || !NetworkingManager.Instance.IsServer) return;
            HostAnnouncer.Publish();
        }
    }

    /// <summary>
    /// Bloqueia o save do personagem promovido: nivel e recompensas desta sessao nao chegam ao
    /// arquivo. Bloquear (em vez de trocar o nivel durante o save) evita a recursao causada por
    /// SaveDataThrottler -> Character.Save sincrono + setter de ExperienceLevel enfileirando save.
    /// </summary>
    [HarmonyPatch(typeof(Character), "Save", new[] { typeof(bool) })]
    internal static class SaveGuardPatch
    {
        [HarmonyPrefix]
        private static bool Prefix(Character __instance) => !SessionGuard.ShouldBlockSave(__instance);
    }

    /// <summary>Sessao de rede iniciada: reanuncia o minimo do grupo vigente.</summary>
    [HarmonyPatch(typeof(Root), "set_PlayingMultiplayer", new[] { typeof(bool) })]
    internal static class HostAnnouncePatch
    {
        [HarmonyPostfix]
        private static void Postfix(bool value)
        {
            if (value) HostAnnouncer.Publish();
        }
    }

    /// <summary>
    /// Saida de sessao: devolve o nivel original aos personagens vivos e descarta as marcas.
    /// Restaurar ANTES de esquecer e o que garante que nenhum save do encerramento grave o
    /// nivel promovido.
    /// </summary>
    [HarmonyPatch(typeof(NetworkingManager), "ExecuteExitToMainMenu", new System.Type[0])]
    internal static class SessionEndPatch
    {
        [HarmonyPostfix]
        private static void Postfix()
        {
            SessionGuard.RestoreAllAndForget();
            PromotionService.Reset();
            FollowUpModPlugin.Log.LogInfo("FU: sessao encerrada; nivel original restaurado");
        }
    }

    /// <summary>
    /// Fixa a ordem das etapas de subida de nivel: Skills -> Items -> Attributes -> Currency.
    /// `RoguelikeManager.LevelUpSequenceOrder` e campo serializado do prefab (:31) e a UI obedece
    /// a ele ao avancar (ConfirmLevelUpSelection, :427) e ao decidir o rotulo "Aceitar" (:138).
    /// Escrever aqui, no Start, garante a ordem antes de qualquer janela abrir (:351).
    /// </summary>
    [HarmonyPatch(typeof(RoguelikeManager), "Start", new System.Type[0])]
    internal static class LevelUpOrderPatch
    {
        [HarmonyPostfix]
        private static void Postfix(RoguelikeManager __instance)
        {
            try
            {
                var antes = __instance != null ? __instance.LevelUpSequenceOrder : null;
                string descricaoAntes = antes == null || antes.Length == 0 ? "null" : string.Join(">", antes);
                if (__instance == null) return;
                // Preserva a presenca de Currency: o prefab desta build tem 3 etapas
                // (Skills>Items>Attributes), sem etapa de moeda. Forcar Currency criaria um
                // passo vazio por nivel (CurrencyEarned=0 na promocao).
                bool temMoeda = false;
                if (antes != null)
                    foreach (var etapa in antes) if (etapa == LevelUpStage.Currency) temMoeda = true;
                var desejada = new List<LevelUpStage>
                {
                    LevelUpStage.Skills,
                    LevelUpStage.Items,
                    LevelUpStage.Attributes
                };
                if (temMoeda) desejada.Add(LevelUpStage.Currency);
                __instance.LevelUpSequenceOrder = desejada.ToArray();
                Diag.Write("ordem de subida: " + descricaoAntes + " -> " + string.Join(">", __instance.LevelUpSequenceOrder));
                FollowUpModPlugin.Log.LogInfo("FU: ordem das etapas de nivel " + descricaoAntes
                    + " -> " + string.Join(">", __instance.LevelUpSequenceOrder));
            }
            catch (Exception ex)
            {
                Diag.Write("ordem de subida falhou: " + ex.GetType().Name);
            }
        }
    }

    /// <summary>
    /// Substitui a confirmacao nativa da subida de nivel para resolver a fila por ETAPA
    /// (todas as skills, depois todos os itens, depois um bloco de atributos). Em caso de
    /// falha, devolve true e o metodo nativo assume - a UI nunca fica travada.
    /// </summary>
    [HarmonyPatch(typeof(RoguelikeManager), "ConfirmLevelUpSelection", new System.Type[0])]
    internal static class LevelUpFlowPatch
    {
        [HarmonyPrefix]
        private static bool Prefix(RoguelikeManager __instance) => !LevelUpFlow.Handle(__instance);
    }

    /// <summary>
    /// Instrumento de diagnostico: registra TODO clique em tile de personagem, inclusive os que
    /// o jogo ignora antes de chamar ToggleSelectedCharacter. Sem isso, "nao consegui adicionar"
    /// nao distingue recusa de nivel (nativa) de clique engolido pela guarda de roster.
    /// </summary>
    [HarmonyPatch(typeof(CharacterChoiceItem), "MouseDown", new[] { typeof(int) })]
    internal static class TileClickPatch
    {
        [HarmonyPostfix]
        private static void Postfix(CharacterChoiceItem __instance)
        {
            try
            {
                var c = __instance != null ? __instance.Character : null;
                bool noRoster = c == null
                    || (GameLogic.instance != null && GameLogic.instance.AllMyCharacters.Contains(c));
                int naParty = NetworkingManager.Instance != null ? NetworkingManager.Instance.PartyCharacters.Count : -1;
                string linha = "clique tile=" + (c == null ? "null" : c.CharacterName + "/nivel " + c.Level)
                    + " roster=" + noRoster + " party=" + naParty
                    + " jaSel=" + (c != null && c.SelectedForBattle);
                Diag.Write(linha);
                FollowUpModPlugin.Log.LogInfo("FU: " + linha);
            }
            catch (Exception ex)
            {
                Diag.Write("clique ilegivel: " + ex.GetType().Name);
            }
        }
    }
}
