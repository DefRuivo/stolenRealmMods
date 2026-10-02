#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) do NIV3-1 — o bloco de nivel 3 da SINERGIA que ficava atras da nota.

O DEFEITO PLANTADO: o prefixo `CorEOrdemDoTooltip` recolhia a linha de auras e as notas, mas NAO o
bloco `Your skills on this status` (escrito pelo `StatusSkillSynergyPatch` em outro gancho, e
excluido do `_conteudosDeNota` pelo `EhBlocoDoNivel3`). Numa tooltip com NOTA e sinergia, a nota era
devolvida pelo fim e ficava DEPOIS da linha azul — a linha azul deixava de ser a ultima (§9.1).

Esta isca acredita na expectativa de HOJE (`DEFEITOS_ESPERADOS = 0` dentro do bloco do defeito: "o
tooltip sai certo"). Como o desenho de hoje QUEBRA mesmo, este arquivo REPROVA citando o motivo.

O conserto e o `cp_nivel3_sinergia_ok.py`, ao lado — os dois sao o MESMO teste fora do bloco
`BLOCO-DO-DEFEITO` (quem confere isso e `testes/puros/t_nivel3_sinergia.py`).
"""
import arcabouco as arc
import regras_nivel3 as n3

META = {
    "nome": "contra-prova-nivel3-sinergia",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: sem recolher o bloco de sinergia, a nota sai DEPOIS da linha azul do nivel 3",
}


# >>> BLOCO-DO-DEFEITO
REGRA = "sem-sinergia"   # o prefixo NAO recolhe o bloco de sinergia (o desenho de hoje).
DEFEITOS_ESPERADOS = 0   # a expectativa de hoje: "o tooltip sai certo" (o defeito nao existia).
# <<< BLOCO-DO-DEFEITO


def corpo():
    print(n3.corpo_da_contra_prova(REGRA, DEFEITOS_ESPERADOS))


if __name__ == "__main__":
    arc.main(META, corpo)
