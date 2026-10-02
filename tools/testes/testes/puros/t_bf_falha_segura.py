#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A MATRIZ DA FALHA-SEGURA do BetterFont, caso a caso (TST-7, cenario 2).

O QUE ESTE TESTE GARANTE
------------------------
O BF-1 prometeu: "so se troca a fonte de um texto com efeito se o que esta EM USO nele
puder ser reproduzido no material novo - uma copia parcial sairia PIOR que nao mexer". A
conferencia disso e `EstiloTransportavel`. Este teste exige que CADA caso da matriz leve a
`nao-tocar`:

    _FaceTex   (textura de face de verdade)      -> nao-tocar
    _BumpMap   (bevel de verdade)                -> nao-tocar
    GLOW_ON                                      -> nao-tocar
    BEVEL_ON                                     -> nao-tocar
    contorno em uso que o material novo nao expoe -> nao-tocar
    sombra em uso que o material novo nao expoe   -> nao-tocar

O ESCOPO CORRIGIDO DEPOIS DO BF-2: "shader diferente do material da serifa" NAO esta mais
nesta lista. O BF-1 recusava por variante de shader - e era exatamente isso que deixava os
textos de combate (que usam `Distance Field Overlay`/`(Surface)`, medido em
`tools/fixtures/bf-shaders-em-jogo.log`) na fonte original. No BF-2 a variante diferente
virou copia BEST-EFFORT propriedade por propriedade: este teste exige que o texto com
shader diferente e efeito transportavel seja CONVERTIDO, e que `EstiloTransportavel` NAO
pergunte o shader.

E o falso positivo que teria mantido o defeito de pe: `_FaceTex`/`_BumpMap` so contam como
efeito quando a textura e DE VERDADE. O default dessas propriedades no shader e a textura
embutida `white`/`bump` do Unity, que `GetTexture` devolve diferente de null mesmo sem
efeito nenhum. `TexturaDeEfeito` tem de distinguir os dois.

O QUE RODA E O QUE NAO RODA
---------------------------
`Material` e nativo do Unity. O que roda e a TRANSCRICAO da conferencia
(`regras_bf_estilo.estilo_transportavel` + `textura_de_efeito`) e `falhas_da_falha_segura`,
que amarra a transcricao ao fonte vivo. Cada defeito e plantado EM MEMORIA e as checagens
TEM de reprovar - pelo motivo certo. A rodada fisica (plantar no `Plugin.cs`, ver
REPROVOU; restaurar, ver PASSOU) esta em `tools/testes/bf-prova-reprovando.log`.

O que NAO se prova aqui: o efeito visual em combate - isso e tela, e so o dono confirma.
"""
import regras_bf_estilo as reg

import arcabouco as arc

META = {
    "nome": "bf-falha-segura",
    "categoria": "pura",
    "requer": [],
    "descricao": "TST-7: a matriz da falha-segura (caso a caso -> nao-tocar) e o shader diferente, que no BF-2 deixou de ser recusa",
}

MATERIAL_NOVO_OK = {"_OutlineWidth": True, "_UnderlaySoftness": True}


def corpo():
    src = reg.fonte()
    arc.exigir(len(src) > 5000, "o fonte do BetterFont veio vazio/curto: a leitura mudou de lugar?")

    # ---- 1) a matriz seca: cada efeito irreproduzivel leva a nao-tocar, PELO MOTIVO CERTO.
    for rotulo, ajuste, motivo in reg.MATRIZ_FALHA_SEGURA:
        mat = dict(ajuste)
        transportavel, motivo_obtido = reg.estilo_transportavel(mat, True, MATERIAL_NOVO_OK)
        arc.exigir(transportavel is False,
                   "o material com %s tinha de REPROVAR a falha-segura (nao-tocar)" % rotulo)
        arc.exigir(motivo in (motivo_obtido or ""),
                   "o material com %s reprovou pela razao ERRADA: esperado mencionar %r, veio %r"
                   % (rotulo, motivo, motivo_obtido))
    # os dois casos que so reprovam quando o material NOVO nao expoe a propriedade.
    for rotulo, ajuste, expoe_parcial, motivo in reg.MATRIZ_NAO_EXPOE:
        transportavel, motivo_obtido = reg.estilo_transportavel(dict(ajuste), True, expoe_parcial)
        arc.exigir(transportavel is False,
                   "o caso '%s' tinha de REPROVAR a falha-segura (nao-tocar)" % rotulo)
        arc.exigir(motivo in (motivo_obtido or ""),
                   "o caso '%s' reprovou pela razao ERRADA: esperado %r, veio %r"
                   % (rotulo, motivo, motivo_obtido))

    # ---- 2) o falso positivo: o DEFAULT do shader (white/bump) NAO e efeito.
    for default in ("white", "bump", None):
        mat = {"face_tex": default, "bump_map": default}
        transportavel, motivo = reg.estilo_transportavel(mat, True, MATERIAL_NOVO_OK)
        arc.exigir(transportavel is True,
                   "o default de textura do shader (%r) foi contado como EFEITO: a falha-segura "
                   "recusaria todo material de SDF (o falso positivo que teria mantido o defeito "
                   "de pe); motivo=%r" % (default, motivo))
    arc.exigir(reg.textura_de_efeito("real") is True, "textura de verdade tem de contar como efeito")
    arc.exigir(reg.textura_de_efeito(None) is False, "ausencia de textura nao e efeito")

    # ---- 3) ESCOPO CORRIGIDO: shader diferente NAO e recusa.
    mat_shader = {"shader_diferente": True}
    transportavel, motivo = reg.estilo_transportavel(mat_shader, True, MATERIAL_NOVO_OK)
    arc.exigir(transportavel is True,
               "shader diferente voltou a REPROVAR a falha-segura: e o defeito do BF-1 (os textos "
               "de combate ficam na fonte original); motivo=%r" % motivo)
    caso_combate = reg.Texto("combate (shader diferente) com efeito", shader_diferente=True,
                             efeito_presente=True, efeito=reg.TRANSPORTAVEL)
    arc.igual(reg.decidir(caso_combate), reg.CONVERTE_COM_TRANSPORTE,
              "o texto de combate com efeito transportavel tem de ser convertido com transporte")

    # ---- 4) o efeito barrado tambem leva a nao-tocar NA DECISAO (a matriz e o que a decisao usa).
    for rotulo, ajuste, _ in reg.MATRIZ_FALHA_SEGURA:
        mat = dict(ajuste)
        transportavel, _ = reg.estilo_transportavel(mat, True, MATERIAL_NOVO_OK)
        texto = reg.Texto(rotulo, material_proprio=True, efeito_presente=True,
                          efeito=reg.TRANSPORTAVEL if transportavel else reg.NAO_TRANSPORTAVEL)
        arc.igual(reg.decidir(texto), reg.NAO_TOCAR,
                  "a decisao para o texto com %s tinha de ser nao-tocar" % rotulo)
    for rotulo, ajuste, expoe_parcial, _ in reg.MATRIZ_NAO_EXPOE:
        transportavel, _ = reg.estilo_transportavel(dict(ajuste), True, expoe_parcial)
        texto = reg.Texto(rotulo, material_proprio=True, efeito_presente=True,
                          efeito=reg.TRANSPORTAVEL if transportavel else reg.NAO_TRANSPORTAVEL)
        arc.igual(reg.decidir(texto), reg.NAO_TOCAR,
                  "a decisao para o texto com %s tinha de ser nao-tocar" % rotulo)

    # ---- 5) a ligacao com o FONTE VIVO.
    falhas = reg.falhas_da_falha_segura(src)
    arc.exigir(not falhas, "a falha-segura do fonte regrediu em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))

    # ---- 6) CONTRA-PROVAS: os defeitos plantados TEM de reprovar, cada um pelo seu motivo.
    plantados = (
        ("a recusa por variante de shader (o defeito do BF-1)",
         reg.defeito_recusa_por_shader, ("shader",)),
        ("a falha-segura deixando de barrar GLOW_ON",
         reg.defeito_sem_glow, ("GLOW_ON",)),
        ("_FaceTex contando por EXISTIR (o default do shader virando efeito)",
         reg.defeito_facetex_sem_textura_de_efeito, ("TexturaDeEfeito",)),
    )
    for rotulo, plantar, motivos in plantados:
        com_defeito = plantar(src)
        arc.exigir(com_defeito != src, "o plantio do defeito (%s) nao achou onde agir" % rotulo)
        falhas_defeito = reg.falhas_da_falha_segura(com_defeito)
        arc.exigir(falhas_defeito, "as checagens PASSARAM num fonte com o defeito (%s): a "
                                    "verificacao nao vale nada" % rotulo)
        for motivo in motivos:
            arc.exigir(any(motivo in f for f in falhas_defeito),
                       "o defeito (%s) nao e pego pelo motivo esperado (%r): %s"
                       % (rotulo, motivo, " | ".join(falhas_defeito)))

    print("matriz da falha-segura: %d caso(s) seco(s) + %d que dependem do material novo reprovam e "
          "levam a nao-tocar; o default de textura do shader nao e efeito; shader diferente NAO e "
          "recusa (o texto de combate converte); %d defeito(s) plantado(s) reprovam pelo motivo certo"
          % (len(reg.MATRIZ_FALHA_SEGURA), len(reg.MATRIZ_NAO_EXPOE), len(plantados)))


if __name__ == "__main__":
    arc.main(META, corpo)
