# EV-R2-FORAPOOL-b04 — parte05: fechamento, inventário de vereditos e anomalias

Fontes: {
  "C:\\dev\\stolen-realm\\docs\\cobertura\\EV-R1\\eventos.json": {
    "sha256": "4a8decac7e98a2b0bf8692057a57789a71b94c230e3b9ca93817f039c86d1d13",
    "bytes": 14343841
  },
  "C:\\dev\\stolen-realm\\docs\\cobertura\\EV-R1\\eventos.schema.json": {
    "sha256": "6950ec43deba94143150f0584bb87ca5406b3ef16f1ae2f18ad8aa943a62b3bc",
    "bytes": 7059
  },
  "C:\\dev\\stolen-realm\\docs\\cobertura\\EV-R1\\lote-NotInEventPool-v2.md": {
    "sha256": "72c4ddba4ae8bf4bc50371bf2b207d26abff4525f4d79e7585c801beb37396e9",
    "bytes": 514868
  },
  "C:\\dev\\stolen-realm\\docs\\cobertura\\EV-R1\\schema.md": {
    "sha256": "a4e62045c51a57bd0eb3084a8c1fb8534b4bfc6303fe38e4a6896e1a96d34cfb",
    "bytes": 8075
  },
  "C:\\dev\\stolen-realm\\docs\\cobertura\\EV-R1\\eventos-originais.json": {
    "sha256": "e52bb7d0fd34a1cd48065f13c856b130103c3b8618c05db13820639750b27766",
    "bytes": 2956196
  },
  "git:097f950:docs/cobertura/EV-R1/catalogo-referencias.json": {
    "commit": "097f950677a02e964f7b43fc1b2998b8daa48c3c",
    "blob": "4e2ea65540dab8acab2ee17aa4a63ad68780443f",
    "sha256": "8a8d21d1721840e288f42480cb0f24aeac26292be7b01a6830384b4e3f983cfe",
    "bytes": 26549924,
    "registros": 2399,
    "resumos": 3214
  },
  "historical_eventos_sha256": "a330439c16a17c73d42793ae84c11181ca42da9dbea2feaaa8c81233ca5015cb",
  "historical_eventos_semantic_equal": true,
  "historical_eventos_crlf_normalized_equal": true
}

Catálogo ausente da pasta atual porque removido do tracking em b2a25ac; recuperado SOMENTE POR LEITURA do blob git em 097f950:docs/cobertura/EV-R1/catalogo-referencias.json. Os SHA-256 histórico e atual do eventos.json diferem por terminação de linha do arquivo (LF/CRLF), mas igualdade do JSON completo e igualdade dos bytes após normalização exclusivamente CRLF foram verificadas; os strings internos permanecem idênticos. Não se modificou o catálogo ou o dump. A lacuna inicial descrita na parte01 está resolvida.

## Contagens calculadas

```json
{
  "eventos": 21,
  "MELHORAR_wording": 19,
  "MANTER": 2,
  "opcoes": 29,
  "acoes": 28,
  "overrides": 0,
  "campos_propostos": 40,
  "substituicoes": 43,
  "nulls_com_motivo": 336,
  "nulls_runtime": 244,
  "nulls_referencia": 92,
  "referencias_nulas_projetadas": 46,
  "pptr_nulos_literais": 567,
  "textos_vazios_auditados": 76,
  "disabled_1": 2,
  "eventos_sem_opcoes": 3,
  "opcoes_ocultas_configuradas": 0,
  "hideOptionEffectText_ativo": 0,
  "prompts_deslocados_propostos": 17,
  "referencias_entrantes_explicitas": 45,
  "aprovacoes": 0,
  "mudancas_recompensa": 0,
  "mudancas_condicao": 0
}
```

Unidade de NULL: cada posição do canônico, inclusive projeção redundante de recompensa; não quantidade de recompensas. PPtrs m_PathID=0 têm contagem separada, inclusive campos_originais; nenhuma destas contagens é ocorrência de runtime. Textos vazios contam os campos narrativos/seleção/rolagem/manuais enumerados, não todo string técnico de serializationData.

## Inventário final dos 21 vereditos PROPOSTOS

| Nº | Chave | Título | Categoria | Raridade | Peso | Proposta | Campos | Aprovação |
|---:|---|---|---|---|---:|---|---:|---|

|64|resources.assets:2545781|The runes of the Ymir|NotInEventPool|Common (0)|1.0|MELHORAR / wording|3|PENDENTE|

|65|resources.assets:2545783|The runes of the Ymir|NotInEventPool|Common (0)|1.0|MELHORAR / wording|4|PENDENTE|

|66|resources.assets:2545747|The Spell Council|NotInEventPool|Common (0)|1.0|MELHORAR / wording|2|PENDENTE|

|67|resources.assets:2545749|The Spell Council|NotInEventPool|Common (0)|1.0|MELHORAR / wording|2|PENDENTE|

|68|resources.assets:2545635|The Sultan|NotInEventPool|Common (0)|1.0|MANTER / nenhuma|0|PENDENTE|

|69|resources.assets:2545643|The Witch|NotInEventPool|Common (0)|1.0|MELHORAR / wording|1|PENDENTE|

|70|resources.assets:2545647|Too Late|NotInEventPool|Common (0)|1.0|MELHORAR / wording|1|PENDENTE|

|71|resources.assets:2545760|Treasure of Moltendunn|NotInEventPool|Common (0)|1.0|MELHORAR / wording|1|PENDENTE|

|72|resources.assets:2545761|Treasure of Moltendunn|NotInEventPool|Common (0)|1.0|MELHORAR / wording|2|PENDENTE|

|73|resources.assets:2545762|Treasure of Moltendunn|NotInEventPool|Common (0)|1.0|MELHORAR / wording|4|PENDENTE|

|74|resources.assets:2545763|Treasure of Moltendunn|NotInEventPool|Common (0)|1.0|MELHORAR / wording|3|PENDENTE|

|75|resources.assets:2545764|Treasure of Moltendunn|NotInEventPool|Common (0)|1.0|MELHORAR / wording|3|PENDENTE|

|76|resources.assets:2545765|Trial of the Ymir|NotInEventPool|Common (0)|1.0|MELHORAR / wording|2|PENDENTE|

|77|resources.assets:2545766|Trial of the Ymir|NotInEventPool|Common (0)|1.0|MELHORAR / wording|2|PENDENTE|

|78|resources.assets:2545570|Unholy Experiments|NotInEventPool|Common (0)|1.0|MELHORAR / wording|2|PENDENTE|

|79|resources.assets:2545768|Unleashed|NotInEventPool|Common (0)|1.0|MELHORAR / wording|1|PENDENTE|

|80|resources.assets:2545769|Unleashed|NotInEventPool|Common (0)|1.0|MELHORAR / wording|1|PENDENTE|

|81|resources.assets:2545772|What Lurks|NotInEventPool|Common (0)|1.0|MANTER / nenhuma|0|PENDENTE|

|82|resources.assets:2545775|Witch's Pyre|NotInEventPool|Rare (2)|1.0|MELHORAR / wording|2|PENDENTE|

|83|resources.assets:2545782|Ymir Rune, Honor|NotInEventPool|Common (0)|1.0|MELHORAR / wording|2|PENDENTE|

|84|resources.assets:2545784|Ymir Rune, Strength|NotInEventPool|Common (0)|1.0|MELHORAR / wording|2|PENDENTE|

## Auditoria individual de vazios, NULL e referências nulas

Os NULL de runtime preservam o motivo específico do contêiner. Mesmo flags dar=false não autorizam substituir quantidade_final por zero. Os PPtr nulos são ausências estáticas autorais, não runtime não exercitado.

### 64 — resources.assets:2545781 — The runes of the Ymir

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/campos_originais/characterSelectedText",
  "/opcoes/0/rolagem/texto_misterioso",
  "/opcoes/1/rolagem/texto_misterioso",
  "/opcoes/1/efeitos/0/texto"
]
```

NULL (cada posição com tipo e motivo):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/1/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

Referências nulas projetadas:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  }
]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[]
```

### 65 — resources.assets:2545783 — The runes of the Ymir

Vazios narrativos e de seleção/rolagem:

```json
[
  "/campos_originais/characterSelectedText",
  "/opcoes/0/rolagem/texto_misterioso",
  "/opcoes/1/rolagem/texto_misterioso"
]
```

NULL (cada posição com tipo e motivo):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/1/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

Referências nulas projetadas:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  }
]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[]
```

### 66 — resources.assets:2545747 — The Spell Council

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/opcoes/0/rolagem/texto_misterioso"
]
```

NULL (cada posição com tipo e motivo):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

Referências nulas projetadas:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  }
]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/candidatos/0",
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
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/candidatos/0",
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
]
```

### 67 — resources.assets:2545749 — The Spell Council

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/campos_originais/characterSelectedText",
  "/opcoes/0/rolagem/texto_misterioso",
  "/opcoes/1/rolagem/texto_misterioso"
]
```

NULL (cada posição com tipo e motivo):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/1/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

Referências nulas projetadas:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  }
]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/candidatos/0",
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
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/candidatos/0",
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
]
```

### 68 — resources.assets:2545635 — The Sultan

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/campos_originais/promptToSelectCharacter",
  "/campos_originais/characterSelectedText"
]
```

NULL (cada posição com tipo e motivo):

```json
[]
```

Referências nulas projetadas:

```json
[]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[]
```

### 69 — resources.assets:2545643 — The Witch

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/campos_originais/promptToSelectCharacter",
  "/campos_originais/characterSelectedText"
]
```

NULL (cada posição com tipo e motivo):

```json
[]
```

Referências nulas projetadas:

```json
[]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[]
```

### 70 — resources.assets:2545647 — Too Late

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/campos_originais/promptToSelectCharacter",
  "/campos_originais/characterSelectedText"
]
```

NULL (cada posição com tipo e motivo):

```json
[]
```

Referências nulas projetadas:

```json
[]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[]
```

### 71 — resources.assets:2545760 — Treasure of Moltendunn

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/campos_originais/characterSelectedText",
  "/opcoes/0/rolagem/texto_misterioso",
  "/opcoes/0/efeitos/0/texto",
  "/opcoes/1/rolagem/texto_misterioso"
]
```

NULL (cada posição com tipo e motivo):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

Referências nulas projetadas:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  }
]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[]
```

### 72 — resources.assets:2545761 — Treasure of Moltendunn

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/campos_originais/characterSelectedText",
  "/opcoes/0/rolagem/texto_misterioso",
  "/opcoes/1/texto",
  "/opcoes/1/rolagem/texto_misterioso"
]
```

NULL (cada posição com tipo e motivo):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/1/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/1/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/recompensas/1/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/1/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/1/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/1/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

Referências nulas projetadas:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  }
]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/1/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/1/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/1/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/1/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/1/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/1/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/1/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/1/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[
  {
    "campo": "/opcoes/0/efeitos/1/efeitos/0/recompensas/status/candidatos/0",
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
  },
  {
    "campo": "/opcoes/0/recompensas/1/padrao/0/status/candidatos/0",
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
]
```

### 73 — resources.assets:2545762 — Treasure of Moltendunn

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/campos_originais/characterSelectedText",
  "/opcoes/0/rolagem/texto_misterioso",
  "/opcoes/1/rolagem/texto_misterioso"
]
```

NULL (cada posição com tipo e motivo):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/1/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/1/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/recompensas/1/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/1/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/1/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/1/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

Referências nulas projetadas:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  }
]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/1/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/1/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/1/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/1/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/1/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/1/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/1/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/1/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[
  {
    "campo": "/opcoes/0/efeitos/1/efeitos/0/recompensas/status/candidatos/0",
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
  },
  {
    "campo": "/opcoes/0/recompensas/1/padrao/0/status/candidatos/0",
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
]
```

### 74 — resources.assets:2545763 — Treasure of Moltendunn

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/campos_originais/characterSelectedText",
  "/opcoes/0/rolagem/texto_misterioso",
  "/opcoes/1/texto",
  "/opcoes/1/rolagem/texto_misterioso"
]
```

NULL (cada posição com tipo e motivo):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

Referências nulas projetadas:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  }
]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/1/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/1/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/1/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/1/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/1/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/1/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/1/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/1/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/1/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[]
```

### 75 — resources.assets:2545764 — Treasure of Moltendunn

Vazios narrativos e de seleção/rolagem:

```json
[
  "/campos_originais/characterSelectedText",
  "/opcoes/0/rolagem/texto_misterioso",
  "/opcoes/1/rolagem/texto_misterioso",
  "/opcoes/2/rolagem/texto_misterioso"
]
```

NULL (cada posição com tipo e motivo):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/1/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/2/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/2/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/2/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/2/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/2/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/2/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/2/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/2/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/2/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/2/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/2/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/2/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/2/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

Referências nulas projetadas:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/2/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/2/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  }
]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/2/efeitos/0/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/2/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/2/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/2/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/2/efeitos/0/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/2/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/2/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/2/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/2/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/2/campos_originais/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/2/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/2/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/2/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/2/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/2/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/2/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/2/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/2/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/2/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/2/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/candidatos/0",
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
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/candidatos/0",
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
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/status/candidatos/0",
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
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/status/candidatos/0",
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
  },
  {
    "campo": "/opcoes/2/efeitos/0/efeitos/0/recompensas/status/candidatos/0",
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
  },
  {
    "campo": "/opcoes/2/recompensas/0/padrao/0/status/candidatos/0",
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
]
```

### 76 — resources.assets:2545765 — Trial of the Ymir

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/campos_originais/characterSelectedText",
  "/opcoes/0/rolagem/texto_misterioso"
]
```

NULL (cada posição com tipo e motivo):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

Referências nulas projetadas:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  }
]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/candidatos/0",
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
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/candidatos/1",
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
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/candidatos/2",
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
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/candidatos/0",
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
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/candidatos/1",
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
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/candidatos/2",
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
]
```

### 77 — resources.assets:2545766 — Trial of the Ymir

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/campos_originais/characterSelectedText",
  "/opcoes/0/rolagem/texto_misterioso",
  "/opcoes/1/rolagem/texto_misterioso"
]
```

NULL (cada posição com tipo e motivo):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/1/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

Referências nulas projetadas:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  }
]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[]
```

### 78 — resources.assets:2545570 — Unholy Experiments

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/campos_originais/characterSelectedText",
  "/opcoes/0/rolagem/texto_misterioso",
  "/opcoes/0/efeitos/0/texto",
  "/opcoes/1/rolagem/texto_misterioso"
]
```

NULL (cada posição com tipo e motivo):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/1/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/1/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/1/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

Referências nulas projetadas:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/1/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  }
]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/1/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/1/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[]
```

### 79 — resources.assets:2545768 — Unleashed

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/opcoes/0/rolagem/texto_misterioso"
]
```

NULL (cada posição com tipo e motivo):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

Referências nulas projetadas:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  }
]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/candidatos/0",
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
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/candidatos/0",
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
]
```

### 80 — resources.assets:2545769 — Unleashed

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/campos_originais/characterSelectedText",
  "/opcoes/0/rolagem/texto_misterioso"
]
```

NULL (cada posição com tipo e motivo):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

Referências nulas projetadas:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  }
]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[]
```

### 81 — resources.assets:2545772 — What Lurks

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/campos_originais/promptToSelectCharacter",
  "/campos_originais/characterSelectedText",
  "/opcoes/0/rolagem/texto_misterioso"
]
```

NULL (cada posição com tipo e motivo):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

Referências nulas projetadas:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  }
]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/candidatos/0",
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
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/candidatos/0",
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
]
```

### 82 — resources.assets:2545775 — Witch's Pyre

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/opcoes/0/rolagem/texto_misterioso",
  "/opcoes/0/efeitos/0/texto"
]
```

NULL (cada posição com tipo e motivo):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

Referências nulas projetadas:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  }
]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/candidatos/0",
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
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/candidatos/0",
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
]
```

### 83 — resources.assets:2545782 — Ymir Rune, Honor

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/campos_originais/characterSelectedText",
  "/opcoes/0/rolagem/texto_misterioso"
]
```

NULL (cada posição com tipo e motivo):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

Referências nulas projetadas:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/evento_encadeado",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  }
]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/chainedEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/candidatos/0",
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
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/candidatos/0",
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
]
```

### 84 — resources.assets:2545784 — Ymir Rune, Strength

Vazios narrativos e de seleção/rolagem:

```json
[
  "/texto_resultados_possiveis",
  "/campos_originais/characterSelectedText",
  "/opcoes/0/rolagem/texto_misterioso"
]
```

NULL (cada posição com tipo e motivo):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/chave",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia/nome",
    "tipo": "REFERENCIA_NULA_ASSET",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/dados_recompensa_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/ouro/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/experiencia/quantidade_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/itens/sorteio_final",
    "tipo": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/resultado_sorteado",
    "tipo": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

Referências nulas projetadas:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/referencia",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  }
]
```

PPtr nulos literais (campo original incluído):

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/batalha/override/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/efeitos/0/campos_originais/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/opcoes/0/campos_originais/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/m_GameObject",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/serializationData/Prefab",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/consumedEffect",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/VictoryEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/FailureEvent",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/eventActions/0/battleOverrideInfo/MapToForce",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  },
  {
    "campo": "/campos_originais/eventOptions/0/generatedBattle",
    "motivo": "PPtr serializado m_PathID=0: referência nula no asset; não resultado de partida."
  }
]
```

Status candidatos/remoções referenciados, textos vazios de descrição e fórmulas mantidos literalmente:

```json
[
  {
    "campo": "/opcoes/0/efeitos/0/efeitos/0/recompensas/status/candidatos/0",
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
  },
  {
    "campo": "/opcoes/0/recompensas/0/padrao/0/status/candidatos/0",
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
]
```

## Limites e aprovação

21/21 análises entregues nas partes02–04; inventário inicial na parte01, final nesta parte05. Toda recompensa/condição proposta como MANTER; zero aprovações. Campos vazios e efeitos vazios não preenchidos. Nenhuma alteração de plugin/DLL/assets/arquivo do jogo, nenhum jogo/build/deploy.

NAO_EXERCITADO: runtime/UI, seleção, disponibilidade, sorteios, quantidades finais, aplicação de status, comportamento de laços e combate. Motivo: tarefa exclusivamente documental. Sem alegação de teste no jogo.

A biblioteca JSON Schema, se disponível, será usada apenas para validar o canônico original; checagens documentais adicionais e negativos pertencem a validar.py e validacao.json. Não confundir schema com teste funcional do jogo.

Referências locais explícitas varridas: canônico (256 PartyEvent) e catálogo (2399 registros). Isso não cobre referências codificadas em strings, código ou bytes Odin privados. Snapshot de apoio em referencias-auditadas.json; ausências são registradas, não completadas por suposição.

Revisão humana já pré-criada: t_8e74c724. A fase documental pode ser concluída para liberar a dependência, sem revisão duplicada no mesmo cartão e sem atribuir aprovação ao dono.
