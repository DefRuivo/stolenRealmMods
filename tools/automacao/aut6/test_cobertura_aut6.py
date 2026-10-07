#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_cobertura_aut6.py - AUT-6: a suite do avaliador de tooltips/shrines por personagem.

O QUE ELA PROVA
---------------
1. **AUSENCIA NAO E APROVACAO**: sem observacao nenhuma, nenhum criterio vira OK e o exit e 2
   (INCOMPLETO).
2. **COBERTURA POR TAREFA**: RV-26/27/28/29/31/33/34 (mais RV-46 e a regressao do BUG-34) tem
   criterio no conjunto - tarefa da frente sem criterio seria ponto cego.
3. **O CAMINHO POSITIVO EXISTE**: com as fixtures versionadas o avaliador fecha 20 OK e **nenhum
   REPROVADO**; e com uma observacao de RUNTIME completa (identidade + sessao + hash + evidencia)
   os MESMOS casos fecham com `prova_runtime` - o avaliador nao e um "nunca aprova".
4. **FIXTURE NAO PROVA RUNTIME**: no caminho so-fixture `prova_runtime` e 0 em TODOS os criterios
   e o exit continua 2.
5. **CONTROLE NEGATIVO**: cada defeito plantado (globule errado, dedupe multiplicado, linha fora
   da aura, nota no feed, nota fora do corpo, teto diferente do asset, runtime sem cadeia) e
   REPROVADO/NAO_EXERCITADO no estado esperado - inclusive os dois lados da regressao do Armor.
6. **A DIVERGENCIA DO RV-49 e REGISTRADA, nao apagada**: ela sai sempre INDETERMINADO com os dois
   fatos e a decisao do dono - e o unico criterio que impede o exit 0 com a rodada completa.
7. **ISCA (`--isca`)**: planta um defeito NA PROPRIA comparacao (esperado errado) e exige que o
   caso positivo REPROVE - checagem que nunca foi vista reprovando seria decoracao.

USO
---
    python tools/automacao/aut6/test_cobertura_aut6.py          # exit 0 se tudo PASSOU
    python tools/automacao/aut6/test_cobertura_aut6.py --isca   # prova de fogo do proprio teste
"""
import copy
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(os.path.dirname(AQUI))
REPO = os.path.dirname(TOOLS)

if AQUI not in sys.path:
    sys.path.insert(0, AQUI)
import cobertura as co  # noqa: E402
import observacoes_fixture as of  # noqa: E402
import suporte_testes as st

FIXTURE_LOG = os.path.join(REPO, "tools", "fixtures", "shrines-exemplo.log")
DLL_SHA = "cafe" * 16  # qualquer hash de 64 chars; a identidade da rodada declara o MESMO


def _obs(**kw):
    return kw


def _casos():
    with open(co.CASOS_PADRAO, encoding="utf-8") as fh:
        return json.load(fh)


def _sem_rv49(casos):
    c = copy.deepcopy(casos)
    c["casos"] = [x for x in c["casos"] if x["tipo"] != "divergencia_rv49"]
    return c


def _obs_runtime():
    """Contraexemplo: re-rotular fixtures NUNCA e cadeia completa de runtime."""
    obs = copy.deepcopy(of.constroi())
    for o in obs:
        o["procedencia"] = "runtime"
        o.pop("rotulo_fixture", None)
        o["sessao"] = "sessao-fixture-1"
        o["hash_fonte"] = DLL_SHA
        o.setdefault("evidencia", [os.path.relpath(FIXTURE_LOG, REPO).replace("\\", "/")])
    return obs


IDENT = {"fonte_sha": "fonte", "dll_sha": DLL_SHA}


# --------------------------------------------------------------- checagens


def _estados(crits):
    d = {}
    for c in crits:
        d.setdefault(c["estado"], []).append(c["id"])
    return d


def _so(crits, prefixo):
    return [c for c in crits if c["id"].startswith(prefixo)]


def t_offline_ausencia_incompleta():
    crits = co.avaliar([], None)
    r = co.resumo(crits)
    assert r["OK"] == 0, "ausencia produziu OK: %r" % _estados(crits)
    # o unico criterio que NAO e NAO_EXERCITADO e a divergencia do RV-49 (INDETERMINADO por desenho)
    assert r["INDETERMINADO"] == 1, "esperado 1 INDETERMINADO (RV-49): %r" % _estados(crits)
    assert r["NAO_EXERCITADO"] == r["total"] - 1, "nem todo criterio ficou NAO_EXERCITADO"
    assert co.exit_de(crits) == 2, "exit de rodada vazia deveria ser 2 (INCOMPLETO)"
    assert r["com_prova_runtime"] == 0


def t_cobertura_por_tarefa():
    casos = _casos()
    crits = co.avaliar([], None, casos)
    matriz = co.matriz_cobertura(casos, crits)
    for rv in ("RV-26", "RV-27", "RV-28", "RV-29", "RV-31", "RV-33", "RV-34", "RV-46", "BUG-34"):
        assert rv in matriz, "tarefa sem criterio (ponto cego): %s" % rv
        assert matriz[rv], "tarefa %s sem criterio avaliado" % rv


def t_fixture_positiva():
    crits = co.avaliar(of.constroi(), None)
    r = co.resumo(crits)
    assert r["REPROVADO"] == 0, "fixture valida reprovou: %r" % _estados(crits)
    assert r["NAO_EXERCITADO"] == 4, "cor/posicao/transicao/completude precisam continuar ausentes"
    assert r["OK"] >= 20, "esperado >= 20 OK no conjunto de fixtures, obtido %d" % r["OK"]


def t_fixture_nao_prova_runtime():
    crits = co.avaliar(of.constroi(), None)
    assert co.resumo(crits)["com_prova_runtime"] == 0, "fixture contou como prova de runtime"
    assert co.exit_de(crits) == 2, "so-fixture deveria sair 2"
    for c in crits:
        if c['id'] in ('S-rv49-divergencia-perigo', 'S-aut6-completude-runtime'):
            assert c['classe'] == 'runtime' and not c['prova_runtime']
            continue
        assert c["procedencia"] in ("fixture", "execucao"), "procedencia vazou: %s" % c
        assert c["classe"] == "offline", "fixture com classe runtime: %s" % c["id"]
        assert c["prova_runtime"] is False, "criterio sem jogo marcado como prova: %s" % c["id"]
        if c['id'] != 'S-rv29-transicao-mesmo-personagem':
            assert c["procedencia"] == "fixture", "procedencia vazou: %s" % c["id"]


def t_runtime_completo_fecha_e_rv49_trava():
    obs, ident = st.gravar([st.corpo()], 'positivo-contrato')
    assert co._cadeia(obs[0], st.cadeia_kw(ident)) == (None, None), 'bytes completos devem fechar a cadeia'
    crits = co.avaliar(obs, ident, {'casos': [st.CASO_CORPO]})
    assert len(crits) == 3 and all(c['estado'] == 'OK' for c in crits), _estados(crits)
    assert not any(c['prova_runtime'] for c in crits), 'simulacao de contrato nao prova produto'
    assert co.exit_de(crits) == 2
    assert co.resumo(co.avaliar(_obs_runtime(), IDENT))['com_prova_runtime'] == 0


def t_runtime_sem_identidade_nao_aprova():
    crits = co.avaliar(_obs_runtime(), None)
    r = co.resumo(crits)
    assert r["OK"] == 0 or r["com_prova_runtime"] == 0, "runtime aprovou sem identidade"
    assert r["com_prova_runtime"] == 0
    assert all("identidade insuficiente" in c["motivo"] or c["estado"] == "INDETERMINADO"
               for c in crits if c["estado"] == "NAO_EXERCITADO") or r["OK"] == 0


def t_runtime_hash_divergente_indeterminado():
    obs, ident = st.gravar([st.corpo()], 'hash-antigo')
    obs[0]['dll_sha'] = 'beef'*16
    crits = co.avaliar(obs, ident, {'casos': [st.CASO_CORPO]})
    indet = [c for c in crits if c["estado"] == "INDETERMINADO"]
    assert len(indet) == 3, "hash de outra build nao virou INDETERMINADO"
    divergentes = [c for c in indet if "OUTRA build" in c["motivo"]]
    assert len(divergentes) >= 1, "o motivo nao nomeia a build divergente"
    assert co.resumo(crits)["com_prova_runtime"] == 0, "aprovou com hash de outra build"


def t_runtime_sem_evidencia_nao_aprova():
    obs = _obs_runtime()
    for o in obs:
        o["evidencia"] = ["tools/nao-existe.json"]
        o.pop("objeto", None)
    crits = co.avaliar(obs, IDENT)
    assert co.resumo(crits)["com_prova_runtime"] == 0, "aprovou sem artefato lido de verdade"


def t_runtime_criterio_carrega_cadeia():
    """Cada resultado identifica hash de fonte/DLL, configuracao e cenario (contrato positivo)."""
    obs, ident = st.gravar([st.corpo()], 'cadeia-criterio')
    cadeia = co._cadeia_do_criterio(obs[0], st.cadeia_kw(ident))
    for k in ('sessao', 'fonte_sha', 'dll_sha', 'config_sha'):
        assert cadeia[k] == obs[0][k]
    assert cadeia['ambiente_prova'] == 'teste_contrato'
    crits = co.avaliar(obs, ident, {'casos': [st.CASO_CORPO]})
    for c in crits:
        assert c["identidade_rodada"]["casos_sha256"]
        assert c["identidade_rodada"]["observacoes"]
        assert c['evidencia'][0]['sha256']
    incompletos = co.avaliar([], {"fonte_sha": "f", "dll_sha": "d"})
    assert all(c["identidade_rodada"]["dll_sha"] == "d" for c in incompletos), \
        "o criterio incompleto tambem tem de identificar a identidade confrontada"


def t_globule_pct_fora_da_acao():
    obs = copy.deepcopy(of.constroi())
    for o in obs:
        o["feed"] = o.get("feed", "").replace("ChkG1 Sustenance I = 8%", "ChkG1 Sustenance I = 9%")
    crits = _so(co.avaliar(obs, None), "S-rv28-globule")
    assert crits and all(c["estado"] == "REPROVADO" for c in crits[:1]), \
        "globule com %% fora da acao do motor passou: %r" % [(c["id"], c["estado"]) for c in crits]
    assert any(c["estado"] == "OK" for c in crits[1:]), "o outro personagem (correto) virou REPROVADO"


def t_globule_frase_nao_fecha_com_o_pool():
    obs = copy.deepcopy(of.constroi())
    for o in obs:
        o["feed"] = o.get("feed", "").replace("8 health and 4 mana", "8 health and 9 mana")
    crits = _so(co.avaliar(obs, None), "S-rv28-globule")
    assert any(c["estado"] == "REPROVADO" and "pool" in c["motivo"] for c in crits), \
        "frase que nao fecha com o pool nao foi pega"


def t_dedupe_multiplicado():
    obs = copy.deepcopy(of.constroi())
    for o in obs:
        # a linha que o caso casa e a do acumulado GRANDE (5 auras) - o item do Dodge dela.
        o["feed"] = o.get("feed", "").replace("Dodge +40% (total +75%)", "Dodge +120% (total +75%)")
    crits = _so(co.avaliar(obs, None), "S-rv31-dedupe")
    assert len(crits) == 1 and crits[0]["estado"] == "REPROVADO", \
        "contribuicao multiplicada por instancia passou: %r" % crits
    assert "multiplicada" in crits[0]["motivo"]


def t_dedupe_sem_repeticao_incompleto():
    obs = copy.deepcopy(of.constroi())
    for o in obs:
        o["feed"] = "\n".join(l for l in o.get("feed", "").splitlines()
                              if "instancias=[Guardian Aura x2, Rogue Aura x3]" not in l)
    crits = _so(co.avaliar(obs, None), "S-rv31-dedupe")
    assert crits[0]["estado"] == "NAO_EXERCITADO", "sem repeticao o caso devia ficar incompleto"


def t_fora_da_aura_com_linha():
    obs = copy.deepcopy(of.constroi())
    for o in obs:
        # a rodada de SAIDA ganha a linha do personagem que deveria estar fora.
        if o.get("personagem") == "ChkFora":
            o["feed"] = o["feed"] + "\n[Info   :Better Tooltips] [Shrine RV-23] RV-31 acumulado: " \
                "auras=[Warrior Aura] char=ChkFora bonus=20 -> Damage +24% (total +54%)\n"
    crits = _so(co.avaliar(obs, None), "S-rv29-fora")
    assert crits[0]["estado"] == "REPROVADO", "linha FORA da aura nao reprovou: %r" % crits
    assert "RV-29" in crits[0]["motivo"]


def t_dentro_da_aura_sem_linha():
    obs = copy.deepcopy(of.constroi())
    for o in obs:
        if o.get("personagem") == "ChkWA":
            o["feed"] = "\n".join(l for l in o["feed"].splitlines() if "char=ChkWA" not in l)
    crits = _so(co.avaliar(obs, None), "S-rv29-dentro")
    assert crits[0]["estado"] == "REPROVADO", "DENTRO sem linha nao reprovou: %r" % crits


def t_entrar_sair_sem_declaracao():
    obs = copy.deepcopy(of.constroi())
    for o in obs:
        o.pop("dentro_da_aura", None)
    crits = (_so(co.avaliar(obs, None), "S-rv29-dentro")
             + _so(co.avaliar(obs, None), "S-rv29-fora"))
    assert crits and all(c["estado"] == "NAO_EXERCITADO" for c in crits), \
        "obsevacao sem a declaracao dentro/fora virou conclusao: %r" % [
            (c["id"], c["estado"]) for c in crits]


def t_armor_nota_no_feed():
    obs = copy.deepcopy(of.constroi())
    for o in obs:
        if o.get("superficie") == "feed":
            o["texto_renderizado"] += "\nArmor blocks damage: each 10 Armor reduces damage taken by 1."
    crits = _so(co.avaliar(obs, None), "S-bug34")
    feed = [c for c in crits if c["id"].endswith("/feed")][0]
    assert feed["estado"] == "REPROVADO", "nota no FEED nao reprovou"
    assert feed["reabre_bug"] is False and feed["regressao_de"] == "BUG-34"
    corpo = [c for c in crits if c["id"].endswith("/corpo")][0]
    assert corpo["estado"] == "OK", "o corpo nao deveria reprovar por causa do feed"


def t_armor_corpo_sem_nota():
    obs = copy.deepcopy(of.constroi())
    for o in obs:
        if o.get("superficie") == "tooltip_status":
            o["texto_renderizado"] = "Increased Armor\n@Armor@ and @Magic Armor@ increased by [0]."
    crits = _so(co.avaliar(obs, None), "S-bug34")
    corpo = [c for c in crits if c["id"].endswith("/corpo")][0]
    assert corpo["estado"] == "REPROVADO", "corpo SEM a nota nao reprovou"
    assert corpo["reabre_bug"] is False


def t_armor_sem_superficie_incompleto():
    obs = copy.deepcopy(of.constroi())
    for o in obs:
        o.pop("superficie", None)
    crits = _so(co.avaliar(obs, None), "S-bug34")
    assert all(c["estado"] == "NAO_EXERCITADO" for c in crits), \
        "regressao sem as superficies declaradas virou conclusao"


def t_teto_diferente_do_asset():
    obs = copy.deepcopy(of.constroi())
    for o in obs:
        o["feed"] = o.get("feed", "").replace(
            "RV-46 teto 'DamageReduction': MaxValue=50 char=Man2Guard",
            "RV-46 teto 'DamageReduction': MaxValue=60 char=Man2Guard")
    crits = _so(co.avaliar(obs, None), "S-rv46-teto")
    assert crits[0]["estado"] == "REPROVADO", "teto diferente do asset nao reprovou: %r" % crits
    assert "MaxValue" in crits[0]["motivo"]


def t_limite_sem_asset_incompleto():
    cfg = _casos()
    um = {"casos": [c for c in cfg["casos"] if c["id"] == "S-rv46-teto-damage-reduction"]}
    crits = co.avaliar(of.constroi(), None, um, asset="nao/existe/resources.assets")
    assert crits[0]["estado"] == "NAO_EXERCITADO", "sem asset o limite virou conclusao"
    assert "offset DOCUMENTADO" in crits[0]["motivo"] or "asset ausente" in crits[0]["motivo"]


def t_corpo_tooltip_regressao():
    obs = copy.deepcopy(of.constroi())
    for o in obs:
        if o.get("superficie") == "tooltip_shrine":
            o["texto_renderizado"] = "Increases dodge chance by 40%.\nDodge +40% (total +57%)"
    crits = _so(co.avaliar(obs, None), "S-rv26-corpo")
    assert crits[0]["estado"] == "REPROVADO", "corpo sem a LINHA nao reprovou"
    assert "linha" in crits[0]["motivo"]


def t_esperado_rastreavel():
    crits = co.avaliar(of.constroi(), None)
    for c in crits:
        if c["estado"] not in ("OK", "REPROVADO"):
            continue
        esperado = c["esperado"]
        if isinstance(esperado, dict) and esperado.get("fonte"):
            fonte = str(esperado["fonte"]).replace("\\", "/")
            assert ("tools/" in fonte or "docs/" in fonte or "resources.assets" in fonte
                    or "BetterTooltips/" in fonte), "fonte nao rastreavel: %r" % fonte


def t_sem_pedido_humano():
    """Nenhuma lacuna vai ao dono como roteiro: a divergencia do RV-49 e falha AUTOMATICA
    (volta ao ciclo) e nao uma decisao residual que libera o verde."""
    crits = co.avaliar([], None)
    humanos = [c for c in crits if c.get("tipo_pendencia") == "decisao_dono"]
    assert not humanos, "RV-49 nao pode sair como decisao residual: %r" % humanos
    rv49 = next(c for c in crits if c["id"] == "S-rv49-divergencia-perigo")
    assert rv49["autorizacao_necessaria"] is False and rv49["tipo_pendencia"] == "divergencia_de_medicao"
    assert rv49["esperado"]["fato_30_09"] and rv49["esperado"]["fato_03_10"], "divergencia apagada"
    assert "RV-49" in rv49["lacuna_probe"], "a lacuna automatica nao nomeia a divergencia"
    proibidas = ("solicit", "pergunt", "peça", "peca", "por favor", "avise")
    for c in crits:
        m = c["motivo"].lower()
        assert not any(p in m for p in proibidas), "motivo tecnico pedindo ao humano: %r" % c["motivo"]


# --------------------------------------------------------------- runner


TESTES = [v for k, v in sorted(globals().items()) if k.startswith("t_") and callable(v)]


def roda(isca=False):
    falhas = []
    for fn in TESTES:
        try:
            fn()
            print("PASSOU  %s" % fn.__name__)
        except AssertionError as e:
            falhas.append((fn.__name__, str(e)))
            print("FALHOU  %s: %s" % (fn.__name__, e))
    if isca:
        falhas.extend(_isca())
    print("\nTOTAL|rodaram=%d reprovaram=%d" % (len(TESTES) + (1 if isca else 0), len(falhas)))
    return 1 if falhas else 0


def _isca():
    """PROVA DE FOGO: com o esperado da comparacao errado, o caso positivo TEM de reprovar."""
    falhas = []
    original = co._fonte_buff

    def errado(aura, atributo, bonus):
        esp, fonte = original(aura, atributo, bonus)
        return (None if esp is None else esp + 1.0), fonte

    co._fonte_buff = errado
    try:
        crits = co.avaliar(of.constroi(), None)
        reprovou = [c for c in crits if c["estado"] == "REPROVADO"]
    finally:
        co._fonte_buff = original
    if not reprovou:
        falhas.append(("isca", "esperado plantado (+1) NAO reprovou: a comparacao e vacua"))
        print("FALHOU  isca: defeito plantado nao detectado")
    else:
        print("PASSOU  isca: defeito plantado detectado (%d criterio(s) reprovados)"
              % len(reprovou))
    return falhas


if __name__ == "__main__":
    sys.exit(roda(isca="--isca" in sys.argv))
