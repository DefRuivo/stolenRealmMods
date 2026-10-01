#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do par do REL-1: o MESMO pre-flight, com a trava desligada e ligada.

Par deste arquivo: `cp_rel_artefato_velho_recusado.py`. Fora do bloco `BLOCO-DO-DEFEITO` os
dois sao identicos (quem confere e a parte 4 de `testes/puros/t_trava_artefato_fonte.py`),
como manda o README do arcabouco: a isca e o conserto so podem diferir NO QUE DESCREVE O
DEFEITO.

O plantio e o mesmo nos dois: um mod com a FONTE MAIS NOVA que a DLL (o defeito medido em
01/10/2026, quando o empacotador teria entregue a Release de 30/09 com o defeito no lugar do
conserto). A expectativa do corpo tambem e a mesma e e a trava VIVA: a DLL velha tem de ser
RECUSADA. O que muda, dentro do bloco, e se a trava esta ligada.

Este arquivo (a ISCA) desliga a trava `artefato_esta_atual` no modulo carregado, que e o
empacotador de ANTES do REL-1: sem ninguem conferindo, o pre-flight aceita a DLL velha em
silencio e a expectativa do corpo cai. Ele tem de sair REPROVOU (exit 1) pelo motivo certo -
nao ter pego o defeito.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import arcabouco as arc  # noqa: E402
import regras_rel as rel  # noqa: E402

META = {
    "nome": "contra-prova-rel-artefato-velho-isca",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: com a trava desligada o pre-flight ACEITA a DLL mais antiga que a fonte",
}


# >>> BLOCO-DO-DEFEITO
GUARDA = False   # empacotador de ANTES do REL-1: nada confere a DLL contra a fonte.
# <<< BLOCO-DO-DEFEITO


def corpo():
    with tempfile.TemporaryDirectory(prefix="rel1-cp-") as raiz:
        rel.monta_mod(raiz, nome="BetterTooltips", fonte_mais_nova=True)
        passou, mensagem = rel.roda_preflight(raiz, usar_guarda=GUARDA)
        # A expectativa nao muda: a DLL mais antiga que a fonte NUNCA pode ser aceita.
        arc.exigir(not passou,
                   "o pre-flight ACEITOU a DLL mais antiga que a fonte - empacotar entregaria "
                   "um binario sem a edicao (o defeito do REL-1)")
        arc.exigir("ARTEFATO VELHO" in mensagem,
                   "reprovou, mas por outro motivo: %s" % mensagem[:200])


if __name__ == "__main__":
    arc.main(META, corpo)
