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


        /// <summary>
        /// Duas correcoes de acabamento pedidas em teste:
        ///
        /// (a) A COR. O postfix principal aplica as tabelas; este roda DEPOIS dele
        ///     (HarmonyPriority.Low = por ultimo nos postfixes) e troca o marcador #C8B090
        ///     pela cor de "texto especial" do proprio tooltip.
        ///
        /// (b) A POSICAO. O jogo monta o tooltip como [descricao], uma quebra de linha e depois
        ///     [custos e alcance]
        ///     (ShowSkillTooltip, l.214400-214455 do decompilado), e a explicacao entra na
        ///     descricao - ou seja, ficava ANTES dos custos. Em vez de mudar a tabela (que e
        ///     chaveada pelo texto da descricao), este prefix pega o bloco ja colorido e o
        ///     move para o fim do corpo, que e o texto entregue a `ShowTooltip`.
        /// </summary>
        [HarmonyPatch]
        internal static class CorEOrdemDoTooltip
        {
            /// <summary>Diagnostico 1x: diz no log se o prefix achou o bloco (ou nao).</summary>
            private static bool _diagnosticadoCor;

            /// <summary>Mira o overload de ShowTooltip que recebe o corpo do tooltip.</summary>
            private static System.Reflection.MethodBase TargetMethod()
            {
                foreach (System.Reflection.MethodInfo m in AccessTools.GetDeclaredMethods(typeof(Tooltip)))
                {
                    if (m.Name == "ShowTooltip" && m.GetParameters().Length > 4)
                    {
                        return m;
                    }
                }
                return null;
            }

            /// <summary>Move a explicacao para o fim (depois de custos e alcance).</summary>
            private static void Prefix(ref string __3)
            {
                if (string.IsNullOrEmpty(__3))
                {
                    return;
                }
                string cor = string.IsNullOrEmpty(_corEspecialDoJogo) ? "C8B090" : _corEspecialDoJogo;
                string abre = "<color=#" + cor + ">";
                int i = __3.IndexOf(abre, StringComparison.Ordinal);
                if (i < 0)
                {
                    if (!_diagnosticadoCor)
                    {
                        _diagnosticadoCor = true;
                        Plugin.Log.LogInfo("BetterTooltips: ShowTooltip interceptado SEM o bloco (procurando " + abre + ")");
                    }
                    return;
                }
                if (!_diagnosticadoCor)
                {
                    _diagnosticadoCor = true;
                    Plugin.Log.LogInfo("BetterTooltips: ShowTooltip interceptado, bloco da explicacao movido para o fim (cor #" + cor + ")");
                }
                int f = __3.IndexOf("</color>", i, StringComparison.Ordinal);
                if (f < 0)
                {
                    return;
                }
                int ini = ((i > 0 && __3[i - 1] == '\n') ? i - 1 : i);
                string nota = __3.Substring(ini, f + "</color>".Length - ini);
                __3 = __3.Remove(ini, f + "</color>".Length - ini).TrimEnd() + "\n\n" + nota.TrimStart('\n').TrimEnd();
            }
        }
        /// <summary>
        /// A cor das explicacoes do mod NAO e escolhida por nos: e a cor de "texto especial" do
        /// PROPRIO tooltip do jogo (`specialDescColor`, campo do Tooltip em GUIManager), a MESMA
        /// que colore os nomes de status nas linhas nativas do tipo
        /// "All [damage type] damage applies {STA=Heat}". Fonte: Tooltip.cs do Assembly, onde a
        /// linha 214387 usa `ColorUtility.ToHtmlStringRGB(specialTextColor)` e a 214388 monta o
        /// token `{STA=<nome>}`.
        /// Nas tabelas o marcador fica como #C8B090 (um azul qualquer, so para o texto continuar
        /// legivel se a leitura falhar); aqui ele e trocado pela cor real do jogo.
        /// </summary>
        internal static string _corEspecialDoJogo;

        internal static string ComACorDoJogo(string texto)
        {
            if (string.IsNullOrEmpty(texto) || texto.IndexOf("#C8B090", StringComparison.Ordinal) < 0)
            {
                return texto;
            }
            if (_corEspecialDoJogo == null)
            {
                try
                {
                    Tooltip t = GUIManager.instance != null ? GUIManager.instance.tooltip : null;
                    _corEspecialDoJogo = t != null
                        ? UnityEngine.ColorUtility.ToHtmlStringRGB(t.specialDescColor)
                        : string.Empty;
                    Plugin.Log.LogInfo("BetterTooltips: cor do jogo para explicacoes = #" + _corEspecialDoJogo);
                }
                catch (Exception ex)
                {
                    _corEspecialDoJogo = string.Empty;
                    Plugin.Log.LogWarning("BetterTooltips: nao consegui ler specialTextColor (" + ex.Message + "); mantendo o fallback.");
                }
            }
            return string.IsNullOrEmpty(_corEspecialDoJogo)
                ? texto
                : texto.Replace("#C8B090", _corEspecialDoJogo);
        }

        /// <summary>
        /// Aplica a cor do bloco de explicacao DEPOIS das tabelas.
        ///
        /// PRECISA ficar DENTRO desta classe: aqui o alvo e `OptionsManager.Localize` (do
        /// `[HarmonyPatch]` acima). Eu havia posto este postfix numa classe separada que mira
        /// `Tooltip.ShowTooltip` - cujo retorno e `void` - e o Harmony reportou
        /// "HarmonyException: IL Compile Error" no log sem executar nada. Sintoma no tooltip:
        /// nota ainda no azul de fallback.
        ///
        /// ORDEM: em POSTFIX a prioridade e CRESCENTE (Low roda PRIMEIRO), entao `Priority.High`
        /// roda por ULTIMO - que e o que precisamos para ver o texto ja com as tabelas.
        /// </summary>
        [HarmonyPostfix, HarmonyPriority(Priority.High)]
        private static void CorDoJogoPostfix(ref string __result)
        {
            __result = ComACorDoJogo(__result);
        }

        private static readonly Dictionary<string, string> TextAppends = new Dictionary<string, string>
        {
            // Fire Breath - o texto nao dava o alcance. Fonte: campo `alvos` do `ActionProps`
            // (blast=Distance(Source.Cell) <= 4 + IsSameHemisphere + DistanceFromLine < 3f/2f).
            { "Breath fire dealing *0 fire damage to all enemies in a cone. ",
              "\n<color=#C8B090>The cone reaches 4 hexes from you.</color>" },
            // Frost Breath - o texto nao dava o alcance. Fonte: campo `alvos` do `ActionProps`
            // (blast=Distance(Source.Cell) <= 4 + IsSameHemisphere + DistanceFromLine < 3f/2f).
            { "Deals *0 cold damage each turn.",
              "\n<color=#C8B090>Hits everything in a cone reaching 4 hexes from you.</color>" },
            // Stunning Slam tem texto PROPRIO (cita o {STA=Stunned}); o `Slam` e o `Crushing`
            // Slam dividem um texto identico e ficam com uma entrada so. Fonte do alcance: o
            // campo `alvos` do `ActionProps`.
            { "Deals *0 weapon damage and applies {STA=Stunned} to all enemies within a line for 1 turn.",
              "\n<color=#C8B090>The line reaches 5 hexes from you.</color>" },
            // Slam - o texto dava a FORMA mas nao o alcance. Fonte: campo `alvos` do
            // `ActionProps` (blast/rsel): Cell.Distance(Source.Cell) <= 5 && Cell.IsSameHemisphere(...) && Cell.DistanceFromLine(...) < 3f/2f
            { "Deals *0 weapon damage to all enemies within a line.",
              "\n<color=#C8B090>The line reaches 5 hexes from you.</color>" },
            // Ice Lance - o texto dava a FORMA mas nao o alcance. Fonte: campo `alvos` do
            // `ActionProps` (blast/rsel): ... Distance(Source.Cell) <= 10 ... (mesma forma de linha)
            { "The caster hurls a razor-like shard of ice piercing foes in a line dealing *0 cold damage. ",
              "\n<color=#C8B090>The line reaches 10 hexes from you.</color>" },
            // Breath of Winter - o texto dava a FORMA mas nao o alcance. Fonte: campo `alvos` do
            // `ActionProps` (blast/rsel): ... Distance(Source.Cell) <= 4 ... (cone de 3 hexes de largura)
            { "Conjures the breath of a frost dragon dealing *0 cold damage to all enemies in a cone. ",
              "\n<color=#C8B090>The cone reaches 4 hexes from you.</color>" },
            // Lightning Breath - o texto dava a FORMA mas nao o alcance. Fonte: campo `alvos` do
            // `ActionProps` (blast/rsel): ... Distance(Source.Cell) <= 4 ... (cone de 3 hexes de largura)
            { "Breath lightning dealing *0 lightning damage to all enemies in a cone. ",
              "\n<color=#C8B090>The cone reaches 4 hexes from you.</color>" },
            // Charge - o texto dava a FORMA mas nao o alcance. Fonte: campo `alvos` do
            // `ActionProps` (blast/rsel): rsel=Source.Cell.IsInSixLine(Cell, 7) && Source.Cell.HasDirectPath(Cell)
            { "Charges to the target and deals *0 weapon damage to all enemies in your path.",
              "\n<color=#C8B090>The path is a line of up to 7 hexes.</color>" },
            // Informacao que o texto nao dava e que o usuario observou em jogo: a corrente pode
            // voltar no MESMO alvo. Fonte no codigo (`ActionInfo`): `ProjectileChain` +
            // `ProjectileChainCount` + `ProjectileChainTarget` e, decisivo,
            // `public bool ChainSameTarget = true` - o mesmo alvo pode ser atingido de novo,
            // entao o "5" conta SALTOS, nao inimigos distintos. O teste do jogo corrobora:
            // ele tem dois inimigos e basta ("Chain Lightning chained to the second enemy").
            { "Conjures a lightning bolt that chains up to 5 enemies near the target dealing *0 lightning damage to each target.  ",
              "\n<color=#C8B090>The 5 counts the chain's HOPS, not different enemies: the bolt can hit the same enemy again, so with only two enemies in range it bounces between them.</color>" },
            // "Power of Mana" (`ManaPowerMod`) nao tinha explicacao em lugar nenhum.
            // Fonte: `num36 = properties.CostsMana ? source["ManaPowerMod"] : 0f` somado em
            // `num29`, que multiplica dano E cura (`num9 *= num46`). O JOGO usa o termo
            // "power of mana using abilities" em `Forbidden Power` e no proprio `Rainstorm`.
            { "Increase the mana cost of all skills by 20% and increase the power of mana using skills by 40%.",
              "\n<color=#C8B090>Power of Mana increases the damage and healing of abilities that cost Mana.\nIt does not change how much Mana they cost, it does nothing for abilities that cost no Mana,\nand it does not change the duration or the bonuses of the statuses those abilities apply.</color>" },
            // "Power of Mana" (`ManaPowerMod`) nao tinha explicacao em lugar nenhum.
            // Fonte: `num36 = properties.CostsMana ? source["ManaPowerMod"] : 0f` somado em
            // `num29`, que multiplica dano E cura (`num9 *= num46`). O JOGO usa o termo
            // "power of mana using abilities" em `Forbidden Power` e no proprio `Rainstorm`.
            { "Increase the mana cost of all skills by an additional 30% and increase the power of mana using skills by an additional 60%.",
              "\n<color=#C8B090>Power of Mana increases the damage and healing of abilities that cost Mana.\nIt does not change how much Mana they cost, it does nothing for abilities that cost no Mana,\nand it does not change the duration or the bonuses of the statuses those abilities apply.</color>" },
            // "Power of Mana" (`ManaPowerMod`) nao tinha explicacao em lugar nenhum.
            // Fonte: `num36 = properties.CostsMana ? source["ManaPowerMod"] : 0f` somado em
            // `num29`, que multiplica dano E cura (`num9 *= num46`). O JOGO usa o termo
            // "power of mana using abilities" em `Forbidden Power` e no proprio `Rainstorm`.
            { "Calls down a magical rain that increases potency of Mana using abilities by 50% for allies within the area. Lasts 2 turns.",
              "\n<color=#C8B090>Power of Mana increases the damage and healing of abilities that cost Mana.\nIt does not change how much Mana they cost, it does nothing for abilities that cost no Mana,\nand it does not change the duration or the bonuses of the statuses those abilities apply.</color>" },
            // OMISSAO (nao mentir por omissao): o efeito real e
            // `Mathf.Min(Target.Health - 1, Target['MaxHealth'] * .1f)`. Os 10% do texto
            // estao certos, mas o `Min` com `Health - 1` garante que NAO MATA - e o texto
            // nao dizia. Muda a decisao de quem hesita em usar num aliado quase morto.
            { "Removes all negative statuses from friendly target but inflicts 10% of target's maximum health as fire damage. Can be used when Disabled.",
              "\n<color=#C8B090>This cannot reduce the target below 1 health.</color>" },
            // ---- Escala por NÍVEL (RV-8b-2g) ----
            // Fonte: código do jogo. `GetFlatDamageValue(level, rarity) =
            // Mathf.Ceil(FlatDamageNodes.GetMultipler((int)level) * GetStatRarityMod(rarity))`
            // — é uma CURVA DE NÍVEL, não um atributo. O valor atual já aparece na tooltip
            // (é o [0]); o que faltava era dizer COM O QUE ele escala, que era a pergunta
            // legítima do jogador ("invisto em Might para isso melhorar?").
            // São as 5 skills do jogo que usam essa curva (Huntsman I/II, Thorns I/II e
            // Vengeful Shadows); a chave "Physical damage increased by [0]." cobre as duas
            // Huntsman porque as duas escalam igual.
            { "Grants [0] Return Physical Damage.",  "\n<color=#C8B090>Scales with your character level.</color>" },
            { "Grants an additional [0] Return Physical Damage.",  "\n<color=#C8B090>Scales with your character level.</color>" },
            { "Grants [0] Return Shadow Damage.",  "\n<color=#C8B090>Scales with your character level.</color>" },
            { "Physical damage increased by [0].",  "\n<color=#C8B090>Scales with your character level.</color>" },

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
              "\n<color=#C8B090>Scales with your character level.</color>" },
            { "Damage caused steals [0] points of @Dexterity@. Lasts the entire battle. Stacks up to 10 times.",
              "\n<color=#C8B090>Scales with your character level.</color>" },
            { "Damage caused steals [0] points of @Intelligence@. Lasts the entire battle. Stacks up to 10 times.",
              "\n<color=#C8B090>Scales with your character level.</color>" },
            { "Damage caused steals [0] points of @Might@. Lasts the entire battle. Stacks up to 10 times.",
              "\n<color=#C8B090>Scales with your character level.</color>" },
            { "Envelopes the target in living vines that increase @armor@ and @magic armor@ by [0] and causes the target to regenerate *0 @health@ each turn.",
              "\n<color=#C8B090>Scales with your character level.</color>" },
            { "Increases all attributes by [0]. In addition, 10% of your highest attribute value is added to all other attributes.  Current Bonus: [1]",
              "\n<color=#C8B090>Scales with your character level.</color>" },
            { "Encases the friendly target in a dome of ice granting [0] Armor and Magic Armor for the duration. Immobilizes the target.",
              "\n<color=#C8B090>Scales with your character level.</color>" },

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
              "\n<color=#C8B090>One is summoned at random:\n- Raven: Melee Attack, Evasion\n- Raccoon: Melee Attack, Steal Action\n- Coyote: Melee Attack, Cripple\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },
            { "Summons a Stag, Wolf, or Boar to fight for you.",
              "\n<color=#C8B090>One is summoned at random:\n- Stag: Stunning Kick, Melee Attack\n- Wolf: Melee Attack, Howl\n- Boar: Melee Attack, Fracture\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },
            { "Summons a Bear, Moose, or Panther to fight for you.",
              "\n<color=#C8B090>One is summoned at random:\n- Bear (a Grizzly): Stunning Slam, Wild Cleave\n- Moose: Ground Slam, Melee Attack\n- Panther: Shadow Walk, Melee Attack\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },
            { "Summons a Tundra Wolf to fight for you.",
              "\n<color=#C8B090>Tundra Wolf: Melee Attack, Howl\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },
            { "Summons a Dire Wolf to fight for you.",
              "\n<color=#C8B090>Dire Wolf: Melee Attack, Blood Howl\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },
            { "Summon a grizzly to fight your enemies.",
              "\n<color=#C8B090>Grizzly: Stunning Slam, Wild Cleave\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },
            { "Summon a wolf to fight your enemies.",
              "\n<color=#C8B090>Wolf: Melee Attack, Howl\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },
            { "Summon a Raven to fight your enemies. ",
              "\n<color=#C8B090>Raven: Melee Attack, Evasion\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },
            { "Raise an Undead Ranger to fight by your side.",
              "\n<color=#C8B090>Undead Ranger: Ranged Attack, Hide In Shadows\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },
            { "Raise an Undead Berserker to fight by your side.",
              "\n<color=#C8B090>Undead Berserker: Bleeding Cleave\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>" },

            // Brambles e Ice Wall NAO invocam bicho: sao objetos destrutiveis que bloqueiam
            // hexes. Passam pelo MESMO caminho de beneficio dos bichos (CreateDestructible
            // -> ProcessSummonMasterStats, com `casterStatsToBenefitFrom` setado), entao
            // tambem ganham Might/Int. A diferenca que importa e outra: entram com
            // `addToSummonList: false` - NAO contam como summon, e efeitos que contam
            // invocacoes (Ecosystem) nao os veem. Por isso a frase deles fala de "nao conta
            // como summon" em vez de repetir a dos bichos.
            // A flag `BenefitFromCasterStats` e lida SO neste caminho de destrutivel (l.41998
            // -> CreateDestructible): NAO governa os bichos, que recebem os efeitos do dono
            // incondicionalmente no CreateSummon. Chama-la de "herdaStats" foi rotulo meu e
            // induzia a conclusao errada ("nao herda = nao escala").
            { "Summon brambles to block 4 hexes. Attackers will take physical damage when striking the brambles. Lasts 4 turns.",
              "\n<color=#C8B090>Benefits from your Might and Intelligence, but does not count as a summon.</color>" },
            { "Summon pillars of ice to block 4 hexes blocking enemy's line of sight. Attackers take cold damage.  Lasts 4 turns.",
              "\n<color=#C8B090>Benefits from your Might and Intelligence, but does not count as a summon.</color>" },

            // ---- Omissao: o texto nao pode estar certo pela METADE (RV-8b-3, 29/09) ----
            // Regra do usuario: se o resultado depende de algo que o texto nao diz, e defeito.
            // Achado por tools/check_omissao.py (classes O1..O6).
            // Ascendancy: o status concede 20% e DURA 5 TURNOS; a skill so dizia o 20%.
            { "Increases the target allies' stats by 20%.",
              "\n<color=#C8B090>Lasts 5 turns.</color>" },
            // Touch of Chaos: REVERTIDO a pedido do usuario (29/09). A arvore do Chaos e
            // divertida justamente por NAO revelar os resultados - Coin of Chaos, Benevolence,
            // Malevolence, Hurting e Helping seguem omitidos DE PROPOSITO. Nao "corrigir"
            // isto de novo: e design, nao omissao. Ver a excecao do Chaos na regra de omissao.

            // ---- O que INFLUENCIA a cura e o dano holy (arvore Light, 29/09) ----
            // Fonte: GetActionDamage, l.38843-38859. O multiplicador da cura e o MESMO do
            // dano holy:
            //     float num24 = source["DamageModHealing"];         // <- "Holy Power"
            //     float num26 = target?["HealingReceivedBonus"];
            //     num7 *= 1f + num24 / 100f;    // dano holy
            //     num9 *= 1f + num24 / 100f;    // cura
            //     num9 *= 1f + num26 / 100f;    // cura, pelo lado do ALVO
            // A BASE da cura vem de `Source.SpellPower('Light')` - e `SpellPower(type)`
            // devolve **`AttackPower`** (l.36040): entao escala com arma/Might, NAO com
            // Inteligencia. As curas por % de vida (`Healing Hand`, `Divine Intervention`)
            // nao tem essa base e por isso levam so a linha do Holy Power.
            // "Holy Power" e o nome que o PROPRIO JOGO usa: `Empowered Light` diz "Increases
            // Holy Power and Healing Received by 10%" e o efeito dela e `DamageModHealing` -
            // o mesmo atributo que multiplica a cura aqui.
            { "Restores target's health by *0.",
              "\n<color=#C8B090>Healing scales with your Attack Power and Holy Power.\nReduced by effects that lower the target's healing received.</color>" },
            { "Restores *0 health to all allies within 2 hexes of target.",
              "\n<color=#C8B090>Healing scales with your Attack Power and Holy Power.\nReduced by effects that lower the target's healing received.\nThe 2-hex area is centred on the chosen TARGET, not on the caster.</color>" },
            { "Target restores *0 health per turn. ",
              "\n<color=#C8B090>Healing scales with your Attack Power and Holy Power.\nReduced by effects that lower the target's healing received.</color>" },
            { "All allies within 3 hexes of you heal for *0 per turn. ",
              "\n<color=#C8B090>Healing scales with your Attack Power and Holy Power.\nReduced by effects that lower the target's healing received.</color>" },
            { "The caster reaches out in aid healing 30% of target's maximum health.",
              "\n<color=#C8B090>Healing scales with your Holy Power.\nReduced by effects that lower the target's healing received.</color>" },
            { "Restores the target to full health.",
              "\n<color=#C8B090>Healing scales with your Holy Power.\nReduced by effects that lower the target's healing received.</color>" },
            { "Summons a radiant light applying {STA=Blind} to the target dealing *0 Holy damage.",
              "\n<color=#C8B090>Damage scales with your Attack Power and Holy Power.</color>" },
            { "Breathe out a stream of holy light dealing *0 holy damage to all enemies and healing *0 to all allies in range.",
              "\n<color=#C8B090>Damage and healing scale with your Attack Power and Holy Power.\nHealing is reduced by effects that lower the target's healing received.</color>" },
            { "Expel a powerful celestial light blinding enemies and dealing *0 holy damage to all enemies and healing *1 to all allies in range.",
              "\n<color=#C8B090>Damage and healing scale with your Attack Power and Holy Power.\nHealing is reduced by effects that lower the target's healing received.</color>" },
            // Fechamento do lote da Light (29/09): quatro que tambem escalam e nao diziam.
            // `Holy Ground` era o caso mais enganoso - o STATUS dele guarda o valor na chave
            // `HolyDamage`, mas o teste do proprio jogo prova que CURA:
            //   Assert(caster.Health > hp, "Holy Ground did not heal the caster standing on it")
            // A chave e so o slot de armazenamento; o multiplicador de Holy Power entra
            // igual (num7 *= 1 + DamageModHealing/100).
            { "Consecrate an area of ground to heal allies that stand upon it. Heals *0 per turn for 3 turns. ",
              "\n<color=#C8B090>Healing scales with your Attack Power and Holy Power.</color>" },
            { "Any target you heal with Cure, Regenerate, Healing Hand, Mass Cure, or Divine Intervention also receives an additional healing over time effect restoring *0 health for 3 turns.",
              "\n<color=#C8B090>Healing scales with your Attack Power and Holy Power.</color>" },
            { "Calls down a shield that protects the target absorbing *0 damage. ",
              "\n<color=#C8B090>Absorption scales with your Attack Power and Holy Power.</color>" },
            { "Conjures a shield imbued with holy flame absorbing *0 damage. Upon shield depletion, it explodes and deals *0 holy damage to all foes in a 3 hex radius.",
              "\n<color=#C8B090>Damage and absorption scale with your Attack Power and Holy Power.</color>" },

            // ---- Explicações de mecânica: powerups e status (BT-3..BT-8) ----
            // Fonte: o código do jogo (Assembly-CSharp, decompilado). Cada bloco abaixo
            // diz no próprio comentário qual atributo/método confirma a mecânica.
            { "+ 20% increased Treasure Find",  "\n<color=#C8B090>Increases the chance for enemies to drop items. Does not affect item rarity. Stacks with your party.</color>" },
            { "+ 40% increased Treasure Find",  "\n<color=#C8B090>Increases the chance for enemies to drop items. Does not affect item rarity. Stacks with your party.</color>" },
            { "+ 60% increased Treasure Find",  "\n<color=#C8B090>Increases the chance for enemies to drop items. Does not affect item rarity. Stacks with your party.</color>" },
            { "+ 80% increased Treasure Find",  "\n<color=#C8B090>Increases the chance for enemies to drop items. Does not affect item rarity. Stacks with your party.</color>" },
            { "+ 100% increased Treasure Find",  "\n<color=#C8B090>Increases the chance for enemies to drop items. Does not affect item rarity. Stacks with your party.</color>" },

            // Gold Find — MECÂNICA VERIFICADA NO CÓDIGO (confirmação empírica via RoguelikeDebugger):
            //   - ApplyGoldModifiers lê character["GoldMod"] somado à party e multiplica o ouro
            //   - usado na distribuição de ouro pós-batalha (PostBattleManager), recompensas de
            //     aventura/quest e ouro de eventos
            //   - "GoldMod" é um asset CharacterAttribute; efeitos de powerup viram contribuições
            //     de atributo (mecanismo provado na BT-3)
            { "+ 10% increased Gold Find",  "\n<color=#C8B090>Increases the gold you earn. Stacks with your party.</color>" },
            { "+ 20% increased Gold Find",  "\n<color=#C8B090>Increases the gold you earn. Stacks with your party.</color>" },
            { "+ 30% increased Gold Find",  "\n<color=#C8B090>Increases the gold you earn. Stacks with your party.</color>" },
            { "+ 40% increased Gold Find",  "\n<color=#C8B090>Increases the gold you earn. Stacks with your party.</color>" },
            { "+ 50% increased Gold Find",  "\n<color=#C8B090>Increases the gold you earn. Stacks with your party.</color>" },

            // Damage and Healing — VERIFICADO: soma no atributo "DamageMod" base, que entra
            // em (1 + (DamageMod + DamageMod<Tipo> + ManaPowerMod)/100) × (1+AbilityPower/100)
            // para TODOS os tipos de dano E para a cura (DamageModHealing usa a mesma base).
            { "+ 5% to Damage and Healing",  "\n<color=#C8B090>Increases all damage you deal and all healing you do.</color>" },
            { "+ 10% to Damage and Healing",  "\n<color=#C8B090>Increases all damage you deal and all healing you do.</color>" },
            { "+ 15% to Damage and Healing",  "\n<color=#C8B090>Increases all damage you deal and all healing you do.</color>" },
            { "+ 20% to Damage and Healing",  "\n<color=#C8B090>Increases all damage you deal and all healing you do.</color>" },
            { "+ 25% to Damage and Healing",  "\n<color=#C8B090>Increases all damage you deal and all healing you do.</color>" },

            // Damage Reduction — VERIFICADO: atributo "DamageReduction" vira camada
            // multiplicativa (1 - (DamageReduction + Resilience + TakeCover)/100) na cadeia
            // de redução de dano. Texto GERADO DINAMICAMENTE (BuildDamageReductionNote) com
            // a ordem real do GlobalSettings (padrão: redução geral → resists → armadura).

            // Movement — VERIFICADO: soma ao atributo "FreeMovementPoints" (movimento por turno).
            // (RV-5: versão não-redundante — o original já diz "additional movement")
            { "Gain 1 additional movement",  "\n<color=#C8B090>Each movement point lets you move one extra hex per turn.</color>" },
            { "Gain 2 additional movement",  "\n<color=#C8B090>Each movement point lets you move one extra hex per turn.</color>" },

            // Range — VERIFICADO: o powerup alimenta "RangeTypeAdderRanged" (o melee não
            // muda — dump: RangeMelee=0, RangeRanged=2 com Lv2). Texto reflete ranged.
            { "Gain 1 additional range",  "\n<color=#C8B090>Increases the range of your ranged attacks and skills. Does not apply to certain skills.</color>" },
            { "Gain 2 additional range",  "\n<color=#C8B090>Increases the range of your ranged attacks and skills. Does not apply to certain skills.</color>" },

            // Skill Options — VERIFICADO: RoguelikeManager.GetSkillChoices(numOpcoesBase +
            // character["AdditionalRoguelikeSkillOptions"]) → mais opções na escolha de skill.
            { "Skill Options +1",  "\n<color=#C8B090>Increases the number of skill choices offered when leveling up.</color>" },
            { "Skill Options +2",  "\n<color=#C8B090>Increases the number of skill choices offered when leveling up.</color>" },

            // Attribute Points — VERIFICADO: UnspentStatPoints = base + (Level-1) ×
            // (NumStatsPerNewLevel + AdditionalRoguelikeAttributesPointsPerLevel).
            { "Attribute Points Per Level +1",  "\n<color=#C8B090>Grants additional attribute points each time you level up.</color>" },
            { "Attribute Points Per Level +2",  "\n<color=#C8B090>Grants additional attribute points each time you level up.</color>" },
            { "Attribute Points Per Level +3",  "\n<color=#C8B090>Grants additional attribute points each time you level up.</color>" },

            // Resists — VERIFICADO: dano do elemento × (1 - Resist/100), camada multiplicativa
            // na cadeia de redução (case DamageReductionCalcOrder.Resists em ApplyAction).
            { "[[ResistCold]] +10%",  "\n<color=#C8B090>Reduces Cold damage you take.</color>" },
            { "[[ResistCold]] +15%",  "\n<color=#C8B090>Reduces Cold damage you take.</color>" },
            { "[[ResistCold]] +20%",  "\n<color=#C8B090>Reduces Cold damage you take.</color>" },
            { "[[ResistFire]] +10%",  "\n<color=#C8B090>Reduces Fire damage you take.</color>" },
            { "[[ResistFire]] +15%",  "\n<color=#C8B090>Reduces Fire damage you take.</color>" },
            { "[[ResistFire]] +20%",  "\n<color=#C8B090>Reduces Fire damage you take.</color>" },
            { "[[ResistLightning]] +10%",  "\n<color=#C8B090>Reduces Lightning damage you take.</color>" },
            { "[[ResistLightning]] +15%",  "\n<color=#C8B090>Reduces Lightning damage you take.</color>" },
            { "[[ResistLightning]] +20%",  "\n<color=#C8B090>Reduces Lightning damage you take.</color>" },
            { "[[ResistPhysical]] +10%",  "\n<color=#C8B090>Reduces Physical damage you take.</color>" },
            { "[[ResistPhysical]] +15%",  "\n<color=#C8B090>Reduces Physical damage you take.</color>" },
            { "[[ResistPhysical]] +20%",  "\n<color=#C8B090>Reduces Physical damage you take.</color>" },

            // Summon Damage & Health — VERIFICADO: atributos SummonDamageMod/SummonHealthMod.
            { "+ 5% to Summon Damage and Health",  "\n<color=#C8B090>Increases the damage and health of your summoned creatures.</color>" },
            { "+ 10% to Summon Damage and Health",  "\n<color=#C8B090>Increases the damage and health of your summoned creatures.</color>" },
            { "+ 15% to Summon Damage and Health",  "\n<color=#C8B090>Increases the damage and health of your summoned creatures.</color>" },
            { "+ 20% to Summon Damage and Health",  "\n<color=#C8B090>Increases the damage and health of your summoned creatures.</color>" },
            { "+ 25% to Summon Damage and Health",  "\n<color=#C8B090>Increases the damage and health of your summoned creatures.</color>" },

            // Skill Tree Removal — VERIFICADO: remove árvores do pool de escolhas;
            // MinimumTreesRemaining=4; texto "can only be chosen at level 1" vem do próprio jogo.
            { "Skill Tree Removals +1",  "\n<color=#C8B090>Lets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen.</color>" },
            { "Skill Tree Removals +2",  "\n<color=#C8B090>Lets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen.</color>" },
            { "Skill Tree Removals +3",  "\n<color=#C8B090>Lets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen.</color>" },
            { "Skill Tree Removals +4",  "\n<color=#C8B090>Lets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen.</color>" },
            { "Skill Tree Removals +5",  "\n<color=#C8B090>Lets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen.</color>" },
            { "Skill Tree Removals +6",  "\n<color=#C8B090>Lets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen.</color>" },
            { "Skill Tree Removals +7",  "\n<color=#C8B090>Lets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen.</color>" },
            { "Skill Tree Removals +8",  "\n<color=#C8B090>Lets you remove skill trees from your pool of skill choices (at least 4 trees remain). Can only be chosen at select party screen.</color>" },
        };

        // Primeiras correções reais de texto — apenas digitação/espaçamento observados
        // no jogo, sem nenhuma afirmação de gameplay. Chave = texto original exato.
        private static readonly Dictionary<string, string> TextFixes = new Dictionary<string, string>
        {
            // DEFEITO DE TEXTO: o asset exige o proximo alvo dentro de 3 hexes
            // (`chainAlvo=... Cell.InRange(LastCell, 3)`), nao 2.
            { "Dash to an enemy dealing *0 weapon damage then quickly dash to an enemy within 2 hexes to strike again. Strikes up to 4 times.  Each time you strike a target it increases your dodge chance by 8%.  Lasts 2 turns. ",
              "Dash to an enemy dealing *0 weapon damage then quickly dash to an enemy within 3 hexes to strike again. Strikes up to 4 times.  Each time you strike a target it increases your dodge chance by 8%.  Lasts 2 turns. " },
            // DEFEITO DE TEXTO: idem `Dodging Strikes` (`Cell.InRange(LastCell, 3)`).
            { "Dash to an enemy dealing *0 weapon damage then quickly dash to an enemy within 2 hexes to strike again. Strikes up to 4 times.  Each time you hit increases the damage of Power Strikes by 50%.",
              "Dash to an enemy dealing *0 weapon damage then quickly dash to an enemy within 3 hexes to strike again. Strikes up to 4 times.  Each time you hit increases the damage of Power Strikes by 50%." },
            // DEFEITO DE TEXTO (2 em 1): "up to 4 times" com `DashMaxChainCount=3` (os irmaos
            // dizem 4 E tem 4, o laco `DashChainCount < DashMaxChainCount` produz
            // exatamente o campo) e "within 2 hexes" com `InRange(LastCell, 3)`
            // (`InRange(c, n) => Distance <= n`). Se a dev subir o asset, esta chave sai.
            { "Dash to an enemy dealing *0 weapon damage then quickly dash to an enemy within 2 hexes to strike again. Strikes up to 4 times.",
              "Dash to an enemy dealing *0 weapon damage then quickly dash to an enemy within 3 hexes to strike again. Strikes up to 3 times." },
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
                // Haunt: o texto dizia "Lifesteals for 6%" e o codigo faz
                // `SourceStored['HealingForced'] = Source['MaxHealth'] * .025f` - 2,5%.
                // Alem disso o PROPRIO texto do status diz 8%: os tres numeros divergiam.
                // Vale o codigo (regra do projeto: ele vence em divergencia), entao o texto
                // da skill passa a dizer 2,5%. O 8% do status e inconsistencia de dados do
                // jogo e NAO se conserta por aqui: status nao estao no dicionario de
                // localizacao, e um campo bruto do asset (fica para o RV-9).
                "Deals *0 shadow damage to the target every turn for 3 turns. @Life Steals@ for 6%.   @Life Steal@ heals you for a percentage of your @max health@ each time you hit. Reduced for area of effect and no ap cost abilities.",
                "Deals *0 shadow damage to the target every turn for 3 turns. @Life Steals@ for 2.5%. @Life Steal@ heals you for a percentage of your @max health@ each time you hit. Reduced for area of effect and no ap cost abilities."
            },
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
                // O beneficio de Might/Int vale para TODO summon (o CreateSummon aplica
                // ProcessSummonMasterStats incondicionalmente); o que muda entre eles e o
                // que o bicho FAZ, nao se ele escala. Ver o bloco do Brambles abaixo.
                "Raise a Undead Wizard to fight by your side.",
                "Raise an Undead Wizard to fight by your side.\n<color=#C8B090>Undead Wizard: Bone Explosion, Consumption, Ghost Armor\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>"
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
                "Raise a skeletal archer to fight by your side.\n<color=#C8B090>Skeletal Archer: Ranged Attack\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>"
            },
            {
                "Summon a skeletal mage to fight by your side.",
                "Raise a skeletal mage to fight by your side.\n<color=#C8B090>Skeletal Mage: Frost Nova, Fireball, Twister, Ghost Armor\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>"
            },
            {
                "Summon a skeletal warrior to fight by your side.",
                "Raise a skeletal warrior to fight by your side.\n<color=#C8B090>Skeletal Warrior: Melee Attack, Cleave\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>"
            },
            {
                // Unico invocador com fecho diferente: 6 usam "by your side", 1 usava "for you".
                "Raise a Mighty Iron Golem to fight for you.",
                "Raise a Mighty Iron Golem to fight by your side.\n<color=#C8B090>Iron Golem: Ground Slam\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>"
            },
            {
                // Familia "Shapeshift *": 3 abrem com "Shapeshift into", esta abria com
                // "Gain the ability to shapeshift into" (mesma redacao, mais verbosa).
                // O "Scales with" tambem entra aqui (RV-8b-2i): a formula e
                // `10 * Source.Level`, e quem esta nas duas tabelas so executa a CORRECAO
                // - uma explicacao no TextAppends para este texto nunca rodaria.
                "Gain the ability to shapeshift into a powerful elemental @Dragonkin@. Empowers basic attack, grants new abilities, and resistance based on the color you choose. Increases @Armor@ by [0].",
                "Shapeshift into a powerful elemental @Dragonkin@. Empowers basic attack, grants new abilities, and resistance based on the color you choose. Increases @Armor@ by [0].\n<color=#C8B090>Scales with your character level.</color>"
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
                "Summons a Timber Wolf to fight for you.\n<color=#C8B090>Timber Wolf: Cripple, Melee Attack\nDoes not copy your attributes.\nYour Might raises its damage; your Intelligence, its health.</color>"
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
