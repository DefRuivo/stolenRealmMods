## Entangled Boar
Chave: `resources.assets:2545589` — GUID: `ad2b9f6c-46c8-4e66-ae0d-8825c3948d41`
Categoria: Normal — raridade: Common (0) — peso relativo: 1.0
Origem: events/entangled boar — SHA objeto: `31dde506c7176062328d57a18261c88ca218d33aa437a5783d92b39115b50703`

### Texto original
A <green><b><incr>Wild Boar</incr></b></green>, powerfully built and grim-eyed, is caught in a thorny snare. The thick Bristlethorn, is tough as twisted iron and studded with wicked thorns that dig deep into the boar's hide.

Every movement the boar makes only seems to make the situation worse. The thorns bite deeper into its flesh, drawing forth beads of crimson that seep into the rich, damp earth. It thrashes and grunts in raw, unfiltered fear and pain, its eyes wild with the primitive instinct of a creature trapped and in distress.

### Resultados possíveis (texto autoral)
Who will approach the boar?

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
      1
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

### Opção 1: Help
Attempt to free the boar.

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

#### Ação 1: Success — RollLimit 11
With a swift, precise stroke, you cut through the thorny vine. The tension in the boar's body eases as the vine's grip lessens. The boar stumbles, then rights itself, its eyes wide.

The boar grunts, a low, rumbling sound that seems almost... grateful. You turn to leave, but a rustle behind you gives you pause.


Turning, you find the boar following you, its eyes fixed on you with something akin to loyalty. It seems the beast, in its own wild, untamed way, has pledged its gratitude to you. You can't help but smile, feeling a strange sense of companionship.

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
          "chave": "resources.assets:2545413",
          "nome": "Boar Charm",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545413
          },
          "tipo": "EventStatus",
          "descricao": "Allows you to summon a @level@ {1,30} Wild Boar to fight for you.\n\n<i><color=#808080>The boar you rescued follows you.</i></color>\n",
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

#### Ação 2: Failure — RollLimit 1
The vine, is stubbornly resistant to your blade, and refuses to yield. You quickly find yourself entangled in the thick vine as well. 

Swinging your blade desperately, you tumble free, gasping for breath, your hands and arms lined with shallow cuts.

With a heavy heart, you back away, sheathing your sword. The boar's panicked grunts echo in your ears, a bitter reminder of your failure.



Efeito 1 (configuração autoral, não resultado de partida):
```json
{
  "vida_mana": {
    "percentMaxHealth": -30.0,
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
          "chave": "resources.assets:2545498",
          "nome": "Restrained",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545498
          },
          "tipo": "EventStatus",
          "descricao": "Reduces @Reflex@ by @20%@ per stack.",
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
                "chave": "resources.assets:2544456",
                "nome": "ReflexBase",
                "pptr": {
                  "m_FileID": 0,
                  "m_PathID": 2544456
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
The potential risks are too great.

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
With a final, regretful look at the ensnared boar, [name] turns away, leaving the creature to its own fight.


---

