# EV-R2-FORAPOOL-b02 — parte 03, eventos 29–35

Fontes: `C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-NotInEventPool-v2.md`, `eventos.json`, `eventos.schema.json`, `schema.md` e `catalogo-referencias.json`. Coordenadas `opcoes/0` e `efeitos/0` são índices JSON base zero; títulos Opção 1/Ação 1 são base um. Strings JSON exibem os controles originais. Cada proposta é PENDENTE, não uma decisão do dono. Recompensa/condição: MANTER, sem alteração; aplicação runtime: NAO_EXERCITADO (tarefa offline, sem jogo).


## 29. Master of Rage — resources.assets:2545650

Chave: `resources.assets:2545650`. GUID real: `bc2329a7-1bb4-427a-89f2-afbbc4e157d0`. Asset: `Master of Rage - Victory`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 1; ações: 1; overrides: 0. Origem: `events/master of rage - victory`.

VEREDITO PROPOSTO: MELHORAR — natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

Eliminar fragmento solto e alinhar a ambientação da confirmação à floresta já descrita; não alterar a habilidade configurada.

### Texto atual → proposta exata

Campo: `texto`.

Atual (campo completo):
```json
"As the last wendigo falls, the forest seems to breathe a sigh of relief. You are weary but victorious. \n\nIn the aftermath of the battle, Barloc emerges from the shadowed woods. His gaze is intense, taking in the scene before him. The fallen Wendigos, the triumphant hero, the churned earth and shattered trees.\r\n\r\nWith a nod of approval, he approaches you. \"You fought well,\" he says, his deep voice booming in the silent forest. \"You've faced the fury and sins of others, and now it's time to face your own.\"\r\n\r\nYou listen attentively as Barloc imparts his wisdom, his words carrying the weight of countless battles and years spent perfecting his rage. "
```

PROPOSTA EXATA (campo completo):
```json
"As the last wendigo falls, the forest seems to breathe a sigh of relief. You are weary but victorious. \n\nIn the aftermath of the battle, Barloc emerges from the shadowed woods. His gaze is intense as he takes in the scene before him: the fallen wendigos, the triumphant hero, the churned earth and shattered trees.\r\n\r\nWith a nod of approval, he approaches you. \"You fought well,\" he says, his deep voice booming in the silent forest. \"You've faced the fury and sins of others, and now it's time to face your own.\"\r\n\r\nYou listen attentively as Barloc imparts his wisdom, his words carrying the weight of countless battles and years spent perfecting his rage. "
```

Justificativa: Eliminar fragmento solto e alinhar a ambientação da confirmação à floresta já descrita; não alterar a habilidade configurada.

Campo: `opcoes/0/efeitos/0/texto`.

Atual (campo completo):
```json
"The grizzled barbarian's lessons echo in the quiet mountain, promising new levels of power and control. "
```

PROPOSTA EXATA (campo completo):
```json
"The grizzled barbarian's lessons echo in the quiet forest, promising new levels of power and control. "
```

Justificativa: Eliminar fragmento solto e alinhar a ambientação da confirmação à floresta já descrita; não alterar a habilidade configurada.

### Todos os textos atuais e decisão por campo

`texto` — MELHORAR conforme proposta acima:
```json
"As the last wendigo falls, the forest seems to breathe a sigh of relief. You are weary but victorious. \n\nIn the aftermath of the battle, Barloc emerges from the shadowed woods. His gaze is intense, taking in the scene before him. The fallen Wendigos, the triumphant hero, the churned earth and shattered trees.\r\n\r\nWith a nod of approval, he approaches you. \"You fought well,\" he says, his deep voice booming in the silent forest. \"You've faced the fury and sins of others, and now it's time to face your own.\"\r\n\r\nYou listen attentively as Barloc imparts his wisdom, his words carrying the weight of countless battles and years spent perfecting his rage. "
```

`texto_resultados_possiveis` — MANTER:
```json
""
```

`campos_originais/promptToSelectCharacter` — MANTER:
```json
"Who will listen to his pleas?"
```

`campos_originais/characterSelectedText` — MANTER:
```json
""
```

`opcoes/0/titulo` — MANTER:
```json
"Learn"
```

`opcoes/0/texto` — MANTER:
```json
"Perfect your rage."
```

`opcoes/0/rolagem/texto_misterioso` — MANTER:
```json
""
```

`opcoes/0/efeitos/0/texto` — MELHORAR conforme proposta acima:
```json
"The grizzled barbarian's lessons echo in the quiet mountain, promising new levels of power and control. "
```

### Anomalias, cautelas e limites

- Fortuna Perfect Rage (2545460) é a configuração consultada. A concessão/aplicação efetiva da skill no personagem é NAO_EXERCITADO.

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
      "chave": "resources.assets:2545460",
      "nome": "Perfect Rage",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Perfect Rage",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545460",
      "nome": "Perfect Rage",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Perfect Rage",
      "registro_catalogo": true,
      "resumo_catalogo": true
    }
  ],
  "pptrs_nao_nulos": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545460
      },
      "chave": "resources.assets:2545460",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Perfect Rage"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545460
      },
      "chave": "resources.assets:2545460",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Perfect Rage"
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
      "origem": "resources.assets:2545649",
      "campo": "$.opcoes[0].efeitos[0].batalha.override.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545649",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[120]"
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
          "texto": "The grizzled barbarian's lessons echo in the quiet mountain, promising new levels of power and control. ",
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
                      "chave": "resources.assets:2545460",
                      "nome": "Perfect Rage",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545460
                      },
                      "tipo": "EventStatus",
                      "descricao": "Grants the skill Perfect Rage.\n\n<i><color=#808080>\"Rage, like fire, in our veins does ignite,\nA storm within, both destroyer and might.\"</i></color>\n",
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
              "remocoes_status": [
                {
                  "RemovalCondition": "ActionStatus.Name == \"Rage Unleashed\"",
                  "RemovalTarget": 1,
                  "ActionOnRemoval": {
                    "m_FileID": 0,
                    "m_PathID": 0
                  },
                  "DurationTypesToRemove": [
                    1
                  ],
                  "FilterBenefitType": 0,
                  "BenefitType": 0,
                  "NumStatusesToRemove": "",
                  "StealStatuses": 0,
                  "GiveStatuses": 0,
                  "ForceDispell": 0
                }
              ]
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



## 30. Mimic — resources.assets:2545754

Chave: `resources.assets:2545754`. GUID real: `edab07b7-0e1e-4958-b9f1-d0682e99e999`. Asset: `Treasure Chest Mimic Victory`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 3; ações: 3; overrides: 0. Origem: `events/treasure chest mimic victory`.

VEREDITO PROPOSTO: MANTER — natureza: wording/recompensa/condicao. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

Narração e três alternativas são legíveis e coerentes com os candidatos. A metáfora das asas não é promessa de voo literal. Sem evidência offline para rebalancear ou reescrever só por preferência.

### Texto atual → proposta exata

MANTER todos os campos textuais; nenhuma substituição proposta.

### Todos os textos atuais e decisão por campo

`texto` — MANTER:
```json
"With a final, bone-rattling roar, the Mimic convulses, then collapses, slowly dissolving into an amorphous mass.\n\n\nWhere the Mimic has fallen, a shimmering pile of treasure remains."
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
"Scroll of Monster Summoning"
```

`opcoes/0/texto` — MANTER:
```json
"Did that scroll just growl?"
```

`opcoes/1/titulo` — MANTER:
```json
"Elixir of the Scarlet Ox"
```

`opcoes/1/texto` — MANTER:
```json
"The potion bubbles with magic."
```

`opcoes/2/titulo` — MANTER:
```json
"Silver Signet"
```

`opcoes/2/texto` — MANTER:
```json
"The small signet shines brightly even in the dark."
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
"As you unroll it, an image of a hulking beast claws itself into existence, so realistic that it seems as if it could burst from the parchment at any moment. It snarls, snapping its jaws and swiping with lethal-looking claws."
```

`opcoes/1/efeitos/0/texto` — MANTER:
```json
"The potion glows with a fiery hue, illuminating the shadows of your face. Drinking it in the heat of battle would metaphorically bestow upon you wings."
```

`opcoes/2/efeitos/0/texto` — MANTER:
```json
"The moment you touch the ring, you hear the distant clashing of steel, as if phantom warriors were locked in eternal battle. It is a haunting sound, echoing from another time and place. The ring is likely tied to a lineage of warriors, perhaps a token of battle or symbol of honor."
```

### Anomalias, cautelas e limites

- Scroll of Monster Summoning, Elixir of the Scarlet Ox e Silver Signet são EventStatus configurados, não três itens de loot. Preservar fórmulas e descrições do catálogo; RNG/nível/aplicação final NAO_EXERCITADO.

- Manter as três quebras de linha na narrativa; a aparência na UI não foi exercitada.

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
      "chave": "resources.assets:2545467",
      "nome": "Scroll of Monster Summoning",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Scroll of Monster Summoning",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545467",
      "nome": "Scroll of Monster Summoning",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Scroll of Monster Summoning",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.status.candidatos[0]",
      "chave": "resources.assets:2545432",
      "nome": "Elixir of the Scarlet Ox",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Elixir of the Scarlet Ox",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[1].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545432",
      "nome": "Elixir of the Scarlet Ox",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Elixir of the Scarlet Ox",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.status.candidatos[0]",
      "chave": "resources.assets:2545470",
      "nome": "Silver Signet",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Silver Signet",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544501",
      "nome": "AdditionalWeaponDamage",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "AdditionalWeaponDamage",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[1].atributo",
      "chave": "resources.assets:2544401",
      "nome": "Armor",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "Armor",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[2].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545470",
      "nome": "Silver Signet",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Silver Signet",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[2].recompensas[0].padrao[0].status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544501",
      "nome": "AdditionalWeaponDamage",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "AdditionalWeaponDamage",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[2].recompensas[0].padrao[0].status.candidatos[0].modificadores[1].atributo",
      "chave": "resources.assets:2544401",
      "nome": "Armor",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "Armor",
      "registro_catalogo": true,
      "resumo_catalogo": true
    }
  ],
  "pptrs_nao_nulos": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545467
      },
      "chave": "resources.assets:2545467",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Scroll of Monster Summoning"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545467
      },
      "chave": "resources.assets:2545467",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Scroll of Monster Summoning"
    },
    {
      "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545432
      },
      "chave": "resources.assets:2545432",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Elixir of the Scarlet Ox"
    },
    {
      "campo": "$.opcoes[1].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545432
      },
      "chave": "resources.assets:2545432",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Elixir of the Scarlet Ox"
    },
    {
      "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545470
      },
      "chave": "resources.assets:2545470",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Silver Signet"
    },
    {
      "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544501
      },
      "chave": "resources.assets:2544501",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "AdditionalWeaponDamage"
    },
    {
      "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[1].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544401
      },
      "chave": "resources.assets:2544401",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "Armor"
    },
    {
      "campo": "$.opcoes[2].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545470
      },
      "chave": "resources.assets:2545470",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Silver Signet"
    },
    {
      "campo": "$.opcoes[2].recompensas[0].padrao[0].status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544501
      },
      "chave": "resources.assets:2544501",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "AdditionalWeaponDamage"
    },
    {
      "campo": "$.opcoes[2].recompensas[0].padrao[0].status.candidatos[0].modificadores[1].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544401
      },
      "chave": "resources.assets:2544401",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "Armor"
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
      "origem": "resources.assets:2545755",
      "campo": "$.opcoes[0].efeitos[0].batalha.override.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545755",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[0].eventActions[0].battleOverrideInfo.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[225]"
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
    "targetType": 0,
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
          "texto": "As you unroll it, an image of a hulking beast claws itself into existence, so realistic that it seems as if it could burst from the parchment at any moment. It snarls, snapping its jaws and swiping with lethal-looking claws.",
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
                      "chave": "resources.assets:2545467",
                      "nome": "Scroll of Monster Summoning",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545467
                      },
                      "tipo": "EventStatus",
                      "descricao": "Summons a random @level@ {1,30} Monster to fight for you.\n\n<i><color=#808080>\"Something on this list has to be useful...\"</i></color>",
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
          "texto": "The potion glows with a fiery hue, illuminating the shadows of your face. Drinking it in the heat of battle would metaphorically bestow upon you wings.",
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
                      "chave": "resources.assets:2545432",
                      "nome": "Elixir of the Scarlet Ox",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545432
                      },
                      "tipo": "EventStatus",
                      "descricao": "Grants Elixir of the Scarlet Ox: Grants 1 additional Action Point and 3 Movement Points. Applies Exhaustion. 1 charge.\n\n<i><color=#808080>\"Bestows upon you wings.  Metaphorically of course.\"</color></i>\n",
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
          "texto": "The moment you touch the ring, you hear the distant clashing of steel, as if phantom warriors were locked in eternal battle. It is a haunting sound, echoing from another time and place. The ring is likely tied to a lineage of warriors, perhaps a token of battle or symbol of honor.",
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
                      "chave": "resources.assets:2545470",
                      "nome": "Silver Signet",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545470
                      },
                      "tipo": "EventStatus",
                      "descricao": "Grants {8,200} Armor. 1% of your Armor is added as Additional Weapon Damage.\n\n<i><color=#808080>\"Be both the storm and the mountain, in war's tumultuous dance,\nBlend the fury of offense, with defense's steadfast stance.\"</i></color>\n\n",
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
                            "chave": "resources.assets:2544501",
                            "nome": "AdditionalWeaponDamage",
                            "pptr": {
                              "m_FileID": 0,
                              "m_PathID": 2544501
                            },
                            "tipo": "CharacterAttribute"
                          },
                          "metodo": {
                            "valor": 0,
                            "nome": "Base"
                          },
                          "expressao": "Source[\"Armor\"] * {.01f, .01f}",
                          "segunda_passagem": false
                        },
                        {
                          "atributo": {
                            "chave": "resources.assets:2544401",
                            "nome": "Armor",
                            "pptr": {
                              "m_FileID": 0,
                              "m_PathID": 2544401
                            },
                            "tipo": "CharacterAttribute"
                          },
                          "metodo": {
                            "valor": 0,
                            "nome": "Base"
                          },
                          "expressao": "{8, 200}",
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



## 31. Ogre Debt Collector — resources.assets:2545657

Chave: `resources.assets:2545657`. GUID real: `efff6400-391a-4158-9248-07d98b39db76`. Asset: `Ogre Debt Collector Battle Failure`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 1; ações: 1; overrides: 0. Origem: `events/ogre debt collector battle failure`.

VEREDITO PROPOSTO: MANTER — natureza: wording/recompensa/condicao. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

O desfecho de derrota já comunica a consequência por placeholders. Mantê-los evita fixar nomes ou valores que o runtime deve preencher.

### Texto atual → proposta exata

MANTER todos os campos textuais; nenhuma substituição proposta.

### Todos os textos atuais e decisão por campo

`texto` — MANTER:
```json
"You were defeated by the Ogre!\n\nHe and his minions left you [o1a1_status] and [o1a1_status2]."
```

`texto_resultados_possiveis` — MANTER:
```json
""
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
"Leave"
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

- Preservar [o1a1_status] e [o1a1_status2] literalmente. Há dois candidatos Battered (2545489) e Bruised (2545490); isso não autoriza substituir os tokens por nomes nesta proposta.

- Descrição da opção Leave e texto da ação estão vazios: sinalizar e manter, pois a narrativa já apresenta o desfecho; não inventar efeitos adicionais.

- `disabled=0` é configuração; disponibilidade efetiva NAO_EXERCITADO. Nenhuma remoção/reativação proposta.

- Textos vazios auditados: 4. Campos: `texto_resultados_possiveis`, `opcoes/0/texto`, `opcoes/0/rolagem/texto_misterioso`, `opcoes/0/efeitos/0/texto`.

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
      "chave": "resources.assets:2545489",
      "nome": "Battered",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Battered",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544401",
      "nome": "Armor",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "Armor",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[1].atributo",
      "chave": "resources.assets:2544430",
      "nome": "MagicArmor",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "MagicArmor",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[1]",
      "chave": "resources.assets:2545490",
      "nome": "Bruised",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Bruised",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[1].modificadores[0].atributo",
      "chave": "resources.assets:2544436",
      "nome": "MaxHealth",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "MaxHealth",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545489",
      "nome": "Battered",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Battered",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544401",
      "nome": "Armor",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "Armor",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].modificadores[1].atributo",
      "chave": "resources.assets:2544430",
      "nome": "MagicArmor",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "MagicArmor",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[1]",
      "chave": "resources.assets:2545490",
      "nome": "Bruised",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Bruised",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[1].modificadores[0].atributo",
      "chave": "resources.assets:2544436",
      "nome": "MaxHealth",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "MaxHealth",
      "registro_catalogo": true,
      "resumo_catalogo": true
    }
  ],
  "pptrs_nao_nulos": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545489
      },
      "chave": "resources.assets:2545489",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Battered"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544401
      },
      "chave": "resources.assets:2544401",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "Armor"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[1].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544430
      },
      "chave": "resources.assets:2544430",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "MagicArmor"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[1].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545490
      },
      "chave": "resources.assets:2545490",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Bruised"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[1].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544436
      },
      "chave": "resources.assets:2544436",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "MaxHealth"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545489
      },
      "chave": "resources.assets:2545489",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Battered"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544401
      },
      "chave": "resources.assets:2544401",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "Armor"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].modificadores[1].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544430
      },
      "chave": "resources.assets:2544430",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "MagicArmor"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[1].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545490
      },
      "chave": "resources.assets:2545490",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Bruised"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[1].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544436
      },
      "chave": "resources.assets:2544436",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "MaxHealth"
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
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2544649",
      "tipo": "BattleInfo",
      "campo": "$.failureEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[127]"
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
    "targetType": 3,
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
                      "chave": "resources.assets:2545489",
                      "nome": "Battered",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545489
                      },
                      "tipo": "EventStatus",
                      "descricao": "Reduces @Armor@ and @Magic Armor@ by @25%@ per stack.",
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
                            "chave": "resources.assets:2544401",
                            "nome": "Armor",
                            "pptr": {
                              "m_FileID": 0,
                              "m_PathID": 2544401
                            },
                            "tipo": "CharacterAttribute"
                          },
                          "metodo": {
                            "valor": 1,
                            "nome": "Percentage"
                          },
                          "expressao": "-25",
                          "segunda_passagem": false
                        },
                        {
                          "atributo": {
                            "chave": "resources.assets:2544430",
                            "nome": "MagicArmor",
                            "pptr": {
                              "m_FileID": 0,
                              "m_PathID": 2544430
                            },
                            "tipo": "CharacterAttribute"
                          },
                          "metodo": {
                            "valor": 1,
                            "nome": "Percentage"
                          },
                          "expressao": "-25",
                          "segunda_passagem": false
                        }
                      ]
                    },
                    {
                      "chave": "resources.assets:2545490",
                      "nome": "Bruised",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545490
                      },
                      "tipo": "EventStatus",
                      "descricao": "Reduces @Max Health@ by @10%@ per stack.",
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
                            "chave": "resources.assets:2544436",
                            "nome": "MaxHealth",
                            "pptr": {
                              "m_FileID": 0,
                              "m_PathID": 2544436
                            },
                            "tipo": "CharacterAttribute"
                          },
                          "metodo": {
                            "valor": 1,
                            "nome": "Percentage"
                          },
                          "expressao": "-10",
                          "segunda_passagem": true
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



## 32. Ogre Debt Collector — resources.assets:2545658

Chave: `resources.assets:2545658`. GUID real: `59467858-3651-4088-829c-b2c0abb5d316`. Asset: `Ogre Debt Collector Battle Victory`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 1; ações: 1; overrides: 0. Origem: `events/ogre debt collector battle victory`.

VEREDITO PROPOSTO: MANTER — natureza: wording/recompensa/condicao. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

O desfecho de vitória e a opção Loot descrevem claramente a recuperação do tesouro. Não há base offline para alterar o valor econômico.

### Texto atual → proposta exata

MANTER todos os campos textuais; nenhuma substituição proposta.

### Todos os textos atuais e decisão por campo

`texto` — MANTER:
```json
"With a bellow of pain and surprise, the ogre staggers back, his eyes wide. He clutches at his wounds, and then his knees buckle. With a ground-shaking thud, he crashes to the earth."
```

`texto_resultados_possiveis` — MANTER:
```json
""
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
"Loot"
```

`opcoes/0/texto` — MANTER:
```json
"Reclaim the treasure that <orange><b><incr>Krothug</incr></b></orange> had stolen."
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

- Ouro dar=true, razão=6.0; quantidade_final=NULL com motivo dependente de nível/multiplicador. Não converter razão em quantidade absoluta.

- Texto da ação vazio: manter; não adicionar quantidade ou confirmação que dependa de runtime. Esta chave é a vitória, distinta da derrota 2545657.

- `disabled=0` é configuração; disponibilidade efetiva NAO_EXERCITADO. Nenhuma remoção/reativação proposta.

- Textos vazios auditados: 3. Campos: `texto_resultados_possiveis`, `opcoes/0/rolagem/texto_misterioso`, `opcoes/0/efeitos/0/texto`.

- NULL preservados: 13; motivos por caminho no anexo de auditoria `EV-R2-FORAPOOL-b02-parte05.md`. Inclui projeção redundante de recompensa: não somar como efeitos extras.

- Referências nulas projetadas: 2. Combate/RNG/quantidade final/status aplicado/UI: NAO_EXERCITADO — somente configuração offline disponível.

- Opção 1: ocultar sem requisitos=false; ocultar por status=[]; hideOptionEffectText=0. Exibição real NAO_EXERCITADO.

### Referências consultadas e encadeamentos de entrada

Configurações de candidato não são concessões executadas. Catálogo consultado por chave, sem expandir/editar as definições externas.
```json
{
  "referencias": [],
  "pptrs_nao_nulos": [],
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
      "origem": "resources.assets:2545659",
      "campo": "$.opcoes[1].efeitos[0].batalha.override.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2544649",
      "tipo": "BattleInfo",
      "campo": "$.victoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545659",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[1].eventActions[0].battleOverrideInfo.VictoryEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[128]"
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
                  "dar": true,
                  "retirar": false,
                  "razao": 6.0,
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



## 33. Party like a Pirate — resources.assets:2545661

Chave: `resources.assets:2545661`. GUID real: `fd31de51-fdde-4e83-a6c9-344c4ed2bfd0`. Asset: `Party like a Pirate 1`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 2; ações: 2; overrides: 0. Origem: `events/party like a pirate 1`.

VEREDITO PROPOSTO: MELHORAR — natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

Eliminar contradição entre os gritos imaginários que cessam e a risada que cresce logo após, mantendo o abandono da sequência.

### Texto atual → proposta exata

Campo: `opcoes/1/efeitos/0/texto`.

Atual (campo completo):
```json
"\"No... No more,\" you mutter, struggling to keep your voice steady. The spectral cheers in your mind falter, replaced by a surprised murmur. Your body feels heavy and your senses dull, but the ethereal laughter of the skeletal crew is louder than ever, as you stumble away."
```

PROPOSTA EXATA (campo completo):
```json
"\"No... No more,\" you mutter, struggling to keep your voice steady. The spectral cheers in your mind falter, replaced by a surprised murmur. Your body feels heavy and your senses dull, and the ethereal laughter of the skeletal crew fades as you stumble away."
```

Justificativa: Eliminar contradição entre os gritos imaginários que cessam e a risada que cresce logo após, mantendo o abandono da sequência.

### Todos os textos atuais e decisão por campo

`texto` — MANTER:
```json
"The air is heavy with the scent of aged liquor and salty sea breezes, as the tap continues to flow. There is a perverse joy about the place, a carefree abandon that draws you in. "
```

`texto_resultados_possiveis` — MANTER:
```json
""
```

`campos_originais/promptToSelectCharacter` — MANTER:
```json
"Who will listen to his pleas?"
```

`campos_originais/characterSelectedText` — MANTER:
```json
""
```

`opcoes/0/titulo` — MANTER:
```json
"Sip"
```

`opcoes/0/texto` — MANTER:
```json
"Bottoms up."
```

`opcoes/1/titulo` — MANTER:
```json
"Leave"
```

`opcoes/1/texto` — MANTER:
```json
"You've had enough."
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
"Your second swig finds you less resistant. Your head spins more, and you can almost hear the raucous laughter of the pirates growing louder. You sway, mimicking their endless party. "
```

`opcoes/1/efeitos/0/texto` — MELHORAR conforme proposta acima:
```json
"\"No... No more,\" you mutter, struggling to keep your voice steady. The spectral cheers in your mind falter, replaced by a surprised murmur. Your body feels heavy and your senses dull, but the ethereal laughter of the skeletal crew is louder than ever, as you stumble away."
```

### Anomalias, cautelas e limites

- Sip encadeia para 2545662; percentMaxHealth=-10.0 e candidato Confused (2545491) permanecem. Não interpretar -10.0 como redução permanente do atributo Max Health sem runtime.

- Leave não configura retirada dos status já recebidos. Não propor nem prometer recuperação/cura ao sair.

- `disabled=0` é configuração; disponibilidade efetiva NAO_EXERCITADO. Nenhuma remoção/reativação proposta.

- Textos vazios auditados: 4. Campos: `texto_resultados_possiveis`, `campos_originais/characterSelectedText`, `opcoes/0/rolagem/texto_misterioso`, `opcoes/1/rolagem/texto_misterioso`.

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
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0]",
      "chave": "resources.assets:2545491",
      "nome": "Confused",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Confused",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544451",
      "nome": "IntelligenceBase",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "IntelligenceBase",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].efeitos[0].evento_encadeado",
      "chave": "resources.assets:2545662",
      "nome": "Party like a Pirate 2",
      "tipo_catalogo": "PartyEvent",
      "nome_asset_catalogo": "Party like a Pirate 2",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545491",
      "nome": "Confused",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Confused",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544451",
      "nome": "IntelligenceBase",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "IntelligenceBase",
      "registro_catalogo": true,
      "resumo_catalogo": true
    }
  ],
  "pptrs_nao_nulos": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545491
      },
      "chave": "resources.assets:2545491",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Confused"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544451
      },
      "chave": "resources.assets:2544451",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "IntelligenceBase"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].evento_encadeado.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545662
      },
      "chave": "resources.assets:2545662",
      "tipo_catalogo": "PartyEvent",
      "nome_catalogo": "Party like a Pirate 2"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545491
      },
      "chave": "resources.assets:2545491",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Confused"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544451
      },
      "chave": "resources.assets:2544451",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "IntelligenceBase"
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
      "origem": "resources.assets:2545664",
      "campo": "$.opcoes[0].efeitos[0].evento_encadeado.pptr"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545664",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[0].eventActions[0].chainedEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[131]"
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
          "texto": "Your second swig finds you less resistant. Your head spins more, and you can almost hear the raucous laughter of the pirates growing louder. You sway, mimicking their endless party. ",
          "resultado": {
            "valor": 0,
            "nome": "Success"
          },
          "limite_rolagem": 0,
          "texto_efeitos_manual": [],
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
                      "chave": "resources.assets:2545491",
                      "nome": "Confused",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545491
                      },
                      "tipo": "EventStatus",
                      "descricao": "Reduces @Intelligence@ by @20%@ per stack.",
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
                            "chave": "resources.assets:2544451",
                            "nome": "IntelligenceBase",
                            "pptr": {
                              "m_FileID": 0,
                              "m_PathID": 2544451
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
            "chave": "resources.assets:2545662",
            "nome": "Party like a Pirate 2",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545662
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
          "texto": "\"No... No more,\" you mutter, struggling to keep your voice steady. The spectral cheers in your mind falter, replaced by a surprised murmur. Your body feels heavy and your senses dull, but the ethereal laughter of the skeletal crew is louder than ever, as you stumble away.",
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



## 34. Party like a Pirate — resources.assets:2545662

Chave: `resources.assets:2545662`. GUID real: `e9d21980-ff00-4c6d-b3dc-ef1040133f97`. Asset: `Party like a Pirate 2`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 2; ações: 2; overrides: 0. Origem: `events/party like a pirate 2`.

VEREDITO PROPOSTO: MELHORAR — natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

Mesma contradição textual da fase anterior; alinhar o trecho compartilhado sem unificar as chaves e seus efeitos.

### Texto atual → proposta exata

Campo: `opcoes/1/efeitos/0/texto`.

Atual (campo completo):
```json
"\"No... No more,\" you mutter, struggling to keep your voice steady. The spectral cheers in your mind falter, replaced by a surprised murmur. Your body feels heavy and your senses dull, but the ethereal laughter of the skeletal crew is louder than ever, as you stumble away."
```

PROPOSTA EXATA (campo completo):
```json
"\"No... No more,\" you mutter, struggling to keep your voice steady. The spectral cheers in your mind falter, replaced by a surprised murmur. Your body feels heavy and your senses dull, and the ethereal laughter of the skeletal crew fades as you stumble away."
```

Justificativa: Mesma contradição textual da fase anterior; alinhar o trecho compartilhado sem unificar as chaves e seus efeitos.

### Todos os textos atuais e decisão por campo

`texto` — MANTER:
```json
"Imaginary roars and hoots of approval fill your ears. You square your shoulders and raise a cup to the absent eyes of the skeletal pirates. \"To the captain and his men,\" you say, nodding to each of the grinning skulls, \"may your spirits forever sail on seas of joy.\""
```

`texto_resultados_possiveis` — MANTER:
```json
""
```

`campos_originais/promptToSelectCharacter` — MANTER:
```json
"Who will listen to his pleas?"
```

`campos_originais/characterSelectedText` — MANTER:
```json
""
```

`opcoes/0/titulo` — MANTER:
```json
"Sip"
```

`opcoes/0/texto` — MANTER:
```json
"Bottoms up."
```

`opcoes/1/titulo` — MANTER:
```json
"Leave"
```

`opcoes/1/texto` — MANTER:
```json
"You've had enough."
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
"The rum is strong, too strong. It burns your throat with each swig, sending shivers down your spine, igniting a fire in your belly. Your world is a top, spinning and dancing like the ghostly pirates you imagine around you."
```

`opcoes/1/efeitos/0/texto` — MELHORAR conforme proposta acima:
```json
"\"No... No more,\" you mutter, struggling to keep your voice steady. The spectral cheers in your mind falter, replaced by a surprised murmur. Your body feels heavy and your senses dull, but the ethereal laughter of the skeletal crew is louder than ever, as you stumble away."
```

### Anomalias, cautelas e limites

- Sip encadeia para 2545663; percentMaxHealth=-10.0 e candidato Visually Impaired (2545503) permanecem, distintos da fase anterior.

- Leave não configura cura nem remoção das penalidades anteriores.

- `disabled=0` é configuração; disponibilidade efetiva NAO_EXERCITADO. Nenhuma remoção/reativação proposta.

- Textos vazios auditados: 4. Campos: `texto_resultados_possiveis`, `campos_originais/characterSelectedText`, `opcoes/0/rolagem/texto_misterioso`, `opcoes/1/rolagem/texto_misterioso`.

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
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0]",
      "chave": "resources.assets:2545503",
      "nome": "Visually Impaired",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Visually Impaired",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544493",
      "nome": "RangeTypeAdderRanged",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "RangeTypeAdderRanged",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].efeitos[0].evento_encadeado",
      "chave": "resources.assets:2545663",
      "nome": "Party like a Pirate 3",
      "tipo_catalogo": "PartyEvent",
      "nome_asset_catalogo": "Party like a Pirate 3",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545503",
      "nome": "Visually Impaired",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Visually Impaired",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].modificadores[0].atributo",
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
        "m_PathID": 2545503
      },
      "chave": "resources.assets:2545503",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Visually Impaired"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544493
      },
      "chave": "resources.assets:2544493",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "RangeTypeAdderRanged"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].evento_encadeado.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545663
      },
      "chave": "resources.assets:2545663",
      "tipo_catalogo": "PartyEvent",
      "nome_catalogo": "Party like a Pirate 3"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545503
      },
      "chave": "resources.assets:2545503",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Visually Impaired"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].modificadores[0].atributo.pptr",
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
      "origem": "resources.assets:2545661",
      "campo": "$.opcoes[0].efeitos[0].evento_encadeado.pptr"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545661",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[0].eventActions[0].chainedEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[132]"
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
          "texto": "The rum is strong, too strong. It burns your throat with each swig, sending shivers down your spine, igniting a fire in your belly. Your world is a top, spinning and dancing like the ghostly pirates you imagine around you.",
          "resultado": {
            "valor": 0,
            "nome": "Success"
          },
          "limite_rolagem": 0,
          "texto_efeitos_manual": [],
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
                      "chave": "resources.assets:2545503",
                      "nome": "Visually Impaired",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545503
                      },
                      "tipo": "EventStatus",
                      "descricao": "Reduces @Range@ by @3@ per stack.",
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
                          "expressao": "-3",
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
            "chave": "resources.assets:2545663",
            "nome": "Party like a Pirate 3",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545663
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
          "texto": "\"No... No more,\" you mutter, struggling to keep your voice steady. The spectral cheers in your mind falter, replaced by a surprised murmur. Your body feels heavy and your senses dull, but the ethereal laughter of the skeletal crew is louder than ever, as you stumble away.",
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



## 35. Party like a Pirate — resources.assets:2545663

Chave: `resources.assets:2545663`. GUID real: `20c770ea-3ca7-452d-9236-8abcaa33f2a3`. Asset: `Party like a Pirate 3`. Categoria: NotInEventPool. Raridade: Common (0). Peso relativo: 1.0. `disabled=0`. Opções: 2; ações: 2; overrides: 0. Origem: `events/party like a pirate 3`.

VEREDITO PROPOSTO: MELHORAR — natureza: wording. Recompensa: MANTER. Condição: MANTER. Aprovação do dono: PENDENTE.

Corrigir ligação de orações no quarto copo e a contradição do texto de saída; manter o final da cadeia e suas penalidades/fortuna.

### Texto atual → proposta exata

Campo: `opcoes/0/efeitos/0/texto`.

Atual (campo completo):
```json
"On your fourth cup, you slump against a barrel, your head spinning. The skeletal pirates loom around you, their eyeless sockets seem to look down on you in approval. \"You're one of us now,\" their silent mouths seem to say, and in your rum-addled brain, you laugh, raising your cup one last time."
```

PROPOSTA EXATA (campo completo):
```json
"On your fourth cup, you slump against a barrel, your head spinning. The skeletal pirates loom around you; their eyeless sockets seem to look down on you in approval. \"You're one of us now,\" their silent mouths seem to say, and in your rum-addled brain, you laugh, raising your cup one last time."
```

Justificativa: Corrigir ligação de orações no quarto copo e a contradição do texto de saída; manter o final da cadeia e suas penalidades/fortuna.

Campo: `opcoes/1/efeitos/0/texto`.

Atual (campo completo):
```json
"\"No... No more,\" you mutter, struggling to keep your voice steady. The spectral cheers in your mind falter, replaced by a surprised murmur. Your body feels heavy and your senses dull, but the ethereal laughter of the skeletal crew is louder than ever, as you stumble away."
```

PROPOSTA EXATA (campo completo):
```json
"\"No... No more,\" you mutter, struggling to keep your voice steady. The spectral cheers in your mind falter, replaced by a surprised murmur. Your body feels heavy and your senses dull, and the ethereal laughter of the skeletal crew fades as you stumble away."
```

Justificativa: Corrigir ligação de orações no quarto copo e a contradição do texto de saída; manter o final da cadeia e suas penalidades/fortuna.

### Todos os textos atuais e decisão por campo

`texto` — MANTER:
```json
"The lights dance overhead as you drink, the rum conjuring fanciful images of the skeletal pirates applauding you, their ethereal cheers echoing in your ears."
```

`texto_resultados_possiveis` — MANTER:
```json
""
```

`campos_originais/promptToSelectCharacter` — MANTER:
```json
"Who will listen to his pleas?"
```

`campos_originais/characterSelectedText` — MANTER:
```json
""
```

`opcoes/0/titulo` — MANTER:
```json
"Sip"
```

`opcoes/0/texto` — MANTER:
```json
"Bottoms up."
```

`opcoes/1/titulo` — MANTER:
```json
"Leave"
```

`opcoes/1/texto` — MANTER:
```json
"You've had enough."
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
"On your fourth cup, you slump against a barrel, your head spinning. The skeletal pirates loom around you, their eyeless sockets seem to look down on you in approval. \"You're one of us now,\" their silent mouths seem to say, and in your rum-addled brain, you laugh, raising your cup one last time."
```

`opcoes/1/efeitos/0/texto` — MELHORAR conforme proposta acima:
```json
"\"No... No more,\" you mutter, struggling to keep your voice steady. The spectral cheers in your mind falter, replaced by a surprised murmur. Your body feels heavy and your senses dull, but the ethereal laughter of the skeletal crew is louder than ever, as you stumble away."
```

### Anomalias, cautelas e limites

- Sip tem encadeamento nulo nesta fase, percentMaxHealth=-10.0 e candidatos Bruised (2545490) e Pirate's Rum (2545462). Preservar ambos; não tratar a fortuna como cancelamento automático das penalidades.

- Sair não configura remoção de status anteriores.

- `disabled=0` é configuração; disponibilidade efetiva NAO_EXERCITADO. Nenhuma remoção/reativação proposta.

- Textos vazios auditados: 4. Campos: `texto_resultados_possiveis`, `campos_originais/characterSelectedText`, `opcoes/0/rolagem/texto_misterioso`, `opcoes/1/rolagem/texto_misterioso`.

- NULL preservados: 26; motivos por caminho no anexo de auditoria `EV-R2-FORAPOOL-b02-parte05.md`. Inclui projeção redundante de recompensa: não somar como efeitos extras.

- Referências nulas projetadas: 4. Combate/RNG/quantidade final/status aplicado/UI: NAO_EXERCITADO — somente configuração offline disponível.

- Opção 1: ocultar sem requisitos=false; ocultar por status=[]; hideOptionEffectText=0. Exibição real NAO_EXERCITADO.

- Opção 2: ocultar sem requisitos=false; ocultar por status=[]; hideOptionEffectText=0. Exibição real NAO_EXERCITADO.

### Referências consultadas e encadeamentos de entrada

Configurações de candidato não são concessões executadas. Catálogo consultado por chave, sem expandir/editar as definições externas.
```json
{
  "referencias": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0]",
      "chave": "resources.assets:2545490",
      "nome": "Bruised",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Bruised",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544436",
      "nome": "MaxHealth",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "MaxHealth",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[1]",
      "chave": "resources.assets:2545462",
      "nome": "Pirate's Rum",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Pirate's Rum",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[1].modificadores[0].atributo",
      "chave": "resources.assets:2544414",
      "nome": "DamageReduction",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "DamageReduction",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0]",
      "chave": "resources.assets:2545490",
      "nome": "Bruised",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Bruised",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].modificadores[0].atributo",
      "chave": "resources.assets:2544436",
      "nome": "MaxHealth",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "MaxHealth",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[1]",
      "chave": "resources.assets:2545462",
      "nome": "Pirate's Rum",
      "tipo_catalogo": "EventStatus",
      "nome_asset_catalogo": "Pirate's Rum",
      "registro_catalogo": true,
      "resumo_catalogo": true
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[1].modificadores[0].atributo",
      "chave": "resources.assets:2544414",
      "nome": "DamageReduction",
      "tipo_catalogo": "CharacterAttribute",
      "nome_asset_catalogo": "DamageReduction",
      "registro_catalogo": true,
      "resumo_catalogo": true
    }
  ],
  "pptrs_nao_nulos": [
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545490
      },
      "chave": "resources.assets:2545490",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Bruised"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544436
      },
      "chave": "resources.assets:2544436",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "MaxHealth"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[1].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545462
      },
      "chave": "resources.assets:2545462",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Pirate's Rum"
    },
    {
      "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos[1].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544414
      },
      "chave": "resources.assets:2544414",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "DamageReduction"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545490
      },
      "chave": "resources.assets:2545490",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Bruised"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[0].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544436
      },
      "chave": "resources.assets:2544436",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "MaxHealth"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[1].pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545462
      },
      "chave": "resources.assets:2545462",
      "tipo_catalogo": "EventStatus",
      "nome_catalogo": "Pirate's Rum"
    },
    {
      "campo": "$.opcoes[0].recompensas[0].padrao[0].status.candidatos[1].modificadores[0].atributo.pptr",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544414
      },
      "chave": "resources.assets:2544414",
      "tipo_catalogo": "CharacterAttribute",
      "nome_catalogo": "DamageReduction"
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
    }
  ],
  "referencias_entrada": [
    {
      "fonte": "eventos.json",
      "origem": "resources.assets:2545662",
      "campo": "$.opcoes[0].efeitos[0].evento_encadeado.pptr"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2545662",
      "tipo": "PartyEvent",
      "campo": "$.eventOptions[0].eventActions[0].chainedEvent"
    },
    {
      "fonte": "catalogo-referencias.json",
      "origem": "resources.assets:2547145",
      "tipo": "ListHolderEvents",
      "campo": "$.Events[133]"
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
          "texto": "On your fourth cup, you slump against a barrel, your head spinning. The skeletal pirates loom around you, their eyeless sockets seem to look down on you in approval. \"You're one of us now,\" their silent mouths seem to say, and in your rum-addled brain, you laugh, raising your cup one last time.",
          "resultado": {
            "valor": 0,
            "nome": "Success"
          },
          "limite_rolagem": 0,
          "texto_efeitos_manual": [],
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
                      "chave": "resources.assets:2545490",
                      "nome": "Bruised",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545490
                      },
                      "tipo": "EventStatus",
                      "descricao": "Reduces @Max Health@ by @10%@ per stack.",
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
                            "chave": "resources.assets:2544436",
                            "nome": "MaxHealth",
                            "pptr": {
                              "m_FileID": 0,
                              "m_PathID": 2544436
                            },
                            "tipo": "CharacterAttribute"
                          },
                          "metodo": {
                            "valor": 1,
                            "nome": "Percentage"
                          },
                          "expressao": "-10",
                          "segunda_passagem": true
                        }
                      ]
                    },
                    {
                      "chave": "resources.assets:2545462",
                      "nome": "Pirate's Rum",
                      "pptr": {
                        "m_FileID": 0,
                        "m_PathID": 2545462
                      },
                      "tipo": "EventStatus",
                      "descricao": "Increases @Damage Reduction@ by {5,20}%.\n\n<i><color=#808080>Numbs everything, including pain!</i></color>\n",
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
                            "chave": "resources.assets:2544414",
                            "nome": "DamageReduction",
                            "pptr": {
                              "m_FileID": 0,
                              "m_PathID": 2544414
                            },
                            "tipo": "CharacterAttribute"
                          },
                          "metodo": {
                            "valor": 0,
                            "nome": "Base"
                          },
                          "expressao": "{5,20}",
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
          "texto": "\"No... No more,\" you mutter, struggling to keep your voice steady. The spectral cheers in your mind falter, replaced by a surprised murmur. Your body feels heavy and your senses dull, but the ethereal laughter of the skeletal crew is louder than ever, as you stumble away.",
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


