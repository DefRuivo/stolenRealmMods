#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FORMATO-5 - a prova NOS DOIS SENTIDOS da migracao do call site do PULADO PELO ESCAPE.

    python tools/testes/formato5-prova-regras-bf-343.py

O QUE ESTE SCRIPT PROVA
-----------------------
A checagem que a FORMATO-4 achou viva no `regras_bf.py` media DISTANCIA em caracteres entre o
marcador `"PULADO (escape` e o argumento `TipoLinhaDiag.Escape`:

    janela = sweep2[i_escape:i_escape + 900]

A migracao (FORMATO-5) troca a janela pelo recorte ESTRUTURAL do `recorte.py`
(`rec.bloco_que_contem`), reutilizando o modulo - e a checagem tem de:

  [1] INOFENSIVA - um retoque que NAO muda comportamento no `FontSweep` (um comentario de 1077
      chars entre o marcador e o argumento) NAO pode reprovar. A janela de 900 reprovava (o
      argumento sai da janela); o recorte estrutural nao (nao ha margem, ha casamento de chaves);
  [2] DEFEITO REAL - o argumento trocado (`TipoLinhaDiag.Efeito`) ou removido (`null`) continua
      sendo PEGO.

O `JANELA_ANTIGA` abaixo existe SO AQUI, como CONTROLE NEGATIVO da direcao [1] - ele nao esta em
nenhum caminho de checagem (a FORMATO-4 ja registrou essa familia em `FORMATO-4-varredura.md` §2).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc          # noqa: E402  (depende do sys.path acima)
import recorte as rec            # noqa: E402
import regras_bf                 # noqa: E402

# CONTROLE NEGATIVO: a janela que a FORMATO-4 mandou migrar. Nunca em caminho de checagem.
JANELA_ANTIGA = 900
TAMANHO_DO_RETOQUE = 1077        # medido pela FORMATO-4: o retoque que estoura a janela

MARCADOR = '"PULADO (escape'
ARGUMENTO = "TipoLinhaDiag.Escape"
# A linha que fica ENTRE o marcador e o argumento - e onde o retoque inofensivo entra.
ANCORA_DO_RETOQUE = '"n/a (texto pulado: fonte e material nao foram tocados)",'
# O argumento inteiro, para a variante "removido".
ANCORA_DO_ARGUMENTO = '"n/a (texto pulado: nada foi transportado)", null, TipoLinhaDiag.Escape);'

secoes = []


def secao(titulo):
    secoes.append(titulo)
    print("\n" + titulo)


def recorte_do_call_site(src):
    """(sweep, i_escape, bloco_estrutural, cabe_na_janela_antiga) do fonte dado."""
    sweep = regras_bf.corpo(src, regras_bf.SWEEP)
    arc.exigir(sweep, "nao achei o FontSweep no fonte")
    i = sweep.find(MARCADOR)
    arc.exigir(i >= 0, "nao achei o marcador %r no FontSweep" % MARCADOR)
    bloco = rec.bloco_que_contem(sweep, i)
    return sweep, i, bloco, ARGUMENTO in sweep[i:i + JANELA_ANTIGA]


def com_retoque_inofensivo(src, tamanho=TAMANHO_DO_RETOQUE):
    """Insere um COMENTARIO de `tamanho` chars ENTRE o marcador e o argumento.

    Um comentario nao muda comportamento (o `regras_bf.sem_comentarios` / `rec.codigo_efetivo`
    ja provam isso no projeto) - e e o retoque INOFENSIVO que a janela de caracteres nao aguenta.
    """
    i = src.find(ANCORA_DO_RETOQUE)
    arc.exigir(i >= 0, "nao achei a ancora do retoque no fonte")
    k = src.find("\n", i) + 1
    arc.exigir(k > 0, "nao achei o fim da linha da ancora do retoque")
    prefixo = "                                    // retoque inofensivo FORMATO-5 "
    linha = prefixo + ("p" * (tamanho - len(prefixo) - 1)) + "\n"
    arc.exigir(len(linha) == tamanho,
               "o retoque nao tem os %d chars pedidos (tem %d)" % (tamanho, len(linha)))
    arc.exigir("\n" in linha and "//" in linha, "o retoque nao e uma linha de comentario")
    return src[:k] + linha + src[k:]


def com_o_argumento_removido(src):
    """O segundo defeito REAL: o argumento do tipo some do call site (`null` no lugar)."""
    arc.exigir(ANCORA_DO_ARGUMENTO in src, "nao achei o call site do escape no fonte")
    return src.replace(ANCORA_DO_ARGUMENTO,
                       '"n/a (texto pulado: nada foi transportado)", null, null);', 1)


def main():
    fonte_vivo = regras_bf.fonte()

    # ------------------------------------------------------------------ [0] o vivo
    secao("[0] O FONTE VIVO (o alvo da migracao)")
    sweep, i, bloco, cabe = recorte_do_call_site(fonte_vivo)
    print("    FontSweep = %d chars | call site em i=%d" % (len(sweep), i))
    print("    recorte estrutural = %d chars | contem %s? %s" % (len(bloco), ARGUMENTO, ARGUMENTO in bloco))
    print("    a janela ANTIGA de %d chars caberia? %s" % (JANELA_ANTIGA, cabe))
    arc.exigir(ARGUMENTO in bloco, "o recorte estrutural do fonte vivo nao traz o argumento")
    print("    falhas_da_fonte(fonte vivo) = %r" % (regras_bf.falhas_da_fonte(fonte_vivo),))

    # ------------------------------------------------- [1] retoque INOFENSIVO
    secao("[1] RETOQUE INOFENSIVO (%d chars entre o marcador e o argumento)" % TAMANHO_DO_RETOQUE)
    retocado = com_retoque_inofensivo(fonte_vivo)
    arc.exigir(len(retocado) == len(fonte_vivo) + TAMANHO_DO_RETOQUE,
               "o retoque nao entrou (delta de %d chars)" % (len(retocado) - len(fonte_vivo)))
    sweep_r, i_r, bloco_r, cabe_r = recorte_do_call_site(retocado)
    print("      a JANELA ANTIGA de %d acha %s?      %s   <- se False, a janela QUEBRA por "
          "edicao inofensiva" % (JANELA_ANTIGA, ARGUMENTO, cabe_r))
    print("      o RECORTE ESTRUTURAL acha?        %s   <- o recorte NAO quebra"
          % (ARGUMENTO in bloco_r))
    arc.exigir(not cabe_r, "a janela antiga NAO quebrou - o retoque nao serve de prova")
    arc.exigir(ARGUMENTO in bloco_r, "o retoque INOFENSIVO quebrou o recorte estrutural")

    falhas_retocado = regras_bf.falhas_da_fonte(retocado)
    print("      falhas_da_fonte(fonte retocado) = %r" % (falhas_retocado,))
    arc.exigir(not falhas_retocado,
               "o retoque INOFENSIVO reprovou a checagem (era o defeito da janela): %r"
               % (falhas_retocado,))
    print("      OK: o retoque inofensivo NAO reprova e ESTOURA a janela de %d" % JANELA_ANTIGA)

    # ----------------------------------------------------- [2] os defeitos REAIS
    secao("[2] OS DEFEITOS REAIS continuam sendo pegos")
    plantados = (
        ("o argumento trocado (TipoLinhaDiag.Efeito)",
         regras_bf.fonte_com_o_escape_como_efeito(fonte_vivo)),
        ("o argumento REMOVIDO (null)", com_o_argumento_removido(fonte_vivo)),
    )
    for rotulo, defeituoso in plantados:
        arc.exigir(defeituoso != fonte_vivo, "o defeito %r nao foi plantado" % rotulo)
        sweep_d, i_d, bloco_d, _ = recorte_do_call_site(defeituoso)
        pego_pelo_recorte = ARGUMENTO not in bloco_d
        falhas = regras_bf.falhas_da_fonte(defeituoso)
        print("    [%s]" % rotulo)
        print("        o recorte estrutural PEGA (bloco sem %s)?  %s" % (ARGUMENTO, pego_pelo_recorte))
        print("        falhas_da_fonte = %d" % len(falhas))
        for f in falhas:
            print("            - %s" % f)
        arc.exigir(pego_pelo_recorte, "o recorte estrutural NAO pegou o defeito %r" % rotulo)
        arc.exigir(falhas, "falhas_da_fonte NAO pegou o defeito %r" % rotulo)
    print("    OK: os dois defeitos reais continuam sendo pegos")

    # ------------------------------------------------------------------- veredito
    print("\n" + "=" * 78)
    print(" FORMATO-5: %d de %d secoes provadas -> OK" % (len(secoes), len(secoes)))
    print("   (o call site e recortado por CASAMENTO DE CHAVES, nunca por janela de caracteres)")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except arc.Falhou as erro:
        print("\n[FALHOU] %s" % erro)
        sys.exit(1)
