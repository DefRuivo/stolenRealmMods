#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rstv19.py - RSTV-19: a POSICAO do container de nos (nao cair no rodape/corte).

O QUE ESTA BIBLIOTECA TRAVA (lida do FONTE vivo, nunca de copia)
----------------------------------------------------------------
Achado medido: os nos da aba 'All Trees' caiam no RODAPE e eram cortados pela borda. A causa esta
no pai do container. O 'Skill Item Container' NATIVO (level1, 'Skill Tree Window' > GO 490738) e
filho DIRETO da JANELA do SkillTreeManager, ancorado no CENTRO dela, com `anchoredPosition (0, 26.7)`
(o centro cai 26.7u ACIMA do centro da janela). O mod poe o `RstvNodeContainer` dentro da
`RstvTreeArea`, cujo CENTRO nao e o centro da janela: a area comeca `AlturaDaBarraDeClasses + 4`
abaixo do topo do painel, e o painel comeca abaixo da barra de abas. Na janela viva o centro da area
fica ~64.25u ABAIXO do centro da janela — copiar o (0, 26.7) CRU para dentro da AREA joga os nos
64.25u baixo demais e o tier 5 encosta/atravessa o rodape.

1. A COMPENSACAO: `GarantirContainerDeNos` posiciona o container em
   `centro da JANELA + YDoContainerDeNos` (via `DeslocamentoDoCentroDaArea`), nao no centro da area.
2. AS CONTAS (modelo puro): centro do container (com) = 26.7; (sem, o DEFEITO) = centro_area + 26.7.
   O fundo do no = centro - 4*vp*escala - no_efetivo/2; a area = painel abaixo da barra de abas.

DE ONDE VEM O ESPERADO
----------------------
Os numeros da JANELA e da BARRA sao os do PREFAB/cena (medidos, nao estimados): CanvasScaler
1920x1080 escala 1.8 -> canvas 1066.(6) x 600; 'Character Menu Manager Window' [3942] sizeDelta.y =
-6.2; 'Menu Tab Manager' [762] anchoredPosition.y = 11.2 e altura 53.7. O modelo REPRODUZ a area
logada na janela viva (`area da arvore 1050.7x449.3 px` no Player.log) — e essa conferencia prova que
o modelo le a geometria certa.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import recorte as rec

# --------------------------------------------------------- numeros MEDIDOS ---
# CanvasScaler (1920x1080, scaleFactor 1.8) -> o canvas vive em unidades de 1066.(6) x 600.
CANVAS_LARGURA = 1066.67
CANVAS_ALTURA = 600.0
JANELA_SD_ALTURA = -6.2     # 'Character Menu Manager Window' [3942].m_SizeDelta.y
BARRA_AP_Y = 11.2           # 'Menu Tab Manager' [762].m_AnchoredPosition.y
BARRA_ALTURA = 53.7         # 'Menu Tab Manager' [762].m_SizeDelta.y
Y_NATIVO = 26.7             # 'Skill Item Container' [490738].m_AnchoredPosition.y
ESCALA_NATIVA = 1.7
LADO_DO_NO = 30.0           # 'Skill Tree Item Active' RectTransform 30x30
ESCALA_DO_NO = 0.9          # localScale do no no prefab
VP_LOG = 33.0               # tierVerticalPadding lido do manager na janela viva (log: "padding 47/33")
VP_PADRAO = 35.0            # SkillTreeManager.tierVerticalPadding padrao do prefab

# A AREA LOGADA na janela viva (EVIDENCIA): "area da arvore 1050.7x449.3 px".
AREA_LOG = (1050.7, 449.3)
# O no tem 45.9u: exigir pelo menos MEIO NO de folga acima da borda de baixo = "visivel, nao cortado".
MARGEM_MINIMA = 24.0

GARANTIR = "private static RectTransform GarantirContainerDeNos(RectTransform area)"
DESLOCAMENTO = "private static float DeslocamentoDoCentroDaArea(RectTransform area)"


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


def le_const(src, nome):
    """Le uma constante `private const float Nome = 12.3f` do fonte (o valor, nao o texto)."""
    m = re.search(nome + r"\s*=\s*(-?[0-9]+(?:\.[0-9]+)?)f", _efetivo(src))
    return float(m.group(1)) if m else None


# ------------------------------------------------------------- modelos puros ---

def topo_da_janela_y():
    return (CANVAS_ALTURA + JANELA_SD_ALTURA) / 2.0


def base_da_janela_y():
    return -topo_da_janela_y()


def largura_da_janela():
    return CANVAS_LARGURA


def topo_do_painel_y(margem_superior):
    """O topo do painel: a base da barra de abas menos a MargemSuperior (PainelAbaixoDaBarra)."""
    base_da_barra = topo_da_janela_y() + BARRA_AP_Y - BARRA_ALTURA
    return base_da_barra - margem_superior


def base_do_painel_y(margem_inferior):
    return base_da_janela_y() + margem_inferior


def topo_da_area_y(margem_superior, altura_classes):
    return topo_do_painel_y(margem_superior) - (altura_classes + 4.0)


def base_da_area_y(margem_inferior):
    return base_do_painel_y(margem_inferior)


def altura_da_area(margem_superior, margem_inferior, altura_classes):
    return topo_da_area_y(margem_superior, altura_classes) - base_da_area_y(margem_inferior)


def largura_da_area(margem_lateral):
    return largura_da_janela() - 2.0 * margem_lateral


def centro_da_area_y(margem_superior, margem_inferior, altura_classes):
    return (topo_da_area_y(margem_superior, altura_classes) + base_da_area_y(margem_inferior)) / 2.0


def deslocamento_do_centro(margem_superior, margem_inferior, altura_classes):
    """O quanto o centro da AREA esta abaixo do centro da JANELA (positivo = janela acima)."""
    return 0.0 - centro_da_area_y(margem_superior, margem_inferior, altura_classes)


def centro_do_container(com_deslocamento, margem_superior, margem_inferior, altura_classes):
    """O centro do container em coordenadas da JANELA (0 = centro da janela)."""
    centro = centro_da_area_y(margem_superior, margem_inferior, altura_classes)
    if com_deslocamento:
        centro += deslocamento_do_centro(margem_superior, margem_inferior, altura_classes)
    return centro + Y_NATIVO


def no_efetivo(escala):
    return LADO_DO_NO * ESCALA_DO_NO * escala


def fundo_do_no(centro_container, vp, escala):
    """A borda de BAIXO do tier mais fundo (o 5o), em coordenadas da janela."""
    return centro_container - 4.0 * vp * escala - no_efetivo(escala) / 2.0


def topo_do_no(centro_container, escala):
    return centro_container + no_efetivo(escala) / 2.0


def folga_acima_do_rodape(centro_container, vp, escala, margem_inferior):
    """Quanta folga sobra entre o fundo do no e a borda de baixo da AREA (negativo = cortado)."""
    return fundo_do_no(centro_container, vp, escala) - base_da_area_y(margem_inferior)


# ------------------------------------------------------------------ checagens ---

def falhas_da_posicao(src_tab):
    """Defeitos da POSICAO do container no FONTE. Lista vazia = a posicao nativa esta de pe."""
    falhas = []
    efetivo = _efetivo(src_tab)

    if DESLOCAMENTO not in efetivo:
        falhas.append("nao achei `%s` no SkillTreesTab.cs — sem ela nao ha como tirar a posicao "
                      "do centro da AREA e casar com o centro da JANELA (RSTV-19)" % DESLOCAMENTO)

    container = _corpo(src_tab, GARANTIR)
    if container is None:
        falhas.append("nao achei %s no SkillTreesTab.cs" % GARANTIR)
        return falhas

    if "YDoContainerDeNos" not in container:
        falhas.append("GarantirContainerDeNos nao usa `YDoContainerDeNos` (o 26.7 do 'Skill Item "
                      "Container' nativo)")
    if "DeslocamentoDoCentroDaArea" not in container:
        ms = le_const(src_tab, "MargemSuperior")
        mi = le_const(src_tab, "MargemInferior")
        ac = le_const(src_tab, "AlturaDaBarraDeClasses")
        desloc = (deslocamento_do_centro(ms, mi, ac)
                  if (ms is not None and mi is not None and ac is not None) else 64.25)
        falhas.append("GarantirContainerDeNos poe o container CRU em relacao ao centro da AREA "
                      "(o (0, 26.7) do nativo) — sem compensar que a area fica ~%.2fu ABAIXO do "
                      "centro da janela: os nos caem no rodape e sao cortados (RSTV-19)" % desloc)
    return falhas


# ------------------------------------------------------------ plantio de defeitos ---

_ANCORA_DESLOCAMENTO = ("container.anchoredPosition = new Vector2(0f, "
                        "DeslocamentoDoCentroDaArea(area) + YDoContainerDeNos);")
_DEFEITO_DESLOCAMENTO = "container.anchoredPosition = new Vector2(0f, YDoContainerDeNos);"


def fonte_sem_deslocamento(src=None):
    """O MESMO fonte com a posicao CRUA (o centro da AREA) — o DEFEITO do RSTV-19, em memoria."""
    texto = fonte(caminho_aba()) if src is None else src
    if _ANCORA_DESLOCAMENTO not in texto:
        return texto
    return texto.replace(_ANCORA_DESLOCAMENTO, _DEFEITO_DESLOCAMENTO, 1)
