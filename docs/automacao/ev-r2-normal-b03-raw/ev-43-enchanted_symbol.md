## Enchanted Symbol
Chave: `resources.assets:2545588` — GUID: `51200c46-6ca9-4e5e-b68d-ee6424dee157`
Categoria: Normal — raridade: Common (0) — peso relativo: 1.0
Origem: events/enchanted symbol — SHA objeto: `e508ca5622b66018a7cf3fade82e758bc934fd2abe87637ef10ed575673f8a51`

### Texto original



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
    "allowedTerrainTypes": [
      2
    ],
    "allowAtAllTimesOfDay": 1,
    "allowedTimeOfDay": 0,
    "allowAtAllLevels": 1,
    "minLevel": 1,
    "terrainTypesAllowedAtAnyTime": [],
    "KeepInDeckWhenUsed": 0,
    "isLesserEvent": 1,
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
    "valor": 2,
    "nome": "Both"
  },
  "full_release": {
    "valor": 0,
    "nome": "None"
  }
}
```

### Opção 1: Activate
Grants [o1a1_status].

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
          "chave": "resources.assets:2545387",
          "nome": "Intelligence",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545387
          },
          "tipo": "EventStatus",
          "descricao": "Intelligence increased by [0].",
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
                "valor": 0,
                "nome": "Base"
              },
              "expressao": "Mathf.Round(1f+(0.2f*IslandLevel))",
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

