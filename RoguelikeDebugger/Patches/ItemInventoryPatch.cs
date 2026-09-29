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
                    // Censo (RV-7): descricao COMPLETA.
                    var desc = it.OptionalDescription ?? "";

                    // CONSÚMIVEL (29/09, pedido do usuário): o item lança `ConsumableAction`
                    // como AÇÃO normal (`ExecuteAction(..., ItemInfo.ConsumableAction)`), e
                    // toda cura de ação passa pelo `GetActionDamage` — exatamente onde o
                    // `ChildOfTheAbyss` zera o `num9` (o valor de Healing). Dumpamos a ação e
                    // os efeitos dela para provar de que lado a poção cai, em vez de supor.
                    var cons = new System.Text.StringBuilder();
                    if (it.IsConsumable && it.ConsumableAction != null)
                    {
                        cons.Append(it.ConsumableAction.name).Append("::");
                        if (it.ConsumableAction.Effects != null)
                        {
                            foreach (var ef in it.ConsumableAction.Effects)
                            {
                                // `Effects` é IEffectInfo[] (interface, sem `Action`): o campo
                                // mora no GeneralEffect, que é o tipo concreto.
                                var ge = ef as GeneralEffect;
                                if (ge != null && !string.IsNullOrEmpty(ge.Action))
                                {
                                    cons.Append(ge.Action).Append("; ");
                                }
                            }
                        }
                    }
                    // O campo novo entra ANTES do desc=: o parser do censo ancora o desc no
                    // fim da linha, e nenhum valor pode conter '|' (vira o separador).
                    Plugin.Log.LogInfo(
                        $"[Item] '{it.name}' | tipo={it.ItemType} | raridade={it.Rarity} | " +
                        $"lvlMin={it.MinLevel} | consumivel={cons.ToString().Replace("|", "/").Replace("\n", " ")} | " +
                        $"desc=\"{desc.Replace("\n", " ")}\"");
                }

                // Coleta ATIVA dos afixos: o getter é lazy e não é acessado no menu,
                // então carregamos a lista nós mesmos (o próprio jogo faz o mesmo
                // Resources.LoadAll quando precisa).
                DumpItemMods();

                // Idem para os powerups (RV-7): o getter também é lazy e o menu não acessa.
                PowerupInventoryPatch.Trigger();
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"[Item] erro no inventário: {e.Message}");
            }
        }

        private static bool _modsDumped;

        private static void DumpItemMods()
        {
            try
            {
                if (_modsDumped)
                {
                    return;
                }
                var mods = Game.Instance.ItemMods;
                if (mods == null || mods.Length <= 1)
                {
                    return;
                }
                _modsDumped = true;

                Plugin.Log.LogInfo($"[ItemMod] Inventário: {mods.Length} afixos carregados.");
                foreach (var mod in mods)
                {
                    if (mod == null)
                    {
                        continue;
                    }
                    // Censo (RV-7): descricao COMPLETA.
                    var desc = mod.Description ?? "";
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
