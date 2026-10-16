"""Auditoria automática offline do EV-R2-NORMAL-b01-parte02 (cobertura, identidade, caminhos, literais, contagens).

Checa: integridade das fontes, cobertura/identidade dos 20 registros, caminhos JSONPath,
literais antes→depois contra a fonte, contagens/vereditos e coerência md<->json.
Uso: python b01_audit.py [--md]
Somente leitura das fontes; escreve apenas artefatos do lote.
"""
import json, os, sys, hashlib, re
from collections import Counter

SRC = "C:/dev/stolen-realm/docs/cobertura/EV-R1"
DEST = "C:/dev/stolen-realm/docs/automacao"
BASE = os.path.dirname(os.path.abspath(__file__))
MD = os.path.join(DEST, "EV-R2-NORMAL-b01-parte02.md")
VAL = os.path.join(BASE, "EV-R2-NORMAL-b01-parte02-validacao.json")
PARTE01 = os.path.join(DEST, "EV-R2-NORMAL-b01-parte01.md")

BASE_SHA = {
    "eventos.json": "4a8decac7e98a2b0bf8692057a57789a71b94c230e3b9ca93817f039c86d1d13",
    "lote-Normal-v2.md": "83b30ada3d78e596b8c7c0784d5e741b43654b14ab02d5377d8a1b245b84f146",
    "eventos.schema.json": "6950ec43deba94143150f0584bb87ca5406b3ef16f1ae2f18ad8aa943a62b3bc",
    "catalogo-referencias.json": "94077cc887621933abe7bbbbd96e91c5a887478dba8fd000b8f4a4129c3745a5",
}
PARTE01_SHA = "e65daa3413e18adc1d73b6272d936f8d7d593da83e90abfbb06c34f6aee530e9"

PASS, FAIL = [], []


def ck(name, cond, detail=""):
    (PASS if cond else FAIL).append(f"{name}{(' :: ' + detail) if detail else ''}")
    print(("PASS " if cond else "FAIL ") + name + ((" :: " + detail) if detail else ""))


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def resolve(obj, path):
    """Resolve $.a.b[0].c -> (ok, valor)."""
    if not path.startswith("$"):
        return False, None
    toks = re.findall(r"\.([A-Za-z_][A-Za-z0-9_]*)|\[(\d+)\]", path[1:])
    cur = obj
    for key, idx in toks:
        if key:
            if not isinstance(cur, dict) or key not in cur:
                return False, None
            cur = cur[key]
        else:
            if not isinstance(cur, list) or int(idx) >= len(cur):
                return False, None
            cur = cur[int(idx)]
    return True, cur


def load_normal():
    with open(os.path.join(SRC, "eventos.json"), encoding="utf-8") as f:
        ev = json.load(f)["eventos"]
    return [e for e in ev if e.get("categoria") == "Normal"]


def facts(normal20, all_normal):
    F = {}
    F["total_normal"] = len(all_normal)
    F["disabled"] = [i for i, e in enumerate(normal20, 1) if (e["condicoes"] or {}).get("disabled") == 1]
    F["editor_only"] = [i for i, e in enumerate(normal20, 1) if (e["condicoes"] or {}).get("EditorOnly") == 1]
    F["texto_vazio"] = [i for i, e in enumerate(normal20, 1) if (e.get("texto") or "") == ""]
    F["texto_ghost"] = [i for i, e in enumerate(normal20, 1)
                        if (e.get("texto") or "") == "The yearning ghost extends her hand pleading for help."]
    opt_total = sum(len(e.get("opcoes") or []) for e in normal20)
    opt_empty_texto = sum(1 for e in normal20 for o in (e.get("opcoes") or []) if (o.get("texto") or "") == "")
    slot_total = opt_total
    slot_bonus_empty = sum(1 for e in normal20 for o in (e.get("opcoes") or [])
                           if not ((o.get("rolagem") or {}).get("bonus") or []))
    F["opcoes_total"] = opt_total
    F["opcoes_texto_vazio"] = opt_empty_texto
    F["slots_bonus_vazio"] = slot_bonus_empty
    F["bonus_nao_vazio"] = sorted({i for i, e in enumerate(normal20, 1) for o in (e.get("opcoes") or [])
                                   if ((o.get("rolagem") or {}).get("bonus") or [])})
    F["batalha_iniciar_true"] = sorted({i for i, e in enumerate(normal20, 1) for o in (e.get("opcoes") or [])
                                        for a in (o.get("efeitos") or []) if (a.get("batalha") or {}).get("iniciar") is True})
    F["drf_null_com_batalha"] = sorted({i for i, e in enumerate(normal20, 1) for o in (e.get("opcoes") or [])
                                        for a in (o.get("efeitos") or []) if (a.get("batalha") or {}).get("dados_recompensa_final", "x") is None})
    ids = Counter(e["id"] for e in normal20)
    F["ids_duplicados"] = {k: v for k, v in ids.items() if v > 1}
    F["ids_unicos"] = len(set(e["id"] for e in normal20))
    F["chaves_unicas"] = len(set(e["chave"] for e in normal20))
    tit = Counter(e["titulo"] for e in normal20)
    F["titulos_repetidos"] = {k: v for k, v in tit.items() if v > 1}
    F["raridades"] = dict(Counter(e["raridade"]["nome"] for e in normal20))
    F["pesos"] = {str(k): v for k, v in Counter(e["peso"] for e in normal20).items()}
    F["typos_originais"] = {i: [w for w in ["appeares", "whisperes"] if w in (e.get("texto") or "")]
                            for i, e in enumerate(normal20, 1)}
    F["typos_originais"] = {k: v for k, v in F["typos_originais"].items() if v}
    # PPtr nulo chave/nome: sempre presente? conta eventos com pelo menos um ref nulo
    def has_null_pptr(o):
        if isinstance(o, dict):
            if o.get("chave") is None and o.get("nome") is None and "motivo" in o:
                return True
            return any(has_null_pptr(v) for v in o.values())
        if isinstance(o, list):
            return any(has_null_pptr(v) for v in o)
        return False
    F["eventos_com_pptr_nulo"] = [i for i, e in enumerate(normal20, 1) if has_null_pptr(e)]
    return F


def main():
    normal = load_normal()
    n20 = normal[:20]
    val = json.load(open(VAL, encoding="utf-8"))

    print("== 1. Integridade das fontes ==")
    for f_, h in BASE_SHA.items():
        ck(f"sha256 {f_}", sha(os.path.join(SRC, f_)) == h, sha(os.path.join(SRC, f_)))
    ck("parte01 (proposta reprovada) inalterada", sha(PARTE01) == PARTE01_SHA, sha(PARTE01))
    ck("parte02 não sobrescreve parte01", os.path.exists(PARTE01))

    print("== 2. Cobertura e identidade (20/20, ordem do JSON categoria Normal) ==")
    recs = val["registros"]
    ck("20 registros", len(recs) == 20, str(len(recs)))
    ck("ordinais 1..20 únicos", sorted(r["ordinal"] for r in recs) == list(range(1, 21)))
    ident_bad = []
    for r, e in zip(recs, n20):
        for kf, ke in [("chave", "chave"), ("id", "id"), ("titulo", "titulo"), ("categoria", "categoria"),
                       ("peso", "peso")]:
            if r[kf] != e[ke]:
                ident_bad.append((r["ordinal"], kf, r[kf], e[ke]))
        if r["raridade"]["nome"] != e["raridade"]["nome"] or r["raridade"]["valor"] != e["raridade"]["valor"]:
            ident_bad.append((r["ordinal"], "raridade", r["raridade"], e["raridade"]))
    ck("chave/id/título/categoria/raridade/peso conferem com a fonte", not ident_bad, str(ident_bad))
    ck("ordem posicional = ordem do JSON Normal (1..20)",
       [r["chave"] for r in recs] == [e["chave"] for e in n20])

    print("== 3. Caminhos JSONPath e literais antes->depois ==")
    path_bad, lit_bad = [], []
    for r, e in zip(recs, n20):
        for p in r["propostas"]:
            ok, v = resolve(e, p["path"])
            if not ok:
                path_bad.append((r["ordinal"], p["code"], p["path"]))
                continue
            if p["tipo"] == "CAMPO":
                if v != p["antes"]:
                    lit_bad.append((r["ordinal"], p["code"], "CAMPO divergente", repr(v), repr(p["antes"])))
            else:
                if not isinstance(v, str) or p["antes"] not in v:
                    lit_bad.append((r["ordinal"], p["code"], "TRECHO ausente", repr(v)[:80], repr(p["antes"])))
            if p["antes"] == p["depois"]:
                lit_bad.append((r["ordinal"], p["code"], "antes==depois", "", ""))
    ck("todos os JSONPath resolvem na fonte", not path_bad, str(path_bad))
    ck("todos os literais 'antes' batem na fonte e depois difere", not lit_bad, str(lit_bad[:5]))
    ck("20 registros com veredito e justificativa",
       all(r["veredito"] in ("MANTER", "MELHORAR") and r["justificativa"] for r in recs))
    ck("MELHORAR tem natureza e >=1 proposta exata",
       all(r["natureza"] != "—" and r["propostas"] for r in recs if r["veredito"] == "MELHORAR"))
    ck("MANTER não propõe alteração", all(not r["propostas"] for r in recs if r["veredito"] == "MANTER"))

    print("== 4. Vereditos e contagens ==")
    manter = [r["ordinal"] for r in recs if r["veredito"] == "MANTER"]
    melhorar = [r["ordinal"] for r in recs if r["veredito"] == "MELHORAR"]
    ck("MANTER = 7 (#5,11,12,15,16,17,18)", manter == [5, 11, 12, 15, 16, 17, 18], str(manter))
    ck("MELHORAR = 13 (restantes)", melhorar == [1, 2, 3, 4, 6, 7, 8, 9, 10, 13, 14, 19, 20], str(melhorar))
    F = facts(n20, normal)
    ck("fonte: 160 eventos categoria Normal, faixa = primeiros 20", F["total_normal"] == 160)
    ck("fonte: disabled = %s" % F["disabled"], F["disabled"] == [1, 4, 8, 10, 14])
    ck("fonte: texto vazio = %s" % F["texto_vazio"], F["texto_vazio"] == [6, 7, 9, 10, 19, 20])
    ck("fonte: texto do fantasma repetido = %s" % F["texto_ghost"], F["texto_ghost"] == [1, 8, 14])
    ck("fonte: bônus de rolagem não vazio = %s (slots vazios %d/%d)"
       % (F["bonus_nao_vazio"], F["slots_bonus_vazio"], F["opcoes_total"]), F["bonus_nao_vazio"] == [2, 3, 5, 11])
    ck("fonte: batalha.iniciar=true = %s" % F["batalha_iniciar_true"], F["batalha_iniciar_true"] == [4, 9, 10, 15, 16, 20])
    ck("fonte: ids duplicados = %s (únicos %d, chaves %d)"
       % (F["ids_duplicados"], F["ids_unicos"], F["chaves_unicas"]), list(F["ids_duplicados"].values()) == [2])
    ck("fonte: typos originais = %s" % F["typos_originais"],
       F["typos_originais"] == {2: ["appeares"], 13: ["whisperes"]})
    ck("fonte: PPtr nulo presente em 20/20 (não é anomalia distintiva)",
       F["eventos_com_pptr_nulo"] == list(range(1, 21)))
    ck("validação JSON coerente com os fatos",
       val["contagens"]["manter"] == 7 and val["contagens"]["melhorar"] == 13
       and val["contagens"]["total"] == 20)

    if "--md" in sys.argv:
        print("== 5. Coerência md <-> validação JSON ==")
        md = open(MD, encoding="utf-8").read()
        ck("md existe e tem 20 seções '### <ordinal> —'",
           len(re.findall(r"^### \d+ — ", md, re.M)) == 20, str(len(re.findall(r"^### \d+ — ", md, re.M))))
        missing = []
        for r in recs:
            for p in r["propostas"]:
                if p["code"] not in md or p["path"] not in md:
                    missing.append((r["ordinal"], p["code"], p["path"]))
        ck("md cita todas as propostas (código + JSONPath)", not missing, str(missing[:5]))
        ck("md declara MANTER=7 / MELHORAR=13", "MANTER = 7" in md and "MELHORAR = 13" in md)
        ck("md registra supersessão nominal", "supersed" in md.lower() or "SUPERSED" in md)
        ck("md marca runtime NAO_EXERCITADO", "NAO_EXERCITADO" in md)

    with open(os.path.join(BASE, "EV-R2-NORMAL-b01-parte02-fatos.json"), "w", encoding="utf-8") as f:
        json.dump(F, f, ensure_ascii=False, indent=1)

    print("== RESULTADO ==")
    print("PASS %d / FAIL %d / exit %d" % (len(PASS), len(FAIL), 1 if FAIL else 0))
    if FAIL:
        for x in FAIL:
            print("FAIL:", x)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
