#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_status_numeros.py - RV-9: confere os NUMEROS da descricao do status contra os efeitos.

A REGRA QUE ESTE SCRIPT APLICA
------------------------------
No RV-8b (as 451 skills) o que fechou quase tudo foi uma pergunta so: **o numero que o texto
promete existe no asset?** Aqui e a mesma pergunta, aplicada aos status, em escala (sao 560).

Como ler o resultado (importante)
---------------------------------
Este script NAO decide defeito. Ele monta a TRIAGEM: separa os casos em que todo numero da
descricao tem um numero correspondente nos efeitos (ruido baixo) dos casos em que a descricao
cita um numero que nao existe em efeito nenhum (candidatos a omissao ou a defeito real, que a
leitura manual confirma). Muito do que ele marca e falso positivo por natureza - duracao
("for 2 turns") nao mora nos efeitos, mora no campo de duracao; percentuais de descricao
podem vir de `StatusPower`.

Fontes: `docs/cobertura/status.csv` (nome, tipo, efeitos, efeitosDano, descricao).
Saida : `docs/cobertura/revisao/RV-9-numeros.md` (fora do git, como os outros .md).

Uso: python tools/check_status_numeros.py [--grupo Normal]
"""
import csv
import io
import os
import re
import sys
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(RAIZ, 'docs', 'cobertura', 'status.csv')
REL = os.path.join(RAIZ, 'docs', 'cobertura', 'revisao', 'RV-9-numeros.md')

# palavras que indicam duracao/contagem estrutural: nao precisam de par nos efeitos
DURACAO = re.compile(r'\b(turn|turns|second|seconds|round|rounds|stack|stacks|hex|hexes)\b', re.I)


def numeros(txt):
    """Numeros REAIS da descricao. Duas exclusoes aprendidas na primeira rodada:
    (a) `[0]`/`[10]` sao TOKENS de template do jogo - o valor real vem do efeito (`[0]` casou
        com `DamageModCold:Base:2` e marcou os 6 `Affinity` como suspeitos, todos corretos);
    (b) numero colado em unidade estrutural (turn/stack/hex) e DURACAO ou CONTAGEM, que mora
        em campo proprio, nao nos efeitos ("Lasts 5 turns" marcou o `Ascendancy`).
    """
    limpo = re.sub(r'\[[^\]]*\]', ' ', txt or '')
    # (c) `*0` tambem e TOKEN de expressao de dano (mesma familia do `[0]`, licao do RV-8a)
    limpo = re.sub(r'\*\s*\d+(?:[.,]\d+)?', ' ', limpo)
    limpo = re.sub(r'\d+\s*(?:turn|turns|stack|stacks|hex|hexes|round|rounds)', ' ', limpo, flags=re.I)
    return set(re.findall(r'\d+(?:[.,]\d+)?', limpo))


def valores_dos_efeitos(efeitos):
    """`Efeito:Base:50, Outro:Percentage:-10` -> {50, -10} (so o que vem depois do ultimo ':')."""
    out = set()
    for pedaco in (efeitos or '').split(','):
        if ':' not in pedaco:
            continue
        valor = pedaco.rsplit(':', 1)[-1].strip()
        for n in re.findall(r'\d+(?:[.,]\d+)?', valor):
            out.add(n)
    return out


def main():
    grupo = 'Normal'
    if '--grupo' in sys.argv:
        grupo = sys.argv[sys.argv.index('--grupo') + 1]
    with io.open(CSV, encoding='utf-8') as fh:
        linhas = [r for r in csv.DictReader(fh) if r.get('tipo') == grupo]

    limpos, triagem = [], []
    for r in linhas:
        desc = r.get('descricao') or ''
        ef = (r.get('efeitos') or '') + ' ' + (r.get('efeitosDano') or '')
        nd, ne = numeros(desc), valores_dos_efeitos(ef)
        sobra = nd - ne
        if not nd and not ef.strip():
            continue                      # sem texto e sem efeito: nada a conferir aqui
        if sobra:
            triagem.append((r, sorted(sobra)))
        else:
            limpos.append(r)

    print('grupo `%s`: %d status' % (grupo, len(linhas)))
    print('  todo numero da descricao tem par nos efeitos : %d' % len(limpos))
    print('  com numero sem par (triagem manual)          : %d' % len(triagem))
    print('  por forma do texto: %s' % dict(Counter(
        'cita duracao' if DURACAO.search(r.get('descricao') or '') else 'sem duracao'
        for r in linhas).most_common()))

    p = ['# RV-9 — Triagem dos números (grupo `%s`)' % grupo, '',
         'Gerado por `tools/check_status_numeros.py`. **Isto é triagem, não veredito**: o script',
         'não julga se o texto está certo — separa quem cita um número que **não existe em efeito',
         'nenhum** do asset, que é onde o defeito ou a omissão costuma estar.', '',
         '## Números', '',
         '| o que | quantos |', '|---|---|',
         '| status no grupo | %d |' % len(linhas),
         '| todo número da descrição tem par nos efeitos | %d |' % len(limpos),
         '| com número sem par — conferir | **%d** |' % len(triagem), '',
         '> Falsos positivos esperados: **duração** ("for 2 turns") não mora nos efeitos — mora no',
         '> campo de duração; percentuais podem vir de `StatusPower`. Conferir sempre o texto',
         '> COMPLETO antes de decidir (lição do RV-8c: uma nota redundante no `Meteor`).', '',
         '## Fila de triagem', '',
         '| status | tipo | número sem par | descrição | efeitos |', '|---|---|---|---|---|']
    for r, sobra in triagem:
        desc = (r.get('descricao') or '').replace('|', '/')[:78]
        ef = (r.get('efeitos') or r.get('efeitosDano') or '').replace('|', '/')[:58]
        p.append('| `%s` | %s | %s | %s | %s |' % (r['nome'][:30], r['raridade'], ','.join(sobra), desc, ef))

    os.makedirs(os.path.dirname(REL), exist_ok=True)
    io.open(REL, 'w', encoding='utf-8', newline='\n').write('\n'.join(p) + '\n')
    print('relatorio: %s' % REL)
    return 0


if __name__ == '__main__':
    sys.exit(main())
