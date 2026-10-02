#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A REGRA DE OURO DO BETTERCOMBATTEXT (TST-8, cenario 1): o material e sempre a COPIA.

O QUE ESTE TESTE GARANTE
------------------------
No TextMeshPro o material da fonte e COMPARTILHADO por todos os textos que usam aquela fonte.
Escrever nele muda a interface inteira. O BCT promete (README: "The effect always uses a
per-text copy of the material - never the shared one") escrever so na COPIA por componente
que o getter `TMP_Text.fontMaterial` devolve.

A checagem mais FORTE disso nao e procurar linhas no fonte (depende de achar TODAS as linhas):
e a AUSENCIA do setter entre as REFERENCIAS do IL. Em .NET, `x.fontSharedMaterial = v` vira
uma referencia (MemberRef) ao metodo `set_fontSharedMaterial`; se essa referencia NAO existe
na tabela MemberRef da DLL do PACOTE, o compilador nao viu nenhuma atribuicao, em nenhuma
linha, de nenhum arquivo. O leitor de metadados e PYTHON PURO (`regras_bct.ler_metadados`) e
o comando dele esta no cabecalho do modulo:

    python tools/testes/regras_bct.py                       # a DLL do pacote (dist/) ou do bin/
    python tools/testes/regras_bct.py <caminho-da.dll>      # a leitura crua, na mao

O que NAO e prova de nada: um leitor que "varre e nao acha nada". Por isso o teste exige o
CONTROLE POSITIVO - as referencias de LEITURA que a DLL TEM (`get_fontSharedMaterial`,
`get_fontMaterial`, `SetMaterialDirty`, `set_fontSize`, ...) tem de aparecer. E a contra-prova
planta o defeito NO IL, renomeando os bytes da referencia de leitura para a de escrita (o
prefixo `get_`/`set_` tem o mesmo tamanho): a checagem TEM de acusar.

PROCEDENCIA DA DLL
------------------
A DLL vem do PACOTE em `dist/` (o mesmo arquivo que o jogador instala) e, na falta dele, do
build local em `bin/Release` ou `bin/Debug` - `dist/` e `bin/` sao gitignored (artefato de
build). Sem nenhuma DLL o teste NAO RODOU (exit 2): nunca um verde escondendo a checagem.

O QUE ESTE TESTE NAO PROVA
--------------------------
Nao abre o jogo: que o contorno APARECA na tela so o dono confirma. E o caso "o material em
uso ja e a instancia de OUTRO mod" tem uma ressalva registrada no relatorio/log: o getter do
TMP REUSA a instancia do outro mod em vez de clonar por cima (`TextMeshProUGUI.GetMaterial`
so cria copia quando `m_fontMaterial` e nulo ou tem InstanceID diferente) - o mod escreve NELA,
sem `CreateMaterialInstance`, e nao espalha porque a instancia e por componente.
"""
import regras_bct as reg

import arcabouco as arc

META = {
    "nome": "bct-regra-de-ouro",
    "categoria": "pura",
    "requer": [],
    "descricao": "TST-8/1: o material e sempre a copia por componente - o IL da DLL do pacote nao referencia setter de material e o fonte so le o compartilhado",
}


def corpo():
    # ---------------------------------------------------------------- o FONTE
    styler = reg.fonte(reg.STYLER)
    arc.exigir(len(styler) > 3000, "o TextStyler.cs veio vazio/curto: a leitura mudou de lugar?")

    falhas = reg.falhas_regra_de_ouro_no_fonte(styler)
    arc.exigir(not falhas, "a regra de ouro caiu no fonte: %s" % " | ".join(falhas))

    com_defeito = reg.defeito_escreve_no_compartilhado(styler)
    arc.exigir(com_defeito != styler,
               "o plantio do defeito (escrever no compartilhado) nao achou onde agir")
    falhas_defeito = reg.falhas_regra_de_ouro_no_fonte(com_defeito)
    arc.exigir(falhas_defeito, "as checagens PASSARAM num fonte que escreve no material "
                               "compartilhado: elas nao pegam o defeito da regra de ouro")

    # ------------------------------------------------------------------ o IL
    origem, dados = reg.dll_do_pacote()
    if dados is None:
        raise arc.NaoRodou(
            "nao achei a DLL do BetterCombatText (pacote em dist/gumatos-BetterCombatText-*.zip "
            "ou bin/Release|Debug/netstandard2.1/BetterCombatText.dll). A prova da regra de ouro "
            "e sobre o CODIGO COMPILADO - sem a DLL isto NAO RODOU (exit 2), nunca verde.",
            faltando="dll-do-bct")

    meta = reg.ler_metadados(dados)
    falhas_il = reg.falhas_dos_metadados(meta)
    arc.exigir(not falhas_il,
               "o IL da DLL do pacote (%s) reprovou em %d ponto(s): %s"
               % (origem, len(falhas_il), " | ".join(falhas_il)))

    # Contra-prova NO IL: a referencia de leitura vira a de escrita (mesmo comprimento) - e o
    # que a DLL seria se o mod tivesse escrito `x.fontSharedMaterial = v`.
    mutado = reg.il_com_o_setter_do_compartilhado(dados)
    arc.exigir(mutado != dados,
               "o plantio no IL nao achou a referencia `get_fontSharedMaterial` para renomear: "
               "a checagem nao esta lendo a tabela certa")
    meta_mutado = reg.ler_metadados(mutado)
    falhas_mutado = reg.falhas_dos_metadados(meta_mutado)
    arc.exigir(any("set_fontSharedMaterial" in f for f in falhas_mutado),
               "com o SETTER plantado no IL as checagens nao acusaram o setter de material: %s"
               % " | ".join(falhas_mutado or ["(nada)"]))

    print("fonte: so le `fontSharedMaterial` e escreve na copia do getter `fontMaterial`; "
          "IL da DLL do pacote (%s, sha256 %s, %d referencias de membro, %d AssemblyRef): "
          "NENHUM setter de material entre as referencias; controle positivo com %d referencia(s) "
          "que a DLL TEM; setter plantado no IL acusa"
          % (origem, meta["sha256"][:16], len(meta["memberrefs"]), len(meta["assemblyrefs"]),
             len(reg.MEMBROS_ESPERADOS)))


if __name__ == "__main__":
    arc.main(META, corpo)
