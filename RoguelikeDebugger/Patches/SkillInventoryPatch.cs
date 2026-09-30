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
                    $"nSummons={(ac.Summons == null ? -1 : ac.Summons.Count)} | " +
                    $"refStatus={(refStatus != null ? Limpa(refStatus.Name) : "")} | " +
                    $"danoExpr={Junta(ac.DamageExpressionOverrides)} | " +
                    $"expr={Junta(ac.DescriptionExpressions)} | " +
                    $"desc=\"{Limpa(ac.Description)}\"");

                // RV-8b-0f: PROPRIEDADES DA AÇÃO. A tooltip mostra dano/efeito, mas omite
                // limite de alvos, alcance, knockback, nº de golpes, cooldown e chance de
                // proc - que é a classe de dúvida que sobrou no Ranger (`Rally` +3 x +2,
                // `Volley` 5 x 3 alvos). O `RangeAdderAttributes` que eu tinha anotado no
                // quadro NÃO é campo público do ActionInfo: é um Dictionary privado do
                // `ActionProperties` (l.317488, já convertido em CacheAttributeName) - o
                // "alcance por hex" que interessa chega por ATRIBUTO (`Patient Hunter` dá
                // `RangeTypeAdderRanged`), e isso o campo `attr` do dump já cobre.
                var alvos = new System.Text.StringBuilder();
                int nAlvos = 0;
                if (ac.Targets != null)
                {
                    foreach (var t in ac.Targets)
                    {
                        var ti = t as TargetInfo;
                        if (ti == null)
                        {
                            continue;
                        }
                        nAlvos++;
                        alvos.Append('[')
                             .Append("sel=").Append(Limpa(ti.Selection)).Append(';')
                             .Append("rsel=").Append(Limpa(ti.RangeSelection)).Append(';')
                             .Append("blast=").Append(Limpa(ti.BlastRange)).Append(';')
                             .Append("range=").Append(ti.SimpleRange).Append(';')
                             .Append("ali=").Append(ti.TargetAllies ? 1 : 0)
                             .Append("ini=").Append(ti.TargetEnemies ? 1 : 0)
                             .Append("self=").Append(ti.TargetSelf ? 1 : 0).Append(']');
                    }
                }

                var chances = new System.Text.StringBuilder();
                if (ac.ActionChances != null)
                {
                    foreach (var ch in ac.ActionChances)
                    {
                        if (ch != null)
                        {
                            chances.Append(ch.ActionInfo != null ? Limpa(ch.ActionInfo.name) : "?")
                                   .Append(':').Append(ch.Chance).Append(',');
                        }
                    }
                }

                // Status que a acao APLICA (RV-8b-0f). Sem isto o `Rally` fica indecidivel:
                // a acao dele tem nEfeitos=0 e o "+3 de movimento" que o texto promete mora
                // num ActionStatusInfo, nao num GeneralEffect. O valor em si esta no status
                // (coluna `attr` do status.csv), entao aqui basta o NOME para ligar um ao
                // outro. `SourceStatusEffects` sao os aplicados em quem usa a acao.
                var statusAplic = new System.Text.StringBuilder();
                if (ac.StatusEffects != null)
                {
                    foreach (var st in ac.StatusEffects)
                    {
                        if (st != null)
                        {
                            statusAplic.Append(Limpa(st.Name)).Append(',');
                        }
                    }
                }
                var statusFonte = new System.Text.StringBuilder();
                if (ac.SourceStatusEffects != null)
                {
                    foreach (var st in ac.SourceStatusEffects)
                    {
                        if (st != null)
                        {
                            statusFonte.Append(Limpa(st.Name)).Append(',');
                        }
                    }
                }

                Plugin.Log.LogInfo(
                    $"[ActionProps] '{nome}' | tipo={ac.ActionType} | beneficio={ac.BenefitType} | " +
                    $"skillType={ac.SkillType} | nAlvos={nAlvos} | alvos={alvos} | " +
                    $"alcance={(ac.UseMaxRangeOverride ? ac.MaxRangeOverride.ToString() : "-")} | " +
                    $"alcanceBlast={(ac.UseMaxRangeBlastOverride ? ac.MaxRangeBlastOverride.ToString() : "-")} | " +
                    $"knockback={(ac.UseKnockback ? ac.KnockbackAmount.ToString() : "-")} | " +
                    $"hits={(ac.UseMultipleHits ? ac.NumHits.ToString() : "-")} | " +
                    // Campos do `ActionInfo` que eu nao despejava e que resolvem casos concretos
                    // do Monk: DashMaxChainCount e o TETO da serie de golpes (padrao 1, e o
                    // codigo para a corrente em `ChainCount < BaseAction.DashMaxChainCount`);
                    // KnockbackCollideAction e o "any enemy hit by the target also receives
                    // damage" dos chutes de knockback; ActivationIndicatorHexes pode ser a area
                    // das skills self-cast (Cyclone Kick 4 / Quaking Fist 3).
                    $"maxChain={ac.DashMaxChainCount} | " +
                    $"colisao={(ac.KnockbackCollideAction != null ? ac.KnockbackCollideAction.name : "-")} | " +
                    $"hexesAtiv={(string.IsNullOrEmpty(ac.ActivationIndicatorHexes) ? "-" : ac.ActivationIndicatorHexes.Replace('\n', ','))} | " +
                    $"numHitsEq={(ac.UseNumHitsEquation ? "Sim" : "-")} | " +
                    // A corrente de PROJETIL (a `Chain Lightning`): quantos saltos, qual a
                    // regra do proximo alvo e, o que o texto nao diz, se o MESMO alvo pode ser
                    // atingido de novo (`ChainSameTarget` e true por padrao).
                    $"chainProj={(ac.ProjectileChain ? "Sim" : "Nao")} | " +
                    $"chainProjN={ac.ProjectileChainCount} | " +
                    $"chainProjAlvo={Limpa(ac.ProjectileChainTarget)} | " +
                    $"chainMesmo={ac.ChainSameTarget} | " +
                    // Os DOIS campos que fecham casos concretos que ficaram abertos:
                    // (a) `DashChainTarget` - a string que escolhe os alvos da corrente. E o
                    //     candidato ao raio do PUXAO do `Cyclone Kick` ("pulls enemies within
                    //     4 hexes"), que nao esta em `alcanceHits` (la vem "1") nem no
                    //     `knockback` (vem "-"): o puxao usa a maquinaria da corrente de dash.
                    // (b) `StatusRemovals[].ActionOnRemoval` - a acao disparada POR status
                    //     removido, onde mora o "10% da vida maxima" do `Soul Cleanse`. Uso o
                    //     `EfeitosDe` que ja existe para ler as expressoes dela.
                    $"chainAlvo={Limpa(ac.DashChainTarget)} | " +
                    $"chainMesmoAlvo={(ac.DashChainSameTarget ? "Sim" : "Nao")} | " +
                    $"remocoes={(ac.StatusRemovals == null ? 0 : ac.StatusRemovals.Length)} | " +
                    $"remocoesP={(ac.PostActionStatusRemovals == null ? 0 : ac.PostActionStatusRemovals.Length)} | " +
                    $"remocao={(ac.StatusRemovals != null && ac.StatusRemovals.Length > 0 && ac.StatusRemovals[0].ActionOnRemoval != null ? Limpa(ac.StatusRemovals[0].ActionOnRemoval.name) + "=>" + EfeitosDe(ac.StatusRemovals[0].ActionOnRemoval) : "-")} | " +
                    $"remocaoTipo={(ac.StatusRemovals != null && ac.StatusRemovals.Length > 0 ? ac.StatusRemovals[0].BenefitType.ToString() + "/" + Limpa(ac.StatusRemovals[0].NumStatusesToRemove) : "-")} | " +
                    $"exprHits={Limpa(ac.NumHitsEquation)} | alcanceHits={Limpa(ac.MultipleHitRange)} | " +
                    $"cooldown={Limpa(ac.Cooldown)} | cargas={Limpa(ac.MaxCharges)}/{Limpa(ac.InitialCharges)} | " +
                    $"precisa={Limpa(ac.UseCondition)} | condFalha={Limpa(ac.UseConditionFailText)} | " +
                    $"statusAplicados={statusAplic} | statusFonte={statusFonte} | chances={chances}");

                // RV-8b-2h: INVOCAÇÕES. A tooltip de "Nature Summoning I" diz apenas
                // "Summons a Raven, Coyote, or Raccoon to fight for you." - não diz o que
                // cada bicho faz. Os dados existem no asset: ActionInfo.Summons é a lista
                // de CharacterInfo e cada CharacterInfo tem a List<SkillInfo> Skills com
                // as habilidades dele. As flags (sorteio/herda stats/morre com o caster)
                // explicam a mecânica que a tooltip também omite.
                if (ac.Summons != null && ac.Summons.Count > 0)
                {
                    var criaturas = new System.Text.StringBuilder();
                    foreach (var c in ac.Summons)
                    {
                        if (c == null)
                        {
                            continue;
                        }
                        criaturas.Append(Limpa(c.name)).Append('[');
                        // As habilidades do bicho invocado vêm em SkillsAndAI[].Skill; a
                        // List<SkillInfo> Skills costuma vir VAZIA nos summons (por isso as
                        // duas são tentadas, com a segunda só como reserva).
                        int nHab = 0;
                        if (c.SkillsAndAI != null)
                        {
                            foreach (var sa in c.SkillsAndAI)
                            {
                                if (sa != null && sa.Skill != null &&
                                    !string.IsNullOrEmpty(sa.Skill.SkillName))
                                {
                                    criaturas.Append(Limpa(sa.Skill.SkillName)).Append(',');
                                    nHab++;
                                }
                            }
                        }
                        if (nHab == 0 && c.Skills != null)
                        {
                            foreach (var sk in c.Skills)
                            {
                                if (sk != null && !string.IsNullOrEmpty(sk.SkillName))
                                {
                                    criaturas.Append(Limpa(sk.SkillName)).Append(',');
                                }
                            }
                        }
                        criaturas.Append("]; ");
                    }
                    Plugin.Log.LogInfo(
                        $"[Summon] '{nome}' | sorteio={(ac.RandomSummonFromList ? "sim" : "nao")} | " +
                        $"herdaStats={(ac.BenefitFromCasterStats ? "sim" : "nao")} | " +
                        $"morreComCaster={(ac.DieWhenCasterDies ? "sim" : "nao")} | " +
                        $"persistente={(ac.IsPersistantSummon ? "sim" : "nao")} | " +
                        $"doencaDeInvocacao={(ac.HasSummoningSickness ? "sim" : "nao")} | " +
                        $"criaturas={criaturas}");
                }
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

                    // RV-8b-0f: GATILHOS. A dúvida do `Marked Prey` ("Attacks" x "Basic
                    // attacks") se decide aqui: `TriggerType` diz QUANDO dispara e
                    // `AddBasicAttackToActionList` diz se ataque básico conta. Não existe
                    // um valor `OnBasicAttack` no enum (são 29 valores, de OnHittingAny a
                    // OnGettingHitAnyIncludingProcs) - quem responde é este par. Sem isso a
                    // tooltip pode prometer mais do que o jogo faz.
                    if (sk.SkillTriggers != null)
                    {
                        foreach (var tg in sk.SkillTriggers)
                        {
                            if (tg == null)
                            {
                                continue;
                            }
                            var acoesTg = new System.Text.StringBuilder();
                            if (tg.Actions != null)
                            {
                                foreach (var a in tg.Actions)
                                {
                                    if (a != null && !string.IsNullOrEmpty(a.name))
                                    {
                                        acoesTg.Append(Limpa(a.name)).Append(',');
                                        // RV-8b-2e: ação concedida por GATILHO não está em
                                        // ActionsGranted, então nunca entrava no inventário de
                                        // ações - e o valor que a tooltip promete mora nela
                                        // (`Natural Selection` promete 5% de vida máxima, e o
                                        // `Natural Succession Proc` não existe no assembly).
                                        _acoes[a.name] = a;
                                    }
                                }
                            }
                            var statusTg = new System.Text.StringBuilder();
                            if (tg.ActionStatuses != null)
                            {
                                foreach (var st in tg.ActionStatuses)
                                {
                                    if (st != null)
                                    {
                                        statusTg.Append(Limpa(st.Name)).Append(',');
                                    }
                                }
                            }
                            Plugin.Log.LogInfo(
                                $"[Trigger] '{sk.SkillName}' | tipo={tg.TriggerType} | " +
                                $"cond={Limpa(tg.Condition)} | addBasicAttack={(tg.AddBasicAttackToActionList ? "sim" : "nao")} | " +
                                $"garanteUm={(tg.GauranteeOneAction ? "sim" : "nao")} | " +
                                $"chanceIgual={(tg.GiveAllActionsEqualChance ? "sim" : "nao")} | " +
                                $"chances={Junta(tg.ActionChanceEquations)} | acoes={acoesTg} | " +
                                $"status={statusTg} | chancesStatus={Junta(tg.ActionStatusChanceEquations)} | " +
                                $"nEfeitos={(tg.GeneralEffects == null ? 0 : tg.GeneralEffects.Length)} | " +
                                // O cooldown PROPRIO do trigger: e ele que vale no caminho de proc
                                // (`TriggerCooldownDict[trigger] = trigger.Cooldown`), nao o da acao.
                                // O `Calculated Risk` cita "1 turn cooldown" no texto e a acao `Evasion`
                                // dele tem cooldown=3 - este campo desempata.
                                $"cooldownTrig={tg.Cooldown}");
                        }
                    }
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
