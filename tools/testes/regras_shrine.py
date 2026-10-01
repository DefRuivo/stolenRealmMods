#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_shrine.py - as REGRAS do EXCESSO DE SHRINE em Python puro (familia TST-2).

O QUE E ESTE ARQUIVO
--------------------
A transcricao, em Python, das regras que os testes da familia TST-2 exercitam:
a cadeia do `ShrineEffectBonus`, a escala das 12 auras, a soma por atributo, a
desduplicacao das instancias vivas (RV-46), os itens das auras SEM atributo de
personagem (Dwarven/Decay/Flame) e o formato dos numeros da linha
"Your active shrine auras:".

ONDE ESTE ARQUIVO MORA E POR QUE
--------------------------------
Ele esta em `tools/testes/` (ao lado do `arcabouco.py`) e NAO dentro de
`testes/`: a descoberta do runner so olha `t_*.py` dentro de `testes/`, entao
uma BIBLIOTECA aqui nao vira um teste fantasma nem entra na contagem de
"ignorados". Os testes e as iscas importam este modulo (`import regras_shrine`),
que chega pelo PYTHONPATH que o arcabouco monta para o subprocesso.

DE ONDE VEM CADA COISA (nada aqui e "de cabeca")
------------------------------------------------
* A CONTA: `docs/cobertura/revisao/RV-19-shrines.md` - §2.2 (Mathf.Round(BASE *
  (1 + bonus/100)), half-to-even), §3 (as fontes do ShrineEffectBonus e a
  SUBSTITUICAO do Omnism I pelo II), §4.2/§4.3 (as formulas do dano e a % por
  tipo de inimigo), §9.1/§9.2 (as telas do dono e a aditividade).
* O TEXTO E A REGRA DA LINHA: `BetterTooltips/Patches/ShrineAuraPatch.cs` - cada
  funcao cita `arquivo:linha` da regra que transcreve.
* OS NUMEROS (bases e percentuais): `tools/dados/shrines-esperado.csv` e
  `tools/dados/shrines-percentuais.csv`, GERADOS por
  `tools/gera_shrines_esperado.py` a partir de `docs/cobertura/status.csv` (o
  censo do dump do jogo) e do `resources.assets`. Este modulo NUNCA digita uma
  base nem um percentual: ele LE a tabela versionada e FALHA (exit 1) se ela nao
  estiver la - tabela gerada ausente e defeito do repositorio, nao dependencia.

O VALOR ESPERADO, POR OUTRO LADO, NAO VEM DAQUI
-----------------------------------------------
Vem da fixture `excesso-shrine.esperado.json`, GERADA pelo oraculo em C#
`tools/testes/fixtures/geradores/oraculo_excesso_shrine`, que passa pelo caminho
de conta do motor (aritmetica FLOAT + Math.Round ToEven + Mathf.CeilToInt). Uma
fixture gerada pela MESMA implementacao do teste nao prova nada: por isso o
esperado e do oraculo (C#) e este modulo e a segunda implementacao, que tem de
bater com ele.
"""
import csv
import math
import os

import arcabouco as arc

# ------------------------------------------------------------------ fontes do bonus

# RV-19 §3: as 5 fontes do `ShrineEffectBonus`. `Omnism II` e `Worship` valem 100
# e 20; os 20 e 100 aparecem tambem como `caso_bonus` na tabela gerada e o teste
# confere essa coincidencia.
FONTES = {
    "Omnism I": 8,
    "Omnism II": 20,
    "Horn of Devotion (+50)": 50,
    "Horn of Devotion (+100)": 100,
    "Worship": 100,
}

# RV-19 §3: o motor DESCARTA uma skill quando o personagem conhece alguma das
# `SkillsThatReplace` dela - `Omnism I` e substituida pela `Omnism II`. Com as
# duas tiers o total e 20, NAO 28 (o teste do proprio jogo, `LearnAndExpectAttributeDelta`,
# decompilado l.183505, asserta o delta de 20f).
SUBSTITUI = {
    "Omnism I": "Omnism II",
}

# RV-19 §9.1/§10.5 e o print do dono: o resto (total - contribuicao) e o pedaco da
# ficha que NAO e aura e ele e CONSTANTE entre hovers do mesmo personagem.
RESTO_DO_PRINT = {
    "DamageMod": 25.0,
    "DamageReduction": 20.0,
}

# ShrineAuraPatch.cs l.1545/1549/1553 (`RotuloSemAtributo`): a etiqueta das auras
# cujo efeito NAO e atributo de personagem. A chave no mod e o texto exato da
# descricao do status; aqui o nome da aura da tabela gerada e 1:1 com ela.
ROTULO_SEM_ATRIBUTO = {
    "Dwarven Aura": "Stun chance",
    "Decay Shrine Aura": "Shadow damage per turn",
    "Flame Shrine Aura": "Fire damage to attackers",
}

# A mesma familia da linha viva: ShrineAuraPatch.cs l.319-335 (`ShrineKeys`) e o
# §2 do RV-19 (as 12 auras: 9 de buff + as 3 sem atributo).
AURAS_DA_FAMILIA = (
    "Warrior Aura", "Guardian Aura", "Conqueror Aura", "Rogue Aura", "Reaper Aura",
    "Seraph Aura", "Shaman Aura", "Energy Aura", "Fury",
    "Dwarven Aura", "Decay Shrine Aura", "Flame Shrine Aura",
)

# ------------------------------------------------------------------ a linha (formato)

# ShrineAuraPatch.cs l.984 (`OrdemDosAtributos`): a ordem canonica dos itens da
# linha azul. Um atributo fora desta lista entra depois, na ordem de encontro.
ORDEM_DOS_ATRIBUTOS = (
    "DamageMod", "DamageReduction", "CritChance", "DodgeChance",
    "LifeOnHit", "HealthPerTurnPercent", "ManaPerTurnPercent", "ManaCostMod",
)

SINAL_NEGATIVO = "\u2212"  # menos U+2212, o do mod (ShrineAuraPatch.cs l.927)


# ------------------------------------------------------------------ a conta (motor)


def escala(base, bonus):
    """`Mathf.Round(BASE * (1 + bonus/100))` - fator e produto em FLOAT (RV-19 §2.2).

    A referencia viva e a mesma das outras auras (RV-19 §2.1/§2.2): o `[0]` do
    tooltip sai desta conta. `round` do Python JA e half-to-even, igual ao
    `Math.Round` do jogo.
    """
    fator = arc.f32(1.0 + arc.f32(arc.f32(bonus) / arc.f32(100.0)))
    produto = arc.f32(arc.f32(base) * fator)
    return int(round(produto))


def inteiro_do_jogo(v):
    """`Mathf.CeilToInt` - a convencao da FICHA (ShrineAuraPatch.cs l.950 `InteiroDoJogo`).

    O jogo monta o numero do atributo com `Mathf.Ceil(character[atributo])` +
    `floatToText` (decompilado l.125348-125356 e l.93303-93310): a linha azul usa a
    MESMA grandeza. NaN/infinito (estado corrompido) viram 0 em vez de derrubar.
    """
    if v is None:
        return 0
    f = float(v)
    if math.isnan(f) or math.isinf(f):
        return 0
    return int(math.ceil(arc.f32(f)))


def com_sinal(v):
    """ShrineAuraPatch.cs l.924 (`ComSinal`): "+" para >= 0, U+2212 para negativo.

    O sinal e lido DEPOIS do arredondamento: `-0.4` sai "+0", nunca "-0".
    """
    n = inteiro_do_jogo(v)
    return ("+" if n >= 0 else SINAL_NEGATIVO) + str(abs(n))


def total_com_sinal(nome, v):
    """ShrineAuraPatch.cs l.967 (`TotalComSinal`): o total do parenteses do item.

    `DamageReduction` positivo REDUZ o dano tomado, entao o valor sai invertido (o
    inteiro da ficha e aplicado ANTES da inversao - RV-45).
    """
    n = inteiro_do_jogo(v)
    exibido = -n if nome == "DamageReduction" else n
    return com_sinal(exibido) + "%"


def formatar(atributo, v):
    """ShrineAuraPatch.cs l.897 (`Format`): o rotulo do atributo. None = desconhecido."""
    n = inteiro_do_jogo(v)
    if atributo == "DamageReduction":
        return "Damage taken " + (SINAL_NEGATIVO + str(n) if n > 0 else "+" + str(abs(n))) + "%"
    if atributo == "ManaCostMod":
        if n <= 0:
            return "Mana Costs reduced by " + str(abs(n)) + "%"
        return "Mana Costs increased by " + str(n) + "%"
    prefixos = {
        "DamageMod": "Damage ",
        "CritChance": "Crit Chance ",
        "DodgeChance": "Dodge ",
        "LifeOnHit": "Life Steal ",
        "HealthPerTurnPercent": "Health per turn ",
        "ManaPerTurnPercent": "Mana per turn ",
    }
    if atributo not in prefixos:
        return None
    return prefixos[atributo] + com_sinal(v) + "%"


def item(atributo, contribuicao, total):
    """RV-44 (ShrineAuraPatch.cs l.1087): `<o que as auras entregam> (total <o total>)`."""
    return formatar(atributo, contribuicao) + " (total " + total_com_sinal(atributo, total) + ")"


def dano(maxhealth, pct, bonus, minimo1):
    """O dano das duas auras de perigo (RV-19 §4.2).

    Flame: `Mathf.Max(1,  Mathf.Round((MaxHealth * pct) * (1 + bonus/100)))` -
    tem minimo 1. Decay: a MESMA conta SEM o `Mathf.Max(1,` - pode dar 0.
    `pct` ja em fracao (0.05 = 5%), lido do `shrines-percentuais.csv`.
    """
    fator = arc.f32(1.0 + arc.f32(arc.f32(bonus) / arc.f32(100.0)))
    bruto = arc.f32(arc.f32(arc.f32(maxhealth) * arc.f32(pct)) * fator)
    d = int(round(bruto))
    return max(1, d) if minimo1 else d


# ------------------------------------------------------------------ as tabelas geradas


def _ler_csv_do_repo(nome):
    """Le uma tabela GERADA do repositorio (tools/dados). Ausente = defeito (exit 1)."""
    caminho = os.path.join(arc.raiz_do_repo(), "tools", "dados", nome)
    if not os.path.isfile(caminho):
        raise arc.Falhou(
            "tabela gerada ausente: tools/dados/%s (versionada; gerada por "
            "tools/gera_shrines_esperado.py) - a fonte dos numeros sumiu" % nome)
    with open(caminho, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def tabela_esperado():
    """`tools/dados/shrines-esperado.csv`: base, atributo e contribuicao por caso de bonus."""
    linhas = _ler_csv_do_repo("shrines-esperado.csv")
    if not linhas:
        raise arc.Falhou("tools/dados/shrines-esperado.csv esta VAZIA - a fonte dos numeros sumiu")
    return linhas


def percentuais():
    """`tools/dados/shrines-percentuais.csv` -> ({(aura, tipo): fracao}, {aura: minimo1}).

    A % por tipo de inimigo das acoes `Flame Aura Proc` / `Decay Aura Proc`
    (RV-19 §4.3) e o `minimo1` - que, no asset, so o Flame tem.
    """
    pct, minimo1 = {}, {}
    for linha in _ler_csv_do_repo("shrines-percentuais.csv"):
        pct[(linha["aura"], linha["tipo"])] = float(linha["percentual"]) / 100.0
        minimo1[linha["aura"]] = linha["minimo1"] == "sim"
    if not pct:
        raise arc.Falhou("tools/dados/shrines-percentuais.csv esta VAZIA - a fonte dos percentuais sumiu")
    return pct, minimo1


def auras_da_tabela():
    """{aura: {atributo: base}} da tabela gerada (o par (aura, atributo) e a chave).

    O `Fury` tem DUAS linhas (DamageMod +25 e DamageReduction -25); as auras sem
    atributo de personagem (Dwarven/Decay/Flame) tem a coluna de atributo VAZIA -
    e e isso que a linha azul trata como "item proprio" (RV-46).
    """
    auras = {}
    for linha in tabela_esperado():
        if int(linha["caso_bonus"]) != 0:
            continue
        auras.setdefault(linha["aura"], {})[linha["atributo"]] = float(linha["base"])
    return auras


# ------------------------------------------------------------------ a cadeia do bonus


def fontes_efetivas(fontes):
    """As fontes que CONTAM: uma skill substituida por outra conhecida e descartada (RV-19 §3)."""
    return [f for f in fontes if not (f in SUBSTITUI and SUBSTITUI[f] in fontes)]


def bonus_total(fontes):
    """O `ShrineEffectBonus` do personagem: a SOMA das fontes efetivas (o motor soma o bucket Base).

    RV-19 §3 (§9.2 lembra que o efeito e `Base` e entra somado, `val + parsed2`,
    decompilado l.37256-37271).
    """
    total = 0
    for f in fontes_efetivas(fontes):
        if f not in FONTES:
            raise arc.Falhou("fonte de bonus desconhecida: %r (registre em regras_shrine.FONTES)" % f)
        total += FONTES[f]
    return total


def tabela_de_bonus(entrada):
    """{id do caso: total} a partir da entrada da fixture (as FONTES de cada cena)."""
    return {c["id"]: bonus_total(c["fontes"]) for c in entrada["bonus"]}


# ------------------------------------------------------------------ a linha agregada


def contexto(entrada):
    """Junta tudo que a linha agregada precisa: auras, percentuais, bonus e etiquetas."""
    pct, minimo1 = percentuais()
    return {
        "auras": auras_da_tabela(),
        "pct": pct,
        "minimo1": minimo1,
        "bonus": tabela_de_bonus(entrada),
        "rotulos": ROTULO_SEM_ATRIBUTO,
    }


# ------------------------------------------------------------------ o caso da familia TST-2

CASO = "excesso-shrine"


def entrada_do_caso():
    """A ENTRADA da fixture da familia (um dataset so, compartilhado pelos 4 testes).

    O `caso` da fixture e `excesso-shrine` para os quatro arquivos de teste: e UM
    oraculo e UM par entrada/esperado para a familia inteira (bonus, agregado,
    dano e formatacao sao o mesmo material, olhado por angulos diferentes).
    """
    return arc.ler_json(CASO, "entrada")


def esperado_do_caso():
    """O ESPERADO da fixture - o que o oraculo em C# calculou. Nada aqui e digitado."""
    return arc.ler_json(CASO, "esperado")


def por_id(lista):
    """Indexa uma lista de dicts com `id` (cenas, casos de bonus, casos de formato)."""
    return {x["id"]: x for x in lista}


def contribuicao_do_motor(unicas, atributo, bonus, stacks, ctx):
    """RV-44 (ShrineAuraPatch.cs l.1682 `ContribuicaoDasAuras`): a soma, aura por aura.

    A soma e sobre as auras VIVAS JA DESDUPLICADAS (RV-46) - o motor soma o
    `AttributeEffects` de cada status e o status repetido na lista e a MESMA aura,
    nao uma segunda contribuicao. `stacks` multiplica (l.1733, `TotalStacks` do
    motor, decompilado l.37263: um status vivo tem no minimo 1 stack).
    """
    total = 0
    entrou = []
    for aura in unicas:
        base = ctx["auras"].get(aura, {}).get(atributo)
        if base is None:
            continue
        total += escala(base, bonus) * stacks[aura]
        entrou.append(aura)
    return total, entrou


def vivas_desduplicadas(cena):
    """As auras VIVAS unicas (`AurasUnicas`, l.1220) + os stacks + as repeticoes para o log.

    Cada `instancias` da cena e UMA entrada da lista viva do personagem (cada
    (re)entrada na area do ground effect cria um status NOVO - cabecalho do mod,
    l.1203-1210). A MESMA aura repetida conta UMA vez; as repeticoes voltam como
    `Nome xN` (vao para o LOG, nunca para o numero). `stacks` e o `TotalStacks` do
    status (o motor multiplica o valor por ele - l.1733).
    """
    unicas, contagem, stacks = [], {}, {}
    for viva in cena["vivas"]:
        for _ in range(max(1, int(viva.get("instancias", 1)))):
            aura = viva["aura"]
            if aura in contagem:
                contagem[aura] += 1
                continue
            contagem[aura] = 1
            unicas.append(aura)
            stacks[aura] = max(1, int(viva.get("stacks", 1)))
    repeticoes = [("%s x%d" % (a, contagem[a])) for a in unicas if contagem[a] > 1]
    return unicas, stacks, repeticoes


def agregar(cena, ctx):
    """A linha `Your active shrine auras:` da cena - a transcricao de `AcumuladoShrines`.

    Devolve {"itens", "linha", "repeticoes", "avisos"} com a MESMA forma que o
    oraculo em C# gera (a fixture). Regras, com a citacao:
      * l.1220 `AurasUnicas`  - a mesma aura repetida na lista viva conta UMA vez,
        e as repeticoes vao para o log (`Nome xN`), nunca para o numero.
      * l.1596 `AtributosDasAuras` + l.984 - um item por ATRIBUTO, ordem canonica.
      * l.1682 - a contribuicao e a soma das auras distintas naquele atributo.
      * l.1359/1435/1541 - a aura viva sem atributo de personagem ganha item
        proprio; o que nao virar item sai no LOG com o motivo (a lista se
        apresenta como COMPLETA: nenhuma aura viva pode sumir calada).
      * l.1123 - sem nenhum item, a linha nao sai e o log diz por que.
    """
    bonus = ctx["bonus"][cena["bonus_id"]]
    unicas, stacks, repeticoes = vivas_desduplicadas(cena)

    # um item por atributo, na ordem canonica (o que nao estiver nela entra depois)
    achados = []
    for aura in unicas:
        for atributo in ctx["auras"].get(aura, {}):
            if atributo and atributo not in achados:
                achados.append(atributo)
    atributos = [a for a in ORDEM_DOS_ATRIBUTOS if a in achados]
    atributos += [a for a in achados if a not in atributos]

    itens, avisos, somadas = [], [], []
    for atributo in atributos:
        contrib, entrou = contribuicao_do_motor(unicas, atributo, bonus, stacks, ctx)
        if not entrou:
            continue
        somadas += entrou
        total = cena["totais"].get(atributo)
        if total is None:
            raise arc.Falhou("cena %r: o atributo %r tem contribuicao e a cena nao declarou o total"
                             % (cena["id"], atributo))
        itens.append(item(atributo, contrib, total))

    for aura in unicas:
        if aura in somadas:
            continue
        rotulo = ctx["rotulos"].get(aura)
        if rotulo is None:
            avisos.append("RV-46 AVISO: a aura viva '%s' NAO virou item da linha"
                          " (efeito sem atributo de personagem e sem etiqueta conhecida)" % aura)
            continue
        if aura == "Dwarven Aura":
            if not any(v["aura"] == aura and v.get("expressao", True) for v in cena["vivas"]):
                avisos.append("RV-46 AVISO: a aura viva '%s' NAO virou item da linha"
                              " (sem expressao de chance avaliada)" % aura)
                continue
            itens.append(rotulo + " " + com_sinal(escala(ctx["auras"][aura][""], bonus)) + "%")
        elif aura == "Decay Shrine Aura":
            if float(cena["maxhealth"]) <= 0.0:
                avisos.append("RV-46 AVISO: a aura viva '%s' NAO virou item da linha"
                              " (receptor sem MaxHealth)" % aura)
                continue
            d = dano(cena["maxhealth"], ctx["pct"][(aura, cena["tipo_receptor"])], bonus,
                     ctx["minimo1"][aura])
            itens.append(rotulo + " " + ("%g" % d))
        elif aura == "Flame Shrine Aura":
            valores = []
            for alvo in cena["alvos"]:
                if float(alvo["maxhealth"]) <= 0.0:
                    continue
                b = ctx["bonus"][alvo["bonus_id"]]
                d = dano(alvo["maxhealth"], ctx["pct"][(aura, alvo["tipo"])], b, ctx["minimo1"][aura])
                valores.append(alvo["nome"] + " " + ("%g" % d))
            if not valores:
                avisos.append("RV-46 AVISO: a aura viva '%s' NAO virou item da linha"
                              " (nenhum alvo com o status do Flame vivo agora)" % aura)
                continue
            itens.append(rotulo + ": " + ", ".join(valores))
        else:
            avisos.append("RV-46 AVISO: a aura viva '%s' NAO virou item da linha"
                          " (efeito sem atributo de personagem sem item implementado)" % aura)

    if not itens:
        avisos.append("RV-46 sem linha: %d aura(s) viva(s) sem nenhum numero provado (nada estimado)"
                      % len(unicas))
        linha = ""
    else:
        linha = "Your active shrine auras: " + "; ".join(itens) + "."
    return {"itens": itens, "linha": linha, "repeticoes": repeticoes, "avisos": avisos}
