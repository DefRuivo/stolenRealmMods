#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BF-2R/BF-3: o teto do diagnostico do BetterFont ainda escondia a linha de COMBATE - e o conserto.

O QUE ESTE TESTE GARANTE
------------------------
A revisao independente da BF-2 mostrou que os DOIS tetos do diagnostico NAO faziam o que
prometiam, e que o defeito era funcional (nao cosmetico): a linha `[diag]` do texto de combate -
a que o dono liga `LogDiagnosticoEstilo` para ler - continuava podendo nao sair.

Tres causas, todas medidas no fonte e/ou nos logs do dono:

  (A) [BF-2R] O TETO DE ROTINA ERA INALCANCAVEL. `deEfeito` era tirado do CONTEUDO da linha
      (`copiados`/`naoTransportados`/`registros`) e `copiados` NUNCA vem vazio num texto
      convertido (as cores de face `_FaceColor`/`_FaceDilate` existem nos dois shaders). Ou seja:
      TODA linha virava "de efeito" e o teto de 120 (rotina) nunca era usado.
  (B) [BF-2R] O TETO DE EFEITO ERA DA SESSAO. A medicao REAL de quantos textos tem efeito no
      material num boot esta em `tools/fixtures/bf-efeito-no-boot.json` (365 de 488) - e o teste
      antigo DIGITAVA `efeitos_no_boot = 5`. Com 365 > 300 o teto de efeito E alcancado na cena de
      boot (o log do dono traz "limite de 300 linhas de efeito atingido"): e por isso o orcamento
      tem de ser POR CENA.
  (C) [BF-3] O PULADO PELO ESCAPE CONTAVA COMO EFEITO. Com `PularTextosEstilizados=true` (a
      config do dono) a varredura pula ~484 textos numa passada (o log do dono mede 484 e 624 -
      `tools/fixtures/bf-varredura-em-jogo.log`) e o call site do escape passava "de efeito": os
      pulados esgotavam o teto de 300 ANTES da linha de combate - que, nessa config, E um pulado.
      Um texto pulado pelo escape nao transportou efeito nenhum: ele tem teto PROPRIO
      (`TetoDiagEscape`) e nao disputa o orcamento de efeito.

  (D) [FIX-6/FIX-8, achado 2 da REV-56] A CONTA DO TETO DO ESCAPE. O valor era 700, dimensionado
      pelo MAIOR pulo medido numa varredura - 624 (varredura de 640 textos). O FIX-6 subiu para 900
      com a conta "793 objetos x a fracao de pulo = 773". A FIX-8 refutou as DUAS pernas: (a) a
      fracao nao e sobre o TOTAL, porque o texto que ja esta na serifa nunca chega ao escape (o
      `if (t.font == _serifFont) continue;` vem antes) - a base certa e 640 - 12 = 628 e a fracao e
      624/628 = 0,9936, nao 0,975; (b) o 793 nao estava versionado e fechou 353 + 61 + 379 = 793
      EXATO, com ZERO pulados - mesmo tomado como base, so 793 - 379 = 414 chegam ao escape, que a
      0,9936 dao ~411 pulados. Ou seja: o teto so precisa passar do maior pulo MEDIDO numa cena
      (624) - o antigo 700 JA cobria, e o 900 NAO e necessario (fica como folga deliberada de limite
      de log). ESTE teste CONFERE A CONTA com o log VERSIONADO (`regras_bf.maior_pulado_medido()` /
      `candidatos_ao_escape()` / `fracao_de_pulo_da_maior_varredura()`, nada digitado).

  (E) [FIX-6/FIX-8, achado 1 da REV-56] A TRAVA DO ORCAMENTO CONFERIA TOKEN, NAO COMPORTAMENTO. A
      REV-56 plantou TRES variantes com os tokens de pe (o `GetActiveScene()` num COMENTARIO com
      `cena` fixa; o ramo do escape incrementando o contador de EFEITO; o corte do escape preso ao
      TETO DE EFEITO) e a checagem da fonte devolveu lista VAZIA nas tres. A FIX-8 fechou a CLASSE
      (e nao a grafia): o bloco de zeramento dentro de um `if (false)`, a cena gravada ANTES do guarda
      (que o deixa sempre verdadeiro) e a chamada do reset DEPOIS do uso do contador tambem passavam.
      Por isso `regras_bf.falhas_da_fonte` roda a conferencia de COMPORTAMENTO
      (`regras_bf.falhas_do_comportamento`): le o CODIGO EFETIVO (sem comentarios), EXECUTA o
      orcamento e decide ALCANCE + ORDEM do zeramento. Todas as variantes sao plantadas aqui EMBAIXO
      e TEM de reprovar - a "variante D" (reset so na primeira cena) e as duas novas (`if (false)` e
      cena antes do guarda) e o reset depois do uso caem pela MESMA medida, que e o ponto: fechar a
      classe, nao reconhecer a forma.

O conserto (BF-2R + BF-3): a classificacao e EXPLICITA e de TRES vias (`TipoLinhaDiag`:
ROTINA/EFEITO/ESCAPE - quem chama diz se ha efeito no material), o orcamento e POR CENA
(`OrcamentoDoDiagnosticoPorCena` zera os tres contadores quando a cena ativa muda) e o pulado pelo
escape tem teto proprio, dimensionado pela varredura medida.

COMO ELE PROVA (e o que ele NAO prova)
--------------------------------------
`Material` e classe nativa do Unity: nao se instancia fora do jogo, entao o C# nao roda aqui. O
que roda e o modelo `regras_bf.ModeloOrcamentoDiag` - a transcricao da regra - e os casos sao
montados com a escala REAL, lida dos arquivos versionados (`bf-efeito-no-boot.json` e
`bf-varredura-em-jogo.log`) e com os TETOS lidos do fonte vivo. Nada e digitado:

  * cena de boot (config default): os textos do universo medido, com 365 de efeito no material;
  * cena de combate: a linha do texto de combate (material com halo) -> TEM de sair;
  * cena de combate (config do dono): 484 pulados pelo escape e, depois deles, a linha do texto
    de combate - que naquela config tambem E um pulado -> TEM de sair, sem consumir o orcamento
    de efeito.

Cada caso roda tambem nos modelos do DEFEITO (a BF-2, com o orcamento da sessao + classificacao
pelo conteudo; a BF-2R, com o escape contado como efeito; e o reset so na primeira cena): ali a
linha de combate NAO sai - a isca embutida, sem a qual o teste poderia estar passando por
construcao. A outra metade da ligacao com o fonte vivo esta em `regras_bf.falhas_da_fonte` (reset
por cena ALCANCAVEL + classificacao explicita de tres vias + call sites) e na isca externa
`tools/testes/contra-prova/cp_bf_diag_orcamento.py`.
"""
import regras_bf

import arcabouco as arc

META = {
    "nome": "bf-diag-orcamento",
    "categoria": "pura",
    "requer": [],
    "descricao": "BF-2R/BF-3: orcamento do diagnostico POR CENA, com teto proprio para o pulado pelo escape - a linha de combate sai depois de centenas de textos",
}

# Nomes de cena sao rotulos do caso (o modelo nao conhece as cenas do jogo): o que importa e que
# a segunda cena seja DIFERENTE da primeira, que e o que `SceneManager.GetActiveScene()` entrega.
CENA_BOOT = "cena-de-boot"
CENA_COMBATE = "cena-de-combate"
LINHA_DO_COMBATE = "NOME DO INIMIGO (material com halo/contorno)"
LINHA_DO_COMBATE_PULADA = "NOME DO INIMIGO (pulado pelo escape: material estilizado)"


def escala():
    """A escala REAL, dos arquivos versionados - nunca digitada aqui."""
    somas = regras_bf.textos_por_varredura()
    arc.exigir(somas, "o log versionado %s nao tem linha de resumo de varredura (a prova em jogo "
                      "sumiu do repositorio)" % regras_bf.LOG_VARREDURA)
    pulados = regras_bf.pulados_por_varredura()
    arc.exigir(pulados, "o log versionado nao tem o campo de PULADOS por varredura (a escala da "
                        "config do dono sumiu)")
    efeito = regras_bf.textos_com_efeito_no_boot()
    arc.exigir(efeito, "a medicao dos textos COM EFEITO no boot nao esta em %s (era ela que o teste "
                       "digitava como 5)" % regras_bf.FIXTURE_EFEITO)
    return max(somas), max(pulados), efeito


def cenario_config_default(modelo, efeito):
    """Config default (PularTextosEstilizados=false): a cena de boot com a escala MEDIDA, depois o
    combate. A cena de boot gasta o teto de efeito (e a medicao real: 365 > 300); a de combate
    comeca com o orcamento zerado e a linha do texto de combate tem de sair."""
    universo = efeito["universo_de_textos"]
    com_efeito = efeito["com_efeito_no_material"]
    for i in range(universo - com_efeito):
        modelo.logar(CENA_BOOT, "boot-rotina-%d" % i, regras_bf.ROTINA)
    for i in range(com_efeito):
        modelo.logar(CENA_BOOT, "boot-efeito-%d" % i, regras_bf.EFEITO)
    modelo.logar(CENA_COMBATE, LINHA_DO_COMBATE, regras_bf.EFEITO)
    return modelo


def cenario_config_do_dono(modelo, pulados):
    """Config do DONO (PularTextosEstilizados=true), numa UNICA cena: a varredura pula os textos
    pelo escape e a linha que interessa - o texto de combate - TAMBEM e um pulado. Ela tem de sair,
    e o pulo nao pode consumir o orcamento de EFEITO."""
    for i in range(pulados):
        modelo.logar(CENA_COMBATE, "escape-%d" % i, regras_bf.ESCAPE)
    modelo.logar(CENA_COMBATE, LINHA_DO_COMBATE_PULADA, regras_bf.ESCAPE)
    return modelo


def corpo():
    src = regras_bf.fonte()
    arc.exigir(len(src) > 5000, "o fonte do BetterFont veio vazio/curto: a leitura mudou de lugar?")

    # --- os TRES tetos saem do FONTE VIVO (nunca digitados) --------------------------------
    tetos = regras_bf.tetos_do_diagnostico(src)
    arc.exigir(tetos is not None,
               "nao achei TetoDiagRotina/TetoDiagEfeito/TetoDiagEscape no fonte vivo: os tetos do "
               "diagnostico sumiram ou mudaram de nome")
    teto_rotina, teto_efeito, teto_escape = tetos

    textos_na_varredura, pulados_na_varredura, efeito = escala()
    com_efeito = efeito["com_efeito_no_material"]
    universo = efeito["universo_de_textos"]

    arc.exigir(textos_na_varredura > teto_efeito,
               "a medicao em jogo (%d textos numa varredura) nao passa o teto de efeito (%d): o "
               "caso perdeu o que ele existe para provar" % (textos_na_varredura, teto_efeito))
    arc.exigir(com_efeito > teto_efeito,
               "a MEDICAO dos textos com efeito (%d) nao passa o teto de efeito (%d): o caso da "
               "BF-2R perdeu o que ele existe para provar" % (com_efeito, teto_efeito))
    arc.exigir(universo - com_efeito > 0,
               "a medicao diz que TODOS os textos tem efeito - a classificacao de rotina nao seria "
               "exercitada")
    # BF-3: o teto do escape tem de CABER a varredura medida do dono (senao o pulado que
    # interessa fica de fora por orcamento, que e o defeito).
    arc.exigir(pulados_na_varredura < teto_escape,
               "a varredura medida do dono (%d pulados numa passada) NAO cabe no teto do escape "
               "(%d): a linha do texto de combate - que nessa config E um pulado - fica de fora"
               % (pulados_na_varredura, teto_escape))
    # FIX-8 (achado 2 da FIX-7R): o teto do escape se dimensiona pelo MAIOR pulo de UMA cena no log
    # VERSIONADO - nao por projecao. O FIX-6 exigia aqui uma "projecao" (793 x 0,975 = 773) que era
    # falsa DUAS vezes: (a) a fracao usava o TOTAL no denominador, mas o texto que ja esta na serifa
    # nunca chega ao escape (o `if (t.font == _serifFont) continue;` vem antes) - a base certa e o
    # total menos os que ja estao na serifa; (b) o 793 so existia em log gitignored e fechava
    # 353 + 61 + 379 = 793 EXATO, com ZERO pulados. A conta certa, so com o log versionado: maior
    # varredura 640 textos, 12 ja na serifa -> 628 candidatos, 624/628 = 0,9936 de pulo. Como o maior
    # pulo MEDIDO de uma cena e 624, o teto so precisa passar de 624 (o antigo 700 ja cobria).
    maior_pulo = regras_bf.maior_pulado_medido()
    candidatos = regras_bf.candidatos_ao_escape()
    fracao = regras_bf.fracao_de_pulo_da_maior_varredura()
    arc.exigir(maior_pulo and candidatos and fracao is not None,
               "nao consegui ler do log versionado (%s) o maior pulo por cena / os candidatos ao "
               "escape / a fracao de pulo: a conta do teto do escape ficou sem base" % regras_bf.LOG_VARREDURA)
    arc.exigir(candidatos == textos_na_varredura - (regras_bf.maior_varredura() or {}).get("ja_na_serifa", 0),
               "os candidatos ao escape (%d) nao descontam quem ja esta na serifa da maior varredura "
               "(%d textos): a base do pulo voltou a ser o TOTAL" % (candidatos, textos_na_varredura))
    arc.exigir(maior_pulo < teto_escape,
               "o maior pulo MEDIDO numa cena (%d) NAO cabe no teto do escape (%d): a linha do "
               "texto de combate - que nessa config E um pulado - fica de fora por orcamento"
               % (maior_pulo, teto_escape))

    # --- 1) CONFIG DEFAULT: o conserto ------------------------------------------------------
    agora = cenario_config_default(regras_bf.ModeloOrcamentoDiag(teto_rotina, teto_efeito, teto_escape), efeito)
    arc.exigir(agora.linhas and agora.linhas[-1] == LINHA_DO_COMBATE,
               "a linha do texto de COMBATE nao saiu mesmo com o orcamento por cena: serie de "
               "linhas=%r" % (agora.linhas[-3:],))
    arc.exigir(CENA_COMBATE in agora.cenas_zeradas,
               "o modelo nao registrou a troca de cena: %r" % (agora.cenas_zeradas,))
    # A MEDICAO manda: num boot real o teto de efeito E alcancado (365 > 300) - por isso o
    # orcamento tem de ser POR CENA, e nao "sobrar orcamento" no boot.
    arc.exigir(agora.cortes_efeito > 0,
               "a escala MEDIDA (%d textos com efeito) nao gastou o teto de efeito (%d): a medicao "
               "e o caso nao combinam" % (com_efeito, teto_efeito))

    # --- 2) CONFIG DO DONO: o caso que a BF-3 fecha -----------------------------------------
    dono = cenario_config_do_dono(regras_bf.ModeloOrcamentoDiag(teto_rotina, teto_efeito, teto_escape),
                                  pulados_na_varredura)
    arc.exigir(dono.linhas and dono.linhas[-1] == LINHA_DO_COMBATE_PULADA,
               "a linha do texto de combate nao saiu na config do DONO mesmo com o teto proprio do "
               "escape: serie de linhas=%r" % (dono.linhas[-3:],))
    arc.exigir(dono.cortes_escape == 0,
               "a varredura medida (%d pulados) cortou %d linha(s) de escape: o teto do escape nao "
               "cabe a escala do dono" % (pulados_na_varredura, dono.cortes_escape))
    arc.exigir(dono.efeito == 0 and dono.cortes_efeito == 0,
               "o pulado pelo escape consumiu o orcamento de EFEITO (%d linha(s), %d corte(s)): "
               "pular nao e 'de efeito' - um pulado nao transportou efeito nenhum"
               % (dono.efeito, dono.cortes_efeito))

    # --- 3) AS ISCAS EMBUTIDAS: o MESMO caso nos modelos do DEFEITO -------------------------
    # (a) BF-2: orcamento da sessao + classificacao pelo conteudo
    antes = cenario_config_default(regras_bf.ModeloOrcamentoDiagAntesBF2R(teto_rotina, teto_efeito, teto_escape), efeito)
    arc.exigir(LINHA_DO_COMBATE not in antes.linhas,
               "o modelo do defeito da BF-2 NAO reproduz o defeito: a linha de combate saiu nele "
               "(o teste estaria passando por construcao)")
    arc.exigir(antes.cortes_efeito > 0,
               "o modelo do defeito da BF-2 nao gastou o teto de efeito na cena de boot: %d corte(s)"
               % antes.cortes_efeito)
    arc.exigir(antes.cortes_rotina == 0,
               "o teto de ROTINA foi usado no modelo do defeito da BF-2 (%d corte(s)): ele tinha de "
               "ser inalcancavel - e isso e o defeito que a revisao mediu" % antes.cortes_rotina)

    # (b) BF-3: o pulado pelo escape contado como EFEITO, na config do dono
    dono_defeito = cenario_config_do_dono(
        regras_bf.ModeloOrcamentoDiagEscapeComoEfeito(teto_rotina, teto_efeito, teto_escape),
        pulados_na_varredura)
    arc.exigir(LINHA_DO_COMBATE_PULADA not in dono_defeito.linhas,
               "o modelo do defeito da BF-3 NAO reproduz o defeito: a linha do texto de combate "
               "saiu nele (o teste estaria passando por construcao)")
    arc.exigir(dono_defeito.cortes_efeito > 0,
               "o modelo do defeito da BF-3 nao gastou o teto de efeito com os pulados: %d corte(s)"
               % dono_defeito.cortes_efeito)

    # (c) BF-3: o reset so na PRIMEIRA cena (o ponto cego da trava da BF-2R)
    primeira = cenario_config_default(
        regras_bf.ModeloOrcamentoDiagResetSoNaPrimeiraCena(teto_rotina, teto_efeito, teto_escape), efeito)
    arc.exigir(LINHA_DO_COMBATE not in primeira.linhas,
               "o modelo do reset SO NA PRIMEIRA cena nao reproduz o defeito: a linha de combate "
               "saiu nele")

    # --- 4) A LIGACAO COM O FONTE VIVO: a estrutura do conserto esta de pe -------------------
    falhas = regras_bf.falhas_da_fonte(src)
    arc.exigir(not falhas, "o fonte do BetterFont regrediu em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))

    # Os defeitos, reinjetados no texto do fonte, tem de REPROVAR as checagens - cada um pelo SEU
    # motivo (um "reprova por qualquer coisa" nao vale).
    # As variantes de RESET (a "D" e as tres da FIX-8) sao a MESMA CLASSE e caem pela MESMA medida
    # - o zeramento nao alcancado/antes do uso. O motivo e um so de proposito: e a medida que as
    # une, e nao a forma de cada uma.
    MOTIVO_ZERAMENTO = "ZERAMENTO NAO e ALCANCADO"
    plantados = [
        ("o orcamento da BF-2 (sessao + classificacao pelo conteudo)",
         regras_bf.fonte_com_o_orcamento_da_bf2, ("SESSAO", "CONTEUDO")),
        ("o pulado pelo escape contado como EFEITO (BF-3)",
         regras_bf.fonte_com_o_escape_como_efeito, ("nao como `TipoLinhaDiag.Escape`",)),
        ("o reset so na PRIMEIRA cena (`if (_diagCena != null)`)",
         regras_bf.fonte_com_o_reset_so_na_primeira_cena, (MOTIVO_ZERAMENTO,)),
        ("o reset INALCANCAVEL (`if (true) return`)",
         regras_bf.fonte_com_o_reset_inalcancavel, (MOTIVO_ZERAMENTO,)),
        # FIX-6 (achado 1): as TRES variantes da REV-56, com TODOS os tokens de pe. A checagem
        # antiga (substring) devolvia lista VAZIA nas tres; a conferencia de COMPORTAMENTO tem de
        # reprovar cada uma pela sua medida.
        ("(A) a cena lida vira COMENTARIO e `cena` fica FIXA (reset so na 1a cena)",
         regras_bf.fonte_com_a_cena_fixa_no_comentario, (MOTIVO_ZERAMENTO,)),
        ("(B) o ramo do escape volta a incrementar o contador de EFEITO",
         regras_bf.fonte_com_o_escape_incrementando_o_efeito, ("o contador do tipo `Escape` NAO corta",)),
        ("(C) o corte do escape passa a depender TAMBEM do TETO DE EFEITO",
         regras_bf.fonte_com_o_corte_do_escape_no_teto_de_efeito, ("cena MISTA",)),
        # FIX-8 (achado 1 da FIX-7R) - a CLASSE que a checagem de TOKEN nao fechava. As tres mantem
        # TODOS os tokens do zeramento (a comparacao de cena, os tres `= 0;`, o `return;`) e caiam
        # na MESMA medida: o zeramento nao e ALCANCADO a cada troca de cena / nao acontece ANTES do
        # uso. Reconhecer a forma (a "variante D") nao bastava; executar, bastou.
        ("FIX-8 (1) o bloco de ZERAMENTO dentro de um `if (false)`",
         regras_bf.fonte_com_o_zeramento_em_if_falso, (MOTIVO_ZERAMENTO,)),
        ("FIX-8 (2) `_diagCena = cena` ANTES do guarda (guarda sempre verdadeiro)",
         regras_bf.fonte_com_a_cena_gravada_antes_do_guarda, (MOTIVO_ZERAMENTO,)),
        ("FIX-8 (3) o reset CHAMADO depois do uso do contador",
         regras_bf.fonte_com_o_reset_depois_do_uso, (MOTIVO_ZERAMENTO,)),
    ]
    for rotulo, plantar, motivos in plantados:
        com_defeito = plantar(src)
        arc.exigir(com_defeito != src,
                   "o plantio do defeito (%s) nao achou onde agir: as checagens nao estao lendo o "
                   "trecho certo do fonte" % rotulo)
        falhas_defeito = regras_bf.falhas_da_fonte(com_defeito)
        arc.exigir(falhas_defeito,
                   "as checagens PASSARAM num fonte com o defeito plantado (%s): a verificacao nao "
                   "vale nada" % rotulo)
        for motivo in motivos:
            arc.exigir(any(motivo in f for f in falhas_defeito),
                       "o defeito (%s) nao e pego pelo motivo esperado (%r): %s"
                       % (rotulo, motivo, " | ".join(falhas_defeito)))

    print("teto de rotina=%d, de efeito=%d, do escape=%d; medido: %d textos no universo com %d com "
          "efeito, e ate %d pulados numa varredura; pelo log VERSIONADO: maior varredura %d textos, "
          "%d candidatos ao escape (%d ja na serifa) e o maior pulo de uma cena e %d (fracao "
          "%.4f); a linha de combate saiu nas DUAS configs (default e a do dono) e NAO saiu nos tres "
          "modelos do defeito; o fonte reprova os %d defeitos plantados"
          % (teto_rotina, teto_efeito, teto_escape, universo, com_efeito, pulados_na_varredura,
             textos_na_varredura, candidatos, textos_na_varredura - candidatos, maior_pulo, fracao,
             len(plantados)))


if __name__ == "__main__":
    arc.main(META, corpo)
