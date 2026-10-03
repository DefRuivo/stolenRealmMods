#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A SOMBRA TEM DE CONTRASTAR COM A LETRA (BCT-4) - a lei do contraste.

O DEFEITO RELATADO (dono, 02/10, a SEGUNDA rodada)
--------------------------------------------------
O nome do inimigo tem a letra CLARA e ela e o `#CBB396` (highlightedColor/specialDescColor do
jogo). O BCT-3 dava a essa letra a sombra CLARA `#CBB396` - a MESMA cor da letra. O log de 02/10
(l.3359) mostra os dois numeros: `cor da LETRA no alvo='#CBB396' (luminancia 0.717 -> letra CLARA);
sombra que FICOU no material=_UnderlayColor '#CBB396 alfa=0.35'`. Sombra igual a letra = contraste
ZERO (invisivel, ou um "blob").

A LEI (BCT-4)
-------------
O que determina a sombra VISIVEL e o contraste com a LETRA (o glyph esta encostado na sombra) E com
o FUNDO (a sombra cai sobre ele):

    POLARIDADE (BCT-3): fundo ESCURO -> sombra CLARA; fundo CLARO -> sombra ESCURA;
                        auto -> pela LETRA (BCT-2).
    LEI (BCT-4):        se a cor do balde escolhido NAO contrastar com a LETRA
                        (diferenca de luminancia < `ContrasteMinimo`), o balde VIRA.
    VETO (BCT-5):       a sombra tem de ficar do LADO OPOSTO da luminancia da letra - fonte
                        CLARA -> sombra ESCURA; fonte ESCURA -> sombra CLARA. A proposta do FUNDO
                        cai quando poe a sombra do mesmo lado da fonte.

A sombra CLARA e o BRANCO PURO (`#FFFFFF`): o `#CBB396` era a PROPRIA cor de texto do jogo e a
cor comum do nome do inimigo. MESMO com o branco, o LIMIAR do BCT-4 nao bastava: #CBB396 contra
#FFFFFF difere so 0.283 (>= 0.2, "passava") e a sombra saia CLARA sobre uma fonte CLARA - o
"sombra na mesma cor da fonte" do dono. Por isso o BCT-5 decide pelo LADO, nao pelo limiar: o
nome do inimigo (letra CLARA) ganha a sombra ESCURA `#000000`, que CONTRASTA com a fonte.

O INVARIANTE QUE ESTE TESTE PROVA
---------------------------------
Para TODA cor da paleta do jogo (a fixture, nunca digitada) e TODO valor de `Fundo`, a sombra
escolhida fica do LADO OPOSTO da letra e contrasta com ela (>= `ContrasteMinimo`). A regra ANTES
do BCT-4 viola o invariante no caso relatado: `#CBB396` -> sombra `#CBB396` (contraste 0).

COMO ESTE TESTE E PROVADO REPROVANDO
------------------------------------
1. O MODELO do defeito (`ModeloFundoDaSombraAntes`) devolve `#CBB396` para a letra `#CBB396` em
   fundo escuro - contraste zero (a isca tem de reprovar o invariante).
2. No FONTE, `defeito_sombra_sem_contraste_com_a_letra` (tira a guarda que VIRA o balde) e
   `defeito_cor_sombra_clara_volta_cbb396` (poe o #CBB396 de volta) reprovam
   `falhas_do_contraste_da_letra`.
"""
import regras_bct as reg

import arcabouco as arc

META = {
    "nome": "bct-sombra-contraste-letra",
    "categoria": "pura",
    "requer": [],
    "descricao": "BCT-4/BCT-5: a sombra CONTRASTA com a LETRA - ela fica do LADO OPOSTO da "
                 "luminancia da fonte (fonte CLARA -> sombra ESCURA; fonte ESCURA -> sombra CLARA) "
                 "em toda a paleta e em todo Fundo; o nome do inimigo (#CBB396, letra CLARA) ganha "
                 "a sombra ESCURA #000000, nunca uma sombra clara 'da mesma cor da fonte'",
}


def corpo():
    paleta = reg.paleta_do_jogo()
    arc.exigir(paleta is not None, "nao achei a fixture da paleta (%s)" % reg.FIXTURE_CORES)
    cores = paleta["guimanager"]["cores"]
    fundos = (reg.FUNDO_ESCURO, reg.FUNDO_CLARO, reg.FUNDO_AUTO)

    # ------------------------------------------------ 1) O CASE RELATADO (o log de 02/10)
    letra_bege = cores["highlightedColor"]      # #CBB396 - a cor do nome do inimigo
    sombra = reg.sombra_para(letra_bege, reg.FUNDO_ESCURO)
    arc.exigir(sombra != letra_bege,
               "a sombra do nome do inimigo (%s) nao pode ser a PROPRIA cor da letra (%s)"
               % (sombra, letra_bege))
    arc.igual(sombra, reg.SOMBRA_ESCURA,
              "letra bege %s (CLARA) em qualquer fundo -> sombra ESCURA (#%s), que CONTRASTA com a "
              "fonte (BCT-5)" % (letra_bege, reg.SOMBRA_ESCURA))
    arc.exigir(reg.contraste_com_a_letra(letra_bege, sombra) >= reg.CONTRASTE_MINIMO,
               "a sombra #%s tem de CONTRASTAR com a letra #%s (>= %s)"
               % (sombra, letra_bege, reg.CONTRASTE_MINIMO))

    # ------------------------------------------------ 2) O INVARIANTE: TODA cor x TODO fundo
    violacoes = []
    for nome in sorted(cores):
        hex_letra = cores[nome].lstrip("#")
        for fundo in fundos:
            hex_sombra = reg.sombra_para(hex_letra, fundo)
            c = reg.contraste_com_a_letra(hex_letra, hex_sombra)
            if c < reg.CONTRASTE_MINIMO:
                violacoes.append("%s (%s) fundo=%s -> sombra #%s (contraste %.3f)"
                                 % (nome, hex_letra, fundo, hex_sombra, c))
    arc.exigir(not violacoes,
               "%d violacao(oes) da LEI do contraste (a sombra da propria cor da letra): %s"
               % (len(violacoes), " | ".join(violacoes)))

    # A cor de letra que COLIDE com o branco (o proprio branco) faz a lei VIRAR o balde.
    arc.igual(reg.sombra_para(cores["physicalColor"], reg.FUNDO_ESCURO), reg.SOMBRA_ESCURA,
              "letra BRANCA + fundo escuro: a sombra clara branca daria contraste zero -> o balde "
              "vira para a ESCURA")

    # A POLARIDADE do fundo so vale quando NAO contradiz a fonte (veto da letra, BCT-5).
    arc.igual(reg.sombra_para(cores["highlightedColor"], reg.FUNDO_ESCURO), reg.SOMBRA_ESCURA,
              "letra CLARA #CBB396: mesmo declarando fundo ESCURO, o veto da letra (BCT-5) da a "
              "sombra ESCURA - clara-sobre-clara era o defeito relatado")
    arc.igual(reg.sombra_para(cores["highlightedColor"], reg.FUNDO_CLARO), reg.SOMBRA_ESCURA,
              "fundo CLARO -> sombra ESCURA (BCT-3), que aqui tambem e o lado oposto da letra")

    # ------------------------------------------------ 3) a ISCA (o defeito ANTES do BCT-4) reprova
    ruim = reg.ModeloFundoDaSombraAntes()
    arc.igual(ruim.sombra(letra_bege, reg.FUNDO_ESCURO), reg.SOMBRA_CLARA_ANTIGA,
              "isca: a regra ANTES do BCT-4 devolve #%s - a MESMA cor da letra #%s"
              % (reg.SOMBRA_CLARA_ANTIGA, letra_bege))
    arc.exigir(reg.contraste_com_a_letra(letra_bege,
                                         ruim.sombra(letra_bege, reg.FUNDO_ESCURO))
               < reg.CONTRASTE_MINIMO,
               "isca: a sombra do defeito nao contrasta com a letra - a isca REPROVA o invariante")

    # ------------------------------------------------ 4) o FONTE (a lei no C#)
    cfg = reg.fonte(reg.CFG)
    styler = reg.fonte(reg.STYLER)
    arc.exigir(len(cfg) > 3000 and len(styler) > 3000,
               "Configuracao.cs/TextStyler.cs vieram vazios: a leitura mudou de lugar?")

    falhas = reg.falhas_do_contraste_da_letra(cfg, styler)
    arc.exigir(not falhas, "a lei do contraste caiu: %s" % " | ".join(falhas))

    # -------------------------------- 5) CONTRA-PROVA no FONTE (os defeitos plantados REPROVAM)
    for rotulo, plantar, marca in (
            ("o VETO DA LETRA arrancado (a letra clara ganha sombra clara)",
             reg.defeito_sombra_sem_contraste_com_a_letra, "VETO DA LETRA"),
            ("a sombra clara de volta no #CBB396 (a cor da propria letra)",
             reg.defeito_cor_sombra_clara_volta_cbb396, "CorSombraClara")):
        com_defeito = plantar(cfg)
        arc.exigir(com_defeito != cfg, "o plantio do defeito nao achou onde agir (%s)" % rotulo)
        falhas_defeito = reg.falhas_do_contraste_da_letra(com_defeito, styler)
        arc.exigir(falhas_defeito, "as checagens PASSARAM com o defeito plantado (%s): o teste nao "
                                   "vigia nada" % rotulo)
        arc.exigir(any(marca in f for f in falhas_defeito),
                   "o defeito (%s) nao foi acusado no ponto certo (%s): %s"
                   % (rotulo, marca, " | ".join(falhas_defeito)))

    print("lei do contraste: %d cor(es) da paleta x %d fundo(s) - a sombra SEMPRE contrasta com a "
          "letra (>= %.2f); o caso relatado #%s + fundo escuro -> sombra #%s (o #%s antigo era a "
          "mesma cor da letra); 2 defeito(s) plantado(s) reprovam"
          % (len(cores), len(fundos), reg.CONTRASTE_MINIMO, letra_bege, sombra,
             reg.SOMBRA_CLARA_ANTIGA))


if __name__ == "__main__":
    arc.main(META, corpo)
