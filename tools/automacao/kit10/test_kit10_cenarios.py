#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_kit10_cenarios.py - testes OFFLINE do KIT-10 (positivos + CONTROLES NEGATIVOS + isca).

O QUE ESTE ARQUIVO PROVA (e o que NAO prova)
--------------------------------------------
Exercita `kit10_cenarios.avaliar()` contra cenarios FIXTURE e contra DEFEITOS PLANTADOS:
  * cada defeito tem o estado que o avaliador TEM de devolver (controle negativo);
  * um conjunto RUNTIME COMPLETO (identidade + sessao + hash + evidencia lida) fecha OK COM
    `prova_runtime=True` (prova que ele CONSEGUE ficar verde);
  * um conjunto sem a cadeia NAO fecha OK (runtime ausente nao recebe OK).
**Fixture testa o AVALIADOR; fixture NAO prova runtime.**

Convencao do repositorio: `RESULTADO|<PASSOU|REPROVOU>|<nome>|<detalhe>`, exit 0 = todos PASSOU,
1 = algum REPROVOU, 2 = nao conseguiu rodar (modulo/tabela ausente).

USO
---
    python tools/automacao/kit10/test_kit10_cenarios.py
    python tools/automacao/kit10/test_kit10_cenarios.py --isca   # planta defeito -> TEM de REPROVAR
"""

import argparse
import hashlib
import importlib.util
import json
import os
import sys
import tempfile
import traceback

AQUI = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(os.path.dirname(AQUI))
REPO = os.path.dirname(TOOLS)

EXIT_OK, EXIT_FALHOU, EXIT_NAO_RODOU = 0, 1, 2

SHA = "ab" * 32
DLL = "cd" * 32
ESTADOS = ("OK", "REPROVADO", "NAO_EXERCITADO", "INDETERMINADO")
CAMPOS_CRITERIO = ("id", "mod", "estado", "classe", "procedencia", "esperado", "observado",
                   "evidencia", "motivo", "tarefa_origem")


class Falhou(Exception):
    pass


class NaoRodou(Exception):
    pass


_MOD = None


def mod():
    global _MOD
    if _MOD is None:
        caminho = os.path.join(AQUI, "kit10_cenarios.py")
        if not os.path.isfile(caminho):
            raise NaoRodou("kit10_cenarios.py ausente: %s" % caminho)
        spec = importlib.util.spec_from_file_location("kit10_cenarios_t", caminho)
        _MOD = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_MOD)
    return _MOD


def exigir(cond, msg):
    if not cond:
        raise Falhou(msg)


_WS = None


def ws():
    global _WS
    if _WS is None:
        _WS = tempfile.mkdtemp(prefix="kit10-teste-")
    return _WS


def _com_cadeia(corpo, nome_arquivo):
    """Transforma um corpo de observacao FIXTURE numa observacao de RUNTIME com a CADEIA COMPLETA.

    A cadeia exigida pelo fechamento do AUT-7 (`_fecha` + `_vinculo_obs`): `procedencia=runtime`,
    `sessao`, `fonte_sha`/`dll_sha` batendo com a identidade, E a EVIDENCIA de um arquivo REAL que
    contenha a observacao (o artefato lido). Sem ela o criterio NAO fecha OK.
    """
    obs = dict(corpo)
    obs.update({"procedencia": "runtime", "sessao": "s1", "fonte_sha": SHA, "dll_sha": DLL})
    # O arquivo de evidencia contem a OBSERVACAO (sem o proprio campo `evidencia`), que e o que o
    # vinculo do fechamento do AUT-7 exige: o artefato lido tem de conter a observacao.
    caminho = os.path.join(ws(), nome_arquivo)
    with open(caminho, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(obs, fh, ensure_ascii=False, sort_keys=True)
    sha = hashlib.sha256(open(caminho, "rb").read()).hexdigest()
    obs["evidencia"] = [{"caminho": caminho, "sha256": sha, "sessao": "s1"}]
    return obs


def _ident():
    return {"fonte_sha": SHA, "dll_sha": DLL}


def _por_id(crits, prefixo):
    return [c for c in crits if c["id"].startswith(prefixo)]


# ------------------------------------------------------------------ A. contexto/dano

CORPO_A = {
    "tipo": "contexto_dano", "objeto": "flame-ground", "mod": "BetterTooltips",
    "aura_dano": "Flame Shrine Aura", "tipo_alvo": "Fodder", "maxhealth": 200,
    "dano_observado": 28, "fonte_bonus": 0, "receptor_bonus": 100,
    "aura_buff": "Rogue Aura", "atributo": "DodgeChance", "contrib_observada": 40,
}
ID_A = "KIT-10/shrines/contexto-dano-fonte-receptor/flame-ground"


def t_A_ok_runtime():
    """Ground effect: dano no eixo `Source` (bonus 0) + tooltip de buff no eixo `Target` do receptor."""
    obs = _com_cadeia(CORPO_A, "a-ok.json")
    crits = mod().avaliar([obs], _ident())
    c = _por_id(crits, ID_A)[0]
    exigir(c["estado"] == "OK", "A esperado OK, veio %s (%s)" % (c["estado"], c["motivo"]))
    exigir(c["prova_runtime"] is True, "A sem prova_runtime")
    exigir(c["esperado"]["dano_ground_effect"]["valor"] == 28.0, "dano esperado != 28: %r" % c["esperado"])
    exigir(c["esperado"]["dano_ground_effect"]["eixo"] == "Source", "eixo do dano != Source")
    exigir(c["esperado"]["tooltip_buff_do_receptor"]["valor"] == 40.0,
           "contrib do buff != 40: %r" % c["esperado"]["tooltip_buff_do_receptor"])


def t_A_defeito_source_injetado():
    """DEFEITO (RV-34): o bonus do jogador reinjetado em `Source` -> REPROVADO."""
    corpo = dict(CORPO_A, objeto="flame-fonte-injetada", fonte_bonus=100)
    obs = _com_cadeia(corpo, "a-def-fonte.json")
    crits = mod().avaliar([obs], _ident())
    c = _por_id(crits, "KIT-10/shrines/contexto-dano-fonte-receptor/flame-fonte-injetada")[0]
    exigir(c["estado"] == "REPROVADO", "defeito do Source injetado passou: %s (%s)" % (c["estado"], c["motivo"]))
    exigir(c["prova_runtime"] is False, "defeito marcou prova_runtime=True")


def t_A_defeito_dano_escalou_receptor():
    """DEFEITO: o dano do ground effect escalou com o bonus do RECEPTOR (eixo errado) -> REPROVADO."""
    corpo = dict(CORPO_A, objeto="flame-escalou", dano_observado=56)
    obs = _com_cadeia(corpo, "a-def-dano.json")
    crits = mod().avaliar([obs], _ident())
    c = _por_id(crits, "KIT-10/shrines/contexto-dano-fonte-receptor/flame-escalou")[0]
    exigir(c["estado"] == "REPROVADO", "dano escalando com o receptor passou: %s" % c["estado"])
    exigir("RECEPTOR" in c["motivo"] or "escalou" in c["motivo"], "motivo sem a causa: %r" % c["motivo"])


# ------------------------------------------------------------------ B. worship/dobro

CORPO_B = {
    "tipo": "worship_dobro", "objeto": "dobro-misto", "mod": "BetterTooltips",
    "vivas": [{"aura": "Dwarven Aura", "instancias": 2}, {"aura": "Rogue Aura", "instancias": 2}],
    "itens_observados": {"Dwarven Aura": 2, "Rogue Aura": 1},
}
ID_B = "KIT-10/shrines/worship-dobro-preservado/dobro-misto"


def t_B_ok_dobro_preservado():
    """Confirmado: gatilho conta POR INSTANCIA (2); atributo conta UMA vez (1). O dobro e preservado."""
    obs = _com_cadeia(CORPO_B, "b-ok.json")
    crits = mod().avaliar([obs], _ident())
    c = _por_id(crits, ID_B)[0]
    exigir(c["estado"] == "OK", "B esperado OK, veio %s (%s)" % (c["estado"], c["motivo"]))
    exigir(c["esperado"]["itens_por_aura"]["Dwarven Aura"] == 2,
           "gatilho deveria esperar 2 itens (dobro preservado): %r" % c["esperado"])
    exigir(c["esperado"]["itens_por_aura"]["Rogue Aura"] == 1,
           "atributo deveria esperar 1 item (RV-46): %r" % c["esperado"])


def t_B_defeito_dobro_removido():
    """DEFEITO: o dobro do gatilho REMOVIDO (2 instancias -> 1 item) -> REPROVADO. Regra do cartao."""
    corpo = dict(CORPO_B, objeto="dobro-removido")
    corpo["itens_observados"] = {"Dwarven Aura": 1, "Rogue Aura": 1}
    obs = _com_cadeia(corpo, "b-def.json")
    crits = mod().avaliar([obs], _ident())
    c = _por_id(crits, "KIT-10/shrines/worship-dobro-preservado/dobro-removido")[0]
    exigir(c["estado"] == "REPROVADO", "remover o dobro do gatilho passou: %s" % c["estado"])
    exigir("REMOV" in c["motivo"].upper(), "motivo sem a marca do dobro removido: %r" % c["motivo"])


# ------------------------------------------------------------------ C. estilo por evento

CORPO_C = {
    "tipo": "estilo_evento", "objeto": "BossHealthbar_Text", "componente": "TMP",
    "mod": "BetterCombatText", "estagio": "combate", "evento_id": "evt-7",
}
ID_C = "KIT-10/estilo/por-evento-nao-boot/BossHealthbar_Text"


def t_C_ok_evento():
    """Superficie canonica do BCT lida no EVENTO, nao no prefab de boot."""
    obs = _com_cadeia(CORPO_C, "c-ok.json")
    crits = mod().avaliar([obs], _ident())
    c = _por_id(crits, ID_C)[0]
    exigir(c["estado"] == "OK", "C esperado OK, veio %s (%s)" % (c["estado"], c["motivo"]))
    exigir("BossHealthbar" in c["observado"]["superficies"], "superficie canonica nao reconhecida")


def t_C_defeito_boot():
    """DEFEITO: superficie lida no PREFAB DE BOOT -> REPROVADO (o objeto de boot nao carrega o efeito)."""
    corpo = dict(CORPO_C, objeto="PlayerInfoWindow_Text", estagio="boot")
    obs = _com_cadeia(corpo, "c-def.json")
    crits = mod().avaliar([obs], _ident())
    c = _por_id(crits, "KIT-10/estilo/por-evento-nao-boot/PlayerInfoWindow_Text")[0]
    exigir(c["estado"] == "REPROVADO", "leitura de prefab de boot passou: %s" % c["estado"])
    exigir("boot" in c["motivo"], "motivo sem o estagio: %r" % c["motivo"])


def t_C_sem_evento_nao_ok():
    """Sem `estagio`/`evento_id` a leitura por evento NAO pode fechar OK -> NAO_EXERCITADO."""
    corpo = dict(CORPO_C, objeto="StatusIcon_Text")
    corpo.pop("estagio")
    corpo.pop("evento_id")
    obs = _com_cadeia(corpo, "c-sem-evento.json")
    crits = mod().avaliar([obs], _ident())
    c = _por_id(crits, "KIT-10/estilo/por-evento-nao-boot/StatusIcon_Text")[0]
    exigir(c["estado"] == "NAO_EXERCITADO", "sem evento deveria NAO_EXERCITADO, veio %s" % c["estado"])
    exigir(c["prova_runtime"] is False, "sem evento marcou prova_runtime=True")


# ------------------------------------------------------------------ guardas anti-FALSO-OK (KIT-10R)

def t_A_buff_fora_da_tabela_nao_ok():
    """F3 (KIT-10R): `aura_buff` fora da tabela de esperados -> tooltip NAO medida -> NAO_EXERCITADO."""
    corpo = dict(CORPO_A, objeto="a-buff-fora", aura_buff="Aura Que Nao Existe")
    obs = _com_cadeia(corpo, "a-buff-fora.json")
    crits = mod().avaliar([obs], _ident())
    c = _por_id(crits, "KIT-10/shrines/contexto-dano-fonte-receptor/a-buff-fora")[0]
    exigir(c["estado"] == "NAO_EXERCITADO",
           "buff fora da tabela fechou %s (%s)" % (c["estado"], c["motivo"]))
    exigir(c["prova_runtime"] is False, "buff fora da tabela marcou prova_runtime=True")


def t_A_contrib_ausente_nao_ok():
    """F3 (KIT-10R): buff na tabela mas `contrib_observada` ausente -> tooltip NAO medida -> NAO_EXERCITADO."""
    corpo = dict(CORPO_A, objeto="a-contrib-ausente")
    corpo.pop("contrib_observada")
    obs = _com_cadeia(corpo, "a-contrib-ausente.json")
    crits = mod().avaliar([obs], _ident())
    c = _por_id(crits, "KIT-10/shrines/contexto-dano-fonte-receptor/a-contrib-ausente")[0]
    exigir(c["estado"] == "NAO_EXERCITADO",
           "contrib ausente fechou %s (%s)" % (c["estado"], c["motivo"]))
    exigir(c["prova_runtime"] is False, "contrib ausente marcou prova_runtime=True")


def t_A_dano_ausente_nao_ok():
    """F5 (KIT-10R2): `dano_observado` AUSENTE -> dano NAO medido -> NAO_EXERCITADO (nunca OK)."""
    corpo = dict(CORPO_A, objeto="a-dano-ausente")
    corpo.pop("dano_observado")
    obs = _com_cadeia(corpo, "a-dano-ausente.json")
    c = _por_id(mod().avaliar([obs], _ident()), "KIT-10/shrines/contexto-dano-fonte-receptor/a-dano-ausente")[0]
    exigir(c["estado"] == "NAO_EXERCITADO",
           "dano ausente fechou %s (%s)" % (c["estado"], c["motivo"]))
    exigir(c["prova_runtime"] is False, "dano ausente marcou prova_runtime=True")
    exigir("dano" in c["motivo"], "motivo sem a causa do dano ausente: %r" % c["motivo"])


def t_A_receptor_ausente_nao_ok():
    """F6 (KIT-10R2): `receptor_bonus` AUSENTE -> eixo `Target` NAO exercitado -> NAO_EXERCITADO."""
    corpo = dict(CORPO_A, objeto="a-receptor-ausente")
    corpo.pop("receptor_bonus")
    obs = _com_cadeia(corpo, "a-receptor-ausente.json")
    c = _por_id(mod().avaliar([obs], _ident()), "KIT-10/shrines/contexto-dano-fonte-receptor/a-receptor-ausente")[0]
    exigir(c["estado"] == "NAO_EXERCITADO",
           "receptor ausente fechou %s (%s)" % (c["estado"], c["motivo"]))
    exigir(c["prova_runtime"] is False, "receptor ausente marcou prova_runtime=True")
    exigir("receptor_bonus" in c["motivo"], "motivo sem a causa do receptor ausente: %r" % c["motivo"])


def t_A_fonte_ausente_nao_ok():
    """F7 (KIT-10R2): `fonte_bonus` AUSENTE -> NAO_EXERCITADO (campo nao medido NAO e FALHOU)."""
    corpo = dict(CORPO_A, objeto="a-fonte-ausente")
    corpo.pop("fonte_bonus")
    obs = _com_cadeia(corpo, "a-fonte-ausente.json")
    c = _por_id(mod().avaliar([obs], _ident()), "KIT-10/shrines/contexto-dano-fonte-receptor/a-fonte-ausente")[0]
    exigir(c["estado"] == "NAO_EXERCITADO",
           "fonte ausente fechou %s (nao pode ser REPROVADO): %s" % (c["estado"], c["motivo"]))
    exigir(c["prova_runtime"] is False, "fonte ausente marcou prova_runtime=True")


def t_A_buff_ausente_nao_ok():
    """A tooltip do RECEPTOR e metade do aspecto: sem `aura_buff` ela NAO foi medida -> NAO_EXERCITADO."""
    corpo = dict(CORPO_A, objeto="a-buff-ausente")
    corpo.pop("aura_buff")
    obs = _com_cadeia(corpo, "a-buff-ausente.json")
    c = _por_id(mod().avaliar([obs], _ident()), "KIT-10/shrines/contexto-dano-fonte-receptor/a-buff-ausente")[0]
    exigir(c["estado"] == "NAO_EXERCITADO",
           "buff ausente fechou %s (%s)" % (c["estado"], c["motivo"]))
    exigir(c["prova_runtime"] is False, "buff ausente marcou prova_runtime=True")


def t_B_itens_ausentes_nao_ok():
    """F2 (KIT-10R): aura viva sem NENHUM item observado -> NAO_EXERCITADO (nunca OK)."""
    corpo = dict(CORPO_B, objeto="b-sem-itens", itens_observados={})
    obs = _com_cadeia(corpo, "b-sem-itens.json")
    crits = mod().avaliar([obs], _ident())
    c = _por_id(crits, ID_B.replace("dobro-misto", "b-sem-itens"))[0]
    exigir(c["estado"] == "NAO_EXERCITADO",
           "itens vazios fecharam %s (%s)" % (c["estado"], c["motivo"]))
    exigir(c["prova_runtime"] is False, "itens vazios marcaram prova_runtime=True")
    exigir(c["observado"]["sem_observacao"] == ["Dwarven Aura", "Rogue Aura"],
           "aura viva nao foi marcada como sem observacao: %r" % c["observado"].get("sem_observacao"))


def t_B_itens_parciais_nao_ok():
    """F2 (KIT-10R): UMA aura viva sem item observado ja basta -> NAO_EXERCITADO (nunca OK)."""
    corpo = dict(CORPO_B, objeto="b-parcial", itens_observados={"Dwarven Aura": 2})
    obs = _com_cadeia(corpo, "b-parcial.json")
    crits = mod().avaliar([obs], _ident())
    c = _por_id(crits, ID_B.replace("dobro-misto", "b-parcial"))[0]
    exigir(c["estado"] == "NAO_EXERCITADO",
           "item parcial fechou %s (%s)" % (c["estado"], c["motivo"]))
    exigir(c["prova_runtime"] is False, "item parcial marcou prova_runtime=True")


def t_C_estagio_desconhecido_nao_ok():
    """F1 (KIT-10R): `estagio` fora da whitelist de EVENTO (+ `evento_id`) -> NAO_EXERCITADO."""
    corpo = dict(CORPO_C, objeto="BossHealthbar_Text", estagio="banana", evento_id="evt-9")
    obs = _com_cadeia(corpo, "c-estagio-banana.json")
    crits = mod().avaliar([obs], _ident())
    c = _por_id(crits, ID_C)[0]
    exigir(c["estado"] == "NAO_EXERCITADO",
           "estagio inventado fechou %s (%s)" % (c["estado"], c["motivo"]))
    exigir(c["prova_runtime"] is False, "estagio inventado marcou prova_runtime=True")


# ------------------------------------------------------------------ D. debugger sem truncar

LINHA_OK = "[Info   :Roguelike Debugger] [Status] 'Foo' | tier=1 | desc=\"texto intacto\""
ID_D_OK = "KIT-10/debugger/sem-truncar/dump-ok"

CORPO_D_OK = {"tipo": "debugger_dump", "objeto": "dump-ok", "mod": "RoguelikeDebugger",
              "log_texto": LINHA_OK}


def t_D_ok_sem_truncar():
    """Linha de dump com `desc=` por ultimo, sem `|` em valor e DESC ancorada no fim."""
    obs = _com_cadeia(CORPO_D_OK, "d-ok.json")
    crits = mod().avaliar([obs], _ident())
    c = _por_id(crits, ID_D_OK)[0]
    exigir(c["estado"] == "OK", "D esperado OK, veio %s (%s)" % (c["estado"], c["motivo"]))
    exigir(c["observado"]["linhas_reconhecidas"] == 1, "linha nao reconhecida pelo censo")


def t_D_defeito_pipe_no_valor():
    """DEFEITO: valor com `|` trunca em silencio -> REPROVADO."""
    linha = "[Info   :Roguelike Debugger] [Status] 'Foo' | tags=a|b | desc=\"x\""
    obs = _com_cadeia({"tipo": "debugger_dump", "objeto": "dump-pipe", "log_texto": linha}, "d-pipe.json")
    crits = mod().avaliar([obs], _ident())
    c = _por_id(crits, "KIT-10/debugger/sem-truncar/dump-pipe")[0]
    exigir(c["estado"] == "REPROVADO", "valor com pipe passou: %s" % c["estado"])


def t_D_defeito_truncado():
    """DEFEITO: campo DEPOIS do `desc=` -> a descricao trunca -> REPROVADO."""
    linha = "[Info   :Roguelike Debugger] [Status] 'Foo' | desc=\"x\" | extra=1"
    obs = _com_cadeia({"tipo": "debugger_dump", "objeto": "dump-trunc", "log_texto": linha}, "d-trunc.json")
    crits = mod().avaliar([obs], _ident())
    c = _por_id(crits, "KIT-10/debugger/sem-truncar/dump-trunc")[0]
    exigir(c["estado"] == "REPROVADO", "desc seguido de campo passou: %s" % c["estado"])


# ------------------------------------------------------------------ reuso + contrato

def t_reuso_cic4_aut7():
    """O KIT-10 REUSA CIC-4 e AUT-7: os ids dos dois aparecem no conjunto de criterios."""
    crits = mod().avaliar([], {})
    ids = [c["id"] for c in crits]
    exigir(any(i.startswith("S-dois-personagens-rogue") for i in ids),
           "criterios do CIC-4 ausentes (reuso quebrado)")
    exigir(any(i.startswith("AUT-7/BetterStats/") for i in ids),
           "criterios do AUT-7 ausentes (reuso quebrado)")
    exigir(any(i.startswith("AUT-7/BetterCombatText/") for i in ids),
           "criterios do AUT-7/BCT ausentes (reuso quebrado)")


def t_contrato_campos():
    """Todo criterio do KIT-10 traz o contrato v1 e estados/procedencias validos."""
    obs = _com_cadeia(CORPO_A, "contrato-a.json")
    for c in mod().avaliar([obs], _ident()):
        for campo in CAMPOS_CRITERIO:
            exigir(campo in c, "criterio %r sem o campo %r" % (c.get("id"), campo))
        exigir(c["estado"] in ESTADOS, "estado fora do contrato: %r" % c["estado"])
        exigir(c["procedencia"] in ("execucao", "runtime", "fixture"), "procedencia invalida")
        exigir(isinstance(c["evidencia"], list), "evidencia tem de ser lista")


def t_esperado_rastreavel_kit10():
    """Todo criterio KIT-10 com esperado traz a FONTE do esperado (nada de numero sem procedencia)."""
    obs = [_com_cadeia(CORPO_A, "rast-a.json"), _com_cadeia(CORPO_B, "rast-b.json")]
    for c in mod().avaliar(obs, _ident()):
        if not c["id"].startswith("KIT-10/"):
            continue
        if c["estado"] == "NAO_EXERCITADO" and c["esperado"] is None:
            continue
        exp = c.get("esperado")
        exigir(exp is not None, "criterio %r sem esperado" % c["id"])
        # o esperado pode ser dict (A) ou dict-de-dicts (B/D); a fonte tem de estar em algum lugar
        texto = json.dumps(exp, ensure_ascii=False)
        exigir(any(x in texto for x in ("regras_shrine", "shrines-esperado", "shrines-percentuais",
                                        "RV-", "DWA-2", "census", "regras_debugger", "RV-46")),
               "esperado sem fonte rastreavel: %r" % exp)


# ------------------------------------------------------------------ runtime ausente nao recebe OK

def t_fixture_nao_prova_runtime():
    """Sem cadeia (observacao fixture) -> NENHUM criterio KIT-10 OK; exit 2 (nunca verde por fixture)."""
    obs = [dict(CORPO_A, objeto="fixture-a"), dict(CORPO_B, objeto="fixture-b"),
           dict(CORPO_C, objeto="fixture-c"), dict(CORPO_D_OK, objeto="fixture-d")]
    crits = mod().avaliar(obs, {})
    kit = [c for c in crits if c["id"].startswith("KIT-10/")]
    for c in kit:
        exigir(c["estado"] != "OK", "fixture fechou OK: %s (%s)" % (c["id"], c["motivo"]))
        exigir(c["prova_runtime"] is False, "fixture marcou prova_runtime=True: %s" % c["id"])
    exigir(mod().exit_de(crits) == EXIT_NAO_RODOU, "exit de so-fixture tem de ser 2")


# ------------------------------------------------------------------ CONTROLE NEGATIVO (agregado)

def _roda_negativos(trocar_espera=False):
    """Cada defeito plantado TEM de devolver REPROVADO. Devolve (falhas, total)."""
    casos = [
        ("N-A-source", lambda: _com_cadeia(dict(CORPO_A, objeto="n-a-fonte", fonte_bonus=100), "n-a.json")),
        ("N-A-dano", lambda: _com_cadeia(dict(CORPO_A, objeto="n-a-dano", dano_observado=56), "n-a2.json")),
        ("N-B-dobro", lambda: _com_cadeia(dict(CORPO_B, objeto="n-b", itens_observados={"Dwarven Aura": 1, "Rogue Aura": 1}), "n-b.json")),
        ("N-C-boot", lambda: _com_cadeia(dict(CORPO_C, objeto="BossHealthbar_Text", estagio="boot"), "n-c.json")),
        ("N-D-pipe", lambda: _com_cadeia({"tipo": "debugger_dump", "objeto": "n-d", "log_texto":
                                          "[Info   :Roguelike Debugger] [Status] 'x' | tags=a|b | desc=\"y\""}, "n-d.json")),
    ]
    falhas, total = [], 0
    for nome, montar in casos:
        obs = montar()
        crits = mod().avaliar([obs], _ident())
        alvo = [c for c in crits if c["id"].startswith("KIT-10/") and c["observado"] is not None]
        estados = {c["estado"] for c in alvo}
        total += 1
        esperado = "REPROVADO"
        if trocar_espera and nome == "N-A-source":
            esperado = "OK"          # ISCA: o defeito N-A deveria ser pego
        if esperado not in estados:
            falhas.append("%s: esperado=%s estados=%s" % (nome, esperado, sorted(estados)))
    return falhas, total


def t_controle_negativo():
    """Os 5 defeitos plantados sao pegos com REPROVADO (avaliador nao aprova tudo)."""
    falhas, total = _roda_negativos()
    exigir(total == 5, "esperava 5 controles negativos, rodei %d" % total)
    exigir(not falhas, "controle negativo NAO pego: " + "; ".join(falhas))


def t_isca_deve_reprovar():
    """Prova de fogo do proprio teste: com a espera trocada, a comparacao TEM de falhar."""
    falhas, _ = _roda_negativos(trocar_espera=True)
    exigir(falhas, "a isca (espera trocada) NAO fez o teste falhar - o teste nao mede nada")


# --------------------------------------------------------- guardas anti-FALSO-OK (F1/F2/F3 do KIT-10R)

def _roda_falsos_ok(trocar_espera=False):
    """Cada LACUNA plantada TEM de devolver NAO_EXERCITADO (nunca OK, nunca prova_runtime).

    Sao os tres falsos-OK que a revisao independente KIT-10R provou: estagio inventado (F1),
    aura viva sem item observado (F2) e tooltip de buff nao medida (F3).
    """
    def _a_sem_contrib():
        corpo = dict(CORPO_A, objeto="g3-contrib-ausente")
        corpo.pop("contrib_observada")
        return corpo

    def _sem(objeto, campo):
        """CORPO_A sem UM campo medido: a ausencia tem de virar NAO_EXERCITADO, nunca OK."""
        corpo = dict(CORPO_A, objeto=objeto)
        corpo.pop(campo)
        return corpo

    casos = [
        ("G1-estagio-desconhecido", lambda: _com_cadeia(
            dict(CORPO_C, objeto="BossHealthbar_Text", estagio="banana", evento_id="evt-9"),
            "g1.json")),
        ("G2-itens-ausentes", lambda: _com_cadeia(
            dict(CORPO_B, objeto="g2-itens-ausentes", itens_observados={}), "g2.json")),
        ("G2-itens-parciais", lambda: _com_cadeia(
            dict(CORPO_B, objeto="g2-itens-parciais", itens_observados={"Dwarven Aura": 2}), "g2b.json")),
        ("G3-buff-fora-tabela", lambda: _com_cadeia(
            dict(CORPO_A, objeto="g3-buff-fora", aura_buff="Aura Que Nao Existe"), "g3.json")),
        ("G3-contrib-ausente", lambda: _com_cadeia(_a_sem_contrib(), "g3b.json")),
        # F5/F6/F7 (KIT-10R2): campo NAO MEDIDO nao pode fechar OK. Cada lacuna -> NAO_EXERCITADO.
        ("G4-dano-ausente", lambda: _com_cadeia(_sem("g4-dano-ausente", "dano_observado"), "g4.json")),
        ("G5-receptor-ausente", lambda: _com_cadeia(_sem("g5-receptor-ausente", "receptor_bonus"), "g5.json")),
        ("G6-fonte-ausente", lambda: _com_cadeia(_sem("g6-fonte-ausente", "fonte_bonus"), "g6.json")),
        ("G7-buff-ausente", lambda: _com_cadeia(_sem("g7-buff-ausente", "aura_buff"), "g7.json")),
    ]
    falhas, total = [], 0
    for nome, montar in casos:
        obs = montar()
        crits = mod().avaliar([obs], _ident())
        alvo = [c for c in crits if c["id"].startswith("KIT-10/") and c["observado"] is not None]
        total += 1
        esperado = "NAO_EXERCITADO"
        if trocar_espera and nome == "G1-estagio-desconhecido":
            esperado = "OK"          # ISCA: estagio inventado NAO pode fechar OK
        estados = {c["estado"] for c in alvo}
        if esperado not in estados:
            falhas.append("%s: esperado=%s estados=%s" % (nome, esperado, sorted(estados)))
        provados = [c["id"] for c in alvo if c.get("prova_runtime")]
        if provados:
            falhas.append("%s: lacuna marcou prova_runtime=True em %s" % (nome, provados))
    return falhas, total


def t_guardas_sem_falso_ok():
    """F1/F2/F3 (KIT-10R) + F5/F6/F7 (KIT-10R2): lacuna de coleta NAO fecha OK nem prova_runtime."""
    falhas, total = _roda_falsos_ok()
    exigir(total == 9, "esperava 9 guardas anti-falso-OK, rodei %d" % total)
    exigir(not falhas, "lacuna recebeu OK/prova_runtime: " + "; ".join(falhas))


def t_isca_guardas_deve_reprovar():
    """Prova de fogo das guardas novas: com a espera trocada, a comparacao TEM de falhar."""
    falhas, _ = _roda_falsos_ok(trocar_espera=True)
    exigir(falhas, "a isca das guardas anti-falso-OK NAO fez o teste falhar - o teste nao mede nada")


CASOS = [
    ("A-ok-runtime", t_A_ok_runtime),
    ("A-defeito-source-injetado", t_A_defeito_source_injetado),
    ("A-defeito-dano-escalou-receptor", t_A_defeito_dano_escalou_receptor),
    ("B-ok-dobro-preservado", t_B_ok_dobro_preservado),
    ("B-defeito-dobro-removido", t_B_defeito_dobro_removido),
    ("C-ok-evento", t_C_ok_evento),
    ("C-defeito-boot", t_C_defeito_boot),
    ("C-sem-evento-nao-ok", t_C_sem_evento_nao_ok),
    ("D-ok-sem-truncar", t_D_ok_sem_truncar),
    ("D-defeito-pipe-no-valor", t_D_defeito_pipe_no_valor),
    ("D-defeito-truncado", t_D_defeito_truncado),
    ("A-guarda-buff-fora-tabela", t_A_buff_fora_da_tabela_nao_ok),
    ("A-guarda-contrib-ausente", t_A_contrib_ausente_nao_ok),
    ("B-guarda-itens-ausentes", t_B_itens_ausentes_nao_ok),
    ("B-guarda-itens-parciais", t_B_itens_parciais_nao_ok),
    ("C-guarda-estagio-desconhecido", t_C_estagio_desconhecido_nao_ok),
    ("A-guarda-dano-ausente", t_A_dano_ausente_nao_ok),
    ("A-guarda-receptor-ausente", t_A_receptor_ausente_nao_ok),
    ("A-guarda-fonte-ausente", t_A_fonte_ausente_nao_ok),
    ("A-guarda-buff-ausente", t_A_buff_ausente_nao_ok),
    ("reuso-cic4-aut7", t_reuso_cic4_aut7),
    ("contrato-campos", t_contrato_campos),
    ("esperado-rastreavel-kit10", t_esperado_rastreavel_kit10),
    ("fixture-nao-prova-runtime", t_fixture_nao_prova_runtime),
    ("controle-negativo", t_controle_negativo),
    ("isca-teste-deve-reprovar", t_isca_deve_reprovar),
    ("guardas-sem-falso-ok", t_guardas_sem_falso_ok),
    ("isca-guardas-deve-reprovar", t_isca_guardas_deve_reprovar),
]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Testes offline do avaliador KIT-10.")
    ap.add_argument("--isca", action="store_true",
                    help="planta defeito (espera trocada) -> a suite TEM de sair REPROVOU/exit 1")
    args = ap.parse_args(argv)

    if args.isca:
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

    print("TOTAL|rodaram=%d reprovaram=%d nao_rodaram=%d" % (rodaram, reprovaram, nao_rodaram))
    if reprovaram:
        return EXIT_FALHOU
    if nao_rodaram:
        return EXIT_NAO_RODOU
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
