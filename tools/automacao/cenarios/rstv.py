#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rstv.py - CIC-3: avaliadores executaveis RSTV para o ciclo automatico.

CONTRATO (docs/automacao/CICLO-VALIDACAO-escopo.md, v1 + correcoes funcionais)
-----------------------------------------------------------------------------
    avaliar(observacoes, identidade) -> lista de criterios

* `identidade`: dict com `fonte_sha` e `dll_sha` (e `config_sha` quando a config
  for relevante). Podem faltar — e, faltando, NUNCA sai OK.
* `observacoes`: lista de dicts. O adaptador LE o formato AUT-4/CIC-5 REAL
  (`tools/automacao/runtime/coletor.py`), nas DUAS formas que existem hoje:
    1) leitura CRUA do probe (`aut4probe.json`): campos planos `objeto`,
       `texto_bruto`, `texto_renderizado`, `personagem`, `geometria`, `owners`;
    2) leitura NORMALIZADA de `coletor.consolidar`: bloco `campos` no formato
       `{campo: {estado, valor, alvo}}` + `sessao`/`hash_fonte` injetados do
       TOPO do JSON do probe (`anexar_contexto`).
  Nao impoe formato novo ao coletor — le o que ja existe. NAO se inventa campo
  de emissao: o que o probe/coletor nao emite sai como LACUNA declarada.
* Criterio: `id`, `mod`, `estado` (OK/REPROVADO/NAO_EXERCITADO/INDETERMINADO),
  `classe` (offline/runtime), `procedencia` (execucao/runtime/fixture),
  `esperado`, `observado`, `evidencia`, `motivo`, `tarefa_origem`. Campos extras
  rastreaveis: `prova_runtime`, `sessao`, `fonte_sha`, `dll_sha`, `config_sha`,
  `lacuna_probe`, `tipo_pendencia`, `autorizacao_necessaria`.

REGRA DE HONESTIDADE (a mesma do AUT-3/AUT-4 e das correcoes do ciclo)
---------------------------------------------------------------------
* AUSENTE / incompleto / malformado NUNCA vira OK — mesmo com `dados`/`contrib`
  marcados e mesmo com identidade valida. `motivos` (falta/incompletude) forca
  NAO_EXERCITADO; quando o confronto e IMPOSSIVEL (sem alvo/dependencia), sai
  INDETERMINADO. Defeito detectado continua REPROVADO.
* FIXTURE testa o AVALIADOR, nao comprova runtime. Com procedencia `fixture`, a
  AUSENCIA de defeito NAO fecha OK (sai NAO_EXERCITADO) — mas um DEFEITO plantado
  continua REPROVADO: e assim que um controle negativo prova que a regra pega o
  defeito.
* Sem `fonte_sha` E `dll_sha` nao existe OK possivel.
* `procedencia=runtime` exige `sessao` e `hash_fonte` nao vazios; o `hash_fonte`
  do coletor CIC-5 e o sha256 da **DLL** do probe, e tem de casar com o `dll_sha`
  da identidade (bytes atuais). Hash declarado que DIVERGE -> INDETERMINADO
  (rodada de bytes diferentes); hash declarado que a identidade NAO conhece ->
  NAO_EXERCITADO (cadeia incompleta). `fonte_sha`/`dll_sha` declarados por nome
  tambem sao conferidos. Nao se exige prova criptografica nova: a IDENTIDADE do
  artefato esperado e o criterio suficiente contra dado lido ausente/mismatch.
* Dados vivos ausentes (campo/coleta/preparacao) sao LACUNA TECNICA: o criterio
  carrega `lacuna_probe` e `tipo_pendencia='tecnica'` (autorizacao_necessaria
  False por default, nunca "todo runtime ausente e do dono").
* `avaliar` SEMPRE devolve o conjunto canonico EXATO das 7 capacidades, inclusive
  quando dado malformado derruba uma capacidade (id por nome de funcao, nunca
  derivado de split de string).

FECHAMENTO F1-F7 (parecer CIC-3R) — verde GLOBAL exige leitura COMPLETA e
BEM-FORMADA de CADA dimensao do criterio
-----------------------------------------------------------------------
O funil reprovava o valor ERRADO, mas fechava verde quando a dimensao nao tinha
sido lida ou a contagem vinha `null` (achado A3 do parecer). Cada achado F1-F7
virou regra explicita:

* **F1** `RSTV-6-readonly-skills-pontos`: o criterio anuncia skills E pontos —
  ler um par so NAO fecha OK; a dimensao nunca lida vira lacuna declarada.
* **F2** `RSTV-21-tooltip-restauracao`: `janelas_duplicadas` so prova AUSENCIA
  com contagem OBSERVADA valida (numero finito >= 0); `null`/negativo/bool/lista
  = leitura malformada, nunca OK.
* **F3** `RSTV-25b-dependencia`: valor por tier tem de ser contagem valida E a
  contagem tem de CONDIZER com a Dependency real (o `esperado` declarado e
  "linhas == Dependency"); truthiness deixou de valer como confronto.
* **F4** `RSTV-geometria-clipping`: bbox exige numero FINITO ('NaN'/infinito =
  malformado) junto da tela — dado nao mensuravel nunca fecha OK.
* **F5** cadeia de hash: `hash_fonte`/`hash_dll`/`dll_sha` declarados na MESMA
  observacao com valores DIFERENTES sao contradicao — o alias do coletor nao
  sobrescreve a divergencia declarada.
* **F6** `RSTV-26-placeholders`: o OK passa a exigir o texto RENDERIZADO
  observado; sem render nao se afirma "placeholder resolvido" (nao observado
  nao e o mesmo que resolvido).
* **F7** sessoes: observacoes de SESSOES diferentes na mesma capacidade nao sao
  prova de um unico ciclo (INDETERMINADO) — e nenhuma sessao e copiada para o
  criterio como se fosse a do conjunto inteiro.
* **L2** `RSTV-25b-dependencia`: `arestas_inventadas` deriva o TIPO esperado
  (contagem: numero finito >= 0) em vez de aceitar qualquer coisa que compare
  igual. Forma presente e MALFORMADA (texto '2', '', lista, dict, negativo,
  'NaN') e leitura malformada declarada — nunca OK; o inteiro/float valido, o
  booleano e a chave ausente seguem o comportamento anterior.

LACUNAS DO PROBE ATUAL (declaradas; NAO sao OK, nao sao maquiadas)
------------------------------------------------------------------
O `AUT4Probe`/coletor de hoje emite UMA leitura por TMP_Text ativo e um contexto
`personagem = {gui_state, tem_personagem_selecionado, personagem}`. Ele NAO
emite (por observacao):

  * snapshot ANTES/DEPOIS de skills/pontos do personagem (guarda de leitura);
  * ciclo ABRIR/FECHAR da janela read-only nem pai/indice do tooltip
    (restauracao e anti-duplicacao);
  * linhas de dependencia por tier alem do marcador que o proprio mod escreve
    no LogOutput.log (RSTV-25b continua INDETERMINADO);
  * `tela` (dimensao do viewport) junto da bbox; nem `config_sha` por observacao.

`avaliar` LE esses campos SE existirem (formato documentado em
`docs/automacao/CIC-3-entrega.md`) e, quando faltam, devolve NAO_EXERCITADO /
INDETERMINADO com `lacuna_probe` + `tipo_pendencia` — nada de campo inventado
apresentado como se o probe ja emitisse.
"""
import argparse
import json
import math
import re
import sys

ESQUEMA = "CIC-3/rstv/1"
MOD = "RoguelikeSkillTreeVisualizer"
TAREFA_ORIGEM = "t_76a41ea7"  # AUT-5 (reusada pela CIC-3)

OK, REPROVADO, NAO_EXERCITADO, INDETERMINADO = (
    "OK", "REPROVADO", "NAO_EXERCITADO", "INDETERMINADO")

EXIT_OK, EXIT_FALHOU, EXIT_NAO_RODOU = 0, 1, 2
PROCEDENCIAS = ("execucao", "runtime", "fixture")

# Campos do criterio — o contrato do CICLO-VALIDACAO-escopo.md.
CAMPOS_CRITERIO = ("id", "mod", "estado", "classe", "procedencia", "esperado",
                   "observado", "evidencia", "motivo", "tarefa_origem")

# Campos extras que o contrato positivo pede (rastreaveis).
CAMPOS_EXTRA = ("prova_runtime", "sessao", "fonte_sha", "dll_sha", "config_sha",
                "lacuna_probe", "tipo_pendencia", "autorizacao_necessaria")

# Chave canonica da identidade por campo da observacao. O COLETOR CIC-5 grava
# `hash_fonte` = sha256 da **DLL** do probe (nao da fonte do repo) — ver
# `coletor.derivar_config`/`provar_atualidade` e CIC-5-entrega ("a identidade do
# probe (`hash_fonte`) casa com `dll_sha`"). Logo `hash_fonte` e `hash_dll` sao
# AMBOS a cadeia da DLL; `fonte_sha` so casa por nome explicito (R-1 do CIC-5R).
# F5: o alias ACRESCENTA um valor a chave canonica — nunca sobrescreve um valor
# explicito declarado na mesma observacao (divergencia declarada nao se apaga).
_ALIAS_HASH = (("hash_fonte", "dll_sha"), ("hash_dll", "dll_sha"))

# ------------------------------------------------------------------ placeholders
# O DEFEITO RSTV-26: o hover mostra o dano como '*0' LITERAL quando o
# `character` do motor e null (tela Party Select). Marcadores aceitos:
#   * `*0`  -> valor de dano nao resolvido (a assinatura do bug);
#   * `[N]` -> indice de DescriptionExpressions nao substituido;
#   * `@X@` -> tag de atributo/negrito nao resolvida.
# No TEXTO CRU o token `[N]` e o TEMPLATE legitimo do motor (o renderizador e
# que substitui) — por isso o indice so reprova no TEXTO RENDERIZADO.
_RE_MARCADORES = (
    ("asterisco-zero", re.compile(r"\*0(?![\d.,])")),
    ("indice-literal", re.compile(r"\[\d+\]")),
    ("atributo-nao-resolvido", re.compile(r"@[A-Za-z][\w ]{0,40}@")),
)
_RE_TELA = re.compile(r"(\d+)\s*[xX]\s*(\d+)")

# id canonico de cada capacidade avaliada. `avaliar` SEMPRE devolve este
# conjunto (com NAO_EXERCITADO quando nao ha dado) para o ciclo ver o quadro
# completo, nao so o que por acaso veio na rodada.
CAPACIDADES = (
    ("RSTV-6-readonly-personagem",
     "personagem alvo da leitura e o esperado (nao o personagem errado)"),
    ("RSTV-6-readonly-skills-pontos",
     "skills/pontos do personagem inalterados antes/depois (sem gasto/mutacao)"),
    ("RSTV-21-janela-ciclo",
     "janela read-only abre E fecha no ciclo"),
    ("RSTV-21-tooltip-restauracao",
     "pai/indice do tooltip restaurados no fechar e sem janela duplicada"),
    ("RSTV-26-placeholders",
     "tooltip de skill sem placeholder literal ('*0', '[indice]', '@atributo@')"),
    ("RSTV-25b-dependencia",
     "linhas por tier condizem com Dependency; T5 sem Dependency e ausencia legitima"),
    ("RSTV-geometria-clipping",
     "geometria dentro da tela, com largura/altura > 0 (sem clipping)"),
)

# Lacuna declarada por capacidade (o que o probe/coletor de hoje NAO emite).
LACUNA_PERSONAGEM = ("o AUT4Probe nao emite 'personagem_esperado' (alvo do cenario) "
                     "por observacao; sem alvo declarado nao ha confronto possivel")
LACUNA_SKILLS = ("o AUT4Probe nao emite snapshot antes/depois de skills/pontos; sem o "
                 "par completo (skills_antes/depois, pontos_antes/depois) nao ha guarda "
                 "de leitura somente")
LACUNA_JANELA = ("o AUT4Probe le cada TMP_Text uma vez e nao emite o ciclo ABRIR/FECHAR "
                 "da janela read-only (campo 'janela' = {aberta, fechada})")
LACUNA_TOOLTIP = ("o AUT4Probe nao emite tooltip_pai/indice antes/depois nem contagem de "
                  "janelas duplicadas; sem o par completo nao da para provar "
                  "restauracao/anti-duplicacao")
LACUNA_DEPENDENCIA = ("o AUT4Probe nao emite linhas por tier nem a contagem de Dependency "
                      "real ('linhas_dependencia'/'dependency_por_tier'); sem o par nao ha "
                      "confronto (RSTV-25b continua INDETERMINADO)")
LACUNA_GEOMETRIA = ("o AUT4Probe nao emite 'tela' (dimensao do viewport) junto da bbox; "
                    "sem a tela nao ha contexto de clipping")
LACUNA_MALFORMADO = "dado malformado derrubou a capacidade (id canonico preservado)"


# --------------------------------------------------------------- adaptadores ---

def _campo(obs, nome):
    """Le um campo da observacao nas DUAS formas do AUT-4/CIC-5 (crua e normalizada)."""
    if not isinstance(obs, dict):
        return None
    if nome in obs:
        return obs[nome]
    campos = obs.get("campos")
    if isinstance(campos, dict):
        item = campos.get(nome)
        if isinstance(item, dict) and "valor" in item:
            estado = str(item.get("estado") or "").strip().upper()
            if estado and estado != "PRESENTE":
                # NAO_APLICAVEL com fallback declarado (objeto inativo) usa o fallback.
                if estado == "NAO_APLICAVEL" and item.get("fallback"):
                    return _campo(obs, item["fallback"])
                return None
            return item.get("valor")
    return None


def _texto(obs, nome):
    v = _campo(obs, nome)
    return v if isinstance(v, str) and v.strip() else None


def _txt(v):
    return v.strip() if isinstance(v, str) else ""


def _obs_lista(observacoes):
    if observacoes is None:
        return []
    if isinstance(observacoes, dict):
        observacoes = observacoes.get("observacoes", [observacoes])
    if not isinstance(observacoes, (list, tuple)):
        return []
    return [o for o in observacoes if isinstance(o, dict)]


def _procedencia(obs):
    p = str(obs.get("procedencia") or "fixture").strip().lower()
    return p if p in PROCEDENCIAS else "fixture"


def _identidade_ok(identidade):
    if not isinstance(identidade, dict):
        return False
    fonte = _txt(identidade.get("fonte_sha"))
    dll = _txt(identidade.get("dll_sha"))
    return bool(fonte) and bool(dll)


def _hashes_identidade(identidade):
    """Hashes que a identidade CONHECE (topo `*_sha` + blocos artefatos/hashes)."""
    conhecidos = {}
    idn = identidade if isinstance(identidade, dict) else {}
    for k, v in idn.items():
        if isinstance(k, str) and k.endswith("_sha") and _txt(v):
            conhecidos[k] = _txt(v)
    for grupo in ("artefatos", "hashes"):
        bloco = idn.get(grupo)
        if isinstance(bloco, dict):
            for kk, vv in bloco.items():
                if _txt(vv):
                    conhecidos[str(kk)] = _txt(vv)
    return conhecidos


def _hashes_obs(obs):
    """Hashes que a OBSERVACAO declara, por chave canonica: `{chave: [valores]}`.

    O `hash_fonte` do coletor CIC-5 e o sha da DLL: entra sob a chave canonica
    `dll_sha`. Nomes explicitos (`fonte_sha`/`dll_sha`) tambem contam.

    F5: o valor NAO e um escalar. Duas declaracoes da mesma chave canonica com
    valores diferentes ficam AMBAS na lista — o alias do coletor nao sobrescreve
    (nem e sobrescrito por) o valor explicito. Quem confronta detecta a
    contradicao; antes, o ultimo alias lido apagava a divergencia declarada.
    """
    por_chave = {}

    def _adiciona(chave, valor):
        if _txt(valor):
            por_chave.setdefault(chave, set()).add(_txt(valor))

    for k, v in obs.items():
        if isinstance(k, str) and k.endswith("_sha"):
            _adiciona(k, v)
    for alias, canonico in _ALIAS_HASH:
        _adiciona(canonico, obs.get(alias))
    return {chave: sorted(valores) for chave, valores in por_chave.items()}


def _hashes_obs_contraditorios(obs):
    """F5: chaves canonicas que a observacao declara com mais de um valor."""
    return sorted(chave for chave, valores in _hashes_obs(obs).items() if len(valores) > 1)


def _checagem_hashes(obs, identidade):
    """(divergentes, nao_confirmados) entre os hashes declarados e a identidade.

    * divergente     -> a observacao mediu bytes DIFERENTES da build atual, OU
      declara a mesma chave canonica com dois valores diferentes (F5: a
      contradicao nao se resolve a favor do alias);
    * nao_confirmado -> a observacao declara um hash que a identidade NAO conhece
      (cadeia incompleta) — nenhum dos dois pode fechar OK.
    """
    conhecidos = _hashes_identidade(identidade)
    divergentes, nao_confirmados = [], []
    for chave, valores in _hashes_obs(obs).items():
        if len(valores) > 1:
            divergentes.append(chave)  # contradicao declarada: nao ha valor "bom"
            continue
        valor = valores[0]
        if chave in conhecidos:
            if conhecidos[chave] != valor:
                divergentes.append(chave)
        else:
            nao_confirmados.append(chave)
    return sorted(set(divergentes)), sorted(set(nao_confirmados))


def _evidencia_runtime(obs, identidade):
    """A observacao PROVA runtime? (proc runtime + sessao/hash_fonte + cadeia/identidade)."""
    if _procedencia(obs) != "runtime":
        return False
    if not _txt(obs.get("sessao")):
        return False
    if not _txt(obs.get("hash_fonte")):
        return False
    if not _identidade_ok(identidade):
        return False
    divergentes, nao_confirmados = _checagem_hashes(obs, identidade)
    return not divergentes and not nao_confirmados


def _hash_divergente(obs, identidade):
    """Compat: True se algum hash declarado pela obs diverge da identidade atual."""
    if _procedencia(obs) != "runtime" or not _identidade_ok(identidade):
        return False
    return bool(_checagem_hashes(obs, identidade)[0])


def _evidencia(obs):
    v = obs.get("evidencia")
    if isinstance(v, str):
        return [v]
    if isinstance(v, (list, tuple)):
        return [str(x) for x in v]
    return []


# ------------------------------------------------------------------ criterios ---

def _criterio(cid, estado, procedencia, esperado, observado, motivo, evidencia,
              classe="runtime", extra=None):
    c = {
        "id": cid,
        "mod": MOD,
        "estado": estado,
        "classe": classe,
        "procedencia": procedencia,
        "esperado": esperado,
        "observado": observado,
        "evidencia": sorted(set(str(e) for e in (evidencia or []))),
        "motivo": motivo,
        "tarefa_origem": TAREFA_ORIGEM,
    }
    if extra:
        for k, v in extra.items():
            c.setdefault(k, v)
    return c


def _extras(estado, proc, identidade, contrib, lacuna=None, tipo_pendencia=None):
    """Campos extras rastreaveis: prova da build + classificacao de pendencia.

    * OK         -> `prova_runtime=True`, sessao + hashes da identidade (contrato).
    * REPROVADO  -> sem pendencia (e defeito acionavel pelo ciclo).
    * NAO_EXERCITADO/INDETERMINADO -> LACUNA TECNICA por default: `lacuna_probe`
      + `tipo_pendencia='tecnica'`, `autorizacao_necessaria=False`. Autorizacao
      so quando o motivo exigir o dono (nao e o caso das lacunas do probe).
    """
    extra = {
        "prova_runtime": estado == OK,
        "fonte_sha": _txt((identidade or {}).get("fonte_sha")),
        "dll_sha": _txt((identidade or {}).get("dll_sha")),
    }
    cfg = _txt((identidade or {}).get("config_sha"))
    if cfg:
        extra["config_sha"] = cfg
    if estado == OK:
        sessao = next((_txt(o.get("sessao")) for o in contrib if _txt(o.get("sessao"))), "")
        extra["sessao"] = sessao or None
        extra["tipo_pendencia"] = None
        extra["autorizacao_necessaria"] = False
    elif estado == REPROVADO:
        extra["tipo_pendencia"] = None
        extra["autorizacao_necessaria"] = False
    else:
        extra["tipo_pendencia"] = tipo_pendencia or "tecnica"
        extra["autorizacao_necessaria"] = False
        if lacuna:
            extra["lacuna_probe"] = lacuna
    return extra


def _fecha(contrib, defeitos, dados, identidade, esperado, observado,
           motivos=None, indeterminado=False):
    """Traduz (defeitos, motivos, dados, identidade) no estado do criterio + motivo.

    `contrib` e a lista de observacoes que alimentaram a capacidade. Regras:
      * defeito sempre REPROVADO (mesmo em fixture: e o controle negativo);
      * motivos (campo ausente/incompleto/malformado) NUNCA vira OK — mesmo com
        `dados=True`: vira NAO_EXERCITADO (ou INDETERMINADO se o confronto e
        impossivel);
      * sem dado -> NAO_EXERCITADO;
      * so fecha OK com procedencia runtime, sessao/hash_fonte e identidade
        suficiente, com os hashes declarados casando com a identidade;
      * F5: hash declarado com DOIS valores na mesma observacao e contradicao ->
        INDETERMINADO (o alias do coletor nao sobrescreve o valor explicito);
      * F7: contrib de SESSOES diferentes nao e prova de um unico ciclo ->
        INDETERMINADO (e nenhuma sessao e copiada para o criterio).
    """
    proc = "execucao"
    if contrib:
        procs = {_procedencia(o) for o in contrib}
        proc = "runtime" if procs == {"runtime"} else ("fixture" if "fixture" in procs else "execucao")

    if defeitos:
        return REPROVADO, proc, "DEFEITO: " + "; ".join(defeitos)
    if not dados:
        motivo = "sem observacao/leitura para esta capacidade (AUSENTE nao e OK)"
        if motivos:
            motivo += " — " + "; ".join(motivos)
        return NAO_EXERCITADO, proc, motivo
    if motivos:
        base = ("campo AUSENTE/incompleto nao vira OK — " + "; ".join(motivos))
        return ((INDETERMINADO if indeterminado else NAO_EXERCITADO), proc, base)

    # F7: a capacidade fala de UM ciclo. Observacoes de sessoes diferentes nao
    # sao prova de um unico ciclo (e nenhuma sessao pode ser copiada como se
    # fosse a do conjunto).
    sessoes = sorted({_txt(o.get("sessao")) for o in contrib if _txt(o.get("sessao"))})
    if len(sessoes) > 1:
        return INDETERMINADO, proc, ("observacoes de SESSOES diferentes (%s) na mesma "
                                     "capacidade: nao e prova de um UNICO ciclo"
                                     % ", ".join(sessoes))

    runtime_ok = all(_evidencia_runtime(o, identidade) for o in contrib)
    if runtime_ok:
        return OK, proc, "leitura runtime completa com identidade suficiente"

    # F5: a MESMA observacao declarando valores diferentes para a mesma chave
    # canonica de hash e contradicao declarada — nunca se resolve a favor do alias.
    contraditorios = sorted({ch for o in contrib for ch in _hashes_obs_contraditorios(o)})
    if contraditorios:
        return INDETERMINADO, proc, ("hash (%s) declarado com VALORES DIFERENTES na mesma "
                                     "observacao: declaracao contraditoria, nunca OK"
                                     % ", ".join(contraditorios))

    if not _identidade_ok(identidade):
        return NAO_EXERCITADO, proc, ("sem identidade suficiente (fonte_sha/dll_sha): "
                                      "nunca OK sem identidade")
    divergentes = sorted({ch for o in contrib for ch in _checagem_hashes(o, identidade)[0]})
    if divergentes:
        return INDETERMINADO, proc, ("hash (%s) da observacao != identidade: resultado de "
                                     "bytes DIFERENTES (nao vale para a build atual)"
                                     % ", ".join(divergentes))
    nao_confirmados = sorted({ch for o in contrib for ch in _checagem_hashes(o, identidade)[1]})
    if nao_confirmados:
        return NAO_EXERCITADO, proc, ("hash (%s) nao confirmado pela identidade: cadeia "
                                      "incompleta, nunca OK" % ", ".join(nao_confirmados))
    if proc == "fixture":
        return NAO_EXERCITADO, proc, "fixture rotulada: testa o avaliador, NAO comprova runtime"
    return NAO_EXERCITADO, proc, "runtime sem sessao/hash_fonte: nao identifica a build medida"


# --------------------------------------------- capacidade: personagem (RSTV-6)

def _cap_personagem(obs_list, identidade):
    contrib, defeitos, dados, motivos = [], [], False, []
    for o in obs_list:
        esperado_nome = o.get("personagem_esperado") or o.get("alvo_personagem")
        ctx = _campo(o, "personagem")
        obs_nome = None
        if isinstance(ctx, dict):
            obs_nome = ctx.get("personagem")
        elif isinstance(ctx, str):
            obs_nome = ctx
        if esperado_nome is None and obs_nome is None:
            continue
        contrib.append(o)
        dados = True
        if esperado_nome is None:
            motivos.append("sem 'personagem_esperado' (alvo do cenario) — nao da para julgar o alvo")
            continue
        if not str(obs_nome or "").strip():
            motivos.append("personagem observado AUSENTE (nada selecionado?)")
            continue
        if str(obs_nome).strip() != str(esperado_nome).strip():
            defeitos.append("personagem errado: esperado %r, lido %r"
                            % (str(esperado_nome), str(obs_nome)))
    indeterminado = bool(motivos) and all(m.startswith("sem 'personagem_esperado'") for m in motivos)
    ev = [e for o in contrib for e in _evidencia(o)]
    estado, proc, motivo = _fecha(contrib, defeitos, dados, identidade,
                                  "personagem == alvo declarado",
                                  "personagens lidos: %s" % ([_campo(o, "personagem") for o in contrib] or "nenhum"),
                                  motivos, indeterminado)
    extra = _extras(estado, proc, identidade, contrib, lacuna=LACUNA_PERSONAGEM)
    return _criterio("RSTV-6-readonly-personagem", estado, proc,
                     "personagem lido == alvo do cenario", "ver observado", motivo, ev, extra=extra)


# ------------------------------------ capacidade: skills/pontos (RSTV-6, guarda)

def _par(obs, nomes):
    a = _campo(obs, nomes[0])
    b = _campo(obs, nomes[1])
    return (a, b) if (a is not None or b is not None) else None


def _lista_de_str(v):
    """skills TEM de ser lista/tupla de strings — nunca string nem dict."""
    return isinstance(v, (list, tuple)) and all(isinstance(x, str) for x in v)


def _numerico(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _contagem_observada(v):
    """Contagem OBSERVADA valida (F2): numero finito >= 0.

    `None`, booleano, texto, lista ou negativo NAO sao contagem — a chave presente
    com valor malformado nao prova ausencia de duplicata.
    """
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    f = float(v)
    return f if math.isfinite(f) and f >= 0 else None


def _cap_skills_pontos(obs_list, identidade):
    """Guarda de leitura somente: skills E pontos inalterados antes/depois.

    F1: o criterio anuncia as DUAS dimensoes (skills e pontos). Ler um par so
    NAO fecha OK — a dimensao que nunca foi lida vira lacuna declarada, em vez de
    "ambas inalteradas" afirmado com metade da leitura.
    """
    contrib, defeitos, dados, motivos = [], [], False, []
    lidas = set()  # dimensoes com par antes/depois COMPLETO em alguma leitura
    for o in obs_list:
        achou = False
        # pares explicitos
        for (na, nb, rotulo) in (("skills_antes", "skills_depois", "skills"),
                                 ("pontos_antes", "pontos_depois", "pontos")):
            par = _par(o, (na, nb))
            if par is None:
                continue
            achou = True
            antes, depois = par
            if antes is None or depois is None:
                motivos.append("%s: par antes/depois incompleto" % rotulo)
                continue
            lidas.add(rotulo)
            if rotulo == "pontos":
                if not (_numerico(antes) and _numerico(depois)):
                    motivos.append("pontos: valor nao numerico (antes=%r, depois=%r)"
                                   % (antes, depois))
                elif float(depois) < float(antes):
                    defeitos.append("GASTO de pontos: antes=%s, depois=%s" % (antes, depois))
                elif float(depois) != float(antes):
                    defeitos.append("pontos MUDARAM: antes=%s, depois=%s" % (antes, depois))
            else:
                if not (_lista_de_str(antes) and _lista_de_str(depois)):
                    motivos.append("skills: campo malformado — esperado lista de strings "
                                   "(antes=%s, depois=%s)"
                                   % (type(antes).__name__, type(depois).__name__))
                elif sorted(antes) != sorted(depois):
                    defeitos.append("skills MUDARAM: antes=%s, depois=%s" % (antes, depois))
        # snapshots compostos
        sa, sb = _campo(o, "snapshot_antes"), _campo(o, "snapshot_depois")
        if isinstance(sa, dict) or isinstance(sb, dict):
            achou = True
            sa, sb = sa or {}, sb or {}
            tem_p = ("pontos" in sa) or ("pontos" in sb)
            tem_s = ("skills" in sa) or ("skills" in sb)
            if not (tem_p or tem_s):
                motivos.append("snapshot_antes/depois sem as chaves 'skills'/'pontos'")
            if tem_p:
                pa, pb = sa.get("pontos"), sb.get("pontos")
                if pa is None or pb is None:
                    motivos.append("snapshot pontos: par antes/depois incompleto")
                elif not (_numerico(pa) and _numerico(pb)):
                    motivos.append("snapshot pontos: valor nao numerico")
                else:
                    lidas.add("pontos")
                    if pb != pa:
                        defeitos.append("GASTO/mudanca de pontos no snapshot: antes=%s, depois=%s"
                                        % (pa, pb))
            if tem_s:
                ka, kb = sa.get("skills"), sb.get("skills")
                if ka is None or kb is None:
                    motivos.append("snapshot skills: par antes/depois incompleto")
                elif not (_lista_de_str(ka) and _lista_de_str(kb)):
                    motivos.append("snapshot skills: campo malformado — esperado lista de strings")
                else:
                    lidas.add("skills")
                    if sorted(ka) != sorted(kb):
                        defeitos.append("skills mudaram no snapshot: antes=%s, depois=%s" % (ka, kb))
        if achou:
            contrib.append(o)
            dados = True
    if dados:
        # F1: sem o par COMPLETO da dimensao nao ha como afirmar que ela ficou
        # inalterada — a ausencia de leitura e lacuna, nunca OK.
        for dimensao in ("skills", "pontos"):
            if dimensao not in lidas:
                motivos.append("%s: dimensao NUNCA lida (nenhum par antes/depois "
                               "completo) — nao se afirma 'skills e pontos inalterados'"
                               % dimensao)
    ev = [e for o in contrib for e in _evidencia(o)]
    estado, proc, motivo = _fecha(contrib, defeitos, dados, identidade,
                                  "skills e pontos inalterados (leitura somente)",
                                  "dimensoes lidas: %s; leituras: %d"
                                  % (sorted(lidas) or "nenhuma", len(contrib)), motivos)
    extra = _extras(estado, proc, identidade, contrib, lacuna=LACUNA_SKILLS)
    return _criterio("RSTV-6-readonly-skills-pontos", estado, proc,
                     "skills/pontos inalterados", "ver observado", motivo, ev, extra=extra)


# --------------------------------------------- capacidade: ciclo janela (RSTV-21)

def _cap_janela_ciclo(obs_list, identidade):
    contrib, defeitos, dados, motivos = [], [], False, []
    for o in obs_list:
        j = _campo(o, "janela")
        if not isinstance(j, dict):
            continue
        contrib.append(o)
        dados = True
        tem_ab = "aberta" in j
        tem_fe = "fechada" in j
        if not (tem_ab or tem_fe):
            motivos.append("janela sem os campos 'aberta'/'fechada' (registro incompleto)")
            continue
        if not tem_ab or not tem_fe:
            motivos.append("janela incompleta (faltou 'aberta' ou 'fechada')")
        if tem_ab and j.get("aberta") is not True:
            defeitos.append("janela nao registrou ABERTURA (aberta=%r)" % (j.get("aberta"),))
        if tem_fe and j.get("fechada") is not True:
            defeitos.append("janela nao registrou FECHAMENTO (fechada=%r)" % (j.get("fechada"),))
    ev = [e for o in contrib for e in _evidencia(o)]
    estado, proc, motivo = _fecha(contrib, defeitos, dados, identidade,
                                  "janela abre e fecha no ciclo",
                                  "ciclos registrados: %d" % len(contrib), motivos)
    extra = _extras(estado, proc, identidade, contrib, lacuna=LACUNA_JANELA)
    return _criterio("RSTV-21-janela-ciclo", estado, proc,
                     "abre E fecha", "ver observado", motivo, ev, extra=extra)


# --------------------------------- capacidade: restauracao tooltip (RSTV-21)

def _cap_tooltip_restauracao(obs_list, identidade):
    contrib, defeitos, dados, motivos = [], [], False, []
    for o in obs_list:
        tem = any(k in o for k in ("tooltip_pai_antes", "tooltip_pai_depois",
                                   "tooltip_indice_antes", "tooltip_indice_depois",
                                   "janelas_duplicadas", "duplicata"))
        if not tem:
            continue
        contrib.append(o)
        dados = True
        tem_pai = ("tooltip_pai_antes" in o) or ("tooltip_pai_depois" in o)
        tem_idx = ("tooltip_indice_antes" in o) or ("tooltip_indice_depois" in o)
        tem_dup = ("janelas_duplicadas" in o) or ("duplicata" in o)
        if not tem_pai:
            motivos.append("tooltip pai: antes/depois AUSENTE")
        if not tem_idx:
            motivos.append("tooltip indice: antes/depois AUSENTE")
        if not tem_dup:
            motivos.append("contagem de janelas duplicadas AUSENTE")
        else:
            # F2: a chave PRESENTE nao basta. Provar AUSENCIA de duplicata exige
            # CONTAGEM OBSERVADA valida; `null`/negativo/bool/lista e leitura
            # malformada (antes disso, o funil tratava qualquer coisa como zero).
            if "janelas_duplicadas" in o:
                dup = o.get("janelas_duplicadas")
                n = _contagem_observada(dup)
                if n is None:
                    motivos.append("janelas_duplicadas MALFORMADA (%r): contagem observada "
                                   "valida (numero finito >= 0) e obrigatoria para provar "
                                   "ausencia de janela duplicada" % (dup,))
                elif n > 0:
                    defeitos.append("janela DUPLICADA: janelas_duplicadas=%s" % (dup,))
            if "duplicata" in o:
                d = o.get("duplicata")
                if not isinstance(d, bool):
                    motivos.append("duplicata MALFORMADA (%r): esperado booleano — "
                                   "declaracao invalida nao prova ausencia" % (d,))
                elif d:
                    defeitos.append("janela duplicada (duplicata=true)")
        for rotulo, ka, kb in (("pai", "tooltip_pai_antes", "tooltip_pai_depois"),
                               ("indice", "tooltip_indice_antes", "tooltip_indice_depois")):
            a, b = o.get(ka), o.get(kb)
            if a is None or b is None:
                if (ka in o) or (kb in o):
                    motivos.append("tooltip %s: antes/depois incompleto" % rotulo)
                continue
            if a != b:
                defeitos.append("tooltip %s NAO restaurado: antes=%r, depois=%r" % (rotulo, a, b))
    ev = [e for o in contrib for e in _evidencia(o)]
    estado, proc, motivo = _fecha(contrib, defeitos, dados, identidade,
                                  "tooltip devolvido ao pai/indice original; sem duplicata",
                                  "ciclos inspecionados: %d" % len(contrib), motivos)
    extra = _extras(estado, proc, identidade, contrib, lacuna=LACUNA_TOOLTIP)
    return _criterio("RSTV-21-tooltip-restauracao", estado, proc,
                     "pai/indice iguais e sem duplicata", "ver observado",
                     motivo, ev, extra=extra)


# ------------------------------------------------ capacidade: placeholders (RSTV-26)

def _marcadores(obs):
    bruto = _texto(obs, "texto_bruto")
    render = _texto(obs, "texto_renderizado")
    achados = []
    for campo, txt in (("texto_bruto", bruto), ("texto_renderizado", render)):
        if not txt:
            continue
        for nome, rx in _RE_MARCADORES:
            if nome == "indice-literal" and campo == "texto_bruto":
                continue  # `[N]` cru e o TEMPLATE legitimo; so reprova ja renderizado
            m = rx.search(txt)
            if m:
                achados.append({"campo": campo, "marcador": nome, "trecho": m.group(0)})
    return achados, bool(bruto or render)


def _cap_placeholders(obs_list, identidade):
    contrib, defeitos, dados, motivos = [], [], False, []
    for o in obs_list:
        achados, tem = _marcadores(o)
        if not tem:
            continue
        contrib.append(o)
        dados = True
        for a in achados:
            defeitos.append("placeholder %s em %s: %r"
                            % (a["marcador"], a["campo"], a["trecho"]))
        if not _texto(o, "texto_renderizado"):
            # F6: o template CRU pode ser legitimo (o '[N]' e o proprio motor), mas
            # nao prova o RENDER. Sem o texto renderizado nao se declara
            # "placeholder resolvido" — nao observado != resolvido.
            motivos.append("texto RENDERIZADO nao observado (so o cru): nao da para "
                           "afirmar que o placeholder foi resolvido")
    ev = [e for o in contrib for e in _evidencia(o)]
    estado, proc, motivo = _fecha(contrib, defeitos, dados, identidade,
                                  "nenhum '*0'/indice/@atributo@ literal no texto",
                                  "textos inspecionados: %d" % len(contrib), motivos)
    if estado == OK:
        motivo = "tooltip RENDERIZADO observado e sem placeholder literal"
    extra = _extras(estado, proc, identidade, contrib)
    return _criterio("RSTV-26-placeholders", estado, proc,
                     "texto renderizado sem placeholder literal", "ver observado",
                     motivo, ev, extra=extra)


# --------------------------------------- capacidade: linhas de dependencia (RSTV-25b)

def _cap_dependencia(obs_list, identidade):
    contrib, defeitos, dados, motivos = [], [], False, []
    indeterminado = False
    for o in obs_list:
        linhas = _campo(o, "linhas_dependencia")
        dep = _campo(o, "dependency_por_tier") or _campo(o, "dependency")
        arestas = o.get("arestas_inventadas")
        if linhas is None and dep is None and arestas is None:
            continue
        contrib.append(o)
        dados = True
        # L2 (parecer CIC-3R2, mesma classe F2/F3): `arestas_inventadas` e uma
        # CONTAGEM — o TIPO esperado e o numero finito >= 0 (int/float), nao
        # "qualquer coisa que compare igual". Antes, so o numero nao-bool > 0
        # virava defeito; uma forma MALFORMADA (texto '2', '', lista, dict,
        # negativo, 'NaN') NAO era lida como leitura malformada e fechava OK.
        # Agora a forma presente e malformada vira motivo declarado — nunca OK.
        # O booleano segue o comportamento historico (nao e contagem): a guarda
        # `not isinstance(arestas, bool)` preservada.
        if arestas is not None and not isinstance(arestas, bool):
            contagem = _contagem_observada(arestas)
            if contagem is None:
                motivos.append("`arestas_inventadas` MALFORMADA (%r): exigida "
                               "contagem observada valida (numero finito >= 0); forma "
                               "textual/nao numerica/negativa nao prova ausencia de "
                               "aresta inventada" % (arestas,))
            elif contagem > 0:
                defeitos.append("aresta de dependencia INVENTADA (sem Dependency real)")
        if linhas is None:
            motivos.append("linhas por tier AUSENTES")
            indeterminado = True
        if dep is None:
            motivos.append("Dependency real AUSENTE — confronto impossivel")
            indeterminado = True
        if isinstance(linhas, dict) and isinstance(dep, dict):
            for tier in sorted(set(list(linhas) + list(dep))):
                n_lin, n_dep = linhas.get(tier), dep.get(tier)
                # F3: o confronto exige CONTAGEM VALIDA dos dois lados. Truthiness
                # ('abc', -2) e a comparacao que nunca acontece (1 x 3) deixam de
                # fechar o criterio — o proprio `esperado` declara
                # "linhas == Dependency real".
                invalidos = []
                if tier in linhas and _contagem_observada(n_lin) is None:
                    invalidos.append("linhas=%r" % (n_lin,))
                if tier in dep and _contagem_observada(n_dep) is None:
                    invalidos.append("Dependency=%r" % (n_dep,))
                if invalidos:
                    motivos.append("%s: valor INVALIDO no confronto (%s) — contagem observada "
                                   "(numero finito >= 0) e obrigatoria dos dois lados"
                                   % (tier, ", ".join(invalidos)))
                    indeterminado = True
                    continue
                v_lin = _contagem_observada(n_lin) if tier in linhas else None
                v_dep = _contagem_observada(n_dep) if tier in dep else None
                if tier == "T5" and not v_dep:
                    # T5 sem Dependency e AUSENCIA LEGITIMA (nao se inventa aresta).
                    if v_lin:
                        defeitos.append("T5 tem linha mas nao tem Dependency: aresta INVENTADA")
                    continue
                if v_dep and not v_lin:
                    defeitos.append("%s com Dependency=%s e nenhuma linha (conector ausente)"
                                    % (tier, n_dep))
                elif v_lin and not v_dep:
                    defeitos.append("%s com linha e Dependency=0 (aresta INVENTADA)" % tier)
                elif v_lin is not None and v_dep is not None and v_lin != v_dep:
                    defeitos.append("%s: linhas=%s != Dependency=%s (o criterio declara "
                                    "'linhas == Dependency real')" % (tier, n_lin, n_dep))
        elif (linhas is not None and not isinstance(linhas, dict)) \
                or (dep is not None and not isinstance(dep, dict)):
            motivos.append("linhas/Dependency em formato incompleto — confronto parcial")
            indeterminado = True
    ev = [e for o in contrib for e in _evidencia(o)]
    estado, proc, motivo = _fecha(contrib, defeitos, dados, identidade,
                                  "linhas == Dependency real; T5 sem Dependency e legitimo",
                                  "tiers inspecionados: %d" % len(contrib), motivos, indeterminado)
    extra = _extras(estado, proc, identidade, contrib, lacuna=LACUNA_DEPENDENCIA)
    return _criterio("RSTV-25b-dependencia", estado, proc,
                     "linhas condizem com Dependency", "ver observado", motivo, ev, extra=extra)


# ------------------------------------------- capacidade: geometria/clipping

def _numero_finito(v):
    """Numero FINITO da leitura (aceita texto numerico, como `float()` aceitava).

    F4: 'NaN'/'Infinity' passavam por `float()` e viravam comparacoes sempre
    falsas — nao medem dimensao nenhuma. Nao finito NAO e numero.
    """
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        f = float(v)
    elif isinstance(v, str):
        try:
            f = float(v.strip())
        except ValueError:
            return None
    else:
        return None
    return f if math.isfinite(f) else None


def _bbox(o):
    """(caixa, motivo) da geometria da observacao.

    * `(None, None)`   -> nao ha leitura de caixa nesta observacao (AUSENTE);
    * `(None, motivo)` -> ha leitura, mas ela e INVALIDA (F4: valor presente que
      nao e numero finito, ou `tela` malformada) — dado nao mensuravel nunca OK;
    * `(dict, None)`   -> caixa mensuravel (valores finitos) + `tela` lida.
    """
    g = _campo(o, "geometria")
    if not isinstance(g, dict):
        return None, None
    caixa = g.get("caixa_na_tela_px")
    if not isinstance(caixa, dict):
        return None, None
    valores, invalidos = {}, []
    for nome in ("x", "y", "largura", "altura"):
        if nome not in caixa:
            return None, None  # leitura incompleta do campo: sem dado (AUSENTE)
        f = _numero_finito(caixa.get(nome))
        if f is None:
            invalidos.append("%s=%r" % (nome, caixa.get(nome)))
        else:
            valores[nome] = f
    if invalidos:
        return None, ("caixa_na_tela_px MALFORMADA (%s): exigido numero finito em "
                      "x/y/largura/altura — 'NaN'/infinito nao mede dimensao"
                      % ", ".join(invalidos))
    tela = None
    bruto_tela = g.get("tela")
    m = _RE_TELA.search(str(bruto_tela or ""))
    if m:
        tela = (float(m.group(1)), float(m.group(2)))
    elif _txt(bruto_tela):
        return None, ("geometria.tela MALFORMADA (%r): esperado 'LARGURAxALTURA'"
                      % (bruto_tela,))
    return {"x": valores["x"], "y": valores["y"], "largura": valores["largura"],
            "altura": valores["altura"], "tela": tela}, None


def _cap_geometria(obs_list, identidade):
    contrib, defeitos, dados, motivos = [], [], False, []
    for o in obs_list:
        b, invalido = _bbox(o)
        if invalido:
            # leitura presente e MALFORMADA: e dado (entra em contrib), mas nunca OK
            contrib.append(o)
            dados = True
            motivos.append(invalido)
            continue
        if b is None:
            continue
        contrib.append(o)
        dados = True
        if b["largura"] <= 0 or b["altura"] <= 0:
            defeitos.append("dimensao nao positiva: largura=%s altura=%s" % (b["largura"], b["altura"]))
        if b["tela"] is None:
            motivos.append("tela AUSENTE — sem contexto de clipping (confronto parcial)")
            continue
        W, H = b["tela"]
        if b["x"] < -0.5 or b["y"] < -0.5:
            defeitos.append("caixa fora da tela (x=%s y=%s)" % (b["x"], b["y"]))
        if b["x"] + b["largura"] > W + 0.5:
            defeitos.append("CLIPPING horizontal: x+largura=%.1f > tela=%.1f"
                            % (b["x"] + b["largura"], W))
        if b["y"] + b["altura"] > H + 0.5:
            defeitos.append("CLIPPING vertical: y+altura=%.1f > tela=%.1f"
                            % (b["y"] + b["altura"], H))
    ev = [e for o in contrib for e in _evidencia(o)]
    estado, proc, motivo = _fecha(contrib, defeitos, dados, identidade,
                                  "bbox dentro da tela e dimensoes > 0",
                                  "geometrias inspecionadas: %d" % len(contrib), motivos)
    extra = _extras(estado, proc, identidade, contrib, lacuna=LACUNA_GEOMETRIA)
    return _criterio("RSTV-geometria-clipping", estado, proc,
                     "bbox dentro da tela", "ver observado", motivo, ev, extra=extra)


# ------------------------------------------------------------------- avaliar ---

# (id canonico, funcao). O id vem DAQUI — nunca de split do nome da funcao.
_CAPS = (
    ("RSTV-6-readonly-personagem", _cap_personagem),
    ("RSTV-6-readonly-skills-pontos", _cap_skills_pontos),
    ("RSTV-21-janela-ciclo", _cap_janela_ciclo),
    ("RSTV-21-tooltip-restauracao", _cap_tooltip_restauracao),
    ("RSTV-26-placeholders", _cap_placeholders),
    ("RSTV-25b-dependencia", _cap_dependencia),
    ("RSTV-geometria-clipping", _cap_geometria),
)


def avaliar(observacoes, identidade):
    """Avalia as observacoes RSTV e devolve a lista de criterios (contrato v1).

    Nunca levanta por dado ausente/malformado: capacidade sem leitura sai
    NAO_EXERCITADO; excecao -> INDETERMINADO, mas SEMPRE com o id canonico do
    conjunto (o quadro de 7 e preservado mesmo no caminho de erro).
    """
    obs = _obs_lista(observacoes)
    identidade = identidade if isinstance(identidade, dict) else {}
    criterios = []
    for cid, cap in _CAPS:
        try:
            criterios.append(cap(obs, identidade))
        except Exception as erro:  # dado malformado nao derruba o avaliador
            criterios.append(_criterio(
                cid, INDETERMINADO, "execucao",
                "avaliar sem excecao",
                "erro ao avaliar: %s: %s" % (type(erro).__name__, erro),
                "observacao malformada derrubou a capacidade (id canonico preservado)", [],
                extra=_extras(INDETERMINADO, "execucao", identidade, [],
                              lacuna=LACUNA_MALFORMADO)))
    return criterios


# ------------------------------------------------------------------- resumo ----

def resumir(criterios, identidade):
    contagem = {}
    for c in criterios:
        contagem[c["estado"]] = contagem.get(c["estado"], 0) + 1
    return {
        "esquema": ESQUEMA,
        "identidade": {"fonte_sha": (identidade or {}).get("fonte_sha"),
                       "dll_sha": (identidade or {}).get("dll_sha"),
                       "config_sha": (identidade or {}).get("config_sha"),
                       "suficiente": _identidade_ok(identidade)},
        "por_mod": {MOD: contagem},
        "contagem": contagem,
        "runtime_exercitado": bool(contagem.get("OK")),
        "prova_runtime": bool(contagem.get("OK")),
        "reprovado": bool(contagem.get("REPROVADO")),
        "criterios": criterios,
    }


# --------------------------------------------------------------------- CLI -----

def _identidade_de(arquivo=None, fonte=None, dll=None):
    ident = {}
    if arquivo:
        with open(arquivo, encoding="utf-8") as fh:
            ident = json.load(fh)
    if fonte is not None:
        ident["fonte_sha"] = fonte
    if dll is not None:
        ident["dll_sha"] = dll
    return ident if isinstance(ident, dict) else {}


def _desempacotar(dados):
    """Aceita lista de observacoes OU resultado AUT-4/CIC-5 (com 'observacoes')."""
    procedencia, rotulo, ident = None, None, {}
    if isinstance(dados, dict):
        procedencia = dados.get("procedencia")
        rotulo = dados.get("rotulo_fixture")
        ident = dados.get("identidade") or {}
        if not ident:
            # `hash_fonte` do coletor CIC-5 e o sha da DLL: entra como `dll_sha`
            # (a fonte so por nome explicito `fonte_sha`). Ver CIC-5R R-1.
            ds = dados.get("hash_dll") or dados.get("hash_fonte")
            if ds:
                ident = {"dll_sha": ds}
        obs = dados.get("observacoes", [dados])
    elif isinstance(dados, list):
        obs = dados
    else:
        obs = []
    obs = [dict(o) for o in obs if isinstance(o, dict)]
    for o in obs:
        if not o.get("procedencia") and procedencia:
            o["procedencia"] = procedencia
        if not o.get("rotulo_fixture") and rotulo:
            o["rotulo_fixture"] = rotulo
    return obs, ident


def main(argv=None):
    ap = argparse.ArgumentParser(description="CIC-3: avaliadores RSTV (offline/opt-in).")
    ap.add_argument("--observacoes", required=True,
                    help="JSON: lista de observacoes OU resultado AUT-4 com 'observacoes'")
    ap.add_argument("--identidade", help="JSON com fonte_sha/dll_sha")
    ap.add_argument("--fonte-sha", help="sobrepoe fonte_sha da identidade")
    ap.add_argument("--dll-sha", help="sobrepoe dll_sha da identidade")
    ap.add_argument("--out", help="grava o resumo (JSON) neste arquivo")
    args = ap.parse_args(argv)

    with open(args.observacoes, encoding="utf-8") as fh:
        dados = json.load(fh)
    obs, ident_embutida = _desempacotar(dados)
    identidade = dict(ident_embutida)
    identidade.update(_identidade_de(args.identidade, args.fonte_sha, args.dll_sha))

    criterios = avaliar(obs, identidade)
    resultado = resumir(criterios, identidade)
    texto = json.dumps(resultado, ensure_ascii=False, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(texto)
    print(texto)

    if any(c["estado"] == REPROVADO for c in criterios):
        return EXIT_FALHOU
    if any(c["estado"] == OK for c in criterios):
        return EXIT_OK
    return EXIT_NAO_RODOU


if __name__ == "__main__":
    sys.exit(main())
