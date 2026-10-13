# EV-R2-FORAPOOL-b02 — parte 04, eventos 36–42

Fontes: `C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-NotInEventPool-v2.md`, `eventos.json`, `eventos.schema.json`, `schema.md` e `catalogo-referencias.json`. Coordenadas `opcoes/0` e `efeitos/0` são índices JSON base zero; títulos Opção 1/Ação 1 são base um. Strings JSON exibem os controles originais. Cada proposta é PENDENTE, não uma decisão do dono. Recompensa/condição: MANTER, sem alteração; aplicação runtime: NAO_EXERCITADO (tarefa offline, sem jogo).


## 36. Pirate's Treasure — resources.assets:2545667

Chave: `resources.assets:2545667`. GUID real: `ae77d198-ad55-44dd-ac1f-8abc86c91f0e`. Asset: `Pirate's Treasure - Victory`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 1; ações: 1; overrides: 0. Origem: `events/pirate's treasure - victory`.

VEREDITO PROPOSTO: MELHORAR — natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

Corrigir ligação de frases, lay/lie e tempo verbal. O tesouro segue figurativo: não transformar Cursed Coin em pagamento de ouro.

### Texto atual → proposta exata

Campo: `texto`.

Atual (campo completo):
```json
"As the last skeleton falls, you turn to the chest. The skeletal pirate has released its grip, the wooden chest now lies open. Within it lays old coins, each glimmering with a sinister aura – a heap of cursed gold. "
```

PROPOSTA EXATA (campo completo):
```json
"As the last skeleton falls, you turn to the chest. The skeletal pirate has released its grip, and the wooden chest now lies open. Within it lie old coins, each glimmering with a sinister aura – a heap of cursed gold. "
```

Justificativa: Corrigir ligação de frases, lay/lie e tempo verbal. O tesouro segue figurativo: não transformar Cursed Coin em pagamento de ouro.

Campo: `opcoes/0/efeitos/0/texto`.

Atual (campo completo):
```json
"You knew the price of greed, but for now, you have the treasure you sought. What the curse will bring, only time will tell."
```

PROPOSTA EXATA (campo completo):
```json
"You know the price of greed, but for now, you have the treasure you sought. What the curse will bring, only time will tell."
```

Justificativa: Corrigir ligação de frases, lay/lie e tempo verbal. O tesouro segue figurativo: não transformar Cursed Coin em pagamento de ouro.

### Todos os textos atuais e decisão por campo

`texto` — MELHORAR conforme proposta acima:
```json
"As the last skeleton falls, you turn to the chest. The skeletal pirate has released its grip, the wooden chest now lies open. Within it lays old coins, each glimmering with a sinister aura – a heap of cursed gold. "
```

`texto_resultados_possiveis` — MANTER:
```json
""
```

`campos_originais/promptToSelectCharacter` — MANTER:
```json
"Who will take the crystal?"
```

`campos_originais/characterSelectedText` — MANTER:
```json
""
```

`opcoes/0/titulo` — MANTER:
```json
"Loot"
```

`opcoes/0/texto` — MANTER:
```json
"Take the cursed gold."
```

`opcoes/0/rolagem/texto_misterioso` — MANTER:
```json
""
```

`opcoes/0/efeitos/0/texto` — MELHORAR conforme proposta acima:
```json
"You knew the price of greed, but for now, you have the treasure you sought. What the curse will bring, only time will tell."
```

### Anomalias, cautelas e limites

- Opção Take the cursed gold concede candidato Cursed Coin (2545423); ouro.dar=false e itens.dar=false. A narrativa não prova pagamento de moedas nem item no inventário.

- Não remover consequências/carga da fortuna nem inventar ouro adicional.

- `disabled=0` é configuração; disponibilidade efetiva NAO_EXERCITADO. Nenhuma remoção/reativação proposta.

- Textos vazios auditados: 3. Campos: `texto_resultados_possiveis`, `campos_originais/characterSelectedText`, `opcoes/0/rolagem/texto_misterioso`.

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
      "chave": "resources.assets:2545423",
      "nome": "Cursed Coin",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Cursed Coin",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545423",
      "nome": "Cursed Coin",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Cursed Coin",
      "registro_catalogo": true,
      "resumo_catalogo": true
    }
  ],
  "pptrs_nao_nulos": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545423
      },
      "chave": "resources.assets:2545423",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Cursed Coin"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[0].CharacterInfo",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545162
      },
      "chave": "resources.assets:2545162",
      "tipo_catalogo": "CharacterInfo",
      "nome_catalogo": "Ice Guardian"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[0].ForcedEnemyMods[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545335
      },
      "chave": "resources.assets:2545335",
      "tipo_catalogo": "EnemyMod",
      "nome_catalogo": "Freezing"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[1].CharacterInfo",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545162
      },
      "chave": "resources.assets:2545162",
      "tipo_catalogo": "CharacterInfo",
      "nome_catalogo": "Ice Guardian"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[1].ForcedEnemyMods[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545335
      },
      "chave": "resources.assets:2545335",
      "tipo_catalogo": "EnemyMod",
      "nome_catalogo": "Freezing"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[2].CharacterInfo",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545162
      },
      "chave": "resources.assets:2545162",
      "tipo_catalogo": "CharacterInfo",
      "nome_catalogo": "Ice Guardian"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[2].ForcedEnemyMods[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545335
      },
      "chave": "resources.assets:2545335",
      "tipo_catalogo": "EnemyMod",
      "nome_catalogo": "Freezing"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[3].CharacterInfo",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545162
      },
      "chave": "resources.assets:2545162",
      "tipo_catalogo": "CharacterInfo",
      "nome_catalogo": "Ice Guardian"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[3].ForcedEnemyMods[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545335
      },
      "chave": "resources.assets:2545335",
      "tipo_catalogo": "EnemyMod",
      "nome_catalogo": "Freezing"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545423
      },
      "chave": "resources.assets:2545423",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Cursed Coin"
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
      "origem": "resources.assets:2545668",
      "campo": "$.opcoes[0].efeitos[0].batalha.override.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545668",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[137]"
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
          "texto": "You knew the price of greed, but for now, you have the treasure you sought. What the curse will bring, only time will tell.",
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
                      "chave": "resources.assets:2545423",
                      "nome": "Cursed Coin",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545423
                      },
                      "tipo": "EventStatus",
                      "descricao": "The first time your health is brought below @1@ instead receive @Cursed Coin@: Health cannot drop below 1. Lasts 2 turns. Applies Ritual Sickness. 1 charge per Quest.\n\n<i><color=#808080>\"Cursed life is still life.\"</color></i>",
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
              "ForcedEnemies": [
                {
                  "OverrideEnemyName": 0,
                  "NameOverride": "",
                  "CharacterInfo": {
                    "m_FileID": 0,
                    "m_PathID": 2545162
                  },
                  "ForcedEnemyMods": [
                    {
                      "m_FileID": 0,
                      "m_PathID": 2545335
                    }
                  ],
                  "IsSuperUnique": 0
                },
                {
                  "OverrideEnemyName": 0,
                  "NameOverride": "",
                  "CharacterInfo": {
                    "m_FileID": 0,
                    "m_PathID": 2545162
                  },
                  "ForcedEnemyMods": [
                    {
                      "m_FileID": 0,
                      "m_PathID": 2545335
                    }
                  ],
                  "IsSuperUnique": 0
                },
                {
                  "OverrideEnemyName": 0,
                  "NameOverride": "",
                  "CharacterInfo": {
                    "m_FileID": 0,
                    "m_PathID": 2545162
                  },
                  "ForcedEnemyMods": [
                    {
                      "m_FileID": 0,
                      "m_PathID": 2545335
                    }
                  ],
                  "IsSuperUnique": 0
                },
                {
                  "OverrideEnemyName": 0,
                  "NameOverride": "",
                  "CharacterInfo": {
                    "m_FileID": 0,
                    "m_PathID": 2545162
                  },
                  "ForcedEnemyMods": [
                    {
                      "m_FileID": 0,
                      "m_PathID": 2545335
                    }
                  ],
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



## 37. Poacher's Demise — resources.assets:2545669

Chave: `resources.assets:2545669`. GUID real: `9738c529-ee32-4a4e-859a-772c18be72fa`. Asset: `Poacher's Prize - Victory`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 1; ações: 1; overrides: 0. Origem: `events/poacher's prize - victory`.

VEREDITO PROPOSTO: MELHORAR — natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

Corrigir a ligação de orações e cage door, preservando a libertação do elefante. A discrepância da fortuna fica explícita para aprovação, sem substituir recompensa.

### Texto atual → proposta exata

Campo: `texto`.

Atual (campo completo):
```json
"With the poachers defeated, you return to the elephant's cage. The lock gives way under your touch, the caged door swings open. The elephant, sensing its newfound freedom, slowly raises its head, its eyes meeting yours.\n\n\nIn a moment of serene understanding, the elephant gently pats you with its trunk, a silent thank you. With a rumble that echoes through the jungle, the elephant then turns and wanders off into the dense foliage, returning to its rightful home.\n\n\n"
```

PROPOSTA EXATA (campo completo):
```json
"With the poachers defeated, you return to the elephant's cage. The lock gives way under your touch, and the cage door swings open. The elephant, sensing its newfound freedom, slowly raises its head, its eyes meeting yours.\n\n\nIn a moment of serene understanding, the elephant gently pats you with its trunk, a silent thank you. With a rumble that echoes through the jungle, the elephant then turns and wanders off into the dense foliage, returning to its rightful home.\n\n\n"
```

Justificativa: Corrigir a ligação de orações e cage door, preservando a libertação do elefante. A discrepância da fortuna fica explícita para aprovação, sem substituir recompensa.

### Todos os textos atuais e decisão por campo

`texto` — MELHORAR conforme proposta acima:
```json
"With the poachers defeated, you return to the elephant's cage. The lock gives way under your touch, the caged door swings open. The elephant, sensing its newfound freedom, slowly raises its head, its eyes meeting yours.\n\n\nIn a moment of serene understanding, the elephant gently pats you with its trunk, a silent thank you. With a rumble that echoes through the jungle, the elephant then turns and wanders off into the dense foliage, returning to its rightful home.\n\n\n"
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
"Reward"
```

`opcoes/0/texto` — MANTER:
```json
""
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

- Opção Reward tem descrição e texto de ação vazios; candidato configurado é Ruby of Rancor (2545465), cuja descrição inclui Die at the end of your turn. A origem da gema não é explicada no texto do elefante.

- Anomalia semântica narrativa/recompensa: propor somente correção gramatical; MANTER recompensa nesta entrega não significa endosso de balanceamento. Não inventar presente do elefante nem trocar fortuna.

- `disabled=0` é configuração; disponibilidade efetiva NAO_EXERCITADO. Nenhuma remoção/reativação proposta.

- Textos vazios auditados: 6. Campos: `texto_resultados_possiveis`, `campos_originais/promptToSelectCharacter`, `campos_originais/characterSelectedText`, `opcoes/0/texto`, `opcoes/0/rolagem/texto_misterioso`, `opcoes/0/efeitos/0/texto`.

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
      "chave": "resources.assets:2545465",
      "nome": "Ruby of Rancor",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Ruby of Rancor",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545465",
      "nome": "Ruby of Rancor",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Ruby of Rancor",
      "registro_catalogo": true,
      "resumo_catalogo": true
    }
  ],
  "pptrs_nao_nulos": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545465
      },
      "chave": "resources.assets:2545465",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Ruby of Rancor"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications[0].ActionStatusPool[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2543476
      },
      "chave": "resources.assets:2543476",
      "tipo_catalogo": "ActionStatusInfo",
      "nome_catalogo": "Ruby Rancor Enemy"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2543476
      },
      "chave": "resources.assets:2543476",
      "tipo_catalogo": "ActionStatusInfo",
      "nome_catalogo": "Ruby Rancor Enemy"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545465
      },
      "chave": "resources.assets:2545465",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Ruby of Rancor"
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
      "origem": "resources.assets:2545670",
      "campo": "$.opcoes[0].efeitos[0].batalha.override.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545670",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[139]"
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
                      "chave": "resources.assets:2545465",
                      "nome": "Ruby of Rancor",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545465
                      },
                      "tipo": "EventStatus",
                      "descricao": "Grants 1 charge of Ruby of Rancor: Grants 3 extra Action Points and reduces Mana Costs. Die at the end of your turn.\n\n<i><color=#808080>The gem seems to hum in your grasp, as if resonating with your heartbeat, its pulses syncing with your own.</color></i>",
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
              "EnemyStatusApplications": [
                {
                  "AllEnemyTypes": 1,
                  "EnemyTypes": [],
                  "Amount": 1,
                  "ActionStatusPool": [
                    {
                      "m_FileID": 0,
                      "m_PathID": 2543476
                    }
                  ]
                }
              ],
              "FillOutBattlePoints": 1,
              "OverrideBattlePoints": 0,
              "BattlePointValue": 8,
              "OverrideEnemyGroupPool": 1,
              "EnemyGroupPool": [
                22
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
              "ovrEnemyStatusRefList": [
                {
                  "m_FileID": 0,
                  "m_PathID": 2543476
                }
              ],
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



## 38. Red Dragon — resources.assets:2545629

Chave: `resources.assets:2545629`. GUID real: `9ad14dbe-13b4-4558-b215-8555482261b8`. Asset: `10 - Red Dragon End`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 0; ações: 0; overrides: 0. Origem: `events/main quests/10 - red dragon end`.

VEREDITO PROPOSTO: MELHORAR — natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

Manter presente e futuro coerentes com o encerramento narrado no presente, sem transformar epílogo em concessão de recompensa.

### Texto atual → proposta exata

Campo: `texto`.

Atual (campo completo):
```json
"The dragon's massive form crashes to the ground, its flames extinguishing in a plume of smoke and ash. The land seems to hold its breath, the sky quieting as the last roar of the dragon fades into silence.\n\nYou stand amidst the smoldering landscape, feeling the weight of what has transpired. Yet, even as you contemplate your victory, you know that your journey is far from over. The realm had become safer, a measure of peace restored, but other dragons still soar the skies, and new challenges would undoubtedly arise.\n\nThe thought of these new challenges stirs within your heart the beginnings of another adventure."
```

PROPOSTA EXATA (campo completo):
```json
"The dragon's massive form crashes to the ground, its flames extinguishing in a plume of smoke and ash. The land seems to hold its breath, the sky quieting as the last roar of the dragon fades into silence.\n\nYou stand amidst the smoldering landscape, feeling the weight of what has transpired. Yet, even as you contemplate your victory, you know that your journey is far from over. The realm has become safer, a measure of peace restored, but other dragons still soar the skies, and new challenges will undoubtedly arise.\n\nThe thought of these new challenges stirs within your heart the beginnings of another adventure."
```

Justificativa: Manter presente e futuro coerentes com o encerramento narrado no presente, sem transformar epílogo em concessão de recompensa.

### Todos os textos atuais e decisão por campo

`texto` — MELHORAR conforme proposta acima:
```json
"The dragon's massive form crashes to the ground, its flames extinguishing in a plume of smoke and ash. The land seems to hold its breath, the sky quieting as the last roar of the dragon fades into silence.\n\nYou stand amidst the smoldering landscape, feeling the weight of what has transpired. Yet, even as you contemplate your victory, you know that your journey is far from over. The realm had become safer, a measure of peace restored, but other dragons still soar the skies, and new challenges would undoubtedly arise.\n\nThe thought of these new challenges stirs within your heart the beginnings of another adventure."
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

- opcoes=[] e AutoStartBattle=0. Não criar botão, loot ou fortune; referências de quest serão auditadas separadamente.

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
      "origem": "resources.assets:2545630",
      "campo": "$.opcoes[0].efeitos[0].batalha.override.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545630",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[98]"
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



## 39. Scent of Blood — resources.assets:2545679

Chave: `resources.assets:2545679`. GUID real: `5d032595-5d84-48e1-a45e-c521fdb9db1d`. Asset: `Scent of Blood - Victory`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 1; ações: 1; overrides: 0. Origem: `events/scent of blood - victory`.

VEREDITO PROPOSTO: MANTER — natureza: wording/recompensa/condicao. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

Reconhecimento da matilha e aceitação da liderança são coerentes com Mark of the Alpha. Sem erro obrigatório ou prova offline para alterar recompensa/condição.

### Texto atual → proposta exata

MANTER todos os campos textuais; nenhuma substituição proposta.

### Todos os textos atuais e decisão por campo

`texto` — MANTER:
```json
"In the aftermath of the battle, the rest of the wolf pack emerges from the shadows of the mountain, their eyes fixed on you. But instead of hostility or vengeance, there is a sense of recognition in their gaze. They have witnessed the fall of their alpha and understand the unspoken law of the wild – strength commands respect.\n"
```

`texto_resultados_possiveis` — MANTER:
```json
""
```

`campos_originais/promptToSelectCharacter` — MANTER:
```json
"Who will learn the Dark Ritual?"
```

`campos_originais/characterSelectedText` — MANTER:
```json
""
```

`opcoes/0/titulo` — MANTER:
```json
"Reward"
```

`opcoes/0/texto` — MANTER:
```json
"Accept your place as the new alpha."
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

- Ação sem texto de ativação: manter e sinalizar. Candidato Mark of the Alpha (2545451), aplicação e seleção finais NAO_EXERCITADO.

- Descrição do candidato contém tags em ordem incomum; preservá-las no catálogo, sem ampliar a revisão para alteração de EventStatus.

- `disabled=0` é configuração; disponibilidade efetiva NAO_EXERCITADO. Nenhuma remoção/reativação proposta.

- Textos vazios auditados: 4. Campos: `texto_resultados_possiveis`, `campos_originais/characterSelectedText`, `opcoes/0/rolagem/texto_misterioso`, `opcoes/0/efeitos/0/texto`.

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
      "chave": "resources.assets:2545451",
      "nome": "Mark of the Alpha",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Mark of the Alpha",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544568",
      "nome": "SummonDamageMod",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "SummonDamageMod",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[1].atributo",
      "chave": "resources.assets:2544572",
      "nome": "SummonHealthMod",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "SummonHealthMod",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545451",
      "nome": "Mark of the Alpha",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Mark of the Alpha",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544568",
      "nome": "SummonDamageMod",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "SummonDamageMod",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].modificadores[1].atributo",
      "chave": "resources.assets:2544572",
      "nome": "SummonHealthMod",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "SummonHealthMod",
      "registro_catalogo": true,
      "resumo_catalogo": true
    }
  ],
  "pptrs_nao_nulos": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545451
      },
      "chave": "resources.assets:2545451",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Mark of the Alpha"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544568
      },
      "chave": "resources.assets:2544568",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "SummonDamageMod"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[1].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544572
      },
      "chave": "resources.assets:2544572",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "SummonHealthMod"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545451
      },
      "chave": "resources.assets:2545451",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Mark of the Alpha"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544568
      },
      "chave": "resources.assets:2544568",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "SummonDamageMod"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].modificadores[1].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544572
      },
      "chave": "resources.assets:2544572",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "SummonHealthMod"
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
      "origem": "resources.assets:2545678",
      "campo": "$.opcoes[0].efeitos[0].batalha.override.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545678",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[148]"
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
                      "chave": "resources.assets:2545451",
                      "nome": "Mark of the Alpha",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545451
                      },
                      "tipo": "EventStatus",
                      "descricao": "<i><color=#808080>\"Look at me, I'm the alpha now!</i></color> \n\nChanges your @Nature Summons@ into @Pack Summons@. Increases Summon Damage and Health by {5,25}%",
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
                            "chave": "resources.assets:2544568",
                            "nome": "SummonDamageMod",
                            "pptr": {
                              "m_FileID": 0,
                              "m_PathID": 2544568
                            },
                            "tipo": "CharacterAttribute"
                          },
                          "metodo": {
                            "valor": 0,
                            "nome": "Base"
                          },
                          "expressao": "{5,25}",
                          "segunda_passagem": false
                        },
                        {
                          "atributo": {
                            "chave": "resources.assets:2544572",
                            "nome": "SummonHealthMod",
                            "pptr": {
                              "m_FileID": 0,
                              "m_PathID": 2544572
                            },
                            "tipo": "CharacterAttribute"
                          },
                          "metodo": {
                            "valor": 0,
                            "nome": "Base"
                          },
                          "expressao": "{5,25}",
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



## 40. Strange Crystal — resources.assets:2545695

Chave: `resources.assets:2545695`. GUID real: `16484ea1-d515-436f-85d1-d9ec385681e2`. Asset: `Strange Ice Crystal - Victory`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 1; ações: 1; overrides: 0. Origem: `events/strange ice crystal - victory`.

VEREDITO PROPOSTO: MELHORAR — natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

Corrigir a grafia do adjetivo frostbitten; manter identificação do cristal de gelo e não adicionar números ao resultado.

### Texto atual → proposta exata

Campo: `texto`.

Atual (campo completo):
```json
"You chip away at the frozen behemoths until they fall back, dissipating into puddles of icy water. Panting and frost-bitten, you turn your attention back to the floating crystal."
```

PROPOSTA EXATA (campo completo):
```json
"You chip away at the frozen behemoths until they fall back, dissipating into puddles of icy water. Panting and frostbitten, you turn your attention back to the floating crystal."
```

Justificativa: Corrigir a grafia do adjetivo frostbitten; manter identificação do cristal de gelo e não adicionar números ao resultado.

### Todos os textos atuais e decisão por campo

`texto` — MELHORAR conforme proposta acima:
```json
"You chip away at the frozen behemoths until they fall back, dissipating into puddles of icy water. Panting and frost-bitten, you turn your attention back to the floating crystal."
```

`texto_resultados_possiveis` — MANTER:
```json
""
```

`campos_originais/promptToSelectCharacter` — MANTER:
```json
"Who will take the crystal?"
```

`campos_originais/characterSelectedText` — MANTER:
```json
""
```

`opcoes/0/titulo` — MANTER:
```json
"Claim your reward"
```

`opcoes/0/texto` — MANTER:
```json
""
```

`opcoes/0/rolagem/texto_misterioso` — MANTER:
```json
""
```

`opcoes/0/efeitos/0/texto` — MANTER:
```json
"You can feel the power humming beneath your fingertips as you touch the gleaming surface of the crystal, a shard breaking off cleanly in your hand. A jolt of energy surges into you, the crystal's icy power now yours to command."
```

### Anomalias, cautelas e limites

- Descrição da opção Claim your reward está vazia; manter. Candidato Ice Crystal (2545449), sem preencher @level@ ou {1,30} do catálogo.

- `disabled=0` é configuração; disponibilidade efetiva NAO_EXERCITADO. Nenhuma remoção/reativação proposta.

- Textos vazios auditados: 4. Campos: `texto_resultados_possiveis`, `campos_originais/characterSelectedText`, `opcoes/0/texto`, `opcoes/0/rolagem/texto_misterioso`.

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
      "chave": "resources.assets:2545449",
      "nome": "Ice Crystal",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Ice Crystal",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545449",
      "nome": "Ice Crystal",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Ice Crystal",
      "registro_catalogo": true,
      "resumo_catalogo": true
    }
  ],
  "pptrs_nao_nulos": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545449
      },
      "chave": "resources.assets:2545449",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Ice Crystal"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[0].CharacterInfo",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545162
      },
      "chave": "resources.assets:2545162",
      "tipo_catalogo": "CharacterInfo",
      "nome_catalogo": "Ice Guardian"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[0].ForcedEnemyMods[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545335
      },
      "chave": "resources.assets:2545335",
      "tipo_catalogo": "EnemyMod",
      "nome_catalogo": "Freezing"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[1].CharacterInfo",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545162
      },
      "chave": "resources.assets:2545162",
      "tipo_catalogo": "CharacterInfo",
      "nome_catalogo": "Ice Guardian"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[1].ForcedEnemyMods[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545335
      },
      "chave": "resources.assets:2545335",
      "tipo_catalogo": "EnemyMod",
      "nome_catalogo": "Freezing"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[2].CharacterInfo",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545162
      },
      "chave": "resources.assets:2545162",
      "tipo_catalogo": "CharacterInfo",
      "nome_catalogo": "Ice Guardian"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[2].ForcedEnemyMods[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545335
      },
      "chave": "resources.assets:2545335",
      "tipo_catalogo": "EnemyMod",
      "nome_catalogo": "Freezing"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[3].CharacterInfo",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545162
      },
      "chave": "resources.assets:2545162",
      "tipo_catalogo": "CharacterInfo",
      "nome_catalogo": "Ice Guardian"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[3].ForcedEnemyMods[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545335
      },
      "chave": "resources.assets:2545335",
      "tipo_catalogo": "EnemyMod",
      "nome_catalogo": "Freezing"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545449
      },
      "chave": "resources.assets:2545449",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Ice Crystal"
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
      "origem": "resources.assets:2545696",
      "campo": "$.opcoes[0].efeitos[0].batalha.override.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545696",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[165]"
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
          "texto": "You can feel the power humming beneath your fingertips as you touch the gleaming surface of the crystal, a shard breaking off cleanly in your hand. A jolt of energy surges into you, the crystal's icy power now yours to command.",
          "resultado": {
            "valor": 0,
            "nome": "Success"
          },
          "limite_rolagem": 16,
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
                      "chave": "resources.assets:2545449",
                      "nome": "Ice Crystal",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545449
                      },
                      "tipo": "EventStatus",
                      "descricao": "<i><color=#808080>The magic crystal emanates cold.</color></i>\n\nAllows you to summon a @level@ {1,30} Ice Golem to fight for you. Benefits from your @Cold Damage@.",
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
              "ForcedEnemies": [
                {
                  "OverrideEnemyName": 0,
                  "NameOverride": "",
                  "CharacterInfo": {
                    "m_FileID": 0,
                    "m_PathID": 2545162
                  },
                  "ForcedEnemyMods": [
                    {
                      "m_FileID": 0,
                      "m_PathID": 2545335
                    }
                  ],
                  "IsSuperUnique": 0
                },
                {
                  "OverrideEnemyName": 0,
                  "NameOverride": "",
                  "CharacterInfo": {
                    "m_FileID": 0,
                    "m_PathID": 2545162
                  },
                  "ForcedEnemyMods": [
                    {
                      "m_FileID": 0,
                      "m_PathID": 2545335
                    }
                  ],
                  "IsSuperUnique": 0
                },
                {
                  "OverrideEnemyName": 0,
                  "NameOverride": "",
                  "CharacterInfo": {
                    "m_FileID": 0,
                    "m_PathID": 2545162
                  },
                  "ForcedEnemyMods": [
                    {
                      "m_FileID": 0,
                      "m_PathID": 2545335
                    }
                  ],
                  "IsSuperUnique": 0
                },
                {
                  "OverrideEnemyName": 0,
                  "NameOverride": "",
                  "CharacterInfo": {
                    "m_FileID": 0,
                    "m_PathID": 2545162
                  },
                  "ForcedEnemyMods": [
                    {
                      "m_FileID": 0,
                      "m_PathID": 2545335
                    }
                  ],
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



## 41. Strange Crystal — resources.assets:2545698

Chave: `resources.assets:2545698`. GUID real: `af416be6-411b-4377-a37d-e712b04b6c4e`. Asset: `Strange Molten Crystal - Victory`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 1; ações: 1; overrides: 0. Origem: `events/strange molten crystal - victory`.

VEREDITO PROPOSTO: MELHORAR — natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

Corrigir vírgula entre orações independentes na queda do golem, preservando a recompensa de fogo e distinguindo-a das outras variantes.

### Texto atual → proposta exata

Campo: `texto`.

Atual (campo completo):
```json
"The last golem crumbles, its once fiery eyes now dull and lifeless, the molten rock cools into a dark, hard crust. Panting heavily, you turn back to the crystal. The air around it still radiates an intense heat, but now, it feels like a challenge instead of a warning."
```

PROPOSTA EXATA (campo completo):
```json
"The last golem crumbles, its once-fiery eyes now dull and lifeless. The molten rock cools into a dark, hard crust. Panting heavily, you turn back to the crystal. The air around it still radiates an intense heat, but now, it feels like a challenge instead of a warning."
```

Justificativa: Corrigir vírgula entre orações independentes na queda do golem, preservando a recompensa de fogo e distinguindo-a das outras variantes.

### Todos os textos atuais e decisão por campo

`texto` — MELHORAR conforme proposta acima:
```json
"The last golem crumbles, its once fiery eyes now dull and lifeless, the molten rock cools into a dark, hard crust. Panting heavily, you turn back to the crystal. The air around it still radiates an intense heat, but now, it feels like a challenge instead of a warning."
```

`texto_resultados_possiveis` — MANTER:
```json
""
```

`campos_originais/promptToSelectCharacter` — MANTER:
```json
"Who will take the crystal?"
```

`campos_originais/characterSelectedText` — MANTER:
```json
""
```

`opcoes/0/titulo` — MANTER:
```json
"Claim your reward"
```

`opcoes/0/texto` — MANTER:
```json
""
```

`opcoes/0/rolagem/texto_misterioso` — MANTER:
```json
""
```

`opcoes/0/efeitos/0/texto` — MANTER:
```json
"Slowly, you reach out again, your hand trembling as it nears the scorching aura. With a quick, determined motion, you break a piece off. A surge of power rushes through you, pure and intense, grounding you despite the blistering heat."
```

### Anomalias, cautelas e limites

- Descrição da opção Claim your reward está vazia; manter. Candidato Molten Crystal (2545456), não Ice Crystal nem Thunder Crystal.

- `disabled=0` é configuração; disponibilidade efetiva NAO_EXERCITADO. Nenhuma remoção/reativação proposta.

- Textos vazios auditados: 4. Campos: `texto_resultados_possiveis`, `campos_originais/characterSelectedText`, `opcoes/0/texto`, `opcoes/0/rolagem/texto_misterioso`.

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
      "chave": "resources.assets:2545456",
      "nome": "Molten Crystal",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Molten Crystal",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545456",
      "nome": "Molten Crystal",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Molten Crystal",
      "registro_catalogo": true,
      "resumo_catalogo": true
    }
  ],
  "pptrs_nao_nulos": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545456
      },
      "chave": "resources.assets:2545456",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Molten Crystal"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[0].CharacterInfo",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545162
      },
      "chave": "resources.assets:2545162",
      "tipo_catalogo": "CharacterInfo",
      "nome_catalogo": "Ice Guardian"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[0].ForcedEnemyMods[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545335
      },
      "chave": "resources.assets:2545335",
      "tipo_catalogo": "EnemyMod",
      "nome_catalogo": "Freezing"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[1].CharacterInfo",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545162
      },
      "chave": "resources.assets:2545162",
      "tipo_catalogo": "CharacterInfo",
      "nome_catalogo": "Ice Guardian"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[1].ForcedEnemyMods[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545335
      },
      "chave": "resources.assets:2545335",
      "tipo_catalogo": "EnemyMod",
      "nome_catalogo": "Freezing"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[2].CharacterInfo",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545162
      },
      "chave": "resources.assets:2545162",
      "tipo_catalogo": "CharacterInfo",
      "nome_catalogo": "Ice Guardian"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[2].ForcedEnemyMods[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545335
      },
      "chave": "resources.assets:2545335",
      "tipo_catalogo": "EnemyMod",
      "nome_catalogo": "Freezing"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[3].CharacterInfo",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545162
      },
      "chave": "resources.assets:2545162",
      "tipo_catalogo": "CharacterInfo",
      "nome_catalogo": "Ice Guardian"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[3].ForcedEnemyMods[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545335
      },
      "chave": "resources.assets:2545335",
      "tipo_catalogo": "EnemyMod",
      "nome_catalogo": "Freezing"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545456
      },
      "chave": "resources.assets:2545456",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Molten Crystal"
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
      "origem": "resources.assets:2545699",
      "campo": "$.opcoes[0].efeitos[0].batalha.override.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545699",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[168]"
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
          "texto": "Slowly, you reach out again, your hand trembling as it nears the scorching aura. With a quick, determined motion, you break a piece off. A surge of power rushes through you, pure and intense, grounding you despite the blistering heat.",
          "resultado": {
            "valor": 0,
            "nome": "Success"
          },
          "limite_rolagem": 16,
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
                      "chave": "resources.assets:2545456",
                      "nome": "Molten Crystal",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545456
                      },
                      "tipo": "EventStatus",
                      "descricao": "<i><color=#808080>The magic crystal emanates heat.</color></i>\n\nAllows you to summon a @level@ {1,30} Molten Golem to fight for you. Benefits from your @Fire Damage@.",
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
              "ForcedEnemies": [
                {
                  "OverrideEnemyName": 0,
                  "NameOverride": "",
                  "CharacterInfo": {
                    "m_FileID": 0,
                    "m_PathID": 2545162
                  },
                  "ForcedEnemyMods": [
                    {
                      "m_FileID": 0,
                      "m_PathID": 2545335
                    }
                  ],
                  "IsSuperUnique": 0
                },
                {
                  "OverrideEnemyName": 0,
                  "NameOverride": "",
                  "CharacterInfo": {
                    "m_FileID": 0,
                    "m_PathID": 2545162
                  },
                  "ForcedEnemyMods": [
                    {
                      "m_FileID": 0,
                      "m_PathID": 2545335
                    }
                  ],
                  "IsSuperUnique": 0
                },
                {
                  "OverrideEnemyName": 0,
                  "NameOverride": "",
                  "CharacterInfo": {
                    "m_FileID": 0,
                    "m_PathID": 2545162
                  },
                  "ForcedEnemyMods": [
                    {
                      "m_FileID": 0,
                      "m_PathID": 2545335
                    }
                  ],
                  "IsSuperUnique": 0
                },
                {
                  "OverrideEnemyName": 0,
                  "NameOverride": "",
                  "CharacterInfo": {
                    "m_FileID": 0,
                    "m_PathID": 2545162
                  },
                  "ForcedEnemyMods": [
                    {
                      "m_FileID": 0,
                      "m_PathID": 2545335
                    }
                  ],
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



## 42. Strange Crystal — resources.assets:2545701

Chave: `resources.assets:2545701`. GUID real: `f4237415-7dae-4398-8804-812ac8fe4c10`. Asset: `Strange Thunder Crystal - Victory`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 1; ações: 1; overrides: 0. Origem: `events/strange thunder crystal - victory`.

VEREDITO PROPOSTO: MANTER — natureza: wording/recompensa/condicao. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

O fim da tempestade e a retirada do fragmento são claros e compatíveis com a variante de trovão. Cortar repetição seria preferência estilística, não correção necessária.

### Texto atual → proposta exata

MANTER todos os campos textuais; nenhuma substituição proposta.

### Todos os textos atuais e decisão por campo

`texto` — MANTER:
```json
"The last thunder golem disintegrates into a burst of light and sound, leaving behind a quiet that is only interrupted by the soft pitter-patter of the rain. The storm has passed, leaving behind a sense of peace."
```

`texto_resultados_possiveis` — MANTER:
```json
""
```

`campos_originais/promptToSelectCharacter` — MANTER:
```json
"Who will take the crystal?"
```

`campos_originais/characterSelectedText` — MANTER:
```json
""
```

`opcoes/0/titulo` — MANTER:
```json
"Claim your reward"
```

`opcoes/0/texto` — MANTER:
```json
""
```

`opcoes/0/rolagem/texto_misterioso` — MANTER:
```json
""
```

`opcoes/0/efeitos/0/texto` — MANTER:
```json
"You approach the crystal once more. This time, instead of a threatening storm, a calming drizzle surrounds you. You take the crystal into your hand, feeling its cool surface against your warm skin. With a swift, controlled motion, you break off a shard. A rush of energy courses through you, powerful and electrifying."
```

### Anomalias, cautelas e limites

- Descrição da opção Claim your reward está vazia; manter. Candidato Thunder Crystal (2545479); preservar esta chave física e não fundir as três Strange Crystal.

- `disabled=0` é configuração; disponibilidade efetiva NAO_EXERCITADO. Nenhuma remoção/reativação proposta.

- Textos vazios auditados: 4. Campos: `texto_resultados_possiveis`, `campos_originais/characterSelectedText`, `opcoes/0/texto`, `opcoes/0/rolagem/texto_misterioso`.

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
      "chave": "resources.assets:2545479",
      "nome": "Thunder Crystal",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Thunder Crystal",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545479",
      "nome": "Thunder Crystal",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Thunder Crystal",
      "registro_catalogo": true,
      "resumo_catalogo": true
    }
  ],
  "pptrs_nao_nulos": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545479
      },
      "chave": "resources.assets:2545479",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Thunder Crystal"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[0].CharacterInfo",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545162
      },
      "chave": "resources.assets:2545162",
      "tipo_catalogo": "CharacterInfo",
      "nome_catalogo": "Ice Guardian"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[0].ForcedEnemyMods[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545335
      },
      "chave": "resources.assets:2545335",
      "tipo_catalogo": "EnemyMod",
      "nome_catalogo": "Freezing"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[1].CharacterInfo",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545162
      },
      "chave": "resources.assets:2545162",
      "tipo_catalogo": "CharacterInfo",
      "nome_catalogo": "Ice Guardian"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[1].ForcedEnemyMods[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545335
      },
      "chave": "resources.assets:2545335",
      "tipo_catalogo": "EnemyMod",
      "nome_catalogo": "Freezing"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[2].CharacterInfo",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545162
      },
      "chave": "resources.assets:2545162",
      "tipo_catalogo": "CharacterInfo",
      "nome_catalogo": "Ice Guardian"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[2].ForcedEnemyMods[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545335
      },
      "chave": "resources.assets:2545335",
      "tipo_catalogo": "EnemyMod",
      "nome_catalogo": "Freezing"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[3].CharacterInfo",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545162
      },
      "chave": "resources.assets:2545162",
      "tipo_catalogo": "CharacterInfo",
      "nome_catalogo": "Ice Guardian"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[3].ForcedEnemyMods[0]",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545335
      },
      "chave": "resources.assets:2545335",
      "tipo_catalogo": "EnemyMod",
      "nome_catalogo": "Freezing"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545479
      },
      "chave": "resources.assets:2545479",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Thunder Crystal"
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
      "origem": "resources.assets:2545702",
      "campo": "$.opcoes[0].efeitos[0].batalha.override.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545702",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[171]"
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
          "texto": "You approach the crystal once more. This time, instead of a threatening storm, a calming drizzle surrounds you. You take the crystal into your hand, feeling its cool surface against your warm skin. With a swift, controlled motion, you break off a shard. A rush of energy courses through you, powerful and electrifying.",
          "resultado": {
            "valor": 0,
            "nome": "Success"
          },
          "limite_rolagem": 16,
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
                      "chave": "resources.assets:2545479",
                      "nome": "Thunder Crystal",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545479
                      },
                      "tipo": "EventStatus",
                      "descricao": "<i><color=#808080>Energy hums within this magic crystal.</color></i>\n\nAllows you to summon a @level@ {1,30} Thunder Golem to fight for you. Benefits from your @Lightning Damage@.",
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
              "ForcedEnemies": [
                {
                  "OverrideEnemyName": 0,
                  "NameOverride": "",
                  "CharacterInfo": {
                    "m_FileID": 0,
                    "m_PathID": 2545162
                  },
                  "ForcedEnemyMods": [
                    {
                      "m_FileID": 0,
                      "m_PathID": 2545335
                    }
                  ],
                  "IsSuperUnique": 0
                },
                {
                  "OverrideEnemyName": 0,
                  "NameOverride": "",
                  "CharacterInfo": {
                    "m_FileID": 0,
                    "m_PathID": 2545162
                  },
                  "ForcedEnemyMods": [
                    {
                      "m_FileID": 0,
                      "m_PathID": 2545335
                    }
                  ],
                  "IsSuperUnique": 0
                },
                {
                  "OverrideEnemyName": 0,
                  "NameOverride": "",
                  "CharacterInfo": {
                    "m_FileID": 0,
                    "m_PathID": 2545162
                  },
                  "ForcedEnemyMods": [
                    {
                      "m_FileID": 0,
                      "m_PathID": 2545335
                    }
                  ],
                  "IsSuperUnique": 0
                },
                {
                  "OverrideEnemyName": 0,
                  "NameOverride": "",
                  "CharacterInfo": {
                    "m_FileID": 0,
                    "m_PathID": 2545162
                  },
                  "ForcedEnemyMods": [
                    {
                      "m_FileID": 0,
                      "m_PathID": 2545335
                    }
                  ],
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


