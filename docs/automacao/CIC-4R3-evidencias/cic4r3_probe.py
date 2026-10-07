#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIC-4R3 - sonda INDEPENDENTE do revisor (nao e do autor).

Le o modulo do produto por caminho e mede, por execucao propria:
  P1 feed vs tooltip DIVERGENTE            -> REPROVADO
  P2 sem tooltip (so FEED)                 -> NAO_EXERCITADO (nunca OK)
  P3 tooltip fixture                       -> NAO_EXERCITADO
  P4 tooltip de outra build                -> INDETERMINADO
  P5 tooltip de outra sessao               -> INDETERMINADO
  P6 tooltip ausente + cadeia do FEED quebrada (N3-like) -> NAO_EXERCITADO do FEED (precedencia)
  P7 tooltip ausente + hash divergente     (N4-like)     -> INDETERMINADO do FEED (precedencia)
  P8 rodada completa autenticada           -> OK/prova_runtime=True (7 OK)
Uso: python cic4r3_probe.py [--modulo CAMINHO] [--repo RAIZ]
"""
import argparse
import importlib.util
import json
import os
import sys

REPO = r"C:\dev\stolen-realm"
MOD = os.path.join("tools", "automacao", "cenarios", "tooltips_shrines.py")
SHA, DLL = "ab" * 32, "cd" * 32
ART = os.path.join("tools", "fixtures", "shrines-rv46-dedupe.log")
FEED = "\n".join([
    "[Info   :Better Tooltips] [Shrine RV-23] RV-31 acumulado: auras=[Rogue Aura] char=ChkRA bonus=0 -> Dodge +20% (total +37%)",
    "[Info   :Better Tooltips] [Shrine RV-23] RV-31 acumulado: auras=[Rogue Aura] char=Raven bonus=100 -> Dodge +40% (total +52%)",
])
ID = "S-dois-personagens-rogue/receptor/bonus=0"


def carga(caminho, repo):
    with open(caminho, encoding="utf-8") as fh:
        fonte = fh.read()
    mod = type(sys)("mod_probe")
    mod.__file__ = os.path.join(repo, MOD)
    exec(compile(fonte, caminho, "exec"), mod.__dict__)
    return mod


def feed(**x):
    o = {"objeto": ART, "procedencia": "runtime", "sessao": "s1", "hash_fonte": DLL,
         "evidencia": [ART], "feed": FEED}
    o.update(x)
    return o


def tool(**x):
    o = {"objeto": "Tooltip.LinhaAzul (ChkRA)", "personagem": "ChkRA", "procedencia": "runtime",
         "sessao": "s1", "hash_fonte": DLL, "evidencia": [ART],
         "texto_renderizado": "Your active shrine auras: Dodge +20% (total +37%)."}
    o.update(x)
    return o


def mede(mod, nome, obs):
    crits = mod.avaliar(obs, {"fonte_sha": SHA, "dll_sha": DLL})
    c = [x for x in crits if x["id"] == ID][0]
    cont = mod.resumo(crits)
    print("  %-28s estado=%-15s prova_runtime=%-5s exit=%-2s feed_vs_tooltip=%-14s prova_runtime_total=%s"
          % (nome, c["estado"], c["prova_runtime"], mod.exit_de(crits),
             c["observado"].get("feed_vs_tooltip"), cont.get("com_prova_runtime")))
    print("      motivo: %s" % c["motivo"][:160])
    return c["estado"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modulo", default=os.path.join(REPO, MOD))
    ap.add_argument("--repo", default=REPO)
    a = ap.parse_args()
    mod = carga(a.modulo, a.repo)
    obtido = []
    obtido.append(mede(mod, "P8-completa-OK",
                       [feed(), tool(),
                        tool(personagem="Raven", objeto="Tooltip.LinhaAzul (Raven)",
                             texto_renderizado="Your active shrine auras: Dodge +40% (total +52%).")]))
    obtido.append(mede(mod, "P1-feed-vs-tooltip-DIVERGE",
                       [feed(), tool(objeto="Tooltip.LinhaAzul (ChkRA-DIVERGE)",
                                     texto_renderizado="Your active shrine auras: Dodge +99% (total +99%).")]))
    obtido.append(mede(mod, "P2-sem-tooltip", [feed()]))
    obtido.append(mede(mod, "P3-tooltip-fixture", [feed(), tool(procedencia="fixture")]))
    obtido.append(mede(mod, "P4-tooltip-outra-build", [feed(), tool(hash_fonte="ff" * 32)]))
    obtido.append(mede(mod, "P5-tooltip-outra-sessao", [feed(), tool(sessao="s9")]))
    obtido.append(mede(mod, "P6-sem-tooltip+feed-sem-hash", [feed(hash_fonte=None)]))
    obtido.append(mede(mod, "P7-sem-tooltip+feed-hash-errado", [feed(hash_fonte="ff" * 32)]))
    print("ESTADOS: %s" % obtido)
    espera = ["OK", "REPROVADO", "NAO_EXERCITADO", "NAO_EXERCITADO", "INDETERMINADO",
              "INDETERMINADO", "NAO_EXERCITADO", "INDETERMINADO"]
    print("DIVERGENCIAS: %s" % [i for i, (g, e) in enumerate(zip(obtido, espera)) if g != e])
    return 0 if obtido == espera else 1


if __name__ == "__main__":
    sys.exit(main())
