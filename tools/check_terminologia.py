#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_terminologia.py - RV-14: consistencia de TERMOS no jogo inteiro.

POR QUE EXISTE
--------------
Pedido do usuario: "manter o contexto e conciso com o restante do jogo - por exemplo, crippled
e slow: se na maioria dos lugares chama de um jeito, nos debuffs tambem devem manter um padrao
comparado com o restante, como as skill trees".

O caso que originou: NENHUMA acao do jogo aplica o status `Crippled`, e CINCO aplicam `Slow` -
inclusive uma skill chamada `Cripple`. Pela regra do padrao da maioria (5 de 5) o texto das
skills ficou como estava. O que faltava era um instrumento para ver isso em TODOS os termos,
e nao so nesse.

O QUE ELE FAZ
-------------
Para cada CONCEITO curado abaixo, conta as variantes de termo nos cinco corpora do censo
(skills, status, itens, afixos, powerups). Onde ha mais de uma variante em uso, ele mostra a
DISTRIBUICAO - que e o que responde "a maioria escreve como?" com numero, nao com impressao.

LIMITE HONESTO
--------------
A lista de conceitos e CURADA a mao (nao existe thesaurus do vocabulario do jogo). Ela cobre o
que ja apareceu em 451 skills e 133 debuffs revisados; conceito novo entra aqui quando a
revisao encontrar. Nao decide nada sozinho: se uma variante tem 3 usos e outra 12, o relatorio
aponta 12 - quem decide se muda e a revisao, e a regra do projeto e seguir a MAIORIA.

Uso: python tools/check_terminologia.py
Saida: docs/cobertura/revisao/RV-14-terminologia.md
"""
import csv
import io
import os
import re
from collections import Counter, OrderedDict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIR = os.path.join(RAIZ, 'docs', 'cobertura')
REL = os.path.join(DIR, 'revisao', 'RV-14-terminologia.md')
CORPORA = OrderedDict([
    ('skills', 'skills.csv'),
    ('status', 'status.csv'),
    ('itens', 'itens.csv'),
    ('afixos', 'afixos.csv'),
    ('powerups', 'powerups.csv'),
])
# conceito -> variantes (regex, sem acento, minusculo). Cada variante e uma contagem propria.
CONCEITOS = OrderedDict([
    ('lentidao (cripple x slow)', [r'\bcrippl\w*', r'\bslow\w*']),
    ('atordoamento (stun x rooted+disabled)', [r'\bstunn?\w*', r'\broot\w*', r'\bdisabl\w*']),
    ('congelamento (frozen x chilled)', [r'\bfrozen\b', r'\bchill\w*']),
    ('vida maxima (max health x maximum health)', [r'\bmax health\b', r'\bmaximum health\b', r'\bmax hp\b']),
    ('dano recebido (taken x received)', [r'damage taken', r'damage received', r'damage this target takes']),
    ('cura (healing x holy power)', [r'\bhealing\b', r'\bholy power\b']),
    ('resistencia sagrada (divine x holy)', [r'\bdivine\b', r'\bholy\b']),
    ('pontos de movimento (movement points x movement)', [r'movement points?', r'\bmovement\b']),
    ('empilhamento (per stack x stacks)', [r'\bper stack\b', r'\bstacks?\b']),
    ('duracao (lasts x for N turns)', [r'\blasts\b', r'\bfor \d+ turns?\b']),
    ('escopo de atributos (all stats x all attributes)', [r'\ball stats\b', r'\ball attributes\b', r'\ball resistances?\b']),
    ('alcance (range x reach)', [r'\brange\b', r'\breach\b']),
    ('acerto critico (crit x critical)', [r'\bcrit\b', r'\bcritical\b']),
    ('area (aura x area x within)', [r'\baura\b', r'\bwithin the area\b', r'\barea\b']),
])


def textos():
    for nome, arq in CORPORA.items():
        p = os.path.join(DIR, arq)
        if not os.path.exists(p):
            continue
        with io.open(p, encoding='utf-8') as fh:
            for r in csv.DictReader(fh):
                campos = [v for k, v in r.items() if v and k in ('nome', 'descricao', 'efeitos', 'efeitosDano', 'texto')]
                if campos:
                    yield nome, ' | '.join(campos)


def main():
    dados = list(textos())
    print('linhas varridas: %d' % len(dados))
    linhas = ['# RV-14 — Consistência de terminologia no jogo', '',
              'Gerado por `tools/check_terminologia.py`. Para cada conceito, a **distribuição das',
              'variantes** nos cinco corpora do censo. Onde há mais de uma em uso, a **maioria** é o',
              'padrão a seguir (regra do projeto, a mesma que fechou o caso `Crippled` × `Slow`).', '',
              '> Limite honesto: a lista de conceitos é **curada à mão** — não existe thesaurus do',
              '> vocabulário do jogo. Conceito novo entra quando a revisão encontra.', '',
              '| conceito | variante | total | skills | status | itens | afixos | powerups |', '',
              '|---|---|---|---|---|---|---|---|']
    achados = 0
    for conceito, variantes in CONCEITOS.items():
        por_var = OrderedDict()
        for v in variantes:
            por_var[v] = Counter()
        for corpus, txt in dados:
            low = txt.lower()
            for v in variantes:
                n = len(re.findall(v, low))
                if n:
                    por_var[v][corpus] += n
        total_geral = sum(sum(c.values()) for c in por_var.values())
        if total_geral == 0:
            continue
        usadas = [(v, c) for v, c in por_var.items() if sum(c.values())]
        if len(usadas) > 1:
            achados += 1
        for v, c in sorted(por_var.items(), key=lambda kv: -sum(kv[1].values())):
            t = sum(c.values())
            if t == 0:
                continue
            linhas.append('| %s | `%s` | %d | %d | %d | %d | %d | %d |' % (
                conceito if v == variantes[0] else '',
                v.replace('\\b', ''), t, c['skills'], c['status'], c['itens'], c['afixos'], c['powerups']))
    linhas += ['', '**Conceitos com mais de uma variante em uso: %d de %d.** Cada linha desses é' % (
        achados, len(CONCEITOS)), 'candidata a padronização pela maioria — nunca por gosto.', '',
        '## Como fechar um caso', '',
        '1. Conte as variantes aqui (é o "a maioria escreve como?").',
        '2. Confirme qual delas o **motor** usa de fato (nome do status/atributo no decompilado).',
        '3. Se o motor e a maioria coincidem, alinhe os textos minoritários.',
        '4. Se o motor contradiz a maioria (caso `Cripple` → status `Slow`), registre a contradição',
        '   e NÃO mexa: foi a decisão tomada para o `Crippled` × `Slow`.', '']
    os.makedirs(os.path.dirname(REL), exist_ok=True)
    io.open(REL, 'w', encoding='utf-8', newline='\n').write('\n'.join(linhas) + '\n')
    print('conceitos com variantes divergentes: %d de %d' % (achados, len(CONCEITOS)))
    print('relatorio: %s' % REL)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
