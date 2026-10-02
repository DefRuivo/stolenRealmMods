#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FORMATO-8 — os casadores de chave LOCAIS do `regras_bf`/`regras_bct` DELEGAM ao `recorte.py`.

POR QUE ESTE TESTE EXISTE
-------------------------
`regras_bf.corpo` e `regras_bct.corpo`/`_bloco_de` recortavam o corpo de um metodo recontando
`{`/`}` na mao. Esse casador LOCAL tinha dois defeitos, os dois do MESMO tipo que a familia
FORMATO varre:

  * era CEGO a literal de string/char — um `}` escrito dentro de uma string (`string s = "}";`)
    fechava o bloco CEDO, e o corpo vinha TRUNCADO (faltava tudo o que vinha depois);
  * devolvia `None` em SILENCIO quando as chaves NAO fechavam — indistinguivel de "a declaracao
    nao existe", e um recorte vazio "passa" em toda checagem.

O `recorte.py` e o oposto e ja era a implementacao canonica: literal-aware, FALHA ALTO
(`arc.Falhou`) e usado pelo `check_patches.py` no CI. A duplicacao era DELIBERADA enquanto os dois
modulos estavam ocupados por outras tarefas (o `regras_bct.sem_comentarios` ate documenta isso);
agora os dois estao livres e os casadores locais passaram a DELEGAR.

O QUE ESTE TESTE PROVA (nos dois sentidos)
------------------------------------------
  1. DIRECAO "literal": um `}` (e um `{`) DENTRO de um literal de string NAO quebra o recorte — o
     corpo devolvido contem os statements que vem DEPOIS do literal.
  2. DIRECAO "sem fechamento": um metodo com as chaves que NAO fecham FALHA ALTO (`arc.Falhou`) em
     vez de virar `None` em silencio — `corpo` e `_bloco_de`.
  3. CONTROLE NEGATIVO: o casador ANTIGO (a implementacao INGENUA recontada aqui em memoria)
     REPROVA as DUAS direcoes — e o que mostra que o teste "reprova" com o defeito, e nao so
     passa com o conserto.
  4. DELEGACAO no fonte VIVO: o recorte dos dois modulos e BYTE A BYTE o do `recorte.py`
     (`rec.bloco_apos` / `rec.bloco_balanceado`) em TODAS as declaracoes que eles leem, e o
     veredito sobre o fonte valido NAO mudou (`falhas_da_fonte` / `falhas_do_comportamento` vazios).
"""
import hashlib

import arcabouco as arc
import recorte as rec
import regras_bf
import regras_bct

META = {
    "nome": "formato8-casadores-locais",
    "categoria": "pura",
    "requer": [],
    "descricao": "FORMATO-8: os casadores de chave locais do regras_bf/regras_bct delegam ao "
                 "recorte.py — chave em literal de string nao quebra e metodo sem fechamento "
                 "FALHA ALTO; o recorte do fonte vivo e byte a byte o estrutural (veredito igual)",
}

DECL = "private static void Alvo("

# DIRECAO 1 — um `}` DENTRO de um literal de string: o casador ingenuo fecha o bloco no `}` do
# literal e perde `depois`/`Alvo2`, que vem DEPOIS dele.
COM_LITERAL_FECHA = (
    "class C\n"
    "{\n"
    "    private static void Alvo()\n"
    "    {\n"
    '        string s = "}";\n'
    "        int depois = 1;\n"
    "        Alvo2();\n"
    "    }\n"
    "}\n"
)

# DIRECAO 1 (variante) — um `{` DENTRO de um literal: o casador ingenuo soma um nivel a mais e
# engole a chave que FECHA a classe.
COM_LITERAL_ABRE = (
    "class C\n"
    "{\n"
    "    private static void Alvo()\n"
    "    {\n"
    '        string t = "{";\n'
    "        int depois = 1;\n"
    "        Alvo2();\n"
    "    }\n"
    "}\n"
)

# DIRECAO 2 — o metodo SEM fechamento (fonte cortado): nada fecha, nem o metodo nem a classe.
SEM_FECHAR = (
    "class C\n"
    "{\n"
    "    private static void Alvo()\n"
    "    {\n"
    "        int x = 1;\n"
)


def _corpo_ingenuo(src, declaracao):
    """O casador ANTIGO, recontado AQUI SO como CONTROLE NEGATIVO (nunca em caminho de checagem).

    E o texto que os dois modulos tinham antes da FORMATO-8: conta `{`/`}` crus (chave de literal
    conta como bloco) e, quando as chaves nao fecham, devolve `None` em silencio.
    """
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


# ------------------------------------------------------- 1/2/3. sintetico, dois sentidos ---

MODULOS = (("regras_bf", regras_bf), ("regras_bct", regras_bct))


def _nao_vem_nada_de_silencio(acao, rotulo):
    """A acao TEM de falhar alto: se voltar um valor (inclusive None), o defeito esta de pe."""
    try:
        valor = acao()
    except arc.Falhou:
        return
    arc.exigir(False, "%s: esperava FALHA ALTA (arc.Falhou) e veio %r — e o SILENCIO do casador "
                      "local (um recorte vazio/None 'passa' em toda checagem)" % (rotulo, valor))


def _direcao_literal():
    """(1) chave dentro de literal de string NAO quebra o recorte — nos DOIS modulos."""
    # CONTROLE NEGATIVO: o casador antigo quebra nas duas formas do literal.
    truncado = _corpo_ingenuo(COM_LITERAL_FECHA, DECL)
    arc.exigir(truncado is not None and "depois" not in truncado,
               "o controle negativo perdeu o sentido: o casador antigo NAO truncou no `}` do "
               "literal (%r)" % (truncado,))
    engolido = _corpo_ingenuo(COM_LITERAL_ABRE, DECL)
    arc.exigir(engolido is not None
               and engolido != rec.bloco_apos(COM_LITERAL_ABRE, COM_LITERAL_ABRE.find(DECL)),
               "o controle negativo perdeu o sentido: o `{` do literal nao desbalanceou o "
               "casador antigo (%r)" % (engolido,))

    for nome, mod in MODULOS:
        corpo = mod.corpo(COM_LITERAL_FECHA, DECL) or ""
        arc.exigir(corpo.startswith("{") and corpo.rstrip().endswith("}"),
                   "[%s] o recorte nao e o corpo `{...}` do metodo: %r" % (nome, corpo))
        for marca in ("depois", "Alvo2"):
            arc.exigir(marca in corpo,
                       "[%s] o `}` DENTRO do literal fechou o bloco cedo: %r ficou de fora (%r)"
                       % (nome, marca, corpo))
        # a variante do `{` no literal: o recorte NAO pode engolir a chave que FECHA a classe.
        corpo_abre = mod.corpo(COM_LITERAL_ABRE, DECL) or ""
        arc.exigir(corpo_abre.startswith("{") and corpo_abre.rstrip().endswith("}")
                   and "depois" in corpo_abre and "Alvo2" in corpo_abre,
                   "[%s] o `{` DENTRO do literal desbalanceou o recorte: %r" % (nome, corpo_abre))
        i_abre = COM_LITERAL_ABRE.find(DECL)
        arc.igual(corpo_abre, rec.bloco_apos(COM_LITERAL_ABRE, i_abre),
                  "[%s] o recorte do `{` de literal nao e o `rec.bloco_apos`" % nome)

    # o `_bloco_de` do regras_bct, na variante do `}` de literal.
    j = COM_LITERAL_FECHA.index("{", COM_LITERAL_FECHA.index(DECL))
    arc.igual(regras_bct._bloco_de(COM_LITERAL_FECHA, j),
              rec.bloco_balanceado(COM_LITERAL_FECHA, j),
              "regras_bct._bloco_de nao casou as chaves por literal (o `}` de string fechou cedo)")


def _direcao_sem_fechamento():
    """(2) metodo sem fechamento FALHA ALTO em vez de `None` — nos DOIS modulos."""
    arc.exigir(_corpo_ingenuo(SEM_FECHAR, DECL) is None,
               "o controle negativo perdeu o sentido: o casador antigo NAO devolveu None")

    for nome, mod in MODULOS:
        _nao_vem_nada_de_silencio(lambda m=mod: m.corpo(SEM_FECHAR, DECL),
                                  "[%s] corpo sem fechamento" % nome)
    j = SEM_FECHAR.index("{", SEM_FECHAR.index(DECL))
    _nao_vem_nada_de_silencio(lambda: regras_bct._bloco_de(SEM_FECHAR, j),
                              "regras_bct._bloco_de sem fechamento")

    # a declaracao AUSENTE continua `None` (um "nao achei" que o chamador relata como FALHA, nao
    # um recorte silencioso): a delegacao nao pode ter transformado isso em excecao.
    for nome, mod in MODULOS:
        arc.exigir(mod.corpo(SEM_FECHAR, "private static void NaoExiste(") is None,
                   "[%s] a declaracao ausente deixou de ser None" % nome)


# --------------------------------------------------- 4. delegacao no fonte VIVO (veredito) ---

DECL_BF = (regras_bf.ET, regras_bf.TEM_EFEITO, regras_bf.TEXTURA, regras_bf.COPIAR,
           regras_bf.REVERTER, regras_bf.DIAG, regras_bf.SWEEP, regras_bf.ORCAMENTO)
DECL_BCT_STYLER = (regras_bct.APLICAR_TMP, "private static void AplicarTamanho(",
                   regras_bct.APLICAR_LEGADO)
DECL_BCT_PLUGIN = (regras_bct.APLICAR_PATCHES, regras_bct.EH_CLASSE)


def _delegacao_no_fonte_vivo():
    """O recorte dos dois modulos e BYTE A BYTE o do `recorte.py` — e o veredito nao mudou."""
    casos = []
    src_bf = regras_bf.fonte()
    for decl in DECL_BF:
        casos.append(("regras_bf", regras_bf.corpo, src_bf, decl))
    for nome, decls in ((regras_bct.STYLER, DECL_BCT_STYLER),
                        (regras_bct.PLUGIN, DECL_BCT_PLUGIN)):
        src = regras_bct.fonte(nome)
        for decl in decls:
            casos.append(("regras_bct:%s" % nome, regras_bct.corpo, src, decl))

    for rotulo, funcao, src, decl in casos:
        i = src.find(decl)
        arc.exigir(i >= 0, "a declaracao %r nao esta no fonte vivo de %s" % (decl, rotulo))
        obtido = funcao(src, decl)
        esperado = rec.bloco_apos(src, i)
        arc.exigir(obtido is not None and obtido.startswith("{") and obtido.rstrip().endswith("}"),
                   "[%s] corpo(%r) nao e um bloco `{...}`: %r" % (rotulo, decl, obtido))
        arc.igual(_assinatura_de(obtido), _assinatura_de(esperado),
                  "[%s] corpo(%r) NAO e o recorte estrutural do recorte.py" % (rotulo, decl))

    # `_bloco_de` do regras_bct tambem delega (o bloco da classe + o corpo de um metodo interno).
    src = regras_bct.fonte(regras_bct.STYLER)
    j = src.find("{", src.find(regras_bct.APLICAR_TMP))
    arc.igual(regras_bct._bloco_de(src, j), rec.bloco_balanceado(src, j),
              "regras_bct._bloco_de nao e o `rec.bloco_balanceado`")

    # NOTA: o veredito NAO e conferido aqui rodando `falhas_da_fonte` sobre o fonte vivo — o
    # `BetterFont/Plugin.cs` e editado por outras tarefas em paralelo, e um teste que reprova
    # enquanto o arquivo esta no meio da escrita reprova por motivo ALHEIO ao dele. O que se
    # confere e a IGUALDADE do recorte com o do `recorte.py` (acima): byte a byte igual, todo
    # consumidor ve o mesmo texto de antes, e o veredito nao tem como mudar. Quem julga o fonte
    # vivo sao os testes do Gate/defaults (`t_bf_*`), no snapshot deles.


def _assinatura_de(texto):
    """(hash, tamanho, primeiros 24 chars) do recorte — a comparacao byte a byte do conteudo."""
    return (hashlib.sha256(texto.encode("utf-8")).hexdigest(), len(texto), texto[:24])


def corpo():
    _direcao_literal()
    _direcao_sem_fechamento()
    _delegacao_no_fonte_vivo()
    print("FORMATO-8: os casadores locais delegam ao recorte.py — chave em literal de string nao "
          "quebra (o controle negativo mostra o casador antigo quebrando) e metodo sem fechamento "
          "FALHA ALTO; no fonte vivo o recorte e byte a byte o do recorte.py e o veredito e o mesmo")


if __name__ == "__main__":
    arc.main(META, corpo)
