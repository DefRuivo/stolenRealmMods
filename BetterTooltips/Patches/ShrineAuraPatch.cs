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
    /// RV-23 (30/09) — a LINHA DE ACUMULADO ("Your active shrine auras: ...") foi REESCRITA:
    ///   (a) receptor: o MESMO resolvedor do prefix (`Tooltip.TooltipCharacter` ->
    ///       `Root.WorldCharacter` -> Source) — o WorldCharacter é vazio e nunca tem as auras;
    ///   (b) a aura mostrada é a DESTA tooltip (o status cuja descrição é o texto localizado), não a
    ///       soma de qualquer aura de shrine que o personagem tenha;
    ///   (c) os valores saem do `ActionStatusInfo.AttributeEffects` REAL do status, avaliado pelas
    ///       expressões do PRÓPRIO jogo (`Game.TryParseWithEnglishCulture`/`Game.TryEval`), em vez de
    ///       uma tabela de 9 nomes com a fórmula reescrita à mão;
    ///   (d) cobre a família inteira (12): Dwarven, Decay e Flame ficavam fora da tabela antiga e as
    ///       tooltips deles exibiam as auras de OUTRO shrine;
    ///   (e) não lê mais `Character.ActionStatuses` (lista viva, que muda durante o turno — era a
    ///       origem do "só em alguns momentos"): o efeito é derivado da DEFINIÇÃO do shrine, com o
    ///       bônus do personagem em foco. Para os dois status cujo efeito não mora no
    ///       `AttributeEffects` (Flame e Decay — o dano vive na ação `* Aura Proc`, RV-19 §4) a linha
    ///       mostra a descrição do próprio status com o `[0]` avaliado pela expressão dele.
    ///
    /// O Source da avaliação é o `Root.WorldCharacter` (o personagem VAZIO do shrine): é o que o jogo
    /// usa como origem da aura e é a razão de Decay/Flame NÃO escalarem com Omnism/Horn, enquanto as
    /// auras de buff (X = Target) escalam com o bônus do personagem em foco.
    /// </summary>
    [HarmonyPatch]
    public static class ShrineAuraPatch
    {
        /// <summary>Chaves de texto (exatas) da família de auras de shrine no LocalizePatch.
        /// Serve de PRÉ-FILTRO barato (o postfix roda em todo texto localizado do jogo); quem decide
        /// se a linha aparece é o `AcumuladoShrines`, casando a chave com a descrição do status.</summary>
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
                Plugin.Log.LogInfo($"[Shrine RV-23] {linha}");
            }
            catch
            {
                // log nunca pode derrubar nada
            }
        }

        /// <summary>Formata um atributo conhecido com a semântica CERTA do jogo (DamageReduction
        /// positivo = dano tomado REDUZIDO; ManaCostMod negativo = custo REDUZIDO).
        /// null = atributo que não está nesta lista; quem chamou usa o nome do próprio jogo.</summary>
        private static string Format(string attr, float v)
        {
            switch (attr)
            {
                case "DamageReduction":
                    return v >= 0 ? "Damage taken −" + v.ToString("0.#") + "%" : "Damage taken +" + (-v).ToString("0.#") + "%";
                case "ManaCostMod":
                    return "Mana Costs reduced by " + (-v).ToString("0.#") + "%";
                case "DamageMod": return "Damage +" + v.ToString("0.#") + "%";
                case "CritChance": return "Crit Chance +" + v.ToString("0.#") + "%";
                case "DodgeChance": return "Dodge +" + v.ToString("0.#") + "%";
                case "LifeOnHit": return "Life Steal +" + v.ToString("0.#") + "%";
                case "HealthPerTurnPercent": return "Health per turn +" + v.ToString("0.#") + "%";
                case "ManaPerTurnPercent": return "Mana per turn +" + v.ToString("0.#") + "%";
                default: return null;
            }
        }

        /// <summary>Começo da linha de auras ativas. O `LocalizePatch` usa este marcador para achar o
        /// bloco azul no corpo do tooltip (RV-27) sem encostar em nenhum outro bloco colorido — nem nos
        /// que o PRÓPRIO jogo colore com essa cor (blocos de status do `ShowTooltip`).</summary>
        internal const string MarcadorLinhaDeAuras = "Your active shrine auras:";

        /// <summary>Linha de acumulado (ou "" se não há nada). Nunca lança.
        /// `chaveDaTooltip` = o texto localizado que está sendo montado: é ele que diz QUAL shrine
        /// está aberto (o hover do shrine mostra `GroundEffectInfo.ActionStatuses[0].Description`,
        /// decompilado l.214180).</summary>
        public static string AcumuladoShrines(string chaveDaTooltip)
        {
            try
            {
                if (Burst2Flame.Game.Instance?.GetAttribute("ShrineEffectBonus") == null)
                {
                    return "";
                }

                // (a) o receptor é o MESMO do prefix: o personagem em foco (o WorldCharacter é vazio).
                Character receptor = Receptor(null, default(GameFunctionParameters));
                if (receptor == null)
                {
                    Marca("acumulado: nenhum receptor disponivel");
                    return "";
                }

                // (b)+(d) a aura é a DESTA tooltip — não a soma das auras de outros shrines.
                ActionStatusInfo aura = AcharAuraDaTooltip(chaveDaTooltip);
                if (aura == null)
                {
                    Marca($"acumulado: nenhuma aura de shrine com a descricao '{chaveDaTooltip}'");
                    return "";
                }

                // (c)+(e) valores do próprio status (AttributeEffects + expressões do jogo).
                string efeito = DescreverEfeito(aura, receptor);
                if (string.IsNullOrEmpty(efeito))
                {
                    Marca($"acumulado: aura '{aura.Name}' sem efeito calculavel para {receptor.CharacterName}");
                    return "";
                }

                Marca($"acumulado: shrine='{aura.Name}' char={receptor.CharacterName} -> {efeito}");
                // O texto do status pode ja terminar em ponto (Flame/Decay): nao somar outro.
                string fecho = (efeito.EndsWith(".", StringComparison.Ordinal)
                    || efeito.EndsWith("!", StringComparison.Ordinal)
                    || efeito.EndsWith("?", StringComparison.Ordinal)) ? "" : ".";
                return "\n<color=#" + LocalizePatch.CorDaLinhaDeAuras() + ">"
                    + MarcadorLinhaDeAuras + " " + efeito + fecho + "</color>";
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[Shrine RV-23] acumulado falhou: {ex.GetType().Name}: {ex.Message}");
                return "";
            }
        }

        /// <summary>
        /// O status de aura que a tooltip está mostrando. `Game.Instance.ActionStatuses` é a lista das
        /// DEFINIÇÕES de status do jogo (não os status vivos de um personagem), então casar pela
        /// descrição não depende do momento do turno. Se mais de um status compartilhar o mesmo texto,
        /// ganha o que tem `AttributeEffects` — é o que carrega o efeito de verdade.
        /// </summary>
        private static ActionStatusInfo AcharAuraDaTooltip(string chaveDaTooltip)
        {
            if (string.IsNullOrEmpty(chaveDaTooltip))
            {
                return null;
            }
            List<ActionStatusInfo> statuses = Burst2Flame.Game.Instance?.ActionStatuses;
            if (statuses == null)
            {
                return null;
            }
            ActionStatusInfo semEfeito = null;
            foreach (ActionStatusInfo s in statuses)
            {
                if (s == null || s.Description == null)
                {
                    continue;
                }
                if (!string.Equals(s.Description, chaveDaTooltip, StringComparison.Ordinal))
                {
                    continue;
                }
                if (s.AttributeEffects != null && s.AttributeEffects.Length > 0)
                {
                    return s;
                }
                if (semEfeito == null)
                {
                    semEfeito = s;
                }
            }
            return semEfeito;
        }

        /// <summary>
        /// O que a aura FAZ, lido do status (nunca de tabela): um item por `AttributeEffects`, com o
        /// valor vindo da expressão do próprio efeito avaliada pelo interpretador do jogo. Auras sem
        /// AttributeEffects (Flame/Decay — o dano mora na ação `* Aura Proc`, RV-19 §4) caem na
        /// descrição do status com o `[0]` avaliado pela expressão dele.
        /// </summary>
        private static string DescreverEfeito(ActionStatusInfo aura, Character receptor)
        {
            List<string> partes = new List<string>();
            CharacterEffectInfo[] efeitos = aura.AttributeEffects;
            if (efeitos != null)
            {
                foreach (CharacterEffectInfo efeito in efeitos)
                {
                    if (efeito == null || efeito.CharacterAttribute == null)
                    {
                        continue;
                    }
                    float valor;
                    if (!ValorDaExpressao(efeito.Amount, receptor, out valor))
                    {
                        Marca($"acumulado: expressao nao avaliada no efeito de '{aura.Name}': {efeito.Amount}");
                        continue;
                    }
                    partes.Add(TextDoEfeito(efeito.CharacterAttribute, valor));
                }
            }
            if (partes.Count == 0)
            {
                string texto = TextoDaDescricao(aura, receptor);
                if (!string.IsNullOrEmpty(texto))
                {
                    partes.Add(texto);
                }
            }
            return partes.Count == 0 ? "" : string.Join("; ", partes.ToArray());
        }

        /// <summary>
        /// Descrição do próprio status com os `[n]` trocados pelo valor real da expressão `n` (mesma
        /// convenção do `ApplyDescriptionExpressions` do jogo).
        /// </summary>
        private static string TextoDaDescricao(ActionStatusInfo aura, Character receptor)
        {
            string texto = aura.Description;
            if (string.IsNullOrEmpty(texto))
            {
                return null;
            }
            string[] expressoes = aura.DescriptionExpressions;
            if (expressoes == null || expressoes.Length == 0)
            {
                expressoes = aura.GetDescriptionExpressionsNonCharacterBased();
            }
            if (expressoes != null)
            {
                for (int i = 0; i < expressoes.Length && i < 10; i++)
                {
                    string token = "[" + i + "]";
                    if (texto.IndexOf(token, StringComparison.Ordinal) < 0)
                    {
                        continue;
                    }
                    float valor;
                    if (!ValorDaExpressao(expressoes[i], receptor, out valor))
                    {
                        continue;
                    }
                    texto = texto.Replace(token, valor.ToString("0.#"));
                }
            }
            return texto.Trim();
        }

        /// <summary>
        /// Avalia a expressão do jogo como o motor faz ao aplicar o efeito: primeiro número puro
        /// (`TryParseWithEnglishCulture`), senão `Game.TryEval` (mesma ordem de
        /// `Character.GetAttributeWalk`).
        /// `Source` = personagem do SHRINE (o `Root.WorldCharacter`, vazio e sem bônus — é isso que
        /// mantém Decay/Flame na base); `Target` = o personagem em foco (é o que faz as auras de buff
        /// escalarem com Omnism/Horn).
        /// </summary>
        private static bool ValorDaExpressao(string expressao, Character receptor, out float valor)
        {
            valor = 0f;
            if (string.IsNullOrEmpty(expressao))
            {
                return false;
            }
            GameFunctionParameters parametros = new GameFunctionParameters
            {
                Source = NetworkingManager.Instance?.NetworkManager?.Root?.WorldCharacter,
                Target = receptor
            };
            // Expressão que lê `Source[...]` precisa do personagem do shrine: sem ele, melhor não
            // mostrar número nenhum do que mostrar um número mentiroso.
            if (parametros.Source == null && expressao.IndexOf("Source[", StringComparison.Ordinal) >= 0)
            {
                return false;
            }
            if (Burst2Flame.Game.TryParseWithEnglishCulture(expressao, out valor))
            {
                return true;
            }
            return Burst2Flame.Game.TryEval<float>(expressao, parametros, out valor);
        }

        /// <summary>
        /// Rótulo do efeito. Os atributos conhecidos têm frase própria (o sinal do atributo não é o
        /// sinal do texto: `DamageReduction` positivo REDUZ o dano tomado e `ManaCostMod` negativo
        /// reduz o custo). Qualquer outro usa o nome de tooltip do PRÓPRIO jogo
        /// (`CharacterAttribute.GetTooltipDisplayName`) — nada inventado aqui.
        /// </summary>
        private static string TextDoEfeito(CharacterAttribute atributo, float v)
        {
            string nome = atributo.name;
            string conhecido = Format(nome, v);
            if (conhecido != null)
            {
                return conhecido;
            }
            string rotulo = atributo.GetTooltipDisplayName();
            if (string.IsNullOrEmpty(rotulo))
            {
                rotulo = nome;
            }
            return rotulo + " " + (v >= 0f ? "+" : "−") + Mathf.Abs(v).ToString("0.#") + "%";
        }
    }
}
