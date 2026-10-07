# -*- coding: utf-8 -*-
"""Borda COR-AUT4-F3: a FORMA de `evidencia_runtime` decide runtime x recusa.

Roda contra o `coletor.py` de um diretorio runtime passado em argv[1]
(default: o repo atual). Mostra a tabela PRESENTE/AUSENTE x status/exit.

Uso: python adv_borda.py <.../tools/automacao/runtime>
"""
import importlib.util
import json
import os
import sys
import tempfile

RUNTIME = sys.argv[1] if len(sys.argv) > 1 else r"C:/dev/stolen-realm/tools/automacao/runtime"
FIX = os.path.join(RUNTIME, "fixtures")
spec = importlib.util.spec_from_file_location("aut4_coletor", os.path.join(RUNTIME, "coletor.py"))
col = importlib.util.module_from_spec(spec)
spec.loader.exec_module(col)
fx = json.load(open(os.path.join(FIX, "probe-saida-exemplo.entrada.json"), encoding="utf-8"))
plano = json.load(open(os.path.join(FIX, "plano-exemplo.entrada.json"), encoding="utf-8"))
obs_ativa = {k: v for k, v in fx["observacoes"][0].items() if k not in ("sessao", "hash_fonte")}


def tmp(d):
    fd, p = tempfile.mkstemp(prefix="borda-", suffix=".json")
    os.close(fd)
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False)
    return p


def roda(art, rot, alvos=None):
    res, cod = col.consolidar_probe(tmp(art), plano, alvos=alvos or list(col.CAMPOS))
    print("  %-56s -> status=%-11s exit=%s evid=%s"
          % (rot, res.get("status"), cod, res.get("evidencia_runtime")))


comum = {"esquema": "AUT-4/1", "status": "CONCLUIDO", "fase": "concluido",
         "sessao": fx["sessao"], "hash_fonte": fx["hash_fonte"], "observacoes": [obs_ativa]}
print("RUNTIME =", RUNTIME)
for v in [False, "false", 0, "0", None, True, "true", 1, "False"]:
    a = dict(comum)
    a["evidencia_runtime"] = v
    roda(a, "PRESENTE evidencia_runtime=%-8r" % (v,))
roda(dict(comum), "AUSENTE a chave (caminho do probe C# real)")
a = dict(comum)
a["evidencia_runtime"] = False
a["procedencia"] = "runtime"
roda(a, "PRESENTE False + chamador procedencia=runtime")
