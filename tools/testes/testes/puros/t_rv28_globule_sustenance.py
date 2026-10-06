#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RV-28 (blindagem) - as GUARDAS do tooltip do globule e a MATRIZ de aceite numerica.

O QUE ESTE TESTE PRENDE
-----------------------
O `RV-28` escreve DENTRO da tooltip do jogo, a cada frame de hover, com o numero lido do personagem
em foco. Este teste prende as duas coisas que o cartao exige:

  * as 5 GUARDAS obrigatorias no FONTE VIVO de `BetterTooltips/Patches/GlobulePatch.cs`
    (assinatura explicita; try/catch com queda para SEM numero; o atributo EXISTE antes da leitura;
    alvo nulo; e a % que vem da lista ATIVA do jogo, nunca de uma soma a mao de tier I + II);
  * a MATRIZ de aceite com o exemplo do dono (personagem com 100 de vida e 200 de mana):
      cenario 2 -> Sustenance I  -> 8 de vida / 16 de mana
      cenario 3 -> Sustenance II -> 20 de vida / 40 de mana
      cenario 4 -> com UMA tier ativa o numero NUNCA soma a outra: 28 / 56 nao aparece

DE ONDE VEM A % (fonte INDEPENDENTE do log e do C# do mod): da ACAO do motor no censo
(`docs/cobertura/acoes.csv:255-256`): `Sustenance I Proc` = `Target.MaxHealth * .08f` e
`Sustenance II Proc` = `.20f`. O mod le a % da DESCRICAO do asset; a acao do proc e o que o motor
REALMENTE aplica — as duas tem de dar o mesmo numero, e este teste lê a segunda.

CENARIOS 1 e 5 (de TELA, ficam na conferencia humana — caminho reprodutivel):
  1. SEM Sustenance -> a tooltip NAO ganha numero nenhum (o texto base sai byte a byte igual).
     Como reproduzir: personagem sem nenhuma tier de Sustenance (ou com a skill respeitada),
     hover em qualquer globule no chao da batalha. Esperado: a descricao do globule
     (`Heals for 50% of Max Health`, `Restores 50% of Max Mana`, ...) sem nenhuma frase extra.
     No log: a marca `[Globule RV-28] '<chave>': <personagem> nao tem Sustenance ativa -> sem numero`
     (uma por combinacao).
  5. VIDA/MANA MUDANDO -> o numero acompanha na proxima abertura do tooltip. Como reproduzir:
     com Sustenance II ativa e a tooltip aberta em um globule, fechar, EQUIPAR/DESEQUIPAR um item que
     mexa em Max Health/Max Mana, reabrir a tooltip. O numero e `MaxHealth x 20%` lido NA HORA do
     hover (com cache curto de ~1s, `GlobulePatch.PctDasTiersAtivas`); ele tem de mudar junto com a
     ficha. Prova objetiva no log: duas marcas `[Globule RV-28] '<chave>': <personagem> ...` com
     numeros diferentes — a segunda depois da troca de equipamento (a marca sai uma vez por
     combinacao, entao no mesmo boot a segunda so aparece se o texto/numero mudar).
"""
import os
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(DIR)))      # tools/testes
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(DIR)), "testes", "puros"))

import arcabouco as arc                # noqa: E402
import regras_rv28_globule as R        # noqa: E402

META = {
    "nome": "rv28-globule-sustenance",
    "categoria": "pura",
    "requer": [],
    "descricao": "as guardas do tooltip do globule (fonte vivo) e a matriz 8/16, 20/40 e nunca 28/56",
}

# A % esperada sai da ACAO do motor (censo), nunca do log nem do comentario do mod.
PCT_TIER = {"Sustenance I": 8.0, "Sustenance II": 20.0}
# O exemplo do dono, literal no cartao.
VIDA, MANA = 100, 200


def corpo():
    fonte = R.le_fonte()

    # --------------------------------------------------------------------- #
    # 1. AS GUARDAS no fonte vivo
    # --------------------------------------------------------------------- #
    viol = R.guardas_do_globule(fonte)
    arc.igual(viol, [], "guardas obrigatorias do tooltip do globule: %s" % viol)

    # O GANCHO tem de ser explicito por TIPO (nunca resolucao por nome) e passar pelo mesmo funil.
    localize = R.le_fonte(R.LOCALIZE)
    arc.exigir("[HarmonyPatch(typeof(OptionsManager), nameof(OptionsManager.Localize))]" in localize,
               "o gancho do Localize perdeu a assinatura explicita por tipo")
    arc.exigir("if (GlobulePatch.EhGlobule(original))" in localize,
               "o postfix do Localize nao consulta mais `GlobulePatch.EhGlobule`")
    arc.exigir("GlobulePatch.FraseSustenance(original)" in localize,
               "o postfix do Localize nao chama mais `GlobulePatch.FraseSustenance`")

    # --------------------------------------------------------------------- #
    # 2. A ISCA EMBUTIDA: cada defeito plantado tem de ser MORGADO pela checagem
    # --------------------------------------------------------------------- #
    vistos = 0
    for nome, defeituoso, o_que_morde in R.iscas():
        v = R.guardas_do_globule(defeituoso)
        arc.exigir(v, "a checagem NAO mordeu o defeito %r (ela nao vale: %s)" % (nome, o_que_morde))
        vistos += 1
    arc.igual(vistos, 4, "as 4 iscas plantadas tem de ser exercitadas")

    # --------------------------------------------------------------------- #
    # 3. A MATRIZ (a % vem do censo das acoes; o pool e o do exemplo do dono)
    # --------------------------------------------------------------------- #
    acoes = R.pct_das_acoes()
    for tier, pct in PCT_TIER.items():
        arc.exigir(tier in acoes, "a acao `%s Proc` sumiu do censo (%s)" % (tier, R.ACOES))
        arc.igual(acoes[tier], pct, "a %% de `%s` no censo das acoes" % tier)

    # cenario 2 - Sustenance I
    h, m = R.cura(VIDA, MANA, R.pct_das_tiers(["Sustenance I"], acoes))
    arc.igual((h, m), ("8", "16"), "cenario 2 (Sustenance I, 100/200)")
    arc.exigir((h, m) != ("28", "56"), "cenario 2 somou a tier II")

    # cenario 3 - Sustenance II
    h, m = R.cura(VIDA, MANA, R.pct_das_tiers(["Sustenance II"], acoes))
    arc.igual((h, m), ("20", "40"), "cenario 3 (Sustenance II, 100/200)")

    # cenario 4 - com UMA tier ativa, o numero NUNCA soma a outra (28/56 nao existe)
    for tier, esperado in (("Sustenance I", ("8", "16")), ("Sustenance II", ("20", "40"))):
        obtido = R.cura(VIDA, MANA, R.pct_das_tiers([tier], acoes))
        arc.igual(obtido, esperado, "cenario 4 (%s sozinha)" % tier)
        arc.exigir(obtido != ("28", "56"),
                   "cenario 4: com so a %s ativa o numero virou 28/56 (a outra tier foi somada a mao)"
                   % tier)

    # a matriz publicada (a que vai para a doc do aceite) tem de bater com o acima
    for linha in R.matriz():
        if linha["cenario"] == 2:
            arc.igual((linha["health"], linha["mana_exibida"]), ("8", "16"), "matriz cenario 2")
        elif linha["cenario"] == 3:
            arc.igual((linha["health"], linha["mana_exibida"]), ("20", "40"), "matriz cenario 3")
        elif linha["cenario"] == 4:
            arc.exigir((linha["health"], linha["mana_exibida"]) != ("28", "56"),
                       "matriz cenario 4 trouxe 28/56 com tiers=%s" % linha["tiers"])

    # --------------------------------------------------------------------- #
    # 4. A PONTE com o harness: as linhas que o avaliador AUT-6 aceitou tem de fechar com o modelo
    # --------------------------------------------------------------------- #
    # O cenario do harness com as DUAS tiers ativas (8 + 20) e a soma do que o JOGO tem ligado — a
    # duvida "a tier II substitui a I?" e o ponto aberto do RV-24, fora deste cartao. O que este
    # teste trava e que a soma e SEMPRE a das tiers que o jogo tem ativas, nunca uma soma do mod:
    # com uma tier o numero e 8/16 ou 20/40 (acima), e so com as duas ele chega a 28/56.
    linhas = R.linhas_da_fixture_aut6()
    arc.exigir(len(linhas) >= 2, "a fixture do AUT-6 perdeu as linhas do globule (%s)" % R.FIXTURE_AUT6)
    declarado = R.caso_globule_aut6()
    for linha in linhas:
        pct = R.pct_das_tiers(linha["tiers"], acoes)
        arc.igual(linha["pct"], pct,
                  "a %% da linha do AUT-6 (%s / %s) contra o censo das acoes"
                  % (linha["char"], "+".join(linha["tiers"])))
        pool = declarado.get(linha["char"]) or {}
        arc.exigir(pool, "o personagem %r da fixture nao esta declarado no caso do AUT-6" % linha["char"])
        arc.igual(linha["tiers"], pool["tiers"], "as tiers da linha de %s" % linha["char"])
        h, m = R.cura(pool["max_health"], pool["max_mana"], pct)
        arc.igual((h, m), (linha["health"], linha["mana"]),
                  "a frase de %s contra o pool declarado (%s/%s) x a %% do motor"
                  % (linha["char"], pool["max_health"], pool["max_mana"]))
        # com UMA tier ativa, nenhuma linha do harness pode trazer 28/56
        if len(linha["tiers"]) == 1:
            arc.exigir((linha["health"], linha["mana"]) != ("28", "56"),
                       "linha de UMA tier ativa em %s somou a outra tier" % linha["char"])

    print("guardas OK no fonte vivo (incl. a guarda de EXISTENCIA antes do indexador); 4 iscas "
          "mordidas; matriz 8/16 e 20/40 com 100/200; nunca 28/56 com uma tier ativa; "
          "ponte com o AUT-6 fecha")
    print("cenarios 1 e 5 (tela) ficam na conferencia humana — caminho reprodutivel na docstring")


if __name__ == "__main__":
    arc.main(META, corpo)
