using System;
using System.Collections.Generic;

namespace BetterPortuguese.Core;

// Composition, not dictionary edits. Exact output allowlists intentionally refuse drift.
internal static class Composition
{
    // POLÍTICA DE PIN (SR-BETA-06 / SR-QA-PIN): pin único e exato na build instalada (open_beta
    // 1.4.9 / build 26878331). Divergiu o sha256, a composição é recusada (BP-COMP/BP-MODS):
    // build nova exige re-medição e re-pin, nunca "aceitar qualquer sha".
    // Re-homologação de 26/11/2026: os alvos de composição foram comparados corpo a corpo entre
    // 1.4.8 e 1.4.9 (todas as 2324 classes top-level; só SteamManager, BardSkillTest e
    // <PrivateImplementationDetails> mudaram) e as assinaturas por NOME continuam iguais.
    // Este valor duplica ApiIdentity.AssemblySha256 de propósito (o BetterPortuguese não
    // referencia RealmApi); os dois pins têm de mudar juntos.
    public const string AssemblySha256 = "f3f0069b3a21e7939ed85d9d31ec5ec7cb4c24015811e25350ed2239a25ed182";
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
    private static readonly (string Original, string Corrected)[] FortuneLabels = Array.ConvertAll(Rarities,
        forms => (forms[0] + " Sorte", "Fortuna " + forms[(int)Agreement.Feminine].ToLowerInvariant()));

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

    // The caller has already proved it's a Fortune, and supplies the asset's exact tier.
    // Never rename the game's shared rarity or Fortune localization keys.
    public static string FortuneSubtitle(int quality, string incoming, out string reason)
    {
        reason = null;
        if ((uint)quality >= (uint)FortuneLabels.Length) { reason = "raridade de Fortuna desconhecida"; return incoming; }
        var (original, corrected) = FortuneLabels[quality];
        if (incoming == corrected) return incoming;
        if (incoming == original) return corrected;
        reason = "subtitulo de Fortuna divergente";
        return incoming;
    }

    public static string DamageLabel(bool healing, string incoming, out string reason)
    {
        reason = null;
        if (!healing) return incoming;
        if (incoming == "Cura por Dano") return incoming;
        // O template pt-BR de "[damage type] Damage" virou "Dano [damage type]" (SR-QA-03), entao o tipo
        // Healing chega aqui como "Dano Cura". A forma antiga ("Cura de Dano") fica aceita logo abaixo
        // para nao quebrar dataset anterior nem o probe; qualquer outra forma continua recusada.
        if (incoming == "Dano Cura") return "Cura por Dano";
        if (incoming != "Cura de Dano") { reason = "rotulo Healing divergente"; return incoming; }
        return "Cura por Dano";
    }
}
