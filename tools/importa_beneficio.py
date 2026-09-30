#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""importa_beneficio.py - traz a classificacao buff/debuff do LOG para o status.csv.

POR QUE EXISTE
--------------
O corte buff x debuff era o que faltava para abrir o RV-9. Ele nao existe no `status.csv`
(nem em campo do asset que este script pudesse ler antes), mas passou a sair no dump:

    [Status] 'Vitality' | tipo=Normal | ... | modelo=- | beneficio=Buff | desc="..."

Fonte do valor: `ActionStatusInfo.IsBeneficial` / `IsHarmful`, computados de `SkillTags`
(l.319287/319428/319430 do decompilado). NAO e o `BenefitType` da linha 101478 - esse e da
classe `EventStatus` (status de evento), nao do status normal.

USO
---
    python tools/importa_beneficio.py            # le o log e atualiza o status.csv
    python tools/importa_beneficio.py --log CAMINHO

Depois dele, rode `python tools/censo_status.py` para ver a fila reordenada.
"""
import csv
import io
import os
import re
import sys
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(RAIZ, 'docs', 'cobertura', 'status.csv')
LOG_PADRAO = os.path.join(
    os.environ.get('APPDATA', ''),
    'r2modmanPlus-local', 'StolenRealm', 'profiles', 'Default', 'BepInEx', 'LogOutput.log')
COLUNA = 'beneficio'
LINHA = re.compile(r"\[Status\] '([^']*)'.*?beneficio=([A-Za-z]+)")


def le_log(caminho):
    if not os.path.exists(caminho):
        print('log nao encontrado: %s' % caminho)
        return {}
    achados = {}
    for l in io.open(caminho, encoding='utf-8', errors='replace'):
        m = LINHA.search(l)
        if m:
            nome, valor = m.group(1), m.group(2)
            if nome in achados and achados[nome] != valor:
                print('  AVISO: %r aparece como %s e %s' % (nome, achados[nome], valor))
            achados[nome] = valor
    return achados


def main():
    log = LOG_PADRAO
    if '--log' in sys.argv:
        log = sys.argv[sys.argv.index('--log') + 1]
    achados = le_log(log)
    print('status lidos do log: %d' % len(achados))
    if not achados:
        return 1

    with io.open(CSV, encoding='utf-8') as fh:
        leitor = csv.DictReader(fh)
        campos = list(leitor.fieldnames)
        linhas = list(leitor)
    if COLUNA not in campos:
        campos.append(COLUNA)

    sem = 0
    for r in linhas:
        v = achados.get(r['nome'])
        if v:
            r[COLUNA] = v
        elif not r.get(COLUNA):
            r[COLUNA] = '?'
            sem += 1

    with io.open(CSV, 'w', encoding='utf-8', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        w.writerows(linhas)

    print('por beneficio: %s' % dict(Counter(r[COLUNA] for r in linhas).most_common()))
    if sem:
        print('sem classificacao (nao apareceram no log): %d' % sem)
    print('status.csv atualizado.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
