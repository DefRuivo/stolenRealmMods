# EV-R2-FORAPOOL-b01 — parte 03: eventos 15–21

Status: PROPOSTAS PARA APROVAÇÃO DO DONO; não implementadas. Fonte: `C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-NotInEventPool-v2.md`, seções 15–21; canônico/schema/referências: `eventos.json`, `eventos.schema.json`, `schema.md`, `catalogo-referencias.json` no mesmo diretório. As regras de substituição literal da parte01 se aplicam. Nenhum valor dinâmico, tag ou placeholder será preenchido ou recalculado.

NULL final é NAO_EXERCITADO, nunca zero: requer estado da partida, nível, alvo, modo e/ou RNG. NULL de PPtr é ausência de referência configurada com m_PathID=0; nem sempre é anomalia funcional, especialmente em campos inativos. Ver auditoria da parte04. Há 0 alterações de DLL/plugin/asset e 0 partidas abertas nesta entrega.

## Inventário parcial — 7 eventos

| Nº | Chave | Título / variante | Categoria | Raridade (valor) | Peso relativo | Veredito proposto | Natureza |
|---|---|---|---|---|---|---|---|
| 15 | resources.assets:2545586 | Enchanted Pumpkin Patch / Victory | NotInEventPool | Rare (2) | 1.0 | MELHORAR | wording |
| 16 | resources.assets:2545594 | Foreboding Gem - Victory | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 17 | resources.assets:2545575 | Gold Lootin' Goblins | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 18 | resources.assets:2545600 | Gold Statue of the First Mountain King / Victory | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 19 | resources.assets:2545605 | Hell Coffer / Victory | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 20 | resources.assets:2545607 | Hell Gate / Victory | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |
| 21 | resources.assets:2545610 | Horn of Glorious Battle / Victory | NotInEventPool | Common (0) | 1.0 | MELHORAR | wording |

## 15 — Enchanted Pumpkin Patch — resources.assets:2545586

VEREDITO PROPOSTO: MELHORAR — wording. Manter Enchanted Pumpkin; nenhum buff numérico novo.

Campo original `campos_originais.promptToSelectCharacter`, CAMPO atual: `Dare to open the Cursed Chest?`
PROPOSTA EXATA: `Who will claim an Enchanted Pumpkin?`
Justificativa: prompt reaproveitado de outra cena. Narrativa e opção Take já são coerentes com o status configurado; não precisam de uma reescrita por estética.

Anomalias/limites: `disabled=0`; 1 opção sem ocultação; resultado global vazio. Enchanted Pumpkin (`resources.assets:2545436`) é Fortune/Permanent, descrição contém `[0]`, fórmulas HealthPerTurn/ManaPerTurn `12`; preservar token e não anunciar valor final. Razão XP=2.0 com dar=false NÃO é prêmio de XP ativo. Referência Cursed Chest Battle (`resources.assets:2544645`) e inimigo forçado residual existem, mas batalha.iniciar=false; não provar combate errado nem mudar referência. Entrada `resources.assets:2545587`. NAO_EXERCITADO: seleção do personagem, aplicação da Fortune, regeneração efetiva e UI.

## 16 — Foreboding Gem - Victory — resources.assets:2545594

VEREDITO PROPOSTO: MELHORAR — wording; recompensa e risco permanecem como configurados. A proposta distingue adquirir a carga de usar seu efeito.

Campo `texto`, TRECHO atual: `Your opponents lay strewn around you`
PROPOSTA EXATA: `Your opponents lie strewn around you`
Campo opção 1 `texto`, CAMPO atual: `You'll be the one to hold the Ruby.`
PROPOSTA EXATA: `Claim Ruby of Rancor. Its charge grants 3 extra Action Points and reduces Mana Costs, but its effect makes you die at the end of your turn.`
Justificativa: concordância temporal e informação de risco omitida pela opção. A descrição autoral de Ruby of Rancor (`resources.assets:2545465`) declara 1 charge, 3 extra Action Points, redução de Mana Costs e morte ao fim do turno. Não inventar o valor de redução de mana, não dizer que o simples ato de pegar o Ruby mata e não remover a morte.

Anomalias/limites: `disabled=0`; 1 opção sem ocultação; resultado global e promptToSelectCharacter vazios. Status Fortune/Permanent e sortear=false; ausência de modificadores de atributo no resumo não prova ausência do efeito da carga. Batalha/encadeamento nulos, batalha não inicia. Entrada `resources.assets:2545595`. NAO_EXERCITADO: concessão e uso da carga, ação ativável, AP/custo efetivo e morte. A nova descrição é proposta documental ancorada na descrição do catálogo, não teste do efeito.

## 17 — Gold Lootin' Goblins — resources.assets:2545575

VEREDITO PROPOSTO: MELHORAR — wording. Manter a missão do First Mountain King, os inimigos e a escolha Leave.

Campo `texto`, TRECHO atual: `treasures that sparkled and gleam in the dim torchlight.`
PROPOSTA EXATA: `treasures that sparkle and gleam in the dim torchlight.`
Campo `texto`, TRECHO atual: `danced in a frenzy of glee`
PROPOSTA EXATA: `dance in a frenzy of glee`
Campo opção 1 `texto`, CAMPO atual: `Destroy these goblins in the name of the First Mountain King`
PROPOSTA EXATA: `Destroy these goblins in the name of the First Mountain King.`
Campo opção 2 `texto`, CAMPO atual: `""` (string vazia).
PROPOSTA EXATA: `Leave the goblins and abandon this confrontation.`
Campo original `campos_originais.promptToSelectCharacter`, CAMPO atual: `Who will listen to his pleas?`
PROPOSTA EXATA: `Who will confront the goblins?`
Justificativa: manter presente consistente, pontuação, esclarecer opção vazia e remover prompt sem súplica. Não prometer saída sem consequência universal: só descrever afastamento, conforme texto da ação.

Anomalias/limites: `disabled=0`; 2 opções sem ocultação; resultado global e descrição Leave vazios. KeepInDeckWhenUsed=1 preservado. Fight inicia batalha, PPtr de batalha NULL, 6 inimigos forçados e vitória `resources.assets:2545574`. `NameOverride` Volcanus/Burnicus aparece com OverrideEnemyName=0: dado residual, não prova que goblins terão esses nomes. Leave não inicia batalha e não tem status candidato no efeito padrão. Entrada no catálogo: EventStatus `resources.assets:2545511`, Dwarf Rage!, `data.ForcedEventBeforeBoss`; registro no ListHolderEvents NÃO equivale a uma partida que exerceu o evento. NAO_EXERCITADO: spawn forçado, saída, combate e nome efetivo dos inimigos.

## 18 — Gold Statue of the First Mountain King — resources.assets:2545600

VEREDITO PROPOSTO: MELHORAR — wording. NÃO adicionar ouro ao efeito nem fixar o loot em 3 itens. A divergência entre título e dados é sinalizada, não consertada com recompensa inventada.

Campo `texto`, TRECHO atual: `Silence fills the chamber, the only sound is your own labored breathing.`
PROPOSTA EXATA: `Silence fills the chamber; the only sound is your own labored breathing.`
Campo opção 1 `titulo`, CAMPO atual: `Claim the gold`
PROPOSTA EXATA: `Claim the statue's spoils`
Campo original `campos_originais.promptToSelectCharacter`, CAMPO atual: `Does anyone owe this Ogre money?`
PROPOSTA EXATA: `Who will claim the statue's spoils?`
Justificativa: corrigir comma splice e não prometer moeda quando ouro.dar=false. O efeito dá itens com tabela inline de peças da estátua. Catálogo identifica Gold Statue Arm (`resources.assets:2546476`), Head (`resources.assets:2546477`) e Torso (`resources.assets:2546478`). “Spoils” não inventa moeda nem resultado final específico.

Anomalias/limites: `disabled=0`; 1 opção sem ocultação; descrição da opção, ação e resultado global vazios. Itens.dar=true, pool Unassigned, quantidade_configurada=0, uma tabela com 3 entradas Chance=100.0 e mustGetOne=0. O ZERO aqui é parâmetro autoral real, NÃO um NULL convertido e NÃO prova de loot final vazio. A tabela inline impede concluir “0 itens” apenas por itemCount. Não interpretar as 3 chances como resultado final exercitado. Batalha da ação inativa; referências batalha/encadeamento NULL. Entradas: `resources.assets:2545601` e BattleInfo `resources.assets:2544646`. NAO_EXERCITADO: peças sorteadas, eventual venda/valor monetário e quantidade efetiva.

## 19 — Hell Coffer — resources.assets:2545605

VEREDITO PROPOSTO: MELHORAR — wording. Manter a escolha entre Enchant Shadow e Enchant Holy e as escalas autorais.

Campo `texto`, TRECHO atual: `slows finally coming to a stop.`
PROPOSTA EXATA: `slows, finally coming to a stop.`
Campo `texto`, TRECHO atual: `A soft click echos as it unlocks`
PROPOSTA EXATA: `A soft click echoes as it unlocks`
Campo original `campos_originais.promptToSelectCharacter`, CAMPO atual: `Does anyone owe this Ogre money?`
PROPOSTA EXATA: `Who will receive the chosen enchantment?`
Campo opção 1 `texto`, CAMPO atual: `""` (string vazia).
PROPOSTA EXATA: `Gain Enchant Shadow.`
Campo opção 2 `texto`, CAMPO atual: `""` (string vazia).
PROPOSTA EXATA: `Gain Enchant Holy.`
Justificativa: pontuação/ortografia e explicação mínima das duas opções vazias. Os candidatos são fixos: Enchant Shadow (`resources.assets:2545435`) e Enchant Holy (`resources.assets:2545434`), Fortune/Permanent; a descrição autoral concede Enchant correspondente com @level@ `{1,30}`. Não fixar nível nem introduzir um item físico.

Anomalias/limites: `disabled=0`; 2 opções sem ocultação; 2 descrições e 2 textos de ação vazios. Descrições de ambos os EventStatus têm fechamento de tags `<i><color...>...</i></color>` fora de ordem; sinalizar sem editar status compartilhados. Nenhuma ação inicia batalha e PPtrs de batalha/encadeamento são nulos. Entrada `resources.assets:2545606`. NAO_EXERCITADO: aprendizado, escala final dos enchantments e seleção de personagem.

## 20 — Hell Gate — resources.assets:2545607

VEREDITO PROPOSTO: MELHORAR — wording. Manter Soul of Fire e seu custo; não criar opção de recusa nesta proposta.

Campo original `campos_originais.promptToSelectCharacter`, CAMPO atual: `Who if any will take his soul?`
PROPOSTA EXATA: `Who will take his soul?`
Campo opção 1 `texto`, CAMPO atual: `Take the <red><b><incr>Soul of Lord Infernicus</incr></b></red>.`
PROPOSTA EXATA: `Take the <red><b><incr>Soul of Lord Infernicus</incr></b></red> and gain Soul of Fire. It increases Fire Damage, but each stack of Heat reduces Healing Received by 5%.`
Justificativa: há 1 opção e nenhuma Leave no asset; remover “if any” evita sugerir recusa que não está configurada nas opções (a UI pode permitir outra saída, NAO_EXERCITADO). Explicitar o custo declarado no status `resources.assets:2545472`, Soul of Fire, sem preencher `{6,30}` como dano final e sem alterar o custo.

Anomalias/limites: `disabled=0`; 1 opção sem ocultação; resultado global e texto de ação vazios. Fortune/Permanent, sortear=false; descrição autoral declara Fire Damage `{6,30}` e -5% de Healing Received por stack de Heat. Configuração residual de inimigo `resources.assets:2545159` com iniciar=false; referência de batalha NULL. Entrada `resources.assets:2545608`. NAO_EXERCITADO: seleção, aplicação da Fortune, escalas e interação Heat/healing. A proposta não certifica a implementação do status.

## 21 — Horn of Glorious Battle — resources.assets:2545610

VEREDITO PROPOSTO: MELHORAR — wording. Manter experiência dar=true/razão=1.0; não prometer um número fixo de XP.

Campo `texto`, TRECHO atual: `you bare numerous injuries.`
PROPOSTA EXATA: `you bear numerous injuries.`
Campo opção 1, ação 1 `texto`, CAMPO atual: `Victory has left you sharper, stronger, and  more experienced. ` (2 espaços após and e espaço final).
PROPOSTA EXATA: `Victory has left you sharper, stronger, and more experienced.`
Campo original `campos_originais.promptToSelectCharacter`, CAMPO atual: `Who will listen to his pleas?`
PROPOSTA EXATA: `Who will claim the victory reward?`
Justificativa: bear/bare, espaços duplicados e prompt sem conexão com o desfecho. Não trocar prêmio por Fortune: LeadsToFortune=0 e nenhum candidato de status nesse efeito. Não acrescentar quantidade de XP à descrição vazia.

Anomalias/limites: `disabled=0`; 1 opção sem ocultação; descrição da opção e resultado global vazios. XP.dar=true, razão=1.0, quantidade_final=NULL. XP pode converter-se em ouro no roguelike/party nível 30, conforme motivo de `eventos.json` e `schema.md`; não declarar XP efetivo garantido nem preencher com 0. Batalha inativa, PPtrs de batalha/encadeamento nulos. Entrada `resources.assets:2545611`. NAO_EXERCITADO: XP/possível conversão em ouro, alvo final, distribuição e UI.

Contagem desta parte: 7 eventos, 7 MELHORAR (wording), 0 MANTER; 0 propostas de mudança de recompensa e 0 de condição. Aprovação PENDENTE para as 7 chaves. O total consolidado e os testes aparecem na parte04.
