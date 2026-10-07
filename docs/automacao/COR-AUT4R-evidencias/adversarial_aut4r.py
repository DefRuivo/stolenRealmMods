#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sondas adversariais da COR-AUT4R — tentam REFUTAR os achados A1/A2/A3/A6 alem do
que as iscas cobrem. Roda 100% sobre a COPIA fora do repo; nada de jogo/perfil.

S1  A1: (c) prints com bytes>0 nao exige que o PNG seja DESTA rodada -> out_dir
         reusado com PNG da rodada anterior satisfaz a prova?  (controle: out_dir novo)
S2  A2: valor MEDIDO vazio ("") conta como PRESENTE (nao-AUSENTE) e satisfaz o alvo?
S3  A3: artefato que se declara `evidencia_runtime: false` SEM rotulo_fixture (e sem
         `procedencia`) ainda consolida como runtime?
S4  A6: `ida_e_volta` com conferiu=true mas SEM o marcador gerado pelo driver
         (o driver so exige o marcador `se` ele vier) -> confirma?
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIMPA = os.path.join(BASE, "trabalho", "base-limpa")
RUNTIME = os.path.join(LIMPA, "tools", "automacao", "runtime")


def coletor():
    spec = importlib.util.spec_from_file_location("aut4_coletor", os.path.join(RUNTIME, "coletor.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def fixture(nome):
    return json.load(open(os.path.join(RUNTIME, "fixtures", "%s.entrada.json" % nome), encoding="utf-8"))


STUB = r'''
import sys, os, json, hashlib
PERFIL = @PERFIL@
OUT = @OUT@
MARKER = @MARKER@
PINTA = @PINTA@          # cria o PNG de verdade?
LISTA = @LISTA@          # lista o PNG em prints?
IDA = @IDA@              # None | "ok" | "sem-marcador"
FLAGS = set(sys.argv[1:])
CFG = os.path.join(PERFIL, "BepInEx", "config", "com.gumatos.aut4probe.cfg")
cfg = {}
try:
    for linha in open(CFG, encoding="utf-8"):
        if "=" in linha:
            k, v = linha.split("=", 1); cfg[k.strip()] = v.strip()
except OSError:
    pass
log_dir = os.path.join(PERFIL, "BepInEx"); os.makedirs(log_dir, exist_ok=True)
open(os.path.join(log_dir, "LogOutput.log"), "w", encoding="utf-8").write(
    "Chainloader startup complete\nAUT4 PROBE: tick via BepInEx.Update (quadro 1)\n")
dll = os.path.join(PERFIL, "BepInEx", "plugins", "AUT4Probe", "AUT4Probe.dll")
h = hashlib.sha256(open(dll, "rb").read()).hexdigest() if os.path.isfile(dll) else ""
os.makedirs(OUT, exist_ok=True)
png = os.path.join(OUT, "01-ui.png")
if PINTA:
    open(png, "wb").write(b"\x89PNG\r\n\x1a\n" + b"0" * 64)
obs = [{
  "objeto": "Tooltip.Title", "caminho": "GUI Manager/Tooltip/Title",
  "componente": "TextMeshProUGUI", "ativo_na_hierarquia": True, "visivel_na_tela": True,
  "texto_bruto": MARKER, "texto_renderizado": MARKER,
  "fonte": "LiberationSans SDF", "material": "m", "shader": "TextMeshPro/Distance Field",
  "shader_suportado": True, "tamanho_fonte": 24.0,
  "keywords": {"OUTLINE_ON": True}, "cores": {"face": "#FFFFFFFF"},
  "geometria": {"caixa_na_tela_px": {"x": 1, "y": 2, "largura": 3, "altura": 4}, "escala": 1.0, "tela": "1920x1080"},
  "owners": ["com.gumatos.bettertooltips"],
  "personagem": {"gui_state": "InMainMenu", "tem_personagem_selecionado": False, "personagem": None},
  "nota_texto_renderizado": None,
}]
probe = {"esquema": "AUT-4/1", "status": "CONCLUIDO", "fase": "concluido",
         "sessao": cfg.get("Sessao") or "SEM-SESSAO", "hash_fonte": h,
         "total_observacoes": 1, "observacoes": obs,
         "prints": ([png.replace("\\", "/")] if LISTA else [])}
if IDA == "ok":
    probe["ida_e_volta"] = {"marcador": cfg.get("MarcadorIdaEVolta") or MARKER,
                            "titulo_lido": cfg.get("MarcadorIdaEVolta") or MARKER, "conferiu": True,
                            "via": "Tooltip.ShowTooltip + releitura"}
elif IDA == "sem-marcador":
    probe["ida_e_volta"] = {"conferiu": True, "via": "declarado, sem o marcador do driver"}
elif IDA == "marcador-errado":
    probe["ida_e_volta"] = {"marcador": "OUTRO-MARCADOR", "titulo_lido": "OUTRO-MARCADOR",
                            "conferiu": True, "via": "declarado com marcador de OUTRA rodada"}
json.dump(probe, open(os.path.join(OUT, "aut4probe.json"), "w", encoding="utf-8"), ensure_ascii=False)
'''


def escreve_stub(dirbase, perfil, out, pinta, lista, ida, marcador="AUT4-MARCADOR"):
    fonte = (STUB.replace("@PERFIL@", json.dumps(perfil)).replace("@OUT@", json.dumps(out))
             .replace("@MARKER@", json.dumps(marcador))
             .replace("@PINTA@", "True" if pinta else "False")
             .replace("@LISTA@", "True" if lista else "False")
             .replace("@IDA@", repr(ida)))
    caminho = os.path.join(dirbase, "stub.py")
    open(caminho, "w", encoding="utf-8").write(fonte)
    return caminho


def rodada(col, plano, raiz, nome, dll, pinta, lista, ida, out_existente=False):
    perfil = os.path.join(raiz, "perfil-" + nome)
    out = os.path.join(raiz, "out-" + nome)
    stub = escreve_stub(raiz, perfil, out, pinta, lista, ida)
    if out_existente:                      # "rodada anterior": out_dir reusado com PNG velho
        os.makedirs(out, exist_ok=True)
        open(os.path.join(out, "01-ui.png"), "wb").write(b"\x89PNG\r\n\x1a\n" + b"V" * 100)
    r, cod = col.executar_rodada(plano, perfil_dir=perfil, out_dir=out, dll_probe=dll,
                                 autorizado=True, jogo_disponivel=True, confirmacao="coleta",
                                 comando_lancamento=[sys.executable, stub], timeout_s=5, poll_s=0.1)
    return r, cod, out


def main():
    col = coletor()
    plano = fixture("plano-exemplo")
    plano["campos_alvo"] = ["objeto", "texto_bruto", "texto_renderizado", "fonte", "material",
                            "shader", "keywords", "cores", "geometria", "owners"]
    with tempfile.TemporaryDirectory(prefix="adversarial-") as raiz:
        dll = os.path.join(raiz, "Aut4Probe.dll")
        open(dll, "wb").write(b"MZ-dll-falsa")

        print("### S1 (A1) — PNG VELHO em out_dir reusado satisfaz a prova (c)?")
        r, cod, out = rodada(col, plano, raiz, "s1-velho", dll, pinta=False, lista=True, ida=None,
                             out_existente=True)
        print("   rodada com PNG VELHO no out_dir : status=%s exit=%s prints=%s"
              % (r["status"], cod, r["provas_execucao"]["prints"]))
        r2, cod2, out2 = rodada(col, plano, raiz, "s1-novo", dll, pinta=False, lista=True, ida=None,
                                out_existente=False)
        print("   CONTROLE out_dir novo (sem PNG) : status=%s exit=%s prints=%s"
              % (r2["status"], cod2, r2["provas_execucao"]["prints"]))

        print("### S2 (A2) — valor MEDIDO vazio ('') satisfaz o alvo?")
        obs = dict(fixture("probe-saida-exemplo")["observacoes"][0])
        obs = {k: v for k, v in obs.items() if k not in ("sessao", "hash_fonte")}
        obs["texto_renderizado"] = ""
        obs["texto_bruto"] = ""
        ctx = {"sessao": "S", "hash_fonte": "H"}
        n = col.normalizar_observacao(col.anexar_contexto([obs], ctx)[0], "runtime", contexto=ctx,
                                      alvos=["texto_bruto", "texto_renderizado"])
        print("   texto_bruto='' -> estado=%s ; texto_renderizado='' -> estado=%s ; lacunas=%s ; ok=%s"
              % (n["campos"]["texto_bruto"]["estado"], n["campos"]["texto_renderizado"]["estado"],
                 n["lacunas"], n["ok"]))
        res, cod = col.consolidar(plano, col.anexar_contexto([obs], ctx), "runtime", contexto=ctx,
                                  alvos=["texto_bruto", "texto_renderizado"])
        print("   consolidador: status=%s exit=%s" % (res["status"], cod))

        print("### S3 (A3) — evidencia_runtime=false SEM rotulo (sem procedencia) ainda vira runtime?")
        fx = fixture("probe-saida-exemplo")
        artefato = dict(fx)
        artefato.pop("procedencia"); artefato.pop("rotulo_fixture")
        artefato["evidencia_runtime"] = False
        # so a observacao ATIVA (todos os alvos lidos) para isolar a procedencia do A2
        artefato["observacoes"] = [dict(o) for o in fx["observacoes"][:1]]
        fd, caminho = tempfile.mkstemp(prefix="adversarial-a3-", suffix=".json"); os.close(fd)
        json.dump(artefato, open(caminho, "w", encoding="utf-8"), ensure_ascii=False)
        res3, cod3 = col.consolidar_probe(caminho, plano, alvos=["objeto", "texto_bruto",
                                                                "texto_renderizado", "fonte",
                                                                "material", "shader", "keywords",
                                                                "cores", "geometria", "owners"])
        print("   artefato declara evidencia_runtime=false -> status=%s exit=%s evidencia_runtime=%s"
              % (res3.get("status"), cod3, res3.get("evidencia_runtime")))

        print("### S4 (A6) — ida_e_volta com conferiu=true SEM o marcador do driver confirma?")
        plano_a6 = dict(plano); plano_a6["demostrar_tooltip"] = True
        r4, cod4, _ = rodada(col, plano_a6, raiz, "s4-sem-marcador", dll, pinta=True, lista=True,
                             ida="sem-marcador")
        print("   sem marcador : status=%s exit=%s ida_e_volta_ok=%s"
              % (r4["status"], cod4, r4["provas_execucao"].get("ida_e_volta_ok")))
        r5, cod5, _ = rodada(col, plano_a6, raiz, "s4-com-marcador", dll, pinta=True, lista=True,
                             ida="ok")
        print("   com marcador : status=%s exit=%s ida_e_volta_ok=%s  (controle positivo)"
              % (r5["status"], cod5, r5["provas_execucao"].get("ida_e_volta_ok")))
        r6, cod6, _ = rodada(col, plano_a6, raiz, "s4-marcador-errado", dll, pinta=True, lista=True,
                             ida="marcador-errado")
        print("   marcador ERRADO : status=%s exit=%s ida_e_volta_ok=%s  (controle: deve reprovar)"
              % (r6["status"], cod6, r6["provas_execucao"].get("ida_e_volta_ok")))


if __name__ == "__main__":
    main()
