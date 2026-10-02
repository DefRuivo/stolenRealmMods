#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FORMATO-7 — a FAIXA de indices do recorte estrutural: o primitivo que a FORMATO-6 remendou a mao.

POR QUE ESTE TESTE EXISTE
-------------------------
A FORMATO-6 precisou do FIM do bloco estrutural e o `recorte.py` so devolvia o bloco como TEXTO;
ela reconstruiu o fim com `codigo.index(bloco, pos) + len(bloco)` — a VOLTA ao texto. Essa volta
tem um furo real: se o TEXTO do bloco aparecer ANTES, dentro de um literal de string entre a
ancora e o bloco de verdade, o `index` casa a COPIA e o fim sai no lugar ERRADO (o trecho corta
antes do bloco). A FORMATO-7 acrescenta a FAIXA `(inicio, fim)` INCLUSIVOS
(`faixa_bloco_apos` / `faixa_bloco_balanceado`, fatiada por `texto_da_faixa`) — ADITIVO: o texto
`bloco_*` continua existindo, como o MESMO calculo da faixa.

O QUE ESTE TESTE PROVA (nos dois sentidos)
------------------------------------------
  1. EQUIVALENCIA: `texto_da_faixa(codigo, faixa_*)` == `bloco_*` == a fatia, no sintetico e no
     fonte REAL — usar a faixa e usar o texto dao o MESMO recorte.
  2. O FURO QUE A FAIXA FECHA: com uma COPIA do bloco dentro de um literal ANTES do bloco, a
     reconstrucao por texto devolve o trecho ERRADO e a faixa devolve o CERTO.
  3. CONSUMIDOR REAL: a regra 2 do `check_patches` por TEXTO (`cp.trecho_do_patch`, a rota da
     FORMATO-6) e a versao por FAIXA dao o MESMO trecho — sintetico, fonte REAL e fonte REAL
     retocada.
  4. DIRECAO 1 — EDICAO INOFENSIVA: um retoque inofensivo dentro do bloco nao quebra NENHUMA das
     duas formas nem muda a igualdade entre elas.
  5. FALHA ALTA: chaves que nao fecham -> as DUAS formas levantam `arc.Falhou` (a faixa nao
     devolve um `(inicio, fim)` de mentira, e o consumidor reprova).
"""
import importlib.util
import os
import re

import arcabouco as arc
import recorte as rec

META = {
    "nome": "formato7-faixa-recorte",
    "categoria": "pura",
    "requer": [],
    "descricao": "FORMATO-7: o recorte estrutural devolve a FAIXA (inicio, fim) alem do texto — "
                 "as duas formas dao o mesmo recorte, a faixa fecha o furo da reconstrucao por "
                 "texto e um retoque inofensivo nao quebra nenhuma das duas",
}

RAIZ = arc.raiz_do_repo()
CAMINHO_CP = os.path.join(RAIZ, "tools", "check_patches.py")
FONTE_REAL = os.path.join(RAIZ, "BetterTooltips", "Patches", "ShrineAuraPatch.cs")
PADRAO_TIPO = r"\b(typeof|nameof)\s*\("


# ------------------------------------------------------------------ 1. sintetico ---

SINTETICO = (
    "[HarmonyPatch]\n"
    "class Patch\n"
    "{\n"
    "    private static readonly System.Type[] Assinatura =\n"
    "        new[] { typeof(AlvoDoPatch), typeof(int) };\n"
    "}\n"
)

# O bloco procurado e a COPIA do MESMO texto que aparece um pouco antes, DENTRO de um literal
# de string (entre a ancora e o bloco de verdade). E o caso que o remendo `index(bloco, pos) +
# len(bloco)` erra: ele acha a copia primeiro.
BLOCO = "{ a(); }"
COM_COPIA = 'if (x) log("%s"); %s fim\n' % (BLOCO, BLOCO)

QUEBRADO = (
    "[HarmonyPatch]\n"
    "class P\n"
    "{\n"
    "    private static void X()\n"
    "    {\n"
    "        return;\n"          # chaves NAO fecham de proposito
)


def _trecho_por_texto(codigo, pos):
    """A reconstrucao da FORMATO-6: pega o TEXTO do bloco e procura de volta a posicao dele."""
    bloco = rec.bloco_apos(codigo, pos)
    fim = codigo.index(bloco, pos) + len(bloco)
    return codigo[pos:fim]


def _trecho_por_faixa(codigo, pos):
    """A rota da FORMATO-7: a FAIXA da o fim pela estrutura, sem procurar o texto de volta."""
    ini, fim = rec.faixa_bloco_apos(codigo, pos)
    return codigo[pos:fim + 1]


def _equivalencia():
    # (a) texto == faixa == fatia, no sintetico.
    for rotulo, codigo, pos in (
        ("sintetico bloco_apos", SINTETICO, SINTETICO.find("[HarmonyPatch]")),
        ("sintetico bloco_balanceado", SINTETICO, SINTETICO.find("{")),
    ):
        if "apos" in rotulo:
            faixa = rec.faixa_bloco_apos(codigo, pos)
            texto = rec.bloco_apos(codigo, pos)
        else:
            faixa = rec.faixa_bloco_balanceado(codigo, pos)
            texto = rec.bloco_balanceado(codigo, pos)
        arc.exigir(rec.texto_da_faixa(codigo, faixa) == texto,
                   "%s: `texto_da_faixa(faixa)` != `bloco` (%r != %r)" % (rotulo, faixa, texto))
        arc.exigir(codigo[faixa[0]] == "{" and codigo[faixa[1]] == "}",
                   "%s: a faixa %r nao comeca no `{` e termina no `}` que casa" % (rotulo, faixa))
        arc.exigir(faixa[1] >= faixa[0], "%s: faixa invertida %r" % (rotulo, faixa))

    # (b) O FURO: a copia do bloco dentro do literal derruba a rota por TEXTO e nao a por FAIXA.
    pos = COM_COPIA.find("if (x)")
    faixa = rec.faixa_bloco_apos(COM_COPIA, pos)
    bloco = rec.bloco_apos(COM_COPIA, pos)
    arc.exigir(bloco == BLOCO, "o recorte estrutural do bloco mudou: %r" % bloco)
    ini_texto = COM_COPIA.index(bloco, pos)
    arc.exigir(ini_texto != faixa[0],
               "a prova perdeu o sentido: o `index` por texto ja casou o bloco CERTO (nao ha copia)")
    arc.exigir(COM_COPIA[ini_texto:ini_texto + len(bloco)] == COM_COPIA[faixa[0]:faixa[1] + 1],
               "a copia nao tem o mesmo texto do bloco — o caso nao reproduz o furo")
    arc.exigir(rec.texto_da_faixa(COM_COPIA, faixa) == BLOCO and
               COM_COPIA[:faixa[0]].rstrip().endswith('");'),
               "a FAIXA casou a copia em vez do bloco de verdade: %r" % (faixa,))
    trecho_texto = _trecho_por_texto(COM_COPIA, pos)
    trecho_faixa = _trecho_por_faixa(COM_COPIA, pos)
    arc.exigir(trecho_texto != trecho_faixa,
               "a prova perdeu o sentido: o `index(bloco, pos)` por TEXTO casou o bloco CERTO "
               "(a copia no literal nao enganou nada) e as duas rotas dao o mesmo trecho")
    arc.exigir(len(trecho_texto) == ini_texto + len(bloco),
               "a rota por TEXTO nao parou na copia (fim em %d, o esperado era %d)"
               % (len(trecho_texto), ini_texto + len(bloco)))
    arc.exigir(faixa[0] >= len(trecho_texto) and faixa[1] >= len(trecho_texto),
               "a rota por FAIXA nao alcancou o bloco de verdade (que comeca depois de onde a "
               "rota por TEXTO parou): faixa %r vs trecho por texto %r" % (faixa, trecho_texto))

    # (c) FALHA ALTA: as DUAS formas levantam `arc.Falhou` com chaves que nao fecham.
    for rotulo, acao in (
        ("bloco_apos", lambda: rec.bloco_apos(QUEBRADO, 0)),
        ("faixa_bloco_apos", lambda: rec.faixa_bloco_apos(QUEBRADO, 0)),
        ("faixa_bloco_balanceado", lambda: rec.faixa_bloco_balanceado(
            QUEBRADO, QUEBRADO.find("{"))),
    ):
        try:
            acao()
        except arc.Falhou:
            pass
        else:
            arc.exigir(False, "`%s` NAO falhou alto nas chaves que nao fecham — devolveu um "
                              "recorte/faixa em silencio" % rotulo)


# ------------------------------------------------------- 2. consumidor real + fonte REAL ---

def _modulo_do_check():
    """Carrega o `check_patches.py` por caminho (a mesma rota do `t_formato6`)."""
    spec = importlib.util.spec_from_file_location("check_patches_f7", CAMINHO_CP)
    cp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cp)
    rec_, arcmod = cp.carregar_recorte()
    return cp, rec_, arcmod


def _retoque(tamanho):
    """Codigo C# inofensivo com pelo menos `tamanho` chars: sem chave, sem literal, sem typeof."""
    linhas, n = [], 0
    while n < tamanho:
        linhas.append("\n    private static int _rastro%d = 0;" % len(linhas))
        n += len(linhas[-1])
    return "".join(linhas)


def _atributo_bare(codigo):
    """(m, fim_attr) do primeiro `[HarmonyPatch]` SEM `typeof/nameof` (o de classe)."""
    for m in re.finditer(r"\[HarmonyPatch\b", codigo):
        fim = codigo.find("]", m.start())
        if not re.search(PADRAO_TIPO, codigo[m.start():fim + 1]):
            return m, fim
    return None, None


def _consumidores(cp, rec_, arcmod, rotulo, codigo, pos):
    """Os DOIS consumidores (texto e faixa) e as tres condicoes que valem para os dois."""
    trecho_texto = cp.trecho_do_patch(codigo, pos, rec_, arcmod)
    trecho_faixa = _trecho_por_faixa(codigo, pos)
    arc.exigir(trecho_texto == trecho_faixa,
               "%s: o consumidor por TEXTO e o por FAIXA divergem:\n  texto: %r\n  faixa: %r"
               % (rotulo, trecho_texto, trecho_faixa))
    arc.exigir(trecho_texto.startswith("[HarmonyPatch]"),
               "%s: o trecho nao comeca no atributo: %r" % (rotulo, trecho_texto[:30]))
    arc.exigir(trecho_texto.rstrip().endswith("}"),
               "%s: o trecho nao fecha no `}` que casa: %r..." % (rotulo, trecho_texto[-40:]))
    arc.exigir(codigo[rec.faixa_bloco_apos(codigo, pos)[1]] == "}",
               "%s: o fim da faixa nao cai num `}`" % rotulo)
    return trecho_texto


def _fonte_real(cp, rec_, arcmod):
    with open(FONTE_REAL, encoding="utf-8") as fh:
        cru = fh.read()
    codigo, _, _ = cp.separar(cru)
    m, _ = _atributo_bare(codigo)
    arc.exigir(m is not None, "nao achei o `[HarmonyPatch]` bare de classe em %s" % FONTE_REAL)

    base = _consumidores(cp, rec_, arcmod, "fonte real", codigo, m.start())
    arc.exigir(re.search(PADRAO_TIPO, base) is not None,
               "o trecho da fonte real nao tem a assinatura por TIPO")
    arc.exigir(rec.texto_da_faixa(codigo, rec.faixa_bloco_apos(codigo, m.start())) ==
               rec.bloco_apos(codigo, m.start()),
               "fonte real: `texto_da_faixa` != `bloco_apos`")

    # DIRECAO 1 — retoque INOFENSIVO logo depois da abertura da classe: a MESMA edicao que a
    # FORMATO-6 planta. Nenhuma das duas formas pode quebrar, e a igualdade entre elas fica.
    abertura = codigo.find("{", m.start())
    retocado = codigo[:abertura + 1] + _retoque(2200) + codigo[abertura + 1:]
    depois = _consumidores(cp, rec_, arcmod, "fonte real retocada", retocado, m.start())
    arc.exigir(len(depois) > len(base) and re.search(PADRAO_TIPO, depois) is not None,
               "o retoque inofensivo derrubou a assinatura por TIPO de algum dos dois consumidores")
    arc.exigir(retocado.find("[HarmonyPatch]") == m.start(),
               "a ancora do atributo mudou de posicao com o retoque")

    # DIREITO/AVESSO do furo tambem no consumidor REAL: a rota por TEXTO e a por FAIXA concordam
    # porque no fonte REAL nao ha copia do bloco num literal antes dele.
    arc.exigir(_trecho_por_texto(codigo, m.start()) == _trecho_por_faixa(codigo, m.start()),
               "no fonte real as duas rotas ja divergem sem edicao nenhuma")


def corpo():
    _equivalencia()
    cp, rec_, arcmod = _modulo_do_check()
    _fonte_real(cp, rec_, arcmod)
    print("FORMATO-7: a FAIXA (inicio, fim) e o MESMO recorte do TEXTO (`texto_da_faixa(faixa_*) "
          "== bloco_*`), fecha o furo do `index(bloco, pos) + len(bloco)` (a copia do bloco num "
          "literal), o consumidor da regra 2 da o mesmo trecho pelas duas rotas e um retoque "
          "inofensivo nao quebra nenhuma delas")


if __name__ == "__main__":
    arc.main(META, corpo)
