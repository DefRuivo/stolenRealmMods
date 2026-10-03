#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A SOMBRA DO NOME DO INIMIGO TEM DE CONTRASTAR (BCT-3 + BCT-4).

O FUNDO manda a POLARIDADE da sombra; a LETRA manda a LEI do contraste.

O DEFEITO RELATADO (dono, 02/10) - duas rodadas
-----------------------------------------------
1. "nao ve NENHUMA sombra nos nomes de inimigo", num campo de batalha ESCURO -> BCT-3: o FUNDO
   manda (fundo escuro -> sombra clara), senao o preto some no campo.
2. Depois: a sombra do nome do inimigo ficou invisivel/"blob". O LOG de 02/10 (l.3359) diz por
   que: `cor da LETRA no alvo='#CBB396' (luminancia 0.717 -> letra CLARA); sombra que FICOU no
   material=_UnderlayColor '#CBB396 alfa=0.35'` -> a sombra CLARA era o #CBB396, a MESMA cor da
   letra: contraste ZERO -> BCT-4: a LETRA manda a LEI.

O QUE A INVESTIGACAO FECHOU (BCT-3)
-----------------------------------
1. A sombra ERA escrita. O log de 02/10 traz `[Nomes (combate)] APLICADO ... sombra=on` (l.3357)
   e NAO traz o aviso `sem-underlay` (que o `AvisoUma` imprime quando o shader nao expoe
   `_UnderlaySoftness`) - logo o ramo `temUnderlay` rodou e o `_UnderlayColor` foi escrito. O
   defeito nao e "nao escrever": e a COR.
2. A cor REAL da letra do nome do inimigo e CLARA: `PlayerInfoWindow.playerName.color` =
   `CharacterNameColor` (= `#` + `GetEnemyQualityColor(EnemyType)`) ou `Color.white`
   (l.156815/156849/156850); o `BossHealthbar.BossName` usa a cor do PREFAB (l.26641).
3. Pelo BCT-2 (sombra pela luminancia da LETRA), letra clara -> sombra `#000000`. Preto sobre o
   campo escuro = contraste ZERO: a sombra existe e nao aparece. Dai o BCT-3 (o FUNDO manda).

O DEFEITO QUE O BCT-4 CONSERTA
------------------------------
O BCT-3 assumia que a letra era ESCURA ao declarar fundo escuro - mas a letra do nome do inimigo e
CLARA e e o `#CBB396`, a MESMA cor da sombra clara do BCT-3. Sombra igual a letra = contraste zero.

A REGRA (BCT-3 + BCT-4 + BCT-5)
------------------------------
    POLARIDADE (BCT-3): fundo ESCURO -> sombra CLARA; fundo CLARO -> sombra ESCURA;
                        auto -> pela LETRA (regra do BCT-2, preservada).
    LEI (BCT-4):        a sombra tem de CONTRASTAR COM A LETRA (diferenca de luminancia
                        >= `ContrasteMinimo`); se a cor do balde escolhido nao contrastar, o
                        balde VIRA.
    VETO (BCT-5):       a sombra fica do LADO OPOSTO da luminancia da FONTE - fonte CLARA ->
                        sombra ESCURA; fonte ESCURA -> sombra CLARA. A proposta do FUNDO cai
                        quando poe a sombra do mesmo lado da letra.

Com a letra `#CBB396` (bege, o nome do inimigo) o VETO decide: mesmo em fundo escuro, a sombra
e a ESCURA `#000000` - ela CONTRASTA com a fonte clara. (O BCT-4 sozinho deixava a sombra CLARA
branca passar: bege #CBB396 x branco #FFFFFF difere 0.283, acima do limiar de 0.2 - clara sobre
clara, "a mesma cor da fonte".)

COMO ESTE TESTE E PROVADO REPROVANDO
------------------------------------
1. O MODELO da regra (`ModeloFundoDaSombra`) prova o comportamento puro; o MODELO do DEFEITO
   ANTES do BCT-4 (`ModeloFundoDaSombraAntes`) devolve `#CBB396` para a letra `#CBB396` em fundo
   escuro (contraste zero). A isca tem de reprovar.
2. No FONTE, `defeito_nomes_fundo_auto` e `defeito_sombra_ignora_fundo` devolvem o defeito
   plantado e `falhas_da_sombra_visivel` tem de acusar.
"""
import regras_bct as reg

import arcabouco as arc

META = {
    "nome": "bct-sombra-visivel-fundo-escuro",
    "categoria": "pura",
    "requer": [],
    "descricao": "BCT-3/BCT-4/BCT-5: o FUNDO propoe e a LETRA VETA - a letra bege #CBB396 (o "
                 "nome do inimigo), sendo CLARA, ganha a sombra ESCURA (#000000) que CONTRASTA com "
                 "a fonte, em qualquer fundo; nunca uma sombra clara (o #CBB396 ou o #FFFFFF do "
                 "BCT-4) 'da mesma cor da fonte'",
}


def corpo():
    paleta = reg.paleta_do_jogo()
    arc.exigir(paleta is not None, "nao achei a fixture da paleta (%s)" % reg.FIXTURE_CORES)
    cores = paleta["guimanager"]["cores"]

    # A letra do nome do inimigo e CLARA e e o bege #CBB396 (highlightedColor/specialDescColor) -
    # a cor do DEFEITO relatado. O branco da propria fixture (physicalColor) e a letra clara que
    # COLIDE com a sombra clara branca (prova a LEI quando nem o branco contrasta).
    letra_bege = cores["highlightedColor"]      # #CBB396 (0.717) - o nome do inimigo
    letra_branca = cores["physicalColor"]       # #FFFFFF (1.000)
    letra_escura = cores["shadowColor"]         # #F000FF (0.395) - a unica escura da paleta

    # ------------------------------------------------ 1) o MODELO do CONSERTO (regra pura)
    m = reg.ModeloFundoDaSombra()

    # O DEFEITO RELATADO: o bege #CBB396 em fundo escuro. A sombra tem de CONTRASTAR com a letra.
    sombra_bege = m.sombra(letra_bege, reg.FUNDO_ESCURO)
    arc.exigir(sombra_bege != letra_bege,
               "a sombra do nome do inimigo (%s) nao pode ser a PROPRIA cor da letra (%s)"
               % (sombra_bege, letra_bege))
    arc.igual(sombra_bege, reg.SOMBRA_ESCURA,
              "letra bege %s (CLARA) ganha a sombra ESCURA (#%s) - a sombra CONTRASTA com a fonte "
              "(BCT-5), nunca sai clara" % (letra_bege, reg.SOMBRA_ESCURA))
    arc.exigir(reg.contraste_com_a_letra(letra_bege, sombra_bege) >= reg.CONTRASTE_MINIMO,
               "a sombra tem de CONTRASTAR com a letra (diferenca de luminancia >= %s)"
               % reg.CONTRASTE_MINIMO)

    # letra ESCURA em fundo escuro: o branco contrasta -> sombra clara (o fundo manda a polaridade).
    arc.igual(m.sombra(letra_escura, reg.FUNDO_ESCURO), reg.SOMBRA_CLARA,
              "letra escura em FUNDO ESCURO tambem ganha a sombra CLARA (o fundo manda)")

    # A LEI segura o caso-limite: a letra BRANCA nao pode ganhar sombra branca -> o balde VIRA.
    arc.igual(m.sombra(letra_branca, reg.FUNDO_ESCURO), reg.SOMBRA_ESCURA,
              "letra BRANCA em fundo escuro NAO pode ganhar sombra BRANCA (contraste zero) - o "
              "balde vira para a ESCURA")

    # fundo CLARO: a polaridade e a escura; a letra clara contrasta com o preto.
    arc.igual(m.sombra(letra_bege, reg.FUNDO_CLARO), reg.SOMBRA_ESCURA,
              "letra clara em FUNDO CLARO ganha a sombra ESCURA")

    # AUTO preserva a regra do BCT-2 (o dono NAO mudou as outras superficies).
    arc.igual(m.sombra(letra_branca, reg.FUNDO_AUTO), reg.SOMBRA_ESCURA,
              "com o fundo NAO declarado (auto) vale a regra do BCT-2 (letra clara -> escura)")
    arc.igual(m.sombra(letra_escura, reg.FUNDO_AUTO), reg.SOMBRA_CLARA,
              "com o fundo NAO declarado (auto), letra escura -> sombra clara (BCT-2)")

    # ------------------------------------------------ 2) a ISCA (o defeito ANTES do BCT-4) reprova
    ruim = reg.ModeloFundoDaSombraAntes()
    arc.igual(ruim.sombra(letra_bege, reg.FUNDO_ESCURO), reg.SOMBRA_CLARA_ANTIGA,
              "isca: o defeito ANTES do BCT-4 devolve o #%s para a letra #%s em fundo escuro - a "
              "sombra IGUAL a letra" % (reg.SOMBRA_CLARA_ANTIGA, reg.SOMBRA_CLARA_ANTIGA))
    arc.exigir(reg.contraste_com_a_letra(letra_bege, ruim.sombra(letra_bege, reg.FUNDO_ESCURO))
               < reg.CONTRASTE_MINIMO,
               "isca: a sombra do defeito NAO contrasta com a letra (e o defeito relatado)")
    arc.exigir(ruim.sombra(letra_bege, reg.FUNDO_ESCURO) != sombra_bege,
               "isca: o MODELO do conserto tem de DIFERIR do defeito em fundo escuro (senao a "
               "checagem passaria por construcao)")

    # ------------------------------------------------ 3) o FONTE (as chaves + o codigo)
    cfg = reg.fonte(reg.CFG)
    styler = reg.fonte(reg.STYLER)
    arc.exigir(len(cfg) > 3000 and len(styler) > 3000,
               "Configuracao.cs/TextStyler.cs vieram vazios: a leitura mudou de lugar?")

    falhas = reg.falhas_da_sombra_visivel(cfg, styler)
    arc.exigir(not falhas, "a sombra visivel caiu: %s" % " | ".join(falhas))

    # A chave nova existe no .cfg e aceita os TRES valores (o default de cada superficie vem do
    # argumento `fundo:` da chamada do construtor, ja conferido em FUNDO_DAS_SUPERFICIES).
    arc.exigir(reg.FUNDO_BIND in cfg,
               "Configuracao.cs nao declara a chave 'Fundo' (`%s`)" % reg.FUNDO_BIND)
    for valor in reg.FUNDOS:
        arc.exigir('"%s"' % valor in cfg,
                   "Configuracao.cs nao cita o valor de fundo '%s' (a chave precisa aceitar "
                   "auto/escuro/claro)" % valor)

    # -------------------------------- 4) CONTRA-PROVA no FONTE (o defeito plantado REPROVA)
    for rotulo, plantar, marca in (
            ("o fundo das NOMES de volta em auto (a regra do BCT-2)",
             reg.defeito_nomes_fundo_auto, "Nomes"),
            ("a regra deixando de ligar FUNDO ESCURO a sombra clara",
             reg.defeito_sombra_ignora_fundo, "FUNDO ESCURO")):
        com_defeito = plantar(cfg)
        arc.exigir(com_defeito != cfg, "o plantio do defeito nao achou onde agir (%s)" % rotulo)
        falhas_defeito = reg.falhas_da_sombra_visivel(com_defeito, styler)
        arc.exigir(falhas_defeito, "as checagens PASSARAM com o defeito plantado (%s): o teste nao "
                                   "vigia nada" % rotulo)
        arc.exigir(any(marca in f for f in falhas_defeito),
                   "o defeito (%s) nao foi acusado no ponto certo (%s): %s"
                   % (rotulo, marca, " | ".join(falhas_defeito)))

    print("fundo+letra mandam: letra bege %s + fundo ESCURO -> sombra #%s (o conserto); a regra "
          "ANTES do BCT-4 dava #%s (a MESMA cor da letra); letra branca + fundo escuro -> #%s (a "
          "lei vira o balde); NOMES declara 'escuro', as outras superficies 'auto'; 2 defeito(s) "
          "plantado(s) reprovam"
          % (letra_bege, sombra_bege, reg.SOMBRA_CLARA_ANTIGA, reg.SOMBRA_ESCURA))


if __name__ == "__main__":
    arc.main(META, corpo)
