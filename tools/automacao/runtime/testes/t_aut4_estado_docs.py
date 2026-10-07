#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUT-4/COR-AUT4 — A7: o estado declarado tem de casar com o DISCO.

O parecer AUT-4R2 (A7) achou o estado DESATUALIZADO: declarava uma DLL que nao e a
do disco, e contagens de testes/iscas que nao existem. Este teste e a trava contra
essa deriva:

  * a lista de testes e de iscas declarada em `AUT-4-estado.json` e IGUAL a do disco
    (nem a mais, nem a menos) — teste que existe e nao esta declarado desaparece;
  * a identidade do artefato e o hash DECLARADO e ele casa com os bytes da DLL em
    disco (a DLL nao e reproduzivel byte a byte: identidade = hash declarado,
    nunca "compila igual");
  * o hash do FONTE tambem e declarado (a DLL velha nao pode passar por fonte nova);
  * o documento humano (`AUT-4-preparacao.md`) cita os MESMOS numeros do disco.

Nao abre jogo, nao instala nada, nao escreve nada: so le bytes.
"""
import hashlib
import json
import os
import re

import comum as C

META = {
    "nome": "aut4-estado-docs",
    "categoria": "pura",
    "requer": [],
    "descricao": "AUT-4-estado.json casa com o disco (testes/iscas declarados = reais) e com os "
                 "hashes declarados da DLL e do fonte; o doc humano cita os mesmos numeros",
}

RUNTIME = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def _rel(*partes):
    return "/".join(("tools", "automacao", "runtime") + partes)


def _listar(pasta, prefixo=None):
    cheio = os.path.join(RUNTIME, pasta)
    saida = []
    for nome in sorted(os.listdir(cheio)):
        if prefixo and not nome.startswith(prefixo):
            continue
        if os.path.isfile(os.path.join(cheio, nome)) and nome.endswith(".py"):
            saida.append(_rel(pasta, nome))
    return saida


def corpo():
    estado_path = os.path.join(C.dir_docs(), "AUT-4-estado.json")
    C.arc.exigir(os.path.isfile(estado_path), "AUT-4-estado.json ausente: %s" % estado_path)
    estado = json.load(open(estado_path, encoding="utf-8"))
    art = estado["artefatos"]

    # ---- A7.2: testes e iscas declarados == disco ----
    testes_disco = _listar("testes", "t_")
    iscas_disco = _listar("testes/contra-prova", "cp_")
    C.arc.igual(sorted(art["testes"]), sorted(testes_disco),
                "A7: a lista de testes declarada tem de ser IGUAL a do disco")
    C.arc.igual(sorted(art["contra_prova"]), sorted(iscas_disco),
                "A7: a lista de iscas declarada tem de ser IGUAL a do disco")

    for caminho in art["testes"] + art["contra_prova"]:
        C.arc.exigir(os.path.isfile(os.path.join(C.REPO, caminho.replace("/", os.sep))),
                     "A7: artefato declarado que nao existe no disco: %s" % caminho)

    # ---- A7.1: identidade = hash DECLARADO, conferido contra os bytes do disco ----
    dll = os.path.join(RUNTIME, "AUT4Probe", "bin", "Release", "AUT4Probe.dll")
    C.arc.exigir(os.path.isfile(dll), "A7: DLL do probe ausente: %s" % dll)
    C.arc.igual(art.get("probe_dll_sha256"), _sha(dll),
                "A7: o hash declarado da DLL tem de ser o dos bytes em disco")
    C.arc.igual(art.get("probe_fonte_sha256"), _sha(os.path.join(RUNTIME, "AUT4Probe",
                                                                "AUT4ProbePlugin.cs")),
                "A7: o hash do FONTE tem de estar declarado e conferir com o disco")
    C.arc.igual(art.get("probe_dll_reprodutivel_byte_a_byte"), False,
                "A7: a DLL tem de declarar que NAO e reproduzivel byte a byte")
    C.arc.exigir(str(art.get("probe_dll_identidade") or "").strip(),
                 "A7: a identidade do artefato (hash declarado) tem de estar registrada")

    # ---- A7.3: o doc humano cita os numeros do disco ----
    doc = os.path.join(C.dir_docs(), "AUT-4-preparacao.md")
    C.arc.exigir(os.path.isfile(doc), "AUT-4-preparacao.md ausente: %s" % doc)
    texto = open(doc, encoding="utf-8").read()
    n, m = len(testes_disco), len(iscas_disco)
    C.arc.exigir("%d/%d" % (n, n) in texto,
                 "A7: o doc tem de citar a contagem real de testes (%d/%d)" % (n, n))
    C.arc.exigir("%d iscas" % m in texto,
                 "A7: o doc tem de citar a contagem real de iscas (%d iscas)" % m)
    # Contagens ANTIGAS nao podem sobreviver. A checagem usa fronteira de digito (e nao
    # substring) porque as contagens CRESCERAM: "22 iscas" CONTEM a substring "2 iscas"
    # e "16/16" conteria "6/6" — o guard literal recusaria o proprio numero correto.
    mantem_antigas = (re.search(r"(?<!\d)6/6(?!\d)", texto)
                      or re.search(r"(?<!\d)2 iscas", texto))
    C.arc.exigir(not mantem_antigas,
                 "A7: o doc nao pode manter as contagens antigas (6/6, 2 iscas)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
