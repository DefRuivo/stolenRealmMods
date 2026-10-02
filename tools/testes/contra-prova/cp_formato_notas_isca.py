#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) do FORMATO das notas (RV-17) — o defeito que a COR-3R achou.

O DEFEITO PLANTADO: o prefixo extraia SO A PRIMEIRA nota do mod e consumia UMA quebra do
separador. Com isso (a) a SEGUNDA nota dos dois casos reais (`Shapeshift Dragonkin`, que tem `[0]`,
e o buff `Miniature`) ficava onde estava — ANTES do `AP Cost` — e a ordem de leitura invertia, e
(b) a outra quebra ficava ORFA entre a descricao e o `AP Cost`.

Esta isca acredita na expectativa ANTIGA (`DEFEITOS_ESPERADOS = 0` dentro do bloco do defeito:
"o tooltip sai certo"). Como o desenho antigo QUEBRA mesmo, este arquivo REPROVA citando o motivo
do formato.

O conserto e o `cp_formato_notas_ok.py`, ao lado — os dois sao o MESMO teste fora do bloco
`BLOCO-DO-DEFEITO` (quem confere isso e `testes/puros/t_formato_notas.py`).
"""
import arcabouco as arc
import regras_formato as fmt

META = {
    "nome": "contra-prova-formato-notas",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: a regra de ANTES do RV-17 (uma nota so, uma quebra so) deixa o tooltip QUEBRADO",
}


# >>> BLOCO-DO-DEFEITO
REGRA = "antiga"        # parava na PRIMEIRA nota e consumia UMA quebra do separador.
DEFEITOS_ESPERADOS = 0  # a expectativa antiga: "o formato sai certo" (o defeito nao existia).
# <<< BLOCO-DO-DEFEITO


def corpo():
    print(fmt.corpo_da_contra_prova(REGRA, DEFEITOS_ESPERADOS))


if __name__ == "__main__":
    arc.main(META, corpo)
