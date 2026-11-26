#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rstv_label.py - o ROTULO da aba do Visualizador tem de ser "Arvores" em UTF-8 correto.

O QUE ESTA BIBLIOTECA TRAVA
---------------------------
`SkillTreesTab.TabLabel` e a constante que vira o texto final da 4a aba (a chave "All Trees" nao
existe no dicionario do jogo, entao `OptionsManager.Localize` devolve o proprio literal). A build
0.3.9 foi entregue com o literal corrompido: os bytes de "Á" (U+00C1) foram lidos como latin-1 e
regravados como "Ã" + U+0081, entao a tela mostra `Ã\u0081rvores` em vez de `Arvores` acentuado.

A regra NAO olha comentario: le o literal da constante no codigo efetivo e compara com o caractere
certo, reprovando por codepoint quando diverge. Cobre tambem a forma escrita como escape
(`\\u00C3\\u0081`), que decodifica para o mesmo texto errado.

COMO O ESPERADO E OBTIDO
------------------------
Fonte lido AO VIVO de `RoguelikeSkillTreeVisualizer/SkillTreesTab.cs`. Os plantios devolvem o MESMO
fonte com o defeito reinjetado, em memoria - provam que a checagem reprova pelo motivo certo.
"""
import os
import re
import unicodedata

import arcabouco as arc
import recorte as rec

ROTULO = "\u00c1rvores"          # Árvores
MOJIBAKE = "\u00c3\u0081rvores"  # o defeito entregue na 0.3.9

ASSINATURA = "internal const string TabLabel = "

C1 = set(range(0x80, 0xA0))


def caminho_aba():
    return os.path.join(arc.raiz_do_repo(), "RoguelikeSkillTreeVisualizer", "SkillTreesTab.cs")


def fonte(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def _literal(src):
    """O valor da constante, ou None. Aceita escape unicode e quebra de linha no meio."""
    efetivo = rec.codigo_efetivo(src)
    i = efetivo.find(ASSINATURA)
    if i < 0:
        return None
    bruto = efetivo[i + len(ASSINATURA):]
    if not bruto.startswith('"'):
        return None
    fim = bruto.find('"', 1)
    if fim < 0:
        return None
    return bruto[1:fim].encode("utf-8").decode("unicode_escape").encode("latin-1").decode("utf-8") \
        if "\\u" in bruto[1:fim] else bruto[1:fim]


def _literal_bruto(src):
    efetivo = rec.codigo_efetivo(src)
    i = efetivo.find(ASSINATURA)
    if i < 0:
        return None
    bruto = efetivo[i + len(ASSINATURA):]
    if not bruto.startswith('"'):
        return None
    fim = bruto.find('"', 1)
    return bruto[1:fim] if fim > 0 else None


def pontos(texto):
    return " ".join("U+%04X" % ord(c) for c in texto)


def falhas_do_rotulo(src):
    """Defeitos do rotulo no FONTE. Lista vazia = o texto na tela sai certo."""
    bruto = _literal_bruto(src)
    if bruto is None:
        return ["nao achei a constante %s em SkillTreesTab.cs" % ASSINATURA.strip()]

    escapado = "\\u" in bruto
    valor = _literal(src)
    if valor is None:
        return ["o literal de TabLabel nao fecha com aspas: %r" % bruto]

    falhas = []
    if valor != ROTULO:
        falhas.append("TabLabel decodifica para %r (%s), esperado %r (%s)"
                      % (valor, pontos(valor), ROTULO, pontos(ROTULO)))
    if any(ord(c) in C1 for c in valor):
        falhas.append("TabLabel carrega caractere de controle C1 (%s) - sintoma de UTF-8 lido como latin-1"
                      % pontos(valor))
    if unicodedata.normalize("NFC", valor) != valor:
        falhas.append("TabLabel nao esta em NFC: %s" % pontos(valor))
    if escapado:
        falhas.append("TabLabel esta escrito como escape unicode (%r); o fonte fica ilegivel e o "
                      "defeito volta a passar despercebido" % bruto)
    if valor == MOJIBAKE:
        falhas.append("TabLabel e exatamente o mojibake entregue na 0.3.9: a tela mostra o rotulo corrompido")
    return falhas


def fonte_com_rotulo_corrompido(src):
    """O DEFEITO plantado: o literal volta a ser o mojibake de latin-1."""
    bruto = _literal_bruto(src)
    if bruto is None:
        return src
    return src.replace(ASSINATURA + '"' + bruto + '"', ASSINATURA + '"' + MOJIBAKE + '"', 1)


def fonte_com_rotulo_escapado(src):
    """Variante nova: o MESMO texto errado, agora escrito como escape (todos os tokens de pe)."""
    bruto = _literal_bruto(src)
    if bruto is None:
        return src
    return src.replace(ASSINATURA + '"' + bruto + '"',
                       ASSINATURA + '"\\u00C3\\u0081rvores"', 1)
