"""Selective real-source mutations in sandbox. A compiler error never counts as RED.
Each named case: baseline PASS -> mutant FAIL/exit1 -> byte restoration -> PASS.
No assertion/test weakening, no game/profile or live source mutation.
"""
import argparse
import json
import os
import shutil
import sys
from pathlib import Path

from prove_offline import ROOT, SOURCE, load_aut3

SDK = "SDK/RegistryV1.cs"
ADAPTER = "OptionalAdapter/CounterAdapter.cs"
STATE = "ExampleMod/CounterState.cs"
CS = [
    ("version", SDK, "if (apiVersion != ApiVersion)", "if (false)"),
    ("duplicate", SDK, "if (entries.ContainsKey(id)) throw new InvalidOperationException(\"EXTENSAO_DUPLICADA\");", "// duplicate guard removed"),
    ("unregister", SDK, "entries.Remove(id);", "{ /* removal disabled */ }"),
    ("replacement", SDK, " && ReferenceEquals(actual, expected)", ""),
    ("mid-publish", SDK, "if (!entries.TryGetValue(pair.Key, out var current) || !ReferenceEquals(current, pair.Value)) continue;", "var current = pair.Value;"),
    ("event-isolation", SDK, "catch (Exception error) { Diagnostic(pair.Key, \"evento\", error); }", "catch (Exception) { throw; }"),
    ("reader-isolation", SDK, 'return new ReadingV1("FALHOU_FECHADO");', 'return new ReadingV1("OBSERVADO");'),
    ("validator-isolation", SDK, 'return new VerdictV1("FALHOU_FECHADO");', 'return new VerdictV1("PASSOU");'),
    ("absent", SDK, 'observed == null || observed.Status != "OBSERVADO"', 'observed == null'),
    ("reentrant", SDK, 'if (publishing) throw', 'if (false) throw'),
    ("limit", SDK, 'if (entries.Count >= 64)', 'if (false)'),
    ("disposed", SDK, 'if (disposed) throw', 'if (false) throw'),
    ("dto", SDK, 'status == "OBSERVADO" ||', 'status == "PASSOU" || status == "OBSERVADO" ||'),
    ("adapter", ADAPTER, 'observed.Value == expected ?', 'true ?'),
    ("mod-isolation", STATE, 'catch (Exception) { /* optional observer isolated */ }', 'catch (Exception) { throw; }'),
    ("diagnostic-limit", SDK, 'if (diagnostics.Count == 64)', 'if (false)'),
    ("dispose-waits", SDK, 'lock (gate)\n            {\n                if (entries.TryGetValue(id, out var actual)', 'if (true)\n            {\n                if (entries.TryGetValue(id, out var actual)'),
]
PY = [
    ("test_version", 'if package["api"] != API_VERSION:', 'if False:'),
    ("test_closed", 'set(obj) != set(required)', 'not set(required).issubset(obj)'),
    ("test_operations", '"menu", "tela", "condicao"', '"menu", "tela", "condicao", "click"'),
    ("test_timeouts", 'type(timeout) not in (int, float)', 'type(timeout) not in (int, float, bool)'),
    ("test_steps", 'not 1 <= len(steps) <= MAX_STEPS', 'not 0 <= len(steps) <= MAX_STEPS'),
    ("test_text", 'if not re.fullmatch(r"[a-z][a-z0-9.-]{0,63}", value):', 'if False:'),
    ("test_json", 'if key in result:', 'if False:'),
    ("test_size", 'if len(data) > MAX_BYTES:', 'if False:'),
    ("test_adapter", 'if adapter != package["adapter"]:', 'if False:'),
    ("test_host_permission", 'if type(observe_authorized) is not bool:', 'if False:'),
    ("test_denied", 'plan = to_plan(package, adapter="offline-file.v1", observe_authorized=observe_authorized)', 'plan = to_plan(package, adapter="offline-file.v1", observe_authorized=True)'),
    ("test_positive", 'result["runtime_exercitado"] = False', 'result["runtime_exercitado"] = True'),
    ("test_missing", 'result["runtime_exercitado"] = False', 'result["runtime_exercitado"] = False\n    result["veredito"] = "OBSERVADO"'),
    ("test_switch", '"alvo": s["target"]', '"alvo": "MainMenu"'),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("evidence", help="existing prove_offline output")
    parser.add_argument("--group", choices=("cs", "py", "extra"), required=True)
    args = parser.parse_args()
    evidence = Path(args.evidence).resolve()
    kit = evidence / "sandbox/tools/automacao/kit13"
    if not kit.is_dir() or (evidence / "sandbox/.git").exists():
        raise RuntimeError("sandbox ausente/invalido")
    aut3 = load_aut3()
    logs = evidence / ("mutations-" + args.group)
    logs.mkdir(exist_ok=False)
    results = []
    env = {"PYTHONDONTWRITEBYTECODE": "1", "DOTNET_CLI_TELEMETRY_OPTOUT": "1", "DOTNET_CLI_HOME": str(evidence / "dotnet-home"), "USERPROFILE": str(evidence / "user-home"), "APPDATA": str(evidence / "appdata"), "TEMP": str(evidence), "TMP": str(evidence), "TMPDIR": str(evidence)}

    def run(label, argv, expected, marker=None):
        r = aut3.run_cmd(argv, cwd=str(kit), env=env, timeout=120)
        text = aut3.sanitiza(r["stdout"] + r["stderr"])
        (logs / (label + ".log")).write_text(text, encoding="utf-8")
        if r["exit_code"] != expected or r["timeout"] or r["erro_lancamento"] or (marker and marker not in text):
            raise RuntimeError("prova incompleta " + label + " exit=" + str(r["exit_code"]))
        return r["exit_code"]

    def build(label, project):
        return run(label, ["dotnet", "build", project, "-c", "Release", "--no-restore", "--nologo", "-p:DeployToBepInEx=false", "-p:GameManaged=" + str(evidence / "sandbox/game-refs")], 0)

    def mutate(case, relative, old, new, project=None, command=None, marker=None):
        path = kit / relative
        original = path.read_bytes()
        text = original.decode("utf-8")
        if text.count(old) != 1: raise RuntimeError("mutacao nao unica: " + case)
        before = aut3.sha256_bytes(original)
        try:
            run(case + "-baseline", command, 0)
            path.write_text(text.replace(old, new), encoding="utf-8", newline="")
            if project: build(case + "-build-mutant", project)
            run(case + "-RED", command, 1, marker)
        finally:
            path.write_bytes(original)
            if project: build(case + "-build-restored", project)
        run(case + "-restored", command, 0)
        after = aut3.sha256_file(str(path))
        if after != before: raise RuntimeError("restauracao nao identica")
        results.append({"case": case, "source": relative, "old": old, "new": new,
                        "baseline": 0, "mutant": 1, "restored": 0, "sha_before": before, "sha_after": after})
        (logs / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
        print("RED_PROVED|" + case + "|0->1->0")

    if args.group == "cs":
        for case, relative, old, new in CS:
            mutate(case, relative, old, new, "Harness/Harness.csproj", ["dotnet", "Harness/bin/Release/net6.0/Harness.dll", case], "FAIL|" + case)
    elif args.group == "py":
        for case, old, new in PY:
            mutate(case, "packages.py", old, new, command=[sys.executable, "-m", "unittest", "test_packages.PackageTests." + case, "-v"], marker="FAIL:")
    else:
        mutate("standalone", STATE, "Count++;", "// count increment disabled", "Standalone/Standalone.csproj", ["dotnet", "Standalone/bin/Release/net6.0/Standalone.dll"], "STANDALONE FALHOU")
        mutate("core-bridge", "CoreBridge/CoreEventsExtension.cs", 'if (enabled()) core.RegistrarEvento', 'if (true) core.RegistrarEvento', "CoreHarness/CoreHarness.csproj", ["dotnet", "CoreHarness/bin/Release/net6.0/CoreHarness.dll"])
    print("MUTATIONS_PASSOU|" + args.group + "|" + str(len(results)))


if __name__ == "__main__":
    main()
