#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Livro de revisao das tooltips: o ANTES, o DEPOIS e a FONTE de cada ajuste.

Le o proprio fonte do mod (`BetterTooltips/Patches/LocalizePatch.cs`) - as tabelas
`TextFixes` (correcao de texto exato) e `TextAppends` (explicacao adicionada) - e
escreve `docs/cobertura/revisao/ANTES-E-DEPOIS.md`.

Por que gerar em vez de escrever a mao: um livro escrito a mao desatualiza no primeiro
ajuste. Aqui o comentario que acompanha cada entrada no fonte E a justificativa, e a
coluna "onde" casa o texto contra o censo para dizer em qual tooltip ele aparece.

Uso: python tools/review_ledger.py
"""
import csv
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTE = os.path.join(RAIZ, "BetterTooltips", "Patches", "LocalizePatch.cs")
COB = os.path.join(RAIZ, "docs", "cobertura")
SAIDA = os.path.join(COB, "revisao", "ANTES-E-DEPOIS.md")

LITERAL = re.compile(r'"((?:[^"\\]|\\.)*)"')
CAB = ["onde", "antes", "depois", "fonte"]
TABELAS = ("TextFixes", "TextAppends")


def desescapa(s):
    return s.replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")


def le_tabela(txt, nome):
    """[(secao, justificativa, chave, valor)] de uma tabela do fonte.

    Delimita a entrada pela LINHA que e so '{' e pela que comeca com '}' - nunca
    quebrando o bloco por '{', porque varios textos do jogo contem tokens como
    '{STA=Bleeding}' e partiriam a entrada ao meio. Foi o que fez a primeira versao
    contar 18 correcoes quando existem dezenas.
    """
    i = txt.find(nome + " = new Dictionary<string, string>")
    if i < 0:
        return []
    j = txt.find("};", i)
    bloco = txt[i:j]

    entradas, secao, comentarios, literais = [], "", [], []
    for linha in bloco.splitlines():
        s = linha.strip()
        # Comentarios valem para a PROXIMA entrada (secao = cabecalho de bloco).
        if s.startswith("// ----"):
            secao = s.strip("/- ").strip()
            continue
        if s.startswith("//"):
            comentarios.append(s.lstrip("/").strip())
            continue
        # Cada linha que abre com '{' INICIA uma entrada - inclusive o '{' do proprio
        # dicionario, que so serve para zerar o buffer. Ignorar isso fazia o '{' do
        # dicionario engolir todas as entradas de uma vez (o appends zerava).
        if s.startswith("{"):
            literais = []
        for m in LITERAL.finditer(s):
            literais.append(desescapa(m.group(1)))
        # Fecha a entrada quando o FIM da linha e '}' ou '},'. Nao basta "contem '}'":
        # os textos tem tokens como {STA=Bleeding}, que fechariam a entrada no meio. E
        # nao basta "comeca com '}'": a entrada pode ter o valor e o fechamento na mesma
        # linha ('"valor" },'), que foi como 4 entradas minhas sumiram do livro.
        fim = s.rstrip()
        if fim.endswith("}") or fim.endswith("},"):
            if len(literais) >= 2:
                entradas.append((secao, " ".join(comentarios), literais[0], literais[1]))
            comentarios, literais = [], []
    return entradas


def indice_censo():
    """texto -> 'skill X (Shadow)' / 'status Y' — para dizer ONDE o texto aparece."""
    idx = {}
    rotulos = [("skills.csv", "arvore", "skill"), ("status.csv", None, "status"),
               ("itens.csv", None, "item"), ("afixos.csv", None, "afixo"),
               ("powerups.csv", None, "powerup")]
    for arq, col_extra, rotulo in rotulos:
        caminho = os.path.join(COB, arq)
        if not os.path.isfile(caminho):
            continue
        with open(caminho, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                for col in ("descricao", "nome", "efeitos"):
                    v = r.get(col)
                    if v and v not in idx:
                        extra = " (%s)" % r[col_extra] if col_extra and r.get(col_extra) else ""
                        idx[v] = "%s %s%s" % (rotulo, r.get("nome", "?"), extra)
    return idx


def tabela(linhas, cabecalho):
    out = ["| %s |" % " | ".join(cabecalho), "|" + "---|" * len(cabecalho)]
    for c in linhas:
        # Quebra de linha REAL dentro da celula destroi a tabela markdown - e as
        # explicacoes de invocacao tem \n de proposito (uma criatura por linha). Viram
        # <br>, que o markdown renderiza como quebra dentro da celula.
        celulas = [str(x).replace("|", "\\|").replace("\n", "<br>")[:340] for x in c]
        out.append("| " + " | ".join(celulas) + " |")
    return out


def main():
    if not os.path.isfile(FONTE):
        print("fonte nao encontrada: %s" % FONTE)
        return 1
    txt = io.open(FONTE, encoding="utf-8").read()
    idx = indice_censo()
    fixes = le_tabela(txt, "TextFixes")
    appends = le_tabela(txt, "TextAppends")

    L = ["# Tooltips — o antes e o depois de cada ajuste\n",
         "> **Gerado** por `python tools/review_ledger.py` a partir do próprio fonte do mod\n"
         "> (`BetterTooltips/Patches/LocalizePatch.cs`). Editar este arquivo à mão não adianta:\n"
         "> ele é reescrito. A justificativa de cada linha é o comentário que acompanha a\n"
         "> entrada no fonte, e a coluna **onde** é o texto casado contra o censo.\n",
         "\n## Resumo\n",
         "| | quantas |", "|---|---:|",
         "| Correções de texto exato (`TextFixes`) | %d |" % len(fixes),
         "| Explicações adicionadas (`TextAppends`) | %d |" % len(appends),
         "| Regras gerais (não são tabela) | 1 |",
         "\n## Regra geral — normalização de espaços\n",
         "Não é uma entrada de tabela: é uma regra no fim do postfix, que vale para **todo**\n"
         "texto localizado (skills, status, itens, dicas). Entra por último de propósito — as\n"
         "chaves das tabelas casam com o texto ORIGINAL, com os espaços duplos inclusos.\n",
         ]
    L += tabela([("qualquer texto com dois espaços seguidos",
                  "um espaço só",
                  "**Medição no próprio jogo**: `\". \"` aparece **116** vezes contra **77** de "
                  "`\".  \"` — a maioria é um espaço, então os duplos são minoria. Cobre 72 skills "
                  "e também itens/status/dicas, que o censo não lista.")],
                ["antes", "depois", "fonte"])
    L.append("\n> Espaço **no fim** do texto ficou de fora de propósito: é invisível no tooltip e "
             "aparar poderia colar palavras se o jogo concatenar strings (decisão registrada "
             "como `RV-8b-2d`).\n")

    for nome, entradas, nota in (
        ("Correções de texto exato (`TextFixes`)", fixes,
         "O texto original vem do asset do jogo; o substituto é o que o jogador passa a ler. "
         "Chave que não existe no asset **nunca dispara** — `tools/check_fix_keys.py` confere."),
        ("Explicações adicionadas (`TextAppends`)", appends,
         "Aqui o texto original é **mantido** e ganha um parágrafo no fim, com a mecânica que a "
         "tooltip não explicava."),
    ):
        L.append("\n## %s\n" % nome)
        L.append("%s\n" % nota)
        # Agrupa por secao do fonte, preservando a ordem em que as entradas aparecem.
        # Quando a entrada nao tem comentario proprio, herda a da linha acima: no fonte a
        # justificativa e escrita uma vez por BLOCO (ex.: os 5 niveis de Treasure Find
        # compartilham uma explicacao so) - repetir "—" esconderia isso do leitor.
        linhas, secao_atual, ultima = [], object(), ""
        for secao, just, chave, valor in entradas:
            if secao != secao_atual:
                if linhas:
                    L += tabela(linhas, CAB)
                secao_atual, linhas, ultima = secao, [], ""
                L.append("\n**%s**\n" % (secao or "(sem seção no fonte)"))
            onde = idx.get(chave, "*não está no censo* (texto de UI/dica)")
            if just:
                ultima = just
                fonte = just
            else:
                fonte = "↑ *mesma fonte da linha acima*" if ultima else "—"
            linhas.append((onde, chave, valor, fonte))
        if linhas:
            L += tabela(linhas, CAB)

    L.append("\n---\n\n## Que fontes entram neste livro\n")
    L.append("| tipo de fonte | como foi usada |\n|---|---|\n"
             "| **O próprio asset do jogo** (via `docs/cobertura/*.csv`) | é o texto ORIGINAL "
             "que a coluna *antes* mostra — casar contra ele é o que garante que a chave dispara |\n"
             "| **O código do jogo** (`Assembly-CSharp.dll`, decompilado) | quando a tooltip "
             "afirma mecânica ou número: é a fonte que **vence em divergência** |\n"
             "| **O texto do próprio jogo para o status** | confirma número que não está no "
             "caster (ex.: `Patient Hunter`, \"Range increased by 1 per stack\") |\n"
             "| **Medição no jogo** (`tools/audit_tooltips.py`) | decidiu o padrão de espaço "
             "(116 × 77), levantou as famílias de redação divergentes e achou os 9 defeitos de grafia |\n"
             "| **Wiki (Fandom)** | segunda opinião — **parou na v.19** e perdeu para o código "
             "em 3 casos no lote Ranger |\n"
             "| **Patch notes datados** (SteamDB) | a versão mais recente é a verdade; usados "
             "para checar mudanças posteriores à v.19 |\n")

    L.append("\n---\n\n## Como conferir se um ajuste foi aplicado\n")
    L.append("1. `python tools/check_fix_keys.py` — a chave existe no texto do jogo? "
             "Chave que não existe **nunca dispara, e falha em silêncio**.\n")
    L.append("2. Abrir a tooltip no jogo. O mod escreve no log toda vez que muda algo\n"
             "   (`LogOutput.log`, linhas `Better Tooltips:`), então o log é a prova.\n")

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    with open(SAIDA, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    print("TextFixes: %d | TextAppends: %d" % (len(fixes), len(appends)))
    print("livro: %s" % SAIDA)
    return 0


if __name__ == "__main__":
    sys.exit(main())
