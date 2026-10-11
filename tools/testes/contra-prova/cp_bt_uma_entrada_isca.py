#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) do cenario 1 - UMA ENTRADA POR TEXTO.

O DEFEITO PLANTADO: a fixture `uma-entrada-plantada.entrada.cs` tem (a) chave repetida DENTRO
de TextFixes e (b) a MESMA chave em TextFixes e TextAppends. Esta isca acredita na expectativa
ERRADA - "o fonte plantado esta limpo" - e por isso REPROVA: as ferramentas veem os dois
defeitos. E o mesmo que o `cp_formato_notas_isca.py` faz (acredita na regra antiga e reprova).

A metade que PASSA e `cp_bt_uma_entrada_ok.py` (o LocalizePatch.cs real esta limpo); quem casa
as duas e `testes/puros/t_bt_contra_prova.py`.
"""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "contra-prova-bt-uma-entrada",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: o fonte plantado 'esta limpo' - mas tem chave duplicada e chave nas duas tabelas",
}


def corpo():
    plantado = arc.ler_texto("uma-entrada-plantada", "entrada", "cs")
    caminho = arc.caminho_fixture("uma-entrada-plantada", "entrada", "cs")

    dup = R.chaves_duplicadas(plantado, "TextFixes")
    cross = R.chaves_nas_duas_tabelas(plantado)
    codigo, saida = R.roda_chave_compartilhada(caminho)

    acusacoes = []
    if dup:
        acusacoes.append("check_dupes: chave duplicada %r" % dup)
    if cross:
        acusacoes.append("chave nas duas tabelas: %r" % cross)
    if codigo != 0:
        linha = [l.strip() for l in saida.splitlines() if "chave nas duas tabelas" in l]
        acusacoes.append("check_chave_compartilhada --estrito reprovou (exit %d): %s"
                         % (codigo, linha or saida.strip().splitlines()[-1:]))

    # A EXPECTATIVA ANTIGA (o defeito): "o fonte plantado nao tem defeito nenhum".
    arc.exigir(not acusacoes,
               "o fonte plantado devia estar LIMPO (o defeito nao existe). As ferramentas "
               "acusaram: " + "; ".join(acusacoes))


if __name__ == "__main__":
    arc.main(META, corpo)
