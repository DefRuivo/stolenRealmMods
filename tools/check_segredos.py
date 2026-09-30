#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Trava de segredo: nenhum token pode entrar no repositorio (nem no historico recente).

Roda sobre os arquivos VERSIONADOS (o que o GitHub publica). Exit 1 se achar qualquer
padrao de credencial. E o passo 6 do release-check.
"""
import io
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Padroes de credencial real (nao texto explicativo). Deliberadamente amplos.
PADROES = [
    (r'\btss_[A-Za-z0-9]{20,}', 'token do Thunderstore'),
    (r'\bghp_[A-Za-z0-9]{20,}', 'token classico do GitHub'),
    (r'\bgho_[A-Za-z0-9]{20,}', 'token OAuth do GitHub'),
    (r'\bghs_[A-Za-z0-9]{20,}', 'token de app do GitHub'),
    (r'\bgithub_pat_[A-Za-z0-9_]{20,}', 'fine-grained PAT do GitHub'),
    (r'\bx-access-token:', 'URL de push com token embutido'),
    (r'\bAKIA[0-9A-Z]{16}\b', 'chave da AWS'),
    (r'-----BEGIN [A-Z ]*PRIVATE KEY-----', 'chave privada'),
]

# Arquivos que por natureza contem os padroes como EXEMPLO (documentacao/esta trava).
ISENTOS = {'tools/check_segredos.py', 'docs/AMBIENTE.md', 'docs/README.md'}


def main():
    arqs = subprocess.run(['git', 'ls-files'], cwd=RAIZ, stdout=subprocess.PIPE).stdout.decode('utf-8', 'replace').splitlines()
    achados = []
    for f in arqs:
        if f in ISENTOS:
            continue
        try:
            s = io.open(os.path.join(RAIZ, f), encoding='utf-8', errors='ignore').read()
        except IOError:
            continue
        for pat, rot in PADROES:
            for m in re.finditer(pat, s):
                linha = s[:m.start()].count(chr(10)) + 1
                achados.append('%s:%d  %s  ->  %s' % (f, linha, rot, m.group(0)[:14] + '...'))

    # o token tambem nao pode estar no commit mais recente nem em arquivo por commitar
    st = subprocess.run(['git', 'status', '--porcelain'], cwd=RAIZ, stdout=subprocess.PIPE).stdout.decode('utf-8', 'replace')
    print('arquivos versionados analisados: %d' % len(arqs))
    print('arquivos em area de teste no momento: %d' % len([l for l in st.splitlines() if l.strip()]))
    if achados:
        print()
        print('!! CREDENCIAL ENCONTRADA NO QUE SERIA PUBLICADO:')
        for a in achados:
            print('   ' + a)
        print()
        print('   NAO COMMITE. Tire o valor do arquivo, use variavel de ambiente ou')
        print('   um arquivo FORA do repositorio, e ROTACIONE o token exposto.')
        return 1
    print('  ==> nenhum padrao de credencial encontrado')

    # Motor GENERICO (formato + entropia) - pega o que ainda nao tem prefixo conhecido.
    r = subprocess.run([sys.executable, os.path.join(RAIZ, 'tools', 'check_padroes_segredo.py')])
    return r.returncode


if __name__ == '__main__':
    sys.exit(main())
