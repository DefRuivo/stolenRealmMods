#!/usr/bin/env python
"""Conformidade da familia UI: superficie IMPLEMENTADA da nossa API x contrato do INVENTARIO.

API-R1-I2 (cartao t_9fa61e7e). Nao executa nada do jogo: le dois JSON de metadados.

Entrada 1 (gerada por comando):  api/docs/ui-contract.json
    dotnet run --project api/tools/Inspect/Inspect.csproj -c Release -- ui \
      api/Plugin/bin/Release/netstandard2.1/RealmApi.dll > api/docs/ui-contract.json

Entrada 2 (contrato anonimizado ja existente): api/docs/contract-inventory.json

Saida: api/docs/ui-contract-diff.json  (veredito + divergencias + controle negativo)
Exit code: 0 somente quando a comparacao passa E o controle negativo acusa erro (nao-vacuidade).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "api" / "docs" / "ui-contract.json"
INVENTORY = ROOT / "api" / "docs" / "contract-inventory.json"
OUT = ROOT / "api" / "docs" / "ui-contract-diff.json"

# Mapa do namespace anonimizado (Inspect surface troca o nome do assembly de origem por este prefixo).
NORMALIZE = {
    "Gumatos.RealmApi.ContractReference.UI.": "Gumatos.RealmApi.UI.",
    "Gumatos.RealmApi.ContractReference.Skills.": "Gumatos.RealmApi.Skills.",
}

FAMILY_TYPES = 5


def load(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def normalize(name):
    for old, new in NORMALIZE.items():
        name = name.replace(old, new)
    return name


def expected_surface(inventory):
    """Superficie esperada a partir do inventario (familia UI + enum Skills.SkillTree)."""
    types = {}
    for entry in inventory["types"]:
        name = entry["name"]
        if ".UI." not in name and not name.endswith(".Skills.SkillTree"):
            continue
        methods = []
        for method in entry["methods"]:
            methods.append(
                {
                    "signature": normalize(method["signature"]),
                    "name": method["signature"].split("::")[-1].split("(")[0],
                    "isStatic": method["isStatic"],
                    "returnType": normalize(method["signature"].split(" ")[0]),
                    "parameters": [
                        {
                            "name": p["name"],
                            "type": normalize(p["type"]),
                            "isOptional": bool(p.get("isOptional")),
                            "hasDefault": bool(p.get("hasDefault")),
                        }
                        for p in method["parameters"]
                    ],
                }
            )
        if name.endswith(".Skills.SkillTree"):
            types[normalize(name)] = {"kind": "enum", "fields": sorted(f["signature"].split("::")[-1] for f in entry["fields"] if f["signature"].split("::")[-1] != "value__")}
        else:
            types[normalize(name)] = {"kind": "class", "methods": methods}
    return {"types": types}


def actual_surface(contract):
    types = {}
    for entry in contract["types"]:
        methods = [
            {
                "signature": m["signature"],
                "name": m["name"],
                "isStatic": bool(m["isStatic"]),
                "returnType": m["returnType"],
                "parameters": [
                    {"name": p["name"], "type": p["type"], "isOptional": bool(p["isOptional"]), "hasDefault": bool(p["hasDefault"])}
                    for p in m["parameters"]
                ],
            }
            for m in entry["methods"]
        ]
        types[entry["name"]] = {"kind": "class", "methods": methods}
    enum = contract.get("skillsEnum")
    if enum:
        types[enum["name"]] = {"kind": "enum", "fields": sorted(enum["fields"])}
    return {"types": types}


def compare(expected, actual):
    problems = []
    for name, spec in sorted(expected["types"].items()):
        got = actual["types"].get(name)
        if got is None:
            problems.append({"type": name, "issue": "tipo ausente na superficie implementada"})
            continue
        if spec["kind"] == "enum":
            if got["fields"] != spec["fields"]:
                problems.append({"type": name, "issue": "membros do enum divergem", "expected": spec["fields"], "actual": got["fields"]})
            continue
        key = lambda m: (m["name"], tuple(p["type"] for p in m["parameters"]))
        expected_set = {key(m): m for m in spec["methods"]}
        actual_set = {key(m): m for m in got["methods"]}
        for k in sorted(set(expected_set) - set(actual_set)):
            problems.append({"type": name, "issue": "metodo ausente", "method": list(k)})
        for k in sorted(set(actual_set) - set(expected_set)):
            problems.append({"type": name, "issue": "metodo a mais (fora do contrato)", "method": list(k)})
        for k in sorted(set(expected_set) & set(actual_set)):
            want, have = expected_set[k], actual_set[k]
            if want["isStatic"] != have["isStatic"]:
                problems.append({"type": name, "issue": "estaticidade divergente", "method": k[0]})
            if want["returnType"] != have["returnType"]:
                problems.append({"type": name, "issue": "retorno divergente", "method": k[0], "expected": want["returnType"], "actual": have["returnType"]})
            if [p["name"] for p in want["parameters"]] != [p["name"] for p in have["parameters"]]:
                problems.append({"type": name, "issue": "nomes de parametro divergentes", "method": k[0],
                                 "expected": [p["name"] for p in want["parameters"]],
                                 "actual": [p["name"] for p in have["parameters"]]})
            if [(p["isOptional"], p["hasDefault"]) for p in want["parameters"]] != [(p["isOptional"], p["hasDefault"]) for p in have["parameters"]]:
                problems.append({"type": name, "issue": "opcionalidade/valor padrao divergentes", "method": k[0],
                                 "expected": [(p["isOptional"], p["hasDefault"]) for p in want["parameters"]],
                                 "actual": [(p["isOptional"], p["hasDefault"]) for p in have["parameters"]]})
    for name in sorted(set(actual["types"]) - set(expected["types"])):
        problems.append({"type": name, "issue": "tipo implementado fora do contrato"})
    family_count = sum(1 for n in expected["types"] if ".UI." in n)
    if family_count != FAMILY_TYPES:
        problems.append({"issue": f"inventario com {family_count} tipos de familia UI; esperado {FAMILY_TYPES}"})
    return problems


def main():
    missing = [str(p) for p in (CONTRACT, INVENTORY) if not p.exists()]
    if missing:
        print("AUSENTE: " + ", ".join(missing))
        return 2
    expected = expected_surface(load(INVENTORY))
    actual = actual_surface(load(CONTRACT))
    problems = compare(expected, actual)

    # Controle negativo (nao-vacuidade): uma assinatura alterada DE PROPOSITO tem de ser acusada.
    mutated = json.loads(json.dumps(actual))
    first = mutated["types"]["Gumatos.RealmApi.UI.UIFactory"]["methods"][0]
    first["parameters"] = list(first["parameters"]) + [{"name": "extra", "type": "System.Int32", "isOptional": False, "hasDefault": False}]
    control = compare(expected, mutated)

    verdict = "CONFORME" if not problems else "DIVERGENTE"
    report = {
        "schemaVersion": 1,
        "scope": "realmapi-ui-family-conformance-vs-inventory",
        "inputs": {"implementedSurface": str(CONTRACT.relative_to(ROOT)), "contractInventory": str(INVENTORY.relative_to(ROOT))},
        "normalization": NORMALIZE,
        "expected": {"types": sorted(expected["types"])},
        "implemented": {"types": sorted(actual["types"])},
        "verdict": verdict,
        "problems": problems,
        "negativeControl": {
            "description": "assinatura alterada de proposito em UIFactory (parametro System.Int32 a mais)",
            "problemsFound": len(control),
            "ok": len(control) > 0,
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    print(f"{verdict}: {len(problems)} divergencia(s); controle negativo acusou {len(control)} -> {OUT}")
    for problem in problems:
        print("  - " + json.dumps(problem, ensure_ascii=False))
    return 0 if (not problems and control) else 1


if __name__ == "__main__":
    sys.exit(main())
