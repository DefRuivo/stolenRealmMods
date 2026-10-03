#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A SOMBRA FANTASMA do BetterFont (BF-5): so acender o UNDERLAY_ON com sombra DE VERDADE.

O DEFEITO (o achado do BCT-4, leitura do prefab com UnityPy)
------------------------------------------------------------
O rotulo 'SectionLabelText' do 'Select Attributes' (TMP no GO 'Label' [680588]) usa o material
'Regular Font (Minion Pro Regular) SDF Material', que traz `_UnderlayColor` preto ALFA 0.5,
`_UnderlayOffsetX/Y`/`_UnderlayDilate`/`_UnderlaySoftness` = 0 e o keyword `UNDERLAY_ON`
DESLIGADO (`m_ValidKeywords == []`). E uma sombra INERTE que o jogo NUNCA desenha. O
`CopiarEstilo` considerava "sombra em uso" por `_UnderlayColor.a > 0.001` (SEM olhar a keyword),
LIGAVA o `UNDERLAY_ON` no material novo e copiava os valores: aparecia uma sombra que o jogo
nunca renderizou - a "sombra muito grossa" relatada pelo dono. (`AcceptButtonText`, do mesmo
prefab, expoe o mesmo padrao com o 'Title Font'.)

O CONSERTO (BF-5)
-----------------
A sombra so esta ATIVA se o shader a DESENHA: a keyword (`UNDERLAY_ON`/`UNDERLAY_INNER`) ligada,
OU offset/dilate != 0 (a geometria que faz a sombra aparecer). A cor `_UnderlayColor` continua
sendo TRANSPORTADA como valor de estilo - o que muda e ela NAO decidir a keyword sozinha.

COMO ESTE TESTE E PROVADO REPROVANDO
------------------------------------
1. A LEI no fonte vivo: `falhas_da_sombra_inerte` (o defeito nao pode existir em ponto nenhum do
   codigo efetivo - portao, criterio de efeito e copia de estilo).
2. O CONTROLE POSITIVO: as duas coisas que FAZEM a sombra aparecer (a keyword e offset/dilate)
   continuam olhadas, senao o conserto vira "nunca transportar sombra".
3. A CONTRA-PROVA EMBUTIDA: `defeito_sombra_por_alfa` planta `_UnderlayColor.a > 0.001` EM MEMORIA
   (mesmo com a keyword desligada) e a checagem TEM de reprovar.
"""
import regras_bf_estilo as reg

import arcabouco as arc

META = {
    "nome": "bf-sombra-inerte",
    "categoria": "pura",
    "requer": [],
    "descricao": "BF-5: o CopiarEstilo so liga UNDERLAY_ON se a fonte tinha a keyword ou "
                 "offset/dilate != 0 - a sombra INERTE do 'Select Attributes' (cor com alfa, "
                 "keyword UNDERLAY_ON desligada e offset/dilate 0) nao volta a acender",
}


def corpo():
    src = reg.fonte()
    arc.exigir(len(src) > 5000,
               "o fonte do BetterFont veio vazio/curto: a leitura mudou de lugar?")

    # 1) A LEI no fonte vivo.
    falhas = reg.falhas_da_sombra_inerte(src)
    arc.exigir(not falhas, "a sombra fantasma voltou em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))

    # 2) CONTROLE POSITIVO: as duas coisas que fazem a sombra aparecer continuam olhadas.
    criterio = reg.soma_criterio_de_sombra(src)
    arc.exigir(criterio is not None,
               "nao achei o criterio de sombra DE VERDADE (`%s`) no fonte"
               % reg.SOMBRA_DESENHADA.strip())
    criterio = criterio or ""
    arc.exigir('IsKeywordEnabled("UNDERLAY_ON")' in criterio,
               "o criterio de sombra nao pergunta a keyword UNDERLAY_ON: a sombra de verdade "
               "(com a keyword ligada) deixaria de ser transportada")
    for prop in reg.PROPS_GEOMETRIA_SOMBRA:
        arc.exigir(prop in criterio,
                   "o criterio de sombra nao olha `%s`: a sombra de verdade (deslocamento/"
                   "expansao) deixaria de ser transportada" % prop)

    # 3) A CONTRA-PROVA EMBUTIDA: o defeito plantado (alfa>0 no lugar da keyword/geometria) REPROVA.
    com_defeito = reg.defeito_sombra_por_alfa(src)
    arc.exigir(com_defeito != src,
               "o plantio do defeito nao achou onde agir (`bool sombraAtiva = ...`)")
    falhas_defeito = reg.falhas_da_sombra_inerte(com_defeito)
    arc.exigir(falhas_defeito,
               "as checagens PASSARAM num fonte com a sombra ligada por `_UnderlayColor.a > 0` "
               "(keyword desligada): a trava nao vigia nada - e o defeito do BF-5")
    arc.exigir(any(("COR" in f) or ("_UnderlayColor" in f) for f in falhas_defeito),
               "o defeito nao foi acusado no ponto certo (a COR decidindo a sombra): %s"
               % " | ".join(falhas_defeito))

    print("sombra de verdade: keyword UNDERLAY_ON/UNDERLAY_INNER OU offset/dilate != 0; a cor "
          "`_UnderlayColor` sozinha NAO acende a sombra; o defeito plantado (alfa>0) reprova")


if __name__ == "__main__":
    arc.main(META, corpo)
