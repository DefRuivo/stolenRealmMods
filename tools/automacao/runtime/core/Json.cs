// KIT-04 Core - Serializador JSON mínimo sem dependências externas
using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using System.Text;

namespace KIT04Core
{
    /// <summary>
    /// Serializador JSON mínimo sem dependências externas.
    /// Suporta: null, string, bool, float, double, int, long, short, byte, IDictionary, IEnumerable.
    /// </summary>
    public static class Json
    {
        /// <summary>
        /// Retorna campos ordenados em dictionary.
        /// </summary>
        public static Dictionary<string, object> Campos(params object[] pares)
        {
            if (pares.Length % 2 != 0)
                throw new ArgumentException("Campos deve ter par de key/value");

            var dic = new Dictionary<string, object>();
            for (var i = 0; i < pares.Length; i += 2)
            {
                var key = pares[i]?.ToString();
                if (key == null)
                    throw new ArgumentException("Chave de campo nao pode ser null");
                dic[key] = pares[i + 1];
            }
            return dic;
        }

        /// <summary>
        /// Serializa objeto para JSON.
        /// </summary>
        public static string Serialize(object obj)
        {
            var sb = new StringBuilder();
            Escreve(sb, obj);
            return sb.ToString();
        }

        /// <summary>
        /// Escreve JSON em StringBuilder.
        /// </summary>
        public static void Escreve(StringBuilder sb, object obj)
        {
            if (obj == null)
            {
                sb.Append("null");
                return;
            }

            switch (obj)
            {
                case string s:
                    Texto(sb, s);
                    break;
                case bool b:
                    sb.Append(b ? "true" : "false");
                    break;
                case float f:
                    sb.Append(f.ToString("R", System.Globalization.CultureInfo.InvariantCulture));
                    break;
                case double d:
                    sb.Append(d.ToString("R", System.Globalization.CultureInfo.InvariantCulture));
                    break;
                case int i:
                    sb.Append(i);
                    break;
                case long l:
                    sb.Append(l);
                    break;
                case short sh:
                    sb.Append(sh);
                    break;
                case byte by:
                    sb.Append(by);
                    break;
                case IDictionary dict:
                    EscreveDict(sb, dict);
                    break;
                case IEnumerable list when !(obj is byte[]):
                    EscreveList(sb, list);
                    break;
                default:
                    // Outros tipos: tentar converter para string
                    Texto(sb, obj.ToString());
                    break;
            }
        }

        /// <summary>
        /// Escreve string JSON (com escape).
        /// </summary>
        public static void Texto(StringBuilder sb, string s)
        {
            sb.Append("\"");
            foreach (var c in s)
            {
                switch (c)
                {
                    case '"': sb.Append("\\\""); break;
                    case '\\': sb.Append("\\\\"); break;
                    case '\b': sb.Append("\\b"); break;
                    case '\f': sb.Append("\\f"); break;
                    case '\n': sb.Append("\\n"); break;
                    case '\r': sb.Append("\\r"); break;
                    case '\t': sb.Append("\\t"); break;
                    default:
                        if (c < ' ')
                            sb.Append("\\u").Append(((int)c).ToString("x4"));
                        else
                            sb.Append(c);
                        break;
                }
            }
            sb.Append("\"");
        }

        /// <summary>
        /// Escreve IDictionary como JSON object.
        /// </summary>
        public static void EscreveDict(StringBuilder sb, IDictionary dict)
        {
            sb.Append("{");
            var primeiro = true;
            foreach (DictionaryEntry entry in dict)
            {
                if (!primeiro) sb.Append(",");
                primeiro = false;
                Texto(sb, entry.Key?.ToString() ?? "");
                sb.Append(":");
                Escreve(sb, entry.Value);
            }
            sb.Append("}");
        }

        /// <summary>
        /// Escreve IEnumerable como JSON array.
        /// </summary>
        public static void EscreveList(StringBuilder sb, IEnumerable list)
        {
            sb.Append("[");
            var primeiro = true;
            foreach (var item in list)
            {
                if (!primeiro) sb.Append(",");
                primeiro = false;
                Escreve(sb, item);
            }
            sb.Append("]");
        }
    }
}
