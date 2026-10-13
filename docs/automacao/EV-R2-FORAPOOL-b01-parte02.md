# EV-R2-FORAPOOL-b01 — parte 02: eventos 8–14

Status: PROPOSTAS PARA APROVAÇÃO DO DONO; não implementadas. Fonte da ordem: `C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-NotInEventPool-v2.md`, seções 8–14. Dados, schema e catálogo: `eventos.json`, `eventos.schema.json`, `schema.md`, `catalogo-referencias.json` em `C:/dev/stolen-realm/docs/cobertura/EV-R1/`. Aplicam-se as regras da parte01: TRECHO = substituir só o trecho literal; CAMPO = string completa; opções/ações base 1. Demais bytes, tags, placeholders e dados mecânicos ficam inalterados.

NULL final = NAO_EXERCITADO, não zero. Ouro/XP exigem estado da partida; loot exige nível/restrições/RNG; aplicação de status/efeitos, alvo e disponibilidade exigem runtime; PPtr=0 indica referência nula configurada. Os caminhos e motivos por evento são inventariados na parte04. Não escolher FullReleaseMode nem confundir projeção redundante de recompensas com prêmio adicional.

## Inventário parcial — 7 eventos

| Nº | Chave | Título / variante | Categoria | Raridade (valor) | Peso relativo | Veredito proposto | Natureza |
|---|---|---|---|---|---|---|---|
| 8 | resources.assets:2545561 | Cursed Chest / Victory | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 9 | resources.assets:2545564 | Cursed Mimic / Victory | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 10 | resources.assets:2545566 | Cursed Tome / Victory 1 | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 11 | resources.assets:2545567 | Cursed Tome / Victory 2 | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 12 | resources.assets:2545568 | Cursed Tome / Victory 3 | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 13 | resources.assets:2545571 | Dark Discoveries / Victory | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 14 | resources.assets:2545574 | Desecrated Statue of the First Mountain King / Victory | NotInEventPool | Mythic (4) | 1.0 | MELHORAR | wording |

## 08 — Cursed Chest — resources.assets:2545561

VEREDITO PROPOSTO: MELHORAR — wording. Manter loot e restrições de raridade; não prometer um item específico.

Campo `texto`, TRECHO atual: `now free from its macabre prison of decay, lays before you.`
PROPOSTA EXATA: `now free from its macabre prison of decay, lies before you.`
Campo original `campos_originais.promptToSelectCharacter`, CAMPO atual: `Does anyone owe this Ogre money?`
PROPOSTA EXATA: `Who will claim the chest's treasure?`
Justificativa: lie/lay e prompt herdado de um Ogre ausente da cena. Não alterar o título nem fingir que a pergunta foi exibida na UI.

Anomalias/limites: `disabled=0`; 1 opção, descrição vazia, ação vazia e resultado global vazio, sem ocultação configurada. Itens dar=true, pool Unassigned, quantidade_configurada=1, sem tabela inline, limitItemRarities=1/possibleRarities=[2,3]. possibleItemTypes=[0,0] com limitItemTypes=0 é resíduo inativo, não motivo para inventar restrição. Batalha da ação não inicia; referência e encadeamento nulos por PPtr=0. Entrada de `resources.assets:2545562` em 2 ações de vitória e de `resources.assets:2544645` (BattleInfo.victoryEvent). NAO_EXERCITADO: item sorteado, quantidade efetiva, disponibilidade e UI.

## 09 — Cursed Mimic — resources.assets:2545564

VEREDITO PROPOSTO: MELHORAR — wording. Manter as 3 escolhas de Fortune e seus valores dinâmicos.

Campo `texto`, TRECHO atual: `The taint dissolved, fading away into smoke and shadow, leaving behind an empty silence.`
PROPOSTA EXATA: `The taint dissolves, fading away into smoke and shadow, leaving behind an empty silence.`
Campo opção 2, ação 1 `texto`, CAMPO atual: `As you take the Frozen Heart it's numbing cold begins to feel... comfortable.`
PROPOSTA EXATA: `As you take the Frozen Heart, its numbing cold begins to feel... comfortable.`
Campo original `campos_originais.promptToSelectCharacter`, CAMPO atual: `Does anyone owe this Ogre money?`
PROPOSTA EXATA: `Who will claim the mimic's treasure?`
Justificativa: continuidade no presente, possessivo its e prompt compatível. Não substituir `[0]`, `{10,250}`, `{100, 200}` ou fórmulas das Fortunes por valores finais.

Anomalias/limites: `disabled=0`; 3 opções sem ocultação configurada. Cada ação tem candidato fixo distinto: Emblem of the Iron Fortress (`resources.assets:2545433`), Frozen Lich Heart (`resources.assets:2545442`), Ball Lightning (`resources.assets:2545409`), todos Fortune/Permanent. “Tesouro” narrativo não é prova de dar itens: itens.dar=false nos 3 efeitos; são status configurados. Referências de batalha/encadeamento nulas, batalhas inativas. Entrada `resources.assets:2545565`. NAO_EXERCITADO: destino dos status, escalas finais e texto de prompt efetivo (targetType=3 serializado).

## 10 — Cursed Tome (Victory 1) — resources.assets:2545566

VEREDITO PROPOSTO: MELHORAR — wording. Manter a escalada da sequência e a saída existente, sem adicionar recompensa intermediária.

Campo opção 1 `texto`, CAMPO atual: `Continue to read from the <incr><indigo><b>Cursed Tome</b></indigo></incr>.`
PROPOSTA EXATA: `Continue to read from the <incr><indigo><b>Cursed Tome</b></indigo></incr> and face another battle.`
Justificativa: Read on tem batalha.iniciar=true e vitória encaminha à etapa seguinte; antecipar o confronto torna a escolha transparente, sem prometer poder imediato. Não mudar tags nem condições.

Anomalias/limites: `disabled=0`; 2 opções sem ocultação configurada; resultado global vazio. Read on inicia batalha com PPtr de referência NULL e ForcedEnemies=[], mas tem VictoryEvent `resources.assets:2545567`. Sem inimigos forçados não significa zero inimigos: o combate pode ser resolvido pelo runtime. Leave tem batalha.iniciar=false e sem candidatos de status no efeito padrão. Entrada `resources.assets:2545569`. Disponibilidade, composição de inimigos, loot/XP de luta e avanço efetivo NAO_EXERCITADO; não preencher esses NULL.

## 11 — Cursed Tome (Victory 2) — resources.assets:2545567

VEREDITO PROPOSTO: MELHORAR — wording. Preservar o CR do texto principal e a diferença entre tags `<indigo>` e `<mythic>` existente em campos distintos.

Campo opção 1 `texto`, CAMPO atual: `Finish what you've started. ` (inclui espaço final).
PROPOSTA EXATA: `Finish what you've started and face the undead champions.`
Campo opção 1, ação 1 `texto`, TRECHO atual: `a power that transcendes the mortal realm.`
PROPOSTA EXATA: `a power that transcends the mortal realm.`
Justificativa: esclarecer a luta final e corrigir erro ortográfico. A batalha configura Evil Caster, Evil Warrior, Evil Rogue; não prometer recompensa antes de vencê-los.

Anomalias/limites: `disabled=0`; 2 opções sem ocultação; resultado global vazio; texto principal contém CR literal, que não será normalizado. Read on tem PPtr de batalha NULL, iniciar=true, 3 inimigos forçados e VictoryEvent `resources.assets:2545568`; não são referências ausentes aos inimigos. Leave inicia=false. Entrada `resources.assets:2545566`. NAO_EXERCITADO: combate, aplicação de EnemyMods, recompensas finais e renderização de CR/tags.

## 12 — Cursed Tome (Victory 3) — resources.assets:2545568

VEREDITO PROPOSTO: MELHORAR — wording. Manter Necronomicon, tag colors e o token `[o1a1_status]`.

Campo `texto`, TRECHO atual: `Your valor and cunning prevaile over the darkness you had summoned.`
PROPOSTA EXATA: `Your valor and cunning prevail over the darkness you had summoned.`
Campo original `campos_originais.promptToSelectCharacter`, CAMPO atual: `Who will take the <indigo><b><incr>Necronomicon</indigo></b></incr> and gain [o1a1_status]?`
PROPOSTA EXATA: `Who will take the <indigo><b><incr>Necronomicon</incr></b></indigo> and gain [o1a1_status]?`
Justificativa: erro ortográfico e fechamento de tags fora da ordem inversa da abertura. O token permanece literal; não resolvê-lo manualmente.

Anomalias/limites: `disabled=0`; 1 opção sem ocultação; resultado global vazio. Necronomicon (`resources.assets:2545457`) é Fortune/Permanent com modificadores `{5,25}` para SummonDamageMod/SummonHealthMod. A descrição dessa referência também tem `<i><color...>...</i></color>` fora de ordem; sinalizar, mas edição desse EventStatus compartilhado está fora da proposta deste PartyEvent. A ação guarda 3 inimigos forçados residuais, porém iniciar=false. Não remover tais campos nem anunciar novo combate. Entrada `resources.assets:2545567`; NAO_EXERCITADO: Fortune efetiva, token e markup na UI.

## 13 — Dark Discoveries — resources.assets:2545571

VEREDITO PROPOSTO: MELHORAR — wording. Não renomear a Fortune nem inventar habilidades extras.

Campo `texto`, TRECHO atual: `Having vanquished the abominations <blue><b><incr>The Necromancer</incr></b></blue> greets you:`
PROPOSTA EXATA: `After you vanquish the abominations, <blue><b><incr>The Necromancer</incr></b></blue> greets you:`
Campo opção 1, ação 1 `texto`, TRECHO atual: `learning to harness the raw power that lay hidden within the realm of the dead.`
PROPOSTA EXATA: `learning to harness the raw power that lies hidden within the realm of the dead.`
Campo original `campos_originais.promptToSelectCharacter`, CAMPO atual: `Who will learn the Dark Ritual?`
PROPOSTA EXATA: `Who will learn Unholy Sacrifice?`
Justificativa: evitar que o sujeito gramatical pareça ser o Necromancer que venceu; corrigir tempo verbal; nome do benefício coerente com o candidato Unholy Sacrifice (`resources.assets:2545485`). A descrição do status declara a skill @Unholy Sacrifice@ e aumento de shadow damage `{6,30}`; não transformar isso em skill ou dano de valor final comprovado.

Anomalias/limites: `disabled=0`; 1 opção sem ocultação; resultado global vazio; ação tem CR final a preservar. Status Fortune/Permanent, sortear=false. Batalha inativa e referências batalha/encadeamento NULL por PPtr=0. Entrada de vitória `resources.assets:2545570`. NAO_EXERCITADO: aprendizagem da skill, modificador final e seleção do personagem.

## 14 — Desecrated Statue of the First Mountain King — resources.assets:2545574

VEREDITO PROPOSTO: MELHORAR — wording. Manter raridade Mythic, KeepInDeckWhenUsed=1 e duração configurada Quest; não “corrigir” a Fortune para Permanent sem decisão do dono.

Campo original `campos_originais.promptToSelectCharacter`, CAMPO atual: `Who will listen to his pleas?`
PROPOSTA EXATA: `Who will receive the Blessing of the Mountain?`
Campo opção 1 `texto`, CAMPO atual: `Take the Blessing.`
PROPOSTA EXATA: `Receive the Blessing of the Mountain for this quest.`
Campo opção 1, ação 1 `texto`, CAMPO atual: `You are filled with a fiery passion for battle and the frothy embrace of ale. It burns within your very being, igniting your spirit with a fierce determination and an insatiable thirst for both victory and merriment.`
PROPOSTA EXATA: `The Blessing of the Mountain fills you with the King's resolve, strengthening your body and helping you resist control effects.`
Justificativa: prompt não corresponde à bênção; duração merece clareza; texto de fogo/cerveja não descreve a resistência a controle e Max Health do status configurado. A nova narrativa não adiciona imunidade, fogo, ale, valor fixo nem duração permanente.

Anomalias/limites: `disabled=0`; 1 opção sem ocultação; resultado global vazio. Blessing of the Mountain (`resources.assets:2545410`) = Fortune com duração Quest; descrição autoral 50% de resistência e Max Health `{15,30}`. A descrição do status compartilhado tem ordem de fechamento `<i><color...>...</i></color>` anômala; fora da edição proposta aqui. Configuração residual de Volcanus/Burnicus com batalha.iniciar=false. Entrada de vitória de `resources.assets:2545575` (Gold Lootin' Goblins). NAO_EXERCITADO: comportamento de KeepInDeckWhenUsed fora do pool, duração/aplicação da Fortune e resistência final.

Contagem desta parte: 7 eventos, 7 MELHORAR (wording), 0 MANTER; 0 propostas de mudança de recompensa e 0 de condição. Aprovação PENDENTE para as 7 chaves. Inventário completo e anomalias por caminho: parte04.
