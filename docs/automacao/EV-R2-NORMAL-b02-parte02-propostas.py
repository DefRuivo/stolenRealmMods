#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Constroi o dado estruturado da correcao documental EV-R2-NORMAL-b02 (ordinais 21-40).

Saida: b02_data.json  (usado pelo gerador do .md e pela auditoria offline)
Fontes (somente leitura): docs/cobertura/EV-R1/{eventos.json,catalogo-referencias.json,lote-Normal-v2.md}
"""
import json, re, os

WS = os.path.dirname(os.path.abspath(__file__))
BASE = r"C:/dev/stolen-realm/docs/cobertura/EV-R1"
EV = json.load(open(os.path.join(BASE, 'eventos.json'), encoding='utf-8'))
FACTS = json.load(open(os.path.join(WS, 'EV-R2-NORMAL-b02-parte02-fatos.json'), encoding='utf-8'))
NORMAL = [e for e in EV['eventos'] if e['categoria'] == 'Normal']
SLICE = NORMAL[20:40]
F = {e['ordinal']: e for e in FACTS['events']}

def src(n):
    return SLICE[n - 21]

def fld(n, dotted):
    """valor exato de um campo por caminho relativo pontuado (listas por indice)."""
    cur = src(n)
    for part in dotted.split('.'):
        m = re.match(r'^([A-Za-z_]+)\[(\d+)\]$', part)
        if m:
            cur = cur[m.group(1)][int(m.group(2))]
        else:
            cur = cur[part]
    return cur

def JP(n, dotted):
    return "$.eventos[%d].%s" % (n, dotted)

def assert_eq(a, b, label):
    if a != b:
        raise SystemExit("ASSERT FAIL %s: %r != %r" % (label, a, b))

EVENTS = []

def ev(n, veredito, justificativa, estado, propostas, refutacoes, observacoes):
    EVENTS.append({
        'ordinal': n, 'veredito': veredito, 'justificativa': justificativa,
        'estado': estado, 'propostas': propostas, 'refutacoes': refutacoes,
        'observacoes': observacoes,
    })

def prop(rotulo, natureza, jsonpath, antes, depois, fundamento, tipo='campo'):
    return {'rotulo': rotulo, 'natureza': natureza, 'jsonpath': jsonpath, 'tipo': tipo,
            'antes': antes, 'depois': depois, 'fundamento': fundamento}

# ---------------------------------------------------------------- 21
assert_eq(fld(21, 'texto_resultados_possiveis'), '', '21 trp')
ev(21, 'MELHORAR',
   'Narrativa de abertura presente (80 caracteres, fala de Roland) e dois ramos jogaveis com status distintos; falta apenas o prompt de selecao que os eventos irmaos usam. Nao se propoe reativar o slot disabled.',
   'texto = <color=#7f2b0a><b>Roland:</b></color> "Go on!  Come at me and see what happens!" (80 ch); texto_resultados_possiveis = "" (vazio); 2 opcoes: "Laugh" (Self -> Curse of the Reaper 2545422; batalha iniciar=true, BattleInfo "Boss Fight - Roland" 2544644) e "Cower" (Self -> Endurance 2545438; mesma batalha). Nenhuma rolagem (bonus [], RollLimit 0) e nenhuma acao Failure em nenhuma das duas opcoes. disabled=1; raridade Common(0); peso 1.0; NodeType Event(7); LeadsToFortune=1.',
   [prop('PROPOSTA DE CONTEUDO', 'texto de prompt ausente', JP(21, 'texto_resultados_possiveis'), '',
         'What will you do?',
         'O literal "What will you do?" ja e usado pelos eventos 26, 27, 28 e 36 desta mesma faixa; o 21 e o unico dos cinco eventos que iniciam batalha (21, 25, 26, 27, 29) sem prompt de selecao. Sem efeito de jogo: campo e apenas texto de interface.')],
   ['parte01: "EVT 21 ... RARIDADE: Boss - Peso: 0.1" -> falso. 21 e Common(0) com peso 1.0 (raridade.valor=0, peso=1.0).',
    'parte01: "texto = (vazio)" -> falso. O texto tem 80 caracteres (fala de Roland).',
    'parte01: "1 unica opcao (FIGHT)" -> falso. Sao 2 opcoes: Laugh e Cower.',
    'parte01: chave resources.assets:2545402 -> falso. A chave real e resources.assets:2545552 (id 00336dd6-9e0d-4a6a-ae09-a285d9a259be).',
    'parte01: "apenas Success (RollLimit 15) ... sem Failure" -> falso quanto ao limite (RollLimit 0 em ambas as acoes) e quanto a inexistencia de Failure ser defeito: com limiar 0 nao existe ramo de falha a exigir.'],
   ['O efeito da opcao 1 e "Curse of the Reaper": StatusType Fortune(1), "Increases Life Steal by 6%. Reduces Max Life by 15%." - ha troca de risco/beneficio, nao um premio puro.',
    'As duas opcoes conduzem a MESMA batalha (BattleInfo 2544644); a diferenca e o status concedido. Dado observado, sem alteracao proposta.',
    'disabled=1 registrado como decisao de configuracao do asset; nenhuma proposta de reativacao (regra de curadoria: nao reativar slots disabled por padrao).'])

# ---------------------------------------------------------------- 22
assert_eq(fld(22, 'condicoes.disabled'), 0, '22 disabled')
ev(22, 'MELHORAR',
   'Evento ativo, com narrativa de 354 caracteres e duas opcoes coerentes; a unica alteracao defensavel e uma correcao ortografica pontual no texto original.',
   'texto (354 ch) termina com "I\'m blind as a bat, but I\'ve the strength of a ogre!"; 2 opcoes: "Drink" (Self -> Brawler\'s Brew 2545414, StatusType Fortune(1), "Might increased by {12,60}. Applies Blind at the start of your turn."; XP dar=false com razao 3.0) e "Leave" (texto imersivo, sem acao) . disabled=0; Common(0); peso 1.0; minLevel 1; allowAtAllTimesOfDay=0/allowedTimeOfDay=1 (somente noite); terreno liberado em qualquer terreno com lista de excecao [WaterTempleRuins, ForgottenMines, CastleGloom, Emberlands].',
   [prop('SUGESTAO DE CORRECAO DO ORIGINAL', 'ortografia (artigo indefinido)',
         JP(22, 'texto'), 'the strength of a ogre!', 'the strength of an ogre!',
         'Antes de vogal o artigo indefinido ingles e "an". O trecho consta da nota manuscrita do alquimista dentro do proprio texto do evento.', tipo='trecho')],
   ['parte01: "3 opcoes (DRINK, SELL, LEAVE)" -> falso. Sao 2 opcoes: Drink e Leave.',
    'parte01: "Opcao 2 (SELL) tem status_requeridos: [5] - requer status Brawler\'s Blessing" -> falso. Nenhuma opcao desta faixa tem status_requeridos (a lista e vazia em todas as 36 opcoes dos 20 eventos).',
    'parte01: "disabled: 1 - evento DESLIGADO" -> falso. disabled=0; o evento esta habilitado.'],
   ['O espaco duplo final em opcoes[0].efeitos[0].texto ("fuzzy.\" ") e cosmetico; registrado em Analise A, sem proposta.',
    'Nenhuma opcao desta faixa concede ouro (ouro.dar=false em todas): o evento e de status, nao de economia.'])

# ---------------------------------------------------------------- 23
ev(23, 'MANTER',
   'Narrativa completa (417 ch), duas escolhas com efeitos distintos e mensuraveis, sem defeito literal detectado. Nao ha proposta defensavel que nao seja preferencia de estilo.',
   'texto (417 ch) descreve o monolito de obsidiana e a runa esmeralda; 2 opcoes: "Activate the blessing" (Self -> Celerity 2545417, Fortune(1), "Dexterity increased by {4,20}.") e "Heal from the monolith" (Self, percentMaxHealth=50.0 e percentMaxMana=50.0 - cura real configurada). Ambas Success com RollLimit 0, sem rolagem. disabled=0; Common(0); peso 1.0; minLevel 1; terreno restrito a FreewindForest(2).',
   [],
   ['parte01: titulo "EVT 23: Cursed Coin Toss" -> falso. O ordinal 23 e "Carved Monolith" (resources.assets:2545555, id 9c907851-1c3e-4d43-9286-96559cbfda7f).',
    'parte01: "3 opcoes de escolha (HEADS, TAILS, WALK AWAY)" -> falso. Sao 2 opcoes (Activate the blessing / Heal from the monolith).',
    'parte01: "texto = (vazio)" -> falso. O texto tem 417 caracteres.'],
   ['A opcao 2 tem cura de 50% de vida e mana maximas sem rolagem; a opcao 1 entrega status permanente de quest (Celerity, durationType=Quest). Ambas as recompensas sao medidas na fonte.'])

# ---------------------------------------------------------------- 24
assert_eq(fld(24, 'texto'), '\n', '24 texto')
assert_eq(fld(24, 'opcoes[0].efeitos[0].texto'), '', '24 acao texto')
ev(24, 'MELHORAR',
   'Vazio narrativo real: o campo texto contem apenas o caractere de nova linha e a acao de resultado nao tem texto. E o caso em que a correcao documental propoe conteudo, preservando o ingles da fonte.',
   'texto = "\\n" (1 caractere: apenas quebra de linha); 1 opcao "Activate" com texto "Grants [o1a1_status]."; acao Success com texto "" (vazio) -> Self -> Dexterity 2545380 (StatusType Normal(0), "Dexterity increased by [0]."); batalha iniciar=false. remocoes_status contem 1 regra cujo ActionOnRemoval e referencia nula (m_PathID 0) - registrada como NULL, sem inferir remocao efetiva. disabled=0; Common(0); peso 1.0; isLesserEvent=1; StorySetting Both(2); allowedNodeTypes=[] com allowOnAllNodeTypes=0.',
   [prop('PROPOSTA DE CONTEUDO', 'narrativa principal ausente', JP(24, 'texto'), '\n',
         'A flat stone tablet leans against the rock, its face cut with a single dwarven rune. The carving is worn smooth in places, as though many hands have traced it before yours.',
         'O evento e um achado de runa que concede Dexterity; a proposta descreve apenas a cena e o objeto, sem introduzir mecanica, valor ou condicao nova. Texto em ingles para preservar o idioma da fonte.'),
    prop('PROPOSTA DE CONTEUDO', 'texto de resultado da acao ausente',
         JP(24, 'opcoes[0].efeitos[0].texto'), '',
         'You press your palm to the rune. A cool current climbs your arm, and your fingers feel lighter, quicker than before.',
         'O unico efeito configurado e o status Dexterity em Self; a proposta narra exatamente esse efeito, sem acrescentar alvo, quantidade ou condicao.')],
   ['parte01: "texto = (vazio)" -> parcialmente impreciso: o campo tem 1 caractere ("\\n"), nao cadeia vazia. O efeito pratico (nenhuma narrativa exibida) e o mesmo; o dado exato importa para a correcao.',
    'parte01: "Exemplo: ... itens de rarezas Uncommon/Very Rare - loot significativo" -> falso. Nao ha recompensa de item configurada (itens.dar=false); o unico efeito e o status Dexterity.',
    'parte01: "Opcao tem rolagem com Intelligence +3, RollLimit 10 - mas sem acao Failure" -> falso. Nao ha rolagem (rolagem.bonus=[], limite_rolagem=0).'],
   ['O unico evento da faixa com 3 campos de texto relevantes vazios simultaneamente (evento, opcao e resultado) e o 37; o 24 tem a opcao preenchida ("Grants [o1a1_status].").'])

# ---------------------------------------------------------------- 25
ev(25, 'MANTER',
   'Narrativa presente nas duas opcoes (481 ch no evento; texto tambem na opcao Strike) e ausencia de falha justificada pelo limiar 0. A referencia de batalha nula e NULL declarado, nao defeito demonstravel offline.',
   'texto (481 ch); 2 opcoes: "Strike" (Success RollLimit 0, com texto de resultado, batalha iniciar=true sem BattleInfo referenciado) e "Leave" (texto "The fear of the unknown grips your spirit..." e acao Success sem efeito). disabled=0; Common(0); peso 1.0; minLevel 1; terreno restrito a FrostwroughtMountain(7); LeadsToFortune=1.',
   [],
   ['parte01: "Chave: resources.assets:2545406" -> falso. Chave real resources.assets:2545560 (id 19b06250-69cc-41bb-9972-530129c41bf2).',
    'parte01: "opcoes[0].texto = (vazio no asset)" -> falso. O texto da opcao 1 e "Ring the gong and issue a challenge.".',
    'parte01: "2 opcoes: STRIKE (Success) e IGNORE" -> impreciso. A segunda opcao chama-se "Leave".'],
   ['batalha.referencia.chave/nome sao NULL em ambas as acoes da opcao 1: registro de referencia nula, cujo motivo e "referencia nula, resultado dependente de runtime ou valor nulo do leitor". Nao se infere batalha vazia nem recompensa ausente.'])

# ---------------------------------------------------------------- 26
ev(26, 'MELHORAR',
   'Evento mais completo da faixa (rolagem com limiar, ramo Success e Failure, ambos com batalha referenciada e evento de vitoria encadeado). A unica alteracao defensavel e a correcao ortografica do texto original.',
   'texto (453 ch); texto_resultados_possiveis = "What will you do?"; 2 opcoes: "Open" (rolagem Intel+3 via rollBonusTypes [3]) com acao Success (RollLimit 12) e acao Failure (RollLimit 0, Self -> Cursed 2545493, "Reduces All Stats by 10% per stack"), ambas iniciando a batalha BattleInfo 2544645 "Cursed Chest Battle" (battlePointValue 16); e "Leave". XP configurado com dar=false e razao 2.0. disabled=0; Rare(2); peso 1.0; minLevel 3; LeadsToFortune=0.',
   [prop('SUGESTAO DE CORRECAO DO ORIGINAL', 'ortografia (confusao bares/bears)',
         JP(26, 'texto'), 'warped and decayed, bares the weight of forgotten sorrows',
         'warped and decayed, bears the weight of forgotten sorrows',
         'O verbo correto e "bears" (suportar, carregar); "bares" e o verbo despir. Mesmo defeito repete-se no ordinal 27 e no 32.', tipo='trecho')],
   ['parte01: "Opcao 1 (OPEN) tem rolagem Intelligence +3, RollLimit 12 - mas sem acao Failure" -> falso. Existe acao Failure (acesso idx 2, RollLimit 0) que aplica o status Cursed e inicia a mesma batalha.',
    'parte01: "Texto de Success ... curto. Sem Failure" -> falso quanto ao Failure: o texto de falha tem 245 caracteres e descreve o nepente e o ataque dos mortos-vivos.',
    'parte01: "2 opcoes: OPEN e IGNORE" -> impreciso. A segunda opcao chama-se "Leave".'],
   ['O campo batalha.dados_recompensa_final e NULL e explicitamente nao exercitado em runtime; nao se infere recompensa da batalha.',
    'O BattleInfo 2544645 encadeia VictoryEvent 2545561 = PartyEvent "Cursed Chest Battle Victory" (categoria NotInEventPool, EventNameOverride "Cursed Chest"), que entrega o loot da arca. Encadeamento medido na fonte.'])

# ---------------------------------------------------------------- 27
ev(27, 'MELHORAR',
   'Segunda variante da arca amaldicoada, com titulo de evento identico ao 26 e nome_asset proprio. Texto do evento e das opcoes identicos ao 26. A alteracao defensavel e a mesma correcao ortografica; a assimetria de rolagem fica documentada como decisao do dono.',
   'titulo "Cursed Chest"; nome_asset "Cursed Mimic Chest"; campos_originais.EventNameOverride "Cursed Chest"; texto (453 ch) identico ao do ordinal 26; texto_resultados_possiveis = "What will you do?"; 2 opcoes: "Open" (rolagem Intel+3 com rollBonusTypes [3], mas acao unica Success com RollLimit 0, texto do mimic, batalha BattleInfo 2544645 "Cursed Chest Battle") e "Leave". disabled=0; Rare(2); peso 1.0; minLevel 4 (um a mais que o 26); LeadsToFortune=1 (o 26 tem 0).',
   [prop('SUGESTAO DE CORRECAO DO ORIGINAL', 'ortografia (confusao bares/bears)',
         JP(27, 'texto'), 'warped and decayed, bares the weight of forgotten sorrows',
         'warped and decayed, bears the weight of forgotten sorrows',
         'Mesma correcao do ordinal 26; o texto e literalmente o mesmo.', tipo='trecho')],
   ['parte01: titulo "EVT 27: Cursed Mimic Chest" -> impreciso. O titulo do evento e "Cursed Chest"; "Cursed Mimic Chest" e o nome_asset. A variante e a segunda arca da faixa.',
    'parte01: "Opcao 1 tem rolagem Intelligence +3, RollLimit 0 - sem rolagem real" -> o bonus e o limiar foram medidos corretamente, mas a conclusao "ambiguidade" fica substituida pelo dado: rollBonusTypes=[3] com EventResultSetting RollLimit=0.',
    'parte01: "Efeito de OPEN: inicia combate com Cursed Mimic (boss fight)" -> a batalha referenciada e a mesma do ordinal 26 (BattleInfo 2544645 "Cursed Chest Battle"); "boss fight" nao consta da fonte.'],
   ['Assimetria medida: o 26 usa o mesmo rollBonusTypes=[3] com RollLimit 12 e ramo Failure; o 27 usa RollLimit 0 sem Failure. Nenhuma alteracao proposta sem decisao do dono, porque alteraria jogabilidade (probabilidade e efeito de falha).',
    'A diferenca LeadsToFortune (26=0, 27=1) e dado de configuracao, sem inferencia sobre recompensa.'])

# ---------------------------------------------------------------- 28
ev(28, 'MANTER',
   'Existe ramo real de risco (Failure com Slowed) e recompensa de XP ao grupo no sucesso; a opcao unica e a propria configuracao do evento-tranca. Nenhum defeito literal detectado.',
   'texto (530 ch); texto_resultados_possiveis = "What will you do?"; 1 opcao "Pull Away" com rolagem Might (rollBonusTypes [0], valor 0) e duas acoes: Success (RollLimit 8) -> XP dar=true razao 0.5 com alvo Party (OverrideTargetType 1 / TargetTypeOverride 2); Failure (RollLimit 1) -> Self -> Slowed 2545501 ("Cooldowns increased by 1 turn."). disabled=0; Common(0); peso 1.0; minLevel 3; terreno restrito a CastleGloom(3).',
   [],
   ['parte01: "1 unica opcao (PULL AWAY) - sem escolha ... Opcao tem rolagem Might +0, RollLimit 8 - mas sem acao Failure" -> falso quanto ao Failure: a acao Failure existe (RollLimit 1, Slowed).',
    'parte01: "Efeitos: ouro e XP" -> falso quanto ao ouro: ouro.dar=false; a recompensa medida e XP 0.5 para o grupo.'],
   ['O bonus de rolagem Might tem valor 0: o dado de atributo esta declarado sem acrescimo. Registrado como dado, sem proposta.'])

# ---------------------------------------------------------------- 29
ev(29, 'MANTER',
   'Duas opcoes com texto proprio (inclusive o "Leave", que narra a recusa) e status Cursed aplicado no ramo de risco; sem defeito literal. LeadsToFortune=1 sem item configurado e dado, nao prova de recompensa ausente.',
   'texto (334 ch); 2 opcoes: "Read" (Success RollLimit 0, sem rolagem, texto de 459 ch, Self -> Cursed 2545493, batalha iniciar=true sem BattleInfo referenciado) e "Leave" (texto "You sense the lurking malevolence within its very essence..." e acao Success sem efeito). disabled=0; Common(0); peso 1.0; minLevel 3; LeadsToFortune=1.',
   [],
   ['parte01: "Opcao 1 (READ) tem rolagem Intelligence +3, RollLimit 10 - mas sem acao Failure" -> falso. Nao ha rolagem (rolagem.bonus=[], limite_rolagem=0) nem ramo de falha; o custo e o status Cursed aplicado no proprio sucesso.',
    'parte01: "Texto de Success presente, curto" -> falso quanto ao tamanho: o texto de sucesso tem 459 caracteres.',
    'parte01: "Sem texto para REFUSE/CLOSE" -> falso. A opcao "Leave" tem texto de opcao completo.',
    'parte01: "LeadsToFortune: 1 - mas sem Fortuna visivel nos efeitos (sem item especial)" -> nao se sustenta como defeito: o indicador e de configuracao e itens.dar=false; nao se infere recompensa ausente.'],
   ['O nome do asset em jogo e "Dark Tome" (marcacao <incr><indigo><b>Dark Tome</b></indigo></incr> no texto), enquanto o titulo do evento e "Cursed Tome". Observacao de rotulo, sem proposta de alteracao.'])

# ---------------------------------------------------------------- 30
ev(30, 'MANTER',
   'Decisao pura (sem rolagem) com texto nos dois ramos, inclusive no "Leave"; o evento funciona como contrato de quest via status tipo Quest. Sem defeito literal.',
   'texto (626 ch, fala do Necromante); 2 opcoes: "Accept" (Success RollLimit 0, texto de resultado, Self -> Dark Discoveries 2545510, StatusType Quest(3), "Locate and destroy the runaway experiments.") e "Leave" (Success RollLimit 0, texto de resultado "She nods her head in understanding..."). disabled=0; Common(0); peso 1.0; minLevel 3; terreno restrito a SunkenSwamplands(8).',
   [],
   ['parte01: "Texto de Success para ACCEPT presente, curto. Sem texto para REFUSE" -> falso. A opcao "Leave" tem texto de resultado proprio.',
    'parte01: "Efeitos de ACCEPT: itens e status" -> falso quanto a itens: itens.dar=false; o efeito e o status de quest.',
    'parte01: "O REFUSE deveria ter alguma consequencia" -> proposta de design, nao defeito: o ramo de recusa tem narrativa e encerra o evento, com StatusType Quest no aceite documentando o objetivo.'],
   ['Nenhuma das 36 opcoes da faixa possui status_requeridos; o evento nao depende de estado previo.'])

# ---------------------------------------------------------------- 31
ev(31, 'MANTER',
   'Narrativa curta porem completa nos dois ramos, com status Ethereal no ramo de ajuda. disabled=1 e decisao de configuracao do asset, sem evidencia de defeito nos dados offline; reativacao nao e proposta.',
   'texto (54 ch) = "The yearning ghost extends her hand pleading for help."; 2 opcoes: "Reach" (Success RollLimit 0, Self -> Ethereal 2545439, Fortune(1), "Increases Physical Resistance by {10,50}%. Reduces Elemental Resistance by {5,25}%.") e "Leave" (Success, texto "You leave, but the ghost\'s disappointment haunts your dreams."). disabled=1; Common(0); peso 1.0; minLevel 1; LeadsToFortune=1.',
   [],
   ['parte01: "1 opcao: REACH - da status [o1a1_status]" -> falso. Sao 2 opcoes: Reach e Leave.',
    'parte01: "Texto de Success presente, curto" -> correto quanto ao tamanho (54 ch no evento), mas a afirmacao ignora que o texto da opcao Leave e da acao do Leave tambem existem.',
    'parte01: chave resources.assets:2545412 -> falso. Chave real resources.assets:2545573 (id 03048d72-af64-4337-8ae9-7475981d36e5).'],
   ['O texto e as duas opcoes deste asset sao identicos, campo a campo, aos do ordinal 34 "Dwarven Drinking Contest" (sha256 distinto: 365632d9... no 31, 2b0bd974... no 34). Ambos disabled=1: padrao de conteudo provisorio. Achado registrado; nenhuma proposta de texto inventado.'])

# ---------------------------------------------------------------- 32
assert_eq(fld(32, 'opcoes[1].efeitos[0].efeitos[0].recompensas.itens.quantidade_configurada'), 0, '32 qtd')
ev(32, 'MELHORAR',
   'A opcao "Loot" promete no texto o item Gold Statue Head e possui tabela de loot com esse item a 100%, mas a quantidade configurada e 0. Esta e a unica proposta desta faixa que altera valor alem de texto, e ela e medida na fonte.',
   'texto (1094 ch, dialogo do Rei Montanha); 2 opcoes: "Accept" (Success RollLimit 0, Self -> Dwarf Rage! 2545511, StatusType Quest(3), statusDescription vazia) e "Loot" (Success RollLimit 0, texto "You pick up the Gold Statue Head thoughtfully...", Self, itens.dar=true, pool Unassigned(2), quantidade_configurada=0, 1 tabela com ItemInfo 2546477 "Gold Statue Head" a 100%, restricoes de tipo/raridade vazias). disabled=0; Common(0); peso 1.0; minLevel 3; terreno restrito a DwarvenHalls(9).',
   [prop('PROPOSTA DE CONTEUDO', 'quantidade de item incompativel com a narrativa',
         JP(32, 'opcoes[1].efeitos[0].efeitos[0].recompensas.itens.quantidade_configurada'),
         '0', '1',
         'A tabela de loot da propria opcao aponta para ItemInfo 2546477 "Gold Statue Head" (Rarity 3, FixedSellPrice 5000, descricao opcional "The Golden Head of the Mountain King.") com Chance 100.0, e o texto da opcao entrega explicitamente o item; com quantidade_configurada=0 nao ha unidade a conceder. Valor de destino 1 alinha configuracao e narrativa. O campo original equivalente e itemCount=0 em campos_originais.'),
    prop('SUGESTAO DE CORRECAO DO ORIGINAL', 'ortografia (confusao bares/bears)',
         JP(32, 'texto'), 'It bares the telltale signs of looting', 'It bears the telltale signs of looting',
         'Mesmo defeito dos ordinais 26 e 27.', tipo='trecho'),
    prop('SUGESTAO DE CORRECAO DO ORIGINAL', 'espaco duplo no texto de resultado',
         JP(32, 'opcoes[1].efeitos[0].texto'), "\"Oh, You wouldn't  dare!\"", "\"Oh, You wouldn't dare!\"",
         'Dois espacos entre "wouldn\'t" e "dare"; correcao cosmetica do literal.', tipo='trecho')],
   ['parte01: titulo "EVT 32: Desecrated Statue of the First Mountain King" esta correto, mas a chave resources.assets:2545413 e falsa (real: 2545576, id 31c21c13-d1fb-4be8-9d45-299dbad44e9e).',
    'parte01: "2 opcoes: ACCEPT e DECLINE" -> falso. A segunda opcao e "Loot".',
    'parte01: "Aceitar gera um quest/objetivo (ajudar o Rei Montanha)" -> correto: o aceite entrega o status tipo Quest "Dwarf Rage!" (2545511).',
    'parte01: "Nenhuma opcao tem rolagem (RollLimit 0, bonus: [])" -> correto para este evento, mas generalizado indevidamente no resumo da proposta.'],
   ['O status Dwarf Rage! (2545511) tem statusDescription vazia na fonte: registrado como ausencia de descricao, sem inferir efeito.'])

# ---------------------------------------------------------------- 33
ev(33, 'MANTER',
   'Tres opcoes distintas, cada uma com status proprio e XP 0.5; limiar 0 em todas significa sucesso automatico, eliminando a necessidade de ramo de falha. Os bonus de rolagem presentes sao inertes nesse desenho - dado documentado, sem alteracao proposta.',
   'texto (916 ch); texto_resultados_possiveis (76 ch) = "The man remains silent, watching with disturbing patience for you to choose."; 3 opcoes, todas Success com RollLimit 0 e XP dar=true razao 0.5: "Crusty Cockroach" (rolagem Vitality+2 -> Well Fed: Stats 2545403, "Stats increased by 10%."), "Hand Soup" (rolagem Reflex+4 -> Well Fed: Treasure 2545404, "Increases item drops and gold gained by 50%.") e "Twitching Tentacle" (rolagem Dexterity+1 -> Well Fed:  Experience 2545402, "Experience gained increased by 50%."). disabled=0; Common(0); peso 1.0; minLevel 1; terrenos CastleGloom(3) e SunkenSwamplands(8).',
   [],
   ['parte01: "Cada opcao tem rolagem com Vitality +2, RollLimit 0" -> impreciso: cada opcao tem atributo de rolagem proprio (Vitality+2, Reflex+4, Dexterity+1); apenas o limiar 0 e comum.',
    'parte01: "Sem Failure em nenhuma opcao ... ambiguidade de rolagem" -> substituido pelo dado: com RollLimit 0 nas tres acoes, nenhuma falha e alcancavel; os tres resultados sao positivos e distintos.',
    'parte01: "Manter as 3 opcoes" -> correto, e a manutencao e o veredito deste cartao.'],
   ['os textos das opcoes 1 e 2 terminam com espaco: cosmetico, registrado em Analise A, sem proposta.'])

# ---------------------------------------------------------------- 34
ev(34, 'MANTER',
   'Asset desabilitado cujo conteudo e copia literal do ordinal 31. Nao ha narrativa propria para corrigir, e inventar texto para um slot disabled nao e proposta defensavel; o achado fica documentado para decisao do dono.',
   'titulo "Dwarven Drinking Contest"; texto (54 ch) identico ao do ordinal 31 ("The yearning ghost extends her hand pleading for help."); 2 opcoes "Reach" e "Leave" identicas em titulo, texto e efeitos (Ethereal 2545439). disabled=1; Common(0); peso 1.0; minLevel 1; LeadsToFortune=1. sha256_objeto 2b0bd974... (distinto do 31).',
   [],
   ['parte01: titulo "EVT 34: Disturbing Statue" -> falso. O ordinal 34 e "Dwarven Drinking Contest" (resources.assets:2545578, id 5777d2ca-8fca-485d-92c8-239f6da0e8a4).',
    'parte01: "2 opcoes: CRAFT e IGNORE ... forja item com atributo bonus" -> falso. As opcoes sao Reach e Leave (status Ethereal).',
    'parte01: "Opcao 1 (CRAFT) tem rolagem Intelligence +3, RollLimit 10" -> falso. Nao ha rolagem neste asset.'],
   ['Achado de curadoria: o asset "Dwarven Drinking Contest" carrega o mesmo conteudo do "Dead Adventurer" (texto, opcoes e efeitos identicos). Ambos disabled=1. Registrado para o dono decidir se havera conteudo proprio; nenhuma alteracao proposta neste lote.'])

# ---------------------------------------------------------------- 35
ev(35, 'MELHORAR',
   'Rolagem com limiar 10 e ramo de falha real com efeitos mensuraveis; a unica alteracao defensavel e a correcao ortografica do texto original.',
   'texto (395 ch); 1 opcao "Act" com rolagem Intel+3 (rollBonusTypes [3]); acao Success (RollLimit 10) -> XP dar=true razao 1.0 alvo Party (OverrideTargetType 1 / TargetOverride 2) com texto de resultado; acao Failure (RollLimit 1) -> percentMaxHealth=-30.0 alvo Party e Self -> Severely Burned 2545499 ("Reduces Fire Resistance by 25% per stack"). disabled=0; Common(0); peso 1.0; minLevel 1; terrenos ForgottenMines(4) e DwarvenHalls(9).',
   [prop('SUGESTAO DE CORRECAO DO ORIGINAL', 'ortografia (quitely/quietly)',
         JP(35, 'opcoes[0].efeitos[0].texto'), 'The dwarven sentry quitely apologizes and allows you safe passage.',
         'The dwarven sentry quietly apologizes and allows you safe passage.',
         'O adverbio ingles e "quietly"; "quitely" nao existe. Correcao pontual no texto de resultado da acao Success.', tipo='trecho')],
   ['parte01: "1 unica opcao (ACT) - sem escolha" -> correto quanto ao numero de opcoes, mas a conclusao de defeito nao se sustenta: existe ramo de risco interno (Success/Failure).',
    'parte01: "Opcao tem rolagem Intelligence +3, RollLimit 10 - mas sem acao Failure" -> falso. A acao Failure existe (RollLimit 1) e aplica -30% de vida maxima ao grupo e o status Severely Burned.',
    'parte01: "Efeitos: XP e itens" -> falso quanto a itens: itens.dar=false; os efeitos medidos sao XP 1.0 para o grupo no sucesso e debuff no fracasso.'],
   ['O ramo de falha afeta o grupo inteiro (alvo Party), nao apenas o personagem que age; dado medido em campos_originais (OverrideTargetType=1, TargetTypeOverride=2).'])

# ---------------------------------------------------------------- 36
ev(36, 'MELHORAR',
   'Duas opcoes com desfechos diferentes (risco com rolagem versus reverencia sem risco) e recompensa comum de status permanente; a alteracao defensavel e uma correcao ortografica no texto de falha.',
   'texto (385 ch); texto_resultados_possiveis = "What will you do?"; 2 opcoes: "Loot" com rolagem Might (rollBonusTypes [0], valor 0), Success (RollLimit 16) -> Self -> Horn of Devotion 2545448 (Fortune(1), durationType Permanent(3), "Increases the effect of Shrines by {50,100}%.") e Failure (RollLimit 1) -> Self -> Weakened 2545504 ("Reduces Might by 20% per stack"); e "Pay Respect" (Success RollLimit 0) -> Self -> Horn of Devotion. disabled=0; Common(0); peso 1.0; minLevel 1; LeadsToFortune=1; terrenos DwarvenHalls(9) e ForgottenMines(4).',
   [prop('SUGESTAO DE CORRECAO DO ORIGINAL', 'ortografia (its/it\'s)',
         JP(36, 'opcoes[0].efeitos[1].texto'), 'but its of no use.', "but it's of no use.",
         'A contraccao de "it is" exige apostrofo; "its" e possessivo. Correcao pontual no texto de falha da opcao Loot.', tipo='trecho')],
   ['parte01: "Opcao 1 (LOOT) tem rolagem Might +0, RollLimit 16 - mas sem acao Failure" -> falso. A acao Failure existe (RollLimit 1, Weakened).',
    'parte01: "2 opcoes: LOOT e LEAVE" -> impreciso. A segunda opcao e "Pay Respect".',
    'parte01: "LeadsToFortune: 1 - da item especial no Success" -> falso quanto a item: Horn of Devotion e um EventStatus (Fortune, permanente), nao um item; itens.dar=false.'],
   ['A recompensa das duas opcoes e o mesmo status; a diferenca e o risco da rolagem (limiar 16) versus a ausencia de rolagem em "Pay Respect". Dado medido, sem alteracao proposta.'])

# ---------------------------------------------------------------- 37
assert_eq(fld(37, 'texto'), '', '37 texto')
assert_eq(fld(37, 'opcoes[0].texto'), '', '37 op texto')
assert_eq(fld(37, 'opcoes[0].efeitos[0].texto'), '', '37 acao texto')
ev(37, 'MELHORAR',
   'Vazio narrativo nos tres niveis (evento, opcao e resultado) no unico evento Legendary da faixa, cuja recompensa e um item fixo e verificavel. Correcao proposta em ingles, com conteudo ancorado no item concedido.',
   'texto = "" (cadeia vazia); texto_resultados_possiveis = ""; 1 opcao "Open" com texto "" e acao Success com texto ""; efeito: Self, itens.dar=true, itemPoolType None(0), quantidade_configurada=1, 1 tabela com 10 entradas do mesmo ItemInfo 2546793 "Gold Bar" (Rarity 3, FixedSellPrice 2500) a Chance 100.0; ouro dar=false com razao 0.0; XP dar=false razao 1.0. disabled=0; Legendary(3); peso 1.0; minLevel 4; StorySetting Both(2); allowAtAllLevels=0.',
   [prop('PROPOSTA DE CONTEUDO', 'narrativa principal ausente', JP(37, 'texto'), '',
         'A low stone altar stands at the end of the hall, its surface swept clean of dust. On it rests an ironbound chest, and beside it a dwarven plaque reads: "What is given is given back."',
         'O evento Legendary entrega exatamente um Gold Bar; a proposta descreve a cena (altar, arca, placa) sem criar mecanica, condicao ou valor novo. Texto em ingles para preservar o idioma da fonte.'),
    prop('PROPOSTA DE CONTEUDO', 'texto da opcao vazio', JP(37, 'opcoes[0].texto'), '',
         'Open the tribute chest.',
         'A opcao chama-se "Open" e nao tem descricao; a proposta nomeia a acao exatamente como ela e configurada (abrir a arca).'),
    prop('PROPOSTA DE CONTEUDO', 'texto de resultado da acao ausente', JP(37, 'opcoes[0].efeitos[0].texto'), '',
         'The lid swings open without a sound. Inside, resting on a bed of dust, lies a single bar of gold - the tribute, returned.',
         'O unico efeito configurado e conceder 1 Gold Bar ao Self; a proposta narra esse resultado sem acrescentar alvo, quantidade ou condicao.')],
   ['parte01: "EVT 37: Dwarven Tribute ... RARIDADE: Common (0)" -> falso. A raridade e Legendary(3).',
    'parte01: "1 unica opcao (PAY)" -> falso. A opcao chama-se "Open".',
    'parte01: "Opcao tem rolagem Intelligence +3, RollLimit 10 - mas sem acao Failure" -> falso. Nao ha rolagem (rolagem.bonus=[], limite_rolagem=0).',
    'parte01: "Efeito: da item ao anao, recebe ouro de volta" -> falso. O efeito medido e conceder 1 Gold Bar ao proprio grupo, com ouro.dar=false (razao 0.0).',
    'parte01: chave resources.assets:2545418 -> falso. Chave real resources.assets:2545581 (id 7022fe7d-f9fb-4407-82ef-4e10f5d45d68).'],
   ['As 10 entradas da tabela apontam todas para o mesmo ItemInfo, com Chance 100.0: a recompensa e deterministica na configuracao (1 Gold Bar). O sorteio final em partida permanece NAO_EXERCITADO.'])

# ---------------------------------------------------------------- 38
ev(38, 'MELHORAR',
   'Rolagem com limiar 12, ramo de falha com dano e status, e recompensa permanente no sucesso. Tres defeitos literais medidos no texto original, todos corrigiveis sem tocar mecanica.',
   'texto (1266 ch, pagina do grimorio de Edwin); 2 opcoes: "Cast" com rolagem Intel+3 (rollBonusTypes [3]), Success (RollLimit 12) -> Self -> Edwin\'s Enchantment 2545429 (Fortune(1), durationType Permanent(3), "Power for mana use increased by {25,50}%. Mana costs are now paid in Health instead.") e Failure (RollLimit 1) -> percentMaxHealth=-30.0 Self -> Confused 2545491 ("Reduces Intelligence by 20% per stack"); e "Leave" (texto "You think better of fleeting fame."). disabled=0; Common(0); peso 1.0; minLevel 1; LeadsToFortune=1.',
   [prop('SUGESTAO DE CORRECAO DO ORIGINAL', 'espaco inicial no texto original', JP(38, 'texto'),
         ' On a worn table lays a spellbook', 'On a worn table lays a spellbook',
         'O texto comeca com um espaco antes de "On"; correcao de espaco inicial.', tipo='trecho'),
    prop('SUGESTAO DE CORRECAO DO ORIGINAL', 'ortografia (Infact/In fact)', JP(38, 'texto'),
         'Infact, only a fool', 'In fact, only a fool',
         '"Infact" nao e palavra em ingles; a locucao correta e "In fact".', tipo='trecho'),
    prop('SUGESTAO DE CORRECAO DO ORIGINAL', 'pontuacao (ponto duplo)', JP(38, 'opcoes[0].efeitos[0].texto'),
         'to fuel [his] magic..', 'to fuel [his] magic.',
         'O texto de sucesso termina com dois pontos finais; correcao de pontuacao no fecho da frase.', tipo='trecho')],
   ['parte01: titulo "EVT 38: Dwarven Forge" -> falso. O ordinal 38 e "Edwin\'s Demise" (resources.assets:2545582, id 4af726e7-657e-403a-883b-e3221fdd700c).',
    'parte01: "2 opcoes: FORGE e BUY ... ambas com rolagem Intelligence +3, RollLimit 10 - mas sem acao Failure" -> falso. As opcoes sao Cast e Leave; o limiar e 12 e existe acao Failure (RollLimit 1).',
    'parte01: "Ambas dao itens de forja (diferentes raridades/precos)" -> falso. Nao ha recompensa de item; os efeitos sao status permanente no sucesso e dano + Confused no fracasso.'],
   ['O status Edwin\'s Enchantment tem duracao Permanent(3): recompensa persistente no sucesso, com descricao que explicita o custo (mana paga em vida).'])

# ---------------------------------------------------------------- 39
ev(39, 'MELHORAR',
   'Narrativa rica (840 ch), mas com duas aberturas consecutivas para a mesma arvore, a segunda repetindo o proprio nome. Duas escolhas com efeitos distintos. Correcoes propostas sao de edicao de texto.',
   'texto (840 ch) com dupla introducao: paragrafo 1 inicia "A massive <green><b><incr>Elder Tree</incr></b></green> grows here..." e paragrafo 3 inicia "You stumble upon an entity as old as time itself: the <green><b><incr>Elder Tree</incr></b></green>."; 2 opcoes: "Rest" (Success RollLimit 0, Self, percentMaxHealth=100.0 e percentMaxMana=100.0, texto de resultado presente) e "Eat" (Success RollLimit 0, Self, XP dar=true razao 2.0). disabled=0; Common(0); peso 1.0; minLevel 1; allowAtAllLevels=1; LeadsToFortune=0; terreno restrito a FreewindForest(2).',
   [prop('SUGESTAO DE CORRECAO DO ORIGINAL', 'narrativa duplicada (dois inicios)',
         JP(39, 'texto'),
         'A massive <green><b><incr>Elder Tree</incr></b></green> grows here. Its giant body formed not only of wood but of living stone and ore. All around it life seems to flourish as if it were the very heart of the forest.\n\nYou stumble upon an entity as old as time itself: the ',
         'A massive <green><b><incr>Elder Tree</incr></b></green> grows here. Its giant body formed not only of wood but of living stone and ore. All around it life seems to flourish as if it were the very heart of the forest.\n\nIt stands regal and magnificent, its massive trunk adorned with the etchings of time, its gnarled boughs stretching out like the arms of a benevolent giant.',
         'O trecho removido ("You stumble upon an entity as old as time itself: the ") repete a mesma apresentacao e reapresenta o nome da arvore logo apos o primeiro paragrafo; a remocao mantem a frase seguinte intacta.', tipo='trecho'),
    prop('SUGESTAO DE CORRECAO DO ORIGINAL', 'espaco inicial no texto da opcao',
         JP(39, 'opcoes[0].texto'), ' Enjoy the tranquility the Elder Tree brings.',
         'Enjoy the tranquility the Elder Tree brings.', 'Correcao de espaco inicial no texto da opcao "Rest".', tipo='trecho')],
   ['parte01: titulo "EVT 39: Dwarven Market" -> falso. O ordinal 39 e "Elder Tree" (resources.assets:2545583, id 2779cca5-013a-4bbc-ba32-e7d25ef7c8b7).',
    'parte01: "3 opcoes: BUY, SELL, LEAVE" -> falso. Sao 2 opcoes: Rest e Eat.',
    'parte01: "EVT 39 marcado com LeadsToFortune: 1 mas sem Fortuna visivel" -> falso. LeadsToFortune do ordinal 39 e 0.'],
   ['A opcao "Rest" concede 100% de vida e mana maximas, o maior valor de cura da faixa, sem rolagem; a opcao "Eat" concede XP com razao 2.0 ao Self. Valores medidos.'])

# ---------------------------------------------------------------- 40
ev(40, 'MANTER',
   'Narrativa presente (283 ch), prompt de selecao presente, rolagem com limiar 10 e ramo de falha com efeitos reais. A opcao unica e a configuracao do evento-sentinela; nenhum defeito literal detectado.',
   'texto (283 ch); texto_resultados_possiveis (38 ch) = "Who will attempt to disrupt the magic?"; 1 opcao "Disrupt" com rolagem Dexterity+1 (rollBonusTypes [1]); Success (RollLimit 10) -> XP dar=true razao 1.0 alvo Party (OverrideTargetType 1 / TargetOverride 2); Failure (RollLimit 1) com dois efeitos: Party sem recompensa e Self com percentMaxHealth=-20.0 -> Mortally Wounded 2545497 ("Reduces Healing Received by 25% per stack"). disabled=0; Common(0); peso 1.0; minLevel 1; allowOnAllTerrainTypes=1 sem excecoes.',
   [],
   ['parte01: "1 unica opcao (DISRUPT) - sem escolha" -> correto quanto ao numero de opcoes; a conclusao de defeito nao se sustenta porque existe ramo interno de risco.',
    'parte01: "Opcao tem rolagem Dexterity +1, RollLimit 10 - mas sem acao Failure" -> falso. A acao Failure existe (RollLimit 1) e aplica -20% de vida maxima e o status Mortally Wounded.',
    'parte01: "Efeito: XP e ouro" -> falso quanto ao ouro: ouro.dar=false; a recompensa medida e XP 1.0 para o grupo.'],
   ['O ramo de falha tem dois efeitos distintos (Party sem recompensa e Self com debuff), sendo o unique da faixa com essa composicao. Dado medido.'])

# --------------------------------------------------------------
counts = {}
for e in EVENTS:
    counts[e['veredito']] = counts.get(e['veredito'], 0) + 1

out = {
    'schema': 'ev-r2-normal-b02-corretiva/1',
    'faixa': [21, 40],
    'total_eventos': len(EVENTS),
    'contagens_veredito': counts,
    'fontes': {
        'eventos_json': 'C:/dev/stolen-realm/docs/cobertura/EV-R1/eventos.json',
        'lote_normal_md': 'C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-Normal-v2.md',
        'schema': 'C:/dev/stolen-realm/docs/cobertura/EV-R1/eventos.schema.json',
        'catalogo': 'C:/dev/stolen-realm/docs/cobertura/EV-R1/catalogo-referencias.json',
    },
    'agregados': FACTS['agregados'],
    'events': EVENTS,
}

json.dump(out, open(os.path.join(WS, 'EV-R2-NORMAL-b02-parte02-validacao.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('eventos:', len(EVENTS), 'vereditos:', counts,
      'propostas:', sum(len(e['propostas']) for e in EVENTS),
      'refutacoes:', sum(len(e['refutacoes']) for e in EVENTS))
