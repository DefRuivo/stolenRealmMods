#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""censo_status.py - cria/mantem o censo de revisao dos STATUS (RV-9).

POR QUE EXISTE
--------------
O RV-9 pede "revisar todos os buffs e debuffs e seus tooltips, na mesma linha de formato
das skills". Nas 11 arvores de skill o primeiro passo foi sempre o mesmo: CENSO. Sem ele
nao da para saber o que falta, nem medir progresso.

DIFERENCA EM RELACAO AO CENSO DE SKILLS
---------------------------------------
As skills tinham uma coluna de status desde o inicio. Os status NAO: o `status.csv` (560
entradas) tem nome/tipo/raridade/efeitos/efeitosDano/nEfeitosDano/classe/descricao. Entao
este script ADICIONA a coluna `revisao` (default `pendente`), preservando tudo o que ja
existe - rodar de novo nunca perde trabalho.

O CORTE buff x debuff
---------------------
Ainda NAO esta no CSV. Depende do `BenefitType` do status/efeitos (em investigacao). Ate
la o censo agrupa pelo que EXISTE: `tipo` (Normal 457 / Fortune 83 / Quest 14 / QuestItem 6).
O alvo do pedido do usuario sao os `Normal`, onde vivem buffs e debuffs.

USO
---
    python tools/censo_status.py            # atualiza a coluna e reescreve o relatorio
    python tools/censo_status.py --resumo    # so imprime os numeros
"""
import csv
import io
import os
import sys
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(RAIZ, 'docs', 'cobertura', 'status.csv')
REL = os.path.join(RAIZ, 'docs', 'cobertura', 'revisao', 'RV-9-censo.md')
COLUNA = 'revisao'
VEREDITOS = ('pendente', 'revisado', 'corrigido', 'sem-explicacao', 'intocavel')


def carrega():
    with io.open(CSV, encoding='utf-8') as fh:
        leitor = csv.DictReader(fh)
        campos = list(leitor.fieldnames)
        return list(leitor), campos


def salva(linhas, campos):
    with io.open(CSV, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        w.writerows(linhas)


def main():
    linhas, campos = carrega()
    novo = COLUNA not in campos
    if novo:
        campos.append(COLUNA)
    for r in linhas:
        if not r.get(COLUNA):
            r[COLUNA] = 'pendente'
    if novo:
        salva(linhas, campos)

    por_tipo = Counter(r['tipo'] for r in linhas)
    por_revisao = Counter(r[COLUNA] for r in linhas)
    print('status.csv: %d entradas' % len(linhas))
    print('  por tipo  : %s' % dict(por_tipo.most_common()))
    print('  por revisao: %s' % dict(por_revisao.most_common()))
    if '--resumo' in sys.argv:
        return 0

    normal = [r for r in linhas if r['tipo'] == 'Normal']
    pend = [r for r in normal if r[COLUNA] == 'pendente']
    partes = [
        '# RV-9 — Censo dos status (buffs e debuffs)',
        '',
        'Gerado por `tools/censo_status.py`. **Alvo do pedido:** revisar todos os buffs e',
        'debuffs e seus tooltips, **na mesma linha de formato das skills** (o processo completo',
        'está descrito no RV-9 do `KANBAN.md`).',
        '',
        '## Onde estamos',
        '',
        '| grupo | entradas | pendentes |',
        '|---|---|---|',
    ]
    for tipo, n in por_tipo.most_common():
        p = len([r for r in linhas if r['tipo'] == tipo and r[COLUNA] == 'pendente'])
        partes.append('| `%s` | %d | %d |' % (tipo, n, p))
    partes += [
        '',
        '**Pendentes no grupo `Normal` (buffs/debuffs): %d de %d.**' % (len(pend), len(normal)),
        '',
        '> O corte **buff x debuff** ainda não está no CSV: depende do `BenefitType` do status',
        '> (em investigação por agente). Enquanto isso o agrupamento é pelo `tipo` do asset.',
        '> Quando o campo for dumpado, este censo ganha a coluna e a fila é reordenada:',
        '> **Harmful (debuffs) → Beneficial (buffs) → Quest/Fortune/resto**.',
        '',
        '## Fila de trabalho (primeiros 60 pendentes de `Normal`)',
        '',
        '| nome | raridade | efeitos | revise |',
        '|---|---|---|---|',
    ]
    for r in pend[:60]:
        ef = (r['efeitos'] or r['efeitosDano'] or '')[:70].replace('|', '/')
        partes.append('| `%s` | %s | %s | ⬜ |' % (r['nome'][:38], r['raridade'], ef))
    partes += [
        '',
        '## Como o veredito entra',
        '',
        'Os mesmos quatro estados das skills, na coluna `%s` do `status.csv`:' % COLUNA,
        '- `revisado` — conferido no asset/código, texto de pé;',
        '- `corrigido` — o texto mudou (entra no `TextFixes`);',
        '- `sem-explicacao` — omissão **por design** (ex.: os sorteios do Chaos);',
        '- `intocavel` — não se mexe (ex.: árvore Bard).',
        '',
        'Status **não** estão no dicionário de localização: são campos brutos do asset, então a',
        'correção é em **runtime (Harmony)**, não em tabela de texto.',
    ]
    os.makedirs(os.path.dirname(REL), exist_ok=True)
    io.open(REL, 'w', encoding='utf-8', newline='\n').write('\n'.join(partes) + '\n')
    print('relatorio: %s' % REL)
    return 0


if __name__ == '__main__':
    sys.exit(main())
