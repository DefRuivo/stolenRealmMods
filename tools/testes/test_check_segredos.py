#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Regressao ORG-PRE-SEG: gramaticas publicas nao isentam credenciais.

Uso offline: python -B tools/testes/test_check_segredos.py
Somente biblioteca padrao. Scanners REAIS em repos Git temporarios; nenhum
valor real e utilizado. Iscas sinteticas montadas, nunca impressas.
"""
import hashlib
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('cps_org_seg', TOOLS / 'check_padroes_segredo.py')
if spec is None or spec.loader is None:
    raise RuntimeError('scanner generico nao localizado')
cps = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cps)
# Partes curtas: o proprio fonte nao contem uma credencial literal/iscas longas.
OPACO = 'A1b2C3d4E5f6G7h8' + 'I9j0K1l2M3n4O5p6' + 'Q7r8S9t0'
HEX = hashlib.sha256(b'fixture-publica-org-pre-seg').hexdigest()
SESSAO = 'AUT4-' + '20261009-185146-' + 'abcd1234'
MARCADOR = 'AUT4-IDA-E-VOLTA-' + SESSAO
CRITERIO = 'KIT09-RSTV25b-' + 'sem-aresta-inventada'
ENSAIO = 'm10-publicacao-' + 'propaga-excecao-baseline-P15'
KIT14 = 'KIT14-run704-' + 'without-passive-readonly-' + '20261009-185146'
PUBLICOS = [SESSAO, 'sessao=' + SESSAO, MARCADOR, MARCADOR + '-CORPO',
            CRITERIO, ENSAIO, KIT14, 'RESTORED_SHA=' + HEX,
            'sha256Alvo=' + HEX, 'SHA256' + HEX]


def formatos_sinteticos():
    casos = [('github_pat', 'github_' + 'pat_' + OPACO)]
    casos += [('github_' + letra, 'gh' + letra + '_' + OPACO) for letra in 'pousr']
    casos += [('thunderstore', 'ts' + 's_' + OPACO),
              ('slack', 'xo' + 'xb-' + OPACO),
              ('openai', 's' + 'k-' + OPACO),
              ('aws', 'AK' + 'IA' + '0123456789ABCDEF'),
              ('google', 'AI' + 'za' + OPACO[:35]),
              ('gitlab', 'gl' + 'pat-' + OPACO),
              ('npm', 'np' + 'm_' + OPACO[:36]),
              ('private_key', '-----BEGIN RSA PRIVATE KEY-----\n' + OPACO * 2),
              ('url_push', 'x-access-' + 'token:' + OPACO),
              ('basic', 'Basic ' + OPACO),
              ('assignment', 'token = ' + OPACO)]
    return casos


class Gramaticas(unittest.TestCase):
    def test_limites_inalterados(self):
        self.assertEqual(cps.LIMIAR_ENTROPIA, 4.0)
        self.assertEqual(cps.LIMIAR_COMPRIMENTO, 32)
        self.assertEqual(cps.CANDIDATO.pattern, r'[A-Za-z0-9_\-+/=]{32,}')
        self.assertEqual(cps.ISENTOS, {
            'tools/check_segredos.py', 'tools/check_padroes_segredo.py',
            'docs/AMBIENTE.md', 'docs/README.md', 'docs/CI.md', 'docs/PUBLICACAO.md'})

    def test_publicos(self):
        for i, v in enumerate(PUBLICOS):
            with self.subTest(caso=i):
                self.assertIsNotNone(cps.classificar_dado_publico(v))
                self.assertFalse(cps.parece_segredo(v))

    def test_token_sem_prefixo(self):
        self.assertGreaterEqual(cps.entropia(OPACO), 4.0)
        self.assertIsNone(cps.classificar_dado_publico(OPACO))
        self.assertTrue(cps.parece_segredo(OPACO))

    def test_prefixo_sufixo_nao_herdam_excecao(self):
        for i, v in enumerate(PUBLICOS):
            for j, clone in enumerate((OPACO + v, v + OPACO, v + '-' + OPACO)):
                with self.subTest(caso=i, mutacao=j):
                    self.assertIsNone(cps.classificar_dado_publico(clone))
                    self.assertTrue(cps.parece_segredo(clone))

    def test_datas_horas_e_nonce_invalidos(self):
        casos = [SESSAO.replace('20261009', '20260230'),
                 SESSAO.replace('185146', '245146'),
                 SESSAO[:-1] + 'Z', SESSAO + 'f', SESSAO[:-1],
                 KIT14.replace('20261009', '20261309'),
                 KIT14.replace('185146', '186146'),
                 KIT14.replace('readonly', 'unknown'),
                 KIT14.replace('run704', 'run7040'),
                 CRITERIO + '-outro', ENSAIO.replace('P15', 'P16')]
        for i, v in enumerate(casos):
            with self.subTest(caso=i):
                self.assertIsNone(cps.classificar_dado_publico(v))

    def test_hash_so_com_rotulos_exatos(self):
        for i, v in enumerate(('SHA256' + OPACO, 'RESTORED_SHA=' + OPACO,
                                'sha256Alvo=' + OPACO, 'hash=' + OPACO,
                                'token=' + HEX, 'SHA256' + HEX[:-1],
                                'SHA256' + HEX + 'f')):
            with self.subTest(caso=i):
                self.assertIsNone(cps.classificar_dado_publico(v))
        for i, v in enumerate(('SHA256' + OPACO, 'RESTORED_SHA=' + OPACO,
                                'sha256Alvo=' + OPACO)):
            with self.subTest(opaco=i):
                self.assertTrue(cps.parece_segredo(v))

    def test_mascara_sem_valor_nem_prefixo(self):
        msg = cps.mascara(OPACO)
        self.assertNotIn(OPACO, msg)
        self.assertNotIn(OPACO[:14], msg)
        self.assertIn('<REDACTED>', msg)


class ScannersReais(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='org-pre-seg-', dir=os.environ.get('TMPDIR'))
        cls.root = Path(cls.temp.name)
        (cls.root / 'tools').mkdir()
        for nome in ('check_segredos.py', 'check_padroes_segredo.py'):
            shutil.copyfile(TOOLS / nome, cls.root / 'tools' / nome)
        subprocess.run(['git', 'init', '-q'], cwd=cls.root, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cls.alvo = cls.root / 'docs' / 'automacao' / 'prova.txt'
        cls.alvo.parent.mkdir(parents=True)
        cls.alvo.write_text('sem segredo\n', encoding='utf-8')
        subprocess.run(['git', 'add', '--', 'docs/automacao/prova.txt'], cwd=cls.root,
                       check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    @classmethod
    def tearDownClass(cls):
        # Git Windows deixa arquivos read-only; TemporaryDirectory trata isso.
        cls.temp.cleanup()

    def rodar(self, bruto, esperado, valores=()):
        self.alvo.write_bytes(bruto)
        for scanner in ('check_segredos.py', 'check_padroes_segredo.py'):
            r = subprocess.run([sys.executable, '-B', str(self.root / 'tools' / scanner)],
                               cwd=self.root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               timeout=30)
            out = (r.stdout + r.stderr).decode('utf-8', 'replace')
            # Nao incluir stdout/dados/valores no erro de teste.
            self.assertEqual(r.returncode, esperado, msg='scanner=%s exit=%s' % (scanner, r.returncode))
            for v in valores:
                self.assertNotIn(v, out, msg='saida nao pode expor a isca')
                self.assertNotIn(v[:14], out, msg='saida nao pode expor prefixo da isca')
        return out

    def test_cli_publicos_verdes(self):
        self.rodar(('\n'.join(PUBLICOS) + '\n').encode(), 0)

    def test_cli_sem_prefixo_em_docs_e_mascarado(self):
        out = self.rodar(('valor = ' + OPACO).encode(), 1, (OPACO,))
        self.assertIn('ENTROPIA', out)
        self.assertIn('<REDACTED>', out)

    def test_cli_formatos_conhecidos(self):
        for label, v in formatos_sinteticos():
            with self.subTest(formato=label):
                # Header PEM nao e um prefixo de valor secreto; o corpo e a isca.
                self.rodar(v.encode(), 1, (OPACO,))

    def test_cli_publico_nao_isenta_vizinho(self):
        for i, v in enumerate(PUBLICOS):
            with self.subTest(caso=i):
                self.rodar((v + '\nvalor = ' + OPACO).encode(), 1, (OPACO,))

    def test_cli_publico_em_atribuicao_secreta_reprova(self):
        for i, v in enumerate(PUBLICOS):
            with self.subTest(caso=i):
                self.rodar(('token = "' + v + '"').encode(), 1)

    def test_cli_publico_em_campo_json_reprova(self):
        for i, v in enumerate(PUBLICOS):
            # So candidatos de 32+ recebem a nova excecao no scanner. A sessao
            # AUT4 nua tem 29 chars, fora do heuristico anterior e deste patch.
            if len(v) < cps.LIMIAR_COMPRIMENTO:
                continue
            with self.subTest(caso=i):
                self.rodar(('{"secret": "' + v + '"}').encode(), 1)

    def test_cli_formato_conhecido_em_binario(self):
        v = 'ts' + 's_' + OPACO
        self.rodar(b'\x00\xff' + v.encode() + b'\x00', 1, (v,))

    def test_cli_verde_apos_remocao(self):
        self.rodar(('valor = ' + OPACO).encode(), 1, (OPACO,))
        self.rodar(b'sem segredo\n', 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
