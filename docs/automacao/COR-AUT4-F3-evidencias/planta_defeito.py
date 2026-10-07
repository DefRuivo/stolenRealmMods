# -*- coding: utf-8 -*-
"""Planta o defeito da COR-AUT4-F3 (volta ao `is False` cru) numa COPIA fora do repo.
Mostra que, com o defeito, a isca nova PASSA e o runner fica VERMELHO (exit 1).
"""
import io
import os
import shutil
import subprocess
import sys

SCRATCH = r"C:/Users/Pichau/AppData/Local/hermes/cache/scratch/cor-aut4f3"
FIX = os.path.join(SCRATCH, "fix")
DEF = os.path.join(SCRATCH, "defeito")

NOVO = (
    '    declarada_ev = bool(saida.get("evidencia_runtime_presente"))\n'
    '    ev_valor = saida.get("evidencia_runtime")\n'
    '    declara_runtime = (not declarada_ev) or (ev_valor is True)\n'
    '    rotulado_fixture = (declarada == "fixture" or not declara_runtime)\n'
)
DEFEITO = (
    '    ev_valor = saida.get("evidencia_runtime")\n'
    '    rotulado_fixture = (declarada == "fixture" or ev_valor is False)  # DEFEITO PLANTADO\n'
)

if os.path.isdir(DEF):
    shutil.rmtree(DEF)
shutil.copytree(FIX, DEF)

alvo = os.path.join(DEF, "tools", "automacao", "runtime", "coletor.py")
texto = io.open(alvo, encoding="utf-8").read()
assert texto.count(NOVO) == 1, "bloco novo nao encontrado (nao planto em cima de duvida)"
io.open(alvo, "w", encoding="utf-8", newline="\n").write(texto.replace(NOVO, DEFEITO))
print("DEFEITO PLANTADO em:", alvo)
print("  -> `rotulado_fixture = (declarada == 'fixture' or ev_valor is False)` (cru)")

for modo, args in (("suite", []), ("contra-prova", ["--contra-prova"])):
    proc = subprocess.run([sys.executable, "tools/automacao/runtime/roda_testes_runtime.py"] + args,
                          cwd=DEF, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          universal_newlines=True)
    saida = proc.stdout or ""
    print("=" * 74)
    print("[%s] exit=%d" % (modo, proc.returncode))
    for linha in saida.splitlines():
        if ("REPROVOU" in linha or "PROVA FALHOU" in linha or "VEREDITO" in linha
                or "forma-errada" in linha):
            print("   | " + linha.strip())
