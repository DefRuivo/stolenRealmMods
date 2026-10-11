# EV-R1 — SemPoolDeclarado (10)

## Admiral Blackbeard
Chave: `resources.assets:2545638` — GUID: `04cc0b09-7bed-462a-a71c-fc81d280905c`
Categoria: SemPoolDeclarado — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/5 - admiral blackbeard start — SHA objeto: `a9a0f60789d439e7aab0f87904b61eb845f606888327fa845d1066ef5c486adf`

### Texto original
In the heart of the ancient ruins, where the whispers of the sea merge with the echoes of a forgotten past, you finally come face to face with the dread pirate, Blackbeard.

He stands like a specter of old, his figure imposing, clad in tattered sea-worn garb, a rapier in one hand glinting with ghostly light, and a hook for a hand gleaming menacingly in the other.

"Another fool comes seeking to take what is mine?" Blackbeard's voice is a growl, as rough as the tempestuous seas he has mastered. "Robbers, come to plunder my treasure!"

Blackbeard's eyes, dark as the deepest ocean trenches, bore into you with a mix of distrust and deadly malice. The years at sea, chasing treasure and battling the waves, have etched lines of cunning and cruelty into his face. His greed, like a malignant shadow, has consumed him, leaving in its wake a man driven by paranoia and the relentless pursuit of wealth.

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

### Opção 1: Fight
You launch into the fray, curiosity mingling with your strikes as you ponder the twisted fates the curse has woven for these conspirators.

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
      "m_PathID": 2545637
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

## King Under the Mountain
Chave: `resources.assets:2545634` — GUID: `a84f7a47-e0cf-4bc9-a7e6-b0136ae7b63f`
Categoria: SemPoolDeclarado — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/3 - mountain king ironheart start — SHA objeto: `7d32b859ade905a058d70fce78cad14ab35f92065d80e2fafd9d992d01bea9ca`

### Texto original
As you draw near the dwarven throne, a profound melancholy envelops Ironheart.

"Long ago," the king began, his voice echoing off the cold stone walls, "our halls shone with the light of a thousand torches, and our forges burned bright, crafting wonders the likes of which the world has never seen since. And now?" the Mountain King jestures dismally at the surrounding ruins. 

"Long have the dragons slumbered," his voice rumbles, deep as the earth, "but we paid dearly for it."

"A tempest of fire and fury they were. In our desperation, we turned to forbidden powers, dark powers..." He pauses, his gaze distant, haunted. "We tried, lad. You can't say we didn't try."
<br/>
With sudden intensity, his eyes, like smoldering coals, fix on you. "Your father, he had an insatiable curiosity, always delving where eyes shouldn't pry. He dug too deep, too greedily in my kingdom."

A madness dances in the Mountain King's eyes, the flickering flames of a once-noble spirit now consumed by fear and desperation. 

"I sent them, the bandits, to protect what is mine. But you persisted, like your father. And now, you leave me no choice. I cannot allow you or your father's legacy to leave these halls. The secrets of my kingdom must remain within these walls, even if it means your end."

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

### Opção 1: Fight
Hesitantly you step into the fray, your mind swirling with questions about what transformed this ally into an adversary

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
      "m_PathID": 2545633
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

## Red Dragon
Chave: `resources.assets:2545630` — GUID: `68fdf79b-d4d6-43d5-afd7-3174d9b085d4`
Categoria: SemPoolDeclarado — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/10 - red dragon start — SHA objeto: `b2ea1cb000f1427b176a43eaf4419a8d8f0fd1348b14e322de1b223f121d4e4d`

### Texto original
Emerging from a smoky haze, is the massive form of a full-grown red dragon, an ancient creature of legend and the embodiment of the Emberlands itself.

The dragon's wings, vast and powerful, beat against the sky, each stroke a tempest that sends waves of hot air swirling through the scorched landscape. Its wingspan is like a canvas upon which the tales of ages could be written, a testament to the countless years it has soared above the realm.

Its talons, sharp and deadly, are like swords forged in the deepest fires of the earth, capable of rending stone and metal alike. They scrape against the hardened ground, sending sparks flying, a display of its fearsome prowess and the lethal grace with which it moves.

The dragon's breath is a spectacle of wild flame, erratic and destructive, a force of nature unleashed. With every exhalation, torrents of fire pour from its maw, painting the air with streaks of incandescence. The flames dance around its head like a crown of chaos, a reminder that this creature is the very incarnation of flame, a being for whom fire is both breath and essence.

Never have you felt more alive than in this moment, standing before the red dragon in the heart of its domain.

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

### Opção 1: Fight
You ascend to confront a challenge, a thousand years in the making.

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
      "m_PathID": 2545629
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

## The Bandit
Chave: `resources.assets:2545628` — GUID: `5f33c065-84a9-455b-b539-12c2bad9e74a`
Categoria: SemPoolDeclarado — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/1 - boss bandit start — SHA objeto: `466a765744ea6772752107ac2664df68c2bec68273a8ecf50d24b846f7c74ea3`

### Texto original
The Blood Mask Boss waits with a calculated patience in a wide clearing. The trees around the perimeter seem to form a natural amphitheater, setting the stage for the imminent confrontation.

His eyes, sharp and observant, scan the surroundings, betraying a hint of anticipation beneath his otherwise composed demeanor. It is almost as if he has chosen this spot deliberately, knowing its significance to you.

"Ah, there you are! I was beginning to wonder if the tales of your valor were just that—tales." he gloats. "Ironheart believed that you'd come for your father's journal, but I wagered that the cries of this forest would draw you out."

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

### Opção 1: Fight
Fury mounts within you, understanding that they ravaged the forest solely to lure you into their trap.

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
      "m_PathID": 2545627
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

## The Dead One
Chave: `resources.assets:2545646` — GUID: `dda682c8-8f63-4e88-be4d-e77642927ba4`
Categoria: SemPoolDeclarado — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/9 - the dead one start — SHA objeto: `85976fad2c1d3571e750c5beecb5fa093e401683db1e4254fadf60e427376c19`

### Texto original
In the deepest, most forsaken depths of Castle Gloom you come upon the source of the all-consuming darkness. It is not a creature of malice or cunning, but rather the embodiment of an end most absolute – the Dead One. This entity is not evil in intent; it is the very essence of finality, the cessation of all things – laughter, love, life, memory – made manifest in this world.

Around the Dead One, the air seems to thin, as if the very essence of life is being drawn into the vacuum of its being. You can feel the pull of the abyss, a call to let go of all the struggles, fears, and pains that life entails, to surrender to the peace of nonexistence. It is a siren's call, seductive in its promise of an end to all suffering, an end to the relentless march of time and the burdens it brings.

Yet, within yourself stirs a profound resistance to this call. The relics you have gathered, each a remnant of a life once lived, a memory once cherished, glow with a faint but defiant light in the presence of the Dead One. They are reminders of all that is at stake, beacons of the lives, loves, and joys that had filled the realm before this shadow had fallen upon it.

Drawing upon the innermost reserves of your spirit, you confront the Dead One not just with sword or might, but with the resilience of one who clings to life in all its complexity and beauty. You stand as a testament to the enduring will of existence, a challenge to the void that seeks to claim all.


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

### Opção 1: Fight
Your determination crystalizes as you confront the entity that has ensnared your father's soul, among many, in its unyielding grasp.

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
      "m_PathID": 2545645
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

## The Dusk King
Chave: `resources.assets:2545640` — GUID: `78bc2027-e1df-4d62-8d07-596148f41d29`
Categoria: SemPoolDeclarado — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/6 - the dusk king start — SHA objeto: `e3cd26ec1b7c1da31b23b04849e5087d0caf35ad82c02afbb1d451ce88b6c3c7`

### Texto original
The summit is a desolate expanse, a frozen wasteland where the wind howls with the cries of lost souls.

Here, amidst the eternal snows and beneath the grey, brooding sky, you are confronted by a figure as chilling as the frostbitten air itself - the Dusk King, an undead lich whose very presence exudes an aura of bitter cold that seems to leech the warmth from the world.
<br/>
His voice is like the rustling of dead leaves, a sound both haunting and ageless. 

"You tread the path your father once walked, seeking to unravel the tapestries of fate we have woven. But you cannot fathom the choices we were forced to make, the sacrifices we bore to keep the dragons at bay."

"The Dead One feeds upon the dragons, eating their minds, driving them into a slumber from which they can not awaken."
<br/>
"Should you, or your father, undo the bindings that we have wrought to hold the dragons at bay, it would unleash a cataclysm upon the world."

"I cannot permit the world to fall into such peril again." the lich declares, his voice resolute in its somber decree.
<br/>
With those ominous words, the snow around you begins to stir, as if responding to the will of the Dusk King. From the white expanse emerge figures, ghastly and gruesome, the undead who lay frozen beneath the frost.

### Resultados possíveis (texto autoral)



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

### Opção 1: Fight
You steel yourself for a confrontation with a being whose existence has spanned more than a thousand years.

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
      "m_PathID": 2545639
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

## The Medusa
Chave: `resources.assets:2545642` — GUID: `c2d5010d-a2e3-425c-ab06-450332a297b8`
Categoria: SemPoolDeclarado — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/7 - the medusa start — SHA objeto: `07481ec9293d0aded9dcf0ad2ec85d3849600bf700c72b10ba5c73189ea50be3`

### Texto original
Amidst the dense foliage, where light and shadow play their eternal dance, you come upon a creature of legend, a being of dread and awe.

The Medusa, with her serpentine hair writhing like a nest of vipers, emerges from the undergrowth, her presence is a chilling blight upon the verdant world around her. Her skin is like scales, glistening in the dappled sunlight that filter through the canopy.

Her eyes, cold and reptilian, lock onto you with a predatory gaze. As your eyes meet, you feel a chill run through your veins, a sluggishness creeping into your limbs.

The Medusa circles you, her movements sinuous and graceful, yet filled with a menacing intent. She is the predator, and you, the unwitting prey, ensnared in her deadly dance.


### Resultados possíveis (texto autoral)



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

### Opção 1: Fight
You tread lightly, unknowing of the cunning snares the jungle sprites may have woven.

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
      "m_PathID": 2545641
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

## The Prospector
Chave: `resources.assets:2545632` — GUID: `d5fc09c8-94cd-4d69-bb3b-f7d6ce0d5e3e`
Categoria: SemPoolDeclarado — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/2 - the prospector start — SHA objeto: `bbde246c4782d70d71243e2817771855b19e4fad309fd36736f836d32efe999c`

### Texto original
A great dwarf stands like a sentinel in the dim light, his broad shoulders and stout frame a testament to years of laborious toil within the earth's embrace. His beard, long and unkempt, is flecked with the dust of the earth, and his eyes, sharp and piercing, gleam like the very gems he unearthes.

"The king himself said ye would show," his voice booms through the cavernous tunnels, "but I didn't believe anyone would be daft enough to venture here."  

With a swift movement, he lifts his massive pickaxe. “Some truths should remain buried. Your father, alas, never grasped that wisdom.”


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

### Opção 1: Fight
You steel yourself, preparing to confront a master of the subterranean realm.

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
      "m_PathID": 2545631
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
Chave: `resources.assets:2545636` — GUID: `fe62eca6-1277-4a23-a06b-449f790ae83a`
Categoria: SemPoolDeclarado — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/4 - the sultan start — SHA objeto: `fa4ce38013e08fb8763c2d69f193f57a415da4528c803298804a455ebb8179cc`

### Texto original
The air is thick with tension as you stand before the once-noble ruler of Wyrmrest. The Sultan's eyes, once a reflection of wisdom and kindness, now burn with an unsettling fervor for power.

"In Wyrmrest, strength is the only currency that holds any value. The weak are nothing but dust beneath the feet of the mighty." He says with a voice that is cold and unyielding. "My lands are sacred and every stone, every grain of sand, is protected by my strength."

His gaze fixes upon you with a predatory intensity. 

"You are an intruder, seeking to lay claim to the treasures that rightfully belong to me. You seek to undermine my authority, and for that, the sentence can only be death."


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

### Opção 1: Fight
You brace for the impending conflict, your thoughts wandering to what mystical amulets or enchanted talismans the Sultan might possess for his safeguarding.

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
      "m_PathID": 2545635
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

## The Witch
Chave: `resources.assets:2545644` — GUID: `4d91f160-6313-4c54-994a-182f8e9093c4`
Categoria: SemPoolDeclarado — raridade: Common (0) — peso relativo: 1.0
Origem: events/main quests/8 - the witch start — SHA objeto: `163bc38f4f09feeaa25e98e6c8d5af7309ceab6de9f79d9f2ae662fdd4de310b`

### Texto original
The Witch, shrouded in tattered robes that hang from her like moss from the gnarled trees, wanders the swamp with a demented grace. Around her, the decay seems to intensify, as if her very presence poisons the already fetid air. Wherever she steps, the ground becomes more putrid, the water more stagnant. It is as though she is an embodiment of the swamp's corruption, a living manifestation of its darkest aspect.

Her eyes, when she finally takes notice of you, are wild and unseeing, gleaming with a crazed light. In her gaze, you see not just madness, but a deep, consuming malice.

"So, you come to end my life?" she cackles, her voice a croaking echo that seems to blend with the swamp's chorus of decay. "This land is my sustenance, my eternal wellspring. I will live forever, and you, poor fool, will but add to my immortality. Your corpse will decay in these waters, feeding the swamp that sustains me."

Her laughter is a chilling sound, one that seems to resonate with the very essence of the swamp. In her twisted mind, she has become one with the land, a guardian of its corruption, thriving on the decay that has overtaken the once-vibrant forest.

### Resultados possíveis (texto autoral)



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

### Opção 1: Fight
You confront an adversary whose singular fixation, spanning centuries, has been the ceaseless pursuit of immortality.

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
      "m_PathID": 2545643
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
