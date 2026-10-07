#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_rstv.py - teste executavel do avaliador RSTV (CIC-3), offline.

Reusa o arcabouco do projeto (`tools/testes/arcabouco.py`, exit 0/1/2 + linha
`RESULTADO|...`) e as fixtures ROTULADAS deste diretorio. Nada aqui abre o jogo,
builda, instala probe ou toca no produto.

O QUE ESTE TESTE PROVA
----------------------
1. Contrato: `avaliar` devolve criterios com TODOS os campos exigidos, so com
   estados validos, e sempre o conjunto canonico EXATO das 7 capacidades — mesmo
   quando dado malformado derruba uma capacidade (B3).
2. FIXTURE NAO VIRA OK: a fixture limpa sai 100% NAO_EXERCITADO (nenhum OK) e
   sem REPROVADO.
3. AUSENTE nao e OK: o caso sem leitura sai todo NAO_EXERCITADO, com lacuna
   tecnica declarada (`lacuna_probe` + `tipo_pendencia=tecnica`).
4. LACUNAS (B1/B2): com procedencia runtime + identidade SUFICIENTE, campo
   ausente/incompleto/malformado NAO fecha OK — vira NAO_EXERCITADO/INDETERMINADO
   e pendencia TECNICA (nao autorizacao por default).
5. CONTROLES NEGATIVOS: cada caso plantado (gasto de skills/pontos, personagem
   errado, placeholder '*0'/indice, tooltip nao restaurado, janela duplicada,
   janela que nao fecha, clipping, aresta de dependencia inventada) REPROVA.
6. O caminho OK EXISTE, exercitado por um ARTEFATO SINTETICO persistido
   (`rstv-positivo.entrada.json`, rotulado como sintetico): o teste injeta
   procedencia runtime + sessao e usa os hashes declarados como identidade.
7. CADEIA (B4): sem identidade nunca ha OK; hash divergente (fonte/dll) ->
   INDETERMINADO; hash nao confirmado (config) -> NAO_EXERCITADO; e o criterio
   PROPAGA fonte_sha/dll_sha/config_sha + prova_runtime + sessao.
8. Adaptador le as DUAS formas do AUT-4/CIC-5: campos planos do probe e bloco
   `campos` normalizado; `[N]` no texto CRU e template legitimo e so reprova
   no RENDERIZADO.
9. CLI real: exit code por estado (2 fixture, 1 defeito).
10. INTEGRACAO COM O COLETOR CIC-5 REAL: a fixture real do probe passa pelo
    `coletor` de verdade (procedencia auto-detectada -> FIXTURE), a forma
    NORMALIZADA que ele produz e lida por `avaliar` (bloco `campos`, fallback
    NAO_APLICAVEL) e o campo `hash_fonte` do coletor (sha256 da **DLL**) casa com
    `dll_sha` da identidade — NAO com `fonte_sha` (R-1 do CIC-5R). Tudo rotulado;
    nao prova runtime.
11. F1-F7 (parecer CIC-3R): cada defeito que ANTES fechava verde (dimensao nunca
    lida, contagem null/invalida, truthiness no confronto de dependencia,
    geometria nao finita, alias de hash contraditorio, render nao observado,
    sessoes misturadas) sai do OK com o motivo NOMEANDO o defeito; removido o
    defeito, o mesmo criterio volta a OK. A tabela de casos e reusada pela prova
    RED contra o `rstv.py` anterior (`prova_red_f1f7.py`).
12. L2 (parecer CIC-3R2): `arestas_inventadas` deriva o TIPO esperado (contagem
    finita >= 0); a forma MALFORMADA (`"2"` string-de-numero, vazio, lista,
    dict, negativo, `"NaN"`) NAO fecha OK — vira leitura malformada declarada
    (NAO_EXERCITADO + pendencia tecnica); o inteiro/float valido, o booleano e a
    chave ausente seguem fechando OK, e a contagem valida > 0 continua REPROVADO.

`--contra-prova` roda a isca meta: com o `_fecha` trocado por um "sempre OK" os
controles DEIXAM de reprovar — provando que o REPROVADO vem da regra, nao do
acaso.
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))                    # .../cenarios
REPO = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))       # raiz do repo

sys.path.insert(0, os.path.join(REPO, "tools", "testes"))
import arcabouco as arc  # noqa: E402  (precisa do sys.path acima)

META = {
    "nome": "cic3-rstv",
    "categoria": "pura",
    "requer": [],
    "descricao": "avaliador RSTV: fixture nao vira OK, lacunas nao viram OK, controles reprovam, runtime identifica",
}

REQUERIDOS = ("id", "mod", "estado", "classe", "procedencia", "esperado",
              "observado", "evidencia", "motivo", "tarefa_origem")
ESTADOS = ("OK", "REPROVADO", "NAO_EXERCITADO", "INDETERMINADO")
TIPOS_PENDENCIA = (None, "tecnica", "autorizacao")


# --------------------------------------------------------------------- apoio ---

def rstv():
    """Importa `rstv.py` como modulo (sem depender do cwd)."""
    caminho = os.path.join(AQUI, "rstv.py")
    spec = importlib.util.spec_from_file_location("cic3_rstv", caminho)
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


def identidade():
    i = carrega("rstv-identidade")
    return {"fonte_sha": i["fonte_sha"], "dll_sha": i["dll_sha"]}


def runtime_ctx(ident, **extra):
    """Observacao runtime minima com identidade suficiente (a lacuna vem do resto).

    O campo `hash_fonte` do coletor CIC-5 e o sha256 da **DLL** do probe (ver
    `coletor.derivar_config`/`provar_atualidade` e CIC-5-entrega: "a identidade do
    probe (`hash_fonte`) casa com `dll_sha`"). Por isso ele e confrontado com
    `dll_sha` da identidade — nao com `fonte_sha` (achado R-1 do CIC-5R).
    """
    base = {"procedencia": "runtime", "sessao": "2026-10-05T00:00:00",
            "hash_fonte": ident["dll_sha"]}
    base.update(extra)
    return base


def por_id(criterios, cid):
    alvo = [c for c in criterios if c["id"] == cid]
    arc.exigir(len(alvo) == 1, "criterio %s: esperado 1, achei %d" % (cid, len(alvo)))
    return alvo[0]


# -------------------------------------------------------------------- assercoes -

def _schema(R, criterios):
    ids = [c["id"] for c in criterios]
    canonico = [cid for cid, _ in R.CAPACIDADES]
    arc.igual(ids, canonico, "conjunto canonico EXATO (ordem e tamanho) sempre presente")
    arc.igual(len(ids), len(set(ids)), "ids de criterio duplicados: %s" % ids)
    for c in criterios:
        for campo in REQUERIDOS:
            arc.exigir(campo in c, "criterio %s sem o campo %r" % (c.get("id"), campo))
        arc.exigir(c["estado"] in ESTADOS, "estado invalido em %s: %r" % (c["id"], c["estado"]))
        arc.exigir(isinstance(c["evidencia"], list), "evidencia de %s nao e lista" % c["id"])
        arc.igual(c["mod"], "RoguelikeSkillTreeVisualizer", "mod do criterio %s" % c["id"])
        arc.exigir(c.get("tipo_pendencia") in TIPOS_PENDENCIA,
                   "%s tipo_pendencia invalido: %r" % (c["id"], c.get("tipo_pendencia")))
        arc.exigir(isinstance(c.get("autorizacao_necessaria"), bool),
                   "%s autorizacao_necessaria nao e bool" % c["id"])
        arc.exigir(isinstance(c.get("prova_runtime"), bool),
                   "%s prova_runtime nao e bool" % c["id"])
        if c["estado"] != "OK":
            arc.exigir(c["prova_runtime"] is False,
                       "%s nao-OK nao pode declarar prova_runtime" % c["id"])


def _fixture_nao_vira_ok(R, ident):
    fx = carrega("rstv-observacoes")
    criterios = R.avaliar(fx["observacoes"], ident)
    _schema(R, criterios)
    ok = [c["id"] for c in criterios if c["estado"] == "OK"]
    reprovado = [c["id"] for c in criterios if c["estado"] == "REPROVADO"]
    arc.igual(ok, [], "fixture limpa NAO pode fechar OK (fixture nao prova runtime)")
    arc.igual(reprovado, [], "fixture limpa nao tem defeito, nao pode reprovar")
    for cid, _ in R.CAPACIDADES:
        por_id(criterios, cid)
    for c in criterios:
        if c["procedencia"] == "fixture":
            arc.exigir(c["estado"] != "OK", "%s fechou OK com procedencia fixture" % c["id"])


def _ausente(R, ident):
    aus = carrega("rstv-ausente")
    criterios = R.avaliar(aus["observacoes"], ident)
    _schema(R, criterios)
    arc.igual({c["estado"] for c in criterios}, {"NAO_EXERCITADO"},
              "sem leitura: toda capacidade NAO_EXERCITADO (AUSENTE nao e OK)")
    dep = por_id(criterios, "RSTV-25b-dependencia")
    arc.igual(dep.get("tipo_pendencia"), "tecnica", "RSTV-25b sem dado deve ser pendencia tecnica")
    arc.exigir(dep.get("lacuna_probe"), "RSTV-25b sem dado deve declarar lacuna_probe")
    arc.exigir(dep.get("autorizacao_necessaria") is False,
               "lacuna tecnica NAO e autorizacao por default")


def _lacunas(R, ident):
    """B1/B2: com identidade SUFICIENTE, ausencia/incompletude/malformado nao vira OK."""
    fx = carrega("rstv-lacunas")
    arc.exigir(fx.get("casos"), "fixture de lacunas sem 'casos'")
    for caso in fx["casos"]:
        obs = runtime_ctx(ident, **caso["observacao"])
        cs = R.avaliar([obs], ident)
        c = por_id(cs, caso["criterio_esperado"])
        arc.igual(c["estado"], caso["estado_esperado"],
                  "lacuna %r (%s): esperado %s, obtido %s"
                  % (caso["nome"], caso["criterio_esperado"],
                     caso["estado_esperado"], c["estado"]))
        arc.exigir(c["estado"] != "OK",
                   "lacuna %r fechou OK (AUSENTE/incompleto/malformado nunca vira OK)" % caso["nome"])
        arc.exigir(not c["motivo"].startswith("DEFEITO"),
                   "lacuna %r nao e defeito plantado (motivo=%r)" % (caso["nome"], c["motivo"]))
        arc.igual(c.get("tipo_pendencia"), "tecnica",
                  "lacuna %r deve classificar como pendencia TECNICA" % caso["nome"])
        arc.exigir(c.get("lacuna_probe"), "lacuna %r deve declarar lacuna_probe" % caso["nome"])
        arc.exigir(c.get("autorizacao_necessaria") is False,
                   "lacuna %r nao deve exigir autorizacao por default" % caso["nome"])


def _controles(R, ident):
    ctl = carrega("rstv-controles")
    arc.exigir(len(ctl["casos"]) >= 9, "esperava ao menos 9 controles negativos")
    for caso in ctl["casos"]:
        criterios = R.avaliar([caso["observacao"]], ident)
        c = por_id(criterios, caso["criterio_esperado"])
        arc.igual(c["estado"], caso["estado_esperado"],
                  "controle %r (%s): esperado %s, obtido %s"
                  % (caso["nome"], caso["criterio_esperado"], caso["estado_esperado"], c["estado"]))
        arc.exigir(c["motivo"].startswith("DEFEITO"),
                   "controle %r deveria trazer motivo de DEFEITO, veio %r" % (caso["nome"], c["motivo"]))


def _caminho_ok(R, ident):
    """O caminho OK existe, exercitado por um ARTEFATO SINTETICO persistido."""
    pos = carrega("rstv-positivo")
    arc.exigir(pos.get("sintetico") is True,
               "o artefato positivo tem de estar rotulado como SINTETICO")
    ident_pos = {"fonte_sha": pos["fonte_sha"], "dll_sha": pos["dll_sha"],
                 "config_sha": pos.get("config_sha")}
    obs = [dict({"procedencia": "runtime", "sessao": pos["sessao"]}, **o)
           for o in pos["observacoes"]]
    cs = R.avaliar(obs, ident_pos)
    _schema(R, cs)
    ok = [c["id"] for c in cs if c["estado"] == "OK"]
    arc.igual(len(ok), len(R.CAPACIDADES),
              "artefato positivo (sintetico) deveria fechar TODAS OK; OK=%s" % ok)
    for c in cs:
        arc.exigir(c["prova_runtime"] is True, "%s OK sem prova_runtime" % c["id"])
        arc.igual(c["fonte_sha"], ident_pos["fonte_sha"], "%s nao propagou fonte_sha" % c["id"])
        arc.igual(c["dll_sha"], ident_pos["dll_sha"], "%s nao propagou dll_sha" % c["id"])
        arc.igual(c.get("config_sha"), ident_pos["config_sha"], "%s nao propagou config_sha" % c["id"])
        arc.igual(c.get("sessao"), pos["sessao"], "%s OK sem a sessao da observacao" % c["id"])
    # coerencia: SEM identidade nao ha OK
    arc.igual([c["id"] for c in R.avaliar(obs, {}) if c["estado"] == "OK"], [],
              "sem fonte_sha/dll_sha nao pode haver OK")


def _cadeia(R, ident):
    """B4: cadeia de hash runtime — diverge/nao-confirmado nunca fecha OK."""
    cid = "RSTV-6-readonly-skills-pontos"
    # F1: a leitura da capacidade tem de ser COMPLETA (skills E pontos); so assim
    # o teste isola a CADEIA de hash como unico motivo possivel de nao-OK.
    par = {"skills_antes": ["A"], "skills_depois": ["A"],
           "pontos_antes": 4, "pontos_depois": 4}
    # hash_fonte divergente -> INDETERMINADO
    c = por_id(R.avaliar([runtime_ctx(ident, hash_fonte="f" * 64, **par)], ident), cid)
    arc.igual(c["estado"], "INDETERMINADO", "hash_fonte divergente -> INDETERMINADO")
    # hash_dll divergente -> INDETERMINADO (antes era IGNORADO)
    c = por_id(R.avaliar([runtime_ctx(ident, hash_dll="f" * 64, **par)], ident), cid)
    arc.igual(c["estado"], "INDETERMINADO", "hash_dll divergente -> INDETERMINADO")
    # config_sha declarado e nao conhecido pela identidade -> NAO_EXERCITADO
    c = por_id(R.avaliar([runtime_ctx(ident, config_sha="c" * 64, **par)], ident), cid)
    arc.igual(c["estado"], "NAO_EXERCITADO", "config_sha nao confirmado -> NAO_EXERCITADO")
    # R-1 (CIC-5R): a convencao ANTIGA (hash_fonte == sha da FONTE) NAO amarra a
    # build — o campo `hash_fonte` do coletor e o sha da DLL. Um valor que casa
    # com a fonte e nao com a DLL NUNCA pode fechar OK.
    arc.exigir(ident["fonte_sha"] != ident["dll_sha"],
               "fixture de identidade: fonte_sha e dll_sha tem de ser distintos")
    c = por_id(R.avaliar([runtime_ctx(ident, hash_fonte=ident["fonte_sha"], **par)], ident), cid)
    arc.exigir(c["estado"] != "OK",
               "hash_fonte == fonte_sha (convencao antiga) nao pode fechar OK (R-1)")
    # cadeia completa -> OK
    c = por_id(R.avaliar([runtime_ctx(ident, hash_dll=ident["dll_sha"], **par)], ident), cid)
    arc.igual(c["estado"], "OK", "fonte+dll casando com a identidade -> OK")
    # propagacao dos hashes + prova ao criterio (contrato positivo)
    arc.exigir([k for k in c if k.endswith("_sha")], "criterio deve expor hashes (*_sha)")
    arc.igual(c["fonte_sha"], ident["fonte_sha"], "criterio nao propagou fonte_sha")
    arc.igual(c["dll_sha"], ident["dll_sha"], "criterio nao propagou dll_sha")


def _obs_completa():
    """Leitura runtime COMPLETA e coerente (base dos controles F1-F7).

    Todos os campos que o criterio declara, sem defeito nenhum: e a mesma
    substancia do artefato positivo sintetico, sem depender do arquivo.
    """
    return {
        "personagem_esperado": "Raven",
        "personagem": {"gui_state": "ChoosingCharacter", "tem_personagem_selecionado": True,
                       "personagem": "Raven"},
        "skills_antes": ["Fireball", "Shield"], "skills_depois": ["Fireball", "Shield"],
        "pontos_antes": 4, "pontos_depois": 4,
        "janela": {"aberta": True, "fechada": True},
        "tooltip_pai_antes": "GUI Manager/Tooltips / Popups",
        "tooltip_pai_depois": "GUI Manager/Tooltips / Popups",
        "tooltip_indice_antes": 3, "tooltip_indice_depois": 3,
        "janelas_duplicadas": 0,
        "texto_bruto": "Deals [0] fire damage.", "texto_renderizado": "Deals 14 fire damage.",
        "linhas_dependencia": {"T4": 2, "T5": 0}, "dependency_por_tier": {"T4": 2, "T5": 0},
        "arestas_inventadas": 0,
        "geometria": {"caixa_na_tela_px": {"x": 10, "y": 20, "largura": 300, "altura": 40},
                      "tela": "1920x1080"},
    }


def _fechamento_f1_f7(R, ident):
    """F1-F7 (parecer CIC-3R): o defeito plantado nao fecha mais verde.

    Metodo (a regra do projeto: "todo teste tem de ser MOSTRADO REPROVANDO"): o
    caso parte de uma leitura runtime COMPLETA (os 7 criterios OK); o defeito do
    achado e entao plantado na dimensao que ele ataca. O criterio alvo tem de
    SAIR do OK e o motivo tem de nomear o defeito. No fim, a base e reavaliada:
    removido o defeito, o mesmo criterio volta a OK.

    A mesma tabela de casos e reusada pela prova RED contra o `rstv.py` anterior
    (que fechava OK em F1-F4/F6/F7) — o defeito nao foi inventado aqui: ele
    existia nos bytes antigos do produto.
    """
    base = runtime_ctx(ident, **_obs_completa())
    cs = R.avaliar([dict(base)], ident)
    _schema(R, cs)
    ok = [c["id"] for c in cs if c["estado"] == "OK"]
    arc.igual(len(ok), len(R.CAPACIDADES),
              "F1-F7 controle positivo: leitura completa tem de fechar TODAS OK; OK=%s" % ok)

    def sem(obs, *chaves):
        novo = dict(obs)
        for k in chaves:
            novo.pop(k, None)
        return novo

    def com(obs, **mudancas):
        novo = dict(obs)
        novo.update(mudancas)
        return novo

    geo_nan_x = {"caixa_na_tela_px": {"x": "NaN", "y": 20, "largura": 300, "altura": 40},
                 "tela": "1920x1080"}
    geo_nan_largura = {"caixa_na_tela_px": {"x": 10, "y": 20, "largura": float("nan"),
                                            "altura": 40},
                       "tela": "1920x1080"}
    casos = (
        # F1 — dimensao inteira nunca lida nao vira "ambas inalteradas"
        ("F1-skills-sem-pontos", "RSTV-6-readonly-skills-pontos", "NAO_EXERCITADO",
         [sem(base, "pontos_antes", "pontos_depois")], "pontos: dimensao NUNCA lida"),
        ("F1-pontos-sem-skills", "RSTV-6-readonly-skills-pontos", "NAO_EXERCITADO",
         [sem(base, "skills_antes", "skills_depois")], "skills: dimensao NUNCA lida"),
        # F2 — contagem invalida nao prova ausencia de duplicata
        ("F2-duplicadas-null", "RSTV-21-tooltip-restauracao", "NAO_EXERCITADO",
         [com(base, janelas_duplicadas=None)], "janelas_duplicadas MALFORMADA"),
        ("F2-duplicadas-negativo", "RSTV-21-tooltip-restauracao", "NAO_EXERCITADO",
         [com(base, janelas_duplicadas=-1)], "janelas_duplicadas MALFORMADA"),
        ("F2-duplicadas-bool", "RSTV-21-tooltip-restauracao", "NAO_EXERCITADO",
         [com(base, janelas_duplicadas=False)], "janelas_duplicadas MALFORMADA"),
        ("F2-duplicadas-lista", "RSTV-21-tooltip-restauracao", "NAO_EXERCITADO",
         [com(base, janelas_duplicadas=[])], "janelas_duplicadas MALFORMADA"),
        ("F2-duplicata-nao-booleana", "RSTV-21-tooltip-restauracao", "NAO_EXERCITADO",
         [sem(com(base, duplicata=None), "janelas_duplicadas")], "duplicata MALFORMADA"),
        # F3 — truthiness deixa de valer como confronto
        ("F3-contagem-diferente", "RSTV-25b-dependencia", "REPROVADO",
         [com(base, linhas_dependencia={"T4": 1}, dependency_por_tier={"T4": 3})],
         "linhas=1 != Dependency=3"),
        ("F3-valores-invalidos", "RSTV-25b-dependencia", "INDETERMINADO",
         [com(base, linhas_dependencia={"T4": "abc"}, dependency_por_tier={"T4": -2})],
         "valor INVALIDO no confronto"),
        # F4 — dado nao finito nao mede dimensao
        ("F4-nan-x", "RSTV-geometria-clipping", "NAO_EXERCITADO",
         [com(base, geometria=geo_nan_x)], "caixa_na_tela_px MALFORMADA"),
        ("F4-nan-largura", "RSTV-geometria-clipping", "NAO_EXERCITADO",
         [com(base, geometria=geo_nan_largura)], "largura=nan"),
        # F5 — divergencia declarada nao e sobrescrita pelo alias do coletor
        ("F5-hash-contraditorio", "RSTV-6-readonly-skills-pontos", "INDETERMINADO",
         [com(base, dll_sha="d" * 64)], "VALORES DIFERENTES"),
        # F6 — template CRU sem render observado nao e "placeholder resolvido"
        ("F6-cru-sem-render", "RSTV-26-placeholders", "NAO_EXERCITADO",
         [sem(base, "texto_renderizado")], "RENDERIZADO nao observado"),
        # F7 — sessoes distintas nao sao prova de um unico ciclo
        ("F7-sessoes-misturadas", "RSTV-6-readonly-skills-pontos", "INDETERMINADO",
         [com(base, sessao="sessao-A"), com(base, sessao="sessao-B")], "SESSOES diferentes"),
    )
    for nome, cid, esperado, obs_lista, fragmento in casos:
        cs = R.avaliar([dict(o) for o in obs_lista], ident)
        _schema(R, cs)
        c = por_id(cs, cid)
        arc.igual(c["estado"], esperado,
                  "%s: esperado %s, obtido %s (motivo=%r)"
                  % (nome, esperado, c["estado"], c["motivo"]))
        arc.exigir(c["estado"] != "OK", "%s nao pode fechar OK (achado do parecer CIC-3R)" % nome)
        arc.exigir(fragmento in c["motivo"],
                   "%s: o motivo tem de nomear o defeito (%r); veio %r"
                   % (nome, fragmento, c["motivo"]))
        arc.exigir(c["prova_runtime"] is False, "%s: nao-OK nao pode declarar prova_runtime" % nome)

    # remove o defeito -> o mesmo criterio volta a OK (base reavaliada)
    cs = R.avaliar([dict(base)], ident)
    arc.igual([c["id"] for c in cs if c["estado"] == "OK"], [cid for cid, _ in R.CAPACIDADES],
              "removido o defeito, a leitura completa tem de voltar a fechar TODAS OK")


def _l2_arestas_inventadas(R, ident):
    """L2 (parecer CIC-3R2): `arestas_inventadas` deriva o TIPO esperado.

    O defeito (mesma classe F2/F3, PRE-EXISTENTE): o campo era lido como
    "qualquer coisa que compare igual" — so o numero nao-bool > 0 virava
    defeito, e a forma MALFORMADA (`"2"` string, `""`, `[]`, `{}`, `-1`, `"NaN"`)
    fechava OK. O cartao CIC-3-L2 corrige: o valor presente e malformado e
    LEITURA MALFORMADA declarada (NAO_EXERCITADO, nunca OK); o valor canonico
    legitimo (inteiro/float valido, o booleano historico e a chave ausente)
    segue o comportamento ANTERIOR.

    A tabela das formas MALFORMADAS e a prova RED: contra o `rstv.py` sem a
    derivacao de tipo, cada uma delas fecha OK (ver a contra-prova em copia).
    """
    base = runtime_ctx(ident, **_obs_completa())

    def obs(**mud):
        novo = dict(base)
        novo.update(mud)
        return novo

    # controle positivo: a base completa fecha OK antes de plantar nada
    c = por_id(R.avaliar([obs()], ident), "RSTV-25b-dependencia")
    arc.igual(c["estado"], "OK", "L2 controle positivo: base completa tem de fechar OK")

    # (nome, valor, estado_esperado, fragmento_do_motivo)
    casos = (
        # legitimos: comportamento ANTERIOR preservado (fecham OK)
        ("L2-int-zero", 0, "OK", ""),
        ("L2-float-zero", 0.0, "OK", ""),
        ("L2-bool-true", True, "OK", ""),
        ("L2-none-explicito", None, "OK", ""),
        # defeitos: contagem valida > 0 continua REPROVADO (trava intacta)
        ("L2-int-um", 1, "REPROVADO", "INVENTADA"),
        ("L2-int-dois", 2, "REPROVADO", "INVENTADA"),
        ("L2-float-dois", 2.0, "REPROVADO", "INVENTADA"),
        # MALFORMADOS: NAO fecham OK — viram leitura malformada declarada
        ("L2-string-numero", "2", "NAO_EXERCITADO", "MALFORMADA"),
        ("L2-string-vazia", "", "NAO_EXERCITADO", "MALFORMADA"),
        ("L2-string-nan", "NaN", "NAO_EXERCITADO", "MALFORMADA"),
        ("L2-lista", [], "NAO_EXERCITADO", "MALFORMADA"),
        ("L2-dict", {}, "NAO_EXERCITADO", "MALFORMADA"),
        ("L2-negativo", -1, "NAO_EXERCITADO", "MALFORMADA"),
    )
    for nome, valor, esperado, fragmento in casos:
        c = por_id(R.avaliar([obs(arestas_inventadas=valor)], ident),
                   "RSTV-25b-dependencia")
        arc.igual(c["estado"], esperado,
                  "%s (valor=%r): esperado %s, obtido %s (motivo=%r)"
                  % (nome, valor, esperado, c["estado"], c["motivo"]))
        if esperado == "OK":
            arc.exigir(c["prova_runtime"] is True, "%s OK tem de declarar prova_runtime" % nome)
            continue
        arc.exigir(fragmento in c["motivo"],
                   "%s: o motivo tem de nomear %r; veio %r" % (nome, fragmento, c["motivo"]))
        if esperado == "REPROVADO":
            # defeito plantado ACIONAVEL: o motivo e de DEFEITO
            arc.exigir(c["motivo"].startswith("DEFEITO"),
                       "%s deveria trazer motivo de DEFEITO; veio %r" % (nome, c["motivo"]))
        else:
            # leitura MALFORMADA (lacuna) nao pode parecer defeito plantado
            arc.exigir(not c["motivo"].startswith("DEFEITO"),
                       "%s nao e defeito plantado (motivo=%r)" % (nome, c["motivo"]))
        arc.exigir(c["prova_runtime"] is False,
                   "%s nao-OK nao pode declarar prova_runtime" % nome)

    # a forma MALFORMADA e LEITURA MALFORMADA (lacuna tecnica declarada) —
    # o mesmo contrato de B1/B2/L1, nao um novo estado
    for nome, valor in (("L2-string-numero", "2"), ("L2-lista", []),
                        ("L2-negativo", -1), ("L2-string-vazia", "")):
        c = por_id(R.avaliar([obs(arestas_inventadas=valor)], ident),
                   "RSTV-25b-dependencia")
        arc.igual(c["estado"], "NAO_EXERCITADO", "%s: leitura malformada -> NAO_EXERCITADO" % nome)
        arc.igual(c.get("tipo_pendencia"), "tecnica",
                  "%s: leitura malformada e pendencia TECNICA" % nome)
        arc.exigir(c.get("lacuna_probe"), "%s: leitura malformada declara lacuna_probe" % nome)

    # a chave AUSENTE (caminho valido de ausencia) segue fechando OK
    sem_chave = dict(base)
    sem_chave.pop("arestas_inventadas", None)
    c = por_id(R.avaliar([sem_chave], ident), "RSTV-25b-dependencia")
    arc.igual(c["estado"], "OK", "L2-chave-ausente: a ausencia legitima tem de fechar OK")


def _canonico_excecao(R, ident):
    """B3: o conjunto canonico das 7 sobrevive a dado malformado e a excecoes."""
    canonico = [cid for cid, _ in R.CAPACIDADES]
    # (a) dado que ANTES derrubava a capacidade (pontos nao numerico) virou lacuna,
    #     MAS o conjunto canonico continua exato.
    cs = R.avaliar([runtime_ctx(ident, pontos_antes=1, pontos_depois="abc")], ident)
    arc.igual([c["id"] for c in cs], canonico,
              "conjunto canonico exato mesmo com dado malformado")
    arc.exigir(all(i.startswith("RSTV") for i in [c["id"] for c in cs]),
               "nenhum id fora do canonico (sem fallback por nome de funcao)")
    # (b) excecao REAL numa capacidade: o id canonico dela e preservado.
    def boom(_obs, _ident):
        raise RuntimeError("boom proposital")

    original = R._CAPS
    try:
        R._CAPS = (("RSTV-26-placeholders", boom),)
        cs = R.avaliar([runtime_ctx(ident)], ident)
    finally:
        R._CAPS = original
    arc.igual([c["id"] for c in cs], ["RSTV-26-placeholders"],
              "excecao preserva o id canonico da capacidade")
    arc.igual(cs[0]["estado"], "INDETERMINADO", "excecao -> INDETERMINADO")
    arc.exigir(cs[0].get("lacuna_probe"), "excecao deve declarar lacuna_probe")


def _adaptadores(R, ident):
    # [N] no texto CRU e o TEMPLATE legitimo e NAO pode reprovar — mas o OK passa
    # a exigir o RENDERIZADO observado (F6 do parecer CIC-3R).
    c = por_id(R.avaliar([runtime_ctx(ident, texto_bruto="Deals [2] fire damage.")], ident),
               "RSTV-26-placeholders")
    arc.igual(c["estado"], "NAO_EXERCITADO",
              "indice no texto CRU: template legitimo, mas sem render nao fecha OK (F6)")
    arc.exigir(not c["motivo"].startswith("DEFEITO"),
               "o template CRU nao e DEFEITO (o '[N]' e do motor): %r" % c["motivo"])
    arc.exigir("RENDERIZADO nao observado" in c["motivo"],
               "F6: o motivo tem de dizer que o render nao foi observado: %r" % c["motivo"])
    # com o RENDERIZADO limpo, o MESMO cru fecha OK (o template nao e o defeito)
    c = por_id(R.avaliar([runtime_ctx(ident, texto_bruto="Deals [2] fire damage.",
                                      texto_renderizado="Deals 14 fire damage.")], ident),
               "RSTV-26-placeholders")
    arc.igual(c["estado"], "OK", "cru com template + render limpo tem de fechar OK")
    # '*' no cru sem o zero nao e o defeito
    c = por_id(R.avaliar([runtime_ctx(ident, texto_bruto="Deals *2 fire damage.",
                                      texto_renderizado="Deals *2 fire damage.")], ident),
               "RSTV-26-placeholders")
    arc.igual(c["estado"], "OK", "'*2' nao e o defeito '*0'")
    # forma NORMALIZADA (bloco campos) e lida
    norm = [{"procedencia": "fixture", "rotulo_fixture": "x",
             "campos": {"texto_renderizado": {"estado": "PRESENTE", "valor": "Deals *0 damage."}}}]
    c = por_id(R.avaliar(norm, ident), "RSTV-26-placeholders")
    arc.igual(c["estado"], "REPROVADO", "bloco 'campos' normalizado tem de ser lido")


def _modulo(caminho, nome):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _coletor():
    """Importa o coletor CIC-5 REAL (somente leitura) para costurar o formato."""
    caminho = os.path.join(REPO, "tools", "automacao", "runtime", "coletor.py")
    arc.exigir(os.path.isfile(caminho), "coletor CIC-5 ausente: %s" % caminho)
    return _modulo(caminho, "cic5_coletor")


def _fixture_probe():
    caminho = os.path.join(REPO, "tools", "automacao", "runtime", "fixtures",
                           "probe-saida-exemplo.entrada.json")
    with open(caminho, encoding="utf-8") as fh:
        return caminho, json.load(fh)


def _integracao_cic5(R, ident):
    """Costura REAL probe -> coletor (CIC-5) -> `rstv.avaliar`.

    Prova que o adaptador le o formato REAL do coletor (bloco `campos` normalizado
    + `sessao`/`hash_fonte` do TOPO injetados) e que o `hash_fonte` do coletor
    (sha256 da DLL, ver `coletor.derivar_config`) e confrontado com `dll_sha` da
    identidade — nao com `fonte_sha` (achado R-1 do CIC-5R). NAO prova runtime:
    nada aqui foi lido do jogo.
    """
    col = _coletor()
    fx_path, fx = _fixture_probe()
    plano = os.path.join(REPO, "tools", "automacao", "runtime", "fixtures",
                         "plano-exemplo.entrada.json")

    # (1) o proprio coletor NAO deixa a fixture rotulada virar runtime
    res, codigo = col.consolidar_probe(fx_path, plano)
    arc.igual(res["status"], "FIXTURE",
              "coletor CIC-5: fixture rotulada tem de sair FIXTURE")
    arc.igual(codigo, 2, "coletor CIC-5: fixture -> exit 2")

    # (2) forma NORMALIZADA REAL (produzida pelo proprio coletor) -> avaliar
    ctx = {"sessao": fx["sessao"], "hash_fonte": fx["hash_fonte"]}
    norm = [col.normalizar_observacao(o, "fixture", rotulo_fixture="probe-saida-exemplo")
            for o in col.anexar_contexto(fx["observacoes"], ctx)]
    arc.exigir(all("campos" in n for n in norm),
               "coletor: observacao normalizada sem o bloco 'campos'")
    cs = R.avaliar(norm, ident)
    _schema(R, cs)
    arc.igual([c["id"] for c in cs if c["estado"] == "OK"], [],
              "formato REAL do coletor (fixture) NAO pode fechar OK")
    # o fallback NAO_APLICAVEL do objeto INATIVO tem de ser lido pelo adaptador
    inativa = next((n for n in norm
                    if n["campos"]["texto_renderizado"]["estado"] == "NAO_APLICAVEL"), None)
    arc.exigir(inativa is not None, "coletor: fixture sem objeto inativo NAO_APLICAVEL")
    arc.igual(R._campo(inativa, "texto_renderizado"), "AUT4-MARCADOR-DESCRICAO",
              "adaptador deve ler o fallback NAO_APLICAVEL (texto_bruto) do coletor")

    # (3) CONTRATO DE HASH (R-1): hash_fonte do coletor == dll_sha da identidade.
    #     Observacao no formato REAL, com procedencia runtime + sessao + hash_fonte
    #     = sha da DLL (valores da fixture, ROTULADOS como sinteticos).
    dll, src = fx["hash_fonte"], "0" * 64
    arc.exigir(dll != src, "fixture: hash da DLL tem de diferir do da fonte")
    ident_cic5 = {"fonte_sha": src, "dll_sha": dll}
    obs_rt = dict(norm[0])
    obs_rt.update(procedencia="runtime", sessao=fx["sessao"], hash_fonte=dll)
    c = por_id(R.avaliar([obs_rt], ident_cic5), "RSTV-26-placeholders")
    arc.igual(c["estado"], "OK",
              "hash_fonte == dll_sha tem de amarrar a build (integracao CIC-5/R-1)")
    arc.igual(c.get("dll_sha"), dll, "criterio OK deve propagar o dll_sha da identidade")
    # a convencao ANTIGA (hash_fonte == fonte_sha) NAO pode fechar OK
    obs_err = dict(obs_rt)
    obs_err["hash_fonte"] = src
    c = por_id(R.avaliar([obs_err], ident_cic5), "RSTV-26-placeholders")
    arc.exigir(c["estado"] != "OK",
               "hash_fonte == fonte_sha (convencao antiga) nao pode fechar OK")


def _cli():
    """Exercita a CLI REAL do rstv.py (exit code por estado)."""
    py = sys.executable
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    base = [py, os.path.join(AQUI, "rstv.py")]

    def roda(obs_path, ident_path):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "res.json")
            proc = subprocess.run(base + ["--observacoes", obs_path,
                                          "--identidade", ident_path, "--out", out],
                                  cwd=REPO, env=env, stdout=subprocess.PIPE,
                                  stderr=subprocess.STDOUT, universal_newlines=True, timeout=120)
            arc.exigir(os.path.isfile(out), "CLI nao gravou --out")
            with open(out, encoding="utf-8") as fh:
                return proc.returncode, json.load(fh)

    # fixture limpa -> NAO_EXERCITADO -> exit 2
    codigo, res = roda(os.path.join(AQUI, "rstv-observacoes.entrada.json"),
                       os.path.join(AQUI, "rstv-identidade.json"))
    arc.igual(codigo, 2, "CLI de fixture limpa deveria sair 2 (nao exercitado)")
    arc.igual(res["runtime_exercitado"], False, "fixture nao pode contar como runtime exercitado")

    # um controle com defeito -> REPROVADO -> exit 1
    ctl = carrega("rstv-controles")
    with tempfile.TemporaryDirectory() as tmp:
        caso = os.path.join(tmp, "caso.json")
        with open(caso, "w", encoding="utf-8") as fh:
            json.dump([ctl["casos"][0]["observacao"]], fh)
        codigo, res = roda(caso, os.path.join(AQUI, "rstv-identidade.json"))
    arc.igual(codigo, 1, "CLI com defeito plantado deveria sair 1 (reprovado)")
    arc.igual(res["reprovado"], True, "resumo do CLI deveria marcar reprovado")


# ---------------------------------------------------------------------- suite --

def corpo():
    R = rstv()
    ident = identidade()
    _fixture_nao_vira_ok(R, ident)
    _ausente(R, ident)
    _lacunas(R, ident)
    _controles(R, ident)
    _caminho_ok(R, ident)
    _cadeia(R, ident)
    _fechamento_f1_f7(R, ident)
    _l2_arestas_inventadas(R, ident)
    _canonico_excecao(R, ident)
    _adaptadores(R, ident)
    _integracao_cic5(R, ident)
    _cli()


# ---------------------------------------------------------------- contra-prova -

def contra_prova():
    """Isca meta: um `_fecha` 'sempre OK' NAO pega os controles.

    Prova que o REPROVADO dos controles vem da regra de avaliacao, nao de um
    passe livre. Reprovacao de verdade exige defeito detectado.
    """
    R = rstv()
    ident = identidade()
    ctl = carrega("rstv-controles")
    falhas = []
    original = R._fecha
    try:
        R._fecha = lambda *a, **k: (R.OK, "runtime", "isca: sempre OK")
        for caso in ctl["casos"]:
            c = por_id(R.avaliar([caso["observacao"]], ident), caso["criterio_esperado"])
            if c["estado"] == "REPROVADO":
                falhas.append("isca 'sempre OK' ainda reprovou %s" % caso["nome"])
        if not falhas:
            print("CONTRA-PROVA|PASSOU|isca 'sempre OK' deixou os %d controles passarem "
                  "(o REPROVADO real vem da regra)" % len(ctl["casos"]))
    finally:
        R._fecha = original
    for f in falhas:
        print("CONTRA-PROVA|REPROVOU|%s" % f)
    return 1 if falhas else 0


def main():
    ap = argparse.ArgumentParser(description="CIC-3 teste do avaliador RSTV.")
    ap.add_argument("--contra-prova", action="store_true",
                    help="roda so a isca meta (o avaliador 'sempre OK' nao pode pegar os controles)")
    args, _ = ap.parse_known_args()
    if args.contra_prova:
        return contra_prova()
    return arc.roda(META, corpo)


if __name__ == "__main__":
    sys.exit(main())
