#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_bf_estilo.py - TST-7: a DECISAO DE ESTILO do BetterFont, lida do FONTE vivo.

POR QUE ESTA BIBLIOTECA EXISTE (e o que ela acrescenta a `regras_bf.py`)
-----------------------------------------------------------------------
`regras_bf.py` cobre duas coisas: (1) o PORTAO DE MATERIAL (o conserto do BF-2: variante
de shader nao e recusa, o criterio e o efeito presente) e (2) o ORCAMENTO do diagnostico
(BF-2R/BF-3/FIX-6). Esta biblioteca cobre o resto do comportamento do BF-1/BF-2 que o
dono pediu testado no TST-7, e que nao tinha modelo puro:

  * A DECISAO POR TEXTO, como funcao pura de quatro saidas - converter-com-transporte,
    converter-simples, nao-tocar, escape (TST-7, cenario 1) e o ESCAPE ligado/desligado
    (cenario 4). O `FontSweep` do `BetterFont/Plugin.cs` faz essa decisao a cada texto;
    `Material` e classe NATIVA do Unity e nao se instancia fora do jogo, entao o que se
    pode exercitar aqui e a TRANSCRICAO da decisao - e `falhas_da_decisao` amarra a
    transcricao a ESTRUTURA do fonte (a ORDEM dos ramos, os `continue` de quem nao e
    tocado, e o `efeitoPresente &&` do portao).
  * A MATRIZ DA FALHA-SEGURA, caso a caso (TST-7, cenario 2): `_FaceTex`, `_BumpMap`,
    `GLOW_ON`, `BEVEL_ON` e - no escopo CORRIGIDO depois do BF-2 - o shader diferente,
    que DEIXOU de ser recusa (virou copia best-effort). O modelo `estilo_transportavel`
    transcreve `EstiloTransportavel`; `TexturaDeEfeito` transcreve a distincao entre o
    default embutido do shader (branco/bump) e uma textura de EFEITO de verdade.
  * A LISTA DE PRESERVACAO (TST-7, cenario 3): o que e copiado e o que NAO e - as duas
    listas saem dos GRUPOS e das CHAMADAS do proprio `CopiarEstilo`, nunca digitadas.
  * OS DEFAULTS com arquivo:linha (TST-7, cenario 5) e os GETTERS SEGUROS.
  * O ACOPLAMENTO ZERO como teste-testemunha (TST-7, cenario 6): no fonte E na DLL
    construida.

REGRA DO PROJETO: todo teste tem de ser MOSTRADO REPROVANDO. Cada mutacao
(`fonte_com_*`/`dll_...`) existe para o teste plantar o defeito EM MEMORIA, ver as
checagens reprovarem, e so entao considera-las prontas. O plantio fisico no
`BetterFont/Plugin.cs` (rodar, ver REPROVOU; restaurar, ver PASSOU) esta registrado em
`tools/testes/bf-prova-reprovando.log`.
"""
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import recorte as rec
import regras_bf as bf

# Os termos proibidos (nome/GUID do outro mod) sao os MESMOS da trava do `regras_bf`:
# uma lista so, para as duas travas nunca divergirem.
PROIBIDOS = bf.PROIBIDOS

# ===========================================================================
# 1) A DECISAO POR TEXTO - as quatro saidas do TST-7 (cenario 1) + o escape (4)
# ===========================================================================

CONVERTE_COM_TRANSPORTE = "converter-com-transporte"
CONVERTE_SIMPLES = "converter-simples"
NAO_TOCAR = "nao-tocar"
ESCAPE = "escape"
JA_NA_SERIFA = "ja-na-serifa"
REVERTIDO = "revertido"

# Sentinela de "o texto tem efeito no material, mas ele NAO pode ser reproduzido".
# E o que separa `converter-com-transporte` de `nao-tocar` na decisao.
TRANSPORTAVEL = "transportavel"
NAO_TRANSPORTAVEL = "nao-transportavel"


class Texto(object):
    """O que o texto TEM, do ponto de vista da decisao (o material e nativo do Unity).

    Nao e o material de verdade: e a descricao do material nos termos que a decisao
    pergunta. Cada campo corresponde a uma pergunta EXATA do `FontSweep`:

      `material_proprio`   -> `EhEstilizado`: o material em uso nao e o padrao da fonte
                              do texto (o que QUALQUER mod faz ao clonar por componente);
      `shader_diferente`   -> `EhEstilizado`: shader != o da fonte serifada (o caso dos
                              textos de combate do jogo);
      `efeito_presente`    -> `TemEfeitoNoMaterial`: este material carrega contorno/sombra/
                              glow (nao "este texto foi classificado como estilizado");
      `efeito`             -> o veredito de `EstiloTransportavel` para esse material;
      `usa_material_novo`  -> `UsaMaterialDaFonteNova`: o `LoadFontAsset` ja apontou para o
                              atlas da fonte nova (guarda contra copiar para o material errado).

    `shader_diferente` e `material_proprio` NAO sao recusa no BF-2: eles so classificam o
    texto para o ESCAPE. O portao e `efeito_presente` x `efeito`.
    """

    def __init__(self, rotulo, ja_na_serifa=False, material_proprio=False,
                 shader_diferente=False, efeito_presente=False, efeito=TRANSPORTAVEL,
                 usa_material_novo=True):
        self.rotulo = rotulo
        self.ja_na_serifa = ja_na_serifa
        self.material_proprio = material_proprio
        self.shader_diferente = shader_diferente
        self.efeito_presente = efeito_presente
        self.efeito = efeito
        self.usa_material_novo = usa_material_novo

    def estilizado(self):
        return self.material_proprio or self.shader_diferente


def decidir(texto, preservar_estilo=True, pular_estilizados=False):
    """TRANSCRICAO da decisao do `FontSweep` - a funcao pura que o TST-7 pede.

    Espelha, na ordem, os ramos do fonte (BetterFont/Plugin.cs, `FontSweep`):

        if (t.font == _serifFont) continue;                          -> JA_NA_SERIFA
        bool estilizado = EhEstilizado(...);                          (material proprio
                                                                        OU shader diferente)
        if (estilizado && PularEstilizadosLigado) { ...; continue; }  -> ESCAPE
        if (efeitoPresente && !EstiloTransportavel(...)) { ...; continue; } -> NAO_TOCAR
        t.font = _serifFont; if (PreservarEstilo && antigo != null
            && UsaMaterialDaFonteNova) { CopiarEstilo(...); }         -> CONVERTE_*
        catch { ReverterTexto(...); continue; }                       -> REVERTIDO (nao ficou)

    `CONVERTE_COM_TRANSPORTE` = o texto TINHA efeito no material e ele foi reaplicado no
    material por componente; `CONVERTE_SIMPLES` = nao havia efeito para transportar (o
    `CopiarEstilo` ainda roda com PreservarEstilo ligado, mas copia os valores do material
    padrao da PROPRIA fonte - nada de estilo externo). `NAO_TOCAR` agrupa o pulado por
    efeito nao transportavel e o revertido: nos dois casos o texto termina como estava.
    """
    if texto.ja_na_serifa:
        return JA_NA_SERIFA
    if texto.estilizado() and pular_estilizados:
        return ESCAPE
    if texto.efeito_presente and texto.efeito == NAO_TRANSPORTAVEL:
        return NAO_TOCAR
    if texto.efeito_presente and preservar_estilo and texto.usa_material_novo:
        return CONVERTE_COM_TRANSPORTE
    return CONVERTE_SIMPLES


# ===========================================================================
# 2) A MATRIZ DA FALHA-SEGURA (cenario 2) e a textura de EFEITO de verdade
# ===========================================================================

def textura_de_efeito(unidade):
    """TRANSCRICAO de `TexturaDeEfeito`: a textura e EFEITO ou o default do shader?

    `None`            -> nao ha textura;
    `"white"/"bump"`  -> a embutida do Unity (o default do shader) -> NAO e efeito;
    `"real"`          -> textura de verdade (tamanho de atlas)     -> e efeito.
    """
    if unidade is None:
        return False
    if unidade in ("white", "bump", "gray", "black", "unity_default"):
        return False
    return True


def estilo_transportavel(mat, transporte_ligado=True, expoe=None):
    """TRANSCRICAO de `EstiloTransportavel`. Devolve `(transportavel, motivo)`.

    `mat` descreve o material EM USO: `face_tex`, `bump_map` (cada um `None` |
    `"white"`/`"bump"` (default) | `"real"`), `glow_on`, `bevel_on`, `contorno_em_uso`,
    `sombra_em_uso`, `shader_diferente`. `expoe` descreve o material NOVO (a fonte
    serifada): `_OutlineWidth` e `_UnderlaySoftness` (bool).

    O ESCOPO CORRIGIDO DEPOIS DO BF-2: `shader_diferente` NAO entra nesta conta. O BF-1
    recusava por variante de shader e era isso que deixava os textos de combate na fonte
    original (o defeito que o BF-2 consertou): a variante diferente virou copia best-effort
    propriedade por propriedade (`HasProperty`), e o que a variante nova nao expuser sai no
    log como nao transportado. Este modelo NAO PERGUNTA o shader de proposito - e essa a
    expectativa, e `falhas_da_falha_segura` exige que o fonte tambem nao pergunte.
    """
    if mat is None:
        return True, None
    if textura_de_efeito(mat.get("face_tex")):
        return False, "_FaceTex (textura de face) em uso"
    if textura_de_efeito(mat.get("bump_map")):
        return False, "_BumpMap (bevel) em uso"
    if mat.get("glow_on"):
        return False, "GLOW_ON ligado"
    if mat.get("bevel_on"):
        return False, "BEVEL_ON ligado"
    if not transporte_ligado:
        # Sem copia pedida: as conferencias abaixo sao sobre a COPIA caber no material
        # novo, e nao ha copia. O que barra acima continua valendo sempre.
        return True, None
    if expoe is None:
        return False, "a fonte serifada ainda nao tem material"
    if mat.get("contorno_em_uso") and not expoe.get("_OutlineWidth"):
        return False, "contorno em uso e o material novo nao expoe _OutlineWidth"
    if mat.get("sombra_em_uso") and not expoe.get("_UnderlaySoftness"):
        return False, "sombra em uso e o material novo nao expoe underlay"
    return True, None


MATRIZ_FALHA_SEGURA = (
    # (rotulo, ajuste no material, motivo esperado no fonte)
    ("_FaceTex (textura de face de verdade)", {"face_tex": "real"}, "_FaceTex"),
    ("_BumpMap (bevel de verdade)", {"bump_map": "real"}, "_BumpMap"),
    ("GLOW_ON", {"glow_on": True}, "GLOW_ON"),
    ("BEVEL_ON", {"bevel_on": True}, "BEVEL_ON"),
)

# Os dois casos que dependem do material NOVO nao expor o efeito: o mesmo material (contorno
# ou sombra em uso) com um material novo que nao tem a propriedade tem de reprovar.
MATRIZ_NAO_EXPOE = (
    ("contorno em uso que o material novo nao expoe", {"contorno_em_uso": True},
     {"_UnderlaySoftness": True}, "_OutlineWidth"),
    ("sombra em uso que o material novo nao expoe", {"sombra_em_uso": True},
     {"_OutlineWidth": True}, "underlay"),
)

# ===========================================================================
# 3) O FONTE VIVO: grupos, chamadas de copia, defaults com linha, getters
# ===========================================================================

GRUPO_PROPS_COR = "PropsCor"
GRUPO_PROPS_FLOAT = "PropsFloat"
GRUPO_PROPS_VETOR = "PropsVetor"
GRUPO_KEYWORDS_MASCARA = "KeywordsMascara"
GRUPO_PROPS_FONTE = "PropsDeFonteRegistradas"

# O que PRECISA ser transportado (cenario 3) - a promessa do BF-ESTILO/BF-1.
PRECISA_COPIAR = {
    GRUPO_PROPS_COR: ("_FaceColor", "_OutlineColor", "_UnderlayColor"),
    GRUPO_PROPS_FLOAT: (
        "_FaceDilate", "_OutlineWidth", "_OutlineSoftness",
        "_UnderlayOffsetX", "_UnderlayOffsetY", "_UnderlayDilate", "_UnderlaySoftness",
        "_VertexOffsetX", "_VertexOffsetY", "_MaskSoftnessX", "_MaskSoftnessY",
    ),
    GRUPO_PROPS_VETOR: ("_ClipRect",),
}
PRECISA_LIGAR = ("OUTLINE_ON", "UNDERLAY_ON")          # as keywords que LIGAM o efeito

# O que NAO pode ser transportado (cenario 3): pertence a FONTE/atlas NOVA, ou e um
# efeito que a copia nao reproduz (e ai o texto nao e tocado, nao "copiado pela metade").
NAO_PODE_COPIAR = (
    "_MainTex", "_GradientScale", "_TextureWidth", "_TextureHeight", "_ScaleRatio",
    "_FaceTex", "_BumpMap", "GLOW_ON", "BEVEL_ON", "_WeightNormal", "_WeightBold",
)


def fonte():
    return bf.fonte()


def grupo(src, nome):
    """Le um `string[] <nome> = { ... };` do fonte. Devolve a lista ou None se sumiu."""
    i = src.find("string[] " + nome)
    if i < 0:
        return None
    j = src.find("{", i)
    k = src.find("}", j)
    if j < 0 or k < 0:
        return None
    return re.findall(r'"([^"]+)"', src[j:k])


def copiar_corpo(src):
    return bf.corpo(src, bf.COPIAR)


def _ramo(sweep, marcador):
    """O bloco `{ ... }` balanceado que comeca no PRIMEIRO `{` depois de `marcador`.

    FORMATO-3: o casamento de chaves passa pelo `recorte.py` — chave dentro de literal de
    string/char nao conta (o `$"...{x}..."` do diagnostico nao confunde mais). Devolve `None`
    (contrato antigo) quando o marcador ou a abertura somem.
    """
    i = sweep.find(marcador)
    if i < 0:
        return None
    p = sweep.find("{", i)
    if p < 0:
        return None
    try:
        bloco = rec.bloco_balanceado(sweep, p)
    except arc.Falhou:
        return None
    return sweep[i:p + len(bloco)]


# O `CopiarEstilo` nao escreve o NOME da propriedade em cada Set: ele percorre os GRUPOS
# (`for ... string p = PropsCor[i] ... novo.SetColor(p, ...)`). Entao o conjunto copiado
# sai dos DOIS lados: o grupo tem de existir E a chamada do grupo tem de existir no corpo.
GRUPO_METODO = ((GRUPO_PROPS_COR, "SetColor"), (GRUPO_PROPS_FLOAT, "SetFloat"),
                (GRUPO_PROPS_VETOR, "SetVector"))


def copia_efetiva(src):
    """O que `CopiarEstilo` transporta, lido da ESTRUTURA. Devolve um dict.

      `grupos`      - nome do grupo -> lista lida do fonte (ou None se sumiu);
      `grupos_ativos`- nome do grupo -> lista, SO quando o corpo do metodo percorre o grupo
                       chamando o Set correspondente (`novo.SetColor(p` etc.);
      `keywords`    - as keywords com `EnableKeyword("LITERAL")`;
      `keywords_grupo` - as keywords ligadas por loop (o grupo KeywordsMascara).
    """
    corpo = copiar_corpo(src)
    grupos = {}
    ativos = {}
    for nome, metodo in GRUPO_METODO:
        lista = grupo(src, nome)
        grupos[nome] = lista
        if lista is not None and corpo is not None and ("novo.%s(p" % metodo) in corpo:
            ativos[nome] = lista
    keywords = sorted(set(re.findall(r'novo\.EnableKeyword\(\s*"([^"]+)"', corpo or "")))
    keywords_grupo = grupo(src, GRUPO_KEYWORDS_MASCARA) if corpo and "novo.EnableKeyword(k)" in corpo else []
    return {"grupos": grupos, "grupos_ativos": ativos, "keywords": keywords,
            "keywords_grupo": keywords_grupo or []}


def propriedades_proibidas_presentes(src):
    """Quais propriedades de `NAO_PODE_COPIAR` entram numa copia (grupo ativo ou keyword)."""
    efetiva = copia_efetiva(src)
    copiadas = set()
    for lista in efetiva["grupos_ativos"].values():
        copiadas.update(lista)
    copiadas.update(efetiva["keywords"])
    copiadas.update(efetiva["keywords_grupo"])
    return [p for p in NAO_PODE_COPIAR if p in copiadas]


def defaults_com_linha(src):
    """Os tres `BindSeguro(...)` de config, com o valor e a LINHA do fonte (cenario 5).

    Devolve `{chave: {"valor": bool, "linha": int}}`. E a leitura por `arquivo:linha` que
    o TST-7 pede - se um default mudar (o unico que mudou no BF-1 foi `PularTextosEstilizados`
    para `false`), a checagem aponta a linha.
    """
    achados = {}
    for numero, linha in enumerate(src.splitlines(), 1):
        m = re.search(r'BindSeguro\("([^"]+)",\s*"([^"]+)",\s*(true|false)\s*,', linha)
        if m:
            achados[m.group(2)] = {"secao": m.group(1), "valor": m.group(3) == "true",
                                   "linha": numero}
    return achados


def getters_seguros(src):
    """Os tres getters: o valor em caso de FALHA de config (entrada null) por chave."""
    achados = {}
    for chave, getter in (("PreservarEstilo", "PreservarEstiloLigado"),
                          ("PularTextosEstilizados", "PularEstilizadosLigado"),
                          ("LogDiagnosticoEstilo", "LogDiagnosticoLigado")):
        m = re.search(r"bool\s+%s\b[^{]*\{[^}]*return\s+([^;]+);" % getter, src, flags=re.S)
        if m:
            corpo = m.group(1)
            # `== null || X.Value` -> sem entrada vale TRUE (conservador/ligado);
            # `!= null && X.Value` -> sem entrada vale FALSE (desligado).
            achados[chave] = {"conservador_ligado": ("== null ||" in corpo),
                              "expressao": " ".join(corpo.split())}
    return achados


# ===========================================================================
# 4) ACOPLAMENTO ZERO - fonte E DLL (cenario 6)
# ===========================================================================

def ocorrencias_de_acoplamento(texto):
    """Nomes/GUIDs de outro mod que aparecam no texto, na ordem de `PROIBIDOS` (de `regras_bf`)."""
    return [p for p in PROIBIDOS if p in texto]


def dlls_do_betterfont():
    """As DLLs construidas do BetterFont que existem no worktree (build local)."""
    raiz = os.path.join(arc.raiz_do_repo(), "BetterFont", "bin")
    achadas = []
    if not os.path.isdir(raiz):
        return achadas
    for pasta, _, arquivos in os.walk(raiz):
        for nome in arquivos:
            if nome.lower() == "betterfont.dll":
                achadas.append(os.path.join(pasta, nome))
    return sorted(achadas)


def ocorrencias_nos_bytes(dados):
    """O mesmo teste-testemunha sobre BYTES: procura em UTF-8 e UTF-16LE (o .NET).

    Se o CODIGO citar o outro mod, o nome/GUID entra nos metadados ou num literal e a busca
    acha. Hoje a busca da VAZIO nas duas codificacoes - e e isso que o teste trava.
    """
    achados = []
    for proibido in PROIBIDOS:
        for codec in ("utf-8", "utf-16-le"):
            if proibido.encode(codec) in dados:
                achados.append("%s (%s)" % (proibido, codec))
    return achados


def ocorrencias_no_binario(caminho):
    """A mesma varredura, sobre o ARQUIVO da DLL construida."""
    with io.open(caminho, "rb") as fh:
        return ocorrencias_nos_bytes(fh.read())


# ===========================================================================
# 5) AS CHECAGENS SOBRE O FONTE (o que os testes puros exercitam)
# ===========================================================================

def falhas_da_decisao(src):
    """A decisao do `FontSweep` esta na ORDEM e com os freios certos? Lista vazia = ok."""
    falhas = []
    sweep = bf.corpo(src, bf.SWEEP)
    if sweep is None:
        return ["nao achei o `FontSweep` no fonte"]

    # (a) o escape vem ANTES do portao, e so vale para ESTILIZADO.
    i_escape = sweep.find("estilizado && Plugin.PularEstilizadosLigado")
    if i_escape < 0:
        falhas.append("o ramo do ESCAPE nao esta preso a `estilizado && Plugin.PularEstilizadosLigado`: "
                      "o texto estilizado deixa de ser pulado (ou o NAO estilizado passa a ser pulado)")
    i_portao = sweep.find("efeitoPresente &&")
    if i_portao < 0:
        falhas.append("o portao nao esta preso a `efeitoPresente &&`: ele volta a olhar a "
                      "classificacao do texto (o defeito do BF-1) em vez do EFEITO no material")
    if i_escape >= 0 and i_portao >= 0 and i_escape > i_portao:
        falhas.append("o ramo do ESCAPE vem DEPOIS do portao de efeito: com o escape ligado "
                      "o texto estilizado passaria a ser julgado pelo portao, e nao pulado")

    # (b) o ramo do escape NAO toca no texto: `continue` imediato (nada de fonte/material).
    if i_escape >= 0:
        ramo = _ramo(sweep, "if (estilizado && Plugin.PularEstilizadosLigado)")
        if ramo is None:
            falhas.append("nao consegui ler o bloco do ramo do ESCAPE")
        else:
            if "continue" not in ramo:
                falhas.append("o ramo do ESCAPE nao da `continue`: o texto pulado seria tocado")
            if "t.font = _serifFont" in ramo:
                falhas.append("o ramo do ESCAPE troca a fonte antes de sair (o pulo nao e pulo)")

    # (c) o caminho de sucesso troca a fonte E chama a copia/padding no MESMO try.
    #     O recorte e o `try { ... }` INTEIRO por casamento de chaves (FORMATO-3) — nao uma
    #     janela de 1200 caracteres, que media DISTANCIA e reprovava por reformatacao.
    i_troca = sweep.find("t.font = _serifFont")
    if i_troca < 0:
        falhas.append("nao achei a troca de fonte no `FontSweep`")
    else:
        try:
            trecho = rec.bloco_que_contem(sweep, i_troca)
        except arc.Falhou as erro:
            falhas.append("nao consegui recortar o bloco da troca de fonte por casamento de "
                          "chaves: %s" % erro)
            trecho = ""
        for trecho_esperado, rotulo in (("CopiarEstilo(", "a copia do estilo"),
                                        ("UpdateMeshPadding()", "o recalculo do padding"),
                                        ("SetVerticesDirty()", "o pedido de redesenho")):
            if trecho_esperado not in trecho:
                falhas.append("o caminho de sucesso nao chama %s depois de trocar a fonte" % rotulo)

    # (d) o getter de estilo e usado na troca de fonte (o caminho novo) sem pular o portao.
    if "Plugin.PreservarEstiloLigado && antigo != null && UsaMaterialDaFonteNova(t)" not in sweep:
        falhas.append("o transporte de estilo nao esta preso a "
                      "`PreservarEstiloLigado && antigo != null && UsaMaterialDaFonteNova(t)`")

    # (e) nao existe a recusa por shader em lugar nenhum do tratamento (o defeito do BF-1).
    for trecho, rotulo in (("antigo.shader != padraoNovo.shader", "recusa por shader"),
                           ("shader incompativel", "motivo de recusa por shader")):
        if trecho in sweep:
            falhas.append("o `FontSweep` cita %s (defeito do BF-1)" % rotulo)
    return falhas


def falhas_da_falha_segura(src):
    """A matriz da falha-segura no fonte: os quatro efeitos secos barram, o shader nao."""
    falhas = []
    et = bf.corpo(src, bf.ET)
    if et is None:
        return ["nao achei `EstiloTransportavel` no fonte"]

    for prop, motivo in (("_FaceTex", "_FaceTex"), ("_BumpMap", "_BumpMap"),
                         ("GLOW_ON", "GLOW_ON"), ("BEVEL_ON", "BEVEL_ON")):
        if motivo not in et:
            falhas.append("a falha-segura nao barra por %s: o texto com esse efeito seria "
                          "trocado e perderia o efeito (copia parcial, pior que nao mexer)" % prop)

    # _FaceTex/_BumpMap tem de passar por TexturaDeEfeito (o default do shader nao e efeito).
    for prop in ("_FaceTex", "_BumpMap"):
        linha_prop = [l for l in et.splitlines() if prop in l]
        if not linha_prop or not any("TexturaDeEfeito(" in l for l in linha_prop):
            falhas.append("%s nao passa por TexturaDeEfeito: o default embutido do shader "
                          "volta a contar como efeito e a falha-segura recusa todo material de SDF" % prop)

    # O ESCOPO CORRIGIDO (BF-2): shader diferente NAO reprova.
    if "shader" in et and ("!=" in et or "==" in et):
        for linha in et.splitlines():
            if "shader" in linha and ("!=" in linha or "==" in linha):
                falhas.append("a falha-segura voltou a RECUSAR por variante de shader (`%s`): "
                              "e o defeito do BF-1 - os textos de combate ficam na fonte original"
                              % linha.strip())
    return falhas


def falhas_da_preservacao(src):
    """As DUAS listas do cenario 3: o que copia, o que NAO copia (e o que tem de logar)."""
    falhas = []
    efetiva = copia_efetiva(src)
    if copiar_corpo(src) is None:
        return ["nao achei `CopiarEstilo` no fonte"]

    # LISTA 1: o que PRECISA estar copiado (grupo com o Set) / ligado (keyword).
    for nome_grupo, props in PRECISA_COPIAR.items():
        lista = efetiva["grupos"].get(nome_grupo)
        if lista is None:
            falhas.append("nao achei o grupo `%s` no fonte" % nome_grupo)
            continue
        if nome_grupo not in efetiva["grupos_ativos"]:
            metodo = dict(GRUPO_METODO)[nome_grupo]
            falhas.append("o grupo `%s` NAO e percorrido por um `novo.%s(p, ...)` em CopiarEstilo: "
                          "as propriedades dele deixaram de ser transportadas" % (nome_grupo, metodo))
        for prop in props:
            if prop not in lista:
                falhas.append("`%s` saiu do grupo %s: uma propriedade de ESTILO deixou de ser "
                              "transportada" % (prop, nome_grupo))

    for keyword in PRECISA_LIGAR:
        if keyword not in efetiva["keywords"]:
            falhas.append("a keyword `%s` deixou de ser LIGADA no material novo: sem ela o "
                          "contorno/sombra nao aparece no shader" % keyword)
    if "UNDERLAY_INNER" not in efetiva["keywords"]:
        falhas.append("a keyword `UNDERLAY_INNER` deixou de ser transportada (a sombra interna "
                      "volta a sair 'outer' calada)")
    for keyword in ("MASK_SOFT", "MASK_HARD", "MASK_TEX"):
        if keyword not in efetiva["keywords_grupo"]:
            falhas.append("a keyword de recorte `%s` saiu do grupo transportado" % keyword)

    # LISTA 2: o que NAO pode ser copiado (pertence a FONTE/atlas nova ou e efeito irreproduzivel).
    proibidas = propriedades_proibidas_presentes(src)
    if proibidas:
        falhas.append("a copia passou a transportar o que pertence a FONTE NOVA (ou a um efeito que "
                      "a copia nao reproduz): %s" % ", ".join(sorted(proibidas)))

    # LISTA 2b: o que NAO e copiado e TEM de ser nomeado no log (`perdidos`/`registros`).
    copiar = copiar_corpo(src) or ""
    for prop in ("_FaceTex", "_BumpMap", "GLOW_ON", "BEVEL_ON", "_GradientScale"):
        if prop not in copiar:
            falhas.append("`%s` nao e copiado NEM nomeado no log: ficaria em branco para quem "
                          "le o diagnostico" % prop)
    pesos = grupo(src, GRUPO_PROPS_FONTE) or []
    if "RegistrarDiferenca(" not in copiar:
        falhas.append("os parametros da fonte (`PropsDeFonteRegistradas`) deixaram de ser registrados")
    for prop in ("_WeightNormal", "_WeightBold"):
        if prop not in pesos:
            falhas.append("`%s` nao esta no grupo dos parametros da fonte registrados" % prop)
    return falhas


def falhas_dos_defaults(src):
    """Os tres defaults e os getters seguros: o unico que mudou no BF-1 foi o escape."""
    falhas = []
    esperado = {"PreservarEstilo": True, "PularTextosEstilizados": False, "LogDiagnosticoEstilo": False}
    achados = defaults_com_linha(src)
    for chave, valor in esperado.items():
        if chave not in achados:
            falhas.append("nao achei o `BindSeguro` da chave %s no fonte" % chave)
            continue
        if achados[chave]["valor"] != valor:
            falhas.append("o default de %s mudou (linha %d): esperado %s, obtido %s"
                          % (chave, achados[chave]["linha"], valor, achados[chave]["valor"]))

    getters = getters_seguros(src)
    if not getters.get("PularTextosEstilizados", {}).get("conservador_ligado"):
        falhas.append("o getter de `PularTextosEstilizados` nao cai no CONSERVADOR (true) quando "
                      "a entrada de config e null: falha de config deixaria de proteger o texto")
    if getters.get("PreservarEstilo", {}).get("conservador_ligado") is not True:
        falhas.append("o getter de `PreservarEstilo` nao vale true sem entrada de config")
    if getters.get("LogDiagnosticoEstilo", {}).get("conservador_ligado") is not False:
        falhas.append("o getter de `LogDiagnosticoEstilo` nao vale false sem entrada de config")
    return falhas


def falhas_do_nao_regride(src):
    """O que o dono aprovou e nao pode mudar: o caminho do texto NORMAL e o fallback."""
    falhas = []
    sweep = bf.corpo(src, bf.SWEEP)
    if sweep is None:
        return ["nao achei `FontSweep` no fonte"]

    if "t.font = _serifFont" not in sweep:
        falhas.append("a troca de fonte dos textos NORMAIS sumiu")
    if "RegistrarFallback(t)" not in sweep:
        falhas.append("a varredura deixou de registrar a fonte original como fallback "
                      "(icones/simbolos sem glifo viram quadradinhos - a promessa da 1.0.0)")

    registrar = bf.corpo(src, "private void RegistrarFallback(")
    if registrar is None:
        falhas.append("nao achei `RegistrarFallback` no fonte")
    else:
        if "fallbackFontAssetTable.Add(t.font)" not in registrar:
            falhas.append("`RegistrarFallback` nao adiciona a fonte original do texto ao fallback")

    # O resumo da varredura continua dizendo os tres desfechos (o texto que o dono aprovou).
    for trecho, rotulo in (("texto(s) convertidos para a serifa", "os convertidos"),
                           ("pulado(s) pelo escape", "os pulados pelo escape"),
                           ("intocado(s) por efeito nao transportavel", "os intocados por efeito")):
        if trecho not in sweep:
            falhas.append("o resumo da varredura deixou de dizer %s" % rotulo)

    # SEM GAMEPLAY: o unico gancho do mod e a localizacao da UI (OptionsManager.Localize).
    patches = re.findall(r"\[HarmonyPatch\(typeof\((\w+)\)", src)
    if not patches:
        falhas.append("nao achei nenhum `[HarmonyPatch(typeof(...))]` no fonte")
    for alvo in patches:
        if alvo != "OptionsManager":
            falhas.append("o mod passou a ganchar `%s`: a promessa e que ele so toca a "
                          "LOCALIZACAO da UI (OptionsManager), nunca gameplay" % alvo)
    if "LocalizeFontTrigger" not in src:
        falhas.append("o gatilho `LocalizeFontTrigger` (aplicacao preguicosa no primeiro Localize) sumiu")
    return falhas


# ===========================================================================
# 5b) BF-5 - A SOMBRA FANTASMA: a decisao de sombra nao pode ser por COR
# ===========================================================================
# O ACHADO DO BCT-4 (leitura do prefab com UnityPy): o rotulo 'SectionLabelText' do 'Select
# Attributes' (TMP no GO 'Label' [680588]) usa o material 'Regular Font (Minion Pro Regular) SDF
# Material', que traz `_UnderlayColor` preto alfa 0.5, `_UnderlayOffsetX/Y`/`_UnderlayDilate`/
# `_UnderlaySoftness` = 0 e o keyword `UNDERLAY_ON` DESLIGADO (`m_ValidKeywords == []`). E uma
# sombra INERTE que o jogo NUNCA desenha. O `CopiarEstilo` considerava "sombra em uso" por
# `_UnderlayColor.a > 0.001` (SEM olhar a keyword), LIGAVA o `UNDERLAY_ON` no material novo e
# copiava os valores: aparecia uma sombra que o jogo nunca renderizou - a "sombra muito grossa".
# O criterio certo e o que faz a sombra APARECER: keyword ligada OU offset/dilate != 0.

# A declaracao do helper que decide a sombra DE VERDADE (lida do fonte; se o nome mudar, a
# checagem REPROVA dizendo que sumiu - nunca passa vazia).
SOMBRA_DESENHADA = "private static bool SombraDesenhada("
# As propriedades GEOMETRICAS da sombra (o que a faz aparecer). `_UnderlaySoftness` NAO entra:
# sozinha ela nao desloca nem expande a sombra (fica atras do glifo, oculta).
PROPS_GEOMETRIA_SOMBRA = ("_UnderlayOffsetX", "_UnderlayOffsetY", "_UnderlayDilate")
# O defeito: a COR (alfa) decidindo a sombra sem a keyword. Vale para o fonte EFETIVO (sem
# comentarios), para um comentario que cite o padrao nao acusar.
PADRAO_SOMBRA_POR_COR = re.compile(r'GetColor\(\s*"_UnderlayColor"\s*\)\.a\s*>\s*0')


def expressao_sombra_ativa(src):
    """A decisao `bool sombraAtiva = ...;` do `CopiarEstilo`, ou None se a declaracao sumiu."""
    corpo = copiar_corpo(src) or ""
    i = corpo.find("bool sombraAtiva")
    if i < 0:
        return None
    fim = corpo.find(";", i)
    if fim < 0:
        return None
    return corpo[i:fim + 1]


def soma_criterio_de_sombra(src):
    """O corpo do helper `SombraDesenhada` (o criterio de sombra DE VERDADE), ou None."""
    return bf.corpo(src, SOMBRA_DESENHADA)


def falhas_da_sombra_inerte(src):
    """BF-5: a sombra NAO pode ser acesa por `_UnderlayColor.a > 0` sozinho. Lista vazia = ok.

    Tres exigencias, todas lidas do FONTE vivo:
      1. a decisao `bool sombraAtiva` precisa perguntar a KEYWORD (direto ou via o helper);
      2. ela NAO pode olhar a COR (`_UnderlayColor`/`GetColor`) - a cor nao prova que o shader
         desenha a sombra (o prefab do jogo tem alfa 0.5 com a keyword desligada);
      3. o helper `SombraDesenhada` precisa perguntar a keyword E olhar offset/dilate (a sombra
         de verdade); e o padrao `GetColor("_UnderlayColor").a > 0` nao pode sobrar em NENHUM
         ponto do codigo efetivo (portao, criterio de efeito e copia de estilo).
    """
    falhas = []
    if copiar_corpo(src) is None:
        return ["nao achei `CopiarEstilo` no fonte"]

    expr = expressao_sombra_ativa(src)
    if expr is None:
        falhas.append("nao achei a decisao de sombra `bool sombraAtiva = ...` em CopiarEstilo: "
                      "sem ela o UNDERLAY_ON pode voltar a ser ligado por qualquer coisa")
    else:
        tem_keyword = 'IsKeywordEnabled("UNDERLAY_ON")' in expr
        tem_helper = "SombraDesenhada(" in expr
        if not tem_keyword and not tem_helper:
            falhas.append("a decisao de sombra nao pergunta a KEYWORD da fonte "
                          "(IsKeywordEnabled(\"UNDERLAY_ON\")): a sombra INERTE (cor com alfa e "
                          "keyword desligada) volta a ser acesa")
        if "_UnderlayColor" in expr or "GetColor(" in expr:
            falhas.append("a decisao de sombra ainda olha a COR (`_UnderlayColor`/GetColor): a cor "
                          "sozinha NAO prova que o shader desenha a sombra - o prefab do jogo tem "
                          "preto alfa 0.5 com a keyword desligada e offset/dilate 0 (sombra inerte)")

    criterio = soma_criterio_de_sombra(src)
    if criterio is None:
        falhas.append("nao achei o criterio de sombra DE VERDADE (%s): sem ele, ou a sombra de "
                      "verdade deixa de ser transportada, ou a inerte volta a ser acesa"
                      % SOMBRA_DESENHADA.strip())
    else:
        if 'IsKeywordEnabled("UNDERLAY_ON")' not in criterio:
            falhas.append("%s nao pergunta a keyword UNDERLAY_ON" % SOMBRA_DESENHADA.strip())
        for prop in PROPS_GEOMETRIA_SOMBRA:
            if prop not in criterio:
                falhas.append("%s nao olha `%s`: a sombra de VERDADE (deslocamento/expansao) "
                              "deixaria de ser transportada" % (SOMBRA_DESENHADA.strip(), prop))

    if PADRAO_SOMBRA_POR_COR.search(bf.sem_comentarios(src)):
        falhas.append("o fonte ainda decide sombra por `_UnderlayColor.a > 0` (sem keyword): a "
                      "sombra INERTE do prefab volta a acender o UNDERLAY_ON - a 'sombra muito "
                      "grossa' do 'Select Attributes'")
    return falhas


# ===========================================================================
# 6) AS MUTACOES (o defeito plantado) - usadas pelos testes EM MEMORIA
# ===========================================================================
# Cada uma devolve o texto do fonte com UM defeito. Se nao achar onde agir, devolve o
# fonte intacto - e o teste REPROVA dizendo que a mutacao nao encontrou o trecho (isso e
# defeito do plantio, nao prova de nada).

def _troca(texto, alvo, novo):
    if alvo not in texto:
        return texto
    return texto.replace(alvo, novo, 1)


def defeito_escape_como_gate(texto=None):
    """O portao volta a olhar a CLASSIFICACAO do texto (`estilizado`), nao o efeito."""
    src = fonte() if texto is None else texto
    return _troca(src, "if (efeitoPresente &&", "if (estilizado &&")


def defeito_escape_sem_continue(texto=None):
    """O ramo do ESCAPE deixa de dar `continue`: o texto pulado seria tocado."""
    src = fonte() if texto is None else texto
    return _troca(src, 'null, TipoLinhaDiag.Escape);\n                            }\n                            continue;',
                  'null, TipoLinhaDiag.Escape);\n                            }')


def defeito_recusa_por_shader(texto=None):
    """O BF-1 de volta: variante de shader diferente e RECUSA (o defeito corrigido)."""
    src = fonte() if texto is None else texto
    alvo = "                if (!transporteLigado)"
    defeito = ('                if (antigo.shader != padraoNovo.shader)\n'
               '                {\n'
               '                    motivo = "shader incompativel";\n'
               '                    return false;\n'
               '                }\n\n'
               '                if (!transporteLigado)')
    return _troca(src, alvo, defeito)


def defeito_sem_glow(texto=None):
    """A falha-segura deixa de barrar GLOW_ON."""
    src = fonte() if texto is None else texto
    alvo = ('                if (antigo.IsKeywordEnabled("GLOW_ON"))\n'
            '                {\n'
            '                    motivo = "GLOW_ON ligado — glow nao e transportado";\n'
            '                    return false;\n'
            '                }\n\n')
    return _troca(src, alvo, "")


def defeito_facetex_sem_textura_de_efeito(texto=None):
    """`_FaceTex` volta a contar por EXISTIR (o default embutido vira 'efeito')."""
    src = fonte() if texto is None else texto
    return _troca(src,
                  'if (antigo.HasProperty("_FaceTex") && TexturaDeEfeito(antigo.GetTexture("_FaceTex")))',
                  'if (antigo.HasProperty("_FaceTex"))')


def defeito_copia_gradient_scale(texto=None):
    """A copia passa a transportar `_GradientScale` (parametro do atlas NOVO)."""
    src = fonte() if texto is None else texto
    return _troca(src, '"_FaceDilate",', '"_FaceDilate", "_GradientScale",')


def defeito_sem_underlay_on(texto=None):
    """A keyword UNDERLAY_ON deixa de ser ligada (a sombra para de aparecer)."""
    src = fonte() if texto is None else texto
    return _troca(src, 'novo.EnableKeyword("UNDERLAY_ON");', '')


def defeito_sombra_por_alfa(texto=None):
    """PLANTA o defeito do BF-5: a COR (alfa) volta a acender a sombra, sem olhar a keyword.

    E o estado anterior ao conserto: `bool sombraAtiva` decidido por `_UnderlayColor.a > 0.001`
    (mesmo com `UNDERLAY_ON` desligado e offset/dilate zero), que liga o UNDERLAY_ON no material
    novo e faz aparecer a 'sombra muito grossa' do 'Select Attributes'.
    """
    src = fonte() if texto is None else texto
    alvo = "            bool sombraAtiva = SombraDesenhada(antigo);"
    defeito = ('            bool sombraAtiva = antigo.IsKeywordEnabled("UNDERLAY_ON") ||\n'
               '                               antigo.IsKeywordEnabled("UNDERLAY_INNER") ||\n'
               '                               (antigo.HasProperty("_UnderlayColor") && '
               'antigo.GetColor("_UnderlayColor").a > 0.001f);')
    return _troca(src, alvo, defeito)


def defeito_default_escape_true(texto=None):
    """`PularTextosEstilizados` volta ao default antigo (`true`) - o escape vira o padrao."""
    src = fonte() if texto is None else texto
    return _troca(src,
                  'PularTextosEstilizados = BindSeguro("Estilo", "PularTextosEstilizados", false,',
                  'PularTextosEstilizados = BindSeguro("Estilo", "PularTextosEstilizados", true,')


def defeito_default_preservar_false(texto=None):
    """`PreservarEstilo` volta a `false` (a troca de fonte apaga o estilo)."""
    src = fonte() if texto is None else texto
    return _troca(src,
                  'PreservarEstilo = BindSeguro("Estilo", "PreservarEstilo", true,',
                  'PreservarEstilo = BindSeguro("Estilo", "PreservarEstilo", false,')


def defeito_getter_pular_inseguro(texto=None):
    """O getter de `PularTextosEstilizados` deixa de cair no conservador sem config."""
    src = fonte() if texto is None else texto
    return _troca(src,
                  "get { return PularTextosEstilizados == null || PularTextosEstilizados.Value; }",
                  "get { return PularTextosEstilizados != null && PularTextosEstilizados.Value; }")


def defeito_acopla_outro_mod(texto=None):
    """O CODIGO do BetterFont passa a citar o nome E o GUID do outro mod (o invariante 3)."""
    src = fonte() if texto is None else texto
    return _troca(src, "        internal static ManualLogSource Log { get; private set; }",
                  "        internal static ManualLogSource Log { get; private set; }\n"
                  "        // acoplado ao BetterCombatText (DefRuivo_StolenRealmMods-BetterCombatText)")


def defeito_sem_padding(texto=None):
    """O caminho do texto NORMAL deixa de recalcular o padding (contorno cortado)."""
    src = fonte() if texto is None else texto
    return _troca(src, "                                    t.UpdateMeshPadding();", "")


def defeito_sem_fallback(texto=None):
    """`RegistrarFallback` deixa de adicionar a fonte original (icones viram quadradinho)."""
    src = fonte() if texto is None else texto
    return _troca(src, "_serifFont.fallbackFontAssetTable.Add(t.font);", "")
