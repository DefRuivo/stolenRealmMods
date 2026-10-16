# EV-R2-FORAPOOL-b04 — parte 02: eventos 64–70

Fonte: C:\dev\stolen-realm\docs\cobertura\EV-R1/eventos.json; ordem: C:\dev\stolen-realm\docs\cobertura\EV-R1/lote-NotInEventPool-v2.md. Contagem desta parte: 7/7 eventos. Todos os vereditos são PROPOSTOS, aprovação do dono PENDENTE.

Coordenadas JSON Pointer com índices base 0; índices de leitura de opções/ações continuam base 1. Strings exibidas como literais JSON preservam CR/LF, espaços e tags. Catálogo: git 097f950:docs/cobertura/EV-R1/catalogo-referencias.json; provenance completa na parte05 e fontes-hashes.json.

## 64. The runes of the Ymir

Chave: `resources.assets:2545781`; GUID: `57998f83-17c5-4e55-bf59-f56403d0ce14`; nome_asset: Ymir Rune, Courage.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording: corrigir o tempo verbal e a capitalização de ice; adequar o prompt ao monólito, sem alterar a sequência de combates.

### Análise específica

- A narrativa descreve a queda do treant e a próxima aparição do lobo. A opção Touch inicia combate; Leave tem ação com texto vazio. Não inventar texto para essa saída.

- Prompt de seleção fala em pleas sem personagem suplicante na cena. Exibição efetiva desse campo: NAO_EXERCITADO.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/opcoes/0/texto`

Texto atual (literal completo):

```json
"Reach out and place the palm of your hand on the Ice."
```

PROPOSTA EXATA (literal completo):

```json
"Reach out and place the palm of your hand on the ice."
```

Justificativa: Substantivo comum, não nome próprio.

Campo `/opcoes/0/efeitos/0/texto`

Texto atual (literal completo):

```json
"As before, you reach out and placed your palm on the ice. The cool sensation envelops you, as though you were stepping into a winter’s night. It is soothing and peaceful, a calm before the storm.\r\n\r\nAnd storm it does. A howl echoes through the icy landscape, freezing you in place. From the blizzard emerges a wolf, its fur white as snow and eyes glowing like the pale moon. Blue runes trace its form, glowing brightly with arcane light."
```

PROPOSTA EXATA (literal completo):

```json
"As before, you reach out and place your palm on the ice. The cool sensation envelops you, as though you were stepping into a winter’s night. It is soothing and peaceful, a calm before the storm.\r\n\r\nAnd storm it does. A howl echoes through the icy landscape, freezing you in place. From the blizzard emerges a wolf, its fur white as snow and eyes glowing like the pale moon. Blue runes trace its form, glowing brightly with arcane light."
```

Justificativa: Concordância temporal com a narração no presente.

Campo `/campos_originais/promptToSelectCharacter`

Texto atual (literal completo):

```json
"Who will listen to his pleas?"
```

PROPOSTA EXATA (literal completo):

```json
"Who will approach the rune?"
```

Justificativa: Remove pedido de socorro deslocado sem afirmar escolha já efetuada.

### Textos atuais não alterados

Campo `/texto`

```json
"A sudden gust of wind sweeps through the clearing, chilling you to the bone as the treant falls, dissolving into a whirlwind of frost.\n\nTurning your attention back to the ancient rune, you observe it shift once more, the intricate markings dancing into a new pattern."
```

Campo `/texto_resultados_possiveis` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/campos_originais/characterSelectedText` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/titulo`

```json
"Touch"
```

Campo `/opcoes/0/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/1/titulo`

```json
"Leave"
```

Campo `/opcoes/1/texto`

```json
"You have no time for these ancient markings."
```

Campo `/opcoes/1/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/1/efeitos/0/texto` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

### Anomalias, disponibilidade e referências

disabled=0; opções=2; ações=2; NULL auditados=26; refs nulas projetadas=4. Todos os caminhos e motivos destes NULL estão individualizados na parte05 e propostas-auditadas.json.

Condições/modos/prefab (literais, sem escolha de variante):

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
    "allowOnAllTerrainTypes": 0,
    "allowedTerrainTypes": [
      7
    ],
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
  "prefab": {
    "Guid": "c8f074f5fa9927c4f80ff8f6fa02e346",
    "Path": "Island Hex Pieces\\Events\\Ymir Rune, Courage 1"
  }
}
```

Opções ocultas: [
  {
    "opcao": 1,
    "ocultar_sem_requisitos": false,
    "ocultar_se_status": [],
    "hideOptionEffectText": 0
  },
  {
    "opcao": 2,
    "ocultar_sem_requisitos": false,
    "ocultar_se_status": [],
    "hideOptionEffectText": 0
  }
]. hideOptionEffectText oculta texto de efeito, não necessariamente a opção. Exibição efetiva: NAO_EXERCITADO.

Referências entrantes explícitas recuperadas no canônico/catálogo (sem alegação de varredura de código/runtime):

```json
[
  {
    "origem": "resources.assets:2545783",
    "tipo": "PartyEvent",
    "campo": "/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "destino": "resources.assets:2545781"
  },
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/249",
    "destino": "resources.assets:2545781"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[
  {
    "opcao": 1,
    "titulo": "Touch",
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
    "acoes": [
      {
        "indice": 1,
        "resultado": {
          "valor": 0,
          "nome": "Success"
        },
        "limite_rolagem": 0,
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
                "OverrideEnemyName": 1,
                "NameOverride": "Trial of Courage",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545308
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 1
              },
              {
                "OverrideEnemyName": 0,
                "NameOverride": "",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545307
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 0
              },
              {
                "OverrideEnemyName": 0,
                "NameOverride": "",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545307
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 0
              },
              {
                "OverrideEnemyName": 0,
                "NameOverride": "",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545309
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 0
              },
              {
                "OverrideEnemyName": 0,
                "NameOverride": "",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545309
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 0
              },
              {
                "OverrideEnemyName": 0,
                "NameOverride": "",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545309
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 0
              },
              {
                "OverrideEnemyName": 0,
                "NameOverride": "",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545309
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 0
              },
              {
                "OverrideEnemyName": 0,
                "NameOverride": "",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545309
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
            "OverrideEnemyGroupPool": 1,
            "EnemyGroupPool": [
              48
            ],
            "OverrideEnemyTypePool": 0,
            "EnemyTypePool": [],
            "VictoryEvent": {
              "m_FileID": 0,
              "m_PathID": 2545780
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
    "opcao": 2,
    "titulo": "Leave",
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
    "acoes": [
      {
        "indice": 1,
        "resultado": {
          "valor": 0,
          "nome": "Success"
        },
        "limite_rolagem": 0,
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
```

NAO_EXERCITADO: runtime/UI, disponibilidade, RNG, aplicação final de status, ouro/XP/loot finais e combate, porque a tarefa proíbe execução do jogo. Referência nula com motivo m_PathID=0 permanece distinta de resultado não exercitado.

## 65. The runes of the Ymir

Chave: `resources.assets:2545783`; GUID: `180d0256-b0b8-42bd-a0b7-d87bbcdcb874`; nome_asset: Ymir Rune, Honor.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording: padronizar rune/ice e retirar o prompt de súplica deslocado; manter o elo polar bear → treant.

### Análise específica

- O título visível é The runes of the Ymir, mas nome_asset é Ymir Rune, Honor. Não confundir com a chave disabled 2545782.

- A variante possui duas opções, incluindo saída com texto próprio; não eliminar por título repetido.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/texto_resultados_possiveis`

Texto atual (literal completo):

```json
"Will you touch the Rune?"
```

PROPOSTA EXATA (literal completo):

```json
"Will you touch the rune?"
```

Justificativa: rune é substantivo comum neste contexto.

Campo `/opcoes/0/texto`

Texto atual (literal completo):

```json
"You reach out and place the palm of your hand on the Ice."
```

PROPOSTA EXATA (literal completo):

```json
"You reach out and place the palm of your hand on the ice."
```

Justificativa: Capitalização consistente.

Campo `/opcoes/1/efeitos/0/texto`

Texto atual (literal completo):

```json
"You turn away from the Runes and walk on."
```

PROPOSTA EXATA (literal completo):

```json
"You turn away from the runes and walk on."
```

Justificativa: Capitalização consistente.

Campo `/campos_originais/promptToSelectCharacter`

Texto atual (literal completo):

```json
"Who will listen to his pleas?"
```

PROPOSTA EXATA (literal completo):

```json
"Who will approach the rune?"
```

Justificativa: Não há personagem suplicante na cena.

### Textos atuais não alterados

Campo `/texto`

```json
"With a resounding cry and a final, powerful swing, you strike the final blow. The polar bear does not fall, but instead, it shatters into a whirlwind of frost, leaving nothing behind but an empty silence.\n\n\nTurning back to the rune, you watch with wide eyes as it alters itself, the ancient markings transforming, shifting into a pattern unknown to you. Despite the change, the pull is still there, the rune calling out to you in a silent whisper. "
```

Campo `/campos_originais/characterSelectedText` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/titulo`

```json
"Touch"
```

Campo `/opcoes/0/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/efeitos/0/texto`

```json
"An icy chill runs through you, a sensation akin to the one you'd felt earlier but colder, more potent.\n\n\nJust as you become lost in the sensation, a loud, thunderous sound jolts you out of your reverie. A treant, mighty and tall, its bark as ancient as the Ymir themselves, emerges from the mist, its branches crashing and rustling in a cacophony of sounds.\n"
```

Campo `/opcoes/1/titulo`

```json
"Leave"
```

Campo `/opcoes/1/texto`

```json
"You have no time for these ancient markings."
```

Campo `/opcoes/1/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

### Anomalias, disponibilidade e referências

disabled=0; opções=2; ações=2; NULL auditados=26; refs nulas projetadas=4. Todos os caminhos e motivos destes NULL estão individualizados na parte05 e propostas-auditadas.json.

Condições/modos/prefab (literais, sem escolha de variante):

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
    "allowOnAllTerrainTypes": 0,
    "allowedTerrainTypes": [
      7
    ],
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
  "prefab": {
    "Guid": "eeb71aace06cd604a8da1600f161c653",
    "Path": "Island Hex Pieces\\Events\\Ymir Rune, Honor 1"
  }
}
```

Opções ocultas: [
  {
    "opcao": 1,
    "ocultar_sem_requisitos": false,
    "ocultar_se_status": [],
    "hideOptionEffectText": 0
  },
  {
    "opcao": 2,
    "ocultar_sem_requisitos": false,
    "ocultar_se_status": [],
    "hideOptionEffectText": 0
  }
]. hideOptionEffectText oculta texto de efeito, não necessariamente a opção. Exibição efetiva: NAO_EXERCITADO.

Referências entrantes explícitas recuperadas no canônico/catálogo (sem alegação de varredura de código/runtime):

```json
[
  {
    "origem": "resources.assets:2545785",
    "tipo": "PartyEvent",
    "campo": "/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "destino": "resources.assets:2545783"
  },
  {
    "origem": "resources.assets:2545784",
    "tipo": "PartyEvent",
    "campo": "/eventOptions/0/eventActions/0/chainedEvent",
    "destino": "resources.assets:2545783"
  },
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/251",
    "destino": "resources.assets:2545783"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[
  {
    "opcao": 1,
    "titulo": "Touch",
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
    "acoes": [
      {
        "indice": 1,
        "resultado": {
          "valor": 0,
          "nome": "Success"
        },
        "limite_rolagem": 0,
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
                "OverrideEnemyName": 1,
                "NameOverride": "Trial of Honor",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545233
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 1
              },
              {
                "OverrideEnemyName": 0,
                "NameOverride": "",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545231
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 0
              },
              {
                "OverrideEnemyName": 0,
                "NameOverride": "",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545231
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 0
              },
              {
                "OverrideEnemyName": 0,
                "NameOverride": "",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545231
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 0
              },
              {
                "OverrideEnemyName": 0,
                "NameOverride": "",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545231
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
            "OverrideEnemyGroupPool": 1,
            "EnemyGroupPool": [
              48
            ],
            "OverrideEnemyTypePool": 0,
            "EnemyTypePool": [],
            "VictoryEvent": {
              "m_FileID": 0,
              "m_PathID": 2545781
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
    "opcao": 2,
    "titulo": "Leave",
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
    "acoes": [
      {
        "indice": 1,
        "resultado": {
          "valor": 0,
          "nome": "Success"
        },
        "limite_rolagem": 0,
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
```

NAO_EXERCITADO: runtime/UI, disponibilidade, RNG, aplicação final de status, ouro/XP/loot finais e combate, porque a tarefa proíbe execução do jogo. Referência nula com motivo m_PathID=0 permanece distinta de resultado não exercitado.

## 66. The Spell Council

Chave: `resources.assets:2545747`; GUID: `bfe5418a-b839-4c4d-881a-08805a2a4310`; nome_asset: The Spell Council - Victory.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording: corrigir artigo/tempo verbal e prompt de ogro sem relação com o Mad Mage.

### Análise específica

- Configuração de status: Rune of Refreshment. giveGold=false, embora razão de ouro seja 15.0; giveItems=false. A runa narrada não comprova item de inventário.

- characterSelectedText=Good luck [name]... permanece: não há prova de defeito além de frase genérica; preservar placeholder. Nenhuma alteração na descrição do status.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/opcoes/0/efeitos/0/texto`

Texto atual (literal completo):

```json
"With grand flourish, the Mad Mage conjures a radiant rune that floats down to your outstretched hand. \n\nIt seems to be carved from an iridescent material, neither stone nor metal, yet harder than diamond and as shimmering as purest silver. It is adorned with a series of intricate glyphs and symbols that danced and pulsed with a serene, soft light."
```

PROPOSTA EXATA (literal completo):

```json
"With a grand flourish, the Mad Mage conjures a radiant rune that floats down to your outstretched hand. \n\nIt seems to be carved from an iridescent material, neither stone nor metal, yet harder than diamond and as shimmering as purest silver. It is adorned with a series of intricate glyphs and symbols that dance and pulse with a serene, soft light."
```

Justificativa: Artigo indefinido necessário.; Manter a narração no presente.

Campo `/campos_originais/promptToSelectCharacter`

Texto atual (literal completo):

```json
"Does anyone owe this Ogre money?"
```

PROPOSTA EXATA (literal completo):

```json
"Who will accept the Mad Mage's gift?"
```

Justificativa: Ogro e dívida pertencem a outra cena; proposta apenas textual.

### Textos atuais não alterados

Campo `/texto`

```json
"Just as you are catching your breath after battle, a vortex of magical energy whirls into existence before you, coalescing into the familiar form of the Mad Mage. He materializes fully, an expression of bewildered relief etched across his face. His eyes sweep the scene before landing on you, then widen in recognition.\n\n\"Is it... is it truly so?\" he whispers, his voice carrying an echo of the storm that freed him. \"Am I finally free of those meddlesome wizards?\" A crazed laugh breaks from his lips, full of relief and disbelief. \"I can hardly believe it! Free, after all this time!\"\n\nTurning to you, the Mad Mage's manic laughter subsides, replaced with an intense, scrutinizing gaze. \"You have my gratitude, adventurer,\" he says, his tone serious for the first time. \"You have done more than you know. Take this as a token of my gratitude.\"\n\n"
```

Campo `/texto_resultados_possiveis` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/campos_originais/characterSelectedText`

```json
"Good luck [name]..."
```

Campo `/opcoes/0/titulo`

```json
"Accept"
```

Campo `/opcoes/0/texto`

```json
"Claim your reward."
```

Campo `/opcoes/0/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

### Anomalias, disponibilidade e referências

disabled=0; opções=1; ações=1; NULL auditados=13; refs nulas projetadas=2. Todos os caminhos e motivos destes NULL estão individualizados na parte05 e propostas-auditadas.json.

Condições/modos/prefab (literais, sem escolha de variante):

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
  "prefab": {
    "Guid": "5099dc17509294c448f79a416f0135d9",
    "Path": "Island Hex Pieces\\Events\\Unleashed"
  }
}
```

Opções ocultas: [
  {
    "opcao": 1,
    "ocultar_sem_requisitos": false,
    "ocultar_se_status": [],
    "hideOptionEffectText": 0
  }
]. hideOptionEffectText oculta texto de efeito, não necessariamente a opção. Exibição efetiva: NAO_EXERCITADO.

Referências entrantes explícitas recuperadas no canônico/catálogo (sem alegação de varredura de código/runtime):

```json
[
  {
    "origem": "resources.assets:2545748",
    "tipo": "PartyEvent",
    "campo": "/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "destino": "resources.assets:2545747"
  },
  {
    "origem": "resources.assets:2545749",
    "tipo": "PartyEvent",
    "campo": "/eventOptions/1/eventActions/0/battleOverrideInfo/VictoryEvent",
    "destino": "resources.assets:2545747"
  },
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/217",
    "destino": "resources.assets:2545747"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[
  {
    "opcao": 1,
    "titulo": "Accept",
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
    "acoes": [
      {
        "indice": 1,
        "resultado": {
          "valor": 0,
          "nome": "Success"
        },
        "limite_rolagem": 0,
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
                "razao": 15.0,
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
                  "limitItemTypes": 1,
                  "possibleItemTypes": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5,
                    7
                  ],
                  "limitItemRarities": 1,
                  "possibleRarities": [
                    3,
                    4
                  ]
                },
                "sorteio_final": null,
                "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
              },
              "status": {
                "candidatos": [
                  {
                    "chave": "resources.assets:2545466",
                    "nome": "Rune of Refreshment",
                    "pptr": {
                      "m_FileID": 0,
                      "m_PathID": 2545466
                    },
                    "tipo": "EventStatus",
                    "descricao": "Reset all cooldowns. Cost 75% of Max Mana. 1 charge per battle.\n\n<i><color=#808080>A tremendous sacrifice is required to power this inert rune.</color></i>",
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
```

NAO_EXERCITADO: runtime/UI, disponibilidade, RNG, aplicação final de status, ouro/XP/loot finais e combate, porque a tarefa proíbe execução do jogo. Referência nula com motivo m_PathID=0 permanece distinta de resultado não exercitado.

## 67. The Spell Council

Chave: `resources.assets:2545749`; GUID: `b033c3a9-ab04-4d4b-9961-d4846e25261f`; nome_asset: The Spell Council.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording: rotular a recusa por sua ação e alinhar o prompt ao conselho.

### Análise específica

- Agree configura o status Quest The Mad Mage - Part 4; a opção de desafio inicia combate. Não trocar recusa por saída pacífica.

- O conselho exige captura, mas a cadeia Unleashed narra a morte do mago. Tensão narrativa sinalizada, não inventar mecânica de captura nem mudar condição/recompensa.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/opcoes/1/titulo`

Texto atual (literal completo):

```json
"Oblivion "
```

PROPOSTA EXATA (literal completo):

```json
"Defy"
```

Justificativa: Nomeia a escolha de desafiar, não um resultado prometido; elimina espaço terminal. Proposta opcional sujeita ao dono.

Campo `/campos_originais/promptToSelectCharacter`

Texto atual (literal completo):

```json
"Who will listen to his pleas?"
```

PROPOSTA EXATA (literal completo):

```json
"Who will answer the Spell Council?"
```

Justificativa: Adequa o sujeito ao conselho de três magos.

### Textos atuais não alterados

Campo `/texto`

```json
"You come under the heavy gaze of three formidable wizards, each adorned in robes representing their affinity for distinct elements: fire, ice, and lightning.\n\nA remnant of the elemental chains' power pulses within you, resonating with the magical auras of the wizards. The tallest of the trio, a stern woman wreathed in an aura of flickering flames, steps forward.\n\n\n\"You,\" she declares, her voice echoing, \"you have released the Mad Mage.\"\n\n\nCaught off guard, you try to explain, to justify your actions. But the icy-eyed wizard silences you with a frost-laden hand. \"You have unleashed chaos into the world,\" he says, his voice as chilling as his gaze. \"And chaos must be subdued.\"\n\n\nThe third wizard, shrouded in an aura of crackling electricity, steps in. \"You have a task, adventurer,\" he declares, sparks dancing around him as he speaks. \"You must capture the Mad Mage and return him to his chains. He must pay for the turmoil he has caused.\"\n\n\n\"And if you fail...\" The fiery wizard's voice drops, her gaze harder than a dragon's scales. \"Then you will find oblivion a lenient fate compared to what we shall impose.\""
```

Campo `/texto_resultados_possiveis` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/campos_originais/characterSelectedText` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/titulo`

```json
"Agree"
```

Campo `/opcoes/0/texto`

```json
"You will bring the Mad Mage to justice."
```

Campo `/opcoes/0/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/efeitos/0/texto`

```json
"With a determined nod, you accept the charge, your resolve solidifying under the heavy gaze of the elemental wizards. You will find the Mad Mage. You will right your wrong."
```

Campo `/opcoes/1/texto`

```json
"You'll not be told what to do."
```

Campo `/opcoes/1/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/1/efeitos/0/texto`

```json
"Surprise flits across the wizards' faces, their expressions hardening as you refuse. \"You dare defy us?!\" "
```

### Anomalias, disponibilidade e referências

disabled=0; opções=2; ações=2; NULL auditados=26; refs nulas projetadas=4. Todos os caminhos e motivos destes NULL estão individualizados na parte05 e propostas-auditadas.json.

Condições/modos/prefab (literais, sem escolha de variante):

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
  "prefab": {
    "Guid": "819d4b8e0c894874c91b0ee54c438f27",
    "Path": "Island Hex Pieces\\Events\\The Spell Council"
  }
}
```

Opções ocultas: [
  {
    "opcao": 1,
    "ocultar_sem_requisitos": false,
    "ocultar_se_status": [],
    "hideOptionEffectText": 0
  },
  {
    "opcao": 2,
    "ocultar_sem_requisitos": false,
    "ocultar_se_status": [],
    "hideOptionEffectText": 0
  }
]. hideOptionEffectText oculta texto de efeito, não necessariamente a opção. Exibição efetiva: NAO_EXERCITADO.

Referências entrantes explícitas recuperadas no canônico/catálogo (sem alegação de varredura de código/runtime):

```json
[
  {
    "origem": "resources.assets:2545518",
    "tipo": "EventStatus",
    "campo": "/ForcedNextEvent",
    "destino": "resources.assets:2545749"
  },
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/216",
    "destino": "resources.assets:2545749"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[
  {
    "opcao": 1,
    "titulo": "Agree",
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
    "acoes": [
      {
        "indice": 1,
        "resultado": {
          "valor": 0,
          "nome": "Success"
        },
        "limite_rolagem": 0,
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
                    "chave": "resources.assets:2545519",
                    "nome": "The Mad Mage - Part 4",
                    "pptr": {
                      "m_FileID": 0,
                      "m_PathID": 2545519
                    },
                    "tipo": "EventStatus",
                    "descricao": "",
                    "duracao": {
                      "valor": 3,
                      "nome": "Permanent"
                    },
                    "status_tipo": {
                      "valor": 3,
                      "nome": "Quest"
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
    "opcao": 2,
    "titulo": "Oblivion ",
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
    "acoes": [
      {
        "indice": 1,
        "resultado": {
          "valor": 0,
          "nome": "Success"
        },
        "limite_rolagem": 0,
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
                "OverrideEnemyName": 1,
                "NameOverride": "Master of Flame",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545236
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 1
              },
              {
                "OverrideEnemyName": 1,
                "NameOverride": "Master of Frost",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545237
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 1
              },
              {
                "OverrideEnemyName": 1,
                "NameOverride": "Master of Storm",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545238
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 1
              },
              {
                "OverrideEnemyName": 0,
                "NameOverride": "",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545239
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 0
              },
              {
                "OverrideEnemyName": 0,
                "NameOverride": "",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545235
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 0
              },
              {
                "OverrideEnemyName": 0,
                "NameOverride": "",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545234
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
              "m_PathID": 2545747
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
```

NAO_EXERCITADO: runtime/UI, disponibilidade, RNG, aplicação final de status, ouro/XP/loot finais e combate, porque a tarefa proíbe execução do jogo. Referência nula com motivo m_PathID=0 permanece distinta de resultado não exercitado.

## 68. The Sultan

Chave: `resources.assets:2545635`; GUID: `dce2e114-c816-4ffd-a0fa-5263c0395782`; nome_asset: 4 - The Sultan End.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MANTER; natureza: nenhuma. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MANTER: epílogo inteligível do Sultan, sem erro objetivo que justifique reescrita neste lote.

### Análise específica

- Zero opções é dado autoral, não falta de extração. O texto narra obtenção de amuleto e uma memória; não contém configuração de recompensa em opções.

- Preservar br/> e quebras literais; a apresentação efetiva e a posse do amuleto no runtime não foram exercitadas.

### Propostas exatas (nenhuma aplicação autorizada)

Nenhuma substituição proposta. Textos atuais completos preservados abaixo.

### Textos atuais não alterados

Campo `/texto`

```json
"In a final, catastrophic moment, volatile energies tear through the Sultan, reducing him to nothing but ash.\n\nFrom the remnants of the Sultan's demise, a faint light begins to emerge, growing brighter and more tangible. Out of the ashes floats an amulet, its gold shimmering with an ethereal light, untouched by the destruction that had just unfolded.\n\r\nThe moment your fingers touch the necklace, a rush of energy surges through you, and you are transported once more into a vivid memory that is not your own. \n\r<br/>\nYou find yourself witnessing a moment of profound intimacy and love – the Sultan, a man now unrecognizable from the tyrant you had just faced, in a tender embrace with a beautiful woman with raven-black hair. The Sultan's expression, devoid of the hardness and cruelty that had marked his face in battle, is filled with genuine affection and happiness. \n\nThe couple seem utterly at peace, lost in their love for each other.\n\r<br/>\nAs quickly as it had begun, the vision dissipates, leaving you standing in the blinding heat of Wyrmrest. With the amulet now in your possession, you turn your attention back to the path laid out in your father's journal. It beckons you onwards, towards the vast and treacherous expanse of the sea. \n\n\n\n"
```

Campo `/texto_resultados_possiveis` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/campos_originais/promptToSelectCharacter` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/campos_originais/characterSelectedText` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

### Anomalias, disponibilidade e referências

disabled=0; opções=0; ações=0; NULL auditados=0; refs nulas projetadas=0. Todos os caminhos e motivos destes NULL estão individualizados na parte05 e propostas-auditadas.json.

Condições/modos/prefab (literais, sem escolha de variante):

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
  "prefab": {
    "Guid": "5c32f1e7921398548b604c709d76d243",
    "Path": "Island Hex Pieces\\Events\\The Sultan - 1"
  }
}
```

Opções ocultas: []. hideOptionEffectText oculta texto de efeito, não necessariamente a opção. Exibição efetiva: NAO_EXERCITADO.

Referências entrantes explícitas recuperadas no canônico/catálogo (sem alegação de varredura de código/runtime):

```json
[
  {
    "origem": "resources.assets:2545636",
    "tipo": "PartyEvent",
    "campo": "/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "destino": "resources.assets:2545635"
  },
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/104",
    "destino": "resources.assets:2545635"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[]
```

NAO_EXERCITADO: runtime/UI, disponibilidade, RNG, aplicação final de status, ouro/XP/loot finais e combate, porque a tarefa proíbe execução do jogo. Referência nula com motivo m_PathID=0 permanece distinta de resultado não exercitado.

## 69. The Witch

Chave: `resources.assets:2545643`; GUID: `81632a77-5c59-495f-9d0d-32acca8b75cd`; nome_asset: 8 - The Witch End.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording: corrigir três erros lexicais sem mudar o epílogo, a memória ou a missão.

### Análise específica

- Zero opções. O teddy bear narrado não deve ser transformado em recompensa inventada.

- Preservar tags br/>, nomes da região e a narrativa da juventude da Witch.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/texto`

Texto atual (literal completo):

```json
"The Witch's form, once a vessel of corruption and malevolence, begins to dissolve. Her cruel visage, twisted by years of darkness, bubbles and melts into the swamp itself, as if the land is reclaiming a part of its lost self. The foul air and the murky waters around her seeth and churn, swallowing the remnants of her existence.\n\nFrom the dissipating form of the Witch, a light rises, pure and cleansing. It swirls amidst the foul miasma of the swamp, a beacon of hope in the heart of despair. Encased within this light is a simple object, starkly out of place in the grim surroundings – a child's teddy bear, worn by time but still holding the echoes of innocence and care.\n\nYou reach out and take the bear. As your fingers brush against its fabric, a vision envelopes you, transporting you to a time and place far removed from the decay of the swamp.\n<br/>\nYou find yourself in a forest at night, a world away from the corruption you have just witnessed. Above, the stars shine brightly, their light filtering through the canopy to dance upon the forest floor. The air is alive with the sound of crickets and the gentle movement of fireflies, a symphony of the night.\r\n\r\nThere, in a clearing, lays a young girl, the Witch in her innocent youth, curled up beside her pet wolf. Both sleep peacefully, nestled together for warmth under the starlit sky. The girl, a caretaker of the forest, is at home in this natural haven, her heart intertwined with the life around her. The vision is a glimpse into a past untainted by darkness, a time of innocence and harmony.\n<br/>\nAs the vision fades, you are brought back to the grim reality of the Sunken Swamp. The beautiful forest of the vision is now the stinking bog that surrounds you, a bleak reminder of the transformation wrought by the curse.\r\n\r\nWith the child's bear in hand, the final relic mentioned in your father's journal, you know that your quest is nearing its end. You have gathered the artifacts, each a key to understanding the depth of the curse that had befallen the realm.\r\n\r\nNow, all that remains is to retrace the last steps of your father, to follow the path that would lead him to the looming Castle Gloom.\n\n"
```

PROPOSTA EXATA (literal completo):

```json
"The Witch's form, once a vessel of corruption and malevolence, begins to dissolve. Her cruel visage, twisted by years of darkness, bubbles and melts into the swamp itself, as if the land is reclaiming a part of its lost self. The foul air and the murky waters around her seethe and churn, swallowing the remnants of her existence.\n\nFrom the dissipating form of the Witch, a light rises, pure and cleansing. It swirls amidst the foul miasma of the swamp, a beacon of hope in the heart of despair. Encased within this light is a simple object, starkly out of place in the grim surroundings – a child's teddy bear, worn by time but still holding the echoes of innocence and care.\n\nYou reach out and take the bear. As your fingers brush against its fabric, a vision envelops you, transporting you to a time and place far removed from the decay of the swamp.\n<br/>\nYou find yourself in a forest at night, a world away from the corruption you have just witnessed. Above, the stars shine brightly, their light filtering through the canopy to dance upon the forest floor. The air is alive with the sound of crickets and the gentle movement of fireflies, a symphony of the night.\r\n\r\nThere, in a clearing, lies a young girl, the Witch in her innocent youth, curled up beside her pet wolf. Both sleep peacefully, nestled together for warmth under the starlit sky. The girl, a caretaker of the forest, is at home in this natural haven, her heart intertwined with the life around her. The vision is a glimpse into a past untainted by darkness, a time of innocence and harmony.\n<br/>\nAs the vision fades, you are brought back to the grim reality of the Sunken Swamp. The beautiful forest of the vision is now the stinking bog that surrounds you, a bleak reminder of the transformation wrought by the curse.\r\n\r\nWith the child's bear in hand, the final relic mentioned in your father's journal, you know that your quest is nearing its end. You have gathered the artifacts, each a key to understanding the depth of the curse that had befallen the realm.\r\n\r\nNow, all that remains is to retrace the last steps of your father, to follow the path that would lead him to the looming Castle Gloom.\n\n"
```

Justificativa: Ortografia do verbo seethe.; envelops é o verbo envolver; envelopes não é a forma pretendida.; lie indica estar deitada; lay é transitivo.

### Textos atuais não alterados

Campo `/texto_resultados_possiveis` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/campos_originais/promptToSelectCharacter` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/campos_originais/characterSelectedText` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

### Anomalias, disponibilidade e referências

disabled=0; opções=0; ações=0; NULL auditados=0; refs nulas projetadas=0. Todos os caminhos e motivos destes NULL estão individualizados na parte05 e propostas-auditadas.json.

Condições/modos/prefab (literais, sem escolha de variante):

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
  "prefab": {
    "Guid": "9f6163ee8a0fb5e41b602721709e08c1",
    "Path": "Island Hex Pieces\\Events\\The Witch - 1"
  }
}
```

Opções ocultas: []. hideOptionEffectText oculta texto de efeito, não necessariamente a opção. Exibição efetiva: NAO_EXERCITADO.

Referências entrantes explícitas recuperadas no canônico/catálogo (sem alegação de varredura de código/runtime):

```json
[
  {
    "origem": "resources.assets:2545644",
    "tipo": "PartyEvent",
    "campo": "/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "destino": "resources.assets:2545643"
  },
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/112",
    "destino": "resources.assets:2545643"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[]
```

NAO_EXERCITADO: runtime/UI, disponibilidade, RNG, aplicação final de status, ouro/XP/loot finais e combate, porque a tarefa proíbe execução do jogo. Referência nula com motivo m_PathID=0 permanece distinta de resultado não exercitado.

## 70. Too Late

Chave: `resources.assets:2545647`; GUID: `555fe1d0-e62f-420b-9ce6-cb66f38a2ce1`; nome_asset: 9 - Too Late.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording: capitalização após travessão dentro da mesma frase, preservando a fala do pai.

### Análise específica

- Zero opções e nenhum bloco de recompensa por opção. Manter o desfecho de chegada tardia e as memórias como elemento narrativo, não como bônus calculado.

- NULL não aparece neste objeto canônico; isso não demonstra resultados finais calculados.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/texto`

Texto atual (literal completo):

```json
"As you recognize the ensnared spirit, a deep sorrow engulfs your heart. The realization dawns – You are too late. You failed to save your father.\r\n\r\nYour father’s ghost comforts you.\r\n\n“Hold no sorrow. You are blameless. It was the ailment's doing. I perished in pursuit of my passion, and now, with your arrival, you can finish what I started.”\r\n\nEven as your father harbors no resentment, a tide of guilt washes over you for leaving him behind. Lingering thoughts haunt you – would he yet draw breath had you never strayed from his side?\n\nYour father's voice cleaves through the fog of your sorrow, anchoring you back to the present.\n\n\"As you delve deeper into the castle's heart, the darkness will begin to cloud your mind, a fog that dulls the senses and fills your thoughts with whispers of doubt and despair.\"\n\n\"Grasp tightly the memories you've gathered. The Dead One wields no dominion over the echoes you hold.\"\n\n"
```

PROPOSTA EXATA (literal completo):

```json
"As you recognize the ensnared spirit, a deep sorrow engulfs your heart. The realization dawns – you are too late. You failed to save your father.\r\n\r\nYour father’s ghost comforts you.\r\n\n“Hold no sorrow. You are blameless. It was the ailment's doing. I perished in pursuit of my passion, and now, with your arrival, you can finish what I started.”\r\n\nEven as your father harbors no resentment, a tide of guilt washes over you for leaving him behind. Lingering thoughts haunt you – would he yet draw breath had you never strayed from his side?\n\nYour father's voice cleaves through the fog of your sorrow, anchoring you back to the present.\n\n\"As you delve deeper into the castle's heart, the darkness will begin to cloud your mind, a fog that dulls the senses and fills your thoughts with whispers of doubt and despair.\"\n\n\"Grasp tightly the memories you've gathered. The Dead One wields no dominion over the echoes you hold.\"\n\n"
```

Justificativa: Continuação da oração, não início de nova sentença.

### Textos atuais não alterados

Campo `/texto_resultados_possiveis` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/campos_originais/promptToSelectCharacter` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/campos_originais/characterSelectedText` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

### Anomalias, disponibilidade e referências

disabled=0; opções=0; ações=0; NULL auditados=0; refs nulas projetadas=0. Todos os caminhos e motivos destes NULL estão individualizados na parte05 e propostas-auditadas.json.

Condições/modos/prefab (literais, sem escolha de variante):

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
  "prefab": {
    "Guid": "308fb17c0e9e6df46bd6763372acc808",
    "Path": "Island Hex Pieces\\Events\\The Dead One - 1"
  }
}
```

Opções ocultas: []. hideOptionEffectText oculta texto de efeito, não necessariamente a opção. Exibição efetiva: NAO_EXERCITADO.

Referências entrantes explícitas recuperadas no canônico/catálogo (sem alegação de varredura de código/runtime):

```json
[
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/116",
    "destino": "resources.assets:2545647"
  },
  {
    "origem": "resources.assets:2547315",
    "tipo": "QuestInfo",
    "campo": "/serializationData/ReferencedUnityObjects/0",
    "destino": "resources.assets:2545647"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[]
```

NAO_EXERCITADO: runtime/UI, disponibilidade, RNG, aplicação final de status, ouro/XP/loot finais e combate, porque a tarefa proíbe execução do jogo. Referência nula com motivo m_PathID=0 permanece distinta de resultado não exercitado.
