using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using HarmonyLib;

namespace BetterTexts.Patches
{
    /// <summary>
    /// Intercepta OptionsManager.Localize(string original, LanguageGender, Gender) — o funil
    /// por onde passa TODO texto localizado do jogo — e altera o valor final (__result).
    ///
    /// Postfix = roda DEPOIS do método original. Recebemos:
    ///   - original : a string de entrada (texto em inglês, que é a base do jogo)
    ///   - __result : o valor que o método vai retornar; com `ref` podemos substituí-lo
    ///
    /// Por que Postfix e não Prefix: queremos o texto FINAL (já localizado/processado),
    /// e queremos que o jogo continue fazendo o trabalho dele — só complementamos a saída.
    /// </summary>
    [HarmonyPatch(typeof(OptionsManager), nameof(OptionsManager.Localize))]
    public static class LocalizePatch
    {
        // Explicações adicionadas ao final do texto.
        //
        // Treasure Find — MECÂNICA CONFIRMADA (código + teste em jogo):
        //   - o efeito do powerup soma +20 por nível ao atributo "DropQuantityMod" (5 níveis → +100)
        //   - GameLogic.GetCharacterLootDropModifier soma o atributo de TODOS os personagens da party
        //   - o roll de loot multiplica a chance de cada item por esse modificador
        // Logo: +X% Treasure Find = +X% de chance de drop, acumulando com a party.
        private static readonly Dictionary<string, string> TextAppends = new Dictionary<string, string>
        {
            { "+ 20% increased Treasure Find", "\nIncreases the chance for enemies to drop items. Does not affect item rarity. Stacks with your party." },
            { "+ 40% increased Treasure Find", "\nIncreases the chance for enemies to drop items. Does not affect item rarity. Stacks with your party." },
            { "+ 60% increased Treasure Find", "\nIncreases the chance for enemies to drop items. Does not affect item rarity. Stacks with your party." },
            { "+ 80% increased Treasure Find", "\nIncreases the chance for enemies to drop items. Does not affect item rarity. Stacks with your party." },
            { "+ 100% increased Treasure Find", "\nIncreases the chance for enemies to drop items. Does not affect item rarity. Stacks with your party." },

            // Gold Find — MECÂNICA VERIFICADA NO CÓDIGO (confirmação empírica via RoguelikeDebugger):
            //   - ApplyGoldModifiers lê character["GoldMod"] somado à party e multiplica o ouro
            //   - usado na distribuição de ouro pós-batalha (PostBattleManager), recompensas de
            //     aventura/quest e ouro de eventos
            //   - "GoldMod" é um asset CharacterAttribute; efeitos de powerup viram contribuições
            //     de atributo (mecanismo provado na BT-3)
            { "+ 10% increased Gold Find", "\nIncreases the gold you earn. Stacks with your party." },
            { "+ 20% increased Gold Find", "\nIncreases the gold you earn. Stacks with your party." },
            { "+ 30% increased Gold Find", "\nIncreases the gold you earn. Stacks with your party." },
            { "+ 40% increased Gold Find", "\nIncreases the gold you earn. Stacks with your party." },
            { "+ 50% increased Gold Find", "\nIncreases the gold you earn. Stacks with your party." },

            // Damage and Healing — VERIFICADO: soma no atributo "DamageMod" base, que entra
            // em (1 + (DamageMod + DamageMod<Tipo> + ManaPowerMod)/100) × (1+AbilityPower/100)
            // para TODOS os tipos de dano E para a cura (DamageModHealing usa a mesma base).
            { "+ 5% to Damage and Healing", "\nIncreases all damage you deal and all healing you do." },
            { "+ 10% to Damage and Healing", "\nIncreases all damage you deal and all healing you do." },
            { "+ 15% to Damage and Healing", "\nIncreases all damage you deal and all healing you do." },
            { "+ 20% to Damage and Healing", "\nIncreases all damage you deal and all healing you do." },
            { "+ 25% to Damage and Healing", "\nIncreases all damage you deal and all healing you do." },

            // Damage Reduction — VERIFICADO: atributo "DamageReduction" vira camada
            // multiplicativa (1 - (DamageReduction + Resilience + TakeCover)/100) na cadeia
            // de redução de dano. Texto GERADO DINAMICAMENTE (BuildDamageReductionNote) com
            // a ordem real do GlobalSettings (padrão: redução geral → resists → armadura).

            // Movement — VERIFICADO: soma ao atributo "FreeMovementPoints" (movimento por turno).
            // (RV-5: versão não-redundante — o original já diz "additional movement")
            { "Gain 1 additional movement", "\nEach movement point lets you move one extra hex per turn." },
            { "Gain 2 additional movement", "\nEach movement point lets you move one extra hex per turn." },

            // Range — VERIFICADO: o powerup alimenta "RangeTypeAdderRanged" (o melee não
            // muda — dump: RangeMelee=0, RangeRanged=2 com Lv2). Texto reflete ranged.
            { "Gain 1 additional range", "\nIncreases the range of your ranged attacks and skills. Does not apply to certain skills." },
            { "Gain 2 additional range", "\nIncreases the range of your ranged attacks and skills. Does not apply to certain skills." },

            // Skill Options — VERIFICADO: RoguelikeManager.GetSkillChoices(numOpcoesBase +
            // character["AdditionalRoguelikeSkillOptions"]) → mais opções na escolha de skill.
            { "Skill Options +1", "\nIncreases the number of skill choices offered when leveling up." },
            { "Skill Options +2", "\nIncreases the number of skill choices offered when leveling up." },

            // Attribute Points — VERIFICADO: UnspentStatPoints = base + (Level-1) ×
            // (NumStatsPerNewLevel + AdditionalRoguelikeAttributesPointsPerLevel).
            { "Attribute Points Per Level +1", "\nGrants additional attribute points each time you level up." },
            { "Attribute Points Per Level +2", "\nGrants additional attribute points each time you level up." },
            { "Attribute Points Per Level +3", "\nGrants additional attribute points each time you level up." },

            // Resists — VERIFICADO: dano do elemento × (1 - Resist/100), camada multiplicativa
            // na cadeia de redução (case DamageReductionCalcOrder.Resists em ApplyAction).
            { "[[ResistCold]] +10%", "\nReduces Cold damage you take." },
            { "[[ResistCold]] +15%", "\nReduces Cold damage you take." },
            { "[[ResistCold]] +20%", "\nReduces Cold damage you take." },
            { "[[ResistFire]] +10%", "\nReduces Fire damage you take." },
            { "[[ResistFire]] +15%", "\nReduces Fire damage you take." },
            { "[[ResistFire]] +20%", "\nReduces Fire damage you take." },
            { "[[ResistLightning]] +10%", "\nReduces Lightning damage you take." },
            { "[[ResistLightning]] +15%", "\nReduces Lightning damage you take." },
            { "[[ResistLightning]] +20%", "\nReduces Lightning damage you take." },
            { "[[ResistPhysical]] +10%", "\nReduces Physical damage you take." },
            { "[[ResistPhysical]] +15%", "\nReduces Physical damage you take." },
            { "[[ResistPhysical]] +20%", "\nReduces Physical damage you take." },

            // Summon Damage & Health — VERIFICADO: atributos SummonDamageMod/SummonHealthMod.
            { "+ 5% to Summon Damage and Health", "\nIncreases the damage and health of your summoned creatures." },
            { "+ 10% to Summon Damage and Health", "\nIncreases the damage and health of your summoned creatures." },
            { "+ 15% to Summon Damage and Health", "\nIncreases the damage and health of your summoned creatures." },
            { "+ 20% to Summon Damage and Health", "\nIncreases the damage and health of your summoned creatures." },
            { "+ 25% to Summon Damage and Health", "\nIncreases the damage and health of your summoned creatures." },

            // Skill Tree Removal — VERIFICADO: remove árvores do pool de escolhas;
            // MinimumTreesRemaining=4; texto "can only be chosen at level 1" vem do próprio jogo.
            { "Skill Tree Removals +1", "\nLets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen." },
            { "Skill Tree Removals +2", "\nLets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen." },
            { "Skill Tree Removals +3", "\nLets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen." },
            { "Skill Tree Removals +4", "\nLets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen." },
            { "Skill Tree Removals +5", "\nLets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen." },
            { "Skill Tree Removals +6", "\nLets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen." },
            { "Skill Tree Removals +7", "\nLets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen." },
            { "Skill Tree Removals +8", "\nLets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen." },
        };

        // Primeiras correções reais de texto — apenas digitação/espaçamento observados
        // no jogo, sem nenhuma afirmação de gameplay. Chave = texto original exato.
        private static readonly Dictionary<string, string> TextFixes = new Dictionary<string, string>
        {
            {
                "Shops are refreshed every time your party completes a quest.  Check back often for new loot!",
                "Shops are refreshed every time your party completes a quest. Check back often for new loot!"
            },
            {
                "A well timed healing or mana potion can turn the tide of battle. ",
                "A well timed healing or mana potion can turn the tide of battle."
            },
        };

        private static readonly HashSet<string> _appliedFixes = new HashSet<string>();
        private static readonly HashSet<string> _appliedAppends = new HashSet<string>();

        // Powerups de atributo: "+ N to Might/Dexterity/Intelligence/Vitality/Reflex".
        // Os efeitos por ponto são os MESMOS que o tooltip de stats do jogo mostra
        // (Tooltip.ShowMainStatTooltip), com os valores lidos do GlobalSettings em runtime.
        private static readonly Regex AttributePowerupRegex = new Regex(
            @"^\+\s*\d+\s+to\s+(Might|Dexterity|Intelligence|Vitality|Reflex)$",
            RegexOptions.Compiled);

        private static readonly Regex DamageReductionRegex = new Regex(
            @"^\+\s*\d+%\s+Damage Reduction$",
            RegexOptions.Compiled);

        // Statuses que concedem atributos (BT-6a): descrições como
        // "Might increased by [0]." (status) ou "Dexterity increased by 30." (poções).
        // Mesma explicação dinâmica dos powerups.
        private static readonly (Regex Pattern, string Attribute)[] StatusAttributeRules =
        {
            (new Regex(@"^Might increased by (\[\d+\]|\d+)\.$", RegexOptions.Compiled), "Might"),
            (new Regex(@"^Dexterity increased by (\[\d+\]|\d+)\.$", RegexOptions.Compiled), "Dexterity"),
            (new Regex(@"^Intelligence increased\.$|^Intelligence increased by (\[\d+\]|\d+)\.$", RegexOptions.Compiled), "Intelligence"),
            (new Regex(@"^Vitality increased by (\[\d+\]|\d+)\.$", RegexOptions.Compiled), "Vitality"),
            (new Regex(@"^Reflex increased by (\[\d+\]|\d+)\.$", RegexOptions.Compiled), "Reflex"),
        };

        // BT-6c: Fortunes que concedem atributos, formato "@Might@ increased by {12,60}."
        private static readonly (Regex Pattern, string Attribute)[] FortuneAttributeRules =
        {
            (new Regex(@"^@Might@ increased by \{\d+,\d+\}\.?", RegexOptions.Compiled), "Might"),
            (new Regex(@"^@Dexterity@ increased by \{\d+,\d+\}\.?", RegexOptions.Compiled), "Dexterity"),
            (new Regex(@"^@Intelligence@ increased by \{\d+,\d+\}\.?", RegexOptions.Compiled), "Intelligence"),
            (new Regex(@"^@Vitality@ increased by \{\d+,\d+\}\.?", RegexOptions.Compiled), "Vitality"),
            (new Regex(@"^@Reflex@ increased by \{\d+,\d+\}\.?", RegexOptions.Compiled), "Reflex"),
        };

        // BT-6b: statuses que reduzem resistências — explicar a mecânica de resistência
        // (fórmula verificada: dano × (1 - Resist/100); resistência negativa AMPLIFICA o dano).
        private const string ResistanceExplainSuffix =
            "\nResistances reduce their damage type by the listed %. If a resistance goes negative, that damage type is amplified instead.";

        private static readonly string[] ResistanceReductionPrefixes =
        {
            "Elemental resistance reduced by 5% per stack",                       // Heat
            "Reduces @Cold Resistance@ by @25%@ per stack",                       // Frostbitten
            "Reduces @Fire Resistance@ by @25%@ per stack",                       // Severely Burned
            "Reduces @Physical Resistance@ by @25%@ per stack",                   // Sundered
            "Reduces Elemental resistances by 25%",                               // Curse of Elements
            "@Resistance@ lowered by 20%",                                        // Fracture / Dispelling Fracture
            "@Resistances@ lowered by 20%. Reduces healing received by 50%",      // Mortal Fracture
        };

        // BT-7a: glossário de mecânicas nos tooltips de skills — definições tiradas
        // das descrições dos PRÓPRIOS status do jogo (inventário da BT-6, sem invenção).
        // A exclusão evita redundância quando o texto já define o termo (ex.: a
        // descrição do status Stealth já menciona o crítico garantido).
        // REGRA: nada relacionado a Bard/música (Crescendo, Harmony, Songs) — a árvore
        // chega na próxima atualização do jogo; não mexer.
        // Rótulos da ficha de personagem que NUNCA devem receber explicação
        // (ex.: a linha "Life Steal" do bloco de Stats é só um número + nome).
        private static readonly HashSet<string> GlossaryLabelExclusions = new HashSet<string>
        {
            "Life Steal",
            "Lifesteal",
            "Stealth",
            "Enrage",
            "Marked Prey",
        };

        private static readonly (Regex Match, string Append, string ExcludeIfContains)[] SkillGlossaryRules =
        {
            (new Regex(@"\bStealth\b", RegexOptions.Compiled),
             "\nStealth: attacking from stealth has 100% critical hit chance.",
             "critical hit chance"),
            (new Regex(@"Marked Prey", RegexOptions.Compiled),
             "\nMarked Prey: increases damage taken by 10% per stack.",
             "Damage taken"),
            // BT-7b: Enrage — status do jogo: "Immune to all movement impairing effects
            // and knockback." (verificado: statuses TriggersEnrage rolam StatusResistImpairment
            // em alvos com CanEnrage; troca de fase limpa esses statuses).
            (new Regex(@"\bEnrage\b", RegexOptions.Compiled),
             "\nEnraged characters are immune to movement impairing effects and knockback.",
             "immune to"),
            // BT-7b: Life Steal — RV-7: TEXTO OFICIAL do jogo (localização + patch notes v0.22):
            // "Life Steal heals you for a percentage of your Max Health each time you hit.
            // Reduced for area of effect abilities." — o código atual calcula a partir da
            // vida perdida do ALVO; pendente confirmação empírica via [LifeSteal] debug.
            (new Regex(@"Life Steal|Lifesteal", RegexOptions.Compiled),
             "\nLife Steal: heals you for a percentage of your Max Health each time you hit. Reduced for area of effect abilities.",
             "heals you for"),
        };

        // BT-8: afixos de itens — mecânicas verificadas no código (Character.ApplyAction):
        // Armor: dano - (Armor/ArmorPerDamagePointReduction), com cap maxArmorReductionPercent.
        // Resists: dano × (1 - Resist/100) por elemento.
        // Só disparam em textos com verbo de modificação ("increased/added/...") para não
        // poluir rótulos simples (ex.: o label "Armor" da ficha de stats).
        private static readonly Regex ArmorAffixRegex = new Regex(@"\bArmor\b", RegexOptions.Compiled);
        private static readonly Regex ResistAffixRegex = new Regex(@"\bResistance\w*\b", RegexOptions.Compiled);

        private static string BuildArmorNote()
        {
            var gs = GlobalSettingsManager.instance?.globalSettings;
            if (gs == null)
            {
                return null;
            }
            return "\nArmor blocks damage: each " + gs.ArmorPerDamagePointReduction.ToString("0.##") +
                " Armor reduces damage taken by 1 (capped at " +
                gs.maxArmorReductionPercent.ToString("0.##") +
                "% of the incoming damage). Armor and Magic Armor do not reduce Shadow damage.";
        }

        private static string BuildAttributeEffects(string attribute)
        {
            var gs = GlobalSettingsManager.instance?.globalSettings;
            if (gs == null)
            {
                return null;
            }

            switch (attribute)
            {
                case "Might":
                    return "\nEffects per point:\n" +
                        $"+{gs.AbilityPwrPerMight.ToString("0.##")}% Damage & Healing\n" +
                        $"+{gs.AbilityPwrPerMightSummon.ToString("0.##")}% Summon Damage\n" +
                        $"+{gs.ArmorPercPerMight.ToString("0.##")}% Armor & Magic Armor";
                case "Dexterity":
                    return "\nEffects per point:\n" +
                        $"+{gs.CritRatingPerDex.ToString("0.##")} Crit Rating\n" +
                        $"+{gs.CritDamagePerDex.ToString("0.##")}% Crit Damage\n" +
                        $"1 Movement Per {gs.MovementPointPerDexInterval} Dex (Max 3)";
                case "Intelligence":
                    return "\nEffects per point:\n" +
                        $"+{gs.ManaPerInt.ToString("0.##")} Max Mana\n" +
                        $"+{gs.MaxManaPercPerInt.ToString("0.##")}% Max Mana\n" +
                        $"1 Skill Range Per {gs.RangePerIntInterval} Int (Max 3)\n" +
                        $"+{gs.SummonLifePerInt.ToString("0.##")}% Summon Health";
                case "Vitality":
                    return "\nEffects per point:\n" +
                        $"+{gs.MaxHealthPerVit.ToString("0.##")} Max Health\n" +
                        $"+{gs.MaxHealthPercPerVit.ToString("0.##")}% Max Health";
                case "Reflex":
                    return "\nEffects per point:\n" +
                        $"+{gs.DodgeRatingPerReflex.ToString("0.##")} Dodge Rating\n" +
                        $"+{gs.DodgeCounterChancePerReflex.ToString("0.##")}% Dodge Counter Chance\n" +
                        $"+{gs.OppAttackPercDmgPerReflex.ToString("0.##")}% Opportunity Attack Damage\n" +
                        $"+{gs.OppAttackPercDmgPerReflex.ToString("0.##")}% Counter Attack Damage\n" +
                        $"1 Counter Attack a turn Per {gs.ExtraCounterAttacksPerReflexInterval} Reflex (Max 3)";
                default:
                    return null;
            }
        }

        /// <summary>
        /// Nota dinâmica do Damage Reduction (RV-5/RV-7): lê a ordem de redução de dano real
        /// do GlobalSettings e mostra a cadeia completa do cálculo.
        /// Padrão do jogo: GeneralReduction → Resists → Armor.
        /// </summary>
        private static string BuildDamageReductionNote()
        {
            try
            {
                var gs = GlobalSettingsManager.instance?.globalSettings;
                if (gs == null)
                {
                    return null;
                }
                var order = gs.DamageReductionOrder;
                if (order == null || order.Length == 0)
                {
                    return null;
                }
                var names = new List<string>();
                bool foundGeneral = false;
                foreach (var stage in order)
                {
                    string s = stage.ToString();
                    if (s == "GeneralReduction")
                    {
                        foundGeneral = true;
                        continue;
                    }
                    if (foundGeneral)
                    {
                        names.Add(
                            s == "Resists" ? "Resistances" :
                            s == "Armor" ? "Armor" : s);
                    }
                }
                if (foundGeneral && names.Count > 0)
                {
                    // Redação do usuário (18:55): "Applied before X and Y" —
                    // lista somente as etapas que vêm DEPOIS da redução geral.
                    return "\nReduces all damage you take. Applied before "
                        + string.Join(" and ", names) + ".";
                }
                return "\nReduces all damage you take.";
            }
            catch
            {
                return "\nReduces all damage you take.";
            }
        }

        private static void Postfix(string original, ref string __result)
        {
            if (original == null || __result == null)
            {
                return;
            }

            // Só mexemos quando o texto exibido é o inglês original
            // (em outros idiomas o resultado vem traduzido e não tocamos).
            if (__result != original)
            {
                return;
            }

            if (TextFixes.TryGetValue(original, out string fixedText))
            {
                __result = fixedText;
                if (_appliedFixes.Add(original))
                {
                    Plugin.Log.LogInfo($"BetterTexts: corrigido '{original}' -> '{fixedText}'");
                }
            }
            else if (TextAppends.TryGetValue(original, out string append))
            {
                __result += append;
                if (_appliedAppends.Add(original))
                {
                    Plugin.Log.LogInfo($"BetterTexts: explicação adicionada a '{original}'");
                }
            }
            else
            {
                // Powerups de atributo: espelha os "Effects Per Point" do tooltip de stats.
                Match m = AttributePowerupRegex.Match(original);
                if (m.Success)
                {
                    string effects = BuildAttributeEffects(m.Groups[1].Value);
                    if (effects != null)
                    {
                        __result += effects;
                        if (_appliedAppends.Add(original))
                        {
                            Plugin.Log.LogInfo($"BetterTexts: efeitos por ponto adicionados a '{original}'");
                        }
                    }
                }
                else
                {
                    // Damage Reduction (RV-5): nota dinâmica com a ordem de redução.
                    if (DamageReductionRegex.IsMatch(original))
                    {
                        string note = BuildDamageReductionNote();
                        if (note != null)
                        {
                            __result += note;
                            if (_appliedAppends.Add(original))
                            {
                                Plugin.Log.LogInfo($"BetterTexts: ordem de redução adicionada a '{original}'");
                            }
                        }
                    }

                    // Statuses que concedem atributos (BT-6a): mesma explicação dinâmica.
                    bool appended = false;
                    foreach (var rule in StatusAttributeRules)
                    {
                        if (rule.Pattern.IsMatch(original))
                        {
                            string effects = BuildAttributeEffects(rule.Attribute);
                            if (effects != null)
                            {
                                __result += effects;
                                appended = true;
                            }
                            break;
                        }
                    }

                    // Fortunes que concedem atributos (BT-6c).
                    if (!appended)
                    {
                        foreach (var rule in FortuneAttributeRules)
                        {
                            if (rule.Pattern.IsMatch(original))
                            {
                                string effects = BuildAttributeEffects(rule.Attribute);
                                if (effects != null)
                                {
                                    __result += effects;
                                    appended = true;
                                }
                                break;
                            }
                        }
                    }

                    // Statuses que reduzem resistências (BT-6b): mecânica de resistência.
                    if (!appended)
                    {
                        foreach (var prefix in ResistanceReductionPrefixes)
                        {
                            if (original.StartsWith(prefix, StringComparison.Ordinal))
                            {
                                __result += ResistanceExplainSuffix;
                                appended = true;
                                break;
                            }
                        }
                    }

                    // Glossário de mecânicas nos tooltips de skills (BT-7a).
                    if (!appended)
                    {
                        foreach (var rule in SkillGlossaryRules)
                        {
                            if (GlossaryLabelExclusions.Contains(original.Trim()) ||
                                original.Trim().EndsWith(" Applied"))
                            {
                                break;
                            }
                            if (rule.Match.IsMatch(original) &&
                                !original.Contains(rule.ExcludeIfContains))
                            {
                                __result += rule.Append;
                                appended = true;
                                break;
                            }
                        }
                    }

                    // Afixos de itens (BT-8): Armor e Resistências.
                    if (!appended)
                    {
                        string low = original.ToLower();
                        bool hasVerb = low.Contains("increased") || low.Contains("added") ||
                            low.Contains("lowered") || low.Contains("reduced") ||
                            low.Contains("granted");
                        if (hasVerb && ArmorAffixRegex.IsMatch(original) &&
                            !original.Contains("blocks damage"))
                        {
                            string note = BuildArmorNote();
                            if (note != null)
                            {
                                __result += note;
                                appended = true;
                            }
                        }
                        else if (hasVerb && ResistAffixRegex.IsMatch(original) &&
                            !original.Contains("Summon resistance") &&
                            !original.Contains("resistances reduce"))
                        {
                            __result += ResistanceExplainSuffix;
                            appended = true;
                        }
                    }

                    if (appended && _appliedAppends.Add(original))
                    {
                        Plugin.Log.LogInfo($"BetterTexts: explicação adicionada a '{original}'");
                    }
                }
            }
        }
    }
}
