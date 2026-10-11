#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""COMPOSICAO DA TOOLTIP (TST-3, cenario 6) - ordem, uma linha em branco, idempotencia.

O QUE ESTE TESTE PRENDE
-----------------------
`LocalizePatch.CorEOrdemDoTooltip.Prefix` (l.231-243) recolhe as NOTAS (por CONTEUDO,
`TirarNotaDoMod` l.324-362) e a linha de AURAS/sinergia (por MARCADOR, `TirarBloco` l.260-302),
junto com o separador que o `AnexarNota` escreveu (`InicioDoSeparador` l.380-392, ate DUAS
quebras), e remonta:

    corpo  +  ("\\n\\n" + nota) para CADA nota  +  ("\\n\\n" + aura)  <- a aura por ULTIMO

Os invariantes (docs/TEXTO-TOOLTIPS.md §9.1):

  1. ORDEM - corpo, notas na ordem, a linha de auras SEMPRE por ultimo;
  2. UMA LINHA EM BRANCO antes de cada bloco (nunca o bloco colado, nunca 3+ quebras);
  3. IDEMPOTENCIA - passar o prefixo de novo NAO duplica nota nem linha.

A isca `cp_bt_composicao_isca.py` (aura antes das notas) e `cp_bt_composicao_idem_isca.py`
(sem extrair -> 2a passada duplica) REPROVAM; as metades `..._ok.py` PASSAM.
"""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "bt-composicao-tooltip",
    "categoria": "pura",
    "requer": [],
    "descricao": "o prefixo remonta corpo, notas (na ordem) e a linha de auras por ULTIMO, com uma linha em branco antes de cada bloco e sem duplicar na 2a passada",
}


def corpo():
    real = R.le_fonte()

    # PIN ESTRUTURAL: a ordem no C# e a montagem que o teste espelha.
    pos_nota = R.pin(real, 'corpo += "\\n\\n" + blocoNota;', "a nota anexada depois do corpo")
    pos_aura = R.pin(real, 'corpo += "\\n\\n" + aura;', "a linha de auras anexada")
    arc.exigir(pos_nota < pos_aura,
               "o C# tem de anexar a NOTA antes da AURA (a aura e a ultima): nota em %d, aura em %d"
               % (pos_nota, pos_aura))
    R.pin(real, "description.TrimEnd()", "o corpo e aparado antes de remontar")
    R.pin(real, "private static int InicioDoSeparador", "o consumo do separador (ate 2 quebras)")

    texto, conteudos = R.material_da_composicao()

    # 1..3 - ORDEM + LINHA EM BRANCO + IDEMPOTENCIA no caso correto.
    defeitos = R.defeitos_da_composicao(texto, conteudos, modo="rv17")
    arc.igual(defeitos, [], "a composicao rv17 divergiu: %s" % defeitos)

    saida = R.compoe(texto, conteudos, modo="rv17")

    # A saída e corpo, nota, aura - nessa ordem, um "\n\n" separando.
    corpo_txt = "Devour the life force of all enemies dealing 10 Shadow Damage."
    nota = "Each stack grants another 10% Max Health."
    esperado = (corpo_txt + "\n\n<color=#" + R.MARCADOR_NOTA + ">" + nota + "</color>"
                + "\n\n<color=#" + R.MARCADOR_AURA + ">Active shrine auras: +10 Might</color>")
    arc.igual(saida, esperado, "a remontagem corpo->nota->aura")

    # IDEMPOTENCIA explicita: compor de novo devolve o mesmo texto (nao duplica).
    arc.igual(R.compoe(saida, conteudos, modo="rv17"), saida,
              "a 2a passada nao pode mudar a tooltip")

    print("corpo->nota->aura conferem; 1 linha em branco por bloco; a 2a passada e identica "
          "(sem duplicar nota nem linha)")


if __name__ == "__main__":
    arc.main(META, corpo)
