#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_proveniencia.py - as regras do CARIMBO DE PROVENIENCIA do RoguelikeDebugger (DBG-R2).

O QUE ESTE MODULO E
-------------------
A biblioteca da familia de testes do cartao `t_3b7c681b` (INT-R1-C3). Aqui mora a ligacao entre tres
coisas que precisam concordar, e o teste puro (`testes/puros/t_dbg_r2_proveniencia.py`) so' chama
estas funcoes:

  1. o VERIFICADOR real (`tools/verifica_proveniencia_debugger.py`) - importado a partir do arquivo,
     nunca uma copia digitada, para que teste e ferramenta nao divirjam;
  2. o FONTE C# vivo (`RoguelikeDebugger/Proveniencia.cs` + `Plugin.cs`) - de onde saem os campos
     que o verificador EXIGE (o contrato tem de estar dos DOIS lados);
  3. as FONTES QUE NAO PODEM MUDAR neste cartao (os 10 `Patches/*.cs`, `EfeitosInfo.cs` e o
     `.csproj`) - com o sha256 medido ANTES da implementacao, de 11/10/2026.

O QUE ELE NAO PROVA
-------------------
Nao executa o plugin no jogo (pediria a `lib/` e uma partida): o carimbo em runtime continua
NAO_EXERCITADO. Ele prova o formato, o contrato e a estaticidade das fontes.
"""
import hashlib
import importlib.util
import os
import re
import sys

import arcabouco as arc

RAIZ = arc.raiz_do_repo()
VERIFICADOR = os.path.join(RAIZ, "tools", "verifica_proveniencia_debugger.py")
ALVO = os.path.join(RAIZ, "api", "docs", "target-game.json")

FONTES = {
    "proveniencia": os.path.join("RoguelikeDebugger", "Proveniencia.cs"),
    "plugin": os.path.join("RoguelikeDebugger", "Plugin.cs"),
    "csproj": os.path.join("RoguelikeDebugger", "RoguelikeDebugger.csproj"),
}

# sha256 das fontes do debugger NAO atingidas pelo cartao, medidos ANTES de implementar
# (sha256sum RoguelikeDebugger/*.cs RoguelikeDebugger/Patches/*.cs -> docs/automacao/DBG-R2-parte02.md).
# Se qualquer um destes hashes mudar, o cartao reescreveu gancho existente ou mexeu no contrato de
# build - e o teste tem de reprovar.
INTOCADOS = {
    "RoguelikeDebugger/EfeitosInfo.cs": "69ffbf2ccaae4471e0ba882b494a6e512e8c2fec9a3aa0bc226b83e2e45a450b",
    "RoguelikeDebugger/Patches/ActionStatusInventoryPatch.cs": "77748b53441feecdf8c92310867e0f3d0953d67519b939ebc44190f0d598e140",
    "RoguelikeDebugger/Patches/EventRollDebugPatch.cs": "b2d8fcdf318e616236acedcaed8c0ff4947a07cb3b23d92fdf07471739cb1c18",
    "RoguelikeDebugger/Patches/ExpDebugPatch.cs": "45e21c5a49d1106e64b0c66b3710f32f13df3211bb48062fcda8fa295c778d1e",
    "RoguelikeDebugger/Patches/FlameShrineProcPatch.cs": "4988abbf136d7699775efc71f9a900505b1e0591c8f41fb340fb4dd80d5a0a11",
    "RoguelikeDebugger/Patches/GoldModifierDebugPatch.cs": "d3ab912bbbfe4b9a32e13a6f6daba146fdeb63579e9939d95d7670ac11d30384",
    "RoguelikeDebugger/Patches/ItemInventoryPatch.cs": "d67663c092347e17f63f702da24c406d76ae8382b88f3ddc170df3067f4fb36b",
    "RoguelikeDebugger/Patches/LifeStealDebugPatch.cs": "ee9a54896b34d57796a4e1d27f1e24c6bc0623cfaf35214985457ae24ab91a7c",
    "RoguelikeDebugger/Patches/LootModifierDebugPatch.cs": "1a81a879a1af2636df3bfd35bd0124993f31435494a49b18e4f4a82cf1474b59",
    "RoguelikeDebugger/Patches/PowerupInventoryPatch.cs": "41cc5596459569b4af7e0e70c27075c641159d70a9bfac2b80b5e2d6cdb7b7e8",
    "RoguelikeDebugger/Patches/SkillInventoryPatch.cs": "629d1d1f07e697996da020fa0a9f6c30b7cc592b01a48c83f53bf406ff6e02b1",
    "RoguelikeDebugger/RoguelikeDebugger.csproj": "d2df3d9a130b3a80f14ec35f1104c119f78fccf0c247cbccaa5ed36b6c648541",
}

# `campos.Add("chave=" + ...)` / `"chave=" +` em qualquer forma: a chave que o C# EMITE.
CHAVE_EMITIDA = re.compile(r'"([A-Za-z][A-Za-z0-9]*)="')


# -------------------------------------------------------------- verificador ---

def modulo_do_verificador():
    """Importa o `tools/verifica_proveniencia_debugger.py` REAL (nao uma copia digitada)."""
    if "_verif_prov_dbg_r2" in sys.modules:
        return sys.modules["_verif_prov_dbg_r2"]
    arc.exigir(os.path.isfile(VERIFICADOR), "nao achei o verificador: %s" % VERIFICADOR)
    spec = importlib.util.spec_from_file_location("_verif_prov_dbg_r2", VERIFICADOR)
    arc.exigir(spec is not None and spec.loader is not None,
               "nao consegui montar o import do verificador: %s" % VERIFICADOR)
    modulo = importlib.util.module_from_spec(spec)
    sys.modules["_verif_prov_dbg_r2"] = modulo
    spec.loader.exec_module(modulo)
    return modulo


def marca():
    return modulo_do_verificador().MARCA


def verificar(log, alvo=None):
    """(veredito, motivos, avisos, notas, campos) do verificador real."""
    return modulo_do_verificador().verificar(log, alvo)


def veredito(log, alvo=None):
    return verificar(log, alvo)[0]


def nome_do_veredito(codigo):
    return modulo_do_verificador().NOMES[codigo]


def campos_exigidos():
    """Os campos que o verificador EXIGE, lidos do proprio verificador."""
    modulo = modulo_do_verificador()
    return {
        "inicio": list(modulo.OBRIGATORIOS_INICIO),
        "estado": list(modulo.OBRIGATORIOS_ESTADO),
        "fim": list(modulo.OBRIGATORIOS_FIM),
    }


# ------------------------------------------------------------------ fontes ---

def caminho_da_fonte(rel):
    return os.path.join(RAIZ, rel.replace("/", os.sep))


def fonte(nome):
    caminho = caminho_da_fonte(FONTES[nome])
    arc.exigir(os.path.isfile(caminho), "nao achei a fonte: %s" % caminho)
    with open(caminho, encoding="utf-8") as arquivo:
        return arquivo.read()


def sha256(caminho):
    with open(caminho, "rb") as arquivo:
        return hashlib.sha256(arquivo.read()).hexdigest()


def hashes_intocados():
    """{caminho relativo: sha256 medido} - a conferencia e' feita pelo chamador."""
    return {rel: sha256(caminho_da_fonte(rel)) for rel in sorted(INTOCADOS)}


def campos_emitidos_no_cs():
    """As chaves que o C# do carimbo emite (lidas do fonte VIVO)."""
    texto = fonte("proveniencia")
    chaves = set(CHAVE_EMITIDA.findall(texto))
    # `dllDebugger=` e' montado por concatenacao (`"dllDebugger=" + ...`) e ja' entra no regex;
    # `estadoDump=` aparece em tres fases.
    return chaves


def faltando_no_cs():
    """Campos exigidos pelo verificador que o C# NAO emite - o contrato quebrado dos dois lados."""
    emitidos = campos_emitidos_no_cs()
    faltando = []
    for onde, campos in campos_exigidos().items():
        for chave in campos:
            if chave not in emitidos:
                faltando.append("%s: %s" % (onde, chave))
    return faltando


# ----------------------------------------------------------------- fixture ---

def fixture(caso, papel="entrada", ext="log"):
    return arc.caminho_fixture(caso, papel, ext)


def ler_fixture(caso):
    return arc.ler_texto(caso)


def fixtures_do_cartao():
    """Os quatro dumps versionados deste cartao, com o veredito esperado."""
    return {
        "dbg-r2-proveniencia": 0,
        "dbg-r2-sem-proveniencia": 1,
        "dbg-r2-truncado": 2,
        "dbg-r2-identidade-incoerente": 1,
    }


def alvo_do_repo():
    return ALVO
