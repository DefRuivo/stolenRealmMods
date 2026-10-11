#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""instalador.py - KIT-15: instalar / atualizar / remover / rollback do kit-rstv.

Offline, stdlib, sem usuario fixo, sem SDK, sem rede, sem abrir jogo.

Autoridade (KIT-15F, achados F2/F12): o MANIFESTO do pacote e a unica fonte de verdade.
O instalador NAO redescobre arquivos no disco nem recalcula o hash para "aceitar" o que
encontrou: ele confere cada arquivo DECLARADO (nome + sha256 + bytes) contra o disco e
FALHA FECHADO quando ha divergencia, arquivo extra nao declarado ou componente obrigatorio
ausente. O recibo tambem e validado (schema/tipos/confinamento) antes de qualquer uso.

Confinamento: todo caminho relativo (destino, backup, recibo) e validado contra a raiz do
destino antes de qualquer efeito; traversal, absoluto, drive e UNC sao recusados.

Atomicidade (F3): cada entrada da transacao e registrada ANTES da copia correspondente, de
modo que falha de IO em qualquer copia/backup/recibo/journal e revertida sem deixar payload.

Layout instalado:
    <destino>/kit-rstv.manifest.json          identidade/versoes/hashes
    <destino>/components/<id>/...             fontes por componente
    <destino>/tools/...                       ferramenta empacotada
    <destino>/docs/...                        documentacao
    <destino>/.kit-rstv-installed.json        recibo (o que esta instalado)
    <destino>/.kit-rstv-backups/<ts>/...      bytes anteriores (para rollback/remover)
    <destino>/.kit-rstv-transacoes/<ts>.json  log da transacao

Exit: 0 = ok; 1 = falha logica (input/hash/estado); 2 = erro de infraestrutura.
Arquivo local que NAO pertence ao manifesto nunca e apagado nem sobrescrito.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import time
import zipfile

SCHEMA_MANIFESTO = "kit-rstv/manifesto/1"
SCHEMA_RECIBO = "kit-rstv/instalado/1"
SCHEMA_TRANSACAO = "kit-rstv/transacao/1"

ARQ_MANIFESTO = "kit-rstv.manifest.json"
ARQ_RECIBO = ".kit-rstv-installed.json"
DIR_BACKUPS = ".kit-rstv-backups"
DIR_TRANSACOES = ".kit-rstv-transacoes"

AQUI = os.path.dirname(os.path.abspath(__file__))

_RE_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_RE_ID = re.compile(r"^[A-Za-z0-9._-]+$")
_RE_DRIVE = re.compile(r"^[A-Za-z]:")


# --------------------------------------------------------------------------- #
# utilidades
# --------------------------------------------------------------------------- #
def sha256_arquivo(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def sha256_bytes(dados):
    return hashlib.sha256(dados).hexdigest()


def _ts():
    """Timestamp unico por transacao, inclusive ENTRE PROCESSOS.

    A unicidade e obrigatoria: o cofre de backups usa o ts no caminho, entao instalar e
    remover dentro do mesmo segundo NAO pode compartilhar pasta (isso sobrescreveria o
    backup original e o rollback devolveria o arquivo errado). Por isso o carimbo leva
    milissegundos, PID e um contador do processo."""
    global _CONTADOR_TS
    _CONTADOR_TS += 1
    return "%s-%03d-%05d-%04d" % (
        time.strftime("%Y%m%d-%H%M%S"),
        int(time.time() * 1000) % 1000,
        os.getpid() % 100000,
        _CONTADOR_TS % 10000,
    )


_CONTADOR_TS = 0


def _garantir_dir(caminho):
    os.makedirs(caminho, exist_ok=True)
    return caminho


def carregar_json(caminho):
    with open(caminho, "r", encoding="utf-8") as fh:
        return json.load(fh)


def gravar_json(caminho, dados):
    _garantir_dir(os.path.dirname(os.path.abspath(caminho)))
    with open(caminho, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(dados, fh, indent=2, ensure_ascii=False, sort_keys=False)
        fh.write("\n")


# --------------------------------------------------------------------------- #
# confinamento de caminhos (F12)
# --------------------------------------------------------------------------- #
def _dentro(raiz, caminho):
    raiz = os.path.abspath(raiz)
    alvo = os.path.abspath(caminho)
    try:
        return os.path.commonpath([raiz, alvo]) == raiz
    except ValueError:
        return False


def validar_rel(rel, rotulo="caminho"):
    """Valida um caminho RELATIVO seguro: nao vazio, nao absoluto/drive/UNC, sem traversal.

    Devolve a lista de partes normalizadas; levanta ValueError se inseguro."""
    if not isinstance(rel, str) or not rel.strip():
        raise ValueError("%s ausente ou vazio" % rotulo)
    norm = rel.replace("\\", "/")
    if norm.startswith("//"):
        raise ValueError("%s UNC nao permitido: %r" % (rotulo, rel))
    if norm.startswith("/") or _RE_DRIVE.match(norm):
        raise ValueError("%s absoluto/drive nao permitido: %r" % (rotulo, rel))
    partes = [p for p in norm.split("/") if p not in ("", ".")]
    if not partes:
        raise ValueError("%s vazio: %r" % (rotulo, rel))
    if any(p == ".." for p in partes):
        raise ValueError("%s com traversal nao permitido: %r" % (rotulo, rel))
    return partes


def caminho_seguro(raiz, rel, rotulo="caminho"):
    """Resolve `rel` sob `raiz`, garantindo que o resultado continua DENTRO de `raiz`."""
    partes = validar_rel(rel, rotulo)
    alvo = os.path.join(raiz, *partes)
    if not _dentro(raiz, alvo):
        raise ValueError("%s fora da raiz do destino: %r" % (rotulo, rel))
    return alvo


def validar_id(componente, rotulo="id de componente"):
    if not isinstance(componente, str) or not _RE_ID.match(componente) or componente in (".", ".."):
        raise ValueError("%s invalido: %r" % (rotulo, componente))
    return componente


# --------------------------------------------------------------------------- #
# manifesto e resolucao de arquivos (F2)
# --------------------------------------------------------------------------- #
def _validar_arquivos(lista, rotulo):
    if not isinstance(lista, list):
        raise ValueError("%s: 'arquivos' precisa ser lista" % rotulo)
    vistos = set()
    for arq in lista:
        if not isinstance(arq, dict):
            raise ValueError("%s: arquivo nao e objeto" % rotulo)
        rel = arq.get("rel")
        validar_rel(rel, "%s: rel" % rotulo)
        if rel in vistos:
            raise ValueError("%s: rel duplicado %r" % (rotulo, rel))
        vistos.add(rel)
        if not isinstance(arq.get("sha256"), str) or not _RE_HEX64.match(arq["sha256"]):
            raise ValueError("%s: sha256 invalido para %r" % (rotulo, rel))
        if "bytes" in arq and arq["bytes"] is not None and not isinstance(arq["bytes"], int):
            raise ValueError("%s: bytes invalido para %r" % (rotulo, rel))
    return True


def validar_manifesto(man):
    """Valida o contrato do manifesto do PACOTE. Levanta ValueError se invalido."""
    if not isinstance(man, dict):
        raise ValueError("manifesto nao e um objeto JSON")
    if man.get("schema") != SCHEMA_MANIFESTO:
        raise ValueError("schema de manifesto inesperado: %r" % man.get("schema"))
    comps = man.get("componentes")
    if not isinstance(comps, list) or not comps:
        raise ValueError("manifesto sem lista de componentes")
    ids = set()
    obrigatorios = 0
    for comp in comps:
        if not isinstance(comp, dict):
            raise ValueError("componente nao e objeto")
        cid = validar_id(comp.get("id"), "id de componente")
        if cid in ids:
            raise ValueError("id de componente duplicado: %s" % cid)
        ids.add(cid)
        origem = comp.get("origem_dir")
        if not isinstance(origem, str) or not origem.strip():
            raise ValueError("componente %s sem origem_dir" % cid)
        validar_rel(origem, "origem_dir de %s" % cid)
        if bool(comp.get("obrigatorio")):
            obrigatorios += 1
        _validar_arquivos(comp.get("arquivos"), "componente %s" % cid)
    if obrigatorios == 0:
        raise ValueError("manifesto sem nenhum componente obrigatorio")
    for chave in ("ferramenta", "documentacao"):
        bloco = man.get(chave)
        if bloco is None:
            continue
        if not isinstance(bloco, dict):
            raise ValueError("%s nao e objeto" % chave)
        origem = bloco.get("origem_dir")
        if origem is not None:
            validar_rel(origem, "origem_dir de %s" % chave)
        if bloco.get("arquivos") is not None:
            _validar_arquivos(bloco.get("arquivos"), chave)
    return man


def carregar_manifesto(raiz_pacote):
    caminho = os.path.join(raiz_pacote, ARQ_MANIFESTO)
    if not os.path.isfile(caminho):
        raise FileNotFoundError(caminho)
    return validar_manifesto(carregar_json(caminho))


def _casa_excluir(rel, excluir):
    partes = rel.split("/")
    for e in excluir or []:
        e = str(e).strip("/")
        if not e:
            continue
        if "/" in e:
            if rel == e or rel.startswith(e + "/"):
                return True
        elif e in partes:
            return True
        elif fnmatch.fnmatch(partes[-1], e):
            return True
    return False


def listar_bloco(base_dir, incluir=None, excluir=None):
    """Lista (rel, caminho) de um bloco de origem, aplicando incluir/excluir e podando
    __pycache__/.git/bin/obj. Determinista; reutilizado pelo instalador e pelo pacote."""
    if not os.path.isdir(base_dir):
        return []
    incluir = incluir or ["*"]
    saida = []
    for atual, dirs, arquivos in os.walk(base_dir):
        dirs[:] = sorted(d for d in dirs if d not in ("__pycache__", ".git", "bin", "obj"))
        for a in sorted(arquivos):
            caminho = os.path.join(atual, a)
            rel = os.path.relpath(caminho, base_dir).replace("\\", "/")
            if _casa_excluir(rel, excluir):
                continue
            if not any(fnmatch.fnmatch(rel, pat) or fnmatch.fnmatch(a, pat) for pat in incluir):
                continue
            saida.append((rel, caminho))
    return saida


def arquivos_do_manifesto(raiz_pacote, manifesto):
    """Devolve a lista de arquivos DECLARADOS no manifesto, com destino e hash declarados.

    Cada item: componente, obrigatorio, origem (caminho absoluto no pacote), rel (destino
    relativo final), sha256 e bytes DECLARADOS pelo manifesto (nao recalculados aqui)."""
    itens = []
    for comp in manifesto.get("componentes", []):
        cid = comp["id"]
        origem_dir = comp.get("origem_dir") or ("components/%s" % cid)
        base = os.path.join(raiz_pacote, *validar_rel(origem_dir, "origem_dir"))
        for arq in comp.get("arquivos", []):
            itens.append({
                "componente": cid,
                "obrigatorio": bool(comp.get("obrigatorio")),
                "origem": os.path.join(base, *validar_rel(arq["rel"], "rel")),
                "origem_dir": origem_dir,
                "rel": "components/%s/%s" % (cid, arq["rel"]),
                "sha256": arq["sha256"],
                "bytes": arq.get("bytes"),
            })
    for chave, prefixo in (("ferramenta", "tools"), ("documentacao", "docs")):
        bloco = manifesto.get(chave) or {}
        origem_dir = bloco.get("origem_dir") or prefixo
        base = os.path.join(raiz_pacote, *validar_rel(origem_dir, "origem_dir"))
        for arq in bloco.get("arquivos") or []:
            itens.append({
                "componente": chave,
                "obrigatorio": True,
                "origem": os.path.join(base, *validar_rel(arq["rel"], "rel")),
                "origem_dir": origem_dir,
                "rel": "%s/%s" % (prefixo, arq["rel"]),
                "sha256": arq["sha256"],
                "bytes": arq.get("bytes"),
            })
    return itens


def conferir_pacote(raiz_pacote, manifesto):
    """Confere o pacote contra o manifesto ANTES de qualquer efeito (F2/F12).

    - origem_dir de cada bloco existe e esta confinada;
    - cada arquivo declarado existe no disco com o sha256/bytes DECLARADOS;
    - nenhum arquivo NAO declarado aparece sob os blocos declarados (fechamento exato).
    Devolve lista de problemas (vazia = ok)."""
    problemas = []

    def _bloco(chave, origem_dir, incluir, excluir, arquivos):
        try:
            base = caminho_seguro(raiz_pacote, origem_dir, "origem_dir de %s" % chave)
        except ValueError as exc:
            problemas.append(str(exc))
            return
        if not os.path.isdir(base):
            problemas.append("%s: origem ausente %s" % (chave, origem_dir))
            return
        esperados = {}
        for arq in arquivos:
            esperados[arq["rel"]] = arq
            try:
                caminho = os.path.join(base, *validar_rel(arq["rel"], "%s: rel" % chave))
            except ValueError as exc:
                problemas.append(str(exc))
                continue
            if not os.path.isfile(caminho):
                problemas.append("%s: arquivo declarado ausente: %s" % (chave, arq["rel"]))
                continue
            if sha256_arquivo(caminho) != arq["sha256"]:
                problemas.append("%s: hash divergente do manifesto: %s" % (chave, arq["rel"]))
            if arq.get("bytes") is not None and os.path.getsize(caminho) != arq["bytes"]:
                problemas.append("%s: tamanho divergente do manifesto: %s" % (chave, arq["rel"]))
        encontrados = {rel for rel, _ in listar_bloco(base, incluir, excluir)}
        for extra in sorted(encontrados - set(esperados)):
            problemas.append("%s: arquivo NAO declarado no manifesto: %s" % (chave, extra))

    for comp in manifesto.get("componentes", []):
        cid = comp["id"]
        _bloco("componente %s" % cid, comp.get("origem_dir") or ("components/%s" % cid),
               comp.get("incluir") or ["*"], comp.get("excluir") or [],
               comp.get("arquivos") or [])
    for chave, prefixo in (("ferramenta", "tools"), ("documentacao", "docs")):
        bloco = manifesto.get(chave)
        if not bloco:
            continue
        _bloco(chave, bloco.get("origem_dir") or prefixo, bloco.get("incluir") or ["*"],
               bloco.get("excluir") or [], bloco.get("arquivos") or [])
    return problemas


# --------------------------------------------------------------------------- #
# estado / transacoes
# --------------------------------------------------------------------------- #
def validar_recibo(rec):
    """Valida o contrato do recibo (F2/F12). Devolve True/False (nunca levanta)."""
    if not isinstance(rec, dict):
        return False
    if rec.get("schema") != SCHEMA_RECIBO:
        return False
    arquivos = rec.get("arquivos")
    if not isinstance(arquivos, list):
        return False
    for arq in arquivos:
        if not isinstance(arq, dict):
            return False
        try:
            validar_rel(arq.get("rel"), "recibo: rel")
        except ValueError:
            return False
        if not isinstance(arq.get("sha256"), str) or not _RE_HEX64.match(arq["sha256"]):
            return False
        bk = arq.get("backup_original")
        if bk is not None:
            try:
                validar_rel(bk, "recibo: backup_original")
            except ValueError:
                return False
        osh = arq.get("original_sha256")
        if osh is not None and (not isinstance(osh, str) or not _RE_HEX64.match(osh)):
            return False
    return True


def ler_recibo(destino):
    caminho = os.path.join(destino, ARQ_RECIBO)
    if not os.path.isfile(caminho):
        return None
    try:
        rec = carregar_json(caminho)
    except (OSError, ValueError):
        return None
    return rec if validar_recibo(rec) else None


def _salvar_backup(destino, ts, rel, existia):
    """Copia os bytes atuais para o cofre de backups. Devolve o caminho relativo ou None."""
    if not existia:
        return None
    origem = caminho_seguro(destino, rel, "origem de backup")
    destino_bkp = caminho_seguro(destino, "%s/%s/%s" % (DIR_BACKUPS, ts, rel), "destino de backup")
    _garantir_dir(os.path.dirname(destino_bkp))
    shutil.copy2(origem, destino_bkp)
    return "%s/%s/%s" % (DIR_BACKUPS, ts, rel)


def _restaurar_backup(destino, rel_backup, rel, esperado=None):
    """Restaura `rel` a partir de um backup, validando a identidade ANTES de sobrescrever."""
    origem = caminho_seguro(destino, rel_backup, "backup")
    if not os.path.isfile(origem):
        raise FileNotFoundError("backup ausente: %s" % rel_backup)
    obtido_bkp = sha256_arquivo(origem)
    if esperado and obtido_bkp != esperado:
        raise ValueError("backup corrompido/divergente (%s): esperado %s obtido %s"
                         % (rel_backup, esperado, obtido_bkp))
    destino_final = caminho_seguro(destino, rel, "destino de restauracao")
    _garantir_dir(os.path.dirname(destino_final))
    shutil.copy2(origem, destino_final)
    return sha256_arquivo(destino_final)


def registrar_transacao(destino, ts, operacao, entradas, recibo_antes):
    caminho = caminho_seguro(destino, "%s/%s.json" % (DIR_TRANSACOES, ts), "transacao")
    gravar_json(caminho, {
        "schema": SCHEMA_TRANSACAO,
        "ts": ts,
        "operacao": operacao,
        "destino": os.path.abspath(destino),
        "entradas": entradas,
        "recibo_antes": recibo_antes,
    })
    return caminho


def transacao_mais_recente(destino):
    base = os.path.join(destino, DIR_TRANSACOES)
    if not os.path.isdir(base):
        return None
    nomes = [n for n in os.listdir(base) if n.endswith(".json")]
    if not nomes:
        return None
    nomes.sort(key=lambda n: (os.path.getmtime(os.path.join(base, n)), n))
    return os.path.join(base, nomes[-1])


def reverter_transacao(destino, transacao):
    """Reverte as entradas (ordem inversa). Devolve lista de problemas."""
    problemas = []
    for entrada in reversed(transacao.get("entradas", [])):
        rel = entrada.get("rel")
        try:
            acao = entrada.get("reverter") or ("apagar" if entrada.get("acao") == "criado" else "restaurar")
            if acao == "nada":
                continue
            if acao == "apagar":
                alvo = caminho_seguro(destino, rel, "alvo de reversao")
                if os.path.isfile(alvo):
                    os.remove(alvo)
            else:
                bk = entrada.get("reverter_backup") or entrada.get("backup")
                if not bk:
                    problemas.append("sem backup para reverter %s" % rel)
                    continue
                obtido = _restaurar_backup(destino, bk, rel, esperado=entrada.get("sha_antes"))
                if entrada.get("sha_antes") and obtido != entrada.get("sha_antes"):
                    problemas.append("restauracao divergente de %s" % rel)
        except Exception as exc:
            problemas.append("falha ao reverter %s: %s" % (rel, exc))

    recibo_antes = transacao.get("recibo_antes")
    caminho_recibo = os.path.join(destino, ARQ_RECIBO)
    try:
        if recibo_antes is None:
            if os.path.isfile(caminho_recibo):
                os.remove(caminho_recibo)
        else:
            gravar_json(caminho_recibo, recibo_antes)
    except OSError as exc:
        problemas.append("falha ao restaurar recibo: %s" % exc)
    return problemas


def _limpar_dirs_vazios(destino, rel):
    atual = os.path.dirname(os.path.join(destino, *validar_rel(rel)))
    raiz = os.path.abspath(destino)
    while os.path.abspath(atual).startswith(raiz) and os.path.abspath(atual) != raiz:
        try:
            if os.listdir(atual):
                return
            os.rmdir(atual)
        except OSError:
            return
        atual = os.path.dirname(atual)


# --------------------------------------------------------------------------- #
# operacoes
# --------------------------------------------------------------------------- #
def selecionar(manifesto, itens, componentes=None, com_opcionais=True):
    sempre = ("ferramenta", "documentacao")
    if componentes:
        queridos = {c.strip() for c in componentes if c.strip()}
        desconhecidos = queridos - {c["id"] for c in manifesto.get("componentes", [])}
        desconhecidos -= set(sempre)
        if desconhecidos:
            raise ValueError("componente desconhecido: %s" % ", ".join(sorted(desconhecidos)))
        itens = [i for i in itens if i["componente"] in queridos or i["componente"] in sempre]
    elif not com_opcionais:
        itens = [i for i in itens if i["obrigatorio"]]
    return itens


def instalar(raiz_pacote, destino, componentes=None, com_opcionais=True, forcar=False):
    try:
        manifesto = carregar_manifesto(raiz_pacote)
    except (FileNotFoundError, ValueError) as exc:
        return 1, {"erro": "manifesto invalido ou ausente: %s" % exc}

    problemas_pacote = conferir_pacote(raiz_pacote, manifesto)
    if problemas_pacote:
        return 1, {"erro": "pacote divergente do manifesto (falha fechada, nada foi escrito)",
                   "problemas": problemas_pacote}

    try:
        itens = selecionar(manifesto, arquivos_do_manifesto(raiz_pacote, manifesto), componentes, com_opcionais)
    except ValueError as exc:
        return 1, {"erro": str(exc)}
    if not itens:
        return 1, {"erro": "nenhum arquivo selecionado"}

    _garantir_dir(destino)
    recibo_antes = ler_recibo(destino)
    anteriores = {}
    if recibo_antes:
        anteriores = {a["rel"]: a for a in recibo_antes.get("arquivos", [])}

    ts = _ts()
    entradas = []
    novos = []
    caminho_tx = os.path.join(destino, DIR_TRANSACOES, ts + ".json")
    try:
        for item in itens:
            rel = item["rel"]
            alvo = caminho_seguro(destino, rel, "destino de %s" % rel)
            existia = os.path.isfile(alvo)
            sha_antes = sha256_arquivo(alvo) if existia else None
            anterior = anteriores.get(rel)

            if existia and not forcar and sha_antes == item["sha256"]:
                # ja identico ao pacote: nada a escrever (preserva a posse registrada).
                base = anterior or {}
                novos.append({"rel": rel, "componente": item["componente"], "sha256": item["sha256"],
                              "bytes": item.get("bytes"), "preexistente": base.get("preexistente", True),
                              "backup_original": base.get("backup_original"),
                              "original_sha256": base.get("original_sha256")})
                continue

            if anterior is not None:
                preexistente = bool(anterior.get("preexistente"))
                backup_original = anterior.get("backup_original")
                original_sha256 = anterior.get("original_sha256")
            else:
                preexistente = existia
                backup_original = None
                original_sha256 = sha_antes if existia else None

            backup = _salvar_backup(destino, ts, rel, existia)
            if preexistente and backup_original is None:
                backup_original = backup
                original_sha256 = sha_antes

            entradas.append({"rel": rel, "acao": "criado" if not existia else "sobrescrito",
                             "backup": backup, "sha_antes": sha_antes,
                             "reverter": "apagar" if not existia else "restaurar",
                             "reverter_backup": backup})
            # F3: journal ANTES da copia -- falha na copia ainda e recuperavel.
            registrar_transacao(destino, ts, "instalar", entradas, recibo_antes)

            _garantir_dir(os.path.dirname(alvo))
            shutil.copy2(item["origem"], alvo)

            obtido = sha256_arquivo(alvo)
            if obtido != item["sha256"]:
                problemas = reverter_transacao(destino, carregar_json(caminho_tx))
                return 1, {"erro": "hash divergente apos escrita", "rel": rel,
                           "esperado": item["sha256"], "obtido": obtido, "rollback": problemas or "ok"}

            novos.append({"rel": rel, "componente": item["componente"], "sha256": item["sha256"],
                          "bytes": item.get("bytes"), "preexistente": preexistente,
                          "backup_original": backup_original, "original_sha256": original_sha256})
    except Exception as exc:
        problemas = []
        if os.path.isfile(caminho_tx):
            try:
                problemas = reverter_transacao(destino, carregar_json(caminho_tx))
            except Exception as exc2:
                problemas = ["falha ao reverter transacao: %s" % exc2]
        return 1, {"erro": "falha de IO durante a instalacao: %s" % exc, "rollback": problemas or "ok"}

    # F5: arquivos ja possuidos que saem da selecao permanecem sob posse (sem orfaos) enquanto
    # continuarem intactos no disco. Reduzir a selecao nao apaga o que ja foi instalado.
    selecionados = {i["rel"] for i in itens}
    ja = {a["rel"] for a in novos}
    for rel, anterior in anteriores.items():
        if rel in selecionados or rel in ja:
            continue
        try:
            alvo = os.path.join(destino, *validar_rel(rel, "rel do recibo anterior"))
        except ValueError:
            continue
        if os.path.isfile(alvo) and anterior.get("sha256") and sha256_arquivo(alvo) == anterior["sha256"]:
            novos.append(anterior)

    recibo = {
        "schema": SCHEMA_RECIBO,
        "pacote": manifesto.get("pacote"),
        "versao": manifesto.get("versao"),
        "instalado_em": ts,
        "destino": os.path.abspath(destino),
        "arquivos": sorted(novos, key=lambda a: a["rel"]),
    }
    gravar_json(os.path.join(destino, ARQ_RECIBO), recibo)
    if entradas:
        registrar_transacao(destino, ts, "instalar", entradas, recibo_antes)
    return 0, {"operacao": "instalar", "destino": os.path.abspath(destino), "versao": manifesto.get("versao"),
               "arquivos_escritos": len(entradas), "arquivos_total": len(itens), "ts": ts}


def remover(destino):
    recibo = ler_recibo(destino)
    if not recibo:
        return 1, {"erro": "nenhum recibo valido em %s (nada a remover)" % os.path.abspath(destino)}
    ts = _ts()
    entradas = []
    problemas = []
    for arq in sorted(recibo.get("arquivos", []), key=lambda a: a["rel"]):
        rel = arq["rel"]
        try:
            alvo = caminho_seguro(destino, rel, "alvo de remocao")
        except ValueError as exc:
            problemas.append(str(exc))
            continue
        if not os.path.isfile(alvo):
            continue
        sha_antes = sha256_arquivo(alvo)
        backup = _salvar_backup(destino, ts, rel, True)
        entrada = {"rel": rel, "acao": "removido", "backup": backup, "sha_antes": sha_antes,
                   "reverter": "restaurar", "reverter_backup": backup}

        if arq.get("preexistente") and arq.get("backup_original"):
            # arquivo do usuario sobrescrito pelo kit: devolver o original, nunca apagar.
            entradas.append(entrada)
            try:
                _restaurar_backup(destino, arq["backup_original"], rel, esperado=arq.get("original_sha256"))
            except Exception as exc:
                problemas.append("backup original nao restaurado para %s: %s" % (rel, exc))
        elif arq.get("preexistente"):
            # preexistente IDENTICO ao pacote: o kit nao o criou; deixar como esta (F5).
            continue
        else:
            entradas.append(entrada)
            try:
                os.remove(alvo)
                _limpar_dirs_vazios(destino, rel)
            except OSError as exc:
                problemas.append("falha ao remover %s: %s" % (rel, exc))

    registrar_transacao(destino, ts, "remover", entradas, recibo)
    if not problemas:
        os.remove(os.path.join(destino, ARQ_RECIBO))
    return (0 if not problemas else 1), {"operacao": "remover", "destino": os.path.abspath(destino),
                                         "arquivos_tratados": len(entradas), "problemas": problemas, "ts": ts}


def rollback(destino):
    caminho = transacao_mais_recente(destino)
    if not caminho:
        return 1, {"erro": "nenhuma transacao para reverter em %s" % os.path.abspath(destino)}
    try:
        transacao = carregar_json(caminho)
    except (OSError, ValueError) as exc:
        return 1, {"erro": "transacao ilegivel: %s" % exc}
    problemas = reverter_transacao(destino, transacao)
    return (0 if not problemas else 1), {"operacao": "rollback", "transacao": os.path.relpath(caminho, destino),
                                         "operacao_revertida": transacao.get("operacao"),
                                         "problemas": problemas}


def status(destino):
    recibo = ler_recibo(destino)
    if not recibo:
        return 0, {"estado": "AUSENTE", "destino": os.path.abspath(destino)}
    faltando = []
    divergentes = []
    for arq in recibo.get("arquivos", []):
        alvo = os.path.join(destino, *validar_rel(arq["rel"]))
        if not os.path.isfile(alvo):
            faltando.append(arq["rel"])
        elif sha256_arquivo(alvo) != arq["sha256"]:
            divergentes.append(arq["rel"])
    return 0, {"estado": "INSTALADO" if not faltando and not divergentes else "DIVERGENTE",
               "destino": os.path.abspath(destino), "pacote": recibo.get("pacote"), "versao": recibo.get("versao"),
               "arquivos": len(recibo.get("arquivos", [])), "faltando": faltando, "divergentes": divergentes}


# --------------------------------------------------------------------------- #
# entrada: zip ou diretorio
# --------------------------------------------------------------------------- #
class PacoteTemporario:
    def __init__(self, caminho):
        self.caminho = caminho
        self.tmp = None

    def __enter__(self):
        if os.path.isdir(self.caminho):
            return os.path.abspath(self.caminho)
        if zipfile.is_zipfile(self.caminho):
            self.tmp = tempfile.mkdtemp(prefix="kit-rstv-pkg-")
            with zipfile.ZipFile(self.caminho) as zf:
                zf.extractall(self.tmp)
            return self.tmp
        raise FileNotFoundError("pacote nem diretorio nem zip valido: %s" % self.caminho)

    def __exit__(self, *exc):
        if self.tmp:
            shutil.rmtree(self.tmp, ignore_errors=True)
        return False


def _achar_raiz(extraido):
    if os.path.isfile(os.path.join(extraido, ARQ_MANIFESTO)):
        return extraido
    for nome in sorted(os.listdir(extraido)):
        sub = os.path.join(extraido, nome)
        if os.path.isdir(sub) and os.path.isfile(os.path.join(sub, ARQ_MANIFESTO)):
            return sub
    raise FileNotFoundError("%s nao encontrado sob %s" % (ARQ_MANIFESTO, extraido))


def main(argv=None):
    ap = argparse.ArgumentParser(description="KIT-15: instalador offline do kit-rstv")
    ap.add_argument("operacao", choices=["instalar", "atualizar", "remover", "rollback", "status"])
    ap.add_argument("--pacote", help="diretorio ou zip do pacote (default: esta pasta)")
    ap.add_argument("--destino", help="destino; sem ele usa descoberta.py (sem usuario fixo)")
    ap.add_argument("--componentes", help="lista separada por virgula (default: todos)")
    ap.add_argument("--sem-opcionais", action="store_true", help="instala somente os componentes obrigatorios")
    ap.add_argument("--forcar", action="store_true", help="reescreve mesmo quando o hash confere")
    ap.add_argument("--json", action="store_true", help="imprime resultado em JSON")
    args = ap.parse_args(argv)

    sys.path.insert(0, AQUI)
    try:
        from descoberta import destino_do_kit
    except Exception as exc:  # pragma: no cover - infra
        print("ERRO-INFRA KIT-15: descoberta indisponivel: %s" % exc, file=sys.stderr)
        return 2

    destino, origem = destino_do_kit(explicito=args.destino)
    if not destino:
        print("ERRO-INFRA KIT-15: destino indeterminado (use --destino ou KIT_RSTV_HOME)", file=sys.stderr)
        return 2

    componentes = args.componentes.split(",") if args.componentes else None
    pacote = args.pacote or AQUI

    try:
        if args.operacao == "status":
            rc, dados = status(destino)
        elif args.operacao == "rollback":
            rc, dados = rollback(destino)
        elif args.operacao == "remover":
            rc, dados = remover(destino)
        else:
            with PacoteTemporario(pacote) as raiz:
                rc, dados = instalar(_achar_raiz(raiz), destino, componentes=componentes,
                                     com_opcionais=not args.sem_opcionais, forcar=args.forcar)
    except FileNotFoundError as exc:
        print("ERRO-INFRA KIT-15: %s" % exc, file=sys.stderr)
        return 2
    except ValueError as exc:
        dados = {"erro": str(exc)}
        rc = 1
    except Exception as exc:  # pragma: no cover - infra
        print("ERRO-INFRA KIT-15: %s" % exc, file=sys.stderr)
        return 2

    dados["destino_origem"] = origem
    if args.json:
        print(json.dumps(dados, indent=2, ensure_ascii=False))
    else:
        print("KIT15|%s|exit=%d|destino=%s|%s" % (args.operacao.upper(), rc, destino,
                                                  json.dumps(dados, ensure_ascii=False)))
    return rc


if __name__ == "__main__":
    sys.exit(main())
