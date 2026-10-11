#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pacote.py - KIT-15: monta/verifica o zip/release candidato LOCAL a partir do manifesto.

Offline, stdlib. NAO publica (nada de push/tag/GitHub Release/Thunderstore/publicar:true).

    python pacote.py montar --saida <dir-de-provas> [--zip <arquivo.zip>]
    python pacote.py verificar <arquivo.zip>

`montar` faz: staging -> kit-rstv.manifest.json (com hashes MEDIDOS) -> zip deterministico
-> testzip -> scan de segredos/DLL proprietaria -> relatorio JSON em <saida>/pacote-relatorio.json.

`verificar` (KIT-15F, achado F2) NAO confia apenas em CRC: le o manifesto EMBUTIDO, valida o
contrato, confere o hash de CADA membro declarado e recusa membro nao declarado. CRC valido
nao e identidade.

Layout (KIT-15F, achado F8): funciona tanto no repositorio do autor (manifesto.json + dirs de
origem) quanto na arvore DISTRIBUIDA (o pacote extraido, com components/ + tools/ + docs/), sem
depender de variaveis ou do layout do repositorio do autor.

Exit: 0 = pacote gerado/verificado e limpo; 1 = achado/problema; 2 = erro de infraestrutura.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import shutil
import sys
import time
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import instalador  # noqa: E402
from instalador import (  # noqa: E402
    ARQ_MANIFESTO,
    SCHEMA_MANIFESTO,
    carregar_json,
    gravar_json,
    sha256_arquivo,
)
import scan as scan_mod  # noqa: E402

SCHEMA_PACOTE_MANIFESTO = "kit-rstv/manifesto/1"
ARQ_RECIPE = "manifesto.json"
DATA_ZIP = (1980, 1, 1, 0, 0, 0)  # zip deterministico


def _modo_de(base):
    if os.path.isdir(os.path.join(base, "tools", "automacao")):
        return "repo"
    if os.path.isdir(os.path.join(base, "components")) and os.path.isdir(os.path.join(base, "tools")):
        return "pacote"
    return None


def resolver_fonte(raiz=None):
    """Resolve (modo, base, caminho_recipe) da origem das fontes.

    - modo 'repo': base e a raiz do repositorio (tem tools/automacao); recipe e o manifesto.json
      que acompanha a ferramenta.
    - modo 'pacote': base e a raiz do pacote distribuido (tem components/ e tools/); recipe e o
      proprio kit-rstv.manifest.json.
    Ordem: --raiz/KIT15_RAIZ -> subida a partir de AQUI -> layout distribuido (AQUI/..)."""
    explicito = raiz or os.environ.get("KIT15_RAIZ")
    if explicito:
        base = os.path.abspath(explicito)
        modo = _modo_de(base)
        if modo:
            recipe = os.path.join(AQUI, ARQ_RECIPE) if modo == "repo" else os.path.join(base, ARQ_MANIFESTO)
            return modo, base, recipe
    atual = AQUI
    for _ in range(8):
        modo = _modo_de(atual)
        if modo == "repo":
            return "repo", atual, os.path.join(AQUI, ARQ_RECIPE)
        pai = os.path.dirname(atual)
        if pai == atual:
            break
        atual = pai
    base = os.path.dirname(AQUI)
    if _modo_de(base) == "pacote":
        return "pacote", base, os.path.join(base, ARQ_MANIFESTO)
    raise FileNotFoundError("origem das fontes nao encontrada a partir de %s" % AQUI)


def _raiz_repo(raiz=None):
    """Compatibilidade: devolve a base da origem (raiz do repo OU raiz do pacote)."""
    return resolver_fonte(raiz)[1]


def _copiar(origem, destino):
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    shutil.copy2(origem, destino)


def montar_staging(base, staging, recipe, modo):
    """Copia para o staging: componentes + ferramenta + documentacao."""
    if os.path.isdir(staging):
        shutil.rmtree(staging)
    os.makedirs(staging)

    for comp in recipe.get("componentes", []):
        origem = os.path.join(base, comp["origem_dir"])
        if not os.path.isdir(origem):
            raise FileNotFoundError("componente %s: origem ausente %s" % (comp["id"], origem))
        for rel, caminho in instalador.listar_bloco(origem, comp.get("incluir") or ["*"],
                                                     comp.get("excluir") or []):
            _copiar(caminho, os.path.join(staging, "components", comp["id"], rel))

    ferr = recipe.get("ferramenta") or {}
    origem_ferr = os.path.join(base, ferr.get("origem_dir") or "tools/automacao/kit15")
    if modo == "repo":
        for nome in ferr.get("incluir") or []:
            caminho = os.path.join(origem_ferr, nome)
            if os.path.isfile(caminho):
                _copiar(caminho, os.path.join(staging, "tools", nome))
    else:
        for rel, caminho in instalador.listar_bloco(origem_ferr, ferr.get("incluir") or ["*"],
                                                     ferr.get("excluir") or []):
            _copiar(caminho, os.path.join(staging, "tools", rel))

    doc = recipe.get("documentacao") or {}
    origem_doc = os.path.join(base, doc.get("origem_dir") or "tools/automacao/kit15")
    if modo == "repo":
        for nome in doc.get("incluir") or []:
            caminho = os.path.join(origem_doc, nome)
            if os.path.isfile(caminho):
                _copiar(caminho, os.path.join(staging, "docs", nome))
        sub = os.path.join(origem_doc, "docs")
        if os.path.isdir(sub):
            for rel, caminho in instalador.listar_bloco(sub, ["*"], []):
                _copiar(caminho, os.path.join(staging, "docs", rel))
    else:
        for rel, caminho in instalador.listar_bloco(origem_doc, doc.get("incluir") or ["*"],
                                                     doc.get("excluir") or []):
            _copiar(caminho, os.path.join(staging, "docs", rel))
    return staging


def _medir_bloco(base_dir):
    arquivos = []
    for atual, dirs, nomes in os.walk(base_dir):
        dirs[:] = sorted(d for d in dirs if d not in ("__pycache__", ".git", "bin", "obj"))
        for a in sorted(nomes):
            caminho = os.path.join(atual, a)
            rel = os.path.relpath(caminho, base_dir).replace("\\", "/")
            arquivos.append({"rel": rel, "sha256": sha256_arquivo(caminho), "bytes": os.path.getsize(caminho)})
    return sorted(arquivos, key=lambda x: x["rel"])


def gerar_manifesto_pacote(staging, recipe):
    """Escreve kit-rstv.manifest.json com hashes MEDIDOS de TODOS os blocos entregues
    (componentes + ferramenta + documentacao). KIT-15F/F2: os tres blocos passam a declarar
    'arquivos' com sha256/bytes -- o instalador valida contra isso e falha fechado."""
    comps = []
    total = 0
    for comp in recipe.get("componentes", []):
        base_rel = "components/%s" % comp["id"]
        arquivos = _medir_bloco(os.path.join(staging, base_rel))
        total += len(arquivos)
        comps.append({
            "id": comp["id"], "nome": comp.get("nome"), "versao": comp.get("versao"),
            "versao_origem": comp.get("versao_origem"), "obrigatorio": bool(comp.get("obrigatorio")),
            "linguagem": comp.get("linguagem"), "papel": comp.get("papel"),
            "origem_dir": base_rel, "incluir": ["*"], "excluir": [],
            "arquivos": arquivos,
        })

    ferr = dict(recipe.get("ferramenta") or {})
    ferr.update({"origem_dir": "tools", "incluir": ["*"], "excluir": []})
    ferr["arquivos"] = _medir_bloco(os.path.join(staging, "tools"))
    total += len(ferr["arquivos"])

    doc = dict(recipe.get("documentacao") or {})
    doc.update({"origem_dir": "docs", "incluir": ["*"], "excluir": []})
    doc["arquivos"] = _medir_bloco(os.path.join(staging, "docs"))
    total += len(doc["arquivos"])

    manifesto = {
        "schema": SCHEMA_PACOTE_MANIFESTO,
        "pacote": recipe.get("pacote"),
        "nome_exibivel": recipe.get("nome_exibivel"),
        "versao": recipe.get("versao"),
        "descricao": recipe.get("descricao"),
        "build": {"em": time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()), "autor": "kit15/pacote.py"},
        "componentes": comps,
        "ferramenta": ferr,
        "documentacao": doc,
        "dependencias": recipe.get("dependencias"),
        "compatibilidade": recipe.get("compatibilidade"),
        "total_arquivos": total,
    }
    gravar_json(os.path.join(staging, ARQ_MANIFESTO), manifesto)
    return manifesto


def zipar(staging, destino_zip):
    os.makedirs(os.path.dirname(os.path.abspath(destino_zip)), exist_ok=True)
    membros = []
    for atual, dirs, arquivos in os.walk(staging):
        dirs[:] = sorted(dirs)
        for a in sorted(arquivos):
            caminho = os.path.join(atual, a)
            rel = os.path.relpath(caminho, staging).replace("\\", "/")
            membros.append((rel, caminho))
    membros.sort()
    with zipfile.ZipFile(destino_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel, caminho in membros:
            zi = zipfile.ZipInfo(rel, date_time=DATA_ZIP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(caminho, "rb") as fh:
                zf.writestr(zi, fh.read())
    return [m[0] for m in membros]


def testzip(destino_zip):
    with zipfile.ZipFile(destino_zip) as zf:
        return zf.testzip()


def _declarados_do_manifesto(man):
    """Mapa rel-destino-final -> sha256 declarado, para os tres blocos."""
    d = {}
    for comp in man.get("componentes", []):
        for a in comp.get("arquivos") or []:
            d["components/%s/%s" % (comp["id"], a["rel"])] = a["sha256"]
    for chave, prefixo in (("ferramenta", "tools"), ("documentacao", "docs")):
        for a in (man.get(chave) or {}).get("arquivos") or []:
            d["%s/%s" % (prefixo, a["rel"])] = a["sha256"]
    return d


def montar(saida, zip_saida=None, raiz=None):
    modo, base, recipe_path = resolver_fonte(raiz)
    recipe = carregar_json(recipe_path)
    versao = recipe.get("versao")
    staging = os.path.join(saida, "staging")
    os.makedirs(saida, exist_ok=True)

    montar_staging(base, staging, recipe, modo)
    manifesto = gerar_manifesto_pacote(staging, recipe)

    destino_zip = zip_saida or os.path.join(saida, "kit-rstv-%s.zip" % versao)
    membros = zipar(staging, destino_zip)
    erro_zip = testzip(destino_zip)
    achados = scan_mod.varrer_zip(destino_zip)

    relatorio = {
        "schema": "kit-rstv/pacote-relatorio/1",
        "pacote": recipe.get("pacote"),
        "versao": versao,
        "modo_origem": modo,
        "zip": os.path.abspath(destino_zip),
        "zip_sha256": sha256_arquivo(destino_zip),
        "zip_bytes": os.path.getsize(destino_zip),
        "zip_membros": len(membros),
        "zip_testzip": erro_zip,
        "arquivos_manifesto": manifesto["total_arquivos"],
        "componentes": [{"id": c["id"], "versao": c["versao"], "obrigatorio": c["obrigatorio"],
                         "arquivos": len(c["arquivos"])} for c in manifesto["componentes"]],
        "scan_achados": achados,
        "scan_total": len(achados),
        "veredito": "PACOTE_LIMPO" if (not achados and erro_zip is None) else "PACOTE_COM_ACHADO",
        "publicacao": "NAO_EXECUTADA (push/tag/GitHub Release/Thunderstore pertencem a KIT-G4)",
        "membros": membros,
    }
    gravar_json(os.path.join(saida, "pacote-relatorio.json"), relatorio)
    return (0 if relatorio["veredito"] == "PACOTE_LIMPO" else 1), relatorio


def verificar(caminho_zip):
    if not zipfile.is_zipfile(caminho_zip):
        raise FileNotFoundError("nao e um zip valido: %s" % caminho_zip)
    erro = testzip(caminho_zip)
    achados = scan_mod.varrer_zip(caminho_zip)
    problemas = []
    man = None
    with zipfile.ZipFile(caminho_zip) as zf:
        nomes = zf.namelist()
        membros = [n for n in nomes if not n.endswith("/")]
        if ARQ_MANIFESTO not in membros:
            problemas.append("manifesto ausente do zip")
        else:
            try:
                man = json.loads(zf.read(ARQ_MANIFESTO).decode("utf-8"))
                instalador.validar_manifesto(man)
            except Exception as exc:
                man = None
                problemas.append("manifesto invalido: %s" % exc)
        if man is not None:
            declarados = _declarados_do_manifesto(man)
            for rel, sha in sorted(declarados.items()):
                if rel not in membros:
                    problemas.append("membro declarado ausente no zip: %s" % rel)
                    continue
                if hashlib.sha256(zf.read(rel)).hexdigest() != sha:
                    problemas.append("hash divergente do manifesto no zip: %s" % rel)
            for extra in sorted(set(membros) - set(declarados) - {ARQ_MANIFESTO}):
                problemas.append("membro NAO declarado no manifesto: %s" % extra)

    relatorio = {
        "schema": "kit-rstv/pacote-verificacao/1",
        "zip": os.path.abspath(caminho_zip),
        "zip_sha256": sha256_arquivo(caminho_zip),
        "membros": len(membros),
        "zip_membros": len(membros),
        "testzip": erro,
        "problemas": problemas,
        "scan_achados": achados,
        "scan_total": len(achados),
        "tem_manifesto": ARQ_MANIFESTO in membros,
        "veredito": "OK" if (not achados and erro is None and not problemas) else "ACHADO",
    }
    return (0 if relatorio["veredito"] == "OK" else 1), relatorio


def main(argv=None):
    ap = argparse.ArgumentParser(description="KIT-15: pacote candidato local (sem publicar)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("montar")
    m.add_argument("--saida", required=True, help="diretorio de provas (novo)")
    m.add_argument("--zip", dest="zip_saida", default=None)
    m.add_argument("--raiz", default=None)
    m.add_argument("--json", action="store_true")
    v = sub.add_parser("verificar")
    v.add_argument("zip")
    v.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    try:
        if args.cmd == "montar":
            os.makedirs(args.saida, exist_ok=True)
            rc, rel = montar(args.saida, args.zip_saida, args.raiz)
        else:
            rc, rel = verificar(args.zip)
    except Exception as exc:
        print("ERRO-INFRA KIT-15 pacote: %s" % exc, file=sys.stderr)
        return 2

    # KIT-15F/F7: a saida legivel nao pode depender de chave inexistente (KeyError zip_membros).
    campos = ("zip", "zip_sha256", "zip_membros", "scan_total", "veredito", "tem_manifesto")
    if args.json:
        print(json.dumps(rel, indent=2, ensure_ascii=False))
    else:
        print("PACOTE|%s|%s" % (rel.get("veredito"), json.dumps(
            {k: rel.get(k) for k in campos if k in rel}, ensure_ascii=False)))
    return rc


if __name__ == "__main__":
    sys.exit(main())
