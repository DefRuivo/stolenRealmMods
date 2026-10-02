#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""NAO REGRIDE O QUE O DONO APROVOU: o texto das notas e a troca de fonte dos NORMAIS (TST-7, cenario 7).

O QUE ESTE TESTE GARANTE
------------------------
O BF-1/BF-2 mudaram o comportamento do texto ESTILIZADO (que passou a ser convertido com
transporte). O que NAO podia mudar - porque o dono ja aprovou em tela - e:

  * a TROCA DE FONTE DOS TEXTOS NORMAIS: o texto sem efeito continua sendo convertido pelo
    caminho de sucesso (`t.font = _serifFont`, `UpdateMeshPadding()` para o contorno nao ser
    cortado na borda do mesh, `SetVerticesDirty()`);
  * o REGISTRO DA FONTE ORIGINAL como fallback (`RegistrarFallback`): e o que impede
    icones/simbolos que a Times nao tem virarem quadradinhos - promessa da 1.0.0;
  * o TEXTO DAS NOTAS: o resumo da varredura que o dono le no log continua dizendo os TRES
    desfechos (convertidos, pulados pelo escape, intocados por efeito nao transportavel);
  * a promessa SEM GAMEPLAY: o unico gancho Harmony do mod e a LOCALIZACAO da UI
    (`OptionsManager.Localize`), nunca um metodo de gameplay.

NOTA DE ESCOPO ("o texto das notas"). O BetterFont nao tem "notas de texto" no sentido do
plano (essas sao do BetterTooltips); o "texto" que este mod escreve e o resumo da varredura e
as linhas de diagnostico, e e ele que fica vigiado aqui.

A contra-prova embutida remove o padding do caminho de sucesso e remove a adicao do fallback
- as checagens TEM de reprovar nas duas. A rodada fisica esta em
`tools/testes/bf-prova-reprovando.log`.
"""
import regras_bf_estilo as reg

import arcabouco as arc

META = {
    "nome": "bf-nao-regride",
    "categoria": "pura",
    "requer": [],
    "descricao": "TST-7: nao regride o que o dono aprovou - a troca de fonte dos textos NORMAIS (com padding), o fallback da fonte original, o resumo da varredura e zero mudanca de gameplay",
}


def corpo():
    src = reg.fonte()
    arc.exigir(len(src) > 5000, "o fonte do BetterFont veio vazio/curto: a leitura mudou de lugar?")

    # ---- 1) o texto NORMAL continua convertido pelo caminho de sucesso.
    caso_normal = reg.Texto("texto normal (UI comum, sem efeito)")
    arc.igual(reg.decidir(caso_normal), reg.CONVERTE_SIMPLES,
              "o texto normal tem de continuar sendo convertido (caminho de sucesso)")

    # ---- 2) a estrutura do caminho de sucesso e o fallback.
    falhas = reg.falhas_do_nao_regride(src)
    arc.exigir(not falhas, "o que o dono aprovou regrediu em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))
    # (o padding e a copia do caminho de sucesso sao vigiados por `falhas_da_decisao`)
    falhas_decisao = reg.falhas_da_decisao(src)
    arc.exigir(not falhas_decisao, "o caminho de sucesso regrediu: %s" % " | ".join(falhas_decisao))

    # ---- 3) CONTRA-PROVAS EMBUTIDAS.
    sem_padding = reg.defeito_sem_padding(src)
    arc.exigir(sem_padding != src, "o plantio da remocao do padding nao achou onde agir")
    arc.exigir(any("padding" in f for f in reg.falhas_da_decisao(sem_padding)),
               "remover o `UpdateMeshPadding()` do caminho de sucesso passou (o contorno seria "
               "cortado na borda do mesh)")

    sem_fallback = reg.defeito_sem_fallback(src)
    arc.exigir(sem_fallback != src, "o plantio da remocao do fallback nao achou onde agir")
    arc.exigir(any("fallback" in f for f in reg.falhas_do_nao_regride(sem_fallback)),
               "remover a adicao da fonte original ao fallback passou (icones/simbolos virariam "
               "quadradinhos)")

    print("texto normal segue no caminho de sucesso (font + padding + redesenho), fallback da "
          "fonte original registrado, resumo da varredura com os tres desfechos e o unico gancho e "
          "`OptionsManager.Localize` (zero gameplay); %d defeito(s) plantado(s) reprovam" % 2)


if __name__ == "__main__":
    arc.main(META, corpo)
