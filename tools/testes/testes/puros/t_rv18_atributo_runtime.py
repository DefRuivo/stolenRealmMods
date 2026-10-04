#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RV-18 (03/10) — A ROTA DE SUBSTITUICAO EM RUNTIME das notas de powerup de ATRIBUTO.

POR QUE ESTE TESTE EXISTE
-------------------------
O censo de powerups (RV-10/12) deixou ~25 propostas de nota de ATRIBUTO (5 atributos x 5 niveis)
FORA da entrega porque elas trazem os campos do GlobalSettings como PLACEHOLDER
(`{CritRatingPerDex}`, `{MovementPointPerDexInterval}`, ...). Anexar o texto ASSIM mostra o campo
CRU na tela — pior que nao ter nota.

A ROTA (o que este teste trava): o texto da proposta vive na tabela `AttributePowerupNotes` com os
`{Campo}`; `ResolverCamposDeAtributo` troca cada token pelo valor lido em runtime do MESMO
`GlobalSettingsManager.instance.globalSettings` que o tooltip de stats do jogo usa; e, se sobrar
QUALQUER token, a nota INTEIRA e descartada (nunca o campo cru).

O QUE ELE PRENDE
----------------
  1. ESTRUTURA: a tabela tem os cinco atributos e SEM chave duplicada (INC-1: chave repetida em
     Dictionary derruba o `LocalizePatch` inteiro no construtor estatico); o `BuildAttributeEffects`
     DELEGA para a tabela + o resolvedor — nao ha mais `switch` montando o texto a mao.
  2. COBERTURA: TODO `{Campo}` de TODO template tem campo no mapa `CamposDeAtributoDoGlobalSettings`
     — um token orfao faria a nota sumir (ou, sem a guarda, sair cru).
  3. COMPORTAMENTO (o espelho do C#, exercitado com um mapa de valores de AMOSTRA): os cinco
     templates resolvem para o texto EXATO com os valores, SEM `{`/`}`.
  4. A GUARDA (isca EMBUTIDA): com um token FORA do mapa o resolvedor devolve NADA (a nota nao sai)
     e a versao ingenua (que substitui so o que conhece) DEIXA o placeholder CRU — a checagem
     `tem_placeholder` reprova a segunda. O caso BOM passa a MESMA checagem (a isca nao e decoracao).

LIMITE (o que este teste NAO prova): ele NAO executa o C# do mod (isso pediria a `lib/` do jogo e um
harness por test). A ligacao com o C# e o RECORTE ESTRUTURAL (`recorte.py`) da tabela, do resolvedor
e da delegacao — ancorado em IDENTIFICADOR, nunca em numero de linha. Os VALORES reais do
`GlobalSettings` saem do log do dono; aqui o mapa e de AMOSTRA.
"""
import io
import os
import re
import sys

import arcabouco as arc
import recorte as rec

sys.path.insert(0, os.path.join(arc.raiz_do_repo(), "tools"))
import tabelas as tab  # noqa: E402  o parser UNICO das tabelas do LocalizePatch.cs

META = {
    "nome": "rv18-atributo-runtime",
    "categoria": "pura",
    "requer": [],
    "descricao": "RV-18: as 5 notas de 'Effects per point' dos powerups de ATRIBUTO saem da tabela "
                 "AttributePowerupNotes (com os {Campo}) resolvidas em runtime pelo GlobalSettings "
                 "antes de anexar — nenhum token sai CRU (token sem campo derruba a nota inteira), "
                 "sem chave duplicada (INC-1) e com a delegacao do BuildAttributeEffects presa no fonte",
}

ARQUIVO = os.path.join("BetterTooltips", "Patches", "LocalizePatch.cs")

# Os cinco atributos primarios dos powerups `+ N to <atributo>` (censo: powerups.csv, "revisado").
ATRIBUTOS = ["Might", "Dexterity", "Intelligence", "Vitality", "Reflex"]

# Os 16 campos do GlobalSettings que as propostas citam (o conjunto fecha: nenhum token a mais).
CAMPOS_ESPERADOS = {
    "AbilityPwrPerMight", "AbilityPwrPerMightSummon", "ArmorPercPerMight",
    "CritRatingPerDex", "CritDamagePerDex", "MovementPointPerDexInterval",
    "ManaPerInt", "MaxManaPercPerInt", "RangePerIntInterval", "SummonLifePerInt",
    "MaxHealthPerVit", "MaxHealthPercPerVit",
    "DodgeRatingPerReflex", "DodgeCounterChancePerReflex", "OppAttackPercDmgPerReflex",
    "ExtraCounterAttacksPerReflexInterval",
}

# A AMOSTRA de valores do GlobalSettings (rotulada como tal): o que o jogo leria em runtime entraria
# no lugar destes, pelo MESMO caminho. O valor e o que separa a prova de "texto com buraco".
AMOSTRA = {
    "AbilityPwrPerMight": "1", "AbilityPwrPerMightSummon": "1", "ArmorPercPerMight": "1",
    "CritRatingPerDex": "2", "CritDamagePerDex": "1.5", "MovementPointPerDexInterval": "5",
    "ManaPerInt": "2", "MaxManaPercPerInt": "1", "RangePerIntInterval": "5", "SummonLifePerInt": "2",
    "MaxHealthPerVit": "3", "MaxHealthPercPerVit": "1",
    "DodgeRatingPerReflex": "2", "DodgeCounterChancePerReflex": "5", "OppAttackPercDmgPerReflex": "5",
    "ExtraCounterAttacksPerReflexInterval": "5",
}

# O DEPOIS esperado, valor por valor (fixo, nao derivado do proprio resolvedor).
ESPERADO = {
    "Might": "Effects per point:\n"
             "+1% Damage & Healing\n"
             "+1% Summon Damage\n"
             "+1% Armor & Magic Armor",
    "Dexterity": "Effects per point:\n"
                 "+2 Crit Rating\n"
                 "+1.5% Crit Damage\n"
                 "1 Movement Per 5 Dex (Max 3)",
    "Intelligence": "Effects per point:\n"
                    "+2 Max Mana\n"
                    "+1% Max Mana\n"
                    "1 Skill Range Per 5 Int (Max 3)\n"
                    "+2% Summon Health",
    "Vitality": "Effects per point:\n"
                "+3 Max Health\n"
                "+1% Max Health",
    "Reflex": "Effects per point:\n"
              "+2 Dodge Rating\n"
              "+5% Dodge Counter Chance\n"
              "+5% Opportunity Attack Damage\n"
              "+5% Counter Attack Damage\n"
              "1 Counter Attack a turn Per 5 Reflex (Max 3)",
}


def _codigo():
    with io.open(os.path.join(arc.raiz_do_repo(), ARQUIVO), encoding="utf-8") as fh:
        return fh.read()


def _tabela(codigo):
    """(chaves_na_ordem, {atributo: template}) de `AttributePowerupNotes`, pelo parser UNICO."""
    pares = tab.pares(codigo, "AttributePowerupNotes")
    return [c for c, _v in pares], {c: v for c, v in pares}


def _campos_do_fonte(codigo):
    """Os NOMES dos tokens que o mapa do C# escreve (`{ "Token", gs.Campo... }`)."""
    corpo = rec.corpo_do_metodo(
        codigo, "private static Dictionary<string, string> CamposDeAtributoDoGlobalSettings(")
    return re.findall(r'\{\s*"([A-Za-z][A-Za-z0-9_]*)",\s*gs\.', corpo)


def _tokens(template):
    return re.findall(r"\{([A-Za-z][A-Za-z0-9_]*)\}", template)


# ---------------------------------------------------------------- espelho do C# ---

def resolve(texto, campos):
    """ESPELHO do `ResolverCamposDeAtributo`: None quando um token nao tem valor (a nota inteira e
    descartada). Mesma guarda: `{` sem `}` -> None; sem `{` -> devolve o texto."""
    if not texto or not campos:
        return None
    pedacos, i = [], 0
    while i < len(texto):
        abre = texto.find("{", i)
        if abre < 0:
            pedacos.append(texto[i:])
            break
        fecha = texto.find("}", abre + 1)
        if fecha < 0:
            return None
        pedacos.append(texto[i:abre])
        token = texto[abre + 1:fecha]
        if token not in campos or campos[token] is None:
            return None
        pedacos.append(campos[token])
        i = fecha + 1
    return "".join(pedacos)


def resolve_cru(texto, campos):
    """O DEFEITO (a versao ingenua, "so troca o que conhece"): o token desconhecido FICA CRU.
    E o desenho que o RV-18 proibe — a isca EMBUTIDA da checagem `tem_placeholder`."""
    saida = texto
    for token, valor in campos.items():
        saida = saida.replace("{" + token + "}", valor)
    return saida


def tem_placeholder(texto):
    return "{" in texto or "}" in texto


def corpo():
    codigo = _codigo()

    # ------------------------------------------------------- 1. A ESTRUTURA NO FONTE
    chaves, tabela = _tabela(codigo)
    arc.igual(sorted(tabela), sorted(ATRIBUTOS),
              "a tabela `AttributePowerupNotes` tem de ter os cinco atributos primarios")
    dup = sorted({c for c in chaves if chaves.count(c) > 1})
    arc.igual(dup, [], "chave DUPLICADA em `AttributePowerupNotes` (INC-1: derruba o LocalizePatch "
                       "inteiro no construtor estatico): %s" % dup)

    logica = rec.codigo_efetivo(codigo)   # citacao em comentario nao e codigo
    arc.exigir("switch (attribute)" not in logica,
               "o `BuildAttributeEffects` voltou a montar o texto com `switch` — o texto tem de vir "
               "da tabela `AttributePowerupNotes` (os `{Campo}` resolvidos em runtime)")
    assin_build = "private static string BuildAttributeEffects(string attribute)"
    build = rec.corpo_do_metodo(logica, assin_build)
    rec.exigir_metodo_inteiro(build, assin_build, ('return "\\n" + resolvido;',))
    for marca in ("AttributePowerupNotes.TryGetValue",
                  "ResolverCamposDeAtributo(template, CamposDeAtributoDoGlobalSettings(), out resolvido)",
                  'return "\\n" + resolvido;'):
        arc.exigir(marca in build,
                   "o `BuildAttributeEffects` nao delega pela rota do RV-18 (faltou %r)" % marca)
    arc.exigir(build.count("return null;") >= 3,
               "o `BuildAttributeEffects` tem de ser fail-safe nos ramos (sem atributo, sem template "
               "e resolucao falha) — achei %d `return null;`" % build.count("return null;"))

    assin_res = "private static bool ResolverCamposDeAtributo("
    resolv = rec.corpo_do_metodo(logica, assin_res)
    rec.exigir_metodo_inteiro(resolv, assin_res)
    arc.exigir("campos.TryGetValue(token, out valor)" in resolv,
               "o resolvedor nao consulta o mapa por token")
    arc.exigir("return false;" in resolv, "o resolvedor nao tem a guarda de token ausente")
    arc.exigir("System.Text.StringBuilder" in resolv,
               "o resolvedor tem de remontar o texto (nao pode entregar o template cru)")

    # ------------------------------------------------------- 2. A COBERTURA DOS TOKENS
    campos = _campos_do_fonte(codigo)
    arc.igual(len(campos), len(set(campos)),
              "o mapa `CamposDeAtributoDoGlobalSettings` tem token repetido: %s" % campos)
    arc.igual(set(campos), CAMPOS_ESPERADOS,
              "o mapa tem de trazer os 16 campos das propostas (nem a mais, nem a menos)")
    todos = set()
    for attr in ATRIBUTOS:
        tokens = _tokens(tabela[attr])
        arc.exigir(tokens, "o template de '%s' nao tem NENHUM `{Campo}` (nao e nota de runtime)" % attr)
        orfaos = sorted(set(tokens) - set(campos))
        arc.exigir(not orfaos,
                   "o template de '%s' cita `%s`, sem campo no mapa — esse token faria a nota "
                   "sumir (ou, sem a guarda, sair CRU)" % (attr, ", ".join(orfaos)))
        todos |= set(tokens)
    arc.igual(todos, CAMPOS_ESPERADOS,
              "o conjunto de tokens dos templates tem de bater com o mapa")

    # ------------------------------------------------------- 3. O COMPORTAMENTO (com a amostra)
    for attr in ATRIBUTOS:
        antes = tabela[attr]
        arc.exigir(tem_placeholder(antes),
                   "o ANTES de '%s' tinha de sair CRU (com `{...}`) — e a razao do RV-18" % attr)
        depois = resolve(antes, AMOSTRA)
        arc.exigir(depois is not None,
                   "o resolvedor devolveu NADA para '%s' com o mapa completo" % attr)
        arc.exigir(not tem_placeholder(depois),
                   "o DEPOIS de '%s' ainda tem `{`/`}` (placeholder CRU na tela): %r" % (attr, depois))
        arc.igual(depois, ESPERADO[attr], "o texto resolvido de '%s'" % attr)

    # ------------------------------------------------------- 4. A GUARDA (isca EMBUTIDA)
    sem_um = dict(AMOSTRA)
    sem_um.pop("CritRatingPerDex")
    dex = tabela["Dexterity"]
    arc.exigir("CritRatingPerDex" not in sem_um and len(sem_um) == len(AMOSTRA) - 1,
               "a isca embutida nao removeu o token do mapa (nao plantou nada)")
    arc.igual(resolve(dex, sem_um), None,
              "com um token FORA do mapa o resolvedor tinha de descartar a nota inteira")
    cru = resolve_cru(dex, sem_um)
    arc.exigir(tem_placeholder(cru),
               "a versao INGENUA (que so troca o que conhece) tinha de deixar o campo CRU — a "
               "checagem `tem_placeholder` NAO ve o defeito: %r" % cru)
    arc.exigir("{CritRatingPerDex}" in cru,
               "a isca tinha de deixar exatamente o token `{CritRatingPerDex}` cru: %r" % cru)
    arc.exigir(not tem_placeholder(resolve(dex, AMOSTRA)),
               "a checagem acusou o texto BOM — ela reprova sempre e nao prova nada")

    print("RV-18: %d nota(s) de atributo resolvidas em runtime (%s); %d campo(s) de GlobalSettings"
          % (len(ATRIBUTOS), ", ".join(ATRIBUTOS), len(campos)))
    for attr in ATRIBUTOS:
        print("  [%s]" % attr)
        print("    ANTES  (cru)   : %r" % tabela[attr])
        print("    DEPOIS (amostra): %r" % resolve(tabela[attr], AMOSTRA))
    print("isca embutida: `CritRatingPerDex` fora do mapa -> o resolvedor devolve NADA (a nota nao "
          "sai); a versao ingenua deixa `{CritRatingPerDex}` CRU e a checagem REPROVA — o caso bom "
          "PASSA a mesma checagem")


if __name__ == "__main__":
    arc.main(META, corpo)
