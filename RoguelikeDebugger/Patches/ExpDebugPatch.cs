using System;
using HarmonyLib;

namespace RoguelikeDebugger.Patches
{
    /// <summary>
    /// Postfix em GameLogic.GetTotalExpValue(float modifier) — total de experiência
    /// da batalha. O jogo já loga por inimigo (GetExpValue → Debug.Log); aqui
    /// registramos o total + o modificador aplicado, para investigação de
    /// Experience (RD-1).
    /// </summary>
    [HarmonyPatch(typeof(GameLogic), nameof(GameLogic.GetTotalExpValue))]
    public static class ExpDebugPatch
    {
        private static void Postfix(float modifier, ref float __result)
        {
            try
            {
                Plugin.Log.LogInfo($"[Exp] Total de experiencia da batalha: {__result} (modificador recebido: {modifier})");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"[Exp] erro no debug: {e.Message}");
            }
        }
    }
}
