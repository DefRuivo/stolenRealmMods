using System;
using System.Collections.Generic;
using Burst2Flame;
using HarmonyLib;

namespace RoguelikeDebugger.Patches
{
    /// <summary>
    /// Inventário completo de status/efeitos do jogo (BT-6).
    /// O setter de Game.ActionStatuses é chamado uma única vez com lista VAZIA
    /// (o jogo popula via Add no getter), então patchamos o GETTER: na primeira
    /// vez em que a lista estiver populada, despeja o inventário completo.
    /// </summary>
    [HarmonyPatch(typeof(Game), "get_ActionStatuses")]
    public static class ActionStatusInventoryPatch
    {
        private static bool _dumped;
        private static int _lastCount = -1;
        private static int _stableHits;

        /// <summary>
        /// Os gatilhos de um status (RV-8b-0g + RD-2). `ActionStatusInfo.SkillTriggers` e
        /// `SkillTrigger[]` e `SkillTrigger.GeneralEffects` e `GeneralEffect[]` - array
        /// CONCRETO (l.45797 do decompilado), entao NESTE caminho o cast nao falha: o que
        /// faltava era o campo sair no dump. Caso aberto que isto fecha: o `Dwarven Aura`,
        /// cujo stun nao esta em nenhuma acao do status.
        ///
        /// RD-2 - DUAS COISAS QUE FALTAVAM AQUI:
        /// (a) `SkillTrigger.Targets` (l.46590: `[TextArea] public string Targets;`). A nota
        ///     antiga do projeto dizia que `SkillTrigger` NAO tinha esse campo; ele existe, e
        ///     e ELE que fecha a pergunta aberta das auras de shrine (RV-19, secao 7): lido do
        ///     asset (resources.assets), o `Flame Shrine Aura` (pathID 2543240) tem
        ///     `SkillTriggers[0].Targets = "Cell.IsCurrentHex(Target)"` com `TriggerType=1` e
        ///     `Condition="Source.IsEnemy(Target)"`, e o `Decay Shrine Aura` (2543234) tem
        ///     `"Cell.IsCurrentHex(Source)"` com `TriggerType=4`. Nao passa por `ActionsOnTick`.
        /// (b) as ACOES do gatilho saem com os PROPRIOS efeitos (`Nome{ef=...}`): acao de
        ///     gatilho nao e concedida por skill, entao nunca entra no inventario `[Action]` -
        ///     era por isso que a formula que executa o proc das auras (`Flame Aura Proc` /
        ///     `Decay Aura Proc`, pathIDs 2544297/2544288) nao existia em lugar nenhum do
        ///     dump (RV-19, secao 7).
        /// Formato: indice:Tipo[ef=...~cond=...~status=...~alvos=...~acoes=...~chances=...~cd=...]; ...
        /// </summary>
        private static string TriggersDe(ActionStatusInfo s)
        {
            if (s == null || s.SkillTriggers == null || s.SkillTriggers.Length == 0)
            {
                return "";
            }
            var sb = new System.Text.StringBuilder();
            foreach (var tg in s.SkillTriggers)
            {
                if (tg == null)
                {
                    continue;
                }
                var stt = new System.Text.StringBuilder();
                if (tg.ActionStatuses != null)
                {
                    foreach (var st in tg.ActionStatuses)
                    {
                        if (st != null)
                        {
                            stt.Append(EfeitosInfo.Limpa(st.Name)).Append(',');
                        }
                    }
                }
                // RD-2: as acoes que o gatilho dispara, com os efeitos delas (a formula mora
                // no `Effects[]` da ACAO; `Descreve` le o array `IEffectInfo[]` por reflexao e
                // publica o tipo concreto de cada elemento).
                var acs = new System.Text.StringBuilder();
                if (tg.Actions != null)
                {
                    foreach (var ac in tg.Actions)
                    {
                        if (ac == null)
                        {
                            continue;
                        }
                        acs.Append(EfeitosInfo.Limpa(ac.name))
                           .Append("{ef=").Append(EfeitosInfo.Descreve(ac.Effects)).Append("}; ");
                    }
                }
                sb.Append(tg.TriggerType)
                  .Append("[ef=").Append(EfeitosInfo.Descreve(tg.GeneralEffects))
                  .Append("~cond=").Append(EfeitosInfo.Limpa(tg.Condition))
                  .Append("~status=").Append(stt)
                  // RD-2 (a): o campo que a nota antiga dava como inexistente.
                  .Append("~alvos=").Append(EfeitosInfo.Limpa(tg.Targets))
                  .Append("~acoes=").Append(acs.ToString().TrimEnd(' ', ';'))
                  .Append("~chances=").Append(EfeitosInfo.Junta(tg.ActionChanceEquations))
                  // O cooldown PROPRIO do gatilho: e ele que vale no caminho de proc.
                  .Append("~cd=").Append(tg.Cooldown)
                  .Append("]; ");
            }
            return sb.ToString().TrimEnd(' ', ';');
        }

        /// <summary>
        /// RD-2: o gancho de TEMPO do status, num campo so (`tick=`). `ApplyAction(ActionStatus)`
        /// (l.39260-39398) le, nesta ordem: (1) os `Effects` proprios, com `TickTargets` dizendo
        /// POR CELULA quem leva o dano; (2) `StatusEffectsOnTick` (+Condition +Targets);
        /// (3) `ActionsOnTick` (+Condition +Targets). Todos os campos vem do `ActionStatusInfo`
        /// (l.441035/441042/441045/441047/441049/441052/441055/441057/441059).
        ///
        /// MEDICAO DESTE BUILD (421 `ActionStatusInfo` de resources.assets, lidos do asset):
        /// `TickTargets`, `ActionsOnTick`, `ActionsOnTickCondition/Targets` e
        /// `StatusEffectsOnTickCondition/Targets` estao VAZIOS em 100% deles; so
        /// `StatusEffectsOnTick` tem caso (`Freeze Earth`, `Ice Storm`, `Faerie Swarm`,
        /// `Blood Mist`, `Slow Poison Aura`, `The Bad Bloom`). O campo sai assim mesmo: o
        /// pedido do dono e colher AGORA o que uma funcao futura vai precisar, e o `tick=-`
        /// de toda linha e a medida - nao a suposicao - de que o proc das auras de shrine
        /// NAO passa por aqui (ele passa pelo `SkillTriggers[].Targets`, ver `TriggersDe`).
        /// </summary>
        private static string TickDe(ActionStatusInfo s)
        {
            bool temAlvos = !string.IsNullOrEmpty(s.TickTargets);
            bool temCond = !string.IsNullOrEmpty(s.ActionsOnTickCondition);
            bool temAlvoAcoes = !string.IsNullOrEmpty(s.ActionsOnTickTargets);
            bool temAcoes = s.ActionsOnTick != null && s.ActionsOnTick.Length > 0;
            bool temStCond = !string.IsNullOrEmpty(s.StatusEffectsOnTickCondition);
            bool temStAlvos = !string.IsNullOrEmpty(s.StatusEffectsOnTickTargets);
            bool temSt = s.StatusEffectsOnTick != null && s.StatusEffectsOnTick.Length > 0;
            if (!(temAlvos || temCond || temAlvoAcoes || temAcoes || temStCond || temStAlvos || temSt))
            {
                return "-";
            }

            var acoes = new System.Text.StringBuilder();
            if (s.ActionsOnTick != null)
            {
                foreach (var ac in s.ActionsOnTick)
                {
                    if (ac == null)
                    {
                        continue;
                    }
                    acoes.Append(EfeitosInfo.Limpa(ac.name))
                         .Append("{ef=").Append(EfeitosInfo.Descreve(ac.Effects)).Append("}; ");
                }
            }

            return "[alvos=" + EfeitosInfo.Limpa(s.TickTargets)
                 + ";cond=" + EfeitosInfo.Limpa(s.ActionsOnTickCondition)
                 + ";alvoAcoes=" + EfeitosInfo.Limpa(s.ActionsOnTickTargets)
                 + ";acoes=" + acoes.ToString().TrimEnd(' ', ';')
                 + ";proc=" + (s.ActionsOnTickProcTriggers ? "sim" : "nao")
                 + ";status=" + EfeitosInfo.Nomes(s.StatusEffectsOnTick)
                 + ";statusCond=" + EfeitosInfo.Limpa(s.StatusEffectsOnTickCondition)
                 + ";statusAlvos=" + EfeitosInfo.Limpa(s.StatusEffectsOnTickTargets)
                 + ";nStatusOv=" + (s.StatusEffectsOnTickOverrides == null ? 0 : s.StatusEffectsOnTickOverrides.Length)
                 + "]";
        }

        /// <summary>
        /// RD-2: o par de auras do MOTOR - `AuraSourceStatus` + `AuraTriggerStatus`
        /// (l.441108/441110) e os overrides do gatilho (l.441112). E a mecanica lida em
        /// l.41796-41834 (`HasStatus(AuraSourceStatus.name)` / `AuraTriggerStatus`), a mesma
        /// que os selos e as `Aura of X` usam. MEDICAO DESTE BUILD: preenchido em 40 dos 421
        /// statuses - e SEMPRE junto de `IsAura=1` (os 40 batem), ou seja `IsAura` e o sinal
        /// barato do censo de auras.
        /// ATENCAO: as auras de SHRINE (`Flame/Decay Shrine Aura`) NAO estao nesses 40 - no
        /// asset elas vem com `IsAura=0` e sem este par; o que elas usam e o gatilho
        /// (`SkillTriggers[].Targets`), nao a mecanica de aura. Nao confundir as duas.
        /// </summary>
        private static string AuraDe(ActionStatusInfo s)
        {
            int ov = s.AuraTriggerStatusOverrides == null ? 0 : s.AuraTriggerStatusOverrides.Length;
            if (s.AuraSourceStatus == null && s.AuraTriggerStatus == null && ov == 0)
            {
                return "-";
            }
            return "[fonte=" + EfeitosInfo.Nome(s.AuraSourceStatus)
                 + ";gatilho=" + EfeitosInfo.Nome(s.AuraTriggerStatus)
                 + ";nGatilhoOv=" + ov + "]";
        }
        private static void Postfix(List<ActionStatusInfo> __result)
        {
            try
            {
                if (_dumped || __result == null || __result.Count <= 1)
                {
                    return;
                }

                // O jogo carrega os status incrementalmente durante o loading:
                // só despejamos quando o tamanho ficar estável por 5 acessos seguidos.
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

                Plugin.Log.LogInfo($"[Status] Inventário: {__result.Count} status carregados.");
                EfeitosInfo.Zerar();   // RV-8b-0g: resumo de tipos concretos e por categoria
                foreach (var s in __result)
                {
                    if (s == null)
                    {
                        continue;
                    }
                    // Censo (RV-7): descricao COMPLETA (o corte em 90 chars cortava a mecanica).
                    var desc = s.Description ?? "";

                    // Efeitos de atributo: e o que permite separar DEBUFF de BUFF pelo sinal
                    // do valor (RV-9 revisa debuffs primeiro, por pedido do projeto).
                    var ef = new System.Text.StringBuilder();
                    if (s.AttributeEffects != null)
                    {
                        foreach (var e in s.AttributeEffects)
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

                    // RV-8b-0e: os GeneralEffect.Action NA ORDEM. E ESTA a lista que o `*N`
                    // do texto indexa quando o dano da skill vem de um status
                    // (Tooltip.GetDamageString l.2218 -> l.2233). O `efeitos=` acima e
                    // AttributeEffects - campo DIFERENTE; nao confundir os dois.
                    var efGerais = new System.Text.StringBuilder();
                    int nGerais = 0;
                    if (s.Effects != null)
                    {
                        foreach (var e in s.Effects)
                        {
                            var ge = e as GeneralEffect;
                            if (ge == null)
                            {
                                continue;
                            }
                            nGerais++;   // conta MESMO o de Action vazio: e assim que o tooltip indexa
                            if (!string.IsNullOrEmpty(ge.Action))
                            {
                                efGerais.Append(ge.Action.Replace("\n", " ").Replace("\r", " ")
                                                        .Replace("|", "/").Replace("\"", "'").Trim())
                                        .Append("; ");
                            }
                        }
                    }

                    // AURA (29/09): o "within N hexes" dos selos (`Seal of Protection/Might/
                    // Salvation`), do `Bless` e afins NÃO está no alvo da ação — a ação é
                    // auto-aplicada (`self=1`, `range=0`) e o raio mora AQUI, no status.
                    // `IsAura` + `AuraRadius` (default **3**, que é exatamente o número dos
                    // três selos) + quem ela afeta. Sem este campo, toda a classe de
                    // afirmação "N hexes" fica sem par no dump — foi o que travou 6 itens da
                    // árvore Light.
                    // RV-8d(b): as habilidades que a FORMA ganha (Shapeshift Werewolf/Dire/Vampire Bat)
                    // vivem no `CharacterInfo` do personagem substituido. `public List<SkillInfo> Skills`
                    // (l.319927 do decompilado). Sem isto, o "Gain new abilities" do texto fica sem par.
                    // RV-8b-0g: TIPO CONCRETO de CADA efeito. `Effects` e `IEffectInfo[]` -
                    // interface VAZIA (l.322255 do decompilado) - e o cast `e as GeneralEffect`
                    // (logo acima) devolve null em todo elemento que nao seja `GeneralEffect`:
                    // era assim que o dado sumia do dump. Ha DUAS implementacoes na montagem,
                    // `GeneralEffect` (l.322250, campo `Action`) e `CharacterVariableEffectInfo`
                    // (l.320295, campos EffectTarget / CharacterVariableAttribute / Amount) -
                    // justamente os que o cast antigo descartava. `nEfeitosTot` e o
                    // `Effects.Length` (inclui os de acao vazia e os de tipo nao-GeneralEffect).
                    var efTipos = EfeitosInfo.Descreve(s.Effects);

                    // Mesmo tratamento para `AttributeEffects` (CharacterEffectInfo[]):
                    // array de tipo CONCRETO, entao o cast nunca falhou aqui - mas o dump so
                    // publicava nome:metodo:valor e perdia as flags (Infinite,
                    // CalculateOnSecondPass, HideIfNotEquipped, IgnoreTierEffects).
                    var attrTipos = EfeitosInfo.Descreve(s.AttributeEffects);

                    string modelo;
                    if (s.ModelChangeCharacter != null)
                    {
                        var habs = s.ModelChangeCharacter.Skills;
                        var txt = "";
                        if (habs != null)
                        {
                            int lim = habs.Count > 14 ? 14 : habs.Count;
                            for (int h = 0; h < lim; h++)
                            {
                                if (habs[h] == null) continue;
                                txt += (txt.Length > 0 ? "; " : "") + habs[h].name;
                            }
                            if (habs.Count > lim) txt += "; (+" + (habs.Count - lim) + ")";
                        }
                        modelo = s.ModelChangeCharacter.name + " [" + txt + "]";
                    }
                    else modelo = "-";

                    Plugin.Log.LogInfo(
                        $"[Status] '{s.Name}' | tipo={s.StatusType} | raridade={s.Rarity} | " +
                        $"efeitos={ef} | efeitosDano={efGerais} | nEfeitosDano={nGerais} | " +
                        $"aura={(s.IsAura ? "sim" : "nao")} | raio={s.AuraRadius} | " +
                        $"auraAli={(s.AuraEffectsAllies ? "sim" : "nao")} | auraIni={(s.AuraEffectsEnemies ? "sim" : "nao")} | " +
                        $"modelo={modelo} | " +
                        // RV-9 (29/09): classificacao buff/debuff do ASSET. NAO existe `BenefitType`
                        // em `ActionStatusInfo` - esse campo e da classe `EventStatus` (status de evento).
                        // O certo aqui e `IsBeneficial`/`IsHarmful`, computados de `SkillTags`
                        // (l.319287/319428/319430). E o que separa buffs de debuffs no censo do RV-9.
                        $"beneficio={(s.IsBeneficial ? "Buff" : (s.IsHarmful ? "Debuff" : "Neutro"))} | " +
                        // RV-9: dois campos que travavam itens do lote 1 dos debuffs - os textos
                        // "Stacks up to N times" (o cap mora em `MaxStacks`) e "Lasts N turns" (a
                        // duracao mora em `Duration`). Nenhum dos dois era exportado (l.319149/319141).
                        $"dur={s.Duration} | maxStk={s.MaxStacks} | " +
                        // RV-8b-0g: o dado que o cast antigo perdia, mais os gatilhos do status.
                        // `SkillTriggers` e `SkillTrigger[]` e `SkillTrigger.GeneralEffects` e
                        // `GeneralEffect[]` (l.45797) - array CONCRETO, entao NESTE caminho o
                        // cast nao falha; o que faltava era o campo sair no dump (caso aberto
                        // do `Dwarven Aura`: o stun nao esta na acao, e o suspeito e o gatilho).
                        $"nEfeitosTot={EfeitosInfo.Conta(s.Effects)} | efTipos={efTipos} | " +
                        $"nAttrEf={EfeitosInfo.Conta(s.AttributeEffects)} | attrTipos={attrTipos} | " +
                        $"nTrig={EfeitosInfo.Conta(s.SkillTriggers)} | trigEf={TriggersDe(s)} | " +
                        // RD-2: os ganchos de EXPRESSAO e de TEMPO do status, mais as duas
                        // referencias de tooltip. Onde cada um mora no motor (decompilado):
                        //   expr      = DescriptionExpressions              (l.441015) - 138/421 statuses
                        //   danoExpr  = DamageExpressionOverrides           (l.441020) - 1/421
                        //   refAcao   = TooltipDamageInfoRefAction          (l.441022) - 19/421
                        //   refStatus = TooltipDamageInfoRefStatus          (l.441024) - 7/421
                        //   tick      = ActionsOnTick/StatusEffectsOnTick*  (ver TickDe) - 6/421
                        //   auraSts   = AuraSourceStatus/AuraTriggerStatus  (ver AuraDe)  - 40/421
                        // `expr` e o que carrega a FORMULA das auras de shrine: no asset, o
                        // `Flame Shrine Aura` tem DescriptionExpressions =
                        // ["Mathf.Round(5 * (1 + (Source[\"ShrineEffectBonus\"] / 100)))] e o
                        // `Decay Shrine Aura` o mesmo com base 10 - os numeros que o RV-19
                        // deduziu do decompilado saem agora do dump, lidos do motor.
                        $"expr={EfeitosInfo.Junta(s.DescriptionExpressions)} | " +
                        $"danoExpr={EfeitosInfo.Junta(s.DamageExpressionOverrides)} | " +
                        $"refAcao={EfeitosInfo.Nome(s.TooltipDamageInfoRefAction)} | " +
                        $"refStatus={EfeitosInfo.Nome(s.TooltipDamageInfoRefStatus)} | " +
                        $"tick={TickDe(s)} | auraSts={AuraDe(s)} | " +
                        $"desc=\"{desc.Replace("\n", " ")}\"");
                }

                // Prova, no proprio log, de que existe elemento que nao e GeneralEffect -
                // e de quais tipos concretos apareceram na categoria.
                Plugin.Log.LogInfo($"[Efeitos] resumo (status): {EfeitosInfo.Resumo()}");
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"[Status] erro no inventário: {e.Message}");
            }
        }
    }
}
