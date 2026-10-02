#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""DESLIGAR E INERTE (TST-8, cenario 4): com Ativar=false nenhum gancho age.

O QUE ESTE TESTE GARANTE
------------------------
A chave mestra (`1. Geral` > `Ativar = false`) e a promessa do mod inteiro: "o jogo roda
100% original". Para isso ela precisa de DUAS coisas, e o teste confere as duas:

  1. `Plugin.Awake` checa `if (!Cfg.Ativar.Value)` ANTES de `AplicarPatches()` e sai - nenhum
     gancho Harmony e registrado, entao nenhum postfix pode rodar (nem lancar excecao);
  2. TODO metodo de gancho e inerte por si - `if (!Plugin.Ativo) return;` no proprio corpo, ou
     por delegacao a um metodo do mesmo arquivo que tem essa guarda (o caso do gatilho do
     diagnostico, que chama `DiagnosticoRotina.Tentar`, e o de `PatchRotulosDeStatus`).

A segunda e a que pega a regressao: um gancho novo sem guarda continua aplicado (se a chave
foi ligada antes) e passaria a agir - o "postfix quente" mexendo na tela com o mod desligado.
O modelo puro (`regras_bct.ModeloDeModo`) fecha o sentido: com `ativo=False` o gancho responde
"nada"; o modelo do defeito responde "mudou".

A rodada fisica (a guarda arrancada de um Postfix, o teste reprovando, o fonte restaurado byte
a byte) esta em `tools/testes/bct-prova-reprovando.log`.
"""
import regras_bct as reg

import arcabouco as arc

META = {
    "nome": "bct-desligar-inerte",
    "categoria": "pura",
    "requer": [],
    "descricao": "TST-8/4: com Ativar=false nenhum gancho age - Awake sai antes de aplicar e todo postfix e guardado (direto ou por delegacao)",
}

SUPERFICIES = ("Nomes (combate)", "Eventos (texto do dado)", "Rotulos (combate)")


def corpo():
    plugin = reg.fonte(reg.PLUGIN)
    patches = reg.fonte(reg.PATCHES)
    diag = reg.fonte(reg.DIAG)
    outros = {reg.PATCHES: patches, reg.DIAG: diag}

    falhas = reg.falhas_desligar_inertes(plugin, outros)
    arc.exigir(not falhas, "com Ativar=false o mod NAO ficaria inerte: %s" % " | ".join(falhas))

    # a contra-prova: um Postfix sem a guarda TEM de ser acusado.
    com_defeito = reg.defeito_gancho_sem_guarda(patches)
    arc.exigir(com_defeito != patches, "o plantio do defeito (gancho sem guarda) nao achou onde agir")
    falhas_defeito = reg.falhas_desligar_inertes(plugin, {reg.PATCHES: com_defeito, reg.DIAG: diag})
    arc.exigir(falhas_defeito, "as checagens PASSARAM com um Postfix sem `if (!Plugin.Ativo)`")
    arc.exigir(any("PatchNomeDoChefe" in f for f in falhas_defeito),
               "o gancho sem guarda nao foi nomeado na falha: %s" % " | ".join(falhas_defeito))

    # o MODELO puro: desligado = nada age, em nenhuma superficie; ligado = age.
    desligado = reg.ModeloDeModo(False)
    resultados = [desligado.gancho(s) for s in SUPERFICIES]
    arc.igual(resultados, ["nada"] * len(SUPERFICIES),
              "com Ativar=false o gancho de cada superficie")
    arc.igual(desligado.agiu, 0, "quantos ganchos agiram com o mod desligado")

    ligado = reg.ModeloDeModo(True)
    arc.igual([ligado.gancho(s) for s in SUPERFICIES], ["mudou"] * len(SUPERFICIES),
              "com Ativar=true o gancho de cada superficie")
    arc.igual(ligado.agiu, len(SUPERFICIES), "quantos ganchos agiram com o mod ligado")

    ruim = reg.ModeloDeModoAntesDaChave(False)
    arc.igual([ruim.gancho(s) for s in SUPERFICIES], ["mudou"] * len(SUPERFICIES),
              "a isca: SEM a guarda, o gancho age mesmo com Ativar=false")
    arc.igual(ruim.agiu, len(SUPERFICIES), "a isca precisa mostrar os ganchos agindo desligado")

    classes = (reg.classes_de_gancho(plugin) + reg.classes_de_gancho(patches)
               + reg.classes_de_gancho(diag))
    print("Awake sai antes de aplicar a chave mestra; %d classe(s) de gancho guardadas (direto ou "
          "por delegacao); modelo: desligado=%s (agiram %d), ligado=%s (agiram %d), sem guarda=%s; "
          "1 defeito plantado reprova"
          % (len(classes), resultados, desligado.agiu, ["mudou"] * len(SUPERFICIES), ligado.agiu,
             [ruim.gancho(s) for s in ("x",)]))


if __name__ == "__main__":
    arc.main(META, corpo)
