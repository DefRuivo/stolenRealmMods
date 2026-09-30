using System;
using System.Collections.Generic;
using System.Reflection;
using System.Text;
using Burst2Flame;

namespace RoguelikeDebugger
{
    /// <summary>
    /// RV-8b-0g: descreve arrays de efeito pelo TIPO CONCRETO de cada elemento.
    ///
    /// MOTIVO: `ActionStatusInfo.Effects` e `ActionInfo.Effects` sao `IEffectInfo[]`
    /// (interface VAZIA - l.322255 do decompilado) e o dump antigo fazia
    /// `e as GeneralEffect` para ler o campo `Action`. Em todo elemento cujo tipo concreto
    /// NAO seja `GeneralEffect` esse cast devolve null e o dado desaparecia do dump - foi o
    /// que deixou 2 entradas do censo de tooltips como "indeterminado".
    ///
    /// A montagem tem DUAS implementacoes da interface:
    ///   - `GeneralEffect`              (l.322250): { string Action; }
    ///   - `CharacterVariableEffectInfo` (l.320295): { EffectTarget EffectTarget;
    ///                                                   CharacterVariableAttribute CharacterVariableAttribute;
    ///                                                   string Amount; }
    ///
    /// Por isso aqui a leitura e por REFLEXAO, e nao por cast: (a) cobre os dois tipos sem
    /// referenciar cada um, (b) publica o NOME do tipo concreto de cada elemento (o dado que
    /// responde "de que tipo era o efeito que sumia") e (c) se uma versao futura do jogo
    /// adicionar um terceiro tipo, ele aparece no dump sem recompilar o mod.
    ///
    /// Vale para QUALQUER array (`IEffectInfo[]`, `GeneralEffect[]`, `CharacterEffectInfo[]`),
    /// porque o parametro e `System.Array`.
    ///
    /// REGRA DO PROJETO: nada de valor inventado - tudo o que sai daqui e lido do objeto do
    /// jogo. Nenhum valor pode conter '|' (separador dos campos do censo), aspas ou quebra de
    /// linha: tudo passa por <see cref="Limpa"/>.
    /// </summary>
    internal static class EfeitosInfo
    {
        /// <summary>Quantos elementos de cada tipo concreto ja foram vistos (resumo do dump).</summary>
        private static readonly Dictionary<string, int> Contagem = new Dictionary<string, int>();

        private static int _total;
        private static int _naoGeneralEffect;

        /// <summary>Zera os contadores (o resumo e por categoria de dump).</summary>
        public static void Zerar()
        {
            Contagem.Clear();
            _total = 0;
            _naoGeneralEffect = 0;
        }

        /// <summary>
        /// Linha de resumo do que passou pelo <see cref="Descreve"/> desde o ultimo Zerar():
        /// quantos elementos no total, quantos de CADA tipo concreto e quantos NAO eram
        /// `GeneralEffect` (ou seja: quantos o cast antigo descartava). E a prova, no log, de
        /// que existe elemento de outro tipo.
        /// </summary>
        public static string Resumo()
        {
            var sb = new StringBuilder();
            sb.Append("total=").Append(_total);
            sb.Append(" | porTipo={");
            bool primeiro = true;
            // ordem estavel (Dictionary nao garante ordem de iteracao)
            var chaves = new List<string>(Contagem.Keys);
            chaves.Sort(StringComparer.Ordinal);
            foreach (var k in chaves)
            {
                if (!primeiro)
                {
                    sb.Append("; ");
                }
                primeiro = false;
                sb.Append(k).Append('=').Append(Contagem[k]);
            }
            sb.Append("}");
            sb.Append(" | naoGeneralEffect=").Append(_naoGeneralEffect);
            return sb.ToString();
        }

        /// <summary>Quantos elementos o array tem (0 se for null).</summary>
        public static int Conta(Array arr)
        {
            return arr == null ? 0 : arr.Length;
        }

        /// <summary>
        /// Descreve o array NA ORDEM: `indice:TipoConcreto{campo=valor; ...}; ...`.
        /// String vazia quando o array e null ou esta vazio (mesma convencao dos outros campos
        /// vazios do dump). Nunca lanca: um campo que explodir sai como `Nome=&lt;erro&gt;`,
        /// para o dump continuar de pe.
        /// </summary>
        public static string Descreve(Array arr)
        {
            return DescreveCore(arr, false);
        }

        /// <summary>
        /// Descreve um `IEffectInfo[]` (`ActionStatusInfo.Effects` / `ActionInfo.Effects`):
        /// e o array que o cast `as GeneralEffect` percorria, entao AQUI cada elemento que
        /// nao seja `GeneralEffect` entra na conta de `naoGeneralEffect` (o defeito antigo).
        /// </summary>
        public static string Descreve(IEffectInfo[] arr)
        {
            return DescreveCore(arr, true);
        }

        private static string DescreveCore(Array arr, bool origemIEffectInfo)
        {
            if (arr == null || arr.Length == 0)
            {
                return "";
            }
            var sb = new StringBuilder();
            for (int i = 0; i < arr.Length; i++)
            {
                object o;
                try
                {
                    o = arr.GetValue(i);
                }
                catch (Exception e)
                {
                    o = null;
                    sb.Append(i).Append(":<erro:").Append(e.GetType().Name).Append(">; ");
                    continue;
                }
                sb.Append(i).Append(':').Append(Um(o, origemIEffectInfo)).Append("; ");
            }
            return sb.ToString().TrimEnd(' ', ';');
        }

        /// <summary>Um elemento: `Tipo{campo=valor; ...}`.</summary>
        private static string Um(object o, bool origemIEffectInfo)
        {
            if (o == null)
            {
                Contagem["null"] = Contagem.TryGetValue("null", out var vn) ? vn + 1 : 1;
                _total++;
                return "null";
            }

            Type t = o.GetType();
            string nome = t.Name;
            Contagem[nome] = Contagem.TryGetValue(nome, out var v) ? v + 1 : 1;
            _total++;
            if (origemIEffectInfo && !(o is GeneralEffect))
            {
                // O contador do defeito: quem o cast antigo (`as GeneralEffect`) perdia.
                // So conta em array IEffectInfo[] - `CharacterEffectInfo[]` e `GeneralEffect[]`
                // sao de tipo CONCRETO e nunca passaram por cast nenhum.
                _naoGeneralEffect++;
            }

            FieldInfo[] campos;
            try
            {
                campos = t.GetFields(BindingFlags.Public | BindingFlags.Instance);
            }
            catch (Exception)
            {
                campos = new FieldInfo[0];
            }
            Array.Sort(campos, (a, b) => string.CompareOrdinal(a.Name, b.Name));

            var sb = new StringBuilder();
            sb.Append(nome).Append('{');
            bool primeiro = true;
            foreach (var f in campos)
            {
                if (f.IsStatic)
                {
                    continue;
                }
                object valor;
                try
                {
                    valor = f.GetValue(o);
                }
                catch (Exception e)
                {
                    valor = "<erro:" + e.GetType().Name + ">";
                }
                if (!primeiro)
                {
                    sb.Append(';');
                }
                primeiro = false;
                sb.Append(f.Name).Append('=').Append(Valor(valor));
            }
            sb.Append('}');
            return sb.ToString();
        }

        /// <summary>Valor de um campo, em texto: asset do jogo vira o NOME do asset.</summary>
        private static string Valor(object v)
        {
            if (v == null)
            {
                return "-";
            }

            var uo = v as UnityEngine.Object;
            if (uo != null)
            {
                // `!= null` aqui e o operador da Unity (asset destruido conta como null)
                return Limpa(uo.name);
            }

            var s = v as string;
            if (s != null)
            {
                return s.Length == 0 ? "-" : Limpa(s);
            }

            var arr = v as Array;
            if (arr != null)
            {
                return "[" + arr.Length + "]";
            }

            return Limpa(v.ToString());
        }

        /// <summary>
        /// Normaliza um valor para caber numa linha de dump: sem quebra de linha, sem o
        /// separador '|' e sem aspas (mesmas regras do Limpa() dos patches).
        /// </summary>
        public static string Limpa(string s)
        {
            return (s ?? "").Replace("\n", " ").Replace("\r", " ")
                            .Replace("|", "/").Replace("\"", "'").Trim();
        }
    }
}
