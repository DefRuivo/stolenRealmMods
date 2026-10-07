# -*- coding: utf-8 -*-
"""Sonda adversarial COR-AUT4-F2R: (1) "" em TODAS as superficies; (2) burla por artefato vazio/forjado."""
import importlib.util
import json
import os
import sys
import tempfile

BASE = r"C:/Users/Pichau/AppData/Local/hermes/cache/scratch/cor-aut4f2r/base"
RUNTIME = os.path.join(BASE, "tools", "automacao", "runtime")
FIX = os.path.join(RUNTIME, "fixtures")


def mod(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


col = mod("aut4_coletor", os.path.join(RUNTIME, "coletor.py"))
fx = json.load(open(os.path.join(FIX, "probe-saida-exemplo.entrada.json"), encoding="utf-8"))
plano = json.load(open(os.path.join(FIX, "plano-exemplo.entrada.json"), encoding="utf-8"))
ALVOS = list(col.CAMPOS)
ctx = {"sessao": fx["sessao"], "hash_fonte": fx["hash_fonte"]}
obs_ativa = {k: v for k, v in fx["observacoes"][0].items() if k not in ("sessao", "hash_fonte")}


def tmp_art(dados):
    fd, p = tempfile.mkstemp(prefix="adv-", suffix=".json")
    os.close(fd)
    with open(p, "w", encoding="utf-8") as fh:
        json.dump(dados, fh, ensure_ascii=False)
    return p


print("=" * 78)
print("BLOCO 1 - _estado_do_campo: VAZIO = NAO LIDO em todas as formas")
print("=" * 78)
for v in ["", "   ", "\t", "\n", [], {}, (), set(), frozenset()]:
    print("  valor=%-14r -> %s" % (v, col._estado_do_campo(v)))
print("  CONTROLE valor='x'   -> %s" % col._estado_do_campo("x"))
print("  CONTROLE valor=[1]   -> %s" % col._estado_do_campo([1]))
print("  CONTROLE valor={'a':1}-> %s" % col._estado_do_campo({"a": 1}))

print()
print("=" * 78)
print("BLOCO 2 - normalizar_observacao: cada campo-alvo VAZIO vira LACUNA")
print("=" * 78)
for campo, vazio in (("texto_renderizado", ""), ("texto_bruto", "  "), ("owners", []),
                     ("keywords", {}), ("cores", {}), ("fonte", ""), ("material", ""),
                     ("shader", ""), ("objeto", ""), ("caminho", ""), ("geometria", {})):
    o = dict(obs_ativa)
    o[campo] = vazio
    if campo == "texto_renderizado":
        o["nota_texto_renderizado"] = None  # objeto ATIVO: sem fallback
    n = col.normalizar_observacao(o, "runtime", contexto=ctx, alvos=[campo])
    print("  alvo=%-18s valor=%-6r -> lacuna=%-5s ok=%s"
          % (campo, vazio, campo in n["lacunas"], n["ok"]))

print()
print("  objeto INATIVO com texto_renderizado='' E texto_bruto='' (sem fallback possivel):")
o = dict(obs_ativa)
o["ativo_na_hierarquia"] = False
o["texto_renderizado"] = ""
o["texto_bruto"] = ""
n = col.normalizar_observacao(o, "runtime", contexto=ctx, alvos=["texto_renderizado"])
print("     estado=%s lacuna=%s (NAO pode virar NAO_APLICAVEL)"
      % (n["campos"]["texto_renderizado"]["estado"], "texto_renderizado" in n["lacunas"]))

print()
print("=" * 78)
print("BLOCO 3 - artefato VAZIO/FORJADO nao confirma (caminho consolidar_probe)")
print("=" * 78)


def probe(dados, rotulo, alvos=ALVOS):
    res, cod = col.consolidar_probe(tmp_art(dados), plano, alvos=alvos)
    st = res.get("status") if isinstance(res, dict) else res
    evr = res.get("evidencia_runtime") if isinstance(res, dict) else None
    print("  %-46s -> status=%-12s exit=%s evid_runtime=%s" % (rotulo, st, cod, evr))
    return st, cod


base_rt = {"esquema": "AUT-4/1", "procedencia": "runtime", "evidencia_runtime": True,
           "status": "CONCLUIDO", "fase": "concluido", "sessao": fx["sessao"],
           "hash_fonte": fx["hash_fonte"]}

# (a) artefato vazio: nenhuma observacao, mas declara runtime+CONCLUIDO
vazio = dict(base_rt, observacoes=[])
probe(vazio, "(a) observacoes=[] (vazio) + runtime + CONCLUIDO")

# (b) uma observacao com TODOS os alvos vazios
obs_tudo_vazio = {c: ("", ) and "" for c in ALVOS}
obs_tudo_vazio.update({"ativo_na_hierarquia": True, "nota_texto_renderizado": None})
for c in ("objeto", "texto_bruto", "fonte", "material", "shader", "texto_renderizado"):
    obs_tudo_vazio[c] = ""
for c in ("keywords", "cores", "geometria"):
    obs_tudo_vazio[c] = {}
obs_tudo_vazio["owners"] = []
probe(dict(base_rt, observacoes=[obs_tudo_vazio]), "(b) 1 obs com TODOS os alvos vazios")

# (c) observacao declara status OK com campo vazio (deve RECUSAR)
obs_ok_vazio = dict(obs_ativa, texto_renderizado="", status="OK")
try:
    n = col.normalizar_observacao(obs_ok_vazio, "runtime", contexto=ctx, alvos=["texto_renderizado"])
    print("  (c) obs com status=OK e rendered vazio  -> ACEITOU (FALHA): status=%s" % n)
except col.ObservacaoInvalida as e:
    print("  (c) obs com status=OK e rendered vazio  -> RECUSOU ObservacaoInvalida")

# (d) artefato sem sessao/hash (nao identifica a build) -> deve recusar, nao confirmar
sem_id = {"esquema": "AUT-4/1", "procedencia": "runtime", "evidencia_runtime": True,
          "status": "CONCLUIDO", "fase": "concluido", "observacoes": [obs_ativa]}
try:
    res, cod = col.consolidar_probe(tmp_art(sem_id), plano, alvos=ALVOS)
    print("  (d) runtime SEM sessao/hash -> status=%s exit=%s (nao pode confirmar)"
          % (res.get("status"), cod))
except col.ObservacaoInvalida as e:
    print("  (d) runtime SEM sessao/hash -> RECUSOU ObservacaoInvalida")

# CONTROLE POSITIVO: obs ativa com todos os campos lidos -> CONFIRMADA/0
ok_obs = dict(obs_ativa)
probe(dict(base_rt, observacoes=[ok_obs]), "(+) CONTROLE obs ativa completa (runtime)", alvos=None)

print()
print("=" * 78)
print("BLOCO 4 - A3: evidencia_runtime=false NUNCA vira CONFIRMADA")
print("=" * 78)
fx_falso = {k: v for k, v in fx.items() if k not in ("procedencia", "rotulo_fixture")}
fx_falso["evidencia_runtime"] = False
probe(fx_falso, "evidencia_runtime=False (bool) sozinho", alvos=list(col.CAMPOS))
print("  (inversao) res.evidencia_runtime acima tem de ser False, nunca True")

# caller FORCA procedencia=runtime
res, cod = col.consolidar_probe(tmp_art(fx_falso), plano, alvos=list(col.CAMPOS),
                                procedencia="runtime")
print("  caller forca procedencia=runtime        -> status=%s exit=%s evid_runtime=%s"
      % (res.get("status"), cod, res.get("evidencia_runtime")))

# BORDA: evidencia_runtime como STRING "false" ou 0 (nao e o bool do probe)
for v in ["false", 0, "no"]:
    art = {k: val for k, val in fx.items()}
    art["procedencia"] = "runtime"
    art["evidencia_runtime"] = v
    art["status"] = "CONCLUIDO"
    try:
        res, cod = col.consolidar_probe(tmp_art(art), plano, alvos=list(col.CAMPOS))
        print("  BORDA evidencia_runtime=%-8r -> status=%s exit=%s evid_runtime=%s"
              % (v, res.get("status"), cod, res.get("evidencia_runtime")))
    except col.ObservacaoInvalida as e:
        print("  BORDA evidencia_runtime=%-8r -> RECUSOU" % (v,))
print("=" * 78)
