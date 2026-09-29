using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using HarmonyLib;

namespace BetterTooltips.Patches
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
            // ---- Escala por NÍVEL (RV-8b-2g) ----
            // Fonte: código do jogo. `GetFlatDamageValue(level, rarity) =
            // Mathf.Ceil(FlatDamageNodes.GetMultipler((int)level) * GetStatRarityMod(rarity))`
            // — é uma CURVA DE NÍVEL, não um atributo. O valor atual já aparece na tooltip
            // (é o [0]); o que faltava era dizer COM O QUE ele escala, que era a pergunta
            // legítima do jogador ("invisto em Might para isso melhorar?").
            // São as 5 skills do jogo que usam essa curva (Huntsman I/II, Thorns I/II e
            // Vengeful Shadows); a chave "Physical damage increased by [0]." cobre as duas
            // Huntsman porque as duas escalam igual.
            { "Grants [0] Return Physical Damage.", "\nScales with your character level." },
            { "Grants an additional [0] Return Physical Damage.", "\nScales with your character level." },
            { "Grants [0] Return Shadow Damage.", "\nScales with your character level." },
            { "Physical damage increased by [0].", "\nScales with your character level." },

            // Segunda leva (RV-8b-2i): a varredura `tools/check_scaling.py` percorreu as
            // fórmulas de TODAS as skills e achou 9 que escalam com `Source.Level` sem
            // dizer isso no texto. Cinco já estavam cobertas acima (a curva FlatDamage) e
            // estas são as outras. A `Shapeshift Dragonkin` entra pela tabela de
            // correções: quem está nas DUAS tabelas só executa a correção, então uma
            // explicação aqui ficaria código morto.
            // Não cobertas de propósito: Attack Power (70 skills) e Spell Power (~65) —
            // são o caminho padrão de dano, o valor já aparece na tooltip e repetir
            // "escala com ataque" em 135 skills seria ruído, não informação.
            { "@Intelligence@ grants [0] @Armor@ and @Magic Armor@ per point.  Current Bonus: [1]",
              "\nScales with your character level." },
            { "Damage caused steals [0] points of @Dexterity@. Lasts the entire battle. Stacks up to 10 times.",
              "\nScales with your character level." },
            { "Damage caused steals [0] points of @Intelligence@. Lasts the entire battle. Stacks up to 10 times.",
              "\nScales with your character level." },
            { "Damage caused steals [0] points of @Might@. Lasts the entire battle. Stacks up to 10 times.",
              "\nScales with your character level." },
            { "Envelopes the target in living vines that increase @armor@ and @magic armor@ by [0] and causes the target to regenerate *0 @health@ each turn.",
              "\nScales with your character level." },
            { "Increases all attributes by [0]. In addition, 10% of your highest attribute value is added to all other attributes.  Current Bonus: [1]",
              "\nScales with your character level." },
            { "Encases the friendly target in a dome of ice granting [0] Armor and Magic Armor for the duration. Immobilizes the target.",
              "\nScales with your character level." },

            // ---- O que cada INVOCAÇÃO faz (RV-8b-2h) ----
            // Fonte: os assets do jogo, via dump. `ActionInfo.Summons` é a lista de
            // CharacterInfo e `CharacterInfo.SkillsAndAI[].Skill` são as habilidades da
            // criatura - a tooltip só diz o NOME de cada bicho, nunca o que ele faz.
            // `herdaStats=nao` em todas estas: o invocado NÃO herda seus atributos, então
            // nenhuma delas escala com o que você investe.
            // Uma linha por criatura: com três nomes e suas habilidades numa linha só o
            // texto fica ilegível no tooltip. O \n é o mesmo separador que o jogo usa nos
            // textos dele; e só ASCII, para não depender de glifo na fonte do jogo.
            { "Summons a Raven, Coyote, or Raccoon to fight for you.",
              "\nOne is summoned at random:\n- Raven: Melee Attack, Evasion\n- Raccoon: Melee Attack, Steal Action\n- Coyote: Melee Attack, Cripple\nDoes not inherit your stats." },
            { "Summons a Stag, Wolf, or Boar to fight for you.",
              "\nOne is summoned at random:\n- Stag: Stunning Kick, Melee Attack\n- Wolf: Melee Attack, Howl\n- Boar: Melee Attack, Fracture\nDoes not inherit your stats." },
            { "Summons a Bear, Moose, or Panther to fight for you.",
              "\nOne is summoned at random:\n- Bear (a Grizzly): Stunning Slam, Wild Cleave\n- Moose: Ground Slam, Melee Attack\n- Panther: Shadow Walk, Melee Attack\nDoes not inherit your stats." },
            { "Summons a Tundra Wolf to fight for you.",
              "\nTundra Wolf: Melee Attack, Howl\nDoes not inherit your stats." },
            { "Summons a Dire Wolf to fight for you.",
              "\nDire Wolf: Melee Attack, Blood Howl\nDoes not inherit your stats." },
            { "Summon a grizzly to fight your enemies.",
              "\nGrizzly: Stunning Slam, Wild Cleave\nDoes not inherit your stats." },
            { "Summon a wolf to fight your enemies.",
              "\nWolf: Melee Attack, Howl\nDoes not inherit your stats." },
            { "Summon a Raven to fight your enemies. ",
              "\nRaven: Melee Attack, Evasion\nDoes not inherit your stats." },
            { "Raise an Undead Ranger to fight by your side.",
              "\nUndead Ranger: Ranged Attack, Hide In Shadows\nDoes not inherit your stats." },

            // Brambles e Ice Wall NAO invocam bicho: invocam o MESMO objeto (a criatura
            // `Brambles`) para bloquear hexes. Sao os UNICOS de 18 invocadores com
            // `herdaStats=sim` - o objeto herda os seus atributos, ao contrario dos
            // Raise/Summon/Animal Companion (16 com `herdaStats=nao`). Eu tinha
            // generalizado "herdaStats=nao em todas"; o dump dos 18 mostrou 16 nao / 2 sim,
            // e os 2 sao justamente estes. Por isso a frase aqui e o INVERSO da dos bichos.
            { "Summon brambles to block 4 hexes. Attackers will take physical damage when striking the brambles. Lasts 4 turns.",
              "\nCounts as a summon and inherits your stats." },
            { "Summon pillars of ice to block 4 hexes blocking enemy's line of sight. Attackers take cold damage.  Lasts 4 turns.",
              "\nCounts as a summon and inherits your stats." },

            // ---- Explicações de mecânica: powerups e status (BT-3..BT-8) ----
            // Fonte: o código do jogo (Assembly-CSharp, decompilado). Cada bloco abaixo
            // diz no próprio comentário qual atributo/método confirma a mecânica.
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
            // ---- Textos de UI e dicas de loading (fontes: o log do boot do jogo) ----
            // Não estão no censo de tooltips (que cobre skills/status/itens/afixos/
            // powerups). O defeito era o espaço duplo deixado depois do ponto.
            {
                "Shops are refreshed every time your party completes a quest.  Check back often for new loot!",
                "Shops are refreshed every time your party completes a quest. Check back often for new loot!"
            },
            {
                "A well timed healing or mana potion can turn the tide of battle. ",
                "A well timed healing or mana potion can turn the tide of battle."
            },

            // ---- RV-8b, arvore Shadow (29/09) ----
            // Só gramática/espacamento, sem tocar em mecânica. A chave é o texto EXATO
            // do asset (espaços duplos e espaço no fim contam).
            {
                // "creates an poison gas cloud applies" -> artigo errado + falta conectivo
                "The caster creates an poison gas cloud applies @4@ stacks of {STA=Poisoned} within 2 hexes of the selected target.",
                "The caster creates a poison gas cloud that applies @4@ stacks of {STA=Poisoned} within 2 hexes of the selected target."
            },
            {
                // "a Undead Wizard" -> artigo errado (som de vogal)
                // RV-8b-2 (lote Shadow): a explicacao da invocacao entra AQUI, dentro do
                // valor, e nao no TextAppends - quem esta nas duas tabelas so executa a
                // correcao, e uma explicacao no appends nunca rodaria. Fonte das
                // habilidades e o dump `[Summon]` (CharacterInfo.SkillsAndAI[].Skill);
                // `herdaStats=nao` em todos os Raise/Summon desta arvore.
                "Raise a Undead Wizard to fight by your side.",
                "Raise an Undead Wizard to fight by your side.\nUndead Wizard: Bone Explosion, Consumption, Ghost Armor\nDoes not inherit your stats."
            },
            {
                // espaco duplo no meio + espaco sobrando no fim
                "Completely negates the next attack.  Lasts until hit. ",
                "Completely negates the next attack. Lasts until hit."
            },
            {
                // espaco sobrando no fim
                "Crush the target's soul dealing *0 @Shadow Damage@ increased by your Max Health. ",
                "Crush the target's soul dealing *0 @Shadow Damage@ increased by your Max Health."
            },

            // ---- RV-8b, padronizacao pela MAIORIA (29/09) ----
            // Regra do projeto: quando skills irmas divergem na redacao, vale o padrao da
            // maioria - e a maioria costuma estar no proprio NOME da skill. Levantado por
            // tools/audit_tooltips.py (checagem E2).
            // Nomes: "Raise Skeletal Archer/Mage/Warrior" -> descricoes diziam "Summon".
            {
                "Summon a skeletal archer to fight by your side.",
                "Raise a skeletal archer to fight by your side.\nSkeletal Archer: Ranged Attack\nDoes not inherit your stats."
            },
            {
                "Summon a skeletal mage to fight by your side.",
                "Raise a skeletal mage to fight by your side.\nSkeletal Mage: Frost Nova, Fireball, Twister, Ghost Armor\nDoes not inherit your stats."
            },
            {
                "Summon a skeletal warrior to fight by your side.",
                "Raise a skeletal warrior to fight by your side.\nSkeletal Warrior: Melee Attack, Cleave\nDoes not inherit your stats."
            },
            {
                // Unico invocador com fecho diferente: 6 usam "by your side", 1 usava "for you".
                "Raise a Mighty Iron Golem to fight for you.",
                "Raise a Mighty Iron Golem to fight by your side.\nIron Golem: Ground Slam\nDoes not inherit your stats."
            },
            {
                // Familia "Shapeshift *": 3 abrem com "Shapeshift into", esta abria com
                // "Gain the ability to shapeshift into" (mesma redacao, mais verbosa).
                // O "Scales with" tambem entra aqui (RV-8b-2i): a formula e
                // `10 * Source.Level`, e quem esta nas duas tabelas so executa a CORRECAO
                // - uma explicacao no TextAppends para este texto nunca rodaria.
                "Gain the ability to shapeshift into a powerful elemental @Dragonkin@. Empowers basic attack, grants new abilities, and resistance based on the color you choose. Increases @Armor@ by [0].",
                "Shapeshift into a powerful elemental @Dragonkin@. Empowers basic attack, grants new abilities, and resistance based on the color you choose. Increases @Armor@ by [0].\nScales with your character level."
            },

            // ---- RV-8b-2, grafia/gramatica (29/09) ----
            // Levantado por varredura em TODAS as 417 skills: "benefical" (3x),
            // "additonal" (2x), "abilites" (1x) e "the damage of by" (3x).
            // Aqui so a GRAFIA: espaco duplo e espaco no fim ficam a cargo da regra geral
            // de normalizacao no fim do postfix (uma entrada por frase seria centenas).
            {
                // "additonal" -> "additional"
                "Sacrifice 15% of your maximum health in exchange for an additonal action this turn.  Applies {STA=Exhaustion}.",
                "Sacrifice 15% of your maximum health in exchange for an additional action this turn.  Applies {STA=Exhaustion}."
            },
            {
                // "abilites" -> "abilities"
                "Increase the range of all non-melee abilites by 1 hex. ",
                "Increase the range of all non-melee abilities by 1 hex. "
            },
            {
                // "increases the damage of by X%" -> "increases the damage by X%"
                "Deals *0 weapon damage. Every hex between you and your target increases the damage of by 10%.  Called Shot cannot be dodged or blocked.",
                "Deals *0 weapon damage. Every hex between you and your target increases the damage by 10%.  Called Shot cannot be dodged or blocked."
            },
            {
                // "benefical" -> "beneficial"
                "Deals *0 weapon damage, removes 1 random benefical status from the target and lowers the target's @Resistance@ by 20% for 2 turns.",
                "Deals *0 weapon damage, removes 1 random beneficial status from the target and lowers the target's @Resistance@ by 20% for 2 turns."
            },
            {
                "Deals *0 weapon damage. Removes 1 random benefical status from the target.",
                "Deals *0 weapon damage. Removes 1 random beneficial status from the target."
            },
            {
                // "additonal" -> "additional"
                "Every enemy slain on your turn grants 1 additonal AP.  Can only grant up to 1 additional AP per turn.",
                "Every enemy slain on your turn grants 1 additional AP.  Can only grant up to 1 additional AP per turn."
            },
            {
                "Deals *0 shadow damage and removes a random benefical status from the target. If a status is removed, the target suffers an additional *0 shadow damage.",
                "Deals *0 shadow damage and removes a random beneficial status from the target. If a status is removed, the target suffers an additional *0 shadow damage."
            },
            {
                // "increases the damage of by 10%" -> "increases the damage by 10%"
                "Deals *0 weapon damage.  Every hex between you and your target increases the damage of by 10%. ",
                "Deals *0 weapon damage.  Every hex between you and your target increases the damage by 10%. "
            },
            {
                // "increases the damage of by 15%" -> "increases the damage by 15%"
                "Deals *0 weapon damage.  Every hex between you and your target increases the damage of by 15%. ",
                "Deals *0 weapon damage.  Every hex between you and your target increases the damage by 15%. "
            },

            // ---- RV-8b-2e, concordancia e pontuacao (29/09) ----
            // Levantado por varredura em TODAS as 417 skills, com o PADRAO DO JOGO como
            // régua: "1 turns" aparece 1x em 417 (os outros usam "1 turn"); e das 8
            // descricoes sem ponto final, 6 sao o padrao "Current Bonus: [0]" (termina em
            // valor dinamico, e sao 6 de 6 -> fica como esta). Sobram estas 3, cujos
            // irmaos TEM ponto: Frozen Orb/Sun Fire (Bleeding Shot e Entangle tem) e
            // Pack Summoning I (II e III tem).
            {
                // unico caso de concordancia errada no jogo inteiro
                "Infects enemies with Stunning Spores applying {STA=Stun} for 1 turns.",
                "Infects enemies with Stunning Spores applying {STA=Stun} for 1 turn."
            },
            {
                "Hurls a ball of Ice dealing *0 cold damage to all targets in range. Applies 5 stacks of {STA=Chilled}",
                "Hurls a ball of Ice dealing *0 cold damage to all targets in range. Applies 5 stacks of {STA=Chilled}."
            },
            {
                "Hurls a ball of flame dealing *0 fire damage to all targets in range. Applies 10 stacks of {STA=Heat}",
                "Hurls a ball of flame dealing *0 fire damage to all targets in range. Applies 10 stacks of {STA=Heat}."
            },
            {
                "Summons a Timber Wolf to fight for you",
                "Summons a Timber Wolf to fight for you.\nTimber Wolf: Cripple, Melee Attack\nDoes not inherit your stats."
            },
        };

        private static readonly HashSet<string> _appliedFixes = new HashSet<string>();
        private static readonly HashSet<string> _appliedAppends = new HashSet<string>();

        /// <summary>Marcador de vida: o postfix já recebeu texto em inglês nesta sessão.</summary>
        private static bool _loggedAlive;

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
            "% Life Steal",
            "% Lifesteal",
            "Stealth",
            "Enrage",
            "Marked Prey",
        };

        /// <summary>
        /// Rótulos curtos ("Life Steal", "Life Steal: 15%", "% Life Steal", "X Applied")
        /// são exibição pura e não devem receber explicação do glossário.
        /// </summary>
        private static bool IsGlossaryLabel(string original)
        {
            string t = original.Trim();
            if (GlossaryLabelExclusions.Contains(t) || t.EndsWith(" Applied"))
            {
                return true;
            }
            if (t.Length <= 24)
            {
                string low = t.ToLower();
                if (low.StartsWith("life steal") || low.StartsWith("lifesteal"))
                {
                    return true;
                }
            }
            return false;
        }

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

            // Marcador de vida: prova no log que o postfix está recebendo texto em inglês.
            // O patch só loga quando MUDA algo; sem esta linha, um boot em que nenhuma
            // string conhecida apareceu parece "mod morto" no log.
            if (!_loggedAlive)
            {
                _loggedAlive = true;
                string amostra = original.Length > 60 ? original.Substring(0, 60) + "..." : original;
                Plugin.Log.LogInfo($"BetterTooltips: postfix ativo (1a localizacao em ingles: '{amostra}')");
            }

            if (TextFixes.TryGetValue(original, out string fixedText))
            {
                __result = fixedText;
                if (_appliedFixes.Add(original))
                {
                    Plugin.Log.LogInfo($"BetterTooltips: corrigido '{original}' -> '{fixedText}'");
                }
            }
            else if (TextAppends.TryGetValue(original, out string append))
            {
                __result += append;
                if (_appliedAppends.Add(original))
                {
                    Plugin.Log.LogInfo($"BetterTooltips: explicação adicionada a '{original}'");
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
                            Plugin.Log.LogInfo($"BetterTooltips: efeitos por ponto adicionados a '{original}'");
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
                                Plugin.Log.LogInfo($"BetterTooltips: ordem de redução adicionada a '{original}'");
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
                            if (IsGlossaryLabel(original))
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
                        Plugin.Log.LogInfo($"BetterTooltips: explicação adicionada a '{original}'");
                    }
                }
            }

            // Normalizacao de espacos (RV-8b-2): o padrao do jogo e UM espaco depois do
            // ponto (116 ocorrencias contra 77), mas varias frases vem com dois e a
            // diferenca APARECE no tooltip. E regra geral de proposito: vale para todo
            // texto localizado (skills, status, itens, dicas), nao so para as skills que a
            // varredura achou - centenas de entradas na tabela nao escalariam.
            // Roda DEPOIS das tabelas porque as chaves de TextFixes casam com o texto
            // ORIGINAL, espacos duplos inclusos.
            // NAO aparamos o fim: espaco sobrando no fim nao aparece no tooltip, e aparar
            // poderia colar palavras se o jogo concatenar strings.
            if (__result.Contains("  "))
            {
                string antes = __result;
                while (__result.Contains("  "))
                {
                    __result = __result.Replace("  ", " ");
                }
                if (_appliedFixes.Add("espacos:" + antes))
                {
                    Plugin.Log.LogInfo($"BetterTooltips: espacos normalizados em '{antes}'");
                }
            }
        }
    }
}
