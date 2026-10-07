#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUT-4 — manifest de artefatos e rollback EXATO.

O manifest lista cada artefato com sha256/bytes. O rollback classifica o que
surgiu, o que mudou e o que sumiu comparando o antes/depois — inclusive arquivos
que o probe CRIOU (o .cfg que nasce sozinho na 1a execucao), que precisam ser
removidos, nao apenas a pasta do probe.
"""
import hashlib
import os
import tempfile

import comum as C

META = {
    "nome": "aut4-manifest-rollback",
    "categoria": "pura",
    "requer": [],
    "descricao": "manifest com sha256 e rollback que enxerga arquivo CRIADO pelo probe (nao so a pasta)",
}


def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def corpo():
    col = C.coletor()
    with tempfile.TemporaryDirectory(prefix="aut4-mf-") as raiz:
        a = os.path.join(raiz, "capprobe.json")
        b = os.path.join(raiz, "01.png")
        open(a, "w", encoding="utf-8").write("{}")
        open(b, "wb").write(b"\x89PNG")

        m = col.montar_manifest(raiz, ["capprobe.json", "01.png"])
        C.arc.igual(m["total"], 2, "dois artefatos no manifest")
        por_nome = {x["arquivo"]: x for x in m["artefatos"]}
        C.arc.igual(por_nome["capprobe.json"]["sha256"], _sha(a), "sha256 do json")
        C.arc.igual(por_nome["01.png"]["bytes"], 4, "bytes do png")

        # rollback: antes sem nada, depois com os artefatos + um .cfg que o probe criou
        antes = {}
        cfg = os.path.join(raiz, "com.gumatos.aut4probe.cfg")
        open(cfg, "w", encoding="utf-8").write("[Geral]")
        depois = {"capprobe.json": _sha(a), "01.png": _sha(b),
                  "com.gumatos.aut4probe.cfg": _sha(cfg)}
        rb = col.planejar_rollback(antes, depois)
        C.arc.exigir("capprobe.json" in rb["criados"], "json contado como criado")
        C.arc.exigir("com.gumatos.aut4probe.cfg" in rb["criados"],
                     "o .cfg criado pelo probe TEM de entrar no rollback (nao so a pasta)")
        C.arc.igual(rb["modificados"], [], "nada modificado quando antes esta vazio")
        C.arc.igual(rb["extra"], False, "sem sobra: tudo classificado")

        # agora um arquivo que MUDOU e um que SUMIU
        antes2 = {"x": "1111", "y": "2222"}
        depois2 = {"x": "3333"}
        rb2 = col.planejar_rollback(antes2, depois2)
        C.arc.igual(rb2["modificados"], ["x"], "x mudou")
        C.arc.igual(rb2["removidos"], ["y"], "y sumiu e precisa voltar")


if __name__ == "__main__":
    C.arc.main(META, corpo)
