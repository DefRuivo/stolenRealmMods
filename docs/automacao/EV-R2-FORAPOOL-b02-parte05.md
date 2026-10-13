# EV-R2-FORAPOOL-b02 — parte 05: fechamento, inventário de vereditos e auditoria

Fontes: `C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-NotInEventPool-v2.md`, `eventos.json`, `eventos.schema.json`, `schema.md` e `catalogo-referencias.json`. Coordenadas `opcoes/0` e `efeitos/0` são índices JSON base zero; títulos Opção 1/Ação 1 são base um. Strings JSON exibem os controles originais. Cada proposta é PENDENTE, não uma decisão do dono. Recompensa/condição: MANTER, sem alteração; aplicação runtime: NAO_EXERCITADO (tarefa offline, sem jogo).


## Contagens

```json
{
  "eventos": 21,
  "chaves_unicas": 21,
  "opcoes": 28,
  "acoes": 28,
  "overrides": 1,
  "MELHORAR_wording": 16,
  "MANTER": 5,
  "campos_textuais_alterados": 24,
  "substituicoes": 33,
  "nulls_com_motivo": 364,
  "referencias_nulas_projetadas": 52,
  "textos_vazios_auditados": 77,
  "disabled_1": 0,
  "opcoes_sem_opcoes": 2,
  "opcoes_ocultas_configuradas": 0,
  "opcoes_hideOptionEffectText": 1,
  "mudancas_recompensa": 0,
  "mudancas_condicao": 0,
  "aprovacoes_do_dono": 0
}
```

Contagem de NULL inclui as projeções redundantes `opcoes[].recompensas`, mas exclui `campos_originais`; portanto não representa número de prêmios independentes. Contagem de textos vazios cobre narrativa, resultados possíveis, dois campos de seleção, títulos/descrições das opções, mysteryRollEffectText, activationText e manualEffectText: escopo preciso, não todas as strings de todos os objetos.

## Inventário final

| Nº | Chave | Título | Veredito proposto | Natureza | Campos alterados | NULL | Aprovação |
|---:|---|---|---|---|---:|---:|---|

| 22 | resources.assets:2545613 | Jack in the Box | MELHORAR | wording | 3 | 24 | PENDENTE |

| 23 | resources.assets:2545615 | Jack in the Box | MELHORAR | wording | 2 | 24 | PENDENTE |

| 24 | resources.assets:2545614 | Jack in the Box - Victory | MELHORAR | wording | 2 | 21 | PENDENTE |

| 25 | resources.assets:2545633 | King Under the Mountain | MELHORAR | wording | 1 | 0 | PENDENTE |

| 26 | resources.assets:2545620 | Lady of the Well | MELHORAR | wording | 1 | 13 | PENDENTE |

| 27 | resources.assets:2545617 | Lesser Mimic | MELHORAR | wording | 2 | 39 | PENDENTE |

| 28 | resources.assets:2545625 | Magic Mirror | MELHORAR | wording | 1 | 13 | PENDENTE |

| 29 | resources.assets:2545650 | Master of Rage | MELHORAR | wording | 2 | 13 | PENDENTE |

| 30 | resources.assets:2545754 | Mimic | MANTER | wording/recompensa/condicao | 0 | 39 | PENDENTE |

| 31 | resources.assets:2545657 | Ogre Debt Collector | MANTER | wording/recompensa/condicao | 0 | 13 | PENDENTE |

| 32 | resources.assets:2545658 | Ogre Debt Collector | MANTER | wording/recompensa/condicao | 0 | 13 | PENDENTE |

| 33 | resources.assets:2545661 | Party like a Pirate | MELHORAR | wording | 1 | 24 | PENDENTE |

| 34 | resources.assets:2545662 | Party like a Pirate | MELHORAR | wording | 1 | 24 | PENDENTE |

| 35 | resources.assets:2545663 | Party like a Pirate | MELHORAR | wording | 2 | 26 | PENDENTE |

| 36 | resources.assets:2545667 | Pirate's Treasure | MELHORAR | wording | 2 | 13 | PENDENTE |

| 37 | resources.assets:2545669 | Poacher's Demise | MELHORAR | wording | 1 | 13 | PENDENTE |

| 38 | resources.assets:2545629 | Red Dragon | MELHORAR | wording | 1 | 0 | PENDENTE |

| 39 | resources.assets:2545679 | Scent of Blood | MANTER | wording/recompensa/condicao | 0 | 13 | PENDENTE |

| 40 | resources.assets:2545695 | Strange Crystal | MELHORAR | wording | 1 | 13 | PENDENTE |

| 41 | resources.assets:2545698 | Strange Crystal | MELHORAR | wording | 1 | 13 | PENDENTE |

| 42 | resources.assets:2545701 | Strange Crystal | MANTER | wording/recompensa/condicao | 0 | 13 | PENDENTE |

## Fontes imutáveis — SHA-256

```json
{
  "lote-NotInEventPool-v2.md": "72c4ddba4ae8bf4bc50371bf2b207d26abff4525f4d79e7585c801beb37396e9",
  "eventos.json": "4a8decac7e98a2b0bf8692057a57789a71b94c230e3b9ca93817f039c86d1d13",
  "eventos.schema.json": "6950ec43deba94143150f0584bb87ca5406b3ef16f1ae2f18ad8aa943a62b3bc",
  "catalogo-referencias.json": "94077cc887621933abe7bbbbd96e91c5a887478dba8fd000b8f4a4129c3745a5",
  "schema.md": "a4e62045c51a57bd0eb3084a8c1fb8534b4bfc6303fe38e4a6896e1a96d34cfb"
}
```

## Limites

- NAO_EXERCITADO: runtime, UI, jogo, RNG, disponibilidade, seleção e aplicação final de status, quantidades finais de XP/ouro/loot, combate. Motivo: análise documental/offline.
- NULL de resultado final não é zero; PPtr nulo é ausência estrutural, com motivo específico.
- Não houve implementação nem alteração de fonte canônica, DLL/plugin/asset/jogo.
- Referências entrantes: PPtr locais explícitos nos eventos canônicos (sem duplicações de campos_originais) e nos registros do catálogo. Não é busca universal de chamadas em código, strings de prefab ou runtime.

## Auditoria de NULL por evento e caminho

### 22. resources.assets:2545613 — 24 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

### 23. resources.assets:2545615 — 24 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

### 24. resources.assets:2545614 — 21 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].overrides[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].overrides[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].overrides[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].overrides[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].overrides[0].recompensas[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].overrides[0].recompensas[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].overrides[0].recompensas[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].overrides[0].recompensas[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

### 25. resources.assets:2545633 — 0 NULL

```json
[]
```

### 26. resources.assets:2545620 — 13 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

### 27. resources.assets:2545617 — 39 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[2].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[2].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[2].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[2].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[2].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[2].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[2].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[2].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[2].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

### 28. resources.assets:2545625 — 13 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

### 29. resources.assets:2545650 — 13 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

### 30. resources.assets:2545754 — 39 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[2].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[2].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[2].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[2].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[2].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[2].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[2].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[2].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[2].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[2].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

### 31. resources.assets:2545657 — 13 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

### 32. resources.assets:2545658 — 13 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

### 33. resources.assets:2545661 — 24 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

### 34. resources.assets:2545662 — 24 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

### 35. resources.assets:2545663 — 26 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

### 36. resources.assets:2545667 — 13 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

### 37. resources.assets:2545669 — 13 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

### 38. resources.assets:2545629 — 0 NULL

```json
[]
```

### 39. resources.assets:2545679 — 13 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

### 40. resources.assets:2545695 — 13 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

### 41. resources.assets:2545698 — 13 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

### 42. resources.assets:2545701 — 13 NULL

```json
[
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.referencia.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].batalha.dados_recompensa_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.chave",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].efeitos[0].evento_encadeado.nome",
    "valor": null,
    "classe": "REFERENCIA_NULA",
    "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
  },
  {
    "campo": "$.opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
    "valor": null,
    "classe": "NAO_EXERCITADO",
    "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
  }
]
```

## Leitura humana e próximo passo

Partes 02, 03 e 04 contêm 7 eventos cada e todos os campos completos atuais/propostos; parte 01 traz 21 linhas do inventário com categoria, raridade e peso. `propostas-auditadas.json` guarda 21 propostas com coordenadas e motivos. `validar.py` executa verificações offline independentes. Todos os 21 vereditos são propostos e não aprovados. O filho t_8e74c724 é humano e deve continuar aguardando o dono. Nenhuma implementação autorizada.
