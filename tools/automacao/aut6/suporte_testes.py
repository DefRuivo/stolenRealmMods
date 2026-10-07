"""Emissor de TESTE DE CONTRATO, nao fixture de runtime/produto.

Escreve bytes de entrada e manifest reais de sandbox. Nao consulta jogo,
nao chama probe e sempre marca ambiente_prova=teste_contrato: o avaliador
pode aprovar a logica, jamais promover esta entrada a prova_runtime.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile

BASE = Path(os.environ.get('HERMES_KANBAN_WORKSPACE') or os.environ.get('TMPDIR') or Path(__file__).parent)
TMP = tempfile.TemporaryDirectory(prefix='aut6-contrato-', dir=BASE)
ROOT = Path(TMP.name)
IDENT = {'fonte_sha': 'a'*64, 'dll_sha': 'b'*64, 'config_sha': 'c'*64, 'sessao': 'teste-contrato-1'}
CASO_CORPO = {'id': 'S-rv26-corpo-linha-nota', 'tipo': 'corpo_tooltip', 'rv': ['RV-26', 'RV-27'],
              'superficie': 'tooltip_shrine', 'nota_fragmento': 'Shrine Effect Bonus'}


def corpo():
    return dict(IDENT, id='test-body', relatorio='test-body', procedencia='runtime',
                ambiente_prova='teste_contrato', origem='emissor_offline_de_teste',
                cenario=CASO_CORPO['id'], objeto='GUI/Tooltip/Description', personagem='TesteA',
                superficie='tooltip_shrine', texto_renderizado='Shrine Effect Bonus\n\nYour active shrine auras: Damage +24%.',
                ativo_na_hierarquia=True, visivel_na_tela=True, status='OK', ok=True,
                linha_azul_cor='#0011FF', cor_azul_jogo='#0011FF',
                fonte_cor='controle independente de teste, nao cor do produto',
                linha_azul_retangulo={'x': 10, 'y': 10, 'largura': 40, 'altura': 10},
                corpo_retangulo={'x': 0, 'y': 0, 'largura': 100, 'altura': 100}, linha_azul_ultima=True)


def gravar(obs, nome='medidas'):
    """Bytes e manifest independentes do payload que depois tentamos adulterar."""
    obs = copy.deepcopy(obs)
    for o in obs:
        o.pop('evidencia', None)
    path = ROOT / (nome + '.json')
    path.write_text(json.dumps({'procedencia': 'runtime', 'ambiente_prova': 'teste_contrato',
                                'observacoes': obs}, ensure_ascii=False), encoding='utf-8')
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    ident = dict(IDENT, manifest={'artefatos': [{'caminho': str(path), 'sha256': sha}]})
    for i, o in enumerate(obs):
        o['evidencia'] = [{'caminho': str(path), 'sha256': sha, 'ponteiro': '/observacoes/%d' % i}]
    return obs, ident


def cadeia_kw(ident):
    return {'suficiente': True, 'faltando': [], 'kwargs': ident}
