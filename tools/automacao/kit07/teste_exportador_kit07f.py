#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KIT-07F - testes ADICIONAIS do exportador (offline, sem rede e sem jogo).

Cobre o que a suite original nao cobria: NOME de arquivo excluido e PNG saneados
no caminho fisico e no manifesto (F1), COLISAO de nomes mascarados, recusa por
CAMINHOS CANONICOS (origem == destino escrito de outra forma), TETOS contados em
bytes REAIS de saida (nao de entrada) sem deixar parcial, NOME RESERVADO sem
sobrescrever o input (F5), erros de I/O da CLI sem traceback e com exit distinto
(dominio=1 / infra=2), e log textual selecionado em segmento de binario (F9)
entrando sanitizado enquanto assembly/save seguem fora.

Credencial: FICTICIA, montada por concatenacao (nunca literal no arquivo).

O modulo sob teste pode ser trocado por KIT07F_MODULE=<caminho> - e assim que a
MESMA suite e mostrada REPROVANDO no modulo antigo (RED) e passando no corrigido.

Uso:  python tools/automacao/kit07/teste_exportador_kit07f.py
Exit: 0 = verde; 1 = alguma verificacao reprovou; 2 = infraestrutura ausente.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
MODULO = os.path.abspath(os.environ.get("KIT07F_MODULE")
                         or os.path.join(AQUI, "exportador.py"))
sys.path.insert(0, os.path.dirname(MODULO))
sys.path.insert(0, os.path.join(RAIZ, "tools", "automacao", "offline"))

import exportador as e  # noqa: E402

# Credenciais FICTICIAS montadas por partes (nenhum valor real, nenhum literal).
TOKEN_A = "tss_" + "Q9a2B5c8" * 4
TOKEN_B = "tss_" + "R7d3E6f1" * 4
PREFIXO_A = TOKEN_A[:12]
PREFIXO_B = TOKEN_B[:12]
SEGREDO = "Super" + "Secret" + "Value123456"

BASE = None


def _base():
    global BASE
    if BASE is None:
        base = os.environ.get("KIT07F_TMP") or tempfile.mkdtemp(prefix="kit07f-")
        BASE = os.path.join(base, "kit07f-suite")
        shutil.rmtree(BASE, ignore_errors=True)
        os.makedirs(BASE)
    return BASE


def _novo(nome):
    caminho = os.path.join(_base(), nome)
    shutil.rmtree(caminho, ignore_errors=True)
    os.makedirs(caminho)
    return caminho


def _escreve(caminho, dados):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    modo = "wb" if isinstance(dados, bytes) else "w"
    with open(caminho, modo, **({} if modo == "wb" else {"encoding": "utf-8"})) as fh:
        fh.write(dados)


def _politica(**kw):
    """Politica do modulo, com overhead zerado quando o modulo o suporta.

    O modulo ANTIGO nao conhece `overhead_bytes`: o teste continua valido la (a
    contagem antiga e por entrada) e o atributo extra nao vira TypeError.
    """
    pol = e.PoliticaExportacao()
    for chave, valor in kw.items():
        setattr(pol, chave, valor)
    if "overhead_bytes" in kw:
        setattr(pol, "overhead_bytes", kw["overhead_bytes"])
    return pol


def _cli(origem, destino, *extra):
    proc = subprocess.run(
        [sys.executable, MODULO, "--origem", origem, "--destino", destino, *extra],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        universal_newlines=True, encoding="utf-8", errors="replace", timeout=60)
    return proc


def _tamanho(pacote):
    total = 0
    for raiz, _dirs, arquivos in os.walk(pacote):
        for nome in arquivos:
            total += os.path.getsize(os.path.join(raiz, nome))
    return total


def _nomes_fisicos(raiz):
    return "\n".join(os.path.join(raiz, r, n).replace(os.sep, "/")
                     for r, _d, arqs in os.walk(raiz) for n in arqs)


class Adicionais(unittest.TestCase):

    # --- F1: nomes EXCLUIDOS tambem sao saida -------------------------------
    def test_nome_excluido_com_credencial_e_saneado(self):
        origem = _novo("f1-excluidos")
        _escreve(os.path.join(origem, "capture_%s.dll" % TOKEN_A), b"\x00dll")
        _escreve(os.path.join(origem, "saves_%s.txt" % TOKEN_B), "evento")
        _escreve(os.path.join(origem, "limpo.json"), '{"evento": "e1"}')
        destino = os.path.join(_base(), "f1-excluidos-out")
        man = e.montar_pacote(origem, destino)
        manifest_txt = open(os.path.join(destino, "manifest.json"), encoding="utf-8").read()
        blob = manifest_txt + "\n" + _nomes_fisicos(destino)
        for prefixo in (PREFIXO_A, PREFIXO_B):
            self.assertNotIn(prefixo, blob, "prefixo de credencial em nome excluido/metadata")

    def test_png_nome_com_credencial_saneado(self):
        origem = _novo("f1-png")
        _escreve(os.path.join(origem, "shot_%s.png" % TOKEN_A), b"\x89PNG\r\nsintetico")
        destino = os.path.join(_base(), "f1-png-out")
        man = e.montar_pacote(origem, destino)
        blob = json.dumps(man) + "\n" + _nomes_fisicos(destino)
        self.assertNotIn(PREFIXO_A, blob, "prefixo em nome de PNG/metadata")
        motivos = {i["motivo"] for i in man["excluidos"]}
        self.assertIn("png_opt_in", motivos)
        self.assertFalse(os.path.exists(os.path.join(destino, "shot_%s.png" % TOKEN_A)))

    # --- F1: colisao de nomes mascarados -----------------------------------
    def test_colisao_de_nomes_mascarados_distinta(self):
        origem = _novo("f1-colisao")
        _escreve(os.path.join(origem, "ev_%s.log" % TOKEN_A), "evento A")
        _escreve(os.path.join(origem, "ev_%s.log" % TOKEN_B), "evento B")
        destino = os.path.join(_base(), "f1-colisao-out")
        man = e.montar_pacote(origem, destino)
        self.assertEqual(len(man["arquivos"]), 2, "colisao perdeu um arquivo")
        caminhos = [a["caminho"] for a in man["arquivos"]]
        self.assertEqual(len(set(caminhos)), 2, "colisao gerou caminho repetido")
        for prefixo in (PREFIXO_A, PREFIXO_B):
            self.assertNotIn(prefixo, json.dumps(man), "prefixo sobreviveu apos colisao")
        conteudos = set()
        for item in man["arquivos"]:
            alvo = os.path.join(destino, *item["caminho"].split("/"))
            dados = open(alvo, "rb").read()
            self.assertEqual(hashlib.sha256(dados).hexdigest(), item["sha256"])
            self.assertEqual(len(dados), item["bytes"])
            conteudos.add(dados)
        self.assertEqual(conteudos, {b"evento A", b"evento B"})

    # --- F3: caminhos canonicos --------------------------------------------
    def test_paths_canonicos_iguais_recusa_sem_tocar_origem(self):
        dados = _novo("f3-dados")
        _escreve(os.path.join(dados, "evento.json"), json.dumps({"password": SEGREDO}))
        origem = os.path.join(_base(), "f3-canonico")
        e.montar_pacote(dados, origem)          # origem passa a ser um pacote VALIDO
        alvo = os.path.join(origem, "evento.json")
        antes = open(alvo, "rb").read()
        # destino canonico equivalente ao proprio pacote de origem
        destino = os.path.join(origem, "sub", "..")
        recusou = False
        try:
            e.montar_pacote(origem, destino)
        except e.ErroExportacao:
            recusou = True
        self.assertTrue(recusou, "origem escrita por destino canonico equivalente")
        self.assertEqual(open(alvo, "rb").read(), antes, "origem foi alterada")
        self.assertTrue(os.path.isfile(os.path.join(origem, e.MARCADOR)),
                        "a origem (pacote valido) foi consumida/alterada")

    def test_paths_canonicos_filho_recusado_sem_parcial(self):
        origem = _novo("f3-filho")
        _escreve(os.path.join(origem, "evento.json"), "{}")
        destino = os.path.join(origem, "nested", "out")
        with self.assertRaises(e.ErroExportacao):
            e.montar_pacote(origem, destino)
        self.assertFalse(os.path.exists(os.path.join(origem, "nested")))

    # --- F7: tetos em bytes REAIS de saida --------------------------------
    def test_teto_conta_bytes_reais_de_saida_sem_parcial(self):
        origem = _novo("f7-saida")
        _escreve(os.path.join(origem, "evento.txt"), "x" * 50)

        referencia = os.path.join(_base(), "f7-referencia")
        e.montar_pacote(origem, referencia)
        real = _tamanho(referencia)
        # O pacote REAL e dominado pela metadata (manifest/relatorio/marcador).
        self.assertGreater(real, 50 * 4, "pacote de referencia menor que a entrada")

        # Teto de 200 bytes: a ENTRADA (50) cabe; a SAIDA real (~1 kB) nao.
        # Contagem por entrada (modulo antigo) aceitaria e gravaria > teto.
        com_folga = os.path.join(_base(), "f7-folga")
        e.montar_pacote(origem, com_folga,
                        _politica(max_total_bytes=5000, overhead_bytes=0))
        self.assertLessEqual(_tamanho(com_folga), 5000)

        with self.assertRaises(e.ErroExportacao):
            e.montar_pacote(origem, com_folga,
                            _politica(max_total_bytes=200, overhead_bytes=0))

        # Recusa segura: SEM parcial novo e com o pacote anterior intacto.
        self.assertLessEqual(_tamanho(com_folga), 5000)
        self.assertTrue(os.path.isfile(os.path.join(com_folga, e.MARCADOR)),
                        "recusa apagou o pacote anterior")
        self.assertFalse(os.path.exists(com_folga + e._SUFIXO_TEMP),
                         "recusa deixou diretorio temporario para tras")

    def test_teto_por_arquivo_conta_saida_sanitizada(self):
        origem = _novo("f7-por-arquivo")
        texto = "a@b.co x@y.co"          # 13 bytes na entrada
        _escreve(os.path.join(origem, "evento.txt"), texto)
        destino = os.path.join(_base(), "f7-por-arquivo-out")
        # 14 bytes: a ENTRADA cabe; a SAIDA sanitizada (<EMAIL> <EMAIL>, 15) nao.
        man = e.montar_pacote(origem, destino, _politica(max_bytes_por_arquivo=14))
        motivos = {i["motivo"] for i in man["excluidos"]}
        self.assertIn("excede_limite_por_arquivo", motivos,
                      "teto por arquivo contou entrada, nao saida")
        self.assertFalse(os.path.exists(os.path.join(destino, "evento.txt")))
        self.assertEqual(man["diagnostico"]["incluidos"], 0)

    # --- F5: nome reservado nao sobrescreve input -------------------------
    def test_nome_reservado_nao_sobrescreve_input(self):
        origem = _novo("f5-reservado")
        _escreve(os.path.join(origem, "manifest.json"), json.dumps({"evento": "entrada"}))
        _escreve(os.path.join(origem, "relatorio.md"), "relatorio de entrada")
        destino = os.path.join(_base(), "f5-reservado-out")
        man = e.montar_pacote(origem, destino)
        self.assertEqual(len(man["arquivos"]), 2)
        for item in man["arquivos"]:
            alvo = os.path.join(destino, *item["caminho"].split("/"))
            dados = open(alvo, "rb").read()
            self.assertEqual(hashlib.sha256(dados).hexdigest(), item["sha256"])
            self.assertEqual(len(dados), item["bytes"])
        # o manifesto do pacote continua sendo o do exportador
        pacote_manifest = json.load(open(os.path.join(destino, "manifest.json"), encoding="utf-8"))
        self.assertEqual(pacote_manifest["kit"], e.KIT)

    # --- F8: erros de I/O da CLI ------------------------------------------
    def test_cli_destino_arquivo_exit_dominio_sem_traceback(self):
        origem = _novo("f8-arquivo")
        _escreve(os.path.join(origem, "evento.json"), "{}")
        destino = os.path.join(_base(), "destino-ocupado.txt")
        _escreve(destino, "arquivo ocupando o caminho do pacote")
        proc = _cli(origem, destino)
        self.assertEqual(proc.returncode, 1, "destino-arquivo nao e erro de DOMINIO (1)")
        self.assertNotIn("Traceback", proc.stdout + proc.stderr, "traceback bruto na CLI")
        self.assertIn("ERRO KIT-07", proc.stderr)

    def test_cli_origem_inexistente_exit2_sem_traceback(self):
        destino = os.path.join(_base(), "f8-sem-origem-out")
        proc = _cli(os.path.join(_base(), "nao-existe-mesmo"), destino)
        self.assertEqual(proc.returncode, 2)
        self.assertNotIn("Traceback", proc.stdout + proc.stderr)
        self.assertFalse(os.path.exists(destino))

    def test_cli_destino_alheio_exit1_sem_traceback(self):
        origem = _novo("f8-alheio")
        _escreve(os.path.join(origem, "evento.json"), "{}")
        destino = _novo("f8-alheio-destino")
        _escreve(os.path.join(destino, "meu.txt"), "nao me apague")
        proc = _cli(origem, destino)
        self.assertEqual(proc.returncode, 1)
        self.assertNotIn("Traceback", proc.stdout + proc.stderr)
        self.assertTrue(os.path.isfile(os.path.join(destino, "meu.txt")))

    # --- F9: log textual em segmento de binario ---------------------------
    def test_f9_log_bepinex_entra_e_assembly_sai(self):
        origem = _novo("f9-bepinex")
        _escreve(os.path.join(origem, "BepInEx", "LogOutput.log"),
                 "login token=%s\n" % TOKEN_A)
        _escreve(os.path.join(origem, "BepInEx", "Assembly-CSharp.dll"), b"\x00dll")
        _escreve(os.path.join(origem, "BepInEx", "config.json"), '{"evento": "e1"}')
        destino = os.path.join(_base(), "f9-bepinex-out")
        man = e.montar_pacote(origem, destino)
        incluidos = {a["caminho"] for a in man["arquivos"]}
        self.assertIn("BepInEx/LogOutput.log", incluidos)
        self.assertIn("BepInEx/config.json", incluidos)
        self.assertNotIn("BepInEx/Assembly-CSharp.dll", incluidos)
        motivos = {i["caminho"]: i["motivo"] for i in man["excluidos"]}
        self.assertEqual(motivos.get("BepInEx/Assembly-CSharp.dll"), "assembly_proprietario")
        texto = open(os.path.join(destino, "BepInEx", "LogOutput.log"), encoding="utf-8").read()
        self.assertNotIn(PREFIXO_A, texto, "log selecionado vazou prefixo")


def _roda():
    if not os.path.isfile(MODULO):
        sys.stderr.write("ERRO KIT-07F: modulo ausente: %s\n" % MODULO)
        return 2
    suite = unittest.TestLoader().loadTestsFromTestCase(Adicionais)
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if resultado.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(_roda())
