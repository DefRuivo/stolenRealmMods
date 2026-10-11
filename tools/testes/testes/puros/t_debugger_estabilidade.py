#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ESTABILIDADE das categorias do censo (TST-5) - nenhum campo pode desaparecer.

O QUE ESTE TESTE PRENDE (e por que existe)
------------------------------------------
O dump do RoguelikeDebugger alimenta `docs/cobertura/*.csv` por categoria. As COLUNAS
desses CSVs sao o contrato do censo: `tools/census.py` escreve o cabecalho declarado em
`CATS` e o projeto ja anexou colunas a mao (a coluna `status` da revisao, `dur`, `maxStk`)
DEPOIS dele. Duas coisas silenciosas podem acontecer e este teste as impede:

  * uma COLUNA do `census.py` desaparecer -> a rodada do censo reescreve o CSV sem ela;
  * o censo LER (`f.get(...)`) uma chave que o `FIELD` nao reconhece -> a coluna sai
    VAZIA em silencio, sem erro nenhum.

ESTE TESTE EXIGE
----------------
  1. As SETE categorias do censo continuam as mesmas.
  2. Para cada categoria, as colunas declaradas no `census.py` sao o PREFIXO do
     cabecalho do CSV VERSIONADO `docs/cobertura/<arquivo>` (procedencia: o CSV e o
     artefato; nada digitado). Nenhuma coluna some, nem muda de ordem.
  3. Toda chave que o censo le com `f.get(chave)` existe no `FIELD` (senao vira vazio).
  4. Nenhum cabecalho tem coluna repetida (a segunda seria escrita por engano).

PROVA DE FOGO
-------------
Isca embutida (coluna removida / chave fora do FIELD / CSV encurtado, em copias em
memoria) + a prova FISICA no `tools/census.py` real (restaurado byte a byte com sha256)
em `tools/testes/debugger-prova-de-fogo.log`.

O QUE ESTE TESTE NAO PROVA
--------------------------
Nao roda o `parse()` (ele ESCREVE os CSVs); nao executa o C# do mod. Le os cabecalhos
versionados e a fonte do censo.
"""
import ast
import csv
import os

import arcabouco as arc
import regras_debugger as rd

META = {
    "nome": "debugger-estabilidade",
    "categoria": "pura",
    "requer": [],
    "descricao": ("as 7 categorias do censo continuam, as colunas de cada uma sao o prefixo "
                  "do CSV versionado (nenhuma some) e toda chave lida com f.get existe no "
                  "FIELD (senao a coluna vira vazia) - com isca embutida"),
}

CENSO = rd.carrega_censo()
CATEGORIAS = {"Skill", "Action", "Summon", "Status", "Item", "ItemMod", "Powerup"}


def _chaves_lidas(codigo_censo):
    """As chaves passadas a `f.get("...")` no `census.py` (analise do AST)."""
    arvore = ast.parse(codigo_censo)
    chaves = set()
    for no in ast.walk(arvore):
        if (isinstance(no, ast.Call) and isinstance(no.func, ast.Attribute)
                and no.func.attr == "get" and isinstance(no.func.value, ast.Name)
                and no.func.value.id == "f" and no.args
                and isinstance(no.args[0], ast.Constant)
                and isinstance(no.args[0].value, str)):
            chaves.add(no.args[0].value)
    return chaves


def _cabecalhos_csv(arquivos):
    """Le a PRIMEIRA linha (cabecalho) de cada CSV versionado."""
    cabecalhos = {}
    base = os.path.join(arc.raiz_do_repo(), "docs", "cobertura")
    for arquivo in arquivos:
        caminho = os.path.join(base, arquivo)
        arc.exigir(os.path.isfile(caminho), "nao achei o CSV versionado %s" % caminho)
        with open(caminho, encoding="utf-8", newline="") as fh:
            cabecalhos[arquivo] = next(csv.reader(fh))
    return cabecalhos


def _falhas_de_estabilidade(cats, cabecalhos_csv, whitelist, chaves):
    falhas = []
    for cat in sorted(cats):
        arquivo, colunas = cats[cat]
        if len(set(colunas)) != len(colunas):
            falhas.append("categoria %s: coluna REPETIDA no censo %s" % (cat, colunas))
        if arquivo not in cabecalhos_csv:
            falhas.append("categoria %s: nao ha o CSV %s" % (cat, arquivo))
            continue
        csv_cols = cabecalhos_csv[arquivo]
        if colunas != csv_cols[:len(colunas)]:
            falhas.append("categoria %s (%s): as colunas do censo %s NAO sao o prefixo do "
                          "CSV versionado %s" % (cat, arquivo, colunas, csv_cols))
    for chave in sorted(chaves):
        if chave not in whitelist:
            falhas.append("o censo LE `f.get(%r)` mas o FIELD nao reconhece a chave - a "
                          "coluna vira VAZIA em silencio" % chave)
    return falhas


def corpo():
    cats = rd.cabecalhos_do_censo(CENSO)
    whitelist = rd.chaves_do_field(CENSO)
    chaves = _chaves_lidas(rd.le_censo_texto())

    # ------------------------------------------------ 1. as SETE categorias
    arc.igual(set(cats), CATEGORIAS,
              "as categorias do censo mudaram - uma categoria inteira pode ter sumido")

    # ------------------------------------------------ 2. colunas x CSV versionado
    cabecalhos = _cabecalhos_csv([cats[c][0] for c in sorted(cats)])
    falhas = _falhas_de_estabilidade(cats, cabecalhos, whitelist, chaves)
    arc.exigir(not falhas,
               "o contrato de colunas do censo regrediu:\n  - %s" % "\n  - ".join(falhas))

    para_relato = ", ".join("%s=%d" % (c, len(cats[c][1])) for c in sorted(cats))
    arc.exigir(len(chaves) >= 20, "achei poucas chaves `f.get` (%d) - a leitura do AST falhou?"
               % len(chaves))

    # ------------------------------------------------ 3. ISCAS embutidas
    # (a) uma COLUNA da categoria Skill some.
    cats_falta = {c: (cats[c][0], list(cats[c][1])) for c in cats}
    cats_falta["Skill"][1].remove("descricao")
    f = _falhas_de_estabilidade(cats_falta, cabecalhos, whitelist, chaves)
    arc.exigir(f, "a isca da coluna removida NAO mordeu")

    # (b) uma ORDEM trocada (tier antes de arvore).
    cats_ordem = {c: (cats[c][0], list(cats[c][1])) for c in cats}
    cols = cats_ordem["Skill"][1]
    cols[1], cols[2] = cols[2], cols[1]
    arc.exigir(_falhas_de_estabilidade(cats_ordem, cabecalhos, whitelist, chaves),
               "a isca da ordem trocada NAO mordeu")

    # (c) uma chave lida sai do FIELD -> a coluna vira vazia.
    whitelist_falta = [k for k in whitelist if k != "nEfeitosDano"]
    f = _falhas_de_estabilidade(cats, cabecalhos, whitelist_falta, chaves)
    arc.exigir(any("nEfeitosDano" in x for x in f),
               "a isca da chave fora do FIELD NAO mordeu: %s" % f)

    # (d) o CSV versionado perde uma coluna no meio.
    cabecalhos_curto = dict(cabecalhos)
    cabecalhos_curto["skills.csv"] = [c for c in cabecalhos["skills.csv"] if c != "tags"]
    f = _falhas_de_estabilidade(cats, cabecalhos_curto, whitelist, chaves)
    arc.exigir(any("Skill" in x for x in f), "a isca do CSV encurtado NAO mordeu: %s" % f)

    print("estabilidade: %d categorias (%s); %d chaves lidas com f.get, todas no FIELD; "
          "4 iscas reprovam pela razao certa" % (len(cats), para_relato, len(chaves)))


if __name__ == "__main__":
    arc.main(META, corpo)
