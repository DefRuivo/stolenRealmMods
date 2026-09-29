#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Bancada de revisao de uma arvore de skills (RV-8b-2c em diante).

Para cada skill da arvore, junta o TEXTO com o CODIGO:
  - `attr`     = AttributeEffects da skill (o que ela muda no personagem)
  - `expr`     = DescriptionExpressions (o array que o [N] indexa)
  - `danoExpr` = DamageExpressionOverrides (o que o *N usa quando a acao nao supre)
  - `acts`     = as acoes concedidas, com os GeneralEffect.Action (a formula de dano)
  - os status citados no texto como {STA=X} -> efeitos/descricao do status

E levanta o que fica SEM PAR no codigo: as porcentagens ditas no texto que nao
aparecem em lugar nenhum dos efeitos. Isso NAO e veredito de bug (o valor pode estar
numa propriedade que o dump ainda nao cobre, ex.: escala por hex), e sim a lista do
que precisa de conferencia humana / triangulacao externa.

Uso:   python tools/verify_tree.py <arvore>
Saida: docs/cobertura/revisao/ficha-<arvore>.md  (+ resumo no stdout)
"""
import csv
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COB = os.path.join(RAIZ, "docs", "cobertura")
SAIDA_DIR = os.path.join(COB, "revisao")

STA = re.compile(r"\{STA=([^}]+)\}")
PCT = re.compile(r"(\d+(?:\.\d+)?)\s*%")
HEX = re.compile(r"(\d+)\s+hex")


def carrega(nome):
    caminho = os.path.join(COB, nome)
    if not os.path.isfile(caminho):
        return {}
    with open(caminho, encoding="utf-8") as fh:
        return {r["nome"]: r for r in csv.DictReader(fh)}


def lista(txt):
    return [x.strip() for x in (txt or "").split(";") if x.strip()]


def main():
    if len(sys.argv) < 2:
        print("uso: python tools/verify_tree.py <arvore>")
        return 1
    arvore = sys.argv[1]
    det, sts, acs = carrega("skills-detalhe.csv"), carrega("status.csv"), carrega("acoes.csv")
    skills = [r for r in csv.DictReader(open(os.path.join(COB, "skills.csv"), encoding="utf-8"))
              if r["arvore"].lower() == arvore.lower()]
    if not skills:
        print("arvore '%s' nao encontrada" % arvore)
        return 1
    skills.sort(key=lambda r: (int(r["tier"] or 0), r["nome"]))
    nomes_repetidos = {}
    for r in skills:
        nomes_repetidos[r["nome"]] = nomes_repetidos.get(r["nome"], 0) + 1

    L = ["# Ficha de revisao — arvore **%s** (%d skills)\n" % (arvore.capitalize(), len(skills)),
         "> Gerado por `tools/verify_tree.py`. Junta o TEXTO da tooltip com o que o jogo\n"
         "> CALCULA. A ultima linha de cada ficha (`conferir`) lista o que **nao** tem par no\n"
         "> codigo — e o que precisa de olho humano ou triangulacao externa, nao veredito.\n"]
    sem_par_total = 0
    for r in skills:
        d = det.get(r["nome"], {})
        passiva = " · **PASSIVA**" if d.get("passivo") == "sim" else ""
        # Nome repetido = variantes da MESMA skill (ex.: Pack Hunter I em T1 e T2, ou os
        # ataques basicos por tipo de arma). Como o join com skills-detalhe e por NOME,
        # o codigo mostrado abaixo pode ser de outra variante - e isso ja gerou falso
        # alarme uma vez. O skid separa as duas.
        repetido = nomes_repetidos.get(r["nome"], 0)
        aviso = (" · ⚠ **nome repetido** (%d variantes — confira o `attr` pelo `skid` em "
                 "`skills-detalhe.csv`)" % repetido) if repetido > 1 else ""
        L.append("\n## T%s %s%s%s\n" % (r["tier"], r["nome"], passiva, aviso))
        L.append("`%s`\n" % r["status"])
        L.append("\n**Texto:** %s\n" % r["descricao"])
        if d.get("attr"):
            L.append("\n**attr:** `%s`\n" % d["attr"])
        if d.get("expr"):
            L.append("\n**expr:** `%s`\n" % d["expr"])
        if d.get("danoExpr"):
            L.append("\n**danoExpr:** `%s`\n" % d["danoExpr"])
        # Acoes concedidas + a formula de dano de cada uma.
        corpo = " ".join([d.get("attr", ""), d.get("expr", ""), d.get("danoExpr", "")])
        # Tira o sufixo 'f' dos literais float do C# (`SummonCount * 5f`): sem isso o
        # `\b` do casamento falha em "5f" e o numero que ESTA no codigo aparece como
        # "sem par" - foi o que acusou Ecosystem (5%) por engano.
        corpo = re.sub(r"\b(\d+(?:\.\d+)?)f\b", r"\1", corpo)
        for nome_ac in lista(d.get("acts")):
            a = acs.get(nome_ac)
            if not a:
                corpo += " " + nome_ac
                continue
            formula = a["efeitosRef"] if a["refAcao"].strip() else a["efeitos"]
            L.append("\n**acao `%s`:** `%s`\n" % (nome_ac, (formula or "-")[:200]))
            corpo += " " + formula
        # Status citados no texto: os numeros podem estar AQUI, nao no caster.
        # Dois caminhos: o token {STA=X} e o NOME do status escrito na propria frase - as
        # marcas dizem "while Tracker's Mark is active" sem token, e so por token elas
        # escapavam do cruzamento (viravam falso alarme de "sem par").
        citados = set(STA.findall(r["descricao"]))
        for nome_st in sorted(sts, key=len, reverse=True):
            if nome_st in citados or len(nome_st) < 4:
                continue
            # Nome PROPRIO, fora dos tokens @...@ : o texto tem a palavra "damage" solta
            # e o censo tem um status chamado "Damage", entao casar sem esse cuidado
            # ligava o status errado (e poluia a ficha com um efeito vazio).
            if re.search(r"(?<![@\w])%s(?![@\w])" % re.escape(nome_st), r["descricao"]):
                citados.add(nome_st)
        # Descarta nome que e pedaco de outro ja casado ("Mark" dentro de "Tracker's Mark").
        citados = {n for n in citados if not any(n != o and n in o for o in citados)}
        for nome_st in sorted(citados):
            s = sts.get(nome_st)
            if not s:
                L.append("\n**status `%s`:** *nao esta no censo de status*\n" % nome_st)
                continue
            L.append("\n**status `%s`:** efeitos=`%s` classe=%s\n"
                     % (nome_st, s["efeitos"] or "-", s["classe"]))
            if s["descricao"]:
                L.append("\n> %s\n" % s["descricao"])
            corpo += " " + s["efeitos"] + " " + s["descricao"]

        # O que o texto afirma e o codigo nao confirma.
        # O strip do sufixo 'f' vale de novo aqui: as formulas das acoes e os efeitos
        # dos status entram no corpo DEPOIS do primeiro strip.
        corpo = re.sub(r"\b(\d+(?:\.\d+)?)f\b", r"\1", corpo)
        sem_par = []
        for p in PCT.findall(r["descricao"]):
            if not re.search(r"[:\s(]%s\b" % re.escape(p), corpo):
                sem_par.append(p + "%")
        for h in HEX.findall(r["descricao"]):
            if not re.search(r"[:\s(]%s\b" % re.escape(h), corpo):
                sem_par.append(h + " hex")
        if sem_par:
            sem_par_total += 1
            L.append("\n**conferir:** %s — sem par no codigo dumpado\n"
                     % ", ".join(sorted(set(sem_par))))
        else:
            L.append("\n**conferir:** tudo o que o texto afirma tem par no codigo — ok\n")

    os.makedirs(SAIDA_DIR, exist_ok=True)
    saida = os.path.join(SAIDA_DIR, "ficha-%s.md" % arvore.lower())
    with open(saida, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    print("%s: %d skills | %d com algo a conferir" % (arvore, len(skills), sem_par_total))
    print("ficha: %s" % saida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
