using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace BetterPortuguese.Core;

// Only BT-owned colored blocks are translated; never a global string replacement.
internal static class ModText
{
    public const string AuraHeader = "Your active shrine auras:";
    public const string SynergyHeader = "Your skills on this status:";
    private const string Number = @"[+−-]?[0-9]+(?:[.,][0-9]+)?";
    private static readonly Regex Colors = new Regex(@"<color=#[0-9A-Fa-f]{6}>(?<body>[^<>]*)</color>", RegexOptions.CultureInvariant, TimeSpan.FromMilliseconds(50));
    private static readonly Regex AttributeSuffix = new Regex(@" \(<color=#[0-9A-Fa-f]{6}>(?<parts>[^<>\r\n]+)</color>\)$", RegexOptions.CultureInvariant, TimeSpan.FromMilliseconds(30));
    private static readonly Regex AttributePart = new Regex(@"^(?<number>" + Number + @") (?<label>[^<>\r\n]+)$", RegexOptions.CultureInvariant);
    private static readonly Regex ValueSuffix = new Regex(@" \((?:<color=#[0-9A-Fa-f]{6}>)?" + Number + @"(?:</color>)?(?: health for you| health per turn for you|% increased damage right now| damage per turn for you)\)\.$", RegexOptions.CultureInvariant);

    // Rebase BEFORE BT registers notes/colors. Keep BP's exact localized origin,
    // and only transplant the colored tail and independently identified dynamic suffix.
    public static string Rebase(ModCatalog map, string original, string localized, string generated, Func<string,string> localize)
    {
        if (generated == null || localized == null || original == null || generated == original) return localized;
        int tail = generated.Length;
        foreach (Match m in Colors.Matches(generated))
            if (m.Value.StartsWith("<color=#C8B090>", StringComparison.Ordinal) || m.Groups["body"].Value.StartsWith(AuraHeader, StringComparison.Ordinal))
            { tail = m.Index; while (tail > 0 && generated[tail-1] == '\n') tail--; break; }
        string main = generated.Substring(0, tail).TrimEnd();
        string result = localized;
        Match value = ValueSuffix.Match(main);
        if (value.Success && !original.EndsWith(value.Value, StringComparison.Ordinal))
        {
            if (!map.TryWhole("suffix", value.Value, localize, out string translated)) throw new FormatException("Unknown BT value suffix");
            result = localized.TrimEnd();
            if (result.EndsWith(".", StringComparison.Ordinal)) result = result.Substring(0, result.Length-1);
            result += translated;
        }
        else
        {
            Match attr = AttributeSuffix.Match(main);
            if (attr.Success && !original.EndsWith(attr.Value, StringComparison.Ordinal))
            {
                string parts = TranslateAttributeList(attr.Groups["parts"].Value, localize);
                result = localized.TrimEnd() + attr.Value.Replace(attr.Groups["parts"].Value, parts);
            }
        }
        return result + generated.Substring(tail);
    }
    private static string TranslateAttributeList(string input, Func<string,string> localize)
    {
        return string.Join(", ", input.Split(new[]{", "}, StringSplitOptions.None).Select(part => {
            Match m = AttributePart.Match(part);
            if (!m.Success) throw new FormatException("Unknown BT attribute suffix");
            return m.Groups["number"].Value + " " + localize(m.Groups["label"].Value);
        }));
    }
    public static string Translate(ModCatalog map, string input, ISet<string> ownedNotes, Func<string,string> localize, Action<string> refusal)
    {
        if (input == null || input.Length > 65536) return input;
        return Colors.Replace(input, m => {
            string body = m.Groups["body"].Value, translated;
            if (ownedNotes.Contains(body))
            {
                if (!map.TryNote(body, localize, out translated)) { refusal?.Invoke("nota BT fora do mapa; bloco preservado"); return m.Value; }
            }
            else if (body.StartsWith(AuraHeader + " ", StringComparison.Ordinal))
                translated = Blue(map, body, AuraHeader, localize, false);
            else if (body.StartsWith(SynergyHeader + " ", StringComparison.Ordinal))
                translated = Blue(map, body, SynergyHeader, localize, true);
            else return m.Value;
            return m.Value.Substring(0, m.Groups["body"].Index-m.Index) + translated + "</color>";
        });
    }
    private static string Blue(ModCatalog map, string body, string header, Func<string,string> localize, bool synergy)
    {
        if (!body.EndsWith(".", StringComparison.Ordinal) || !map.TryWhole("header", header, localize, out string title)) return body;
        string[] items = body.Substring(header.Length+1, body.Length-header.Length-2).Split(new[]{"; "}, StringSplitOptions.None);
        var result = new List<string>();
        foreach (string item in items)
        {
            string value;
            if (synergy) value = Synergy(map, item, localize);
            else if (!map.TryAura(item, localize, out value)) return body;
            result.Add(value);
        }
        return title + " " + string.Join("; ", result) + ".";
    }
    private static string Fragment(ModCatalog map, string text)
        => map.TryWhole("fragment", text, null, out string value) ? value : text;
    private static string Synergy(ModCatalog map, string item, Func<string,string> localize)
    {
        var m = Regex.Match(item, @"^(?<names>.+) (?<number>" + Number + @")(?<effect>%? [^<>]+?)(?<stack> per stack)?$", RegexOptions.CultureInvariant, TimeSpan.FromMilliseconds(30));
        if (!m.Success) throw new FormatException("Unknown BT synergy layout");
        string names = string.Join(" + ", m.Groups["names"].Value.Split(new[]{" + "}, StringSplitOptions.None).Select(localize));
        string effect = m.Groups["effect"].Value;
        if (effect == "% damage" || effect == "% Max Health") effect = Fragment(map, effect);
        else effect = effect.StartsWith("% ", StringComparison.Ordinal) ? "% " + localize(effect.Substring(2)) : " " + localize(effect.Substring(1));
        return names + " " + m.Groups["number"].Value + effect + Fragment(map, m.Groups["stack"].Value);
    }
}
