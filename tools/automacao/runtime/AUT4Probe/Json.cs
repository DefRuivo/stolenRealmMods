// AUT-4: serializador JSON minimo (sem dependencia externa). Mesmo espirito do
// Json.cs do CAP-1: escreve Dictionary<string,object>, listas e primitivos.
using System;
using System.Collections;
using System.Collections.Generic;
using System.Globalization;
using System.Text;

namespace Aut4Probe
{
    internal static class Json
    {
        public static Dictionary<string, object> Campos(params object[] pares)
        {
            var d = new Dictionary<string, object>();
            for (int i = 0; i + 1 < pares.Length; i += 2) d[Convert.ToString(pares[i])] = pares[i + 1];
            return d;
        }

        public static string Serialize(object o)
        {
            var sb = new StringBuilder();
            Escreve(sb, o);
            return sb.ToString();
        }

        private static void Escreve(StringBuilder sb, object o)
        {
            if (o == null) { sb.Append("null"); return; }
            if (o is string s) { Texto(sb, s); return; }
            if (o is bool b) { sb.Append(b ? "true" : "false"); return; }
            if (o is float f) { sb.Append(f.ToString("R", CultureInfo.InvariantCulture)); return; }
            if (o is double dbl) { sb.Append(dbl.ToString("R", CultureInfo.InvariantCulture)); return; }
            if (o is int || o is long || o is short || o is byte)
            { sb.Append(Convert.ToString(o, CultureInfo.InvariantCulture)); return; }

            if (o is IDictionary<string, object> map)
            {
                sb.Append('{');
                bool prim = true;
                foreach (var par in map)
                {
                    if (!prim) sb.Append(',');
                    prim = false;
                    Texto(sb, par.Key);
                    sb.Append(':');
                    Escreve(sb, par.Value);
                }
                sb.Append('}');
                return;
            }
            if (o is IDictionary dico)
            {
                sb.Append('{');
                bool prim = true;
                foreach (DictionaryEntry par in dico)
                {
                    if (!prim) sb.Append(',');
                    prim = false;
                    Texto(sb, Convert.ToString(par.Key));
                    sb.Append(':');
                    Escreve(sb, par.Value);
                }
                sb.Append('}');
                return;
            }
            if (o is IEnumerable en)
            {
                sb.Append('[');
                bool prim = true;
                foreach (var item in en)
                {
                    if (!prim) sb.Append(',');
                    prim = false;
                    Escreve(sb, item);
                }
                sb.Append(']');
                return;
            }
            Texto(sb, Convert.ToString(o, CultureInfo.InvariantCulture));
        }

        private static void Texto(StringBuilder sb, string s)
        {
            sb.Append('"');
            foreach (char c in s)
            {
                switch (c)
                {
                    case '"': sb.Append("\\\""); break;
                    case '\\': sb.Append("\\\\"); break;
                    case '\n': sb.Append("\\n"); break;
                    case '\r': sb.Append("\\r"); break;
                    case '\t': sb.Append("\\t"); break;
                    default:
                        if (c < ' ') sb.Append("\\u").Append(((int)c).ToString("x4"));
                        else sb.Append(c);
                        break;
                }
            }
            sb.Append('"');
        }
    }
}
