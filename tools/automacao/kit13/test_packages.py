import copy
import json
import tempfile
import unittest
from pathlib import Path

import packages as p

HERE = Path(__file__).resolve().parent


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.package = json.loads((HERE / "examples/menu.json").read_text(encoding="utf-8"))
        self.tmp = tempfile.TemporaryDirectory(prefix="kit13-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def reject(self, change):
        package = copy.deepcopy(self.package)
        change(package)
        with self.assertRaises(p.PackageError):
            p.validate_package(package)

    def test_version(self):
        self.reject(lambda x: x.update(api="2.0.0"))
        self.reject(lambda x: x.update(schema="KIT13/scenario/2"))

    def test_closed(self):
        for field in ("authorization", "autorizacao", "shell", "module", "assembly", "signature", "credentials", "ativa_autorizada"):
            with self.subTest(field=field):
                self.reject(lambda x: x.update({field: True}))
        self.reject(lambda x: x["steps"][0].update(command="not executed"))
        self.reject(lambda x: x["steps"][0].pop("target"))

    def test_operations(self):
        for op in ("click", "exec", "salvar", None, {}, "menu\n"):
            with self.subTest(op=op):
                self.reject(lambda x: x["steps"][0].update(op=op))
        self.reject(lambda x: x["steps"][0].update(op="condicao", target="invented"))

    def test_timeouts(self):
        for timeout in (True, "0.1", 0, -1, float("nan"), float("inf"), 61, 10 ** 400, None):
            with self.subTest(timeout=timeout):
                self.reject(lambda x: x["steps"][0].update(timeout_s=timeout))
        self.reject(lambda x: x.update(steps=[dict(x["steps"][0], id=str(i), timeout_s=60) for i in range(3)]))

    def test_steps(self):
        self.reject(lambda x: x.update(steps=[]))
        self.reject(lambda x: x.update(steps=[dict(x["steps"][0], id=str(i)) for i in range(33)]))
        self.reject(lambda x: x["steps"].append(copy.deepcopy(x["steps"][0])))

    def test_text(self):
        for field, value in (("id", "../evil"), ("adapter", "module.py" + "!"), ("id", "a" * 65)):
            with self.subTest(field=field, value=value):
                self.reject(lambda x: x.update({field: value}))
        self.reject(lambda x: x["steps"][0].update(target=" " * 2))
        self.reject(lambda x: x["steps"][0].update(target="a" * 129))

    def test_json(self):
        bad = self.root / "bad.json"
        duplicate = json.dumps(self.package)[:-1] + ',"id":"example.menu"}'
        for text in (duplicate, '{"x": NaN}', '{"x": Infinity}', '{'):
            with self.subTest(text=text):
                bad.write_text(text, encoding="utf-8")
                with self.assertRaises(p.PackageError):
                    p.load_package(bad)
        bad.write_bytes(b"\xff")
        with self.assertRaises(p.PackageError):
            p.load_package(bad)

    def test_size(self):
        bad = self.root / "big.json"
        bad.write_text(json.dumps(self.package) + " " * p.MAX_BYTES, encoding="utf-8")
        with self.assertRaises(p.PackageError):
            p.load_package(bad)

    def test_adapter(self):
        with self.assertRaises(p.PackageError):
            p.to_plan(self.package, adapter="other-game.v1", observe_authorized=True)

    def test_host_permission(self):
        with self.assertRaises(p.PackageError):
            p.to_plan(self.package, adapter="offline-file.v1", observe_authorized="false")  # type: ignore[arg-type] -- intentional malformed host input
        plan = p.to_plan(self.package, adapter="offline-file.v1", observe_authorized=True)
        self.assertFalse(plan["autorizacao"]["ativa_autorizada"])
        self.assertFalse(plan["passos"][0]["requer_acao"])
        self.assertEqual(plan["modo"], "observacao")

    def test_denied(self):
        result = p.run_offline(self.package, self.root / "missing", self.root / "lock")
        self.assertEqual(result["veredito"], "NAO_EXERCITADO")
        self.assertEqual(result["passos"], [])
        self.assertFalse((self.root / "lock").exists())

    def test_positive(self):
        result = p.run_offline(self.package, HERE / "examples/state.json", self.root / "lock", observe_authorized=True)
        self.assertEqual(result["veredito"], "OBSERVADO")
        self.assertEqual(result["passos"][0]["alvo"], "MainMenu")
        self.assertFalse(result["runtime_exercitado"])
        self.assertFalse((self.root / "lock").exists())

    def test_missing(self):
        result = p.run_offline(self.package, self.root / "missing", self.root / "lock", observe_authorized=True)
        self.assertEqual(result["veredito"], "FALHOU")
        self.assertIn("ausente", result["passos"][0]["diagnostico"])
        self.assertFalse(result["runtime_exercitado"])

    def test_switch(self):
        before = (HERE / "packages.py").read_bytes()
        a = p.run_offline(self.package, HERE / "examples/state.json", self.root / "lock", observe_authorized=True)
        b = p.run_offline(p.load_package(HERE / "examples/skills.json"), HERE / "examples/state.json", self.root / "lock", observe_authorized=True)
        self.assertEqual((a["passos"][0]["alvo"], b["passos"][0]["alvo"]), ("MainMenu", "Skills"))
        self.assertEqual(before, (HERE / "packages.py").read_bytes())


if __name__ == "__main__":
    unittest.main(verbosity=2)
