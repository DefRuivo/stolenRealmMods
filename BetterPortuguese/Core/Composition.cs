using System;
using System.Collections.Generic;

namespace BetterPortuguese.Core;

// Composition, not dictionary edits. Exact output allowlists intentionally refuse drift.
internal static class Composition
{
    public const string AssemblySha256 = "8bb4a7c512da20770a81dfac0347e9a68a8c0eff736f4566c52a66923b37855a";
    internal enum Agreement { Masculine, Feminine, MasculinePlural, FemininePlural }
    internal static readonly IReadOnlyDictionary<string, Agreement> Nouns = new Dictionary<string, Agreement>(StringComparer.Ordinal)
    {
        // All noun-bearing ItemType/EquipmentType values in the measured build.
        ["Arma"] = Agreement.Feminine, ["Escudo"] = Agreement.Masculine,
        ["Cabeça"] = Agreement.Feminine, ["Armadura"] = Agreement.Feminine,
        ["Anel"] = Agreement.Masculine, ["Amuleto"] = Agreement.Masculine,
        ["Consumível"] = Agreement.Masculine, ["Material"] = Agreement.Masculine,
        ["Ferramenta"] = Agreement.Feminine, ["Mercadoria"] = Agreement.Feminine,
        ["Espada de 1M"] = Agreement.Feminine, ["Espada 2M"] = Agreement.Feminine,
        ["Machado de 1M"] = Agreement.Masculine, ["Machado de 2 Mãos"] = Agreement.Masculine,
        ["Arma de Haste"] = Agreement.Feminine, ["Arco"] = Agreement.Masculine,
        ["Arma de 1 Mão"] = Agreement.Feminine, ["Arma de 2M"] = Agreement.Feminine,
        ["Cajado"] = Agreement.Masculine, ["Varinha"] = Agreement.Feminine,
        ["Maça 1M"] = Agreement.Feminine, ["Maça 2M"] = Agreement.Feminine,
        ["Arma de Punho"] = Agreement.Feminine,
        // Requested vocabulary; these are not separate enum types in this build.
        ["Espada"] = Agreement.Feminine, ["Adaga"] = Agreement.Feminine,
        ["Lança"] = Agreement.Feminine, ["Bota"] = Agreement.Feminine,
        ["Botas"] = Agreement.FemininePlural, ["Luva"] = Agreement.Feminine,
        ["Luvas"] = Agreement.FemininePlural, ["Capa"] = Agreement.Feminine,
        ["Maça"] = Agreement.Feminine, ["Machado"] = Agreement.Masculine
    };
    // Columns: game default, feminine, masculine plural, feminine plural.
    internal static readonly string[][] Rarities = {
        new[] { "Comum", "Comum", "Comuns", "Comuns" },
        new[] { "Incomum", "Incomum", "Incomuns", "Incomuns" },
        new[] { "Raro", "Rara", "Raros", "Raras" },
        new[] { "Lendário", "Lendária", "Lendários", "Lendárias" },
        new[] { "Mítico", "Mítica", "Míticos", "Míticas" }
    };

    public static bool Enabled(Settings settings, bool portuguese, out string reason)
    {
        reason = settings == null || !settings.Valid ? "config invalida" :
            !settings.Active ? "Ativo=false" : settings.Variant != Conjunto.Corrigido ? "Conjunto=Original" :
            !portuguese ? "idioma diferente de pt-BR" : null;
        return reason == null;
    }

    // Only a complete, bare subtitle line can match. No regex/global replacement,
    // no edits to title, affixes, description, colors or the requirement/header lines.
    public static string ItemSubtitle(string incoming, out string reason)
    {
        reason = null;
        if (incoming == null) { reason = "subtitulo nulo"; return incoming; }
        var lines = incoming.Split('\n');
        int found = -1;
        string replacement = null;
        for (int i = 0; i < lines.Length; i++)
        {
            foreach (var noun in Nouns)
            {
                if (lines[i] == noun.Key) // Common is omitted by the native main path.
                {
                    if (found >= 0) { reason = "mais de uma linha de tipo"; return incoming; }
                    found = i; replacement = lines[i];
                }
                foreach (var forms in Rarities)
                {
                    // Accept the native masculine form or already-correct output (idempotence).
                    string desired = forms[(int)noun.Value] + " " + noun.Key;
                    if (lines[i] != forms[0] + " " + noun.Key && lines[i] != desired) continue;
                    if (found >= 0) { reason = "mais de uma linha de tipo"; return incoming; }
                    found = i; replacement = desired;
                }
            }
        }
        if (found < 0) { reason = "formato/raridade/tipo nao reconhecido"; return incoming; }
        if (lines[found] == replacement) return incoming;
        lines[found] = replacement;
        return string.Join("\n", lines);
    }

    public static string DamageLabel(bool healing, string incoming, out string reason)
    {
        reason = null;
        if (!healing) return incoming;
        if (incoming == "Cura por Dano") return incoming;
        if (incoming != "Cura de Dano") { reason = "rotulo Healing divergente"; return incoming; }
        return "Cura por Dano";
    }
}
