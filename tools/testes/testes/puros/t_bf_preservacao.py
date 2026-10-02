#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A LISTA DE PRESERVACAO do BetterFont: o que VAI e o que NAO VAI (TST-7, cenario 3).

O QUE ESTE TESTE GARANTE
------------------------
Quando o BetterFont troca a fonte, `CopiarEstilo` leva o ESTILO do material antigo para o
material por componente da fonte nova. Este teste tem DUAS listas explicitas - uma que
PRECISA estar copiada/ligada, outra que NAO pode ser copiada - e confere as duas contra o
fonte vivo. Se alguem "melhorar" a copia e passar a transportar o que pertence a fonte
nova, o teste reprova.

LISTA 1 - PRECISA SER TRANSPORTADO (o estilo do texto):
  cores:    _FaceColor, _OutlineColor, _UnderlayColor
  floats:   _FaceDilate, _OutlineWidth, _OutlineSoftness,
            _UnderlayOffsetX/Y, _UnderlayDilate, _UnderlaySoftness,   (o contorno e a sombra)
            _VertexOffsetX/Y, _MaskSoftnessX/Y                          (buracos fechados no BF-2)
  vetor:    _ClipRect                                                  (recorte de texto mascarado/rolavel)
  keywords: OUTLINE_ON, UNDERLAY_ON   <- sao ELAS que ligam contorno e sombra no shader
            (mais UNDERLAY_INNER e MASK_SOFT/HARD/TEX)

LISTA 2 - NAO PODE SER TRANSPORTADO (pertence a FONTE/atlas NOVA, ou e efeito que a copia
nao reproduz e por isso o texto inteiro e deixado intacto):
  _MainTex, _GradientScale, _TextureWidth, _TextureHeight, _ScaleRatio_*,
  _FaceTex, _BumpMap, _WeightNormal, _WeightBold, GLOW_ON, BEVEL_ON.

O que fica de fora POR PROPOSITO tem de ser NOMEADO no log (`perdidos`/`registros`) - nada
pode passar em branco para quem le o diagnostico.

DE ONDE VEM A VERDADE
---------------------
Nao ha lista digitada: os GRUPOS (`PropsCor`, `PropsFloat`, `PropsVetor`, `KeywordsMascara`,
`PropsDeFonteRegistradas`) e as CHAMADAS do `CopiarEstilo` sao lidos do fonte vivo. Os
defeitos plantados EM MEMORIA (passar a copiar `_GradientScale`; nao ligar `UNDERLAY_ON`)
TEM de reprovar. A rodada fisica esta em `tools/testes/bf-prova-reprovando.log`.
"""
import regras_bf_estilo as reg

import arcabouco as arc

META = {
    "nome": "bf-preservacao",
    "categoria": "pura",
    "requer": [],
    "descricao": "TST-7: as duas listas do BetterFont - o que CopiarEstilo transporta (cores, contorno, sombra, offsets e as keywords OUTLINE_ON/UNDERLAY_ON) e o que NAO pode transportar (atlas, _GradientScale, _FaceTex, _BumpMap, GLOW_ON, BEVEL_ON)",
}


def corpo():
    src = reg.fonte()
    arc.exigir(len(src) > 5000, "o fonte do BetterFont veio vazio/curto: a leitura mudou de lugar?")

    efetiva = reg.copia_efetiva(src)

    # ---- LISTA 1: o que PRECISA estar copiado/ligado, lido do fonte.
    for nome_grupo, props in reg.PRECISA_COPIAR.items():
        lista = efetiva["grupos"].get(nome_grupo)
        arc.exigir(lista is not None, "o grupo `%s` sumiu do fonte" % nome_grupo)
        arc.exigir(nome_grupo in efetiva["grupos_ativos"],
                   "o grupo `%s` NAO e percorrido por um Set em CopiarEstilo: nada dele e transportado"
                   % nome_grupo)
        for prop in props:
            arc.exigir(prop in lista, "`%s` saiu do grupo %s: uma propriedade de ESTILO deixou de "
                                      "ser transportada" % (prop, nome_grupo))
    for keyword in ("OUTLINE_ON", "UNDERLAY_ON"):
        arc.exigir(keyword in efetiva["keywords"],
                   "a keyword `%s` deixou de ser LIGADA: sem ela contorno/sombra NAO aparecem no "
                   "shader (copiar o valor nao basta)" % keyword)
    arc.exigir("UNDERLAY_INNER" in efetiva["keywords"], "UNDERLAY_INNER deixou de ser transportada")
    for keyword in ("MASK_SOFT", "MASK_HARD", "MASK_TEX"):
        arc.exigir(keyword in efetiva["keywords_grupo"],
                   "a keyword de recorte `%s` deixou de ser transportada" % keyword)

    # ---- LISTA 2: o que NAO pode ser copiado.
    proibidas = reg.propriedades_proibidas_presentes(src)
    arc.exigir(not proibidas,
               "a copia passou a transportar o que pertence a FONTE NOVA / a um efeito "
               "irreproduzivel: %s" % ", ".join(sorted(proibidas)))
    # e o que fica de fora tem de ser NOMEADO no log.
    copiar = reg.copiar_corpo(src) or ""
    for prop in ("_FaceTex", "_BumpMap", "GLOW_ON", "BEVEL_ON", "_GradientScale"):
        arc.exigir(prop in copiar, "`%s` nao e copiado NEM nomeado no log: ficaria em branco" % prop)
    pesos = reg.grupo(src, reg.GRUPO_PROPS_FONTE) or []
    for prop in ("_WeightNormal", "_WeightBold"):
        arc.exigir(prop in pesos, "`%s` nao esta no grupo dos parametros da fonte registrados "
                                  "(nao e copiado NEM logado)" % prop)

    # ---- a checagem consolidada (a mesma lista, sobre o fonte vivo).
    falhas = reg.falhas_da_preservacao(src)
    arc.exigir(not falhas, "a lista de preservacao regrediu em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))

    # ---- CONTRA-PROVAS EMBUTIDAS.
    com_gradient = reg.defeito_copia_gradient_scale(src)
    arc.exigir(com_gradient != src, "o plantio da copia de `_GradientScale` nao achou onde agir")
    falhas_gradient = reg.falhas_da_preservacao(com_gradient)
    arc.exigir(any("_GradientScale" in f and "FONTE NOVA" in f for f in falhas_gradient),
               "a copia passando a transportar `_GradientScale` (parametro do atlas novo) passou: %s"
               % " | ".join(falhas_gradient))

    sem_underlay = reg.defeito_sem_underlay_on(src)
    arc.exigir(sem_underlay != src, "o plantio do UNDERLAY_ON ausente nao achou onde agir")
    falhas_underlay = reg.falhas_da_preservacao(sem_underlay)
    arc.exigir(any("UNDERLAY_ON" in f for f in falhas_underlay),
               "a keyword UNDERLAY_ON deixando de ser ligada passou (a sombra para de aparecer): %s"
               % " | ".join(falhas_underlay))

    print("lista 1 (transportada): %d propriedade(s) nos %d grupos ativos + keywords %s; "
          "lista 2 (NAO transportada): %s - todas nomeadas no log; %d defeito(s) plantado(s) reprovam"
          % (sum(len(v) for v in efetiva["grupos_ativos"].values()),
             len(efetiva["grupos_ativos"]),
             ",".join(efetiva["keywords"] + efetiva["keywords_grupo"]),
             ",".join(reg.NAO_PODE_COPIAR), 2))


if __name__ == "__main__":
    arc.main(META, corpo)
