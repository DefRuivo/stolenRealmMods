#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FORMATO-8 - a prova NOS DOIS SENTIDOS dos casadores de chave locais, na mao.

    python tools/testes/formato8-prova-casadores.py

O QUE ESTE SCRIPT PROVA
-----------------------
`regras_bf.corpo` e `regras_bct.corpo`/`_bloco_de` recortavam o corpo de um metodo recontando
`{`/`}` na mao. O casador LOCAL tinha dois defeitos, e a migracao (FORMATO-8) faz os dois
delegarem ao `recorte.py` (literal-aware e FALHA ALTO). A prova tem de mostrar, no MESMO lugar:

  [1] LITERAL - um `}` DENTRO de um literal de string fechava o bloco CEDO (corpo TRUNCADO). O
      casador ANTIGO (recontado aqui, em memoria, como CONTROLE NEGATIVO) faz isso; o delegado
      devolve o corpo inteiro;
  [2] SEM FECHAMENTO - um metodo com as chaves que NAO FECHAM virava `None` em SILENCIO (o
      casador antigo); o delegado FALHA ALTO (`arc.Falhou`);
  [3] O FONTE VIVO - o recorte dos dois modulos, em TODAS as declaracoes que eles leem, e BYTE A
      BYTE o do `recorte.py` (`rec.bloco_apos`/`rec.bloco_balanceado`): o veredito NAO mudou.

NADA AQUI TOCA ARQUIVO NENHUM: o casador antigo e recontado em memoria e as fontes sao lidas como
elas estao. (A rodada FISICA - o casador antigo plantado de volta nos arquivos, o teste
reprovando, o arquivo restaurado byte a byte - esta registrada em
`tools/testes/formato8-prova-casadores.log`.)
"""
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc          # noqa: E402  (depende do sys.path acima)
import recorte as rec            # noqa: E402
import regras_bf                 # noqa: E402
import regras_bct                # noqa: E402

DECL = "private static void Alvo("

COM_LITERAL = (
    "class C\n{\n    private static void Alvo()\n    {\n"
    '        string s = "}";\n'
    "        int depois = 1;\n"
    "        Alvo2();\n    }\n}\n"
)
SEM_FECHAR = (
    "class C\n{\n    private static void Alvo()\n    {\n"
    "        int x = 1;\n"
)

secoes = []


def secao(titulo):
    secoes.append(titulo)
    print("\n" + titulo)


def _corpo_ingenuo(src, declaracao):
    """O casador ANTIGO, recontado SO como CONTROLE NEGATIVO (nunca em caminho de checagem)."""
    i = src.find(declaracao)
    if i < 0:
        return None
    j = src.find("{", i)
    if j < 0:
        return None
    nivel, k = 0, j
    while k < len(src):
        if src[k] == "{":
            nivel += 1
        elif src[k] == "}":
            nivel -= 1
            if nivel == 0:
                return src[j:k + 1]
        k += 1
    return None


def _nunca_silencio(acao, rotulo):
    try:
        valor = acao()
    except arc.Falhou as erro:
        print("      %s: FALHOU ALTO -> %s" % (rotulo, erro))
        return
    raise arc.Falhou("%s: esperava arc.Falhou e veio %r (o SILENCIO do casador local)"
                     % (rotulo, valor))


def main():
    # ----------------------------------------------------------------------- [1] LITERAL
    secao("[1] LITERAL - chave DENTRO de um literal de string nao pode quebrar o recorte")
    antigo = _corpo_ingenuo(COM_LITERAL, DECL)
    print("    o CASADOR ANTIGO devolveu: %r" % (antigo,))
    print("      contem 'depois' e 'Alvo2' (o que vem DEPOIS do literal)? %s"
          % ("depois" in (antigo or "") and "Alvo2" in (antigo or "")))
    arc.exigir("depois" not in (antigo or ""),
               "o controle negativo perdeu o sentido: o casador antigo nao truncou no literal")
    for nome, mod in (("regras_bf", regras_bf), ("regras_bct", regras_bct)):
        corpo = mod.corpo(COM_LITERAL, DECL) or ""
        print("    %-11s (delegado) devolveu %d chars, contem 'depois'/'Alvo2'? %s"
              % (nome, len(corpo), "depois" in corpo and "Alvo2" in corpo))
        arc.exigir(corpo.rstrip().endswith("}") and "depois" in corpo and "Alvo2" in corpo,
                   "%s: o `}` do literal fechou o bloco cedo" % nome)
    j = COM_LITERAL.index("{", COM_LITERAL.index(DECL))
    arc.igual(regras_bct._bloco_de(COM_LITERAL, j), rec.bloco_balanceado(COM_LITERAL, j),
              "_bloco_de nao e o rec.bloco_balanceado")

    # ------------------------------------------------------------------ [2] SEM FECHAMENTO
    secao("[2] SEM FECHAMENTO - metodo com chaves que nao fecham tem de FALHAR ALTO")
    print("    o CASADOR ANTIGO devolveu: %r  <- SILENCIO (indistinguivel de 'nao achei')"
          % (_corpo_ingenuo(SEM_FECHAR, DECL),))
    arc.exigir(_corpo_ingenuo(SEM_FECHAR, DECL) is None,
               "o controle negativo perdeu o sentido: o casador antigo nao devolveu None")
    for nome, mod in (("regras_bf", regras_bf), ("regras_bct", regras_bct)):
        _nunca_silencio(lambda m=mod: m.corpo(SEM_FECHAR, DECL), "%s.corpo" % nome)
    j = SEM_FECHAR.index("{", SEM_FECHAR.index(DECL))
    _nunca_silencio(lambda: regras_bct._bloco_de(SEM_FECHAR, j), "regras_bct._bloco_de")
    for nome, mod in (("regras_bf", regras_bf), ("regras_bct", regras_bct)):
        arc.exigir(mod.corpo(SEM_FECHAR, "private static void NaoExiste(") is None,
                   "%s: a declaracao AUSENTE deixou de ser None" % nome)

    # ------------------------------------------------------------------------ [3] O VIVO
    secao("[3] O FONTE VIVO - o recorte delegado e BYTE A BYTE o do recorte.py (veredito igual)")
    casos = []
    src_bf = regras_bf.fonte()
    for decl in (regras_bf.ET, regras_bf.TEM_EFEITO, regras_bf.TEXTURA, regras_bf.COPIAR,
                 regras_bf.REVERTER, regras_bf.DIAG, regras_bf.SWEEP, regras_bf.ORCAMENTO):
        casos.append(("regras_bf", regras_bf.corpo, src_bf, decl))
    for nome in (regras_bct.STYLER, regras_bct.PLUGIN):
        src = regras_bct.fonte(nome)
        decls = ((regras_bct.APLICAR_TMP, "private static void AplicarTamanho(",
                  regras_bct.APLICAR_LEGADO) if nome == regras_bct.STYLER
                 else (regras_bct.APLICAR_PATCHES, regras_bct.EH_CLASSE))
        for decl in decls:
            casos.append(("regras_bct:%s" % nome, regras_bct.corpo, src, decl))
    for rotulo, funcao, src, decl in casos:
        i = src.find(decl)
        arc.exigir(i >= 0, "a declaracao %r nao esta em %s" % (decl, rotulo))
        obtido = funcao(src, decl)
        esperado = rec.bloco_apos(src, i)
        mesmo = (obtido == esperado)
        print("    %-26s %-42s %d chars | byte a byte igual? %s"
              % (rotulo, decl, len(esperado), mesmo))
        arc.exigir(mesmo, "[%s] corpo(%r) NAO e o recorte do recorte.py" % (rotulo, decl))
    src_st = regras_bct.fonte(regras_bct.STYLER)
    j = src_st.find("{", src_st.find(regras_bct.APLICAR_TMP))
    arc.igual(regras_bct._bloco_de(src_st, j), rec.bloco_balanceado(src_st, j),
              "_bloco_de do regras_bct nao delega")
    print("    (o hash do `corpo` do BetterFont/FontSweep: %s)"
          % hashlib.sha256((regras_bf.corpo(src_bf, regras_bf.SWEEP) or "").encode("utf-8")
                           ).hexdigest()[:16])

    print("\n" + "=" * 78)
    print(" FORMATO-8: %d de %d secoes provadas -> OK" % (len(secoes), len(secoes)))
    print("   (chave em literal de string nao quebra; metodo sem fechamento FALHA ALTO; o")
    print("    recorte do fonte vivo e byte a byte o do recorte.py - veredito inalterado)")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except arc.Falhou as erro:
        print("\n[FALHOU] %s" % erro)
        sys.exit(1)
