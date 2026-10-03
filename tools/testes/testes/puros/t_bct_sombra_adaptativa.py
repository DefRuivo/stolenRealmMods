#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A SOMBRA ADAPTATIVA DO BETTERCOMBATTEXT (BCT-2): cor da letra -> luminancia -> sombra.

O QUE ESTE TESTE GARANTE
------------------------
A sombra deixou de ser FIXA e igual ao contorno. Agora ela ACOMPANHA a cor da letra:

    luminancia <  0.5  -> letra ESCURA -> sombra CLARA   (#FFFFFF)
    luminancia >= 0.5  -> letra CLARA  -> sombra ESCURA  (#000000)

A luminancia e a `Color.grayscale` do Unity (0.299R + 0.587G + 0.114B). O #000000 e o preto
neutro; a sombra CLARA e o BRANCO (#FFFFFF) — o #CBB396 (o antigo) era a PROPRIA cor de texto
do jogo e a cor comum do nome do inimigo, entao a sombra saia igual a letra (corrigido no BCT-4,
ver `t_bct_sombra_contraste_letra.py`).

ONDE O NEGOCIO E SENSIVEL (o que este teste vigia)
--------------------------------------------------
1. AS CORES VEM DA FIXTURE. O teste NAO digita a paleta: le
   `tools/testes/fixtures/cores-do-jogo.entrada.json` (leitura datada do prefab, 01/10) e so
   confere que o HEX da sombra clara e o `highlightedColor` de verdade. A tabela de baldes e
   IMPRESSA a partir da fixture.
2. A REGRA PURA existe no formato pedido: cor -> luminancia -> balde -> hex.
3. O C# LE A COR REAL DA LETRA (`tmp.color` no TMP, `txt.color` no legado) e escolhe a sombra
   por ela (`CorSombraPara(...)`), com as TRES chaves novas sob '1. Geral'
   (`SombraAdaptativa`, `CorSombraClara`, `CorSombraEscura`).
4. REAVALIACAO SEM RE-INSTANCIAR (o critico): o jogo pode REUSAR o componente mudando a cor
   (o dado que vira fogo e depois gelo). A cada chamada o mod RELE a cor e, se o BALDE virou,
   troca SO a cor da sombra (`_UnderlayColor` / `Shadow.effectColor`) - sem `new Material` e
   sem `AddComponent`. O MODELO do reuso prova isso: 1 material, 1 instancia, 1 troca de sombra.

COMO E PROVADO QUE REPROVA
--------------------------
`falhas_da_sombra_adaptativa` tem de REPROVAR quando se planta a regra ANTIGA ("sombra fixa
que ignora a luminancia") ou quando some a reavaliacao. O MODELO do defeito
(`ModeloEstilizadorAdaptativoFixo`) mostra o mesmo: o texto reusado fica com a sombra da
primeira cor. E a isca embutida: sem ela, as checagens passariam por construcao.

A rodada FISICA (o defeito plantado no TextStyler.cs, o teste reprovando, o fonte restaurado
byte a byte) esta em `tools/testes/bct2-sombra-prova-reprovando.log`.
"""
import regras_bct as reg

import arcabouco as arc

META = {
    "nome": "bct-sombra-adaptativa",
    "categoria": "pura",
    "requer": [],
    "descricao": "BCT-2: sombra ADAPTATIVA (cor -> luminancia -> balde -> hex): letra escura ganha #CBB396, letra clara ganha #000000, inclusive no REUSO do componente sem re-instancia",
}


def corpo():
    paleta = reg.paleta_do_jogo()
    arc.exigir(paleta is not None,
               "nao achei a fixture da paleta em %s (as cores da sombra vem dela, nunca digitadas)"
               % reg.FIXTURE_CORES)

    # ------------------------------------------------------------------ 1) a tabela de baldes
    linhas = reg.tabela_de_baldes(paleta)
    por_nome = dict((nome, (hexv, lum, balde)) for nome, hexv, lum, balde in linhas)

    # A sombra CLARA CORRIGIDA (BCT-4) e o BRANCO PURO: o #CBB396 era a PROPRIA cor de texto do
    # jogo (highlightedColor/specialDescColor) e a cor comum do nome do inimigo — a sombra saia
    # IGUAL a letra. O branco esta na paleta como `physicalColor`.
    arc.igual(paleta["guimanager"]["cores"]["physicalColor"].lstrip("#"), reg.SOMBRA_CLARA,
              "a sombra clara tem de ser o branco da paleta (`physicalColor`)")

    # As cores de dano que importam, por NOME (nunca por numero digitado aqui).
    arc.igual(por_nome["shadowColor"][2], reg.SOMBRA_CLARA,
              "shadowColor (%s, lum %.3f) e LETRA ESCURA -> sombra clara"
              % (por_nome["shadowColor"][0], por_nome["shadowColor"][1]))
    for nome in ("fireColor", "coldColor", "lightningColor", "healingColor", "manaColor",
                 "physicalColor"):
        arc.igual(por_nome[nome][2], reg.SOMBRA_ESCURA,
                  "%s (%s, lum %.3f) e LETRA CLARA -> sombra escura"
                  % (nome, por_nome[nome][0], por_nome[nome][1]))

    # A PARTICAO da paleta: so o `shadowColor` cai na sombra clara; todo o resto, na escura.
    claras = sorted(n for n, _h, _l, b in linhas if b == reg.SOMBRA_CLARA)
    arc.igual(claras, ["shadowColor"],
              "a unica cor da paleta que pede sombra CLARA tem de ser o `shadowColor`")

    # A borda do limiar: logo ABAIXO de 0.5 e letra escura; logo ACIMA, letra clara.
    arc.exigir(reg.balde_da_sombra("7F7F7F") == reg.SOMBRA_CLARA,
               "abaixo do limiar (0.5) a letra e ESCURA -> sombra clara")
    arc.exigir(reg.balde_da_sombra("808080") == reg.SOMBRA_ESCURA,
               "no/por cima do limiar (0.5) a letra e CLARA -> sombra escura")

    # ------------------------------------------------- 2) a regra no FONTE (tres chaves + codigo)
    cfg = reg.fonte(reg.CFG)
    styler = reg.fonte(reg.STYLER)
    arc.exigir(len(cfg) > 3000 and len(styler) > 3000,
               "Configuracao.cs/TextStyler.cs vieram vazios: a leitura mudou de lugar?")

    falhas = reg.falhas_da_sombra_adaptativa(cfg, styler)
    arc.exigir(not falhas, "a sombra adaptativa caiu: %s" % " | ".join(falhas))

    # ------------------------------------------------ 3) CONTRA-PROVAS no fonte (tem de reprovar)
    for rotulo, plantar, marca in (
            ("a sombra FIXA que ignora a luminancia (a regra antiga)",
             reg.defeito_sombra_fixa_ignora_luminancia, "CorSombraPara(tmp.color)"),
            ("a reavaliacao sem re-instancia arrancada",
             reg.defeito_reavaliacao_ausente, "ReavaliarSombraTmp(tmp, cfg, nosso)")):
        com_defeito = plantar(styler)
        arc.exigir(com_defeito != styler, "o plantio do defeito (%s) nao achou onde agir" % rotulo)
        falhas_defeito = reg.falhas_da_sombra_adaptativa(cfg, com_defeito)
        arc.exigir(falhas_defeito, "as checagens PASSARAM com o defeito (%s)" % rotulo)
        arc.exigir(any(marca in f for f in falhas_defeito),
                   "o defeito (%s) nao foi acusado no ponto certo (%s): %s"
                   % (rotulo, marca, " | ".join(falhas_defeito)))

    # ------------------------------------- 4) o MODELO do REUSO (balde que vira) - idempotencia
    clara_hex = reg.SOMBRA_CLARA
    escura_hex = reg.SOMBRA_ESCURA
    letra_clara = paleta["guimanager"]["cores"]["fireColor"]      # #FF5353 (clara)
    letra_escura = paleta["guimanager"]["cores"]["shadowColor"]  # #F000FF (escura)

    bom = reg.ModeloEstilizadorAdaptativo()
    primeira = bom.aplicar_com_cor(7, "material-do-prefab", letra_clara)
    # 1) ainda com a MESMA cor: nada a fazer (idempotente)...
    arc.igual(bom.reavaliar(7, letra_clara), "no-op", "mesma cor -> a sombra ja esta certa")
    # 2) outra cor CLARA (fire -> cold): continua no mesmo balde -> nada a fazer.
    arc.igual(bom.reavaliar(7, paleta["guimanager"]["cores"]["coldColor"]), "no-op",
              "a cor mudou mas o BALDE nao: nao reescreve a sombra")
    # 3) agora uma cor ESCURA (shadow): o BALDE vira -> troca SO a sombra.
    virou = bom.reavaliar(7, letra_escura)
    arc.igual(primeira, "aplicou", "a primeira passada instancia o material")
    arc.igual(virou, "trocou-sombra", "o BALDE virou -> a sombra tem de acompanhar")
    arc.igual(bom.sombra[7], clara_hex, "depois do reuso com letra escura, a sombra e a CLARA")
    arc.igual(bom.materiais, 1, "o reuso NAO re-instancia material")
    arc.igual(bom.aplicacoes, 1, "o reuso NAO re-aplica o efeito inteiro")
    arc.igual(bom.escritas_de_contorno, 1, "o contorno e escrito UMA vez por componente")
    arc.igual(bom.trocas_de_sombra, 1, "exatamente UMA troca de sombra no reuso")

    # A ISCA: o modelo do defeito (sombra fixa) NAO acompanha o reuso - e a regra antiga.
    ruim = reg.ModeloEstilizadorAdaptativoFixo()
    ruim.aplicar_com_cor(7, "material-do-prefab", letra_clara)
    arc.igual(ruim.reavaliar(7, letra_escura), "no-op",
              "isca: a sombra fixa ignora a luminancia e nunca troca")
    arc.igual(ruim.sombra[7], escura_hex,
              "isca: com o defeito o texto reusado fica com a sombra da PRIMEIRA cor")
    arc.igual(ruim.trocas_de_sombra, 0, "isca: zero trocas de sombra no defeito")

    print("sombra adaptativa: limiar %.2f; sombra clara #%s (highlightedColor da fixture), "
          "escura #%s; %d cor(es) da paleta na sombra CLARA, o resto na ESCURA (%s); "
          "reuso: 1 material, 1 aplicacao, 1 troca de sombra; 2 defeito(s) plantado(s) reprovam"
          % (reg.LIMIAR_LUMINANCIA, clara_hex, escura_hex, len(claras),
             ", ".join("%s=lum%.3f" % (n, l) for n, _h, l, _b in linhas)))


if __name__ == "__main__":
    arc.main(META, corpo)
