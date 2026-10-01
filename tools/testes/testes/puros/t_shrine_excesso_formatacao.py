#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EXCESSO DE SHRINE (TST-2): o FORMATO dos numeros da linha (as BORDAS do plano).

O QUE ESTE TESTE GARANTE
------------------------
A grandeza do numero e a da FICHA do jogo: `Mathf.Ceil` + inteiro
(`ShrineAuraPatch.cs` l.950 `InteiroDoJogo`, transcrevendo o decompilado
l.125348-125356 + l.93303-93310). Disso saem as bordas que o dono pediu:

1. **valor fracionario do equipamento** (`53.4`, o print do dono): sai `+54`, nunca
   `+53.4` - a convencao do Ceil do jogo.
2. **inteiro nao ganha `.0`**: `40` sai `+40`.
3. **`.5` exato**: `Ceil(0.5) = 1`.
4. **`-0.4`**: o ceil e 0 e o SINAL E LIDO DEPOIS do arredondamento -> `+0%`,
   nunca `-0` (l.924).
5. **negativo fracionario**: `Ceil(-53.4) = -53` (inverter antes daria -54 - RV-45).
6. **UM sinal de porcentagem, nunca dois**: cada rotulo tem exatamente um `%` (e o
   total do parenteses, outro).
7. **`DamageReduction` e `ManaCostMod` tem o sinal do TEXTO invertido em relacao ao
   atributo** (l.897): `DamageReduction` +20 vira `Damage taken −20%`; `ManaCostMod`
   -50 vira `Mana Costs reduced by 50%`, e um total POSITIVO e custo AUMENTADO (RV-43).
8. O sinal de menos e o U+2212 do mod (l.927) - nao um hifen ASCII.

DE ONDE VEM O ESPERADO
----------------------
`excesso-shrine.esperado.json` (oraculo em C#, `Mathf.CeilToInt`). O teste ainda LE
o `ShrineAuraPatch.cs` vivo e confere que os literais das etiquetas continuam la:
assim a expectativa fica amarrada a FONTE, e nao a uma copia que pode envelhecer.
"""
import os

import arcabouco as arc
import regras_shrine as reg

META = {
    "nome": "shrine-excesso-formatacao",
    "categoria": "pura",
    "requer": [],
    "descricao": "bordas de formato: Ceil da ficha, .5, -0.4, inteiro sem .0, um % por rotulo e U+2212",
}

# Os literais que a fixture assume existirem no mod vivo (os rotulos dos atributos
# conhecidos e a regra do sinal). Se a redacao mudar la, o teste avisa que a
# expectativa precisa de nova revisao - em vez de continuar "verde" contra um texto
# que nao existe mais.
LITERAIS_DA_FONTE = (
    ('"Damage taken \u2212"', "o rotulo do DamageReduction invertido (l.903)"),
    ('"Mana Costs reduced by "', "o rotulo do ManaCostMod reduzido (l.905)"),
    ('"Mana Costs increased by "', "o rotulo do ManaCostMod aumentado (l.906)"),
    ('"Dodge "', "o rotulo do DodgeChance (l.909)"),
    ("Mathf.CeilToInt(v)", "a convencao inteira da ficha (InteiroDoJogo, l.952)"),
    ('n >= 0 ? "+" : "\u2212"', "o sinal explicito com o menos U+2212 (ComSinal, l.927)"),
)


def corpo():
    esp = reg.esperado_do_caso()
    casos = reg.por_id(esp["formatacao"])

    # ------------------------------------------------------------------ as bordas da fixture
    for cid, c in casos.items():
        arc.igual(reg.inteiro_do_jogo(c["valor"]), c["inteiro"],
                  "inteiro da ficha para %s (valor %s)" % (cid, c["valor"]))
        arc.igual(reg.com_sinal(c["valor"]), c["com_sinal"], "sinal de %s" % cid)
        arc.igual(reg.formatar(c["atributo"], c["valor"]), c["rotulo"], "rotulo de %s" % cid)
        arc.igual(reg.total_com_sinal(c["atributo"], c["valor"]), c["total_com_sinal"],
                  "o total do parenteses de %s" % cid)
        # UM sinal de % por numero - nem zero, nem dois.
        arc.igual(c["rotulo"].count("%"), 1, "o rotulo de %s tem exatamente um sinal de %%: %r"
                  % (cid, c["rotulo"]))
        arc.igual(c["total_com_sinal"].count("%"), 1, "o total de %s tem exatamente um %%" % cid)
        arc.exigir("%%" not in c["rotulo"] and "%%" not in c["total_com_sinal"],
                   "o valor de %s saiu com DOIS sinais de porcentagem: %r / %r"
                   % (cid, c["rotulo"], c["total_com_sinal"]))

    # ------------------------------------------------------------------ nomeando cada borda
    frac = casos["equipamento-fracionario"]
    arc.igual(reg.formatar(frac["atributo"], frac["valor"]), "Dodge +54%",
              "BORDA do equipamento: 53.4 com a convencao do Ceil do jogo (o print do dono tinha 53.4)")
    arc.exigir(".0" not in reg.formatar("CritChance", casos["inteiro-nao-ganha-ponto"]["valor"]),
               "o inteiro ganhou '.0' - a linha azul nao pode destoar da ficha")
    arc.igual(reg.inteiro_do_jogo(0.5), 1, "BORDA .5: Ceil(0.5) = 1")
    arc.igual(reg.com_sinal(-0.4), "+0",
              "BORDA -0.4: o sinal e lido DEPOIS do arredondamento (Ceil(-0.4) = 0 -> '+0')")
    arc.exigir(reg.com_sinal(-0.4) != "\u22120", "saiu '-0' - a leitura do sinal esta antes do arredondamento")
    arc.igual(reg.inteiro_do_jogo(-53.4), -53,
              "BORDA do negativo fracionario: Ceil(-53.4) = -53 (inverter antes daria -54, RV-45)")
    arc.igual(reg.formatar("DamageMod", -25.0), "Damage \u221225%",
              "o menos e o U+2212 do mod, nao o hifen")
    arc.exigir("-" not in reg.formatar("DamageMod", -25.0),
               "saiu com hifen ASCII no lugar do U+2212")

    # ------------------------------------------------------------------ os dois atributos invertidos
    arc.igual(reg.formatar("DamageReduction", 20.0), "Damage taken \u221220%",
              "DamageReduction POSITIVO reduz o dano tomado: o rotulo inverte o sinal")
    arc.igual(reg.formatar("DamageReduction", -30.0), "Damage taken +30%",
              "DamageReduction NEGATIVO aumenta o dano tomado (o total do print do dono)")
    arc.igual(reg.total_com_sinal("DamageReduction", -30.0), "+30%",
              "o total do parenteses segue a MESMA grandeza e o mesmo sinal invertido")
    arc.igual(reg.formatar("ManaCostMod", -50.0), "Mana Costs reduced by 50%",
              "Energy Coil: o EFEITO e -50 e o texto diz reduzido")
    arc.igual(reg.formatar("ManaCostMod", 20.0), "Mana Costs increased by 20%",
              "RV-43: total POSITIVO de ManaCostMod e custo AUMENTADO")
    arc.igual(reg.item("ManaCostMod", -100.0, 20.0), "Mana Costs reduced by 100% (total +20%)",
              "RV-43: a aura empurra -100 e o TOTAL da ficha e +20 - os dois numeros sem se contradizer")

    # ------------------------------------------------------------------ a fonte viva
    caminho = os.path.join(arc.raiz_do_repo(), "BetterTooltips", "Patches", "ShrineAuraPatch.cs")
    arc.exigir(os.path.isfile(caminho),
               "a fonte dos rotulos sumiu: %s (o teste vigia o mod vivo)" % caminho)
    with open(caminho, encoding="utf-8") as fh:
        fonte = fh.read()
    for literal, o_que in LITERAIS_DA_FONTE:
        arc.exigir(literal in fonte,
                   "o literal %s nao esta mais no mod (%s) - a fixture desta familia precisa de nova"
                   " revisao contra o ShrineAuraPatch.cs" % (literal, o_que))

    print("formatacao: %d bordas conferidas contra o oraculo e %d literais da fonte viva"
          % (len(casos), len(LITERAIS_DA_FONTE)))


if __name__ == "__main__":
    arc.main(META, corpo)
