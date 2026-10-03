#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A POSICAO DO CONTAINER DE NOS — os nos NAO caem no rodape/corte (RSTV-19).

O QUE ISTO TRAVA
----------------
Achado medido: os nos da aba 'All Trees' caiam no RODAPE e eram cortados pela borda. O container
`RstvNodeContainer` estava posicionado com o `(0, 26.7)` do 'Skill Item Container' NATIVO, mas em
relacao ao centro da `RstvTreeArea` — que NAO e o centro da janela. A area comeca
`AlturaDaBarraDeClasses + 4` abaixo do topo do painel, e o painel abaixo da barra de abas; o centro
da area fica ~64.25u ABAIXO do centro da janela, entao o (0, 26.7) cru jogava os nos 64.25u baixo
demais e o tier 5 encostava no rodape.

AS CONTAS (modelo puro, conferido contra a JANELA VIVA)
-------------------------------------------------------
CanvasScaler 1920x1080 escala 1.8 -> canvas 1066.(6) x 600; janela [3942] = 593.8 de altura; barra
[762] = ap 11.2 / altura 53.7. O modelo tem de REPRODUZIR a area logada na janela viva
(`area da arvore 1050.7x449.3 px`) — e essa conferencia prova que o modelo le a geometria certa.

DE ONDE VEM O ESPERADO
----------------------
As regras vivem em `tools/testes/regras_rstv19.py`; o fonte e lido AO VIVO do mod (nunca copia). O
plantio `fonte_sem_deslocamento` reinjeta a posicao CRUA (centro da AREA) no MESMO fonte, em memoria,
e as MESMAS checagens tem de REPROVAR. O que NAO se prova aqui (e so o dono confirma, em tela): os
nos desenharem na posicao relativa da referencia.
"""
import regras_rstv19 as reg

import arcabouco as arc

META = {
    "nome": "rstv19-posicao-nos",
    "categoria": "pura",
    "requer": [],
    "descricao": ("RSTV-19: o container dos nos e posicionado no centro da JANELA + 26.7 (como o "
                  "'Skill Item Container' nativo), nao no centro da area ~64u abaixo — sem a "
                  "compensacao os nos caem no rodape (folga < meio no) e a checagem REPROVA"),
}


def _perto(obtido, esperado, rotulo, tol=0.5):
    arc.exigir(abs(obtido - esperado) <= tol,
               "%s: esperado ~%.2f, obtido %.3f" % (rotulo, esperado, obtido))


def corpo():
    src = reg.fonte(reg.caminho_aba())
    arc.exigir(len(src) > 1000, "o SkillTreesTab.cs veio vazio/curto: a leitura mudou de lugar?")

    # 1) O FONTE: a compensacao (centro da JANELA), nao o (0, 26.7) cru no centro da AREA.
    falhas = reg.falhas_da_posicao(src)
    arc.exigir(not falhas, "a posicao do container regrediu em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))

    # 2) AS CONSTANTES do fonte (geometria do painel).
    margem_superior = reg.le_const(src, "MargemSuperior")
    margem_inferior = reg.le_const(src, "MargemInferior")
    margem_lateral = reg.le_const(src, "MargemLateral")
    altura_classes = reg.le_const(src, "AlturaDaBarraDeClasses")
    y_nativo = reg.le_const(src, "YDoContainerDeNos")
    escala = reg.le_const(src, "EscalaDoContainerDeNos")
    for valor, nome in ((margem_superior, "MargemSuperior"), (margem_inferior, "MargemInferior"),
                        (margem_lateral, "MargemLateral"),
                        (altura_classes, "AlturaDaBarraDeClasses"),
                        (y_nativo, "YDoContainerDeNos"), (escala, "EscalaDoContainerDeNos")):
        arc.exigir(valor is not None, "nao consegui ler `%s` do SkillTreesTab.cs" % nome)
    _perto(y_nativo, reg.Y_NATIVO, "o YDoContainerDeNos (o (0, 26.7) do nativo)")
    _perto(escala, reg.ESCALA_NATIVA, "a EscalaDoContainerDeNos")

    # 3) O MODELO REPRODUZ A JANELA VIVA: a area logada e 1050.7 x 449.3.
    _perto(reg.largura_da_area(margem_lateral), reg.AREA_LOG[0],
           "a largura da area do modelo (conferencia contra o Player.log)")
    _perto(reg.altura_da_area(margem_superior, margem_inferior, altura_classes), reg.AREA_LOG[1],
           "a altura da area do modelo (conferencia contra o Player.log)")

    # 4) COM a compensacao o container cai no MESMO lugar relativo do nativo (centro da janela + 26.7).
    centro_com = reg.centro_do_container(True, margem_superior, margem_inferior, altura_classes)
    _perto(centro_com, reg.Y_NATIVO,
           "o centro do container (tem de ser o centro da JANELA + YDoContainerDeNos)")
    arc.exigir(reg.deslocamento_do_centro(margem_superior, margem_inferior, altura_classes) > 40.0,
               "a compensacao saiu pequena demais para haver regressao de posicao: o modelo nao "
               "esta lendo a area abaixo do topo do painel")

    # 5) OS NOS VISIVEIS: o tier 5 sobra MEIO NO (24u) acima da borda de baixo (nao cortado), e o
    #    topo do tier 1 fica ABAIXO do topo da area (nao escondido atras da barra de classes).
    for vp in (reg.VP_LOG, reg.VP_PADRAO):
        folga = reg.folga_acima_do_rodape(centro_com, vp, escala, margem_inferior)
        arc.exigir(folga >= reg.MARGEM_MINIMA,
                   "com o padding vertical %.0f o fundo do no fica a %.1fu do rodape — menos que "
                   "meio no (%.0fu) de folga: o no aparece cortado" % (vp, folga, reg.MARGEM_MINIMA))
        arc.exigir(reg.topo_do_no(centro_com, escala) <
                   reg.topo_da_area_y(margem_superior, altura_classes),
                   "o topo do no (%.1fu) NAO esta abaixo do topo da area (%.1fu)"
                   % (reg.topo_do_no(centro_com, escala),
                      reg.topo_da_area_y(margem_superior, altura_classes)))

    # 6) O DEFEITO (centro da AREA, sem compensacao) TEM de cair no rodape: se tambem ficasse visivel,
    #    a checagem nao distinguiria nada.
    centro_sem = reg.centro_do_container(False, margem_superior, margem_inferior, altura_classes)
    _perto(centro_sem, centro_com - reg.deslocamento_do_centro(margem_superior, margem_inferior,
                                                               altura_classes),
           "o modelo do defeito (centro da area) nao bate com o deslocamento medido")
    pior = min(reg.folga_acima_do_rodape(centro_sem, vp, escala, margem_inferior)
               for vp in (reg.VP_LOG, reg.VP_PADRAO))
    arc.exigir(pior < reg.MARGEM_MINIMA,
               "o DEFEITO (sem o deslocamento) tambem daria folga %.1fu >= %.0fu — a checagem nao "
               "reprova o defeito" % (pior, reg.MARGEM_MINIMA))

    # 7) PROVA DE FOGO NO FONTE: com a posicao CRUA plantada, as checagens REPROVAM pelo motivo certo.
    defeito = reg.fonte_sem_deslocamento(src)
    arc.exigir(defeito != src,
               "o plantio do defeito nao encontrou a ancora (a linha do `DeslocamentoDoCentroDaArea` "
               "+ YDoContainerDeNos): a checagem nao le o trecho certo")
    falhas_defeito = reg.falhas_da_posicao(defeito)
    arc.exigir(len(falhas_defeito) >= 1 and any("rodape" in f or "DeslocamentoDoCentroDaArea" in f
                                                for f in falhas_defeito),
               "as checagens PASSARAM (ou reprovaram por outro motivo) com a posicao crua no centro "
               "da area: %s" % " | ".join(falhas_defeito))

    print("RSTV-19: o container dos nos cai no centro da JANELA + %.1fu (deslocamento da area "
          "= +%.2fu); o tier 5 sobra >= %.1fu acima da borda de baixo (visivel) e o DEFEITO "
          "(centro da AREA) REPROVA (folga %.1fu < meio no)."
          % (reg.Y_NATIVO, reg.deslocamento_do_centro(margem_superior, margem_inferior, altura_classes),
             min(reg.folga_acima_do_rodape(centro_com, vp, escala, margem_inferior)
                 for vp in (reg.VP_LOG, reg.VP_PADRAO)), pior))


if __name__ == "__main__":
    arc.main(META, corpo)
