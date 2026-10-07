#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CIC-5R — os achados do parecer independente CIC-5R no coletor AUT-4 (regressao offline).

Prova, por execucao, cada conserto desta frente (AUT-4F). O parecer e
`docs/automacao/CIC-5R-revisao.md`.

  R-1  `hash_fonte` do coletor e o sha256 da DLL do probe: os adaptadores de cenario
       (`cenarios/rstv.py`, `cenarios/tooltips_shrines.py`) tem de confrontar
       `hash_fonte` com `dll_sha` — NUNCA com `fonte_sha`. Antes, toda observacao
       runtime LEGITIMA era marcada INDETERMINADO/"OUTRA build".
  R-2  CLI `--executar` sem `--perfil`/`--out-dir`: o gate decide ANTES de normalizar
       caminho -> NAO_EXERCITADO/exit 2, nunca `TypeError`/exit 1.
  R-3  a espera de estado para por ESTADO TERMINAL: `status` terminal tambem (o catch
       do probe grava `status=ERRO` SEM setar `fase`). Antes, o erro do instrumento
       queimava o teto INTEIRO da espera.
  R-4  `encerrar_imagem` NAO mata mais por imagem (`taskkill /F /IM` mataria TODAS as
       instancias): encerra SO os PIDs que nasceram nesta rodada e, sem medicao,
       RECUSA. O `Popen` do lancador e o steam.exe, nao o jogo.
  R-5  o runner de contra-prova nao aceita mais `exit == 1` por EXCECAO: so a linha
       `RESULTADO|REPROVOU|` (assert/`Falhou`) conta como prova.
  S-2  `campos_alvo` de TODOS os cenarios governa o veredito — nao so o topo/1o.
  S-3  campo EXTRA declarado alvo e ausente e LACUNA (nao fecha verde).

Nao abre o jogo, nao instala probe, nao toca no perfil do dono: e execucao offline.
"""
import importlib.util
import json
import os
import tempfile

import comum as C

META = {
    "nome": "aut4-cic5r",
    "categoria": "pura",
    "requer": [],
    "descricao": "CIC-5R R-1 (hash_fonte=dll_sha nos adaptadores), R-2 (gate antes do "
                 "abspath), R-3 (espera para por status terminal), R-4 (encerra so PID novo), "
                 "R-5 (contra-prova rejeita crash), S-2 (alvos de todos os cenarios) e "
                 "S-3 (extra alvo ausente e lacuna)",
}

DIR_CENARIOS = os.path.join(C.REPO, "tools", "automacao", "cenarios")
ALVOS_ATIVOS = ["objeto", "texto_bruto", "texto_renderizado", "fonte", "material",
                "shader", "keywords", "cores", "geometria", "owners"]

SRC_SHA = "a" * 64
DLL_SHA = "b" * 64


def _importar(caminho, nome):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _cenario(nome):
    return _importar(os.path.join(DIR_CENARIOS, "%s.py" % nome), "cic5r_%s" % nome)


def _escrever(dados, sufixo=".json"):
    fd, caminho = tempfile.mkstemp(prefix="cic5r-", suffix=sufixo)
    os.close(fd)
    with open(caminho, "w", encoding="utf-8") as fh:
        json.dump(dados, fh, ensure_ascii=False)
    return caminho


def corpo():
    col = C.coletor()
    fx = C.fixture("probe-saida-exemplo")
    plano = C.fixture("plano-exemplo")
    ctx = {"sessao": fx["sessao"], "hash_fonte": fx["hash_fonte"]}
    anexadas = col.anexar_contexto(fx["observacoes"], ctx)

    # ============================ R-1: hash_fonte e a chave da DLL ============
    for nome in ("rstv", "tooltips_shrines"):
        mod = _cenario(nome)
        alias = dict(getattr(mod, "_ALIAS_HASH"))
        C.arc.igual(alias.get("hash_fonte"), "dll_sha",
                    "R-1: %s tem de aliasar hash_fonte -> dll_sha (nunca fonte_sha)" % nome)
        C.arc.igual(alias.get("hash_dll"), "dll_sha",
                    "R-1: %s tem de aliasar hash_dll -> dll_sha" % nome)

    rstv = _cenario("rstv")
    identidade = {"fonte_sha": SRC_SHA, "dll_sha": DLL_SHA}
    obs_rt = {"procedencia": "runtime", "sessao": "s1", "hash_fonte": DLL_SHA}
    C.arc.igual(rstv._checagem_hashes(obs_rt, identidade), ([], []),
                "R-1: hash_fonte (sha da DLL) casa com dll_sha — nao diverge nem fica "
                "nao-confirmado")
    C.arc.igual(rstv._hash_divergente(obs_rt, identidade), False,
                "R-1: observacao legitima NAO pode ser marcada divergente")
    C.arc.igual(rstv._evidencia_runtime(obs_rt, identidade), True,
                "R-1: observacao legitima PROVA runtime (a cadeia da DLL fecha)")

    ts = _cenario("tooltips_shrines")
    ident_kwargs = {"suficiente": True, "faltando": [], "fonte_sha": SRC_SHA, "dll_sha": DLL_SHA}
    estado_ts, motivo_ts = ts._cadeia_runtime(obs_rt, ident_kwargs)
    C.arc.exigir(estado_ts != "INDETERMINADO",
                 "R-1: tooltips_shrines NAO pode dar INDETERMINADO/\"OUTRA build\" para uma "
                 "observacao LEGITIMA (veio %r: %s)" % (estado_ts, motivo_ts))
    obs_rt_ev = dict(obs_rt, evidencia=["log-lido"])
    C.arc.igual(ts._cadeia_runtime(obs_rt_ev, ident_kwargs), (None, None),
                "R-1: a cadeia da observacao legitima (hash da DLL + evidencia) FECHA")
    C.arc.igual(ts._cadeia_runtime({"procedencia": "runtime", "sessao": "s1",
                                    "hash_fonte": "c" * 64, "evidencia": ["log"]}, ident_kwargs)[0],
                "INDETERMINADO",
                "R-1: hash de OUTRA build continua INDETERMINADO (o conserto nao afrouxou)")
    # controle negativo: hash que NAO e o da DLL continua divergindo.
    obs_outra = {"procedencia": "runtime", "sessao": "s1", "hash_fonte": "c" * 64}
    C.arc.igual(rstv._hash_divergente(obs_outra, identidade), True,
                "R-1: hash de OUTRA build continua divergente (o conserto nao afrouxou)")

    # ============================ R-2: gate ANTES do abspath ==================
    try:
        r2, c2 = col.executar_rodada(plano, perfil_dir=None, out_dir=None, dll_probe=__file__,
                                     autorizado=True, jogo_disponivel=True, confirmacao="coleta")
    except TypeError as erro:
        C.arc.exigir(False, "R-2: --executar sem --perfil NAO pode estourar TypeError "
                            "(veio: %s)" % erro)
    C.arc.igual(c2, 2, "R-2: autorizado sem destino -> exit 2 (default honesto, nao crash)")
    C.arc.igual(r2["status"], "NAO_EXERCITADO", "R-2: status NAO_EXERCITADO")
    C.arc.exigir("out_dir" in r2["motivo"] and "perfil_dir" in r2["motivo"],
                 "R-2: o motivo nomeia os destinos que faltam")
    C.arc.igual(r2.get("efeitos_colaterais", []), [], "R-2: nada foi tocado")

    # ============================ R-3: espera por status terminal =============
    with tempfile.TemporaryDirectory(prefix="cic5r-r3-") as raiz:
        caminho_log = os.path.join(raiz, "LogOutput.log")        # ausente de proposito
        caminho_json = os.path.join(raiz, "aut4probe.json")
        with open(caminho_json, "w", encoding="utf-8") as fh:
            json.dump({"fase": "lendo-objetos", "status": "ERRO"}, fh)
        estado = col._esperar_estado(caminho_log, caminho_json, 0.6, 0.05)
        C.arc.igual(estado["status"], "ERRO", "R-3: a espera registra o status do probe")
        C.arc.igual(estado["fase"], "lendo-objetos", "R-3: a fase nao-terminal fica visivel")
        C.arc.exigir(estado["segundos"] < 0.3,
                     "R-3: status terminal tem de PARAR a espera (nao queimar o teto: "
                     "%.3f s de 0.6 s)" % estado["segundos"])

    # ============================ R-4: encerra so o PID NOVO ==================
    recusado = col.planejar_encerramento("Stolen Realm.exe", None, None)
    C.arc.igual(recusado["recusado"], True,
                "R-4: sem medicao dos PIDs o encerramento e RECUSADO (fail-closed)")
    C.arc.igual(recusado["pids"], [], "R-4: recusado nao mata ninguem")
    decisao = col.planejar_encerramento("Stolen Realm.exe", {100, 200}, {100, 200, 300})
    C.arc.igual(decisao["pids"], [300],
                "R-4: encerra SO o PID que nasceu nesta rodada (o do dono, 100/200, sobrevive)")
    C.arc.igual(decisao["recusado"], False, "R-4: com medicao, decide por PID")
    C.arc.igual(col.planejar_encerramento("x.exe", {7}, {7})["pids"], [],
                "R-4: nada novo -> nada a encerrar")
    fonte_col = open(os.path.join(C.RUNTIME, "coletor.py"), encoding="utf-8").read()
    C.arc.exigir('"/F", "/IM"' not in fonte_col,
                 "R-4: o encerramento por IMAGEM (mata todas as instancias) nao pode existir")
    C.arc.exigir('"/PID"' in fonte_col, "R-4: o encerramento tem de ser por PID")

    # ============================ R-5: contra-prova rejeita crash =============
    runner = _importar(os.path.join(C.RUNTIME, "roda_testes_runtime.py"), "cic5r_runner")
    ok_estado, ok_falhou = runner.classificar_contra_prova(
        1, "RESULTADO|REPROVOU|meu-teste|falhou de proposito")
    C.arc.igual(ok_falhou, False, "R-5: assert/Falhou CONTA como prova")
    crash_estado, crash_falhou = runner.classificar_contra_prova(
        1, "RESULTADO|REPROVOU|meu-teste|excecao inesperada: Traceback (most recent call last)")
    C.arc.igual(crash_falhou, True, "R-5: reprovar por EXCECAO nao pode contar (era o defeito)")
    C.arc.exigir("EXCECAO" in crash_estado, "R-5: o rotulo nomeia o crash")
    C.arc.igual(runner.classificar_contra_prova(0, "RESULTADO|PASSOU|x|ok")[1], True,
                "R-5: isca que PASSA continua vermelha")
    C.arc.igual(runner.classificar_contra_prova(2, "RESULTADO|NAO_RODOU|x|falta lib")[1], True,
                "R-5: NAO RODOU continua vermelho")

    # ============================ S-2: alvos de TODOS os cenarios =============
    plano2 = dict(plano)
    plano2.pop("campos_alvo", None)
    plano2["cenarios"] = [
        {"nome": "primeiro", "alvos": ["Tooltip.Title"], "campos_alvo": ["material"]},
        {"nome": "segundo", "alvos": ["Tooltip.Description"], "campos_alvo": ["tamanho_fonte"]},
    ]
    alvos = col._alvos_do_plano(plano2)
    C.arc.exigir("material" in alvos, "S-2: o alvo do 1o cenario entra")
    C.arc.exigir("tamanho_fonte" in alvos,
                 "S-2: o alvo do 2o cenario TAMBEM governa o veredito (antes era ignorado)")

    obs_s2 = dict(anexadas[0])
    obs_s2["tamanho_fonte"] = None                     # 2o cenario nao lido
    n_s2 = col.normalizar_observacao(col.anexar_contexto([obs_s2], ctx)[0], "runtime",
                                     alvos=alvos)
    C.arc.exigir("tamanho_fonte" in n_s2["lacunas"],
                 "S-2: o alvo declarado no 2o cenario e COBRADO (lacuna)")
    consolidado_s2, cod_s2 = col.consolidar(plano2, col.anexar_contexto([obs_s2], ctx),
                                            "runtime", contexto=ctx)
    C.arc.igual(consolidado_s2["status"], "INCOMPLETO",
                "S-2: plano com alvo do 2o cenario nao lido NAO fecha CONFIRMADA")
    C.arc.exigir(cod_s2 != 0, "S-2: INCOMPLETO -> exit != 0")

    # controle positivo: com o 2o cenario lido, o mesmo plano fecha.
    obs_s2ok = dict(anexadas[0])
    consolidado_ok, cod_ok = col.consolidar(plano2, col.anexar_contexto([obs_s2ok], ctx),
                                            "runtime", contexto=ctx)
    C.arc.igual(consolidado_ok["status"], "CONFIRMADA",
                "S-2: com TODOS os alvos lidos o plano fecha (o alvo governa, nao atrapalha)")
    C.arc.igual(cod_ok, 0, "S-2: exit 0 no controle positivo")

    # ============================ S-3: campo EXTRA alvo =======================
    n_extra_ok = col.normalizar_observacao(anexadas[0], "runtime", alvos=["shader_suportado"])
    C.arc.igual(n_extra_ok["lacunas"], [], "S-3: extra alvo PRESENTE nao gera lacuna")
    obs_extra = dict(anexadas[0])
    obs_extra["shader_suportado"] = None
    n_extra = col.normalizar_observacao(obs_extra, "runtime", alvos=["shader_suportado"])
    C.arc.exigir("shader_suportado" in n_extra["lacunas"],
                 "S-3: campo EXTRA declarado alvo e AUSENTE tem de virar lacuna")
    C.arc.igual(n_extra["ok"], False, "S-3: com lacuna de extra, nao fecha ok")
    consolidado_s3, cod_s3 = col.consolidar(plano, col.anexar_contexto([obs_extra], ctx),
                                            "runtime", contexto=ctx,
                                            alvos=["shader_suportado"])
    C.arc.igual(consolidado_s3["status"], "INCOMPLETO",
                "S-3: extra alvo ausente -> INCOMPLETO, nunca CONFIRMADA")
    C.arc.exigir(cod_s3 != 0, "S-3: exit != 0")


if __name__ == "__main__":
    C.arc.main(META, corpo)
