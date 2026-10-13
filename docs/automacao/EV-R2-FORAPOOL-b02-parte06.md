# EV-R2-FORAPOOL-b02 — parte 06: cautelas de apresentação não exercitada

Complemento imutável às partes 01–05. Fontes: `C:/dev/stolen-realm/docs/cobertura/EV-R1/eventos.json`, campos `campos_originais.promptToSelectCharacter`, `characterSelectedText`, `targetType`, `characterPool` e `opcoes[].campos_originais.hideOptionEffectText`. Os textos atuais completos desses campos também estão nas partes 02–04. Nenhuma mudança adicional é proposta por este complemento: permanecem 16 MELHORAR/wording, 5 MANTER e aprovação PENDENTE para as 21 chaves.

## Prompts com assunto aparentemente herdado de outro evento

Há 11 prompts cujo assunto diverge do contexto desta chave. Isso é anomalia textual no asset, não prova de texto exibido na UI. A proposta para ESSES CAMPOS é MANTER temporariamente: o caminho de seleção de personagem não foi exercitado e não há autorização para alterar condições/targetType. Não contam como novas substituições.

| Nº | Chave | Texto atual de promptToSelectCharacter (JSON literal) | Sinalização |
|---:|---|---|---|
| 22 | resources.assets:2545613 | `"Who will try and crack the <b><legend><incr>Heavy Safe</b></legend></incr>?"` | Fala de cofre, não da caixa/manivela. Tags têm fechamentos em ordem incomum; preservados. |
| 23 | resources.assets:2545615 | `"Who will try and crack the <b><legend><incr>Heavy Safe</b></legend></incr>?"` | Mesmo prompt de cofre; chave distinta da fase 2. |
| 24 | resources.assets:2545614 | `"Who will try and crack the <b><legend><incr>Heavy Safe</b></legend></incr>?"` | Mesmo prompt de cofre no desfecho do Jester/Paladin. |
| 27 | resources.assets:2545617 | `"Does anyone owe this Ogre money?"` | Menção de ogro no desfecho de Lesser Mimic; targetType=3 e characterPool=1, sem inferir se o prompt aparece. |
| 29 | resources.assets:2545650 | `"Who will listen to his pleas?"` | Pleas não são descritas na cena de treinamento com Barloc. |
| 30 | resources.assets:2545754 | `"Does anyone owe this Ogre money?"` | Menção de ogro em Mimic. |
| 33 | resources.assets:2545661 | `"Who will listen to his pleas?"` | Cena de rum/piratas sem interlocutor fazendo súplicas. |
| 34 | resources.assets:2545662 | `"Who will listen to his pleas?"` | Mesmo assunto deslocado, em outra fase. |
| 35 | resources.assets:2545663 | `"Who will listen to his pleas?"` | Mesmo assunto deslocado na quarta bebida. |
| 36 | resources.assets:2545667 | `"Who will take the crystal?"` | O texto e o efeito referem tesouro/Cursed Coin, não cristal. |
| 39 | resources.assets:2545679 | `"Who will learn the Dark Ritual?"` | Contexto de alpha da matilha e Mark of the Alpha, não ritual. |

`characterSelectedText="Good luck [name]..."` aparece nas chaves 2545617, 2545754, 2545657 e 2545658 (4 registros). Manter literalmente `[name]`; a seleção de personagem e a adequação da confirmação depois de vitória/derrota são NAO_EXERCITADO. Nos outros registros auditados, o texto selecionado está vazio e continua vazio.

Prompts não listados como assunto deslocado não são automaticamente comprovados corretos na UI. Todos os 21 eventos têm disponibilidade/apresentação NAO_EXERCITADO, motivo: tarefa somente documental, sem jogo ou runtime. Os dois epílogos sem opções (25 e 38) têm referências entrantes de VictoryEvent no canônico e no catálogo; ausência de opções não significa evento órfão.

## Efeito oculto não é opção oculta

Seção 22, `resources.assets:2545613`, Opção 2 Leave:

- `hideOptionEffectText=1`: configuração autoral para ocultar o texto de efeitos da opção.
- `ocultar_sem_requisitos=false` e `ocultar_se_status=[]`: nenhuma condição de ocultação da opção configurada nesses campos.
- Portanto, não afirmar que Leave esteja oculto ou seguro. Sua ação configura combate, inimigo forçado e VictoryEvent, embora a referência Battle seja nula.
- É a única das 28 opções do lote com `hideOptionEffectText` ativo. Não revelar na descrição um prêmio, chance ou cálculo que não foi exercitado, nem mudar esse flag.

## Leitura das anomalias sem decisão automática

A parte 02 já propõe tornar a confirmação do Paladin neutra entre Ivory Dragon Scale e o override Wrath of the Righteous, sem escolher a recompensa. A parte 04 já sinaliza Ruby of Rancor no evento do elefante e Cursed Coin em Pirate's Treasure, sem transformar fortuna em item ou ouro. Estes apontamentos não autorizam corrigir balanceamento, apagar protótipos, fundir variantes ou ativar eventos fora do pool.
