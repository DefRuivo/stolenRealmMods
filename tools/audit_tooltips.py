#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Auditoria de conteudo das tooltips de SKILL (RV-8b).

Responde, skill por skill, as perguntas que o olho humano esquece de fazer:
  A. a skill causa dano e o texto NAO diz o TIPO de dano?
  B. a skill causa dano e o texto NAO tem valor dinamico (numero fixo/ausente)?
  C. a skill tem efeito em AREA e o texto NAO fala de area?
  D. a descricao e curta/vazia? (candidata a "nao deve ser explicada" - flavor)
  E. familias de redacao: descricoes com o mesmo fecho divergem na abertura?
     (e o que pega "Summona skeletal..." vs "Raise an Undead..." - o padrao
      deve seguir a MAIORIA, e a maioria costuma estar no proprio nome da skill)

Uso:   python tools/audit_tooltips.py [arvore]      (sem arvore = todas)
Saida: docs/cobertura/auditoria-tooltips.md
"""
import csv
import os
import re
import sys
from collections import Counter, defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_SKILLS = os.path.join(RAIZ, "docs", "cobertura", "skills.csv")
SAIDA = os.path.join(RAIZ, "docs", "cobertura", "auditoria-tooltips.md")

PLACEHOLDER = re.compile(r"(\*\d+|\[\d+\]|\{[^}]*\}|@[^@]+@)")
CURTO = 25
AREA = re.compile(r"hex|area|all enemies|within|radius|nearby|around", re.I)
DINAMICO = re.compile(r"\*\d|\[\d")
INTOCAVEIS = {"intocavel", "sem-explicacao"}


def mascara(desc):
    """Troca placeholders por um token, para comparar a REDACAO entre skills."""
    return PLACEHOLDER.sub("~", desc).lower()


def palavras(desc):
    return re.findall(r"[a-z']+", mascara(desc))


def main():
    filtro = sys.argv[1].lower() if len(sys.argv) > 1 else None
    linhas = []
    with open(CSV_SKILLS, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["status"] in INTOCAVEIS:
                continue
            if filtro and r["arvore"].lower() != filtro:
                continue
            linhas.append(r)

    a, b, c, d = [], [], [], []
    por_arvore = defaultdict(list)
    for r in linhas:
        nome, arvore, tags = r["nome"], r["arvore"], r["tags"]
        dano, desc = r["dano"], r["descricao"].strip()
        tg = set(tags.split(",")) if tags else set()
        tgt = tags.lower()
        por_arvore[arvore].append(r)

        if "DealsDamage" in tgt:
            # A: tipo de dano citado? (o texto pode usar @Shadow Damage@ ou o nome cru)
            alvo = dano.lower()
            if alvo and alvo != "none" and alvo not in desc.lower().replace("@", ""):
                a.append((arvore, nome, dano, desc))
            # B: valor dinamico presente?
            if not DINAMICO.search(desc):
                b.append((arvore, nome, desc))

        if "AreaEffect" in tgt and not AREA.search(desc):
            c.append((arvore, nome, desc))

        if len(desc) < CURTO:
            d.append((arvore, nome, desc))

    # E2 (precisa): familias pelo NOME - skills que compartilham a primeira palavra do
    # nome (Raise *, Leech *, Thirst *) devem abrir a descricao do mesmo jeito.
    # E aqui que a regra do "padrao da maioria" morde: a maioria costuma estar no nome.
    nomes = defaultdict(list)
    for r in linhas:
        nomes[r["nome"].split()[0]].append(r)
    familias_nome = []
    for prefixo, membros in sorted(nomes.items()):
        if len(membros) < 3:
            continue
        aberturas = Counter(palavras(m["descricao"])[0] if palavras(m["descricao"]) else "~"
                            for m in membros)
        if len(aberturas) > 1:
            # Filtro que tira o ruido: so interessa quando a palavra do nome e um VERBO
            # que alguma descricao ecoa (ex.: "Raise *" -> descricoes comecando com
            # "raise"). Nome que compartilha so um substantivo ("Aura *", "Fire *")
            # junta skills sem relacao nenhuma.
            if prefixo.lower() in aberturas:
                familias_nome.append((prefixo, aberturas, membros))

    # E (candidata): mesmo fecho de frase, abertura divergente. Frouxa de proposito -
    # grupos com muita variedade sao templates DIFERENTES que so terminam parecido.
    familias = defaultdict(list)
    for r in linhas:
        p = palavras(r["descricao"])
        if len(p) >= 3:
            familias[tuple(p[-2:])].append(r)
    variantes = []
    for fecho, membros in familias.items():
        if len(membros) < 3:
            continue
        aberturas = Counter(palavras(m["descricao"])[0] for m in membros)
        if len(aberturas) > 1:
            variantes.append((fecho, aberturas, membros))

    def tabela(rows, cols, cabecalho):
        out = ["| %s |" % " | ".join(cabecalho), "|" + "---|" * len(cabecalho)]
        for r in rows:
            out.append("| " + " | ".join(str(x).replace("|", "\\|")[:110] for x in r) + " |")
        return out

    L = ["# Auditoria de conteudo das tooltips de skill (RV-8b)\n",
         "> `python tools/audit_tooltips.py%s` — %d skills, Bard e demais intocaveis fora.\n"
         % ((" " + filtro) if filtro else "", len(linhas)),
         "\n| checagem | achados |", "|---|---:|",
         "| A · causa dano e não diz o **tipo** de dano | %d |" % len(a),
         "| B · causa dano e não tem **valor dinâmico** | %d |" % len(b),
         "| C · efeito em **área** sem menção de área no texto | %d |" % len(c),
         "| D · descrição **curta/vazia** (candidata a flavor) | %d |" % len(d),
         "| E2 · famílias por **nome** com abertura divergente (precisa) | %d |" % len(familias_nome),
         "| E · famílias por **fecho** com abertura divergente (candidatas) | %d |" % len(variantes),
         "\n> Nem todo achado é defeito: D costuma ser skill que **não deve ser explicada**\n"
         "> (flavor) e A/B podem ser texto gerado por expressão. A auditoria levanta, a\n"
         "> revisão decide.\n"]

    for titulo, rows, cols, cab in (
        ("A · Sem tipo de dano", a, None, ["arvore", "skill", "dano", "descricao"]),
        ("B · Sem valor dinâmico", b, None, ["arvore", "skill", "descricao"]),
        ("C · Area sem texto de area", c, None, ["arvore", "skill", "descricao"]),
        ("D · Descricao curta/vazia", d, None, ["arvore", "skill", "descricao"]),
    ):
        L.append("\n## %s (%d)\n" % (titulo, len(rows)))
        if rows:
            L += tabela(rows, cols, cab)
        else:
            L.append("Nenhum.\n")

    L.append("\n## E2 · Famílias por NOME com abertura divergente (%d)\n" % len(familias_nome))
    L.append("Skills que compartilham a primeira palavra do nome deveriam abrir a descrição do "
             "mesmo jeito. **É aqui que vale a regra do padrão da maioria** — e a maioria "
             "costuma estar no próprio nome:\n")
    for prefixo, aberturas, membros in familias_nome:
        L.append("\n**%s \\*** — aberturas: %s\n" % (prefixo, dict(aberturas)))
        L += tabela([(m["nome"], m["arvore"], m["descricao"]) for m in membros], None,
                    ["skill", "arvore", "descricao"])

    L.append("\n## E · Famílias por FECHO divergentes — candidatas (%d)\n" % len(variantes))
    L.append("Mesmo fecho de frase, abertura diferente — é aqui que se aplica a regra "
             "do **padrão da maioria** (a maioria costuma estar no próprio nome da skill):\n")
    for fecho, aberturas, membros in variantes:
        L.append("\n**…%s** — aberturas: %s\n" % (" ".join(fecho), dict(aberturas)))
        L += tabela([(m["nome"], m["arvore"], m["descricao"]) for m in membros], None,
                    ["skill", "arvore", "descricao"])

    with open(SAIDA, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    print("skills auditadas: %d" % len(linhas))
    print("  A sem tipo de dano : %d" % len(a))
    print("  B sem valor dinamico: %d" % len(b))
    print("  C area sem texto   : %d" % len(c))
    print("  D curta/vazia      : %d" % len(d))
    print("  E2 familias por nome divergentes: %d" % len(familias_nome))
    print("  E  familias por fecho (candidatas): %d" % len(variantes))
    print("relatorio: %s" % SAIDA)
    return 0


if __name__ == "__main__":
    sys.exit(main())
