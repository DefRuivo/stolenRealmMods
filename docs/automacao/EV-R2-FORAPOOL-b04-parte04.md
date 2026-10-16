# EV-R2-FORAPOOL-b04 — parte 04: eventos 78–84

Fonte: C:\dev\stolen-realm\docs\cobertura\EV-R1/eventos.json; ordem: C:\dev\stolen-realm\docs\cobertura\EV-R1/lote-NotInEventPool-v2.md. Contagem desta parte: 7/7 eventos. Todos os vereditos são PROPOSTOS, aprovação do dono PENDENTE.

Coordenadas JSON Pointer com índices base 0; índices de leitura de opções/ações continuam base 1. Strings exibidas como literais JSON preservam CR/LF, espaços e tags. Catálogo: git 097f950:docs/cobertura/EV-R1/catalogo-referencias.json; provenance completa na parte05 e fontes-hashes.json.

## 78. Unholy Experiments

Chave: `resources.assets:2545570`; GUID: `603a0843-ebb3-426f-9500-86812ad6d1d7`; nome_asset: Dark Discoveries - Battle.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording: manter exude no presente e retirar prompt de súplica; não alterar o combate ou abandono.

### Análise específica

- Fight tem texto de ativação vazio e inicia batalha. Flee tem texto próprio; remoções de status serão preservadas e mostradas na auditoria.

- Não preencher texto de ativação vazio nem inventar recompensa pelo combate.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/texto`

Texto atual (literal completo):

```json
"These wretched <blue><b><incr>Abominations</incr></b></blue>, swollen with the tormented souls of the damned, exuded a putrid odor that assaults the senses, a nauseating blend of decay and malevolence.\n\nAs you draw near, the foul stench grows stronger, a physical manifestation of the abominations' unholy nature. It permeates the air, clinging to your clothes and filling your nostrils with a sickening mixture of rot and despair."
```

PROPOSTA EXATA (literal completo):

```json
"These wretched <blue><b><incr>Abominations</incr></b></blue>, swollen with the tormented souls of the damned, exude a putrid odor that assaults the senses, a nauseating blend of decay and malevolence.\n\nAs you draw near, the foul stench grows stronger, a physical manifestation of the abominations' unholy nature. It permeates the air, clinging to your clothes and filling your nostrils with a sickening mixture of rot and despair."
```

Justificativa: Coerência temporal no presente.

Campo `/campos_originais/promptToSelectCharacter`

Texto atual (literal completo):

```json
"Who will listen to his pleas?"
```

PROPOSTA EXATA (literal completo):

```json
"Who will confront the abominations?"
```

Justificativa: Prompt relacionado ao encontro, sem alterar escolha de combate/fuga.

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
"Fight"
```

Campo `/opcoes/0/texto`

```json
"Rid the realm of these terrible <blue><b>Abominations</b></blue>."
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
"Flee"
```

Campo `/opcoes/1/texto`

```json
"Abandon this quest and flee."
```

Campo `/opcoes/1/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/1/efeitos/0/texto`

```json
"The putrid smell unlocks a primal fear deep within you. You turn away, abandoning this ill-fated quest."
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
    "Guid": "2ffc5b718fd4f5b40a560c027f0f52e9",
    "Path": "Island Hex Pieces\\Events\\Bloated Abominations"
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
    "origem": "resources.assets:2545510",
    "tipo": "EventStatus",
    "campo": "/ForcedEventBeforeBoss",
    "destino": "resources.assets:2545570"
  },
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/40",
    "destino": "resources.assets:2545570"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[
  {
    "opcao": 1,
    "titulo": "Fight",
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
                  "m_PathID": 2545160
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 0
              },
              {
                "OverrideEnemyName": 0,
                "NameOverride": "",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545160
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 0
              },
              {
                "OverrideEnemyName": 0,
                "NameOverride": "",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545160
                },
                "ForcedEnemyMods": [],
                "IsSuperUnique": 0
              },
              {
                "OverrideEnemyName": 0,
                "NameOverride": "",
                "CharacterInfo": {
                  "m_FileID": 0,
                  "m_PathID": 2545160
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
              "m_PathID": 2545571
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
    "titulo": "Flee",
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

## 79. Unleashed

Chave: `resources.assets:2545768`; GUID: `af493a35-ca03-4351-933f-cc688f2cd56e`; nome_asset: Unleashed - Victory.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording: substituir apenas o prompt de dívida com Ogre, sem reescrever o epílogo do Mad Mage.

### Análise específica

- O livro é suporte narrativo da fortuna Elemental Equilibrium, não item de inventário garantido: giveItems=false. Razão ouro=15.0 com dar=false não significa pagamento de 15 moedas.

- Preservar o título humorístico completo do livro e Good luck [name]..., sem tocar no placeholder.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/campos_originais/promptToSelectCharacter`

Texto atual (literal completo):

```json
"Does anyone owe this Ogre money?"
```

PROPOSTA EXATA (literal completo):

```json
"Who will take the spellbook?"
```

Justificativa: Não há Ogre ou dívida na cena.

### Textos atuais não alterados

Campo `/texto`

```json
"In the face of your relentless onslaught, the Mad Mage overreaches, drawing too deeply from his own wellspring of power. His laughter turns into a scream as his own magic consumes him, the elemental tempest reaching a climax and then suddenly imploding, a violent silence replacing the chaos. When the dust and steam clear, the Mad Mage is gone, his body reduced to ashes by his own elemental might.\n\nIn the midst of the smoldering remains, a single object catches your eye: a worn, leather-bound book, untouched by the elemental fury that had consumed its master. "
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
"Reward"
```

Campo `/opcoes/0/texto`

```json
"Take the spellbook for yourself."
```

Campo `/opcoes/0/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/efeitos/0/texto`

```json
"Cautiously, you pick it up. The cover reads: 'Expeditions in Elemental Equilibrium by Jason the Devastatingly Sane.'"
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
    "Guid": "abc8a97298d1d304bb9ebdbe9d6f8859",
    "Path": "Island Hex Pieces\\Events\\Mad Mage Victory"
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
    "origem": "resources.assets:2545769",
    "tipo": "PartyEvent",
    "campo": "/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "destino": "resources.assets:2545768"
  },
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/238",
    "destino": "resources.assets:2545768"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[
  {
    "opcao": 1,
    "titulo": "Reward",
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
                    "chave": "resources.assets:2545430",
                    "nome": "Elemental Equilibrium",
                    "pptr": {
                      "m_FileID": 0,
                      "m_PathID": 2545430
                    },
                    "tipo": "EventStatus",
                    "descricao": "Dealing damage with a specific element will grant you a buff that increases all elemental damage. Stacks for each element.\n\n<i><color=#808080>\"Who defines sanity, after all? Is it the crowd of sheep who mindlessly follow the whims of their shepherd, their dull lives dictated by rules and norms? Or is it the lone wolf, who, by daring to break free from the pack, is deemed insane?\"</color></i>",
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

## 80. Unleashed

Chave: `resources.assets:2545769`; GUID: `a7de4c70-7f15-486f-aa7e-40c71c190d9f`; nome_asset: Unleashed.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording: contextualizar a seleção para o confronto, mantendo a fala do Mad Mage.

### Análise específica

- Fight inicia combate com VictoryEvent=2545768. Não alterar a cadeia para capturar o mago: isso seria nova mecânica sem autorização.

- O prompt de pleas tem sujeito possível, mas não corresponde à cena: o mago confronta o jogador e recusa novas correntes.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/campos_originais/promptToSelectCharacter`

Texto atual (literal completo):

```json
"Who will listen to his pleas?"
```

PROPOSTA EXATA (literal completo):

```json
"Who will confront the Mad Mage?"
```

Justificativa: Explicitar o encontro sem prometer resultado.

### Textos atuais não alterados

Campo `/texto`

```json
"After what feels like an eternity, you find him. The <violet><b><incr>Mad Mage</incr></b></violet> stands at the heart of a whirling tempest of raw elemental power. Fire, ice, and lightning cascade off him in radiant waves, painting a terrifying tableau against the sky. As you approach, the Mad Mage turns, a warm smile stretching across his gaunt face.\n\n\n\"If it isn't my liberator,\" he says calmly, stepping forward. His gaze is as wild as the swirling elements around him. \"Tell me, have you come to wish me well in my freedom, or have you grown to fear what you cannot control?\""
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
"Fight"
```

Campo `/opcoes/0/texto`

```json
"You must stop the chaos he brings."
```

Campo `/opcoes/0/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/efeitos/0/texto`

```json
"\"Ah, so it is,\" the Mad Mage sighs, the tempest of elements around him briefly subsiding. \"It's a pity, my liberator. I had hoped you were different.\"\n\n\nA silence falls between you, the only sound the crackling of fire, the drip of melting ice, and the low hum of electricity. The disappointment in the Mad Mage's voice echoes in your ears. But then, the silence is broken as the Mad Mage's expression hardens, his eyes flaring with newfound determination.\n\n\n\"No more!\" he thunders, his voice echoing across the landscape. \"No more chains! Your ignorance, your fear... it will be your downfall!\""
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
    "origem": "resources.assets:2545519",
    "tipo": "EventStatus",
    "campo": "/ForcedNextEvent",
    "destino": "resources.assets:2545769"
  },
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/237",
    "destino": "resources.assets:2545769"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[
  {
    "opcao": 1,
    "titulo": "Fight",
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
                  "m_PathID": 2545167
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
              "m_PathID": 2545768
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

## 81. What Lurks

Chave: `resources.assets:2545772`; GUID: `927680ab-1141-4524-a714-e418cac289f2`; nome_asset: What Lurks - Victory.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MANTER; natureza: nenhuma. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MANTER: epílogo e escolha Take são claros; a fortuna configurada sustenta a referência narrativa ao veneno sem valor inventado.

### Análise específica

- Configura Claw of the Anthulk como fortuna; o benefício final não é calculado neste parecer.

- batalha.iniciar=false, mas VictoryEvent residual aponta 2545547. Tratar como configuração potencialmente inativa; não alegar combate extra nem remover o elo por conta própria.

- A descrição de status contém fechamento de tags fora de ordem e fórmulas. Sinalizar como dado de referência, não reescrever descrição global neste lote.

### Propostas exatas (nenhuma aplicação autorizada)

Nenhuma substituição proposta. Textos atuais completos preservados abaixo.

### Textos atuais não alterados

Campo `/texto`

```json
"With a final shudder, the <b><green><incr>Anthulk</incr></green></b> collapses, its life force draining away into the desert sand. Panting, your eyes fall on the massive claw. It still oozes venom, the lethal toxin gleaming wickedly in the sun."
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

Campo `/opcoes/0/titulo`

```json
"Take"
```

Campo `/opcoes/0/texto`

```json
"Take the venomous claw of the Anthulk."
```

Campo `/opcoes/0/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/efeitos/0/texto`

```json
"With effort, you pry the claw from the beast's lifeless grip, its size and weight substantial even in your strong hands. The venom can make your weapons more lethal, a crucial edge in the unpredictable life of an adventurer. "
```

### Anomalias, disponibilidade e referências

disabled=0; opções=1; ações=1; NULL auditados=11; refs nulas projetadas=1. Todos os caminhos e motivos destes NULL estão individualizados na parte05 e propostas-auditadas.json.

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
      0,
      3,
      5
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
    "Guid": "27929f0fb89857942874ddcc0e1a8fcc",
    "Path": "Island Hex Pieces\\Events\\What Lurks_"
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
    "origem": "resources.assets:2545773",
    "tipo": "PartyEvent",
    "campo": "/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "destino": "resources.assets:2545772"
  },
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/242",
    "destino": "resources.assets:2545772"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[
  {
    "opcao": 1,
    "titulo": "Take",
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
                "razao": 2.0,
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
                  "possibleItemTypes": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5
                  ],
                  "limitItemRarities": 0,
                  "possibleRarities": [
                    2,
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
                    "chave": "resources.assets:2545419",
                    "nome": "Claw of the Anthulk",
                    "pptr": {
                      "m_FileID": 0,
                      "m_PathID": 2545419
                    },
                    "tipo": "EventStatus",
                    "descricao": "Your weapon attacks apply level {1,30} Anthulk Venom: Increases the Physical Damage the target takes by GetFlatDamageDealt(.5, Physical) per stack.\n\n<i><color=#808080>\"The venomous claw of a mature Anthulk.\"</i></color>",
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
            "chave": "resources.assets:2544645",
            "nome": "Cursed Chest Battle",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2544645
            },
            "tipo": "BattleInfo"
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
                  "m_PathID": 2545015
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
              "m_PathID": 2545547
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

## 82. Witch's Pyre

Chave: `resources.assets:2545775`; GUID: `526e30e7-0f03-4409-bb34-35c81045b0aa`; nome_asset: Witch's Pyre - Victory.

Categoria: NotInEventPool; raridade: Rare (2); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording: coerência temporal e prompt de contrato no lugar de Cursed Chest.

### Análise específica

- É o único Rare (2) deste lote. Take tem texto de ação vazio e configura Bloodied Bargain; não fabricar item/XP final.

- Preservar [name] is feeling brave... e suas tags/placeholders; exibição real dos prompts não exercitada.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/texto`

Texto atual (literal completo):

```json
"<b><incr><red>The Risen Witch</red></incr></b> stumbles backwards, a look of disbelief on her face. With a final, desperate incantation, the flames that had failed to consume her on the pyre came to life around her once again.\n\n\nThe inferno surges upwards, consuming the witch in a brilliant spectacle of destruction. Her shriek echoes through the night, a sound of profound agony that sends a chill running down your spine.\n\nAmong the ashes, you find a scroll, seemingly untouched by the flames. A bloody handprint stains the parchment, a grotesque seal that marks the dark contract that had granted the witch her powers."
```

PROPOSTA EXATA (literal completo):

```json
"<b><incr><red>The Risen Witch</red></incr></b> stumbles backwards, a look of disbelief on her face. With a final, desperate incantation, the flames that had failed to consume her on the pyre come to life around her once again.\n\n\nThe inferno surges upwards, consuming the witch in a brilliant spectacle of destruction. Her shriek echoes through the night, a sound of profound agony that sends a chill running down your spine.\n\nAmong the ashes, you find a scroll, seemingly untouched by the flames. A bloody handprint stains the parchment, a grotesque seal that marks the dark contract that had granted the witch her powers."
```

Justificativa: Manter presente com stumbles/surges.

Campo `/campos_originais/promptToSelectCharacter`

Texto atual (literal completo):

```json
"Dare to open the Cursed Chest?"
```

PROPOSTA EXATA (literal completo):

```json
"Who will retrieve the contract?"
```

Justificativa: A cena contém um contrato entre as cinzas, não um baú.

### Textos atuais não alterados

Campo `/texto_resultados_possiveis` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/campos_originais/characterSelectedText`

```json
"[name] is feeling brave..."
```

Campo `/opcoes/0/titulo`

```json
"Take"
```

Campo `/opcoes/0/texto`

```json
"Retrieve the blood-stained contract."
```

Campo `/opcoes/0/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/efeitos/0/texto` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

### Anomalias, disponibilidade e referências

disabled=0; opções=1; ações=1; NULL auditados=11; refs nulas projetadas=1. Todos os caminhos e motivos destes NULL estão individualizados na parte05 e propostas-auditadas.json.

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
      2
    ],
    "allowAtAllTimesOfDay": 1,
    "allowedTimeOfDay": 1,
    "allowAtAllLevels": 1,
    "minLevel": 1,
    "terrainTypesAllowedAtAnyTime": [
      2,
      0,
      3,
      5
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
    "Guid": "493446ec46bfff44a89b595dc75eff85",
    "Path": "Island Hex Pieces\\Events\\Witch's Pyre"
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
    "origem": "resources.assets:2545776",
    "tipo": "PartyEvent",
    "campo": "/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "destino": "resources.assets:2545775"
  },
  {
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/245",
    "destino": "resources.assets:2545775"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[
  {
    "opcao": 1,
    "titulo": "Take",
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
                "razao": 2.0,
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
                  "possibleItemTypes": [
                    0,
                    1,
                    2,
                    3,
                    4,
                    5
                  ],
                  "limitItemRarities": 0,
                  "possibleRarities": [
                    2,
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
                    "chave": "resources.assets:2545412",
                    "nome": "Bloodied Bargain",
                    "pptr": {
                      "m_FileID": 0,
                      "m_PathID": 2545412
                    },
                    "tipo": "EventStatus",
                    "descricao": "Increases @Physical Damage@ by {8,40}%. Physical damage you deal applies 1 stack of @Bleeding@.\n\n<i><color=#808080>A price in blood must be paid, just be sure you're not the one to pay it.</color></i>",
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
                          "chave": "resources.assets:2544380",
                          "nome": "DamageModPhysical",
                          "pptr": {
                            "m_FileID": 0,
                            "m_PathID": 2544380
                          },
                          "tipo": "CharacterAttribute"
                        },
                        "metodo": {
                          "valor": 0,
                          "nome": "Base"
                        },
                        "expressao": "{8,40}",
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
            "chave": "resources.assets:2544645",
            "nome": "Cursed Chest Battle",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2544645
            },
            "tipo": "BattleInfo"
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
                  "m_PathID": 2545119
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

## 83. Ymir Rune, Honor

Chave: `resources.assets:2545782`; GUID: `e826b457-4b55-46db-bd38-0f9239a0b915`; nome_asset: Ymir Rune, Honor - Victory.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording/apresentação: corrigir somente a ordem de fechamento das tags e contextualizar o prompt; disabled permanece 1.

### Análise específica

- Variante disabled=1 com EventPrefabReference Guid/Path vazios. Não habilitar nem eliminar: disponibilidade efetiva não exercitada.

- Configura o QuestItem Ymir Rune, Honor com descrição vazia; não confundir com a fortuna Honor of the Ymir ou a chave ativa 2545783.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/texto`

Texto atual (literal completo):

```json
"You have defeated the <gold><b><incr>Trial of Honor</gold></b></incr>! \n"
```

PROPOSTA EXATA (literal completo):

```json
"You have defeated the <gold><b><incr>Trial of Honor</incr></b></gold>! \n"
```

Justificativa: Fechar na ordem inversa de abertura gold/b/incr; preservar todas as tags e conteúdo.

Campo `/campos_originais/promptToSelectCharacter`

Texto atual (literal completo):

```json
"Who will listen to his pleas?"
```

PROPOSTA EXATA (literal completo):

```json
"Who will claim the rune?"
```

Justificativa: Remover súplica deslocada.

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
"Claim"
```

Campo `/opcoes/0/texto`

```json
"Take the rune."
```

Campo `/opcoes/0/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/efeitos/0/texto`

```json
"Greater honor has given you greater conviction.\n"
```

### Anomalias, disponibilidade e referências

disabled=1; opções=1; ações=1; NULL auditados=13; refs nulas projetadas=2. Todos os caminhos e motivos destes NULL estão individualizados na parte05 e propostas-auditadas.json.

Condições/modos/prefab (literais, sem escolha de variante):

```json
{
  "condicoes": {
    "disabled": 1,
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
    "Guid": "",
    "Path": ""
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
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/252",
    "destino": "resources.assets:2545782"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[
  {
    "opcao": 1,
    "titulo": "Claim",
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
                    "chave": "resources.assets:2545508",
                    "nome": "Ymir Rune, Honor",
                    "pptr": {
                      "m_FileID": 0,
                      "m_PathID": 2545508
                    },
                    "tipo": "EventStatus",
                    "descricao": "",
                    "duracao": {
                      "valor": 3,
                      "nome": "Permanent"
                    },
                    "status_tipo": {
                      "valor": 2,
                      "nome": "QuestItem"
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

## 84. Ymir Rune, Strength

Chave: `resources.assets:2545784`; GUID: `3e15219a-3607-4fe4-ae6f-3fc421135fcb`; nome_asset: Ymir Rune, Strength - Victory.

Categoria: NotInEventPool; raridade: Common (0); peso relativo: 1.0.

VEREDITO PROPOSTO: MELHORAR; natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação: PENDENTE.

MELHORAR wording/apresentação: corrigir fechamento das tags e prompt; manter disabled e encadeamento original.

### Análise específica

- Variante disabled=1, prefab Guid/Path vazios e QuestItem Ymir Rune, Strength com descrição vazia. Nenhuma ativação proposta.

- evento_encadeado aponta 2545783, cuja projeção nome=Ymir Rune, Honor usa nome do asset; o título visível canônico é The runes of the Ymir. Não redirecionar para a chave 2545782 por semelhança de nomes.

### Propostas exatas (nenhuma aplicação autorizada)

Campo `/texto`

Texto atual (literal completo):

```json
"You have defeated the <gold><b><incr>Trial of Strength</gold></b></incr>! \n"
```

PROPOSTA EXATA (literal completo):

```json
"You have defeated the <gold><b><incr>Trial of Strength</incr></b></gold>! \n"
```

Justificativa: Corrigir aninhamento, preservando a mesma coleção de tags.

Campo `/campos_originais/promptToSelectCharacter`

Texto atual (literal completo):

```json
"Who will listen to his pleas?"
```

PROPOSTA EXATA (literal completo):

```json
"Who will claim the rune?"
```

Justificativa: Alinhar a seleção à opção Claim.

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
"Claim"
```

Campo `/opcoes/0/texto`

```json
"Take the rune."
```

Campo `/opcoes/0/rolagem/texto_misterioso` — STRING VAZIA NO ASSET (não NULL).

```json
""
```

Campo `/opcoes/0/efeitos/0/texto`

```json
"The strength to conquer swells within you.\n"
```

### Anomalias, disponibilidade e referências

disabled=1; opções=1; ações=1; NULL auditados=11; refs nulas projetadas=1. Todos os caminhos e motivos destes NULL estão individualizados na parte05 e propostas-auditadas.json.

Condições/modos/prefab (literais, sem escolha de variante):

```json
{
  "condicoes": {
    "disabled": 1,
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
    "Guid": "",
    "Path": ""
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
    "origem": "resources.assets:2547145",
    "tipo": "ListHolderEvents",
    "campo": "/Events/254",
    "destino": "resources.assets:2545784"
  }
]
```

Configuração literal de ações, combate e recompensas (não resultados calculados; projeção de recompensas por opção não é adicional):

```json
[
  {
    "opcao": 1,
    "titulo": "Claim",
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
                    "chave": "resources.assets:2545509",
                    "nome": "Ymir Rune, Strength",
                    "pptr": {
                      "m_FileID": 0,
                      "m_PathID": 2545509
                    },
                    "tipo": "EventStatus",
                    "descricao": "",
                    "duracao": {
                      "valor": 3,
                      "nome": "Permanent"
                    },
                    "status_tipo": {
                      "valor": 2,
                      "nome": "QuestItem"
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
          "chave": "resources.assets:2545783",
          "nome": "Ymir Rune, Honor",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545783
          },
          "tipo": "PartyEvent"
        }
      }
    ]
  }
]
```

NAO_EXERCITADO: runtime/UI, disponibilidade, RNG, aplicação final de status, ouro/XP/loot finais e combate, porque a tarefa proíbe execução do jogo. Referência nula com motivo m_PathID=0 permanece distinta de resultado não exercitado.
