#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detector GENERICO de credencial. Nao contem nenhum valor de token - so FORMATOS e
medidas estatisticas, para pegar o que ainda nao tem nome conhecido.

Roda sobre os arquivos versionados (o que o GitHub publica). Exit 1 se achar qualquer coisa.
E o motor do passo 0 do release-check e do passo 1 do CI.
"""
import io
import math
import os
import re
import subprocess
import sys
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# FORMATOS conhecidos. Sao padroes de prefixo, NAO valores: um valor nunca entra aqui.
FORMATOS = [
    (r'\bgithub_pat_[A-Za-z0-9_]{20,}', 'PAT fine-grained do GitHub'),
    (r'\bgh[pousr]_[A-Za-z0-9]{30,}', 'token do GitHub (classico/OAuth/app)'),
    (r'\btss_[A-Za-z0-9]{20,}', 'token do Thunderstore'),
    (r'\bxox[baprs]-[A-Za-z0-9-]{10,}', 'token do Slack'),
    (r'\bsk-[A-Za-z0-9]{20,}', 'chave da OpenAI/Anthropic'),
    (r'\bAKIA[0-9A-Z]{16}\b', 'chave de acesso da AWS'),
    (r'\bAIza[0-9A-Za-z_-]{35}\b', 'chave da API do Google'),
    (r'\bglpat-[A-Za-z0-9_-]{20,}', 'token do GitLab'),
    (r'\bnpm_[A-Za-z0-9]{36}\b', 'token do npm'),
    (r'-----BEGIN [A-Z ]*PRIVATE KEY-----', 'chave privada PEM'),
    (r'\bx-access-token:', 'URL de clone/push com token embutido'),
    (r'\bBasic\s+[A-Za-z0-9+/=]{24,}', 'credencial Basic embutida'),
    (r'(?i)\b(pass(?:word|wd)?|secret|token|api[_-]?key|auth)\b\s*[:=]\s*["\']?[A-Za-z0-9_\-]{24,}', 'atribuicao com valor longo'),
]

# Estrutural: string longa e de alta entropia (pega o que ainda nao tem prefixo conhecido).
CANDIDATO = re.compile(r'[A-Za-z0-9_\-+/=]{32,}')
LIMIAR_ENTROPIA = 4.0       # bits por caractere
LIMIAR_COMPRIMENTO = 32


def parece_segredo(v):
    """Decide por CARACTERISTICA, sem lista de excecoes (excecao apodrece).

    Credencial de verdade: alta entropia, varios DIGITOS, mistura de maiuscula e minuscula,
    e nao parece caminho, URL, hash hex nem nome de arquivo/classe. Calibrado contra os 10
    falsos positivos reais do repositorio (todos tinham 0 ou 1 digito).
    """
    if any(c in v for c in '/@:<>') or chr(92) in v:   # caminho, URL, e-mail, separador
        return False
    if re.fullmatch(r'[0-9a-fA-F]+', v):                 # hash hex (commit, md5, pid de asset)
        return False
    if re.fullmatch(r'[A-Za-z]+', v):                    # so letras = identificador/palavra
        return False
    if len(re.findall(r'[0-9]', v)) < 4:                 # segredo tem varios digitos
        return False
    if not (re.search(r'[A-Z]', v) and re.search(r'[a-z]', v)):
        return False
    if re.fullmatch(r'[a-z][A-Za-z0-9]*', v) and len(re.findall(r'[0-9]', v)) < 6:
        return False                                     # camelCase com poucos digitos
    return entropia(v) >= LIMIAR_ENTROPIA

# Arquivos que por natureza contem os FORMATOS como exemplo (esta lista nao e um valor).
ISENTOS = {
    'tools/check_segredos.py',
    'tools/check_padroes_segredo.py',
    'docs/AMBIENTE.md',
    'docs/README.md',
    'docs/CI.md',
    'docs/PUBLICACAO.md',
}


def entropia(s):
    if not s:
        return 0.0
    c = Counter(s)
    n = float(len(s))
    return -sum((v / n) * math.log(v / n, 2) for v in c.values())


def mascara(s):
    """Nunca devolve o valor: so o prefixo, o tamanho e a entropia."""
    pre = s[:14] if len(s) > 14 else s[:4]
    return '%s<...> (%d chars, entropia %.1f)' % (pre, len(s), entropia(s))


def main():
    arqs = subprocess.run(['git', 'ls-files'], cwd=RAIZ,
                          stdout=subprocess.PIPE).stdout.decode('utf-8', 'replace').splitlines()
    achados = []
    binarios = 0
    for f in arqs:
        if f in ISENTOS:
            continue
        try:
            bruto = io.open(os.path.join(RAIZ, f), 'rb').read()
        except IOError:
            continue
        s = bruto.decode('utf-8', 'ignore')
        # A regra de ENTROPIA so vale para TEXTO. Num binario (PNG de screenshot/arte, DLL)
        # qualquer sequencia de 32+ caracteres base64-like e alta entropia POR NATUREZA: o
        # heuristico acusava a arte de icone versionada em docs/img/ (falso positivo que travava
        # o passo 0 do release-check). Os FORMATOS conhecidos (tss_, ghp_, ...) continuam sendo
        # procurados em TODOS os arquivos, binarios inclusive - o que muda e so o heuristico.
        eh_texto = b'\x00' not in bruto
        if eh_texto:
            try:
                bruto.decode('utf-8')
            except UnicodeDecodeError:
                eh_texto = False
        if not eh_texto:
            binarios += 1
        for i, linha in enumerate(s.split(chr(10)), 1):
            for pat, rot in FORMATOS:
                for m in re.finditer(pat, linha):
                    achados.append('%s:%d  FORMATO  %s' % (f, i, rot))
            if not eh_texto:
                continue
            for m in CANDIDATO.finditer(linha):
                v = m.group(0)
                if not parece_segredo(v) or len(v) < LIMIAR_COMPRIMENTO:
                    continue
                achados.append('%s:%d  ENTROPIA %s' % (f, i, mascara(v)))

    print('arquivos versionados analisados: %d' % len(arqs))
    print('  (%d binario(s) fora do heuristico de entropia; os formatos conhecidos foram '
          'procurados neles tambem)' % binarios)
    print('formatos conhecidos: %d | limiar de entropia: %.1f bits/char | comprimento minimo: %d'
          % (len(FORMATOS), LIMIAR_ENTROPIA, LIMIAR_COMPRIMENTO))
    if achados:
        print()
        print('!! POSSIVEL CREDENCIAL NO QUE SERIA PUBLICADO:')
        for a in achados[:40]:
            print('   ' + a)
        if len(achados) > 40:
            print('   ... e mais %d' % (len(achados) - 40))
        print()
        print('   Nada de valor fixo pode entrar no repositorio. Tire o valor, use arquivo fora do')
        print('   repo ou secret, e ROTACIONE se ele ja chegou a ser exposto.')
        return 1
    print('  ==> nenhum padrao de credencial encontrado')
    return 0


if __name__ == '__main__':
    sys.exit(main())
