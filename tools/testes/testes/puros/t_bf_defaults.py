#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OS DEFAULTS do BetterFont, com arquivo:linha (TST-7, cenario 5).

O QUE ESTE TESTE GARANTE
------------------------
As tres chaves de config e os tres GETTERS SEGUROS, lidos do fonte vivo com a LINHA:

    Estilo/PreservarEstilo        = true    (nao mudou - o transporte do estilo)
    Estilo/PularTextosEstilizados = false   (MUDOU no BF-1: era true, virou false; e o ESCAPE)
    Diagnostico/LogDiagnosticoEstilo = false (nao mudou - sem spam no log)

E os getters: sem entrada de config (falha ao ler/criar), o valor e o CONSERVADOR de cada
um - `PularEstilizadosLigado` vale true (o texto estilizado fica intocado),
`PreservarEstiloLigado` vale true, `LogDiagnosticoLigado` vale false. ATENCAO ao ponto que
a doc errava: chave/arquivo `.cfg` AUSENTE nao cai no conservador - o BepInEx cria a
entrada com o default do Bind (false) e o caminho novo vale; o conservador so entra quando
ler/criar a entrada FALHA (getter seguro com entrada null).

POR QUE O `PularTextosEstilizados` E O QUE MAIS IMPORTA
-------------------------------------------------------
E o unico default que mudou no BF-1, e e o ESCAPE: `true` restaura o comportamento antigo
(o texto estilizado fica 100% intocado e perde a serifa - o defeito da interface
inconsistente que o dono relatou); `false` (o novo default) troca a fonte e transporta o
efeito. Quem mexer nesse default muda o comportamento em jogo, entao a linha fica vigiada.

PROCEDENCIA: tudo e lido do `BetterFont/Plugin.cs` VIVO (`defaults_com_linha` /
`getters_seguros`). A contra-prova embutida planta cada defeito EM MEMORIA (voltar o
default do escape para `true`, o do PreservarEstilo para `false`, o getter inseguro) e as
checagens TEM de reprovar apontando a linha. A rodada fisica esta em
`tools/testes/bf-prova-reprovando.log`.
"""
import os

import regras_bf_estilo as reg

import arcabouco as arc

META = {
    "nome": "bf-defaults",
    "categoria": "pura",
    "requer": [],
    "descricao": "TST-7: os defaults das 3 chaves (PularTextosEstilizados=false e o escape; PreservarEstilo=true; LogDiagnosticoEstilo=false) com arquivo:linha e os getters seguros",
}

ARQUIVO = "BetterFont/Plugin.cs"
ESPERADO = {"PreservarEstilo": True, "PularTextosEstilizados": False, "LogDiagnosticoEstilo": False}
CONSERVADOR = {"PreservarEstilo": True, "PularTextosEstilizados": True, "LogDiagnosticoEstilo": False}


def corpo():
    src = reg.fonte()
    arc.exigir(len(src) > 5000, "o fonte do BetterFont veio vazio/curto: a leitura mudou de lugar?")

    # ---- os tres defaults, com a linha.
    achados = reg.defaults_com_linha(src)
    for chave, valor in ESPERADO.items():
        arc.exigir(chave in achados,
                   "nao achei o `BindSeguro` da chave %s em %s" % (chave, ARQUIVO))
        arc.igual(achados[chave]["valor"], valor,
                  "%s:%d - default de %s" % (ARQUIVO, achados[chave]["linha"], chave))
    # a ordem importa: o escape e o `false` novo; os outros dois nao mudaram.
    arc.igual(achados["PularTextosEstilizados"]["valor"], False,
              "%s:%d - PularTextosEstilizados tem de ser false (o unico default que mudou no BF-1: "
              "false = troca a fonte e transporta o efeito; true = ESCAPE, o comportamento antigo)"
              % (ARQUIVO, achados["PularTextosEstilizados"]["linha"]))

    # ---- os tres getters seguros (o valor sem entrada de config).
    getters = reg.getters_seguros(src)
    for chave, valor in CONSERVADOR.items():
        arc.exigir(chave in getters, "nao achei o getter seguro de %s no fonte" % chave)
        arc.igual(getters[chave]["conservador_ligado"], valor,
                  "%s - getter de %s sem entrada de config" % (ARQUIVO, chave))

    # ---- a checagem consolidada.
    falhas = reg.falhas_dos_defaults(src)
    arc.exigir(not falhas, "os defaults regrediram em %d ponto(s): %s" % (len(falhas), " | ".join(falhas)))

    # ---- CONTRA-PROVAS EMBUTIDAS: cada defeito reprova, e a mensagem aponta a linha.
    plantados = (
        ("o default do ESCAPE voltando a `true`", reg.defeito_default_escape_true,
         "PularTextosEstilizados", "linha %d" % achados["PularTextosEstilizados"]["linha"]),
        ("`PreservarEstilo` voltando a `false`", reg.defeito_default_preservar_false,
         "PreservarEstilo", "linha %d" % achados["PreservarEstilo"]["linha"]),
        ("o getter de `PularTextosEstilizados` deixando o conservador", reg.defeito_getter_pular_inseguro,
         "PularTextosEstilizados", "CONSERVADOR"),
    )
    for rotulo, plantar, chave, marca in plantados:
        com_defeito = plantar(src)
        arc.exigir(com_defeito != src, "o plantio do defeito (%s) nao achou onde agir" % rotulo)
        falhas_defeito = reg.falhas_dos_defaults(com_defeito)
        arc.exigir(falhas_defeito, "as checagens PASSARAM num fonte com o defeito (%s)" % rotulo)
        arc.exigir(any(chave in f for f in falhas_defeito),
                   "o defeito (%s) nao e pego pela chave certa (%s): %s"
                   % (rotulo, chave, " | ".join(falhas_defeito)))

    print("defaults em %s: PreservarEstilo=%s (linha %d), PularTextosEstilizados=%s (linha %d, "
          "o escape), LogDiagnosticoEstilo=%s (linha %d); getters seguros: pular=%s, preservar=%s, "
          "diagnostico=%s; %d defeito(s) plantado(s) reprovam"
          % (os.path.basename(ARQUIVO), achados["PreservarEstilo"]["valor"], achados["PreservarEstilo"]["linha"],
             achados["PularTextosEstilizados"]["valor"], achados["PularTextosEstilizados"]["linha"],
             achados["LogDiagnosticoEstilo"]["valor"], achados["LogDiagnosticoEstilo"]["linha"],
             CONSERVADOR["PularTextosEstilizados"], CONSERVADOR["PreservarEstilo"],
             CONSERVADOR["LogDiagnosticoEstilo"], len(plantados)))


if __name__ == "__main__":
    arc.main(META, corpo)
