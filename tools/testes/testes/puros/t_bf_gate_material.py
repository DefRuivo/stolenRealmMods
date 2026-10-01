#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O PORTAO DE MATERIAL DO BETTERFONT (BF-2): o conserto do BF-1 esta de pe no FONTE.

O QUE ESTE TESTE GARANTE
------------------------
A revisao independente refutou o BF-1 com uma prova simples: o material dos textos de
combate do jogo usa OUTRA variante de shader (medido em jogo e versionado em
`tools/fixtures/bf-shaders-em-jogo.log`: `TextMeshPro/Distance Field Overlay` no nome do
inimigo e `Distance Field (Surface)` no numero do dado, contra `Mobile/Distance Field` da
fonte serifada). O gate do BF-1 recusava por shader diferente e o texto ficava na fonte
original - ou seja, o conserto nao consertava o caso que ele mira. Pior: era regressao,
porque antes esses textos ERAM convertidos com copia best-effort guardada por HasProperty.

Este teste le o `BetterFont/Plugin.cs` VIVO (nao uma copia - a expectativa fica amarrada ao
que sera compilado) e confere a ESTRUTURA da decisao consertada, que e o que da para
verificar sem abrir o jogo (Material e classe nativa do Unity, nao se instancia em teste):
variante de shader nao recusada; gate pelo efeito presente no material; fonte e estilo
mudando juntos com reversao; buracos de propriedade fechados; defaults intactos; zero
acoplamento com outro mod **no codigo** (a trava varre o `Plugin.cs`; o `README` cita o
`BetterCombatText` de proposito, para explicar a convivencia - e isso e desejado).

DE ONDE VEM O ESPERADO
----------------------
As regras vivem em `tools/testes/regras_bf.py`, extraidas do proprio conserto; a isca
`tools/testes/contra-prova/cp_bf_gate_shader.py` reinjeta o defeito do BF-1 e MOSTRA estas
checagens reprovando - sem essa metade, uma checagem que passa por construcao seria
decoracao. O que NAO se prova aqui (e so o dono confirma, em tela): o nome do inimigo e o
numero do dado ganharem a serifa e o halo.
"""
import regras_bf

import arcabouco as arc

META = {
    "nome": "bf-gate-material",
    "categoria": "pura",
    "requer": [],
    "descricao": "BF-2: variante de shader nao e recusa, gate pelo efeito no material, fonte+estilo juntos e buracos fechados",
}


def corpo():
    src = regras_bf.fonte()
    arc.exigir(len(src) > 5000, "o fonte do BetterFont veio vazio/curto: a leitura mudou de lugar?")

    falhas = regras_bf.falhas_da_fonte(src)
    arc.exigir(not falhas, "o fonte do BetterFont regrediu em %d ponto(s): %s" % (len(falhas), " | ".join(falhas)))

    # Contra-prova embutida: as MESMAS checagens tem de reprovar num fonte com o defeito do
    # BF-1 reinjetado (a recusa por variante de shader). Se isto passar, a checagem acima e
    # vacuidade, nao verificacao.
    com_defeito = regras_bf.fonte_com_o_defeito_do_bf1(src)
    arc.exigir(com_defeito != src, "o plantio do defeito do BF-1 nao encontrou onde agir: a checagem "
                                   "nao esta lendo o trecho certo do fonte")
    falhas_defeito = regras_bf.falhas_da_fonte(com_defeito)
    arc.exigir(len(falhas_defeito) >= 1,
               "as checagens passaram num fonte COM a recusa por shader do BF-1: elas nao pegam o defeito")
    arc.exigir(any("shader" in f for f in falhas_defeito),
               "a checagem reprovou o defeito, mas nao por shader: %s" % " | ".join(falhas_defeito))

    # O segundo defeito plantado (gate pela classificacao do texto, em vez do efeito).
    com_gate_antigo = regras_bf.fonte_com_o_defeito_do_gate(src)
    arc.exigir(com_gate_antigo != src, "o plantio do gate antigo nao encontrou onde agir")
    falhas_gate = regras_bf.falhas_da_fonte(com_gate_antigo)
    arc.exigir(len(falhas_gate) >= 1,
               "as checagens passaram num fonte cujo portao volta a olhar a classificacao do texto")

    print("gate sem recusa por variante de shader, pelo efeito no material, com reversao: "
          "%d checagem(ns) sobre o fonte vivo; %d defeito(s) plantado(s) reprovam"
          % (1, 2))


if __name__ == "__main__":
    arc.main(META, corpo)
