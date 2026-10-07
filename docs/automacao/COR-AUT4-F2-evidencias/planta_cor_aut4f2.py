#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PROVA COR-AUT4-F2 — planta CADA defeito numa COPIA fora do repo e mede o runner.

Para cada achado (A1-c/A2/A3/A6) reverte a correcao correspondente em `coletor.py`
(ou no stub da regressao) NA COPIA e mostra a suite e a contra-prova ficando
VERMELHAS (exit 1). Sem o defeito (arvore final) as duas ficam VERDES (exit 0).

Uso:  python planta_cor_aut4f2.py <arvore_final> <scratch>
"""
import json
import os
import shutil
import subprocess
import sys

FINAL = os.path.abspath(sys.argv[1])
SCRATCH = os.path.abspath(sys.argv[2])

COL = os.path.join("tools", "automacao", "runtime", "coletor.py")
STUB = os.path.join("tools", "automacao", "runtime", "testes", "t_aut4_execucao.py")

# (nome, [(arquivo, trecho_correto, trecho_defeito), ...])
DEFEITOS = [
    ("A1c", [(COL,
              "        fresco = bool(existe and mtime is not None and lancamento_epoca is not None\n"
              "                      and mtime + 1e-3 >= lancamento_epoca)\n",
              "        fresco = bool(existe and bytes_ > 0)      # DEFEITO A1c: sem datar\n"),
             (COL,
              "        p[\"existe\"] and p[\"bytes\"] > 0 and p[\"posterior_ao_lancamento\"] for p in ev[\"prints\"])",
              "        p[\"existe\"] and p[\"bytes\"] > 0 for p in ev[\"prints\"])")]),
    ("A2", [(COL,
             "    if valor is None:\n        return \"AUSENTE\"\n    if isinstance(valor, str):\n"
             "        if valor.strip().upper() in AUSENTES or not valor.strip():\n            return \"AUSENTE\"\n"
             "        return \"PRESENTE\"\n    if isinstance(valor, (list, tuple, set, frozenset, dict)) and len(valor) == 0:\n"
             "        return \"AUSENTE\"\n    return \"PRESENTE\"\n",
             "    if valor is None:\n        return \"AUSENTE\"\n"
             "    if isinstance(valor, str) and valor.strip().upper() in AUSENTES:\n        return \"AUSENTE\"\n"
             "    return \"PRESENTE\"\n")]),
    ("A3", [(COL,
             "    rotulado_fixture = (declarada == \"fixture\"\n"
             "                        or saida.get(\"evidencia_runtime\") is False)\n",
             "    rotulado_fixture = (declarada == \"fixture\"\n"
             "                        or (saida.get(\"evidencia_runtime\") is False and bool(rotulo)))  # DEFEITO A3\n")]),
    ("A6", [(COL,
             "                conferiu = (bool(ida_volta.get(\"conferiu\"))\n"
             "                            and str(ida_volta.get(\"marcador\") or \"\") == str(marcador_ida_volta))\n",
             "                conferiu = bool(ida_volta.get(\"conferiu\")) and (\n"
             "                    not ida_volta.get(\"marcador\") or\n"
             "                    str(ida_volta.get(\"marcador\")) == marcador_ida_volta)  # DEFEITO A6\n")]),
]


def rodar(dir_arvore, extra=()):
    proc = subprocess.run([sys.executable,
                           os.path.join("tools", "automacao", "runtime", "roda_testes_runtime.py")] + list(extra),
                          cwd=dir_arvore, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          universal_newlines=True)
    return proc.returncode, proc.stdout or ""


def linhas_relevantes(texto, chaves):
    return [l.strip() for l in texto.splitlines() if any(k in l for k in chaves)]


def main():
    CHAVES = ("A1c", "A2 (F2)", "A2/I", "A3 (F2)", "A6", "A6m", "A2-sec", "alvo vazio",
              "PNG de rodada", "sem o marcador", "evidencia_runtime=false",
              "REPROVOU", "VEREDITO", "PROVA FALHOU")
    saida = []
    for nome, edits in DEFEITOS:
        destino = os.path.join(SCRATCH, "def_" + nome)
        if os.path.isdir(destino):
            shutil.rmtree(destino)
        shutil.copytree(FINAL, destino)
        for rel, bom, ruim in edits:
            caminho = os.path.join(destino, rel)
            texto = open(caminho, encoding="utf-8").read()
            if bom not in texto:
                raise SystemExit("trecho correto NAO encontrado em %s (%s)" % (rel, nome))
            open(caminho, "w", encoding="utf-8").write(texto.replace(bom, ruim, 1))
        # a fixture/stub da regressao segue a forma REAL ("") — o defeito e so o coletor.
        cs, out_s = rodar(destino)
        cp, out_cp = rodar(destino, ["--contra-prova"])
        saida.append("=" * 78)
        saida.append("DEFEITO PLANTADO: %s  ->  suite exit=%s | contra-prova exit=%s"
                     % (nome, cs, cp))
        saida.append("-- suite:")
        for l in linhas_relevantes(out_s, CHAVES):
            saida.append("   " + l)
        saida.append("-- contra-prova:")
        for l in linhas_relevantes(out_cp, CHAVES):
            saida.append("   " + l)
    # sem defeito (arvore final)
    cs, out_s = rodar(FINAL)
    cp, out_cp = rodar(FINAL, ["--contra-prova"])
    saida.append("=" * 78)
    saida.append("SEM DEFEITO (arvore final)  ->  suite exit=%s | contra-prova exit=%s" % (cs, cp))
    saida.append("   suite:     " + " | ".join(linhas_relevantes(out_s, ["VEREDITO"])))
    saida.append("   contra:    " + " | ".join(linhas_relevantes(out_cp, ["VEREDITO"])))
    texto = "\n".join(saida)
    print(texto)
    open(os.path.join(SCRATCH, "planta_cor_aut4f2.log"), "w", encoding="utf-8").write(texto + "\n")


if __name__ == "__main__":
    main()
