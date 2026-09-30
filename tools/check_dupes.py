#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_dupes.py - acha chave DUPLICADA nos dicionarios do LocalizePatch.

POR QUE ESTA FERRAMENTA EXISTE
------------------------------
Em 29/09 o mod de textos simplesmente parou de carregar, e o jogo registrou:

    ArgumentException: An item with the same key has already been added.
    Key: Deals *0 weapon damage to all enemies within a line.
    Rethrow as TypeInitializationException: The type initializer for
    'BetterTooltips.Patches.LocalizePatch' threw an exception.

Um `Dictionary<string,string>` em C# NAO aceita chave repetida: `Add` estoura
`ArgumentException`. Como as tabelas do mod sao campos `static readonly`
inicializados no construtor estatico, a excecao vira `TypeInitializationException`
e **a classe inteira nao carrega** - nao perde so a entrada nova, perde TODO o mod
de textos. E o `check_fix_keys.py` nao pegava isso: ele conta chaves e compara com
o censo, mas contagem de chave repetida continua "certa".

A CAUSA RAIZ (para nao repetir)
-------------------------------
Eu vinha escrevendo **uma entrada por skill**. Mas skills diferentes podem ter o
MESMO texto: `Slam` e `Crushing Slam` sao identicos ("Deals *0 weapon damage to all
enemies within a line."), e `Stunning Slam` tem texto proprio. Uma entrada por skill
= tres chaves, duas iguais = crash.

REGRA: **uma entrada por TEXTO, nao por skill**. Se duas skills compartilham o texto,
uma entrada so serve as duas (o lookup do mod e por texto).

COMO O PARSER LE
----------------
Cada entrada tem 2 strings: (chave, valor). Entao:
  1. remove linhas de comentario (`//`), que contem aspas soltas em prosa;
  2. varre o bloco string por string, respeitando escape (`\\"`);
  3. pega as strings de indice PAR = chaves (a impar e o valor).
Tentar fazer isso com regex `[^"\\\\]` foi o que quebrou na primeira tentativa: o
heredoc do shell colapsa as barras e o padrao chega invalido ("unterminated
character set"). Varredura caractere a caractere nao tem esse problema.

USO
---
    python tools/check_dupes.py            # 0 = limpo, 1 = tem duplicata

Roda no ritual de build: build 0 erros -> check_fix_keys -> check_dupes -> instalar.
"""
import io
import os
import sys
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQ = os.path.join(RAIZ, 'BetterTooltips', 'Patches', 'LocalizePatch.cs')
BLOCOS = ('TextFixes', 'TextAppends')

NL = chr(10)
Q = chr(34)
BS = chr(92)


def extrai_chaves(seg):
    """Strings de indice par dentro do bloco (as impares sao os valores)."""
    linhas = [l for l in seg.split(NL) if not l.strip().startswith('//')]
    seg = NL.join(linhas)
    strs = []
    k = 0
    while True:
        k = seg.find(Q, k)
        if k < 0:
            break
        m = k + 1
        buf = []
        while m < len(seg):
            c = seg[m]
            if c == BS:                      # escape: consome 2 chars
                buf.append(seg[m:m + 2])
                m += 2
                continue
            if c == Q:
                break
            buf.append(c)
            m += 1
        strs.append(''.join(buf))
        k = m + 1
    return [strs[i] for i in range(0, len(strs), 2)]


def main():
    if not os.path.exists(ARQ):
        print('nao achei %s' % ARQ)
        return 1
    s = io.open(ARQ, encoding='utf-8').read()
    ruins = 0
    for bloco in BLOCOS:
        try:
            i = s.index(bloco)
            j = s.index('};', i)
        except ValueError:
            print('%s: bloco nao encontrado' % bloco)
            continue
        chaves = extrai_chaves(s[i:j])
        dup = {k: n for k, n in Counter(chaves).items() if n > 1}
        print('%-12s %3d entradas | duplicadas: %s' % (bloco, len(chaves),
              (', '.join(repr(k[:60]) for k in dup)) if dup else 'nenhuma'))
        for k, n in dup.items():
            print('   x%d  %r' % (n, k[:100]))
        ruins += len(dup)
    if ruins:
        print(NL + '>>> %d chave(s) duplicada(s): em C# isso vira ArgumentException e derruba' % ruins)
        print('    o LocalizePatch INTEIRO na inicializacao estatica. Use UMA entrada por TEXTO')
        print('    (se duas skills dividem o texto, uma entrada serve as duas).')
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
