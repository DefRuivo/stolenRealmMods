#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Varredura de OMISSAO (regra do usuario, 29/09): a tooltip deixa de fora algo que muda a
decisao do jogador?

Nao basta o texto estar CERTO - ele nao pode estar CERTO PELA METADE. O caso que originou
a regra: as invocacoes diziam "does not inherit your stats" e omitiam que Might aumenta o
dano e Intelligence a vida do bicho.

Classes medidas (tudo a partir do dump do RoguelikeDebugger no LogOutput.log):

  O1  status APLICADO pela acao que o texto nao cita        (ex.: aplica Bleeding e cala)
  O2  numero de GOLPES > 1 que o texto nao diz              ("hits 3 times")
  O3  KNOCKBACK presente e nao citado
  O4  DURACAO: o status aplicado diz "Lasts N turns" e a skill nao fala de turno
  O5  STACK: o status aplicado tem limite de stack e a skill nao fala de stack

Le o LOG (nao o censo) de proposito: os campos de [ActionProps] ainda nao estao no
censo.py, e o log e regenerado a cada ciclo, entao esta sempre atual.

Uso: python tools/check_omissao.py [arvore]
"""
import csv
import io
import os
import re
import sys
from collections import Counter, defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COB = os.path.join(RAIZ, "docs", "cobertura")
SAIDA = os.path.join(COB, "revisao", "omissoes.md")
LOG = ("%USERPROFILE%/AppData/Roaming/r2modmanPlus-local/StolenRealm/"
       "profiles/Default/BepInEx/LogOutput.log")

# Nomes de status que sao palavra comum: casar por eles da falso positivo em massa
# (o censo tem um status chamado "Damage" e o texto de meia duvida de skills tem a palavra).
GENERICOS = {"damage", "health", "armor", "attack", "speed", "move", "movement",
             "power", "chance", "effect", "buff", "debuff", "status", "mana", "magic",
             "range", "hit", "hits", "target", "self", "ally", "enemy", "stack", "stacks"}


def campo(linha, nome):
    m = re.search(re.escape(nome) + r"=([^|]*)", linha)
    return m.group(1).strip() if m else ""


def carrega(nome):
    caminho = os.path.join(COB, nome)
    if not os.path.isfile(caminho):
        return []
    with open(caminho, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def citado(texto, nome):
    """
    O texto cita o status? Aceita o nome inteiro, a palavra, ou o RADICAL de 5 letras.

    O radical existe por causa de dois casos reais que a comparacao por palavra inteira
    errava: "Stunned" x "Stunning Kick" (mesmo radical, palavra diferente) e "Slow" (4
    letras - exigir 5 fazia TODA skill que aplica Slow virar suspeita).
    """
    t = texto.lower()
    if nome.lower() in t:
        return True
    for p in re.findall(r"[A-Za-z]{4,}", nome):
        if p.lower() in GENERICOS:
            continue
        if p.lower() in t or p.lower()[:4] in t:
            return True
    return False


def chaves_do_mod():
    """
    Textos que o mod JA corrige/explica. O censo e o estado ANTES do mod: sem isto a
    varredura acusa para sempre o que ja esta resolvido (os Nature Summoning, por ex.,
    ja tem a lista de bichos na tooltip).
    """
    fonte = os.path.join(RAIZ, "BetterTooltips", "Patches", "LocalizePatch.cs")
    if not os.path.isfile(fonte):
        return set()
    with io.open(fonte, encoding="utf-8") as fh:
        txt = fh.read()
    return {m.group(1).replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")
            for m in re.finditer(r'\{\s*(?://[^\n]*\n\s*)*"((?:[^"\\]|\\.)*)"\s*,', txt)}


def main():
    filtro = sys.argv[1].lower() if len(sys.argv) > 1 else None

    if not os.path.isfile(LOG):
        print("sem log: rode bash scratch/test-cycle.sh 30 \"Debugger\" antes")
        return 1

    props, descs = {}, {}
    for l in io.open(LOG, encoding="utf-8", errors="replace"):
        m = re.search(r"\[ActionProps\] '([^']+)'", l)
        if m:
            props[m.group(1)] = l
        m = re.search(r"\[Skill\] '([^']+)'.*desc=\"(.*)\"", l)
        if m:
            descs.setdefault(m.group(1), m.group(2))

    skills = carrega("skills.csv")
    det = {r["nome"]: r for r in carrega("skills-detalhe.csv")}
    stt = {r["nome"]: r for r in carrega("status.csv")}
    chaves = chaves_do_mod()
    achados = defaultdict(list)
    vistos = Counter()
    cobertos = 0

    for r in skills:
        nome, arvore = r["nome"], r["arvore"]
        if r["status"] in ("intocavel", "sem-explicacao"):
            continue
        if filtro and arvore.lower() != filtro:
            continue
        texto = r["descricao"] or ""
        # O mod ja mexe neste texto (correcao ou explicacao)? Entao nao e omissao pendente:
        # o censo mostra o estado ANTES do mod. Sem este corte os Nature Summoning (que ja
        # ganharam a lista de bichos) apareceriam para sempre.
        if texto in chaves or texto.strip() in chaves:
            cobertos += 1
            continue
        d = det.get(nome, {})
        for ac in [x.strip() for x in (d.get("acts") or "").split(";") if x.strip()]:
            p = props.get(ac)
            if not p:
                continue
            vistos[arvore] += 1

            # O1 - status aplicado e nao citado
            for st in [x for x in campo(p, "statusAplicados").split(",") if x.strip()]:
                # Status que se chama como a propria skill nao precisa ser CITADO: o nome do
                # status e interno e o jogador infere (Ascendancy, Dark Ritual, Blood Howl).
                # Mas isso vale SO para o O1: duracao e stack do status continuam sendo
                # omissao mesmo com o nome batendo (Ascendancy dura 5 turnos e a skill cala).
                auto_nomeado = st.lower() in nome.lower() or nome.lower() in st.lower()
                item = (arvore, nome, st)
                if (not auto_nomeado and not citado(texto, st)
                        and item not in achados["O1 status aplicado nao citado"]):
                    achados["O1 status aplicado nao citado"].append(item)
                s = stt.get(st)
                if not s:
                    continue

                # O4/O5 - o que o proprio texto do status diz e a skill omite.
                # O4 nao vale quando a skill cita o status por OUTRO nome (token {STA=X}):
                # ai o detalhe mora na tooltip do status e nao e omissao.
                sdesc = s.get("descricao") or ""
                m = re.search(r"Lasts? (\d+) turns?", sdesc, re.I)
                if (m and not re.search(r"\bturns?\b", texto, re.I)
                        and (auto_nomeado or not citado(texto, st))):
                    item = (arvore, nome, "status %s: lasts %s turns" % (st, m.group(1)))
                    if item not in achados["O4 duracao omitida"]:
                        achados["O4 duracao omitida"].append(item)
                if re.search(r"stack", sdesc, re.I) and not re.search(r"stack", texto, re.I):
                    item = (arvore, nome, "status %s: %s" % (st, sdesc[:70]))
                    if item not in achados["O5 stack omitido"]:
                        achados["O5 stack omitido"].append(item)

            # O2 - golpes multiplos (o texto pode dizer o numero sem dizer "hits")
            h = campo(p, "hits")
            if h and h != "-" and not re.search(r"\btimes\b|\bhits\b|per hit|\b" + h + r"\b", texto, re.I):
                item = (arvore, nome, "hits=%s" % h)
                if item not in achados["O2 golpes multiplos omitidos"]:
                    achados["O2 golpes multiplos omitidos"].append(item)

            # O3 - knockback
            if campo(p, "knockback") not in ("", "-") and "knock" not in texto.lower():
                item = (arvore, nome, "knockback=%s" % campo(p, "knockback"))
                if item not in achados["O3 knockback omitido"]:
                    achados["O3 knockback omitido"].append(item)

            # O6 - efeito ALEATORIO de uma lista que o texto nao revela. Ex.: "Enchant an
            # ally with a random Chaos Modifier" (Benevolence/Touch of Chaos) - sem saber as
            # opcoes o jogador nao decide nada. E a MESMA classe dos Nature Summoning, que
            # listavam 3 bichos e nao diziam o que cada um faz; la a lista esta no campo de
            # CRIATURAS, aqui no de status. Criterio: 3+ opcoes e o texto cita menos da metade.
            distintos = sorted({x for x in campo(p, "statusAplicados").split(",") if x.strip()})
            if len(distintos) >= 3:
                citados = [s for s in distintos if citado(texto, s)]
                if len(citados) * 2 < len(distintos):
                    item = (arvore, nome, "%d opcoes: %s"
                            % (len(distintos), ", ".join(distintos[:7])))
                    if item not in achados["O6 lista aleatoria nao revelada"]:
                        achados["O6 lista aleatoria nao revelada"].append(item)

    L = ["# Omissoes — o que a tooltip deixa de fora (regra do usuario, 29/09)\n",
         "> Gerado por `tools/check_omissao.py%s`. Le o dump de boot e compara o que o "
         "codigo FAZ com o que o texto DIZ. Texto certo pela metade tambem e defeito.\n"
         % ((" " + filtro) if filtro else "")]
    for classe in sorted(achados):
        itens = achados[classe]
        L.append("\n## %s — %d\n" % (classe, len(itens)))
        L += ["| arvore | skill | o que o codigo tem |", "|---|---|---|"]
        for arv, sk, extra in itens:
            L.append("| %s | %s | %s |" % (arv, sk, extra.replace("|", "/")[:110]))
    if not achados:
        L.append("\nNada encontrado nas classes medidas.\n")

    with io.open(SAIDA, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    print("acoes analisadas por arvore: %s" % dict(vistos))
    print()
    for classe in sorted(achados):
        print("  %-38s %3d" % (classe, len(achados[classe])))
    print("\nrelatorio: %s" % SAIDA)
    return 0


if __name__ == "__main__":
    sys.exit(main())
