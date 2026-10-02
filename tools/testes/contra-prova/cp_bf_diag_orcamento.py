#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do orcamento do diagnostico do BetterFont (BF-2R/BF-3): a ISCA.

O que este arquivo faz aqui: ele existe para o runner ter o que reprovar. A regra do plano
(`docs/PLANO-DE-TESTES.md`) e que todo teste seja MOSTRADO REPROVANDO - e a unica forma de mostrar
isso num teste que le o FONTE vivo e rodar as MESMAS checagens contra um fonte com o defeito
plantado.

Os DEFEITOS plantados aqui sao SETE, e as checagens tem de REPROVAR em CADA um, pelo SEU motivo
(um "reprova por qualquer coisa" nao vale):

  (a) `regras_bf.fonte_com_o_orcamento_da_bf2` - o orcamento da BF-2: contadores da SESSAO (sem o
      reset por cena) E classificacao da linha tirada do CONTEUDO (`!IsNullOrEmpty(copiados)`), que
      torna o teto de ROTINA inalcancavel porque num texto convertido `copiados` nunca vem vazio;
  (b) `regras_bf.fonte_com_o_escape_como_efeito` - o PULADO PELO ESCAPE contado como EFEITO (o
      estado da BF-2R): com `PularTextosEstilizados=true` (a config do dono) os ~484 pulados de uma
      varredura disputam o teto de 300 e a linha de combate fica de fora;
  (c) `regras_bf.fonte_com_o_reset_so_na_primeira_cena` - o PONTO CEGO da trava da BF-2R: o guarda
      do reset vira `if (_diagCena != null)`. O reset existe e os tokens do zero nao mudam - a
      checagem antiga (que conferia os tokens) passava com a suite inteira; o que muda e que o
      reset deixa de ser ALCANCAVEL a cada troca de cena;
  (d) `regras_bf.fonte_com_o_reset_inalcancavel` - `if (true) return;` no comeco do reset: nenhum
      token do zero e tocado, e o reset nunca roda.

E as TRES variantes da REV-56 (FIX-6, achado 1), que a checagem de TOKEN deixava passar com lista
VAZIA de falhas - todas com os tokens de pe:

  (e) `regras_bf.fonte_com_a_cena_fixa_no_comentario` - `SceneManager.GetActiveScene()` fica DENTRO
      DE UM COMENTARIO e `cena` passa a ler uma string FIXA: o reset so roda na PRIMEIRA cena (o
      substring `"GetActiveScene" in fonte` continuava satisfeito pelo comentario);
  (f) `regras_bf.fonte_com_o_escape_incrementando_o_efeito` - o ramo do escape volta a incrementar
      o contador de EFEITO: o pulo passa a gastar o orcamento que nao e dele;
  (g) `regras_bf.fonte_com_o_corte_do_escape_no_teto_de_efeito` - o guarda do escape ganha
      `|| _diagLinhasDeEfeito >= TetoDiagEfeito`: numa cena mista a linha de combate cai junto.

E a CLASSE que a FIX-8 fechou (achado 1 da FIX-7R) - todos com TODOS os tokens do zeramento de pe,
e antes passando com lista vazia:

  (h) `regras_bf.fonte_com_o_zeramento_em_if_falso` - os tres `= 0;` dentro de um `if (false)`;
  (i) `regras_bf.fonte_com_a_cena_gravada_antes_do_guarda` - `_diagCena = cena;` ANTES do guarda, que
      fica sempre verdadeiro: o corpo (com os tres zeros) nunca roda;
  (j) `regras_bf.fonte_com_o_reset_depois_do_uso` - a chamada do reset DESLOCADA para depois do uso
      do contador: o primeiro texto de cada cena e julgado contra o orcamento da cena anterior.

Este arquivo tem de sair REPROVOU (exit 1) - se ele PASSAR, quem esta quebrada e a checagem. Nao
consertar este arquivo: o "conserto" e o `t_bf_diag_orcamento.py`, ao lado.
"""
import regras_bf

import arcabouco as arc

META = {
    "nome": "contra-prova-bf-diag-orcamento",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca do BF-2R/BF-3/FIX-8: com o orcamento da BF-2, o escape contado como efeito, o reset inalcancavel/so na 1a cena e a CLASSE do zeramento (if false, cena antes do guarda, reset depois do uso) reinjetados, as checagens tem de REPROVAR",
}


def corpo():
    src = regras_bf.fonte()
    arc.exigir(len(src) > 5000, "o fonte do BetterFont veio vazio/curto")

    # Cada defeito tem de ser PEGO, e pelo SEU motivo.
    MOTIVO_ZERAMENTO = "ZERAMENTO NAO e ALCANCADO"
    plantados = [
        ("o orcamento da BF-2 (sessao + classificacao pelo conteudo)",
         regras_bf.fonte_com_o_orcamento_da_bf2, ("SESSAO", "CONTEUDO")),
        ("o pulado pelo escape contado como EFEITO",
         regras_bf.fonte_com_o_escape_como_efeito, ("nao como `TipoLinhaDiag.Escape`",)),
        ("o reset so na PRIMEIRA cena (`if (_diagCena != null)`)",
         regras_bf.fonte_com_o_reset_so_na_primeira_cena, (MOTIVO_ZERAMENTO,)),
        ("o reset INALCANCAVEL (`if (true) return`)",
         regras_bf.fonte_com_o_reset_inalcancavel, (MOTIVO_ZERAMENTO,)),
        # FIX-6 (achado 1 da REV-56) - as TRES variantes que a checagem de TOKEN deixava passar.
        ("(A) a cena lida vira COMENTARIO e `cena` fica FIXA (reset so na 1a cena)",
         regras_bf.fonte_com_a_cena_fixa_no_comentario, (MOTIVO_ZERAMENTO,)),
        ("(B) o ramo do escape volta a incrementar o contador de EFEITO",
         regras_bf.fonte_com_o_escape_incrementando_o_efeito, ("o contador do tipo `Escape` NAO corta",)),
        ("(C) o corte do escape passa a depender TAMBEM do TETO DE EFEITO",
         regras_bf.fonte_com_o_corte_do_escape_no_teto_de_efeito, ("cena MISTA",)),
        # FIX-8 (achado 1 da FIX-7R) - a CLASSE, com todos os tokens de pe.
        ("FIX-8 (1) o bloco de ZERAMENTO dentro de um `if (false)`",
         regras_bf.fonte_com_o_zeramento_em_if_falso, (MOTIVO_ZERAMENTO,)),
        ("FIX-8 (2) `_diagCena = cena` ANTES do guarda (guarda sempre verdadeiro)",
         regras_bf.fonte_com_a_cena_gravada_antes_do_guarda, (MOTIVO_ZERAMENTO,)),
        ("FIX-8 (3) o reset CHAMADO depois do uso do contador",
         regras_bf.fonte_com_o_reset_depois_do_uso, (MOTIVO_ZERAMENTO,)),
    ]

    resumo = []
    for rotulo, plantar, motivos in plantados:
        com_defeito = plantar(src)
        if com_defeito == src:
            raise arc.Falhou("o plantio do defeito (%s) nao encontrou onde agir: as checagens nao "
                             "estao lendo o trecho certo do fonte" % rotulo)

        falhas = regras_bf.falhas_da_fonte(com_defeito)
        if not falhas:
            raise arc.Falhou("as checagens PASSARAM num fonte com o defeito plantado (%s): a "
                             "verificacao do conserto nao vale nada" % rotulo)
        for motivo in motivos:
            if not any(motivo in f for f in falhas):
                raise arc.Falhou("o defeito (%s) nao e pego pelo motivo esperado (%r): %s"
                                 % (rotulo, motivo, " | ".join(falhas)))
        resumo.append("%s: %d checagem(ns)" % (rotulo, len(falhas)))

    # Chegou aqui: TODOS os defeitos foram pegos. Esta isca reprova de proposito, dizendo o motivo.
    raise arc.Falhou("isca: os dez defeitos do orcamento foram pegos pelas checagens (esperado) - "
                     + " | ".join(resumo))


if __name__ == "__main__":
    arc.main(META, corpo)
