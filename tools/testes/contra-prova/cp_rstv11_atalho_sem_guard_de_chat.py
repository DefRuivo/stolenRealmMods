#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do atalho (RSTV-11a): a ISCA do guard de CHAT.

O que este arquivo faz aqui: ele existe para o runner ter o que reprovar. A regra do plano
(`docs/PLANO-DE-TESTES.md`) e que todo teste seja MOSTRADO REPROVANDO - e a unica forma de mostrar
isso num teste que le o FONTE vivo e rodar as MESMAS checagens contra um fonte com o defeito plantado.

O DEFEITO: o postfix de `KeybindManager.Update` roda nos early-returns do jogo (l.133374 e o que sai
quando ha campo de texto em foco), entao sem o handler replicar o guard de FOCO DE TEXTO a tecla
dispara DURANTE O CHAT. Aqui o guard deixa de ser um ramo VIVO (`if (FocoDeTexto())` ->
`if (false && FocoDeTexto())`), em memoria, sem tocar em arquivo. As checagens de
`tools/testes/regras_rstv11.py` TEM de reprovar pelo guard de chat, e o modelo puro tem de mostrar que
a regra defeituosa ABRE com o chat aberto enquanto a implementada NAO. Este arquivo tem de sair
REPROVOU (exit 1) - se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv11_atalho_f10.py`, ao lado.
"""
import regras_rstv11 as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv11-atalho-sem-guard",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-11a: com o guard de chat morto no atalho, o fonte e o modelo tem de "
                  "REPROVAR"),
}


def corpo():
    src = reg.fonte(reg.caminho_atalho())
    src_patches = reg.fonte(reg.caminho_patches())
    src_plugin = reg.fonte(reg.caminho_plugin())

    # 1) A ISCA NO FONTE: o defeito reinjetado tem de ser pego pelo guard de chat.
    com_defeito = reg.fonte_com_atalho_sem_guard(src)
    if com_defeito == src:
        raise arc.Falhou("o plantio do defeito nao encontrou a ancora (`if (FocoDeTexto())`): a isca "
                         "nao esta lendo o trecho certo")
    falhas = reg.falhas_do_atalho(com_defeito, src_patches, src_plugin)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM num fonte com o guard de chat morto: a verificacao do "
                         "atalho nao vale nada")
    if not any("foco de texto" in f or "chat" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pelo guard de chat: %s"
                         % " | ".join(falhas))

    # 2) A ISCA NO MODELO: com o chat aberto, a regra implementada NAO abre e a defeituosa ABRE.
    chat = dict(reg.CENARIO_CHAT_ABERTO)
    if reg.atalho_novo(chat) is not None:
        raise arc.Falhou("a regra implementada ABRIU com o chat aberto: o guard de chat nao esta de pe")
    if reg.atalho_sem_guard(chat) is None:
        raise arc.Falhou("a regra defeituosa NAO abriu com o chat aberto: a isca nao reproduz o defeito")

    # Chegou aqui: o defeito FOI pego (fonte e modelo). Esta isca reprova de proposito, dizendo o motivo.
    raise arc.Falhou("isca: o 'atalho sem guard de chat' foi pego pelo fonte e pelo modelo (esperado) - "
                     "fonte: %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
