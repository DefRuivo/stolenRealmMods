#!/usr/bin/env python3
"""ORG-PRE-DOC: positivos e negativos reais da CLI, offline e stdlib.

Fixtures sintéticas declaradas; nenhuma ferramenta privada/jogo/perfil necessário.
    python tools/test_audita_docs.py -v
"""
import copy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from docs_proveniencia import ARQUIVO, SCHEMA, carregar, reconhece, sha_texto

TOOLS = Path(__file__).resolve().parent


def escrever(raiz, caminho, texto):
    alvo = raiz / caminho
    alvo.parent.mkdir(parents=True, exist_ok=True)
    alvo.write_text(texto, encoding='utf-8', newline='\n')


def registro(raiz, doc, linha, categoria, nome):
    texto = (raiz / doc).read_text(encoding='utf-8')
    return {'documento': doc, 'linha': linha, 'categoria': categoria, 'nome': nome,
            'sha256_documento': sha_texto(texto),
            'sha256_linha': sha_texto(texto.splitlines()[linha - 1]),
            'origem': 'workspace privado da rodada sintética (fixture)',
            'justificativa': 'Comando/log histórico preservado; não é instrução atual do clone.'}


def catalogo(raiz, itens):
    escrever(raiz, ARQUIVO, json.dumps({'schema': SCHEMA, 'ocorrencias': itens}, ensure_ascii=False))


class RegistroTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='audita-proveniencia-', dir=os.environ.get('TMPDIR'))
        self.addCleanup(self.tmp.cleanup)
        self.raiz = Path(self.tmp.name)
        self.doc = 'docs/automacao/rodada.md'
        escrever(self.raiz, self.doc, '# Fotografia da rodada\n\npython review_controls.py\n')
        self.item = registro(self.raiz, self.doc, 3, 'ferramenta-local', 'review_controls.py')
        self.itens = [self.item]

    def carregar(self):
        catalogo(self.raiz, self.itens)
        return carregar(self.raiz, [self.doc])

    def test_registro_exato_valido(self):
        itens, erros = self.carregar()
        self.assertEqual(erros, [])
        self.assertTrue(reconhece(itens, self.doc, 3, 'ferramenta-local', 'review_controls.py'))

    def test_nao_isenta_outra_linha_nome_classe_ou_documento(self):
        itens, erros = self.carregar()
        self.assertEqual(erros, [])
        for chave in [('docs/README.md', 3, 'ferramenta-local', 'review_controls.py'),
                      (self.doc, 4, 'ferramenta-local', 'review_controls.py'),
                      (self.doc, 3, 'caminho-historico', 'review_controls.py'),
                      (self.doc, 3, 'ferramenta-local', 'review_fake.py')]:
            with self.subTest(chave=chave):
                self.assertFalse(reconhece(itens, *chave))

    def test_documento_alterado_invalida(self):
        with (self.raiz / self.doc).open('a', encoding='utf-8') as out:
            out.write('\nInstrução nova e falsa.\n')
        itens, erros = self.carregar()
        self.assertFalse(itens)
        self.assertIn('snapshot ausente/alterado', erros[0])

    def test_hash_da_linha_alterado_reprova(self):
        self.item['sha256_linha'] = '0' * 64
        itens, erros = self.carregar()
        self.assertFalse(itens)
        self.assertIn('linha alterada', erros[0])

    def test_linha_fora_do_documento_reprova(self):
        self.item['linha'] = 999
        itens, erros = self.carregar()
        self.assertFalse(itens)
        self.assertIn('ocorrencia ausente', erros[0])

    def test_documento_nao_versionado_reprova(self):
        catalogo(self.raiz, self.itens)
        itens, erros = carregar(self.raiz, [])
        self.assertFalse(itens)
        self.assertTrue(erros)

    def test_duplicado_reprova_e_nao_reconhece(self):
        self.itens.append(copy.deepcopy(self.item))
        itens, erros = self.carregar()
        self.assertFalse(itens)
        self.assertIn('duplicado', erros[0])

    def test_identidades_malformadas_reprovam(self):
        for campo, valor in [('documento', '../escape.md'), ('linha', True),
                             ('linha', 0), ('categoria', 'arquivo-inteiro'),
                             ('sha256_documento', 'nao-hash'), ('origem', ''),
                             ('nome', ''), ('justificativa', None)]:
            with self.subTest(campo=campo, valor=valor):
                item = copy.deepcopy(self.item)
                item[campo] = valor
                self.itens = [item]
                itens, erros = self.carregar()
                self.assertFalse(itens)
                self.assertTrue(erros)

    def test_arquivo_ausente_reprova(self):
        itens, erros = carregar(self.raiz, [self.doc])
        self.assertFalse(itens)
        self.assertIn('registro ausente/ilegivel', erros[0])

    def test_json_invalido_reprova(self):
        escrever(self.raiz, ARQUIVO, '{')
        itens, erros = carregar(self.raiz, [self.doc])
        self.assertFalse(itens)
        self.assertTrue(erros)

    def test_schema_invalido_reprova(self):
        escrever(self.raiz, ARQUIVO, '{}')
        itens, erros = carregar(self.raiz, [self.doc])
        self.assertFalse(itens)
        self.assertTrue(erros)

    def test_crlf_e_lf_equivalentes(self):
        (self.raiz / self.doc).write_bytes((self.raiz / self.doc).read_bytes().replace(b'\n', b'\r\n'))
        itens, erros = self.carregar()
        self.assertEqual(erros, [])
        self.assertEqual(len(itens), 1)


class CliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='audita-cli-', dir=os.environ.get('TMPDIR'))
        self.addCleanup(self.tmp.cleanup)
        self.raiz = Path(self.tmp.name)
        (self.raiz / 'tools').mkdir()
        for nome in ('audita_docs.py', 'docs_proveniencia.py'):
            shutil.copyfile(TOOLS / nome, self.raiz / 'tools' / nome)
        # Fixture declarada: parser simulado só provê o formato necessário ao check 3.
        escrever(self.raiz, 'tools/check_dupes.py', "print('TextFixes 101 entradas | TextAppends 197 entradas')\n")
        escrever(self.raiz, 'docs/README.md', '### `cobertura/revisao/` - 0 relatorios\n\n'
                 '| Grupo | Arquivos | Nº |\n|---|---|---|\n')
        (self.raiz / 'docs/cobertura/revisao').mkdir(parents=True)
        catalogo(self.raiz, [])
        self.git('init', '--quiet')
        self.git('add', '--', 'tools/audita_docs.py', 'tools/docs_proveniencia.py',
                 'tools/check_dupes.py', ARQUIVO, 'docs/README.md')
        self.doc = 'docs/automacao/rodada.md'

    def git(self, *args):
        subprocess.run(['git', *args], cwd=self.raiz, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def doc_tracked(self, texto, doc=None):
        doc = doc or self.doc
        escrever(self.raiz, doc, texto)
        self.git('add', '--', doc)

    def rodar(self):
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONIOENCODING='utf-8')
        proc = subprocess.run([sys.executable, str(self.raiz / 'tools/audita_docs.py')],
                              cwd=self.raiz, env=env, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, encoding='utf-8', timeout=60)
        self.assertNotIn('Traceback', proc.stdout)
        return proc

    def assert_verde(self):
        proc = self.rodar()
        self.assertEqual(proc.returncode, 0, proc.stdout)
        self.assertIn('nenhuma inconsistencia', proc.stdout)
        return proc

    def assert_vermelho(self, motivo):
        proc = self.rodar()
        self.assertEqual(proc.returncode, 1, proc.stdout)
        self.assertIn(motivo, proc.stdout)
        return proc

    def historico(self, nome='review_controls.py', categoria='ferramenta-local', extra=''):
        self.doc_tracked('# Fotografia da rodada\n\npython ' + nome + '\n' + extra)
        catalogo(self.raiz, [registro(self.raiz, self.doc, 3, categoria, nome)])

    def test_baseline_minimo_verde(self):
        self.assert_verde()

    def test_script_local_exato_verde(self):
        self.historico()
        self.assertIn('ok-contexto', self.assert_verde().stdout)

    def test_script_atual_falso_reprova(self):
        self.doc_tracked('Execute agora `tools/review_fake.py`.\n')
        self.assert_vermelho('doc cita ferramenta inexistente: review_fake.py')

    def test_mesmo_nome_em_nova_doc_reprova(self):
        self.historico()
        self.doc_tracked('Execute agora `tools/review_controls.py`.\n', 'docs/automacao/atual.md')
        self.assert_vermelho('doc cita ferramenta inexistente: review_controls.py')

    def test_nova_citacao_no_snapshot_reprova(self):
        self.historico()
        with (self.raiz / self.doc).open('a', encoding='utf-8') as out:
            out.write('\nExecute agora `tools/review_controls.py`.\n')
        self.assert_vermelho('snapshot ausente/alterado')
        self.assert_vermelho('doc cita ferramenta inexistente: review_controls.py')

    def test_editar_linha_historica_reprova(self):
        self.historico()
        escrever(self.raiz, self.doc, '# Fotografia da rodada\n\nExecute agora tools/review_controls.py\n')
        self.assert_vermelho('snapshot ausente/alterado')

    def test_remover_registro_volta_a_reprovar(self):
        self.historico()
        catalogo(self.raiz, [])
        self.assert_vermelho('doc cita ferramenta inexistente: review_controls.py')

    def test_reload_local_historico_verde(self):
        self.historico('ReloadProbe/Plugin.cs', 'caminho-historico')
        # O token da regra 7 é ReloadProbe, não um caminho alternativo.
        catalogo(self.raiz, [registro(self.raiz, self.doc, 3, 'caminho-historico', 'ReloadProbe')])
        self.assertIn('ok-snapshot', self.assert_verde().stdout)

    def test_reload_atual_falso_reprova(self):
        self.doc_tracked('Compile `ReloadProbe/Plugin.cs` deste clone.\n')
        self.assert_vermelho('caminho que nao esta mais no repo: ReloadProbe')

    def test_scratch_old_atual_falso_reprova(self):
        self.doc_tracked('Abra os fontes versionados em `scratch/old/`.\n')
        self.assert_vermelho('caminho que nao esta mais no repo: scratch/old')

    def test_historico_nao_isenta_link_quebrado(self):
        self.historico(extra='\n[Manual](nao-existe.md)\n')
        self.assert_vermelho('link quebrado -> nao-existe.md')

    def test_ferramenta_explicitamente_em_api_verde(self):
        escrever(self.raiz, 'api/tools/check_ui_contract.py', '# Fixture tracked\n')
        self.git('add', '--', 'api/tools/check_ui_contract.py')
        self.doc_tracked('Execute `api/tools/check_ui_contract.py`.\n')
        self.assert_verde()

    def test_ferramenta_relativa_a_api_readme_verde(self):
        escrever(self.raiz, 'api/tools/check_ui_contract.py', '# Fixture tracked\n')
        self.git('add', '--', 'api/tools/check_ui_contract.py')
        self.doc_tracked('  tools/check_ui_contract.py -> ferramenta\n', 'api/README.md')
        self.assert_verde()

    def test_mesmo_basename_em_caminho_falso_reprova(self):
        escrever(self.raiz, 'api/tools/check_ui_contract.py', '# Fixture tracked\n')
        self.git('add', '--', 'api/tools/check_ui_contract.py')
        self.doc_tracked('Execute `tools/check_ui_contract.py`.\n')
        self.assert_vermelho('doc cita ferramenta inexistente: check_ui_contract.py')

    def test_ferramenta_fora_tools_so_no_disco_reprova(self):
        escrever(self.raiz, 'api/tools/check_ui_contract.py', '# Fixture NÃO tracked\n')
        self.doc_tracked('Execute `api/tools/check_ui_contract.py`.\n')
        self.assert_vermelho('doc cita ferramenta inexistente: check_ui_contract.py')

    def test_link_atual_realmente_quebrado_reprova(self):
        self.doc_tracked('[Manual](manual-removido.md)\n')
        self.assert_vermelho('link quebrado -> manual-removido.md')

    def test_catalogo_corrompido_reprova_cli_sem_traceback(self):
        escrever(self.raiz, ARQUIVO, '{')
        self.assert_vermelho('registro ausente/ilegivel')


if __name__ == '__main__':
    unittest.main()
