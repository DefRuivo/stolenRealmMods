using System;
using System.Collections.Generic;
using Burst2Flame;
using HarmonyLib;

namespace RoguelikeDebugger.Patches
{
    /// <summary>
    /// Inventário completo de itens base e afixos (BT-8).
    /// Game.Items e Game.ItemMods são lazy: despejamos quando o tamanho estabilizar
    /// (mesmo mecanismo de estabilização dos status/skills).
    /// </summary>
    [HarmonyPatch(typeof(Game), "get_Items")]
    public static class ItemInventoryPatch
    {
        private static bool _itemsDumped;
        private static int _itemsLast = -1;
        private static int _itemsStable;

        private static void Postfix(List<ItemInfo> __result)
        {
            try
            {
                if (_itemsDumped || __result == null || __result.Count <= 1)
                {
                    return;
                }
                if (__result.Count == _itemsLast)
                {
                    _itemsStable++;
                }
                else
                {
                    _itemsStable = 1;
                    _itemsLast = __result.Count;
                }
                if (_itemsStable < 5)
                {
                    return;
                }
                _itemsDumped = true;

                Plugin.Log.LogInfo($"[Item] Inventário: {__result.Count} itens base carregados.");
                foreach (var it in __result)
                {
                    if (it == null)
                    {
                        continue;
                    }
                    var desc = it.OptionalDescription ?? "";
                    if (desc.Length > 100)
                    {
                        desc = desc.Substring(0, 100) + "...";
                    }
                    Plugin.Log.LogInfo(
                        $"[Item] '{it.name}' | tipo={it.ItemType} | raridade={it.Rarity} | " +
                        $"lvlMin={it.MinLevel} | desc=\"{desc.Replace("\n", " ")}\"");
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"[Item] erro no inventário: {e.Message}");
            }
        }
    }

    [HarmonyPatch(typeof(Game), "get_ItemMods")]
    public static class ItemModInventoryPatch
    {
        private static bool _modsDumped;
        private static int _modsLast = -1;
        private static int _modsStable;

        private static void Postfix(ItemMod[] __result)
        {
            try
            {
                if (_modsDumped || __result == null || __result.Length <= 1)
                {
                    return;
                }
                if (__result.Length == _modsLast)
                {
                    _modsStable++;
                }
                else
                {
                    _modsStable = 1;
                    _modsLast = __result.Length;
                }
                if (_modsStable < 5)
                {
                    return;
                }
                _modsDumped = true;

                Plugin.Log.LogInfo($"[ItemMod] Inventário: {__result.Length} afixos carregados.");
                foreach (var mod in __result)
                {
                    if (mod == null)
                    {
                        continue;
                    }
                    var desc = mod.Description ?? "";
                    if (desc.Length > 100)
                    {
                        desc = desc.Substring(0, 100) + "...";
                    }
                    Plugin.Log.LogInfo(
                        $"[ItemMod] '{mod.name}' | tipo={mod.ItemModType} | raridade={mod.Rarity} | " +
                        $"desc=\"{desc.Replace("\n", " ")}\"");
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"[ItemMod] erro no inventário: {e.Message}");
            }
        }
    }
}
