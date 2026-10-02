#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IDEMPOTENCIA DO BETTERCOMBATTEXT (TST-8, cenario 2): aplicar duas vezes nao acumula.

O QUE ESTE TESTE GARANTE
------------------------
Os ganchos do mod sao POSTFIXES de metodos que o jogo chama a cada escrita do texto - o nome
do inimigo e reescrito, o stack do buff muda, o dado rola. Sem um registro por componente, a
rotina re-instancia o material e re-aplica o efeito a cada chamada (acumula). O mod mantem
`MateriaisInstanciados` (InstanceID -> material NAO compartilhado) e sai na segunda chamada:

    if (MateriaisInstanciados.TryGetValue(id, out var nosso) && nosso != null && nosso == compartilhadoAntes)
        return;                              // ja e a nossa instancia deste componente

O ajuste de fonte do mesmo jeito: `AplicarTamanho` guarda o tamanho ORIGINAL e escreve
`original + extra` (nunca `fontSize + extra`, que somaria a cada frame). O caminho legado
(UI.Text) tem o mesmo par: `TextosLegadosTratados` e `TamanhoOriginalLegado`.

COMO A IDEMPOTENCIA E TESTADA
-----------------------------
1. na ESTRUTURA do fonte: as tres pecas do guarda (consulta, instancia, registro) na ORDEM
   certa, e o ajuste de fonte partindo do original;
2. no MODELO transcrito (`regras_bct.ModeloEstilizadorTmp`): aplicar duas vezes no MESMO
   componente devolve "aplicou" e depois "no-op", com `aplicacoes == 1`. O modelo do defeito
   (`ModeloEstilizadorTmpSemGuarda`) devolve "aplicou" nas duas e `aplicacoes == 2` - e a
   isca embutida: sem ela, a checagem 1 passaria por construcao.

A rodada FISICA (o guarda arrancado do TextStyler.cs, o teste reprovando, o fonte restaurado
byte a byte) esta em `tools/testes/bct-prova-reprovando.log`.
"""
import regras_bct as reg

import arcabouco as arc

META = {
    "nome": "bct-idempotencia",
    "categoria": "pura",
    "requer": [],
    "descricao": "TST-8/2: aplicar duas vezes no mesmo componente nao acumula (registro por InstanceID no TMP e no legado, e o piso no tamanho original)",
}


def corpo():
    styler = reg.fonte(reg.STYLER)
    arc.exigir(len(styler) > 3000, "o TextStyler.cs veio vazio/curto: a leitura mudou de lugar?")

    # ------------------------------------------------------- 1) a ESTRUTURA do fonte
    falhas = reg.falhas_da_idempotencia(styler)
    arc.exigir(not falhas, "a idempotencia caiu: %s" % " | ".join(falhas))

    for rotulo, plantar in (("o guarda por InstanceID sumindo", reg.defeito_sem_guarda_idempotencia),
                            ("o ajuste de fonte somando no valor atual", reg.defeito_tamanho_acumula)):
        com_defeito = plantar(styler)
        arc.exigir(com_defeito != styler, "o plantio do defeito (%s) nao achou onde agir" % rotulo)
        falhas_defeito = reg.falhas_da_idempotencia(com_defeito)
        arc.exigir(falhas_defeito, "as checagens PASSARAM num fonte com o defeito (%s)" % rotulo)

    # --------------------------------------------------------- 2) o MODELO transcrito
    bom = reg.ModeloEstilizadorTmp()
    primeira = bom.aplicar(4242, "material-do-prefab")
    segunda = bom.aplicar(4242, "instancia-4242")
    arc.igual((primeira, segunda), ("aplicou", "no-op"),
              "duas aplicacoes no MESMO componente (o postfix roda a cada escrita do texto)")
    arc.igual(bom.aplicacoes, 1, "quantas vezes o mod instanciou material e escreveu props")
    arc.igual(bom.materiais, 1, "quantas instancias de material o mod criou para o componente")

    ruim = reg.ModeloEstilizadorTmpSemGuarda()
    ruim.aplicar(4242, "material-do-prefab")
    segunda_ruim = ruim.aplicar(4242, "instancia-4242")
    arc.igual(segunda_ruim, "aplicou",
              "a isca: SEM o guarda, a segunda chamada tem de RE-aplicar (acumular)")
    arc.exigir(ruim.aplicacoes == 2,
               "a isca precisa mostrar 2 aplicacoes acumuladas, veio %d" % ruim.aplicacoes)

    print("guarda por InstanceID no TMP (%d aplicacoes registradas na 2a chamada) e no legado; "
          "tamanho parte do original; modelo: 1a=%s 2a=%s aplicacoes=%d (sem guarda: 2a=%s "
          "aplicacoes=%d); %d defeito(s) plantado(s) reprovam"
          % (bom.aplicacoes, primeira, segunda, bom.aplicacoes, segunda_ruim, ruim.aplicacoes, 2))


if __name__ == "__main__":
    arc.main(META, corpo)
