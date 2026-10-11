using System;
using System.Collections.Generic;
using System.Globalization;
using System.Text;

namespace RoguelikeLevelProgression.Core
{
    /// <summary>
    /// Leitor/escritor JSON minimo e ESTRITO, sem dependencia externa (o mod e standalone:
    /// nao assume Newtonsoft nem System.Text.Json no runtime do jogo).
    /// Suporta exatamente o subconjunto necessario ao sidecar v1 (parte05 §4):
    /// objeto, array, string, inteiro, float, booleano e null.
    /// Rejeita entrada malformada (o chamador trata como ledger corrompido).
    /// </summary>
    public static class MiniJson
    {
        public sealed class ParseException : Exception
        {
            public ParseException(string message) : base(message) { }
        }

        public static string Escape(string s)
        {
            if (s == null) return "null";
            var sb = new StringBuilder(s.Length + 2);
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
                    case '\b': sb.Append("\\b"); break;
                    case '\f': sb.Append("\\f"); break;
                    default:
                        if (c < ' ') sb.Append("\\u").Append(((int)c).ToString("x4", CultureInfo.InvariantCulture));
                        else sb.Append(c);
                        break;
                }
            }
            sb.Append('"');
            return sb.ToString();
        }

        public static string Number(long v) { return v.ToString(CultureInfo.InvariantCulture); }

        public static string Number(double v)
        {
            if (double.IsNaN(v) || double.IsInfinity(v)) throw new ArgumentException("numero nao finito");
            return v.ToString("R", CultureInfo.InvariantCulture);
        }

        // ---------------- parser ----------------

        private sealed class Parser
        {
            private readonly string _s;
            private int _i;

            public Parser(string s) { _s = s; _i = 0; }

            public object ParseDocument()
            {
                SkipWs();
                object v = ParseValue();
                SkipWs();
                if (_i != _s.Length) throw new ParseException("conteudo extra apos o documento na posicao " + _i);
                return v;
            }

            private void SkipWs()
            {
                while (_i < _s.Length)
                {
                    char c = _s[_i];
                    if (c == ' ' || c == '\t' || c == '\r' || c == '\n') { _i++; continue; }
                    break;
                }
            }

            private object ParseValue()
            {
                if (_i >= _s.Length) throw new ParseException("fim inesperado");
                char c = _s[_i];
                switch (c)
                {
                    case '{': return ParseObject();
                    case '[': return ParseArray();
                    case '"': return ParseString();
                    case 't': Expect("true"); return true;
                    case 'f': Expect("false"); return false;
                    case 'n': Expect("null"); return null;
                    default: return ParseNumber();
                }
            }

            private void Expect(string literal)
            {
                if (_i + literal.Length > _s.Length || string.CompareOrdinal(_s, _i, literal, 0, literal.Length) != 0)
                    throw new ParseException("literal invalido na posicao " + _i);
                _i += literal.Length;
            }

            private Dictionary<string, object> ParseObject()
            {
                var d = new Dictionary<string, object>(StringComparer.Ordinal);
                _i++; // {
                SkipWs();
                if (_i < _s.Length && _s[_i] == '}') { _i++; return d; }
                while (true)
                {
                    SkipWs();
                    if (_i >= _s.Length || _s[_i] != '"') throw new ParseException("chave esperada na posicao " + _i);
                    string key = ParseString();
                    if (d.ContainsKey(key)) throw new ParseException("chave duplicada: " + key);
                    SkipWs();
                    if (_i >= _s.Length || _s[_i] != ':') throw new ParseException("':' esperado na posicao " + _i);
                    _i++;
                    SkipWs();
                    d[key] = ParseValue();
                    SkipWs();
                    if (_i >= _s.Length) throw new ParseException("fim inesperado no objeto");
                    if (_s[_i] == ',') { _i++; continue; }
                    if (_s[_i] == '}') { _i++; return d; }
                    throw new ParseException("',' ou '}' esperado na posicao " + _i);
                }
            }

            private List<object> ParseArray()
            {
                var l = new List<object>();
                _i++; // [
                SkipWs();
                if (_i < _s.Length && _s[_i] == ']') { _i++; return l; }
                while (true)
                {
                    SkipWs();
                    l.Add(ParseValue());
                    SkipWs();
                    if (_i >= _s.Length) throw new ParseException("fim inesperado no array");
                    if (_s[_i] == ',') { _i++; continue; }
                    if (_s[_i] == ']') { _i++; return l; }
                    throw new ParseException("',' ou ']' esperado na posicao " + _i);
                }
            }

            private string ParseString()
            {
                _i++; // opening quote
                var sb = new StringBuilder();
                while (true)
                {
                    if (_i >= _s.Length) throw new ParseException("string sem fechamento");
                    char c = _s[_i++];
                    if (c == '"') return sb.ToString();
                    if (c != '\\') { sb.Append(c); continue; }
                    if (_i >= _s.Length) throw new ParseException("escape incompleto");
                    char e = _s[_i++];
                    switch (e)
                    {
                        case '"': sb.Append('"'); break;
                        case '\\': sb.Append('\\'); break;
                        case '/': sb.Append('/'); break;
                        case 'n': sb.Append('\n'); break;
                        case 'r': sb.Append('\r'); break;
                        case 't': sb.Append('\t'); break;
                        case 'b': sb.Append('\b'); break;
                        case 'f': sb.Append('\f'); break;
                        case 'u':
                            if (_i + 4 > _s.Length) throw new ParseException("escape unicode incompleto");
                            sb.Append((char)int.Parse(_s.Substring(_i, 4), NumberStyles.HexNumber, CultureInfo.InvariantCulture));
                            _i += 4;
                            break;
                        default: throw new ParseException("escape invalido: \\" + e);
                    }
                }
            }

            private object ParseNumber()
            {
                int start = _i;
                if (_i < _s.Length && (_s[_i] == '-' || _s[_i] == '+')) _i++;
                bool isFloat = false;
                while (_i < _s.Length)
                {
                    char c = _s[_i];
                    if (c >= '0' && c <= '9') { _i++; continue; }
                    if (c == '.' || c == 'e' || c == 'E' || c == '+' || c == '-') { isFloat = true; _i++; continue; }
                    break;
                }
                if (_i == start) throw new ParseException("numero esperado na posicao " + start);
                string tok = _s.Substring(start, _i - start);
                if (!isFloat)
                {
                    long l;
                    if (long.TryParse(tok, NumberStyles.Integer, CultureInfo.InvariantCulture, out l)) return l;
                }
                double d;
                if (!double.TryParse(tok, NumberStyles.Float, CultureInfo.InvariantCulture, out d))
                    throw new ParseException("numero invalido: " + tok);
                if (double.IsNaN(d) || double.IsInfinity(d)) throw new ParseException("numero nao finito: " + tok);
                return d;
            }
        }

        public static Dictionary<string, object> TryParseObject(string text, out string error)
        {
            error = null;
            if (text == null) { error = "texto nulo"; return null; }
            try
            {
                var root = new Parser(text).ParseDocument();
                var obj = root as Dictionary<string, object>;
                if (obj == null) { error = "raiz nao e objeto"; return null; }
                return obj;
            }
            catch (Exception ex)
            {
                error = ex.GetType().Name + ": " + ex.Message;
                return null;
            }
        }
    }
}
