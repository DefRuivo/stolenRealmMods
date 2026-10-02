#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""SEM ACOPLAMENTO: o BetterFont nao cita o outro mod (TST-7, cenario 6).

O QUE ESTE TESTE GARANTE
------------------------
Invariante 3 do projeto (`docs/PLANO-DE-TESTES.md`): "Mods nao se referenciam entre si
(zero ocorrencia do nome/GUID de um no codigo do outro)". O BetterFont e o
BetterCombatText convivem (o halos dos textos de combate), e a regra que faz isso ser
generico - e nao um caso especial - e justamente esta: o CODIGO do BetterFont nao pode
conhecer o outro mod. A regra de copia e "o que estava no material anterior daquele texto
continua la", para QUALQUER mod.

Este teste-testemunha varre:
  1. o CODIGO (`BetterFont/Plugin.cs`) - sempre;
  2. a DLL CONSTRUIDA do BetterFont (build local, `BetterFont/bin/`) quando ela existir -
     o nome/GUID apareceria nos metadados ou num literal, em UTF-8 ou UTF-16LE (.NET);
  3. o PROPRIO DETECTOR: um blob sintetico com o nome em UTF-16LE TEM de ser flagrado, e um
     blob limpo NAO - senao um detector quebrado ("varre e nao acha nada") passaria por
     acoplamento zero.

O QUE NAO ESTA NESTE ESCOPO (de proposito)
------------------------------------------
A DOC do mod (`README.md`, `CHANGELOG.md`) CITA o outro mod para EXPLICAR a convivencia
entre os dois, e isso e pedido pelo dono - o que nao pode e o CODIGO conhecer o outro mod.
Por isso a varredura e de `BetterFont/Plugin.cs` e da DLL, nunca do README.

A contra-prova embutida injeta o nome E o GUID do outro mod no fonte EM MEMORIA: a
varredura TEM de acusar os dois. A rodada fisica esta em `tools/testes/bf-prova-reprovando.log`.
"""
import os

import regras_bf_estilo as reg

import arcabouco as arc

META = {
    "nome": "bf-sem-acoplamento",
    "categoria": "pura",
    "requer": [],
    "descricao": "TST-7: invariante 3 - o codigo do BetterFont (fonte e DLL) nao cita nome/GUID do outro mod; e o detector nao e vazio",
}


def corpo():
    src = reg.fonte()
    arc.exigir(len(src) > 5000, "o fonte do BetterFont veio vazio/curto: a leitura mudou de lugar?")

    # ---- 1) o CODIGO: o fonte vivo.
    acoplamentos = reg.ocorrencias_de_acoplamento(src)
    arc.exigir(not acoplamentos,
               "o CODIGO do BetterFont cita outro mod: %s (o invariante 3 proibe; a copia de "
               "estilo tem de valer para QUALQUER mod, nao para um caso especifico)" % acoplamentos)

    # ---- 3) o DETECTOR nao e vazio: com um blob sintetico (ASCII + UTF-16LE, como o .NET)
    #       acusa; com um blob limpo, nao.
    sujo = b"\x00\x01\x02BetterCombatText\x03\x04" + "com.gumatos.bettercombattext".encode("utf-16-le")
    achados_sujos = reg.ocorrencias_nos_bytes(sujo)
    arc.exigir(any("BetterCombatText" in a for a in achados_sujos) and
               any("com.gumatos.bettercombattext" in a for a in achados_sujos),
               "o detector de binario NAO acusou um blob com o nome e o GUID do outro mod: "
               "a varredura da DLL estaria passando por nao achar nada (%r)" % achados_sujos)
    arc.exigir(not reg.ocorrencias_nos_bytes(b"\x00" * 64 + b"BetterFont"),
               "o detector acusou acoplamento num blob LIMPO: falso positivo")

    # ---- 2) a DLL construida, quando existir.
    dlls = reg.dlls_do_betterfont()
    for dll in dlls:
        arc.exigir(os.path.getsize(dll) > 0, "a DLL %s veio vazia" % dll)
        achados = reg.ocorrencias_no_binario(dll)
        arc.exigir(not achados,
                   "a DLL %s cita outro mod: %s" % (os.path.relpath(dll, arc.raiz_do_repo()), achados))

    # ---- CONTRA-PROVA EMBUTIDA: o defeito plantado (nome E GUID no fonte) tem de ser acusado.
    com_acoplamento = reg.defeito_acopla_outro_mod(src)
    arc.exigir(com_acoplamento != src, "o plantio do acoplamento nao achou onde agir")
    acusados = reg.ocorrencias_de_acoplamento(com_acoplamento)
    arc.exigir(len(acusados) >= 2,
               "o plantio citou o nome E o GUID do outro mod, mas a varredura acusou so %r" % acusados)

    print("fonte limpo (%d termo(s) proibido(s) varrido(s), 0 achado); detector de binario provado "
          "no blob sujo/limpo; %d DLL(s) construida(s) varrida(s) e limpa(s); o acoplamento "
          "plantado acusa %d termo(s)"
          % (len(reg.PROIBIDOS), len(dlls), len(acusados)))


if __name__ == "__main__":
    arc.main(META, corpo)
