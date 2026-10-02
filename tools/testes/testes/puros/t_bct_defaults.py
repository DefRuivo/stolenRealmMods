#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OS DEFAULTS DO BETTERCOMBATTEXT (TST-8, cenario 3): tooltip DESLIGADO, eventos LIGADO.

O QUE ESTE TESTE GARANTE
------------------------
Os defaults do `.cfg` sao comportamento em jogo, e o par que mais importa e este:

    secao "4. Eventos (texto do dado)"  Ativar = TRUE   (o dado ganha o efeito - o pedido)
    secao "6. Tooltip de status"        Ativar = FALSE  (o grupo do tooltip NAO liga sozinho)

POR QUE O TOOLTIP VEM DESLIGADO. O nome do buff/debuff nao tem rotulo proprio em combate:
ele so aparece no tooltip generico, e o componente que o desenha (`Tooltip.Title` /
`Tooltip.Description`) e O MESMO dos tooltips de skill, item e powerup. Ligar por padrao
instanciaria o material DESSE componente compartilhado e o halo valeria para TODO tooltip do
jogo - fora do pedido ("efeito so nos textos alvo"). O teste exige que esse motivo esteja
ESCRITO acima do default: quem ligar tem de saber o que esta ligando.

Ainda na ESPEC (pedido do dono, 30/09): a chave mestra `Ativar` LIGADA, o numero de vida
DESLIGADO (fora do pedido original) e o diagnostico de arranque LIGADO.

DE ONDE VEM O ESPERADO
----------------------
Os valores sao LIDOS do `Configuracao.cs` vivo, com arquivo:linha (`regras_bct.binds_com_linha`).
A ESPEC (ligado/desligado de cada grupo) e a exigencia do dono, transcrita em
`regras_bct.ESPEC_DEFAULTS` - nao e um numero que o fonte possa ditar. A contra-prova planta
os dois defeitos classicos (tooltip ligado, eventos desligado): as checagens TEM de reprovar
apontando a linha. A rodada fisica esta em `tools/testes/bct-prova-reprovando.log`.
"""
import regras_bct as reg

import arcabouco as arc

META = {
    "nome": "bct-defaults",
    "categoria": "pura",
    "requer": [],
    "descricao": "TST-8/3: tooltip de status DESLIGADO (Title/Description sao compartilhados com skill/item/powerup), eventos/dado LIGADO, chave mestra LIGADA; com arquivo:linha",
}


def corpo():
    cfg = reg.fonte(reg.CFG)
    arc.exigir(len(cfg) > 3000, "o Configuracao.cs veio vazio/curto: a leitura mudou de lugar?")

    achados = reg.binds_com_linha(cfg)
    arc.exigir(len(achados) >= len(reg.ESPEC_DEFAULTS),
               "so achei %d `Bind` com default LITERAL no Configuracao.cs (a ESPEC tem %d): a "
               "leitura dos defaults mudou de forma" % (len(achados), len(reg.ESPEC_DEFAULTS)))

    falhas = reg.falhas_dos_defaults(cfg)
    arc.exigir(not falhas, "os defaults regrediram: %s" % " | ".join(falhas))

    # Mostra a leitura por arquivo:linha (o que o cenario pede).
    linhas = {}
    for secao, chave, valor in reg.ESPEC_DEFAULTS:
        casa = [a for a in achados if secao in (a["secao"] or "") and a["chave"] == chave]
        arc.exigir(casa, "nao achei o `Bind` de %s > %s" % (secao, chave))
        linhas["%s > %s" % (secao, chave)] = (casa[0]["valor"], casa[0]["linha"])
        arc.igual(casa[0]["valor"], valor,
                  "%s:%d - default de %s > %s" % (reg.CFG, casa[0]["linha"], secao, chave))

    # O evento/dado LIGADO e o tooltip DESLIGADO, lado a lado (o par que o cenario pede).
    arc.igual(linhas["4. Eventos > Ativar"][0], True,
              "%s:%d - o grupo de eventos/dado tem de vir LIGADO"
              % (reg.CFG, linhas["4. Eventos > Ativar"][1]))
    arc.igual(linhas["6. Tooltip > Ativar"][0], False,
              "%s:%d - o grupo do tooltip de status tem de vir DESLIGADO (Title/Description sao "
              "compartilhados com skill/item/powerup)"
              % (reg.CFG, linhas["6. Tooltip > Ativar"][1]))

    # Contra-provas: cada defeito reprova, e a mensagem aponta a LINHA.
    for rotulo, plantar, chave in (
            ("o tooltip ligado por padrao", reg.defeito_default_tooltip_ligado, "6. Tooltip"),
            ("o eventos/dado desligado por padrao", reg.defeito_default_eventos_desligado, "4. Eventos")):
        com_defeito = plantar(cfg)
        arc.exigir(com_defeito != cfg, "o plantio do defeito (%s) nao achou onde agir" % rotulo)
        falhas_defeito = reg.falhas_dos_defaults(com_defeito)
        arc.exigir(falhas_defeito, "as checagens PASSARAM com o defeito (%s)" % rotulo)
        arc.exigir(any(chave in f for f in falhas_defeito),
                   "o defeito (%s) nao foi apontado na secao certa (%s): %s"
                   % (rotulo, chave, " | ".join(falhas_defeito)))

    print("defaults lidos de %s: %s; %d defeito(s) plantado(s) reprovam apontando a linha"
          % (reg.CFG, "; ".join("%s=%s(linha %d)" % (k, v[0], v[1]) for k, v in sorted(linhas.items())), 2))


if __name__ == "__main__":
    arc.main(META, corpo)
