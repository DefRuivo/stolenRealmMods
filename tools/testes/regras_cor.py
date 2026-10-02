#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_cor.py — a biblioteca da familia das CORES (COR-2), ao lado do `arcabouco.py`.

Duas coisas moram aqui:

1. AS REGRAS DE COR lidas da LEITURA DATADA do jogo (fixture `cores-do-jogo.json`): o
   espelho do `EhAzul` do `LocalizePatch.cs` e a SANIDADE do nivel 2 — a cor da explicacao
   tem de ser o tom "special" do jogo e NAO pode ser azul (senao os niveis 2 e 3 colapsam,
   que foi o achado do COR-1). A procedencia da fixture esta dentro dela: e a leitura do
   PREFAB do jogo (01/10) com o CONTROLE que valida o leitor (o `coldColor` do asset tem de
   dar exatamente o `#00D7FF` que o log de runtime imprime).

2. A BANCADA DA TRAVA (o furo do COR-1): a nota fundida que a primeira versao ignorava e o
   plantio da troca de cor numa COPIA do `LocalizePatch.cs`, para a isca
   (`contra-prova/cp_cor_nota_fundida_isca.py`) provar que a trava de hoje reprova.

NAO e um teste: nao tem META nem corpo(). Quem le sao os testes da familia.
"""
import os
import re
import subprocess
import sys
import tempfile

import arcabouco as arc
import recorte as rec

sys.path.insert(0, os.path.join(arc.raiz_do_repo(), "tools"))
import tabelas as tab  # noqa: E402  o parser UNICO das tabelas do LocalizePatch.cs (PARSER-1)

BS = chr(92)

CASO = "cores-do-jogo"

# A nota FUNDIDA que a trava do COR-1 ignorava: ela e uma das 12 notas de SHRINE e vive no
# formato de UMA quebra de linha (`\n<color=#...>`), que a primeira versao nao olhava.
NOTA_FUNDIDA_DE_SHRINE = "Recover [0]% of maximum mana each turn."
HEX_PLANTADO = "#C0FFEE"
MOTIVO_DA_TRAVA = "cor que nao e a do nivel 2"

# FIX-4 — O FURO DO COMENTARIO DE BLOCO (achado da REV-55). O COR-2 fez o parser da trava pular
# o comentario de LINHA dentro do `{` (o formato 'chave em linha propria', ex. `Shapeshift
# Dragonkin`). O comentario de BLOCO (`/* ... */`) antes da chave NAO era pulado: a entrada
# sumia da varredura (25 -> 24 blocos de nota) e a troca de cor nela passava em silencio. A
# entrada alvo e a do `Undead Wizard`, que ja vive no formato 'chave em linha propria' e carrega
# o marcador do nivel 2.
ENTRADA_DO_BLOCO = '"Raise a Undead Wizard to fight by your side.",'
COMENTARIO_DE_BLOCO = ("/* FIX-4: comentario de BLOCO dentro da chave (sem `//`) - esta entrada "
                       "NAO pode ficar invisivel para a trava */")
NL = chr(10)

CHECK_NOTAS = os.path.join(arc.raiz_do_repo(), "tools", "check_notas_redundantes.py")
FONTE_MOD = os.path.join(arc.raiz_do_repo(), "BetterTooltips", "Patches", "LocalizePatch.cs")

# ===================================================== BANCADA-1: A QUEBRA DO JOGO ====
# A LEITURA do caminho de MONTAGEM da tooltip (fixture versionada `formato-notas.entrada.json`):
# os trechos LITERAIS do `ShowSkillTooltip`, do `ShowGroundEffectTooltip` e do
# `ShowActionStatusTooltip`, com o numero de quebras que o JOGO escreve em cada ponto. E a
# procedencia e o controle estao dentro dela.
CASO_DO_FORMATO = "formato-notas"

# A REGRA DA BANCADA (o numero que o `monta_a_descricao` usa). Ela tem de ser IGUAL ao que a
# leitura da fixture conta — quem confere e `testes/puros/t_formato_notas.py`.
#
# BANCADA-1 (01/10) — A CORRECAO. A bancada montava os custos com UMA quebra
# (`texto.rstrip("\n") + "\n" + custo`), e o `ShowSkillTooltip` escreve DUAS: a l.1470 acrescenta
# uma quebra ao original (`original += "\n"`) e a l.1536 concatena `original + "\n" + "AP Cost: ..."`.
# Com UMA quebra a bancada NAO reproduzia o jogo (nao existia a linha em branco que o jogador ve
# entre a descricao e o `AP Cost`) — e, pior, o checador de formato acusava o texto DO JOGO de
# "linha em branco orfa". A regra que o RV-17 travou estava errada; o codigo do mod, nao (o
# `InicioDoSeparador` consumir as DUAS quebras e o que preserva a linha em branco do jogo).
QUEBRAS_ANTES_DO_CUSTO_DA_BANCADA = 2

_SEP = re.compile(r"[\s,]+")


def hex_para_rgb(cor):
    """'#RRGGBB' -> tupla de floats 0..1, a mesma faixa que o `Color` do Unity guarda."""
    c = cor.lstrip("#")
    return tuple(int(c[i:i + 2], 16) / 255.0 for i in (0, 2, 4))


def eh_azul(cor):
    """ESPELHO do `EhAzul` do `LocalizePatch.cs` (a mesma conta, nos mesmos floats 0..1):

        float excesso = (c.b - c.r) + (c.b - c.g);
        return c.b >= c.r && c.b >= c.g && c.b > 0.35f && excesso > 0.05f;

    E a sanidade do NIVEL 3: se o build mudar o campo para um tom bege, a linha de auras
    nao vira uma copia silenciosa das notas.
    """
    r, g, b = hex_para_rgb(cor)
    excesso = (b - r) + (b - g)
    return b >= r and b >= g and b > 0.35 and excesso > 0.05


def eh_tom_de_explicacao(cor):
    """SANIDADE do NIVEL 2 (o que faltava — so o nivel 3 tinha teste): a cor da explicacao
    e um tom QUENTE/NEUTRO (o bege "special" do jogo), nunca um azul. Se o campo virar azul,
    o nivel 2 e o nivel 3 ficam indistinguiveis e a convencao morre em silencio."""
    return not eh_azul(cor)


def distancia_por_canal(a, b):
    """Maior diferenca (0..255) entre dois hex, canal a canal. Serve para aceitar a diferenca
    entre o marcador e o campo: o marcador foi medido por PIXEL num print (29/09) e o campo foi
    lido do prefab (01/10) — sao metodos diferentes, a igualdade exata nao se exige."""
    ca, cb = a.lstrip("#"), b.lstrip("#")
    return max(abs(int(ca[i:i + 2], 16) - int(cb[i:i + 2], 16)) for i in (0, 2, 4))


# --------------------------------------------------------------------------- fixture ---

def leitura_datada():
    """A leitura datada do jogo (fixture versionada). Devolve o dict inteiro."""
    return arc.ler_json(CASO, "entrada")


# ------------------------------------------------- leitura do FORMATO (BANCADA-1) ---
# A fixture `formato-notas.entrada.json` e a LEITURA do caminho de montagem da tooltip: os trechos
# literais do decompilado do `Tooltip` e as quebras que o jogo escreve em cada ponto. Ela NAO e
# decoracao: cada `trecho` tem de aparecer LITERALMENTE no decompilado (o teste procura os arquivos
# quando existem nesta maquina) e o numero de quebras sai da contagem dos escapes do proprio trecho.

def leitura_do_formato():
    """A leitura DATADA do caminho de montagem da tooltip (fixture versionada)."""
    return arc.ler_json(CASO_DO_FORMATO, "entrada")


def caminho_da_tooltip(nome, leitura=None):
    """O caminho `skill` / `ground_effect` / `status` da leitura do formato.

    `leitura` permite ler uma leitura PLANTADA (o controle e a contra-prova exercitam estas funcoes
    sobre uma copia mutada); `None` = a fixture versionada.
    """
    caminhos = (leitura or leitura_do_formato())["caminhos"]
    if nome not in caminhos:
        raise arc.Falhou("a leitura do formato nao tem o caminho %r (tem: %s)"
                         % (nome, ", ".join(sorted(caminhos))))
    return caminhos[nome]


def quebras_antes_do_custo_do_jogo():
    """Quantas quebras o `ShowSkillTooltip` escreve entre a descricao e a PRIMEIRA linha de custo.

    O numero NAO esta digitado na fixture: ele e a SOMA do campo `quebras` das linhas do caminho
    `skill`, e cada `quebras` saiu da contagem dos escapes `\\n` do `ramo_que_roda` (o ramo do
    ternario que EXECUTA) — que por sua vez tem de estar contido no `trecho` literal do decompilado.
    """
    linhas = caminho_da_tooltip("skill")["linhas"]
    if len(linhas) < 2:
        raise arc.Falhou("a leitura do formato tem de trazer as DUAS linhas do caminho da skill "
                         "(l.1470 e l.1536); trouxe %d" % len(linhas))
    total = sum(l["quebras"] for l in linhas)
    if total < 2:
        raise arc.Falhou("a leitura do formato contradiz o decompilado: o `AP Cost` da skill nao "
                         "pode ser precedido de menos de DUAS quebras (achei %d)" % total)
    return total


def tem_ap_cost_no_texto():
    """Se o caminho do GROUND EFFECT tem bloco de custo no texto (NAO tem: nao ha `AP Cost`)."""
    return bool(caminho_da_tooltip("ground_effect")["custo_no_texto"])


def custos_do_jogo(nome="skill", leitura=None):
    """As linhas de custo/metadados que o jogo escreve nesse caminho, como aparecem no texto."""
    return tuple(caminho_da_tooltip(nome, leitura)["custo_no_texto"])


# ==================================================== BANCADA-2: A PRIMEIRA LINHA DE CUSTO ====
# O JOGO escreve a LINHA EM BRANCO dele antes da PRIMEIRA linha de custo de cada caminho, E SO
# DELA: o `AP Cost` da skill (l.1470 + l.1536) e o `Duration Type` do status (l.1013). As linhas
# SEGUINTES do bloco de custo (`Range`, `Blast Radius`, `Mana Cost`, `Cooldown` — l.1558/1561/
# 1565/1572) vem com UMA quebra cada: NAO tem linha em branco antes. O checador do BANCADA-1
# liberava o bloco INTEIRO e por isso ACEITAVA uma forma que o jogo NUNCA escreve
# (`descricao \n\n AP Cost \n\n Range`) — foi um afrouxamento que o conserto trouxe de brinde.

def _trechos_do_grupo(nome, grupo, leitura=None):
    """Os `trecho`s literais do grupo da leitura do formato: `linhas` (os pontos onde o jogo escreve
    a linha em branco) ou `linhas_seguintes` (as linhas que vem com UMA quebra cada)."""
    return tuple(l["trecho"] for l in caminho_da_tooltip(nome, leitura).get(grupo, ()))


def primeiras_linhas_de_custo(nome="skill", leitura=None):
    """As linhas de CUSTO/METADADOS que o JOGO precede de linha em branco — a PRIMEIRA de cada
    caminho (o `AP Cost` da skill, o `Duration Type` do status), e nenhuma outra.

    A classificacao NAO e digitada a mao: sai do TRECHO VERIFICADO — so entra a entrada de
    `custo_no_texto` que aparece LITERALMENTE no `trecho` de uma linha do grupo `linhas` (os pontos
    onde o jogo escreve as duas quebras, conferidos contra o decompilado pelo
    `regras_formato.controle_da_leitura_do_formato`). A linha que mora nas `linhas_seguintes` NAO
    entra — logo a linha em branco antes dela fica sem permissao no checador (BANCADA-2).
    """
    trechos = _trechos_do_grupo(nome, "linhas", leitura)
    return tuple(c for c in custos_do_jogo(nome, leitura) if any(c in t for t in trechos))


def controle_das_linhas_de_custo(leitura=None):
    """O CONTROLE da lista `custo_no_texto` (BANCADA-2): ela e escrita A MAO na fixture e, sem
    controle, envelheceria em silencio — uma linha que o jogo NAO escreve passaria a ser aceita, ou
    uma que ele escreve sumiria e o checador deixaria de ver o defeito.

    Aqui CADA entrada tem de aparecer LITERALMENTE no `trecho` de ALGUMA linha do caminho (as
    `linhas` ou as `linhas_seguintes`) — entrada digitada a mao REPROVA. E, se o caminho TEM custo, a
    PRIMEIRA linha de custo (a unica que vem depois da linha em branco do jogo) tem de existir: sem
    ela o restringimento do BANCADA-2 perde a base.

    Devolve quantas entradas foram conferidas (o teste exige um minimo — controle que nao confere
    nada e decoracao).
    """
    leitura = leitura or leitura_do_formato()
    conferidas = 0
    for nome in sorted(leitura["caminhos"]):
        entradas = custos_do_jogo(nome, leitura)
        trechos = (_trechos_do_grupo(nome, "linhas", leitura)
                   + _trechos_do_grupo(nome, "linhas_seguintes", leitura))
        for custo in entradas:
            arc.exigir(any(custo in t for t in trechos),
                       "a lista `custo_no_texto` do caminho %r traz %r, que NAO aparece no `trecho` "
                       "literal de nenhuma linha — o jogo NAO escreve essa linha (entrada digitada a "
                       "mao?)" % (nome, custo))
            conferidas += 1
        if entradas:
            arc.exigir(primeiras_linhas_de_custo(nome, leitura),
                       "o caminho %r tem `custo_no_texto` mas nenhuma linha de custo veio do grupo "
                       "`linhas` (os pontos da linha em branco do jogo): o restringimento do "
                       "BANCADA-2 perdeu a base" % nome)
    return conferidas


def _com_cerquilha(hex_):
    """O hex de cor SEMPRE com `#` — a bancada monta o bloco como `"<color=" + hex + ">"`, e o C#
    escreve `"<color=#" + hex`. Sem esta guarda, um hex sem `#` (lido de outro lugar) montaria
    `<color=CBB396>` — um bloco que o jogo nunca escreve — e NENHUMA busca acharia, em silencio."""
    if not isinstance(hex_, str) or not hex_.startswith("#") or len(hex_) != 7:
        raise arc.Falhou("hex de cor invalido para `\"<color=\" + hex`: %r (tem de ser '#RRGGBB')"
                         % (hex_,))
    return hex_


def cor_do_campo(nome, componente=0):
    """Hex de um campo de cor do componente `Tooltip` do jogo, pela leitura versionada."""
    leitura = leitura_datada()
    componente_tooltip = leitura["tooltip"]["componentes"][componente]
    return _com_cerquilha(componente_tooltip["cores"][nome]["hex"])


def cor_da_hud(nome):
    """Hex de uma cor do `GUIManager` (a paleta da HUD), pela leitura versionada."""
    return _com_cerquilha(leitura_datada()["guimanager"]["cores"][nome])


def log_de_runtime():
    """As linhas do log de runtime (sessao COM a DLL do perfil) que a fixture guarda como
    CONTROLE da leitura: e por elas que se sabe qual cor o jogo leu de verdade."""
    return leitura_datada()["log_de_runtime"]


# ---------------------------------------------------------------------------- fonte ---

def fonte_do_mod():
    with open(FONTE_MOD, encoding="utf-8") as fh:
        return fh.read()


def entrada_marcador():
    """O marcador do nivel 2 COMO O CODIGO o declara (`MarcadorCorDeExplicacao = "C8B090"`).

    Sai do fonte, nao de um literal do teste: se alguem trocar o marcador no codigo, os testes
    da familia acompanham — e a convencao (docs/TEXTO-TOOLTIPS.md §2) e quem diz qual e o certo.
    """
    m = re.search(r'MarcadorCorDeExplicacao\s*=\s*"([0-9A-Fa-f]{6})"', fonte_do_mod())
    if not m:
        raise arc.Falhou("nao achei `MarcadorCorDeExplicacao = \"RRGGBB\"` no LocalizePatch.cs")
    return _com_cerquilha("#" + m.group(1).upper())


def marcadores_do_nivel_3():
    """Os MARCADORES DE TEXTO do nivel 3, lidos dos fontes dos patches — os MESMOS dois que o
    `EhBlocoDoNivel3` do C# compara: a linha de auras ativas (`ShrineAuraPatch.
    MarcadorLinhaDeAuras`) e o bloco de sinergia status x skill (`StatusSkillSynergyPatch.
    Marcador`). O nivel 3 nunca e reconhecido por cor: a cor dele e da paleta da HUD e pode
    colapsar no marcador de reserva (ver docs/TEXTO-TOOLTIPS.md §8.3)."""
    achados = []
    for nome_arquivo in ("ShrineAuraPatch.cs", "StatusSkillSynergyPatch.cs"):
        caminho = os.path.join(os.path.dirname(FONTE_MOD), nome_arquivo)
        with open(caminho, encoding="utf-8") as fh:
            texto = fh.read()
        m = re.search(r'internal\s+const\s+string\s+Marcador(?:LinhaDeAuras)?\s*=\s*"([^"]+)"', texto)
        if not m:
            raise arc.Falhou("nao achei o marcador do nivel 3 em %s" % nome_arquivo)
        achados.append(m.group(1))
    return achados


def eh_bloco_do_nivel_3(texto):
    """ESPELHO do `EhBlocoDoNivel3` do `LocalizePatch.cs`: o bloco pertence ao nivel 3 quando ABRE
    com um dos marcadores de texto proprios dele — nunca pela cor (a cor dele pode ser, no
    colapso, o mesmo marcador do nivel 2)."""
    return any(texto.startswith(m) for m in marcadores_do_nivel_3())


def texto_da_tabela(nome):
    """Bloco `nome = new Dictionary ... }` do `LocalizePatch.cs`, com a posicao inicial.

    O fim do bloco e achado pelo primeiro `private static` no nivel de indentacao da classe
    (as tabelas sao seguidas de metodo), sem depender do parser da trava.
    """
    fonte = fonte_do_mod()
    k = fonte.index("%s = new Dictionary" % nome)
    k = fonte.index("{", k)
    corpo = fonte[k:]
    m = re.search(r"\n {8}private static", corpo)
    return (corpo[:m.start()] if m else corpo), k


def notas_fundidas_com_cor():
    """As entradas de `TextFixes` cujo valor tem cor `<color=#RRGGBB>`, em QUALQUER formato.

    Medida INDEPENDENTE do parser do `check_notas_redundantes.py` (regex sobre o bloco da
    tabela): e esta medida que prova que existem notas no formato de UMA quebra — o furo.
    Devolve uma lista de (quantas_quebras_antes_da_cor, hex, trecho_do_valor).
    """
    bloco, _ = texto_da_tabela("TextFixes")
    achados = []
    for m in re.finditer(r'<color=#([0-9A-Fa-f]{6})>', bloco):
        antes4 = bloco[max(0, m.start() - 4):m.start()]
        antes2 = bloco[max(0, m.start() - 2):m.start()]
        if antes4 == BS + "n" + BS + "n":
            quebras = 2
        elif antes2 == BS + "n":
            quebras = 1
        else:
            quebras = 0
        achados.append((quebras, "#" + m.group(1).upper(), rec.bloco_que_contem(bloco, m.start())))
    return achados


# ---------------------------------------------------------------------------- trava ---

def planta_troca_na_nota_fundida(dir_tmp, alvo=NOTA_FUNDIDA_DE_SHRINE, hex_novo=HEX_PLANTADO):
    """Copia o `LocalizePatch.cs` e troca a COR da nota fundida `alvo` (a chave fica intacta).

    Devolve (caminho da copia, trecho ORIGINAL da chave ate a cor, texto original inteiro) —
    o trecho original e o que prova que o alvo e uma nota fundida de shrine no formato de UMA
    quebra; a copia e o que a trava le.
    """
    fonte = fonte_do_mod()
    i = fonte.index(alvo)
    j = fonte.index("#C8B090", i)
    trocado = fonte[:j] + hex_novo + fonte[j + len("#C8B090"):]
    caminho = os.path.join(dir_tmp, "LocalizePatch.cs")
    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write(trocado)
    # O trecho original devolvido e a ENTRADA INTEIRA da tabela (do `{` ao `}` que casa), por
    # CASAMENTO DE CHAVES — nunca uma janela de 120/160 caracteres. A janela media DISTANCIA e
    # reprovava por reformatacao (um `Shrine Effect Bonus` mais adiante ficava fora dela).
    return caminho, rec.bloco_que_contem(fonte, j), fonte


def roda_a_trava_notas(caminho):
    """Roda `tools/check_notas_redundantes.py --fonte <caminho>`; devolve (exit, saida)."""
    proc = subprocess.run(
        [sys.executable, CHECK_NOTAS, "--fonte", caminho],
        cwd=arc.raiz_do_repo(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        universal_newlines=True, timeout=300)
    return proc.returncode, proc.stdout or ""


def corpo_da_isca_da_trava(esperado):
    """O corpo compartilhado pelas duas metades da contra-prova da trava de cor.

    `esperado` e 0 na ISCA (a trava antiga DEIXA PASSAR) e 1 na metade sem o defeito (a trava
    PEGA). Como a trava de hoje PEGA, a isca reprova e a metade ok passa.
    """
    with tempfile.TemporaryDirectory(prefix="cor2-nota-fundida-") as tmp:
        caminho, trecho, _fonte = planta_troca_na_nota_fundida(tmp)

        # A isca so vale se o defeito caiu no LUGAR certo: na COPIA a cor plantada esta no lugar
        # da nota, e no ORIGINAL essa nota e uma nota fundida de SHRINE, no formato de UMA quebra
        # (o formato que o COR-1 nao olhava).
        with open(caminho, encoding="utf-8") as fh:
            copia = fh.read()
        arc.exigir(copia.count(HEX_PLANTADO) == 1,
                   "a copia tinha de ter exatamente UMA ocorrencia da cor plantada (%s): %d"
                   % (HEX_PLANTADO, copia.count(HEX_PLANTADO)))
        arc.exigir((BS + "n<color=#C8B090") in trecho,
                   "a nota alvo tem de estar no formato de UMA quebra (o furo do COR-1): %r"
                   % trecho[-90:])
        arc.exigir((BS + "n" + BS + "n<color=#C8B090") not in trecho,
                   "a nota alvo nao pode estar no formato de DUAS quebras: %r" % trecho[-90:])
        arc.exigir("Shrine Effect Bonus" in trecho,
                   "a nota fundida alvo tem de ser uma das de SHRINE: %r" % trecho[-120:])

        codigo, saida = roda_a_trava_notas(caminho)

        arc.exigir(codigo == esperado,
                   "%s a troca de cor numa nota FUNDIDA de SHRINE (formato de UMA quebra): "
                   "plantei %s em '%s' e a trava saiu com exit %d; saida: %s"
                   % ("DEIXA PASSAR" if esperado == 0 else "PEGOU", HEX_PLANTADO,
                      NOTA_FUNDIDA_DE_SHRINE, codigo, saida.strip()[-260:]))
        arc.exigir(HEX_PLANTADO in saida and MOTIVO_DA_TRAVA in saida,
                   "a trava reagiu, mas NAO pela COR da nota fundida (%s) — saida: %s"
                   % (HEX_PLANTADO, saida.strip()[-260:]))
    return "a trava %s a troca de cor na nota fundida de SHRINE (%s -> %s), no formato de UMA quebra" % (
        "pegou" if esperado else "deixou passar", "#C8B090", HEX_PLANTADO)


# ------------------------------------------------- FIX-4: comentario de BLOCO na chave ---

def planta_troca_na_entrada_com_bloco(dir_tmp, alvo=ENTRADA_DO_BLOCO, hex_novo=HEX_PLANTADO):
    """Copia o `LocalizePatch.cs`, insere um COMENTARIO DE BLOCO (`/* ... */`) ANTES da chave
    `alvo` e troca a COR dessa entrada (a chave fica intacta).

    O comentario de bloco e o formato que o parser da trava (COR-2) NAO pulava: sem o conserto
    do FIX-4 a entrada sumia da varredura e a troca nao reprovava. Devolve (caminho da copia,
    texto original inteiro).
    """
    fonte = fonte_do_mod()
    arc.exigir(fonte.count(alvo) == 1,
               "a chave alvo do comentario de bloco tem de ser unica no fonte: achei %d"
               % fonte.count(alvo))
    com_comentario = fonte.replace(
        alvo, '                ' + COMENTARIO_DE_BLOCO + NL + '                ' + alvo)
    i = com_comentario.index(alvo)
    j = com_comentario.index('#C8B090', i)
    trocado = com_comentario[:j] + hex_novo + com_comentario[j + len('#C8B090'):]
    caminho = os.path.join(dir_tmp, 'LocalizePatch.cs')
    with open(caminho, 'w', encoding='utf-8') as fh:
        fh.write(trocado)
    return caminho, fonte


def corpo_da_isca_do_comentario_de_bloco(esperado):
    """O corpo compartilhado pelas duas metades da contra-prova do COMENTARIO DE BLOCO (FIX-4).

    `esperado` e 0 na ISCA (a trava ANTIGA deixa passar - a entrada estava invisivel) e 1 na
    metade sem o defeito (a trava PEGA). Como a trava de hoje PEGA, a isca reprova e a metade
    ok passa.
    """
    with tempfile.TemporaryDirectory(prefix="cor-fix4-bloco-") as tmp:
        caminho, _fonte = planta_troca_na_entrada_com_bloco(tmp)
        with open(caminho, encoding="utf-8") as fh:
            copia = fh.read()

        # A isca so vale se o defeito caiu no LUGAR certo: o comentario de BLOCO tem de vir
        # imediatamente ANTES da chave (e nao dentro do valor), e a cor plantada tem de aparecer
        # UMA vez.
        arc.exigir(copia.count(HEX_PLANTADO) == 1,
                   "a copia tinha de ter exatamente UMA ocorrencia da cor plantada (%s): %d"
                   % (HEX_PLANTADO, copia.count(HEX_PLANTADO)))
        arc.exigir(COMENTARIO_DE_BLOCO + NL + '                ' + ENTRADA_DO_BLOCO in copia,
                   "o comentario de BLOCO tem de vir imediatamente antes da chave alvo")

        codigo, saida = roda_a_trava_notas(caminho)

        arc.exigir(codigo == esperado,
                   "%s a troca de cor numa entrada com COMENTARIO DE BLOCO dentro da chave "
                   "(formato `{ /* ... */ \"chave\" }`): plantei %s em %s e a trava saiu com "
                   "exit %d; saida: %s"
                   % ("DEIXA PASSAR" if esperado == 0 else "PEGOU", HEX_PLANTADO,
                      ENTRADA_DO_BLOCO, codigo, saida.strip()[-260:]))
        arc.exigir(HEX_PLANTADO in saida and MOTIVO_DA_TRAVA in saida,
                   "a trava reagiu, mas NAO pela COR da entrada com comentario de bloco (%s) — "
                   "saida: %s" % (HEX_PLANTADO, saida.strip()[-260:]))
    return ("a trava %s a troca de cor na entrada com COMENTARIO DE BLOCO dentro da chave "
            "(%s -> %s), no formato 'chave em linha propria' com `/* ... */`"
            % ("pegou" if esperado else "deixou passar", "#C8B090", HEX_PLANTADO))


# ======================================================= COR-3: A POSICAO =====
#
# O COR-2 fez a cor do nivel 2 chegar ao bloco. Achado do COR-3: a cor declarada do nivel 2
# (`Tooltip.specialDescColor`, #CBB396) e o MESMO literal que o motor escreve nos valores
# dinamicos das skills — `ApplyDescriptionExpressions` (l.2327 do decompilado) grava
# `<color=#CBB396>VALOR</color>` para o `[N]`, e `GetDamageString` (l.2276) grava
# `<size=..><color=#CBB396>NN</color></size>` para o `*N` (o dano). A partir do momento em que a
# troca do marcador passou a ACONTECER, "o primeiro bloco da cor do nivel 2" deixou de ser a
# NOSSA nota e passou a ser o VALOR DE DANO da skill: era ele que o `CorEOrdemDoTooltip` movia
# para o fundo do tooltip.
#
# As funcoes abaixo sao o ESPELHO dessa etapa do `LocalizePatch.cs` (mesma convencao do
# `eh_azul`, que ja era o espelho do teste de azul). Quem as le sao os testes da familia.

COR_DO_VALOR_DO_MOTOR = "#CBB396"      # literal do motor (43 usos no Assembly)
ABRE_COR = "<color="   # o hex ja vem com o "#" (ex.: "#C8B090")
ABRE_COR_COM_HASH = ABRE_COR + "#"     # a abertura como o C# a procura (`const string abertura`)
FECHA_COR = "</color>"


def valor_de_tabela(bruto):
    """O valor de uma entrada do `.cs` como ele fica em memoria (quebra de linha de verdade)."""
    return bruto.replace(BS + "n", chr(10)).replace(BS + '"', '"')


def _entradas(nome):
    """(chave, valor) de TODAS as entradas de uma tabela de `LocalizePatch.cs`, na ordem do arquivo.

    Fonte UNICA: `tools/tabelas.py`. O regex que vivia aqui (`{ "k", "v" }` colado) NAO
    pulava comentario entre a abertura `{` e a chave — nem de LINHA nem de BLOCO — e por
    isso nao via 15 das 101 entradas de `TextFixes` (o ponto cego que o COR-3 mediu:
    o alcance saia 283/76 no lugar de 298/83).
    """
    return tab.pares(fonte_do_mod(), nome)


def pares_de_skill_com_dano():
    """Pares (chave, nota) REAIS de tooltip de SKILL com dano: chave com `*N` e valor com a nota
    do nivel 2 — o material onde o defeito do COR-3 aparece. Ordem do arquivo (determinista)."""
    pares = []
    for nome in ("TextAppends", "TextFixes"):
        for chave, valor in _entradas(nome):
            if "*0" in chave and ("<color=#C8B090>" in valor):
                pares.append((chave, valor))
    return pares


def par_de_shrine():
    """Pares (chave, nota) de uma das 12 notas de SHRINE enxugadas pelo dono (a de dodge): o valor
    `[0]` sai na linha branca e a nota diz a base — a mesma leitura do defeito, no outro material."""
    alvo = "Increases dodge chance by [0]%."
    for nome in ("TextAppends", "TextFixes"):
        for chave, valor in _entradas(nome):
            if chave == alvo:
                return chave, valor
    raise arc.Falhou("nao achei a chave de shrine %r nas tabelas do LocalizePatch.cs" % alvo)


def dano_do_motor(texto, valor, tamanho=18.9):
    """`GetDamageString` (l.2276): `*0` -> `<size=..><color=#CBB396>NN</color></size>`."""
    return texto.replace("*0", "<size=%s><color=%s>%s</color></size>"
                              % (tamanho, COR_DO_VALOR_DO_MOTOR, valor))


def expressao_do_motor(texto, valor):
    """`ApplyDescriptionExpressions` (l.2327): `[0]` -> `<color=#CBB396>VALOR</color>`."""
    return texto.replace("[0]", ABRE_COR + COR_DO_VALOR_DO_MOTOR + ">" + str(valor) + FECHA_COR)


def _registra_blocos(texto, registro):
    """Espelho do `RegistrarBlocosDeNota` (COR-3): o CONTEUDO de cada bloco que nasceu com o
    marcador. E a identidade que sobrevive a troca de cor.

    REV-17/COR-3R: o C# EXCLUI os blocos do NIVEL 3 (`EhBlocoDoNivel3`): um bloco que abre com o
    marcador de texto do nivel 3 e uma linha de ESTADO (auras / skills), nao uma nota do nivel 2 —
    se ele caiu no marcador de reserva, nao entra no registro (e nunca e movido como nota). Sem
    esta exclusao, o espelho registrava um bloco que o codigo NAO registra: o teste media um
    comportamento que nao existe.
    """
    abre = ABRE_COR + entrada_marcador() + ">"
    i = 0
    while i < len(texto):
        j = texto.find(abre, i)
        if j < 0:
            return
        fim = texto.find(FECHA_COR, j + len(abre))
        if fim < 0:
            return
        conteudo = texto[j + len(abre):fim]
        if not eh_bloco_do_nivel_3(conteudo):
            registro.add(conteudo)
        i = fim + 1


def com_a_cor_do_jogo(texto, cor_do_campo, registro):
    """Espelho do `ComACorDoJogo` + do gancho das notas: a chave localizada, a nota anexada com o
    MARCADOR e a cor do nivel 2 resolvida — REGISTRANDO os blocos antes da troca."""
    if entrada_marcador() not in texto:
        return texto
    _registra_blocos(texto, registro)
    return texto.replace(ABRE_COR + entrada_marcador() + ">", ABRE_COR + cor_do_campo + ">")


def _bloco_em(texto, i):
    """(inicio, fim, conteudo) do bloco `<color=#...>...</color>` que abre em `i`."""
    fecha_tag = texto.index(">", i)
    conteudo_ini = fecha_tag + 1
    fim = texto.index(FECHA_COR, conteudo_ini)
    return conteudo_ini, fim + len(FECHA_COR), texto[conteudo_ini:fim]


def tira_o_primeiro_bloco_da_cor(texto, hex_):
    """A REGRA ANTIGA do `CorEOrdemDoTooltip`: 'o primeiro bloco da cor do nivel 2'.

    É o codigo que esta no build do dono (`TirarBloco(ref description, <cor do nivel 2>,
    ultimo: false, null, out bloco2)`). Devolve (texto sem o bloco, bloco).
    """
    i = texto.find(ABRE_COR + hex_ + ">")
    if i < 0:
        return texto, None
    ini_conteudo, fim, _conteudo = _bloco_em(texto, i)
    ini = i - 1 if i > 0 and texto[i - 1] == chr(10) else i
    bloco = texto[ini:fim].strip(chr(10)).rstrip()
    return texto[:ini] + texto[fim:], bloco


def _inicio_do_separador(texto, posicao, inteira=True):
    """ESPELHO do `InicioDoSeparador` do C# (RV-17): o bloco em `posicao` mais a LINHA EM BRANCO
    que o `AnexarNota` escreveu antes dele (ate DUAS quebras). Consumir so uma deixava a outra
    orfa no corpo — era ela que aparecia como linha em branco entre a descricao e o `AP Cost`
    depois que a nota era movida para o fim. Nas entradas FUNDIDAS (uma quebra so) nada mais e
    consumido: aquela quebra e o separador do proprio texto.

    `inteira=False` e o desenho ANTES do RV-17 (uma quebra so): e ele que a contra-prova planta.
    """
    ini = posicao
    if ini > 0 and texto[ini - 1] == chr(10):
        ini -= 1
        if inteira and ini > 0 and texto[ini - 1] == chr(10):
            ini -= 1
    return ini


def tira_a_nota_do_mod(texto, registro, inteira=True):
    """A REGRA DO COR-3 (`TirarNotaDoMod`): a NOSSA nota e achada pelo CONTEUDO que o mod escreveu,
    nunca pela cor. Devolve (texto sem a nota, nota).

    RV-17: como no C#, o trecho removido leva junto a linha em branco INTEIRA que o `AnexarNota`
    escreveu antes do bloco (`_inicio_do_separador`)."""
    i = 0
    while i < len(texto):
        # BANCADA-1: a busca do C# e `const string abertura = "<color=#"` — o `#` faz parte da
        # abertura. Procurar so `"<color="` casaria tambem um `<color=Nome>` que o jogo nunca
        # escreve: a bancada aceitaria um bloco que o codigo NAO aceita.
        j = texto.find(ABRE_COR_COM_HASH, i)
        if j < 0:
            return texto, None
        conteudo_ini, fim, conteudo = _bloco_em(texto, j)
        if conteudo in registro:
            ini = _inicio_do_separador(texto, j, inteira)
            nota = texto[ini:fim].strip(chr(10)).rstrip()
            return texto[:ini] + texto[fim:], nota
        i = fim
    return texto, None


def tira_as_notas_do_mod(texto, registro, inteira=True):
    """TODAS as notas do mod, na ORDEM em que aparecem (RV-17) — o laco do `CorEOrdemDoTooltip`.
    Devolve (texto sem as notas, [notas]). Uma tooltip pode ter DUAS: os dois casos reais sao o
    `Shapeshift Dragonkin` e o buff `Miniature`."""
    notas = []
    while True:
        texto, nota = tira_a_nota_do_mod(texto, registro, inteira)
        if nota is None:
            return texto, notas
        notas.append(nota)


def monta_a_descricao(chave, nota, dano=None, expressao=None, custos=(), aura=None,
                      notas=(), valor_sem_cor=None,
                      quebras_antes_do_custo=QUEBRAS_ANTES_DO_CUSTO_DA_BANCADA):
    """O caminho REAL ate o texto que o `ShowSkillTooltip` entrega ao `Tooltip.ShowTooltip`:

      1. a chave localizada (o texto do nivel 1, com os marcadores do motor `*N`/`[N]` ainda crus);
      2. o gancho das notas anexa a nota (bloco com o MARCADOR) e resolve a cor do nivel 2;
      3. a linha azul do nivel 3 (auras de shrine) e anexada por ULTIMO no texto da descricao;
      4. o MOTOR resolve `*N` (dano) e `[N]` (expressao) — os dois em `<color=#CBB396>`;
      5. o `ShowSkillTooltip` concatena os CUSTOS/ALCANCE depois da descricao.

    `nota` e a nota da tabela (`TextAppends`); `notas` e a lista de blocos FUNDIDOS que o texto ja
    carrega (os dois casos com DUAS notas: `Shapeshift Dragonkin` e `Miniature`); `valor_sem_cor` e
    a parte do nivel 1 de uma entrada fundida (o texto corrigido, sem nota nenhuma).

    `quebras_antes_do_custo` e quantas QUEBRAS o jogo escreve entre a descricao e a 1a linha de
    custo — BANCADA-1: DUAS (l.1470 + l.1536), o que da UMA LINHA EM BRANCO antes do `AP Cost`. As
    linhas de custo SEGUINTES vao com UMA quebra cada (`Range`/`Mana Cost`/`Cooldown`, l.1558/1565/1572).
    O valor da fixture (`quebras_antes_do_custo_do_jogo()`) e quem diz qual e o certo; este
    parametro existe para a contra-prova poder PLANTAR o defeito (a bancada antiga, com uma quebra).

    Devolve (texto que chega ao prefixo, registro das notas do mod).
    """
    texto = chave if valor_sem_cor is None else valor_sem_cor
    if nota:
        texto = anexa_nota(texto, nota)
    for fundida in notas:
        texto = anexa_nota(texto, fundida)
    if aura:
        texto = anexa_nota(texto, aura)
    registro = set()
    texto = com_a_cor_do_jogo(texto, cor_do_nivel_2(), registro)
    if dano is not None:
        texto = dano_do_motor(texto, dano)
    if expressao is not None:
        texto = expressao_do_motor(texto, expressao)
    if custos:
        if quebras_antes_do_custo < 1:
            raise arc.Falhou("`quebras_antes_do_custo` tem de ser pelo menos 1 (l.1536), veio %r"
                             % (quebras_antes_do_custo,))
        # l.1470 (`original += "\n"`) + l.1536 (`original + "\n" + "AP Cost: ..."`); o jogo NAO
        # apara o original (quem chega aqui nunca termina em quebra: o `AnexarNota` apara).
        texto += chr(10) * quebras_antes_do_custo
        for i, custo in enumerate(custos):
            if i:
                texto += chr(10)
            texto += custo
    return texto, registro


# ---------------------------------------------------- BANCADA-1: a MOLDURA do ground effect ---
# O `ShowGroundEffectTooltip` (l.1219-1304) NAO monta custo nenhum. O corpo dele e a moldura abaixo,
# e e ELA que envolve a descricao localizada (onde a nota e a linha azul foram anexadas):
#
#   <color=#CBB396>Titulo[Stacks]</color>\n   (l.1243 - a cor do jogo, UMA quebra)
#   <size=...>                                 (l.1244 - `num = Description.fontSize * 0.9f`)
#     <descricao: texto do jogo + a NOTA + a linha azul do nivel 3>
#     \nTurns Remaining: <color=#CBB396>N</color>   (l.1254 - UMA quebra, so quando o
#                                                    `ShowRemainingTurnsOnTooltip` do asset pede)
#     \n<color=#...>Friendly</color>                (l.1278 - UMA quebra; Enemy/Neutral sao os
#                                                    outros ramos do mesmo `switch`)
#   </size>                                    (l.1291)
#
# Ou seja: no caminho do ground effect NAO existe `AP Cost` nem `Range` — a "tooltip de shrine" que
# a bancada modelava como skill era de OUTRO caminho. A unica linha em branco daqui e a que separa
# ground effects DISTINTOS (o dicionario e reescrito com "\n\n" entre as entradas, l.1298).
TAMANHO_DO_GROUND_EFFECT = "13.5"   # `Description.fontSize * 0.9f` (l.1228): o formato importa que
                                    # o `<size>` EXISTA, nao o numero exato da fonte do prefab


def molda_ground_effect(texto, titulo):
    """A MOLDURA REAL do `ShowGroundEffectTooltip` em volta do texto localizado (o caminho da
    tooltip de SHRINE): titulo na cor do jogo, `<size>`, a descricao, `Turns Remaining` e a linha
    de TIME — cada parte com UMA quebra. NAO ha `AP Cost` nem `Range` (ver a leitura do formato)."""
    return ("<color=#CBB396>" + titulo + "[Stacks]</color>" + chr(10)
            + "<size=" + TAMANHO_DO_GROUND_EFFECT + ">" + texto
            + chr(10) + "Turns Remaining: <color=#CBB396>3</color>"
            + chr(10) + "<color=#64FF6A>Friendly</color>" + "</size>")


def anexa_nota(texto, nota):
    """ESPELHO do `AnexarNota` do C#: `TrimEnd` no texto, EXATAMENTE UMA linha em branco, e o
    `TrimStart('\\n')` da nota (a tabela escreve o valor com uma quebra na frente).

    O `TrimStart` nao e detalhe: sem ele a bancada produzia DUAS linhas em branco (a quebra da
    tabela somada ao `\\n\\n` do helper) — um formato que o codigo NUNCA escreveu. A bancada
    media um texto mais largo que o real, e um teste de FORMATO preso nela travaria o formato
    errado."""
    return texto.rstrip() + chr(10) + chr(10) + (nota or "").lstrip(chr(10))


def cor_do_nivel_2():
    """A cor declarada do nivel 2 (`Tooltip.specialDescColor`, lida no prefab em 01/10)."""
    return cor_do_campo("specialDescColor")


def cor_da_linha_azul():
    """O azul do nivel 3 em uso (elo 2: `GUIManager.coldColor`)."""
    return cor_da_hud("coldColor")


def monta_a_posicao(corpo, bloco):
    """O `CorEOrdemDoTooltip`: o bloco sai de onde estava e vai para o FIM do corpo, com uma linha
    em branco antes (a mesma regra do `AnexarNota`)."""
    if not bloco:
        return corpo
    return corpo.rstrip() + chr(10) + chr(10) + bloco


MARCADOR_DA_AURA = "Your active shrine auras:"


def tira_o_bloco_da_aura(texto, inteira=True):
    """A LINHA DE AURAS do nivel 3 (RV-27) — o unico bloco que o prefixo ainda acha por COR, e com
    razao: a cor dela e o azul da paleta, que o motor nao usa em valor nenhum, e o bloco carrega o
    MARCADOR DE TEXTO proprio (`Your active shrine auras:`) — o mesmo par do `TirarBloco(...
    corAura, ultima, ShrineAuraPatch.MarcadorLinhaDeAuras, ...)`."""
    hex_ = cor_da_linha_azul()
    i = texto.find(ABRE_COR + hex_ + ">")
    if i < 0:
        return texto, None
    _ini_conteudo, fim, conteudo = _bloco_em(texto, i)
    if MARCADOR_DA_AURA not in conteudo:
        return texto, None
    ini = _inicio_do_separador(texto, i)
    bloco = texto[ini:fim].strip(chr(10)).rstrip()
    return texto[:ini] + texto[fim:], bloco


def aplica_o_prefixo(texto, registro, regra_antiga, todas_as_notas=True, consome_a_linha_inteira=True):
    """O `CorEOrdemDoTooltip.Prefix` INTEIRO, na ordem do codigo: tira a linha de auras (nivel 3),
    tira as notas — pela regra pedida — e devolve tudo no fim, as NOTAS primeiro (na ordem em que
    aparecem) e a linha azul por ultimo.

    QUATRO desenhos, e a diferenca entre eles e a prova:

      * `regra_antiga=True` — a extracao por COR do build do dono (movia o primeiro bloco
        `#CBB396`, que podia ser o VALOR DO MOTOR): o defeito do COR-3;
      * `regra_antiga=False` — a extracao por CONTEUDO do COR-3;
      * `todas_as_notas=False` — para na PRIMEIRA nota mesmo na extracao por conteudo: era o
        estado do codigo ANTES do RV-17, e e o defeito dos DOIS casos com duas notas (`Shapeshift
        Dragonkin` e `Miniature`): a segunda ficava atras, antes do `AP Cost`;
      * `consome_a_linha_inteira=False` — consome so UMA quebra do separador, como antes do
        RV-17: a outra fica ORFA entre a descricao e o `AP Cost`.
    """
    corpo, aura = tira_o_bloco_da_aura(texto, consome_a_linha_inteira)
    if regra_antiga:
        corpo, nota = tira_o_primeiro_bloco_da_cor(corpo, cor_do_nivel_2())
        notas = [nota] if nota is not None else []
    elif todas_as_notas:
        corpo, notas = tira_as_notas_do_mod(corpo, registro, consome_a_linha_inteira)
    else:
        corpo, nota = tira_a_nota_do_mod(corpo, registro, consome_a_linha_inteira)
        notas = [nota] if nota is not None else []
    for bloco in notas:
        corpo = monta_a_posicao(corpo, bloco)
    return monta_a_posicao(corpo, aura)
