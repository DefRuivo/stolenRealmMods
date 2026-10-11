#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BUG-34T - A PROVA DE FOGO FISICA no `LocalizePatch.cs` REAL (bancada reproduzivel, fora da suite).

O QUE ESTA BANCADA PROVA
------------------------
O achado BUG-34T: a trava antiga recortava uma JANELA de 2200 chars em volta de cada alvo, e a
janela da PRIMEIRA entrada de feed alcancava o bloco VIZINHO. Planta cada defeito no FONTE REAL,
roda o teste pelo RUNNER de verdade e exige `REPROVOU` (exit 1) pelo MOTIVO CERTO — e mede, na
mesma fonte plantada, o que a janela REMOVIDA respondia (nos defeitos da entrada de texto ela dava
VERDE: e o furo). O fonte e restaurado BYTE A BYTE (sha256 conferido) depois de cada isca.

Uso (da raiz do repo):
    python tools/testes/bt34-feed-prova-de-fogo.py > tools/testes/bt34-feed-prova-de-fogo.log
"""
import hashlib
import os
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(DIR))
sys.path.insert(0, DIR)

import arcabouco as arc          # noqa: E402
import regras_bt_texto as R      # noqa: E402

FONTE = os.path.join(RAIZ, "BetterTooltips", "Patches", "LocalizePatch.cs")
TESTE = os.path.join("tools", "testes", "testes", "puros", "t_bt34_nota_fora_do_feed.py")
ROTULO_TXT = R.ENTRADAS_DE_FEED[0][0]
ALVO_TXT = R.ENTRADAS_DE_FEED[0][1]


def sha256(caminho):
    with open(caminho, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def le():
    # VERBATIM (newline="" = sem traducao): o fonte e CRLF e tem de VOLTAR CRLF — o sha256 da
    # restauracao so fecha se os bytes forem os mesmos, nao se o texto "parecer" igual.
    with open(FONTE, encoding="utf-8", newline="") as fh:
        return fh.read()


def escreve(texto):
    with open(FONTE, "w", encoding="utf-8", newline="") as fh:
        fh.write(texto)


def em_crlf(texto):
    """De volta ao fim de linha do arquivo (o plantio e medido em LF; o disco recebe CRLF)."""
    return texto.replace("\n", "\r\n")


def roda_teste():
    """O teste pelo RUNNER de verdade (exit code cru + saida)."""
    proc = subprocess.run([sys.executable, "tools/testes/roda_testes.py", "--teste", TESTE],
                          cwd=RAIZ, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          universal_newlines=True, timeout=600)
    return proc.returncode, proc.stdout or ""


def plantas(real):
    """(nome, fonte plantada, motivo esperado, a janela antiga era CEGA?)"""
    return [
        ("ENTRAR removido da entrada de TEXTO (battle log)",
         R.sem_trecho_no_bloco(real, ALVO_TXT, "                    EntrarTextoDeFeed();\n"),
         "nao ENTRA", True),
        ("SAIR removido da entrada de TEXTO (battle log)",
         R.sem_trecho_no_bloco(real, ALVO_TXT, "                    SairTextoDeFeed();\n"),
         "nao SAI", True),
        ("FINALIZER removido da entrada de TEXTO (battle log)",
         R.sem_trecho_no_bloco(real, ALVO_TXT, "            private static void Finalizer()\n"),
         "nao tem `Finalizer`", True),
        ("ARMOR sem guard (controle: a janela antiga TAMBEM pegava)",
         real.replace(R.GUARD_ARMOR, R.GUARD_ARMOR.replace("!ehTextoDeFeed && ", "", 1), 1),
         "regra de ARMOR", False),
    ]


def main():
    if not os.path.isfile(FONTE):
        raise SystemExit("nao achei o fonte: %s" % FONTE)
    cru = le()
    antes = sha256(FONTE)
    print("FONTE: %s" % FONTE)
    print("sha256 ANTES: %s (%d bytes)" % (antes, len(cru.encode("utf-8"))))
    print("teste: %s" % TESTE)

    # O plantio e medido em LF; a ida-e-volta para o arquivo (CRLF) tem de ser BYTE-IDENTICA.
    if em_crlf(cru.replace("\r\n", "\n")) != cru:
        raise SystemExit("!! o fonte nao e CRLF puro: a ida-e-volta de fim de linha nao e identica "
                         "(nao mexo no arquivo)")
    print("fim de linha: CRLF puro (a ida-e-volta e byte-identica)")
    original = cru.replace("\r\n", "\n")

    falhas = 0
    try:
        for nome, plantado, motivo, janela_cega in plantas(real=original):
            if plantado == original:
                print("\n!! a isca %r nao plantou nada" % nome)
                falhas += 1
                continue
            print("\n" + "=" * 78)
            print("ISCA: %s" % nome)
            print("=" * 78)

            # o que a janela REMOVIDA respondia nesta fonte plantada (a medida do furo)
            vjan = R.falhas_da_janela_2200(plantado)
            print("janela de %d chars (checagem REMOVIDA): %s"
                  % (R.JANELA_REMOVIDA, "VERDE (cega)" if not vjan else "reprova %r" % vjan))
            if janela_cega and vjan:
                print("!! a janela antiga DEVIA estar cega a este defeito: %r" % vjan)
                falhas += 1

            escreve(em_crlf(plantado))
            try:
                codigo, saida = roda_teste()
            finally:
                escreve(cru)
            print("REPROVOU?" if codigo == 1 else "NAO REPROVOU (exit %d)" % codigo)
            for linha in saida.splitlines():
                if ("REPROVOU" in linha or "PROVA" in linha or motivo in linha or "VEREDITO" in linha
                        or "detalhe" in linha):
                    print("   | %s" % linha.strip())
            if codigo != 1:
                print("!! o teste NAO reprovou o defeito plantado (exit %d)" % codigo)
                falhas += 1
            if motivo not in saida:
                print("!! o teste nao reprovou pelo MOTIVO CERTO (esperava %r)" % motivo)
                falhas += 1

            depois = sha256(FONTE)
            print("sha256 DEPOIS: %s -> %s" % (depois, "RESTAURADO byte a byte" if depois == antes
                                               else "!!! NAO RESTAUROU"))
            if depois != antes:
                falhas += 1
    finally:
        escreve(cru)

    final = sha256(FONTE)
    print("\n" + "=" * 78)
    print("fonte final: %s (%s)" % (final, "IDENTICO ao inicial" if final == antes else "DIVERGENTE"))
    # a fonte restaurada tem de voltar a APROVAR (o teste fica verde de novo)
    codigo, _saida = roda_teste()
    print("teste na fonte restaurada: %s (exit %d)"
          % ("PASSOU (VERDE)" if codigo == 0 else "REPROVOU", codigo))
    if codigo != 0:
        falhas += 1
    if final != antes:
        falhas += 1

    print("\nRESULTADO DA BANCADA: %s" % ("TODAS AS ISCAS OK" if falhas == 0
                                          else "%d PROBLEMA(S)" % falhas))
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
