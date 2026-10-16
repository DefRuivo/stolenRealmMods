"""EV-R2-NORMAL-b01-parte02 — gera a validação estruturada (propostas, vereditos, contagens).

Somente leitura das fontes EV-R1. Não edita originais, EV-R1, jogo ou plugins.
Uso: python b01_parte02.py gen
"""
import json, os, sys, hashlib

SRC = "C:/dev/stolen-realm/docs/cobertura/EV-R1"
DEST = "C:/dev/stolen-realm/docs/automacao"
BASE = os.path.dirname(os.path.abspath(__file__))

FONTES = ["eventos.json", "lote-Normal-v2.md", "eventos.schema.json", "catalogo-referencias.json"]
BASE_SHA = {
    "eventos.json": "4a8decac7e98a2b0bf8692057a57789a71b94c230e3b9ca93817f039c86d1d13",
    "lote-Normal-v2.md": "83b30ada3d78e596b8c7c0784d5e741b43654b14ab02d5377d8a1b245b84f146",
    "eventos.schema.json": "6950ec43deba94143150f0584bb87ca5406b3ef16f1ae2f18ad8aa943a62b3bc",
    "catalogo-referencias.json": "94077cc887621933abe7bbbbd96e91c5a887478dba8fd000b8f4a4129c3745a5",
}


def load_events():
    with open(os.path.join(SRC, "eventos.json"), encoding="utf-8") as f:
        ev = json.load(f)["eventos"]
    return [e for e in ev if e.get("categoria") == "Normal"][:20]


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


GHOST = "The yearning ghost extends her hand pleading for help."
REACH = "You reach out to the ghost. Gain [o1a1_status]."
REACH_ACT = ("You reach out, but your hand passes through cold air. Memories flood your mind and longing fills your heart."
             "\n\nYou gain [o1a1_status].")
LEAVE = "The chill in the air causes you to hesitate. You leave without helping."

# ---------------------------------------------------------------------------
# RECORDS: 20 registros. Vereditos MANTER=7 (5,11,12,15,16,17,18) / MELHORAR=13.
# Propostas: tipo CAMPO (substitui a string inteira do campo) ou TRECHO (substitui
# exatamente o trecho citado dentro do campo). "antes" é literal conferido na fonte.
# ---------------------------------------------------------------------------
R = {}

R[1] = dict(
    veredito="MELHORAR", natureza="texto-de-opcao com placeholder sem status configurado (slot disabled observado, sem reativação proposta)",
    justificativa=[
        "Texto do evento (54 chars) reaparece literalmente em #8 e #14.",
        "Opção 1 'Reach' pede '[o1a1_status]' no texto, mas $.opcoes[0].condicoes.status_requeridos[0] é PPtr nulo (m_PathID=0) e $.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos=[] — nenhum status é concedido.",
        "$.condicoes.disabled=1: registrado como estado, não como defeito a corrigir por inferência.",
    ],
    props=[
        dict(code="1.1", tipo="CAMPO", path="$.opcoes[0].texto", antes=REACH,
             depois="You reach out to the ghost.",
             nota="Remove o token sem candidato configurado. Alternativa de autoria: configurar status real em $.opcoes[0].condicoes.status_requeridos[0] e $.opcoes[0].efeitos[0].efeitos[0].recompensas.status.candidatos (não propomos status inventado)."),
        dict(code="1.2", tipo="CAMPO", path="$.opcoes[0].efeitos[0].texto", antes=REACH_ACT,
             depois="You reach out, but your hand passes through cold air. Memories flood your mind and longing fills your heart.",
             nota="Idem 1.1 na prosa de ativação; mesmo placeholder, mesmo campo vazio de candidatos."),
    ])

R[2] = dict(
    veredito="MELHORAR", natureza="typo no texto original (sugestão de correção do ORIGINAL, não do EV-R1)",
    justificativa=[
        "Literal real do original é 'appeares' (a parte01 citou 'appeaures', que não existe na fonte).",
        "Opção única 'Disable' com bonus={valor:2,nome:Vitality}; Success limite 10 concede experiência (dar=true); Failure limite 1 aplica -20 percentMaxHealth e status Battered (resources.assets:2545489).",
        "Acrescentar opção 'Leave' seria mudança de conteúdo (decisão do autor), não correção de texto — não proposta aqui.",
    ],
    props=[
        dict(code="2.1", tipo="TRECHO", path="$.texto", antes="appeares", depois="appears",
             nota="antes→depois do TEXTO ORIGINAL; nenhum arquivo do jogo/EV-R1 é editado."),
    ])

R[3] = dict(
    veredito="MELHORAR", natureza="descrição de opção ausente",
    justificativa=[
        "As três opções têm $.opcoes[*].texto='' (vazio) e $.opcoes[*].rolagem.misteriosa=true.",
        "Alegação de recompensa da parte01 REFUTADA pelo catálogo: $.opcoes[0].efeitos[*].efeitos[0].recompensas.itens.dar=true com tabelas mustGetOne=1/Chance=100 — opção 1: Bottled Anger(2546488)/Rage(2546491)/Fury(2546489)/Wrath(2546492); opção 2: Oil of Momentum(2546526)/Speed(2546528)/Alacrity(2546525)/Acceleration(2546524); opção 3: Potion of Endurance(2546549)/Vitality(2546553)/Fortitude(2546550)/Life(2546551).",
        "$.opcoes[*].rolagem.bonus=[{valor:3,nome:Intelligence}] (RollBonusType 3=Intelligence): bônus de rolagem configurado, não vazio.",
        "As quatro ações de cada opção têm limite_rolagem 1/6/12/16, todas Success (sem Failure).",
    ],
    props=[
        dict(code="3.1", tipo="CAMPO", path="$.opcoes[0].texto", antes="",
             depois="Brew the crimson draught the scroll describes.",
             nota="Fundamentado na ação 1: 'should turn a bright red'."),
        dict(code="3.2", tipo="CAMPO", path="$.opcoes[1].texto", antes="",
             depois="Mix the sweet-smelling draught the scroll describes.",
             nota="Fundamentado na ação 1: 'should release a sweet aroma'."),
        dict(code="3.3", tipo="CAMPO", path="$.opcoes[2].texto", antes="",
             depois="Prepare the silver tonic the scroll describes.",
             nota="Fundamentado na ação 1: 'should turn a bright silver'."),
    ])

R[4] = dict(
    veredito="MELHORAR", natureza="descrição de opção ausente + estrutura de rolagem observada",
    justificativa=[
        "$.opcoes[0].titulo='Steel Yourself', $.opcoes[0].texto='' (vazio).",
        "$.opcoes[0].efeitos[0] (Success, limite_rolagem=10) e $.opcoes[0].efeitos[1] (Failure, limite_rolagem=0) ambos com batalha.iniciar=true: a rolagem muda o texto, não o resultado (combate nos dois ramos).",
        "allowedNodeTypes=[0] (NodeType 0=NormalFight) e minLevel=2; $.condicoes.disabled=1 registrado como estado — não propomos reativar nem criar/remover opções.",
    ],
    props=[
        dict(code="4.1", tipo="CAMPO", path="$.opcoes[0].texto", antes="",
             depois="Steady your nerves — the ambush springs either way.",
             nota="Fundamentado nos dois textos de ação reais ('you ready yourself for battle' / 'your enemies surround you')."),
    ])

R[5] = dict(
    veredito="MANTER", natureza="—",
    justificativa=[
        "Texto de 611 chars com falas e tags de realce; duas opções (Accept/Leave) e $.condicoes.LeadsToFortune=1.",
        "Accept tem $.opcoes[0].rolagem.bonus=[{0,Might},{1,Dexterity}]; Success limite 12 concede ouro (razao 6.0) e status 'Point Blank' (2545463); Failure limite 0 concede ouro (razao 3.0) e status Fatigued(2545495)/Weakened(2545504).",
        "'Gobin Hood' é jogo de palavras intencional (goblin + Robin Hood), não erro de digitação.",
    ], props=[])

R[6] = dict(
    veredito="MELHORAR", natureza="texto narrativo ausente (evento de tesouro)",
    justificativa=[
        "$.texto='' (0 chars) e a única ação (Success limite 0) também tem texto vazio.",
        "allowedNodeTypes=[3] (NodeType 3=Treasure), raridade Uncommon(1), $.opcoes[0].efeitos[0].efeitos[0].recompensas.itens: dar=true, quantidade_configurada=2, possibleRarities=[2,3] (ItemQuality 2=Rare,3=Legendary).",
        "#6 e #7 NÃO são cópias totais: #6 concede 2 itens e vem de 'events/armor chest - roguelike'; #7 concede 1 item e vem de 'events/armor chest'.",
    ],
    props=[
        dict(code="6.1", tipo="CAMPO", path="$.texto", antes="",
             depois="An iron-banded armor chest waits beside the path, its hinges dark with age.",
             nota="Cena ancorada no nó de tesouro e na raridade Uncommon do próprio asset."),
    ])

R[7] = dict(
    veredito="MELHORAR", natureza="texto narrativo ausente (evento de tesouro, variante de #6)",
    justificativa=[
        "$.texto='' (0 chars); ação única Success limite 0 com texto vazio.",
        "Distingue-se de #6 por direito: $.opcoes[0].efeitos[0].efeitos[0].recompensas.itens.quantidade_configurada=1 (contra 2 em #6) e caminho de asset próprio ('events/armor chest').",
        "Mesmo título não implica duplicata — chaves (2545536 / 2545537), ids e caminhos de recurso são distintos.",
    ],
    props=[
        dict(code="7.1", tipo="CAMPO", path="$.texto", antes="",
             depois="A weathered armor chest lies half-buried by the roadside, a single piece of gear rattling inside.",
             nota="O 'single piece' espelha quantidade_configurada=1, diferenciando a cena da de #6."),
    ])

R[8] = dict(
    veredito="MELHORAR", natureza="texto incompatível com o título (reuso literal do texto de #1/#14)",
    justificativa=[
        "$.texto é literalmente o mesmo de #1 e #14, mas o título é 'Barbarian Fisherman'.",
        "As duas opções e seus textos de ação também são os do encontro do fantasma (opção 1 concede status Ethereal, 2545439).",
        "$.condicoes.disabled=1: registrado como estado; NÃO propomos reativar o slot.",
    ],
    props=[
        dict(code="8.1", tipo="CAMPO", path="$.texto", antes=GHOST,
             depois="A broad-shouldered barbarian kneels at the riverbank, hauling in a catch with both hands and a grin full of broken teeth.",
             nota="Alinha a cena ao título real do asset."),
        dict(code="8.2", tipo="CAMPO", path="$.opcoes[0].texto", antes=REACH,
             depois="Lend the barbarian a hand with the line.",
             nota="Mantém a opção 1 como a que concede o status Ethereal do asset."),
        dict(code="8.3", tipo="CAMPO", path="$.opcoes[1].texto", antes=LEAVE,
             depois="Leave the fisherman to his catch.",
             nota="Os textos de ação $.opcoes[0].efeitos[0].texto e $.opcoes[1].efeitos[0].texto ainda citam fantasma/frio e exigem a mesma passagem de autoria (prosa longa não é inventada aqui)."),
    ])

R[9] = dict(
    veredito="MELHORAR", natureza="texto narrativo ausente (evento de combate)",
    justificativa=[
        "$.texto='' (0 chars); $.opcoes[0].titulo='Fight!', $.opcoes[0].texto='' e o texto da ação Success também é vazio.",
        "batalha.iniciar=true sem ForcedEnemies e sem referencia (PPtr m_PathID=0) — o encontro é resolvido no runtime.",
        "$.condicoes.KeepInDeckWhenUsed=1 e peso=5.0; allowedNodeTypes=[0] (NormalFight).",
        "Alegação da parte01 de que dados_recompensa_final NULL significaria 'sistema de recompensas não configurado' é REFUTADA: o motivo do campo é explícito (runtime não exercitado).",
        "Achado novo: #9 e #10 compartilham o MESMO id 5b740c2b-3480-48f2-997b-88c8291db0c0, embora tenham chaves distintas.",
    ],
    props=[
        dict(code="9.1", tipo="CAMPO", path="$.texto", antes="",
             depois="Somewhere beyond the ridge, steel rings against steel — the fight is already waiting.",
             nota="Ancorado em batalha.iniciar=true e no nó NormalFight do asset."),
    ])

R[10] = dict(
    veredito="MELHORAR", natureza="texto narrativo ausente em conteúdo de teste",
    justificativa=[
        "$.condicoes.disabled=1 E $.condicoes.EditorOnly=1 (único da faixa com EditorOnly=1); $.texto='' e textos de ação vazios.",
        "ForcedEnemies configurado: The Dead One (2545072); peso=5.0; KeepInDeckWhenUsed=1.",
        "NÃO propomos alterar $.condicoes.disabled nem excluir o slot: desativar/remover é decisão do autor, não decorrência de estar disabled.",
    ],
    props=[
        dict(code="10.1", tipo="CAMPO", path="$.texto", antes="",
             depois="The air here holds its breath — something has been waiting a long time to test you.",
             nota="PROPOSTA CONDICIONAL: só se aplica caso o autor decida manter o slot ativo; nenhuma mudança de disabled é proposta."),
    ])

R[11] = dict(
    veredito="MANTER", natureza="—",
    justificativa=[
        "Texto de 354 chars, $.texto_resultados_possiveis='Who will attempt to disarm the trap?' e opção única 'Overpower' com $.opcoes[0].rolagem.bonus=[{0,Might}].",
        "Success limite 10 concede experiência (dar=true, alvo Party); Failure limite 1 aplica -20 percentMaxHealth e status Crippled (2545492).",
        "Nenhum campo inconsistente; nenhuma anomalia constatada.",
    ], props=[])

R[12] = dict(
    veredito="MANTER", natureza="—",
    justificativa=[
        "Texto de 345 chars; opção única 'Escape' com descrição própria.",
        "Success limite 12 concede experiência (dar=true, razao 0.5); Failure limite 1 aplica -20 percentMaxHealth e status Frostbitten (2545496).",
        "Nenhuma anomalia constatada.",
    ], props=[])

R[13] = dict(
    veredito="MELHORAR", natureza="typo no texto original (sugestão de correção do ORIGINAL)",
    justificativa=[
        "Literal real do original: 'whisperes' — achado válido preservado da parte01.",
        "Alegação da parte01 de que $.opcoes[*].rolagem.bonus vazio indicaria 'mecânica de sorte não implementada' é REFUTADA: bônus de rolagem vazio é o padrão da faixa (26 de 32 slots) e as ações são Success com limite_rolagem 0; nada indica rolagem quebrada.",
        "Opção 1 concede status Ethereal (2545439) e LeadsToFortune=1.",
    ],
    props=[
        dict(code="13.1", tipo="TRECHO", path="$.texto", antes="whisperes", depois="whispers",
             nota="antes→depois do TEXTO ORIGINAL; nenhum arquivo do jogo/EV-R1 é editado."),
    ])

R[14] = dict(
    veredito="MELHORAR", natureza="texto incompatível com o título (reuso literal do texto de #1/#8)",
    justificativa=[
        "$.texto é o mesmo de #1/#8, mas o título é 'Blood of the Abyss'.",
        "Opção 1 concede status Ethereal (2545439); LeadsToFortune=1; $.condicoes.disabled=1 registrado como estado, sem proposta de reativação.",
    ],
    props=[
        dict(code="14.1", tipo="CAMPO", path="$.texto", antes=GHOST,
             depois="A crimson glow pulses from a fissure in the rock, and the air turns thick with the smell of old blood.",
             nota="Alinha a cena ao título real do asset."),
        dict(code="14.2", tipo="CAMPO", path="$.opcoes[0].texto", antes=REACH,
             depois="Reach toward the pulsing light.",
             nota="Mantém a opção 1 como a que concede o status Ethereal."),
        dict(code="14.3", tipo="CAMPO", path="$.opcoes[1].texto", antes=LEAVE,
             depois="Turn away from the fissure.",
             nota="Textos de ação ainda citam fantasma/frio e exigem a mesma passagem de autoria."),
    ])

R[15] = dict(
    veredito="MANTER", natureza="—",
    justificativa=[
        "Texto de 328 chars; duas opções (Rest/Leave) com descrições próprias.",
        "Rest (Success limite 0) inicia batalha com referencia real 'Cursed Chest Battle' (resources.assets:2544645) e concede experiência (razao 2.0); Leave aplica Fatigued(2545495)/Enfeebled(2545494).",
        "Rare(2), minLevel=3, caminho 'events/bonefire - (roguelike)' — asset distinto de #16 (chave 2545548, 'events/bonefire'), apesar do texto idêntico.",
    ], props=[])

R[16] = dict(
    veredito="MANTER", natureza="—",
    justificativa=[
        "Mesmo conteúdo autoral de #15, porém com chave (2545548), id e caminho ('events/bonefire') próprios.",
        "Rest inicia batalha 'Cursed Chest Battle' (2544645); Leave aplica Fatigued/Enfeebled.",
        "Título e texto repetidos não constituem registro duplicado: não há chave ou id repetido entre #15 e #16.",
    ], props=[])

R[17] = dict(
    veredito="MANTER", natureza="—",
    justificativa=[
        "Texto de 143 chars; três opções com descrições próprias.",
        "Rest (Success limite 0) cura 50 percentMaxHealth e 50 percentMaxMana.",
        "'Reroll Skill' NÃO é opção sem efeito: $.opcoes[1].campos_originais.openSkillRerollMenu=1; 'Level Up Fortunes' usa $.opcoes[2].campos_originais.levelUpFortunesToCharacterLevel=1. Ambos são flags reais, não recompensas vazias.",
        "allowedNodeTypes=[2] (NodeType 2=RestSite).",
    ], props=[])

R[18] = dict(
    veredito="MANTER", natureza="—",
    justificativa=[
        "Texto idêntico ao de #17, mas opções diferentes (Rest/Prepare) e caminho próprio ('events/bonfire'; #17 é 'events/bonfire (roguelike)').",
        "Rest cura 50 percentMaxHealth/50 percentMaxMana; Prepare concede o status 'Prepared' (2545391).",
        "Nenhuma anomalia constatada.",
    ], props=[])

R[19] = dict(
    veredito="MELHORAR", natureza="texto narrativo ausente em evento StoryOnly",
    justificativa=[
        "$.texto='' (0 chars) e $.opcoes[0].texto='' (vazio); a ação Rest tem texto próprio ('You feel well rested.').",
        "$.condicoes.historia=StoryOnly (StorySetting) — o asset é declaradamente narrativo e não tem narrativa.",
        "Rest cura 25 percentMaxHealth/25 percentMaxMana; allowedNodeTypes=[2] (RestSite).",
    ],
    props=[
        dict(code="19.1", tipo="CAMPO", path="$.texto", antes="",
             depois="You settle beside the low-burning fire, and the tale of this place slowly takes shape in the embers.",
             nota="Coerente com o StorySetting=StoryOnly e com o nó de descanso."),
        dict(code="19.2", tipo="CAMPO", path="$.opcoes[0].texto", antes="",
             depois="Sit by the fire and listen.",
             nota="Descrição da única opção, hoje vazia."),
    ])

R[20] = dict(
    veredito="MELHORAR", natureza="texto narrativo ausente (evento de chefe)",
    justificativa=[
        "$.texto='' (0 chars); $.opcoes[0].titulo='Fight!', $.opcoes[0].texto='' e texto da ação Success vazio.",
        "allowedNodeTypes=[5] (NodeType 5=Boss); batalha.iniciar=true sem ForcedEnemies e sem referencia (PPtr m_PathID=0).",
        "Alegação da parte01 de recompensa inexistente/sistema não configurado é REFUTADA: $.opcoes[0].efeitos[0].batalha.dados_recompensa_final=null traz motivo explícito de runtime não exercitado.",
    ],
    props=[
        dict(code="20.1", tipo="CAMPO", path="$.texto", antes="",
             depois="The path ends at a sealed gate, and behind it something vast shifts its weight.",
             nota="Ancorado no nó Boss e no combate já configurado do asset."),
    ])


# ---------------------------------------------------------------------------
def gen():
    normal = load_events()
    recs = []
    for i, e in enumerate(normal, 1):
        r = R[i]
        assert r["veredito"] in ("MANTER", "MELHORAR")
        co = e.get("condicoes") or {}
        rec = dict(
            ordinal=i, chave=e["chave"], id=e["id"], titulo=e["titulo"], categoria=e["categoria"],
            raridade={"valor": e["raridade"]["valor"], "nome": e["raridade"]["nome"]},
            peso=e["peso"], veredito=r["veredito"], natureza=r["natureza"],
            justificativa=r["justificativa"], propostas=r["props"],
            fatos=dict(
                disabled=co.get("disabled"), EditorOnly=co.get("EditorOnly"),
                minLevel=co.get("minLevel"), allowedNodeTypes=co.get("allowedNodeTypes"),
                historia=(e.get("historia") or {}).get("nome"),
                texto_len=len(e.get("texto") or ""), n_opcoes=len(e.get("opcoes") or []),
                caminho_asset=(e.get("origem") or {}).get("caminhos_resource"),
                sha256_objeto=(e.get("origem") or {}).get("sha256_objeto"),
            ),
        )
        recs.append(rec)

    manter = [r["ordinal"] for r in recs if r["veredito"] == "MANTER"]
    melhorar = [r["ordinal"] for r in recs if r["veredito"] == "MELHORAR"]

    val = dict(
        schema="EV-R2-NORMAL-b01-parte02-validacao/1", lote="Normal", faixa=[1, 20],
        fontes_sha256=BASE_SHA, propostas_originais_reprovadas="EV-R2-NORMAL-b01-parte01.md",
        contagens=dict(total=len(recs), manter=len(manter), melhorar=len(melhorar),
                       manter_ordinais=manter, melhorar_ordinais=melhorar,
                       total_propostas=sum(len(r["propostas"]) for r in recs)),
        registros=recs,
    )
    with open(os.path.join(BASE, "EV-R2-NORMAL-b01-parte02-validacao.json"), "w", encoding="utf-8") as f:
        json.dump(val, f, ensure_ascii=False, indent=1)
    print("VALIDACAO_OK registros=%d manter=%d melhorar=%d propostas=%d" %
          (len(recs), len(manter), len(melhorar), val["contagens"]["total_propostas"]))
    return val


if __name__ == "__main__":
    gen()
