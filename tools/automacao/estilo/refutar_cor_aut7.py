#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""refutar_cor-aut7.py - COR-AUT7: refutacao INDEPENDENTE das correcoes (execucao 387).

Reusa as MESMAS variantes sinteticas do revisor AUT-7R (t_c718923e, execucao 381) e as
roda contra a correcao, pelas CLIs REAIS (produtor -> consolidador). Nenhum dado aqui e
runtime: as entradas sao sinteticas e rotuladas. Sem jogo/build/deploy/save/publicacao.
"""
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

W = os.path.dirname(os.path.abspath(__file__))


def _raiz_do_repo():
    """Raiz do repo (a que tem `BetterFont/`), subindo do lugar deste script."""
    d = W
    for _ in range(6):
        if os.path.isdir(os.path.join(d, "BetterFont")):
            return d
        d = os.path.dirname(d)
    return os.path.join(W, "repo")


S = os.environ.get("COR_S") or _raiz_do_repo()
OUT = os.environ.get("COR_OUT") or os.path.join(S, "docs", "automacao", "COR-AUT7-evidencias")
os.makedirs(OUT, exist_ok=True)
TMP = tempfile.mkdtemp(prefix="cor-aut7-")
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TEMP=TMP, TMP=TMP, TMPDIR=TMP,
           PYTHONIOENCODING="utf-8")
sys.path.insert(0, os.path.join(S, "tools"))
sys.path.insert(0, os.path.join(S, "tools", "automacao"))


def sha(caminho):
    h = hashlib.sha256()
    with io.open(caminho, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def roda(nome, argv, timeout=1800):
    p = subprocess.run([sys.executable] + list(argv), cwd=S, env=ENV,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    with io.open(os.path.join(OUT, nome + ".stdout"), "wb") as fh:
        fh.write(p.stdout)
    with io.open(os.path.join(OUT, nome + ".stderr"), "wb") as fh:
        fh.write(p.stderr)
    print("  %-34s exit=%s" % (nome, p.returncode))
    return p


import importlib.util


def carrega(nome, rel):
    spec = importlib.util.spec_from_file_location(nome, os.path.join(S, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


ea = carrega("cor_estilo", os.path.join("tools", "automacao", "estilo", "estilo_atributos.py"))
ra = carrega("cor_aceite", os.path.join("tools", "automacao", "aceite", "relatorio_aceite.py"))

IDENT = dict(ea.identidade_do_repo(S)[0])
IDENT["sessao"] = "cor-aut7-sintetica-sem-runtime"
IDENT["dll_sha"] = ("d" * 64)
ident_path = os.path.join(OUT, "identidade.json")
with io.open(ident_path, "w", encoding="utf-8") as fh:
    fh.write(json.dumps(IDENT, indent=2))
MARCADOR = os.path.join(OUT, "marcador-sintetico.txt")
with io.open(MARCADOR, "w", encoding="utf-8") as fh:
    fh.write("CONTROLE SINTETICO - NAO E EVIDENCIA DE RUNTIME\n")


def obs(**kw):
    base = {"procedencia": "runtime", "sessao": IDENT["sessao"], "fonte_sha": IDENT["fonte_sha"],
            "dll_sha": IDENT["dll_sha"], "evidencia": MARCADOR}
    base.update(kw)
    return base


# As MESMAS oito variantes insuficientes do revisor (rotuladas sinteticas).
VARIANTES = {
    "BF-only-fonts-no-material": (
        [obs(objeto="Tooltip.Title", fonte="new", mod_ativo=True),
         obs(objeto="Tooltip.Title", fonte="old", mod_ativo=False)],
        "runtime-preservacao-estilo"),
    "BF-unvalidated-control-fixture": (
        [obs(objeto="Tooltip.Title", fonte="new", mod_ativo=True),
         {"objeto": "Tooltip.Title", "fonte": "old", "mod_ativo": False, "procedencia": "fixture"}],
        "runtime-preservacao-estilo"),
    "BF-config-arbitrary-hash-no-keys": (
        [obs(config_sha="arbitrary-not-a-config-hash")], "runtime-config"),
    "BCT-only-one-surface-no-colors": (
        [obs(objeto="BossHealthbar_Text", keywords={"OUTLINE_ON": True})],
        "runtime-superficies-contraste"),
    "BCT-duplicate-same-reading": (
        [obs(objeto="BossHealthbar_Text", keywords={"OUTLINE_ON": True})] * 2, "runtime-idempotencia"),
    "BCT-levelup-no-fields": (
        [obs(objeto="unrelated-menu-text", nao_deve_exibir_efeito=True)],
        "runtime-sem-vazamento-levelup"),
    "Debugger-empty-log": (
        [obs(log=True, boot_novo=True)], "runtime-contrato-dump"),
    "Debugger-real-delimiters": (
        [obs(log=True, boot_novo=True,
             log_texto='[Info   :Roguelike Debugger] [Status] \'Buff\' | tipo=Buff | '
                       'desc="Description"')], "runtime-contrato-dump"),
}

res = {"execucao": "387 (correcao)", "variantes": {}, "suites": {}, "cache": {}, "runtime": "NAO EXERCITADO"}
print("== variantes do revisor contra a correcao (CLI produtor -> consolidador)")
for nome, (observacoes, sufixo) in VARIANTES.items():
    inp = os.path.join(OUT, nome + ".input.json")
    with io.open(inp, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(observacoes, indent=2))
    p1 = roda("cli-" + nome, ["tools/automacao/estilo/estilo_atributos.py", "--repo", S,
                              "--out-dir", OUT, "--sem-suite", "--identidade", ident_path,
                              "--observacoes", inp, "--out", os.path.join(OUT, nome + ".estilo.json")])
    p2 = roda("cons-" + nome, ["tools/automacao/aceite/relatorio_aceite.py", "--repo", S,
                               "--out-dir", OUT, "--sem-suite", "--identidade", ident_path,
                               "--estilo-observacoes", inp, "--out", os.path.join(OUT, nome + ".aceite.json")])
    with io.open(os.path.join(OUT, nome + ".estilo.json"), encoding="utf-8") as fh:
        est = json.load(fh)
    alvo = [c for c in est["criterios"] if c["id"].endswith(sufixo)][0]
    with io.open(os.path.join(OUT, nome + ".aceite.json"), encoding="utf-8") as fh:
        ace = json.load(fh)
    todos = [c for b in ace["decisao"]["por_mod"].values() for c in b["criterios"]]
    dc = [c for c in todos if c["id"] == alvo["id"]][0]
    vinc = alvo["id"] in [c["id"] for b in ace["decisao"]["por_mod"].values()
                          for c in b["ok_vinculantes"]]
    res["variantes"][nome] = {"estado_estilo": alvo["estado"], "classificacao_consolidador":
                              dc["classificacao"], "ok_vinculante": vinc,
                              "exit_estilo": p1.returncode, "exit_consolidador": p2.returncode,
                              "sintetico": True,
                              "esperado": "NOT_REPROVADO" if nome == "Debugger-real-delimiters" else "NOT_OK"}
    print("    %-32s estilo=%s consolidador=%s vinculante=%s"
          % (nome, alvo["estado"], dc["classificacao"], vinc))

print("== suites internas da entrega")
for nome, argv in (("suite-estilo", ["tools/automacao/estilo/test_estilo_atributos.py"]),
                   ("suite-aceite", ["tools/automacao/aceite/test_relatorio_aceite.py"])):
    p = roda(nome, argv)
    texto = p.stdout.decode("utf-8", "replace")
    res["suites"][nome] = {"exit": p.returncode, "total": texto.strip().splitlines()[-2]
                           if p.returncode == 0 else texto.strip().splitlines()[-1]}

print("== cache --sem-suite: mutacao de FONTE tem de invalidar")
p = roda("cache-suite-cheia", ["tools/automacao/estilo/estilo_atributos.py", "--repo", S,
                               "--out-dir", OUT, "--identidade", ident_path,
                               "--out", os.path.join(OUT, "cheia.json")])
with io.open(os.path.join(OUT, "cheia.json"), encoding="utf-8") as fh:
    cheia = json.load(fh)
res["cache"]["ok_com_suite_real"] = {m: [c["id"] for c in cheia["criterios"]
                                         if c["mod"] == m and c["estado"] == "OK"]
                                     for m in ("BetterFont", "BetterCombatText", "RoguelikeDebugger")}
fonte = os.path.join(S, "BetterFont", "Plugin.cs")
orig = io.open(fonte, "rb").read()
h_orig = sha(fonte)
try:
    with io.open(fonte, "wb") as fh:
        fh.write(b"// fonte DELIBERADAMENTE invalida: o cache NAO pode reusar prova\n")
    p2 = roda("cache-suite-mutada", ["tools/automacao/estilo/estilo_atributos.py", "--repo", S,
                                     "--out-dir", OUT, "--sem-suite", "--identidade", ident_path,
                                     "--out", os.path.join(OUT, "mutada.json")])
    with io.open(os.path.join(OUT, "mutada.json"), encoding="utf-8") as fh:
        mutada = json.load(fh)
    res["cache"]["cache_valido_apos_mutacao"] = mutada["medicao"].get("cache_valido")
    res["cache"]["melhorfont_ok_apos_mutacao"] = [c["id"] for c in mutada["criterios"]
                                                  if c["mod"] == "BetterFont" and c["estado"] == "OK"]
    res["cache"]["exit_apos_mutacao"] = p2.returncode
    p3 = roda("cache-mutada-consolidador", ["tools/automacao/aceite/relatorio_aceite.py", "--repo", S,
                                            "--out-dir", OUT, "--sem-suite", "--identidade", ident_path,
                                            "--out", os.path.join(OUT, "mutada.aceite.json")])
    with io.open(os.path.join(OUT, "mutada.aceite.json"), encoding="utf-8") as fh:
        mace = json.load(fh)
    res["cache"]["ok_vinculante_apos_mutacao"] = [c["id"] for c in
                                                  mace["decisao"]["por_mod"]["BetterFont"]["ok_vinculantes"]]
finally:
    with io.open(fonte, "wb") as fh:
        fh.write(orig)
res["cache"]["fonte_restaurada_byte_a_byte"] = sha(fonte) == h_orig
print("  cache: antes=%s | mutado valido=%s BetterFont_OK=%s | vinculante=%s | restaurado=%s"
      % (res["cache"]["ok_com_suite_real"], res["cache"]["cache_valido_apos_mutacao"],
         len(res["cache"]["melhorfont_ok_apos_mutacao"]) if "melhorfont_ok_apos_mutacao" in res["cache"]
         else "?", res["cache"].get("ok_vinculante_apos_mutacao"),
         res["cache"]["fonte_restaurada_byte_a_byte"]))

print("== frentes AUT-5/6: resultado vazio/malformado -> lacuna (nunca frente=0)")
vazio = os.path.join(OUT, "frente-vazia.json")
with io.open(vazio, "w", encoding="utf-8") as fh:
    fh.write(json.dumps({"criterios": []}))
p = roda("frente-vazia", ["tools/automacao/aceite/relatorio_aceite.py", "--repo", S, "--out-dir", OUT,
                          "--sem-suite", "--identidade", ident_path, "--rstv-criterios", vazio,
                          "--shrines-criterios", vazio, "--out", os.path.join(OUT, "frente-vazia.json.out")])
with io.open(os.path.join(OUT, "frente-vazia.json.out"), encoding="utf-8") as fh:
    fv = json.load(fh)
res["frentes_vazias"] = {"por_frente": fv["por_frente"], "exit": p.returncode,
                         "lacunas_canonicas": [c["id"] for b in fv["decisao"]["por_mod"].values()
                                               for c in b.get("criterios", [])
                                               if str(c.get("id", "")).endswith("resultado-vazio")]}
print("  por_frente=%s lacunas=%s" % (res["frentes_vazias"]["por_frente"],
                                      res["frentes_vazias"]["lacunas_canonicas"]))

print("== dump real do produto reconhecido (linha do fonte vivo, nao fixture inventada)")
linhas = []
for rel in ("RoguelikeDebugger/Patches/SkillInventoryPatch.cs",
            "RoguelikeDebugger/Patches/ActionStatusInventoryPatch.cs"):
    with io.open(os.path.join(S, rel), encoding="utf-8") as fh:
        for i, l in enumerate(fh.read().splitlines(), 1):
            if "desc=" in l or " | " in l:
                linhas.append({"arquivo": rel, "linha": i, "texto": l.strip()[:200]})
res["dump_do_produto"] = linhas[:12]
print("  linhas de contrato do produto: %d" % len(linhas))

res["hashes"] = {rel: sha(os.path.join(S, rel)) for rel in (
    "tools/automacao/estilo/estilo_atributos.py",
    "tools/automacao/estilo/test_estilo_atributos.py",
    "tools/automacao/aceite/relatorio_aceite.py",
    "tools/automacao/aceite/test_relatorio_aceite.py")}
with io.open(os.path.join(OUT, "refutacao-cor-aut7.json"), "w", encoding="utf-8") as fh:
    fh.write(json.dumps(res, indent=2, ensure_ascii=False, default=str))
print("\nfalsos OK remanescentes: %s"
      % [n for n, v in res["variantes"].items()
         if (v["ok_vinculante"] or v["estado_estilo"] == "OK") and n != "Debugger-real-delimiters"])
print("falso reprovado no contrato real: %s"
      % (res["variantes"]["Debugger-real-delimiters"]["estado_estilo"] == "REPROVADO"))
print("relatorio:", os.path.join(OUT, "refutacao-cor-aut7.json"))
