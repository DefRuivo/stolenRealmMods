using System;
using System.Collections.Generic;
using HarmonyLib;
using RoguelikeLevelProgression.Core;
using RoguelikeLevelProgression.Runtime;

namespace RoguelikeLevelProgression.Patches
{
    /// <summary>
    /// UI. InventoryManager.RefreshHealthbars tem o literal >= 30 (corpus 126620) e mostra "Max".
    /// Aqui o bloco de XP e RECALCULADO no mesmo formato vanilla apenas quando o personagem esta
    /// no escopo ampliado E o nivel passou do 30 do literal; Health/Mana permanecem intactos
    /// (equivalente limitado ao bloco de XP, como permite a parte05/D).
    /// </summary>
    public static class InventoryManagerPatches
    {
        public static bool Prefix(InventoryManager __instance, out Character __state)
        {
            __state = null;
            try
            {
                var c = GameLogic.instance != null ? GameLogic.instance.CurrentlySelectedCharacter : null;
                if (c == null) return true;
                if (!ExtensionScope.AppliesTo(c)) return true;
                if (ExtensionScope.Push(c)) __state = c;
            }
            catch (Exception)
            {
                __state = null;
            }
            return true;
        }

        public static void Finalizer(Character __state)
        {
            if (__state != null) ExtensionScope.Pop();
        }

        public static void Postfix(InventoryManager __instance, Character __state)
        {
            var c = __state;
            if (c == null || __instance == null) return;
            if (!ExtensionScope.AppliesTo(c)) return;
            int level;
            try { level = c.Level; }
            catch (Exception) { return; }
            // Abaixo do literal 30 o calculo vanilla ja esta correto (a extensao torna os pisos coerentes).
            if (level < 30) return;

            try
            {
                float floorCur = Character.GetExperienceFloorForLevel(level);
                float floorNext = Character.GetExperienceFloorForLevel(level + 1);
                float exp = c.Experience;
                float span = (float)Math.Ceiling(floorNext) - (float)Math.Ceiling(floorCur);
                float done = (float)Math.Ceiling(exp) - (float)Math.Ceiling(floorCur);
                bool ok = XpCurve.IsUsableNumber(span) && XpCurve.IsUsableNumber(done) && span > 0f;
                if (!ok)
                {
                    Log.WarnOnce("RefreshHealthbars: barra de XP sem divisor valido em nivel " + level + "; exibindo 0");
                    if (__instance.ToNextLevelImage != null) __instance.ToNextLevelImage.fillAmount = 0f;
                    if (__instance.ToNextLevelText != null) __instance.ToNextLevelText.text = "0";
                    return;
                }
                float ratio = done / span;
                if (ratio < 0f) ratio = 0f;
                if (ratio > 1f) ratio = 1f;
                if (__instance.ToNextLevelImage != null) __instance.ToNextLevelImage.fillAmount = ratio;
                if (__instance.ToNextLevelText != null)
                {
                    float remaining = span - done;
                    if (remaining < 0f) remaining = 0f;
                    __instance.ToNextLevelText.text = GUIManager.instance.floatToText((float)Math.Ceiling(remaining));
                }
            }
            catch (Exception ex)
            {
                Log.WarnOnce("RefreshHealthbars: recálculo da barra falhou (" + ex.GetType().Name + ": " + ex.Message + ")");
            }
        }
    }

    /// <summary>
    /// Skillbar.UpdateExpBar (corpus 332983-332991): usa os pisos de XP, sem guarda contra
    /// divisor zero/NaN. O escopo estendido mantem a formula coerente e a guarda impede NaN.
    /// </summary>
    public static class SkillbarPatches
    {
        public static bool Prefix(Skillbar __instance, out bool __state)
        {
            __state = false;
            Character c = null;
            try { c = __instance != null ? __instance.Character : null; }
            catch (Exception) { return true; }
            if (c == null) return true;
            if (!ExtensionScope.AppliesTo(c)) return true;
            __state = ExtensionScope.Push(c);
            try
            {
                int level = c.Level;
                float span = Character.GetExperienceFloorForLevel(level + 1) - Character.GetExperienceFloorForLevel(level);
                if (!XpCurve.IsUsableNumber(span) || span <= 0f)
                {
                    Log.WarnOnce("UpdateExpBar: divisor invalido (" + span.ToString("R") + "); barra zerada");
                    if (__instance.expBar != null) __instance.expBar.fillAmount = 0f;
                    if (__state) { ExtensionScope.Pop(); __state = false; }
                    return false;
                }
            }
            catch (Exception ex)
            {
                Log.WarnOnce("UpdateExpBar: guarda falhou (" + ex.GetType().Name + ": " + ex.Message + ")");
                if (__state) { ExtensionScope.Pop(); __state = false; }
                return false;
            }
            return true;
        }

        public static void Finalizer(bool __state)
        {
            if (__state) ExtensionScope.Pop();
        }
    }
}
