#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_bf.py - BF-2: as decisoes do portao de material do BetterFont, lidas do FONTE vivo.

POR QUE ESTA BIBLIOTECA EXISTE
------------------------------
O BF-1 (1.0.1) protegendo o efeito do material RECUSAVA exatamente o caso que ele
existe para consertar: o gate reprovava por SHADER DIFERENTE, e os textos de combate do
jogo (nome do inimigo, numero do dado) usam outra variante de SDF que o material da
fonte serifada - entao eles ficavam na fonte original, que e o defeito relatado pelo
dono. Uma revisao independente refutou o BF-1 por isso.

O conserto (BF-2, 1.0.2) e uma decisao de CODIGO dentro de `BetterFont/Plugin.cs`, e e
dificil de exercitar em teste puro (Material e classe nativa do Unity: nao se instancia
fora do jogo). O que SE PODE verificar a maquina, e o que estas regras fazem, e a
ESTRUTURA da decisao no fonte versionado:

  1. o gate NAO recusa por variante de shader (a recusa que produzia o defeito);
  2. o gate olha o EFEITO PRESENTE no material, nao a classificacao do texto nem a
     config (`TemEfeitoNoMaterial` antes de `EstiloTransportavel`);
  3. a config nao e pulada: a fonte e o estilo mudam JUNTOS e sao revertidos juntos
     (`ReverterTexto` no catch);
  4. os buracos de propriedade estao fechados (UNDERLAY_INNER, MASK_*/_ClipRect,
     _VertexOffsetX/Y, _WeightNormal/_WeightBold registrados);
  5. `_FaceTex`/`_BumpMap` so contam como efeito quando a textura e DE VERDADE
     (default "white"/"bump" do shader e a textura embutida do Unity);
  6. os defaults das tres chaves nao mudaram.

A regra do projeto (`docs/PLANO-DE-TESTES.md`) e que todo teste seja MOSTRADO REPROVANDO:
por isso o plantio do defeito vive em `fonte_com_o_defeito_do_bf1`, usado pela isca
`tools/testes/contra-prova/cp_bf_gate_shader.py` - o mesmo conjunto de checagens roda
contra um fonte com o defeito do BF-1 reinjetado e TEM de reprovar.
"""
import collections
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import recorte as rec


def caminho_do_fonte():
    return os.path.join(arc.raiz_do_repo(), "BetterFont", "Plugin.cs")


def fonte():
    """O fonte vivo do mod (nao uma copia: a expectativa fica amarrada ao que sera compilado)."""
    with io.open(caminho_do_fonte(), encoding="utf-8") as fh:
        return fh.read()


def corpo(src, declaracao):
    """Corpo `{...}` de um metodo, a partir da DECLARACAO exata — DELEGA ao recorte ESTRUTURAL.

    FORMATO-8 — O QUE ESTAVA ERRADO AQUI: o recorte era um casador de chaves LOCAL, cego a
    LITERAL de string e que devolvia `None` em SILENCIO (o oposto do contrato do `recorte.py`).
    Duas consequencias mediveis: um `}` dentro de um literal (`string s = "}";`) fechava o bloco
    CEDO — o corpo vinha TRUNCADO, faltando o que vinha depois —, e um metodo com as chaves que
    NAO fecham virava `None`, indistinguivel de "a declaracao nao existe" (um recorte vazio
    "passa" em toda checagem). Agora a conta e a do `recorte.py` (`rec.bloco_apos`): literal-aware
    (chave em string/char nao conta) e FALHA ALTO (`arc.Falhou`) quando as chaves nao fecham.

    `rec.bloco_apos` — e nao `rec.corpo_do_metodo` — porque o CONTRATO dos consumidores e o corpo
    COMECANDO em `{`: o parser do orcamento faz `_Programa(corpo[1:-1])` (tira a `{` e a `}`), e o
    `corpo_do_metodo` devolveria a ASSINATURA junto (as duas fatias sairiam do mesmo calculo, mas o
    consumidor nao le a assinatura). A declaracao AUSENTE continua devolvendo `None`: isso e um
    "nao achei" que o chamador relata como falha, nao um recorte silencioso.
    """
    i = src.find(declaracao)
    if i < 0:
        return None
    return rec.bloco_apos(src, i)


def sem_comentarios(src):
    """O CODIGO EFETIVO: o fonte sem comentario de LINHA (`//`) e de BLOCO (`/* */`).

    POR QUE ISTO EXISTE (FIX-6, achado da REV-56): a trava conferia TOKEN com `in`, e um
    comentario satisfaz substring. A variante (A) do defeito deixa a chamada
    `SceneManager.GetActiveScene()` DENTRO DE UM COMENTARIO (`// cena = ...GetActiveScene()...`)
    e le uma string fixa - a checagem antiga via `"GetActiveScene" in orcamento` dava verde com o
    reset DESLIGADO. Comentario nao e codigo: o que a conferencia de COMPORTAMENTO le e este
    texto. Literais de string/char sao preservados (o `//` dentro de um literal nao e comentario).
    """
    saida = []
    i, n = 0, len(src)
    literal = None
    while i < n:
        c = src[i]
        if literal is None:
            if src.startswith("//", i):
                while i < n and src[i] != "\n":
                    i += 1
                continue
            if src.startswith("/*", i):
                i += 2
                while i < n and not src.startswith("*/", i):
                    i += 1
                i += 2
                continue
            if c == '"' or c == "'":
                literal = c
            saida.append(c)
            i += 1
            continue
        saida.append(c)
        if c == "\\" and i + 1 < n:      # escape dentro do literal: o proximo nao fecha
            saida.append(src[i + 1])
            i += 2
            continue
        if c == literal:
            literal = None
        i += 1
    return "".join(saida)


# As declaracoes exatas que este modulo le. Se um nome mudar no fonte, a checagem
# REPROVA dizendo qual sumiu - em vez de passar vazia por cima de um metodo que nao
# existe mais (foi assim que uma varredura de tokens acusou 102 falsos positivos).
ET = "private bool EstiloTransportavel("
TEM_EFEITO = "private static bool TemEfeitoNoMaterial("
TEXTURA = "private static bool TexturaDeEfeito("
COPIAR = "private static string CopiarEstilo("
REVERTER = "private static void ReverterTexto("
DIAG = "private void Diagnostico("
SWEEP = "private void FontSweep()"
ORCAMENTO = "private void OrcamentoDoDiagnosticoPorCena()"

# Defaults das tres chaves (nao podem mudar nesta tarefa).
DEFAULTS = (
    ('BindSeguro("Estilo", "PreservarEstilo", true', "PreservarEstilo"),
    ('BindSeguro("Estilo", "PularTextosEstilizados", false', "PularTextosEstilizados"),
    ('BindSeguro("Diagnostico", "LogDiagnosticoEstilo", false', "LogDiagnosticoEstilo"),
)

# Acoplamento ZERO **NO CODIGO**: nenhuma linha do FONTE DO MOD (BetterFont/Plugin.cs) pode citar
# o outro mod. A trava varre SO esse arquivo — nao a doc, nao o manifest, nao o README. E de
# proposito: o README cita o BetterCombatText (nome e interacao) para EXPLICAR ao jogador a
# convivencia entre os dois, e isso e pedido pelo dono; o que nao pode e o CODIGO conhecer o outro
# mod (a regra do projeto e mods independentes — a copia de estilo vale para "qualquer mod", nao
# para um caso especifico). Se um dia isto passar a varrer docs/, o README vai reprovar aqui.
PROIBIDOS = ("BetterCombatText", "bettercombattext", "com.gumatos.bettercombattext",
             "DefRuivo_StolenRealmMods-BetterCombatText")


def _falta(texto, trecho, rotulo):
    return None if trecho in texto else "faltou %s (%r)" % (rotulo, trecho)


def falhas_da_fonte(src):
    """Devolve a lista de defeitos encontrados no fonte. Lista vazia = o conserto esta de pe."""
    falhas = []

    # ---------------------------------------------------------------- 1) o gate
    et = corpo(src, ET)
    if et is None:
        falhas.append("nao achei %s no fonte" % ET)
    else:
        if "antigo.shader != padraoNovo.shader" in et:
            falhas.append("o gate voltou a RECUSAR por variante de shader (o defeito do BF-1)")
        if "shader incompativel" in et:
            falhas.append("o gate tem motivo de recusa por shader no fonte (o defeito do BF-1)")
        if not any("TexturaDeEfeito(" in linha and "_FaceTex" in linha for linha in et.splitlines()):
            falhas.append("_FaceTex nao passa por TexturaDeEfeito: o default 'white' do shader "
                          "volta a ser contado como efeito e o gate recusa todo material de SDF")
        if not any("TexturaDeEfeito(" in linha and "_BumpMap" in linha for linha in et.splitlines()):
            falhas.append("_BumpMap nao passa por TexturaDeEfeito (default 'bump' do shader)")
        if "!transporteLigado" not in et:
            falhas.append("a conferencia nao separa 'ha copia pedida' de 'so efeito irreproduzivel'")

    # ------------------------------------------------- 2) o criterio do portao
    efeito = corpo(src, TEM_EFEITO)
    if efeito is None:
        falhas.append("nao achei %s (o criterio passou a ser a classificacao do texto?)" % TEM_EFEITO)
    textura = corpo(src, TEXTURA)
    if textura is None:
        falhas.append("nao achei %s (default de textura volta a contar como efeito)" % TEXTURA)
    else:
        for t in ("whiteTexture", "normalTexture", "blackTexture", "grayTexture"):
            if t not in textura:
                falhas.append("TexturaDeEfeito nao compara com Texture2D.%s (embutida do Unity)" % t)

    sweep = corpo(src, SWEEP)
    if sweep is None:
        falhas.append("nao achei %s" % SWEEP)
    else:
        if "TemEfeitoNoMaterial(" not in sweep:
            falhas.append("fontSweep nao chama TemEfeitoNoMaterial: o portao volta a olhar a "
                          "classificacao do texto em vez do efeito no material")
        linha_gate = [l for l in sweep.splitlines() if "EstiloTransportavel(" in l]
        if not linha_gate:
            falhas.append("fontSweep nao chama EstiloTransportavel")
        elif any("estilizado" in l for l in linha_gate):
            falhas.append("o portao voltou a ser condicionado a 'estilizado' (defeito do BF-1: "
                          "texto NAO classificado nao era protegido)")
        if "efeitoPresente &&" not in sweep:
            falhas.append("a chamada do portao nao esta presa ao efeito presente no material")

        # ------------------------------------------ 3) ordem da falha-segura
        # A troca de fonte e a copia tem de estar no MESMO bloco, com catch que REVERTE. O
        # trecho vai do inicio das variaveis do bloco ate o fim do catch.
        inicio_bloco = sweep.find("string registros = null;")
        if inicio_bloco < 0:
            inicio_bloco = sweep.find("string copiados = null;")
        trecho = sweep[inicio_bloco:] if inicio_bloco >= 0 else sweep
        pos_troca = trecho.find("t.font = _serifFont")
        pos_catch = trecho.find("catch (System.Exception e)")
        pos_reverte = trecho.find("ReverterTexto(")
        if pos_troca < 0:
            falhas.append("nao achei a troca de fonte no fontSweep")
        if pos_catch < 0 or pos_catch < pos_troca:
            falhas.append("a troca de fonte nao esta dentro do bloco com catch (falha-segura na ordem errada)")
        if pos_reverte < 0 or pos_reverte < pos_catch:
            falhas.append("a falha da troca/copia nao REVERTE o texto (fonte trocada com estilo parcial)")
    revert = corpo(src, REVERTER)
    if revert is None:
        falhas.append("nao achei %s" % REVERTER)
    else:
        if "t.font = fonteAntiga" not in revert:
            falhas.append("ReverterTexto nao devolve a fonte original")
        if "t.fontSharedMaterial = antigo" not in revert:
            falhas.append("ReverterTexto nao devolve o material original")

    # --------------------------------------- 4) buracos de propriedade fechados
    copiar = corpo(src, COPIAR)
    if copiar is None:
        falhas.append("nao achei %s" % COPIAR)
    else:
        for trecho, rotulo in (
            ("PropsVetor", "o grupo de propriedades de VETOR (_ClipRect)"),
            ("KeywordsMascara", "o grupo das keywords de recorte (MASK_*)"),
            ("UNDERLAY_INNER", "UNDERLAY_INNER transportado"),
            ("PropsDeFonteRegistradas", "_WeightNormal/_WeightBold registrados"),
            ("RegistrarDiferenca(", "o registro do que fica fora"),
            ("registros", "o canal de 'registros' (o que fica fora COM o motivo)"),
        ):
            f = _falta(copiar, trecho, rotulo)
            if f:
                falhas.append(f)

    # a declaracao dos grupos vive no nivel da classe (fora do CopiarEstilo)
    for trecho, rotulo in (
        ('"_VertexOffsetX", "_VertexOffsetY"', "_VertexOffsetX/_VertexOffsetY no grupo de floats"),
        ('"_MaskSoftnessX", "_MaskSoftnessY"', "_MaskSoftnessX/_MaskSoftnessY no grupo de floats"),
        ('"_ClipRect"', "_ClipRect no grupo de vetores"),
        ('"_WeightNormal", "_WeightBold"', "os dois pesos da fonte no grupo de registrados"),
        ('"MASK_SOFT", "MASK_HARD", "MASK_TEX"', "as tres keywords de masking"),
    ):
        f = _falta(src, trecho, rotulo)
        if f:
            falhas.append(f)

    # ------------------------------------------------- 5) diagnostico utilizavel
    diag = corpo(src, DIAG)
    if diag is None:
        falhas.append("nao achei %s" % DIAG)
    else:
        for trecho, rotulo in (
            ("shaderDestino", "o antes/depois da variante de shader na linha de diag"),
            ("registros:", "o campo de registros na linha de diag"),
            ("_diagLinhasDeEfeito", "o teto proprio das linhas de EFEITO"),
        ):
            f = _falta(diag, trecho, rotulo)
            if f:
                falhas.append(f)

    # ------------------------------------- 8) BF-2R: o orcamento do diagnostico
    # O achado da revisao da BF-2: a linha de COMBATE continuava podendo nao sair. Duas causas,
    # duas checagens: (a) os contadores eram da SESSAO e o orcamento se esgotava antes do combate
    # (a varredura de boot ve 400+ textos - 406 e 484 medidos no log do dono); (b) `deEfeito` era
    # tirado do CONTEUDO da linha, e como `copiados` nunca vem vazio num texto convertido, TODA
    # linha era contada como de efeito e o teto de ROTINA era INALCANCAVEL.
    orcamento = corpo(src, ORCAMENTO)
    if orcamento is None:
        falhas.append("nao achei %s: o orcamento do diagnostico voltou a ser da SESSAO "
                      "(o teto se esgota antes da cena de combate)" % ORCAMENTO)
    else:
        if "GetActiveScene" not in orcamento:
            falhas.append("o orcamento do diagnostico nao olha a CENA ativa: nao ha como ele "
                          "zerar por cena")
        # ---------------------------------------------------------------------------
        # BF-3 -> FIX-6 — A ALCANÇABILIDADE DO RESET, CONFERIDA POR COMPORTAMENTO.
        #
        # O QUE ESTAVA ERRADO (achado da REV-56): aqui havia quatro checagens de TOKEN
        # (`"if (cena == _diagCena)"`, `"_diagCena != null"`, a contagem de `return;` e a ORDEM
        # guarda->grava->zero). A revisao plantou TRES variantes do MESMO defeito que mantem
        # TODOS os tokens de pe e a lista de falhas veio VAZIA nas tres:
        #   (A) `cena = SceneManager.GetActiveScene()...` vira COMENTARIO e `cena` passa a ser
        #       string FIXA -> o reset roda so na PRIMEIRA cena (orcamento de sessao);
        #   (B) o ramo do ESCAPE volta a incrementar o contador de EFEITO (o defeito da BF-2R);
        #   (C) o corte do escape passa a depender do TETO DE EFEITO.
        # Comentario satisfaz substring; comportamento, nao. A conferencia passou a ser a de
        # `falhas_do_comportamento`: o modelo e LIDO DO CODIGO EFETIVO (sem comentarios) e roda a
        # SEQUENCIA REAL de pulados do dono - a mesma coisa que o teste puro faz. Os tokens
        # continuam sendo conferidos adiante, mas como SUBSIDIARIOS: quem tem de reprovar e o
        # comportamento.
        falhas.extend(falhas_do_comportamento(src))

    if diag is not None:
        # A ASSINATURA: o corpo comeca na chave, entao o parametro se le do trecho da declaracao.
        inicio = src.find(DIAG)
        assinatura = src[inicio:src.find("{", inicio)] if inicio >= 0 else ""
        if "TipoLinhaDiag tipo" not in assinatura:
            falhas.append("a classificacao da linha nao e explicita e de TRES vias: Diagnostico nao "
                          "recebe 'TipoLinhaDiag tipo' (quem chama tem de dizer se a linha e de ROTINA, "
                          "de EFEITO ou PULADA pelo escape - a BF-3 mostrou que 'de efeito = true' fixo "
                          "no escape esgotava o teto de 300 antes da linha de combate)")
        if "OrcamentoDoDiagnosticoPorCena()" not in diag:
            falhas.append("Diagnostico nao zera o orcamento por cena (o teto volta a ser da SESSAO)")
        for teto in NOMES_TETOS:
            if teto not in diag:
                falhas.append("os tetos do diagnostico nao usam a constante %s (o teste nao consegue "
                              "le-la do fonte)" % teto)
        # BF-3: o PULADO PELO ESCAPE tem de ter contador PROPRIO - nao pode disputar o de EFEITO.
        if "_diagLinhasDeEscape" not in diag:
            falhas.append("o pulado pelo escape nao tem contador PROPRIO (_diagLinhasDeEscape): com "
                          "PularTextosEstilizados ligado (a config do dono) os ~484 pulados de uma "
                          "varredura disputam o teto de EFEITO e a linha de combate fica de fora")
        for linha in diag.splitlines():
            if "IsNullOrEmpty" in linha and ("deEfeito" in linha or "tipo" in linha):
                falhas.append("a linha de EFEITO voltou a ser tirada do CONTEUDO da linha "
                              "(copiados/naoTransportados/registros): o teto de rotina fica "
                              "INALCANCAVEL, porque num texto convertido 'copiados' nunca vem vazio")

    if tetos_do_diagnostico(src) is None:
        falhas.append("nao achei TetoDiagRotina/TetoDiagEfeito/TetoDiagEscape como 'const int' no "
                      "fonte (sem eles o teste nao consegue ler os tetos sem digitar)")

    sweep2 = corpo(src, SWEEP)
    if sweep2 is not None:
        if "efeitoPresente ? TipoLinhaDiag.Efeito : TipoLinhaDiag.Rotina" not in sweep2:
            falhas.append("o call site do CONVERTIDO nao classifica a linha pelo EFEITO PRESENTE no "
                          "material (efeitoPresente): um texto SEM efeito no material volta a "
                          "consumir o teto de EFEITO")
        # BF-3: o texto pulado pelo ESCAPE nao pode ser contado como linha de EFEITO.
        if "TipoLinhaDiag.Escape" not in sweep2:
            falhas.append("o texto pulado pelo escape nao e marcado como PULADO (TipoLinhaDiag.Escape): "
                          "volta a contar como linha de EFEITO e o teto de 300 se esgota antes da "
                          "linha de combate na config do dono (PularTextosEstilizados ligado)")
        else:
            i_escape = sweep2.find('"PULADO (escape')
            if i_escape >= 0:
                # FORMATO-5: o recorte do call site do PULADO PELO ESCAPE e ESTRUTURAL, nunca uma
                # janela de caracteres. A janela de 900 media DISTANCIA: um retoque INOFENSIVO no
                # FontSweep entre o marcador e o argumento (1077 chars medidos) estourava a janela e
                # a checagem REPROVAVA por motivo ALHEIO ao defeito (FORMATO-4). O menor bloco `{...}`
                # que CONTEM o call site nao tem margem (medido: 408 chars) e `rec.bloco_que_contem`
                # FALHA ALTO se o bloco nao fechar - nunca devolve um pedaco que "passa" vazio.
                try:
                    bloco = rec.bloco_que_contem(sweep2, i_escape)
                except arc.Falhou as erro:
                    falhas.append("nao consegui recortar o call site do PULADO PELO ESCAPE por "
                                  "casamento de chaves: %s" % erro)
                else:
                    if "TipoLinhaDiag.Escape" not in bloco:
                        falhas.append("o call site do PULADO PELO ESCAPE nao passa TipoLinhaDiag.Escape "
                                      "(o pulo voltou a ser contado no orcamento de EFEITO)")
        if "IsNullOrEmpty(copiados)" in sweep2 or "IsNullOrEmpty(registros)" in sweep2:
            falhas.append("um call site de Diagnostico classifica a linha pelo CONTEUDO dela "
                          "(IsNullOrEmpty(copiados/registros)) - e o defeito da BF-2")

    # --------------------------------------------------- 6) defaults intactos
    for trecho, chave in DEFAULTS:
        f = _falta(src, trecho, "o default da chave " + chave)
        if f:
            falhas.append(f)

    # -------------------------------------------------- 7) acoplamento zero
    # O ESCOPO desta trava e o CODIGO do mod (BetterFont/Plugin.cs) - nao a doc. Ver o comentario
    # de PROIBIDOS: o README cita o outro mod de proposito, para explicar a convivencia.
    for proibido in PROIBIDOS:
        if proibido in src:
            falhas.append("acoplamento com outro mod NO CODIGO: o fonte cita %r" % proibido)

    return falhas


def fonte_com_o_defeito_do_bf1(src=None):
    """O MESMO fonte com o defeito do BF-1 reinjetado: a recusa por variante de shader.

    Nao mexe em arquivo nenhum: devolve o texto. E a isca (`cp_bf_gate_shader.py`) que usa
    isto para provar que as checagens acima reprovam de verdade.
    """
    texto = fonte() if src is None else src
    alvo = "                if (!transporteLigado)"
    defeito = ('                if (antigo.shader != padraoNovo.shader)\n'
               '                {\n'
               '                    motivo = "shader incompativel";\n'
               '                    return false;\n'
               '                }\n\n'
               '                if (!transporteLigado)')
    if alvo not in texto:
        return texto
    return texto.replace(alvo, defeito, 1)


def fonte_com_o_defeito_do_gate(src=None):
    """Segundo defeito plantado: o portao volta a olhar a classificacao do texto (BF-1)."""
    texto = fonte() if src is None else src
    alvo = "                        if (efeitoPresente &&"
    defeito = ("                        string motivoEstilo2;\n"
               "                        bool estilizadoDeNovo = EhEstilizado(antigo, fonteAntiga, out motivoEstilo2);\n"
               "                        if (estilizadoDeNovo && Plugin.PreservarEstiloLigado &&")
    if alvo not in texto:
        return texto
    return texto.replace(alvo, defeito, 1)

# ===========================================================================
# BF-2R - O ORCAMENTO DO DIAGNOSTICO (o defeito que escondia a linha de combate)
# ===========================================================================
#
# `FontUpdater` (BetterFont/Plugin.cs) mantem TRES contadores de linhas de diagnostico e os
# consulta em `Diagnostico`:
#
#   _diagLinhas         -> TetoDiagRotina   (linha de ROTINA: material SEM efeito nenhum)
#   _diagLinhasDeEfeito -> TetoDiagEfeito   (linha de EFEITO: material com efeito, pulado, revertido)
#   _diagLinhasDeEscape -> TetoDiagEscape   (linha PULADA pelo escape - nada foi transportado)
#
# e `OrcamentoDoDiagnosticoPorCena` ZERA os tres quando a cena ativa muda.
#
# NADA AQUI E DIGITADO: a contagem de textos e de pulados por varredura sai do log VERSIONADO
# (`tools/fixtures/bf-varredura-em-jogo.log`), a medicao dos textos com efeito no material sai do
# fixture `tools/fixtures/bf-efeito-no-boot.json`, os TETOS sao lidos do fonte vivo
# (`tetos_do_diagnostico`) e o COMPORTAMENTO e EXECUTADO do codigo efetivo do fonte
# (`MaquinaDoDiagnostico`, FIX-8).

NOMES_TETOS = ("TetoDiagRotina", "TetoDiagEfeito", "TetoDiagEscape")
LOG_VARREDURA = os.path.join("tools", "fixtures", "bf-varredura-em-jogo.log")
FIXTURE_EFEITO = os.path.join("tools", "fixtures", "bf-efeito-no-boot.json")


def tetos_do_diagnostico(src=None):
    """Le `TetoDiagRotina`/`TetoDiagEfeito`/`TetoDiagEscape` do FONTE. Devolve a tupla ou None.

    Nunca digitado: se o nome de uma constante mudar, isto devolve None e a checagem REPROVA
    dizendo qual sumiu - em vez de passar por cima com numero velho.
    """
    texto = fonte() if src is None else src
    valores = []
    for nome in NOMES_TETOS:
        casamento = re.search(r"const\s+int\s+" + nome + r"\s*=\s*(\d+)", texto)
        if casamento is None:
            return None
        valores.append(int(casamento.group(1)))
    return tuple(valores)


# ---------------------------------------------------------------- a escala medida (versionada)
_CAMPOS_DA_VARREDURA = (
    ("convertidos", r"(\d+)\s+texto\(s\)\s+convertidos"),
    ("pulados", r"(\d+)\s+pulado\(s\)"),
    ("intocados", r"(\d+)\s+intocado\(s\)"),
    ("ja_na_serifa", r"(\d+)\s+(?:ja|j\u00e1)\s+na\s+serifa"),
)


def varreduras_medidas():
    """As varreduras do log VERSIONADO, campo a campo. `None` = o log de prova sumiu.

    Cada linha de resumo do `Better Font: varredura - ...` vira um dict com os campos nomeados e o
    TOTAL (`textos`), que e a soma dos inteiros da linha: foi assim que o FORMATO do resumo pode
    mudar entre a 1.0.1 ("pulado(s) por material estilizado") e a 1.0.2 ("pulado(s) pelo escape")
    sem quebrar a leitura. Linhas `#` sao procedencia, nao dado.
    """
    caminho = os.path.join(arc.raiz_do_repo(), LOG_VARREDURA)
    if not os.path.isfile(caminho):
        return None
    varreduras = []
    with io.open(caminho, encoding="utf-8") as fh:
        for linha in fh:
            if linha.lstrip().startswith("#") or u"varredura \u2014" not in linha:
                continue
            dado = {"linha": linha.strip()}
            for nome, padrao in _CAMPOS_DA_VARREDURA:
                casamento = re.search(padrao, linha)
                dado[nome] = int(casamento.group(1)) if casamento else 0
            dado["textos"] = sum(int(n) for n in re.findall(r"\d+", linha))
            varreduras.append(dado)
    return varreduras


def textos_por_varredura():
    """Quantos textos cada varredura encontrou, lido do log VERSIONADO (medicao em jogo)."""
    varreduras = varreduras_medidas()
    return None if varreduras is None else [d["textos"] for d in varreduras]


def pulados_por_varredura():
    """Quantos textos cada varredura PULOU PELO ESCAPE, lido do MESMO log versionado."""
    varreduras = varreduras_medidas()
    return None if varreduras is None else [d["pulados"] for d in varreduras]


def maior_varredura():
    """A varredura de MAIOR total do log versionado (a escala da config do dono)."""
    varreduras = varreduras_medidas()
    if not varreduras:
        return None
    return max(varreduras, key=lambda d: d["textos"])


def maior_pulado_medido():
    """O MAIOR pulo pelo escape de UMA cena no log VERSIONADO - a base do `TetoDiagEscape`.

    FIX-8 (achado 2 da FIX-7R): e ESTE numero que dimensiona o teto, e nao a projecao da
    varredura de 793 objetos - que so existia em log gitignored, fechava 793 exato com ZERO
    pulados e, tomada como base mesmo assim, so tem 414 textos que chegam ao escape. O log
    versionado mede 484, 406, 484 e 624 pulados por cena; o maior e 624, entao o teto so precisa
    passar de 624 (o antigo 700 JA cobria - a premissa de que ele estava apertado cai; o 900
    fica como folga deliberada de limite de log).
    """
    pulados = pulados_por_varredura()
    return None if not pulados else max(pulados)


def candidatos_ao_escape(varredura=None):
    """Quantos textos de uma varredura PODEM chegar ao escape: os que NAO estao ja na serifa.

    FIX-8 (achado 2 da FIX-7R): a ordem do `FontSweep` e
    `if (t.font == _serifFont) { jaNaSerifa++; continue; }` ANTES do escape - o texto que ja esta
    na serifa NUNCA chega ao `PularTextosEstilizados`. Logo o pulado de uma passada e limitado por
    `textos - ja_na_serifa`, e nao pelo total da varredura.
    """
    dado = maior_varredura() if varredura is None else varredura
    if not dado:
        return None
    return dado["textos"] - dado["ja_na_serifa"]


def fracao_de_pulo_da_maior_varredura():
    """A FRACAO DE PULO da maior varredura medida - sobre QUEM CHEGA ao escape, nao sobre o total.

    FIX-8: a fracao era 624/640 = 0,975, com o TOTAL no denominador. Os 12 textos que a varredura
    de 640 ja encontrou na serifa nao passam pelo escape, entao o denominador certo e
    640 - 12 = 628 e a fracao e 624/628 = 0,9936.
    """
    dado = maior_varredura()
    if not dado:
        return None
    candidatos = candidatos_ao_escape(dado)
    if not candidatos:
        return None
    return dado["pulados"] / float(candidatos)


def pulados_da_sessao_do_dono():
    """A sequencia REAL de pulados por CENA de uma sessao do dono, do log versionado.

    FIX-8: aqui havia uma PROJECAO (793 textos x a fracao errada = 773) que dimensionava o teto do
    escape. Ela caiu por dois motivos: (a) o denominador estava errado (0,975 em vez de 0,9936);
    (b) a varredura de 793 objetos NAO foi feita com o escape ligado - 353 convertidos + 61
    intocados + 379 ja na serifa = 793 EXATO, ZERO pulado pelo escape - entao ela nao projeta pulo
    nenhum. O que fica e a sequencia MEDIDA: 484, 406, 484 e 624 pulados, uma por cena.
    """
    pulados = pulados_por_varredura()
    return None if not pulados else list(pulados)


def textos_com_efeito_no_boot():
    """A MEDICAO, num boot real, de quantos textos TMP tem EFEITO no material (BF-3).

    O teste da BF-2R usava `efeitos_no_boot = 5` DIGITADO. Este numero a maquina le de
    `tools/fixtures/bf-efeito-no-boot.json`, que traz a medicao do boot real, a derivacao (de
    quais linhas ela saiu) e a procedencia - nunca um numero digitado no teste.
    """
    caminho = os.path.join(arc.raiz_do_repo(), FIXTURE_EFEITO)
    if not os.path.isfile(caminho):
        return None
    with io.open(caminho, encoding="utf-8") as fh:
        return __import__("json").load(fh)


ROTINA = "rotina"
EFEITO = "efeito"
ESCAPE = "escape"


class ModeloOrcamentoDiag(object):
    """MODELO do orcamento de linhas do diagnostico do BetterFont (BF-2R/BF-3, C# -> Python).

    E a transcricao das REGRAS, usada como ISCA nos testes: rodar o mesmo cenario neste modelo e
    nos modelos do DEFEITO (abaixo) e o que prova que o cenario discrimina. Quem julga o FONTE e a
    `MaquinaDoDiagnostico` (FIX-8), que EXECUTA o codigo efetivo.
    """

    def __init__(self, teto_rotina, teto_efeito, teto_escape=0):
        self.teto_rotina = teto_rotina
        self.teto_efeito = teto_efeito
        self.teto_escape = teto_escape
        self.cena = None
        self.rotina = 0
        self.efeito = 0
        self.escape = 0
        self.cortes_rotina = 0
        self.cortes_efeito = 0
        self.cortes_escape = 0
        self.linhas = []
        self.cenas_zeradas = []

    def _zera_se_trocou_de_cena(self, cena):
        """`OrcamentoDoDiagnosticoPorCena`: cena igual = mantem; cena nova = zera os tres."""
        if cena == self.cena:
            return
        self.cena = cena
        self.rotina = 0
        self.efeito = 0
        self.escape = 0
        self.cenas_zeradas.append(cena)

    def logar(self, cena, rotulo, tipo):
        """`Diagnostico(...)`: aplica o teto do TIPO da linha e devolve se ela foi logada."""
        self._zera_se_trocou_de_cena(cena)
        if tipo == EFEITO:
            if self.efeito >= self.teto_efeito:
                self.cortes_efeito += 1
                return False
            self.efeito += 1
        elif tipo == ESCAPE:
            if self.escape >= self.teto_escape:
                self.cortes_escape += 1
                return False
            self.escape += 1
        else:
            if self.rotina >= self.teto_rotina:
                self.cortes_rotina += 1
                return False
            self.rotina += 1
        self.linhas.append(rotulo)
        return True


class ModeloOrcamentoDiagAntesBF2R(ModeloOrcamentoDiag):
    """O orcamento COMO ESTAVA na BF-2 - o defeito que a revisao mediu, transcrito.

    (A) `deEfeito` vinha do CONTEUDO da linha e num texto convertido `copiados` nunca vem vazio,
        entao TODA linha era de EFEITO (o teto de ROTINA era inalcancavel);
    (B) os contadores eram da SESSAO: nao existia cena, nada zerava.
    """

    def _zera_se_trocou_de_cena(self, cena):
        self.cena = cena  # a cena e registrada, mas NADA e zerado: orcamento da sessao

    def logar(self, cena, rotulo, tipo):
        return ModeloOrcamentoDiag.logar(self, cena, rotulo, EFEITO)


class ModeloOrcamentoDiagEscapeComoEfeito(ModeloOrcamentoDiag):
    """O orcamento COMO ESTA na BF-2R - o defeito que a BF-3 conserta (achado da revisao).

    O unico defeito aqui e o call site do PULADO PELO ESCAPE passar "de efeito": o modelo e o do
    conserto (por cena, com a classificacao explicita), mas o pulo pelo escape E contado no
    orcamento de EFEITO. Com `PularTextosEstilizados=true` (a config do dono) a varredura pula
    ~484 textos numa passada e o teto de 300 se esgota ANTES da linha de combate - que nessa
    config E um pulado.
    """

    def logar(self, cena, rotulo, tipo):
        return ModeloOrcamentoDiag.logar(self, cena, rotulo, EFEITO if tipo == ESCAPE else tipo)


class ModeloOrcamentoDiagResetSoNaPrimeiraCena(ModeloOrcamentoDiag):
    """O ponto cego da trava da BF-2R: o reset existe, mas so ALCANCA a PRIMEIRA cena.

    E o `if (_diagCena != null) { return; }` (em vez de `if (cena == _diagCena)`): depois da
    primeira cena o orcamento nunca mais zera - volta a ser o da SESSAO, com o teto de efeito se
    esgotando antes da cena de combate.
    """

    def _zera_se_trocou_de_cena(self, cena):
        if self.cena is not None:
            return  # `_diagCena != null`: ja rodou uma vez, nunca mais zera
        self.cena = cena
        self.rotina = 0
        self.efeito = 0
        self.escape = 0
        self.cenas_zeradas.append(cena)


def fonte_com_o_orcamento_da_bf2(src=None):
    """Reinjeta no fonte os DEFEITOS do orcamento da BF-2 (o que a revisao achou).

    Sao DOIS defeitos, e as checagens tem de pegar os dois:
      (a) sem a chamada de `OrcamentoDoDiagnosticoPorCena` em `Diagnostico` -> o orcamento volta a
          ser da SESSAO e o teto se esgota antes da cena de combate;
      (b) a classificacao da linha volta a sair do CONTEUDO dela, em vez de `efeitoPresente`:
          o call site do CONVERTIDO passa `!IsNullOrEmpty(copiados)`. Como `copiados` nunca vem
          vazio num texto convertido, toda linha e de EFEITO e o teto de ROTINA fica inalcancavel.
    """
    texto = fonte() if src is None else src

    alvo_cena = "            OrcamentoDoDiagnosticoPorCena();\n"
    if alvo_cena in texto:
        texto = texto.replace(alvo_cena, "", 1)

    alvo_classificacao = "efeitoPresente ? TipoLinhaDiag.Efeito : TipoLinhaDiag.Rotina);"
    if alvo_classificacao in texto:
        texto = texto.replace(alvo_classificacao,
                              "!string.IsNullOrEmpty(copiados) ? TipoLinhaDiag.Efeito : TipoLinhaDiag.Rotina);", 1)

    return texto


def fonte_com_o_escape_como_efeito(src=None):
    """Reinjeta o defeito que a BF-3 conserta: o PULADO PELO ESCAPE contado como EFEITO.

    E o `true` fixo no call site do escape (o estado da BF-2R): com a chave do dono ligada os
    ~484 pulados de uma varredura passam a disputar o teto de EFEITO (300) e a linha de combate
    fica de fora. Nao mexe em mais nada: so a classificacao do escape.
    """
    texto = fonte() if src is None else src
    alvo = '"n/a (texto pulado: nada foi transportado)", null, TipoLinhaDiag.Escape);'
    if alvo in texto:
        texto = texto.replace(alvo, '"n/a (texto pulado: nada foi transportado)", null, TipoLinhaDiag.Efeito);', 1)
    return texto


def fonte_com_o_reset_so_na_primeira_cena(src=None):
    """O ponto cego da trava da BF-2R, plantado: `if (_diagCena != null)` no lugar do guarda.

    O reset continua existindo e os tokens do zero continuam iguais - por isso a checagem antiga
    (que conferia os TOKENS) passava. O que muda e que o reset deixa de ser ALCANCAVEL a cada
    troca de cena: depois da primeira, nada zera.
    """
    texto = fonte() if src is None else src
    alvo = "            if (cena == _diagCena)\n"
    if alvo in texto:
        texto = texto.replace(alvo, "            if (_diagCena != null)\n", 1)
    return texto


def fonte_com_o_reset_inalcancavel(src=None):
    """O jeito DIRETO de desligar o reset sem mexer em token nenhum: `if (true) { return; }`.

    O `return` sai ANTES de qualquer zero, entao o orcamento e sempre o da SESSAO; os tokens do
    zero (e o guarda) continuam no fonte, intocados.
    """
    texto = fonte() if src is None else src
    alvo = "        private void OrcamentoDoDiagnosticoPorCena()\n        {\n"
    if alvo in texto:
        texto = texto.replace(alvo, alvo + "            if (true)\n            {\n                return;\n            }\n\n", 1)
    return texto


def fonte_com_o_zeramento_em_if_falso(src=None):
    """A variante plantada pela FIX-7R (1): o bloco de ZERAMENTO dentro de um `if (false)`.

    Os tokens do zero continuam TODOS no fonte (os tres `= 0;` estao la, o guarda esta la, ha um
    `return;` so) - e a checagem de TOKEN dava lista VAZIA. Comportamento: o `if (false)` nunca
    executa, entao o orcamento nunca zera e o primeiro texto de cada cena e contado contra a cena
    anterior.
    """
    texto = fonte() if src is None else src
    alvo = ("            _diagCena = cena;\n"
            "            _diagLinhas = 0;\n"
            "            _diagLinhasDeEfeito = 0;\n"
            "            _diagLinhasDeEscape = 0;\n")
    novo = ("            _diagCena = cena;\n"
            "            if (false)\n"
            "            {\n"
            "                _diagLinhas = 0;\n"
            "                _diagLinhasDeEfeito = 0;\n"
            "                _diagLinhasDeEscape = 0;\n"
            "            }\n")
    if alvo in texto:
        texto = texto.replace(alvo, novo, 1)
    return texto


def fonte_com_a_cena_gravada_antes_do_guarda(src=None):
    """A variante plantada pela FIX-7R (2): `_diagCena = cena;` ANTES do guarda.

    O guarda continua escrito `if (cena == _diagCena)` - mas com a cena ja gravada ele fica
    SEMPRE verdadeiro, entao o corpo (com os tres zeros) nunca executa. Para a checagem de TOKEN
    nao mudou NADA: a comparacao de cena, os tres zeramentos e a contagem de `return;` estao
    identicos. Comportamento: o zeramento nao e alcancado em troca de cena nenhuma.
    """
    texto = fonte() if src is None else src
    alvo = ("            if (cena == _diagCena)\n"
            "            {\n"
            "                return;\n"
            "            }\n"
            "\n"
            "            _diagCena = cena;\n")
    novo = ("            _diagCena = cena;\n"
            "\n"
            "            if (cena == _diagCena)\n"
            "            {\n"
            "                return;\n"
            "            }\n")
    if alvo in texto:
        texto = texto.replace(alvo, novo, 1)
    return texto


def fonte_com_o_reset_depois_do_uso(src=None):
    """A variante plantada pela FIX-7R (3): o reset CHAMADO depois do uso do contador.

    Tira a chamada de `OrcamentoDoDiagnosticoPorCena()` de antes dos cortes e a poe depois deles
    (mas antes dos incrementos). Todos os tokens de pe - o reset existe, a comparacao de cena
    existe, os tres zeros existem. Comportamento: o PRIMEIRO texto de cada cena e julgado contra o
    orcamento da cena ANTERIOR, que pode estar esgotado - e a linha que interessa cai.
    """
    texto = fonte() if src is None else src
    alvo = "            OrcamentoDoDiagnosticoPorCena();\n\n"
    if alvo not in texto:
        return texto
    texto = texto.replace(alvo, "", 1)
    marco = ("            if (tipo == TipoLinhaDiag.Efeito)\n"
             "            {\n"
             "                _diagLinhasDeEfeito++;\n")
    if marco in texto:
        texto = texto.replace(marco, "            OrcamentoDoDiagnosticoPorCena();\n\n" + marco, 1)
    return texto


# ===========================================================================
# FIX-8 - A CONFERENCIA DE COMPORTAMENTO: EXECUTAR o orcamento, nao reconhecer a forma
# ===========================================================================
#
# O QUE ESTAVA ERRADO (achado 1 da FIX-7R, que refutou o FIX-6/FIX-7): a conferencia lia TOKEN do
# fonte - a comparacao de cena, os tres `= 0;`, a contagem de `return;` - e montava um modelo a
# parte. A revisao plantou, e MEDIU, tres variantes que mantem TODOS os tokens:
#
#   (1) o bloco de zeramento dentro de um `if (false) { ... }`              -> o zero nunca roda;
#   (2) `_diagCena = cena;` ANTES do guarda `if (cena == _diagCena)`        -> guarda sempre
#       verdadeiro: o corpo (com os tres zeros) nunca roda;
#   (3) a chamada do reset DEPOIS do uso do contador                       -> o primeiro texto de
#       cada cena e contado contra o orcamento da cena anterior.
#
# Nas duas primeiras a lista de falhas vinha VAZIA - e o teste do orcamento E o teste-vigia davam
# verde com o defeito plantado. Zerar SO UM contador era pego (o modelo contava `= 0;`); zerar
# DEPOIS de usar passava. O erro de fundo nao era a GRAFIA da variante conhecida, era a CLASSE:
# "o zeramento e ALCANCADO a cada troca de cena" e "acontece ANTES do contador ser usado" nao se
# decidem lendo forma - decidem-se EXECUTANDO.
#
# O que a conferencia faz agora: parseia o CODIGO EFETIVO (sem comentarios) de
# `OrcamentoDoDiagnosticoPorCena` e de `Diagnostico` num subconjunto de C# (expressoes com
# precedencia, if/else, try/catch, return, blocos) e EXECUTA os statements sobre um ambiente. O
# contador do modelo E o contador do fonte; `if (false)`, guarda sempre verdadeiro e chamada
# depois do uso sao consequencia da execucao, nao de um padrao reconhecido.
#
# OS CENARIOS (todos rodam sobre o fonte vivo):
#   (A) ALCANCE + ORDEM - enche o contador de CADA tipo de linha ate o corte, troca de cena e
#       pede UMA linha do mesmo tipo: ela TEM de sair (o zero foi alcancado E veio antes do uso);
#   (B) a sequencia REAL de pulados do dono (log versionado) e a linha de COMBATE no fim -> sai;
#   (C) o pulado pelo escape NAO gasta o orcamento de EFEITO (lido dos contadores executados);
#   (D) a cena MISTA (efeito alem do teto + pulos, na MESMA cena) -> a linha de COMBATE sai - e
#       NAO RODAR O CENARIO E FALHA ALTA, nunca silencio (achado 3 da FIX-7R).


class NaoEntendi(Exception):
    """O interpretador nao entendeu um trecho do fonte. Quem chama REPROVA - nunca passa vazio."""


class Simbolico(object):
    """Valor que o interpretador NAO calcula (objeto do jogo, membro ou chamada desconhecida).

    Compara por IDENTIDADE - um simbolo nunca e igual a um literal nem a outro simbolo - e vale
    como referencia nao nula, que e a convencao do C# para um objeto que existe.
    """
    _contador = [0]

    def __init__(self, nome="?"):
        Simbolico._contador[0] += 1
        self.nome = nome
        self.id = Simbolico._contador[0]

    def __repr__(self):
        return "<%s#%d>" % (self.nome, self.id)

    def __eq__(self, outro):
        return self is outro

    def __ne__(self, outro):
        return self is not outro

    def __hash__(self):
        return self.id

    def __bool__(self):
        return True


_NAO_SEI = object()

_TOKENS = re.compile(
    r"(?P<espaco>\s+)"
    r"|(?P<numero>\d+)"
    r"|(?P<nome>[A-Za-z_]\w*)"
    r"|(?P<op>\+\+|--|&&|\|\||==|!=|>=|<=|\+=|-=|[+\-*/%<>=!?:.,;()\[\]{}&])"
)


def _fim_do_literal(texto, i):
    """Indice DEPOIS do literal que comeca em `i` - aspa simples, aspa dupla ou interpolada `$"`.

    A interpolada precisa de cuidado: o jogo escreve `$"fonte='{... : "(nula)")}' -> "`, com
    literais DENTRO das chaves. O que fecha o literal e a aspa de fora, com o nivel de chaves em
    zero - nao a primeira aspa que aparece.
    """
    interpolada = texto[i] == "$"
    if interpolada:
        i += 1
    aspa = texto[i]
    i += 1
    nivel = 0
    while i < len(texto):
        c = texto[i]
        if aspa == '"' and c == "\\":
            i += 2
            continue
        if interpolada and c == "{":
            if texto[i + 1:i + 2] == "{":
                i += 2
                continue
            nivel += 1
            i += 1
            continue
        if interpolada and c == "}" and nivel > 0:
            if texto[i + 1:i + 2] == "}":
                i += 2
                continue
            nivel -= 1
            i += 1
            continue
        if c == aspa and nivel == 0:
            return i + 1
        i += 1
    raise NaoEntendi("literal sem fechar a partir de %r" % (texto[max(0, i - 30):i + 20],))


def _e_inicio_de_literal(texto, i):
    c = texto[i]
    return c == '"' or c == "'" or (c == "$" and texto[i + 1:i + 2] == '"')


def _tokeniza(texto):
    """Tokeniza uma expressao (literais, nomes, operadores). Fonte ilegivel = NaoEntendi."""
    saida = []
    i = 0
    while i < len(texto):
        if _e_inicio_de_literal(texto, i):
            fim = _fim_do_literal(texto, i)
            saida.append(("texto", texto[i:fim]))
            i = fim
            continue
        casamento = _TOKENS.match(texto, i)
        if casamento is None:
            raise NaoEntendi("nao consegui ler o trecho %r" % texto[i:i + 40])
        i = casamento.end()
        if casamento.lastgroup != "espaco":
            saida.append((casamento.lastgroup, casamento.group()))
    return saida


def _texto_do_literal(bruto):
    """Desfaz as aspas e os escapes de um literal de string/char; `$"..."` perde o `$`."""
    if bruto.startswith("$"):
        bruto = bruto[1:]
    corpo = bruto[1:-1]
    corpo = corpo.replace('\\"', '"').replace("\\'", "'").replace("\\\\", "\\")
    return corpo


class Contexto(object):
    """O que a EXECUCAO enxerga: constantes, variaveis locais, campos da classe e a cena atual."""

    def __init__(self, tetos=None, variaveis=None, campos=None, cena=None, maquina=None):
        self.tetos = tetos or {}
        self.variaveis = variaveis if variaveis is not None else {}
        self.campos = campos if campos is not None else {}
        self.cena = cena
        self.maquina = maquina
        self.em_diagnostico = True
        self.logou = False
        self.avisos = []

    def le(self, nome):
        if nome in self.variaveis:
            return self.variaveis[nome]
        if nome.startswith("_") and nome in self.campos:
            return self.campos[nome]
        if nome in ("Plugin.LogDiagnosticoLigado", "Plugin.PularEstilizadosLigado"):
            return True          # a config do dono: diagnostico LIGADO
        if nome in self.tetos:
            return int(self.tetos[nome])
        if nome.startswith("TipoLinhaDiag."):
            return nome.split(".")[-1]
        return _NAO_SEI

    def grava(self, nome, valor):
        if nome.startswith("_"):
            self.campos[nome] = valor
        else:
            self.variaveis[nome] = valor


class _Retorno(Exception):
    """O `return;` do codigo executado."""


class _Expr(object):
    """Avaliador de EXPRESSOES do subconjunto usado pelo orcamento (precedencia de C#)."""

    def __init__(self, texto, contexto):
        self.tk = _tokeniza(texto)
        self.i = 0
        self.ctx = contexto

    def atual(self):
        return self.tk[self.i] if self.i < len(self.tk) else ("fim", "")

    def come(self):
        t = self.atual()
        self.i += 1
        return t

    def espera(self, valor):
        t = self.come()
        if t[1] != valor:
            raise NaoEntendi("esperava %r e achei %r" % (valor, t[1]))
        return t

    def avaliar(self):
        valor = self.ternario()
        if self.atual()[1] != "":
            raise NaoEntendi("sobrou %r na expressao" % self.atual()[1])
        return valor

    def ternario(self):
        condicao = self.ou()
        if self.atual()[1] == "?":
            self.come()
            entao = self.ternario()
            self.espera(":")
            senao = self.ternario()
            return entao if bool(condicao) else senao
        return condicao

    # ---- precedencia (do mais fraco ao mais forte)
    def ou(self):
        valor = self.e_()
        while self.atual()[1] == "||":
            self.come()
            outro = self.e_()
            valor = bool(valor) or bool(outro)
        return valor

    def e_(self):
        valor = self.igualdade()
        while self.atual()[1] == "&&":
            self.come()
            outro = self.igualdade()
            valor = bool(valor) and bool(outro)
        return valor

    def igualdade(self):
        valor = self.relacao()
        while self.atual()[1] in ("==", "!="):
            operador = self.come()[1]
            outro = self.relacao()
            valor = (valor == outro) if operador == "==" else (valor != outro)
        return valor

    def relacao(self):
        valor = self.soma()
        while self.atual()[1] in ("<", ">", "<=", ">="):
            operador = self.come()[1]
            outro = self.soma()
            try:
                if operador == "<":
                    valor = valor < outro
                elif operador == ">":
                    valor = valor > outro
                elif operador == "<=":
                    valor = valor <= outro
                else:
                    valor = valor >= outro
            except TypeError:
                raise NaoEntendi("nao sei comparar %r %s %r" % (valor, operador, outro))
        return valor

    def soma(self):
        valor = self.produto()
        while self.atual()[1] in ("+", "-"):
            operador = self.come()[1]
            outro = self.produto()
            if operador == "+":
                if isinstance(valor, (int, float)) and isinstance(outro, (int, float)):
                    valor = valor + outro
                else:
                    valor = str(valor) + str(outro)
            else:
                try:
                    valor = valor - outro
                except TypeError:
                    raise NaoEntendi("nao sei subtrair %r - %r" % (valor, outro))
        return valor

    def produto(self):
        valor = self.unario()
        while self.atual()[1] in ("*", "/", "%"):
            operador = self.come()[1]
            outro = self.unario()
            try:
                if operador == "*":
                    valor = valor * outro
                elif operador == "/":
                    valor = valor / outro
                else:
                    valor = valor % outro
            except TypeError:
                raise NaoEntendi("nao sei calcular %r %s %r" % (valor, operador, outro))
        return valor

    def unario(self):
        if self.atual()[1] == "!":
            self.come()
            return not bool(self.unario())
        if self.atual()[1] == "-":
            self.come()
            valor = self.unario()
            if not isinstance(valor, (int, float)):
                raise NaoEntendi("nao sei negar %r" % (valor,))
            return -valor
        return self.posfixo()

    # ---- primarios, membros e chamadas
    def posfixo(self):
        valor, caminho = self.primario()
        while True:
            t = self.atual()
            if t[1] == ".":
                self.come()
                nome = self.come()[1]
                caminho = (caminho + "." + nome) if caminho else nome
                valor = self._membro(valor, caminho, nome)
            elif t[1] == "(":
                argumentos = self._argumentos()
                valor = self._chamada(caminho, valor, argumentos)
                caminho = None
            else:
                break
        return valor

    def primario(self):
        t = self.atual()
        if t[0] == "numero":
            self.come()
            return int(t[1]), None
        if t[0] == "texto":
            self.come()
            return _texto_do_literal(t[1]), None
        if t[1] == "(":
            self.come()
            valor = self.ternario()
            self.espera(")")
            return valor, None
        if t[0] == "nome":
            self.come()
            nome = t[1]
            if nome == "true":
                return True, None
            if nome == "false":
                return False, None
            if nome == "null":
                return None, None
            valor = self.ctx.le(nome)
            return (Simbolico(nome) if valor is _NAO_SEI else valor), nome
        raise NaoEntendi("nao entendi o comeco da expressao em %r" % (t[1],))

    def _argumentos(self):
        self.espera("(")
        argumentos = []
        if self.atual()[1] == ")":
            self.come()
            return argumentos
        while True:
            argumentos.append(self.ternario())
            t = self.come()
            if t[1] == ")":
                return argumentos
            if t[1] != ",":
                raise NaoEntendi("esperava ',' ou ')' na chamada e achei %r" % (t[1],))

    def _membro(self, valor, caminho, nome):
        # `GetActiveScene().name` - a cena lida e uma string, e `.name` dela e ela propria.
        if isinstance(valor, str) and nome == "name":
            return valor
        # `TipoLinhaDiag.Efeito` - o enum, pelo nome do valor (a comparacao e com o parametro).
        if caminho.startswith("TipoLinhaDiag."):
            return caminho.split(".")[-1]
        return Simbolico(caminho)

    def _chamada(self, caminho, receptor, argumentos):
        ultimo = caminho.split(".")[-1] if caminho else ""
        ctx = self.ctx
        if ultimo == "GetActiveScene":
            return ctx.cena
        if ultimo == "OrcamentoDoDiagnosticoPorCena":
            if ctx.maquina is not None:
                ctx.maquina.executa_reset(ctx)
            return None
        if caminho in ("Plugin.Log.LogInfo", "Plugin.Log.LogWarning", "Plugin.Log.LogError"):
            if ultimo == "LogInfo" and ctx.em_diagnostico:
                ctx.logou = True
            return None
        if ultimo == "AvisoDeCorte":
            ctx.avisos.append(argumentos[0] if argumentos else "?")
            return None
        if caminho == "string.IsNullOrEmpty":
            alvo = argumentos[0] if argumentos else None
            return alvo is None or (isinstance(alvo, str) and alvo == "")
        if caminho == "string.StartsWith" or ultimo == "StartsWith":
            if isinstance(receptor, str) and argumentos and isinstance(argumentos[0], str):
                return receptor.startswith(argumentos[0])
            return Simbolico(caminho)
        if ultimo == "Add":
            return True      # `_diagVistos.Add(chave)`: as chaves dos cenarios sao unicas
        return Simbolico(caminho or "?")


class _Programa(object):
    """Parser de STATEMENTS (bloco / if-else / try-catch / return / comando) de um metodo."""

    def __init__(self, texto):
        self.t = texto
        self.i = 0

    def pula(self):
        while self.i < len(self.t) and self.t[self.i] in " \t\r\n":
            self.i += 1

    def vejo(self, palavra):
        self.pula()
        if not self.t.startswith(palavra, self.i):
            return False
        j = self.i + len(palavra)
        return j >= len(self.t) or not (self.t[j].isalnum() or self.t[j] == "_")

    def consome(self, palavra):
        if not self.vejo(palavra):
            raise NaoEntendi("esperava %r em %r" % (palavra, self.t[self.i:self.i + 30]))
        self.i += len(palavra)

    def tudo(self):
        lista = self.statements()
        self.pula()
        if self.i < len(self.t):
            raise NaoEntendi("sobrou codigo nao lido: %r" % self.t[self.i:self.i + 40])
        return lista

    def statements(self):
        lista = []
        while True:
            self.pula()
            if self.i >= len(self.t) or self.t[self.i] == "}":
                return lista
            lista.append(self.statement())

    def bloco(self):
        self.pula()
        if self.i >= len(self.t) or self.t[self.i] != "{":
            raise NaoEntendi("esperava '{' em %r" % self.t[self.i:self.i + 30])
        self.i += 1
        corpo = self.statements()
        self.pula()
        if self.i >= len(self.t) or self.t[self.i] != "}":
            raise NaoEntendi("bloco sem '}' fechando")
        self.i += 1
        return ("bloco", corpo)

    def statement(self):
        if self.vejo("if"):
            return self.se_()
        if self.vejo("try"):
            return self.tente()
        if self.vejo("return"):
            self.consome("return")
            return ("return", self.ate(";").strip())
        for proibido in ("foreach", "while", "for", "switch", "do"):
            if self.vejo(proibido):
                raise NaoEntendi("o orcamento do diagnostico deveria ser linear: achei %r" % proibido)
        self.pula()
        if self.i < len(self.t) and self.t[self.i] == "{":
            return self.bloco()
        return ("cmd", self.ate(";").strip())

    def se_(self):
        self.consome("if")
        condicao = self.entre_parenteses()
        self.pula()
        if self.i < len(self.t) and self.t[self.i] == "{":
            entao = self.bloco()
        else:
            entao = self.statement()
        senao = None
        if self.vejo("else"):
            self.consome("else")
            if self.vejo("if"):
                senao = self.se_()
            elif self.t[self.i] == "{":
                senao = self.bloco()
            else:
                senao = self.statement()
        return ("if", condicao, entao, senao)

    def tente(self):
        self.consome("try")
        corpo_try = self.bloco()
        self.pula()
        if not self.vejo("catch"):
            raise NaoEntendi("try sem catch")
        self.consome("catch")
        self.pula()
        if self.i < len(self.t) and self.t[self.i] == "(":
            self.entre_parenteses()
            self.pula()
        corpo_catch = self.bloco()
        self.pula()
        if self.vejo("finally"):
            self.consome("finally")
            self.bloco()
        return ("try", corpo_try, corpo_catch)

    def entre_parenteses(self):
        self.pula()
        if self.i >= len(self.t) or self.t[self.i] != "(":
            raise NaoEntendi("esperava '(' em %r" % self.t[self.i:self.i + 30])
        i, nivel = self.i + 1, 1
        while i < len(self.t):
            if _e_inicio_de_literal(self.t, i):
                i = _fim_do_literal(self.t, i)
                continue
            c = self.t[i]
            if c == "(":
                nivel += 1
            elif c == ")":
                nivel -= 1
                if nivel == 0:
                    texto = self.t[self.i + 1:i]
                    self.i = i + 1
                    return texto
            i += 1
        raise NaoEntendi("parenteses sem fechar")

    def ate(self, alvo):
        i, nivel = self.i, 0
        while i < len(self.t):
            if _e_inicio_de_literal(self.t, i):
                i = _fim_do_literal(self.t, i)
                continue
            c = self.t[i]
            if c in "([{":
                nivel += 1
            elif c in ")]}":
                if c == "}" and nivel == 0:
                    break
                nivel -= 1
            elif c == alvo and nivel == 0:
                texto = self.t[self.i:i]
                self.i = i + 1
                return texto
            i += 1
        raise NaoEntendi("nao achei %r antes do fim" % alvo)


_TIPOS_DECLARADOS = ("string", "int", "bool", "float", "double", "long", "var",
                     "Material", "TMP_Text", "TMP_FontAsset", "List", "Dictionary")


def _posicao_da_atribuicao(texto):
    """O `=` de uma atribuicao no nivel de fora (ignora `==`, `<=`, `+=`, e o que esta dentro de
    parenteses/colchetes/chaves ou de um literal). -1 = nao ha."""
    nivel, i = 0, 0
    while i < len(texto):
        if _e_inicio_de_literal(texto, i):
            i = _fim_do_literal(texto, i)
            continue
        c = texto[i]
        if c in "([{":
            nivel += 1
        elif c in ")]}":
            nivel -= 1
        elif c == "=" and nivel == 0:
            antes = texto[i - 1] if i else ""
            depois = texto[i + 1] if i + 1 < len(texto) else ""
            if antes not in "=!<>+-*/%&|" and depois != "=" and antes != "":
                return i
        i += 1
    return -1


class MaquinaDoDiagnostico(object):
    """EXECUTA o orcamento do diagnostico do FONTE vivo (FIX-8).

    Monta os statements do CODIGO EFETIVO (`sem_comentarios`) de `OrcamentoDoDiagnosticoPorCena` e
    de `Diagnostico` e os executa, chamada a chamada. Nao ha reconhecimento de forma: o que decide
    o resultado e o caminho que a EXECUCAO toma no fonte que sera compilado.

    `logar(cena, rotulo, tipo)` responde o que o C# responde - a linha SAIU (True) ou nao saiu
    (False) - e `campos` guarda os CONTADORES depois da execucao, no mesmo padrao do fonte.
    """

    def __init__(self, src=None):
        texto = fonte() if src is None else src
        self.erro = None
        self.efetivo = sem_comentarios(texto)
        tetos = tetos_do_diagnostico(texto)
        if tetos is None:
            self.erro = ("nao achei TetoDiagRotina/TetoDiagEfeito/TetoDiagEscape como `const int` no "
                         "fonte: sem os tetos nao ha o que executar")
            return
        self.tetos = dict(zip(NOMES_TETOS, tetos))
        corpo_reset = corpo(self.efetivo, ORCAMENTO)
        corpo_diag = corpo(self.efetivo, DIAG)
        corpo_sweep = corpo(self.efetivo, SWEEP)
        if corpo_reset is None or corpo_diag is None:
            self.erro = ("nao achei `%s` / `%s` no CODIGO EFETIVO do fonte: sem os dois metodos nao "
                         "ha comportamento para executar" % (ORCAMENTO, DIAG))
            return
        if corpo_sweep is None:
            self.erro = "nao achei `%s` no fonte: sem ele nao ha como ler o call site do escape" % SWEEP
            return
        try:
            self.st_reset = _Programa(corpo_reset[1:-1]).tudo()
            self.st_diag = _Programa(corpo_diag[1:-1]).tudo()
        except NaoEntendi as erro:
            self.erro = ("nao consegui INTERPRETAR o orcamento do CODIGO EFETIVO (%s): sem executar "
                         "o fonte a conferencia de comportamento nao vale nada" % erro)
            return
        self.efetivo_sweep = corpo_sweep
        self.tipos = self._tipos_do_enum()
        self.corte_por_contador = self._corte_por_contador()
        self.contadores_do_fonte = sorted(set(list(self.corte_por_contador) +
                                              re.findall(r"(_diag\w+)\s*\+\+", self.efetivo)))
        self.finais_iniciais = self._campos_iniciais(texto)
        self._papeis = None
        self.reiniciar()

    # ------------------------------------------------------------------ montagem
    def _tipos_do_enum(self):
        casamento = re.search(r"enum\s+TipoLinhaDiag\s*\{(.*?)\}", self.efetivo, re.S)
        if not casamento:
            return []
        return [n for n in re.findall(r"[A-Za-z_]\w*", casamento.group(1)) if n != "internal"]

    def _corte_por_contador(self):
        """O teto que GUARDA cada contador, lido das comparacoes do proprio `Diagnostico`."""
        return dict((contador, teto) for contador, teto
                    in re.findall(r"(_diag\w+)\s*>=\s*(TetoDiag\w+)", self.efetivo))

    def _campos_iniciais(self, texto):
        campos = {}
        for casamento in re.finditer(r"private\s+(?:static\s+)?(?:readonly\s+)?(int|bool|float|double|long|string)\s+(_diag\w+)", texto):
            tipo, nome = casamento.group(1), casamento.group(2)
            campos[nome] = None if tipo == "string" else (False if tipo == "bool" else 0)
        return campos

    def reiniciar(self):
        """Zera o ESTADO DA EXECUCAO (nao o orcamento do mod): como se a cena/sessao comecasse."""
        self.campos = dict(self.finais_iniciais)
        self.logadas = []
        self.resets_executados = 0
        self.zeramentos = []
        self.avisos = []
        self.zerou = False

    # ------------------------------------------------------------------ execucao
    def executa_reset(self, contexto):
        """A chamada de `OrcamentoDoDiagnosticoPorCena()` - o corpo do metodo, EXECUTADO."""
        self.resets_executados += 1
        antes = dict((c, self.campos.get(c)) for c in self.contadores_do_fonte)
        sub = Contexto(tetos=self.tetos, variaveis={}, campos=self.campos,
                       cena=contexto.cena, maquina=self)
        sub.em_diagnostico = False
        try:
            self._executa(self.st_reset, sub)
        except _Retorno:
            pass
        zerados = sorted(c for c in antes if antes[c] and not self.campos.get(c))
        if zerados:
            self.zeramentos.append((contexto.cena, tuple(zerados)))
            self.zerou = True

    def logar(self, cena, rotulo, tipo):
        """Uma chamada de `Diagnostico(...)`: True = a linha SAIU; False = foi cortada."""
        contexto = Contexto(tetos=self.tetos, variaveis={}, campos=self.campos,
                            cena=cena, maquina=self)
        contexto.variaveis["situacao"] = rotulo
        contexto.variaveis["tipo"] = tipo
        try:
            self._executa(self.st_diag, contexto)
        except _Retorno:
            pass
        if contexto.logou:
            self.logadas.append(rotulo)
        self.avisos.extend(contexto.avisos)
        return bool(contexto.logou)

    def _executa(self, lista, contexto):
        for stmt in lista:
            self._exec(stmt, contexto)

    def _exec(self, stmt, contexto):
        operacao = stmt[0]
        if operacao == "bloco":
            for filho in stmt[1]:
                self._exec(filho, contexto)
        elif operacao == "if":
            if bool(_Expr(stmt[1], contexto).avaliar()):
                self._exec(stmt[2], contexto)
            elif stmt[3] is not None:
                self._exec(stmt[3], contexto)
        elif operacao == "return":
            raise _Retorno()
        elif operacao == "try":
            try:
                self._exec(stmt[1], contexto)
            except _Retorno:
                raise
            except Exception:
                self._exec(stmt[2], contexto)
        else:
            self._cmd(stmt[1], contexto)

    def _cmd(self, texto, contexto):
        texto = texto.strip()
        if not texto:
            return
        primeiro = texto.split()[0] if texto.split() else ""
        # --- declaracao de variavel local: `string cena;`, `bool foiConvertido = ...;`
        if primeiro in _TIPOS_DECLARADOS or "<" in primeiro.split("=")[0]:
            casamento = re.match(r"^[\w:<>,\.\s]+?\s+([A-Za-z_]\w*)\s*(?:=\s*(.*))?$", texto, re.S)
            if casamento:
                nome = casamento.group(1)
                if casamento.group(2) is None:
                    contexto.grava(nome, None if primeiro == "string" else 0)
                else:
                    contexto.grava(nome, _Expr(casamento.group(2), contexto).avaliar())
                return
        # --- incremento: `_diagLinhasDeEfeito++;`
        casamento = re.match(r"^([A-Za-z_]\w*)\+\+$", texto)
        if casamento:
            nome = casamento.group(1)
            contexto.grava(nome, int(contexto.le(nome) or 0) + 1)
            return
        # --- atribuicao composta: `x += y;`
        casamento = re.match(r"^([A-Za-z_]\w*)\s*\+=\s*(.*)$", texto, re.S)
        if casamento:
            nome = casamento.group(1)
            contexto.grava(nome, int(contexto.le(nome) or 0) + int(_Expr(casamento.group(2), contexto).avaliar() or 0))
            return
        # --- atribuicao simples
        posicao = _posicao_da_atribuicao(texto)
        if posicao > 0:
            destino = texto[:posicao].strip()
            valor = _Expr(texto[posicao + 1:], contexto).avaliar()
            if "." not in destino and "[" not in destino:
                contexto.grava(destino, valor)     # `t.font = x` nao muda o orcamento
            return
        # --- expressao solta (chamadas: o reset, o Log, o AvisoDeCorte)
        _Expr(texto, contexto).avaliar()

    # ------------------------------------------------------------------ medicoes
    def papeis_dos_tipos(self):
        """Para CADA tipo do enum, o CONTADOR que ele incrementa - medido RODANDO o fonte."""
        if self._papeis is None:
            papeis = {}
            for nome in self.tipos:
                self.reiniciar()
                antes = dict(self.campos)
                self.logar("cena-de-medicao", "mede-" + nome, nome)
                papeis[nome] = sorted(c for c in self.contadores_do_fonte
                                      if self.contador(c) > int(antes.get(c) or 0))
            self._papeis = papeis
            self.reiniciar()
        return self._papeis

    def tipo_com_o_teto(self, nome_teto):
        """O tipo de linha cujo contador e guardado por `nome_teto` - ligacao medida, nao digitada."""
        for tipo, contadores in self.papeis_dos_tipos().items():
            for contador in contadores:
                if self.corte_por_contador.get(contador) == nome_teto:
                    return tipo
        return None

    def contador_do_tipo(self, tipo):
        contadores = self.papeis_dos_tipos().get(tipo) or []
        return contadores[0] if contadores else None

    def teto_do_tipo(self, tipo):
        contador = self.contador_do_tipo(tipo)
        nome_teto = self.corte_por_contador.get(contador)
        if nome_teto is None:
            return None
        return self.tetos.get(nome_teto)

    def enche_ate_o_corte(self, tipo, cena, limite):
        """Loga linhas do TIPO ate a primeira que NAO sai (o contador do tipo chegou ao teto)."""
        n = 0
        while n < limite:
            if not self.logar(cena, "enche-%s-%d" % (tipo, n), tipo):
                return n
            n += 1
        return None

    def contador(self, nome):
        return int(self.campos.get(nome) or 0)


def modelo_do_fonte(src=None):
    """A MAQUINA que EXECUTA o orcamento do FONTE vivo (FIX-8). `erro` != None = nao executou."""
    return MaquinaDoDiagnostico(src)


def argumentos_da_chamada(texto, posicao_do_abre):
    """Le a lista de argumentos de uma chamada a partir do '(' (nivel de fora, literais opacos)."""
    i, nivel, argumentos, inicio = posicao_do_abre, 0, [], posicao_do_abre + 1
    while i < len(texto):
        if _e_inicio_de_literal(texto, i):
            i = _fim_do_literal(texto, i)
            continue
        c = texto[i]
        if c in "([{":
            nivel += 1
        elif c in ")]}":
            nivel -= 1
            if c == ")" and nivel == 0:
                pedaco = texto[inicio:i].strip()
                if pedaco:
                    argumentos.append(pedaco)
                return argumentos
        # FIX-8: a virgula que separa ARGUMENTOS fica no nivel de DENTRO da chamada (o '(' que
        # abriu ja somou 1), nao no nivel de fora. Com `nivel == 0` esta funcao NUNCA separava
        # nada (devolvia a chamada inteira como UM argumento), `tipos_dos_call_sites` caia no
        # `len(argumentos) < 2` em TODOS os call sites e a conferencia de comportamento nao
        # achava o call site do escape no fonte vivo - falha de teste, nao do mod.
        elif c == "," and nivel == 1:
            argumentos.append(texto[inicio:i].strip())
            inicio = i + 1
        i += 1
    raise NaoEntendi("chamada sem ')' fechando")


def tipos_dos_call_sites(maquina):
    """O `TipoLinhaDiag.*` que cada call site de `Diagnostico(...)` passa - AVALIANDO a expressao.

    Nao e leitura de token: o argumento do tipo e uma EXPRESSAO do fonte (no caso do texto
    convertido, um ternario sobre `efeitoPresente`) e ela e avaliada nos dois valores da variavel,
    com o MESMO avaliador que executa o orcamento. Devolve {situacao: tipo}.
    """
    texto = maquina.efetivo_sweep
    tipos = {}
    for casamento in re.finditer(r"(?<![\w.])Diagnostico\s*\(", texto):
        abre = texto.index("(", casamento.start())
        try:
            argumentos = argumentos_da_chamada(texto, abre)
        except NaoEntendi:
            continue
        if len(argumentos) < 2:
            continue
        contexto = Contexto(tetos=maquina.tetos, variaveis={"efeitoPresente": True},
                            campos={"efeitoPresente": True}, cena="cena-do-call-site")
        try:
            situacao = _Expr(argumentos[0], contexto).avaliar()
            tipo_com_efeito = _Expr(argumentos[-1], contexto).avaliar()
        except NaoEntendi:
            continue
        contexto2 = Contexto(tetos=maquina.tetos, variaveis={"efeitoPresente": False},
                             campos={"efeitoPresente": False}, cena="cena-do-call-site")
        try:
            tipo_sem_efeito = _Expr(argumentos[-1], contexto2).avaliar()
        except NaoEntendi:
            tipo_sem_efeito = None
        tipos[str(situacao)] = {"tipo_com_efeito": tipo_com_efeito,
                                "tipo_sem_efeito": tipo_sem_efeito,
                                "texto_do_tipo": argumentos[-1]}
    return tipos


LINHA_DO_COMBATE = "NOME DO INIMIGO (material com halo/contorno)"
CENA_A = "cena-A"
CENA_B = "cena-B"
CENA_MISTA = "cena-mista"
PREFIXO_DO_ESCAPE = "PULADO (escape"


def falhas_do_comportamento(src=None):
    """A CONFERENCIA DE COMPORTAMENTO da trava do orcamento (FIX-8). Lista vazia = de pe.

    Executa o CODIGO EFETIVO do fonte e roda os cenarios que decidem o que a conferencia de token
    NUNCA decidiu: se o ZERAMENTO e ALCANCADO a cada troca de cena, se ele acontece ANTES de o
    contador ser usado, e se o pulado pelo escape nao gasta o orcamento de efeito.
    """
    texto = fonte() if src is None else src
    maquina = modelo_do_fonte(texto)
    if maquina.erro:
        return [maquina.erro]

    falhas = []
    if not maquina.tipos:
        return ["nao achei o enum TipoLinhaDiag no CODIGO EFETIVO: sem os tipos nao ha como "
                "executar a classificacao das linhas"]
    papeis = maquina.papeis_dos_tipos()
    tipo_do_efeito = maquina.tipo_com_o_teto("TetoDiagEfeito")
    tipo_do_escape = maquina.tipo_com_o_teto("TetoDiagEscape")
    if tipo_do_efeito is None or tipo_do_escape is None:
        return ["o fonte nao liga os tipos de linha aos tetos: executando o codigo, nenhum tipo "
                "corta por TetoDiagEfeito/TetoDiagEscape (contadores por tipo = %r)" % (papeis,)]

    call_sites = tipos_dos_call_sites(maquina)
    do_escape = [(situacao, dado) for situacao, dado in call_sites.items()
                 if situacao.startswith(PREFIXO_DO_ESCAPE)]
    if not do_escape:
        falhas.append("nao achei o call site do texto PULADO pelo escape em `%s` (avaliando a "
                      "situacao de cada `Diagnostico(...)`): sem ele nao ha como conferir o "
                      "comportamento do pulo" % SWEEP)
        tipo_do_pulo = tipo_do_escape
    else:
        situacao, dado = do_escape[0]
        tipo_do_pulo = dado["tipo_com_efeito"]
        if tipo_do_pulo != tipo_do_escape:
            falhas.append("o texto PULADO pelo escape sai como `TipoLinhaDiag.%s` (avaliado da "
                          "expressao do proprio call site) e nao como `TipoLinhaDiag.%s`, que e o "
                          "tipo guardado por TetoDiagEscape: o pulo volta a disputar o orcamento "
                          "de EFEITO - pular nao e 'de efeito'" % (tipo_do_pulo, tipo_do_escape))

    # ---------------------------------------------------------------- (A) ALCANCE e ORDEM
    # Enche o contador de CADA tipo ate o corte (o teto), troca de cena e pede UMA linha do MESMO
    # tipo. Ela TEM de sair: o zeramento foi ALCANCADO na troca de cena E veio ANTES do uso do
    # contador. E aqui que caem o `if (false)`, o guarda sempre verdadeiro e o reset depois do uso.
    for tipo in maquina.tipos:
        maquina.reiniciar()
        teto = maquina.teto_do_tipo(tipo)
        limite = (teto if teto else 0) + 5
        cortou = maquina.enche_ate_o_corte(tipo, CENA_A, limite)
        if cortou is None:
            falhas.append("o contador do tipo `%s` NAO corta (enchi %d linhas em `%s`): o teto do "
                          "tipo nao esta ligado ao contador que ele incrementa" % (tipo, limite, CENA_A))
            continue
        saiu = maquina.logar(CENA_B, "linha-da-cena-nova-%s" % tipo, tipo)
        if not saiu:
            falhas.append("o ZERAMENTO NAO e ALCANCADO a cada troca de cena (ou nao acontece ANTES "
                          "do contador ser usado): executando o CODIGO EFETIVO do fonte, o contador "
                          "do tipo `%s` foi cheio ate o CORTE na cena '%s' (%d linha(s), teto=%s) e "
                          "UMA linha do MESMO tipo na cena '%s' NAO saiu - o orcamento voltou a ser "
                          "o da SESSAO. Nao e leitura de token: o `if (false)` em volta do "
                          "zeramento, o guarda que ficou sempre verdadeiro por a cena ser gravada "
                          "antes dele e a chamada do reset depois do uso caem TODOS aqui"
                          % (tipo, CENA_A, cortou, teto, CENA_B))
    if falhas:
        return falhas

    # ---------------------------------------------------------------- (B) A SEQUENCIA REAL
    cenas = pulados_da_sessao_do_dono()
    if not cenas:
        falhas.append("a sequencia real de pulados do dono nao esta no log versionado (%s): a "
                      "conferencia de comportamento ficou sem escala" % LOG_VARREDURA)
        return falhas
    maquina.reiniciar()
    for i, n in enumerate(cenas):
        for j in range(n):
            maquina.logar("cena-%d" % i, "pulado-%d-%d" % (i, j), tipo_do_pulo)
    ultima = "cena-%d" % (len(cenas) - 1)
    if not maquina.logar(ultima, LINHA_DO_COMBATE, tipo_do_pulo):
        falhas.append("a linha de COMBATE nao sai com a sequencia REAL de pulados do dono (%d "
                      "pulado(s) em %d cena(s), %d corte(s)): o orcamento do diagnostico volta a "
                      "esconder exatamente a linha que o dono liga `LogDiagnosticoEstilo` para ler"
                      % (sum(cenas), len(cenas), len(maquina.avisos)))

    # ---------------------------------------------------------------- (C) O PULO NAO E EFEITO
    contador_efeito = maquina.contador_do_tipo(tipo_do_efeito)
    if contador_efeito and maquina.contador(contador_efeito) > 0:
        falhas.append("o pulado pelo escape consumiu o orcamento de EFEITO (%s = %d depois de uma "
                      "sessao SO de pulos): pular nao e 'de efeito' - um pulado nao transportou "
                      "efeito nenhum" % (contador_efeito, maquina.contador(contador_efeito)))

    # ---------------------------------------------------------------- (D) A CENA MISTA
    # O cenario que prova que o corte do PULADO nao esta preso ao teto de EFEITO. FALHA ALTA: se a
    # medicao nao exercita o caso, isso NAO pode virar silencio (achado 3 da FIX-7R).
    medicao = textos_com_efeito_no_boot() or {}
    com_efeito = medicao.get("com_efeito_no_material")
    teto_efeito = maquina.tetos.get("TetoDiagEfeito", 0)
    if not com_efeito:
        falhas.append("FALHA ALTA: a MEDICAO dos textos com efeito no material nao esta em %s - "
                      "sem ela o cenario MISTO (efeito alem do teto + pulos, na mesma cena) nao "
                      "tem escala, e nao rodar o cenario nao pode passar em silencio" % FIXTURE_EFEITO)
    elif com_efeito <= teto_efeito:
        falhas.append("FALHA ALTA: a MEDICAO dos textos com efeito no material (%d) NAO passa o "
                      "teto de efeito (%d) - o cenario MISTO deixou de exercitar o caso que ele "
                      "existe para provar, e um cenario que nao roda nao pode virar silencio "
                      "(achado 3 da FIX-7R)" % (com_efeito, teto_efeito))
    efeito_na_cena = max(int(com_efeito or 0), int(teto_efeito) + 1)
    maquina.reiniciar()
    for i in range(efeito_na_cena):
        maquina.logar(CENA_MISTA, "efeito-%d" % i, tipo_do_efeito)
    for j in range(max(cenas)):
        maquina.logar(CENA_MISTA, "pulado-%d" % j, tipo_do_pulo)
    if not maquina.logar(CENA_MISTA, LINHA_DO_COMBATE, tipo_do_pulo):
        falhas.append("numa cena MISTA (%d textos de EFEITO - o teto de efeito JA esgotado - + os "
                      "%d pulos medidos, na MESMA cena) a linha de COMBATE nao sai: o corte do "
                      "texto PULADO pelo escape esta preso ao orcamento de EFEITO, que a propria "
                      "varredura esgota - o pulo tem de ter o teto dele"
                      % (efeito_na_cena, max(cenas)))
    return falhas


def fonte_com_a_cena_fixa_no_comentario(src=None):
    """VARIANTE (A) da REV-56: a leitura da cena vira COMENTARIO e `cena` passa a ser FIXA.

    Todos os TOKENS sobrevivem (`GetActiveScene` continua no texto, `if (cena == _diagCena)` intacto).
    Comportamento: `_diagCena` e sempre a mesma string, entao o reset roda so na PRIMEIRA cena.
    """
    texto = fonte() if src is None else src
    alvo = "                cena = UnityEngine.SceneManagement.SceneManager.GetActiveScene().name;"
    troca = ("                // cena = UnityEngine.SceneManagement.SceneManager.GetActiveScene().name;\n"
             "                cena = \"GameSceneNew\";")
    if alvo in texto:
        texto = texto.replace(alvo, troca, 1)
    return texto


def fonte_com_o_escape_incrementando_o_efeito(src=None):
    """VARIANTE (B) da REV-56: o ramo do ESCAPE volta a incrementar o contador de EFEITO.

    O corte do escape continua no teto proprio e o call site continua passando `TipoLinhaDiag.Escape`.
    Comportamento: o pulo passa a gastar o orcamento de efeito (o defeito da BF-2R).
    """
    texto = fonte() if src is None else src
    alvo = "                _diagLinhasDeEscape++;\n"
    if alvo in texto:
        texto = texto.replace(alvo, alvo + "                _diagLinhasDeEfeito++;\n", 1)
    return texto


def fonte_com_o_corte_do_escape_no_teto_de_efeito(src=None):
    """VARIANTE (C) da REV-56: o CORTE do escape passa a depender TAMBEM do TETO DE EFEITO.

    O ramo continua sendo o do escape, o contador do escape continua sendo incrementado e o guarda
    proprio (`_diagLinhasDeEscape >= TetoDiagEscape`) continua escrito - ao lado dele entra
    `|| _diagLinhasDeEfeito >= TetoDiagEfeito`. Os tokens presentes: e por isso que a conferencia
    tem de EXECUTAR. Comportamento: numa cena MISTA (efeito alem do teto + pulos) o orcamento de
    efeito, ja esgotado, corta tambem o texto pulado pelo escape - inclusive a linha de combate.
    """
    texto = fonte() if src is None else src
    alvo = "                if (_diagLinhasDeEscape >= TetoDiagEscape)"
    troca = ("                if (_diagLinhasDeEscape >= TetoDiagEscape"
             " || _diagLinhasDeEfeito >= TetoDiagEfeito)")
    if alvo in texto:
        texto = texto.replace(alvo, troca, 1)
    return texto
