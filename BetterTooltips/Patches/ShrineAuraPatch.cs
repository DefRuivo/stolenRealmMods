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
    ///
    /// RV-29 (30/09) — a LINHA SÓ APARECE PARA QUEM TEM A AURA ATIVA. O defeito: a decisão (e) acima
    /// derivou a aura da DEFINIÇÃO do shrine aberto e nunca olhou o estado do personagem em foco, então
    /// a linha saía em TODO hover de shrine — inclusive para quem estava FORA da área (o usuário viu
    /// "personagens que não têm os buffs aparecendo como se tivessem"). A correção usa a lista VIVA de
    /// status (`Character.ActionStatuses`) APENAS COMO FILTRO. (O método daquele fix, `AcharStatusVivo`,
    /// ficava preso à chave da tooltip e foi substituído no RV-31 por `AurasVivas` — o filtro agora é
    /// "tem ALGUMA aura de shrine viva", e o valor passou a sair do indexador do personagem.)
    /// Prova de que o filtro é o vínculo correto: o status aplicado pela aura É o mesmo objeto
    /// que o tooltip do shrine descreve (`GroundEffectInfo.ActionStatuses[0]`, decompilado l.214180) e o
    /// motor o cria no personagem ao entrar na área — `GroundEffect.AddGroundEffectedPlayer` ->
    /// `CreateActionStatus(Source, player, statusInfo, ...)` (decompilado l.116911-116924), chamado de
    /// dentro de `GameLogic.ProcessGroundEffects` quando o personagem entra/termina o movimento
    /// (decompilado l.112652 e l.34445).
    ///
    /// RV-30 (30/09) — "valor DOBRADO": NÃO havia dobra na aritmética deste arquivo, e o número do
    /// jogador não foi mudado. O que a investigação provou (logs do jogo do usuário + assets):
    ///   (1) o valor sai de UMA avaliação da expressão do próprio status — `ValorDaExpressao`
    ///       (l.444-467) chama `TryParseWithEnglishCulture` e, se falhar, `Game.TryEval<float>` UMA vez;
    ///       o motor usa exatamente a mesma ordem na caminhada de atributos (decompilado l.37256-37263),
    ///       e o ÚNICO multiplicador extra do motor é `parsed2 *= TotalStacks` (l.37263), que não é
    ///       reescrito aqui;
    ///   (2) a diferença entre personagens é do PERSONAGEM, não do código: no log do usuário a MESMA
    ///       chave/base 20 saiu 20 para Ashley e 40 para Raven (`Crit Chance +20%` / `Crit Chance +40%`),
    ///       o que só se explica por `Target["ShrineEffectBonus"]` = 0 e 100 no receptor;
    ///   (3) o +100 tem nome nos assets do jogo: o perk `Worship` — "100% increased effect from Shrines"
    ///       com valor 100 (`resources.assets` @1519682848-1519682905), ao lado do CharacterInfo
    ///       `T2_Worshiper`/@1519682296, no mesmo arquivo que define o atributo `ShrineEffectBonus`
    ///       (@1519625600). É o termo que o usuário citou — e o único +100% de shrine além do roll de
    ///       100 do Horn of Devotion.
    ///   Logo: a aura de um Worshiper vale ×2 DE VERDADE (base 20 -> 40); o que fazia isso parecer
    ///   invenção era (a) a linha sair também para quem não tinha a aura (RV-29, corrigido acima) e
    ///   (b) a nota do mod citar só Omnism I/II e Horn como fontes do bônus (LocalizePatch, corrigido).
    ///   O log do acumulado passa a imprimir `bonus=` do receptor, para o usuário conferir a origem.
    ///
    /// RV-31 (30/09) — a linha VOLTA A SOMAR TODAS AS AURAS VIVAS (defeito relatado pelo usuário: a
    /// linha "Your active shrine auras" mostrava só a aura do shrine cuja tooltip estava aberta).
    /// Efeito colateral do RV-29: a correção filtrou pelo status VIVO (certo) mas amarrou a leitura na
    /// CHAVE DA TOOLTIP (errado) — `AcharStatusVivo(receptor, chaveDaTooltip)` devolvia só o status
    /// cuja descrição é o texto do shrine aberto, e a linha ficava no singular de fato.
    ///
    /// Os dois comportamentos agora coexistem:
    ///   (1) FILTRO (RV-29 preservado): `AurasVivas(receptor)` pergunta à lista VIVA de status quais
    ///       auras de shrine o personagem em foco está recebendo AGORA; nenhuma -> a linha não sai;
    ///   (2) CONTEÚDO AGREGADO (RV-20, o nome sempre foi no plural): um item por ATRIBUTO que as
    ///       auras vivas mexem — a UNIÃO delas, não só a da tooltip.
    ///
    /// COMO O VALOR É LIDO (a regra que evita inventar soma): a autoridade é o PRÓPRIO motor. Para
    /// cada atributo, lê-se o valor FINAL do personagem pelo indexador `Character[atributo]`
    /// (`Character.this[string]`, decompilado l.32662-32675 -> `GetAttribute(CharacterAttribute)`,
    /// l.40520) — ele JÁ é o resultado de todas as contribuições somadas pelo jogo (base + efeitos de
    /// gear/skills/shrine). Não somamos nada aqui, não aplicamos `(1 + bonus/100)` por fora e não
    /// assumimos aditividade: se o motor combina as contribuições de outro jeito, o número lido já
    /// reflete. É o MESMO valor que a ficha mostra (o BetterStats imprime `character[finalAttrs[i].name]`,
    /// `BetterStats/Plugin.cs` l.77) — é com ela que o usuário confere. O `^` desta linha é a única
    /// entrada que multiplica cada aura (`ShrineEffectBonus`), e ela já está dentro do número lido.
    ///
    /// O que NÃO entra: Flame e Decay (o efeito deles é dano numa AÇÃO `* Aura Proc`, RV-19 §4 — não
    /// existe atributo de personagem para ler) e o stun do Dwarven. Sem atributo, não há item: inventar
    /// um número para eles seria justamente o que o RV-30 mostrou que não se pode fazer.
    ///
    /// RV-33 (30/09) — o DANO REAL das duas auras de perigo na tooltip, como NÚMERO CRU.
    ///
    /// DECAY (calculável e direto). A ação `Decay Aura Proc` grava
    ///   TargetStored["ShadowDamage"] = Mathf.Round((Target["MaxHealth"] *
    ///   Target.GetValueByEnemyType(.05f, .1f, .12f, .15f, .2f, .1f)) * (1 + (Source["ShrineEffectBonus"] / 100)))
    /// — a string do asset (`resources.assets` @1519519282, UTF-16, len 171; idêntica no cache compilado
    /// l.87116/87118). Não tem `Mathf.Max(1,` (por isso o Decay pode dar
    /// 0). A ORDEM dos parâmetros de `GetValueByEnemyType` é a assinatura real do jogo (decompilado
    /// l.38351): `(boss, champion, elite, soldier, fodder, player)`, e um personagem NÃO-AI devolve o 6º
    /// (`player`) — logo o jogador leva `10%` da PRÓPRIA vida máxima, que é o exemplo do dono do jogo
    /// (100 de vida -> 10 por turno). O algoritmo que fecha o caso: o gatilho do status tem
    /// TriggerType = 4 (`OnTurnStart`, l.110131/110136 chamam `ProcessSkillTriggers(null, ...)`) e
    /// `Targets = Cell.IsCurrentHex(Source)` (asset, logo depois do status `Decay Shrine Aura`), avaliado
    /// com `Source = this` (o PORTADOR do status, decompilado l.41034-41040) — o proc acerta o próprio
    /// portador no começo do turno DELE. Dano por turno DELE na aura, não do round inteiro.
    ///
    /// FLAME (a premissa do pedido NÃO bate com a fórmula, e isso está PROVADO):
    ///   - a fórmula (asset @1519546098, UTF-16, len 187; decompilado l.87156/87158) é idêntica à do
    ///     Decay trocando a lista de % por (.025f, .08f, .1f, .12f, .14f, .05f) e com `Mathf.Max(1,`;
    ///   - o `Target` dela é QUEM LEVA o dano, e quem leva é o ATACANTE: o gatilho do status tem
    ///     TriggerType = 1 (`OnGettingHitDamaging` — o inteiro no asset, TriggerType é o 1º campo de
    ///     `SkillTrigger`, l.45778; o enum em l.45741 dá 1 = OnGettingHitDamaging), a chamada é
    ///     `target.ProcessSkillTriggers(source, ..., OnGettingHitDamaging, ...)` (decompilado l.40075),
    ///     ou seja `this` = quem FOI acertado e o `target` do gatilho = o ATACANTE; a Condition do asset
    ///     é `Source.IsEnemy(Target)` e o `Targets` é `Cell.IsCurrentHex(Target)` (avaliados com
    ///     `Source = this; Target = atacante`, l.41034-41040) -> a ação roda na célula do ATACANTE.
    ///     Controle cruzado: o status `Dwarven Totem Aura Status` tem a MESMA Condition/Targets e
    ///     TriggerType = 0 (`OnHittingDamaging`, l.40048, `this` = o atacante) -> o efeito cai no
    ///     DEFENSOR, que é exatamente o que o texto do Dwarven diz ("stun the target").
    ///   - conclusão: o dano do Flame é % da vida máxima DE QUEM LEVA O DANO (o atacante que bateu em
    ///     alguém dentro da aura), NÃO da vida do personagem que está na aura. Como o atacante é
    ///     DESCONHECIDO no hover, um número único por atacante é impossível — limitação do jogo, não do
    ///     mod. O que sai é a escala na nota + UM ITEM POR PERSONAGEM que está na área da aura (a lista
    ///     de `FraseAlvosDoFlame`), cada um com a conta feita sobre a vida máxima E o tipo DELE.
    ///   - NÃO PROVADO (e por isso NÃO escrito no texto): de quem é o `ShrineEffectBonus` lido no
    ///     fator `(1 + Source[...]/100)`. O executor é `UseTriggerSource && TriggerSource != null ?
    ///     TriggerSource : this` (l.41051) e `TriggerSource = actionStatus.Source` (l.33501) — mas o
    ///     valor de `UseTriggerSource` no asset não foi possível ler com segurança byte a byte. O caso
    ///     do dono do jogo (sem o perk Worship) vale 1 nos dois caminhos; a medição em jogo que fecha
    ///     está no relatório do RV-33.
    ///
    /// AS DUAS CONSTANTES DE FÓRMULA OMITEM DE PROPÓSITO o fator `(1 + Source["ShrineEffectBonus"]/100)`
    /// que existe no asset nas duas ações: ele vale 1 com o shrine como origem da aura (o bônus não
    /// provado acima) e o dono do jogo pediu vida máxima × porcentagem. O resto é a fórmula do jogo,
    /// com o `Mathf.Max(1,` do Flame (o Decay não tem mínimo).
    ///
    /// O QUE ENTROU NA TOOLTIP (especificação do dono do jogo, 30/09): o Flame mostra UM ITEM POR ALVO
    /// que está na área da aura — quem TEM o status do Flame vivo, party e inimigos (`AlvosNaAreaDoFlame`)
    /// — com `Target` = esse alvo: vida máxima DELE × a % do tipo DELE, o CRU (sem mitigação nenhuma),
    /// porque o hover não sabe quem vai atacar. O Decay mostra o dano por turno do personagem em foco na
    /// própria linha do jogo. O fator `ShrineEffectBonus` fica FORA dos dois números (ver acima): é vida
    /// máxima × porcentagem, como o dono do jogo pediu.
    ///
    /// Nada aqui aplica mitigação: o número é o CRU da fórmula (vida máxima × %), sem armadura,
    /// resistência ou qualquer modificador posterior. Sem número provado, a linha do jogo fica INTACTA.
    ///
    /// ASSINATURA: nada muda no Harmony aqui — este arquivo segue com a assinatura explícita por TIPO
    /// no único patch (`ApplyDescriptionExpressions`, 5 tipos, `ref __2`) e nenhum parâmetro por índice
    /// novo. Todo o trabalho novo é código de leitura, dentro de try/catch.
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

        /// <summary>
        /// RV-26 — RECEPTOR da tooltip, exposto para os outros patches (RV-28 usa o mesmo: o número
        /// tem de ser do personagem em foco, nunca do WorldCharacter vazio do shrine).
        /// </summary>
        internal static Character ReceptorDaTooltip()
        {
            return Receptor(null, default(GameFunctionParameters));
        }

        /// <summary>
        /// RV-26 (30/09), reescrito no RV-33 — o NÚMERO do Flame Shrine por ALVO NA ÁREA DA AURA.
        ///
        /// DE QUEM É A VIDA MÁXIMA (o ponto que a RV-26 deixou indecidido e agora está fechado): o `Target`
        /// da fórmula é QUEM LEVA O DANO, e quem leva é o ATACANTE que disparou a aura — TriggerType =
        /// `OnGettingHitDamaging` no asset + Condition `Source.IsEnemy(Target)` + `Targets =
        /// Cell.IsCurrentHex(Target)`, avaliados com `Source = this` (quem foi acertado) e `Target` = o
        /// atacante. Prova completa no cabeçalho desta classe. NÃO é a vida máxima do personagem que
        /// apenas está parado na aura.
        ///
        /// O QUE A TOOLTIP MOSTRA (especificação do dono do jogo, 30/09): a aura aplica o status a quem
        /// está na área, então dá para ENUMERAR os alvos — varre-se quem TEM o status do Flame vivo
        /// (party e inimigos) e, por alvo, sai o dano com `Target` = ESSE alvo, com o nome ao lado. Quem
        /// ataca é desconhecido no hover: um número único por atacante é impossível; o número por ALVO
        /// na área é exatamente o que a fórmula do jogo dá (limitação do jogo, não do mod).
        ///
        /// CRU, como pedido: `Mathf.Max(1, Mathf.Round(MaxHealth * GetValueByEnemyType(...)))` — o
        /// `Mathf.Max(1,` é do jogo; não entra redução de dano, resistência nem modificador posterior. O
        /// fator `(1 + Source["ShrineEffectBonus"] / 100)` da fórmula do asset é OMITIDO de propósito
        /// (vale 1 com o shrine como origem da aura; a origem do bônus não está provada byte a byte —
        /// ver cabeçalho — e o dono do jogo pediu vida máxima × porcentagem).
        ///
        /// Devolve "" quando nenhum alvo tem o status vivo, ou em qualquer falha: nenhum número é
        /// inventado e o texto do jogo (com a escala na nota) fica como está.
        /// </summary>
        public static string FraseAlvosDoFlame(string chaveDaTooltip)
        {
            try
            {
                if (!string.Equals(chaveDaTooltip, ChaveFlame, StringComparison.Ordinal))
                {
                    return "";
                }
                List<Character> alvos = AlvosNaAreaDoFlame();
                if (alvos.Count == 0)
                {
                    // Item 4 da especificação: sem alvo na área, NENHUM número — a escala já está na nota.
                    Marca("RV-33 Flame sem alvo: ninguem com o status da aura vivo agora (nenhum numero)");
                    return "";
                }
                List<string> partes = new List<string>();
                foreach (Character alvo in alvos)
                {
                    if (alvo == null || alvo.MaxHealth <= 0f)
                    {
                        continue;
                    }
                    float dano;
                    if (!ValorDaExpressao(FormulaDanoFlameCru, alvo, out dano))
                    {
                        Marca($"RV-33 Flame alvo '{alvo.CharacterName}' sem numero: formula nao avaliada");
                        continue;
                    }
                    string nome = string.IsNullOrEmpty(alvo.CharacterName) ? "(sem nome)" : alvo.CharacterName;
                    partes.Add(nome + " " + dano.ToString("0.#"));
                    // Item 6 da especificação: o log diz DE QUAL ALVO saiu cada número, com a vida máxima
                    // e o tipo que entraram na conta, para a conferência em jogo.
                    Marca($"RV-33 Flame alvo '{nome}': MaxHealth={alvo.MaxHealth.ToString("0.#")}"
                        + $" tipo={TipoDoAlvo(alvo)} dano={dano.ToString("0.#")}");
                }
                if (partes.Count == 0)
                {
                    return "";
                }
                return "In the aura now (raw damage it takes as the attacker, from its own Max Health): "
                    + string.Join("; ", partes.ToArray()) + ".";
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[Shrine RV-33] alvos do Flame falharam (texto intacto): {ex.GetType().Name}: {ex.Message}");
                return "";
            }
        }

        /// <summary>
        /// RV-33 — os personagens que TÊM o status da aura do Flame vivo agora, ou seja, quem está dentro
        /// da área (party E inimigos). A varredura é a mesma família de leitura do RV-31
        /// (`Character.ActionStatuses`, a lista VIVA, casada pela descrição do status contra a chave do
        /// Flame) aplicada a `Root.AllCharacters` — a raiz pública que o jogo usa em `CharactersInBattle`
        /// (decompilado l.140373/140375). Falha de leitura devolve lista vazia: sem prova, sem número.
        /// </summary>
        private static List<Character> AlvosNaAreaDoFlame()
        {
            List<Character> achados = new List<Character>();
            try
            {
                Burst2Flame.Observable.ObservableList<Character> todos =
                    NetworkingManager.Instance?.NetworkManager?.Root?.AllCharacters;
                if (todos == null || todos.Count == 0)
                {
                    return achados;
                }
                foreach (Character c in todos)
                {
                    if (c == null || c.ActionStatuses == null)
                    {
                        continue;
                    }
                    foreach (ActionStatus s in c.ActionStatuses)
                    {
                        if (s == null || s.ActionStatusInfo == null)
                        {
                            continue;
                        }
                        // Duas formas de reconhecer o status da aura, as duas provadas no asset:
                        // a DESCRIÇÃO exibida (a mesma que a tooltip do ground effect mostra,
                        // `GroundEffectInfo.ActionStatuses[0].Description`, decompilado l.214180) e o NOME
                        // do asset (`Flame Shrine Aura`). Aceitar as duas cobre o caso de o status aplicado
                        // na área não carregar a mesma descrição — sem nenhuma delas, não há número.
                        if (string.Equals(s.ActionStatusInfo.Description, ChaveFlame, StringComparison.Ordinal)
                            || string.Equals(s.ActionStatusInfo.name, NomeStatusFlame, StringComparison.Ordinal))
                        {
                            achados.Add(c);
                            break;
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[Shrine RV-33] varredura de alvos falhou ({ex.GetType().Name}): {ex.Message}");
                achados.Clear();
            }
            return achados;
        }

        /// <summary>O tipo de inimigo do alvo — só para o log (é dele que sai a % na fórmula).</summary>
        private static string TipoDoAlvo(Character c)
        {
            try
            {
                return c.IsAI ? c.EnemyType.ToString() : "player";
            }
            catch (Exception ex)
            {
                return "(" + ex.GetType().Name + ")";
            }
        }

        /// <summary>A chave de texto exata do Flame Shrine (a descrição da aura).</summary>
        internal const string ChaveFlame = "Attackers take Fire Damage.";

        /// <summary>O nome do asset do status da aura do Flame (`resources.assets`, status com a descrição
        /// acima) — usado como segunda forma de reconhecer o status aplicado a quem está na área.</summary>
        internal const string NomeStatusFlame = "Flame Shrine Aura";

        /// <summary>
        /// A fórmula do dano do Flame por alvo, CRUA como o dono do jogo pediu: vida máxima × a % do tipo
        /// do próprio alvo, com o `Mathf.Max(1,` do jogo. É a fórmula do asset da ação `Flame Aura Proc`
        /// (`resources.assets` @1519546098, UTF-16, len 187: `TargetStored["FireDamage"] = Mathf.Max(1,  Mathf.Round(...))`,
        /// idêntica no cache compilado l.87156/87158) SEM o fator `(1 + (Source["ShrineEffectBonus"] / 100))`
        /// — o único trecho omitido de propósito (vale 1 com o shrine como origem da aura; a origem do
        /// bônus não está provada byte a byte, ver cabeçalho). Avaliada pelo INTERPRETADOR DO PRÓPRIO JOGO
        /// (`Game.TryEval`), com `Target` = o alvo da vez: nenhum número dela é escrito à mão aqui.
        /// </summary>
        private const string FormulaDanoFlameCru =
            "Mathf.Max(1, Mathf.Round(Target[\"MaxHealth\"] * Target.GetValueByEnemyType(.025f, .08f, .1f, .12f, .14f, .05f)))";

        /// <summary>A chave de texto exata do Decay Shrine (a descrição da aura).</summary>
        internal const string ChaveDecay = "Take [0]% of your Max Health in Shadow Damage per turn.";

        /// <summary>
        /// RV-33 — a fórmula do dano do Decay, CRUA: vida máxima do próprio alvo × a % do tipo dele, SEM
        /// o `Mathf.Max(1,` (o Decay pode dar 0). É a fórmula do asset da ação `Decay Aura Proc`
        /// (`resources.assets` @1519519282, UTF-16, len 171 — o texto é
        /// `TargetStored["ShadowDamage"] = ` + isto; idêntica no cache compilado l.87116/87118), SEM o
        /// fator `(1 + (Source["ShrineEffectBonus"] / 100))` — o único trecho omitido de propósito (vale
        /// 1 com o shrine como origem da aura; a origem do bônus não está provada byte a byte).
        /// A lista de % é (.05f, .1f, .12f, .15f, .2f, .1f — 5% boss, 10% champion, 12% elite,
        /// 15% soldier, 20% fodder, 10% player).
        /// </summary>
        private const string FormulaDanoDecay =
            "Mathf.Round(Target[\"MaxHealth\"] * Target.GetValueByEnemyType(.05f, .1f, .12f, .15f, .2f, .1f))";

        /// <summary>
        /// RV-33 — o DANO POR TURNO do Decay Shrine como NÚMERO na linha do jogo.
        ///
        /// Entrega a linha ORIGINAL (`Take [0]% ... per turn.`) com o dano literal acrescentado no fim —
        /// o `[0]` é PRESERVADO de propósito: quem troca o `[0]` pela % do status é o motor
        /// (`ApplyDescriptionExpressions`). A expressão do status no asset (status `Decay Shrine Aura`) é
        /// `Mathf.Round(10 * (1 + (Source["ShrineEffectBonus"] / 100)))`, que com o shrine como origem da
        /// aura dá 10 — a MESMA base de tipo que o dano usa, então o número e a % exibidos não se
        /// contradizem no caso real (o valor do fator é o ponto não provado, ver cabeçalho).
        ///
        /// O `Target` da avaliação é o personagem em foco (o `ReceptorDaTooltip`, resolvido como a
        /// TooltipCharacter): é ele quem está na aura, e é quem o proc do Decay acerta no começo do
        /// turno dele (TriggerType `OnTurnStart` + `Targets = Cell.IsCurrentHex(Source)` com
        /// `Source = this` = o portador — prova no cabeçalho desta classe). Um personagem de 100 de vida
        /// mostra "10 damage per turn for you".
        ///
        /// Sem receptor, sem vida ou com a expressão não avaliada devolve null: a linha do jogo fica
        /// INTACTA e o log diz o motivo.
        /// </summary>
        public static string LinhaDecayComValor(string chaveDaTooltip)
        {
            try
            {
                if (!string.Equals(chaveDaTooltip, ChaveDecay, StringComparison.Ordinal))
                {
                    return null;
                }
                Character naAura = ReceptorDaTooltip();
                if (naAura == null)
                {
                    Marca("RV-33 Decay sem numero: nenhum receptor (personagem em foco) disponivel");
                    return null;
                }
                if (naAura.MaxHealth <= 0f)
                {
                    Marca("RV-33 Decay sem numero: receptor sem MaxHealth");
                    return null;
                }
                float dano;
                if (!ValorDaExpressao(FormulaDanoDecay, naAura, out dano))
                {
                    // Reserva: a MESMA conta, com a % lida pelo interpretador (o Decay NÃO tem
                    // Mathf.Max(1, então o 0 é um resultado legítimo).
                    float pct;
                    if (!ValorDaExpressao(PorcentagemDoDecay, naAura, out pct))
                    {
                        Marca("RV-33 Decay sem numero: formula e % nao avaliadas pelo interpretador");
                        return null;
                    }
                    dano = Mathf.Round(naAura.MaxHealth * pct);
                    Marca("RV-33 Decay reserva: formula completa nao avaliada; dano montado a partir da % do alvo");
                }
                // A linha do jogo termina em ponto: o número entra antes dele, e o `[0]` fica no lugar.
                string linha = ChaveDecay.Substring(0, ChaveDecay.Length - 1)
                    + " (" + dano.ToString("0.#") + " damage per turn for you).";
                Marca($"RV-33 linha do Decay: {naAura.CharacterName} MaxHealth={naAura.MaxHealth.ToString("0.#")}"
                    + $" -> '{linha}'");
                return linha;
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[Shrine RV-33] valor do Decay falhou (linha intacta): {ex.GetType().Name}: {ex.Message}");
                return null;
            }
        }

        /// <summary>A % do próprio portador da aura no Decay, lida do asset (mesma lista da fórmula
        /// acima): 10% para o jogador.</summary>
        private const string PorcentagemDoDecay =
            "Target.GetValueByEnemyType(.05f, .1f, .12f, .15f, .2f, .1f)";

        /// <summary>Loga cada combinação UMA vez (o postfix roda a cada frame de hover).</summary>
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

        /// <summary>Ordem da linha: os atributos que a família de auras de shrine mexe, na ordem em que
        /// o censo os lista (Warrior/DamageMod, Guardian/DamageReduction, Conqueror/CritChance,
        /// Rogue/DodgeChance, Reaper/LifeOnHit, Seraph/HealthPerTurnPercent, Shaman/ManaPerTurnPercent,
        /// Energy/ManaCostMod — Fury entra nos dois primeiros). Um atributo fora desta lista NÃO é
        /// descartado: entra depois, na ordem em que apareceu, com o rótulo do próprio jogo.</summary>
        private static readonly string[] OrdemDosAtributos =
        {
            "DamageMod", "DamageReduction", "CritChance", "DodgeChance",
            "LifeOnHit", "HealthPerTurnPercent", "ManaPerTurnPercent", "ManaCostMod"
        };

        /// <summary>
        /// Linha de acumulado (ou "" se não há nada). Nunca lança.
        ///
        /// RV-31 — a linha é o AGREGADO das auras de shrine VIVAS no personagem em foco (um item por
        /// ATRIBUTO da família), e não mais a aura do shrine cuja tooltip está aberta. O filtro do
        /// RV-29 continua: sem NENHUMA aura de shrine viva, não há linha.
        ///
        /// `chaveDaTooltip` = o texto localizado que está sendo montado. Ele NÃO decide mais o conteúdo
        /// (era isso que fazia a linha mostrar só a aura do shrine aberto); entra apenas no log.
        /// </summary>
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

                // (b) FILTRO (RV-29 preservado, agora sem o recorte pela tooltip): quais auras de
                // shrine este personagem está recebendo AGORA? Nenhuma -> nada de linha.
                List<ActionStatus> ativas = AurasVivas(receptor);
                if (ativas.Count == 0)
                {
                    Marca($"RV-31 sem linha: {receptor.CharacterName} nao tem aura de shrine viva agora"
                        + $" (tooltip '{chaveDaTooltip}')");
                    return "";
                }

                // (c) CONTEÚDO AGREGADO: um item por ATRIBUTO que as auras vivas mexem (a intenção do
                // RV-20, cujo nome sempre foi no plural). Flame/Decay (o efeito é dano numa ação) e o
                // stun do Dwarven não têm atributo de personagem — não entram, não há o que ler.
                List<CharacterAttribute> atributos = AtributosDasAuras(ativas);
                if (atributos.Count == 0)
                {
                    Marca($"RV-31 sem linha: {ativas.Count} aura(s) viva(s) sem atributo de personagem"
                        + $" em {receptor.CharacterName}");
                    return "";
                }

                // (d) O VALOR é do MOTOR: `Character[atributo]` é o total FINAL do personagem (base +
                // todas as contribuições, as do shrine inclusive). Não somamos nada aqui e não
                // aplicamos (1 + bonus/100) por fora — o número lido já é o resultado do jogo, e é o
                // mesmo que a ficha (BetterStats) mostra. Se o jogo combina as contribuições de outro
                // jeito, o valor lido já reflete isso.
                List<string> partes = new List<string>();
                foreach (CharacterAttribute atributo in atributos)
                {
                    string nome = atributo.name;
                    // O INDEXADOR LANÇA para nome desconhecido (`Character.this[string]`,
                    // decompilado l.32662-32675): checar antes de ler.
                    if (string.IsNullOrEmpty(nome) || Burst2Flame.Game.Instance.GetAttribute(nome) == null)
                    {
                        Marca($"RV-31 item omitido: atributo '{nome}' ausente neste build");
                        continue;
                    }
                    float valor = receptor[nome];
                    partes.Add(TextDoEfeito(atributo, valor));
                }
                if (partes.Count == 0)
                {
                    return "";
                }

                string efeito = string.Join("; ", partes.ToArray());
                // RV-30: o `bonus=` entra no log de propósito — é a ÚNICA entrada que multiplica o
                // valor da aura, e sai do ATRIBUTO do próprio personagem (ex.: perk Worship = 100),
                // nunca de uma segunda aplicação do mod. Aqui ele é o bonus de quem tem as auras, e
                // serve para o usuário conferir a origem do número. Os nomes das auras agregadas vão
                // no log para a conferência em jogo dizer QUAIS auras entraram na conta.
                Marca($"RV-31 acumulado: auras=[{string.Join(", ", NomesDasAuras(ativas).ToArray())}]"
                    + $" char={receptor.CharacterName} bonus={BonusDoReceptor(receptor)} -> {efeito}");
                // Os itens terminam em "%": o fecho é sempre o ponto.
                return "\n<color=#" + LocalizePatch.CorDaLinhaDeAuras() + ">"
                    + MarcadorLinhaDeAuras + " " + efeito + ".</color>";
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[Shrine RV-23] acumulado falhou: {ex.GetType().Name}: {ex.Message}");
                return "";
            }
        }

        /// <summary>
        /// RV-31 — TODAS as auras de shrine VIVAS no personagem em foco. É o caminho do RV-29
        /// (`Character.ActionStatuses`, a lista viva, que muda durante o turno) SEM descartar as que
        /// não são a da tooltip: a pergunta que a lista responde é "quais auras de shrine este
        /// personagem está recebendo agora?".
        ///
        /// O casamento é pela DESCRIÇÃO contra `ShrineKeys` — a MESMA definição de família que o
        /// `LocalizePatch` usa de pré-filtro e o mesmo texto que o tooltip do shrine mostra
        /// (`GroundEffectInfo.ActionStatuses[0]`, decompilado l.214180). O valor de cada atributo NÃO
        /// sai daqui: sai do indexador do personagem (ver `AcumuladoShrines`).
        ///
        /// Falha de leitura devolve lista vazia: sem prova de que a aura está viva, a linha não sai.
        /// </summary>
        private static List<ActionStatus> AurasVivas(Character receptor)
        {
            List<ActionStatus> ativas = new List<ActionStatus>();
            if (receptor == null)
            {
                return ativas;
            }
            try
            {
                Burst2Flame.Observable.ObservableList<ActionStatus> vivos = receptor.ActionStatuses;
                if (vivos == null || vivos.Count == 0)
                {
                    return ativas;
                }
                foreach (ActionStatus s in vivos)
                {
                    if (s == null || s.ActionStatusInfo == null || s.ActionStatusInfo.Description == null)
                    {
                        continue;
                    }
                    if (ShrineKeys.Contains(s.ActionStatusInfo.Description))
                    {
                        ativas.Add(s);
                    }
                }
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[Shrine RV-31] leitura da lista viva falhou ({ex.GetType().Name}): {ex.Message}");
                ativas.Clear();
            }
            return ativas;
        }

        /// <summary>
        /// RV-31 — os atributos que as auras VIVAS mexem, SEM repetição (Fury aparece com dois: dano
        /// ganho e dano tomado; duas auras que mexem no mesmo atributo viram UM item) e na ordem
        /// canônica de `OrdemDosAtributos`. A lista sai do `AttributeEffects` do PRÓPRIO status — o
        /// nome de atributo de cada shrine não é cravado no código.
        /// </summary>
        private static List<CharacterAttribute> AtributosDasAuras(List<ActionStatus> auras)
        {
            List<CharacterAttribute> achados = new List<CharacterAttribute>();
            HashSet<string> vistos = new HashSet<string>();
            foreach (ActionStatus s in auras)
            {
                CharacterEffectInfo[] efeitos = s.ActionStatusInfo != null ? s.ActionStatusInfo.AttributeEffects : null;
                if (efeitos == null)
                {
                    continue;
                }
                foreach (CharacterEffectInfo efeito in efeitos)
                {
                    if (efeito == null || efeito.CharacterAttribute == null)
                    {
                        continue;
                    }
                    string nome = efeito.CharacterAttribute.name;
                    if (!string.IsNullOrEmpty(nome) && vistos.Add(nome))
                    {
                        achados.Add(efeito.CharacterAttribute);
                    }
                }
            }

            // Ordem canônica primeiro; o que não estiver na lista entra depois, na ordem de encontro.
            List<CharacterAttribute> ordenados = new List<CharacterAttribute>();
            HashSet<string> postos = new HashSet<string>();
            foreach (string canonico in OrdemDosAtributos)
            {
                foreach (CharacterAttribute a in achados)
                {
                    if (string.Equals(a.name, canonico, StringComparison.Ordinal) && postos.Add(canonico))
                    {
                        ordenados.Add(a);
                        break;
                    }
                }
            }
            foreach (CharacterAttribute a in achados)
            {
                if (postos.Add(a.name))
                {
                    ordenados.Add(a);
                }
            }
            return ordenados;
        }

        /// <summary>Nomes das auras vivas — só para o log (a conferência em jogo precisa ver QUAIS
        /// auras o agregado somou).</summary>
        private static List<string> NomesDasAuras(List<ActionStatus> auras)
        {
            List<string> nomes = new List<string>();
            foreach (ActionStatus s in auras)
            {
                string nome = (s != null && s.ActionStatusInfo != null) ? s.ActionStatusInfo.Name : null;
                nomes.Add(string.IsNullOrEmpty(nome) ? "(sem nome)" : nome);
            }
            return nomes;
        }

        /// <summary>RV-30 — o `ShrineEffectBonus` REAL do receptor, só para o log (a única entrada que
        /// multiplica o valor da aura). Nunca entra no texto; o número mostrado é o que a expressão do
        /// jogo devolve. Chamado só depois do guard `GetAttribute("ShrineEffectBonus") != null`.</summary>
        private static string BonusDoReceptor(Character receptor)
        {
            try
            {
                return receptor != null ? receptor["ShrineEffectBonus"].ToString("0.#") : "(sem receptor)";
            }
            catch (Exception ex)
            {
                return "(" + ex.GetType().Name + ")";
            }
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
