using System;
using System.Collections.Generic;
using Burst2Flame;
using HarmonyLib;

namespace RoguelikeDebugger.Patches
{
    /// <summary>
    /// Inventário completo de skills/spells do jogo (BT-7 · enriquecido no RV-8b-0).
    /// Patch no getter de Game.Skills: despeja a lista quando o tamanho estabilizar
    /// (o jogo popula incrementalmente durante o loading, como nos status).
    ///
    /// RV-8b-0: além do texto, despeja o que o jogo CALCULA — DescriptionExpressions
    /// (o array que o [N] do texto indexa em runtime), DamageExpressionOverrides,
    /// ActionsGranted, AttributeEffects e PassiveActionStatuses. Sem isso a revisão da
    /// tooltip vira leitura de prosa: não dá pra conferir se os NÚMEROS escritos no
    /// texto batem com a mecânica.
    ///
    /// FORMATO: os campos novos entram ANTES de desc=, porque tools/census.py casa
    /// "campo=valor" separado por "|" e precisa que desc= continue por ÚLTIMO. Nenhum
    /// valor pode conter "|" (o separador) nem aspas — por isso tudo passa por Limpa().
    /// </summary>
    [HarmonyPatch(typeof(Game), "get_Skills")]
    public static class SkillInventoryPatch
    {
        private static bool _dumped;
        private static int _lastCount = -1;
        private static int _stableHits;

        /// <summary>
        /// Normaliza um valor para caber no formato de uma linha do censo:
        /// sem quebra de linha, sem o separador '|' e sem aspas.
        /// </summary>
        private static string Limpa(string s)
        {
            return (s ?? "").Replace("\n", " ").Replace("\r", " ")
                            .Replace("|", "/").Replace("\"", "'").Trim();
        }

        /// <summary>Junta um array de strings já limpas, separando por ';'.</summary>
        private static string Junta(string[] itens)
        {
            if (itens == null)
            {
                return "";
            }
            var sb = new System.Text.StringBuilder();
            foreach (var i in itens)
            {
                if (!string.IsNullOrEmpty(i))
                {
                    sb.Append(Limpa(i)).Append("; ");
                }
            }
            return sb.ToString().TrimEnd(' ', ';');
        }

        private static void Postfix(List<SkillInfo> __result)
        {
            try
            {
                if (_dumped || __result == null || __result.Count <= 1)
                {
                    return;
                }

                // Estabilização: dump só quando o tamanho ficar igual por 5 acessos seguidos.
                if (__result.Count == _lastCount)
                {
                    _stableHits++;
                }
                else
                {
                    _stableHits = 1;
                    _lastCount = __result.Count;
                }
                if (_stableHits < 5)
                {
                    return;
                }
                _dumped = true;

                Plugin.Log.LogInfo($"[Skill] Inventário: {__result.Count} skills carregados.");
                foreach (var sk in __result)
                {
                    if (sk == null)
                    {
                        continue;
                    }
                    // Censo (RV-7): descricao COMPLETA. O corte em 110 chars existia para nao
                    // poluir o log, mas sem o texto inteiro o checklist de revisao nao serve.
                    var desc = sk.Description ?? "";

                    // O que a skill concede (nome do asset de cada ação).
                    var acts = new System.Text.StringBuilder();
                    if (sk.ActionsGranted != null)
                    {
                        foreach (var a in sk.ActionsGranted)
                        {
                            if (a != null && !string.IsNullOrEmpty(a.name))
                            {
                                acts.Append(Limpa(a.name)).Append("; ");
                            }
                        }
                    }

                    // Status que uma passiva aplica.
                    var pstat = new System.Text.StringBuilder();
                    if (sk.PassiveActionStatuses != null)
                    {
                        foreach (var ps in sk.PassiveActionStatuses)
                        {
                            if (ps != null && !string.IsNullOrEmpty(ps.Name))
                            {
                                pstat.Append(Limpa(ps.Name)).Append("; ");
                            }
                        }
                    }

                    // Efeitos de atributo: MESMO formato do dump de status (RV-9), para as
                    // duas categorias falarem a mesma lingua.
                    var ef = new System.Text.StringBuilder();
                    if (sk.AttributeEffects != null)
                    {
                        foreach (var e in sk.AttributeEffects)
                        {
                            if (e == null || e.CharacterAttribute == null)
                            {
                                continue;
                            }
                            ef.Append(e.CharacterAttribute.name).Append(':')
                              .Append(e.CharacterEffectMethod).Append(':')
                              .Append(e.Amount).Append(", ");
                        }
                    }

                    string tags = sk.SkillTags != null ? string.Join(",", sk.SkillTags) : "";
                    Plugin.Log.LogInfo(
                        $"[Skill] '{sk.SkillName}' | tipo={sk.SkillType} | dano={sk.DamageType} | " +
                        $"tier={sk.Tier} | tags={tags} | skid={sk.Guid} | " +
                        $"passivo={(sk.IsPassive ? "sim" : "nao")} | " +
                        $"attr={ef} | acts={acts} | pstat={pstat} | " +
                        $"expr={Junta(sk.DescriptionExpressions)} | " +
                        $"danoExpr={Junta(sk.DamageExpressionOverrides)} | " +
                        $"upg={Limpa(sk.UpgradeText)} | " +
                        $"desc=\"{desc.Replace("\n", " ")}\"");
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"[Skill] erro no inventário: {e.Message}");
            }
        }
    }
}
