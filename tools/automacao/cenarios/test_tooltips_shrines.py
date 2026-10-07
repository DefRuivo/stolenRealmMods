#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_tooltips_shrines.py - CIC-4: testes OFFLINE (positivos + CONTROLES NEGATIVOS) do avaliador.

O QUE ESTE ARQUIVO PROVA (e o que NAO prova)
--------------------------------------------
Ele exercita `tooltips_shrines.avaliar()` contra fixtures versionadas e contra DEFEITOS
PLANTADOS (controle negativo): cada defeito tem o estado que o avaliador TEM de devolver, e um
avaliador que aprova tudo reprova aqui. **Fixture testa o AVALIADOR; fixture NAO prova runtime**
(`prova_runtime=False` e exit 2 no caminho so-fixture).

CONVENCAO (a mesma do repositorio): imprime `RESULTADO|<PASSOU|REPROVOU>|<nome>|<detalhe>`,
exit 0 = todos PASSOU, 1 = algum REPROVOU, 2 = nao conseguiu rodar (fixture/tabela ausente).

USO
---
    python tools/automacao/cenarios/test_tooltips_shrines.py
    python tools/automacao/cenarios/test_tooltips_shrines.py --isca   # planta defeito -> TEM de REPROVAR
"""

import argparse
import importlib.util
import json
import os
import sys
import traceback

AQUI = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(os.path.dirname(AQUI))
REPO = os.path.dirname(TOOLS)
FIX_POS = os.path.join(AQUI, "shrines-observacoes.exemplo.json")
FIX_NEG = os.path.join(AQUI, "shrines-controle-negativo.json")
FIX_CASOS = os.path.join(AQUI, "shrines-casos.json")

EXIT_OK, EXIT_FALHOU, EXIT_NAO_RODOU = 0, 1, 2

ESTADOS = ("OK", "REPROVADO", "NAO_EXERCITADO", "INDETERMINADO")
CAMPOS_CRITERIO = ("id", "mod", "estado", "classe", "procedencia", "esperado", "observado",
                   "evidencia", "motivo", "tarefa_origem")


class Falhou(Exception):
    pass


class NaoRodou(Exception):
    pass


def _carregar(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


_MOD = None


def mod():
    global _MOD
    if _MOD is None:
        _MOD = _carregar("tooltips_shrines_cic4", os.path.join(AQUI, "tooltips_shrines.py"))
    return _MOD


def _json(caminho):
    if not os.path.isfile(caminho):
        raise NaoRodou("fixture ausente: %s" % caminho)
    with open(caminho, encoding="utf-8") as fh:
        return json.load(fh)


def exigir(cond, msg):
    if not cond:
        raise Falhou(msg)


# --------------------------------------------------------------- helpers (contrato runtime)

SHA = "ab" * 32
DLL = "cd" * 32
# ART: artefato REAL que existe no repo - usado como "o arquivo que foi lido" (evidencia).
ART = os.path.join("tools", "fixtures", "shrines-rv46-dedupe.log")

FEED_FULL = "\n".join([
    "[Info   :Better Tooltips] [Shrine RV-23] RV-31 acumulado: auras=[Rogue Aura] char=ChkRA bonus=0 -> Dodge +20% (total +37%)",
    "[Info   :Better Tooltips] [Shrine RV-23] RV-31 acumulado: auras=[Rogue Aura] char=Raven bonus=100 -> Dodge +40% (total +52%)",
    "[Info   :Better Tooltips] [Shrine RV-23] RV-31 acumulado: auras=[Dwarven Aura] char=ChkDW0 bonus=0 -> Stun chance +20%",
    "[Info   :Better Tooltips] [Shrine RV-23] RV-31 acumulado: auras=[Dwarven Aura] char=ChkDW20 bonus=20 -> Stun chance +24%",
    "[Info   :Better Tooltips] [Shrine RV-23] RV-31 acumulado: auras=[Dwarven Aura] char=ChkDW bonus=100 -> Stun chance +40%",
    "[Info   :Better Tooltips] [Shrine RV-23] RV-34 Flame alvo 'ChkGob': MaxHealth=200 tipo=Fodder bonus=100 dano=28",
])
FEED_RECEPTOR = ("[Info   :Better Tooltips] [Shrine RV-23] RV-31 acumulado: auras=[Rogue Aura] "
                 "char=ChkRA bonus=0 -> Dodge +20% (total +37%)")
ID_RECEPTOR = "S-dois-personagens-rogue/receptor/bonus=0"


def _ident_ok():
    return {"fonte_sha": SHA, "dll_sha": DLL}


def _rodada_runtime_completa(com_evidencia=True, com_hash=True, sessao="s1"):
    """Observacoes de uma rodada runtime COMPLETA (identificada). `com_evidencia=False` simula a
    rodada que NAO trouxe o artefato lido (correcao #9: nao pode fechar OK por rotulo) - os
    objetos tambem deixam de apontar para arquivo real, como no repro do CIC-4R."""
    base = {"procedencia": "runtime", "sessao": sessao}
    if com_hash:
        base["hash_fonte"] = DLL      # hash_fonte do coletor CIC-5 = sha da DLL -> casa com dll_sha
    ev = {"evidencia": [ART]} if com_evidencia else {}
    log = ART if com_evidencia else "LogOutput.log"
    regressao = (os.path.join("BetterTooltips", "Patches", "LocalizePatch.cs")
                 if com_evidencia else "FeedDeCombate")
    obs = [
        dict(base, objeto=log, feed=FEED_FULL, **ev),
        dict(base, objeto="Tooltip.LinhaAzul (ChkRA)", personagem="ChkRA", **ev,
             texto_renderizado="Your active shrine auras: Dodge +20% (total +37%)."),
        dict(base, objeto="Tooltip.LinhaAzul (Raven)", personagem="Raven", **ev,
             texto_renderizado="Your active shrine auras: Dodge +40% (total +52%)."),
        dict(base, objeto=regressao, **ev, texto_renderizado="Increased Armor Applied"),
    ]
    return obs


def _obs_receptor(**extra):
    """Superficie FEED do receptor (ChkRA), autenticada na rodada (sessao/hash/artefato)."""
    o = {"objeto": ART, "procedencia": "runtime", "sessao": "s1", "hash_fonte": DLL,
         "evidencia": [ART], "feed": FEED_RECEPTOR}
    o.update(extra)
    return o


def _obs_tooltip_receptor(**extra):
    """Superficie TOOLTIP (contra-prova) do receptor: MESMA sessao/hash/artefato do feed.

    Desde o COR-CIC4 (achados A/B do CIC-4R2) o criterio 'feed vs tooltip' so fecha OK com a
    segunda superficie EXISTINDO e AUTENTICADA - os testes de cadeia declaram as duas.
    """
    o = {"objeto": "Tooltip.LinhaAzul (ChkRA)", "personagem": "ChkRA",
         "procedencia": "runtime", "sessao": "s1", "hash_fonte": DLL, "evidencia": [ART],
         "texto_renderizado": "Your active shrine auras: Dodge +20% (total +37%)."}
    o.update(extra)
    return o


_DEC = None


def decisao():
    """`decisao.py` (CIC-2) como CONSUMIDOR do contrato - import so-leitura, para integrar a
    saida do avaliador no ciclo. Nunca editado por este arquivo."""
    global _DEC
    if _DEC is None:
        caminho = os.path.join(TOOLS, "automacao", "ciclo", "decisao.py")
        if not os.path.isfile(caminho):
            raise NaoRodou("decisao.py ausente: %s" % caminho)
        _DEC = _carregar("decisao_cic4", caminho)
    return _DEC


def _criterio(crits, cid):
    for c in crits:
        if c["id"] == cid:
            return c
    raise Falhou("criterio ausente: %s" % cid)


# --------------------------------------------------------------- casos POSITIVOS

def t_contrato():
    """`avaliar` devolve criterios com o contrato v1 completo e estados validos."""
    obs = _json(FIX_POS)
    crits = mod().avaliar(obs, {})
    exigir(isinstance(crits, list) and crits, "avaliar devolveu lista vazia")
    for c in crits:
        for campo in CAMPOS_CRITERIO:
            exigir(campo in c, "criterio %r sem o campo %r" % (c.get("id"), campo))
        exigir(c["estado"] in ESTADOS, "estado fora do contrato: %r" % c["estado"])
        exigir(isinstance(c["evidencia"], list), "evidencia tem de ser lista de caminhos")
        exigir(c["classe"] in ("offline", "runtime"), "classe invalida: %r" % c["classe"])
        exigir(c["procedencia"] in ("execucao", "runtime", "fixture"),
               "procedencia invalida: %r" % c["procedencia"])


def t_positivo_dois_personagens():
    """Dois personagens na MESMA aura: cada um OK com o PROPRIO bonus (nunca somado)."""
    crits = mod().avaliar(_json(FIX_POS), {})
    por = {c["id"]: c for c in crits}
    r0 = por.get("S-dois-personagens-rogue/receptor/bonus=0")
    r100 = por.get("S-dois-personagens-rogue/source/bonus=100")
    exigir(r0 and r0["estado"] == "OK", "receptor (bonus 0) nao OK: %r" % (r0 and r0["estado"]))
    exigir(r100 and r100["estado"] == "OK", "source (bonus 100) nao OK: %r" % (r100 and r100["estado"]))
    exigir(r0["esperado"]["valor"] == 20.0, "esperado do receptor != 20: %r" % r0["esperado"])
    exigir(r100["esperado"]["valor"] == 40.0, "esperado do source != 40: %r" % r100["esperado"])
    exigir(r0["observado"]["contrib"] == 20.0 and r100["observado"]["contrib"] == 40.0,
           "contribs observadas erradas")
    exigir(r0["observado"].get("feed_vs_tooltip") == "IGUAL",
           "feed vs tooltip do receptor nao conferido/igual")


def t_positivo_dwarven():
    """Aura de gatilho (sem atributo) em tres personagens: item proprio por personagem."""
    crits = mod().avaliar(_json(FIX_POS), {})
    for pid, val in (("chkdw0", 20.0), ("chkdw20", 24.0), ("chkdw", 40.0)):
        c = [x for x in crits if x["id"].startswith("S-dois-personagens-dwarven/" + pid + "/")][0]
        exigir(c["estado"] == "OK", "Dwarven %s nao OK: %s (%s)" % (pid, c["estado"], c["motivo"]))
        exigir(c["esperado"]["valor"] == val, "Dwarven %s esperado != %s: %r" % (pid, val, c["esperado"]))


def t_positivo_flame():
    """Aura de PERIGO: o dano do alvo bate com o ORACULO (regras_shrine.dano, eixo Source)."""
    crits = mod().avaliar(_json(FIX_POS), {})
    c = [x for x in crits if x["id"].startswith("S-perigo-flame/")][0]
    exigir(c["estado"] == "OK", "Flame nao OK: %s (%s)" % (c["estado"], c["motivo"]))
    exigir(c["esperado"]["valor"] == 28.0, "dano esperado do Flame != 28: %r" % c["esperado"])
    exigir(c["esperado"]["eixo"] == "Source", "eixo do Flame tem de ser Source (RV-30)")
    exigir(c["observado"]["dano"] == 28.0, "dano observado != 28")


def t_positivo_regressao_bug34():
    """Regressao BUG-34: FEED limpo -> OK e NAO reabre o bug (reabre_bug False)."""
    crits = mod().avaliar(_json(FIX_POS), {})
    c = [x for x in crits if x["id"].startswith("S-regressao-bug34-armor")][0]
    exigir(c["estado"] == "OK", "regressao BUG-34 nao OK: %s" % c["motivo"])
    exigir(c.get("reabre_bug") is False, "o criterio de regressao NAO pode reabrir o BUG-34")
    exigir(c.get("regressao_de") == "BUG-34", "criterio sem marca de regressao")


def t_fixture_nao_prova_runtime():
    """So fixture -> NENHUM criterio com prova_runtime e o CLI sai 2 (nunca verde por fixture)."""
    crits = mod().avaliar(_json(FIX_POS), {})
    exigir(all(not c["prova_runtime"] for c in crits),
           "fixture marcou prova_runtime=True")
    exigir(mod().exit_de(crits) == EXIT_NAO_RODOU,
           "exit de so-fixture tem de ser 2, veio %r" % mod().exit_de(crits))


def t_identidade_suficiente_aprova():
    """Observacao de RUNTIME com identidade suficiente, hash da DLL casando e as DUAS superficies
    autenticadas -> OK/prova_runtime."""
    obs = [_obs_receptor(), _obs_tooltip_receptor()]
    crits = mod().avaliar(obs, {"fonte_sha": SHA, "dll_sha": DLL})
    c = [x for x in crits if x["id"].startswith("S-dois-personagens-rogue/receptor")][0]
    exigir(c["estado"] == "OK" and c["prova_runtime"] is True,
           "runtime com identidade nao virou OK/prova_runtime: %s/%r" % (c["estado"], c["prova_runtime"]))


def t_esperado_rastreavel():
    """Todo criterio com esperado traz a FONTE (arquivo/linha) — nada de numero sem procedencia."""
    crits = mod().avaliar(_json(FIX_POS), {})
    for c in crits:
        if c["estado"] == "NAO_EXERCITADO" and c["esperado"] is None:
            continue
        exp = c.get("esperado") or {}
        exigir(isinstance(exp, dict) and exp.get("fonte"),
               "criterio %r sem fonte rastreavel no esperado" % c["id"])
        exigir(("tools/dados/" in exp["fonte"]) or ("KANBAN" in exp["fonte"])
               or ("regras_shrine" in exp["fonte"]) or ("RV-19" in exp["fonte"])
               or ("LocalizePatch" in exp["fonte"]),
               "fonte do esperado sem caminho do repositorio: %r" % exp["fonte"])


def t_sem_pedido_humano():
    """Lacuna tecnica NAO vira pedido humano: NAO_EXERCITADO diz o proximo passo TECNICO."""
    crits = mod().avaliar(_json(FIX_POS), {})
    proibidos = ("pergunt", "contate", "solicit", "peça", "peca ao dono", "usuario deve")
    for c in crits:
        if c["estado"] != "NAO_EXERCITADO":
            continue
        baixo = (c["motivo"] or "").lower()
        for p in proibidos:
            exigir(p not in baixo,
                   "NAO_EXERCITADO %r empurra tarefa automatizavel ao humano: %r" % (c["id"], c["motivo"]))


def t_runtime_completo_verde():
    """Rodada runtime COMPLETA (todas as superficies + identidade + evidencia lida) -> 7/7 OK e exit 0.

    E o par do `fixture-nao-prova-runtime`: prova que o avaliador CONSEGUE ficar verde quando o
    conjunto observado esta inteiro, identificado E com o ARTEFATO QUE FOI LIDO declarado como
    evidencia (correcao #9: sem artefato lido, o criterio nao fecha). Ver tambem
    `runtime-verde-integra-decisao`.
    """
    obs = _rodada_runtime_completa(com_evidencia=True)
    crits = mod().avaliar(obs, _ident_ok())
    cont = mod().resumo(crits)
    exigir(cont["OK"] == 7 and cont["REPROVADO"] == 0 and cont["NAO_EXERCITADO"] == 0,
           "rodada runtime completa nao deu 7 OK: %r" % cont)
    exigir(cont["com_prova_runtime"] == 7, "prova_runtime incompleta: %r" % cont)
    exigir(mod().exit_de(crits) == EXIT_OK, "exit de runtime completo tem de ser 0")


# --------------------------------------------------------------- #8/#9 — prova de contrato (RED)

def t_runtime_sem_evidencia_nao_aprova():
    """#8/#9 - rotulo `runtime` com identidade e hash casando MAS sem o artefato lido: NAO fecha OK.

    Este e o achado do CIC-4R: um conjunto 100% autoral rotulado runtime era vendido como prova.
    O contrato exige evidencia baseada no artefato realmente lido (correcao #9).
    """
    obs = _rodada_runtime_completa(com_evidencia=False)
    crits = mod().avaliar(obs, _ident_ok())
    c = _criterio(crits, ID_RECEPTOR)
    exigir(c is not None, "criterio do receptor ausente")
    exigir(c["estado"] != "OK", "runtime SEM evidencia fechou OK (evidence fingida): %s" % c["motivo"])
    exigir(c["prova_runtime"] is False, "runtime SEM evidencia marcou prova_runtime=True")
    exigir(not c["evidencia"], "evidencia inventada sem artefato lido: %r" % c["evidencia"])


def t_runtime_sem_hash_fonte_nao_aprova():
    """#8 (missinghash) - rotulo runtime, identidade suficiente, SEM `hash_fonte`: NAO amarra aos bytes."""
    obs = _rodada_runtime_completa(com_hash=False)
    crits = mod().avaliar(obs, _ident_ok())
    c = _criterio(crits, ID_RECEPTOR)
    exigir(c["estado"] == "NAO_EXERCITADO",
           "runtime sem hash_fonte devia ser NAO_EXERCITADO, veio %s (%s)" % (c["estado"], c["motivo"]))
    exigir(c["prova_runtime"] is False, "runtime sem hash_fonte marcou prova_runtime=True")


def t_runtime_hash_fonte_divergente_indeterminado():
    """#8/R-1 (mismatch) - hash_fonte (DLL) != dll_sha da rodada: INDETERMINADO, nunca OK."""
    sha = "ff" * 32
    obs = [{"objeto": ART, "procedencia": "runtime", "sessao": "s1", "evidencia": [ART],
            "hash_fonte": sha, "feed": FEED_RECEPTOR}]
    crits = mod().avaliar(obs, _ident_ok())
    c = _criterio(crits, ID_RECEPTOR)
    exigir(c["estado"] == "INDETERMINADO",
           "hash_fonte de outra build devia ser INDETERMINADO, veio %s" % c["estado"])
    exigir(c["prova_runtime"] is False, "hash divergente marcou prova_runtime=True")


def t_rotulo_ausente_nao_vira_runtime():
    """#8 - observacao SEM rotulo de procedencia NAO pode ser tratada como runtime por default."""
    obs = [{"objeto": ART, "sessao": "s1", "hash_fonte": DLL, "evidencia": [ART], "feed": FEED_RECEPTOR}]
    crits = mod().avaliar(obs, _ident_ok())
    c = _criterio(crits, ID_RECEPTOR)
    exigir(c["estado"] != "OK", "rotulo ausente virou runtime OK (default perigoso)")
    exigir(c["prova_runtime"] is False, "rotulo ausente marcou prova_runtime=True")


def t_contrato_procedencia_classe():
    """Contrato: procedencia no enum (execucao/runtime/fixture) e classe coerente com ela."""
    for obs, ident in ((_json(FIX_POS), {}),
                       (_rodada_runtime_completa(com_evidencia=True), _ident_ok()),
                       (_rodada_runtime_completa(com_evidencia=False), _ident_ok())):
        for c in mod().avaliar(obs, ident):
            exigir(c["procedencia"] in ("execucao", "runtime", "fixture"),
                   "%s: procedencia fora do contrato: %r" % (c["id"], c["procedencia"]))
            if c["procedencia"] == "runtime":
                exigir(c["classe"] == "runtime",
                       "%s: procedencia runtime exige classe runtime (veio %r)" % (c["id"], c["classe"]))
            else:
                exigir(c["classe"] in ("offline", "runtime"),
                       "%s: classe invalida %r" % (c["id"], c["classe"]))


def t_evidencia_vem_do_artefato_lido():
    """#9 - a evidencia do criterio runtime e o ARTEFATO LIDO, nao a tabela do esperado fingida."""
    obs = [_obs_receptor(), _obs_tooltip_receptor()]
    crits = mod().avaliar(obs, _ident_ok())
    c = _criterio(crits, ID_RECEPTOR)
    exigir(c["estado"] == "OK", "runtime completo com artefato deveria OK: %s" % c["motivo"])
    exigir(ART in c["evidencia"], "evidencia nao veio do artefato lido: %r" % c["evidencia"])
    exigir(all("shrines-esperado.csv" not in e for e in c["evidencia"]),
           "o CSV do esperado nao e evidencia da observacao: %r" % c["evidencia"])
    exigir(c.get("sessao") and c.get("fonte_sha") and c.get("dll_sha"),
           "criterio runtime OK sem cadeia (sessao/fonte_sha/dll_sha): %r" % c)


def t_hash_fonte_dll_casa_identidade():
    """R-1 (integracao com a coleta real): o `hash_fonte` do coletor CIC-5 e o sha256 da **DLL** do
    probe -> casa com o `dll_sha` da identidade, NAO com o `fonte_sha` (sha da fonte do repo). Uma
    observacao legitima de coleta real tem de fechar OK/prova_runtime."""
    obs = [_obs_receptor(), _obs_tooltip_receptor()]
    crits = mod().avaliar(obs, {"fonte_sha": SHA, "dll_sha": DLL})
    c = _criterio(crits, ID_RECEPTOR)
    exigir(c["estado"] == "OK" and c["prova_runtime"] is True,
           "hash_fonte(DLL) deveria casar com dll_sha e fechar OK: %s (%s)" % (c["estado"], c["motivo"]))


def t_hash_fonte_source_divergente_nao_aprova():
    """R-1 (inverso): o contrato NAO e `hash_fonte`==`fonte_sha`. Um hash da FONTE declarado em
    `hash_fonte` nao amarra a DLL medida -> nunca OK."""
    obs = [{"objeto": ART, "procedencia": "runtime", "sessao": "s1",
            "hash_fonte": SHA, "evidencia": [ART], "feed": FEED_RECEPTOR}]
    crits = mod().avaliar(obs, {"fonte_sha": SHA, "dll_sha": DLL})
    c = _criterio(crits, ID_RECEPTOR)
    exigir(c["estado"] != "OK", "hash da FONTE em hash_fonte virou OK (contrato errado): %s" % c["estado"])
    exigir(c["prova_runtime"] is False, "prova_runtime True com hash de fonte")


def t_criterio_propaga_fonte_e_dll_da_identidade():
    """Contrato: o criterio de runtime OK propaga `fonte_sha`/`dll_sha` DA IDENTIDADE (nao o
    `hash_fonte` da observacao), para o `decisao.py` confrontar contra a rodada."""
    obs = [_obs_receptor(), _obs_tooltip_receptor()]
    crits = mod().avaliar(obs, {"fonte_sha": SHA, "dll_sha": DLL})
    c = _criterio(crits, ID_RECEPTOR)
    exigir(c.get("fonte_sha") == SHA, "fonte_sha do criterio != identidade: %r" % c.get("fonte_sha"))
    exigir(c.get("dll_sha") == DLL, "dll_sha do criterio != identidade: %r" % c.get("dll_sha"))


# ------------------------------------------- A/B — a 2a superficie (COR-CIC4)

def _so_feed():
    """A rodada runtime COMPLETA sem as tooltips (achado A do CIC-4R2: so a superficie do FEED)."""
    return [o for o in _rodada_runtime_completa(com_evidencia=True) if not o.get("personagem")]


def t_sem_tooltip_nao_fecha_ok():
    """ACHADO A (CIC-4R2) — FEED completo, identificado e com artefato lido, mas SEM a segunda
    superficie: o criterio e 'feed vs tooltip' -> o que falta sai NAO_EXERCITADO, nunca OK.

    E o par do `runtime-completo-verde`: removida a TOOLTIP, o ciclo NAO pode fechar verde.
    """
    crits = mod().avaliar(_so_feed(), _ident_ok())
    c = _criterio(crits, ID_RECEPTOR)
    exigir(c["estado"] == "NAO_EXERCITADO",
           "rodada sem a superficie TOOLTIP devia NAO_EXERCITADO, veio %s (%s)"
           % (c["estado"], c["motivo"]))
    exigir(c["prova_runtime"] is False, "rodada sem tooltip marcou prova_runtime=True")
    exigir(c["observado"].get("feed_vs_tooltip") == "SEM_TOOLTIP",
           "observado sem a marca da superficie faltante: %r" % c["observado"])
    exigir(mod().exit_de(crits) != EXIT_OK, "exit da rodada sem tooltip nao pode ser 0")
    dec = decisao().consolidar(crits, {"fonte_sha": SHA, "dll_sha": DLL, "raiz": REPO})
    exigir(dec["por_mod"]["BetterTooltips"]["estado"] != "OK",
           "o ciclo fechou OK sem a segunda superficie: %r"
           % dec["por_mod"]["BetterTooltips"]["estado"])
    exigir(dec["resumo"]["ok_vinculantes"] < 7,
           "sem tooltip ainda vinculou 7 criterios: %r" % dec["resumo"])
    exigir(not dec["pendencias_humanas"],
           "a lacuna da segunda superficie virou pedido humano: %r" % dec["pendencias_humanas"])
    exigir(dec["falhas_automaticas"], "a lacuna nao voltou ao ciclo (fila de agente)")


def t_contra_prova_fixture_nao_autentica():
    """ACHADO B (CIC-4R2) — TOOLTIP `fixture` fecha a COMPARACAO e NAO o CRITERIO."""
    obs = _rodada_runtime_completa(com_evidencia=True)
    for o in obs:
        if o.get("personagem"):
            o["procedencia"] = "fixture"
            o["rotulo_fixture"] = "contra-prova-de-fixture"
    crits = mod().avaliar(obs, _ident_ok())
    c = _criterio(crits, ID_RECEPTOR)
    exigir(c["estado"] != "OK", "contra-prova de fixture fechou o criterio: %s" % c["estado"])
    exigir(c["prova_runtime"] is False, "contra-prova de fixture marcou prova_runtime=True")
    exigir(c["observado"].get("feed_vs_tooltip") == "IGUAL",
           "a comparacao das superficies deixou de ser medida: %r" % c["observado"])
    dec = decisao().consolidar(crits, {"fonte_sha": SHA, "dll_sha": DLL, "raiz": REPO})
    exigir(dec["por_mod"]["BetterTooltips"]["estado"] != "OK",
           "o ciclo fechou OK com contra-prova de fixture")


def t_contra_prova_outra_build_indeterminado():
    """ACHADO B — TOOLTIP de OUTRA build (hash divergente da identidade) nao autentica: INDETERMINADO."""
    obs = [_obs_receptor(), _obs_tooltip_receptor(hash_fonte="ff" * 32)]
    crits = mod().avaliar(obs, _ident_ok())
    c = _criterio(crits, ID_RECEPTOR)
    exigir(c["estado"] == "INDETERMINADO",
           "tooltip de outra build devia INDETERMINADO, veio %s (%s)" % (c["estado"], c["motivo"]))
    exigir(c["prova_runtime"] is False, "contra-prova de outra build marcou prova_runtime=True")


def t_contra_prova_outra_sessao_indeterminado():
    """ACHADO B — TOOLTIP de OUTRA sessao (mesma build) nao prova o mesmo ciclo: INDETERMINADO."""
    obs = [_obs_receptor(), _obs_tooltip_receptor(sessao="s9")]
    crits = mod().avaliar(obs, _ident_ok())
    c = _criterio(crits, ID_RECEPTOR)
    exigir(c["estado"] == "INDETERMINADO",
           "contra-prova de outra sessao devia INDETERMINADO, veio %s (%s)"
           % (c["estado"], c["motivo"]))
    exigir(c["prova_runtime"] is False, "contra-prova de outra sessao marcou prova_runtime=True")


def t_runtime_verde_integra_decisao():
    """Fiacao: rodada runtime ESTAVEL (7 OK com evidencia) fecha OK no `decisao.py` - sem mismatch."""
    crits = mod().avaliar(_rodada_runtime_completa(com_evidencia=True), _ident_ok())
    cont = mod().resumo(crits)
    exigir(cont["OK"] == 7 and cont["com_prova_runtime"] == 7,
           "rodada estavel nao deu 7 OK: %r" % cont)
    dec = decisao().consolidar(crits, {"fonte_sha": SHA, "dll_sha": DLL, "raiz": REPO})
    exigir(dec["por_mod"]["BetterTooltips"]["estado"] == "OK",
           "decisao nao fechou o mod OK: %r" % dec["por_mod"]["BetterTooltips"]["estado"])
    exigir(dec["resumo"]["ok_vinculantes"] == 7,
           "ok_vinculantes != 7: %r" % dec["resumo"])
    exigir(not dec["falhas_automaticas"], "rodada estavel gerou falha automatica: %r"
           % [f["id"] for f in dec["falhas_automaticas"]])


def t_runtime_sem_evidencia_integra_decisao():
    """#9 - a rodada SEM artefato lido NAO pode ficar verde nem no modulo NEM no ciclo (sem fingir)."""
    crits = mod().avaliar(_rodada_runtime_completa(com_evidencia=False), _ident_ok())
    exigir(mod().resumo(crits)["OK"] == 0, "rodada sem evidencia deu OK no modulo")
    dec = decisao().consolidar(crits, {"fonte_sha": SHA, "dll_sha": DLL, "raiz": REPO})
    exigir(dec["resumo"]["ok_vinculantes"] == 0,
           "rodada sem evidencia virou prova vinculante: %r" % dec["resumo"])
    exigir(dec["por_mod"]["BetterTooltips"]["estado"] != "OK",
           "rodada sem evidencia fechou OK no ciclo")


def t_lacuna_coleta_vai_pra_fila_nao_pro_dono():
    """Runtime field faltante = lacuna TECNICA (fila de agente), NAO autorizacao humana por default."""
    obs = [{"objeto": ART, "procedencia": "runtime", "sessao": "s1", "hash_fonte": DLL,
            "evidencia": [ART], "feed": "linha sem marcador [Shrine RV-23]"}]
    crits = mod().avaliar(obs, _ident_ok())
    dec = decisao().consolidar(crits, {"fonte_sha": SHA, "dll_sha": DLL, "raiz": REPO})
    exigir(dec["resumo"]["ok_vinculantes"] == 0, "lacuna de coleta virou prova: %r" % dec["resumo"])
    exigir(not dec["pendencias_humanas"],
           "lacuna de coleta virou pendencia humana (autorizacao default): %r"
           % [p.get("criterios") for p in dec["pendencias_humanas"]])
    exigir(dec["falhas_automaticas"], "lacuna de coleta nao voltou ao ciclo (fila de agente)")
    exigir(dec["por_mod"]["BetterTooltips"]["estado"] == "NAO_EXERCITADO",
           "mod com lacuna de coleta devia NAO_EXERCITADO, veio %r"
           % dec["por_mod"]["BetterTooltips"]["estado"])


# --------------------------------------------------------------- CONTROLE NEGATIVO

def _roda_negativos(trocar_espera=False):
    """Cada defeito plantado TEM de devolver o estado declarado. Devolve (falhas, total)."""
    neg = _json(FIX_NEG)
    falhas, total = [], 0
    for caso in neg["casos"]:
        crits = mod().avaliar(caso["observacoes"], caso.get("identidade") or {})
        por = {c["id"]: c for c in crits}
        for cid, esperado in caso["espera"].items():
            total += 1
            if trocar_espera and caso["id"].startswith("N1"):
                esperado = "OK"          # ISCA: o defeito N1 deveria ser pego; com a espera trocada
            got = (por.get(cid) or {}).get("estado")
            if got != esperado:
                falhas.append("%s: %s esperado=%s obtido=%s" % (caso["id"], cid, esperado, got))
    return falhas, total


def t_controle_negativo():
    """Os 9 defeitos plantados sao pegos com o estado certo (avaliador nao aprova tudo)."""
    falhas, total = _roda_negativos()
    exigir(total == 9, "esperava 9 controles negativos, rodei %d" % total)
    exigir(not falhas, "controle negativo NAO pego: " + "; ".join(falhas))


def t_isca_deve_reprovar():
    """Prova de fogo do PROPRIO teste: com a espera trocada, a comparacao TEM de falhar."""
    falhas, _ = _roda_negativos(trocar_espera=True)
    exigir(falhas, "a isca (espera trocada) NAO fez o teste falhar — o teste nao mede nada")


# --------------------------------------------------------------- runner

CASOS = [
    ("contrato-v1", t_contrato),
    ("positivo-dois-personagens", t_positivo_dois_personagens),
    ("positivo-dwarven", t_positivo_dwarven),
    ("positivo-flame-oraculo", t_positivo_flame),
    ("positivo-regressao-bug34", t_positivo_regressao_bug34),
    ("fixture-nao-prova-runtime", t_fixture_nao_prova_runtime),
    ("identidade-suficiente-aprova", t_identidade_suficiente_aprova),
    ("runtime-completo-verde", t_runtime_completo_verde),
    ("esperado-rastreavel", t_esperado_rastreavel),
    ("sem-pedido-humano", t_sem_pedido_humano),
    ("controle-negativo", t_controle_negativo),
    ("isca-teste-deve-reprovar", t_isca_deve_reprovar),
    # #8/#9 - prova de contrato runtime (redes de seguranca contra falso verde / evidence fingida)
    ("runtime-sem-evidencia-nao-aprova", t_runtime_sem_evidencia_nao_aprova),
    ("runtime-sem-hash-fonte-nao-aprova", t_runtime_sem_hash_fonte_nao_aprova),
    ("runtime-hash-divergente-indeterminado", t_runtime_hash_fonte_divergente_indeterminado),
    ("rotulo-ausente-nao-vira-runtime", t_rotulo_ausente_nao_vira_runtime),
    ("contrato-procedencia-classe", t_contrato_procedencia_classe),
    ("evidencia-vem-do-artefato-lido", t_evidencia_vem_do_artefato_lido),
    # R-1: hash_fonte (sha da DLL do coletor) casa com dll_sha, nunca com fonte_sha
    ("hash-fonte-dll-casa-identidade", t_hash_fonte_dll_casa_identidade),
    ("hash-fonte-source-divergente-nao-aprova", t_hash_fonte_source_divergente_nao_aprova),
    ("criterio-propaga-fonte-e-dll-da-identidade", t_criterio_propaga_fonte_e_dll_da_identidade),
    ("runtime-verde-integra-decisao", t_runtime_verde_integra_decisao),
    ("runtime-sem-evidencia-integra-decisao", t_runtime_sem_evidencia_integra_decisao),
    ("lacuna-coleta-vai-pra-fila", t_lacuna_coleta_vai_pra_fila_nao_pro_dono),
    # A/B (COR-CIC4): a segunda superficie (TOOLTIP) tem de existir E ser autenticada
    ("sem-tooltip-nao-fecha-ok", t_sem_tooltip_nao_fecha_ok),
    ("contra-prova-fixture-nao-autentica", t_contra_prova_fixture_nao_autentica),
    ("contra-prova-outra-build-indeterminado", t_contra_prova_outra_build_indeterminado),
    ("contra-prova-outra-sessao-indeterminado", t_contra_prova_outra_sessao_indeterminado),
]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Testes offline do avaliador CIC-4 shrines.")
    ap.add_argument("--isca", action="store_true",
                    help="planta defeito (espera trocada) -> a suite TEM de sair REPROVOU/exit 1")
    args = ap.parse_args(argv)

    rodaram, reprovaram, nao_rodaram = 0, 0, 0
    for nome, fn in CASOS:
        try:
            fn()
            print("RESULTADO|PASSOU|%s|ok" % nome)
            rodaram += 1
        except NaoRodou as e:
            print("RESULTADO|NAO_RODOU|%s|%s" % (nome, e))
            nao_rodaram += 1
        except Falhou as e:
            print("RESULTADO|REPROVOU|%s|%s" % (nome, e))
            reprovaram += 1
        except Exception:
            print("RESULTADO|REPROVOU|%s|excecao: %s" % (nome, traceback.format_exc()))
            reprovaram += 1

    if args.isca:
        # Modo isca: roda a comparacao dos controles negativos com a espera TROCADA. O teste
        # tem de DETECTAR a falha (a comparacao nao pode ser vacua).
        try:
            falhas, _ = _roda_negativos(trocar_espera=True)
        except Exception as e:  # noqa: BLE001
            print("ISCA|FALHA|excecao: %s" % e)
            return EXIT_FALHOU
        if falhas:
            print("ISCA|OK|defeito plantado detectado: %s" % "; ".join(falhas))
            return EXIT_OK
        print("ISCA|FALHA|com a espera trocada o teste NAO detectou falha (teste nao mede nada)")
        return EXIT_FALHOU

    print("TOTAL|rodaram=%d reprovaram=%d nao_rodaram=%d" % (rodaram, reprovaram, nao_rodaram))
    if reprovaram:
        return EXIT_FALHOU
    if nao_rodaram:
        return EXIT_NAO_RODOU
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
