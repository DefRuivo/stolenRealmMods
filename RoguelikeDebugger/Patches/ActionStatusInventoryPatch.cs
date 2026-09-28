using System;
using System.Collections.Generic;
using Burst2Flame;
using HarmonyLib;

namespace RoguelikeDebugger.Patches
{
    /// <summary>
    /// Inventário completo de status/efeitos do jogo (BT-6).
    /// O setter de Game.ActionStatuses é chamado uma única vez com lista VAZIA
    /// (o jogo popula via Add no getter), então patchamos o GETTER: na primeira
    /// vez em que a lista estiver populada, despeja o inventário completo.
    /// </summary>
    [HarmonyPatch(typeof(Game), "get_ActionStatuses")]
    public static class ActionStatusInventoryPatch
    {
        private static bool _dumped;
        private static int _lastCount = -1;
        private static int _stableHits;

        private static void Postfix(List<ActionStatusInfo> __result)
        {
            try
            {
                if (_dumped || __result == null || __result.Count <= 1)
                {
                    return;
                }

                // O jogo carrega os status incrementalmente durante o loading:
                // só despejamos quando o tamanho ficar estável por 5 acessos seguidos.
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

                Plugin.Log.LogInfo($"[Status] Inventário: {__result.Count} status carregados.");
                foreach (var s in __result)
                {
                    if (s == null)
                    {
                        continue;
                    }
                    var desc = s.Description ?? "";
                    if (desc.Length > 90)
                    {
                        desc = desc.Substring(0, 90) + "...";
                    }
                    Plugin.Log.LogInfo(
                        $"[Status] '{s.Name}' | tipo={s.StatusType} | raridade={s.Rarity} | " +
                        $"desc=\"{desc.Replace("\n", " ")}\"");
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"[Status] erro no inventário: {e.Message}");
            }
        }
    }
}
