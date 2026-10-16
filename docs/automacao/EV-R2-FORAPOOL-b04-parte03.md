# EV-R2-FORAPOOL-b04 — parte 03: eventos 71–77

Fonte: C:\dev\stolen-realm\docs\cobertura\EV-R1/eventos.json; ordem: C:\dev\stolen-realm\docs\cobertura\EV-R1/lote-NotInEventPool-v2.md. Contagem desta parte: 7/7 eventos. Todos os vereditos são PROPOSTOS, aprovação do dono PENDENTE.

Coordenadas JSON Pointer com índices base 0; índices de leitura de opções/ações continuam base 1. Strings exibidas como literais JSON preservam CR/LF, espaços e tags. Catálogo: git 097f950:docs/cobertura/EV-R1/catalogo-referencias.json; provenance completa na parte05 e fontes-hashes.json.

## 71. Treasure of Moltendunn

Chave: `resources.assets:2545760`; GUID: `2f8ff63f-f021-4dc6-b13c-b928121964c1`; nome_asset: Treasure of Moltendunn 1.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording: remover prompt de súplica deslocado; o restante da descoberta do baú pode permanecer.

### Análise específica

- Dig possui ação de texto vazio e encadeia 2545761. Leave não tem ações; não acrescentar efeito de saída nem resposta fictícia.

- O tesouro é apenas promessa nesta etapa; nenhum ouro/item final é informado.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/campos_originais/promptToSelectCharacter`

Texto atual (literal completo):

```json
"Who will listen to his pleas?"
```

PROPOSTA EXATA (literal completo):

```json
"Who will uncover the treasure?"
```

Justificativa: Alinha a seleção de personagem à escavação.

### Textos atuais não alterados

Campo `/texto`

```json
"Spurred on by the promise of the legendary Treasure of Moltendunn, you make your way through the terrain outlined on the map. After many trials and tests of wit and skill, you find yourself standing before a sight that makes your heart pound - a chest, half buried in the sand, its glinting lock winking at you in the light."
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
"Dig"
```

Campo `/opcoes/0/texto`

```json
"Uncover the treasure."
```

Campo `/opcoes/0/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/efeitos/0/texto` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/1/titulo`

```json
"Leave"
```

Campo `/opcoes/1/texto`

```json
"You have second thoughts about the hunt."
```

Campo `/opcoes/1/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

### Anomalias, disponibilidade e referências

disabled=0; opções=2; ações=1; NULL auditados=11; refs nulas projetadas=1. Todos os caminhos e motivos destes NULL estão individualizados na parte05 e propostas-auditadas.json.

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
    "requiredStatusesToSpawn": [
      {
        "m_FileID": 0,
        "m_PathID": 2545521
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
  "prefab": {
    "Guid": "3873b75868fc58042bc7e4c2f5a1e922",
    "Path": "Island Hex Pieces\\Events\\Sinking Chest"
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
    "origem": "resources.assets:2545521",
    "tipo": "EventStatus",
    "campo": "/ForcedNextEvent",
    "destino": "resources.assets:2545760"
  },
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/229",
    "destino": "resources.assets:2545760"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[
  {
    "opcao": 1,
    "titulo": "Dig",
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
          "chave": "resources.assets:2545761",
          "nome": "Treasure of Moltendunn 2",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545761
          },
          "tipo": "PartyEvent"
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
    "acoes": []
  }
]
```

NAO_EXERCITADO: runtime/UI, disponibilidade, RNG, aplicação final de status, ouro/XP/loot finais e combate, porque a tarefa proíbe execução do jogo. Referência nula com motivo m_PathID=0 permanece distinta de resultado não exercitado.

## 72. Treasure of Moltendunn

Chave: `resources.assets:2545761`; GUID: `96252be8-6f1a-4c87-ab16-258d31eaa501`; nome_asset: Treasure of Moltendunn 2.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording: pontuar a descrição de Dig e contextualizar o prompt; condições/recompensas ficam MANTER.

### Análise específica

- Success com RollLimit=8 encadeia 2545763; Failure com RollLimit=0 encadeia 2545762, configura percentMaxHealth=-10.0 e Fatigued. Não derivar probabilidade nem dano final.

- Give Up tem descrição vazia e nenhuma ação. Preservar a ausência, sem preencher por narrativa inventada.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/opcoes/0/texto`

Texto atual (literal completo):

```json
"You dig even faster unwilling to let the treasure go."
```

PROPOSTA EXATA (literal completo):

```json
"You dig even faster, unwilling to let the treasure go."
```

Justificativa: Separar oração participial.

Campo `/campos_originais/promptToSelectCharacter`

Texto atual (literal completo):

```json
"Who will listen to his pleas?"
```

PROPOSTA EXATA (literal completo):

```json
"Who will keep digging?"
```

Justificativa: Remove a súplica de personagem inexistente.

### Textos atuais não alterados

Campo `/texto`

```json
"Without hesitation, you set to work, your fingers scrabbling through the sand to uncover the rest of the chest. Yet, the more you dig, the deeper the chest sinks, like it is being swallowed by the earth itself. Rocks and dirt fall from the sides of the hole, the ground shifting and groaning beneath your weight."
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
"Dig"
```

Campo `/opcoes/0/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/efeitos/0/texto`

```json
"As you dig faster, you notice the ground isn't merely sinking - it is churning, as if caught in the gears of some vast machinery. Fear ripples through you, a sense of dread settling like a stone in your stomach. This isn't a mere chest buried in the sand. It is a trap."
```

Campo `/opcoes/0/efeitos/1/texto`

```json
"The more you dig, the faster the chest sinks. Rocks and debris batter you, adding to your growing exhaustion. Your strength wanes, your endurance tested to its limits. Your heart pounds in your chest, and sweat streams down your face, mixing with the sand and dust."
```

Campo `/opcoes/1/titulo`

```json
"Give Up"
```

Campo `/opcoes/1/texto` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/1/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

### Anomalias, disponibilidade e referências

disabled=0; opções=2; ações=2; NULL auditados=22; refs nulas projetadas=2. Todos os caminhos e motivos destes NULL estão individualizados na parte05 e propostas-auditadas.json.

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
    "Guid": "3873b75868fc58042bc7e4c2f5a1e922",
    "Path": "Island Hex Pieces\\Events\\Sinking Chest"
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
    "origem": "resources.assets:2545760",
    "tipo": "PartyEvent",
    "campo": "/eventOptions/0/eventActions/0/chainedEvent",
    "destino": "resources.assets:2545761"
  },
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/230",
    "destino": "resources.assets:2545761"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[
  {
    "opcao": 1,
    "titulo": "Dig",
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
        "limite_rolagem": 8,
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
          "chave": "resources.assets:2545763",
          "nome": "Treasure of Moltendunn 4",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545763
          },
          "tipo": "PartyEvent"
        }
      },
      {
        "indice": 2,
        "resultado": {
          "valor": 1,
          "nome": "Failure"
        },
        "limite_rolagem": 0,
        "efeitos": [
          {
            "vida_mana": {
              "percentMaxHealth": -10.0,
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
                    "chave": "resources.assets:2545495",
                    "nome": "Fatigued",
                    "pptr": {
                      "m_FileID": 0,
                      "m_PathID": 2545495
                    },
                    "tipo": "EventStatus",
                    "descricao": "Reduces Dexterity by @20%@ per stack.",
                    "duracao": {
                      "valor": 1,
                      "nome": "Quest"
                    },
                    "status_tipo": {
                      "valor": 0,
                      "nome": "Normal"
                    },
                    "modificadores": [
                      {
                        "atributo": {
                          "chave": "resources.assets:2544448",
                          "nome": "DexterityBase",
                          "pptr": {
                            "m_FileID": 0,
                            "m_PathID": 2544448
                          },
                          "tipo": "CharacterAttribute"
                        },
                        "metodo": {
                          "valor": 1,
                          "nome": "Percentage"
                        },
                        "expressao": "-20",
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
          "chave": "resources.assets:2545762",
          "nome": "Treasure of Moltendunn 3",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545762
          },
          "tipo": "PartyEvent"
        }
      }
    ]
  },
  {
    "opcao": 2,
    "titulo": "Give Up",
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
    "acoes": []
  }
]
```

NAO_EXERCITADO: runtime/UI, disponibilidade, RNG, aplicação final de status, ouro/XP/loot finais e combate, porque a tarefa proíbe execução do jogo. Referência nula com motivo m_PathID=0 permanece distinta de resultado não exercitado.

## 73. Treasure of Moltendunn

Chave: `resources.assets:2545762`; GUID: `11d0a54b-fb4e-4e63-b6ac-1fb07d03f3c2`; nome_asset: Treasure of Moltendunn 3.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording: concordância e pontuação; não remover a repetição configurada da tentativa.

### Análise específica

- Failure volta à própria chave 2545762 e configura perda percentMaxHealth=-10.0 e Fatigued. Isso é um laço serializado, não prova de travamento em jogo.

- Success leva a 2545763. O comportamento acumulado, RNG e duração efetiva da fadiga são NAO_EXERCITADO.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/texto`

Texto atual (literal completo):

```json
"It is a cruel trap, a relentless mechanical nightmare designed to thwart any who seeks the Treasure of Moltendunn. Frustration and determination battle within you, each demanding control. Will you succumb to the ceaseless pull of the earth, or can you outwit the ancient machinery and seize the treasure you have sought? "
```

PROPOSTA EXATA (literal completo):

```json
"It is a cruel trap, a relentless mechanical nightmare designed to thwart any who seek the Treasure of Moltendunn. Frustration and determination battle within you, each demanding control. Will you succumb to the ceaseless pull of the earth, or can you outwit the ancient machinery and seize the treasure you have sought? "
```

Justificativa: Concordância de who com any no sentido plural de todos os buscadores.

Campo `/opcoes/0/texto`

Texto atual (literal completo):

```json
"You dig even faster unwilling to let the treasure go."
```

PROPOSTA EXATA (literal completo):

```json
"You dig even faster, unwilling to let the treasure go."
```

Justificativa: Separar oração participial.

Campo `/opcoes/1/texto`

Texto atual (literal completo):

```json
"Despite your new find you won't risk being buried alive."
```

PROPOSTA EXATA (literal completo):

```json
"Despite your new find, you won't risk being buried alive."
```

Justificativa: Pontuar adjunto introdutório.

Campo `/campos_originais/promptToSelectCharacter`

Texto atual (literal completo):

```json
"Who will listen to his pleas?"
```

PROPOSTA EXATA (literal completo):

```json
"Who will keep digging?"
```

Justificativa: Alinhar ao desafio de escavação.

### Textos atuais não alterados

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
"Dig"
```

Campo `/opcoes/0/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/efeitos/0/texto`

```json
"You notice the glint of metal beneath the dirt. You brush the soil away, revealing a network of gears and cogs, spinning and whirling, pulling the chest further into the ground. The trap is intricate, designed to ensnare greedy treasure hunters who acted without thinking."
```

Campo `/opcoes/0/efeitos/1/texto`

```json
"Rocks and debris batter you, adding to your growing exhaustion. Your strength wanes, your endurance tested to its limits. Your heart pounds in your chest, and sweat streams down your face, mixing with the sand and dust."
```

Campo `/opcoes/1/titulo`

```json
"Give Up"
```

Campo `/opcoes/1/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

### Anomalias, disponibilidade e referências

disabled=0; opções=2; ações=2; NULL auditados=22; refs nulas projetadas=2. Todos os caminhos e motivos destes NULL estão individualizados na parte05 e propostas-auditadas.json.

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
    "Guid": "3873b75868fc58042bc7e4c2f5a1e922",
    "Path": "Island Hex Pieces\\Events\\Sinking Chest"
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
    "origem": "resources.assets:2545761",
    "tipo": "PartyEvent",
    "campo": "/eventOptions/0/eventActions/1/chainedEvent",
    "destino": "resources.assets:2545762"
  },
  {
    "origem": "resources.assets:2545762",
    "tipo": "PartyEvent",
    "campo": "/eventOptions/0/eventActions/1/chainedEvent",
    "destino": "resources.assets:2545762"
  },
  {
    "origem": "resources.assets:2545763",
    "tipo": "PartyEvent",
    "campo": "/eventOptions/0/eventActions/1/chainedEvent",
    "destino": "resources.assets:2545762"
  },
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/231",
    "destino": "resources.assets:2545762"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[
  {
    "opcao": 1,
    "titulo": "Dig",
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
        "limite_rolagem": 8,
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
          "chave": "resources.assets:2545763",
          "nome": "Treasure of Moltendunn 4",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545763
          },
          "tipo": "PartyEvent"
        }
      },
      {
        "indice": 2,
        "resultado": {
          "valor": 1,
          "nome": "Failure"
        },
        "limite_rolagem": 0,
        "efeitos": [
          {
            "vida_mana": {
              "percentMaxHealth": -10.0,
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
                    "chave": "resources.assets:2545495",
                    "nome": "Fatigued",
                    "pptr": {
                      "m_FileID": 0,
                      "m_PathID": 2545495
                    },
                    "tipo": "EventStatus",
                    "descricao": "Reduces Dexterity by @20%@ per stack.",
                    "duracao": {
                      "valor": 1,
                      "nome": "Quest"
                    },
                    "status_tipo": {
                      "valor": 0,
                      "nome": "Normal"
                    },
                    "modificadores": [
                      {
                        "atributo": {
                          "chave": "resources.assets:2544448",
                          "nome": "DexterityBase",
                          "pptr": {
                            "m_FileID": 0,
                            "m_PathID": 2544448
                          },
                          "tipo": "CharacterAttribute"
                        },
                        "metodo": {
                          "valor": 1,
                          "nome": "Percentage"
                        },
                        "expressao": "-20",
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
          "chave": "resources.assets:2545762",
          "nome": "Treasure of Moltendunn 3",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545762
          },
          "tipo": "PartyEvent"
        }
      }
    ]
  },
  {
    "opcao": 2,
    "titulo": "Give Up",
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
    "acoes": []
  }
]
```

NAO_EXERCITADO: runtime/UI, disponibilidade, RNG, aplicação final de status, ouro/XP/loot finais e combate, porque a tarefa proíbe execução do jogo. Referência nula com motivo m_PathID=0 permanece distinta de resultado não exercitado.

## 74. Treasure of Moltendunn

Chave: `resources.assets:2545763`; GUID: `085d4df2-878c-4979-a83f-7aeea9d034ec`; nome_asset: Treasure of Moltendunn 4.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording: simplificar a frase introdutória e pontuar a opção; preservar os ramos de sucesso/falha.

### Análise específica

- Success leva a 2545764; Failure leva a 2545762. A ação Failure tem efeitos=[] apesar do texto de exaustão. Não copiar automaticamente o dano/Fatigued das etapas anteriores.

- Give Up tem descrição vazia e nenhuma ação. Sinalizar, não inventar novos efeitos.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/texto`

Texto atual (literal completo):

```json
"You'll need to disarm the trap, to stop the machinery that is swallowing the chest. You scan the arrangement of gears, your mind racing to decipher their purpose and function."
```

PROPOSTA EXATA (literal completo):

```json
"You'll need to disarm the trap to stop the machinery that is swallowing the chest. You scan the arrangement of gears, your mind racing to decipher their purpose and function."
```

Justificativa: Remover vírgula que separa verbo e oração de finalidade.

Campo `/opcoes/0/texto`

Texto atual (literal completo):

```json
"Your mind races thinking of ways to stop the trap."
```

PROPOSTA EXATA (literal completo):

```json
"Your mind races, thinking of ways to stop the trap."
```

Justificativa: Pontuar oração participial.

Campo `/campos_originais/promptToSelectCharacter`

Texto atual (literal completo):

```json
"Who will listen to his pleas?"
```

PROPOSTA EXATA (literal completo):

```json
"Who will disarm the trap?"
```

Justificativa: Adequar o prompt ao mecanismo.

### Textos atuais não alterados

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
"Disarm"
```

Campo `/opcoes/0/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/efeitos/0/texto`

```json
"Noticing a main cog that seems to be driving the rest, you draw your weapon, wedging it into the intricate web of spinning gears. With a final, heaving push, you jam the cog, grinding the machinery to a halt. The sinking ceases, the chest frozen in its descent."
```

Campo `/opcoes/0/efeitos/1/texto`

```json
"Rocks and debris batter you, adding to your growing exhaustion. Your strength wanes, your endurance tested to its limits. Your heart pounds in your chest, and sweat streams down your face, mixing with the sand and dust."
```

Campo `/opcoes/1/titulo`

```json
"Give Up"
```

Campo `/opcoes/1/texto` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/1/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

### Anomalias, disponibilidade e referências

disabled=0; opções=2; ações=2; NULL auditados=14; refs nulas projetadas=2. Todos os caminhos e motivos destes NULL estão individualizados na parte05 e propostas-auditadas.json.

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
    "Guid": "3873b75868fc58042bc7e4c2f5a1e922",
    "Path": "Island Hex Pieces\\Events\\Sinking Chest"
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
    "origem": "resources.assets:2545761",
    "tipo": "PartyEvent",
    "campo": "/eventOptions/0/eventActions/0/chainedEvent",
    "destino": "resources.assets:2545763"
  },
  {
    "origem": "resources.assets:2545762",
    "tipo": "PartyEvent",
    "campo": "/eventOptions/0/eventActions/0/chainedEvent",
    "destino": "resources.assets:2545763"
  },
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/232",
    "destino": "resources.assets:2545763"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[
  {
    "opcao": 1,
    "titulo": "Disarm",
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
        "limite_rolagem": 8,
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
          "chave": "resources.assets:2545764",
          "nome": "Treasure of Moltendunn 5",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545764
          },
          "tipo": "PartyEvent"
        }
      },
      {
        "indice": 2,
        "resultado": {
          "valor": 1,
          "nome": "Failure"
        },
        "limite_rolagem": 0,
        "efeitos": [],
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
          "chave": "resources.assets:2545762",
          "nome": "Treasure of Moltendunn 3",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545762
          },
          "tipo": "PartyEvent"
        }
      }
    ]
  },
  {
    "opcao": 2,
    "titulo": "Give Up",
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
    "acoes": []
  }
]
```

NAO_EXERCITADO: runtime/UI, disponibilidade, RNG, aplicação final de status, ouro/XP/loot finais e combate, porque a tarefa proíbe execução do jogo. Referência nula com motivo m_PathID=0 permanece distinta de resultado não exercitado.

## 75. Treasure of Moltendunn

Chave: `resources.assets:2545764`; GUID: `38383f9f-e2b6-4b4c-abb3-5fb1a688e046`; nome_asset: Treasure of Moltendunn 5.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording: fechar a frase e corrigir comma splice do Oculus; contextualizar o prompt, mantendo as três escolhas.

### Análise específica

- As opções configuram separadamente Dragon Claw Talisman, Phoenix Feather e Oculus Gem como EventStatus/Fortune. Não tratá-los como três itens cumulativos ou inventar valores.

- Nenhuma variante de modo é escolhida pelo parecer. A aplicação final das fortunas é NAO_EXERCITADO.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/texto`

Texto atual (literal completo):

```json
"Breathing hard, you turn your attention back to the chest. You've won this round, but the Treasure of Moltendunn has already proved itself to be as treacherous as it is tempting. With newfound caution, you reach out to open the chest"
```

PROPOSTA EXATA (literal completo):

```json
"Breathing hard, you turn your attention back to the chest. You've won this round, but the Treasure of Moltendunn has already proved itself to be as treacherous as it is tempting. With newfound caution, you reach out to open the chest."
```

Justificativa: Ponto final ausente.

Campo `/opcoes/2/efeitos/0/texto`

Texto atual (literal completo):

```json
"As your fingers come into contact with it, the gem vanishes. Startled, you feel a weight in your pocket. Reaching in, you find the gem, it had teleported away from your hand and into your pocket, as if it has a mind of its own."
```

PROPOSTA EXATA (literal completo):

```json
"As your fingers come into contact with it, the gem vanishes. Startled, you feel a weight in your pocket. Reaching in, you find the gem. It has teleported away from your hand and into your pocket, as if it has a mind of its own."
```

Justificativa: Separar orações independentes e alinhar o tempo ao presente narrativo.

Campo `/campos_originais/promptToSelectCharacter`

Texto atual (literal completo):

```json
"Who will listen to his pleas?"
```

PROPOSTA EXATA (literal completo):

```json
"Who will claim a treasure?"
```

Justificativa: Não afirmar concessão de todas as escolhas.

### Textos atuais não alterados

Campo `/texto_resultados_possiveis`

```json
"What treasure will you take?"
```

Campo `/campos_originais/characterSelectedText` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/titulo`

```json
"Dragon Claw Talisman"
```

Campo `/opcoes/0/texto`

```json
"The strange item sparkles with embers."
```

Campo `/opcoes/0/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/efeitos/0/texto`

```json
"A petrified claw of a red dragon whelp, ancient yet perfectly preserved. Its fiery hue is frozen in time, the rough texture a stark contrast against the smooth, cold interior of the chest."
```

Campo `/opcoes/1/titulo`

```json
"Phoenix Feather"
```

Campo `/opcoes/1/texto`

```json
"The dull gray feather looks withered and lifeless."
```

Campo `/opcoes/1/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/1/efeitos/0/texto`

```json
"As your fingers brush against the feather, it disintegrates into ashes, leaving nothing but soot on your fingers. Yet, in the blink of an eye, the ashes coalesce into a brilliant fiery orange in a flash of flame. The feather, reborn from its own ashes, pulses with energy, a testament to the power of rebirth and resilience."
```

Campo `/opcoes/2/titulo`

```json
"Oculus Gem"
```

Campo `/opcoes/2/texto`

```json
"The gem swirls with magical energy."
```

Campo `/opcoes/2/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

### Anomalias, disponibilidade e referências

disabled=0; opções=3; ações=3; NULL auditados=39; refs nulas projetadas=6. Todos os caminhos e motivos destes NULL estão individualizados na parte05 e propostas-auditadas.json.

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
    "Guid": "3873b75868fc58042bc7e4c2f5a1e922",
    "Path": "Island Hex Pieces\\Events\\Sinking Chest"
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
  },
  {
    "opcao": 3,
    "ocultar_sem_requisitos": false,
    "ocultar_se_status": [],
    "hideOptionEffectText": 0
  }
]. hideOptionEffectText oculta texto de efeito, não necessariamente a opção. Exibição efetiva: NAO_EXERCITADO.

Referências entrantes explícitas recuperadas no canônico/catálogo (sem alegação de varredura de código/runtime):

```json
[
  {
    "origem": "resources.assets:2545763",
    "tipo": "PartyEvent",
    "campo": "/eventOptions/0/eventActions/0/chainedEvent",
    "destino": "resources.assets:2545764"
  },
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/233",
    "destino": "resources.assets:2545764"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[
  {
    "opcao": 1,
    "titulo": "Dragon Claw Talisman",
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
                    "chave": "resources.assets:2545424",
                    "nome": "Dragon Claw Talisman",
                    "pptr": {
                      "m_FileID": 0,
                      "m_PathID": 2545424
                    },
                    "tipo": "EventStatus",
                    "descricao": "Summons a @level@ {1,30} Red Dragon Whelp to fight for you.\n\n<i><color=#808080>\"The magically preserved claw of a Dragonling.\"</i></color>",
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
    "opcao": 2,
    "titulo": "Phoenix Feather",
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
                    "chave": "resources.assets:2545461",
                    "nome": "Phoenix Feather",
                    "pptr": {
                      "m_FileID": 0,
                      "m_PathID": 2545461
                    },
                    "tipo": "EventStatus",
                    "descricao": "Brings you back with 20% Health. 1 charge per Quest.\n\n<i><color=#808080>\"The glowing feather of a Phoenix.\"</color></i>\n",
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
    "opcao": 3,
    "titulo": "Oculus Gem",
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
                  "valor": 1,
                  "nome": "Global"
                },
                "quantidade_configurada": 2,
                "tabelas": [],
                "restricoes": {
                  "limitItemTypes": 0,
                  "possibleItemTypes": [],
                  "limitItemRarities": 1,
                  "possibleRarities": [
                    2,
                    3
                  ]
                },
                "sorteio_final": null,
                "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
              },
              "status": {
                "candidatos": [
                  {
                    "chave": "resources.assets:2545458",
                    "nome": "Oculus Gem",
                    "pptr": {
                      "m_FileID": 0,
                      "m_PathID": 2545458
                    },
                    "tipo": "EventStatus",
                    "descricao": "Teleports you randomly when struck. 4 turn cooldown.\n\n<i><color=#808080>Where you'll go, nobody knows!</i></color> ",
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

## 76. Trial of the Ymir

Chave: `resources.assets:2545765`; GUID: `3847efc5-47dd-4913-b33c-16eedc922228`; nome_asset: Trial of the Ymir - Victory.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording: resolver contradição entre defeat e yield sem afirmar morte; contextualizar seleção.

### Análise específica

- Há três candidatos de status no mesmo efeito: Strength of the Ymir, Courage of the Ymir e Honor of the Ymir; sortear=false, quantidade_sorteada_configurada=1. Não substituir configuração por resultado efetivo.

- Descrições de status possuem incongruências próprias, por exemplo Honor cita Speed no flavor. São apenas sinalizadas, sem proposta fora dos campos deste evento nem alteração de fórmulas.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/texto`

Texto atual (literal completo):

```json
"The frost giant roars in defeat, his gaze locked onto you. He had not been defeated - rather, he has chosen to yield.\n\n\n\"You have proven your worth, Rune Conqueror,\" the frost giant admits, a note of admiration in his booming voice. \"You have shown strength, upheld your honor, and faced this trial with unyielding courage.\""
```

PROPOSTA EXATA (literal completo):

```json
"The frost giant roars, his gaze locked onto you. He has not fallen—he has chosen to yield.\n\n\n\"You have proven your worth, Rune Conqueror,\" the frost giant admits, a note of admiration in his booming voice. \"You have shown strength, upheld your honor, and faced this trial with unyielding courage.\""
```

Justificativa: Evita afirmar e negar derrota na mesma abertura; preserva rendição e sobrevivência.

Campo `/campos_originais/promptToSelectCharacter`

Texto atual (literal completo):

```json
"Who will listen to his pleas?"
```

PROPOSTA EXATA (literal completo):

```json
"Who will receive the blessings of the Ymir?"
```

Justificativa: Alinha o prompt ao epílogo da prova.

### Textos atuais não alterados

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
"Accept"
```

Campo `/opcoes/0/texto`

```json
"Receive the Might of Ymir."
```

Campo `/opcoes/0/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/efeitos/0/texto`

```json
"A surge of strength unlike anything you've ever felt before floods your frame, infusing your body with a power that is ancient and mighty.\n\n\n\"You are now blessed with the Might of the Ymir, a testament to your victory here today. Carry it with you, Rune Conqueror, and let it guide your path.\""
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
  "prefab": {
    "Guid": "dceeb6fc966a15c43a4b0072fad449f0",
    "Path": "Island Hex Pieces\\Events\\Test of the Ymir"
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
    "origem": "resources.assets:2545766",
    "tipo": "PartyEvent",
    "campo": "/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "destino": "resources.assets:2545765"
  },
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/235",
    "destino": "resources.assets:2545765"
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
                    "chave": "resources.assets:2545473",
                    "nome": "Strength of the Ymir",
                    "pptr": {
                      "m_FileID": 0,
                      "m_PathID": 2545473
                    },
                    "tipo": "EventStatus",
                    "descricao": "Allows you to wield Two-handed Axes, Swords, and Hammers in one hand. Weapon Damage is lowered by {50,35}% if you choose to do so.\n\n<i><color=#808080>You carry the Might of the Ymir!</color></i>",
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
                          "chave": "resources.assets:2544583",
                          "nome": "CanDualWieldTwoHanded",
                          "pptr": {
                            "m_FileID": 0,
                            "m_PathID": 2544583
                          },
                          "tipo": "CharacterAttribute"
                        },
                        "metodo": {
                          "valor": 4,
                          "nome": "Set"
                        },
                        "expressao": "1",
                        "segunda_passagem": false
                      },
                      {
                        "atributo": {
                          "chave": "resources.assets:2544626",
                          "nome": "StrengthOfYmirDamageReduction",
                          "pptr": {
                            "m_FileID": 0,
                            "m_PathID": 2544626
                          },
                          "tipo": "CharacterAttribute"
                        },
                        "metodo": {
                          "valor": 0,
                          "nome": "Base"
                        },
                        "expressao": "Target.IsDualWielding2H ? {50,35} : 0",
                        "segunda_passagem": false
                      }
                    ]
                  },
                  {
                    "chave": "resources.assets:2545420",
                    "nome": "Courage of the Ymir",
                    "pptr": {
                      "m_FileID": 0,
                      "m_PathID": 2545420
                    },
                    "tipo": "EventStatus",
                    "descricao": "Increases your @Action Points@ by @1@. If you are using a One-Handed Sword, Axe, Hammer, Gun, or Wand.\n\n<i><color=#808080>You carry the Speed of the Ymir!</color></i>",
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
                          "chave": "resources.assets:2544324",
                          "nome": "ExtraTurnActionPoints",
                          "pptr": {
                            "m_FileID": 0,
                            "m_PathID": 2544324
                          },
                          "tipo": "CharacterAttribute"
                        },
                        "metodo": {
                          "valor": 0,
                          "nome": "Base"
                        },
                        "expressao": "(Source.HasWeaponType(\"Sword_1H\") || Source.HasWeaponType(\"Axe_1H\") || Source.HasWeaponType(\"Mace_1H\") || Source.HasWeaponType(\"FistWeapon\") || Source.HasWeaponType(\"Gun_1H\") || Source.HasWeaponType(\"Wand\")) && !Source.WieldingTwoHanded ? 1 : 0",
                        "segunda_passagem": false
                      }
                    ]
                  },
                  {
                    "chave": "resources.assets:2545447",
                    "nome": "Honor of the Ymir",
                    "pptr": {
                      "m_FileID": 0,
                      "m_PathID": 2545447
                    },
                    "tipo": "EventStatus",
                    "descricao": "Every hex between you and your target increases damage dealt by an additional @12%@ when wielding a Staff, Bow, or Two Handed Gun.\n\n<i><color=#808080>You carry the Speed of the Ymir!</color></i>",
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
                        "expressao": "Source.HasWeaponType(\"Staff\") || Source.HasWeaponType(\"Bow\") || Source.HasWeaponType(\"Gun_2H\") ? 12 : 0 ",
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
                  "m_PathID": 2545232
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
```

NAO_EXERCITADO: runtime/UI, disponibilidade, RNG, aplicação final de status, ouro/XP/loot finais e combate, porque a tarefa proíbe execução do jogo. Referência nula com motivo m_PathID=0 permanece distinta de resultado não exercitado.

## 77. Trial of the Ymir

Chave: `resources.assets:2545766`; GUID: `a2a6b0b1-aaa0-41e4-8d9d-0caa21fb8380`; nome_asset: Trial of the Ymir.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording: corrigir concordância de eyes e contextualizar a prova.

### Análise específica

- Accept inicia combate e tem VictoryEvent=2545765. Decline possui ação de texto, sem combate. Não modificar a opção de recusa.

- Tags do Frost Giant e das falas permanecem idênticas. Renderização/UI não exercitadas.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/texto`

Texto atual (literal completo):

```json
"As you approach the giant, your gaze wanders over the towering figure. The <b><blue><incr>Frost Giant</incr></blue></b> is a creature of majesty and power, a child of the Ymir as ancient as the icy landscapes he traverses. His skin shimmers like fresh ice under the glow of the northern lights, radiating a cold, ethereal beauty that leaves you in awe.\n\n\n\"<blue>Well met, Rune Conqueror,</blue>\" the giant's voice echoes around you, a glacial rumble that sends vibrations coursing through the snow underfoot. His icy-blue eyes bores into you, a glimmer of respect evident in their frost-rimed depths.\n\n\n\"<blue>You carry the mark of our kin. The runes you carry are not simple magic but the embodiment of Ymir's principles: strength, honor, and courage. You have come far, and have been tested, but the greatest trial lies ahead,</blue>\" the giant proclaims, his voice echoing amidst the cold mountains."
```

PROPOSTA EXATA (literal completo):

```json
"As you approach the giant, your gaze wanders over the towering figure. The <b><blue><incr>Frost Giant</incr></blue></b> is a creature of majesty and power, a child of the Ymir as ancient as the icy landscapes he traverses. His skin shimmers like fresh ice under the glow of the northern lights, radiating a cold, ethereal beauty that leaves you in awe.\n\n\n\"<blue>Well met, Rune Conqueror,</blue>\" the giant's voice echoes around you, a glacial rumble that sends vibrations coursing through the snow underfoot. His icy-blue eyes bore into you, a glimmer of respect evident in their frost-rimed depths.\n\n\n\"<blue>You carry the mark of our kin. The runes you carry are not simple magic but the embodiment of Ymir's principles: strength, honor, and courage. You have come far, and have been tested, but the greatest trial lies ahead,</blue>\" the giant proclaims, his voice echoing amidst the cold mountains."
```

Justificativa: Concordância plural.

Campo `/campos_originais/promptToSelectCharacter`

Texto atual (literal completo):

```json
"Who will listen to his pleas?"
```

PROPOSTA EXATA (literal completo):

```json
"Who will face the trial?"
```

Justificativa: Remover súplica sem contexto.

### Textos atuais não alterados

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
"Accept"
```

Campo `/opcoes/0/texto`

```json
"You are ready."
```

Campo `/opcoes/0/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/efeitos/0/texto`

```json
"\"<blue>Very well, Rune Conqueror. Show us your strength, uphold your honor, and let your courage guide you. For you face now not just a trial, but a rite of passage. Triumph, and earn the blessings of the Ymir.</blue>\""
```

Campo `/opcoes/1/titulo`

```json
"Decline"
```

Campo `/opcoes/1/texto`

```json
"This trial proves too much for you."
```

Campo `/opcoes/1/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/1/efeitos/0/texto`

```json
"The sight of the towering giant gives you pause."
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
    "Guid": "dceeb6fc966a15c43a4b0072fad449f0",
    "Path": "Island Hex Pieces\\Events\\Test of the Ymir"
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
    "origem": "resources.assets:2545522",
    "tipo": "EventStatus",
    "campo": "/ForcedEventBeforeBoss",
    "destino": "resources.assets:2545766"
  },
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/234",
    "destino": "resources.assets:2545766"
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
                  "m_PathID": 2545232
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
              "m_PathID": 2545765
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
    "titulo": "Decline",
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
