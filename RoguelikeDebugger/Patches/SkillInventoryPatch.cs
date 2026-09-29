using System;
using System.Collections.Generic;
using System.Linq;
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
    /// RV-8b-0c: a fórmula de DANO não está na skill, está na AÇÃO que ela concede.
    /// Das 150 skills que usam *N no texto, 131 não têm danoExpr e só 2 não têm acts.
    /// Por isso este patch também despeja, uma vez por ação, os `GeneralEffect.Action`
    /// dela NA ORDEM — é esse array que o `*N` indexa (ver Tooltip.GetDamageString:
    /// `effects[int.Parse(texto[num+1, 1])]`, um dígito só, e o resultado é a faixa
    /// MIN-MAX de dano).
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

        /// <summary>Ações concedidas pelas skills (RV-8b-0c), por nome do asset.</summary>
        private static readonly Dictionary<string, ActionInfo> _acoes =
            new Dictionary<string, ActionInfo>();

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

        /// <summary>
        /// Despeja as ações concedidas pelas skills (RV-8b-0c). É aqui que vive a fórmula
        /// de dano: o `*N` do texto da skill vira `effects[N]`, e `effects` são os
        /// `GeneralEffect.Action` desta ação, na ordem do array (Depois o
        /// `DamageExpressionOverrides` sobrescreve por índice, se existir).
        /// </summary>
        private static void DespejaAcoes()
        {
            Plugin.Log.LogInfo($"[Action] Inventário: {_acoes.Count} ações concedidas por skills.");

            // O tooltip NÃO usa os efeitos da própria ação: se `TooltipDamageInfoRefAction`
            // estiver setado, é ELE que carrega a fórmula (Tooltip.GetDamageString, l.2222).
            // E a skill só olha a PRIMEIRA ação concedida (l.1443, ActionsGranted.First).
            // Por isso andamos a corrente de refs com uma fila, em vez de um foreach simples:
            // as ações-referência não são concedidas por ninguém e so apareceriam por acaso.
            var fila = new Queue<string>(_acoes.Keys.OrderBy(x => x, StringComparer.Ordinal));
            var vistos = new HashSet<string>();
            while (fila.Count > 0)
            {
                string nome = fila.Dequeue();
                if (!vistos.Add(nome))
                {
                    continue;
                }
                ActionInfo ac;
                if (!_acoes.TryGetValue(nome, out ac) || ac == null)
                {
                    continue;
                }

                var refAcao = ac.TooltipDamageInfoRefAction;
                var refStatus = ac.TooltipDamageInfoRefStatus;
                if (refAcao != null && !string.IsNullOrEmpty(refAcao.name))
                {
                    _acoes[refAcao.name] = refAcao;   // garante que o ref seja visitado
                    fila.Enqueue(refAcao.name);
                }

                // Efeitos próprios e efeitos da ação referenciada (o que o tooltip usa).
                string dono = EfeitosDe(ac);
                string refe = refAcao != null ? EfeitosDe(refAcao) : "";

                // A contagem que VALE para o `*N`: o tooltip filtra por TIPO e indexa o
                // array inteiro, incluindo as entradas de Action vazio (que EfeitosDe nao
                // lista). Contar errado aqui faz o censo acusar defeito que nao existe.
                int nDono = ContaEfeitos(ac);
                int nRef = refAcao != null ? ContaEfeitos(refAcao) : 0;

                Plugin.Log.LogInfo(
                    $"[Action] '{nome}' | dano={ac.DamageType} | " +
                    $"efeitos={dono} | refAcao={(refAcao != null ? Limpa(refAcao.name) : "")} | " +
                    $"efeitosRef={refe} | " +
                    $"nEfeitos={nDono} | nEfeitosRef={nRef} | " +
                    $"refStatus={(refStatus != null ? Limpa(refStatus.Name) : "")} | " +
                    $"danoExpr={Junta(ac.DamageExpressionOverrides)} | " +
                    $"expr={Junta(ac.DescriptionExpressions)} | " +
                    $"desc=\"{Limpa(ac.Description)}\"");
            }
        }

        /// <summary>
        /// Quantos GeneralEffect a ação tem. É ESTA a contagem que vale para o `*N`: o
        /// tooltip filtra por tipo e indexa o array inteiro, incluindo entradas de
        /// `Action` vazio (que o EfeitosDe não lista).
        /// </summary>
        private static int ContaEfeitos(ActionInfo ac)
        {
            int n = 0;
            if (ac != null && ac.Effects != null)
            {
                foreach (var e in ac.Effects)
                {
                    if (e is GeneralEffect)
                    {
                        n++;
                    }
                }
            }
            return n;
        }

        /// <summary>
        /// Os `GeneralEffect.Action` de uma ação, NA ORDEM do array: é exatamente o que o
        /// `*N` do texto indexa (`effects[N]` em Tooltip.GetDamageString).
        /// </summary>
        private static string EfeitosDe(ActionInfo ac)
        {
            var sb = new System.Text.StringBuilder();
            if (ac != null && ac.Effects != null)
            {
                foreach (var e in ac.Effects)
                {
                    var ge = e as GeneralEffect;
                    if (ge != null && !string.IsNullOrEmpty(ge.Action))
                    {
                        sb.Append(Limpa(ge.Action)).Append("; ");
                    }
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
                                _acoes[a.name] = a;   // RV-8b-0c: a fórmula do dano mora aqui
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

                // Depois das skills, as ações que elas concedem (RV-8b-0c).
                DespejaAcoes();
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"[Skill] erro no inventário: {e.Message}");
            }
        }
    }
}
