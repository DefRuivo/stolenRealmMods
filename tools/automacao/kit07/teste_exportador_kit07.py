#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KIT-07 - suite de testes do exportador (unittest, offline).

Roda sem jogo, sem save real, sem rede. Cada verificacao aqui e um caminho
POSITIVO ou o exercicio de uma trave; os defeitos plantados (controle negativo)
ficam em `contra_prova_kit07.py` e TEM de reprovar.

Credencial usada: FICTICIA, montada por concatenacao (nunca literal no arquivo),
sem valor real. Exigimos que nem o VALOR nem o PREFIXO da credencial apareca em
stdout, stderr, manifest.json ou relatorio.

Uso:  python tools/automacao/kit07/teste_exportador_kit07.py
Exit: 0 = verde; 1 = alguma verificacao reprovou; 2 = infraestrutura ausente.
"""
import json
import os
import shutil
import subprocess
import sys
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, "tools", "automacao", "offline"))

import exportador  # noqa: E402
import aut3_lib  # noqa: E402

# Credencial FICTICIA montada por partes: nenhum valor real, nenhum literal.
TOKEN = "tss_" + "A1b2C3d4" + "E5f6G7h8" + "I9j0K1l2M3n4O5p6"
PREFIXO = TOKEN[:12]
SEGREDO_ASSIGN = "Super" + "Secret" + "Value123456"          # password: X
USUARIO_RUIDO = "C:\\Users\\Fulano" + "DeTal"
EMAIL_RUIDO = "fulano" + "@" + "example.com"
IP_RUIDO = "192.168." + "0.10"

BASE = None


def _base():
    global BASE
    if BASE is None:
        BASE = os.path.join(aut3_lib.area_trabalho(), "kit07-suite")
        shutil.rmtree(BASE, ignore_errors=True)
        os.makedirs(BASE)
    return BASE


def _novo(nome):
    caminho = os.path.join(_base(), nome)
    shutil.rmtree(caminho, ignore_errors=True)
    os.makedirs(caminho)
    return caminho


def _escreve(caminho, texto, binario=False):
    with open(caminho, "wb" if binario else "w",
              **(dict() if binario else dict(encoding="utf-8"))) as fh:
        fh.write(texto)


def _origem_com_eventos():
    origem = _novo("origem")
    _escreve(os.path.join(origem, "eventos.json"), json.dumps({
        "evento": "clique_recebido",
        "token": TOKEN,
        "password": SEGREDO_ASSIGN,
        "caminho_log": USUARIO_RUIDO + "\\AppData\\Local\\Stolen Realm\\Player.log",
        "contato": EMAIL_RUIDO,
        "host": IP_RUIDO,
    }))
    _escreve(os.path.join(origem, "Player.log"),
             "login token=%s\npath %s\n" % (TOKEN, USUARIO_RUIDO))
    return origem


class TesteExportador(unittest.TestCase):

    def test_exclui_save_e_assembly(self):
        origem = _origem_com_eventos()
        _escreve(os.path.join(origem, "slot1.sav"), "save binario")
        _escreve(os.path.join(origem, "Assembly-CSharp.dll"), b"\x00dll", binario=True)
        _escreve(os.path.join(origem, "UnityEngine.CoreModule.dll"), b"\x00dll", binario=True)
        os.makedirs(os.path.join(origem, "saves"))
        _escreve(os.path.join(origem, "saves", "auto.json"), "{}")
        destino = os.path.join(_base(), "pkg-save")
        man = exportador.montar_pacote(origem, destino)
        incluidos = {a["caminho"] for a in man["arquivos"]}
        self.assertIn("eventos.json", incluidos)
        self.assertNotIn("slot1.sav", incluidos)
        self.assertNotIn("Assembly-CSharp.dll", incluidos)
        motivos = {}
        for item in man["excluidos"]:
            motivos.setdefault(item["motivo"], []).append(item["caminho"])
        self.assertIn("slot1.sav", motivos.get("save", []))
        self.assertIn("Assembly-CSharp.dll", motivos.get("assembly_proprietario", []))
        self.assertFalse(os.path.exists(os.path.join(destino, "slot1.sav")))

    def test_png_desligado_por_padrao(self):
        origem = _origem_com_eventos()
        _escreve(os.path.join(origem, "quadro.png"), b"\x89PNG\r\n", binario=True)
        destino = os.path.join(_base(), "pkg-png-off")
        man = exportador.montar_pacote(origem, destino)
        self.assertNotIn("quadro.png", {a["caminho"] for a in man["arquivos"]})
        excl = {i["caminho"]: i["motivo"] for i in man["excluidos"]}
        self.assertEqual(excl.get("quadro.png"), "png_opt_in")
        self.assertIn("quadro.png", man["diagnostico"]["png_para_revisao"])
        self.assertTrue(man["diagnostico"]["avisos"])

    def test_png_ligado_marca_como_nao_sanitizado(self):
        origem = _origem_com_eventos()
        _escreve(os.path.join(origem, "quadro.png"), b"\x89PNG\r\ndados", binario=True)
        destino = os.path.join(_base(), "pkg-png-on")
        man = exportador.montar_pacote(
            origem, destino, exportador.PoliticaExportacao(incluir_png=True))
        item = [a for a in man["arquivos"] if a["caminho"] == "quadro.png"][0]
        self.assertFalse(item["sanitizado"])
        self.assertIn("aviso", item)

    def test_sanitiza_segredo_ficticio_no_json_e_log(self):
        origem = _origem_com_eventos()
        destino = os.path.join(_base(), "pkg-sanit")
        man = exportador.montar_pacote(origem, destino)
        for nome in ("eventos.json", "Player.log"):
            caminho = os.path.join(destino, nome)
            with open(caminho, encoding="utf-8") as fh:
                texto = fh.read()
            self.assertNotIn(TOKEN, texto, "%s vazou o valor" % nome)
            self.assertNotIn(PREFIXO, texto, "%s vazou o prefixo" % nome)
        item = [a for a in man["arquivos"] if a["caminho"] == "eventos.json"][0]
        self.assertTrue(item["sanitizado"])

    def test_minimiza_pessoal(self):
        origem = _origem_com_eventos()
        destino = os.path.join(_base(), "pkg-pessoal")
        exportador.montar_pacote(origem, destino)
        with open(os.path.join(destino, "eventos.json"), encoding="utf-8") as fh:
            texto = fh.read()
        self.assertNotIn(USUARIO_RUIDO, texto)
        self.assertNotIn(EMAIL_RUIDO, texto)
        self.assertNotIn(IP_RUIDO, texto)
        self.assertIn("<USUARIO>", texto)
        self.assertIn("<EMAIL>", texto)

    def test_manifest_hash_confere(self):
        origem = _origem_com_eventos()
        destino = os.path.join(_base(), "pkg-hash")
        man = exportador.montar_pacote(origem, destino)
        for item in man["arquivos"]:
            caminho = os.path.join(destino, *item["caminho"].split("/"))
            self.assertTrue(os.path.isfile(caminho))
            self.assertEqual(aut3_lib.sha256_file(caminho), item["sha256"])
            self.assertEqual(os.path.getsize(caminho), item["bytes"])

    def test_origem_intacta(self):
        origem = _origem_com_eventos()
        antes = aut3_lib.sha256_file(os.path.join(origem, "eventos.json"))
        exportador.montar_pacote(origem, os.path.join(_base(), "pkg-origem"))
        depois = aut3_lib.sha256_file(os.path.join(origem, "eventos.json"))
        self.assertEqual(antes, depois)

    def test_sem_upload_na_fonte(self):
        with open(exportador.__file__, encoding="utf-8") as fh:
            fonte = fh.read()
        for proibido in ("import socket", "import urllib", "import requests",
                         "import http.client", "urlopen", "ftplib"):
            self.assertNotIn(proibido, fonte, "fonte contem %r" % proibido)
        self.assertFalse(exportador.PoliticaExportacao().para_dict()["permitir_upload"])
        with self.assertRaises(exportador.ErroExportacao):
            exportador.montar_pacote(
                os.path.dirname(exportador.__file__), os.path.join(_base(), "x"),
                exportador.PoliticaExportacao(permitir_upload=True))

    def test_limite_por_arquivo(self):
        origem = _novo("origem-limite")
        _escreve(os.path.join(origem, "grande.json"), "x" * 5000)
        destino = os.path.join(_base(), "pkg-lim")
        man = exportador.montar_pacote(
            origem, destino, exportador.PoliticaExportacao(max_bytes_por_arquivo=1000))
        self.assertEqual(man["diagnostico"]["incluidos"], 0)
        self.assertEqual(man["excluidos"][0]["motivo"], "excede_limite_por_arquivo")
        self.assertFalse(os.path.exists(os.path.join(destino, "grande.json")))

    def test_limite_total(self):
        origem = _novo("origem-total")
        _escreve(os.path.join(origem, "a.json"), "a" * 700)
        _escreve(os.path.join(origem, "b.json"), "b" * 700)
        with self.assertRaises(exportador.ErroExportacao):
            exportador.montar_pacote(
                origem, os.path.join(_base(), "pkg-total"),
                exportador.PoliticaExportacao(max_total_bytes=1000))

    def test_binario_desconhecido_excluido(self):
        origem = _novo("origem-bin")
        _escreve(os.path.join(origem, "texto.json"), "{}")
        _escreve(os.path.join(origem, "segredo.dat"), b"\x00\x01\x02", binario=True)
        destino = os.path.join(_base(), "pkg-bin")
        man = exportador.montar_pacote(origem, destino)
        excl = {i["caminho"]: i["motivo"] for i in man["excluidos"]}
        self.assertEqual(excl.get("segredo.dat"), "formato_binario_desconhecido")

    def test_nao_sobrescreve_destino_alheio(self):
        origem = _origem_com_eventos()
        destino = _novo("destino-alheio")
        _escreve(os.path.join(destino, "meu.txt"), "nao me apague")
        with self.assertRaises(exportador.ErroExportacao):
            exportador.montar_pacote(origem, destino)
        self.assertTrue(os.path.isfile(os.path.join(destino, "meu.txt")))

    def test_exclusao_segura_recusa_fora_e_apaga_pacote(self):
        comuns = _novo("dir-comum")
        _escreve(os.path.join(comuns, "arquivo.txt"), "x")
        with self.assertRaises(exportador.ErroExportacao):
            exportador.limpar_temporarios(comuns)
        self.assertTrue(os.path.isfile(os.path.join(comuns, "arquivo.txt")))

        origem = _origem_com_eventos()
        destino = os.path.join(_base(), "pkg-limpar")
        exportador.montar_pacote(origem, destino)
        removidos = exportador.limpar_temporarios(destino)
        self.assertTrue(removidos)
        self.assertFalse(os.path.exists(destino))
        # a origem continua intacta
        self.assertTrue(os.path.isfile(os.path.join(origem, "eventos.json")))

    def test_cli_nao_vaza_prefixo(self):
        origem = _origem_com_eventos()
        destino = os.path.join(_base(), "pkg-cli")
        proc = subprocess.run(
            [sys.executable, exportador.__file__, "--origem", origem, "--destino", destino],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, encoding="utf-8", errors="replace")
        self.assertEqual(proc.returncode, 0, proc.stderr)
        saidas = {"stdout": proc.stdout, "stderr": proc.stderr}
        for nome in ("manifest.json", "relatorio.md"):
            with open(os.path.join(destino, nome), encoding="utf-8") as fh:
                saidas[nome] = fh.read()
        # Todo arquivo TEXTUAL empacotado tambem e saida: nada de segredo no conteudo.
        for raiz, _dirs, arquivos in os.walk(destino):
            for nome in arquivos:
                if os.path.splitext(nome)[1].lower() in exportador.EXT_TEXTO:
                    caminho = os.path.join(raiz, nome)
                    with open(caminho, encoding="utf-8") as fh:
                        saidas[os.path.relpath(caminho, destino)] = fh.read()
        for rotulo, texto in saidas.items():
            self.assertNotIn(TOKEN, texto, "%s vazou valor" % rotulo)
            self.assertNotIn(PREFIXO, texto, "%s vazou prefixo" % rotulo)
            self.assertNotIn(SEGREDO_ASSIGN, texto, "%s vazou segredo de atribuicao" % rotulo)


def _roda():
    carregador = unittest.TestLoader()
    suite = carregador.loadTestsFromTestCase(TesteExportador)
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if resultado.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(_roda())
