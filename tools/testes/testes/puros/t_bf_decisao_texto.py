#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A DECISAO POR TEXTO do BetterFont - as quatro saidas - e o ESCAPE (TST-7, cenarios 1 e 4).

O QUE ESTE TESTE GARANTE
------------------------
O `FontSweep` do `BetterFont/Plugin.cs` decide, para cada texto TMP, entre QUATRO desfechos:

    converter-com-transporte   o texto tinha EFEITO no material (o jogo em combate, ou
                               QUALQUER mod que clonou o material por componente) e o efeito
                               foi reaplicado no material novo por componente;
    converter-simples          o texto nao tinha efeito para transportar (a UI comum);
    nao-tocar                  o efeito existe mas NAO pode ser reproduzido -> o texto
                               fica exatamente como esta (copia parcial sairia pior);
    escape                     `PularTextosEstilizados` ligado: o texto estilizado fica
                               100% intocado (o comportamento antigo da 1.0.1).

Material e classe NATIVA do Unity: nao se instancia fora do jogo. O que roda aqui e a
funcao pura `regras_bf_estilo.decidir`, TRANSCRICAO do `FontSweep`, com os tres casos do
TST-7 e o escape; e `falhas_da_decisao` amarra a transcricao a ESTRUTURA do fonte vivo (a
ORDEM escape-antes-do-portao, os `continue` de quem nao e tocado, e o `efeitoPresente &&`
do portao). Fonte vivo = o que sera compilado, nao uma copia.

OS TRES CASOS (cenario 1) E O ESCAPE (cenario 4)
------------------------------------------------
  (a) texto normal (material e o da propria fonte, sem efeito)      -> converter-simples
  (b) efeito aplicado por OUTRO mod (copia por componente), ok      -> converter-com-transporte
  (c) efeito presente que a copia NAO reproduz                      -> nao-tocar
  (4) ESCAPE LIGADO: o estilizado volta a ser pulado, o resto nao muda; DESLIGADO (o default
      novo) vale o caso (b). O default lido do fonte e `false` (ver o teste dos defaults).

O ESCOPO CORRIGIDO DEPOIS DO BF-2: "shader diferente" NAO e recusa. O BF-1 recusava por
variante de shader e deixava os textos de combate na fonte original - o defeito que o BF-2
consertou. O caso abaixo exige que o texto com shader diferente e efeito transportavel seja
CONVERTIDO (best-effort), e a contra-prova embutida mostra que um modelo que voltasse a
recusar por shader seria REPROVADO por este teste.

COMO ELE PROVA (regra do projeto: todo teste tem de ser mostrado reprovando)
----------------------------------------------------------------------------
Cada defeito e plantado EM MEMORIA sobre o fonte (`regras_bf_estilo.defeito_*`) e as
checagens TEM de reprovar - pelo motivo certo. O plantio fisico no `BetterFont/Plugin.cs`
(rodar, ver REPROVOU; restaurar, ver PASSOU) esta em `tools/testes/bf-prova-reprovando.log`.

O que NAO se prova aqui (e so o dono confirma, em tela): o nome do inimigo e o numero do
dado ganharem a serifa E o halo em combate.
"""
import regras_bf_estilo as reg

import arcabouco as arc

META = {
    "nome": "bf-decisao-texto",
    "categoria": "pura",
    "requer": [],
    "descricao": "TST-7: a decisao por texto (converter-com-transporte/convert-simples/nao-tocar/escape) e o escape ligado/desligado, como funcao pura sobre o fonte vivo",
}

# ---------------------------------------------------------------------------
# OS CASOS. Cada `Texto` responde, nos termos da decisao, o que o material DAQUELE
# texto tem. `material_proprio`/`shader_diferente` = `EhEstilizado`; `efeito_presente`
# = `TemEfeitoNoMaterial`; `efeito` = o veredito de `EstiloTransportavel`.
# ---------------------------------------------------------------------------
CASO_A_NORMAL = reg.Texto("texto normal (material da propria fonte, sem efeito)")
CASO_B_OUTRO_MOD = reg.Texto("efeito de OUTRO mod (material proprio, transportavel)",
                             material_proprio=True, efeito_presente=True)
CASO_C_NAO_TRANSPORTAVEL = reg.Texto("efeito que a copia nao reproduz",
                                     material_proprio=True, efeito_presente=True,
                                     efeito=reg.NAO_TRANSPORTAVEL)
CASO_D_SHADER_DIFERENTE = reg.Texto("texto de combate (variante de shader diferente), com efeito",
                                    shader_diferente=True, efeito_presente=True)
CASO_E_SO_SHADER = reg.Texto("variante de shader diferente, SEM efeito",
                             shader_diferente=True)
CASO_F_NAO_CLASSIFICADO_COM_EFEITO = reg.Texto(
    "texto NAO classificado cuja PROPRIA fonte traz glow (efeito nao transportavel)",
    material_proprio=False, shader_diferente=False, efeito_presente=True,
    efeito=reg.NAO_TRANSPORTAVEL)
CASO_G_JA_SERIFA = reg.Texto("ja esta na serifa", ja_na_serifa=True)


def decidir_com_o_defeito_do_bf1(texto, preservar_estilo=True, pular_estilizados=False):
    """O BF-1: variante de shader diferente era RECUSA (o defeito que o BF-2 consertou).

    Nao mexe no modelo de `regras_bf_estilo`: ANTEPOE a recusa por shader. Se o teste
    estivesse passando por construcao, este modelo daria o mesmo resultado do corrigido -
    e ele NAO da (o caso do texto de combate sai `nao-tocar` nele).
    """
    if texto.shader_diferente and texto.efeito_presente:
        return reg.NAO_TOCAR
    return reg.decidir(texto, preservar_estilo, pular_estilizados)


def corpo():
    src = reg.fonte()
    arc.exigir(len(src) > 5000, "o fonte do BetterFont veio vazio/curto: a leitura mudou de lugar?")

    # ---- cenario 1: os tres casos, na config default (PreservarEstilo=true, escape=false)
    arc.igual(reg.decidir(CASO_A_NORMAL), reg.CONVERTE_SIMPLES,
              "(a) texto normal (material e o da propria fonte)")
    arc.igual(reg.decidir(CASO_B_OUTRO_MOD), reg.CONVERTE_COM_TRANSPORTE,
              "(b) efeito aplicado por OUTRO mod (material proprio, transportavel) tem de ser "
              "CONVERTIDO e os efeitos transportados")
    arc.igual(reg.decidir(CASO_C_NAO_TRANSPORTAVEL), reg.NAO_TOCAR,
              "(c) efeito presente que a copia NAO reproduz: o texto NAO pode ser tocado")

    # O portao olha o EFEITO PRESENTE no material, nao a classificacao do texto (defeito BF-2):
    # um texto NAO estilizado cuja propria fonte traz o efeito tambem e protegido.
    arc.igual(reg.decidir(CASO_F_NAO_CLASSIFICADO_COM_EFEITO), reg.NAO_TOCAR,
              "texto NAO classificado com efeito no material tem de ser protegido tambem "
              "(o portao nao pode olhar a classificacao do texto)")

    # ESCOPO CORRIGIDO (BF-2): shader diferente NAO e recusa.
    arc.igual(reg.decidir(CASO_D_SHADER_DIFERENTE), reg.CONVERTE_COM_TRANSPORTE,
              "texto de combate (variante de shader diferente) COM efeito transportavel tem de "
              "ser CONVERTIDO - variante de shader nao e recusa no BF-2")
    arc.igual(reg.decidir(CASO_E_SO_SHADER), reg.CONVERTE_SIMPLES,
              "variante de shader diferente SEM efeito: converte pelo caminho simples")
    arc.igual(reg.decidir(CASO_G_JA_SERIFA), reg.JA_NA_SERIFA, "texto ja na serifa")
    # PreservarEstilo=false: o efeito NAO e transportado -> o texto ainda e convertido (simples).
    arc.igual(reg.decidir(CASO_B_OUTRO_MOD, preservar_estilo=False), reg.CONVERTE_SIMPLES,
              "com PreservarEstilo=false o texto com efeito e convertido SEM transporte")

    # ---- cenario 4: o ESCAPE. Ligado, o ESTILIZADO volta a ser pulado; o NAO estilizado nao muda.
    # `EhEstilizado` inclui material proprio E variante de shader diferente - os dois sao pulados.
    estilizados = (CASO_B_OUTRO_MOD, CASO_C_NAO_TRANSPORTAVEL, CASO_D_SHADER_DIFERENTE, CASO_E_SO_SHADER)
    for caso in estilizados:
        arc.igual(reg.decidir(caso, pular_estilizados=True), reg.ESCAPE,
                  "ESCAPE ligado: o texto estilizado '%s' tem de ser pulado (comportamento antigo)" % caso.rotulo)
    for caso in (CASO_A_NORMAL,):
        arc.igual(reg.decidir(caso, pular_estilizados=True), reg.CONVERTE_SIMPLES,
                  "ESCAPE ligado: o texto NAO estilizado '%s' continua sendo convertido (o resto "
                  "nao muda)" % caso.rotulo)
    # Desligado (o default novo): o caso (b) de volta.
    arc.igual(reg.decidir(CASO_B_OUTRO_MOD, pular_estilizados=False), reg.CONVERTE_COM_TRANSPORTE,
              "ESCAPE desligado (default): o texto com efeito de outro mod e convertido E transportado")

    # ---- a ligacao com o FONTE VIVO: a decisao esta na ORDEM e com os freios certos.
    falhas = reg.falhas_da_decisao(src)
    arc.exigir(not falhas, "a decisao do `FontSweep` regrediu em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))

    # ---- CONTRA-PROVA EMBUTIDA: o defeito plantado tem de REPROVAR, pelo motivo certo.
    com_gate_antigo = reg.defeito_escape_como_gate(src)
    arc.exigir(com_gate_antigo != src, "o plantio do portao antigo nao achou onde agir")
    falhas_portao = reg.falhas_da_decisao(com_gate_antigo)
    arc.exigir(any("efeitoPresente" in f or "classificacao" in f for f in falhas_portao),
               "o portao voltando a olhar a classificacao do texto passou: %s"
               % " | ".join(falhas_portao))

    com_escape_sem_continue = reg.defeito_escape_sem_continue(src)
    arc.exigir(com_escape_sem_continue != src, "o plantio do escape sem `continue` nao achou onde agir")
    falhas_escape = reg.falhas_da_decisao(com_escape_sem_continue)
    arc.exigir(any("ESCAPE" in f and "continue" in f for f in falhas_escape),
               "o ramo do escape sem `continue` passou (o texto pulado seria tocado): %s"
               % " | ".join(falhas_escape))

    # ---- CONTRA-PROVA DO MODELO: um modelo que voltasse a recusar por shader (o BF-1) tem de
    #      dar resultado DIFERENTE do corrigido - senao o caso (d) estaria passando por construcao.
    arc.igual(decidir_com_o_defeito_do_bf1(CASO_D_SHADER_DIFERENTE), reg.NAO_TOCAR,
              "o modelo do defeito do BF-1 (recusa por shader) tinha de dar `nao-tocar`")
    arc.exigir(decidir_com_o_defeito_do_bf1(CASO_D_SHADER_DIFERENTE) != reg.decidir(CASO_D_SHADER_DIFERENTE),
               "o modelo do defeito e o corrigido concordam no texto de combate: o caso (d) nao "
               "distingue os dois (passaria por construcao)")

    print("decisao: normal=converter-simples, efeito-de-outro-mod=converter-com-transporte, "
          "nao-transportavel=nao-tocar, shader-diferente=converte (nao e recusa); ESCAPE ligado "
          "pula os estilizados e mantem os normais; %d defeito(s) plantado(s) reprovam pelo motivo certo"
          % 3)


if __name__ == "__main__":
    arc.main(META, corpo)
