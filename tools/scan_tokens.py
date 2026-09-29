#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
RV-8 (fase 1) - Varredura de tooltips segundo a GRAMATICA REAL do jogo.

Objetivo: separar "texto que parece placeholder" de "texto que realmente quebra".
A primeira tentativa desta varredura (29/09) tratou todo `[...]` como suspeito e
acusou 102 casos - **todos falsos positivos**. O motivo e que o jogo tem TRES
pipelines de texto diferentes, e o mesmo colchete significa coisas distintas:

  1) DESCricao de SKILL / STATUS / POWERUP -> `Tooltip.ApplyDescriptionExpressions`
       ApplyAttributeTextTags roda antes: "[[X]]" -> "<b>nome do atributo</b>".
       Depois, para cada "[":
            char c = text[pos+1];                        // UM caractere
            if (!int.TryParse(c, out N))
                return "Parsing Error with: " + c;       // ABORTA o tooltip
            value = eval(expressions[N]);                // indice de expressao
            text.Remove(pos, 3);                         // remove "[N" + 1 char
       -> "[" sem digito QUEBRA o tooltip; "[NN]" (2+ digitos) le so o primeiro
          digito, remove 3 chars e usa a expressao ERRADA.

  2) ITEM -> `OptionsManager.Localize(OptionalDescription).Replace("[token]", v)`
       Os `[...]` aqui sao TOKENS NOMEADOS de template ("[level value]",
       "{SKL=...}") trocados pelo chamador. Nao passam pela regra (1).

  3) AFIXO de item -> mesmo esquema de template; "[15]" e o valor rolado do afixo.

Por isso a varredura e feita POR CATEGORIA, com a gramatica esperada de cada uma.
O que interessa e o resultado nas categorias de EXPRESSAO: alerta ali e candidato
a bug real.

Uso:   python tools/scan_tokens.py
Saida: docs/cobertura/alerta-tokens.md
"""
import csv
import glob
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COBERTURA = os.path.join(RAIZ, "docs", "cobertura")
SAIDA = os.path.join(COBERTURA, "alerta-tokens.md")

# categoria -> gramatica esperada do texto da descricao
GRAMATICA = {
    "skills":   "expressao",
    "status":   "expressao",
    "powerups": "expressao",
    "itens":    "template",
    "afixos":   "template",
}

ATRIBUTO = re.compile(r"\[\[[^\]]*\]\]")


def analisa(desc):
    """Aplica a gramatica de expressao e devolve os achados (classe, detalhe)."""
    s = ATRIBUTO.sub("", desc or "")     # ApplyAttributeTextTags ja consumiu os [[X]]
    achados = []
    i = 0
    while True:
        i = s.find("[", i)
        if i < 0:
            break
        prox = s[i + 1:i + 2]
        if not prox.isdigit():
            achados.append(("A", "`[%s` - sem digito depois do `[`" % prox))
            break                        # o jogo aborta aqui mesmo
        fim = i + 1
        while fim < len(s) and s[fim].isdigit():
            fim += 1
        if fim - (i + 1) > 1:
            achados.append(("B", "indice `[%s]` com 2+ digitos" % s[i + 1:fim]))
        i = fim
    return achados


def main():
    alertas = {"A": [], "B": []}
    esperados = []
    total = 0
    for arq in sorted(glob.glob(os.path.join(COBERTURA, "*.csv"))):
        cat = os.path.basename(arq)[:-4]
        gram = GRAMATICA.get(cat, "expressao")
        with open(arq, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                total += 1
                achados = analisa(r.get("descricao", ""))
                if not achados:
                    continue
                linha = (cat, r.get("nome", ""), achados[0][1], r.get("descricao", ""))
                if gram == "template":
                    esperados.append(linha)
                else:
                    alertas[achados[0][0]].append(linha)

    L = []
    L.append("# Varredura de tokens das tooltips — resultado\n")
    L.append("> Gerado por `python tools/scan_tokens.py` • %d entradas varridas.\n" % total)
    L.append("**Regra extraída do código** (`Tooltip.ApplyDescriptionExpressions`): em "
             "descrição de skill/status/powerup, `[` sem dígito devolve "
             "`Parsing Error with:` **no lugar do tooltip inteiro**, e `[NN]` (2+ dígitos) "
             "faz o jogo ler só o primeiro dígito e usar a expressão errada.\n")

    n = len(alertas["A"]) + len(alertas["B"])
    L.append("\n## Veredito\n")
    if n == 0:
        L.append("**Nenhum caso nas categorias de expressão** (skills, status, powerups). "
                 "Ou seja: os `[...]` que aparecem no censo **não são** placeholders vazando — "
                 "cada um pertence a um pipeline que o jogo resolve.\n")
    else:
        L.append("**%d candidato(s) a bug real** — categorias de expressão, onde o texto "
                 "NÃO é template:\n" % n)

    for classe, titulo in (("A", "Classe A — `[` sem dígito (quebra o tooltip)"),
                           ("B", "Classe B — índice de 2+ dígitos (valor errado)")):
        L.append("\n### %s\n" % titulo)
        itens = alertas[classe]
        if not itens:
            L.append("Nenhum caso.\n")
            continue
        L.append("| categoria | entrada | detalhe | descricao |")
        L.append("|---|---|---|---|")
        for cat, nome, det, desc in itens:
            L.append("| %s | %s | %s | %s |"
                     % (cat, nome.replace("|", "\\|"), det, desc.replace("|", "\\|")[:120]))

    L.append("\n## Esperado (não é bug): categorias de template\n")
    L.append("`itens` e `afixos` usam `Localize(...).Replace(\"[token]\", valor)` — os "
             "colchetes ali são tokens nomeados trocados pelo próprio chamador. "
             "**%d ocorrências**, todas esperadas.\n" % len(esperados))
    if esperados:
        L.append("<details><summary>ver a lista</summary>\n")
        L.append("| categoria | entrada | detalhe | descricao |")
        L.append("|---|---|---|---|")
        for cat, nome, det, desc in esperados:
            L.append("| %s | %s | %s | %s |"
                     % (cat, nome.replace("|", "\\|"), det, desc.replace("|", "\\|")[:100]))
        L.append("\n</details>\n")

    with open(SAIDA, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    print("varridas: %d entradas" % total)
    print("ALERTAS nas categorias de expressao (skills/status/powerups): %d "
          "(A=%d, B=%d)" % (n, len(alertas["A"]), len(alertas["B"])))
    print("esperados por template (itens/afixos): %d" % len(esperados))
    print("relatorio: %s" % SAIDA)
    return 0


if __name__ == "__main__":
    sys.exit(main())
