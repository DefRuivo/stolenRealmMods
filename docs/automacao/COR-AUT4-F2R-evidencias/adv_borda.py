# -*- coding: utf-8 -*-
"""Borda A3: evidencia_runtime como STRING/0 (nao o bool do probe) + ausencia do campo."""
import importlib.util
import json
import os
import tempfile

BASE = r"C:/Users/Pichau/AppData/Local/hermes/cache/scratch/cor-aut4f2r/base"
RUNTIME = os.path.join(BASE, "tools", "automacao", "runtime")
FIX = os.path.join(RUNTIME, "fixtures")
spec = importlib.util.spec_from_file_location("aut4_coletor", os.path.join(RUNTIME, "coletor.py"))
col = importlib.util.module_from_spec(spec)
spec.loader.exec_module(col)
fx = json.load(open(os.path.join(FIX, "probe-saida-exemplo.entrada.json"), encoding="utf-8"))
plano = json.load(open(os.path.join(FIX, "plano-exemplo.entrada.json"), encoding="utf-8"))
obs_ativa = {k: v for k, v in fx["observacoes"][0].items() if k not in ("sessao", "hash_fonte")}


def tmp(d):
    fd, p = tempfile.mkstemp(prefix="borda-", suffix=".json"); os.close(fd)
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False)
    return p


def roda(art, rot):
    res, cod = col.consolidar_probe(tmp(art), plano, alvos=list(col.CAMPOS))
    print("  %-52s -> status=%-11s exit=%s evid=%s"
          % (rot, res.get("status"), cod, res.get("evidencia_runtime")))


# artefato com TODOS os alvos lidos (so a obs ativa) e SEM procedencia
comum = {"esquema": "AUT-4/1", "status": "CONCLUIDO", "fase": "concluido",
         "sessao": fx["sessao"], "hash_fonte": fx["hash_fonte"], "observacoes": [obs_ativa]}
for v in [False, "false", 0, None]:
    a = dict(comum); a["evidencia_runtime"] = v
    roda(a, "evidencia_runtime=%-7r (todos os alvos lidos)" % (v,))
a = dict(comum)  # sem a chave
roda(a, "SEM a chave evidencia_runtime (todos alvos lidos)")
a = dict(comum); a["evidencia_runtime"] = True; a["procedencia"] = "runtime"
roda(a, "evidencia_runtime=True (controle positivo)")
