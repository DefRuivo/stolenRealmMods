#!/usr/bin/env python3
"""KIT13 v1 packages: data only. Trusted host authorization is NEVER read from package.

CLI is deliberately OFFLINE: file source + KIT11 executor; no live game/actions/plugins.
Only Python stdlib required, no Hermes/AI/network/account.
"""
import argparse
import copy
import importlib.util
import json
import math
import re
from pathlib import Path

API_VERSION = "1.0.0"
MAX_BYTES = 65536
MAX_STEPS = 32
OPERATIONS = frozenset(("menu", "tela", "condicao"))


class PackageError(ValueError):
    pass


def _executor():
    path = Path(__file__).resolve().parents[1] / "kit11" / "executor.py"
    spec = importlib.util.spec_from_file_location("kit13_executor", path)
    if spec is None or spec.loader is None:
        raise PackageError("executor KIT11 indisponivel")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _keys(obj, required, where):
    if type(obj) is not dict or set(obj) != set(required):
        raise PackageError(where + ": campos obrigatorios/extras invalidos")


def _text(value, where, maximum=128):
    if type(value) is not str or not value.strip() or len(value) > maximum:
        raise PackageError(where + ": texto invalido")
    return value


def validate_package(package):
    _keys(package, ("schema", "api", "id", "adapter", "steps"), "pacote")
    if package["schema"] != "KIT13/scenario/1":
        raise PackageError("schema incompativel")
    if package["api"] != API_VERSION:
        raise PackageError("API_INCOMPATIVEL: esperado " + API_VERSION)
    for key in ("id", "adapter"):
        value = _text(package[key], key, 64)
        if not re.fullmatch(r"[a-z][a-z0-9.-]{0,63}", value):
            raise PackageError(key + ": identificador invalido")
    steps = package["steps"]
    if type(steps) is not list or not 1 <= len(steps) <= MAX_STEPS:
        raise PackageError("steps: limite 1..32")
    executor = _executor()  # consume the reviewed condition vocabulary, not a copied list
    seen = set()
    total = 0.0
    for step in steps:
        _keys(step, ("id", "op", "target", "timeout_s"), "passo")
        name = _text(step["id"], "passo.id", 64)
        if name in seen:
            raise PackageError("passo.id duplicado")
        seen.add(name)
        if type(step["op"]) is not str or step["op"] not in OPERATIONS:
            raise PackageError("operacao nao permitida")
        target = _text(step["target"], "passo.target")
        if step["op"] == "condicao" and target not in executor.CONDICOES_CONHECIDAS:
            raise PackageError("condicao desconhecida pelo KIT11")
        timeout = step["timeout_s"]
        if type(timeout) not in (int, float) or not 0 < timeout <= 60 or not math.isfinite(timeout):
            raise PackageError("timeout_s: finito, numerico, >0 e <=60")
        total += timeout
    if total > 120:
        raise PackageError("orcamento total excede 120s")
    return copy.deepcopy(package)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise PackageError("chave JSON duplicada: " + key)
        result[key] = value
    return result


def load_package(path):
    # Bounded read avoids loading an arbitrarily large file before checking its size.
    with open(path, "rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise PackageError("pacote excede 65536 bytes")
    try:
        package = json.loads(data.decode("utf-8"), object_pairs_hook=_pairs,
                             parse_constant=lambda value: (_ for _ in ()).throw(PackageError("numero JSON invalido")))
    except (UnicodeError, ValueError, RecursionError) as error:
        raise PackageError("JSON invalido: " + type(error).__name__) from error
    return validate_package(package)


def to_plan(package, *, adapter, observe_authorized=False):
    package = validate_package(package)
    if type(observe_authorized) is not bool:
        raise PackageError("autorizacao do host deve ser bool")
    if adapter != package["adapter"]:
        raise PackageError("ADAPTER_INCOMPATIVEL: esperado " + package["adapter"])
    return {"esquema": "KIT-11/executor/1", "versao": 1, "modo": "observacao",
            "autorizacao": {"observacao_autorizada": observe_authorized, "ativa_autorizada": False},
            "passos": [{"nome": s["id"], "tipo": s["op"], "alvo": s["target"],
                        "timeout_s": s["timeout_s"], "requer_acao": False} for s in package["steps"]]}


def run_offline(package, state_file, lock_file, *, observe_authorized=False):
    plan = to_plan(package, adapter="offline-file.v1", observe_authorized=observe_authorized)
    executor = _executor()
    result = executor.executar(plan, executor.FonteDeArquivo(str(state_file)),
                               frente=executor.FrenteUnica(str(lock_file)), intervalo_s=0.005)
    # A file or fixture is not game runtime evidence even when executor reports OBSERVADO.
    result["runtime_exercitado"] = False
    result["kit13"] = {"api": API_VERSION, "package": package["id"], "source": "offline-file",
                       "qualification": "OFFLINE_ONLY"}
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package")
    parser.add_argument("state_file")
    parser.add_argument("--lock", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--allow-offline-observation", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = run_offline(load_package(args.package), args.state_file, args.lock,
                             observe_authorized=args.allow_offline_observation)
    except (OSError, PackageError) as error:
        result = {"veredito": "FALHOU_FECHADO", "runtime_exercitado": False,
                  "motivo": str(error), "kit13": {"api": API_VERSION, "qualification": "OFFLINE_ONLY"}}
    Path(args.output).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    verdict = result["veredito"]
    print("KIT13|" + verdict + "|OFFLINE_ONLY")
    return 2 if verdict == "NAO_EXERCITADO" else 0 if verdict in ("OBSERVADO", "PASSOU") else 1


if __name__ == "__main__":
    raise SystemExit(main())
