using System;
using System.Collections.Generic;
using System.Text;
using System.Text.RegularExpressions;
using Burst2Flame;
using HarmonyLib;

namespace BetterTooltips.Patches
{
    /// <summary>
    /// CHL-1 (01/10) — SKILLS QUE INTERAGEM COM UM STATUS APARECEM NA TOOLTIP DESSE STATUS, com o
    /// valor lido do MOTOR e por um mecanismo GENERICO (nenhum `if` para Chill).
    ///
    /// O QUE A TOOLTIP DO JOGO JA DIZ E O QUE ELA OMITE (o defeito que este arquivo fecha):
    ///   * o status `Chilled` (o asset; censo `docs/cobertura/status.csv:71`) tem CINCO
    ///     `AttributeEffects` no asset, e TRES deles leem atributo do personagem que APLICOU o
    ///     status (`Source[...]`):
    ///       `DamageMod:Base:-(Source["ChilledDamageReduction"])`
    ///       `MaxHealth:Percentage:Source["Frostbite"] == 1 ? -5 : 0`
    ///       `Armor:Percentage:Source["InvulnerableWinter"] == 1 ? 5 : 0` (+ o irmao de MagicArmor)
    ///   * a DESCRICAO do status nao tem lugar nenhum para eles: o texto do asset e
    ///     "Movement points reduced by one per stack.  Lasts 2 turns.  Five stacks of Chilled freezes
    ///     the target." — sem `[N]`, sem `[[X]]`. O jogador com `Frostbite I` nao descobre, na
    ///     tooltip do Chilled, que as pilhas dele derrubam o dano do alvo.
    ///
    /// DE QUEM E O NUMERO (o ponto que ja custou uma reescrita no Flame): e do personagem do lado
    /// **SOURCE** do status — quem APLICOU o Chilled, ou seja quem tem a skill. Prova no MOTOR, nao
    /// por deducao: `Character.GetAttributeValueByMethod` monta os parametros do efeito do status como
    /// `gameFunctionParameters.Source = actionStatus3.Source; gameFunctionParameters.Target =
    /// actionStatus3.Target;` (decompilado l.37212-37214) e avalia o `Amount` com eles. E o teste de
    /// integracao do PROPRIO JOGO fecha o caso: `FrostbiteI` (decompilado l.183874-183884) aprende a
    /// skill no CASTER, confere o atributo NELE (`ChilledDamageReduction`, 2) e afirma que o ALVO
    /// perde 10 de `DamageMod` com 5 pilhas — o numero esta no caster e o efeito cai no alvo.
    /// NAO e o "personagem que esta vendo" que decide nada: a tooltip ja recebe o `Source` do status
    /// (`Tooltip.ShowActionStatusTooltip`, l.213903/214072) e e ELE que a formula le. Quando nao ha
    /// status vivo (ex.: a Ficha/fortune), o proprio motor poe ali o personagem em foco.
    ///
    /// O MECANISMO (generico, todo ele lido do asset; nada de tabela de nomes de skill):
    ///   1. no primeiro uso, indexa os status do jogo (`Game.Instance.ActionStatuses`) que tenham
    ///      `AttributeEffects` lendo atributo do SOURCE com a sintaxe `Source["X"]` — a MESMA do asset;
    ///   2. na tooltip, avalia a EXPRESSAO DO PROPRIO STATUS (`effect.Amount`) pelo interpretador do
    ///      jogo (`Game.TryParseWithEnglishCulture` e, se falhar, `Game.TryEval<float>`), com os
    ///      parametros que o motor usaria. Valor 0 (ou expressao nao avaliada) = SILENCIO: sem a
    ///      skill o atributo e 0 e a linha nao sai — nunca "0", nunca linha vazia;
    ///   3. o rotulo do item sao as skills do personagem do lado SOURCE que concedem o atributo lido
    ///      (`Character.Skills` + `CharacterInfo.SkillsAndAI[].Skill`, casando pelo NOME do atributo em
    ///      `SkillInfo.AttributeEffects`, como `CharacterEffectInfo.Matches`, l.319887, faz — ele NAO
    ///      olha `EffectTarget`). Sem skill conhecida, o rotulo cai no nome de tooltip do PROPRIO
    ///      motor (`CharacterAttribute.GetTooltipDisplayName`) — nenhuma atribuicao inventada;
    ///   4. a frase do valor vem por ATRIBUTO AFETADO (nunca por skill/status), com a procedencia
    ///      citada na tabela; atributo fora da tabela cai no nome do motor.
    ///
    /// Por que esta linha NAO e a de auras de shrine (`ShrineAuraPatch`) e nao a substitui: as NOVE
    /// auras de buff leem `Target["ShrineEffectBonus"]` nos `AttributeEffects` do status — o atributo
    /// da propria vitima — e o numero delas JA aparece na linha branca do shrine (o `[0]` da descricao,
    /// que o prefix do RV-22/RV-34 corrige). Aqui so entra leitura do **Source**, que a tooltip do
    /// status NAO mostra em lugar nenhum.
    ///
    /// NIV3-1R (01/10) — A RESSALVA QUE FALTAVA NA FRASE ACIMA. "As auras leem `Target[...]`" vale
    /// para as 9 com `AttributeEffects` (as de buff). **Flame e Decay tambem leem
    /// `Source["ShrineEffectBonus"]`**, so que na FORMULA DE DANO do proprio action (`* Aura Proc`) —
    /// FORA do `AttributeEffects`, que e o UNICO lugar que o indice deste patch varre. A distincao
    /// importa para quem for reusar a frase: o criterio do indice e o `AttributeEffects`, nao "aura
    /// de shrine" em geral.
    ///
    /// SEGURANCA (a licao do incidente de 30/09): a assinatura real do alvo e
    ///   ApplyDescriptionExpressions(string text, string[] expressions,
    ///                               GameFunctionParameters gameFunctionParameters,
    ///                               float fontSize, float rangeMod = 0f)
    /// O patch declara a assinatura EXPLICITA por TIPO no [HarmonyPatch] e le os DOIS argumentos que
    /// usa pelo NOME do original (`string text`, `ref GameFunctionParameters gameFunctionParameters`)
    /// — nenhum parametro por posicao (`__0`/`__2`). A ligacao por nome e a do proprio Harmony
    /// (`PatchArgumentExtensions.GetArgumentIndex` = `Array.IndexOf` dos nomes do metodo do jogo) e o
    /// slot 2 e o `GameFunctionParameters`, NUNCA o 3 (float fontSize): foi um `__3` (o slot do float)
    /// lido como objeto que derrubou o jogo com 112 NullReferenceException. Com o nome, uma renomeacao
    /// no jogo faz o Harmony RECUSAR o gancho (com o nome no log) em vez de ler o slot errado em
    /// silencio. O postfix e o MESMO funil por onde passam todos os tooltips de
    /// skill/status/powerup/aura — o corpo inteiro e try/catch e, em qualquer falha, o texto segue
    /// para o jogo como estava.
    ///
    /// NAO duplica: a linha so sai quando o texto ainda nao a tem, e o `__result` e remontado a cada
    /// chamada (nada acumula entre frames de hover).
    /// </summary>
    [HarmonyPatch]
    public static class StatusSkillSynergyPatch
    {
        /// <summary>
        /// O gancho. Roda para TODA tooltip do jogo: as duas primeiras checagens (o status vivo e o
        /// indice de textos) sao as baratas, e qualquer falha devolve o texto intacto.
        /// </summary>
        [HarmonyPatch(typeof(Tooltip), nameof(Tooltip.ApplyDescriptionExpressions),
            new Type[] { typeof(string), typeof(string[]), typeof(GameFunctionParameters), typeof(float), typeof(float) })]
        [HarmonyPostfix]
        private static void AcrescentaLinhaDeSinergia(string text, ref string __result, ref GameFunctionParameters gameFunctionParameters)
        {
            try
            {
                if (__result == null || __result.Length == 0)
                {
                    return;
                }
                if (__result.IndexOf(Marcador, StringComparison.Ordinal) >= 0)
                {
                    // Ja tem o bloco (defensivo: nunca anexar duas vezes no mesmo texto).
                    return;
                }
                StatusComSinergia alvo = StatusDaTooltip(text, __result, gameFunctionParameters);
                if (alvo == null)
                {
                    return;
                }

                // (2) DE QUEM E O NUMERO: o MESMO personagem que o motor le na expressao do status.
                // Com o status vivo, o Source DELE (l.37212-37214); sem status vivo, o Source que o
                // proprio chamador montou (a Ficha/fortune passa o personagem em foco).
                Character dono = gameFunctionParameters.ActionStatus != null ? gameFunctionParameters.ActionStatus.Source : gameFunctionParameters.Source;
                if (dono == null)
                {
                    Marca($"status '{alvo.Info.Name}': sem personagem do lado SOURCE — sem linha (nada estimado)");
                    return;
                }

                string bloco = Bloco(alvo, dono, gameFunctionParameters);
                if (string.IsNullOrEmpty(bloco))
                {
                    return;
                }
                __result = __result + bloco;
            }
            catch (Exception ex)
            {
                // Nunca propagar: o texto vai para a tela como o jogo o montou.
                Plugin.Log.LogWarning($"[CHL-1] postfix falhou (texto intacto): {ex.GetType().Name}: {ex.Message}");
            }
        }

        /// <summary>Marcador do bloco (prefixo da linha azul; usado tambem como trava contra duplicata
        /// e pelo log). Mesma familia visual da linha de auras ativas (`LocalizePatch`), que usa o
        /// marcador irmao "Your active shrine auras:" — os DOIS sao o NIVEL 3 da convencao
        /// (docs/TEXTO-TOOLTIPS.md), na cor azul resolvida por `LocalizePatch.CorDaLinhaDeAuras()`.
        /// `internal` porque o `LocalizePatch` precisa dele para NAO repintar este bloco com a cor do
        /// nivel 2 quando a paleta azul nao pudo ser lida.</summary>
        internal const string Marcador = "Your skills on this status:";

        /// <summary>
        /// O bloco (ou null quando nao ha nada provado a mostrar). Uma linha, itens separados por ';',
        /// terminada em ponto: o NOME vem PRIMEIRO, o valor DEPOIS — a skill que o causa (ou, sem
        /// skill, o nome do atributo pelo motor) abre o item, e o valor com sinal segue colado, ex.:
        /// "Frostbite I −2% damage per stack". Mesma ordem do irmao aprovado da linha de auras
        /// ("Dodge +40%"); nunca texto longo.
        /// </summary>
        private static string Bloco(StatusComSinergia alvo, Character dono, GameFunctionParameters parametros)
        {
            List<string> itens = new List<string>();
            foreach (EfeitoDoStatus efeito in alvo.Efeitos)
            {
                float valor;
                if (!Avalia(efeito.Expressao, dono, parametros, out valor))
                {
                    Marca($"status '{alvo.Info.Name}': expressao '{efeito.Expressao}' nao avaliada pelo motor — efeito fora da linha");
                    continue;
                }
                if (valor == 0f)
                {
                    // Sem a skill o atributo lido e 0: o jogo nao aplica nada e a linha NAO sai.
                    Marca($"status '{alvo.Info.Name}': '{efeito.Expressao}' = 0 em {Nome(dono)} — silencio (sem a skill)");
                    continue;
                }

                List<string> nomes = SkillsQueConcedem(dono, efeito.AtributosLidos);
                string rotulo = nomes.Count > 0
                    ? string.Join(" + ", nomes.ToArray())
                    : NomeDoAtributo(efeito.AtributosLidos[0]);

                string item = rotulo + " " + ComSinal(valor) + FraseDoAfetado(efeito.AtributoAfetado, efeito.Metodo)
                    + (efeito.PerStack ? " per stack" : "");
                if (!itens.Contains(item))
                {
                    itens.Add(item);
                }
                Marca($"status '{alvo.Info.Name}' char={Nome(dono)}: {efeito.Expressao} = {valor.ToString("0.#")}"
                    + $" -> '{item}' (skills=[{string.Join(", ", nomes.ToArray())}])");
            }

            if (itens.Count == 0)
            {
                return null;
            }
            return "\n<color=#" + LocalizePatch.CorDaLinhaDeAuras() + ">" + Marcador + " "
                + string.Join("; ", itens.ToArray()) + ".</color>";
        }

        /// <summary>
        /// Qual status esta tooltip descreve.
        ///   (a) o caminho DETERMINISTA: o status VIVO que o chamador passou
        ///       (`GameFunctionParameters.ActionStatus` = `sourceStatus` em
        ///       `Tooltip.ShowActionStatusTooltip`, l.213903/214072) — e o MESMO objeto que o motor
        ///       percorre em `GetAttributeValueByMethod`, entao nao ha o que casar por texto;
        ///   (b) a reserva (Ficha/fortune/evento, onde o status vivo pode nao existir): casar o texto
        ///       que chegou contra a DESCRICAO do asset, normalizada — so contra os status que tem
        ///       leitura do SOURCE no indice (poucos), o que torna falso positivo improvavel.
        /// </summary>
        private static StatusComSinergia StatusDaTooltip(string textoOriginal, string resultado, GameFunctionParameters parametros)
        {
            List<StatusComSinergia> indice = Indice();
            if (indice == null || indice.Count == 0)
            {
                return null;
            }

            if (parametros.ActionStatus != null && parametros.ActionStatus.ActionStatusInfo != null)
            {
                ActionStatusInfo info = parametros.ActionStatus.ActionStatusInfo;
                foreach (StatusComSinergia s in indice)
                {
                    // Referencia primeiro (o asset e o mesmo objeto); GUID depois, porque o motor
                    // pode entregar uma COPIA do `ActionStatusInfo` no status vivo — a copia carrega
                    // o mesmo `Guid` (campo do asset) e a linha continua saindo.
                    bool mesmoGuid = s.Info.Guid != Guid.Empty && s.Info.Guid == info.Guid;
                    if (ReferenceEquals(s.Info, info) || mesmoGuid)
                    {
                        Marca($"tooltip do status vivo '{info.Name}': caminho (a), pelo ActionStatus"
                            + $"{(ReferenceEquals(s.Info, info) ? "(referencia)" : "(guid)")}");
                        return s;
                    }
                }
                Marca($"tooltip do status vivo '{info.Name}': nao esta no indice (efeito sem leitura do SOURCE)"
                    + " — sem linha");
                return null;
            }

            string viaTexto = Normaliza(textoOriginal);
            string viaResultado = Normaliza(resultado);
            foreach (StatusComSinergia s in indice)
            {
                if ((viaTexto.Length > 0 && string.Equals(s.ChaveNormalizada, viaTexto, StringComparison.Ordinal))
                    || (viaResultado.Length > 0 && string.Equals(s.ChaveNormalizada, viaResultado, StringComparison.Ordinal)))
                {
                    Marca($"tooltip do status '{s.Info.Name}': vindo pela DESCRICAO (reserva (b))");
                    return s;
                }
            }
            return null;
        }

        // =====================================================================
        // O INDICE (uma vez por sessao; o jogo carrega os status incrementalmente)
        // =====================================================================

        /// <summary>Um `AttributeEffect` do status que le atributo do personagem que aplicou o status.</summary>
        private sealed class EfeitoDoStatus
        {
            public string AtributoAfetado;
            public CharacterEffectMethod Metodo;
            public string Expressao;
            public List<string> AtributosLidos;
            public bool PerStack;
        }

        private sealed class StatusComSinergia
        {
            public ActionStatusInfo Info;
            public string ChaveNormalizada;
            public List<EfeitoDoStatus> Efeitos;
        }

        private static List<StatusComSinergia> _indice;
        private static readonly Regex RefDeAtributo = new Regex(
            "(Source|Target)\\s*\\[\\s*[\"']([^\"']+)[\"']\\s*\\]", RegexOptions.Compiled);

        private static readonly Dictionary<string, string> _normalizadas = new Dictionary<string, string>();

        /// <summary>
        /// Os status cujos efeitos leem atributo do **SOURCE** (`Source["X"]` no `Amount`):
        /// e a direcao "a skill de quem aplicou muda o que o status faz no alvo".
        ///
        /// Fica de FORA, de proposito, o que nao se pode atribuir a uma skill:
        ///   * `Target["X"]` — leitura do atributo do PROPRIO portador (as 9 auras de buff leem
        ///     `Target["ShrineEffectBonus"]` assim, e o numero delas ja sai na descricao/linha de auras;
        ///     NIV3-1R: Flame e Decay, que leem `Source["ShrineEffectBonus"]`, o fazem na FORMULA DE
        ///     DANO do action — fora do `AttributeEffects`, logo fora do alcance deste indice);
        ///   * `Amount` com `{...}` — o motor substitui essas faixas por `BracketedValues` ANTES de
        ///     avaliar (l.37220-37230); sem reproduzir isso a avaliacao sairia errada, entao o efeito
        ///     fica fora (silencio) — nada de numero estimado;
        ///   * status que concede o proprio atributo que le (o Emblem of the Iron Fortress concede
        ///     `Armor` e le `Source["Armor"]`): isso e o status escalando com a propria concessao, nao
        ///     a skill de alguem.
        /// Falha de leitura nao cria indice vazio permanente: devolve null e tenta de novo no hover
        /// seguinte (os status carregam durante o loading).
        /// </summary>
        private static List<StatusComSinergia> Indice()
        {
            if (_indice != null)
            {
                return _indice;
            }
            try
            {
                List<ActionStatusInfo> status = Burst2Flame.Game.Instance?.ActionStatuses;
                if (status == null || status.Count == 0)
                {
                    return null;
                }

                List<StatusComSinergia> novo = new List<StatusComSinergia>();
                foreach (ActionStatusInfo info in status)
                {
                    if (info == null || info.AttributeEffects == null)
                    {
                        continue;
                    }

                    // Os atributos que o PROPRIO status concede ao portador (EffectTarget == Target e
                    // o unico bucket que o motor acumula, l.37207-37210) — usados para o excluir o
                    // caso "o status escala com a propria concessao".
                    HashSet<string> concedidos = new HashSet<string>();
                    foreach (CharacterEffectInfo e in info.AttributeEffects)
                    {
                        if (e != null && e.CharacterAttribute != null && e.EffectTarget == EffectTarget.Target)
                        {
                            concedidos.Add(e.CharacterAttribute.name);
                        }
                    }

                    List<EfeitoDoStatus> efeitos = new List<EfeitoDoStatus>();
                    foreach (CharacterEffectInfo efeito in info.AttributeEffects)
                    {
                        if (efeito == null || efeito.CharacterAttribute == null)
                        {
                            continue;
                        }
                        string expr = efeito.Amount;
                        if (string.IsNullOrEmpty(expr) || expr.IndexOf('{') >= 0)
                        {
                            continue;
                        }
                        List<string> lidos = new List<string>();
                        foreach (Match m in RefDeAtributo.Matches(expr))
                        {
                            if (!string.Equals(m.Groups[1].Value, "Source", StringComparison.Ordinal))
                            {
                                continue;
                            }
                            string atributo = m.Groups[2].Value;
                            if (string.IsNullOrEmpty(atributo) || concedidos.Contains(atributo) || lidos.Contains(atributo))
                            {
                                continue;
                            }
                            lidos.Add(atributo);
                        }
                        if (lidos.Count == 0)
                        {
                            continue;
                        }
                        efeitos.Add(new EfeitoDoStatus
                        {
                            AtributoAfetado = efeito.CharacterAttribute.name,
                            Metodo = efeito.CharacterEffectMethod,
                            Expressao = expr,
                            AtributosLidos = lidos,
                            // Regra do MOTOR: `parsed2 *= (method == Set) ? 1 : TotalStacks` (l.37263) —
                            // so o metodo `Set` nao escala por pilha; as pilhas do status multiplicam o resto.
                            PerStack = efeito.CharacterEffectMethod != CharacterEffectMethod.Set
                        });
                    }

                    if (efeitos.Count == 0)
                    {
                        continue;
                    }
                    novo.Add(new StatusComSinergia
                    {
                        Info = info,
                        ChaveNormalizada = Normaliza(info.Description),
                        Efeitos = efeitos
                    });
                }

                _indice = novo;
                List<string> nomes = new List<string>();
                foreach (StatusComSinergia s in novo)
                {
                    nomes.Add(s.Info.Name);
                }
                Marca($"[CHL-1] indice de sinergia status x skill: {novo.Count} status cujo efeito le atributo do SOURCE"
                    + $": [{string.Join(", ", nomes.ToArray())}]");
                return _indice;
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[CHL-1] indice falhou (tento de novo no proximo hover): {ex.GetType().Name}: {ex.Message}");
                return null;
            }
        }

        /// <summary>
        /// As skills que o personagem TEM e que concedem um dos atributos que a expressao le.
        ///
        /// CHL-2 (nit registrado aqui, SO comentario): este casamento e MAIS FROUXO que o do motor,
        /// nao um espelho exato. O filtro abaixo casa SO pelo NOME do atributo
        /// (`e.CharacterAttribute.name`), enquanto o `Matches` do motor (`CharacterEffect.Matches`,
        /// l.44712-44719; espelho de `CharacterEffectInfo.Matches`) exige os TRES de uma vez: o mesmo
        /// `CharacterAttribute` (por referencia), o mesmo `CharacterEffectMethod`
        /// E a mesma segunda passada (`SecondPass == secondPass`). Metodo e segunda passada NAO sao
        /// comparados aqui de proposito: o rotulo e uma ATRIBUICAO (qual skill concede o atributo),
        /// nao a avaliacao do proprio efeito — casar a skill por um efeito de mesmo atributo e
        /// metodo/passada diferentes e aceitavel, mas nunca se leia esta funcao como o `Matches`.
        ///
        /// `EffectTarget` e indiferente nos DOIS: o `Matches` do motor NAO olha o alvo, e por isso o
        /// filtro aqui tambem nao olha — o dump do proprio jogo mostra `Frostbite I` com
        /// `EffectTarget=Source` e `Frozen Core` com `EffectTarget=Target`, e o teste de integracao
        /// afirma o valor nos DOIS casos NO CASTER (l.183874/184138).
        ///
        /// `Character.Skills` cobre os dois caminhos do motor (l.32847: para IA e `CharacterInfo.Skills`,
        /// para o jogador e a lista aprendida, alimentada por `AddSkill`). `SkillsAndAI[].Skill` entra
        /// junto porque o `CharacterInfo.Skills` dos inimigos costuma vir VAZIO — sem essa uniao, um
        /// inimigo que aplica o status nao teria rotulo (o valor continuaria certo).
        /// </summary>
        private static List<string> SkillsQueConcedem(Character dono, List<string> atributosLidos)
        {
            List<string> nomes = new List<string>();
            try
            {
                List<SkillInfo> todas = new List<SkillInfo>();
                List<SkillInfo> aprendidas = dono.Skills;
                if (aprendidas != null)
                {
                    todas.AddRange(aprendidas);
                }
                CharacterInfo info = dono.CharacterInfo;
                if (info != null && info.SkillsAndAI != null)
                {
                    foreach (SkillAndAI sa in info.SkillsAndAI)
                    {
                        if (sa != null && sa.Skill != null && !todas.Contains(sa.Skill))
                        {
                            todas.Add(sa.Skill);
                        }
                    }
                }

                foreach (SkillInfo skill in todas)
                {
                    if (skill == null || skill.AttributeEffects == null)
                    {
                        continue;
                    }
                    foreach (CharacterEffectInfo e in skill.AttributeEffects)
                    {
                        if (e == null || e.CharacterAttribute == null)
                        {
                            continue;
                        }
                        if (!atributosLidos.Contains(e.CharacterAttribute.name))
                        {
                            continue;
                        }
                        string nome = !string.IsNullOrEmpty(skill.SkillName) ? skill.SkillName : skill.name;
                        if (!string.IsNullOrEmpty(nome) && !nomes.Contains(nome))
                        {
                            nomes.Add(nome);
                        }
                        break;
                    }
                }
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[CHL-1] leitura das skills falhou (rotulo cai no nome do motor): {ex.GetType().Name}: {ex.Message}");
                nomes.Clear();
            }
            return nomes;
        }

        /// <summary>
        /// Avalia a expressao do PROPRIO status como o motor faz ao acumular o efeito: primeiro numero
        /// puro (`Game.TryParseWithEnglishCulture`), senao `Game.TryEval` (a MESMA ordem de
        /// `Character.GetAttributeValueByMethod`, l.37256-37263).
        ///
        /// `dono` entra nas DUAS posicoes Source/Target de proposito? NAO: o `Source` e o personagem
        /// do lado SOURCE do status (quem a formula le) e o `Target` e o do proprio status. Trocar isso
        /// foi o defeito do Flame (RV-26 -> RV-34) — o numero tem de sair do personagem que a
        /// expressao aponta.
        /// </summary>
        private static bool Avalia(string expressao, Character dono, GameFunctionParameters parametros, out float valor)
        {
            valor = 0f;
            if (string.IsNullOrEmpty(expressao))
            {
                return false;
            }
            if (Burst2Flame.Game.TryParseWithEnglishCulture(expressao, out valor))
            {
                return true;
            }
            GameFunctionParameters p = parametros;
            p.Source = dono;
            return Burst2Flame.Game.TryEval<float>(expressao, p, out valor);
        }

        /// <summary>
        /// A frase do efeito, por ATRIBUTO AFETADO — nunca por skill nem por status: qualquer par
        /// (status x skill) que mexa no mesmo atributo sai com a MESMA redacao, e uma skill nova que
        /// passe a alimentar um desses atributos entra na linha sozinha.
        ///
        /// Procedencia de cada entrada (asset + teste do motor):
        ///   * `DamageMod` — o status `Chilled` aplica `DamageMod:Base:-(Source["ChilledDamageReduction"])`
        ///     (status.csv:71) e o texto da skill que concede o atributo diz exatamente
        ///     "Your stacks of chilled now reduce the targets damage by 2%." (skills.csv:173) — logo a
        ///     unidade do atributo e `%` e a grandeza e "damage". O teste do jogo: 5 pilhas com
        ///     `Frostbite I` = -10 de `DamageMod` (l.183881).
        ///   * `MaxHealth` — o status aplica `MaxHealth:Percentage:Source["Frostbite"] == 1 ? -5 : 0`
        ///     (status.csv:71) e o texto da skill diz "Each stack of chilled now reduces the target's
        ///     maxium health by 5%." (skills.csv:175); o teste do jogo: 5 pilhas = -25% (l.184138-184144).
        ///
        /// Atributo fora da tabela NAO ganha frase nova: sai o nome de tooltip do PROPRIO motor
        /// (`CharacterAttribute.GetTooltipDisplayName`, l.319847) — o mesmo criterio que o
        /// `ShrineAuraPatch` usa para atributo desconhecido. Nenhuma redacao inventada aqui.
        /// </summary>
        private static string FraseDoAfetado(string atributo, CharacterEffectMethod metodo)
        {
            switch (atributo)
            {
                case "DamageMod":
                    return "% damage";
                case "MaxHealth":
                    return "% Max Health";
            }
            // Fora da tabela, a UNIDADE vem do PROPRIO asset: o metodo `Percentage` do efeito e
            // porcentagem por definicao (a % do atributo afetado) e `CharacterAttribute.
            // OverrideAsPercentage` (campo do asset, l.319747+) declara os atributos exibidos em %.
            // O NOME e o do motor (`GetTooltipDisplayName`/`DisplayName`) — nunca um nome nosso.
            bool porcento = metodo == CharacterEffectMethod.Percentage || AtributoPorcento(atributo);
            return (porcento ? "% " : " ") + NomeDoAtributo(atributo);
        }

        /// <summary>`OverrideAsPercentage` do atributo, lido do asset pelo motor (false quando o
        /// atributo nao existe neste build — a unidade entao nao e inventada, sai sem o `%`).</summary>
        private static bool AtributoPorcento(string nome)
        {
            try
            {
                CharacterAttribute attr = Burst2Flame.Game.Instance?.GetAttribute(nome);
                return attr != null && attr.OverrideAsPercentage;
            }
            catch (Exception)
            {
                return false;
            }
        }

        /// <summary>Nome de exibicao do atributo, do PROPRIO motor (nunca um nome nosso).</summary>
        private static string NomeDoAtributo(string nome)
        {
            try
            {
                CharacterAttribute attr = Burst2Flame.Game.Instance?.GetAttribute(nome);
                if (attr != null)
                {
                    string exibido = attr.GetTooltipDisplayName();
                    if (!string.IsNullOrEmpty(exibido))
                    {
                        return exibido;
                    }
                    if (!string.IsNullOrEmpty(attr.DisplayName))
                    {
                        return attr.DisplayName;
                    }
                }
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[CHL-1] nome do atributo '{nome}' indisponivel: {ex.GetType().Name}: {ex.Message}");
            }
            return nome;
        }

        /// <summary>Valor com sinal explicito, no formato da linha de auras (RV-43/RV-45 do
        /// `ShrineAuraPatch`): "+" para positivo ou zero, "−" (U+2212) para negativo, uma casa quando
        /// houver fracao (o numero e resultado de FORMULA do motor, nao da ficha).</summary>
        private static string ComSinal(float v)
        {
            if (float.IsNaN(v) || float.IsInfinity(v))
            {
                return "0";
            }
            string n = Math.Abs(v).ToString("0.#");
            return (v < 0f ? "−" : "+") + n;
        }

        /// <summary>
        /// Chave de comparacao de uma descricao: sem tags de cor/marcacao, sem os tokens do tooltip
        /// (`[N]`, `[[X]]`, `{...}`) e sem espacos repetidos. Serve so a reserva (b) — o caminho
        /// principal nao casa texto nenhum.
        /// </summary>
        private static string Normaliza(string texto)
        {
            if (string.IsNullOrEmpty(texto))
            {
                return "";
            }
            if (_normalizadas.TryGetValue(texto, out string pronto))
            {
                return pronto;
            }
            string s = texto;
            try
            {
                s = Regex.Replace(s, "<[^>]*>", " ");
                s = Regex.Replace(s, "\\[\\[[^\\]]*\\]\\]", " ");
                s = Regex.Replace(s, "\\[[^\\]]*\\]", " ");
                s = Regex.Replace(s, "\\{[^\\}]*\\}", " ");
                s = Regex.Replace(s, "\\s+", " ").Trim().ToLowerInvariant();
            }
            catch (Exception)
            {
                s = texto;
            }
            if (_normalizadas.Count < 500)
            {
                _normalizadas[texto] = s;
            }
            return s;
        }

        private static string Nome(Character c)
        {
            try
            {
                return c != null && !string.IsNullOrEmpty(c.CharacterName) ? c.CharacterName : "(sem nome)";
            }
            catch (Exception)
            {
                return "(sem nome)";
            }
        }

        /// <summary>
        /// Marcador de vida + dedupe. O gancho roda a cada frame de hover — a linha de vida sai UMA
        /// vez, na primeira linha logada (e ela existe para o log provar que o gancho entrou).
        /// </summary>
        private static readonly HashSet<string> _marcas = new HashSet<string>();
        private static bool _vivo;

        private static void Marca(string linha)
        {
            try
            {
                if (_marcas.Count >= 300 || !_marcas.Add(linha))
                {
                    return;
                }
                if (!_vivo)
                {
                    _vivo = true;
                    Plugin.Log.LogInfo("[CHL-1] gancho de sinergia status x skill ativo em "
                        + "ApplyDescriptionExpressions (postfix)");
                }
                Plugin.Log.LogInfo("[CHL-1] " + linha);
            }
            catch
            {
                // log nunca pode derrubar nada
            }
        }
    }
}
