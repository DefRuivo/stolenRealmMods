#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O APLICADOR E A CONTRA-PROVA DO check_patches (TST-8, cenario 8).

O QUE ESTE TESTE GARANTE
------------------------
O BCT aplica os ganchos UM A UM (`ArmonyPatch` por CLASSE, `CreateClassProcessor(tipo)` +
`processador.Patch()`), com a contagem REAL no log (`ganchosOk/ganchosTotal`, `metodosOk`) -
nunca `PatchAll()`, que e tudo-ou-nada: um gancho ruim deixa os outros sem aplicar, em
silencio. `tools/check_patches.py` (a trava TRV-1) ja cobre parte disso - este teste e a
CONTRA-PROVA dela.

O DEFEITO QUE A TRAVA EXISTE PARA PEGAR (A-1 da REV-2): o FILTRO do aplicador
(`EhClasseDeGancho`) exige `[HarmonyPrefix]`/`[HarmonyPostfix]` NO METODO e nao cita os nomes de
convencao do Harmony (`Prefix`/`Postfix`/`Transpiler`/`Finalizer`). Os dois valem igual para o
Harmony, e o `PatchAll()` aceitava os dois - com o filtro errado o mod CARREGA, loga
"carregado." e aplica ZERO gancho: o silencio parecendo sucesso (4 mods, 14 classes, 0
aplicadas). A trava tem de ser vigiada: um filtro assim TEM de ser reprovado por ela.

COMO E TESTADO
--------------
1. no FONTE do BCT: aplicador proprio, sem `PatchAll`, com a contagem real, e o filtro aceitando
   o gancho por `[HarmonyPatch]` no TIPO (os 9 ganchos do BCT sao declarados pela CONVENCAO DE
   NOME - metodo `Postfix` sem atributo - entao um filtro que exigisse atributo os perderia);
2. na TRAVA (`tools/check_patches.py`, importada como modulo): a mesma decisao da REGRA 5 roda
   sobre o Plugin.cs VIVO (nao reprova) e sobre o Plugin.cs com o FILTRO DEFEITUOSO plantado (TEM
   de reprovar, nomeando `EhClasseDeGancho`). A conta sai do proprio codigo do mod: as classes de
   patch e os metodos de gancho vem de `classes_de_patch` da trava, nunca digitados.

A rodada fisica (o filtro defeituoso no Plugin.cs, o teste reprovando, o fonte restaurado byte
a byte) esta em `tools/testes/bct-prova-reprovando.log`.
"""
import regras_bct as reg

import arcabouco as arc

META = {
    "nome": "bct-aplicador",
    "categoria": "pura",
    "requer": [],
    "descricao": "TST-8/8: o mod aplica gancho a gancho com contagem real (sem PatchAll) e o filtro so aceita [HarmonyPatch] no TIPO - e a contra-prova da trava check_patches (filtro que exige atributo TEM de reprovar)",
}


def corpo():
    plugin = reg.fonte(reg.PLUGIN)
    projeto = [reg.fonte(n) for n in reg.FONTES]
    arc.exigir(len(plugin) > 3000, "o Plugin.cs veio vazio/curto: a leitura mudou de lugar?")

    # ---------------------------------------------------------------- 1) o FONTE
    falhas = reg.falhas_do_aplicador(plugin)
    arc.exigir(not falhas, "o aplicador regrediu: %s" % " | ".join(falhas))

    classes = [c for texto in projeto for c in reg.classes_de_gancho(texto)]
    ganchos = [(c[0], m[0]) for c in classes for m in c[3]]
    arc.exigir(len(classes) >= 9, "esperava >=9 classes de gancho no BCT (7 em Patches.cs + 2 no "
                                  "DiagnosticoArranque.cs), achei %d" % len(classes))
    arc.exigir(len(ganchos) == len(classes),
               "cada classe de gancho tem 1 metodo (%d classes, %d metodos)" % (len(classes), len(ganchos)))
    # O BCT declara os ganchos pela CONVENCAO DE NOME (metodo `Postfix` sem atributo): se algum
    # deles passa a ter o ATRIBUTO, o filtro que exige atributo deixaria de ser um defeito - o
    # teste avisa em vez de virar vacuidade.
    by_name = []
    for nome in (reg.PATCHES, reg.DIAG):
        texto = reg.sem_comentarios(reg.fonte(nome))
        if "HarmonyPostfix" in texto or "HarmonyPrefix" in texto:
            by_name.append(nome)
    arc.exigir(not by_name,
               "os ganchos de %s passaram a ser declarados por ATRIBUTO: a premissa deste teste "
               "(gancho por convencao de nome, que o filtro defeituoso perde) mudou" % by_name)

    # ------------------------------------------------- 2) a TRAVA (contra-prova)
    reprova_bom, detalhe_bom = reg.decisao_do_check_patches(plugin, projeto)
    arc.exigir(not reprova_bom,
               "a trava `tools/check_patches.py` REPROVOU o Plugin.cs VIVO (falso positivo): %s"
               % detalhe_bom)
    arc.exigir("por nome" in detalhe_bom,
               "a trava nao contou os ganchos por convencao de nome (o BCT so tem desses): %s"
               % detalhe_bom)

    com_defeito = reg.defeito_filtro_exige_atributo(plugin)
    arc.exigir(com_defeito != plugin, "o plantio do filtro defeituoso nao achou onde agir")
    reprova_mau, detalhe_mau = reg.decisao_do_check_patches(com_defeito, projeto)
    arc.exigir(reprova_mau, "a TRAVA NAO REPROVOU um filtro que exige atributo no metodo e nao "
                            "cita os nomes de convencao: a trava deixou o defeito A-1 passar "
                            "(%s)" % detalhe_mau)
    arc.exigir("EhClasseDeGancho" in detalhe_mau,
               "a trava reprovou, mas nao nomeou o filtro defeituoso: %s" % detalhe_mau)

    print("aplicador proprio (%d classe(s), %d metodo(s) de gancho, %d por convencao de nome), "
          "sem PatchAll, com contagem real; trava `check_patches` verde no Plugin.cs vivo "
          "(%s) e REPROVANDO o filtro defeituoso (%s)"
          % (len(classes), len(ganchos), sum(1 for c in classes for m in c[3]),
             detalhe_bom, detalhe_mau))


if __name__ == "__main__":
    arc.main(META, corpo)
