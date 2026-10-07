#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIC-4R3 - sonda 2 do revisor: cantos e a fronteira DECLARADA (nao ampliada) do COR-CIC4.

  C1 observacao COMBINADA (feed + personagem + texto_renderizado no MESMO objeto) runtime
  C2 rodada runtime completa SEM tooltips -> quais criterios ficam OK/prova_runtime=True
     (a fronteira declarada: Dwarven/sem_atributo, Flame/perigo e regressao NAO comparam tooltip)
  C4 rodada de FIXTURE (feed fixture + tooltip fixture) -> OK nao-vinculante (prova_runtime=False)
Uso: python cic4r3_probe2.py [--modulo CAMINHO] [--repo RAIZ]
"""
import argparse
import os
import sys

REPO = r"C:\dev\stolen-realm"
MOD = os.path.join("tools", "automacao", "cenarios", "tooltips_shrines.py")
SHA, DLL = "ab" * 32, "cd" * 32
ART = os.path.join("tools", "fixtures", "shrines-rv46-dedupe.log")
FEED = "\n".join([
    "[Info   :Better Tooltips] [Shrine RV-23] RV-31 acumulado: auras=[Rogue Aura] char=ChkRA bonus=0 -> Dodge +20% (total +37%)",
    "[Info   :Better Tooltips] [Shrine RV-23] RV-31 acumulado: auras=[Rogue Aura] char=Raven bonus=100 -> Dodge +40% (total +52%)",
    "[Info   :Better Tooltips] [Shrine RV-23] RV-31 acumulado: auras=[Dwarven Aura] char=ChkDW0 bonus=0 -> Stun chance +20%",
    "[Info   :Better Tooltips] [Shrine RV-23] RV-31 acumulado: auras=[Dwarven Aura] char=ChkDW20 bonus=20 -> Stun chance +24%",
    "[Info   :Better Tooltips] [Shrine RV-23] RV-31 acumulado: auras=[Dwarven Aura] char=ChkDW bonus=100 -> Stun chance +40%",
    "[Info   :Better Tooltips] [Shrine RV-23] RV-34 Flame alvo 'ChkGob': MaxHealth=100 tipo=Fodder bonus=100 dano=14",
])


def carga(caminho, repo):
    with open(caminho, encoding="utf-8") as fh:
        fonte = fh.read()
    mod = type(sys)("mod_probe2")
    mod.__file__ = os.path.join(repo, MOD)
    exec(compile(fonte, caminho, "exec"), mod.__dict__)
    return mod


def feed(**x):
    o = {"objeto": ART, "procedencia": "runtime", "sessao": "s1", "hash_fonte": DLL,
         "evidencia": [ART], "feed": FEED}
    o.update(x)
    return o


def mostra(nome, crits, mod):
    print("== %s (exit=%s)" % (nome, mod.exit_de(crits)))
    for c in crits:
        print("   %-52s %-15s prova_runtime=%-5s fvt=%s"
              % (c["id"], c["estado"], c["prova_runtime"],
                 (c["observado"] or {}).get("feed_vs_tooltip")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modulo", default=os.path.join(REPO, MOD))
    ap.add_argument("--repo", default=REPO)
    a = ap.parse_args()
    mod = carga(a.modulo, a.repo)

    combinada = [feed(personagem="ChkRA", objeto="Tooltip.LinhaAzul (ChkRA)",
                      texto_renderizado="Your active shrine auras: Dodge +20% (total +37%).")]
    mostra("C1 observacao COMBINADA (feed+tooltip no mesmo objeto runtime)", mod.avaliar(combinada, {"fonte_sha": SHA, "dll_sha": DLL}), mod)

    sem_tooltip = [feed(), {"objeto": os.path.join("BetterTooltips", "Patches", "LocalizePatch.cs"),
                            "procedencia": "runtime", "sessao": "s1", "hash_fonte": DLL,
                            "evidencia": [ART], "texto_renderizado": "Increased Armor Applied"}]
    mostra("C2 rodada runtime SEM nenhuma tooltip de personagem", mod.avaliar(sem_tooltip, {"fonte_sha": SHA, "dll_sha": DLL}), mod)

    fixture = [feed(procedencia="fixture"), {"objeto": "Tooltip.LinhaAzul (ChkRA)",
                                             "personagem": "ChkRA", "procedencia": "fixture",
                                             "rotulo_fixture": "probe2",
                                             "texto_renderizado": "Your active shrine auras: Dodge +20% (total +37%)."}]
    crits = mod.avaliar(fixture, {"fonte_sha": SHA, "dll_sha": DLL})
    mostra("C4 rodada de FIXTURE (feed+tooltip fixture)", crits, mod)
    print("C4 resumo: %s" % mod.resumo(crits))
    return 0


if __name__ == "__main__":
    sys.exit(main())
