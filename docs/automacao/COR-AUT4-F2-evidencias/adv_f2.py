#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Re-mede as sondas adversariais da COR-AUT4R (S1/A1-c, V1/A2, S3/A3, S4/A6)
na arvore indicada. Uso: python adv_f2.py <runtime_dir> <rotulo>
"""
import importlib.util
import json
import os
import sys
import tempfile
import time

RUNTIME = os.path.abspath(sys.argv[1])
ROTULO = sys.argv[2] if len(sys.argv) > 2 else RUNTIME

STUB = r'''
import sys, os, json, hashlib
PERFIL = @PERFIL@; OUT = @OUT@; FLAGS = set(sys.argv[1:])
CFG = os.path.join(PERFIL, "BepInEx", "config", "com.gumatos.aut4probe.cfg")
cfg = {}
for l in open(CFG, encoding="utf-8"):
    if "=" in l:
        k, v = l.split("=", 1); cfg[k.strip()] = v.strip()
os.makedirs(os.path.join(PERFIL, "BepInEx"), exist_ok=True)
open(os.path.join(PERFIL, "BepInEx", "LogOutput.log"), "w", encoding="utf-8").write(
    "Chainloader startup complete\nAUT4 PROBE: tick via BepInEx.Update (quadro 1)\n")
dll = os.path.join(PERFIL, "BepInEx", "plugins", "AUT4Probe", "AUT4Probe.dll")
h = hashlib.sha256(open(dll, "rb").read()).hexdigest()
os.makedirs(OUT, exist_ok=True)
png = os.path.join(OUT, "01-ui.png")
if "--sem-novo-print" not in FLAGS:
    open(png, "wb").write(b"\x89PNG\r\n\x1a\n" + b"0" * 64)
rend = None
if "--rend-vazio" in FLAGS:
    rend = ""
obs = [
 {"objeto": "Tooltip.Title", "caminho": "a/b", "componente": "TextMeshProUGUI",
  "ativo_na_hierarquia": True, "visivel_na_tela": True, "texto_bruto": "M",
  "texto_renderizado": "M", "fonte": "f", "material": "m",
  "shader": "TextMeshPro/Distance Field", "shader_suportado": True, "tamanho_fonte": 24.0,
  "keywords": {"OUTLINE_ON": True}, "cores": {"face": "#FFFFFFFF"},
  "geometria": {"caixa_na_tela_px": {"x": 1, "y": 2, "largura": 3, "altura": 4}, "escala": 1.0, "tela": "1920x1080"},
  "owners": ["com.gumatos.bettertooltips"], "personagem": {"gui_state": "InMainMenu"},
  "nota_texto_renderizado": None}]
if "--inativo" in FLAGS:
    obs.append(
 {"objeto": "Tooltip.Description", "caminho": "a/c", "componente": "TextMeshProUGUI",
  "ativo_na_hierarquia": False, "visivel_na_tela": False, "texto_bruto": "M-DESC",
  "texto_renderizado": rend, "fonte": "f", "material": "m",
  "shader": "TextMeshPro/Distance Field", "shader_suportado": True, "tamanho_fonte": 18.0,
  "keywords": {"OUTLINE_ON": False}, "cores": {"face": "#FFFFFFFF"},
  "geometria": {"caixa_na_tela_px": {"x": 1, "y": 2, "largura": 3, "altura": 4}, "escala": 0.0, "tela": "1920x1080"},
  "owners": ["com.gumatos.bettertooltips"], "personagem": {"gui_state": "InMainMenu"},
  "nota_texto_renderizado": "objeto INATIVO: GetParsedText() sai vazio; vale o texto_bruto."})
probe = {"esquema": "AUT-4/1", "status": "CONCLUIDO", "fase": "concluido",
         "sessao": cfg.get("Sessao") or "SEM-SESSAO", "hash_fonte": h,
         "total_observacoes": 2, "observacoes": obs, "prints": [png.replace("\\", "/")]}
if "--ida-ok" in FLAGS:
    m = cfg.get("MarcadorIdaEVolta") or "X"
    probe["ida_e_volta"] = {"marcador": m, "titulo_lido": m, "conferiu": True}
if "--ida-sem-marcador" in FLAGS:
    probe["ida_e_volta"] = {"titulo_lido": "X", "conferiu": True}
if "--ida-marcador-errado" in FLAGS:
    probe["ida_e_volta"] = {"marcador": "ERRADO", "titulo_lido": "X", "conferiu": True}
json.dump(probe, open(os.path.join(OUT, "aut4probe.json"), "w", encoding="utf-8"), ensure_ascii=False)
'''


def coletor():
    spec = importlib.util.spec_from_file_location("aut4_coletor", os.path.join(RUNTIME, "coletor.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def fixture(nome):
    return json.load(open(os.path.join(RUNTIME, "fixtures", "%s.entrada.json" % nome), encoding="utf-8"))


ALVOS_RENDER = ["objeto", "texto_bruto", "texto_renderizado", "fonte", "material", "shader",
                "keywords", "cores", "geometria", "owners"]


def roda(col, raiz, nome, flags=(), alvos=ALVOS_RENDER, demostrar=False, pre_png=False):
    perfil = os.path.join(raiz, "p-" + nome)
    out = os.path.join(raiz, "o-" + nome)
    stub = os.path.join(raiz, "stub-%s.py" % nome)
    open(stub, "w", encoding="utf-8").write(
        STUB.replace("@PERFIL@", json.dumps(perfil)).replace("@OUT@", json.dumps(out)))
    dll = os.path.join(raiz, "Aut4Probe.dll")
    open(dll, "wb").write(b"MZ-dll-falsa")
    plano = dict(fixture("plano-exemplo"))
    plano["campos_alvo"] = list(alvos)
    if demostrar:
        plano["demostrar_tooltip"] = True
    if pre_png:
        os.makedirs(out, exist_ok=True)
        p = os.path.join(out, "01-ui.png")
        open(p, "wb").write(b"\x89PNG\r\n\x1a\n" + b"5" * 64)
        os.utime(p, (time.time() - 3600.0, time.time() - 3600.0))
    r, cod = col.executar_rodada(plano, perfil_dir=perfil, out_dir=out, dll_probe=dll,
                                 autorizado=True, jogo_disponivel=True, confirmacao="coleta",
                                 comando_lancamento=[sys.executable, stub] + list(flags),
                                 timeout_s=5, poll_s=0.1)
    return r, cod


def main():
    col = coletor()
    print("### %s" % ROTULO)
    with tempfile.TemporaryDirectory(prefix="adv-f2-") as raiz:
        # S1 (A1-c): PNG VELHO no out_dir reusado x out_dir novo
        r, cod = roda(col, raiz, "s1velho", flags=("--sem-novo-print",), pre_png=True)
        ps = (r.get("provas_execucao") or {}).get("prints") or [{}]
        print("S1  PNG VELHO  : status=%s exit=%s prints_ok=%s" % (r["status"], cod, ps[0].get("posterior_ao_lancamento", "n/a")))
        r, cod = roda(col, raiz, "s1novo")
        print("S1c controle   : status=%s exit=%s" % (r["status"], cod))
        # V1 (A2): forma REAL ('') x fixture (None)
        r, cod = roda(col, raiz, "v1vazio", flags=("--inativo", "--rend-vazio"))
        cons = r.get("consolidado") or {}
        print("V1  rend=''    : rodada=%s exit=%s consolidado=%s lacunas=%s"
              % (r["status"], cod, cons.get("status"), cons.get("lacunas")))
        r, cod = roda(col, raiz, "v1null", flags=("--inativo",))
        cons = r.get("consolidado") or {}
        print("V1c rend=None  : rodada=%s exit=%s consolidado=%s lacunas=%s"
              % (r["status"], cod, cons.get("status"), cons.get("lacunas")))
        # V(contêineres vazios)
        ctx = {"sessao": "S", "hash_fonte": "H"}
        base = {k: v for k, v in fixture("probe-saida-exemplo")["observacoes"][0].items()
                if k not in ("sessao", "hash_fonte")}
        for campo, vazio in (("owners", []), ("keywords", {}), ("cores", {})):
            obs = dict(base)
            obs[campo] = vazio
            n = col.normalizar_observacao(col.anexar_contexto([obs], ctx)[0], "runtime",
                                          contexto=ctx, alvos=[campo])
            print("V(%-8s) %-4r : estado=%s lacunas=%s"
                  % (campo, vazio, n["campos"][campo]["estado"], n["lacunas"]))
        # S3 (A3): evidencia_runtime=false sozinho (observacao ATIVA so, todos os alvos lidos)
        fx = fixture("probe-saida-exemplo")
        art = {k: v for k, v in fx.items() if k not in ("procedencia", "rotulo_fixture")}
        art["evidencia_runtime"] = False
        art["observacoes"] = [fx["observacoes"][0]]
        caminho = os.path.join(raiz, "art-a3.json")
        json.dump(art, open(caminho, "w", encoding="utf-8"), ensure_ascii=False)
        res, cod = col.consolidar_probe(caminho, fixture("plano-exemplo"), alvos=ALVOS_RENDER)
        print("S3  ev_runtime=false : status=%s exit=%s evidencia_runtime=%s"
              % (res.get("status"), cod, res.get("evidencia_runtime")))
        # S4 (A6)
        for nome, flag in (("sem masc", "--ida-sem-marcador"), ("com masc", "--ida-ok"),
                           ("masc errado", "--ida-marcador-errado")):
            r, cod = roda(col, raiz, "s4" + flag.replace("-", ""), flags=(flag,), demostrar=True)
            ok = (r.get("provas_execucao") or {}).get("ida_e_volta_ok")
            print("S4  %-11s : status=%s exit=%s ida_e_volta_ok=%s" % (nome, r["status"], cod, ok))


if __name__ == "__main__":
    main()
