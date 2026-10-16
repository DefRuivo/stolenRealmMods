# EV-R2-NORMAL-b06-parte03 — correção documental 101–120

Tarefa: t_b6fbd61d; original t_d8fe364d; revisão independente/pai t_4c07d669.
Data local da geração incremental: 2026-10-13T18:04:48-03:00.

Estado: PROPOSTA_NAO_IMPLEMENTADA_AGUARDA_DONO. Runtime: NAO_EXERCITADO. Sem jogo, DLL/plugin, alteração de EV-R1, publicação ou push.

Fontes autoritativas deste escopo, somente leitura: docs/cobertura/EV-R1/eventos.json, lote-Normal-v2.md, eventos.schema.json e catalogo-referencias.json. Parecer: independent-review.txt e review-dossier.zip anexados ao pai. Baseline 11/11 entradas do pai intactas no início; revalidada pela auditoria ao final.

Companheiro obrigatório: EV-R2-NORMAL-b06-parte03-evidencias.json (snapshot normalizado completo por evento, todos os NULL por JSONPath/motivo, propostas exatas e catálogo ForcedEnemies). É evidência documental, não substituição de eventos.json. Strings, escapes, tags e placeholders atuais são preservados literalmente em JSON. JSONPath $. nas tabelas é relativo ao evento identificado; índice absoluto zero-based indicado por evento. Não confundir indice autoral (começa em 1) com índices [0] dos arrays.

Normal designa categoria/pool; Common/Uncommon/Legendary são raridades. Peso é relativo, não probabilidade final. limite_rolagem é limiar serializado, não uma chance calculada. Referência de batalha não nula sozinha não indica iniciar=true. Modificadores de XP não são XP final.

Interpretação de alvo: campos_originais.targetType/characterPool e efeitos[].alvo são copiados nas evidências. Self/tipo_default_serializado é configuração, não demonstração de que todo efeito atingirá um único integrante nem de que a party inteira será afetada. Seleção concreta, RNG, atributos finais, moedas, loot e combate são runtime NAO_EXERCITADO. As mudanças propostas abaixo têm como alvo apenas strings, não esses parâmetros.

## Retificações nominais da parte01

Esta parte03 substitui a análise da parte01 para o escopo 101–120; a parte01 permanece intacta como histórico reprovado, não como fonte de dados atuais. Correção da proposta documental não equivale a editar o original inglês.

1. Identidades e prosa: corrigidas 18 chaves primárias; preservadas as de 117/118. Small Chest é :2545688 e Small Pile of Gold é :2545689, ambos Common/peso1.0/texto vazio. As chaves :2545710/:2545711 pertencem a 115/116. Os GUIDs, a prosa dos dois eventos menores e a prosa/SHA atribuídos a Sword na parte01 não são fonte; não são reproduzidos como original nesta parte.
2. Acusação de path_id duplicado REFUTADA: Snowstorm! é :2545690, Novice é :2545713. A colisão foi introduzida pela parte01, não pelas fontes.
3. Acusações Ethereal em Snowstorm!/Spear Trap/Stone Covered Grave e combate Ogre Debt Collector na sepultura REFUTADAS. Snowstorm! Failure1 aplica -30.0 percentMaxHealth e Frostbitten; Spear Trap Failure1 aplica -30.0 e Mortally Wounded; sepultura Failure1 aplica Enfeebled e nenhuma opção inicia batalha. As opções reais e os efeitos são inventariados abaixo.
4. Acusação de três Strange Crystal sem combate ou sem diferenciação REFUTADA: 106/107/108 iniciam batalha em Investigate, têm narrativas/terrenos e Ice/Molten/Thunder Guardian distintos. Retiradas sugestões genéricas de buff e a estatística sem evidência “99%”. Não há status Ethereal atual nesses três eventos.
5. Polished/Uncommon para Strange Fruit e colored 110–113 REFUTADO: são Common/peso1.0/disabled1 e Reach aplica Ethereal. Há narrativa de fantasma compartilhada, não uma prova de que precisam de quatro novos buffs de produção. Mantê-los desabilitados não oculta o achado; evita redesenho sem autorização.
6. Sword in the Stone é Common/peso1.0 e texto_resultados_possiveis preenchido; acusação de prompt vazio REFUTADA. Uma sugestão editorial concreta diferente, identificada como proposta, aparece abaixo. Não inserir GUID/SHA fictícios nem renomear o campo para texto_resultados_possíveis.
7. whose → who's é achado VÁLIDO do inglês ORIGINAL em opcoes[0].texto de 117/118, não no título Fight. Apenas documentado antes→depois. Retirar acusações de ogros: ForcedEnemies resolve Champion/Elite e Soldier/Fodder. O nome do template Ogre Debt Collector Battle não identifica a composição forçada. Os literais de ExpModifier são strings "3" (Expert) e "1.5" (Novice), com UseRewardModifiers=1. A comparação numérica dessas expressões constantes é 3 > 1.5; não mede XP efetivo e não sustenta Novice maior.
8. Test 119/120 já estão disabled1; retirar a proposta redundante de desativação e a afirmação de exposição na produção. Normal é categoria/pool, não prova de habilitação.
9. Removida a duplicação 108; 115/116 lidos por inteiro, inclusive opções, efeitos, overrides e encadeamento. Não há veredito de leitura inconclusa. A contagem antiga era 21 seções (3 MANTER/16 MELHORAR/2 de leitura inconclusa) contra 20 linhas (2 MANTER/18 MELHORAR); a contagem nova deriva do inventário único abaixo. O conflito em 109 e em 115/116 é encerrado pela decisão nova, sem herdar a tabela antiga.
10. Todas as sugestões novas são textos ingleses exatos; nenhuma tradução PT-BR de prosa do jogo é proposta. A explicação está em PT-BR. Não há ação “verificar buff” tratada como melhoria concluída nem alteração de status inexistente.

## Inventário único de decisões

| Ordinal | Chave | ID/GUID literal | Título literal | Categoria | Raridade | Peso | disabled | Decisão | Mudanças |
|---|---|---|---|---|---|---|---|---|---|
| 101 | resources.assets:2545688 | 851bad73-b960-4f87-a7b5-2e8d5f88f9ef | Small Chest | Normal | Common (0) | 1.0 | 0 | MANTER | 0 |
| 102 | resources.assets:2545689 | e3ae319f-0153-4966-9351-45728bd15ab2 | Small Pile of Gold | Normal | Common (0) | 1.0 | 0 | MANTER | 0 |
| 103 | resources.assets:2545690 | cf387b4d-057c-4da8-b0fd-b2126f0719b9 | Snowstorm! | Normal | Common (0) | 1.0 | 0 | MANTER | 0 |
| 104 | resources.assets:2545691 | 13817dd0-dd84-421e-bdb0-88e3f633c929 | Spear Trap | Normal | Common (0) | 1.0 | 0 | MELHORAR | 2 |
| 105 | resources.assets:2545692 | 5b93b343-2faf-4dd7-a851-5517f0c359f8 | Stone Covered Grave | Normal | Common (0) | 1.0 | 0 | MELHORAR | 1 |
| 106 | resources.assets:2545696 | b788d19c-f4c6-4884-a73b-70316efe8684 | Strange Crystal | Normal | Common (0) | 1.0 | 0 | MANTER | 0 |
| 107 | resources.assets:2545699 | 08b61e7f-8de1-4d56-8ad5-2ff7441a94ff | Strange Crystal | Normal | Common (0) | 1.0 | 0 | MANTER | 0 |
| 108 | resources.assets:2545702 | abf8f4db-5d17-4b75-984f-aa3f4638e610 | Strange Crystal | Normal | Common (0) | 1.0 | 0 | MANTER | 0 |
| 109 | resources.assets:2545693 | 9fadcccd-4a0b-422d-ba1f-c3d7a92f9448 | Strange Fruit | Normal | Common (0) | 1.0 | 1 | MANTER | 0 |
| 110 | resources.assets:2545694 | d4781e02-f860-4e50-9873-28a7f346b6c0 | Strange Green Crystal | Normal | Common (0) | 1.0 | 1 | MANTER | 0 |
| 111 | resources.assets:2545697 | cba95a7e-6d68-4229-9486-bacbd212ed54 | Strange Indigo Crystal | Normal | Common (0) | 1.0 | 1 | MANTER | 0 |
| 112 | resources.assets:2545700 | 63f3d9fc-910b-43e4-a347-99bafa8fa67a | Strange Orange Crystal | Normal | Common (0) | 1.0 | 1 | MANTER | 0 |
| 113 | resources.assets:2545703 | 4b273849-3355-4744-a21a-82274ad3efd7 | Strange Violet Crystal | Normal | Common (0) | 1.0 | 1 | MANTER | 0 |
| 114 | resources.assets:2545707 | 696ca858-700e-422f-8c63-edb61dda4e1c | Sword in the Stone | Normal | Common (0) | 1.0 | 0 | MELHORAR | 1 |
| 115 | resources.assets:2545710 | 94acc548-5d82-4605-a78b-f09748a50c0b | Talk to the Spirits. | Normal | Common (0) | 1.0 | 0 | MELHORAR | 1 |
| 116 | resources.assets:2545711 | 767772c7-68a5-48b1-9fc6-e1f502fa4cfb | Talking Suit of Armor | Normal | Uncommon (1) | 1.0 | 0 | MELHORAR | 1 |
| 117 | resources.assets:2545712 | 7a266af9-0c86-4165-a05f-4eb9b70fbf1b | Target Dummy Practice: Expert | Normal | Legendary (3) | 1.0 | 0 | MELHORAR | 3 |
| 118 | resources.assets:2545713 | a3161d22-3f5d-4ef4-8604-e8c0278722a0 | Target Dummy Practice: Novice | Normal | Uncommon (1) | 1.0 | 0 | MELHORAR | 2 |
| 119 | resources.assets:2545720 | 42742a47-8ea8-47f6-9115-44c22108e33b | Test - All Characters Event | Normal | Common (0) | 1.0 | 1 | MANTER | 0 |
| 120 | resources.assets:2545722 | 098afbc3-12a4-42d8-9c47-85497c72c35b | Test - Boss Event End | Normal | Common (0) | 1.0 | 1 | MANTER | 0 |

Contagem: 20 eventos únicos; MANTER=13; MELHORAR=7; mudanças de strings=11; decisões sem leitura inconclusa=20. NULL declarados por caminho=550; entradas ForcedEnemies resolvidas=20.

## Análise individual

### Evento 101 — Small Chest

Chave: `resources.assets:2545688`; índice absoluto: `$.eventos[101]`; ID/GUID: `851bad73-b960-4f87-a7b5-2e8d5f88f9ef`.
Categoria: Normal; raridade: Common (0); peso: 1.0; disabled: 0; nome_asset: "Small Chest".
Origem: arquivo=resources.assets; path_id=2545688; sha256_objeto=`6e5302eeebe9a3640b71f0edc4ce1d2fe5d68db5871c86013b26d32a99b4cc17`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MANTER. MANTER o evento menor (isLesserEvent=1) e suas strings vazias. Open concede um item (Global, quantidade_configurada=1), sem ouro/XP habilitados. Vazio é valor literal, não prosa perdida; não há evidência offline para exigir narrativa ou alterar recompensa.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "",
  "texto_resultados_possiveis": ""
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Open"; texto=""; ações=1.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 0.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

NULL: 13 caminhos declarados; todos listados com motivo em `eventos[ordinal=101].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Mudanças propostas: nenhuma. Preservar todos os campos/valores atuais; correções acima são da análise documental, não dos assets.

### Evento 102 — Small Pile of Gold

Chave: `resources.assets:2545689`; índice absoluto: `$.eventos[102]`; ID/GUID: `e3ae319f-0153-4966-9351-45728bd15ab2`.
Categoria: Normal; raridade: Common (0); peso: 1.0; disabled: 0; nome_asset: "Small Pile of Gold".
Origem: arquivo=resources.assets; path_id=2545689; sha256_objeto=`af6cc793138cdba40b252578ccdd17cea7a6ccc9e348ac4022b3b1ac3bbe51a7`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MANTER. MANTER o evento menor (isLesserEvent=1) e suas strings vazias. Take habilita ouro com razão 0.25, sem item/XP habilitados. A quantidade final depende da partida; não inventar moeda fixa nem armadilha.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "",
  "texto_resultados_possiveis": ""
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Take"; texto=""; ações=1.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": true,
    "retirar": false,
    "razao": 0.25
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
  },
  "itens": {
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

NULL: 13 caminhos declarados; todos listados com motivo em `eventos[ordinal=102].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Mudanças propostas: nenhuma. Preservar todos os campos/valores atuais; correções acima são da análise documental, não dos assets.

### Evento 103 — Snowstorm!

Chave: `resources.assets:2545690`; índice absoluto: `$.eventos[103]`; ID/GUID: `cf387b4d-057c-4da8-b0fd-b2126f0719b9`.
Categoria: Normal; raridade: Common (0); peso: 1.0; disabled: 0; nome_asset: "Snowstorm!".
Origem: arquivo=resources.assets; path_id=2545690; sha256_objeto=`4fd686bd01ffac1144e6944006c278a04a391040ad13292368e0df62355b63a2`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MANTER. MANTER a estrutura atual: Survive possui Success/limite_rolagem=10 com XP habilitado/razão 0.5 e Failure/limite_rolagem=1 com percentMaxHealth=-30.0 e Frostbitten. Não há Ethereal nem batalha configurada; não há base para redesenhar o risco como resistências mistas.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "A savage <blue><b><incr>Snowstorm</incr></b></blue> rips through the frozen wilds, swallowing the familiar landmarks and the sparse shelter of the evergreens in a swirling abyss of white. Even the sun is smothered by the relentless snowfall, plunging the world into an eerie, muted twilight. The temperature plummets, each breath seizing your lungs with an icy grip.",
  "texto_resultados_possiveis": "What will you do?"
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Survive"; texto="Bundle up and press forward."; ações=2.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=10; texto="In the heart of the storm, something within you stirs. A defiance, fierce and fiery, rising against the encroaching despair. And so you cling onto that ember of hope, letting it fuel your determination, and push onwards.\n\n\nFinally, as if honoring your relentless perseverance, the storm begins to relent. Its howling winds quiet to a whimper, its furious assault fades into a gentle flurry. Exhausted yet triumphant, you emerge from the storm's icy grip.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": true,
    "razao": 0.5
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
  - `$.opcoes[0].efeitos[1]`: resultado=Failure (1); limite_rolagem=1; texto="Your boots slip and skid on hidden ice, each step becoming a treacherous journey in itself. The biting chill gnaws at your flesh, sinking its icy teeth through your weather-beaten clothes. \n\r\nYou crumple to the ground, the chill seeping through your clothing and into your bones. The cold tightens its grip, as the world begins to fade into an endless expanse of white.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[1].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 0.5
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
    Efeito `$.opcoes[0].efeitos[1].efeitos[1]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [
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
      }
    ],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

NULL: 34 caminhos declarados; todos listados com motivo em `eventos[ordinal=103].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Mudanças propostas: nenhuma. Preservar todos os campos/valores atuais; correções acima são da análise documental, não dos assets.

### Evento 104 — Spear Trap

Chave: `resources.assets:2545691`; índice absoluto: `$.eventos[104]`; ID/GUID: `13817dd0-dd84-421e-bdb0-88e3f633c929`.
Categoria: Normal; raridade: Common (0); peso: 1.0; disabled: 0; nome_asset: "Spear Trap".
Origem: arquivo=resources.assets; path_id=2545691; sha256_objeto=`d23eebf5d182f5de16699264fb15ba0b28ab8a60af84f27466523da0b5cc24ae`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MELHORAR. MELHORAR somente dois erros no inglês original: punctuatethe → punctuate the em texto e eruptes → erupts no texto de Failure. Preservar Success/10, Failure/1, percentMaxHealth=-30.0 e Mortally Wounded; não introduzir dano que já existe nem remover Fortune inexistente.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "Crisscrossed patterns of holes punctuatethe otherwise unremarkable floor. Periodically, spears thrust out from the holes in a sudden, violent eruption of deadly force before retracting back into the stone floor. The <red><b><incr>Spear Trap</incr></b></red> has an organic rhythm to it, like a beast's heartbeat, savage and relentless.\n\nThe spears are crudely fashioned, their tips are sharpened stone, secured to thick wooden shafts with rough, leather bindings. But their primitive appearance belies their lethal potential. The trap is set to skewer anyone or anything that stepped into its path without proper caution.\n",
  "texto_resultados_possiveis": "Who will attempt to disable this lethal trap?"
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Disable"; texto="Brave the incoming spears to make it to the kill switch on the other side."; ações=2.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=10; texto="[name] carefully studies the trap, observing the pattern of the emerging spears, noting the brief lulls in their murderous dance. Then, just as [he] sees [his] opportunity, [he] plunges forward. [He] leaps and rolls, evading the spears as they shoot out to impale [him].\n\n\nFinally, [he] reaches the trap's kill switch, a simple lever hidden behind an outcrop of rock. With a swift motion, [he] pulls it down. The spears shudder to a halt, their lethal dance interrupted.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": true,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
  - `$.opcoes[0].efeitos[1]`: resultado=Failure (1); limite_rolagem=1; texto="With a swift lunge, [name] reaches for the killswitch. [His] fingers brush against the cold, rough surface, only to be snatched back as a spear eruptes from the ground, narrowly missing [his] hand. [He] stumbles backward, but fails to avoid the row of spears that rise up in quick succession.\n\n\nA thick line of red mars [his] side, a deadly souvenir from [his] failed attempt to disarm the trap.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[1].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 0.5
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
    Efeito `$.opcoes[0].efeitos[1].efeitos[1]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [
      {
        "chave": "resources.assets:2545497",
        "nome": "Mortally Wounded",
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545497
        },
        "tipo": "EventStatus",
        "descricao": "Reduces @Healing Received@ by @25%@ per stack.",
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
            "expressao": "-25",
            "segunda_passagem": false
          }
        ]
      }
    ],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

NULL: 34 caminhos declarados; todos listados com motivo em `eventos[ordinal=104].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Proposta concreta — somente sugestão ao dono, não aplicada. Cada antes/depois abaixo é a string COMPLETA; campo espelho informa proveniência serializada, não autoriza edição de EV-R1.

```json
[
  {
    "id": "B06-104-01",
    "natureza": "CORRECAO_DO_INGLES_ORIGINAL",
    "idioma": "en",
    "jsonpath": "$.texto",
    "jsonpath_absoluto": "$.eventos[104].texto",
    "antes": "Crisscrossed patterns of holes punctuatethe otherwise unremarkable floor. Periodically, spears thrust out from the holes in a sudden, violent eruption of deadly force before retracting back into the stone floor. The <red><b><incr>Spear Trap</incr></b></red> has an organic rhythm to it, like a beast's heartbeat, savage and relentless.\n\nThe spears are crudely fashioned, their tips are sharpened stone, secured to thick wooden shafts with rough, leather bindings. But their primitive appearance belies their lethal potential. The trap is set to skewer anyone or anything that stepped into its path without proper caution.\n",
    "depois": "Crisscrossed patterns of holes punctuate the otherwise unremarkable floor. Periodically, spears thrust out from the holes in a sudden, violent eruption of deadly force before retracting back into the stone floor. The <red><b><incr>Spear Trap</incr></b></red> has an organic rhythm to it, like a beast's heartbeat, savage and relentless.\n\nThe spears are crudely fashioned, their tips are sharpened stone, secured to thick wooden shafts with rough, leather bindings. But their primitive appearance belies their lethal potential. The trap is set to skewer anyone or anything that stepped into its path without proper caution.\n",
    "campo_serializado_espelho": "$.campos_originais.encounterText",
    "valor_proposto": "Crisscrossed patterns of holes punctuate the otherwise unremarkable floor. Periodically, spears thrust out from the holes in a sudden, violent eruption of deadly force before retracting back into the stone floor. The <red><b><incr>Spear Trap</incr></b></red> has an organic rhythm to it, like a beast's heartbeat, savage and relentless.\n\nThe spears are crudely fashioned, their tips are sharpened stone, secured to thick wooden shafts with rough, leather bindings. But their primitive appearance belies their lethal potential. The trap is set to skewer anyone or anything that stepped into its path without proper caution.\n",
    "alvo": "Somente o texto deste evento resources.assets:2545691; nenhuma mudança de destinatário/efeito/recompensa.",
    "condicao": "Aprovação expressa do dono; apenas a exibição deste campo deste asset (ou opção/ação indicada pelo JSONPath). Preservar rolagens, placeholders, tags e ramos; não implementar nesta tarefa."
  },
  {
    "id": "B06-104-02",
    "natureza": "CORRECAO_DO_INGLES_ORIGINAL",
    "idioma": "en",
    "jsonpath": "$.opcoes[0].efeitos[1].texto",
    "jsonpath_absoluto": "$.eventos[104].opcoes[0].efeitos[1].texto",
    "antes": "With a swift lunge, [name] reaches for the killswitch. [His] fingers brush against the cold, rough surface, only to be snatched back as a spear eruptes from the ground, narrowly missing [his] hand. [He] stumbles backward, but fails to avoid the row of spears that rise up in quick succession.\n\n\nA thick line of red mars [his] side, a deadly souvenir from [his] failed attempt to disarm the trap.",
    "depois": "With a swift lunge, [name] reaches for the killswitch. [His] fingers brush against the cold, rough surface, only to be snatched back as a spear erupts from the ground, narrowly missing [his] hand. [He] stumbles backward, but fails to avoid the row of spears that rise up in quick succession.\n\n\nA thick line of red mars [his] side, a deadly souvenir from [his] failed attempt to disarm the trap.",
    "campo_serializado_espelho": "$.opcoes[0].efeitos[1].campos_originais.activationText",
    "valor_proposto": "With a swift lunge, [name] reaches for the killswitch. [His] fingers brush against the cold, rough surface, only to be snatched back as a spear erupts from the ground, narrowly missing [his] hand. [He] stumbles backward, but fails to avoid the row of spears that rise up in quick succession.\n\n\nA thick line of red mars [his] side, a deadly souvenir from [his] failed attempt to disarm the trap.",
    "alvo": "Somente o texto deste evento resources.assets:2545691; nenhuma mudança de destinatário/efeito/recompensa.",
    "condicao": "Aprovação expressa do dono; apenas a exibição deste campo deste asset (ou opção/ação indicada pelo JSONPath). Preservar rolagens, placeholders, tags e ramos; não implementar nesta tarefa."
  }
]
```

### Evento 105 — Stone Covered Grave

Chave: `resources.assets:2545692`; índice absoluto: `$.eventos[105]`; ID/GUID: `5b93b343-2faf-4dd7-a851-5517f0c359f8`.
Categoria: Normal; raridade: Common (0); peso: 1.0; disabled: 0; nome_asset: "Stone Covered Grave".
Origem: arquivo=resources.assets; path_id=2545692; sha256_objeto=`e5d64203ecce1473eb0988a5ebd98de4052ae929b8612f9c9d8932a98a476e6f`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MELHORAR. MELHORAR somente whispereof → whisper of em texto. Preservar Loot grave (Success/8: ouro razão 0.5 e um item; Failure/1: Enfeebled) e Leave sem ações serializadas. Nenhuma ação inicia batalha: retirar a acusação de Ogre Debt Collector, não propor inimigos substitutos.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "A simple wooden stake, battered by time and weather, marks a solemn grave. You stand over the humble mound of stone and earth, pondering your own mortality and the possible treasure below. Graves often whispereof untold riches hidden beneath the undisturbed soil.",
  "texto_resultados_possiveis": "What will you do?"
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Loot grave"; texto="Rob the grave."; ações=2.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=8; texto="With a sigh, you kneel and begin to gently move the stones. Your actions are slow, methodical. Not out of respect, but to make sure you don't harm anything valuable that might lay beneath. Your hand brushes against something solid, and your heart gives a hopeful lurch.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": true,
    "retirar": false,
    "razao": 0.5
  },
  "experiencia": {
    "dar": false,
    "razao": 2.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
  - `$.opcoes[0].efeitos[1]`: resultado=Failure (1); limite_rolagem=1; texto="With a sigh, you kneel and begin to gently move the stones. Your actions are slow, methodical. Not out of respect, but to make sure you don't harm anything valuable that might lay beneath. Soon enough, your fingertips brush against something solid—a wooden casket, rotted and eaten by time, but still intact.\r\n\r\nYour heart pounds in your chest as you pry open the coffin, a foul, fetid stench hits you like a wave. You grimace, looking for any sign of riches or possessions, but there is nothing more than the sad, silent testament of mortality.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[1].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
      "limitItemRarities": 1,
      "possibleRarities": [
        1,
        2
      ]
    }
  },
  "status": {
    "candidatos": [
      {
        "chave": "resources.assets:2545494",
        "nome": "Enfeebled",
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545494
        },
        "tipo": "EventStatus",
        "descricao": "Reduces @Damage@ by @20%@ per stack.",
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
            "expressao": "-20",
            "segunda_passagem": false
          }
        ]
      }
    ],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
- `$.opcoes[1]`: titulo="Leave"; texto="Think better of disturbing the dead."; ações=0.

NULL: 26 caminhos declarados; todos listados com motivo em `eventos[ordinal=105].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Proposta concreta — somente sugestão ao dono, não aplicada. Cada antes/depois abaixo é a string COMPLETA; campo espelho informa proveniência serializada, não autoriza edição de EV-R1.

```json
[
  {
    "id": "B06-105-01",
    "natureza": "CORRECAO_DO_INGLES_ORIGINAL",
    "idioma": "en",
    "jsonpath": "$.texto",
    "jsonpath_absoluto": "$.eventos[105].texto",
    "antes": "A simple wooden stake, battered by time and weather, marks a solemn grave. You stand over the humble mound of stone and earth, pondering your own mortality and the possible treasure below. Graves often whispereof untold riches hidden beneath the undisturbed soil.",
    "depois": "A simple wooden stake, battered by time and weather, marks a solemn grave. You stand over the humble mound of stone and earth, pondering your own mortality and the possible treasure below. Graves often whisper of untold riches hidden beneath the undisturbed soil.",
    "campo_serializado_espelho": "$.campos_originais.encounterText",
    "valor_proposto": "A simple wooden stake, battered by time and weather, marks a solemn grave. You stand over the humble mound of stone and earth, pondering your own mortality and the possible treasure below. Graves often whisper of untold riches hidden beneath the undisturbed soil.",
    "alvo": "Somente o texto deste evento resources.assets:2545692; nenhuma mudança de destinatário/efeito/recompensa.",
    "condicao": "Aprovação expressa do dono; apenas a exibição deste campo deste asset (ou opção/ação indicada pelo JSONPath). Preservar rolagens, placeholders, tags e ramos; não implementar nesta tarefa."
  }
]
```

### Evento 106 — Strange Crystal

Chave: `resources.assets:2545696`; índice absoluto: `$.eventos[106]`; ID/GUID: `b788d19c-f4c6-4884-a73b-70316efe8684`.
Categoria: Normal; raridade: Common (0); peso: 1.0; disabled: 0; nome_asset: "Strange Ice Crystal".
Origem: arquivo=resources.assets; path_id=2545696; sha256_objeto=`8c63f22a42c51bdfaf76b35904b937f8e6aff99eeca47b5f1d605a6bacc4b9b1`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MANTER. MANTER a variante azul/frio do deserto: Investigate inicia batalha com quatro Ice Guardian e modificador forçado próprio; Leave não inicia batalha. minLevel=3. Não há status Ethereal para substituir, nem necessidade demonstrada de inventar buff defensivo.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "In the parched dunes of Wyrmrest Desert, you find a gleaming anomaly that seems to defy the reality of its surroundings. A <blue><b><incr>Strange Crystal</incr></b></blue> floats eerily above the hot sand, its very presence carving out a radius of chilling winter within the searing landscape. Snow falls gently around it, each flake sparkling like diamond dust in the stark contrast of the desert sun. An oasis of cold in the sweltering desert.\r\n\nWith every step closer, the oppressive desert heat is replaced by an increasingly frigid blast. You steel yourself against the cold, squinting up at the magnificent crystal. There is something about the frosty gem that seems to promise immense power. \n",
  "texto_resultados_possiveis": "What will you do?"
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Investigate"; texto="Perhaps you can take some of this crystal's power for yourself."; ações=1.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="Unable to resist the lure of untapped power, you reach out, your fingers stretching towards the enticing gleam of the crystal. But as your hand nears its surface, the air around the crystal roiles with sudden ferocity. With a loud, shattering noise, towering figures rise from the frozen sand, shaped from the very ice and magic that surrounds the crystal. They stand as colossal guardians, their crystalline bodies refracting the desert sunlight into a thousand colors.".
    Batalha: iniciar=true, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
- `$.opcoes[1]`: titulo="Leave"; texto="The cold wind causes you to hesitate, and you decide against investigating it further."; ações=1.
  - `$.opcoes[1].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="With a last glance at the icy spectacle, you turn away, leaving the oddity behind, carrying forward with the desert's heat pressing relentlessly against your back.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[1].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

ForcedEnemies resolvido por CharacterInfo no catálogo (m_FileID=0/resources.assets). Não inferido do título do template:

```json
[
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[0].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545162
    },
    "chave": "resources.assets:2545162",
    "script": "CharacterInfo",
    "nome_asset": "Ice Guardian",
    "mods": [
      {
        "indice": 0,
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545335
        },
        "script": "EnemyMod",
        "nome_asset": "Freezing"
      }
    ]
  },
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[1].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545162
    },
    "chave": "resources.assets:2545162",
    "script": "CharacterInfo",
    "nome_asset": "Ice Guardian",
    "mods": [
      {
        "indice": 0,
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545335
        },
        "script": "EnemyMod",
        "nome_asset": "Freezing"
      }
    ]
  },
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[2].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545162
    },
    "chave": "resources.assets:2545162",
    "script": "CharacterInfo",
    "nome_asset": "Ice Guardian",
    "mods": [
      {
        "indice": 0,
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545335
        },
        "script": "EnemyMod",
        "nome_asset": "Freezing"
      }
    ]
  },
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[3].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545162
    },
    "chave": "resources.assets:2545162",
    "script": "CharacterInfo",
    "nome_asset": "Ice Guardian",
    "mods": [
      {
        "indice": 0,
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545335
        },
        "script": "EnemyMod",
        "nome_asset": "Freezing"
      }
    ]
  }
]
```

NULL: 26 caminhos declarados; todos listados com motivo em `eventos[ordinal=106].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Mudanças propostas: nenhuma. Preservar todos os campos/valores atuais; correções acima são da análise documental, não dos assets.

### Evento 107 — Strange Crystal

Chave: `resources.assets:2545699`; índice absoluto: `$.eventos[107]`; ID/GUID: `08b61e7f-8de1-4d56-8ad5-2ff7441a94ff`.
Categoria: Normal; raridade: Common (0); peso: 1.0; disabled: 0; nome_asset: "Strange Molten Crystal".
Origem: arquivo=resources.assets; path_id=2545699; sha256_objeto=`ce0e1aebe73a6ffe0b2da64d812efba4871d9e8137a42b182a2b52b5efef34e5`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MANTER. MANTER a variante vermelha/calor da selva: Investigate inicia batalha com quatro Molten Guardian e modificador forçado próprio; Leave não inicia batalha. minLevel=3. O conteúdo já difere de 106; retirar a tese de variante idêntica sem combate e a generalização sem evidência.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "Amid the lush, dense foliage of the jungle, an anomaly cuts through the saturated air - a <red><b><incr>Strange Crystal</incr></b></red>, bathed in an ember glow. Steam rises from where it hovers, twisting the air with volcanic heat, a fiery aura in sharp contrast to the damp, emerald greenery. Drenched in sweat, you cautiously approach the burning radiance. It is dangerously hot, yet you are drawn to the extraordinary jewel.",
  "texto_resultados_possiveis": "What will you do?"
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Investigate"; texto="Perhaps you can take some of this crystal's power for yourself."; ações=1.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="As you outstretch your hand towards the crystal, the ground rumbles beneath you. In a fissure of volcanic eruption, golems of molten rock and ash spring forth. They tower over you, their bodies glowing with an internal fire, acting as the crystal's fierce protectors.".
    Batalha: iniciar=true, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
- `$.opcoes[1]`: titulo="Leave"; texto="The heat causes you to hesitate, and you decide against investigating it further."; ações=1.
  - `$.opcoes[1].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="With a last glance at the volcanic spectacle, you turn away, leaving the oddity behind, pushing further into the emerald jungle.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[1].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

ForcedEnemies resolvido por CharacterInfo no catálogo (m_FileID=0/resources.assets). Não inferido do título do template:

```json
[
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[0].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545165
    },
    "chave": "resources.assets:2545165",
    "script": "CharacterInfo",
    "nome_asset": "Molten Guardian",
    "mods": [
      {
        "indice": 0,
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545334
        },
        "script": "EnemyMod",
        "nome_asset": "Explosive"
      }
    ]
  },
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[1].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545165
    },
    "chave": "resources.assets:2545165",
    "script": "CharacterInfo",
    "nome_asset": "Molten Guardian",
    "mods": [
      {
        "indice": 0,
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545334
        },
        "script": "EnemyMod",
        "nome_asset": "Explosive"
      }
    ]
  },
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[2].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545165
    },
    "chave": "resources.assets:2545165",
    "script": "CharacterInfo",
    "nome_asset": "Molten Guardian",
    "mods": [
      {
        "indice": 0,
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545334
        },
        "script": "EnemyMod",
        "nome_asset": "Explosive"
      }
    ]
  },
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[3].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545165
    },
    "chave": "resources.assets:2545165",
    "script": "CharacterInfo",
    "nome_asset": "Molten Guardian",
    "mods": [
      {
        "indice": 0,
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545334
        },
        "script": "EnemyMod",
        "nome_asset": "Explosive"
      }
    ]
  }
]
```

NULL: 26 caminhos declarados; todos listados com motivo em `eventos[ordinal=107].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Mudanças propostas: nenhuma. Preservar todos os campos/valores atuais; correções acima são da análise documental, não dos assets.

### Evento 108 — Strange Crystal

Chave: `resources.assets:2545702`; índice absoluto: `$.eventos[108]`; ID/GUID: `abf8f4db-5d17-4b75-984f-aa3f4638e610`.
Categoria: Normal; raridade: Common (0); peso: 1.0; disabled: 0; nome_asset: "Strange Thunder Crystal".
Origem: arquivo=resources.assets; path_id=2545702; sha256_objeto=`ec4351e85aca4ea408d3187df74203c42122d6e5c4e73686bc9aeeb11bdbace4`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MANTER. MANTER a variante amarela/tempestade de Emberlands: Investigate inicia batalha com quatro Thunder Guardian e modificador forçado próprio; Leave não inicia batalha. minLevel=3. A identidade é única neste lote; não duplicar a seção nem inventar buff utilitário.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "Walking upon the fiery landscape of the Emberlands, you are greeted not by the oppressive heat you'd expect, but by the cool touch of rain and the deep, resonating rumble of thunder echoing across the open sky. The smell of fresh rain blends with the scent of smoke and ash, as great drops of water meet the burning ground with a soft sizzle.\n\nHovering in front of you is a <yellow><b><incr>Strange Crystal</incr></b></yellow> of immense size, glimmering and reflecting the stormy skies overhead. \n\nYour heart pounds as you approach the mesmerizing crystal, drawn by its captivating allure.",
  "texto_resultados_possiveis": "What will you do?"
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Investigate"; texto="Perhaps you can take some of this crystal's power for yourself."; ações=1.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="With a breath of courage, you extend your hand towards the crystal. The moment your fingertips grace its cool, smooth surface, the sky roars in disapproval. What had been a calm rain quickly turns into a tempestuous maelstrom, the once distant thunder now sounding alarmingly close.\n\n\nFrom the stormy canvas above, giant figures of thunder and lightning descended, manifesting into terrifying golems.".
    Batalha: iniciar=true, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
- `$.opcoes[1]`: titulo="Leave"; texto="The sudden storm causes you to hesitate, and you decide against investigating it further."; ações=1.
  - `$.opcoes[1].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="With a last glance at the stormy spectacle, you turn away, leaving the oddity behind, pushing further into the Emberlands.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[1].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

ForcedEnemies resolvido por CharacterInfo no catálogo (m_FileID=0/resources.assets). Não inferido do título do template:

```json
[
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[0].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545168
    },
    "chave": "resources.assets:2545168",
    "script": "CharacterInfo",
    "nome_asset": "Thunder Guardian",
    "mods": [
      {
        "indice": 0,
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545358
        },
        "script": "EnemyMod",
        "nome_asset": "Teleporting"
      }
    ]
  },
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[1].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545168
    },
    "chave": "resources.assets:2545168",
    "script": "CharacterInfo",
    "nome_asset": "Thunder Guardian",
    "mods": [
      {
        "indice": 0,
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545358
        },
        "script": "EnemyMod",
        "nome_asset": "Teleporting"
      }
    ]
  },
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[2].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545168
    },
    "chave": "resources.assets:2545168",
    "script": "CharacterInfo",
    "nome_asset": "Thunder Guardian",
    "mods": [
      {
        "indice": 0,
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545358
        },
        "script": "EnemyMod",
        "nome_asset": "Teleporting"
      }
    ]
  },
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[3].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545168
    },
    "chave": "resources.assets:2545168",
    "script": "CharacterInfo",
    "nome_asset": "Thunder Guardian",
    "mods": [
      {
        "indice": 0,
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545358
        },
        "script": "EnemyMod",
        "nome_asset": "Teleporting"
      }
    ]
  }
]
```

NULL: 26 caminhos declarados; todos listados com motivo em `eventos[ordinal=108].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Mudanças propostas: nenhuma. Preservar todos os campos/valores atuais; correções acima são da análise documental, não dos assets.

### Evento 109 — Strange Fruit

Chave: `resources.assets:2545693`; índice absoluto: `$.eventos[109]`; ID/GUID: `9fadcccd-4a0b-422d-ba1f-c3d7a92f9448`.
Categoria: Normal; raridade: Common (0); peso: 1.0; disabled: 1; nome_asset: "Strange Fruit".
Origem: arquivo=resources.assets; path_id=2545693; sha256_objeto=`0c7b2edbc5aa22d4faa5c66e226e93c9b033654eba1cc375ec99c7f28dccc9d1`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MANTER. MANTER disabled=1 e os dados atuais, sem ativar o evento. Há discrepância real entre título Strange Fruit e narrativa de fantasma; Reach aplica Ethereal e também habilita um item. Por ser asset desabilitado, não propor redesign/rebalanceamento sem decisão de reativação do dono. O antigo Polished/+25% duplo era dado falso.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "The yearning ghost extends her hand pleading for help.",
  "texto_resultados_possiveis": ""
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Reach"; texto="You reach out to the ghost. Gain [o1a1_status]."; ações=1.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="You reach out, but your hand passes through cold air. Memories flood your mind and longing fills your heart.\n\nYou gain [o1a1_status].".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
  },
  "itens": {
    "dar": true,
    "pool_tipo": {
      "valor": 2,
      "nome": "Unassigned"
    },
    "quantidade_configurada": 1,
    "tabelas": [],
    "restricoes": {
      "limitItemTypes": 1,
      "possibleItemTypes": [],
      "limitItemRarities": 1,
      "possibleRarities": []
    }
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
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
- `$.opcoes[1]`: titulo="Leave"; texto="The chill in the air causes you to hesitate. You leave without helping."; ações=1.
  - `$.opcoes[1].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="You leave, but the ghost's disappointment haunts your dreams.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[1].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

NULL: 26 caminhos declarados; todos listados com motivo em `eventos[ordinal=109].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Mudanças propostas: nenhuma. Preservar todos os campos/valores atuais; correções acima são da análise documental, não dos assets.

### Evento 110 — Strange Green Crystal

Chave: `resources.assets:2545694`; índice absoluto: `$.eventos[110]`; ID/GUID: `d4781e02-f860-4e50-9873-28a7f346b6c0`.
Categoria: Normal; raridade: Common (0); peso: 1.0; disabled: 1; nome_asset: "Strange Green Crystal".
Origem: arquivo=resources.assets; path_id=2545694; sha256_objeto=`25a95bf4e1fc8f84879b6c497ce4ef825d7c7cdf816a5509292c8ba8c3001d64`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MANTER. MANTER disabled=1; narrativa de fantasma e Reach/Ethereal são dados atuais de um template desabilitado, não buff Polished de cristal verde. A discrepância título/narrativa é registrada, mas não exige ativação nem mudança mecânica neste escopo.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "The yearning ghost extends her hand pleading for help.",
  "texto_resultados_possiveis": ""
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Reach"; texto="You reach out to the ghost. Gain [o1a1_status]."; ações=1.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="You reach out, but your hand passes through cold air. Memories flood your mind and longing fills your heart.\n\nYou gain [o1a1_status].".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
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
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
- `$.opcoes[1]`: titulo="Leave"; texto="The chill in the air causes you to hesitate. You leave without helping."; ações=1.
  - `$.opcoes[1].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="You leave, but the ghost's disappointment haunts your dreams.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[1].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

NULL: 26 caminhos declarados; todos listados com motivo em `eventos[ordinal=110].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Mudanças propostas: nenhuma. Preservar todos os campos/valores atuais; correções acima são da análise documental, não dos assets.

### Evento 111 — Strange Indigo Crystal

Chave: `resources.assets:2545697`; índice absoluto: `$.eventos[111]`; ID/GUID: `cba95a7e-6d68-4229-9486-bacbd212ed54`.
Categoria: Normal; raridade: Common (0); peso: 1.0; disabled: 1; nome_asset: "Strange Indigo Crystal".
Origem: arquivo=resources.assets; path_id=2545697; sha256_objeto=`ba4ab9b6af2d5206bad107d47e2a665c445f8a2afce993a8e8f1bf4fe8d580d4`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MANTER. MANTER disabled=1; narrativa de fantasma e Reach/Ethereal são dados atuais de um template desabilitado, não buff Polished de cristal índigo. Registrar a discrepância sem criar mana/inteligência ou duração inventadas.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "The yearning ghost extends her hand pleading for help.",
  "texto_resultados_possiveis": ""
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Reach"; texto="You reach out to the ghost. Gain [o1a1_status]."; ações=1.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="You reach out, but your hand passes through cold air. Memories flood your mind and longing fills your heart.\n\nYou gain [o1a1_status].".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
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
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
- `$.opcoes[1]`: titulo="Leave"; texto="The chill in the air causes you to hesitate. You leave without helping."; ações=1.
  - `$.opcoes[1].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="You leave, but the ghost's disappointment haunts your dreams.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[1].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

NULL: 26 caminhos declarados; todos listados com motivo em `eventos[ordinal=111].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Mudanças propostas: nenhuma. Preservar todos os campos/valores atuais; correções acima são da análise documental, não dos assets.

### Evento 112 — Strange Orange Crystal

Chave: `resources.assets:2545700`; índice absoluto: `$.eventos[112]`; ID/GUID: `63f3d9fc-910b-43e4-a347-99bafa8fa67a`.
Categoria: Normal; raridade: Common (0); peso: 1.0; disabled: 1; nome_asset: "Strange Orange Crystal".
Origem: arquivo=resources.assets; path_id=2545700; sha256_objeto=`b19b8bdbc8d6ccc7768884fd2bb81917a50b98172cad9a0cc6aea6d2dc7b5a65`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MANTER. MANTER disabled=1; narrativa de fantasma e Reach/Ethereal são dados atuais de um template desabilitado, não buff Polished de cristal laranja. Registrar a discrepância sem criar força/dano ou duração inventados.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "The yearning ghost extends her hand pleading for help.",
  "texto_resultados_possiveis": ""
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Reach"; texto="You reach out to the ghost. Gain [o1a1_status]."; ações=1.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="You reach out, but your hand passes through cold air. Memories flood your mind and longing fills your heart.\n\nYou gain [o1a1_status].".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
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
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
- `$.opcoes[1]`: titulo="Leave"; texto="The chill in the air causes you to hesitate. You leave without helping."; ações=1.
  - `$.opcoes[1].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="You leave, but the ghost's disappointment haunts your dreams.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[1].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

NULL: 26 caminhos declarados; todos listados com motivo em `eventos[ordinal=112].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Mudanças propostas: nenhuma. Preservar todos os campos/valores atuais; correções acima são da análise documental, não dos assets.

### Evento 113 — Strange Violet Crystal

Chave: `resources.assets:2545703`; índice absoluto: `$.eventos[113]`; ID/GUID: `4b273849-3355-4744-a21a-82274ad3efd7`.
Categoria: Normal; raridade: Common (0); peso: 1.0; disabled: 1; nome_asset: "Strange Violet Crystal".
Origem: arquivo=resources.assets; path_id=2545703; sha256_objeto=`6ecafd6b179454d799485eaba4b6740fa94fb7afcb95d92547adf967bc9654dd`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MANTER. MANTER disabled=1; narrativa de fantasma e Reach/Ethereal são dados atuais de um template desabilitado, não buff Polished de cristal violeta. A ausência de diferenciação entre estes templates não justifica percentuais sem teste; preservar a configuração.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "The yearning ghost extends her hand pleading for help.",
  "texto_resultados_possiveis": ""
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Reach"; texto="You reach out to the ghost. Gain [o1a1_status]."; ações=1.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="You reach out, but your hand passes through cold air. Memories flood your mind and longing fills your heart.\n\nYou gain [o1a1_status].".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
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
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
- `$.opcoes[1]`: titulo="Leave"; texto="The chill in the air causes you to hesitate. You leave without helping."; ações=1.
  - `$.opcoes[1].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="You leave, but the ghost's disappointment haunts your dreams.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[1].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

NULL: 26 caminhos declarados; todos listados com motivo em `eventos[ordinal=113].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Mudanças propostas: nenhuma. Preservar todos os campos/valores atuais; correções acima são da análise documental, não dos assets.

### Evento 114 — Sword in the Stone

Chave: `resources.assets:2545707`; índice absoluto: `$.eventos[114]`; ID/GUID: `696ca858-700e-422f-8c63-edb61dda4e1c`.
Categoria: Normal; raridade: Common (0); peso: 1.0; disabled: 0; nome_asset: "Sword in the Stone".
Origem: arquivo=resources.assets; path_id=2545707; sha256_objeto=`03c65db52323405fe93c1009d0d59d9f5a9abbcbdddef0e54bbc78e83a088e16`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MELHORAR. MELHORAR somente a consistência de tempo verbal: You approached the sword → You approach the sword em texto. texto_resultados_possiveis já está preenchido. Preservar Retrieve/Success18 (item e The True King), Failure0 (Weakened e encadeamento Sword in the Stone 1), Leave e Common/peso1.0.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "Deep within the forest you find a gleaming <b><gold>Sword</gold></b> lodged into a massive stone, the brilliant sheen of its blade contrasts starkly against the dull gray of the rock. The weapon is an artwork, its craftsmanship surpassing anything you have seen before. It is an enigma, a beacon of lustrous steel amidst the undergrowth and detritus.\n\nYou approached the sword, captivated by its beauty. Its hilt is wrought of intricately interwoven patterns, a delicate dance of metal that hints at the work of a master smith. The blade itself is magnificent, a length of flawless steel that shines as if it were the day it were forged. How long it has been here is unknowable, but its splendor has clearly withstood the test of time.",
  "texto_resultados_possiveis": "Who will attempt to pull the <b><gold>Sword</gold></b> from the stone?"
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Retrieve"; texto="Attempt to pull the <b><gold>Sword</gold></b> from the stone."; ações=2.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=18; texto="Your fingers curl around the hilt, feeling an unexpected warmth seeping into your hand. An odd sense of harmony resonates within you, a chord that seems to reverberate between your heart and the sword. With renewed vigor, you pull, the veins in your arm throbbing with the exertion.\n\n\nSuddenly, the sword comes free. You stumble back in surprise, the blade held aloft in your hand. It shines even brighter now, as if recognizing its new master.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
  },
  "itens": {
    "dar": true,
    "pool_tipo": {
      "valor": 0,
      "nome": "None"
    },
    "quantidade_configurada": 1,
    "tabelas": [
      {
        "mustGetOne": 1,
        "itemLootChances": [
          {
            "ItemInfo": {
              "m_FileID": 0,
              "m_PathID": 2547088
            },
            "Chance": 100.0
          }
        ]
      }
    ],
    "restricoes": {
      "limitItemTypes": 0,
      "possibleItemTypes": [],
      "limitItemRarities": 0,
      "possibleRarities": []
    }
  },
  "status": {
    "candidatos": [
      {
        "chave": "resources.assets:2545478",
        "nome": "The True King",
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545478
        },
        "tipo": "EventStatus",
        "descricao": "Light Spells no longer cost mana to cast. @Holy Power@ increased by {6,30}%.\n\n<i><color=#808080>\"The light is your birth right.\"</color></i>\n",
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
              "chave": "resources.assets:2544378",
              "nome": "DamageModHealing",
              "pptr": {
                "m_FileID": 0,
                "m_PathID": 2544378
              },
              "tipo": "CharacterAttribute"
            },
            "metodo": {
              "valor": 0,
              "nome": "Base"
            },
            "expressao": "{6,30}",
            "segunda_passagem": false
          },
          {
            "atributo": {
              "chave": "resources.assets:2544479",
              "nome": "ManaCostModLight",
              "pptr": {
                "m_FileID": 0,
                "m_PathID": 2544479
              },
              "tipo": "CharacterAttribute"
            },
            "metodo": {
              "valor": 0,
              "nome": "Base"
            },
            "expressao": "{-10000, -10000}",
            "segunda_passagem": false
          }
        ]
      }
    ],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
  - `$.opcoes[0].efeitos[1]`: resultado=Failure (1); limite_rolagem=0; texto="Tentatively, you reach out, your fingers closing around the ornate hilt. With a determined grit, you pull at the sword, your muscles straining under the effort. But the stone is unyielding, keeping the weapon locked tight within its grip. You release the hilt, your hands trembling with exertion. Frustration bubbles within you, your heavy breaths echoing your defeat. The failed attempt has left you [o1a2_status].".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": "resources.assets:2545704", "nome": "Sword in the Stone 1", "pptr": {"m_FileID": 0, "m_PathID": 2545704}, "tipo": "PartyEvent"}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[1].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
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
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
- `$.opcoes[1]`: titulo="Leave"; texto="You haven't the time for swords or stones."; ações=1.
  - `$.opcoes[1].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[1].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

NULL: 37 caminhos declarados; todos listados com motivo em `eventos[ordinal=114].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Proposta concreta — somente sugestão ao dono, não aplicada. Cada antes/depois abaixo é a string COMPLETA; campo espelho informa proveniência serializada, não autoriza edição de EV-R1.

```json
[
  {
    "id": "B06-114-01",
    "natureza": "AJUSTE_EDITORIAL_DO_INGLES_ORIGINAL",
    "idioma": "en",
    "jsonpath": "$.texto",
    "jsonpath_absoluto": "$.eventos[114].texto",
    "antes": "Deep within the forest you find a gleaming <b><gold>Sword</gold></b> lodged into a massive stone, the brilliant sheen of its blade contrasts starkly against the dull gray of the rock. The weapon is an artwork, its craftsmanship surpassing anything you have seen before. It is an enigma, a beacon of lustrous steel amidst the undergrowth and detritus.\n\nYou approached the sword, captivated by its beauty. Its hilt is wrought of intricately interwoven patterns, a delicate dance of metal that hints at the work of a master smith. The blade itself is magnificent, a length of flawless steel that shines as if it were the day it were forged. How long it has been here is unknowable, but its splendor has clearly withstood the test of time.",
    "depois": "Deep within the forest you find a gleaming <b><gold>Sword</gold></b> lodged into a massive stone, the brilliant sheen of its blade contrasts starkly against the dull gray of the rock. The weapon is an artwork, its craftsmanship surpassing anything you have seen before. It is an enigma, a beacon of lustrous steel amidst the undergrowth and detritus.\n\nYou approach the sword, captivated by its beauty. Its hilt is wrought of intricately interwoven patterns, a delicate dance of metal that hints at the work of a master smith. The blade itself is magnificent, a length of flawless steel that shines as if it were the day it were forged. How long it has been here is unknowable, but its splendor has clearly withstood the test of time.",
    "campo_serializado_espelho": "$.campos_originais.encounterText",
    "valor_proposto": "Deep within the forest you find a gleaming <b><gold>Sword</gold></b> lodged into a massive stone, the brilliant sheen of its blade contrasts starkly against the dull gray of the rock. The weapon is an artwork, its craftsmanship surpassing anything you have seen before. It is an enigma, a beacon of lustrous steel amidst the undergrowth and detritus.\n\nYou approach the sword, captivated by its beauty. Its hilt is wrought of intricately interwoven patterns, a delicate dance of metal that hints at the work of a master smith. The blade itself is magnificent, a length of flawless steel that shines as if it were the day it were forged. How long it has been here is unknowable, but its splendor has clearly withstood the test of time.",
    "alvo": "Somente o texto deste evento resources.assets:2545707; nenhuma mudança de destinatário/efeito/recompensa.",
    "condicao": "Aprovação expressa do dono; apenas a exibição deste campo deste asset (ou opção/ação indicada pelo JSONPath). Preservar rolagens, placeholders, tags e ramos; não implementar nesta tarefa."
  }
]
```

### Evento 115 — Talk to the Spirits.

Chave: `resources.assets:2545710`; índice absoluto: `$.eventos[115]`; ID/GUID: `94acc548-5d82-4605-a78b-f09748a50c0b`.
Categoria: Normal; raridade: Common (0); peso: 1.0; disabled: 0; nome_asset: "Talk ta de Spirits!".
Origem: arquivo=resources.assets; path_id=2545710; sha256_objeto=`907314ed02db8834def9b99447a67389759ff27a79941c2599213d3fcf5018b8`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MELHORAR. MELHORAR somente o prompt autoral vazio de texto_resultados_possiveis para explicitar a escolha já existente. Sacrifice/Success0 aplica percentMaxHealth=-30.0 e encadeia Talk ta de Spirits! 1 (:2545708); Decline não causa esse custo. Não prometer buff/XP/loot nem analisar a continuação fora da faixa. O ponto no título é preservado, sem diagnóstico automático de erro.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "A gnarled goblin, thin and aged, sits hunched over a crackling blue fire. He hums softly, a low, melodic chant that seems to echo within the flames.\n\n\nThe goblin lifts his gaze to meet yours. His eyes hold the weight of centuries, but there is a spark of wisdom there, a knowing that surpasses the mere comprehension of time. \"Your ancestors,\" he rasps, his voice like the crackling of dry leaves. \"They wish to speak with you. Will you pay the price, to hear them?\"",
  "texto_resultados_possiveis": ""
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Sacrifice"; texto="Give up your lifeblood."; ações=1.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="The goblin draws a small, sharp blade from his rags and offers it. You take it, your heart pounding in your chest as you slice a shallow cut across your palm, the crimson droplets hissing as they fall into the blue flames.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": "resources.assets:2545708", "nome": "Talk ta de Spirits! 1", "pptr": {"m_FileID": 0, "m_PathID": 2545708}, "tipo": "PartyEvent"}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
- `$.opcoes[1]`: titulo="Decline"; texto="You don't have time for spirits now."; ações=1.
  - `$.opcoes[1].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="You walk away, wondering what your ancestors would say...".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[1].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

NULL: 24 caminhos declarados; todos listados com motivo em `eventos[ordinal=115].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Proposta concreta — somente sugestão ao dono, não aplicada. Cada antes/depois abaixo é a string COMPLETA; campo espelho informa proveniência serializada, não autoriza edição de EV-R1.

```json
[
  {
    "id": "B06-115-01",
    "natureza": "ADICAO_DE_WORDING_EM_INGLES",
    "idioma": "en",
    "jsonpath": "$.texto_resultados_possiveis",
    "jsonpath_absoluto": "$.eventos[115].texto_resultados_possiveis",
    "antes": "",
    "depois": "Will you sacrifice some of your lifeblood to speak with your ancestors?",
    "campo_serializado_espelho": "$.campos_originais.encounterPossibleResultsText",
    "valor_proposto": "Will you sacrifice some of your lifeblood to speak with your ancestors?",
    "alvo": "Somente o texto deste evento resources.assets:2545710; nenhuma mudança de destinatário/efeito/recompensa.",
    "condicao": "Aprovação expressa do dono; apenas a exibição deste campo deste asset (ou opção/ação indicada pelo JSONPath). Preservar rolagens, placeholders, tags e ramos; não implementar nesta tarefa."
  }
]
```

### Evento 116 — Talking Suit of Armor

Chave: `resources.assets:2545711`; índice absoluto: `$.eventos[116]`; ID/GUID: `767772c7-68a5-48b1-9fc6-e1f502fa4cfb`.
Categoria: Normal; raridade: Uncommon (1); peso: 1.0; disabled: 0; nome_asset: "Talking Suit of Armor".
Origem: arquivo=resources.assets; path_id=2545711; sha256_objeto=`081b13c288b4e97a74b659d5c206e0af8adc985f71ccdd8d36203c1d295b57ab`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MELHORAR. MELHORAR somente o prompt autoral vazio de texto_resultados_possiveis para apresentar Polish ou Sharpen. Polish/Success0 aplica Polished (descrição literal: Armor/Magic Armor {15,250}); Sharpen/Success0 aplica Sharpened (Physical Damage GetFlatDamageValue()). Ouro não está habilitado em nenhuma opção, apesar de razões serializadas. Não mudar buffs/duração/raridade.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "Your eyes are drawn to a decorative armor stand proudly displayed on a stone pedestal. A suit of armor stands resolute, the burnished steel gleaming in the light.\n\n\nYou approach the armor stand, eyes wide with admiration as you take in the ornate detailing. The intricate scrollwork and gem-encrusted embellishments speak of a time when glory and honor were as much a part of a warrior's armor as the steel that protected him.\n\n\nJust as you reach out a hand to trace the decorative etchings, a deep voice echoes from within the armor, causing you to jump back in surprise.\n\n\n\"Hold there, knave!\" The voice boomed out, gruff and resonating within the metallic shell. \"With armor as stained as yours, I'm surprised you dare to touch mine!\"\n\n\"And those weapons, dull as a rusted spoon!\" The voice continued with more than a hint of disgust. \"They'd barely nick a foe, let alone strike a fatal blow. You wouldn't have lasted a minute in the decorated company of <silver><b><incr>Captain Henry Irons</incr></b></silver>!\"\n\n",
  "texto_resultados_possiveis": ""
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Polish"; texto="Begin furiously polishing your armor to appease the sentient Captain Irons."; ações=1.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="\"Still looks like something a hedge knight discarded,\" Captain Irons mused aloud. Yet, despite the continuous critique, there is an underlying tone of approval that encourages you.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 0.5
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [
      {
        "chave": "resources.assets:2545464",
        "nome": "Polished",
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545464
        },
        "tipo": "EventStatus",
        "descricao": "Increases @Armor@ and @Magic Armor@ by {15,250}.",
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
              "chave": "resources.assets:2544401",
              "nome": "Armor",
              "pptr": {
                "m_FileID": 0,
                "m_PathID": 2544401
              },
              "tipo": "CharacterAttribute"
            },
            "metodo": {
              "valor": 0,
              "nome": "Base"
            },
            "expressao": "{15,250}",
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
              "valor": 0,
              "nome": "Base"
            },
            "expressao": "{15,250}",
            "segunda_passagem": false
          }
        ]
      }
    ],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
- `$.opcoes[1]`: titulo="Sharpen"; texto="Quickly sharpen your weapon to satisfy Captain Irons."; ações=1.
  - `$.opcoes[1].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="Despite the grousing, you can hear the hint of admiration creeping into the armor's tone. \"Well, it's a start,\" Irons finally admits, and the words feel like a hard-earned compliment.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[1].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 3.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [
      {
        "chave": "resources.assets:2545468",
        "nome": "Sharpened",
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545468
        },
        "tipo": "EventStatus",
        "descricao": "Increases @Physical Damage@ by GetFlatDamageValue().",
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
              "chave": "resources.assets:2544371",
              "nome": "DamageFlatPhysical",
              "pptr": {
                "m_FileID": 0,
                "m_PathID": 2544371
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
      }
    ],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

NULL: 26 caminhos declarados; todos listados com motivo em `eventos[ordinal=116].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Proposta concreta — somente sugestão ao dono, não aplicada. Cada antes/depois abaixo é a string COMPLETA; campo espelho informa proveniência serializada, não autoriza edição de EV-R1.

```json
[
  {
    "id": "B06-116-01",
    "natureza": "ADICAO_DE_WORDING_EM_INGLES",
    "idioma": "en",
    "jsonpath": "$.texto_resultados_possiveis",
    "jsonpath_absoluto": "$.eventos[116].texto_resultados_possiveis",
    "antes": "",
    "depois": "Will you polish your armor or sharpen your weapon for Captain Irons?",
    "campo_serializado_espelho": "$.campos_originais.encounterPossibleResultsText",
    "valor_proposto": "Will you polish your armor or sharpen your weapon for Captain Irons?",
    "alvo": "Somente o texto deste evento resources.assets:2545711; nenhuma mudança de destinatário/efeito/recompensa.",
    "condicao": "Aprovação expressa do dono; apenas a exibição deste campo deste asset (ou opção/ação indicada pelo JSONPath). Preservar rolagens, placeholders, tags e ramos; não implementar nesta tarefa."
  }
]
```

### Evento 117 — Target Dummy Practice: Expert

Chave: `resources.assets:2545712`; índice absoluto: `$.eventos[117]`; ID/GUID: `7a266af9-0c86-4165-a05f-4eb9b70fbf1b`.
Categoria: Normal; raridade: Legendary (3); peso: 1.0; disabled: 0; nome_asset: "Target Dummy Practice_ Expert".
Origem: arquivo=resources.assets; path_id=2545712; sha256_objeto=`0a45d17474cf820e433e69868111cdc428abd702848dd56067f9e162195bf2ed`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MELHORAR. MELHORAR somente o inglês: whose → who's em opcoes[0].texto, not matter → no matter em opcoes[1].texto e preencher texto_resultados_possiveis vazio com o mesmo prompt já usado em Novice. Fight continua sendo o título. ForcedEnemies são um Target Dummy Champion e três Target Dummy Elite; ExpModifier=3. Não substituir a batalha por supostos ogros.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "Arrayed before you stand four <silver><b><incr>Armored Target Dummies</incr></b></silver>, motionless metal sentinels. Yet, as you approach, a voice calls out, strangely alive and full of mirth. “Well, well,” it cackles, the sound strangely amplified around you. “What have we here? The sorriest excuse for a hero I've ever seen.\"\r\n\r\nYour brow furrows in confusion, but before you can react, another voice chimes in. \"You call those muscles? My grandma's knitting needles are thicker!\"\n\nThe jibes seem to come from the dummies, a bizarre enchantment has breathed life into them. \n\n\"Go on, hero,\" a dummy taunts, \"Show us what little you've got.\"",
  "texto_resultados_possiveis": ""
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Fight"; texto="Show these Dummies whose boss!"; ações=1.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="\"My grandmother could hit harder than you, and she was inanimate!\"".
    Batalha: iniciar=true, manual=false, referência={"chave": "resources.assets:2544649", "nome": "Ogre Debt Collector Battle", "pptr": {"m_FileID": 0, "m_PathID": 2544649}, "tipo": "BattleInfo"}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 3.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
- `$.opcoes[1]`: titulo="Leave"; texto="The dummies' taunts can't goad you into hitting them, not matter how hurtful they are..."; ações=1.
  - `$.opcoes[1].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="\"<bounce>ALL HAIL, LORD OF THE COWARDS!</bounce>\" the Dummies taunt. \"We can't even hit you back, ya ninny!\".".
    Batalha: iniciar=false, manual=false, referência={"chave": "resources.assets:2544649", "nome": "Ogre Debt Collector Battle", "pptr": {"m_FileID": 0, "m_PathID": 2544649}, "tipo": "BattleInfo"}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[1].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

ForcedEnemies resolvido por CharacterInfo no catálogo (m_FileID=0/resources.assets). Não inferido do título do template:

```json
[
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[0].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545174
    },
    "chave": "resources.assets:2545174",
    "script": "CharacterInfo",
    "nome_asset": "Target Dummy Champion",
    "mods": []
  },
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[1].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545175
    },
    "chave": "resources.assets:2545175",
    "script": "CharacterInfo",
    "nome_asset": "Target Dummy Elite",
    "mods": []
  },
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[2].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545175
    },
    "chave": "resources.assets:2545175",
    "script": "CharacterInfo",
    "nome_asset": "Target Dummy Elite",
    "mods": []
  },
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[3].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545175
    },
    "chave": "resources.assets:2545175",
    "script": "CharacterInfo",
    "nome_asset": "Target Dummy Elite",
    "mods": []
  }
]
```

NULL: 22 caminhos declarados; todos listados com motivo em `eventos[ordinal=117].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Proposta concreta — somente sugestão ao dono, não aplicada. Cada antes/depois abaixo é a string COMPLETA; campo espelho informa proveniência serializada, não autoriza edição de EV-R1.

```json
[
  {
    "id": "B06-117-01",
    "natureza": "CORRECAO_DO_INGLES_ORIGINAL",
    "idioma": "en",
    "jsonpath": "$.opcoes[0].texto",
    "jsonpath_absoluto": "$.eventos[117].opcoes[0].texto",
    "antes": "Show these Dummies whose boss!",
    "depois": "Show these Dummies who's boss!",
    "campo_serializado_espelho": "$.opcoes[0].campos_originais.description",
    "valor_proposto": "Show these Dummies who's boss!",
    "alvo": "Somente o texto deste evento resources.assets:2545712; nenhuma mudança de destinatário/efeito/recompensa.",
    "condicao": "Aprovação expressa do dono; apenas a exibição deste campo deste asset (ou opção/ação indicada pelo JSONPath). Preservar rolagens, placeholders, tags e ramos; não implementar nesta tarefa."
  },
  {
    "id": "B06-117-02",
    "natureza": "CORRECAO_DO_INGLES_ORIGINAL",
    "idioma": "en",
    "jsonpath": "$.opcoes[1].texto",
    "jsonpath_absoluto": "$.eventos[117].opcoes[1].texto",
    "antes": "The dummies' taunts can't goad you into hitting them, not matter how hurtful they are...",
    "depois": "The dummies' taunts can't goad you into hitting them, no matter how hurtful they are...",
    "campo_serializado_espelho": "$.opcoes[1].campos_originais.description",
    "valor_proposto": "The dummies' taunts can't goad you into hitting them, no matter how hurtful they are...",
    "alvo": "Somente o texto deste evento resources.assets:2545712; nenhuma mudança de destinatário/efeito/recompensa.",
    "condicao": "Aprovação expressa do dono; apenas a exibição deste campo deste asset (ou opção/ação indicada pelo JSONPath). Preservar rolagens, placeholders, tags e ramos; não implementar nesta tarefa."
  },
  {
    "id": "B06-117-03",
    "natureza": "ADICAO_DE_WORDING_EM_INGLES",
    "idioma": "en",
    "jsonpath": "$.texto_resultados_possiveis",
    "jsonpath_absoluto": "$.eventos[117].texto_resultados_possiveis",
    "antes": "",
    "depois": "Will you teach these dummies a lesson?",
    "campo_serializado_espelho": "$.campos_originais.encounterPossibleResultsText",
    "valor_proposto": "Will you teach these dummies a lesson?",
    "alvo": "Somente o texto deste evento resources.assets:2545712; nenhuma mudança de destinatário/efeito/recompensa.",
    "condicao": "Aprovação expressa do dono; apenas a exibição deste campo deste asset (ou opção/ação indicada pelo JSONPath). Preservar rolagens, placeholders, tags e ramos; não implementar nesta tarefa."
  }
]
```

### Evento 118 — Target Dummy Practice: Novice

Chave: `resources.assets:2545713`; índice absoluto: `$.eventos[118]`; ID/GUID: `a3161d22-3f5d-4ef4-8604-e8c0278722a0`.
Categoria: Normal; raridade: Uncommon (1); peso: 1.0; disabled: 0; nome_asset: "Target Dummy Practice_ Novice".
Origem: arquivo=resources.assets; path_id=2545713; sha256_objeto=`56dd249f4b119e39853c8e70a847f284d6187eab599a7292912021b371a9c6af`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MELHORAR. MELHORAR somente o inglês: whose → who's em opcoes[0].texto e not matter → no matter em opcoes[1].texto. texto_resultados_possiveis já preenchido fica intacto. ForcedEnemies são um Target Dummy Soldier e três Target Dummy Fodder; ExpModifier=1.5, menor que Expert=3. Não afirmar XP efetivo medido ou trocar inimigos.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "Four simple <green><b><incr>Target Dummies</incr></b></green> stand assembled in front of you. Identical and humble in their simplicity. Yet, as you step closer, a voice calls out.\n\n\n\"Aha! Boys, look here!\" comes a rough, husky voice that is decidedly out of place coming from an inanimate object. You glance around, a puzzled look on your face, your eyes finally landing on the straw dummies.\n\n\n\"Look at this sorry sight,\" the voice continues, a chuckle in its tone. \"I think we're looking at the walking definition of a 'zero.' Is there such a thing as the opposite of a hero? Because if so, that's what you are.\"\n\n\nA chorus of laughter rings out from the straw figures. ",
  "texto_resultados_possiveis": "Will you teach these dummies a lesson?"
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Fight"; texto="Show these Dummies whose boss!"; ações=1.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="\"If looks could kill I'd be dead already!\"".
    Batalha: iniciar=true, manual=false, referência={"chave": "resources.assets:2544649", "nome": "Ogre Debt Collector Battle", "pptr": {"m_FileID": 0, "m_PathID": 2544649}, "tipo": "BattleInfo"}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 3.0
  },
  "experiencia": {
    "dar": false,
    "razao": 0.5
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
- `$.opcoes[1]`: titulo="Leave"; texto="The dummies' taunts can't goad you into hitting them, not matter how hurtful they are..."; ações=1.
  - `$.opcoes[1].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="\"You're runnin' away from straw?!\" the Dummies taunt. \"<bounce>So Brave!</bounce>\".".
    Batalha: iniciar=false, manual=false, referência={"chave": "resources.assets:2544649", "nome": "Ogre Debt Collector Battle", "pptr": {"m_FileID": 0, "m_PathID": 2544649}, "tipo": "BattleInfo"}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[1].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

ForcedEnemies resolvido por CharacterInfo no catálogo (m_FileID=0/resources.assets). Não inferido do título do template:

```json
[
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[0].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545177
    },
    "chave": "resources.assets:2545177",
    "script": "CharacterInfo",
    "nome_asset": "Target Dummy Soldier",
    "mods": []
  },
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[1].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545176
    },
    "chave": "resources.assets:2545176",
    "script": "CharacterInfo",
    "nome_asset": "Target Dummy Fodder",
    "mods": []
  },
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[2].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545176
    },
    "chave": "resources.assets:2545176",
    "script": "CharacterInfo",
    "nome_asset": "Target Dummy Fodder",
    "mods": []
  },
  {
    "jsonpath": "$.opcoes[0].efeitos[0].batalha.override.ForcedEnemies[3].CharacterInfo",
    "pptr": {
      "m_FileID": 0,
      "m_PathID": 2545176
    },
    "chave": "resources.assets:2545176",
    "script": "CharacterInfo",
    "nome_asset": "Target Dummy Fodder",
    "mods": []
  }
]
```

NULL: 22 caminhos declarados; todos listados com motivo em `eventos[ordinal=118].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Proposta concreta — somente sugestão ao dono, não aplicada. Cada antes/depois abaixo é a string COMPLETA; campo espelho informa proveniência serializada, não autoriza edição de EV-R1.

```json
[
  {
    "id": "B06-118-01",
    "natureza": "CORRECAO_DO_INGLES_ORIGINAL",
    "idioma": "en",
    "jsonpath": "$.opcoes[0].texto",
    "jsonpath_absoluto": "$.eventos[118].opcoes[0].texto",
    "antes": "Show these Dummies whose boss!",
    "depois": "Show these Dummies who's boss!",
    "campo_serializado_espelho": "$.opcoes[0].campos_originais.description",
    "valor_proposto": "Show these Dummies who's boss!",
    "alvo": "Somente o texto deste evento resources.assets:2545713; nenhuma mudança de destinatário/efeito/recompensa.",
    "condicao": "Aprovação expressa do dono; apenas a exibição deste campo deste asset (ou opção/ação indicada pelo JSONPath). Preservar rolagens, placeholders, tags e ramos; não implementar nesta tarefa."
  },
  {
    "id": "B06-118-02",
    "natureza": "CORRECAO_DO_INGLES_ORIGINAL",
    "idioma": "en",
    "jsonpath": "$.opcoes[1].texto",
    "jsonpath_absoluto": "$.eventos[118].opcoes[1].texto",
    "antes": "The dummies' taunts can't goad you into hitting them, not matter how hurtful they are...",
    "depois": "The dummies' taunts can't goad you into hitting them, no matter how hurtful they are...",
    "campo_serializado_espelho": "$.opcoes[1].campos_originais.description",
    "valor_proposto": "The dummies' taunts can't goad you into hitting them, no matter how hurtful they are...",
    "alvo": "Somente o texto deste evento resources.assets:2545713; nenhuma mudança de destinatário/efeito/recompensa.",
    "condicao": "Aprovação expressa do dono; apenas a exibição deste campo deste asset (ou opção/ação indicada pelo JSONPath). Preservar rolagens, placeholders, tags e ramos; não implementar nesta tarefa."
  }
]
```

### Evento 119 — Test - All Characters Event

Chave: `resources.assets:2545720`; índice absoluto: `$.eventos[119]`; ID/GUID: `42742a47-8ea8-47f6-9115-44c22108e33b`.
Categoria: Normal; raridade: Common (0); peso: 1.0; disabled: 1; nome_asset: "Test - All Characters Event".
Origem: arquivo=resources.assets; path_id=2545720; sha256_objeto=`650289a46a35ee99fc3c5ec82ad91ff8033428543f77dfb3ffa7d67fbb366643`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MANTER. MANTER disabled=1 e os dados de teste, incluindo textos-placeholder e status Test Event Status. São quatro resultados em Open. e uma ação em Close. O prefixo Test não demonstra exposição no runtime; não duplicar uma desativação já existente nem corrigir todo o fixture como texto de produção.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "Timmy talked about this chest...",
  "texto_resultados_possiveis": "So open or close?"
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Open."; texto="Tacos are dexiious. Gain  [o1a1_health]"; ações=4.
  - `$.opcoes[0].efeitos[0]`: resultado=CriticalSuccess (2); limite_rolagem=16; texto="Here comes the sun, do do do do. Here comes the sun.".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
```json
{
  "vida_mana": {
    "percentMaxHealth": 15.0,
    "percentMaxMana": 15.0,
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 0.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [
      {
        "chave": "resources.assets:2545526",
        "nome": "Test Event Status - Critical Success",
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545526
        },
        "tipo": "EventStatus",
        "descricao": "Critical Success",
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
            "expressao": "-5",
            "segunda_passagem": false
          },
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
            "expressao": "-5",
            "segunda_passagem": false
          },
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
              "valor": 1,
              "nome": "Percentage"
            },
            "expressao": "-5",
            "segunda_passagem": false
          },
          {
            "atributo": {
              "chave": "resources.assets:2544458",
              "nome": "VitalityBase",
              "pptr": {
                "m_FileID": 0,
                "m_PathID": 2544458
              },
              "tipo": "CharacterAttribute"
            },
            "metodo": {
              "valor": 1,
              "nome": "Percentage"
            },
            "expressao": "-5",
            "segunda_passagem": false
          },
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
            "expressao": "-5",
            "segunda_passagem": false
          }
        ]
      }
    ],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
  - `$.opcoes[0].efeitos[1]`: resultado=Success (0); limite_rolagem=11; texto="Success!\n".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[1].efeitos[0]` (configuração, não resultado final):
```json
{
  "vida_mana": {
    "percentMaxHealth": 25.0,
    "percentMaxMana": 25.0,
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
  "ouro": {
    "dar": true,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": true,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [
      {
        "chave": "resources.assets:2545528",
        "nome": "Test Event Status - Success",
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545528
        },
        "tipo": "EventStatus",
        "descricao": "Success",
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
            "expressao": "-5",
            "segunda_passagem": false
          },
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
            "expressao": "-5",
            "segunda_passagem": false
          },
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
              "valor": 1,
              "nome": "Percentage"
            },
            "expressao": "-5",
            "segunda_passagem": false
          },
          {
            "atributo": {
              "chave": "resources.assets:2544458",
              "nome": "VitalityBase",
              "pptr": {
                "m_FileID": 0,
                "m_PathID": 2544458
              },
              "tipo": "CharacterAttribute"
            },
            "metodo": {
              "valor": 1,
              "nome": "Percentage"
            },
            "expressao": "-5",
            "segunda_passagem": false
          },
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
            "expressao": "-5",
            "segunda_passagem": false
          }
        ]
      }
    ],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
  - `$.opcoes[0].efeitos[2]`: resultado=Failure (1); limite_rolagem=5; texto="Failure".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[2].efeitos[0]` (configuração, não resultado final):
```json
{
  "vida_mana": {
    "percentMaxHealth": -35.0,
    "percentMaxMana": -35.0,
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
  "ouro": {
    "dar": false,
    "retirar": true,
    "razao": 1.0
  },
  "experiencia": {
    "dar": true,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [
      {
        "chave": "resources.assets:2545527",
        "nome": "Test Event Status - Failure",
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545527
        },
        "tipo": "EventStatus",
        "descricao": "Failure",
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
            "expressao": "-5",
            "segunda_passagem": false
          },
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
            "expressao": "-5",
            "segunda_passagem": false
          },
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
              "valor": 1,
              "nome": "Percentage"
            },
            "expressao": "-5",
            "segunda_passagem": false
          },
          {
            "atributo": {
              "chave": "resources.assets:2544458",
              "nome": "VitalityBase",
              "pptr": {
                "m_FileID": 0,
                "m_PathID": 2544458
              },
              "tipo": "CharacterAttribute"
            },
            "metodo": {
              "valor": 1,
              "nome": "Percentage"
            },
            "expressao": "-5",
            "segunda_passagem": false
          },
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
            "expressao": "-5",
            "segunda_passagem": false
          }
        ]
      }
    ],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
  - `$.opcoes[0].efeitos[3]`: resultado=CriticalFailure (3); limite_rolagem=0; texto="Critical Failure".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[3].efeitos[0]` (configuração, não resultado final):
```json
{
  "vida_mana": {
    "percentMaxHealth": -45.0,
    "percentMaxMana": -45.0,
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [
      {
        "chave": "resources.assets:2545525",
        "nome": "Test Event Status - Critical Failure",
        "pptr": {
          "m_FileID": 0,
          "m_PathID": 2545525
        },
        "tipo": "EventStatus",
        "descricao": "Critical Failure",
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
            "expressao": "-5",
            "segunda_passagem": false
          },
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
            "expressao": "-5",
            "segunda_passagem": false
          },
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
              "valor": 1,
              "nome": "Percentage"
            },
            "expressao": "-5",
            "segunda_passagem": false
          },
          {
            "atributo": {
              "chave": "resources.assets:2544458",
              "nome": "VitalityBase",
              "pptr": {
                "m_FileID": 0,
                "m_PathID": 2544458
              },
              "tipo": "CharacterAttribute"
            },
            "metodo": {
              "valor": 1,
              "nome": "Percentage"
            },
            "expressao": "-5",
            "segunda_passagem": false
          },
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
            "expressao": "-5",
            "segunda_passagem": false
          }
        ]
      }
    ],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
- `$.opcoes[1]`: titulo="Close"; texto="Dont open this crazy thing"; ações=1.
  - `$.opcoes[1].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="asdasda".
    Batalha: iniciar=false, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[1].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
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
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

NULL: 65 caminhos declarados; todos listados com motivo em `eventos[ordinal=119].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Mudanças propostas: nenhuma. Preservar todos os campos/valores atuais; correções acima são da análise documental, não dos assets.

### Evento 120 — Test - Boss Event End

Chave: `resources.assets:2545722`; índice absoluto: `$.eventos[120]`; ID/GUID: `098afbc3-12a4-42d8-9c47-85497c72c35b`.
Categoria: Normal; raridade: Common (0); peso: 1.0; disabled: 1; nome_asset: "Test - Boss Event End".
Origem: arquivo=resources.assets; path_id=2545722; sha256_objeto=`1badb4e52784533de424033b2600a9c251cf58c6c400d11caa298854244e7c68`. Demais caminhos_resource e proveniência exatos no JSON companheiro.

Veredito: MANTER. MANTER disabled=1 e os dados de teste. As duas ações têm iniciar=true e referência de batalha nula; isso é configuração declarada, não prova de erro em produção. Preservar sem ativar, remover ou inventar batalha. A exposição real não foi exercitada.

Valores atuais literais (JSON; sem tradução; strings vazias são "", não NULL):

```json
{
  "texto": "Timmy talked about this chest...",
  "texto_resultados_possiveis": ""
}
```

Opções e ações lidas integralmente:
- `$.opcoes[0]`: titulo="Fight Meh"; texto="Use the key and open the chest."; ações=1.
  - `$.opcoes[0].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="You use the key!".
    Batalha: iniciar=true, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[0].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 0.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```
- `$.opcoes[1]`: titulo="Fight Meh!!!"; texto="Dont open this crazy thing"; ações=1.
  - `$.opcoes[1].efeitos[0]`: resultado=Success (0); limite_rolagem=0; texto="".
    Batalha: iniciar=true, manual=false, referência={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; encadeamento={"chave": null, "nome": null, "motivo": "PPtr serializado com m_PathID=0 (referência nula no asset)."}; overrides de modo=0.
    Efeito `$.opcoes[1].efeitos[0].efeitos[0]` (configuração, não resultado final):
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
  "ouro": {
    "dar": false,
    "retirar": false,
    "razao": 1.0
  },
  "experiencia": {
    "dar": false,
    "razao": 1.0
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
    }
  },
  "status": {
    "candidatos": [],
    "sortear": false,
    "quantidade_sorteada_configurada": 1
  },
  "skills": [],
  "remocoes_status": []
}
```

NULL: 26 caminhos declarados; todos listados com motivo em `eventos[ordinal=120].null_por_caminho` do companheiro (a notação ordinal= é seletor documental, não JSONPath executável). Inclui referências nulas PPtr/path0 e resultados finais dependentes de runtime, inclusive cópias em opcoes[].recompensas. Não preencher por suposição. Runtime: NAO_EXERCITADO.

Mudanças propostas: nenhuma. Preservar todos os campos/valores atuais; correções acima são da análise documental, não dos assets.

## Proveniência da entrega incremental

A parte02 e seu JSON, encontrados na retomada de uma tentativa interrompida deste cartão, foram lidos e preservados byte a byte. A parte03 conserva seus 20 vereditos e 11 sugestões, substitui a entrega documental para revisão e acrescenta a explicitação dos literais de batalha. A primeira execução de python audit_b06.py falhou em XP modifiers porque o auditor comparava strings serializadas a números; não foi falha nos assets. O auditor foi corrigido para exigir os tipos e valores literais "3"/"1.5", sem normalizar a fonte. A comparação numérica é separada e não equivale a XP recebido.

Retificadas também as condições genéricas atribuídas na parte01 a 103–116: não herdar a afirmação de terrainTypesAllowedAtAnyTime=[4,3] para todos. condicoes e modos completos de cada evento estão copiados no JSON companheiro, com os índices e valores da fonte. Somente 117/118 nesta faixa têm esse array [4,3]. Categoria Normal não implica modo, terreno ou elegibilidade uniformes.

## Literais de configuração de batalha

Cada caminho abaixo é relativo ao evento do ordinal indicado. ExpModifier é string serializada (incluindo ""), não número já calculado; UseRewardModifiers é flag inteira. Mesmo um override preenchido não ativa batalha quando iniciar=false. Não há alteração mecânica proposta nestas linhas.

| Ordinal de origem | JSONPath da ação | iniciar | UseRewardModifiers | ExpModifier literal JSON | ForcedEnemies configurados |
|---|---|---|---|---|---|
| origem=101 | $.opcoes[0].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=102 | $.opcoes[0].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=103 | $.opcoes[0].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=103 | $.opcoes[0].efeitos[1] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=104 | $.opcoes[0].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=104 | $.opcoes[0].efeitos[1] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=105 | $.opcoes[0].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=105 | $.opcoes[0].efeitos[1] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=106 | $.opcoes[0].efeitos[0] | true | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 4 |
| origem=106 | $.opcoes[1].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=107 | $.opcoes[0].efeitos[0] | true | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 4 |
| origem=107 | $.opcoes[1].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=108 | $.opcoes[0].efeitos[0] | true | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 4 |
| origem=108 | $.opcoes[1].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=109 | $.opcoes[0].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=109 | $.opcoes[1].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=110 | $.opcoes[0].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=110 | $.opcoes[1].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=111 | $.opcoes[0].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=111 | $.opcoes[1].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=112 | $.opcoes[0].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=112 | $.opcoes[1].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=113 | $.opcoes[0].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=113 | $.opcoes[1].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=114 | $.opcoes[0].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=114 | $.opcoes[0].efeitos[1] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=114 | $.opcoes[1].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=115 | $.opcoes[0].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=115 | $.opcoes[1].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=116 | $.opcoes[0].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=116 | $.opcoes[1].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=117 | $.opcoes[0].efeitos[0] | true | 1 | "3" | 4 |
| origem=117 | $.opcoes[1].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=118 | $.opcoes[0].efeitos[0] | true | 1 | "1.5" | 4 |
| origem=118 | $.opcoes[1].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=119 | $.opcoes[0].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=119 | $.opcoes[0].efeitos[1] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=119 | $.opcoes[0].efeitos[2] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=119 | $.opcoes[0].efeitos[3] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=119 | $.opcoes[1].efeitos[0] | false | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=120 | $.opcoes[0].efeitos[0] | true | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |
| origem=120 | $.opcoes[1].efeitos[0] | true | 0 | "Mathf.Max(0, 5 - (TurnCount - 1)) * 100" | 0 |

## Auditoria offline e limites

Comando real (executar no workspace deste cartão): `python audit_b06.py`. Auditor separado do gerador (autoverificação do implementador, não substitui o revisor independente), com leitura nova das fontes e da parte03: ordem MD/JSON, cobertura/identidades, GUID/SHA, todo snapshot literal, campos/espelhos antes→depois, NULL por caminho/motivo, contagens e ForcedEnemies via catálogo. Controles negativos devem rejeitar identidade adulterada, antes inventado, SHA falso, caminho incorreto, NULL omitido, catálogo adulterado e seção duplicada. Saída real é entregue em EV-R2-NORMAL-b06-parte03-audit.txt e no handoff do cartão, não fabricada aqui.

A validação é exclusivamente offline. Não valida layout, placeholders renderizados, o balanceamento no jogo, a exposição dos templates disabled ou a premiação final. Aprovação técnica e aprovação de conteúdo pelo dono ainda são necessárias antes de qualquer futura implementação. Para desfazer a proposta documental, ignorar a parte03 e seu companheiro; nenhum arquivo-fonte nem a parte01 foi alterado.
