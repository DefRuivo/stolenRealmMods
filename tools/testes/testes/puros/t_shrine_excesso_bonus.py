#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EXCESSO DE SHRINE (TST-2): a CADEIA do `ShrineEffectBonus` e a escala das 12 auras.

O QUE ESTE TESTE GARANTE
------------------------
1. O bonus total de cada caso sai da SOMA das fontes EFETIVAS (RV-19 §3):
   `Worship` (+100) + `Omnism II` (+20) = 120; as tres bencaos somam; e
   `Omnism I` + `Omnism II` = **20, NAO 28** - a I e da lista `SkillsThatReplace`
   da II e o motor DESCARTA a substituida (o teste do proprio jogo,
   `LearnAndExpectAttributeDelta(..., "CHAOS_2_P1_Omnism II", "ShrineEffectBonus", 20f)`,
   decompilado l.183505, asserta o delta de 20).
2. A contribuicao de cada aura em cada bonus do eixo e
   `Mathf.Round(BASE * (1 + bonus/100))` - half-to-even, fator e produto em FLOAT -
   com a BASE lida da tabela gerada (nunca digitada aqui).
3. Nos casos 0/20/100 o ORACULO (C#) e a TABELA GERADA do repositorio
   (`tools/dados/shrines-esperado.csv`) CONCORDAM linha a linha: o teste confere a
   coincidencia. Se a fonte do repositorio mudar, ele acusa - e a fixture e que
   fica velha.

DE ONDE VEM O ESPERADO (nada aqui e "de cabeca")
------------------------------------------------
* `excesso-shrine.esperado.json` - o ORACULO em C#
  (`tools/testes/fixtures/geradores/oraculo_excesso_shrine`), que passa pelo caminho
  de conta do motor: float + `Math.Round` ToEven + `Mathf.CeilToInt`.
* `tools/dados/shrines-esperado.csv` - tabela GERADA por
  `tools/gera_shrines_esperado.py` de `docs/cobertura/status.csv` (o censo do dump)
  e do `resources.assets`; cada linha cita a fonte da base.
* `docs/cobertura/revisao/RV-19-shrines.md` §2.2 (a escala) e §3 (as fontes).
"""
import arcabouco as arc
import regras_shrine as reg

META = {
    "nome": "shrine-excesso-bonus",
    "categoria": "pura",
    "requer": [],
    "descricao": "cadeia do ShrineEffectBonus (0/8/20/50/100 + combinacoes) e a escala das auras",
}

# O eixo de bonus da fixture. NAO e uma lista de valores esperados: e a lista de
# entrada que o oraculo percorreu (o esperado de cada um esta na fixture).
EIXO_MINIMO = (0, 8, 20, 50, 100)


def corpo():
    ent = reg.entrada_do_caso()
    esp = reg.esperado_do_caso()
    casos = reg.por_id(ent["bonus"])
    esperado_bonus = reg.por_id(esp["bonus_total"])

    # ------------------------------------------------------------------ 1. a cadeia
    arc_ids = sorted(casos)
    if arc_ids != sorted(esperado_bonus):
        raise arc.Falhou("os casos de bonus da entrada e do esperado nao batem: %s x %s"
                             % (arc_ids, sorted(esperado_bonus)))
    for cid in arc_ids:
        caso = casos[cid]
        esperado = esperado_bonus[cid]
        obtido = reg.bonus_total(caso["fontes"])
        arc.igual(obtido, esperado["total"],
                      "bonus '%s' (%s)" % (cid, " + ".join(caso["fontes"]) or "sem fonte"))
        substituidas = [f for f in caso["fontes"] if f not in reg.fontes_efetivas(caso["fontes"])]
        arc.igual(sorted(substituidas), sorted(esperado["substituidas"]),
                      "fontes substituidas do caso '%s'" % cid)

    # Os casos que o dono pediu, nomeados - cada numero vem do proprio esperado
    # (mensagem diz a conta; o valor nao e digitado).
    def total(cid):
        return esperado_bonus[cid]["total"]

    arc.igual(reg.bonus_total([]), total("sem-bonus"), "sem bencao: o total e 0")
    arc.igual(reg.bonus_total(["Omnism II"]), total("omnism2"), "Omnism II sozinha (+20)")
    arc.igual(reg.bonus_total(["Worship"]), total("worship"), "Worship sozinho (+100)")
    arc.igual(reg.bonus_total(["Horn of Devotion (+50)"]), total("horn-50"),
                  "Horn no roll de +50")
    arc.igual(reg.bonus_total(["Worship", "Omnism II"]), total("worship-omnism2"),
                  "Worship (+100) + Omnism II (+20) = a soma das duas fontes")
    arc.igual(reg.bonus_total(["Worship", "Horn of Devotion (+50)"]), total("worship-horn50"),
                  "Worship (+100) + Horn (+50)")
    arc.igual(reg.bonus_total(["Worship", "Omnism II", "Horn of Devotion (+50)"]),
                  total("tres-bencaos"), "as TRES bencaos acumuladas")
    # A SUBSTITUICAO: com as duas tiers o total e o da II, NAO a soma 8 + 20.
    arc.igual(reg.bonus_total(["Omnism I", "Omnism II"]), total("omnism1-omnism2"),
                  "Omnism I + Omnism II: a I e SUBSTITUIDA pela II (20, nao 8 + 20)")
    arc.exigir(total("omnism1-omnism2") != reg.FONTES["Omnism I"] + reg.FONTES["Omnism II"],
                   "a fixture esta somando as duas tiers (28): a substituicao do RV-19 §3 nao esta valendo")
    arc.igual(reg.bonus_total(["Worship", "Omnism I", "Omnism II"]), total("tres-omnism"),
                  "tres fontes com as duas tiers dentro: a I cai, sobram 100 + 20")

    # ------------------------------------------------------------------ 2. a escala
    esperado_escala = {}
    for e in esp["escala"]:
        esperado_escala[(e["aura"], e["base"], e["bonus"])] = e["contribuicao"]
    vistas = set()
    for e in esp["escala"]:
        obtido = reg.escala(e["base"], e["bonus"])
        arc.igual(obtido, e["contribuicao"],
                      "escala da aura '%s' (base %s) com bonus %s" % (e["aura"], e["base"], e["bonus"]))
        vistas.add((e["aura"], e["atributo"]))
    # Toda aura x atributo da tabela gerada tem de estar na matriz (nada de aura sumida).
    da_tabela = {(aura, atributo) for aura, por_atributo in reg.auras_da_tabela().items()
                 for atributo in por_atributo}
    arc.igual(sorted(vistas), sorted(da_tabela),
                  "a matriz da escala tem de cobrir todas as (aura, atributo) da tabela gerada")
    # A familia e de 12 auras (RV-19 §2): 9 com atributo de personagem + as 3 sem
    # atributo (Dwarven/Decay/Flame). Uma aura nova ou renomeada na tabela acusa aqui.
    arc.igual(sorted(reg.auras_da_tabela()), sorted(reg.AURAS_DA_FAMILIA),
              "a familia de auras da tabela gerada x a familia do RV-19 §2")

    # ------------------------------------------------------------------ 3. oraculo x tabela GERADA
    # A tabela do repositorio e a SEGUNDA fonte: o teste refaz a conta dela com a
    # nossa formula e confere o que a fixture diz - os tres tem de concordar.
    linhas = reg.tabela_esperado()
    arc.exigir(linhas, "tools/dados/shrines-esperado.csv sem linhas")
    conferidas = 0
    for linha in linhas:
        base = float(linha["base"])
        caso = int(float(linha["caso_bonus"]))
        esperado_csv = float(linha["contribuicao_esperada"])
        arc.igual(reg.escala(base, caso), esperado_csv,
                      "tabela gerada: %s/%s base %s com bonus %s (%s)"
                      % (linha["aura"], linha["atributo"] or "(sem atributo)", linha["base"],
                         linha["caso_bonus"], linha["fonte_base"]))
        chave = (linha["aura"], base, caso)
        if chave in esperado_escala:
            arc.igual(esperado_escala[chave], esperado_csv,
                          "o oraculo e a tabela gerada discordam em %s base %s bonus %s"
                          % (linha["aura"], base, caso))
            conferidas += 1
    arc.exigir(conferidas > 0,
                   "nenhuma linha da tabela gerada casou com a matriz da fixture - a fixture esta velha")

    # O eixo da fixture tem de conter os 5 casos provados pela tabela gerada.
    eixo = set(ent["eixo_bonus"])
    for caso in EIXO_MINIMO:
        arc.exigir(caso in eixo, "o eixo de bonus da fixture perdeu o caso %s" % caso)
    # ... e os caso_bonus da tabela gerada tem de estar dentro do eixo.
    for linha in linhas:
        caso = int(float(linha["caso_bonus"]))
        arc.exigir(caso in eixo,
                       "a tabela gerada tem o caso_bonus %s e o eixo da fixture nao" % caso)

    # As fontes de bonus usadas pela fixture existem no modulo (nenhum nome solto).
    for cid, caso in casos.items():
        for fonte in caso["fontes"]:
            arc.exigir(fonte in reg.FONTES,
                           "a fixture usa uma fonte de bonus desconhecida: %r (caso %s)" % (fonte, cid))

    print("cadeia: %d casos; escala: %d valores conferidos contra o oraculo e a tabela gerada"
          % (len(casos), len(esp["escala"])))


if __name__ == "__main__":
    arc.main(META, corpo)
