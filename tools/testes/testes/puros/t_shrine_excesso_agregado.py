#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EXCESSO DE SHRINE (TST-2): a LINHA AGREGADA `Your active shrine auras:` item por item.

O QUE ESTE TESTE GARANTE
------------------------
1. **A contribuicao cabe na conta do MOTOR** - o defeito do print do dono: com a
   MESMA aura 3x na lista viva a linha saiu `Dodge +120%` com a aura valendo 40.
   Cada aura viva entra UMA vez (RV-46/`AurasUnicas`, `ShrineAuraPatch.cs`
   1296 · `AurasUnicas()`): `Dodge +40% (total +57%)`. A repeticao vai para o LOG (`Rogue Aura x3`),
   nunca para o numero.
2. **Duas auras no mesmo atributo SOMAM e o item nao se repete** (Warrior + Fury em
   `DamageMod` = 40 + 50 = 90, num item so) - 1915 · `ContribuicaoDasAuras()`.
3. **STACKS do mesmo status sao outra coisa**: `TotalStacks = 2` multiplica o valor
   (o motor soma `val + parsed2 * stacks`, decompilado l.37263; `ShrineAuraPatch.cs`
   1966 · `ContribuicaoDasAuras()`) - `Damage +80%`, ao contrario da aura repetida (que continua contando 1x).
4. **Nenhuma aura viva some calada**: o Dwarven (aura viva SEM atributo de
   personagem) tem item proprio (`Stun chance +40%`) ou sai no LOG com o motivo
   (`RV-46 AVISO: a aura viva 'Dwarven Aura' NAO virou item`). A linha se
   apresenta como COMPLETA.
5. Um item por ATRIBUTO, na ordem canonica (1032 · `OrdemDosAtributos`), e a linha inteira fecha na
   ordem dos itens (o comparador de log corta por `; `).
6. **DWA-2** - a dedupe do RV-46 e POR TIPO DE EFEITO: aura de ATRIBUTO repetida conta
   UMA vez (o motor soma as instancias e o teto corta), mas aura de GATILHO
   (`SkillTriggers`; Dwarven/Decay/Flame) conta UMA vez POR INSTANCIA, porque o motor
   avalia o gatilho uma vez por status vivo (`Character.SkillTriggers` l.33489-33508 +
   `ProcessSkillTriggers` l.40953-40959, rolando a chance em l.41211-41216). Com DOIS
   Dwarven Shrines no alcance a linha sai `Stun chance +40%; Stun chance +40%` - duas
   rolagens de verdade, nunca um `+80%` somado a mao.

DE ONDE VEM O ESPERADO
----------------------
`excesso-shrine.esperado.json` (oraculo em C#, `oraculo_excesso_shrine`) e os
numeros de base/percentual da tabela GERADA (`tools/dados/*.csv`). As regras
citadas por `arquivo:linha` sao o `BetterTooltips/Patches/ShrineAuraPatch.cs`
vivo - e o teste LE esse arquivo para provar que a trava que ele vigia continua
ligada no codigo (deduplicacao antes da soma).
"""
import os
import re

import arcabouco as arc
import regras_shrine as reg

META = {
    "nome": "shrine-excesso-agregado",
    "categoria": "pura",
    "requer": [],
    "descricao": "linha agregada: aura repetida conta 1x (Dodge +120% -> +40%), auras somam, Dwarven nunca some",
}

# A regra que o defeito de hoje atropelou: a lista viva e DESDUPLICADA antes de
# somar. Sem estas duas ligacoes no codigo do mod, o teste reprova - nao porque
# "mudou de forma", mas porque a trava do defeito do `Dodge +120%` saiu de la.
LIGACOES = (
    (r"AurasUnicas\(ativas, out repeticoes\)",
     "a deduplicacao da lista viva (AurasUnicas) saiu de AcumuladoShrines"),
    (r"ContribuicaoDasAuras\(unicas,",
     "a soma passou a usar outra lista que nao a DESDUPLICADA (ContribuicaoDasAuras(unicas,)"),
    # DWA-2: o outro lado da moeda - os itens das auras SEM atributo tem de sair da lista TIPADA
    # (aura de gatilho conta por INSTANCIA; aura de atributo continua 1x). Sem esta ligacao, a
    # desdupe do RV-46 volta a valer para TUDO e a segunda rolagem do Dwarven some em silencio.
    (r"ItensSemAtributo\(porInstancia,",
     "os itens sem atributo deixaram de sair da lista TIPADA por efeito (ItensSemAtributo(porInstancia,)"),
)


def corpo():
    ent = reg.entrada_do_caso()
    esp = reg.esperado_do_caso()
    ctx = reg.contexto(ent)
    cenas = reg.por_id(ent["agregado"])
    esperadas = reg.por_id(esp["agregado"])

    arc.igual(sorted(cenas), sorted(esperadas),
              "as cenas do agregado na entrada e no esperado")

    saidas = {}
    for cid, cena in cenas.items():
        saida = reg.agregar(cena, ctx)
        saidas[cid] = saida
        alvo = esperadas[cid]
        arc.igual(saida["itens"], alvo["itens"], "itens da cena '%s'" % cid)
        arc.igual(saida["linha"], alvo["linha"], "linha da cena '%s'" % cid)
        arc.igual(saida["repeticoes"], alvo["repeticoes"], "repeticoes registradas na cena '%s'" % cid)
        arc.igual(saida["avisos"], alvo["avisos"], "avisos (log) da cena '%s'" % cid)

        # INVARIANTE 2 do plano: a lista se diz completa. Uma cena com aura viva
        # nunca pode sair SEM item e SEM aviso (nada de silencio).
        distintas = []
        for viva in cena["vivas"]:
            if viva["aura"] not in distintas:
                distintas.append(viva["aura"])
        arc.exigir(saida["itens"] or saida["avisos"],
                   "cena '%s': %d aura(s) viva(s) e nenhum item nem aviso - a lista ficou em silencio"
                   % (cid, len(distintas)))
        if not saida["itens"]:
            for aura in distintas:
                arc.exigir(any(aura in aviso for aviso in saida["avisos"]),
                           "cena '%s': a aura viva '%s' nao virou item e o log nao a nomeia" % (cid, aura))

    # ------------------------------------------------------------------ o defeito do print
    rogue = saidas["rogue-x3-stacks-1"]
    arc.igual(rogue["itens"], ["Dodge +40% (total +57%)"],
              "o DEFEITO DO PRINT (Dodge +120% com a aura valendo 40): a aura repetida 3x na lista viva")
    arc.exigir("120" not in rogue["linha"],
               "a linha esta multiplicando a contribuicao pelo numero de instancias: %r" % rogue["linha"])
    arc.igual(rogue["repeticoes"], ["Rogue Aura x3"],
              "a repeticao tem de ir para o LOG (a lista viva tinha a mesma aura 3x)")
    # A contribuicao do item E a do motor: a soma das auras DISTINTAS vivas.
    distinta, entrou = reg.contribuicao_do_motor(
        ["Rogue Aura"], "DodgeChance", ctx["bonus"]["worship"], {"Rogue Aura": 1}, ctx)
    arc.igual(entrou, ["Rogue Aura"], "quantas auras distintas entram na soma do Dodge")
    arc.igual(reg.item("DodgeChance", distinta, 57), rogue["itens"][0],
              "a contribuicao do item tem de ser a conta do motor (1 aura viva valendo 40)")
    # O SINAL que denunciou o defeito: multiplicada por instancia, a contribuicao passa do
    # TOTAL do personagem (o resto ficaria negativo) - e `120` nao e o valor de aura nenhuma.
    arc.exigir(distinta * 3 > 57,
               "a conta do defeito (3 x %d) tem de ESTOURAR o total do personagem - o sinal do achado" % distinta)
    arc.exigir(distinta <= 57,
               "a contribuicao CORRETA (%d) tem de caber no total do personagem (57)" % distinta)

    # ------------------------------------------------------------------ duas auras, um item
    dois = saidas["warrior-mais-fury"]
    war = reg.escala(ctx["auras"]["Warrior Aura"]["DamageMod"], ctx["bonus"]["worship"])
    fury = reg.escala(ctx["auras"]["Fury"]["DamageMod"], ctx["bonus"]["worship"])
    arc.igual(reg.item("DamageMod", war + fury, 115), dois["itens"][0],
              "Warrior + Fury em DamageMod: as contribuicoes SOMAM (%d + %d) e o item e UM" % (war, fury))
    itens_damage_mod = [i for i in dois["itens"]
                        if i.startswith("Damage ") and not i.startswith("Damage taken ")]
    arc.igual(len(itens_damage_mod), 1,
              "duas auras no mesmo atributo nao podem virar dois itens")
    arc.igual(dois["repeticoes"], [], "duas auras DIFERENTES nao sao repeticao")

    # ------------------------------------------------------------------ tres fontes vivas
    tres = saidas["tres-fontes-mesmo-atributo"]
    arc.igual(tres["itens"], dois["itens"],
              "tres entradas vivas (Warrior x2 + Fury) no mesmo atributo: um item so, com a MESMA conta")
    arc.igual(tres["repeticoes"], ["Warrior Aura x2"], "a entrada repetida vai para o log")

    # ------------------------------------------------------------------ stacks x instancias
    stacks = saidas["warrior-stacks-2"]
    arc.igual(stacks["itens"][0],
              reg.item("DamageMod", war * 2, 155),
              "STACKS do mesmo status (TotalStacks 2) MULTIPLICAM o valor - e o motor que soma assim")
    arc.exigir(stacks["itens"][0] != rogue["itens"][0],
               "stacks e instancias repetidas nao podem dar o mesmo tratamento")

    # ------------------------------------------------------------------ o Dwarven sumido
    dwarven = saidas["dwarven-so"]
    arc.igual(dwarven["itens"], ["Stun chance +40%"],
              "o DWARVEN SUMIDO: aura viva sem atributo de personagem tem item proprio (RV-46)")
    arc.exigir(dwarven["itens"], "a unica aura viva da cena nao pode sumir da lista")
    sem_expr = saidas["dwarven-sem-expressao"]
    arc.igual(sem_expr["itens"], [], "sem expressao avaliada nao existe numero (nada estimado)")
    arc.exigir(any("Dwarven Aura" in a for a in sem_expr["avisos"]),
               "sem numero, a aura tem de sair no LOG com o motivo - nunca calada")
    arc.exigir(sem_expr["avisos"], "a cena sem item tem de trazer o motivo no log")

    # ------------------------------------------------------------------ DWA-2: DOIS Dwarven no alcance
    # O defeito do dono (30/09): "a Dwarven Aura nao esta stackando com mais de um shrine no alcance".
    # O efeito dela NAO e atributo de personagem, e CHANCE DE GATILHO - e o motor avalia o gatilho UMA
    # VEZ POR STATUS VIVO (`Character.SkillTriggers` decompilado l.33489-33508 + `ProcessSkillTriggers`
    # l.40953-40959, rolando em l.41211-41216). Entao com DOIS shrines a linha tem DOIS itens, cada um
    # com o numero do asset: a segunda rolagem conta, e NADA e somado a mao (o motor nao soma chance).
    dois_dwarven = saidas["dwarven-x2"]
    arc.igual(dois_dwarven["itens"], ["Stun chance +40%", "Stun chance +40%"],
              "DWA-2: dois Dwarven Shrines no alcance = duas rolagens de 40% (um item por INSTANCIA)")
    arc.exigir("80" not in dois_dwarven["linha"],
               "a chance de gatilho foi SOMADA a mao (%r) - o motor rola duas vezes a mesma chance, "
               "nao soma: o `+80%%` seria a mentira do outro lado do `Dodge +120%%`"
               % dois_dwarven["linha"])
    arc.igual(dois_dwarven["repeticoes"], ["Dwarven Aura x2"],
              "a repeticao continua registrada no LOG (instancias=[Dwarven Aura x2])")
    arc.exigir(dois_dwarven["itens"] != dwarven["itens"],
               "o caso de DOIS shrines nao pode dar o mesmo que o de UM: era exatamente o defeito")

    # A regra e por TIPO de efeito, nao por nome de aura: o Decay (OnTurnStart, tambem sem atributo de
    # personagem) conta por instancia pelo mesmo caminho.
    dois_decay = saidas["decay-x2"]
    arc.igual(dois_decay["itens"], ["Shadow damage per turn 20", "Shadow damage per turn 20"],
              "DWA-2 e por TIPO: o gatilho do Decay tambem roda uma vez por instancia")
    arc.igual(dois_decay["repeticoes"], ["Decay Shrine Aura x2"],
              "o log registra a repeticao do Decay tambem")

    # E o outro lado NAO regrediu: aura de ATRIBUTO repetida continua contando UMA vez (RV-46) - o
    # `Dodge +40%` do print do dono. Se este par mudasse junto, o conserto teria sido amplo demais.
    arc.igual(rogue["itens"], ["Dodge +40% (total +57%)"],
              "a aura de ATRIBUTO repetida 3x continua contando 1x (RV-46 intacto depois do DWA-2)")

    # ------------------------------------------------------------------ o resto do print do dono
    # Os TOTAIS das cenas do Fury vem do print do dono (RV-19 §9.1, bonus 0 e 100): o
    # `resto` (total - contribuicao das auras) tem de ser o MESMO nos dois hovers e nos
    # casos com o Warrior junto - e o que prova a aditividade (§9.2) e o que da
    # procedencia ao total 115 (= 75 do print + 40 do Warrior).
    for cid in ("fury-so", "warrior-mais-fury", "tres-fontes-mesmo-atributo"):
        cena = cenas[cid]
        unicas, stacks, _ = reg.vivas_desduplicadas(cena)
        for atributo, resto_do_print in reg.RESTO_DO_PRINT.items():
            contrib, _entrou = reg.contribuicao_do_motor(unicas, atributo, ctx["bonus"][cena["bonus_id"]],
                                                         stacks, ctx)
            arc.igual(cena["totais"][atributo] - contrib, resto_do_print,
                      "cena '%s': o resto (total - contribuicao) de %s tem de ser o do print do dono"
                      % (cid, atributo))

    # ------------------------------------------------------------------ o total no teto
    # O outro lado do `Dodge +120%`: aqui a contribuicao NAO cabe no total e isso e LEGITIMO -
    # o motor CORTA o total no teto do atributo (RV-46/commit bc394e7: DamageReduction
    # MaxValue=50). Guardian (+40 de dano tomado) + Fury (-50) = -10 liquidos; o total fica no
    # teto. O item tem de trazer a conta das DUAS auras e o total do motor.
    teto = saidas["teto-guardian-mais-fury"]
    guard = reg.escala(ctx["auras"]["Guardian Aura"]["DamageReduction"], ctx["bonus"]["worship"])
    fury_red = reg.escala(ctx["auras"]["Fury"]["DamageReduction"], ctx["bonus"]["worship"])
    arc.igual(reg.item("DamageReduction", guard + fury_red, -50), teto["itens"][1],
              "Guardian (%d) + Fury (%d) em DamageReduction, com o total no TETO do atributo"
              % (guard, fury_red))
    arc.exigir(abs(guard + fury_red) < abs(-50.0),
               "o total declarado (-50) nao esta mais no teto: a cena perdeu o sentido")

    # ------------------------------------------------------------------ a linha completa
    mista = saidas["linha-mista"]
    arc.igual(len(mista["itens"]), 5, "a linha mista tem 5 itens (2 de atributo + 3 sem atributo)")
    arc.igual([i.split(" ")[0] for i in mista["itens"][:2]], ["Damage", "Dodge"],
              "a ordem dos itens de atributo e a canonica (1032 · `OrdemDosAtributos`)")
    arc.exigir(mista["linha"].startswith("Your active shrine auras: "),
               "a linha comeca pelo marcador estavel do mod (1025 · `MarcadorLinhaDeAuras`)")
    arc.exigir(mista["linha"].endswith("."), "os itens terminam em '%': o fecho e sempre o ponto (l.1145)")
    arc.igual(mista["repeticoes"], ["Rogue Aura x2"], "a Rogue repetida conta 1x tambem na linha mista")

    # ------------------------------------------------------------------ a medicao em jogo
    # `tools/fixtures/shrines-rv46-dedupe.log` foi produzido pelo JOGO com o mod instalado: e a
    # MEDICAO, e a medicao em jogo VENCE a leitura de asset (RV-19 §0.5). O modelo tem de
    # reproduzir os itens que o jogo logou - inclusive nos dois casos que viraram defeito.
    log_caminho = os.path.join(arc.raiz_do_repo(), "tools", "fixtures", "shrines-rv46-dedupe.log")
    arc.exigir(os.path.isfile(log_caminho),
               "o log da medicao em jogo sumiu: %s (a fonte que vence a leitura de asset)" % log_caminho)
    with open(log_caminho, encoding="utf-8", errors="replace") as fh:
        log = fh.read()

    def itens_logados(aura, bonus):
        """Os itens das linhas `RV-31 acumulado` de um hover com aquela aura viva e aquele bonus."""
        padrao = re.compile(r"acumulado: auras=\[%s\](?: instancias=\[[^\]]*\])? char=\S+ bonus=%d -> (.+)$"
                            % (re.escape(aura), bonus), re.M)
        return [m.group(1).strip() for m in padrao.finditer(log)]

    def cena_simples(aura, bonus_total):
        """Uma cena de uma aura viva, com o `bonus_id` daquele total (0/20/100 no dataset)."""
        bonus_id = [bid for bid, total in ctx["bonus"].items() if total == bonus_total]
        arc.exigir(bonus_id, "o dataset nao tem um caso de bonus com total %s" % bonus_total)
        return {"id": "log-%s-%s" % (aura, bonus_total), "bonus_id": bonus_id[0], "maxhealth": 100.0,
                "tipo_receptor": "player", "vivas": [{"aura": aura, "instancias": 1, "stacks": 1}],
                "alvos": [], "totais": {}}

    # (a) o DWARVEN sozinho, que era o "aura viva fora da lista": 20 / 24 / 40 no jogo.
    for bonus_total in (0, 20, 100):
        item_modelo = reg.agregar(cena_simples("Dwarven Aura", bonus_total), ctx)["itens"]
        itens_do_jogo = itens_logados("Dwarven Aura", bonus_total)
        arc.exigir(itens_do_jogo, "o log nao tem hover do Dwarven com bonus %s" % bonus_total)
        arc.exigir(item_modelo and item_modelo[0] in itens_do_jogo,
                   "o item do Dwarven do modelo (%s) nao esta entre os do jogo (%s)"
                   % (item_modelo, itens_do_jogo))

    # (b) o ROGUE sozinho com bonus 100: o jogo logou `Dodge +40% (total +57%)` - o MESMO item
    # da cena `rogue-x3-stacks-1` deste teste (que tem 3 entradas vivas da mesma aura).
    arc.exigir(rogue["itens"][0] in itens_logados("Rogue Aura", 100),
               "o item do print do dono (%s) nao aparece na medicao em jogo" % rogue["itens"][0])

    # (c) A MEDICAO DO DEFEITO: o hover com a lista viva repetida (Guardian x2, Rogue x3)
    # loga `instancias=[...]` e as contribuicoes de UMA aura. Se o jogo tivesse logado o numero
    # multiplicado, aqui estaria 80/120.
    arc.exigir("instancias=[Guardian Aura x2, Rogue Aura x3]" in log,
               "a medicao em jogo do defeito (instancias repetidas) nao esta no log")
    linha_repetida = [l for l in log.splitlines() if "instancias=[Guardian Aura x2, Rogue Aura x3]" in l]
    arc.igual(len(linha_repetida), 1, "linhas do acumulado com as instancias repetidas no log")
    efeito = linha_repetida[0].split(" -> ", 1)[1]
    guard_uma = reg.escala(ctx["auras"]["Guardian Aura"]["DamageReduction"], ctx["bonus"]["worship"])
    rogue_uma = reg.escala(ctx["auras"]["Rogue Aura"]["DodgeChance"], ctx["bonus"]["worship"])
    arc.exigir(reg.formatar("DodgeChance", rogue_uma) in efeito,
               "o jogo nao logou o Dodge de UMA Rogue (%s) no hover com 3 entradas: %s"
               % (reg.formatar("DodgeChance", rogue_uma), efeito))
    arc.exigir(reg.formatar("DamageReduction", guard_uma) in efeito,
               "o jogo nao logou o `Damage taken` de UMA Guardian no hover com 2 entradas: %s" % efeito)
    arc.exigir("120" not in efeito and "80" not in efeito,
               "a medicao em jogo tem o numero multiplicado por instancia: %s" % efeito)

    # ------------------------------------------------------------------ o mod vivo
    caminho = os.path.join(arc.raiz_do_repo(), "BetterTooltips", "Patches", "ShrineAuraPatch.cs")
    arc.exigir(os.path.isfile(caminho),
               "a fonte viva das regras sumiu: %s (o teste vigia ela, nao uma copia)" % caminho)
    with open(caminho, encoding="utf-8") as fh:
        fonte = fh.read()
    for padrao, mensagem in LIGACOES:
        arc.exigir(re.search(padrao, fonte) is not None,
                   "%s (procurei /%s/ em BetterTooltips/Patches/ShrineAuraPatch.cs)" % (mensagem, padrao))

    print("agregado: %d cenas conferidas (aura repetida, duas auras no mesmo atributo, stacks,"
          " Dwarven e a linha mista)" % len(cenas))


if __name__ == "__main__":
    arc.main(META, corpo)
