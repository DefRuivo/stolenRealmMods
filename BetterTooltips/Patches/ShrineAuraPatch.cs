using System;
using System.Collections.Generic;
using System.Reflection;
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
    /// O Source da avaliação ERA o `Root.WorldCharacter` (o personagem VAZIO do shrine) — premissa do
    /// RV-26/33 DERRUBADA em 30/09 pela medição em jogo do dono do jogo (RV-34): Decay e Flame TAMBÉM
    /// escalam com o bônus do personagem, e com o perk `Worship` o dano DOBRA. Hoje o fator das duas
    /// auras de perigo é avaliado com `Source` = `Target` = o PRÓPRIO personagem avaliado (ver RV-34
    /// adiante), e o `Source` vazio do shrine também é trocado pelo receptor no prefix (sem ele, o
    /// `[0]` da linha do Decay sairia na base enquanto o dano real dobra).
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
    /// COMO O VALOR É LIDO (a regra que evita inventar soma): o TOTAL é a autoridade do PRÓPRIO motor —
    /// para cada atributo, lê-se o valor FINAL do personagem pelo indexador `Character[atributo]`
    /// (`Character.this[string]`, decompilado l.32662-32675 -> `GetAttribute(CharacterAttribute)`,
    /// l.40520) — ele JÁ é o resultado de todas as contribuições somadas pelo jogo (base + efeitos de
    /// gear/skills/shrine). Não somamos nada aqui, não aplicamos `(1 + bonus/100)` por fora e não
    /// assumimos aditividade: se o motor combina as contribuições de outro jeito, o número lido já
    /// reflete. É o MESMO valor que a ficha mostra (o BetterStats imprime `character[finalAttrs[i].name]`,
    /// `BetterStats/Plugin.cs` l.77) — é com ela que o usuário confere.
    ///
    /// RV-44 (30/09) — O TOTAL SAIU DA FRENTE DO ITEM. Defeito relatado com print do dono: a linha se
    /// chama "Your active shrine auras" e mostrava aura + skill + equipamento num número só — no
    /// Goblin Battle Standard (Fury) o tooltip do shrine dizia 25% (50% com `Worship`) e a linha dizia
    /// 50% (75%), e no Rogue Shrine dizia `Dodge +57%` com a aura entregando 40% (20 × 2 do Worship).
    /// Na tela isso é indistinguível de "a aura dá 57%". Agora cada item é
    /// **`<o que as auras dão> (total <o total do personagem>%)`** — ex.: `Dodge +40% (total +57%)`,
    /// `Damage +25% (total +50%)` —, com a contribuição saindo do `AttributeEffects` REAL das auras
    /// VIVAS (a mesma expressão que o tooltip do shrine mostra, avaliada pelo motor: 20 × (1+bônus/100))
    /// e o total continuando a ser o indexador. Um item por atributo (RV-31) e a ordem canônica não
    /// mudam; **duas auras no mesmo atributo SOMAM as contribuições** (`Warrior + Fury` em `DamageMod`).
    /// Prova com as telas do dono (30/09) — as contas fecham de forma aditiva nas duas:
    ///   Fury sem Worship: aura 25 / total 50 (resto da ficha +25); Damage taken: aura 25 / total 5
    ///     (`DamageReduction` −25 / −5 -> resto +20).
    ///   Fury com Worship: aura 50 / total 75 (resto +25); Damage taken: aura 50 / total 30
    ///     (`DamageReduction` −50 / −30 -> resto +20).
    ///   Rogue Shrine com Worship: `Dodge +40% (total +57%)` (resto +17).
    /// O parênteses é o número que o jogador lê na ficha, então o resto é constatável em tela — o log
    /// `RV-44 item ...: aura=... total=... resto=...` imprime as três parcelas em cada hover.
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
    ///   - DE QUEM É O `ShrineEffectBonus` DO FATOR (fechado em 30/09 pelo teste do dono do jogo, RV-34):
    ///     é o do PRÓPRIO PERSONAGEM AVALIADO. A dúvida nasceu porque o executor do gatilho é
    ///     `UseTriggerSource && TriggerSource != null ? TriggerSource : this` (l.41051) com
    ///     `TriggerSource = actionStatus.Source` (l.33501) — mas a MEDIÇÃO em jogo venceu a leitura de
    ///     asset (hierarquia de fontes do projeto): com o perk `Worship` (+100 em `ShrineEffectBonus`,
    ///     um PERK DO PERSONAGEM) o dano por turno que o jogador RECEBE é o DOBRO. Logo o fator vale 2
    ///     nesse caso, e a origem do bônus é o personagem na aura (a vítima no Decay; cada alvo da lista
    ///     no Flame), não o personagem vazio do shrine. Prova no log do próprio jogo (30/09):
    ///     `RV-31 acumulado: ... char=Raven bonus=100` ao lado de `RV-33 linha do Decay: Raven
    ///     MaxHealth=233 -> ... (23 damage per turn for you)` — o número era 10% (23) com o bônus 100
    ///     que a aura de buff do MESMO personagem já aplicava (Life Steal +16 = base 8 × 2).
    ///
    /// RV-34 (30/09) — O FATOR ENTRA NA CONTA DAS DUAS AURAS DE PERIGO. As constantes de fórmula passam
    /// a ser o RHS do asset COPIADO BYTE A BYTE, com o `(1 + (Source["ShrineEffectBonus"] / 100))`
    /// dentro:
    ///   Flame: `Mathf.Max(1,  Mathf.Round((Target["MaxHealth"] * Target.GetValueByEnemyType(.025f,
    ///           .08f, .1f, .12f, .14f, .05f)) * (1 + (Source["ShrineEffectBonus"] / 100))))`
    ///   Decay: `Mathf.Round((Target["MaxHealth"] * Target.GetValueByEnemyType(.05f, .1f, .12f, .15f,
    ///           .2f, .1f)) * (1 + (Source["ShrineEffectBonus"] / 100)))`
    /// (assets @1519546098 len 187 e @1519519282 len 171; o texto COMPLETO, com o prefixo
    ///  `TargetStored["XDamage"] = `, é a chave do cache compilado l.87116/87156.)
    /// A avaliação usa `Source` = `Target` = o PERSONAGEM AVALIADO (`ValorDaExpressao` com os dois
    /// parâmetros): é ele quem leva o dano e é o `ShrineEffectBonus` DELE que o fator lê.
    ///
    /// SEM O ATRIBUTO NO BUILD, O NÚMERO FICA COMO ESTAVA: `Character[atributo]` LANÇA para nome
    /// desconhecido (l.32662-32675), então antes de avaliar qualquer fórmula com o fator confere-se
    /// `Game.Instance.GetAttribute("ShrineEffectBonus") != null` (`FormulaDoDano`). Faltando o atributo,
    /// entra a constante SEM o fator (a MESMA de antes) e o log diz o motivo — nada é estimado.
    ///
    /// O QUE ENTROU NA TOOLTIP (especificação do dono do jogo, 30/09): o Flame mostra UM ITEM POR ALVO
    /// que está na área da aura — quem TEM o status do Flame vivo, party e inimigos (`AlvosNaAreaDoFlame`)
    /// — com `Target` = esse alvo: vida máxima DELE × a % do tipo DELE × o bônus DELE, o CRU (sem
    /// mitigação nenhuma), porque o hover não sabe quem vai atacar. O Decay mostra o dano por turno do
    /// personagem em foco na própria linha do jogo. Em ambos o número é ANTES DAS REDUÇÕES DE DANO
    /// (RV-34): a marca curta está nas DUAS notas do `LocalizePatch` ("before damage reduction").
    ///
    /// RV-34 (30/09) — os `No Compiled Expression for (Single):` do log: 2 eram NOSSOS e 2 são do JOGO, e a
    /// natureza do aviso é de CACHE, não de falha (provado linha a linha no decompilado):
    ///   - quem escreve é `CompiledDynamicExpresso.GetExpression<T>` (l.49971-49995): se a string EXATA não
    ///     está no cache COMPILADO do build (`CompiledExpressions`), ele imprime `Debug.LogError` UMA vez
    ///     por string única (`MissingExpressions`, l.49980-49984) e devolve null; o `Game.GetExpression<T>`
    ///     (l.321789-321818) então COMPILA essa mesma string no interpretador (`Interpreter.ParseAsDelegate`,
    ///     l.321831) e devolve o valor CERTO. O aviso significa "esta string não veio pré-compilada no
    ///     build do jogo" — não "esta expressão falhou".
    ///   - prova no log do usuário (Player-prev.log l.3104-3107 e l.3134/3137): as duas primeiras são as
    ///     DUAS constantes do RV-26 (a fórmula do Flame e a % do Flame), e o número saiu CERTO logo depois
    ///     (`RV-26 linha com valor: Raven MaxHealth=233 -> ... 12 for you` = `Max(1, Round(233 * .05))`, com
    ///     o log do próprio mod entre o aviso e o valor). As outras DUAS são do JOGO, não nossas: as
    ///     `Amount` que o `Root.CreateSummon` monta em runtime (`Source.SummonMaster[...]`, decompilado
    ///     l.144099-144121), avaliadas no combate — nenhuma das duas strings existe no nosso código (grep
    ///     no repo e nas DLLs: 0).
    ///   - O ESPAÇAMENTO NÃO É A CAUSA (hipótese conferida): a string do RV-26 era o RHS do asset COPIADO
    ///     byte a byte — com os DOIS espaços de `Max(1,  ` (asset @1519546156) — e deu o aviso igual. A
    ///     chave do cache do jogo é a expressão INTEIRA, com o prefixo `TargetStored["FireDamage"] = `
    ///     (l.87156); qualquer string sem esse prefixo falta no cache, com um espaço ou com dois. Alinhar
    ///     espaçamento não removeria aviso nenhum.
    ///   - EFEITO PRÁTICO: as 3 constantes deste arquivo (`FormulaDanoFlameCru`, `FormulaDanoDecay`,
    ///     `PorcentagemDoDecay`) são avaliadas UMA vez por sessão e imprimiriam o MESMO aviso (3 linhas de
    ///     Error num log que o usuário lê), sem nada quebrado. `RegistrarNoCacheDoJogo` pré-registra essas
    ///     3 strings em `MissingExpressions` (por reflexão; campo ausente = nada suprimido) para o aviso não
    ///     sair. O valor e o caminho de compilação não mudam: `MissingExpressions` é lido SÓ nesse guard
    ///     (l.49980/50006) e o cache que resolve o valor é outro (`CompiledExpressions`). Falha REAL de
    ///     expressão continua imprimindo `This expression caused an error: ...` (l.321857-321869) e caindo
    ///     no fallback sem número.
    ///
    /// Nada aqui aplica mitigação: o número é o CRU da fórmula (vida máxima × % × o bônus do
    /// personagem), sem armadura, resistência ou qualquer modificador posterior. Sem número provado, a
    /// linha do jogo fica INTACTA.
    ///
    /// RV-46 (30/09) — DOIS DEFEITOS DA LINHA AZUL, os dois achados pelo dono em captura.
    ///
    /// (1) CONTRIBUIÇÃO MULTIPLICADA — `Dodge +120%` com a aura valendo 40 (print do dono, Rogue Shrine):
    ///     A CAUSA É INSTÂNCIA REPETIDA NA LISTA VIVA, NÃO STACK. Prova no log do jogo do dono
    ///     (`Player.log` do perfil, 30/09):
    ///       `RV-44 item 'DodgeChance': aura=+120% total=+75% resto=−45% em [Guardian Aura, Rogue Aura,
    ///        Reaper Aura, Conqueror Aura, Rogue Aura, Rogue Aura]` (l.3498) — a MESMA aura aparece TRÊS
    ///       vezes na lista, e cada instância entra na soma; o `RV-44 soma` do mesmo hover mostra
    ///       `'Rogue Aura' Base +40% (stacks=1)`, ou seja **1 stack por instância**: 3 × 40 = 120.
    ///     Mecânica (decompilado do build atual):
    ///       - `Character.GetAttributeValueByMethod` percorre TODAS as entradas de `ActionStatuses`
    ///         (Character.cs:8494) e soma o efeito de cada uma × `TotalStacks` (Character.cs:8563) —
    ///         não há dedupe no motor;
    ///       - quem CRIA a segunda instância é o próprio ground effect: `GroundEffect.AddGroundEffectedPlayer`
    ///         (l.102) só sai cedo se o jogador JÁ está em `EffectedPlayers` (l.104-110) e, ao aplicar,
    ///         cria um status NOVO (`GameLogic.CreateActionStatus`, l.158). `RemoveGroundEffectedPlayer`
    ///         (l.174-216) só remove quando `item.Infinite` — e as auras do censo têm `Infinite=False`
    ///         (dump `[Status] ... | maxStk=100`). Logo: sair e voltar à área (ou terminar o movimento
    ///         nela) ACUMULA instâncias do mesmo status até a duração de 3 turnos expirar.
    ///     Por que o TOTAL (75) não fecha com 120 — e não é erro do mod: os atributos do jogo têm TETO
    ///     (`Character.GetAttribute`, Character.cs:11871-11878: `if (HasMax && num > MaxValue) num = MaxValue`).
    ///     No asset, `DodgeChance` tem `HasMax` com **MaxValue = 75** (`resources.assets` @1519604232;
    ///     os dois bools imediatamente antes são HasMax=1/UseMaxAttribute=0) e `DamageReduction` tem
    ///     **MaxValue = 50** (@1519603860). A medição bate: o índice `Character[atributo]` sai 51.9 com
    ///     UMA Rogue Aura viva (resto 11.9 do personagem) e **75** com duas e com três (91.9/131.9
    ///     cortados no teto); `Damage taken` sai −40 com um Guardian e **−50** com dois (−80 cortado).
    ///     O CONTRIBUTO, portanto, tem de contar cada aura UMA VEZ — é o número que a própria linha
    ///     branca do shrine mostra (`Increases dodge chance by 40%.`) e o que o motor avalia na
    ///     expressão do asset (20 × (1 + bônus/100)); a soma por INSTÂNCIA era a multiplicação.
    ///     `AurasUnicas` (abaixo) desduplica a lista viva pelo status (nome + descrição) para os
    ///     ITENS e para a soma; as repetições vão para o log (`instancias=[nome xN]` na âncora e
    ///     `RV-46 instancias`), nunca para o número. O multiplicador por `TotalStacks` CONTINUA
    ///     (é regra do motor, Character.cs:8563) — no caso do print os stacks eram 1, então ele não
    ///     era a causa; fica só o que o motor realmente usa.
    ///     Teto vai no log (`RV-46 teto '<atributo>'`): com o total no teto o `resto` deixa de ser
    ///     comparável e quem lê o log precisa saber disso. Nenhum texto mudou por causa do teto.
    ///
    /// (2) AURA VIVA FORA DA LISTA — a aura do Dwarven não aparecia (defeito do dono, 30/09: com a
    ///     `Dwarven Aura` ativa a linha mostrava `Damage taken`, `Crit Chance`, `Dodge` e `Life Steal`
    ///     e NADA do Dwarven). CAUSA: os itens saem por ATRIBUTO de personagem (`AtributosDasAuras` /
    ///     `ContribuicaoDasAuras` casam `CharacterEffectInfo.CharacterAttribute`) e o efeito do Dwarven
    ///     NÃO é atributo: o dump de boot do próprio jogo diz `[Status] 'Dwarven Aura' | efeitos= |
    ///     nAttrEf=0 | nTrig=1 | trigEf=OnHittingDamaging[cond=Source.IsEnemy(Target)~status=Stunned]`
    ///     — o valor mora na CHANCE do gatilho: `SkillTriggers[0].ActionStatusChanceEquations[0]`
    ///     (`SkillTrigger.cs:34`; o motor avalia com `Game.Eval<float>` — Character.cs:12492/12511 —,
    ///     exatamente o mesmo caminho que `ValorDaExpressao` usa). No asset (`Dwarven Totem Aura Status`,
    ///     `resources.assets` @1517115056) a fórmula aparece 2×:
    ///       @1517115395 (ao lado da Description, = `DescriptionExpressions[0]`) e
    ///       @1517115647 (dentro do gatilho, ao lado de `Source.IsEnemy(Target)`/`Cell.IsCurrentHex(Target)`)
    ///     — as DUAS são `Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100)))`, o mesmo número
    ///     da linha branca do shrine (40 com bônus 100). É esse o item: `Stun chance +40%`.
    ///     REGRA QUE FICA (dono, 30/09): a linha se chama "Your active shrine auras" e se apresenta como
    ///     COMPLETA — nenhuma aura viva pode sair em silêncio. Das 12, TRÊS têm efeito que não é atributo
    ///     de personagem (censo: 9/9 das outras têm `AttributeEffects`): Dwarven (chance de stun),
    ///     Decay Shrine Aura (`OnTurnStart`, dano por turno) e Flame Shrine Aura (`OnGettingHitDamaging`,
    ///     dano em quem ataca). As três ganham item próprio com o número do asset avaliado pelo motor
    ///     (`ItemDaAuraSemAtributo`); qualquer aura viva que NÃO virar item sai no log com o motivo
    ///     (`RV-46 AVISO`), nunca sumindo calada.
    ///
    /// ASSINATURA: nada muda no Harmony aqui — este arquivo segue com a assinatura explícita por TIPO
    /// no único patch (`ApplyDescriptionExpressions`, 5 tipos, `ref __2`) e nenhum parâmetro por índice
    /// novo. Todo o trabalho novo é código de leitura, dentro de try/catch.
    ///
    /// DWA-2 (30/09) — A DEDUPE DO RV-46 ERA AMPLA DEMAIS: ela é por TIPO DE EFEITO, não por aura.
    ///
    /// O dono reportou que `Dwarven Aura` não stacka com mais de um `Dwarven Shrine` no alcance. A
    /// causa: o RV-46 passou a desduplicar a lista viva ANTES de tudo, e isso está certo para efeito de
    /// ATRIBUTO, mas o efeito do Dwarven é CHANCE DE GATILHO — e aí o motor NÃO corta a repetição.
    ///
    /// O QUE O MOTOR FAZ, POR TIPO (decompilado do build atual; os números de linha são do arquivo
    /// `Assembly-CSharp.decompiled.cs` do cache):
    ///
    ///  (a) EFEITO DE ATRIBUTO DE PERSONAGEM (`ActionStatusInfo.AttributeEffects` com
    ///      `EffectTarget = Target`): `Character.GetAttributeValueByMethod` percorre a lista de status
    ///      do personagem inteira (l.37194), casa o efeito pelo ATRIBUTO e soma
    ///      `valor * TotalStacks` por status (l.37255-37273) — SEM dedupe. Quem corta é o TETO do
    ///      atributo: `Character.GetAttribute`, l.40571-40578 (`HasMax` → `MaxValue`/`MaxAttribute`),
    ///      depois do `Mathf.Ceil` (l.40587). Ou seja: as instâncias extras SOMAM no motor e o teto
    ///      pode engolir essa soma; a CONTRIBUIÇÃO de UMA aura é o número que a linha branca do shrine
    ///      mostra (`20 * (1 + bônus/100)`) e é o que a linha azul exibe, UMA VEZ por aura — é a regra
    ///      do RV-46 e ela continua valendo aqui (`AurasUnicas`).
    ///
    ///  (b) EFEITO DE GATILHO (status com `SkillTriggers`, sem atributo de personagem): o motor NÃO
    ///      corta — ele CONTA a repetição, uma vez por INSTÂNCIA viva:
    ///        - `Character.SkillTriggers` (getter, l.33467) percorre `ActionStatuses` (l.33489) e
    ///          acrescenta os `SkillTriggers` de CADA status (l.33497-33508). Com o MESMO status vivo
    ///          N vezes, o MESMO gatilho entra N vezes na lista.
    ///        - `Character.ProcessSkillTriggers` copia essa lista inteira (l.40948-40952) e percorre
    ///          TODAS as entradas (l.40953): o único guard que poderia pular a segunda é o cooldown do
    ///          PRÓPRIO gatilho (l.40956, `TriggerCooldownDict[trigger] > 0f`, alimentado por
    ///          `trigger.Cooldown` em l.40995). O gatilho do Dwarven tem `Cooldown = 0` no asset
    ///          (conferido nos bytes: `resources.assets` @1517115748 = `00 00 00 00`, na MESMA posição
    ///          em que o gatilho do `Quick Hands` tem `00 00 80 3f` = 1.0 — e cujo `cooldownTrig=1` o
    ///          log do jogo mostra, casando com o "Can only trigger once per turn." do texto dele), e
    ///          `MaxNumUses` vazio — nada bloqueia a segunda instância.
    ///        - A chance é rolada POR ENTRADA: `GetRollResult(Burst2Flame.Game.Eval<float>(
    ///          trigger.ActionStatusChanceEquations[num8]))` (l.41211-41216), com a expressão do asset
    ///          — a MESMA string da `DescriptionExpressions[0]`. `TotalStacks` NÃO multiplica chance de
    ///          gatilho (o fator de stacks existe só no caminho de ATRIBUTO, l.37263).
    ///      Consequência: com DOIS Dwarven Shrines no alcance há DUAS `Dwarven Aura` vivas (cada shrine
    ///      do mapa tem o PRÓPRIO `Source`: `ConvertToGroundEffect` recebe o character do shrine,
    ///      l.110814-110822, e o status é criado por ground effect em `GroundEffect.AddGroundEffectedPlayer`,
    ///      l.116924) e o motor rola a chance DUAS vezes por golpe. Esconder a segunda instância era o
    ///      defeito; o número NÃO é somado a mão (duas rolagens de 40% não são "80%").
    ///
    /// A REGRA TIPADA QUE FICA (nenhum nome de aura no meio): `TipoDoEfeito` lê o ASSET do
    /// status (`AttributeEffects` → `Atributo`; `SkillTriggers` → `Gatilho`) e `AurasQueContamPorInstancia`
    /// monta a lista dos itens sem atributo: aura de ATRIBUTO entra UMA vez (RV-46), aura de GATILHO
    /// entra UMA vez POR INSTÂNCIA. O tipo é logado (`RV-46/DWA-2 tipos de efeito`) e as contagens
    /// também — a linha continua se apresentando como COMPLETA.
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

                // RV-34 — o Source do personagem VAZIO do shrine TAMBÉM é trocado pelo receptor: é o
                // que faz o `[0]` das duas auras de perigo sair com o bônus REAL. Prova no asset
                // (status serializados em UTF-8): a expressão do status do Decay é
                // `Mathf.Round(10 * (1 + (Source["ShrineEffectBonus"] / 100)))` e a do Flame,
                // `Mathf.Round(5 * (1 + (Source[...] / 100)))` — as DUAS leem `Source`, e o hover do
                // shrine entrega `Source = Root.WorldCharacter` (l.214179/214182), o personagem sem
                // bônus: sem esta troca a linha diria "Take 10%" enquanto o dano real dobra. Só é
                // trocado quando o Source é EXATAMENTE esse personagem (`EhPersonagemVazioDoShrine`);
                // `Source` de skill/status com personagem de verdade (o caster) não é tocado.
                bool alvoVazio = __2.Target == null;
                bool fonteVazia = __2.Source == null;
                bool fonteEhMundoDoShrine = !fonteVazia && EhPersonagemVazioDoShrine(__2.Source);
                if (!alvoVazio && !fonteVazia && !fonteEhMundoDoShrine)
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

                // Preenche o que está vazio e troca o Source VAZIO do shrine pelo receptor: o número
                // passa a ser calculado com o bônus REAL do receptor (Omnism I/II +8/+12 = 20; perk
                // Worship = 100; item Horn of Devotion {50,100}).
                if (fonteVazia || fonteEhMundoDoShrine)
                {
                    __2.Source = receptor;
                }
                if (alvoVazio)
                {
                    __2.Target = receptor;
                }
                Marca($"params: Target{(alvoVazio ? "(vazio)->" : "(intacto)")}{receptor.CharacterName}"
                    + $" Source{(fonteVazia ? "(vazio)->" : fonteEhMundoDoShrine ? "(shrine)->" : "(intacto)")}"
                    + $"{(fonteVazia || fonteEhMundoDoShrine ? receptor.CharacterName : "(mantido)")}");
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
        /// RV-34 — o `Source` que o hover do shrine entrega é o `Root.WorldCharacter`: o personagem
        /// VAZIO do ground effect (`Root.CreateNewGroundEffectCharacter` -> `Observable.New&lt;Character&gt;()`,
        /// decompilado l.110814/143680), sem nome, sem vida e SEM `ShrineEffectBonus`. O motor o usa como
        /// origem da aura, mas o bônus que o jogador quer ver é o do receptor: a MEDIÇÃO em jogo (RV-34)
        /// mostrou o dano do Decay DOBRANDO com o perk `Worship`, e as expressões dos status do Decay e
        /// do Flame leem `Source[...]` (asset) — com o personagem vazio elas sairiam sempre na base.
        ///
        /// A troca é por IDENTIDADE contra esse personagem exato: nenhum `Source` de skill/status (que
        /// é o caster, um personagem de verdade) entra aqui.
        /// </summary>
        private static bool EhPersonagemVazioDoShrine(Character fonte)
        {
            if (fonte == null)
            {
                return false;
            }
            try
            {
                Character mundo = NetworkingManager.Instance?.NetworkManager?.Root?.WorldCharacter;
                return mundo != null && ReferenceEquals(fonte, mundo);
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[Shrine RV-34] WorldCharacter indisponivel: {ex.GetType().Name}: {ex.Message}");
                return false;
            }
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
        /// RV-26 (30/09), reescrito no RV-33 e no RV-34 — o NÚMERO do Flame Shrine por ALVO NA ÁREA DA
        /// AURA.
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
        /// RV-34 — CRU e COMPLETO, como pedido: `Mathf.Max(1, Mathf.Round(MaxHealth ×
        /// GetValueByEnemyType(...) × (1 + Source["ShrineEffectBonus"]/100)))`. O `Mathf.Max(1,` é do
        /// jogo; o fator do bônus ENTRA (medido em jogo: com `Worship` o dano dobra) e é lido do PRÓPRIO
        /// ALVO (`Source` = `Target` = o alvo da vez). Não entra redução de dano, resistência nem
        /// modificador posterior — a marca "before damage reduction" está na nota da chave.
        ///
        /// TX-1 (01/10) — ONDE ESTA FRASE ENTRA: no COMECO do bloco da nota da chave (`LocalizePatch`,
        /// trecho `original == ShrineAuraPatch.ChaveFlame`), colada na linha branca do jogo — valor
        /// primeiro, explicacao curta depois. O TEXTO da frase nao mudou: continua dizendo que o numero e
        /// `raw damage` (PRE-REDUCAO) e que sai da vida maxima E do Shrine Effect Bonus DO PROPRIO
        /// personagem avaliado como atacante.
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
                    // RV-34: Source = Target = o alvo — o alvo é quem leva o dano e é o
                    // `ShrineEffectBonus` DELE que o fator `(1 + Source[...]/100)` lê (Worship -> dobro).
                    if (!ValorDaExpressao(FormulaDoDano(FormulaDanoFlameCru, FormulaDanoFlameSemBonus), alvo, alvo, out dano))
                    {
                        Marca($"RV-34 Flame alvo '{alvo.CharacterName}' sem numero: formula nao avaliada");
                        continue;
                    }
                    string nome = string.IsNullOrEmpty(alvo.CharacterName) ? "(sem nome)" : alvo.CharacterName;
                    // RV-45: o `0.#` NÃO pode imprimir fração — o dano vem de `Mathf.Max(1,
                    // Mathf.Round(...))` na fórmula do asset (inteiro por construção).
                    partes.Add(nome + " " + dano.ToString("0.#"));
                    // Item 6 da especificação: o log diz DE QUAL ALVO saiu cada número, com a vida máxima,
                    // o tipo e o BÔNUS dele que entraram na conta, para a conferência em jogo.
                    Marca($"RV-34 Flame alvo '{nome}': MaxHealth={alvo.MaxHealth.ToString("0.#")}"
                        + $" tipo={TipoDoAlvo(alvo)} bonus={BonusDoReceptor(alvo)} dano={dano.ToString("0.#")}");
                }
                if (partes.Count == 0)
                {
                    return "";
                }
                return "In the aura now (raw damage it takes as the attacker, from its own Max Health"
                    + " and its own Shrine Effect Bonus): " + string.Join("; ", partes.ToArray()) + ".";
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
        /// RV-34 — a fórmula do dano do Flame por alvo, CRUA como o dono do jogo pediu: vida máxima × a
        /// % do tipo do próprio alvo × o `ShrineEffectBonus` DELE, com o `Mathf.Max(1,` do jogo. É o RHS
        /// do asset da ação `Flame Aura Proc` COPIADO BYTE A BYTE (`resources.assets` @1519546098,
        /// UTF-16, len 187 — o texto completo tem o prefixo `TargetStored["FireDamage"] = ` e a mesma
        /// string está no cache compilado l.87156/87158). Avaliada pelo INTERPRETADOR DO PRÓPRIO JOGO
        /// (`Game.TryEval`), com `Source` = `Target` = o alvo da vez (o alvo é quem leva o dano e é o
        /// bônus DELE que o fator lê — prova em jogo no cabeçalho): nenhum número é escrito à mão aqui.
        /// </summary>
        private const string FormulaDanoFlameCru =
            "Mathf.Max(1,  Mathf.Round((Target[\"MaxHealth\"] * Target.GetValueByEnemyType(.025f, .08f, .1f, .12f, .14f, .05f)) * (1 + (Source[\"ShrineEffectBonus\"] / 100))))";

        /// <summary>
        /// RV-34 — a MESMA fórmula do Flame SEM o fator do `ShrineEffectBonus` (a constante do RV-33).
        /// Só entra quando o atributo NÃO existe neste build (`FormulaDoDano`), porque o indexador
        /// `Character[atributo]` lança para nome desconhecido: sem o atributo, o número fica como estava
        /// e o log diz por quê — nada é estimado.
        /// </summary>
        private const string FormulaDanoFlameSemBonus =
            "Mathf.Max(1, Mathf.Round(Target[\"MaxHealth\"] * Target.GetValueByEnemyType(.025f, .08f, .1f, .12f, .14f, .05f)))";

        /// <summary>A chave de texto exata do Decay Shrine (a descrição da aura).</summary>
        internal const string ChaveDecay = "Take [0]% of your Max Health in Shadow Damage per turn.";

        /// <summary>
        /// RV-46 — a chave de texto exata do Dwarven (a descrição da aura). É a aura cujo efeito NÃO é
        /// atributo de personagem: o valor vive na CHANCE do gatilho (`Stunned`) — ver
        /// `ExpressaoDeChance`/`RotuloSemAtributo`.
        /// </summary>
        internal const string ChaveDwarven = "Your attacks have a [0]% chance to stun the target.";

        /// <summary>
        /// RV-34 — a fórmula do dano por turno do Decay, CRUA: vida máxima do próprio personagem × a %
        /// do tipo DELE × o `ShrineEffectBonus` DELE, SEM o `Mathf.Max(1,` (o Decay pode dar 0). É o RHS
        /// do asset da ação `Decay Aura Proc` COPIADO BYTE A BYTE (`resources.assets` @1519519282,
        /// UTF-16, len 171 — o texto completo tem o prefixo `TargetStored["ShadowDamage"] = ` e a mesma
        /// string está no cache compilado l.87116/87118). Avaliada pelo interpretador do jogo com
        /// `Source` = `Target` = o personagem em foco (é ele quem leva o dano e é o bônus DELE que o
        /// fator lê). A lista de % é (.05f, .1f, .12f, .15f, .2f, .1f — 5% boss, 10% champion,
        /// 12% elite, 15% soldier, 20% fodder, 10% player).
        /// </summary>
        private const string FormulaDanoDecay =
            "Mathf.Round((Target[\"MaxHealth\"] * Target.GetValueByEnemyType(.05f, .1f, .12f, .15f, .2f, .1f)) * (1 + (Source[\"ShrineEffectBonus\"] / 100)))";

        /// <summary>
        /// RV-34 — a MESMA fórmula do Decay SEM o fator do `ShrineEffectBonus` (a constante do RV-33).
        /// Só entra quando o atributo NÃO existe neste build (`FormulaDoDano`): sem o atributo, o número
        /// fica como estava e o log diz por quê — nada é estimado.
        /// </summary>
        private const string FormulaDanoDecaySemBonus =
            "Mathf.Round(Target[\"MaxHealth\"] * Target.GetValueByEnemyType(.05f, .1f, .12f, .15f, .2f, .1f))";

        /// <summary>
        /// RV-34 — escolhe a fórmula do dano pela DISPONIBILIDADE do atributo no build. O indexador
        /// `Character[atributo]` LANÇA para nome desconhecido (decompilado l.32662-32675), então a
        /// fórmula COM o fator `(1 + (Source["ShrineEffectBonus"] / 100))` só entra quando
        /// `Game.Instance.GetAttribute` encontra o atributo. Sem ele, o número fica como estava (a
        /// constante SEM o fator) e o log diz o motivo — número provado ou nada, regra do projeto.
        /// </summary>
        private static string FormulaDoDano(string comFator, string semFator)
        {
            if (Burst2Flame.Game.Instance?.GetAttribute("ShrineEffectBonus") != null)
            {
                return comFator;
            }
            Marca("RV-34 fator do ShrineEffectBonus NAO aplicado: atributo ausente neste build"
                + " — o numero sai como estava, SEM o fator (nada estimado)");
            return semFator;
        }

        /// <summary>
        /// RV-34 — o fator `(1 + ShrineEffectBonus/100)` do personagem, lido pelo INDEXADOR do jogo
        /// (`Character.this[string]`) — o MESMO valor que a expressão `Source["ShrineEffectBonus"]` lê.
        /// Usado só no caminho de RESERVA do Decay (quando a fórmula inteira não é avaliada). Sem o
        /// atributo no build, ou em falha de leitura, devolve 1: o número fica o de antes, nunca um
        /// bônus estimado.
        /// </summary>
        private static float FatorDoBonus(Character personagem)
        {
            if (personagem == null)
            {
                return 1f;
            }
            if (Burst2Flame.Game.Instance?.GetAttribute("ShrineEffectBonus") == null)
            {
                Marca("RV-34 reserva do Decay sem fator: atributo ShrineEffectBonus ausente neste build");
                return 1f;
            }
            try
            {
                return 1f + personagem["ShrineEffectBonus"] / 100f;
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[Shrine RV-34] leitura do ShrineEffectBonus falhou (fator=1): {ex.GetType().Name}: {ex.Message}");
                return 1f;
            }
        }

        /// <summary>
        /// RV-33/RV-34 — o DANO POR TURNO do Decay Shrine como NÚMERO na linha do jogo.
        ///
        /// Entrega a linha ORIGINAL (`Take [0]% ... per turn.`) com o dano literal acrescentado no fim —
        /// o `[0]` é PRESERVADO de propósito: quem troca o `[0]` pela % do status é o motor
        /// (`ApplyDescriptionExpressions`). A expressão do status no asset (`Decay Shrine Aura`, UTF-8)
        /// é `Mathf.Round(10 * (1 + (Source["ShrineEffectBonus"] / 100)))` e ela lê `Source` — o
        /// `ShrineAuraPatch` (prefix, RV-34) entrega aí o personagem em foco, de modo que a % E o dano
        /// saem com o MESMO bônus e não se contradizem (com Worship: "20%" e o dobro do dano).
        ///
        /// O `Target`/`Source` da avaliação é o personagem em foco (o `ReceptorDaTooltip`, resolvido como
        /// a TooltipCharacter): é ele quem está na aura, é quem o proc do Decay acerta no começo do turno
        /// dele (TriggerType `OnTurnStart` + `Targets = Cell.IsCurrentHex(Source)` com `Source = this` =
        /// o portador — prova no cabeçalho desta classe) e é o `ShrineEffectBonus` DELE que o fator lê
        /// (medido em jogo: com Worship o dano dobra). Um personagem de 100 de vida COM Worship mostra
        /// "20 damage per turn for you"; sem o perk, "10".
        ///
        /// O número é ANTES DAS REDUÇÕES DE DANO (RV-34) — a marca está na nota da chave no
        /// `LocalizePatch` ("before damage reduction").
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
                // RV-34: Source = Target = o personagem na aura — ele é quem leva o dano (o proc roda no
                // começo do turno DELE) e é o ShrineEffectBonus DELE que o fator lê (com Worship, o dobro).
                if (!ValorDaExpressao(FormulaDoDano(FormulaDanoDecay, FormulaDanoDecaySemBonus), naAura, naAura, out dano))
                {
                    // Reserva: a MESMA conta, com a % lida pelo interpretador (o Decay NÃO tem
                    // Mathf.Max(1, então o 0 é um resultado legítimo) e o fator do bônus lido do
                    // personagem pelo indexador — 1 quando o atributo não existe: nada é estimado.
                    float pct;
                    if (!ValorDaExpressao(PorcentagemDoDecay, naAura, naAura, out pct))
                    {
                        Marca("RV-34 Decay sem numero: formula e % nao avaliadas pelo interpretador");
                        return null;
                    }
                    dano = Mathf.Round(naAura.MaxHealth * pct * FatorDoBonus(naAura));
                    Marca("RV-34 Decay reserva: formula completa nao avaliada; dano montado a partir da % e do bonus do personagem");
                }
                // A linha do jogo termina em ponto: o número entra antes dele, e o `[0]` fica no lugar.
                // RV-45: o `0.#` aqui NÃO pode imprimir fração — o número vem do `Mathf.Round` da
                // própria fórmula do asset (ou, na reserva, de `Mathf.Round(MaxHealth x % x fator)`),
                // ou seja já é inteiro. Conferido: nenhuma conta desta linha passa pelo formatador de
                // atributo (`InteiroDoJogo`), que é o único lugar onde a fração existia.
                string linha = ChaveDecay.Substring(0, ChaveDecay.Length - 1)
                    + " (" + dano.ToString("0.#") + " damage per turn for you).";
                // CHK-1 §7.1 (conserto APLICADO) — O `tipo=` DO PORTADOR ENTROU NA MARCA. O esperado do
                // Decay e `MaxHealth x % DO TIPO x (1 + bonus)` e a % muda por tipo (player 10%, IA
                // 5..20 — `FormulaDanoDecay`); sem o campo, a conferencia mecanica so podia calcular
                // com a % de `player` (o unico caminho pelo qual o mod resolve o receptor) e um
                // portador IA virava ACHADO sem causa atribuivel. O `TipoDoAlvo` e o MESMO da linha do
                // Flame (mesma nomenclatura, mesma fonte). Campo de LOG: nenhum texto do jogador muda.
                Marca($"RV-34 linha do Decay: {naAura.CharacterName} MaxHealth={naAura.MaxHealth.ToString("0.#")}"
                    + $" tipo={TipoDoAlvo(naAura)} bonus={BonusDoReceptor(naAura)} -> '{linha}'");
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
        /// RV-43 (01/10) — O SINAL É TRATADO EM TODOS OS CASOS: um total pode ser POSITIVO onde a aura
        /// empurra para baixo (Energy Coil −50 + `Forbidden Power` ManaCostMod:Base:50, status.csv:191,
        /// ou `Fuel for the Flames I/II` +20/+30, skills.csv:178-179 = total +20) e NEGATIVO onde a aura
        /// soma. Antes só DamageReduction, ManaCostMod e o default tratavam o sinal; os outros montavam
        /// "+" fixo e imprimiriam "+ -20%" com total negativo. O rótulo do total POSITIVO é o
        /// comportamento correto de hoje e NÃO muda.
        /// RV-45 (01/10) — A GRANDEZA SAI INTEIRA (`InteiroDoJogo`), como na ficha do próprio jogo:
        /// antes o rótulo do `Damage taken`/`Mana Costs` usava `ToString("0.#")` e imprimia o decimal
        /// da fração do equipamento. No zero o rótulo lê "+0%" (é a mesma leitura da ficha; a forma
        /// anterior escolhia o "−" por causa do sinal do float cru).
        /// null = atributo que não está nesta lista; quem chamou usa o nome do próprio jogo.</summary>
        private static string Format(string attr, float v)
        {
            int n = InteiroDoJogo(v);
            switch (attr)
            {
                case "DamageReduction":
                    return n > 0 ? "Damage taken −" + n + "%" : "Damage taken +" + Mathf.Abs(n) + "%";
                case "ManaCostMod":
                    return n <= 0 ? "Mana Costs reduced by " + Mathf.Abs(n) + "%"
                                  : "Mana Costs increased by " + n + "%";
                case "DamageMod": return "Damage " + ComSinal(v) + "%";
                case "CritChance": return "Crit Chance " + ComSinal(v) + "%";
                case "DodgeChance": return "Dodge " + ComSinal(v) + "%";
                case "LifeOnHit": return "Life Steal " + ComSinal(v) + "%";
                case "HealthPerTurnPercent": return "Health per turn " + ComSinal(v) + "%";
                case "ManaPerTurnPercent": return "Mana per turn " + ComSinal(v) + "%";
                default: return null;
            }
        }

        /// <summary>RV-43 — valor com o SINAL explícito, no MESMO formato do rótulo de atributo
        /// desconhecido (o `default` do `TextDoEfeito`): "+" para total positivo ou ZERO, "−"
        /// (menos U+2212, o mesmo dos outros rótulos) para negativo.
        /// RV-45 — sai no INTEIRO da convenção do jogo (`InteiroDoJogo`): o exemplo que originou o
        /// conserto é o `(total +53.4%)` do print do dono. O texto que o jogo mostra da MESMA grandeza
        /// é inteiro ("Crit chance increased by 54%"), então a linha azul não pode destoar. O sinal é
        /// lido DEPOIS do arredondamento (senão `-0.4` viraria "−0").</summary>
        private static string ComSinal(float v)
        {
            int n = InteiroDoJogo(v);
            return (n >= 0 ? "+" : "−") + Mathf.Abs(n);
        }

        /// <summary>
        /// RV-45 — O VALOR DE ATRIBUTO NA GRANDEZA QUE O JOGO EXIBE. Descoberta no decompilado:
        /// `InventoryManager.UpdateStats` (decompilado l.125348-125356) monta o valor do atributo na
        /// FICHA com `component.text = GUIManager.instance.floatToText(Mathf.Ceil(character[atributo]))`
        /// e `GUIManager.floatToText` (l.93303-93310) é `f.ToString()` — ou seja: o jogo arredonda PARA
        /// CIMA (`Mathf.Ceil`) e imprime INTEIRO, mesmo quando o atributo tem fração (equipamento dá
        /// décimos de crit/dodge). É a MESMA grandeza que a linha azul mostra (o `Character[atributo]`),
        /// então a linha azul usa a mesma regra da ficha.
        ///
        /// O jogo tem uma SEGUNDA convenção na tela de level up (`RoguelikeManager`, l.163759-163764:
        /// `CurrentRoguelikeSkillSelectingCharacter[atributo].ToString("F0")`, que arredonda ao par) e
        /// ela NÃO se aplica aqui: o número da linha azul é o da FICHA, e é a ficha que o jogador abre
        /// para conferir/equipar. Mesmo critério do `BetterStats`, que já aplica `Mathf.Ceil` nos DOIS
        /// lugares (l.179 e l.335) — precedente aprovado do projeto.
        ///
        /// Isto é FORMATO, não conta: nenhuma fórmula do RV-34 muda (as duas auras de perigo continuam
        /// saindo do interpretador do motor, o Decay com `Mathf.Round` e sem `Max(1)`, o Flame com
        /// `Max(1, Round(...))` e o fator do `ShrineEffectBonus` em ambos — nenhum deles passa por
        /// aqui). NaN/infinito (estado corrompido) vira 0 em vez de derrubar a tooltip.
        /// </summary>
        private static int InteiroDoJogo(float v)
        {
            return (float.IsNaN(v) || float.IsInfinity(v)) ? 0 : Mathf.CeilToInt(v);
        }

        /// <summary>
        /// RV-44 — o TOTAL do personagem no parênteses do item, na MESMA grandeza do rótulo que vem
        /// antes dele: `DamageReduction` positivo REDUZ o dano tomado, então o valor sai invertido
        /// (`Damage taken +25% (total +5%)` = aura empurrando +25 de dano tomado e um total de +5, isto
        /// é, `DamageReduction` = −5 no indexador). Nos outros atributos o sinal cru serve — inclusive
        /// `ManaCostMod`, cujo total POSITIVO é custo aumentado (RV-43) e o rótulo da frente
        /// (`Mana Costs reduced by 50%` / `increased by 20%`) já diz para que lado a aura empurra.
        /// Não é uma segunda leitura do motor: é o MESMO `Character[atributo]` que já foi lido.
        /// RV-45 — o inteiro da ficha (`InteiroDoJogo`) é aplicado ao valor CRU do atributo e SÓ DEPOIS
        /// o sinal é invertido: inverter primeiro arredondaria do lado errado do número
        /// (`Ceil(-53.4) = -53`, que é o `-53` que a ficha mostra; `-Ceil(53.4) = -54`).
        /// </summary>
        private static string TotalComSinal(string nome, float v)
        {
            int n = InteiroDoJogo(v);
            float exibido = string.Equals(nome, "DamageReduction", StringComparison.Ordinal) ? -n : n;
            return ComSinal(exibido) + "%";
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
        ///
        /// RV-44 — cada item é a **contribuição das auras** na frente e o **total do personagem** no
        /// parênteses: `Dodge +40% (total +57%)`, `Damage +25% (total +50%)`. A contribuição sai do
        /// `AttributeEffects` das auras vivas (`ContribuicaoDasAuras`), o total do indexador do motor.
        /// Sem contribuição separável com confiança, o item sai só com o total (fallback).
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

                // (c) RV-46 — UMA VEZ POR AURA: a lista viva pode carregar a MESMA aura repetida (cada
                // (re)entrada na área cria um status NOVO — ver o cabeçalho) e somar por instância é o
                // defeito do print do dono (`Dodge +120%` com a aura valendo 40). Os itens e a soma
                // usam a lista desduplicada; as repetições vão para o LOG, nunca para o número.
                List<string> repeticoes;
                List<ActionStatus> unicas = AurasUnicas(ativas, out repeticoes);
                if (repeticoes.Count > 0)
                {
                    Marca($"RV-46 instancias repetidas na lista viva de {receptor.CharacterName}:"
                        + $" [{string.Join(", ", repeticoes.ToArray())}] — o motor soma cada instancia"
                        + " (Character.cs:8494 + TotalStacks em Character.cs:8563) e o TETO do atributo"
                        + " corta o total; a CONTRIBUICAO conta cada aura UMA vez (e o numero que a linha"
                        + " branca do proprio shrine mostra)");
                }

                // (c2) DWA-2 — A DESDUPE ACIMA E PARA EFEITO DE ATRIBUTO. E o TIPO do efeito (lido do
                // asset do status, nunca do nome da aura) que diz se a repeticao conta no MOTOR:
                //   - ATRIBUTO de personagem: o motor SOMA as instancias e o TETO corta (l.37194/37263 +
                //     l.40571-40578) -> cada aura entra UMA vez (RV-46, e a regra do `Dodge +120%`);
                //   - GATILHO (`SkillTriggers` sem atributo): o motor monta a lista de gatilhos um POR
                //     status vivo (l.33489-33508), percorre TODAS as entradas (l.40953-40959) e rola a
                //     chance de novo em cada uma (l.41211-41216) -> cada INSTANCIA conta, e o item sai
                //     uma vez por instancia (o motor rola N vezes; nao existe soma de chance).
                List<string> contamAtributo;
                List<string> contamGatilho;
                List<ActionStatus> porInstancia = AurasQueContamPorInstancia(ativas, out contamAtributo,
                    out contamGatilho);
                if (contamGatilho.Count > 0)
                {
                    Marca($"RV-46/DWA-2 tipo do efeito: atributo=[{string.Join(", ", contamAtributo.ToArray())}]"
                        + " (1x por aura: o motor soma as instancias e o teto do atributo corta —"
                        + " l.37194/37263 + l.40571-40578)"
                        + $" | gatilho=[{string.Join(", ", contamGatilho.ToArray())}]"
                        + " (1 item por INSTANCIA: o gatilho entra na lista uma vez por status vivo"
                        + " — l.33489-33508 —, o laco percorre todas as entradas — l.40953-40959 — e a"
                        + " chance e rolada de novo em cada uma — l.41211-41216; o gatilho do Dwarven tem"
                        + " Cooldown=0 e MaxNumUses vazio no asset, entao nada bloqueia a repeticao;"
                        + " TotalStacks NAO multiplica chance de gatilho)");
                }

                // (d) CONTEÚDO AGREGADO: um item por ATRIBUTO que as auras vivas mexem (a intenção do
                // RV-20, cujo nome sempre foi no plural). As auras cujo efeito NÃO é atributo de
                // personagem (Dwarven/Decay/Flame) ganham item próprio logo abaixo (RV-46) — mas a
                // ausência de atributo não pode mais MATAR a linha (senão uma área só com o Dwarven
                // mostraria "suas auras ativas" vazio).
                List<CharacterAttribute> atributos = AtributosDasAuras(unicas);
                if (atributos.Count == 0)
                {
                    Marca($"RV-46 nenhuma das {unicas.Count} aura(s) viva(s) de {receptor.CharacterName}"
                        + " mexe em atributo de personagem — os itens saem do proprio status quando o"
                        + " asset da o numero (Dwarven/Decay/Flame)");
                }

                // (e) DOIS NÚMEROS POR ITEM (RV-44): a CONTRIBUIÇÃO DAS AURAS na frente — é o que o
                // nome da linha ("Your active shrine auras") promete — e o TOTAL DO PERSONAGEM entre
                // parênteses. O total continua saindo do MOTOR (`Character[atributo]`, o MESMO número
                // da ficha/BetterStats: base + gear + skills + auras); a contribuição sai do
                // `AttributeEffects` das auras VIVAS (SEM as repetições — RV-46), avaliado pela
                // expressão do PRÓPRIO asset na mesma ordem do motor (`TryParseWithEnglishCulture` e,
                // se falhar, `Game.TryEval`), com `Target` = `Source` = o personagem em foco — é assim
                // que as 9 auras de BUFF da família leem o `ShrineEffectBonus` (`Target[...]`;
                // `status.csv:205` do Fury e irmãs: 9/9 com `AttributeEffects`, todas `Base`; Dwarven
                // não expõe efeito e Decay/Flame usam `Source`). Nada é somado por fora do efeito do asset.
                List<string> partes = new List<string>();
                HashSet<ActionStatus> somadas = new HashSet<ActionStatus>();
                HashSet<string> emFallback = new HashSet<string>(StringComparer.Ordinal);
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
                    float total = receptor[nome];
                    float contribuicao;
                    if (ContribuicaoDasAuras(unicas, atributo, receptor, somadas, out contribuicao))
                    {
                        partes.Add(TextDoEfeito(atributo, contribuicao)
                            + " (total " + TotalComSinal(nome, total) + ")");
                        // O `resto` (total − contribuição) é o pedaço da ficha que NÃO é aura: é ele que
                        // prova, em jogo, se o total é aditivo — com as duas telas do dono (30/09) o
                        // resto deu +25 (DamageMod) e +20 (DamageReduction) nos DOIS casos. RV-46: com o
                        // total no TETO do atributo (HasMax/MaxValue) o resto NÃO é comparável, e por
                        // isso o teto vai no log ao lado (`RV-46 teto ... no-teto=sim`).
                        // CHK-1 §7.2 (conserto APLICADO) — a marca ganhou `char=` e `bonus=`: sem eles a
                        // evidencia provava o valor da aura mas NAO era atribuivel a um caso (a
                        // conferencia so tinha a linha `RV-31 acumulado` como ancora). Campo de LOG.
                        Marca($"RV-44 item '{nome}': aura={ComSinal(contribuicao)}% total={ComSinal(total)}%"
                            + $" resto={ComSinal(total - contribuicao)}% char={receptor.CharacterName}"
                            + $" bonus={BonusDoReceptor(receptor)}"
                            + $" em [{string.Join(", ", NomesDasAuras(unicas).ToArray())}]");
                        MarcaTeto(atributo, receptor, nome, total);
                    }
                    else
                    {
                        // FALLBACK (RV-44): sem contribuição separável com confiança (efeito não
                        // somável — `Multiplicative`/`Set` — ou expressão não avaliada; a família de
                        // shrine NÃO tem nenhum desses casos hoje, conferido no censo: 9/9 são
                        // `Base`), o item sai com o total do personagem, como antes.
                        emFallback.Add(nome);
                        partes.Add(TextDoEfeito(atributo, total));
                        Marca($"RV-44 item '{nome}' sem separacao: sai com o total do personagem ({ComSinal(total)}%)");
                        MarcaTeto(atributo, receptor, nome, total);
                    }
                }

                // (f) RV-46 — NENHUMA AURA VIVA SAI EM SILÊNCIO (regra do dono, 30/09): a linha se chama
                // "Your active shrine auras" e se apresenta como COMPLETA. As auras cujo efeito não é
                // atributo de personagem (Dwarven = chance de stun, Decay = dano por turno, Flame = dano
                // em quem ataca) ganham item próprio com o número do asset avaliado pelo motor; o que
                // não virar item sai no LOG com o motivo.
                // DWA-2: a lista passada é a TIPADA (`porInstancia`) — aura de GATILHO entra uma vez por
                // INSTANCIA (o motor avalia o gatilho uma vez por status vivo); aura de atributo/desconhecida
                // continua entrando UMA vez (RV-46, a mesma `unicas`).
                ItensSemAtributo(porInstancia, receptor, somadas, emFallback, partes);

                if (partes.Count == 0)
                {
                    Marca($"RV-46 sem linha: {unicas.Count} aura(s) viva(s) em {receptor.CharacterName}"
                        + " sem nenhum numero provado (nada estimado)");
                    return "";
                }

                string efeito = string.Join("; ", partes.ToArray());
                // RV-30: o `bonus=` entra no log de propósito — é a ÚNICA entrada que multiplica o
                // valor da aura, e sai do ATRIBUTO do próprio personagem (ex.: perk Worship = 100),
                // nunca de uma segunda aplicação do mod. Aqui ele é o bonus de quem tem as auras, e
                // serve para o usuário conferir a origem do número. Os nomes das auras agregadas vão
                // no log para a conferência em jogo dizer QUAIS auras entraram na conta.
                // RV-46: `instancias=[...]` só sai quando a lista viva trazia a MESMA aura repetida —
                // é o campo que separa "a aura está viva" de "a aura está viva N vezes sem valor
                // próprio novo" (e o que permite ao comparador não contar a repetição como aura).
                string campoInstancias = repeticoes.Count == 0
                    ? "" : " instancias=[" + string.Join(", ", repeticoes.ToArray()) + "]";
                Marca($"RV-31 acumulado: auras=[{string.Join(", ", NomesDasAuras(unicas).ToArray())}]"
                    + campoInstancias
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
        /// sai daqui: o TOTAL sai do indexador do personagem e a CONTRIBUIÇÃO das auras, do
        /// `AttributeEffects` destas MESMAS auras (ver `AcumuladoShrines`/`ContribuicaoDasAuras`, RV-44).
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
        /// RV-46 — A MESMA AURA SÓ UMA VEZ. A lista viva (`Character.ActionStatuses`) pode conter o
        /// MESMO status várias vezes: cada (re)entrada na área do ground effect cria um status NOVO
        /// (`GroundEffect.AddGroundEffectedPlayer` -> `GameLogic.CreateActionStatus`, decompilado
        /// l.102/158) e o motor só remove quando o status é `Infinite` (l.206-213) — a aura do shrine
        /// não é. O log do jogo do dono mostra o caso: `em [Guardian Aura, Rogue Aura, Reaper Aura,
        /// Conqueror Aura, Rogue Aura, Rogue Aura]` com `aura=+120%` (3 × 40, e o `RV-44 soma` dizendo
        /// `stacks=1` em cada instância).
        ///
        /// A chave é a identidade do status como o jogo a apresenta (nome + descrição do
        /// `ActionStatusInfo`) — é o que o log e o dono veem, e o que sobrevive a uma cópia de runtime
        /// do asset. As repetições NÃO são descartadas em silêncio: voltam em `repeticoes` ("Nome xN")
        /// para o log.
        ///
        /// Falha de leitura devolve a lista como veio (melhor repetir do que esconder aura): é log,
        /// não número.
        /// </summary>
        private static List<ActionStatus> AurasUnicas(List<ActionStatus> vivas, out List<string> repeticoes)
        {
            repeticoes = new List<string>();
            List<ActionStatus> unicas = new List<ActionStatus>();
            if (vivas == null)
            {
                return unicas;
            }
            try
            {
                Dictionary<string, int> contagem = new Dictionary<string, int>(StringComparer.Ordinal);
                Dictionary<string, string> nomeDaChave = new Dictionary<string, string>(StringComparer.Ordinal);
                List<string> ordem = new List<string>();
                foreach (ActionStatus s in vivas)
                {
                    if (s == null)
                    {
                        continue;
                    }
                    string chave = ChaveDaAura(s);
                    int n;
                    if (contagem.TryGetValue(chave, out n))
                    {
                        contagem[chave] = n + 1;
                        continue;
                    }
                    contagem[chave] = 1;
                    nomeDaChave[chave] = NomeDaAura(s);
                    ordem.Add(chave);
                    unicas.Add(s);
                }
                foreach (string chave in ordem)
                {
                    if (contagem[chave] > 1)
                    {
                        repeticoes.Add(nomeDaChave[chave] + " x" + contagem[chave]);
                    }
                }
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[Shrine RV-46] desduplicacao falhou (lista devolvida como veio): {ex.GetType().Name}: {ex.Message}");
                repeticoes.Clear();
                return vivas;
            }
            return unicas;
        }

        /// <summary>RV-46 — identidade da aura na lista: nome + descrição do `ActionStatusInfo` (nunca
        /// só a referência: o jogo pode entregar uma cópia de runtime do mesmo status).</summary>
        private static string ChaveDaAura(ActionStatus s)
        {
            try
            {
                ActionStatusInfo info = s != null ? s.ActionStatusInfo : null;
                string nome = info != null ? info.Name : null;
                string descricao = info != null ? info.Description : null;
                if (string.IsNullOrEmpty(nome))
                {
                    nome = descricao;
                }
                return (nome ?? "") + "\u0001" + (descricao ?? "");
            }
            catch (Exception ex)
            {
                return "(sem chave: " + ex.GetType().Name + ")";
            }
        }

        /// <summary>
        /// DWA-2 — O TIPO DO EFEITO DA AURA. É ele (e NÃO o nome da aura) que decide se a instância
        /// repetida na lista viva conta no número exibido, porque é ele que decide o que o MOTOR faz com
        /// a repetição. Sai do ASSET do próprio status — os mesmos campos que o motor lê.
        /// </summary>
        private enum TipoDoEfeitoDaAura
        {
            /// <summary>Efeito de ATRIBUTO de personagem (`AttributeEffects` com `EffectTarget = Target`).
            /// O motor soma TODAS as instâncias (`Character.GetAttributeValueByMethod`, l.37194/37263) e
            /// CORTA no teto do atributo (`Character.GetAttribute`, l.40571-40578) — a instância extra
            /// não muda o número final e por isso entra UMA vez na linha (RV-46).</summary>
            Atributo,

            /// <summary>Efeito de GATILHO (`SkillTriggers`), sem atributo de personagem. O motor monta a
            /// lista de gatilhos um POR status vivo (`Character.SkillTriggers`, l.33489-33508), percorre
            /// TODAS as entradas (`ProcessSkillTriggers`, l.40953-40959) e rola a chance de novo em cada
            /// uma (l.41211-41216) — a repetição CONTA, e a linha conta junto (um item por instância).</summary>
            Gatilho,

            /// <summary>Nem atributo de personagem, nem gatilho: nada aqui prova o que o motor faz com a
            /// repetição. Conta UMA vez (conservador) e, sem item, o motivo sai no LOG — nunca calada.</summary>
            Outro
        }

        /// <summary>
        /// DWA-2 — o tipo do efeito pelo ASSET do status: `AttributeEffects` (com o efeito mirando o
        /// PORTADOR, `EffectTarget.Target` — o mesmo filtro do laço do motor) diz ATRIBUTO; senão,
        /// `SkillTriggers` diz GATILHO (é o campo que o motor percorre para disparar coisa). Falha de
        /// leitura cai em `Outro` (conservador: conta uma vez), nunca em exceção.
        /// </summary>
        private static TipoDoEfeitoDaAura TipoDoEfeito(ActionStatusInfo info)
        {
            if (info == null)
            {
                return TipoDoEfeitoDaAura.Outro;
            }
            try
            {
                CharacterEffectInfo[] efeitos = info.AttributeEffects;
                if (efeitos != null)
                {
                    foreach (CharacterEffectInfo efeito in efeitos)
                    {
                        if (efeito != null && efeito.CharacterAttribute != null
                            && efeito.EffectTarget == EffectTarget.Target)
                        {
                            return TipoDoEfeitoDaAura.Atributo;
                        }
                    }
                }
                if (info.SkillTriggers != null && info.SkillTriggers.Length > 0)
                {
                    return TipoDoEfeitoDaAura.Gatilho;
                }
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[Shrine DWA-2] leitura do tipo de efeito falhou: {ex.GetType().Name}: {ex.Message}");
            }
            return TipoDoEfeitoDaAura.Outro;
        }

        /// <summary>
        /// DWA-2 — a lista que alimenta os itens das auras SEM atributo de personagem, já TIPADA:
        ///
        ///   * aura de ATRIBUTO (ou de tipo desconhecido) entra UMA vez — a desdupe do RV-46, que é a
        ///     regra do `Dodge +120%`: o motor soma as instâncias e o teto corta, então a instância extra
        ///     não muda número nenhum;
        ///   * aura de GATILHO entra UMA vez POR INSTÂNCIA — o motor avalia o gatilho uma vez por status
        ///     vivo (um item por rolagem de chance). O número de cada item continua sendo o do asset:
        ///     NADA é somado à mão (duas rolagens de 40% não são 80%).
        ///
        /// `deAtributo`/`deGatilho` saem só para o LOG (quais auras caíram em cada tipo; `Nome xN` quando
        /// o gatilho tem mais de uma instância). Falha de leitura devolve a lista como veio (melhor
        /// repetir do que esconder aura).
        /// </summary>
        private static List<ActionStatus> AurasQueContamPorInstancia(List<ActionStatus> vivas,
            out List<string> deAtributo, out List<string> deGatilho)
        {
            deAtributo = new List<string>();
            deGatilho = new List<string>();
            List<ActionStatus> itens = new List<ActionStatus>();
            if (vivas == null)
            {
                return itens;
            }
            try
            {
                Dictionary<string, int> contagem = new Dictionary<string, int>(StringComparer.Ordinal);
                Dictionary<string, ActionStatus> primeira = new Dictionary<string, ActionStatus>(StringComparer.Ordinal);
                Dictionary<string, TipoDoEfeitoDaAura> tipoDaChave = new Dictionary<string, TipoDoEfeitoDaAura>(StringComparer.Ordinal);
                List<string> ordem = new List<string>();
                foreach (ActionStatus s in vivas)
                {
                    if (s == null || s.ActionStatusInfo == null)
                    {
                        continue;
                    }
                    TipoDoEfeitoDaAura tipo = TipoDoEfeito(s.ActionStatusInfo);
                    string chave = ChaveDaAura(s);
                    int n;
                    if (!contagem.TryGetValue(chave, out n))
                    {
                        contagem[chave] = 1;
                        ordem.Add(chave);
                        primeira[chave] = s;
                        tipoDaChave[chave] = tipo;
                        // Primeira instância: entra sempre (é o item da aura) — e é aqui que o TIPO é
                        // registrado no log.
                        itens.Add(s);
                        string nome = NomeDaAura(s);
                        if (tipo == TipoDoEfeitoDaAura.Gatilho)
                        {
                            Marca($"DWA-2 '{nome}': efeito de GATILHO (o motor avalia uma vez por status"
                                + " vivo; a repetição conta) — TotalStacks nao multiplica chance");
                        }
                        else
                        {
                            deAtributo.Add(nome);
                            if (tipo == TipoDoEfeitoDaAura.Outro)
                            {
                                Marca($"DWA-2 '{nome}': efeito nem atributo de personagem nem gatilho"
                                    + " — conta UMA vez (nada prova o que o motor faz com a repetição)");
                            }
                        }
                        continue;
                    }
                    contagem[chave] = n + 1;
                    if (tipo == TipoDoEfeitoDaAura.Gatilho)
                    {
                        // O motor NÃO corta a repetição de gatilho: a instância extra entra na linha.
                        itens.Add(s);
                    }
                }
                foreach (string chave in ordem)
                {
                    if (contagem[chave] > 1 && tipoDaChave[chave] == TipoDoEfeitoDaAura.Gatilho)
                    {
                        deGatilho.Add(NomeDaAura(primeira[chave]) + " x" + contagem[chave]);
                    }
                }
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[Shrine DWA-2] separacao por tipo de efeito falhou (lista devolvida como veio): {ex.GetType().Name}: {ex.Message}");
                deAtributo.Clear();
                deGatilho.Clear();
                return vivas;
            }
            return itens;
        }

        /// <summary>
        /// RV-46 — o TETO do atributo, quando o asset define um (`CharacterAttribute.HasMax`), e o
        /// registro de que o total está batendo nele. O motor corta o valor no teto
        /// (`Character.GetAttribute`, decompilado l.11871-11878) — então, com o total no teto, o
        /// `resto` do item (`total − contribuição`) NÃO é "a parte da ficha que não é aura" e não pode
        /// ser comparado entre hovers. O teto vai no log para quem confere saber; NENHUM texto muda por
        /// causa dele (o número exibido continua o do motor).
        /// </summary>
        private static void MarcaTeto(CharacterAttribute atributo, Character receptor, string nome, float total)
        {
            try
            {
                float teto;
                if (!TetoDoAtributo(atributo, receptor, out teto))
                {
                    return;
                }
                Marca($"RV-46 teto '{nome}': MaxValue={teto.ToString("0.#")} char={receptor.CharacterName}"
                    + $" total={ComSinal(total)}% no-teto={(total >= teto ? "sim" : "nao")}"
                    + " (HasMax do atributo no asset: acima disso o motor corta — Character.cs:11871-11878)");
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[Shrine RV-46] leitura do teto falhou (nenhum campo extra no log): {ex.GetType().Name}: {ex.Message}");
            }
        }

        /// <summary>RV-46 — o teto do atributo pelo PRÓPRIO objeto do jogo (`HasMax`/`MaxValue`, ou o
        /// atributo apontado por `UseMaxAttribute`). `false` = atributo sem teto neste build.</summary>
        private static bool TetoDoAtributo(CharacterAttribute atributo, Character receptor, out float teto)
        {
            teto = 0f;
            if (atributo == null || !atributo.HasMax)
            {
                return false;
            }
            if (atributo.UseMaxAttribute)
            {
                CharacterAttribute outro = atributo.MaxAttribute;
                if (outro == null || receptor == null || string.IsNullOrEmpty(outro.name))
                {
                    return false;
                }
                teto = receptor[outro.name];
                return true;
            }
            teto = atributo.MaxValue;
            return true;
        }

        /// <summary>
        /// RV-46 — O ITEM DE UMA AURA VIVA QUE NÃO MEXE EM ATRIBUTO DE PERSONAGEM. A linha se chama
        /// "Your active shrine auras" e se apresenta como COMPLETA (regra do dono, 30/09): nenhuma aura
        /// viva pode sair em silêncio. São TRÊS das 12 (censo: as outras 9 têm `AttributeEffects`):
        ///
        ///   - `Dwarven Aura` — o efeito é a CHANCE do gatilho (`OnHittingDamaging` -> `Stunned`):
        ///     `ActionStatusInfo.SkillTriggers[].ActionStatusChanceEquations` (asset @1517115647, a
        ///     MESMA string da `DescriptionExpressions[0]` @1517115395). Item: `Stun chance +40%`.
        ///   - `Decay Shrine Aura` — dano por turno (`OnTurnStart`): a MESMA fórmula que a linha do
        ///     próprio Decay usa (RV-33/RV-34), avaliada com `Source` = `Target` = o personagem em
        ///     foco. Item: `Shadow damage per turn 23`.
        ///   - `Flame Shrine Aura` — dano em QUEM ATACA (`OnGettingHitDamaging`), que o hover não
        ///     conhece: um número por ALVO na área, o mesmo cru da linha do próprio Flame (RV-34).
        ///     Item: `Fire damage to attackers: <alvo> <dano>, ...`; sem alvo com o status vivo, o
        ///     número não existe (mesma regra do RV-33) e a aura sai no LOG.
        ///
        /// DWA-2 — a lista recebida é a TIPADA (`AurasQueContamPorInstancia`): aura de GATILHO chega
        /// aqui uma vez POR INSTÂNCIA (o motor avalia o gatilho uma vez por status vivo), então os TRÊS
        /// itens acima podem sair repetidos quando há mais de um shrine no alcance — cada linha é uma
        /// rolagem/um proc de verdade. Aura de atributo/desconhecida chega uma vez só (RV-46).
        ///
        /// Quem decide a etiqueta é `RotuloSemAtributo` (tabela pelo texto EXATO do asset, o mesmo
        /// `ShrineKeys` que define a família) — nenhum nome inventado no meio do código. Valor nunca é
        /// estimado: sem expressão avaliada, o item não sai e o LOG diz por quê.
        /// </summary>
        private static void ItensSemAtributo(List<ActionStatus> unicas, Character receptor,
            HashSet<ActionStatus> somadas, HashSet<string> emFallback, List<string> partes)
        {
            if (unicas == null || receptor == null || partes == null)
            {
                return;
            }
            foreach (ActionStatus s in unicas)
            {
                try
                {
                    if (s == null || s.ActionStatusInfo == null)
                    {
                        continue;
                    }
                    if (TemItemNaLinha(s, somadas, emFallback))
                    {
                        continue;
                    }
                    string nome = NomeDaAura(s);
                    string motivo;
                    string item = ItemDaAuraSemAtributo(s, receptor, out motivo);
                    if (item != null)
                    {
                        partes.Add(item);
                        Marca($"RV-46 item sem atributo: '{nome}' -> '{item}'"
                            + $" char={receptor.CharacterName} bonus={BonusDoReceptor(receptor)}");
                    }
                    else
                    {
                        // REGRA (dono, 30/09): a lista se apresenta como completa — se não deu para
                        // representar, o motivo fica no log. Nunca sumir calada.
                        Marca($"RV-46 AVISO: a aura viva '{nome}' NAO virou item da linha ({motivo})"
                            + " — a lista esta incompleta e isto esta registrado; nenhum numero foi estimado");
                    }
                }
                catch (Exception ex)
                {
                    Plugin.Log.LogWarning($"[Shrine RV-46] item sem atributo falhou (nada entra na linha): {ex.GetType().Name}: {ex.Message}");
                }
            }
        }

        /// <summary>RV-46 — esta aura já está representada na linha? Sim quando ela ENTROU na soma de
        /// algum item de atributo (`somadas`) ou quando o item do atributo dela saiu no fallback com o
        /// TOTAL do personagem (`emFallback`): nos dois casos o efeito dela aparece na linha.</summary>
        private static bool TemItemNaLinha(ActionStatus s, HashSet<ActionStatus> somadas, HashSet<string> emFallback)
        {
            if (s == null || s.ActionStatusInfo == null)
            {
                return false;
            }
            if (somadas != null && somadas.Contains(s))
            {
                return true;
            }
            CharacterEffectInfo[] efeitos = s.ActionStatusInfo.AttributeEffects;
            if (efeitos == null || emFallback == null)
            {
                return false;
            }
            foreach (CharacterEffectInfo e in efeitos)
            {
                if (e != null && e.CharacterAttribute != null && emFallback.Contains(e.CharacterAttribute.name))
                {
                    return true;
                }
            }
            return false;
        }

        /// <summary>
        /// RV-46 — o item (texto final) de uma aura sem atributo de personagem, ou `null` + `motivo`.
        /// Só as três auras de efeito sem atributo têm etiqueta; qualquer outra aura viva que chegue
        /// aqui devolve `null` com motivo — o LOG registra (regra da lista completa).
        /// </summary>
        private static string ItemDaAuraSemAtributo(ActionStatus aura, Character receptor, out string motivo)
        {
            motivo = null;
            ActionStatusInfo info = aura.ActionStatusInfo;
            string chave = info.Description;
            string rotulo = RotuloSemAtributo(chave);
            if (rotulo == null)
            {
                motivo = "efeito sem atributo de personagem e sem etiqueta conhecida (descricao '"
                    + (chave ?? "(nula)") + "')";
                return null;
            }

            // (1) DECAY — dano por turno do personagem em foco, a MESMA fórmula da linha do Decay
            // (RV-34), sem o `Mathf.Max(1,` (o Decay pode dar 0). `Source` = `Target` = o personagem.
            if (string.Equals(chave, ChaveDecay, StringComparison.Ordinal))
            {
                if (receptor.MaxHealth <= 0f)
                {
                    motivo = "receptor sem MaxHealth";
                    return null;
                }
                float dano;
                if (!ValorDaExpressao(FormulaDoDano(FormulaDanoDecay, FormulaDanoDecaySemBonus), receptor, receptor, out dano))
                {
                    motivo = "formula do Decay nao avaliada pelo interpretador do motor";
                    return null;
                }
                Marca($"RV-46 item do Decay: MaxHealth={receptor.MaxHealth.ToString("0.#")}"
                    + $" bonus={BonusDoReceptor(receptor)} dano={dano.ToString("0.#")}"
                    + $" tipo={TipoDoAlvo(receptor)}");
                return rotulo + " " + dano.ToString("0.#");
            }

            // (2) FLAME — um número por ALVO na área (o mesmo número cru da linha do próprio Flame,
            // RV-33/RV-34). O hover não sabe quem vai atacar, então não existe UM número.
            if (string.Equals(chave, ChaveFlame, StringComparison.Ordinal))
            {
                List<Character> alvos = AlvosNaAreaDoFlame();
                List<string> valores = new List<string>();
                foreach (Character alvo in alvos)
                {
                    if (alvo == null || alvo.MaxHealth <= 0f)
                    {
                        continue;
                    }
                    float dano;
                    if (!ValorDaExpressao(FormulaDoDano(FormulaDanoFlameCru, FormulaDanoFlameSemBonus), alvo, alvo, out dano))
                    {
                        continue;
                    }
                    string nomeAlvo = string.IsNullOrEmpty(alvo.CharacterName) ? "(sem nome)" : alvo.CharacterName;
                    valores.Add(nomeAlvo + " " + dano.ToString("0.#"));
                    Marca($"RV-46 item do Flame alvo '{nomeAlvo}': MaxHealth={alvo.MaxHealth.ToString("0.#")}"
                        + $" tipo={TipoDoAlvo(alvo)} bonus={BonusDoReceptor(alvo)} dano={dano.ToString("0.#")}");
                }
                if (valores.Count == 0)
                {
                    motivo = "nenhum alvo com o status do Flame vivo agora (o dano e de quem ataca:"
                        + " sem atacante, sem numero)";
                    return null;
                }
                // Separador `, ` (e não `; `): o `; ` separa os ITENS da linha azul — o comparador
                // mecanico corta a linha por ele e um `; ` dentro do item do Flame o quebraria em dois.
                return rotulo + ": " + string.Join(", ", valores.ToArray());
            }

            // (3) DWARVEN — chance de stun. A expressão é a do GATILHO do status (`Stunned`), avaliada
            // pelo motor com `Target` = o personagem em foco (a convenção de TODA a família: as
            // expressões das 12 auras leem `Target["ShrineEffectBonus"]`); no asset ela é a MESMA
            // string da `DescriptionExpressions[0]`, que é o número da linha branca do shrine.
            if (string.Equals(chave, ChaveDwarven, StringComparison.Ordinal))
            {
                string expressao = ExpressaoDeChance(info);
                float chance;
                if (!string.IsNullOrEmpty(expressao)
                    && ValorDaExpressao(expressao, receptor, receptor, out chance))
                {
                    Marca($"RV-46 item do Dwarven: chance do gatilho '{expressao}' = {chance.ToString("0.#")}"
                        + $" char={receptor.CharacterName} bonus={BonusDoReceptor(receptor)}");
                    return rotulo + " " + ComSinal(chance) + "%";
                }
                // Reserva: a `DescriptionExpressions` do próprio status (o `[0]` da linha branca).
                string[] exprs = info.DescriptionExpressions;
                if (exprs != null && exprs.Length > 0
                    && ValorDaExpressao(exprs[0], receptor, receptor, out chance))
                {
                    Marca($"RV-46 item do Dwarven (descricao): '{exprs[0]}' = {chance.ToString("0.#")}"
                        + $" char={receptor.CharacterName} bonus={BonusDoReceptor(receptor)}");
                    return rotulo + " " + ComSinal(chance) + "%";
                }
                motivo = "sem expressao de chance avaliada (gatilho: '" + (expressao ?? "nenhum")
                    + "'; descricao: '" + (exprs != null && exprs.Length > 0 ? exprs[0] : "nenhuma") + "')";
                return null;
            }

            motivo = "efeito sem atributo de personagem sem item implementado nesta versao";
            return null;
        }

        /// <summary>
        /// RV-46 — a etiqueta do item de uma aura cujo efeito NÃO é atributo de personagem. É uma
        /// TABELA DE NOME (nunca de número): o valor de cada uma sai do asset, avaliado pelo motor. A
        /// chave é o texto EXATO da descrição do status — o mesmo critério que define a família
        /// (`ShrineKeys`). `null` = aura desconhecida: quem chamou loga o motivo e não inventa item.
        /// </summary>
        private static string RotuloSemAtributo(string chaveDaAura)
        {
            if (string.Equals(chaveDaAura, ChaveDwarven, StringComparison.Ordinal))
            {
                return "Stun chance";
            }
            if (string.Equals(chaveDaAura, ChaveDecay, StringComparison.Ordinal))
            {
                return "Shadow damage per turn";
            }
            if (string.Equals(chaveDaAura, ChaveFlame, StringComparison.Ordinal))
            {
                return "Fire damage to attackers";
            }
            return null;
        }

        /// <summary>
        /// RV-46 — a expressão de CHANCE do status: o gatilho que aplica um status com
        /// `ActionStatusChanceEquations` (o Dwarven aplica `Stunned`). É o campo que o motor avalia
        /// (`Game.Eval&lt;float&gt;(trigger.ActionStatusChanceEquations[i], ...)`, decompilado
        /// l.12492/12511) — o índice casa com `ActionStatuses[i]` do MESMO gatilho. `null` = status sem
        /// gatilho com chance (o caminho do Decay/Flame, cujo valor não é chance).
        /// </summary>
        private static string ExpressaoDeChance(ActionStatusInfo info)
        {
            if (info == null || info.SkillTriggers == null)
            {
                return null;
            }
            foreach (SkillTrigger gatilho in info.SkillTriggers)
            {
                if (gatilho == null || gatilho.ActionStatuses == null || gatilho.ActionStatusChanceEquations == null)
                {
                    continue;
                }
                int n = Math.Min(gatilho.ActionStatuses.Length, gatilho.ActionStatusChanceEquations.Length);
                for (int i = 0; i < n; i++)
                {
                    if (gatilho.ActionStatuses[i] != null
                        && !string.IsNullOrEmpty(gatilho.ActionStatusChanceEquations[i]))
                    {
                        return gatilho.ActionStatusChanceEquations[i];
                    }
                }
            }
            return null;
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

        /// <summary>
        /// RV-44 — A CONTRIBUIÇÃO DAS AURAS em UM atributo: a soma, aura por aura, do `AttributeEffects`
        /// REAL de cada aura VIVA (nunca o total do personagem). É o número que o tooltip do shrine, o
        /// de cada aura, mostra: a expressão do asset (`Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"]
        /// / 100)))` e irmãs; ver `status.csv:205` para o Fury) avaliada pelo PRÓPRIO motor — a mesma
        /// ordem de `Character.GetAttributeWalk` (decompilado l.37256-37263: `TryParseWithEnglishCulture`
        /// e, se falhar, `Game.TryEval` com `Source`/`Target`/`StatusLevel` do status).
        ///
        /// POR QUE NÃO SOMAR O TOTAL DO PERSONAGEM: o defeito relatado (30/09, print do dono) é que a
        /// linha se chama "Your active shrine auras" e mostrava aura + skill + equipamento num número
        /// só — indistinguível de "a aura dá 50%" quando a aura dá 25%. Aqui entra o que a aura dá; o
        /// total vai no parênteses (é o mesmo número da ficha).
        ///
        /// REGRAS DA SOMA (todas tiradas do motor, nenhuma inventada):
        ///   - `EffectTarget` tem de ser `Target` — o laço de `ActionStatuses` do motor descarta
        ///     `EffectTarget.Source` (decompilado l.37207-37210); um efeito assim não entra no total do
        ///     portador e também não entra aqui (só é logado).
        ///   - `Base`/`Additive`/`Percentage` SOMAM (`val = val + parsed2`, l.37263-37271); é o bucket
        ///     aditivo do motor.
        ///   - `Multiplicative` e `Set` NÃO são somáveis (multiplicam/substituem): qualquer um deles num
        ///     atributo devolve `false` e o item sai no fallback, com o total do personagem (a família
        ///     de shrine não tem nenhum caso hoje — censo: as 9 que têm `AttributeEffects` são todas `Base`).
        ///   - `TotalStacks` multiplica o valor (l.37263), como no motor; um status vivo tem no mínimo 1.
        ///   - **DUAS AURAS NO MESMO ATRIBUTO SOMAM** (o caso do print: Warrior + Fury em `DamageMod`, e
        ///     o próprio Fury em `DamageMod` e `DamageReduction`): o item continua sendo UM por atributo
        ///     e o valor é a soma das contribuições — não o total do personagem.
        ///
        /// `false` = não há contribuição separável com confiança (nenhum efeito somável, efeito não
        /// somável ou expressão não avaliada): quem chamou usa o total rotulado. Nunca estima.
        ///
        /// RV-46 — a lista recebida é a DESDUPLICADA (`AurasUnicas`): cada aura entra UMA vez. A aura
        /// viva repetida na lista do personagem (mesmo status aplicado de novo ao (re)entrar na área)
        /// não é uma segunda aura, é a mesma — e contá-la duas vezes foi o `Dodge +120%` do print do
        /// dono (a aura vale 40, e 40 é o que a linha branca do shrine mostra). `somadas` recebe as
        /// auras que ENTRARAM na soma deste atributo: é o que `ItensSemAtributo` usa para saber quais
        /// auras já estão representadas na linha (RV-46, regra da lista completa).
        /// </summary>
        private static bool ContribuicaoDasAuras(List<ActionStatus> auras, CharacterAttribute atributo,
            Character receptor, HashSet<ActionStatus> somadas, out float contribuicao)
        {
            contribuicao = 0f;
            if (auras == null || atributo == null || receptor == null)
            {
                return false;
            }
            string nome = atributo.name;
            bool somou = false;
            foreach (ActionStatus s in auras)
            {
                CharacterEffectInfo[] efeitos = s != null && s.ActionStatusInfo != null
                    ? s.ActionStatusInfo.AttributeEffects
                    : null;
                if (efeitos == null)
                {
                    continue;
                }
                // Status vivo = no mínimo 1 stack (o motor multiplica por `TotalStacks`).
                int stacks = s.TotalStacks > 1 ? s.TotalStacks : 1;
                foreach (CharacterEffectInfo efeito in efeitos)
                {
                    if (efeito == null || efeito.CharacterAttribute == null)
                    {
                        continue;
                    }
                    if (!string.Equals(efeito.CharacterAttribute.name, nome, StringComparison.Ordinal))
                    {
                        continue;
                    }
                    if (efeito.EffectTarget != EffectTarget.Target)
                    {
                        Marca($"RV-44 '{nome}': efeito de '{NomeDaAura(s)}' mira {efeito.EffectTarget}"
                            + " (nao entra no total do portador) — fora da contribuicao");
                        continue;
                    }
                    if (efeito.CharacterEffectMethod == CharacterEffectMethod.Multiplicative
                        || efeito.CharacterEffectMethod == CharacterEffectMethod.Set)
                    {
                        Marca($"RV-44 '{nome}': efeito {efeito.CharacterEffectMethod} em '{NomeDaAura(s)}'"
                            + " nao e somavel — item sai com o TOTAL do personagem");
                        return false;
                    }
                    float valor;
                    if (!ValorDaExpressao(efeito.Amount, receptor, receptor, out valor))
                    {
                        Marca($"RV-44 '{nome}': expressao '{efeito.Amount}' de '{NomeDaAura(s)}'"
                            + " nao avaliada — item sai com o TOTAL do personagem");
                        return false;
                    }
                    contribuicao += valor * stacks;
                    if (somadas != null)
                    {
                        somadas.Add(s);
                    }
                    somou = true;
                    // CHK-1 §7.2 (conserto APLICADO) — `char=` e `bonus=` na marca: e ela que nomeia a
                    // aura E o atributo, entao com os dois campos a evidencia fica atribuivel a um caso
                    // isolado (sem depender da ancora `RV-31 acumulado`). Campo de LOG.
                    Marca($"RV-44 soma '{nome}': '{NomeDaAura(s)}' {efeito.CharacterEffectMethod}"
                        + $" {ComSinal(valor * stacks)}% (stacks={stacks})"
                        + $" char={receptor.CharacterName} bonus={BonusDoReceptor(receptor)}");
                }
            }
            return somou;
        }

        /// <summary>Nome do status da aura, só para o log (identifica QUEM entrou na soma).</summary>
        private static string NomeDaAura(ActionStatus s)
        {
            try
            {
                if (s != null && s.ActionStatusInfo != null && !string.IsNullOrEmpty(s.ActionStatusInfo.Name))
                {
                    return s.ActionStatusInfo.Name;
                }
            }
            catch (Exception ex)
            {
                return "(" + ex.GetType().Name + ")";
            }
            return "(sem nome)";
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

        /// <summary>RV-30/RV-34 — o `ShrineEffectBonus` REAL do personagem passado, só para o log (a única
        /// entrada que multiplica o valor da aura). Serve ao receptor do agregado e a cada ALVO do Flame.
        /// Nunca entra no texto; o número mostrado é o que a expressão do jogo devolve. Chamado só depois
        /// do guard `GetAttribute("ShrineEffectBonus") != null` (o indexador lança para nome desconhecido).</summary>
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
        ///
        /// RV-34 — `gameSource` é QUEM o fator `Source["ShrineEffectBonus"]` lê, e `gameTarget` é quem
        /// tem a vida máxima/percentual lidos. Nas DUAS auras de perigo os dois são o MESMO personagem
        /// avaliado (medido em jogo: com `Worship` o dano dobra), então quem chama passa o personagem
        /// nas duas posições. Antes desta revisão o `Source` era o `Root.WorldCharacter` (o personagem
        /// VAZIO do shrine) — era isso que fazia o fator valer 1 e o número sair na base.
        /// </summary>
        private static bool ValorDaExpressao(string expressao, Character gameTarget, Character gameSource, out float valor)
        {
            valor = 0f;
            if (string.IsNullOrEmpty(expressao))
            {
                return false;
            }
            GameFunctionParameters parametros = new GameFunctionParameters
            {
                Source = gameSource,
                Target = gameTarget
            };
            // Expressão que lê `Source[...]` precisa do personagem: sem ele, melhor não mostrar número
            // nenhum do que mostrar um número mentiroso.
            if (parametros.Source == null && expressao.IndexOf("Source[", StringComparison.Ordinal) >= 0)
            {
                return false;
            }
            if (Burst2Flame.Game.TryParseWithEnglishCulture(expressao, out valor))
            {
                return true;
            }
            // RV-34: o aviso `No Compiled Expression` é de CACHE do build (não de falha) e sairia uma vez
            // por constante nossa; registrado antes da primeira avaliação, ele não sai. O valor e o
            // caminho de compilação não mudam (ver o cabeçalho desta classe).
            RegistrarNoCacheDoJogo();
            return Burst2Flame.Game.TryEval<float>(expressao, parametros, out valor);
        }

        /// <summary>RV-34 — pré-registra as NOSSAS expressões na lista de avisos de cache do jogo.
        ///
        /// `CompiledDynamicExpresso.MissingExpressions` (campo privado estático, l.49969) é lido em UM
        /// lugar só: o guard que imprime `No Compiled Expression` (l.49980 para valor, l.50006 para void).
        /// Pôr ali as strings que nós avaliamos não muda NADA no valor (o cache que resolve é o outro,
        /// `CompiledExpressions`) — só impede o `Debug.LogError` de uma linha por constante num log que o
        /// usuário lê, já que é o mod que chega primeiro nessas expressões.
        ///
        /// Campo ausente/renomeado (build novo do jogo): a reflexão falha, nada é suprimido e o aviso
        /// volta exatamente como era — nenhuma exceção sai daqui.</summary>
        private static void RegistrarNoCacheDoJogo()
        {
            if (_avisosDeCacheRegistrados)
            {
                return;
            }
            _avisosDeCacheRegistrados = true;
            try
            {
                // O tipo é do namespace GLOBAL no assembly do jogo (conferido: `ilspycmd -t
                // CompiledDynamicExpresso`); o nome com prefixo fica como segunda tentativa.
                Type tipo = typeof(Burst2Flame.Game).Assembly.GetType("CompiledDynamicExpresso")
                    ?? typeof(Burst2Flame.Game).Assembly.GetType("Burst2Flame.CompiledDynamicExpresso");
                FieldInfo campo = tipo?.GetField("MissingExpressions", BindingFlags.Static | BindingFlags.NonPublic);
                HashSet<string> avisos = campo?.GetValue(null) as HashSet<string>;
                if (avisos == null)
                {
                    Marca("RV-34 aviso de cache: MissingExpressions nao acessivel neste build"
                        + " — o aviso 'No Compiled Expression' volta (nada mais muda)");
                    return;
                }
                string[] nossas = { FormulaDanoFlameCru, FormulaDanoFlameSemBonus, FormulaDanoDecay, FormulaDanoDecaySemBonus, PorcentagemDoDecay };
                int registradas = 0;
                foreach (string expressao in nossas)
                {
                    if (avisos.Add(expressao))
                    {
                        registradas++;
                    }
                }
                Marca($"RV-34 aviso de cache: {registradas}/{nossas.Length} formula(s) nossa(s) fora da lista"
                    + " — sem 'No Compiled Expression' para elas (o valor vem do interpretador do mesmo jeito)");
            }
            catch (Exception ex)
            {
                Plugin.Log.LogWarning($"[Shrine RV-34] registro no cache de avisos falhou (aviso do jogo volta): {ex.GetType().Name}: {ex.Message}");
            }
        }

        /// <summary>RV-34 — as constantes já registradas (o registro roda uma vez por sessão).</summary>
        private static bool _avisosDeCacheRegistrados;

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
            // RV-45: mesma convenção inteira da ficha (não é só o crit: QUALQUER atributo que o
            // equipamento deixe quebrado sai inteiro, como o rótulo conhecido acima).
            int n = InteiroDoJogo(v);
            return rotulo + " " + (n >= 0 ? "+" : "−") + Mathf.Abs(n) + "%";
        }
    }
}
