using System;
using System.Collections.Generic;
using HarmonyLib;

namespace RoguelikeDebugger.Patches
{
    /// <summary>
    /// Postfix em GameLogic.ApplyGoldModifiers(float originalGold) — ponto onde o jogo
    /// soma o atributo "GoldMod" de cada personagem da party e multiplica o ouro.
    /// Chamado na distribuição de ouro pós-batalha, recompensas de aventura e eventos.
    ///
    /// Objetivo: confirmar que o powerup "Increased Gold Find" alimenta o GoldMod
    /// (esperado: Lv5 → +50, espelhando o Treasure Find/DropQuantityMod da BT-3).
    /// </summary>
    [HarmonyPatch(typeof(GameLogic), nameof(GameLogic.ApplyGoldModifiers))]
    public static class GoldModifierDebugPatch
    {
        private static void Postfix(float originalGold, ref float __result)
        {
            try
            {
                var party = NetworkingManager.Instance?.MyPartyCharacters;
                var parts = new List<string>();
                float sum = 0f;
                if (party != null)
                {
                    foreach (var c in party)
                    {
                        float v = c["GoldMod"];
                        sum += v;
                        parts.Add($"{c.CharacterName}={v}");
                    }
                }

                Plugin.Log.LogInfo(
                    $"[Gold] ouro base={originalGold} party=[{(parts.Count > 0 ? string.Join(", ", parts) : "-")}] " +
                    $"GoldMod soma={sum} ouro final={__result}");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"[Gold] erro no debug: {e.Message}");
            }
        }
    }
}
