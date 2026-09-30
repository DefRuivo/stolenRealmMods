using System;
using System.Collections.Generic;
using Burst2Flame;
using HarmonyLib;
using UnityEngine;

namespace BetterTooltips.Patches
{
    /// <summary>
    /// RV-22 (30/09) — auras de shrine com o número FINAL (com Omnism/Horn) na tooltip,
    /// corrigindo os PARÂMETROS que alimentam a expressão do jogo — NUNCA reescrevendo texto.
    ///
    /// CAUSA RAIZ (decompilado do build atual):
    ///   - as auras escalam por `Mathf.Round(BASE * (1 + X["ShrineEffectBonus"]/100))`, com
    ///     X = Target (Warrior/Guardian/Conqueror/Rogue/Reaper/Seraph/Shaman/Energy/Fury/Dwarven)
    ///     e X = Source nas duas auras de perigo (Decay/Flame);
    ///   - o hover do shrine (Tooltip.ShowGroundEffectTooltip, l.214177/214180) monta o
    ///     GameFunctionParameters com `Source = Root.WorldCharacter` e SEM Target;
    ///   - o motor só faz `if (Target == null) Target = Source` (ApplyDescriptionExpressions,
    ///     l.215241-215243) — e o WorldCharacter é um personagem VAZIO (Root.CreateWorldCharacter,
    ///     l.143680 = `Observable.New<Character>()`), sem atributo nenhum: o bônus lido é 0 e a
    ///     tooltip mostra SEMPRE o número base (observado em jogo: com Omnism o valor não mudava).
    ///
    /// FIX: prefix em `Tooltip.ApplyDescriptionExpressions` — o funil por onde passam TODOS os
    /// tooltips de skill/status/powerup e o hover do ground effect (6 chamadas no motor) — que
    /// PREENCHE apenas os parâmetros VAZIOS (Target/Source) com o RECEPTOR resolvido. O texto
    /// continua sendo montado pelo jogo; nós só damos a ele o personagem certo para ler o
    /// `ShrineEffectBonus`. Nunca usa "o máximo da party": é o personagem resolvido, na ordem
    /// `Tooltip.TooltipCharacter` -> `Root.WorldCharacter` -> `Source` existente.
    ///
    /// SEGURANÇA (aprendizado do incidente de 30/09): a assinatura real do alvo é
    ///   ApplyDescriptionExpressions(string text, string[] expressions,
    ///                               GameFunctionParameters gameFunctionParameters,
    ///                               float fontSize, float rangeMod = 0f)
    /// logo __0=text, __1=expressions, __2=GameFunctionParameters, __3=float fontSize.
    /// Este prefix declara a assinatura EXPLÍCITA por TIPO no [HarmonyPatch] (nunca resolução por
    /// nome) e lê `ref GameFunctionParameters __2` — o slot 2, NUNCA o __3. O prefix antigo lia
    /// `ref GameFunctionParameters __3` (o slot do float fontSize), interpretava o lixo da memória
    /// float como GameFunctionParameters e derrubou o jogo com 112 NullReferenceException dentro de
    /// GUIManager.Update (a batalha travava).
    ///
    /// O método roda em TODA tooltip do jogo: todo o corpo é try/catch e, em qualquer falha, os
    /// parâmetros chegam ao original exatamente como estavam.
    ///
    /// A Dwarven Aura fica FORA do acumulado: o efeito real dela não mora no AttributeEffects
    /// (vazio no dump, sem fórmula no cache compilado) — registrar, não somar.
    /// </summary>
    [HarmonyPatch]
    public static class ShrineAuraPatch
    {
        private static readonly HashSet<string> Family = new HashSet<string>
        {
            "Warrior Aura", "Guardian Aura", "Conqueror Aura", "Rogue Aura", "Reaper Aura",
            "Energy Aura", "Seraph Aura", "Shaman Aura", "Fury"
        };

        private static readonly Dictionary<string, (string attr, float baseVal)> AuraMap =
            new Dictionary<string, (string, float)>
            {
                { "Warrior Aura",   ("DamageMod", 20f) },
                { "Guardian Aura",  ("DamageReduction", 20f) },
                { "Conqueror Aura", ("CritChance", 20f) },
                { "Rogue Aura",     ("DodgeChance", 20f) },
                { "Reaper Aura",    ("LifeOnHit", 8f) },
                { "Energy Aura",    ("ManaCostMod", -50f) },
                { "Seraph Aura",    ("HealthPerTurnPercent", 10f) },
                { "Shaman Aura",    ("ManaPerTurnPercent", 10f) },
                { "Fury",           ("DamageMod", 25f) }, // Fury também tem DamageReduction −25 (no loop)
            };

        /// <summary>Chaves de texto (exatas) da família de auras de shrine no LocalizePatch.</summary>
        private static readonly HashSet<string> ShrineKeys = new HashSet<string>
        {
            "Attackers take Fire Damage.",
            "Take [0]% of your Max Health in Shadow Damage per turn.",
            "Damage increased by [0]%. ",
            "Reduces Damage taken by [0]%. ",
            "Critical hit chance increased by [0]%.",
            "Increases dodge chance by [0]%.",
            "Lifesteal increased by [0]%.",
            "Decreases the cost of mana using abilities by [0]%.",
            "Your attacks have a [0]% chance to stun the target.",
            "Recover [0]% of maximum health each turn. ",
            "Recover [0]% of maximum mana each turn. ",
            "Damage increased by [0]%. Damage taken increased by [0]%. "
        };

        public static bool IsShrineKey(string text)
        {
            return text != null && ShrineKeys.Contains(text);
        }

        private static bool UsesShrineBonus(string[] expressions)
        {
            if (expressions == null)
            {
                return false;
            }
            foreach (string e in expressions)
            {
                if (e != null && e.Contains("ShrineEffectBonus"))
                {
                    return true;
                }
            }
            return false;
        }

        // ============================================================================
        // RV-22 — os PARÂMETROS da expressão (nunca o texto).
        // Assinatura explícita em 5 tipos: __0=string text, __1=string[] expressions,
        // __2=GameFunctionParameters, __3=float fontSize, __4=float rangeMod.
        // O método roda em TODA tooltip do jogo.
        // ============================================================================
        [HarmonyPatch(typeof(Tooltip), nameof(Tooltip.ApplyDescriptionExpressions),
            new Type[] { typeof(string), typeof(string[]), typeof(GameFunctionParameters), typeof(float), typeof(float) })]
        [HarmonyPrefix]
        private static void FixShrineExpressionParams(Tooltip __instance, string[] expressions, ref GameFunctionParameters __2)
        {
            try
            {
                // (3) só age quando alguma expressão usa o atributo das auras de shrine.
                if (!UsesShrineBonus(expressions))
                {
                    return;
                }
                if (!_vivo)
                {
                    _vivo = true;
                    Plugin.Log.LogInfo("[Shrine RV-22] prefix de parametros ativo em ApplyDescriptionExpressions (__2 = GameFunctionParameters)");
                }

                // Já vieram os dois personagens (ex.: tooltip de status, que passa Source e Target):
                // não há parâmetro vazio a alimentar — não mexer.
                bool alvoVazio = __2.Target == null;
                bool fonteVazia = __2.Source == null;
                if (!alvoVazio && !fonteVazia)
                {
                    return;
                }

                // (6) `character["ShrineEffectBonus"]` LANÇA para nome desconhecido
                // (Character.this[string], l.32662-32675): sem o atributo no build, não tocar em nada.
                if (Burst2Flame.Game.Instance?.GetAttribute("ShrineEffectBonus") == null)
                {
                    Marca("atributo ShrineEffectBonus ausente neste build — parametros intactos");
                    return;
                }

                // (4) receptor: TooltipCharacter -> Root.WorldCharacter -> Source existente.
                Character receptor = Receptor(__instance, __2);
                if (receptor == null)
                {
                    Marca("nenhum receptor disponivel — parametros intactos ([0] fica na base)");
                    return;
                }

                // Preenche SÓ o que está vazio: o número passa a ser calculado com o bônus REAL
                // do receptor (Omnism I/II +8/+12 = 20; item Horn of Devotion {50,100}).
                if (fonteVazia)
                {
                    __2.Source = receptor;
                }
                if (alvoVazio)
                {
                    __2.Target = receptor;
                }
                Marca($"params: Target{(alvoVazio ? "(vazio)->" : "(intacto)")}{receptor.CharacterName}"
                    + $" Source{(fonteVazia ? "(vazio)->" : "(intacto)")}{(fonteVazia ? receptor.CharacterName : "(mantido)")}");
            }
            catch (Exception ex)
            {
                // (5) nunca propagar: os parâmetros chegam ao original intactos.
                Plugin.Log.LogWarning($"[Shrine RV-22] prefix falhou (parametros devolvidos intactos): {ex.GetType().Name}: {ex.Message}");
            }
        }

        /// <summary>Marcador de vida + dedupe (o prefix roda a cada frame de hover).</summary>
        private static readonly HashSet<string> _marcas = new HashSet<string>();
        private static bool _vivo = false;

        /// <summary>
        /// Receptor do efeito da aura — quem tem o `ShrineEffectBonus` que o jogador quer ver.
        /// Ordem: personagem em foco na UI -> WorldCharacter -> Source existente.
        /// NUNCA o "máximo da party" (o número é de um personagem concreto).
        /// </summary>
        private static Character Receptor(Tooltip tooltip, GameFunctionParameters parametros)
        {
            try
            {
                Tooltip t = tooltip;
                if (t == null && GUIManager.instance != null)
                {
                    t = GUIManager.instance.tooltip;
                }
                if (t != null)
                {
                    // Tooltip.TooltipCharacter = GameLogic.instance.CurrentlySelectedCharacter
                    Character emFoco = t.TooltipCharacter;
                    if (emFoco != null)
                    {
                        return emFoco;
                    }
                }
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[Shrine RV-22] TooltipCharacter indisponivel: {ex.GetType().Name}: {ex.Message}");
            }

            try
            {
                Character mundo = NetworkingManager.Instance?.NetworkManager?.Root?.WorldCharacter;
                if (mundo != null)
                {
                    return mundo;
                }
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[Shrine RV-22] WorldCharacter indisponivel: {ex.GetType().Name}: {ex.Message}");
            }

            // Último recurso: o próprio personagem que o chamador já passou.
            return parametros.Source != null ? parametros.Source : parametros.Target;
        }

        /// <summary>Loga cada combinação UMA vez (o prefix roda a cada frame de hover).</summary>
        private static void Marca(string linha)
        {
            try
            {
                if (_marcas.Count >= 200 || !_marcas.Add(linha))
                {
                    return;
                }
                Plugin.Log.LogInfo($"[Shrine RV-22] {linha}");
            }
            catch
            {
                // log nunca pode derrubar nada
            }
        }

        /// <summary>Formata um atributo acumulado com a semântica CERTA do jogo:
        /// DamageReduction positivo = dano tomado REDUZIDO; ManaCostMod negativo = custo REDUZIDO.</summary>
        private static string Format(string attr, float v)
        {
            switch (attr)
            {
                case "DamageReduction":
                    return v >= 0 ? "Damage taken −" + v + "%" : "Damage taken +" + (-v) + "%";
                case "ManaCostMod":
                    return "Mana Costs reduced by " + (-v) + "%";
                case "DamageMod": return "Damage +" + v + "%";
                case "CritChance": return "Crit Chance +" + v + "%";
                case "DodgeChance": return "Dodge +" + v + "%";
                case "LifeOnHit": return "Life Steal +" + v + "%";
                case "HealthPerTurnPercent": return "Health per turn +" + v + "%";
                case "ManaPerTurnPercent": return "Mana per turn +" + v + "%";
                default: return attr + " " + v + "%";
            }
        }

        /// <summary>Linha de acumulado (ou "" se não há nada). Nunca lança.</summary>
        public static string AcumuladoShrines()
        {
            try
            {
                // RV-22: o receptor é o MESMO do prefix — o WorldCharacter é vazio e nunca carrega
                // as auras ativas (elas ficam nos ActionStatuses do PERSONAGEM que está no shrine).
                if (Burst2Flame.Game.Instance?.GetAttribute("ShrineEffectBonus") == null)
                {
                    return "";
                }
                Character c = Receptor(null, default(GameFunctionParameters));
                if (c == null || c.ActionStatuses == null || c.ActionStatuses.Count == 0)
                {
                    Marca($"acumulado: receptor indisponivel (char={(c == null ? "(null)" : c.CharacterName)})");
                    return "";
                }
                float bonus = c["ShrineEffectBonus"];
                Dictionary<string, float> totals = new Dictionary<string, float>();
                int vistos = 0;
                foreach (var st in c.ActionStatuses)
                {
                    if (st == null || st.ActionStatusInfo == null)
                    {
                        continue;
                    }
                    string nome = st.ActionStatusInfo.Name;
                    if (!Family.Contains(nome) || !AuraMap.TryGetValue(nome, out var m))
                    {
                        continue;
                    }
                    vistos++;
                    float v = Mathf.Round(m.baseVal * (1f + bonus / 100f));
                    if (nome == "Fury")
                    {
                        Add(totals, "DamageMod", v);
                        Add(totals, "DamageReduction", -v);
                    }
                    else
                    {
                        Add(totals, m.attr, v);
                    }
                }
                Marca($"acumulado: char={c.CharacterName} bonus={bonus} auras={vistos} statuses={c.ActionStatuses.Count}");
                if (totals.Count == 0)
                {
                    return "";
                }
                List<string> parts = new List<string>();
                foreach (var kv in totals)
                {
                    parts.Add(Format(kv.Key, kv.Value));
                }
                string linha = "\n<color=#C8B090>Your active shrine auras: " + string.Join("; ", parts) + ".</color>";
                Marca("acumulado: " + linha.Replace("\n", " | "));
                return linha;
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[Shrine RV-22] acumulado falhou: {ex.GetType().Name}: {ex.Message}");
                return "";
            }
        }

        private static void Add(Dictionary<string, float> totals, string attr, float v)
        {
            totals[attr] = totals.TryGetValue(attr, out float cur) ? cur + v : v;
        }
    }
}
