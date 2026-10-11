"""Build/run proof OFFLINE in a fresh sandbox; no game or profile operations.

Reuses AUT3 command/sanitization/hash helpers. Copies source tracked AND untracked
from tools/automacao (excluding outputs), selected reference DLLs for compilation only.
No .git, remotes, credentials, owner profile, saves or proprietary DLL in source zip.
"""
import argparse
import importlib.util
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "tools/automacao/kit13"


def load_aut3():
    spec = importlib.util.spec_from_file_location("kit13_aut3", ROOT / "tools/automacao/offline/aut3_lib.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("AUT3 helper indisponivel")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="NEW evidence directory, normally scratch/kit/KIT-13-run661")
    args = parser.parse_args()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=False)
    sandbox = out / "sandbox"
    sandbox.mkdir()
    lib = load_aut3()
    baseline = {}
    suffixes = {".py", ".cs", ".csproj", ".json", ".props", ".md", ".sh"}
    files = [ROOT / "Directory.Build.props", SOURCE / "nuget.config"]
    for path in (ROOT / "tools/automacao").rglob("*"):
        if path.is_file() and path.suffix in suffixes and not any(part in {"bin", "obj", "__pycache__", ".git", "out"} for part in path.relative_to(ROOT).parts):
            files.append(path)
    reference_names = ("BepInEx.dll", "0Harmony.dll", "UnityEngine.dll", "UnityEngine.CoreModule.dll", "UnityEngine.UI.dll", "UnityEngine.TextRenderingModule.dll", "UnityEngine.UIModule.dll")
    files.extend(ROOT / "lib" / name for name in reference_names)
    for path in files:
        relative = path.relative_to(ROOT)
        baseline[str(relative)] = lib.sha256_file(str(path))
        target = sandbox / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    managed = Path("E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/Managed")
    game_refs = sandbox / "game-refs"
    game_refs.mkdir()
    for name in ("UnityEngine.ScreenCaptureModule.dll", "UnityEngine.ImageConversionModule.dll"):
        shutil.copy2(managed / name, game_refs / name)
    (out / "baseline.json").write_text(json.dumps(baseline, indent=2), encoding="utf-8")
    kit = sandbox / "tools/automacao/kit13"
    logs = out / "logs"
    logs.mkdir()
    records = []
    env = {"DOTNET_CLI_TELEMETRY_OPTOUT": "1", "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1", "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": str(out), "TEMP": str(out), "TMP": str(out), "DOTNET_CLI_HOME": str(out / "dotnet-home"), "USERPROFILE": str(out / "user-home"), "APPDATA": str(out / "appdata"), "HOME": str(out / "user-home")}

    def command(label, argv, expected=0, cwd=kit, contains=None):
        record = lib.run_cmd([str(a) for a in argv], cwd=str(cwd), timeout=180, env=env)
        text = lib.sanitiza(record["stdout"] + record["stderr"])
        (logs / (label + ".log")).write_text(text, encoding="utf-8")
        record.pop("stdout"); record.pop("stderr")
        record.update(label=label, expected=expected, log=str(logs / (label + ".log")))
        records.append(record)
        (out / "commands.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
        print(label + "|exit=" + str(record["exit_code"]))
        if record["exit_code"] != expected or record["timeout"] or record["erro_lancamento"] or (contains and contains not in text):
            raise RuntimeError("FALHOU ou NAO_EXERCITADO: " + label + "; consulte log")
        return text

    projects = [str(p.relative_to(kit)) for p in sorted(kit.rglob("*.csproj"))]
    for i, project in enumerate(projects):
        command("preflight-denied-" + str(i), ["dotnet", "msbuild", project, "-t:Kit13OfflinePreflight", "-p:DeployToBepInEx=true", "-nologo"], 1, contains="KIT13:")
        command("preflight-safe-" + str(i), ["dotnet", "msbuild", project, "-t:Kit13OfflinePreflight", "-p:DeployToBepInEx=false", "-nologo"])
    for name, project in (("mod", "ExampleMod/ExampleMod.csproj"), ("harness", "Harness/Harness.csproj"), ("standalone", "Standalone/Standalone.csproj"), ("core", "CoreHarness/CoreHarness.csproj")):
        command("build-" + name, ["dotnet", "build", project, "-c", "Release", "-p:DeployToBepInEx=false", "-p:GameManaged=" + str(game_refs), "--nologo"])
    command("csharp-tests", ["dotnet", "Harness/bin/Release/net6.0/Harness.dll"], contains="Ran 17 tests; failures=0")
    # Only the standalone app + its OWN state library; SDK physically absent.
    bare = out / "bare-mod"
    shutil.copytree(kit / "Standalone/bin/Release/net6.0", bare)
    if any("KitSdk" in p.name or "Adapter" in p.name or "KIT04" in p.name for p in bare.iterdir()):
        raise RuntimeError("standalone indevidamente depende do kit")
    command("standalone-no-kit", ["dotnet", str(bare / "Standalone.dll")], cwd=bare, contains="count=2; kit absent")
    command("core-bridge", ["dotnet", "CoreHarness/bin/Release/net6.0/CoreHarness.dll"], contains="disabled=0 enabled=1")
    command("python-tests", [sys.executable, "-m", "unittest", "test_packages", "-v"], contains="Ran 14 tests")
    for label, package, state, allow, expected in (
        ("denied", "examples/menu.json", "examples/state.json", False, 2),
        ("menu", "examples/menu.json", "examples/state.json", True, 0),
        ("skills", "examples/skills.json", "examples/state.json", True, 0),
        ("missing", "examples/menu.json", "missing.json", True, 1)):
        argv = [sys.executable, "packages.py", package, state, "--lock", str(out / "front.lock"), "--output", str(out / ("cli-" + label + ".json"))]
        if allow: argv.append("--allow-offline-observation")
        command("cli-" + label, argv, expected)
        result = json.loads((out / ("cli-" + label + ".json")).read_text(encoding="utf-8"))
        if result["runtime_exercitado"] is not False:
            raise RuntimeError("fixture promovida a runtime")
    changed = [path for path, digest in baseline.items() if lib.sha256_file(str(ROOT / path)) != digest]
    copied = [path for path, digest in baseline.items() if lib.sha256_file(str(sandbox / path)) != digest]
    verification = {"baseline_files": len(baseline), "live_changed": changed, "copy_mismatch": copied,
                    "no_git": not (sandbox / ".git").exists(), "runtime_exercitado": False,
                    "dll_hashes": {str(p.relative_to(kit)): lib.sha256_file(str(p)) for p in kit.rglob("*.dll") if "bin" in p.parts and "Release" in p.parts}}
    (out / "verification.json").write_text(json.dumps(verification, indent=2), encoding="utf-8")
    if changed or copied: raise RuntimeError("fontes alterados durante prova")
    print("KIT13 BASELINE PASSOU; game NAO_EXERCITADO; " + str(out))


if __name__ == "__main__":
    main()
