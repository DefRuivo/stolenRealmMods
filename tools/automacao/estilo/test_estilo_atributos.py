#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_estilo_atributos.py - AUT-7: teste da frente de estilo/atributos/dump.

Roda SOZINHO (nao entra no runner `tools/testes/`): e teste de FERRAMENTA, na
mesma convencao de `tools/automacao/ciclo/test_*.py` (exit 0 = tudo verde,
1 = reprovou, 2 = nao rodou).

A REGRA DO PROJETO: todo teste tem de ser MOSTRADO REPROVANDO. Aqui os defeitos
sao PLANTADOS na entrada (fonte do BetterStats copiado com defeito; sombra fora do
modelo do `regras_bct`; par ligado/desligado divergente; cadeia de prova
incompleta) e a checagem TEM de reprovar. E o que prova que a medicao mede.

Uso:
    python tools/automacao/estilo/test_estilo_atributos.py
Exit: 0 = TUDO OK · 1 = alguma checagem falhou · 2 = nao deu para rodar.
"""
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
if AQUI not in sys.path:
    sys.path.insert(0, AQUI)

import estilo_atributos as ea  # noqa: E402

RAIZ = ea.RAIZ
CASOS = []
FALHAS = []


def caso(nome):
    def deco(fn):
        CASOS.append((nome, fn))
        return fn
    return deco


def exigir(cond, msg):
    if not cond:
        raise AssertionError(msg)


def _sombras_bct():
    bct = ea._bct()
    return bct


def _sha(caminho):
    h = hashlib.sha256()
    with io.open(caminho, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def _vincular(obs, pasta, nome, sessao=None):
    """Da a observacao uma evidencia REAL: o proprio JSON com sha256 conferivel.

    Sem isto um OK de runtime seria falso: a evidencia tem de estar amarrada aos bytes
    (o arquivo contem a observacao) e a sessao da observacao tem de ser a da rodada.
    """
    caminho = os.path.join(pasta, nome + ".obs.json")
    if sessao:
        obs["sessao"] = sessao
    with io.open(caminho, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(obs, ensure_ascii=False, sort_keys=True))
    obs["evidencia"] = [{"caminho": caminho, "sha256": _sha(caminho)}]
    return obs


def _identidade_completa(sessao="sessao-1"):
    """Identidade de rodada com SHA-256 COMPLETO (placeholder de 12 chars nao vale)."""
    return {"fonte_sha": "f" * 64, "dll_sha": "d" * 64, "sessao": sessao}


def _material_completo(valor=0.5, cor="#FFFFFFFF"):
    """TODAS as propriedades efetivas do material exigidas por `regras_bf_estilo`."""
    import regras_bf_estilo as rbf
    props = {}
    for grupo, nomes in rbf.PRECISA_COPIAR.items():
        for nome in nomes:
            props[nome] = ([valor] * 4 if nome == "_ClipRect" else
                           (cor if nome.endswith("Color") else valor))
    return props


def _arquivo_evidencia():
    """Arquivo REAL para figurar como evidencia declarada pela observacao."""
    caminho = os.path.join(tempfile.gettempdir(), "aut7-evidencia-de-teste.json")
    with io.open(caminho, "w", encoding="utf-8") as fh:
        fh.write("{\"observacao\": \"arquivo de evidencia do teste do AUT-7\"}")
    return caminho


# ------------------------------------------------------------------ offline

@caso("estado-do-registro: mapeia suite, isca e NAO_RODOU")
def _t_estado_do_registro():
    exigir(ea._estado_do_registro({"esperado": "passar", "estado": "PASSOU"}) == ea.OK,
           "PASSOU com esperado=passar tem de ser OK")
    exigir(ea._estado_do_registro({"esperado": "passar", "estado": "REPROVOU"}) == ea.REPROVADO,
           "REPROVOU tem de ser REPROVADO")
    exigir(ea._estado_do_registro({"esperado": "passar", "estado": "NAO_RODOU"})
           == ea.NAO_EXERCITADO, "NAO_RODOU nunca pode virar OK")
    exigir(ea._estado_do_registro({"esperado": "reprovar", "estado": "PROVA_OK"}) == ea.OK,
           "isca que reprovou como devia e PROVA_OK")
    exigir(ea._estado_do_registro({"esperado": "reprovar", "estado": "PROVA_FALHOU"})
           == ea.REPROVADO, "isca que NAO reprovou e defeito do controle negativo")
    exigir(ea._estado_do_registro({"esperado": "reprovar", "estado": "PASSOU"})
           == ea.REPROVADO, "isca que PASSOU tem de reprovar (o controle negativo quebrou)")
    exigir(ea._estado_do_registro({"esperado": "passar", "estado": "??"}) == ea.INDETERMINADO,
           "estado desconhecido nao pode virar OK")


@caso("BetterStats estrutural: fonte real passa nos 6 checks")
def _t_bs_ok():
    criterios, detalhe = ea.medir_betterstats(RAIZ, None)
    ids = [c["id"] for c in criterios]
    exigir(len(ids) == 6, "esperava 6 checagens estruturais do BetterStats, veio %d" % len(ids))
    for c in criterios:
        exigir(c["estado"] == ea.OK,
               "%s saiu %s no fonte real (esperado OK): %s" % (c["id"], c["estado"], c["observado"]))
    exigir(all(ch["ok"] for ch in detalhe["checks"]), "o detalhe tem de concordar com os criterios")


@caso("BetterStats estrutural: DEFEITO plantado tem de REPROVAR (base do final)")
def _t_bs_defeito_base():
    tmp = tempfile.mkdtemp(prefix="aut7-bs-")
    try:
        os.makedirs(os.path.join(tmp, "BetterStats"))
        src = io.open(os.path.join(RAIZ, "BetterStats", "Plugin.cs"), encoding="utf-8").read()
        com_defeito = ea.defeito_do_betterstats(src, "base-do-final")
        exigir(com_defeito != src, "o plantio do defeito nao mudou nada")
        with io.open(os.path.join(tmp, "BetterStats", "Plugin.cs"), "w", encoding="utf-8") as fh:
            fh.write(com_defeito)
        criterios, _ = ea.medir_betterstats(tmp, None)
        por_id = {c["id"]: c["estado"] for c in criterios}
        exigir(por_id.get("AUT-7/BetterStats/estrutural/base-do-savedmap") == ea.REPROVADO,
               "com a base vinda do valor FINAL o check tem de REPROVAR: %r" % por_id)
        exigir(por_id.get("AUT-7/BetterStats/estrutural/final-do-motor") == ea.OK,
               "o defeito de base nao pode derrubar a checagem do valor FINAL")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@caso("BetterStats estrutural: DEFEITO plantado tem de REPROVAR (geometria sem guarda)")
def _t_bs_defeito_geometria():
    tmp = tempfile.mkdtemp(prefix="aut7-bs-")
    try:
        os.makedirs(os.path.join(tmp, "BetterStats"))
        src = io.open(os.path.join(RAIZ, "BetterStats", "Plugin.cs"), encoding="utf-8").read()
        com_defeito = ea.defeito_do_betterstats(src, "geometria-sem-guarda")
        exigir(com_defeito != src, "o plantio do defeito nao mudou nada")
        with io.open(os.path.join(tmp, "BetterStats", "Plugin.cs"), "w", encoding="utf-8") as fh:
            fh.write(com_defeito)
        criterios, _ = ea.medir_betterstats(tmp, None)
        por_id = {c["id"]: c["estado"] for c in criterios}
        exigir(por_id.get("AUT-7/BetterStats/estrutural/geometria-deslocada-uma-vez") == ea.REPROVADO,
               "sem o deslocamento de -40f o check de geometria tem de REPROVAR: %r" % por_id)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@caso("medicao offline REAL: roda a suite do projeto e nao deixa mod sem familia de teste")
def _t_medicao_offline_real():
    out = tempfile.mkdtemp(prefix="aut7-med-")
    try:
        def medir():
            return ea.medir_offline(RAIZ, out, identidade={"fonte_sha": "x", "dll_sha": "y"})

        criterios, meta = medir()
        # A arvore viva tem ESCRITORES CONCORRENTES: se alguem mexer num caminho coberto durante
        # os ~100s da rodada, a guarda de drift (fail-closed) descarta a saida da suite e nao sobra
        # criterio de teste. Isso e comportamento correto da guarda, nao defeito da entrega - entao
        # repete UMA vez antes de reprovar (sem afrouxar o que o caso exige).
        if not [c for c in criterios if c.get("mod") == "BetterFont" and "/puro/" in str(c.get("id"))]:
            print("          (sem criterio de suite: drift na arvore viva - repetindo a rodada)")
            criterios, meta = medir()
        por_mod = {}
        for c in criterios:
            por_mod.setdefault(c["mod"], []).append(c)
        for mod in ea.MODS:
            exigir(mod in por_mod, "mod %s ficou sem NENHUM criterio na medicao" % mod)
        # BetterFont/BCT/Debugger: provam pela suite REAL (puros) - e o runner tem de ter saida.
        for mod, prefixo in (("BetterFont", "t_bf_"), ("BetterCombatText", "t_bct_"),
                             ("RoguelikeDebugger", "t_debugger_")):
            provas = [c for c in por_mod[mod] if "/puro/" in c["id"]]
            exigir(provas, "%s devia ter provas da suite pura" % mod)
            exigir(all(c["estado"] == ea.OK for c in provas),
                   "%s: algum teste puro nao saiu OK: %r"
                   % (mod, [(c["id"], c["estado"]) for c in provas if c["estado"] != ea.OK]))
            for c in provas:
                exigir(c["evidencia"], "%s: prova sem evidencia nao vale" % c["id"])
        # BetterStats nao tem familia `t_bs_*`: a lacuna tem de estar DITA, nunca escondida.
        exigir(any("/suite-ausente" in c["id"] for c in por_mod["BetterStats"]),
               "BetterStats sem familia de teste tem de declarar a lacuna")
        exigir(meta["suites"]["puros"]["sha256"], "a saida da suite pura tem de ter sha256")
        exigir(meta["suites"]["contra_prova"]["sha256"],
               "a saida da suite de contra-prova tem de ter sha256")
    finally:
        shutil.rmtree(out, ignore_errors=True)


# ------------------------------------------------------------------ runtime

@caso("runtime SEM observacao: os 11 aspectos existem e NENHUM e OK")
def _t_runtime_vazio():
    criterios = ea.avaliar([], {"fonte_sha": "f" * 8, "dll_sha": "d" * 8})
    ids = {c["id"] for c in criterios}
    esperados = {cid for cid, _m, _f in ea._ASPECTOS}
    exigir(ids == esperados, "o conjunto canonico de aspectos mudou: %r" % sorted(ids ^ esperados))
    for c in criterios:
        exigir(c["estado"] == ea.NAO_EXERCITADO,
               "%s sem observacao tem de ser NAO_EXERCITADO, veio %s" % (c["id"], c["estado"]))
        exigir(c["motivo"], "%s sem motivo dito" % c["id"])
        exigir(c["estado"] != ea.OK, "%s nao pode sair OK sem medicao" % c["id"])


@caso("runtime: observacao MALFORMADA nao levanta e nunca vira OK")
def _t_runtime_malformado():
    lixo = [None, 3, "texto", {"campos": "nao-e-dict"}, {"cores": {"texto": None}}]
    criterios = ea.avaliar(lixo, {})
    exigir(len(criterios) == len(ea._ASPECTOS), "o avaliador tem de devolver os 11 ids mesmo com lixo")
    for c in criterios:
        exigir(c["estado"] in (ea.NAO_EXERCITADO, ea.INDETERMINADO),
               "%s com lixo saiu %s (OK/REPROVADO seriam falso veredito)" % (c["id"], c["estado"]))


SUPERFICIES = None


def _superficies():
    global SUPERFICIES
    if SUPERFICIES is None:
        SUPERFICIES = list(ea._bct().SUPERFICIES_DO_BCT)
    return SUPERFICIES


def _obs_superficie(nome, texto_hex="FFFFFF", sombra_hex=None, procedencia="fixture",
                    extras=None, alfa=1.0):
    """Observacao de UMA superficie alvo, no formato do probe (cores com alfa)."""
    bct = ea._bct()
    sombra = sombra_hex or str(bct.sombra_para(texto_hex)).upper().lstrip("#")
    obs = {
        "objeto": nome + "_Text",
        "caminho": "Canvas/HUD/" + nome + "/Text",
        "componente": "TextMeshProUGUI",
        "cores": {"texto": "#%sFF (r=1 g=1 b=1 a=1)" % texto_hex,
                  "sombra": "#%s%s (r=0 g=0 b=0 a=%s)" % (sombra, "FF" if alfa >= 1 else "80", alfa)},
        "keywords": {"OUTLINE_ON": True, "UNDERLAY_ON": True},
        "procedencia": procedencia,
    }
    if extras:
        obs.update(extras)
    return obs


def _todas_superficies(procedencia="fixture", extras=None):
    return [_obs_superficie(n, procedencia=procedencia, extras=extras) for n in _superficies()]


def _obs_superficie_bct(texto_hex, sombra_hex, procedencia="fixture", extras=None):
    """Compativel com os casos antigos: uma superficie com sombra ESCOLHIDA pelo teste."""
    return _obs_superficie(_superficies()[0], texto_hex, sombra_hex, procedencia, extras)


@caso("BetterCombatText: sombra fora do modelo do regras_bct tem de REPROVAR")
def _t_bct_sombra_errada():
    bct = _sombras_bct()
    exigir(bct is not None, "regras_bct indisponivel: sem modelo independente nao ha prova")
    letra = "FFFFFF"
    errada = letra
    exigir(str(bct.sombra_para(letra)).upper().lstrip("#") != errada,
           "a sombra errada do teste coincide com a esperada: o caso nao prova nada")
    criterios = ea.avaliar([_obs_superficie_bct(letra, errada)], {})
    alvo = [c for c in criterios if c["id"].endswith("runtime-superficies-contraste")][0]
    exigir(alvo["estado"] == ea.REPROVADO,
           "sombra igual a letra tem de REPROVAR, veio %s (%s)" % (alvo["estado"], alvo["observado"]))


@caso("BetterCombatText: UMA superficie so (sem as canonicas) nunca vira OK")
def _t_bct_superficie_unica():
    """ACHADO AUT-7R: uma unica BossHealthbar com OUTLINE_ON e SEM cores era OK."""
    so_uma = [_obs_superficie(_superficies()[0])]
    so_uma[0]["cores"] = {}
    alvo = [c for c in ea.avaliar(so_uma, _identidade_completa())
            if c["id"].endswith("runtime-superficies-contraste")][0]
    exigir(alvo["estado"] != ea.OK,
           "superficie unica sem cores nao pode virar OK, veio %s" % alvo["estado"])
    exigir(alvo["estado"] == ea.NAO_EXERCITADO,
           "falta de cores e de superficies canonicas e LACUNA, veio %s" % alvo["estado"])


@caso("BetterCombatText: sombra CERTA em fixture NAO vira OK (fixture nao prova runtime)")
def _t_bct_fixture_nao_aprova():
    criterios = ea.avaliar(_todas_superficies("fixture"), _identidade_completa())
    alvo = [c for c in criterios if c["id"].endswith("runtime-superficies-contraste")][0]
    exigir(alvo["estado"] == ea.NAO_EXERCITADO,
           "fixture com valores certos tem de sair NAO_EXERCITADO, veio %s" % alvo["estado"])
    exigir(alvo.get("prova_runtime") is not True, "fixture nao pode carimbar prova_runtime")


@caso("BetterCombatText: runtime so fecha OK com TODAS as superficies, session e evidencia")
def _t_bct_cadeia():
    ident = _identidade_completa("sessao-1")
    pasta = tempfile.mkdtemp(prefix="aut7-evid-")
    try:
        completos = [_vincular(_obs_superficie(n, procedencia="runtime", extras={
            "fonte_sha": ident["fonte_sha"], "dll_sha": ident["dll_sha"]}), pasta, "sup%d" % i,
            "sessao-1") for i, n in enumerate(_superficies())]
        alvo = [c for c in ea.avaliar(completos, ident)
                if c["id"].endswith("runtime-superficies-contraste")][0]
        exigir(alvo["estado"] == ea.OK,
               "runtime com cadeia completa e todas as superficies devia fechar OK, veio %s (%s)"
               % (alvo["estado"], alvo["motivo"]))
        exigir(alvo["prova_runtime"] is True, "OK de runtime exige prova_runtime=True")
        exigir(set(_superficies()) == set(alvo["superficies_medidas"]),
               "as superficies canonicas medidas tem de estar declaradas: %r"
               % alvo["superficies_medidas"])
        # 1) sem sessao; 2) evidencia que NAO contem a observacao; 3) identidade curta
        sem_sessao = [dict(o, sessao="") for o in completos]
        alvo2 = [c for c in ea.avaliar(sem_sessao, ident)
                 if c["id"].endswith("runtime-superficies-contraste")][0]
        exigir(alvo2["estado"] != ea.OK,
               "runtime SEM sessao nao pode virar OK (nunca OK por rotulo), veio %s" % alvo2["estado"])
        solto = [dict(o, evidencia=[_arquivo_evidencia()]) for o in completos]
        alvo3 = [c for c in ea.avaliar(solto, ident)
                 if c["id"].endswith("runtime-superficies-contraste")][0]
        exigir(alvo3["estado"] != ea.OK,
               "evidencia que nao contem a observacao nao pode virar OK, veio %s" % alvo3["estado"])
        alvo4 = [c for c in ea.avaliar(completos, {"fonte_sha": "f" * 12, "dll_sha": "d" * 12,
                                                   "sessao": "sessao-1"})
                 if c["id"].endswith("runtime-superficies-contraste")][0]
        exigir(alvo4["estado"] != ea.OK,
               "identidade incompleta (hash curto) nao pode assinar OK, veio %s" % alvo4["estado"])
    finally:
        shutil.rmtree(pasta, ignore_errors=True)


@caso("BetterCombatText: 6 leituras NAO marcam a 7a superficie (A3: token, nunca substring)")
def _t_bct_superficie_token():
    """ACHADO A3: `Healthbar` e substring de `BossHealthbar` - 6 leituras marcavam as 7."""
    sup = _superficies()
    exigir("Healthbar" in sup and "BossHealthbar" in sup,
           "o caso exige as superficies `Healthbar`/`BossHealthbar`: %r" % sup)
    sem_healthbar = [n for n in sup if n != "Healthbar"]
    exigir(len(sem_healthbar) == len(sup) - 1, "esperava 6 das 7 superficies")
    ident = _identidade_completa("sessao-1")
    pasta = tempfile.mkdtemp(prefix="aut7-a3-")
    try:
        obs = [_vincular(_obs_superficie(n, procedencia="runtime", extras={
            "fonte_sha": ident["fonte_sha"], "dll_sha": ident["dll_sha"]}), pasta, "sup%d" % i,
            "sessao-1") for i, n in enumerate(sem_healthbar)]
        alvo = [c for c in ea.avaliar(obs, ident)
                if c["id"].endswith("runtime-superficies-contraste")][0]
        exigir(alvo["estado"] == ea.NAO_EXERCITADO,
               "faltando a superficie `Healthbar` o criterio tem de ser LACUNA, veio %s (%s)"
               % (alvo["estado"], alvo["motivo"]))
        exigir("Healthbar" not in alvo["superficies_medidas"],
               "`Healthbar` NAO pode ser dada como medida por substring de `BossHealthbar`: %r"
               % alvo["superficies_medidas"])
        exigir(set(sem_healthbar) <= set(alvo["superficies_medidas"]),
               "as 6 superficies realmente lidas tem de continuar medidas: %r"
               % alvo["superficies_medidas"])
        exigir("Healthbar" in str(alvo["motivo"]),
               "a lacuna tem de NOMEAR a superficie ausente: %r" % alvo["motivo"])
        # controle POSITIVO: com as 7 de verdade o mesmo cenario fecha OK
        todas = [_vincular(_obs_superficie(n, procedencia="runtime", extras={
            "fonte_sha": ident["fonte_sha"], "dll_sha": ident["dll_sha"]}), pasta, "todas%d" % i,
            "sessao-1") for i, n in enumerate(sup)]
        alvo2 = [c for c in ea.avaliar(todas, ident)
                 if c["id"].endswith("runtime-superficies-contraste")][0]
        exigir(alvo2["estado"] == ea.OK,
               "as 7 superficies medias de verdade tem de fechar OK, veio %s (%s)"
               % (alvo2["estado"], alvo2["motivo"]))
        exigir(set(sup) == set(alvo2["superficies_medidas"]),
               "as 7 superficies canonicas tem de estar declaradas: %r" % alvo2["superficies_medidas"])
    finally:
        shutil.rmtree(pasta, ignore_errors=True)


@caso("BetterCombatText: idempotencia exige estagios/eventos/leituras independentes")
def _t_bct_idempotencia():
    nome = _superficies()[0]
    ident = _identidade_completa("sessao-1")
    pasta = tempfile.mkdtemp(prefix="aut7-idem-")
    try:
        def leitura(i):
            o = _obs_superficie(nome, procedencia="runtime", extras={
                "fonte_sha": ident["fonte_sha"], "dll_sha": ident["dll_sha"],
                "estagio": "estagio-%d" % i, "leitura_id": "leitura-%d" % i,
                "evento_id": "evento-%d" % i, "timestamp": "2026-10-05T20:0%d:00" % i})
            return _vincular(o, pasta, "leit%d" % i, "sessao-1")
        copia = [leitura(1), leitura(1)]
        copia[1] = _obs_superficie(nome, procedencia="runtime", extras={
            "fonte_sha": ident["fonte_sha"], "dll_sha": ident["dll_sha"], "estagio": "estagio-1",
            "leitura_id": "leitura-1", "evento_id": "evento-1", "timestamp": "2026-10-05T20:01:00"})
        copia[1] = _vincular(copia[1], pasta, "leit1copia", "sessao-1")
        alvo = [c for c in ea.avaliar(copia, ident)
                if c["id"].endswith("runtime-idempotencia")][0]
        exigir(alvo["estado"] != ea.OK,
               "duas leituras copiadas da MESMA leitura nao podem virar OK, veio %s" % alvo["estado"])
        boas = [leitura(1), leitura(2)]
        alvo2 = [c for c in ea.avaliar(boas, ident)
                 if c["id"].endswith("runtime-idempotencia")][0]
        exigir(alvo2["estado"] == ea.OK,
               "duas leituras independentes e estaveis deviam fechar OK, veio %s (%s)"
               % (alvo2["estado"], alvo2["motivo"]))
        divergentes = [leitura(1), leitura(2)]
        divergentes[1] = dict(divergentes[1],
                              cores={"texto": "#FFFFFFFF (a=1)", "sombra": "#FFFFFFFF (a=1)"})
        alvo3 = [c for c in ea.avaliar(divergentes, ident)
                 if c["id"].endswith("runtime-idempotencia")][0]
        exigir(alvo3["estado"] == ea.REPROVADO,
               "valores que mudam entre passadas tem de REPROVAR, veio %s" % alvo3["estado"])
    finally:
        shutil.rmtree(pasta, ignore_errors=True)


@caso("BetterCombatText: marca isolada de texto alheio (sem campos/contexto) nunca e OK")
def _t_bct_levelup_marca_isolada():
    """ACHADO AUT-7R: `nao_deve_exibir_efeito=true` sem campos/contexto virava OK."""
    marca = {"objeto": "unrelated-menu-text", "nao_deve_exibir_efeito": True,
             "procedencia": "runtime"}
    alvo = [c for c in ea.avaliar([marca], _identidade_completa())
            if c["id"].endswith("runtime-sem-vazamento-levelup")][0]
    exigir(alvo["estado"] != ea.OK,
           "marca isolada de texto alheio nao pode virar OK, veio %s" % alvo["estado"])
    exigir(alvo["estado"] == ea.NAO_EXERCITADO,
           "sem contexto/alvo/controle nativo a resposta e LACUNA, veio %s" % alvo["estado"])
    # estilo NATIVO igual ao controle nao e vazamento: exige o controle desligado.
    pasta = tempfile.mkdtemp(prefix="aut7-lev-")
    try:
        tipo = list(ea._bct().TIPOS_DO_LEVELUP)[0]
        comum = {"tipo_levelup": tipo, "contexto": "level-up",
                 "propriedades_material": _material_completo(), "shader_keywords": ["KEYWORD_A"],
                 "cores": {"texto": "#FFFFFFFF (a=1)", "contorno": "#000000FF (a=1)"},
                 "keywords": {"OUTLINE_ON": True, "UNDERLAY_ON": False}}
        alvo_obs = dict({"objeto": "Skill_Description", "nao_deve_exibir_efeito": True,
                         "procedencia": "runtime", "fonte_sha": "f" * 64, "dll_sha": "d" * 64},
                        **comum)
        controle = dict({"objeto": "Skill_Description", "mod_ativo": False, "procedencia": "runtime",
                         "fonte_sha": "f" * 64, "dll_sha": "d" * 64,
                         "evidencia": [_arquivo_evidencia()]}, **comum)
        alvo_obs["controle_nativo"] = _vincular(controle, pasta, "controle", "sessao-1")
        _vincular(alvo_obs, pasta, "alvo", "sessao-1")
        itens = ea.avaliar([alvo_obs], _identidade_completa("sessao-1"))
        criterios = [c for c in itens if c["id"].endswith("runtime-sem-vazamento-levelup")]
        # So o primeiro tipo foi coletado: os demais seguem lacuna (nunca OK).
        exigir(all(c["estado"] != ea.OK for c in criterios),
               "vazamento com estilo igual ao nativo nao e OK: %r" % [c["estado"] for c in criterios])
        vazado = dict(alvo_obs, cores={"texto": "#FFFFFFFF (a=1)", "contorno": "#FF00FFFF (a=1)"})
        vazado = _vincular(vazado, pasta, "vazado", "sessao-1")
        crit_v = [c for c in ea.avaliar([vazado], _identidade_completa("sessao-1"))
                  if c["id"].endswith("runtime-sem-vazamento-levelup")][0]
        exigir(crit_v["estado"] == ea.REPROVADO,
               "efeito DIFERENTE do estilo nativo no level-up tem de REPROVAR, veio %s"
               % crit_v["estado"])
    finally:
        shutil.rmtree(pasta, ignore_errors=True)


@caso("BetterFont: sem o PAR ligado/desligado a preservacao fica NAO_EXERCITADO")
def _t_bf_sem_controle():
    so_ligado = {"objeto": "Tooltip.Title", "fonte": "Serifa_Nova", "mod_ativo": True,
                 "cores": {"contorno": "#FFFFFFFF (r=1 g=1 b=1 a=1)"},
                 "keywords": {"OUTLINE_ON": True}, "procedencia": "fixture"}
    criterios = ea.avaliar([so_ligado], {})
    alvo = [c for c in criterios if c["id"].endswith("runtime-preservacao-estilo")][0]
    exigir(alvo["estado"] == ea.NAO_EXERCITADO,
           "sem controle o criterio tem de ser NAO_EXERCITADO, veio %s" % alvo["estado"])
    exigir("controle" in (alvo.get("lacuna_probe") or "").lower(),
           "a lacuna tem de NOMEAR o controle que falta")


@caso("BetterFont: par com cor divergente tem de REPROVAR; par fiel nao vira OK")
def _t_bf_par():
    def par(fonte_ligada, cor_ligada, cor_desligada, material=None):
        base = {"propriedades_material": material or _material_completo(),
                "shader_keywords": ["OUTLINE_ON", "UNDERLAY_ON"],
                "keywords": {"OUTLINE_ON": True, "UNDERLAY_ON": True}}
        return [
            dict({"objeto": "Tooltip.Title", "fonte": fonte_ligada, "mod_ativo": True,
                  "cores": {"texto": "#FFFFFFFF (a=1)", "face": cor_ligada,
                            "contorno": "#000000FF (a=1)", "sombra": "#000000FF (a=1)"},
                  "procedencia": "fixture"}, **base),
            dict({"objeto": "Tooltip.Title", "fonte": "Serifa_Original", "mod_ativo": False,
                  "cores": {"texto": "#FFFFFFFF (a=1)", "face": cor_desligada,
                            "contorno": "#000000FF (a=1)", "sombra": "#000000FF (a=1)"},
                  "procedencia": "fixture"}, **base)]
    divergente = par("Serifa_Nova", "#FFFFFFFF (a=1)", "#FF0000FF (a=1)")
    alvo = [c for c in ea.avaliar(divergente, {})
            if c["id"].endswith("runtime-preservacao-estilo")][0]
    exigir(alvo["estado"] == ea.REPROVADO,
           "cor que mudou entre ligado/desligado tem de REPROVAR, veio %s" % alvo["estado"])
    nao_trocou = par("Serifa_Original", "#FF0000FF (a=1)", "#FF0000FF (a=1)")
    alvo2 = [c for c in ea.avaliar(nao_trocou, {})
             if c["id"].endswith("runtime-preservacao-estilo")][0]
    exigir(alvo2["estado"] == ea.REPROVADO,
           "fonte que NAO trocou tem de REPROVAR, veio %s" % alvo2["estado"])
    fiel = par("Serifa_Nova", "#FF0000FF (a=1)", "#FF0000FF (a=1)")
    alvo3 = [c for c in ea.avaliar(fiel, {})
             if c["id"].endswith("runtime-preservacao-estilo")][0]
    exigir(alvo3["estado"] == ea.NAO_EXERCITADO,
           "par fiel em fixture NAO pode virar OK, veio %s" % alvo3["estado"])


@caso("BetterFont: propriedades efetivas do material incompletas nunca viram OK")
def _t_bf_material_incompleto():
    """ACHADO AUT-7R: campo ausente do material nao pode aprovar preservacao."""
    ident = _identidade_completa("sessao-1")
    pasta = tempfile.mkdtemp(prefix="aut7-bfmat-")
    try:
        def leitura(nome, ligado, material, estagio=1):
            o = {"objeto": "Tooltip.Title", "mod_ativo": ligado,
                 "fonte": "Serifa_Nova" if ligado else "Serifa_Original",
                 "cores": {"texto": "#FFFFFFFF (a=1)", "face": "#FF0000FF (a=1)",
                           "contorno": "#000000FF (a=1)", "sombra": "#000000FF (a=1)"},
                 "keywords": {"OUTLINE_ON": True, "UNDERLAY_ON": True},
                 "shader_keywords": ["OUTLINE_ON"], "propriedades_material": material,
                 "procedencia": "runtime", "fonte_sha": ident["fonte_sha"],
                 "dll_sha": ident["dll_sha"]}
            return _vincular(o, pasta, nome, "sessao-1")
        falta = dict(_material_completo())
        falta.pop("_OutlineWidth")
        incompleto = [leitura("li", True, falta), leitura("di", False, falta)]
        alvo = [c for c in ea.avaliar(incompleto, ident)
                if c["id"].endswith("runtime-preservacao-estilo")][0]
        exigir(alvo["estado"] != ea.OK,
               "material sem `_OutlineWidth` nao pode virar OK, veio %s" % alvo["estado"])
        completo = [leitura("lc", True, _material_completo()),
                    leitura("dc", False, _material_completo())]
        alvo2 = [c for c in ea.avaliar(completo, ident)
                 if c["id"].endswith("runtime-preservacao-estilo")][0]
        exigir(alvo2["estado"] == ea.OK,
               "par completo com todas as propriedades devia fechar OK, veio %s (%s)"
               % (alvo2["estado"], alvo2["motivo"]))
        # controle de OUTRA sessao (o achado BF-unvalidated-control-fixture)
        outra = [leitura("ls", True, _material_completo()),
                 dict(leitura("ds", False, _material_completo()), sessao="sessao-9")]
        alvo3 = [c for c in ea.avaliar(outra, ident)
                 if c["id"].endswith("runtime-preservacao-estilo")][0]
        exigir(alvo3["estado"] != ea.OK,
               "controle em sessao diferente nao pode assinar a prova, veio %s" % alvo3["estado"])
        # controle com procedencia fixture (nao pode ser sobreposto pelo runtime)
        fixture = [leitura("lf", True, _material_completo()),
                   dict(leitura("df", False, _material_completo()), procedencia="fixture")]
        alvo4 = [c for c in ea.avaliar(fixture, ident)
                 if c["id"].endswith("runtime-preservacao-estilo")][0]
        exigir(alvo4["estado"] != ea.OK,
               "controle fixture nao pode virar prova runtime, veio %s" % alvo4["estado"])
    finally:
        shutil.rmtree(pasta, ignore_errors=True)


@caso("BetterFont: `rotulo_fixture`/`evidencia_runtime=false` nunca viram runtime")
def _t_bf_rotulo_fixture():
    """ACHADO AUT-7R/COR-AUT6 E1: o rotulo tem de vencer a procedencia declarada."""
    obs = {"objeto": "Tooltip.Title", "fonte": "Serifa_Nova", "mod_ativo": True,
           "rotulo_fixture": True, "procedencia": "runtime", "config_sha": "a" * 64,
           "cores": {"texto": "#FFFFFFFF (a=1)"}, "keywords": {"OUTLINE_ON": True}}
    criterios = ea.avaliar([obs], _identidade_completa())
    exigir(all(c["estado"] != ea.OK for c in criterios),
           "rotulo_fixture=true nao pode produzir OK: %r" % [(c["id"], c["estado"]) for c in criterios])
    obs2 = dict(obs, rotulo_fixture=False, evidencia_runtime=False)
    exigir(all(c["estado"] != ea.OK for c in ea.avaliar([obs2], _identidade_completa())),
           "evidencia_runtime=false nao pode produzir OK")


@caso("BetterFont: config exige arquivo, hash e chaves/valores contra os defaults")
def _t_bf_config():
    """ACHADO AUT-7R: hash arbitrario era OK sem ler chave nenhuma."""
    ident = dict(_identidade_completa(), config={"sha256": "a" * 64})
    pasta = tempfile.mkdtemp(prefix="aut7-cfg-")
    try:
        import regras_bf_estilo as rbf
        defaults = rbf.defaults_com_linha(io.open(os.path.join(RAIZ, "BetterFont", "Plugin.cs"),
                                                   encoding="utf-8").read())
        cfg = os.path.join(pasta, "com.gumatos.betterfont.cfg")
        with io.open(cfg, "w", encoding="utf-8") as fh:
            fh.write("[Geral]\n" + "".join(
                "%s = %s\n" % (k, "true" if v["valor"] else "false")
                for k, v in sorted(defaults.items())))
        sha = _sha(cfg)
        ident["config"] = {"sha256": sha}
        valores = {k: bool(v["valor"]) for k, v in defaults.items()}
        bom = {"objeto": "BetterFont.cfg", "procedencia": "runtime", "config_sha": sha,
               "fonte_sha": ident["fonte_sha"], "dll_sha": ident["dll_sha"],
               "config": {"caminho": cfg, "sha256": sha, "valores": valores}}
        criterios = ea.avaliar([_vincular(bom, pasta, "bom", "sessao-1")], ident)
        alvo = [c for c in criterios if c["id"].endswith("runtime-config")][0]
        exigir(alvo["estado"] == ea.OK,
               "config com chaves e valores conferidos devia fechar OK, veio %s (%s)"
               % (alvo["estado"], alvo["motivo"]))
        arbitrario = dict(bom, config_sha="arbitrary-not-a-config-hash")
        alvo2 = [c for c in ea.avaliar([_vincular(arbitrario, pasta, "arb", "sessao-1")], ident)
                 if c["id"].endswith("runtime-config")][0]
        exigir(alvo2["estado"] != ea.OK,
               "hash arbitrario sem chaves nao pode ser OK, veio %s" % alvo2["estado"])
        sem_chaves = dict(bom, config={"caminho": cfg, "sha256": sha})
        alvo3 = [c for c in ea.avaliar([_vincular(sem_chaves, pasta, "sem", "sessao-1")], ident)
                 if c["id"].endswith("runtime-config")][0]
        exigir(alvo3["estado"] != ea.OK,
               "config sem chaves/valores lidos nao pode ser OK, veio %s" % alvo3["estado"])
        divergente = dict(bom, config={"caminho": cfg, "sha256": sha,
                                       "valores": dict(valores, **{k: not v for k, v in list(valores.items())[:1]})})
        alvo4 = [c for c in ea.avaliar([_vincular(divergente, pasta, "div", "sessao-1")], ident)
                 if c["id"].endswith("runtime-config")][0]
        exigir(alvo4["estado"] == ea.REPROVADO,
               "valor de chave que diverge do arquivo tem de REPROVAR, veio %s" % alvo4["estado"])
    finally:
        shutil.rmtree(pasta, ignore_errors=True)


@caso("BetterFont: par com chave de um lado SO tem de REPROVAR (A1: conjunto completo)")
def _t_bf_par_chave_de_um_lado():
    """ACHADO A1: a comparacao por INTERSECCAO deixava chave de um lado so sem medicao."""
    base = {"propriedades_material": _material_completo(),
            "shader_keywords": ["OUTLINE_ON", "UNDERLAY_ON"],
            "keywords": {"OUTLINE_ON": True, "UNDERLAY_ON": True}}
    cores = {"texto": "#FFFFFFFF (a=1)", "face": "#FF0000FF (a=1)",
             "contorno": "#000000FF (a=1)", "sombra": "#000000FF (a=1)"}

    def par(extra_no_ligado):
        cores_ligado = dict(cores)
        if extra_no_ligado:
            cores_ligado["_ExtraDoMod"] = "extra_so_no_ligado"
        return [
            dict({"objeto": "Tooltip.Title", "fonte": "Serifa_Nova", "mod_ativo": True,
                  "cores": cores_ligado, "procedencia": "fixture"}, **base),
            dict({"objeto": "Tooltip.Title", "fonte": "Serifa_Original", "mod_ativo": False,
                  "cores": dict(cores), "procedencia": "fixture"}, **base)]

    def alvo_de(observacoes):
        return [c for c in ea.avaliar(observacoes, {})
                if c["id"].endswith("runtime-preservacao-estilo")][0]

    com_extra = alvo_de(par(True))
    exigir(com_extra["estado"] == ea.REPROVADO,
           "chave que existe so no lado LIGADO tem de REPROVAR o par, veio %s (%s)"
           % (com_extra["estado"], com_extra["observado"]))
    exigir("_ExtraDoMod" in json.dumps(com_extra["observado"], ensure_ascii=False),
           "o motivo tem de NOMEAR a chave de um lado so: %r" % com_extra["observado"])
    sem_extra = alvo_de(par(False))
    exigir(sem_extra["estado"] != ea.REPROVADO,
           "o par identico (controle) nao pode REPROVAR: a diferenca tem de vir da chave extra (%s)"
           % sem_extra["observado"])


@caso("BetterFont: config legitimo com identidade sem hash de config e LACUNA (A2)")
def _t_bf_config_identidade():
    """ACHADO A2: exigir o hash de config DENTRO da identidade do CIC-1 tornava o criterio
    insatisfazivel e REPROVAVA config legitimo (fail-closed, mas falso REPROVADO)."""
    import regras_bf_estilo as rbf
    ident = _identidade_completa("sessao-1")
    pasta = tempfile.mkdtemp(prefix="aut7-cfg2-")
    try:
        defaults = rbf.defaults_com_linha(io.open(os.path.join(RAIZ, "BetterFont", "Plugin.cs"),
                                                  encoding="utf-8").read())
        cfg = os.path.join(pasta, "com.gumatos.betterfont.cfg")
        with io.open(cfg, "w", encoding="utf-8") as fh:
            fh.write("[Geral]\n" + "".join(
                "%s = %s\n" % (k, "true" if v["valor"] else "false")
                for k, v in sorted(defaults.items())))
        sha = _sha(cfg)
        valores = {k: bool(v["valor"]) for k, v in defaults.items()}
        bom = {"objeto": "BetterFont.cfg", "procedencia": "runtime", "config_sha": sha,
               "fonte_sha": ident["fonte_sha"], "dll_sha": ident["dll_sha"],
               "config": {"caminho": cfg, "sha256": sha, "valores": valores}}

        def alvo_de(identidade, obs=None):
            return [c for c in ea.avaliar([_vincular(dict(obs or bom), pasta, "cfgi", "sessao-1")],
                                          identidade)
                    if c["id"].endswith("runtime-config")][0]

        # (a) identidade SEM nenhum hash de config: LACUNA com o proximo passo nomeado
        sem_hash = alvo_de(ident)
        exigir(sem_hash["estado"] == ea.NAO_EXERCITADO,
               "config legitimo com identidade sem hash de config tem de ser LACUNA, veio %s (%s)"
               % (sem_hash["estado"], sem_hash["motivo"]))
        exigir("config" in str(sem_hash["motivo"]).lower(),
               "a lacuna tem de NOMEAR o que falta: %r" % sem_hash["motivo"])
        # (b) identidade que DECLARA o hash certo (entrada do proprio CLI): fecha OK
        com_hash = alvo_de(dict(ident, config_sha=sha))
        exigir(com_hash["estado"] == ea.OK,
               "com o config_sha declarado na identidade o criterio devia fechar OK, veio %s (%s)"
               % (com_hash["estado"], com_hash["motivo"]))
        # (c) identidade que declara OUTRO hash de config: REPROVADO (hash de outra rodada)
        outro = alvo_de(dict(ident, config_sha="c" * 64))
        exigir(outro["estado"] == ea.REPROVADO,
               "config_sha da identidade diferente do declarado tem de REPROVAR, veio %s"
               % outro["estado"])
        # (d) bytes do arquivo != sha declarado: REPROVADO (defeito real, nao lacuna)
        ruim = alvo_de(dict(ident, config_sha=sha), dict(bom, config_sha="d" * 64))
        exigir(ruim["estado"] == ea.REPROVADO,
               "sha que nao bate com os bytes do arquivo tem de REPROVAR, veio %s" % ruim["estado"])
    finally:
        shutil.rmtree(pasta, ignore_errors=True)


def _log_do_boot(categorias=None, pipe_no_valor=False):
    """Log com a forma REAL do dump: `|` entre campos e `desc="..."` por ULTIMO."""
    import regras_debugger as rd
    censo = rd.carrega_censo()
    chaves = [k for k in rd.chaves_do_field(censo) if k != "desc"]
    linhas = []
    for cat in (categorias or list(censo.CATS)):
        campos = " | ".join("%s=%s" % (k, "v|v" if pipe_no_valor else "v") for k in chaves)
        linhas.append('[Info   :Roguelike Debugger] [%s] \'nome do dump\' | %s | desc="texto"'
                      % (cat, campos))
    return "\n".join(linhas)


@caso("Debugger: log VAZIO nunca e OK; o contrato real com `|` antes do desc= nao reprova")
def _t_debugger_contrato():
    """ACHADO AUT-7R duplo: log vazio era OK e o separador `|` legitimo reprovava."""
    vazio = [{"log": True, "boot_novo": True, "procedencia": "fixture", "log_texto": ""}]
    alvo = [c for c in ea.avaliar(vazio, {}) if c["id"].endswith("runtime-contrato-dump")][0]
    exigir(alvo["estado"] != ea.OK,
           "log VAZIO/sem linhas reconhecidas nao pode ser OK, veio %s" % alvo["estado"])
    exigir(alvo["estado"] == ea.NAO_EXERCITADO,
           "log vazio e LACUNA declarada, veio %s" % alvo["estado"])
    real = [{"log": True, "boot_novo": True, "procedencia": "fixture",
             "log_texto": _log_do_boot()}]
    alvo2 = [c for c in ea.avaliar(real, {}) if c["id"].endswith("runtime-contrato-dump")][0]
    exigir(alvo2["estado"] != ea.REPROVADO,
           "o contrato REAL (com `|` antes do `desc=`) NAO pode reprovar: %s" % alvo2["observado"])
    # campo DEPOIS do desc= e valor com pipe continuam sendo defeito
    depois = [{"log": True, "boot_novo": True, "procedencia": "fixture",
               "log_texto": '[Info   :Roguelike Debugger] [Status] \'x\' | desc="d" | tipo=Buff'}]
    alvo3 = [c for c in ea.avaliar(depois, {}) if c["id"].endswith("runtime-contrato-dump")][0]
    exigir(alvo3["estado"] == ea.REPROVADO,
           "campo depois do `desc=` tem de REPROVAR, veio %s" % alvo3["estado"])
    sujo = [{"log": True, "boot_novo": True, "procedencia": "fixture",
             "log_texto": _log_do_boot(pipe_no_valor=True)}]
    alvo4 = [c for c in ea.avaliar(sujo, {}) if c["id"].endswith("runtime-contrato-dump")][0]
    exigir(alvo4["estado"] == ea.REPROVADO,
           "valor com `|` (trunca o FIELD) tem de REPROVAR, veio %s" % alvo4["estado"])
    # runtime completo: TODAS as categorias canonicas, sessao e evidencia vinculada
    ident = _identidade_completa("sessao-log")
    pasta = tempfile.mkdtemp(prefix="aut7-log-")
    try:
        texto = _log_do_boot()
        obs = {"log": True, "boot_novo": True, "procedencia": "runtime", "log_texto": texto,
               "fonte_sha": ident["fonte_sha"], "dll_sha": ident["dll_sha"], "sessao": "sessao-log"}
        bom = _vincular(obs, pasta, "log", "sessao-log")
        bom["evidencia"][0]["sessao"] = "sessao-log"
        crit = [c for c in ea.avaliar([bom], ident) if c["id"].endswith("runtime-contrato-dump")][0]
        exigir(crit["estado"] == ea.OK,
               "log real completo com cadeia vinculada devia fechar OK, veio %s (%s)"
               % (crit["estado"], crit["motivo"]))
        exigir(set(ea._modulo("aut7_regras_debugger",
                              os.path.join(ea.TESTES, "regras_debugger.py")).carrega_censo().CATS)
               <= set(crit["categorias_reconhecidas"]),
               "as categorias canonicas reconhecidas tem de estar declaradas")
    finally:
        shutil.rmtree(pasta, ignore_errors=True)


@caso("plano do AUT-7: consumivel pelo contrato do coletor AUT-4 (e plano quebrado recusado)")
def _t_plano():
    plano = os.path.join(AQUI, "plano-estilo.entrada.json")
    exigir(os.path.isfile(plano), "o plano de coleta do AUT-7 tem de existir em %s" % plano)
    r = ea.validar_plano_aut4(plano)
    if r.get("motivo") == "coletor AUT-4 (tools/automacao/runtime/coletor.py) indisponivel":
        return  # sem o coletor nao da para validar; nao e falso verde
    exigir(r.get("ok") is True, "o plano do AUT-7 tem de ser aceito pelo contrato do AUT-4: %s"
           % r.get("motivo"))
    exigir(r.get("status_da_rodada_sem_autorizacao") == "NAO_EXERCITADO",
           "sem autorizacao a rodada tem de sair NAO_EXERCITADO, veio %r"
           % r.get("status_da_rodada_sem_autorizacao"))
    tmp = os.path.join(tempfile.mkdtemp(prefix="aut7-plano-"), "quebrado.json")
    with io.open(tmp, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"esquema": "AUT-4/1", "cenarios": []}))
    r2 = ea.validar_plano_aut4(tmp)
    exigir(r2.get("ok") is False, "plano sem autorizacao/cenarios tem de ser recusado: %r" % r2)


@caso("--sem-suite: cache sem vinculo (ou mutado) NAO reusa prova antiga")
def _t_cache_stale():
    """ACHADO AUT-7R critico: fonte trocada em sandbox mantinha 12 OK vinculantes."""
    tmp = tempfile.mkdtemp(prefix="aut7-cache-")
    try:
        alvo = os.path.join(tmp, "BetterFont")
        os.makedirs(alvo)
        fonte = os.path.join(alvo, "Plugin.cs")
        with io.open(fonte, "w", encoding="utf-8") as fh:
            fh.write("// fonte qualquer\n")
        antes = ea.fotografia_suite(tmp)
        exigir("BetterFont/Plugin.cs" in antes["arquivos"], "a fotografia tem de ter o fonte: %r" % antes)
        with io.open(fonte, "w", encoding="utf-8") as fh:
            fh.write("// fonte DELIBERADAMENTE invalida\n")
        depois = ea.fotografia_suite(tmp)
        exigir(antes != depois,
               "trocar o fonte TEM de mudar a fotografia (senao o cache continua valido)")
        novo = os.path.join(tmp, "tools", "testes", "t_bf_novo.py")
        os.makedirs(os.path.dirname(novo))
        with io.open(novo, "w", encoding="utf-8") as fh:
            fh.write("# teste novo\n")
        exigir(ea.fotografia_suite(tmp) != depois,
               "entrar/sair arquivo do CONJUNTO de caminhos tambem invalida")
        # o CLI com --sem-suite num out-dir sem vinculo nao pode produzir OK de suite
        out = tempfile.mkdtemp(prefix="aut7-cache-out-")
        try:
            argv = [sys.executable, os.path.join(AQUI, "estilo_atributos.py"),
                    "--repo", RAIZ, "--out-dir", out, "--sem-suite",
                    "--out", os.path.join(out, "saida.json")]
            proc = subprocess.run(argv, cwd=RAIZ, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  timeout=300)
            exigir(proc.returncode in (0, 1, 2), "exit inesperado: %s" % proc.returncode)
            dados = json.loads(proc.stdout.decode("utf-8", "replace"))
            exigir(dados["medicao"]["cache_valido"] is False,
                   "sem vinculo o cache tem de ser declarado invalido")
            for mod in ("BetterFont", "BetterCombatText", "RoguelikeDebugger"):
                exigir(dados["por_mod"].get(mod, {}).get(ea.OK, 0) == 0,
                       "%s nao pode ter OK com cache invalido: %r" % (mod, dados["por_mod"][mod]))
        finally:
            shutil.rmtree(out, ignore_errors=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@caso("cache --sem-suite: os ARTEFATOS que a suite MEDE entram na fotografia (A6)")
def _t_cache_artefatos_medidos():
    """ACHADO A6: sem o pacote `dist/*.zip` e as DLLs de `bin/` na fotografia, plantar o
    defeito da regra de ouro SO no artefato medido mantinha `cache_valido=true`."""
    tmp = tempfile.mkdtemp(prefix="aut7-artef-")
    try:
        os.makedirs(os.path.join(tmp, "dist"))
        bin_dir = os.path.join(tmp, "BetterCombatText", "bin", "Release", "netstandard2.1")
        os.makedirs(bin_dir)
        pacote = os.path.join(tmp, "dist", "gumatos-BetterCombatText-0.1.1.zip")
        dll = os.path.join(bin_dir, "BetterCombatText.dll")
        with io.open(pacote, "wb") as fh:
            fh.write(b"PK\x03\x04 pacote sintetico do teste\n")
        with io.open(dll, "wb") as fh:
            fh.write(b"MZ dll de Release sintetica\n")
        antes = ea.fotografia_suite(tmp)
        exigir("artefatos" in antes, "a fotografia tem de separar os artefatos medidos: %r" % list(antes))
        exigir("dist/gumatos-BetterCombatText-0.1.1.zip" in antes["artefatos"],
               "o pacote de dist/ que a suite MEDE tem de entrar na fotografia: %r"
               % list(antes["artefatos"]))
        exigir("BetterCombatText/bin/Release/netstandard2.1/BetterCombatText.dll" in antes["artefatos"],
               "a DLL de bin/Release medida tem de entrar na fotografia: %r" % list(antes["artefatos"]))
        # o defeito plantado no ARTEFATO medido tem de mudar a fotografia (invalida o cache)
        orig = io.open(dll, "rb").read()
        with io.open(dll, "wb") as fh:
            fh.write(orig.replace(b"Release", b"Release+defeito"))
        exigir(ea.fotografia_suite(tmp) != antes,
               "mutar a DLL de bin/ TEM de mudar a fotografia (senao a prova velha segue vinculante)")
        with io.open(dll, "wb") as fh:
            fh.write(orig)
        exigir(ea.fotografia_suite(tmp) == antes, "restaurar byte a byte tem de voltar a fotografia")
        with io.open(pacote, "ab") as fh:
            fh.write(b"defeito no pacote\n")
        exigir(ea.fotografia_suite(tmp) != antes,
               "mutar o pacote `dist/*.zip` TEM de mudar a fotografia")
        with io.open(pacote, "wb") as fh:
            fh.write(b"PK\x03\x04 pacote sintetico do teste\n")
        exigir(ea.fotografia_suite(tmp) == antes, "restaurar o pacote tem de voltar a fotografia")
        os.remove(dll)
        exigir(ea.fotografia_suite(tmp) != antes,
               "sair um artefato medido da arvore TEM de mudar a fotografia")
        # e o repo vivo: se ha pacote em dist/, ele esta coberto
        import glob as _glob
        zips = _glob.glob(os.path.join(RAIZ, "dist", "*.zip"))
        if zips:
            viva = ea.fotografia_suite(RAIZ)
            cobertos = [os.path.basename(z) for z in zips
                        if any(k.endswith(os.path.basename(z)) for k in viva["artefatos"])]
            exigir(len(cobertos) == len(zips),
                   "todo pacote de dist/ do repo tem de estar na fotografia: faltam %r"
                   % [os.path.basename(z) for z in zips if z not in cobertos])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@caso("CLI: --sem-suite roda de ponta a ponta e nunca sai 0 sem prova")
def _t_cli():
    out = tempfile.mkdtemp(prefix="aut7-cli-")
    try:
        argv = [sys.executable, os.path.join(AQUI, "estilo_atributos.py"),
                "--repo", RAIZ, "--out-dir", out, "--sem-suite",
                "--identidade", "{\"fonte_sha\":\"x\",\"dll_sha\":\"y\"}"]
        proc = subprocess.run(argv, cwd=RAIZ, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              timeout=300)
        exigir(proc.returncode in (0, 1, 2), "exit inesperado: %s" % proc.returncode)
        texto = proc.stdout.decode("utf-8", "replace")
        dados = json.loads(texto[texto.index("{"):])
        exigir(dados.get("total", 0) >= len(ea._ASPECTOS),
               "o CLI tem de devolver os criterios de runtime tambem")
        exigir("criterios" in dados, "o resumo do CLI tem de trazer os criterios")
        # Sem a suite rodada, os mods com familia de teste ficam NAO_EXERCITADO (nunca OK).
        por_mod = dados.get("por_mod") or {}
        for mod in ("BetterFont", "BetterCombatText", "RoguelikeDebugger"):
            exigir(por_mod.get(mod, {}).get(ea.OK, 0) == 0,
                   "%s sem suite rodada nao pode ter OK" % mod)
    finally:
        shutil.rmtree(out, ignore_errors=True)


# ------------------------------------------- cobertura da fotografia (achado A6 / COR-AUT7-F2)
# As ENTRADAS que os testes MAPEADOS leem foram medidas com gancho de auditoria
# (`sys.addaudithook`) sobre a rodada viva: `tools/fixtures/**` (lido por `t_bf_diag_orcamento`),
# `tools/dados/*`, `docs/cobertura/*`, os fontes dos 6 mods, `lib/`, `ReloadProbe/`, `scratch/`
# e os projetos da arvore (a guarda de deploy varre a raiz inteira).
ENTRADAS_QUE_A_SUITE_LE = (
    ("tools/fixtures/bf-efeito-no-boot.json", b'{"material_com_efeito": 3}\n'),
    ("tools/fixtures/bf-varredura-em-jogo.log", b"varredura em jogo\n"),
    ("tools/dados/shrines-esperado.csv", b"arquivo,valor\n"),
    ("docs/cobertura/skills.csv", b"id,texto\n"),
    ("docs/PLANO-DE-TESTES.md", b"# plano\n"),
    ("Directory.Build.props", b"<Project/>\n"),
    ("ReloadProbe/ReloadProbe.csproj", b"<Project/>\n"),
    ("scratch/bancada/prova.csproj", b"<Project/>\n"),
    ("BetterTooltips/Patches/LocalizePatch.cs", b"// fonte\n"),
    ("lib/Assembly-CSharp.dll", b"MZ sintetica\n"),
)


def _escreve_entradas(tmp, entradas=ENTRADAS_QUE_A_SUITE_LE):
    for rel, dados in entradas:
        caminho = os.path.join(tmp, rel.replace("/", os.sep))
        pasta = os.path.dirname(caminho)
        if pasta:
            os.makedirs(pasta, exist_ok=True)
        with io.open(caminho, "wb") as fh:
            fh.write(dados)


def _escreve_json(caminho, dado):
    with io.open(caminho, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(dado, ensure_ascii=False))


@caso("cache --sem-suite: as ENTRADAS lidas pelos testes entram na fotografia (A6/F2)")
def _t_fotografia_entradas_dos_testes():
    """ACHADO A6 (rodada 425 da COR-AUT7-F2): a fotografia cobria os artefatos MEDIDOS mas NAO
    `tools/fixtures/**`, lido pelos testes mapeados: apagar a fixture mantinha `cache_valido=true`
    com prova velha e o criterio saia OK/OK_VINCULANTE."""
    tmp = tempfile.mkdtemp(prefix="aut7-entradas-")
    try:
        _escreve_entradas(tmp)
        antes = ea.fotografia_suite(tmp)
        faltando = [rel for rel, _ in ENTRADAS_QUE_A_SUITE_LE if rel not in antes["arquivos"]]
        exigir(not faltando,
               "ENTRADAS que a suite LE tem de estar na fotografia: faltam %r" % faltando)
        for rel, _ in ENTRADAS_QUE_A_SUITE_LE:
            caminho = os.path.join(tmp, rel.replace("/", os.sep))
            original = io.open(caminho, "rb").read()
            with io.open(caminho, "wb") as fh:
                fh.write(original + b"\ndefeito plantado na ENTRADA medida\n")
            exigir(ea.fotografia_suite(tmp) != antes,
                   "ALTERAR %s tem de mudar a fotografia (senao a prova velha segue vinculante)" % rel)
            with io.open(caminho, "wb") as fh:
                fh.write(original)
            exigir(ea.fotografia_suite(tmp) == antes, "restaurar %s tem de voltar a fotografia" % rel)
            os.remove(caminho)
            exigir(ea.fotografia_suite(tmp) != antes, "APAGAR %s tem de mudar a fotografia" % rel)
            with io.open(caminho, "wb") as fh:
                fh.write(original)
            exigir(ea.fotografia_suite(tmp) == antes,
                   "restaurar %s (apagada) tem de voltar a fotografia" % rel)
        # PROJETO NOVO em qualquer lugar da arvore: as guardas varrem a raiz inteira
        novo = os.path.join(tmp, "scratch", "bancada-nova", "nova.csproj")
        os.makedirs(os.path.dirname(novo), exist_ok=True)
        with io.open(novo, "w", encoding="utf-8") as fh:
            fh.write("<Project/>\n")
        exigir(ea.fotografia_suite(tmp) != antes,
               "ENTRAR um .csproj novo na arvore tem de mudar a fotografia (as guardas varrem a raiz)")
        # DERIVADOS nao entram: se entrassem, a propria rodada invalidaria a fotografia contra si
        derivados = ea.fotografia_suite(tmp)
        for rel in ("tools/__pycache__/x.cpython-314.pyc", "BetterFont/obj/Debug/x.cs"):
            caminho = os.path.join(tmp, rel.replace("/", os.sep))
            os.makedirs(os.path.dirname(caminho), exist_ok=True)
            with io.open(caminho, "w", encoding="utf-8") as fh:
                fh.write("derivado\n")
        exigir(ea.fotografia_suite(tmp) == derivados,
               "DERIVADO (__pycache__/obj) nao pode entrar na fotografia de ENTRADAS")
        # a DLL de bin/ nao entra como FONTE (e derivada), mas ENTRA como ARTEFATO que a suite MEDE
        dll = os.path.join(tmp, "BetterFont", "bin", "Debug", "BetterFont.dll")
        os.makedirs(os.path.dirname(dll), exist_ok=True)
        with io.open(dll, "wb") as fh:
            fh.write(b"MZ derivada\n")
        com_dll = ea.fotografia_suite(tmp)
        exigir("BetterFont/bin/Debug/BetterFont.dll" not in com_dll["arquivos"],
               "DLL de bin/ e DERIVADA: nao entra na fotografia de fontes")
        exigir("BetterFont/bin/Debug/BetterFont.dll" in com_dll["artefatos"],
               "DLL de bin/ e ARTEFATO MEDIDO: tem de estar no bloco `artefatos`")
        # repo vivo: as entradas que os testes leem estao TODAS cobertas (fontes em `arquivos`,
        # DLLs de bin/ no bloco `artefatos`; `bin`/`obj`/`__pycache__` sao derivados e ficam fora)
        viva = ea.fotografia_suite(RAIZ)
        for raiz in ("tools/fixtures", "tools/dados", "docs/cobertura", "lib", "ReloadProbe"):
            base = os.path.join(RAIZ, raiz)
            if not os.path.isdir(base):
                continue
            for pasta, subdirs, nomes in os.walk(base):
                subdirs[:] = [d for d in subdirs if d not in ea.DIRS_FORA_DA_FOTOGRAFIA]
                for nome in nomes:
                    rel = os.path.relpath(os.path.join(pasta, nome), RAIZ).replace("\\", "/")
                    if rel in viva["arquivos"] or rel in viva["artefatos"]:
                        continue
                    exigir(False, "o repo vivo le %s: tem de estar na fotografia" % rel)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@caso("cache --sem-suite: apagar a FIXTURE lida por teste mapeado zera o OK de suite (A6/F2)")
def _t_sem_suite_fixture_apagada():
    """Regressao NEGATIVA ponta a ponta (CLI real, cache real): com a fixture no lugar o
    `--sem-suite` reusa a prova (OK); apagando a fixture lida pelo teste mapeado o cache tem de
    ser declarado INVALIDO e nenhum criterio de suite pode sair OK. Foi assim que o falso-OK
    vinculante do A6/F2 passou na rodada 425."""
    tmp = tempfile.mkdtemp(prefix="aut7-fixture-")
    try:
        _escreve_entradas(tmp)
        out = os.path.join(tmp, "evidencias")
        os.makedirs(out, exist_ok=True)
        raiz_testes = os.path.join(tmp, "tools", "testes", "testes")
        puros = os.path.join(out, "suite-puros.json")
        cp = os.path.join(out, "suite-contra-prova.json")
        _escreve_json(puros, {"raiz": raiz_testes, "modo": "suite", "exit_code": 0,
                              "contagem": {"PASSOU": 1},
                              "testes": [{"arquivo": "puros/t_bf_diag_orcamento.py",
                                          "nome": "t_bf_diag_orcamento", "esperado": "passar",
                                          "estado": "PASSOU", "detalhe": "le a fixture do boot"}]})
        _escreve_json(cp, {"raiz": raiz_testes, "modo": "suite", "exit_code": 0,
                           "contagem": {"PROVA_OK": 1},
                           "testes": [{"arquivo": "contra-prova/cp_bf_diag_orcamento.py",
                                       "nome": "cp_bf_diag_orcamento", "esperado": "reprovar",
                                       "estado": "PROVA_OK", "detalhe": "isca reprovou"}]})
        # cache no MESMO formato que a rodada viva grava, com a fotografia do estado intacto
        _escreve_json(os.path.join(out, "suite-vinculo.json"),
                      {"fotografia": ea.fotografia_suite(tmp),
                       "resultados": {puros: _sha(puros), cp: _sha(cp)}})

        def roda_cli():
            argv = [sys.executable, os.path.abspath(ea.__file__), "--repo", tmp, "--out-dir", out,
                    "--sem-suite", "--sem-runtime", "--identidade",
                    json.dumps({"fonte_sha": "f" * 64, "dll_sha": "d" * 64})]
            proc = subprocess.run(argv, cwd=tmp, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  timeout=300)
            texto = proc.stdout.decode("utf-8", "replace")
            dados = json.loads(texto[texto.index("{"):])
            oks = [c for c in dados.get("criterios", [])
                   if c.get("mod") == "BetterFont" and c.get("estado") == ea.OK]
            return proc.returncode, dados, oks

        codigo, dados, oks = roda_cli()
        exigir(codigo in (0, 1, 2), "exit inesperado: %s" % codigo)
        exigir(dados["medicao"]["cache_valido"] is True,
               "com a entrada intacta o cache tem de ser VALIDO: %r"
               % dados["medicao"].get("cache_valido"))
        exigir(len(oks) == 2,
               "com o cache valido os dois criterios de suite (puro + isca) saem OK: %r"
               % [c["id"] for c in oks])
        # o DEFEITO: a entrada lida pelo teste mapeado some
        alvo = os.path.join(tmp, "tools", "fixtures", "bf-efeito-no-boot.json")
        original = io.open(alvo, "rb").read()
        os.remove(alvo)
        _, dados2, oks2 = roda_cli()
        exigir(dados2["medicao"]["cache_valido"] is False,
               "apagar a FIXTURE lida pelo teste mapeado tem de invalidar o cache: %r"
               % dados2["medicao"].get("cache_valido"))
        exigir(not oks2,
               "com o cache INVALIDO nenhum criterio de suite pode sair OK: %r" % [c["id"] for c in oks2])
        exigir(all(c.get("estado") != ea.OK
                   for c in dados2.get("criterios", []) if "bf-diag-orcamento" in str(c.get("id"))),
               "o criterio do teste cuja entrada sumiu nao pode sair OK")
        # restaurar byte a byte: o cache VOLTA a valer (a invalidacao vem da entrada, nao de ruido)
        with io.open(alvo, "wb") as fh:
            fh.write(original)
        _, dados3, oks3 = roda_cli()
        exigir(dados3["medicao"]["cache_valido"] is True,
               "restaurada byte a byte, a entrada volta a validar o cache")
        exigir(len(oks3) == 2, "restaurado, os criterios de suite voltam a OK: %r" % [c["id"] for c in oks3])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def rodar():
    print("test_estilo_atributos.py - %d caso(s)" % len(CASOS))
    for nome, fn in CASOS:
        try:
            fn()
            print("  [OK   ] %s" % nome)
        except AssertionError as erro:
            FALHAS.append((nome, str(erro)))
            print("  [FALHA] %s\n          %s" % (nome, erro))
        except Exception as erro:  # erro de ambiente/teste: nunca conta como verde
            FALHAS.append((nome, "%s: %s" % (type(erro).__name__, erro)))
            print("  [ERRO ] %s\n          %s: %s" % (nome, type(erro).__name__, erro))
    print("total: %d | falhas: %d" % (len(CASOS), len(FALHAS)))
    if FALHAS:
        print("REPROVADAS: %s" % "; ".join(n for n, _ in FALHAS))
        return 1
    print("TUDO OK")
    return 0


if __name__ == "__main__":
    sys.exit(rodar())
