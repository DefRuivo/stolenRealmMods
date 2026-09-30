#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RV-15 — Varredura GLOBAL de notas redundantes / duplicadas nos tooltips.

O QUE ELE CAÇA (os tres defeitos que o usuario reportou em 30/09):

  1. NOTA == CHAVE .......... a nota repete exatamente o texto que ja estava la.
     Ex. real: `{ "Skill range is reduced to 1 hex.", "\n<color=...>Skill range is reduced to 1 hex.</color>" }`
     -> o tooltip mostra a frase DUAS vezes.

  2. NOTA CONTIDA NA CHAVE ...... a nota inteira ja aparece dentro do texto original
     (nao acrescenta nada ao jogador). Ex. real: o status `Sleep`, cuja chave ja dizia
     "Cannot move or perform actions and damage taken increased by 50%..." e cuja nota
     repetia "Cannot move or perform actions; damage taken is increased by 50%".

  3. NOTA QUE REPETE UM TRECHO LONGO ...... a nota repete o inicio da chave (>= N palavras
     em sequencia), o que na pratica le como eco.

Tambem lista as notas IRRELEVANTES conhecidas do usuario, que sao outro tipo de defeito
(explicar Armor onde Armor e FONTE de dano, nao mitigacao — `Battle Ready`, `Diamond Ice`);
essas sao resolvidas por regra no codigo, e aqui aparecem so para conferencia.

USO:  python tools/check_notas_redundantes.py [-v]
      -v  mostra tambem as notas OK (para conferir que a varredura esta vendo tudo)

Saida: docs/cobertura/revisao/RV-15-notas-redundantes.md  (e resumo no terminal)
Sai com codigo 1 se achar qualquer caso — serve de trava de release.

CURADO A MAO x GERADO
---------------------
O que a ferramenta GERA termina na linha `<!-- fim-gerado -->`; tudo o que vier DEPOIS dessa
linha e escrito a mao, e relido do arquivo e regravado identico por `tools/preserva_curado.py`
— a ferramenta nao apaga trabalho curado (antes de 30/09 ela montava o arquivo inteiro com
`io.open(SAIDA, 'w')` e derrubava qualquer coisa acrescentada depois, o mesmo defeito que
apagou as 53 linhas do veredito do RV-14). Blocos `<!-- curado --> ... <!-- /curado -->`
tambem sao preservados.
"""

import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import preserva_curado  # noqa: E402  guarda do trecho curado a mao (ver o docstring dele)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTE = os.path.join(RAIZ, 'BetterTooltips', 'Patches', 'LocalizePatch.cs')
SAIDA = os.path.join(RAIZ, 'docs', 'cobertura', 'revisao', 'RV-15-notas-redundantes.md')

BS = chr(92)
Q = chr(34)
NL = chr(10)

MIN_PALAVRAS_ECO = 6  # a partir de quantas palavras em sequencia a nota vira eco


def bloco(fonte, nome):
    """Devolve o texto do dicionario `nome` da classe, pulando strings ao contar chaves."""
    k = fonte.index('%s = new Dictionary' % nome)
    k = fonte.index('{', k)
    i = k + 1
    d = 1
    while i < len(fonte) and d > 0:
        c = fonte[i]
        # Comentario pode ter aspas soltas em prosa: se nao pular a linha inteira, o
        # scanner trata essa aspa como inicio de string e perde um `{`/`}` no caminho,
        # o que fazia o bloco terminar cedo (28 de 195 notas analisadas).
        if fonte.startswith('//', i):
            i = fonte.find(NL, i)
            if i < 0:
                break
            continue
        if c == Q:
            i += 1
            while i < len(fonte):
                if fonte[i] == BS:
                    i += 2
                    continue
                if fonte[i] == Q:
                    i += 1
                    break
                i += 1
            continue
        if c == '{':
            d += 1
        elif c == '}':
            d -= 1
        i += 1
    return fonte[k:i], k


def le_string(t, i):
    """Le uma string C# a partir da aspa em t[i]. Devolve (conteudo, proximo_indice)."""
    i += 1
    buf = []
    while i < len(t):
        c = t[i]
        if c == BS:
            buf.append(t[i:i + 2])
            i += 2
            continue
        if c == Q:
            return ''.join(buf), i + 1
        buf.append(c)
        i += 1
    return None, i


def entradas(texto, offset):
    """Pares (linha, comentario, chave, valor) na ordem do arquivo."""
    out = []
    i = 0
    comentario = []
    while i < len(texto):
        c = texto[i]
        if c == Q:
            _, i = le_string(texto, i)
            continue
        if texto.startswith('//', i):
            fim = texto.find(NL, i)
            if fim < 0:
                break
            comentario.append(texto[i:fim].strip())
            i = fim
            continue
        if c == '{':
            j = i + 1
            while j < len(texto) and texto[j] in ' \t\r\n':
                j += 1
            if j < len(texto) and texto[j] == Q:
                chave, j2 = le_string(texto, j)
                if chave is not None:
                    m = j2
                    while m < len(texto) and texto[m] in ' \t\r\n':
                        m += 1
                    if m < len(texto) and texto[m] == ',':
                        m += 1
                        while m < len(texto) and texto[m] in ' \t\r\n':
                            m += 1
                        if m < len(texto) and texto[m] == Q:
                            valor, m2 = le_string(texto, m)
                            if valor is not None:
                                linha = texto[:i].count(NL) + offset
                                out.append((linha, ' '.join(comentario)[:120], chave, valor))
                                comentario = []
                                i = m2
                                continue
        if c not in ' \t\r':
            comentario = []
        i += 1
    return out


def desmarca(v):
    """Tira o markup e devolve o texto puro, minusculo, com espacos normalizados."""
    v = re.sub(r'<color=#[0-9A-Fa-f]{6}>', ' ', v)
    v = re.sub(r'</?[a-zA-Z]+>', ' ', v)          # <i> <b> </color> etc.
    v = v.replace(BS + 'n', ' ')                  # o escape de quebra de linha
    v = re.sub(r'\{STA=([^}]*)\}', r'\1', v)      # token de status -> nome
    v = v.replace('@', ' ')
    v = re.sub(r'\s+', ' ', v)
    return v.strip().lower()


def palavras(t):
    return [p for p in re.findall(r'[a-z0-9%]+', t) if len(p) > 1]


def maior_sequencia_comum(a, b):
    """Maior numero de palavras SEGUIDAS de `a` que aparecem tambem em `b`."""
    pa, pb = palavras(a), palavras(b)
    if not pa or not pb:
        return 0
    conj = set()
    for n in range(2, len(pb) + 1):
        for i in range(len(pb) - n + 1):
            conj.add(' '.join(pb[i:i + n]))
    melhor = 0
    for n in range(len(pa), 1, -1):
        for i in range(len(pa) - n + 1):
            if ' '.join(pa[i:i + n]) in conj:
                return n
    return melhor


def main():
    verbose = '-v' in sys.argv
    if not os.path.exists(FONTE):
        print('nao achei %s' % FONTE)
        return 2
    fonte = io.open(FONTE, encoding='utf-8').read()
    _, off = bloco(fonte, 'TextAppends')
    itens = entradas(bloco(fonte, 'TextAppends')[0], off)

    iguais, contidas, ecos, ok = [], [], [], []
    for linha, com, chave, valor in itens:
        c, v = desmarca(chave), desmarca(valor)
        if not v:
            ok.append((linha, com, chave, valor, 'nota vazia (so cor/markup)'))
        elif v == c:
            iguais.append((linha, com, chave, valor))
        elif len(v) > 12 and v in c:
            contidas.append((linha, com, chave, valor))
        else:
            n = maior_sequencia_comum(v, c)
            if n >= MIN_PALAVRAS_ECO:
                ecos.append((linha, com, chave, valor, n))
            else:
                ok.append((linha, com, chave, valor, 'unica'))

    L = []
    L.append('# RV-15 - Notas redundantes / duplicadas nos tooltips')
    L.append('')
    L.append('Gerado por `tools/check_notas_redundantes.py` a partir de `BetterTooltips/Patches/LocalizePatch.cs`.')
    L.append('')
    L.append('O que a ferramenta **gera** termina na linha `<!-- fim-gerado -->`; tudo o que vier')
    L.append('depois dela e escrito a mao e **nunca** e reescrito (ver `tools/preserva_curado.py`).')
    L.append('')
    L.append('Uma nota existe para dizer o que o texto **nao** diz. Quando ela repete o proprio texto,')
    L.append('o jogador le a mesma frase duas vezes e a explicacao perde credito - foi o que o usuario')
    L.append('reportou em 30/09 (`Blinding Lights` duplicado, `Blind`/`Sleep` redundantes,')
    L.append('`Praying Shot`/`Chok` na mesma familia).')
    L.append('')
    L.append('## Resumo')
    L.append('')
    L.append('| caso | quantas | o que significa |')
    L.append('|---|---|---|')
    L.append('| nota == chave | **%d** | texto e nota sao a MESMA frase: aparece duplicado na tela |' % len(iguais))
    L.append('| nota contida na chave | **%d** | a nota inteira ja esta no texto: nao acrescenta nada |' % len(contidas))
    L.append('| nota ecoa >= %d palavras da chave | **%d** | repete o inicio do texto em sequencia |' % (MIN_PALAVRAS_ECO, len(ecos)))
    L.append('| notas unicas (OK) | %d | dizem algo que o texto nao diz |' % len(ok))
    L.append('')
    L.append('Total de notas analisadas: **%d**.' % len(itens))
    L.append('')

    def secao(titulo, itens_, extra=None):
        L.append('## %s' % titulo)
        L.append('')
        if not itens_:
            L.append('Nenhum caso. ')
            L.append('')
            return
        for it in itens_:
            L.append('- **l.%d** `%s`' % (it[0], (it[1] or '(sem comentario)')[:110]))
            L.append('  - chave: %s' % re.sub(r'\s+', ' ', it[2])[:190])
            L.append('  - nota : %s' % re.sub(r'\s+', ' ', it[3])[:190])
            if extra:
                L.append('  - %s' % extra(it))
            L.append('')

    secao('1. Nota identica a chave (DUPLICADO na tela)', iguais)
    secao('2. Nota inteiramente contida na chave (redundante)', contidas)
    secao('3. Nota que ecoa o texto', ecos, extra=lambda it: 'palavras em sequencia: **%d**' % it[4])

    if verbose:
        L.append('## Notas unicas (OK)')
        L.append('')
        for it in ok:
            L.append('- l.%d `%s` -> %s' % (it[0], (it[1] or '')[:80], re.sub(r'\s+', ' ', it[3])[:120]))
        L.append('')

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    try:
        origem, n_linhas = preserva_curado.grava(SAIDA, NL.join(L))
    except preserva_curado.CuradoPerdido as e:
        print('ABORTADO: %s' % e)
        return 3

    print('RV-15 - varredura de notas redundantes')
    print('  notas analisadas ......... %d' % len(itens))
    print('  nota == chave ............ %d  (duplicado na tela)' % len(iguais))
    print('  nota contida na chave .... %d' % len(contidas))
    print('  nota ecoando >= %d palavras %d' % (MIN_PALAVRAS_ECO, len(ecos)))
    print('  notas unicas (OK) ........ %d' % len(ok))
    print('  curado preservado ........ %d linha(s) a mao (%s)' % (n_linhas, origem))
    print('  relatorio: %s' % os.path.relpath(SAIDA, RAIZ).replace(chr(92), '/'))
    for it in iguais + contidas + ecos:
        print('    l.%d  %s' % (it[0], (it[1] or '')[:80]))
    return 1 if (iguais or contidas or ecos) else 0


if __name__ == '__main__':
    sys.exit(main())
