"""Exercise the actual registry step without upload or external network calls."""
import contextlib
from email.message import Message
import io
import json
import os
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch
import urllib.error

ROOT = Path(__file__).resolve().parents[2]
MOD = 'RoguelikeUnlimitedLevelProgression'
VERSION = '0.1.1'
STAMP = '2026-10-17T02:59:35.654040Z'


def registry_code():
    workflow = (ROOT / '.github/workflows/publish.yml').read_text(encoding='utf-8')
    block = workflow.split('      - name: Confere na API publica e atualiza o registro\n', 1)[1]
    block = block.split("          python - <<'PY'\n", 1)[1].split('\n          PY', 1)[0]
    return '\n'.join(line[10:] for line in block.splitlines())


class RegistryTests(unittest.TestCase):
    def exercise(self, version=None, latest=None, community=None, package_sequence=None):
        calls = []
        sleeps = []
        version = version if version is not None else 404
        latest = latest if latest is not None else 404
        sequence = list(package_sequence or [])

        def urlopen(request, timeout=None):
            url = request.full_url
            calls.append(url)
            if '/api/v1/package/' in url:
                result = community if community is not None else []
            elif url.endswith('/' + VERSION + '/'):
                result = version
            else:
                result = sequence.pop(0) if sequence else latest
            if isinstance(result, int):
                raise urllib.error.HTTPError(url, result, 'fixture', Message(), io.BytesIO())
            class Response(io.BytesIO):
                status = 200
            return Response(json.dumps(result).encode())

        original = Path.cwd()
        with tempfile.TemporaryDirectory(prefix='registry-test-', dir=ROOT) as temp:
            os.chdir(temp)
            try:
                Path('release').mkdir()
                ledger = Path('release/mods.json')
                ledger.write_text(json.dumps({'comunidade': 'stolen-realm', 'mods': [
                    {'nome': MOD, 'publicar': True, 'versao_publicada': None, 'publicado_em': None}
                ]}), encoding='utf-8')
                Path('target.csproj').write_text('<Project><Version>0.1.1</Version></Project>', encoding='utf-8')
                packer = types.SimpleNamespace(returncode=0, stdout=json.dumps([
                    {'nome': MOD, 'csproj': 'target.csproj'}
                ]).encode())
                env = {'ALVOS': json.dumps([MOD]), 'TEAM': 'DefRuivo_StolenRealmMods',
                       'GITHUB_OUTPUT': str(Path(temp) / 'output'), 'GITHUB_STEP_SUMMARY': str(Path(temp) / 'summary')}
                code = registry_code()
                exit_code = 0
                with patch.dict(os.environ, env), patch('urllib.request.urlopen', side_effect=urlopen), \
                     patch('subprocess.run', return_value=packer), patch('time.sleep', side_effect=sleeps.append), \
                     contextlib.redirect_stdout(io.StringIO()):
                    try:
                        exec(compile(code, 'publish.yml:registra', 'exec'), {})
                    except SystemExit as error:
                        exit_code = error.code
                return exit_code, json.loads(ledger.read_text(encoding='utf-8'))['mods'][0], calls, sleeps
            finally:
                os.chdir(original)

    @staticmethod
    def live(**changes):
        return dict({'version_number': VERSION, 'is_active': True, 'date_created': STAMP}, **changes)

    def test_exact_version_registers_platform_timestamp(self):
        status, entry, _, _ = self.exercise(version=self.live())
        self.assertEqual(status, 0)
        self.assertEqual((entry['versao_publicada'], entry['publicado_em']), (VERSION, STAMP))

    def test_package_latest_rescues_version_404_and_stale_list(self):
        status, entry, _, _ = self.exercise(latest={'latest': self.live()})
        self.assertEqual(status, 0)
        self.assertEqual((entry['versao_publicada'], entry['publicado_em']), (VERSION, STAMP))

    def test_transient_package_429_recovers_with_bounded_retry(self):
        status, entry, _, sleeps = self.exercise(package_sequence=[429, {'latest': self.live()}])
        self.assertEqual(status, 0)
        self.assertEqual(entry['versao_publicada'], VERSION)
        self.assertEqual(sleeps, [5])

    def test_missing_package_fails_and_keeps_registry_empty(self):
        status, entry, calls, sleeps = self.exercise()
        self.assertEqual(status, 1)
        self.assertIsNone(entry['versao_publicada'])
        self.assertLessEqual(len(calls), 7)
        self.assertEqual(sleeps, [5, 5])

    def test_wrong_latest_version_is_not_recorded(self):
        status, entry, _, _ = self.exercise(latest={'latest': self.live(version_number='0.1.2')})
        self.assertEqual(status, 1)
        self.assertIsNone(entry['versao_publicada'])

    def test_inactive_latest_is_not_recorded(self):
        status, entry, _, _ = self.exercise(latest={'latest': self.live(is_active=False)})
        self.assertEqual(status, 1)
        self.assertIsNone(entry['versao_publicada'])

    def test_missing_platform_timestamp_is_not_invented(self):
        status, entry, _, _ = self.exercise(version=self.live(date_created=None), latest={'latest': self.live(date_created=None)})
        self.assertEqual(status, 1)
        self.assertIsNone(entry['versao_publicada'])

    def test_community_fallback_preserved(self):
        status, entry, _, _ = self.exercise(community=[{
            'full_name': 'DefRuivo_StolenRealmMods-' + MOD, 'versions': [self.live()]
        }])
        self.assertEqual(status, 0)
        self.assertEqual(entry['publicado_em'], STAMP)


if __name__ == '__main__':
    unittest.main()
