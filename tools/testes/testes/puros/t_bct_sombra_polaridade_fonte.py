#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A SOMBRA CONTRASTA COM A FONTE (BCT-5) - a POLARIDADE pela LETRA.

O REQUISITO DO DONO (02/10, a TERCEIRA rodada)
----------------------------------------------
"a sombra do nome do inimigo precisa CONTRASTAR com a fonte: fonte CLARA -> sombra ESCURA,
fonte ESCURA -> sombra CLARA, com as cores da paleta."

O DEFEITO QUE ESTE TESTE FECHA
------------------------------
O BCT-3 escolhia a sombra pelo FUNDO (fundo escuro -> sombra clara). A letra do nome do inimigo
e CLARA (`#CBB396`, `highlightedColor`/`specialDescColor`, luminancia 0.717): o fundo escuro
mandava a sombra CLARA - clara sobre clara. O BCT-4 tentou pegar isso por um LIMIAR de contraste
(0.2), mas `#CBB396` contra o branco `#FFFFFF` difere so 0.283: passava, e a sombra continuava
CLARA sobre uma fonte CLARA - "a sombra fica da mesma cor da fonte". A causa do `.cfg` do perfil
(somado) era `CorSombraClara = CBB396`, a PROPRIA cor da fonte, herdada de um build antigo: com
ela a letra bege virava `#000000` (por acaso), mas a letra BRANCA do nome (`CharacterNameColor`
= `Color.white`) recebia o bege `#CBB396`.

A LEI (BCT-5)
-------------
A sombra tem de ficar do LADO OPOSTO da luminancia da FONTE:

    letra CLARA  (luminancia >= 0.5) -> sombra ESCURA (#000000)
    letra ESCURA (luminancia <  0.5) -> sombra CLARA  (#FFFFFF)

O FUNDO continua PROPONDO a polaridade (BCT-3), mas o VETO DA LETRA cai sobre a proposta quando
ela poe a sombra do mesmo lado da fonte. Sem limiar: o LADO decide. A lei numerica do BCT-4
(diferenca de luminancia >= `ContrasteMinimo`) segue como rede contra um balde mal configurado.

E a VISIBILIDADE: o alfa da sombra dos NOMES tem de ser alto o bastante (>= `ALFA_SOMBRA_MINIMA`)
- a 0.35 a sombra escura era translucida demais e sumia no proprio glifo.

COMO ESTE TESTE E PROVADO REPROVANDO
------------------------------------
1. A ISCA (`ModeloFundoDaSombraAntes`, o defeito ANTES do BCT-5): devolve uma sombra CLARA para
   a letra CLARA `#CBB396` - o invariante do LADO reprova.
2. No FONTE: `defeito_letra_clara_sombra_clara` (arranca o VETO DA LETRA) e
   `defeito_alfa_sombra_baixo` (alfa de volta a 0.35) TEM de reprovar `falhas_do_contraste_da_letra`
   e `falhas_da_visibilidade`.
"""
import regras_bct as reg

import arcabouco as arc

META = {
    "nome": "bct-sombra-polaridade-fonte",
    "categoria": "pura",
    "requer": [],
    "descricao": "BCT-5: a sombra CONTRASTA com a FONTE - letra CLARA ganha sombra ESCURA e letra "
                 "ESCURA ganha sombra CLARA (o LADO oposto da luminancia), em toda a paleta e em "
                 "todo Fundo, com alfa visivel; a letra clara #CBB396 do nome do inimigo nunca mais "
                 "ganha uma sombra clara 'da mesma cor da fonte'",
}


def corpo():
    paleta = reg.paleta_do_jogo()
    arc.exigir(paleta is not None, "nao achei a fixture da paleta (%s)" % reg.FIXTURE_CORES)
    cores = paleta["guimanager"]["cores"]
    fundos = (reg.FUNDO_ESCURO, reg.FUNDO_CLARO, reg.FUNDO_AUTO)

    # ------------------------------------------------ 1) O INVARIANTE DO LADO (toda a paleta)
    violacoes = []
    for nome in sorted(cores):
        hex_letra = cores[nome].lstrip("#")
        letra_escura = reg.luminancia(hex_letra) < reg.LIMIAR_LUMINANCIA
        for fundo in fundos:
            hex_sombra = reg.sombra_para(hex_letra, fundo)
            lado = "CLARA" if letra_escura else "ESCURA"   # a sombra do LADO OPOSTO
            if hex_sombra != getattr(reg, "SOMBRA_" + lado):
                violacoes.append("%s (%s) fundo=%s -> sombra #%s (esperada a %s)"
                                 % (nome, hex_letra, fundo, hex_sombra, lado))
                continue
            if reg.contraste_com_a_letra(hex_letra, hex_sombra) < reg.CONTRASTE_MINIMO:
                violacoes.append("%s (%s) fundo=%s -> sombra #%s sem contraste com a letra"
                                 % (nome, hex_letra, fundo, hex_sombra))
    arc.exigir(not violacoes,
               "%d violacao(oes) da POLARIDADE PELA FONTE (a sombra tem de ficar do lado oposto "
               "da letra): %s" % (len(violacoes), " | ".join(violacoes)))

    # ------------------------------------------------ 2) o CASE RELATADO (o nome do inimigo)
    letra_bege = cores["highlightedColor"]       # #CBB396 (0.717) - LETRA CLARA
    letra_escura = cores["shadowColor"]          # #F000FF (0.395) - a unica LETRA ESCURA
    for fundo in fundos:
        arc.igual(reg.sombra_para(letra_bege, fundo), reg.SOMBRA_ESCURA,
                  "letra CLARA %s (nome do inimigo) + fundo %s: a sombra tem de ser ESCURA "
                  "(#%s) - ela CONTRASTA com a fonte" % (letra_bege, fundo, reg.SOMBRA_ESCURA))
        arc.igual(reg.sombra_para(letra_escura, fundo), reg.SOMBRA_CLARA,
                  "letra ESCURA %s + fundo %s: a sombra tem de ser CLARA (#%s)"
                  % (letra_escura, fundo, reg.SOMBRA_CLARA))
    arc.exigir(reg.sombra_para(letra_bege, reg.FUNDO_ESCURO) != letra_bege,
               "a sombra do nome do inimigo nao pode ser a PROPRIA cor (clara) da letra")

    # ------------------------------------------------ 3) a ISCA (a regra ANTES do BCT-5) reprova
    ruim = reg.ModeloFundoDaSombraAntes()
    sombra_ruim = ruim.sombra(letra_bege, reg.FUNDO_ESCURO)
    arc.igual(sombra_ruim, reg.SOMBRA_CLARA_ANTIGA,
              "isca: a regra ANTES do BCT-5 devolve #%s para a letra clara #%s"
              % (reg.SOMBRA_CLARA_ANTIGA, letra_bege))
    arc.exigir(reg.luminancia(reg.SOMBRA_CLARA_ANTIGA) >= reg.LIMIAR_LUMINANCIA,
               "isca: o #%s e uma sombra CLARA - ela fica do MESMO lado da letra clara (o defeito)"
               % reg.SOMBRA_CLARA_ANTIGA)
    arc.exigir(sombra_ruim != reg.sombra_para(letra_bege, reg.FUNDO_ESCURO),
               "isca: o MODELO do conserto tem de DIFERIR do defeito, senao a checagem passaria "
               "por construcao")

    # ------------------------------------------------ 4) o FONTE (o veto + a visibilidade)
    cfg = reg.fonte(reg.CFG)
    styler = reg.fonte(reg.STYLER)
    arc.exigir(len(cfg) > 3000 and len(styler) > 3000,
               "Configuracao.cs/TextStyler.cs vieram vazios: a leitura mudou de lugar?")

    falhas = reg.falhas_do_contraste_da_letra(cfg, styler)
    arc.exigir(not falhas, "a polaridade pela fonte caiu: %s" % " | ".join(falhas))

    falhas_vis = reg.falhas_da_visibilidade(cfg)
    arc.exigir(not falhas_vis, "a VISIBILIDADE da sombra caiu: %s" % " | ".join(falhas_vis))

    # -------------------------------- 5) CONTRA-PROVAS no FONTE (os defeitos plantados REPROVAM)
    for rotulo, plantar, checar, marca in (
            ("a letra CLARA ganha sombra CLARA (o VETO DA LETRA arrancado)",
             reg.defeito_letra_clara_sombra_clara, reg.falhas_do_contraste_da_letra, "VETO DA LETRA"),
            ("a sombra dos NOMES volta a alfa 0.35 (fraca demais para se ver)",
             reg.defeito_alfa_sombra_baixo, reg.falhas_da_visibilidade, "alfaSombra")):
        com_defeito = plantar(cfg)
        arc.exigir(com_defeito != cfg, "o plantio do defeito nao achou onde agir (%s)" % rotulo)
        if checar is reg.falhas_da_visibilidade:
            falhas_defeito = checar(com_defeito)
        else:
            falhas_defeito = checar(com_defeito, styler)
        arc.exigir(falhas_defeito, "as checagens PASSARAM com o defeito plantado (%s): o teste "
                                   "nao vigia nada" % rotulo)
        arc.exigir(any(marca in f for f in falhas_defeito),
                   "o defeito (%s) nao foi acusado no ponto certo (%s): %s"
                   % (rotulo, marca, " | ".join(falhas_defeito)))

    print("polaridade pela FONTE: %d cor(es) da paleta x %d fundo(s) - a sombra SEMPRE fica do "
          "lado OPOSTO da letra; o nome do inimigo (letra CLARA %s) -> sombra ESCURA #%s "
          "(contraste %.3f); a letra escura %s -> sombra CLARA #%s; alfa da sombra dos NOMES >= "
          "%.2f; 2 defeito(s) plantado(s) reprovam"
          % (len(cores), len(fundos), letra_bege, reg.SOMBRA_ESCURA,
             reg.contraste_com_a_letra(letra_bege, reg.SOMBRA_ESCURA), letra_escura,
             reg.SOMBRA_CLARA, reg.ALFA_SOMBRA_MINIMA))


if __name__ == "__main__":
    arc.main(META, corpo)
