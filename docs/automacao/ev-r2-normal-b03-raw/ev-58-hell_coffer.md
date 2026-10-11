## Hell Coffer
Chave: `resources.assets:2545606` — GUID: `f41a780b-f4aa-455c-b26f-895129f63261`
Categoria: Normal — raridade: Mythic (4) — peso relativo: 1.0
Origem: events/hell coffer — SHA objeto: `f1803712ec88905b8075eee409b77ba21f335d9142ee90dbbf24592222c64aca`

### Texto original
Suspended above a stone pedestal is a <red><b><incr>Hell Coffer</red></b></incr>, an object of legend and fear. Encrusted with jagged obsidian and adorned with runes glowing as though forged in hellfire, the coffer is an infernal masterpiece.

The stories whisper of such artifacts, constructs of the demonic realms where damned lords store their most precious possessions. The promise of the treasure it holds is an intoxicating allure to any mortal. Yet, it is a lure designed to ensnare the greedy and unwary, drawing them into a pact with powers they could hardly fathom.

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
    "allowOnAllTerrainTypes": 0,
    "allowedTerrainTypes": [
      5
    ],
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

### Opção 1: Open
Attempt to loot the Hell Coffer.

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
You reach out and tentatively touch the surface of the Coffer.

The reaction is instantaneous. The coffer begins to spin, its dark light intensifying. From its depths, the damned rise, figures of pure flame and fury. Their cries of rage and hatred fill your mind, echoing out across the emberlands. You find yourself surrounded, the fiery figures advancing, their intentions clear and deadly.

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
      "tabelas": [],
      "restricoes": {
        "limitItemTypes": 0,
        "possibleItemTypes": [
          1,
          2,
          3
        ],
        "limitItemRarities": 0,
        "possibleRarities": [
          1,
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

Combate configurado:
```json
{
  "iniciar": true,
  "manual": false,
  "referencia": {
    "chave": "resources.assets:2544646",
    "nome": "Gold Statue of the First Mountain King Battle",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2544646
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
          "m_PathID": 2545247
        },
        "ForcedEnemyMods": [],
        "IsSuperUnique": 1
      },
      {
        "OverrideEnemyName": 0,
        "NameOverride": "",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545249
        },
        "ForcedEnemyMods": [],
        "IsSuperUnique": 1
      },
      {
        "OverrideEnemyName": 0,
        "NameOverride": "",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545250
        },
        "ForcedEnemyMods": [],
        "IsSuperUnique": 1
      },
      {
        "OverrideEnemyName": 0,
        "NameOverride": "",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545251
        },
        "ForcedEnemyMods": [],
        "IsSuperUnique": 0
      },
      {
        "OverrideEnemyName": 0,
        "NameOverride": "",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545251
        },
        "ForcedEnemyMods": [],
        "IsSuperUnique": 0
      },
      {
        "OverrideEnemyName": 0,
        "NameOverride": "",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545251
        },
        "ForcedEnemyMods": [],
        "IsSuperUnique": 0
      },
      {
        "OverrideEnemyName": 0,
        "NameOverride": "",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545251
        },
        "ForcedEnemyMods": [],
        "IsSuperUnique": 0
      }
    ],
    "EnemyModApplications": [],
    "EnemyStatusApplications": [],
    "FillOutBattlePoints": 1,
    "OverrideBattlePoints": 0,
    "BattlePointValue": 8,
    "OverrideEnemyGroupPool": 1,
    "EnemyGroupPool": [
      29
    ],
    "OverrideEnemyTypePool": 0,
    "EnemyTypePool": [],
    "VictoryEvent": {
      "m_FileID": 0,
      "m_PathID": 2545605
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
Think better of falling for this devlish trap.

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
Survival is a treasure far more precious than any gem, and to risk your life for mere riches, you knew, was a fool's gamble.


---

