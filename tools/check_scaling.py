#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Varredura de ESCALA (RV-8b-2i): a skill escala com algo que a tooltip nao diz?

Ideia: o texto da tooltip mostra o VALOR atual (o *N/[N] resolvido), mas nem sempre diz
DE QUE ele depende. O jogador fica sem saber se vale investir num atributo. Esta
varredura le as formulas de cada skill (attr + expr + danoExpr + efeitos da acao), tira
as FONTES de escala que aparecem nelas e cruza com as palavras do texto.

Saida: docs/cobertura/revisao/escala.md, com
  - o resumo por fonte (quantas skills usam cada uma)
  - a lista das que escalam com algo que o texto NAO menciona (o que interessa)

Uso: python tools/check_scaling.py [arvore]
"""
import csv
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tabelas as _tab  # noqa: E402  o parser UNICO das tabelas do LocalizePatch.cs

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COB = os.path.join(RAIZ, "docs", "cobertura")
SAIDA = os.path.join(COB, "revisao", "escala.md")
# O fonte do mod: para saber o que JA foi resolvido (o censo e o estado antes do mod).
FONTE_MOD = os.path.join(RAIZ, "BetterTooltips", "Patches", "LocalizePatch.cs")

# (regex na formula, nome legivel, palavras que a tooltip usaria para dizer isso)
FONTES = [
    (r"Source\.AttackPower", "Attack Power (dano de arma, cresce com Might)",
     None),   # None = caminho padrao de dano: a tooltip mostra o valor, nao precisa dizer
    (r"Source\.SpellPower\(\s*'(\w+)'\s*\)", "Spell Power de {0}", None),
    (r"Source\.GetFlatDamageValue", "NIVEL do personagem (curva Flat Damage)",
     ("level",)),
    (r"Source\.Level", "NIVEL do personagem", ("level",)),
    (r"Source\[\s*'([A-Za-z]+)'\s*\]", "atributo {0}", None),
    (r"Source\.NumAlliesWithin\(\s*(\d+)\s*\)", "aliados em {0} hexes", ("ally", "allies")),
    (r"Source\.SummonCount", "invocacoes ativas", ("summon",)),
    (r"Source\.HighestStatValue", "seu MAIOR atributo", ("highest",)),
    (r"Source\.LastDamageTypeTaken", "ultimo tipo de dano sofrido", ("last type",)),
    (r"Target\.Level", "NIVEL do ALVO", ("level",)),
    (r"Source\.MaxHealth|Source\[\s*'MaxHealth'\s*\]", "vida maxima", ("health",)),
    (r"Source\.IsShapeshifted|IsShapeshift", "estar transformado", ("shapeshift",)),
]


def carrega(nome):
    caminho = os.path.join(COB, nome)
    if not os.path.isfile(caminho):
        return []
    with open(caminho, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def chaves_do_mod():
    """
    Textos que o mod JA corrige/explica. O censo e o estado ANTES do mod, entao sem
    isto o relatorio acusaria para sempre o que ja esta resolvido. Pega o TEXTO de
    chave de cada entrada das duas tabelas.

    FONTE UNICA: `tools/tabelas.py` (o regex local pulava so o comentario de LINHA
    logo apos o `{` e casava chave fantasma dentro de comentario: 302 no lugar de 298).

    A DIFERENCA DE -4 E GANHO, NAO PERDA DE COBERTURA (conferido pelo PARSER-1R). O regex
    varria o arquivo INTEIRO e colhia 4 chaves de inicializadores FORA dos blocos
    `TextFixes`/`TextAppends` — `Armor increased by 5%`, `Increased Armor`,
    `Elemental resistance reduced by 5% per stack` e `Life Steal`. DUAS delas casam com o
    censo, entao a lista antiga de "ja resolvido pelo mod" tinha 2 casos FALSOS: o parser
    unico le exatamente as 298 entradas de verdade (o regex via 302) e a contagem passou a
    ser MAIS ESTRITA. Nao ha cobertura perdida — so fantasma removido.
    """
    if not os.path.isfile(FONTE_MOD):
        return set()
    with open(FONTE_MOD, encoding="utf-8") as fh:
        return _tab.chaves(fh.read())


def lista(txt):
    return [x.strip() for x in (txt or "").split(";") if x.strip()]


def main():
    filtro = sys.argv[1].lower() if len(sys.argv) > 1 else None
    skills = carrega("skills.csv")
    det = {r["nome"]: r for r in carrega("skills-detalhe.csv")}
    acs = {r["nome"]: r for r in carrega("acoes.csv")}

    usos = Counter()
    faltando = defaultdict(list)   # fonte -> [(arvore, skill, texto)]
    ja_coberto = defaultdict(list)  # fonte -> [(arvore, skill)] que o mod ja resolve
    chaves = chaves_do_mod()
    for r in skills:
        if r["status"] in ("intocavel", "sem-explicacao"):
            continue
        if filtro and r["arvore"].lower() != filtro:
            continue
        d = det.get(r["nome"], {})
        corpo = " ".join([d.get("attr", ""), d.get("expr", ""), d.get("danoExpr", "")])
        for nome_ac in lista(d.get("acts")):
            a = acs.get(nome_ac)
            if a:
                corpo += " " + (a["efeitosRef"] if a["refAcao"].strip() else a["efeitos"])
        if not corpo.strip():
            continue
        texto = r["descricao"].lower()
        for regex, rotulo, palavras in FONTES:
            m = re.search(regex, corpo)
            if not m:
                continue
            nome = rotulo.format(*m.groups()) if "{0}" in rotulo else rotulo
            usos[nome] += 1
            # Só interessa quando a tooltip NÃO diz: ou porque a fonte é "não óbvia"
            # (palavras = None nunca é cobrada, ex. dano padrão) ou porque falta a palavra.
            if palavras is None:
                continue
            if not any(p in texto for p in palavras):
                if r["descricao"] in chaves or r["descricao"].strip() in chaves:
                    ja_coberto[nome].append((r["arvore"], r["nome"]))
                else:
                    faltando[nome].append((r["arvore"], r["nome"], r["descricao"]))

    L = ["# Escala — o que a tooltip não diz (RV-8b-2i)\n",
         "> Gerado por `python tools/check_scaling.py%s`. Le as fórmulas de cada skill e "
         "cruza com as palavras do texto.\n" % ((" " + filtro) if filtro else ""),
         "\n> Desde o PARSER-1 (01/10) a lista \"já resolvido pelo mod\" lê o parser ÚNICO "
         "(`tools/tabelas.py`). O regex antigo varria o arquivo inteiro e colhia 4 chaves "
         "FANTASMA de inicializadores fora dos blocos (302 no lugar de 298); DUAS casavam "
         "com o censo, ou seja a lista antiga tinha 2 casos FALSOS. A contagem caiu para o "
         "número real: é MAIS ESTRITO — ganho, não perda.\n",
         "\n## Fontes de escala encontradas\n",
         "| fonte | skills que usam | precisa estar no texto? |",
         "|---|---:|---|"]
    for nome, n in usos.most_common():
        L.append("| %s | %d | %s |" % (nome, n, "**sim**" if nome in faltando else "—"))

    L.append("\n## O que FALTA no texto (é aqui que vale adicionar)\n")
    if not faltando:
        L.append("Nada: toda skill que escala cobrada pelo critério já diz com o que escala.\n")
    for nome in sorted(faltando, key=lambda k: -len(faltando[k])):
        linhas = faltando[nome]
        L.append("\n### %s — %d skill(s)\n" % (nome, len(linhas)))
        L += ["| arvore | skill | texto |", "|---|---|---|"]
        for arv, sk, txt in linhas:
            L.append("| %s | %s | %s |" % (arv, sk, txt.replace("|", "\\|")[:150]))

    L.append("\n## Já resolvido pelo mod (o censo é o estado ANTES)\n")
    if not ja_coberto:
        L.append("Nada ainda.\n")
    else:
        for nome in sorted(ja_coberto):
            L.append("\n**%s** — %s\n" % (nome, ", ".join("`%s` (%s)" % (s, a)
                                                          for a, s in ja_coberto[nome])))

    with open(SAIDA, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    print("fontes de escala encontradas:")
    for nome, n in usos.most_common():
        print("  %-45s %3d skills" % (nome, n))
    print("\nfaltando no texto:")
    for nome in sorted(faltando, key=lambda k: -len(faltando[k])):
        print("  %-45s %3d skills" % (nome, len(faltando[nome])))
    print("\nrelatorio: %s" % SAIDA)
    return 0


if __name__ == "__main__":
    sys.exit(main())
