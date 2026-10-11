"""Proveniência documental estreita: uma ocorrência num snapshot, nunca uma pasta.

O registro não prova existência no clone nem autoriza rodar ferramentas privadas.
Só distingue frases preservadas da história de instruções atuais. Mudança no
snapshot, linha, nome ou categoria invalida a declaração (falha fechada).
"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

ARQUIVO = 'tools/audita_docs_proveniencia.json'
SCHEMA = 'audita-docs/proveniencia/1'
CATEGORIAS = {'ferramenta-local', 'caminho-historico'}
CAMPOS = {'documento', 'linha', 'categoria', 'nome', 'sha256_documento',
          'sha256_linha', 'origem', 'justificativa'}


def sha_texto(texto):
    """UTF-8 com CRLF normalizado; independente do checkout Windows/Linux."""
    return hashlib.sha256(texto.replace('\r\n', '\n').encode('utf-8')).hexdigest()


def carregar(raiz, documentos):
    """Retorna (ocorrências válidas por chave exata, erros explícitos do catálogo)."""
    raiz = Path(raiz)
    erros = []
    validas = {}
    try:
        registro = json.loads((raiz / ARQUIVO).read_text(encoding='utf-8'))
    except (OSError, UnicodeError, ValueError) as exc:
        return {}, ['proveniencia: registro ausente/ilegivel (%s)' % type(exc).__name__]
    if (not isinstance(registro, dict) or registro.get('schema') != SCHEMA
            or not isinstance(registro.get('ocorrencias'), list)):
        return {}, ['proveniencia: schema/ocorrencias invalidos']
    documentos = set(documentos)
    cache = {}
    vistas = set()
    for n, item in enumerate(registro['ocorrencias'], 1):
        erro = None
        if not isinstance(item, dict) or set(item) != CAMPOS:
            erros.append('proveniencia: registro %d tem campos invalidos' % n)
            continue
        doc, linha, categoria, nome = (item[k] for k in ('documento', 'linha', 'categoria', 'nome'))
        if (not isinstance(doc, str) or '\\' in doc or PurePosixPath(doc).is_absolute()
                or '..' in PurePosixPath(doc).parts or doc not in documentos
                or type(linha) is not int or linha < 1
                or not isinstance(categoria, str) or categoria not in CATEGORIAS
                or not isinstance(nome, str) or not nome.strip()
                or any(not isinstance(item[k], str) or not item[k].strip()
                       for k in ('origem', 'justificativa'))
                or any(not isinstance(item[k], str) or not re.fullmatch('[0-9a-f]{64}', item[k])
                       for k in ('sha256_documento', 'sha256_linha'))):
            erros.append('proveniencia: registro %d tem identidade/origem invalidas' % n)
            continue
        chave = (doc, linha, categoria, nome)
        if chave in vistas:
            erros.append('proveniencia: registro duplicado %s:%d (%s)' % (doc, linha, nome))
            validas.pop(chave, None)
            continue
        vistas.add(chave)
        if doc not in cache:
            try:
                cache[doc] = (raiz / doc).read_text(encoding='utf-8')
            except (OSError, UnicodeError):
                cache[doc] = None
        texto = cache[doc]
        linhas = texto.splitlines() if texto is not None else []
        if texto is None or sha_texto(texto) != item['sha256_documento']:
            erro = 'snapshot ausente/alterado'
        elif linha > len(linhas) or nome not in linhas[linha - 1]:
            erro = 'ocorrencia ausente'
        elif sha_texto(linhas[linha - 1]) != item['sha256_linha']:
            erro = 'linha alterada'
        if erro:
            erros.append('proveniencia: %s:%d (%s): %s' % (doc, linha, nome, erro))
        else:
            validas[chave] = item
    return validas, erros


def reconhece(registros, documento, linha, categoria, nome):
    return (documento, linha, categoria, nome) in registros
