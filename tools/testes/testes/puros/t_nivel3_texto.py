#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NIV3-2 — o TEXTO da linha de nivel 3 (sinergia status x skill), preso pela FONTE.

O DEFEITO (achado da DOC-17)
----------------------------
A linha de nivel 3 que o NIV3-1 passou a recolher — `Your skills on this status: <skill> +N% damage
per stack` (o bloco do `StatusSkillSynergyPatch`) — **nao tinha NENHUM teste que prendesse o TEXTO**
dela (grep no repo: zero). E ela JA estava documentada com o **SINAL INVERTIDO**: o documento
mostrava `+2% damage per stack` para o `Frostbite I` quando o valor avaliado pelo motor e **-2** e o
`ComSinal` do patch imprime o menos **U+2212** para negativo. A prova de qual e o certo e a LINHA DE
LOG REAL do jogo (01/10):

    [CHL-1] status 'Chilled' char=Shriner: -(Source["ChilledDamageReduction"]) = -2
        -> 'Frostbite I \u22122% damage per stack' (skills=[Frostbite I])

(`scratch/cap1/out/log-anterior-antes-da-rotina.log:9735`; o byte do menos e **U+2212**, nao o hifen
ASCII `-`.) O documento foi corrigido pela DOC-17, mas **nada prendia o codigo a ele**. Uma linha de
estado que o jogador LE merece o mesmo tratamento do resto: o texto sai da FONTE e e conferido
contra a prova.

O QUE ESTE TESTE PRENDE
-----------------------
  1. O PREFIXO. O marcador lido do fonte (`StatusSkillSynergyPatch.Marcador`) e
     `Your skills on this status:` e e o prefixo da linha.
  2. A JUNCAO. Varias skills no rotulo de UM item sao unidas pelo separador do proprio fonte
     (`string.Join(" + ", nomes)`); varios ITENS sao unidos por `string.Join("; ", itens)`.
  3. O SINAL, NOS DOIS CASOS. Positivo sai com `+`; negativo sai com o menos **U+2212** (o mesmo do
     `ComSinal`), **NUNCA** com o hifen ASCII. O item negativo do caso real e exatamente
     `Frostbite I \u22122% damage per stack` — o item da linha de log do jogo.
  4. O CASO DE UMA SKILL SO e o de VARIAS SKILLS (as duas juncões e o item por pilha).

COMO O ESPERADO E ANCORADO
--------------------------
Nenhum pedaco do texto e digitado a mao: o marcador, os DOIS caracteres de sinal, o separador de
skills, o de itens, o espaco do rotulo, o sufixo ` per stack`, o ponto final e as frases por atributo
afetado (`% damage`, `% Max Health`) sao LIDOS DO FONTE pelos **identificadores** (nunca por numero
de linha). A composicao (na mesma ordem do `Bloco`) e entao comparada com a FORMA REAL — a linha de
log do jogo — e com a cor do nivel 3 da paleta (`reg.cor_da_linha_azul`).

NAO MUDA COMPORTAMENTO: o teste so LE. O bloco continua sendo nivel 3 para o NIV3-1 (a ordem relativa
a aura e **IMPOSTA NO CODIGO** — `aura = sinergia + "\\n\\n" + aura`, §9.1 do TEXTO-TOOLTIPS.md; quem
a trava e `t_nivel3_sinergia.py`). Aqui so se prega o TEXTO.

A PROVA DE QUE REPROVA: `_o_sinal_invertido_reprova` planta a inversao **EM MEMORIA** (o arquivo nao
e tocado) e exige que a checagem caia — PELO MOTIVO CERTO (o sinal). A rodada FISICA, com o fonte
plantado numa COPIA e restaurado byte a byte (sha256 conferido), esta em
`tools/testes/niv3-texto-prova.log`.
"""
import os
import re

import arcabouco as arc
import regras_cor as reg

META = {
    "nome": "nivel3-texto",
    "categoria": "pura",
    "requer": [],
    "descricao": "NIV3-2: o TEXTO da linha de nivel 3 (sinergia) preso pela FONTE — o prefixo, a "
                 "juncao de skills/itens e o SINAL nos dois casos (U+2212 no negativo, nao hifen); "
                 "o sinal invertido e o hifen REPROVAM",
}

# O menos do mod (U+2212) e o que NAO pode aparecer no lugar dele.
SINAL_NEGATIVO = "\u2212"
SINAL_POSITIVO = "+"
HIFEN_ASCII = "-"

MARCADOR_ESPERADO = "Your skills on this status:"

# A PROVA REAL: a linha de log do jogo (01/10) e o item que ela mostra.
LOG_DO_JOGO = ("status 'Chilled' char=Shriner: -(Source[\"ChilledDamageReduction\"]) = -2 "
               "-> 'Frostbite I \u22122% damage per stack' (skills=[Frostbite I])")
ITEM_REAL_NEGATIVO = "Frostbite I \u22122% damage per stack"

# As formas presas: a composicao lida da fonte tem de bater EXATAMENTE com elas.
LINHA_NEGATIVA_UMA_SKILL = "Your skills on this status: Frostbite I \u22122% damage per stack."
LINHA_POSITIVA_UMA_SKILL = "Your skills on this status: Frostbite I +2% damage per stack."
LINHA_NEGATIVA_VARIAS_SKILLS = ("Your skills on this status: Frostbite I + Frozen Core "
                                "\u22122% damage per stack.")
LINHA_NEGATIVA_VARIOS_ITENS = ("Your skills on this status: Frostbite I \u22122% damage per stack; "
                               "Frozen Core \u22125% Max Health per stack.")

ARQUIVO_DO_PATCH = "StatusSkillSynergyPatch.cs"


# ------------------------------------------------------------------ o fonte ---

def _fonte(codigo=None):
    """O fonte do bloco de sinergia (ou o `codigo` passado, para a prova em memoria).

    O caminho sai de `reg.FONTE_MOD` (o `LocalizePatch.cs`, no mesmo diretorio), entao a prova
    FISICA pode apontar `reg.FONTE_MOD` para uma COPIA e exercitar o teste contra ela sem tocar
    no arquivo do repo.
    """
    if codigo is not None:
        return codigo
    caminho = os.path.join(os.path.dirname(reg.FONTE_MOD), ARQUIVO_DO_PATCH)
    arc.exigir(os.path.isfile(caminho), "o fonte do bloco de sinergia sumiu: %s" % caminho)
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def _extrai(padrao, codigo, o_que):
    m = re.search(padrao, codigo)
    if not m:
        raise arc.Falhou("nao achei %s no fonte do `%s` (padrao %r)" % (o_que, ARQUIVO_DO_PATCH, padrao))
    return m.group(1)


def _pecas(codigo=None):
    """As pecas do TEXTO, LIDAS DO FONTE pelos identificadores (nunca por numero de linha)."""
    codigo = _fonte(codigo)
    frases = {}
    for m in re.finditer(r'case\s+"([^"]+)"\s*:\s*return\s+"([^"]*)"', codigo):
        frases[m.group(1)] = m.group(2)
    for atributo in ("DamageMod", "MaxHealth"):
        if atributo not in frases:
            raise arc.Falhou("a `FraseDoAfetado` perdeu o `case %r` (a redacao do atributo afetado)"
                             % atributo)
    return {
        "marcador": _extrai(r'internal\s+const\s+string\s+Marcador\s*=\s*"([^"]+)"',
                            codigo, "o marcador do bloco"),
        "negativo": _extrai(r'v\s*<\s*0f\s*\?\s*"([^"]*)"\s*:', codigo,
                            "o sinal NEGATIVO do `ComSinal`"),
        "positivo": _extrai(r'v\s*<\s*0f\s*\?\s*"[^"]*"\s*:\s*"([^"]*)"', codigo,
                            "o sinal POSITIVO do `ComSinal`"),
        "sep_skills": _extrai(r'nomes\.Count\s*>\s*0\s*\?\s*string\.Join\(\s*"([^"]*)"', codigo,
                              "a juncao de varias skills no rotulo"),
        "sep_itens": _extrai(r'string\.Join\(\s*"([^"]*)"\s*,\s*itens', codigo,
                             "a juncao de varios itens"),
        "espaco": _extrai(r'Marcador\s*\+\s*"([^"]*)"\s*\+\s*string\.Join', codigo,
                          "o espaco depois do marcador"),
        "espaco_item": _extrai(r'rotulo\s*\+\s*"([^"]*)"\s*\+\s*ComSinal', codigo,
                               "o espaco entre o rotulo e o sinal"),
        "per_stack": _extrai(r'PerStack\s*\?\s*"([^"]*)"\s*:\s*""', codigo,
                             "o sufixo dos efeitos por pilha"),
        "termino": _extrai(r'itens\.ToArray\(\)\)\s*\+\s*"([^"]*)"', codigo,
                           "o termino do bloco"),
        "frases": frases,
    }


# --------------------------------------------------------------- composicao ---

def _numero(v):
    """O `ToString("0.#")` do `ComSinal`: inteiro nao ganha `.0`; uma casa quando ha fracao."""
    v = abs(float(v))
    if v == int(v):
        return str(int(v))
    return ("%.1f" % v).rstrip("0").rstrip(".")


def com_sinal(valor, codigo=None):
    """O `ComSinal` do patch: `+` para >= 0, o menos U+2212 para negativo."""
    p = _pecas(codigo)
    return (p["negativo"] if valor < 0 else p["positivo"]) + _numero(valor)


def rotulo_de_skills(nomes, codigo=None):
    """O rotulo de UM item: varias skills unidas pelo separador do fonte (uma so sai inalterada)."""
    p = _pecas(codigo)
    if not nomes:
        raise arc.Falhou("o rotulo do item precisa de pelo menos uma skill")
    return p["sep_skills"].join(nomes)


def item(rotulo, valor, afetado="DamageMod", per_stack=True, codigo=None):
    """A `string item = rotulo + " " + ComSinal(valor) + FraseDoAfetado(...) + (PerStack ? ...)`."""
    p = _pecas(codigo)
    return (rotulo + p["espaco_item"] + com_sinal(valor, codigo) + p["frases"][afetado]
            + (p["per_stack"] if per_stack else ""))


def linha(itens, codigo=None):
    """O texto da linha de nivel 3 (sem markup): marcador + espaco + itens + ponto."""
    p = _pecas(codigo)
    termino = p["termino"]
    ponto = termino[:-len(reg.FECHA_COR)] if termino.endswith(reg.FECHA_COR) else termino
    return p["marcador"] + p["espaco"] + p["sep_itens"].join(itens) + ponto


def bloco(itens, codigo=None):
    """O bloco INTEIRO como o `Bloco` o devolve: UMA quebra CRUA na frente e a cor do nivel 3."""
    return ("\n" + reg.ABRE_COR + reg.cor_da_linha_azul() + ">" + linha(itens, codigo)
            + reg.FECHA_COR)


# ----------------------------------------------------------------- a trava ---

def verifica_texto(codigo=None):
    """A trava inteira do TEXTO, na forma do `Bloco`. Levanta `arc.Falhou` na primeira divergencia."""
    p = _pecas(codigo)

    # (1) O PREFIXO.
    arc.exigir(p["marcador"].startswith("Your skills on this status"),
               "o marcador do nivel 3 nao comeca com 'Your skills on this status': %r" % p["marcador"])
    arc.igual(p["marcador"], MARCADOR_ESPERADO, "o marcador do bloco de sinergia")

    # (2) O SINAL — o que a DOC-17 corrigiu.
    arc.igual(p["negativo"], SINAL_NEGATIVO,
              "o sinal NEGATIVO do `ComSinal` tem de ser o menos U+2212, nao o hifen ASCII %r "
              "(o valor de `Frostbite I` e -2): veio %r" % (HIFEN_ASCII, p["negativo"]))
    arc.igual(p["positivo"], SINAL_POSITIVO, "o sinal POSITIVO do `ComSinal`")
    arc.exigir(p["negativo"] != p["positivo"],
               "os dois sinais do `ComSinal` viraram o mesmo caractere: %r" % p["negativo"])

    # (3) A JUNCAO e o resto da forma.
    arc.igual(p["sep_skills"], " + ", "a juncao de varias skills no rotulo de um item")
    arc.igual(p["sep_itens"], "; ", "a juncao de varios itens")
    arc.igual(p["espaco"], " ", "o espaco depois do marcador")
    arc.igual(p["espaco_item"], " ", "o espaco entre o rotulo e o sinal")
    arc.igual(p["per_stack"], " per stack", "o sufixo dos efeitos por pilha")

    # (4) O SINAL NOS DOIS CASOS.
    arc.igual(com_sinal(-2.0, codigo), SINAL_NEGATIVO + "2", "o valor -2 (Frostbite I) com sinal")
    arc.igual(com_sinal(2.0, codigo), "+2", "um valor +2 com sinal")
    arc.exigir(HIFEN_ASCII not in com_sinal(-2.0, codigo),
               "o valor negativo saiu com hifen ASCII: %r" % com_sinal(-2.0, codigo))

    # (5) UMA skill so — negativo (o item REAL do log) e positivo.
    neg = item(rotulo_de_skills(["Frostbite I"], codigo), -2.0, codigo=codigo)
    pos = item(rotulo_de_skills(["Frostbite I"], codigo), 2.0, codigo=codigo)
    arc.igual(neg, ITEM_REAL_NEGATIVO,
              "o item do caso REAL (Chilled + Frostbite I) tem de ser o da linha de log do jogo")
    arc.igual(linha([neg], codigo), LINHA_NEGATIVA_UMA_SKILL, "a linha com UMA skill, negativa")
    arc.igual(linha([pos], codigo), LINHA_POSITIVA_UMA_SKILL, "a linha com UMA skill, positiva")
    arc.exigir(HIFEN_ASCII not in linha([neg], codigo),
               "a linha negativa saiu com hifen ASCII: %r" % linha([neg], codigo))
    arc.exigir(SINAL_NEGATIVO in linha([neg], codigo), "a linha negativa perdeu o U+2212")

    # (6) VARIAS skills no rotulo de UM item (o `string.Join(" + ", nomes)`).
    varias = item(rotulo_de_skills(["Frostbite I", "Frozen Core"], codigo), -2.0, codigo=codigo)
    arc.igual(linha([varias], codigo), LINHA_NEGATIVA_VARIAS_SKILLS,
              "a linha com VARIAS skills no mesmo item (a juncao com ' + ')")

    # (7) VARIOS itens (o `string.Join("; ", itens)`) — o segundo efeito real do Chilled.
    segundo = item(rotulo_de_skills(["Frozen Core"], codigo), -5.0, afetado="MaxHealth",
                   codigo=codigo)
    arc.igual(linha([neg, segundo], codigo), LINHA_NEGATIVA_VARIOS_ITENS,
              "a linha com os DOIS itens do Chilled (a juncao com '; ')")

    # (8) O BLOCO: UMA quebra CRUA na frente e a cor do nivel 3 (o que o NIV3-1 deixa para o prefixo).
    b = bloco([neg], codigo)
    arc.exigir(b.startswith("\n" + reg.ABRE_COR + reg.cor_da_linha_azul() + ">"),
               "o bloco tem de comecar com UMA quebra CRUA e a cor do nivel 3: %r" % b)
    arc.exigir(b.endswith(reg.FECHA_COR), "o bloco tem de fechar o `</color>`: %r" % b)
    arc.igual(b, "\n" + reg.ABRE_COR + reg.cor_da_linha_azul() + ">" + LINHA_NEGATIVA_UMA_SKILL
              + reg.FECHA_COR, "o bloco inteiro do caso real")
    return p, neg


# ------------------------------------------------------------------- prova ---

def _plantio(codigo, de, para, o_que):
    arc.igual(codigo.count(de), 1,
              "o plantio de %s tinha de achar o trecho UMA vez (o fonte mudou?): %d"
              % (o_que, codigo.count(de)))
    return codigo.replace(de, para, 1)


def _reprova_pelo_motivo(codigo_mutado, o_que):
    """A checagem tem de CAIR, e por um motivo que nombra o SINAL — nao por outra coisa."""
    try:
        verifica_texto(codigo_mutado)
    except arc.Falhou as erro:
        mensagem = str(erro)
        arc.exigir("sinal" in mensagem.lower() or "U+2212" in mensagem,
                   "%s foi pego, mas por um motivo que nao e o do NIV3-2 (o sinal): %s"
                   % (o_que, mensagem))
        return mensagem
    raise arc.Falhou("%s PASSOU — a trava do texto do nivel 3 e decoracao" % o_que)


def _o_sinal_invertido_reprova():
    """A PROVA (em memoria, o arquivo nao e tocado): o sinal invertido e o hifen ASCII tem de REPROVAR.

    O `ComSinal` do fonte e `v < 0f ? "U+2212" : "+"`. A inversao troca os DOIS caracteres (o
    negativo passa a sair com `+`, que foi o defeito da DOC-17); o outro plantio troca o U+2212
    pelo hifen ASCII. Os dois tem de ser vistos.
    """
    codigo = _fonte()
    de = '? "' + SINAL_NEGATIVO + '" : "' + SINAL_POSITIVO + '"'

    invertido = _plantio(codigo, de, '? "' + SINAL_POSITIVO + '" : "' + SINAL_NEGATIVO + '"',
                         "a inversao do sinal")
    # o efeito do defeito, explicitamente: com o sinal invertido o valor -2 sai '+2' — exatamente o
    # texto que a DOC-17 tinha documentado errado.
    arc.igual(linha([item(rotulo_de_skills(["Frostbite I"], invertido), -2.0, codigo=invertido)],
                    invertido), LINHA_POSITIVA_UMA_SKILL,
              "o plantio nao reproduziu o defeito da DOC-17 (o valor -2 saindo '+2')")
    razao_invertido = _reprova_pelo_motivo(invertido, "o sinal INVERTIDO")

    hifen = _plantio(codigo, de, '? "' + HIFEN_ASCII + '" : "' + SINAL_POSITIVO + '"',
                     "o hifen ASCII no lugar do U+2212")
    razao_hifen = _reprova_pelo_motivo(hifen, "o hifen ASCII no lugar do menos U+2212")
    return razao_invertido, razao_hifen


def corpo():
    # ---------------------------------------------------- 1. A TRAVA DO TEXTO
    _p, neg = verifica_texto()

    # ---------------------------------------------------- 2. A PROVA REAL (o log)
    i = LOG_DO_JOGO.index("-> '") + len("-> '")
    j = LOG_DO_JOGO.index("' (skills=", i)
    arc.igual(LOG_DO_JOGO[i:j], ITEM_REAL_NEGATIVO,
              "o item preso tem de ser o da linha de log do jogo (as aspas do log)")
    arc.exigir(SINAL_NEGATIVO in ITEM_REAL_NEGATIVO and HIFEN_ASCII not in ITEM_REAL_NEGATIVO,
               "a prova real tem de trazer o U+2212 e nenhum hifen: %r" % ITEM_REAL_NEGATIVO)

    # ---------------------------------------------------- 3. O SINAL INVERTIDO REPROVA
    razao_invertido, razao_hifen = _o_sinal_invertido_reprova()

    print("NIV3-2 fechado: a linha de nivel 3 e composta DA FONTE (marcador %r, juncao de skills "
          "%r, juncao de itens %r) e bate com a linha de log do jogo (%r); o caso positivo usa '+' "
          "e o negativo usa o U+2212. O plantio em memoria REPROVOU nos DOIS defeitos: a inversao "
          "(%s) e o hifen ASCII (%s)"
          % (_pecas()["marcador"], _pecas()["sep_skills"], _pecas()["sep_itens"], neg,
             razao_invertido, razao_hifen))


if __name__ == "__main__":
    arc.main(META, corpo)
