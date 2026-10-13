# EV-R2-FORAPOOL-b02 — parte 02, eventos 22–28

Fontes: `C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-NotInEventPool-v2.md`, `eventos.json`, `eventos.schema.json`, `schema.md` e `catalogo-referencias.json`. Coordenadas `opcoes/0` e `efeitos/0` são índices JSON base zero; títulos Opção 1/Ação 1 são base um. Strings JSON exibem os controles originais. Cada proposta é PENDENTE, não uma decisão do dono. Recompensa/condição: MANTER, sem alteração; aplicação runtime: NAO_EXERCITADO (tarefa offline, sem jogo).


## 22. Jack in the Box — resources.assets:2545613

Chave: `resources.assets:2545613`. GUID real: `829367c4-e662-483a-8be7-ba402d121e10`. Asset: `Jack in the Box - Phase 2`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 2; ações: 2; overrides: 0. Origem: `events/jack in the box - phase 2`.

VEREDITO PROPOSTO: MELHORAR — natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

Corrigir construção inglesa, erro ortográfico e alternância indevida de passado/presente sem mudar o loop nem o combate ao sair.

### Texto atual → proposta exata

Campo: `texto`.

Atual (campo completo):
```json
"Turn after turn, you anticipate the monstrous spring-loaded figure within to burst forth. Yet, the jack-in-the-box defies expectation. With each rotation, the melody continues, chilling your bones and testing your resolve, but the lid remains closed."
```

PROPOSTA EXATA (campo completo):
```json
"Turn after turn, you expect the monstrous spring-loaded figure within to burst forth. Yet, the jack-in-the-box defies expectation. With each rotation, the melody continues, chilling your bones and testing your resolve, but the lid remains closed."
```

Justificativa: Corrigir construção inglesa, erro ortográfico e alternância indevida de passado/presente sem mudar o loop nem o combate ao sair.

Campo: `opcoes/0/texto`.

Atual (campo completo):
```json
"Continue to turn the Crank."
```

PROPOSTA EXATA (campo completo):
```json
"Continue to turn the crank."
```

Justificativa: Corrigir construção inglesa, erro ortográfico e alternância indevida de passado/presente sem mudar o loop nem o combate ao sair.

Campo: `opcoes/1/efeitos/0/texto`.

Atual (campo completo):
```json
"As you move away, the silence shatters. A blast echoes through the castle as the jack-in-the-box explodes open, a riot of colorful confetti eruptes from its depths. Laughter, eerie and cruel, echoes through the halls as the figure within came into view. The Jack was no more.\n\n\nIn its place stands The Jester. A grotesque caricature of what was once a joyful figure, he wears a motley costume of bright colors, each piece patterned with mocking faces. His own face, disturbingly human, bares a twisted smile as his eyes gleam with cruel mirth. A demon in the garb of a clown, he had awaited your departure to reveal his true, horrifying nature, ready to play his wicked games with the trespassers who dared to disturb his rest."
```

PROPOSTA EXATA (campo completo):
```json
"As you move away, the silence shatters. A blast echoes through the castle as the jack-in-the-box explodes open, a riot of colorful confetti erupts from its depths. Laughter, eerie and cruel, echoes through the halls as the figure within comes into view. The Jack is no more.\n\n\nIn its place stands The Jester. A grotesque caricature of what was once a joyful figure, he wears a motley costume of bright colors, each piece patterned with mocking faces. His own face, disturbingly human, bares a twisted smile as his eyes gleam with cruel mirth. A demon in the garb of a clown, he has awaited your departure to reveal his true, horrifying nature, ready to play his wicked games with the trespassers who dared to disturb his rest."
```

Justificativa: Corrigir construção inglesa, erro ortográfico e alternância indevida de passado/presente sem mudar o loop nem o combate ao sair.

### Todos os textos atuais e decisão por campo

`texto` — MELHORAR conforme proposta acima:
```json
"Turn after turn, you anticipate the monstrous spring-loaded figure within to burst forth. Yet, the jack-in-the-box defies expectation. With each rotation, the melody continues, chilling your bones and testing your resolve, but the lid remains closed."
```

`texto_resultados_possiveis` — MANTER:
```json
"What will you do?"
```

`campos_originais/promptToSelectCharacter` — MANTER:
```json
"Who will try and crack the <b><legend><incr>Heavy Safe</b></legend></incr>?"
```

`campos_originais/characterSelectedText` — MANTER:
```json
""
```

`opcoes/0/titulo` — MANTER:
```json
"Crank"
```

`opcoes/0/texto` — MELHORAR conforme proposta acima:
```json
"Continue to turn the Crank."
```

`opcoes/1/titulo` — MANTER:
```json
"Leave"
```

`opcoes/1/texto` — MANTER:
```json
"Give up on this twisted game."
```

`opcoes/0/rolagem/texto_misterioso` — MANTER:
```json
""
```

`opcoes/1/rolagem/texto_misterioso` — MANTER:
```json
""
```

`opcoes/0/efeitos/0/texto` — MANTER:
```json
"As the handle moves, the haunting melody plays, a chilling echo of a once innocent children's tune now twisted by its dark surroundings. The notes hang in the air, shrouded in an eerie suspense."
```

`opcoes/1/efeitos/0/texto` — MELHORAR conforme proposta acima:
```json
"As you move away, the silence shatters. A blast echoes through the castle as the jack-in-the-box explodes open, a riot of colorful confetti eruptes from its depths. Laughter, eerie and cruel, echoes through the halls as the figure within came into view. The Jack was no more.\n\n\nIn its place stands The Jester. A grotesque caricature of what was once a joyful figure, he wears a motley costume of bright colors, each piece patterned with mocking faces. His own face, disturbingly human, bares a twisted smile as his eyes gleam with cruel mirth. A demon in the garb of a clown, he had awaited your departure to reveal his true, horrifying nature, ready to play his wicked games with the trespassers who dared to disturb his rest."
```

### Anomalias, cautelas e limites

- Opção Crank encadeia para a própria chave 2545613: loop autoral, não exclusão ou condição a corrigir nesta proposta.

- Leave inicia combate com referência Battle nula, manual=false, mas ForcedEnemies contém 2545118 e VictoryEvent aponta 2545614. Não declarar combate quebrado nem transformar Leave em saída segura.

- UseRewardModifiers=0; expressões ExpModifier/GoldModifier/LootModifier com TurnCount permanecem literais, sem extrapolar prêmio por número de voltas.

- `disabled=0` é configuração; disponibilidade efetiva NAO_EXERCITADO. Nenhuma remoção/reativação proposta.

- Textos vazios auditados: 3. Campos: `campos_originais/characterSelectedText`, `opcoes/0/rolagem/texto_misterioso`, `opcoes/1/rolagem/texto_misterioso`.

- NULL preservados: 24; motivos por caminho no anexo de auditoria `EV-R2-FORAPOOL-b02-parte05.md`. Inclui projeção redundante de recompensa: não somar como efeitos extras.

- Referências nulas projetadas: 3. Combate/RNG/quantidade final/status aplicado/UI: NAO_EXERCITADO — somente configuração offline disponível.

- Opção 1: ocultar sem requisitos=false; ocultar por status=[]; hideOptionEffectText=0. Exibição real NAO_EXERCITADO.

- Opção 2: ocultar sem requisitos=false; ocultar por status=[]; hideOptionEffectText=1. Exibição real NAO_EXERCITADO.

### Referências consultadas e encadeamentos de entrada

Configurações de candidato não são concessões executadas. Catálogo consultado por chave, sem expandir/editar as definições externas.
```json
{
  "referencias": [
    {
      "campo": "$.opcoes[0].efeitos[0].evento_encadeado",
      "chave": "resources.assets:2545613",
      "nome": "Jack in the Box - Phase 2",
      "tipo_catalogo": "PartyEvent",
      "nome_asset_catalogo": "Jack in the Box - Phase 2",
      "registro_catalogo": true,
      "resumo_catalogo": true
    }
  ],
  "pptrs_nao_nulos": [
    {
      "campo": "$.opcoes[0].efeitos[0].evento_encadeado.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545613
      },
      "chave": "resources.assets:2545613",
      "tipo_catalogo": "PartyEvent",
      "nome_catalogo": "Jack in the Box - Phase 2"
    },
    {
      "campo": "$.opcoes[1].efeitos[0].batalha.override.ForcedEnemies[0].CharacterInfo",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545118
      },
      "chave": "resources.assets:2545118",
      "tipo_catalogo": "CharacterInfo",
      "nome_catalogo": "The Jester"
    },
    {
      "campo": "$.opcoes[1].efeitos[0].batalha.override.VictoryEvent",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545614
      },
      "chave": "resources.assets:2545614",
      "tipo_catalogo": "PartyEvent",
      "nome_catalogo": "Jack in the Box - Victory"
    }
  ],
  "referencias_nulas": [
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.referencia",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.opcoes[1].efeitos[0].batalha.referencia",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.opcoes[1].efeitos[0].evento_encadeado",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    }
  ],
  "referencias_entrada": [
    {
      "fonte": "eventos.json",
      "origem": "resources.assets:2545613",
      "campo": "$.opcoes[0].efeitos[0].evento_encadeado.pptr"
    },
    {
      "fonte": "eventos.json",
      "origem": "resources.assets:2545615",
      "campo": "$.opcoes[0].efeitos[0].evento_encadeado.pptr"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545613",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[0].eventActions[0].chainedEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545615",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[0].eventActions[0].chainedEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[83]"
    }
  ]
}
```

### Condições, modos e configuração completa das ações

```json
{
  "condicoes": {
    "disabled": 0,
    "EditorOnly": 0,
    "allowOnAllNodeTypes": 0,
    "allowedNodeTypes": [
      7
    ],
    "requiredStatusesToSpawn": [],
    "allowOnAllTerrainTypes": 1,
    "allowedTerrainTypes": [],
    "allowAtAllTimesOfDay": 1,
    "allowedTimeOfDay": 0,
    "allowAtAllLevels": 1,
    "minLevel": 1,
    "terrainTypesAllowedAtAnyTime": [],
    "KeepInDeckWhenUsed": 0,
    "isLesserEvent": 0,
    "LeadsToFortune": 1
  },
  "modos": [
    {
      "valor": 0,
      "nome": "Campaign"
    },
    {
      "valor": 1,
      "nome": "Roguelike"
    }
  ],
  "historia": {
    "valor": 0,
    "nome": "NonStoryOnly"
  },
  "full_release": {
    "valor": 0,
    "nome": "None"
  },
  "apresentacao_autoral": {
    "AutoStartBattle": 0,
    "targetType": 0,
    "characterPool": 0,
    "showContinueBtnInsteadOfSingleOption": 0,
    "disableAutoChoose": 0,
    "RefEventStatuses": []
  },
  "opcoes": [
    {
      "indice": 1,
      "condicoes": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      },
      "rolagem": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      },
      "hideOptionEffectText": 0,
      "efeitos": [
        {
          "indice": 1,
          "texto": "As the handle moves, the haunting melody plays, a chilling echo of a once innocent children's tune now twisted by its dark surroundings. The notes hang in the air, shrouded in an eerie suspense.",
          "resultado": {
            "valor": 0,
            "nome": "Success"
          },
          "limite_rolagem": 0,
          "texto_efeitos_manual": [],
          "efeitos": [
            {
              "vida_mana": {
                "percentMaxHealth": 0.0,
                "percentMaxMana": 0.0,
                "percentCurHealth": 0.0,
                "percentCurMana": 0.0
              },
              "alvo": {
                "override": false,
                "tipo_override": {
                  "valor": 2,
                  "nome": "Party"
                },
                "tipo_default_serializado": {
                  "valor": 0,
                  "nome": "Self"
                }
              },
              "recompensas": {
                "ouro": {
                  "dar": false,
                  "retirar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
                },
                "experiencia": {
                  "dar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
                },
                "itens": {
                  "dar": false,
                  "pool_tipo": {
                    "valor": 2,
                    "nome": "Unassigned"
                  },
                  "quantidade_configurada": 1,
                  "tabelas": [],
                  "restricoes": {
                    "limitItemTypes": 0,
                    "possibleItemTypes": [],
                    "limitItemRarities": 0,
                    "possibleRarities": []
                  },
                  "sorteio_final": null,
                  "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
                },
                "status": {
                  "candidatos": [],
                  "sortear": false,
                  "quantidade_sorteada_configurada": 1,
                  "resultado_sorteado": null,
                  "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
                },
                "skills": []
              },
              "remocoes_status": []
            }
          ],
          "overrides": [],
          "batalha": {
            "iniciar": false,
            "manual": false,
            "referencia": {
              "chave": null,
              "nome": null,
              "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
            },
            "override": {
              "ForceRandomSuperUnique": 0,
              "DisableSuperUnique": 0,
              "DisableEnemyMods": 0,
              "UseRewardModifiers": 0,
              "ExpModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GoldModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "LootModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GauranteedLoot": [],
              "ForcedEnemies": [],
              "EnemyModApplications": [],
              "EnemyStatusApplications": [],
              "FillOutBattlePoints": 0,
              "OverrideBattlePoints": 0,
              "BattlePointValue": 8,
              "OverrideEnemyGroupPool": 0,
              "EnemyGroupPool": [],
              "OverrideEnemyTypePool": 0,
              "EnemyTypePool": [],
              "VictoryEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "FailureEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "EnemyTurnFirst": 0,
              "ForceMap": 0,
              "MapToForce": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "ovrEnemyStatusRefList": [],
              "ovrEnemyModRefList": []
            },
            "dados_recompensa_final": null,
            "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
          },
          "evento_encadeado": {
            "chave": "resources.assets:2545613",
            "nome": "Jack in the Box - Phase 2",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545613
            },
            "tipo": "PartyEvent"
          }
        }
      ]
    },
    {
      "indice": 2,
      "condicoes": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      },
      "rolagem": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      },
      "hideOptionEffectText": 1,
      "efeitos": [
        {
          "indice": 1,
          "texto": "As you move away, the silence shatters. A blast echoes through the castle as the jack-in-the-box explodes open, a riot of colorful confetti eruptes from its depths. Laughter, eerie and cruel, echoes through the halls as the figure within came into view. The Jack was no more.\n\n\nIn its place stands The Jester. A grotesque caricature of what was once a joyful figure, he wears a motley costume of bright colors, each piece patterned with mocking faces. His own face, disturbingly human, bares a twisted smile as his eyes gleam with cruel mirth. A demon in the garb of a clown, he had awaited your departure to reveal his true, horrifying nature, ready to play his wicked games with the trespassers who dared to disturb his rest.",
          "resultado": {
            "valor": 0,
            "nome": "Success"
          },
          "limite_rolagem": 0,
          "texto_efeitos_manual": [],
          "efeitos": [
            {
              "vida_mana": {
                "percentMaxHealth": 0.0,
                "percentMaxMana": 0.0,
                "percentCurHealth": 0.0,
                "percentCurMana": 0.0
              },
              "alvo": {
                "override": false,
                "tipo_override": {
                  "valor": 0,
                  "nome": "Self"
                },
                "tipo_default_serializado": {
                  "valor": 0,
                  "nome": "Self"
                }
              },
              "recompensas": {
                "ouro": {
                  "dar": false,
                  "retirar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
                },
                "experiencia": {
                  "dar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
                },
                "itens": {
                  "dar": false,
                  "pool_tipo": {
                    "valor": 2,
                    "nome": "Unassigned"
                  },
                  "quantidade_configurada": 1,
                  "tabelas": [],
                  "restricoes": {
                    "limitItemTypes": 0,
                    "possibleItemTypes": [],
                    "limitItemRarities": 0,
                    "possibleRarities": []
                  },
                  "sorteio_final": null,
                  "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
                },
                "status": {
                  "candidatos": [],
                  "sortear": false,
                  "quantidade_sorteada_configurada": 1,
                  "resultado_sorteado": null,
                  "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
                },
                "skills": []
              },
              "remocoes_status": []
            }
          ],
          "overrides": [],
          "batalha": {
            "iniciar": true,
            "manual": false,
            "referencia": {
              "chave": null,
              "nome": null,
              "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
            },
            "override": {
              "ForceRandomSuperUnique": 0,
              "DisableSuperUnique": 0,
              "DisableEnemyMods": 0,
              "UseRewardModifiers": 0,
              "ExpModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GoldModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "LootModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GauranteedLoot": [],
              "ForcedEnemies": [
                {
                  "OverrideEnemyName": 0,
                  "NameOverride": "",
                  "CharacterInfo": {
                    "m_FileID": 0,
                    "m_PathID": 2545118
                  },
                  "ForcedEnemyMods": [],
                  "IsSuperUnique": 0
                }
              ],
              "EnemyModApplications": [],
              "EnemyStatusApplications": [],
              "FillOutBattlePoints": 0,
              "OverrideBattlePoints": 0,
              "BattlePointValue": 8,
              "OverrideEnemyGroupPool": 0,
              "EnemyGroupPool": [],
              "OverrideEnemyTypePool": 0,
              "EnemyTypePool": [],
              "VictoryEvent": {
                "m_FileID": 0,
                "m_PathID": 2545614
              },
              "FailureEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "EnemyTurnFirst": 0,
              "ForceMap": 0,
              "MapToForce": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "ovrEnemyStatusRefList": [],
              "ovrEnemyModRefList": []
            },
            "dados_recompensa_final": null,
            "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
          },
          "evento_encadeado": {
            "chave": null,
            "nome": null,
            "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
          }
        }
      ]
    }
  ]
}
```



## 23. Jack in the Box — resources.assets:2545615

Chave: `resources.assets:2545615`. GUID real: `c260fb9c-4f6c-40d8-8b55-2244d53e54d4`. Asset: `Jack in the Box`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 2; ações: 2; overrides: 0. Origem: `events/jack in the box`.

VEREDITO PROPOSTO: MELHORAR — natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

Uniformizar a narração no presente e o adjetivo composto; manter tags e a transição para a fase 2.

### Texto atual → proposta exata

Campo: `texto`.

Atual (campo completo):
```json
"The <b><rainb><incr>Jack-in-the-Box</incr></rainb></b> is immense, a garish curiosity nestled within the shadowed halls of this accursed castle. Its wooden carvings are painted in jaunty hues that clash with the ominous atmosphere that hangs about it. As you approach, it seemed to possess an aura that both invites and warns of the chaos contained within."
```

PROPOSTA EXATA (campo completo):
```json
"The <b><rainb><incr>Jack-in-the-Box</incr></rainb></b> is immense, a garish curiosity nestled within the shadowed halls of this accursed castle. Its wooden carvings are painted in jaunty hues that clash with the ominous atmosphere that hangs about it. As you approach, it seems to possess an aura that both invites and warns of the chaos contained within."
```

Justificativa: Uniformizar a narração no presente e o adjetivo composto; manter tags e a transição para a fase 2.

Campo: `opcoes/0/efeitos/0/texto`.

Atual (campo completo):
```json
"As the handle moves, a haunting melody starts to play, a chilling echo of a once innocent children's tune now twisted by its dark surroundings. The notes hang in the air, shrouded in an eerie suspense."
```

PROPOSTA EXATA (campo completo):
```json
"As the handle moves, a haunting melody starts to play, a chilling echo of a once-innocent children's tune now twisted by its dark surroundings. The notes hang in the air, shrouded in an eerie suspense."
```

Justificativa: Uniformizar a narração no presente e o adjetivo composto; manter tags e a transição para a fase 2.

### Todos os textos atuais e decisão por campo

`texto` — MELHORAR conforme proposta acima:
```json
"The <b><rainb><incr>Jack-in-the-Box</incr></rainb></b> is immense, a garish curiosity nestled within the shadowed halls of this accursed castle. Its wooden carvings are painted in jaunty hues that clash with the ominous atmosphere that hangs about it. As you approach, it seemed to possess an aura that both invites and warns of the chaos contained within."
```

`texto_resultados_possiveis` — MANTER:
```json
"What will you do?"
```

`campos_originais/promptToSelectCharacter` — MANTER:
```json
"Who will try and crack the <b><legend><incr>Heavy Safe</b></legend></incr>?"
```

`campos_originais/characterSelectedText` — MANTER:
```json
""
```

`opcoes/0/titulo` — MANTER:
```json
"Crank"
```

`opcoes/0/texto` — MANTER:
```json
"Turn the crank and play the game."
```

`opcoes/1/titulo` — MANTER:
```json
"Leave"
```

`opcoes/1/texto` — MANTER:
```json
"You have no time for childish games."
```

`opcoes/0/rolagem/texto_misterioso` — MANTER:
```json
""
```

`opcoes/1/rolagem/texto_misterioso` — MANTER:
```json
""
```

`opcoes/0/efeitos/0/texto` — MELHORAR conforme proposta acima:
```json
"As the handle moves, a haunting melody starts to play, a chilling echo of a once innocent children's tune now twisted by its dark surroundings. The notes hang in the air, shrouded in an eerie suspense."
```

`opcoes/1/efeitos/0/texto` — MANTER:
```json
"The <b><rainb><incr>Box</incr></rainb></b> will remain a mystery for now."
```

### Anomalias, cautelas e limites

- Crank conduz a resources.assets:2545613, não a si mesmo. Leave nesta fase não inicia combate: não confundir com a seção 22.

- `disabled=0` é configuração; disponibilidade efetiva NAO_EXERCITADO. Nenhuma remoção/reativação proposta.

- Textos vazios auditados: 3. Campos: `campos_originais/characterSelectedText`, `opcoes/0/rolagem/texto_misterioso`, `opcoes/1/rolagem/texto_misterioso`.

- NULL preservados: 24; motivos por caminho no anexo de auditoria `EV-R2-FORAPOOL-b02-parte05.md`. Inclui projeção redundante de recompensa: não somar como efeitos extras.

- Referências nulas projetadas: 3. Combate/RNG/quantidade final/status aplicado/UI: NAO_EXERCITADO — somente configuração offline disponível.

- Opção 1: ocultar sem requisitos=false; ocultar por status=[]; hideOptionEffectText=0. Exibição real NAO_EXERCITADO.

- Opção 2: ocultar sem requisitos=false; ocultar por status=[]; hideOptionEffectText=0. Exibição real NAO_EXERCITADO.

### Referências consultadas e encadeamentos de entrada

Configurações de candidato não são concessões executadas. Catálogo consultado por chave, sem expandir/editar as definições externas.
```json
{
  "referencias": [
    {
      "campo": "$.opcoes[0].efeitos[0].evento_encadeado",
      "chave": "resources.assets:2545613",
      "nome": "Jack in the Box - Phase 2",
      "tipo_catalogo": "PartyEvent",
      "nome_asset_catalogo": "Jack in the Box - Phase 2",
      "registro_catalogo": true,
      "resumo_catalogo": true
    }
  ],
  "pptrs_nao_nulos": [
    {
      "campo": "$.opcoes[0].efeitos[0].evento_encadeado.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545613
      },
      "chave": "resources.assets:2545613",
      "tipo_catalogo": "PartyEvent",
      "nome_catalogo": "Jack in the Box - Phase 2"
    },
    {
      "campo": "$.condicoes.requiredStatusesToSpawn[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545523
      },
      "chave": "resources.assets:2545523",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Wrath of the Righteous"
    }
  ],
  "referencias_nulas": [
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.referencia",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.opcoes[1].efeitos[0].batalha.referencia",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.opcoes[1].efeitos[0].evento_encadeado",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    }
  ],
  "referencias_entrada": [
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545523",
      "tipo": "EventStatus",
      "campo": "$.ForcedEventBeforeBoss"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[82]"
    }
  ]
}
```

### Condições, modos e configuração completa das ações

```json
{
  "condicoes": {
    "disabled": 0,
    "EditorOnly": 0,
    "allowOnAllNodeTypes": 0,
    "allowedNodeTypes": [
      7
    ],
    "requiredStatusesToSpawn": [
      {
        "m_FileID": 0,
        "m_PathID": 2545523
      }
    ],
    "allowOnAllTerrainTypes": 1,
    "allowedTerrainTypes": [],
    "allowAtAllTimesOfDay": 1,
    "allowedTimeOfDay": 0,
    "allowAtAllLevels": 1,
    "minLevel": 1,
    "terrainTypesAllowedAtAnyTime": [],
    "KeepInDeckWhenUsed": 0,
    "isLesserEvent": 0,
    "LeadsToFortune": 0
  },
  "modos": [
    {
      "valor": 0,
      "nome": "Campaign"
    },
    {
      "valor": 1,
      "nome": "Roguelike"
    }
  ],
  "historia": {
    "valor": 0,
    "nome": "NonStoryOnly"
  },
  "full_release": {
    "valor": 0,
    "nome": "None"
  },
  "apresentacao_autoral": {
    "AutoStartBattle": 0,
    "targetType": 0,
    "characterPool": 0,
    "showContinueBtnInsteadOfSingleOption": 0,
    "disableAutoChoose": 0,
    "RefEventStatuses": []
  },
  "opcoes": [
    {
      "indice": 1,
      "condicoes": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      },
      "rolagem": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      },
      "hideOptionEffectText": 0,
      "efeitos": [
        {
          "indice": 1,
          "texto": "As the handle moves, a haunting melody starts to play, a chilling echo of a once innocent children's tune now twisted by its dark surroundings. The notes hang in the air, shrouded in an eerie suspense.",
          "resultado": {
            "valor": 0,
            "nome": "Success"
          },
          "limite_rolagem": 0,
          "texto_efeitos_manual": [],
          "efeitos": [
            {
              "vida_mana": {
                "percentMaxHealth": 0.0,
                "percentMaxMana": 0.0,
                "percentCurHealth": 0.0,
                "percentCurMana": 0.0
              },
              "alvo": {
                "override": false,
                "tipo_override": {
                  "valor": 2,
                  "nome": "Party"
                },
                "tipo_default_serializado": {
                  "valor": 0,
                  "nome": "Self"
                }
              },
              "recompensas": {
                "ouro": {
                  "dar": false,
                  "retirar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
                },
                "experiencia": {
                  "dar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
                },
                "itens": {
                  "dar": false,
                  "pool_tipo": {
                    "valor": 2,
                    "nome": "Unassigned"
                  },
                  "quantidade_configurada": 1,
                  "tabelas": [],
                  "restricoes": {
                    "limitItemTypes": 0,
                    "possibleItemTypes": [],
                    "limitItemRarities": 0,
                    "possibleRarities": []
                  },
                  "sorteio_final": null,
                  "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
                },
                "status": {
                  "candidatos": [],
                  "sortear": false,
                  "quantidade_sorteada_configurada": 1,
                  "resultado_sorteado": null,
                  "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
                },
                "skills": []
              },
              "remocoes_status": []
            }
          ],
          "overrides": [],
          "batalha": {
            "iniciar": false,
            "manual": false,
            "referencia": {
              "chave": null,
              "nome": null,
              "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
            },
            "override": {
              "ForceRandomSuperUnique": 0,
              "DisableSuperUnique": 0,
              "DisableEnemyMods": 0,
              "UseRewardModifiers": 0,
              "ExpModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GoldModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "LootModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GauranteedLoot": [],
              "ForcedEnemies": [],
              "EnemyModApplications": [],
              "EnemyStatusApplications": [],
              "FillOutBattlePoints": 0,
              "OverrideBattlePoints": 0,
              "BattlePointValue": 8,
              "OverrideEnemyGroupPool": 0,
              "EnemyGroupPool": [],
              "OverrideEnemyTypePool": 0,
              "EnemyTypePool": [],
              "VictoryEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "FailureEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "EnemyTurnFirst": 0,
              "ForceMap": 0,
              "MapToForce": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "ovrEnemyStatusRefList": [],
              "ovrEnemyModRefList": []
            },
            "dados_recompensa_final": null,
            "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
          },
          "evento_encadeado": {
            "chave": "resources.assets:2545613",
            "nome": "Jack in the Box - Phase 2",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545613
            },
            "tipo": "PartyEvent"
          }
        }
      ]
    },
    {
      "indice": 2,
      "condicoes": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      },
      "rolagem": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      },
      "hideOptionEffectText": 0,
      "efeitos": [
        {
          "indice": 1,
          "texto": "The <b><rainb><incr>Box</incr></rainb></b> will remain a mystery for now.",
          "resultado": {
            "valor": 0,
            "nome": "Success"
          },
          "limite_rolagem": 0,
          "texto_efeitos_manual": [],
          "efeitos": [
            {
              "vida_mana": {
                "percentMaxHealth": 0.0,
                "percentMaxMana": 0.0,
                "percentCurHealth": 0.0,
                "percentCurMana": 0.0
              },
              "alvo": {
                "override": false,
                "tipo_override": {
                  "valor": 0,
                  "nome": "Self"
                },
                "tipo_default_serializado": {
                  "valor": 0,
                  "nome": "Self"
                }
              },
              "recompensas": {
                "ouro": {
                  "dar": false,
                  "retirar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
                },
                "experiencia": {
                  "dar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
                },
                "itens": {
                  "dar": false,
                  "pool_tipo": {
                    "valor": 2,
                    "nome": "Unassigned"
                  },
                  "quantidade_configurada": 1,
                  "tabelas": [],
                  "restricoes": {
                    "limitItemTypes": 0,
                    "possibleItemTypes": [],
                    "limitItemRarities": 0,
                    "possibleRarities": []
                  },
                  "sorteio_final": null,
                  "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
                },
                "status": {
                  "candidatos": [],
                  "sortear": false,
                  "quantidade_sorteada_configurada": 1,
                  "resultado_sorteado": null,
                  "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
                },
                "skills": []
              },
              "remocoes_status": []
            }
          ],
          "overrides": [],
          "batalha": {
            "iniciar": false,
            "manual": false,
            "referencia": {
              "chave": null,
              "nome": null,
              "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
            },
            "override": {
              "ForceRandomSuperUnique": 0,
              "DisableSuperUnique": 0,
              "DisableEnemyMods": 0,
              "UseRewardModifiers": 0,
              "ExpModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GoldModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "LootModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GauranteedLoot": [],
              "ForcedEnemies": [],
              "EnemyModApplications": [],
              "EnemyStatusApplications": [],
              "FillOutBattlePoints": 0,
              "OverrideBattlePoints": 0,
              "BattlePointValue": 8,
              "OverrideEnemyGroupPool": 0,
              "EnemyGroupPool": [],
              "OverrideEnemyTypePool": 0,
              "EnemyTypePool": [],
              "VictoryEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "FailureEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "EnemyTurnFirst": 0,
              "ForceMap": 0,
              "MapToForce": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "ovrEnemyStatusRefList": [],
              "ovrEnemyModRefList": []
            },
            "dados_recompensa_final": null,
            "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
          },
          "evento_encadeado": {
            "chave": null,
            "nome": null,
            "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
          }
        }
      ]
    }
  ]
}
```



## 24. Jack in the Box - Victory — resources.assets:2545614

Chave: `resources.assets:2545614`. GUID real: `3251055e-02b6-4581-9994-d258c7ad0cfc`. Asset: `Jack in the Box - Victory`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 1; ações: 1; overrides: 1. Origem: `events/jack in the box - victory`.

VEREDITO PROPOSTO: MELHORAR — natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

Separar as duas frases da fala e tornar o resultado neutro entre a recompensa padrão e o override Disable, sem selecionar uma variante.

### Texto atual → proposta exata

Campo: `texto`.

Atual (campo completo):
```json
"You have vanquished <b><rainb><incr>The Jester</incr></rainb></b>! \n\n<b><gold><incr>The Paladin</incr></gold></b> greets you:\n\n\"You have done what I could not, Hero. You have brought an end to the evil that has twisted this kingdom.\"\n\n\"Take this as a token of my gratitude, let it remind you that for every shadow in the dark, there lives a beacon of light to banish it.\""
```

PROPOSTA EXATA (campo completo):
```json
"You have vanquished <b><rainb><incr>The Jester</incr></rainb></b>! \n\n<b><gold><incr>The Paladin</incr></gold></b> greets you:\n\n\"You have done what I could not, Hero. You have brought an end to the evil that has twisted this kingdom.\"\n\n\"Take this as a token of my gratitude. Let it remind you that for every shadow in the dark, there lives a beacon of light to banish it.\""
```

Justificativa: Separar as duas frases da fala e tornar o resultado neutro entre a recompensa padrão e o override Disable, sem selecionar uma variante.

Campo: `opcoes/0/efeitos/0/texto`.

Atual (campo completo):
```json
"You feel the power of light burn within the scale."
```

PROPOSTA EXATA (campo completo):
```json
"You feel the power of light within the Paladin's gift."
```

Justificativa: Separar as duas frases da fala e tornar o resultado neutro entre a recompensa padrão e o override Disable, sem selecionar uma variante.

### Todos os textos atuais e decisão por campo

`texto` — MELHORAR conforme proposta acima:
```json
"You have vanquished <b><rainb><incr>The Jester</incr></rainb></b>! \n\n<b><gold><incr>The Paladin</incr></gold></b> greets you:\n\n\"You have done what I could not, Hero. You have brought an end to the evil that has twisted this kingdom.\"\n\n\"Take this as a token of my gratitude, let it remind you that for every shadow in the dark, there lives a beacon of light to banish it.\""
```

`texto_resultados_possiveis` — MANTER:
```json
""
```

`campos_originais/promptToSelectCharacter` — MANTER:
```json
"Who will try and crack the <b><legend><incr>Heavy Safe</b></legend></incr>?"
```

`campos_originais/characterSelectedText` — MANTER:
```json
""
```

`opcoes/0/titulo` — MANTER:
```json
"Accept"
```

`opcoes/0/texto` — MANTER:
```json
"Take <b><gold><incr>The Paladin</incr></gold></b>'s gift."
```

`opcoes/0/rolagem/texto_misterioso` — MANTER:
```json
""
```

`opcoes/0/efeitos/0/texto` — MELHORAR conforme proposta acima:
```json
"You feel the power of light burn within the scale."
```

### Anomalias, cautelas e limites

- Padrão referencia Ivory Dragon Scale (2545426); override FullReleaseMode Disable referencia Wrath of the Righteous (2545488). O texto atual menciona scale embora as variantes sejam distintas; a proposta usa gift e preserva ambos os efeitos.

- Texto de resultados possíveis vazio: manter; uma opção de aceitação já existe.

- `disabled=0` é configuração; disponibilidade efetiva NAO_EXERCITADO. Nenhuma remoção/reativação proposta.

- Textos vazios auditados: 3. Campos: `texto_resultados_possiveis`, `campos_originais/characterSelectedText`, `opcoes/0/rolagem/texto_misterioso`.

- NULL preservados: 21; motivos por caminho no anexo de auditoria `EV-R2-FORAPOOL-b02-parte05.md`. Inclui projeção redundante de recompensa: não somar como efeitos extras.

- Referências nulas projetadas: 2. Combate/RNG/quantidade final/status aplicado/UI: NAO_EXERCITADO — somente configuração offline disponível.

- Opção 1: ocultar sem requisitos=false; ocultar por status=[]; hideOptionEffectText=0. Exibição real NAO_EXERCITADO.

### Referências consultadas e encadeamentos de entrada

Configurações de candidato não são concessões executadas. Catálogo consultado por chave, sem expandir/editar as definições externas.
```json
{
  "referencias": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0]",
      "chave": "resources.assets:2545426",
      "nome": "Ivory Dragon Scale",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Dragonkin White",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].efeitos[0].overrides[0].efeitos[0].recompensas.status.candidatos[0]",
      "chave": "resources.assets:2545488",
      "nome": "Wrath of the Righteous",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Wrath of the Righteous",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].efeitos[0].overrides[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544378",
      "nome": "DamageModHealing",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "DamageModHealing",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545426",
      "nome": "Ivory Dragon Scale",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Dragonkin White",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].overrides[0].recompensas[0].status.candidatos[0]",
      "chave": "resources.assets:2545488",
      "nome": "Wrath of the Righteous",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Wrath of the Righteous",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].overrides[0].recompensas[0].status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544378",
      "nome": "DamageModHealing",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "DamageModHealing",
      "registro_catalogo": true,
      "resumo_catalogo": true
    }
  ],
  "pptrs_nao_nulos": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545426
      },
      "chave": "resources.assets:2545426",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Dragonkin White"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].overrides[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545488
      },
      "chave": "resources.assets:2545488",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Wrath of the Righteous"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].overrides[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544378
      },
      "chave": "resources.assets:2544378",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "DamageModHealing"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545426
      },
      "chave": "resources.assets:2545426",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Dragonkin White"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].overrides[0].recompensas[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545488
      },
      "chave": "resources.assets:2545488",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Wrath of the Righteous"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].overrides[0].recompensas[0].status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544378
      },
      "chave": "resources.assets:2544378",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "DamageModHealing"
    }
  ],
  "referencias_nulas": [
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.referencia",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.opcoes[0].efeitos[0].evento_encadeado",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    }
  ],
  "referencias_entrada": [
    {
      "fonte": "eventos.json",
      "origem": "resources.assets:2545613",
      "campo": "$.opcoes[1].efeitos[0].batalha.override.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545613",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[1].eventActions[0].battleOverrideInfo.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[84]"
    }
  ]
}
```

### Condições, modos e configuração completa das ações

```json
{
  "condicoes": {
    "disabled": 0,
    "EditorOnly": 0,
    "allowOnAllNodeTypes": 0,
    "allowedNodeTypes": [
      7
    ],
    "requiredStatusesToSpawn": [],
    "allowOnAllTerrainTypes": 1,
    "allowedTerrainTypes": [],
    "allowAtAllTimesOfDay": 1,
    "allowedTimeOfDay": 0,
    "allowAtAllLevels": 1,
    "minLevel": 1,
    "terrainTypesAllowedAtAnyTime": [],
    "KeepInDeckWhenUsed": 0,
    "isLesserEvent": 0,
    "LeadsToFortune": 1
  },
  "modos": [
    {
      "valor": 0,
      "nome": "Campaign"
    },
    {
      "valor": 1,
      "nome": "Roguelike"
    }
  ],
  "historia": {
    "valor": 0,
    "nome": "NonStoryOnly"
  },
  "full_release": {
    "valor": 0,
    "nome": "None"
  },
  "apresentacao_autoral": {
    "AutoStartBattle": 0,
    "targetType": 0,
    "characterPool": 0,
    "showContinueBtnInsteadOfSingleOption": 0,
    "disableAutoChoose": 1,
    "RefEventStatuses": []
  },
  "opcoes": [
    {
      "indice": 1,
      "condicoes": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      },
      "rolagem": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      },
      "hideOptionEffectText": 0,
      "efeitos": [
        {
          "indice": 1,
          "texto": "You feel the power of light burn within the scale.",
          "resultado": {
            "valor": 0,
            "nome": "Success"
          },
          "limite_rolagem": 0,
          "texto_efeitos_manual": [],
          "efeitos": [
            {
              "vida_mana": {
                "percentMaxHealth": 0.0,
                "percentMaxMana": 0.0,
                "percentCurHealth": 0.0,
                "percentCurMana": 0.0
              },
              "alvo": {
                "override": false,
                "tipo_override": {
                  "valor": 2,
                  "nome": "Party"
                },
                "tipo_default_serializado": {
                  "valor": 0,
                  "nome": "Self"
                }
              },
              "recompensas": {
                "ouro": {
                  "dar": false,
                  "retirar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
                },
                "experiencia": {
                  "dar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
                },
                "itens": {
                  "dar": false,
                  "pool_tipo": {
                    "valor": 2,
                    "nome": "Unassigned"
                  },
                  "quantidade_configurada": 1,
                  "tabelas": [],
                  "restricoes": {
                    "limitItemTypes": 0,
                    "possibleItemTypes": [],
                    "limitItemRarities": 0,
                    "possibleRarities": []
                  },
                  "sorteio_final": null,
                  "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
                },
                "status": {
                  "candidatos": [
                    {
                      "chave": "resources.assets:2545426",
                      "nome": "Ivory Dragon Scale",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545426
                      },
                      "tipo": "EventStatus",
                      "descricao": "Gain the ability to shapeshift into a White Dragonkin.\n\n<i><color=#808080>\"Imbued with a gentle radiance, it serves as a testament to the enduring strength of the forces of light\"</i></color>\n",
                      "duracao": {
                        "valor": 3,
                        "nome": "Permanent"
                      },
                      "status_tipo": {
                        "valor": 1,
                        "nome": "Fortune"
                      },
                      "modificadores": []
                    }
                  ],
                  "sortear": false,
                  "quantidade_sorteada_configurada": 1,
                  "resultado_sorteado": null,
                  "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
                },
                "skills": []
              },
              "remocoes_status": []
            }
          ],
          "overrides": [
            {
              "modo": {
                "valor": 1,
                "nome": "Disable"
              },
              "efeitos": [
                {
                  "vida_mana": {
                    "percentMaxHealth": 0.0,
                    "percentMaxMana": 0.0,
                    "percentCurHealth": 0.0,
                    "percentCurMana": 0.0
                  },
                  "alvo": {
                    "override": false,
                    "tipo_override": {
                      "valor": 2,
                      "nome": "Party"
                    },
                    "tipo_default_serializado": {
                      "valor": 0,
                      "nome": "Self"
                    }
                  },
                  "recompensas": {
                    "ouro": {
                      "dar": false,
                      "retirar": false,
                      "razao": 1.0,
                      "quantidade_final": null,
                      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
                    },
                    "experiencia": {
                      "dar": false,
                      "razao": 1.0,
                      "quantidade_final": null,
                      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
                    },
                    "itens": {
                      "dar": false,
                      "pool_tipo": {
                        "valor": 2,
                        "nome": "Unassigned"
                      },
                      "quantidade_configurada": 1,
                      "tabelas": [],
                      "restricoes": {
                        "limitItemTypes": 0,
                        "possibleItemTypes": [],
                        "limitItemRarities": 0,
                        "possibleRarities": []
                      },
                      "sorteio_final": null,
                      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
                    },
                    "status": {
                      "candidatos": [
                        {
                          "chave": "resources.assets:2545488",
                          "nome": "Wrath of the Righteous",
                          "pptr": {
                            "m_FileID": 0,
                            "m_PathID": 2545488
                          },
                          "tipo": "EventStatus",
                          "descricao": "Healing skills in the Light tree can now deal damage to enemies as well as heal allies. @Holy Power@ increased by {6,30}%.\n\n<i><color=#808080>\"The light of vengence burns brightly!\"</color></i>\n",
                          "duracao": {
                            "valor": 3,
                            "nome": "Permanent"
                          },
                          "status_tipo": {
                            "valor": 1,
                            "nome": "Fortune"
                          },
                          "modificadores": [
                            {
                              "atributo": {
                                "chave": "resources.assets:2544378",
                                "nome": "DamageModHealing",
                                "pptr": {
                                  "m_FileID": 0,
                                  "m_PathID": 2544378
                                },
                                "tipo": "CharacterAttribute"
                              },
                              "metodo": {
                                "valor": 0,
                                "nome": "Base"
                              },
                              "expressao": "{6,30}",
                              "segunda_passagem": false
                            }
                          ]
                        }
                      ],
                      "sortear": false,
                      "quantidade_sorteada_configurada": 1,
                      "resultado_sorteado": null,
                      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
                    },
                    "skills": []
                  },
                  "remocoes_status": []
                }
              ]
            }
          ],
          "batalha": {
            "iniciar": false,
            "manual": false,
            "referencia": {
              "chave": null,
              "nome": null,
              "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
            },
            "override": {
              "ForceRandomSuperUnique": 0,
              "DisableSuperUnique": 0,
              "DisableEnemyMods": 0,
              "UseRewardModifiers": 0,
              "ExpModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GoldModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "LootModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GauranteedLoot": [],
              "ForcedEnemies": [],
              "EnemyModApplications": [],
              "EnemyStatusApplications": [],
              "FillOutBattlePoints": 0,
              "OverrideBattlePoints": 0,
              "BattlePointValue": 8,
              "OverrideEnemyGroupPool": 0,
              "EnemyGroupPool": [],
              "OverrideEnemyTypePool": 0,
              "EnemyTypePool": [],
              "VictoryEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "FailureEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "EnemyTurnFirst": 0,
              "ForceMap": 0,
              "MapToForce": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "ovrEnemyStatusRefList": [],
              "ovrEnemyModRefList": []
            },
            "dados_recompensa_final": null,
            "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
          },
          "evento_encadeado": {
            "chave": null,
            "nome": null,
            "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
          }
        }
      ]
    }
  ]
}
```



## 25. King Under the Mountain — resources.assets:2545633

Chave: `resources.assets:2545633`. GUID real: `01cb5dd1-ba2c-472f-9601-8a43aa56e8b9`. Asset: `3 - Mountain King Ironheart End`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 0; ações: 0; overrides: 0. Origem: `events/main quests/3 - mountain king ironheart end`.

VEREDITO PROPOSTO: MELHORAR — natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

Corrigir concordância, repetição e tempos verbais na narrativa pós-combate sem criar opção, item ou recompensa.

### Texto atual → proposta exata

Campo: `texto`.

Atual (campo completo):
```json
"With a final, mighty blow you strike down the mighty dwarf. The madness in Ironheart's eyes fade, and for a moment, he is the noble king he once was.\n\nSuddenly, from the depths of his armor, a soft glow begins to emerge. It's a light so pure and gentle, it seems out of place in the dark, cold hall. A small feather, illuminated in a halo of light, floats gracefully from his chest. It's a robin's feather, delicate and beautiful, a symbol of life and new beginnings.\n\nCompelled by an unknown force, you reach out and grasp the feather. The moment your fingers touch it, the world around you dissolves. You are enveloped in a memory so vivid, it's as though you've been transported through time.\n\r<br/>\nYou find yourself in the dwarven halls of restored splendor, one filled with warmth and laughter. Before you sits Ironheart, but not as the deranged monarch you had just battled. This is Ironheart in his youth, a robust and cheerful king, his eyes sparkling with joy and kindness. On his lap, giggling with innocent delight, is a small dwarven child, his daughter. She playfully tugs at his beard, her laughter echoing through the hall, a sound of pure happiness.\n\r\r<br/>\nAs the memory fades you find yourself back in the present, with the magical feather still warm in your hand. For a long moment, you stare at it, recalling your reading about this very feather in your father's journal. You had dismissed it as a figment of your father's illness-induced imagination, a fanciful creation borne from the erratic and fragmented later entries of the journal. But now, as the feather lay tangible and radiant in your hand, the reality of its existence shakes your understanding of what is possible. \n\nChronicled within the journal is not only this feather but also other items of mystical importance scattered across the realm.\n\nThe next item of importance, as described in the journal, is an amulet, said to be in the possession of a sultan in the deserts of Wyrmrest. \n"
```

PROPOSTA EXATA (campo completo):
```json
"With a final, mighty blow, you strike down the dwarf. The madness in Ironheart's eyes fades, and for a moment, he is the noble king he once was.\n\nSuddenly, from the depths of his armor, a soft glow begins to emerge. It's a light so pure and gentle, it seems out of place in the dark, cold hall. A small feather, illuminated in a halo of light, floats gracefully from his chest. It's a robin's feather, delicate and beautiful, a symbol of life and new beginnings.\n\nCompelled by an unknown force, you reach out and grasp the feather. The moment your fingers touch it, the world around you dissolves. You are enveloped in a memory so vivid, it's as though you've been transported through time.\n\r<br/>\nYou find yourself in the dwarven halls, restored to splendor and filled with warmth and laughter. Before you sits Ironheart, but not as the deranged monarch you had just battled. This is Ironheart in his youth, a robust and cheerful king, his eyes sparkling with joy and kindness. On his lap, giggling with innocent delight, is a small dwarven child, his daughter. She playfully tugs at his beard, her laughter echoing through the hall, a sound of pure happiness.\n\r\r<br/>\nAs the memory fades, you find yourself back in the present, with the magical feather still warm in your hand. For a long moment, you stare at it, recalling your reading about this very feather in your father's journal. You had dismissed it as a figment of your father's illness-induced imagination, a fanciful creation borne from the erratic and fragmented later entries of the journal. But now, as the feather lies tangible and radiant in your hand, the reality of its existence shakes your understanding of what is possible. \n\nChronicled within the journal is not only this feather but also other items of mystical importance scattered across the realm.\n\nThe next item of importance, as described in the journal, is an amulet, said to be in the possession of a sultan in the deserts of Wyrmrest. \n"
```

Justificativa: Corrigir concordância, repetição e tempos verbais na narrativa pós-combate sem criar opção, item ou recompensa.

### Todos os textos atuais e decisão por campo

`texto` — MELHORAR conforme proposta acima:
```json
"With a final, mighty blow you strike down the mighty dwarf. The madness in Ironheart's eyes fade, and for a moment, he is the noble king he once was.\n\nSuddenly, from the depths of his armor, a soft glow begins to emerge. It's a light so pure and gentle, it seems out of place in the dark, cold hall. A small feather, illuminated in a halo of light, floats gracefully from his chest. It's a robin's feather, delicate and beautiful, a symbol of life and new beginnings.\n\nCompelled by an unknown force, you reach out and grasp the feather. The moment your fingers touch it, the world around you dissolves. You are enveloped in a memory so vivid, it's as though you've been transported through time.\n\r<br/>\nYou find yourself in the dwarven halls of restored splendor, one filled with warmth and laughter. Before you sits Ironheart, but not as the deranged monarch you had just battled. This is Ironheart in his youth, a robust and cheerful king, his eyes sparkling with joy and kindness. On his lap, giggling with innocent delight, is a small dwarven child, his daughter. She playfully tugs at his beard, her laughter echoing through the hall, a sound of pure happiness.\n\r\r<br/>\nAs the memory fades you find yourself back in the present, with the magical feather still warm in your hand. For a long moment, you stare at it, recalling your reading about this very feather in your father's journal. You had dismissed it as a figment of your father's illness-induced imagination, a fanciful creation borne from the erratic and fragmented later entries of the journal. But now, as the feather lay tangible and radiant in your hand, the reality of its existence shakes your understanding of what is possible. \n\nChronicled within the journal is not only this feather but also other items of mystical importance scattered across the realm.\n\nThe next item of importance, as described in the journal, is an amulet, said to be in the possession of a sultan in the deserts of Wyrmrest. \n"
```

`texto_resultados_possiveis` — MANTER:
```json
""
```

`campos_originais/promptToSelectCharacter` — MANTER:
```json
""
```

`campos_originais/characterSelectedText` — MANTER:
```json
""
```

### Anomalias, cautelas e limites

- opcoes=[] e AutoStartBattle=0 no canônico. A pena e o amuleto são menções narrativas; não inventar EventActionEffects nem recompensa a partir do texto.

- Preservar literalmente controles CR/LF e <br/> nesta rodada. Renderização dessas quebras na UI é NAO_EXERCITADO.

- `disabled=0` é configuração; disponibilidade efetiva NAO_EXERCITADO. Nenhuma remoção/reativação proposta.

- Textos vazios auditados: 3. Campos: `texto_resultados_possiveis`, `campos_originais/promptToSelectCharacter`, `campos_originais/characterSelectedText`.

- NULL preservados: 0; motivos por caminho no anexo de auditoria `EV-R2-FORAPOOL-b02-parte05.md`. Inclui projeção redundante de recompensa: não somar como efeitos extras.

- Referências nulas projetadas: 0. Combate/RNG/quantidade final/status aplicado/UI: NAO_EXERCITADO — somente configuração offline disponível.

- Opções vazias (`[]`): não criar opção ou prêmio; referência externa de quest não é prova de entrega executada.

### Referências consultadas e encadeamentos de entrada

Configurações de candidato não são concessões executadas. Catálogo consultado por chave, sem expandir/editar as definições externas.
```json
{
  "referencias": [],
  "pptrs_nao_nulos": [],
  "referencias_nulas": [],
  "referencias_entrada": [
    {
      "fonte": "eventos.json",
      "origem": "resources.assets:2545634",
      "campo": "$.opcoes[0].efeitos[0].batalha.override.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545634",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[102]"
    }
  ]
}
```

### Condições, modos e configuração completa das ações

```json
{
  "condicoes": {
    "disabled": 0,
    "EditorOnly": 0,
    "allowOnAllNodeTypes": 1,
    "allowedNodeTypes": [],
    "requiredStatusesToSpawn": [],
    "allowOnAllTerrainTypes": 1,
    "allowedTerrainTypes": [],
    "allowAtAllTimesOfDay": 1,
    "allowedTimeOfDay": 0,
    "allowAtAllLevels": 1,
    "minLevel": 1,
    "terrainTypesAllowedAtAnyTime": [],
    "KeepInDeckWhenUsed": 0,
    "isLesserEvent": 0,
    "LeadsToFortune": 0
  },
  "modos": [
    {
      "valor": 0,
      "nome": "Campaign"
    },
    {
      "valor": 1,
      "nome": "Roguelike"
    }
  ],
  "historia": {
    "valor": 0,
    "nome": "NonStoryOnly"
  },
  "full_release": {
    "valor": 0,
    "nome": "None"
  },
  "apresentacao_autoral": {
    "AutoStartBattle": 0,
    "targetType": 0,
    "characterPool": 1,
    "showContinueBtnInsteadOfSingleOption": 0,
    "disableAutoChoose": 1,
    "RefEventStatuses": []
  },
  "opcoes": []
}
```



## 26. Lady of the Well — resources.assets:2545620

Chave: `resources.assets:2545620`. GUID real: `a13116b5-0fbf-4598-ab44-f19a70f96365`. Asset: `Lady of the Well - Victory`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 1; ações: 1; overrides: 0. Origem: `events/lady of the well - victory`.

VEREDITO PROPOSTO: MELHORAR — natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

Corrigir movimento descendente em inglês e alinhar o nome narrativo do coração ao nome já usado na opção, sem afirmar que seja item de inventário ou renomear a fortuna.

### Texto atual → proposta exata

Campo: `texto`.

Atual (campo completo):
```json
"Defeated, the <violet><b><incr>Lady of the Well</incr></b></violet> slithers back down the cracks of the sealed well, but she has left her <violet>Shadowy Heart</violet>. "
```

PROPOSTA EXATA (campo completo):
```json
"Defeated, the <violet><b><incr>Lady of the Well</incr></b></violet> slithers back down through the cracks of the sealed well, but she has left her <violet>Shadow-Drenched Heart</violet>. "
```

Justificativa: Corrigir movimento descendente em inglês e alinhar o nome narrativo do coração ao nome já usado na opção, sem afirmar que seja item de inventário ou renomear a fortuna.

### Todos os textos atuais e decisão por campo

`texto` — MELHORAR conforme proposta acima:
```json
"Defeated, the <violet><b><incr>Lady of the Well</incr></b></violet> slithers back down the cracks of the sealed well, but she has left her <violet>Shadowy Heart</violet>. "
```

`texto_resultados_possiveis` — MANTER:
```json
""
```

`campos_originais/promptToSelectCharacter` — MANTER:
```json
""
```

`campos_originais/characterSelectedText` — MANTER:
```json
""
```

`opcoes/0/titulo` — MANTER:
```json
"Take"
```

`opcoes/0/texto` — MANTER:
```json
"Take the <quest>Shadow-Drenched Heart</quest>."
```

`opcoes/0/rolagem/texto_misterioso` — MANTER:
```json
""
```

`opcoes/0/efeitos/0/texto` — MANTER:
```json
""
```

### Anomalias, cautelas e limites

- Narrativa cita Shadowy Heart, opção cita Shadow-Drenched Heart e efeito referencia EventStatus Drop of Shadow (2545427). Proposta apenas unifica os dois nomes narrativos; mantém o nome e a definição da fortuna.

- Ação 1 tem texto vazio; manter vazio, sem fabricar confirmação ou recompensa. giveItems=false: a tag <quest> não comprova item de inventário.

- `disabled=0` é configuração; disponibilidade efetiva NAO_EXERCITADO. Nenhuma remoção/reativação proposta.

- Textos vazios auditados: 5. Campos: `texto_resultados_possiveis`, `campos_originais/promptToSelectCharacter`, `campos_originais/characterSelectedText`, `opcoes/0/rolagem/texto_misterioso`, `opcoes/0/efeitos/0/texto`.

- NULL preservados: 13; motivos por caminho no anexo de auditoria `EV-R2-FORAPOOL-b02-parte05.md`. Inclui projeção redundante de recompensa: não somar como efeitos extras.

- Referências nulas projetadas: 2. Combate/RNG/quantidade final/status aplicado/UI: NAO_EXERCITADO — somente configuração offline disponível.

- Opção 1: ocultar sem requisitos=false; ocultar por status=[]; hideOptionEffectText=0. Exibição real NAO_EXERCITADO.

### Referências consultadas e encadeamentos de entrada

Configurações de candidato não são concessões executadas. Catálogo consultado por chave, sem expandir/editar as definições externas.
```json
{
  "referencias": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0]",
      "chave": "resources.assets:2545427",
      "nome": "Drop of Shadow",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Drop of Shadow",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544381",
      "nome": "DamageModShadow",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "DamageModShadow",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545427",
      "nome": "Drop of Shadow",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Drop of Shadow",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544381",
      "nome": "DamageModShadow",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "DamageModShadow",
      "registro_catalogo": true,
      "resumo_catalogo": true
    }
  ],
  "pptrs_nao_nulos": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545427
      },
      "chave": "resources.assets:2545427",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Drop of Shadow"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544381
      },
      "chave": "resources.assets:2544381",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "DamageModShadow"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[0].CharacterInfo",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545113
      },
      "chave": "resources.assets:2545113",
      "tipo_catalogo": "CharacterInfo",
      "nome_catalogo": "Lady of the Well"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545427
      },
      "chave": "resources.assets:2545427",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Drop of Shadow"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544381
      },
      "chave": "resources.assets:2544381",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "DamageModShadow"
    }
  ],
  "referencias_nulas": [
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.referencia",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.opcoes[0].efeitos[0].evento_encadeado",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    }
  ],
  "referencias_entrada": [
    {
      "fonte": "eventos.json",
      "origem": "resources.assets:2545621",
      "campo": "$.opcoes[0].efeitos[0].batalha.override.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545621",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[90]"
    }
  ]
}
```

### Condições, modos e configuração completa das ações

```json
{
  "condicoes": {
    "disabled": 0,
    "EditorOnly": 0,
    "allowOnAllNodeTypes": 0,
    "allowedNodeTypes": [
      7
    ],
    "requiredStatusesToSpawn": [],
    "allowOnAllTerrainTypes": 1,
    "allowedTerrainTypes": [],
    "allowAtAllTimesOfDay": 1,
    "allowedTimeOfDay": 0,
    "allowAtAllLevels": 1,
    "minLevel": 1,
    "terrainTypesAllowedAtAnyTime": [],
    "KeepInDeckWhenUsed": 0,
    "isLesserEvent": 0,
    "LeadsToFortune": 1
  },
  "modos": [
    {
      "valor": 0,
      "nome": "Campaign"
    },
    {
      "valor": 1,
      "nome": "Roguelike"
    }
  ],
  "historia": {
    "valor": 0,
    "nome": "NonStoryOnly"
  },
  "full_release": {
    "valor": 0,
    "nome": "None"
  },
  "apresentacao_autoral": {
    "AutoStartBattle": 0,
    "targetType": 0,
    "characterPool": 0,
    "showContinueBtnInsteadOfSingleOption": 0,
    "disableAutoChoose": 1,
    "RefEventStatuses": []
  },
  "opcoes": [
    {
      "indice": 1,
      "condicoes": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      },
      "rolagem": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      },
      "hideOptionEffectText": 0,
      "efeitos": [
        {
          "indice": 1,
          "texto": "",
          "resultado": {
            "valor": 0,
            "nome": "Success"
          },
          "limite_rolagem": 0,
          "texto_efeitos_manual": [],
          "efeitos": [
            {
              "vida_mana": {
                "percentMaxHealth": 0.0,
                "percentMaxMana": 0.0,
                "percentCurHealth": 0.0,
                "percentCurMana": 0.0
              },
              "alvo": {
                "override": false,
                "tipo_override": {
                  "valor": 0,
                  "nome": "Self"
                },
                "tipo_default_serializado": {
                  "valor": 0,
                  "nome": "Self"
                }
              },
              "recompensas": {
                "ouro": {
                  "dar": false,
                  "retirar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
                },
                "experiencia": {
                  "dar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
                },
                "itens": {
                  "dar": false,
                  "pool_tipo": {
                    "valor": 2,
                    "nome": "Unassigned"
                  },
                  "quantidade_configurada": 1,
                  "tabelas": [],
                  "restricoes": {
                    "limitItemTypes": 0,
                    "possibleItemTypes": [],
                    "limitItemRarities": 0,
                    "possibleRarities": []
                  },
                  "sorteio_final": null,
                  "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
                },
                "status": {
                  "candidatos": [
                    {
                      "chave": "resources.assets:2545427",
                      "nome": "Drop of Shadow",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545427
                      },
                      "tipo": "EventStatus",
                      "descricao": "Shadow damage you deal applies @Sludge@. Increase @Shadow Damage@ by {10,40}%.\n\n<i><color=#808080>\"It's stickier than you imagined.\"</color></i>\n",
                      "duracao": {
                        "valor": 3,
                        "nome": "Permanent"
                      },
                      "status_tipo": {
                        "valor": 1,
                        "nome": "Fortune"
                      },
                      "modificadores": [
                        {
                          "atributo": {
                            "chave": "resources.assets:2544381",
                            "nome": "DamageModShadow",
                            "pptr": {
                              "m_FileID": 0,
                              "m_PathID": 2544381
                            },
                            "tipo": "CharacterAttribute"
                          },
                          "metodo": {
                            "valor": 0,
                            "nome": "Base"
                          },
                          "expressao": "{10,40}",
                          "segunda_passagem": false
                        }
                      ]
                    }
                  ],
                  "sortear": false,
                  "quantidade_sorteada_configurada": 1,
                  "resultado_sorteado": null,
                  "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
                },
                "skills": []
              },
              "remocoes_status": []
            }
          ],
          "overrides": [],
          "batalha": {
            "iniciar": false,
            "manual": false,
            "referencia": {
              "chave": null,
              "nome": null,
              "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
            },
            "override": {
              "ForceRandomSuperUnique": 0,
              "DisableSuperUnique": 0,
              "DisableEnemyMods": 0,
              "UseRewardModifiers": 0,
              "ExpModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GoldModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "LootModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GauranteedLoot": [],
              "ForcedEnemies": [
                {
                  "OverrideEnemyName": 0,
                  "NameOverride": "",
                  "CharacterInfo": {
                    "m_FileID": 0,
                    "m_PathID": 2545113
                  },
                  "ForcedEnemyMods": [],
                  "IsSuperUnique": 0
                }
              ],
              "EnemyModApplications": [],
              "EnemyStatusApplications": [],
              "FillOutBattlePoints": 0,
              "OverrideBattlePoints": 0,
              "BattlePointValue": 8,
              "OverrideEnemyGroupPool": 0,
              "EnemyGroupPool": [],
              "OverrideEnemyTypePool": 0,
              "EnemyTypePool": [],
              "VictoryEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "FailureEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "EnemyTurnFirst": 0,
              "ForceMap": 0,
              "MapToForce": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "ovrEnemyStatusRefList": [],
              "ovrEnemyModRefList": []
            },
            "dados_recompensa_final": null,
            "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
          },
          "evento_encadeado": {
            "chave": null,
            "nome": null,
            "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
          }
        }
      ]
    }
  ]
}
```



## 27. Lesser Mimic — resources.assets:2545617

Chave: `resources.assets:2545617`. GUID real: `012ddc27-7b28-4365-9a05-20920ec59c59`. Asset: `Jewelry Box Mimic Victory`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 3; ações: 3; overrides: 0. Origem: `events/jewelry box mimic victory`.

VEREDITO PROPOSTO: MELHORAR — natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

Corrigir o tempo verbal na segunda opção e a pontuação na descrição da visão, mantendo as três escolhas e seus status.

### Texto atual → proposta exata

Campo: `opcoes/1/efeitos/0/texto`.

Atual (campo completo):
```json
"When you pick it up and turned the key set into its side, the device hums to life, sending out a powerful pulse that sends dust motes scattering and your hair standing on end. "
```

PROPOSTA EXATA (campo completo):
```json
"When you pick it up and turn the key set into its side, the device hums to life, sending out a powerful pulse that sends dust motes scattering and your hair standing on end. "
```

Justificativa: Corrigir o tempo verbal na segunda opção e a pontuação na descrição da visão, mantendo as três escolhas e seus status.

Campo: `opcoes/2/efeitos/0/texto`.

Atual (campo completo):
```json
"As you pick up the Crystal Ball and peer into it, you gasp. The surface of the crystal shifts and swirls revealing an overhead view of the surrounding area. Your location, the winding tunnels, and even the far-off flicker of a goblin camp - it is like looking at a living map."
```

PROPOSTA EXATA (campo completo):
```json
"As you pick up the Crystal Ball and peer into it, you gasp. The surface of the crystal shifts and swirls, revealing an overhead view of the surrounding area. Your location, the winding tunnels, and even the far-off flicker of a goblin camp - it is like looking at a living map."
```

Justificativa: Corrigir o tempo verbal na segunda opção e a pontuação na descrição da visão, mantendo as três escolhas e seus status.

### Todos os textos atuais e decisão por campo

`texto` — MANTER:
```json
"With an agonizing screech, the final Mimic collapses in on itself, its form dissolving into an amorphous puddle leaving behind only its treasure.\n\n"
```

`texto_resultados_possiveis` — MANTER:
```json
"What treasure will you take?"
```

`campos_originais/promptToSelectCharacter` — MANTER:
```json
"Does anyone owe this Ogre money?"
```

`campos_originais/characterSelectedText` — MANTER:
```json
"Good luck [name]..."
```

`opcoes/0/titulo` — MANTER:
```json
"Enchanted Whetstone"
```

`opcoes/0/texto` — MANTER:
```json
"A whetstone, unassuming in its appearance, the color of storm clouds at dusk. It is imbued with enchantments of old, filled with the power to hone the edge of any weapon. "
```

`opcoes/1/titulo` — MANTER:
```json
"Dwarven Force Generator"
```

`opcoes/1/texto` — MANTER:
```json
"A strange artifact that looks like a tightly wound spring set within a sphere of unblemished steel. You can see an intricate network of runes, their glow pulsating in a magical rhythm. "
```

`opcoes/2/titulo` — MANTER:
```json
"Crystal Ball"
```

`opcoes/2/texto` — MANTER:
```json
"Roughly the size of an apple and pulsing with an inner light that seems almost alive."
```

`opcoes/0/rolagem/texto_misterioso` — MANTER:
```json
""
```

`opcoes/1/rolagem/texto_misterioso` — MANTER:
```json
""
```

`opcoes/2/rolagem/texto_misterioso` — MANTER:
```json
""
```

`opcoes/0/efeitos/0/texto` — MANTER:
```json
"As you run the stone along your weapon, sparks fly off, and when you pull your weapon back, the blade glints with a deadly sharpness. "
```

`opcoes/1/efeitos/0/texto` — MELHORAR conforme proposta acima:
```json
"When you pick it up and turned the key set into its side, the device hums to life, sending out a powerful pulse that sends dust motes scattering and your hair standing on end. "
```

`opcoes/2/efeitos/0/texto` — MELHORAR conforme proposta acima:
```json
"As you pick up the Crystal Ball and peer into it, you gasp. The surface of the crystal shifts and swirls revealing an overhead view of the surrounding area. Your location, the winding tunnels, and even the far-off flicker of a goblin camp - it is like looking at a living map."
```

### Anomalias, cautelas e limites

- As três opções concedem configurações de EventStatus distintos; não são três itens finais calculados. Enchanted Whetstone tem duração Quest; os outros dois, Permanent: não homogeneizar durações.

- A Crystal Ball descreve visão de mapa, mas o efeito configurado fala em alcance e bônus por distância; flag de revelação de mapa não foi demonstrada. Manter a visão como narrativa, sem prometer mecânica de exploração.

- `disabled=0` é configuração; disponibilidade efetiva NAO_EXERCITADO. Nenhuma remoção/reativação proposta.

- Textos vazios auditados: 3. Campos: `opcoes/0/rolagem/texto_misterioso`, `opcoes/1/rolagem/texto_misterioso`, `opcoes/2/rolagem/texto_misterioso`.

- NULL preservados: 39; motivos por caminho no anexo de auditoria `EV-R2-FORAPOOL-b02-parte05.md`. Inclui projeção redundante de recompensa: não somar como efeitos extras.

- Referências nulas projetadas: 6. Combate/RNG/quantidade final/status aplicado/UI: NAO_EXERCITADO — somente configuração offline disponível.

- Opção 1: ocultar sem requisitos=false; ocultar por status=[]; hideOptionEffectText=0. Exibição real NAO_EXERCITADO.

- Opção 2: ocultar sem requisitos=false; ocultar por status=[]; hideOptionEffectText=0. Exibição real NAO_EXERCITADO.

- Opção 3: ocultar sem requisitos=false; ocultar por status=[]; hideOptionEffectText=0. Exibição real NAO_EXERCITADO.

### Referências consultadas e encadeamentos de entrada

Configurações de candidato não são concessões executadas. Catálogo consultado por chave, sem expandir/editar as definições externas.
```json
{
  "referencias": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0]",
      "chave": "resources.assets:2545437",
      "nome": "Enchanted Whetstone",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Enchanted Whetstone",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544396",
      "nome": "WeaponDamageMod",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "WeaponDamageMod",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545437",
      "nome": "Enchanted Whetstone",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Enchanted Whetstone",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544396",
      "nome": "WeaponDamageMod",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "WeaponDamageMod",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.status.candidatos[0]",
      "chave": "resources.assets:2545428",
      "nome": "Dwarven Force Generator",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Dwarven Force Generator",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[1].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545428",
      "nome": "Dwarven Force Generator",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Dwarven Force Generator",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.status.candidatos[0]",
      "chave": "resources.assets:2545421",
      "nome": "Crystal Ball",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Crystal Ball",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544394",
      "nome": "PerHexRangeDamageBonus",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "PerHexRangeDamageBonus",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[1].atributo",
      "chave": "resources.assets:2544493",
      "nome": "RangeTypeAdderRanged",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "RangeTypeAdderRanged",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[2].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545421",
      "nome": "Crystal Ball",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Crystal Ball",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[2].recompensas[0].padrao[0].status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544394",
      "nome": "PerHexRangeDamageBonus",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "PerHexRangeDamageBonus",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[2].recompensas[0].padrao[0].status.candidatos[0].modificadores[1].atributo",
      "chave": "resources.assets:2544493",
      "nome": "RangeTypeAdderRanged",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "RangeTypeAdderRanged",
      "registro_catalogo": true,
      "resumo_catalogo": true
    }
  ],
  "pptrs_nao_nulos": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545437
      },
      "chave": "resources.assets:2545437",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Enchanted Whetstone"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544396
      },
      "chave": "resources.assets:2544396",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "WeaponDamageMod"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545437
      },
      "chave": "resources.assets:2545437",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Enchanted Whetstone"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544396
      },
      "chave": "resources.assets:2544396",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "WeaponDamageMod"
    },
    {
      "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545428
      },
      "chave": "resources.assets:2545428",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Dwarven Force Generator"
    },
    {
      "campo": "$.opcoes[1].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545428
      },
      "chave": "resources.assets:2545428",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Dwarven Force Generator"
    },
    {
      "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545421
      },
      "chave": "resources.assets:2545421",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Crystal Ball"
    },
    {
      "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544394
      },
      "chave": "resources.assets:2544394",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "PerHexRangeDamageBonus"
    },
    {
      "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[1].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544493
      },
      "chave": "resources.assets:2544493",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "RangeTypeAdderRanged"
    },
    {
      "campo": "$.opcoes[2].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545421
      },
      "chave": "resources.assets:2545421",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Crystal Ball"
    },
    {
      "campo": "$.opcoes[2].recompensas[0].padrao[0].status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544394
      },
      "chave": "resources.assets:2544394",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "PerHexRangeDamageBonus"
    },
    {
      "campo": "$.opcoes[2].recompensas[0].padrao[0].status.candidatos[0].modificadores[1].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544493
      },
      "chave": "resources.assets:2544493",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "RangeTypeAdderRanged"
    }
  ],
  "referencias_nulas": [
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.referencia",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.opcoes[0].efeitos[0].evento_encadeado",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.opcoes[1].efeitos[0].batalha.referencia",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.opcoes[1].efeitos[0].evento_encadeado",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.opcoes[2].efeitos[0].batalha.referencia",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.opcoes[2].efeitos[0].evento_encadeado",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    }
  ],
  "referencias_entrada": [
    {
      "fonte": "eventos.json",
      "origem": "resources.assets:2545618",
      "campo": "$.opcoes[0].efeitos[0].batalha.override.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545618",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[88]"
    }
  ]
}
```

### Condições, modos e configuração completa das ações

```json
{
  "condicoes": {
    "disabled": 0,
    "EditorOnly": 0,
    "allowOnAllNodeTypes": 0,
    "allowedNodeTypes": [
      7
    ],
    "requiredStatusesToSpawn": [],
    "allowOnAllTerrainTypes": 1,
    "allowedTerrainTypes": [],
    "allowAtAllTimesOfDay": 1,
    "allowedTimeOfDay": 1,
    "allowAtAllLevels": 1,
    "minLevel": 1,
    "terrainTypesAllowedAtAnyTime": [
      4,
      3
    ],
    "KeepInDeckWhenUsed": 0,
    "isLesserEvent": 0,
    "LeadsToFortune": 1
  },
  "modos": [
    {
      "valor": 0,
      "nome": "Campaign"
    },
    {
      "valor": 1,
      "nome": "Roguelike"
    }
  ],
  "historia": {
    "valor": 0,
    "nome": "NonStoryOnly"
  },
  "full_release": {
    "valor": 0,
    "nome": "None"
  },
  "apresentacao_autoral": {
    "AutoStartBattle": 0,
    "targetType": 3,
    "characterPool": 1,
    "showContinueBtnInsteadOfSingleOption": 0,
    "disableAutoChoose": 1,
    "RefEventStatuses": []
  },
  "opcoes": [
    {
      "indice": 1,
      "condicoes": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      },
      "rolagem": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      },
      "hideOptionEffectText": 0,
      "efeitos": [
        {
          "indice": 1,
          "texto": "As you run the stone along your weapon, sparks fly off, and when you pull your weapon back, the blade glints with a deadly sharpness. ",
          "resultado": {
            "valor": 0,
            "nome": "Success"
          },
          "limite_rolagem": 0,
          "texto_efeitos_manual": [],
          "efeitos": [
            {
              "vida_mana": {
                "percentMaxHealth": 0.0,
                "percentMaxMana": 0.0,
                "percentCurHealth": 0.0,
                "percentCurMana": 0.0
              },
              "alvo": {
                "override": false,
                "tipo_override": {
                  "valor": 0,
                  "nome": "Self"
                },
                "tipo_default_serializado": {
                  "valor": 0,
                  "nome": "Self"
                }
              },
              "recompensas": {
                "ouro": {
                  "dar": false,
                  "retirar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
                },
                "experiencia": {
                  "dar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
                },
                "itens": {
                  "dar": false,
                  "pool_tipo": {
                    "valor": 2,
                    "nome": "Unassigned"
                  },
                  "quantidade_configurada": 1,
                  "tabelas": [],
                  "restricoes": {
                    "limitItemTypes": 0,
                    "possibleItemTypes": [],
                    "limitItemRarities": 0,
                    "possibleRarities": []
                  },
                  "sorteio_final": null,
                  "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
                },
                "status": {
                  "candidatos": [
                    {
                      "chave": "resources.assets:2545437",
                      "nome": "Enchanted Whetstone",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545437
                      },
                      "tipo": "EventStatus",
                      "descricao": "Weapon damage increased by {10,40}%\n\n<i><color=#808080>Captain Henry Irons would be proud!</color></i>",
                      "duracao": {
                        "valor": 1,
                        "nome": "Quest"
                      },
                      "status_tipo": {
                        "valor": 1,
                        "nome": "Fortune"
                      },
                      "modificadores": [
                        {
                          "atributo": {
                            "chave": "resources.assets:2544396",
                            "nome": "WeaponDamageMod",
                            "pptr": {
                              "m_FileID": 0,
                              "m_PathID": 2544396
                            },
                            "tipo": "CharacterAttribute"
                          },
                          "metodo": {
                            "valor": 0,
                            "nome": "Base"
                          },
                          "expressao": "{10, 40}",
                          "segunda_passagem": false
                        }
                      ]
                    }
                  ],
                  "sortear": false,
                  "quantidade_sorteada_configurada": 1,
                  "resultado_sorteado": null,
                  "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
                },
                "skills": []
              },
              "remocoes_status": []
            }
          ],
          "overrides": [],
          "batalha": {
            "iniciar": false,
            "manual": false,
            "referencia": {
              "chave": null,
              "nome": null,
              "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
            },
            "override": {
              "ForceRandomSuperUnique": 0,
              "DisableSuperUnique": 0,
              "DisableEnemyMods": 0,
              "UseRewardModifiers": 0,
              "ExpModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GoldModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "LootModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GauranteedLoot": [],
              "ForcedEnemies": [],
              "EnemyModApplications": [],
              "EnemyStatusApplications": [],
              "FillOutBattlePoints": 0,
              "OverrideBattlePoints": 0,
              "BattlePointValue": 8,
              "OverrideEnemyGroupPool": 0,
              "EnemyGroupPool": [],
              "OverrideEnemyTypePool": 0,
              "EnemyTypePool": [],
              "VictoryEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "FailureEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "EnemyTurnFirst": 0,
              "ForceMap": 0,
              "MapToForce": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "ovrEnemyStatusRefList": [],
              "ovrEnemyModRefList": []
            },
            "dados_recompensa_final": null,
            "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
          },
          "evento_encadeado": {
            "chave": null,
            "nome": null,
            "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
          }
        }
      ]
    },
    {
      "indice": 2,
      "condicoes": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      },
      "rolagem": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      },
      "hideOptionEffectText": 0,
      "efeitos": [
        {
          "indice": 1,
          "texto": "When you pick it up and turned the key set into its side, the device hums to life, sending out a powerful pulse that sends dust motes scattering and your hair standing on end. ",
          "resultado": {
            "valor": 0,
            "nome": "Success"
          },
          "limite_rolagem": 0,
          "texto_efeitos_manual": [],
          "efeitos": [
            {
              "vida_mana": {
                "percentMaxHealth": 0.0,
                "percentMaxMana": 0.0,
                "percentCurHealth": 0.0,
                "percentCurMana": 0.0
              },
              "alvo": {
                "override": false,
                "tipo_override": {
                  "valor": 0,
                  "nome": "Self"
                },
                "tipo_default_serializado": {
                  "valor": 0,
                  "nome": "Self"
                }
              },
              "recompensas": {
                "ouro": {
                  "dar": false,
                  "retirar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
                },
                "experiencia": {
                  "dar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
                },
                "itens": {
                  "dar": false,
                  "pool_tipo": {
                    "valor": 2,
                    "nome": "Unassigned"
                  },
                  "quantidade_configurada": 1,
                  "tabelas": [],
                  "restricoes": {
                    "limitItemTypes": 0,
                    "possibleItemTypes": [],
                    "limitItemRarities": 0,
                    "possibleRarities": []
                  },
                  "sorteio_final": null,
                  "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
                },
                "status": {
                  "candidatos": [
                    {
                      "chave": "resources.assets:2545428",
                      "nome": "Dwarven Force Generator",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545428
                      },
                      "tipo": "EventStatus",
                      "descricao": "All Teleport (Relocate, Teleport Self, Teleport Other, Escape) spells deal *0 physical damage on entry within 1 hex and knockback 2 hexes.\n\n<i><color=#808080>Crafted by Durn Spellbeard, widely known for his legendary entrances.</i></color>\n\n",
                      "duracao": {
                        "valor": 3,
                        "nome": "Permanent"
                      },
                      "status_tipo": {
                        "valor": 1,
                        "nome": "Fortune"
                      },
                      "modificadores": []
                    }
                  ],
                  "sortear": false,
                  "quantidade_sorteada_configurada": 1,
                  "resultado_sorteado": null,
                  "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
                },
                "skills": []
              },
              "remocoes_status": []
            }
          ],
          "overrides": [],
          "batalha": {
            "iniciar": false,
            "manual": false,
            "referencia": {
              "chave": null,
              "nome": null,
              "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
            },
            "override": {
              "ForceRandomSuperUnique": 0,
              "DisableSuperUnique": 0,
              "DisableEnemyMods": 0,
              "UseRewardModifiers": 0,
              "ExpModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GoldModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "LootModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GauranteedLoot": [],
              "ForcedEnemies": [],
              "EnemyModApplications": [],
              "EnemyStatusApplications": [],
              "FillOutBattlePoints": 0,
              "OverrideBattlePoints": 0,
              "BattlePointValue": 8,
              "OverrideEnemyGroupPool": 0,
              "EnemyGroupPool": [],
              "OverrideEnemyTypePool": 0,
              "EnemyTypePool": [],
              "VictoryEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "FailureEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "EnemyTurnFirst": 0,
              "ForceMap": 0,
              "MapToForce": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "ovrEnemyStatusRefList": [],
              "ovrEnemyModRefList": []
            },
            "dados_recompensa_final": null,
            "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
          },
          "evento_encadeado": {
            "chave": null,
            "nome": null,
            "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
          }
        }
      ]
    },
    {
      "indice": 3,
      "condicoes": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      },
      "rolagem": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      },
      "hideOptionEffectText": 0,
      "efeitos": [
        {
          "indice": 1,
          "texto": "As you pick up the Crystal Ball and peer into it, you gasp. The surface of the crystal shifts and swirls revealing an overhead view of the surrounding area. Your location, the winding tunnels, and even the far-off flicker of a goblin camp - it is like looking at a living map.",
          "resultado": {
            "valor": 0,
            "nome": "Success"
          },
          "limite_rolagem": 0,
          "texto_efeitos_manual": [],
          "efeitos": [
            {
              "vida_mana": {
                "percentMaxHealth": 0.0,
                "percentMaxMana": 0.0,
                "percentCurHealth": 0.0,
                "percentCurMana": 0.0
              },
              "alvo": {
                "override": false,
                "tipo_override": {
                  "valor": 0,
                  "nome": "Self"
                },
                "tipo_default_serializado": {
                  "valor": 0,
                  "nome": "Self"
                }
              },
              "recompensas": {
                "ouro": {
                  "dar": false,
                  "retirar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
                },
                "experiencia": {
                  "dar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
                },
                "itens": {
                  "dar": false,
                  "pool_tipo": {
                    "valor": 2,
                    "nome": "Unassigned"
                  },
                  "quantidade_configurada": 1,
                  "tabelas": [],
                  "restricoes": {
                    "limitItemTypes": 0,
                    "possibleItemTypes": [],
                    "limitItemRarities": 0,
                    "possibleRarities": []
                  },
                  "sorteio_final": null,
                  "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
                },
                "status": {
                  "candidatos": [
                    {
                      "chave": "resources.assets:2545421",
                      "nome": "Crystal Ball",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545421
                      },
                      "tipo": "EventStatus",
                      "descricao": "Gain {.5,1.5}% bonus damage for every hex between you and your target. Skill range increased by {1,3}.\n\n<i><color=#808080>It doesn't show the future but a clearer picture of the present.</color></i>\n",
                      "duracao": {
                        "valor": 3,
                        "nome": "Permanent"
                      },
                      "status_tipo": {
                        "valor": 1,
                        "nome": "Fortune"
                      },
                      "modificadores": [
                        {
                          "atributo": {
                            "chave": "resources.assets:2544394",
                            "nome": "PerHexRangeDamageBonus",
                            "pptr": {
                              "m_FileID": 0,
                              "m_PathID": 2544394
                            },
                            "tipo": "CharacterAttribute"
                          },
                          "metodo": {
                            "valor": 0,
                            "nome": "Base"
                          },
                          "expressao": "{.5,1.5}",
                          "segunda_passagem": false
                        },
                        {
                          "atributo": {
                            "chave": "resources.assets:2544493",
                            "nome": "RangeTypeAdderRanged",
                            "pptr": {
                              "m_FileID": 0,
                              "m_PathID": 2544493
                            },
                            "tipo": "CharacterAttribute"
                          },
                          "metodo": {
                            "valor": 0,
                            "nome": "Base"
                          },
                          "expressao": "{1,3}",
                          "segunda_passagem": false
                        }
                      ]
                    }
                  ],
                  "sortear": false,
                  "quantidade_sorteada_configurada": 1,
                  "resultado_sorteado": null,
                  "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
                },
                "skills": []
              },
              "remocoes_status": []
            }
          ],
          "overrides": [],
          "batalha": {
            "iniciar": false,
            "manual": false,
            "referencia": {
              "chave": null,
              "nome": null,
              "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
            },
            "override": {
              "ForceRandomSuperUnique": 0,
              "DisableSuperUnique": 0,
              "DisableEnemyMods": 0,
              "UseRewardModifiers": 0,
              "ExpModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GoldModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "LootModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GauranteedLoot": [],
              "ForcedEnemies": [],
              "EnemyModApplications": [],
              "EnemyStatusApplications": [],
              "FillOutBattlePoints": 0,
              "OverrideBattlePoints": 0,
              "BattlePointValue": 8,
              "OverrideEnemyGroupPool": 0,
              "EnemyGroupPool": [],
              "OverrideEnemyTypePool": 0,
              "EnemyTypePool": [],
              "VictoryEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "FailureEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "EnemyTurnFirst": 0,
              "ForceMap": 0,
              "MapToForce": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "ovrEnemyStatusRefList": [],
              "ovrEnemyModRefList": []
            },
            "dados_recompensa_final": null,
            "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
          },
          "evento_encadeado": {
            "chave": null,
            "nome": null,
            "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
          }
        }
      ]
    }
  ]
}
```



## 28. Magic Mirror — resources.assets:2545625

Chave: `resources.assets:2545625`. GUID real: `1f0f2b4d-7ec4-4b10-b489-f382c460efeb`. Asset: `Magic Mirror - Victory`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 1; ações: 1; overrides: 0. Origem: `events/magic mirror - victory`.

VEREDITO PROPOSTO: MELHORAR — natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

Remover a mudança injustificada do presente para o passado na descrição do término da batalha.

### Texto atual → proposta exata

Campo: `texto`.

Atual (campo completo):
```json
"The <violet><b><incr>Magic Mirror</incr></b></violet> explodes into a shower of glinting shards, the twisted reflections shrieking as they disintegrate along with their prison. The room is plunged into an eerie silence as the echoes of the battle faded away.\n\nYou look around, panting heavily, and find a single shard of the mirror, still intact. Your dark reflection is trapped within it, now just an imprisoned ghost of malice."
```

PROPOSTA EXATA (campo completo):
```json
"The <violet><b><incr>Magic Mirror</incr></b></violet> explodes into a shower of glinting shards, the twisted reflections shrieking as they disintegrate along with their prison. The room is plunged into an eerie silence as the echoes of the battle fade away.\n\nYou look around, panting heavily, and find a single shard of the mirror, still intact. Your dark reflection is trapped within it, now just an imprisoned ghost of malice."
```

Justificativa: Remover a mudança injustificada do presente para o passado na descrição do término da batalha.

### Todos os textos atuais e decisão por campo

`texto` — MELHORAR conforme proposta acima:
```json
"The <violet><b><incr>Magic Mirror</incr></b></violet> explodes into a shower of glinting shards, the twisted reflections shrieking as they disintegrate along with their prison. The room is plunged into an eerie silence as the echoes of the battle faded away.\n\nYou look around, panting heavily, and find a single shard of the mirror, still intact. Your dark reflection is trapped within it, now just an imprisoned ghost of malice."
```

`texto_resultados_possiveis` — MANTER:
```json
""
```

`campos_originais/promptToSelectCharacter` — MANTER:
```json
""
```

`campos_originais/characterSelectedText` — MANTER:
```json
""
```

`opcoes/0/titulo` — MANTER:
```json
"Take"
```

`opcoes/0/texto` — MANTER:
```json
"Grab a shard of the <violet><b><incr>Magic Mirror</incr></b></violet>. "
```

`opcoes/0/rolagem/texto_misterioso` — MANTER:
```json
""
```

`opcoes/0/efeitos/0/texto` — MANTER:
```json
"With an odd sense of satisfaction, you claim the shard, a strange token from a battle that blurred the lines between reality and reflection. It serves as a haunting reminder of the duality within you, a shadowy testament of the darkness confronted and overcome.\r"
```

### Anomalias, cautelas e limites

- Ação padrão tem experiencia.dar=true e razão 1.0, além de Mirror Shard (2545455). XP final permanece NULL e pode ser convertido em ouro; não prometer valor nem XP garantido.

- CR final no texto da ação e espaço final na opção permanecem; UI NAO_EXERCITADO.

- `disabled=0` é configuração; disponibilidade efetiva NAO_EXERCITADO. Nenhuma remoção/reativação proposta.

- Textos vazios auditados: 4. Campos: `texto_resultados_possiveis`, `campos_originais/promptToSelectCharacter`, `campos_originais/characterSelectedText`, `opcoes/0/rolagem/texto_misterioso`.

- NULL preservados: 13; motivos por caminho no anexo de auditoria `EV-R2-FORAPOOL-b02-parte05.md`. Inclui projeção redundante de recompensa: não somar como efeitos extras.

- Referências nulas projetadas: 2. Combate/RNG/quantidade final/status aplicado/UI: NAO_EXERCITADO — somente configuração offline disponível.

- Opção 1: ocultar sem requisitos=false; ocultar por status=[]; hideOptionEffectText=0. Exibição real NAO_EXERCITADO.

### Referências consultadas e encadeamentos de entrada

Configurações de candidato não são concessões executadas. Catálogo consultado por chave, sem expandir/editar as definições externas.
```json
{
  "referencias": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0]",
      "chave": "resources.assets:2545455",
      "nome": "Mirror Shard",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Mirror Shard",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545455",
      "nome": "Mirror Shard",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Mirror Shard",
      "registro_catalogo": true,
      "resumo_catalogo": true
    }
  ],
  "pptrs_nao_nulos": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545455
      },
      "chave": "resources.assets:2545455",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Mirror Shard"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545455
      },
      "chave": "resources.assets:2545455",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Mirror Shard"
    }
  ],
  "referencias_nulas": [
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.referencia",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.opcoes[0].efeitos[0].evento_encadeado",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    }
  ],
  "referencias_entrada": [
    {
      "fonte": "eventos.json",
      "origem": "resources.assets:2545626",
      "campo": "$.opcoes[0].efeitos[1].batalha.override.VictoryEvent"
    },
    {
      "fonte": "eventos.json",
      "origem": "resources.assets:2545626",
      "campo": "$.opcoes[1].efeitos[0].batalha.override.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545626",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[0].eventActions[1].battleOverrideInfo.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545626",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[1].eventActions[0].battleOverrideInfo.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[95]"
    }
  ]
}
```

### Condições, modos e configuração completa das ações

```json
{
  "condicoes": {
    "disabled": 0,
    "EditorOnly": 0,
    "allowOnAllNodeTypes": 0,
    "allowedNodeTypes": [
      7
    ],
    "requiredStatusesToSpawn": [],
    "allowOnAllTerrainTypes": 1,
    "allowedTerrainTypes": [],
    "allowAtAllTimesOfDay": 0,
    "allowedTimeOfDay": 1,
    "allowAtAllLevels": 1,
    "minLevel": 1,
    "terrainTypesAllowedAtAnyTime": [
      4,
      3
    ],
    "KeepInDeckWhenUsed": 0,
    "isLesserEvent": 0,
    "LeadsToFortune": 1
  },
  "modos": [
    {
      "valor": 0,
      "nome": "Campaign"
    },
    {
      "valor": 1,
      "nome": "Roguelike"
    }
  ],
  "historia": {
    "valor": 0,
    "nome": "NonStoryOnly"
  },
  "full_release": {
    "valor": 0,
    "nome": "None"
  },
  "apresentacao_autoral": {
    "AutoStartBattle": 0,
    "targetType": 0,
    "characterPool": 0,
    "showContinueBtnInsteadOfSingleOption": 0,
    "disableAutoChoose": 1,
    "RefEventStatuses": []
  },
  "opcoes": [
    {
      "indice": 1,
      "condicoes": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      },
      "rolagem": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      },
      "hideOptionEffectText": 0,
      "efeitos": [
        {
          "indice": 1,
          "texto": "With an odd sense of satisfaction, you claim the shard, a strange token from a battle that blurred the lines between reality and reflection. It serves as a haunting reminder of the duality within you, a shadowy testament of the darkness confronted and overcome.\r",
          "resultado": {
            "valor": 0,
            "nome": "Success"
          },
          "limite_rolagem": 0,
          "texto_efeitos_manual": [],
          "efeitos": [
            {
              "vida_mana": {
                "percentMaxHealth": 0.0,
                "percentMaxMana": 0.0,
                "percentCurHealth": 0.0,
                "percentCurMana": 0.0
              },
              "alvo": {
                "override": false,
                "tipo_override": {
                  "valor": 0,
                  "nome": "Self"
                },
                "tipo_default_serializado": {
                  "valor": 0,
                  "nome": "Self"
                }
              },
              "recompensas": {
                "ouro": {
                  "dar": false,
                  "retirar": false,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
                },
                "experiencia": {
                  "dar": true,
                  "razao": 1.0,
                  "quantidade_final": null,
                  "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
                },
                "itens": {
                  "dar": false,
                  "pool_tipo": {
                    "valor": 2,
                    "nome": "Unassigned"
                  },
                  "quantidade_configurada": 1,
                  "tabelas": [],
                  "restricoes": {
                    "limitItemTypes": 0,
                    "possibleItemTypes": [],
                    "limitItemRarities": 0,
                    "possibleRarities": []
                  },
                  "sorteio_final": null,
                  "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
                },
                "status": {
                  "candidatos": [
                    {
                      "chave": "resources.assets:2545455",
                      "nome": "Mirror Shard",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545455
                      },
                      "tipo": "EventStatus",
                      "descricao": "Summon a Dark clone of yourself but it fights for you. \n\n<i><color=#808080>You hold a shard of your shattered reflection!</color></i>\n",
                      "duracao": {
                        "valor": 3,
                        "nome": "Permanent"
                      },
                      "status_tipo": {
                        "valor": 1,
                        "nome": "Fortune"
                      },
                      "modificadores": []
                    }
                  ],
                  "sortear": false,
                  "quantidade_sorteada_configurada": 1,
                  "resultado_sorteado": null,
                  "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
                },
                "skills": []
              },
              "remocoes_status": []
            }
          ],
          "overrides": [],
          "batalha": {
            "iniciar": false,
            "manual": false,
            "referencia": {
              "chave": null,
              "nome": null,
              "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
            },
            "override": {
              "ForceRandomSuperUnique": 0,
              "DisableSuperUnique": 0,
              "DisableEnemyMods": 0,
              "UseRewardModifiers": 0,
              "ExpModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GoldModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "LootModifier": "Mathf.Max(0, 5 - (TurnCount - 1)) * 100",
              "GauranteedLoot": [],
              "ForcedEnemies": [],
              "EnemyModApplications": [],
              "EnemyStatusApplications": [],
              "FillOutBattlePoints": 0,
              "OverrideBattlePoints": 0,
              "BattlePointValue": 8,
              "OverrideEnemyGroupPool": 0,
              "EnemyGroupPool": [],
              "OverrideEnemyTypePool": 0,
              "EnemyTypePool": [],
              "VictoryEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "FailureEvent": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "EnemyTurnFirst": 0,
              "ForceMap": 0,
              "MapToForce": {
                "m_FileID": 0,
                "m_PathID": 0
              },
              "ovrEnemyStatusRefList": [],
              "ovrEnemyModRefList": []
            },
            "dados_recompensa_final": null,
            "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
          },
          "evento_encadeado": {
            "chave": null,
            "nome": null,
            "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
          }
        }
      ]
    }
  ]
}
```


