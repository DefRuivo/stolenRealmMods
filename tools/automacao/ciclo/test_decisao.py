#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_decisao.py - CIC-2: testes REAIS da consolidacao de decisao + roteiro humano.

Prova por COMPORTAMENTO (nao por leitura do codigo do autor):

  * fiacao: `consolidar()` devolve por_mod / falhas_automaticas /
    pendencias_humanas / pronto_para_decisao / aceite_humano / publicacao;
  * NUNCA OK por rotulo: fixture, evidencia ausente, hash de bytes antigos,
    identidade insuficiente e CADEIA DE PROVA RUNTIME incompleta NAO viram prova;
  * contrato positivo de runtime (CICLO-VALIDACAO-escopo.md, secao "Correcoes
    funcionais da primeira integracao"): `prova_runtime=true`, `sessao`,
    `fonte_sha`, `dll_sha` (+ `config_sha` quando config relevante) e evidencia
    atual/manifest coerente - tudo CONFRONTADO com a identidade da coleta, nunca
    aceito so por um rotulo `runtime`. `prova_runtime=false` NUNCA vincula.
  * lacuna de probe/campo/coleta/preparacao e falha AUTOMATIZAVEL (fila de
    agente); SO `autorizacao_necessaria=true`, `tipo_pendencia=autorizacao` ou
    `julgamento_visual` explicito vao ao dono - nao se manda todo runtime
    ausente ao humano por padrao;
  * a instrucao ESPECIFICA (`julgamento_humano`/`instrucoes_humanas`) e
    preservada no roteiro;
  * pronto_para_decisao, aceite_humano e publicacao sao estados SEPARADOS;
  * a CLI real (subprocesso) le criterios JSON e devolve o exit code certo.

Exit: 0 = tudo passou; 1 = reprovou; 2 = nao consegui rodar.
Uso:  python tools/automacao/ciclo/test_decisao.py
Contra-prova (mutante): CIC2_DECISAO=<copia> python .../test_decisao.py
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
CAMINHO_MODULO = os.environ.get("CIC2_DECISAO") or os.path.join(AQUI, "decisao.py")
PY = sys.executable
RESULTADOS = []
FALHAS = []


def checar(nome, cond, detalhe=""):
    cond = bool(cond)
    RESULTADOS.append((nome, cond, detalhe))
    if not cond:
        FALHAS.append(nome)
    print("RESULTADO|%s|%s|%s" % ("PASSOU" if cond else "REPROVOU", nome, detalhe))
    return cond


def carregar():
    spec = importlib.util.spec_from_file_location("cic2_decisao_test", CAMINHO_MODULO)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


# --------------------------------------------------------------- area segura

def area_scratch():
    for cand in (os.environ.get("BH_AGENT_WORKSPACE"), os.environ.get("TMPDIR"),
                 os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes", "cache", "scratch")):
        if not cand:
            continue
        try:
            os.makedirs(cand, exist_ok=True)
        except OSError:
            continue
        if os.path.isdir(cand):
            return cand
    return tempfile.gettempdir()


# --------------------------------------------------------------- construtores

def crit(cid, mod="BetterTooltips", estado="OK", classe="offline", procedencia="execucao",
         evidencia=None, **extra):
    c = {"id": cid, "mod": mod, "estado": estado, "classe": classe,
         "procedencia": procedencia, "esperado": "ok", "observado": "ok",
         "evidencia": list(evidencia or []), "motivo": "", "tarefa_origem": "T-test"}
    c.update(extra)
    return c


def ident(fonte="a" * 64, dll="b" * 64, raiz=None, sessao=None, **extra):
    d = {"fonte_sha": fonte, "dll_sha": dll}
    if raiz:
        d["raiz"] = raiz
    if sessao:
        d["sessao"] = sessao
    d.update(extra)
    return d


def crit_runtime(cid, mod="BetterTooltips", estado="OK", evidencia=None, **extra):
    """Criterio de runtime com a CADEIA COMPLETA do contrato positivo (base do caso real)."""
    c = crit(cid, mod=mod, estado=estado, classe="runtime", procedencia="runtime",
             evidencia=evidencia)
    c.update({"prova_runtime": True, "sessao": "s1",
              "fonte_sha": "a" * 64, "dll_sha": "b" * 64})
    c.update(extra)
    return c


def mod_de(dic, nome):
    return dic["por_mod"].get(nome, {})


def cria_evid(base, rel, texto="prova"):
    caminho = os.path.join(base, rel)
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write(texto)
    return caminho


def evid_hash(base, rel, texto="prova"):
    """Evidencia em arquivo EXISTENTE com sha256 DECLARADO (o que o runtime exige)."""
    caminho = cria_evid(base, rel, texto)
    return {"caminho": caminho, "sha256": hashlib.sha256(texto.encode("utf-8")).hexdigest()}


def sha_de(texto):
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


# ============================================================ casos de decisao

def t_sem_criterios(D):
    d = D.consolidar([], ident())
    checar("sem criterios -> nao pronto", d["pronto_para_decisao"] is False)
    checar("sem criterios -> resumo.criterios == 0", d["resumo"]["criterios"] == 0)
    checar("sem criterios -> falhas vazias", d["falhas_automaticas"] == [])
    checar("sem criterios -> contrato presente",
           all(k in d for k in ("por_mod", "falhas_automaticas", "pendencias_humanas",
                                "pronto_para_decisao", "aceite_humano", "publicacao")))
    checar("sem criterios -> aceite NAO_PRONUNCIADO",
           d["aceite_humano"].get("status") == "NAO_PRONUNCIADO")
    checar("sem criterios -> publicacao NAO_VERIFICADO",
           d["publicacao"].get("status") == "NAO_VERIFICADO")


def t_ok_vinculante_offline(D, tmp):
    ev = cria_evid(tmp, "ev/c1.log")
    c = crit("C1", evidencia=[ev])
    d = D.consolidar([c], ident(raiz=tmp))
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("offline real OK -> prova vinculante", it["prova_vinculante"] is True)
    checar("offline real OK -> classificacao OK_VINCULANTE", it["classificacao"] == "OK_VINCULANTE")
    checar("offline real OK -> pronto para decisao", d["pronto_para_decisao"] is True)
    checar("offline real OK -> sem falhas", d["falhas_automaticas"] == [])
    checar("offline real OK -> sem pendencia humana", d["pendencias_humanas"] == [])
    checar("offline real OK -> mod estado OK", mod_de(d, "BetterTooltips")["estado"] == "OK")


def t_ok_runtime_vinculante(D, tmp):
    """Contrato positivo de runtime: prova_runtime+sessao+fonte/dll+evidencia com hash."""
    ev = evid_hash(tmp, "ev/r1.json", "prova-runtime-1")
    c = crit_runtime("R1", evidencia=[ev])
    d = D.consolidar([c], ident(raiz=tmp, sessao="s1"))
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("runtime real OK com cadeia completa -> vinculante", it["prova_vinculante"] is True)
    checar("runtime real OK com cadeia completa -> pronto", d["pronto_para_decisao"] is True)
    checar("runtime real OK com cadeia completa -> sem falhas", d["falhas_automaticas"] == [])


def t_prova_runtime_false_nunca_vinculante(D, tmp):
    """REPRO CIC-2R (achado 3a): OK+runtime com prova_runtime=False NAO pode virar prova."""
    ev = evid_hash(tmp, "ev/r2.json", "evidencia-existente")
    c = crit_runtime("R2R", evidencia=[ev])
    c["prova_runtime"] = False
    d = D.consolidar([c], ident(raiz=tmp, sessao="s1"))
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("CIC2R: prova_runtime=False NUNCA vinculante", it["prova_vinculante"] is False)
    checar("CIC2R: prova_runtime=False -> falha automatica (nao OK_VINCULANTE)",
           it["classificacao"] == "FALHA_AUTOMATICA")
    checar("CIC2R: prova_runtime=False nao vai ao humano", d["pendencias_humanas"] == [])
    checar("CIC2R: prova_runtime=False -> nao pronto", d["pronto_para_decisao"] is False)


def t_runtime_ok_sem_cadeia_nao_vincula(D, tmp):
    """So o rotulo runtime (sem prova_runtime/sessao) NAO fecha OK, mesmo com hashes certos."""
    ev = cria_evid(tmp, "ev/r3.json")
    c = crit("R3", classe="runtime", procedencia="runtime", evidencia=[ev],
             hashes={"fonte_sha": "a" * 64, "dll_sha": "b" * 64})
    d = D.consolidar([c], ident(raiz=tmp))
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("runtime OK sem prova_runtime/sessao -> NAO vinculante", it["prova_vinculante"] is False)
    checar("runtime OK sem cadeia -> falha automatica", it["classificacao"] == "FALHA_AUTOMATICA")
    checar("runtime OK sem cadeia -> nao vai ao humano", d["pendencias_humanas"] == [])
    checar("runtime OK sem cadeia -> motivo nomeia a cadeia",
           "cadeia" in it["motivo_decisao"].lower())


def t_runtime_hash_divergente_nao_vincula(D, tmp):
    """fonte_sha do criterio de OUTRA build: aprovacao anterior invalidada."""
    ev = evid_hash(tmp, "ev/r4.json", "x")
    c = crit_runtime("R4D", evidencia=[ev], fonte_sha="c" * 64)
    d = D.consolidar([c], ident(raiz=tmp, sessao="s1"))     # identidade fonte_sha=a*64
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("runtime com fonte_sha de outra build -> NAO vinculante", it["prova_vinculante"] is False)
    checar("runtime com fonte divergente -> falha automatica", it["classificacao"] == "FALHA_AUTOMATICA")
    checar("runtime com fonte divergente -> nao pronto", d["pronto_para_decisao"] is False)


def t_runtime_sessao_divergente_nao_vincula(D, tmp):
    ev = evid_hash(tmp, "ev/r5.json", "x")
    c = crit_runtime("R5S", evidencia=[ev], sessao="sX")
    d = D.consolidar([c], ident(raiz=tmp, sessao="sY"))
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("runtime com sessao divergente -> NAO vinculante", it["prova_vinculante"] is False)
    checar("runtime com sessao divergente -> falha automatica", it["classificacao"] == "FALHA_AUTOMATICA")


def t_config_relevante_sem_config_sha(D, tmp):
    ev = evid_hash(tmp, "ev/cfg1.json", "x")
    c = crit_runtime("RCFG", evidencia=[ev], config_relevante=True)
    d = D.consolidar([c], ident(raiz=tmp, sessao="s1", artefatos={"config/tooltips.cfg": "d" * 64}))
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("config relevante sem config_sha -> NAO vinculante", it["prova_vinculante"] is False)
    checar("config relevante sem config_sha -> falha automatica", it["classificacao"] == "FALHA_AUTOMATICA")


def t_config_sha_confirmado_vincula(D, tmp):
    ev = evid_hash(tmp, "ev/cfg2.json", "x")
    c = crit_runtime("RCFG2", evidencia=[ev], config_relevante=True, config_sha="d" * 64)
    d = D.consolidar([c], ident(raiz=tmp, sessao="s1", artefatos={"config/tooltips.cfg": "d" * 64}))
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("config_sha confirmado pela identidade -> vinculante", it["prova_vinculante"] is True)


def t_manifest_incoerente_nao_vincula(D, tmp):
    ev = evid_hash(tmp, "ev/m1.json", "conteudo-real")
    c = crit_runtime("RMAN", evidencia=[ev])
    identidade = ident(raiz=tmp, sessao="s1",
                       manifest={"artefatos": [{"arquivo": "m1.json", "sha256": "e" * 64}]})
    d = D.consolidar([c], identidade)
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("evidencia difere do manifest da coleta -> NAO vinculante", it["prova_vinculante"] is False)
    checar("evidencia difere do manifest -> falha automatica", it["classificacao"] == "FALHA_AUTOMATICA")


def t_manifest_coerente_vincula(D, tmp):
    ev = evid_hash(tmp, "ev/m2.json", "conteudo-real")
    c = crit_runtime("RMAN2", evidencia=[ev])
    identidade = ident(raiz=tmp, sessao="s1",
                       manifest={"artefatos": [{"arquivo": "m2.json", "sha256": sha_de("conteudo-real")}]})
    d = D.consolidar([c], identidade)
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("evidencia coerente com o manifest -> vinculante", it["prova_vinculante"] is True)


def t_evidencia_ausente_declarada_sha(D, tmp):
    """Evidencia com sha declarado mas arquivo inexistente: nao fecha."""
    c = crit_runtime("REV", evidencia=[{"caminho": os.path.join(tmp, "nao-existe.json"),
                                        "sha256": "f" * 64}])
    d = D.consolidar([c], ident(raiz=tmp, sessao="s1"))
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("runtime com evidencia ausente -> NAO vinculante", it["prova_vinculante"] is False)
    checar("runtime com evidencia ausente -> falha automatica", it["classificacao"] == "FALHA_AUTOMATICA")


def t_label_ok_sem_evidencia(D):
    c = crit("C2", evidencia=[])
    d = D.consolidar([c], ident())
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("OK sem evidencia -> NAO vinculante", it["prova_vinculante"] is False)
    checar("OK sem evidencia -> falha automatica", it["classificacao"] == "FALHA_AUTOMATICA")
    checar("OK sem evidencia -> nao pronto", d["pronto_para_decisao"] is False)
    checar("OK sem evidencia -> falha nao vai ao humano", d["pendencias_humanas"] == [])


def t_evidencia_ausente(D, tmp):
    c = crit("C3", evidencia=[os.path.join(tmp, "nao-existe.log")])
    d = D.consolidar([c], ident(raiz=tmp))
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("evidencia ausente -> falha automatica", it["classificacao"] == "FALHA_AUTOMATICA")
    checar("evidencia ausente -> prova false", it["prova_vinculante"] is False)
    checar("evidencia ausente -> motivo menciona evidencia",
           "evidencia" in it["motivo_decisao"].lower())
    checar("evidencia ausente -> nao pronto", d["pronto_para_decisao"] is False)


def t_fixture_nunca_prova(D):
    c = crit("F1", classe="runtime", procedencia="fixture", estado="OK", evidencia=["x"],
             prova_runtime=False)
    d = D.consolidar([c], ident())
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("fixture -> NAO_CONTA_COMO_PROVA", it["classificacao"] == "NAO_CONTA_COMO_PROVA")
    checar("fixture -> prova false", it["prova_vinculante"] is False)
    checar("fixture -> nao pronto", d["pronto_para_decisao"] is False)
    checar("fixture sozinha -> falha automatica sintetica (sem prova real)",
           any("sem-prova" in f.get("id", "") for f in d["falhas_automaticas"]))


def t_fixture_reprovada_e_falha(D):
    c = crit("F2", classe="offline", procedencia="fixture", estado="REPROVADO")
    d = D.consolidar([c], ident())
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("fixture REPROVADA -> falha automatica", it["classificacao"] == "FALHA_AUTOMATICA")


def t_hash_stale_reprova(D, tmp):
    ev = cria_evid(tmp, "ev/stale.log")
    c = crit("C4", evidencia=[ev], hashes={"dll_sha": "c" * 64})
    d = D.consolidar([c], ident(raiz=tmp))
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("hash de bytes antigos -> prova false", it["prova_vinculante"] is False)
    checar("hash de bytes antigos -> falha automatica", it["classificacao"] == "FALHA_AUTOMATICA")
    checar("hash de bytes antigos -> motivo de bytes antigos",
           "antig" in it["motivo_decisao"].lower() or "diverg" in it["motivo_decisao"].lower())
    checar("hash de bytes antigos -> nao pronto", d["pronto_para_decisao"] is False)


def t_hash_nao_confirmado(D, tmp):
    ev = cria_evid(tmp, "ev/nc.log")
    c = crit("C5", evidencia=[ev], hashes={"config/tooltips.cfg": "d" * 64})
    d = D.consolidar([c], ident(raiz=tmp))
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("hash nao confirmado pela identidade -> falha automatica",
           it["classificacao"] == "FALHA_AUTOMATICA")
    checar("hash nao confirmado -> nao vinculante", it["prova_vinculante"] is False)


def t_hash_confirmado_ok(D, tmp):
    ev = cria_evid(tmp, "ev/conf.log")
    c = crit("C6", evidencia=[ev], hashes={"config/tooltips.cfg": "d" * 64})
    identidade = ident(raiz=tmp, artefatos={"config/tooltips.cfg": "d" * 64})
    d = D.consolidar([c], identidade)
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("hash de config confirmado -> vinculante", it["prova_vinculante"] is True)


def t_identidade_insuficiente(D, tmp):
    ev = cria_evid(tmp, "ev/id.log")
    c = crit("C7", evidencia=[ev])
    d = D.consolidar([c], {"raiz": tmp})          # sem fonte_sha/dll_sha
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("identidade insuficiente -> prova false", it["prova_vinculante"] is False)
    checar("identidade insuficiente -> falha automatica", it["classificacao"] == "FALHA_AUTOMATICA")
    checar("identidade insuficiente -> nao pronto", d["pronto_para_decisao"] is False)


def t_offline_nao_exercitado_vira_falha(D):
    c = crit("C8", classe="offline", procedencia="execucao", estado="NAO_EXERCITADO")
    d = D.consolidar([c], ident())
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("offline NAO_EXERCITADO -> falha automatica", it["classificacao"] == "FALHA_AUTOMATICA")
    checar("offline NAO_EXERCITADO -> NAO vai ao humano", d["pendencias_humanas"] == [])
    checar("offline NAO_EXERCITADO -> nao pronto", d["pronto_para_decisao"] is False)


def t_runtime_lacuna_tecnica_vai_agente(D):
    """Achado 5a: lacuna de probe/coleta e AUTOMATIZAVEL, nao vai ao dono por padrao."""
    c = crit("RL", classe="runtime", procedencia="runtime", estado="NAO_EXERCITADO",
             lacuna_probe="AUT4Probe atual nao emite snapshot antes/depois")
    d = D.consolidar([c], ident())
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("runtime NE lacuna tecnica -> falha automatica", it["classificacao"] == "FALHA_AUTOMATICA")
    checar("runtime NE lacuna tecnica -> NAO vai ao humano", d["pendencias_humanas"] == [])
    checar("runtime NE lacuna tecnica -> volta na fila de agente",
           any(f["id"] == "RL" for f in d["falhas_automaticas"]))
    checar("runtime NE lacuna tecnica -> nao pronto", d["pronto_para_decisao"] is False)


def t_runtime_autorizacao_explicita_vai_humano(D):
    c = crit("RA", classe="runtime", procedencia="runtime", estado="NAO_EXERCITADO",
             autorizacao_necessaria=True)
    d = D.consolidar([c], ident())
    checar("autorizacao_necessaria=true -> pendencia humana", len(d["pendencias_humanas"]) == 1)
    if d["pendencias_humanas"]:
        p = d["pendencias_humanas"][0]
        checar("autorizacao explicita -> tipo autorizacao", p["tipo"] == "autorizacao")
        checar("autorizacao explicita -> instrucao concreta", bool(p["instrucoes"]))
        checar("autorizacao explicita -> agrega o criterio", "RA" in p["criterios"])
    checar("autorizacao explicita -> sem falha automatica", d["falhas_automaticas"] == [])
    checar("autorizacao explicita -> pronto p/ decisao", d["pronto_para_decisao"] is True)


def t_runtime_tipo_pendencia_julgamento_visual(D):
    c = crit("RJ", classe="runtime", procedencia="runtime", estado="NAO_EXERCITADO",
             tipo_pendencia="julgamento_visual", instrucoes_humanas="conferir a janela em tela")
    d = D.consolidar([c], ident())
    checar("tipo_pendencia=julgamento_visual -> pendencia humana", len(d["pendencias_humanas"]) == 1)
    if d["pendencias_humanas"]:
        p = d["pendencias_humanas"][0]
        checar("tipo_pendencia=julgamento_visual -> tipo julgamento_visual",
               p["tipo"] == "julgamento_visual")
        checar("tipo_pendencia=julgamento_visual -> instrucao preservada",
               "conferir a janela" in (p["instrucoes"] or ""))


def t_runtime_sem_sinal_nao_vai_humano(D):
    """Sem sinal explicito, runtime NE NAO e humano (nao se empurra tudo ao dono)."""
    c = crit("RS", classe="runtime", procedencia="runtime", estado="NAO_EXERCITADO",
             motivo="precisa do LogOutput.log do proximo boot")
    d = D.consolidar([c], ident())
    checar("runtime NE sem sinal -> NAO vai ao humano", d["pendencias_humanas"] == [])
    checar("runtime NE sem sinal -> falha automatica", d["falhas_automaticas"] != [])


def t_runtime_julgamento_visual(D, tmp):
    ev = evid_hash(tmp, "ev/vis.json", "x")
    c = crit_runtime("R3V", evidencia=[ev], julgamento_humano="confirmar layout do tab em tela")
    d = D.consolidar([c], ident(raiz=tmp, sessao="s1"))
    it = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("runtime OK com julgamento -> ainda vinculante", it["prova_vinculante"] is True)
    checar("runtime OK com julgamento -> pendencia humana visual",
           len(d["pendencias_humanas"]) == 1 and d["pendencias_humanas"][0]["tipo"] == "julgamento_visual")
    checar("runtime OK com julgamento -> pronto", d["pronto_para_decisao"] is True)


def t_instrucao_especifica_preservada(D, tmp):
    """Achado 5b: a instrucao ESPECIFICA de julgamento_humano nao pode ser perdida."""
    ev = evid_hash(tmp, "ev/v2.json", "x")
    texto = "CONFIRMAR o layout do tab X na tela (ESPECIFICA)"
    c = crit_runtime("V2", evidencia=[ev], julgamento_humano=texto)
    d = D.consolidar([c], ident(raiz=tmp, sessao="s1"))
    roteiro = d["roteiro_humano"]["itens"]
    crit_norm = d["por_mod"]["BetterTooltips"]["criterios"][0]
    checar("julgamento visual -> pendencia humana", len(d["pendencias_humanas"]) == 1)
    checar("instrucao especifica preservada no criterio normalizado",
           crit_norm.get("julgamento_humano") == texto)
    checar("instrucao especifica aparece no roteiro",
           any(texto in (i.get("instrucoes") or "") for i in roteiro))
    checar("prova tecnica ainda vinculante", crit_norm["prova_vinculante"] is True)


def t_reprovado_vira_falha(D):
    c = crit("C9", estado="REPROVADO", classe="offline", procedencia="execucao")
    d = D.consolidar([c], ident())
    checar("REPROVADO -> falha automatica",
           d["por_mod"]["BetterTooltips"]["criterios"][0]["classificacao"] == "FALHA_AUTOMATICA")
    checar("REPROVADO -> mod estado REPROVADO",
           mod_de(d, "BetterTooltips")["estado"] == "REPROVADO")
    checar("REPROVADO -> nao pronto", d["pronto_para_decisao"] is False)


def t_por_mod_resume(D):
    cs = [crit("C10", mod="BetterTooltips", evidencia=[]),           # falha
          crit("R4", mod="RSTV", classe="runtime", procedencia="runtime",
               estado="NAO_EXERCITADO", autorizacao_necessaria=True)]  # pendencia humana
    d = D.consolidar(cs, ident())
    checar("por_mod separa os mods", set(d["por_mod"]) == {"BetterTooltips", "RSTV"})
    checar("por_mod BetterTooltips com falha", len(mod_de(d, "BetterTooltips")["falhas_automaticas"]) == 1)
    checar("por_mod RSTV com pendencia", len(mod_de(d, "RSTV")["pendencias_humanas"]) == 1)


def t_nao_joga_falha_automatizavel_no_humano(D):
    cs = [crit("OFF", classe="offline", procedencia="execucao", estado="NAO_EXERCITADO"),
          crit("RUN", mod="RSTV", classe="runtime", procedencia="runtime", estado="NAO_EXERCITADO",
               autorizacao_necessaria=True)]
    d = D.consolidar(cs, ident())
    ids_humano = {i for p in d["pendencias_humanas"] for i in p["criterios"]}
    checar("offline NE nao aparece no roteiro humano", "OFF" not in ids_humano)
    checar("autorizacao explicita aparece no roteiro humano", "RUN" in ids_humano)
    checar("offline NE vira falha automatica",
           any(f["id"] == "OFF" for f in d["falhas_automaticas"]))


def t_aceite_publicacao_separados(D):
    c = crit("C11", estado="REPROVADO")
    d = D.consolidar([c], ident(), aceite_humano={"BetterTooltips": {"aceito": True, "por": "dono"}})
    checar("aceite pronunciado", d["aceite_humano"].get("pronunciado") is True)
    checar("aceite NAO muda pronto_para_decisao", d["pronto_para_decisao"] is False)
    checar("aceite com falha -> inconsistente",
           "BetterTooltips" in d.get("aceite_inconsistente", []))
    checar("publicacao continua NAO_VERIFICADO", d["publicacao"]["status"] == "NAO_VERIFICADO")


def t_roteiro_humano_curto(D, tmp):
    ev = evid_hash(tmp, "ev/v1.json", "x")
    cs = [crit("A1", mod="M1", classe="runtime", procedencia="runtime", estado="NAO_EXERCITADO",
               autorizacao_necessaria=True),
          crit("A2", mod="M1", classe="runtime", procedencia="runtime", estado="NAO_EXERCITADO",
               autorizacao_necessaria=True),
          crit_runtime("V1", mod="M2", evidencia=[ev], julgamento_humano="confirmar aparencia")]
    d = D.consolidar(cs, ident(raiz=tmp, sessao="s1"))
    roteiro = d["roteiro_humano"]["itens"]
    chaves = {(i["mod"], i["tipo"]) for i in roteiro}
    checar("roteiro agrega por mod+tipo", chaves == {("M1", "autorizacao"), ("M2", "julgamento_visual")})
    checar("roteiro tem no maximo 1 item por mod+tipo", len(roteiro) == 2)
    checar("roteiro autorizacao conta 2 criterios",
           [i for i in roteiro if i["tipo"] == "autorizacao"][0]["total"] == 2)
    checar("roteiro nao e o checklist completo (menos itens que criterios)",
           len(roteiro) < len(cs))


def t_criterio_malformado(D):
    cs = [{"id": "X1"}]           # faltando estado/classe/procedencia
    d = D.consolidar(cs, ident())
    it = d["por_mod"]["transversal"]["criterios"][0]
    checar("malformado -> falha automatica", it["classificacao"] == "FALHA_AUTOMATICA")
    checar("malformado -> nao pronto", d["pronto_para_decisao"] is False)


def t_cadeia_residual_integracao(D, tmp):
    """Buraco de cadeia que NAO fecha + os DOIS limites do contrato dos produtores.

    Fecha: hash de cadeia que a identidade conhece e diverge (o criterio nao pode se
    auto-absolver por um bloco aninhado). NAO fecha por decisao de contrato (e o
    criterio NAO pode ser endurecido aqui sem quebrar CIC-3/CIC-4): identidade sem
    `sessao` (contrato CIC-2-correcao.md regra 2: confronto "quando ela declara") e
    evidencia como caminho do artefato lido, sem sha por arquivo (o adaptador CIC-4
    emite assim). Os dois ficam PINADOS abaixo para ninguem aperta-los em silencio.
    """
    ev = evid_hash(tmp, "ev/integracao.json", "coleta-de-teste")
    base = crit_runtime("CADEIA", evidencia=[ev])
    for nome, c, i in (
        ("hash de cadeia aninhado divergente", crit_runtime("NESTED", evidencia=[ev],
            fonte_sha=None, cadeia={"fonte_sha": "c" * 64}), ident(raiz=tmp, sessao="s1")),
        # Isola a regra do MANIFEST: a coleta diz o sha REAL (bate com o disco) e o
        # criterio declara outro sha para o MESMO arquivo. Sem a regra, o manifest do
        # criterio sobrescreveria o da coleta e o criterio se absolveria sozinho.
        ("manifest do criterio nao sobrescreve o da coleta", dict(base, manifest={"artefatos": [
            {"arquivo": "integracao.json", "sha256": "e" * 64}]}), ident(raiz=tmp, sessao="s1",
            manifest={"artefatos": [{"arquivo": "integracao.json", "sha256": ev["sha256"]}]})),
    ):
        d = D.consolidar([c], i)
        checar(nome + " -> falha tecnica (nao OK)", bool(d["falhas_automaticas"])
               and not d["pronto_para_decisao"])

    # (pin) identidade sem sessao: o contrato com os produtores diz "confrontar quando a
    # identidade declara" - endurecer aqui reprovaria a rodada dos produtores reais.
    d = D.consolidar([base], ident(raiz=tmp))
    checar("CONTRATO: identidade sem sessao ainda vincula (CIC-2-correcao.md regra 2)",
           d["resumo"]["ok_vinculantes"] == 1 and not d["falhas_automaticas"])
    # (pin) evidencia como caminho do artefato lido (formato dos adaptadores CIC-3/4).
    d = D.consolidar([crit_runtime("PATH", evidencia=[ev["caminho"]])], ident(raiz=tmp, sessao="s1"))
    checar("CONTRATO: evidencia por caminho do artefato lido ainda vincula",
           d["resumo"]["ok_vinculantes"] == 1 and not d["falhas_automaticas"])

    cs = [crit_runtime("VIS-A", evidencia=[ev], julgamento_humano="Confirmar contraste da janela"),
          crit_runtime("VIS-B", evidencia=[ev], julgamento_humano="Confirmar sobreposicao do tooltip")]
    d = D.consolidar(cs, ident(raiz=tmp, sessao="s1"))
    itens = d["roteiro_humano"]["itens"]
    checar("agregacao preserva as DUAS instrucoes no roteiro",
           len(itens) == 1 and all(c["julgamento_humano"] in itens[0]["instrucoes"] for c in cs))
    checar("agregacao mantem rastreio por criterio",
           all(itens[0]["instrucoes_por_criterio"].get(c["id"]) == c["julgamento_humano"] for c in cs))

    # Reuso dos produtores reais: nenhuma lacuna de coleta deve ir ao dono;
    # criterio positivo com caminhos do artefato usa o manifest AUT-4 como hash da evidencia.
    cenarios = os.path.join(os.path.dirname(AQUI), "cenarios")
    for nome in ("rstv", "tooltips_shrines"):
        spec = importlib.util.spec_from_file_location("cic2_integracao_" + nome,
            os.path.join(cenarios, nome + ".py"))
        produtor = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(produtor)
        i = ident(raiz=tmp, sessao="s1")
        cs = produtor.avaliar([], i)
        d = D.consolidar(cs, i)
        checar(nome + " real sem coleta -> somente agentes", bool(d["falhas_automaticas"])
            and not d["pendencias_humanas"] and not d["pronto_para_decisao"])

    spec = importlib.util.spec_from_file_location("cic2_aut4", os.path.join(
        os.path.dirname(AQUI), "runtime", "coletor.py"))
    coletor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(coletor)
    # Convencao do produtor CIC-3 (rstv.py `_ALIAS_HASH`): o `hash_fonte` do coletor
    # CIC-5 e o sha da DLL, entao uma rodada coerente declara hash_fonte == dll_sha.
    i = ident(raiz=tmp, sessao="s1", manifest=coletor.montar_manifest(tmp, [ev["caminho"]]))
    obs = [{"procedencia": "runtime", "sessao": "s1", "hash_fonte": "b" * 64,
            "texto_renderizado": "Deals 15 damage", "evidencia": [ev["caminho"]]}]
    spec = importlib.util.spec_from_file_location("cic2_rstv_positivo", os.path.join(cenarios, "rstv.py"))
    produtor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(produtor)
    cs = [c for c in produtor.avaliar(obs, i) if c["id"] == "RSTV-26-placeholders"]
    d = D.consolidar(cs, i)
    checar("RSTV real + manifest AUT4 -> positivo do contrato", d["pronto_para_decisao"]
        and not d["falhas_automaticas"])
    cria_evid(tmp, "ev/integracao.json", "bytes-alterados")
    d = D.consolidar(cs, i)
    checar("mesma rodada apos alterar a evidencia -> nao pronto", bool(d["falhas_automaticas"])
        and not d["pronto_para_decisao"])


# ==================================================================== CLI real

def _roda_cli(args, env_extra=None):
    env = dict(os.environ)
    env["PYTHONIOENCODING"] = "utf-8"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if env_extra:
        env.update(env_extra)
    return subprocess.run([PY, CAMINHO_MODULO] + args, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, universal_newlines=True,
                          encoding="utf-8", env=env, timeout=120)


def _escreve_json(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as fh:
        json.dump(dados, fh, ensure_ascii=False)


def t_cli_real_positivo(tmp):
    repo = os.path.join(tmp, "cli_pos")
    ev = cria_evid(repo, "ev/cli.log")
    crits = [crit("CLI1", evidencia=[os.path.relpath(ev, repo).replace("\\", "/")],
                  hashes={"fonte_sha": "a" * 64})]
    arq_c = os.path.join(repo, "criterios.json")
    arq_i = os.path.join(repo, "identidade.json")
    _escreve_json(arq_c, crits)
    _escreve_json(arq_i, {"fonte_sha": "a" * 64, "dll_sha": "b" * 64})
    r = _roda_cli(["--criterios", arq_c, "--identidade", arq_i, "--repo", repo])
    checar("CLI positivo exit 0", r.returncode == 0, "exit=%s" % r.returncode)
    try:
        saida = json.loads(r.stdout)
    except ValueError:
        saida = None
    checar("CLI positivo emite JSON parseavel", isinstance(saida, dict),
           (r.stdout or "")[:120] + (r.stderr or "")[:120])
    if isinstance(saida, dict):
        checar("CLI positivo: pronto_para_decisao true", saida["pronto_para_decisao"] is True)
        checar("CLI positivo: contrato completo",
               all(k in saida for k in ("por_mod", "falhas_automaticas", "pendencias_humanas",
                                        "pronto_para_decisao", "aceite_humano", "publicacao")))
        checar("CLI positivo: roteiro_humano presente", "roteiro_humano" in saida)


def t_cli_real_runtime_ok(tmp):
    repo = os.path.join(tmp, "cli_rt_ok")
    ev = evid_hash(repo, "ev/rt.json", "conteudo")
    crits = [crit_runtime("CLIRT", evidencia=[ev])]
    arq_c = os.path.join(repo, "criterios.json")
    arq_i = os.path.join(repo, "identidade.json")
    _escreve_json(arq_c, crits)
    _escreve_json(arq_i, {"fonte_sha": "a" * 64, "dll_sha": "b" * 64, "sessao": "s1"})
    r = _roda_cli(["--criterios", arq_c, "--identidade", arq_i, "--repo", repo])
    checar("CLI runtime com cadeia completa exit 0", r.returncode == 0, "exit=%s" % r.returncode)


def t_cli_real_runtime_label_falso(tmp):
    """REPRO CIC-2R na CLI real: prova_runtime=False tem de sair reprovado (exit 1)."""
    repo = os.path.join(tmp, "cli_rt_false")
    ev = evid_hash(repo, "ev/rt.json", "conteudo")
    c = crit_runtime("CLIRF", evidencia=[ev])
    c["prova_runtime"] = False
    arq_c = os.path.join(repo, "criterios.json")
    arq_i = os.path.join(repo, "identidade.json")
    _escreve_json(arq_c, [c])
    _escreve_json(arq_i, {"fonte_sha": "a" * 64, "dll_sha": "b" * 64, "sessao": "s1"})
    r = _roda_cli(["--criterios", arq_c, "--identidade", arq_i, "--repo", repo,
                   "--resultado", os.path.join(repo, "decisao.json")])
    checar("CLI prova_runtime=False exit 1", r.returncode == 1, "exit=%s" % r.returncode)
    saida = None
    try:
        saida = json.loads(r.stdout)
    except ValueError:
        pass
    if isinstance(saida, dict):
        checar("CLI prova_runtime=False: 0 vinculantes",
               saida["resumo"]["ok_vinculantes"] == 0)
        checar("CLI prova_runtime=False: falha automatica registrada",
               saida["resumo"]["falhas_automaticas"] >= 1)
        checar("CLI prova_runtime=False: nada no roteiro humano",
               saida["roteiro_humano"]["total"] == 0)


def t_cli_real_negativo(tmp):
    repo = os.path.join(tmp, "cli_neg")
    os.makedirs(repo, exist_ok=True)
    crits = [crit("CLIN1", estado="REPROVADO")]
    arq_c = os.path.join(repo, "criterios.json")
    arq_i = os.path.join(repo, "identidade.json")
    _escreve_json(arq_c, crits)
    _escreve_json(arq_i, {"fonte_sha": "a" * 64, "dll_sha": "b" * 64})
    r = _roda_cli(["--criterios", arq_c, "--identidade", arq_i, "--repo", repo,
                   "--resultado", os.path.join(repo, "decisao.json")])
    checar("CLI negativo exit 1 (falha automatica)", r.returncode == 1, "exit=%s" % r.returncode)
    checar("CLI negativo grava --resultado",
           os.path.isfile(os.path.join(repo, "decisao.json")))


def t_cli_real_sem_criterios(tmp):
    repo = os.path.join(tmp, "cli_vazio")
    os.makedirs(repo, exist_ok=True)
    arq_c = os.path.join(repo, "criterios.json")
    _escreve_json(arq_c, [])
    r = _roda_cli(["--criterios", arq_c, "--repo", repo])
    checar("CLI sem criterios exit 2", r.returncode == 2, "exit=%s" % r.returncode)


def t_cli_arquivo_inexistente(tmp):
    r = _roda_cli(["--criterios", os.path.join(tmp, "nao-existe.json")])
    checar("CLI criterios ausente exit 2 (nao rodou)", r.returncode == 2, "exit=%s" % r.returncode)


# ==================================================================== runner

def _guarda(fn, *args):
    try:
        fn(*args)
    except Exception as erro:  # noqa: BLE001 - vira REPROVOU, nao derruba o arquivo
        checar("erro inesperado em %s" % getattr(fn, "__name__", fn), False,
               "%s: %s" % (type(erro).__name__, erro))


def main():
    try:
        D = carregar()
    except Exception as erro:  # noqa: BLE001
        print("RESULTADO|NAO_RODOU|carregar|%s: %s" % (type(erro).__name__, erro))
        return 2
    base = area_scratch()
    with tempfile.TemporaryDirectory(prefix="t-cic2-", dir=base) as tmp:
        _guarda(t_sem_criterios, D)
        _guarda(t_ok_vinculante_offline, D, tmp)
        _guarda(t_ok_runtime_vinculante, D, tmp)
        _guarda(t_prova_runtime_false_nunca_vinculante, D, tmp)
        _guarda(t_runtime_ok_sem_cadeia_nao_vincula, D, tmp)
        _guarda(t_runtime_hash_divergente_nao_vincula, D, tmp)
        _guarda(t_runtime_sessao_divergente_nao_vincula, D, tmp)
        _guarda(t_config_relevante_sem_config_sha, D, tmp)
        _guarda(t_config_sha_confirmado_vincula, D, tmp)
        _guarda(t_manifest_incoerente_nao_vincula, D, tmp)
        _guarda(t_manifest_coerente_vincula, D, tmp)
        _guarda(t_evidencia_ausente_declarada_sha, D, tmp)
        _guarda(t_label_ok_sem_evidencia, D)
        _guarda(t_evidencia_ausente, D, tmp)
        _guarda(t_fixture_nunca_prova, D)
        _guarda(t_fixture_reprovada_e_falha, D)
        _guarda(t_hash_stale_reprova, D, tmp)
        _guarda(t_hash_nao_confirmado, D, tmp)
        _guarda(t_hash_confirmado_ok, D, tmp)
        _guarda(t_identidade_insuficiente, D, tmp)
        _guarda(t_offline_nao_exercitado_vira_falha, D)
        _guarda(t_runtime_lacuna_tecnica_vai_agente, D)
        _guarda(t_runtime_autorizacao_explicita_vai_humano, D)
        _guarda(t_runtime_tipo_pendencia_julgamento_visual, D)
        _guarda(t_runtime_sem_sinal_nao_vai_humano, D)
        _guarda(t_runtime_julgamento_visual, D, tmp)
        _guarda(t_instrucao_especifica_preservada, D, tmp)
        _guarda(t_reprovado_vira_falha, D)
        _guarda(t_por_mod_resume, D)
        _guarda(t_nao_joga_falha_automatizavel_no_humano, D)
        _guarda(t_aceite_publicacao_separados, D)
        _guarda(t_roteiro_humano_curto, D, tmp)
        _guarda(t_criterio_malformado, D)
        _guarda(t_cadeia_residual_integracao, D, tmp)
        _guarda(t_cli_real_positivo, tmp)
        _guarda(t_cli_real_runtime_ok, tmp)
        _guarda(t_cli_real_runtime_label_falso, tmp)
        _guarda(t_cli_real_negativo, tmp)
        _guarda(t_cli_real_sem_criterios, tmp)
        _guarda(t_cli_arquivo_inexistente, tmp)
    print()
    print("total: %d | falhas: %d" % (len(RESULTADOS), len(FALHAS)))
    if FALHAS:
        print("REPROVADAS: %s" % ", ".join(FALHAS))
        return 1
    print("TUDO OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
