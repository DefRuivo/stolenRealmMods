# EV-R1 — NotInEventPool (84 eventos)

## Admiral Blackbeard
Chave: `resources.assets:2545637` — GUID: `f5475aa4-e4e2-4449-a392-0a4f7948315f`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/5 - admiral blackbeard end — SHA objeto: `28d002141ad1475cfb829abc90e4cccc3ee01493178fe3b72e1ed3e5d9af42dd`

### Texto original
Shadowy chains, manifestations of the curse that had consumed Blackbeard's soul, emerge from the abyss, reaching for the fallen pirate. With an inexorable grip, they pull him down into the unfathomable depths of darkness, an abyss where greed and power has led him. 

A soft glow emanates from the spot where Blackbeard had vanished. There, lying amidst the ancient stones of the temple, is a brilliant gold coin, radiant and untouched by the darkness that had just been vanquished.

Tentatively, you reach out and touch the coin, its surface cool and smooth under your fingers.
<br/>
You are carried aboard a ship, the deck alive with the sounds of the sea – the creaking of wood, the cry of gulls, and the rush of the wind. Here, amidst the salt and spray, sits a young Blackbeard, his face unmarked by the years of hardship and cruelty that would later define him. His hair is tousled by the sea breeze, and his eyes sparkle with the untamed spirit of adventure.

The young Blackbeard is laughing heartily, surrounded by his shipmates, as they engage in a game of chance. The atmosphere is light and jovial, filled with the camaraderie of men and women who share a love for the sea and the thrill of adventure. They are brothers in arms, united by the bonds forged in the vast and unpredictable embrace of the ocean.
<br/>
Your mind is awash with questions, a torrent as tumultuous as the sea that surrounds the ruins. The memories unveiled by these magical artifacts paints pictures of lives that had once been, lives of men before they were consumed by the shadows of their desires. You can't help but ponder the enigma your father is unraveling, a mystery that intertwines the fates of these men with the ancient and mysterious defeat of the dragons.

The journal now points towards a new destination – the frosty peaks of Frostwrought Mountain.

### Resultados possíveis (texto autoral)
(string vazia no asset)

### Condições e modos
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
  }
}
```


---

## Bonefire
Chave: `resources.assets:2545545` — GUID: `05935caa-5cfd-411e-8ab8-92d6d0bc9018`
Categoria: NotInEventPool — raridade: Uncommon (1) — peso relativo: 1.0
Origem: events/bonefire (roguelike) - victory — SHA objeto: `1331c529795e7f55906fef7966172805d690ca81a0c01f88a758cc702dc2eeba`

### Texto original
Despite your growing fatigue, you fight with relentless determination. Shattering bone after bone, extinguishing the eerie light in the skeletons' hollow eye sockets.

With a final, resounding crack, the last skeleton falls, and the bonfire's flames abruptly extinguish, plunging the area into darkness. Weary but victorious, you stand panting in the sudden silence, your breath fogging in the cold air.

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
      2
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

### Opção 1: Rest
Sit by the fire and recover your strength.

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
(string vazia no asset)

Efeito 1 (configuração autoral, não resultado de partida):
```json
{
  "vida_mana": {
    "percentMaxHealth": 50.0,
    "percentMaxMana": 50.0,
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

### Opção 2: Reroll Skill
(string vazia no asset)

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
You've rerolled a skill!

### Opção 3: Level Up Fortunes
(string vazia no asset)

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
Your Fortunes have been leveled up!


---

## Bonefire
Chave: `resources.assets:2545547` — GUID: `6b8e0706-2a01-49f2-916a-9dccad57f73b`
Categoria: NotInEventPool — raridade: Rare (2) — peso relativo: 1.0
Origem: events/bonefire - victory — SHA objeto: `f821c79eaab003478b4274e073ec95ee9e1a813a6a2d919c67d56315c244a546`

### Texto original
Despite your growing fatigue, you fight with relentless determination. Shattering bone after bone, extinguishing the eerie light in the skeletons' hollow eye sockets.

With a final, resounding crack, the last skeleton falls, and the bonfire's flames abruptly extinguish, plunging the area into darkness. Weary but victorious, you stand panting in the sudden silence, your breath fogging in the cold air.

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
    "allowAtAllTimesOfDay": 0,
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
    "LeadsToFortune": 0
  },
  "modos": [
    {
      "valor": 0,
      "nome": "Campaign"
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

### Opção 1: Rest
Sit and recover your strength.

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
(string vazia no asset)

Efeito 1 (configuração autoral, não resultado de partida):
```json
{
  "vida_mana": {
    "percentMaxHealth": 50.0,
    "percentMaxMana": 50.0,
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

### Opção 2: Prepare
Take time to prepare for what's ahead.

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
(string vazia no asset)

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
          "chave": "resources.assets:2545391",
          "nome": "Prepared",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545391
          },
          "tipo": "EventStatus",
          "descricao": "Item and gold drops are increased by 20%.",
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
                "chave": "resources.assets:2544419",
                "nome": "DropQuantityMod",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544419
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "20",
              "segunda_passagem": false
            },
            {
              "atributo": {
                "chave": "resources.assets:2544424",
                "nome": "GoldMod",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544424
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "20",
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


---

## Challenger's Gong
Chave: `resources.assets:2545557` — GUID: `8acc5e69-2a57-46db-87f5-5ee7de130916`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/challenger's gong - victory 1 — SHA objeto: `fff60d788c1e468a81fafbff2a7f490fc5fc022412bba82f9ad60d9ebd938dce`

### Texto original
Waves of challengers continue to emerge, their weapons glinting in the pale winter light. Warriors from different lands, armed with their prowess and honed skills, converge upon the gong to prove their worth.

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
  }
}
```

### Opção 1: Fight
You must continue to fight on.

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
(string vazia no asset)

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

Combate configurado:
```json
{
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
        "NameOverride": "Master Leo",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545132
        },
        "ForcedEnemyMods": [],
        "IsSuperUnique": 1
      },
      {
        "OverrideEnemyName": 1,
        "NameOverride": "Master Donnie",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545129
        },
        "ForcedEnemyMods": [],
        "IsSuperUnique": 1
      },
      {
        "OverrideEnemyName": 1,
        "NameOverride": "Master Mikey",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545133
        },
        "ForcedEnemyMods": [],
        "IsSuperUnique": 1
      },
      {
        "OverrideEnemyName": 1,
        "NameOverride": "Master Raph",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545134
        },
        "ForcedEnemyMods": [],
        "IsSuperUnique": 1
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
      "m_PathID": 2545558
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
}
```

---

## Challenger's Gong
Chave: `resources.assets:2545558` — GUID: `ae1bb381-411b-4ed0-b1fb-1a3c06dc8559`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/challenger's gong - victory 2 — SHA objeto: `9b6781c561e3e9da8876fd4eba889ab20cb68a2daf31658209a1a395c763afb8`

### Texto original
Battles erupte, their clash echoing through the mountain passes, as heroes meet in a whirlwind of steel and fury. But it is <orange><b><incr>Ronin</incr></b></orange>, a warrior of renowned skill and indomitable spirit, who emerges as the final challenger to the gong's call. His reputation precedes him, and tales of his valor have spread like wildfire throughout the Stolen Realm. He stands tall, his eyes ablaze with determination, as he steps forth to claim the honor of facing the gong's ultimate trial.

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
  }
}
```

### Opção 1: Fight
Confront <orange><b><incr>Ronin</incr></b></orange>.

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
(string vazia no asset)

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

Combate configurado:
```json
{
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
          "m_PathID": 2545135
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
      "m_PathID": 2545559
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
}
```

---

## Challenger's Gong
Chave: `resources.assets:2545559` — GUID: `18894a29-845e-4a2f-a58e-504da8a0aad2`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/challenger's gong - victory 3 — SHA objeto: `894de76b1c6fa0a5768cf8f3324444d9d407b7d5a7adfa21794cb3dc10c4b754`

### Texto original
At last, the final foe falls. <orange><b><incr>Ronin</incr></b></orange>, a being of malice and iron, brought a test to your very soul. As the last echoes of the battle subside, the great golden gong falls silent, its purpose fulfilled. The challengers, both defeated and triumphant, vanish, leaving only the memories of their valor behind. You stand alone amidst the stillness of the snow-capped mountains, your victory an indelible mark upon your journey.

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
  }
}
```

### Opção 1: Reward
You bear the honor of victory.

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
(string vazia no asset)

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
```


---

## Consumed by Rage
Chave: `resources.assets:2545649` — GUID: `bb2ea4ea-f11f-4bb1-9812-0623428ffe12`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/master of rage - 1 — SHA objeto: `99740da7d657aa0afa63a90d121eab8b4673e9bfcf536f5e6a2791bd2081cfee`

### Texto original
As you reach the arid mountain pass, a harsh wind cuts through your cloak and chills you to the bone. Your breath fogs in the cold air, as you trudge through the rough terrain, the fresh snow crunching beneath your boots.


Then, a low howl echoes through the mountain, sending a jolt of fear through your heart. Eyes glowing with a ghastly blue light emerge from beyond the pass, followed by monstrous forms taking shape.


Wendigos, beings of nightmare and rage. Each bares horns sprouting from their skulls, bodies lean and drawn out to the point of emaciation, their hideous forms resembling humanoid stags.


Savage snarls fill the mountain as the wendigos advance, their claws leaving gouges in the frozen ground. 

### Resultados possíveis (texto autoral)
What will you do?

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
  }
}
```

### Opção 1: Fight
Slay the Wendigo.

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
The Wendigos charge with a chilling cry, their gangly forms a horrifying silhouette against the snow. Their movements are unhindered by the biting cold, propelled forward by an insatiable hunger and unbridled rage.

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

Combate configurado:
```json
{
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
          "m_PathID": 2545299
        },
        "ForcedEnemyMods": [],
        "IsSuperUnique": 0
      },
      {
        "OverrideEnemyName": 0,
        "NameOverride": "",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545299
        },
        "ForcedEnemyMods": [],
        "IsSuperUnique": 0
      },
      {
        "OverrideEnemyName": 0,
        "NameOverride": "",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545299
        },
        "ForcedEnemyMods": [],
        "IsSuperUnique": 0
      },
      {
        "OverrideEnemyName": 0,
        "NameOverride": "",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545299
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
      "m_PathID": 2545650
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
}
```
### Opção 2: Leave
No amount of anger can convince you to stay.

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
The moment you see the wendigo, you falter. Courage and determination bleeds away, replaced by the primal instinct of survival. You turn on your heels, casting aside your plans of attack. 

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
          "chave": "resources.assets:2545494",
          "nome": "Enfeebled",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545494
          },
          "tipo": "EventStatus",
          "descricao": "Reduces @Damage@ by @20%@ per stack.",
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
                "chave": "resources.assets:2544373",
                "nome": "DamageMod",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544373
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
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
```


---

## Cursed Chest
Chave: `resources.assets:2545561` — GUID: `29e3b6c4-59da-42f0-8622-5b4667ce8c68`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/cursed chest battle victory — SHA objeto: `ba6aafb6b599cf9273241fc6543d993709abf695cafdcde03114312cc0b6502c`

### Texto original
At last, the undead are vanquished, their twisted forms returning to the earth.

The <indigo><b><incr>Cursed Chest</incr></b></indigo>, now free from its macabre prison of decay, lays before you. With caution and a mingling sense of anticipation, you open the chest, revealing its hidden treasure. 

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
  }
}
```

### Opção 1: Claim your reward!
(string vazia no asset)

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
(string vazia no asset)

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
      "dar": true,
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
          0
        ],
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

## Cursed Mimic
Chave: `resources.assets:2545564` — GUID: `a0c631c5-b0b7-4956-97c5-2440b1a84d19`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/cursed mimic chest victory — SHA objeto: `e158350bf11deadf5f15c3c351c5aea8de1becdf793f0dde392e4f8b57304739`

### Texto original
The mimic shrinks back, until, finally, it gives a last gurgling growl in defeat. The taint dissolved, fading away into smoke and shadow, leaving behind an empty silence.

As the darkness vanishes, it reveals a small mound of treasure in its wake.

### Resultados possíveis (texto autoral)
What treasure will you take?

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
  }
}
```

### Opção 1: Emblem of the Iron Fortress
The emblem is a miniature fortress shield wrought in iron, its fine details shimmering with an inner light that seems to defy the darkness around you. 

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
Holding it, you can feel a sensation of resolute protection, as if you were clad in impenetrable armor.

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
          "chave": "resources.assets:2545433",
          "nome": "Emblem of the Iron Fortress",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545433
          },
          "tipo": "EventStatus",
          "descricao": "Grants {10,250} Armor. 3% of your Armor is added as physical damage return.\n\n<i><color=#808080>The Iron Fortress, an indomitable monolith of enduring strength, stood resolute and unyielding for hundreds of years, its towering parapets and impenetrable defenses the silent testament to countless civilizations that had crumbled in their futile attempts to conquer it.</color></i>",
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
                "chave": "resources.assets:2544387",
                "nome": "DamageReturnedFlatPhysical",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544387
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "Source[\"Armor\"] * {.03f, .03f}",
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
              "expressao": "{10, 250}",
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

### Opção 2: Frozen Lich Heart
Frigid air swirls around the decaying heart.

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
As you take the Frozen Heart it's numbing cold begins to feel... comfortable.

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
          "chave": "resources.assets:2545442",
          "nome": "Frozen Lich Heart",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545442
          },
          "tipo": "EventStatus",
          "descricao": "Your cold damage is increased by [0]% against targets that are frozen. Grants immunity to chilled.\n\n<i><color=#808080>The Frozen Heart of the Lich, pulsating with a masterful power of ice and the chill of a thousand winters, imbued its holder with a profound affinity for the cold, such that even in the harshest blizzards they would find a comfortable sanctuary.</color></i>",
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
                "chave": "resources.assets:2544376",
                "nome": "DamageModColdToFrozen",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544376
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "{100, 200}",
              "segunda_passagem": false
            },
            {
              "atributo": {
                "chave": "resources.assets:2544534",
                "nome": "ImmunityChilled",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544534
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 4,
                "nome": "Set"
              },
              "expressao": "1",
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

### Opção 3: Ball Lightning
A tiny marble, within which a swirling storm seems to be contained, radiating with raw, electric energy.

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
You can feel the thrum of power, the contained lightning yearning to be released. A ball of lightning, a weapon of pure energy, and one that could turn the tide of any future battle.

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
          "chave": "resources.assets:2545409",
          "nome": "Ball Lightning",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545409
          },
          "tipo": "EventStatus",
          "descricao": "Dealing lightning damage grants a stack of Overcharge: Each stack adds <color=#CBB396>[0]</color> lightning damage to your next basic attack.\n\n<i><color=#808080>In fury, the sky roars, a tempest untamed,\nLightning cracks, an ephemeral fire, wild and unchained.</color></i>",
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
                "chave": "resources.assets:2544579",
                "nome": "BallLightningAmount",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544579
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "ActionStatus.GetFlatDamageValue * 15 * Target.DamageModLightning",
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


---

## Cursed Tome
Chave: `resources.assets:2545566` — GUID: `256779e1-0d70-40a6-9aea-65054cf58c0a`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/cursed tome - battle 2 — SHA objeto: `ac5bb95bbd9ec9b80e9efc5b2f65c245652ebc7c6967e4af4cc24c8eb046b757`

### Texto original
The air reeks of decay and the sound of bone against steel echoes through the chamber. Though victorious, a tantalizing temptation lingers in the air—the beckoning call to read further within the cursed tome, to unlock even greater powers.

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
    "allowAtAllTimesOfDay": 0,
    "allowedTimeOfDay": 1,
    "allowAtAllLevels": 1,
    "minLevel": 1,
    "terrainTypesAllowedAtAnyTime": [
      0,
      4,
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
  }
}
```

### Opção 1: Read on
Continue to read from the <incr><indigo><b>Cursed Tome</b></indigo></incr>.

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
Against your better judgment, you succumb once more to the allure of the forbidden words. Page after page, you delve deeper into the arcane text, your voice resonating with both trepidation and a growing hunger for power. 

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

Combate configurado:
```json
{
  "iniciar": true,
  "manual": false,
  "referencia": {
    "chave": null,
    "nome": null,
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  "override": {
    "ForceRandomSuperUnique": 1,
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
    "FillOutBattlePoints": 1,
    "OverrideBattlePoints": 0,
    "BattlePointValue": 8,
    "OverrideEnemyGroupPool": 1,
    "EnemyGroupPool": [
      43
    ],
    "OverrideEnemyTypePool": 0,
    "EnemyTypePool": [],
    "VictoryEvent": {
      "m_FileID": 0,
      "m_PathID": 2545567
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
}
```
### Opção 2: Leave
Fear takes your hearts and you resist the insidious whispers that still dance upon the edges of your consciousness.

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
You place the <incr><indigo><b>Cursed Tome</b></indigo></incr> back upon its altar and back away.

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

## Cursed Tome
Chave: `resources.assets:2545567` — GUID: `1f424434-f6b6-4a63-af9d-3880c5a2f9a2`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/cursed tome - battle 3 — SHA objeto: `5e6f783e4baa139b8ed7d02fbfe37e8946cb516267cdc20df2067ece73119cc1`

### Texto original
With each incantation, the shadows deepen, and a newfound connection to the realm of the undead is forged. The cursed tome holds yet more temptations. It whispers promises of untold power, urging you to delve deeper, to uncover its darkest secrets.

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
    "allowAtAllTimesOfDay": 0,
    "allowedTimeOfDay": 1,
    "allowAtAllLevels": 1,
    "minLevel": 1,
    "terrainTypesAllowedAtAnyTime": [
      0,
      4,
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
  }
}
```

### Opção 1: Read on
Finish what you've started. 

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
Unyielding in your resolve, you continue to read aloud from the cursed tome, its words resonating with a power that transcendes the mortal realm.

Grotesque specters of a bygone age appear, hungering for the living, their eyes empty voids of malice.

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

Combate configurado:
```json
{
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
        "NameOverride": "Evil Caster",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2548224
        },
        "ForcedEnemyMods": [
          {
            "m_FileID": 0,
            "m_PathID": 2545360
          }
        ],
        "IsSuperUnique": 1
      },
      {
        "OverrideEnemyName": 1,
        "NameOverride": "Evil Warrior",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2548222
        },
        "ForcedEnemyMods": [
          {
            "m_FileID": 0,
            "m_PathID": 2545360
          }
        ],
        "IsSuperUnique": 1
      },
      {
        "OverrideEnemyName": 1,
        "NameOverride": "Evil Rogue",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2548223
        },
        "ForcedEnemyMods": [
          {
            "m_FileID": 0,
            "m_PathID": 2545360
          }
        ],
        "IsSuperUnique": 1
      }
    ],
    "EnemyModApplications": [],
    "EnemyStatusApplications": [],
    "FillOutBattlePoints": 0,
    "OverrideBattlePoints": 0,
    "BattlePointValue": 8,
    "OverrideEnemyGroupPool": 1,
    "EnemyGroupPool": [],
    "OverrideEnemyTypePool": 0,
    "EnemyTypePool": [],
    "VictoryEvent": {
      "m_FileID": 0,
      "m_PathID": 2545568
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
}
```
### Opção 2: Leave
Fear takes your hearts and you resist the insidious whispers that still dance upon the edges of your consciousness.

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
Your shaking hands close the <incr><mythic><b>Cursed Tome</b></mythic></incr> and you run for your life!

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

## Cursed Tome
Chave: `resources.assets:2545568` — GUID: `08293297-072b-415d-abf0-f966e0c6645f`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/cursed tome - victory — SHA objeto: `5bdb8b540a78bd8a33e5213326ec8fc45cd17d4cba0f0ac4be5cb77d941ca2c9`

### Texto original
Your valor and cunning prevaile over the darkness you had summoned. As the undead champions crumbled into dust, their forms dispersing into nothingness, a surge of power courses through you. You have harnessed the very essence of the <indigo><b><incr>Necronomicon</incr></b></indigo>.

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
    "allowAtAllTimesOfDay": 0,
    "allowedTimeOfDay": 1,
    "allowAtAllLevels": 1,
    "minLevel": 1,
    "terrainTypesAllowedAtAnyTime": [
      0,
      4,
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
  }
}
```

### Opção 1: Take
Take the <indigo><b><incr>Necronomicon</incr></b></indigo>'s power for yourself.

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
The whispers grow more insistent as you take the <indigo><b><incr>Necronomicon</incr></b></indigo>, unraveling all the mysteries that lay within.

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
          "chave": "resources.assets:2545457",
          "nome": "Necronomicon",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545457
          },
          "tipo": "EventStatus",
          "descricao": "<i><color=#808080>You carry the Necronomicon!</i></color> \n\nChanges your @Skeletal Summons@ into something... stronger. Increases Summon Damage and Health by {5,25}%",
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
```


---

## Dark Discoveries
Chave: `resources.assets:2545571` — GUID: `32b5d67b-797e-4a2e-8af6-1b2ee1e1b4c7`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/dark discoveries - victory — SHA objeto: `a3e23b1b2515801f536a2e0b4a1e8789e6f5d20ab382d5b218db8085655eac4a`

### Texto original
Having vanquished the abominations <blue><b><incr>The Necromancer</incr></b></blue> greets you:

"You have returned the souls of the damned to me. As agreed, I shall be your mentor, guiding your steps through the perilous realm of necromancy. But it will be your hearts, your intentions, that shall determine the outcome. The power itself is neither good nor evil—it is how it is wielded that defines its nature."

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
  }
}
```

### Opção 1: Accept
Learn the techniques of the Necromancer.

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
Under the guidance of the Necromancer, you delve into the intricacies of necromantic spells, learning to harness the raw power that lay hidden within the realm of the dead.

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
          "chave": "resources.assets:2545485",
          "nome": "Unholy Sacrifice",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545485
          },
          "tipo": "EventStatus",
          "descricao": "Grants the skill @Unholy Sacrifice@. Increases @Shadow Damage@ by {6,30}%.",
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
```


---

## Desecrated Statue of the First Mountain King
Chave: `resources.assets:2545574` — GUID: `ff5a1efb-7689-4e82-99b2-0bda947a8f47`
Categoria: NotInEventPool — raridade: Mythic (4) — peso relativo: 1.0
Origem: events/desecrated statue of the first mountain king - victory — SHA objeto: `64131e410a2785a4e444aee18134009eea7cfbe6e771ffc18106424838b53f1c`

### Texto original
With the wild pack of goblins vanquished and victory ringing through the air, you survey the aftermath of your hard-fought battle. Amidst the scattered remnants of the goblin horde, you find pieces of the golden statue. The voice of the King fills your mind:

"Those pesky goblins have been tainting my sacred halls for far too long. 'Bout time someone put 'em in their place!" 

"May your hearts be as sturdy as the stone, and your spirits as unyielding as the forge. Go forth, with the Blessing of the Mountain."

### Resultados possíveis (texto autoral)
(string vazia no asset)

### Condições e modos
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
    "KeepInDeckWhenUsed": 1,
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
  }
}
```

### Opção 1: Accept
Take the Blessing.

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
You are filled with a fiery passion for battle and the frothy embrace of ale. It burns within your very being, igniting your spirit with a fierce determination and an insatiable thirst for both victory and merriment.

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
          "chave": "resources.assets:2545410",
          "nome": "Blessing of the Mountain",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545410
          },
          "tipo": "EventStatus",
          "descricao": "Grants a 50% chance to resist any control effects.  Increases @Max Health@ by {15,30}%.\n\n<i><color=#808080>Enough is enough!</i></color>\n",
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
                "chave": "resources.assets:2544554",
                "nome": "StatusResistImpairment",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544554
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "{50, 50}",
              "segunda_passagem": false
            },
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
              "expressao": "{15,30}",
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
```


---

## Enchanted Pumpkin Patch
Chave: `resources.assets:2545586` — GUID: `9b40c53e-d59b-443b-a06b-4f5719f4666a`
Categoria: NotInEventPool — raridade: Rare (2) — peso relativo: 1.0
Origem: events/enchanted pumpkin patch - victory — SHA objeto: `2fff85fce3566b883f70b8f6c78682b93a5e78b73399ade2bb98e7b650282907`

### Texto original
With a resounding crash, the final blow is struck. <b><incr><indigo>The Scarecrow</indigo></incr></b> lets out a creaking groan that echoes through the still forest air, its luminescent eyes flickering once before fading out. It collapses back into its initial position, once more an ordinary sentinel amidst the pumpkins.

Victorious, you once again turn your attention to the enchanted pumpkins. 

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
  }
}
```

### Opção 1: Take
Claim an <b><orange>Enchanted Pumpkin</orange></b> for yourself.

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
You reach out and pluck a large pumpkin from the vine. Its surface is warm to the touch, a subtle energy thrumming beneath the smooth rind.

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
          "chave": "resources.assets:2545436",
          "nome": "Enchanted Pumpkin",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545436
          },
          "tipo": "EventStatus",
          "descricao": "Gain [0] Health and Mana each turn.\n\n<i><color=#808080>There is an intoxicating aroma about it. It smells of autumn nights and whispered tales around a fire, of ancient magic and timeless tales.</color></i>\n",
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
                "chave": "resources.assets:2544426",
                "nome": "HealthPerTurn",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544426
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "12",
              "segunda_passagem": false
            },
            {
              "atributo": {
                "chave": "resources.assets:2544431",
                "nome": "ManaPerTurn",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544431
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "12",
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


---

## Foreboding Gem - Victory
Chave: `resources.assets:2545594` — GUID: `46d77b69-0a9f-4d25-bc2d-15e6745c120b`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/foreboding gem - victory — SHA objeto: `44dd80410dcef98eba00f0341a94ae3713b0ab61a434dd4563506f53264c43f7`

### Texto original
Finally, after what seems like an eternity of battling shadows, you emerge victorious. Your opponents lay strewn around you, their madness extinguished, replaced by a vacant stare. They had been driven to the edge by the ruby, the allure too strong, the pull too intoxicating.

Carefully, you approach the pedestal, the <red><b><incr>Ruby</incr></b></red> pulsating with an ethereal light. The gem is yours for the taking, the fruits of a hard-won battle.

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
  }
}
```

### Opção 1: Take
You'll be the one to hold the Ruby.

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
The warm, crimson light illuminates your face, casting an eerie glow over your features. Your eyes, usually warm and friendly, now mirror the fierce glow of the gem.

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
```


---

## Gold Lootin' Goblins
Chave: `resources.assets:2545575` — GUID: `ca065336-aaaa-409a-826a-8d1b523acc5b`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/desecrated statue of the first mountain king battle — SHA objeto: `8998a59aa658e552a975a848eb0fcc9c71cb993b96e3af49013c09534621851f`

### Texto original
A band of raucous <b><green><incr>Goblins</incr></green></b> revel in their ill-gotten gains. These mischievous creatures, driven by their insatiable greed, have amassed a collection of treasures that sparkled and gleam in the dim torchlight.

Their celebration echoes through the caverns, filling the air with a cacophony of cackles, guttural laughter, and discordant songs. The goblins, with their hunched forms and gleaming eyes, danced in a frenzy of glee, their long, spindly fingers clutching their newfound wealth.

These are undoubtedly the culprits who desecrated the statue of the Mountain King.

### Resultados possíveis (texto autoral)
(string vazia no asset)

### Condições e modos
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
    "KeepInDeckWhenUsed": 1,
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
  }
}
```

### Opção 1: Fight
Destroy these goblins in the name of the First Mountain King

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
At your approach, the goblins' grins twist into snarls, as they brandish their crude weapons with a savage glee.

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

Combate configurado:
```json
{
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
        "NameOverride": "Volcanus",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545180
        },
        "ForcedEnemyMods": [
          {
            "m_FileID": 0,
            "m_PathID": 2545324
          }
        ],
        "IsSuperUnique": 1
      },
      {
        "OverrideEnemyName": 0,
        "NameOverride": "",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545178
        },
        "ForcedEnemyMods": [
          {
            "m_FileID": 0,
            "m_PathID": 2545324
          }
        ],
        "IsSuperUnique": 1
      },
      {
        "OverrideEnemyName": 0,
        "NameOverride": "",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545179
        },
        "ForcedEnemyMods": [
          {
            "m_FileID": 0,
            "m_PathID": 2545324
          }
        ],
        "IsSuperUnique": 1
      },
      {
        "OverrideEnemyName": 0,
        "NameOverride": "Burnicus",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545182
        },
        "ForcedEnemyMods": [
          {
            "m_FileID": 0,
            "m_PathID": 2545324
          }
        ],
        "IsSuperUnique": 0
      },
      {
        "OverrideEnemyName": 0,
        "NameOverride": "Burnicus",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545182
        },
        "ForcedEnemyMods": [
          {
            "m_FileID": 0,
            "m_PathID": 2545324
          }
        ],
        "IsSuperUnique": 0
      },
      {
        "OverrideEnemyName": 0,
        "NameOverride": "",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545182
        },
        "ForcedEnemyMods": [
          {
            "m_FileID": 0,
            "m_PathID": 2545324
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
      "m_PathID": 2545574
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
}
```
### Opção 2: Leave
(string vazia no asset)

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
As you behold the tumultuous revelry and the wild gleam in the goblins' eyes, a seed of doubt takes root within your heart. Perhaps the honor of a statue isn't worth all this.

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

## Gold Statue of the First Mountain King
Chave: `resources.assets:2545600` — GUID: `d4f3d443-58a3-4d3d-be7d-e2dcc5edb65c`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/gold statue of the first mountain king battle victory — SHA objeto: `fa08a4b31a7e48592a6ddfcbd840696e1592f7681a0a951d71d55c7d1d05b02d`

### Texto original
In the end, the dwarven guard could not stand against you. With a final, valiant cry, the last of the dwarves falls. Silence fills the chamber, the only sound is your own labored breathing. The battle is over. You are victorious. Free to desecrate the sacred statue.

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
  }
}
```

### Opção 1: Claim the gold
(string vazia no asset)

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
(string vazia no asset)

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
      "dar": true,
      "pool_tipo": {
        "valor": 2,
        "nome": "Unassigned"
      },
      "quantidade_configurada": 0,
      "tabelas": [
        {
          "mustGetOne": 0,
          "itemLootChances": [
            {
              "ItemInfo": {
                "m_FileID": 0,
                "m_PathID": 2546476
              },
              "Chance": 100.0
            },
            {
              "ItemInfo": {
                "m_FileID": 0,
                "m_PathID": 2546477
              },
              "Chance": 100.0
            },
            {
              "ItemInfo": {
                "m_FileID": 0,
                "m_PathID": 2546478
              },
              "Chance": 100.0
            }
          ]
        }
      ],
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

## Hell Coffer
Chave: `resources.assets:2545605` — GUID: `f40b4b0b-e070-4566-8cfd-3b2061b83e38`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/hell coffer victory — SHA objeto: `8c23e375e5759483318a92b0d5403842b5450981011207b9ba87803989ffa281`

### Texto original
Finally, the last of the fiery damned falls, its form collapsing into embers that quickly fade away. The <red><b><incr>Hell Coffer</incr></b></red>, once spinning with the force of a maelstrom, slows finally coming to a stop. A soft click echos as it unlocks, revealing its treasures to the victorious.

### Resultados possíveis (texto autoral)
What treasure will you take?

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
  }
}
```

### Opção 1: Enchant Shadow
(string vazia no asset)

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
(string vazia no asset)

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
          "chave": "resources.assets:2545435",
          "nome": "Enchant Shadow",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545435
          },
          "tipo": "EventStatus",
          "descricao": "Grants @level@ {1,30} Enchant Shadow.\n\n<i><color=#808080>Wreathe your weapon in darkest shadow.</i></color>\n",
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
```

### Opção 2: Enchant Holy
(string vazia no asset)

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
(string vazia no asset)

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
          "chave": "resources.assets:2545434",
          "nome": "Enchant Holy",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545434
          },
          "tipo": "EventStatus",
          "descricao": "Grants @level@ {1,30} Enchant Holy.\n\n<i><color=#808080>Brandish your weapon in glorious light.</i></color>\n",
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
```


---

## Hell Gate
Chave: `resources.assets:2545607` — GUID: `a0c8980b-0e39-42fe-bdba-f9570b2ce256`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/hell gate - victory — SHA objeto: `56a0917dc255a6ed69fd80d04ab8b21be5a6aea7197282e3511482850690194c`

### Texto original
You have defeated <red><b><incr>Lord Infernicus</incr></b></red>!

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
  }
}
```

### Opção 1: Claim
Take the <red><b><incr>Soul of Lord Infernicus</incr></b></red>.

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
(string vazia no asset)

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
          "chave": "resources.assets:2545472",
          "nome": "Soul of Fire",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545472
          },
          "tipo": "EventStatus",
          "descricao": "Gain {6,30}% Increased Fire Damage. Your stacks of Heat now reduce Healing Received by 5% per stack.\n\n<i><color=#808080>The burning soul of Lord Infernicus!</color></i>\n",
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
                "chave": "resources.assets:2544377",
                "nome": "DamageModFire",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544377
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "{6,30}",
              "segunda_passagem": false
            },
            {
              "atributo": {
                "chave": "resources.assets:2544625",
                "nome": "SoulOfFire",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544625
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 4,
                "nome": "Set"
              },
              "expressao": "{1, 1}",
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


---

## Horn of Glorious Battle
Chave: `resources.assets:2545610` — GUID: `8efe225e-a0d9-40ad-925a-44c3a953f52c`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/horn of glorious battle - victory — SHA objeto: `c01804994cf564b613495af7eb8f675e746938238d312f962bbbe738749939db`

### Texto original
Victory was hard-won and bittersweet. The cavern floor is littered with fallen foes, and you bare numerous injuries. But you are alive, and have proven yourself against a horde of summoned enemies. You have faced the call of the battle and emerged victorious.

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
  }
}
```

### Opção 1: Victory
(string vazia no asset)

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
Victory has left you sharper, stronger, and  more experienced. 

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

## Jack in the Box
Chave: `resources.assets:2545613` — GUID: `829367c4-e662-483a-8be7-ba402d121e10`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/jack in the box - phase 2 — SHA objeto: `1b64f1bd9c4c81194cc1a6e700a11a9ca7e19ddb6c8ec19abf65e39216f47394`

### Texto original
Turn after turn, you anticipate the monstrous spring-loaded figure within to burst forth. Yet, the jack-in-the-box defies expectation. With each rotation, the melody continues, chilling your bones and testing your resolve, but the lid remains closed.

### Resultados possíveis (texto autoral)
What will you do?

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
  }
}
```

### Opção 1: Crank
Continue to turn the Crank.

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
As the handle moves, the haunting melody plays, a chilling echo of a once innocent children's tune now twisted by its dark surroundings. The notes hang in the air, shrouded in an eerie suspense.

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

Evento encadeado:
```json
{
  "chave": "resources.assets:2545613",
  "nome": "Jack in the Box - Phase 2",
  "pptr": {
    "m_FileID": 0,
    "m_PathID": 2545613
  },
  "tipo": "PartyEvent"
}
```
### Opção 2: Leave
Give up on this twisted game.

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
As you move away, the silence shatters. A blast echoes through the castle as the jack-in-the-box explodes open, a riot of colorful confetti eruptes from its depths. Laughter, eerie and cruel, echoes through the halls as the figure within came into view. The Jack was no more.


In its place stands The Jester. A grotesque caricature of what was once a joyful figure, he wears a motley costume of bright colors, each piece patterned with mocking faces. His own face, disturbingly human, bares a twisted smile as his eyes gleam with cruel mirth. A demon in the garb of a clown, he had awaited your departure to reveal his true, horrifying nature, ready to play his wicked games with the trespassers who dared to disturb his rest.

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

Combate configurado:
```json
{
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
}
```

---

## Jack in the Box
Chave: `resources.assets:2545615` — GUID: `c260fb9c-4f6c-40d8-8b55-2244d53e54d4`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/jack in the box — SHA objeto: `da62f746c1504be9cb7275be8d3447a7c5000e98dd82acd93318255e080e5a0b`

### Texto original
The <b><rainb><incr>Jack-in-the-Box</incr></rainb></b> is immense, a garish curiosity nestled within the shadowed halls of this accursed castle. Its wooden carvings are painted in jaunty hues that clash with the ominous atmosphere that hangs about it. As you approach, it seemed to possess an aura that both invites and warns of the chaos contained within.

### Resultados possíveis (texto autoral)
What will you do?

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
  }
}
```

### Opção 1: Crank
Turn the crank and play the game.

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
As the handle moves, a haunting melody starts to play, a chilling echo of a once innocent children's tune now twisted by its dark surroundings. The notes hang in the air, shrouded in an eerie suspense.

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

Evento encadeado:
```json
{
  "chave": "resources.assets:2545613",
  "nome": "Jack in the Box - Phase 2",
  "pptr": {
    "m_FileID": 0,
    "m_PathID": 2545613
  },
  "tipo": "PartyEvent"
}
```
### Opção 2: Leave
You have no time for childish games.

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
The <b><rainb><incr>Box</incr></rainb></b> will remain a mystery for now.

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

## Jack in the Box - Victory
Chave: `resources.assets:2545614` — GUID: `3251055e-02b6-4581-9994-d258c7ad0cfc`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/jack in the box - victory — SHA objeto: `e8030e31d1125a81c080002d8390fa430a0f7b447c65ba3cf9dbb0cc75b22ff5`

### Texto original
You have vanquished <b><rainb><incr>The Jester</incr></rainb></b>! 

<b><gold><incr>The Paladin</incr></gold></b> greets you:

"You have done what I could not, Hero. You have brought an end to the evil that has twisted this kingdom."

"Take this as a token of my gratitude, let it remind you that for every shadow in the dark, there lives a beacon of light to banish it."

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
  }
}
```

### Opção 1: Accept
Take <b><gold><incr>The Paladin</incr></gold></b>'s gift.

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
You feel the power of light burn within the scale.

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
```

Overrides por FullReleaseMode (todos preservados):
```json
[
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
]
```

---

## King Under the Mountain
Chave: `resources.assets:2545633` — GUID: `01cb5dd1-ba2c-472f-9601-8a43aa56e8b9`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/3 - mountain king ironheart end — SHA objeto: `287c8d1a7c671abd02f9c6b2aec55a8e5a10b86447a1e6b7b58dd908eb312fe1`

### Texto original
With a final, mighty blow you strike down the mighty dwarf. The madness in Ironheart's eyes fade, and for a moment, he is the noble king he once was.

Suddenly, from the depths of his armor, a soft glow begins to emerge. It's a light so pure and gentle, it seems out of place in the dark, cold hall. A small feather, illuminated in a halo of light, floats gracefully from his chest. It's a robin's feather, delicate and beautiful, a symbol of life and new beginnings.

Compelled by an unknown force, you reach out and grasp the feather. The moment your fingers touch it, the world around you dissolves. You are enveloped in a memory so vivid, it's as though you've been transported through time.
<br/>
You find yourself in the dwarven halls of restored splendor, one filled with warmth and laughter. Before you sits Ironheart, but not as the deranged monarch you had just battled. This is Ironheart in his youth, a robust and cheerful king, his eyes sparkling with joy and kindness. On his lap, giggling with innocent delight, is a small dwarven child, his daughter. She playfully tugs at his beard, her laughter echoing through the hall, a sound of pure happiness.
<br/>
As the memory fades you find yourself back in the present, with the magical feather still warm in your hand. For a long moment, you stare at it, recalling your reading about this very feather in your father's journal. You had dismissed it as a figment of your father's illness-induced imagination, a fanciful creation borne from the erratic and fragmented later entries of the journal. But now, as the feather lay tangible and radiant in your hand, the reality of its existence shakes your understanding of what is possible. 

Chronicled within the journal is not only this feather but also other items of mystical importance scattered across the realm.

The next item of importance, as described in the journal, is an amulet, said to be in the possession of a sultan in the deserts of Wyrmrest. 


### Resultados possíveis (texto autoral)
(string vazia no asset)

### Condições e modos
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
  }
}
```


---

## Lady of the Well
Chave: `resources.assets:2545620` — GUID: `a13116b5-0fbf-4598-ab44-f19a70f96365`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/lady of the well - victory — SHA objeto: `c392e22a3be66f17a69da884ed10883a542608888be3332e131320d993b04df6`

### Texto original
Defeated, the <violet><b><incr>Lady of the Well</incr></b></violet> slithers back down the cracks of the sealed well, but she has left her <violet>Shadowy Heart</violet>. 

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
  }
}
```

### Opção 1: Take
Take the <quest>Shadow-Drenched Heart</quest>.

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
(string vazia no asset)

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
```


---

## Lesser Mimic
Chave: `resources.assets:2545617` — GUID: `012ddc27-7b28-4365-9a05-20920ec59c59`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/jewelry box mimic victory — SHA objeto: `6f999e8a2b7a1655e58ed130dbfca0663b3ee3f0e15ba2c62b85336b65d3c1aa`

### Texto original
With an agonizing screech, the final Mimic collapses in on itself, its form dissolving into an amorphous puddle leaving behind only its treasure.



### Resultados possíveis (texto autoral)
What treasure will you take?

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
  }
}
```

### Opção 1: Enchanted Whetstone
A whetstone, unassuming in its appearance, the color of storm clouds at dusk. It is imbued with enchantments of old, filled with the power to hone the edge of any weapon. 

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
As you run the stone along your weapon, sparks fly off, and when you pull your weapon back, the blade glints with a deadly sharpness. 

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
```

### Opção 2: Dwarven Force Generator
A strange artifact that looks like a tightly wound spring set within a sphere of unblemished steel. You can see an intricate network of runes, their glow pulsating in a magical rhythm. 

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
When you pick it up and turned the key set into its side, the device hums to life, sending out a powerful pulse that sends dust motes scattering and your hair standing on end. 

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
```

### Opção 3: Crystal Ball
Roughly the size of an apple and pulsing with an inner light that seems almost alive.

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
As you pick up the Crystal Ball and peer into it, you gasp. The surface of the crystal shifts and swirls revealing an overhead view of the surrounding area. Your location, the winding tunnels, and even the far-off flicker of a goblin camp - it is like looking at a living map.

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
```


---

## Magic Mirror
Chave: `resources.assets:2545625` — GUID: `1f0f2b4d-7ec4-4b10-b489-f382c460efeb`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/magic mirror - victory — SHA objeto: `423a80328f4e4bf4db1abf77abf7ac5d22fd5bebaedf2592663643ab7099adb1`

### Texto original
The <violet><b><incr>Magic Mirror</incr></b></violet> explodes into a shower of glinting shards, the twisted reflections shrieking as they disintegrate along with their prison. The room is plunged into an eerie silence as the echoes of the battle faded away.

You look around, panting heavily, and find a single shard of the mirror, still intact. Your dark reflection is trapped within it, now just an imprisoned ghost of malice.

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
  }
}
```

### Opção 1: Take
Grab a shard of the <violet><b><incr>Magic Mirror</incr></b></violet>. 

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
With an odd sense of satisfaction, you claim the shard, a strange token from a battle that blurred the lines between reality and reflection. It serves as a haunting reminder of the duality within you, a shadowy testament of the darkness confronted and overcome.

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
```


---

## Master of Rage
Chave: `resources.assets:2545650` — GUID: `bc2329a7-1bb4-427a-89f2-afbbc4e157d0`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/master of rage - victory — SHA objeto: `a6e7d4446b5c28eb3639963a6639731233e31041b38eea9a91b598f90597ace1`

### Texto original
As the last wendigo falls, the forest seems to breathe a sigh of relief. You are weary but victorious. 

In the aftermath of the battle, Barloc emerges from the shadowed woods. His gaze is intense, taking in the scene before him. The fallen Wendigos, the triumphant hero, the churned earth and shattered trees.

With a nod of approval, he approaches you. "You fought well," he says, his deep voice booming in the silent forest. "You've faced the fury and sins of others, and now it's time to face your own."

You listen attentively as Barloc imparts his wisdom, his words carrying the weight of countless battles and years spent perfecting his rage. 

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
  }
}
```

### Opção 1: Learn
Perfect your rage.

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
The grizzled barbarian's lessons echo in the quiet mountain, promising new levels of power and control. 

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
```


---

## Mimic
Chave: `resources.assets:2545754` — GUID: `edab07b7-0e1e-4958-b9f1-d0682e99e999`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/treasure chest mimic victory — SHA objeto: `3a0f78b09a1ef76dc85b64883c75f57ffe06043c9c15c7b125f562557d2726ce`

### Texto original
With a final, bone-rattling roar, the Mimic convulses, then collapses, slowly dissolving into an amorphous mass.


Where the Mimic has fallen, a shimmering pile of treasure remains.

### Resultados possíveis (texto autoral)
What treasure will you take?

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
  }
}
```

### Opção 1: Scroll of Monster Summoning
Did that scroll just growl?

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
As you unroll it, an image of a hulking beast claws itself into existence, so realistic that it seems as if it could burst from the parchment at any moment. It snarls, snapping its jaws and swiping with lethal-looking claws.

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
```

### Opção 2: Elixir of the Scarlet Ox
The potion bubbles with magic.

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
The potion glows with a fiery hue, illuminating the shadows of your face. Drinking it in the heat of battle would metaphorically bestow upon you wings.

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
```

### Opção 3: Silver Signet
The small signet shines brightly even in the dark.

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
The moment you touch the ring, you hear the distant clashing of steel, as if phantom warriors were locked in eternal battle. It is a haunting sound, echoing from another time and place. The ring is likely tied to a lineage of warriors, perhaps a token of battle or symbol of honor.

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
```


---

## Ogre Debt Collector
Chave: `resources.assets:2545657` — GUID: `efff6400-391a-4158-9248-07d98b39db76`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/ogre debt collector battle failure — SHA objeto: `30eda1c92c6f20a70361c3f422fe0dc5c374484f66f5132e9696afb7ccc11074`

### Texto original
You were defeated by the Ogre!

He and his minions left you [o1a1_status] and [o1a1_status2].

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
  }
}
```

### Opção 1: Leave
(string vazia no asset)

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
(string vazia no asset)

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
```


---

## Ogre Debt Collector
Chave: `resources.assets:2545658` — GUID: `59467858-3651-4088-829c-b2c0abb5d316`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/ogre debt collector battle victory — SHA objeto: `aab8c652ffc0b481c0a3da6a8dca218e3c52e280aaf133bc4c13f213322972cf`

### Texto original
With a bellow of pain and surprise, the ogre staggers back, his eyes wide. He clutches at his wounds, and then his knees buckle. With a ground-shaking thud, he crashes to the earth.

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
  }
}
```

### Opção 1: Loot
Reclaim the treasure that <orange><b><incr>Krothug</incr></b></orange> had stolen.

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
(string vazia no asset)

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
```


---

## Party like a Pirate
Chave: `resources.assets:2545661` — GUID: `fd31de51-fdde-4e83-a6c9-344c4ed2bfd0`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/party like a pirate 1 — SHA objeto: `818a5d657cf471191045a66eb45f6bd40d1d319ae8b5b1f13fa6aba08876cba9`

### Texto original
The air is heavy with the scent of aged liquor and salty sea breezes, as the tap continues to flow. There is a perverse joy about the place, a carefree abandon that draws you in. 

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
  }
}
```

### Opção 1: Sip
Bottoms up.

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
Your second swig finds you less resistant. Your head spins more, and you can almost hear the raucous laughter of the pirates growing louder. You sway, mimicking their endless party. 

Efeito 1 (configuração autoral, não resultado de partida):
```json
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
```

Evento encadeado:
```json
{
  "chave": "resources.assets:2545662",
  "nome": "Party like a Pirate 2",
  "pptr": {
    "m_FileID": 0,
    "m_PathID": 2545662
  },
  "tipo": "PartyEvent"
}
```
### Opção 2: Leave
You've had enough.

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
"No... No more," you mutter, struggling to keep your voice steady. The spectral cheers in your mind falter, replaced by a surprised murmur. Your body feels heavy and your senses dull, but the ethereal laughter of the skeletal crew is louder than ever, as you stumble away.

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

## Party like a Pirate
Chave: `resources.assets:2545662` — GUID: `e9d21980-ff00-4c6d-b3dc-ef1040133f97`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/party like a pirate 2 — SHA objeto: `3ab7c0bc4415fe0e8202cf84bccd29cde6d5ae43b02fb7c99b7a01bfb148ae8d`

### Texto original
Imaginary roars and hoots of approval fill your ears. You square your shoulders and raise a cup to the absent eyes of the skeletal pirates. "To the captain and his men," you say, nodding to each of the grinning skulls, "may your spirits forever sail on seas of joy."

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
  }
}
```

### Opção 1: Sip
Bottoms up.

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
The rum is strong, too strong. It burns your throat with each swig, sending shivers down your spine, igniting a fire in your belly. Your world is a top, spinning and dancing like the ghostly pirates you imagine around you.

Efeito 1 (configuração autoral, não resultado de partida):
```json
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
```

Evento encadeado:
```json
{
  "chave": "resources.assets:2545663",
  "nome": "Party like a Pirate 3",
  "pptr": {
    "m_FileID": 0,
    "m_PathID": 2545663
  },
  "tipo": "PartyEvent"
}
```
### Opção 2: Leave
You've had enough.

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
"No... No more," you mutter, struggling to keep your voice steady. The spectral cheers in your mind falter, replaced by a surprised murmur. Your body feels heavy and your senses dull, but the ethereal laughter of the skeletal crew is louder than ever, as you stumble away.

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

## Party like a Pirate
Chave: `resources.assets:2545663` — GUID: `20c770ea-3ca7-452d-9236-8abcaa33f2a3`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/party like a pirate 3 — SHA objeto: `ce9c1a2fae430c93bb6e5af86d19652025931fa0825808c2d0d2a16ce3122c75`

### Texto original
The lights dance overhead as you drink, the rum conjuring fanciful images of the skeletal pirates applauding you, their ethereal cheers echoing in your ears.

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
  }
}
```

### Opção 1: Sip
Bottoms up.

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
On your fourth cup, you slump against a barrel, your head spinning. The skeletal pirates loom around you, their eyeless sockets seem to look down on you in approval. "You're one of us now," their silent mouths seem to say, and in your rum-addled brain, you laugh, raising your cup one last time.

Efeito 1 (configuração autoral, não resultado de partida):
```json
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
```

### Opção 2: Leave
You've had enough.

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
"No... No more," you mutter, struggling to keep your voice steady. The spectral cheers in your mind falter, replaced by a surprised murmur. Your body feels heavy and your senses dull, but the ethereal laughter of the skeletal crew is louder than ever, as you stumble away.

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

## Pirate's Treasure
Chave: `resources.assets:2545667` — GUID: `ae77d198-ad55-44dd-ac1f-8abc86c91f0e`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/pirate's treasure - victory — SHA objeto: `c84748b8f41389727fe38e042510316332844aaaccaf7d17633766fc609a5ecb`

### Texto original
As the last skeleton falls, you turn to the chest. The skeletal pirate has released its grip, the wooden chest now lies open. Within it lays old coins, each glimmering with a sinister aura – a heap of cursed gold. 

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
  }
}
```

### Opção 1: Loot
Take the cursed gold.

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
You knew the price of greed, but for now, you have the treasure you sought. What the curse will bring, only time will tell.

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
```


---

## Poacher's Demise
Chave: `resources.assets:2545669` — GUID: `9738c529-ee32-4a4e-859a-772c18be72fa`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/poacher's prize - victory — SHA objeto: `25df2a9e168925072575120a6e70d8191726a06ba5bc893533e4994e1a0db2e2`

### Texto original
With the poachers defeated, you return to the elephant's cage. The lock gives way under your touch, the caged door swings open. The elephant, sensing its newfound freedom, slowly raises its head, its eyes meeting yours.


In a moment of serene understanding, the elephant gently pats you with its trunk, a silent thank you. With a rumble that echoes through the jungle, the elephant then turns and wanders off into the dense foliage, returning to its rightful home.




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
  }
}
```

### Opção 1: Reward
(string vazia no asset)

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
(string vazia no asset)

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
```


---

## Red Dragon
Chave: `resources.assets:2545629` — GUID: `9ad14dbe-13b4-4558-b215-8555482261b8`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/10 - red dragon end — SHA objeto: `28bc49c588406bf00c69865e1a20942fc58694e4a93a77a188113fe46e027558`

### Texto original
The dragon's massive form crashes to the ground, its flames extinguishing in a plume of smoke and ash. The land seems to hold its breath, the sky quieting as the last roar of the dragon fades into silence.

You stand amidst the smoldering landscape, feeling the weight of what has transpired. Yet, even as you contemplate your victory, you know that your journey is far from over. The realm had become safer, a measure of peace restored, but other dragons still soar the skies, and new challenges would undoubtedly arise.

The thought of these new challenges stirs within your heart the beginnings of another adventure.

### Resultados possíveis (texto autoral)
(string vazia no asset)

### Condições e modos
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
  }
}
```


---

## Scent of Blood
Chave: `resources.assets:2545679` — GUID: `5d032595-5d84-48e1-a45e-c521fdb9db1d`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/scent of blood - victory — SHA objeto: `d1ea4f96e50fb4f877c58c33cea95ddb4a59b84cb8c667b75f251a9cf3de50e6`

### Texto original
In the aftermath of the battle, the rest of the wolf pack emerges from the shadows of the mountain, their eyes fixed on you. But instead of hostility or vengeance, there is a sense of recognition in their gaze. They have witnessed the fall of their alpha and understand the unspoken law of the wild – strength commands respect.


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
  }
}
```

### Opção 1: Reward
Accept your place as the new alpha.

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
(string vazia no asset)

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
```


---

## Strange Crystal
Chave: `resources.assets:2545695` — GUID: `16484ea1-d515-436f-85d1-d9ec385681e2`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/strange ice crystal - victory — SHA objeto: `436f53ed9d7b7658f880c17f5491d39fc0ee61fde74d2a50dc0fb9447a52fe15`

### Texto original
You chip away at the frozen behemoths until they fall back, dissipating into puddles of icy water. Panting and frost-bitten, you turn your attention back to the floating crystal.

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
  }
}
```

### Opção 1: Claim your reward
(string vazia no asset)

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

#### Ação 1: Success — RollLimit 16
You can feel the power humming beneath your fingertips as you touch the gleaming surface of the crystal, a shard breaking off cleanly in your hand. A jolt of energy surges into you, the crystal's icy power now yours to command.

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
```


---

## Strange Crystal
Chave: `resources.assets:2545698` — GUID: `af416be6-411b-4377-a37d-e712b04b6c4e`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/strange molten crystal - victory — SHA objeto: `186c786d3d07bfad1d5fa36ab78992a2f7484cc52f767df9285b9e6cd7d56d45`

### Texto original
The last golem crumbles, its once fiery eyes now dull and lifeless, the molten rock cools into a dark, hard crust. Panting heavily, you turn back to the crystal. The air around it still radiates an intense heat, but now, it feels like a challenge instead of a warning.

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
  }
}
```

### Opção 1: Claim your reward
(string vazia no asset)

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

#### Ação 1: Success — RollLimit 16
Slowly, you reach out again, your hand trembling as it nears the scorching aura. With a quick, determined motion, you break a piece off. A surge of power rushes through you, pure and intense, grounding you despite the blistering heat.

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
```


---

## Strange Crystal
Chave: `resources.assets:2545701` — GUID: `f4237415-7dae-4398-8804-812ac8fe4c10`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/strange thunder crystal - victory — SHA objeto: `96cad52e4ed72e1618e181c90ddf03ab8ab165a2961b44a2baed50471caf7b86`

### Texto original
The last thunder golem disintegrates into a burst of light and sound, leaving behind a quiet that is only interrupted by the soft pitter-patter of the rain. The storm has passed, leaving behind a sense of peace.

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
  }
}
```

### Opção 1: Claim your reward
(string vazia no asset)

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

#### Ação 1: Success — RollLimit 16
You approach the crystal once more. This time, instead of a threatening storm, a calming drizzle surrounds you. You take the crystal into your hand, feeling its cool surface against your warm skin. With a swift, controlled motion, you break off a shard. A rush of energy courses through you, powerful and electrifying.

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
```


---

## Sword in the Stone
Chave: `resources.assets:2545704` — GUID: `22307b00-cfcd-42c4-ae4d-54de5f5b30db`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/sword in the stone 1 — SHA objeto: `482464ac270586b9998253095876f53e61acf812d709dbc0431b580352b769a3`

### Texto original
Perhaps another attempt would prove more successful?

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
  }
}
```

### Opção 1: Retrieve
Attempt to pull the <b><gold>Sword</gold></b> from the stone.

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
        "valor": 0,
        "nome": "Might"
      }
    ],
    "misteriosa": true,
    "texto_misterioso": ""
  }
}
```

#### Ação 1: Success — RollLimit 18
Your fingers curl around the hilt, feeling an unexpected warmth seeping into your hand. An odd sense of harmony resonates within you, a chord that seems to reverberate between your heart and the sword. With renewed vigor, you pull, the veins in your arm throbbing with the exertion.


Suddenly, the sword comes free. You stumble back in surprise, the blade held aloft in your hand. It shines even brighter now, as if recognizing its new master.

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
      "dar": true,
      "pool_tipo": {
        "valor": 0,
        "nome": "None"
      },
      "quantidade_configurada": 1,
      "tabelas": [
        {
          "mustGetOne": 1,
          "itemLootChances": [
            {
              "ItemInfo": {
                "m_FileID": 0,
                "m_PathID": 2547088
              },
              "Chance": 100.0
            }
          ]
        }
      ],
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
          "chave": "resources.assets:2545478",
          "nome": "The True King",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545478
          },
          "tipo": "EventStatus",
          "descricao": "Light Spells no longer cost mana to cast. @Holy Power@ increased by {6,30}%.\n\n<i><color=#808080>\"The light is your birth right.\"</color></i>\n",
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
            },
            {
              "atributo": {
                "chave": "resources.assets:2544479",
                "nome": "ManaCostModLight",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544479
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "{-10000, -10000}",
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

#### Ação 2: Failure — RollLimit 0
You try again, summoning every ounce of strength within you. Yet despite your desperate efforts, the result is the same. The sword remains stubbornly lodged within the stone, an unclaimed prize that seems to mock your efforts. The failed attempt has left you [o1a2_status].

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
          "chave": "resources.assets:2545504",
          "nome": "Weakened",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545504
          },
          "tipo": "EventStatus",
          "descricao": "Reduces @Might@ by 20% per stack.",
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
                "chave": "resources.assets:2544453",
                "nome": "MightBase",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544453
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

Evento encadeado:
```json
{
  "chave": "resources.assets:2545705",
  "nome": "Sword in the Stone 2",
  "pptr": {
    "m_FileID": 0,
    "m_PathID": 2545705
  },
  "tipo": "PartyEvent"
}
```
### Opção 2: Leave
You haven't the time for swords or stones.

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
(string vazia no asset)

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

## Sword in the Stone
Chave: `resources.assets:2545705` — GUID: `ae735002-a8fc-4cc3-995b-33c12ada3e63`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/sword in the stone 2 — SHA objeto: `3c77a3044b08e7f06a2f1f3b7b1d614107d5007c7166dbe30f13e3cf9f2b3d0c`

### Texto original
Perhaps another attempt would prove more successful?

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
  }
}
```

### Opção 1: Retrieve
Attempt to pull the <b><gold>Sword</gold></b> from the stone.

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
        "valor": 0,
        "nome": "Might"
      }
    ],
    "misteriosa": true,
    "texto_misterioso": ""
  }
}
```

#### Ação 1: Success — RollLimit 18
Your fingers curl around the hilt, feeling an unexpected warmth seeping into your hand. An odd sense of harmony resonates within you, a chord that seems to reverberate between your heart and the sword. With renewed vigor, you pull, the veins in your arm throbbing with the exertion.


Suddenly, the sword comes free. You stumble back in surprise, the blade held aloft in your hand. It shines even brighter now, as if recognizing its new master.

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
      "dar": true,
      "pool_tipo": {
        "valor": 0,
        "nome": "None"
      },
      "quantidade_configurada": 1,
      "tabelas": [
        {
          "mustGetOne": 1,
          "itemLootChances": [
            {
              "ItemInfo": {
                "m_FileID": 0,
                "m_PathID": 2547088
              },
              "Chance": 100.0
            }
          ]
        }
      ],
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
          "chave": "resources.assets:2545478",
          "nome": "The True King",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545478
          },
          "tipo": "EventStatus",
          "descricao": "Light Spells no longer cost mana to cast. @Holy Power@ increased by {6,30}%.\n\n<i><color=#808080>\"The light is your birth right.\"</color></i>\n",
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
            },
            {
              "atributo": {
                "chave": "resources.assets:2544479",
                "nome": "ManaCostModLight",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544479
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "{-10000, -10000}",
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

#### Ação 2: Failure — RollLimit 0
With a heave, you pull. Your muscles strain and your breath grows ragged, but the sword remains steadfast, the stone refusing to relinquish its hold. You stagger back, frustrated and tired, a sheen of sweat dotting your brow. The failed attempt has left you [o1a2_status].

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
          "chave": "resources.assets:2545504",
          "nome": "Weakened",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545504
          },
          "tipo": "EventStatus",
          "descricao": "Reduces @Might@ by 20% per stack.",
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
                "chave": "resources.assets:2544453",
                "nome": "MightBase",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544453
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

Evento encadeado:
```json
{
  "chave": "resources.assets:2545706",
  "nome": "Sword in the Stone 3",
  "pptr": {
    "m_FileID": 0,
    "m_PathID": 2545706
  },
  "tipo": "PartyEvent"
}
```
### Opção 2: Leave
You haven't the time for swords or stones.

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
(string vazia no asset)

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

## Sword in the Stone
Chave: `resources.assets:2545706` — GUID: `fb36f25c-2e0a-41cb-8c7b-e4ff1a0cd1f9`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/sword in the stone 3 — SHA objeto: `3d3081559027d1858f852be7e1935d2406876d7d7da71ce785191601a64d6eb1`

### Texto original
Perhaps another attempt would prove more successful?

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
  }
}
```

### Opção 1: Retrieve
Attempt to pull the <b><gold>Sword</gold></b> from the stone.

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
        "valor": 0,
        "nome": "Might"
      }
    ],
    "misteriosa": true,
    "texto_misterioso": ""
  }
}
```

#### Ação 1: Success — RollLimit 18
Your fingers curl around the hilt, feeling an unexpected warmth seeping into your hand. An odd sense of harmony resonates within you, a chord that seems to reverberate between your heart and the sword. With renewed vigor, you pull, the veins in your arm throbbing with the exertion.


Suddenly, the sword comes free. You stumble back in surprise, the blade held aloft in your hand. It shines even brighter now, as if recognizing its new master.

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
      "dar": true,
      "pool_tipo": {
        "valor": 0,
        "nome": "None"
      },
      "quantidade_configurada": 1,
      "tabelas": [
        {
          "mustGetOne": 1,
          "itemLootChances": [
            {
              "ItemInfo": {
                "m_FileID": 0,
                "m_PathID": 2547088
              },
              "Chance": 100.0
            }
          ]
        }
      ],
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
          "chave": "resources.assets:2545478",
          "nome": "The True King",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545478
          },
          "tipo": "EventStatus",
          "descricao": "Light Spells no longer cost mana to cast. @Holy Power@ increased by {6,30}%.\n\n<i><color=#808080>\"The light is your birth right.\"</color></i>\n",
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
            },
            {
              "atributo": {
                "chave": "resources.assets:2544479",
                "nome": "ManaCostModLight",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544479
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "{-10000, -10000}",
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

#### Ação 2: Failure — RollLimit 0
With a deep breath, you try again. Your entire being focused on the task, your muscles coiling with effort. Yet, once again, the sword stays in place, stubbornly silent and immovable. You fall to your knees, your hopes dashed. The failed attempt has left you [o1a2_status].

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
          "chave": "resources.assets:2545504",
          "nome": "Weakened",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545504
          },
          "tipo": "EventStatus",
          "descricao": "Reduces @Might@ by 20% per stack.",
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
                "chave": "resources.assets:2544453",
                "nome": "MightBase",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544453
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
You haven't the time for swords or stones.

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
(string vazia no asset)

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

## Talk to the Spirits.
Chave: `resources.assets:2545708` — GUID: `b74e712d-64f4-4985-84eb-18faec5b1f85`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/talk ta de spirits! 1 — SHA objeto: `78b3263a05c878830b50cbf50b27c6f5f39897ff0efb3274abaec8f722ed92c3`

### Texto original
"Part of your spirit now," the sage demands next, his hands moving in a complex pattern over the fire. You take a deep breath, a sense of foreboding washing over you. 

### Resultados possíveis (texto autoral)
Will you sacrifice?

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
  }
}
```

### Opção 1: Sacrifice
Give up your mana.

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
A sharp pain follows as the goblin chants over the fire, the flame flaring brightly as it claims a portion of your spirit. The sensation is strange, like a piece of you is being torn away, leaving an empty space in its wake.

Efeito 1 (configuração autoral, não resultado de partida):
```json
{
  "vida_mana": {
    "percentMaxHealth": 0.0,
    "percentMaxMana": -30.0,
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

Evento encadeado:
```json
{
  "chave": "resources.assets:2545709",
  "nome": "Talk ta de Spirits! 2",
  "pptr": {
    "m_FileID": 0,
    "m_PathID": 2545709
  },
  "tipo": "PartyEvent"
}
```
### Opção 2: Decline
The sacrifice is too great.

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
You walk away, wondering what your ancestors would say...

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

## Talk to the Spirits.
Chave: `resources.assets:2545709` — GUID: `bacd9421-4c77-492b-b704-e9a8e77db0bd`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/talk ta de spirits! 2 — SHA objeto: `874191e9ac9474fb5f8e55338e908aece4501c6d38b062f75958caa20fe4acb8`

### Texto original
With the final act, the sage begins to chant, his words twisting and turning in the air like the spiraling smoke above the fire. As the sage's voice grows louder, you feel a power washing over you. Then, quite suddenly, the cave is filled with whispers, ethereal and ancient.


You recognized them, the voices of your ancestors. They speak of hardships and triumphs, love and sacrifice. Their voices are soft, their messages powerful, and their wisdom invaluable. 

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
  }
}
```

### Opção 1: Protection
Petition for protection.

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
They bestow upon you their blessing, a shield of protection woven from their collective love and strength. You are filled with a comforting warmth, and the fire turns a serene shade of white.

As you step out of the vision and back into the world, you can feel the spirits following closely. They move with you, their forms nearly invisible but for the faint glimmer that traces your silhouette. 

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
          "chave": "resources.assets:2545407",
          "nome": "Ancestral Protection",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545407
          },
          "tipo": "EventStatus",
          "descricao": "Grants a 10% chance to cast @Level@ {1,30} Avenging Ancestors on an enemy that strikes you. Grants {20,300} Armor and Magic Armor.\n\n<i><color=#808080>\"You do not walk this world alone. With every step you take, you tread upon the footprints of your ancestors. They have blazed the trail before you, weathering storms you cannot fathom, crossing paths you cannot see.\"</i></color>",
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
              "expressao": "{20,300}",
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
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "{20,300}",
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


---

## Taste for Blood
Chave: `resources.assets:2545714` — GUID: `a1d68598-66ff-4361-8c90-5e4ffa6b931d`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/taste for blood  - bishop victory — SHA objeto: `72885d60c35361c96df79edd4896225d25eb81b0d6e21e5c9df3c35873f7c32a`

### Texto original
You have defeated The Bishop! Samara greets you.

"He stole everything from me. My family, my future, my humanity. I was but a pawn in his twisted game. But no more."

"Take this... for helping me sate my vengeance."


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
  }
}
```

### Opção 1: Accept 
Take her gift.

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
"Be a force of retribution, balancing the scales for the pain and suffering caused by those who are supposed to be shepherds of the light."

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
          "chave": "resources.assets:2545486",
          "nome": "Vampirism",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545486
          },
          "tipo": "EventStatus",
          "descricao": "Increases @Life Steal@ by @12@% and @Damage@ by @35@%.\n\nGain the ability to shapeshift into a @Vampire Bat@.\n\nDecreases @Fire Resistance@ by @25@%. Can no longer heal from anything but lifesteal.\n\n<i><color=#808080>\"A vampire not evil, a paradox in twilight's gleam,\nCleansing the world, in a dark redemption's dream.\"</i></color>\n\n",
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
                "chave": "resources.assets:2544459",
                "nome": "LifeOnHit",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544459
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "{12,12}",
              "segunda_passagem": false
            },
            {
              "atributo": {
                "chave": "resources.assets:2544585",
                "nome": "ChildOfTheAbyss",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544585
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 4,
                "nome": "Set"
              },
              "expressao": "{1,1}",
              "segunda_passagem": false
            },
            {
              "atributo": {
                "chave": "resources.assets:2544373",
                "nome": "DamageMod",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544373
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "{35,35}",
              "segunda_passagem": false
            },
            {
              "atributo": {
                "chave": "resources.assets:2544498",
                "nome": "ResistFire",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544498
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "{-25,-25}",
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


---

## Taste for Blood
Chave: `resources.assets:2545715` — GUID: `a806d1db-be3a-4eb7-be2b-36e655f162d0`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/taste for blood  - samara victory — SHA objeto: `ff56b0ce1b2c739d0a15e69df272638f15431a5614e2234d418936646ee03609`

### Texto original
You have defeated Samara! The Bishop greets you with a smile.

"You have done very well my child!" the Bishop says, his voice a soothing melody. Yet, as he speaks, you notice a subtle change in his demeanor. The once kind and gentle eyes now carry a hint of something darker, a shadow that seems out of place in his holy countenance.

His hands, clasped together in gratitude, unfold to reveal a remarkable object - an Ebony Scale. This scale, unlike any you have seen before, is as dark as the deepest night, absorbing the light around it as if it were a fragment of the abyss itself.

He extends the scale towards you, urging you to take it.


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
  }
}
```

### Opção 1: Accept 
Take his gift.

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
As your fingers grasp the dark artifact, a chill runs down your spine.

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
          "chave": "resources.assets:2545425",
          "nome": "Ebony Dragon Scale",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545425
          },
          "tipo": "EventStatus",
          "descricao": "Gain the ability to shapeshift into a Black Dragonkin.\n\n<i><color=#808080>\"The scale emanates a palpable aura of malevolence, a taint that seems to claw at the very air around it.\"</color></i>",
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
```


---

## Taste for Blood
Chave: `resources.assets:2545716` — GUID: `850460da-6433-4de4-ba65-76963154f6e8`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/taste for blood 1 — SHA objeto: `debde4661b232de5a39abc8009b9491a4d37170ef3b6c2747bbb4d28140b1156`

### Texto original
She was not a rotting corpse as you had half-expected, but a young woman of otherworldly beauty, her face as timeless as the night itself. Her eyes flicker open, and in their ruby depths, you see a promise of darkness and power.

Her gaze holds you captive; you are drawn to her like a moth to a flame. Her lips, as red as a blooming rose, curl into a tantalizing smile. She holds out her hand, not in fear or plea, but in invitation.


"Join me," <red><incr><b>Samara</b></incr></red> whispers, her voice echoing like a melody through the ancient crypt, "Allow me to grant you the power of the night. A single bite, and you will be forever changed."

### Resultados possíveis (texto autoral)
Will you succumb?

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
  }
}
```

### Opção 1: Give In
Eagerly accept her gift.

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
A satisfied grin dances on <red><incr><b>Samara</b></incr></red>'s lips as she draws you close. In a swift, predatory movement, she sinks her fangs into your neck. You tense, your heart slams against your chest as the lifeblood is drawn from you. A wave of euphoria washes over you, followed by an onslaught of pain as her essence intertwines with yours.

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
          "chave": "resources.assets:2545476",
          "nome": "Taste for Blood",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545476
          },
          "tipo": "EventStatus",
          "descricao": "Increases @Life Steal@ by 4%.\n\n<i><color=#808080>\"Everyone needs to eat.\"</i></color>",
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
                "chave": "resources.assets:2544459",
                "nome": "LifeOnHit",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544459
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "{4, 4}",
              "segunda_passagem": false
            }
          ]
        },
        {
          "chave": "resources.assets:2545512",
          "nome": "Hunger for Vengeance",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545512
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
```

### Opção 2: Resist
Reject her curse.

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

#### Ação 1: Success — RollLimit 14
You clench your fists, gritting your teeth as you force your eyes away from the woman's hypnotic gaze. You shiver at the seductive sound of her voice that reverberates in your skull, echoing her enticing promise. Yet, you stand your ground, the thought of your humanity fading away horrifying you more than her allure.

"You...refuse?" the vampiress questioned, her voice a whispes of disbelief. Her ruby eyes flash with an icy fury, her enchanting visage twists with veiled disappointment and barely concealed rage.

"Very well," she murmurs, and waves you away dismissively, a queen dismissing her subjects. 

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

#### Ação 2: Failure — RollLimit 0
In spite of the warnings flashing in your mind, you step forward, captivated by <red><incr><b>Samara</b></incr></red>'s hypnotic gaze. She is breathtaking, the embodiment of an enchanting enigma, a deadly allure that whispered promises of power. 

Every instinct is screaming at you to break free, to flee, but you are trapped in the web of her alluring enchantment.

In the chilling silence of the crypt, her fangs pierce your flesh. The sudden pain is a stark reminder of the reality you have forgotten, the peril you have walked into. But it is too late. As the icy venom courses through your veins, your world spins and goes dark.

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
          "chave": "resources.assets:2545476",
          "nome": "Taste for Blood",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545476
          },
          "tipo": "EventStatus",
          "descricao": "Increases @Life Steal@ by 4%.\n\n<i><color=#808080>\"Everyone needs to eat.\"</i></color>",
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
                "chave": "resources.assets:2544459",
                "nome": "LifeOnHit",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544459
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "{4, 4}",
              "segunda_passagem": false
            }
          ]
        },
        {
          "chave": "resources.assets:2545512",
          "nome": "Hunger for Vengeance",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545512
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
```


---

## Taste for Blood
Chave: `resources.assets:2545717` — GUID: `882a9b9c-9acb-4c6a-85e1-54b4ee44dd27`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/taste for blood 2 - an innocent life — SHA objeto: `37cb53a7b1f9ce877886d2246a4a2ca24c2b07a57106f0fbdd5fc0ce88384675`

### Texto original
<red><incr><b>Samara</b></incr></red> stands confronting a terrified bishop, the man's eyes are wide with pure, unfiltered terror.


In the dim candlelight, the vampire's skin glows with an ethereal light, highlighting her unearthly beauty. Her fangs, now bared in a cruel smile, glint menacingly. The sight is both terrifying and enchanting, a testament to her unholy power.


The vampire's voice, a bewitching melody, fills your mind, thundering with a command, "<red><b>Slay the bishop!</b></red>" It is not a suggestion, but an order - one that tugs at the very edges of your resolve. The words echo around your skull, each syllable like a hammer blow, shattering the peace within.

### Resultados possíveis (texto autoral)
Will you resist Samara?

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
  }
}
```

### Opção 1: Give In
Slay the bishop.

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

#### Ação 1: Success — RollLimit 12
As you near the trembling figure, an intense flash of images rush into your mind, unbidden yet consuming. You see the same bishop, his hands soaked in innocent blood, his eyes lit with unholy fervor. A young Samara lay lifeless on a dark altar, her life sacrificed in the pursuit of dark power. The vision is too raw, too visceral, to be an illusion.

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

Combate configurado:
```json
{
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
          "m_PathID": 2545116
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
      "m_PathID": 2545714
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
}
```
### Opção 2: Resist
Attempt to resist Samara's command.

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

#### Ação 1: Success — RollLimit 10
A moment of clarity cuts through the insidious voice like a blade. You are not a puppet to be commanded, especially by a creature of darkness. You steel your resolve, meeting the vampire's gaze with a defiant glare.

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

Evento encadeado:
```json
{
  "chave": "resources.assets:2545718",
  "nome": "Taste for Blood 3 - Priest's Plea",
  "pptr": {
    "m_FileID": 0,
    "m_PathID": 2545718
  },
  "tipo": "PartyEvent"
}
```
#### Ação 2: Failure — RollLimit 0
As you resist Samara's call, an intense flash of images rush into your mind, unbidden yet consuming. You see the same bishop, his hands soaked in innocent blood, his eyes lit with unholy fervor. A young Samara lay lifeless on a dark altar, her life sacrificed in the pursuit of dark power. The vision is too raw, too visceral, to be an illusion.

Combate configurado:
```json
{
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
          "m_PathID": 2545116
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
}
```

---

## Taste for Blood
Chave: `resources.assets:2545718` — GUID: `c869d363-e251-4c9f-81f2-a9f0089e0c4b`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/taste for blood 3 - priest's plea — SHA objeto: `b106fccbef014a3f9c3ec84d2ce1346dcadd981d970f4ad08dd63b9c944012f3`

### Texto original
From the corners of your eyes, you see the priest pleading, words tumbling out in a terrified rush, "Stop... you must stop her! Free yourself! Don’t let her control you!" Samara's reaction is immediate and fierce. Her face contorts in rage, a snarl forming on her lips as she spits at the priest, "Liar! I'll drink your blood for what you’ve done to me."

### Resultados possíveis (texto autoral)
Who will you listen to?

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
  }
}
```

### Opção 1: Listen to the Bishop
Slay Samara.

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
The desperation in the bishop's voice stirs you, reminding you of the hero you are meant to be. You step forward, drawing the vampire's attention away from the bishop, ready to challenge her and protect the innocent. You will not allow the monster to harm the man of faith.

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

Combate configurado:
```json
{
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
          "m_PathID": 2545041
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
      "m_PathID": 2545715
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
}
```
### Opção 2: Side with Samara
Slay the Bishop

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
As you near the trembling bishop, an intense flash of images rush into your mind, unbidden yet consuming. You see the same bishop, his hands soaked in innocent blood, his eyes lit with unholy fervor. A young Samara lay lifeless on a dark altar, her life sacrificed in the pursuit of dark power. The vision is too raw, too visceral, to be an illusion.

The Bishop looks at you, a smug smile playing on his lips. His eyes are no longer filled with fear, replaced instead by a cold, calculated calm. The smile widens, twisting into a cruel sneer as he threatens, "You dare raise your weapon against a man of the church? You will regret this, fool."

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

Combate configurado:
```json
{
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
          "m_PathID": 2545116
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
      "m_PathID": 2545714
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
}
```

---

## The Animator
Chave: `resources.assets:2545731` — GUID: `367876d3-1828-4bf5-bff6-c6b768e81012`
Categoria: NotInEventPool — raridade: Mythic (4) — peso relativo: 1.0
Origem: events/the animator - success — SHA objeto: `2b249e9250a9f472571572e127a6767ae6c2a8bf328cf7a6478e652df60732f6`

### Texto original
"You're back!" Ani exclaims, the clinking sounds of her tools against the golem falling silent. She dusts her hands on her apron, her eyes light up at the sight of the glowing hearts. "And you've brought the hearts! Brilliant!"

Handing over the fire demon hearts, you watch as Ani inspects them, her experienced hands deftly feeling their pulsating warmth. "Perfect," she murmurs, her eyes filled with an almost manic excitement.

With utmost care, Ani unlocks a panel on the golem's chest. She carefully places the hearts inside, securing the compartment. The light from the hearts diffuses across the golem's interior, casting a web of intricate shadows against the cave walls. The heroes watch in amazement as she channels her own magic, her fingers tracing the arcane symbols that cover the golem.

The moment the last symbol is lit, the golem's eyes flicker to life. Ani steps back, her face flush with triumph, and the golem starts to move, its limbs creaking loudly. It takes a step forward, and another, the ground shaking beneath its weight.

"Thanks to your efforts, I see no reason not to allow my friend here to assist you in your endeavors." She pats the large golem affectionately. Its steely exterior now hums with a fiery energy from within, its eyes glowing a warm, familiar orange.

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
  }
}
```

### Opção 1: Reward
(string vazia no asset)

Condições/rolagem:
```json
{
  "condicoes": {
    "status_requeridos": [
      {
        "chave": "resources.assets:2545505",
        "nome": "Burning Demon Hearts",
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545505
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
The golem steps forward, creaking and groaning as it moves. It is a spectacle of engineering and magic, an iron giant ready to protect its master. Despite its formidable exterior, there was a gentle quality to it, a subtle warmth that came from the fire demon hearts that now powered it.

"Be gentle with him," Ani says, her voice full of motherly concern. "And remember, he's not just a tool. He's a companion, a friend."

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
          "chave": "resources.assets:2545477",
          "nome": "The Heart of Iron",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545477
          },
          "tipo": "EventStatus",
          "descricao": "<i><color=#808080>You bear the Heart of Iron!</i></color>\n\n Allows you to raise a @level@ {1,30} Iron Golem to fight for you. Benefits from your @Physical Damage@.",
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
```


---

## The Bandit
Chave: `resources.assets:2545627` — GUID: `28d9e36f-1bfd-40e3-8fee-c835bfb470c4`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/1 - boss bandit end — SHA objeto: `96c2b0526b905988ee913ee5ce3829e35ac176f335860f49437c754a8da443b3`

### Texto original
The remaining Blood Masks, witnessing the defeat of their leader, succumb to their cowardly nature. They scatter, fleeing into the shadows of the forest. 
<br/>
Amongst their stolen plunder, you unearth your Father's leather-bound journal. Worn with age, it contains a lifetimes worth of knowledge, gained from his countless adventures across the realm. Memories flood your mind as you recall your final moments with him. 

As you stand there, thumbing through the journal, a pit of worry gnaws at your stomach. Your father would not have parted with this, his life's work, willingly, nor in sound mind.
<br/>
If what the bandit said was true, then the old Mountain King Ironheart might hold clues to your father's disappearance.

The journey to Ironheart would be a perilous path through the Forgotten Mines, veering into the remnants of a once-glorious dwarven realm. There, amidst the echoes of a bygone era, the dwarf king reigned over a kingdom fractured, its splendor lost to the corridors of time. 

The thought of this distant land and untold tales, stirs within your heart the beginnings of another adventure.

### Resultados possíveis (texto autoral)
(string vazia no asset)

### Condições e modos
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
  }
}
```


---

## The Burning Hearts of Demons
Chave: `resources.assets:2545729` — GUID: `8158bcdc-cb19-47f4-a880-f89743353cb3`
Categoria: NotInEventPool — raridade: Mythic (4) — peso relativo: 1.0
Origem: events/the animator - battle victory — SHA objeto: `eefc5b47037e57fd6fdd153df1839941dc4cf10aff09c64d5f3e774c96629d83`

### Texto original
The last of the <b><red><incr>Fire Demons</incr></red></b> roars, its wail echoing through the cavern, as it collapses, its fire extinguishing with a hiss.

With the fire demons vanquished, you can retrieve their hearts. 

### Resultados possíveis (texto autoral)
(string vazia no asset)

### Condições e modos
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
    "KeepInDeckWhenUsed": 1,
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

### Opção 1: Loot
(string vazia no asset)

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
Moving to the fallen creatures, you carefully extract the still-glowing hearts, and wrap them in a heat-resistant pouch Ani had given you.

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
          "chave": "resources.assets:2545505",
          "nome": "Burning Demon Hearts",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545505
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
```


---

## The Burning Hearts of Demons
Chave: `resources.assets:2545730` — GUID: `b25094f9-0cb0-45e2-9583-9f19f2746d3c`
Categoria: NotInEventPool — raridade: Mythic (4) — peso relativo: 1.0
Origem: events/the animator - battle — SHA objeto: `0fccd2d0789f625aeb7d30a57c4987912795eb79dcc01c59e4466b77804675e3`

### Texto original
Within a cavernous maw, the <b><red><incr>Fire Demons</incr></red></b> stand, their immense forms cut imposing figures against the flickering light. 

They are like pillars of living flame, their bodies perpetually ablaze, the air around them rippling with unbearable heat. As they move, embers flicker off their forms, drifting upwards before winking out of existence, giving the impression of a constant, fiery rain. Horns, cruel and sharp, twisted from their skulls, framing faces filled with an infernal light that burn brighter than any earthly flame.


### Resultados possíveis (texto autoral)
Will you fight?

### Condições e modos
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
    "KeepInDeckWhenUsed": 1,
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

### Opção 1: Fight
(string vazia no asset)

Condições/rolagem:
```json
{
  "condicoes": {
    "status_requeridos": [
      {
        "chave": "resources.assets:2545515",
        "nome": "The Animator - Quest Accept",
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545515
        },
        "tipo": "EventStatus",
        "descricao": "",
        "duracao": {
          "valor": 1,
          "nome": "Quest"
        },
        "status_tipo": {
          "valor": 3,
          "nome": "Quest"
        },
        "modificadores": []
      }
    ],
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
You will face this challenge as you have all others, with courage and determination.

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

Combate configurado:
```json
{
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
        "NameOverride": "Volcanus",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545226
        },
        "ForcedEnemyMods": [
          {
            "m_FileID": 0,
            "m_PathID": 2545325
          }
        ],
        "IsSuperUnique": 1
      },
      {
        "OverrideEnemyName": 1,
        "NameOverride": "Burnicus",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545226
        },
        "ForcedEnemyMods": [
          {
            "m_FileID": 0,
            "m_PathID": 2545325
          }
        ],
        "IsSuperUnique": 1
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
      "m_PathID": 2545729
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
}
```
### Opção 2: Leave
(string vazia no asset)

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
Despite your initial commitment, you can’t deny the raw power of these fire demons, and the very real possibility of your own death. 

Silently, you retreat, moving as quietly as you can back the way you came.

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

## The Dead One
Chave: `resources.assets:2545645` — GUID: `823ba17d-183e-4cc8-b159-fbbf9c59cbe6`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/9 - the dead one end — SHA objeto: `eff804a59360dc91907e34ec29c48bfcf4f979ba409a333cb64d8aa97e09e3d6`

### Texto original
In an instant that felt like an eternity, you succeed in pushing back the abyss, banishing the Dead One from the realm. The darkness recedes like a tide, and with its retreat, you feel a rush of clarity and memory flooding back into your mind. Memories, long obscured by the oppressive gloom, now take a deep breath, filling your consciousness with vivid recollections of love, joy, and adventure.

As the abyss abates, a spectral light emerges in the lingering magic, coalescing into the form of your father. There he stands, a figure both familiar and revered, his eyes no longer clouded by the mists of illness but shining with a knowing clarity. He greets you with a smile that speaks of pride and understanding.

"You have done what I could not," your father says, his voice resonant with warmth and wisdom. "You have banished the abyss from the realm, restored the memories and the light that had been lost."

He explains to you the tragic tale of the realm's leaders, how, in their fear and despair of the dragons, they had sacrificed their most cherished memories to summon the Dead One. This loss had led them astray, transforming them into lost and fallen shadows of their former selves, and with them, the realm too had fallen into darkness.

"The dragons will rise from their slumber," your father continues, "but you must face them, not with fear, but with courage. Life, with all its pain and uncertainty, is a journey worth taking. It is better to embrace the full spectrum of existence than to surrender to the abyss."

Your father's spectral form begins to fade, but the light in his eyes remain, a beacon of hope and guidance. "You have the strength to face what comes next, to rebuild and to heal. Go forth, my child, and live the life that is yours to claim."



### Resultados possíveis (texto autoral)
(string vazia no asset)

### Condições e modos
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
  }
}
```


---

## The Dusk King
Chave: `resources.assets:2545639` — GUID: `47d52f5f-01d4-48f1-8956-690e5bb2aafd`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/6 - the dusk king end — SHA objeto: `418bad022481ad9e9e3f972c1b63ec208982ab9e635ef1603efe1fb2c9f022f7`

### Texto original
In the stark silence of Frostwrought Mountain's summit, the skeletal form of the Dusk King lay defeated. The once-mighty lich, now nothing more than bones scattered in the snow.

From the fallen form of the Dusk King, a light begins to emerge, piercing the gloom of the mountain. It emanates from the king's armor, revealing a crown of pure gold, its jewels gleaming with an inner light. 

As your fingers grasp the crown, a vision envelopes you, transporting you to a time and place far removed from this icy desolation.
<br/>
You are in a grand hall, resplendent with banners and the warm glow of torchlight. Before you stands a noble king, regal and benevolent, his eyes shining with pride. The king is bestowing a great honor upon a young warrior, who kneels before him in humble reverence.

Through the eyes of the vision, you feel the overwhelming joy of a proud parent, the king witnessing his own son receiving the honor of knighthood.
<br/>
The vision fades, leaving you once again on the frozen summit, staring at the lifeless form of the Dusk King. 

Your father had indeed discovered that the cure the ancient kings had sought for the dragons had imparted a terrible curse – a solution that had brought untold suffering and transformed protectors into tormented guardians of a dark legacy.

The need to find your father is more pressing than ever.

### Resultados possíveis (texto autoral)
(string vazia no asset)

### Condições e modos
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
  }
}
```


---

## The Mad Mage
Chave: `resources.assets:2545740` — GUID: `2d96a688-b25e-409b-80c0-a1266789efeb`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/the mad mage 2 — SHA objeto: `7e81ebba8e385fe1c84d236d7da7226ddfc6ac69e9f0e8107ce8fdb40774ff43`

### Texto original
A crazed laugh fills the air, the prisoner's eyes alight with anticipation. "Good, good! Now, the next one."

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
    "requiredStatusesToSpawn": [
      {
        "m_FileID": 0,
        "m_PathID": 2545516
      }
    ],
    "allowOnAllTerrainTypes": 1,
    "allowedTerrainTypes": [],
    "allowAtAllTimesOfDay": 1,
    "allowedTimeOfDay": 0,
    "allowAtAllLevels": 0,
    "minLevel": 3,
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
  }
}
```

### Opção 1: Break
Release the prisoner from the second chain.

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
As you touch the second chain, an intense cold spreads through you, frost forming on your skin, a biting chill that gnaws at your bones. Yet you stand firm, absorbing the magic until the icy chain, too, dissipates into frosty mist.

Efeito 1 (configuração autoral, não resultado de partida):
```json
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
          "chave": "resources.assets:2545482",
          "nome": "Touch of Frost",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545482
          },
          "tipo": "EventStatus",
          "descricao": "Increases @Cold Damage@ by GetFlatDamageValue().",
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
                "chave": "resources.assets:2544367",
                "nome": "DamageFlatCold",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544367
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "ActionStatus.GetFlatDamageValue",
              "segunda_passagem": false
            }
          ]
        },
        {
          "chave": "resources.assets:2545496",
          "nome": "Frostbitten",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545496
          },
          "tipo": "EventStatus",
          "descricao": "Reduces @Cold Resistance@ by @25%@ per stack.",
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
                "chave": "resources.assets:2544495",
                "nome": "ResistCold",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544495
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "-25",
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

Evento encadeado:
```json
{
  "chave": "resources.assets:2545741",
  "nome": "The Mad Mage 3",
  "pptr": {
    "m_FileID": 0,
    "m_PathID": 2545741
  },
  "tipo": "PartyEvent"
}
```
### Opção 2: Leave
You think it's too dangerous to free him.

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
You leave wondering what crimes required such powerful bonds.

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

## The Mad Mage
Chave: `resources.assets:2545741` — GUID: `4eda9b0c-848d-472d-9036-1bcb41d2ce7b`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/the mad mage 3 — SHA objeto: `8bbbb7c165534e8ec513fb729e2a4d269ccdfb5823a005527a7d6640d3f8eeed`

### Texto original
"Yes! One more. You're almost there!" The prisoner cackles, his excitement bordering on hysteria.

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
    "requiredStatusesToSpawn": [
      {
        "m_FileID": 0,
        "m_PathID": 2545517
      }
    ],
    "allowOnAllTerrainTypes": 1,
    "allowedTerrainTypes": [],
    "allowAtAllTimesOfDay": 1,
    "allowedTimeOfDay": 0,
    "allowAtAllLevels": 0,
    "minLevel": 3,
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
  }
}
```

### Opção 1: Break
Release the prisoner from the last chain.

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

#### Ação 1: Success — RollLimit 8
You reach for the third chain. The shock hits you like a punch, sending jolts of electricity coursing through your body. You grit your teeth against the pain, absorbing the raw power, until the last chain bursts into sparks and vanishes.

"At last!" the prisoner cries, his laughter echoing across the barren landscape. "Freedom!" As the chains fall away, a storm of elements spirals around him. Fire, ice, and lightning coalesce in a swirling vortex that engulfs him. Then, just as abruptly, the elements vanish along with the prisoner, leaving you alone to ponder what you have unleashed.

Efeito 1 (configuração autoral, não resultado de partida):
```json
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
          "chave": "resources.assets:2545483",
          "nome": "Touch of Thunder",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545483
          },
          "tipo": "EventStatus",
          "descricao": "Increases @Lightning Damage@ by GetFlatDamageValue().",
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
                "chave": "resources.assets:2544370",
                "nome": "DamageFlatLightning",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544370
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "ActionStatus.GetFlatDamageValue",
              "segunda_passagem": false
            }
          ]
        },
        {
          "chave": "resources.assets:2545518",
          "nome": "Legacy of the Mad Mage",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545518
          },
          "tipo": "EventStatus",
          "descricao": "What have you unleashed upon the world?",
          "duracao": {
            "valor": 3,
            "nome": "Permanent"
          },
          "status_tipo": {
            "valor": 3,
            "nome": "Quest"
          },
          "modificadores": []
        },
        {
          "chave": "resources.assets:2545500",
          "nome": "Shocked",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545500
          },
          "tipo": "EventStatus",
          "descricao": "Reduces @Lightning Resistance@ by @25%@ per stack.",
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
                "chave": "resources.assets:2544499",
                "nome": "ResistLightning",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544499
                },
                "tipo": "CharacterAttribute"
              },
              "metodo": {
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "-25",
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
You think it's too dangerous to free him.

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
You leave wondering what crimes required such powerful bonds.

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

## The Medusa
Chave: `resources.assets:2545641` — GUID: `654654a8-fb4c-4b0a-9541-39c5f437ec90`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/7 - the medusa end — SHA objeto: `07744f17811e99570fdce3801da4f8cb1386443283969845e3dec2279dc659ed`

### Texto original
In the moment of her defeat, as if by some ancient and unfathomable magic, the Medusa turns to stone. Her form, forever captured in a tableau of anguish and rage, becomes a statue, a permanent testament to her tragic fate.

The jungle around you falls into an eerie silence, as if the very earth and sky are pausing to mourn the loss of this creature as cursed as she was fearsome.

And then a light emanates, growing in intensity, from within the statue. A jewel, brilliant and green, appears, its facets exquisitely wrought, as if by the hands of a master artisan. 
<br/>
You take the jewel and see a woman, strong and fierce, her eyes alight with the fire of leadership and the warmth of compassion. She sits upon a throne, not as a tyrant ruling with an iron fist, but as a chieftain who leads her people with care and protection. Her presence is commanding, yet there is a kindness in her demeanor, a love for her people that is palpable.

Her people look to her with respect and affection. She does not stand above them, but among them, a leader who bares the responsibility of her position not as a burden, but as a sacred duty.
<br/>
The vision fades, leaving you once again in the heart of the jungle, the stone form of the Medusa before you.

The curse that plagues this realm, turning its protectors into monsters and its beauty into peril, is a blight that you are determined to end.

### Resultados possíveis (texto autoral)
(string vazia no asset)

### Condições e modos
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
  }
}
```


---

## The Prospector
Chave: `resources.assets:2545631` — GUID: `d21cccf8-d886-4271-ac3e-da0dcf528cd0`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/2 - the prospector end — SHA objeto: `2209e8dbca9dc675c8943e8b7bd292d6728b6e7b74a2af6104c901fdad67b473`

### Texto original
The prospector's words, like ghostly whispers, dance in your mind as you gaze into the serpentine depths of the caverns, pathways to the realm of the Mountain King. What secrets had your father unraveled in these silent, stone-clad halls?

What had he discovered, unearthed from the veils of earth, that incited such betrayal and turned hearts against him? Such ponderings, like shadows, clung to your thoughts, unyielding and haunting.

### Resultados possíveis (texto autoral)
(string vazia no asset)

### Condições e modos
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
  }
}
```


---

## The runes of the Ymir
Chave: `resources.assets:2545780` — GUID: `02eff442-4bb6-4e23-b99c-07c5d74e50d3`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/ymir rune, courage - victory — SHA objeto: `18b23937f2d693f47cf239f155f0b03603c2161865fdb7c338222353d2df384f`

### Texto original
The frost wolf's cry echoes across the barren landscape as it too dissipates in ice and mist. As the frost settles, the glowing runes flickered out, and you are left standing alone in the snow.

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
  }
}
```

### Opção 1: Victory!
The lessons from the runes are etched on your heart, as clear as the markings on the ice.

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
Despite your victories, you can't help but feel a sense of anticipation, a promise of a greater challenge still to come. But for now, you savor the quiet calm that the icy landscape offers.

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
          "chave": "resources.assets:2545522",
          "nome": "Trial of the Ymir",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545522
          },
          "tipo": "EventStatus",
          "descricao": "A greater challenge looms ahead.",
          "duracao": {
            "valor": 1,
            "nome": "Quest"
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
```


---

## The runes of the Ymir
Chave: `resources.assets:2545781` — GUID: `57998f83-17c5-4e55-bf59-f56403d0ce14`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/ymir rune, courage — SHA objeto: `e5645d5282be742fa48fb0bc3ae16540909c8e48d4ec4fe41ff96e6a79658aa5`

### Texto original
A sudden gust of wind sweeps through the clearing, chilling you to the bone as the treant falls, dissolving into a whirlwind of frost.

Turning your attention back to the ancient rune, you observe it shift once more, the intricate markings dancing into a new pattern.

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
  }
}
```

### Opção 1: Touch
Reach out and place the palm of your hand on the Ice.

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
As before, you reach out and placed your palm on the ice. The cool sensation envelops you, as though you were stepping into a winter’s night. It is soothing and peaceful, a calm before the storm.

And storm it does. A howl echoes through the icy landscape, freezing you in place. From the blizzard emerges a wolf, its fur white as snow and eyes glowing like the pale moon. Blue runes trace its form, glowing brightly with arcane light.

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

Combate configurado:
```json
{
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
}
```
### Opção 2: Leave
You have no time for these ancient markings.

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
(string vazia no asset)

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

## The runes of the Ymir
Chave: `resources.assets:2545783` — GUID: `180d0256-b0b8-42bd-a0b7-d87bbcdcb874`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/ymir rune, honor — SHA objeto: `e7f6183c11b8d7eac32e68ccbcc3b127868a8bdb483e2110dd63e01632137821`

### Texto original
With a resounding cry and a final, powerful swing, you strike the final blow. The polar bear does not fall, but instead, it shatters into a whirlwind of frost, leaving nothing behind but an empty silence.


Turning back to the rune, you watch with wide eyes as it alters itself, the ancient markings transforming, shifting into a pattern unknown to you. Despite the change, the pull is still there, the rune calling out to you in a silent whisper. 

### Resultados possíveis (texto autoral)
Will you touch the Rune?

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
  }
}
```

### Opção 1: Touch
You reach out and place the palm of your hand on the Ice.

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
An icy chill runs through you, a sensation akin to the one you'd felt earlier but colder, more potent.


Just as you become lost in the sensation, a loud, thunderous sound jolts you out of your reverie. A treant, mighty and tall, its bark as ancient as the Ymir themselves, emerges from the mist, its branches crashing and rustling in a cacophony of sounds.


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

Combate configurado:
```json
{
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
}
```
### Opção 2: Leave
You have no time for these ancient markings.

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
You turn away from the Runes and walk on.

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

## The Spell Council
Chave: `resources.assets:2545747` — GUID: `bfe5418a-b839-4c4d-881a-08805a2a4310`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/the spell council - victory — SHA objeto: `83193b41bf240343108902f7a1b0ea0a3873707edb5836576a5c270bcd3673b4`

### Texto original
Just as you are catching your breath after battle, a vortex of magical energy whirls into existence before you, coalescing into the familiar form of the Mad Mage. He materializes fully, an expression of bewildered relief etched across his face. His eyes sweep the scene before landing on you, then widen in recognition.

"Is it... is it truly so?" he whispers, his voice carrying an echo of the storm that freed him. "Am I finally free of those meddlesome wizards?" A crazed laugh breaks from his lips, full of relief and disbelief. "I can hardly believe it! Free, after all this time!"

Turning to you, the Mad Mage's manic laughter subsides, replaced with an intense, scrutinizing gaze. "You have my gratitude, adventurer," he says, his tone serious for the first time. "You have done more than you know. Take this as a token of my gratitude."



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
  }
}
```

### Opção 1: Accept
Claim your reward.

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
With grand flourish, the Mad Mage conjures a radiant rune that floats down to your outstretched hand. 

It seems to be carved from an iridescent material, neither stone nor metal, yet harder than diamond and as shimmering as purest silver. It is adorned with a series of intricate glyphs and symbols that danced and pulsed with a serene, soft light.

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
```


---

## The Spell Council
Chave: `resources.assets:2545749` — GUID: `b033c3a9-ab04-4d4b-9961-d4846e25261f`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/the spell council — SHA objeto: `d82fe59b4a8c943eb3f6e0ecd900942f56d30be144e11a72d75ceb1b95d2a830`

### Texto original
You come under the heavy gaze of three formidable wizards, each adorned in robes representing their affinity for distinct elements: fire, ice, and lightning.

A remnant of the elemental chains' power pulses within you, resonating with the magical auras of the wizards. The tallest of the trio, a stern woman wreathed in an aura of flickering flames, steps forward.


"You," she declares, her voice echoing, "you have released the Mad Mage."


Caught off guard, you try to explain, to justify your actions. But the icy-eyed wizard silences you with a frost-laden hand. "You have unleashed chaos into the world," he says, his voice as chilling as his gaze. "And chaos must be subdued."


The third wizard, shrouded in an aura of crackling electricity, steps in. "You have a task, adventurer," he declares, sparks dancing around him as he speaks. "You must capture the Mad Mage and return him to his chains. He must pay for the turmoil he has caused."


"And if you fail..." The fiery wizard's voice drops, her gaze harder than a dragon's scales. "Then you will find oblivion a lenient fate compared to what we shall impose."

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
  }
}
```

### Opção 1: Agree
You will bring the Mad Mage to justice.

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
With a determined nod, you accept the charge, your resolve solidifying under the heavy gaze of the elemental wizards. You will find the Mad Mage. You will right your wrong.

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
```

### Opção 2: Oblivion 
You'll not be told what to do.

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
Surprise flits across the wizards' faces, their expressions hardening as you refuse. "You dare defy us?!" 

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

Combate configurado:
```json
{
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
}
```

---

## The Sultan
Chave: `resources.assets:2545635` — GUID: `dce2e114-c816-4ffd-a0fa-5263c0395782`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/4 - the sultan end — SHA objeto: `2e1ba7000bfa1cd347b86e8380e77aa61e76ac6f82ced8e95df3a1bd28aa2aad`

### Texto original
In a final, catastrophic moment, volatile energies tear through the Sultan, reducing him to nothing but ash.

From the remnants of the Sultan's demise, a faint light begins to emerge, growing brighter and more tangible. Out of the ashes floats an amulet, its gold shimmering with an ethereal light, untouched by the destruction that had just unfolded.

The moment your fingers touch the necklace, a rush of energy surges through you, and you are transported once more into a vivid memory that is not your own. 
<br/>
You find yourself witnessing a moment of profound intimacy and love – the Sultan, a man now unrecognizable from the tyrant you had just faced, in a tender embrace with a beautiful woman with raven-black hair. The Sultan's expression, devoid of the hardness and cruelty that had marked his face in battle, is filled with genuine affection and happiness. 

The couple seem utterly at peace, lost in their love for each other.
<br/>
As quickly as it had begun, the vision dissipates, leaving you standing in the blinding heat of Wyrmrest. With the amulet now in your possession, you turn your attention back to the path laid out in your father's journal. It beckons you onwards, towards the vast and treacherous expanse of the sea. 





### Resultados possíveis (texto autoral)
(string vazia no asset)

### Condições e modos
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
  }
}
```


---

## The Witch
Chave: `resources.assets:2545643` — GUID: `81632a77-5c59-495f-9d0d-32acca8b75cd`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/8 - the witch end — SHA objeto: `135b83d9c1d25f75dfbc430a862e81323f8538cb03c3e732cd000e9e542c67db`

### Texto original
The Witch's form, once a vessel of corruption and malevolence, begins to dissolve. Her cruel visage, twisted by years of darkness, bubbles and melts into the swamp itself, as if the land is reclaiming a part of its lost self. The foul air and the murky waters around her seeth and churn, swallowing the remnants of her existence.

From the dissipating form of the Witch, a light rises, pure and cleansing. It swirls amidst the foul miasma of the swamp, a beacon of hope in the heart of despair. Encased within this light is a simple object, starkly out of place in the grim surroundings – a child's teddy bear, worn by time but still holding the echoes of innocence and care.

You reach out and take the bear. As your fingers brush against its fabric, a vision envelopes you, transporting you to a time and place far removed from the decay of the swamp.
<br/>
You find yourself in a forest at night, a world away from the corruption you have just witnessed. Above, the stars shine brightly, their light filtering through the canopy to dance upon the forest floor. The air is alive with the sound of crickets and the gentle movement of fireflies, a symphony of the night.

There, in a clearing, lays a young girl, the Witch in her innocent youth, curled up beside her pet wolf. Both sleep peacefully, nestled together for warmth under the starlit sky. The girl, a caretaker of the forest, is at home in this natural haven, her heart intertwined with the life around her. The vision is a glimpse into a past untainted by darkness, a time of innocence and harmony.
<br/>
As the vision fades, you are brought back to the grim reality of the Sunken Swamp. The beautiful forest of the vision is now the stinking bog that surrounds you, a bleak reminder of the transformation wrought by the curse.

With the child's bear in hand, the final relic mentioned in your father's journal, you know that your quest is nearing its end. You have gathered the artifacts, each a key to understanding the depth of the curse that had befallen the realm.

Now, all that remains is to retrace the last steps of your father, to follow the path that would lead him to the looming Castle Gloom.



### Resultados possíveis (texto autoral)
(string vazia no asset)

### Condições e modos
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
  }
}
```


---

## Too Late
Chave: `resources.assets:2545647` — GUID: `555fe1d0-e62f-420b-9ce6-cb66f38a2ce1`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/9 - too late — SHA objeto: `71cd19b829d1d9bc3107ce9c6670daf9e60c6c11d14d226fba64e7764f5e6144`

### Texto original
As you recognize the ensnared spirit, a deep sorrow engulfs your heart. The realization dawns – You are too late. You failed to save your father.

Your father’s ghost comforts you.

“Hold no sorrow. You are blameless. It was the ailment's doing. I perished in pursuit of my passion, and now, with your arrival, you can finish what I started.”

Even as your father harbors no resentment, a tide of guilt washes over you for leaving him behind. Lingering thoughts haunt you – would he yet draw breath had you never strayed from his side?

Your father's voice cleaves through the fog of your sorrow, anchoring you back to the present.

"As you delve deeper into the castle's heart, the darkness will begin to cloud your mind, a fog that dulls the senses and fills your thoughts with whispers of doubt and despair."

"Grasp tightly the memories you've gathered. The Dead One wields no dominion over the echoes you hold."



### Resultados possíveis (texto autoral)
(string vazia no asset)

### Condições e modos
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
  }
}
```


---

## Treasure of Moltendunn
Chave: `resources.assets:2545760` — GUID: `2f8ff63f-f021-4dc6-b13c-b928121964c1`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/treasure of moltendunn 1 — SHA objeto: `e9c638da30b968037c5c9a31114996b97ebb681627b4c4b8608b06d71ce4c568`

### Texto original
Spurred on by the promise of the legendary Treasure of Moltendunn, you make your way through the terrain outlined on the map. After many trials and tests of wit and skill, you find yourself standing before a sight that makes your heart pound - a chest, half buried in the sand, its glinting lock winking at you in the light.

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
  }
}
```

### Opção 1: Dig
Uncover the treasure.

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
(string vazia no asset)

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

Evento encadeado:
```json
{
  "chave": "resources.assets:2545761",
  "nome": "Treasure of Moltendunn 2",
  "pptr": {
    "m_FileID": 0,
    "m_PathID": 2545761
  },
  "tipo": "PartyEvent"
}
```
### Opção 2: Leave
You have second thoughts about the hunt.

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


---

## Treasure of Moltendunn
Chave: `resources.assets:2545761` — GUID: `96252be8-6f1a-4c87-ab16-258d31eaa501`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/treasure of moltendunn 2 — SHA objeto: `3733eb38682d5c322a9f9ed6664ea9120c24a40ef55736eb4cd4e9fb1612f62b`

### Texto original
Without hesitation, you set to work, your fingers scrabbling through the sand to uncover the rest of the chest. Yet, the more you dig, the deeper the chest sinks, like it is being swallowed by the earth itself. Rocks and dirt fall from the sides of the hole, the ground shifting and groaning beneath your weight.

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
  }
}
```

### Opção 1: Dig
You dig even faster unwilling to let the treasure go.

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

#### Ação 1: Success — RollLimit 8
As you dig faster, you notice the ground isn't merely sinking - it is churning, as if caught in the gears of some vast machinery. Fear ripples through you, a sense of dread settling like a stone in your stomach. This isn't a mere chest buried in the sand. It is a trap.

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

Evento encadeado:
```json
{
  "chave": "resources.assets:2545763",
  "nome": "Treasure of Moltendunn 4",
  "pptr": {
    "m_FileID": 0,
    "m_PathID": 2545763
  },
  "tipo": "PartyEvent"
}
```
#### Ação 2: Failure — RollLimit 0
The more you dig, the faster the chest sinks. Rocks and debris batter you, adding to your growing exhaustion. Your strength wanes, your endurance tested to its limits. Your heart pounds in your chest, and sweat streams down your face, mixing with the sand and dust.

Efeito 1 (configuração autoral, não resultado de partida):
```json
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
```

Evento encadeado:
```json
{
  "chave": "resources.assets:2545762",
  "nome": "Treasure of Moltendunn 3",
  "pptr": {
    "m_FileID": 0,
    "m_PathID": 2545762
  },
  "tipo": "PartyEvent"
}
```
### Opção 2: Give Up
(string vazia no asset)

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


---

## Treasure of Moltendunn
Chave: `resources.assets:2545762` — GUID: `11d0a54b-fb4e-4e63-b6ac-1fb07d03f3c2`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/treasure of moltendunn 3 — SHA objeto: `0b86721095ef55e12764d85730d24764af5420d863d9f3748cae39558a9baff8`

### Texto original
It is a cruel trap, a relentless mechanical nightmare designed to thwart any who seeks the Treasure of Moltendunn. Frustration and determination battle within you, each demanding control. Will you succumb to the ceaseless pull of the earth, or can you outwit the ancient machinery and seize the treasure you have sought? 

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
  }
}
```

### Opção 1: Dig
You dig even faster unwilling to let the treasure go.

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

#### Ação 1: Success — RollLimit 8
You notice the glint of metal beneath the dirt. You brush the soil away, revealing a network of gears and cogs, spinning and whirling, pulling the chest further into the ground. The trap is intricate, designed to ensnare greedy treasure hunters who acted without thinking.

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

Evento encadeado:
```json
{
  "chave": "resources.assets:2545763",
  "nome": "Treasure of Moltendunn 4",
  "pptr": {
    "m_FileID": 0,
    "m_PathID": 2545763
  },
  "tipo": "PartyEvent"
}
```
#### Ação 2: Failure — RollLimit 0
Rocks and debris batter you, adding to your growing exhaustion. Your strength wanes, your endurance tested to its limits. Your heart pounds in your chest, and sweat streams down your face, mixing with the sand and dust.

Efeito 1 (configuração autoral, não resultado de partida):
```json
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
```

Evento encadeado:
```json
{
  "chave": "resources.assets:2545762",
  "nome": "Treasure of Moltendunn 3",
  "pptr": {
    "m_FileID": 0,
    "m_PathID": 2545762
  },
  "tipo": "PartyEvent"
}
```
### Opção 2: Give Up
Despite your new find you won't risk being buried alive.

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


---

## Treasure of Moltendunn
Chave: `resources.assets:2545763` — GUID: `085d4df2-878c-4979-a83f-7aeea9d034ec`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/treasure of moltendunn 4 — SHA objeto: `8d3e8db487d595f7196b4a303d2808e7975f4728567924668aebf42b338e1d0b`

### Texto original
You'll need to disarm the trap, to stop the machinery that is swallowing the chest. You scan the arrangement of gears, your mind racing to decipher their purpose and function.

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
  }
}
```

### Opção 1: Disarm
Your mind races thinking of ways to stop the trap.

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

#### Ação 1: Success — RollLimit 8
Noticing a main cog that seems to be driving the rest, you draw your weapon, wedging it into the intricate web of spinning gears. With a final, heaving push, you jam the cog, grinding the machinery to a halt. The sinking ceases, the chest frozen in its descent.

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

Evento encadeado:
```json
{
  "chave": "resources.assets:2545764",
  "nome": "Treasure of Moltendunn 5",
  "pptr": {
    "m_FileID": 0,
    "m_PathID": 2545764
  },
  "tipo": "PartyEvent"
}
```
#### Ação 2: Failure — RollLimit 0
Rocks and debris batter you, adding to your growing exhaustion. Your strength wanes, your endurance tested to its limits. Your heart pounds in your chest, and sweat streams down your face, mixing with the sand and dust.

Evento encadeado:
```json
{
  "chave": "resources.assets:2545762",
  "nome": "Treasure of Moltendunn 3",
  "pptr": {
    "m_FileID": 0,
    "m_PathID": 2545762
  },
  "tipo": "PartyEvent"
}
```
### Opção 2: Give Up
(string vazia no asset)

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


---

## Treasure of Moltendunn
Chave: `resources.assets:2545764` — GUID: `38383f9f-e2b6-4b4c-abb3-5fb1a688e046`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/treasure of moltendunn 5 — SHA objeto: `c63984d0bb3c23391bd6bb34ac253de6487165f4d4c0955d92a5807ddf99779c`

### Texto original
Breathing hard, you turn your attention back to the chest. You've won this round, but the Treasure of Moltendunn has already proved itself to be as treacherous as it is tempting. With newfound caution, you reach out to open the chest

### Resultados possíveis (texto autoral)
What treasure will you take?

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
  }
}
```

### Opção 1: Dragon Claw Talisman
The strange item sparkles with embers.

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
A petrified claw of a red dragon whelp, ancient yet perfectly preserved. Its fiery hue is frozen in time, the rough texture a stark contrast against the smooth, cold interior of the chest.

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
```

### Opção 2: Phoenix Feather
The dull gray feather looks withered and lifeless.

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
As your fingers brush against the feather, it disintegrates into ashes, leaving nothing but soot on your fingers. Yet, in the blink of an eye, the ashes coalesce into a brilliant fiery orange in a flash of flame. The feather, reborn from its own ashes, pulses with energy, a testament to the power of rebirth and resilience.

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
```

### Opção 3: Oculus Gem
The gem swirls with magical energy.

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
As your fingers come into contact with it, the gem vanishes. Startled, you feel a weight in your pocket. Reaching in, you find the gem, it had teleported away from your hand and into your pocket, as if it has a mind of its own.

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
```


---

## Trial of the Ymir
Chave: `resources.assets:2545765` — GUID: `3847efc5-47dd-4913-b33c-16eedc922228`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/trial of the ymir - victory — SHA objeto: `f306ad503ae04760a32877a5e3f925560f79331526860ea2ce8edbfcbc5ee715`

### Texto original
The frost giant roars in defeat, his gaze locked onto you. He had not been defeated - rather, he has chosen to yield.


"You have proven your worth, Rune Conqueror," the frost giant admits, a note of admiration in his booming voice. "You have shown strength, upheld your honor, and faced this trial with unyielding courage."

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
  }
}
```

### Opção 1: Accept
Receive the Might of Ymir.

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
A surge of strength unlike anything you've ever felt before floods your frame, infusing your body with a power that is ancient and mighty.


"You are now blessed with the Might of the Ymir, a testament to your victory here today. Carry it with you, Rune Conqueror, and let it guide your path."

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
```


---

## Trial of the Ymir
Chave: `resources.assets:2545766` — GUID: `a2a6b0b1-aaa0-41e4-8d9d-0caa21fb8380`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/trial of the ymir — SHA objeto: `f156abf50f3366dc9cf6cfd43212803a25deeaeff22101d3d24baed9f1462cda`

### Texto original
As you approach the giant, your gaze wanders over the towering figure. The <b><blue><incr>Frost Giant</incr></blue></b> is a creature of majesty and power, a child of the Ymir as ancient as the icy landscapes he traverses. His skin shimmers like fresh ice under the glow of the northern lights, radiating a cold, ethereal beauty that leaves you in awe.


"<blue>Well met, Rune Conqueror,</blue>" the giant's voice echoes around you, a glacial rumble that sends vibrations coursing through the snow underfoot. His icy-blue eyes bores into you, a glimmer of respect evident in their frost-rimed depths.


"<blue>You carry the mark of our kin. The runes you carry are not simple magic but the embodiment of Ymir's principles: strength, honor, and courage. You have come far, and have been tested, but the greatest trial lies ahead,</blue>" the giant proclaims, his voice echoing amidst the cold mountains.

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
  }
}
```

### Opção 1: Accept
You are ready.

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
"<blue>Very well, Rune Conqueror. Show us your strength, uphold your honor, and let your courage guide you. For you face now not just a trial, but a rite of passage. Triumph, and earn the blessings of the Ymir.</blue>"

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

Combate configurado:
```json
{
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
}
```
### Opção 2: Decline
This trial proves too much for you.

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
The sight of the towering giant gives you pause.

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

## Unholy Experiments
Chave: `resources.assets:2545570` — GUID: `603a0843-ebb3-426f-9500-86812ad6d1d7`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/dark discoveries - battle — SHA objeto: `73e01b63220dc3c78aee878f54fae87bf9d0838c4e4e6f1d6f1644b86c8c4639`

### Texto original
These wretched <blue><b><incr>Abominations</incr></b></blue>, swollen with the tormented souls of the damned, exuded a putrid odor that assaults the senses, a nauseating blend of decay and malevolence.

As you draw near, the foul stench grows stronger, a physical manifestation of the abominations' unholy nature. It permeates the air, clinging to your clothes and filling your nostrils with a sickening mixture of rot and despair.

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
  }
}
```

### Opção 1: Fight
Rid the realm of these terrible <blue><b>Abominations</b></blue>.

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
(string vazia no asset)

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

Combate configurado:
```json
{
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
}
```
### Opção 2: Flee
Abandon this quest and flee.

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
The putrid smell unlocks a primal fear deep within you. You turn away, abandoning this ill-fated quest.

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

## Unleashed
Chave: `resources.assets:2545768` — GUID: `af493a35-ca03-4351-933f-cc688f2cd56e`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/unleashed - victory — SHA objeto: `ad86c39885474ab16799867ba1e34de80443ff4cb203de2f0b7e3b3e9ce99cc2`

### Texto original
In the face of your relentless onslaught, the Mad Mage overreaches, drawing too deeply from his own wellspring of power. His laughter turns into a scream as his own magic consumes him, the elemental tempest reaching a climax and then suddenly imploding, a violent silence replacing the chaos. When the dust and steam clear, the Mad Mage is gone, his body reduced to ashes by his own elemental might.

In the midst of the smoldering remains, a single object catches your eye: a worn, leather-bound book, untouched by the elemental fury that had consumed its master. 

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
  }
}
```

### Opção 1: Reward
Take the spellbook for yourself.

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
Cautiously, you pick it up. The cover reads: 'Expeditions in Elemental Equilibrium by Jason the Devastatingly Sane.'

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
```


---

## Unleashed
Chave: `resources.assets:2545769` — GUID: `a7de4c70-7f15-486f-aa7e-40c71c190d9f`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/unleashed — SHA objeto: `31bd7f9bf0345f6217f887d93d36521fb14fcea923ea333a139be91cec2f35f9`

### Texto original
After what feels like an eternity, you find him. The <violet><b><incr>Mad Mage</incr></b></violet> stands at the heart of a whirling tempest of raw elemental power. Fire, ice, and lightning cascade off him in radiant waves, painting a terrifying tableau against the sky. As you approach, the Mad Mage turns, a warm smile stretching across his gaunt face.


"If it isn't my liberator," he says calmly, stepping forward. His gaze is as wild as the swirling elements around him. "Tell me, have you come to wish me well in my freedom, or have you grown to fear what you cannot control?"

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
  }
}
```

### Opção 1: Fight
You must stop the chaos he brings.

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
"Ah, so it is," the Mad Mage sighs, the tempest of elements around him briefly subsiding. "It's a pity, my liberator. I had hoped you were different."


A silence falls between you, the only sound the crackling of fire, the drip of melting ice, and the low hum of electricity. The disappointment in the Mad Mage's voice echoes in your ears. But then, the silence is broken as the Mad Mage's expression hardens, his eyes flaring with newfound determination.


"No more!" he thunders, his voice echoing across the landscape. "No more chains! Your ignorance, your fear... it will be your downfall!"

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

Combate configurado:
```json
{
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
}
```

---

## What Lurks
Chave: `resources.assets:2545772` — GUID: `927680ab-1141-4524-a714-e418cac289f2`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/what lurks - victory — SHA objeto: `d661c103dc5da99074b4ef41d054321d6666b6cdeb2b561364de5b3abfceabf8`

### Texto original
With a final shudder, the <b><green><incr>Anthulk</incr></green></b> collapses, its life force draining away into the desert sand. Panting, your eyes fall on the massive claw. It still oozes venom, the lethal toxin gleaming wickedly in the sun.

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
  }
}
```

### Opção 1: Take
Take the venomous claw of the Anthulk.

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
With effort, you pry the claw from the beast's lifeless grip, its size and weight substantial even in your strong hands. The venom can make your weapons more lethal, a crucial edge in the unpredictable life of an adventurer. 

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
```


---

## Witch's Pyre
Chave: `resources.assets:2545775` — GUID: `526e30e7-0f03-4409-bb34-35c81045b0aa`
Categoria: NotInEventPool — raridade: Rare (2) — peso relativo: 1.0
Origem: events/witch's pyre - victory — SHA objeto: `e1f1da5da50b553bc66b9021904391f277ed796cd2cb66f220b9cff83ab54f07`

### Texto original
<b><incr><red>The Risen Witch</red></incr></b> stumbles backwards, a look of disbelief on her face. With a final, desperate incantation, the flames that had failed to consume her on the pyre came to life around her once again.


The inferno surges upwards, consuming the witch in a brilliant spectacle of destruction. Her shriek echoes through the night, a sound of profound agony that sends a chill running down your spine.

Among the ashes, you find a scroll, seemingly untouched by the flames. A bloody handprint stains the parchment, a grotesque seal that marks the dark contract that had granted the witch her powers.

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
  }
}
```

### Opção 1: Take
Retrieve the blood-stained contract.

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
(string vazia no asset)

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
```


---

## Ymir Rune, Honor
Chave: `resources.assets:2545782` — GUID: `e826b457-4b55-46db-bd38-0f9239a0b915`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/ymir rune, honor - victory — SHA objeto: `58beff0baea8d9b1663cfe489191d6ec8cd6edd1d5c0d76cc835b748393fb66f`

### Texto original
You have defeated the <gold><b><incr>Trial of Honor</gold></b></incr>! 


### Resultados possíveis (texto autoral)
(string vazia no asset)

### Condições e modos
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
  }
}
```

### Opção 1: Claim
Take the rune.

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
Greater honor has given you greater conviction.


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
```


---

## Ymir Rune, Strength
Chave: `resources.assets:2545784` — GUID: `3e15219a-3607-4fe4-ae6f-3fc421135fcb`
Categoria: NotInEventPool — raridade: Common (0) — peso relativo: 1.0
Origem: events/ymir rune, strength - victory — SHA objeto: `525e0bbea0c4dd6f2f2c33b39e36882a4ab9b94b175f69fc36504cfbd7eebdb5`

### Texto original
You have defeated the <gold><b><incr>Trial of Strength</gold></b></incr>! 


### Resultados possíveis (texto autoral)
(string vazia no asset)

### Condições e modos
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
  }
}
```

### Opção 1: Claim
Take the rune.

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
The strength to conquer swells within you.


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
```

Evento encadeado:
```json
{
  "chave": "resources.assets:2545783",
  "nome": "Ymir Rune, Honor",
  "pptr": {
    "m_FileID": 0,
    "m_PathID": 2545783
  },
  "tipo": "PartyEvent"
}
```
