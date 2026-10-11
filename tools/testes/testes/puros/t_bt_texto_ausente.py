#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TEXTO DO JOGO AUSENTE OU INESPERADO (TST-3, cenario 4) - texto INTACTO + motivo, nunca metade.

O QUE ESTE TESTE PRENDE
-----------------------
`LocalizePatch.Postfix` (l.2248-2262) tira um SNAPSHOT de `__result`, roda
`AplicarNotasDoFunil` DENTRO de try/catch e, na excecao, devolve o snapshot INTACTO mais
`RegistrarFalhaIgnorada` (l.2272-2288) - que loga UMA vez por motivo distinto.

Os TRES casos:

  1. A CHAVE NAO EXISTE MAIS - nao casa o lookup -> o texto do jogo fica como veio;
  2. A EXPRESSAO NAO AVALIA - a regra dinamica lanca -> snapshot intacto + motivo no log;
  3. VALOR NULO no dicionario - `AnexarNota` (l.2033) devolve o texto quando a nota e vazia.

Em NENHUM caso o mod pode escrever "pela metade": o texto devolvido tem de ser EXATAMENTE o
snapshot. A isca `cp_bt_texto_ausente_isca.py` usa a regra SEM guarda (a excecao escapa) e
REPROVA; a metade que PASSA e `..._ok.py`.
"""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "bt-texto-ausente",
    "categoria": "pura",
    "requer": [],
    "descricao": "chave morta, expressao que nao avalia e valor nulo deixam o texto do jogo intacto e a falha e DECLARADA - nunca escrita pela metade",
}


def corpo():
    real = R.le_fonte()

    # PIN: o snapshot, o try/catch e o registro da falha tem de existir no FONTE.
    R.pin(real, "string textoDoJogo = __result;", "o snapshot do texto do jogo")
    R.pin(real, "catch (Exception e)", "o try/catch do Postfix")
    R.pin(real, "RegistrarFalhaIgnorada(\"postfix do funil OptionsManager.Localize\", e)",
          "a falha declarada no log (nunca em silencio)")
    R.pin(real, "if (string.IsNullOrEmpty(nota))", "o AnexarNota tolera nota vazia/nula")

    viol = R.violacoes_do_funil("seguro")
    arc.igual(viol, [], "falha no texto ausente/inesperado: %s" % viol)

    # Prova independente do caso 2: o motivo tem de nomear a excecao (a falha e declarada).
    def lanca(_o, _r):
        raise RuntimeError("explodiu")

    _texto, motivo = R.funil("Texto Com [0]", "Texto Com [0]", {}, {}, dinamico=lanca)
    arc.exigir(motivo and "RuntimeError" in motivo,
               "a falha tinha de ser declarada com o tipo da excecao; veio: %r" % motivo)

    print("3 casos (chave morta / expressao que nao avalia / valor nulo) mantem o texto do "
          "jogo intacto e declaram a falha")


if __name__ == "__main__":
    arc.main(META, corpo)
