#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Auditoria de conteudo das tooltips de SKILL (RV-8b).

Responde, skill por skill, as perguntas que o olho humano esquece de fazer:
  A. a skill causa dano e o texto NAO diz o TIPO de dano?
  B. a skill causa dano e o texto NAO tem valor dinamico (numero fixo/ausente)?
  C. a skill tem efeito em AREA e o texto NAO fala de area?
  D. a descricao e curta/vazia? (candidata a "nao deve ser explicada" - flavor)
  E. familias por FECHO de frase com abertura divergente  (candidata, frouxa)
  E2. familias por NOME com abertura divergente           (precisa - regra da maioria)
  G. placeholder [N] que aponta para uma expressao que NAO EXISTE (RV-8b-0)
     -> so foi possivel depois do dump passar a trazer DescriptionExpressions.
        A gramatica do jogo le UM digito e usa expr[N] (RV-8a); se N passa do
        tamanho do array, o valor sai errado/vazio e o TEXTO PARECE CERTO.

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
# Detalhe mecanico das skills (RV-8b-0): o que o jogo CALCULA. Sem ele nao da para
# conferir se o texto aponta para a expressao certa - so da para ler a prosa.
CSV_DETALHE = os.path.join(RAIZ, "docs", "cobertura", "skills-detalhe.csv")
# As acoes concedidas (RV-8b-0c): a formula de DANO do `*N` mora aqui, nao na skill.
CSV_ACOES = os.path.join(RAIZ, "docs", "cobertura", "acoes.csv")
# Os status (RV-8b-0e): quando o dano da skill vem de um status, e a lista de
# GeneralEffect DELE que o `*N` indexa.
CSV_STATUS = os.path.join(RAIZ, "docs", "cobertura", "status.csv")
SAIDA = os.path.join(RAIZ, "docs", "cobertura", "auditoria-tooltips.md")

PLACEHOLDER = re.compile(r"(\*\d+|\[\d+\]|\{[^}]*\}|@[^@]+@)")
PLACEHOLDER_N = re.compile(r"\[(\d+)\]")
CURTO = 25
AREA = re.compile(r"hex|area|all enemies|within|radius|nearby|around", re.I)
DINAMICO = re.compile(r"\*\d|\[\d")
INTOCAVEIS = {"intocavel", "sem-explicacao"}


def mascara(desc):
    """Troca placeholders por um token, para comparar a REDACAO entre skills."""
    return PLACEHOLDER.sub("~", desc).lower()


def palavras(desc):
    return re.findall(r"[a-z']+", mascara(desc))


def carrega_detalhe():
    """nome -> linha do skills-detalhe.csv (o detalhe mecanico do RV-8b-0)."""
    det = {}
    if not os.path.isfile(CSV_DETALHE):
        return det
    with open(CSV_DETALHE, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            det[r["nome"]] = r
    return det


def n_expressoes(txt):
    """Quantas expressoes o jogo tem para esta skill (o dump junta com '; ')."""
    return len([x for x in (txt or "").split("; ") if x.strip()])


def main():
    filtro = sys.argv[1].lower() if len(sys.argv) > 1 else None
    detalhe = carrega_detalhe()
    linhas = []
    with open(CSV_SKILLS, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["status"] in INTOCAVEIS:
                continue
            if filtro and r["arvore"].lower() != filtro:
                continue
            linhas.append(r)

    a, b, c, d, g = [], [], [], [], []
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

        # G: o texto manda o jogador olhar para expr[N] - esse indice existe?
        det = detalhe.get(nome)
        if det is not None:
            total_expr = n_expressoes(det.get("expr", ""))
            for idx in PLACEHOLDER_N.findall(desc):
                if int(idx) >= total_expr:
                    g.append((arvore, nome, "[" + idx + "]", total_expr, desc))

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

    # H: o `*N` (faixa de dano) indexa `effects[N]`, e `effects` NAO é a skill: é a
    # PRIMEIRA ação concedida (Tooltip l.1443) e, dentro dela, ou o
    # `TooltipDamageInfoRefAction` (l.2222) ou o `TooltipDamageInfoRefStatus` (l.2218).
    # A contagem que vale inclui os GeneralEffect de Action vazio — por isso usa
    # nEfeitos/nEfeitosRef, e não o tamanho da lista de efeitos.
    acoes = {}
    if os.path.isfile(CSV_ACOES):
        with open(CSV_ACOES, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                acoes[r["nome"]] = r
    statuses = {}
    if os.path.isfile(CSV_STATUS):
        with open(CSV_STATUS, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                statuses[r["nome"]] = r
    h, h_nv = [], []
    for r in linhas:
        idxs = [int(x) for x in re.findall(r"\*(\d)", r["descricao"])]
        if not idxs:
            continue
        det = detalhe.get(r["nome"])
        if det is None:
            continue
        # O jogo usa ActionsGranted.FirstOrDefault() — a primeira, nao a melhor de todas.
        acs = [a.strip() for a in (det.get("acts") or "").split(";") if a.strip()]
        if not acs or acs[0] not in acoes:
            continue
        ac = acoes[acs[0]]
        if ac.get("refStatus", "").strip():
            # O dano vem de um STATUS (Tooltip l.2218): a lista e a dos GeneralEffect DELE
            # (RV-8b-0e). Sem o status no censo, nao da para conferir - e ai sim e lacuna.
            st = statuses.get(ac["refStatus"].strip())
            n = int(st.get("nEfeitosDano") or 0) if st else 0
            if n == 0:
                h_nv.append((r["arvore"], r["nome"], ac["refStatus"].strip()))
                continue
        else:
            n = int(ac.get("nEfeitosRef") or 0) if ac.get("refAcao", "").strip() else int(ac.get("nEfeitos") or 0)
        # Os DamageExpressionOverrides da SKILL ESTENDEM a lista de efeitos (Tooltip
        # l.2240-2252): se a skill tem 2 overrides e a acao 1 efeito, `*1` existe.
        n_skill = len([x for x in (det.get("danoExpr") or "").split(";") if x.strip()])
        n = max(n, n_skill)
        if n <= max(idxs):
            h.append((r["arvore"], r["nome"], max(idxs), n, r["descricao"]))

    def tabela(rows, cabecalho):
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
         "| G · placeholder `[N]` apontando para **expressão inexistente** | %d |" % len(g),
         "| H · `*N` (dano) fora do alcance da fórmula | %d |" % len(h),
         "| H · `*N` **não verificável** (dano vem de status — escopo aberto) | %d |" % len(h_nv),
         "\n> Nem todo achado é defeito: D costuma ser skill que **não deve ser explicada**\n"
         "> (flavor) e H-não-verificável é lacuna do CENSO, não do jogo. A auditoria\n"
         "> levanta, a revisão decide.\n"]

    for titulo, rows, cab in (
        ("A · Sem tipo de dano", a, ["arvore", "skill", "dano", "descricao"]),
        ("B · Sem valor dinâmico", b, ["arvore", "skill", "descricao"]),
        ("C · Area sem texto de area", c, ["arvore", "skill", "descricao"]),
        ("D · Descricao curta/vazia", d, ["arvore", "skill", "descricao"]),
        ("G · Placeholder [N] fora do alcance das expressões", g,
         ["arvore", "skill", "placeholder", "expressoes", "descricao"]),
        ("H · Placeholder *N fora do alcance da fórmula de dano", h,
         ["arvore", "skill", "usado", "a_formula_tem", "descricao"]),
        ("H · *N não verificável (dano vem de status)", h_nv,
         ["arvore", "skill", "usado"]),
    ):
        L.append("\n## %s (%d)\n" % (titulo, len(rows)))
        if rows:
            L += tabela(rows, cab)
        else:
            L.append("Nenhum.\n")

    L.append("\n## E2 · Famílias por NOME com abertura divergente (%d)\n" % len(familias_nome))
    L.append("Skills que compartilham a primeira palavra do nome deveriam abrir a descrição do "
             "mesmo jeito. **É aqui que vale a regra do padrão da maioria** — e a maioria "
             "costuma estar no próprio nome:\n")
    for prefixo, aberturas, membros in familias_nome:
        L.append("\n**%s \\*** — aberturas: %s\n" % (prefixo, dict(aberturas)))
        L += tabela([(m["nome"], m["arvore"], m["descricao"]) for m in membros],
                    ["skill", "arvore", "descricao"])

    L.append("\n## E · Famílias por FECHO divergentes — candidatas (%d)\n" % len(variantes))
    L.append("Mesmo fecho de frase, abertura diferente. Lista frouxa de propósito: quase "
             "tudo aqui são templates diferentes que por acaso terminam igual.\n")
    for fecho, aberturas, membros in variantes:
        L.append("\n**…%s** — aberturas: %s\n" % (" ".join(fecho), dict(aberturas)))
        L += tabela([(m["nome"], m["arvore"], m["descricao"]) for m in membros],
                    ["skill", "arvore", "descricao"])

    with open(SAIDA, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    print("skills auditadas: %d" % len(linhas))
    print("  A  sem tipo de dano : %d" % len(a))
    print("  B  sem valor dinamico: %d" % len(b))
    print("  C  area sem texto   : %d" % len(c))
    print("  D  curta/vazia      : %d" % len(d))
    print("  E2 familias por nome divergentes: %d" % len(familias_nome))
    print("  E  familias por fecho (candidatas): %d" % len(variantes))
    print("  G  placeholder [N] fora do alcance: %d" % len(g))
    print("  H  *N fora do alcance da formula: %d" % len(h))
    print("  H  *N nao verificavel (via status): %d" % len(h_nv))
    print("relatorio: %s" % SAIDA)
    return 0


if __name__ == "__main__":
    sys.exit(main())
