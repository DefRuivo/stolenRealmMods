using System;
using Burst2Flame;
using HarmonyLib;

namespace RoguelikeDebugger.Patches
{
    /// <summary>
    /// RD-1: log do roll de eventos do mapa (WorldMapGenerator.GetRandomEvent).
    /// Mecânica (código): eventos saem de um BARAĺHO por NodeTypeEventSet
    /// (DeckRandomizer), sorteio ponderado por ChanceRatio; eventos recém-visitados
    /// saem do baralho (LastVisitedEvents); nós Event principais podem forçar
    /// fortune (50%); filtros CanSpawn(terreno, hora, tipo de nó, status, nível)
    /// com fallbacks progressivos.
    /// </summary>
    [HarmonyPatch(typeof(WorldMapGenerator), nameof(WorldMapGenerator.GetRandomEvent))]
    public static class EventRollDebugPatch
    {
        private static void Postfix(NodeTypeEventSet nodeTypeEventSet, TerrainAndTime terrainAndTime,
            int level, PartyEvent __result)
        {
            try
            {
                if (__result == null)
                {
                    Plugin.Log.LogWarning("[Event] roll retornou null (ver fallbacks no Player.log).");
                    return;
                }
                Plugin.Log.LogInfo(
                    $"[Event] '{__result.name}' | nodo={nodeTypeEventSet.nodeType} " +
                    $"minor={nodeTypeEventSet.isMinor} spawn={nodeTypeEventSet.eventSpawnType} | " +
                    $"terreno={terrainAndTime.TerrainType}/{terrainAndTime.TimeOfDay} | nível={level} | " +
                    $"chance={__result.ChanceRatio} | temBatalha={__result.HasBattle}");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"[Event] erro no debug: {e.Message}");
            }
        }
    }
}
