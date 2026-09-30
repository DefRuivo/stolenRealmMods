#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Analisa os itens "conferir" de uma arvore: o que o texto AFIRMA e o codigo tem?

Le a ficha gerada por tools/verify_tree.py (docs/cobertura/revisao/ficha-<arvore>.md),
pega as linhas `**conferir:** ... sem par no codigo dumpado` e, para cada skill, imprime
tudo que o codigo diz sobre aquele numero: os efeitos de atributo da skill, as expressoes,
as ACOES que ela concede (com os efeitos e a acao referenciada), os GATILHOS (tipo,
condicao, status que aplicam) e os STATUS aplicados (com efeitos e efeitosDano).

E o que fecha um item "sem par": o numero costuma estar em algum lugar que a bancada do
verify_tree nao olha (efeito de acao, status aplicado, gatilho).

Uso: python tools/analisa_conferir.py <arvore>
"""
import csv
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COB = os.path.join(RAIZ, "docs", "cobertura")
LOG = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")),
                   "r2modmanPlus-local", "StolenRealm", "profiles", "Default",
                   "BepInEx", "LogOutput.log")


def carrega(nome):
    caminho = os.path.join(COB, nome)
    if not os.path.isfile(caminho):
        return []
    with open(caminho, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def campo(linha, nome):
    m = re.search(re.escape(nome) + r"=([^|]*)", linha)
    return m.group(1).strip() if m else ""


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    arvore = sys.argv[1].lower()
    ficha = os.path.join(COB, "revisao", "ficha-%s.md" % arvore)
    if not os.path.isfile(ficha):
        print("sem ficha: rode python tools/verify_tree.py %s" % arvore)
        return 1

    # Quais skills tem item a conferir
    alvos = {}
    atual = None
    for l in io.open(ficha, encoding="utf-8"):
        m = re.match(r"^## (.+?)\s*$", l)
        if m:
            # O cabecalho traz o tier colado ("T1 Call of the Grave"), o censo nao.
            atual = re.sub(r"^T\d+\s+", "", m.group(1).split(" · ")[0].strip())
        if l.startswith("**conferir:**") and "sem par" in l:
            alvos.setdefault(atual, l.split("**conferir:**")[1].strip())

    sk = {r["nome"]: r for r in carrega("skills.csv")}
    det = {r["nome"]: r for r in carrega("skills-detalhe.csv")}
    acs = {r["nome"]: r for r in carrega("acoes.csv")}
    stt = {r["nome"]: r for r in carrega("status.csv")}

    props, trig = {}, {}
    if os.path.isfile(LOG):
        for l in io.open(LOG, encoding="utf-8", errors="replace"):
            m = re.search(r"\[ActionProps\] '([^']+)'", l)
            if m:
                props[m.group(1)] = l
            m = re.search(r"\[Trigger\] '([^']+)'", l)
            if m:
                trig.setdefault(m.group(1), []).append(l.split("] ", 2)[-1].strip())

    print("arvore %s: %d skills a conferir\n" % (arvore, len(alvos)))
    for nome, oque in alvos.items():
        r = sk.get(nome, {})
        d = det.get(nome, {})
        print("=" * 78)
        print("%s   [conferir: %s]" % (nome, oque))
        print("  texto   : %s" % (r.get("descricao") or "?")[:150])
        print("  attr    : %s" % (d.get("attr") or "(vazio)")[:150])
        if d.get("expr"):
            print("  expr    : %s" % d["expr"][:130])
        if d.get("danoExpr"):
            print("  danoExpr: %s" % d["danoExpr"][:130])
        if d.get("upg"):
            print("  upg     : %s" % d["upg"][:120])
        for t in trig.get(nome, []):
            print("  gatilho : %s" % t[:175])
        for ac in [x.strip() for x in (d.get("acts") or "").split(";") if x.strip()]:
            a = acs.get(ac)
            p = props.get(ac)
            if a:
                print("  acao %s: nEfeitos=%s | efeitos=%s" % (ac, a.get("nEfeitos"), (a.get("efeitos") or "")[:110]))
                if a.get("refAcao") or a.get("efeitosRef"):
                    print("           ref=%s | efeitosRef=%s" % (a.get("refAcao"), (a.get("efeitosRef") or "")[:100]))
                if a.get("refStatus"):
                    print("           refStatus=%s" % a.get("refStatus"))
            if p:
                sts = [x for x in campo(p, "statusAplicados").split(",") if x.strip()]
                if sts:
                    print("           aplica   : %s" % ", ".join(sts))
                if campo(p, "cond") not in ("", "-"):
                    print("           cond     : %s" % campo(p, "cond")[:80])
                for st in sts:
                    s = stt.get(st)
                    if s:
                        print("             %s -> efeitos=%s | efeitosDano=%s"
                              % (st, (s.get("efeitos") or "")[:70], (s.get("efeitosDano") or "")[:70]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
