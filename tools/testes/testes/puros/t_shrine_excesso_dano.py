#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EXCESSO DE SHRINE (TST-2): o DANO do Flame e do Decay (as duas auras de perigo).

O QUE ESTE TESTE GARANTE
------------------------
1. A formula das duas acoes e a do asset, com o fator do `ShrineEffectBonus` GENERICO no bonus -
   mas o bonus que entra e o do EIXO da aura. RV-30 (03/10): as duas de PERIGO leem
   `Source["ShrineEffectBonus"]` e num ground effect o `Source` e o personagem VAZIO do shrine,
   logo o fator e `1 + BONUS_DA_FONTE/100 = 1` (o bonus do JOGADOR NAO as multiplica):
   `Flame`: `Mathf.Max(1,  Mathf.Round(MaxHealth * %do tipo))`;
   `Decay`: a MESMA conta SEM o `Mathf.Max(1,` - o Decay pode dar 0, o Flame nao
   (RV-19 §4.2/§4.3 + RV-30; `ShrineAuraPatch.cs` `FormulaDanoFlameSemBonus` / `FormulaDanoDecaySemBonus`).
2. Com **vida maxima 100** o numero ISOLA a porcentagem do tipo
   (RV-19 §10 CORRIGIDO pelo RV-30: Decay 10% -> 10 e Flame 5% -> 5, IGUAIS nos 3 bonus do jogador -
   o `[0]`% NAO dobra com Worship: o fabrico do numero dobrado era o defeito).
3. **Decay com vida maxima 3 da 0** (3 x 10% = 0.3 -> Round -> 0, SEM minimo) e o
   **Flame com a mesma vida da 1** (`Mathf.Max(1, ...)`) - o par isola o minimo.
4. As BORDAS de arredondamento do motor: `Mathf.Round` e half-to-EVEN, entao
   `0.5 -> 0` e `2.5 -> 2` (o "meio para cima" daria 1 e 3).
5. **Flame com varios alvos**: um valor por alvo, com a vida maxima e a % do tipo DELE
   (o hover nao sabe quem vai atacar - a lista e uma projecao). O FATOR e o do eixo `Source`
   (o shrine, RV-30), igual para todos os alvos.
   **Flame sem alvo**: sem numero, e a aura sai no LOG (nunca calada).

DE ONDE VEM O ESPERADO
----------------------
`excesso-shrine.esperado.json` (oraculo em C#) e `tools/dados/shrines-percentuais.csv`
(a tabela GERADA das acoes `Flame Aura Proc`/`Decay Aura Proc`, com o offset do
asset em cada linha). A tabela do §10 do RV-19 entra como SEGUNDA fonte, conferida
contra o oraculo - as duas tem de bater.
"""
import arcabouco as arc
import regras_shrine as reg

META = {
    "nome": "shrine-excesso-dano",
    "categoria": "pura",
    "requer": [],
    "descricao": "dano do Flame/Decay: minimo 1 so no Flame, vida maxima 3/100, half-to-even e um alvo por item",
}

# ACEITE do dono (RV-19 §10, a tabela de conferencia em jogo: "com 100 de vida o
# dano e o mesmo numero"): o `[0]`% vira dano com vida maxima 100. CORRIGIDO pelo RV-30: o fator
# das duas auras de PERIGO e o do SOURCE (o shrine), entao o numero NAO muda com o bonus do jogador.
# O teste confere que o ORACULO concorda com a tabela - duas fontes, um numero.
ACEITE_RV19_10 = {
    # (aura, tipo) -> dano com vida maxima 100 e o fator do eixo `Source` (BONUS_DA_FONTE = 0)
    ("Decay Shrine Aura", "player"): 10,
    ("Flame Shrine Aura", "player"): 5,
}


def corpo():
    ent = reg.entrada_do_caso()
    esp = reg.esperado_do_caso()
    pct, minimo1 = reg.percentuais()
    ctx = reg.contexto(ent)

    linhas = {}
    for d in esp["danos"]:
        linhas[(d["aura"], d["tipo"], float(d["maxhealth"]), d["bonus"])] = d

    def esperado(aura, tipo, mh, bonus):
        chave = (aura, tipo, float(mh), bonus)
        arc.exigir(chave in linhas, "a matriz da fixture nao tem %r" % (chave,))
        return linhas[chave]

    # ------------------------------------------------------------------ a matriz inteira
    for (aura, tipo, mh, bonus), d in linhas.items():
        # RV-30: o fator que multiplica e o `bonus_fonte` (o do eixo `Source` = o shrine), NAO o
        # `bonus` do jogador da cena. O `bonus`/`bonus_id` continuam na fixture so como rotulo da cena.
        obtido = reg.dano(mh, pct[(aura, tipo)], d["bonus_fonte"], minimo1[aura])
        arc.igual(obtido, d["dano"],
                  "dano do %s contra %s (vida %s, bonus do jogador %s, bonus da fonte %s)"
                  % (aura, tipo, mh, bonus, d["bonus_fonte"]))
        arc.igual(d["minimo1"], minimo1[aura],
                  "o `minimo1` do %s tem de vir da tabela gerada" % aura)

    # ------------------------------------------------------------------ o minimo e a % do tipo
    arc.exigir(minimo1["Flame Shrine Aura"], "o Min(1) do Flame tem de estar na tabela gerada")
    arc.exigir(not minimo1["Decay Shrine Aura"], "o Decay NAO pode ter minimo (RV-19 §4.3)")

    # vida maxima 100 isola a porcentagem: com bonus 0 o dano E a % do tipo
    for tipo in ("boss", "champion", "elite", "soldier", "fodder", "player"):
        obtido = reg.dano(100, pct[("Decay Shrine Aura", tipo)], 0, False)
        arc.igual(obtido, round(pct[("Decay Shrine Aura", tipo)] * 100),
                  "Decay com vida 100 e bonus 0: o numero e a propria %% do tipo '%s'" % tipo)
    # Decay vida 3 (a borda que o dono pediu): 0, sem minimo nenhum.
    arc.igual(reg.dano(3, pct[("Decay Shrine Aura", "player")], 0, minimo1["Decay Shrine Aura"]), 0,
              "DECAY COM VIDA MAXIMA 3: tem de dar 0 (3 x 10% = 0.3 -> Round, sem minimo)")
    arc.igual(reg.agregar(reg.por_id(ent["agregado"])["decay-vida-3"], ctx)["itens"],
              ["Shadow damage per turn 0"], "o item do Decay com vida 3 sai com 0, nao some")
    # Flame vida 3: o Max(1, ...) segura em 1.
    arc.igual(reg.dano(3, pct[("Flame Shrine Aura", "player")], 0, minimo1["Flame Shrine Aura"]), 1,
              "FLAME COM VIDA MAXIMA 3: o Mathf.Max(1, ...) nao deixa cair para 0")

    # ------------------------------------------------------------------ half-to-even (as .5)
    arc.igual(reg.dano(10, pct[("Decay Shrine Aura", "boss")], 0, False), 0,
              "BORDA .5: Decay com vida 10 contra boss = 0.5 -> Mathf.Round -> 0 (meio para o PAR)")
    arc.exigir(reg.dano(10, pct[("Decay Shrine Aura", "boss")], 0, False) != 1,
               "0.5 virou 1: o arredondamento nao e o Mathf.Round do motor")
    arc.igual(reg.dano(100, pct[("Flame Shrine Aura", "boss")], 0, minimo1["Flame Shrine Aura"]), 2,
              "BORDA .5: Flame com vida 100 contra boss = 2.5 -> 2 (e nao 3)")

    # ------------------------------------------------------------------ o aceite do RV-19 §10 (RV-30)
    eixos = reg.eixos_das_auras()
    for (aura, tipo), valor in ACEITE_RV19_10.items():
        # o fator e o do eixo `Source`: nos 3 casos do jogador o numero com 100 de vida e o MESMO.
        for bonus_jogador in (0, 20, 100):
            obtido = reg.dano(100, pct[(aura, tipo)],
                              reg.bonus_do_eixo(eixos[aura], bonus_jogador), minimo1[aura])
            arc.igual(obtido, valor,
                      "RV-19 §10 corrigido pelo RV-30: %s com 100 de vida no bonus do jogador %s"
                      % (aura, bonus_jogador))
        # a fixture do oraculo tem de dar o MESMO numero nos dois extremos do bonus do jogador.
        arc.igual(esperado(aura, tipo, 100, 0)["dano"], valor,
                  "a fixture tem de concordar com a tabela (RV-19 §10) no bonus do jogador 0 (%s)" % aura)
        arc.igual(esperado(aura, tipo, 100, 100)["dano"], valor,
                  "o dano do %s NAO pode mudar com o bonus do jogador (RV-30) - fixture no bonus 100" % aura)

    # ------------------------------------------------------------------ o EIXO do dano (RV-30)
    # O fator que multiplica as duas auras de PERIGO e o do SOURCE (shrine), NAO o do jogador. O
    # `dano()` continua GENERICO no bonus - o que o MODELO faz e passar o bonus do eixo `Source`.
    # O defeito do numero DOBRADO era passar o bonus do JOGADOR aqui.
    for aura, tipo in (("Decay Shrine Aura", "player"), ("Flame Shrine Aura", "elite")):
        base = reg.dano(100, pct[(aura, tipo)], reg.BONUS_DA_FONTE, minimo1[aura])
        com_bonus_do_jogador = reg.dano(100, pct[(aura, tipo)],
                                        reg.bonus_do_eixo(eixos[aura], 100), minimo1[aura])
        arc.igual(com_bonus_do_jogador, base,
                  "RV-30: o bonus do jogador NAO multiplica %s contra %s (o eixo e `Source`)" % (aura, tipo))
    # ... e o MODELO da linha tambem nao deixa o bonus do jogador entrar: o item do Decay no bonus
    # 100 (worship) tem de ser IGUAL ao do bonus 0.
    cena_100 = reg.por_id(ent["agregado"])["decay-so"]
    cena_0 = {"id": "rv30-decay-bonus-0", "bonus_id": "sem-bonus", "maxhealth": 100.0,
              "tipo_receptor": "player",
              "vivas": [{"aura": "Decay Shrine Aura", "instancias": 1, "stacks": 1, "expressao": True}],
              "alvos": [], "totais": {}}
    arc.igual(reg.agregar(cena_100, ctx)["itens"], reg.agregar(cena_0, ctx)["itens"],
              "RV-30: o item do Decay no bonus do jogador 100 (worship) e o MESMO do bonus 0")

    # ------------------------------------------------------------------ varios alvos / sem alvo
    cena = reg.por_id(ent["agregado"])["flame-varios-alvos"]
    saida = reg.agregar(cena, ctx)
    arc.igual(len(saida["itens"]), 1, "o Flame e UM item na linha, com todos os alvos dentro")
    alvos_txt = saida["itens"][0].split(": ", 1)[1]
    valores = [t.rsplit(" ", 1) for t in alvos_txt.split(", ")]
    arc.igual(len(valores), len(cena["alvos"]),
              "um valor por ALVO na area (o hover nao sabe quem vai atacar)")
    for (nome, valor), alvo in zip(valores, cena["alvos"]):
        arc.igual(nome, alvo["nome"], "a ordem dos alvos do item e a ordem da cena")
        # RV-30: o fator e o do eixo `Source` (o shrine), igual para TODOS os alvos.
        esperado_alvo = reg.dano(alvo["maxhealth"], pct[("Flame Shrine Aura", alvo["tipo"])],
                                 reg.BONUS_DA_FONTE, minimo1["Flame Shrine Aura"])
        arc.igual(int(valor), esperado_alvo,
                  "o valor do alvo '%s' sai da vida/%%/bonus DELE" % alvo["nome"])
    sem_alvo = reg.agregar(reg.por_id(ent["agregado"])["flame-sem-alvo"], ctx)
    arc.igual(sem_alvo["itens"], [], "sem alvo na area nao existe UM numero para o Flame (RV-19 §4.4)")
    arc.exigir(sem_alvo["avisos"], "a aura do Flame sem alvo tem de sair no LOG com o motivo")
    arc.igual(sem_alvo["linha"], "", "sem nenhum numero provado, a linha nao sai (nada estimado)")

    print("dano: %d valores da matriz + as bordas (vida 3, vida 100, .5) e os alvos do Flame"
          % len(linhas))


if __name__ == "__main__":
    arc.main(META, corpo)
