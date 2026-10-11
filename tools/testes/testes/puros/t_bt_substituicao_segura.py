#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SUBSTITUICAO SEGURA (TST-3, cenario 2) - o mod so troca quando o exibido e o ingles original.

O QUE ESTE TESTE PRENDE
-----------------------
`LocalizePatch.AplicarNotasDoFunil` (l.2298-2303): "So mexemos quando o texto exibido e o
ingles original". Na pratica, `__result != original` faz RETURN e o lookup e por TEXTO EXATO
(`TextFixes.TryGetValue(original)` l.2315 / `TextAppends.TryGetValue(original)` l.2323).

Os TRES casos que a regra tem de RECUSAR (nenhum casa o lookup):

  1. TEXTO JA LOCALIZADO - o `original` chega em ingles, mas o `__result` ja veio traduzido;
  2. A CHAVE COMO SUBSTRING - "prefixo " + chave + " sufixo" NAO e a chave;
  3. MESMO COMECO, TEXTO DIFERENTE - chave + " e mais alguma coisa" NAO e a chave.

E o caso que ela tem de ACEITAR: `exibido == original` -> troca (correcao) ou anexa (nota).

A metade que REPROVA (regra por SUBSTRING) e `cp_bt_substituicao_isca.py`; a que PASSA e
`..._ok.py`; quem casa as duas e `t_bt_contra_prova.py`.
"""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "bt-substituicao-segura",
    "categoria": "pura",
    "requer": [],
    "descricao": "o funil so troca com o texto exibido == original em ingles: texto localizado, substring e mesmo-comeco ficam intactos",
}


def corpo():
    real = R.le_fonte()

    # PIN: a guarda tem de existir no FONTE de verdade (o espelho nao pode envelhecer sozinho).
    R.pin(real, "if (__result != original)", "a guarda 'so mexe no ingles original'")
    R.pin(real, "if (TextFixes.TryGetValue(original, out string fixedText))", "o lookup exato de TextFixes")
    R.pin(real, "else if (TextAppends.TryGetValue(original, out string append))", "o lookup exato de TextAppends")

    # Casos sobre as TABELAS DE VERDADE.
    viol = R.violacoes_da_substituicao(real, modo="estrito")
    arc.igual(viol, [], "substituicao segura divergiu: %s" % viol)

    # O caso "chave como substring" tem de ser RECUSADO de fato (nao pode virar troca).
    fixes = dict(R._tab.pares(real, "TextFixes"))
    chave = next(iter(fixes))
    obtido = R.substituir(chave, "prefixo " + chave + " sufixo", fixes, {})
    arc.igual(obtido, "prefixo " + chave + " sufixo",
              "a chave como SUBSTRING nao pode ser trocada (o lookup e exato)")

    print("5 casos de substituicao conferem contra as tabelas de verdade "
          "(%d TextFixes)" % len(fixes))


if __name__ == "__main__":
    arc.main(META, corpo)
