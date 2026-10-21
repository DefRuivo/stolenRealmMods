using System;
using System.Collections.Generic;
using HarmonyLib;
using TMPro;
using BepInEx.Logging;

namespace BetterPortuguese.Runtime
{
    /// <summary>
    /// Tradução das LINHAS DE EFEITO dos eventos (o "★ Reroll a skill" embaixo de cada opção).
    ///
    /// Por que existe: essas linhas não passam por `OptionsManager.Localize`. O texto vem do
    /// próprio asset do evento (`EventAction`/`EventOption`) e é escrito direto no TMP por
    /// `EventOptionSelectionItem.PopulateResultEffects` e `EventResultEffect.SetEventAction`.
    /// Resultado: mesmo com a localização pt-BR correta no banco, a linha sai em inglês.
    ///
    /// O patch só troca o TEXTO EXIBIDO, por correspondência exata: nada de heurística, nada de
    /// substituição parcial que possa comer nome de skill. String desconhecida é registrada uma vez
    /// (quando `Diagnostico=true`) para a tabela crescer com evidência — nunca inventada.
    /// </summary>
    internal static class EventEffectText
    {
        private static readonly Dictionary<string, string> Fixes = new Dictionary<string, string>(StringComparer.Ordinal)
        {
            ["Reroll a skill"] = "Role novamente uma habilidade",
            ["Level up Fortunes"] = "Aumente o nível das suas Fortunas",
        };

        // Textos de botao/rotulo que o jogo escreve com chave propria e que continuam em ingles na
        // tela (o funil de localizacao nao devolve a entrada pt-BR para elas). Correspondencia EXATA.
        private static readonly Dictionary<string, string> Baloes = new Dictionary<string, string>(StringComparer.Ordinal)
        {
            ["Battle"] = "Batalhar",
            ["Hard Battle"] = "Batalha Difícil",
            ["Rest"] = "Descanso",
        };

        private static ManualLogSource _log;
        private static bool _diag;
        private static readonly HashSet<string> _seen = new HashSet<string>(StringComparer.Ordinal);

        public static void Install(Harmony harmony, Func<bool> diagnostico, ManualLogSource log)
        {
            _log = log;
            try
            {
                harmony.Patch(
                    AccessTools.Method(typeof(EventOptionSelectionItem), nameof(EventOptionSelectionItem.PopulateResultEffects)),
                    postfix: new HarmonyMethod(AccessTools.Method(typeof(EventEffectText), nameof(AfterPopulate))));
                // Alguns ações são preenchidas fora do Populate; o setter é o segundo caminho.
                harmony.Patch(
                    AccessTools.Method(typeof(EventResultEffect), nameof(EventResultEffect.SetEventAction)),
                    postfix: new HarmonyMethod(AccessTools.Method(typeof(EventEffectText), nameof(AfterSetAction))));
                harmony.Patch(
                    AccessTools.Method(typeof(NavNodeVotingButton), "set_NodeType"),
                    postfix: new HarmonyMethod(AccessTools.Method(typeof(EventEffectText), nameof(AfterNodeType))));
                _diag = diagnostico?.Invoke() ?? false;
                log?.LogInfo("BetterPortuguese: traducao das linhas de efeito de evento registrada (" + Fixes.Count + " regras).");
            }
            catch (Exception ex)
            {
                log?.LogWarning("BetterPortuguese: linhas de efeito de evento NAO traduzidas: " + ex.GetType().Name + ": " + ex.Message);
            }
        }

        private static void AfterPopulate(EventOptionSelectionItem __instance)
        {
            try
            {
                Apply(__instance.SingleActionEffectText);
                Apply(__instance.SuccessEffectText);
                Apply(__instance.FailureEffectText);
            }
            catch (Exception ex) { _log?.LogWarning("BetterPortuguese: efeito de evento preservado: " + ex.GetType().Name); }
        }

        private static void AfterSetAction(EventResultEffect __instance)
        {
            try { Apply(__instance); }
            catch (Exception ex) { _log?.LogWarning("BetterPortuguese: efeito de evento preservado: " + ex.GetType().Name); }
        }

        private static void AfterNodeType(NavNodeVotingButton __instance)
        {
            try
            {
                if (__instance == null || __instance.NodeTypeText == null) return;
                string atual = __instance.NodeTypeText.text;
                if (string.IsNullOrEmpty(atual)) return;
                if (Baloes.TryGetValue(atual, out var traduzido)) { __instance.NodeTypeText.text = traduzido; return; }
                if (_diag && _seen.Add("nav:" + atual)) _log?.LogInfo("BP-TEXTO: rotulo de no sem traducao: '" + atual + "'");
            }
            catch (Exception ex) { _log?.LogWarning("BetterPortuguese: rotulo de no preservado: " + ex.GetType().Name); }
        }

        private static void Apply(EventResultEffect effect)
        {
            TMP_Text text = effect != null ? effect.EffectText : null;
            if (text == null || string.IsNullOrEmpty(text.text)) return;
            string atual = text.text;
            if (Fixes.TryGetValue(atual, out var traduzido))
            {
                text.text = traduzido;
                return;
            }
            if (_diag && _seen.Add(atual))
                _log?.LogInfo("BP-EVENTO: linha sem traducao: '" + atual + "'");
        }
    }
}
