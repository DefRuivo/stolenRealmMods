#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PARSER-1: o ponto cego do COMENTARIO entre a abertura `{` e a chave — a prova REPROVANDO.

O DEFEITO (o 4o irmao da mesma familia de leitor): um parser que casa `{ "chave", "valor" }`
com um regex exigindo a aspa logo depois do `{` NAO VE as entradas com COMENTARIO entre a
abertura e a chave — nem o de LINHA (`//`) nem o de BLOCO (`/* */`). A entrada some da
varredura EM SILENCIO. Foi o furo do COR-2 (comentario de linha no
`check_notas_redundantes.py`), do FIX-4 (comentario de bloco, idem) e — o que este teste
prende — o do REGEX que vivia em `regras_cor._entradas`, que alimentava o alcance do COR-3
(`scratch/cor3/cor3_alcance.py`) com os numeros SUBESTIMADOS: 283/76 no lugar de 298/83.

COMO ESTE TESTE REPROVA QUANDO O CONSERTO SOME
----------------------------------------------
`leitura_antiga` e o regex EXATO que vivia em `regras_cor._entradas` (versionado aqui como
SNAPSHOT do defeito). `leitura_nova` e o parser unico (`tools/tabelas.py`). O teste EXIGE
que a antiga NAO veja a chave plantada e que a nova veja — com a saida literal das duas. Se
alguem reintroduzir o regex no lugar do parser compartilhado, a `leitura_nova` volta a ser
cega, as assercoes caem e o teste REPROVA. Um teste que nao falha nao e teste.

Alem da prova sintetica (determinista), o teste cobra o CONSERTO em TODOS os consumidores do
parser: os OITO saem de `tools/tabelas.py` e cada um tem de concordar com ele sobre o fonte
REAL, no SEU contrato. Sao eles (o mesmo rol do docstring do `tabelas.py`):

    1. tools/check_chave_compartilhada.py::bloco/entradas   (cru)
    2. tools/check_dupes.py::chaves_do_bloco                (cru; importa o 1)
    3. tools/check_notas_redundantes.py::bloco/entradas     (cru)
    4. tools/check_fix_keys.py::blocos                      (decodificado)
    5. tools/check_omissao.py::chaves_do_mod                (decodificado, as DUAS tabelas)
    6. tools/check_scaling.py::chaves_do_mod                (decodificado, as DUAS tabelas)
    7. tools/review_ledger.py::le_tabela                    (decodificado)
    8. tools/testes/regras_cor.py::_entradas                (decodificado)

A PROVA DE QUE A CONFERENCIA PEGA UMA REVERSAO. O leitor ANTIGO do `check_omissao`/
`check_scaling` nao lia os blocos: varria o arquivo INTEIRO e colhia chaves de OUTROS
inicializadores (o PARSER-1R mediu 302 no lugar de 298 — 4 fantasmas, DUAS casando com o
censo, ou seja 2 "ja cobertas" FALSAS). Por isso a reversao de qualquer dos dois muda
`chaves_do_mod()` e o `arc.igual` contra o parser unico cai. O teste mede e imprime essa
divergencia (`antigo_arquivo != unificado`); ela e o que da dente a conferencia.
"""
import os
import re
import sys

import arcabouco as arc

sys.path.insert(0, os.path.join(arc.raiz_do_repo(), "tools"))
import tabelas as tab          # noqa: E402  o parser UNICO (o conserto do PARSER-1)
import regras_cor as reg       # noqa: E402  regras da familia de COR (material dos testes)
import check_notas_redundantes as cnr   # noqa: E402  copia do FIX-4, migrada
import check_chave_compartilhada as ccc  # noqa: E402  o "parser unico" historico, migrado
import check_fix_keys as cfk   # noqa: E402  chave x censo, migrado
import check_dupes as cdup     # noqa: E402  duplicadas (importa o ccc), migrado
import check_omissao as com    # noqa: E402  o que o mod cobre, migrado
import check_scaling as csc    # noqa: E402  idem para a escala, migrado
import review_ledger as rl     # noqa: E402  livro ANTES-E-DEPOIS, migrado

META = {
    "nome": "parser-comentario-na-chave",
    "categoria": "pura",
    "requer": [],
    "descricao": "PARSER-1: o parser VE a chave com comentario de LINHA e de BLOCO entre a "
                 "abertura e a chave (o regex antigo nao via) e os OITO consumidores usam "
                 "tabelas.py",
}

# O regex EXATO que vivia em `regras_cor._entradas` (o leitor cego). E o DEFEITO, decorado
# aqui de proposito: sem o snapshot, a prova nao teria contra o que comparar.
REGEX_ANTIGO = re.compile(r'\{\s*"((?:[^"\\]|\\.)*)"\s*,\s*"((?:[^"\\]|\\.)*)"\s*\}')

# O leitor ANTIGO do `check_omissao.py`/`check_scaling.py`: pulava so o comentario de LINHA
# logo apos o `{` e varria o arquivo INTEIRO (nao os blocos), colhendo chave de qualquer
# inicializador. E o outro snapshot do defeito que este teste prende (o do -4).
REGEX_ANTIGO_ARQUIVO = re.compile(r'\{\s*(?://[^\n]*\n\s*)*"((?:[^"\\]|\\.)*)"\s*,')

BS = chr(92)


def desescapa(s):
    """O desescape do projeto (o mesmo do `check_fix_keys.py`/`check_omissao.py`)."""
    return s.replace(BS + '"', '"').replace(BS + 'n', "\n").replace(BS + BS, BS)


def leitura_antiga(bloco):
    """As chaves que o regex antigo via num bloco — a leitura CEGA ao comentario."""
    return [m.group(1) for m in REGEX_ANTIGO.finditer(bloco)]


# A tabela FALSA com os dois formatos de comentario entre a abertura e a chave. A `*0` e o
# `[0]` de proposito: sao os marcadores do MOTOR de valor (o alvo do alcance do COR-3).
FONTE_FALSA = (
    "private static Dictionary<string, string> TextFixes = new Dictionary<string, string>\n"
    "{\n"
    "    { \"sem comentario *0\", \"valor A\" },\n"
    "    {\n"
    "        // comentario de LINHA antes da chave (o furo do COR-3)\n"
    "        \"com linha *0\",\n"
    "        \"valor B\"\n"
    "    },\n"
    "    {\n"
    "        /* comentario de BLOCO antes da chave (o furo do FIX-4) */\n"
    "        \"com bloco [0]\",\n"
    "        \"valor C\"\n"
    "    },\n"
    "};\n")

PLANTADAS = ["com linha *0", "com bloco [0]"]
ESPERADAS_PELA_NOVA = ["sem comentario *0"] + PLANTADAS


def corpo():
    fonte = arc.raiz_do_repo()

    # ---------------------------------------------------------------- 1. PROVA SINTETICA
    bloco, _k = tab.bloco(FONTE_FALSA, "TextFixes")
    antigas = leitura_antiga(bloco)
    novas = [c for _l, _com, c, _v in tab.entradas(bloco, 1)]

    print("leitura ANTIGA (regex de regras_cor._entradas): %r" % antigas)
    print("leitura NOVA   (tools/tabelas.py, parser unico) : %r" % novas)

    # A ISCA: a leitura antiga NAO ve as duas entradas plantadas — e e por isso que os
    # numeros do COR-3 subestimavam. Se isto deixar de valer, o teste cai (o defeito sumiu
    # do snapshot ou o regex mudou de comportamento — os dois merecem atencao).
    for alvo in PLANTADAS:
        arc.exigir(alvo not in antigas,
                   "a leitura ANTIGA passou a ver %r — o snapshot do defeito perdeu o sentido" % alvo)
    arc.exigir(not novas or all(alvo in novas for alvo in PLANTADAS),
               "a leitura NOVA NAO viu %s (viu %r): o parser unico esta cego ao comentario"
               % (PLANTADAS, novas))
    arc.igual(sorted(novas), sorted(ESPERADAS_PELA_NOVA),
              "a leitura NOVA tem de ver as 3 entradas (com e sem comentario)")
    arc.exigir(len(antigas) < len(novas),
               "a leitura ANTIGA (%d) tem de ver MENOS que a NOVA (%d) — e o ponto cego do "
               "COR-3 (entradas com comentario invisiveis)" % (len(antigas), len(novas)))

    # ---------------------------------------------------------------- 2. FONTE REAL
    # Cada consumidor do parser tem de concordar com `tabelas.py`: e a prova de que a
    # implementacao e UMA so, e nao copias remendadas.
    with open(os.path.join(fonte, "BetterTooltips", "Patches", "LocalizePatch.cs"),
              encoding="utf-8") as fh:
        real = fh.read()
    nl = tab.NL

    total_antigo = total_unico = 0
    for nome in tab.NOMES:
        bloco_r, k_r = tab.bloco(real, nome)
        base = real[:k_r].count(nl) + 1
        novas_r = {c for _l, _com, c, _v in tab.entradas(bloco_r, base)}          # cru
        novas_dec = {tab.valor_de_tabela(c) for c in novas_r}                     # decodificado
        antigas_r = set(leitura_antiga(bloco_r))
        total_antigo += len(antigas_r)
        total_unico += len(novas_r)

        # (a) o regex antigo nao pode achar chave que o parser unico nao ache (senao o
        #     parser unico perde entradas)...
        orfas = antigas_r - novas_r
        arc.exigir(not orfas,
                   "no fonte REAL, o regex antigo achou chave que o parser unico NAO ve em "
                   "%s: %r" % (nome, sorted(orfas)[:3]))
        # (b) ...e o regex antigo TEM de perder entradas no total (as com comentario): se as
        #     duas leituras empatarem, o ponto cego do COR-3 nao esta sendo exercitado.
        print("fonte real %-12s antigo=%d  unico=%d  (perdidas pelo antigo: %d)"
              % (nome, len(antigas_r), len(novas_r), len(novas_r) - len(antigas_r)))

        # (c) OS OITO consumidores concordam com o parser unico, cada um no SEU contrato
        #     (regras_cor/check_fix_keys/check_dupes/review_ledger decodificam a chave; os
        #     outros entregam o texto cru; o ledger ainda carrega secao e justificativa).

        # 1) check_chave_compartilhada — o wrapper historico (cru).
        txt_c, k_c = ccc.bloco(real, nome)
        de_comp = {c for _l, _com, c, _v in ccc.entradas(txt_c, real[:k_c].count(nl))}
        arc.igual(de_comp, novas_r, "check_chave_compartilhada.entradas tem de usar o parser unico (%s)" % nome)

        # 2) check_dupes — importa o ccc (cru).
        de_dupes = set(cdup.chaves_do_bloco(real, nome))
        arc.igual(de_dupes, novas_r, "check_dupes.chaves_do_bloco tem de usar o parser unico (%s)" % nome)

        # 3) check_notas_redundantes — a copia do FIX-4 (cru).
        de_notas = {c for _l, _com, c, _v in cnr.entradas(*_bloco_e_base(real, nome))}
        arc.igual(de_notas, novas_r, "check_notas_redundantes.entradas tem de usar o parser unico (%s)" % nome)

        # 4) check_fix_keys — chave x censo (decodificado).
        de_fix = {c for n, c in cfk.blocos(real) if n == nome}
        arc.igual(de_fix, novas_dec, "check_fix_keys.blocos tem de usar o parser unico (%s)" % nome)

        # 7) review_ledger — o livro ANTES-E-DEPOIS (decodificado; secao + justificativa).
        de_livro = {chave for _s, _j, chave, _v in rl.le_tabela(real, nome)}
        arc.igual(de_livro, novas_dec, "review_ledger.le_tabela tem de usar o parser unico (%s)" % nome)

        # 8) regras_cor — o material dos testes de COR (decodificado).
        de_regras = {c for c, _v in reg._entradas(nome)}
        arc.igual(de_regras, novas_dec, "regras_cor._entradas tem de usar o parser unico (%s)" % nome)

    # 5 e 6) check_omissao e check_scaling devolvem o CONJUNTO das DUAS tabelas (o que o mod
    #        ja cobre). Nao tem recorte por tabela: a conferencia e do conjunto inteiro.
    unificado = tab.chaves(real)
    arc.igual(com.chaves_do_mod(), unificado,
              "check_omissao.chaves_do_mod tem de usar o parser unico (as duas tabelas)")
    arc.igual(csc.chaves_do_mod(), unificado,
              "check_scaling.chaves_do_mod tem de usar o parser unico (as duas tabelas)")

    arc.exigir(total_antigo < total_unico,
               "no fonte REAL o regex antigo ve %d chaves e o parser unico %d — o ponto cego "
               "do COR-3 (entradas com comentario invisiveis) deixou de existir? conferir"
               % (total_antigo, total_unico))
    print("fonte real TOTAL  antigo=%d  unico=%d  (perdidas pelo antigo: %d)"
          % (total_antigo, total_unico, total_unico - total_antigo))

    # (d) A REVERSAO SERIA PEGA. O leitor ANTIGO de `check_omissao`/`check_scaling` varria o
    #     arquivo INTEIRO: colhia chave de OUTROS inicializadores (as fantasmas do -4). Se um
    #     dos dois voltasse ao regex, o `chaves_do_mod()` acima deixaria de ser igual ao
    #     `unificado` e a conferencia de (5)/(6) cairia. Aqui a divergencia e MEDIDA, nao narrada.
    antigo_arquivo = {desescapa(m.group(1)) for m in REGEX_ANTIGO_ARQUIVO.finditer(real)}
    fantasmas = sorted(antigo_arquivo - unificado)
    arc.exigir(antigo_arquivo != unificado,
               "o leitor ANTIGO de omissao/escala tinha de DIVERGIR do parser unico — e essa "
               "divergencia que faz a reversao ser pega pela conferencia de (5)/(6); os dois "
               "coincidiram, entao a conferencia nao teria dente")
    arc.exigir(len(antigo_arquivo) > len(unificado),
               "o leitor ANTIGO de omissao/escala (%d) tinha de colher MAIS que o parser unico "
               "(%d) no fonte real — as chaves fantasma de outros inicializadores"
               % (len(antigo_arquivo), len(unificado)))
    print("reversao pega: o leitor ANTIGO de omissao/escala veria %d chaves, o parser unico %d "
          "— %d fantasma(s) de outros inicializadores: %r"
          % (len(antigo_arquivo), len(unificado), len(fantasmas), fantasmas[:6]))

    print("os 8 consumidores (check_chave_compartilhada, check_dupes, check_notas_redundantes, "
          "check_fix_keys, check_omissao, check_scaling, review_ledger, regras_cor) concordam "
          "com o parser unico em %s" % (tab.NOMES,))


def _bloco_e_base(real, nome):
    bloco, k = tab.bloco(real, nome)
    return bloco, real[:k].count(tab.NL) + 1


if __name__ == "__main__":
    arc.main(META, corpo)
