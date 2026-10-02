#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A TRAVA DE COR DAS NOTAS FUNDIDAS (COR-2): ela confere TODAS, e REAGE a troca.

POR QUE ESTE TESTE EXISTE
-------------------------
A trava `tools/check_notas_redundantes.py` (familia 4) nasceu no COR-1 (01/10) para pegar
nota sem o tom do nivel 2. A REV-50 achou o furo: ela so olhava as notas fundidas em
`TextFixes` no formato de DUAS quebras (`\\n\\n<color=#...>`). Das 21 entradas com cor ela
conferia 11 e IGNORAVA 10 — e DUAS DAS 12 NOTAS DE SHRINE moravam nas ignoradas
(`Recover [0]% of max mana/health each turn`, formato de UMA quebra). Trocar a cor de uma
nota fundida passava em silencio.

Aqui ficam tres coisas, nesta ordem:

  1. a trava esta VERDE na fonte real E declara ter conferido TODAS as notas fundidas (o
     numero que ela imprime bate com a contagem independente deste teste, feita por regex
     sobre a tabela — nao pelo parser dela);
  2. as duas notas de SHRINE no formato de UMA quebra (o furo) fazem parte do conjunto que
     ela confere — o teste mede o formato, nao confia na promessa;
  3. a isca versionada REPROVA pelo motivo certo e a metade sem o defeito PASSA — o par que
     transforma "fechamos o furo" em prova executavel (o defeito e a expectativa antiga).
"""
import os

import arcabouco as arc
import recorte as rec
import regras_cor as reg

META = {
    "nome": "trava-cor-notas-fundidas",
    "categoria": "pura",
    "requer": [],
    "descricao": "a trava de cor confere TODAS as notas fundidas (inclusive as de UMA quebra) e REAGE a troca de cor — tambem com COMENTARIO DE BLOCO dentro da chave (FIX-4)",
}


def _conferidas(saida):
    """O numero que a trava imprime de notas fundidas conferidas."""
    import re

    m = re.search(r"(\d+) bloco\(s\) de nota fundida", saida)
    arc.exigir(m, "a trava nao declara quantos blocos de nota fundida conferiu (saida: %s)" % saida[-200:])
    return int(m.group(1))


def _corpo_sem_bloco(caminho):
    """Texto a partir do `def corpo`, sem as linhas do BLOCO-DO-DEFEITO (o defeito e o que muda)."""
    with open(caminho, encoding="utf-8") as fh:
        linhas = fh.read().splitlines()
    inicio = next((n for n, linha in enumerate(linhas) if linha.startswith("def corpo")), None)
    arc.exigir(inicio is not None, "%s nao tem `def corpo`" % caminho)
    dentro, guardadas = False, []
    for linha in linhas[inicio:]:
        if linha.strip().startswith("# >>> BLOCO-DO-DEFEITO"):
            dentro = True
            continue
        if linha.strip().startswith("# <<< BLOCO-DO-DEFEITO"):
            dentro = False
            continue
        if not dentro:
            guardadas.append(linha)
    return "\n".join(guardadas)


def _o_recorte_da_entrada_e_estrutural():
    """PROVA NOS DOIS SENTIDOS (FORMATO-3), em COPIA EM MEMORIA — o arquivo real nao e tocado.

    (1) um RETOQUE INOFENSIVO no VALOR da entrada (texto a mais antes do `Shrine Effect Bonus`,
        do tipo que escreve melhor a explicacao) NAO pode quebrar o recorte — a janela que
        existia (160 caracteres a partir da chave) QUEBRAVA com ele;
    (2) o DEFEITO REAL (a nota de shrine deixar de citar o `Shrine Effect Bonus`) TEM de
        continuar sendo pego: o bloco estrutural nao traz mais a frase.
    """
    fonte = reg.fonte_do_mod()
    chave = "Recover [0]% of maximum mana each turn."
    frase = "Base 10%; the value shown already includes the Shrine Effect Bonus."

    # (1) O RETOQUE: mais texto na explicacao, ANTES do `Shrine Effect Bonus`.
    retoque = ("Base 10%; o valor mostrado ja inclui, com uma explicacao bem mais longa do que a "
               "janela fixa antiga conseguia alcancar a partir da chave da tabela, o Shrine "
               "Effect Bonus.")
    retocado = fonte.replace(frase, retoque, 1)
    arc.exigir(retocado != fonte, "o retoque nao achou a nota de shrine — nao plantou nada")
    j = retocado.index("<color=#C8B090", retocado.index(chave))
    trecho = rec.bloco_que_contem(retocado, j)
    arc.exigir("Shrine Effect Bonus" in trecho,
               "o retoque INOFENSIVO quebrou o recorte (o `Shrine Effect Bonus` saiu da entrada)")
    # ...e a JANELA ANTIGA (a chave + 160) teria cortado: o que a prova demonstra. Exige que a
    # FRASE INTEIRA caia fora da janela (nao so o comeco dela) — a margem tem de ser folgada.
    i = retocado.index(chave)
    arc.exigir("Shrine Effect Bonus" not in retocado[i:j + 160],
               "a janela de 160 aguentou o retoque — a prova nao demonstra que o conserto era "
               "necessario (o retoque encurtou?)")

    # (2) O DEFEITO REAL: a nota deixa de citar o `Shrine Effect Bonus` — SO a entrada do mana
    #     (o par de shrine divide a frase; mutar o arquivo inteiro pegaria a outra entrada).
    i = fonte.index(chave)
    defeito = fonte[:i] + fonte[i:].replace("Shrine Effect Bonus", "Bonus de santuario", 1)
    arc.exigir(defeito != fonte and "Shrine Effect Bonus" not in defeito[i:i + 200],
               "o plantio do defeito nao achou o `Shrine Effect Bonus` na entrada do mana")
    jf = defeito.index("<color=#C8B090", defeito.index(chave))
    arc.exigir("Shrine Effect Bonus" not in rec.bloco_que_contem(defeito, jf),
               "o DEFEITO REAL (a nota sem o `Shrine Effect Bonus`) PASSOU — a checagem e decoracao")


def corpo():
    # ---------------------------------------------------------------- 1. VERDE + COBERTURA
    codigo, saida = reg.roda_a_trava_notas(reg.FONTE_MOD)
    arc.igual(codigo, 0,
              "a trava de cor das notas tem de estar VERDE na fonte real; saida: %s" % saida[-300:])

    notas = reg.notas_fundidas_com_cor()
    duas = [n for n in notas if n[0] == 2]
    uma = [n for n in notas if n[0] == 1]
    sem_quebra = [n for n in notas if n[0] == 0]
    do_marcador = [n for n in notas if n[1] == reg.entrada_marcador()]

    # A contagem e INDEPENDENTE do parser da trava (regex sobre o bloco da tabela).
    arc.exigir(len(uma) > 0,
               "nao existe nenhuma entrada de TextFixes com cor no formato de UMA quebra — "
               "o cenario do furo sumiu, e com ele a prova (notas: %d)" % len(notas))
    arc.igual(_conferidas(saida), len(do_marcador),
              "a trava tem de conferir TODAS as notas fundidas (as %d com o marcador; "
              "hoje ela diz que conferiu outras)" % len(do_marcador))
    arc.igual(len(uma) + len(duas) + len(sem_quebra), len(notas),
              "as tres formas de cor em TextFixes (sem quebra / uma / duas) tem de somar o total")
    arc.exigir(len(duas) > 0 and len(uma) > 0,
               "faltou um dos formatos: %d com duas quebras, %d com uma" % (len(duas), len(uma)))

    # ---------------------------------------------------------------- 2. AS NOTAS DE SHRINE
    # As DUAS notas de shrine do furo: chave de `Recover ... each turn.` com a nota no formato
    # de UMA quebra e o texto de Shrine Effect Bonus. Nao basta uma: o achado era um par.
    # A prova nos DOIS SENTIDOS do recorte (FORMATO-3) vem antes: o retoque inofensivo nao
    # quebra, e o defeito real continua sendo pego — em copia em memoria.
    _o_recorte_da_entrada_e_estrutural()
    fonte = reg.fonte_do_mod()
    for chave in ("Recover [0]% of maximum mana each turn.",
                  "Recover [0]% of maximum health each turn."):
        i = fonte.index(chave)
        j = fonte.index("<color=#C8B090", i)
        antes = fonte[j - 2:j]
        arc.igual(antes, reg.BS + "n",
                  "a nota de shrine '%s' tem de estar no formato de UMA quebra "
                  "(o furo do COR-1); antes da cor veio %r" % (chave, antes))
        # O recorte e a ENTRADA INTEIRA da tabela (o bloco `{ ... }` que casa), nunca uma janela
        # de caracteres. Guarda: ou o recorte comeca em `{` e traz a CHAVE e o VALOR, ou REPROVA.
        trecho = rec.bloco_que_contem(fonte, j)
        arc.exigir(trecho.lstrip().startswith("{") and chave in trecho and "</color>" in trecho,
                   "o recorte da nota de shrine '%s' NAO e a ENTRADA INTEIRA da tabela (do `{` ao "
                   "`}` que casa) — voltou a ser uma janela de caracteres?: %r"
                   % (chave, trecho[:90]))
        arc.exigir("Shrine Effect Bonus" in trecho,
                   "a nota de shrine '%s' deixou de citar o Shrine Effect Bonus" % chave)
        arc.exigir(any("Shrine Effect Bonus" in n[2] for n in uma),
                   "a nota de shrine '%s' nao entra no conjunto de UMA quebra medido" % chave)

    # ---------------------------------------------------------------- 3. ISCA x OK
    isca = os.path.join(arc.DIR_CONTRA_PROVA, "cp_cor_nota_fundida_isca.py")
    ok = os.path.join(arc.DIR_CONTRA_PROVA, "cp_cor_nota_fundida_ok.py")
    for caminho in (isca, ok):
        arc.exigir(os.path.isfile(caminho), "a isca da trava de cor sumiu: %s" % caminho)

    cod_isca, saida_isca = arc.executar_arquivo(isca)
    arc.igual(arc.ler_meta(isca).get("esperado"), "reprovar",
              "a isca tem de declarar `esperado: reprovar` no META")
    arc.igual(cod_isca, arc.EXIT_FALHOU,
              "a isca tinha de REPROVAR (exit 1); saida: %s"
              % (saida_isca.strip().splitlines() or ["<sem saida>"])[-1])
    arc.exigir("DEIXA PASSAR" in saida_isca,
               "a isca tinha de reprovar na EXPECTATIVA ANTIGA (a trava deixa passar), nao em "
               "outra coisa: %s" % (saida_isca.strip().splitlines() or ["<sem saida>"])[-1])
    arc.exigir(reg.HEX_PLANTADO in saida_isca,
               "a isca tem de citar a cor que plantou (%s): %s"
               % (reg.HEX_PLANTADO, saida_isca.strip().splitlines()[-1]))

    cod_ok, saida_ok = arc.executar_arquivo(ok)
    arc.igual(cod_ok, arc.EXIT_OK,
              "a metade sem o defeito tinha de PASSAR (exit 0); saida: %s"
              % (saida_ok.strip().splitlines() or ["<sem saida>"])[-1])
    arc.exigir("pegou a troca de cor" in saida_ok,
               "a metade ok tinha de provar que a trava PEGA a troca; saida: %s"
               % (saida_ok.strip().splitlines() or ["<sem saida>"])[-1])

    arc.igual(_corpo_sem_bloco(isca), _corpo_sem_bloco(ok),
              "a isca e a metade ok divergem fora do bloco do defeito - nao sao o mesmo teste")

    # ------------------------------------------------- 4. O FURO DO COMENTARIO DE BLOCO (FIX-4)
    # O COR-2 fez o parser pular o comentario de LINHA dentro do `{`; o comentario de BLOCO
    # (`/* ... */`) antes da chave continuava escondendo a entrada (25 -> 24 blocos de nota) e a
    # troca de cor nela NAO reprovava. O par abaixo prova o conserto: a isca reprova na
    # expectativa antiga ("DEIXA PASSAR") e a metade ok passa (a trava PEGA e cita a cor).
    isca_bloco = os.path.join(arc.DIR_CONTRA_PROVA, "cp_cor_comentario_bloco_isca.py")
    ok_bloco = os.path.join(arc.DIR_CONTRA_PROVA, "cp_cor_comentario_bloco_ok.py")
    for caminho in (isca_bloco, ok_bloco):
        arc.exigir(os.path.isfile(caminho),
                   "a contra-prova do comentario de bloco sumiu: %s" % caminho)

    cod_isb, saida_isb = arc.executar_arquivo(isca_bloco)
    arc.igual(arc.ler_meta(isca_bloco).get("esperado"), "reprovar",
              "a isca do comentario de bloco tem de declarar `esperado: reprovar` no META")
    arc.igual(cod_isb, arc.EXIT_FALHOU,
              "a isca do comentario de bloco tinha de REPROVAR (exit 1); saida: %s"
              % (saida_isb.strip().splitlines() or ["<sem saida>"])[-1])
    arc.exigir("DEIXA PASSAR" in saida_isb,
               "a isca do comentario de bloco tinha de reprovar na EXPECTATIVA ANTIGA (a trava "
               "deixava passar), nao em outra coisa: %s"
               % (saida_isb.strip().splitlines() or ["<sem saida>"])[-1])
    arc.exigir(reg.HEX_PLANTADO in saida_isb,
               "a isca do comentario de bloco tem de citar a cor que plantou (%s): %s"
               % (reg.HEX_PLANTADO, (saida_isb.strip().splitlines() or [""])[-1]))

    cod_okb, saida_okb = arc.executar_arquivo(ok_bloco)
    arc.igual(cod_okb, arc.EXIT_OK,
              "a metade ok do comentario de bloco tinha de PASSAR (exit 0); saida: %s"
              % (saida_okb.strip().splitlines() or ["<sem saida>"])[-1])
    arc.exigir("pegou a troca de cor" in saida_okb,
               "a metade ok do comentario de bloco tinha de provar que a trava PEGA a troca; "
               "saida: %s" % (saida_okb.strip().splitlines() or ["<sem saida>"])[-1])

    arc.igual(_corpo_sem_bloco(isca_bloco), _corpo_sem_bloco(ok_bloco),
              "a isca e a metade ok do comentario de bloco divergem fora do bloco do defeito")

    print("trava verde e conferindo %d notas fundidas (%d de uma quebra, %d de duas); "
          "isca REPROVOU e a metade ok PASSOU; e o par do COMENTARIO DE BLOCO (FIX-4) "
          "REPROVOU/PASSOU igual" % (len(do_marcador), len(uma), len(duas)))


if __name__ == "__main__":
    arc.main(META, corpo)
