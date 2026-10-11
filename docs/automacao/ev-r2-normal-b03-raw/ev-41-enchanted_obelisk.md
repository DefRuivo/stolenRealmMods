## Enchanted Obelisk
Chave: `resources.assets:2545585` — GUID: `36c51484-b50b-4627-a9a7-64d221a22f1a`
Categoria: Normal — raridade: Common (0) — peso relativo: 1.0
Origem: events/enchanted obelisk — SHA objeto: `bb1c733ab8dd48a07f5c6a8f0e67e355eeab059af353513444b732d8f20b4773`

### Texto original
Rising from the earth like the tooth of some gargantuan beast, an obelisk crafted entirely from limestone, ancient and weathered stands proud and defiant. 

Upon the weather-beaten stone, a single white rune is etched, glowing softly in the dying light of the day. Its luminescence pulsing gently, in rhythm with the heart of the world. Even from a distance, you can sense its potent magic, a beacon drawing you towards it.

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
      2
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

### Opção 1: Activate the blessing
Press the palm of your hand upon the obelisk.

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
[name] extends [his] hand, [his] fingertips barely brushing against the cool, rugged surface. Instantly, a pulse of energy courses through [him], [his] minds expanding, their senses sharpening. A sudden clarity washes over [him], like a veil lifting from their eyes. 

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
          "chave": "resources.assets:2545415",
          "nome": "Brilliance",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545415
          },
          "tipo": "EventStatus",
          "descricao": "@Intelligence@ increased by {4,20}.",
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
              "expressao": "{4,20}",
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

### Opção 2: Heal from the obelisk
Draw the energy from the limestone obelisk.

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
[name] extends [his] hand, [his] fingertips barely brushing against the cool, rugged surface. The magic flows into [him], warm and invigorating. [his] wounds knit together, [his] fatigue washed away like dust in the rain. Each pulse of the rune is a surge of revitalization, a surge of healing energy that left [him] standing taller, [his] body whole and [his] spirit unbroken.

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


---

