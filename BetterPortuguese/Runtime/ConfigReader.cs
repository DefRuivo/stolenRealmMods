using System;
using System.Collections.Generic;
using System.IO;
using BetterPortuguese.Core;

namespace BetterPortuguese.Runtime;
internal static class ConfigReader
{
    // BepInEx silently retains a previous value on a malformed serialized setting.
    // Validate our four raw keys before Reload, so typo != permission for Corrigido.
    public static Settings Parse(string text, Settings defaults)
    {
        var values = new Dictionary<string, string>(StringComparer.Ordinal);
        string section = "";
        foreach (var raw in text.Split('\n'))
        {
            var line = raw.Trim();
            if (line.Length == 0 || line.StartsWith("#") || line.StartsWith(";")) continue;
            if (line.StartsWith("[") && line.EndsWith("]")) { section = line.Substring(1, line.Length - 2); continue; }
            if (section != "Geral") continue;
            int at = line.IndexOf('=');
            if (at < 0) throw new FormatException("Malformed BetterPortuguese config line");
            string key = line.Substring(0, at).Trim();
            if (key != "Ativo" && key != "Conjunto" && key != "IntegracaoMods" && key != "Diagnostico") throw new FormatException("Unknown BetterPortuguese setting");
            if (values.ContainsKey(key)) throw new FormatException("Duplicate BetterPortuguese setting");
            values.Add(key, line.Substring(at + 1).Trim());
        }
        bool Boolean(string key, bool fallback) => values.TryGetValue(key, out var v) ? bool.TryParse(v, out var b) ? b : throw new FormatException("Invalid " + key) : fallback;
        var variant = defaults.Variant;
        if (values.TryGetValue("Conjunto", out var chosen))
        {
            if (chosen != "Original" && chosen != "Corrigido") throw new FormatException("Conjunto must be Original or Corrigido");
            variant = chosen == "Original" ? Conjunto.Original : Conjunto.Corrigido;
        }
        return new Settings(Boolean("Ativo", defaults.Active), variant, Boolean("IntegracaoMods", defaults.IntegrateMods), Boolean("Diagnostico", defaults.Diagnostic));
    }
}
