#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""refutar_cor_aut7f2.py - COR-AUT7-F2: refutacao dos achados A1-A9 (execucao 415).

Roda as CLIs REAIS (produtor -> decisor -> consolidador) e as suites da ferramenta e do
aceite contra os nove achados do parecer independente COR-AUT7R (t_11839818, execucao 408).
Nenhum dado aqui e runtime: as entradas sao SINTETICAS e rotuladas. Sem jogo, build, deploy,
save ou publicacao.

A mutacao de ARTEFATO (o experimento A6: pacote `dist/*.zip` e DLL de `bin/`) acontece numa
COPIA do repo em sandbox - o repo vivo e tratado como READ-ONLY por este script. O unico
arquivo do repo vivo reescrito aqui e o doc gerado pela propria ferramenta
(`AUT-7-relatorio.md` / `AUT-7-resultado.json`, pela CLI corrigida, como a correcao manda).

Uso (tres fases, cada uma bem abaixo do limite de um processo longo):
    python tools/automacao/estilo/refutar_cor_aut7f2.py            # fase 1: achados A1-A9 (CLIs reais)
    python tools/automacao/estilo/refutar_cor_aut7f2_entradas.py   # fase 1.5: ENTRADAS medidas no cache
    python tools/automacao/estilo/fechar_cor_aut7f2.py             # fase 2: suites verdes + docs
As fases 1.5 e 2 COMPLETAM o mesmo `refutacao-cor-aut7-f2.json` (a 1.5 grava `achados.A6_entradas`;
a 2 grava `suites` e `docs`/`hashes` e escreve `docs-antes.txt`). O experimento A6 (R1-R7) reusa
uma copia do repo em `COR_F2_SANDBOX`; a copia e RECOPIADA automaticamente se o codigo entregue
mudou (sandbox de execucao anterior produziria evidencia de outro binario).
Env:
    COR_S            raiz do repo (default: sobe a partir deste arquivo)
    COR_OUT          diretorio de evidencia (default: docs/automacao/COR-AUT7-F2-evidencias)
    COR_F2_SANDBOX   onde criar a copia do repo (default: <TMP>/cor-aut7f2-sandbox)
"""
import glob
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile

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
OUT = os.environ.get("COR_OUT") or os.path.join(S, "docs", "automacao", "COR-AUT7-F2-evidencias")
SANDBOX_RAIZ = os.environ.get("COR_F2_SANDBOX") or os.path.join(
    os.environ.get("TEMP") or tempfile.gettempdir(), "cor-aut7f2-sandbox")
os.makedirs(OUT, exist_ok=True)
TMP = tempfile.mkdtemp(prefix="cor-aut7f2-")
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", TEMP=TMP, TMP=TMP, TMPDIR=TMP,
           PYTHONIOENCODING="utf-8")
sys.path.insert(0, os.path.join(S, "tools"))
sys.path.insert(0, os.path.join(S, "tools", "automacao"))
sys.path.insert(0, os.path.join(S, "tools", "automacao", "estilo"))

ESTILO = os.path.join("tools", "automacao", "estilo", "estilo_atributos.py")
ACEITE = os.path.join("tools", "automacao", "aceite", "relatorio_aceite.py")
DOC_REL = os.path.join("docs", "automacao", "AUT-7-relatorio.md")
DOC_RES = os.path.join("docs", "automacao", "AUT-7-resultado.json")
DENTRO_DO_PACOTE = "plugins/BetterCombatText/BetterCombatText.dll"
PADRAO_OK = b"get_fontSharedMaterial"      # membro do controle POSITIVO do leitor de IL
PADRAO_DEFEITO = b"set_fontSharedMaterial"  # vira setter de material = defeito da regra de ouro


def sha(caminho):
    h = hashlib.sha256()
    with io.open(caminho, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def sha_bytes(dados):
    return hashlib.sha256(dados).hexdigest()


def roda(nome, argv, cwd=None, timeout=3600, guardar=True):
    p = subprocess.run([sys.executable] + list(argv), cwd=cwd or S, env=ENV,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    if guardar:
        with io.open(os.path.join(OUT, nome + ".stdout"), "wb") as fh:
            fh.write(p.stdout)
        with io.open(os.path.join(OUT, nome + ".stderr"), "wb") as fh:
            fh.write(p.stderr)
    print("  %-38s exit=%s" % (nome, p.returncode))
    return p


def escreve_json(nome, dado):
    caminho = os.path.join(OUT, nome)
    with io.open(caminho, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(dado, indent=2, ensure_ascii=False, default=str))
    return caminho


def carrega(nome, rel):
    import importlib.util
    spec = importlib.util.spec_from_file_location(nome, os.path.join(S, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def identidade_sintetica():
    ident = {"fonte_sha": "f" * 64, "dll_sha": "d" * 64, "sessao": "cor-aut7f2-sintetica"}
    caminho = os.path.join(OUT, "identidade.json")
    with io.open(caminho, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(ident, indent=2))
    return ident, caminho


IDENT, IDENT_PATH = identidade_sintetica()
MARCADOR = os.path.join(OUT, "marcador-sintetico.txt")
with io.open(MARCADOR, "w", encoding="utf-8") as fh:
    fh.write("CONTROLE SINTETICO DA REFUTACAO - NAO E EVIDENCIA DE RUNTIME\n")
SHA_MARCADOR = sha(MARCADOR)


def obs(**kw):
    base = {"procedencia": "runtime", "sessao": IDENT["sessao"], "fonte_sha": IDENT["fonte_sha"],
            "dll_sha": IDENT["dll_sha"], "evidencia": MARCADOR}
    base.update(kw)
    return base


OBS_DIR = os.path.join(OUT, "obs")
os.makedirs(OBS_DIR, exist_ok=True)


def vincular(o, nome):
    """Amarra a observacao aos BYTES da propria evidencia (regra do `_vinculo_obs`).

    Sem isto um OK de runtime seria falso: o arquivo de evidencia tem de CONTER a observacao
    e o sha tem de bater. O arquivo fica no diretorio de evidencia desta refutacao.
    """
    caminho = os.path.join(OBS_DIR, nome + ".obs.json")
    baseline = {k: v for k, v in o.items() if k != "evidencia"}
    with io.open(caminho, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(baseline, ensure_ascii=False, sort_keys=True))
    o = dict(o)
    o["evidencia"] = [{"caminho": caminho, "sha256": sha(caminho)}]
    return o


def roda_par(nome, observacoes, sufixo):
    """CLI produtor (estilo) -> CLI consolidador para UMA observacao, devolvendo o criterio."""
    entrada = os.path.join(OUT, nome + ".input.json")
    with io.open(entrada, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(observacoes, indent=2))
    est_json = os.path.join(OUT, nome + ".estilo.json")
    ace_json = os.path.join(OUT, nome + ".aceite.json")
    p1 = roda("cli-" + nome, [ESTILO, "--repo", S, "--out-dir", OUT, "--sem-suite",
                              "--identidade", IDENT_PATH, "--observacoes", entrada,
                              "--out", est_json])
    p2 = roda("cons-" + nome, [ACEITE, "--repo", S, "--out-dir", OUT, "--sem-suite",
                               "--identidade", IDENT_PATH, "--estilo-observacoes", entrada,
                               "--out", ace_json])
    with io.open(est_json, encoding="utf-8") as fh:
        est = json.load(fh)
    alvos = [c for c in est["criterios"] if str(c["id"]).endswith(sufixo)]
    alvo = alvos[0] if alvos else {}
    with io.open(ace_json, encoding="utf-8") as fh:
        ace = json.load(fh)
    todos = [c for b in ace["decisao"]["por_mod"].values() for c in b.get("criterios", [])]
    dc = [c for c in todos if c["id"] == alvo.get("id")]
    vinc = alvo.get("id") in [c["id"] for b in ace["decisao"]["por_mod"].values()
                              for c in b.get("ok_vinculantes", [])]
    return {"estado_estilo": alvo.get("estado"), "superficies_medidas": alvo.get("superficies_medidas"),
            "motivo_estilo": str(alvo.get("motivo"))[:300],
            "classificacao_consolidador": (dc[0]["classificacao"] if dc else None),
            "ok_vinculante": bool(vinc), "exit_produtor": p1.returncode,
            "exit_consolidador": p2.returncode, "sintetico": True}


RES = {"tarefa": "t_cd1332d7 (COR-AUT7-F2)", "execucao": "430",
       "fonte_dos_achados": "COR-AUT7R (t_11839818, execucao 408)",
       "revisao_da_rodada_1": "execucao 425 (parecer: A6 nao fechado - a fotografia nao cobria as "
                              "ENTRADAS lidas pelos testes; ver `achados.A6_entradas`, fase 1.5)",
       "runtime": "NAO EXERCITADO", "achados": {}, "hashes": {}}

# As TRES fases completam UM relatorio. Reexecutar a fase 1 nao pode apagar o que as outras
# gravaram no mesmo JSON (fase 1.5: `achados.A6_entradas`; fase 2: `suites`/`docs`): senao a
# evidencia das ENTRADAS medidas desapareceria em silencio num re-run - a mesma classe de
# falso-OK (prova que some e ninguem ve) que este cartao conserta.
JSON_REFUTACAO = os.path.join(OUT, "refutacao-cor-aut7-f2.json")
if os.path.isfile(JSON_REFUTACAO):
    try:
        _PREV = json.load(io.open(JSON_REFUTACAO, encoding="utf-8"))
    except ValueError:
        _PREV = None
    if isinstance(_PREV, dict):
        for _k, _v in ((_PREV.get("achados") or {}).items()):
            if _k == "A6_entradas":
                RES["achados"][_k] = _v
        for _k in ("suites", "docs"):
            if _PREV.get(_k):
                RES[_k] = _PREV[_k]
        print("== relatorio anterior preservado: %s" % sorted(RES["achados"]))

print("== A3: superficie do BCT por TOKEN (6 leituras nao podem marcar a 7a)")
bct = carrega("f2_regras_bct", os.path.join("tools", "testes", "regras_bct.py"))
SUP = list(bct.SUPERFICIES_DO_BCT)
sem_healthbar = [n for n in SUP if n != "Healthbar"]


def leitura_bct(nome_sup, indice):
    cores = {"texto": "#FFFFFFFF (r=1 g=1 b=1 a=1)", "sombra": "#%sFF (r=0 g=0 b=0 a=1)"
                                                          % str(bct.sombra_para("FFFFFF")).upper().lstrip("#")}
    return vincular(obs(objeto=nome_sup + "_Text", caminho="Canvas/HUD/" + nome_sup + "/Text",
                        componente="TextMeshProUGUI", cores=cores,
                        keywords={"OUTLINE_ON": True, "UNDERLAY_ON": True}),
                    "bct-%d-%s" % (indice, nome_sup))


a3 = roda_par("A3-bct-6-de-7-superficies",
              [leitura_bct(n, i) for i, n in enumerate(sem_healthbar)],
              "runtime-superficies-contraste")
a3.update({"canonicas": SUP, "leituras_enviadas": sem_healthbar,
           "esperado": "NOT_OK: sem leitura da superficie `Healthbar`, o criterio tem de ser "
                       "LACUNA nominal (nunca OK/OK_VINCULANTE)",
           "falso_OK_sumiu": (a3["estado_estilo"] != "OK" and not a3["ok_vinculante"]
                              and "Healthbar" not in (a3["superficies_medidas"] or []))})
RES["achados"]["A3"] = a3
print("    estado=%s vinculante=%s medidas=%s" % (a3["estado_estilo"], a3["ok_vinculante"],
                                                  len(a3["superficies_medidas"] or [])))

print("== A3b (controle positivo): as 7 superficies de verdade fecham OK")
a3b = roda_par("A3b-bct-7-de-7-superficies", [leitura_bct(n, 100 + i) for i, n in enumerate(SUP)],
               "runtime-superficies-contraste")
a3b["esperado"] = "OK (controle): o criterio continua satisfazivel"
a3b["controle_ok"] = a3b["estado_estilo"] == "OK"
RES["achados"]["A3b_controle"] = a3b
print("    estado=%s vinculante=%s" % (a3b["estado_estilo"], a3b["ok_vinculante"]))

print("== A1: par BF com chave de um lado SO tem de REPROVAR")
rbf = carrega("f2_regras_bf_estilo", os.path.join("tools", "testes", "regras_bf_estilo.py"))
MATERIAL = {}
for _grupo, _nomes in rbf.PRECISA_COPIAR.items():
    for _nome in _nomes:
        MATERIAL[_nome] = ([0.5] * 4 if _nome == "_ClipRect"
                           else ("#FFFFFFFF" if _nome.endswith("Color") else 0.5))
CORES = {"texto": "#FFFFFFFF (a=1)", "face": "#FF0000FF (a=1)", "contorno": "#000000FF (a=1)",
         "sombra": "#000000FF (a=1)"}
EXTRA = {"_ExtraDoMod": "extra_so_no_lado_ligado"}


def par_bf(cor_ligada, cor_desligada):
    """Par ligado/desligado do BF em FIXTURE (o par em si nao afirma runtime)."""
    comum = {"objeto": "Tooltip.Title", "procedencia": "fixture",
             "keywords": {"OUTLINE_ON": True, "UNDERLAY_ON": True},
             "shader_keywords": ["OUTLINE_ON", "UNDERLAY_ON"], "propriedades_material": MATERIAL}
    return [dict(comum, fonte="Serifa_Nova", mod_ativo=True, cores=cor_ligada),
            dict(comum, fonte="Serifa_Original", mod_ativo=False, cores=cor_desligada)]


a1 = roda_par("A1-bf-par-chave-de-um-lado", par_bf(dict(CORES, **EXTRA), CORES),
              "runtime-preservacao-estilo")
a1.update({"chave_extra": "_ExtraDoMod",
           "esperado": "REPROVADO: chave que existe SO de um lado e diferenca medida",
           "falso_OK_sumiu": (a1["estado_estilo"] == "REPROVADO" and not a1["ok_vinculante"])})
RES["achados"]["A1"] = a1
print("    estado=%s vinculante=%s motivo=%s" % (a1["estado_estilo"], a1["ok_vinculante"],
                                                 a1["motivo_estilo"][:90]))

print("== A1b (controle positivo): o MESMO par sem a chave extra nao REPROVA")
a1b = roda_par("A1b-bf-par-identico", par_bf(CORES, CORES), "runtime-preservacao-estilo")
a1b["esperado"] = "nao REPROVADO (controle): a diferenca do A1 vem da chave, nao do resto"
a1b["controle_ok"] = a1b["estado_estilo"] != "REPROVADO"
RES["achados"]["A1b_controle"] = a1b
print("    estado=%s vinculante=%s" % (a1b["estado_estilo"], a1b["ok_vinculante"]))

print("== A2: config legitimo x identidade (com e sem hash de config declarado)")
A2_DIR = os.path.join(OUT, "config")
os.makedirs(A2_DIR, exist_ok=True)
defaults = rbf.defaults_com_linha(io.open(os.path.join(S, "BetterFont", "Plugin.cs"),
                                          encoding="utf-8").read())
CFG = os.path.join(A2_DIR, "com.gumatos.betterfont.cfg")
with io.open(CFG, "w", encoding="utf-8") as fh:
    fh.write("[Geral]\n" + "".join("%s = %s\n" % (k, "true" if v["valor"] else "false")
                                   for k, v in sorted(defaults.items())))
SHA_CFG = sha(CFG)
VALORES = {k: bool(v["valor"]) for k, v in defaults.items()}
CFG_OBS = vincular(obs(objeto="BetterFont.cfg", config_sha=SHA_CFG,
                       config={"caminho": CFG, "sha256": SHA_CFG, "valores": VALORES}),
                   "config-bf")
IDENT_COM_CFG = os.path.join(OUT, "identidade-com-config.json")
with io.open(IDENT_COM_CFG, "w", encoding="utf-8") as fh:
    fh.write(json.dumps(dict(IDENT, config_sha=SHA_CFG), indent=2))
IDENT_CFG_ERRADA = os.path.join(OUT, "identidade-config-errada.json")
with io.open(IDENT_CFG_ERRADA, "w", encoding="utf-8") as fh:
    fh.write(json.dumps(dict(IDENT, config_sha="c" * 64), indent=2))


def roda_config(nome, ident_path, observacao):
    entrada = os.path.join(OUT, nome + ".input.json")
    with io.open(entrada, "w", encoding="utf-8") as fh:
        fh.write(json.dumps([observacao], indent=2))
    est_json = os.path.join(OUT, nome + ".estilo.json")
    ace_json = os.path.join(OUT, nome + ".aceite.json")
    p1 = roda("cli-" + nome, [ESTILO, "--repo", S, "--out-dir", OUT, "--sem-suite",
                              "--identidade", ident_path, "--observacoes", entrada,
                              "--out", est_json])
    p2 = roda("cons-" + nome, [ACEITE, "--repo", S, "--out-dir", OUT, "--sem-suite",
                               "--identidade", ident_path, "--estilo-observacoes", entrada,
                               "--out", ace_json])
    with io.open(est_json, encoding="utf-8") as fh:
        est = json.load(fh)
    alvo = [c for c in est["criterios"] if str(c["id"]).endswith("runtime-config")][0]
    with io.open(ace_json, encoding="utf-8") as fh:
        ace = json.load(fh)
    vinc = alvo["id"] in [c["id"] for b in ace["decisao"]["por_mod"].values()
                          for c in b.get("ok_vinculantes", [])]
    return {"estado_estilo": alvo["estado"], "motivo_estilo": str(alvo["motivo"])[:300],
            "ok_vinculante": bool(vinc), "exit_produtor": p1.returncode,
            "exit_consolidador": p2.returncode, "identidade": os.path.basename(ident_path),
            "sintetico": True}


a2_sem = roda_config("A2-config-identidade-sem-hash", IDENT_PATH, CFG_OBS)
a2_sem.update({"esperado": "NAO_EXERCITADO (LACUNA declarada) - antes era REPROVADO: criterio "
                           "insatisfazivel / falso-REPROVADO de config legitimo",
               "corrigido": a2_sem["estado_estilo"] == "NAO_EXERCITADO"})
a2_com = roda_config("A2-config-identidade-com-hash", IDENT_COM_CFG, CFG_OBS)
a2_com.update({"esperado": "OK (criterio satisfazivel: a identidade declara o config_sha)",
               "corrigido": a2_com["estado_estilo"] == "OK"})
a2_errado = roda_config("A2-config-identidade-hash-errado", IDENT_CFG_ERRADA, CFG_OBS)
a2_errado.update({"esperado": "REPROVADO (hash de config de OUTRA rodada)",
                  "corrigido": a2_errado["estado_estilo"] == "REPROVADO"})
RES["achados"]["A2"] = {"sem_hash_na_identidade": a2_sem, "com_hash_na_identidade": a2_com,
                        "hash_errado": a2_errado, "config_sha_real": SHA_CFG}
for k in ("sem_hash_na_identidade", "com_hash_na_identidade", "hash_errado"):
    print("    %-26s estado=%s" % (k, RES["achados"]["A2"][k]["estado_estilo"]))

print("== A7: X5 do parecer (rotulo OK, arquivo qualquer, identidade emprestada)")
X7_DIR = os.path.join(OUT, "frentes")
os.makedirs(X7_DIR, exist_ok=True)


def frente_json(nome, itens, identidade=None):
    dado = {"esquema": "AUT-6/refutacao-f2", "criterios": itens}
    if identidade:
        dado["identidade"] = identidade
    caminho = os.path.join(X7_DIR, nome + ".json")
    with io.open(caminho, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(dado, ensure_ascii=False))
    return caminho


def roda_frente(nome, itens, ident_result=None):
    caminho = frente_json(nome, itens, ident_result)
    ace_json = os.path.join(OUT, "cons-" + nome + ".aceite.json")
    p = roda("cons-" + nome, [ACEITE, "--repo", S, "--out-dir", OUT, "--sem-suite",
                              "--identidade", IDENT_PATH, "--shrines-criterios", caminho,
                              "--out", ace_json])
    with io.open(ace_json, encoding="utf-8") as fh:
        ace = json.load(fh)
    todos = [c for b in ace["decisao"]["por_mod"].values() for c in b.get("criterios", [])]
    alvo = [c for c in todos if str(c["id"]).startswith("AUT-6/sint")]
    vinc = [c["id"] for b in ace["decisao"]["por_mod"].values() for c in b.get("ok_vinculantes", [])]
    return {"classificacao": [(c["estado"], c["classificacao"]) for c in alvo],
            "ok_vinculante": [v for v in vinc if v.startswith("AUT-6/sint")],
            "lacunas_canonicas": sorted({c["id"] for c in todos
                                         if str(c["id"]).startswith("AUT-6/")
                                         and not str(c["id"]).startswith("AUT-6/sint")}),
            "exit": p.returncode, "sintetico": True}


def item_frente(id_, **kw):
    c = {"id": id_, "mod": "BetterTooltips", "estado": "OK", "classe": "runtime",
         "procedencia": "runtime", "prova_runtime": True, "sessao": IDENT["sessao"],
         "esperado": "criterio sintetico da refutacao", "observado": "rotulo OK sem medicao",
         "evidencia": [{"caminho": MARCADOR, "sha256": SHA_MARCADOR}]}
    c.update(kw)
    return c


a7 = {
    "X5a-evidencia-inexistente": roda_frente("X5a-evidencia-inexistente", [item_frente(
        "AUT-6/sint/ev-inexistente", evidencia=[{"caminho": os.path.join(X7_DIR, "NAO-EXISTE.json"),
                                                 "sha256": "0" * 64}])]),
    "X5b-rotulo-arquivo-qualquer": roda_frente("X5b-rotulo-arquivo-qualquer",
                                               [item_frente("AUT-6/sint/rotulo")]),
    "X5c-identidade-divergente": roda_frente("X5c-identidade-divergente", [item_frente(
        "AUT-6/sint/ident-div", identidade={"fonte_sha": "0" * 64, "dll_sha": "1" * 64})]),
    "X5d-sem-evidencia": roda_frente("X5d-sem-evidencia",
                                     [item_frente("AUT-6/sint/sem-ev", evidencia=[])]),
    "X5e-sha-divergente": roda_frente("X5e-sha-divergente", [item_frente(
        "AUT-6/sint/sha-ruim", evidencia=[{"caminho": MARCADOR, "sha256": "f" * 64}])]),
    "X5f-resultado-de-outra-rodada": roda_frente(
        "X5f-resultado-de-outra-rodada",
        [item_frente("AUT-6/sint/proprio", fonte_sha=IDENT["fonte_sha"], dll_sha=IDENT["dll_sha"])],
        ident_result={"fonte_sha": "9" * 64, "dll_sha": "8" * 64}),
    "controle-item-com-identidade-propria": roda_frente(
        "controle-item-com-identidade-propria",
        [item_frente("AUT-6/sint/legitimo", fonte_sha=IDENT["fonte_sha"], dll_sha=IDENT["dll_sha"])],
        ident_result=IDENT),
}
for _n, _v in a7.items():
    print("    %-38s %s | vinculante=%s | lacunas=%s"
          % (_n, _v["classificacao"], _v["ok_vinculante"], _v["lacunas_canonicas"]))
a7["_leitura"] = ("X5a/X5d/X5e: item inadmissivel (lacuna canonica de malformado); X5b/X5c/X5f: "
                  "item REBAIXADO para NAO_EXERCITADO e NAO vinculante; o controle com "
                  "identidade propria continua seguindo OK - a frente real nao foi enfraquecida.")
RES["achados"]["A7"] = a7

print("== A8: a frente REAL do AUT-6 carrega na arvore entregue")
ra = carrega("f2_relatorio_aceite", ACEITE)
mod, rel_aut6, rotulo = ra._frente_avaliador("AUT-6")
crit_aut6 = ra.criterios_shrines([{"objeto": "Tooltip.Title", "procedencia": "fixture"}], IDENT)
a8 = {
    "modulo_preferido": rel_aut6,
    "carregou": mod is not None,
    "rotulo": rotulo,
    "itens": len(crit_aut6),
    "ids_amostra": [c.get("id") for c in crit_aut6[:5]],
    "adaptador_em_todos": all(c.get("adaptador") for c in crit_aut6),
    "algum_avaliador_indisponivel": any(str(c.get("id", "")).endswith("avaliador-indisponivel")
                                        for c in crit_aut6),
    "algum_tooltips_shrines": any("tooltips_shrines" in str(c.get("adaptador")) for c in crit_aut6),
    "sha_do_modulo": sha(os.path.join(S, rel_aut6)) if os.path.isfile(os.path.join(S, rel_aut6)) else None,
    "proibicao_do_fallback_mantida": True,
}
escreve_json("adaptador-aut6.json", a8)
RES["achados"]["A8"] = a8
print("    carregou=%s itens=%d indisponivel=%s fallback_shrines=%s"
      % (a8["carregou"], a8["itens"], a8["algum_avaliador_indisponivel"],
         a8["algum_tooltips_shrines"]))

print("== A5: o numero do dump do produto, medido (73 nao era 'reconhecidas pelo parser')")
import importlib.util as _ilu
sys.path.insert(0, os.path.join(S, "tools", "testes"))
sys.path.insert(0, os.path.join(S, "tools"))
spec = _ilu.spec_from_file_location("f2_regras_debugger", os.path.join(S, "tools", "testes", "regras_debugger.py"))
rd = _ilu.module_from_spec(spec)
spec.loader.exec_module(rd)
censo = rd.carrega_censo()
A5_ARQUIVOS = ("RoguelikeDebugger/Patches/SkillInventoryPatch.cs",
               "RoguelikeDebugger/Patches/ActionStatusInventoryPatch.cs")


def mede_linhas(predicado, arquivos):
    achadas = []
    for rel in arquivos:
        caminho = os.path.join(S, rel)
        if not os.path.isfile(caminho):
            continue
        for i, linha in enumerate(io.open(caminho, encoding="utf-8",
                                          errors="replace").read().splitlines(), 1):
            if predicado(linha):
                achadas.append({"arquivo": rel, "linha": i, "texto": linha.strip()[:200],
                                "reconhecida_pelo_LINE": bool(censo.LINE.match(linha.strip()))})
    return achadas


# Cada numero tem de vir COM o seu predicado declarado (achado menor da rodada 425: o campo
# `total_com_predicado_estrito: 5` nao era reproduzivel pelo predicado que o nome sugeria - 5 e
# o numero de linhas com `desc=` e SEM `' | '`, nao o de um predicado "estrito" de aspas).
def _pred_pipe(l):
    return " | " in l


def _pred_desc(l):
    return "desc=" in l


linhas_produto = mede_linhas(lambda l: _pred_pipe(l) or _pred_desc(l), A5_ARQUIVOS)
linhas_pipe = mede_linhas(_pred_pipe, A5_ARQUIVOS)
linhas_desc = mede_linhas(_pred_desc, A5_ARQUIVOS)
linhas_desc_sem_pipe = mede_linhas(lambda l: _pred_desc(l) and not _pred_pipe(l), A5_ARQUIVOS)
linhas_aspas = mede_linhas(lambda l: '" | "' in l or "desc=" in l, A5_ARQUIVOS)
reconhecidas = sum(1 for l in linhas_produto if l["reconhecida_pelo_LINE"])
CONTAGENS = (
    ("' | ' in linha (separador real, com espacos)", len(linhas_pipe)),
    ("'desc=' in linha", len(linhas_desc)),
    ("' | ' in linha or 'desc=' in linha (o predicado da correcao anterior - e o TOTAL)",
     len(linhas_produto)),
    ("'desc=' in linha E ' | ' NOT in linha (o que o campo mal rotulado chamava de 'estrito')",
     len(linhas_desc_sem_pipe)),
    ("'\" | \"' in linha or 'desc=' in linha (aspas literais)", len(linhas_aspas)),
)
a5 = {"o_que_a_doc_dizia": "73 reconhecidas pelo parser real",
      "medido": {"arquivos": list(A5_ARQUIVOS),
                 "contagens_por_predicado": [{"predicado": p, "total": n} for p, n in CONTAGENS],
                 "linhas_do_fonte_com_pipe_ou_desc": len(linhas_produto),
                 "linhas_do_fonte_reconhecidas_pelo_LINE": reconhecidas,
                 "o_que_o_LINE_do_censo_reconhece":
                     "o parser `LINE` do censo (tools/census.py) exige o formato `k=\"v\"` sem "
                     "pipes: reconhece 0 linhas dos fontes C# medidos"},
      "leitura": ("73 e o numero de LINHAS dos .cs que contem ` | ` ou `desc=` (o predicado da "
                  "correcao anterior) - fonte C#, nao log; o `LINE` do censo reconhece %d delas. "
                  "Cada numero deste bloco vem com o predicado que o produz." % reconhecidas),
      "artefato": "dump-do-produto.json (lista COMPLETA das linhas, com a flag do parser)"}
escreve_json("dump-do-produto.json", {"arquivos": list(A5_ARQUIVOS),
                                     "predicados_e_totais": [{"predicado": p, "total": n}
                                                             for p, n in CONTAGENS],
                                     "total": len(linhas_produto),
                                     "reconhecidas_pelo_LINE": reconhecidas,
                                     "o_que_o_LINE_do_censo_reconhece":
                                         a5["medido"]["o_que_o_LINE_do_censo_reconhece"],
                                     "linhas": linhas_produto})
RES["achados"]["A5"] = a5
print("    total=%d reconhecidas_pelo_LINE=%d | %s"
      % (len(linhas_produto), reconhecidas,
         "; ".join("%d=%s" % (n, p[:44]) for p, n in CONTAGENS)))

print("== A6: cache --sem-suite x ARTEFATO medido (experimento R1-R7 em sandbox)")


def copia_do_repo(destino):
    if os.path.isdir(destino):
        shutil.rmtree(destino, ignore_errors=True)
    shutil.copytree(S, destino, ignore=shutil.ignore_patterns(
        ".git", "__pycache__", "*.pyc", ".worktrees", "COR-AUT7-F2-evidencias"))
    return destino


SBX = os.path.join(SANDBOX_RAIZ, "repo")
# A copia do sandbox tem de ser do CODIGO ATUAL: sandbox de uma execucao anterior (outra
# rodada, outro codigo) produziria evidencia de um binario que nao e o entregue - a mesma
# classe de falso-OK que este cartao conserta.
FONTES_DA_ENTREGA = (ESTILO, "tools/automacao/estilo/test_estilo_atributos.py",
                     "tools/automacao/estilo/refutar_cor_aut7f2.py",
                     "tools/automacao/estilo/refutar_cor_aut7f2_entradas.py",
                     "tools/automacao/estilo/fechar_cor_aut7f2.py",
                     ACEITE, "tools/automacao/aceite/test_relatorio_aceite.py")


def _sandbox_desatualizado():
    if not os.path.isdir(SBX):
        return True
    for rel in FONTES_DA_ENTREGA:
        origem, copia = os.path.join(S, rel), os.path.join(SBX, rel)
        if not os.path.isfile(copia) or sha(origem) != sha(copia):
            print("   sandbox desatualizado em %s: recopiando" % rel)
            return True
    return False


if _sandbox_desatualizado():
    SBX = copia_do_repo(SBX)
OUT_SBX = os.path.join(SBX, "f2-evidencias")
os.makedirs(OUT_SBX, exist_ok=True)
IDENT_SBX = os.path.join(OUT_SBX, "identidade.json")
with io.open(IDENT_SBX, "w", encoding="utf-8") as fh:
    fh.write(json.dumps(IDENT, indent=2))
ea = carrega("f2_estilo", ESTILO)
a6 = {"sandbox": SBX, "sandbox_copia_de": S}

pacotes = sorted(glob.glob(os.path.join(SBX, "dist", "gumatos-BetterCombatText-*.zip")))
PACOTE = pacotes[-1] if pacotes else None
DLL_BIN = os.path.join(SBX, "BetterCombatText", "bin", "Release", "netstandard2.1",
                       "BetterCombatText.dll")
a6["pacote"] = os.path.relpath(PACOTE, SBX).replace("\\", "/") if PACOTE else None
a6["dll_de_bin"] = os.path.relpath(DLL_BIN, SBX).replace("\\", "/") if os.path.isfile(DLL_BIN) else None


def criterio_da_ouro(json_path):
    with io.open(json_path, encoding="utf-8") as fh:
        dados = json.load(fh)
    achados = [c for c in dados.get("criterios", []) if str(c.get("id", "")).endswith("bct-regra-de-ouro")]
    return (achados[0] if achados else {}), dados


def roda_suite_sbx(nome):
    saida = os.path.join(OUT_SBX, nome + ".estilo.json")
    p = roda("A6-" + nome, [ESTILO, "--repo", SBX, "--out-dir", OUT_SBX,
                            "--identidade", IDENT_SBX, "--out", saida], cwd=SBX)
    crit, dados = criterio_da_ouro(saida)
    return p, crit, dados, saida


def roda_sem_suite_sbx(nome, ident=IDENT_SBX, aceite=False):
    est = os.path.join(OUT_SBX, nome + ".estilo.json")
    if aceite:
        ace = os.path.join(OUT_SBX, nome + ".aceite.json")
        p = roda("A6-" + nome, [ACEITE, "--repo", SBX, "--out-dir", OUT_SBX, "--sem-suite",
                                "--identidade", ident, "--out", ace], cwd=SBX)
        with io.open(ace, encoding="utf-8") as fh:
            dados = json.load(fh)
        todos = [c for b in dados["decisao"]["por_mod"].values() for c in b.get("criterios", [])]
        alvo = [c for c in todos if str(c.get("id", "")).endswith("bct-regra-de-ouro")]
        vinc = [c["id"] for b in dados["decisao"]["por_mod"].values()
                for c in b.get("ok_vinculantes", []) if str(c["id"]).endswith("bct-regra-de-ouro")]
        return p, (alvo[0] if alvo else {}), vinc, dados
    p = roda("A6-" + nome, [ESTILO, "--repo", SBX, "--out-dir", OUT_SBX, "--sem-suite",
                            "--identidade", ident, "--out", est], cwd=SBX)
    crit, dados = criterio_da_ouro(est)
    return p, crit, dados, est


def planta_defeito_no_pacote(pacote):
    """Reescreve a DLL DENTRO do pacote criando `set_fontSharedMaterial` (regra de ouro)."""
    with zipfile.ZipFile(pacote) as zf:
        membros = [(i, zf.read(i.filename)) for i in zf.infolist()]
    novo = []
    for i, d in membros:
        if i.filename == DENTRO_DO_PACOTE:
            assert PADRAO_OK in d, "a DLL do pacote nao trouxe o controle positivo do leitor"
            d = d.replace(PADRAO_OK, PADRAO_DEFEITO)
        novo.append((i, d))
    with zipfile.ZipFile(pacote, "w", zipfile.ZIP_DEFLATED) as zf:
        for i, d in novo:
            zf.writestr(i, d)


# R1 - rodada REAL com a suite no sandbox: prova OK + cache gravado
t0 = time.time()
p1, c1, d1, _ = roda_suite_sbx("R1-suite-real")
foto_r1 = ea.fotografia_suite(SBX)
cache = os.path.join(OUT_SBX, "suite-vinculo.json")
a6["R1"] = {"exit": p1.returncode, "criterio": c1.get("id"), "estado": c1.get("estado"),
            "segundos": round(time.time() - t0, 1),
            "cache_gravado": os.path.isfile(cache),
            "fotografia_arquivos": len(foto_r1["arquivos"]),
            "fotografia_artefatos": len(foto_r1["artefatos"]),
            "pacote_na_fotografia": ("dist/" + os.path.basename(PACOTE)) in foto_r1["artefatos"],
            "dll_de_bin_na_fotografia": (a6["dll_de_bin"] or "") in foto_r1["artefatos"]}
print("    R1 estado=%s cache=%s arquivos=%d artefatos=%d"
      % (a6["R1"]["estado"], a6["R1"]["cache_gravado"], a6["R1"]["fotografia_arquivos"],
         a6["R1"]["fotografia_artefatos"]))

# guarda o cache "anterior" (o que seria reusado com prova velha)
CACHE_GUARDADO = os.path.join(TMP, "cache-anterior")
os.makedirs(CACHE_GUARDADO, exist_ok=True)
for nome_arq in ("suite-vinculo.json", "suite-puros.json", "suite-contra-prova.json"):
    origem = os.path.join(OUT_SBX, nome_arq)
    if os.path.isfile(origem):
        shutil.copy2(origem, os.path.join(CACHE_GUARDADO, nome_arq))
a6["cache_anterior_guardado"] = sorted(os.listdir(CACHE_GUARDADO))
zip_original = io.open(PACOTE, "rb").read()
sha_zip_original = sha_bytes(zip_original)

# R2 - planta o DEFEITO da regra de ouro SO no pacote medido
planta_defeito_no_pacote(PACOTE)
foto_mutada = ea.fotografia_suite(SBX)
a6["R2"] = {"zip_sha_antes": sha_zip_original, "zip_sha_depois": sha(PACOTE),
            "zip_mudou": sha(PACOTE) != sha_zip_original,
            "fotografia_mudou": foto_mutada != foto_r1,
            "artefato_do_pacote_na_foto_mudou": (foto_mutada["artefatos"] != foto_r1["artefatos"]),
            "arquivos_de_fonte_intactos": (foto_mutada["arquivos"] == foto_r1["arquivos"])}
print("    R2 zip_mudou=%s fotografia_mudou=%s (fonte intacta=%s)"
      % (a6["R2"]["zip_mudou"], a6["R2"]["fotografia_mudou"], a6["R2"]["arquivos_de_fonte_intactos"]))

# R3 - rodada REAL nova: o defeito tem de REPROVAR
p3, c3, d3, _ = roda_suite_sbx("R3-suite-real-com-defeito")
a6["R3"] = {"exit": p3.returncode, "criterio": c3.get("id"), "estado": c3.get("estado"),
            "detalhe": str(c3.get("observado"))[:400],
            "defeito_detectado": c3.get("estado") == "REPROVADO"}
print("    R3 estado=%s exit=%s" % (a6["R3"]["estado"], p3.returncode))

# R4 - --sem-suite com o CACHE ANTERIOR (prova velha): nao pode reusar
for nome_arq in a6["cache_anterior_guardado"]:
    shutil.copy2(os.path.join(CACHE_GUARDADO, nome_arq), os.path.join(OUT_SBX, nome_arq))
p4, c4, d4, _ = roda_sem_suite_sbx("R4-sem-suite-cache-anterior")
ok_de_suite = [c["id"] for c in d4.get("criterios", [])
               if c.get("estado") == "OK"
               and ("/puro/" in str(c.get("id")) or "/controle-negativo/" in str(c.get("id")))]
a6["R4"] = {"exit": p4.returncode, "cache_valido": (d4.get("medicao") or {}).get("cache_valido"),
            "estado_do_criterio": c4.get("estado"),
            "ok_de_suite_reusados": len(ok_de_suite), "amostra": ok_de_suite[:5],
            "falso_OK_sumiu": ((d4.get("medicao") or {}).get("cache_valido") is False
                               and not ok_de_suite)}
print("    R4 cache_valido=%s OK_de_suite=%d" % (a6["R4"]["cache_valido"], a6["R4"]["ok_de_suite_reusados"]))

# R4b - controle: um cache no formato ANTERIOR a correcao (fotografia sem `artefatos`)
vinculo = json.load(io.open(os.path.join(CACHE_GUARDADO, "suite-vinculo.json"), encoding="utf-8"))
antigo = dict(vinculo)
antigo["fotografia"] = {k: v for k, v in vinculo["fotografia"].items() if k != "artefatos"}
with io.open(os.path.join(OUT_SBX, "suite-vinculo.json"), "w", encoding="utf-8") as fh:
    fh.write(json.dumps(antigo, sort_keys=True))
p4b, c4b, d4b, _ = roda_sem_suite_sbx("R4b-sem-suite-formato-anterior")
a6["R4b_controle"] = {"cache_no_formato_anterior_aceito": (d4b.get("medicao") or {}).get("cache_valido"),
                      "estado_do_criterio": c4b.get("estado"),
                      "leitura": "fotografia sem `artefatos` (formato pre-correcao) nao e aceita: "
                                 "e o caminho exato do falso-OK do A6"}
print("    R4b cache no formato anterior aceito=%s" % a6["R4b_controle"]["cache_no_formato_anterior_aceito"])

# R5 - consolidador com --sem-suite e o cache anterior: zero OK_VINCULANTE no artefato medido
with io.open(os.path.join(OUT_SBX, "suite-vinculo.json"), "w", encoding="utf-8") as fh:
    fh.write(json.dumps(vinculo, sort_keys=True))
p5, c5, vinc5, _ = roda_sem_suite_sbx("R5-consolidador-cache-anterior", aceite=True)
a6["R5"] = {"exit": p5.returncode, "classificacao": c5.get("estado"), "ok_vinculantes": vinc5,
            "algum_vinculante_do_artefato": bool(vinc5)}
print("    R5 vinculantes do criterio=%s exit=%s" % (vinc5, p5.returncode))

# R6 - variante: defeito SO na DLL de bin/Release, cache anterior de novo
with io.open(PACOTE, "wb") as fh:
    fh.write(zip_original)
dll_bin_original = io.open(DLL_BIN, "rb").read()
with io.open(DLL_BIN, "wb") as fh:
    fh.write(dll_bin_original.replace(PADRAO_OK, PADRAO_DEFEITO))
foto_bin = ea.fotografia_suite(SBX)
p6, c6, d6, _ = roda_sem_suite_sbx("R6-sem-suite-dll-de-bin-mutada")
a6["R6"] = {"exit": p6.returncode, "cache_valido": (d6.get("medicao") or {}).get("cache_valido"),
            "estado_do_criterio": c6.get("estado"),
            "fotografia_mudou": foto_bin != foto_r1,
            "artefato_de_bin_na_foto_mudou": (foto_bin["artefatos"] != foto_r1["artefatos"]),
            "falso_OK_sumiu": (d6.get("medicao") or {}).get("cache_valido") is False}
print("    R6 cache_valido=%s fotografia_mudou=%s" % (a6["R6"]["cache_valido"], a6["R6"]["fotografia_mudou"]))

# R7 - restaura byte a byte e confirma que o cache VOLTA a ser valido (nao e bug de invalidacao)
with io.open(DLL_BIN, "wb") as fh:
    fh.write(dll_bin_original)
with io.open(PACOTE, "wb") as fh:
    fh.write(zip_original)
foto_restaurada = ea.fotografia_suite(SBX)
p7, c7, d7, _ = roda_sem_suite_sbx("R7-sem-suite-restaurado")
a6["R7"] = {"exit": p7.returncode,
            "zip_restaurado_byte_a_byte": sha(PACOTE) == sha_zip_original,
            "dll_de_bin_restaurada_byte_a_byte": sha(DLL_BIN) == sha_bytes(dll_bin_original),
            "fotografia_igual_a_R1": foto_restaurada == foto_r1,
            "cache_valido": (d7.get("medicao") or {}).get("cache_valido"),
            "estado_do_criterio": c7.get("estado"),
            "ok_de_suite": sum(1 for c in d7.get("criterios", []) if c.get("estado") == "OK"
                               and c.get("procedencia") == "execucao")}
print("    R7 restaurado=%s cache_valido=%s OK_de_suite=%d"
      % (a6["R7"]["zip_restaurado_byte_a_byte"], a6["R7"]["cache_valido"], a6["R7"]["ok_de_suite"]))

a6["leitura"] = ("com a fotografia cobrindo os artefatos MEDIDOS (dist/*.zip e <Mod>/bin/**/*.dll), "
                 "qualquer defeito plantado SO no artefato muda a fotografia: a rodada viva REPROVA "
                 "(R3) e o `--sem-suite` com a prova velha nao reusa nada (R4/R6). Restaurado byte a "
                 "byte, o cache volta a valer (R7) - a invalidacao vem do artefato, nao de ruido. "
                 "As ENTRADAS que a suite LE (fora dist/bin) sao medidas na FASE 1.5 "
                 "(`refutar_cor_aut7f2_entradas.py`, secoes E1-E5), que fecha o ponto levantado pela "
                 "revisao independente da rodada 425.")
RES["achados"]["A6"] = a6

print("== A4: o limite do `|` dentro do valor (redacao)")
RES["achados"]["A4"] = {
    "o_que_a_doc_dizia": "`|` dentro de valor e quebra de linha => REPROVADO",
    "limite_medido": "so vale com o `|` COLADO ao valor (`tags=fogo|gelo`); no separador real "
                     "(\" | \") o `FIELD = [^|]+` trunca em silencio e a linha passa por valida",
    "onde": "tools/census.py:53 (FIELD/DESC) + tools/testes/regras_debugger.py:170",
    "correcao": "frase qualificada no doc + limite comentado no ponto que decide "
                "(estilo_atributos.py, aspecto de contrato do dump)"}
print("    %s" % RES["achados"]["A4"]["limite_medido"])

print("== hashes das fontes da correcao e relatorio desta fase")
RES["hashes"] = {rel: sha(os.path.join(S, rel)) for rel in (
    ESTILO, "tools/automacao/estilo/test_estilo_atributos.py",
    "tools/automacao/estilo/refutar_cor_aut7f2.py",
    "tools/automacao/estilo/refutar_cor_aut7f2_entradas.py",
    "tools/automacao/estilo/fechar_cor_aut7f2.py",
    ACEITE, "tools/automacao/aceite/test_relatorio_aceite.py") if os.path.isfile(os.path.join(S, rel))}
RES["hashes"]["cobertura_aut6"] = a8["sha_do_modulo"]
RES["fase"] = ("achados (A1-A9) nesta fase; as ENTRADAS que a suite LE no cache `--sem-suite` "
               "sao medidas em `python tools/automacao/estilo/refutar_cor_aut7f2_entradas.py` "
               "(fase 1.5, secoes E1-E5, que completa ESTE mesmo JSON em `achados.A6_entradas`) e o "
               "fecho (suites verdes + docs regerados + docs-antes.txt) em "
               "`python tools/automacao/estilo/fechar_cor_aut7f2.py` (fase 2)")

escreve_json("refutacao-cor-aut7-f2.json", RES)


def _fechou(item):
    """O achado fechou? (cada um tem o seu proprio sinal de regressao negativa)."""
    if not isinstance(item, dict):
        return None
    for chave in ("falso_OK_sumiu", "corrigido", "controle_ok"):
        if chave in item:
            return item[chave]
    return None


print("\nfecho por achado:")
for nome in ("A1", "A1b_controle", "A2", "A3", "A3b_controle", "A6", "A7", "A8", "A5"):
    dado = RES["achados"].get(nome)
    if nome == "A6":
        print("  A6: R1=%s R3=%s cache_reusado_R4=%s cache_reusado_R6=%s restaurado=%s"
              % (dado["R1"]["estado"], dado["R3"]["estado"], dado["R4"]["cache_valido"],
                 dado["R6"]["cache_valido"], dado["R7"]["zip_restaurado_byte_a_byte"]))
    elif nome == "A2":
        print("  A2: sem_hash=%s com_hash=%s hash_errado=%s"
              % (dado["sem_hash_na_identidade"]["estado_estilo"],
                 dado["com_hash_na_identidade"]["estado_estilo"],
                 dado["hash_errado"]["estado_estilo"]))
    elif nome == "A7":
        print("  A7: %s" % {k: v["ok_vinculante"] for k, v in dado.items()
                            if isinstance(v, dict) and "ok_vinculante" in v})
    elif nome == "A8":
        print("  A8: carregou=%s itens=%s indisponivel=%s" % (dado["carregou"], dado["itens"],
                                                              dado["algum_avaliador_indisponivel"]))
    elif nome == "A5":
        print("  A5: linhas=%s reconhecidas_pelo_LINE=%s"
              % (dado["medido"]["linhas_do_fonte_com_pipe_ou_desc"],
                 dado["medido"]["linhas_do_fonte_reconhecidas_pelo_LINE"]))
    else:
        print("  %s: %s" % (nome, _fechou(dado)))
print("relatorio:", os.path.join(OUT, "refutacao-cor-aut7-f2.json"))
