"""Validacoes de medidas AUT-6 sem alterar produto/oraculos."""
import math


def corpo(o):
    raw = o['_raw']
    if raw.get('ativo_na_hierarquia') is False or raw.get('visivel_na_tela') is False:
        return 'INDETERMINADO', 'componente inativo/invisivel nao prova corpo renderizado'
    if o['rotulo'] == 'runtime':
        for k in ('ativo_na_hierarquia', 'visivel_na_tela', 'objeto', 'personagem'):
            if raw.get(k) is None:
                return 'NAO_EXERCITADO', 'corpo sem campo tecnico %s' % k
        if raw.get('ativo_na_hierarquia') is not True or raw.get('visivel_na_tela') is not True:
            return 'INDETERMINADO', 'visibilidade/atividade nao comprovada'
    return None, None


def retangulo(v):
    if not isinstance(v, dict) or not all(k in v for k in ('x', 'y', 'largura', 'altura')):
        return None
    vals = [v[k] for k in ('x', 'y', 'largura', 'altura')]
    if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in vals):
        return None
    if vals[2] <= 0 or vals[3] <= 0:
        return None
    return vals


def estilo(raw):
    """Dois criterios independentes: cor do span, posicao final + contencao."""
    measured, expected, source = raw.get('linha_azul_cor'), raw.get('cor_azul_jogo'), raw.get('fonte_cor')
    if not measured or not expected or not source:
        cor = ('NAO_EXERCITADO', 'sem cor do span/controle azul independente/fonte da cor')
    elif measured != expected:
        cor = ('REPROVADO', 'cor da linha difere do azul medido no controle do jogo')
    else:
        cor = (None, None)
    line = retangulo(raw.get('linha_azul_retangulo'))
    body = retangulo(raw.get('corpo_retangulo'))
    if not line or not body or raw.get('linha_azul_ultima') is None:
        pos = ('NAO_EXERCITADO', 'sem retangulos medidos/ordem final da linha azul')
    else:
        x, y, w, h = line
        bx, by, bw, bh = body
        within = bx <= x and by <= y and x+w <= bx+bw and y+h <= by+bh
        pos = (None, None) if within and raw['linha_azul_ultima'] is True else (
            'REPROVADO', 'linha azul fora do corpo ou nao e o ultimo bloco')
    return [('cor', cor, {'cor': expected, 'fonte': source}, measured),
            ('posicao', pos, {'contida_no_corpo': True, 'ultimo_bloco': True,
                             'fonte': 'docs/TEXTO-TOOLTIPS.md + LocalizePatch.cs RV-27'},
             {'linha': raw.get('linha_azul_retangulo'), 'corpo': raw.get('corpo_retangulo'),
              'ultima': raw.get('linha_azul_ultima')})]
