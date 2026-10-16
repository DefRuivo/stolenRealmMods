# -*- coding: utf-8 -*-
"""Gera os dados estruturados (EV-R2-NORMAL-b03-propostas.json) a partir das
fontes canonicas EV-R1, com redacao PT-BR acentuada e indice de acao correto.

Uso: python gen_b03_final.py
Nao escreve nas fontes; escreve apenas artefatos novos deste lote.
"""
import json, os

BASE = "C:/dev/stolen-realm"
EV = BASE + "/docs/cobertura/EV-R1/eventos.json"
OUT_JSON = BASE + "/docs/automacao/EV-R2-NORMAL-b03-propostas.json"
WS = "C:/Users/Pichau/AppData/Local/hermes/kanban/workspaces/t_99925533"

norm = [e for e in json.load(open(EV, encoding="utf-8"))["eventos"] if e["categoria"] == "Normal"]
RANGE = list(range(41, 61))
BY = {i: norm[i - 1] for i in RANGE}

RETRATACOES = [
    dict(
        id="A1", assunto="Títulos inventados #47–#51 e chave ausente",
        acusado="parte01 nomeia #47 Eternal Flame, #48 Eternal Guard, #49 Eternal Pool, #50 Exploding Skeleton e #51 Extinguished Altar. "
                "Nenhum desses títulos existe nos 256 registros do JSON, e a chave resources.assets:2545597 não é citada em lugar nenhum do documento.",
        real="Os títulos reais são #47 Etched Rune (resources.assets:2545592), #48 Fickle Fungus (:2545593), #49 Foreboding Gem (:2545595), "
             "#50 Fountain of Life (:2545596) e #51 Friend or Foe (:2545597).",
        efeito="RETRATADO INTEGRALMENTE: as seções 47–51 de parte01 não correspondem a nenhum evento da faixa. Esta parte cobre os cinco eventos reais, "
               "incluindo a chave :2545597 que faltava."),
    dict(
        id="A2", assunto="GUID duplicado #46–#51 e literais de proveniência",
        acusado="parte01 declara «CRÍTICO: Eventos 46–51 compartilham GUID duplicado 81c8fe59-5e3b-4e5e-b196-ec9bfcf44649» e recomenda corrigir os ids 46–51. "
                "Cita ainda, como proveniência, o GUID de #41 e os SHA de #54, #55, #56, #57 e #58 — nenhum deles existe na fonte.",
        real="Nenhum dos 256 registros tem o id acusado. Os seis ids reais de #46–#51 são todos distintos: 46 81c8fe59-5e3b-4e96-8148-0e89d7ce48f7; "
             "47 c8e5ace5-c340-450b-9d33-c0f525acb410; 48 9c731a7c-bbce-4c95-a4aa-fd9700ec70f0; 49 e4dc06e1-2425-4578-9cd7-087d78eb0d18; "
             "50 b6728bfa-321a-4c53-98c6-9b3d4d8f1ca1; 51 a5c05b2d-a0d7-4e95-afc6-66beff7d1a6f. O único GUID duplicado real dos 256 registros é "
             "5b740c2b-3480-48f2-997b-88c8291db0c0 em resources.assets:2545539 e :2545540 (#9 Battle e #10 Battletest Event), fora da faixa 41–60.",
        efeito="RETRATADO INTEGRALMENTE: a recomendação de corrigir os ids 46–51 fica retirada; não há defeito a corrigir nesses seis eventos. "
               "A duplicação real (#9/#10) é registrada como sinalização fora do escopo desta faixa, para cartão próprio."),
    dict(
        id="A3", assunto="Campos de texto vazios",
        acusado="parte01 fala em 2 vazios (#43 e #56), trata ambos como string estrita vazia e não cita #47.",
        real="Vazios narrativos reais da faixa: #43 Enchanted Symbol com $.texto = '\\n' (1 caractere, U+000A), #47 Etched Rune com $.texto = '\\n' "
             "(1 caractere) e #56 Hard Battle com $.texto = '' (0 caracteres). São TRÊS eventos: #43 e #47 são whitespace, não string estrita vazia; "
             "#56 é string estrita vazia. Também estão vazios os activationText dos três (0 caracteres).",
        efeito="CORRIGIDO: a contagem passa a 3 vazios (43, 47, 56), com a distinção whitespace vs string vazia explicitada e #47 presente."),
    dict(
        id="A4", assunto="Raridade Mythic de #54 e #58",
        acusado="parte01 trata a raridade Mythic como «ANOMALIA DE RARIDADE» e propõe «baixar para Common» ou «mover para lote Mythic».",
        real="#54 Gold Statue of the First Mountain King e #58 Hell Coffer têm raridade {valor:4,nome:Mythic} VERDADEIRA, categoria=Normal, peso=1.0 e "
             "pool=[{valor:0,nome:Normal}]. Não existe pool «Common»: Common é raridade, não pool. Distribuição real da faixa: 17 Common, 1 Rare (#50) e "
             "2 Mythic (#54, #58).",
        efeito="RETRATADO INTEGRALMENTE: retiradas a acusação de inconsistência e qualquer proposta de downgrade ou de movimentação de lote. Raridade e pool "
               "são campos independentes e ambos estão coerentes na fonte."),
    dict(
        id="A5", assunto="Enchanted Obelisk (#41) «sem cura»",
        acusado="parte01 afirma «vida_mana tem todos os valores 0.0 — nenhuma cura ou mana é aplicada em runtime» e propõe percentCurHealth = 0.25 e "
                "percentMaxMana = 0.15.",
        real="A opção 2, «Heal from the obelisk», já tem opcoes[2].efeitos[1].efeitos[1].vida_mana = {percentMaxHealth:50.0, percentMaxMana:50.0, "
             "percentCurHealth:0.0, percentCurMana:0.0}: 50% de vida e de mana MÁXIMAS estão configurados. A opção 1 grava o status Brilliance "
             "(resources.assets:2545415, «@Intelligence@ increased by {4,20}», duração Quest, tipo Fortune).",
        efeito="RETRATADO INTEGRALMENTE: não existe cura zero demonstrada em #41 e a proposta 0.25/0.15 é retirada — além de sem base, 0.25/0.15 seriam "
               "frações, enquanto os campos do jogo são percentuais (a fonte grava 50.0)."),
    dict(
        id="A6", assunto="Opções inventadas em #53, #59 e #60",
        acusado="parte01 descreve #53 com as opções «Attack» e «Sneak past»; #59 com «Enter» e «Close»; #60 com «Disable — Brave the flames to disable the trap».",
        real="#53 Goblin Scout Tower tem UMA opção, «Strike silently» (rolagem Dexterity +1): Success com limite_rolagem 12 e sem batalha, e Failure com "
             "limite_rolagem 1 iniciando batalha com 1 inimigo forçado. #59 Hell Gate tem «Wait» e «Leave». #60 Hold your Breath tem UMA opção, «Claim» "
             "(Vitality +2, Success com limite 14, Failure com limite 0 e -35 percentMaxHealth em Self).",
        efeito="RETRATADO INTEGRALMENTE: as propostas de melhorar, renomear ou subtitular opções inexistentes são retiradas; nenhuma opção é criada, "
               "removida ou renomeada."),
    dict(
        id="A7", assunto="Contagens do corpo, ordinal de #60 e português",
        acusado="parte01 fecha com «MANTER 14» e «MELHORAR 6» listando 13 e 7 nomes, numera Hold your Breath como 56 no quadro de visão geral (duplicando "
                "Hard Battle), usa «oubuff» (L343), «interrupto» (L366) e «goblnica» (L393) e contém 28 escapes de aspas desnecessários.",
        real="As 20 seções de parte01 contêm, de fato, 13 MANTER e 7 MELHORAR; Hold your Breath é o ordinal 60 (resources.assets:2545609); as palavras "
             "corretas são «ou buff», «interruptor» e «goblínica».",
        efeito="CORRIGIDO: esta parte usa o ordinal 60 para Hold your Breath, fecha em 13 MANTER / 7 MELHORAR e não usa escapes de aspas nem os erros de "
               "digitação citados."),
]

def opt_summary(e):
    out = []
    for o in e["opcoes"]:
        acts = []
        for a in o["efeitos"]:
            acts.append(dict(indice=a["indice"], resultado=a["resultado"]["nome"], limite=a["limite_rolagem"],
                             batalha=bool(a["batalha"]["iniciar"])))
        out.append(dict(indice=o["indice"], titulo=o["titulo"], texto=o["texto"],
                        rolagem_bonus=[b["nome"] for b in o["rolagem"]["bonus"]],
                        misteriosa=bool(o["rolagem"]["misteriosa"]), acoes=acts))
    return out

EVENTOS = {}

def ev(n, veredito, natureza, justificativa, propostas=None, sinalizacoes=None, retratacao=""):
    e = BY[n]
    EVENTOS[n] = dict(
        ordinal=n, chave=e["chave"], id=e["id"], titulo=e["titulo"], categoria=e["categoria"],
        nome_asset=e["nome_asset"], raridade=e["raridade"], peso=e["peso"],
        pool=[p["nome"] for p in e["pool"]], disabled=e["condicoes"]["disabled"],
        historia=e["historia"]["nome"], modos=[m["nome"] for m in e["modos"]],
        isLesserEvent=e["condicoes"]["isLesserEvent"], LeadsToFortune=e["condicoes"]["LeadsToFortune"],
        allowedNodeTypes=e["condicoes"]["allowedNodeTypes"], minLevel=e["condicoes"]["minLevel"],
        allowedTerrainTypes=e["condicoes"]["allowedTerrainTypes"],
        sha256_objeto=e["origem"]["sha256_objeto"], path_id=e["origem"]["path_id"],
        texto=e["texto"], texto_len=len(e["texto"]),
        texto_vazio_estrito=(e["texto"] == ""),
        texto_so_whitespace=(e["texto"] != "" and e["texto"].strip() == ""),
        texto_resultados_possiveis=e["texto_resultados_possiveis"],
        opcoes=opt_summary(e),
        veredito=veredito, natureza=natureza, justificativa=justificativa,
        propostas=propostas or [], sinalizacoes=sinalizacoes or [], retratacao=retratacao,
    )

ev(41, "MANTER", "—",
   "MANTER. As duas opções são distintas em efeito E em narrativa: «Activate the blessing» grava o status Brilliance "
   "(opcoes[1].efeitos[1].efeitos[1].recompensas.status.candidatos[1] = resources.assets:2545415, «@Intelligence@ increased by {4,20}», duração Quest) e "
   "«Heal from the obelisk» grava vida_mana {percentMaxHealth:50.0, percentMaxMana:50.0} em Self. Os activationText de sucesso também diferem entre as "
   "opções («a pulse of energy courses through» contra «The magic flows into»). Não há cura zero, não há texto idêntico entre as opções e não há defeito de "
   "configuração demonstrado. Sem alteração proposta.",
   sinalizacoes=["Chave e GUID reais desta seção diferem dos que parte01 citou: o GUID acusado 36c51484-b50b-4681-9e7f-6006b9c27192 não existe; o real é "
                 "36c51484-b50b-4627-a9a7-64d221a22f1a (ver A2 e A5)."],
   retratacao="Supersede a seção 41 e as recomendações 1–2 de parte01 (cura inerte e valores 0.25/0.15).")

ev(42, "MANTER", "—",
   "MANTER. «Take» inicia batalha no sucesso (opcoes[1].efeitos[1].batalha.iniciar = true, referência resources.assets:2544645 «Cursed Chest Battle», "
   "1 ForcedEnemy com m_PathID 2545119 e VictoryEvent :2545586) e o texto de sucesso descreve exatamente a armadilha do espantalho («a sudden grip, cold and "
   "iron-hard»). «Leave» não inicia batalha nem aplica efeito. Texto e configuração estão alinhados. Sem alteração proposta.",
   sinalizacoes=["O GUID real é 3bda807e-075d-45e3-afe7-b9d0f9d4b34c; o literal citado por parte01 (3bda807e-075d-454a-b095-476036a90c8f) não existe."])

ev(43, "MELHORAR", "SUGESTAO DE ALTERACAO DO TEXTO ORIGINAL (vazio) - ingles (EN)",
   "MELHORAR. Evento menor (isLesserEvent=1) sem nenhuma narrativa: $.texto = '\\n' (1 caractere) e "
   "$.opcoes[1].efeitos[1].campos_originais.activationText = '' (0 caracteres). A única descrição de opção é «Grants [o1a1_status].», remissão ao candidato "
   "do catálogo (status Intelligence, resources.assets:2545387). O evento concede um status real, mas o jogador não recebe contexto algum. Proponho texto "
   "exato, em inglês, para os dois campos vazios e uma descrição autoral no lugar da remissão; não proponho mudar título, status, raridade, peso ou condições. "
   "Textos propostos em inglês, mesma língua do campo original — NÃO é tradução PT-BR.",
   propostas=[
       dict(jsonpath="$.texto", antes="\n",
            depois="A symbol is etched into the stone here, its lines too regular to be anything natural and too worn to be recent. A faint warmth comes off the mark, as though something patient were waiting inside it.",
            nota="CAMPO completo (hoje whitespace). Sugestão de texto original, inglês (EN)."),
       dict(jsonpath="$.opcoes[1].efeitos[1].campos_originais.activationText", antes="",
            depois="You lay your hand against the symbol. The warmth climbs your arm, your thoughts sharpen to a fine edge, and the mark dims to a dull, spent grey.",
            nota="CAMPO completo (hoje vazio). Sugestão de texto original, EN. Não altera o status concedido."),
       dict(jsonpath="$.opcoes[1].texto", antes="Grants [o1a1_status].",
            depois="Trace the symbol's lines and take what it offers.",
            nota="CAMPO completo. Substitui a remissão ao placeholder por descrição autoral."),
   ],
   sinalizacoes=["O placeholder [o1a1_status] não prova falha de renderização: o JSON resolve o candidato (Intelligence, resources.assets:2545387) e o "
                 "resultado efetivo depende do runtime, que NÃO foi exercitado."])

ev(44, "MANTER", "—",
   "MANTER. «Help» tem rolagem automática (bonus vazio) com Success em limite_rolagem 11 e Failure em limite_rolagem 1; o sucesso concede o status "
   "«Boar Charm» (resources.assets:2545413, invocação de Wild Boar) e a falha aplica -30 percentMaxHealth em Self junto do status «Restrained» "
   "(2545498, «Reduces @Reflex@ by @20%@ per stack»). «Leave» não tem efeito. Narrativa de sucesso e falha bem diferenciadas, efeito real conferido. "
   "Sem alteração proposta.",
   sinalizacoes=["O GUID real é ad2b9f6c-46c8-4e66-ae0d-8825c3948d41; o literal citado por parte01 (ad2b9f6c-46c8-4e6e-b196-ec9bfcf44649) não existe."])

ev(45, "MANTER", "—",
   "MANTER. Opção única «React» com rolagem bonus = [{valor:4,nome:Reflex}]: Success em limite 10 concede experiência a Party com razão 0.5; Failure em "
   "limite 1 concede XP 0.5 a Party e aplica -30 percentMaxHealth em Self junto do status «Severely Burned» (resources.assets:2545499, «Reduces @Fire "
   "Resistance@ by @25%@ per stack»). As quantidades finais são NULL por dependerem de estado de partida (NAO_EXERCITADO). Sem alteração proposta.")

ev(46, "MANTER", "—",
   "MANTER. O id real é 81c8fe59-5e3b-4e96-8148-0e89d7ce48f7, distinto de todos os demais: NÃO há GUID duplicado nesta faixa. As duas opções diferem em "
   "efeito (a opção 1 grava o status «Strength» em Self; a opção 2 grava vida_mana 50%/50%) e em texto de sucesso. Sem alteração proposta.",
   retratacao="Supersede integralmente a seção 46 e a «ANOMALIA CRÍTICA» de GUID duplicado (ver A2).")

ev(47, "MELHORAR", "SUGESTAO DE ALTERACAO DO TEXTO ORIGINAL (vazio) - ingles (EN)",
   "MELHORAR. Evento menor (isLesserEvent=1, história Both) sem narrativa: $.texto = '\\n' (1 caractere) e "
   "$.opcoes[1].efeitos[1].campos_originais.activationText = '' (0 caracteres). A descrição da opção é «Grants [o1a1_status].». O status concedido é real e "
   "distinto do de #43 («Might», resources.assets:2545388). Este evento foi OMITIDO por parte01, que o substituiu pelo título inexistente «Eternal Flame», e "
   "passa a ser tratado explicitamente aqui. Proponho texto exato, em inglês, para os dois campos vazios.",
   propostas=[
       dict(jsonpath="$.texto", antes="\n",
            depois="A single rune is cut deep into the floor, its channels dark with age. Nothing about it is lit, yet the air above it bends as though seen through heat.",
            nota="CAMPO completo (hoje whitespace). Sugestão de texto original, inglês (EN)."),
       dict(jsonpath="$.opcoes[1].efeitos[1].campos_originais.activationText", antes="",
            depois="[name] crouches and presses [his] palm flat against the rune. Strength floods through [him] - brief, blunt and unmistakable - and the mark goes dark.",
            nota="CAMPO completo (hoje vazio). Sugestão de texto original, EN. Placeholders [name] e [his] preservados no padrão do jogo."),
       dict(jsonpath="$.opcoes[1].texto", antes="Grants [o1a1_status].",
            depois="Press your hand to the rune and take its strength.",
            nota="CAMPO completo. Substitui a remissão ao placeholder por descrição autoral."),
   ],
   retratacao="A seção 47 de parte01 (título «Eternal Flame», GUID inexistente e texto inventado) é substituída integralmente por este evento real.",
   sinalizacoes=["O placeholder [o1a1_status] não prova falha de renderização (mesmo motivo de #43); runtime NAO_EXERCITADO."])

ev(48, "MANTER", "—",
   "MANTER. Opção única «Resist»: Success em limite 10 (XP 0.5 a Party) e Failure em limite 0 (-30 percentMaxHealth em Self junto do status «Enfeebled»). "
   "O texto original já descreve a nuvem de esporos tóxicos, coerente com a rolagem de resistência. Sem alteração proposta.",
   retratacao="A seção 48 de parte01 (título inventado «Eternal Guard», GUID duplicado falso) é substituída integralmente por este evento real.")

ev(49, "MANTER", "—",
   "MANTER. «Take» inicia batalha no sucesso (batalha.iniciar = true, com ForcedEnemies vazio e referência nula — usa o BattleInfo do próprio evento, "
   "BattlePointValue 16 —, com VictoryEvent = `resources.assets:2545594` «Foreboding Gem - Victory» e FailureEvent nulo) e o texto descreve a corrida pela gema e o confronto com os outros aventureiros; «Leave» não tem batalha. LeadsToFortune=1 e terreno [4]. "
   "Configuração e narrativa estão coerentes entre si. Sem alteração proposta.",
   sinalizacoes=["Bytes residuais: $.opcoes[1].efeitos[1].campos_originais.activationText termina com «\\r\\n\\r» (2 CR, ambos no fim da string). Não proponho "
                 "alteração porque, sendo fim de string, não há quebra visível nem efeito de conteúdo — fica registrado para referência. Os casos com CR no "
                 "MEIO da string (54, 59 e 60) recebem proposta de normalização."])

ev(50, "MANTER", "—",
   "MANTER. «Drink» aplica vida_mana {percentMaxHealth:10.0, percentMaxMana:10.0} em Self, com Success único em limite 0 e sem ação de falha. O texto é curto "
   "(42 caracteres) mas funcional; isLesserEvent=1 e raridade Rare (valor 2) são campos reais e coerentes. Sem alteração proposta.")

ev(51, "MANTER", "—",
   "MANTER. Evento DESATIVADO (condicoes.disabled=1) — o único da faixa — com allowedNodeTypes=[0]. As opções reais são «Persuade» (Success em limite 10: "
   "vida_mana +20/20 em Self, XP 1.0 e itens com limitItemTypes=1 e raridades [1,2,3]; Failure em limite 0 com batalha) e «Fight» (batalha no sucesso único). "
   "Estar desativado não autoriza reativar nem remover conteúdo por padrão, e não há defeito demonstrado nas opções reais. Sem alteração proposta.",
   retratacao="A seção 51 de parte01 (título inexistente «Extinguished Altar», chave ausente) é substituída integralmente por este evento real.")

ev(52, "MANTER", "—",
   "MANTER. «Disable» com rolagem bonus = [{valor:4,nome:Reflex}]: Success em limite 10 concede XP a Party (razão 1.0); Failure em limite 1 concede XP 0.5 a "
   "Party e aplica -30 percentMaxHealth em Self junto do status «Severely Burned». O sha256_objeto do evento é exatamente o citado por parte01 "
   "(b01526f476347afe1a0a0ffc793b0bcc86a49f6197fa7ec8345cbe27f0c93d45). Sem alteração proposta.")

ev(53, "MANTER", "—",
   "MANTER, com sinalizações. O evento tem UMA opção real, «Strike silently» (rolagem bonus = [{valor:1,nome:Dexterity}]): Success em limite 12 concede XP 1.0 "
   "a Party sem iniciar batalha; Failure em limite 1 inicia batalha com 1 inimigo forçado. Não existem as opções «Attack» e «Sneak past» atribuídas por "
   "parte01 e não há defeito demonstrado nas opções reais. Sem alteração proposta.",
   retratacao="Supersede integralmente a seção 53 de parte01 (opções inventadas e MELHORAR sobre opção inexistente).",
   sinalizacoes=["$.opcoes[1].texto (descrição da opção) está vazio (''). O mesmo ocorre em #56 («Fight!») e, no campo equivalente, em #43 e #47. Regra desta "
                 "parte: só proponho texto onde o EVENTO não tem narrativa alguma ($.texto e activationText vazios: casos 43, 47 e 56); descrição de opção "
                 "vazia isolada não é defeito por si — registrada sem proposta.",
                 "O fato de o texto de falha repetir a abertura do texto de sucesso («With an expert hand, [name] strikes...») é estilo do asset, não erro de dado."])

ev(54, "MELHORAR", "SUGESTAO DE ALTERACAO DO TEXTO ORIGINAL (normalizacao de bytes CR) - ingles (EN)",
   "MELHORAR. Identidade, raridade (Mythic, valor 4), pool (Normal), peso, condições e efeitos estão corretos e NÃO são propostos para mudança (ver A4). "
   "O defeito real é de bytes: o asset mistura CR LF com LF. $.opcoes[1].efeitos[1].campos_originais.activationText («Steal») usa «\\r\\n\\r\\n» no meio do "
   "texto, enquanto o restante do campo usa «\\n\\n», e $.opcoes[2].texto («Leave») termina com «\\r». Proponho apenas normalizar para o padrão do próprio "
   "campo; nenhuma palavra, tag ou placeholder é alterado.",
   propostas=[
       dict(jsonpath="$.opcoes[1].efeitos[1].campos_originais.activationText",
            antes="determination.\r\n\r\nYou pause awkwardly",
            depois="determination.\n\nYou pause awkwardly",
            nota="TRECHO. Remove 2 caracteres CR; preserva LF, espaços e os demais bytes."),
       dict(jsonpath="$.opcoes[2].texto", antes="dwarven culture.\r", depois="dwarven culture.",
            nota="TRECHO final. Remove 1 CR final; preserva todo o resto, inclusive o apóstrofo e o ponto."),
   ],
   retratacao="Supersede a seção 54 de parte01: a «ANOMALIA DE RARIDADE» e o downgrade para Common ficam retirados (A4), e os GUID/SHA citados por parte01 "
              "não correspondem à fonte.",
   sinalizacoes=["$.opcoes[1].efeitos[1].batalha.referencia = resources.assets:2544646 «Gold Statue of the First Mountain King Battle», com 2 ForcedEnemies: "
                 "BattleInfo própria do evento, coerente. Registrado, sem proposta."])

ev(55, "MANTER", "—",
   "MANTER. «Disable» com rolagem bonus = [{valor:1,nome:Dexterity}]: Success em limite 10 concede XP 1.0 a Party; Failure em limite 1 aplica "
   "-30 percentMaxHealth em Party junto do status «Visually Impaired». Texto, rolagem e efeitos são internamente coerentes, e o sha256_objeto real é "
   "cb553ab3c082faf152bd47cabba6d79301c8d58d8e411673bf80b3e72c439bd6 (o literal citado por parte01, "
   "e7c7c5b9e3b7e4a8f1d2c6b5a9e8d7c6b5a4e3d2c1b0a9f8e7d6c5b4a3e2d1c0, não existe). Não proponho alteração de balanceamento.",
   sinalizacoes=["Divergência de alvo, registrada SEM proposta: #55 é o único evento da faixa cujo dano de falha mira Party; #52, armadilha irmã, mira Self e "
                 "dá XP de consolo a Party. Se o dono decidir uniformizar, os campos seriam: campo `alvo` da falha em "
                 "$.opcoes[1].efeitos[2].efeitos[1].alvo.tipo_override; candidato Party (2) -> Self (0); valor hoje {valor:2,nome:Party}; condição: somente o "
                 "efeito de -30 percentMaxHealth e o status «Visually Impaired» daquela ação. NÃO é proposta deste parecer e não altera o veredito MANTER."])

ev(56, "MELHORAR", "SUGESTAO DE ALTERACAO DO TEXTO ORIGINAL (vazio) - ingles (EN)",
   "MELHORAR. É o único evento de combate da faixa (allowedNodeTypes=[1], história Both) e está totalmente sem texto: $.texto = '' (0 caracteres, string "
   "estrita vazia), $.texto_resultados_possiveis = '', $.opcoes[1].texto = '' e o activationText do sucesso único = ''. A única opção, «Fight!», inicia "
   "batalha (batalha.iniciar = true com referência nula: usa o BattleInfo do próprio evento; itens restritos a possibleItemTypes=[0] e raridades [1,2,3]). "
   "Proponho texto exato, em inglês, para os três campos vazios; não altero título, opção, ids, batalha nem recompensa.",
   propostas=[
       dict(jsonpath="$.texto", antes="",
            depois="A wall of armed figures bars the way, weapons already bared. No words are offered and none are asked for - only the scrape of steel and the first rush of boots on stone.",
            nota="CAMPO completo (hoje vazio). Sugestão de texto original, inglês (EN)."),
       dict(jsonpath="$.opcoes[1].texto", antes="", depois="Draw your weapon and meet them head on.",
            nota="CAMPO completo (hoje vazio). Sugestão de texto original, EN."),
       dict(jsonpath="$.opcoes[1].efeitos[1].campos_originais.activationText", antes="",
            depois="Steel meets steel, and the fight is joined.",
            nota="CAMPO completo (hoje vazio). Sugestão de texto original, EN."),
   ],
   retratacao="Supersede a seção 56 de parte01: o documento anterior descrevia «Hard Battle» com GUID duplicado falso, «Nulls: 7» e textos de sucesso e falha "
              "inexistentes — o evento tem UMA ação, Success, com batalha.")

ev(57, "MANTER", "—",
   "MANTER. «Attempt» com rolagem bonus = [{valor:1,nome:Dexterity}] e rolagem misteriosa (misteriosa=true, texto_misterioso vazio): Success em limite 14 "
   "concede ouro a Party com razão 15.0 (quantidade_final NULL = NAO_EXERCITADO) e itens restritos a raridades [3,4]; Failure em limite 1 aplica os status "
   "«Confused» e «Fatigued». «Leave» não tem efeito. Sem alteração proposta.",
   sinalizacoes=["O sha256_objeto real é 848015627b3cfaf0c5cdea5144437fc249f23bd796a7487927c1ddda3882d78f; o literal citado por parte01 "
                 "(c5b4a3e2d1c0b9a8f7e6d5c4b3a2e1d0c9b8a7f6e5d4c3b2a1e0d9c8b7a6e5d4) não existe."])

ev(58, "MELHORAR", "SUGESTAO DE ALTERACAO DO TEXTO ORIGINAL (erro literal) - ingles (EN)",
   "MELHORAR. Identidade, raridade (Mythic, valor 4), pool (Normal) e LeadsToFortune=1 estão corretos e não são propostos para mudança (ver A4). O defeito "
   "real é lexical: $.opcoes[2].texto («Leave») escreve «devlish», forma que não existe em inglês («devilish»). Correção literal de uma palavra, sem tocar "
   "efeitos, batalha (a opção 1 usa resources.assets:2544646 com 7 ForcedEnemies) nem raridade.",
   propostas=[
       dict(jsonpath="$.opcoes[2].texto", antes="Think better of falling for this devlish trap.",
            depois="Think better of falling for this devilish trap.",
            nota="TRECHO. Substitui «devlish» por «devilish»; o restante do campo fica inalterado."),
   ],
   retratacao="Supersede a seção 58 de parte01: a «ANOMALIA DE RARIDADE» e o MELHORAR por raridade ficam retirados (A4). O sha256_objeto real é "
              "f1803712ec88905b8075eee409b77ba21f335d9142ee90dbbf24592222c64aca; o literal de parte01, de comprimento incompatível, não existe.")

ev(59, "MELHORAR", "SUGESTAO DE ALTERACAO DO TEXTO ORIGINAL (gramatica e bytes CR) - ingles (EN)",
   "MELHORAR. As opções reais são «Wait» e «Leave» — nenhuma opção é criada, renomeada ou removida (ver A6). O texto de «Leave» tem erro gramatical (falta "
   "«to» antes de «wait around») e o activationText de «Wait» mistura CR LF com LF em dois pontos, além de faltar o espaço depois da vírgula em "
   "«\"Wrong turn,\"he mutters». Proponho a correção literal e a normalização de bytes; nada mais muda.",
   propostas=[
       dict(jsonpath="$.opcoes[2].texto",
            antes="No amount of curiosity can convince you wait around to see what exits this Infernal Portal.",
            depois="No amount of curiosity can convince you to wait around to see what exits this Infernal Portal.",
            nota="TRECHO. Insere «to». O restante do campo fica inalterado."),
       dict(jsonpath="$.opcoes[1].efeitos[1].campos_originais.activationText",
            antes="confusion.\r\n\r\n\"Wrong turn,\"he mutters",
            depois="confusion.\n\n\"Wrong turn,\" he mutters",
            nota="TRECHO. Remove 2 CR e insere 1 espaço depois da vírgula; preserva LF e o restante do campo."),
       dict(jsonpath="$.opcoes[1].efeitos[1].campos_originais.activationText",
            antes="surprised?\"\r\n\r\nDespite the dire circumstances",
            depois="surprised?\"\n\nDespite the dire circumstances",
            nota="TRECHO. Remove 2 CR; preserva LF e o restante do campo."),
   ],
   retratacao="Supersede a seção 59 de parte01 (opções inventadas «Enter» e «Close», subtítulos propostos e MELHORAR por clareza sobre opções inexistentes).",
   sinalizacoes=["O sucesso de «Wait» inicia batalha (1 ForcedEnemy) e aplica «Severely Burned» em Self; a narrativa descreve Lord Infernicus emergindo do "
                 "portal. Registrado como observação de design, sem proposta."])

ev(60, "MELHORAR", "SUGESTAO DE ALTERACAO DO TEXTO ORIGINAL (normalizacao de bytes CR) - ingles (EN)",
   "MELHORAR. Ordinal corrigido: Hold your Breath é o ordinal 60 (resources.assets:2545609) — parte01 o numerava 56 no quadro de visão geral, duplicando Hard "
   "Battle (ver A7). A opção real é ÚNICA, «Claim» (rolagem bonus = [{valor:2,nome:Vitality}]): Success em limite 14 concede XP 1.0 e itens (raridades [3,4]) a "
   "Party; Failure em limite 0 aplica -35 percentMaxHealth em Self. Nenhuma opção é criada ou renomeada (ver A6). O defeito real é de bytes: em $.texto o "
   "separador entre o primeiro e o segundo parágrafo é «\\r\\n\\r\\n», enquanto o restante do campo usa «\\n\\n».",
   propostas=[
       dict(jsonpath="$.texto", antes="tube of water.\r\n\r\nGlowing fish",
            depois="tube of water.\n\nGlowing fish",
            nota="TRECHO. Remove 2 CR; preserva LF, espaços e o restante do texto (811 caracteres hoje)."),
   ],
   retratacao="Supersede a seção 60 de parte01 (título «Disable — Brave the flames to disable the trap», copiado de Furnace Trap, e RollLimit 14/0 descritos "
              "como ambíguos) e corrige o ordinal do evento no quadro de visão geral.")

assert len(EVENTOS) == 20, len(EVENTOS)
manter = [n for n in RANGE if EVENTOS[n]["veredito"] == "MANTER"]
melhorar = [n for n in RANGE if EVENTOS[n]["veredito"] == "MELHORAR"]

data = dict(
    lote="b03", faixa=[41, 60], categoria="Normal", total=20,
    vereditos=dict(MANTER=manter, MELHORAR=melhorar),
    retratacoes=RETRATACOES, eventos=[EVENTOS[n] for n in RANGE],
)
os.makedirs(WS, exist_ok=True)
json.dump(data, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("MANTER", len(manter), manter)
print("MELHORAR", len(melhorar), melhorar)
print("OUT_JSON", OUT_JSON)
