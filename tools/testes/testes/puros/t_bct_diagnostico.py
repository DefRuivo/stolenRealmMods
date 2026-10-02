#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O DIAGNOSTICO DE ARRANQUE DO BETTERCOMBATTEXT (TST-8, cenario 6).

O QUE ESTE TESTE GARANTE
------------------------
O diagnostico de arranque procura os componentes alvo em cena UMA vez, para escrever no log
qual fonte/material/shader cada um usa. A varredura de cena (`Resources.FindObjectsOfTypeAll`)
e cara e roda na THREAD PRINCIPAL - o defeito de desempenho medido foi varrer a cena inteira a
cada 2s PARA SEMPRE (~110 varreduras por arranque). O conserto tem tres pontas:

  1. o INTERVALO entre varreduras (era 2s; virou 5s) e a espera minima (20s);
  2. a PARADA no primeiro sucesso: assim que um alvo aparece em cena o diagnostico roda e a
     varredura encerra de VEZ (`_feito = true;`), com a desistencia em 240s como rede;
  3. a chave de config que ZERA o custo: `1. Geral` > `DiagnosticoNoArranque = false` = nenhuma
     varredura na sessao.

COMO E TESTADO
--------------
Os tres numeros sao LIDOS do fonte (`regras_bct.constantes_do_diagnostico`) - nunca digitados -
e comparados com a ESPEC (`ESPEC_DIAG`, a exigencia: 20s / 5s / 240s). O COMPORTAMENTO sai do
modelo puro `regras_bct.ModeloDiagnostico`, transcrito do `Tentar`, rodado numa linha do tempo
por frame (o gatilho real e o `GUIManager.Update`):

  * sem alvo nenhum, ate 300s: o numero de varreduras tem de ser EXATAMENTE o da formula tirada
    das proprias constantes (`(desistir-espera)/intervalo + 1` = 45) - e 107 com o defeito de 2s;
  * com o alvo aparecendo em 30s: o diagnostico roda UMA vez e a varredura PARA (0 varreduras
    depois disso) - o modelo do defeito continua varrendo;
  * com a chave desligada: ZERO varreduras.

A PARADA e conferida por ESTRUTURA tambem (o `_feito = true;` entre `TemAlvoEmCena()` e
`Rodar()`), porque conferir so o token `_feito = true;` nao vale: ha outro igual no ramo do
config, e ele sozinho satisfazia a busca de substring (a mesma armadilha da REV-56 na trava do
orcamento do BetterFont).

A rodada fisica (o intervalo voltando a 2s e a parada arrancada, o teste reprovando, o fonte
restaurado byte a byte) esta em `tools/testes/bct-prova-reprovando.log`.
"""
import regras_bct as reg

import arcabouco as arc

META = {
    "nome": "bct-diagnostico",
    "categoria": "pura",
    "requer": [],
    "descricao": "TST-8/6: o diagnostico de arranque - intervalo 5s (era 2s), PARADA no primeiro sucesso e a chave que zera a varredura - provado por modelo puro do tempo/estado",
}

ATE = 300.0        # a linha do tempo da simulacao (segundos)


def corpo():
    diag = reg.fonte(reg.DIAG)
    arc.exigir(len(diag) > 3000, "o DiagnosticoArranque.cs veio vazio/curto: a leitura mudou de lugar?")

    valores = reg.constantes_do_diagnostico(diag)
    if valores is None:
        raise arc.Falhou("nao achei as tres constantes do diagnostico em %s: o teste le o "
                         "intervalo do fonte, nunca digita o numero" % reg.DIAG)
    espera, intervalo, desistir = valores
    arc.igual(valores, reg.ESPEC_DIAG,
              "as constantes do diagnostico lidas do fonte (espera, intervalo, desistir)")

    falhas = reg.falhas_do_diagnostico(diag)
    arc.exigir(not falhas, "o diagnostico regrediu: %s" % " | ".join(falhas))

    # ------------------------------------------------ o COMPORTAMENTO (modelo puro)
    pior = reg.simular_arranque(reg.ModeloDiagnostico(espera, intervalo, desistir), ATE)
    esperado = int((desistir - espera) / intervalo) + 1
    arc.igual(pior.varreduras, esperado,
              "varreduras numa cena sem NENHUM alvo, ate %.0fs (formula das constantes do fonte: "
              "(%.0f-%.0f)/%.0f+1)" % (ATE, desistir, espera, intervalo))
    arc.igual(pior.execucoes, 1, "o diagnostico roda UMA vez no pior caso (ao desistir)")
    arc.exigir(pior.varreduras < 50,
               "o diagnostico varreu a cena %d vezes no pior caso: e o defeito de desempenho"
               % pior.varreduras)

    com_alvo = reg.simular_arranque(reg.ModeloDiagnostico(espera, intervalo, desistir), ATE,
                                    tem_alvo_em=30.0)
    arc.igual(com_alvo.execucoes, 1, "execucoes do diagnostico com o alvo em cena aos 30s")
    arc.igual(com_alvo.varreduras, int((30.0 - espera) / intervalo) + 1,
              "varreduras ate o alvo aparecer (o gatilho roda a cada frame)")
    antes = com_alvo.varreduras
    for t in (40.0, 60.0, 120.0, 240.0, 300.0):
        arc.igual(com_alvo.tentar(t, True), None,
                  "varredura aos %.0fs DEPOIS do primeiro sucesso (o diagnostico tem de PARAR)"
                  % t)
    arc.igual(com_alvo.varreduras, antes, "varreduras depois do primeiro sucesso")

    desligado = reg.simular_arranque(reg.ModeloDiagnostico(espera, intervalo, desistir), ATE,
                                     config_ligada=False)
    arc.igual(desligado.varreduras, 0,
              "varreduras com `DiagnosticoNoArranque = false` (a chave tem de ZERAR o custo)")
    arc.igual(desligado.execucoes, 0, "execucoes do diagnostico com a chave desligada")

    # ------------------------------------------------ asISCAS (o defeito transcrito)
    dois_segundos = reg.simular_arranque(reg.ModeloDiagnosticoIntervalo2(espera, desistir), ATE)
    arc.exigir(dois_segundos.varreduras > pior.varreduras * 2,
               "o modelo do defeito (2s) tinha de varrer muito mais que o conserto: %d vs %d"
               % (dois_segundos.varreduras, pior.varreduras))

    sem_parada = reg.simular_arranque(reg.ModeloDiagnosticoSemParada(espera, intervalo, desistir),
                                      ATE)
    sem_parada.tentar(300.0, True)
    pos_sucesso = reg.simular_arranque(reg.ModeloDiagnosticoSemParada(espera, intervalo, desistir),
                                       ATE, tem_alvo_em=30.0)
    arc.exigir(pos_sucesso.varreduras > com_alvo.varreduras + 5,
               "o modelo sem parada tinha de CONTINUAR varrendo depois do sucesso (%d varreduras, "
               "contra %d do conserto)" % (pos_sucesso.varreduras, com_alvo.varreduras))
    arc.exigir(sem_parada.varreduras > 50,
               "o modelo sem parada tinha de varrer sem fim, veio %d" % sem_parada.varreduras)

    # ------------------------------------------------ contra-provas no FONTE
    for rotulo, plantar, marca in (
            ("o intervalo voltando a 2s", reg.defeito_diagnostico_2s, "IntervaloChecagem"),
            ("a varredura deixando de encerrar", reg.defeito_diagnostico_sem_parada, "_feito"),
            ("a chave deixando de desligar", reg.defeito_diagnostico_ignora_config, "DiagnosticoNoArranque")):
        com_defeito = plantar(diag)
        arc.exigir(com_defeito != diag, "o plantio do defeito (%s) nao achou onde agir" % rotulo)
        falhas_defeito = reg.falhas_do_diagnostico(com_defeito)
        arc.exigir(falhas_defeito, "as checagens PASSARAM com o defeito (%s)" % rotulo)
        arc.exigir(any(marca in f for f in falhas_defeito),
                   "o defeito (%s) nao foi apontado em '%s': %s"
                   % (rotulo, marca, " | ".join(falhas_defeito)))

    # O defeito do intervalo tem de mudar as CONSTANTES LIDAS (prova de que o teste le o lugar
    # certo, e nao um numero digitado).
    arc.exigir(reg.constantes_do_diagnostico(reg.defeito_diagnostico_2s(diag)) != reg.ESPEC_DIAG,
               "o defeito do intervalo nao mudou as constantes lidas do fonte: o teste esta lendo "
               "o lugar errado")

    print("constantes lidas do fonte=(%.0f, %.0f, %.0f) (ESPEC=%s); modelo: pior caso ate %.0fs=%d "
          "varredura(s) (formula %d), com alvo em 30s=%d e PARA (%d depois), chave desligada=%d; "
          "iscas: 2s=%d, sem parada=%d varredura(s); 3 defeito(s) plantado(s) reprovam"
          % (espera, intervalo, desistir, reg.ESPEC_DIAG, ATE, pior.varreduras, esperado,
             com_alvo.varreduras, com_alvo.varreduras - antes, desligado.varreduras,
             dois_segundos.varreduras, sem_parada.varreduras))


if __name__ == "__main__":
    arc.main(META, corpo)
