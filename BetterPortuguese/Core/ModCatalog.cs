using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;

namespace BetterPortuguese.Core;

// The map is owned by BP; the optional BT assembly is discovered by reflection at runtime.
// Templates are anchored and typed. Opaque player-name lists are never localized or rescanned.
internal sealed class ModCatalog
{
    public const string BetterTooltipsGuid = "com.gumatos.bettertooltips";
    public const string BetterTooltipsVersion = "0.1.5";
    public sealed class Rule
    {
        public string Id, Kind, Source, Target;
        public string[] Slots;
        private Regex matcher, wholeMatcher;
        public Rule(Dictionary<string, object> row)
        {
            JsonShape.Fields(row, "id", "kind", "source", "ptBR", "slots", "approvalTaskId");
            Id = JsonShape.Text(row["id"]); Kind = JsonShape.Text(row["kind"]);
            Source = JsonShape.Text(row["source"]); Target = JsonShape.Text(row["ptBR"]);
            Slots = JsonShape.Array(row["slots"]).Select(x => JsonShape.Text(x)).ToArray();
            if (!Regex.IsMatch(Id, "^BT-[0-9]{4}$") || JsonShape.Text(row["approvalTaskId"]) != "t_2e0fe616" ||
                !new[] { "note", "suffix", "header", "aura", "fragment" }.Contains(Kind) || Source.Length == 0 || Target.Length == 0)
                throw new FormatException("Invalid BT rule");
            if (!TokenGuard.Inventory(Source).SequenceEqual(TokenGuard.Inventory(Target), StringComparer.Ordinal))
                throw new FormatException("Mod functional tokens changed: " + Id);
            var sourceSlots = Regex.Matches(Source, @"\{([0-9]+)\}").Cast<Match>().Select(m => int.Parse(m.Groups[1].Value)).OrderBy(x => x).ToArray();
            var targetSlots = Regex.Matches(Target, @"\{([0-9]+)\}").Cast<Match>().Select(m => int.Parse(m.Groups[1].Value)).OrderBy(x => x).ToArray();
            if (!sourceSlots.SequenceEqual(Enumerable.Range(0, Slots.Length)) || !targetSlots.SequenceEqual(sourceSlots)) throw new FormatException("Invalid template slots: " + Id);
            string pattern = Regex.Escape(Source);
            for (int i = 0; i < Slots.Length; i++)
            {
                string numeric = @"[+−-]?[0-9]+(?:[.,][0-9]+)?";
                string part = Slots[i] == "number" ? numeric : Slots[i] == "richNumber" ? @"(?:<color=#[0-9A-Fa-f]{6}>" + numeric + @"</color>|" + numeric + ")" :
                    Slots[i] == "gameText" ? @"[^<>\r\n]{1,512}?" : Slots[i] == "opaque" ? @"[^<>\r\n]{1,8192}?" : throw new FormatException("Unknown slot type");
                pattern = pattern.Replace(Regex.Escape("{" + i + "}"), "(?<v" + i + ">" + part + ")");
            }
            matcher = new Regex(@"\G(?:" + pattern + ")", RegexOptions.CultureInvariant, TimeSpan.FromMilliseconds(30));
            wholeMatcher = new Regex(@"\A(?:" + pattern + @")\z", RegexOptions.CultureInvariant, TimeSpan.FromMilliseconds(30));
        }
        public bool Match(string text, int start, Func<string, string> localize, out int length, out string result, bool whole = false)
        {
            var m = (whole ? wholeMatcher : matcher).Match(text, start); length = m.Success ? m.Length : 0; result = null;
            if (!m.Success) return false;
            // Single pass over the TARGET. Never substitute into another captured name.
            result = Regex.Replace(Target, @"\{([0-9]+)\}", token => {
                int n = int.Parse(token.Groups[1].Value); string value = m.Groups["v" + n].Value;
                return Slots[n] == "gameText" ? (localize?.Invoke(value) ?? value) : value;
            });
            return true;
        }
    }
    public IReadOnlyList<Rule> Rules { get; }
    public int Count => Rules.Count;
    public static bool Enabled(Settings s, bool portuguese) => s != null && s.Valid && s.Active &&
        s.Variant == Conjunto.Corrigido && s.IntegrateMods && portuguese;
    private ModCatalog(string json)
    {
        var root = JsonShape.Object(StrictJson.Parse(json));
        JsonShape.Fields(root, "schemaVersion", "locale", "modGuid", "modVersion", "records");
        if (JsonShape.Int(root["schemaVersion"]) != 1 || JsonShape.Text(root["locale"]) != "pt-BR" ||
            JsonShape.Text(root["modGuid"]) != BetterTooltipsGuid || JsonShape.Text(root["modVersion"]) != BetterTooltipsVersion)
            throw new FormatException("Invalid mod registry identity/version");
        var rules = JsonShape.Array(root["records"]).Select(x => new Rule(JsonShape.Object(x))).ToList();
        if (rules.Count == 0 || rules.Select(r => r.Id).Distinct().Count() != rules.Count ||
            rules.Select(r => r.Kind + "\0" + r.Source).Distinct().Count() != rules.Count)
            throw new FormatException("Empty/duplicate mod registry");
        Rules = rules.AsReadOnly();
    }
    public static ModCatalog Parse(string json) => new ModCatalog(json);

    public bool TryWhole(string kind, string input, Func<string,string> localize, out string output)
    {
        output = input;
        if (input == null) return false;
        foreach (Rule rule in Rules.Where(r => r.Kind == kind).OrderByDescending(r => r.Source.Length))
            if (rule.Match(input, 0, localize, out int length, out string value, whole: true) && length == input.Length)
            { output = value; return true; }
        return false;
    }
    public bool TryNote(string input, Func<string,string> localize, out string output)
    {
        output = input;
        if (input == null || input.Length > 32768) return false;
        var builder = new StringBuilder(input.Length);
        int cursor = 0;
        var rules = Rules.Where(r => r.Kind == "note").OrderByDescending(r => r.Source.Length).ToArray();
        while (cursor < input.Length)
        {
            if (char.IsWhiteSpace(input[cursor])) { builder.Append(input[cursor++]); continue; }
            bool found = false;
            foreach (Rule rule in rules)
            {
                if (!rule.Match(input, cursor, localize, out int length, out string value)) continue;
                // Notes consist of whole sentences/lines, not arbitrary replacements in names.
                if (cursor + length < input.Length && !char.IsWhiteSpace(input[cursor + length])) continue;
                builder.Append(value); cursor += length; found = true; break;
            }
            if (!found) return false; // atomic refusal: no partly translated mechanic
        }
        output = builder.ToString(); return true;
    }
    public bool TryAura(string input, Func<string,string> localize, out string output)
    {
        output = input;
        string total = "";
        var suffix = Regex.Match(input, @" \(total [+−-]?[0-9]+(?:[.,][0-9]+)?%\)$", RegexOptions.CultureInvariant);
        if (suffix.Success) { total = suffix.Value; input = input.Substring(0, suffix.Index); }
        if (!TryWhole("aura", input, localize, out string translated)) return false;
        output = translated + total; return true;
    }
}
