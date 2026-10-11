## Heavy Safe
Chave: `resources.assets:2545604` — GUID: `9b45cc6c-33cb-4936-acc7-76140acef17f`
Categoria: Normal — raridade: Common (0) — peso relativo: 1.0
Origem: events/heavy safe — SHA objeto: `848015627b3cfaf0c5cdea5144437fc249f23bd796a7487927c1ddda3882d78f`

### Texto original
You stand around a <b><gold><incr>Hulking Safe</incr></gold></b>, its matte black exterior reflecting the dim torchlight. The solid steel structure is an intimidating sight, its austere facade is marked only by a complex locking mechanism, a series of concentric rings each adorned with cryptic symbols and numbers.


No visible latch, no obvious keyhole. Just this unyielding enigma waiting to be solved. An opportunity for immense wealth, shrouded in an armor of cold, hardened steel.

### Resultados possíveis (texto autoral)
(string vazia no asset)

### Condições e modos
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
    "allowAtAllLevels": 0,
    "minLevel": 4,
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
  }
}
```

### Opção 1: Attempt
Try and crack the safe.

Condições/rolagem:
```json
{
  "condicoes": {
    "status_requeridos": [],
    "ocultar_sem_requisitos": false,
    "ocultar_se_status": []
  },
  "rolagem": {
    "bonus": [
      {
        "valor": 1,
        "nome": "Dexterity"
      }
    ],
    "misteriosa": true,
    "texto_misterioso": ""
  }
}
```

#### Ação 1: Success — RollLimit 14
[name] gently rests [his] hands on the cold, unyielding metal, [his] fingers tracing the numbers on the dial. [his] ear presses against the steel surface, [he] begins to turn the dial slowly, listening for the subtle clicks and shifts that would guide [him].


The soft scrape of metal against metal echoed, a symphony of patience and precision. [name]'s focus was unyielding, his gaze locked onto the task at hand. And then, after what seemed like hours in the suffocating silence, there came a distinct click, different from the rest. [he] pauses, then gently turns the handle. The door of the safe swings open with a reluctant creak.

Efeito 1 (configuração autoral, não resultado de partida):
```json
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
      "dar": true,
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
      "dar": true,
      "pool_tipo": {
        "valor": 2,
        "nome": "Unassigned"
      },
      "quantidade_configurada": 1,
      "tabelas": [
        {
          "mustGetOne": 0,
          "itemLootChances": []
        }
      ],
      "restricoes": {
        "limitItemTypes": 0,
        "possibleItemTypes": [],
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
```

#### Ação 2: Failure — RollLimit 1
Slowly, [name]'s hands begin their dance around the dial, [his] ears listening for the subtlest of sounds. Minutes pass, stretching into tense hours, as [he] remains locked in a silent battle with the obstinate vault.


But despite [his] skill, the safe remains unyielding. No comforting click, no gratifying shift of mechanisms echos from within its steel walls. Each combination attempted only meets the same, disheartening silence. The dial spins, numbers blurring and dancing in [his] vision, but the safe offers no encouragement, no indication of progress.

Efeito 1 (configuração autoral, não resultado de partida):
```json
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
        },
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
```

### Opção 2: Leave
You simply do not have the time to linger here for hours attempting to crack the safe.

Condições/rolagem:
```json
{
  "condicoes": {
    "status_requeridos": [],
    "ocultar_sem_requisitos": false,
    "ocultar_se_status": []
  },
  "rolagem": {
    "bonus": [],
    "misteriosa": false,
    "texto_misterioso": ""
  }
}
```

#### Ação 1: Success — RollLimit 0
There is a quiet regret as you turn away, a mourning for the treasure left behind. The allure of the unopened safe is a siren's call you are forced to ignore, an opportunity lost to the pressing weight of time.

Efeito 1 (configuração autoral, não resultado de partida):
```json
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
```


---

