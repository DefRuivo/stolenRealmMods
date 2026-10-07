#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ACHADO candidato da COR-AUT4R — campo MEDIDO VAZIO ("", [], {}) conta como LIDO.

A prova de que isso nao e hipotese sai do proprio jogo:
  ilspycmd -t TMPro.TMP_Text lib/Unity.TextMeshPro.dll
      public virtual string GetParsedText() {
          if (m_textInfo == null) { return string.Empty; }   // "" — nunca null
          ... return new string(array);                      // "" quando characterCount == 0
      }
O probe AUT-4 faz `Trunc(Seguro(() => t.GetParsedText()) as string, 600)` e
`Trunc` so devolve null para ENTRADA null. Logo o artefato REAL traz
`texto_renderizado: ""` para o objeto sem mesh gerado — enquanto a FIXTURE
(`probe-saida-exemplo.entrada.json`) traz `null` para o mesmo caso. O coletor
(`_estado_do_campo`) le "" como PRESENTE, entao o alvo `texto_renderizado` passa
a LIDO e a lacuna do A2 desaparece.

V1  caminho completo (executar_rodada) com a forma REAL do artefato.
V1c CONTROLE: mesma rodada com `null` (a forma da fixture) -> tem de dar INCOMPLETO.
V2  `owners: []` (lista vazia) com alvo `owners`.
V3  `keywords: {}` (dicionario vazio) com alvo `keywords`.
"""
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUNTIME = os.path.join(BASE, "trabalho", "base-limpa", "tools", "automacao", "runtime")


def coletor():
    spec = importlib.util.spec_from_file_location("aut4_coletor", os.path.join(RUNTIME, "coletor.py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def fixture(nome):
    return json.load(open(os.path.join(RUNTIME, "fixtures", "%s.entrada.json" % nome), encoding="utf-8"))


STUB = r'''
import sys, os, json, hashlib
PERFIL = @PERFIL@; OUT = @OUT@; VAZIO = @VAZIO@
CFG = os.path.join(PERFIL, "BepInEx", "config", "com.gumatos.aut4probe.cfg")
cfg = {}
for linha in open(CFG, encoding="utf-8"):
    if "=" in linha:
        k, v = linha.split("=", 1); cfg[k.strip()] = v.strip()
os.makedirs(os.path.join(PERFIL, "BepInEx"), exist_ok=True)
open(os.path.join(PERFIL, "BepInEx", "LogOutput.log"), "w", encoding="utf-8").write(
    "Chainloader startup complete\nAUT4 PROBE: tick via BepInEx.Update (quadro 1)\n")
dll = os.path.join(PERFIL, "BepInEx", "plugins", "AUT4Probe", "AUT4Probe.dll")
h = hashlib.sha256(open(dll, "rb").read()).hexdigest()
os.makedirs(OUT, exist_ok=True)
png = os.path.join(OUT, "01-ui.png")
open(png, "wb").write(b"\x89PNG\r\n\x1a\n" + b"0" * 64)
# objeto ATIVO com tudo lido + objeto INATIVO exatamente como o probe C# emite hoje:
# GetParsedText() -> string.Empty (""), nao null.
REND = "" if VAZIO else None
obs = [
  {"objeto": "Tooltip.Title", "caminho": "a/b", "componente": "TextMeshProUGUI",
   "ativo_na_hierarquia": True, "visivel_na_tela": True, "texto_bruto": "M",
   "texto_renderizado": "M", "fonte": "f", "material": "m",
   "shader": "TextMeshPro/Distance Field", "shader_suportado": True, "tamanho_fonte": 24.0,
   "keywords": {"OUTLINE_ON": True}, "cores": {"face": "#FFFFFFFF"},
   "geometria": {"caixa_na_tela_px": {"x": 1, "y": 2, "largura": 3, "altura": 4}, "escala": 1.0, "tela": "1920x1080"},
   "owners": [], "personagem": {"gui_state": "InMainMenu"}, "nota_texto_renderizado": None},
  {"objeto": "Tooltip.Description", "caminho": "a/c", "componente": "TextMeshProUGUI",
   "ativo_na_hierarquia": False, "visivel_na_tela": False, "texto_bruto": "M-DESC",
   "texto_renderizado": REND, "fonte": "f", "material": "m",
   "shader": "TextMeshPro/Distance Field", "shader_suportado": True, "tamanho_fonte": 18.0,
   "keywords": {}, "cores": {"face": "#FFFFFFFF"},
   "geometria": {"caixa_na_tela_px": {"x": 1, "y": 2, "largura": 3, "altura": 4}, "escala": 0.0, "tela": "1920x1080"},
   "owners": [], "personagem": {"gui_state": "InMainMenu"},
   "nota_texto_renderizado": "objeto INATIVO: GetParsedText() sai vazio ate o TMP gerar o mesh; vale o texto_bruto."},
]
json.dump({"esquema": "AUT-4/1", "status": "CONCLUIDO", "fase": "concluido",
           "sessao": cfg.get("Sessao") or "SEM-SESSAO", "hash_fonte": h,
           "total_observacoes": 2, "observacoes": obs,
           "prints": [png.replace("\\", "/")]},
          open(os.path.join(OUT, "aut4probe.json"), "w", encoding="utf-8"), ensure_ascii=False)
'''


def roda(col, raiz, nome, vazio, alvos):
    perfil, out = os.path.join(raiz, "p-" + nome), os.path.join(raiz, "o-" + nome)
    stub = os.path.join(raiz, "stub-%s.py" % nome)
    open(stub, "w", encoding="utf-8").write(STUB.replace("@PERFIL@", json.dumps(perfil))
                                            .replace("@OUT@", json.dumps(out))
                                            .replace("@VAZIO@", "True" if vazio else "False"))
    dll = os.path.join(raiz, "Aut4Probe.dll")
    open(dll, "wb").write(b"MZ-dll-falsa")
    plano = fixture("plano-exemplo"); plano["campos_alvo"] = alvos
    r, cod = col.executar_rodada(plano, perfil_dir=perfil, out_dir=out, dll_probe=dll,
                                 autorizado=True, jogo_disponivel=True, confirmacao="coleta",
                                 comando_lancamento=[sys.executable, stub], timeout_s=5, poll_s=0.1)
    return r, cod


def main():
    col = coletor()
    ALVOS = ["objeto", "texto_bruto", "texto_renderizado", "fonte", "material", "shader",
             "keywords", "cores", "geometria", "owners"]
    with tempfile.TemporaryDirectory(prefix="vazio-") as raiz:
        r, cod = roda(col, raiz, "v1-vazio", True, ALVOS)
        cons = r.get("consolidado") or {}
        print("V1   artefato REAL (texto_renderizado='') : rodada=%s exit=%s consolidado=%s lacunas=%s"
              % (r["status"], cod, cons.get("status"), cons.get("lacunas")))
        r2, cod2 = roda(col, raiz, "v1-null", False, ALVOS)
        cons2 = r2.get("consolidado") or {}
        print("V1c  CONTROLE (texto_renderizado=null, forma da fixture): rodada=%s exit=%s consolidado=%s lacunas=%s"
              % (r2["status"], cod2, cons2.get("status"), cons2.get("lacunas")))

        ctx = {"sessao": "S", "hash_fonte": "H"}
        for campo, valor in (("owners", []), ("keywords", {}), ("cores", {})):
            obs = dict(fixture("probe-saida-exemplo")["observacoes"][0])
            obs = {k: v for k, v in obs.items() if k not in ("sessao", "hash_fonte")}
            obs[campo] = valor
            n = col.normalizar_observacao(col.anexar_contexto([obs], ctx)[0], "runtime",
                                          contexto=ctx, alvos=[campo])
            print("V(%s) valor=%r -> estado=%s lacunas=%s ok=%s"
                  % (campo, valor, n["campos"][campo]["estado"], n["lacunas"], n["ok"]))


if __name__ == "__main__":
    main()
