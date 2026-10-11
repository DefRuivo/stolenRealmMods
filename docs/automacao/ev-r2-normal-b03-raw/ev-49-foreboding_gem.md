## Foreboding Gem
Chave: `resources.assets:2545595` — GUID: `e4dc06e1-2425-4578-9cd7-087d78eb0d18`
Categoria: Normal — raridade: Common (0) — peso relativo: 1.0
Origem: events/foreboding gem — SHA objeto: `29d4e6dd01286594affbb4420e4af66f313016e908f282c47fefbcff9a094d75`

### Texto original
This cave, previously draped in a sullen darkness, comes alive in a feverish light. The source of this illumination is a <red><b><incr>Giant Ruby</incr></b></red>, its radiant glow throwing a surreal dance of shadows on the stone walls. This gem is unlike any you had seen before, a pulsating heart in the belly of the earth, casting an allure that is both mesmerizing and disconcerting.

It lays nestled atop a rock pedestal, its facets catching the light and fracturing it into a thousand crimson shards. You find yourself drawn to it, enraptured by its brilliance, your gaze reflected in its fiery depths.

As you venture closer, your steps echo in the cavernous silence, you notice you are not alone. Other shadows move around you, dancing in the ruby's glow, creeping closer. Other adventurers, driven by the same allure, the same pursuit.

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
      4
    ],
    "allowAtAllTimesOfDay": 1,
    "allowedTimeOfDay": 1,
    "allowAtAllLevels": 1,
    "minLevel": 1,
    "terrainTypesAllowedAtAnyTime": [
      4
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
Grab the ruby before someone else does.

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
A race begins, a frantic dash towards the tantalizing gem, a clash of desires igniting into a fierce competition. 

Once an object of mesmerizing beauty, the ruby becomes an ominous beacon, driving your opponents to madness. Their eyes glow with a dangerous light, a reflection of the gem's eerie illumination.

The serene atmosphere of the cavern is soon replaced with the sound of steel, the cries of battle, the frenzied desperation to reach the ruby first.


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
    "OverrideBattlePoints": 1,
    "BattlePointValue": 16,
    "OverrideEnemyGroupPool": 1,
    "EnemyGroupPool": [
      22,
      37,
      38,
      39,
      40
    ],
    "OverrideEnemyTypePool": 0,
    "EnemyTypePool": [],
    "VictoryEvent": {
      "m_FileID": 0,
      "m_PathID": 2545594
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
}
```
### Opção 2: Leave
Pull yourself away from the allure of the ruby.

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
You feel the ruby's call, a whisper in the back of your mind, an urging to step forward and claim it.


Your gaze lingers on the gem, but you hold your ground, choosing caution over temptation.

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

