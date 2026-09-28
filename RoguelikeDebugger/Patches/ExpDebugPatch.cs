using System;
using HarmonyLib;

namespace RoguelikeDebugger.Patches
{
    /// <summary>
    /// Postfix em GameLogic.GetTotalExpValue(float modifier) — breakdown de experiência
    /// da batalha (RD-1).
    /// Fórmula (código): final = Σ por-inimigo × modifier, onde
    /// por-inimigo = Ceil( GetExperiencePerBattlePoint(min(30,Lvl)) × PointValue
    ///   × Difficulty.ExperienceMod × (1+Σ EnemyMods.exp) / (1+AdditionalBattlePointsPerc/100) ).
    /// </summary>
    [HarmonyPatch(typeof(GameLogic), nameof(GameLogic.GetTotalExpValue))]
    public static class ExpDebugPatch
    {
        private static void Postfix(float modifier, ref float __result)
        {
            try
            {
                float baseSum = (modifier != 0f) ? __result / modifier : 0f;
                float diffMod = GameLogic.instance.CurrentDifficulty.ExperienceMod;
                Plugin.Log.LogInfo(
                    $"[Exp] total={__result:F1} | base(por inimigos)={baseSum:F1} | " +
                    $"modificador da batalha={modifier:F2} | multiplicador de dificuldade={diffMod:F2}");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"[Exp] erro no debug: {e.Message}");
            }
        }
    }

    /// <summary>
    /// Postfix em Character.GetExpValue() — valor de experiência por inimigo morto (RD-1).
    /// O jogo já faz Debug.Log disso (vai para o Player.log); aqui espelhamos no
    /// LogOutput.log para termos tudo em um lugar só.
    /// </summary>
    [HarmonyPatch(typeof(Character), nameof(Character.GetExpValue))]
    public static class EnemyExpDebugPatch
    {
        private static void Postfix(Character __instance, ref float __result)
        {
            try
            {
                if (__instance == null)
                {
                    return;
                }
                Plugin.Log.LogInfo(
                    $"[ExpInimigo] {__instance.CharacterInfo.name} (Lv {__instance.Level}, " +
                    $"PointValue {__instance.PointValue}) = {__result:F1} exp");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"[ExpInimigo] erro no debug: {e.Message}");
            }
        }
    }
}
