using System;
using System.Collections.Generic;
using Burst2Flame;
using HarmonyLib;

namespace RoguelikeDebugger.Patches
{
    /// <summary>
    /// Inventário completo de skills/spells do jogo (BT-7).
    /// Patch no getter de Game.Skills: despeja a lista quando o tamanho estabilizar
    /// (o jogo popula incrementalmente durante o loading, como nos status).
    /// </summary>
    [HarmonyPatch(typeof(Game), "get_Skills")]
    public static class SkillInventoryPatch
    {
        private static bool _dumped;
        private static int _lastCount = -1;
        private static int _stableHits;

        private static void Postfix(List<SkillInfo> __result)
        {
            try
            {
                if (_dumped || __result == null || __result.Count <= 1)
                {
                    return;
                }

                // Estabilização: dump só quando o tamanho ficar igual por 5 acessos seguidos.
                if (__result.Count == _lastCount)
                {
                    _stableHits++;
                }
                else
                {
                    _stableHits = 1;
                    _lastCount = __result.Count;
                }
                if (_stableHits < 5)
                {
                    return;
                }
                _dumped = true;

                Plugin.Log.LogInfo($"[Skill] Inventário: {__result.Count} skills carregados.");
                foreach (var sk in __result)
                {
                    if (sk == null)
                    {
                        continue;
                    }
                    // Censo (RV-7): descricao COMPLETA. O corte em 110 chars existia para nao
                    // poluir o log, mas sem o texto inteiro o checklist de revisao nao serve.
                    var desc = sk.Description ?? "";
                    string tags = sk.SkillTags != null ? string.Join(",", sk.SkillTags) : "";
                    Plugin.Log.LogInfo(
                        $"[Skill] '{sk.SkillName}' | tipo={sk.SkillType} | dano={sk.DamageType} | " +
                        $"tier={sk.Tier} | tags={tags} | desc=\"{desc.Replace("\n", " ")}\"");
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"[Skill] erro no inventário: {e.Message}");
            }
        }
    }
}
