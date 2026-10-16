# -*- coding: utf-8 -*-
"""Auditoria offline do lote EV-R2-NORMAL-b03 (eventos 41-60, categoria Normal).

Somente leitura sobre as fontes EV-R1 e sobre a proposta anterior.
Verifica: integridade das 11 fontes, ordem Normal (markdown vs JSON), identidade
das 20 posicoes, unicidade de GUID, literais falsos de EV-R2-NORMAL-b03-parte01.md,
campos de texto vazios, posicao dos CR, justificativas MD x propostas.json,
existencia literal dos campos "antes" de
cada proposta, contagens de veredito e fatos pontuais (#41 cura, #54/#58 raridade,
#49 VictoryEvent/FailureEvent e referencia de batalha).

Uso: python EV-R2-NORMAL-b03-validar.py
Saida: EV-R2-NORMAL-b03-validacao.json no mesmo diretorio + resumo PASS/FAIL.
"""
import json, os, re, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(HERE))
EV = os.path.join(BASE, "docs", "cobertura", "EV-R1", "eventos.json")
MD = os.path.join(BASE, "docs", "cobertura", "EV-R1", "lote-Normal-v2.md")
SCHEMA = os.path.join(BASE, "docs", "cobertura", "EV-R1", "eventos.schema.json")
CAT = os.path.join(BASE, "docs", "cobertura", "EV-R1", "catalogo-referencias.json")
P01 = os.path.join(BASE, "docs", "automacao", "EV-R2-NORMAL-b03-parte01.md")
PROP = os.path.join(BASE, "docs", "automacao", "EV-R2-NORMAL-b03-propostas.json")
MD02 = os.path.join(BASE, "docs", "automacao", "EV-R2-NORMAL-b03-parte02.md")
OUT = os.path.join(BASE, "docs", "automacao", "EV-R2-NORMAL-b03-validacao.json")

SOURCES = {
    "C:/dev/stolen-realm/docs/cobertura/EV-R1/eventos.json": "4a8decac7e98a2b0bf8692057a57789a71b94c230e3b9ca93817f039c86d1d13",
    "C:/dev/stolen-realm/docs/cobertura/EV-R1/lote-Normal-v2.md": "83b30ada3d78e596b8c7c0784d5e741b43654b14ab02d5377d8a1b245b84f146",
    "C:/dev/stolen-realm/docs/cobertura/EV-R1/eventos.schema.json": "6950ec43deba94143150f0584bb87ca5406b3ef16f1ae2f18ad8aa943a62b3bc",
    "C:/dev/stolen-realm/docs/cobertura/EV-R1/catalogo-referencias.json": "94077cc887621933abe7bbbbd96e91c5a887478dba8fd000b8f4a4129c3745a5",
    "C:/dev/stolen-realm/docs/automacao/EV-R2-NORMAL-b01-parte01.md": "e65daa3413e18adc1d73b6272d936f8d7d593da83e90abfbb06c34f6aee530e9",
    "C:/dev/stolen-realm/docs/automacao/EV-R2-NORMAL-b02-parte01.md": "cbd464a551efb1420c0032c00c03ecbeee5933781f465a8a12d06c57ef046552",
    "C:/dev/stolen-realm/docs/automacao/EV-R2-NORMAL-b03-parte01.md": "80f14e416c0e05302c4fed7ed2c51793cd975426013647e09887dfbb8cd813b5",
    "C:/dev/stolen-realm/docs/automacao/EV-R2-NORMAL-b04-parte01.md": "2dbc044be0e4a568fb2483658d6da7c4c27eb28b17e6a7421ba0764e209ac0fc",
    "C:/Users/Pichau/AppData/Local/hermes/kanban/attachments/t_a5c365a4/analise-ev81-100.md": "abb389ed1600a6ca72edde89ed599c920f53123e154a7c9dcab7c16ae6063235",
    "C:/dev/stolen-realm/docs/automacao/EV-R2-NORMAL-b06-parte01.md": "d79c302a20ec3968787bc1174810fbefa2922609a10caa8cd2704484a5bdeb83",
    "C:/dev/stolen-realm/docs/automacao/EV-R2-NORMAL-b07-parte01.md": "d8d553f8945bdb4c33da7cf7a51e27fcd40194f3900d7a1d9fc99381bbd5e344",
}

REPORT = []
FAILS = []
def check(name, ok, detail):
    REPORT.append({"check": name, "ok": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + name + " | " + str(detail))
    if not ok:
        FAILS.append(name)

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

# 1) integridade das 11 fontes ------------------------------------------------
unchanged, changed = [], []
for path, expected in SOURCES.items():
    got = sha256(path)
    (unchanged if got == expected else changed).append(path)
check("SOURCES_11_UNCHANGED", len(unchanged) == 11 and not changed,
      json.dumps({"inputs": len(SOURCES), "unchanged": len(unchanged), "changed": changed}))

# 2) fontes ---------------------------------------------------------------
doc = json.load(open(EV, encoding="utf-8"))
eventos = doc["eventos"]
norm = [e for e in eventos if e["categoria"] == "Normal"]
check("NORMAL_COUNT_160", len(norm) == 160, len(norm))

md_titles = [l[3:].strip() for l in open(MD, encoding="utf-8") if l.startswith("## ")]
json_titles = [e["titulo"] for e in norm]
check("MD_EQUALS_JSON_NORMAL_ORDER", md_titles == json_titles,
      json.dumps({"md_sections": len(md_titles), "json_normal": len(json_titles),
                  "iguais": md_titles == json_titles}))

# 3) GUIDs ---------------------------------------------------------------
ids = [e["id"] for e in eventos]
dups = {}
for e in eventos:
    dups.setdefault(e["id"], []).append(e["chave"])
dups = {k: v for k, v in dups.items() if len(v) > 1}
ACCUSED = "81c8fe59-5e3b-4e5e-b196-ec9bfcf44649"
check("GUID_UNICOS", len(set(ids)) == 255 and len(ids) == 256, {"total": len(ids), "unicos": len(set(ids))})
check("GUID_DUPLICADO_REAL_UNICO", dups == {"5b740c2b-3480-48f2-997b-88c8291db0c0":
                                            ["resources.assets:2545539", "resources.assets:2545540"]},
      json.dumps(dups))
check("GUID_ACUSADO_AUSENTE", ACCUSED not in ids, {"literal": ACCUSED, "existe_em_algum_evento": ACCUSED in ids})

# 4) identidade das 20 posicoes ------------------------------------------
prop = json.load(open(PROP, encoding="utf-8"))
por_ord = {ev["ordinal"]: ev for ev in prop["eventos"]}
identity_bad = []
for n in range(41, 61):
    e = norm[n - 1]
    p = por_ord[n]
    for campo, real in (("chave", e["chave"]), ("id", e["id"]), ("titulo", e["titulo"]),
                        ("categoria", e["categoria"]), ("raridade", e["raridade"]),
                        ("peso", e["peso"]), ("disabled", e["condicoes"]["disabled"])):
        if p[campo] != real:
            identity_bad.append({"ordinal": n, "campo": campo, "doc": p[campo], "json": real})
check("IDENTIDADE_20_POSICOES", not identity_bad, {"divergencias": identity_bad})

# 5) SHA de proveniencia do documento vs fonte ---------------------------
sha_bad = [{"ordinal": n, "doc": por_ord[n]["sha256_objeto"], "json": norm[n - 1]["origem"]["sha256_objeto"]}
           for n in range(41, 61) if por_ord[n]["sha256_objeto"] != norm[n - 1]["origem"]["sha256_objeto"]]
check("SHA256_OBJETO_20", not sha_bad, {"divergencias": sha_bad})

# 5b) justificativas do MD x propostas.json (texto literal) ----------------
md_txt = open(MD02, encoding="utf-8").read()
just_bad = [{"ordinal": p["ordinal"], "justificativa_json": p["justificativa"][:80]}
            for p in prop["eventos"] if p["justificativa"] not in md_txt]
check("MD_JUSTIFICATIVAS_20_EQ_JSON", not just_bad,
      json.dumps({"eventos": len(prop["eventos"]), "divergencias": just_bad}))

# 6) literais (GUID/SHA) citados em parte01 que nao existem na fonte -----
txt01 = open(P01, encoding="utf-8").read()
uuid_re = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b")
sha_re = re.compile(r"\b[0-9a-f]{40,}\b")
sha_source = {e["origem"]["sha256_objeto"] for e in eventos}
uuid_source = set(ids)
falsos_guid, falsos_sha = [], []
for m in uuid_re.finditer(txt01):
    if m.group(0) not in uuid_source:
        falsos_guid.append(m.group(0))
for m in sha_re.finditer(txt01):
    if m.group(0) not in sha_source:
        falsos_sha.append(m.group(0))
check("P01_LITERAIS_FALSOS", bool(falsos_guid) and bool(falsos_sha),
      json.dumps({"guid_ocorrencias": len(falsos_guid), "guid_distintos": sorted(set(falsos_guid)),
                  "sha_ocorrencias": len(falsos_sha), "sha_distintos": sorted(set(falsos_sha)),
                  "sha_comprimentos": sorted({len(x) for x in falsos_sha})}))
SHA58 = "f1803712ec88905b8075eee409b77ba21f335d9142ee90dbbf2459222c64aca"
check("P01_SHA58_COMPRIMENTO_INCOMPATIVEL",
      SHA58 in txt01 and len(SHA58) != 64 and SHA58 not in sha_source and norm[57]["origem"]["sha256_objeto"] != SHA58,
      json.dumps({"literal": SHA58, "comprimento": len(SHA58), "existe_na_fonte": SHA58 in sha_source,
                  "sha_real_58": norm[57]["origem"]["sha256_objeto"]}))
check("P01_LITERAL_ACUSADO_PRESENTE_NO_DOC", ACCUSED in txt01, True)

# 7) campos de texto vazios --------------------------------------------
vazios = []
for n in range(41, 61):
    e = norm[n - 1]
    if e["texto"].strip() == "":
        vazios.append({"ordinal": n, "titulo": e["titulo"], "repr": repr(e["texto"]),
                       "len": len(e["texto"]), "estrito_vazio": e["texto"] == "",
                       "somente_whitespace": e["texto"] != "" and e["texto"].strip() == ""})
check("VAZIOS_43_47_56", [v["ordinal"] for v in vazios] == [43, 47, 56], json.dumps(vazios))

# 8) posicao dos CR ------------------------------------------------------
cr = []
for n in range(41, 61):
    e = norm[n - 1]
    alvos = [("$.texto", e["texto"])]
    for o in e["opcoes"]:
        alvos.append(("$.opcoes[%d].texto" % o["indice"], o["texto"]))
        for a in o["efeitos"]:
            alvos.append(("$.opcoes[%d].efeitos[%d].campos_originais.activationText" % (o["indice"], a["indice"]),
                          str(a["campos_originais"].get("activationText", ""))))
    for path, val in alvos:
        if "\r" in val:
            pos = [i for i, ch in enumerate(val) if ch == "\r"]
            cr.append({"ordinal": n, "jsonpath": path, "cr": len(pos),
                       "posicao": "FIM" if all(p >= len(val) - 4 for p in pos) else "MEIO"})
check("CR_INVENTARIO", sorted({c["ordinal"] for c in cr}) == [49, 54, 59, 60], json.dumps(cr))

# 9) campos "antes" das propostas existem literalmente ------------------
def resolve(e, jsonpath):
    toks = jsonpath.split(".")[1:]
    cur = e
    for tok in toks:
        m = re.match(r"^([a-z_]+)\[(\d+)\]$", tok)
        if m:
            cur = cur[m.group(1)][int(m.group(2)) - 1]
        else:
            cur = cur[tok]
    return cur

antes_ok, antes_bad = 0, []
for n in range(41, 61):
    e = norm[n - 1]
    for pr in por_ord[n]["propostas"]:
        try:
            valor = resolve(e, pr["jsonpath"])
        except Exception as ex:
            antes_bad.append({"ordinal": n, "jsonpath": pr["jsonpath"], "erro": repr(ex)})
            continue
        if pr["antes"] not in valor:
            antes_bad.append({"ordinal": n, "jsonpath": pr["jsonpath"], "antes": pr["antes"][:60],
                              "erro": "antes nao encontrado"})
        elif pr["depois"] == pr["antes"]:
            antes_bad.append({"ordinal": n, "jsonpath": pr["jsonpath"], "erro": "depois igual ao antes"})
        else:
            antes_ok += 1
check("ANTES_LITERAIS_CONFERIDOS", not antes_bad, json.dumps({"pass": antes_ok, "falhas": antes_bad}))

# 10) contagens de veredito ----------------------------------------------
manter = [n for n in range(41, 61) if por_ord[n]["veredito"] == "MANTER"]
melhorar = [n for n in range(41, 61) if por_ord[n]["veredito"] == "MELHORAR"]
outros = [n for n in range(41, 61) if por_ord[n]["veredito"] not in ("MANTER", "MELHORAR")]
check("VEREDITOS_13_7", len(manter) == 13 and len(melhorar) == 7 and not outros,
      json.dumps({"MANTER": len(manter), "MELHORAR": len(melhorar), "outros": outros}))
check("ORDINAIS_UNICOS_41_60", sorted(por_ord) == list(range(41, 61)), sorted(por_ord))

# 11) fatos pontuais retratados -----------------------------------------
e41 = norm[40]; e54 = norm[53]; e58 = norm[57]
vm = e41["opcoes"][1]["efeitos"][0]["efeitos"][0]["vida_mana"]
check("EV41_CURA_50_50", vm["percentMaxHealth"] == 50.0 and vm["percentMaxMana"] == 50.0, json.dumps(vm))
check("EV54_EV58_MYTHIC_POOL_NORMAL",
      e54["raridade"] == {"valor": 4, "nome": "Mythic"} and e58["raridade"] == {"valor": 4, "nome": "Mythic"}
      and [p["nome"] for p in e54["pool"]] == ["Normal"] and [p["nome"] for p in e58["pool"]] == ["Normal"],
      json.dumps({"54": {"rar": e54["raridade"], "pool": [p["nome"] for p in e54["pool"]]},
                  "58": {"rar": e58["raridade"], "pool": [p["nome"] for p in e58["pool"]]}}))
e53 = norm[52]
acts53 = [(a["resultado"]["nome"], a["limite_rolagem"], bool(a["batalha"]["iniciar"]))
          for a in e53["opcoes"][0]["efeitos"]]
check("EV53_UMA_OPCAO_STRIKE_SILENTLY",
      len(e53["opcoes"]) == 1 and e53["opcoes"][0]["titulo"] == "Strike silently"
      and acts53 == [("Success", 12, False), ("Failure", 1, True)],
      json.dumps({"opcoes": [o["titulo"] for o in e53["opcoes"]], "acoes": acts53}))
e59 = norm[58]
check("EV59_WAIT_LEAVE", [o["titulo"] for o in e59["opcoes"]] == ["Wait", "Leave"],
      [o["titulo"] for o in e59["opcoes"]])
e60 = norm[59]
check("EV60_HOLD_YOUR_BREATH_ORDINAL_60",
      e60["titulo"] == "Hold your Breath" and e60["chave"] == "resources.assets:2545609"
      and [o["titulo"] for o in e60["opcoes"]] == ["Claim"],
      {"titulo": e60["titulo"], "chave": e60["chave"], "opcoes": [o["titulo"] for o in e60["opcoes"]]})

# 11b) VictoryEvent/FailureEvent e referencia de batalha por evento -------
# (campo que escapou da rodada 1: #49 tem VictoryEvent :2545594 «Foreboding
#  Gem - Victory» e FailureEvent nulo; a referencia de batalha e que e nula)
def ref_chave(b):
    r = b.get("referencia") or {}
    return r.get("chave")

def pptr(b, campo):
    return (b.get("override") or {}).get(campo)

batalha_inv = []
for n in range(41, 61):
    for o in norm[n - 1]["opcoes"]:
        for a in o["efeitos"]:
            b = a["batalha"]
            if b["iniciar"]:
                batalha_inv.append({
                    "ordinal": n, "opcao": o["indice"], "acao": a["indice"],
                    "resultado": a["resultado"]["nome"],
                    "referencia": ref_chave(b),
                    "victory_event": (pptr(b, "VictoryEvent") or {}).get("m_PathID"),
                    "failure_event": (pptr(b, "FailureEvent") or {}).get("m_PathID"),
                    "forced_enemies": pptr(b, "ForcedEnemies"),
                    "battle_point_value": pptr(b, "BattlePointValue"),
                })
check("BATALHA_VICTORY_FAILURE_INVENTARIO_20",
      len(batalha_inv) == 9 and all(b["resultado"] in ("Success", "Failure") for b in batalha_inv),
      json.dumps(batalha_inv))

b49 = norm[48]["opcoes"][0]["efeitos"][0]["batalha"]
check("EV49_BATALHA_VICTORY_EVENT_2545594",
      b49["iniciar"] is True and ref_chave(b49) is None
      and pptr(b49, "ForcedEnemies") == []
      and pptr(b49, "BattlePointValue") == 16
      and pptr(b49, "VictoryEvent") == {"m_FileID": 0, "m_PathID": 2545594}
      and pptr(b49, "FailureEvent") == {"m_FileID": 0, "m_PathID": 0},
      json.dumps({"referencia": ref_chave(b49),
                  "VictoryEvent": pptr(b49, "VictoryEvent"),
                  "FailureEvent": pptr(b49, "FailureEvent"),
                  "ForcedEnemies": pptr(b49, "ForcedEnemies"),
                  "BattlePointValue": pptr(b49, "BattlePointValue")}))

cat = json.load(open(CAT, encoding="utf-8"))
alvo49 = [r for r in cat["registros"] if r.get("path_id") == 2545594 and r.get("file") == "resources.assets"]
check("CATALOGO_2545594_FOREBODING_GEM_VICTORY",
      len(alvo49) == 1 and alvo49[0]["script"] == "PartyEvent"
      and alvo49[0]["data"]["m_Name"] == "Foreboding Gem - Victory",
      json.dumps([{"file": r["file"], "path_id": r["path_id"], "script": r["script"],
                   "nome": r["data"]["m_Name"]} for r in alvo49]))

txt02 = open(MD02, encoding="utf-8").read()
FRASE_CORRETA = "referência nula — usa o BattleInfo do próprio evento, BattlePointValue 16 —"
check("MD49_VICTORYEVENT_CORRIGIDO",
      "ForcedEnemies vazio e VictoryEvent nulo" not in txt02
      and FRASE_CORRETA in txt02
      and "`resources.assets:2545594` «Foreboding Gem - Victory»" in txt02
      and "FailureEvent nulo" in txt02,
      json.dumps({"frase_falsa_presente": "ForcedEnemies vazio e VictoryEvent nulo" in txt02,
                  "frase_correta_presente": FRASE_CORRETA in txt02,
                  "victory_event_citado": "`resources.assets:2545594` «Foreboding Gem - Victory»" in txt02,
                  "failure_event_nulo_citado": "FailureEvent nulo" in txt02}))

# 12) distribuicoes / inventario -----------------------------------------
rar = {}
for n in range(41, 61):
    r = norm[n - 1]["raridade"]["nome"]
    rar[r] = rar.get(r, 0) + 1
disabled = [n for n in range(41, 61) if norm[n - 1]["condicoes"]["disabled"] == 1]
batalhas = []
for n in range(41, 61):
    for o in norm[n - 1]["opcoes"]:
        for a in o["efeitos"]:
            if a["batalha"]["iniciar"]:
                batalhas.append([n, o["indice"], a["indice"], a["resultado"]["nome"]])
n_opcoes = sum(len(norm[n - 1]["opcoes"]) for n in range(41, 61))
check("INVENTARIO_DISTRIBUICOES",
      rar == {"Common": 17, "Rare": 1, "Mythic": 2} and disabled == [51] and n_opcoes == 30 and len(batalhas) == 9,
      json.dumps({"raridades": rar, "disabled": disabled, "opcoes_total": n_opcoes,
                  "acoes_com_batalha": batalhas,
                  "eventos_com_batalha": sorted({b[0] for b in batalhas})}))

# 13) o documento nao propoe balanceamento -------------------------------
nat = set()
for n in range(41, 61):
    nat.add(por_ord[n]["natureza"])
check("SEM_PROPOSTA_DE_BALANCEAMENTO",
      all(("MECANICA" not in x.upper()) and ("BALANCEAMENTO" not in x.upper()) for x in nat),
      sorted(nat))

resumo = {
    "lote": "b03", "faixa": [41, 60], "categoria": "Normal",
    "checks": len(REPORT), "pass": sum(1 for r in REPORT if r["ok"]),
    "fail": len(FAILS), "falhas": FAILS,
    "vereditos": {"MANTER": manter, "MELHORAR": melhorar},
    "vazios": [v["ordinal"] for v in vazios],
    "cr": cr,
    "propostas_antes_conferidas": antes_ok,
    "literais_falsos_parte01": {"guid_distintos": sorted(set(falsos_guid)),
                                "guid_ocorrencias": len(falsos_guid),
                                "sha_distintos": sorted(set(falsos_sha)),
                                "sha_ocorrencias": len(falsos_sha)},
    "nota_final": "Auditoria offline; runtime NAO_EXERCITADO. Nenhuma fonte foi modificada.",
    "report": REPORT,
}
json.dump(resumo, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("TOTAL %d PASS %d FAIL %d" % (resumo["checks"], resumo["pass"], resumo["fail"]))
print("OUT", OUT)
sys.exit(1 if FAILS else 0)
