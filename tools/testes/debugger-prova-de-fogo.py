#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""debugger-prova-de-fogo.py - a prova FISICA dos testes do dump (TST-5).

Roda FORA da suite (nome sem `t_`/`cp_`: o runner o CONTA como ignorado, nao como
teste). E a bancada reproduzivel que produziu `debugger-prova-de-fogo.log`.

O que ele mede, para CADA teste da familia do RoguelikeDebugger:

  1. o teste PASSA no repo limpo (exit 0);
  2. um defeito PLANTADO no arquivo real faz o teste REPROVAR (exit 1);
  3. o arquivo e RESTAURADO byte a byte (sha256 conferido).

Nada e instalado, nada e commitado; nenhum arquivo fica modificado. O defeito nunca
toca um mod de jogador - so `tools/census.py` (ferramenta) e o proprio Debugger (mod
de diagnostico), sempre restaurados.

    python tools/testes/debugger-prova-de-fogo.py | tee tools/testes/debugger-prova-de-fogo.log
"""
import hashlib
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

import arcabouco as arc  # noqa: E402

RAIZ = arc.raiz_do_repo()
RODA = os.path.join(AQUI, "roda_testes.py")
PUROS = os.path.join(AQUI, "testes", "puros")

# (rotulo, teste, arquivo-alvo, trecho-antes, trecho-depois)
# O `antes` tem de aparecer EXATAMENTE UMA vez no alvo.
PLANTIOS = (
    ("parser-censo",
     os.path.join(PUROS, "t_debugger_parser_contrato.py"),
     os.path.join("tools", "census.py"),
     r'r"|efeitosRef|refAcao|refStatus|nEfeitos|nEfeitosRef|efeitosDano|nEfeitosDano"',
     r'r"|efeitosRef|refAcao|refStatus|nEfeitos|nEfeitosRef|efeitosDano"'),

    ("reflexao-cast",
     os.path.join(PUROS, "t_debugger_reflexao_cast.py"),
     os.path.join("RoguelikeDebugger", "EfeitosInfo.cs"),
     "Type t = o.GetType();\n            string nome = t.Name;",
     'Type t = o.GetType();\n            string nome = (o as GeneralEffect) != null ? "GeneralEffect" : "?";'),

    ("saneamento",
     os.path.join(PUROS, "t_debugger_saneamento.py"),
     os.path.join("RoguelikeDebugger", "EfeitosInfo.cs"),
     '.Replace("|", "/")',
     ""),   # remove a troca do separador -> o Limpa deixa de sanear '|'

    ("estabilidade",
     os.path.join(PUROS, "t_debugger_estabilidade.py"),
     os.path.join("tools", "census.py"),
     '["nome", "arvore", "tier",',
     '["nome", "tier",'),
)


def sha256(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def le(caminho):
    with open(caminho, "rb") as fh:
        return fh.read()


def escreve_bytes(caminho, dados):
    with open(caminho, "wb") as fh:
        fh.write(dados)


def roda_teste(teste):
    proc = subprocess.run([sys.executable, RODA, "--teste", teste],
                          cwd=RAIZ, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          universal_newlines=True, timeout=300)
    detalhe = ""
    for linha in (proc.stdout or "").splitlines():
        # O RUNNER consome a linha RESULTADO| do teste e imprime o RELATORIO; o que
        # se le de volta aqui e a linha do relatorio.
        if linha.startswith("[PASSOU ]") or linha.startswith("[REPROVOU]"):
            detalhe = linha.strip()
    return proc.returncode, detalhe


def _variante(antes, texto):
    """O `antes` com \n ou com \r\n - o que casar no texto (o repo mistura EOL)."""
    for cand in (antes, antes.replace("\n", "\r\n")):
        if texto.count(cand) == 1:
            return cand
    return None


def main():
    print("=" * 78)
    print(" PROVA DE FOGO FISICA - testes do RoguelikeDebugger (TST-5)")
    print(" raiz: %s" % RAIZ)
    print("=" * 78)
    falhou = False
    for rotulo, teste, alvo_rel, antes, depois in PLANTIOS:
        alvo = os.path.join(RAIZ, alvo_rel)
        if not os.path.isfile(teste):
            print("\n[%s] TESTE AUSENTE: %s" % (rotulo, teste))
            falhou = True
            continue
        original = le(alvo)
        texto = original.decode("utf-8")
        h_antes = hashlib.sha256(original).hexdigest()[:16]
        print("\n[%s] alvo: %s (sha256 %s...)" % (rotulo, alvo_rel, h_antes))

        # 1. o teste PASSA no repo limpo.
        cod_ok, det_ok = roda_teste(teste)
        print("  1. repo limpo      -> exit %d  (%s)" % (cod_ok, det_ok))
        if cod_ok != 0:
            print("     ESPERAVA PASSOU - sem o defeito o teste tem de passar.")
            falhou = True
            continue

        # 2. planta o defeito.
        ancora = _variante(antes, texto)
        if ancora is None:
            print("     ANCORA INVALIDA: %r nao aparece 1x em %s" % (antes, alvo_rel))
            falhou = True
            continue
        mutado = texto.replace(ancora, depois.replace("\n", "\r\n") if "\r\n" in ancora else depois, 1)
        escreve_bytes(alvo, mutado.encode("utf-8"))
        try:
            cod_def, det_def = roda_teste(teste)
        finally:
            # 3. restaura e confere byte a byte.
            escreve_bytes(alvo, original)
        h_depois = hashlib.sha256(le(alvo)).hexdigest()[:16]
        print("  2. defeito plantado -> exit %d  (%s)" % (cod_def, det_def))
        print("  3. restaurado       -> sha256 %s... (%s)"
              % (h_depois, "IDENTICO" if h_depois == h_antes else "!!! DIVERGENTE !!!"))
        if cod_def != 1:
            print("     ESPERAVA REPROVOU (exit 1) - a trava NAO mordeu o defeito.")
            falhou = True
        if h_depois != h_antes:
            print("     FALHA GRAVE: o arquivo NAO foi restaurado byte a byte.")
            falhou = True

    print("\n" + "=" * 78)
    if falhou:
        print(" VEREDITO: PROVA DE FOGO FALHOU")
        return 1
    print(" VEREDITO: PROVA DE FOGO OK - cada teste passa limpo, reprova com o defeito")
    print("           plantado e o arquivo volta byte a byte (sha256 igual).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
