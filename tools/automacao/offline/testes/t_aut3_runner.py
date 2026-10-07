#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teste do mapeamento de cobertura do orquestrador AUT-3 (matriz AUT-2 -> AUT-3).

Contra-prova do proprio mapeador: uma isca de contra-prova (PROVA_OK) das
t_rstv* NAO pode rebaixar o criterio T-RSTV6; runtime tem de sair
NAO_EXERCITADO (nunca OK); e um mod com build provado sai OK_OFFLINE.

Uso: python tools/automacao/offline/testes/t_aut3_runner.py
"""
import json
import os
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.dirname(AQUI)
sys.path.insert(0, LIB)
import aut3_lib      # noqa: E402
import bancada_aut3  # noqa: E402

RESULTADOS = []


def checar(nome, cond, detalhe=""):
    RESULTADOS.append((nome, bool(cond)))
    print("RESULTADO|%s|%s|%s" % ("PASSOU" if cond else "REPROVOU", nome, detalhe))


def main():
    matriz = {"cobertura": [
        {"id": "M1", "mod": "BetterFont"},
        {"id": "T-RSTV6", "mod": "RoguelikeSkillTreeVisualizer"},
        {"id": "T-RSTV21", "mod": "RoguelikeSkillTreeVisualizer"},
        {"id": "S-RV-26", "mod": "BetterTooltips"},
        {"id": "X-RUNTIME-NAO-DECLARADO", "mod": "RoguelikeSkillTreeVisualizer"},
        {"id": "AUT-REUSE", "mod": "transversal"},
    ]}
    with tempfile.TemporaryDirectory(prefix="aut3-map-", dir=aut3_lib.area_trabalho()) as repo:
        os.makedirs(os.path.join(repo, "docs", "automacao"))
        os.makedirs(os.path.join(repo, "tools", "testes"))
        # alvos de REUSO do AUT-REUSE: sem eles o criterio NAO pode ser OK (AUT-3F).
        for rel in ("tools/testes/roda_testes.py", "tools/checa_shrines.py"):
            with open(os.path.join(repo, rel), "w", encoding="utf-8") as fh:
                fh.write("# alvo de reuso\n")
        with open(os.path.join(repo, "docs", "automacao", "AUT-2-matriz.json"), "w",
                  encoding="utf-8") as fh:
            json.dump(matriz, fh)

        builds = [{"mod": "BetterFont", "estado": "OK", "fonte_dll_provada": True,
                   "sha_sandbox": "2c07f5e959af"}]
        suites = [{"id": "suite_puros", "estado": "OK", "testes": [
            {"arquivo": "tools/testes/t_rstv21.py", "estado": "PASSOU"},
            {"arquivo": "tools/testes/contra-prova/cp_rstv21_x.py", "estado": "PROVA_OK"}]}]
        cobertura = bancada_aut3.montar_cobertura(repo, builds, [], suites)
        por_id = {i["id"]: i for i in cobertura["itens"]}
        checar("T-RSTV6 com isca PROVA_OK segue OK_OFFLINE",
               por_id["T-RSTV6"]["estado"] == "OK_OFFLINE", por_id["T-RSTV6"]["estado"])
        checar("M1 build provado -> OK_OFFLINE",
               por_id["M1"]["estado"] == "OK_OFFLINE", por_id["M1"]["estado"])
        checar("criterio runtime -> NAO_EXERCITADO",
               por_id["T-RSTV21"]["estado"] == "NAO_EXERCITADO", por_id["T-RSTV21"]["estado"])
        checar("S-RV-26 runtime -> NAO_EXERCITADO",
               por_id["S-RV-26"]["estado"] == "NAO_EXERCITADO")
        checar("criterio NAO declarado nao vira OK",
               por_id["X-RUNTIME-NAO-DECLARADO"]["estado"] == "NAO_EXERCITADO",
               por_id["X-RUNTIME-NAO-DECLARADO"]["estado"])
        checar("AUT-REUSE -> OK_OFFLINE (reuso provado)",
               por_id["AUT-REUSE"]["estado"] == "OK_OFFLINE", por_id["AUT-REUSE"]["estado"])
        checar("resumo conta NAO_EXERCITADO separado",
               cobertura["resumo"]["NAO_EXERCITADO"] == 3, str(cobertura["resumo"]))

    falhas = [n for n, ok in RESULTADOS if not ok]
    print()
    print("total: %d | falhas: %d" % (len(RESULTADOS), len(falhas)))
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
