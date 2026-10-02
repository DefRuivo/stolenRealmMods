#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A PRECONDICAO DO SHADER (TST-8, cenario 7): confirmar a capacidade antes de aplicar.

O QUE ESTE TESTE GARANTE
------------------------
O contorno/halo e a sombra do TextMeshPro dependem de DUAS coisas no material: a PROPRIEDADE
(`_OutlineWidth`, `_UnderlaySoftness`) e a VARIANTE DE SHADER que as usa. O material dos
textos de combate e distance field - o diagnostico do proprio mod mediu, em jogo, os nomes
(`tools/fixtures/bf-shaders-em-jogo.log`, versionado):

    NOME DO INIMIGO (hover)   shader=TextMeshPro/Distance Field Overlay
    NOME DO INIMIGO (chefe)   shader=TextMeshPro/Distance Field Overlay
    Tooltip.Title             shader=TextMeshPro/Distance Field
    NUMERO NA FACE DO DADO    shader=TextMeshPro/Distance Field (Surface)

Sao TRES variantes diferentes - o que prova que decidir pelo NOME do shader e errado. O que o
mod tem de fazer e CONFIRMAR a precondicao pela CAPACIDADE, e so entao aplicar:

    bool ehDistanceField = mat.HasProperty("_OutlineWidth");
    bool temUnderlay     = mat.HasProperty("_UnderlaySoftness");
    if (cfg.HaloAtivo.Value) { if (ehDistanceField) { ...aplica... } else { ...avisa... } }

O teste vigia que (a) a confirmacao existe e GOVERNAR o ramo (`if (ehDistanceField)`), (b) ela
vem ANTES da escrita das propriedades, (c) a decisao NAO e pelo nome do shader, e (d) quando a
precondicao falha o mod AVISA (por superficie, uma vez) em vez de ficar em silencio.

A rodada fisica (o ramo aplicando sem confirmar, e a decisao passando para o nome do shader, o
teste reprovando, o fonte restaurado byte a byte) esta em `tools/testes/bct-prova-reprovando.log`.
"""
import regras_bct as reg

import arcabouco as arc

META = {
    "nome": "bct-precondicao-shader",
    "categoria": "pura",
    "requer": [],
    "descricao": "TST-8/7: o efeito confirma a precondicao do shader (HasProperty _OutlineWidth/_UnderlaySoftness) antes de aplicar, em vez de confiar por nome/variante",
}

ALVO_DO_DIAGNOSTICO = "TextMeshPro/Distance Field"


def corpo():
    styler = reg.fonte(reg.STYLER)
    arc.exigir(len(styler) > 3000, "o TextStyler.cs veio vazio/curto: a leitura mudou de lugar?")

    falhas = reg.falhas_da_precondicao(styler)
    arc.exigir(not falhas, "a precondicao regrediu: %s" % " | ".join(falhas))

    # A medicao versionada: as superficies alvo SAO distance field (e de variantes diferentes).
    medidos = reg.shaders_medidos()
    if not medidos:
        raise arc.Falhou("nao achei a medicao de shaders em %s (o diagnostico ja provou que a "
                         "variante Distance Field existe)" % reg.SHADER_LOG)
    arc.exigir(any(ALVO_DO_DIAGNOSTICO in s for s in medidos),
               "a medicao em jogo nao tem nenhum shader '%s': a precondicao do cenario mudou"
               % ALVO_DO_DIAGNOSTICO)
    arc.exigir(len(set(medidos)) > 1,
               "a medicao em jogo deveria mostrar VARIANTES diferentes dos textos de combate "
               "(e o motivo de nao decidir pelo NOME do shader): %s" % sorted(set(medidos)))

    # Contra-provas no fonte.
    nao_confere = reg.defeito_precondicao_nao_confere(styler)
    arc.exigir(nao_confere != styler, "o plantio do defeito (aplicar sem confirmar) nao achou onde agir")
    falhas_a = reg.falhas_da_precondicao(nao_confere)
    arc.exigir(falhas_a, "as checagens PASSARAM com o ramo aplicando sem confirmar a precondicao")
    arc.exigir(any("ehDistanceField" in f for f in falhas_a),
               "o defeito nao foi acusado na precondicao certa: %s" % " | ".join(falhas_a))

    por_nome = reg.defeito_precondicao_por_nome(styler)
    arc.exigir(por_nome != styler, "o plantio do defeito (decidir pelo nome) nao achou onde agir")
    falhas_b = reg.falhas_da_precondicao(por_nome)
    arc.exigir(falhas_b, "as checagens PASSARAM decidindo pelo NOME do shader")
    arc.exigir(any("nome do shader" in f.lower() for f in falhas_b),
               "o defeito 'decidir pelo nome' nao foi acusado como tal: %s" % " | ".join(falhas_b))

    print("precondicao confirmada por `HasProperty(\"_OutlineWidth\")`/`(\"_UnderlaySoftness\")` "
          "ANTES de aplicar, e o ramo governado por ela; medicao versionada (%s) com %d shader(s): "
          "%s; 2 defeito(s) plantado(s) reprovam"
          % (reg.SHADER_LOG, len(set(medidos)), sorted(set(medidos))))


if __name__ == "__main__":
    arc.main(META, corpo)
