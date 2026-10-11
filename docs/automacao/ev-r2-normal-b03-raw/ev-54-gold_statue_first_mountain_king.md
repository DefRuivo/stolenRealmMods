## Gold Statue of the First Mountain King
Chave: `resources.assets:2545601` — GUID: `a93098ef-da50-40e2-a216-4b0f4e258fda`
Categoria: Normal — raridade: Mythic (4) — peso relativo: 1.0
Origem: events/gold statue of the first mountain king — SHA objeto: `1fbfa5e7f19f8df65be36dee00d47356bd2b33dbcc9595c4e2dec7e08f17e74a`

### Texto original
A statue, towering and grand, gleams with a lustre untouched by time. The magnificent statue, cast from pure gold, is a testament to the great skill and artistry of the dwarves. It is a glorious depiction of the <gold>First Mountain King</gold>, a legendary figure who laid the foundation for the dwarven kingdom.


You stand in awe, your gaze drawn to the intricately detailed armor, the steadfast expression, and the hefty hammers held firmly in the king's grip. The temptation of the golden figure is potent - it is a treasure that could secure fortunes, a prize that could change your life.

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
    "allowedTerrainTypes": [
      4
    ],
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

### Opção 1: Steal
Give into temptation and take what you can.

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
You set about your dubious task and begin to pry loose the most valuable parts. 

Your efforts, however, do not go unnoticed. A gruff voice calls out, and dwarf guards, armed and armored, emerge from the shadows. The stern face under the helmet showed no surprise, only grim determination.

You pause awkwardly, tools poised mid-air, as the dwarf strides forward. "Ye dare desecrate the likeness of our first king!" he bellows, brandishing his axe menacingly. "Prepare to meet your end, robbers!"

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
          "m_PathID": 2545080
        },
        "ForcedEnemyMods": [],
        "IsSuperUnique": 1
      },
      {
        "OverrideEnemyName": 0,
        "NameOverride": "",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545081
        },
        "ForcedEnemyMods": [],
        "IsSuperUnique": 1
      }
    ],
    "EnemyModApplications": [],
    "EnemyStatusApplications": [],
    "FillOutBattlePoints": 1,
    "OverrideBattlePoints": 0,
    "BattlePointValue": 8,
    "OverrideEnemyGroupPool": 1,
    "EnemyGroupPool": [
      30
    ],
    "OverrideEnemyTypePool": 0,
    "EnemyTypePool": [],
    "VictoryEvent": {
      "m_FileID": 0,
      "m_PathID": 2545600
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
You can't bring yourself to destroy this monument, the essence of a rich and proud dwarven culture.

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

