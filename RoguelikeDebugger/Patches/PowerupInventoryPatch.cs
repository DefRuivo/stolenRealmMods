using System;
using Burst2Flame;
using HarmonyLib;

namespace RoguelikeDebugger.Patches
{
    /// <summary>
    /// Inventário completo de powerups roguelike (RV-7 — censo de tooltips).
    /// Game.RoguelikePowerups é lazy (Resources.LoadAll "Roguelike Powerups"), então
    /// usamos o mesmo padrão dos outros dumps: despeja quando o tamanho estabilizar.
    /// Cada linha é um NÍVEL de powerup (nome, guid, nível, custo, efeitos e descrição),
    /// porque o texto exibido no tooltip é por nível.
    /// </summary>
    [HarmonyPatch(typeof(Game), "get_RoguelikePowerups")]
    public static class PowerupInventoryPatch
    {
        private static bool _dumped;

        /// <summary>
        /// Força o carregamento: o getter é lazy e o menu pode nunca acessá-lo, então
        /// alguém que roda no boot (o dump de itens) chama isto.
        /// </summary>
        internal static void Trigger()
        {
            try
            {
                Plugin.Log.LogInfo("[Powerup] trigger chamado (forçando o load lazy).");
                var _ = Game.Instance.RoguelikePowerups;
                Plugin.Log.LogInfo($"[Powerup] getter retornou {(_ == null ? "null" : _.Length + " itens")}.");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"[Powerup] trigger falhou: {e.Message}");
            }
        }

        private static void Postfix(RoguelikePowerup[] __result)
        {
            try
            {
                // Diferente dos status/skills (populados incrementalmente), aqui o getter é um
                // Resources.LoadAll — atômico. Então basta UMA chamada com array válido.
                if (_dumped || __result == null || __result.Length <= 1)
                {
                    return;
                }
                _dumped = true;

                Plugin.Log.LogInfo($"[Powerup] Inventário: {__result.Length} powerups carregados.");
                foreach (var p in __result)
                {
                    if (p == null)
                    {
                        continue;
                    }
                    if (p.PowerupLevels == null || p.PowerupLevels.Length == 0)
                    {
                        Plugin.Log.LogInfo($"[Powerup] '{p.Name}' | guid={p.Guid} | (sem níveis)");
                        continue;
                    }
                    for (int i = 0; i < p.PowerupLevels.Length; i++)
                    {
                        var lv = p.PowerupLevels[i];
                        if (lv == null)
                        {
                            continue;
                        }
                        var ef = new System.Text.StringBuilder();
                        if (lv.CharacterEffects != null)
                        {
                            foreach (var e in lv.CharacterEffects)
                            {
                                if (e == null || e.CharacterAttribute == null)
                                {
                                    continue;
                                }
                                ef.Append(e.CharacterAttribute.name).Append(':')
                                  .Append(e.CharacterEffectMethod).Append(':')
                                  .Append(e.Amount).Append(", ");
                            }
                        }
                        string desc = (lv.Description ?? "").Replace("\n", " ");
                        Plugin.Log.LogInfo(
                            $"[Powerup] '{p.Name}' | guid={p.Guid} | nivel={i + 1} | custo={lv.Cost} | " +
                            $"efeitos={ef} | desc=\"{desc}\"");
                    }
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"[Powerup] erro no inventário: {e.Message}");
            }
        }
    }
}
