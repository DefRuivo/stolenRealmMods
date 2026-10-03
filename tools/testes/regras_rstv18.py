#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rstv18.py - RSTV-18: a escala x1.7 do container NATIVO ('Skill Item Container') nos NOS.

O QUE ESTA BIBLIOTECA TRAVA (lida do FONTE vivo, nunca de copia)
----------------------------------------------------------------
Achado medido (2 agentes): os NOS da aba 'All Trees' saiam PEQUENOS — 46px de tela contra ~78px da
referencia, razao x1.70. A causa esta no PREFAB: o nativo coloca os nos DENTRO do
`Skill Item Container` (level1, 'Skill Tree Window Roguelike' > GO 490738), um RectTransform 1000x800
com localScale (1.7, 1.7, 1.7). O no e o `Skill Tree Item Active` 30x30 com localScale 0.9 ->
30 x 0.9 x 1.7 = 45.9u efetivo. O mod reimplementou o layout SEM esse container e desenhava
30 x 0.9 x 1.0 = 27u. O pitch tambem escala junto (47 x 1.7 = 79.9u horizontal, 33 x 1.7 = 56.1u
vertical — os paddings vem do `SkillTreeManager` em runtime, l.177207).

1. A ESCALA: `EscalaDoContainerDeNos` tem de ser 1.7 (o DEFEITO plantado e 1.0 = sem o container).
2. O CONTAINER: `GarantirContainerDeNos` cria/acha o `RstvNodeContainer` com `localScale` nessa
   escala, `sizeDelta (1000, 800)`, `anchoredPosition (0, 26.7)` — os numeros do prefab nativo.
3. OS NOS VIVEM NO CONTAINER: `Popular` instancia o `skillTreeItemActivePrefab` em `paiDeNos`
   (= `_containerDeNos`); a area (`_areaDaArvore`, escala 1) fica so para as linhas de dependencia.
4. AS CONTAS (modelo puro): no_efetivo(escala) = 30 x 0.9 x escala; pitch_horizontal(escala, hp) =
   hp x escala; pitch_vertical(escala, vp) = vp x escala.

A funcao de PLANTIO devolve o MESMO fonte com a escala do container reinjetada em 1.0, em memoria.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import recorte as rec

# Os numeros do prefab (medidos, nao estimados).
ESCALA_NATIVA = 1.7
LADO_DO_NO = 30.0      # 'Skill Tree Item Active' RectTransform (30x30)
ESCALA_DO_NO = 0.9     # localScale do no no prefab
HP = 47.0              # nodeHorizontalPadding
VP = 33.0              # tierVerticalPadding (valor lido do manager em runtime)

NO_DE_REFERENCIA = LADO_DO_NO * ESCALA_DO_NO * ESCALA_NATIVA   # 45.9u

# Assinaturas exatas lidas do fonte. Se um nome mudar, a checagem REPROVA dizendo qual sumiu.
GARANTIR = "private static RectTransform GarantirContainerDeNos(RectTransform area)"
POPULAR = "internal static void Popular(SkillType tipo)"
LINHAS = "private static void DesenharLinhasDeDependencia()"


# ------------------------------------------------------------------ caminhos ---

def _dir_mod():
    return os.path.join(arc.raiz_do_repo(), "RoguelikeSkillTreeVisualizer")


def caminho_aba():
    return os.path.join(_dir_mod(), "SkillTreesTab.cs")


def fonte(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def _efetivo(src):
    return rec.codigo_efetivo(src)


def _corpo(src, assinatura):
    return rec.corpo_do_metodo(_efetivo(src), assinatura)


# ------------------------------------------------------------- modelos puros ---

def no_efetivo(escala):
    """O tamanho do no em unidades do canvas: RectTransform x localScale do no x escala do container."""
    return LADO_DO_NO * ESCALA_DO_NO * escala


def pitch_horizontal(escala, hp=HP):
    """O passo entre colunas: o padding horizontal x a escala do container."""
    return hp * escala


def pitch_vertical(escala, vp=VP):
    """O passo entre tiers: o padding vertical x a escala do container."""
    return vp * escala


def escala_do_container(src):
    """Le a constante `EscalaDoContainerDeNos` do fonte (o valor que o container recebe)."""
    m = re.search(r"EscalaDoContainerDeNos\s*=\s*([0-9]+(?:\.[0-9]+)?)f", _efetivo(src))
    return float(m.group(1)) if m else None


# ------------------------------------------------------------------ checagens ---

def falhas_dos_nos(src_tab):
    """Defeitos da escala do container dos nos no FONTE. Lista vazia = a escala nativa esta de pe."""
    falhas = []
    efetivo = _efetivo(src_tab)

    # 1) A CONSTANTE: 1.7 (o 'Skill Item Container' nativo). 1.0 = o DEFEITO (sem o container).
    escala = escala_do_container(src_tab)
    if escala is None:
        falhas.append("nao achei a constante `EscalaDoContainerDeNos` no SkillTreesTab.cs — sem ela "
                      "nao ha a escala x1.7 do 'Skill Item Container'")
    elif abs(escala - ESCALA_NATIVA) > 1e-6:
        falhas.append("a escala do container dos nos e %.2fx — o 'Skill Item Container' NATIVO e "
                      "1.7x (o no sairia %.1fu em vez de %.1fu, e o pitch %.1fu em vez de %.1fu)"
                      % (escala, no_efetivo(escala), no_efetivo(ESCALA_NATIVA),
                         pitch_horizontal(escala), pitch_horizontal(ESCALA_NATIVA)))

    # 2) O CONTAINER: criado/achado por NOME, com o RectTransform e a escala do prefab.
    container = _corpo(src_tab, GARANTIR)
    if container is None:
        falhas.append("nao achei %s no SkillTreesTab.cs" % GARANTIR)
    else:
        if "localScale" not in container or "EscalaDoContainerDeNos" not in container:
            falhas.append("GarantirContainerDeNos nao aplica `localScale` com a escala nativa do container")
        for trecho, rotulo in (("NodeContainerName", "o nome idempotente do container"),
                               ("sizeDelta", "o RectTransform do container (1000x800)"),
                               ("anchoredPosition", "o deslocamento do container (0, 26.7)"),
                               ("SetParent", "o container criado sob a area dos nos")):
            if trecho not in container:
                falhas.append("GarantirContainerDeNos nao faz %s (trecho %r)" % (rotulo, trecho))

    # 3) OS NOS VIVEM NO CONTAINER (nao na area crua).
    popular = _corpo(src_tab, POPULAR)
    if popular is None:
        falhas.append("nao achei %s no SkillTreesTab.cs" % POPULAR)
    else:
        if "_containerDeNos" not in popular:
            falhas.append("Popular NAO usa `_containerDeNos` — os nos continuam na area crua, sem a escala 1.7")
        if "paiDeNos = _containerDeNos" not in popular:
            falhas.append("Popular nao escolhe o container como pai dos nos (`paiDeNos = _containerDeNos ...`)")
        if "Instantiate(gui.skillTreeItemActivePrefab, paiDeNos)" not in popular:
            falhas.append("Popular nao instancia o no em `paiDeNos` — o no fica sem o frame x1.7")

    # 4) AS LINHAS continuam no IRMAO sem escala (senao dobrariam o 1.7).
    linhas = _corpo(src_tab, LINHAS)
    if linhas is None:
        falhas.append("nao achei %s no SkillTreesTab.cs" % LINHAS)
    elif "SetParent(_areaDaArvore, false)" not in linhas:
        falhas.append("as linhas de dependencia nao ficam no irmao sem escala (`_areaDaArvore`) — elas "
                      "entrariam no frame x1.7 e dobrariam a escala")

    return falhas


# ------------------------------------------------------------ plantio de defeitos ---

_ANCORA_ESCALA = "EscalaDoContainerDeNos = 1.7f"
_DEFEITO_ESCALA = "EscalaDoContainerDeNos = 1.0f"


def fonte_com_escala_1(src=None):
    """O MESMO fonte com a escala do container em 1.0 (o DEFEITO: layout sem o frame nativo)."""
    texto = fonte(caminho_aba()) if src is None else src
    if _ANCORA_ESCALA not in texto:
        return texto
    return texto.replace(_ANCORA_ESCALA, _DEFEITO_ESCALA, 1)
