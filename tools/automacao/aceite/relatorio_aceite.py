#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""relatorio_aceite.py - AUT-7: relatorio de aceite do DoD por mod (t_674c5976).

O QUE ESTE MODULO E
-------------------
O COMANDO OFFLINE unico que consolida as frentes de validacao do ciclo AUT em UM
relatorio por mod/mudanca, com o status TECNICO separado de ACEITE HUMANO e de
VERSAO PUBLICADA:

  * AUT-3 (bancada estatica/build/regressao) - via o orquestrador CIC-1, que deriva
    os criterios do `AUT-3-resultado.json` e confronta o snapshot com os bytes ATUAIS
    (resultado velho NAO vale para fonte nova);
  * AUT-5 (RSTV)   - `tools/automacao/cenarios/rstv.py::avaliar`;
  * AUT-6 (shrines) - `tools/automacao/aut6/cobertura.py::avaliar` (a frente REAL do
    COR-AUT6). O antigo `tools/automacao/cenarios/tooltips_shrines.py` NAO substitui essa
    frente: mediria por outras regras e poderia passar por integracao do AUT-6;
  * AUT-7 (esta frente: BetterFont/BetterCombatText/BetterStats/RoguelikeDebugger) -
    `tools/automacao/estilo/estilo_atributos.py` (medicao offline REAL + runtime).

A classificacao NAO e reimplementada: quem decide prova vinculante / falha
automatica / pendencia humana e o `tools/automacao/ciclo/decisao.py` (CIC-2), com
a regra "nunca OK por rotulo". Se o modulo de decisao nao estiver disponivel, este
relatorio NAO improvisa um veredito: ele sai INCOMPLETO (exit 2) dizendo o que falta.

O QUE ESTE RELATORIO SEPARA (e por que)
---------------------------------------
  * `tecnico`        - o que a automacao provou/falhou: NAO e aceite;
  * `aceite_humano`  - pronunciamento do dono (jogo/UI), por padrao NAO_PRONUNCIADO;
  * `publicacao`     - versao no ar (Thunderstore e imutavel), por padrao NAO_VERIFICADO.
  * `revisoes`       - AUT-3R/5R/6R: enquanto houver revisao pendente, a consolidacao
    final e declarada PROVISORIA (`consolidacao_final=false`).

"CARREGADO" NAO E "EFICAZ": nenhum criterio aqui aprova mod por ter carregado. O
relatorio leva a prova (caminho + sha256) e o que NAO foi exercitado fica dito.

CLI
---
    python tools/automacao/aceite/relatorio_aceite.py --repo C:/dev/stolen-realm \
        --out-dir <dir-de-evidencia> [--aut3-resultado <AUT-3-resultado.json>] \
        [--rstv-observacoes obs.json] [--shrines-observacoes obs.json] \
        [--estilo-observacoes obs.json] [--identidade ident.json] [--aceite aceite.json] \
        [--revisoes revisoes.json] [--relatorio docs/automacao/AUT-7-relatorio.md] \
        [--out saida.json] [--texto] [--sem-suite]

Exit: 0 = sem falha automatica (o que falta e decisao humana) · 1 = ha falha
      automatica (volta ao ciclo) · 2 = nao deu para consolidar (falta entrada/ferramenta).
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
TOOLS = os.path.join(RAIZ, "tools")
TESTES = os.path.join(TOOLS, "testes")
AUTOMACAO = os.path.join(TOOLS, "automacao")
# O pacote `aut6` entra no sys.path porque `aut6/cobertura.py` faz `import prova` no TOPO
# (achado A8): carregado por caminho, esse import falhava e a frente real saia
# `AUT-6/avaliador-indisponivel` com 0 itens. `prova.py`/`validacoes.py` existem SO em
# `aut6/`, entao o diretorio e o dono legitimo desses nomes.
AUT6 = os.path.join(AUTOMACAO, "aut6")
for _p in (TESTES, TOOLS, AUTOMACAO, AUT6):
    if _p not in sys.path:
        sys.path.insert(0, _p)

ESQUEMA = "AUT-7/aceite/1"
TAREFA = "t_674c5976"
MODS = ("BetterTooltips", "BetterFont", "BetterCombatText", "BetterStats",
        "RoguelikeSkillTreeVisualizer", "RoguelikeDebugger")
FRENTES = ("AUT-3", "AUT-5", "AUT-6", "AUT-7")

EXIT_OK, EXIT_FALHOU, EXIT_NAO_RODOU = 0, 1, 2
_CACHE = {}


def _modulo(nome, caminho):
    chave = "mod:" + nome
    if chave in _CACHE:
        return _CACHE[chave]
    try:
        spec = importlib.util.spec_from_file_location(nome, caminho)
        m = importlib.util.module_from_spec(spec)
        sys.modules[nome] = m
        spec.loader.exec_module(m)
    except Exception:
        m = None
    _CACHE[chave] = m
    return m


def _estilo():
    return _modulo("aut7_estilo_rel", os.path.join(AUTOMACAO, "estilo", "estilo_atributos.py"))


def _decisao():
    return _modulo("aut7_decisao", os.path.join(AUTOMACAO, "ciclo", "decisao.py"))


def _ciclo():
    return _modulo("aut7_ciclo_rel", os.path.join(AUTOMACAO, "ciclo", "ciclo.py"))


def _rstv():
    return _modulo("aut7_rstv", os.path.join(AUTOMACAO, "cenarios", "rstv.py"))


def _shrines():
    return _modulo("aut7_shrines", os.path.join(AUTOMACAO, "cenarios", "tooltips_shrines.py"))


def _ler(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def _ler_json(caminho):
    return json.loads(_ler(caminho))


def _escrever(caminho, texto):
    pasta = os.path.dirname(os.path.abspath(caminho))
    if pasta:
        os.makedirs(pasta, exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(texto)


def _nao_exercitado(mod, cid, motivo, classe="offline", evidencia=None, extra=None):
    """Criterio honesto de LACUNA (nunca OK), no contrato do ciclo."""
    c = {"id": cid, "mod": mod, "estado": "NAO_EXERCITADO", "classe": classe,
         "procedencia": "execucao", "esperado": "a frente medir este item",
         "observado": "nao medido nesta rodada", "motivo": motivo,
         "evidencia": list(evidencia or []), "tarefa_origem": TAREFA}
    if extra:
        c.update(extra)
    return c


# --------------------------------------------------------------- frentes -> criterios

def situacao_aut3(repo, caminho_aut3):
    """Estado do resultado do AUT-3 frente aos bytes ATUAIS (o motivo da lacuna, sem sumir).

    Sem isto o leitor ve "criterio offline nao exercitado" (texto da decisao) e perde a
    CAUSA: resultado ausente, ilegivel ou snapshot que nao corresponde a fonte de agora.
    """
    base = {"arquivo": os.path.abspath(caminho_aut3) if caminho_aut3 else None,
            "presente": bool(caminho_aut3 and os.path.isfile(caminho_aut3)),
            "snapshot_ok": None, "motivo": "", "gerado_em": None, "veredito": None}
    ciclo = _ciclo()
    if ciclo is None:
        base["motivo"] = "orquestrador CIC-1 indisponivel"
        return base
    if not base["presente"]:
        base["motivo"] = "resultado do AUT-3 ausente: rode a bancada e aponte --aut3-resultado"
        return base
    try:
        aut3, erro = ciclo.carregar_aut3(caminho_aut3)
    except Exception as ex:
        base["motivo"] = "resultado do AUT-3 ilegivel (%s: %s)" % (type(ex).__name__, ex)
        return base
    if aut3 is None:
        base["motivo"] = erro or "resultado do AUT-3 em formato inesperado"
        return base
    base["gerado_em"] = aut3.get("gerado_em")
    base["veredito"] = aut3.get("veredito")
    base["sha256"] = (_ev_rel(caminho_aut3) or {}).get("sha256")
    try:
        ok, motivo, _det = ciclo.confrontar_snapshot(aut3, repo)
    except Exception as ex:
        base["motivo"] = "nao deu para confrontar o snapshot (%s: %s)" % (type(ex).__name__, ex)
        return base
    base["snapshot_ok"] = bool(ok)
    base["motivo"] = motivo
    return base


def criterios_aut3(repo, caminho_aut3, identidade):
    """Criterios do AUT-3 pelo orquestrador CIC-1 (snapshot confrontado com os bytes atuais)."""
    ciclo = _ciclo()
    if ciclo is None:
        return [_nao_exercitado("transversal", "AUT-3/modulo-indisponivel",
                                "orquestrador CIC-1 (ciclo.py) indisponivel: nao da para "
                                "reusar a bancada AUT-3 sem reimplementar o que ja existe")]
    if not caminho_aut3 or not os.path.isfile(caminho_aut3):
        return [_nao_exercitado("transversal", "AUT-3/resultado-ausente",
                                "AUT-3 sem resultado em %r: rode a bancada offline "
                                "(`tools/automacao/offline/bancada_aut3.py --jogo`) e aponte "
                                "`--aut3-resultado`" % (caminho_aut3,),
                                evidencia=[_ev_rel(caminho_aut3)] if caminho_aut3 else None)]
    try:
        aut3, erro = ciclo.carregar_aut3(caminho_aut3)
        if aut3 is None:
            return [_nao_exercitado("transversal", "AUT-3/resultado-ilegivel",
                                    "%s (esperado um resultado do AUT-3 no formato da bancada "
                                    "offline)" % erro, evidencia=[_ev_rel(caminho_aut3)])]
        ok, motivo, _det = ciclo.confrontar_snapshot(aut3, repo)
        return ciclo.criterios_aut3(aut3, identidade, repo=repo, snapshot_ok=ok,
                                    snapshot_motivo=motivo)
    except Exception as erro:
        return [_nao_exercitado("transversal", "AUT-3/nao-leu",
                                "nao deu para ler o AUT-3 (%s: %s)"
                                % (type(erro).__name__, erro),
                                evidencia=[_ev_rel(caminho_aut3)])]


def _ev_rel(caminho):
    if not caminho or not os.path.isfile(caminho):
        return None
    h = hashlib.sha256()
    with open(caminho, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return {"caminho": os.path.abspath(caminho), "sha256": h.hexdigest()}


def _sha(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def _gap(mod, cid, motivo, evidencia=None, frente=None):
    """Lacuna CANONICA de frente: id estavel, evidencia real, nunca frente=0."""
    c = _nao_exercitado(mod, cid, motivo, evidencia=evidencia)
    if frente:
        c["frente_origem"] = frente
    return c


def _anotar(c, frente, adaptador, identidade):
    c = dict(c)
    c["frente_origem"] = c.get("frente_origem") or frente
    c["adaptador"] = adaptador
    # A identidade da rodada entra como RASTREABILIDADE, nunca como prova EMPRESTADA (achado
    # A7): um item sem identidade propria virava OK_VINCULANTE so porque o adaptador lhe
    # dava `fonte_sha`/`dll_sha` da rodada.
    c["identidade_da_rodada"] = {k: (identidade or {}).get(k)
                                 for k in ("fonte_sha", "dll_sha") if (identidade or {}).get(k)}
    return c


def _identidade_do_item(c):
    """Identidade que o PROPRIO item declara (topo, `identidade`, `identidade_rodada`, `hashes`)."""
    achados = {}
    for bloco in (c, c.get("identidade"), c.get("identidade_rodada"), c.get("hashes"),
                  c.get("artefatos")):
        if isinstance(bloco, dict):
            for k in ("fonte_sha", "dll_sha"):
                v = bloco.get(k)
                if isinstance(v, str) and v.strip():
                    achados.setdefault(k, v.strip())
    return achados


def _refs_de_evidencia(entradas, repo):
    """`evidencia` -> [{caminho, sha256}] CONFERINDO existencia e bytes (achado A7).

    Devolve `(refs, problemas)`. Entrada sem arquivo real, ou com sha declarado que nao bate
    com os bytes, e PROBLEMA: o item nao entra como prova por rotulo. Quando a frente so
    declara o caminho, o sha e calculado aqui e passa a acompanhar a prova.
    """
    refs, problemas = [], []
    for e in (entradas or []):
        if isinstance(e, dict):
            caminho = e.get("caminho") or e.get("arquivo") or e.get("path") or e.get("evidencia")
            declarado = e.get("sha256") or e.get("hash")
        else:
            caminho, declarado = e, None
        caminho = str(caminho or "").strip()
        if not caminho:
            problemas.append("evidencia sem caminho")
            continue
        real = caminho if os.path.isabs(caminho) else os.path.join(repo, caminho)
        if not os.path.isfile(real):
            problemas.append("evidencia inexistente: %s" % caminho)
            continue
        sha = _sha(real)
        if declarado and str(declarado).strip() != sha:
            problemas.append("evidencia com sha divergente dos bytes: %s" % caminho)
            continue
        refs.append({"caminho": os.path.abspath(real), "sha256": sha})
    return refs, problemas


def _rebaixar(c, motivo):
    """Item de rodada nao confrontavel NAO fica OK: vira lacuna nomeada (achado A7)."""
    c = dict(c)
    c["estado"] = "NAO_EXERCITADO"
    c["motivo"] = ((str(c.get("motivo") or "") + " | ") + motivo).strip(" |")
    c["lacuna_probe"] = motivo
    c["tipo_pendencia"] = "coleta_tecnica"
    return c


def _validar_resultado_frente(frente, mod, caminho, identidade):
    """Resultado da frente: schema, cobertura canonica, identidade e evidencia por item.

    Devolve `(criterios, lacunas, cobertura)`. Resultado vazio/malformado NUNCA vira
    frente=0: gera criterio de lacuna com id canonico. A evidencia de cada item e
    CONFERIDA (existencia + sha) e item de rodada que nao confere com a identidade atual e
    REBAIXADO - rotulo OK com arquivo qualquer nao vira prova vinculante (achado A7).
    """
    ev = _ev_rel(caminho)
    adaptador = {"frente": frente, "arquivo": os.path.abspath(caminho) if caminho else None,
                 "sha256": (ev or {}).get("sha256")}

    def _lacuna(cid, motivo):
        return _anotar(_gap(mod, cid, motivo, [ev] if ev else None, frente), frente, adaptador,
                       identidade)
    try:
        dado = _ler_json(caminho)
    except Exception as erro:
        return ([_lacuna("%s/resultado-ilegivel" % frente,
                         "resultado do %s ilegivel (%s: %s)" % (frente, type(erro).__name__, erro))],
                [], {"itens": 0, "adaptador": adaptador})
    itens = dado.get("criterios") if isinstance(dado, dict) else (dado if isinstance(dado, list) else None)
    if not isinstance(itens, list) or not itens:
        return ([_lacuna("%s/resultado-vazio" % frente,
                         "resultado do %s veio vazio/fora do schema: frente sem cobertura NAO pode "
                         "desaparecer do relatorio (nem virar frente=0)" % frente)],
                [], {"itens": 0, "adaptador": adaptador})
    declarada = dado.get("identidade") if isinstance(dado, dict) else None
    divergentes = [k for k in ("fonte_sha", "dll_sha")
                   if isinstance(declarada, dict) and str(declarada.get(k) or "").strip()
                   and str((identidade or {}).get(k) or "").strip()
                   and declarada.get(k) != (identidade or {}).get(k)]
    lacunas = []
    if divergentes:
        lacunas.append(_lacuna("%s/identidade-divergente" % frente,
                               "%s: resultado declara %s de outra rodada que nao corresponde a "
                               "identidade atual" % (frente, ", ".join(divergentes))))
    bons, ruins, rebaixados = [], [], []
    for c in itens:
        if (not isinstance(c, dict) or not c.get("id") or not str(c.get("mod") or "").strip()
                or c.get("estado") not in ("OK", "REPROVADO", "NAO_EXERCITADO", "INDETERMINADO")):
            ruins.append(str(c)[:120])
            continue
        if not c.get("evidencia"):
            ruins.append(c.get("id"))
            continue
        refs, problemas = _refs_de_evidencia(c.get("evidencia"), RAIZ)
        if problemas or not refs:
            ruins.append("%s (%s)" % (c.get("id"), "; ".join(problemas) or "sem ref conferivel"))
            continue
        item = dict(c)
        item["evidencia"] = refs
        if divergentes:
            item = _rebaixar(item, "item de rodada divergente (%s): %s"
                                   % (frente, ", ".join(divergentes)))
            rebaixados.append(item.get("id"))
        elif item.get("estado") == "OK" and str(item.get("classe") or "").lower() == "runtime":
            proprio = _identidade_do_item(item)
            faltando = [k for k in ("fonte_sha", "dll_sha") if not proprio.get(k)]
            diverg = [k for k in ("fonte_sha", "dll_sha")
                      if proprio.get(k) and str((identidade or {}).get(k) or "").strip()
                      and proprio[k] != str((identidade or {}).get(k))]
            if faltando:
                item = _rebaixar(item, "item de runtime sem identidade PROPRIA (%s): a rodada nao "
                                       "empresta identidade para fechar OK" % ", ".join(faltando))
                rebaixados.append(item.get("id"))
            elif diverg:
                item = _rebaixar(item, "item declara %s de outra rodada" % ", ".join(diverg))
                rebaixados.append(item.get("id"))
        bons.append(_anotar(item, frente, adaptador, identidade))
    if ruins:
        lacunas.append(_lacuna("%s/resultado-malformado" % frente,
                               "%s: %d criterio(s) sem id/estado/evidencia verificavel: %s"
                               % (frente, len(ruins), "; ".join(ruins)[:300])))
    if rebaixados:
        lacunas.append(_lacuna("%s/item-nao-vinculado" % frente,
                               "%s: %d item(ns) de rodada nao confrontavel rebaixado(s) para "
                               "NAO_EXERCITADO (nao vinculante): %s"
                               % (frente, len(rebaixados), ", ".join(rebaixados)[:300])))
    cobertura = {"itens": len(bons), "descartados": len(ruins), "rebaixados": len(rebaixados),
                 "mods": sorted({str(c.get("mod")) for c in bons}), "adaptador": adaptador}
    if not bons:
        return (lacunas or [_lacuna("%s/resultado-vazio" % frente,
                                    "resultado do %s sem nenhum criterio utilizavel" % frente)],
                [], cobertura)
    return bons, lacunas, cobertura


def _frente_avaliador(frente):
    """Avaliador REAL da frente; para o AUT-6 da PREFERENCIA ao aut6/cobertura.py.

    Nao reimplementa nada: devolve `(modulo, rel, rotulo)` ou `(None, rel, motivo)`.
    """
    if frente == "AUT-6":
        rel = os.path.join("tools", "automacao", "aut6", "cobertura.py")
        m = _modulo("aut7_aut6_cobertura", os.path.join(RAIZ, rel))
        if m is not None and hasattr(m, "avaliar"):
            return m, rel, "aut6/cobertura.py::avaliar (integracoes COR-AUT6)"
        # A frente REAL e a do COR-AUT6: se ela nao carregar, a frente vira LACUNA NOMEADA.
        # Nao existe substituto silencioso - outro avaliador mediria com outras regras e o
        # resultado poderia passar por integracao do AUT-6.
        alternativa = os.path.join("tools", "automacao", "cenarios", "tooltips_shrines.py")
        nota = "nenhum modulo da frente AUT-6 carregou"
        if os.path.isfile(os.path.join(RAIZ, alternativa)):
            nota += (" (o antigo %s NAO substitui a frente real: mediria por outras regras)"
                     % "cenarios/tooltips_shrines.py")
        return None, rel, nota
    rel = os.path.join("tools", "automacao", "cenarios", "rstv.py")
    m = _modulo("aut7_rstv", os.path.join(RAIZ, rel))
    if m is not None and hasattr(m, "avaliar"):
        return m, rel, "cenarios/rstv.py::avaliar"
    return None, rel, "avaliador RSTV (cenarios/rstv.py) indisponivel"


def _criterios_de_arquivo(caminho):
    """Criterios ja produzidos pelo CLI da frente (`{"criterios": [...]}` ou lista)."""
    dado = _ler_json(caminho)
    if isinstance(dado, dict):
        cr = dado.get("criterios")
        return cr if isinstance(cr, list) else None
    return dado if isinstance(dado, list) else None


def _via_frente(frente, mod, observacoes, identidade, criterios_arquivo):
    """Resultado da frente (validado) OU observacoes (avaliador real) OU a lacuna dita."""
    if criterios_arquivo:
        bons, lacunas, cobertura = _validar_resultado_frente(frente, mod, criterios_arquivo, identidade)
        return list(bons) + list(lacunas), cobertura
    mod_av, rel, adaptador = _frente_avaliador(frente)
    if not observacoes:
        return [_gap(mod, "%s/nao-exercitado" % frente,
                     "%s NAO foi exercitado nesta rodada: sem observacoes de runtime e sem "
                     "resultado da frente. Nada aqui e OK; a rodada runtime depende de "
                     "autorizacao do dono" % frente, frente=frente)], {"itens": 0, "adaptador": adaptador}
    if mod_av is None:
        return [_gap(mod, "%s/avaliador-indisponivel" % frente, "%s: %s" % (frente, adaptador),
                     frente=frente)], {"itens": 0, "adaptador": adaptador}
    try:
        itens = mod_av.avaliar(observacoes, identidade or {})
    except Exception as erro:
        return [_gap(mod, "%s/avaliador-falhou" % frente,
                     "%s: avaliador %s levantou (%s: %s)" % (frente, adaptador, type(erro).__name__, erro),
                     frente=frente)], {"itens": 0, "adaptador": adaptador}
    if not isinstance(itens, list) or not itens:
        return [_gap(mod, "%s/resultado-vazio" % frente,
                     "%s: avaliador %s devolveu resultado vazio (lacuna, nunca frente=0)"
                     % (frente, adaptador), frente=frente)], {"itens": 0, "adaptador": adaptador}
    ev_ad = _ev_rel(os.path.join(RAIZ, rel))
    adapt = {"frente": frente, "modulo": os.path.abspath(os.path.join(RAIZ, rel)),
             "rotulo": adaptador, "sha256": (ev_ad or {}).get("sha256")}
    return ([_anotar(c, frente, adapt, identidade) for c in itens if isinstance(c, dict)],
            {"itens": len(itens), "adaptador": adapt})


def criterios_rstv(observacoes, identidade, criterios_arquivo=None):
    """Criterios do AUT-5 (RSTV). O resultado da frente e validado; vazio vira lacuna."""
    criterios, _ = _via_frente("AUT-5", "RoguelikeSkillTreeVisualizer", observacoes, identidade,
                               criterios_arquivo)
    return criterios


def criterios_shrines(observacoes, identidade, criterios_arquivo=None):
    """Criterios do AUT-6 (tooltips/shrines), reusando a frente real do aut6/cobertura.py."""
    criterios, _ = _via_frente("AUT-6", "BetterTooltips", observacoes, identidade,
                               criterios_arquivo)
    return criterios


def criterios_estilo(repo, out_dir, identidade, observacoes, rodar_suite=True):
    """Criterios do AUT-7: medicao offline REAL + avaliacao dos aspectos de runtime."""
    m = _estilo()
    if m is None:
        return [_nao_exercitado("transversal", "AUT-7/modulo-indisponivel",
                                "medidor de estilo (estilo_atributos.py) indisponivel")], {}
    criterios, meta = m.medir_offline(repo, out_dir, identidade, rodar=rodar_suite)
    criterios = list(criterios) + list(m.avaliar(observacoes or [], identidade or {}))
    return criterios, meta


# ------------------------------------------------------------------- relatorio

def _nome_ev(ev):
    """Nome curto de uma evidencia: o item da decisao traz o CAMINHO solto; a medicao traz dict."""
    if isinstance(ev, dict):
        ev = ev.get("caminho") or ev.get("arquivo") or ""
    if not ev:
        return ""
    return os.path.basename(str(ev))


def _crit(c):
    return {
        "id": c.get("id"), "mod": c.get("mod"), "estado": c.get("estado"),
        "classe": c.get("classe"), "procedencia": c.get("procedencia"),
        "classificacao": c.get("classificacao"), "esperado": c.get("esperado"),
        "observado": c.get("observado"), "motivo": c.get("motivo_decisao") or c.get("motivo"),
        "evidencia": c.get("evidencia") or [],
        "lacuna_probe": c.get("lacuna_probe"), "tipo_pendencia": c.get("tipo_pendencia"),
        "instrucoes_humanas": c.get("instrucoes_humanas"),
        "tarefa_origem": c.get("tarefa_origem"),
    }


def montar_relatorio(dec, criterios, meta_estilo, aut3=None):
    """Relatorio por mod: provas, regressao, lacunas e roteiro humano minimo."""
    por_mod = dec.get("por_mod") or {}
    humano = {}
    for item in (dec.get("roteiro_humano") or {}).get("itens", []):
        humano.setdefault(item["mod"], []).append(item)
    relatorio = {"tecnico": {}, "por_mod": {}, "revisoes": None, "aut3": aut3 or {}}

    for mod in list(MODS):
        b = por_mod.get(mod)
        if not b:
            relatorio["por_mod"][mod] = {
                "estado": "NAO_EXERCITADO", "provas": [], "regressao": [], "lacunas": [],
                "roteiro_humano": [],
                "nota": "nenhum criterio desta frente para o mod (nenhuma prova, nada exercitado)"}
            continue
        provas = [_crit(c) for c in b.get("ok_vinculantes", [])]
        regressao = [_crit(c) for c in b.get("falhas_automaticas", [])]
        lacunas = [_crit(c) for c in b.get("criterios", [])
                   if c.get("estado") in ("NAO_EXERCITADO", "INDETERMINADO")
                   and c.get("classificacao") not in ("OK_VINCULANTE",)]
        relatorio["por_mod"][mod] = {
            "estado": b.get("estado"),
            "total_criterios": b.get("total"),
            "provas": provas,
            "regressao": regressao,
            "lacunas": lacunas,
            "roteiro_humano": humano.get(mod, []),
        }
    relatorio["tecnico"] = {
        "falhas_automaticas": [_crit(c) for c in dec.get("falhas_automaticas", [])],
        "pronto_para_decisao": dec.get("pronto_para_decisao"),
        "motivo": dec.get("motivo_pronto_para_decisao"),
        "resumo": dec.get("resumo"),
    }
    return relatorio


def texto_do_relatorio(rel, revisoes):
    linhas = ["AUT-7 - RELATORIO DE ACEITE POR MOD (DoD)", ""]
    t = rel["tecnico"]
    r = t.get("resumo") or {}
    linhas.append("STATUS TECNICO (automacao; NAO e aceite):")
    linhas.append("  criterios=%s OK=%s falhas_automaticas=%s pendencias_humanas=%s"
                  % (r.get("criterios"), r.get("ok_vinculantes"), r.get("falhas_automaticas"),
                     r.get("pendencias_humanas")))
    linhas.append("  pronto_para_decisao=%s — %s" % (t.get("pronto_para_decisao"), t.get("motivo")))
    aut3 = rel.get("aut3") or {}
    if aut3:
        if aut3.get("snapshot_ok") is None:
            linhas.append("  ATENCAO AUT-3: %s" % aut3.get("motivo", ""))
        elif not aut3.get("snapshot_ok"):
            linhas.append("  ATENCAO AUT-3: resultado de %s NAO corresponde aos bytes atuais — "
                          "%s. TODOS os criterios do AUT-3 saem NAO_EXERCITADO ate nova rodada "
                          "(falha AUTOMATIZAVEL: nova rodada, nao tarefa do dono)."
                          % (aut3.get("gerado_em"), aut3.get("motivo", "")))
        else:
            linhas.append("  AUT-3: snapshot confere com os bytes atuais (%s)"
                          % aut3.get("gerado_em"))
    linhas.append("")
    for mod in MODS:
        d = rel["por_mod"][mod]
        linhas.append("== %s — estado tecnico: %s" % (mod, d["estado"]))
        if d.get("nota"):
            linhas.append("   %s" % d["nota"])
        if d["provas"]:
            linhas.append("   PROVAS (%d):" % len(d["provas"]))
            for p in d["provas"]:
                ev = p["evidencia"][0] if p["evidencia"] else "sem evidencia"
                linhas.append("     - [%s] %s (%s)" % (p["classificacao"], p["id"], _nome_ev(ev)))
        else:
            linhas.append("   PROVAS: nenhuma")
        if d["regressao"]:
            linhas.append("   REGRESSAO/FALHA (%d):" % len(d["regressao"]))
            for f in d["regressao"]:
                linhas.append("     - %s: %s" % (f["id"], str(f["motivo"])[:150]))
        if d["lacunas"]:
            linhas.append("   LACUNAS (%d):" % len(d["lacunas"]))
            for l in d["lacunas"]:
                linhas.append("     - %s [%s]: %s" % (l["id"], l["estado"], str(l["motivo"])[:150]))
        if d["roteiro_humano"]:
            linhas.append("   ROTEIRO HUMANO (residual):")
            for i in d["roteiro_humano"]:
                acao = ("AUTORIZAR rodada runtime" if i["tipo"] == "autorizacao"
                        else "JULGAR visual/UX")
                linhas.append("     - [%s] %s (criterios: %s)"
                              % (acao, i["mod"], ", ".join(i["criterios"])))
                for p in str(i.get("instrucoes") or "").splitlines():
                    if p.strip():
                        linhas.append("         * %s" % p.strip())
        linhas.append("")
    linhas.append("REVISOES (AUT-3R/5R/6R): %s"
                  % json.dumps(revisoes.get("revisoes", {}), ensure_ascii=False))
    linhas.append("CONSOLIDACAO FINAL: %s — %s"
                  % ("SIM" if revisoes.get("consolidacao_final") else "NAO (PROVISORIA)",
                     revisoes.get("motivo", "")))
    linhas.append("")
    linhas.append("ACEITE HUMANO: %s (estado SEPARADO do tecnico)"
                  % (rel.get("aceite_humano", {}) or {}).get("status", "NAO_PRONUNCIADO"))
    linhas.append("PUBLICACAO: %s (estado SEPARADO; versao publicada e imutavel)"
                  % (rel.get("publicacao", {}) or {}).get("status", "NAO_VERIFICADO"))
    linhas.append("")
    linhas.append("> Automacao NAO substitui aceite humano nem publicacao do DoD.")
    return "\n".join(linhas)


def markdown_do_relatorio(rel, revisoes, meta_estilo):
    l = ["# AUT-7 — relatorio de aceite por mod (provisorio)", ""]
    l.append("> Gerado por `tools/automacao/aceite/relatorio_aceite.py` (offline). "
             "Status TECNICO, ACEITE HUMANO e PUBLICACAO sao estados SEPARADOS. "
             "Nenhum \"carregado\" aqui vira \"eficaz\".")
    l.append("")
    t = rel["tecnico"]
    r = t.get("resumo") or {}
    l.append("## Status tecnico (automacao)")
    l.append("")
    l.append("| criterios | OK vinculantes | falhas automaticas | pendencias humanas | "
             "nao contam como prova |")
    l.append("|---|---|---|---|---|")
    l.append("| %s | %s | %s | %s | %s |" % (r.get("criterios"), r.get("ok_vinculantes"),
                                             r.get("falhas_automaticas"),
                                             r.get("pendencias_humanas"),
                                             r.get("nao_conta_como_prova")))
    l.append("")
    l.append("- **pronto_para_decisao**: %s — %s" % (t.get("pronto_para_decisao"), t.get("motivo")))
    l.append("- **consolidacao final**: %s — %s"
             % ("SIM" if revisoes.get("consolidacao_final") else "NAO (PROVISORIA)",
                revisoes.get("motivo", "")))
    l.append("- **aceite humano**: %s (estado separado)"
             % (rel.get("aceite_humano", {}) or {}).get("status", "NAO_PRONUNCIADO"))
    l.append("- **publicacao**: %s (estado separado; online NAO e consultado aqui)"
             % (rel.get("publicacao", {}) or {}).get("status", "NAO_VERIFICADO"))
    aut3 = rel.get("aut3") or {}
    if aut3:
        if aut3.get("snapshot_ok") is None:
            l.append("- **ATENCAO AUT-3**: %s" % aut3.get("motivo", ""))
        elif not aut3.get("snapshot_ok"):
            l.append("- **ATENCAO AUT-3**: o resultado de `%s` NAO corresponde aos bytes atuais — "
                     "%s. **Todos** os criterios do AUT-3 saem `NAO_EXERCITADO` ate uma nova rodada "
                     "da bancada sobre a arvore atual (falha AUTOMATIZAVEL: nova rodada, nao "
                     "tarefa do dono)." % (aut3.get("gerado_em"), aut3.get("motivo", "")))
        else:
            l.append("- **AUT-3**: snapshot confere com os bytes atuais (%s)" % aut3.get("gerado_em"))
    l.append("")
    for mod in MODS:
        d = rel["por_mod"][mod]
        l.append("## %s — estado tecnico: `%s`" % (mod, d["estado"]))
        if d.get("nota"):
            l.append("")
            l.append(d["nota"])
        l.append("")
        l.append("### Provas (%d)" % len(d["provas"]))
        if d["provas"]:
            for p in d["provas"]:
                ev = p["evidencia"][0] if p["evidencia"] else None
                l.append("- `%s` — %s%s" % (p["id"], str(p["observado"])[:160],
                                            (" | evidencia: `%s`" % _nome_ev(ev)) if ev else ""))
        else:
            l.append("- nenhuma")
        l.append("")
        l.append("### Regressao / falha automatica (%d)" % len(d["regressao"]))
        if d["regressao"]:
            for f in d["regressao"]:
                l.append("- `%s` — %s" % (f["id"], str(f["motivo"])[:200]))
        else:
            l.append("- nenhuma")
        l.append("")
        l.append("### Lacunas (%d)" % len(d["lacunas"]))
        if d["lacunas"]:
            for x in d["lacunas"]:
                l.append("- `%s` [%s] — %s" % (x["id"], x["estado"], str(x["motivo"])[:220]))
        else:
            l.append("- nenhuma")
        l.append("")
        l.append("### Roteiro humano minimo")
        if d["roteiro_humano"]:
            for i in d["roteiro_humano"]:
                acao = ("AUTORIZAR rodada runtime" if i["tipo"] == "autorizacao"
                        else "JULGAR visual/UX")
                l.append("- **[%s]** criterios: %s" % (acao, ", ".join(i["criterios"])))
                for p in str(i.get("instrucoes") or "").splitlines():
                    if p.strip():
                        l.append("  - %s" % p.strip())
        else:
            l.append("- nada: nenhuma pendencia humana deste mod.")
        l.append("")
    l.append("## Hashes do insumo (medicao desta rodada)")
    l.append("")
    for rotulo, dados_suite in ((meta_estilo or {}).get("suites", {}) or {}).items():
        l.append("- suite `%s`: `%s` (exit do runner=%s, sha256=`%s`)"
                 % (rotulo, os.path.basename(str(dados_suite.get("arquivo"))),
                    dados_suite.get("exit_runner"), str(dados_suite.get("sha256"))[:16]))
    l.append("")
    l.append("> Automacao NAO substitui aceite humano nem publicacao do DoD. "
             "AUSENTE/NAO_EXERCITADO/INDETERMINADO nunca sao OK.")
    l.append("")
    return "\n".join(l)


def _revisoes(caminho):
    """AUT-3R/5R/6R: enquanto pendente, a consolidacao final e PROVISORIA."""
    base = {"revisoes": {"AUT-3R": "PENDENTE", "AUT-5R": "PENDENTE", "AUT-6R": "PENDENTE"},
            "consolidacao_final": False,
            "motivo": "consolidacao final depende AUT-3R/5R/6R (revisao independente)"}
    if not caminho or not os.path.isfile(caminho):
        return base
    try:
        dado = _ler_json(caminho)
    except Exception as erro:
        base["motivo"] = "manifesto de revisoes ilegivel (%s): tratado como PENDENTE" % erro
        return base
    rev = dict(base["revisoes"])
    rev.update(dado.get("revisoes") or {})
    pendentes = sorted(k for k, v in rev.items()
                       if str(v).strip().upper() not in ("OK", "APROVADO", "APROVADA", "DONE"))
    return {"revisoes": rev, "consolidacao_final": not pendentes,
            "motivo": ("todas as revisoes fechadas com OK" if not pendentes
                       else "revisao(oes) pendente(s)/nao-OK: %s" % ", ".join(pendentes)),
            "arquivo": os.path.abspath(caminho)}


def consolidar(repo, out_dir, *, aut3_resultado=None, obs_estilo=None, obs_rstv=None,
               obs_shrines=None, crit_rstv=None, crit_shrines=None, identidade=None,
               aceite=None, revisoes_path=None, relatorio_path=None, rodar_suite=True):
    """Consolida as quatro frentes e devolve (resultado, exit_code)."""
    estilo = _estilo()
    decisao = _decisao()
    if estilo is None or decisao is None:
        return {"esquema": ESQUEMA, "tarefa": TAREFA, "status": "INCOMPLETO",
                "motivo": "dependencia ausente: %s"
                          % ", ".join(n for n, m in (("estilo_atributos.py", estilo),
                                                     ("decisao.py (CIC-2)", decisao)) if m is None)},\
            EXIT_NAO_RODOU

    if identidade is None:
        identidade, erro_ident = estilo.identidade_do_repo(repo)
        if erro_ident:
            identidade = dict(identidade or {})
            identidade["_erro"] = erro_ident
    identidade = identidade or {}

    c_aut3 = criterios_aut3(repo, aut3_resultado, identidade)
    c_rstv, meta_rstv = _via_frente("AUT-5", "RoguelikeSkillTreeVisualizer", obs_rstv, identidade,
                                    crit_rstv)
    c_shrines, meta_shrines = _via_frente("AUT-6", "BetterTooltips", obs_shrines, identidade,
                                          crit_shrines)
    c_estilo, meta_estilo = criterios_estilo(repo, out_dir, identidade, obs_estilo,
                                             rodar_suite=rodar_suite)
    criterios = list(c_aut3) + list(c_rstv or []) + list(c_shrines or []) + list(c_estilo or [])

    dec = decisao.consolidar(criterios, identidade, aceite_humano=aceite)
    sit_aut3 = situacao_aut3(repo, aut3_resultado)
    rel = montar_relatorio(dec, criterios, meta_estilo, aut3=sit_aut3)
    rel["aceite_humano"] = dec.get("aceite_humano")
    rel["publicacao"] = dec.get("publicacao")
    if isinstance(aceite, dict) and isinstance(aceite.get("publicacao"), dict):
        # declaracao do dono entra como DECLARADA (nao como verificacao online)
        rel["publicacao"] = dict(aceite["publicacao"])
        rel["publicacao"]["fonte"] = "declarada pelo dono no --aceite (NAO verificada online)"
    rev = _revisoes(revisoes_path)
    rel["revisoes"] = rev

    resultado = {
        "esquema": ESQUEMA, "tarefa": TAREFA,
        "identidade": dec.get("identidade"),
        "criterios": len(criterios),
        "por_frente": {
            "AUT-3": len(c_aut3),
            "AUT-5": len(c_rstv),
            "AUT-6": len(c_shrines),
            "AUT-7": len(c_estilo),
        },
        "frentes": {"AUT-5": meta_rstv, "AUT-6": meta_shrines},
        "decisao": dec,
        "relatorio": rel,
        "aut3": sit_aut3,
        "medicao_estilo": meta_estilo,
        "revisoes": rev,
    }
    resultado["texto"] = texto_do_relatorio(rel, rev)
    resultado["markdown"] = markdown_do_relatorio(rel, rev, meta_estilo)
    if relatorio_path:
        _escrever(relatorio_path, resultado["markdown"])
        resultado["relatorio_escrito"] = os.path.abspath(relatorio_path)
    codigo = EXIT_FALHOU if dec.get("falhas_automaticas") else EXIT_OK
    return resultado, codigo


def _carregar_observacoes(caminho):
    if not caminho:
        return []
    dado = _ler_json(caminho)
    if isinstance(dado, dict) and isinstance(dado.get("observacoes"), list):
        return dado["observacoes"]
    return dado if isinstance(dado, list) else []


def main(argv=None):
    ap = argparse.ArgumentParser(description="AUT-7: relatorio de aceite do DoD por mod (offline).")
    ap.add_argument("--repo", default=RAIZ)
    ap.add_argument("--out-dir", default=os.path.join(os.path.expandvars("%TEMP%"), "aut7-aceite"))
    ap.add_argument("--aut3-resultado",
                    default=os.path.join(RAIZ, "docs", "automacao", "AUT-3-resultado.json"))
    ap.add_argument("--estilo-observacoes")
    ap.add_argument("--rstv-observacoes")
    ap.add_argument("--shrines-observacoes")
    ap.add_argument("--rstv-criterios", help="resultado (JSON com 'criterios') da frente AUT-5")
    ap.add_argument("--shrines-criterios", help="resultado (JSON com 'criterios') da frente AUT-6")
    ap.add_argument("--identidade")
    ap.add_argument("--aceite")
    ap.add_argument("--revisoes", default=os.path.join(RAIZ, "docs", "automacao",
                                                       "AUT-7-revisoes.json"))
    ap.add_argument("--relatorio", help="grava o relatorio em markdown neste caminho")
    ap.add_argument("--out", help="grava o resultado completo (JSON) neste caminho")
    ap.add_argument("--texto", action="store_true", help="imprime a leitura humana")
    ap.add_argument("--sem-suite", action="store_true",
                    help="nao roda a suite pura/contra-prova; reusa os JSON em --out-dir")
    args = ap.parse_args(argv)

    identidade = None
    if args.identidade:
        try:
            identidade = _ler_json(args.identidade)
        except Exception as erro:
            print("ERRO: nao li --identidade: %s" % erro, file=sys.stderr)
            return EXIT_NAO_RODOU
    aceite = None
    if args.aceite:
        try:
            aceite = _ler_json(args.aceite)
        except Exception as erro:
            print("ERRO: nao li --aceite: %s" % erro, file=sys.stderr)
            return EXIT_NAO_RODOU
    try:
        obs_estilo = _carregar_observacoes(args.estilo_observacoes)
        obs_rstv = _carregar_observacoes(args.rstv_observacoes)
        obs_shrines = _carregar_observacoes(args.shrines_observacoes)
    except Exception as erro:
        print("ERRO: nao li as observacoes: %s" % erro, file=sys.stderr)
        return EXIT_NAO_RODOU

    resultado, codigo = consolidar(
        os.path.abspath(args.repo), os.path.abspath(args.out_dir),
        aut3_resultado=args.aut3_resultado, obs_estilo=obs_estilo, obs_rstv=obs_rstv,
        obs_shrines=obs_shrines, crit_rstv=args.rstv_criterios,
        crit_shrines=args.shrines_criterios, identidade=identidade, aceite=aceite,
        revisoes_path=args.revisoes, relatorio_path=args.relatorio,
        rodar_suite=not args.sem_suite)

    # Na tela vai o RESUMO; o JSON completo so no --out (o dump inteiro tem milhares de
    # linhas e nao ajuda quem le o terminal).
    resumo = {
        "esquema": resultado.get("esquema"), "tarefa": resultado.get("tarefa"),
        "identidade": resultado.get("identidade"), "criterios": resultado.get("criterios"),
        "por_frente": resultado.get("por_frente"),
        "status_tecnico": (resultado.get("relatorio") or {}).get("tecnico"),
        "revisoes": resultado.get("revisoes"),
        "aceite_humano": (resultado.get("relatorio") or {}).get("aceite_humano"),
        "publicacao": (resultado.get("relatorio") or {}).get("publicacao"),
        "relatorio_escrito": resultado.get("relatorio_escrito"),
        "medicao_estilo_suites": (resultado.get("medicao_estilo") or {}).get("suites"),
    }
    if args.out:
        _escrever(args.out, json.dumps(
            {k: v for k, v in resultado.items() if k not in ("texto", "markdown")},
            ensure_ascii=False, indent=2, default=str))
        resumo["saida_completa"] = os.path.abspath(args.out)
    print(json.dumps(resumo, ensure_ascii=False, indent=2, default=str))
    if args.texto and "texto" in resultado:
        print("\n" + resultado["texto"])
    return codigo


if __name__ == "__main__":
    sys.exit(main())
