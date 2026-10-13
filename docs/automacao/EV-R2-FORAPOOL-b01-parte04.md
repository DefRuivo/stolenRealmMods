# EV-R2-FORAPOOL-b01 — parte 04: inventário consolidado e auditoria

Escopo: 21 propostas, eventos 1–21 das 84 seções de `C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-NotInEventPool-v2.md`. Partes01–03 contêm 7 propostas cada. Esta parte acrescenta auditoria, strings completas dos campos propostos e um complemento ao evento 3; não conta novamente eventos nem recompensas.

Status: aprovação do dono PENDENTE para as 21 chaves. VEREDITO PROPOSTO, nunca decisão aprovada. Todos os 21 vereditos são MELHORAR/wording; recompensas e condições são MANTER. 0 implementações, 0 mudanças em jogo/DLL/plugin, 0 execução do jogo.

Fontes estáticas: `eventos.json` (canônico), `eventos.schema.json` (campos), `schema.md` (semântica) e `catalogo-referencias.json` (referências), todos em `C:/dev/stolen-realm/docs/cobertura/EV-R1/`. Chave física prevalece sobre título/GUID; variantes preservadas. Peso é relativo, não chance absoluta.

## Contagem e inventário

Contagem extraída: 84 seções no lote; 21 eventos neste cartão; 30 opções; 30 ações. 260 campos NULL na projeção normalizada sem duplicar recompensas/campos_originais/ausencias. 52 strings vazias nos campos de narrativa/título/descrição/ação e nos 2 prompts inventariados. Contagens não equivalem a resultados de partida.

| Nº | Chave | Título | Categoria | Raridade | Peso | Proposta / natureza | Parte | Aprovação |
|---|---|---|---|---|---|---|---|---|
| 1 | resources.assets:2545637 | Admiral Blackbeard | NotInEventPool | Common (0) | 1.0 | MELHORAR / wording | parte01 | PENDENTE |
| 2 | resources.assets:2545545 | Bonefire | NotInEventPool | Uncommon (1) | 1.0 | MELHORAR / wording | parte01 | PENDENTE |
| 3 | resources.assets:2545547 | Bonefire | NotInEventPool | Rare (2) | 1.0 | MELHORAR / wording | parte01 | PENDENTE |
| 4 | resources.assets:2545557 | Challenger's Gong | NotInEventPool | Common (0) | 1.0 | MELHORAR / wording | parte01 | PENDENTE |
| 5 | resources.assets:2545558 | Challenger's Gong | NotInEventPool | Common (0) | 1.0 | MELHORAR / wording | parte01 | PENDENTE |
| 6 | resources.assets:2545559 | Challenger's Gong | NotInEventPool | Common (0) | 1.0 | MELHORAR / wording | parte01 | PENDENTE |
| 7 | resources.assets:2545649 | Consumed by Rage | NotInEventPool | Common (0) | 1.0 | MELHORAR / wording | parte01 | PENDENTE |
| 8 | resources.assets:2545561 | Cursed Chest | NotInEventPool | Common (0) | 1.0 | MELHORAR / wording | parte02 | PENDENTE |
| 9 | resources.assets:2545564 | Cursed Mimic | NotInEventPool | Common (0) | 1.0 | MELHORAR / wording | parte02 | PENDENTE |
| 10 | resources.assets:2545566 | Cursed Tome | NotInEventPool | Common (0) | 1.0 | MELHORAR / wording | parte02 | PENDENTE |
| 11 | resources.assets:2545567 | Cursed Tome | NotInEventPool | Common (0) | 1.0 | MELHORAR / wording | parte02 | PENDENTE |
| 12 | resources.assets:2545568 | Cursed Tome | NotInEventPool | Common (0) | 1.0 | MELHORAR / wording | parte02 | PENDENTE |
| 13 | resources.assets:2545571 | Dark Discoveries | NotInEventPool | Common (0) | 1.0 | MELHORAR / wording | parte02 | PENDENTE |
| 14 | resources.assets:2545574 | Desecrated Statue of the First Mountain King | NotInEventPool | Mythic (4) | 1.0 | MELHORAR / wording | parte02 | PENDENTE |
| 15 | resources.assets:2545586 | Enchanted Pumpkin Patch | NotInEventPool | Rare (2) | 1.0 | MELHORAR / wording | parte03 | PENDENTE |
| 16 | resources.assets:2545594 | Foreboding Gem - Victory | NotInEventPool | Common (0) | 1.0 | MELHORAR / wording | parte03 | PENDENTE |
| 17 | resources.assets:2545575 | Gold Lootin' Goblins | NotInEventPool | Common (0) | 1.0 | MELHORAR / wording | parte03 | PENDENTE |
| 18 | resources.assets:2545600 | Gold Statue of the First Mountain King | NotInEventPool | Common (0) | 1.0 | MELHORAR / wording | parte03 | PENDENTE |
| 19 | resources.assets:2545605 | Hell Coffer | NotInEventPool | Common (0) | 1.0 | MELHORAR / wording | parte03 | PENDENTE |
| 20 | resources.assets:2545607 | Hell Gate | NotInEventPool | Common (0) | 1.0 | MELHORAR / wording | parte03 | PENDENTE |
| 21 | resources.assets:2545610 | Horn of Glorious Battle | NotInEventPool | Common (0) | 1.0 | MELHORAR / wording | parte03 | PENDENTE |

## Leitura obrigatória dos NULL e limites

NAO_EXERCITADO: jogo/runtime Unity, disponibilidade numa party, escolha de personagem, UI/renderização/placeholder, XP/ouro/loot finais, RNG, aplicação de status, batalhas e evolução das Fortunes. Motivo: escopo exclusivamente documental; o jogo não foi aberto. O verificador é offline e NÃO certifica a execução dos eventos.

Nos campos finais com NULL, os motivos abaixo são copiados do contêiner canônico. Não são zero nem recompensa ausente. Flags dar=false são configuração autoral, separadas de quantidade_final=NULL. PPtr serializado m_PathID=0 significa referência nula configurada, não runtime pendente. Campos de combate com iniciar=false podem guardar resíduos; com iniciar=true e referência nula, overrides ou seleção runtime podem definir a batalha. Não transformar PPtr NULL isolado em diagnóstico de evento quebrado.

Opções ocultas: distinguir ocultar_sem_requisitos/hideIfHasStatuses de hideOptionEffectText (ocultação do TEXTO de efeitos, não necessariamente do botão). Visibilidade efetiva é NAO_EXERCITADO. ListHolderEvents comprova inventário, não disparo runtime. Entradas de PartyEvent, BattleInfo e EventStatus são referências estáticas; escanear o catálogo não decodifica universalmente Odin nem garante todos os vínculos possíveis.

Não escolher FullReleaseMode por inferência; os overrides autorais permanecem. Não duplicar opcoes[].recompensas, que é projeção dos efeitos. Strings completas abaixo são simulação DOCUMENTAL de redação para aprovação, não alteração dos dados nem substituição de NULL.

## Complemento incremental à parte01

Evento 3, `resources.assets:2545547`, campo `campos_originais.promptToSelectCharacter`: atual `"Dare to open the Cursed Chest?"` → PROPOSTA EXATA `"Who will rest or prepare for the journey ahead?"`. Prompt herdado de Cursed Chest na variante Campaign, identificado na leitura completa dos campos originais; não alterar targetType.

Evento 7, `resources.assets:2545649`, campo `campos_originais.promptToSelectCharacter`: atual `"Who will listen to his pleas?"` → PROPOSTA EXATA `"Who will face the wendigos?"`. Formalização da proposta adicional já descrita na parte01; não é uma segunda mudança no mesmo campo.

A auditoria complementa entradas omitidas na primeira leitura: Bonefire Campaign (evento 3) também é vitória de `resources.assets:2545772`; Consumed by Rage (evento 7) é ForcedNextEvent do EventStatus Master of Rage (`resources.assets:2545514`). Nenhum dos dois fatos autoriza mudar disponibilidade/pool. Ver caminhos exatos por evento abaixo.

## Auditoria por evento — 21 registros

### 01 — Admiral Blackbeard — resources.assets:2545637

Fonte canônica: `eventos.json#/eventos/161`. GUID real: `f5475aa4-e4e2-4449-a392-0a4f7948315f`. Resource: `["events/main quests/5 - admiral blackbeard end"]`. Objeto SHA-256: `28d002141ad1475cfb829abc90e4cccc3ee01493178fe3b72e1ed3e5d9af42dd`.

Categoria=NotInEventPool; raridade=Common (0); peso=1.0; disabled=0; EditorOnly=0. 0 opções / 0 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 1, "allowedNodeTypes": [], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 1, "allowedTimeOfDay": 0, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 0}`

Textos vazios inventariados: 3. `$.texto_resultados_possiveis=""`; `$.campos_originais.promptToSelectCharacter=""`; `$.campos_originais.characterSelectedText=""`


Referências de entrada encontradas: 2 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545638` (PartyEvent, Admiral Blackbeard), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[106]`.

Referências PPtr NÃO nulas do objeto original: 1; resolvidas no catálogo: 1. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.

Campos NULL na projeção sem duplicação: 0. Motivo literal do contêiner:
- Nenhum NULL na projeção normalizada; isso NÃO significa runtime exercitado.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `texto` ATUAL: `"Shadowy chains, manifestations of the curse that had consumed Blackbeard's soul, emerge from the abyss, reaching for the fallen pirate. With an inexorable grip, they pull him down into the unfathomable depths of darkness, an abyss where greed and power has led him. \n\nA soft glow emanates from the spot where Blackbeard had vanished. There, lying amidst the ancient stones of the temple, is a brilliant gold coin, radiant and untouched by the darkness that had just been vanquished.\n\nTentatively, you reach out and touch the coin, its surface cool and smooth under your fingers.\n\r<br/>\nYou are carried aboard a ship, the deck alive with the sounds of the sea – the creaking of wood, the cry of gulls, and the rush of the wind. Here, amidst the salt and spray, sits a young Blackbeard, his face unmarked by the years of hardship and cruelty that would later define him. His hair is tousled by the sea breeze, and his eyes sparkle with the untamed spirit of adventure.\n\nThe young Blackbeard is laughing heartily, surrounded by his shipmates, as they engage in a game of chance. The atmosphere is light and jovial, filled with the camaraderie of men and women who share a love for the sea and the thrill of adventure. They are brothers in arms, united by the bonds forged in the vast and unpredictable embrace of the ocean.\n\r<br/>\nYour mind is awash with questions, a torrent as tumultuous as the sea that surrounds the ruins. The memories unveiled by these magical artifacts paints pictures of lives that had once been, lives of men before they were consumed by the shadows of their desires. You can't help but ponder the enigma your father is unraveling, a mystery that intertwines the fates of these men with the ancient and mysterious defeat of the dragons.\n\nThe journal now points towards a new destination – the frosty peaks of Frostwrought Mountain."`
  PROPOSTA EXATA COMPLETA: `"Shadowy chains, manifestations of the curse that had consumed Blackbeard's soul, emerge from the abyss, reaching for the fallen pirate. With an inexorable grip, they pull him down into the unfathomable depths of darkness, an abyss where greed and power have led him. \n\nA soft glow emanates from the spot where Blackbeard had vanished. There, lying amidst the ancient stones of the temple, is a brilliant gold coin, radiant and untouched by the darkness that had just been vanquished.\n\nTentatively, you reach out and touch the coin, its surface cool and smooth under your fingers.\n\r<br/>\nYou are carried aboard a ship, the deck alive with the sounds of the sea – the creaking of wood, the cry of gulls, and the rush of the wind. Here, amidst the salt and spray, sits a young Blackbeard, his face unmarked by the years of hardship and cruelty that would later define him. His hair is tousled by the sea breeze, and his eyes sparkle with the untamed spirit of adventure.\n\nThe young Blackbeard is laughing heartily, surrounded by his shipmates, as they engage in a game of chance. The atmosphere is light and jovial, filled with the camaraderie of men and women who share a love for the sea and the thrill of adventure. They are brothers in arms, united by the bonds forged in the vast and unpredictable embrace of the ocean.\n\r<br/>\nYour mind is awash with questions, a torrent as tumultuous as the sea that surrounds the ruins. The memories unveiled by these magical artifacts paint pictures of lives that had once been, lives of men before they were consumed by the shadows of their desires. You can't help but ponder the enigma your father is unraveling, a mystery that intertwines the fates of these men with the ancient and mysterious defeat of the dragons.\n\nThe journal now points towards a new destination – the frosty peaks of Frostwrought Mountain."`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 02 — Bonefire — resources.assets:2545545

Fonte canônica: `eventos.json#/eventos/162`. GUID real: `05935caa-5cfd-411e-8ab8-92d6d0bc9018`. Resource: `["events/bonefire (roguelike) - victory"]`. Objeto SHA-256: `1331c529795e7f55906fef7966172805d690ca81a0c01f88a758cc702dc2eeba`.

Categoria=NotInEventPool; raridade=Uncommon (1); peso=1.0; disabled=0; EditorOnly=0. 3 opções / 3 ações. Modos: `[{"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 0, "allowedNodeTypes": [2], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 1, "allowedTimeOfDay": 0, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 0}`

Textos vazios inventariados: 6. `$.texto_resultados_possiveis=""`; `$.campos_originais.promptToSelectCharacter=""`; `$.campos_originais.characterSelectedText=""`; `$.opcoes[0].efeitos[0].texto=""`; `$.opcoes[1].texto=""`; `$.opcoes[2].texto=""`

Opção 1 (Rest): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 50.0, "percentMaxMana": 50.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`
Opção 2 (Reroll Skill): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 1, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 2/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Opção 3 (Level Up Fortunes): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 1}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 3/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.

Referências de entrada encontradas: 2 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545546` (PartyEvent, Bonefire), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[15]`.

Referências PPtr NÃO nulas do objeto original: 1; resolvidas no catálogo: 1. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.

Campos NULL na projeção sem duplicação: 19. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (12 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`, `$.opcoes[1].efeitos[0].batalha.referencia.chave`, `$.opcoes[1].efeitos[0].batalha.referencia.nome`, `$.opcoes[1].efeitos[0].evento_encadeado.chave`, `$.opcoes[1].efeitos[0].evento_encadeado.nome`, `$.opcoes[2].efeitos[0].batalha.referencia.chave`, `$.opcoes[2].efeitos[0].batalha.referencia.nome`, `$.opcoes[2].efeitos[0].evento_encadeado.chave`, `$.opcoes[2].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (3 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`, `$.opcoes[1].efeitos[0].batalha.dados_recompensa_final`, `$.opcoes[2].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `texto` ATUAL: `"Despite your growing fatigue, you fight with relentless determination. Shattering bone after bone, extinguishing the eerie light in the skeletons' hollow eye sockets.\n\nWith a final, resounding crack, the last skeleton falls, and the bonfire's flames abruptly extinguish, plunging the area into darkness. Weary but victorious, you stand panting in the sudden silence, your breath fogging in the cold air."`
  PROPOSTA EXATA COMPLETA: `"Despite your growing fatigue, you fight with relentless determination, shattering bone after bone and extinguishing the eerie light in the skeletons' hollow eye sockets.\n\nWith a final, resounding crack, the last skeleton falls, and the bonfire's flames abruptly extinguish, plunging the area into darkness. Weary but victorious, you stand panting in the sudden silence, your breath fogging in the cold air."`
- `opcoes[0].texto` ATUAL: `"Sit by the fire and recover your strength."`
  PROPOSTA EXATA COMPLETA: `"Sit and recover your strength."`
- `opcoes[1].texto` ATUAL: `""`
  PROPOSTA EXATA COMPLETA: `"Open the skill reroll menu."`
- `opcoes[2].texto` ATUAL: `""`
  PROPOSTA EXATA COMPLETA: `"Level up your Fortunes to your character level."`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 03 — Bonefire — resources.assets:2545547

Fonte canônica: `eventos.json#/eventos/163`. GUID real: `6b8e0706-2a01-49f2-916a-9dccad57f73b`. Resource: `["events/bonefire - victory"]`. Objeto SHA-256: `f821c79eaab003478b4274e073ec95ee9e1a813a6a2d919c67d56315c244a546`.

Categoria=NotInEventPool; raridade=Rare (2); peso=1.0; disabled=0; EditorOnly=0. 2 opções / 2 ações. Modos: `[{"valor": 0, "nome": "Campaign"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 0, "allowedNodeTypes": [7], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 0, "allowedTimeOfDay": 1, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [4, 0, 3, 5], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 0}`

Textos vazios inventariados: 3. `$.texto_resultados_possiveis=""`; `$.opcoes[0].efeitos[0].texto=""`; `$.opcoes[1].efeitos[0].texto=""`

Opção 1 (Rest): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 50.0, "percentMaxMana": 50.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`
Opção 2 (Prepare): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 2/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 2/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [{"chave": "resources.assets:2545391", "nome": "Prepared", "pptr": {"m_FileID": 0, "m_PathID": 2545391}, "tipo": "EventStatus", "descricao": "Item and gold drops are increased by 20%.", "duracao": {"valor": 1, "nome": "Quest"}, "status_tipo": {"valor": 0, "nome": "Normal"}, "modificadores": [{"atributo": {"chave": "resources.assets:2544419", "nome": "DropQuantityMod", "pptr": {"m_FileID": 0, "m_PathID": 2544419}, "tipo": "CharacterAttribute"}, "metodo": {"valor": 0, "nome": "Base"}, "expressao": "20", "segunda_passagem": false}, {"atributo": {"chave": "resources.assets:2544424", "nome": "GoldMod", "pptr": {"m_FileID": 0, "m_PathID": 2544424}, "tipo": "CharacterAttribute"}, "metodo": {"valor": 0, "nome": "Base"}, "expressao": "20", "segunda_passagem": false}]}], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`

Referências de entrada encontradas: 3 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545548` (PartyEvent, Bonefire), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2545772` (PartyEvent, What Lurks), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[17]`.

Referências PPtr NÃO nulas do objeto original: 3; resolvidas no catálogo: 3. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.
- `$.campos_originais.eventOptions[1].eventActions[0].EventActionEffects[0].eventStatuses[0]` → `resources.assets:2545391`: Prepared / EventStatus; resolvida=True.
- `$.campos_originais.eventOptions[1].eventActions[0].EventActionEffects[0].rolledEventStatuses[0]` → `resources.assets:2545391`: Prepared / EventStatus; resolvida=True.

Campos NULL na projeção sem duplicação: 18. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (8 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`, `$.opcoes[1].efeitos[0].batalha.referencia.chave`, `$.opcoes[1].efeitos[0].batalha.referencia.nome`, `$.opcoes[1].efeitos[0].evento_encadeado.chave`, `$.opcoes[1].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (2 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`, `$.opcoes[1].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `texto` ATUAL: `"Despite your growing fatigue, you fight with relentless determination. Shattering bone after bone, extinguishing the eerie light in the skeletons' hollow eye sockets.\n\nWith a final, resounding crack, the last skeleton falls, and the bonfire's flames abruptly extinguish, plunging the area into darkness. Weary but victorious, you stand panting in the sudden silence, your breath fogging in the cold air."`
  PROPOSTA EXATA COMPLETA: `"Despite your growing fatigue, you fight with relentless determination, shattering bone after bone and extinguishing the eerie light in the skeletons' hollow eye sockets.\n\nWith a final, resounding crack, the last skeleton falls, and the bonfire's flames abruptly extinguish, plunging the area into darkness. Weary but victorious, you stand panting in the sudden silence, your breath fogging in the cold air."`
- `opcoes[1].texto` ATUAL: `"Take time to prepare for what's ahead."`
  PROPOSTA EXATA COMPLETA: `"Take time to prepare for what's ahead and gain Prepared for this quest."`
- `campos_originais.promptToSelectCharacter` ATUAL: `"Dare to open the Cursed Chest?"`
  PROPOSTA EXATA COMPLETA: `"Who will rest or prepare for the journey ahead?"`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 04 — Challenger's Gong — resources.assets:2545557

Fonte canônica: `eventos.json#/eventos/164`. GUID real: `8acc5e69-2a57-46db-87f5-5ee7de130916`. Resource: `["events/challenger's gong - victory 1"]`. Objeto SHA-256: `fff60d788c1e468a81fafbff2a7f490fc5fc022412bba82f9ad60d9ebd938dce`.

Categoria=NotInEventPool; raridade=Common (0); peso=1.0; disabled=0; EditorOnly=0. 1 opções / 1 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 0, "allowedNodeTypes": [7], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 1, "allowedTimeOfDay": 0, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 1}`

Textos vazios inventariados: 3. `$.texto_resultados_possiveis=""`; `$.campos_originais.characterSelectedText=""`; `$.opcoes[0].efeitos[0].texto=""`

Opção 1 (Fight): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`true`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=4; VictoryEvent=`{"m_FileID": 0, "m_PathID": 2545558}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`

Referências de entrada encontradas: 2 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545560` (PartyEvent, Challenger's Gong), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[27]`.

Referências PPtr NÃO nulas do objeto original: 6; resolvidas no catálogo: 6. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[0].CharacterInfo` → `resources.assets:2545132`: Leo / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[1].CharacterInfo` → `resources.assets:2545129`: Donnie / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[2].CharacterInfo` → `resources.assets:2545133`: Mikey / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[3].CharacterInfo` → `resources.assets:2545134`: Raph / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent` → `resources.assets:2545558`: Challenger's Gong - Victory 2 / PartyEvent; resolvida=True.

Campos NULL na projeção sem duplicação: 9. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (4 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (1 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `campos_originais.promptToSelectCharacter` ATUAL: `"Who will listen to his pleas?"`
  PROPOSTA EXATA COMPLETA: `"Who will face the next challengers?"`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 05 — Challenger's Gong — resources.assets:2545558

Fonte canônica: `eventos.json#/eventos/165`. GUID real: `ae1bb381-411b-4ed0-b1fb-1a3c06dc8559`. Resource: `["events/challenger's gong - victory 2"]`. Objeto SHA-256: `9b6781c561e3e9da8876fd4eba889ab20cb68a2daf31658209a1a395c763afb8`.

Categoria=NotInEventPool; raridade=Common (0); peso=1.0; disabled=0; EditorOnly=0. 1 opções / 1 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 0, "allowedNodeTypes": [7], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 1, "allowedTimeOfDay": 0, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 1}`

Textos vazios inventariados: 3. `$.texto_resultados_possiveis=""`; `$.campos_originais.characterSelectedText=""`; `$.opcoes[0].efeitos[0].texto=""`

Opção 1 (Fight): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`true`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=1; VictoryEvent=`{"m_FileID": 0, "m_PathID": 2545559}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`

Referências de entrada encontradas: 2 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545557` (PartyEvent, Challenger's Gong), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[28]`.

Referências PPtr NÃO nulas do objeto original: 3; resolvidas no catálogo: 3. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[0].CharacterInfo` → `resources.assets:2545135`: Ronin / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent` → `resources.assets:2545559`: Challenger's Gong - Victory 3 / PartyEvent; resolvida=True.

Campos NULL na projeção sem duplicação: 9. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (4 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (1 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `texto` ATUAL: `"Battles erupte, their clash echoing through the mountain passes, as heroes meet in a whirlwind of steel and fury. But it is <orange><b><incr>Ronin</incr></b></orange>, a warrior of renowned skill and indomitable spirit, who emerges as the final challenger to the gong's call. His reputation precedes him, and tales of his valor have spread like wildfire throughout the Stolen Realm. He stands tall, his eyes ablaze with determination, as he steps forth to claim the honor of facing the gong's ultimate trial."`
  PROPOSTA EXATA COMPLETA: `"Battles erupt, their clash echoing through the mountain passes, as heroes meet in a whirlwind of steel and fury. But it is <orange><b><incr>Ronin</incr></b></orange>, a warrior of renowned skill and indomitable spirit, who emerges as the final challenger to the gong's call. His reputation precedes him, and tales of his valor have spread like wildfire throughout the Stolen Realm. He stands tall, his eyes ablaze with determination, as he steps forth to claim the honor of facing the gong's ultimate trial."`
- `campos_originais.promptToSelectCharacter` ATUAL: `"Who will listen to his pleas?"`
  PROPOSTA EXATA COMPLETA: `"Who will confront Ronin?"`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 06 — Challenger's Gong — resources.assets:2545559

Fonte canônica: `eventos.json#/eventos/166`. GUID real: `18894a29-845e-4a2f-a58e-504da8a0aad2`. Resource: `["events/challenger's gong - victory 3"]`. Objeto SHA-256: `894de76b1c6fa0a5768cf8f3324444d9d407b7d5a7adfa21794cb3dc10c4b754`.

Categoria=NotInEventPool; raridade=Common (0); peso=1.0; disabled=0; EditorOnly=0. 1 opções / 1 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 0, "allowedNodeTypes": [7], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 1, "allowedTimeOfDay": 0, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 1}`

Textos vazios inventariados: 3. `$.texto_resultados_possiveis=""`; `$.campos_originais.characterSelectedText=""`; `$.opcoes[0].efeitos[0].texto=""`

Opção 1 (Reward): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=1; VictoryEvent=`{"m_FileID": 0, "m_PathID": 2545559}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [{"chave": "resources.assets:2545412", "nome": "Bloodied Bargain", "pptr": {"m_FileID": 0, "m_PathID": 2545412}, "tipo": "EventStatus", "descricao": "Increases @Physical Damage@ by {8,40}%. Physical damage you deal applies 1 stack of @Bleeding@.\n\n<i><color=#808080>A price in blood must be paid, just be sure you're not the one to pay it.</color></i>", "duracao": {"valor": 3, "nome": "Permanent"}, "status_tipo": {"valor": 1, "nome": "Fortune"}, "modificadores": [{"atributo": {"chave": "resources.assets:2544380", "nome": "DamageModPhysical", "pptr": {"m_FileID": 0, "m_PathID": 2544380}, "tipo": "CharacterAttribute"}, "metodo": {"valor": 0, "nome": "Base"}, "expressao": "{8,40}", "segunda_passagem": false}]}], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`

Referências de entrada encontradas: 3 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545558` (PartyEvent, Challenger's Gong), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2545559` (PartyEvent, Challenger's Gong), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[29]`.

Referências PPtr NÃO nulas do objeto original: 5; resolvidas no catálogo: 5. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[0].CharacterInfo` → `resources.assets:2545135`: Ronin / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent` → `resources.assets:2545559`: Challenger's Gong - Victory 3 / PartyEvent; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].EventActionEffects[0].eventStatuses[0]` → `resources.assets:2545412`: Bloodied Bargain / EventStatus; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].EventActionEffects[0].rolledEventStatuses[0]` → `resources.assets:2545412`: Bloodied Bargain / EventStatus; resolvida=True.

Campos NULL na projeção sem duplicação: 9. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (4 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (1 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `campos_originais.promptToSelectCharacter` ATUAL: `"Who will take the ?"`
  PROPOSTA EXATA COMPLETA: `"Who will receive the reward?"`
- `opcoes[0].texto` ATUAL: `"You bear the honor of victory."`
  PROPOSTA EXATA COMPLETA: `"You bear the honor of victory and receive Bloodied Bargain."`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 07 — Consumed by Rage — resources.assets:2545649

Fonte canônica: `eventos.json#/eventos/167`. GUID real: `bb2ea4ea-f11f-4bb1-9812-0623428ffe12`. Resource: `["events/master of rage - 1"]`. Objeto SHA-256: `99740da7d657aa0afa63a90d121eab8b4673e9bfcf536f5e6a2791bd2081cfee`.

Categoria=NotInEventPool; raridade=Common (0); peso=1.0; disabled=0; EditorOnly=0. 2 opções / 2 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 0, "allowedNodeTypes": [7], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 1, "allowedTimeOfDay": 0, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 1}`

Textos vazios inventariados: 1. `$.campos_originais.characterSelectedText=""`

Opção 1 (Fight): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`true`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=4; VictoryEvent=`{"m_FileID": 0, "m_PathID": 2545650}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`
Opção 2 (Leave): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 2/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 2/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [{"chave": "resources.assets:2545494", "nome": "Enfeebled", "pptr": {"m_FileID": 0, "m_PathID": 2545494}, "tipo": "EventStatus", "descricao": "Reduces @Damage@ by @20%@ per stack.", "duracao": {"valor": 1, "nome": "Quest"}, "status_tipo": {"valor": 0, "nome": "Normal"}, "modificadores": [{"atributo": {"chave": "resources.assets:2544373", "nome": "DamageMod", "pptr": {"m_FileID": 0, "m_PathID": 2544373}, "tipo": "CharacterAttribute"}, "metodo": {"valor": 0, "nome": "Base"}, "expressao": "-20", "segunda_passagem": false}]}], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": [{"RemovalCondition": "ActionStatus.Name == \"Rage Unleashed\"", "RemovalTarget": 1, "ActionOnRemoval": {"m_FileID": 0, "m_PathID": 0}, "DurationTypesToRemove": [1], "FilterBenefitType": 0, "BenefitType": 0, "NumStatusesToRemove": "", "StealStatuses": 0, "GiveStatuses": 0, "ForceDispell": 0}]}`

Referências de entrada encontradas: 2 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545514` (EventStatus, Master of Rage), `data.ForcedNextEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[119]`.

Referências PPtr NÃO nulas do objeto original: 8; resolvidas no catálogo: 8. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[0].CharacterInfo` → `resources.assets:2545299`: Wendigo / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[1].CharacterInfo` → `resources.assets:2545299`: Wendigo / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[2].CharacterInfo` → `resources.assets:2545299`: Wendigo / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[3].CharacterInfo` → `resources.assets:2545299`: Wendigo / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent` → `resources.assets:2545650`: Master of Rage - Victory / PartyEvent; resolvida=True.
- `$.campos_originais.eventOptions[1].eventActions[0].EventActionEffects[0].eventStatuses[0]` → `resources.assets:2545494`: Enfeebled / EventStatus; resolvida=True.
- `$.campos_originais.eventOptions[1].eventActions[0].EventActionEffects[0].rolledEventStatuses[0]` → `resources.assets:2545494`: Enfeebled / EventStatus; resolvida=True.

Campos NULL na projeção sem duplicação: 18. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (8 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`, `$.opcoes[1].efeitos[0].batalha.referencia.chave`, `$.opcoes[1].efeitos[0].batalha.referencia.nome`, `$.opcoes[1].efeitos[0].evento_encadeado.chave`, `$.opcoes[1].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (2 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`, `$.opcoes[1].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `texto` ATUAL: `"As you reach the arid mountain pass, a harsh wind cuts through your cloak and chills you to the bone. Your breath fogs in the cold air, as you trudge through the rough terrain, the fresh snow crunching beneath your boots.\n\n\nThen, a low howl echoes through the mountain, sending a jolt of fear through your heart. Eyes glowing with a ghastly blue light emerge from beyond the pass, followed by monstrous forms taking shape.\n\n\nWendigos, beings of nightmare and rage. Each bares horns sprouting from their skulls, bodies lean and drawn out to the point of emaciation, their hideous forms resembling humanoid stags.\n\n\nSavage snarls fill the mountain as the wendigos advance, their claws leaving gouges in the frozen ground. "`
  PROPOSTA EXATA COMPLETA: `"As you reach the arid mountain pass, a harsh wind cuts through your cloak and chills you to the bone. Your breath fogs in the cold air, as you trudge through the rough terrain, the fresh snow crunching beneath your boots.\n\n\nThen, a low howl echoes through the mountain, sending a jolt of fear through your heart. Eyes glowing with a ghastly blue light emerge from beyond the pass, followed by monstrous forms taking shape.\n\n\nWendigos, beings of nightmare and rage. Each bears horns sprouting from their skulls, bodies lean and drawn out to the point of emaciation, their hideous forms resembling humanoid stags.\n\n\nSavage snarls fill the mountain as the wendigos advance, their claws leaving gouges in the frozen ground. "`
- `opcoes[0].texto` ATUAL: `"Slay the Wendigo."`
  PROPOSTA EXATA COMPLETA: `"Slay the wendigos."`
- `opcoes[1].texto` ATUAL: `"No amount of anger can convince you to stay."`
  PROPOSTA EXATA COMPLETA: `"Leave the pass. This choice applies Enfeebled and is configured to remove Rage Unleashed."`
- `opcoes[1].efeitos[0].texto` ATUAL: `"The moment you see the wendigo, you falter. Courage and determination bleeds away, replaced by the primal instinct of survival. You turn on your heels, casting aside your plans of attack. "`
  PROPOSTA EXATA COMPLETA: `"The moment you see the wendigo, you falter. Courage and determination bleed away, replaced by the primal instinct of survival. You turn on your heels, casting aside your plans of attack. "`
- `campos_originais.promptToSelectCharacter` ATUAL: `"Who will listen to his pleas?"`
  PROPOSTA EXATA COMPLETA: `"Who will face the wendigos?"`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 08 — Cursed Chest — resources.assets:2545561

Fonte canônica: `eventos.json#/eventos/168`. GUID real: `29e3b6c4-59da-42f0-8622-5b4667ce8c68`. Resource: `["events/cursed chest battle victory"]`. Objeto SHA-256: `ba6aafb6b599cf9273241fc6543d993709abf695cafdcde03114312cc0b6502c`.

Categoria=NotInEventPool; raridade=Common (0); peso=1.0; disabled=0; EditorOnly=0. 1 opções / 1 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 0, "allowedNodeTypes": [7], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 1, "allowedTimeOfDay": 1, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [4, 3], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 0}`

Textos vazios inventariados: 3. `$.texto_resultados_possiveis=""`; `$.opcoes[0].texto=""`; `$.opcoes[0].efeitos[0].texto=""`

Opção 1 (Claim your reward!): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": true, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [0, 0], "limitItemRarities": 1, "possibleRarities": [2, 3]}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`

Referências de entrada encontradas: 4 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545562` (PartyEvent, Cursed Chest), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2545562` (PartyEvent, Cursed Chest), `campos_originais.eventOptions[0].eventActions[1].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2544645` (BattleInfo, Cursed Chest Battle), `data.victoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[31]`.

Referências PPtr NÃO nulas do objeto original: 1; resolvidas no catálogo: 1. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.

Campos NULL na projeção sem duplicação: 9. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (4 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (1 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `texto` ATUAL: `"At last, the undead are vanquished, their twisted forms returning to the earth.\n\nThe <indigo><b><incr>Cursed Chest</incr></b></indigo>, now free from its macabre prison of decay, lays before you. With caution and a mingling sense of anticipation, you open the chest, revealing its hidden treasure. "`
  PROPOSTA EXATA COMPLETA: `"At last, the undead are vanquished, their twisted forms returning to the earth.\n\nThe <indigo><b><incr>Cursed Chest</incr></b></indigo>, now free from its macabre prison of decay, lies before you. With caution and a mingling sense of anticipation, you open the chest, revealing its hidden treasure. "`
- `campos_originais.promptToSelectCharacter` ATUAL: `"Does anyone owe this Ogre money?"`
  PROPOSTA EXATA COMPLETA: `"Who will claim the chest's treasure?"`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 09 — Cursed Mimic — resources.assets:2545564

Fonte canônica: `eventos.json#/eventos/169`. GUID real: `a0c631c5-b0b7-4956-97c5-2440b1a84d19`. Resource: `["events/cursed mimic chest victory"]`. Objeto SHA-256: `e158350bf11deadf5f15c3c351c5aea8de1becdf793f0dde392e4f8b57304739`.

Categoria=NotInEventPool; raridade=Common (0); peso=1.0; disabled=0; EditorOnly=0. 3 opções / 3 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 0, "allowedNodeTypes": [7], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 1, "allowedTimeOfDay": 1, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [4, 3], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 1}`

Textos vazios inventariados: 0. Nenhum nos campos de narrativa inventariados.

Opção 1 (Emblem of the Iron Fortress): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [{"chave": "resources.assets:2545433", "nome": "Emblem of the Iron Fortress", "pptr": {"m_FileID": 0, "m_PathID": 2545433}, "tipo": "EventStatus", "descricao": "Grants {10,250} Armor. 3% of your Armor is added as physical damage return.\n\n<i><color=#808080>The Iron Fortress, an indomitable monolith of enduring strength, stood resolute and unyielding for hundreds of years, its towering parapets and impenetrable defenses the silent testament to countless civilizations that had crumbled in their futile attempts to conquer it.</color></i>", "duracao": {"valor": 3, "nome": "Permanent"}, "status_tipo": {"valor": 1, "nome": "Fortune"}, "modificadores": [{"atributo": {"chave": "resources.assets:2544387", "nome": "DamageReturnedFlatPhysical", "pptr": {"m_FileID": 0, "m_PathID": 2544387}, "tipo": "CharacterAttribute"}, "metodo": {"valor": 0, "nome": "Base"}, "expressao": "Source[\"Armor\"] * {.03f, .03f}", "segunda_passagem": false}, {"atributo": {"chave": "resources.assets:2544401", "nome": "Armor", "pptr": {"m_FileID": 0, "m_PathID": 2544401}, "tipo": "CharacterAttribute"}, "metodo": {"valor": 0, "nome": "Base"}, "expressao": "{10, 250}", "segunda_passagem": false}]}], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`
Opção 2 (Frozen Lich Heart): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 2/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 2/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [{"chave": "resources.assets:2545442", "nome": "Frozen Lich Heart", "pptr": {"m_FileID": 0, "m_PathID": 2545442}, "tipo": "EventStatus", "descricao": "Your cold damage is increased by [0]% against targets that are frozen. Grants immunity to chilled.\n\n<i><color=#808080>The Frozen Heart of the Lich, pulsating with a masterful power of ice and the chill of a thousand winters, imbued its holder with a profound affinity for the cold, such that even in the harshest blizzards they would find a comfortable sanctuary.</color></i>", "duracao": {"valor": 3, "nome": "Permanent"}, "status_tipo": {"valor": 1, "nome": "Fortune"}, "modificadores": [{"atributo": {"chave": "resources.assets:2544376", "nome": "DamageModColdToFrozen", "pptr": {"m_FileID": 0, "m_PathID": 2544376}, "tipo": "CharacterAttribute"}, "metodo": {"valor": 0, "nome": "Base"}, "expressao": "{100, 200}", "segunda_passagem": false}, {"atributo": {"chave": "resources.assets:2544534", "nome": "ImmunityChilled", "pptr": {"m_FileID": 0, "m_PathID": 2544534}, "tipo": "CharacterAttribute"}, "metodo": {"valor": 4, "nome": "Set"}, "expressao": "1", "segunda_passagem": false}]}], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`
Opção 3 (Ball Lightning): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 3/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 3/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [{"chave": "resources.assets:2545409", "nome": "Ball Lightning", "pptr": {"m_FileID": 0, "m_PathID": 2545409}, "tipo": "EventStatus", "descricao": "Dealing lightning damage grants a stack of Overcharge: Each stack adds <color=#CBB396>[0]</color> lightning damage to your next basic attack.\n\n<i><color=#808080>In fury, the sky roars, a tempest untamed,\nLightning cracks, an ephemeral fire, wild and unchained.</color></i>", "duracao": {"valor": 3, "nome": "Permanent"}, "status_tipo": {"valor": 1, "nome": "Fortune"}, "modificadores": [{"atributo": {"chave": "resources.assets:2544579", "nome": "BallLightningAmount", "pptr": {"m_FileID": 0, "m_PathID": 2544579}, "tipo": "CharacterAttribute"}, "metodo": {"valor": 0, "nome": "Base"}, "expressao": "ActionStatus.GetFlatDamageValue * 15 * Target.DamageModLightning", "segunda_passagem": false}]}], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`

Referências de entrada encontradas: 2 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545565` (PartyEvent, Cursed Chest), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[34]`.

Referências PPtr NÃO nulas do objeto original: 7; resolvidas no catálogo: 7. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].EventActionEffects[0].eventStatuses[0]` → `resources.assets:2545433`: Emblem of the Iron Fortress / EventStatus; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].EventActionEffects[0].rolledEventStatuses[0]` → `resources.assets:2545433`: Emblem of the Iron Fortress / EventStatus; resolvida=True.
- `$.campos_originais.eventOptions[1].eventActions[0].EventActionEffects[0].eventStatuses[0]` → `resources.assets:2545442`: Frozen Lich Heart / EventStatus; resolvida=True.
- `$.campos_originais.eventOptions[1].eventActions[0].EventActionEffects[0].rolledEventStatuses[0]` → `resources.assets:2545442`: Frozen Lich Heart / EventStatus; resolvida=True.
- `$.campos_originais.eventOptions[2].eventActions[0].EventActionEffects[0].eventStatuses[0]` → `resources.assets:2545409`: Ball Lightning / EventStatus; resolvida=True.
- `$.campos_originais.eventOptions[2].eventActions[0].EventActionEffects[0].rolledEventStatuses[0]` → `resources.assets:2545409`: Ball Lightning / EventStatus; resolvida=True.

Campos NULL na projeção sem duplicação: 27. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (3 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`, `$.opcoes[2].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (3 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`, `$.opcoes[2].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (3 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`, `$.opcoes[2].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (3 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`, `$.opcoes[2].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (12 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`, `$.opcoes[1].efeitos[0].batalha.referencia.chave`, `$.opcoes[1].efeitos[0].batalha.referencia.nome`, `$.opcoes[1].efeitos[0].evento_encadeado.chave`, `$.opcoes[1].efeitos[0].evento_encadeado.nome`, `$.opcoes[2].efeitos[0].batalha.referencia.chave`, `$.opcoes[2].efeitos[0].batalha.referencia.nome`, `$.opcoes[2].efeitos[0].evento_encadeado.chave`, `$.opcoes[2].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (3 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`, `$.opcoes[1].efeitos[0].batalha.dados_recompensa_final`, `$.opcoes[2].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `texto` ATUAL: `"The mimic shrinks back, until, finally, it gives a last gurgling growl in defeat. The taint dissolved, fading away into smoke and shadow, leaving behind an empty silence.\n\nAs the darkness vanishes, it reveals a small mound of treasure in its wake."`
  PROPOSTA EXATA COMPLETA: `"The mimic shrinks back, until, finally, it gives a last gurgling growl in defeat. The taint dissolves, fading away into smoke and shadow, leaving behind an empty silence.\n\nAs the darkness vanishes, it reveals a small mound of treasure in its wake."`
- `opcoes[1].efeitos[0].texto` ATUAL: `"As you take the Frozen Heart it's numbing cold begins to feel... comfortable."`
  PROPOSTA EXATA COMPLETA: `"As you take the Frozen Heart, its numbing cold begins to feel... comfortable."`
- `campos_originais.promptToSelectCharacter` ATUAL: `"Does anyone owe this Ogre money?"`
  PROPOSTA EXATA COMPLETA: `"Who will claim the mimic's treasure?"`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 10 — Cursed Tome — resources.assets:2545566

Fonte canônica: `eventos.json#/eventos/170`. GUID real: `256779e1-0d70-40a6-9aea-65054cf58c0a`. Resource: `["events/cursed tome - battle 2"]`. Objeto SHA-256: `ac5bb95bbd9ec9b80e9efc5b2f65c245652ebc7c6967e4af4cc24c8eb046b757`.

Categoria=NotInEventPool; raridade=Common (0); peso=1.0; disabled=0; EditorOnly=0. 2 opções / 2 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 0, "allowedNodeTypes": [7], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 0, "allowedTimeOfDay": 1, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [0, 4, 3, 5], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 1}`

Textos vazios inventariados: 1. `$.texto_resultados_possiveis=""`

Opção 1 (Read on): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`true`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 2545567}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`
Opção 2 (Leave): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 2/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 2/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`

Referências de entrada encontradas: 2 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545569` (PartyEvent, Cursed Tome), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[36]`.

Referências PPtr NÃO nulas do objeto original: 2; resolvidas no catálogo: 2. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent` → `resources.assets:2545567`: Cursed Tome - Battle 3 / PartyEvent; resolvida=True.

Campos NULL na projeção sem duplicação: 18. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (8 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`, `$.opcoes[1].efeitos[0].batalha.referencia.chave`, `$.opcoes[1].efeitos[0].batalha.referencia.nome`, `$.opcoes[1].efeitos[0].evento_encadeado.chave`, `$.opcoes[1].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (2 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`, `$.opcoes[1].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `opcoes[0].texto` ATUAL: `"Continue to read from the <incr><indigo><b>Cursed Tome</b></indigo></incr>."`
  PROPOSTA EXATA COMPLETA: `"Continue to read from the <incr><indigo><b>Cursed Tome</b></indigo></incr> and face another battle."`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 11 — Cursed Tome — resources.assets:2545567

Fonte canônica: `eventos.json#/eventos/171`. GUID real: `1f424434-f6b6-4a63-af9d-3880c5a2f9a2`. Resource: `["events/cursed tome - battle 3"]`. Objeto SHA-256: `5e6f783e4baa139b8ed7d02fbfe37e8946cb516267cdc20df2067ece73119cc1`.

Categoria=NotInEventPool; raridade=Common (0); peso=1.0; disabled=0; EditorOnly=0. 2 opções / 2 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 0, "allowedNodeTypes": [7], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 0, "allowedTimeOfDay": 1, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [0, 4, 3, 5], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 1}`

Textos vazios inventariados: 1. `$.texto_resultados_possiveis=""`

Opção 1 (Read on): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`true`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=3; VictoryEvent=`{"m_FileID": 0, "m_PathID": 2545568}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`
Opção 2 (Leave): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 2/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 2/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`

Referências de entrada encontradas: 2 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545566` (PartyEvent, Cursed Tome), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[37]`.

Referências PPtr NÃO nulas do objeto original: 8; resolvidas no catálogo: 8. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[0].CharacterInfo` → `resources.assets:2548224`: Undead Wizard / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[0].ForcedEnemyMods[0]` → `resources.assets:2545360`: Undying / EnemyMod; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[1].CharacterInfo` → `resources.assets:2548222`: Undead Berserker / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[1].ForcedEnemyMods[0]` → `resources.assets:2545360`: Undying / EnemyMod; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[2].CharacterInfo` → `resources.assets:2548223`: Undead Ranger / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[2].ForcedEnemyMods[0]` → `resources.assets:2545360`: Undying / EnemyMod; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent` → `resources.assets:2545568`: Cursed Tome - Victory / PartyEvent; resolvida=True.

Campos NULL na projeção sem duplicação: 18. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (8 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`, `$.opcoes[1].efeitos[0].batalha.referencia.chave`, `$.opcoes[1].efeitos[0].batalha.referencia.nome`, `$.opcoes[1].efeitos[0].evento_encadeado.chave`, `$.opcoes[1].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (2 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`, `$.opcoes[1].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `opcoes[0].texto` ATUAL: `"Finish what you've started. "`
  PROPOSTA EXATA COMPLETA: `"Finish what you've started and face the undead champions."`
- `opcoes[0].efeitos[0].texto` ATUAL: `"Unyielding in your resolve, you continue to read aloud from the cursed tome, its words resonating with a power that transcendes the mortal realm.\n\nGrotesque specters of a bygone age appear, hungering for the living, their eyes empty voids of malice."`
  PROPOSTA EXATA COMPLETA: `"Unyielding in your resolve, you continue to read aloud from the cursed tome, its words resonating with a power that transcends the mortal realm.\n\nGrotesque specters of a bygone age appear, hungering for the living, their eyes empty voids of malice."`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 12 — Cursed Tome — resources.assets:2545568

Fonte canônica: `eventos.json#/eventos/172`. GUID real: `08293297-072b-415d-abf0-f966e0c6645f`. Resource: `["events/cursed tome - victory"]`. Objeto SHA-256: `5bdb8b540a78bd8a33e5213326ec8fc45cd17d4cba0f0ac4be5cb77d941ca2c9`.

Categoria=NotInEventPool; raridade=Common (0); peso=1.0; disabled=0; EditorOnly=0. 1 opções / 1 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 0, "allowedNodeTypes": [7], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 0, "allowedTimeOfDay": 1, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [0, 4, 3, 5], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 1}`

Textos vazios inventariados: 1. `$.texto_resultados_possiveis=""`

Opção 1 (Take): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=3; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [{"chave": "resources.assets:2545457", "nome": "Necronomicon", "pptr": {"m_FileID": 0, "m_PathID": 2545457}, "tipo": "EventStatus", "descricao": "<i><color=#808080>You carry the Necronomicon!</i></color> \n\nChanges your @Skeletal Summons@ into something... stronger. Increases Summon Damage and Health by {5,25}%", "duracao": {"valor": 3, "nome": "Permanent"}, "status_tipo": {"valor": 1, "nome": "Fortune"}, "modificadores": [{"atributo": {"chave": "resources.assets:2544568", "nome": "SummonDamageMod", "pptr": {"m_FileID": 0, "m_PathID": 2544568}, "tipo": "CharacterAttribute"}, "metodo": {"valor": 0, "nome": "Base"}, "expressao": "{5,25}", "segunda_passagem": false}, {"atributo": {"chave": "resources.assets:2544572", "nome": "SummonHealthMod", "pptr": {"m_FileID": 0, "m_PathID": 2544572}, "tipo": "CharacterAttribute"}, "metodo": {"valor": 0, "nome": "Base"}, "expressao": "{5,25}", "segunda_passagem": false}]}], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`

Referências de entrada encontradas: 2 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545567` (PartyEvent, Cursed Tome), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[38]`.

Referências PPtr NÃO nulas do objeto original: 5; resolvidas no catálogo: 5. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[0].CharacterInfo` → `resources.assets:2548224`: Undead Wizard / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[1].CharacterInfo` → `resources.assets:2548222`: Undead Berserker / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[2].CharacterInfo` → `resources.assets:2548223`: Undead Ranger / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].EventActionEffects[0].eventStatuses[0]` → `resources.assets:2545457`: Necronomicon / EventStatus; resolvida=True.

Campos NULL na projeção sem duplicação: 9. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (4 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (1 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `texto` ATUAL: `"Your valor and cunning prevaile over the darkness you had summoned. As the undead champions crumbled into dust, their forms dispersing into nothingness, a surge of power courses through you. You have harnessed the very essence of the <indigo><b><incr>Necronomicon</incr></b></indigo>."`
  PROPOSTA EXATA COMPLETA: `"Your valor and cunning prevail over the darkness you had summoned. As the undead champions crumbled into dust, their forms dispersing into nothingness, a surge of power courses through you. You have harnessed the very essence of the <indigo><b><incr>Necronomicon</incr></b></indigo>."`
- `campos_originais.promptToSelectCharacter` ATUAL: `"Who will take the <indigo><b><incr>Necronomicon</indigo></b></incr> and gain [o1a1_status]?"`
  PROPOSTA EXATA COMPLETA: `"Who will take the <indigo><b><incr>Necronomicon</incr></b></indigo> and gain [o1a1_status]?"`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 13 — Dark Discoveries — resources.assets:2545571

Fonte canônica: `eventos.json#/eventos/173`. GUID real: `32b5d67b-797e-4a2e-8af6-1b2ee1e1b4c7`. Resource: `["events/dark discoveries - victory"]`. Objeto SHA-256: `a3e23b1b2515801f536a2e0b4a1e8789e6f5d20ab382d5b218db8085655eac4a`.

Categoria=NotInEventPool; raridade=Common (0); peso=1.0; disabled=0; EditorOnly=0. 1 opções / 1 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 0, "allowedNodeTypes": [7], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 1, "allowedTimeOfDay": 0, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 1}`

Textos vazios inventariados: 2. `$.texto_resultados_possiveis=""`; `$.campos_originais.characterSelectedText=""`

Opção 1 (Accept): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [{"chave": "resources.assets:2545485", "nome": "Unholy Sacrifice", "pptr": {"m_FileID": 0, "m_PathID": 2545485}, "tipo": "EventStatus", "descricao": "Grants the skill @Unholy Sacrifice@. Increases @Shadow Damage@ by {6,30}%.", "duracao": {"valor": 3, "nome": "Permanent"}, "status_tipo": {"valor": 1, "nome": "Fortune"}, "modificadores": [{"atributo": {"chave": "resources.assets:2544381", "nome": "DamageModShadow", "pptr": {"m_FileID": 0, "m_PathID": 2544381}, "tipo": "CharacterAttribute"}, "metodo": {"valor": 0, "nome": "Base"}, "expressao": "{6,30}", "segunda_passagem": false}]}], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`

Referências de entrada encontradas: 2 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545570` (PartyEvent, Unholy Experiments), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[41]`.

Referências PPtr NÃO nulas do objeto original: 2; resolvidas no catálogo: 2. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].EventActionEffects[0].eventStatuses[0]` → `resources.assets:2545485`: Unholy Sacrifice / EventStatus; resolvida=True.

Campos NULL na projeção sem duplicação: 9. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (4 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (1 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `texto` ATUAL: `"Having vanquished the abominations <blue><b><incr>The Necromancer</incr></b></blue> greets you:\n\n\"You have returned the souls of the damned to me. As agreed, I shall be your mentor, guiding your steps through the perilous realm of necromancy. But it will be your hearts, your intentions, that shall determine the outcome. The power itself is neither good nor evil—it is how it is wielded that defines its nature.\""`
  PROPOSTA EXATA COMPLETA: `"After you vanquish the abominations, <blue><b><incr>The Necromancer</incr></b></blue> greets you:\n\n\"You have returned the souls of the damned to me. As agreed, I shall be your mentor, guiding your steps through the perilous realm of necromancy. But it will be your hearts, your intentions, that shall determine the outcome. The power itself is neither good nor evil—it is how it is wielded that defines its nature.\""`
- `opcoes[0].efeitos[0].texto` ATUAL: `"Under the guidance of the Necromancer, you delve into the intricacies of necromantic spells, learning to harness the raw power that lay hidden within the realm of the dead.\r"`
  PROPOSTA EXATA COMPLETA: `"Under the guidance of the Necromancer, you delve into the intricacies of necromantic spells, learning to harness the raw power that lies hidden within the realm of the dead.\r"`
- `campos_originais.promptToSelectCharacter` ATUAL: `"Who will learn the Dark Ritual?"`
  PROPOSTA EXATA COMPLETA: `"Who will learn Unholy Sacrifice?"`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 14 — Desecrated Statue of the First Mountain King — resources.assets:2545574

Fonte canônica: `eventos.json#/eventos/174`. GUID real: `ff5a1efb-7689-4e82-99b2-0bda947a8f47`. Resource: `["events/desecrated statue of the first mountain king - victory"]`. Objeto SHA-256: `64131e410a2785a4e444aee18134009eea7cfbe6e771ffc18106424838b53f1c`.

Categoria=NotInEventPool; raridade=Mythic (4); peso=1.0; disabled=0; EditorOnly=0. 1 opções / 1 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 1, "allowedNodeTypes": [], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 1, "allowedTimeOfDay": 0, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [], "KeepInDeckWhenUsed": 1, "isLesserEvent": 0, "LeadsToFortune": 1}`

Textos vazios inventariados: 2. `$.texto_resultados_possiveis=""`; `$.campos_originais.characterSelectedText=""`

Opção 1 (Accept): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=2; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [{"chave": "resources.assets:2545410", "nome": "Blessing of the Mountain", "pptr": {"m_FileID": 0, "m_PathID": 2545410}, "tipo": "EventStatus", "descricao": "Grants a 50% chance to resist any control effects.  Increases @Max Health@ by {15,30}%.\n\n<i><color=#808080>Enough is enough!</i></color>\n", "duracao": {"valor": 1, "nome": "Quest"}, "status_tipo": {"valor": 1, "nome": "Fortune"}, "modificadores": [{"atributo": {"chave": "resources.assets:2544554", "nome": "StatusResistImpairment", "pptr": {"m_FileID": 0, "m_PathID": 2544554}, "tipo": "CharacterAttribute"}, "metodo": {"valor": 0, "nome": "Base"}, "expressao": "{50, 50}", "segunda_passagem": false}, {"atributo": {"chave": "resources.assets:2544436", "nome": "MaxHealth", "pptr": {"m_FileID": 0, "m_PathID": 2544436}, "tipo": "CharacterAttribute"}, "metodo": {"valor": 1, "nome": "Percentage"}, "expressao": "{15,30}", "segunda_passagem": true}]}], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`

Referências de entrada encontradas: 2 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545575` (PartyEvent, Gold Lootin' Goblins), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[44]`.

Referências PPtr NÃO nulas do objeto original: 6; resolvidas no catálogo: 6. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[0].CharacterInfo` → `resources.assets:2545226`: Volcanic Titan / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[0].ForcedEnemyMods[0]` → `resources.assets:2545325`: Burning / EnemyMod; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[1].CharacterInfo` → `resources.assets:2545226`: Volcanic Titan / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[1].ForcedEnemyMods[0]` → `resources.assets:2545325`: Burning / EnemyMod; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].EventActionEffects[0].eventStatuses[0]` → `resources.assets:2545410`: Blessing of the Mountain / EventStatus; resolvida=True.

Campos NULL na projeção sem duplicação: 9. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (4 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (1 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `campos_originais.promptToSelectCharacter` ATUAL: `"Who will listen to his pleas?"`
  PROPOSTA EXATA COMPLETA: `"Who will receive the Blessing of the Mountain?"`
- `opcoes[0].texto` ATUAL: `"Take the Blessing."`
  PROPOSTA EXATA COMPLETA: `"Receive the Blessing of the Mountain for this quest."`
- `opcoes[0].efeitos[0].texto` ATUAL: `"You are filled with a fiery passion for battle and the frothy embrace of ale. It burns within your very being, igniting your spirit with a fierce determination and an insatiable thirst for both victory and merriment."`
  PROPOSTA EXATA COMPLETA: `"The Blessing of the Mountain fills you with the King's resolve, strengthening your body and helping you resist control effects."`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 15 — Enchanted Pumpkin Patch — resources.assets:2545586

Fonte canônica: `eventos.json#/eventos/175`. GUID real: `9b40c53e-d59b-443b-a06b-4f5719f4666a`. Resource: `["events/enchanted pumpkin patch - victory"]`. Objeto SHA-256: `2fff85fce3566b883f70b8f6c78682b93a5e78b73399ade2bb98e7b650282907`.

Categoria=NotInEventPool; raridade=Rare (2); peso=1.0; disabled=0; EditorOnly=0. 1 opções / 1 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 0, "allowedNodeTypes": [7], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 0, "allowedTerrainTypes": [2], "allowAtAllTimesOfDay": 1, "allowedTimeOfDay": 1, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [2, 0, 3, 5], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 1}`

Textos vazios inventariados: 1. `$.texto_resultados_possiveis=""`

Opção 1 (Take): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": "resources.assets:2544645", "nome": "Cursed Chest Battle", "pptr": {"m_FileID": 0, "m_PathID": 2544645}, "tipo": "BattleInfo"}`; inimigos forçados=1; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 2.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [0, 1, 2, 3, 4, 5], "limitItemRarities": 0, "possibleRarities": [2, 3, 4]}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [{"chave": "resources.assets:2545436", "nome": "Enchanted Pumpkin", "pptr": {"m_FileID": 0, "m_PathID": 2545436}, "tipo": "EventStatus", "descricao": "Gain [0] Health and Mana each turn.\n\n<i><color=#808080>There is an intoxicating aroma about it. It smells of autumn nights and whispered tales around a fire, of ancient magic and timeless tales.</color></i>\n", "duracao": {"valor": 3, "nome": "Permanent"}, "status_tipo": {"valor": 1, "nome": "Fortune"}, "modificadores": [{"atributo": {"chave": "resources.assets:2544426", "nome": "HealthPerTurn", "pptr": {"m_FileID": 0, "m_PathID": 2544426}, "tipo": "CharacterAttribute"}, "metodo": {"valor": 0, "nome": "Base"}, "expressao": "12", "segunda_passagem": false}, {"atributo": {"chave": "resources.assets:2544431", "nome": "ManaPerTurn", "pptr": {"m_FileID": 0, "m_PathID": 2544431}, "tipo": "CharacterAttribute"}, "metodo": {"valor": 0, "nome": "Base"}, "expressao": "12", "segunda_passagem": false}]}], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`

Referências de entrada encontradas: 2 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545587` (PartyEvent, Enchanted Pumpkin Patch), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[56]`.

Referências PPtr NÃO nulas do objeto original: 4; resolvidas no catálogo: 4. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battle` → `resources.assets:2544645`: Cursed Chest Battle / BattleInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[0].CharacterInfo` → `resources.assets:2545119`: The Scarecrow / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].EventActionEffects[0].eventStatuses[0]` → `resources.assets:2545436`: Enchanted Pumpkin / EventStatus; resolvida=True.

Campos NULL na projeção sem duplicação: 7. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (1 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (2 campos): `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `campos_originais.promptToSelectCharacter` ATUAL: `"Dare to open the Cursed Chest?"`
  PROPOSTA EXATA COMPLETA: `"Who will claim an Enchanted Pumpkin?"`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 16 — Foreboding Gem - Victory — resources.assets:2545594

Fonte canônica: `eventos.json#/eventos/176`. GUID real: `46d77b69-0a9f-4d25-bc2d-15e6745c120b`. Resource: `["events/foreboding gem - victory"]`. Objeto SHA-256: `44dd80410dcef98eba00f0341a94ae3713b0ab61a434dd4563506f53264c43f7`.

Categoria=NotInEventPool; raridade=Common (0); peso=1.0; disabled=0; EditorOnly=0. 1 opções / 1 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 0, "allowedNodeTypes": [7], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 1, "allowedTimeOfDay": 0, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 1}`

Textos vazios inventariados: 3. `$.texto_resultados_possiveis=""`; `$.campos_originais.promptToSelectCharacter=""`; `$.campos_originais.characterSelectedText=""`

Opção 1 (Take): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [{"chave": "resources.assets:2545465", "nome": "Ruby of Rancor", "pptr": {"m_FileID": 0, "m_PathID": 2545465}, "tipo": "EventStatus", "descricao": "Grants 1 charge of Ruby of Rancor: Grants 3 extra Action Points and reduces Mana Costs. Die at the end of your turn.\n\n<i><color=#808080>The gem seems to hum in your grasp, as if resonating with your heartbeat, its pulses syncing with your own.</color></i>", "duracao": {"valor": 3, "nome": "Permanent"}, "status_tipo": {"valor": 1, "nome": "Fortune"}, "modificadores": []}], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`

Referências de entrada encontradas: 2 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545595` (PartyEvent, Foreboding Gem), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[64]`.

Referências PPtr NÃO nulas do objeto original: 5; resolvidas no catálogo: 5. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.EnemyStatusApplications[0].ActionStatusPool[0]` → `resources.assets:2543476`: Ruby Rancor Enemy / ActionStatusInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ovrEnemyStatusRefList[0]` → `resources.assets:2543476`: Ruby Rancor Enemy / ActionStatusInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].EventActionEffects[0].eventStatuses[0]` → `resources.assets:2545465`: Ruby of Rancor / EventStatus; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].EventActionEffects[0].rolledEventStatuses[0]` → `resources.assets:2545439`: Ethereal / EventStatus; resolvida=True.

Campos NULL na projeção sem duplicação: 9. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (4 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (1 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `texto` ATUAL: `"Finally, after what seems like an eternity of battling shadows, you emerge victorious. Your opponents lay strewn around you, their madness extinguished, replaced by a vacant stare. They had been driven to the edge by the ruby, the allure too strong, the pull too intoxicating.\n\nCarefully, you approach the pedestal, the <red><b><incr>Ruby</incr></b></red> pulsating with an ethereal light. The gem is yours for the taking, the fruits of a hard-won battle."`
  PROPOSTA EXATA COMPLETA: `"Finally, after what seems like an eternity of battling shadows, you emerge victorious. Your opponents lie strewn around you, their madness extinguished, replaced by a vacant stare. They had been driven to the edge by the ruby, the allure too strong, the pull too intoxicating.\n\nCarefully, you approach the pedestal, the <red><b><incr>Ruby</incr></b></red> pulsating with an ethereal light. The gem is yours for the taking, the fruits of a hard-won battle."`
- `opcoes[0].texto` ATUAL: `"You'll be the one to hold the Ruby."`
  PROPOSTA EXATA COMPLETA: `"Claim Ruby of Rancor. Its charge grants 3 extra Action Points and reduces Mana Costs, but its effect makes you die at the end of your turn."`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 17 — Gold Lootin' Goblins — resources.assets:2545575

Fonte canônica: `eventos.json#/eventos/177`. GUID real: `ca065336-aaaa-409a-826a-8d1b523acc5b`. Resource: `["events/desecrated statue of the first mountain king battle"]`. Objeto SHA-256: `8998a59aa658e552a975a848eb0fcc9c71cb993b96e3af49013c09534621851f`.

Categoria=NotInEventPool; raridade=Common (0); peso=1.0; disabled=0; EditorOnly=0. 2 opções / 2 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 1, "allowedNodeTypes": [], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 1, "allowedTimeOfDay": 0, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [], "KeepInDeckWhenUsed": 1, "isLesserEvent": 0, "LeadsToFortune": 1}`

Textos vazios inventariados: 3. `$.texto_resultados_possiveis=""`; `$.campos_originais.characterSelectedText=""`; `$.opcoes[1].texto=""`

Opção 1 (Fight): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`true`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=6; VictoryEvent=`{"m_FileID": 0, "m_PathID": 2545574}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`
Opção 2 (Leave): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 2/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 2/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`

Referências de entrada encontradas: 2 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545511` (EventStatus, Dwarf Rage!), `data.ForcedEventBeforeBoss`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[45]`.

Referências PPtr NÃO nulas do objeto original: 14; resolvidas no catálogo: 14. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[0].CharacterInfo` → `resources.assets:2545180`: Pale Witch Doctor / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[0].ForcedEnemyMods[0]` → `resources.assets:2545324`: Berserking / EnemyMod; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[1].CharacterInfo` → `resources.assets:2545178`: Pale Ranger / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[1].ForcedEnemyMods[0]` → `resources.assets:2545324`: Berserking / EnemyMod; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[2].CharacterInfo` → `resources.assets:2545179`: Pale Warrior / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[2].ForcedEnemyMods[0]` → `resources.assets:2545324`: Berserking / EnemyMod; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[3].CharacterInfo` → `resources.assets:2545182`: Worg / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[3].ForcedEnemyMods[0]` → `resources.assets:2545324`: Berserking / EnemyMod; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[4].CharacterInfo` → `resources.assets:2545182`: Worg / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[4].ForcedEnemyMods[0]` → `resources.assets:2545324`: Berserking / EnemyMod; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[5].CharacterInfo` → `resources.assets:2545182`: Worg / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[5].ForcedEnemyMods[0]` → `resources.assets:2545324`: Berserking / EnemyMod; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent` → `resources.assets:2545574`: Desecrated Statue of the First Mountain King - Victory / PartyEvent; resolvida=True.

Campos NULL na projeção sem duplicação: 18. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (8 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`, `$.opcoes[1].efeitos[0].batalha.referencia.chave`, `$.opcoes[1].efeitos[0].batalha.referencia.nome`, `$.opcoes[1].efeitos[0].evento_encadeado.chave`, `$.opcoes[1].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (2 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`, `$.opcoes[1].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `texto` ATUAL: `"A band of raucous <b><green><incr>Goblins</incr></green></b> revel in their ill-gotten gains. These mischievous creatures, driven by their insatiable greed, have amassed a collection of treasures that sparkled and gleam in the dim torchlight.\n\nTheir celebration echoes through the caverns, filling the air with a cacophony of cackles, guttural laughter, and discordant songs. The goblins, with their hunched forms and gleaming eyes, danced in a frenzy of glee, their long, spindly fingers clutching their newfound wealth.\n\nThese are undoubtedly the culprits who desecrated the statue of the Mountain King."`
  PROPOSTA EXATA COMPLETA: `"A band of raucous <b><green><incr>Goblins</incr></green></b> revel in their ill-gotten gains. These mischievous creatures, driven by their insatiable greed, have amassed a collection of treasures that sparkle and gleam in the dim torchlight.\n\nTheir celebration echoes through the caverns, filling the air with a cacophony of cackles, guttural laughter, and discordant songs. The goblins, with their hunched forms and gleaming eyes, dance in a frenzy of glee, their long, spindly fingers clutching their newfound wealth.\n\nThese are undoubtedly the culprits who desecrated the statue of the Mountain King."`
- `opcoes[0].texto` ATUAL: `"Destroy these goblins in the name of the First Mountain King"`
  PROPOSTA EXATA COMPLETA: `"Destroy these goblins in the name of the First Mountain King."`
- `opcoes[1].texto` ATUAL: `""`
  PROPOSTA EXATA COMPLETA: `"Leave the goblins and abandon this confrontation."`
- `campos_originais.promptToSelectCharacter` ATUAL: `"Who will listen to his pleas?"`
  PROPOSTA EXATA COMPLETA: `"Who will confront the goblins?"`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 18 — Gold Statue of the First Mountain King — resources.assets:2545600

Fonte canônica: `eventos.json#/eventos/178`. GUID real: `d4f3d443-58a3-4d3d-be7d-e2dcc5edb65c`. Resource: `["events/gold statue of the first mountain king battle victory"]`. Objeto SHA-256: `fa08a4b31a7e48592a6ddfcbd840696e1592f7681a0a951d71d55c7d1d05b02d`.

Categoria=NotInEventPool; raridade=Common (0); peso=1.0; disabled=0; EditorOnly=0. 1 opções / 1 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 0, "allowedNodeTypes": [7], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 1, "allowedTimeOfDay": 1, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [4, 3], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 0}`

Textos vazios inventariados: 3. `$.texto_resultados_possiveis=""`; `$.opcoes[0].texto=""`; `$.opcoes[0].efeitos[0].texto=""`

Opção 1 (Claim the gold): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": true, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 0, "tabelas": [{"mustGetOne": 0, "itemLootChances": [{"ItemInfo": {"m_FileID": 0, "m_PathID": 2546476}, "Chance": 100.0}, {"ItemInfo": {"m_FileID": 0, "m_PathID": 2546477}, "Chance": 100.0}, {"ItemInfo": {"m_FileID": 0, "m_PathID": 2546478}, "Chance": 100.0}]}], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`

Referências de entrada encontradas: 3 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545601` (PartyEvent, Gold Statue of the First Mountain King), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2544646` (BattleInfo, Gold Statue of the First Mountain King Battle), `data.victoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[70]`.

Referências PPtr NÃO nulas do objeto original: 4; resolvidas no catálogo: 4. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].EventActionEffects[0].lootTables[0].itemLootChances[0].ItemInfo` → `resources.assets:2546476`: Gold Statue Arm / ItemInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].EventActionEffects[0].lootTables[0].itemLootChances[1].ItemInfo` → `resources.assets:2546477`: Gold Statue Head / ItemInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].EventActionEffects[0].lootTables[0].itemLootChances[2].ItemInfo` → `resources.assets:2546478`: Gold Statue Torso / ItemInfo; resolvida=True.

Campos NULL na projeção sem duplicação: 9. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (4 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (1 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `texto` ATUAL: `"In the end, the dwarven guard could not stand against you. With a final, valiant cry, the last of the dwarves falls. Silence fills the chamber, the only sound is your own labored breathing. The battle is over. You are victorious. Free to desecrate the sacred statue."`
  PROPOSTA EXATA COMPLETA: `"In the end, the dwarven guard could not stand against you. With a final, valiant cry, the last of the dwarves falls. Silence fills the chamber; the only sound is your own labored breathing. The battle is over. You are victorious. Free to desecrate the sacred statue."`
- `opcoes[0].titulo` ATUAL: `"Claim the gold"`
  PROPOSTA EXATA COMPLETA: `"Claim the statue's spoils"`
- `campos_originais.promptToSelectCharacter` ATUAL: `"Does anyone owe this Ogre money?"`
  PROPOSTA EXATA COMPLETA: `"Who will claim the statue's spoils?"`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 19 — Hell Coffer — resources.assets:2545605

Fonte canônica: `eventos.json#/eventos/179`. GUID real: `f40b4b0b-e070-4566-8cfd-3b2061b83e38`. Resource: `["events/hell coffer victory"]`. Objeto SHA-256: `8c23e375e5759483318a92b0d5403842b5450981011207b9ba87803989ffa281`.

Categoria=NotInEventPool; raridade=Common (0); peso=1.0; disabled=0; EditorOnly=0. 2 opções / 2 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 0, "allowedNodeTypes": [7], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 1, "allowedTimeOfDay": 1, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [4, 3], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 1}`

Textos vazios inventariados: 4. `$.opcoes[0].texto=""`; `$.opcoes[0].efeitos[0].texto=""`; `$.opcoes[1].texto=""`; `$.opcoes[1].efeitos[0].texto=""`

Opção 1 (Enchant Shadow): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [{"chave": "resources.assets:2545435", "nome": "Enchant Shadow", "pptr": {"m_FileID": 0, "m_PathID": 2545435}, "tipo": "EventStatus", "descricao": "Grants @level@ {1,30} Enchant Shadow.\n\n<i><color=#808080>Wreathe your weapon in darkest shadow.</i></color>\n", "duracao": {"valor": 3, "nome": "Permanent"}, "status_tipo": {"valor": 1, "nome": "Fortune"}, "modificadores": []}], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`
Opção 2 (Enchant Holy): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 2/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 2/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [{"chave": "resources.assets:2545434", "nome": "Enchant Holy", "pptr": {"m_FileID": 0, "m_PathID": 2545434}, "tipo": "EventStatus", "descricao": "Grants @level@ {1,30} Enchant Holy.\n\n<i><color=#808080>Brandish your weapon in glorious light.</i></color>\n", "duracao": {"valor": 3, "nome": "Permanent"}, "status_tipo": {"valor": 1, "nome": "Fortune"}, "modificadores": []}], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`

Referências de entrada encontradas: 2 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545606` (PartyEvent, Hell Coffer), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[75]`.

Referências PPtr NÃO nulas do objeto original: 5; resolvidas no catálogo: 5. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].EventActionEffects[0].eventStatuses[0]` → `resources.assets:2545435`: Enchant Shadow / EventStatus; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].EventActionEffects[0].rolledEventStatuses[0]` → `resources.assets:2545467`: Scroll of Monster Summoning / EventStatus; resolvida=True.
- `$.campos_originais.eventOptions[1].eventActions[0].EventActionEffects[0].eventStatuses[0]` → `resources.assets:2545434`: Enchant Holy / EventStatus; resolvida=True.
- `$.campos_originais.eventOptions[1].eventActions[0].EventActionEffects[0].rolledEventStatuses[0]` → `resources.assets:2545432`: Elixir of the Scarlet Ox / EventStatus; resolvida=True.

Campos NULL na projeção sem duplicação: 18. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (2 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`, `$.opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (8 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`, `$.opcoes[1].efeitos[0].batalha.referencia.chave`, `$.opcoes[1].efeitos[0].batalha.referencia.nome`, `$.opcoes[1].efeitos[0].evento_encadeado.chave`, `$.opcoes[1].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (2 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`, `$.opcoes[1].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `texto` ATUAL: `"Finally, the last of the fiery damned falls, its form collapsing into embers that quickly fade away. The <red><b><incr>Hell Coffer</incr></b></red>, once spinning with the force of a maelstrom, slows finally coming to a stop. A soft click echos as it unlocks, revealing its treasures to the victorious."`
  PROPOSTA EXATA COMPLETA: `"Finally, the last of the fiery damned falls, its form collapsing into embers that quickly fade away. The <red><b><incr>Hell Coffer</incr></b></red>, once spinning with the force of a maelstrom, slows, finally coming to a stop. A soft click echoes as it unlocks, revealing its treasures to the victorious."`
- `campos_originais.promptToSelectCharacter` ATUAL: `"Does anyone owe this Ogre money?"`
  PROPOSTA EXATA COMPLETA: `"Who will receive the chosen enchantment?"`
- `opcoes[0].texto` ATUAL: `""`
  PROPOSTA EXATA COMPLETA: `"Gain Enchant Shadow."`
- `opcoes[1].texto` ATUAL: `""`
  PROPOSTA EXATA COMPLETA: `"Gain Enchant Holy."`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 20 — Hell Gate — resources.assets:2545607

Fonte canônica: `eventos.json#/eventos/180`. GUID real: `a0c8980b-0e39-42fe-bdba-f9570b2ce256`. Resource: `["events/hell gate - victory"]`. Objeto SHA-256: `56a0917dc255a6ed69fd80d04ab8b21be5a6aea7197282e3511482850690194c`.

Categoria=NotInEventPool; raridade=Common (0); peso=1.0; disabled=0; EditorOnly=0. 1 opções / 1 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 0, "allowedNodeTypes": [7], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 1, "allowedTimeOfDay": 0, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 1}`

Textos vazios inventariados: 3. `$.texto_resultados_possiveis=""`; `$.campos_originais.characterSelectedText=""`; `$.opcoes[0].efeitos[0].texto=""`

Opção 1 (Claim): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=1; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [{"chave": "resources.assets:2545472", "nome": "Soul of Fire", "pptr": {"m_FileID": 0, "m_PathID": 2545472}, "tipo": "EventStatus", "descricao": "Gain {6,30}% Increased Fire Damage. Your stacks of Heat now reduce Healing Received by 5% per stack.\n\n<i><color=#808080>The burning soul of Lord Infernicus!</color></i>\n", "duracao": {"valor": 3, "nome": "Permanent"}, "status_tipo": {"valor": 1, "nome": "Fortune"}, "modificadores": [{"atributo": {"chave": "resources.assets:2544377", "nome": "DamageModFire", "pptr": {"m_FileID": 0, "m_PathID": 2544377}, "tipo": "CharacterAttribute"}, "metodo": {"valor": 0, "nome": "Base"}, "expressao": "{6,30}", "segunda_passagem": false}, {"atributo": {"chave": "resources.assets:2544625", "nome": "SoulOfFire", "pptr": {"m_FileID": 0, "m_PathID": 2544625}, "tipo": "CharacterAttribute"}, "metodo": {"valor": 4, "nome": "Set"}, "expressao": "{1, 1}", "segunda_passagem": false}]}], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`

Referências de entrada encontradas: 2 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545608` (PartyEvent, Hell Gate), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[77]`.

Referências PPtr NÃO nulas do objeto original: 3; resolvidas no catálogo: 3. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.ForcedEnemies[0].CharacterInfo` → `resources.assets:2545159`: Lord Infernicus / CharacterInfo; resolvida=True.
- `$.campos_originais.eventOptions[0].eventActions[0].EventActionEffects[0].eventStatuses[0]` → `resources.assets:2545472`: Soul of Fire / EventStatus; resolvida=True.

Campos NULL na projeção sem duplicação: 9. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (4 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (1 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `campos_originais.promptToSelectCharacter` ATUAL: `"Who if any will take his soul?"`
  PROPOSTA EXATA COMPLETA: `"Who will take his soul?"`
- `opcoes[0].texto` ATUAL: `"Take the <red><b><incr>Soul of Lord Infernicus</incr></b></red>."`
  PROPOSTA EXATA COMPLETA: `"Take the <red><b><incr>Soul of Lord Infernicus</incr></b></red> and gain Soul of Fire. It increases Fire Damage, but each stack of Heat reduces Healing Received by 5%."`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

### 21 — Horn of Glorious Battle — resources.assets:2545610

Fonte canônica: `eventos.json#/eventos/181`. GUID real: `8efe225e-a0d9-40ad-925a-44c3a953f52c`. Resource: `["events/horn of glorious battle - victory"]`. Objeto SHA-256: `c01804994cf564b613495af7eb8f675e746938238d312f962bbbe738749939db`.

Categoria=NotInEventPool; raridade=Common (0); peso=1.0; disabled=0; EditorOnly=0. 1 opções / 1 ações. Modos: `[{"valor": 0, "nome": "Campaign"}, {"valor": 1, "nome": "Roguelike"}]`; historia: `{"valor": 0, "nome": "NonStoryOnly"}`; full_release: `{"valor": 0, "nome": "None"}`.

Condições serializadas (não disponibilidade comprovada): `{"disabled": 0, "EditorOnly": 0, "allowOnAllNodeTypes": 0, "allowedNodeTypes": [7], "requiredStatusesToSpawn": [], "allowOnAllTerrainTypes": 1, "allowedTerrainTypes": [], "allowAtAllTimesOfDay": 1, "allowedTimeOfDay": 0, "allowAtAllLevels": 1, "minLevel": 1, "terrainTypesAllowedAtAnyTime": [], "KeepInDeckWhenUsed": 0, "isLesserEvent": 0, "LeadsToFortune": 0}`

Textos vazios inventariados: 3. `$.texto_resultados_possiveis=""`; `$.campos_originais.characterSelectedText=""`; `$.opcoes[0].texto=""`

Opção 1 (Victory): condições `{"status_requeridos": [], "ocultar_sem_requisitos": false, "ocultar_se_status": []}`; flags especiais `{"hideOptionEffectText": 0, "openSkillRerollMenu": 0, "levelUpFortunesToCharacterLevel": 0}`; rolagem `{"bonus": [], "misteriosa": false, "texto_misterioso": ""}`. Visibilidade efetiva NAO_EXERCITADO.
Ação 1/1: resultado `{"valor": 0, "nome": "Success"}`; limite=0; iniciar batalha=`false`; manual=`false`; referência=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`; inimigos forçados=0; VictoryEvent=`{"m_FileID": 0, "m_PathID": 0}`; FailureEvent=`{"m_FileID": 0, "m_PathID": 0}`; encadeado=`{"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}`.
Efeito 1/1/PADRÃO/1 — CONFIGURAÇÃO, não resultado de partida: `{"vida_mana": {"percentMaxHealth": 0.0, "percentMaxMana": 0.0, "percentCurHealth": 0.0, "percentCurMana": 0.0}, "alvo": {"override": false, "tipo_override": {"valor": 0, "nome": "Self"}, "tipo_default_serializado": {"valor": 0, "nome": "Self"}}, "recompensas": {"ouro": {"dar": false, "retirar": false, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."}, "experiencia": {"dar": true, "razao": 1.0, "quantidade_final": null, "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."}, "itens": {"dar": false, "pool_tipo": {"valor": 2, "nome": "Unassigned"}, "quantidade_configurada": 1, "tabelas": [], "restricoes": {"limitItemTypes": 0, "possibleItemTypes": [], "limitItemRarities": 0, "possibleRarities": []}, "sorteio_final": null, "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."}, "status": {"candidatos": [], "sortear": false, "quantidade_sorteada_configurada": 1, "resultado_sorteado": null, "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."}, "skills": []}, "remocoes_status": []}`

Referências de entrada encontradas: 2 (inclui ListHolderEvents e resíduos).
- `resources.assets:2545611` (PartyEvent, Horn of Glorious Battle), `campos_originais.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent`.
- `resources.assets:2547145` (ListHolderEvents, ListHolderEvents), `data.Events[80]`.

Referências PPtr NÃO nulas do objeto original: 1; resolvidas no catálogo: 1. m_FileID=0 é resolvido no arquivo resources.assets; externos usam external:file:path.
- `$.campos_originais.m_Script` → `external:1:1910`: None / None; resolvida=True.

Campos NULL na projeção sem duplicação: 9. Motivo literal do contêiner:
- Motivo: Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final`.
- Motivo: Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final`.
- Motivo: EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final`.
- Motivo: Configuração de candidatos preservada; resultado da partida não exercitado. (1 campos): `$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado`.
- Motivo: PPtr serializado com m_PathID=0 (referência nula no asset). (4 campos): `$.opcoes[0].efeitos[0].batalha.referencia.chave`, `$.opcoes[0].efeitos[0].batalha.referencia.nome`, `$.opcoes[0].efeitos[0].evento_encadeado.chave`, `$.opcoes[0].efeitos[0].evento_encadeado.nome`.
- Motivo: Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado. (1 campos): `$.opcoes[0].efeitos[0].batalha.dados_recompensa_final`.

Campos completos afetados pelas propostas (strings JSON preservam controles e espaços):

- `texto` ATUAL: `"Victory was hard-won and bittersweet. The cavern floor is littered with fallen foes, and you bare numerous injuries. But you are alive, and have proven yourself against a horde of summoned enemies. You have faced the call of the battle and emerged victorious."`
  PROPOSTA EXATA COMPLETA: `"Victory was hard-won and bittersweet. The cavern floor is littered with fallen foes, and you bear numerous injuries. But you are alive, and have proven yourself against a horde of summoned enemies. You have faced the call of the battle and emerged victorious."`
- `opcoes[0].efeitos[0].texto` ATUAL: `"Victory has left you sharper, stronger, and  more experienced. "`
  PROPOSTA EXATA COMPLETA: `"Victory has left you sharper, stronger, and more experienced."`
- `campos_originais.promptToSelectCharacter` ATUAL: `"Who will listen to his pleas?"`
  PROPOSTA EXATA COMPLETA: `"Who will claim the victory reward?"`

Aprovação do dono: PENDENTE. Recompensa/condição: MANTER. Runtime/UI/resultado final: NAO_EXERCITADO.

## Prova de fontes e validação

Fontes lidas, não modificadas. SHA-256 de cada arquivo:
- `C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-NotInEventPool-v2.md`: `72c4ddba4ae8bf4bc50371bf2b207d26abff4525f4d79e7585c801beb37396e9`.
- `C:/dev/stolen-realm/docs/cobertura/EV-R1/eventos.json`: `4a8decac7e98a2b0bf8692057a57789a71b94c230e3b9ca93817f039c86d1d13`.
- `C:/dev/stolen-realm/docs/cobertura/EV-R1/eventos.schema.json`: `6950ec43deba94143150f0584bb87ca5406b3ef16f1ae2f18ad8aa943a62b3bc`.
- `C:/dev/stolen-realm/docs/cobertura/EV-R1/schema.md`: `a4e62045c51a57bd0eb3084a8c1fb8534b4bfc6303fe38e4a6896e1a96d34cfb`.
- `C:/dev/stolen-realm/docs/cobertura/EV-R1/catalogo-referencias.json`: `94077cc887621933abe7bbbbd96e91c5a887478dba8fd000b8f4a4129c3745a5`.

O verificador `validar.py` confere 84 seções, as primeiras 21 chaves em ordem, metadados, 3×7 propostas, trechos literais atuais, unicidade de substituição, ausência de mudança de recompensa/condição, preservação de placeholders/tags (exceto a correção explícita de fechamento do prompt do evento 12), NULL com motivo, referências e hashes das fontes. Log real em `docs/automacao/EV-R2-FORAPOOL-b01-validacao.json`; não confundir PASS documental com teste do jogo.

Entrega: 4 partes Markdown; partes01–03 = 21 propostas; parte04 = 21 registros de auditoria. Todas seguem PENDENTE; nenhuma aprovação nem implementação automática.
