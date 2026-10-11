#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prova_red_kit09.py - PROVA RED SELETIVA por guarda do pacote KIT-09 (F7 do KIT-09R).

O QUE ESTE DRIVER PROVA (por item, com neutralizacao ESPECIFICA de UMA guarda)
-----------------------------------------------------------------------------
Para CADA guarda normativa existe um par: (trecho ORIGINAL, trecho neutralizado). O
driver carrega o fonte REAL, aplica SO aquela substituicao (exigindo uma unica
ocorrencia no texto) e avalia a checagem normativa correspondente:

  * fonte ORIGINAL -> a checagem PASSA (o comportamento normativo existe);
  * fonte NEUTRALIZADO -> a mesma checagem FALHA (o defeito volta: e a prova RED).

A neutralizacao e IN-MEMORY: o arquivo do repositorio nunca e reescrito, e o driver
confere o SHA256 do arquivo antes e depois (restauracao byte a byte garantida e
medida, nao afirmada).

Alem disso o driver materializa UM mutante em disco (guard de render-observado, o
mesmo usado na revisao KIT-09R) dentro de uma COPIA descartavel de `tools/` e roda a
suite durável (`test_kit09.py`): a suite tem de REPROVAR com o mutante (exit != 0) e
PASSAR com o byte original restaurado.

Uso:  python tools/automacao/cenarios/prova_red_kit09.py [--json saida.json]
Exit: 0 = todos os RED demonstrados e byte restaurado; 1 = alguma prova falhou.
"""
import argparse
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
FONTE = os.path.join(AQUI, "kit09.py")
SUITE = os.path.join(AQUI, "test_kit09.py")
COLETOR = os.path.join(REPO, "tools", "automacao", "runtime", "coletor.py")


def _load(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


S = _load("kit09_suite_ref", SUITE)          # reusa obs_completa/IDENT/deltas da suite
COL = _load("kit09_coletor_ref", COLETOR)


def _norm(o):
    return COL.normalizar_observacao(o, "runtime", alvos=[])


def _por_id(K, obs, cid, ident=None, envelope=None):
    criterios = K.avaliar_cenarios(obs, ident or S.IDENT, envelope=envelope)
    return [c for c in criterios if c["id"] == cid][0]


# --------------------------------------------------------------- checagens normativas
# Cada funcao devolve True quando o comportamento NORMATIVO se cumpre.

def c_f1_rotulo_observacao(K):
    return _por_id(K, [S.obs_completa(sintetico=True)], "KIT09-RSTV6-personagem")["estado"] != "OK"


def c_f1_envelope_sintetico(K):
    fx = S.carrega("kit09-verdade")
    crit = K.avaliar_cenarios(list(fx["observacoes"]), S.IDENT, envelope=fx)
    return [c["id"] for c in crit if c["estado"] == "OK"] == []


def c_f6_sessao_velha(K):
    ident = dict(S.IDENT, sessao_esperada="2099-01-01T00:00:00")
    c = _por_id(K, [S.obs_completa()], "KIT09-RSTV6-pontos-sem-mutacao", ident=ident)
    return c["prova_runtime"] is False and c["estado"] != "OK"


def c_f2_normalizado_positivo(K):
    c = _por_id(K, [_norm(S.obs_completa())], "KIT09-RSTV21-tooltip-pai")
    return c["estado"] == "OK"


def c_f2_normalizado_defeito(K):
    o = S.obs_completa()
    o["tooltip_pai_depois"] = "outro pai"
    return _por_id(K, [_norm(o)], "KIT09-RSTV21-tooltip-pai")["estado"] == "REPROVADO"


def c_f3_mapas_vazios(K):
    o = S.obs_completa(linhas_dependencia={}, dependency_por_tier={})
    o.pop("arestas_inventadas")
    return _por_id(K, [o], "KIT09-RSTV25b-arestas")["estado"] != "OK"


def c_f3_t5_aresta_inventada(K):
    o = S.obs_completa(linhas_dependencia={"T1": 2, "T5": 1},
                       dependency_por_tier={"T1": 2, "T5": 0})
    o.pop("arestas_inventadas")
    return _por_id(K, [o], "KIT09-RSTV25b-sem-aresta-inventada")["estado"] == "REPROVADO"


def c_f3_ausencia_nao_e_zero(K):
    o = S.obs_completa()
    o.pop("linhas_dependencia")
    return _por_id(K, [o], "KIT09-RSTV25b-ausencia-legitima")["estado"] != "OK"


def c_f4_malformado_caminho(K):
    o = S.obs_completa(tooltip_pai_antes=[], tooltip_pai_depois=[])
    return _por_id(K, [o], "KIT09-RSTV21-tooltip-pai")["estado"] != "OK"


def c_f4_pontos_infinito(K):
    o = S.obs_completa(pontos_antes=float("inf"), pontos_depois=float("inf"))
    return _por_id(K, [o], "KIT09-RSTV6-pontos-sem-mutacao")["estado"] != "OK"


def c_f5_alvo_errado(K):
    o = S.obs_completa(clique_fisico={"recebido": True, "alvo": "MainMenu/QuitButton"})
    return _por_id(K, [o], "KIT09-RSTV5-clique-fisico")["estado"] != "OK"


def c_f7_render_defeito(K):
    o = S.obs_completa(texto_bruto="Deals [2] fire damage.",
                       texto_renderizado="Deals [2] fire damage.")
    return _por_id(K, [o], "KIT09-RSTV26-render-observado")["estado"] == "REPROVADO"


def c_f7_render_ausente(K):
    o = S.obs_completa()
    o.pop("texto_renderizado")
    return _por_id(K, [o], "KIT09-RSTV26-render-observado")["estado"] != "OK"


MUTACOES = (
    ("F1-rotulo-na-observacao", "KIT09-RSTV6-personagem", c_f1_rotulo_observacao,
     "    for o in contrib:\n        for m in _marcas_de_origem(o):",
     "    for o in []:\n        for m in _marcas_de_origem(o):"),
    ("F1-envelope-sintetico", "KIT09-RSTV26-render-observado", c_f1_envelope_sintetico,
     "    for m in _marcas_de_origem(envelope):\n        _add(",
     "    for m in []:\n        _add("),
    ("F6-sessao-esperada", "KIT09-RSTV6-pontos-sem-mutacao", c_f6_sessao_velha,
     "    esperada = RC._txt((ident or {}).get(\"sessao_esperada\"))\n"
     "    if not esperada:\n        return []\n    motivos = []",
     "    return []\n    motivos = []"),
    ("F2-leitura-normalizada", "KIT09-RSTV21-tooltip-pai", c_f2_normalizado_positivo,
     "            a, b = RC._campo(o, ka), RC._campo(o, kb)",
     "            a, b = o.get(ka), o.get(kb)"),
    ("F4-validacao-de-caminho", "KIT09-RSTV21-tooltip-pai", c_f4_malformado_caminho,
     "    if not isinstance(v, str) or not v.strip():\n"
     "        return None, \"%r NAO e um caminho valido (esperado string nao vazia)\" % (v,)\n"
     "    return v.strip(), None",
     "    return v, None"),
    ("F4-finitude-dos-pontos", "KIT09-RSTV6-pontos-sem-mutacao", c_f4_pontos_infinito,
     "                    elif not (RC._numero_finito(antes) is not None\n"
     "                              and RC._numero_finito(depois) is not None):\n"
     "                        # F4 do KIT-09R: finitude/dominio ANTES da comparacao — 'inf'\n"
     "                        # nao e leitura de pontos; antes, inf == inf fechava OK.\n"
     "                        motivos.append(\"pontos: valor NAO FINITO (antes=%r, depois=%r) — \"\n"
     "                                       \"'NaN'/infinito nao mede pontos\" % (antes, depois))\n",
     ""),
    ("F3-mapas-vazios", "KIT09-RSTV25b-arestas", c_f3_mapas_vazios,
     "        if not tiers:\n"
     "            motivos.append(\"nenhum tier lido (mapas vazios): sem leitura nao ha confronto \"\n"
     "                           \"mensuravel — vazio nao aprova\")\n"
     "            indet = True\n"
     "            continue\n",
     ""),
    ("F3-t5-no-criterio-especifico", "KIT09-RSTV25b-sem-aresta-inventada",
     c_f3_t5_aresta_inventada,
     "            for tier in sorted(set(list(linhas) + list(dep))):\n"
     "                pres_l, pres_d = tier in linhas, tier in dep\n"
     "                vl, vd = linhas.get(tier), dep.get(tier)",
     "            for tier in sorted(set(list(linhas) + list(dep))):\n"
     "                pres_l, pres_d = tier in linhas, tier in dep\n"
     "                vl, vd = linhas.get(tier), dep.get(tier)\n"
     "                if tier == \"T5\":\n"
     "                    continue"),
    ("F3-ausencia-nao-e-zero", "KIT09-RSTV25b-ausencia-legitima", c_f3_ausencia_nao_e_zero,
     "        if not isinstance(linhas, dict):\n"
     "            contrib.append(o)\n"
     "            dados = True\n"
     "            motivos.append(\"linhas por tier AUSENTES/INCOMPLETAS (tipo %s): a ausencia \"\n"
     "                           \"legitima exige ler os DOIS lados (0/0), nunca assumir zero\"\n"
     "                           % type(linhas).__name__)\n"
     "            continue\n",
     "        if not isinstance(linhas, dict):\n"
     "            linhas = {t: 0 for t in dep}\n"),
    ("F5-alvo-do-clique", "KIT09-RSTV5-clique-fisico", c_f5_alvo_errado,
     "        if observado != esperado:",
     "        if False:"),
    ("F7-render-igual-ao-template", "KIT09-RSTV26-render-observado", c_f7_render_defeito,
     "        if bruto and render and render.strip() == bruto.strip() and _tem_template(bruto):",
     "        if False:"),
    ("F7-render-ausente", "KIT09-RSTV26-render-observado", c_f7_render_ausente,
     "        if not render:\n"
     "            motivos.append(\"texto RENDERIZADO nao observado (so o cru %r): o template do \"\n"
     "                           \"motor nao prova o render\" % (bruto,))\n"
     "            continue",
     "        if not render:\n            pass"),
)


def _carrega_texto(nome, texto):
    pasta = tempfile.mkdtemp(prefix="kit09red-")
    # o kit09 importa o CIC-3 (`rstv.py`) do PROPRIO diretorio: a copia do fonte
    # precisa do vizinho real para subir igual ao modulo do repositorio.
    shutil.copy2(os.path.join(AQUI, "rstv.py"), os.path.join(pasta, "rstv.py"))
    caminho = os.path.join(pasta, nome + ".py")
    with open(caminho, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(texto)
    return _load(nome, caminho)


def _run_suite_no_mutante(texto_mutante, original):
    """Suite durável contra o mutante em disco (copia descartavel de tools/)."""
    tmp = tempfile.mkdtemp(prefix="kit09red-suite-")
    copia = os.path.join(tmp, "tools", "automacao")
    shutil.copytree(os.path.join(REPO, "tools", "testes"), os.path.join(tmp, "tools", "testes"))
    shutil.copytree(os.path.join(REPO, "tools", "automacao"),
                    os.path.join(tmp, "tools", "automacao"))
    alvo = os.path.join(tmp, "tools", "automacao", "cenarios", "kit09.py")
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
    suite = os.path.join(tmp, "tools", "automacao", "cenarios", "test_kit09.py")

    with open(alvo, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(texto_mutante)
    p_mut = subprocess.run([sys.executable, suite], cwd=tmp, capture_output=True,
                           text=True, encoding="utf-8", env=env, timeout=180)
    with open(alvo, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(original)
    p_ok = subprocess.run([sys.executable, suite], cwd=tmp, capture_output=True,
                          text=True, encoding="utf-8", env=env, timeout=180)
    restaurado = hashlib.sha256(open(alvo, "rb").read()).hexdigest()
    shutil.rmtree(tmp, ignore_errors=True)
    return {"mutante_exit": p_mut.returncode,
            "mutante_stdout": p_mut.stdout.strip()[-400:],
            "restaurado_exit": p_ok.returncode,
            "restaurado_stdout": p_ok.stdout.strip()[-400:],
            "sha_restaurado": restaurado}


def main(argv=None):
    ap = argparse.ArgumentParser(description="KIT-09F: prova RED seletiva por guarda.")
    ap.add_argument("--json", help="grava o relatorio JSON neste arquivo")
    args = ap.parse_args(argv)

    with open(FONTE, "rb") as fh:
        original = fh.read().decode("utf-8")
    sha_antes = hashlib.sha256(original.encode("utf-8")).hexdigest()

    K_orig = _carrega_texto("kit09_pristino", original)
    falhas, provas = [], []
    for nome, cid, checagem, trecho, mutado in MUTACOES:
        ocorrencias = original.count(trecho)
        if ocorrencias != 1:
            falhas.append("%s: trecho alvo aparece %d vez(es) (exigido 1)" % (nome, ocorrencias))
            continue
        verde = bool(checagem(K_orig))
        K_mut = _carrega_texto("kit09_mut_" + nome.replace("-", "_"),
                               original.replace(trecho, mutado))
        try:
            vermelho = not bool(checagem(K_mut))
        except Exception as erro:
            vermelho = True
            detalhe_erro = "%s: %s" % (type(erro).__name__, erro)
        else:
            detalhe_erro = None
        prova = {"mutacao": nome, "criterio": cid, "verde_no_original": verde,
                 "red_no_neutralizado": vermelho, "erro_no_mutante": detalhe_erro}
        if not (verde and vermelho):
            falhas.append("%s: verde=%s red=%s" % (nome, verde, vermelho))
        provas.append(prova)
        print("RED %-32s original=%s neutralizado_reprova=%s %s"
              % (nome, "PASSA" if verde else "FALHA",
                 "SIM" if vermelho else "NAO", detalhe_erro or ""))

    # suite durável contra UM mutante em disco (guarda de render) + restauracao byte a byte
    nome = "F7-render-ausente"
    trecho = dict((m[0], (m[3], m[4])) for m in MUTACOES)[nome]
    mutante_txt = original.replace(trecho[0], trecho[1])
    suite_ev = _run_suite_no_mutante(mutante_txt, original)
    if suite_ev["mutante_exit"] == 0:
        falhas.append("suite durável NAO reprovou com o mutante de render (exit 0)")
    if suite_ev["restaurado_exit"] != 0:
        falhas.append("suite durável nao voltou a PASSAR apos restaurar (exit %d)"
                      % suite_ev["restaurado_exit"])
    if suite_ev["sha_restaurado"] != sha_antes:
        falhas.append("restauracao byte a byte falhou: sha %s != %s"
                      % (suite_ev["sha_restaurado"], sha_antes))
    suite_ev["sha_original"] = sha_antes
    print("SUITE no mutante: exit %s | apos restaurar: exit %s | sha restaurado == original: %s"
          % (suite_ev["mutante_exit"], suite_ev["restaurado_exit"],
             suite_ev["sha_restaurado"] == sha_antes))

    sha_depois = hashlib.sha256(open(FONTE, "rb").read()).hexdigest()
    if sha_depois != sha_antes:
        falhas.append("o fonte do repositorio mudou durante o driver (sha %s != %s)"
                      % (sha_depois, sha_antes))
    relatorio = {"fonte": FONTE, "sha256_antes": sha_antes, "sha256_depois": sha_depois,
                 "mutacoes": provas, "suite_com_mutante": suite_ev, "falhas": falhas}
    if args.json:
        with open(args.json, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(relatorio, fh, ensure_ascii=False, indent=2)
    print("PROVA-RED|%s|%d mutacoes|falhas=%d"
          % ("PASSOU" if not falhas else "REPROVOU", len(provas), len(falhas)))
    for f in falhas:
        print("FALHA", f)
    return 0 if not falhas else 1


if __name__ == "__main__":
    sys.exit(main())
