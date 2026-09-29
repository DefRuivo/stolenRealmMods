#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RV-7 - Censo de tooltips do Stolen Realm.

Le o dump de boot do RoguelikeDebugger (LogOutput.log) e gera um checklist
CSV por categoria em docs/cobertura/. Cada linha = uma tooltip a revisar,
com coluna `status` para o trabalho de revisao (RV-8..RV-12).

Uso:
    python tools/census.py                       # le o LogOutput.log do perfil
    python tools/census.py <caminho-do-log>
"""
import csv
import os
import re
import sys

DEFAULT_LOG = (
    r"%USERPROFILE%\AppData\Roaming\r2modmanPlus-local\StolenRealm"
    r"\profiles\Default\BepInEx\LogOutput.log"
)
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "docs", "cobertura")

# [Info   :Roguelike Debugger] [Skill] 'Verse of Valor' | tipo=Bard | dano=None | tier=1 | tags=... | desc="..."
LINE = re.compile(
    r"^\[[^\]]*:Roguelike Debugger\]\s+\[(?P<cat>Skill|Status|ItemMod|Item|Powerup)\]\s+"
    r"'(?P<name>.*?)'\s+\|\s*(?P<rest>.*)$"
)
FIELD = re.compile(
    r"(?P<key>tipo|dano|tier|tags|raridade|lvlMin|guid|nivel|custo|efeitos)=(?P<val>[^|]+)")
DESC = re.compile(r'desc="(?P<desc>.*)"\s*$')
VALOR = re.compile(r":(-?\d+(?:\.\d+)?)\s*,")


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
    "Skill":   ("skills.csv",   ["nome", "arvore", "tier", "dano", "tags", "descricao", "status"]),
    "Status":  ("status.csv",   ["nome", "tipo", "raridade", "efeitos", "classe", "descricao", "status"]),
    "Item":    ("itens.csv",    ["nome", "tipo", "raridade", "lvlMin", "descricao", "status"]),
    "ItemMod": ("afixos.csv",   ["nome", "tipo", "raridade", "descricao", "status"]),
    "Powerup": ("powerups.csv", ["nome", "guid", "nivel", "custo", "efeitos", "descricao", "status"]),
}


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
        with open(out, "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(header)
            for nome, f, desc in sorted(
                    unicos,
                    key=lambda r: (r[0].lower(),
                                   int(r[1]["nivel"]) if r[1].get("nivel", "").isdigit() else 0)):
                if cat == "Skill":
                    status = "intocavel" if f.get("tipo", "").lower() == "bard" else "pendente"
                    w.writerow([nome, f.get("tipo", ""), f.get("tier", ""), f.get("dano", ""),
                                f.get("tags", ""), desc, status])
                elif cat == "Status":
                    w.writerow([nome, f.get("tipo", ""), f.get("raridade", ""),
                                f.get("efeitos", "").strip().rstrip(","),
                                classe_status(f.get("efeitos", ""), desc), desc, "pendente"])
                elif cat == "Item":
                    w.writerow([nome, f.get("tipo", ""), f.get("raridade", ""),
                                f.get("lvlMin", ""), desc, "pendente"])
                elif cat == "ItemMod":
                    w.writerow([nome, f.get("tipo", ""), f.get("raridade", ""), desc, "pendente"])
                else:  # Powerup: uma linha por nivel, porque o tooltip e por nivel
                    w.writerow([nome, f.get("guid", ""), f.get("nivel", ""), f.get("custo", ""),
                                f.get("efeitos", "").strip().rstrip(","), desc, "pendente"])
        resumo.append((cat, len(items), len(unicos), fname))
    return resumo, truncadas


def main():
    log = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_LOG
    if not os.path.isfile(log):
        print("Log nao encontrado: %s" % log)
        return 1
    resumo, truncadas = parse(log)
    print("Censo gerado em %s\n" % OUT_DIR)
    print("%-10s %10s %10s  %s" % ("categoria", "linhas", "unicos", "arquivo"))
    for cat, total, unicos, fname in resumo:
        print("%-10s %10d %10d  %s" % (cat, total, unicos, fname))
    if truncadas:
        print("\nAVISO: %d entradas com descricao cortada no log (o debugger limita o "
              "tamanho). O nome/tipo/tier continuam validos; a descricao completa tera "
              "de ser lida no jogo ou no asset." % truncadas)
    return 0


if __name__ == "__main__":
    sys.exit(main())
