#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EXCESSO DE SHRINE (TST-2): o DANO do Flame e do Decay (as duas auras de perigo).

O QUE ESTE TESTE GARANTE
------------------------
1. A formula das duas acoes e a do asset, com o fator do `ShrineEffectBonus`:
   `Flame`: `Mathf.Max(1,  Mathf.Round((MaxHealth * %do tipo) * (1 + bonus/100)))`;
   `Decay`: a MESMA conta SEM o `Maxf.Max(1,` - o Decay pode dar 0, o Flame nao
   (RV-19 §4.2/§4.3; `ShrineAuraPatch.cs` 737 · `FormulaDanoFlameCru` / 769 · `FormulaDanoDecay`).
2. Com **vida maxima 100** o numero ISOLA a porcentagem do tipo
   (RV-19 §10: Decay 10% -> 10 no bonus 0 e 20 no bonus 100; Flame 5% -> 5 e 10).
3. **Decay com vida maxima 3 da 0** (3 x 10% = 0.3 -> Round -> 0, SEM minimo) e o
   **Flame com a mesma vida da 1** (`Mathf.Max(1, ...)`) - o par isola o minimo.
4. As BORDAS de arredondamento do motor: `Mathf.Round` e half-to-EVEN, entao
   `0.5 -> 0` e `2.5 -> 2` (o "meio para cima" daria 1 e 3).
5. **Flame com varios alvos**: um valor por alvo, com a vida maxima, a % do tipo e
   o bonus DELE (o hover nao sabe quem vai atacar - a lista e uma projecao).
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
# dano e o mesmo numero"): o `[0]`% vira dano com vida maxima 100. O teste confere
# que o ORACULO concorda com a tabela do relatorio - duas fontes, um numero.
ACEITE_RV19_10 = {
    # (aura, bonus) -> dano com vida maxima 100 e a % de `player`
    ("Decay Shrine Aura", 0): 10,
    ("Decay Shrine Aura", 100): 20,
    ("Flame Shrine Aura", 0): 5,
    ("Flame Shrine Aura", 100): 10,
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
        obtido = reg.dano(mh, pct[(aura, tipo)], bonus, minimo1[aura])
        arc.igual(obtido, d["dano"],
                  "dano do %s contra %s (vida %s, bonus %s)" % (aura, tipo, mh, bonus))
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

    # ------------------------------------------------------------------ o aceite do RV-19 §10
    for (aura, bonus), valor in ACEITE_RV19_10.items():
        obtido = reg.dano(100, pct[(aura, "player")], bonus, minimo1[aura])
        arc.igual(obtido, valor,
                  "RV-19 §10 (a tabela de conferencia em jogo): %s com 100 de vida e bonus %s"
                  % (aura, bonus))
        arc.igual(esperado(aura, "player", 100, bonus)["dano"], valor,
                  "a fixture do oraculo tem de concordar com a tabela do RV-19 §10 (%s, bonus %s)"
                  % (aura, bonus))

    # ------------------------------------------------------------------ o fator do bonus
    for aura, tipo in (("Decay Shrine Aura", "player"), ("Flame Shrine Aura", "elite")):
        base = reg.dano(100, pct[(aura, tipo)], 0, minimo1[aura])
        dobrado = reg.dano(100, pct[(aura, tipo)], 100, minimo1[aura])
        arc.igual(dobrado, base * 2,
                  "com Worship (+100) o fator e 2: %s contra %s dobra (a medicao do dono, RV-19 §0.5)" % (aura, tipo))

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
        esperado_alvo = reg.dano(alvo["maxhealth"], pct[("Flame Shrine Aura", alvo["tipo"])],
                                 ctx["bonus"][alvo["bonus_id"]], minimo1["Flame Shrine Aura"])
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
