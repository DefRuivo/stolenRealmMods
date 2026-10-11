using System;
using System.Collections.Generic;
using HarmonyLib;
using RoguelikeLevelProgression.Core;
using RoguelikeLevelProgression.Runtime;

namespace RoguelikeLevelProgression.Patches
{
    /// <summary>
    /// Recompensas. Nivel de consulta fixo (Rewards.RewardQueryLevel) para consulta E criacao de
    /// item quando o personagem passa do 20 — preserva o patamar 20 em vez de extrapolar chances
    /// (GetMultipler faz LerpUnclamped e pode passar de 100/negativar).
    /// Nao altera LevelUpSequenceOrder compartilhado nem settings/extension global.
    /// </summary>
    public static class RewardQueryPatches
    {
        public static void PrefixSkillChoices(ref int level, Character character)
        {
            if (!PluginState.Enabled) return;
            if (level <= XpCurve.VanillaCapLevel) return;
            if (character == null) return;
            if (!ExtensionScope.AppliesTo(character)) return;
            int query = PluginState.RewardQueryLevel;
            if (query <= XpCurve.VanillaCapLevel || query == level) return;
            level = query;
        }

        public static void PrefixItemChoices(ref int level, Character recipient)
        {
            if (!PluginState.Enabled) return;
            if (level <= XpCurve.VanillaCapLevel) return;
            if (recipient == null) return;
            if (!ExtensionScope.AppliesTo(recipient)) return;
            int query = PluginState.RewardQueryLevel;
            if (query <= XpCurve.VanillaCapLevel || query == level) return;
            level = query;
        }

        /// <summary>Impede que um item nulo entre na lista de opcoes (fallback null do pool vazio).</summary>
        public static void PostfixItemChoices(ref List<Item> __result)
        {
            if (__result == null) return;
            int removed = __result.RemoveAll(item => item == null);
            if (removed > 0)
            {
                Log.Warn("GetItemChoices devolveu " + removed + " item(ns) nulo(s); removidos antes de popular a janela");
            }
            if (__result.Count == 0)
            {
                Log.WarnOnce("GetItemChoices devolveu lista vazia: estagio de itens sera pulado, seguindo para atributos");
            }
        }

        /// <summary>
        /// Contagem da fila: subtrai as skills substituidas (S) registradas no sidecar.
        /// Vale apenas para personagem deste mod; recibo nao concede dinheiro/atributos.
        /// </summary>
        public static void PostfixNeededCount(Character character, ref int __result)
        {
            if (!PluginState.Enabled) return;
            if (character == null) return;
            if (!ExtensionScope.AppliesTo(character)) return;
            int s = LedgerService.ReceiptCount(character);
            if (s <= 0) return;
            __result -= s;
            if (__result < 0) __result = 0;
        }
    }

    /// <summary>
    /// Adaptador da sequencia de level-up (parte05 §4). Trabalha por ENTRADA DA FILA e nao
    /// altera o array LevelUpSequenceOrder compartilhado: apenas avanca CurLevelUpStage quando
    /// o estagio corrente nao tem conteudo valido. Pool de skill esgotado = recibo duravel
    /// ANTES de avancar; se o recibo nao gravar, o estagio NAO e pulado.
    /// </summary>
    public static class LevelUpStagePatches
    {
        private const int MaxStageHops = 8;

        public static void PostfixOpenSkillSelectWindow(RoguelikeManager __instance)
        {
            try
            {
                EnsurePlayableStage(__instance);
            }
            catch (Exception ex)
            {
                Log.WarnOnce("Adaptador de estagio falhou (" + ex.GetType().Name + ": " + ex.Message + "); janela vanilla mantida");
            }
        }

        internal static void EnsurePlayableStage(RoguelikeManager mgr)
        {
            if (mgr == null) return;
            for (int hop = 0; hop < MaxStageHops; hop++)
            {
                LevelUpStage stage;
                try { stage = mgr.CurLevelUpStage; }
                catch (Exception) { return; }

                var character = mgr.CurrentRoguelikeSkillSelectingCharacter;

                if (stage == LevelUpStage.Skills)
                {
                    if (HasSkillOption(mgr)) return;
                    if (character == null || !ExtensionScope.AppliesTo(character)) return; // vanilla decide

                    string error;
                    if (!LedgerService.TryRecordSkippedSkill(character, SafeLevel(character), out error))
                    {
                        Log.Error("pool de skills esgotado e recibo NAO gravado (" + error + "): estagio NAO sera pulado");
                        return;
                    }
                    Log.Warn("pool de skills esgotado no nivel " + SafeLevel(character)
                             + ": recibo S gravado, seguindo para o proximo estagio");
                    if (!AdvanceStage(mgr, character)) return;
                    continue;
                }

                if (stage == LevelUpStage.Items)
                {
                    if (HasItemOption(mgr)) return;
                    Log.Warn("pool de itens vazio: seguindo para o proximo estagio");
                    if (!AdvanceStage(mgr, character)) return;
                    continue;
                }

                // Attributes e Currency sao do jogo; nada a fazer.
                return;
            }
            Log.WarnOnce("adaptador de estagio atingiu o limite de saltos; janela mantida como esta");
        }

        private static int SafeLevel(Character c)
        {
            try { return c.Level; }
            catch (Exception) { return 0; }
        }

        private static bool HasSkillOption(RoguelikeManager mgr)
        {
            try
            {
                var buttons = mgr.SkillOptionBtns;
                if (buttons == null) return false;
                for (int i = 0; i < buttons.Length; i++)
                {
                    var b = buttons[i];
                    if (b != null && b.gameObject != null && b.gameObject.activeSelf && b.SkillInfo != null) return true;
                }
                return false;
            }
            catch (Exception)
            {
                return true; // sem certeza: nao mexer no fluxo vanilla
            }
        }

        private static bool HasItemOption(RoguelikeManager mgr)
        {
            try
            {
                var inv = mgr.ItemInventory;
                if (inv == null) return true;
                var items = inv.AllItems;
                if (items == null || items.Count == 0) return false;
                for (int i = 0; i < items.Count; i++)
                {
                    if (items[i] != null) return true;
                }
                return false;
            }
            catch (Exception)
            {
                return true;
            }
        }

        /// <summary>
        /// Avanca para o proximo estagio da ordem COMPARTILHADA (somente leitura), pulando
        /// Attributes sem pontos pendentes — mesmo comportamento do vanilla em
        /// ConfirmLevelUpSelection. Devolve false quando a entrada da fila terminou.
        /// </summary>
        private static bool AdvanceStage(RoguelikeManager mgr, Character character)
        {
            var order = mgr.LevelUpSequenceOrder;
            if (order == null || order.Length == 0) return false;
            int index = Array.IndexOf(order, mgr.CurLevelUpStage);
            if (index < 0) return false;

            for (int k = index + 1; k < order.Length; k++)
            {
                var next = order[k];
                mgr.CurLevelUpStage = next;
                if (next == LevelUpStage.Attributes)
                {
                    int pending = 0;
                    try { pending = character != null ? character.UnspentStatPoints : 0; }
                    catch (Exception) { pending = 0; }
                    if (pending <= 0) continue;
                }
                return true;
            }

            // acabou a sequencia: fecha esta entrada da fila
            mgr.CharactersWaitingForLevelUp.RemoveAt(0);
            if (mgr.CharactersWaitingForLevelUp.Count > 0)
            {
                mgr.OpenSkillSelectWindow(mgr.CharactersWaitingForLevelUp[0], false);
            }
            else
            {
                mgr.Close();
            }
            return false;
        }
    }

    /// <summary>
    /// Reroll. Se nao existe NENHUMA opcao para o tier forcado, o vanilla removeria a skill e
    /// deixaria a janela travada (SelectedSkillOption nulo). Aqui o reroll e cancelado antes de
    /// qualquer remocao, preservando a skill original (parte05 §4).
    /// </summary>
    public static class RerollPatches
    {
        public static bool PrefixRerollSkill(RoguelikeManager __instance)
        {
            try
            {
                var character = __instance != null ? __instance.CurrentRoguelikeSkillSelectingCharacter : null;
                var selected = __instance != null ? __instance.SelectedSkillOption : null;
                if (character == null || selected == null || selected.SkillInfo == null) return true;
                if (!ExtensionScope.AppliesTo(character)) return true;

                var settings = GameState.Settings();
                int baseOptions = settings != null ? settings.NumSkillOptions : 4;
                int extra = 0;
                try { extra = (int)character["AdditionalRoguelikeSkillOptions"]; }
                catch (Exception) { extra = 0; }
                int numOptions = baseOptions + extra;
                if (numOptions <= 0) numOptions = 1;

                var already = new List<Burst2Flame.SkillInfo>(character.SkillsFromPoints);
                already.Remove(selected.SkillInfo);

                var options = __instance.GetSkillChoices(numOptions, character.Level, already, selected.SkillInfo.Tier, character);
                if (options == null || options.Count == 0)
                {
                    Log.Warn("reroll sem opcoes no tier " + selected.SkillInfo.Tier
                             + ": reroll cancelado, skill original preservada");
                    return false;
                }
                return true;
            }
            catch (Exception ex)
            {
                Log.WarnOnce("guarda de reroll falhou (" + ex.GetType().Name + ": " + ex.Message + "); seguindo o fluxo vanilla");
                return true;
            }
        }
    }

    /// <summary>
    /// Reset de run: SOMENTE depois de SyncCharacterToPreset valido e concluido (parte05 §4).
    /// Preset nulo nao reseta; excecao no corpo original impede o postfix de rodar.
    /// </summary>
    public static class PresetSyncPatches
    {
        public static void Postfix(Character __instance, CharacterPresetFile preset)
        {
            if (__instance == null) return;
            if (preset == null)
            {
                Log.Warn("SyncCharacterToPreset com preset nulo: ledger NAO resetado");
                return;
            }
            if (!ExtensionScope.AppliesTo(__instance)) return;
            int level = 1;
            try { level = __instance.Level; }
            catch (Exception) { return; }
            if (level != 1)
            {
                Log.Warn("SyncCharacterToPreset terminou com Level=" + level + " (esperado 1): ledger NAO resetado");
                return;
            }
            string presetGuid = "";
            try { presetGuid = preset.Guid.ToString(); }
            catch (Exception) { presetGuid = ""; }
            if (string.IsNullOrEmpty(presetGuid))
            {
                try { presetGuid = __instance.CharacterPresetFileGuid; }
                catch (Exception) { }
            }
            LedgerService.OnPresetSyncSuccess(__instance, presetGuid);
        }
    }
}
