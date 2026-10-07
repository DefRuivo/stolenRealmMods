#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""decisao.py - CIC-2: consolidacao por mod e roteiro humano RESIDUAL.

O QUE ESTE ARQUIVO E
--------------------
A camada de DECISAO do ciclo automatico antes da decisao humana. Recebe os
criterios produzidos pelos modulos de cenarios (offline e runtime) e por CIC-1,
CONFERE cada um CONTRA A REALIDADE (a evidencia existe? a identidade
fonte/DLL/config/cenario confere? o criterio e prova vinculante?) e separa tres
coisas que nao se misturam:

  * `falhas_automaticas`   -> o que a AUTOMACAO ainda tem de fazer. Volta ao
    ciclo; NUNCA e empurrado para o dono (criterio offline nao exercitado,
    evidencia que nao fecha, hash de bytes antigos, identidade faltando).
  * `pendencias_humanas`   -> so julgamento visual residual OU autorizacao
    necessaria, com motivo e instrucao concreta e CURTO (agregado por mod+tipo,
    nao o checklist inteiro).
  * `pronto_para_decisao`, `aceite_humano` e `publicacao` -> tres ESTADOS
    SEPARADOS: a automacao terminar nao aceita nem publica.

REGRA QUE NAO SE DOBRA: NUNCA OK POR ROTULO. Um criterio que se declara OK so
conta como prova vinculante se (a) nao e `fixture` (fixture testa o avaliador,
nao o produto), (b) tem evidencia ATUAL e os arquivos existem (sha conferido e,
quando a identidade traz o manifest da coleta, coerente com ele), (c) a
identidade e suficiente (fonte_sha E dll_sha) e os hashes declarados batem com
ela, e (d) — no contrato positivo de runtime — a CADEIA DE PROVA esta completa:
`prova_runtime=true`, `sessao`, `fonte_sha`, `dll_sha` (+ `config_sha` quando
config for relevante), CONFRONTADOS com a identidade da coleta. Ausencia/falha
de cadeia => NAO_EXERCITADO/INDETERMINADO, NUNCA OK (`prova_runtime=false`
jamais vincula). Faltando qualquer coisa, o criterio vira falha AUTOMATIZAVEL —
jamais tarefa humana.

QUEM VAI AO DONO (reduzir o trabalho humano de verdade): so (i) autorizacao
REALMENTE necessaria (`autorizacao_necessaria=true` ou `tipo_pendencia=autorizacao`)
e (ii) julgamento visual EXPLICITAMENTE indicado (`tipo_pendencia=julgamento_visual`,
`julgamento_humano`). Lacuna de probe/campo/coleta/preparacao e falha AUTOMATIZAVEL
(fila de agente) — nao se manda todo `runtime` ausente ao humano por padrao. A
instrucao ESPECIFICA do criterio entra no roteiro, nao a generica.

Reusa os formatos ja existentes: o criterio tem os campos de
`CICLO-VALIDACAO-escopo.md` e a identidade e `{fonte_sha, dll_sha, ...}` (podem
faltar; faltando, nada e OK). Sem dependencia externa: so a stdlib.

Tres pontos que a integracao com os produtores (CIC-3/CIC-4) fixou e que valem
como contrato: (1) hash declarado pelo criterio tambem em bloco aninhado
(`hashes`/`cadeia`) e CONFRONTADO com a identidade — o criterio nao se
auto-absolve; (2) o manifest da COLETA manda, o do criterio nao pode contradize-lo
para o mesmo arquivo; (3) agregar o roteiro por (mod, tipo) NAO apaga instrucao:
instrucoes distintas ficam todas visiveis, com rastreio por criterio.

CLI:
    python decisao.py --criterios criterios.json [--identidade ident.json]
        [--aceite aceite.json] [--repo DIR] [--resultado saida.json] [--texto]
Exit: 0 = pronto_para_decisao (decisao humana a tomar) · 1 = ha falha automatica
      (volta ao ciclo) · 2 = NAO CONSEGUI RODAR / sem criterios / entrada invalida.
"""
import argparse
import hashlib
import json
import os
import sys

ESQUEMA = "CIC-2/1"
EXIT_OK, EXIT_FALHOU, EXIT_NAO_RODOU = 0, 1, 2

ESTADOS = ("OK", "REPROVADO", "NAO_EXERCITADO", "INDETERMINADO")
CLASSES = ("offline", "runtime")
PROCEDENCIAS = ("execucao", "runtime", "fixture")

# classificado de CADA criterio
OK_VINCULANTE = "OK_VINCULANTE"
FALHA_AUTOMATICA = "FALHA_AUTOMATICA"
PENDENCIA_HUMANA = "PENDENCIA_HUMANA"
NAO_CONTA_COMO_PROVA = "NAO_CONTA_COMO_PROVA"

# severidade da falha automatica (define o rotulo de estado do mod)
SEV_REPROVADO = "REPROVADO"
SEV_NAO_EXERCITADO = "NAO_EXERCITADO"


class ErroDecisao(ValueError):
    """Entrada de topo invalida (nao e lista de criterios etc.)."""


# --------------------------------------------------------------- utilidades

def sha256_file(caminho):
    """sha256 hex do arquivo, ou None se nao existir / nao puder ser lido."""
    if not caminho or not os.path.isfile(caminho):
        return None
    h = hashlib.sha256()
    try:
        with open(caminho, "rb") as fh:
            for bloco in iter(lambda: fh.read(1 << 20), b""):
                h.update(bloco)
    except OSError:
        return None
    return h.hexdigest()


def _texto(v):
    return str(v).strip() if isinstance(v, str) else ""


def identidade_suficiente(identidade):
    """Identidade so e suficiente com fonte_sha E dll_sha (padrao dos cenarios).

    Podem faltar; faltando, nenhum criterio pode sair OK — e a lacuna e
    AUTOMATIZAVEL (anexar a identidade da rodada), nunca tarefa do dono.
    """
    if not isinstance(identidade, dict):
        return False
    return bool(_texto(identidade.get("fonte_sha"))) and bool(_texto(identidade.get("dll_sha")))


def _hashes_conhecidos(identidade):
    """Mapa chave->sha que a identidade CONHECE (fonte/dll/config/cenario).

    Aceita chaves `*_sha` no topo e um bloco `artefatos`/`hashes` (dict nome->sha)
    para config/cenario que nao tenham nome `*_sha`.
    """
    conhecidos = {}
    idn = identidade if isinstance(identidade, dict) else {}
    for k, v in idn.items():
        if isinstance(k, str) and k.endswith("_sha") and isinstance(v, str) and v.strip():
            conhecidos[k] = v.strip()
    for grupo in ("artefatos", "hashes"):
        bloco = idn.get(grupo)
        if isinstance(bloco, dict):
            for kk, vv in bloco.items():
                if isinstance(vv, str) and vv.strip():
                    conhecidos[str(kk)] = vv.strip()
    return conhecidos


def _declarados_hashes(criterio):
    """Hashes que o PROPRIO criterio declara (topo `*_sha` ou dict `hashes`)."""
    d = {}
    for k, v in criterio.items():
        if isinstance(k, str) and k.endswith("_sha") and isinstance(v, str) and v.strip():
            d[k] = v.strip()
    bloco = criterio.get("hashes")
    if isinstance(bloco, dict):
        for kk, vv in bloco.items():
            if isinstance(vv, str) and vv.strip():
                d[str(kk)] = vv.strip()
    return d


def _resolver_sha(conhecidos, chave):
    """sha conhecido para `chave`, com o apelido do contrato: `config_sha` x artefato de config.

    O contrato nomeia `config_sha` para a config relevante; a identidade/manifest
    pode expor a config por caminho (`config/*.cfg`). Fora desse apelido, o
    casamento e EXATO (nao se confirma hash por semelhanca de nome).
    """
    if chave in conhecidos and conhecidos[chave]:
        return conhecidos[chave]
    if chave == "config_sha":
        cand = sorted({v for k, v in conhecidos.items() if v and "config" in k.lower()})
        if len(cand) == 1:
            return cand[0]
    return None


def _evidencias(criterio):
    """Normaliza `evidencia` para [(caminho, sha|None), ...]."""
    v = criterio.get("evidencia")
    if v is None:
        return []
    if isinstance(v, str):
        v = [v]
    if not isinstance(v, list):
        return []
    out = []
    for e in v:
        if isinstance(e, str):
            if e.strip():
                out.append((e.strip(), None))
        elif isinstance(e, dict):
            cam = e.get("caminho") or e.get("arquivo") or e.get("path") or e.get("evidencia")
            sha = e.get("sha256") or e.get("hash")
            if cam and str(cam).strip():
                out.append((str(cam).strip(), str(sha).strip() if sha else None))
    return out


def _verifica_evidencia(evidencias, raiz):
    """Confere que cada evidencia EXISTE e, se o criterio declara sha, que bate."""
    if not evidencias:
        return ["sem evidencia (label OK nao basta)"]
    problemas = []
    for cam, sha in evidencias:
        caminho = cam if os.path.isabs(cam) else os.path.join(raiz, cam)
        if not os.path.exists(caminho):
            problemas.append("evidencia ausente: %s" % cam)
            continue
        if sha:
            real = sha256_file(caminho)
            if real is None:
                problemas.append("evidencia ilegivel: %s" % cam)
            elif real != sha:
                problemas.append("evidencia com hash divergente: %s" % cam)
    return problemas


def _sinal_humano(criterio):
    """Tipo de pendencia humana EXPLICITO no criterio, ou None (=> tecnico/automatizavel).

    Contrato (`CICLO-VALIDACAO-escopo.md`, "Correcoes funcionais da primeira
    integracao"): so vao ao dono (i) autorizacao REALMENTE necessaria —
    `autorizacao_necessaria is True` ou `tipo_pendencia == "autorizacao"` — e
    (ii) julgamento visual EXPLICITAMENTE indicado — `tipo_pendencia ==
    "julgamento_visual"`, `julgamento_humano` (string) ou `requer_humano`
    contendo "visual". Qualquer outra coisa (lacuna de probe/campo/coleta/
    preparacao) e falha AUTOMATIZAVEL: volta ao ciclo, nunca ao dono.
    """
    tp = _texto(criterio.get("tipo_pendencia")).lower()
    if tp in ("autorizacao", "julgamento_visual"):
        return tp
    if criterio.get("autorizacao_necessaria") is True:
        return "autorizacao"
    j = criterio.get("julgamento_humano")
    if isinstance(j, str) and j.strip():
        return "julgamento_visual"
    req = criterio.get("requer_humano")
    if isinstance(req, str) and "visual" in req.lower():
        return "julgamento_visual"
    return None


def _valor_cadeia(criterio, nome):
    """Le um campo da cadeia de prova no topo do criterio ou dentro de hashes/artefatos."""
    v = criterio.get(nome)
    if v is None:
        for grupo in ("hashes", "artefatos", "cadeia"):
            bloco = criterio.get(grupo)
            if isinstance(bloco, dict) and bloco.get(nome) is not None:
                v = bloco.get(nome)
                break
    return v


def _sha_fonte(criterio):
    return _valor_cadeia(criterio, "fonte_sha") or _valor_cadeia(criterio, "hash_fonte")


def _mapa_manifest(fonte):
    """basename -> sha256 a partir de um manifest da coleta (`{artefatos:[{arquivo,sha256}]}`)."""
    if not isinstance(fonte, dict):
        return {}
    m = fonte.get("manifest")
    if isinstance(m, dict):
        arts = m.get("artefatos")
    elif isinstance(m, list):
        arts = m
    else:
        arts = None
    saida = {}
    for a in arts or []:
        if not isinstance(a, dict):
            continue
        nome = a.get("arquivo") or a.get("nome") or a.get("caminho")
        sha = a.get("sha256") or a.get("sha")
        if nome and sha:
            saida[os.path.basename(str(nome))] = str(sha)
    return saida


def _cadeia_runtime(criterio, identidade):
    """Problemas da CADEIA de prova de runtime (vazio = completa).

    Runtime nao se aprova por rotulo: exige `prova_runtime=true`, `sessao`,
    `fonte_sha` e `dll_sha` no proprio criterio (e `config_sha` quando
    `config_relevante`), E o confronto dos valores declarados com a identidade da
    coleta (a identidade precisa trazer `sessao`; declarar hash nao basta).
    """
    problemas = []
    if criterio.get("prova_runtime") is not True:
        problemas.append("prova_runtime ausente/false (runtime nao se aprova por rotulo)")
    ident = identidade if isinstance(identidade, dict) else {}
    sessao = _texto(criterio.get("sessao"))
    sessao_ident = _texto(ident.get("sessao"))
    if not sessao:
        problemas.append("sem sessao da coleta")
    elif sessao_ident and sessao != sessao_ident:
        problemas.append("sessao da observacao difere da identidade da rodada")
    if not _texto(_sha_fonte(criterio)):
        problemas.append("sem fonte_sha no criterio")
    if not _texto(_valor_cadeia(criterio, "dll_sha")):
        problemas.append("sem dll_sha no criterio")
    if criterio.get("config_relevante") and not _texto(_valor_cadeia(criterio, "config_sha")):
        problemas.append("config relevante sem config_sha")
    for campo in ("fonte_sha", "dll_sha", "config_sha"):
        declarado = _texto(_valor_cadeia(criterio, campo))
        conhecido = _resolver_sha(_hashes_conhecidos(ident), campo)
        if declarado and conhecido and declarado != conhecido:
            problemas.append("%s do criterio difere da identidade da rodada" % campo)
    return problemas


def _coerencia_manifesto(evidencias, criterio, identidade, raiz):
    """Evidencia x manifest: o sha do arquivo em disco tem de bater com o manifest.

    O manifest da COLETA (identidade) manda: se o criterio declarar um manifest que
    contradiz o da coleta para o mesmo arquivo, o criterio NAO pode se auto-absolver
    (`_mapa_manifest` do criterio nao sobrescreve o da identidade).
    """
    m_coleta = _mapa_manifest(identidade)
    m_crit = _mapa_manifest(criterio)
    problemas = []
    for nome, sha_crit in m_crit.items():
        if nome in m_coleta and m_coleta[nome] != sha_crit:
            problemas.append("manifest do criterio contradiz o da coleta: %s" % nome)
    manifest = dict(m_crit)
    manifest.update(m_coleta)
    for cam, _sha in evidencias:
        ref = manifest.get(os.path.basename(cam))
        if not ref:
            continue
        caminho = cam if os.path.isabs(cam) else os.path.join(raiz, cam)
        real = sha256_file(caminho)
        if real is None:
            problemas.append("evidencia do manifest ilegivel: %s" % cam)
        elif real != ref:
            problemas.append("evidencia difere do manifest da coleta: %s" % cam)
    return problemas


def _instrucao_humana(criterio, tipo):
    explicito = _texto(criterio.get("instrucoes_humanas"))
    if explicito:
        return explicito
    j = criterio.get("julgamento_humano")
    if isinstance(j, str) and j.strip():
        return j.strip()
    req = criterio.get("requer_humano")
    if isinstance(req, str) and req.strip():
        return req.strip()
    if tipo == "julgamento_visual":
        return ("Abrir o jogo no alvo do criterio e confirmar a aparencia/UX; "
                "registrar aceite humano (o dado tecnico ja esta provado).")
    return ("Autorizar UMA frente runtime (AUT-4/5/6) e reexecutar o ciclo; "
            "sem autorizacao nada em jogo e lido.")


def _item(cid, mod, classe, procedencia, estado, classificacao, prova, motivo,
          problemas=None, nao_confirmados=None, severidade=None, tipo_humano=None,
          criterio=None):
    criterio = criterio or {}
    return {
        "id": cid,
        "mod": mod,
        "classe": classe,
        "procedencia": procedencia,
        "estado": estado,
        "estado_efetivo": classificacao,
        "classificacao": classificacao,
        "prova_vinculante": bool(prova),
        "severidade": severidade,
        "motivo_decisao": motivo,
        "problemas": list(problemas or []),
        "hashes_nao_confirmados": list(nao_confirmados or []),
        "tipo_humano": tipo_humano,
        "instrucoes_humanas": _texto(criterio.get("instrucoes_humanas")) or None,
        "julgamento_humano": criterio.get("julgamento_humano"),
        "tipo_pendencia": criterio.get("tipo_pendencia"),
        "autorizacao_necessaria": criterio.get("autorizacao_necessaria"),
        "lacuna_probe": criterio.get("lacuna_probe"),
        "prova_runtime": criterio.get("prova_runtime"),
        "sessao": criterio.get("sessao"),
        "esperado": criterio.get("esperado"),
        "observado": criterio.get("observado"),
        "evidencia": [c for c, _ in _evidencias(criterio)],
        "motivo": criterio.get("motivo"),
        "tarefa_origem": criterio.get("tarefa_origem"),
    }


# --------------------------------------------------------------- criterio

def normalizar_criterio(criterio, identidade, raiz):
    """Classifica UM criterio: prova vinculante, falha automatica ou pendencia humana.

    Fail-closed: qualquer duvida sobre a prova vira falha AUTOMATIZAVEL (volta ao
    ciclo), nunca tarefa do humano.
    """
    if not isinstance(criterio, dict):
        return _item("<nao-objeto>", "transversal", "", "", "INDETERMINADO",
                     FALHA_AUTOMATICA, False,
                     "criterio nao e um objeto JSON: automatizavel",
                     ["criterio malformado"], severidade=SEV_REPROVADO)

    cid = criterio.get("id") or "<sem-id>"
    mod = criterio.get("mod") or "transversal"
    classe = _texto(criterio.get("classe")).lower()
    procedencia = _texto(criterio.get("procedencia")).lower()
    estado = _texto(criterio.get("estado")).upper()
    ident_ok = identidade_suficiente(identidade)

    # (1) malformado -> defeito do pipeline, automatizavel
    problemas = []
    if not criterio.get("id"):
        problemas.append("criterio sem 'id'")
    if estado not in ESTADOS:
        problemas.append("estado invalido/ausente: %r" % criterio.get("estado"))
    if classe not in CLASSES:
        problemas.append("classe invalida/ausente: %r" % criterio.get("classe"))
    if procedencia not in PROCEDENCIAS:
        problemas.append("procedencia invalida/ausente: %r" % criterio.get("procedencia"))
    if problemas:
        return _item(cid, mod, classe, procedencia, estado or "INDETERMINADO",
                     FALHA_AUTOMATICA, False, "criterio malformado: " + "; ".join(problemas),
                     problemas, severidade=SEV_REPROVADO, criterio=criterio)

    # (2) fixture NUNCA prova produto (testa o avaliador)
    if procedencia == "fixture":
        if estado == "REPROVADO":
            return _item(cid, mod, classe, procedencia, estado, FALHA_AUTOMATICA, False,
                         "fixture REPROVOU: a regra/avaliador falhou (automatizavel)",
                         ["fixture reprovada"], severidade=SEV_REPROVADO, criterio=criterio)
        return _item(cid, mod, classe, procedencia, estado, NAO_CONTA_COMO_PROVA, False,
                     "procedencia fixture: testa o avaliador, nao comprova offline/runtime",
                     criterio=criterio)

    # (3) incoerencia classe x procedencia
    incoerente = []
    if classe == "runtime" and procedencia != "runtime":
        incoerente.append("classe runtime exige procedencia runtime (veio %r)" % procedencia)
    if classe == "offline" and procedencia == "runtime":
        incoerente.append("classe offline com procedencia runtime e incoerente")
    if incoerente:
        return _item(cid, mod, classe, procedencia, estado, FALHA_AUTOMATICA, False,
                     "criterio incoerente: " + "; ".join(incoerente), incoerente,
                     severidade=SEV_REPROVADO, criterio=criterio)

    # (4) REPROVADO -> falha automatica (volta ao ciclo)
    if estado == "REPROVADO":
        return _item(cid, mod, classe, procedencia, estado, FALHA_AUTOMATICA, False,
                     criterio.get("motivo") or "criterio REPROVADO: falha acionavel pelo ciclo",
                     severidade=SEV_REPROVADO, criterio=criterio)

    # (5) nao exercitado / indeterminado
    if estado in ("NAO_EXERCITADO", "INDETERMINADO"):
        if not ident_ok:
            return _item(cid, mod, classe, procedencia, estado, FALHA_AUTOMATICA, False,
                         "identidade insuficiente (fonte_sha/dll_sha): automatizavel — anexar a identidade da rodada",
                         ["identidade insuficiente"], severidade=SEV_NAO_EXERCITADO, criterio=criterio)
        if classe == "offline":
            return _item(cid, mod, classe, procedencia, estado, FALHA_AUTOMATICA, False,
                         "criterio offline nao exercitado: automatizavel, volta ao ciclo (nao e tarefa do dono)",
                         ["offline nao exercitado"], severidade=SEV_NAO_EXERCITADO, criterio=criterio)
        # classe runtime: humano SO com sinal EXPLICITO no criterio; o resto
        # (lacuna de probe/campo/coleta/preparacao) e falha automatica (fila de agente).
        tipo = _sinal_humano(criterio)
        if tipo is None:
            lacuna = _texto(criterio.get("lacuna_probe"))
            motivo_orig = _texto(criterio.get("motivo"))
            if lacuna:
                motivo = ("lacuna tecnica de runtime (probe/campo/coleta/preparacao): "
                          "automatizavel, volta ao ciclo — NAO e tarefa do dono — " + lacuna)
            elif motivo_orig:
                motivo = motivo_orig + " (automatizavel: lacuna tecnica, nao vai ao dono)"
            else:
                motivo = ("lacuna tecnica de runtime (probe/campo/coleta/preparacao): "
                          "automatizavel, volta ao ciclo — NAO e tarefa do dono")
            return _item(cid, mod, classe, procedencia, estado, FALHA_AUTOMATICA, False,
                         motivo, ["lacuna tecnica de runtime"], severidade=SEV_NAO_EXERCITADO,
                         criterio=criterio)
        motivo = _texto(criterio.get("motivo")) or (
            "rodada runtime ainda nao autorizada/executada" if tipo == "autorizacao"
            else "precisa de julgamento visual residual")
        return _item(cid, mod, classe, procedencia, estado, PENDENCIA_HUMANA, False,
                     motivo, tipo_humano=tipo, criterio=criterio)

    # (6) estado OK -> so vincula com identidade suficiente + cadeia runtime + evidencia + hashes
    if not ident_ok:
        return _item(cid, mod, classe, procedencia, estado, FALHA_AUTOMATICA, False,
                     "OK declarado SEM identidade suficiente (fonte_sha/dll_sha): nao e aceito",
                     ["identidade insuficiente"], severidade=SEV_REPROVADO, criterio=criterio)

    # (6a) contrato positivo de runtime: prova_runtime + sessao + fonte_sha/dll_sha
    #      (+ config_sha quando config relevante), confrontados com a identidade da
    #      coleta. So o rotulo `runtime` NAO fecha OK; ausencia/falha de cadeia =>
    #      NAO_EXERCITADO (falha automatica), nunca OK.
    if classe == "runtime":
        cadeia = _cadeia_runtime(criterio, identidade)
        if cadeia:
            return _item(cid, mod, classe, procedencia, estado, FALHA_AUTOMATICA, False,
                         "cadeia de prova runtime incompleta: " + "; ".join(cadeia)
                         + " (nunca OK por rotulo)",
                         cadeia, severidade=SEV_NAO_EXERCITADO, criterio=criterio)

    evidencias = _evidencias(criterio)
    problemas = _verifica_evidencia(evidencias, raiz)
    problemas += _coerencia_manifesto(evidencias, criterio, identidade, raiz)
    if problemas:
        return _item(cid, mod, classe, procedencia, estado, FALHA_AUTOMATICA, False,
                     "evidencia/identidade nao fecham: " + "; ".join(problemas), problemas,
                     severidade=SEV_REPROVADO, criterio=criterio)

    conhecidos = _hashes_conhecidos(identidade)
    nao_confirmados = []
    for chave, valor in _declarados_hashes(criterio).items():
        ref = _resolver_sha(conhecidos, chave)
        if ref is None:
            nao_confirmados.append(chave)
        elif ref != valor:
            return _item(cid, mod, classe, procedencia, estado, FALHA_AUTOMATICA, False,
                         "hash %s refere bytes antigos/errados: aprovacao anterior invalidada" % chave,
                         ["hash divergente: %s" % chave], severidade=SEV_REPROVADO, criterio=criterio)
    if nao_confirmados:
        return _item(cid, mod, classe, procedencia, estado, FALHA_AUTOMATICA, False,
                     "hash nao confirmado pela identidade: %s (automatizavel)" % ", ".join(sorted(nao_confirmados)),
                     ["hash nao confirmado"], nao_confirmados, severidade=SEV_NAO_EXERCITADO,
                     criterio=criterio)

    # (7) prova vinculante (com julgamento humano opcional, sem perder a prova)
    tipo = _sinal_humano(criterio)
    if tipo is not None:
        motivo = ("prova tecnica fechou; resta "
                  + ("julgamento visual residual" if tipo == "julgamento_visual"
                     else "autorizacao necessaria"))
        return _item(cid, mod, classe, procedencia, estado, PENDENCIA_HUMANA, True,
                     motivo, tipo_humano=tipo, criterio=criterio)
    return _item(cid, mod, classe, procedencia, estado, OK_VINCULANTE, True,
                 "prova vinculante (offline/runtime real, evidencia presente, identidade confere)",
                 criterio=criterio)


# --------------------------------------------------------------- consolidacao

def _sintetico_sem_prova(mod):
    return _item("%s:sem-prova-vinculante" % mod, mod, "offline", "execucao",
                 "NAO_EXERCITADO", FALHA_AUTOMATICA, False,
                 "mod so tem criterios sem prova vinculante (fixture/rotulo): automatizavel — "
                 "gerar evidencia real (offline/runtime) ligada a identidade",
                 ["sem prova vinculante"], severidade=SEV_NAO_EXERCITADO)


def _estado_mod(bucket):
    if any(f.get("severidade") == SEV_REPROVADO for f in bucket["falhas_automaticas"]):
        return "REPROVADO"
    if bucket["falhas_automaticas"]:
        return "NAO_EXERCITADO"
    if bucket["pendencias_humanas"]:
        return "NAO_EXERCITADO"
    if bucket["ok_vinculantes"]:
        return "OK"
    return "NAO_EXERCITADO"


def _agrega_roteiro(pendencias):
    """Residual CURTO: um item por (mod, tipo), com os ids agregados.

    Agregar NAO pode apagar a instrucao: instrucoes distintas do mesmo (mod, tipo)
    sao concatenadas (uma vez cada) em `instrucoes`, e `instrucoes_por_criterio`
    guarda qual criterio pediu o que.
    """
    ordem = {}
    for n in pendencias:
        tipo = n["tipo_humano"] or "autorizacao"
        chave = (n["mod"], tipo)
        item = ordem.setdefault(chave, {
            "mod": n["mod"], "tipo": tipo, "criterios": [], "motivo": "",
            "classe": n["classe"], "instrucoes": [], "instrucoes_por_criterio": {},
        })
        item["criterios"].append(n["id"])
        instrucao = _instrucao_humana(n, tipo)
        item["instrucoes_por_criterio"][n["id"]] = instrucao
        if instrucao and instrucao not in item["instrucoes"]:
            item["instrucoes"].append(instrucao)
        if not item["motivo"]:
            item["motivo"] = n.get("motivo_decisao") or ""
    itens = []
    for item in ordem.values():
        item = dict(item)
        item["criterios"] = sorted(set(item["criterios"]))
        item["total"] = len(item["criterios"])
        item["instrucoes"] = "\n".join(item["instrucoes"])
        itens.append(item)
    return sorted(itens, key=lambda i: (i["mod"], i["tipo"]))


def _normaliza_aceite(aceite):
    base = {"pronunciado": False, "status": "NAO_PRONUNCIADO", "por_mod": {}}
    if aceite is None:
        return base
    if isinstance(aceite, dict):
        saida = dict(aceite)
        saida.setdefault("pronunciado", True)
        saida.setdefault("status", "PRONUNCIADO")
        saida.setdefault("por_mod", {})
        return saida
    base.update({"pronunciado": True,
                 "status": aceite if isinstance(aceite, str) else repr(aceite)})
    return base


def _aceite_inconsistente(aceite, por_mod):
    """Aceite humano para mod com falha automatica e INCONSISTENTE (nao esconder).

    Aceita as duas formas de aceite por mod: dentro de `por_mod` ou no proprio
    topo keyed pelo nome do mod (`{"BetterTooltips": {"aceito": true}}`).
    """
    mods = set()
    por_mod_aceite = dict(aceite.get("por_mod") or {})
    for chave, valor in aceite.items():
        if isinstance(valor, dict) and "aceito" in valor:
            por_mod_aceite.setdefault(chave, valor)
    for mod, v in por_mod_aceite.items():
        if isinstance(v, dict) and v.get("aceito") is True:
            mods.add(mod)
    if aceite.get("aceito") is True:
        mods |= set(por_mod)
    fora = sorted(m for m in mods if m in por_mod and por_mod[m]["falhas_automaticas"])
    if aceite.get("aceito") is True and any(b["falhas_automaticas"] for b in por_mod.values()):
        fora.append("(global: ha falhas automaticas)")
    return fora


def sumario_humano(dec):
    """Resumo CURTO em PT-BR: so o residual que precisa do dono + o estado real."""
    linhas = []
    roteiro = dec.get("roteiro_humano", {}).get("itens", [])
    linhas.append("ROTEIRO HUMANO (residual) — %d item(ns):" % len(roteiro))
    if roteiro:
        for i in roteiro:
            acao = "AUTORIZAR rodada runtime" if i["tipo"] == "autorizacao" else "JULGAR visual/UX"
            # instrucoes distintas do mesmo (mod, tipo) ficam TODAS visiveis (agregar nao apaga)
            passos = [p.strip() for p in (i.get("instrucoes") or "").splitlines() if p.strip()]
            if not passos:
                passos = [""]
            linhas.append("- [%s] %s:" % (i["mod"], acao))
            for p in passos:
                linhas.append("    * %s" % p)
            linhas.append("    (criterios: %s)" % ", ".join(i["criterios"]))
    else:
        linhas.append("- nada: nenhuma pendencia humana.")
    falhas = dec.get("falhas_automaticas", [])
    linhas.append("")
    linhas.append("FALHAS AUTOMATICAS (voltam ao ciclo, NAO ao dono) — %d:" % len(falhas))
    for f in falhas:
        linhas.append("- [%s] %s: %s" % (f["mod"], f["id"], f["motivo_decisao"]))
    if not falhas:
        linhas.append("- nenhuma.")
    linhas.append("")
    linhas.append("PRONTO PARA DECISAO: %s — %s"
                  % ("SIM" if dec.get("pronto_para_decisao") else "NAO",
                     dec.get("motivo_pronto_para_decisao", "")))
    aceite = dec.get("aceite_humano", {})
    linhas.append("ACEITE HUMANO: %s (estado separado)" % aceite.get("status", "?"))
    linhas.append("PUBLICACAO: %s (estado separado)" % dec.get("publicacao", {}).get("status", "?"))
    if dec.get("aceite_inconsistente"):
        linhas.append("ATENCAO aceite inconsistente com falhas: %s"
                      % ", ".join(dec["aceite_inconsistente"]))
    return "\n".join(linhas)


def consolidar(criterios, identidade, aceite_humano=None):
    """Consolida criterios por mod e devolve a decisao estruturada.

    Devolve dict com: por_mod, falhas_automaticas, pendencias_humanas (residual
    CURTO), pronto_para_decisao, aceite_humano, publicacao, roteiro_humano,
    resumo e aceite_inconsistente. Nada e inferido de rotulo OK: a prova e
    reconferida contra evidencia + identidade.
    """
    if criterios is None:
        criterios = []
    if not isinstance(criterios, list):
        raise ErroDecisao("criterios tem de ser uma lista, veio %r" % type(criterios).__name__)
    identidade = identidade if isinstance(identidade, dict) else {}
    raiz = os.path.abspath(str(identidade.get("raiz") or os.getcwd()))

    norm = [normalizar_criterio(c, identidade, raiz) for c in criterios]

    por_mod = {}
    for n in norm:
        mod = n["mod"]
        b = por_mod.setdefault(mod, {
            "mod": mod, "total": 0, "criterios": [], "falhas_automaticas": [],
            "pendencias_humanas": [], "ok_vinculantes": [], "nao_conta_como_prova": []})
        b["total"] += 1
        b["criterios"].append(n)
        cls = n["classificacao"]
        if cls == FALHA_AUTOMATICA:
            b["falhas_automaticas"].append(n)
        elif cls == PENDENCIA_HUMANA:
            b["pendencias_humanas"].append(n)
        elif cls == OK_VINCULANTE:
            b["ok_vinculantes"].append(n)
        else:
            b["nao_conta_como_prova"].append(n)

    # mod sem NENHUMA prova vinculante e sem pendencia humana: a lacuna e
    # AUTOMATIZAVEL (gerar evidencia real) — nunca vai ao dono.
    for mod, b in por_mod.items():
        if not b["ok_vinculantes"] and not b["pendencias_humanas"] and not b["falhas_automaticas"]:
            b["falhas_automaticas"].append(_sintetico_sem_prova(mod))
        b["estado"] = _estado_mod(b)

    falhas = [dict(n) for b in por_mod.values() for n in b["falhas_automaticas"]]
    pendencias_crit = [dict(n) for b in por_mod.values() for n in b["pendencias_humanas"]]
    pendencias = _agrega_roteiro(pendencias_crit)

    tem_prova = any(b["ok_vinculantes"] for b in por_mod.values())
    pronto = (not falhas) and (tem_prova or bool(pendencias))
    if falhas:
        motivo_pronto = ("NAO: %d falha(s) automatica(s) volta(m) ao ciclo; nada disso vai ao dono"
                         % len(falhas))
    elif not tem_prova and not pendencias:
        motivo_pronto = "NAO: sem criterios/prova vinculante (fixture nao prova o produto)"
    elif pendencias:
        motivo_pronto = ("SIM: automacao sem falhas; resta decisao humana (%d item(ns) no roteiro)"
                         % len(pendencias))
    else:
        motivo_pronto = "SIM: automacao sem falhas e sem pendencia humana; resta aceite/publicacao"

    aceite = _normaliza_aceite(aceite_humano)
    dec = {
        "esquema": ESQUEMA,
        "identidade": {
            "fonte_sha": identidade.get("fonte_sha"),
            "dll_sha": identidade.get("dll_sha"),
            "suficiente": identidade_suficiente(identidade),
            "conhecidos": sorted(_hashes_conhecidos(identidade)),
        },
        "por_mod": por_mod,
        "falhas_automaticas": falhas,
        "pendencias_humanas": pendencias,
        "pronto_para_decisao": pronto,
        "motivo_pronto_para_decisao": motivo_pronto,
        "aceite_humano": aceite,
        "publicacao": {
            "status": "NAO_VERIFICADO",
            "online": None,
            "motivo": ("publicacao e decisao do dono (Thunderstore imutavel); exige aceite humano "
                       "e consulta por pacote; fora desta rodada"),
            "aceite_humano_pronunciado": bool(aceite.get("pronunciado")),
        },
        "aceite_inconsistente": _aceite_inconsistente(aceite, por_mod),
        "resumo": {
            "mods": len(por_mod),
            "criterios": len(norm),
            "ok_vinculantes": sum(1 for n in norm if n["classificacao"] == OK_VINCULANTE),
            "falhas_automaticas": len(falhas),
            "pendencias_humanas": len(pendencias_crit),
            "nao_conta_como_prova": sum(1 for n in norm if n["classificacao"] == NAO_CONTA_COMO_PROVA),
        },
    }
    dec["roteiro_humano"] = {"total": len(pendencias), "itens": pendencias}
    dec["roteiro_humano"]["texto"] = sumario_humano(dec)
    return dec


# --------------------------------------------------------------- CLI

def _ler_json(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return json.load(fh)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="CIC-2: consolida criterios por mod e separa falha automatica de roteiro humano residual.")
    ap.add_argument("--criterios", required=True, help="arquivo JSON com a lista de criterios (ou {criterios:[...]})")
    ap.add_argument("--identidade", default=None, help="arquivo JSON com {fonte_sha, dll_sha, ...}")
    ap.add_argument("--aceite", default=None, help="arquivo JSON com o aceite humano (estado separado)")
    ap.add_argument("--repo", default=None, help="raiz para resolver caminhos de evidencia (default: cwd)")
    ap.add_argument("--resultado", "--out", dest="resultado", default=None, help="grava a decisao neste JSON")
    ap.add_argument("--texto", action="store_true", help="imprime tambem o resumo humano curto")
    args = ap.parse_args(argv)

    try:
        bruto = _ler_json(args.criterios)
    except (OSError, ValueError) as erro:
        print("ERRO: nao li --criterios: %s" % erro, file=sys.stderr)
        return EXIT_NAO_RODOU

    if isinstance(bruto, dict):
        criterios = bruto.get("criterios") or []
        identidade = dict(bruto.get("identidade") or {})
    elif isinstance(bruto, list):
        criterios = bruto
        identidade = {}
    else:
        print("ERRO: --criterios tem de ser lista ou {'criterios': [...]}", file=sys.stderr)
        return EXIT_NAO_RODOU

    if not isinstance(criterios, list):
        print("ERRO: bloco 'criterios' nao e lista", file=sys.stderr)
        return EXIT_NAO_RODOU

    if args.identidade:
        try:
            identidade.update(_ler_json(args.identidade))
        except (OSError, ValueError) as erro:
            print("ERRO: nao li --identidade: %s" % erro, file=sys.stderr)
            return EXIT_NAO_RODOU
    if args.repo:
        identidade["raiz"] = os.path.abspath(args.repo)

    aceite = None
    if args.aceite:
        try:
            aceite = _ler_json(args.aceite)
        except (OSError, ValueError) as erro:
            print("ERRO: nao li --aceite: %s" % erro, file=sys.stderr)
            return EXIT_NAO_RODOU

    dec = consolidar(criterios, identidade, aceite_humano=aceite)
    texto = json.dumps(dec, ensure_ascii=False, indent=2)
    if args.resultado:
        with open(args.resultado, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(texto + "\n")
    print(texto)
    if args.texto:
        print("\n" + dec["roteiro_humano"]["texto"])
    if dec["falhas_automaticas"]:
        return EXIT_FALHOU
    if not criterios:
        return EXIT_NAO_RODOU
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
