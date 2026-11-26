#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O ROTULO DA ABA DO VISUALIZADOR SAI EM UTF-8 CORRETO (RSTV-LABEL / SR-QA-02).

O QUE ISTO TRAVA
----------------
`SkillTreesTab.TabLabel` e o texto final da 4a aba. A build 0.3.9 entregou `Ã\u0081rvores` (o "Á"
lido como latin-1); a aba do jogo nativo ao lado desenha "Á" normalmente, entao nao e fonte.
A checagem compara o literal com o caractere certo e reprova por codepoint.

DE ONDE VEM O ESPERADO
----------------------
Regra em `tools/testes/regras_rstv_label.py`, fonte lido AO VIVO do mod. Os plantios (literal
corrompido e o mesmo texto escrito como escape) provam que a checagem reprova. O que so o dono
confirma em tela: o rotulo desenhado e a aba cabendo na largura de ~78u.
"""
import regras_rstv_label as reg

import arcabouco as arc

META = {
    "nome": "rstv-label-arvores",
    "categoria": "pura",
    "requer": [],
    "descricao": ("RSTV-LABEL: TabLabel decodifica para 'Arvores' acentuado em UTF-8/NFC, sem "
                  "caractere C1 nem escape; o literal corrompido da 0.3.9 e a variante escapada "
                  "reprovam"),
}


def corpo():
    src = reg.fonte(reg.caminho_aba())
    arc.exigir(len(src) > 1000, "SkillTreesTab.cs veio vazio/curto: a leitura mudou de lugar?")

    # 1) O rotulo vivo tem de estar correto.
    falhas = reg.falhas_do_rotulo(src)
    arc.exigir(not falhas, "o rotulo da aba regrediu: %s" % " | ".join(falhas))

    # 2) PROVA DE FOGO 1: o mojibake entregue na 0.3.9 reprova.
    corrompido = reg.fonte_com_rotulo_corrompido(src)
    arc.exigir(corrompido != src,
               "o plantio do defeito nao encontrou a ancora (%r): a checagem nao le o trecho certo"
               % reg.ASSINATURA)
    f1 = reg.falhas_do_rotulo(corrompido)
    arc.exigir(any("C1" in f or "0.3.9" in f for f in f1),
               "as checagens PASSARAM com o rotulo corrompido: %s" % " | ".join(f1))

    # 3) PROVA DE FOGO 2 (variante nova): o MESMO texto errado escrito como escape tambem reprova.
    escapado = reg.fonte_com_rotulo_escapado(src)
    arc.exigir(escapado != src, "o plantio da variante escapada nao encontrou a ancora")
    f2 = reg.falhas_do_rotulo(escapado)
    arc.exigir(len(f2) >= 1, "as checagens PASSARAM com o rotulo errado escrito como escape")

    print("RSTV-LABEL: TabLabel = %r (%s); o mojibake da 0.3.9 e a variante escapada reprovam"
          % (reg.ROTULO, reg.pontos(reg.ROTULO)))


if __name__ == "__main__":
    arc.main(META, corpo)
