using System;
using System.Collections.Generic;

namespace BetterPortuguese.Core
{
    /// <summary>
    /// Tabela de concordância do texto flutuante de status ("[status name] Aplicado").
    /// Fecha por padrão: só os nomes listados em <see cref="Feminine"/> mudam; todo o resto
    /// (nome desconhecido, markup inesperado, formato diferente) volta intacto.
    ///
    /// Origem do texto: Character::ShowOverheadMessageStatus chama
    /// OptionsManager.Localize("[status name] Applied", LanguageGender.None, Gender.None) e concatena
    /// o nome ao sufixo antes de GameLogic::OverheadMessage — o call site passa None, então preencher
    /// Feminine no dicionário seria inerte (SR-QA-09).
    /// </summary>
    internal static class StatusAgreement
    {
        internal const string MasculineSuffix = " Aplicado";
        internal const string FeminineSuffix = " Aplicada";

        /// <summary>
        /// Nomes PT-BR com núcleo feminino verificados em texto flutuante real (runs 01-06 da bancada
        /// 26878331, 154 ocorrências). Não acrescentar nome sem confirmação em jogo: falso positivo
        /// troca texto que estava correto.
        /// </summary>
        internal static readonly HashSet<string> Feminine = new HashSet<string>(StringComparer.Ordinal)
        {
            "Resistência ao Controle",
            "Proteção Elemental",
            "Terra Ardente",
            "Terra Sagrada",
            "Fúria de Batalha",
            "Maldição",
            "Fratura",
            "Nuvem de Fumaça",
            "Aura do Conquistador",
            "Aura de Energia",
            "Aura do Xamã"
        };

        /// <summary>
        /// Devolve o texto corrigido ou o próprio <paramref name="incoming"/> quando não há
        /// correspondência segura. Nunca lança para texto bem formado; <paramref name="reason"/>
        /// descreve o caminho tomado (usado só para log deduplicado).
        /// </summary>
        internal static string Compose(string incoming, out string reason)
        {
            reason = null;
            if (incoming == null) { reason = "texto nulo"; return null; }
            if (incoming.Length < MasculineSuffix.Length) { reason = "curto demais"; return incoming; }

            int closeLen = TrailingClosingTags(incoming);
            int bodyLen = incoming.Length - closeLen;
            if (bodyLen < MasculineSuffix.Length ||
                string.CompareOrdinal(incoming, bodyLen - MasculineSuffix.Length, MasculineSuffix, 0, MasculineSuffix.Length) != 0)
            { reason = "sem sufixo ' Aplicado' no fim"; return incoming; }

            string body = incoming.Substring(0, bodyLen - MasculineSuffix.Length);
            string tail = closeLen == 0 ? string.Empty : incoming.Substring(bodyLen);

            int openLen = LeadingOpeningTags(body);
            string open = body.Substring(0, openLen);
            string rest = body.Substring(openLen);

            // " x2" (ou " x12") fica ENTRE o nome e o sufixo; preservado na posição original.
            string stack = string.Empty;
            int digits = rest.Length;
            while (digits > 0 && rest[digits - 1] >= '0' && rest[digits - 1] <= '9') digits--;
            if (digits < rest.Length && digits >= 2 &&
                rest[digits - 2] == ' ' && (rest[digits - 1] == 'x' || rest[digits - 1] == 'X'))
            { stack = rest.Substring(digits - 2); rest = rest.Substring(0, digits - 2); }

            // Qualquer markup remanescente no meio = formato não previsto: não tocar.
            if (rest.IndexOf('<') >= 0 || rest.IndexOf('>') >= 0) { reason = "markup interna"; return incoming; }

            if (!Feminine.Contains(rest)) { reason = "nome fora da tabela"; return incoming; }

            reason = "feminino:" + rest;
            return open + rest + stack + FeminineSuffix + tail;
        }

        /// <summary>Comprimento das tags de fechamento contíguas no fim ("&lt;/color&gt;&lt;/b&gt;").</summary>
        private static int TrailingClosingTags(string text)
        {
            int len = 0;
            while (len < text.Length && text[text.Length - 1 - len] == '>')
            {
                int start = text.LastIndexOf('<', text.Length - 1 - len);
                if (start < 0) break;
                string tag = text.Substring(start, text.Length - len - start);
                if (!tag.StartsWith("</", StringComparison.Ordinal) || tag.Length < 4) break;
                len += tag.Length;
            }
            return len;
        }

        /// <summary>Comprimento das tags de abertura contíguas no início ("&lt;color=#00FFFF&gt;").</summary>
        private static int LeadingOpeningTags(string text)
        {
            int len = 0;
            while (len < text.Length && text[len] == '<')
            {
                int end = text.IndexOf('>', len + 1);
                if (end < 0 || end + 1 <= len + 1) break;
                len = end + 1;
            }
            return len;
        }
    }
}
