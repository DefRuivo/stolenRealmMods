#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""preserva_curado.py - impede que o relatorio GERADO apague o trabalho CURADO A MAO.

O DEFEITO QUE ELE FECHA (30/09)
-------------------------------
Relatorio de revisao tem DUAS partes no mesmo arquivo .md:

  1. o que a ferramenta GERA a cada rodada (contagens, tabelas) - muda sempre;
  2. o que a REVISAO escreve A MAO (vereditos, precedentes, licoes) - nao muda nunca.

Ate 30/09 cada gerador montava o arquivo INTEIRO (`io.open(caminho, 'w')`), entao a parte 2
era apagada em silencio: `python tools/check_terminologia.py` derrubou as 53 linhas do
`VEREDITO POR CONCEITO` do `docs/cobertura/revisao/RV-14-terminologia.md` (um agente rodou,
viu o estrago e restaurou com `git checkout`). Contagem textual nao avisa: quem roda a
ferramenta para CONFERIR o numero e quem perde o texto curado.

A REGRA (e o porque dela)
-------------------------
O texto gerado e sempre um PREFIXO do arquivo e termina na linha do marcador explicito

    <!-- fim-gerado -->          <- o marcador tem de estar SOZINHO na linha

(e nao a citacao do marcador na prosa do cabecalho: a fronteira e a linha inteira). Tudo o
que vem DEPOIS dessa linha e curado a mao: `grava()` RELÊ o arquivo existente e regrava esse
trecho IDENTICO (byte a byte), sem interpretar nada dele. Blocos
`<!-- curado --> ... <!-- /curado -->` em qualquer posicao do arquivo tambem sao preservados
(segundo formato, para quem preferir delimitar o trecho em vez de confiar na posicao).

Arquivo gerado ANTES desta guarda (sem marcador): usa-se uma ANCORA - um trecho unico da
ULTIMA linha do texto gerado - e tudo o que vem depois dela e tratado como curado. Sem
marcador, sem bloco, sem ancora e com conteudo que o gerado NAO reproduz, `grava()` ABORTA
sem escrever: e melhor nao gravar do que apagar as cegas. A ancora e so para a MIGRACAO -
depois da 1a rodada o arquivo ja tem o marcador e a ancora nao e mais usada.

USO (dentro de tools/, como o parser compartilhado do `check_dupes.py`)
----------------------------------------------------------------------
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import preserva_curado
    origem, linhas = preserva_curado.grava(SAIDA, texto_gerado, ancora='...ultima linha...')
    print('curado preservado: %d linha(s) (%s)' % (linhas, origem))
"""
import io
import os

FIM = '<!-- fim-gerado -->'
INI = '<!-- curado -->'
FIM_CURADO = '<!-- /curado -->'
LEGADO = 'legado (arquivo sem marcador, achado pela ancora)'


class CuradoPerdido(Exception):
    """O arquivo existente tem conteudo que o relatorio gerado nao reproduz - nao gravei."""


def _norm(t):
    return t.replace('\r\n', '\n').rstrip('\n')


def blocos(texto):
    """Trechos entre `<!-- curado -->` e `<!-- /curado -->`, na ordem do arquivo."""
    out = []
    i = 0
    while True:
        a = texto.find(INI, i)
        if a < 0:
            return out
        b = texto.find(FIM_CURADO, a)
        if b < 0:
            return out
        out.append(texto[a:b + len(FIM_CURADO)])
        i = b + len(FIM_CURADO)


def _pos_fim(texto):
    """Fim da linha do marcador (o marcador tem de estar sozinho na linha); -1 se nao ha.

    Linha propria, e nao substring: a prosa do cabecalho pode CITAR o marcador
    (`... termina na linha <!-- fim-gerado -->`), e uma citacao no meio da frase nao pode
    passar por fronteira do gerado.
    """
    alvo = '\n' + FIM + '\n'
    k = texto.rfind(alvo)               # o marcador de verdade e o ULTIMO da linha propria
    if k >= 0:
        return k + len(alvo)
    if texto.startswith(FIM + '\n'):
        return len(FIM) + 1
    return -1


def coda(texto, ancora=None):
    """(trecho curado, de onde ele veio) do arquivo existente; (None, None) se nao da para saber."""
    pos = _pos_fim(texto)
    if pos >= 0:
        return texto[pos:], 'marcador %s' % FIM
    b = blocos(texto)
    if b:
        return '\n\n'.join(b), 'blocos %s' % INI
    if ancora:
        k = texto.rfind(ancora)
        if k >= 0:
            return texto[k + len(ancora):], LEGADO
    return None, None


def grava(caminho, corpo, ancora=None):
    """Grava `corpo` (gerado) seguido do trecho curado relido de `caminho`.

    Devolve (de onde veio o curado, quantas linhas curadas foram preservadas).
    Levanta `CuradoPerdido` sem tocar no arquivo quando o conteudo existente nao e
    reconhecivel como gerado nem como curado.
    """
    corpo = corpo.replace('\r\n', '\n').rstrip('\n')
    velho = None
    if os.path.exists(caminho):
        with io.open(caminho, encoding='utf-8') as fh:   # universal newlines: grava tudo em LF
            velho = fh.read()
    curado, origem = '', 'nenhum trecho curado no arquivo'
    if velho is not None:
        curado, origem = coda(velho, ancora)
        if curado is None:
            if _norm(velho) != _norm(corpo):
                raise CuradoPerdido(
                    '%s tem conteudo que este gerador nao reproduz e nao ha marcador `%s` nem '
                    'ancora: NADA foi escrito. Este arquivo foi gerado ANTES da guarda: coloque '
                    'uma linha so com `%s` logo depois da ultima linha gerada (no fim do arquivo, '
                    'quando ainda nao ha trecho curado) - tudo o que ficar abaixo e preservado.'
                    % (caminho, FIM, FIM))
            curado, origem = '', 'arquivo so com o gerado'
        curado = curado.strip('\n')
    if curado:
        novo = corpo + '\n\n' + FIM + '\n\n' + curado + '\n'
    else:
        novo = corpo + '\n\n' + FIM + '\n'
    os.makedirs(os.path.dirname(os.path.abspath(caminho)), exist_ok=True)
    with io.open(caminho, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(novo)
    return origem, (curado.count('\n') + 1 if curado else 0)
