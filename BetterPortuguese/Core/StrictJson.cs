using System;
using System.Collections.Generic;
using System.Globalization;
using System.Text;

namespace BetterPortuguese.Core;

// No runtime JSON dependency; rejects duplicate members BEFORE any DTO is built.
internal sealed class StrictJson
{
    private readonly string text;
    private int pos;
    private StrictJson(string text) { this.text = text ?? throw new ArgumentNullException(nameof(text)); }
    public static object Parse(string text)
    {
        var reader = new StrictJson(text);
        var result = reader.Value(0);
        reader.White();
        if (reader.pos != text.Length) throw reader.Error("Trailing content");
        return result;
    }
    private FormatException Error(string reason) => new FormatException(reason + " at JSON offset " + pos);
    private void White() { while (pos < text.Length && " \t\r\n".IndexOf(text[pos]) >= 0) pos++; }
    private bool Take(char c) { White(); if (pos < text.Length && text[pos] == c) { pos++; return true; } return false; }
    private void Need(char c) { if (!Take(c)) throw Error("Expected " + c); }
    private object Value(int depth)
    {
        if (depth > 64) throw Error("Maximum nesting exceeded");
        White();
        if (pos >= text.Length) throw Error("Unexpected end");
        char c = text[pos];
        if (c == '"') return String();
        if (c == '{')
        {
            pos++;
            var dict = new Dictionary<string, object>(StringComparer.Ordinal);
            if (Take('}')) return dict;
            do {
                White(); if (pos >= text.Length || text[pos] != '"') throw Error("Expected member name");
                var key = String(); Need(':'); var value = Value(depth + 1);
                if (dict.ContainsKey(key)) throw Error("Duplicate member " + key);
                dict.Add(key, value);
            } while (Take(','));
            Need('}'); return dict;
        }
        if (c == '[')
        {
            pos++;
            var values = new List<object>();
            if (Take(']')) return values;
            do { values.Add(Value(depth + 1)); } while (Take(','));
            Need(']'); return values;
        }
        foreach (var word in new[] { "true", "false", "null" })
        {
            if (pos + word.Length <= text.Length && string.CompareOrdinal(text, pos, word, 0, word.Length) == 0)
            { pos += word.Length; return word == "null" ? null : (object)(word == "true"); }
        }
        int start = pos;
        if (text[pos] == '-') pos++;
        if (pos >= text.Length) throw Error("Number truncated");
        if (text[pos] == '0') pos++;
        else { if (text[pos] < '1' || text[pos] > '9') throw Error("Invalid value"); Digits(); }
        if (pos < text.Length && text[pos] == '.') { pos++; int before = pos; Digits(); if (before == pos) throw Error("Fraction missing"); }
        if (pos < text.Length && (text[pos] == 'e' || text[pos] == 'E'))
        { pos++; if (pos < text.Length && (text[pos] == '+' || text[pos] == '-')) pos++; int before = pos; Digits(); if (before == pos) throw Error("Exponent missing"); }
        if (!decimal.TryParse(text.Substring(start, pos - start), NumberStyles.Float, CultureInfo.InvariantCulture, out var number)) throw Error("Number out of range");
        return number;
    }
    private void Digits() { while (pos < text.Length && text[pos] >= '0' && text[pos] <= '9') pos++; }
    private char Hex()
    {
        if (pos + 4 > text.Length) throw Error("Truncated unicode escape");
        if (!ushort.TryParse(text.Substring(pos, 4), NumberStyles.HexNumber, CultureInfo.InvariantCulture, out var n)) throw Error("Invalid unicode escape");
        pos += 4; return (char)n;
    }
    private string String()
    {
        Need('"'); var result = new StringBuilder();
        while (pos < text.Length)
        {
            char c = text[pos++];
            if (c == '"')
            {
                var s = result.ToString();
                for (int i = 0; i < s.Length; i++)
                    if (char.IsHighSurrogate(s[i])) { if (++i >= s.Length || !char.IsLowSurrogate(s[i])) throw Error("Unpaired surrogate"); }
                    else if (char.IsLowSurrogate(s[i])) throw Error("Unpaired surrogate");
                return s;
            }
            if (c < 32) throw Error("Control character in string");
            if (c != '\\') { result.Append(c); continue; }
            if (pos >= text.Length) throw Error("Truncated escape");
            c = text[pos++];
            switch (c)
            {
                case '"': case '\\': case '/': result.Append(c); break;
                case 'b': result.Append('\b'); break;
                case 'f': result.Append('\f'); break;
                case 'n': result.Append('\n'); break;
                case 'r': result.Append('\r'); break;
                case 't': result.Append('\t'); break;
                case 'u': result.Append(Hex()); break;
                default: throw Error("Invalid escape");
            }
        }
        throw Error("Unterminated string");
    }
}

internal static class JsonShape
{
    public static Dictionary<string, object> Object(object value) => value as Dictionary<string, object> ?? throw new FormatException("Expected object");
    public static List<object> Array(object value) => value as List<object> ?? throw new FormatException("Expected array");
    public static string Text(object value, bool nullable = false) => value == null && nullable ? null : value as string ?? throw new FormatException("Expected string");
    public static bool Bool(object value) => value is bool b ? b : throw new FormatException("Expected boolean");
    public static int Int(object value) => value is decimal n && decimal.Truncate(n) == n && n >= int.MinValue && n <= int.MaxValue ? (int)n : throw new FormatException("Expected integer");
    public static void Fields(Dictionary<string, object> obj, params string[] fields)
    {
        if (obj.Count != fields.Length) throw new FormatException("Unexpected/missing fields");
        foreach (var field in fields) if (!obj.ContainsKey(field)) throw new FormatException("Missing field " + field);
    }
    public static bool Equal(object a, object b)
    {
        if (ReferenceEquals(a, b)) return true;
        if (a is Dictionary<string, object> da && b is Dictionary<string, object> db)
        { if (da.Count != db.Count) return false; foreach (var kv in da) if (!db.TryGetValue(kv.Key, out var x) || !Equal(kv.Value, x)) return false; return true; }
        if (a is List<object> la && b is List<object> lb)
        { if (la.Count != lb.Count) return false; for (int i = 0; i < la.Count; i++) if (!Equal(la[i], lb[i])) return false; return true; }
        return Equals(a, b);
    }
}
