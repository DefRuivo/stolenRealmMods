#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rv28-globule-prova-de-fogo.py - a prova FISICA da blindagem do RV-28.

Roda FORA da suite (nome sem `t_`/`cp_`: o runner o CONTA como ignorado, nao como teste). E a
bancada reproduzivel que produziu `rv28-globule-prova-de-fogo.log`.

Para CADA defeito da lista de guardas obrigatorias, mede o ciclo inteiro no arquivo REAL
(`BetterTooltips/Patches/GlobulePatch.cs`):

  1. o teste PASSA no repo como esta (exit 0);
  2. o defeito PLANTADO no arquivo real faz o teste REPROVAR (exit 1);
  3. o arquivo e RESTAURADO byte a byte (sha256 conferido).

Nada e instalado, nada e commitado; nenhum arquivo fica modificado. Nenhum defeito toca a DLL do
jogo nem o perfil do r2modman - so o FONTE do mod, sempre restaurado.

    python tools/testes/rv28-globule-prova-de-fogo.py | tee tools/testes/rv28-globule-prova-de-fogo.log
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
TESTE = os.path.join(AQUI, "testes", "puros", "t_rv28_globule_sustenance.py")
ALVO_REL = os.path.join("BetterTooltips", "Patches", "GlobulePatch.cs")

# (rotulo, trecho-antes, trecho-depois, o que a guarda tem de acusar)
PLANTIOS = (
    ("A: sem a guarda de existencia",
     'if (!AtributoExiste(personagem, "MaxHealth") || !AtributoExiste(personagem, "MaxMana"))',
     "if (false)",
     "a guarda de existencia ANTES da leitura do atributo"),

    ("B: soma a mao tier I + tier II (28)",
     "pct += daSkill;",
     "pct += 8f + 20f;",
     "a % tem de vir da lista ATIVA do jogo, nunca de uma soma a mao"),

    ("C: o catch re-lanca (tooltip quebra)",
     'Plugin.Log.LogWarning($"[Globule RV-28] frase do Sustenance falhou (tooltip intacto): '
     '{ex.GetType().Name}: {ex.Message}");\n                return "";',
     "throw ex;",
     "a queda para o texto SEM numero, no proprio catch"),

    ("D: a guarda indexa o personagem (lanca)",
     "if (jogo.GetAttribute(nome) != null)",
     "if (personagem[nome] != 0f)",
     "a guarda nao pode indexar (usar as consultas que devolvem null)"),
)


def le(caminho):
    with open(caminho, "rb") as fh:
        return fh.read()


def escreve_bytes(caminho, dados):
    with open(caminho, "wb") as fh:
        fh.write(dados)


def roda_teste():
    proc = subprocess.run([sys.executable, RODA, "--teste", TESTE],
                          cwd=RAIZ, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          universal_newlines=True, timeout=300)
    detalhe = ""
    for linha in (proc.stdout or "").splitlines():
        if linha.startswith("[PASSOU ]") or linha.startswith("[REPROVOU]"):
            detalhe = linha.strip()
    return proc.returncode, detalhe


def _variante(antes, texto):
    """O `antes` com \\n ou com \\r\\n - o que casar 1x no texto (o repo mistura EOL)."""
    for cand in (antes, antes.replace("\n", "\r\n")):
        if texto.count(cand) == 1:
            return cand
    return None


def main():
    alvo = os.path.join(RAIZ, ALVO_REL)
    print("=" * 78)
    print(" PROVA DE FOGO FISICA - blindagem do RV-28 (guardas do tooltip do globule)")
    print(" raiz: %s" % RAIZ)
    print(" alvo: %s" % ALVO_REL)
    print(" teste: %s" % os.path.relpath(TESTE, RAIZ))
    print("=" * 78)
    falhou = False

    original = le(alvo)
    texto = original.decode("utf-8")
    h_original = hashlib.sha256(original).hexdigest()
    print("\nsha256 do alvo (limpo): %s" % h_original)

    # 0. o teste PASSA no repo como esta.
    cod_ok, det_ok = roda_teste()
    print("\n[0] repo como esta -> exit %d  (%s)" % (cod_ok, det_ok))
    if cod_ok != 0:
        print("    ESPERAVA PASSOU - o teste tem de passar ANTES de plantar o defeito.")
        return 1

    for rotulo, antes, depois, o_que_morde in PLANTIOS:
        print("\n[%s]" % rotulo)
        print("  espera acusar: %s" % o_que_morde)
        ancora = _variante(antes, texto)
        if ancora is None:
            print("  ANCORA INVALIDA: %r nao aparece 1x em %s" % (antes[:60], ALVO_REL))
            falhou = True
            continue
        mutado = texto.replace(ancora, depois, 1)
        escreve_bytes(alvo, mutado.encode("utf-8"))
        try:
            cod_def, det_def = roda_teste()
        finally:
            escreve_bytes(alvo, original)
        h_depois = hashlib.sha256(le(alvo)).hexdigest()
        print("  1. defeito plantado -> exit %d  (%s)" % (cod_def, det_def))
        print("  2. restaurado       -> sha256 %s (%s)"
              % (h_depois[:16], "IDENTICO" if h_depois == h_original else "!!! DIVERGENTE !!!"))
        if cod_def != 1:
            print("     ESPERAVA REPROVOU (exit 1) - a trava NAO mordeu o defeito.")
            falhou = True
        if h_depois != h_original:
            print("     FALHA GRAVE: o arquivo NAO foi restaurado byte a byte.")
            falhou = True

    print("\n" + "=" * 78)
    if falhou:
        print(" VEREDITO: PROVA DE FOGO FALHOU")
        return 1
    print(" VEREDITO: PROVA DE FOGO OK - o teste passa no repo, REPROVA em cada um dos %d defeitos"
          % len(PLANTIOS))
    print("           plantados no fonte real e o arquivo volta byte a byte (sha256 igual).")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
