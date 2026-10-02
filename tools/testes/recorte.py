#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""recorte.py - o recorte ESTRUTURAL de fonte C# nos testes: casamento de chaves, NUNCA uma
janela de caracteres.

POR QUE ESTE MODULO EXISTE (FORMATO-3, achado da FORMATO-2 / NIV3-1R)
---------------------------------------------------------------------
O projeto ja pagou quatro vezes pelo MESMO defeito: um teste recorta um trecho de fonte com
uma JANELA FIXA (`codigo[i:i + N`) e mede TEXTO onde queria medir COMPORTAMENTO. A janela nao
tem margem: ela existe enquanto o metodo couber nela:

  * `t_formato_notas` recortava 3200 caracteres do `Prefix` (o metodo tem 3371): a linha da
    aura a 3041 ficava a 159 da borda — a janela ja nao pegava o metodo INTEIRO (cortava o
    `catch`), e o caminho curto para o verde era AFROUXAR a janela;
  * `t_nivel3_sinergia` recorta o MESMO metodo com 3800: sobram 429, e o NIV3-1 ja consumiu
    ~260;
  * o `FontSweep` do BetterFont e lido com janelas de 900 (`regras_bf`) e 1200
    (`regras_bf_estilo`) coladas a um marcador;
  * as notas fundidas de shrine sao lidas com 160 (`t_trava_cor_notas_fundidas`) e 120
    (`regras_cor`).

Uma edicao INOFENSIVA (um log a mais, um local a mais) empurra o marcador para fora da
janela e o teste REPROVA por motivo ALHEIO ao defeito. Aqui o recorte e o BLOCO delimitado
pelas CHAVES: nao ha margem, porque nao ha distancia. O teste acha o trecho de verdade, do
tamanho que ele tiver.

O QUE "ESTRUTURAL" EXIGE
------------------------
  * chave dentro de literal de STRING ou de CHAR nao conta (`{`/`}` num texto nao abre bloco);
  * comentario de LINHA (`//`) e de BLOCO (`/* */`) nao conta (o `{STA=}` de um comentario nao
    e codigo) — so onde o chamador pede (`codigo_efetivo`);
  * SEM a assinatura, SEM a abertura ou com chaves que NAO FECHAM -> FALHA ALTO (`arc.Falhou`),
    nunca um pedaco devolvido em silencio (um recorte vazio "passa" em toda checagem);
  * o recorte de metodo termina em `}` e contem o fim do metodo — o guarda que impede a volta
    da janela. Use `exigir_metodo_inteiro` no ponto de chamada.
  * o recorte sai em DUAS formas do MESMO calculo: o TEXTO (`bloco_balanceado`/`bloco_apos`) e a
    FAIXA de indices `(inicio, fim)` INCLUSIVOS (`faixa_bloco_balanceado`/`faixa_bloco_apos`,
    fatia por `texto_da_faixa`). Quem precisa do FIM do bloco usa a FAIXA — NUNCA reconstroi a
    posicao com `codigo.index(bloco, pos) + len(bloco)`, porque essa volta ao texto pode casar
    uma COPIA do bloco dentro de um literal de string antes do bloco de verdade (FORMATO-7).
"""

import arcabouco as arc


# ------------------------------------------------------------------ scanner ---

def fim_do_literal(codigo, i):
    """Indice logo APOS o literal de string/char que comeca em `i` (trata o escape `\\`).

    `i` aponta para a aspa de abertura. Se o literal nao fechar (fonte cortado), devolve o
    fim do texto — o chamador que exige integridade reprova antes.
    """
    aspas = codigo[i]
    p = i + 1
    while p < len(codigo):
        if codigo[p] == "\\":        # escape: o proximo caractere nao fecha o literal
            p += 2
            continue
        if codigo[p] == aspas:
            return p + 1
        p += 1
    return len(codigo)


def _salta_comentario(codigo, p):
    """Se `p` abre um comentario, devolve o indice depois dele; senao, devolve `p`."""
    n = len(codigo)
    if codigo.startswith("//", p):
        fim = codigo.find("\n", p)
        return n if fim < 0 else fim
    if codigo.startswith("/*", p):
        fim = codigo.find("*/", p + 2)
        return n if fim < 0 else fim + 2
    return p


def _casa(codigo, i_abertura):
    """Indice do `}` que casa com o `{` em `i_abertura`, ou None se as chaves nao fecham.

    Literal-aware: `{`/`}` dentro de string/char nao contam. Comentarios contam como codigo
    por padrao (o chamador que os tem no texto usa `codigo_efetivo` antes).
    """
    nivel, p = 0, i_abertura
    while p < len(codigo):
        c = codigo[p]
        if c in "\"'":
            p = fim_do_literal(codigo, p)
            continue
        if c == "{":
            nivel += 1
        elif c == "}":
            nivel -= 1
            if nivel == 0:
                return p
        p += 1
    return None


# ------------------------------------------------------------------ recortes ---
# DUAS FORMAS DO MESMO RECORTE (FORMATO-7): o TEXTO (`bloco_*`) e a FAIXA de indices
# (`faixa_*`, `(inicio, fim)` INCLUSIVOS). As duas saem do MESMO calculo — `bloco_*` e
# literalmente `texto_da_faixa(codigo, faixa_*)` —, entao nao ha duas verdades para divergir.
# A faixa existe porque quem precisa do FIM do bloco (o caso da FORMATO-6) reconstruia a posicao
# com `codigo.index(bloco, pos) + len(bloco)`, e essa volta ao TEXTO pode casar uma COPIA do
# bloco dentro de um literal de string que esteja antes do bloco de verdade.

def texto_da_faixa(codigo, faixa):
    """O TEXTO da faixa `(inicio, fim)` INCLUSIVA devolvida pelos primitivos de faixa.

    O unico lugar que sabe que o `fim` e INCLUSIVO (fatia `codigo[inicio:fim + 1]`): "usar a
    faixa" e "usar o texto" tem de dar a MESMA fatia, sem cada consumidor repetir a soma.
    """
    arc.exigir(isinstance(faixa, tuple) and len(faixa) == 2,
               "texto_da_faixa: esperava uma faixa (inicio, fim), veio %r" % (faixa,))
    return codigo[faixa[0]:faixa[1] + 1]


def _faixa_balanceada(codigo, i_abertura):
    """(inicio, fim) INCLUSIVOS do bloco `{...}` que comeca em `i_abertura`. FALHA ALTO.

    `inicio` e o indice do proprio `{` e `fim` o do `}` que casa: `codigo[inicio:fim + 1]` e o
    bloco. E o primitivo que FALTAVA (FORMATO-7): da o FIM pela ESTRUTURA (casamento de chaves),
    sem o consumidor procurar o texto do bloco de volta no fonte.
    """
    arc.exigir(0 <= i_abertura < len(codigo) and codigo[i_abertura] == "{",
               "faixa do bloco: a posicao %d nao abre um bloco `{`" % i_abertura)
    fim = _casa(codigo, i_abertura)
    if fim is None:
        raise arc.Falhou(
            "as chaves abertas em %d NAO fecham — o fonte foi cortado?" % i_abertura)
    return i_abertura, fim


def faixa_bloco_balanceado(codigo, i_abertura):
    """(inicio, fim) INCLUSIVOS do bloco `{ ... }` que comeca em `i_abertura`. FALHA ALTO se nao fecha.

    A FAIXA do `bloco_balanceado` (mesma fatia: `texto_da_faixa(codigo, ...) == bloco_balanceado`).
    """
    return _faixa_balanceada(codigo, i_abertura)


def bloco_balanceado(codigo, i_abertura):
    """O bloco `{ ... }` que comeca em `i_abertura`, ate a chave que casa. FALHA ALTO se nao fecha."""
    return texto_da_faixa(codigo, _faixa_balanceada(codigo, i_abertura))


def _abertura_bloco_apos(codigo, ancora):
    """Indice do primeiro `{` em/depois de `ancora` (o `{` de um literal NAO conta). FALHA ALTO."""
    arc.exigir(0 <= ancora <= len(codigo), "bloco_apos: ancora %d fora do fonte" % ancora)
    p = ancora
    while p < len(codigo):
        c = codigo[p]
        if c == "{":
            return p
        if c in "\"'":               # `{` num literal nao abre bloco
            p = fim_do_literal(codigo, p)
            continue
        p += 1
    raise arc.Falhou("nao achei a abertura `{` do bloco a partir da posicao %d" % ancora)


def faixa_bloco_apos(codigo, ancora):
    """(inicio, fim) INCLUSIVOS do bloco `{ ... }` que COMECA no primeiro `{` em/depois de `ancora`.

    A FAIXA (nao o texto): e o que a FORMATO-6 precisava para achar o FIM estrutural — `inicio` e
    o `{` do bloco e `fim` o `}` que casa, entao o fim sai do CASAMENTO DE CHAVES, nunca de
    `codigo.index(bloco, pos) + len(bloco)` (essa busca pode casar uma copia do bloco dentro de um
    literal de string). FALHA ALTO se as chaves nao fecham, como o `bloco_apos`.
    """
    return _faixa_balanceada(codigo, _abertura_bloco_apos(codigo, ancora))


def bloco_apos(codigo, ancora):
    """O bloco `{ ... }` que COMECA no primeiro `{` em/depois de `ancora`. FALHA ALTO.

    E o que prende um ramo `if (...) { ... }` a partir do proprio `if`: o `{` procurado e o do
    ramo, nunca um solto antes dele. `bloco_apos == texto_da_faixa(faixa_bloco_apos(...))`.
    """
    return texto_da_faixa(codigo, faixa_bloco_apos(codigo, ancora))


def corpo_do_metodo(codigo, assinatura):
    """O CORPO INTEIRO do metodo: da ASSINATURA ate o `}` que casa com o `{` de abertura.

    E a versao reutilizavel do recorte que a FORMATO-2 escreveu no `t_formato_notas` — o mesmo
    contrato, num lugar so. Sem a assinatura, sem o `{`, ou com chaves que nao fecham -> FALHA
    ALTO (nunca devolve um pedaco).
    """
    i = codigo.find(assinatura)
    arc.exigir(i >= 0, "nao achei `%s` no fonte" % assinatura)
    abertura = codigo.find("{", i)
    arc.exigir(abertura >= 0, "a assinatura `%s` nao tem corpo (`{`) no fonte" % assinatura)
    fim = _casa(codigo, abertura)
    if fim is None:
        raise arc.Falhou(
            "as chaves do metodo `%s` NAO fecham — o fonte foi cortado?" % assinatura)
    return codigo[i:fim + 1]


def bloco_que_contem(codigo, ancora):
    """O MENOR bloco `{ ... }` (literal-aware) que CONTEM a posicao `ancora`. FALHA ALTO.

    E o recorte de um trecho DENTRO de um bloco ja delimitado — a entrada de uma tabela
    (`{ "chave", "valor" }`), o `try { ... }` de um caminho. Procura o `{` mais PROXIMO antes
    da ancora cujo bloco fecha DEPOIS dela: nao depende do fonte inteiro estar balanceado (um
    `{` solto num comentario distante nao interfere), e nao tem margem.
    """
    arc.exigir(0 <= ancora < len(codigo), "bloco_que_contem: ancora %d fora do fonte" % ancora)
    p = codigo.rfind("{", 0, ancora + 1)
    while p >= 0:
        fim = _casa(codigo, p)
        if fim is not None and fim > ancora:
            return codigo[p:fim + 1]
        p = codigo.rfind("{", 0, p)
    raise arc.Falhou("a posicao %d nao esta dentro de nenhum bloco `{...}` que feche — "
                     "o fonte foi cortado?" % ancora)


# ------------------------------------------------------------------- guardas ---

def exigir_metodo_inteiro(bloco, assinatura, marcas=()):
    """O GUARDA PERMANENTE contra a volta da janela: o recorte e o metodo INTEIRO?

    Exige (a) que o recorte FECHE nas chaves e (b) que ele contenha as `marcas` que provam ser
    o metodo ate o fim (o ultimo statement, o `catch`). Uma janela de caracteres corta ANTES
    disso e REPROVA aqui — nao ha como afrouxar sem apagar o guarda.
    """
    arc.exigir(bloco.rstrip().endswith("}"),
               "o recorte de `%s` NAO fecha nas chaves — nao e o metodo inteiro (voltou a ser "
               "uma janela de caracteres?)" % assinatura)
    for marca in marcas:
        arc.exigir(marca in bloco,
                   "o recorte de `%s` parou antes do fim do metodo: faltou %r (tem de ser o "
                   "corpo inteiro por casamento de chaves, nunca uma janela)" % (assinatura, marca))


# ------------------------------------------------- codigo efetivo (sem comentario) ---

def codigo_efetivo(codigo):
    """O fonte SEM comentario de linha/Bloco — a CITACAO num comentario nao e codigo.

    Preserva literais de string/char (o `//` dentro de um literal nao e comentario). Onde o
    recorte vai atravessar um trecho que tem comentario (ex.: uma tabela inteira), use este
    texto: um `{` citado num comentario deixaria de ser codigo e nao pode entrar na contagem.
    """
    saida, i, n, literal = [], 0, len(codigo), None
    while i < n:
        c = codigo[i]
        if literal is not None:
            saida.append(c)
            if c == "\\" and i + 1 < n:
                saida.append(codigo[i + 1])
                i += 2
                continue
            if c == literal:
                literal = None
            i += 1
            continue
        if c in "\"'":
            literal = c
            saida.append(c)
            i += 1
            continue
        p = _salta_comentario(codigo, i)
        if p != i:
            i = p
            continue
        saida.append(c)
        i += 1
    return "".join(saida)
