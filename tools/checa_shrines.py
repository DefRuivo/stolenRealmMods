#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""checa_shrines.py - CHK-1: confere o log do jogo contra a tabela de esperados GERADA dos shrines.

POR QUE ESTA FERRAMENTA EXISTE
------------------------------
A conferencia das auras de shrine era humana: o dono entrava em partida, lia o numero na tooltip e
transcrevia para comparar com 3 casos calculados a mao. Isso e lento, depende de transcricao e ja
produziu erro (a linha do Flame nasceu com o sujeito errado). Aqui o JOGO produz a informacao
(os mods ja logam o que renderizam) e a ferramenta COMPARA - o dono so precisa abrir cada shrine
uma vez. A regra que a ferramenta segue e a oposta da do `check_patches` que deixou passar um falso
OK: **ausencia NUNCA vira aprovacao**. Shrine nao exercitado sai como AUSENTE, e a lista de nao
exercitados e impressa por extenso no fim.

O QUE ELA LE
------------
1. A tabela de ESPERADOS `tools/dados/shrines-esperado.csv` + `tools/dados/shrines-percentuais.csv`
   - GERADAS por `tools/gera_shrines_esperado.py` a partir da fonte da verdade (censo
   `docs/cobertura/status.csv` e `resources.assets`), nunca digitadas. Nenhum numero esperado vive
   no codigo desta ferramenta: se o CSV mudar, a conferencia muda.
2. O `LogOutput.log` do perfil (o mesmo do censo). Dela saem:
   * o dump de boot do `RoguelikeDebugger` (`[Status] 'nome' | ... | efeitos=<formula> | ...`) -
     usado para CROSS-CHECK da base de cada aura de buff contra o proprio jogo;
   * as linhas do `BetterTooltips` com o marcador estavel `[Shrine RV-23]`:
       - `RV-31 acumulado: auras=[...] char=<nome> bonus=<b> -> <item>; <item>` - a ANCORA: traz o
         bonus, o personagem, QUAIS auras estao vivas e, por atributo, a contribuicao das auras e
         o total do personagem (RV-44);
       - `RV-34 linha do Decay: <char> MaxHealth=<mh> bonus=<b> -> '<linha>'` - o dano por turno;
       - `RV-34 Flame alvo '<nome>': MaxHealth=<mh> tipo=<tipo> bonus=<b> dano=<d>` - o dano por
         atacante projetado, por alvo na area.

COMO LER A SAIDA
----------------
  OK       - o valor observado bate com o esperado (dentro da tolerancia: estes numeros sao
             inteiros; a comparacao e exata).
  ACHADO   - o valor observado DIFERE do esperado. Traz o observado, o esperado e a diferenca, com
             o char e a linha do log. Reprova a rodada (exit 1).
  AUSENTE  - aquela aura/caso NAO foi exercitado (ou o campo que permite comparar nao esta no
             log). Nao reprova sozinho, mas impede o exit 0 (exit 3): ausencia nao e aprovacao.
  AVISO    - linha lida que NAO entra em nenhuma comparacao (evidencia sem caso atribuivel, formato
             antigo etc.), listada para nao virar ponto cego.

Exit codes: 0 = TODAS as linhas do esperado tiveram observacao OK; 1 = pelo menos um ACHADO;
            2 = nao conseguiu verificar (log ou tabela ausente/ilegivel); 3 = sem ACHADO, mas
            com AUSENTE (conferencia INCOMPLETA). Todo exit != 0 imprime o motivo.

USO
---
    python tools/checa_shrines.py                      # log do perfil padrao
    python tools/checa_shrines.py --log caminho.log    # outro log (ex.: fixture de teste)
    python tools/checa_shrines.py --so-cobertura       # so diz o que nao foi exercitado

LIMITES - O QUE ESTA FERRAMENTA **NAO** PROVA
---------------------------------------------
1. **A leitura visual final e do dono.** Ela compara NUMEROS que o mod logou; nao le a tela. Se o
   mod logar um numero certo e desenhar outro (texto composto errado, bloco no lugar errado,
   `[0]` nao substituido, cor/ordem), a ferramenta NAO percebe - o "olhar a tela UMA vez" continua
   sendo o ultimo passo humano (roteiro no doc CHK-1).
2. **A base do Dwarven, do Decay e do Flame nao esta no dump do Debugger.** O `efeitos` delas e
   vazio de proposito (RV-19 §5) - o cross-check contra o jogo so cobre as 9 auras de buff. As
   bases dessas 3 vem do asset (o gerador cita o offset) e NAO tem segunda fonte em log.
3. **O Dwarven (stun) nao tem atributo de personagem**: nao existe numero para comparar no log ->
   fica permanentemente AUSENTE na conferencia mecanica (a leitura e visual: "chance to stun").
   O mesmo vale para o `[0]`% do Decay isolado do dano (o log imprime o DANO por turno; a % so e
   isolavel quando MaxHealth = 100).
4. **O texto do jogo nao e comparado** - as chaves/`TextFixes`/`TextAppends` nao entram aqui.
5. **A `linha do Decay` passou a logar o tipo de inimigo (`tipo=`)** — CHK-1 §7.1, CONSERTO APLICADO
   em 01/10 no `ShrineAuraPatch`: o esperado do Decay usa a % DO TIPO logado (antes era sempre a de
   `player`, e um portador IA virava ACHADO sem causa atribuivel). O campo e OPCIONAL no parser de
   proposito: log anterior ao conserto continua sendo lido, cai na % de `player` e a linha do
   resultado DIZ isso (`[tipo nao logado -> player 10%]`) em vez de fingir que conferiu.
6. **`RV-44 item`/`RV-44 soma` passaram a trazer `char=` e `bonus=`** — CHK-1 §7.2, CONSERTO APLICADO
   em 01/10: com os dois campos a evidencia e ATRIBUIVEL a um caso e sai na secao `EVIDENCIA
   ATRIBUIDA` (com o caso ao lado) em vez de AVISO cego. Sem os campos (log anterior ao conserto)
   vale o AVISO de antes. Quem ancora o caso em OK/ACHADO continua sendo a linha `RV-31 acumulado`.
   (As duas marcas sao de LOG: nenhum texto de jogador mudou com elas.)
7. Ela NAO cobre o caso de bonus +8 (`Omnism I`) e +50 (roll do `Horn of Devotion`): a tabela tem
   os 3 casos exigidos (0, +20, +100). Uma observacao com bonus fora dos 3 sai como AVISO.
8. Ela nao prova que o numero do Flame e o do PORTADOR em vez do ATACANTE (RV-19 §9(ii)):
   ela confere a formula contra o dano logado com `Source = Target = o alvo projetado`. A medicao
   do dano de RETORNO com `Worship` continua sendo uma experiencia em jogo.
"""

import argparse
import csv
import math
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ESPERADO = os.path.join(RAIZ, "tools", "dados", "shrines-esperado.csv")
PERCENTUAIS = os.path.join(RAIZ, "tools", "dados", "shrines-percentuais.csv")
LOG_PADRAO = os.path.join(os.environ.get("APPDATA", ""), "r2modmanPlus-local", "StolenRealm",
                          "profiles", "Default", "BepInEx", "LogOutput.log")

# Marcador ESTAVEL do mod (a funcao `Marca` do ShrineAuraPatch, prefixo fixo) e o do dump.
RE_LINHA_SHRINE = re.compile(r"^\[[A-Za-z]+\s*:\s*Better Tooltips\]\s*\[Shrine RV-23\]\s*(?P<p>.+)$")
RE_LINHA_STATUS = re.compile(r"^\[[A-Za-z]+\s*:\s*Roguelike Debugger\]\s*\[Status\]\s*'(?P<nome>.*?)'\s*\|(?P<c>.*)$")

# Ancoras do comparador.
RE_ACUMULADO = re.compile(
    r"^RV-31 acumulado: auras=\[(?P<auras>[^\]]*)\] char=(?P<char>.+?) bonus=(?P<bonus>-?[0-9.]+) -> (?P<efeito>.+)$")
# CHK-1 §7.1 (CONSERTO APLICADO no mod): a linha do Decay ganhou `tipo=`. O grupo e OPCIONAL de proposito -
# o log anterior ao conserto continua sendo lido, so cai na % de `player` e a saida DIZ isso em vez de fingir.
RE_DECAY = re.compile(
    r"^RV-34 linha do Decay: (?P<char>.+?) MaxHealth=(?P<mh>[0-9.]+)"
    r"(?: tipo=(?P<tipo>[A-Za-z_()]+))? bonus=(?P<bonus>-?[0-9.]+) -> '(?P<linha>.*)'$")
# CHK-1 §7.2 (CONSERTO APLICADO no mod): `RV-44 item`/`RV-44 soma` ganharam `char=` e `bonus=`, que e o que
# torna a evidencia ATRIBUIVEL a um caso. Sem os campos, a linha continua caindo no AVISO de antes.
RE_EVIDENCIA = re.compile(r" char=(?P<char>.+?) bonus=(?P<bonus>-?[0-9.]+)")
RE_DECAY_DANO = re.compile(r"\((?P<dano>[0-9.]+) damage per turn for you\)")
RE_FLAME = re.compile(
    r"^RV-34 Flame alvo '(?P<nome>.*?)': MaxHealth=(?P<mh>[0-9.]+) tipo=(?P<tipo>[A-Za-z_()]+)"
    r" bonus=(?P<bonus>-?[0-9.]+) dano=(?P<dano>[0-9.]+)$")

# Itens da linha de acumulado: o rotulo e a ORDEM sao do `Format`/`TextDoEfeito` do mod (estaveis).
RE_ITEM = re.compile(
    r"^(?P<label>Damage|Damage taken|Crit Chance|Dodge|Life Steal|Health per turn|Mana per turn) "
    r"(?P<s>[+\-\u2212])(?P<v>[0-9.]+)% \(total (?P<ts>[+\-\u2212])(?P<tv>[0-9.]+)%\)$")
RE_ITEM_MANA = re.compile(
    r"^Mana Costs (?P<dir>reduced by|increased by) (?P<v>[0-9.]+)% "
    r"\(total (?P<ts>[+\-\u2212])(?P<tv>[0-9.]+)%\)$")

ROTULO_ATRIBUTO = {
    "Damage": "DamageMod",
    "Damage taken": "DamageReduction",
    "Crit Chance": "CritChance",
    "Dodge": "DodgeChance",
    "Life Steal": "LifeOnHit",
    "Health per turn": "HealthPerTurnPercent",
    "Mana per turn": "ManaPerTurnPercent",
}

# Aliases do nome do status (o `ActionStatusInfo.Name` do asset pode diferir do nome do censo).
ALIASES = {
    "Dwarven Totem Aura Status": "Dwarven Aura",
}

RE_FORMULA_STATUS = re.compile(
    r"Mathf\.Round\((-?[0-9]+(?:\.[0-9]+)?) \* \(1 \+ \((?:Target|Source)\["
    r"\"ShrineEffectBonus\"\] / 100\)\)\)")


def round_half_even(v):
    f = math.floor(v)
    dif = v - f
    if dif > 0.5:
        return f + 1
    if dif < 0.5:
        return f
    return f if f % 2 == 0 else f + 1


def numero(s):
    return float(s.replace("\u2212", "-"))


def sinal(txt):
    return -1.0 if txt in ("-", "\u2212") else 1.0


def fmt(v):
    return "%g" % v


MARCA = {"OK": "[OK]     ", "ACHADO": "[ACHADO] ", "AUSENTE": "[AUSENTE]", "NVER": "[NAO-VER]"}


def marca(s):
    return MARCA.get(s, "[?]      ")


class Achado(object):
    def __init__(self, aura, atributo, caso, observado, esperado, motivo, linha_log, char=""):
        self.aura, self.atributo, self.caso = aura, atributo, caso
        self.observado, self.esperado = observado, esperado
        self.motivo, self.linha_log, self.char = motivo, linha_log, char


def carrega_esperado(caminho):
    if not os.path.isfile(caminho):
        print("FALHA(2): tabela de esperados ausente: %s\n  -> rode `python tools/gera_shrines_esperado.py`."
              % caminho)
        return None
    with open(caminho, newline="", encoding="utf-8") as f:
        leitor = csv.DictReader(f)
        linhas = [r for r in leitor]
    if not linhas:
        print("FALHA(2): a tabela de esperados esta VAZIA: %s" % caminho)
        return None
    return linhas


def carrega_percentuais(caminho):
    if not os.path.isfile(caminho):
        print("FALHA(2): tabela de percentuais ausente: %s\n  -> rode `python tools/gera_shrines_esperado.py`."
              % caminho)
        return None
    pct = {}
    with open(caminho, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            pct.setdefault(r["aura"], {})[r["tipo"]] = float(r["percentual"])
    return pct


def le_log(caminho):
    if not os.path.isfile(caminho):
        print("FALHA(2): log ausente: %s" % caminho)
        return None
    with open(caminho, "rb") as f:
        return f.read().decode("utf-8", errors="replace")


def parseia_acumulado(payload):
    """Devolve a lista de itens (atributo, contribuicao, total) + o cabecalho, ou (None, motivo)."""
    m = RE_ACUMULADO.match(payload)
    if not m:
        return None, None
    auras = [a.strip() for a in m.group("auras").split(",") if a.strip()]
    auras = [ALIASES.get(a, a) for a in auras]
    itens = []
    nao_parseados = []
    for bruto in m.group("efeito").split("; "):
        bruto = bruto.strip()
        mm = RE_ITEM.match(bruto)
        if mm:
            label = mm.group("label")
            v = sinal(mm.group("s")) * float(mm.group("v"))
            tv = sinal(mm.group("ts")) * float(mm.group("tv"))
            if label == "Damage taken":
                # o rotulo e INVERTIDO em relacao ao atributo (`DamageReduction` positivo reduz);
                # o motor soma o valor cru - e com o cru que a conta fecha (RV-19 §9.2).
                v, tv = -v, -tv
            itens.append({"atributo": ROTULO_ATRIBUTO[label], "contrib": v, "total": tv})
            continue
        mm = RE_ITEM_MANA.match(bruto)
        if mm:
            v = float(mm.group("v"))
            if mm.group("dir") == "reduced by":
                v = -v
            tv = sinal(mm.group("ts")) * float(mm.group("tv"))
            itens.append({"atributo": "ManaCostMod", "contrib": v, "total": tv})
            continue
        nao_parseados.append(bruto)
    return {"char": m.group("char"), "bonus": numero(m.group("bonus")), "auras": auras,
            "itens": itens, "nao_parseados": nao_parseados,
            "pre_rv44": (not itens) and all("(total" not in x for x in nao_parseados)}, None


def coleta(log):
    obs = {"acumulado": [], "decay": [], "flame": [], "evidencias": [], "dump": {},
           "avisos": [], "nao_lidas": []}
    for n, linha in enumerate(log.splitlines(), start=1):
        mi = RE_LINHA_SHRINE.match(linha)
        if mi:
            p = mi.group("p").strip()
            if p.startswith("RV-31 acumulado:"):
                o, _ = parseia_acumulado(p)
                if o is None:
                    obs["avisos"].append((n, "RV-31 acumulado em formato NAO reconhecido: %r" % p))
                else:
                    o["linha"] = n
                    obs["acumulado"].append(o)
                    if o["pre_rv44"]:
                        obs["avisos"].append(
                            (n, "linha no formato PRE-RV-44: o item traz o TOTAL do personagem "
                                "('Damage +50%') e NAO a contribuicao das auras ('Damage +25% (total +50%)') "
                                "- nao comparavel. O build instalado e ANTERIOR ao RV-44: recompile e "
                                "reinstale o BetterTooltips e repita a rodada."))
                        continue
                    for bruto in o["nao_parseados"]:
                        obs["avisos"].append(
                            (n, "item do acumulado fora do formato (nao comparavel): %r" % bruto))
            elif p.startswith("RV-34 linha do Decay:"):
                m = RE_DECAY.match(p)
                if not m:
                    obs["avisos"].append((n, "linha do Decay em formato NAO reconhecido: %r" % p))
                    continue
                md = RE_DECAY_DANO.search(m.group("linha"))
                obs["decay"].append({
                    "char": m.group("char"), "mh": float(m.group("mh")),
                    # CHK-1 §7.1: `tipo` pode vir None (log anterior ao conserto do mod).
                    "tipo": m.group("tipo"),
                    "bonus": numero(m.group("bonus")),
                    "dano": float(md.group("dano")) if md else None,
                    "linha": n, "bruto": p,
                })
            elif p.startswith("RV-34 Flame alvo '"):
                m = RE_FLAME.match(p)
                if not m:
                    obs["avisos"].append((n, "alvo do Flame em formato NAO reconhecido: %r" % p))
                    continue
                obs["flame"].append({
                    "nome": m.group("nome"), "mh": float(m.group("mh")), "tipo": m.group("tipo"),
                    "bonus": numero(m.group("bonus")), "dano": float(m.group("dano")),
                    "linha": n, "bruto": p,
                })
            elif p.startswith("RV-44 item ") or p.startswith("RV-44 soma "):
                # CHK-1 §7.2 (conserto aplicado no mod): com `char=` e `bonus=` a evidencia passa a ser
                # ATRIBUIVEL a um caso e deixa de ser AVISO cego. Sem os campos (log anterior ao
                # conserto) vale o limite 6 antigo, com o mesmo texto de antes.
                me = RE_EVIDENCIA.search(p)
                if me:
                    obs["evidencias"].append({
                        "bruto": p, "linha": n, "item": p.startswith("RV-44 item "),
                        "char": me.group("char"), "bonus": numero(me.group("bonus")),
                    })
                else:
                    obs["avisos"].append((n, "evidencia `%s` sem campo bonus/char (nao atribuivel): %r"
                                          % (" ".join(p.split(" ")[:2]), p)))
            elif p.startswith("chave '"):
                # Log do LocalizePatch: mostra o texto final MONTADO, mas com o `[0]` AINDA no lugar
                # (o pipeline de expressoes roda depois). Nao traz numero de aura resolvido -> nao
                # comparavel; contado e nao listado linha a linha (sao centenas por sessao).
                obs["chave"] = obs.get("chave", 0) + 1
            elif p.startswith("RV-31 sem linha:") or p.startswith("RV-33 Decay sem numero:") \
                    or p.startswith("RV-34 Decay sem numero:") or p.startswith("RV-33 Flame sem alvo:") \
                    or p.startswith("RV-34 Flame alvo '") or p.startswith("RV-34 fator") \
                    or p.startswith("RV-44 ") or p.startswith("params:") or p.startswith("RV-34 reserva"):
                obs["avisos"].append((n, p))
            else:
                obs["nao_lidas"].append((n, p))
            continue
        ms = RE_LINHA_STATUS.match(linha)
        if ms:
            campos = dict()
            for pedaco in ms.group("c").split("|"):
                if "=" in pedaco:
                    k, v = pedaco.split("=", 1)
                    campos[k.strip()] = v.strip()
            obs["dump"][ms.group("nome")] = campos
    return obs


def esperado_buff(tabela, aura, atributo, bonus):
    """Contribuicao esperada da aura naquele atributo/caso. None = nao ha linha no esperado."""
    for r in tabela:
        if r["aura"] == aura and r["atributo"] == atributo and float(r["caso_bonus"]) == bonus:
            return float(r["contribuicao_esperada"])
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Confere o log do jogo contra a tabela de esperados dos shrines.")
    ap.add_argument("--log", default=LOG_PADRAO, help="LogOutput.log (default: perfil do r2modman)")
    ap.add_argument("--esperado", default=ESPERADO)
    ap.add_argument("--percentuais", default=PERCENTUAIS)
    ap.add_argument("--so-cobertura", action="store_true", help="imprime apenas o que NAO foi exercitado")
    args = ap.parse_args(argv)

    tabela = carrega_esperado(args.esperado)
    if tabela is None:
        return 2
    pct = carrega_percentuais(args.percentuais)
    if pct is None:
        return 2
    log = le_log(args.log)
    if log is None:
        return 2

    obs = coleta(log)
    achados = []
    resultados = {}   # (aura, atributo, caso) -> [(status, texto)]
    avisos = list(obs["avisos"])

    # ------------------------------------------------------------------ auras de BUFF (por atributo)
    for r in tabela:
        aura, atributo, caso = r["aura"], r["atributo"], r["caso_bonus"]
        caso_f = float(caso)
        chave = (aura, atributo, caso)
        if r["tipo"] != "buff":
            continue
        if not atributo:
            resultados[chave] = [("NVER", "NAO VERIFICAVEL pela ferramenta: o Dwarven nao expoe atributo "
                                           "de personagem (o efeito e chance de stun) - nenhum numero sai "
                                           "no log; a prova e a leitura visual na tela")]
            continue
        cobertos = 0
        for o in obs["acumulado"]:
            if o["bonus"] != caso_f or aura not in o["auras"]:
                continue
            item = None
            for it in o["itens"]:
                if it["atributo"] == atributo:
                    item = it
                    break
            if item is None:
                continue
            # soma esperada das auras VIVAS naquele atributo (o valor logado e a soma - RV-44)
            soma = 0.0
            indeterminado = None
            for a in o["auras"]:
                e = esperado_buff(tabela, a, atributo, caso_f)
                if e is None:
                    indeterminado = a
                    break
                soma += e
            if indeterminado is not None:
                resultados.setdefault(chave, []).append(
                    ("AUSENTE", "hover com a aura '%s', que nao tem linha esperada para o atributo '%s'"
                                % (indeterminado, atributo)))
                continue
            cobertos += 1
            if abs(item["contrib"] - soma) > 1e-9:
                achados.append(Achado(aura, atributo, caso, item["contrib"], soma,
                                      "contribuicao das auras difere", o["linha"], o["char"]))
                resultados.setdefault(chave, []).append(
                    ("ACHADO", "char=%s contrib=%s esperado=%s dif=%+g (log:%d)"
                     % (o["char"], fmt(item["contrib"]), fmt(soma),
                        item["contrib"] - soma, o["linha"])))
            else:
                resultados.setdefault(chave, []).append(
                    ("OK", "char=%s contrib=%s total=%s (log:%d)"
                     % (o["char"], fmt(item["contrib"]), fmt(item["total"]), o["linha"])))
        if cobertos == 0 and chave not in resultados:
            resultados[chave] = [("AUSENTE", "sem hover com bonus=%s e a aura viva no log" % caso)]

    # ------------------------------------------------------------------ decan e flame (dano)
    for r in tabela:
        if r["tipo"] != "perigo":
            continue
        aura, caso = r["aura"], r["caso_bonus"]
        caso_f = float(caso)
        chave = (aura, "", caso)
        pct_player = pct[aura]["player"]
        if aura == "Decay Shrine Aura":
            candidatos = [o for o in obs["decay"] if o["bonus"] == caso_f]
            if not candidatos:
                resultados[chave] = [("AUSENTE", "sem linha do Decay com bonus=%s no log" % caso)]
                continue
            for o in candidatos:
                if o["dano"] is None:
                    resultados.setdefault(chave, []).append(
                        ("AUSENTE", "linha do Decay sem o dano '(N damage per turn for you)': %r" % o["bruto"]))
                    continue
                # CHK-1 §7.1 (conserto aplicado no mod): com o `tipo=` da marca, o esperado usa a % DO
                # TIPO (a que o motor usa de verdade). Sem o campo - log anterior ao conserto - cai na
                # % de `player` e a linha do resultado DIZ isso, como antes.
                tipo = (o.get("tipo") or "").lower()
                tipo = tipo if tipo in pct[aura] else None
                pct_usada = pct[aura][tipo] if tipo else pct_player
                rotulo_tipo = ("tipo=%s %s%%" % (o["tipo"], fmt(pct_usada))) if tipo \
                    else "[tipo nao logado -> player %s%%]" % fmt(pct_player)
                esp = float(round_half_even(o["mh"] * (pct_usada / 100.0) * (1 + caso_f / 100.0)))
                if abs(o["dano"] - esp) > 1e-9:
                    achados.append(Achado(aura, "(dano/turno)", caso, o["dano"], esp,
                                          "dano do Decay difere (%s)" % rotulo_tipo,
                                          o["linha"], o["char"]))
                    resultados.setdefault(chave, []).append(
                        ("ACHADO", "char=%s MaxHealth=%s dano=%s esperado=%s (%s) dif=%+g (log:%d)"
                         % (o["char"], fmt(o["mh"]), fmt(o["dano"]), fmt(esp), rotulo_tipo,
                            o["dano"] - esp, o["linha"])))
                else:
                    resultados.setdefault(chave, []).append(
                        ("OK", "char=%s MaxHealth=%s dano=%s [%s] (log:%d)"
                         % (o["char"], fmt(o["mh"]), fmt(o["dano"]), rotulo_tipo, o["linha"])))
            continue
        # Flame: um item por ALVO na area, cada um com a vida/%%/bonus DELE
        candidatos = [o for o in obs["flame"] if o["bonus"] == caso_f]
        if not candidatos:
            resultados[chave] = [("AUSENTE", "sem alvo do Flame com bonus=%s no log" % caso)]
            continue
        for o in candidatos:
            # `TipoDoAlvo` do mod imprime `EnemyType.ToString()` (ex.: `Boss`, `Fodder`) ou `player`
            # para quem nao e IA: a tabela e por nome MINUSCULO do enum - comparar sem caixa.
            tipo = o["tipo"].lower() if o["tipo"].lower() in pct[aura] else None
            if tipo is None:
                resultados.setdefault(chave, []).append(
                    ("AUSENTE", "tipo '%s' do alvo do Flame nao esta na tabela de percentuais" % o["tipo"]))
                continue
            esp = max(1.0, float(round_half_even(o["mh"] * (pct[aura][tipo] / 100.0) * (1 + caso_f / 100.0))))
            if abs(o["dano"] - esp) > 1e-9:
                achados.append(Achado(aura, "(dano por alvo)", caso, o["dano"], esp,
                                      "dano do Flame difere", o["linha"], o["nome"]))
                resultados.setdefault(chave, []).append(
                    ("ACHADO", "alvo=%s tipo=%s MaxHealth=%s dano=%s esperado=%s dif=%+g (log:%d)"
                     % (o["nome"], o["tipo"], fmt(o["mh"]), fmt(o["dano"]), fmt(esp),
                        o["dano"] - esp, o["linha"])))
            else:
                resultados.setdefault(chave, []).append(
                    ("OK", "alvo=%s tipo=%s MaxHealth=%s dano=%s (log:%d)"
                     % (o["nome"], o["tipo"], fmt(o["mh"]), fmt(o["dano"]), o["linha"])))

    # ------------------------------------------------------------------ aceite (total provado em jogo)
    aceites = []
    for r in tabela:
        if not r["total_esperado"]:
            continue
        aura, atributo, caso = r["aura"], r["atributo"], r["caso_bonus"]
        caso_f = float(caso)
        total_esp = float(r["total_esperado"])
        resto_esp = float(r["resto_esperado"])
        cands = []
        for o in obs["acumulado"]:
            if o["bonus"] != caso_f or aura not in o["auras"]:
                continue
            for it in o["itens"]:
                if it["atributo"] == atributo:
                    cands.append((o, it))
        if not cands:
            aceites.append(("AUSENTE", "%s/%s bonus=%s: sem hover com a aura viva - caso de aceite NAO "
                                       "exercitado (esperado total=%s resto=%s)"
                           % (aura, atributo, caso, fmt(total_esp), fmt(resto_esp))))
            continue
        bate_resto = [c for c in cands if abs((c[1]["total"] - c[1]["contrib"]) - resto_esp) < 1e-9]
        if not bate_resto:
            aceites.append(("AUSENTE", "%s/%s bonus=%s: hover(s) com resto diferente do print do dono "
                                       "(resto doc=%s) - build diferente, aceite nao conferido"
                           % (aura, atributo, caso, fmt(resto_esp))))
            continue
        for o, it in bate_resto:
            if abs(it["total"] - total_esp) > 1e-9:
                achados.append(Achado(aura, atributo, caso, it["total"], total_esp,
                                      "total do personagem difere do print do dono", o["linha"], o["char"]))
                aceites.append(("ACHADO", "%s/%s bonus=%s char=%s total=%s esperado=%s (log:%d)"
                                % (aura, atributo, caso, o["char"], fmt(it["total"]), fmt(total_esp), o["linha"])))
            else:
                aceites.append(("OK", "%s/%s bonus=%s char=%s total=%s resto=%s (log:%d)"
                                % (aura, atributo, caso, o["char"], fmt(it["total"]),
                                   fmt(it["total"] - it["contrib"]), o["linha"])))

    # ------------------------------------------------------------------ aditividade (resto constante)
    adit = []
    por_chave = {}
    for o in obs["acumulado"]:
        for it in o["itens"]:
            por_chave.setdefault((o["char"], it["atributo"]), []).append(
                (o["bonus"], it["contrib"], it["total"], o["linha"]))
    for (char, atributo), lista in sorted(por_chave.items()):
        if len(lista) < 2:
            continue
        restos = sorted(set(round(t - c, 6) for _, c, t, _ in lista))
        if len(restos) > 1:
            achados.append(Achado("(aditividade)", atributo, "todos", restos[0], restos[0],
                                  "resto (total - aura) NAO e constante para %s em %s" % (char, atributo),
                                  lista[0][3], char))
            adit.append(("ACHADO", "char=%s %s: resto varia entre %s (esperado constante)"
                         % (char, atributo, ", ".join(fmt(x) for x in restos))))
        else:
            adit.append(("OK", "char=%s %s: resto=%s constante em %d bonus"
                         % (char, atributo, fmt(restos[0]), len(lista))))

    # ------------------------------------------------------------------ cross-check com o dump
    dump_res = []
    for r in tabela:
        aura, atributo, base, caso = r["aura"], r["atributo"], float(r["base"]), r["caso_bonus"]
        if r["tipo"] != "buff" or caso != "0":
            continue
        nome_dump = aura
        for alias, alvo in ALIASES.items():
            if alvo == aura and alias in obs["dump"]:
                nome_dump = alias
        campos = obs["dump"].get(nome_dump)
        if not campos:
            dump_res.append(("AUSENTE", "%s: sem linha `[Status]` do Debugger no log (a base vem do asset)" % aura))
            continue
        efeitos = campos.get("efeitos", "")
        pares = []
        for parte in efeitos.split(", "):
            if parte.count(":") < 2:
                continue
            a, _metodo, expr = parte.split(":", 2)
            m = RE_FORMULA_STATUS.search(expr)
            if m:
                pares.append((a, float(m.group(1))))
        if not pares:
            dump_res.append(("AUSENTE", "%s: o dump tem a coluna `efeitos` VAZIA - e o caso previsto "
                                        "para Dwarven/Decay/Flame (RV-19 §5); a base vem do asset" % aura))
            continue
        base_dump = None
        for a, b in pares:
            if a == atributo:
                base_dump = b
                break
        if base_dump is None:
            dump_res.append(("AUSENTE", "%s: o dump do Debugger nao traz a formula do atributo '%s' "
                                        "(efeitos: %s)" % (aura, atributo, efeitos.strip())))
            continue
        if abs(base_dump - base) > 1e-9:
            achados.append(Achado(aura, atributo, "0", base_dump, base,
                                  "base do dump do Debugger difere do esperado", 0))
            dump_res.append(("ACHADO", "%s/%s: base do dump=%s e esperado=%s"
                             % (aura, atributo, fmt(base_dump), fmt(base))))
        else:
            dump_res.append(("OK", "%s/%s: base=%s conferida contra o dump do proprio jogo"
                             % (aura, atributo, fmt(base))))

    # ------------------------------------------------------------------ relatorio
    def conta(status):
        return sum(1 for v in resultados.values() for (s, _) in v if s == status)

    nao_exercitados = sorted({(k[0], k[2]) for k, v in resultados.items()
                              if v and all(s == "AUSENTE" for (s, _) in v)})
    nao_verificaveis = sorted({(k[0], k[2]) for k, v in resultados.items()
                               if v and all(s == "NVER" for (s, _) in v)})
    auras_todas = sorted({r["aura"] for r in tabela})
    auras_ok = {k[0] for k, v in resultados.items() if any(s == "OK" for (s, _) in v)}
    auras_nver = {k[0] for k, v in resultados.items() if v and all(s == "NVER" for (s, _) in v)}
    auras_ausentes = [a for a in auras_todas if a not in auras_ok and a not in auras_nver]

    if not args.so_cobertura:
        print("=" * 78)
        print("CHK-1 conferencia mecanica dos shrines")
        print("  log     : %s" % args.log)
        print("  esperado: %s (%d linhas)" % (args.esperado, len(tabela)))
        print("  bonus so existem os 3 casos da tabela: %s" %
              ", ".join(sorted({r["caso_bonus"] for r in tabela}, key=float)))
        print("=" * 78)
        print("\n-- COBERTURA POR AURA --")
        for aura in auras_todas:
            status_aura = {}
            for k, v in resultados.items():
                if k[0] != aura:
                    continue
                status_aura[k[2]] = "OK" if any(s == "OK" for (s, _) in v) else (
                    "ACHADO" if any(s == "ACHADO" for (s, _) in v) else (
                        "N-VER" if all(s == "NVER" for (s, _) in v) else "AUSENTE"))
            linha = "  %-20s" % aura
            for caso in sorted({r["caso_bonus"] for r in tabela if r["aura"] == aura}, key=float):
                linha += " bonus=%-4s %-8s" % (caso, status_aura.get(caso, "AUSENTE"))
            print(linha)

        print("\n-- DETALHE (aura / atributo / caso) --")
        for k in sorted(resultados, key=lambda k: (k[0], k[2], k[1])):
            for s, txt in resultados[k]:
                print("  %s %-20s %-22s bonus=%-3s %s" % (marca(s), k[0], k[1] or "(dano/turno)", k[2], txt))

        if aceites:
            print("\n-- ACEITE (total provado em jogo pelo dono; RV-19 §9.1/§10.5) --")
            for s, txt in aceites:
                print("  %s %s" % (marca(s), txt))

        if adit:
            print("\n-- ADITIVIDADE (resto = total - aura, tem de ser constante por personagem) --")
            for s, txt in adit:
                print("  %s %s" % (marca(s), txt))

        # CHK-1 §7.2 (conserto aplicado no mod): as linhas `RV-44 item`/`RV-44 soma` que trazem `char=`
        # e `bonus=` sao ATRIBUIVEIS a um caso e saem aqui com o dono ao lado, em vez de virarem AVISO
        # cego. Elas NAO decidem OK/ACHADO sozinhas (quem ancora o caso continua sendo o `RV-31
        # acumulado` do mesmo hover) - o que mudou foi a evidencia ter dono.
        print("\n-- EVIDENCIA ATRIBUIDA (RV-44 item/soma com char= e bonus=) --")
        if obs["evidencias"]:
            por_evid = {}
            for e in obs["evidencias"]:
                por_evid.setdefault((e["char"], e["bonus"]), []).append(e)
            for (char, bonus), lista in sorted(por_evid.items()):
                print("  [EVID]    caso char=%s bonus=%s: %d linha(s) atribuida(s) (log:%s)"
                      % (char, fmt(bonus), len(lista),
                         ", ".join(str(x["linha"]) for x in lista)))
        else:
            print("  [AUSENTE] nenhuma linha `RV-44 item`/`RV-44 soma` com `char=`/`bonus=` neste log "
                  "- ou o build e anterior ao CHK-1 §7.2, ou nao houve hover com aura de shrine viva.")

        print("\n-- DUMP DO ROGUELIKEDEBUGGER (fonte independente da base das auras de buff) --")
        for s, txt in dump_res:
            print("  %s %s" % (marca(s), txt))

        if avisos:
            print("\n-- AVISOS (linhas lidas que NAO entram em comparacao; nada de silencio) --")
            vistos = set()
            for n, txt in avisos:
                if txt in vistos:
                    continue
                vistos.add(txt)
                print("  [AVISO]   log:%d %s" % (n, txt))
            if len(avisos) > len(vistos):
                print("  [AVISO]   (%d linhas repetidas omitidas)" % (len(avisos) - len(vistos)))
        if obs.get("chave"):
            print("  [AVISO]   %d linha(s) `chave '...' -> resultado final`: texto localizado, com o `[0]` "
                  "AINDA no lugar (o pipeline de expressoes roda depois) - NAO traz numero de aura." % obs["chave"])
        if obs["nao_lidas"]:
            print("\n-- LINHAS [Shrine ...] NAO RECONHECIDAS (o parser NAO adivinha) --")
            for n, txt in obs["nao_lidas"]:
                print("  [AVISO]   log:%d %r" % (n, txt))
    else:
        print("-- NAO EXERCITADOS (bonus/aura sem nenhuma observacao) --")
        for aura in auras_ausentes:
            print("  %s" % aura)

    print("\n== RESULTADO ==")
    # ACHADO e contado pela LISTA de achados (a autoridade), que inclui os achados que nao sao de
    # uma linha da tabela (cross-check do dump, aditividade) - o contador tem de bater com o REPROVADO.
    print("  OK=%d  ACHADO=%d  AUSENTE=%d  NAO-VERIFICAVEL=%d"
          % (conta("OK"), len(achados), conta("AUSENTE"), conta("NVER")))
    if auras_ausentes:
        print("  NAO EXERCITADOS (nenhum caso OK): %s" % ", ".join(auras_ausentes))
    else:
        print("  NAO EXERCITADOS: nenhum")
    if nao_exercitados:
        print("  AUSENTES linha a linha:")
        for aura, caso in nao_exercitados:
            print("    - %s (bonus=%s)" % (aura, caso))
    if nao_verificaveis:
        print("  NAO VERIFICAVEIS pela ferramenta (nao bloqueiam o exit 0 - a prova e VISUAL): %s"
              % ", ".join("%s (bonus=%s)" % (a, c) for a, c in nao_verificaveis))

    if achados:
        print("\n  REPROVADO por %d achado(s):" % len(achados))
        for a in achados:
            print("    - %s %s bonus=%s: observado=%s esperado=%s dif=%+g (%s%s)"
                  % (a.aura, a.atributo, a.caso, fmt(a.observado), fmt(a.esperado),
                     a.observado - a.esperado, a.motivo,
                     (" log:%d" % a.linha_log) if a.linha_log else ""))
        return 1
    if conta("AUSENTE"):
        print("\n  INCOMPLETO: nada reprovou, mas ha caso AUSENTE - ausencia NAO e aprovacao.")
        return 3
    if conta("NVER"):
        print("  OK: todos os casos EXERCITAVEIS da tabela bateram (%d caso(s) NAO VERIFICAVEL(is) por "
              "desenho - a prova deles e a leitura visual)." % conta("NVER"))
    else:
        print("  OK: todos os casos da tabela foram exercitados e bateram.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
