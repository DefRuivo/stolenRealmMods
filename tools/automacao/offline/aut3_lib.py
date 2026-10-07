#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Nucleo da bancada offline AUT-3.

Funcoes puras/reutilizaveis: hash de arquivo, execucao de comando com timeout e
captura de exit code, e a REGRA DE VEREDITO. A regra e a razao de existir do
modulo: um comando que falha, que nao existe ou que estoura o timeout NUNCA vira
verde, e "nao exercitado" e um estado SEPARADO de OK (nunca somado a verde).

Sem dependencia externa: so a stdlib.
"""
import hashlib
import os
import re
import subprocess
import sys
import tempfile
import time

# Estados possiveis de UM item verificado.
OK = "OK"
REPROVOU = "REPROVOU"
NAO_EXERCITADO = "NAO_EXERCITADO"

# FORMATOS de credencial (os MESMOS dos scanners publicos tools/check_segredos.py e
# tools/check_padroes_segredo.py). Aqui servem so para LIMPAR capturas antes de
# serializar - nunca para revelar valor. Nenhum valor entra nesta lista.
PADROES_SEGREDO = [
    r'\btss_[A-Za-z0-9]{20,}',
    r'\bgh[pousr]_[A-Za-z0-9]{20,}',
    r'\bgithub_pat_[A-Za-z0-9_]{20,}',
    r'\bx-access-token:[A-Za-z0-9_\-]+',
    r'\bsk-[A-Za-z0-9]{20,}',
    r'\bAIza[0-9A-Za-z_-]{35}\b',
    r'\bglpat-[A-Za-z0-9_-]{20,}',
    r'\bnpm_[A-Za-z0-9]{36}\b',
    r'\bxox[baprs]-[A-Za-z0-9-]{10,}',
    r'\bAKIA[0-9A-Z]{16}\b',
    r'-----BEGIN [A-Z ]*PRIVATE KEY-----',
    r'\bBasic\s+[A-Za-z0-9+/=]{24,}',
]


# AUT-3F2 (A2): formatos EXPLICITOS da 2a linha de defesa (sanitiza). Nao ha
# promessa de pegar qualquer segredo arbitrario - o que nao casar um destes
# formatos nao e mascarado (a lista e explicita e revisavel).
_ROTULO_SEGREDO = (r'(?:pass(?:word|wd|phrase)|secret|token|api[_-]?key|apikey|'
                   r'auth(?:orization)?|auth[_-]?token|access[_-]?key|'
                   r'client[_-]?secret|private[_-]?key|credential)')
# valor entre aspas (a chave tambem pode vir entre aspas, ex.: JSON)
_RE_ASSIGN_QUOTED = re.compile(
    r'(?i)(\b' + _ROTULO_SEGREDO + r'\b\s*)(["\']?\s*[:=]\s*)(["\'])([^"\']*)\3')
# valor sem aspas (>= 6 chars, sem espaco/aspas/virgula/ponto-e-virgula)
_RE_ASSIGN_BARE = re.compile(
    r'(?i)(\b' + _ROTULO_SEGREDO + r'\b\s*)(["\']?\s*[:=]\s*)([^\s"\'`,;]{6,})')
# bloco PEM INTEIRO; se a captura truncou (sem rodape), vai ate o fim do texto.
_RE_PEM = re.compile(
    r'-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----.*?(?:-----END [A-Z0-9 ]*PRIVATE KEY-----|\Z)',
    re.S)


def _redigir_assign_quoted(m):
    """Mantem rotulo + separador + aspas; troca SO o valor.

    As aspas de abertura e de fechamento sao o MESMO grupo (3 / backreference).
    """
    return "%s%s%s<REDACTED>%s" % (m.group(1), m.group(2), m.group(3), m.group(3))


def _redigir_assign_bare(m):
    """Mantem rotulo + separador; troca SO o valor."""
    return "%s%s<REDACTED>" % (m.group(1), m.group(2))


def sanitiza(texto):
    """Troca credenciais reconheciveis por <REDACTED>, preservando o contexto.

    Usado ANTES de serializar stdout/stderr de subprocessos: o runner nao pode
    gravar valor NEM prefixo de token em JSON/log. Nao esconde o estado de falha -
    exit code e rotulo do motivo continuam intactos.

    AUT-3F2 (A2): alem dos prefixos conhecidos, cobre EXPLICITAMENTE:
      * o bloco PEM INTEIRO (cabecalho + corpo base64 + rodape) e o mesmo bloco
        quando a captura o truncou (sem o rodape);
      * atribuicao generica (password/secret/token/api_key/...) com valor entre
        aspas ou sem aspas, PRESERVANDO o nome da chave e o separador.
    """
    if not texto:
        return texto
    # 1. bloco PEM inteiro (inclusive truncado): antes de tudo, senao o corpo
    #    base64 sobreviveria e ainda seria cortado em fragmento.
    texto = _RE_PEM.sub("<REDACTED>", texto)
    # 2. atribuicoes genericas: preservam rotulo e separador (contexto).
    texto = _RE_ASSIGN_QUOTED.sub(_redigir_assign_quoted, texto)
    texto = _RE_ASSIGN_BARE.sub(_redigir_assign_bare, texto)
    # 3. prefixos de credencial conhecidos.
    for pat in PADROES_SEGREDO:
        texto = re.sub(pat, "<REDACTED>", texto)
    return texto


def area_trabalho():
    """Base segura para artefatos temporarios dos testes (AUT-3F2/A3).

    NUNCA a Temp local do Windows por padrao. Ordem de preferencia:
      $BH_AGENT_WORKSPACE -> $TMPDIR -> <LOCALAPPDATA>/hermes/cache/scratch
      -> tempfile.gettempdir() (ultimo recurso).
    Exporta TMP/TEMP/TMPDIR para a base, de modo que subprocessos (git, python)
    herdem a area de trabalho segura em vez da Temp local.
    """
    candidatos = [os.environ.get("BH_AGENT_WORKSPACE"), os.environ.get("TMPDIR")]
    local = os.environ.get("LOCALAPPDATA")
    if local:
        candidatos.append(os.path.join(local, "hermes", "cache", "scratch"))
    base = None
    for cand in candidatos:
        if not cand:
            continue
        try:
            os.makedirs(cand, exist_ok=True)
        except OSError:
            continue
        if os.path.isdir(cand):
            base = cand
            break
    if base is None:
        base = tempfile.gettempdir()
    for var in ("TMPDIR", "TEMP", "TMP"):
        os.environ[var] = base
    return base



def sha256_file(caminho):
    """sha256 hex do arquivo, ou None se nao existir / nao puder ser lido."""
    if not caminho or not os.path.isfile(caminho):
        return None
    h = hashlib.sha256()
    try:
        with open(caminho, "rb") as fh:
            for bloco in iter(lambda: fh.read(1 << 20), b""):
                h.update(bloco)
    except OSError:
        return None
    return h.hexdigest()


def sha256_bytes(dados):
    return hashlib.sha256(dados).hexdigest()


def snapshot_arquivos(caminhos):
    """{nome_base: sha256|None} - a base de comparacao antes/depois.

    Se dois caminhos tiverem o mesmo nome base, o ultimo vence: o uso do projeto
    e por diretorio de mod, onde o nome base (a DLL) identifica o artefato.
    """
    return {os.path.basename(c): sha256_file(c) for c in caminhos}


def run_cmd(argv, cwd=None, timeout=300, env=None):
    """Roda um comando isolado e devolve o resultado CRU, sem julgar.

    Chaves: comando, cwd, exit_code (int|None), segundos, timeout (bool),
    erro_lancamento (str|None), stdout, stderr.
    """
    ambiente = dict(os.environ)
    ambiente.setdefault("PYTHONIOENCODING", "utf-8")
    ambiente.setdefault("PYTHONDONTWRITEBYTECODE", "1")
    if env:
        ambiente.update(env)
    inicio = time.monotonic()
    try:
        proc = subprocess.run(
            argv, cwd=cwd, env=ambiente, timeout=timeout,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, encoding="utf-8", errors="replace",
        )
        return {
            "comando": list(argv), "cwd": cwd, "exit_code": proc.returncode,
            "segundos": round(time.monotonic() - inicio, 3), "timeout": False,
            "erro_lancamento": None, "stdout": proc.stdout or "", "stderr": proc.stderr or "",
        }
    except subprocess.TimeoutExpired:
        return {
            "comando": list(argv), "cwd": cwd, "exit_code": None,
            "segundos": round(time.monotonic() - inicio, 3), "timeout": True,
            "erro_lancamento": "timeout apos %ss" % timeout, "stdout": "", "stderr": "",
        }
    except OSError as erro:
        return {
            "comando": list(argv), "cwd": cwd, "exit_code": None,
            "segundos": round(time.monotonic() - inicio, 3), "timeout": False,
            "erro_lancamento": "%s: %s" % (type(erro).__name__, erro), "stdout": "", "stderr": "",
        }


def avalia(resultado, esperado=0):
    """Do resultado CRU para o estado do item. A regra que nao se dobra:

    - rodou e o exit bate com o esperado ................ OK
    - rodou e o exit NAO bate (inclusive erro de build) .. REPROVOU
    - NAO rodou (timeout / comando inexistente) ......... NAO_EXERCITADO
    """
    if resultado.get("timeout") or resultado.get("erro_lancamento"):
        return NAO_EXERCITADO
    if resultado.get("exit_code") == esperado:
        return OK
    return REPROVOU


def veredito(itens):
    """VERDE so quando TODO item e OK. Reprovar e mais grave que nao exercitar."""
    estados = [i.get("estado") for i in itens]
    if any(e == REPROVOU for e in estados):
        return "REPROVADO"
    if any(e == NAO_EXERCITADO for e in estados):
        return "INCOMPLETO"
    if not estados:
        return "INCOMPLETO"
    return "VERDE"


def rel(caminho):
    """Caminho relativo a raiz do repo (para o relatorio nao vazar paths absolutos)."""
    try:
        return os.path.relpath(caminho).replace("\\", "/")
    except ValueError:
        return caminho
