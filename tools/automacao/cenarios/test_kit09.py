#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_kit09.py - suite executavel do pacote de cenarios RSTV do KIT-09 (offline).

Reusa o arcabouco do projeto (`tools/testes/arcabouco.py`: exit 0/1/2 + linha
`RESULTADO|...`) e o avaliador CIC-3 (`rstv.py`, lido por caminho, NAO editado).

O QUE ESTE TESTE PROVA
----------------------
1. CONTRATO: `avaliar_cenarios` devolve SEMPRE o conjunto exato dos 21 criterios
   pequenos, com todos os campos do ciclo + `capacidade_pai`, `cenario_origem`,
   `esperado_origem` (esperado INDEPENDENTE, nunca "observado") e `tarefa_kit`.
2. FIXTURE NAO VIRA OK: a fixture do CIC-3 e o artefato sem leitura saem 100%
   NAO_EXERCITADO (nenhum OK), sem REPROVADO.
3. AUSENTE/MALFORMADO nunca e OK: os casos do `kit09-la.entrada.json` nao fecham OK.
4. CONTROLES NEGATIVOS: cada um dos 21 criterios tem um defeito plantado proprio que
   REPROVA (tabela `CONTROLES`, cobertura EXATA conferida por `_cobertura_exata`) —
   inclusive o mesmo defeito dentro de uma fixture (defeito continua reprovando; o
   que a fixture nao faz e APROVAR).
5. CAMINHO OK EXISTE: uma SIMULACAO POSITIVA NAO ROTULADA fecha TODOS os 21 criterios
   OK quando a identidade/hashes/sessao batem. CONTRATO NOVO (KIT-09F, achado F1 do
   KIT-09R): o artefato SINTETICO persistido (`kit09-verdade.entrada.json`) NAO fecha
   mais OK — ele se declara `sintetico=true`/`rotulo_fixture` e por isso nao qualifica
   runtime (nem na API, nem na lista, nem na CLI). A mudanca e declarada aqui em vez
   de mascarada: a versao anterior exigia exit 0 para esse artefato.
6. TESTES DISTINTOS: `handler_invocado` sem `clique_fisico` fecha o HANDLER e deixa o
   CLIQUE `NAO_EXERCITADO` (e vice-versa) — uma prova nunca substitui a outra.
7. "ATIVO" NAO PROVA AUSENCIA DE OBSTRUCAO: `ativo_na_hierarquia=true` sem o bloco
   `obstrucao` sai `NAO_EXERCITADO` com o motivo nomeando a falacia.
8. DADO VELHO REPROVA: sessao diferente da `sessao_esperada` -> REPROVADO (nao
   "INDETERMINADO generico"); sem `sessao_esperada` na identidade o criterio nao julga.
9. DEPENDENCIA REAL GOVERNA AS ARESTAS: conector ausente, aresta inventada e ausencia
   LEGITIMA (tier com Dependency 0 e 0 linhas) sao casos distintos e distinguidos.
10. ADAPTADOR: le a forma NORMALIZADA (bloco `campos`) do coletor CIC-5 REAL, inclusive
    os campos novos do contrato KIT-09, e a coleta real de fixture nunca fecha OK.
11. ROLL-UP: `por_capacidade` agrega o PIOR estado e sempre traz as 7 capacidades macro.
12. CLI real: exit code por estado (0 OK / 1 DEFEITO / 2 sem OK nem defeito).

`--contra-prova` roda a isca meta: com o `_fecha` do CIC-3 trocado por um "sempre OK"
os controles DEIXAM de reprovar — provando que o REPROVADO vem da regra.
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))

sys.path.insert(0, os.path.join(REPO, "tools", "testes"))
import arcabouco as arc  # noqa: E402  (precisa do sys.path acima)

META = {
    "nome": "kit09-rstv",
    "categoria": "pura",
    "requer": [],
    "descricao": ("KIT-09: 21 criterios pequenos rastreaveis RSTV; fixture/ausente/"
                  "malformado nunca OK; 21 controles reprovam; handler != clique; ativo "
                  "nao prova obstrucao; dado velho reprova"),
}

REQUERIDOS = ("id", "mod", "estado", "classe", "procedencia", "esperado", "observado",
              "evidencia", "motivo", "tarefa_origem")
ESTADOS = ("OK", "REPROVADO", "NAO_EXERCITADO", "INDETERMINADO")
EXTRAS_KIT = ("capacidade_pai", "cenario_origem", "esperado_origem", "tarefa_kit")

FONTE = "a" * 64
DLL = "b" * 64
SESSAO = "2026-10-05T00:00:00-sintetica"
IDENT = {"fonte_sha": FONTE, "dll_sha": DLL, "sessao_esperada": SESSAO}


# --------------------------------------------------------------------- apoio ---

def kit09():
    caminho = os.path.join(AQUI, "kit09.py")
    spec = importlib.util.spec_from_file_location("kit09_mod", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def carrega(nome):
    candidatos = [nome] if nome.endswith(".json") else [nome + ".entrada.json", nome + ".json"]
    for c in candidatos:
        caminho = os.path.join(AQUI, c)
        if os.path.isfile(caminho):
            with open(caminho, encoding="utf-8") as fh:
                return json.load(fh)
    raise arc.Falhou("fixture ausente em %s: %s" % (AQUI, candidatos))


def por_id(criterios, cid):
    alvo = [c for c in criterios if c["id"] == cid]
    arc.exigir(len(alvo) == 1, "criterio %s: esperado 1, achei %d" % (cid, len(alvo)))
    return alvo[0]


def estados(criterios):
    return {c["id"]: c["estado"] for c in criterios}


def obs_completa(**extra):
    """Observacao RUNTIME que satisfaz TODOS os criterios pequenos (base dos deltas).

    Nao e leitura de jogo: existe para exercitar as regras (o caminho OK exige
    procedencia runtime + sessao + hash da DLL == identidade).
    """
    o = {
        "procedencia": "runtime",
        "sessao": SESSAO,
        "hash_fonte": DLL,
        "janela": {"aberta": True, "fechada": True, "fechado_x": True, "fechado_esc": True},
        "personagem": {"gui_state": "ChoosingCharacter", "personagem": "Raven"},
        "personagem_esperado": "Raven",
        "skills_antes": ["Fireball", "Frostbolt"],
        "skills_depois": ["Fireball", "Frostbolt"],
        "pontos_antes": 5,
        "pontos_depois": 5,
        "texto_bruto": "Deals [2] fire damage.",
        "texto_renderizado": "Deals 12 fire damage.",
        "tooltip_pai_antes": "GUI Manager/Tooltips / Popups",
        "tooltip_pai_depois": "GUI Manager/Tooltips / Popups",
        "tooltip_indice_antes": 3,
        "tooltip_indice_depois": 3,
        "janelas_duplicadas": 0,
        "linhas_dependencia": {"T1": 2, "T5": 0},
        "dependency_por_tier": {"T1": 2, "T5": 0},
        "arestas_inventadas": 0,
        "geometria": {"caixa_na_tela_px": {"x": 10, "y": 10, "largura": 100, "altura": 50},
                      "tela": "1920x1080"},
        "handler_invocado": True,
        "clique_fisico": {"recebido": True, "alvo": "BottomBar/SkillsButton"},
        "obstrucao": {"avaliada": True, "obstruido": False, "por": ""},
        "evidencia": ["tools/automacao/cenarios/test_kit09.py"],
    }
    o.update(extra)
    return o


def _delta(**campos):
    """Observacao completa com CAMPOS SUBSTITUIDOS (controle negativo)."""
    return obs_completa(**campos)


# -------------------------------------------------------------------- assercoes --

def _schema(K, criterios):
    ids = [c["id"] for c in criterios]
    arc.igual(ids, list(K.IDS), "conjunto EXATO dos 21 criterios, na ordem de CENARIOS")
    arc.igual(len(ids), 21, "o pacote do KIT-09 tem 21 criterios pequenos")
    arc.igual(len(ids), len(set(ids)), "ids duplicados: %s" % ids)
    macro = [cid for cid, _ in K.RC.CAPACIDADES]
    arc.igual(macro, list(K.CAPACIDADES_MACRO), "7 capacidades macro do CIC-3 preservadas")
    pais = set()
    for c in criterios:
        for campo in REQUERIDOS + EXTRAS_KIT:
            arc.exigir(campo in c, "criterio %s sem o campo %r" % (c.get("id"), campo))
        arc.exigir(c["estado"] in ESTADOS, "estado invalido em %s: %r" % (c["id"], c["estado"]))
        arc.exigir(isinstance(c["evidencia"], list), "evidencia de %s nao e lista" % c["id"])
        arc.igual(c["mod"], "RoguelikeSkillTreeVisualizer", "mod do criterio %s" % c["id"])
        arc.igual(c["tarefa_kit"], "t_a4ca00f9", "criterio %s sem tarefa do KIT-09" % c["id"])
        arc.igual(c["tarefa_origem"], "t_76a41ea7", "rastreabilidade AUT-5 de %s" % c["id"])
        # esperado INDEPENDENTE: origem declarada e nunca a propria observacao julgada
        arc.exigir(isinstance(c["esperado_origem"], str) and c["esperado_origem"].strip(),
                   "%s sem 'esperado_origem'" % c["id"])
        arc.exigir("observado" not in c["esperado_origem"].lower(),
                   "%s deriva o esperado do observado: %r" % (c["id"], c["esperado_origem"]))
        pai = c["capacidade_pai"]
        arc.exigir(pai in macro or pai == K.PAI_BOTAO or pai is None,
                   "%s com pai invalido: %r" % (c["id"], pai))
        if pai is None:
            arc.igual(c["id"], "KIT09-sessao-atual",
                      "so o criterio meta pode nao ter capacidade pai: %s" % c["id"])
        arc.exigir(c["cenario_origem"], "%s sem cenario de origem" % c["id"])
        if c["estado"] != "OK":
            arc.exigir(c["prova_runtime"] is False,
                       "%s nao-OK nao pode declarar prova_runtime" % c["id"])
        pais.add(c["capacidade_pai"])
    arc.exigir(set(macro).issubset(pais), "toda capacidade macro tem criterio pequeno: %s" % pais)


def _fixture_nao_vira_ok(K, ident):
    fx = carrega("rstv-observacoes")
    criterios = K.avaliar_cenarios(fx["observacoes"], ident)
    _schema(K, criterios)
    arc.igual([c["id"] for c in criterios if c["estado"] == "OK"], [],
              "fixture do CIC-3 NAO pode fechar OK")
    arc.igual([c["id"] for c in criterios if c["estado"] == "REPROVADO"], [],
              "fixture limpa nao tem defeito, nao pode reprovar")


def _ausente(K, ident):
    fx = carrega("rstv-ausente")
    criterios = K.avaliar_cenarios(fx["observacoes"], ident)
    _schema(K, criterios)
    for c in criterios:
        arc.igual(c["estado"], "NAO_EXERCITADO",
                  "sem leitura: %s tem de ser NAO_EXERCITADO (obtido %s)"
                  % (c["id"], c["estado"]))


# Mapeamento dos casos de `kit09-la` para o criterio que NAO pode fechar OK.
# Fica aqui (e nao no JSON) porque e uma afirmacao do TESTE sobre a semantica.
LACUNAS_PROIBIDO = {
    "malformado-janela-aberta": "KIT09-RSTV21-abre",
    "malformado-janela-fechado-x": "KIT09-RSTV21-fecha-x",
    "malformado-pontos-string": "KIT09-RSTV6-pontos-sem-mutacao",
    "malformado-geometria-nao-finita": "KIT09-RSTV-geo-medida",
    "malformado-duplicata-null": "KIT09-RSTV21-sem-duplicata",
    "malformado-arestas-texto": "KIT09-RSTV25b-arestas",
    "malformado-handler-texto": "KIT09-RSTV5-handler",
    "malformado-clique-booleano-faltando": "KIT09-RSTV5-clique-fisico",
    "malformado-obstrucao-texto": "KIT09-RSTV5-sem-obstrucao",
    "personagem-sem-alvo-declarado": "KIT09-RSTV6-personagem",
}
# Casos que NAO recebem a base de identidade (leitura realmente ausente).
LACUNAS_SEM_BASE = ("ausente-sem-leitura",)


def _lacunas(K, ident):
    """Ausencia/incompletude/malformado/rotulo-fixture NUNCA viram OK.

    O criterio META `KIT09-sessao-atual` e julgado pela IDENTIDADE (sessao_esperada),
    nao pelos campos do probe: com a base de identidade valida ele fecha OK por
    desenho — os controles dele vivem em `CONTROLES`/`_dado_velho`. Todos os outros
    criterios do caso tem de ficar fora do OK, e o criterio alvo do caso tem de sair
    do OK declarando o defeito de forma/ausencia.
    """
    fx = carrega("kit09-la")
    base = fx.get("base") or {}
    for caso in fx["casos"]:
        nome = caso["nome"]
        obs = {} if nome in LACUNAS_SEM_BASE else dict(base)
        obs.update(caso["observacao"] or {})
        if caso.get("procedencia_do_caso"):
            obs["procedencia"] = caso["procedencia_do_caso"]
        criterios = K.avaliar_cenarios([obs], ident)
        _schema(K, criterios)
        ok = [c["id"] for c in criterios
              if c["estado"] == "OK" and c["id"] != "KIT09-sessao-atual"]
        arc.igual(ok, [], "caso %r nao pode fechar OK: %s" % (nome, ok))
        proibido = LACUNAS_PROIBIDO.get(nome)
        if proibido:
            c = por_id(criterios, proibido)
            arc.exigir(c["estado"] != "OK",
                       "caso %r: %s tem de sair do OK (obtido %s)"
                       % (nome, proibido, c["estado"]))


# tabela de CONTROLES negativos: (nome, delta, criterio que TEM de reprovar)
# F7 do KIT-09R: o conjunto dos IDs cobertos tem de ser EXATAMENTE os 21 criterios.
# `_cobertura_exata` confere essa igualdade (o defeito de render-observado faltava).
CONTROLES = (
    ("abre-falso", {"janela": {"aberta": False, "fechada": True, "fechado_x": True,
                               "fechado_esc": True}}, "KIT09-RSTV21-abre"),
    ("fecha-falsa", {"janela": {"aberta": True, "fechada": False, "fechado_x": True,
                                "fechado_esc": True}}, "KIT09-RSTV21-fecha"),
    ("fecha-x-falso", {"janela": {"aberta": True, "fechada": True, "fechado_x": False,
                                  "fechado_esc": True}}, "KIT09-RSTV21-fecha-x"),
    ("fecha-esc-falso", {"janela": {"aberta": True, "fechada": True, "fechado_x": True,
                                    "fechado_esc": False}}, "KIT09-RSTV21-fecha-esc"),
    ("personagem-errado", {"personagem": {"personagem": "Outro"}}, "KIT09-RSTV6-personagem"),
    ("skills-mudaram", {"skills_depois": ["Fireball"]},
     "KIT09-RSTV6-skills-sem-mutacao"),
    ("pontos-gastos", {"pontos_depois": 3}, "KIT09-RSTV6-pontos-sem-mutacao"),
    ("render-nao-aconteceu", {"texto_bruto": "Deals [2] fire damage.",
                              "texto_renderizado": "Deals [2] fire damage."},
     "KIT09-RSTV26-render-observado"),
    ("placeholder-no-render", {"texto_renderizado": "Deals *0 fire damage."},
     "KIT09-RSTV26-sem-placeholder"),
    ("tooltip-pai-nao-restaurado", {"tooltip_pai_depois": "outro pai"},
     "KIT09-RSTV21-tooltip-pai"),
    ("tooltip-indice-nao-restaurado", {"tooltip_indice_depois": 1},
     "KIT09-RSTV21-tooltip-indice"),
    ("janela-duplicada", {"janelas_duplicadas": 2}, "KIT09-RSTV21-sem-duplicata"),
    ("conector-ausente", {"linhas_dependencia": {"T1": 1, "T5": 0}},
     "KIT09-RSTV25b-arestas"),
    ("aresta-inventada", {"dependency_por_tier": {"T1": 0, "T5": 0}},
     "KIT09-RSTV25b-sem-aresta-inventada"),
    ("ausencia-legitima-violada", {"linhas_dependencia": {"T1": 2, "T5": 1},
                                   "dependency_por_tier": {"T1": 2, "T5": 0}},
     "KIT09-RSTV25b-ausencia-legitima"),
    ("geo-dimensao-zero", {"geometria": {"caixa_na_tela_px": {"x": 10, "y": 10, "largura": 0,
                                                              "altura": 50},
                                         "tela": "1920x1080"}},
     "KIT09-RSTV-geo-medida"),
    ("geo-clipping", {"geometria": {"caixa_na_tela_px": {"x": 1900, "y": 10, "largura": 100,
                                                         "altura": 50},
                                    "tela": "1920x1080"}},
     "KIT09-RSTV-geo-clipping"),
    ("handler-nao-invocado", {"handler_invocado": False}, "KIT09-RSTV5-handler"),
    ("clique-nao-recebido", {"clique_fisico": {"recebido": False, "alvo": "BottomBar/SkillsButton"}},
     "KIT09-RSTV5-clique-fisico"),
    ("botao-obstruido", {"obstrucao": {"avaliada": True, "obstruido": True,
                                       "por": "Overlay/Modal"}},
     "KIT09-RSTV5-sem-obstrucao"),
    ("dado-velho", {"sessao": "2026-09-01T00:00:00"}, "KIT09-sessao-atual"),
    # controles ADVERSARIAIS (mesmo criterio de outra linha; nao entram na cobertura
    # exata dos 21, entram na refutacao dos achados F1/F5)
    ("clique-alvo-errado", {"clique_fisico": {"recebido": True, "alvo": "MainMenu/QuitButton"}},
     "KIT09-RSTV5-clique-fisico"),
    ("fixture-com-defeito", {"procedencia": "fixture", "personagem": {"personagem": "Outro"}},
     "KIT09-RSTV6-personagem"),
    ("sintetico-com-defeito", {"sintetico": True, "personagem": {"personagem": "Outro"}},
     "KIT09-RSTV6-personagem"),
)


# F7: AUSENCIA por criterio — remover a leitura NAO pode virar OK (nem prova_runtime).
AUSENCIA = (
    ("KIT09-RSTV21-abre", {"janela": None}),
    ("KIT09-RSTV21-fecha", {"janela": None}),
    ("KIT09-RSTV21-fecha-x", {"janela": None}),
    ("KIT09-RSTV21-fecha-esc", {"janela": None}),
    ("KIT09-RSTV6-personagem", {"personagem": None, "personagem_esperado": None}),
    ("KIT09-RSTV6-skills-sem-mutacao", {"skills_antes": None, "skills_depois": None}),
    ("KIT09-RSTV6-pontos-sem-mutacao", {"pontos_antes": None, "pontos_depois": None}),
    ("KIT09-RSTV26-render-observado", {"texto_renderizado": None}),
    ("KIT09-RSTV26-sem-placeholder", {"texto_bruto": None, "texto_renderizado": None}),
    ("KIT09-RSTV21-tooltip-pai", {"tooltip_pai_antes": None, "tooltip_pai_depois": None}),
    ("KIT09-RSTV21-tooltip-indice", {"tooltip_indice_antes": None,
                                     "tooltip_indice_depois": None}),
    ("KIT09-RSTV21-sem-duplicata", {"janelas_duplicadas": None}),
    ("KIT09-RSTV25b-arestas", {"linhas_dependencia": None, "dependency_por_tier": None}),
    ("KIT09-RSTV25b-sem-aresta-inventada",
     {"arestas_inventadas": None, "linhas_dependencia": None, "dependency_por_tier": None}),
    ("KIT09-RSTV25b-ausencia-legitima", {"dependency_por_tier": None}),
    ("KIT09-RSTV-geo-medida", {"geometria": None}),
    ("KIT09-RSTV-geo-clipping", {"geometria": None}),
    ("KIT09-RSTV5-handler", {"handler_invocado": None}),
    ("KIT09-RSTV5-clique-fisico", {"clique_fisico": None}),
    ("KIT09-RSTV5-sem-obstrucao", {"obstrucao": None, "ativo_na_hierarquia": None}),
    ("KIT09-sessao-atual", {"sessao": None}),
)


def _controles(K, ident):
    for nome, delta, cid in CONTROLES:
        c = por_id(K.avaliar_cenarios([_delta(**delta)], ident), cid)
        arc.igual(c["estado"], "REPROVADO",
                  "controle %r tem de REPROVAR %s (obtido %s: %s)"
                  % (nome, cid, c["estado"], c["motivo"]))
        arc.exigir(c["motivo"].startswith("DEFEITO"),
                   "controle %r: o motivo tem de nomear o DEFEITO: %r" % (nome, c["motivo"]))


def _cobertura_exata(K, ident):
    """F7: cobertura EXATA dos 21 criterios — por DEFEITO (CONTROLES) e por AUSENCIA.

    A cobertura tem de ser o conjunto EXATO dos 21 IDs: nem falta (o achado F7 era a
    ausencia do controle de render-observado) nem sobra um ID inexistente.
    """
    ids_defeito = {cid for _, _, cid in CONTROLES}
    ids_ausencia = {cid for cid, _ in AUSENCIA}
    arc.igual(sorted(ids_defeito), sorted(K.IDS),
              "CONTROLES tem de cobrir EXATAMENTE os 21 criterios (faltando %s; sobrando %s)"
              % (sorted(set(K.IDS) - ids_defeito), sorted(ids_defeito - set(K.IDS))))
    arc.igual(sorted(ids_ausencia), sorted(K.IDS),
              "AUSENCIA tem de cobrir EXATAMENTE os 21 criterios (faltando %s; sobrando %s)"
              % (sorted(set(K.IDS) - ids_ausencia), sorted(ids_ausencia - set(K.IDS))))
    for cid, delta in AUSENCIA:
        c = por_id(K.avaliar_cenarios([_delta(**delta)], ident), cid)
        arc.exigir(c["estado"] != "OK",
                   "ausencia %s: sem a leitura o criterio NAO pode fechar OK (obtido %s: %s)"
                   % (cid, c["estado"], c["motivo"]))
        arc.igual(c["prova_runtime"], False,
                  "ausencia %s: ausencia de leitura nao pode declarar prova_runtime" % cid)


def _sintetico_nao_qualifica(K, ident):
    """F1: origem DECLARADA sintetica/fixture nunca qualifica runtime — em envelope,
    em lista (rotulos propagados pelo desempacotador) e na observacao. O DEFEITO
    observado numa entrada sintetica continua REPROVANDO (nao se suprime defeito).
    """
    fx = carrega("kit09-verdade")
    crit = K.avaliar_cenarios(list(fx["observacoes"]), ident, envelope=fx)
    _schema(K, crit)
    arc.igual([c["id"] for c in crit if c["estado"] == "OK"], [],
              "envelope sintetico/rotulo_fixture nao pode fechar OK")
    r = K.resumir(crit, ident)
    arc.igual(r["runtime_exercitado"], False,
              "artefato SINTETICO declarado nao pode marcar runtime_exercitado")
    arc.igual(r["origem"]["sintetica"], True, "a saida tem de conservar a ORIGEM sintetica")

    obs, _ = K.RC._desempacotar(fx)
    arc.exigir(any(o.get("rotulo_fixture") for o in obs),
               "o desempacotador nao propagou o rotulo_fixture para as observacoes")
    crit = K.avaliar_cenarios(obs, ident)
    arc.igual([c["id"] for c in crit if c["estado"] == "OK"], [],
              "lista rotulada como fixture nao pode fechar OK")

    c = por_id(K.avaliar_cenarios([obs_completa(sintetico=True)], ident),
               "KIT09-RSTV6-personagem")
    arc.exigir(c["estado"] != "OK",
               "observacao sintetica nao qualifica runtime (obtido %s: %s)"
               % (c["estado"], c["motivo"]))
    arc.igual(c["prova_runtime"], False, "observacao sintetica nao declara prova_runtime")

    c = por_id(K.avaliar_cenarios([obs_completa(sintetico=True,
                                                personagem={"personagem": "Outro"})], ident),
               "KIT09-RSTV6-personagem")
    arc.igual(c["estado"], "REPROVADO",
              "defeito observado em entrada sintetica continua REPROVADO (obtido %s)"
              % c["estado"])


def _normalizado_defeito_reprova(K, ident):
    """F2/F4: o bloco `campos` NORMALIZADO REAL do coletor e lido; defeito medido
    REPROVA e malformado/nao-finito nao vira OK nem no formato normalizado.
    """
    caminho_col = os.path.join(REPO, "tools", "automacao", "runtime", "coletor.py")
    spec = importlib.util.spec_from_file_location("cic5_norm_kit09", caminho_col)
    col = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(col)

    def norm(o):
        return col.normalizar_observacao(o, "runtime", alvos=[])

    for nome, delta, cid in (
            ("parent-defeito", {"tooltip_pai_depois": "outro pai"}, "KIT09-RSTV21-tooltip-pai"),
            ("index-defeito", {"tooltip_indice_depois": 1}, "KIT09-RSTV21-tooltip-indice"),
            ("duplicata-defeito", {"janelas_duplicadas": 2}, "KIT09-RSTV21-sem-duplicata")):
        c = por_id(K.avaliar_cenarios([norm(obs_completa(**delta))], ident), cid)
        arc.igual(c["estado"], "REPROVADO",
                  "normalizado %r: o defeito medido tem de REPROVAR %s (obtido %s: %s)"
                  % (nome, cid, c["estado"], c["motivo"]))
    base = norm(obs_completa())
    for cid in ("KIT09-RSTV21-tooltip-pai", "KIT09-RSTV21-tooltip-indice",
                "KIT09-RSTV21-sem-duplicata"):
        arc.igual(por_id(K.avaliar_cenarios([base], ident), cid)["estado"], "OK",
                  "normalizado positivo tem de fechar OK: %s" % cid)
    mal = norm(obs_completa(tooltip_pai_antes=[], tooltip_pai_depois=[]))
    c = por_id(K.avaliar_cenarios([mal], ident), "KIT09-RSTV21-tooltip-pai")
    arc.exigir(c["estado"] != "OK",
               "normalizado com leitura malformada nao pode fechar OK (obtido %s)" % c["estado"])
    inf = norm(obs_completa(pontos_antes=float("inf"), pontos_depois=float("inf")))
    c = por_id(K.avaliar_cenarios([inf], ident), "KIT09-RSTV6-pontos-sem-mutacao")
    arc.exigir(c["estado"] != "OK",
               "normalizado com pontos NAO FINITOS nao pode fechar OK (obtido %s)" % c["estado"])


def _caminho_ok(K, ident):
    # SIMULACAO POSITIVA NAO ROTULADA: exercita as regras no caminho OK. O artefato
    # SINTETICO persistido (`kit09-verdade.entrada.json`) NAO pode fechar OK — ele se
    # declara sintetico/rotulo_fixture (F1) e tem controle proprio em
    # `_sintetico_nao_qualifica`.
    crit = K.avaliar_cenarios([obs_completa()], ident)
    _schema(K, crit)
    for c in crit:
        arc.igual(c["estado"], "OK", "%s deveria fechar OK: %s" % (c["id"], c["motivo"]))
        arc.igual(c["prova_runtime"], True, "%s OK tem de declarar prova_runtime" % c["id"])
        arc.igual(c["sessao"], SESSAO, "%s OK tem de propagar a sessao" % c["id"])
    arc.igual(K.resumir(crit, ident)["runtime_exercitado"], True,
              "o resumo com tudo OK marca runtime_exercitado")


def _handler_x_clique(K, ident):
    # (a) handler exercitado, clique fisico NAO medido
    o = obs_completa()
    o.pop("clique_fisico")
    crit = K.avaliar_cenarios([o], ident)
    arc.igual(por_id(crit, "KIT09-RSTV5-handler")["estado"], "OK",
              "handler invocado fecha o criterio do HANDLER")
    cs = por_id(crit, "KIT09-RSTV5-clique-fisico")
    arc.igual(cs["estado"], "NAO_EXERCITADO",
              "sem 'clique_fisico' o criterio do CLIQUE nao pode fechar (nem reprovar): %s"
              % cs["motivo"])
    arc.exigir("clique FISICO e teste DISTINTO" in (cs["lacuna_probe"] or "")
               or "clique_fisico" in (cs["lacuna_probe"] or ""),
               "a lacuna do clique tem de declarar o contrato: %r" % cs["lacuna_probe"])
    # (b) clique fisico medido, handler NAO medido
    o2 = obs_completa()
    o2.pop("handler_invocado")
    crit2 = K.avaliar_cenarios([o2], ident)
    arc.igual(por_id(crit2, "KIT09-RSTV5-clique-fisico")["estado"], "OK",
              "clique fisico recebido no alvo fecha o criterio do CLIQUE")
    arc.igual(por_id(crit2, "KIT09-RSTV5-handler")["estado"], "NAO_EXERCITADO",
              "sem 'handler_invocado' o criterio do HANDLER nao pode fechar")


def _ativo_nao_prova_obstrucao(K, ident):
    o = obs_completa()
    o.pop("obstrucao")
    o["ativo_na_hierarquia"] = True
    c = por_id(K.avaliar_cenarios([o], ident), "KIT09-RSTV5-sem-obstrucao")
    arc.igual(c["estado"], "NAO_EXERCITADO",
              "'ativo' sem 'obstrucao' nao pode fechar (obtido %s)" % c["estado"])
    arc.exigir("NAO prova" in c["motivo"],
               "o motivo tem de nomear a falacia de 'ativo': %r" % c["motivo"])
    # controle: 'ativo' false nao vira alvo do criterio (objeto oculto nao mede)
    o2 = obs_completa()
    o2["ativo_na_hierarquia"] = False
    c2 = por_id(K.avaliar_cenarios([o2], ident), "KIT09-RSTV5-sem-obstrucao")
    arc.igual(c2["estado"], "NAO_EXERCITADO",
              "objeto inativo nao mede obstrucao: %s" % c2["motivo"])


def _dado_velho(K):
    # sessao_esperada divergente -> REPROVADO (dado velho), nas 21 criterios que a veem
    ident = dict(IDENT, sessao_esperada="2099-01-01T00:00:00")
    crit = K.avaliar_cenarios([obs_completa()], ident)
    c = por_id(crit, "KIT09-sessao-atual")
    arc.igual(c["estado"], "REPROVADO", "sessao != sessao esperada tem de REPROVAR")
    arc.exigir("DADO VELHO" in c["motivo"], "o motivo tem de nomear DADO VELHO: %r" % c["motivo"])
    # F6: a rodada VELHA nao qualifica NENHUMA capacidade/criterio — nao so o meta.
    qualificados = [x["id"] for x in crit if x["estado"] == "OK" or x["prova_runtime"]]
    arc.igual(qualificados, [],
              "sessao velha nao pode qualificar criterio algum (obtido %s)" % qualificados)
    arc.igual(K.resumir(crit, ident)["runtime_exercitado"], False,
              "dado de outra sessao nao marca runtime_exercitado")
    # ... mas o DEFEITO observavel da rodada velha continua apontado (nao se suprime)
    c2 = por_id(K.avaliar_cenarios([_delta(sessao="2099-01-01T00:00:00",
                                           personagem={"personagem": "Outro"})], ident),
                "KIT09-RSTV6-personagem")
    arc.igual(c2["estado"], "REPROVADO",
              "defeito observavel nao pode ser suprimido pelo dado velho (obtido %s)" % c2["estado"])
    # sem sessao_esperada na identidade o criterio NAO julga
    c = por_id(K.avaliar_cenarios([obs_completa()],
                                  {"fonte_sha": FONTE, "dll_sha": DLL}), "KIT09-sessao-atual")
    arc.igual(c["estado"], "NAO_EXERCITADO",
              "sem 'sessao_esperada' nao ha como julgar dado velho")


def _dependencia(K, ident):
    # ausencia LEGITIMA (T5 com Dependency 0 e 0 linhas) NAO vira conector nem defeito
    crit = K.avaliar_cenarios([obs_completa()], ident)
    for cid in ("KIT09-RSTV25b-arestas", "KIT09-RSTV25b-sem-aresta-inventada",
                "KIT09-RSTV25b-ausencia-legitima"):
        arc.igual(por_id(crit, cid)["estado"], "OK",
                  "ausencia legitima (T5 sem Dependency) nao inventa aresta: %s" % cid)
    # conector ausente e aresta inventada sao DEFEITOS distintos
    c1 = por_id(K.avaliar_cenarios([_delta(linhas_dependencia={"T1": 1, "T5": 0})], ident),
                "KIT09-RSTV25b-arestas")
    arc.exigir("conector AUSENTE" in c1["motivo"], "conector ausente nomeado: %r" % c1["motivo"])
    c2 = por_id(K.avaliar_cenarios([_delta(dependency_por_tier={"T1": 0, "T5": 0})], ident),
                "KIT09-RSTV25b-sem-aresta-inventada")
    arc.exigir("INVENTADA" in c2["motivo"], "aresta inventada nomeada: %r" % c2["motivo"])


def _rollup(K, ident):
    crit = K.avaliar_cenarios([_delta(personagem={"personagem": "Outro"})], ident)
    cap = K.por_capacidade(crit)
    arc.igual(cap["RSTV-6-readonly-personagem"], "REPROVADO",
              "roll-up: defeito de personagem sobe para a capacidade macro")
    arc.igual(cap["RSTV-26-placeholders"], "OK",
              "roll-up: capacidade sem defeito continua OK (defeito nao contamina)")
    r = K.resumir(crit, ident)
    for cid, _ in K.RC.CAPACIDADES:
        arc.exigir(cid in r["por_capacidade"], "resumo sem a capacidade %s" % cid)
    arc.igual(r["reprovado"], True, "resumo marca reprovado")


def _adaptador_coletor(K, ident):
    """Costura REAL probe -> coletor CIC-5 -> kit09 (offline, sem jogo)."""
    caminho_col = os.path.join(REPO, "tools", "automacao", "runtime", "coletor.py")
    arc.exigir(os.path.isfile(caminho_col), "coletor CIC-5 ausente: %s" % caminho_col)
    spec = importlib.util.spec_from_file_location("cic5_coletor_kit09", caminho_col)
    col = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(col)

    fx_path = os.path.join(REPO, "tools", "automacao", "runtime", "fixtures",
                           "probe-saida-exemplo.entrada.json")
    plano = os.path.join(REPO, "tools", "automacao", "runtime", "fixtures",
                         "plano-exemplo.entrada.json")
    with open(fx_path, encoding="utf-8") as fh:
        fx = json.load(fh)

    # (1) a fixture real do probe passa pelo coletor de verdade: nao vira runtime
    res, codigo = col.consolidar_probe(fx_path, plano)
    arc.igual(res["status"], "FIXTURE", "coletor CIC-5: fixture rotulada sai FIXTURE")
    arc.igual(codigo, 2, "coletor CIC-5: fixture -> exit 2")

    # (2) a forma NORMALIZADA real (bloco `campos`) e lida pelos criterios pequenos
    ctx = {"sessao": fx["sessao"], "hash_fonte": fx["hash_fonte"]}
    norm = [col.normalizar_observacao(o, "fixture", rotulo_fixture="probe-saida-exemplo")
            for o in col.anexar_contexto(fx["observacoes"], ctx)]
    arc.exigir(all("campos" in n for n in norm),
               "coletor: observacao normalizada sem o bloco 'campos'")
    crit = K.avaliar_cenarios(norm, ident)
    _schema(K, crit)
    arc.igual([c["id"] for c in crit if c["estado"] == "OK"], [],
              "formato REAL do coletor (fixture) nao pode fechar OK")

    # (3) os CAMPOS NOVOS do contrato KIT-09 tambem sao lidos no bloco `campos`
    novo = {"procedencia": "fixture",
            "campos": {
                "janela": {"estado": "PRESENTE", "valor": {"aberta": True, "fechada": True,
                                                           "fechado_x": True,
                                                           "fechado_esc": True}},
                "handler_invocado": {"estado": "PRESENTE", "valor": True},
                "clique_fisico": {"estado": "PRESENTE",
                                  "valor": {"recebido": True, "alvo": "BottomBar/SkillsButton"}},
                "obstrucao": {"estado": "PRESENTE",
                              "valor": {"avaliada": True, "obstruido": False, "por": ""}}}}
    crit = K.avaliar_cenarios([novo], ident)
    for cid in ("KIT09-RSTV21-abre", "KIT09-RSTV21-fecha-x", "KIT09-RSTV21-fecha-esc",
                "KIT09-RSTV5-handler", "KIT09-RSTV5-clique-fisico",
                "KIT09-RSTV5-sem-obstrucao"):
        c = por_id(crit, cid)
        arc.igual(c["estado"], "NAO_EXERCITADO",
                  "campo novo no bloco 'campos': %s tem de ser lido e ficar NAO_EXERCITADO "
                  "(fixture) — obtido %s (%s)" % (cid, c["estado"], c["motivo"]))
        arc.exigir(not c["motivo"].startswith("campo AUSENTE"),
                   "%s nao leu o campo normalizado: %r" % (cid, c["motivo"]))


def _cli():
    """Exercita a CLI REAL: exit 0 (tudo OK), 1 (defeito), 2 (sem OK nem defeito).

    F1: o artefato SINTETICO persistido NAO qualifica runtime — sai exit 2 com zero
    OK. O caminho exit 0 e exercitado por uma simulacao NAO ROTULADA escrita pelo
    proprio teste num diretorio temporario (nenhum arquivo do repo "se declara
    runtime real").
    """
    py = sys.executable
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    base = [py, os.path.join(AQUI, "kit09.py")]
    ident = os.path.join(AQUI, "kit09-identidade.json")

    def roda(obs_path):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "res.json")
            proc = subprocess.run(base + ["--observacoes", obs_path, "--identidade", ident,
                                          "--out", out],
                                  capture_output=True, text=True, encoding="utf-8", env=env)
            dados = json.load(open(out, encoding="utf-8")) if os.path.isfile(out) else {}
            return proc.returncode, dados

    # (1) SIMULACAO POSITIVA NAO ROTULADA -> exit 0
    with tempfile.TemporaryDirectory() as tmp:
        caminho = os.path.join(tmp, "simulada.entrada.json")
        with open(caminho, "w", encoding="utf-8", newline="\n") as fh:
            json.dump({"observacoes": [obs_completa()]}, fh, ensure_ascii=False)
        cod, res = roda(caminho)
    arc.igual(cod, 0, "CLI com simulacao NAO ROTULADA -> exit 0 (obtido %s)" % cod)
    arc.igual(res["contagem"].get("OK"), 21, "CLI: os 21 criterios OK")
    arc.igual(res["runtime_exercitado"], True, "CLI: runtime_exercitado na simulacao nao rotulada")

    # (2) ARTEFATO SINTETICO DECLARADO -> exit 2 (nenhum OK, nenhum defeito)
    cod, res = roda(os.path.join(AQUI, "kit09-verdade.entrada.json"))
    arc.igual(cod, 2, "CLI do artefato SINTETICO declarado -> exit 2 (obtido %s)" % cod)
    arc.igual(res["contagem"].get("OK"), None, "CLI: artefato sintetico nao pode fechar OK")
    arc.igual(res["runtime_exercitado"], False,
              "CLI: sintetico=true/rotulo_fixture NAO marca runtime_exercitado")
    arc.igual(res["origem"]["sintetica"], True, "CLI: a saida conserva a ORIGEM sintetica")
    arc.igual(res["reprovado"], False, "CLI: sintetico sem defeito nao reprova")

    # (3) DADO VELHO -> exit 1
    cod, res = roda(os.path.join(AQUI, "kit09-velho.entrada.json"))
    arc.igual(cod, 1, "CLI com DADO VELHO -> exit 1 (reprovado)")
    arc.igual(res["reprovado"], True, "resumo do CLI marca reprovado")

    # (4) MALFORMADO/AUSENTE -> exit 2
    cod, res = roda(os.path.join(AQUI, "kit09-la.entrada.json"))
    arc.igual(cod, 2, "CLI com malformado/ausente (sem OK, sem defeito) -> exit 2")
    arc.igual(res["contagem"].get("OK"), None, "CLI: malformado/ausente nunca OK")


# ---------------------------------------------------------------------- suite --

def corpo():
    K = kit09()
    ident = IDENT
    _fixture_nao_vira_ok(K, ident)
    _ausente(K, ident)
    _lacunas(K, ident)
    _controles(K, ident)
    _cobertura_exata(K, ident)
    _sintetico_nao_qualifica(K, ident)
    _normalizado_defeito_reprova(K, ident)
    _caminho_ok(K, ident)
    _handler_x_clique(K, ident)
    _ativo_nao_prova_obstrucao(K, ident)
    _dado_velho(K)
    _dependencia(K, ident)
    _rollup(K, ident)
    _adaptador_coletor(K, ident)
    _cli()


# ---------------------------------------------------------------- contra-prova -

def contra_prova():
    """Isca meta: um `_fecha` 'sempre OK' NAO pega os controles do KIT-09.

    Prova que o REPROVADO dos 21 controles vem da regra de avaliacao, nao de um passe
    livre. Reprovacao de verdade exige defeito detectado.
    """
    K = kit09()
    ident = IDENT
    falhas = []
    original = K.RC._fecha
    try:
        K.RC._fecha = lambda *a, **k: (K.OK, "runtime", "isca: sempre OK")
        for nome, delta, cid in CONTROLES:
            c = por_id(K.avaliar_cenarios([_delta(**delta)], ident), cid)
            if c["estado"] == "REPROVADO":
                falhas.append("isca 'sempre OK' ainda reprovou %s (%s)" % (nome, cid))
    finally:
        K.RC._fecha = original
    if not falhas:
        print("CONTRA-PROVA|PASSOU|isca 'sempre OK' deixou os %d controles passarem "
              "(o REPROVADO real vem da regra)" % len(CONTROLES))
    for f in falhas:
        print("CONTRA-PROVA|REPROVOU|%s" % f)
    return 1 if falhas else 0


def main():
    ap = argparse.ArgumentParser(description="KIT-09 teste do pacote de cenarios RSTV.")
    ap.add_argument("--contra-prova", action="store_true",
                    help="roda so a isca meta (avaliador 'sempre OK' nao pode pegar os controles)")
    args, _ = ap.parse_known_args()
    if args.contra_prova:
        return contra_prova()
    return arc.roda(META, corpo)


if __name__ == "__main__":
    sys.exit(main())
