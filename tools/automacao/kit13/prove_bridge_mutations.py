"""INT-R1-C2-I1: prova de NAO-DECORATIVO da ponte RealmApi -> KitSdk (mold 0->1->0).

Muta o FONTE REAL do adaptador DENTRO DE UM SANDBOX (copia nova), mede o vermelho com a suite offline
real (`ApiBridgeHarness`), restaura byte a byte e confere o sha256 antes/depois (padrao 0->1->0 do
KIT-13, `prove_mutations.py`). Nao enfraquece assercoes, nao toca o jogo, nao toca o perfil r2modman e
nao edita o fonte vivo: a arvore viva e conferida por sha256 no fim (`live_changed`).

Compilacao que falha NUNCA conta como vermelho: cada mutacao exige build do mutante com sucesso e
depois exit 1 com "FAIL|<teste>".

Uso:
    python prove_bridge_mutations.py --out <diretorio NOVO de evidencia>
"""

import argparse
import importlib.util
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
KIT = ROOT / "tools/automacao/kit13"
PROJETO = "ApiBridgeHarness/ApiBridgeHarness.csproj"
DLL = "ApiBridgeHarness/bin/Release/net6.0/ApiBridgeHarness.dll"
FONTE = "ApiBridge/RealmHooksExtension.cs"
LIGACAO = "ApiBridge/RealmHooksBinding.cs"

GATE_ON_EVENT = "if (!Ativo()) return;\n"
GATE_ON_READ = 'if (!Ativo()) return new ReadingV1("NAO_EXERCITADO");'
CATALOGO = "if (!catalogo.Contains(notificacao.HookId)) { desconhecidos++; return; }"
MARCADOR_TRUNCAMENTO = "return texto.Substring(0, teto - MarcaDeTruncamento.Length) + MarcaDeTruncamento;"
LEITURA_DOS_ARGUMENTOS = 'texto.Append("|args=").Append(ArgumentosLegiveis(notificacao.Arguments));'
GUARDA_DO_EVENTO = 'catch (Exception erro) { Diagnostico("evento:" + erro.GetType().Name); }'
GUARDA_DO_PRODUTOR = 'catch (Exception erro) { Diagnostico("produtor:" + erro.GetType().Name); return false; }'
COMPARACAO_EXATA = "if (!string.Equals(declarado, esperado, StringComparison.Ordinal))"
QUADRO_ORDINAL = "var quadro = ordinal++;"
GUARDA_DE_DISPOSE = "lock (gate) { if (disposed) return; }"

MUTACOES = [
    ("m1-gate-do-on-event", FONTE, [(GATE_ON_EVENT, "if (false) return;\n")], ["P5"]),
    ("m2-gate-do-read", FONTE, [(GATE_ON_READ, GATE_ON_READ.replace("!Ativo()", "false"))], ["P5"]),
    ("m3-mapeia-todo-hookid", FONTE, [(CATALOGO, CATALOGO.replace("!catalogo.Contains(notificacao.HookId)", "false"))], ["P8"]),
    ("m4-sem-marcador-de-truncamento", FONTE, [(MARCADOR_TRUNCAMENTO, "return texto.Substring(0, teto);")], ["P10"]),
    ("m5-referencia-viva-dos-argumentos", FONTE, [
        ("        private long ordinal;",
         "        private long ordinal;\n        private static System.Collections.Generic.IReadOnlyList<object?>? vivos;"),
        (LEITURA_DOS_ARGUMENTOS,
         "            vivos ??= notificacao.Arguments;\n            "
         + LEITURA_DOS_ARGUMENTOS.replace("ArgumentosLegiveis(notificacao.Arguments)", "ArgumentosLegiveis(vivos)")),
    ], ["P11"]),
    ("m6-on-event-propaga-excecao", FONTE, [
        (GUARDA_DO_EVENTO, "catch (Exception) { throw; }"),
        (GUARDA_DO_PRODUTOR, "catch (Exception) { throw; }"),
    ], ["P12", "P13"]),
    ("m7-versao-por-prefixo", LIGACAO, [(COMPARACAO_EXATA, "if (string.CompareOrdinal(declarado, esperado) < 0)")], ["P2", "P3"]),
    ("m8-quadro-fixo-em-zero", FONTE, [(QUADRO_ORDINAL, "ordinal++; var quadro = 0;")], ["P7"]),
    ("m9-on-event-depois-do-dispose", FONTE, [(GUARDA_DE_DISPOSE, "lock (gate) { if (false) return; }")], ["P14"]),
    ("m10-publicacao-propaga-excecao", FONTE, [
        ('catch (Exception erro) { Diagnostico("publicacao:" + erro.GetType().Name); }', "catch (Exception) { throw; }"),
        (GUARDA_DO_EVENTO, "catch (Exception) { throw; }"),
    ], ["P15"]),
]

SUFIXOS = {".py", ".cs", ".csproj", ".json", ".props", ".md", ".sh", ".config"}
IGNORAR = {"bin", "obj", "__pycache__", ".git", "out"}


def load_aut3():
    spec = importlib.util.spec_from_file_location("bridge_aut3", ROOT / "tools/automacao/offline/aut3_lib.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("AUT3 helper indisponivel")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def copiar(sandbox: Path):
    """Copia a arvore minima com o layout relativo preservado (o sandbox tem tools/ e api/)."""
    arquivos = [ROOT / "Directory.Build.props"]
    for base in (KIT, ROOT / "api/Core", ROOT / "tools/automacao/runtime/AUT4Probe/Companheiro"):
        for caminho in base.rglob("*"):
            if caminho.is_file() and caminho.suffix in SUFIXOS and not any(p in IGNORAR for p in caminho.relative_to(ROOT).parts):
                arquivos.append(caminho)
    for caminho in arquivos:
        relativo = caminho.relative_to(ROOT)
        destino = sandbox / relativo
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(caminho, destino)
    return arquivos


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", required=True, help="diretorio NOVO de evidencia (o sandbox nasce aqui)")
    args = parser.parse_args()

    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=False)
    sandbox = out / "sandbox"
    sandbox.mkdir()
    lib = load_aut3()
    copiados = copiar(sandbox)
    baseline = {str(p.relative_to(ROOT)): lib.sha256_file(str(p)) for p in copiados}
    kit = sandbox / "tools/automacao/kit13"
    logs = out / "logs"
    logs.mkdir()
    env = {"PYTHONDONTWRITEBYTECODE": "1", "DOTNET_CLI_TELEMETRY_OPTOUT": "1", "DOTNET_SKIP_FIRST_TIME_EXPERIENCE": "1",
           "DOTNET_CLI_HOME": str(out / "dotnet-home"), "USERPROFILE": str(out / "user-home"), "APPDATA": str(out / "appdata"),
           "HOME": str(out / "user-home"), "TEMP": str(out), "TMP": str(out), "TMPDIR": str(out), "NUGET_PACKAGES": str(out / "nuget")}
    registros = []

    def roda(label, argv, esperado, marcador=None):
        resultado = lib.run_cmd([str(a) for a in argv], cwd=str(kit), timeout=300, env=env)
        texto = lib.sanitiza(resultado["stdout"] + resultado["stderr"])
        (logs / (label + ".log")).write_text(texto, encoding="utf-8")
        if resultado["exit_code"] != esperado or resultado["timeout"] or resultado["erro_lancamento"] or (marcador and marcador not in texto):
            raise RuntimeError("prova incompleta em " + label + ": exit=" + str(resultado["exit_code"]))
        registros.append({"label": label, "argv": [str(a) for a in argv], "exit": resultado["exit_code"]})
        (out / "commands.json").write_text(json.dumps(registros, indent=2), encoding="utf-8")
        return texto

    def build(label):
        return roda(label, ["dotnet", "build", PROJETO, "-c", "Release", "--nologo", "-p:DeployToBepInEx=false"], 0)

    def rodar_teste(label, teste, esperado):
        return roda(label, ["dotnet", DLL, teste], esperado, ("FAIL|" + teste) if esperado else "Ran 1 tests; failures=0")

    # O preflight offline dos DOIS projetos novos (mesmo alvo Kit13OfflinePreflight dos outros do kit).
    for nome, projeto in (("api-bridge", "ApiBridge/ApiBridge.csproj"), ("api-bridge-harness", "ApiBridgeHarness/ApiBridgeHarness.csproj")):
        roda("preflight-negado-" + nome, ["dotnet", "msbuild", projeto, "-t:Kit13OfflinePreflight", "-p:DeployToBepInEx=true", "-nologo"], 1, "KIT13:")
        roda("preflight-seguro-" + nome, ["dotnet", "msbuild", projeto, "-t:Kit13OfflinePreflight", "-p:DeployToBepInEx=false", "-nologo"], 0)

    suite = build("build-baseline")
    texto = roda("suite-baseline", ["dotnet", DLL], 0)
    if "Ran 17 tests; failures=0" not in texto:
        raise RuntimeError("baseline da suite nao e o esperado")

    resultados = []
    for caso, relativo, substituicoes, testes in MUTACOES:
        caminho = kit / relativo
        original = caminho.read_bytes()
        texto_fonte = original.decode("utf-8")
        for antigo, novo in substituicoes:
            if texto_fonte.count(antigo) != 1:
                raise RuntimeError("mutacao nao unica em " + caso + ": " + antigo[:60])
            texto_fonte = texto_fonte.replace(antigo, novo)
        antes = lib.sha256_bytes(original)
        for teste in testes:
            rodar_teste(caso + "-baseline-" + teste, teste, 0)
        try:
            caminho.write_text(texto_fonte, encoding="utf-8", newline="")
            build(caso + "-build-mutante")
            for teste in testes:
                rodar_teste(caso + "-RED-" + teste, teste, 1)
        finally:
            caminho.write_bytes(original)
            build(caso + "-build-restaurado")
        for teste in testes:
            rodar_teste(caso + "-restaurado-" + teste, teste, 0)
        depois = lib.sha256_file(str(caminho))
        if depois != antes:
            raise RuntimeError("restauracao nao identica em " + caso)
        resultados.append({"caso": caso, "fonte": relativo,
                           "substituicoes": [{"de": a, "para": b} for a, b in substituicoes],
                           "testes_vermelhos": testes, "baseline": 0, "mutante": 1, "restaurado": 0,
                           "sha256_antes": antes, "sha256_restaurado": depois})
        (out / "mutations.json").write_text(json.dumps(resultados, indent=2), encoding="utf-8")
        print("RED_PROVED|" + caso + "|0->1->0|" + ",".join(testes))

    suite_final = roda("suite-final", ["dotnet", DLL], 0)
    vivo = [p for p, digest in baseline.items() if lib.sha256_file(str(ROOT / p)) != digest]
    copia = [p for p, digest in baseline.items() if lib.sha256_file(str(sandbox / p)) != digest]
    verificacao = {"arquivos": len(baseline), "live_changed": vivo, "sandbox_divergente_do_baseline": copia,
                   "mutacoes": len(resultados),
                   "suite_final": "Ran 17 tests; failures=0" if "Ran 17 tests; failures=0" in suite_final else "DIVERGENTE",
                   "runtime_do_jogo": "NAO_EXERCITADO"}
    (out / "verification.json").write_text(json.dumps(verificacao, indent=2), encoding="utf-8")
    if vivo:
        raise RuntimeError("o fonte VIVO foi alterado: " + str(vivo))
    print("BRIDGE_MUTATIONS_PASSOU|" + str(len(resultados)) + "|" + str(out))


if __name__ == "__main__":
    main()
