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
                    Plugin.Log.LogInfo(
                        $"[Status] '{s.Name}' | tipo={s.StatusType} | raridade={s.Rarity} | " +
                        $"efeitos={ef} | efeitosDano={efGerais} | nEfeitosDano={nGerais} | " +
                        $"aura={(s.IsAura ? "sim" : "nao")} | raio={s.AuraRadius} | " +
                        $"auraAli={(s.AuraEffectsAllies ? "sim" : "nao")} | auraIni={(s.AuraEffectsEnemies ? "sim" : "nao")} | " +
                        $"desc=\"{desc.Replace("\n", " ")}\"");
                }
            }
            catch (Exception e)
            {
                Plugin.Log.LogWarning($"[Status] erro no inventário: {e.Message}");
            }
        }
    }
}
