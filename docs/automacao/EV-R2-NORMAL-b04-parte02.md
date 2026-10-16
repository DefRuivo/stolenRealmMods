# EV-R2-NORMAL-b04 — parte02: correção documental integral de 61–80

Cartão corretivo: t_821c05b9. Original: t_fd20ddc4. Revisão de origem: t_4c07d669. Data de referência: 2026-10-13.

PROPOSTA DOCUMENTAL, NÃO IMPLEMENTADA. Runtime: NAO_EXERCITADO. Aprovação de conteúdo pelo dono: PENDENTE.

## Retirada expressa das alegações da parte01

A parte01 permanece preservada como histórico reprovado. Esta parte02 RETIRA EXPRESSAMENTE suas 20 associações de ordinal/chave incorretas e as análises vinculadas a essas identidades; não as complementa nem autoriza aplicar seus wordings. Somente os títulos #61 e #62 coincidiam na posição. Todos os demais títulos/narrativas atribuídos à faixa são descartados. Taste for Blood 1 não é #63: aparece como destino real do encadeamento de #79, não como membro deste lote.

As afirmações de 20 narrativas vazias, nenhuma desabilitação, raridade Common em todos e peso 1.0 em todos são retiradas. O inventário abaixo reconstrói os dados: vazios apenas #63/#65/#67; disabled=1 em #62/#77; pesos 0.5 em #74/#75 e 0.25 em #76. #61 é Rare/texto 503 caracteres; #62 é Uncommon/texto 756 caracteres. Os comprimentos são Unicode len do valor JSON, incluindo espaços, tags e quebras de linha, não medidas de layout.

Os nomes de campo texto_original, recompensa_final e status_candidatos usados como JSON na parte01 são retirados por inexistirem. Os alvos desta parte usam o campo texto e caminhos completos existentes. A grafia Forged Enemies é retirada; o campo real é ForcedEnemies, dentro de batalha.override. Não se transfere a acusação de IsSuperUnique=1 para #61: seu ForcedEnemies é vazio e ForceRandomSuperUnique=1. A alegação de encadeamento de #62 é retirada: sua ação tem evento_encadeado.chave=NULL com motivo de PPtr nulo. As formas distincto, com献祭 temática e oro da redação anterior são retiradas; a análise nova usa distinto, tema de oferenda e ouro somente quando cabíveis, sem reaproveitar justificativas de eventos inexistentes.

## Fontes e convenções

Fontes somente leitura: C:/dev/stolen-realm/docs/cobertura/EV-R1/eventos.json, lote-Normal-v2.md, eventos.schema.json e catalogo-referencias.json. A ordem de todas as 160 seções ## do Markdown foi comparada à subsequência categoria=Normal do JSON; os 20 registros são as posições 61–80 dessa subsequência. JSONPath usa índice zero do array global $.eventos, não ordinal Normal e não path_id sequencial. A coincidência do índice global com o ordinal neste trecho foi verificada, não presumida.

Cada bloco REGISTRO AUDITÁVEL contém identidade, narrativa e inventário literal em evidencias (jsonpath/valor), propostas em mudancas (antes literal → depois exato) e registro de todos os NULLs normalizados com caminho e motivo. Campos próprios deste documento como veredito, mudancas e texto_chars NÃO são campos EV-R1. Nenhum bloco é um patch executável. Valores em evidencias são transcrições literais dos caminhos citados, não uma simulação de runtime.

Os textos sugeridos estão em inglês. PT-BR é usado apenas na análise e rótulos; nenhuma tradução do texto do jogo é proposta. Todo novo wording, inclusive preenchimento de string vazia, é SUGESTÃO DE ALTERAÇÃO DO ORIGINAL e depende de aprovação, não correção já aplicada ao jogo nem retificação da fonte EV-R1.

Inventário: inclui narrativa, resultados possíveis, condições completas, modos, história, full_release, todas as opções/condições/rolagens e todas as ações/resultados/limites/textos manuais, efeitos/alvos/recompensas/remoções/overrides e principais campos de batalha. O resumo redundante opcoes[].recompensas não é tratado como nova ação: seus NULLs são registrados separadamente com seus caminhos. Campos raw campos_originais e origem.codigo não são reimpressos; permanecem preservados na fonte. Fórmulas padrão de modificador de batalha não são anunciadas como recompensa ativa, especialmente quando UseRewardModifiers=0.

Flags dar/retirar e limitItemTypes/limitItemRarities controlam a interpretação: quantidade_configurada, restrições inativas e razao não são prova de ganho efetivo. Alvo override=false preserva tipo_default_serializado; tipo_override isolado não é alvo efetivo. Limites de rolagem não são probabilidades calculadas. NULL não é zero: quantidade_final, sorteio_final, resultado_sorteado e dados_recompensa_final dependem de partida/runtime; referência chave/nome nula é ausência estática de PPtr, não sorteio. Os motivos individuais são literais da fonte.

Nome de BattleInfo é apenas referência de template, não descrição do efeito final. Exemplo: #64 tem Cursed Chest Battle e ForcedEnemies explícitos; #78 Pay possui Ogre Debt Collector Battle mas iniciar=false, enquanto Refuse tem referência nula e iniciar=true com ForcedEnemies explícitos. Destinos VictoryEvent/FailureEvent são PPtrs de override; não são confundidos com evento_encadeado. referências_catalogo contém os resumos literais das referências locais não nulas usadas por cada evento; não acrescenta efeitos não descritos nesses dados.

## Inventário de identidade

| Ordinal | Chave | ID (GUID) | Título | Categoria | Raridade | Peso | disabled | Texto chars | Veredito |
|---|---|---|---|---|---|---|---|---|---|
| 61 | resources.assets:2545611 | 26e9ac99-9af8-423f-a024-90459dafd88d | Horn of Glorious Battle | Normal | Rare (2) | 1.0 | 0 | 503 | MELHORAR |
| 62 | resources.assets:2545612 | 0d898c20-9308-4239-98e6-a1d61fd531bf | Inconspicuous Burning Demon Skull | Normal | Uncommon (1) | 1.0 | 1 | 756 | MELHORAR |
| 63 | resources.assets:2545616 | 873ac971-40c8-4fd4-8bad-1a69d2ec6fca | Jewelry Box | Normal | Uncommon (1) | 1.0 | 0 | 0 | MELHORAR |
| 64 | resources.assets:2545618 | 3415fc65-d04d-4f99-9689-cb822c0fd365 | Jewelry Box | Normal | Uncommon (1) | 1.0 | 0 | 327 | MELHORAR |
| 65 | resources.assets:2545619 | c7086146-8450-4146-b6b1-4bc830580aa0 | Jewelry Box | Normal | Uncommon (1) | 1.0 | 0 | 0 | MELHORAR |
| 66 | resources.assets:2545621 | 32df0034-5a64-4155-92a5-62c6da8c4322 | Lady of the Well | Normal | Common (0) | 1.0 | 0 | 1209 | MANTER |
| 67 | resources.assets:2545622 | 38a07b13-77ae-4a04-98a5-237b10c31bce | Large Chest | Normal | Rare (2) | 1.0 | 0 | 0 | MELHORAR |
| 68 | resources.assets:2545623 | b2aed602-4583-45b3-a736-ee05bbe4c915 | Large Pile of Gold | Normal | Uncommon (1) | 1.0 | 0 | 48 | MANTER |
| 69 | resources.assets:2545624 | 3c3685cf-05c2-401b-bb42-bd85ae039034 | Lightning Sentry | Normal | Common (0) | 1.0 | 0 | 525 | MELHORAR |
| 70 | resources.assets:2545626 | bbce0c4c-c4df-4ebd-9b5f-fb745c872dc4 | Magic Mirror | Normal | Common (0) | 1.0 | 0 | 719 | MANTER |
| 71 | resources.assets:2545648 | 13531a98-c63d-4759-a46f-461586e41b3a | Mana Spring | Normal | Common (0) | 1.0 | 0 | 550 | MANTER |
| 72 | resources.assets:2545651 | 3c348484-97d8-44fe-9701-7897f376935e | Master of Rage | Normal | Common (0) | 1.0 | 0 | 1211 | MANTER |
| 73 | resources.assets:2545652 | adc51dbf-4064-4194-a024-34126346d7c9 | Mechanical Crusher | Normal | Common (0) | 1.0 | 0 | 397 | MELHORAR |
| 74 | resources.assets:2545653 | cdb949de-0865-4063-837c-c395f6c16878 | Mistress of Chaos | Normal | Common (0) | 0.5 | 0 | 487 | MELHORAR |
| 75 | resources.assets:2545654 | 56dfd84e-2bc7-4b20-891d-f661f99ef68e | Mistress of Chaos | Normal | Common (0) | 0.5 | 0 | 487 | MELHORAR |
| 76 | resources.assets:2545655 | c96278b1-90ed-46c8-8e50-9dc6d6d2cdf0 | Mistress of Chaos | Normal | Common (0) | 0.25 | 0 | 487 | MELHORAR |
| 77 | resources.assets:2545656 | 294579ef-2a2e-47d3-a729-78bc847b1422 | Off Balance | Normal | Common (0) | 1.0 | 1 | 63 | MANTER |
| 78 | resources.assets:2545659 | 2fc9c449-54a4-4b19-b457-3481e6e0aebb | Ogre Debt Collector | Normal | Common (0) | 1.0 | 0 | 376 | MELHORAR |
| 79 | resources.assets:2545660 | ff91cd18-05cb-45a7-abe1-4216f883bfbe | Ornate Coffin | Normal | Common (0) | 1.0 | 0 | 260 | MELHORAR |
| 80 | resources.assets:2545664 | 385d6042-6c20-4ee0-9791-a7a4ec12ae03 | Party like a Pirate | Normal | Common (0) | 1.0 | 0 | 579 | MELHORAR |

## Contagens reproduzíveis

```json
{
  "registros": 20,
  "chaves_unicas": 20,
  "ids_unicos": 20,
  "vereditos": {
    "MELHORAR": 14,
    "MANTER": 6
  },
  "alteracoes_textuais": 20,
  "raridades": {
    "Rare": 2,
    "Uncommon": 5,
    "Common": 13
  },
  "pesos": {
    "1.0": 17,
    "0.5": 2,
    "0.25": 1
  },
  "narrativas_vazias": [
    63,
    65,
    67
  ],
  "disabled": [
    62,
    77
  ],
  "opcoes": 34,
  "acoes": 37,
  "evidencias": 1654,
  "nulls": 425,
  "referencias_catalogo_por_evento": 84
}
```

## Evento 61 — Horn of Glorious Battle

Veredito: MELHORAR. MELHORAR apenas gramática e pontuação da narrativa já existente: espaço duplo, tempos verbais e aspa final sem abertura. A opção Blow the Horn inicia batalha com ForceRandomSuperUnique=1 e ForcedEnemies vazio; não promete riquezas nem inimigo fixo. Leave não inicia batalha. Não alterar opções, valores ou overrides.

Natureza: somente proposta editorial de wording; nenhum valor mecânico, alvo, condição, raridade, peso, disabled ou referência recebe alteração.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 61,
  "json_index": 61,
  "chave": "resources.assets:2545611",
  "id": "26e9ac99-9af8-423f-a024-90459dafd88d",
  "titulo": "Horn of Glorious Battle",
  "categoria": "Normal",
  "raridade": {
    "valor": 2,
    "nome": "Rare"
  },
  "peso": 1.0,
  "disabled": 0,
  "texto_chars": 503,
  "veredito": "MELHORAR",
  "justificativa": "MELHORAR apenas gramática e pontuação da narrativa já existente: espaço duplo, tempos verbais e aspa final sem abertura. A opção Blow the Horn inicia batalha com ForceRandomSuperUnique=1 e ForcedEnemies vazio; não promete riquezas nem inimigo fixo. Leave não inicia batalha. Não alterar opções, valores ou overrides.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "bca2d1c1623af110f528e9a4037e8af899669154da8169ca0c2932b7d4194a08",
  "evidencias": [
    {
      "jsonpath": "$.eventos[61].texto",
      "valor": "Resting upon an ancient stone plinth, you discover a horn, grand and ornate, that seems to sing with an unseen power. It is  enormous, constructed of what appeared to be bone or perhaps ivory, sheathed in fine metals and studded with twinkling jewels. Its dwarven craftsmanship is evident in the meticulous detailing, the intricate patterns that wound their way around the horn like a visual symphony.\n\nYou've heard tale of such horns of battle. Artifacts that summon allies when sounded... or enemies.\""
    },
    {
      "jsonpath": "$.eventos[61].texto_resultados_possiveis",
      "valor": "What will you do?"
    },
    {
      "jsonpath": "$.eventos[61].condicoes",
      "valor": {
        "disabled": 0,
        "EditorOnly": 0,
        "allowOnAllNodeTypes": 0,
        "allowedNodeTypes": [
          7
        ],
        "requiredStatusesToSpawn": [],
        "allowOnAllTerrainTypes": 1,
        "allowedTerrainTypes": [],
        "allowAtAllTimesOfDay": 1,
        "allowedTimeOfDay": 0,
        "allowAtAllLevels": 0,
        "minLevel": 3,
        "terrainTypesAllowedAtAnyTime": [],
        "KeepInDeckWhenUsed": 0,
        "isLesserEvent": 0,
        "LeadsToFortune": 0
      }
    },
    {
      "jsonpath": "$.eventos[61].modos",
      "valor": [
        {
          "valor": 0,
          "nome": "Campaign"
        },
        {
          "valor": 1,
          "nome": "Roguelike"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[61].historia",
      "valor": {
        "valor": 0,
        "nome": "NonStoryOnly"
      }
    },
    {
      "jsonpath": "$.eventos[61].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[61].origem.path_id",
      "valor": 2545611
    },
    {
      "jsonpath": "$.eventos[61].origem.caminhos_resource",
      "valor": [
        "events/horn of glorious battle"
      ]
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].titulo",
      "valor": "Blow the Horn"
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].texto",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].texto",
      "valor": "The sound that erupts is deep and rich, rolling across the landscape like a war drum. It echoes off the mountains, filling the air, the ground, your very bones with its call.\n\n\nThen, silence. A heavy, waiting silence. The echoes of the horn call still ringing in your ears, but everything else seems eerily quiet. And then, you hear it. The steady march of war, the cry of battle, the clatter of armaments. The call has been answered."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": true
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 1
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 1
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 1
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": [
        1,
        2,
        4,
        6,
        8,
        12,
        16,
        19,
        21,
        22,
        25,
        28,
        30,
        41,
        42,
        43,
        45,
        3,
        10,
        18
      ]
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": [
        2,
        4
      ]
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 2545610
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].titulo",
      "valor": "Leave"
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].texto",
      "valor": "The allure of the horn is powerful, but so is the dread of the unknown."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].texto",
      "valor": "With a final, lingering glance at the impressive artifact, you move away, leaving the horn untouched. "
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    }
  ],
  "mudancas": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[61].texto",
      "antes": "Resting upon an ancient stone plinth, you discover a horn, grand and ornate, that seems to sing with an unseen power. It is  enormous, constructed of what appeared to be bone or perhaps ivory, sheathed in fine metals and studded with twinkling jewels. Its dwarven craftsmanship is evident in the meticulous detailing, the intricate patterns that wound their way around the horn like a visual symphony.\n\nYou've heard tale of such horns of battle. Artifacts that summon allies when sounded... or enemies.\"",
      "depois": "Resting upon an ancient stone plinth, you discover a horn, grand and ornate, that seems to sing with an unseen power. It is enormous, constructed of what appears to be bone or perhaps ivory, sheathed in fine metals and studded with twinkling jewels. Its dwarven craftsmanship is evident in the meticulous detailing, the intricate patterns that wind their way around the horn like a visual symphony.\n\nYou've heard tale of such horns of battle. Artifacts that summon allies when sounded... or enemies.",
      "justificativa": "Correção editorial localizada; preserva o aviso sobre aliados ou inimigos e toda a descrição do artefato.",
      "substituicoes": [
        [
          "It is  enormous",
          "It is enormous"
        ],
        [
          "what appeared to be",
          "what appears to be"
        ],
        [
          "patterns that wound",
          "patterns that wind"
        ],
        [
          "... or enemies.\"",
          "... or enemies."
        ]
      ]
    }
  ],
  "nulls": [
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[1].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[1].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[1].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[1].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[1].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[61].opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[61].opcoes[1].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "referencias_catalogo": [
    {
      "chave": "resources.assets:2545610",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545610,
        "type": "MonoBehaviour",
        "script": "PartyEvent",
        "name": "Horn of Glorious Battle - Victory"
      }
    }
  ]
}
```

## Evento 62 — Inconspicuous Burning Demon Skull

Veredito: MELHORAR. MELHORAR o possessivo da narrativa existente, não criar uma descrição substituta. disabled=1 é preservado. Accept tem candidato Deal with a Devil (GoldMod, DropQuantityMod e ExperienceMod com expressão 50, duração Quest), sem batalha nem evento encadeado; Refuse não possui ações. A antiga alegação de encadeamento é retirada.

Natureza: somente proposta editorial de wording; nenhum valor mecânico, alvo, condição, raridade, peso, disabled ou referência recebe alteração.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 62,
  "json_index": 62,
  "chave": "resources.assets:2545612",
  "id": "0d898c20-9308-4239-98e6-a1d61fd531bf",
  "titulo": "Inconspicuous Burning Demon Skull",
  "categoria": "Normal",
  "raridade": {
    "valor": 1,
    "nome": "Uncommon"
  },
  "peso": 1.0,
  "disabled": 1,
  "texto_chars": 756,
  "veredito": "MELHORAR",
  "justificativa": "MELHORAR o possessivo da narrativa existente, não criar uma descrição substituta. disabled=1 é preservado. Accept tem candidato Deal with a Devil (GoldMod, DropQuantityMod e ExperienceMod com expressão 50, duração Quest), sem batalha nem evento encadeado; Refuse não possui ações. A antiga alegação de encadeamento é retirada.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "e07ef2dfae8664cc664f4c089816bd7196954cb67c77c283e7a11d87d4162117",
  "evidencias": [
    {
      "jsonpath": "$.eventos[62].texto",
      "valor": "Before you rests the <color=#EE4B2B><b>burning skull of an infernal fiend</b></color>. It's terrifying bone visage has been blackened by the flames that envelop it. As you approach a harsh voice enters your mind.\n\n<color=#EE4B2B><b>Demon Skull:</b></color> \"<i>Hello, mortal!</i>\"\n\n<color=#EE4B2B><b>Demon Skull:</b></color> \"<i>I am reluctant to admit that I am in need of some aid...</i>\"\n\n<color=#EE4B2B><b>Demon Skull:</b></color> \"<i>Perhaps we can help each other?! I need <color=#B0E0E6>SOULS</color>! And you need... loot and gold and such.</i>\" \n\n<color=#EE4B2B><b>Demon Skull:</b></color> \"<i>Bring me along with you and I will take the souls of those monsters you defeat and in return I will give you <color=#FFD700><b>TREASURE</b></color>!</i>\""
    },
    {
      "jsonpath": "$.eventos[62].texto_resultados_possiveis",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[62].condicoes",
      "valor": {
        "disabled": 1,
        "EditorOnly": 0,
        "allowOnAllNodeTypes": 0,
        "allowedNodeTypes": [
          7
        ],
        "requiredStatusesToSpawn": [],
        "allowOnAllTerrainTypes": 1,
        "allowedTerrainTypes": [
          0,
          1,
          2
        ],
        "allowAtAllTimesOfDay": 1,
        "allowedTimeOfDay": 0,
        "allowAtAllLevels": 1,
        "minLevel": 1,
        "terrainTypesAllowedAtAnyTime": [],
        "KeepInDeckWhenUsed": 0,
        "isLesserEvent": 0,
        "LeadsToFortune": 0
      }
    },
    {
      "jsonpath": "$.eventos[62].modos",
      "valor": [
        {
          "valor": 0,
          "nome": "Campaign"
        },
        {
          "valor": 1,
          "nome": "Roguelike"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[62].historia",
      "valor": {
        "valor": 0,
        "nome": "NonStoryOnly"
      }
    },
    {
      "jsonpath": "$.eventos[62].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[62].origem.path_id",
      "valor": 2545612
    },
    {
      "jsonpath": "$.eventos[62].origem.caminhos_resource",
      "valor": [
        "events/inconspicuous burning demon skull"
      ]
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].titulo",
      "valor": "Accept"
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].texto",
      "valor": "Disregard all morals and place the hellish skull into your bags. Gain [o1a1_status]."
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].texto",
      "valor": "You accept.\n\n<color=#EE4B2B><b>Demon Skull:</b></color> \"<i>Yessss... <b>I WILL FEAST UPON THEIR SOULS!</b></i>\""
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [
          {
            "chave": "resources.assets:2545378",
            "nome": "Deal with a Devil",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545378
            },
            "tipo": "EventStatus",
            "descricao": "<i><color=#808080>You've made a deal with a devil!</i></color> \n\nIncreases experience, item drops, and gold gained by 50%. ",
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
                  "chave": "resources.assets:2544424",
                  "nome": "GoldMod",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544424
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "50",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544419",
                  "nome": "DropQuantityMod",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544419
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "50",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544422",
                  "nome": "ExperienceMod",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544422
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "50",
                "segunda_passagem": false
              }
            ]
          }
        ],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[62].opcoes[1].titulo",
      "valor": "Refuse"
    },
    {
      "jsonpath": "$.eventos[62].opcoes[1].texto",
      "valor": "You think better of helping this soul hungry demon."
    },
    {
      "jsonpath": "$.eventos[62].opcoes[1].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[62].opcoes[1].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    }
  ],
  "mudancas": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[62].texto",
      "antes": "Before you rests the <color=#EE4B2B><b>burning skull of an infernal fiend</b></color>. It's terrifying bone visage has been blackened by the flames that envelop it. As you approach a harsh voice enters your mind.\n\n<color=#EE4B2B><b>Demon Skull:</b></color> \"<i>Hello, mortal!</i>\"\n\n<color=#EE4B2B><b>Demon Skull:</b></color> \"<i>I am reluctant to admit that I am in need of some aid...</i>\"\n\n<color=#EE4B2B><b>Demon Skull:</b></color> \"<i>Perhaps we can help each other?! I need <color=#B0E0E6>SOULS</color>! And you need... loot and gold and such.</i>\" \n\n<color=#EE4B2B><b>Demon Skull:</b></color> \"<i>Bring me along with you and I will take the souls of those monsters you defeat and in return I will give you <color=#FFD700><b>TREASURE</b></color>!</i>\"",
      "depois": "Before you rests the <color=#EE4B2B><b>burning skull of an infernal fiend</b></color>. Its terrifying bone visage has been blackened by the flames that envelop it. As you approach a harsh voice enters your mind.\n\n<color=#EE4B2B><b>Demon Skull:</b></color> \"<i>Hello, mortal!</i>\"\n\n<color=#EE4B2B><b>Demon Skull:</b></color> \"<i>I am reluctant to admit that I am in need of some aid...</i>\"\n\n<color=#EE4B2B><b>Demon Skull:</b></color> \"<i>Perhaps we can help each other?! I need <color=#B0E0E6>SOULS</color>! And you need... loot and gold and such.</i>\" \n\n<color=#EE4B2B><b>Demon Skull:</b></color> \"<i>Bring me along with you and I will take the souls of those monsters you defeat and in return I will give you <color=#FFD700><b>TREASURE</b></color>!</i>\"",
      "justificativa": "Its é possessivo; It's significa it is. Tags, diálogos e valores ficam intactos.",
      "substituicoes": [
        [
          "It's terrifying bone visage",
          "Its terrifying bone visage"
        ]
      ]
    }
  ],
  "nulls": [
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[62].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[62].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[62].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[62].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[62].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[62].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[62].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[62].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[62].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[62].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[62].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[62].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "referencias_catalogo": [
    {
      "chave": "resources.assets:2544419",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2544419,
        "type": "MonoBehaviour",
        "script": "CharacterAttribute",
        "name": "DropQuantityMod"
      }
    },
    {
      "chave": "resources.assets:2544422",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2544422,
        "type": "MonoBehaviour",
        "script": "CharacterAttribute",
        "name": "ExperienceMod"
      }
    },
    {
      "chave": "resources.assets:2544424",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2544424,
        "type": "MonoBehaviour",
        "script": "CharacterAttribute",
        "name": "GoldMod"
      }
    },
    {
      "chave": "resources.assets:2545378",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545378,
        "type": "MonoBehaviour",
        "script": "EventStatus",
        "name": "Deal with a Devil"
      }
    }
  ]
}
```

## Evento 63 — Jewelry Box

Veredito: MELHORAR. MELHORAR preenchendo somente o texto narrativo realmente vazio da variante Roguelike. Open tem uma ação Success sem combate, dar itens=true, quantidade_configurada=2, limitItemTypes=1/possibleItemTypes=[4,5] e limitItemRarities=1/possibleRarities=[2,3]. O novo texto não anuncia tipo decodificado, valor, quantidade final ou tesouro garantido além da configuração.

Natureza: somente proposta editorial de wording; nenhum valor mecânico, alvo, condição, raridade, peso, disabled ou referência recebe alteração.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 63,
  "json_index": 63,
  "chave": "resources.assets:2545616",
  "id": "873ac971-40c8-4fd4-8bad-1a69d2ec6fca",
  "titulo": "Jewelry Box",
  "categoria": "Normal",
  "raridade": {
    "valor": 1,
    "nome": "Uncommon"
  },
  "peso": 1.0,
  "disabled": 0,
  "texto_chars": 0,
  "veredito": "MELHORAR",
  "justificativa": "MELHORAR preenchendo somente o texto narrativo realmente vazio da variante Roguelike. Open tem uma ação Success sem combate, dar itens=true, quantidade_configurada=2, limitItemTypes=1/possibleItemTypes=[4,5] e limitItemRarities=1/possibleRarities=[2,3]. O novo texto não anuncia tipo decodificado, valor, quantidade final ou tesouro garantido além da configuração.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "77d0b454bb1e84ecd52813b25e5f92696ed212786271040378e88e489fc44db6",
  "evidencias": [
    {
      "jsonpath": "$.eventos[63].texto",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[63].texto_resultados_possiveis",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[63].condicoes",
      "valor": {
        "disabled": 0,
        "EditorOnly": 0,
        "allowOnAllNodeTypes": 0,
        "allowedNodeTypes": [
          3
        ],
        "requiredStatusesToSpawn": [],
        "allowOnAllTerrainTypes": 1,
        "allowedTerrainTypes": [
          3,
          4,
          9,
          0
        ],
        "allowAtAllTimesOfDay": 1,
        "allowedTimeOfDay": 0,
        "allowAtAllLevels": 1,
        "minLevel": 1,
        "terrainTypesAllowedAtAnyTime": [],
        "KeepInDeckWhenUsed": 0,
        "isLesserEvent": 0,
        "LeadsToFortune": 0
      }
    },
    {
      "jsonpath": "$.eventos[63].modos",
      "valor": [
        {
          "valor": 1,
          "nome": "Roguelike"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[63].historia",
      "valor": {
        "valor": 2,
        "nome": "Both"
      }
    },
    {
      "jsonpath": "$.eventos[63].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[63].origem.path_id",
      "valor": 2545616
    },
    {
      "jsonpath": "$.eventos[63].origem.caminhos_resource",
      "valor": [
        "events/jewelry box - roguelike"
      ]
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].titulo",
      "valor": "Open"
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].texto",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].texto",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
        "dar": true,
        "pool_tipo": {
          "valor": 2,
          "nome": "Unassigned"
        },
        "quantidade_configurada": 2,
        "tabelas": [],
        "restricoes": {
          "limitItemTypes": 1,
          "possibleItemTypes": [
            4,
            5
          ],
          "limitItemRarities": 1,
          "possibleRarities": [
            2,
            3
          ]
        },
        "sorteio_final": null,
        "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
      }
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    }
  ],
  "mudancas": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[63].texto",
      "antes": "",
      "depois": "A jewelry box rests before you. Open it to see what it holds.",
      "justificativa": "Adicionar contexto mínimo à interação Open sem inventar local, perigo ou efeitos.",
      "substituicoes": []
    }
  ],
  "nulls": [
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[63].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[63].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[63].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[63].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[63].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[63].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[63].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[63].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[63].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[63].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[63].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[63].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "referencias_catalogo": []
}
```

## Evento 64 — Jewelry Box

Veredito: MELHORAR. MELHORAR gramática da narrativa e o nome do recipiente na opção Open. Esta variante tem narrativa preenchida, minLevel=3, Campaign/Roguelike e uma ação que inicia combate: referência Cursed Chest Battle, mas o override contém três ForcedEnemies com CharacterInfo path_id=2545163, DisableSuperUnique=1 e VictoryEvent path_id=2545617. O nome do template não substitui esse override. Leave não inicia combate; nenhum resultado novo é prometido.

Natureza: somente proposta editorial de wording; nenhum valor mecânico, alvo, condição, raridade, peso, disabled ou referência recebe alteração.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 64,
  "json_index": 64,
  "chave": "resources.assets:2545618",
  "id": "3415fc65-d04d-4f99-9689-cb822c0fd365",
  "titulo": "Jewelry Box",
  "categoria": "Normal",
  "raridade": {
    "valor": 1,
    "nome": "Uncommon"
  },
  "peso": 1.0,
  "disabled": 0,
  "texto_chars": 327,
  "veredito": "MELHORAR",
  "justificativa": "MELHORAR gramática da narrativa e o nome do recipiente na opção Open. Esta variante tem narrativa preenchida, minLevel=3, Campaign/Roguelike e uma ação que inicia combate: referência Cursed Chest Battle, mas o override contém três ForcedEnemies com CharacterInfo path_id=2545163, DisableSuperUnique=1 e VictoryEvent path_id=2545617. O nome do template não substitui esse override. Leave não inicia combate; nenhum resultado novo é prometido.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "75582720b12dff2de031b7ab036c911ac2de48db2e3518664a872bbf3311e55f",
  "evidencias": [
    {
      "jsonpath": "$.eventos[64].texto",
      "valor": "In the middle of a musty, long-forgotten chamber, a jewel box lays unattended. The rich gold lining shimmers in the feeble torchlight, a stark contrast to the somber surroundings. The wood, once stained a regal purple, has dulled over time, but still retains a sort of nobility in its bearing.\n\nA fortunate and unexpected find."
    },
    {
      "jsonpath": "$.eventos[64].texto_resultados_possiveis",
      "valor": "What will you do?"
    },
    {
      "jsonpath": "$.eventos[64].condicoes",
      "valor": {
        "disabled": 0,
        "EditorOnly": 0,
        "allowOnAllNodeTypes": 0,
        "allowedNodeTypes": [
          7
        ],
        "requiredStatusesToSpawn": [],
        "allowOnAllTerrainTypes": 0,
        "allowedTerrainTypes": [
          0,
          3,
          9,
          4
        ],
        "allowAtAllTimesOfDay": 1,
        "allowedTimeOfDay": 1,
        "allowAtAllLevels": 0,
        "minLevel": 3,
        "terrainTypesAllowedAtAnyTime": [
          4,
          0,
          3,
          9
        ],
        "KeepInDeckWhenUsed": 0,
        "isLesserEvent": 0,
        "LeadsToFortune": 1
      }
    },
    {
      "jsonpath": "$.eventos[64].modos",
      "valor": [
        {
          "valor": 0,
          "nome": "Campaign"
        },
        {
          "valor": 1,
          "nome": "Roguelike"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[64].historia",
      "valor": {
        "valor": 0,
        "nome": "NonStoryOnly"
      }
    },
    {
      "jsonpath": "$.eventos[64].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[64].origem.path_id",
      "valor": 2545618
    },
    {
      "jsonpath": "$.eventos[64].origem.caminhos_resource",
      "valor": [
        "events/jewelry box mimic"
      ]
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].titulo",
      "valor": "Open"
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].texto",
      "valor": "Open the chest."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].rolagem",
      "valor": {
        "bonus": [
          {
            "valor": 3,
            "nome": "Intelligence"
          }
        ],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].texto",
      "valor": "Your hand barely brushes the surface of the box when it shivers, not with the inanimate tremor of an object moved, but with a living, organic twitch. You yank your hand back as the box's lid splits open, revealing a maw lined with gleaming, razor-sharp teeth."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": true
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": "resources.assets:2544645",
        "nome": "Cursed Chest Battle",
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2544645
        },
        "tipo": "BattleInfo"
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 1
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": [
        {
          "OverrideEnemyName": 0,
          "NameOverride": "Mimic",
          "CharacterInfo": {
            "m_FileID": 0,
            "m_PathID": 2545163
          },
          "ForcedEnemyMods": [],
          "IsSuperUnique": 0
        },
        {
          "OverrideEnemyName": 0,
          "NameOverride": "Mimic",
          "CharacterInfo": {
            "m_FileID": 0,
            "m_PathID": 2545163
          },
          "ForcedEnemyMods": [],
          "IsSuperUnique": 0
        },
        {
          "OverrideEnemyName": 0,
          "NameOverride": "Mimic",
          "CharacterInfo": {
            "m_FileID": 0,
            "m_PathID": 2545163
          },
          "ForcedEnemyMods": [],
          "IsSuperUnique": 0
        }
      ]
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 1
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 2545617
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 2.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].titulo",
      "valor": "Leave"
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].texto",
      "valor": "Leave the dusty box undisturbed."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].texto",
      "valor": "The Stolen Realm is a dangerous world, where even the most enticing treasures could mask deadly threats."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    }
  ],
  "mudancas": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[64].texto",
      "antes": "In the middle of a musty, long-forgotten chamber, a jewel box lays unattended. The rich gold lining shimmers in the feeble torchlight, a stark contrast to the somber surroundings. The wood, once stained a regal purple, has dulled over time, but still retains a sort of nobility in its bearing.\n\nA fortunate and unexpected find.",
      "depois": "In the middle of a musty, long-forgotten chamber, a jewel box lies unattended. The rich gold lining shimmers in the feeble torchlight, a stark contrast to the somber surroundings. The wood, once stained a regal purple, has dulled over time, but still retains a sort of nobility in its bearing.\n\nA fortunate and unexpected find.",
      "justificativa": "Lies é o verbo intransitivo adequado; mantém a surpresa do mimic na ação seguinte.",
      "substituicoes": [
        [
          "a jewel box lays unattended",
          "a jewel box lies unattended"
        ]
      ]
    },
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[64].opcoes[0].texto",
      "antes": "Open the chest.",
      "depois": "Open the jewelry box.",
      "justificativa": "O recipiente descrito e titulado é Jewelry Box; corrigir chest para jewelry box sem anunciar a surpresa de combate.",
      "substituicoes": []
    }
  ],
  "nulls": [
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[64].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[64].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[64].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[64].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[64].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[64].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[64].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[64].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[64].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[64].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[64].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[64].opcoes[1].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[64].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[64].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[64].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    }
  ],
  "referencias_catalogo": [
    {
      "chave": "resources.assets:2544645",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2544645,
        "type": "MonoBehaviour",
        "script": "BattleInfo",
        "name": "Cursed Chest Battle"
      }
    },
    {
      "chave": "resources.assets:2545163",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545163,
        "type": "MonoBehaviour",
        "script": "CharacterInfo",
        "name": "Lesser Mimic"
      }
    },
    {
      "chave": "resources.assets:2545617",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545617,
        "type": "MonoBehaviour",
        "script": "PartyEvent",
        "name": "Jewelry Box Mimic Victory"
      }
    }
  ]
}
```

## Evento 65 — Jewelry Box

Veredito: MELHORAR. MELHORAR preenchendo somente a narrativa realmente vazia da variante Campaign, sem mesclar com #63 ou #64. Open configura itens dar=true, quantidade_configurada=1 e mesmas restrições [4,5]/[2,3], sem batalha. Quantidade final e sorteio continuam NULL; o texto compartilhado com #63 é uma sugestão editorial, não igualdade de identidade ou recompensa.

Natureza: somente proposta editorial de wording; nenhum valor mecânico, alvo, condição, raridade, peso, disabled ou referência recebe alteração.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 65,
  "json_index": 65,
  "chave": "resources.assets:2545619",
  "id": "c7086146-8450-4146-b6b1-4bc830580aa0",
  "titulo": "Jewelry Box",
  "categoria": "Normal",
  "raridade": {
    "valor": 1,
    "nome": "Uncommon"
  },
  "peso": 1.0,
  "disabled": 0,
  "texto_chars": 0,
  "veredito": "MELHORAR",
  "justificativa": "MELHORAR preenchendo somente a narrativa realmente vazia da variante Campaign, sem mesclar com #63 ou #64. Open configura itens dar=true, quantidade_configurada=1 e mesmas restrições [4,5]/[2,3], sem batalha. Quantidade final e sorteio continuam NULL; o texto compartilhado com #63 é uma sugestão editorial, não igualdade de identidade ou recompensa.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "335d04526687a7504428854cd3c3f7922957e0824d50e0e300569ca978932fa4",
  "evidencias": [
    {
      "jsonpath": "$.eventos[65].texto",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[65].texto_resultados_possiveis",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[65].condicoes",
      "valor": {
        "disabled": 0,
        "EditorOnly": 0,
        "allowOnAllNodeTypes": 0,
        "allowedNodeTypes": [
          3
        ],
        "requiredStatusesToSpawn": [],
        "allowOnAllTerrainTypes": 1,
        "allowedTerrainTypes": [
          3,
          4,
          9,
          0
        ],
        "allowAtAllTimesOfDay": 1,
        "allowedTimeOfDay": 0,
        "allowAtAllLevels": 1,
        "minLevel": 1,
        "terrainTypesAllowedAtAnyTime": [],
        "KeepInDeckWhenUsed": 0,
        "isLesserEvent": 0,
        "LeadsToFortune": 0
      }
    },
    {
      "jsonpath": "$.eventos[65].modos",
      "valor": [
        {
          "valor": 0,
          "nome": "Campaign"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[65].historia",
      "valor": {
        "valor": 2,
        "nome": "Both"
      }
    },
    {
      "jsonpath": "$.eventos[65].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[65].origem.path_id",
      "valor": 2545619
    },
    {
      "jsonpath": "$.eventos[65].origem.caminhos_resource",
      "valor": [
        "events/jewelry box"
      ]
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].titulo",
      "valor": "Open"
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].texto",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].texto",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
        "dar": true,
        "pool_tipo": {
          "valor": 2,
          "nome": "Unassigned"
        },
        "quantidade_configurada": 1,
        "tabelas": [],
        "restricoes": {
          "limitItemTypes": 1,
          "possibleItemTypes": [
            4,
            5
          ],
          "limitItemRarities": 1,
          "possibleRarities": [
            2,
            3
          ]
        },
        "sorteio_final": null,
        "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
      }
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    }
  ],
  "mudancas": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[65].texto",
      "antes": "",
      "depois": "A jewelry box rests before you. Open it to see what it holds.",
      "justificativa": "Contextualizar Open sem inventar altar, oferenda ou novas mecânicas.",
      "substituicoes": []
    }
  ],
  "nulls": [
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[65].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[65].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[65].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[65].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[65].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[65].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[65].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[65].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[65].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[65].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[65].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[65].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "referencias_catalogo": []
}
```

## Evento 66 — Lady of the Well

Veredito: MANTER. MANTER neste lote. A narrativa já contextualiza a figura espectral; Investigate a aproxima e inicia batalha com ForcedEnemies CharacterInfo path_id=2545113 e VictoryEvent path_id=2545620. Flee não inicia batalha, mas aplica Crippled e Bruised com sortear=false no efeito de alvo default serializado Self (override=false), não Party. Não interpretar o requisito de spawn com m_PathID=0 como status efetivo. Condições de terreno e minLevel=3 preservadas. Não há base para substituí-la pelo evento fictício Mysterious Altar.

MANTER significa nenhum depois proposto neste lote; não certifica perfeição de estilo, acesso no jogo ou ausência de questões fora de escopo.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 66,
  "json_index": 66,
  "chave": "resources.assets:2545621",
  "id": "32df0034-5a64-4155-92a5-62c6da8c4322",
  "titulo": "Lady of the Well",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 0,
  "texto_chars": 1209,
  "veredito": "MANTER",
  "justificativa": "MANTER neste lote. A narrativa já contextualiza a figura espectral; Investigate a aproxima e inicia batalha com ForcedEnemies CharacterInfo path_id=2545113 e VictoryEvent path_id=2545620. Flee não inicia batalha, mas aplica Crippled e Bruised com sortear=false no efeito de alvo default serializado Self (override=false), não Party. Não interpretar o requisito de spawn com m_PathID=0 como status efetivo. Condições de terreno e minLevel=3 preservadas. Não há base para substituí-la pelo evento fictício Mysterious Altar.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "04c4c09e1998e5fa17491d2ba2d709a5442989e5e23162ec5d36113cdb55e364",
  "evidencias": [
    {
      "jsonpath": "$.eventos[66].texto",
      "valor": "A malaise sweeps over the land as a nebulous shroud emerges from the mouth of an ancient, sealed well. The fog is ethereal, a sickly blend of grays and whites that coil and spin, obscuring the landscape and casting a ghostly pallor over all it touches. It is an aberration, nature corrupted, as if the well was breathing out the stale air of forgotten secrets.\n\n\nFloating above the well is the spectral figure of a <violet><b><incr>Young Lady</incr></b></violet>, her feet barely grazing the crumbling stone rim. Her garments, once likely the finery of a noblewoman, are stained with centuries of dirt and grime. Her hair, matted and wild, tumbles about her in an untamed veil, obscuring her features but for the haunting glint of her eyes.\n\n\nStill as an alabaster statue, she emanates an air of tragic beauty. But it is her eyes that held the most terror. For within their depths gleamed an unnatural light, not of this world, reflecting an existence spent trapped between realms. As you shift uneasily beneath her unwavering gaze, it becomes evident - her sightless eyes track you, observing your every move with an intensity that speaks of longing, despair, and a lingering echo of the world she once knew."
    },
    {
      "jsonpath": "$.eventos[66].texto_resultados_possiveis",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[66].condicoes",
      "valor": {
        "disabled": 0,
        "EditorOnly": 0,
        "allowOnAllNodeTypes": 0,
        "allowedNodeTypes": [
          7
        ],
        "requiredStatusesToSpawn": [
          {
            "m_FileID": 0,
            "m_PathID": 0
          }
        ],
        "allowOnAllTerrainTypes": 0,
        "allowedTerrainTypes": [
          8
        ],
        "allowAtAllTimesOfDay": 1,
        "allowedTimeOfDay": 1,
        "allowAtAllLevels": 0,
        "minLevel": 3,
        "terrainTypesAllowedAtAnyTime": [
          3
        ],
        "KeepInDeckWhenUsed": 0,
        "isLesserEvent": 0,
        "LeadsToFortune": 1
      }
    },
    {
      "jsonpath": "$.eventos[66].modos",
      "valor": [
        {
          "valor": 0,
          "nome": "Campaign"
        },
        {
          "valor": 1,
          "nome": "Roguelike"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[66].historia",
      "valor": {
        "valor": 0,
        "nome": "NonStoryOnly"
      }
    },
    {
      "jsonpath": "$.eventos[66].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[66].origem.path_id",
      "valor": 2545621
    },
    {
      "jsonpath": "$.eventos[66].origem.caminhos_resource",
      "valor": [
        "events/lady of the well"
      ]
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].titulo",
      "valor": "Investigate"
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].texto",
      "valor": "Approach the <violet><b><incr>Lady in the Well</incr></b></violet>."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].texto",
      "valor": "Compelled by curiosity, you cautiously approach the well, your eyes fixed on the ethereal lady. The air around you seems to cool and thicken, the eerie fog swirls and dances around your ankles as if alive. Your heart hammers in your chest, the only sound piercing the suffocating silence of the forgotten landscape.\n\n\nAs you draw near, a horrifying transformation takes place. The spectral figure's passive demeanor abruptly fractures. Her lips pull back into a furious snarl, revealing a grotesque mouth lined with jagged, yellow teeth. Her once serene eyes now burn with a wild, unholy fire, illuminating the well with their malicious glow.\n\n\nA chilling shriek splits the air, the sound so raw and piercing that it rattles your bones and echoes in your ears. The fog around the well roils and churns, taking on the hue of a stormy sea as the specter's anger manifested."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": true
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": [
        {
          "OverrideEnemyName": 0,
          "NameOverride": "",
          "CharacterInfo": {
            "m_FileID": 0,
            "m_PathID": 2545113
          },
          "ForcedEnemyMods": [],
          "IsSuperUnique": 0
        }
      ]
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 2545620
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].titulo",
      "valor": "Flee"
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].texto",
      "valor": "Something about the Lady in the Well unsettles you. Attempt to flee."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].texto",
      "valor": "Fear, as tangible as the chill in the air, seizes your heart. The young woman's spectral gaze is not merely unsettling; it is a manifestation of a reality too chilling to comprehend.\n\nTurning heel, you flee. Your once sturdy resolve gives way to blind panic, your steps echoing a wild, discordant symphony against the forest floor. \n\nA hidden root, reaching out from the undergrowth like a gnarled hand, catches your foot mid-stride, upending you. With a gasp of pain and surprise, you crash heavily into the tangle of roots and moss, your ankle sending shoots of searing pain up your leg."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [
          {
            "chave": "resources.assets:2545492",
            "nome": "Crippled",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545492
            },
            "tipo": "EventStatus",
            "descricao": "Reduces @Movement Points@ by @1@ per stack.",
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
                  "chave": "resources.assets:2544483",
                  "nome": "TurnFreeMovementPoints",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544483
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "-1",
                "segunda_passagem": false
              }
            ]
          },
          {
            "chave": "resources.assets:2545490",
            "nome": "Bruised",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545490
            },
            "tipo": "EventStatus",
            "descricao": "Reduces @Max Health@ by @10%@ per stack.",
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
                  "chave": "resources.assets:2544436",
                  "nome": "MaxHealth",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544436
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 1,
                  "nome": "Percentage"
                },
                "expressao": "-10",
                "segunda_passagem": true
              }
            ]
          }
        ],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    }
  ],
  "mudancas": [],
  "nulls": [
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[1].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[1].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[1].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[1].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[1].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[66].opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[66].opcoes[1].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "referencias_catalogo": [
    {
      "chave": "resources.assets:2544436",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2544436,
        "type": "MonoBehaviour",
        "script": "CharacterAttribute",
        "name": "MaxHealth"
      }
    },
    {
      "chave": "resources.assets:2544483",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2544483,
        "type": "MonoBehaviour",
        "script": "CharacterAttribute",
        "name": "TurnFreeMovementPoints"
      }
    },
    {
      "chave": "resources.assets:2545113",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545113,
        "type": "MonoBehaviour",
        "script": "CharacterInfo",
        "name": "Lady of the Well"
      }
    },
    {
      "chave": "resources.assets:2545490",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545490,
        "type": "MonoBehaviour",
        "script": "EventStatus",
        "name": "Bruised"
      }
    },
    {
      "chave": "resources.assets:2545492",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545492,
        "type": "MonoBehaviour",
        "script": "EventStatus",
        "name": "Crippled"
      }
    },
    {
      "chave": "resources.assets:2545620",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545620,
        "type": "MonoBehaviour",
        "script": "PartyEvent",
        "name": "Lady of the Well - Victory"
      }
    }
  ]
}
```

## Evento 67 — Large Chest

Veredito: MELHORAR. MELHORAR somente a narrativa realmente vazia. Large Chest tem isLesserEvent=1 e Open, uma ação Success sem batalha. Itens dar=true, quantidade_configurada=1, tipos configurados [0,1,2,3,4,5,7] com restrição ligada e raridades [1,2] com restrição ligada. Não chamar o baú de amaldiçoado, não inventar inimigos ou atribuir raridade de item igual à raridade Rare do evento.

Natureza: somente proposta editorial de wording; nenhum valor mecânico, alvo, condição, raridade, peso, disabled ou referência recebe alteração.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 67,
  "json_index": 67,
  "chave": "resources.assets:2545622",
  "id": "38a07b13-77ae-4a04-98a5-237b10c31bce",
  "titulo": "Large Chest",
  "categoria": "Normal",
  "raridade": {
    "valor": 2,
    "nome": "Rare"
  },
  "peso": 1.0,
  "disabled": 0,
  "texto_chars": 0,
  "veredito": "MELHORAR",
  "justificativa": "MELHORAR somente a narrativa realmente vazia. Large Chest tem isLesserEvent=1 e Open, uma ação Success sem batalha. Itens dar=true, quantidade_configurada=1, tipos configurados [0,1,2,3,4,5,7] com restrição ligada e raridades [1,2] com restrição ligada. Não chamar o baú de amaldiçoado, não inventar inimigos ou atribuir raridade de item igual à raridade Rare do evento.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "fdf6ed4c66c44c2f5e6e5150acba01a29a8ce5567ba2c47445409f4ad8a44b81",
  "evidencias": [
    {
      "jsonpath": "$.eventos[67].texto",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[67].texto_resultados_possiveis",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[67].condicoes",
      "valor": {
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
        "isLesserEvent": 1,
        "LeadsToFortune": 0
      }
    },
    {
      "jsonpath": "$.eventos[67].modos",
      "valor": [
        {
          "valor": 0,
          "nome": "Campaign"
        },
        {
          "valor": 1,
          "nome": "Roguelike"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[67].historia",
      "valor": {
        "valor": 2,
        "nome": "Both"
      }
    },
    {
      "jsonpath": "$.eventos[67].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[67].origem.path_id",
      "valor": 2545622
    },
    {
      "jsonpath": "$.eventos[67].origem.caminhos_resource",
      "valor": [
        "events/large chest"
      ]
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].titulo",
      "valor": "Open"
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].texto",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].texto",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 0.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
        "dar": true,
        "pool_tipo": {
          "valor": 2,
          "nome": "Unassigned"
        },
        "quantidade_configurada": 1,
        "tabelas": [],
        "restricoes": {
          "limitItemTypes": 1,
          "possibleItemTypes": [
            0,
            1,
            2,
            3,
            4,
            5,
            7
          ],
          "limitItemRarities": 1,
          "possibleRarities": [
            1,
            2
          ]
        },
        "sorteio_final": null,
        "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
      }
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    }
  ],
  "mudancas": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[67].texto",
      "antes": "",
      "depois": "A large chest stands before you. Open it to see what it holds.",
      "justificativa": "Descrição curta compatível com uma interação menor, sem introduzir localização ou riscos não presentes.",
      "substituicoes": []
    }
  ],
  "nulls": [
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[67].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[67].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[67].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[67].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[67].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[67].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[67].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[67].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[67].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[67].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[67].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[67].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "referencias_catalogo": []
}
```

## Evento 68 — Large Pile of Gold

Veredito: MANTER. MANTER. A frase existente já descreve a pilha de moedas e Take é inequívoco. A ação configura ouro dar=true/retirar=false/razao=3.0 e não inicia combate. A quantidade de ouro final é NULL, não três moedas nem zero; itens têm dar=false apesar de quantidade_configurada=2. Não acrescentar ganho fixo ou outra recompensa.

MANTER significa nenhum depois proposto neste lote; não certifica perfeição de estilo, acesso no jogo ou ausência de questões fora de escopo.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 68,
  "json_index": 68,
  "chave": "resources.assets:2545623",
  "id": "b2aed602-4583-45b3-a736-ee05bbe4c915",
  "titulo": "Large Pile of Gold",
  "categoria": "Normal",
  "raridade": {
    "valor": 1,
    "nome": "Uncommon"
  },
  "peso": 1.0,
  "disabled": 0,
  "texto_chars": 48,
  "veredito": "MANTER",
  "justificativa": "MANTER. A frase existente já descreve a pilha de moedas e Take é inequívoco. A ação configura ouro dar=true/retirar=false/razao=3.0 e não inicia combate. A quantidade de ouro final é NULL, não três moedas nem zero; itens têm dar=false apesar de quantidade_configurada=2. Não acrescentar ganho fixo ou outra recompensa.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "4e72b4e6bfdc7e86995d68349b4972f1e8b9e462e7b436e48a3857266c5e9116",
  "evidencias": [
    {
      "jsonpath": "$.eventos[68].texto",
      "valor": "A large pile of gold coins glitters before you. "
    },
    {
      "jsonpath": "$.eventos[68].texto_resultados_possiveis",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[68].condicoes",
      "valor": {
        "disabled": 0,
        "EditorOnly": 0,
        "allowOnAllNodeTypes": 0,
        "allowedNodeTypes": [
          3
        ],
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
      }
    },
    {
      "jsonpath": "$.eventos[68].modos",
      "valor": [
        {
          "valor": 0,
          "nome": "Campaign"
        },
        {
          "valor": 1,
          "nome": "Roguelike"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[68].historia",
      "valor": {
        "valor": 2,
        "nome": "Both"
      }
    },
    {
      "jsonpath": "$.eventos[68].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[68].origem.path_id",
      "valor": 2545623
    },
    {
      "jsonpath": "$.eventos[68].origem.caminhos_resource",
      "valor": [
        "events/large pile of gold"
      ]
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].titulo",
      "valor": "Take"
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].texto",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].texto",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": true,
        "retirar": false,
        "razao": 3.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
        "dar": false,
        "pool_tipo": {
          "valor": 2,
          "nome": "Unassigned"
        },
        "quantidade_configurada": 2,
        "tabelas": [],
        "restricoes": {
          "limitItemTypes": 1,
          "possibleItemTypes": [
            6,
            7
          ],
          "limitItemRarities": 0,
          "possibleRarities": [
            1
          ]
        },
        "sorteio_final": null,
        "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
      }
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    }
  ],
  "mudancas": [],
  "nulls": [
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[68].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[68].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[68].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[68].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[68].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[68].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[68].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[68].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[68].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[68].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[68].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[68].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "referencias_catalogo": []
}
```

## Evento 69 — Lightning Sentry

Veredito: MELHORAR. MELHORAR somente erros nimbel e a erratic na ação Failure. Disarm usa bônus Intelligence; Success tem limite_rolagem=10 e XP dar=true/razao=1.0 com alvo Party. Failure tem limite_rolagem=1, percentMaxMana=-30 e candidato Shocked, também Party. Nenhuma das ações inicia combate; valores, status e tokens de personagem não serão alterados.

Natureza: somente proposta editorial de wording; nenhum valor mecânico, alvo, condição, raridade, peso, disabled ou referência recebe alteração.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 69,
  "json_index": 69,
  "chave": "resources.assets:2545624",
  "id": "3c3685cf-05c2-401b-bb42-bd85ae039034",
  "titulo": "Lightning Sentry",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 0,
  "texto_chars": 525,
  "veredito": "MELHORAR",
  "justificativa": "MELHORAR somente erros nimbel e a erratic na ação Failure. Disarm usa bônus Intelligence; Success tem limite_rolagem=10 e XP dar=true/razao=1.0 com alvo Party. Failure tem limite_rolagem=1, percentMaxMana=-30 e candidato Shocked, também Party. Nenhuma das ações inicia combate; valores, status e tokens de personagem não serão alterados.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "2afe8c2022e7653ca3542c505f7a80a557491fd86226b5ab6640f5c23a98bcda",
  "evidencias": [
    {
      "jsonpath": "$.eventos[69].texto",
      "valor": "A tempest of arcing electricity announces the existence of the <blue><b><incr>Lightning Sentry</incr></b></blue>. It stands tall and resolute, like a beacon of raw, crackling power, its metallic structure hums with the melody of contained lightning. A towering column of copper and gold, crowned by a sphere of writhing electric currents that cast flickering shadows across the stone floor. Its azure lightning arcs strike randomly, a dance of deadly energy that promises swift, sizzling retribution to any who dare approach."
    },
    {
      "jsonpath": "$.eventos[69].texto_resultados_possiveis",
      "valor": "Who will attempt to disarm the trap?"
    },
    {
      "jsonpath": "$.eventos[69].condicoes",
      "valor": {
        "disabled": 0,
        "EditorOnly": 0,
        "allowOnAllNodeTypes": 0,
        "allowedNodeTypes": [
          7
        ],
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
      }
    },
    {
      "jsonpath": "$.eventos[69].modos",
      "valor": [
        {
          "valor": 0,
          "nome": "Campaign"
        },
        {
          "valor": 1,
          "nome": "Roguelike"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[69].historia",
      "valor": {
        "valor": 0,
        "nome": "NonStoryOnly"
      }
    },
    {
      "jsonpath": "$.eventos[69].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[69].origem.path_id",
      "valor": 2545624
    },
    {
      "jsonpath": "$.eventos[69].origem.caminhos_resource",
      "valor": [
        "events/lightning sentry"
      ]
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].titulo",
      "valor": "Disarm"
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].texto",
      "valor": "Use your knowledge of such traps to disarm."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].rolagem",
      "valor": {
        "bonus": [
          {
            "valor": 3,
            "nome": "Intelligence"
          }
        ],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].texto",
      "valor": "[name] studies the pulsating dance of electricity, following the arcs of lightning as they flicker from the orb to the surrounding environment.\n\nAs the azure flashes lick the air, [he] sees the pattern, the logic behind the lightning's frenzied ballet. [his] fingers trace unseen circuits in the air, [his] mind whirring with calculations and theories.\n\n[name] raises [his] weapon to the metal surface of the sentry, there is a loud hiss, a shower of sparks, and then the blinding light of the energy globe dims. The arcs of lightning slow, their wild dance turning sluggish until, with a final, pathetic spark, they cease entirely."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 10
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": true,
        "tipo_override": {
          "valor": 2,
          "nome": "Party"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": true,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].texto",
      "valor": "[name] steps forward. [His] fingers, nimbel and swift, move to manipulate the conduit channels to redirect the lethal energy safely. But the searing arcs are unpredictable, pulsing with a erratic energy that resists [his] touch.\n\nWith a sudden, violent snap, an arc of energy lashes out at [name]. [He] lets out a strangled cry, reeling back as the electric discharge courses through [him], scorching [his] senses and leaving [him] stunned on the ground."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].resultado",
      "valor": {
        "valor": 1,
        "nome": "Failure"
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].limite_rolagem",
      "valor": 1
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": -30.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].efeitos[0].alvo",
      "valor": {
        "override": true,
        "tipo_override": {
          "valor": 2,
          "nome": "Party"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [
          {
            "chave": "resources.assets:2545500",
            "nome": "Shocked",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545500
            },
            "tipo": "EventStatus",
            "descricao": "Reduces @Lightning Resistance@ by @25%@ per stack.",
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
                  "chave": "resources.assets:2544499",
                  "nome": "ResistLightning",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544499
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "-25",
                "segunda_passagem": false
              }
            ]
          }
        ],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].efeitos[0].recompensas.skills",
      "valor": []
    }
  ],
  "mudancas": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].texto",
      "antes": "[name] steps forward. [His] fingers, nimbel and swift, move to manipulate the conduit channels to redirect the lethal energy safely. But the searing arcs are unpredictable, pulsing with a erratic energy that resists [his] touch.\n\nWith a sudden, violent snap, an arc of energy lashes out at [name]. [He] lets out a strangled cry, reeling back as the electric discharge courses through [him], scorching [his] senses and leaving [him] stunned on the ground.",
      "depois": "[name] steps forward. [His] fingers, nimble and swift, move to manipulate the conduit channels to redirect the lethal energy safely. But the searing arcs are unpredictable, pulsing with an erratic energy that resists [his] touch.\n\nWith a sudden, violent snap, an arc of energy lashes out at [name]. [He] lets out a strangled cry, reeling back as the electric discharge courses through [him], scorching [his] senses and leaving [him] stunned on the ground.",
      "justificativa": "Corrigir ortografia e artigo; preservar [name], [His], [his], [He], [him] e o conteúdo narrativo do fracasso.",
      "substituicoes": [
        [
          "nimbel and swift",
          "nimble and swift"
        ],
        [
          "a erratic energy",
          "an erratic energy"
        ]
      ]
    }
  ],
  "nulls": [
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].efeitos[1].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].efeitos[1].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].efeitos[1].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].efeitos[1].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].efeitos[1].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].efeitos[1].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].recompensas[1].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].recompensas[1].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].recompensas[1].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].recompensas[1].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].recompensas[1].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].recompensas[1].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[69].opcoes[0].recompensas[1].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[69].opcoes[0].recompensas[1].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "referencias_catalogo": [
    {
      "chave": "resources.assets:2544499",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2544499,
        "type": "MonoBehaviour",
        "script": "CharacterAttribute",
        "name": "ResistLightning"
      }
    },
    {
      "chave": "resources.assets:2545500",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545500,
        "type": "MonoBehaviour",
        "script": "EventStatus",
        "name": "Shocked"
      }
    }
  ]
}
```

## Evento 70 — Magic Mirror

Veredito: MANTER. MANTER neste lote. Strike explica a tentativa de quebrar o espelho: Success limite=18 concede XP (razao=1.0) e candidato Mirror Shard, sem batalha; Failure limite=1 inicia batalha com ForcedEnemies path_id=2545173 e VictoryEvent path_id=2545625. Wait também inicia essa batalha, mas EnemyTurnFirst=1 (contra 0 no fracasso de Strike). Não simplificar os ramos para um efeito único ou inventar recompensa monetária.

MANTER significa nenhum depois proposto neste lote; não certifica perfeição de estilo, acesso no jogo ou ausência de questões fora de escopo.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 70,
  "json_index": 70,
  "chave": "resources.assets:2545626",
  "id": "bbce0c4c-c4df-4ebd-9b5f-fb745c872dc4",
  "titulo": "Magic Mirror",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 0,
  "texto_chars": 719,
  "veredito": "MANTER",
  "justificativa": "MANTER neste lote. Strike explica a tentativa de quebrar o espelho: Success limite=18 concede XP (razao=1.0) e candidato Mirror Shard, sem batalha; Failure limite=1 inicia batalha com ForcedEnemies path_id=2545173 e VictoryEvent path_id=2545625. Wait também inicia essa batalha, mas EnemyTurnFirst=1 (contra 0 no fracasso de Strike). Não simplificar os ramos para um efeito único ou inventar recompensa monetária.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "b963836a68d837b525891818dd9ded9e41c78b6a87346915b9b49103e7962566",
  "evidencias": [
    {
      "jsonpath": "$.eventos[70].texto",
      "valor": "In a room of opulence and decay, you find it: a large mirror of such beauty and craftsmanship it seems out of place amidst the cobweb-laden, moth-eaten grandeur of the cursed castle. Set in an ornate frame, carved with detail, the mirror is mesmerizing, drawing your gaze with an almost magnetic pull.\n\nYou squint at the reflection, caught in a moment of curious wonder. But as you look, the reflected image begins to distort.\n\n\nYour reflection darkens, and a cruel, sinister smile creeps across its face, a chilling contrast to your own stunned expression. It has taken on a life of its own.\n\nThe mirror shimmers, and a reflected hand reaches out, stretching beyond the glassy surface and into the reality of the room."
    },
    {
      "jsonpath": "$.eventos[70].texto_resultados_possiveis",
      "valor": "What will you do?"
    },
    {
      "jsonpath": "$.eventos[70].condicoes",
      "valor": {
        "disabled": 0,
        "EditorOnly": 0,
        "allowOnAllNodeTypes": 0,
        "allowedNodeTypes": [
          7
        ],
        "requiredStatusesToSpawn": [],
        "allowOnAllTerrainTypes": 0,
        "allowedTerrainTypes": [
          3
        ],
        "allowAtAllTimesOfDay": 1,
        "allowedTimeOfDay": 1,
        "allowAtAllLevels": 0,
        "minLevel": 3,
        "terrainTypesAllowedAtAnyTime": [
          3
        ],
        "KeepInDeckWhenUsed": 0,
        "isLesserEvent": 0,
        "LeadsToFortune": 1
      }
    },
    {
      "jsonpath": "$.eventos[70].modos",
      "valor": [
        {
          "valor": 0,
          "nome": "Campaign"
        },
        {
          "valor": 1,
          "nome": "Roguelike"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[70].historia",
      "valor": {
        "valor": 0,
        "nome": "NonStoryOnly"
      }
    },
    {
      "jsonpath": "$.eventos[70].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[70].origem.path_id",
      "valor": 2545626
    },
    {
      "jsonpath": "$.eventos[70].origem.caminhos_resource",
      "valor": [
        "events/magic mirror"
      ]
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].titulo",
      "valor": "Strike"
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].texto",
      "valor": "Attempt to smash the mirror before your reflection fully materializes into this world."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].texto",
      "valor": "Reacting swiftly you draw back your fist. Your muscles bunch as you drive your fist forward, aiming straight for the center of the mirror. \n\nA crash echoes through the room as your fist collides with the glass, shards flying in all directions, their glittering dance belying the violent nature of their creation. "
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 18
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": true,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [
          {
            "chave": "resources.assets:2545455",
            "nome": "Mirror Shard",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545455
            },
            "tipo": "EventStatus",
            "descricao": "Summon a Dark clone of yourself but it fights for you. \n\n<i><color=#808080>You hold a shard of your shattered reflection!</color></i>\n",
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
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].texto",
      "valor": "A moment of hesitation is all it takes, a heartbeat of doubt that echoes through the chamber. You lunge, your weapon arcing towards the mirror, but your reflection is quicker. The mirrored version meets your assault, the collision sparking with an eerie light.\n\nYou watch in abject horror as your own reflection comes to life, a twisted reflection a perverse caricature of yourself. "
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].resultado",
      "valor": {
        "valor": 1,
        "nome": "Failure"
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].limite_rolagem",
      "valor": 1
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.iniciar",
      "valor": true
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.DisableEnemyMods",
      "valor": 1
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.ForcedEnemies",
      "valor": [
        {
          "OverrideEnemyName": 0,
          "NameOverride": "",
          "CharacterInfo": {
            "m_FileID": 0,
            "m_PathID": 2545173
          },
          "ForcedEnemyMods": [],
          "IsSuperUnique": 0
        }
      ]
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 2545625
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].titulo",
      "valor": "Wait"
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].texto",
      "valor": "Watch as your reflection steps fully into this world."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].texto",
      "valor": "You watch in abject horror as your own reflection comes to life, a twisted reflection a perverse caricature of yourself. "
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.iniciar",
      "valor": true
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 1
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.ForcedEnemies",
      "valor": [
        {
          "OverrideEnemyName": 0,
          "NameOverride": "",
          "CharacterInfo": {
            "m_FileID": 0,
            "m_PathID": 2545173
          },
          "ForcedEnemyMods": [],
          "IsSuperUnique": 0
        }
      ]
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 2545625
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 1
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    }
  ],
  "mudancas": [],
  "nulls": [
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].efeitos[1].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].efeitos[1].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].efeitos[1].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].efeitos[1].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].efeitos[1].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].efeitos[1].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].recompensas[1].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].recompensas[1].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].recompensas[1].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].recompensas[1].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].recompensas[1].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].recompensas[1].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[0].recompensas[1].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[0].recompensas[1].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[1].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[70].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[70].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    }
  ],
  "referencias_catalogo": [
    {
      "chave": "resources.assets:2545173",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545173,
        "type": "MonoBehaviour",
        "script": "CharacterInfo",
        "name": "Magic Mirror"
      }
    },
    {
      "chave": "resources.assets:2545455",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545455,
        "type": "MonoBehaviour",
        "script": "EventStatus",
        "name": "Mirror Shard"
      }
    },
    {
      "chave": "resources.assets:2545625",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545625,
        "type": "MonoBehaviour",
        "script": "PartyEvent",
        "name": "Magic Mirror - Victory"
      }
    }
  ]
}
```

## Evento 71 — Mana Spring

Veredito: MANTER. MANTER neste lote. A narrativa apresenta a fonte de mana e Absorb corresponde ao candidato Overflowing Energy; a ação não inicia batalha nem encadeia evento. O status preserva expressões {3,15} em IntelligenceBase, {4,20} em ManaCostMod e {8,40} em ManaPowerMod, duração Quest. Não transformar intervalos/expressões em resultado fixo ou inferir recuperação de mana (percentMaxMana=0). Leave tem ação sem efeitos.

MANTER significa nenhum depois proposto neste lote; não certifica perfeição de estilo, acesso no jogo ou ausência de questões fora de escopo.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 71,
  "json_index": 71,
  "chave": "resources.assets:2545648",
  "id": "13531a98-c63d-4759-a46f-461586e41b3a",
  "titulo": "Mana Spring",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 0,
  "texto_chars": 550,
  "veredito": "MANTER",
  "justificativa": "MANTER neste lote. A narrativa apresenta a fonte de mana e Absorb corresponde ao candidato Overflowing Energy; a ação não inicia batalha nem encadeia evento. O status preserva expressões {3,15} em IntelligenceBase, {4,20} em ManaCostMod e {8,40} em ManaPowerMod, duração Quest. Não transformar intervalos/expressões em resultado fixo ou inferir recuperação de mana (percentMaxMana=0). Leave tem ação sem efeitos.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "0953f64335f46b70871589e37c4e4999be7f048175bdac54daff821fc2370967",
  "evidencias": [
    {
      "jsonpath": "$.eventos[71].texto",
      "valor": "The <blue><b><incr>Mana Spring</incr></b></blue> is an incandescent maelstrom of energy. It bursts from the ground with a radiance that outshines even the brightest stars. Its ethereal tendrils, composed of countless hues of blue, writhe and twist in the air like a celestial dance. This is a rarity, a natural font of pure, unadulterated magical power.\n\n\nIn an area deeply soaked in mystical energy, these springs come into existence. This one is particularly vibrant, a testament to the intense magic that must have suffused the land centuries ago."
    },
    {
      "jsonpath": "$.eventos[71].texto_resultados_possiveis",
      "valor": "What will you do?"
    },
    {
      "jsonpath": "$.eventos[71].condicoes",
      "valor": {
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
        "allowAtAllLevels": 1,
        "minLevel": 1,
        "terrainTypesAllowedAtAnyTime": [],
        "KeepInDeckWhenUsed": 0,
        "isLesserEvent": 0,
        "LeadsToFortune": 1
      }
    },
    {
      "jsonpath": "$.eventos[71].modos",
      "valor": [
        {
          "valor": 0,
          "nome": "Campaign"
        },
        {
          "valor": 1,
          "nome": "Roguelike"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[71].historia",
      "valor": {
        "valor": 0,
        "nome": "NonStoryOnly"
      }
    },
    {
      "jsonpath": "$.eventos[71].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[71].origem.path_id",
      "valor": 2545648
    },
    {
      "jsonpath": "$.eventos[71].origem.caminhos_resource",
      "valor": [
        "events/mana spring"
      ]
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].titulo",
      "valor": "Absorb"
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].texto",
      "valor": "Reach out and let the mana flow into you."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].texto",
      "valor": "Gently, almost hesitantly, [name] extends a hand towards the chaotic font of energy. [He] feels the warmth, the raw power radiating from the wellspring and then, as if lured by some unseen force, [he] plunges [his] hand into the spring.\n\n\nThe effect is immediate. Power surges into [him], flooding [his] veins, [his] mind, [his] very essence. It is like a wave, rushing and crashing against [his] mental barriers. The world spins as [he] grapples with the sudden influx of energy, fighting to keep [his] balance."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [
          {
            "chave": "resources.assets:2545459",
            "nome": "Overflowing Energy",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545459
            },
            "tipo": "EventStatus",
            "descricao": "Increases @Mana Costs@ by {4,20}%, power of all @Mana Abilites@ by {8,40}% and @Intelligence@ by {3,15}.\n\n<i><color=#808080>The energies of a Mana Spring swell within you!</i></color> ",
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
                "expressao": "{3,15}",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544478",
                  "nome": "ManaCostMod",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544478
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{4,20}",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544433",
                  "nome": "ManaPowerMod",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544433
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
        ],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].titulo",
      "valor": "Leave"
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].texto",
      "valor": "Nothing here interests you."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].texto",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    }
  ],
  "mudancas": [],
  "nulls": [
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[71].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[71].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[71].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[71].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[71].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[71].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[71].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[71].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[71].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[71].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[71].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[71].opcoes[1].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[71].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[71].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[71].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    }
  ],
  "referencias_catalogo": [
    {
      "chave": "resources.assets:2544433",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2544433,
        "type": "MonoBehaviour",
        "script": "CharacterAttribute",
        "name": "ManaPowerMod"
      }
    },
    {
      "chave": "resources.assets:2544451",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2544451,
        "type": "MonoBehaviour",
        "script": "CharacterAttribute",
        "name": "IntelligenceBase"
      }
    },
    {
      "chave": "resources.assets:2544478",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2544478,
        "type": "MonoBehaviour",
        "script": "CharacterAttribute",
        "name": "ManaCostMod"
      }
    },
    {
      "chave": "resources.assets:2545459",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545459,
        "type": "MonoBehaviour",
        "script": "EventStatus",
        "name": "Overflowing Energy"
      }
    }
  ]
}
```

## Evento 72 — Master of Rage

Veredito: MANTER. MANTER neste lote. A narrativa e Accept/Slay the wendigo já comunicam a missão de Barloc. Accept tem candidatos Rage Unleashed e Master of Rage, sortear=false, e iniciar batalha=false: não é combate instantâneo nem ensino garantido nesta ação. Preservar DamageMod expressão 50 e DamageReduction expressão -50 do primeiro status e a classificação Quest do segundo. Leave não aplica esses efeitos.

MANTER significa nenhum depois proposto neste lote; não certifica perfeição de estilo, acesso no jogo ou ausência de questões fora de escopo.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 72,
  "json_index": 72,
  "chave": "resources.assets:2545651",
  "id": "3c348484-97d8-44fe-9701-7897f376935e",
  "titulo": "Master of Rage",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 0,
  "texto_chars": 1211,
  "veredito": "MANTER",
  "justificativa": "MANTER neste lote. A narrativa e Accept/Slay the wendigo já comunicam a missão de Barloc. Accept tem candidatos Rage Unleashed e Master of Rage, sortear=false, e iniciar batalha=false: não é combate instantâneo nem ensino garantido nesta ação. Preservar DamageMod expressão 50 e DamageReduction expressão -50 do primeiro status e a classificação Quest do segundo. Leave não aplica esses efeitos.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "3fb9c0796dbbe1d2ae13fe159df792f2526d4609718b893e01026487da8c39b5",
  "evidencias": [
    {
      "jsonpath": "$.eventos[72].texto",
      "valor": "A hulking mass of muscle and iron stands before you, muscles rippling beneath a tapestry of scars. It is <red><b><incr>Barloc</incr></b></red>, the legendary barbarian. Towering over you, he brandishes two monstrous weapons, each as large as a grown man, with a nonchalance that suggests a life forged in battle and bloodshed.\n\n\n\"Listen well,\" his voice is a deep rumble, an avalanche given human form. \"Rage, it is a fire that burns within us. In the heart of every warrior, in every blow struck, every life taken. It is our greatest weapon, and our greatest enemy.\"\n\n\nHis eyes smolder like coals boring into your own. \"I can show you how to unlock its potential, to harness its power. But you must prove your worth.\"\n\n\nHe gestures to the north, towards the peak of the summit. \"A pack of Wendigo haunts this mountain, twisted creatures consumed by their own sins, fueled by an unholy rage. They were men once. But they have fallen, succumbed to the very fire I speak of.\"\n\n\n\"Defeat them,\" he says, his gaze unwavering. \"Show me that you can control your rage, not let it control you. Show me that you have the strength, the courage, to face these abominations. Only then, will I impart my teachings to you.\"\n\n"
    },
    {
      "jsonpath": "$.eventos[72].texto_resultados_possiveis",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[72].condicoes",
      "valor": {
        "disabled": 0,
        "EditorOnly": 0,
        "allowOnAllNodeTypes": 0,
        "allowedNodeTypes": [
          7
        ],
        "requiredStatusesToSpawn": [],
        "allowOnAllTerrainTypes": 0,
        "allowedTerrainTypes": [
          7
        ],
        "allowAtAllTimesOfDay": 1,
        "allowedTimeOfDay": 0,
        "allowAtAllLevels": 0,
        "minLevel": 3,
        "terrainTypesAllowedAtAnyTime": [],
        "KeepInDeckWhenUsed": 0,
        "isLesserEvent": 0,
        "LeadsToFortune": 0
      }
    },
    {
      "jsonpath": "$.eventos[72].modos",
      "valor": [
        {
          "valor": 0,
          "nome": "Campaign"
        },
        {
          "valor": 1,
          "nome": "Roguelike"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[72].historia",
      "valor": {
        "valor": 0,
        "nome": "NonStoryOnly"
      }
    },
    {
      "jsonpath": "$.eventos[72].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[72].origem.path_id",
      "valor": 2545651
    },
    {
      "jsonpath": "$.eventos[72].origem.caminhos_resource",
      "valor": [
        "events/master of rage"
      ]
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].titulo",
      "valor": "Accept"
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].texto",
      "valor": "Slay the wendigo."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].texto",
      "valor": "\"I trust you'll find your way. Harness your rage, do not let it harness you,\" Barloc warns, his words echoing in your mind as you venture further into the mountain, ready to face the wendigo."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [
          {
            "chave": "resources.assets:2545392",
            "nome": "Rage Unleashed",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545392
            },
            "tipo": "EventStatus",
            "descricao": "@Damage@ dealt and taken increased by @50@%.\n\n<i><color=#808080>\"You have given into your rage!\"</i></color>",
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
                  "chave": "resources.assets:2544373",
                  "nome": "DamageMod",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544373
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "50",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544414",
                  "nome": "DamageReduction",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544414
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "-50",
                "segunda_passagem": false
              }
            ]
          },
          {
            "chave": "resources.assets:2545514",
            "nome": "Master of Rage",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545514
            },
            "tipo": "EventStatus",
            "descricao": "Slay the nearby Wendigo. ",
            "duracao": {
              "valor": 1,
              "nome": "Quest"
            },
            "status_tipo": {
              "valor": 3,
              "nome": "Quest"
            },
            "modificadores": []
          }
        ],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].titulo",
      "valor": "Leave"
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].texto",
      "valor": "You cannot master your rage this day."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].texto",
      "valor": "Barloc nods his head in understanding. \n\n\"The path of rage is wrought with pain.\""
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    }
  ],
  "mudancas": [],
  "nulls": [
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[1].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[1].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[1].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[1].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[1].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[72].opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[72].opcoes[1].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "referencias_catalogo": [
    {
      "chave": "resources.assets:2544373",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2544373,
        "type": "MonoBehaviour",
        "script": "CharacterAttribute",
        "name": "DamageMod"
      }
    },
    {
      "chave": "resources.assets:2544414",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2544414,
        "type": "MonoBehaviour",
        "script": "CharacterAttribute",
        "name": "DamageReduction"
      }
    },
    {
      "chave": "resources.assets:2545392",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545392,
        "type": "MonoBehaviour",
        "script": "EventStatus",
        "name": "Rage Unleashed"
      }
    },
    {
      "chave": "resources.assets:2545514",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545514,
        "type": "MonoBehaviour",
        "script": "EventStatus",
        "name": "Master of Rage"
      }
    }
  ]
}
```

## Evento 73 — Mechanical Crusher

Veredito: MELHORAR. MELHORAR artigo e concordância/tempo verbal em textos existentes, sem alterar armadilha ou normalizar quebras de linha. Disarm usa Might; Success limite=10 tem XP dar=true/razao=1.0, alvo Party. Failure limite=1 tem efeito0 percentMaxHealth=-20 em Party e efeito1 candidato Bruised em default Self, pois override=false. Não afirmar que Bruised atinge todo o grupo só porque o dano usa Party. Nenhuma ação inicia combate.

Natureza: somente proposta editorial de wording; nenhum valor mecânico, alvo, condição, raridade, peso, disabled ou referência recebe alteração.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 73,
  "json_index": 73,
  "chave": "resources.assets:2545652",
  "id": "adc51dbf-4064-4194-a024-34126346d7c9",
  "titulo": "Mechanical Crusher",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 0,
  "texto_chars": 397,
  "veredito": "MELHORAR",
  "justificativa": "MELHORAR artigo e concordância/tempo verbal em textos existentes, sem alterar armadilha ou normalizar quebras de linha. Disarm usa Might; Success limite=10 tem XP dar=true/razao=1.0, alvo Party. Failure limite=1 tem efeito0 percentMaxHealth=-20 em Party e efeito1 candidato Bruised em default Self, pois override=false. Não afirmar que Bruised atinge todo o grupo só porque o dano usa Party. Nenhuma ação inicia combate.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "84380e7222e327b4543148795042f04923e6f402be8a65c92d1d369c756cdc80",
  "evidencias": [
    {
      "jsonpath": "$.eventos[73].texto",
      "valor": "A <red><b><incr>Mechanical Crusher</incr></b></red> stirs, a disquieting symphony of iron and ingenuity. You hesitate, eyes fixated on the massive plate being drawn upward by intricate network of gears and pulleys, the metallic heartbeat of this contraption. Its cyclical dance is dreadfully mesmerizing - a lift and a plunge, a mechanical predator that threatens to crush everything in its path.\r"
    },
    {
      "jsonpath": "$.eventos[73].texto_resultados_possiveis",
      "valor": "Who will attempt to disarm the trap?"
    },
    {
      "jsonpath": "$.eventos[73].condicoes",
      "valor": {
        "disabled": 0,
        "EditorOnly": 0,
        "allowOnAllNodeTypes": 0,
        "allowedNodeTypes": [
          7
        ],
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
      }
    },
    {
      "jsonpath": "$.eventos[73].modos",
      "valor": [
        {
          "valor": 0,
          "nome": "Campaign"
        },
        {
          "valor": 1,
          "nome": "Roguelike"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[73].historia",
      "valor": {
        "valor": 0,
        "nome": "NonStoryOnly"
      }
    },
    {
      "jsonpath": "$.eventos[73].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[73].origem.path_id",
      "valor": 2545652
    },
    {
      "jsonpath": "$.eventos[73].origem.caminhos_resource",
      "valor": [
        "events/mechanical crusher"
      ]
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].titulo",
      "valor": "Disarm"
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].texto",
      "valor": "Attempt to disarm the deadly trap."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].rolagem",
      "valor": {
        "bonus": [
          {
            "valor": 0,
            "nome": "Might"
          }
        ],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].texto",
      "valor": "From the nearby rubble surrounding the mechanism, [name] heaves a large rock, misshapen and rough-edged.\n\nWith all [his] might, the rock is hurled into the gears, a desperate bid against the machine's relentless rhythm.  Sparks fly as the jagged stone bites into the rotating cogs, grinding against the unforgiving steel.\n\nThe grating of metal against stone fills the air as the rock is ground down bit by bit, the gears grinding to a halt. With a final, resounding thud, the machine sputters and dies."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 10
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": true,
        "tipo_override": {
          "valor": 2,
          "nome": "Party"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": true,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].texto",
      "valor": "In the face of this mechanical menace, [name] seeks to disarm it, eyes set on a hefty stone off to the side. \n\n[he] moves swiftly bending down to grip a stone's rough surface. [his] muscles strain with effort, veins bulging on [his] forehead as [he] put every bit of [his] strength into hoisting the rock. But the weight is a reluctant partner in this dangerous dance, stubbornly resistant to [his] desperate endeavor.\r\n\r\nThe crusher pays no heed to [his] struggles, its rhythm unbroken. [name], trapped in a moment between defiance and desperation, misjudges the tempo. There is a heart-stopping moment when realization flashes across [his] face, a split-second before the crusher came down. [his] scream is cut short by the resounding crash of the metal plate."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].resultado",
      "valor": {
        "valor": 1,
        "nome": "Failure"
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].limite_rolagem",
      "valor": 1
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": -20.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[0].alvo",
      "valor": {
        "override": true,
        "tipo_override": {
          "valor": 2,
          "nome": "Party"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 0.5,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[1].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[1].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[1].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[1].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[1].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[1].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[1].recompensas.status",
      "valor": {
        "candidatos": [
          {
            "chave": "resources.assets:2545490",
            "nome": "Bruised",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545490
            },
            "tipo": "EventStatus",
            "descricao": "Reduces @Max Health@ by @10%@ per stack.",
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
                  "chave": "resources.assets:2544436",
                  "nome": "MaxHealth",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544436
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 1,
                  "nome": "Percentage"
                },
                "expressao": "-10",
                "segunda_passagem": true
              }
            ]
          }
        ],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[1].recompensas.skills",
      "valor": []
    }
  ],
  "mudancas": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[73].texto",
      "antes": "A <red><b><incr>Mechanical Crusher</incr></b></red> stirs, a disquieting symphony of iron and ingenuity. You hesitate, eyes fixated on the massive plate being drawn upward by intricate network of gears and pulleys, the metallic heartbeat of this contraption. Its cyclical dance is dreadfully mesmerizing - a lift and a plunge, a mechanical predator that threatens to crush everything in its path.\r",
      "depois": "A <red><b><incr>Mechanical Crusher</incr></b></red> stirs, a disquieting symphony of iron and ingenuity. You hesitate, eyes fixated on the massive plate being drawn upward by an intricate network of gears and pulleys, the metallic heartbeat of this contraption. Its cyclical dance is dreadfully mesmerizing - a lift and a plunge, a mechanical predator that threatens to crush everything in its path.\r",
      "justificativa": "Inserir artigo; preservar tags e o CR final do original.",
      "substituicoes": [
        [
          "by intricate network",
          "by an intricate network"
        ]
      ]
    },
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].texto",
      "antes": "In the face of this mechanical menace, [name] seeks to disarm it, eyes set on a hefty stone off to the side. \n\n[he] moves swiftly bending down to grip a stone's rough surface. [his] muscles strain with effort, veins bulging on [his] forehead as [he] put every bit of [his] strength into hoisting the rock. But the weight is a reluctant partner in this dangerous dance, stubbornly resistant to [his] desperate endeavor.\r\n\r\nThe crusher pays no heed to [his] struggles, its rhythm unbroken. [name], trapped in a moment between defiance and desperation, misjudges the tempo. There is a heart-stopping moment when realization flashes across [his] face, a split-second before the crusher came down. [his] scream is cut short by the resounding crash of the metal plate.",
      "depois": "In the face of this mechanical menace, [name] seeks to disarm it, eyes set on a hefty stone off to the side. \n\n[he] moves swiftly bending down to grip a stone's rough surface. [his] muscles strain with effort, veins bulging on [his] forehead as [he] puts every bit of [his] strength into hoisting the rock. But the weight is a reluctant partner in this dangerous dance, stubbornly resistant to [his] desperate endeavor.\r\n\r\nThe crusher pays no heed to [his] struggles, its rhythm unbroken. [name], trapped in a moment between defiance and desperation, misjudges the tempo. There is a heart-stopping moment when realization flashes across [his] face, a split-second before the crusher comes down. [his] scream is cut short by the resounding crash of the metal plate.",
      "justificativa": "Alinhar conjugação à narração presente, mantendo tokens e as quebras CRLF originais.",
      "substituicoes": [
        [
          "as [he] put every bit",
          "as [he] puts every bit"
        ],
        [
          "before the crusher came down",
          "before the crusher comes down"
        ]
      ]
    }
  ],
  "nulls": [
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[1].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[1].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[1].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[1].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[1].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[1].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[1].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[1].efeitos[1].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[1].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[1].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].efeitos[1].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].efeitos[1].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].recompensas[1].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].recompensas[1].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].recompensas[1].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].recompensas[1].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].recompensas[1].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].recompensas[1].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].recompensas[1].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].recompensas[1].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].recompensas[1].padrao[1].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].recompensas[1].padrao[1].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].recompensas[1].padrao[1].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].recompensas[1].padrao[1].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].recompensas[1].padrao[1].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].recompensas[1].padrao[1].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[73].opcoes[0].recompensas[1].padrao[1].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[73].opcoes[0].recompensas[1].padrao[1].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "referencias_catalogo": [
    {
      "chave": "resources.assets:2544436",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2544436,
        "type": "MonoBehaviour",
        "script": "CharacterAttribute",
        "name": "MaxHealth"
      }
    },
    {
      "chave": "resources.assets:2545490",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545490,
        "type": "MonoBehaviour",
        "script": "EventStatus",
        "name": "Bruised"
      }
    }
  ]
}
```

## Evento 74 — Mistress of Chaos

Veredito: MELHORAR. MELHORAR a apresentação de Decline porque ambas as opções têm iniciar=true; recusar a oferta não equivale a sair sem batalha. Variante Campaign/Roguelike, nó configurado [7], peso=0.5. Accept tem candidato Chaos Coin (Permanent/Fortune), itens dar=false e override EnemyModApplications Amount=8/AllEnemyTypes=1/DisableSuperUnique=1. Decline tem EnemyModApplications vazio. A sugestão não fixa modificadores, inimigos, duração do combate ou loot final.

Natureza: somente proposta editorial de wording; nenhum valor mecânico, alvo, condição, raridade, peso, disabled ou referência recebe alteração.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 74,
  "json_index": 74,
  "chave": "resources.assets:2545653",
  "id": "cdb949de-0865-4063-837c-c395f6c16878",
  "titulo": "Mistress of Chaos",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 0.5,
  "disabled": 0,
  "texto_chars": 487,
  "veredito": "MELHORAR",
  "justificativa": "MELHORAR a apresentação de Decline porque ambas as opções têm iniciar=true; recusar a oferta não equivale a sair sem batalha. Variante Campaign/Roguelike, nó configurado [7], peso=0.5. Accept tem candidato Chaos Coin (Permanent/Fortune), itens dar=false e override EnemyModApplications Amount=8/AllEnemyTypes=1/DisableSuperUnique=1. Decline tem EnemyModApplications vazio. A sugestão não fixa modificadores, inimigos, duração do combate ou loot final.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "eea04d3f538f4bde98fdf666cb79cd72871090fff1d34274930b335dadb35bbb",
  "evidencias": [
    {
      "jsonpath": "$.eventos[74].texto",
      "valor": "With a reality-bending laugh that echoes within your mind, the Mistress of Chaos unfurls her invitation. Her voice is a melody spun of whispers, a coaxing thread of discord woven into your thoughts. It tastes like temptation, like curiosity, like a gamble against fate.\n\n\n\"Such a dull little toy, you are,\" she coos, her words a twisted lullaby. \"Always playing it safe, always toeing the line. Where's the spark, the flame, the thrill? Let's make things more... entertaining, shall we?\""
    },
    {
      "jsonpath": "$.eventos[74].texto_resultados_possiveis",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[74].condicoes",
      "valor": {
        "disabled": 0,
        "EditorOnly": 0,
        "allowOnAllNodeTypes": 0,
        "allowedNodeTypes": [
          7
        ],
        "requiredStatusesToSpawn": [],
        "allowOnAllTerrainTypes": 1,
        "allowedTerrainTypes": [],
        "allowAtAllTimesOfDay": 1,
        "allowedTimeOfDay": 0,
        "allowAtAllLevels": 0,
        "minLevel": 3,
        "terrainTypesAllowedAtAnyTime": [],
        "KeepInDeckWhenUsed": 0,
        "isLesserEvent": 0,
        "LeadsToFortune": 0
      }
    },
    {
      "jsonpath": "$.eventos[74].modos",
      "valor": [
        {
          "valor": 0,
          "nome": "Campaign"
        },
        {
          "valor": 1,
          "nome": "Roguelike"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[74].historia",
      "valor": {
        "valor": 0,
        "nome": "NonStoryOnly"
      }
    },
    {
      "jsonpath": "$.eventos[74].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[74].origem.path_id",
      "valor": 2545653
    },
    {
      "jsonpath": "$.eventos[74].origem.caminhos_resource",
      "valor": [
        "events/mistress of chaos - coin of chaos"
      ]
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].titulo",
      "valor": "Accept"
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].texto",
      "valor": "You allow her magic to reshape the battlefield."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].texto",
      "valor": "The air around you seems to charge, the very atmosphere bristling as the Mistress of Chaos lets out a delighted laugh. \"Oh, excellent! This will be most entertaining!\" she purrs, her voice swirling around you, weaving an insidious promise into your mind."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": true
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 1
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": [
        {
          "AllEnemyTypes": 1,
          "EnemyTypes": [],
          "Amount": 8,
          "EnemyModPool": [
            {
              "m_FileID": 0,
              "m_PathID": 2545324
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545330
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545331
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545333
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545334
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545335
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545339
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545343
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545348
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545349
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545350
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545351
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545352
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545358
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545360
            }
          ]
        }
      ]
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": [
        {
          "m_FileID": 0,
          "m_PathID": 2545352
        },
        {
          "m_FileID": 0,
          "m_PathID": 2545360
        },
        {
          "m_FileID": 0,
          "m_PathID": 2545331
        },
        {
          "m_FileID": 0,
          "m_PathID": 2545343
        },
        {
          "m_FileID": 0,
          "m_PathID": 2545358
        },
        {
          "m_FileID": 0,
          "m_PathID": 2545335
        },
        {
          "m_FileID": 0,
          "m_PathID": 2545333
        },
        {
          "m_FileID": 0,
          "m_PathID": 2545351
        },
        {
          "m_FileID": 0,
          "m_PathID": 2545339
        },
        {
          "m_FileID": 0,
          "m_PathID": 2545349
        }
      ]
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
        "dar": false,
        "pool_tipo": {
          "valor": 1,
          "nome": "Global"
        },
        "quantidade_configurada": 2,
        "tabelas": [],
        "restricoes": {
          "limitItemTypes": 1,
          "possibleItemTypes": [
            0,
            1,
            2,
            3,
            4,
            5
          ],
          "limitItemRarities": 1,
          "possibleRarities": [
            2,
            3
          ]
        },
        "sorteio_final": null,
        "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [
          {
            "chave": "resources.assets:2545418",
            "nome": "Chaos Coin",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545418
            },
            "tipo": "EventStatus",
            "descricao": "<i><color=#808080>Will you flip the Coin of Chaos?</i></color>\n\n Grants the skill @Coin Flip@",
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
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].titulo",
      "valor": "Decline"
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].texto",
      "valor": "You don't need her mischief this time."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].texto",
      "valor": "The Mistress of Chaos seems to linger a moment longer, her disappointed laughter trickling away like dissipating smoke, leaving you the tangible relief of your choice."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.iniciar",
      "valor": true
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    }
  ],
  "mudancas": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[74].opcoes[1].texto",
      "antes": "You don't need her mischief this time.",
      "depois": "Decline her offer and face the battle without her changes.",
      "justificativa": "Explicitar o combate configurado ao recusar, sem prometer segurança ou recompensa.",
      "substituicoes": []
    },
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].texto",
      "antes": "The Mistress of Chaos seems to linger a moment longer, her disappointed laughter trickling away like dissipating smoke, leaving you the tangible relief of your choice.",
      "depois": "The Mistress of Chaos's laughter fades as you decline her offer. The battle still awaits.",
      "justificativa": "Evitar que a descrição de alívio seja interpretada como ausência de combate; sem alterar iniciar=true.",
      "substituicoes": []
    }
  ],
  "nulls": [
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[74].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[74].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[74].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[74].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[74].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[74].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[74].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[74].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[74].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[74].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[74].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[74].opcoes[1].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[74].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[74].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[74].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    }
  ],
  "referencias_catalogo": [
    {
      "chave": "resources.assets:2545324",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545324,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Berserking"
      }
    },
    {
      "chave": "resources.assets:2545330",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545330,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Cursed"
      }
    },
    {
      "chave": "resources.assets:2545331",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545331,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Destructive"
      }
    },
    {
      "chave": "resources.assets:2545333",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545333,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Elusive"
      }
    },
    {
      "chave": "resources.assets:2545334",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545334,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Explosive"
      }
    },
    {
      "chave": "resources.assets:2545335",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545335,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Freezing"
      }
    },
    {
      "chave": "resources.assets:2545339",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545339,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Giant"
      }
    },
    {
      "chave": "resources.assets:2545343",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545343,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Miniature"
      }
    },
    {
      "chave": "resources.assets:2545348",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545348,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Necromantic"
      }
    },
    {
      "chave": "resources.assets:2545349",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545349,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Rampaging"
      }
    },
    {
      "chave": "resources.assets:2545350",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545350,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Redemptive"
      }
    },
    {
      "chave": "resources.assets:2545351",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545351,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Regenerating"
      }
    },
    {
      "chave": "resources.assets:2545352",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545352,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Resilient"
      }
    },
    {
      "chave": "resources.assets:2545358",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545358,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Teleporting"
      }
    },
    {
      "chave": "resources.assets:2545360",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545360,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Undying"
      }
    },
    {
      "chave": "resources.assets:2545418",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545418,
        "type": "MonoBehaviour",
        "script": "EventStatus",
        "name": "Chaos Coin"
      }
    }
  ]
}
```

## Evento 75 — Mistress of Chaos

Veredito: MELHORAR. MELHORAR a apresentação de Decline pela mesma divergência: os dois ramos iniciam batalha. Esta é a variante Roguelike, nó [1], peso=0.5; não duplicata de #74. Accept não tem Chaos Coin: configura itens dar=true/quantidade=1/Global, restrições tipos [0,1,2,3,4,5], raridades [3,4], e EnemyModApplications Amount=2/AllEnemyTypes=1. Decline não tem essa aplicação de mods. Não transferir status, quantidade=2 inativa ou Amount=8 de outra variante.

Natureza: somente proposta editorial de wording; nenhum valor mecânico, alvo, condição, raridade, peso, disabled ou referência recebe alteração.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 75,
  "json_index": 75,
  "chave": "resources.assets:2545654",
  "id": "56dfd84e-2bc7-4b20-891d-f661f99ef68e",
  "titulo": "Mistress of Chaos",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 0.5,
  "disabled": 0,
  "texto_chars": 487,
  "veredito": "MELHORAR",
  "justificativa": "MELHORAR a apresentação de Decline pela mesma divergência: os dois ramos iniciam batalha. Esta é a variante Roguelike, nó [1], peso=0.5; não duplicata de #74. Accept não tem Chaos Coin: configura itens dar=true/quantidade=1/Global, restrições tipos [0,1,2,3,4,5], raridades [3,4], e EnemyModApplications Amount=2/AllEnemyTypes=1. Decline não tem essa aplicação de mods. Não transferir status, quantidade=2 inativa ou Amount=8 de outra variante.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "5ca2b8d742c2615519988f26ce875462d37fd6d611d72f402d72445e47144a6e",
  "evidencias": [
    {
      "jsonpath": "$.eventos[75].texto",
      "valor": "With a reality-bending laugh that echoes within your mind, the Mistress of Chaos unfurls her invitation. Her voice is a melody spun of whispers, a coaxing thread of discord woven into your thoughts. It tastes like temptation, like curiosity, like a gamble against fate.\n\n\n\"Such a dull little toy, you are,\" she coos, her words a twisted lullaby. \"Always playing it safe, always toeing the line. Where's the spark, the flame, the thrill? Let's make things more... entertaining, shall we?\""
    },
    {
      "jsonpath": "$.eventos[75].texto_resultados_possiveis",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[75].condicoes",
      "valor": {
        "disabled": 0,
        "EditorOnly": 0,
        "allowOnAllNodeTypes": 0,
        "allowedNodeTypes": [
          1
        ],
        "requiredStatusesToSpawn": [],
        "allowOnAllTerrainTypes": 1,
        "allowedTerrainTypes": [],
        "allowAtAllTimesOfDay": 1,
        "allowedTimeOfDay": 0,
        "allowAtAllLevels": 0,
        "minLevel": 3,
        "terrainTypesAllowedAtAnyTime": [],
        "KeepInDeckWhenUsed": 0,
        "isLesserEvent": 0,
        "LeadsToFortune": 0
      }
    },
    {
      "jsonpath": "$.eventos[75].modos",
      "valor": [
        {
          "valor": 1,
          "nome": "Roguelike"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[75].historia",
      "valor": {
        "valor": 0,
        "nome": "NonStoryOnly"
      }
    },
    {
      "jsonpath": "$.eventos[75].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[75].origem.path_id",
      "valor": 2545654
    },
    {
      "jsonpath": "$.eventos[75].origem.caminhos_resource",
      "valor": [
        "events/mistress of chaos - roguelike"
      ]
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].titulo",
      "valor": "Accept"
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].texto",
      "valor": "You allow her magic to reshape the battlefield."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].texto",
      "valor": "The air around you seems to charge, the very atmosphere bristling as the Mistress of Chaos lets out a delighted laugh. \"Oh, excellent! This will be most entertaining!\" she purrs, her voice swirling around you, weaving an insidious promise into your mind."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": true
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": [
        {
          "AllEnemyTypes": 1,
          "EnemyTypes": [],
          "Amount": 2,
          "EnemyModPool": [
            {
              "m_FileID": 0,
              "m_PathID": 2545324
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545330
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545331
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545333
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545334
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545335
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545339
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545343
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545348
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545349
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545350
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545351
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545352
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545358
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545360
            }
          ]
        }
      ]
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": [
        {
          "m_FileID": 0,
          "m_PathID": 2545343
        },
        {
          "m_FileID": 0,
          "m_PathID": 2545352
        }
      ]
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
        "dar": true,
        "pool_tipo": {
          "valor": 1,
          "nome": "Global"
        },
        "quantidade_configurada": 1,
        "tabelas": [],
        "restricoes": {
          "limitItemTypes": 1,
          "possibleItemTypes": [
            0,
            1,
            2,
            3,
            4,
            5
          ],
          "limitItemRarities": 1,
          "possibleRarities": [
            3,
            4
          ]
        },
        "sorteio_final": null,
        "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].titulo",
      "valor": "Decline"
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].texto",
      "valor": "You don't need her mischief this time."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].texto",
      "valor": "The Mistress of Chaos seems to linger a moment longer, her disappointed laughter trickling away like dissipating smoke, leaving you the tangible relief of your choice."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.iniciar",
      "valor": true
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    }
  ],
  "mudancas": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[75].opcoes[1].texto",
      "antes": "You don't need her mischief this time.",
      "depois": "Decline her offer and face the battle without her changes.",
      "justificativa": "Sinalizar a batalha também no ramo de recusa desta variante.",
      "substituicoes": []
    },
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].texto",
      "antes": "The Mistress of Chaos seems to linger a moment longer, her disappointed laughter trickling away like dissipating smoke, leaving you the tangible relief of your choice.",
      "depois": "The Mistress of Chaos's laughter fades as you decline her offer. The battle still awaits.",
      "justificativa": "Remover a interpretação de saída segura; conservar todos os overrides existentes.",
      "substituicoes": []
    }
  ],
  "nulls": [
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[75].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[75].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[75].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[75].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[75].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[75].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[75].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[75].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[75].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[75].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[75].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[75].opcoes[1].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[75].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[75].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[75].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    }
  ],
  "referencias_catalogo": [
    {
      "chave": "resources.assets:2545324",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545324,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Berserking"
      }
    },
    {
      "chave": "resources.assets:2545330",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545330,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Cursed"
      }
    },
    {
      "chave": "resources.assets:2545331",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545331,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Destructive"
      }
    },
    {
      "chave": "resources.assets:2545333",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545333,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Elusive"
      }
    },
    {
      "chave": "resources.assets:2545334",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545334,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Explosive"
      }
    },
    {
      "chave": "resources.assets:2545335",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545335,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Freezing"
      }
    },
    {
      "chave": "resources.assets:2545339",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545339,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Giant"
      }
    },
    {
      "chave": "resources.assets:2545343",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545343,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Miniature"
      }
    },
    {
      "chave": "resources.assets:2545348",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545348,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Necromantic"
      }
    },
    {
      "chave": "resources.assets:2545349",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545349,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Rampaging"
      }
    },
    {
      "chave": "resources.assets:2545350",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545350,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Redemptive"
      }
    },
    {
      "chave": "resources.assets:2545351",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545351,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Regenerating"
      }
    },
    {
      "chave": "resources.assets:2545352",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545352,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Resilient"
      }
    },
    {
      "chave": "resources.assets:2545358",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545358,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Teleporting"
      }
    },
    {
      "chave": "resources.assets:2545360",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545360,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Undying"
      }
    }
  ]
}
```

## Evento 76 — Mistress of Chaos

Veredito: MELHORAR. MELHORAR a apresentação de Decline; iniciar=true nos dois ramos. Esta variante é Campaign, nó [1], peso=0.25. Accept tem item dar=true/quantidade=1/Global e Amount=2 nos mods, mas a lista ovrEnemyModRefList difere de #75 e permanece literal. Não unificar variantes nem alterar peso ou copiar Chaos Coin de #74. Sorteios, efeito runtime e recompensa final permanecem NAO_EXERCITADO.

Natureza: somente proposta editorial de wording; nenhum valor mecânico, alvo, condição, raridade, peso, disabled ou referência recebe alteração.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 76,
  "json_index": 76,
  "chave": "resources.assets:2545655",
  "id": "c96278b1-90ed-46c8-8e50-9dc6d6d2cdf0",
  "titulo": "Mistress of Chaos",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 0.25,
  "disabled": 0,
  "texto_chars": 487,
  "veredito": "MELHORAR",
  "justificativa": "MELHORAR a apresentação de Decline; iniciar=true nos dois ramos. Esta variante é Campaign, nó [1], peso=0.25. Accept tem item dar=true/quantidade=1/Global e Amount=2 nos mods, mas a lista ovrEnemyModRefList difere de #75 e permanece literal. Não unificar variantes nem alterar peso ou copiar Chaos Coin de #74. Sorteios, efeito runtime e recompensa final permanecem NAO_EXERCITADO.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "7d9f7749d6dd30dceee5607fcff16b3013eedcaef02a88ac3bd1dc3a7a6ac2c9",
  "evidencias": [
    {
      "jsonpath": "$.eventos[76].texto",
      "valor": "With a reality-bending laugh that echoes within your mind, the Mistress of Chaos unfurls her invitation. Her voice is a melody spun of whispers, a coaxing thread of discord woven into your thoughts. It tastes like temptation, like curiosity, like a gamble against fate.\n\n\n\"Such a dull little toy, you are,\" she coos, her words a twisted lullaby. \"Always playing it safe, always toeing the line. Where's the spark, the flame, the thrill? Let's make things more... entertaining, shall we?\""
    },
    {
      "jsonpath": "$.eventos[76].texto_resultados_possiveis",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[76].condicoes",
      "valor": {
        "disabled": 0,
        "EditorOnly": 0,
        "allowOnAllNodeTypes": 0,
        "allowedNodeTypes": [
          1
        ],
        "requiredStatusesToSpawn": [],
        "allowOnAllTerrainTypes": 1,
        "allowedTerrainTypes": [],
        "allowAtAllTimesOfDay": 1,
        "allowedTimeOfDay": 0,
        "allowAtAllLevels": 0,
        "minLevel": 3,
        "terrainTypesAllowedAtAnyTime": [],
        "KeepInDeckWhenUsed": 0,
        "isLesserEvent": 0,
        "LeadsToFortune": 0
      }
    },
    {
      "jsonpath": "$.eventos[76].modos",
      "valor": [
        {
          "valor": 0,
          "nome": "Campaign"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[76].historia",
      "valor": {
        "valor": 0,
        "nome": "NonStoryOnly"
      }
    },
    {
      "jsonpath": "$.eventos[76].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[76].origem.path_id",
      "valor": 2545655
    },
    {
      "jsonpath": "$.eventos[76].origem.caminhos_resource",
      "valor": [
        "events/mistress of chaos"
      ]
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].titulo",
      "valor": "Accept"
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].texto",
      "valor": "You allow her magic to reshape the battlefield."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].texto",
      "valor": "The air around you seems to charge, the very atmosphere bristling as the Mistress of Chaos lets out a delighted laugh. \"Oh, excellent! This will be most entertaining!\" she purrs, her voice swirling around you, weaving an insidious promise into your mind."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": true
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": [
        {
          "AllEnemyTypes": 1,
          "EnemyTypes": [],
          "Amount": 2,
          "EnemyModPool": [
            {
              "m_FileID": 0,
              "m_PathID": 2545324
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545330
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545331
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545333
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545334
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545335
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545339
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545343
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545348
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545349
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545350
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545351
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545352
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545358
            },
            {
              "m_FileID": 0,
              "m_PathID": 2545360
            }
          ]
        }
      ]
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": [
        {
          "m_FileID": 0,
          "m_PathID": 2545348
        },
        {
          "m_FileID": 0,
          "m_PathID": 2545334
        }
      ]
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
        "dar": true,
        "pool_tipo": {
          "valor": 1,
          "nome": "Global"
        },
        "quantidade_configurada": 1,
        "tabelas": [],
        "restricoes": {
          "limitItemTypes": 1,
          "possibleItemTypes": [
            0,
            1,
            2,
            3,
            4,
            5
          ],
          "limitItemRarities": 1,
          "possibleRarities": [
            3,
            4
          ]
        },
        "sorteio_final": null,
        "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].titulo",
      "valor": "Decline"
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].texto",
      "valor": "You don't need her mischief this time."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].texto",
      "valor": "The Mistress of Chaos seems to linger a moment longer, her disappointed laughter trickling away like dissipating smoke, leaving you the tangible relief of your choice."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.iniciar",
      "valor": true
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    }
  ],
  "mudancas": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[76].opcoes[1].texto",
      "antes": "You don't need her mischief this time.",
      "depois": "Decline her offer and face the battle without her changes.",
      "justificativa": "Comunicar a batalha no ramo Decline da variante Campaign, sem inventar chance ou valor.",
      "substituicoes": []
    },
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].texto",
      "antes": "The Mistress of Chaos seems to linger a moment longer, her disappointed laughter trickling away like dissipating smoke, leaving you the tangible relief of your choice.",
      "depois": "The Mistress of Chaos's laughter fades as you decline her offer. The battle still awaits.",
      "justificativa": "Alinhar o resultado narrado à batalha configurada, não mudar sua configuração.",
      "substituicoes": []
    }
  ],
  "nulls": [
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[76].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[76].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[76].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[76].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[76].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[76].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[76].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[76].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[76].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[76].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[76].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[76].opcoes[1].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[76].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[76].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[76].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    }
  ],
  "referencias_catalogo": [
    {
      "chave": "resources.assets:2545324",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545324,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Berserking"
      }
    },
    {
      "chave": "resources.assets:2545330",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545330,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Cursed"
      }
    },
    {
      "chave": "resources.assets:2545331",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545331,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Destructive"
      }
    },
    {
      "chave": "resources.assets:2545333",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545333,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Elusive"
      }
    },
    {
      "chave": "resources.assets:2545334",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545334,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Explosive"
      }
    },
    {
      "chave": "resources.assets:2545335",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545335,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Freezing"
      }
    },
    {
      "chave": "resources.assets:2545339",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545339,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Giant"
      }
    },
    {
      "chave": "resources.assets:2545343",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545343,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Miniature"
      }
    },
    {
      "chave": "resources.assets:2545348",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545348,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Necromantic"
      }
    },
    {
      "chave": "resources.assets:2545349",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545349,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Rampaging"
      }
    },
    {
      "chave": "resources.assets:2545350",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545350,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Redemptive"
      }
    },
    {
      "chave": "resources.assets:2545351",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545351,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Regenerating"
      }
    },
    {
      "chave": "resources.assets:2545352",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545352,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Resilient"
      }
    },
    {
      "chave": "resources.assets:2545358",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545358,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Teleporting"
      }
    },
    {
      "chave": "resources.assets:2545360",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545360,
        "type": "MonoBehaviour",
        "script": "EnemyMod",
        "name": "Undying"
      }
    }
  ]
}
```

## Evento 77 — Off Balance

Veredito: MANTER. MANTER neste lote, inclusive disabled=1. Texto preenchido; Surprise tem Success limite=10 com EnemyStatusApplications Amount=1/AllEnemyTypes=1/ActionStatusPool path_id=2543229. Failure limite=0 inicia batalha e configura percentMaxHealth=-20/percentMaxMana=-20 em default Self, não Party; Fight inicia batalha sem esse efeito. Não inventar ativação na partida ou probabilidades a partir dos limites serializados.

MANTER significa nenhum depois proposto neste lote; não certifica perfeição de estilo, acesso no jogo ou ausência de questões fora de escopo.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 77,
  "json_index": 77,
  "chave": "resources.assets:2545656",
  "id": "294579ef-2a2e-47d3-a729-78bc847b1422",
  "titulo": "Off Balance",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 1,
  "texto_chars": 63,
  "veredito": "MANTER",
  "justificativa": "MANTER neste lote, inclusive disabled=1. Texto preenchido; Surprise tem Success limite=10 com EnemyStatusApplications Amount=1/AllEnemyTypes=1/ActionStatusPool path_id=2543229. Failure limite=0 inicia batalha e configura percentMaxHealth=-20/percentMaxMana=-20 em default Self, não Party; Fight inicia batalha sem esse efeito. Não inventar ativação na partida ou probabilidades a partir dos limites serializados.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "f5eb842cb1a6244d31d6a1602b2884ae4ce3680d087d89ea4c1c06e8eb9d6558",
  "evidencias": [
    {
      "jsonpath": "$.eventos[77].texto",
      "valor": "You see your enemy off guard, but the moment will pass quickly."
    },
    {
      "jsonpath": "$.eventos[77].texto_resultados_possiveis",
      "valor": "What will you do?"
    },
    {
      "jsonpath": "$.eventos[77].condicoes",
      "valor": {
        "disabled": 1,
        "EditorOnly": 0,
        "allowOnAllNodeTypes": 0,
        "allowedNodeTypes": [
          0
        ],
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
      }
    },
    {
      "jsonpath": "$.eventos[77].modos",
      "valor": [
        {
          "valor": 0,
          "nome": "Campaign"
        },
        {
          "valor": 1,
          "nome": "Roguelike"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[77].historia",
      "valor": {
        "valor": 0,
        "nome": "NonStoryOnly"
      }
    },
    {
      "jsonpath": "$.eventos[77].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[77].origem.path_id",
      "valor": 2545656
    },
    {
      "jsonpath": "$.eventos[77].origem.caminhos_resource",
      "valor": [
        "events/off balance"
      ]
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].titulo",
      "valor": "Surprise"
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].texto",
      "valor": "Catch them off guard with a sudden attack."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].texto",
      "valor": "Your enemies freeze in terror until they can collect their wits."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 10
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": true
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": [
        {
          "AllEnemyTypes": 1,
          "EnemyTypes": [],
          "Amount": 1,
          "ActionStatusPool": [
            {
              "m_FileID": 0,
              "m_PathID": 2543229
            }
          ]
        }
      ]
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": [
        {
          "m_FileID": 0,
          "m_PathID": 2543229
        }
      ]
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
        "dar": false,
        "pool_tipo": {
          "valor": 1,
          "nome": "Global"
        },
        "quantidade_configurada": 3,
        "tabelas": [],
        "restricoes": {
          "limitItemTypes": 1,
          "possibleItemTypes": [
            0
          ],
          "limitItemRarities": 1,
          "possibleRarities": [
            1,
            2,
            3
          ]
        },
        "sorteio_final": null,
        "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].texto",
      "valor": "You rush in but tangle together like a bunch of bubbling buffoons. Your careless attacks hit friend instead of foe."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].resultado",
      "valor": {
        "valor": 1,
        "nome": "Failure"
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.iniciar",
      "valor": true
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": -20.0,
        "percentMaxMana": -20.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].titulo",
      "valor": "Fight"
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].texto",
      "valor": "Straightforward battle is the best way to handle any situation."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].texto",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.iniciar",
      "valor": true
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    }
  ],
  "mudancas": [],
  "nulls": [
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].efeitos[1].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].efeitos[1].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].efeitos[1].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].efeitos[1].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].efeitos[1].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].efeitos[1].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].recompensas[1].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].recompensas[1].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].recompensas[1].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].recompensas[1].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].recompensas[1].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].recompensas[1].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[0].recompensas[1].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[0].recompensas[1].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[1].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[77].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[77].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    }
  ],
  "referencias_catalogo": [
    {
      "chave": "resources.assets:2543229",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2543229,
        "type": "MonoBehaviour",
        "script": "ActionStatusInfo",
        "name": "GL-Stunned 2T"
      }
    }
  ]
}
```

## Evento 78 — Ogre Debt Collector

Veredito: MELHORAR. MELHORAR preenchendo o texto da ação Refuse realmente vazio, não substituir a narrativa de Krothug. Pay tem ouro retirar=true/razao=3.0 e iniciar=false, apesar da referência de template Ogre Debt Collector Battle; referência não prova combate. Refuse tem referência nula, iniciar=true e três ForcedEnemies, primeiro com NameOverride=Ogre Debt Collector/OverrideEnemyName=1/IsSuperUnique=1/CharacterInfo path_id=2545107; os outros dois apontam 2545108. Preservar VictoryEvent path_id=2545658. Não prometer ouro fixo nem eliminar o combate.

Natureza: somente proposta editorial de wording; nenhum valor mecânico, alvo, condição, raridade, peso, disabled ou referência recebe alteração.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 78,
  "json_index": 78,
  "chave": "resources.assets:2545659",
  "id": "2fc9c449-54a4-4b19-b457-3481e6e0aebb",
  "titulo": "Ogre Debt Collector",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 0,
  "texto_chars": 376,
  "veredito": "MELHORAR",
  "justificativa": "MELHORAR preenchendo o texto da ação Refuse realmente vazio, não substituir a narrativa de Krothug. Pay tem ouro retirar=true/razao=3.0 e iniciar=false, apesar da referência de template Ogre Debt Collector Battle; referência não prova combate. Refuse tem referência nula, iniciar=true e três ForcedEnemies, primeiro com NameOverride=Ogre Debt Collector/OverrideEnemyName=1/IsSuperUnique=1/CharacterInfo path_id=2545107; os outros dois apontam 2545108. Preservar VictoryEvent path_id=2545658. Não prometer ouro fixo nem eliminar o combate.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "77542aacff174ea3c12a87aaf02bcd863d7fde3961b0b41af3a320f3563e8923",
  "evidencias": [
    {
      "jsonpath": "$.eventos[78].texto",
      "valor": "A thunderous growl sets the earth trembling beneath your feet. A beast of stone and sinew lumbers towards you - an ogre named <orange><b><incr>Krothug</incr></b></orange>. His yellow eyes flicker with an avaricious gleam as he spots the golden pouch at your side.\n\n\n\"<shake>Gold!</shake>\" Krothug roared, his voice as rough as gravel. \"<shake>You owe Krothug shiny!</shake>\"\n\n"
    },
    {
      "jsonpath": "$.eventos[78].texto_resultados_possiveis",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[78].condicoes",
      "valor": {
        "disabled": 0,
        "EditorOnly": 0,
        "allowOnAllNodeTypes": 0,
        "allowedNodeTypes": [
          7
        ],
        "requiredStatusesToSpawn": [],
        "allowOnAllTerrainTypes": 1,
        "allowedTerrainTypes": [],
        "allowAtAllTimesOfDay": 1,
        "allowedTimeOfDay": 1,
        "allowAtAllLevels": 0,
        "minLevel": 3,
        "terrainTypesAllowedAtAnyTime": [
          4,
          3
        ],
        "KeepInDeckWhenUsed": 0,
        "isLesserEvent": 0,
        "LeadsToFortune": 0
      }
    },
    {
      "jsonpath": "$.eventos[78].modos",
      "valor": [
        {
          "valor": 0,
          "nome": "Campaign"
        },
        {
          "valor": 1,
          "nome": "Roguelike"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[78].historia",
      "valor": {
        "valor": 0,
        "nome": "NonStoryOnly"
      }
    },
    {
      "jsonpath": "$.eventos[78].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[78].origem.path_id",
      "valor": 2545659
    },
    {
      "jsonpath": "$.eventos[78].origem.caminhos_resource",
      "valor": [
        "events/ogre debt collector"
      ]
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].titulo",
      "valor": "Pay"
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].texto",
      "valor": "Give <orange><b>Krothug</b></orange> your gold."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].texto",
      "valor": "<orange><b><incr>Krothug</incr></b></orange> tears the gold pouch from [name]'s belt with a triumphant roar. \"<shake>Gold mine now!</shake>\" Krothug thundered, raising the pouch high in the air.\n\nA harsh reminder that justice sometimes requires more than words - it requires strength, resilience, and the will to stand against such monstrous injustice.\r\n\r\r\n"
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": "resources.assets:2544649",
        "nome": "Ogre Debt Collector Battle",
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2544649
        },
        "tipo": "BattleInfo"
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": true,
        "razao": 3.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 3.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].titulo",
      "valor": "Refuse"
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].texto",
      "valor": "You will not part with your gold."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].texto",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.iniciar",
      "valor": true
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.ForcedEnemies",
      "valor": [
        {
          "OverrideEnemyName": 1,
          "NameOverride": "Ogre Debt Collector",
          "CharacterInfo": {
            "m_FileID": 0,
            "m_PathID": 2545107
          },
          "ForcedEnemyMods": [],
          "IsSuperUnique": 1
        },
        {
          "OverrideEnemyName": 0,
          "NameOverride": "",
          "CharacterInfo": {
            "m_FileID": 0,
            "m_PathID": 2545108
          },
          "ForcedEnemyMods": [],
          "IsSuperUnique": 0
        },
        {
          "OverrideEnemyName": 0,
          "NameOverride": "",
          "CharacterInfo": {
            "m_FileID": 0,
            "m_PathID": 2545108
          },
          "ForcedEnemyMods": [],
          "IsSuperUnique": 0
        }
      ]
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 2545658
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    }
  ],
  "mudancas": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].texto",
      "antes": "",
      "depois": "You refuse Krothug's demand and prepare to fight.",
      "justificativa": "Contextualizar uma ação que inicia batalha sem inventar a vitória, dano ou loot.",
      "substituicoes": []
    }
  ],
  "nulls": [
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[0].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[1].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[1].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[1].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[1].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[1].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[78].opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[78].opcoes[1].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "referencias_catalogo": [
    {
      "chave": "resources.assets:2544649",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2544649,
        "type": "MonoBehaviour",
        "script": "BattleInfo",
        "name": "Ogre Debt Collector Battle"
      }
    },
    {
      "chave": "resources.assets:2545107",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545107,
        "type": "MonoBehaviour",
        "script": "CharacterInfo",
        "name": "Krothug"
      }
    },
    {
      "chave": "resources.assets:2545108",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545108,
        "type": "MonoBehaviour",
        "script": "CharacterInfo",
        "name": "Ogre Basher"
      }
    },
    {
      "chave": "resources.assets:2545658",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545658,
        "type": "MonoBehaviour",
        "script": "PartyEvent",
        "name": "Ogre Debt Collector Battle Victory"
      }
    }
  ]
}
```

## Evento 79 — Ornate Coffin

Veredito: MELHORAR. MELHORAR verbo intransitivo e separar a primeira frase para remover a emenda por vírgula. Open tem bônus Dexterity, mas a única ação é Success limite=0, iniciar=false e evento_encadeado Taste for Blood 1/resources.assets:2545716. Ouro razao=15.0 com dar=false não é recompensa de quinze moedas; não inventar rolagem de fracasso nem combate direto. Leave não encadeia evento.

Natureza: somente proposta editorial de wording; nenhum valor mecânico, alvo, condição, raridade, peso, disabled ou referência recebe alteração.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 79,
  "json_index": 79,
  "chave": "resources.assets:2545660",
  "id": "ff91cd18-05cb-45a7-abe1-4216f883bfbe",
  "titulo": "Ornate Coffin",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 0,
  "texto_chars": 260,
  "veredito": "MELHORAR",
  "justificativa": "MELHORAR verbo intransitivo e separar a primeira frase para remover a emenda por vírgula. Open tem bônus Dexterity, mas a única ação é Success limite=0, iniciar=false e evento_encadeado Taste for Blood 1/resources.assets:2545716. Ouro razao=15.0 com dar=false não é recompensa de quinze moedas; não inventar rolagem de fracasso nem combate direto. Leave não encadeia evento.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "53623d9f5b436e8033a63c6e281e1f054da5b862e9cbc63433f7c233d281f823",
  "evidencias": [
    {
      "jsonpath": "$.eventos[79].texto",
      "valor": "In the damp, cold stillness of the castle, a resplendent coffin lays in wait, its dark wood and intricate carvings hint at the nobility of its occupant. Its ornate design is like a siren's song, tempting you into disturbing the slumber of its eternal resident."
    },
    {
      "jsonpath": "$.eventos[79].texto_resultados_possiveis",
      "valor": "What will you do?"
    },
    {
      "jsonpath": "$.eventos[79].condicoes",
      "valor": {
        "disabled": 0,
        "EditorOnly": 0,
        "allowOnAllNodeTypes": 0,
        "allowedNodeTypes": [
          7
        ],
        "requiredStatusesToSpawn": [],
        "allowOnAllTerrainTypes": 0,
        "allowedTerrainTypes": [
          3
        ],
        "allowAtAllTimesOfDay": 1,
        "allowedTimeOfDay": 0,
        "allowAtAllLevels": 0,
        "minLevel": 3,
        "terrainTypesAllowedAtAnyTime": [],
        "KeepInDeckWhenUsed": 0,
        "isLesserEvent": 0,
        "LeadsToFortune": 0
      }
    },
    {
      "jsonpath": "$.eventos[79].modos",
      "valor": [
        {
          "valor": 0,
          "nome": "Campaign"
        },
        {
          "valor": 1,
          "nome": "Roguelike"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[79].historia",
      "valor": {
        "valor": 0,
        "nome": "NonStoryOnly"
      }
    },
    {
      "jsonpath": "$.eventos[79].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[79].origem.path_id",
      "valor": 2545660
    },
    {
      "jsonpath": "$.eventos[79].origem.caminhos_resource",
      "valor": [
        "events/ornate coffin"
      ]
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].titulo",
      "valor": "Open"
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].texto",
      "valor": "Open the coffin and see who or what is inside."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].rolagem",
      "valor": {
        "bonus": [
          {
            "valor": 1,
            "nome": "Dexterity"
          }
        ],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].texto",
      "valor": "With an eerie sense of anticipation, you carefully lift the lid. A gasp escapes your lips as you lay your eyes upon its inhabitant. She rises from her coffin, and the light casts eerie shadows on her pale skin."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": "resources.assets:2545716",
        "nome": "Taste for Blood 1",
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545716
        },
        "tipo": "PartyEvent"
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 2,
          "nome": "Party"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 15.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
        "dar": false,
        "pool_tipo": {
          "valor": 2,
          "nome": "Unassigned"
        },
        "quantidade_configurada": 1,
        "tabelas": [
          {
            "mustGetOne": 0,
            "itemLootChances": []
          }
        ],
        "restricoes": {
          "limitItemTypes": 0,
          "possibleItemTypes": [],
          "limitItemRarities": 0,
          "possibleRarities": [
            3,
            4
          ]
        },
        "sorteio_final": null,
        "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].titulo",
      "valor": "Leave"
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].texto",
      "valor": "You will not disturb the dead."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].texto",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    }
  ],
  "mudancas": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[79].texto",
      "antes": "In the damp, cold stillness of the castle, a resplendent coffin lays in wait, its dark wood and intricate carvings hint at the nobility of its occupant. Its ornate design is like a siren's song, tempting you into disturbing the slumber of its eternal resident.",
      "depois": "In the damp, cold stillness of the castle, a resplendent coffin lies in wait. Its dark wood and intricate carvings hint at the nobility of its occupant. Its ornate design is like a siren's song, tempting you into disturbing the slumber of its eternal resident.",
      "justificativa": "Correção gramatical localizada, preservando o convite narrativo e a identidade do caixão.",
      "substituicoes": [
        [
          "a resplendent coffin lays in wait, its dark wood",
          "a resplendent coffin lies in wait. Its dark wood"
        ]
      ]
    }
  ],
  "nulls": [
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[1].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[1].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[1].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[1].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[1].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[79].opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[79].opcoes[1].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "referencias_catalogo": [
    {
      "chave": "resources.assets:2545716",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545716,
        "type": "MonoBehaviour",
        "script": "PartyEvent",
        "name": "Taste for Blood 1"
      }
    }
  ]
}
```

## Evento 80 — Party like a Pirate

Veredito: MELHORAR. MELHORAR somente verbo ausente na narrativa e tempo verbal na ação Sip. Sip tem percentMaxHealth=-10 em default Self e candidato Weakened (MightBase Percentage expressão -20, duração Quest), sem batalha; encadeia Party like a Pirate 1/resources.assets:2545661. Leave não aplica status nem encadeia. Não transformar o convite a beber em ganho fictício ou omitir o custo configurado do inventário.

Natureza: somente proposta editorial de wording; nenhum valor mecânico, alvo, condição, raridade, peso, disabled ou referência recebe alteração.

REGISTRO AUDITÁVEL — antes/depois são strings JSON completas; \n e \r representam literalmente LF e CR do valor, não caracteres inseridos por tradução.

```json
{
  "ordinal": 80,
  "json_index": 80,
  "chave": "resources.assets:2545664",
  "id": "385d6042-6c20-4ee0-9791-a7a4ec12ae03",
  "titulo": "Party like a Pirate",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 0,
  "texto_chars": 579,
  "veredito": "MELHORAR",
  "justificativa": "MELHORAR somente verbo ausente na narrativa e tempo verbal na ação Sip. Sip tem percentMaxHealth=-10 em default Self e candidato Weakened (MightBase Percentage expressão -20, duração Quest), sem batalha; encadeia Party like a Pirate 1/resources.assets:2545661. Leave não aplica status nem encadeia. Não transformar o convite a beber em ganho fictício ou omitir o custo configurado do inventário.",
  "runtime": "NAO_EXERCITADO",
  "aprovacao_dono": "PENDENTE",
  "origem_sha256_objeto": "da799b13cd888521b68945225acb0caa398be6ae8ecd9f02f308b80ef484afdf",
  "evidencias": [
    {
      "jsonpath": "$.eventos[80].texto",
      "valor": " It is a carnival of morbid mirth, with skeletal figures frozen in place, their joyous revelry cut short by death. It is an uncanny scene, death masquerading as life, and you feel an unspoken kinship with these jovial souls.\n\n\nA mug, clenched in the bony hand of a particularly well-dressed skeleton, calls to you. The sloshing liquid inside glowing amber under the light, and a tempting aroma wafts towards you. You can almost hear the teasing invitations of the dead mariners. \"Have a sip, lad,\" a raspy, otherworldly voice seems to whisper, \"Join us in our eternal merriment.\""
    },
    {
      "jsonpath": "$.eventos[80].texto_resultados_possiveis",
      "valor": ""
    },
    {
      "jsonpath": "$.eventos[80].condicoes",
      "valor": {
        "disabled": 0,
        "EditorOnly": 0,
        "allowOnAllNodeTypes": 0,
        "allowedNodeTypes": [
          7
        ],
        "requiredStatusesToSpawn": [],
        "allowOnAllTerrainTypes": 0,
        "allowedTerrainTypes": [
          0
        ],
        "allowAtAllTimesOfDay": 1,
        "allowedTimeOfDay": 0,
        "allowAtAllLevels": 1,
        "minLevel": 1,
        "terrainTypesAllowedAtAnyTime": [],
        "KeepInDeckWhenUsed": 0,
        "isLesserEvent": 0,
        "LeadsToFortune": 0
      }
    },
    {
      "jsonpath": "$.eventos[80].modos",
      "valor": [
        {
          "valor": 0,
          "nome": "Campaign"
        },
        {
          "valor": 1,
          "nome": "Roguelike"
        }
      ]
    },
    {
      "jsonpath": "$.eventos[80].historia",
      "valor": {
        "valor": 0,
        "nome": "NonStoryOnly"
      }
    },
    {
      "jsonpath": "$.eventos[80].full_release",
      "valor": {
        "valor": 0,
        "nome": "None"
      }
    },
    {
      "jsonpath": "$.eventos[80].origem.path_id",
      "valor": 2545664
    },
    {
      "jsonpath": "$.eventos[80].origem.caminhos_resource",
      "valor": [
        "events/party like a pirate"
      ]
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].titulo",
      "valor": "Sip"
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].texto",
      "valor": "Sample what these pirates died for."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].texto",
      "valor": "Your first swig sends your senses spinning; the rum is a flame that dances down your throat, setting your insides alight. It is old and potent, packed with a wildness that spoke of seafaring adventures and high-sea escapades. "
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].evento_encadeado",
      "valor": {
        "chave": "resources.assets:2545661",
        "nome": "Party like a Pirate 1",
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545661
        },
        "tipo": "PartyEvent"
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": -10.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [
          {
            "chave": "resources.assets:2545504",
            "nome": "Weakened",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545504
            },
            "tipo": "EventStatus",
            "descricao": "Reduces @Might@ by 20% per stack.",
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
                  "chave": "resources.assets:2544453",
                  "nome": "MightBase",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544453
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
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].titulo",
      "valor": "Leave"
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].texto",
      "valor": "Don't give in to peer pressure."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].condicoes",
      "valor": {
        "status_requeridos": [],
        "ocultar_sem_requisitos": false,
        "ocultar_se_status": []
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].rolagem",
      "valor": {
        "bonus": [],
        "misteriosa": false,
        "texto_misterioso": ""
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].texto",
      "valor": "You shake your head, clearing the phantom sounds from your mind.\n\n\"No,\" you say, \"this isn't my party.\""
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].resultado",
      "valor": {
        "valor": 0,
        "nome": "Success"
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].limite_rolagem",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].texto_efeitos_manual",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].evento_encadeado",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.iniciar",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.manual",
      "valor": false
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.referencia",
      "valor": {
        "chave": null,
        "nome": null,
        "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.ForceRandomSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.DisableSuperUnique",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.DisableEnemyMods",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.UseRewardModifiers",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.GauranteedLoot",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.ForcedEnemies",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.EnemyModApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.EnemyStatusApplications",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.FillOutBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.OverrideBattlePoints",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.BattlePointValue",
      "valor": 8
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.OverrideEnemyGroupPool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.EnemyGroupPool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.OverrideEnemyTypePool",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.EnemyTypePool",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.VictoryEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.FailureEvent",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.EnemyTurnFirst",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.ForceMap",
      "valor": 0
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.MapToForce",
      "valor": {
        "m_FileID": 0,
        "m_PathID": 0
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.ovrEnemyStatusRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.override.ovrEnemyModRefList",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].efeitos[0].vida_mana",
      "valor": {
        "percentMaxHealth": 0.0,
        "percentMaxMana": 0.0,
        "percentCurHealth": 0.0,
        "percentCurMana": 0.0
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].efeitos[0].alvo",
      "valor": {
        "override": false,
        "tipo_override": {
          "valor": 0,
          "nome": "Self"
        },
        "tipo_default_serializado": {
          "valor": 0,
          "nome": "Self"
        }
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].efeitos[0].remocoes_status",
      "valor": []
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro",
      "valor": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia",
      "valor": {
        "dar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].efeitos[0].recompensas.itens",
      "valor": {
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
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].efeitos[0].recompensas.status",
      "valor": {
        "candidatos": [],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      }
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].efeitos[0].recompensas.skills",
      "valor": []
    }
  ],
  "mudancas": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[80].texto",
      "antes": " It is a carnival of morbid mirth, with skeletal figures frozen in place, their joyous revelry cut short by death. It is an uncanny scene, death masquerading as life, and you feel an unspoken kinship with these jovial souls.\n\n\nA mug, clenched in the bony hand of a particularly well-dressed skeleton, calls to you. The sloshing liquid inside glowing amber under the light, and a tempting aroma wafts towards you. You can almost hear the teasing invitations of the dead mariners. \"Have a sip, lad,\" a raspy, otherworldly voice seems to whisper, \"Join us in our eternal merriment.\"",
      "depois": " It is a carnival of morbid mirth, with skeletal figures frozen in place, their joyous revelry cut short by death. It is an uncanny scene, death masquerading as life, and you feel an unspoken kinship with these jovial souls.\n\n\nA mug, clenched in the bony hand of a particularly well-dressed skeleton, calls to you. The sloshing liquid inside is glowing amber under the light, and a tempting aroma wafts towards you. You can almost hear the teasing invitations of the dead mariners. \"Have a sip, lad,\" a raspy, otherworldly voice seems to whisper, \"Join us in our eternal merriment.\"",
      "justificativa": "Restaurar verbo ausente sem modificar local, personagens, diálogos ou quebras de linha.",
      "substituicoes": [
        [
          "The sloshing liquid inside glowing amber",
          "The sloshing liquid inside is glowing amber"
        ]
      ]
    },
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO ORIGINAL — wording; não implementada",
      "lingua": "en",
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].texto",
      "antes": "Your first swig sends your senses spinning; the rum is a flame that dances down your throat, setting your insides alight. It is old and potent, packed with a wildness that spoke of seafaring adventures and high-sea escapades. ",
      "depois": "Your first swig sends your senses spinning; the rum is a flame that dances down your throat, setting your insides alight. It is old and potent, packed with a wildness that speaks of seafaring adventures and high-sea escapades. ",
      "justificativa": "Alinhar a frase ao tempo presente da ação; conservar o espaço final do original.",
      "substituicoes": [
        [
          "a wildness that spoke of",
          "a wildness that speaks of"
        ]
      ]
    }
  ],
  "nulls": [
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[0].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[0].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[0].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[0].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[0].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[0].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[0].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[1].efeitos[0].efeitos[0].recompensas.status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.referencia.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[1].efeitos[0].batalha.motivo",
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[1].efeitos[0].evento_encadeado.motivo",
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].recompensas[0].padrao[0].ouro.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[1].recompensas[0].padrao[0].ouro.motivo",
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].recompensas[0].padrao[0].experiencia.quantidade_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[1].recompensas[0].padrao[0].experiencia.motivo",
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].recompensas[0].padrao[0].itens.sorteio_final",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[1].recompensas[0].padrao[0].itens.motivo",
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "jsonpath": "$.eventos[80].opcoes[1].recompensas[0].padrao[0].status.resultado_sorteado",
      "valor": null,
      "motivo_jsonpath": "$.eventos[80].opcoes[1].recompensas[0].padrao[0].status.motivo",
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "referencias_catalogo": [
    {
      "chave": "resources.assets:2544453",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2544453,
        "type": "MonoBehaviour",
        "script": "CharacterAttribute",
        "name": "MightBase"
      }
    },
    {
      "chave": "resources.assets:2545504",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545504,
        "type": "MonoBehaviour",
        "script": "EventStatus",
        "name": "Weakened"
      }
    },
    {
      "chave": "resources.assets:2545661",
      "resumo_literal": {
        "file": "resources.assets",
        "path_id": 2545661,
        "type": "MonoBehaviour",
        "script": "PartyEvent",
        "name": "Party like a Pirate 1"
      }
    }
  ]
}
```

## Auditoria e pendências

A auditoria offline acompanha este documento no pacote EV-R2-NORMAL-b04-auditoria.zip. O script relê as quatro fontes e a parte01, verifica SHA256, 160 títulos/seções e suas chaves, a faixa 61–80, identidades completas, cada literal de inventário e antes, cada JSONPath e motivo de NULL, referências de catálogo, tags/placeholders e contagens. Testes negativos verificam rejeição de ordinal/chave adulterados, antes alterado, campo inexistente, motivo falso, referência falsa, contagem falsa e perda de placeholder/tag. A auditoria não avalia estilo automaticamente nem prova comportamento no jogo.

Comando de reprodução, a partir do diretório do pacote extraído: python audit.py --document C:/dev/stolen-realm/docs/automacao/EV-R2-NORMAL-b04-parte02.md. A saída real é preservada em audit-output.txt e no handoff do cartão; nenhuma saída foi escrita aqui antes da execução.

Pendências: revisão independente no MESMO cartão t_821c05b9 e aprovação de conteúdo pelo dono. Sem jogo/runtime, alteração de DLL/plugin, modificação de EV-R1/parte01, publicação ou git push. Aprovar o documento não implementa textos automaticamente.
