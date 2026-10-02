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

COMO O PARSER LE - E POR QUE ELE E UM SO
----------------------------------------
ENTRADA = **um item do dicionario**, isto e, o par `{ "chave", "valor" }`. Essa e a
contagem OFICIAL do projeto - a mesma que o `tools/check_chave_compartilhada.py`
publica - e a unica que a documentacao pode citar.

O parser UNICO e `tools/tabelas.py` (a fonte da verdade: `bloco()`/`entradas()`, que
pulam comentario de LINHA e de BLOCO). Este arquivo NAO le com implementacao propria:
importa `bloco()`/`entradas()` do `check_chave_compartilhada.py`, que e um WRAPPER
migrado sobre o `tabelas.py` (o import direto historicamente vem daqui; o contrato nao
mudou). Se o import falhar o script nao roda, em vez de medir com outra definicao.

Motivo (caso real, 30/09/2026): os dois scripts mediam o MESMO `LocalizePatch.cs` e
discordavam - o `check_dupes` dizia *TextFixes 119 entradas*, o
`check_chave_compartilhada` dizia *86*. Nenhum dos dois estava "certo por outra
definicao": o `check_dupes` fatiava o arquivo a partir da PRIMEIRA ocorrencia crua do
nome (`TextFixes`), e desde 30/09 esse nome aparece antes numa linha de COMENTARIO
dentro de `TextAppends`; o corte comecava na tabela errada e ia ate o primeiro `};`,
entao o "119" era a CAUDA do `TextAppends`. Dois parsers para o mesmo arquivo foi o
que produziu a divergencia - e um numero errado chegou a ser citado na doc. Um parser
so, com a definicao escrita, e o conserto de verdade.

USO
---
    python tools/check_dupes.py     # 0 = limpo, 1 = tem duplicata, 2 = nao achei a tabela

Roda no ritual de build: build 0 erros -> check_fix_keys -> check_dupes -> instalar.
"""
import io
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Wrapper migrado sobre o parser UNICO (`tools/tabelas.py`): a definicao de "entrada"
# mora LA, nao aqui. O import passa pelo `check_chave_compartilhada` por contrato historico.
import check_chave_compartilhada as tabelas     # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARQ = os.path.join(RAIZ, 'BetterTooltips', 'Patches', 'LocalizePatch.cs')
BLOCOS = ('TextFixes', 'TextAppends')

NL = chr(10)


def chaves_do_bloco(fonte, nome):
    """Chaves (1a string) de cada ENTRADA do dicionario `nome`, na ordem do arquivo.

    Entrada = item do dicionario. O bloco e localizado por `NOME = new Dictionary` e por
    casamento de chaves (nao por proximidade de `};`), e cada item e lido como
    `{ "chave", "valor" }`, pulando comentarios - inclusive comentario DENTRO das chaves,
    que a contagem antiga por "strings de indice par" perdia ou desalinhava.
    """
    txt, k = tabelas.bloco(fonte, nome)
    return [e[2] for e in tabelas.entradas(txt, fonte[:k].count(NL))]


def main():
    if not os.path.exists(ARQ):
        print('nao achei %s' % ARQ)
        return 2
    s = io.open(ARQ, encoding='utf-8').read()
    ruins = 0
    for bloco in BLOCOS:
        try:
            chaves = chaves_do_bloco(s, bloco)
        except ValueError:
            # Tabela renomeada/movida: sem isso o script diria "0 entradas" e passaria.
            print('%s: bloco nao encontrado (procura por "%s = new Dictionary")' % (bloco, bloco))
            return 2
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
