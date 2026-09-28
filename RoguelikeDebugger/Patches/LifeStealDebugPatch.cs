using System;
using Burst2Flame;
using HarmonyLib;

namespace RoguelikeDebugger.Patches
{
    /// <summary>
    /// RV-7 — prova empírica do Life Steal.
    /// A localização do jogo e as patch notes v0.22 dizem "% da VIDA MÁXIMA por hit",
    /// mas o código atual (ApplyAction) calcula a partir da vida perdida do ALVO.
    /// Este patch registra cada cura de life steal junto com a vida máxima e o % do
    /// atributo, e cada dano causado por personagens do jogador — para compararmos
    /// no log qual das duas bases gera a cura observada.
    /// </summary>
    [HarmonyPatch(typeof(MessageWindowManager), nameof(MessageWindowManager.CreateBattleLogMessage))]
    public static class LifeStealDebugPatch
    {
        private static void Postfix(Character source, Character target, string message, float value)
        {
            try
            {
                if (message == null)
                {
                    return;
                }

                if (message == "[source] healed [value] health from life steal" && source != null)
                {
                    float ls = source["LifeSteal"];
                    float maxHp = source.MaxHealth;
                    float expectedMaxHpHeal = maxHp * ls / 100f;
                    Plugin.Log.LogInfo(
                        $"[LifeSteal] {source.CharacterName} curou {value:F1} | " +
                        $"vidaMáxima={maxHp:F1} | LifeSteal%={ls:F1} | nível={source.Level} | " +
                        $"(se base=vidaMáx, cura esperada sem redutores={expectedMaxHpHeal:F1})");
                }
                else if (message == "[source] dealt [value] Damage to [target]" &&
                    source != null && !source.IsAI && value > 0f)
                {
                    Plugin.Log.LogInfo(
                        $"[Dmg] {source.CharacterName} causou {value:F1} dano em " +
                        $"{(target != null ? target.CharacterName : "?")} | LifeSteal%={source["LifeSteal"]:F1}");
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"[LifeSteal] erro no debug: {e.Message}");
            }
        }
    }
}
