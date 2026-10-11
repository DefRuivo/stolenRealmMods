## Enchanted Pumpkin Patch
Chave: `resources.assets:2545587` — GUID: `3bda807e-075d-45e3-afe7-b9d0f9d4b34c`
Categoria: Normal — raridade: Common (0) — peso relativo: 1.0
Origem: events/enchanted pumpkin patch — SHA objeto: `f31efea298e25649e5a4700a97cb56f42ac5aeb5ada90c0ecf3731e776c3eb00`

### Texto original
You stumble upon an unlikely sight: an <orange><b><incr>Enchanted Pumpkin Patch</incr></b></orange>, nestled amidst the wilderness. Vibrant pumpkins of all sizes dot the landscape, their rich orange hue glow like embers in the creeping shadows. At the heart of the patch, keeping a silent vigil, stands a towering scarecrow.

Its form is grotesquely exaggerated, angular and ominous under the light, its eyes twin points of baleful luminescence in its shadowed face. Despite its ghastly appearance, a strange, palpable magic thrums in the air around it, tying it to the very life force of the pumpkin patch.



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
    "allowAtAllLevels": 0,
    "minLevel": 3,
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
Reach down and take a <orange><b><incr>Pumpkin</incr></b></orange>.

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
As you reach out to pluck a particularly large pumpkin, a sudden grip, cold and iron-hard, seizes your shoulder. You spin around, coming face to face with the scarecrow. Its eyes now blaze with an unnatural light, the silent guardian brought to life.

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
      "m_PathID": 2545586
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
As enticing as it seems, some treasures are not meant to be taken.

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
A sense of unease lingers in the air, the silence of the scarecrow's ominous presence. You leave the enchanted pumpkins behind.

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

