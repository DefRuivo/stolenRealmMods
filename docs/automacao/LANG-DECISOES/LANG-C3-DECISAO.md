# LANG-C3 — DECISÃO

Templates/variáveis: 1013 IDs cobertos nas 42 partes do lote concluído C3-A; 37 mudanças propostas e 976 MANTER recontados (o handoff diz 973 MANTER; divergência abaixo).

## Leitura curta

33 ajustes só reordenam habilidade/nível, conservando macros e chance/gatilho. Dois corrigem concordância; um explicita “1 de Alcance”; um traduz “Appearance”. Não há comprovação de variável vazando na tela. LANG-01184 também aparece no C2 com os mesmos antes/depois: é uma única mudança, não duas aplicações.

## Opções e custo

- APROVAR TUDO: aceitar os 37 textos exatos conferidos abaixo; custo: escolher explicitamente a versão C3 ou C5 de LANG-00053 e validar composição, macros e layout depois. A divergência de contagem não foi apagada e aprovação documental não demonstra runtime.
- APROVAR SUBCONJUNTO: separar os 33 de ordem habilidade/nível, os dois de concordância, o de sentido ou o rótulo; também é possível aprovar por ID. Custo: registrar precisamente grupos/IDs aceitos e reapresentar os adiados. LANG-01184 exige conciliação com C2, não duplicação.
- REPROVAR: conservar os templates atuais; custo: as redações e o “1” omitido permanecem, exigindo nova proposta se desejado. MANTER não pede aprovação individual (comentário806 do gate).

## Grupos — IDs completos

concordância: uma torrente: LANG-00053
sentido: explicitar 1 de alcance: LANG-00309
ordem habilidade/nível: LANG-00315, LANG-00318, LANG-00320, LANG-00321, LANG-00322, LANG-00323, LANG-00324, LANG-00327, LANG-00328, LANG-00329, LANG-00330, LANG-00331, LANG-00335, LANG-00338, LANG-00339, LANG-00340, LANG-00345, LANG-00346, LANG-00347, LANG-00348, LANG-00358, LANG-00359, LANG-00362, LANG-00363, LANG-00366, LANG-00377, LANG-00386, LANG-01194, LANG-01195, LANG-01196, LANG-03625, LANG-03637, LANG-03885
concordância: espírito sentido: LANG-00425
tradução de rótulo Appearance: LANG-01184

## Itens que mudam — literais

ID | ATUAL | PROPOSTA | natureza. Aspas/escapes usam JSON para preservar a string inteira, inclusive CR/LF, tags e espaços. ATUAL é o snapshot LANG-R1, não leitura de tela. Alvo: campo selecionado offline (selecao_estatica) da entrada pt-BR correspondente; não editar chave/en, campos de gênero, outras entradas nem identificadores dentro das macros.

LANG-00053 | "Ah. Sim, eu definitivamente sou um anão. Eu sou baixo e irritado! [name] grita, fingindo indignação.\n\nO chão sob seus pés começa a tremer de forma ameaçadora. A imensa barba de pedra da estátua do anão se move, a boca intricadamente esculpida desliza aberta para revelar um abismo escancarado. De repente, um torrente de aço derretido jorra da boca do anão, o fogo líquido e brilhante derramando-se no chão diante de você!" | "Ah. Sim, eu definitivamente sou um anão. Eu sou baixo e irritado! [name] grita, fingindo indignação.\n\nO chão sob seus pés começa a tremer de forma ameaçadora. A imensa barba de pedra da estátua do anão se move, a boca intricadamente esculpida desliza aberta para revelar um abismo escancarado. De repente, uma torrente de aço derretido jorra da boca do anão, o fogo líquido e brilhante derramando-se no chão diante de você!" | concordância: uma torrente
LANG-00309 | "Alcance de Habilidade por [stat value] de Int (Máx. 3)" | "1 de Alcance de Habilidade a cada [stat value] de Int (Máx. 3)" | sentido: explicitar 1 de alcance
LANG-00315 | "10% de chance de aplicar Nível [level value] {SKL=Immolate} ao acertar." | "10% de chance de aplicar {SKL=Immolate} de nível [level value] ao acertar." | ordem habilidade/nível
LANG-00318 | "10% de chance de lançar Nível [level value] {SKL=Blinding Light} ao acertar com qualquer habilidade." | "10% de chance de lançar {SKL=Blinding Light} de nível [level value] ao acertar com qualquer habilidade." | ordem habilidade/nível
LANG-00320 | "10% de chance de conjurar Nível [level value] {SKL=Blinding Light} quando atingido." | "10% de chance de conjurar {SKL=Blinding Light} de nível [level value] quando atingido." | ordem habilidade/nível
LANG-00321 | "10% de chance de conjurar Nível [level value] {SKL=Curse} ao atacar." | "10% de chance de conjurar {SKL=Curse} de nível [level value] ao atacar." | ordem habilidade/nível
LANG-00322 | "10% de chance de conjurar Nível [level value] {SKL=Frost Shard} ao acertar." | "10% de chance de conjurar {SKL=Frost Shard} de nível [level value] ao acertar." | ordem habilidade/nível
LANG-00323 | "10% de chance de lançar Nível [level value] {SKL=Howl} quando atingido." | "10% de chance de lançar {SKL=Howl} de nível [level value] quando atingido." | ordem habilidade/nível
LANG-00324 | "10% de chance de lançar Nível [level value] {SKL=Ice Lance} ao atacar." | "10% de chance de lançar {SKL=Ice Lance} de nível [level value] ao atacar." | ordem habilidade/nível
LANG-00327 | "10% de chance de conjurar Nível [level value] {SKL=Reaper's Scythe} ao atacar." | "10% de chance de conjurar {SKL=Reaper's Scythe} de nível [level value] ao atacar." | ordem habilidade/nível
LANG-00328 | "10% de chance de conjurar Nível [level value] {SKL=Slam} ao atacar." | "10% de chance de conjurar {SKL=Slam} de nível [level value] ao atacar." | ordem habilidade/nível
LANG-00329 | "10% de chance de lançar Nível [level value] {SKL=Spectral Chains} ao atacar. 10% de chance de lançar Nível [level value] {SKL=Blind} ao atacar." | "10% de chance de lançar {SKL=Spectral Chains} de nível [level value] ao atacar. 10% de chance de lançar {SKL=Blind} de nível [level value] ao atacar." | ordem habilidade/nível
LANG-00330 | "10% de chance de conjurar Nível [level value] {SKL=Stunning Slam} ao atacar." | "10% de chance de conjurar {SKL=Stunning Slam} de nível [level value] ao atacar." | ordem habilidade/nível
LANG-00331 | "10% de chance de conjurar Nível [level value] {SKL=Thunder Bolt} ao atacar." | "10% de chance de conjurar {SKL=Thunder Bolt} de nível [level value] ao atacar." | ordem habilidade/nível
LANG-00335 | "10% de chance de ativar um Nível [level value] {SKL=Thunder Bolt} ao acertar com qualquer habilidade." | "10% de chance de ativar {SKL=Thunder Bolt} de nível [level value] ao acertar com qualquer habilidade." | ordem habilidade/nível
LANG-00338 | "10% de chance, ao ser atingido, de conjurar Nível [level value] {SKL=Shield of Light}." | "10% de chance, ao ser atingido, de conjurar {SKL=Shield of Light} de nível [level value]." | ordem habilidade/nível
LANG-00339 | "10% de chance ao ser atingido de conjurar Nível [level value] {SKL=Mass Cure}." | "10% de chance ao ser atingido de conjurar {SKL=Mass Cure} de nível [level value]." | ordem habilidade/nível
LANG-00340 | "10% de chance ao ser atingido de lançar Nível [level value] {SKL=Burning Ground}." | "10% de chance ao ser atingido de lançar {SKL=Burning Ground} de nível [level value]." | ordem habilidade/nível
LANG-00345 | "15% de chance de conjurar Nível [level value] {SKL=Chain Lightning} ao atacar com esta arma." | "15% de chance de conjurar {SKL=Chain Lightning} de nível [level value] ao atacar com esta arma." | ordem habilidade/nível
LANG-00346 | "15% de chance de conjurar Nível [level value] {SKL=Detonate} ao atacar." | "15% de chance de conjurar {SKL=Detonate} de nível [level value] ao atacar." | ordem habilidade/nível
LANG-00347 | "15% de chance de conjurar Nível [level value] {SKL=Fracture} ao atacar." | "15% de chance de conjurar {SKL=Fracture} de nível [level value] ao atacar." | ordem habilidade/nível
LANG-00348 | "15% de chance de lançar Nível [level value] {SKL=Frost Nova} ao acertar com qualquer habilidade." | "15% de chance de lançar {SKL=Frost Nova} de nível [level value] ao acertar com qualquer habilidade." | ordem habilidade/nível
LANG-00358 | "20% de chance de conjurar Nível [level value] {SKL=Breath of Winter} ao atacar." | "20% de chance de conjurar {SKL=Breath of Winter} de nível [level value] ao atacar." | ordem habilidade/nível
LANG-00359 | "20% de chance de lançar Nível [level value] {SKL=Burning Ground} ao acertar com qualquer habilidade." | "20% de chance de lançar {SKL=Burning Ground} de nível [level value] ao acertar com qualquer habilidade." | ordem habilidade/nível
LANG-00362 | "20% de chance de conjurar Nível [level value] {SKL=Raise Servant of Abaddon} na morte do inimigo." | "20% de chance de conjurar {SKL=Raise Servant of Abaddon} de nível [level value] na morte do inimigo." | ordem habilidade/nível
LANG-00363 | "20% de chance de conjurar Nível [level value] {SKL=Reaper's Scythe} ao atacar." | "20% de chance de conjurar {SKL=Reaper's Scythe} de nível [level value] ao atacar." | ordem habilidade/nível
LANG-00366 | "25% de chance, quando atingido, de lançar Nível [level value] {SKL=Ankheg Spines}." | "25% de chance, quando atingido, de lançar {SKL=Ankheg Spines} de nível [level value]." | ordem habilidade/nível
LANG-00377 | "5% de chance de lançar Nível [level value] {SKL=Thunder Bolt} ao atingir um inimigo com qualquer habilidade.\n\n5% de chance de lançar Nível [level value] {SKL=Frost Nova} ao atingir um inimigo com qualquer habilidade.\n\n5% de chance de lançar Nível [level value] {SKL=Fireball} ao atingir um inimigo com qualquer habilidade." | "5% de chance de lançar {SKL=Thunder Bolt} de nível [level value] ao atingir um inimigo com qualquer habilidade.\n\n5% de chance de lançar {SKL=Frost Nova} de nível [level value] ao atingir um inimigo com qualquer habilidade.\n\n5% de chance de lançar {SKL=Fireball} de nível [level value] ao atingir um inimigo com qualquer habilidade." | ordem habilidade/nível
LANG-00386 | "8% de chance ao atacar de conjurar Nível [level value] {SKL=Shock}." | "8% de chance ao atacar de conjurar {SKL=Shock} de nível [level value]." | ordem habilidade/nível
LANG-00425 | "<b>Recuperação de Mana</b> aumentada em [0].\n\n<i><color=#808080>\"Invisível, porém sentida, o espírito dança como uma chama ao vento, um sussurro do mundo invisível que ecoa em nossos corações.\"\n</i></color>" | "<b>Recuperação de Mana</b> aumentada em [0].\n\n<i><color=#808080>\"Invisível, porém sentido, o espírito dança como uma chama ao vento, um sussurro do mundo invisível que ecoa em nossos corações.\"\n</i></color>" | concordância: espírito sentido
LANG-01184 | "Appearance: [item name]" | "Aparência: [item name]" | tradução de rótulo Appearance
LANG-01194 | "Aplica Nível [level value] {SKL=Fire Shield} quando atingido." | "Aplica {SKL=Fire Shield} de nível [level value] quando atingido." | ordem habilidade/nível
LANG-01195 | "Aplica Nível [level value] {SKL=Frost Armor} quando atingido." | "Aplica {SKL=Frost Armor} de nível [level value] quando atingido." | ordem habilidade/nível
LANG-01196 | "Aplica Nível [level value] {SKL=Lightning Shield} quando atingido." | "Aplica {SKL=Lightning Shield} de nível [level value] quando atingido." | ordem habilidade/nível
LANG-03625 | "Ganhe Armadura e Armadura Mágica iguais a 2x o seu Poder. 10% de chance, ao ser atingido, de conjurar Nível [level value] {SKL=Pain Suppression}." | "Ganhe Armadura e Armadura Mágica iguais a 2x o seu Poder. 10% de chance, ao ser atingido, de conjurar {SKL=Pain Suppression} de nível [level value]." | ordem habilidade/nível
LANG-03637 | "Ganhe Nível [level value] {SKL=Enchant Fire}.\nGanhe Nível [level value] {SKL=Enchant Cold}.\nGanhe Nível [level value] {SKL=Enchant Lightning}." | "Ganhe {SKL=Enchant Fire} de nível [level value].\nGanhe {SKL=Enchant Cold} de nível [level value].\nGanhe {SKL=Enchant Lightning} de nível [level value]." | ordem habilidade/nível
LANG-03885 | "Concede a habilidade passiva {SKL=Glory}. Ganha Nível [level value] {SKL=Enchant Fire} ao segurar esta arma." | "Concede a habilidade passiva {SKL=Glory}. Ganha {SKL=Enchant Fire} de nível [level value] ao segurar esta arma." | ordem habilidade/nível

## O que não é decisão aqui

Aplicar no dataset, reconciliar mudanças repetidas entre gates, rebuild, testes de gênero/macros/layout, deploy e publicação cabem ao agente depois em escopo autorizado. Não alteramos os catálogos, entregas, decisões humanas ou t_0bddb861. Se houver wording pessoal diferente do ATUAL, preservar o vigente e reapresentar.

## Divergências — os dois lados

- Cartão t_0d1c5584, handoffs1050/1280, comentário859 e inventario-consolidado: “1013”, “973 MANTER” e “37 PROPOR_ALTERACAO”. Recontagem das42 partes: 976 MANTER e37 PROPOR_ALTERACAO, total1013. Os973 são as linhas com formato novo entre parênteses; parte01 tem mais três MANTER explícitos sem parênteses: LANG-00003, LANG-00004, LANG-00005. Não alterei o cartão nem seu inventário.
- Handoff1271 alterna resumo973 MANTER com metadata mantes=976; a recontagem literal acima expõe ambos, sem esconder a inconsistência.
- Handoff01/comment726 era parcial: 200/1013,34 mudanças e813 restantes. Material posterior tem42 partes/1013 IDs e37 mudanças. O snapshot parcial não é prova de pendência atual; os recibos verificacao01/02 ainda se referem ao recorte inicial (o teste se chama first200_exact), não validam sozinhos as1013 linhas.
- Workspace original t_0d1c5584 não está disponível; o cartão só tem inventário e handoff anexos. Recuperação verificável: pacote durável BP-3, que preservou52 membros do live-workspace original. Inventário consolidado recuperado é byte-idêntico ao anexo do C3. Isto comprova o snapshot preservado e suas strings, não possíveis edições posteriores à captura.
- Os dois JSONs auxiliares somam813 registros (200+613); as200 linhas do lote02 continuam conferíveis nas partes10–17. Não reconstruí propostas ausentes do JSON por inferência: li os literais do Markdown e confrontei todos os1013 ATUAIS/chaves ao canônico.
- Sobreposição: LANG-01184 C2/C3 tem proposta idêntica; uma entrada de produto.
- C3/C5, LANG-00053: esta proposta C3 corrige apenas concordância; a alternativa C5 também encurta a narrativa e acrescenta delimitadores da fala. São alternativas diferentes para o mesmo ATUAL: escolher explicitamente uma, sem merge automático. O texto C3 está na lista acima; a alternativa C5 literal é:
"\"Ah. Sim, sou mesmo um anão. Sou baixo e irritado!\" [name] grita, fingindo indignação.\n\nO chão sob seus pés treme ameaçadoramente. A imensa barba de pedra da estátua do anão se move, e a boca esculpida se abre como um abismo. De repente, uma torrente de aço derretido jorra da boca, derramando fogo líquido e brilhante no chão diante de você!"

## Fontes e prova

Canônico: C:/Users/Pichau/AppData/Local/hermes/kanban/attachments/t_2a6474ff/LANG-R1-entrega-final.zip :: entrega02/localizacao-ptbr.json; união dos CSVs revisao-placeholders/revisao-integridade; SHA-256 4d509f13280cd9e210593cfce08420dd8e48a75b4261f9faefee2e6afb6bf161.
Propostas recuperadas: C:/Users/Pichau/AppData/Local/hermes/kanban/attachments/t_739c6068/BETTERPORTUGUESE-BP3-CORRIGIDO.zip :: sources/LANG-proposals/t_0d1c5584/live-workspace/LANG-C3-propostas-parte01.md..parte42.md; SHA-256 028a88af4b4a6de417ee22504a4a5d9772e0978893a1e6510b1b9ba75e7b11b5.
Inventário anexo: C:/Users/Pichau/AppData/Local/hermes/kanban/attachments/t_0d1c5584/LANG-C3-inventario-consolidado.json; SHA-256 6c9c4ba0f55d97a7ddb2c3e7054bfea3a5db66ebe8993867244f0c5502261a68.
Recibos lidos no mesmo prefixo: LANG-C3-verificacao01.json, LANG-C3-verificacao02.json e LANG-C3-pacote-verificacao01.json. Resultados de20 testes são históricos e parciais; nesta rodada conferi seleção,1013 chaves/ATUAIS, decisões e37 pares de proposta ao material recuperado. Não alegar testes de jogo.
NAO_EXERCITADO: runtime, gênero, visibilidade, consumo de variáveis/macros, layout, aprovação do dono e implementação. Presença de marcador e entrada nula secundária são informativas, não defeito confirmado.
Nenhum dos37 pares ficou sem conferência documental; isso não resolve as limitações de runtime nem a divergência de contagem do handoff.
