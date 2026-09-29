#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RV-7 - Censo de tooltips do Stolen Realm.

Le o dump de boot do RoguelikeDebugger (LogOutput.log) e gera um checklist
CSV por categoria em docs/cobertura/. Cada linha = uma tooltip a revisar,
com coluna `status` para o trabalho de revisao (RV-8..RV-12).

RV-8b-0: as skills ganharam um arquivo COMPANHEIRO (skills-detalhe.csv) com o que o
jogo CALCULA - ActionsGranted, AttributeEffects, PassiveActionStatuses, as
DescriptionExpressions (o array que o [N] do texto indexa em runtime), os overrides de
dano e o UpgradeText. Fica separado para a checklist principal nao virar planilha
ilegivel; e ali que se confere se os NUMEROS escritos na tooltip batem com a mecanica.

Uso:
    python tools/census.py                       # le o LogOutput.log do perfil
    python tools/census.py <caminho-do-log>
"""
import csv
import os
import re
import sys

def _appdata():
    """APPDATA do Windows, com fallback para ~/AppData/Roaming."""
    return os.environ.get("APPDATA") or os.path.join(
        os.path.expanduser("~"), "AppData", "Roaming")

DEFAULT_LOG = os.path.join(
    _appdata(), "r2modmanPlus-local", "StolenRealm", "profiles", "Default",
    "BepInEx", "LogOutput.log")
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "docs", "cobertura")

# [Info   :Roguelike Debugger] [Skill] 'Verse of Valor' | tipo=Bard | dano=None | tier=1 |
# tags=... | skid=... | passivo=nao | attr=... | acts=... | pstat=... | expr=... |
# danoExpr=... | upg=... | desc="..."
# ATENCAO ao mexer no dump: os campos vem separados por "|" e nenhum valor pode conter
# "|", e o desc= precisa continuar por ULTIMO (o regex DESC e ancorado no fim da linha).
LINE = re.compile(
    r"^\[[^\]]*:Roguelike Debugger\]\s+\[(?P<cat>Skill|Status|ItemMod|Item|Powerup)\]\s+"
    r"'(?P<name>.*?)'\s+\|\s*(?P<rest>.*)$"
)
FIELD = re.compile(
    r"(?P<key>tipo|dano|tier|tags|raridade|lvlMin|guid|nivel|custo|efeitos"
    r"|skid|passivo|attr|acts|pstat|expr|danoExpr|upg)=(?P<val>[^|]+)")
DESC = re.compile(r'desc="(?P<desc>.*)"\s*$')
VALOR = re.compile(r":(-?\d+(?:\.\d+)?)\s*,")

# Colunas do arquivo companheiro das skills (RV-8b-0).
DETALHE = "skills-detalhe.csv"
DETALHE_HEADER = ["nome", "skid", "passivo", "acts", "pstat", "attr",
                  "expr", "danoExpr", "upg"]


def classe_status(efeitos, desc):
    """
    Pista (nao verdade) de debuff/buff, para o RV-9 poder revisar debuffs primeiro.
    Usa o SINAL dos efeitos de atributo; se nao houver numero, cai na redacao da
    descricao. O revisor corrige a coluna se a heuristica errar.
    """
    valores = VALOR.findall(efeitos or "")
    neg = any(v.startswith("-") for v in valores)
    pos = any(not v.startswith("-") and float(v) != 0 for v in valores)
    if neg and not pos:
        return "debuff"
    if pos and not neg:
        return "buff"
    d = (desc or "").lower()
    if re.search(r"reduc|decreas|lower|weaken|penalt|no longer|prevent", d):
        return "debuff"
    if re.search(r"increas|gain|higher|bonus|extra", d):
        return "buff"
    return "indefinido"


CATS = {
    "Skill":   ("skills.csv",   ["nome", "arvore", "tier", "dano", "tags", "passivo",
                                 "attr", "descricao", "status"]),
    "Status":  ("status.csv",   ["nome", "tipo", "raridade", "efeitos", "classe", "descricao", "status"]),
    "Item":    ("itens.csv",    ["nome", "tipo", "raridade", "lvlMin", "descricao", "status"]),
    "ItemMod": ("afixos.csv",   ["nome", "tipo", "raridade", "descricao", "status"]),
    "Powerup": ("powerups.csv", ["nome", "guid", "nivel", "custo", "efeitos", "descricao", "status"]),
}


def escreve_detalhe(rows):
    """Arquivo companheiro: o detalhe mecanico das skills (RV-8b-0)."""
    out = os.path.join(OUT_DIR, DETALHE)
    vistos = set()
    with open(out, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(DETALHE_HEADER)
        for nome, f, _desc in sorted(rows["Skill"], key=lambda r: r[0].lower()):
            chave = (nome, f.get("skid", ""))
            if chave in vistos:
                continue
            vistos.add(chave)
            w.writerow([nome, f.get("skid", ""), f.get("passivo", ""), f.get("acts", ""),
                        f.get("pstat", ""), f.get("attr", ""), f.get("expr", ""),
                        f.get("danoExpr", ""), f.get("upg", "")])
    return len(vistos)


def parse(path):
    rows = {c: [] for c in CATS}
    truncadas = 0
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for raw in fh:
            line = raw.rstrip("\r\n")
            m = LINE.match(line.strip() if line.startswith("[Info") else line)
            if not m:
                continue
            cat = m.group("cat")
            rest = m.group("rest")
            fields = {k: v.strip() for k, v in FIELD.findall(rest)}
            dm = DESC.search(rest)
            desc = dm.group("desc") if dm else ""
            if not dm:
                truncadas += 1   # descricao cortada pelo debugger
            rows[cat].append((m.group("name"), fields, desc))

    os.makedirs(OUT_DIR, exist_ok=True)
    resumo = []

    n_det = escreve_detalhe(rows)
    resumo.append(("detalhe-skill", n_det, n_det, DETALHE))

    for cat, (fname, header) in CATS.items():
        items = rows[cat]
        # Dedup por (nome + descricao): o dump pode repetir entradas.
        vistos = set()
        unicos = []
        for nome, fields, desc in items:
            chave = (nome, desc)
            if chave in vistos:
                continue
            vistos.add(chave)
            unicos.append((nome, fields, desc))

        out = os.path.join(OUT_DIR, fname)

        # O CSV e GERADO, mas a coluna `status` e preenchida a mao (RV-8..RV-12).
        # Regenerar sem carregar o anterior apagaria todo o trabalho de revisao.
        anterior = {}
        if os.path.isfile(out):
            with open(out, encoding="utf-8") as fh:
                for r in csv.DictReader(fh):
                    if r.get("status"):
                        anterior[(r.get("nome", ""), r.get("nivel", ""))] = r["status"]

        with open(out, "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(header)
            for nome, f, desc in sorted(
                    unicos,
                    key=lambda r: (r[0].lower(),
                                   int(r[1]["nivel"]) if r[1].get("nivel", "").isdigit() else 0)):
                st = anterior.get((nome, f.get("nivel", "")))
                if cat == "Skill":
                    padrao = "intocavel" if f.get("tipo", "").lower() == "bard" else "pendente"
                    w.writerow([nome, f.get("tipo", ""), f.get("tier", ""), f.get("dano", ""),
                                f.get("tags", ""), f.get("passivo", ""), f.get("attr", ""),
                                desc, st or padrao])
                elif cat == "Status":
                    w.writerow([nome, f.get("tipo", ""), f.get("raridade", ""),
                                f.get("efeitos", "").strip().rstrip(","),
                                classe_status(f.get("efeitos", ""), desc), desc,
                                st or "pendente"])
                elif cat == "Item":
                    w.writerow([nome, f.get("tipo", ""), f.get("raridade", ""),
                                f.get("lvlMin", ""), desc, st or "pendente"])
                elif cat == "ItemMod":
                    w.writerow([nome, f.get("tipo", ""), f.get("raridade", ""), desc,
                                st or "pendente"])
                else:  # Powerup: uma linha por nivel, porque o tooltip e por nivel
                    w.writerow([nome, f.get("guid", ""), f.get("nivel", ""), f.get("custo", ""),
                                f.get("efeitos", "").strip().rstrip(","), desc,
                                st or "pendente"])
        resumo.append((cat, len(items), len(unicos), fname))
    return resumo, truncadas


def main():
    log = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_LOG
    if not os.path.isfile(log):
        print("Log nao encontrado: %s" % log)
        return 1
    resumo, truncadas = parse(log)
    print("Censo gerado em %s\n" % OUT_DIR)
    print("%-14s %10s %10s  %s" % ("categoria", "linhas", "unicos", "arquivo"))
    for cat, total, unicos, fname in resumo:
        print("%-14s %10d %10d  %s" % (cat, total, unicos, fname))
    if truncadas:
        print("\nAVISO: %d entradas com descricao cortada no log (o debugger limita o "
              "tamanho). O nome/tipo/tier continuam validos; a descricao completa tera "
              "de ser lida no jogo ou no asset." % truncadas)
    return 0


if __name__ == "__main__":
    sys.exit(main())
