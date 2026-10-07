#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""comum.py - apoio dos testes OFFLINE do runtime AUT-4.

Nao e teste: e o carregador do modulo sob teste (`../coletor.py`) e das fixtures
rotuladas (`../fixtures/`). Os testes de `tools/automacao/runtime/testes/` usam o
MESMO arcabouco do projeto (`tools/testes/arcabouco.py`, reuso, sem editar nada
la): exit 0/1/2 e a linha `RESULTADO|...`.
"""
import importlib.util
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))          # .../runtime/testes
RUNTIME = os.path.dirname(AQUI)                            # .../runtime
REPO = os.path.dirname(os.path.dirname(os.path.dirname(RUNTIME)))  # raiz do repo

sys.path.insert(0, os.path.join(REPO, "tools", "testes"))
import arcabouco as arc  # noqa: E402  (precisa do sys.path acima)

DIR_FIXTURES = os.path.join(RUNTIME, "fixtures")


def coletor():
    """Importa `coletor.py` como modulo (sem depender do cwd do runner)."""
    caminho = os.path.join(RUNTIME, "coletor.py")
    spec = importlib.util.spec_from_file_location("aut4_coletor", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def fixture(nome, papel="entrada"):
    caminho = os.path.join(DIR_FIXTURES, "%s.%s.json" % (nome, papel))
    with open(caminho, encoding="utf-8") as fh:
        return json.load(fh)


def caminho_probe():
    return os.path.join(RUNTIME, "AUT4Probe")


def dir_docs():
    return os.path.join(REPO, "docs", "automacao")
