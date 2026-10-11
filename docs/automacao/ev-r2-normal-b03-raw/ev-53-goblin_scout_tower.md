## Goblin Scout Tower
Chave: `resources.assets:2545599` — GUID: `a443b122-b3e5-4f42-b4b0-bd74a648d40d`
Categoria: Normal — raridade: Common (0) — peso relativo: 1.0
Origem: events/goblin scout tower — SHA objeto: `f7f106030888328f5e0db7a89bfd7dc09d12e3d753d3b3a21f696bed6c34103c`

### Texto original
High above on a weathered timber tower, stands the solitary figure of a <green><incr><b>Goblin Ranger</b></incr></green>. His keen eyes scan the horizon with relentless vigilance, as his hand rests lightly on a bone horn that will, undoubtedly, summon hordes of goblins if it were to sound.

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
      1,
      2
    ],
    "allowAtAllTimesOfDay": 1,
    "allowedTimeOfDay": 0,
    "allowAtAllLevels": 0,
    "minLevel": 3,
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

### Opção 1: Strike silently
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
    "bonus": [
      {
        "valor": 1,
        "nome": "Dexterity"
      }
    ],
    "misteriosa": false,
    "texto_misterioso": ""
  }
}
```

#### Ação 1: Success — RollLimit 12
With an expert hand, [name] strikes at the Goblin from a distance. [His] breath stills, and for a moment, time seems to slow. [He] watches in silence, understanding the gravity of this shot.

It cuts through the still night air like a predator, racing towards its target. The goblin, ever watchful, turns at its soft whistling, his eyes widening in surprise.

But it is too late. [name] hits [his] mark, and with a muffled thud, the goblin collapses. 

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
    "override": true,
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

#### Ação 2: Failure — RollLimit 1
With an expert hand, [name] strikes at the Goblin from a distance. [His] breath stills, and for a moment, time seems to slow. [He] watches in silence, understanding the gravity of this shot.

It whistles, a thin, desperate sound that echoes in quietly, but veeres wide, missing its target.

The goblin, alert to the danger, spins around, his eyes catching the flash of the arrow as it skitters harmlessly off the wood of the tower. His wide-eyed surprise quickly turns into alarm, his hands darting to the bone horn at his side.


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
    "ForcedEnemies": [
      {
        "OverrideEnemyName": 1,
        "NameOverride": "Goblin Ranger",
        "CharacterInfo": {
          "m_FileID": 0,
          "m_PathID": 2545104
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
      12
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
}
```

---

