#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scan.py - KIT-15: scan generico de segredos/conteudo e ausencia de DLL proprietaria.

Escopo: diretorio ou arquivo .zip candidato. Procura
  (a) padroes de credencial/segredo em texto (chave privada, token, senha, PAT, AWS);
  (b) membros proibidos: qualquer *.dll (o kit e distribuido como FONTE; DLL do jogo
      ou de terceiros nao pode entrar no pacote), *.pdb, .git/, perfil/save, __pycache__.

Exit: 0 = limpo; 1 = achado; 2 = erro de infraestrutura.
Saida legivel na tela e, com --json, um relatorio JSON (nao inclui o valor do segredo).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import zipfile

SCHEMA = "kit-rstv/scan/1"

# Padroes de texto. Nenhum padrao imprime o valor casado: so o caminho, a linha e o rotulo.
PADROES = [
    ("chave-privada", re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("aws-access-key", re.compile(rb"\b(AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("github-token", re.compile(rb"\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{30,}\b")),
    ("thunderstore-token", re.compile(rb"(?i)\bts[_ -]?token\b\s*[:=]\s*\S{12,}")),
    # F10 (KIT-15F): aceita a forma JSON (chave entre aspas, aspa ANTES do separador), nao so
    # a forma chave=valor. O valor casado nunca e impresso.
    ("senha-atribuida", re.compile(rb"(?i)\b(senha|password|passwd|pwd)\b\s*[\"']?\s*[:=]\s*[\"']?[^\s\"',;}]{4,}")),
    ("bearer", re.compile(rb"(?i)\bauthorization\b\s*[\"']?\s*:\s*[\"']?\s*bearer\s+\S{12,}")),
    ("api-key", re.compile(rb"(?i)\b(api[_-]?key|access[_-]?token|client[_-]?secret)\b\s*[\"']?\s*[:=]\s*[\"']?[A-Za-z0-9_\-]{16,}")),
]

EXTENSOES_TEXTO = {
    ".py", ".cs", ".json", ".md", ".txt", ".sh", ".cmd", ".ps1", ".yml", ".yaml",
    ".csproj", ".props", ".targets", ".cfg", ".ini", ".toml", ".example", ".lock",
    ".html", ".css", ".js", ".xml", ".schema",
}

DIRETORIOS_PROIBIDOS = (".git/", "__pycache__/", "bin/", "obj/", ".kit-rstv-backups/", ".kit-rstv-transacoes/")
EXTENSOES_PROIBIDAS = (".dll", ".pdb", ".so", ".dylib", ".exe")


def _texto_ou_none(nome):
    ext = os.path.splitext(nome)[1].lower()
    if ext in EXTENSOES_TEXTO:
        return True
    if ext == "" and "/" not in nome:
        return True
    return False


def _varrer_bytes(nome, dados, achados):
    for rotulo, rx in PADROES:
        for m in rx.finditer(dados):
            linha = dados.count(b"\n", 0, m.start()) + 1
            achados.append({"tipo": "segredo", "rotulo": rotulo, "caminho": nome, "linha": linha})


def _checar_nome(nome, achados):
    normalizado = nome.replace("\\", "/")
    base = normalizado.rsplit("/", 1)[-1]
    ext = os.path.splitext(base)[1].lower()
    if ext in EXTENSOES_PROIBIDAS:
        achados.append({"tipo": "binario-proibido", "rotulo": "dll/exe", "caminho": nome, "linha": 0})
    for d in DIRETORIOS_PROIBIDOS:
        if ("/" + normalizado).find("/" + d) >= 0:
            achados.append({"tipo": "caminho-proibido", "rotulo": d.rstrip("/"), "caminho": nome, "linha": 0})
            break
    if normalizado.lower().endswith(".log") or "logoutput" in base.lower():
        achados.append({"tipo": "conteudo-proibido", "rotulo": "log", "caminho": nome, "linha": 0})


def varrer_diretorio(raiz, achados=None):
    achados = [] if achados is None else achados
    for atual, dirs, arquivos in os.walk(raiz):
        # F10 (KIT-15F): NAO podar bin/obj/__pycache__/.git na varredura -- sao exatamente
        # os diretorios proibidos; poda-los tornava o scan silenciosamente LIMPO.
        dirs[:] = sorted(dirs)
        for a in sorted(arquivos):
            caminho = os.path.join(atual, a)
            rel = os.path.relpath(caminho, raiz).replace("\\", "/")
            _checar_nome(rel, achados)
            if not _texto_ou_none(rel):
                continue
            try:
                with open(caminho, "rb") as fh:
                    dados = fh.read()
            except OSError as exc:
                # F10: entrada ilegivel NAO e LIMPO -- vira achado de IO (infra), nunca verde.
                achados.append({"tipo": "erro-io", "rotulo": "ilegivel", "caminho": rel, "linha": 0,
                                "erro": str(exc)})
                continue
            _varrer_bytes(rel, dados, achados)
    return achados


def varrer_zip(caminho, achados=None):
    achados = [] if achados is None else achados
    with zipfile.ZipFile(caminho) as zf:
        for info in sorted(zf.infolist(), key=lambda i: i.filename):
            nome = info.filename
            if info.is_dir():
                continue
            _checar_nome(nome, achados)
            if not _texto_ou_none(nome):
                continue
            _varrer_bytes(nome, zf.read(info), achados)
    return achados


def varrer(caminho):
    if os.path.isdir(caminho):
        return varrer_diretorio(caminho)
    if zipfile.is_zipfile(caminho):
        return varrer_zip(caminho)
    achados = []
    _checar_nome(os.path.basename(caminho), achados)
    if _texto_ou_none(caminho):
        try:
            with open(caminho, "rb") as fh:
                _varrer_bytes(os.path.basename(caminho), fh.read(), achados)
        except OSError as exc:
            achados.append({"tipo": "erro-io", "rotulo": "ilegivel",
                            "caminho": os.path.basename(caminho), "linha": 0, "erro": str(exc)})
    return achados


def main(argv=None):
    ap = argparse.ArgumentParser(description="KIT-15: scan de segredos/conteudo e DLL proprietaria")
    ap.add_argument("alvo", help="diretorio ou arquivo .zip")
    ap.add_argument("--json", action="store_true", help="relatorio JSON")
    args = ap.parse_args(argv)

    if not os.path.exists(args.alvo):
        print("ERRO-INFRA KIT-15 scan: alvo inexistente: %s" % args.alvo, file=sys.stderr)
        return 2
    try:
        achados = varrer(args.alvo)
    except Exception as exc:  # pragma: no cover - infra
        print("ERRO-INFRA KIT-15 scan: %s" % exc, file=sys.stderr)
        return 2

    resumo = {
        "schema": SCHEMA,
        "alvo": os.path.abspath(args.alvo),
        "achados": achados,
        "total": len(achados),
        "veredito": "LIMPO" if not achados else "ACHADO",
    }
    if args.json:
        print(json.dumps(resumo, indent=2, ensure_ascii=False))
    else:
        print("SCAN|%s|%d achados|%s" % (resumo["veredito"], resumo["total"], resumo["alvo"]))
        for a in achados[:50]:
            print("  - %s/%s em %s:%s" % (a["tipo"], a["rotulo"], a["caminho"], a["linha"]))
    return 0 if not achados else 1


if __name__ == "__main__":
    sys.exit(main())
