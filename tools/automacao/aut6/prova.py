"""Vinculo offline de medidas a bytes; nao coleta nem autoriza runtime.

Evidencia runtime: identidade.manifest.artefatos deve conter caminho/sha256;
observacao.evidencia usa {caminho, sha256, ponteiro} (JSON Pointer RFC6901).
O ponteiro seleciona a observacao original; sessao/fonte/dll/config podem vir
DO TOPO DO ARTEFATO, jamais da identidade usada para comparar. Artefatos
rotulados fixture continuam fixture. Hash nao autentica uma origem: o driver
responsavel deve produzir o manifest da coleta; simulacoes sao teste, nao jogo.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

METADADOS = ('id', 'relatorio', 'superficie', 'cenario', 'personagem', 'alvo',
             'sessao', 'fonte_sha', 'dll_sha', 'hash_fonte', 'hash_dll', 'config_sha',
             'config_relevante', 'procedencia', 'rotulo_fixture', 'evidencia_runtime',
             'status', 'ok', 'dentro_da_aura', 'sequencia', 'origem', 'ambiente_prova')


def fixture(o):
    return (o.get('procedencia') == 'fixture' or bool(o.get('rotulo_fixture'))
            or o.get('evidencia_runtime') is False)


def achatar(o):
    c = dict(o)
    for k, v in (o.get('campos') or {}).items():
        if isinstance(v, dict) and v.get('estado') == 'PRESENTE':
            if k in c and c[k] != v.get('valor'):
                c['_conflito_normalizacao'] = True
            else:
                c[k] = v.get('valor')
    return c


def _pointer(doc, ptr):
    if not isinstance(ptr, str) or not ptr.startswith('/'):
        raise ValueError('ponteiro JSON obrigatorio')
    for token in ptr[1:].split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        doc = doc[int(token)] if isinstance(doc, list) else doc[token]
    return doc


def _path(p, raiz):
    p = Path(p)
    return p.resolve() if p.is_absolute() else (Path(raiz) / p).resolve()


def conferir(o, ident, raiz):
    """(estado,motivo,evidencias). Todos os valores consumidos devem existir nos bytes."""
    arts = (ident.get('manifest') or {}).get('artefatos', [])
    conhecidos = {}
    for a in arts:
        if isinstance(a, dict):
            p = a.get('caminho') or a.get('bruto') or a.get('arquivo')
            if p and a.get('sha256'):
                conhecidos[str(_path(p, raiz))] = a['sha256']
    if not conhecidos:
        return 'NAO_EXERCITADO', 'sem manifest verificavel da coleta', []
    refs = o.get('evidencia')
    if not isinstance(refs, list) or not refs:
        return 'NAO_EXERCITADO', 'sem evidencia vinculada por ponteiro JSON', []
    verificadas = []
    for ref in refs:
        if not isinstance(ref, dict):
            return 'NAO_EXERCITADO', 'arquivo existente nao basta: evidencia exige hash e ponteiro JSON', []
        try:
            path = _path(ref['caminho'], raiz)
            esperado = conhecidos.get(str(path))
            if not esperado or not ref.get('sha256'):
                return 'NAO_EXERCITADO', 'evidencia fora do manifest da coleta', []
            real = hashlib.sha256(path.read_bytes()).hexdigest()
            if real != esperado or ref['sha256'] != esperado:
                return 'INDETERMINADO', 'bytes da evidencia contradizem manifest da coleta', []
            doc = json.loads(path.read_text(encoding='utf-8'))
            raw = _pointer(doc, ref.get('ponteiro'))
            if not isinstance(raw, dict):
                raise ValueError('ponteiro nao seleciona objeto')
            if fixture(doc) or fixture(raw) or 'fixtures' in path.parts:
                return 'INDETERMINADO', 'artefato fixture nao prova runtime mesmo se re-rotulado', []
            medido = achatar(raw)
            for k in METADADOS:
                if k not in medido and k in doc:
                    medido[k] = doc[k]
            supplied = achatar(o)
            if medido.get('ambiente_prova') == 'teste_contrato' and supplied.get('ambiente_prova') != 'teste_contrato':
                return 'INDETERMINADO', 'rotulo de teste removido dos bytes: nao prova produto', []
            # Metadata, measurements and scenario guards ALL bind to the same bytes.
            ignorar = {'campos', 'esquema', 'lacunas', 'nao_aplicaveis', 'alvos',
                       'evidencia', 'rotulo', 'manifest', 'objeto_evidencia'}
            for k, valor in supplied.items():
                if k in ignorar or k.startswith('_'):
                    continue
                if k not in medido or medido[k] != valor:
                    return 'INDETERMINADO', 'valor/objeto/cenario nao vinculado aos bytes: %s' % k, []
            for k in ('sessao', 'fonte_sha', 'dll_sha', 'config_sha'):
                if not medido.get(k):
                    return 'NAO_EXERCITADO', 'artefato sem campo tecnico %s' % k, []
            if not (medido.get('cenario') or medido.get('superficie')):
                return 'NAO_EXERCITADO', 'artefato sem cenario/superficie: nao associa a medida', []
            verificadas.append(dict(ref, caminho=str(path)))
        except (OSError, ValueError, KeyError, IndexError, TypeError):
            return 'NAO_EXERCITADO', 'evidencia ilegivel/ponteiro ausente ou invalido', []
    return None, None, verificadas


def normalizar_aut4(obs, *, contexto=None, alvos=None):
    """Chama AUT-4 REAL, preservando campos que seu schema nao transporta.

    contexto so vem do topo do artefato, nao da identidade. Este adaptador nao
    fabrica superficies nem muda procedencia. Entrada ja normalizada pode ser
    consumida por avaliar, mas metadado perdido continua ausente.
    """
    path = Path(__file__).resolve().parents[1] / 'runtime' / 'coletor.py'
    spec = importlib.util.spec_from_file_location('aut6_aut4', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    raw = dict(obs)
    for k in METADADOS:
        if k not in raw and k in (contexto or {}):
            raw[k] = contexto[k]
    procedencia = 'fixture' if fixture(raw) else raw.get('procedencia')
    norm = mod.normalizar_observacao(raw, procedencia,
                                     rotulo_fixture=raw.get('rotulo_fixture'),
                                     contexto=contexto, alvos=alvos)
    for k, v in raw.items():
        if k not in mod.CAMPOS_TODOS or k in METADADOS:
            norm[k] = v
    # Derivacao do normalizador nao e medida declarada pelo artefato.
    for k in ('evidencia_runtime', 'rotulo_fixture', 'ok'):
        if k not in raw:
            norm.pop(k, None)
    return norm
