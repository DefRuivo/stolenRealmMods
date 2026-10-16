# LANG-C2 — DECISÃO

Textos pt-BR iguais ao inglês: 268 candidatos cobertos por três lotes concluídos; 29 propostas de tradução e 239 MANTER.

## Leitura curta

29 mudanças: 11 no b01, sete no b02, 11 no b03. Duas merecem decisão separada: LANG-00488 escolhe “Bucha de Canhão Fanática” para Fodder, sem harmonizar a família inteira; LANG-05221 propõe “Ímpeto III” por inferência da família, sem auxiliar direto. Os demais nomes/termos, rótulos e cinco descrições estão separados abaixo. MANTER é aprovado por padrão (comentário805 do gate), não precisa de revisão item a item.

## Opções e custo

- APROVAR TUDO: aceitar as 29 redações literais; custo: assumir também a escolha editorial de Fodder e a inferência de Momentum III, além da validação posterior de layout/variáveis.
- APROVAR SUBCONJUNTO: escolher lote, natureza ou IDs; recorte simples = 27 propostas, adiando LANG-00488 e LANG-05221. Custo: nova decisão para esses dois e consistência familiar ainda não resolvida fora do escopo.
- REPROVAR: nenhuma das 29 entra; custo: inglês permanece e uma nova rodada editorial será necessária.

## Itens que mudam — literais

ID | ATUAL | PROPOSTA | natureza. Aspas e escapes são JSON: \n/\r conservam controles; não são caracteres a inserir. ATUAL é o dump canônico, não a tela ou o estado instalado. Chaves/identificadores/tokens ingleses não são alvos de alteração.

### b01
LANG-00488 | "<color=#00FFFF>Fanatical Fodder II</color>" | "<color=#00FFFF>Bucha de Canhão Fanática II</color>" | terminologia editorial Fodder
LANG-00490 | "<color=#00FFFF>Lethal Life II</color>" | "<color=#00FFFF>Vida Letal II</color>" | tradução de nome/termo
LANG-01184 | "Appearance: [item name]" | "Aparência: [item name]" | tradução de rótulo/notificação
LANG-01853 | "Casting [action name]" | "Conjurando [action name]" | tradução de rótulo/notificação
LANG-03339 | "Fire Gi" | "Gi de Fogo" | tradução de nome/termo
LANG-03499 | "Frenzy" | "Frenesi" | tradução de nome/termo
LANG-03635 | "Gain Level [level value] {SKL=Enchant Cold}." | "Recebe {SKL=Enchant Cold} de nível [level value]." | tradução de descrição com variáveis
LANG-03636 | "Gain Level [level value] {SKL=Enchant Fire}." | "Recebe {SKL=Enchant Fire} de nível [level value]." | tradução de descrição com variáveis
LANG-03638 | "Gain Level [level value] {SKL=Enchant Lightning}." | "Recebe {SKL=Enchant Lightning} de nível [level value]." | tradução de descrição com variáveis
LANG-03668 | "Game name" | "Nome da partida" | tradução de rótulo/notificação
LANG-03693 | "General" | "Geral" | tradução de rótulo/notificação
### b02
LANG-04844 | "Lethal Life I" | "Vida Letal I" | tradução de nome/termo
LANG-05108 | "Max" | "Máximo" | tradução de rótulo/notificação
LANG-05220 | "Momentum II" | "Ímpeto II" | tradução de nome/termo
LANG-05221 | "Momentum III" | "Ímpeto III" | nome de habilidade; inferência familiar
LANG-05276 | "Movement Per A P" | "Movimento por A P" | tradução de rótulo/notificação
LANG-05608 | "Pending..." | "Pendente..." | tradução de rótulo/notificação
LANG-05687 | "Player [player number]" | "Jogador [player number]" | tradução de rótulo/notificação
### b03
LANG-06516 | "Shako" | "Chacó" | tradução de nome/termo
LANG-06969 | "Stormbringer I" | "Tempestade I" | tradução de nome/termo
LANG-07621 | "The wearer gains Level [level value] {SKL=Aura of Flame}." | "O portador ganha {SKL=Aura of Flame} no nível [level value]." | tradução de descrição com variáveis
LANG-07622 | "The wearer gains Level [level value] {SKL=Fire Shield}." | "O portador ganha {SKL=Fire Shield} no nível [level value]." | tradução de descrição com variáveis
LANG-07730 | "Tier [tier value]:" | "Nível [tier value]:" | tradução de rótulo/notificação
LANG-07894 | "Ultra Backers" | "Ultra Apoiadores" | tradução de rótulo/notificação
LANG-08086 | "Warhammer" | "Martelo de Guerra" | tradução de nome/termo
LANG-08090 | "Warmonger I" | "Belicista I" | tradução de nome/termo
LANG-08091 | "Warmonger II" | "Belicista II" | tradução de nome/termo
LANG-08381 | "Xotec Flayer" | "Esfolador Xotec" | tradução de nome/termo
LANG-08632 | "You sent [player name] [item name]" | "Você enviou para [player name]: [item name]" | tradução de rótulo/notificação

## Grupos por natureza — todos os IDs

terminologia editorial Fodder: LANG-00488
tradução de nome/termo: LANG-00490, LANG-03339, LANG-03499, LANG-04844, LANG-05220, LANG-06516, LANG-06969, LANG-08086, LANG-08090, LANG-08091, LANG-08381
tradução de rótulo/notificação: LANG-01184, LANG-01853, LANG-03668, LANG-03693, LANG-05108, LANG-05276, LANG-05608, LANG-05687, LANG-07730, LANG-07894, LANG-08632
tradução de descrição com variáveis: LANG-03635, LANG-03636, LANG-03638, LANG-07621, LANG-07622
nome de habilidade; inferência familiar: LANG-05221

## O que não é decisão aqui

Aplicação no dataset, rebuild, teste de composição/variáveis e layout, instalação e publicação são trabalho posterior do agente em tarefa autorizada. Não gravamos decisão_dono/texto_aprovado nem desbloqueamos t_15176486. Se o texto vigente for diferente do ATUAL, preservar o wording pessoal e reapresentar; não sobrescrever.

## Divergências e limites

- Contagens e strings dos cartões versus propostas/recibos conferem: 11+7+11 mudanças, 69+93+77 MANTER. Nenhuma divergência de antes/depois encontrada. Todos os 29 pares conferidos documentalmente; runtime/layout/consumo de variáveis NAO_EXERCITADO.
- b01, LANG-00488: o próprio artefato aponta a família existente “Fanático Fodder” (LANG-00474/LANG-00634), enquanto propõe “Bucha de Canhão Fanática II”. Ambos os lados expostos: não harmonizei a família nem escolhi wording novo.
- b01, LANG-01260/Arrown (MANTER): errata01 corrige a descrição de contexto da parte02: não item-name, mas duas referências Arrown-UI. Não há mudança de texto a aprovar nesse ID.
- b02, inventario01 versus inventario02/errata: nas posições126–130 a coluna Parte dizia07, a correção documental diz06. Partes e propostas JSON sempre guardaram os mesmos IDs/textos; nenhuma versão foi sobrescrita aqui.
- Snapshot b01 dizia188 pendentes porque era parcial; cartões b02/b03 estão agora done e foram lidos. Não é falta atual de cobertura.
- REV-2 t_9bfa4875 aprova C2-b02. A menção “b03 reprovado” no resumo desse revisor é EV-R2-NORMAL-b03-CORR (t_99925533), NÃO LANG-C2-b03 (t_523a4ff3), que tem revisão1275 aprovada. Não trocar as identidades dos cartões.

## Fontes e conferência

Canônico: C:/Users/Pichau/AppData/Local/hermes/kanban/attachments/t_2a6474ff/LANG-R1-entrega-final.zip :: entrega02/localizacao-ptbr.json; seleção entrega02/revisao-identicos.csv, 268 IDs ordenados; SHA-256 4d509f13280cd9e210593cfce08420dd8e48a75b4261f9faefee2e6afb6bf161.
Os caminhos docs/automacao citados abaixo são membros de ZIPs duráveis anexados, copiados para fontes/ no workspace. Propostas, inventários/erratas e recibos de pacote lidos. Suites herdadas constam dos recibos históricos; conferência nova aqui é identidade, seleção, strings e cópia literal, não novo teste do jogo.

b01, cartão t_3cf917f5: C:\Users\Pichau\AppData\Local\hermes\kanban\attachments\t_3cf917f5\LANG-C2-b01-entrega01.zip :: docs/automacao/LANG-C2-b01-propostas01.json
SHA-256 ad6c6076dfba6dd50ad178f5a5ea98c1e4e83dd4e6b07022a52e6f3f51ff7fbe
Recibo lido: C:\Users\Pichau\AppData\Local\hermes\kanban\attachments\t_3cf917f5\LANG-C2-b01-pacote-verificacao01.json

b02, cartão t_4bcea2cf: C:\Users\Pichau\AppData\Local\hermes\kanban\attachments\t_4bcea2cf\LANG-C2-b02-entrega01.zip :: docs/automacao/LANG-C2-b02-propostas01.json
SHA-256 b3570e897e11d6a2070396aada2dc99c9d34075e3d978b45bd72de584f0dd3c3
Recibo lido: C:\Users\Pichau\AppData\Local\hermes\kanban\attachments\t_4bcea2cf\LANG-C2-b02-pacote-verificacao01.json

b03, cartão t_523a4ff3: C:\Users\Pichau\AppData\Local\hermes\kanban\attachments\t_523a4ff3\LANG-C2-b03-entrega01.zip :: docs/automacao/LANG-C2-b03-propostas01.json
SHA-256 0f34380a0de7f5b2998f86b918af5b307d12b992ed0819ed6f32c8b553207467
Recibo lido: C:\Users\Pichau\AppData\Local\hermes\kanban\attachments\t_523a4ff3\LANG-C2-b03-pacote-verificacao01.json
