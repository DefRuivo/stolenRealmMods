using System;
using System.Collections.Generic;
using Burst2Flame;
using HarmonyLib;

namespace RoguelikeDebugger.Patches
{
    /// <summary>
    /// Postfix em GameLogic.GetCharacterLootDropModifier() — o ponto onde o jogo
    /// soma o atributo "DropQuantityMod" de cada personagem da party para calcular
    /// o multiplicador de loot. Loga o valor de cada personagem, a soma e o
    /// multiplicador final. Chamado a cada fim de batalha (GenerateLoot).
    ///
    /// Objetivo da investigação: confirmar que o powerup "Treasure Find"
    /// alimenta o DropQuantityMod (antes/depois da compra).
    /// </summary>
    [HarmonyPatch(typeof(GameLogic), nameof(GameLogic.GetCharacterLootDropModifier))]
    public static class LootModifierDebugPatch
    {
        private static void Postfix(ref float __result)
        {
            try
            {
                var party = NetworkingManager.Instance?.MyPartyCharacters;
                if (party == null)
                {
                    Plugin.Log.LogInfo("[Loot] Modificador de loot: party nula.");
                    return;
                }

                // Obs.: no código do jogo, "Root" é uma propriedade PRIVADA que devolve
                // a instância via NetworkingManager — por isso usamos o caminho completo.
                var root = NetworkingManager.Instance.NetworkManager.Root;
                Plugin.Log.LogInfo($"[Loot] PlayingRoguelike={root?.PlayingRoguelike}");

                foreach (var c in party)
                {
                    float v = c["DropQuantityMod"];
                    var pwr = new List<string>();

                    if (root != null &&
                        root.RoguelikePowerupsByConnection != null &&
                        root.RoguelikePowerupsByConnection.TryGetValue(c.OwnerID, out var set) &&
                        set.PowerupAndLevels != null)
                    {
                        foreach (var pl in set.PowerupAndLevels)
                        {
                            if (pl.Level > 0)
                            {
                                var p = Game.Instance.GetFromRoguelikePowerupDict(
                                    Game.Instance.GetGuidFromString(pl.Guid));
                                pwr.Add($"{p?.Name ?? "?"} Lv{pl.Level}");
                            }
                        }
                    }

                    Plugin.Log.LogInfo(
                        $"[Loot] {c.CharacterName}: DropQuantityMod={v}; " +
                        $"GoldMod={c["GoldMod"]}; DamageMod={c["DamageMod"]}; " +
                        $"DamageModHealing={c["DamageModHealing"]}; DamageReduction={c["DamageReduction"]}; " +
                        $"FreeMove={c["FreeMovementPoints"]}; RangeMelee={c["RangeTypeAdderMelee"]}; " +
                        $"RangeRanged={c["RangeTypeAdderRanged"]}; SkillOpts={c["AdditionalRoguelikeSkillOptions"]}; " +
                        $"AttrPtsPerLvl={c["AdditionalRoguelikeAttributesPointsPerLevel"]}; " +
                        $"Resilience={c["Resilience"]}; TakeCover={c["TakeCover"]}; " +
                        $"powerups ativos: {(pwr.Count > 0 ? string.Join(", ", pwr) : "nenhum")}");
                }

                Plugin.Log.LogInfo($"[Loot] Multiplicador final={__result}");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"[Loot] erro no debug: {e.Message}\n{e.StackTrace}");
            }
        }
    }
}
