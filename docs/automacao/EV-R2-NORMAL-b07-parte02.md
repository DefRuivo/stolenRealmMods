# EV-R2-NORMAL-b07 — parte02: correção da proposta 121–140

Corretivo documental t_744ccfbd. Origem: revisão independente t_4c07d669; cartão original t_179fa90f. Esta parte supersede as acusações e a análise incorretas da parte01; não apaga nem modifica a entrega anterior ou ajustes do dono. Não é implementação, reativação nem aprovação de conteúdo pelo dono.

## Escopo e evidências

Exatamente os 20 eventos Normal de ordinais 121–140. Ordem das seções de lote-Normal-v2.md conferida com o filtro categoria=Normal do JSON, sem ordenar path_id. Os índices $.eventos[N] são índices zero-based do arquivo integral, não uma regra geral de equivalência com ordinal Normal.

Fontes somente leitura em C:/dev/stolen-realm/docs/cobertura/EV-R1/: eventos.json, lote-Normal-v2.md, eventos.schema.json, catalogo-referencias.json. Revisão: independent-review.txt e review-dossier.zip anexados ao pai. Baseline de integridade é o source-hashes-before.json do dossiê (quatro fontes + sete propostas originais, 11 entradas).

b07 NÃO cobre 141–160. As sete entregas revisadas não incluíram essa faixa; há b08-parte141.md/142.md/143.md/144.md separados, NÃO revisados neste parecer. Nenhum desses arquivos foi copiado ou sobrescrito. A revisão de b08 precisa de encaminhamento separado; não se declara 160/160 aprovado e não se implementa outra frente.

## Correções que substituem as acusações falsas

1. Narrativas realmente vazias após strip: 0/20, não 19/20. Os textos completos estão transcritos abaixo. Comprimentos de referência: #127 1350, #128 654, #133 307, #134 837, #135 884, #139 481 caracteres. Prompt de resultados vazio é um campo diferente de narrativa vazia; sua ausência isolada não exige preenchimento.
2. Identidades corretas: #127 resources.assets:2545732; #128 resources.assets:2545734; #139 resources.assets:2545785. Não escolher variantes NotInEventPool pelo título. Todos os 20 eventos têm categoria Normal, e todos os sete testes editoriais têm raridade Common (0).
3. Testes são #121–126 e #129, sete no total. #127 é produção editorial. Produção editorial soma treze: sete com disabled=0 e seis com disabled=1 (#130–132, #137–138, #140). disabled=0 significa flag habilitada no asset, não disponibilidade observada numa partida.
4. Os textos de Annie, da estante do Librarian, do prisioneiro Mad Mage, de Sully e do monólito de gelo Ymir existem. As invenções de criatura animada, ser de papel e pedra com musgo são retiradas. Nada é justificado por conteúdo runtime hipotético.
5. referencia/nome NÃO existem no nível superior de evento. NULL é reportado abaixo com JSONPath exato e motivo do contêiner. Uma referência de batalha/encadeamento nula não prova falta de quest. #133, #138 e #139 possuem ramos que configuram iniciar batalha: o NULL da referência não invalida essa flag nem demonstra resultado final no jogo.
6. A lista [2,0,1,4,5,0] tem seis entradas e cinco valores distintos [0,1,2,4,5]. Ela existe em #136, não em #128. Em #136 allowOnAllTerrainTypes=1; a lista sozinha não comprova restrição de surgimento. #128/#137/#140 têm allowAtAllTimesOfDay=1: allowedTimeOfDay=1 sozinho não significa 'somente de dia'. #138 tem allowAtAllTimesOfDay=0; o enum 1 é conservado sem inventar seu nome. Terrain/node enums ficam em valores literais; nenhum é chamado 'Rune Stone' por suposição.
7. Os termos editoriais são opções de jogo, mesma estrutura e intencional. Títulos repetidos ou nomes de etapas NÃO comprovam GUID duplicado. As identidades de variantes e encadeamentos estão no apêndice específico; os 20 ids deste lote são únicos.

## Convenções de leitura

MANTER = não sugerir alteração do texto original deste evento neste corretivo; não significa perfeição ortográfica, revisão de todos os textos do jogo ou validação em partida. MELHORAR = sugestão pontual de texto original em inglês, em campo que existe, com antes/depois integrais e literais. A correção das acusações da parte01 é CORREÇÃO DA PROPOSTA e vale para todos os vinte, independentemente do veredito.

Os fatos JSONPath são snapshots literais, auditáveis com eventos.json. O sufixo técnico .__quantidade__ é uma contagem calculada da lista precedente, não um campo do JSON nem alvo de alteração. Listas de bônus vazias não viram atributos inventados. RollLimit e tipo de resultado são configuração, não probabilidade medida nem sucesso garantido no jogo. Nenhum limite, status, alvo, peso, raridade, condição ou disabled será alterado.

Os blocos de efeitos preservam alvo serializado, flags, razões e candidatos/modificadores. Self com override=false não é prova de beneficiário final sem considerar seleção e estado de partida. Números como -10.0 em percentMaxHealth são valores do campo, não pontos de vida medidos; quantidades finais de ouro/XP, sorteios e recompensas finais de batalha permanecem NULL com seus motivos. Remoções vazias não implicam remoção de status. Runtime: NAO_EXERCITADO em todos os vinte; nenhum jogo, DLL ou plugin executado.

## Inventário e contagens

```json resumo-b07
{
  "faixa": [
    121,
    140
  ],
  "eventos": 20,
  "chaves_unicas": 20,
  "ids_unicos": 20,
  "categorias": {
    "Normal": 20
  },
  "raridades": {
    "Common": 19,
    "Rare": 1
  },
  "pesos": [
    1.0
  ],
  "vereditos": {
    "MANTER": 11,
    "MELHORAR": 9
  },
  "testes": [
    121,
    122,
    123,
    124,
    125,
    126,
    129
  ],
  "testes_disabled": [
    121,
    122,
    123,
    124,
    125,
    126,
    129
  ],
  "producao_disabled": [
    130,
    131,
    132,
    137,
    138,
    140
  ],
  "producao_enabled": [
    127,
    128,
    133,
    134,
    135,
    136,
    139
  ],
  "disabled_total": 13,
  "narrativas_vazias": 0,
  "prompts_vazios": [
    121,
    124,
    125,
    126,
    127,
    130,
    131,
    132,
    134,
    135,
    136,
    137,
    138,
    140
  ],
  "alteracoes_sugeridas": 11,
  "runtime": "NAO_EXERCITADO",
  "aprovacao_do_dono": "PENDENTE",
  "b08": "141–160: revisão separada necessária; não avaliado neste corretivo"
}
```

| Ordinal | Chave | GUID/id | Título | Categoria | Raridade | Peso | disabled | Classe editorial | Veredito |
|---|---|---|---|---|---|---|---|---|---|
| 121 | resources.assets:2545723 | c2f79869-76f7-4b64-bb7f-336cbc861cd3 | Test - Boss Event Start | Normal | Common (0) | 1.0 | 1 | teste | MANTER |
| 122 | resources.assets:2545724 | 87829a2f-3006-44d6-aaf1-bf8126aa2e32 | Test - Choose As Party Event | Normal | Common (0) | 1.0 | 1 | teste | MANTER |
| 123 | resources.assets:2545725 | d23cbec8-878b-4c45-a4df-015388cc4bb8 | Test - Choose One Character Event | Normal | Common (0) | 1.0 | 1 | teste | MANTER |
| 124 | resources.assets:2545726 | 37649e4c-ed20-4051-8ec6-95b85b451c41 | Test - Individual Event | Normal | Common (0) | 1.0 | 1 | teste | MANTER |
| 125 | resources.assets:2545727 | 6a91c4f8-06ea-4d4d-82a3-c1a4e8c1bffc | Test - Test Key (Get) | Normal | Common (0) | 1.0 | 1 | teste | MANTER |
| 126 | resources.assets:2545728 | f51adc00-9270-4c4f-88f9-afbbd8fc75d3 | Test - Test Key (Use) | Normal | Common (0) | 1.0 | 1 | teste | MANTER |
| 127 | resources.assets:2545732 | 7d008743-08fc-4746-b4c9-2201f70b530f | The Animator | Normal | Common (0) | 1.0 | 0 | produção | MELHORAR |
| 128 | resources.assets:2545734 | 2ca74161-3fe7-459d-bdd7-1b6f4741edc4 | The Fortune Teller | Normal | Common (0) | 1.0 | 0 | produção | MANTER |
| 129 | resources.assets:2545733 | e987802d-9895-46d4-a815-69b95b52633e | The Fortune Teller (Test) | Normal | Common (0) | 1.0 | 1 | teste | MANTER |
| 130 | resources.assets:2545735 | 5e259ead-072f-4025-bab5-1c56bfa6ccfa | The Golden Key | Normal | Common (0) | 1.0 | 1 | produção | MELHORAR |
| 131 | resources.assets:2545736 | 9398b8fa-1e1f-4d92-8540-e37731a0d859 | The King | Normal | Common (0) | 1.0 | 1 | produção | MELHORAR |
| 132 | resources.assets:2545737 | 1f2569a9-949b-494a-9651-eb7f00640707 | The Lady | Normal | Common (0) | 1.0 | 1 | produção | MELHORAR |
| 133 | resources.assets:2545738 | 8b9e013f-5f85-47d8-bffc-f1e573b18612 | The Librarian | Normal | Common (0) | 1.0 | 0 | produção | MELHORAR |
| 134 | resources.assets:2545739 | 435d6bd4-fa60-4982-85f8-e4a0ec083837 | The Mad Mage | Normal | Common (0) | 1.0 | 0 | produção | MANTER |
| 135 | resources.assets:2545742 | 764378be-fa1c-43ef-b0e1-6669614105d4 | The Most Dangerous Game | Normal | Common (0) | 1.0 | 0 | produção | MANTER |
| 136 | resources.assets:2545743 | 930f331a-b7fc-49d6-9e7a-1022733e2fca | The Old Well | Normal | Common (0) | 1.0 | 0 | produção | MANTER |
| 137 | resources.assets:2545744 | e100bc75-b20c-4d3f-a3e1-94e22584cf17 | The Oracle | Normal | Common (0) | 1.0 | 1 | produção | MELHORAR |
| 138 | resources.assets:2545745 | f08738de-ec30-4dd2-b947-2774494301e6 | The Pale Knight | Normal | Rare (2) | 1.0 | 1 | produção | MELHORAR |
| 139 | resources.assets:2545785 | 8e63fbe4-3e26-49fc-b9f0-8f4aa4676f67 | The runes of the Ymir | Normal | Common (0) | 1.0 | 0 | produção | MELHORAR |
| 140 | resources.assets:2545746 | 509fbfa8-efd1-4fb3-a7d0-cdca0266ae83 | The Soothsayer | Normal | Common (0) | 1.0 | 1 | produção | MELHORAR |

## EV-121 — Test - Boss Event Start

Veredito: MANTER. Natureza da análise: CORREÇÃO DA PROPOSTA.

Fixture editorial de teste: narrativa Timmy presente, opção Fight Meh concede Test Event Status - Boss Event. A mistura de textos de baú/chefe é conteúdo de teste, não narrativa ausente. Preservar disabled=1 e não reativar.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
Timmy talked about this chest...
```

Não há sugestão de alteração do texto original para este evento.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 121,
  "chave": "resources.assets:2545723",
  "id": "c2f79869-76f7-4b64-bb7f-336cbc861cd3",
  "titulo": "Test - Boss Event Start",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 1,
  "classificacao_editorial": "teste",
  "veredito": "MANTER",
  "justificativa": "Fixture editorial de teste: narrativa Timmy presente, opção Fight Meh concede Test Event Status - Boss Event. A mistura de textos de baú/chefe é conteúdo de teste, não narrativa ausente. Preservar disabled=1 e não reativar.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[121].chave": "resources.assets:2545723",
    "$.eventos[121].id": "c2f79869-76f7-4b64-bb7f-336cbc861cd3",
    "$.eventos[121].titulo": "Test - Boss Event Start",
    "$.eventos[121].nome_asset": "Test - Boss Event Start",
    "$.eventos[121].categoria": "Normal",
    "$.eventos[121].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[121].peso": 1.0,
    "$.eventos[121].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[121].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[121].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[121].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[121].texto": "Timmy talked about this chest...",
    "$.eventos[121].texto_resultados_possiveis": "",
    "$.eventos[121].condicoes": {
      "disabled": 1,
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
      "KeepInDeckWhenUsed": 1,
      "isLesserEvent": 0,
      "LeadsToFortune": 0
    },
    "$.eventos[121].campos_originais.targetType": 0,
    "$.eventos[121].campos_originais.characterPool": 0,
    "$.eventos[121].campos_originais.RefEventStatuses": [],
    "$.eventos[121].opcoes[0].titulo": "Fight Meh",
    "$.eventos[121].opcoes[0].texto": "Use the key and open the chest.",
    "$.eventos[121].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[121].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[121].opcoes[0].efeitos.__quantidade__": 1,
    "$.eventos[121].opcoes[0].efeitos[0].texto": "You use the key!",
    "$.eventos[121].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[121].opcoes[0].efeitos[0].limite_rolagem": 0,
    "$.eventos[121].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[121].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[121].opcoes[0].efeitos[0].batalha.iniciar": false,
    "$.eventos[121].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[121].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[121].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[121].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[121].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[121].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[121].opcoes[0].efeitos[0].efeitos[0].recompensas": {
      "ouro": {
        "dar": false,
        "retirar": false,
        "razao": 0.0,
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
          "valor": 1,
          "nome": "Global"
        },
        "quantidade_configurada": 1,
        "tabelas": [],
        "restricoes": {
          "limitItemTypes": 1,
          "possibleItemTypes": [
            6,
            7
          ],
          "limitItemRarities": 1,
          "possibleRarities": [
            0,
            1,
            2
          ]
        },
        "sorteio_final": null,
        "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
      },
      "status": {
        "candidatos": [
          {
            "chave": "resources.assets:2545524",
            "nome": "Test Event Status - Boss Event",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545524
            },
            "tipo": "EventStatus",
            "descricao": "A key",
            "duracao": {
              "valor": 1,
              "nome": "Quest"
            },
            "status_tipo": {
              "valor": 0,
              "nome": "Normal"
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
    "$.eventos[121].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[121].opcoes[1].titulo": "Leave",
    "$.eventos[121].opcoes[1].texto": "Dont open this crazy thing",
    "$.eventos[121].opcoes[1].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[121].opcoes[1].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[121].opcoes[1].efeitos.__quantidade__": 0
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[121].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[121].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[121].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[121].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[121].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[121].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[121].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[121].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[121].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": []
}
```

## EV-122 — Test - Choose As Party Event

Veredito: MANTER. Natureza da análise: CORREÇÃO DA PROPOSTA.

Fixture editorial de teste com marcação de texto ondulado e referências [refEventStatus1]/[refEventStatus2]. Open./Close/Mystery têm dados reais; Open. configura iniciar batalha apesar da referência nula. Não inferir quest ausente nem corrigir o fixture como produção. Preservar disabled=1.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
<blue>Why</blue> this text so <wave><red>wavy</red></wave>?

You give me [refEventStatus1], I give you [refEventStatus2].
```

Não há sugestão de alteração do texto original para este evento.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 122,
  "chave": "resources.assets:2545724",
  "id": "87829a2f-3006-44d6-aaf1-bf8126aa2e32",
  "titulo": "Test - Choose As Party Event",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 1,
  "classificacao_editorial": "teste",
  "veredito": "MANTER",
  "justificativa": "Fixture editorial de teste com marcação de texto ondulado e referências [refEventStatus1]/[refEventStatus2]. Open./Close/Mystery têm dados reais; Open. configura iniciar batalha apesar da referência nula. Não inferir quest ausente nem corrigir o fixture como produção. Preservar disabled=1.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[122].chave": "resources.assets:2545724",
    "$.eventos[122].id": "87829a2f-3006-44d6-aaf1-bf8126aa2e32",
    "$.eventos[122].titulo": "Test - Choose As Party Event",
    "$.eventos[122].nome_asset": "Test - Choose As Party Event",
    "$.eventos[122].categoria": "Normal",
    "$.eventos[122].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[122].peso": 1.0,
    "$.eventos[122].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[122].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[122].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[122].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[122].texto": "<blue>Why</blue> this text so <wave><red>wavy</red></wave>?\n\nYou give me [refEventStatus1], I give you [refEventStatus2].",
    "$.eventos[122].texto_resultados_possiveis": "Which will you choose?",
    "$.eventos[122].condicoes": {
      "disabled": 1,
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
    },
    "$.eventos[122].campos_originais.targetType": 0,
    "$.eventos[122].campos_originais.characterPool": 0,
    "$.eventos[122].campos_originais.RefEventStatuses": [
      {
        "m_FileID": 0,
        "m_PathID": 2545529
      },
      {
        "m_FileID": 0,
        "m_PathID": 2545436
      }
    ],
    "$.eventos[122].opcoes[0].titulo": "Open.",
    "$.eventos[122].opcoes[0].texto": "Tacos are dexiious.",
    "$.eventos[122].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[122].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[122].opcoes[0].efeitos.__quantidade__": 1,
    "$.eventos[122].opcoes[0].efeitos[0].texto": "oopsie poopsie",
    "$.eventos[122].opcoes[0].efeitos[0].resultado": {
      "valor": 1,
      "nome": "Failure"
    },
    "$.eventos[122].opcoes[0].efeitos[0].limite_rolagem": 0,
    "$.eventos[122].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[122].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[122].opcoes[0].efeitos[0].batalha.iniciar": true,
    "$.eventos[122].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[122].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[122].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[122].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[122].opcoes[0].efeitos[0].batalha.override": {
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
      "FillOutBattlePoints": 1,
      "OverrideBattlePoints": 1,
      "BattlePointValue": 60,
      "OverrideEnemyGroupPool": 0,
      "EnemyGroupPool": [],
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
    "$.eventos[122].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[122].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[122].opcoes[0].efeitos[0].efeitos[0].recompensas": {
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
    "$.eventos[122].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[122].opcoes[1].titulo": "Close",
    "$.eventos[122].opcoes[1].texto": "Dont open this crazy thing",
    "$.eventos[122].opcoes[1].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[122].opcoes[1].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[122].opcoes[1].efeitos.__quantidade__": 1,
    "$.eventos[122].opcoes[1].efeitos[0].texto": "asdasda",
    "$.eventos[122].opcoes[1].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[122].opcoes[1].efeitos[0].limite_rolagem": 0,
    "$.eventos[122].opcoes[1].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[122].opcoes[1].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[122].opcoes[1].efeitos[0].batalha.iniciar": false,
    "$.eventos[122].opcoes[1].efeitos[0].batalha.manual": false,
    "$.eventos[122].opcoes[1].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[122].opcoes[1].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[122].opcoes[1].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[122].opcoes[1].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[122].opcoes[1].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[122].opcoes[1].efeitos[0].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545505",
            "nome": "Burning Demon Hearts",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545505
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
        ],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      },
      "skills": []
    },
    "$.eventos[122].opcoes[1].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[122].opcoes[2].titulo": "Mystery",
    "$.eventos[122].opcoes[2].texto": "What??",
    "$.eventos[122].opcoes[2].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[122].opcoes[2].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[122].opcoes[2].efeitos.__quantidade__": 1,
    "$.eventos[122].opcoes[2].efeitos[0].texto": "tacos",
    "$.eventos[122].opcoes[2].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[122].opcoes[2].efeitos[0].limite_rolagem": 0,
    "$.eventos[122].opcoes[2].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[122].opcoes[2].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[122].opcoes[2].efeitos[0].batalha.iniciar": false,
    "$.eventos[122].opcoes[2].efeitos[0].batalha.manual": false,
    "$.eventos[122].opcoes[2].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[122].opcoes[2].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[122].opcoes[2].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[122].opcoes[2].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 20.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[122].opcoes[2].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[122].opcoes[2].efeitos[0].efeitos[0].recompensas": {
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
    "$.eventos[122].opcoes[2].efeitos[0].efeitos[0].remocoes_status": []
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[122].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[122].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[122].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[122].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[122].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[122].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[122].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[122].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[122].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[122].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[122].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[122].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[122].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[122].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[122].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[122].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[122].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[122].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[122].opcoes[2].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[122].opcoes[2].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[122].opcoes[2].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[122].opcoes[2].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[122].opcoes[2].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[122].opcoes[2].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[122].opcoes[2].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[122].opcoes[2].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[122].opcoes[2].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": []
}
```

## EV-123 — Test - Choose One Character Event

Veredito: MANTER. Natureza da análise: CORREÇÃO DA PROPOSTA.

Fixture editorial de teste com seleção de personagem: Open. usa Might e Open Better usa Dexterity; ambos têm Success 14 e Failure 0. A narrativa Timmy está presente. Preservar textos de teste e disabled=1.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
Timmy talked about this chest...
```

Não há sugestão de alteração do texto original para este evento.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 123,
  "chave": "resources.assets:2545725",
  "id": "d23cbec8-878b-4c45-a4df-015388cc4bb8",
  "titulo": "Test - Choose One Character Event",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 1,
  "classificacao_editorial": "teste",
  "veredito": "MANTER",
  "justificativa": "Fixture editorial de teste com seleção de personagem: Open. usa Might e Open Better usa Dexterity; ambos têm Success 14 e Failure 0. A narrativa Timmy está presente. Preservar textos de teste e disabled=1.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[123].chave": "resources.assets:2545725",
    "$.eventos[123].id": "d23cbec8-878b-4c45-a4df-015388cc4bb8",
    "$.eventos[123].titulo": "Test - Choose One Character Event",
    "$.eventos[123].nome_asset": "Test - Choose One Character Event",
    "$.eventos[123].categoria": "Normal",
    "$.eventos[123].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[123].peso": 1.0,
    "$.eventos[123].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[123].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[123].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[123].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[123].texto": "Timmy talked about this chest...",
    "$.eventos[123].texto_resultados_possiveis": "Who will dare open this chest?",
    "$.eventos[123].condicoes": {
      "disabled": 1,
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
    },
    "$.eventos[123].campos_originais.targetType": 2,
    "$.eventos[123].campos_originais.characterPool": 0,
    "$.eventos[123].campos_originais.RefEventStatuses": [],
    "$.eventos[123].opcoes[0].titulo": "Open.",
    "$.eventos[123].opcoes[0].texto": "Tacos are dexiious",
    "$.eventos[123].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[123].opcoes[0].rolagem": {
      "bonus": [
        {
          "valor": 0,
          "nome": "Might"
        }
      ],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[123].opcoes[0].efeitos.__quantidade__": 2,
    "$.eventos[123].opcoes[0].efeitos[0].texto": "That was good!",
    "$.eventos[123].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[123].opcoes[0].efeitos[0].limite_rolagem": 14,
    "$.eventos[123].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[123].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[123].opcoes[0].efeitos[0].batalha.iniciar": false,
    "$.eventos[123].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[123].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[123].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[123].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[123].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[123].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[123].opcoes[0].efeitos[0].efeitos[0].recompensas": {
      "ouro": {
        "dar": false,
        "retirar": false,
        "razao": 0.0,
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
          "valor": 1,
          "nome": "Global"
        },
        "quantidade_configurada": 1,
        "tabelas": [],
        "restricoes": {
          "limitItemTypes": 1,
          "possibleItemTypes": [
            6,
            7
          ],
          "limitItemRarities": 1,
          "possibleRarities": [
            0,
            1,
            2
          ]
        },
        "sorteio_final": null,
        "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
      },
      "status": {
        "candidatos": [
          {
            "chave": "resources.assets:2545385",
            "nome": "Forbidden Power",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545385
            },
            "tipo": "EventStatus",
            "descricao": "All mana costs increased by 50%. Power of mana costing abilities increased by 50%.",
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
                "expressao": "50",
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
      },
      "skills": []
    },
    "$.eventos[123].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[123].opcoes[0].efeitos[1].texto": "That was bad...",
    "$.eventos[123].opcoes[0].efeitos[1].resultado": {
      "valor": 1,
      "nome": "Failure"
    },
    "$.eventos[123].opcoes[0].efeitos[1].limite_rolagem": 0,
    "$.eventos[123].opcoes[0].efeitos[1].texto_efeitos_manual": [],
    "$.eventos[123].opcoes[0].efeitos[1].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[123].opcoes[0].efeitos[1].batalha.iniciar": false,
    "$.eventos[123].opcoes[0].efeitos[1].batalha.manual": false,
    "$.eventos[123].opcoes[0].efeitos[1].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[123].opcoes[0].efeitos[1].batalha.dados_recompensa_final": null,
    "$.eventos[123].opcoes[0].efeitos[1].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[123].opcoes[1].titulo": "Open Better",
    "$.eventos[123].opcoes[1].texto": "Tacos are dexiious",
    "$.eventos[123].opcoes[1].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[123].opcoes[1].rolagem": {
      "bonus": [
        {
          "valor": 1,
          "nome": "Dexterity"
        }
      ],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[123].opcoes[1].efeitos.__quantidade__": 2,
    "$.eventos[123].opcoes[1].efeitos[0].texto": "That was good!",
    "$.eventos[123].opcoes[1].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[123].opcoes[1].efeitos[0].limite_rolagem": 14,
    "$.eventos[123].opcoes[1].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[123].opcoes[1].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[123].opcoes[1].efeitos[0].batalha.iniciar": false,
    "$.eventos[123].opcoes[1].efeitos[0].batalha.manual": false,
    "$.eventos[123].opcoes[1].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[123].opcoes[1].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[123].opcoes[1].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[123].opcoes[1].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[123].opcoes[1].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[123].opcoes[1].efeitos[0].efeitos[0].recompensas": {
      "ouro": {
        "dar": false,
        "retirar": false,
        "razao": 0.0,
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
          "valor": 1,
          "nome": "Global"
        },
        "quantidade_configurada": 1,
        "tabelas": [],
        "restricoes": {
          "limitItemTypes": 1,
          "possibleItemTypes": [
            6,
            7
          ],
          "limitItemRarities": 1,
          "possibleRarities": [
            0,
            1,
            2
          ]
        },
        "sorteio_final": null,
        "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
      },
      "status": {
        "candidatos": [
          {
            "chave": "resources.assets:2545385",
            "nome": "Forbidden Power",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545385
            },
            "tipo": "EventStatus",
            "descricao": "All mana costs increased by 50%. Power of mana costing abilities increased by 50%.",
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
                "expressao": "50",
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
      },
      "skills": []
    },
    "$.eventos[123].opcoes[1].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[123].opcoes[1].efeitos[1].texto": "That was bad...",
    "$.eventos[123].opcoes[1].efeitos[1].resultado": {
      "valor": 1,
      "nome": "Failure"
    },
    "$.eventos[123].opcoes[1].efeitos[1].limite_rolagem": 0,
    "$.eventos[123].opcoes[1].efeitos[1].texto_efeitos_manual": [],
    "$.eventos[123].opcoes[1].efeitos[1].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[123].opcoes[1].efeitos[1].batalha.iniciar": false,
    "$.eventos[123].opcoes[1].efeitos[1].batalha.manual": false,
    "$.eventos[123].opcoes[1].efeitos[1].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[123].opcoes[1].efeitos[1].batalha.dados_recompensa_final": null,
    "$.eventos[123].opcoes[1].efeitos[1].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[123].opcoes[2].titulo": "Close",
    "$.eventos[123].opcoes[2].texto": "Dont open this crazy thing",
    "$.eventos[123].opcoes[2].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[123].opcoes[2].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[123].opcoes[2].efeitos.__quantidade__": 1,
    "$.eventos[123].opcoes[2].efeitos[0].texto": "asdasda",
    "$.eventos[123].opcoes[2].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[123].opcoes[2].efeitos[0].limite_rolagem": 0,
    "$.eventos[123].opcoes[2].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[123].opcoes[2].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[123].opcoes[2].efeitos[0].batalha.iniciar": false,
    "$.eventos[123].opcoes[2].efeitos[0].batalha.manual": false,
    "$.eventos[123].opcoes[2].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[123].opcoes[2].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[123].opcoes[2].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[123].opcoes[2].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[123].opcoes[2].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[123].opcoes[2].efeitos[0].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545376",
            "nome": "Curse of Sorrow",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545376
            },
            "tipo": "EventStatus",
            "descricao": "Healing is reduced by 50%.",
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
                  "chave": "resources.assets:2544425",
                  "nome": "HealingReceivedBonus",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544425
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
          }
        ],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      },
      "skills": []
    },
    "$.eventos[123].opcoes[2].efeitos[0].efeitos[0].remocoes_status": []
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[123].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[123].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[123].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[123].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[123].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[123].opcoes[0].efeitos[1].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[0].efeitos[1].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[0].efeitos[1].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[0].efeitos[1].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[0].efeitos[1].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[123].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[123].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[123].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[123].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[123].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[123].opcoes[1].efeitos[1].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[1].efeitos[1].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[1].efeitos[1].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[1].efeitos[1].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[1].efeitos[1].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[123].opcoes[2].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[2].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[2].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[2].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[123].opcoes[2].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[123].opcoes[2].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[123].opcoes[2].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[123].opcoes[2].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[123].opcoes[2].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": []
}
```

## EV-124 — Test - Individual Event

Veredito: MANTER. Natureza da análise: CORREÇÃO DA PROPOSTA.

Fixture editorial de teste individual com narrativa Timmy, uma opção Open. e candidato Test Fortune. LeadsToFortune é 1, não 0 como na proposta anterior. Não substituir o teste por narrativa nova nem reativar.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
Timmy talked about this chest...
```

Não há sugestão de alteração do texto original para este evento.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 124,
  "chave": "resources.assets:2545726",
  "id": "37649e4c-ed20-4051-8ec6-95b85b451c41",
  "titulo": "Test - Individual Event",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 1,
  "classificacao_editorial": "teste",
  "veredito": "MANTER",
  "justificativa": "Fixture editorial de teste individual com narrativa Timmy, uma opção Open. e candidato Test Fortune. LeadsToFortune é 1, não 0 como na proposta anterior. Não substituir o teste por narrativa nova nem reativar.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[124].chave": "resources.assets:2545726",
    "$.eventos[124].id": "37649e4c-ed20-4051-8ec6-95b85b451c41",
    "$.eventos[124].titulo": "Test - Individual Event",
    "$.eventos[124].nome_asset": "Test - Individual Event",
    "$.eventos[124].categoria": "Normal",
    "$.eventos[124].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[124].peso": 1.0,
    "$.eventos[124].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[124].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[124].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[124].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[124].texto": "Timmy talked about this chest...",
    "$.eventos[124].texto_resultados_possiveis": "",
    "$.eventos[124].condicoes": {
      "disabled": 1,
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
      "LeadsToFortune": 1
    },
    "$.eventos[124].campos_originais.targetType": 1,
    "$.eventos[124].campos_originais.characterPool": 0,
    "$.eventos[124].campos_originais.RefEventStatuses": [],
    "$.eventos[124].opcoes[0].titulo": "Open.",
    "$.eventos[124].opcoes[0].texto": "Tacos are dexiious",
    "$.eventos[124].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[124].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[124].opcoes[0].efeitos.__quantidade__": 1,
    "$.eventos[124].opcoes[0].efeitos[0].texto": "That was bad",
    "$.eventos[124].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[124].opcoes[0].efeitos[0].limite_rolagem": 0,
    "$.eventos[124].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[124].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[124].opcoes[0].efeitos[0].batalha.iniciar": false,
    "$.eventos[124].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[124].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[124].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[124].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[124].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[124].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[124].opcoes[0].efeitos[0].efeitos[0].recompensas": {
      "ouro": {
        "dar": false,
        "retirar": false,
        "razao": 0.0,
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
          "valor": 1,
          "nome": "Global"
        },
        "quantidade_configurada": 1,
        "tabelas": [],
        "restricoes": {
          "limitItemTypes": 1,
          "possibleItemTypes": [
            6,
            7
          ],
          "limitItemRarities": 1,
          "possibleRarities": [
            0,
            1,
            2
          ]
        },
        "sorteio_final": null,
        "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
      },
      "status": {
        "candidatos": [
          {
            "chave": "resources.assets:2545530",
            "nome": "Test Fortune",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545530
            },
            "tipo": "EventStatus",
            "descricao": "",
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
                  "chave": "resources.assets:2544376",
                  "nome": "DamageModColdToFrozen",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544376
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "100",
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
    "$.eventos[124].opcoes[0].efeitos[0].efeitos[0].remocoes_status": []
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[124].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[124].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[124].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[124].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[124].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[124].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[124].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[124].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[124].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": []
}
```

## EV-125 — Test - Test Key (Get)

Veredito: MANTER. Natureza da análise: CORREÇÃO DA PROPOSTA.

Fixture editorial de obtenção de chave: Take Key concede Test Event Status - Test Key (resources.assets:2545529); Leave não possui ações. Texto original presente. Preservar disabled=1.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
Timmy talked about this chest...
```

Não há sugestão de alteração do texto original para este evento.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 125,
  "chave": "resources.assets:2545727",
  "id": "6a91c4f8-06ea-4d4d-82a3-c1a4e8c1bffc",
  "titulo": "Test - Test Key (Get)",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 1,
  "classificacao_editorial": "teste",
  "veredito": "MANTER",
  "justificativa": "Fixture editorial de obtenção de chave: Take Key concede Test Event Status - Test Key (resources.assets:2545529); Leave não possui ações. Texto original presente. Preservar disabled=1.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[125].chave": "resources.assets:2545727",
    "$.eventos[125].id": "6a91c4f8-06ea-4d4d-82a3-c1a4e8c1bffc",
    "$.eventos[125].titulo": "Test - Test Key (Get)",
    "$.eventos[125].nome_asset": "Test - Test Key (Get)",
    "$.eventos[125].categoria": "Normal",
    "$.eventos[125].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[125].peso": 1.0,
    "$.eventos[125].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[125].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[125].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[125].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[125].texto": "Timmy talked about this chest...",
    "$.eventos[125].texto_resultados_possiveis": "",
    "$.eventos[125].condicoes": {
      "disabled": 1,
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
    },
    "$.eventos[125].campos_originais.targetType": 0,
    "$.eventos[125].campos_originais.characterPool": 0,
    "$.eventos[125].campos_originais.RefEventStatuses": [],
    "$.eventos[125].opcoes[0].titulo": "Take Key",
    "$.eventos[125].opcoes[0].texto": "Grab the test key!",
    "$.eventos[125].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[125].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[125].opcoes[0].efeitos.__quantidade__": 1,
    "$.eventos[125].opcoes[0].efeitos[0].texto": "You got the key!",
    "$.eventos[125].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[125].opcoes[0].efeitos[0].limite_rolagem": 0,
    "$.eventos[125].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[125].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[125].opcoes[0].efeitos[0].batalha.iniciar": false,
    "$.eventos[125].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[125].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[125].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[125].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[125].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[125].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[125].opcoes[0].efeitos[0].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545529",
            "nome": "Test Event Status - Test Key",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545529
            },
            "tipo": "EventStatus",
            "descricao": "A key",
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
        ],
        "sortear": false,
        "quantidade_sorteada_configurada": 1,
        "resultado_sorteado": null,
        "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
      },
      "skills": []
    },
    "$.eventos[125].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[125].opcoes[1].titulo": "Leave",
    "$.eventos[125].opcoes[1].texto": "Don't take the key.",
    "$.eventos[125].opcoes[1].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[125].opcoes[1].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[125].opcoes[1].efeitos.__quantidade__": 0
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[125].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[125].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[125].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[125].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[125].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[125].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[125].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[125].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[125].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": []
}
```

## EV-126 — Test - Test Key (Use)

Veredito: MANTER. Natureza da análise: CORREÇÃO DA PROPOSTA.

Fixture editorial de uso de chave: Open. exige resources.assets:2545529 e oculta sem requisito; Get Key é ocultada quando esse status está presente. Get Key e Leave não possuem ações no inventário. Não confundir ausência de ação com texto narrativo vazio. Preservar disabled=1.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
Timmy talked about this chest...
```

Não há sugestão de alteração do texto original para este evento.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 126,
  "chave": "resources.assets:2545728",
  "id": "f51adc00-9270-4c4f-88f9-afbbd8fc75d3",
  "titulo": "Test - Test Key (Use)",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 1,
  "classificacao_editorial": "teste",
  "veredito": "MANTER",
  "justificativa": "Fixture editorial de uso de chave: Open. exige resources.assets:2545529 e oculta sem requisito; Get Key é ocultada quando esse status está presente. Get Key e Leave não possuem ações no inventário. Não confundir ausência de ação com texto narrativo vazio. Preservar disabled=1.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[126].chave": "resources.assets:2545728",
    "$.eventos[126].id": "f51adc00-9270-4c4f-88f9-afbbd8fc75d3",
    "$.eventos[126].titulo": "Test - Test Key (Use)",
    "$.eventos[126].nome_asset": "Test - Test Key (Use)",
    "$.eventos[126].categoria": "Normal",
    "$.eventos[126].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[126].peso": 1.0,
    "$.eventos[126].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[126].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[126].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[126].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[126].texto": "Timmy talked about this chest...",
    "$.eventos[126].texto_resultados_possiveis": "",
    "$.eventos[126].condicoes": {
      "disabled": 1,
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
    },
    "$.eventos[126].campos_originais.targetType": 0,
    "$.eventos[126].campos_originais.characterPool": 0,
    "$.eventos[126].campos_originais.RefEventStatuses": [],
    "$.eventos[126].opcoes[0].titulo": "Open.",
    "$.eventos[126].opcoes[0].texto": "You already have the key!  Use it!",
    "$.eventos[126].opcoes[0].condicoes": {
      "status_requeridos": [
        {
          "chave": "resources.assets:2545529",
          "nome": "Test Event Status - Test Key",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545529
          },
          "tipo": "EventStatus",
          "descricao": "A key",
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
      ],
      "ocultar_sem_requisitos": true,
      "ocultar_se_status": []
    },
    "$.eventos[126].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[126].opcoes[0].efeitos.__quantidade__": 1,
    "$.eventos[126].opcoes[0].efeitos[0].texto": "You use the key!",
    "$.eventos[126].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[126].opcoes[0].efeitos[0].limite_rolagem": 0,
    "$.eventos[126].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[126].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[126].opcoes[0].efeitos[0].batalha.iniciar": false,
    "$.eventos[126].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[126].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[126].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[126].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[126].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[126].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[126].opcoes[0].efeitos[0].efeitos[0].recompensas": {
      "ouro": {
        "dar": false,
        "retirar": false,
        "razao": 0.0,
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
          "valor": 1,
          "nome": "Global"
        },
        "quantidade_configurada": 1,
        "tabelas": [],
        "restricoes": {
          "limitItemTypes": 1,
          "possibleItemTypes": [
            6,
            7
          ],
          "limitItemRarities": 1,
          "possibleRarities": [
            0,
            1,
            2
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
    "$.eventos[126].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[126].opcoes[1].titulo": "Get Key",
    "$.eventos[126].opcoes[1].texto": "You don't have the key yet.  Get it!",
    "$.eventos[126].opcoes[1].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": [
        {
          "chave": "resources.assets:2545529",
          "nome": "Test Event Status - Test Key",
          "pptr": {
            "m_FileID": 0,
            "m_PathID": 2545529
          },
          "tipo": "EventStatus",
          "descricao": "A key",
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
    },
    "$.eventos[126].opcoes[1].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[126].opcoes[1].efeitos.__quantidade__": 0,
    "$.eventos[126].opcoes[2].titulo": "Leave",
    "$.eventos[126].opcoes[2].texto": "Dont open this crazy thing",
    "$.eventos[126].opcoes[2].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[126].opcoes[2].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[126].opcoes[2].efeitos.__quantidade__": 0
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[126].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[126].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[126].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[126].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[126].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[126].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[126].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[126].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[126].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": []
}
```

## EV-127 — The Animator

Veredito: MELHORAR. Natureza da análise: CORREÇÃO DA PROPOSTA.

Annie é uma mulher que trabalha num golem de ferro alimentado por corações de Fire Demons. A narrativa de 1350 caracteres já existe e será preservada. Uniformizar Ani para Annie na resposta de Accept; não inventar criatura animada nem preencher resultados vazios.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
The glow of a dim lantern casts eerie shadows on the cavern walls, illuminating the determined figure of a woman as she diligently works on a massive iron golem. Tools and scraps of metal litter the ground around her, and the low echo of her humming resonates throughout the cave.

Looking up in surprise, her eyes quickly flicker with a spark of intrigue as she takes you in. "Well, look who the night dragged in," she says with a chuckle, brushing back a loose strand of hair from her face.


"I'm known as '<gold><incr><b>The Animator</b></incr></gold>', but you can call me Annie," she says, her voice carrying a lively lilt as she gestures to the metal monolith beside her. The golem is an impressive sight - a titan of iron and magic, currently lifeless and cold.


"My iron giant here seems to have run out of juice," she admits with a sheepish smile. "You see, he's powered by the hearts of <b><red><incr>Fire Demons</incr></red></b>. Mighty tough to acquire, but oh-so efficient."


A light dances in her eyes as she looks you over, sizing you up. "I've got a proposal for you," she says, her voice taking on a hopeful tone. "There's a pack of those beasts nearby, stirring up all kinds of trouble. If you can handle them, bring me their hearts. In return, I'll lend you my golem's assistance once he's back up and running. What do you say?"
```

Sugestão não implementada: os blocos alteracoes abaixo contêm campo existente, campo serializado equivalente, antes literal e depois exato. Não há alteração de valores mecânicos, condições ou referências.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 127,
  "chave": "resources.assets:2545732",
  "id": "7d008743-08fc-4746-b4c9-2201f70b530f",
  "titulo": "The Animator",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 0,
  "classificacao_editorial": "produção",
  "veredito": "MELHORAR",
  "justificativa": "Annie é uma mulher que trabalha num golem de ferro alimentado por corações de Fire Demons. A narrativa de 1350 caracteres já existe e será preservada. Uniformizar Ani para Annie na resposta de Accept; não inventar criatura animada nem preencher resultados vazios.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[127].chave": "resources.assets:2545732",
    "$.eventos[127].id": "7d008743-08fc-4746-b4c9-2201f70b530f",
    "$.eventos[127].titulo": "The Animator",
    "$.eventos[127].nome_asset": "The Animator",
    "$.eventos[127].categoria": "Normal",
    "$.eventos[127].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[127].peso": 1.0,
    "$.eventos[127].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[127].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[127].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[127].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[127].texto": "The glow of a dim lantern casts eerie shadows on the cavern walls, illuminating the determined figure of a woman as she diligently works on a massive iron golem. Tools and scraps of metal litter the ground around her, and the low echo of her humming resonates throughout the cave.\n\nLooking up in surprise, her eyes quickly flicker with a spark of intrigue as she takes you in. \"Well, look who the night dragged in,\" she says with a chuckle, brushing back a loose strand of hair from her face.\n\n\n\"I'm known as '<gold><incr><b>The Animator</b></incr></gold>', but you can call me Annie,\" she says, her voice carrying a lively lilt as she gestures to the metal monolith beside her. The golem is an impressive sight - a titan of iron and magic, currently lifeless and cold.\n\n\n\"My iron giant here seems to have run out of juice,\" she admits with a sheepish smile. \"You see, he's powered by the hearts of <b><red><incr>Fire Demons</incr></red></b>. Mighty tough to acquire, but oh-so efficient.\"\n\n\nA light dances in her eyes as she looks you over, sizing you up. \"I've got a proposal for you,\" she says, her voice taking on a hopeful tone. \"There's a pack of those beasts nearby, stirring up all kinds of trouble. If you can handle them, bring me their hearts. In return, I'll lend you my golem's assistance once he's back up and running. What do you say?\"",
    "$.eventos[127].texto_resultados_possiveis": "",
    "$.eventos[127].condicoes": {
      "disabled": 0,
      "EditorOnly": 0,
      "allowOnAllNodeTypes": 0,
      "allowedNodeTypes": [
        7
      ],
      "requiredStatusesToSpawn": [],
      "allowOnAllTerrainTypes": 0,
      "allowedTerrainTypes": [
        4
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
    "$.eventos[127].campos_originais.targetType": 0,
    "$.eventos[127].campos_originais.characterPool": 0,
    "$.eventos[127].campos_originais.RefEventStatuses": [],
    "$.eventos[127].opcoes[0].titulo": "Accept",
    "$.eventos[127].opcoes[0].texto": "Agree to hunt the Fire Demons.",
    "$.eventos[127].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[127].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[127].opcoes[0].efeitos.__quantidade__": 1,
    "$.eventos[127].opcoes[0].efeitos[0].texto": " \"Thank you,\" Ani says earnestly. \"The demons are nesting in a lair to the east. Be careful. They're more dangerous than they look.\"",
    "$.eventos[127].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[127].opcoes[0].efeitos[0].limite_rolagem": 0,
    "$.eventos[127].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[127].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[127].opcoes[0].efeitos[0].batalha.iniciar": false,
    "$.eventos[127].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[127].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[127].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[127].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[127].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[127].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[127].opcoes[0].efeitos[0].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545515",
            "nome": "The Animator - Quest Accept",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545515
            },
            "tipo": "EventStatus",
            "descricao": "",
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
      },
      "skills": []
    },
    "$.eventos[127].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[127].opcoes[1].titulo": "Leave",
    "$.eventos[127].opcoes[1].texto": "You can't be bothered right now.",
    "$.eventos[127].opcoes[1].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[127].opcoes[1].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[127].opcoes[1].efeitos.__quantidade__": 1,
    "$.eventos[127].opcoes[1].efeitos[0].texto": "The Animator’s face falls momentarily, but she quickly regains her composure, offering the group a small, understanding smile. \"I see,\" she replies, nodding. \"Every adventurer must walk their own path. I won't keep you from yours. If you ever need help or simply fancy a bit of demon hunting, remember this place.\"",
    "$.eventos[127].opcoes[1].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[127].opcoes[1].efeitos[0].limite_rolagem": 0,
    "$.eventos[127].opcoes[1].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[127].opcoes[1].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[127].opcoes[1].efeitos[0].batalha.iniciar": false,
    "$.eventos[127].opcoes[1].efeitos[0].batalha.manual": false,
    "$.eventos[127].opcoes[1].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[127].opcoes[1].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[127].opcoes[1].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[127].opcoes[1].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[127].opcoes[1].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[127].opcoes[1].efeitos[0].efeitos[0].recompensas": {
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
    "$.eventos[127].opcoes[1].efeitos[0].efeitos[0].remocoes_status": []
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[127].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[127].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[127].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[127].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[127].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[127].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[127].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[127].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[127].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[127].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[127].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[127].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[127].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[127].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[127].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[127].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[127].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[127].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL",
      "idioma": "inglês",
      "campo": "$.eventos[127].opcoes[0].efeitos[0].texto",
      "campo_original": "$.eventos[127].opcoes[0].efeitos[0].campos_originais.activationText",
      "antes": " \"Thank you,\" Ani says earnestly. \"The demons are nesting in a lair to the east. Be careful. They're more dangerous than they look.\"",
      "depois": " \"Thank you,\" Annie says earnestly. \"The demons are nesting in a lair to the east. Be careful. They're more dangerous than they look.\"",
      "motivo": "Padronização do nome apresentado como Annie na narrativa existente.",
      "implementado": false
    }
  ]
}
```

## EV-128 — The Fortune Teller

Veredito: MANTER. Natureza da análise: CORREÇÃO DA PROPOSTA.

A elfa e a bola de cristal estão descritas nos 654 caracteres existentes. See/Witness/View têm Success 11 e Failure 1, com bonus=[]: não são três testes de atributos distintos. Preservar escolha de visões e consequências registradas; o deslize bare na narrativa é reconhecido, mas não há proposta de revisão desse campo neste corretivo. As condições reais não contêm a lista [2,0,1,4,5,0] atribuída anteriormente a este evento.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
Your eyes are drawn to a mysterious figure standing in a clearing, the glow from a crystal ball illuminates her elegant features. Her hair is the color of moonlight, her eyes as deep as the forest night, and her ears bare the unmistakable point of the elven race.

Without lifting her gaze from the swirling mists within the crystal ball, she greets you. "Welcome, adventurer. I have been expecting you." Her fingers trace patterns over the surface of the crystal ball. "Fate has woven a curious tapestry for you. As a seer, it is my task to reveal its design."

As she speaks, the mists within the crystal ball swirl and coalesce, forming vivid images. 
```

Não há sugestão de alteração do texto original para este evento.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 128,
  "chave": "resources.assets:2545734",
  "id": "2ca74161-3fe7-459d-bdd7-1b6f4741edc4",
  "titulo": "The Fortune Teller",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 0,
  "classificacao_editorial": "produção",
  "veredito": "MANTER",
  "justificativa": "A elfa e a bola de cristal estão descritas nos 654 caracteres existentes. See/Witness/View têm Success 11 e Failure 1, com bonus=[]: não são três testes de atributos distintos. Preservar escolha de visões e consequências registradas; o deslize bare na narrativa é reconhecido, mas não há proposta de revisão desse campo neste corretivo. As condições reais não contêm a lista [2,0,1,4,5,0] atribuída anteriormente a este evento.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[128].chave": "resources.assets:2545734",
    "$.eventos[128].id": "2ca74161-3fe7-459d-bdd7-1b6f4741edc4",
    "$.eventos[128].titulo": "The Fortune Teller",
    "$.eventos[128].nome_asset": "The Fortune Teller",
    "$.eventos[128].categoria": "Normal",
    "$.eventos[128].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[128].peso": 1.0,
    "$.eventos[128].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[128].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[128].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[128].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[128].texto": "Your eyes are drawn to a mysterious figure standing in a clearing, the glow from a crystal ball illuminates her elegant features. Her hair is the color of moonlight, her eyes as deep as the forest night, and her ears bare the unmistakable point of the elven race.\n\nWithout lifting her gaze from the swirling mists within the crystal ball, she greets you. \"Welcome, adventurer. I have been expecting you.\" Her fingers trace patterns over the surface of the crystal ball. \"Fate has woven a curious tapestry for you. As a seer, it is my task to reveal its design.\"\n\nAs she speaks, the mists within the crystal ball swirl and coalesce, forming vivid images. ",
    "$.eventos[128].texto_resultados_possiveis": "Dare to gaze into the Crystal Ball?",
    "$.eventos[128].condicoes": {
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
      "allowAtAllLevels": 1,
      "minLevel": 1,
      "terrainTypesAllowedAtAnyTime": [
        4,
        3
      ],
      "KeepInDeckWhenUsed": 0,
      "isLesserEvent": 0,
      "LeadsToFortune": 1
    },
    "$.eventos[128].campos_originais.targetType": 3,
    "$.eventos[128].campos_originais.characterPool": 0,
    "$.eventos[128].campos_originais.RefEventStatuses": [],
    "$.eventos[128].opcoes[0].titulo": "See",
    "$.eventos[128].opcoes[0].texto": "Gaze into the Crystal Ball.",
    "$.eventos[128].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[128].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[128].opcoes[0].efeitos.__quantidade__": 2,
    "$.eventos[128].opcoes[0].efeitos[0].texto": "You see your enemies, battered and broken, scattered before you like leaves in the wind. Your heart swells with confidence as you witness yourself, stronger than ever, defeating your foes with ease.",
    "$.eventos[128].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[128].opcoes[0].efeitos[0].limite_rolagem": 11,
    "$.eventos[128].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[128].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[128].opcoes[0].efeitos[0].batalha.iniciar": false,
    "$.eventos[128].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[128].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[128].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[128].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[128].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[128].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[128].opcoes[0].efeitos[0].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545452",
            "nome": "Martial Prowess",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545452
            },
            "tipo": "EventStatus",
            "descricao": "Increases @Physical Damage@ by {5,20}%.",
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
                "expressao": "{5,20}",
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
    "$.eventos[128].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[128].opcoes[0].efeitos[1].texto": "You see yourself, battered and broken, lying defeated on the ground.",
    "$.eventos[128].opcoes[0].efeitos[1].resultado": {
      "valor": 1,
      "nome": "Failure"
    },
    "$.eventos[128].opcoes[0].efeitos[1].limite_rolagem": 1,
    "$.eventos[128].opcoes[0].efeitos[1].texto_efeitos_manual": [],
    "$.eventos[128].opcoes[0].efeitos[1].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[128].opcoes[0].efeitos[1].batalha.iniciar": false,
    "$.eventos[128].opcoes[0].efeitos[1].batalha.manual": false,
    "$.eventos[128].opcoes[0].efeitos[1].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[128].opcoes[0].efeitos[1].batalha.dados_recompensa_final": null,
    "$.eventos[128].opcoes[0].efeitos[1].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[128].opcoes[0].efeitos[1].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[128].opcoes[0].efeitos[1].efeitos[0].alvo": {
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
    "$.eventos[128].opcoes[0].efeitos[1].efeitos[0].recompensas": {
      "ouro": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      },
      "experiencia": {
        "dar": false,
        "razao": 3.0,
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
            "chave": "resources.assets:2545489",
            "nome": "Battered",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545489
            },
            "tipo": "EventStatus",
            "descricao": "Reduces @Armor@ and @Magic Armor@ by @25%@ per stack.",
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
                  "chave": "resources.assets:2544401",
                  "nome": "Armor",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544401
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 1,
                  "nome": "Percentage"
                },
                "expressao": "-25",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544430",
                  "nome": "MagicArmor",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544430
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 1,
                  "nome": "Percentage"
                },
                "expressao": "-25",
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
      },
      "skills": []
    },
    "$.eventos[128].opcoes[0].efeitos[1].efeitos[0].remocoes_status": [],
    "$.eventos[128].opcoes[1].titulo": "Witness",
    "$.eventos[128].opcoes[1].texto": "Look into your future.",
    "$.eventos[128].opcoes[1].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[128].opcoes[1].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[128].opcoes[1].efeitos.__quantidade__": 2,
    "$.eventos[128].opcoes[1].efeitos[0].texto": "A vision appears, of you standing amidst a storm, lightning crackling around you, a vortex of wind swirling, fire dancing around your form, and ice spiraling up to the sky. The elements combining to empower you, bending to your will.",
    "$.eventos[128].opcoes[1].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[128].opcoes[1].efeitos[0].limite_rolagem": 11,
    "$.eventos[128].opcoes[1].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[128].opcoes[1].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[128].opcoes[1].efeitos[0].batalha.iniciar": false,
    "$.eventos[128].opcoes[1].efeitos[0].batalha.manual": false,
    "$.eventos[128].opcoes[1].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[128].opcoes[1].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[128].opcoes[1].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[128].opcoes[1].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[128].opcoes[1].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[128].opcoes[1].efeitos[0].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545431",
            "nome": "Elemental Power",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545431
            },
            "tipo": "EventStatus",
            "descricao": "Increases @Elemental Damage@ by {5,25}%.",
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
                  "chave": "resources.assets:2544375",
                  "nome": "DamageModCold",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544375
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{5,25}",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544377",
                  "nome": "DamageModFire",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544377
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{5,25}",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544379",
                  "nome": "DamageModLightning",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544379
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{5,25}",
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
    "$.eventos[128].opcoes[1].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[128].opcoes[1].efeitos[1].texto": "You see yourself surrounded by a maelstrom of elements. Fire, ice, and thunder combined in a destructive whirlwind that consume you, leaving nothing but ashes in its wake.",
    "$.eventos[128].opcoes[1].efeitos[1].resultado": {
      "valor": 1,
      "nome": "Failure"
    },
    "$.eventos[128].opcoes[1].efeitos[1].limite_rolagem": 1,
    "$.eventos[128].opcoes[1].efeitos[1].texto_efeitos_manual": [],
    "$.eventos[128].opcoes[1].efeitos[1].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[128].opcoes[1].efeitos[1].batalha.iniciar": false,
    "$.eventos[128].opcoes[1].efeitos[1].batalha.manual": false,
    "$.eventos[128].opcoes[1].efeitos[1].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[128].opcoes[1].efeitos[1].batalha.dados_recompensa_final": null,
    "$.eventos[128].opcoes[1].efeitos[1].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[128].opcoes[1].efeitos[1].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[128].opcoes[1].efeitos[1].efeitos[0].alvo": {
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
    "$.eventos[128].opcoes[1].efeitos[1].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545499",
            "nome": "Severely Burned",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545499
            },
            "tipo": "EventStatus",
            "descricao": "Reduces @Fire Resistance@ by @25%@ per stack.",
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
                  "chave": "resources.assets:2544498",
                  "nome": "ResistFire",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544498
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
          },
          {
            "chave": "resources.assets:2545496",
            "nome": "Frostbitten",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545496
            },
            "tipo": "EventStatus",
            "descricao": "Reduces @Cold Resistance@ by @25%@ per stack.",
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
                  "chave": "resources.assets:2544495",
                  "nome": "ResistCold",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544495
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
          },
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
      },
      "skills": []
    },
    "$.eventos[128].opcoes[1].efeitos[1].efeitos[0].remocoes_status": [],
    "$.eventos[128].opcoes[2].titulo": "View",
    "$.eventos[128].opcoes[2].texto": "Observe what is to come.",
    "$.eventos[128].opcoes[2].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[128].opcoes[2].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[128].opcoes[2].efeitos.__quantidade__": 2,
    "$.eventos[128].opcoes[2].efeitos[0].texto": "You see yourself, fatigued and injured, yet unyielding, enduring against an onslaught that would break lesser beings. You rise again and again, indomitable, an embodiment of perseverance.",
    "$.eventos[128].opcoes[2].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[128].opcoes[2].efeitos[0].limite_rolagem": 11,
    "$.eventos[128].opcoes[2].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[128].opcoes[2].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[128].opcoes[2].efeitos[0].batalha.iniciar": false,
    "$.eventos[128].opcoes[2].efeitos[0].batalha.manual": false,
    "$.eventos[128].opcoes[2].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[128].opcoes[2].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[128].opcoes[2].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[128].opcoes[2].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[128].opcoes[2].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[128].opcoes[2].efeitos[0].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545438",
            "nome": "Endurance",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545438
            },
            "tipo": "EventStatus",
            "descricao": "Increases @Max Health@ by {5, 500}.",
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
                  "chave": "resources.assets:2544436",
                  "nome": "MaxHealth",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544436
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{5, 500}",
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
    "$.eventos[128].opcoes[2].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[128].opcoes[2].efeitos[1].texto": "You see yourself in the throes of an enduring struggle, pushing past your limits only to collapse, your own endurance betraying you at the last moment.",
    "$.eventos[128].opcoes[2].efeitos[1].resultado": {
      "valor": 1,
      "nome": "Failure"
    },
    "$.eventos[128].opcoes[2].efeitos[1].limite_rolagem": 1,
    "$.eventos[128].opcoes[2].efeitos[1].texto_efeitos_manual": [],
    "$.eventos[128].opcoes[2].efeitos[1].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[128].opcoes[2].efeitos[1].batalha.iniciar": false,
    "$.eventos[128].opcoes[2].efeitos[1].batalha.manual": false,
    "$.eventos[128].opcoes[2].efeitos[1].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[128].opcoes[2].efeitos[1].batalha.dados_recompensa_final": null,
    "$.eventos[128].opcoes[2].efeitos[1].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[128].opcoes[2].efeitos[1].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[128].opcoes[2].efeitos[1].efeitos[0].alvo": {
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
    "$.eventos[128].opcoes[2].efeitos[1].efeitos[0].recompensas": {
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
      },
      "skills": []
    },
    "$.eventos[128].opcoes[2].efeitos[1].efeitos[0].remocoes_status": []
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[128].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[128].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[128].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[128].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[128].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[128].opcoes[0].efeitos[1].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[0].efeitos[1].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[0].efeitos[1].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[0].efeitos[1].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[0].efeitos[1].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[128].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[128].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[128].opcoes[0].efeitos[1].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[128].opcoes[0].efeitos[1].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[128].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[128].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[128].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[128].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[128].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[128].opcoes[1].efeitos[1].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[1].efeitos[1].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[1].efeitos[1].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[1].efeitos[1].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[1].efeitos[1].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[128].opcoes[1].efeitos[1].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[128].opcoes[1].efeitos[1].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[128].opcoes[1].efeitos[1].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[128].opcoes[1].efeitos[1].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[128].opcoes[2].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[2].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[2].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[2].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[2].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[128].opcoes[2].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[128].opcoes[2].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[128].opcoes[2].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[128].opcoes[2].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[128].opcoes[2].efeitos[1].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[2].efeitos[1].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[2].efeitos[1].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[2].efeitos[1].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[128].opcoes[2].efeitos[1].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[128].opcoes[2].efeitos[1].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[128].opcoes[2].efeitos[1].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[128].opcoes[2].efeitos[1].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[128].opcoes[2].efeitos[1].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": []
}
```

## EV-129 — The Fortune Teller (Test)

Veredito: MANTER. Natureza da análise: CORREÇÃO DA PROPOSTA.

Classificação editorial de teste fundamentada no título e nome_asset The Fortune Teller (Test), narrativa de 366 caracteres e disabled=1. See/Witness/View têm ramos Success 11/Failure 1. Não é duplicata comprovada do GUID de #128: identidade própria e textos distintos. Preservar o fixture sem reativação.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
A <violet><b><incr>Mysterious Elf</incr></b></violet> stands before a glimmering Crystal Ball. She stares intently into the Crystal and greets you without looking up.

"Welcome Heroes, I have been expecting you."

"I, the wonderous <violet><b><incr>Fortune Teller</incr></b></violet>, shall grant you a gift. Look into the Crystal Ball and you will see your future!"
```

Não há sugestão de alteração do texto original para este evento.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 129,
  "chave": "resources.assets:2545733",
  "id": "e987802d-9895-46d4-a815-69b95b52633e",
  "titulo": "The Fortune Teller (Test)",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 1,
  "classificacao_editorial": "teste",
  "veredito": "MANTER",
  "justificativa": "Classificação editorial de teste fundamentada no título e nome_asset The Fortune Teller (Test), narrativa de 366 caracteres e disabled=1. See/Witness/View têm ramos Success 11/Failure 1. Não é duplicata comprovada do GUID de #128: identidade própria e textos distintos. Preservar o fixture sem reativação.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[129].chave": "resources.assets:2545733",
    "$.eventos[129].id": "e987802d-9895-46d4-a815-69b95b52633e",
    "$.eventos[129].titulo": "The Fortune Teller (Test)",
    "$.eventos[129].nome_asset": "The Fortune Teller (Test)",
    "$.eventos[129].categoria": "Normal",
    "$.eventos[129].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[129].peso": 1.0,
    "$.eventos[129].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[129].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[129].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[129].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[129].texto": "A <violet><b><incr>Mysterious Elf</incr></b></violet> stands before a glimmering Crystal Ball. She stares intently into the Crystal and greets you without looking up.\n\n\"Welcome Heroes, I have been expecting you.\"\n\n\"I, the wonderous <violet><b><incr>Fortune Teller</incr></b></violet>, shall grant you a gift. Look into the Crystal Ball and you will see your future!\"",
    "$.eventos[129].texto_resultados_possiveis": "What do you see?",
    "$.eventos[129].condicoes": {
      "disabled": 1,
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
      "allowAtAllLevels": 1,
      "minLevel": 1,
      "terrainTypesAllowedAtAnyTime": [
        4,
        3
      ],
      "KeepInDeckWhenUsed": 0,
      "isLesserEvent": 0,
      "LeadsToFortune": 1
    },
    "$.eventos[129].campos_originais.targetType": 3,
    "$.eventos[129].campos_originais.characterPool": 0,
    "$.eventos[129].campos_originais.RefEventStatuses": [],
    "$.eventos[129].opcoes[0].titulo": "See",
    "$.eventos[129].opcoes[0].texto": "Gaze into the Crystal Ball.",
    "$.eventos[129].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[129].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[129].opcoes[0].efeitos.__quantidade__": 2,
    "$.eventos[129].opcoes[0].efeitos[0].texto": "\"I see my enemies... battered and broken!\". Gain [o1a1_status].",
    "$.eventos[129].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[129].opcoes[0].efeitos[0].limite_rolagem": 11,
    "$.eventos[129].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[129].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[129].opcoes[0].efeitos[0].batalha.iniciar": false,
    "$.eventos[129].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[129].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[129].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[129].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[129].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[129].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[129].opcoes[0].efeitos[0].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545452",
            "nome": "Martial Prowess",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545452
            },
            "tipo": "EventStatus",
            "descricao": "Increases @Physical Damage@ by {5,20}%.",
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
                "expressao": "{5,20}",
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
    "$.eventos[129].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[129].opcoes[0].efeitos[1].texto": "\"I see my body... battered and broken\". Gain [o1a2_status], [o1a2_status2].",
    "$.eventos[129].opcoes[0].efeitos[1].resultado": {
      "valor": 1,
      "nome": "Failure"
    },
    "$.eventos[129].opcoes[0].efeitos[1].limite_rolagem": 1,
    "$.eventos[129].opcoes[0].efeitos[1].texto_efeitos_manual": [],
    "$.eventos[129].opcoes[0].efeitos[1].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[129].opcoes[0].efeitos[1].batalha.iniciar": false,
    "$.eventos[129].opcoes[0].efeitos[1].batalha.manual": false,
    "$.eventos[129].opcoes[0].efeitos[1].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[129].opcoes[0].efeitos[1].batalha.dados_recompensa_final": null,
    "$.eventos[129].opcoes[0].efeitos[1].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[129].opcoes[0].efeitos[1].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[129].opcoes[0].efeitos[1].efeitos[0].alvo": {
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
    "$.eventos[129].opcoes[0].efeitos[1].efeitos[0].recompensas": {
      "ouro": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      },
      "experiencia": {
        "dar": false,
        "razao": 3.0,
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
            "chave": "resources.assets:2545489",
            "nome": "Battered",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545489
            },
            "tipo": "EventStatus",
            "descricao": "Reduces @Armor@ and @Magic Armor@ by @25%@ per stack.",
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
                  "chave": "resources.assets:2544401",
                  "nome": "Armor",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544401
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 1,
                  "nome": "Percentage"
                },
                "expressao": "-25",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544430",
                  "nome": "MagicArmor",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544430
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 1,
                  "nome": "Percentage"
                },
                "expressao": "-25",
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
      },
      "skills": []
    },
    "$.eventos[129].opcoes[0].efeitos[1].efeitos[0].remocoes_status": [],
    "$.eventos[129].opcoes[1].titulo": "Witness",
    "$.eventos[129].opcoes[1].texto": "Look into your future.",
    "$.eventos[129].opcoes[1].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[129].opcoes[1].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[129].opcoes[1].efeitos.__quantidade__": 2,
    "$.eventos[129].opcoes[1].efeitos[0].texto": "\"I see the elements... combined to empower me!\" Gain [o2a1_status].",
    "$.eventos[129].opcoes[1].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[129].opcoes[1].efeitos[0].limite_rolagem": 11,
    "$.eventos[129].opcoes[1].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[129].opcoes[1].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[129].opcoes[1].efeitos[0].batalha.iniciar": false,
    "$.eventos[129].opcoes[1].efeitos[0].batalha.manual": false,
    "$.eventos[129].opcoes[1].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[129].opcoes[1].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[129].opcoes[1].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[129].opcoes[1].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[129].opcoes[1].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[129].opcoes[1].efeitos[0].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545431",
            "nome": "Elemental Power",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545431
            },
            "tipo": "EventStatus",
            "descricao": "Increases @Elemental Damage@ by {5,25}%.",
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
                  "chave": "resources.assets:2544375",
                  "nome": "DamageModCold",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544375
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{5,25}",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544377",
                  "nome": "DamageModFire",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544377
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{5,25}",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544379",
                  "nome": "DamageModLightning",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544379
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{5,25}",
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
    "$.eventos[129].opcoes[1].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[129].opcoes[1].efeitos[1].texto": "\"I see the elements... combined to destroy me.\" Gain [o2a2_status], [o2a2_status2], [o2a2_status3].",
    "$.eventos[129].opcoes[1].efeitos[1].resultado": {
      "valor": 1,
      "nome": "Failure"
    },
    "$.eventos[129].opcoes[1].efeitos[1].limite_rolagem": 1,
    "$.eventos[129].opcoes[1].efeitos[1].texto_efeitos_manual": [],
    "$.eventos[129].opcoes[1].efeitos[1].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[129].opcoes[1].efeitos[1].batalha.iniciar": false,
    "$.eventos[129].opcoes[1].efeitos[1].batalha.manual": false,
    "$.eventos[129].opcoes[1].efeitos[1].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[129].opcoes[1].efeitos[1].batalha.dados_recompensa_final": null,
    "$.eventos[129].opcoes[1].efeitos[1].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[129].opcoes[1].efeitos[1].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[129].opcoes[1].efeitos[1].efeitos[0].alvo": {
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
    "$.eventos[129].opcoes[1].efeitos[1].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545499",
            "nome": "Severely Burned",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545499
            },
            "tipo": "EventStatus",
            "descricao": "Reduces @Fire Resistance@ by @25%@ per stack.",
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
                  "chave": "resources.assets:2544498",
                  "nome": "ResistFire",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544498
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
          },
          {
            "chave": "resources.assets:2545496",
            "nome": "Frostbitten",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545496
            },
            "tipo": "EventStatus",
            "descricao": "Reduces @Cold Resistance@ by @25%@ per stack.",
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
                  "chave": "resources.assets:2544495",
                  "nome": "ResistCold",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544495
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
          },
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
      },
      "skills": []
    },
    "$.eventos[129].opcoes[1].efeitos[1].efeitos[0].remocoes_status": [],
    "$.eventos[129].opcoes[2].titulo": "View",
    "$.eventos[129].opcoes[2].texto": "Observe what is to come.",
    "$.eventos[129].opcoes[2].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[129].opcoes[2].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[129].opcoes[2].efeitos.__quantidade__": 2,
    "$.eventos[129].opcoes[2].efeitos[0].texto": "\"I see my own endurance unyielding!\" Gain [o3a1_status].",
    "$.eventos[129].opcoes[2].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[129].opcoes[2].efeitos[0].limite_rolagem": 11,
    "$.eventos[129].opcoes[2].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[129].opcoes[2].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[129].opcoes[2].efeitos[0].batalha.iniciar": false,
    "$.eventos[129].opcoes[2].efeitos[0].batalha.manual": false,
    "$.eventos[129].opcoes[2].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[129].opcoes[2].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[129].opcoes[2].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[129].opcoes[2].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[129].opcoes[2].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[129].opcoes[2].efeitos[0].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545438",
            "nome": "Endurance",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545438
            },
            "tipo": "EventStatus",
            "descricao": "Increases @Max Health@ by {5, 500}.",
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
                  "chave": "resources.assets:2544436",
                  "nome": "MaxHealth",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544436
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{5, 500}",
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
    "$.eventos[129].opcoes[2].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[129].opcoes[2].efeitos[1].texto": "\"I see my own strength...fails in the end.\" Gain [o3a2_status], [o3a2_status2].",
    "$.eventos[129].opcoes[2].efeitos[1].resultado": {
      "valor": 1,
      "nome": "Failure"
    },
    "$.eventos[129].opcoes[2].efeitos[1].limite_rolagem": 1,
    "$.eventos[129].opcoes[2].efeitos[1].texto_efeitos_manual": [],
    "$.eventos[129].opcoes[2].efeitos[1].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[129].opcoes[2].efeitos[1].batalha.iniciar": false,
    "$.eventos[129].opcoes[2].efeitos[1].batalha.manual": false,
    "$.eventos[129].opcoes[2].efeitos[1].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[129].opcoes[2].efeitos[1].batalha.dados_recompensa_final": null,
    "$.eventos[129].opcoes[2].efeitos[1].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[129].opcoes[2].efeitos[1].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[129].opcoes[2].efeitos[1].efeitos[0].alvo": {
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
    "$.eventos[129].opcoes[2].efeitos[1].efeitos[0].recompensas": {
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
      },
      "skills": []
    },
    "$.eventos[129].opcoes[2].efeitos[1].efeitos[0].remocoes_status": []
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[129].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[129].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[129].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[129].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[129].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[129].opcoes[0].efeitos[1].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[0].efeitos[1].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[0].efeitos[1].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[0].efeitos[1].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[0].efeitos[1].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[129].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[129].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[129].opcoes[0].efeitos[1].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[129].opcoes[0].efeitos[1].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[129].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[129].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[129].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[129].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[129].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[129].opcoes[1].efeitos[1].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[1].efeitos[1].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[1].efeitos[1].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[1].efeitos[1].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[1].efeitos[1].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[129].opcoes[1].efeitos[1].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[129].opcoes[1].efeitos[1].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[129].opcoes[1].efeitos[1].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[129].opcoes[1].efeitos[1].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[129].opcoes[2].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[2].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[2].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[2].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[2].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[129].opcoes[2].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[129].opcoes[2].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[129].opcoes[2].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[129].opcoes[2].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[129].opcoes[2].efeitos[1].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[2].efeitos[1].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[2].efeitos[1].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[2].efeitos[1].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[129].opcoes[2].efeitos[1].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[129].opcoes[2].efeitos[1].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[129].opcoes[2].efeitos[1].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[129].opcoes[2].efeitos[1].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[129].opcoes[2].efeitos[1].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": []
}
```

## EV-130 — The Golden Key

Veredito: MELHORAR. Natureza da análise: CORREÇÃO DA PROPOSTA.

Há narrativa de fantasma, não texto vazio. Refinar pontuação e clareza da mão estendida sem inventar uma chave dourada só pelo título. Reach mantém o candidato Ethereal e [o1a1_status]; disabled=1 permanece.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
The yearning ghost extends her hand pleading for help.
```

Sugestão não implementada: os blocos alteracoes abaixo contêm campo existente, campo serializado equivalente, antes literal e depois exato. Não há alteração de valores mecânicos, condições ou referências.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 130,
  "chave": "resources.assets:2545735",
  "id": "5e259ead-072f-4025-bab5-1c56bfa6ccfa",
  "titulo": "The Golden Key",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 1,
  "classificacao_editorial": "produção",
  "veredito": "MELHORAR",
  "justificativa": "Há narrativa de fantasma, não texto vazio. Refinar pontuação e clareza da mão estendida sem inventar uma chave dourada só pelo título. Reach mantém o candidato Ethereal e [o1a1_status]; disabled=1 permanece.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[130].chave": "resources.assets:2545735",
    "$.eventos[130].id": "5e259ead-072f-4025-bab5-1c56bfa6ccfa",
    "$.eventos[130].titulo": "The Golden Key",
    "$.eventos[130].nome_asset": "The Golden Key",
    "$.eventos[130].categoria": "Normal",
    "$.eventos[130].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[130].peso": 1.0,
    "$.eventos[130].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[130].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[130].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[130].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[130].texto": "The yearning ghost extends her hand pleading for help.",
    "$.eventos[130].texto_resultados_possiveis": "",
    "$.eventos[130].condicoes": {
      "disabled": 1,
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
      "LeadsToFortune": 1
    },
    "$.eventos[130].campos_originais.targetType": 0,
    "$.eventos[130].campos_originais.characterPool": 0,
    "$.eventos[130].campos_originais.RefEventStatuses": [],
    "$.eventos[130].opcoes[0].titulo": "Reach",
    "$.eventos[130].opcoes[0].texto": "You reach out to the ghost. Gain [o1a1_status].",
    "$.eventos[130].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[130].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[130].opcoes[0].efeitos.__quantidade__": 1,
    "$.eventos[130].opcoes[0].efeitos[0].texto": "You reach out, but your hand passes through cold air. Memories flood your mind and longing fills your heart.\n\nYou gain [o1a1_status].",
    "$.eventos[130].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[130].opcoes[0].efeitos[0].limite_rolagem": 0,
    "$.eventos[130].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[130].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[130].opcoes[0].efeitos[0].batalha.iniciar": false,
    "$.eventos[130].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[130].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[130].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[130].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[130].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[130].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[130].opcoes[0].efeitos[0].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545439",
            "nome": "Ethereal",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545439
            },
            "tipo": "EventStatus",
            "descricao": "Increases @Physical Resistance@ by {10,50}%. Reduces @Elemental Resistance@ by {5,25}%.",
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
                  "chave": "resources.assets:2544500",
                  "nome": "ResistPhysical",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544500
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{10,50}",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544495",
                  "nome": "ResistCold",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544495
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{-5,-25}",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544498",
                  "nome": "ResistFire",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544498
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{-5,-25}",
                "segunda_passagem": false
              },
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
                "expressao": "{-5,-25}",
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
    "$.eventos[130].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[130].opcoes[1].titulo": "Leave",
    "$.eventos[130].opcoes[1].texto": "The chill in the air causes you to hesitate. You leave without helping.",
    "$.eventos[130].opcoes[1].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[130].opcoes[1].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[130].opcoes[1].efeitos.__quantidade__": 1,
    "$.eventos[130].opcoes[1].efeitos[0].texto": "You leave, but the ghost's disappointment haunts your dreams.",
    "$.eventos[130].opcoes[1].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[130].opcoes[1].efeitos[0].limite_rolagem": 0,
    "$.eventos[130].opcoes[1].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[130].opcoes[1].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[130].opcoes[1].efeitos[0].batalha.iniciar": false,
    "$.eventos[130].opcoes[1].efeitos[0].batalha.manual": false,
    "$.eventos[130].opcoes[1].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[130].opcoes[1].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[130].opcoes[1].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[130].opcoes[1].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[130].opcoes[1].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[130].opcoes[1].efeitos[0].efeitos[0].recompensas": {
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
    "$.eventos[130].opcoes[1].efeitos[0].efeitos[0].remocoes_status": []
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[130].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[130].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[130].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[130].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[130].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[130].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[130].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[130].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[130].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[130].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[130].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[130].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[130].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[130].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[130].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[130].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[130].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[130].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL",
      "idioma": "inglês",
      "campo": "$.eventos[130].texto",
      "campo_original": "$.eventos[130].campos_originais.encounterText",
      "antes": "The yearning ghost extends her hand pleading for help.",
      "depois": "The yearning ghost extends her hand, silently pleading for help.",
      "motivo": "Separar a ação da súplica e tornar a frase mais fluida; conservar fantasma e pedido de ajuda existentes.",
      "implementado": false
    }
  ]
}
```

## EV-131 — The King

Veredito: MELHORAR. Natureza da análise: CORREÇÃO DA PROPOSTA.

O título The King não autoriza inventar um rei: o texto existente descreve um fantasma feminino. Melhorar a mesma narrativa curta mantendo seu conteúdo e Ethereal na ação Reach. O campo disabled=1 não muda.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
The yearning ghost extends her hand pleading for help.
```

Sugestão não implementada: os blocos alteracoes abaixo contêm campo existente, campo serializado equivalente, antes literal e depois exato. Não há alteração de valores mecânicos, condições ou referências.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 131,
  "chave": "resources.assets:2545736",
  "id": "9398b8fa-1e1f-4d92-8540-e37731a0d859",
  "titulo": "The King",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 1,
  "classificacao_editorial": "produção",
  "veredito": "MELHORAR",
  "justificativa": "O título The King não autoriza inventar um rei: o texto existente descreve um fantasma feminino. Melhorar a mesma narrativa curta mantendo seu conteúdo e Ethereal na ação Reach. O campo disabled=1 não muda.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[131].chave": "resources.assets:2545736",
    "$.eventos[131].id": "9398b8fa-1e1f-4d92-8540-e37731a0d859",
    "$.eventos[131].titulo": "The King",
    "$.eventos[131].nome_asset": "The King",
    "$.eventos[131].categoria": "Normal",
    "$.eventos[131].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[131].peso": 1.0,
    "$.eventos[131].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[131].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[131].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[131].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[131].texto": "The yearning ghost extends her hand pleading for help.",
    "$.eventos[131].texto_resultados_possiveis": "",
    "$.eventos[131].condicoes": {
      "disabled": 1,
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
      "LeadsToFortune": 1
    },
    "$.eventos[131].campos_originais.targetType": 0,
    "$.eventos[131].campos_originais.characterPool": 0,
    "$.eventos[131].campos_originais.RefEventStatuses": [],
    "$.eventos[131].opcoes[0].titulo": "Reach",
    "$.eventos[131].opcoes[0].texto": "You reach out to the ghost. Gain [o1a1_status].",
    "$.eventos[131].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[131].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[131].opcoes[0].efeitos.__quantidade__": 1,
    "$.eventos[131].opcoes[0].efeitos[0].texto": "You reach out, but your hand passes through cold air. Memories flood your mind and longing fills your heart.\n\nYou gain [o1a1_status].",
    "$.eventos[131].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[131].opcoes[0].efeitos[0].limite_rolagem": 0,
    "$.eventos[131].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[131].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[131].opcoes[0].efeitos[0].batalha.iniciar": false,
    "$.eventos[131].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[131].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[131].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[131].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[131].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[131].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[131].opcoes[0].efeitos[0].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545439",
            "nome": "Ethereal",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545439
            },
            "tipo": "EventStatus",
            "descricao": "Increases @Physical Resistance@ by {10,50}%. Reduces @Elemental Resistance@ by {5,25}%.",
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
                  "chave": "resources.assets:2544500",
                  "nome": "ResistPhysical",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544500
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{10,50}",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544495",
                  "nome": "ResistCold",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544495
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{-5,-25}",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544498",
                  "nome": "ResistFire",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544498
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{-5,-25}",
                "segunda_passagem": false
              },
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
                "expressao": "{-5,-25}",
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
    "$.eventos[131].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[131].opcoes[1].titulo": "Leave",
    "$.eventos[131].opcoes[1].texto": "The chill in the air causes you to hesitate. You leave without helping.",
    "$.eventos[131].opcoes[1].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[131].opcoes[1].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[131].opcoes[1].efeitos.__quantidade__": 1,
    "$.eventos[131].opcoes[1].efeitos[0].texto": "You leave, but the ghost's disappointment haunts your dreams.",
    "$.eventos[131].opcoes[1].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[131].opcoes[1].efeitos[0].limite_rolagem": 0,
    "$.eventos[131].opcoes[1].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[131].opcoes[1].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[131].opcoes[1].efeitos[0].batalha.iniciar": false,
    "$.eventos[131].opcoes[1].efeitos[0].batalha.manual": false,
    "$.eventos[131].opcoes[1].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[131].opcoes[1].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[131].opcoes[1].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[131].opcoes[1].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[131].opcoes[1].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[131].opcoes[1].efeitos[0].efeitos[0].recompensas": {
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
    "$.eventos[131].opcoes[1].efeitos[0].efeitos[0].remocoes_status": []
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[131].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[131].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[131].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[131].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[131].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[131].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[131].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[131].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[131].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[131].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[131].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[131].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[131].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[131].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[131].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[131].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[131].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[131].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL",
      "idioma": "inglês",
      "campo": "$.eventos[131].texto",
      "campo_original": "$.eventos[131].campos_originais.encounterText",
      "antes": "The yearning ghost extends her hand pleading for help.",
      "depois": "The yearning ghost extends her hand, silently pleading for help.",
      "motivo": "Revisão de fluidez do texto existente; nenhuma nova identidade ou história inferida pelo título.",
      "implementado": false
    }
  ]
}
```

## EV-132 — The Lady

Veredito: MELHORAR. Natureza da análise: CORREÇÃO DA PROPOSTA.

A narrativa de fantasma feminino está presente e coincide com #130/#131, mas cada evento tem GUID próprio. Melhorar somente pontuação/fluidez; conservar Reach/Leave, [o1a1_status], Ethereal e disabled=1.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
The yearning ghost extends her hand pleading for help.
```

Sugestão não implementada: os blocos alteracoes abaixo contêm campo existente, campo serializado equivalente, antes literal e depois exato. Não há alteração de valores mecânicos, condições ou referências.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 132,
  "chave": "resources.assets:2545737",
  "id": "1f2569a9-949b-494a-9651-eb7f00640707",
  "titulo": "The Lady",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 1,
  "classificacao_editorial": "produção",
  "veredito": "MELHORAR",
  "justificativa": "A narrativa de fantasma feminino está presente e coincide com #130/#131, mas cada evento tem GUID próprio. Melhorar somente pontuação/fluidez; conservar Reach/Leave, [o1a1_status], Ethereal e disabled=1.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[132].chave": "resources.assets:2545737",
    "$.eventos[132].id": "1f2569a9-949b-494a-9651-eb7f00640707",
    "$.eventos[132].titulo": "The Lady",
    "$.eventos[132].nome_asset": "The Lady",
    "$.eventos[132].categoria": "Normal",
    "$.eventos[132].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[132].peso": 1.0,
    "$.eventos[132].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[132].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[132].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[132].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[132].texto": "The yearning ghost extends her hand pleading for help.",
    "$.eventos[132].texto_resultados_possiveis": "",
    "$.eventos[132].condicoes": {
      "disabled": 1,
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
      "LeadsToFortune": 1
    },
    "$.eventos[132].campos_originais.targetType": 0,
    "$.eventos[132].campos_originais.characterPool": 0,
    "$.eventos[132].campos_originais.RefEventStatuses": [],
    "$.eventos[132].opcoes[0].titulo": "Reach",
    "$.eventos[132].opcoes[0].texto": "You reach out to the ghost. Gain [o1a1_status].",
    "$.eventos[132].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[132].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[132].opcoes[0].efeitos.__quantidade__": 1,
    "$.eventos[132].opcoes[0].efeitos[0].texto": "You reach out, but your hand passes through cold air. Memories flood your mind and longing fills your heart.\n\nYou gain [o1a1_status].",
    "$.eventos[132].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[132].opcoes[0].efeitos[0].limite_rolagem": 0,
    "$.eventos[132].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[132].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[132].opcoes[0].efeitos[0].batalha.iniciar": false,
    "$.eventos[132].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[132].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[132].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[132].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[132].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[132].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[132].opcoes[0].efeitos[0].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545439",
            "nome": "Ethereal",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545439
            },
            "tipo": "EventStatus",
            "descricao": "Increases @Physical Resistance@ by {10,50}%. Reduces @Elemental Resistance@ by {5,25}%.",
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
                  "chave": "resources.assets:2544500",
                  "nome": "ResistPhysical",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544500
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{10,50}",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544495",
                  "nome": "ResistCold",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544495
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{-5,-25}",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544498",
                  "nome": "ResistFire",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544498
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{-5,-25}",
                "segunda_passagem": false
              },
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
                "expressao": "{-5,-25}",
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
    "$.eventos[132].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[132].opcoes[1].titulo": "Leave",
    "$.eventos[132].opcoes[1].texto": "The chill in the air causes you to hesitate. You leave without helping.",
    "$.eventos[132].opcoes[1].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[132].opcoes[1].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[132].opcoes[1].efeitos.__quantidade__": 1,
    "$.eventos[132].opcoes[1].efeitos[0].texto": "You leave, but the ghost's disappointment haunts your dreams.",
    "$.eventos[132].opcoes[1].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[132].opcoes[1].efeitos[0].limite_rolagem": 0,
    "$.eventos[132].opcoes[1].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[132].opcoes[1].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[132].opcoes[1].efeitos[0].batalha.iniciar": false,
    "$.eventos[132].opcoes[1].efeitos[0].batalha.manual": false,
    "$.eventos[132].opcoes[1].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[132].opcoes[1].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[132].opcoes[1].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[132].opcoes[1].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[132].opcoes[1].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[132].opcoes[1].efeitos[0].efeitos[0].recompensas": {
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
    "$.eventos[132].opcoes[1].efeitos[0].efeitos[0].remocoes_status": []
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[132].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[132].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[132].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[132].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[132].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[132].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[132].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[132].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[132].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[132].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[132].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[132].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[132].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[132].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[132].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[132].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[132].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[132].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL",
      "idioma": "inglês",
      "campo": "$.eventos[132].texto",
      "campo_original": "$.eventos[132].campos_originais.encounterText",
      "antes": "The yearning ghost extends her hand pleading for help.",
      "depois": "The yearning ghost extends her hand, silently pleading for help.",
      "motivo": "Revisão textual pontual, sem tratar título ou texto compartilhado como duplicação de identidade.",
      "implementado": false
    }
  ]
}
```

## EV-133 — The Librarian

Veredito: MELHORAR. Natureza da análise: CORREÇÃO DA PROPOSTA.

É uma estante de livros antigos, não um ser de papel. A narrativa de 307 caracteres e What will you do? existem. Uniformizar o presente na ação Search/Success que revela The Arcane Aegis e Tome of Tadashi; preservar nomes, alcova, recompensa e Search/Failure que configura batalha.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
The bookshelf stands tall and imposing, a silent guardian of untold knowledge and secrets. Each shelf is laden with worn-out tomes, their leather-bound covers etched with golden glyphs, their pages yellowed with age. It is a treasure trove of forgotten lore and secret wisdom, just waiting to be discovered.
```

Sugestão não implementada: os blocos alteracoes abaixo contêm campo existente, campo serializado equivalente, antes literal e depois exato. Não há alteração de valores mecânicos, condições ou referências.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 133,
  "chave": "resources.assets:2545738",
  "id": "8b9e013f-5f85-47d8-bffc-f1e573b18612",
  "titulo": "The Librarian",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 0,
  "classificacao_editorial": "produção",
  "veredito": "MELHORAR",
  "justificativa": "É uma estante de livros antigos, não um ser de papel. A narrativa de 307 caracteres e What will you do? existem. Uniformizar o presente na ação Search/Success que revela The Arcane Aegis e Tome of Tadashi; preservar nomes, alcova, recompensa e Search/Failure que configura batalha.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[133].chave": "resources.assets:2545738",
    "$.eventos[133].id": "8b9e013f-5f85-47d8-bffc-f1e573b18612",
    "$.eventos[133].titulo": "The Librarian",
    "$.eventos[133].nome_asset": "The Librarian",
    "$.eventos[133].categoria": "Normal",
    "$.eventos[133].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[133].peso": 1.0,
    "$.eventos[133].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[133].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[133].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[133].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[133].texto": "The bookshelf stands tall and imposing, a silent guardian of untold knowledge and secrets. Each shelf is laden with worn-out tomes, their leather-bound covers etched with golden glyphs, their pages yellowed with age. It is a treasure trove of forgotten lore and secret wisdom, just waiting to be discovered.",
    "$.eventos[133].texto_resultados_possiveis": "What will you do?",
    "$.eventos[133].condicoes": {
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
      "LeadsToFortune": 1
    },
    "$.eventos[133].campos_originais.targetType": 0,
    "$.eventos[133].campos_originais.characterPool": 0,
    "$.eventos[133].campos_originais.RefEventStatuses": [],
    "$.eventos[133].opcoes[0].titulo": "Search",
    "$.eventos[133].opcoes[0].texto": "Scour the books for something of value.",
    "$.eventos[133].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[133].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[133].opcoes[0].efeitos.__quantidade__": 2,
    "$.eventos[133].opcoes[0].efeitos[0].texto": "You trace your fingers along the spines, the worn leather and embossed titles speaking of long lost times and forgotten wisdom. And then, as if guided by an unseen hand, you stop at a particular book, 'The Arcane Aegis,' it read. You tug at it. It feels oddly firm, refusing to give way like the others. You pull harder. There is a soft click, and the bookshelf trembles.\n\n\nWith a low grinding sound that echoes through the quiet chamber, the entire bookshelf begins to swing forward, revealing a hidden alcove behind. Your heart pounds in anticipation. Inside the alcove, atop a marble pedestal, rested a book far grander than any you have ever seen.\n\n\nThe Tome of Tadashi.",
    "$.eventos[133].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[133].opcoes[0].efeitos[0].limite_rolagem": 10,
    "$.eventos[133].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[133].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[133].opcoes[0].efeitos[0].batalha.iniciar": false,
    "$.eventos[133].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[133].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[133].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[133].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[133].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[133].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[133].opcoes[0].efeitos[0].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545480",
            "nome": "Tome of Tadashi",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545480
            },
            "tipo": "EventStatus",
            "descricao": "Grants spells that can allow the user to escape death. Grants {2,10}% Dodge Chance.\n\n<i><color=#808080>\"Living is more than just staying alive, but staying alive can certainly help.\"</i></color> \n",
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
                  "chave": "resources.assets:2544416",
                  "nome": "DodgeChance",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544416
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{2,10}",
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
    "$.eventos[133].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[133].opcoes[0].efeitos[1].texto": "You begin to search methodically, scanning the titles and occasionally pulling out a volume to flip through its pages. Hours seem to pass in minutes as you continue your hunt for a valuable secret hidden within these books.\n\nSuddenly, a harsh clatter sounds, the peaceful silence of the library shatters like glass. You whip around, your heart pounding in your chest. The guards, alerted by the sound, have arrived. ",
    "$.eventos[133].opcoes[0].efeitos[1].resultado": {
      "valor": 1,
      "nome": "Failure"
    },
    "$.eventos[133].opcoes[0].efeitos[1].limite_rolagem": 0,
    "$.eventos[133].opcoes[0].efeitos[1].texto_efeitos_manual": [],
    "$.eventos[133].opcoes[0].efeitos[1].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[133].opcoes[0].efeitos[1].batalha.iniciar": true,
    "$.eventos[133].opcoes[0].efeitos[1].batalha.manual": false,
    "$.eventos[133].opcoes[0].efeitos[1].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[133].opcoes[0].efeitos[1].batalha.dados_recompensa_final": null,
    "$.eventos[133].opcoes[0].efeitos[1].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[133].opcoes[0].efeitos[1].batalha.override": {
      "ForceRandomSuperUnique": 1,
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
        "m_PathID": 0
      },
      "FailureEvent": {
        "m_FileID": 0,
        "m_PathID": 0
      },
      "EnemyTurnFirst": 0,
      "ForceMap": 1,
      "MapToForce": {
        "m_FileID": 0,
        "m_PathID": 2547165
      },
      "ovrEnemyStatusRefList": [],
      "ovrEnemyModRefList": []
    },
    "$.eventos[133].opcoes[1].titulo": "Leave",
    "$.eventos[133].opcoes[1].texto": "Decide against exploring the bookshelf.",
    "$.eventos[133].opcoes[1].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[133].opcoes[1].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[133].opcoes[1].efeitos.__quantidade__": 1,
    "$.eventos[133].opcoes[1].efeitos[0].texto": "",
    "$.eventos[133].opcoes[1].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[133].opcoes[1].efeitos[0].limite_rolagem": 0,
    "$.eventos[133].opcoes[1].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[133].opcoes[1].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[133].opcoes[1].efeitos[0].batalha.iniciar": false,
    "$.eventos[133].opcoes[1].efeitos[0].batalha.manual": false,
    "$.eventos[133].opcoes[1].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[133].opcoes[1].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[133].opcoes[1].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[133].opcoes[1].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[133].opcoes[1].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[133].opcoes[1].efeitos[0].efeitos[0].recompensas": {
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
    "$.eventos[133].opcoes[1].efeitos[0].efeitos[0].remocoes_status": []
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[133].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[133].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[133].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[133].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[133].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[133].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[133].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[133].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[133].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[133].opcoes[0].efeitos[1].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[133].opcoes[0].efeitos[1].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[133].opcoes[0].efeitos[1].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[133].opcoes[0].efeitos[1].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[133].opcoes[0].efeitos[1].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[133].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[133].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[133].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[133].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[133].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[133].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[133].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[133].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[133].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL",
      "idioma": "inglês",
      "campo": "$.eventos[133].opcoes[0].efeitos[0].texto",
      "campo_original": "$.eventos[133].opcoes[0].efeitos[0].campos_originais.activationText",
      "antes": "You trace your fingers along the spines, the worn leather and embossed titles speaking of long lost times and forgotten wisdom. And then, as if guided by an unseen hand, you stop at a particular book, 'The Arcane Aegis,' it read. You tug at it. It feels oddly firm, refusing to give way like the others. You pull harder. There is a soft click, and the bookshelf trembles.\n\n\nWith a low grinding sound that echoes through the quiet chamber, the entire bookshelf begins to swing forward, revealing a hidden alcove behind. Your heart pounds in anticipation. Inside the alcove, atop a marble pedestal, rested a book far grander than any you have ever seen.\n\n\nThe Tome of Tadashi.",
      "depois": "You trace your fingers along the spines, the worn leather and embossed titles speaking of long lost times and forgotten wisdom. And then, as if guided by an unseen hand, you stop at a particular book, 'The Arcane Aegis,' it reads. You tug at it. It feels oddly firm, refusing to give way like the others. You pull harder. There is a soft click, and the bookshelf trembles.\n\n\nWith a low grinding sound that echoes through the quiet chamber, the entire bookshelf begins to swing forward, revealing a hidden alcove behind. Your heart pounds in anticipation. Inside the alcove, atop a marble pedestal, rests a book far grander than any you have ever seen.\n\n\nThe Tome of Tadashi.",
      "motivo": "Consistência do tempo verbal no relato já majoritariamente no presente; lore e desfechos preservados.",
      "implementado": false
    }
  ]
}
```

## EV-134 — The Mad Mage

Veredito: MANTER. Natureza da análise: CORREÇÃO DA PROPOSTA.

Os 837 caracteres descrevem o prisioneiro e três correntes elementais; Break rompe a de fogo, configura percentMaxHealth=-10.0, Touch of Flame e Severely Burned, e encadeia The Mad Mage 2 (resources.assets:2545740). Leave possui resposta própria. Manter o conteúdo e o encadeamento reais, não um suposto texto runtime. Há deslizes de aspas/raspes no original: este veredito preserva o conteúdo, não certifica revisão ortográfica integral.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
A lone prisoner, clothed in frayed rags, stands in a circle of magic chains. Each glows with a strange power. One blazes with searing fire, the second shimmers with frosty ice, and the third crackles with wild bolts of thunder and lightning.

As you approach, the prisoner's eyes flicker to life, a spark of hope kindling within the depth of his tired gaze. You...you can free me," he raspes, his voice hoarse from disuse. "I beg you, grant me this freedom. Look at me, bound by the cruelty of these chains. They leech my power, my essence." 

His eyes, a mirror to his tormented soul, flash with a haunting light as he glances down at the chains. "Help me, and I will help you. It is a trade, a pact, an oath. I've been trapped here for centuries, my power bound, my voice unheard. Release me from this torment, adventurer." he pleads.
```

Não há sugestão de alteração do texto original para este evento.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 134,
  "chave": "resources.assets:2545739",
  "id": "435d6bd4-fa60-4982-85f8-e4a0ec083837",
  "titulo": "The Mad Mage",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 0,
  "classificacao_editorial": "produção",
  "veredito": "MANTER",
  "justificativa": "Os 837 caracteres descrevem o prisioneiro e três correntes elementais; Break rompe a de fogo, configura percentMaxHealth=-10.0, Touch of Flame e Severely Burned, e encadeia The Mad Mage 2 (resources.assets:2545740). Leave possui resposta própria. Manter o conteúdo e o encadeamento reais, não um suposto texto runtime. Há deslizes de aspas/raspes no original: este veredito preserva o conteúdo, não certifica revisão ortográfica integral.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[134].chave": "resources.assets:2545739",
    "$.eventos[134].id": "435d6bd4-fa60-4982-85f8-e4a0ec083837",
    "$.eventos[134].titulo": "The Mad Mage",
    "$.eventos[134].nome_asset": "The Mad Mage 1",
    "$.eventos[134].categoria": "Normal",
    "$.eventos[134].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[134].peso": 1.0,
    "$.eventos[134].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[134].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[134].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[134].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[134].texto": "A lone prisoner, clothed in frayed rags, stands in a circle of magic chains. Each glows with a strange power. One blazes with searing fire, the second shimmers with frosty ice, and the third crackles with wild bolts of thunder and lightning.\n\nAs you approach, the prisoner's eyes flicker to life, a spark of hope kindling within the depth of his tired gaze. You...you can free me,\" he raspes, his voice hoarse from disuse. \"I beg you, grant me this freedom. Look at me, bound by the cruelty of these chains. They leech my power, my essence.\" \n\n\rHis eyes, a mirror to his tormented soul, flash with a haunting light as he glances down at the chains. \"Help me, and I will help you. It is a trade, a pact, an oath. I've been trapped here for centuries, my power bound, my voice unheard. Release me from this torment, adventurer.\" he pleads.",
    "$.eventos[134].texto_resultados_possiveis": "",
    "$.eventos[134].condicoes": {
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
      "allowAtAllLevels": 0,
      "minLevel": 3,
      "terrainTypesAllowedAtAnyTime": [],
      "KeepInDeckWhenUsed": 0,
      "isLesserEvent": 0,
      "LeadsToFortune": 1
    },
    "$.eventos[134].campos_originais.targetType": 0,
    "$.eventos[134].campos_originais.characterPool": 0,
    "$.eventos[134].campos_originais.RefEventStatuses": [],
    "$.eventos[134].opcoes[0].titulo": "Break",
    "$.eventos[134].opcoes[0].texto": "Release the prisoner from the first chain",
    "$.eventos[134].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[134].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[134].opcoes[0].efeitos.__quantidade__": 1,
    "$.eventos[134].opcoes[0].efeitos[0].texto": "Under the prisoner's guidance, you step forward, bracing yourself as you reach for the chain of molten flame. The heat sears into your flesh, the fire's magic sinking deep into your core, but you persist, and the chain evaporates into smoke.",
    "$.eventos[134].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[134].opcoes[0].efeitos[0].limite_rolagem": 0,
    "$.eventos[134].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[134].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": "resources.assets:2545740",
      "nome": "The Mad Mage 2",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2545740
      },
      "tipo": "PartyEvent"
    },
    "$.eventos[134].opcoes[0].efeitos[0].batalha.iniciar": false,
    "$.eventos[134].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[134].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[134].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[134].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[134].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": -10.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[134].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[134].opcoes[0].efeitos[0].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545481",
            "nome": "Touch of Flame",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545481
            },
            "tipo": "EventStatus",
            "descricao": "Increases @Fire Damage@ by GetFlatDamageValue().",
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
                  "chave": "resources.assets:2544368",
                  "nome": "DamageFlatFire",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544368
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "ActionStatus.GetFlatDamageValue",
                "segunda_passagem": false
              }
            ]
          },
          {
            "chave": "resources.assets:2545499",
            "nome": "Severely Burned",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545499
            },
            "tipo": "EventStatus",
            "descricao": "Reduces @Fire Resistance@ by @25%@ per stack.",
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
                  "chave": "resources.assets:2544498",
                  "nome": "ResistFire",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544498
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
      },
      "skills": []
    },
    "$.eventos[134].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[134].opcoes[1].titulo": "Leave",
    "$.eventos[134].opcoes[1].texto": "You think it's too dangerous to free him.",
    "$.eventos[134].opcoes[1].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[134].opcoes[1].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[134].opcoes[1].efeitos.__quantidade__": 1,
    "$.eventos[134].opcoes[1].efeitos[0].texto": "You leave wondering what crimes required such powerful bonds.",
    "$.eventos[134].opcoes[1].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[134].opcoes[1].efeitos[0].limite_rolagem": 0,
    "$.eventos[134].opcoes[1].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[134].opcoes[1].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[134].opcoes[1].efeitos[0].batalha.iniciar": false,
    "$.eventos[134].opcoes[1].efeitos[0].batalha.manual": false,
    "$.eventos[134].opcoes[1].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[134].opcoes[1].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[134].opcoes[1].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[134].opcoes[1].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[134].opcoes[1].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[134].opcoes[1].efeitos[0].efeitos[0].recompensas": {
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
    "$.eventos[134].opcoes[1].efeitos[0].efeitos[0].remocoes_status": []
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[134].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[134].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[134].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[134].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[134].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[134].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[134].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[134].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[134].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[134].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[134].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[134].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[134].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[134].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[134].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[134].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": []
}
```

## EV-135 — The Most Dangerous Game

Veredito: MANTER. Natureza da análise: CORREÇÃO DA PROPOSTA.

Os 884 caracteres apresentam Sully Walker como caçadora, mosquete e troféu Pig Butcher. Recount compara a história do Green Dragon (Success 15) com a da raposa ridicularizada (Failure 0). Há narrativa e respostas suficientes para a escolha; manter sem especular conteúdo runtime. O deslize mutteres numa resposta é reconhecido; MANTER não equivale a texto ortograficamente perfeito.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
A robust figure stands by a fireplace, the orange light dancing in her eyes. With a musket resting in her hands and a bear skin rug beneath her boots, she exudes a commanding presence. The sight of the horrifying trophy hanging above the fireplace sends a shiver down your spine - the severed head of the dreaded Pig Butcher. <gold><incr><b>Sully Walker, the master hunter</b></incr></gold>, greets you.

"Quite a sight, isn't it?" she booms, her eyes not leaving you as she gestures to the monstrous head. "Nothing puts the fear of the wilderness into a man quite like the face of his nightmares, eh?"

You clear your throat, nodding in agreement. The grotesque visage of the Pig Butcher is indeed a horrifying sight to behold.

"And what about you, wanderer?" Sully asks, her voice dropping to a conspiratorial whisper. "What's the most dangerous game you've ever hunted down?"

```

Não há sugestão de alteração do texto original para este evento.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 135,
  "chave": "resources.assets:2545742",
  "id": "764378be-fa1c-43ef-b0e1-6669614105d4",
  "titulo": "The Most Dangerous Game",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 0,
  "classificacao_editorial": "produção",
  "veredito": "MANTER",
  "justificativa": "Os 884 caracteres apresentam Sully Walker como caçadora, mosquete e troféu Pig Butcher. Recount compara a história do Green Dragon (Success 15) com a da raposa ridicularizada (Failure 0). Há narrativa e respostas suficientes para a escolha; manter sem especular conteúdo runtime. O deslize mutteres numa resposta é reconhecido; MANTER não equivale a texto ortograficamente perfeito.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[135].chave": "resources.assets:2545742",
    "$.eventos[135].id": "764378be-fa1c-43ef-b0e1-6669614105d4",
    "$.eventos[135].titulo": "The Most Dangerous Game",
    "$.eventos[135].nome_asset": "The Most Dangerous Game",
    "$.eventos[135].categoria": "Normal",
    "$.eventos[135].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[135].peso": 1.0,
    "$.eventos[135].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[135].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[135].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[135].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[135].texto": "A robust figure stands by a fireplace, the orange light dancing in her eyes. With a musket resting in her hands and a bear skin rug beneath her boots, she exudes a commanding presence. The sight of the horrifying trophy hanging above the fireplace sends a shiver down your spine - the severed head of the dreaded Pig Butcher.\r <gold><incr><b>Sully Walker, the master hunter</b></incr></gold>, greets you.\n\r\n\"Quite a sight, isn't it?\" she booms, her eyes not leaving you as she gestures to the monstrous head. \"Nothing puts the fear of the wilderness into a man quite like the face of his nightmares, eh?\"\r\n\r\nYou clear your throat, nodding in agreement. The grotesque visage of the Pig Butcher is indeed a horrifying sight to behold.\n\n\"And what about you, wanderer?\" Sully asks, her voice dropping to a conspiratorial whisper. \"What's the most dangerous game you've ever hunted down?\"\n",
    "$.eventos[135].texto_resultados_possiveis": "",
    "$.eventos[135].condicoes": {
      "disabled": 0,
      "EditorOnly": 0,
      "allowOnAllNodeTypes": 0,
      "allowedNodeTypes": [
        7
      ],
      "requiredStatusesToSpawn": [],
      "allowOnAllTerrainTypes": 0,
      "allowedTerrainTypes": [
        2,
        1
      ],
      "allowAtAllTimesOfDay": 1,
      "allowedTimeOfDay": 0,
      "allowAtAllLevels": 1,
      "minLevel": 1,
      "terrainTypesAllowedAtAnyTime": [],
      "KeepInDeckWhenUsed": 0,
      "isLesserEvent": 0,
      "LeadsToFortune": 0
    },
    "$.eventos[135].campos_originais.targetType": 0,
    "$.eventos[135].campos_originais.characterPool": 0,
    "$.eventos[135].campos_originais.RefEventStatuses": [],
    "$.eventos[135].opcoes[0].titulo": "Recount",
    "$.eventos[135].opcoes[0].texto": "Tell the tale of the most dangerous game you've felled.",
    "$.eventos[135].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[135].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[135].opcoes[0].efeitos.__quantidade__": 2,
    "$.eventos[135].opcoes[0].efeitos[0].texto": "\"I once tracked a Green Dragon,\" you begin, your voice steady, \"A beast so fierce it could summon lightning from a clear sky, and so swift it could outrun the wind itself.\"\n\n\nYou spin a tale with precision, describing the creature's terrifying speed and its deadly electric attacks. You detail your strategy, the patience required to exploit the brief window of opportunity when the beast is momentarily weakened after an attack. The dramatic climax of your story is the final blow, a desperate strike at the dragon's heart, a leap of faith that could have easily been your last.\n\n\"By the gods,\" Sully mutteres, her eyes bright with respect, \"You've got the heart of a lion, adventurer. I'll wager that dragon didn't know what hit it.\"",
    "$.eventos[135].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[135].opcoes[0].efeitos[0].limite_rolagem": 15,
    "$.eventos[135].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[135].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[135].opcoes[0].efeitos[0].batalha.iniciar": false,
    "$.eventos[135].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[135].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[135].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[135].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[135].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[135].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[135].opcoes[0].efeitos[0].efeitos[0].recompensas": {
      "ouro": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      },
      "experiencia": {
        "dar": true,
        "razao": 3.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
      },
      "itens": {
        "dar": false,
        "pool_tipo": {
          "valor": 1,
          "nome": "Global"
        },
        "quantidade_configurada": 1,
        "tabelas": [],
        "restricoes": {
          "limitItemTypes": 0,
          "possibleItemTypes": [],
          "limitItemRarities": 1,
          "possibleRarities": [
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
    "$.eventos[135].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[135].opcoes[0].efeitos[1].texto": "Seeing an opportunity to impress, you draw yourself up to your full height. You embark on a tale of a wild fox you had slain, describing the fierce battle in vivid detail, the fear and exhilaration you had felt, the triumphant moment when you'd struck the killing blow.\n\n\nSully listens attentively, her expression impassive. When you finish, she laughs, a rich, hearty sound that echoes through the room. \"Oh, child,\" she says, shaking her head, \"I've seen more danger in a housecat.\"",
    "$.eventos[135].opcoes[0].efeitos[1].resultado": {
      "valor": 1,
      "nome": "Failure"
    },
    "$.eventos[135].opcoes[0].efeitos[1].limite_rolagem": 0,
    "$.eventos[135].opcoes[0].efeitos[1].texto_efeitos_manual": [],
    "$.eventos[135].opcoes[0].efeitos[1].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[135].opcoes[0].efeitos[1].batalha.iniciar": false,
    "$.eventos[135].opcoes[0].efeitos[1].batalha.manual": false,
    "$.eventos[135].opcoes[0].efeitos[1].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[135].opcoes[0].efeitos[1].batalha.dados_recompensa_final": null,
    "$.eventos[135].opcoes[0].efeitos[1].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[135].opcoes[0].efeitos[1].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[135].opcoes[0].efeitos[1].efeitos[0].alvo": {
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
    "$.eventos[135].opcoes[0].efeitos[1].efeitos[0].recompensas": {
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
    "$.eventos[135].opcoes[0].efeitos[1].efeitos[0].remocoes_status": []
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[135].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[135].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[135].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[135].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[135].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[135].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[135].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[135].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[135].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[135].opcoes[0].efeitos[1].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[135].opcoes[0].efeitos[1].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[135].opcoes[0].efeitos[1].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[135].opcoes[0].efeitos[1].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[135].opcoes[0].efeitos[1].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[135].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[135].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[135].opcoes[0].efeitos[1].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[135].opcoes[0].efeitos[1].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": []
}
```

## EV-136 — The Old Well

Veredito: MANTER. Natureza da análise: CORREÇÃO DA PROPOSTA.

Os 492 caracteres descrevem o poço abandonado, corda gasta e brilho ao fundo. Climb tem rolagem misteriosa, Success 8 e Failure 1; a falha concede Bruised. Preservar [name]/[his]/[he] e o risco configurado. A lista allowedTerrainTypes tem seis entradas e cinco valores distintos, mas allowOnAllTerrainTypes=1: não propor conserto de disponibilidade pela duplicação isolada.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
You stumble upon an aged well, long abandoned by any surrounding civilization. Its stones, covered in dirt and weathered by time, whisper tales of bygone days.

Curiosity draws you to the edge of the well, where you find a rusted crank and frayed rope. Tentatively, you lean over, peering into the abyss. The well is deep, and the blackness within is a consuming void, its depth unknown and unnerving. Yet, something glitters within the shadows, a tantalizing spark amidst the inky blackness.
```

Não há sugestão de alteração do texto original para este evento.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 136,
  "chave": "resources.assets:2545743",
  "id": "930f331a-b7fc-49d6-9e7a-1022733e2fca",
  "titulo": "The Old Well",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 0,
  "classificacao_editorial": "produção",
  "veredito": "MANTER",
  "justificativa": "Os 492 caracteres descrevem o poço abandonado, corda gasta e brilho ao fundo. Climb tem rolagem misteriosa, Success 8 e Failure 1; a falha concede Bruised. Preservar [name]/[his]/[he] e o risco configurado. A lista allowedTerrainTypes tem seis entradas e cinco valores distintos, mas allowOnAllTerrainTypes=1: não propor conserto de disponibilidade pela duplicação isolada.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[136].chave": "resources.assets:2545743",
    "$.eventos[136].id": "930f331a-b7fc-49d6-9e7a-1022733e2fca",
    "$.eventos[136].titulo": "The Old Well",
    "$.eventos[136].nome_asset": "The Old Well",
    "$.eventos[136].categoria": "Normal",
    "$.eventos[136].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[136].peso": 1.0,
    "$.eventos[136].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[136].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[136].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[136].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[136].texto": "You stumble upon an aged well, long abandoned by any surrounding civilization. Its stones, covered in dirt and weathered by time, whisper tales of bygone days.\n\nCuriosity draws you to the edge of the well, where you find a rusted crank and frayed rope. Tentatively, you lean over, peering into the abyss. The well is deep, and the blackness within is a consuming void, its depth unknown and unnerving. Yet, something glitters within the shadows, a tantalizing spark amidst the inky blackness.",
    "$.eventos[136].texto_resultados_possiveis": "",
    "$.eventos[136].condicoes": {
      "disabled": 0,
      "EditorOnly": 0,
      "allowOnAllNodeTypes": 0,
      "allowedNodeTypes": [
        7
      ],
      "requiredStatusesToSpawn": [],
      "allowOnAllTerrainTypes": 1,
      "allowedTerrainTypes": [
        2,
        0,
        1,
        4,
        5,
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
    },
    "$.eventos[136].campos_originais.targetType": 2,
    "$.eventos[136].campos_originais.characterPool": 0,
    "$.eventos[136].campos_originais.RefEventStatuses": [],
    "$.eventos[136].opcoes[0].titulo": "Climb",
    "$.eventos[136].opcoes[0].texto": "Carefully climb down the well.",
    "$.eventos[136].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[136].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": true,
      "texto_misterioso": ""
    },
    "$.eventos[136].opcoes[0].efeitos.__quantidade__": 2,
    "$.eventos[136].opcoes[0].efeitos[0].texto": "As [name] climbs down, each stone under [his] gloved hands felt like an echo of forgotten stories. The ancient stones, damp with the well's moisture, offered slippery resistance. Yet [he] continues down, steady and slow, [his] focus only on the promise of the shining object below.\n\n\nThere, half-buried in the silt and rock of the well's bottom, lay the source of the glimmer.",
    "$.eventos[136].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[136].opcoes[0].efeitos[0].limite_rolagem": 8,
    "$.eventos[136].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[136].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[136].opcoes[0].efeitos[0].batalha.iniciar": false,
    "$.eventos[136].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[136].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[136].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[136].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[136].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[136].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[136].opcoes[0].efeitos[0].efeitos[0].recompensas": {
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
          "valor": 1,
          "nome": "Global"
        },
        "quantidade_configurada": 1,
        "tabelas": [],
        "restricoes": {
          "limitItemTypes": 0,
          "possibleItemTypes": [],
          "limitItemRarities": 1,
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
    "$.eventos[136].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[136].opcoes[0].efeitos[1].texto": "The wet stones betray [name]. [His] foot slips. A startled cry echoes upwards as [he] loses [his] grip, tumbling down into the darkness. [His] descent is halted abruptly as [he] slams into the bottom of the well, knocking the wind from [his] lungs. ",
    "$.eventos[136].opcoes[0].efeitos[1].resultado": {
      "valor": 1,
      "nome": "Failure"
    },
    "$.eventos[136].opcoes[0].efeitos[1].limite_rolagem": 1,
    "$.eventos[136].opcoes[0].efeitos[1].texto_efeitos_manual": [],
    "$.eventos[136].opcoes[0].efeitos[1].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[136].opcoes[0].efeitos[1].batalha.iniciar": false,
    "$.eventos[136].opcoes[0].efeitos[1].batalha.manual": false,
    "$.eventos[136].opcoes[0].efeitos[1].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[136].opcoes[0].efeitos[1].batalha.dados_recompensa_final": null,
    "$.eventos[136].opcoes[0].efeitos[1].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[136].opcoes[0].efeitos[1].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[136].opcoes[0].efeitos[1].efeitos[0].alvo": {
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
    "$.eventos[136].opcoes[0].efeitos[1].efeitos[0].recompensas": {
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
      },
      "skills": []
    },
    "$.eventos[136].opcoes[0].efeitos[1].efeitos[0].remocoes_status": [],
    "$.eventos[136].opcoes[1].titulo": "Leave",
    "$.eventos[136].opcoes[1].texto": "Your foothold feels too tentative to continue.",
    "$.eventos[136].opcoes[1].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[136].opcoes[1].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[136].opcoes[1].efeitos.__quantidade__": 0
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[136].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[136].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[136].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[136].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[136].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[136].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[136].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[136].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[136].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[136].opcoes[0].efeitos[1].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[136].opcoes[0].efeitos[1].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[136].opcoes[0].efeitos[1].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[136].opcoes[0].efeitos[1].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[136].opcoes[0].efeitos[1].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[136].opcoes[0].efeitos[1].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[136].opcoes[0].efeitos[1].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[136].opcoes[0].efeitos[1].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[136].opcoes[0].efeitos[1].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": []
}
```

## EV-137 — The Oracle

Veredito: MELHORAR. Natureza da análise: CORREÇÃO DA PROPOSTA.

Narrativa existente sobre inimigos próximos/distantes. Corrigir omissão de you na oferta e de of na ação Far, mantendo Evasive Movement/Ranged Precision e todos os campos de alvo. A resposta menciona Party, mas o efeito serializado mostra Self sem override: não afirmar alvo final do grupo. disabled=1 e todos os valores de condições permanecem.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
"Come quick! Your enemies combine against you."

An oracle beckons you to look into the future. You see flashes of many battles.

"I can help escape those that are already close, or see those coming from afar."
```

Sugestão não implementada: os blocos alteracoes abaixo contêm campo existente, campo serializado equivalente, antes literal e depois exato. Não há alteração de valores mecânicos, condições ou referências.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 137,
  "chave": "resources.assets:2545744",
  "id": "e100bc75-b20c-4d3f-a3e1-94e22584cf17",
  "titulo": "The Oracle",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 1,
  "classificacao_editorial": "produção",
  "veredito": "MELHORAR",
  "justificativa": "Narrativa existente sobre inimigos próximos/distantes. Corrigir omissão de you na oferta e de of na ação Far, mantendo Evasive Movement/Ranged Precision e todos os campos de alvo. A resposta menciona Party, mas o efeito serializado mostra Self sem override: não afirmar alvo final do grupo. disabled=1 e todos os valores de condições permanecem.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[137].chave": "resources.assets:2545744",
    "$.eventos[137].id": "e100bc75-b20c-4d3f-a3e1-94e22584cf17",
    "$.eventos[137].titulo": "The Oracle",
    "$.eventos[137].nome_asset": "The Oracle",
    "$.eventos[137].categoria": "Normal",
    "$.eventos[137].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[137].peso": 1.0,
    "$.eventos[137].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[137].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[137].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[137].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[137].texto": "\"Come quick! Your enemies combine against you.\"\n\nAn oracle beckons you to look into the future. You see flashes of many battles.\n\n\"I can help escape those that are already close, or see those coming from afar.\"",
    "$.eventos[137].texto_resultados_possiveis": "",
    "$.eventos[137].condicoes": {
      "disabled": 1,
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
      "allowAtAllLevels": 1,
      "minLevel": 1,
      "terrainTypesAllowedAtAnyTime": [
        4,
        3
      ],
      "KeepInDeckWhenUsed": 0,
      "isLesserEvent": 0,
      "LeadsToFortune": 0
    },
    "$.eventos[137].campos_originais.targetType": 0,
    "$.eventos[137].campos_originais.characterPool": 0,
    "$.eventos[137].campos_originais.RefEventStatuses": [],
    "$.eventos[137].opcoes[0].titulo": "Close",
    "$.eventos[137].opcoes[0].texto": "\"Help me escape from those closing in\". Gain [o1a1_status].",
    "$.eventos[137].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[137].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[137].opcoes[0].efeitos.__quantidade__": 1,
    "$.eventos[137].opcoes[0].efeitos[0].texto": "She snaps her fingers and you feel a new awareness come into your mind. You feel acutely aware of any object living or dead that could hold you fast.\n\nParty gains [o1a1_status].",
    "$.eventos[137].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[137].opcoes[0].efeitos[0].limite_rolagem": 0,
    "$.eventos[137].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[137].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[137].opcoes[0].efeitos[0].batalha.iniciar": false,
    "$.eventos[137].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[137].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[137].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[137].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[137].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[137].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[137].opcoes[0].efeitos[0].efeitos[0].recompensas": {
      "ouro": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      },
      "experiencia": {
        "dar": false,
        "razao": 3.0,
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
            "chave": "resources.assets:2545384",
            "nome": "Evasive Movement",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545384
            },
            "tipo": "EventStatus",
            "descricao": "Grants immunity to opportunity attacks.",
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
                  "chave": "resources.assets:2544547",
                  "nome": "OpportunityAttackImmunity",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544547
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 4,
                  "nome": "Set"
                },
                "expressao": "1",
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
    "$.eventos[137].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[137].opcoes[1].titulo": "Far",
    "$.eventos[137].opcoes[1].texto": "\"Help me see those coming from afar\". Gain [o2a1_status].",
    "$.eventos[137].opcoes[1].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[137].opcoes[1].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[137].opcoes[1].efeitos.__quantidade__": 1,
    "$.eventos[137].opcoes[1].efeitos[0].texto": "She snaps her fingers and you feel a new awareness come into your mind. You feel acutely aware any threat even beyond the range of your vision.\n\nParty gains [o2a1_status].",
    "$.eventos[137].opcoes[1].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[137].opcoes[1].efeitos[0].limite_rolagem": 0,
    "$.eventos[137].opcoes[1].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[137].opcoes[1].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[137].opcoes[1].efeitos[0].batalha.iniciar": false,
    "$.eventos[137].opcoes[1].efeitos[0].batalha.manual": false,
    "$.eventos[137].opcoes[1].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[137].opcoes[1].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[137].opcoes[1].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[137].opcoes[1].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[137].opcoes[1].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[137].opcoes[1].efeitos[0].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545393",
            "nome": "Ranged Precision",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545393
            },
            "tipo": "EventStatus",
            "descricao": "Every hex between you and your target increases damage dealt by an additional 1%.",
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
                "expressao": "1",
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
    "$.eventos[137].opcoes[1].efeitos[0].efeitos[0].remocoes_status": []
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[137].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[137].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[137].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[137].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[137].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[137].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[137].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[137].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[137].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[137].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[137].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[137].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[137].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[137].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[137].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[137].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[137].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[137].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL",
      "idioma": "inglês",
      "campo": "$.eventos[137].texto",
      "campo_original": "$.eventos[137].campos_originais.encounterText",
      "antes": "\"Come quick! Your enemies combine against you.\"\n\nAn oracle beckons you to look into the future. You see flashes of many battles.\n\n\"I can help escape those that are already close, or see those coming from afar.\"",
      "depois": "\"Come quick! Your enemies combine against you.\"\n\nAn oracle beckons you to look into the future. You see flashes of many battles.\n\n\"I can help you escape those that are already close, or see those coming from afar.\"",
      "motivo": "Corrigir objeto ausente no inglês sem alterar a oferta de ajuda.",
      "implementado": false
    },
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL",
      "idioma": "inglês",
      "campo": "$.eventos[137].opcoes[1].efeitos[0].texto",
      "campo_original": "$.eventos[137].opcoes[1].efeitos[0].campos_originais.activationText",
      "antes": "She snaps her fingers and you feel a new awareness come into your mind. You feel acutely aware any threat even beyond the range of your vision.\n\nParty gains [o2a1_status].",
      "depois": "She snaps her fingers and you feel a new awareness come into your mind. You feel acutely aware of any threat even beyond the range of your vision.\n\nParty gains [o2a1_status].",
      "motivo": "Corrigir preposição; manter literalmente Party gains [o2a1_status].",
      "implementado": false
    }
  ]
}
```

## EV-138 — The Pale Knight

Veredito: MELHORAR. Natureza da análise: CORREÇÃO DA PROPOSTA.

Rare (2), disabled=1: narrativa de baú amaldiçoado e ossos, não cavaleiro descrito. Open configura batalha. Inserir vírgula na resposta existente e dar descrição à opção Leave realmente vazia; isso não é preenchimento de falsa narrativa vazia nem criação de cavaleiro ou nova recompensa. Manter raridade, título e condições.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
Bones litter the ground surrounding this Cursed Chest. Its infernal construction is held together by rotting wood and the spine of some poor creature.
```

Sugestão não implementada: os blocos alteracoes abaixo contêm campo existente, campo serializado equivalente, antes literal e depois exato. Não há alteração de valores mecânicos, condições ou referências.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 138,
  "chave": "resources.assets:2545745",
  "id": "f08738de-ec30-4dd2-b947-2774494301e6",
  "titulo": "The Pale Knight",
  "categoria": "Normal",
  "raridade": {
    "valor": 2,
    "nome": "Rare"
  },
  "peso": 1.0,
  "disabled": 1,
  "classificacao_editorial": "produção",
  "veredito": "MELHORAR",
  "justificativa": "Rare (2), disabled=1: narrativa de baú amaldiçoado e ossos, não cavaleiro descrito. Open configura batalha. Inserir vírgula na resposta existente e dar descrição à opção Leave realmente vazia; isso não é preenchimento de falsa narrativa vazia nem criação de cavaleiro ou nova recompensa. Manter raridade, título e condições.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[138].chave": "resources.assets:2545745",
    "$.eventos[138].id": "f08738de-ec30-4dd2-b947-2774494301e6",
    "$.eventos[138].titulo": "The Pale Knight",
    "$.eventos[138].nome_asset": "The Pale Knight",
    "$.eventos[138].categoria": "Normal",
    "$.eventos[138].raridade": {
      "valor": 2,
      "nome": "Rare"
    },
    "$.eventos[138].peso": 1.0,
    "$.eventos[138].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[138].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[138].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[138].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[138].texto": "Bones litter the ground surrounding this Cursed Chest. Its infernal construction is held together by rotting wood and the spine of some poor creature.",
    "$.eventos[138].texto_resultados_possiveis": "",
    "$.eventos[138].condicoes": {
      "disabled": 1,
      "EditorOnly": 0,
      "allowOnAllNodeTypes": 0,
      "allowedNodeTypes": [
        7
      ],
      "requiredStatusesToSpawn": [],
      "allowOnAllTerrainTypes": 1,
      "allowedTerrainTypes": [],
      "allowAtAllTimesOfDay": 0,
      "allowedTimeOfDay": 1,
      "allowAtAllLevels": 1,
      "minLevel": 1,
      "terrainTypesAllowedAtAnyTime": [
        4,
        0,
        3,
        5
      ],
      "KeepInDeckWhenUsed": 0,
      "isLesserEvent": 0,
      "LeadsToFortune": 0
    },
    "$.eventos[138].campos_originais.targetType": 0,
    "$.eventos[138].campos_originais.characterPool": 0,
    "$.eventos[138].campos_originais.RefEventStatuses": [],
    "$.eventos[138].opcoes[0].titulo": "Open",
    "$.eventos[138].opcoes[0].texto": "Open the chest and deal with the consequences.",
    "$.eventos[138].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[138].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[138].opcoes[0].efeitos.__quantidade__": 1,
    "$.eventos[138].opcoes[0].efeitos[0].texto": "The Cursed Chest creaks open releasing a noxious fog. All around you the decaying hands of the undead reach through the earth...",
    "$.eventos[138].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[138].opcoes[0].efeitos[0].limite_rolagem": 0,
    "$.eventos[138].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[138].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[138].opcoes[0].efeitos[0].batalha.iniciar": true,
    "$.eventos[138].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[138].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": "resources.assets:2544645",
      "nome": "Cursed Chest Battle",
      "pptr": {
        "m_FileID": 0,
        "m_PathID": 2544645
      },
      "tipo": "BattleInfo"
    },
    "$.eventos[138].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[138].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[138].opcoes[0].efeitos[0].batalha.override": {
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
    "$.eventos[138].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[138].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[138].opcoes[0].efeitos[0].efeitos[0].recompensas": {
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
    "$.eventos[138].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[138].opcoes[1].titulo": "Leave",
    "$.eventos[138].opcoes[1].texto": "",
    "$.eventos[138].opcoes[1].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[138].opcoes[1].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[138].opcoes[1].efeitos.__quantidade__": 0
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[138].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[138].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[138].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[138].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[138].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[138].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[138].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL",
      "idioma": "inglês",
      "campo": "$.eventos[138].opcoes[0].efeitos[0].texto",
      "campo_original": "$.eventos[138].opcoes[0].efeitos[0].campos_originais.activationText",
      "antes": "The Cursed Chest creaks open releasing a noxious fog. All around you the decaying hands of the undead reach through the earth...",
      "depois": "The Cursed Chest creaks open, releasing a noxious fog. All around you the decaying hands of the undead reach through the earth...",
      "motivo": "Pontuação da resposta que já descreve névoa e mortos-vivos.",
      "implementado": false
    },
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL",
      "idioma": "inglês",
      "campo": "$.eventos[138].opcoes[1].texto",
      "campo_original": "$.eventos[138].opcoes[1].campos_originais.description",
      "antes": "",
      "depois": "Leave the cursed chest unopened.",
      "motivo": "A descrição da opção Leave é realmente vazia; explicitar a ação já indicada pelo título, sem adicionar efeitos.",
      "implementado": false
    }
  ]
}
```

## EV-139 — The runes of the Ymir

Veredito: MELHORAR. Natureza da análise: CORREÇÃO DA PROPOSTA.

Monólito de gelo antigo com runas Ymir: preservar os 481 caracteres, o gelo e o urso polar descrito em Touch. Uniformizar placed para place na resposta, não substituir por pedra com musgo. Touch configura iniciar batalha; Success 0 não é prova de encontro sem risco. Não há campo referencia/nome top-level nem inferência de quest ausente.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
A monolith of ancient ice towers over you, its frosted surface etched with runes of an age long past, the forgotten language of the Ymir. Every stroke of the rune is a story, each etching an echo of a bygone era. And as your gaze traces over them, you feel an odd attraction, a pull that leads you closer, until the ancient ice is mere inches from your face. Its surface, frigid and firm, seems to smoke in the cold, sending up curls of fog that spiral towards the stark white sky.
```

Sugestão não implementada: os blocos alteracoes abaixo contêm campo existente, campo serializado equivalente, antes literal e depois exato. Não há alteração de valores mecânicos, condições ou referências.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 139,
  "chave": "resources.assets:2545785",
  "id": "8e63fbe4-3e26-49fc-b9f0-8f4aa4676f67",
  "titulo": "The runes of the Ymir",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 0,
  "classificacao_editorial": "produção",
  "veredito": "MELHORAR",
  "justificativa": "Monólito de gelo antigo com runas Ymir: preservar os 481 caracteres, o gelo e o urso polar descrito em Touch. Uniformizar placed para place na resposta, não substituir por pedra com musgo. Touch configura iniciar batalha; Success 0 não é prova de encontro sem risco. Não há campo referencia/nome top-level nem inferência de quest ausente.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[139].chave": "resources.assets:2545785",
    "$.eventos[139].id": "8e63fbe4-3e26-49fc-b9f0-8f4aa4676f67",
    "$.eventos[139].titulo": "The runes of the Ymir",
    "$.eventos[139].nome_asset": "Ymir Rune, Strength",
    "$.eventos[139].categoria": "Normal",
    "$.eventos[139].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[139].peso": 1.0,
    "$.eventos[139].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[139].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[139].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[139].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[139].texto": "A monolith of ancient ice towers over you, its frosted surface etched with runes of an age long past, the forgotten language of the Ymir. Every stroke of the rune is a story, each etching an echo of a bygone era. And as your gaze traces over them, you feel an odd attraction, a pull that leads you closer, until the ancient ice is mere inches from your face. Its surface, frigid and firm, seems to smoke in the cold, sending up curls of fog that spiral towards the stark white sky.",
    "$.eventos[139].texto_resultados_possiveis": "Will you touch the Rune?",
    "$.eventos[139].condicoes": {
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
    },
    "$.eventos[139].campos_originais.targetType": 0,
    "$.eventos[139].campos_originais.characterPool": 0,
    "$.eventos[139].campos_originais.RefEventStatuses": [],
    "$.eventos[139].opcoes[0].titulo": "Touch",
    "$.eventos[139].opcoes[0].texto": "You reach out and place the palm of your hand on the Ice.",
    "$.eventos[139].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[139].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[139].opcoes[0].efeitos.__quantidade__": 1,
    "$.eventos[139].opcoes[0].efeitos[0].texto": "You reach out, your hand trembling slightly, and placed your palm onto the ice.\n\n\nImmediately, a chill sweeps through you, not the biting sting of frostbite, but rather a soothing coolness that reaches your very core. It flows through your veins like a river of tranquility, quieting the whispers of worry that dance at the edges of your consciousness. But this fleeting moment of tranquility shatters abruptly, fragmented by a thunderous roar that echoes off the frozen surroundings.\n\nIt is a polar bear, its fur as white as the surrounding snowscape. Glowing blue runes dance over the bear's fur like the heart of an icy flame. Its roar rings out again, the sound rumbling through the ice and the snow, and meeting the echo of the ancient rune in a symphony of old magic.",
    "$.eventos[139].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[139].opcoes[0].efeitos[0].limite_rolagem": 0,
    "$.eventos[139].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[139].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[139].opcoes[0].efeitos[0].batalha.iniciar": true,
    "$.eventos[139].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[139].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[139].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[139].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[139].opcoes[0].efeitos[0].batalha.override": {
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
          "OverrideEnemyName": 1,
          "NameOverride": "Trial of Strength",
          "CharacterInfo": {
            "m_FileID": 0,
            "m_PathID": 2545282
          },
          "ForcedEnemyMods": [],
          "IsSuperUnique": 1
        },
        {
          "OverrideEnemyName": 0,
          "NameOverride": "",
          "CharacterInfo": {
            "m_FileID": 0,
            "m_PathID": 2545281
          },
          "ForcedEnemyMods": [],
          "IsSuperUnique": 0
        },
        {
          "OverrideEnemyName": 0,
          "NameOverride": "",
          "CharacterInfo": {
            "m_FileID": 0,
            "m_PathID": 2545281
          },
          "ForcedEnemyMods": [],
          "IsSuperUnique": 0
        },
        {
          "OverrideEnemyName": 0,
          "NameOverride": "",
          "CharacterInfo": {
            "m_FileID": 0,
            "m_PathID": 2545281
          },
          "ForcedEnemyMods": [],
          "IsSuperUnique": 0
        },
        {
          "OverrideEnemyName": 0,
          "NameOverride": "",
          "CharacterInfo": {
            "m_FileID": 0,
            "m_PathID": 2545281
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
      "OverrideEnemyGroupPool": 1,
      "EnemyGroupPool": [],
      "OverrideEnemyTypePool": 0,
      "EnemyTypePool": [],
      "VictoryEvent": {
        "m_FileID": 0,
        "m_PathID": 2545783
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
    "$.eventos[139].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[139].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[139].opcoes[0].efeitos[0].efeitos[0].recompensas": {
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
    "$.eventos[139].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[139].opcoes[1].titulo": "Leave",
    "$.eventos[139].opcoes[1].texto": "You have no time for these ancient markings.",
    "$.eventos[139].opcoes[1].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[139].opcoes[1].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[139].opcoes[1].efeitos.__quantidade__": 1,
    "$.eventos[139].opcoes[1].efeitos[0].texto": "",
    "$.eventos[139].opcoes[1].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[139].opcoes[1].efeitos[0].limite_rolagem": 0,
    "$.eventos[139].opcoes[1].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[139].opcoes[1].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[139].opcoes[1].efeitos[0].batalha.iniciar": false,
    "$.eventos[139].opcoes[1].efeitos[0].batalha.manual": false,
    "$.eventos[139].opcoes[1].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[139].opcoes[1].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[139].opcoes[1].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[139].opcoes[1].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[139].opcoes[1].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[139].opcoes[1].efeitos[0].efeitos[0].recompensas": {
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
    "$.eventos[139].opcoes[1].efeitos[0].efeitos[0].remocoes_status": []
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[139].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[139].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[139].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[139].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[139].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[139].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[139].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[139].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[139].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[139].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[139].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[139].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[139].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[139].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[139].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[139].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[139].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[139].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL",
      "idioma": "inglês",
      "campo": "$.eventos[139].opcoes[0].efeitos[0].texto",
      "campo_original": "$.eventos[139].opcoes[0].efeitos[0].campos_originais.activationText",
      "antes": "You reach out, your hand trembling slightly, and placed your palm onto the ice.\n\n\nImmediately, a chill sweeps through you, not the biting sting of frostbite, but rather a soothing coolness that reaches your very core. It flows through your veins like a river of tranquility, quieting the whispers of worry that dance at the edges of your consciousness. But this fleeting moment of tranquility shatters abruptly, fragmented by a thunderous roar that echoes off the frozen surroundings.\n\nIt is a polar bear, its fur as white as the surrounding snowscape. Glowing blue runes dance over the bear's fur like the heart of an icy flame. Its roar rings out again, the sound rumbling through the ice and the snow, and meeting the echo of the ancient rune in a symphony of old magic.",
      "depois": "You reach out, your hand trembling slightly, and place your palm onto the ice.\n\n\nImmediately, a chill sweeps through you, not the biting sting of frostbite, but rather a soothing coolness that reaches your very core. It flows through your veins like a river of tranquility, quieting the whispers of worry that dance at the edges of your consciousness. But this fleeting moment of tranquility shatters abruptly, fragmented by a thunderous roar that echoes off the frozen surroundings.\n\nIt is a polar bear, its fur as white as the surrounding snowscape. Glowing blue runes dance over the bear's fur like the heart of an icy flame. Its roar rings out again, the sound rumbling through the ice and the snow, and meeting the echo of the ancient rune in a symphony of old magic.",
      "motivo": "Uniformizar o presente usado em You reach out; conservar a chegada do urso e o combate configurado.",
      "implementado": false
    }
  ]
}
```

## EV-140 — The Soothsayer

Veredito: MELHORAR. Natureza da análise: CORREÇÃO DA PROPOSTA.

Há narrativa marcada de elfa e bola de cristal, não texto vazio. Corrigir unendying para unyielding na ação View, alinhando o termo ao texto da opção; preservar [name], [o3a1_status], Endurance e os três ramos Success 0. Não transformar esse valor em garantia observada no jogo nem reativar disabled=1.

Narrativa existente integral (inglês, não tradução nem proposta):

```text
A <color=#90ee90><b>mysterious elf</b></color> stands before a glimmering Crystal Ball.

<color=#90ee90><b>The Soothsayer:</b></color> "Welcome Watcher, I have been waiting for you."

<color=#90ee90><b>The Soothsayer:</b></color> "This Crystal Ball contains many secrets. If you look into it you will see your great victory!"

<color=#90ee90><b>The Soothsayer:</b></color> "Look into the Crystal Ball, and tell us what you see."
```

Sugestão não implementada: os blocos alteracoes abaixo contêm campo existente, campo serializado equivalente, antes literal e depois exato. Não há alteração de valores mecânicos, condições ou referências.

Fatos, NULL com motivo e propostas verificáveis:

```json evento-b07
{
  "ordinal": 140,
  "chave": "resources.assets:2545746",
  "id": "509fbfa8-efd1-4fb3-a7d0-cdca0266ae83",
  "titulo": "The Soothsayer",
  "categoria": "Normal",
  "raridade": {
    "valor": 0,
    "nome": "Common"
  },
  "peso": 1.0,
  "disabled": 1,
  "classificacao_editorial": "produção",
  "veredito": "MELHORAR",
  "justificativa": "Há narrativa marcada de elfa e bola de cristal, não texto vazio. Corrigir unendying para unyielding na ação View, alinhando o termo ao texto da opção; preservar [name], [o3a1_status], Endurance e os três ramos Success 0. Não transformar esse valor em garantia observada no jogo nem reativar disabled=1.",
  "runtime": "NAO_EXERCITADO",
  "fatos": {
    "$.eventos[140].chave": "resources.assets:2545746",
    "$.eventos[140].id": "509fbfa8-efd1-4fb3-a7d0-cdca0266ae83",
    "$.eventos[140].titulo": "The Soothsayer",
    "$.eventos[140].nome_asset": "The Soothsayer",
    "$.eventos[140].categoria": "Normal",
    "$.eventos[140].raridade": {
      "valor": 0,
      "nome": "Common"
    },
    "$.eventos[140].peso": 1.0,
    "$.eventos[140].pool": [
      {
        "valor": 0,
        "nome": "Normal"
      }
    ],
    "$.eventos[140].historia": {
      "valor": 0,
      "nome": "NonStoryOnly"
    },
    "$.eventos[140].modos": [
      {
        "valor": 0,
        "nome": "Campaign"
      },
      {
        "valor": 1,
        "nome": "Roguelike"
      }
    ],
    "$.eventos[140].full_release": {
      "valor": 0,
      "nome": "None"
    },
    "$.eventos[140].texto": "A <color=#90ee90><b>mysterious elf</b></color> stands before a glimmering Crystal Ball.\n\n<color=#90ee90><b>The Soothsayer:</b></color> \"Welcome Watcher, I have been waiting for you.\"\n\n<color=#90ee90><b>The Soothsayer:</b></color> \"This Crystal Ball contains many secrets. If you look into it you will see your great victory!\"\n\n<color=#90ee90><b>The Soothsayer:</b></color> \"Look into the Crystal Ball, and tell us what you see.\"",
    "$.eventos[140].texto_resultados_possiveis": "",
    "$.eventos[140].condicoes": {
      "disabled": 1,
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
      "allowAtAllLevels": 1,
      "minLevel": 1,
      "terrainTypesAllowedAtAnyTime": [
        4,
        3
      ],
      "KeepInDeckWhenUsed": 0,
      "isLesserEvent": 0,
      "LeadsToFortune": 1
    },
    "$.eventos[140].campos_originais.targetType": 2,
    "$.eventos[140].campos_originais.characterPool": 0,
    "$.eventos[140].campos_originais.RefEventStatuses": [],
    "$.eventos[140].opcoes[0].titulo": "See",
    "$.eventos[140].opcoes[0].texto": "\"I see my enemies... battered and broken!\". Gain [o1a1_status].",
    "$.eventos[140].opcoes[0].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[140].opcoes[0].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[140].opcoes[0].efeitos.__quantidade__": 1,
    "$.eventos[140].opcoes[0].efeitos[0].texto": "[name] sees enemies... broken and battered. [name] gains [o1a1_status].",
    "$.eventos[140].opcoes[0].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[140].opcoes[0].efeitos[0].limite_rolagem": 0,
    "$.eventos[140].opcoes[0].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[140].opcoes[0].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[140].opcoes[0].efeitos[0].batalha.iniciar": false,
    "$.eventos[140].opcoes[0].efeitos[0].batalha.manual": false,
    "$.eventos[140].opcoes[0].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[140].opcoes[0].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[140].opcoes[0].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[140].opcoes[0].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[140].opcoes[0].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[140].opcoes[0].efeitos[0].efeitos[0].recompensas": {
      "ouro": {
        "dar": false,
        "retirar": false,
        "razao": 1.0,
        "quantidade_final": null,
        "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
      },
      "experiencia": {
        "dar": false,
        "razao": 3.0,
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
            "chave": "resources.assets:2545452",
            "nome": "Martial Prowess",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545452
            },
            "tipo": "EventStatus",
            "descricao": "Increases @Physical Damage@ by {5,20}%.",
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
                "expressao": "{5,20}",
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
    "$.eventos[140].opcoes[0].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[140].opcoes[1].titulo": "Witness",
    "$.eventos[140].opcoes[1].texto": "\"I see the elements... combined to empower me!\" Gain [o2a1_status].",
    "$.eventos[140].opcoes[1].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[140].opcoes[1].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[140].opcoes[1].efeitos.__quantidade__": 1,
    "$.eventos[140].opcoes[1].efeitos[0].texto": "[name] sees the elements combined to empower. [name] gains [o2a1_status].",
    "$.eventos[140].opcoes[1].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[140].opcoes[1].efeitos[0].limite_rolagem": 0,
    "$.eventos[140].opcoes[1].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[140].opcoes[1].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[140].opcoes[1].efeitos[0].batalha.iniciar": false,
    "$.eventos[140].opcoes[1].efeitos[0].batalha.manual": false,
    "$.eventos[140].opcoes[1].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[140].opcoes[1].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[140].opcoes[1].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[140].opcoes[1].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[140].opcoes[1].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[140].opcoes[1].efeitos[0].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545431",
            "nome": "Elemental Power",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545431
            },
            "tipo": "EventStatus",
            "descricao": "Increases @Elemental Damage@ by {5,25}%.",
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
                  "chave": "resources.assets:2544375",
                  "nome": "DamageModCold",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544375
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{5,25}",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544377",
                  "nome": "DamageModFire",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544377
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{5,25}",
                "segunda_passagem": false
              },
              {
                "atributo": {
                  "chave": "resources.assets:2544379",
                  "nome": "DamageModLightning",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544379
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{5,25}",
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
    "$.eventos[140].opcoes[1].efeitos[0].efeitos[0].remocoes_status": [],
    "$.eventos[140].opcoes[2].titulo": "View",
    "$.eventos[140].opcoes[2].texto": "\"I see my own endurance unyielding!\" Gain [o3a1_status].",
    "$.eventos[140].opcoes[2].condicoes": {
      "status_requeridos": [],
      "ocultar_sem_requisitos": false,
      "ocultar_se_status": []
    },
    "$.eventos[140].opcoes[2].rolagem": {
      "bonus": [],
      "misteriosa": false,
      "texto_misterioso": ""
    },
    "$.eventos[140].opcoes[2].efeitos.__quantidade__": 1,
    "$.eventos[140].opcoes[2].efeitos[0].texto": "[name] sees endurance unendying. [name] gains [o3a1_status].",
    "$.eventos[140].opcoes[2].efeitos[0].resultado": {
      "valor": 0,
      "nome": "Success"
    },
    "$.eventos[140].opcoes[2].efeitos[0].limite_rolagem": 0,
    "$.eventos[140].opcoes[2].efeitos[0].texto_efeitos_manual": [],
    "$.eventos[140].opcoes[2].efeitos[0].evento_encadeado": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[140].opcoes[2].efeitos[0].batalha.iniciar": false,
    "$.eventos[140].opcoes[2].efeitos[0].batalha.manual": false,
    "$.eventos[140].opcoes[2].efeitos[0].batalha.referencia": {
      "chave": null,
      "nome": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    "$.eventos[140].opcoes[2].efeitos[0].batalha.dados_recompensa_final": null,
    "$.eventos[140].opcoes[2].efeitos[0].batalha.motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado.",
    "$.eventos[140].opcoes[2].efeitos[0].efeitos[0].vida_mana": {
      "percentMaxHealth": 0.0,
      "percentMaxMana": 0.0,
      "percentCurHealth": 0.0,
      "percentCurMana": 0.0
    },
    "$.eventos[140].opcoes[2].efeitos[0].efeitos[0].alvo": {
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
    "$.eventos[140].opcoes[2].efeitos[0].efeitos[0].recompensas": {
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
            "chave": "resources.assets:2545438",
            "nome": "Endurance",
            "pptr": {
              "m_FileID": 0,
              "m_PathID": 2545438
            },
            "tipo": "EventStatus",
            "descricao": "Increases @Max Health@ by {5, 500}.",
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
                  "chave": "resources.assets:2544436",
                  "nome": "MaxHealth",
                  "pptr": {
                    "m_FileID": 0,
                    "m_PathID": 2544436
                  },
                  "tipo": "CharacterAttribute"
                },
                "metodo": {
                  "valor": 0,
                  "nome": "Base"
                },
                "expressao": "{5, 500}",
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
    "$.eventos[140].opcoes[2].efeitos[0].efeitos[0].remocoes_status": []
  },
  "referencias_ou_resultados_null": [
    {
      "campo": "$.eventos[140].opcoes[0].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[140].opcoes[0].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[140].opcoes[0].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[140].opcoes[0].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[140].opcoes[0].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[140].opcoes[0].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[140].opcoes[0].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[140].opcoes[0].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[140].opcoes[0].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[140].opcoes[1].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[140].opcoes[1].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[140].opcoes[1].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[140].opcoes[1].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[140].opcoes[1].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[140].opcoes[1].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[140].opcoes[1].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[140].opcoes[1].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[140].opcoes[1].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    },
    {
      "campo": "$.eventos[140].opcoes[2].efeitos[0].evento_encadeado.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[140].opcoes[2].efeitos[0].evento_encadeado.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[140].opcoes[2].efeitos[0].batalha.referencia.chave",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[140].opcoes[2].efeitos[0].batalha.referencia.nome",
      "valor": null,
      "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."
    },
    {
      "campo": "$.eventos[140].opcoes[2].efeitos[0].batalha.dados_recompensa_final",
      "valor": null,
      "motivo": "Configuração de combate preservada; inimigos, loot/XP efetivos e modificadores são resolvidos no runtime, não exercitado."
    },
    {
      "campo": "$.eventos[140].opcoes[2].efeitos[0].efeitos[0].recompensas.ouro.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions: GetQuestGold(nível), razão e GoldMultiplier; requer estado da partida."
    },
    {
      "campo": "$.eventos[140].opcoes[2].efeitos[0].efeitos[0].recompensas.experiencia.quantidade_final",
      "valor": null,
      "motivo": "Calculada em EventOption.InitActions; pode ser convertida em ouro no roguelike/party nível 30; requer estado da partida."
    },
    {
      "campo": "$.eventos[140].opcoes[2].efeitos[0].efeitos[0].recompensas.itens.sorteio_final",
      "valor": null,
      "motivo": "EventOption.InitActions/LootTable.GetLoot dependem de nível, restrições e RNG; tabelas autorais preservadas."
    },
    {
      "campo": "$.eventos[140].opcoes[2].efeitos[0].efeitos[0].recompensas.status.resultado_sorteado",
      "valor": null,
      "motivo": "Configuração de candidatos preservada; resultado da partida não exercitado."
    }
  ],
  "alteracoes": [
    {
      "natureza": "SUGESTÃO DE ALTERAÇÃO DO TEXTO ORIGINAL",
      "idioma": "inglês",
      "campo": "$.eventos[140].opcoes[2].efeitos[0].texto",
      "campo_original": "$.eventos[140].opcoes[2].efeitos[0].campos_originais.activationText",
      "antes": "[name] sees endurance unendying. [name] gains [o3a1_status].",
      "depois": "[name] sees endurance unyielding. [name] gains [o3a1_status].",
      "motivo": "Corrigir palavra malformada para o termo já usado na opção View.",
      "implementado": false
    }
  ]
}
```

## Identidades das variantes e etapas (somente evidência, fora da cobertura de vereditos)

Cada registro listado conserva sua chave, id, título, nome_asset e categoria próprios. A presença de várias etapas/variantes não é uma acusação de GUID duplicado; as etapas Mad Mage 2/3 são eventos encadeados, não cópias a fundir. Fortune Teller (Test) é #129, não uma segunda identidade Normal de #128. Não há propostas de alteração para estas variantes externas ao lote.

```json variantes-b07
[
  {
    "grupo_editorial": "The Animator",
    "registros": [
      {
        "chave": "resources.assets:2545732",
        "id": "7d008743-08fc-4746-b4c9-2201f70b530f",
        "titulo": "The Animator",
        "nome_asset": "The Animator",
        "categoria": "Normal"
      },
      {
        "chave": "resources.assets:2545731",
        "id": "367876d3-1828-4bf5-bff6-c6b768e81012",
        "titulo": "The Animator",
        "nome_asset": "The Animator - Success",
        "categoria": "NotInEventPool"
      }
    ]
  },
  {
    "grupo_editorial": "The Fortune Teller",
    "registros": [
      {
        "chave": "resources.assets:2545734",
        "id": "2ca74161-3fe7-459d-bdd7-1b6f4741edc4",
        "titulo": "The Fortune Teller",
        "nome_asset": "The Fortune Teller",
        "categoria": "Normal"
      }
    ]
  },
  {
    "grupo_editorial": "The Mad Mage",
    "registros": [
      {
        "chave": "resources.assets:2545739",
        "id": "435d6bd4-fa60-4982-85f8-e4a0ec083837",
        "titulo": "The Mad Mage",
        "nome_asset": "The Mad Mage 1",
        "categoria": "Normal"
      },
      {
        "chave": "resources.assets:2545740",
        "id": "2d96a688-b25e-409b-80c0-a1266789efeb",
        "titulo": "The Mad Mage",
        "nome_asset": "The Mad Mage 2",
        "categoria": "NotInEventPool"
      },
      {
        "chave": "resources.assets:2545741",
        "id": "4eda9b0c-848d-472d-9036-1bcb41d2ce7b",
        "titulo": "The Mad Mage",
        "nome_asset": "The Mad Mage 3",
        "categoria": "NotInEventPool"
      }
    ]
  },
  {
    "grupo_editorial": "The runes of the Ymir",
    "registros": [
      {
        "chave": "resources.assets:2545785",
        "id": "8e63fbe4-3e26-49fc-b9f0-8f4aa4676f67",
        "titulo": "The runes of the Ymir",
        "nome_asset": "Ymir Rune, Strength",
        "categoria": "Normal"
      },
      {
        "chave": "resources.assets:2545780",
        "id": "02eff442-4bb6-4e23-b99c-07c5d74e50d3",
        "titulo": "The runes of the Ymir",
        "nome_asset": "Ymir Rune, Courage - Victory",
        "categoria": "NotInEventPool"
      },
      {
        "chave": "resources.assets:2545781",
        "id": "57998f83-17c5-4e55-bf59-f56403d0ce14",
        "titulo": "The runes of the Ymir",
        "nome_asset": "Ymir Rune, Courage",
        "categoria": "NotInEventPool"
      },
      {
        "chave": "resources.assets:2545783",
        "id": "180d0256-b0b8-42bd-a0b7-d87bbcdcb874",
        "titulo": "The runes of the Ymir",
        "nome_asset": "Ymir Rune, Honor",
        "categoria": "NotInEventPool"
      }
    ]
  }
]
```

## Verificação e pendências

Auditoria offline reproduzível incluída no pacote de revisão, junto ao editorial e baseline protegido. O auditor lê esta parte02 de volta e confere cobertura/canonização, tabela, identidades, campos/literais, igualdade dos fatos e dos NULL, contagens, preservação de marcações/placeholders, vínculos ao catálogo e hashes das 11 entradas originais. Também verifica preservação dos cinco documentos prévios de b07/b08. A guarda adicional ampla conserva o snapshot de outros lotes: mudanças observadas fora do escopo são registradas no relatório e no handoff, sem atribuição de autoria ou alegação de que os dezoito documentos monitorados ficaram intactos. A saída real do comando ficará no handoff; este texto não antecipa um resultado de execução.

Aprovação de conteúdo pelo dono: PENDENTE. Revisão independente deste corretivo: PENDENTE. Runtime de todos os eventos: NAO_EXERCITADO. Nenhum EV-R1, parte01, b08, jogo, DLL/plugin, publicação ou push alterado/executado por este corretivo.
