#!/usr/bin/env python3
"""Metadados e dependencias: layout nao-raiz, lote e controles negativos.

Executar da raiz: python tools/testes/test_valida_pacotes.py
Somente stdlib; fixtures sinteticas fora do repo, sem DLL, build, rede ou ZIP.
"""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
from typing import Any


RAIZ = Path(__file__).resolve().parents[2]
TEAM = "DefRuivo_StolenRealmMods"
BEP = "BepInEx-BepInExPack-5.4.2305"
API = TEAM + "-RealmApi-0.1.0"
RSTV = "RoguelikeSkillTreeVisualizer"


def carregar(caminho, nome) -> Any:
    spec = importlib.util.spec_from_file_location(nome, caminho)
    assert spec is not None and spec.loader is not None
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


class Pacotes(unittest.TestCase):
    def setUp(self):
        temporarios = Path(os.environ.get("TMPDIR") or RAIZ / "scratch")
        temporarios.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="pacotes-", dir=temporarios)
        self.addCleanup(self.temp.cleanup)
        self.raiz = Path(self.temp.name)
        (self.raiz / "tools").mkdir()
        shutil.copy2(RAIZ / "tools/pack-thunderstore.py", self.raiz / "tools/pack-thunderstore.py")
        for pasta, nome, versao, deps in (
            ("api", "RealmApi", "0.1.0", [BEP]),
            (RSTV, RSTV, "0.3.4", [BEP, API]),
        ):
            alvo = self.raiz / pasta
            alvo.mkdir()
            self.escrever_manifest(pasta, {
                "name": nome, "version_number": versao,
                "website_url": "https://example.invalid", "description": "Fixture sintetica",
                "dependencies": deps,
            })
            (alvo / "README.md").write_text("- **Version:** " + versao + "\n", encoding="utf-8")
            (alvo / "CHANGELOG.md").write_text("## " + versao + "\n", encoding="utf-8")
            shutil.copy2(RAIZ / pasta / "icon.png", alvo / "icon.png")
        (self.raiz / RSTV / (RSTV + ".csproj")).write_text("DeployToBepInEx plugins", encoding="utf-8")
        self.cd = carregar(RAIZ / "tools/check_dependencias.py", "dep_pacotes_test")
        self.cd.RAIZ = str(self.raiz)
        self.cd.MODS_JSON = str(self.raiz / "sem-ledger.json")
        self.vp = carregar(RAIZ / ".github/scripts/valida_pacotes.py", "valida_pacotes_test")
        self.vp.RAIZ = str(self.raiz)
        self.vp._MAPA = None
        self.vp.VERSOES_DO_REPO, _ = self.vp.versoes_do_repo()
        self.vp.TEAM_DO_REPO = TEAM

    def escrever_manifest(self, pasta, dados):
        (self.raiz / pasta / "manifest.json").write_text(json.dumps(dados), encoding="utf-8")

    def alterar(self, pasta, **campos):
        p = self.raiz / pasta / "manifest.json"
        dados = json.loads(p.read_text(encoding="utf-8"))
        dados.update(campos)
        self.escrever_manifest(pasta, dados)

    def resolver(self, liberados=None, publicadas=None):
        return self.cd.resolver(self.cd.entradas_do_repo(),
                                {BEP} if publicadas is None else publicadas,
                                {RSTV, "RealmApi"} if liberados is None else liberados)

    def test_identidade_do_pacote_nao_da_pasta(self):
        nomes = {e["nome"] for e in self.cd.entradas_do_repo()}
        self.assertEqual(nomes, {"RealmApi", RSTV})
        self.assertEqual(self.vp.VERSOES_DO_REPO, {"RealmApi": "0.1.0", RSTV: "0.3.4"})

    def test_api_inedita_no_mesmo_lote_resolve_com_ordem(self):
        r = self.resolver()
        self.assertEqual(r["problemas"], [])
        self.assertLess(r["ordem"].index("RealmApi"), r["ordem"].index(RSTV))
        self.assertTrue(any("mesmo lote" in x for x in r["resolvidas"]))

    def test_gate_completo_sem_publicacao_da_api(self):
        with patch.object(self.vp, "carregar_dependencias", return_value=self.cd):
            with contextlib.redirect_stdout(io.StringIO()) as saida:
                codigo = self.vp.main()
        self.assertEqual(codigo, 0, saida.getvalue())
        self.assertIn("pacotes validados: 2 | com problema: 0", saida.getvalue())

    def test_api_publicada_continua_resolvendo(self):
        self.assertEqual(self.resolver(publicadas={BEP, API})["problemas"], [])

    def test_api_nao_liberada_reprova(self):
        r = self.resolver(liberados={RSTV})
        self.assertTrue(any("publicar:false" in x for x in r["problemas"]), r)

    def test_versao_inexistente_reprova(self):
        self.alterar(RSTV, dependencies=[BEP, TEAM + "-RealmApi-9.9.9"])
        self.assertTrue(self.resolver()["problemas"])
        erros, _ = self.vp.valida(RSTV)
        self.assertTrue(any("declara hoje 0.1.0" in x for x in erros), erros)

    def test_namespace_errado_reprova(self):
        self.alterar(RSTV, dependencies=[BEP, "OutroTeam-RealmApi-0.1.0"])
        erros, _ = self.vp.valida(RSTV)
        self.assertTrue(any("namespace" in x for x in erros), erros)

    def test_ciclo_de_ineditas_reprova(self):
        self.alterar("api", dependencies=[BEP, TEAM + "-" + RSTV + "-0.3.4"])
        self.assertEqual(set(self.resolver()["ciclo"]), {"RealmApi", RSTV})

    def test_metadados_validos_dos_dois_layouts(self):
        for pasta in ("api", RSTV):
            with self.subTest(pasta=pasta):
                self.assertEqual(self.vp.valida(pasta)[0], [])

    def test_nome_manifest_divergente_reprova(self):
        self.alterar("api", name="api")
        erros, _ = self.vp.valida("api")
        self.assertTrue(any("!= pacote 'RealmApi'" in x for x in erros), erros)

    def test_png_tamanho_errado_reprova(self):
        p = self.raiz / "api/icon.png"
        dados = bytearray(p.read_bytes())
        dados[16:20] = (128).to_bytes(4, "big")
        p.write_bytes(dados)
        self.assertTrue(any("128x256" in x for x in self.vp.valida("api")[0]))

    def test_arquivos_ausentes_reprovam(self):
        for arquivo in ("icon.png", "README.md", "CHANGELOG.md"):
            (self.raiz / "api" / arquivo).unlink()
        erros, _ = self.vp.valida("api")
        for arquivo in ("icon.png", "README.md", "CHANGELOG.md"):
            self.assertTrue(any(arquivo + " nao existe" in x for x in erros), erros)

    def test_manifest_invalido_reprova(self):
        (self.raiz / "api/manifest.json").write_text("{", encoding="utf-8")
        self.assertTrue(any("JSON valido" in x for x in self.vp.valida("api")[0]))

    def test_limites_e_dependencias_continuam_estritos(self):
        self.alterar("api", version_number="invalida", description="x" * 251,
                     dependencies=["invalida", BEP, BEP])
        erros, _ = self.vp.valida("api")
        for trecho in ("semver", "251 caracteres", "PRIMEIRA", "repetido", "formato"):
            self.assertTrue(any(trecho in x for x in erros), (trecho, erros))

    def test_retirar_dependencia_externa_publicada_reprova(self):
        self.alterar(RSTV, dependencies=[BEP, "Externo-Pacote-1.0.0"])
        self.assertEqual(self.resolver(publicadas={BEP, "Externo-Pacote-1.0.0"})["problemas"], [])
        self.assertTrue(self.resolver()["problemas"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
