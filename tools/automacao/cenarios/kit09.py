#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""kit09.py - KIT-09: pacote de cenarios RSTV em criterios PEQUENOS e rastreaveis.

OBJETIVO (cartao `t_a4ca00f9`)
------------------------------
Reusar AUT-5 (`t_76a41ea7`, plano `tools/automacao/aut5/cenarios-rstv.json`) e CIC-3
(`t_7fdce47f`, avaliador `tools/automacao/cenarios/rstv.py`) para cobrir a observacao e o
teste do Skill Tree Visualizer com criterios pequenos, ligados a um **esperado
independente** (origem declarada, nunca lido da mesma observacao julgada).

O QUE ESTE MODULO ACRESCENTA (sem reabrir o aceite anterior)
-----------------------------------------------------------
O CIC-3 entrega o quadro MACRO de 7 capacidades. Aqui cada capacidade e desdobrada em
criterios pequenos, cada um com `capacidade_pai` (uma das 7 macro, ou o grupo novo
`KIT09-RSTV5-botao-run`) e `cenario_origem` (`S1`..`S5` do plano AUT-5):

  * abrir != fechar != fechar por X != fechar por Esc;
  * personagem correto, skills e pontos SEM MUTACAO (criterios separados);
  * tooltip: render observado != sem placeholder; pai != indice != anti-duplicacao;
  * dependencia: arestas por tier == Dependency real, sem aresta inventada, e
    ausencia LEGITIMA (tier com Dependency 0 e 0 linhas) nao vira conector;
  * geometria: medida != clipping;
  * botao da run: handler != clique fisico (testes DISTINTOS) e "ativo" NAO prova
    ausencia de obstrucao;
  * `KIT09-sessao-atual`: observacao de sessao antiga (dado velho) REPROVA.

NAO DUPLICA AVALIACAO (D1)
--------------------------
`rstv.py` e importado por caminho e as primitivas do CIC-3 sao reusadas: o adaptador das
DUAS formas do AUT-4/CIC-5 (`campos` normalizado + campos planos), o fechamento
(`_fecha`: fixture nunca vira OK, identidade `fonte_sha`/`dll_sha` obrigatoria, cadeia de
hash, sessoes misturadas), `_extras`, `_criterio`, `_selecionar_alvos`, as validacoes de
forma (`_contagem_observada`, `_numerico`, `_lista_de_str`, `_numero_finito`, `_bbox`,
`_marcadores`). Se o contrato do CIC-3 mudar, a importacao FALHA ALTO (fail-closed) em vez
de degradar em silencio.

RUNTIME NAO_EXERCITADO
----------------------
Nada aqui abre o jogo, instala probe, carrega save ou publica. Fixture testa o AVALIADOR e
nunca fecha OK. A rodada viva continua dependendo de KIT-G1/G2 e de autorizacao explicita
do dono. Campos que o probe de hoje NAO emite saem `NAO_EXERCITADO` com `lacuna_probe` +
`tipo_pendencia='tecnica'` — contrato declarado, nunca maquiado como emitido.
"""
import argparse
import importlib.util
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ESQUEMA = "KIT-09/rstv-cenarios/1"
MOD = "RoguelikeSkillTreeVisualizer"
TAREFA_KIT = "t_a4ca00f9"
TAREFA_AUT5 = "t_76a41ea7"


# ------------------------------------------------------------------ import CIC-3 --

def _carregar_rstv():
    caminho = os.path.join(AQUI, "rstv.py")
    if not os.path.isfile(caminho):
        raise RuntimeError("KIT-09: avaliador CIC-3 ausente: %s" % caminho)
    spec = importlib.util.spec_from_file_location("cic3_rstv_kit09", caminho)
    if spec is None or spec.loader is None:
        raise RuntimeError("KIT-09: nao consegui carregar o CIC-3 em %s" % caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


RC = _carregar_rstv()

# Contrato MINIMO reusado do CIC-3. Faltando qualquer peca, o modulo nao sobe: um
# avaliador "quase igual" que degrada em silencio esconderia criterio.
_CONTRATO = ("_campo", "_texto", "_fecha", "_extras", "_criterio", "_selecionar_alvos",
             "_contagem_observada", "_numerico", "_lista_de_str", "_numero_finito",
             "_bbox", "_marcadores", "_obs_lista", "_evidencia", "_desempacotar",
             "CAPACIDADES")
_faltando = [n for n in _CONTRATO if not hasattr(RC, n)]
if _faltando:
    raise RuntimeError("KIT-09: contrato do CIC-3 incompleto (%s): reuso recusado"
                       % ", ".join(_faltando))

OK, REPROVADO, NAO_EXERCITADO, INDETERMINADO = (
    RC.OK, RC.REPROVADO, RC.NAO_EXERCITADO, RC.INDETERMINADO)
EXIT_OK, EXIT_FALHOU, EXIT_NAO_RODOU = RC.EXIT_OK, RC.EXIT_FALHOU, RC.EXIT_NAO_RODOU

CAPACIDADES_MACRO = tuple(cid for cid, _ in RC.CAPACIDADES)
PAI_BOTAO = "KIT09-RSTV5-botao-run"

# Pior estado primeiro: o roll-up por capacidade usa esta ordem.
_PIOR = (REPROVADO, INDETERMINADO, NAO_EXERCITADO, OK)


# --------------------------------------------------------------------- lacunas --

LACUNA_JANELA_MICRO = ("o probe nao emite o ciclo ABRIR/FECHAR em campos separados "
                       "('janela' = {aberta, fechada}) por criterio pequeno")
LACUNA_JANELA_ROTAS = ("o probe nao emite as ROTAS de fechamento "
                       "('janela.fechado_x'/'janela.fechado_esc'); sem as rotas nao da "
                       "para distinguir o X do Esc (AUT-5 S1/S4, item 2 do pedido ao dono)")
LACUNA_SKILLS_DIM = ("o probe nao emite o par antes/depois de '%s' (guarda de leitura "
                     "somente); sem o par completo nao ha como afirmar que ficou inalterado")
LACUNA_RENDER = ("o probe nao emitiu o texto RENDERIZADO do hover; sem o render nao se "
                 "afirma 'placeholder resolvido' (nao observado != resolvido)")
LACUNA_TOOLTIP_CAMPO = ("o probe nao emite 'tooltip_%s_antes/depois' por observacao; sem o "
                        "par completo nao da para provar a restauracao do %s")
LACUNA_DUPLICATA = ("o probe nao emite a contagem de 'janelas_duplicadas'; sem contagem "
                    "observada valida nao se prova ausencia de duplicata")
LACUNA_DEP_TIERS = ("o probe nao emite 'linhas_dependencia' (por tier) nem "
                    "'dependency_por_tier' (Dependency real); sem os dois lados nao ha "
                    "confronto (RSTV-25b)")
LACUNA_ARESTA_INVENTADA = ("o probe nao emite 'arestas_inventadas' nem o par por tier que "
                           "permite derivar a contagem de arestas sem Dependency")
LACUNA_AUSENCIA_LEGITIMA = ("o probe nao emite o per-tier com um tier de Dependency 0 e 0 "
                            "linhas; sem esse tier nao ha ausencia legitima para conferir")
LACUNA_GEO_MEDIDA = ("o probe nao emite 'geometria.caixa_na_tela_px' completa "
                     "(x/y/largura/altura finitos) para a medida")
LACUNA_GEO_CLIPPING = RC.LACUNA_GEOMETRIA
LACUNA_HANDLER = ("o probe nao emite 'handler_invocado' (o caminho do handler do botao "
                  "'Skills' da run, RSTV-30/RSTV-5) — contrato KIT-09, ainda nao emitido")
LACUNA_CLIQUE_FISICO = ("o probe nao emite 'clique_fisico' ({recebido, alvo}): clique FISICO "
                        "e teste DISTINTO do handler; sem ele o handler nao prova o clique")
LACUNA_OBSTRUCAO = ("o probe nao emite 'obstrucao' ({avaliada, obstruido, por}): "
                    "'ativo_na_hierarquia' NAO prova ausencia de obstrucao")
LACUNA_SESSAO = ("a identidade nao declara 'sessao_esperada' nem as observacoes trazem "
                 "'sessao': nao ha como julgar dado velho")
LACUNA_MALFORMADO = RC.LACUNA_MALFORMADO


# --------------------------------------------- origem declarada (F1 do KIT-09R) --
#
# MARCADORES DECLARATIVOS de origem SINTETICA/FIXTURE. Uma entrada que se declara
# sintetica/simulada/rotulada como fixture NAO qualifica runtime — na API, na lista
# de observacoes, no envelope e na CLI. O DEFEITO observado continua reprovando
# (fixture com defeito segue REPROVADO); o que a origem declarada retira e a
# QUALIFICACAO (OK / prova_runtime), nunca a acusacao do defeito.
SINTETICO_CHAVES = ("sintetico", "simulado", "simulacao", "fixture_sintetica")


def _marcas_de_origem(d):
    """Marcas declaradas de origem sintetica/fixture num dict (observacao/envelope)."""
    if not isinstance(d, dict):
        return []
    motivos = []
    rot = RC._txt(d.get("rotulo_fixture"))
    if rot:
        motivos.append("rotulo_fixture=%r" % rot)
    for chave in SINTETICO_CHAVES:
        if d.get(chave) is True:
            motivos.append("%s=true" % chave)
    return motivos


def _guarda_origem(contrib, envelope):
    """Motivos que RETIRAM a qualificacao runtime de qualquer criterio (F1).

    Duas frentes: (a) a observacao declarando origem sintetica/fixture; (b) o
    ENVELOPE declarando origem sintetica/fixture ou CONTRADIZENDO a procedencia
    das observacoes. Contradicao/falsidade de origem falha FECHADO: nenhum
    criterio do arquivo vira prova de runtime.
    """
    motivos = []
    vistos = set()

    def _add(m):
        if m not in vistos:
            vistos.add(m)
            motivos.append(m)

    for o in contrib:
        for m in _marcas_de_origem(o):
            _add("ORIGEM DECLARADA SINTETICA/FIXTURE (%s): testa o avaliador, NAO e leitura "
                 "de jogo — nao qualifica runtime" % m)
    for m in _marcas_de_origem(envelope):
        _add("o ENVELOPE declara ORIGEM SINTETICA/FIXTURE (%s): nenhum criterio deste "
             "arquivo e prova de runtime real" % m)
    if isinstance(envelope, dict):
        proc_env = str(envelope.get("procedencia") or "").strip().lower()
        if proc_env:
            for o in contrib:
                if RC._procedencia(o) != proc_env:
                    _add("PROCEDENCIA CONTRADITORIA: o envelope declara %r e a observacao "
                         "declara %r — origem contraditoria RECUSA a qualificacao"
                         % (proc_env, RC._procedencia(o)))
                    break
    return motivos


def _guarda_sessao(contrib, ident):
    """Motivos que retiram a qualificacao de observacao de OUTRA sessao (F6).

    Nao suprime defeito: o defeito observado continua REPROVADO. O que se recusa e
    rotular dado de outra rodada como prova da rodada ATUAL.
    """
    esperada = RC._txt((ident or {}).get("sessao_esperada"))
    if not esperada:
        return []
    motivos = []
    for o in contrib:
        s = RC._txt(RC._campo(o, "sessao"))
        if s and s != esperada:
            motivos.append("a observacao e da sessao %r, mas a sessao esperada da rodada e "
                           "%r: DADO DE OUTRA RODADA nao qualifica a rodada atual"
                           % (s, esperada))
    return motivos


# ------------------------------- alvo esperado declarado do clique (F5) --

# Alvo esperado do CLIQUE FISICO do botao da RUN, declarado ANTES da leitura.
# Origem: AUT-5 S4 / RSTV-30 ("PNG do HUD com o botao 'Skills'") — o caminho e do
# CENARIO, e nao um path universal de qualquer jogo. Pode ser sobrescrito por
# declaracao explicita (`clique_fisico_alvo_esperado`/`alvo_botao_run` na observacao
# ou `alvo_botao_run` na identidade); sem alvo declarado o criterio NAO julga.
ALVO_BOTAO_RUN = "BottomBar/SkillsButton"
_RE_CAMINHO = re.compile(r"^[A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]+)+$")


def _valor_caminho(v):
    """Valida um CAMINHO observado: string nao vazia. -> (valor, motivo|None)."""
    if not isinstance(v, str) or not v.strip():
        return None, "%r NAO e um caminho valido (esperado string nao vazia)" % (v,)
    return v.strip(), None


def _valor_indice(v):
    """Valida um INDICE observado: inteiro >= 0 (bool nao e indice)."""
    if isinstance(v, bool) or not isinstance(v, int):
        return None, "%r NAO e um indice valido (esperado inteiro >= 0)" % (v,)
    if v < 0:
        return None, "indice NEGATIVO (%r): fora do dominio de um indice de sibling" % (v,)
    return v, None


def _tem_template(txt):
    """O texto carrega token de TEMPLATE do motor ('*0', '[N]', '@atributo@')?"""
    if not isinstance(txt, str) or not txt:
        return False
    return any(rx.search(txt) for _, rx in RC._RE_MARCADORES)


def _alvo_esperado_clique(o, ident):
    """(alvo_esperado, motivo) do clique fisico — declaracao independente validada."""
    declarado = None
    for fonte, chave in ((o, "clique_fisico_alvo_esperado"), (o, "alvo_botao_run"),
                         (ident, "alvo_botao_run"), (ident, "clique_fisico_alvo_esperado")):
        v = RC._txt((fonte or {}).get(chave))
        if v:
            declarado = v
            break
    if not declarado:
        declarado = RC._txt(ALVO_BOTAO_RUN)
    if not declarado:
        return None, ("nenhum alvo esperado declarado para o clique do botao da RUN: sem "
                      "alvo independente nao se comprova o clique (INDETERMINADO)")
    if not _RE_CAMINHO.match(declarado):
        return None, ("o alvo esperado declarado (%r) NAO e um path/id valido: alvo invalido "
                      "nao qualifica o criterio" % (declarado,))
    return declarado, None


# ------------------------------------------------------------------ primitivas --

def _bloco(obs, nome):
    """Le um campo cujo valor e um DICTO (janela/obstrucao/clique_fisico/...)."""
    v = RC._campo(obs, nome)
    return v if isinstance(v, dict) else None


def _res(contrib, defeitos, dados, motivos, observado, lacuna, indeterminado=False):
    return {"contrib": contrib, "defeitos": defeitos, "dados": dados, "motivos": motivos,
            "observado": observado, "lacuna": lacuna, "indeterminado": indeterminado}


def _vazio(lacuna, observado="nenhuma observacao"):
    return _res([], [], False, [], observado, lacuna)


def _bool_exigido(bloco, chave, rotulo, motivos):
    """Le um booleano obrigatorio: ausente/invalido vira MOTIVO (nunca OK)."""
    if chave not in bloco:
        motivos.append("%s: campo %r AUSENTE (registro incompleto)" % (rotulo, chave))
        return None
    v = bloco.get(chave)
    if not isinstance(v, bool):
        motivos.append("%s: %r MALFORMADO (%r) — esperado booleano" % (rotulo, chave, v))
        return None
    return v


# ------------------------------------------- janela read-only (abre/fecha/rotas) --

def _reg_janela_flag(flag, titulo):
    def regra(alvos, ident):
        contrib, defeitos, motivos, dados = [], [], [], False
        for o in alvos:
            j = _bloco(o, "janela")
            if j is None:
                continue
            contrib.append(o)
            dados = True
            v = _bool_exigido(j, flag, "janela", motivos)
            if v is False:
                defeitos.append("%s: janela nao registrou (%s=%r)" % (titulo, flag, j.get(flag)))
        if not dados:
            return _vazio(LACUNA_JANELA_MICRO)
        return _res(contrib, defeitos, dados, motivos,
                    "janela: %s" % (sorted({k for o in contrib
                                            for k in (_bloco(o, "janela") or {})}) or "nada"),
                    LACUNA_JANELA_MICRO)
    return regra


# ------------------------------------------------- personagem (alvo declarado) --

def _reg_personagem(alvos, ident):
    contrib, defeitos, motivos, dados = [], [], [], False
    lidos = []
    for o in alvos:
        esperado = RC._campo(o, "personagem_esperado") or RC._campo(o, "alvo_personagem")
        ctx = RC._campo(o, "personagem")
        obs = None
        if isinstance(ctx, dict):
            obs = ctx.get("personagem")
        elif isinstance(ctx, str):
            obs = ctx
        if esperado is None and obs is None:
            continue
        contrib.append(o)
        dados = True
        lidos.append(obs)
        if esperado is None:
            motivos.append("sem 'personagem_esperado' (alvo do cenario) — nao da para "
                           "julgar o alvo")
            continue
        if not str(obs or "").strip():
            motivos.append("personagem observado AUSENTE (nada selecionado?)")
            continue
        if str(obs).strip() != str(esperado).strip():
            defeitos.append("personagem errado: esperado %r, lido %r"
                            % (str(esperado), str(obs)))
    if not dados:
        return _vazio(RC.LACUNA_PERSONAGEM)
    indeterminado = (bool(motivos)
                     and all(m.startswith("sem 'personagem_esperado'") for m in motivos))
    return _res(contrib, defeitos, dados, motivos, "personagens lidos: %s" % (lidos or "nenhum"),
                RC.LACUNA_PERSONAGEM, indeterminado)


# --------------------------------------- skills/pontos: pares SEM MUTACAO (guarda) --

def _pares_dim(o, dim):
    """Pares antes/depois de uma dimensao ('skills'/'pontos'), explicitos ou snapshot."""
    pares = []
    a, b = RC._campo(o, dim + "_antes"), RC._campo(o, dim + "_depois")
    if a is not None or b is not None:
        pares.append((a, b))
    sa, sb = RC._campo(o, "snapshot_antes"), RC._campo(o, "snapshot_depois")
    if isinstance(sa, dict) or isinstance(sb, dict):
        sa, sb = sa or {}, sb or {}
        if dim in sa or dim in sb:
            pares.append((sa.get(dim), sb.get(dim)))
    return pares


def _reg_dim(dim):
    def regra(alvos, ident):
        contrib, defeitos, motivos, dados = [], [], [], False
        for o in alvos:
            pares = _pares_dim(o, dim)
            if not pares:
                continue
            contrib.append(o)
            dados = True
            for antes, depois in pares:
                if antes is None or depois is None:
                    motivos.append("%s: par antes/depois INCOMPLETO" % dim)
                    continue
                if dim == "pontos":
                    if not (RC._numerico(antes) and RC._numerico(depois)):
                        motivos.append("pontos: valor NAO numerico (antes=%r, depois=%r)"
                                       % (antes, depois))
                    elif not (RC._numero_finito(antes) is not None
                              and RC._numero_finito(depois) is not None):
                        # F4 do KIT-09R: finitude/dominio ANTES da comparacao — 'inf'
                        # nao e leitura de pontos; antes, inf == inf fechava OK.
                        motivos.append("pontos: valor NAO FINITO (antes=%r, depois=%r) — "
                                       "'NaN'/infinito nao mede pontos" % (antes, depois))
                    elif float(depois) < float(antes):
                        defeitos.append("GASTO de pontos: antes=%s, depois=%s" % (antes, depois))
                    elif float(depois) != float(antes):
                        defeitos.append("pontos MUDARAM: antes=%s, depois=%s" % (antes, depois))
                else:
                    if not (RC._lista_de_str(antes) and RC._lista_de_str(depois)):
                        motivos.append("skills: campo MALFORMADO — esperado lista de strings "
                                       "(antes=%s, depois=%s)"
                                       % (type(antes).__name__, type(depois).__name__))
                    elif sorted(antes) != sorted(depois):
                        defeitos.append("skills MUDARAM: antes=%s, depois=%s" % (antes, depois))
        if not dados:
            return _vazio(LACUNA_SKILLS_DIM % dim)
        return _res(contrib, defeitos, dados, motivos,
                    "'%s': %d leitura(s) com par antes/depois" % (dim, len(contrib)),
                    LACUNA_SKILLS_DIM % dim)
    return regra


# ------------------------------------------------ tooltip (render/placeholder) --

def _obs_texto(o):
    return (RC._texto(o, "texto_bruto"),
            RC._texto(o, "texto_renderizado"))


def _reg_render_observado(alvos, ident):
    """Render OBSERVADO do tooltip.

    F7 do KIT-09R: o criterio precisa de um DEFEITO observavel proprio (cobertura
    seletiva), nao so da ausencia. Defeito medido: o 'texto_renderizado' e
    IDENTICO ao TEMPLATE cru que ainda carrega token do motor ('*0'/'[N]'/
    '@atributo@') — o render nao aconteceu; a "leitura" e o proprio template.
    """
    contrib, motivos, dados, defeitos = [], [], False, []
    for o in alvos:
        bruto, render = _obs_texto(o)
        if not bruto and not render:
            continue
        contrib.append(o)
        dados = True
        if not render:
            motivos.append("texto RENDERIZADO nao observado (so o cru %r): o template do "
                           "motor nao prova o render" % (bruto,))
            continue
        if bruto and render and render.strip() == bruto.strip() and _tem_template(bruto):
            defeitos.append("texto RENDERIZADO IDENTICO ao TEMPLATE cru (%r): o render nao "
                            "aconteceu — o placeholder do motor continua literal" % (bruto,))
    if not dados:
        return _vazio(LACUNA_RENDER)
    return _res(contrib, defeitos, dados, motivos,
                "textos renderizados observados: %d" % sum(1 for o in contrib
                                                            if _obs_texto(o)[1]),
                LACUNA_RENDER)


def _reg_sem_placeholder(alvos, ident):
    contrib, defeitos, motivos, dados = [], [], [], False
    for o in alvos:
        achados, tem = RC._marcadores(o)
        if not tem:
            continue
        contrib.append(o)
        dados = True
        for a in achados:
            defeitos.append("placeholder %s em %s: %r" % (a["marcador"], a["campo"], a["trecho"]))
        if not RC._texto(o, "texto_renderizado"):
            motivos.append("texto RENDERIZADO nao observado (so o cru): nao da para afirmar "
                           "que o placeholder foi resolvido")
    if not dados:
        return _vazio(LACUNA_RENDER)
    return _res(contrib, defeitos, dados, motivos,
                "textos inspecionados: %d" % len(contrib), LACUNA_RENDER)


# --------------------------------------------- tooltip: pai/indice duplicacao --

def _reg_tooltip_campo(rotulo, ka, kb, validador):
    """Par antes/depois de um campo do tooltip, lido nas DUAS formas do contrato.

    F2 do KIT-09R: a leitura passa por `RC._campo` (topo + bloco `campos`
    NORMALIZADO do coletor real) — antes, o `o.get`/`in` do topo ignorava o bloco
    normalizado e um DEFEITO medido virava NAO_EXERCITADO.
    F4 do KIT-09R: tipo/dominio/formato sao validados ANTES da igualdade —
    `[]`/`[]`, `'bad'`/`'bad'` e `-1`/`-1` deixam de fechar OK.
    """
    def regra(alvos, ident):
        contrib, defeitos, motivos, dados = [], [], [], False
        for o in alvos:
            a, b = RC._campo(o, ka), RC._campo(o, kb)
            if a is None and b is None:
                continue
            contrib.append(o)
            dados = True
            if a is None or b is None:
                motivos.append("tooltip %s: par %s/%s INCOMPLETO (AUSENTE nao e leitura)"
                               % (rotulo, ka, kb))
                continue
            va, ma = validador(a)
            vb, mb = validador(b)
            if va is None or vb is None:
                motivos.append("tooltip %s: leitura MALFORMADA/FORA DE DOMINIO — %s"
                               % (rotulo, "; ".join(m for m in (ma, mb) if m)))
                continue
            if va != vb:
                defeitos.append("tooltip %s NAO restaurado: antes=%r, depois=%r"
                                % (rotulo, va, vb))
        if not dados:
            return _vazio(LACUNA_TOOLTIP_CAMPO % (rotulo, rotulo))
        return _res(contrib, defeitos, dados, motivos,
                    "ciclos de tooltip inspecionados: %d" % len(contrib),
                    LACUNA_TOOLTIP_CAMPO % (rotulo, rotulo))
    return regra


def _reg_sem_duplicata(alvos, ident):
    contrib, defeitos, motivos, dados = [], [], [], False
    for o in alvos:
        n = RC._campo(o, "janelas_duplicadas")
        d = RC._campo(o, "duplicata")
        if n is None and d is None:
            continue
        contrib.append(o)
        dados = True
        if n is not None:
            c = RC._contagem_observada(n)
            if c is None:
                motivos.append("janelas_duplicadas MALFORMADA (%r): exigida contagem "
                               "observada valida (numero finito >= 0)" % (n,))
            elif c > 0:
                defeitos.append("janela DUPLICADA: janelas_duplicadas=%s" % (n,))
        if d is not None:
            if not isinstance(d, bool):
                motivos.append("duplicata MALFORMADA (%r): esperado booleano" % (d,))
            elif d:
                defeitos.append("janela duplicada (duplicata=true)")
    if not dados:
        return _vazio(LACUNA_DUPLICATA)
    return _res(contrib, defeitos, dados, motivos,
                "leituras com contagem de duplicata: %d" % len(contrib), LACUNA_DUPLICATA)


# ------------------------------------------------- dependencia real x arestas --

def _contagem(v):
    return RC._contagem_observada(v)


def _reg_dep_arestas(alvos, ident):
    """linhas por tier == Dependency real por tier (RSTV-25b).

    F3 do KIT-09R: exige leitura MENSURAVEL dos DOIS lados de cada tier. Ausencia
    nao e zero certo: um tier presente em so um lado vira motivo (nunca OK), mapas
    vazios nao aprovam, e a aresta de T5 e julgada pela regra geral (sem o
    `continue` que pulava T5).
    """
    contrib, defeitos, motivos, dados, indet = [], [], [], False, False
    for o in alvos:
        linhas = RC._campo(o, "linhas_dependencia")
        dep = RC._campo(o, "dependency_por_tier")
        if dep is None:
            dep = RC._campo(o, "dependency")
        if linhas is None and dep is None:
            continue
        contrib.append(o)
        dados = True
        if not isinstance(linhas, dict) or not isinstance(dep, dict):
            motivos.append("linhas/Dependency em formato INCOMPLETO (esperado dict por tier, "
                           "linhas=%s dep=%s)" % (type(linhas).__name__, type(dep).__name__))
            indet = True
            continue
        tiers = sorted(set(list(linhas) + list(dep)))
        if not tiers:
            motivos.append("nenhum tier lido (mapas vazios): sem leitura nao ha confronto "
                           "mensuravel — vazio nao aprova")
            indet = True
            continue
        for tier in tiers:
            pres_l, pres_d = tier in linhas, tier in dep
            nl, nd = linhas.get(tier), dep.get(tier)
            invalidos = []
            if pres_l and _contagem(nl) is None:
                invalidos.append("linhas=%r" % (nl,))
            if pres_d and _contagem(nd) is None:
                invalidos.append("Dependency=%r" % (nd,))
            if invalidos:
                motivos.append("%s: valor INVALIDO no confronto (%s) — contagem observada "
                               "(numero finito >= 0) obrigatoria dos dois lados"
                               % (tier, ", ".join(invalidos)))
                indet = True
                continue
            if not pres_l or not pres_d:
                motivos.append("%s: leitura AUSENTE de um dos lados (linhas=%s, Dependency=%s) "
                               "— ausencia NAO e zero; confronto impossivel"
                               % (tier, nl if pres_l else "AUSENTE",
                                  nd if pres_d else "AUSENTE"))
                indet = True
                continue
            vl, vd = _contagem(nl), _contagem(nd)
            if vd == 0 and vl == 0:
                continue  # ausencia LEGITIMA: 0/0 medido dos dois lados
            if vd == 0 and vl > 0:
                defeitos.append("%s: %s linha(s) para Dependency=0 — aresta INVENTADA "
                                "(conector sem Dependency real)" % (tier, nl))
            elif vl < vd:
                defeitos.append("%s: %s linha(s) para Dependency=%s — conector AUSENTE "
                                "(faltando linha)" % (tier, nl, nd))
            elif vl > vd:
                defeitos.append("%s: %s linha(s) para Dependency=%s — aresta INVENTADA "
                                "(conector sem Dependency real)" % (tier, nl, nd))
    if not dados:
        return _vazio(LACUNA_DEP_TIERS)
    return _res(contrib, defeitos, dados, motivos,
                "tiers inspecionados: %d" % len(contrib), LACUNA_DEP_TIERS, indet)


def _reg_sem_aresta_inventada(alvos, ident):
    """Nenhuma linha sem Dependency real — julga TODOS os tiers, inclusive T5.

    F3 do KIT-09R: a aresta inventada de T5 era pulada (`if tier == 'T5': continue`)
    e o defeito medido desaparecia no criterio especifico.
    """
    contrib, defeitos, motivos, dados = [], [], [], False
    for o in alvos:
        declarado = RC._campo(o, "arestas_inventadas")
        linhas = RC._campo(o, "linhas_dependencia")
        dep = RC._campo(o, "dependency_por_tier")
        if dep is None:
            dep = RC._campo(o, "dependency")
        derivavel = isinstance(linhas, dict) and isinstance(dep, dict)
        if declarado is None and not derivavel:
            continue
        contrib.append(o)
        dados = True
        if declarado is not None and not isinstance(declarado, bool):
            n = _contagem(declarado)
            if n is None:
                motivos.append("`arestas_inventadas` MALFORMADA (%r): exigida contagem "
                               "observada valida (numero finito >= 0)" % (declarado,))
            elif n > 0:
                defeitos.append("aresta de dependencia INVENTADA (sem Dependency real)")
        elif isinstance(declarado, bool) and declarado:
            defeitos.append("arestas_inventadas=true (dependencia inventada)")
        if derivavel:
            for tier in sorted(set(list(linhas) + list(dep))):
                pres_l, pres_d = tier in linhas, tier in dep
                vl, vd = linhas.get(tier), dep.get(tier)
                if pres_l and _contagem(vl) is None:
                    motivos.append("%s: linhas=%r INVALIDO na derivacao da aresta"
                                   % (tier, vl))
                    continue
                if pres_d and _contagem(vd) is None:
                    motivos.append("%s: Dependency=%r INVALIDO na derivacao da aresta"
                                   % (tier, vd))
                    continue
                if not pres_l or not pres_d:
                    motivos.append("%s: leitura AUSENTE de um dos lados (linhas=%s, "
                                   "Dependency=%s) — sem os dois lados nao se prova "
                                   "ausencia de aresta inventada"
                                   % (tier, vl if pres_l else "AUSENTE",
                                      vd if pres_d else "AUSENTE"))
                    continue
                if _contagem(vl) > _contagem(vd):
                    defeitos.append("%s: %s linha(s) para Dependency=%s — aresta INVENTADA "
                                    "(conector sem Dependency real)" % (tier, vl, vd))
    if not dados:
        return _vazio(LACUNA_ARESTA_INVENTADA)
    return _res(contrib, defeitos, dados, motivos,
                "leituras com contagem de arestas: %d" % len(contrib),
                LACUNA_ARESTA_INVENTADA)


def _reg_ausencia_legitima(alvos, ident):
    """Tier com Dependency 0 e 0 LINHAS continua sem conector (ausencia LEGITIMA).

    F3 do KIT-09R: ausencia nao e zero. O criterio so julga o que foi LIDO: sem o
    mapa de linhas (ausente/string) nao ha ausencia legitima para conferir; e o
    tier sem Dependency explicito nao entra como se fosse zero.
    """
    contrib, defeitos, motivos, dados = [], [], [], False
    for o in alvos:
        dep = RC._campo(o, "dependency_por_tier")
        if dep is None:
            dep = RC._campo(o, "dependency")
        if not isinstance(dep, dict):
            continue
        linhas = RC._campo(o, "linhas_dependencia")
        if not isinstance(linhas, dict):
            contrib.append(o)
            dados = True
            motivos.append("linhas por tier AUSENTES/INCOMPLETAS (tipo %s): a ausencia "
                           "legitima exige ler os DOIS lados (0/0), nunca assumir zero"
                           % type(linhas).__name__)
            continue
        achou = False
        for tier in sorted(dep):
            vd = _contagem(dep.get(tier))
            if vd is None:
                achou = True
                motivos.append("%s: Dependency=%r MALFORMADA — sem leitura valida nao ha "
                               "ausencia legitima" % (tier, dep.get(tier)))
                continue
            if vd != 0:
                continue
            achou = True
            if tier not in linhas:
                motivos.append("%s: Dependency=0 mas a contagem de LINHAS nao foi lida — "
                               "ausencia mede-se dos dois lados" % tier)
                continue
            vl = _contagem(linhas.get(tier))
            if vl is None:
                motivos.append("%s: linhas=%r MALFORMADA — sem leitura valida nao ha "
                               "ausencia legitima" % (tier, linhas.get(tier)))
                continue
            if vl > 0:
                defeitos.append("%s sem Dependency real mas com %s linha(s): conector "
                                "INVENTADO (ausencia legitima desrespeitada)"
                                % (tier, linhas.get(tier)))
        if achou:
            contrib.append(o)
            dados = True
    if not dados:
        return _vazio(LACUNA_AUSENCIA_LEGITIMA)
    return _res(contrib, defeitos, dados, motivos,
                "tiers com ausencia legitima conferidos: %d" % len(contrib),
                LACUNA_AUSENCIA_LEGITIMA)


# ---------------------------------------------------------- geometria (medida) --

def _reg_geo_medida(alvos, ident):
    contrib, defeitos, motivos, dados = [], [], [], False
    for o in alvos:
        b, invalido = RC._bbox(o)
        if invalido:
            contrib.append(o)
            dados = True
            motivos.append(invalido)
            continue
        if b is None:
            continue
        contrib.append(o)
        dados = True
        if b["largura"] <= 0 or b["altura"] <= 0:
            defeitos.append("dimensao NAO positiva: largura=%s altura=%s"
                            % (b["largura"], b["altura"]))
    if not dados:
        return _vazio(LACUNA_GEO_MEDIDA)
    return _res(contrib, defeitos, dados, motivos,
                "caixas medidas: %d" % len(contrib), LACUNA_GEO_MEDIDA)


def _reg_geo_clipping(alvos, ident):
    contrib, defeitos, motivos, dados = [], [], [], False
    for o in alvos:
        b, invalido = RC._bbox(o)
        if invalido:
            contrib.append(o)
            dados = True
            motivos.append(invalido)
            continue
        if b is None:
            continue
        contrib.append(o)
        dados = True
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
    if not dados:
        return _vazio(LACUNA_GEO_CLIPPING)
    return _res(contrib, defeitos, dados, motivos,
                "geometrias inspecionadas: %d" % len(contrib), LACUNA_GEO_CLIPPING)


# ------------------------------------------ botao da run: handler x clique x obstrucao --

def _reg_handler(alvos, ident):
    contrib, defeitos, motivos, dados = [], [], [], False
    for o in alvos:
        v = RC._campo(o, "handler_invocado")
        if v is None:
            continue
        contrib.append(o)
        dados = True
        if not isinstance(v, bool):
            motivos.append("handler_invocado MALFORMADO (%r): esperado booleano" % (v,))
        elif v is False:
            defeitos.append("handler NAO invocado: o caminho do handler do botao 'Skills' "
                            "nao foi exercitado")
    if not dados:
        return _vazio(LACUNA_HANDLER)
    return _res(contrib, defeitos, dados, motivos,
                "leituras de handler: %d" % len(contrib), LACUNA_HANDLER)


def _reg_clique_fisico(alvos, ident):
    """Clique FISICO do botao da RUN, confrontado com o ALVO ESPERADO declarado (F5).

    Antes, bastava `recebido=true` com um `alvo` nao vazio: um clique em
    `MainMenu/QuitButton` aprovava o criterio do botao 'Skills' da run. Agora o
    alvo esperado e resolvido de uma declaracao independente e VALIDADA (path/id);
    alvo errado REPROVA, alvo esperado ausente/invalido NAO julga.
    """
    contrib, defeitos, motivos, dados = [], [], [], False
    for o in alvos:
        c = _bloco(o, "clique_fisico")
        if c is None:
            continue
        contrib.append(o)
        dados = True
        recebido = _bool_exigido(c, "recebido", "clique_fisico", motivos)
        if recebido is False:
            defeitos.append("clique FISICO nao recebido (clique_fisico.recebido=false): o "
                            "handler nao prova que o clique chegou ao botao")
            continue
        if recebido is None:
            continue  # campo ausente/malformado: o motivo ja foi registrado
        esperado, m_esp = _alvo_esperado_clique(o, ident)
        if esperado is None:
            motivos.append(m_esp)
            continue
        observado = RC._txt(c.get("alvo"))
        if not observado:
            motivos.append("clique_fisico.recebido=true sem 'alvo' nomeado: nao prova que o "
                           "clique atingiu o botao DA RUN (esperado %r)" % (esperado,))
            continue
        if not _RE_CAMINHO.match(observado):
            motivos.append("clique_fisico.alvo MALFORMADO (%r): esperado path/id valido do "
                           "botao da RUN (%r)" % (observado, esperado))
            continue
        if observado != esperado:
            defeitos.append("clique FISICO atingiu OUTRO alvo: esperado %r, observado %r — "
                            "nao prova o clique no botao DA RUN" % (esperado, observado))
    if not dados:
        return _vazio(LACUNA_CLIQUE_FISICO)
    return _res(contrib, defeitos, dados, motivos,
                "leituras de clique fisico: %d" % len(contrib), LACUNA_CLIQUE_FISICO)


def _reg_sem_obstrucao(alvos, ident):
    contrib, defeitos, motivos, dados = [], [], [], False
    for o in alvos:
        bl = _bloco(o, "obstrucao")
        if bl is None:
            ativo = RC._campo(o, "ativo_na_hierarquia")
            if ativo is None:
                continue
            contrib.append(o)
            dados = True
            motivos.append("obstrucao NAO avaliada: 'ativo_na_hierarquia'=%r NAO prova "
                           "ausencia de obstrucao (o botao pode estar ativo e coberto por "
                           "outra UI); exige 'obstrucao'={avaliada, obstruido, por}" % (ativo,))
            continue
        contrib.append(o)
        dados = True
        av = _bool_exigido(bl, "avaliada", "obstrucao", motivos)
        obs = _bool_exigido(bl, "obstruido", "obstrucao", motivos)
        if av is False:
            motivos.append("obstrucao.avaliada=false: a obstrucao NAO foi verificada "
                           "(declarar 'nao avaliada' nunca fecha OK)")
        if obs is True:
            defeitos.append("botao OBSTRUIDO por %r: clique nao chegaria ao botao"
                            % (RC._txt(bl.get("por")) or "desconhecido",))
    if not dados:
        return _vazio(LACUNA_OBSTRUCAO)
    return _res(contrib, defeitos, dados, motivos,
                "leituras de obstrucao: %d" % len(contrib), LACUNA_OBSTRUCAO)


# ------------------------------------------------------- sessao atual (dado velho) --

def _reg_sessao_atual(alvos, ident):
    esperada = RC._txt((ident or {}).get("sessao_esperada"))
    contrib, defeitos, motivos, dados = [], [], [], False
    for o in alvos:
        s = RC._txt(RC._campo(o, "sessao"))
        if not s:
            continue
        contrib.append(o)
        dados = True
        if esperada and s != esperada:
            defeitos.append("DADO VELHO: observacao da sessao %r != sessao esperada %r "
                            "(resultado de outra rodada/bytes)" % (s, esperada))
    if not esperada:
        return _res(contrib, [], dados, ["a identidade nao declara 'sessao_esperada': nao ha "
                                         "como julgar dado velho"], "sessoes observadas: %d"
                    % len(contrib), LACUNA_SESSAO)
    if not dados:
        return _vazio(LACUNA_SESSAO)
    return _res(contrib, defeitos, dados, motivos,
                "sessao esperada %r; observacoes: %d" % (esperada, len(contrib)), LACUNA_SESSAO)


# ------------------------------------------------------------------ definicoes --

# (id, pai, cenario AUT-5, esperado INDEPENDENTE, origem do esperado, regra).
# O esperado NUNCA vem da regra: a regra so devolve o OBSERVADO.
CENARIOS = (
    ("KIT09-RSTV21-abre", "RSTV-21-janela-ciclo", "S1/S4",
     "janela read-only ABERTA no ciclo",
     "AUT-5 S1/S4 (marcador RSTV-21 'janela read-only ABERTA')",
     _reg_janela_flag("aberta", "abertura")),
    ("KIT09-RSTV21-fecha", "RSTV-21-janela-ciclo", "S1/S4",
     "janela read-only FECHADA no ciclo",
     "AUT-5 S1/S4 (marcador RSTV-21 'janela read-only fechada')",
     _reg_janela_flag("fechada", "fechamento")),
    ("KIT09-RSTV21-fecha-x", "RSTV-21-janela-ciclo", "S1/S4",
     "fechamento pelo X registrado",
     "AUT-5 S1/S4 item 2 do pedido ao dono ('fechando com X e com Esc')",
     _reg_janela_flag("fechado_x", "fechamento por X")),
    ("KIT09-RSTV21-fecha-esc", "RSTV-21-janela-ciclo", "S1/S4",
     "fechamento pelo Esc registrado",
     "AUT-5 S1/S4 item 2 do pedido ao dono ('fechando com X e com Esc')",
     _reg_janela_flag("fechado_esc", "fechamento por Esc")),
    ("KIT09-RSTV6-personagem", "RSTV-6-readonly-personagem", "S1/S3/S4",
     "personagem lido == personagem_esperado declarado ANTES da leitura",
     "AUT-5 'origem_do_esperado': nome declarado pelo dono na rodada autorizada "
     "(nunca lido da mesma observacao julgada)",
     _reg_personagem),
    ("KIT09-RSTV6-skills-sem-mutacao", "RSTV-6-readonly-skills-pontos", "S1/S4",
     "skills_antes == skills_depois (nenhuma skill alterada)",
     "guarda de leitura somente do RSTV-6 (AUT-5 S1/S4)",
     _reg_dim("skills")),
    ("KIT09-RSTV6-pontos-sem-mutacao", "RSTV-6-readonly-skills-pontos", "S1/S4",
     "pontos_antes == pontos_depois (nenhum ponto gasto)",
     "guarda de leitura somente do RSTV-6 (AUT-5 S1/S4)",
     _reg_dim("pontos")),
    ("KIT09-RSTV26-render-observado", "RSTV-26-placeholders", "S5",
     "texto RENDERIZADO do tooltip observado",
     "AUT-5 S5 (so o render prova o placeholder resolvido; F6 do CIC-3R)",
     _reg_render_observado),
    ("KIT09-RSTV26-sem-placeholder", "RSTV-26-placeholders", "S5",
     "nenhum '*0' / '[indice]' / '@atributo@' literal no texto RENDERIZADO",
     "AUT-5 S5 + contrato RSTV-26 (placeholders do tooltip)",
     _reg_sem_placeholder),
    ("KIT09-RSTV21-tooltip-pai", "RSTV-21-tooltip-restauracao", "S1",
     "tooltip_pai_antes == tooltip_pai_depois",
     "AUT-5 S1 (o mod reparenta o tooltip no hover e tem de restaurar)",
     _reg_tooltip_campo("pai", "tooltip_pai_antes", "tooltip_pai_depois", _valor_caminho)),
    ("KIT09-RSTV21-tooltip-indice", "RSTV-21-tooltip-restauracao", "S1",
     "tooltip_indice_antes == tooltip_indice_depois",
     "AUT-5 S1 (indice de sibling restaurado no fechar)",
     _reg_tooltip_campo("indice", "tooltip_indice_antes", "tooltip_indice_depois",
                        _valor_indice)),
    ("KIT09-RSTV21-sem-duplicata", "RSTV-21-tooltip-restauracao", "S1/S4",
     "janelas_duplicadas == 0 (contagem observada valida)",
     "AUT-5 S1/S4 ('abrir duas vezes nao duplica janela')",
     _reg_sem_duplicata),
    ("KIT09-RSTV25b-arestas", "RSTV-25b-dependencia", "S5",
     "linhas por tier == Dependency real por tier",
     "RSTV-24b/RSTV-25 do mod via AUT-5 S5 (Dependency REAL governa as arestas)",
     _reg_dep_arestas),
    ("KIT09-RSTV25b-sem-aresta-inventada", "RSTV-25b-dependencia", "S5",
     "arestas_inventadas == 0 (nenhuma linha sem Dependency real)",
     "RSTV-25b (conector sem Dependency = aresta inventada); AUT-5 S5",
     _reg_sem_aresta_inventada),
    ("KIT09-RSTV25b-ausencia-legitima", "RSTV-25b-dependencia", "S5",
     "tier com Dependency 0 e 0 linhas continua sem conector (ausencia legitima)",
     "AUT-5 S5 ('T5 sem Dependency e ausencia LEGITIMA')",
     _reg_ausencia_legitima),
    ("KIT09-RSTV-geo-medida", "RSTV-geometria-clipping", "S5",
     "caixa_na_tela_px com x/y/largura/altura finitos e dimensoes > 0",
     "AUT-5 S5 (bbox do hover/arvore; F4 do CIC-3R: 'NaN'/infinito nao mede)",
     _reg_geo_medida),
    ("KIT09-RSTV-geo-clipping", "RSTV-geometria-clipping", "S5",
     "caixa dentro da tela (sem clipping horizontal/vertical)",
     "AUT-5 S5 + RSTV-23i (a arvore que excede a area tem de reduzir)",
     _reg_geo_clipping),
    ("KIT09-RSTV5-handler", PAI_BOTAO, "S4",
     "handler do botao 'Skills' da run INVOCADO",
     "AUT-5 guards_run/RSTV-5 + RSTV-30 (o portao decide o CLIQUE); teste de HANDLER",
     _reg_handler),
    ("KIT09-RSTV5-clique-fisico", PAI_BOTAO, "S4",
     "clique FISICO recebido pelo botao da run (alvo nomeado)",
     "AUT-5 S4 ('PNG do HUD com o botao' = clique fisico); teste DISTINTO do handler",
     _reg_clique_fisico),
    ("KIT09-RSTV5-sem-obstrucao", PAI_BOTAO, "S4",
     "obstrucao AVALIADA e ausente (o botao nao esta coberto)",
     "AUT-5 S4/RSTV-30: 'ativo' nao prova ausencia de obstrucao",
     _reg_sem_obstrucao),
    ("KIT09-sessao-atual", None, "todas",
     "sessao da observacao == sessao esperada da identidade",
     "identidade da rodada (hash/sessao da build ATUAL); dado de outra sessao e VELHO",
     _reg_sessao_atual),
)


# ------------------------------------------------------------------ avaliacao --

def _definicoes():
    vistos = {}
    for (cid, pai, cenario, esperado, origem, regra) in CENARIOS:
        if cid in vistos:
            raise RuntimeError("KIT-09: criterio duplicado: %s" % cid)
        if not RC._txt(esperado) or not RC._txt(origem):
            raise RuntimeError("KIT-09: criterio %s sem esperado/origem independente" % cid)
        if pai is not None and pai not in CAPACIDADES_MACRO and pai != PAI_BOTAO:
            raise RuntimeError("KIT-09: criterio %s com pai desconhecido: %r" % (cid, pai))
        if not callable(regra):
            raise RuntimeError("KIT-09: criterio %s sem regra executavel" % cid)
        vistos[cid] = True
    return True


_definicoes()

IDS = tuple(c[0] for c in CENARIOS)


def avaliar_cenarios(observacoes, identidade, envelope=None):
    """Avalia os criterios PEQUENOS do KIT-09 e devolve a lista (ordem de CENARIOS).

    Reusa o fechamento do CIC-3 (`_fecha`): fixture nunca vira OK, identidade
    `fonte_sha`/`dll_sha` e obrigatoria para OK, hash divergente -> INDETERMINADO,
    sessoes misturadas -> INDETERMINADO. Nunca levanta por dado ausente/malformado:
    a capacidade sem leitura sai NAO_EXERCITADO; excecao -> INDETERMINADO com o id
    preservado (o quadro do KIT-09 e sempre completo).

    `envelope` (opcional) e o arquivo/objeto de origem das observacoes. Ele entra
    na GUARDA DE ORIGEM (F1): envelope/observacao declarando origem sintetica ou
    contradizendo a procedencia retira a qualificacao runtime de TODOS os criterios
    do arquivo — sem apagar o defeito observado (que continua REPROVANDO).
    """
    obs = RC._obs_lista(observacoes)
    identidade = identidade if isinstance(identidade, dict) else {}
    criterios = []
    for (cid, pai, cenario, esperado, origem, regra) in CENARIOS:
        alvos, excluidos = ([], {})
        if pai is None:
            alvos = list(obs)
        else:
            alvos, excluidos = RC._selecionar_alvos(obs, pai)
        try:
            r = regra(alvos, identidade)
            motivos = list(r["motivos"])
            motivos += _guarda_origem(r["contrib"], envelope)
            motivos += _guarda_sessao(r["contrib"], identidade)
            estado, proc, motivo = RC._fecha(
                r["contrib"], r["defeitos"], r["dados"], identidade, esperado,
                r["observado"], motivos, r.get("indeterminado", False))
            ev = [e for o in r["contrib"] for e in RC._evidencia(o)]
            extra = RC._extras(estado, proc, identidade, r["contrib"], lacuna=r.get("lacuna"))
            c = RC._criterio(cid, estado, proc, esperado, r["observado"], motivo, ev,
                             extra=extra)
            c["origem_marcas"] = sorted(
                set(_marcas_de_origem(envelope))
                | {m for o in r["contrib"] for m in _marcas_de_origem(o)})
            c["sessoes_lidas"] = sorted({RC._txt(RC._campo(o, "sessao"))
                                         for o in r["contrib"]
                                         if RC._txt(RC._campo(o, "sessao"))})
        except Exception as erro:  # dado malformado nao derruba o avaliador
            c = RC._criterio(
                cid, INDETERMINADO, "execucao", esperado,
                "erro ao avaliar: %s: %s" % (type(erro).__name__, erro),
                "observacao malformada derrubou o criterio (id preservado)", [],
                extra=RC._extras(INDETERMINADO, "execucao", identidade, [],
                                 lacuna=LACUNA_MALFORMADO))
            c["origem_marcas"] = sorted(_marcas_de_origem(envelope))
            c["sessoes_lidas"] = []
        c["capacidade_pai"] = pai
        c["cenario_origem"] = cenario
        c["esperado_origem"] = origem
        c["tarefa_kit"] = TAREFA_KIT
        c["tarefa_origem"] = TAREFA_AUT5  # reuso do CIC-3/AUT-5 (rastreabilidade)
        c["kit09"] = True
        c.setdefault("alvos_julgados", len(alvos))
        if excluidos:
            c["alvos_excluidos"] = dict(sorted(excluidos.items()))
        criterios.append(c)
    return criterios


def por_capacidade(criterios):
    """Roll-up: pior estado por capacidade pai (a decisao existente consome isto)."""
    agregado = {}
    for c in criterios:
        pai = c.get("capacidade_pai") or "(kit09-meta)"
        atual = agregado.get(pai)
        if atual is None or _PIOR.index(c["estado"]) < _PIOR.index(atual):
            agregado[pai] = c["estado"]
    return agregado


def resumir(criterios, identidade):
    contagem = {}
    for c in criterios:
        contagem[c["estado"]] = contagem.get(c["estado"], 0) + 1
    # as 7 macro do CIC-3 aparecem sempre (mesmo sem criterio pequeno avaliado)
    por_cap = {cid: NAO_EXERCITADO for cid in CAPACIDADES_MACRO}
    por_cap[PAI_BOTAO] = NAO_EXERCITADO
    por_cap["(kit09-meta)"] = NAO_EXERCITADO
    por_cap.update(por_capacidade(criterios))
    # F1: a saida CONSERVA origem, sessao e lacunas. Origem declarada como
    # sintetica/fixture (ou contraditoria) nunca marca runtime_exercitado.
    proc = {}
    sessoes = set()
    marcas = set()
    lacunas = set()
    for c in criterios:
        proc[c.get("procedencia")] = proc.get(c.get("procedencia"), 0) + 1
        sessoes.update(c.get("sessoes_lidas") or [])
        marcas.update(c.get("origem_marcas") or [])
        if c.get("lacuna_probe"):
            lacunas.add(c["lacuna_probe"])
    return {
        "esquema": ESQUEMA,
        "criterios_total": len(criterios),
        "identidade": {"fonte_sha": (identidade or {}).get("fonte_sha"),
                       "dll_sha": (identidade or {}).get("dll_sha"),
                       "config_sha": (identidade or {}).get("config_sha"),
                       "sessao_esperada": (identidade or {}).get("sessao_esperada"),
                       "suficiente": RC._identidade_ok(identidade)},
        "por_mod": {MOD: contagem},
        "por_capacidade": por_cap,
        "contagem": contagem,
        "procedencias": dict(sorted(proc.items())),
        "sessoes_observadas": sorted(sessoes),
        "lacunas": sorted(lacunas),
        "origem": {"sintetica": bool(marcas), "marcas": sorted(marcas)},
        "runtime_exercitado": bool(contagem.get(OK)) and not marcas,
        "reprovado": bool(contagem.get(REPROVADO)),
        "criterios": criterios,
    }


# --------------------------------------------------------------------- CLI -----

def main(argv=None):
    ap = argparse.ArgumentParser(description="KIT-09: cenarios RSTV em criterios pequenos.")
    ap.add_argument("--observacoes", required=True,
                    help="JSON: lista de observacoes OU resultado AUT-4/CIC-5 com 'observacoes'")
    ap.add_argument("--identidade", help="JSON com fonte_sha/dll_sha[/sessao_esperada]")
    ap.add_argument("--out", help="grava o resumo (JSON) neste arquivo")
    args = ap.parse_args(argv)

    with open(args.observacoes, encoding="utf-8") as fh:
        dados = json.load(fh)
    obs, ident = RC._desempacotar(dados)
    if args.identidade:
        with open(args.identidade, encoding="utf-8") as fh:
            extra = json.load(fh)
        if isinstance(extra, dict):
            ident.update(extra)

    criterios = avaliar_cenarios(obs, ident, envelope=dados if isinstance(dados, dict) else None)
    resultado = resumir(criterios, ident)
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
