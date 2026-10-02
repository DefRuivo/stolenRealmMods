#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O CAMINHO LEGADO DO BETTERCOMBATTEXT (TST-8, cenario 5): UI.Text recebe contorno DURO.

O QUE ESTE TESTE GARANTE
------------------------
Os rotulos "xN" e o contador de turnos dos icones de buff/debuff NAO sao TextMeshPro: sao
`UnityEngine.UI.Text` legado (o tipo real, medido em jogo pelo proprio diagnostico do mod:
"tipo REAL do rotulo de stack = 'UnityEngine.UI.Text'"). Esse texto desenha com atlas de
BITMAP: nao ha material distance field, nao ha `_OutlineWidth` - halo SUAVE e impossivel ali.
O que EXISTE e o contorno DURO do Unity: o componente `Outline` (BaseMeshEffect, 4 copias
deslocadas) e o `Shadow`.

Entao o caminho legado tem de:
  * usar `AddComponent<Outline>` / `AddComponent<Shadow>` com `effectColor`/`effectDistance`;
  * NAO tocar em material nenhum (`fontMaterial`, `fontSharedMaterial`, `_OutlineWidth`,
    `_UnderlaySoftness`, `EnableKeyword`, `new Material`, `Set*`) - isso seria pedir um efeito
    que o tipo nao tem, e o mod ficaria "tentando" algo inexistente;
  * guardar o caso do GameObject com outro Graphic ANTES do Text (o BaseMeshEffect age no
    PRIMEIRO Graphic - contornar o elemento errado e pior que nao contornar);
  * ser ligado de verdade aos rotulos de stack/turno, pelo TIPO real
    (`TextStyler.AplicarTextoLegado(icone.stackCount, ...)`).

A rodada fisica (o caminho legado passando a pedir material SDF, o teste reprovando, o fonte
restaurado byte a byte) esta em `tools/testes/bct-prova-reprovando.log`.
"""
import regras_bct as reg

import arcabouco as arc

META = {
    "nome": "bct-caminho-legado",
    "categoria": "pura",
    "requer": [],
    "descricao": "TST-8/5: UI.Text legado recebe contorno DURO (Outline/Shadow) e o mod nao tenta material de distance field nos rotulos de status",
}


def corpo():
    styler = reg.fonte(reg.STYLER)
    patches = reg.fonte(reg.PATCHES)
    arc.exigir(len(styler) > 3000, "o TextStyler.cs veio vazio/curto: a leitura mudou de lugar?")

    falhas = reg.falhas_do_caminho_legado(styler) + reg.falhas_da_ligacao_legada(patches)
    arc.exigir(not falhas, "o caminho legado regrediu: %s" % " | ".join(falhas))

    # Contra-prova: o caminho legado passando a pedir material de distance field.
    com_defeito = reg.defeito_legado_usa_material(styler)
    arc.exigir(com_defeito != styler,
               "o plantio do defeito (legado pedindo material SDF) nao achou onde agir")
    falhas_defeito = reg.falhas_do_caminho_legado(com_defeito)
    arc.exigir(falhas_defeito, "as checagens PASSARAM com o caminho legado pedindo material SDF")
    arc.exigir(any("fontMaterial" in f for f in falhas_defeito),
               "o defeito nao foi acusado pelo material: %s" % " | ".join(falhas_defeito))

    # Contra-prova da ligacao: o patch dos rotulos tratando o stack como TMP.
    ligacao_errada = patches.replace("TextStyler.AplicarTextoLegado(icone.stackCount",
                                     "TextStyler.AplicarTmp(icone.stackCount", 1)
    arc.exigir(ligacao_errada != patches,
               "o plantio da ligacao errada (stack como TMP) nao achou onde agir")
    arc.exigir(reg.falhas_da_ligacao_legada(ligacao_errada),
               "as checagens PASSARAM com o stackCount tratado como TMP")

    legado = reg.corpo(styler, reg.APLICAR_LEGADO)
    print("caminho legado: %d caractere(s), contorno DURO por `Outline`/`Shadow` (effectColor/"
          "effectDistance), nenhum material SDF; ligado a `icone.stackCount`/`icone.turnCount`; "
          "2 defeito(s) plantado(s) reprovam" % len(legado or ""))


if __name__ == "__main__":
    arc.main(META, corpo)
