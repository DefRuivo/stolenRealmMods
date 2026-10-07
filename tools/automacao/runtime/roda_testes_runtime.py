#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""roda_testes_runtime.py - runner dos testes OFFLINE do runtime AUT-4.

    python tools/automacao/runtime/roda_testes_runtime.py
    python tools/automacao/runtime/roda_testes_runtime.py --contra-prova

NUM COMANDO RODA TUDO e o exit code diz a verdade (mesma convencao do runner do
projeto, tools/testes/roda_testes.py):

    0  tudo verde
    1  algo REPROVOU   (em --contra-prova: uma isca PASSOU, o que e red)
    2  NAO CONSEGUI RODAR / nenhum teste encontrado

Nao abre o jogo, nao instala probe, nao toca no perfil: e a preparacao offline.
"""
import argparse
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
DIR_TESTES = os.path.join(AQUI, "testes")
DIR_CONTRA = os.path.join(DIR_TESTES, "contra-prova")


def descobrir(raiz, prefixo):
    if not os.path.isdir(raiz):
        return []
    return sorted(os.path.join(raiz, n) for n in os.listdir(raiz)
                  if n.startswith(prefixo) and n.endswith(".py"))


def rodar(caminhos, raiz):
    registros = []
    for caminho in caminhos:
        proc = subprocess.run([sys.executable, caminho], cwd=raiz,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              universal_newlines=True, timeout=300)
        registros.append({"arquivo": os.path.relpath(caminho, raiz),
                          "nome": os.path.splitext(os.path.basename(caminho))[0],
                          "exit": proc.returncode, "saida": (proc.stdout or "").strip()})
    return registros


def classificar_contra_prova(codigo, saida):
    """R-5 (CIC-5R): a isca so conta como PROVA se reprovar DE PROPOSITO.

    Antes, `exit == 1` sozinho bastava — e o arcabouco converte EXCECAO INESPERADA em
    exit 1 tambem, entao um crash passava por "reprovou como devia" e metade do
    controle negativo nao provava nada. Agora exigimos a linha `RESULTADO|REPROVOU|`
    (reprovacao pelo `Falhou`/assert) e a AUSENCIA de `excecao inesperada`.

    Devolve `(estado_legivel, vermelho)`.
    """
    if codigo == 0:
        return "PROVA FALHOU (passou quando devia reprovar)", True
    if codigo != 1:
        return "NAO RODOU", True
    texto = saida or ""
    if "RESULTADO|REPROVOU|" not in texto:
        return "PROVA FALHOU (exit 1 sem a linha RESULTADO|REPROVOU|)", True
    if "excecao inesperada" in texto:
        return "PROVA FALHOU (reprovou por EXCECAO, nao por assert)", True
    return "PROVA OK (reprovou como devia)", False


def main():
    ap = argparse.ArgumentParser(description="Runner dos testes offline do runtime AUT-4.")
    ap.add_argument("--contra-prova", action="store_true",
                    help="roda as iscas de testes/contra-prova/ EXIGINDO que REPROVEM")
    args = ap.parse_args()

    if args.contra_prova:
        caminhos = descobrir(DIR_CONTRA, "cp_")
        modo = "contra-prova (a isca TEM de reprovar)"
    else:
        caminhos = descobrir(DIR_TESTES, "t_")
        modo = "suite offline"

    print("=" * 74)
    print(" AUT-4 runtime — %s" % modo)
    print(" raiz: %s" % AQUI)
    print("=" * 74)
    if not caminhos:
        print(" NENHUM TESTE ENCONTRADO — nada executado nao e verde.")
        return 2

    registros = rodar(caminhos, AQUI)
    vermelho = False
    for r in registros:
        if args.contra_prova:
            estado, falhou = classificar_contra_prova(r["exit"], r["saida"])
            if falhou:
                vermelho = True
        else:
            estado = {0: "PASSOU", 1: "REPROVOU", 2: "NAO RODOU"}.get(r["exit"], "?")
            if r["exit"] != 0:
                vermelho = True
        print("[%-42s] %s" % (estado, r["arquivo"]))
        if r["exit"] != 0:
            for linha in r["saida"].splitlines():
                print("        | %s" % linha)

    print("=" * 74)
    if vermelho:
        print(" VEREDITO: VERMELHO (exit 1)")
        return 1
    print(" VEREDITO: VERDE (exit 0) — %d teste(s)" % len(registros))
    return 0


if __name__ == "__main__":
    sys.exit(main())
