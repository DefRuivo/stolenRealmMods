using System.Collections.Generic;
using Burst2Flame;
using HarmonyLib;
using UnityEngine;

namespace BetterTooltips.Patches
{
    /// <summary>
    /// RV-20 — valores DINÂMICOS de shrine nas tooltips (30/09).
    ///
    /// Causa raiz (decodificada): Tooltip.ShowGroundEffectTooltip monta o GameFunctionParameters
    /// com Source = WorldCharacter e SEM Target. A expressão das auras de shrine é
    /// Mathf.Round(BASE * (1 + (Target["ShrineEffectBonus"] / 100))) — com Target vazio o
    /// bônus vale 0 e o número exibido no hover do shrine é sempre a BASE (observado em jogo
    /// pelo usuário: com Omnism o valor não mudava). No tooltip do STATUS o jogo passa o
    /// personagem como Target, então lá o número já saía correto.
    ///
    /// Fix 1 (prefix abaixo): quando alguma expressão usa "ShrineEffectBonus" e o Target está
    /// vazio, Target = Source — o motor passa a calcular o valor REAL com o bônus do jogador.
    ///
    /// Fix 2 (AcumuladoShrines): linha dinâmica com as auras de shrine ativas no WorldCharacter,
    /// somadas por atributo com o mesmo fator; o LocalizePatch anexa às chaves da família.
    ///
    /// A Dwarven Aura fica FORA do acumulado: o efeito real dela não mora no AttributeEffects
    /// (vazio no dump, sem fórmula no cache compilado) — registrar, não somar.
    /// </summary>
    [HarmonyPatch]
    public static class ShrineAuraPatch
    {
        private static readonly HashSet<string> Family = new HashSet<string>
        {
            "Warrior Aura", "Guardian Aura", "Conqueror Aura", "Rogue Aura", "Reaper Aura",
            "Energy Aura", "Seraph Aura", "Shaman Aura", "Fury"
        };

        private static readonly Dictionary<string, (string attr, float baseVal)> AuraMap =
            new Dictionary<string, (string, float)>
            {
                { "Warrior Aura",   ("DamageMod", 20f) },
                { "Guardian Aura",  ("DamageReduction", 20f) },
                { "Conqueror Aura", ("CritChance", 20f) },
                { "Rogue Aura",     ("DodgeChance", 20f) },
                { "Reaper Aura",    ("LifeOnHit", 8f) },
                { "Energy Aura",    ("ManaCostMod", -50f) },
                { "Seraph Aura",    ("HealthPerTurnPercent", 10f) },
                { "Shaman Aura",    ("ManaPerTurnPercent", 10f) },
                { "Fury",           ("DamageMod", 25f) }, // Fury também tem DamageReduction −25 (no loop)
            };

        /// <summary>Chaves de texto (exatas) da família de auras de shrine no LocalizePatch.</summary>
        private static readonly HashSet<string> ShrineKeys = new HashSet<string>
        {
            "Attackers take Fire Damage.",
            "Take [0]% of your Max Health in Shadow Damage per turn.",
            "Damage increased by [0]%. ",
            "Reduces Damage taken by [0]%. ",
            "Critical hit chance increased by [0]%.",
            "Increases dodge chance by [0]%.",
            "Lifesteal increased by [0]%.",
            "Decreases the cost of mana using abilities by [0]%.",
            "Your attacks have a [0]% chance to stun the target.",
            "Recover [0]% of maximum health each turn. ",
            "Recover [0]% of maximum mana each turn. ",
            "Damage increased by [0]%. Damage taken increased by [0]%. "
        };

        public static bool IsShrineKey(string text)
        {
            return text != null && ShrineKeys.Contains(text);
        }

        private static bool UsesShrineBonus(string[] expressions)
        {
            if (expressions == null)
            {
                return false;
            }
            foreach (string e in expressions)
            {
                if (e != null && e.Contains("ShrineEffectBonus"))
                {
                    return true;
                }
            }
            return false;
        }

        [HarmonyPatch(typeof(Tooltip), "ApplyDescriptionExpressions")]
        [HarmonyPrefix]
        private static void FixShrineTarget(ref GameFunctionParameters __3, string[] expressions)
        {
            if (__3.Target == null && __3.Source != null && UsesShrineBonus(expressions))
            {
                __3.Target = __3.Source;
            }
        }

        /// <summary>Formata um atributo acumulado com a semântica CERTA do jogo:
        /// DamageReduction positivo = dano tomado REDUZIDO; ManaCostMod negativo = custo REDUZIDO.</summary>
        private static string Format(string attr, float v)
        {
            switch (attr)
            {
                case "DamageReduction":
                    return v >= 0 ? "Damage taken −" + v + "%" : "Damage taken +" + (-v) + "%";
                case "ManaCostMod":
                    return "Mana Costs reduced by " + (-v) + "%";
                case "DamageMod": return "Damage +" + v + "%";
                case "CritChance": return "Crit Chance +" + v + "%";
                case "DodgeChance": return "Dodge +" + v + "%";
                case "LifeOnHit": return "Life Steal +" + v + "%";
                case "HealthPerTurnPercent": return "Health per turn +" + v + "%";
                case "ManaPerTurnPercent": return "Mana per turn +" + v + "%";
                default: return attr + " " + v + "%";
            }
        }

        /// <summary>Linha de acumulado (ou "" se não há nada). Nunca lança.</summary>
        public static string AcumuladoShrines()
        {
            try
            {
                Character c = NetworkingManager.Instance?.NetworkManager?.Root?.WorldCharacter;
                if (c == null || c.ActionStatuses == null || c.ActionStatuses.Count == 0)
                {
                    return "";
                }
                float bonus = c["ShrineEffectBonus"];
                Dictionary<string, float> totals = new Dictionary<string, float>();
                foreach (var st in c.ActionStatuses)
                {
                    if (st == null || st.EventStatusInfo == null)
                    {
                        continue;
                    }
                    string nome = st.EventStatusInfo.Name;
                    if (!Family.Contains(nome) || !AuraMap.TryGetValue(nome, out var m))
                    {
                        continue;
                    }
                    float v = Mathf.Round(m.baseVal * (1f + bonus / 100f));
                    if (nome == "Fury")
                    {
                        Add(totals, "DamageMod", v);
                        Add(totals, "DamageReduction", -v);
                    }
                    else
                    {
                        Add(totals, m.attr, v);
                    }
                }
                if (totals.Count == 0)
                {
                    return "";
                }
                List<string> parts = new List<string>();
                foreach (var kv in totals)
                {
                    parts.Add(Format(kv.Key, kv.Value));
                }
                return "\n<color=#C8B090>Your active shrine auras: " + string.Join("; ", parts) + ".</color>";
            }
            catch
            {
                return "";
            }
        }

        private static void Add(Dictionary<string, float> totals, string attr, float v)
        {
            totals[attr] = totals.TryGetValue(attr, out float cur) ? cur + v : v;
        }
    }
}
