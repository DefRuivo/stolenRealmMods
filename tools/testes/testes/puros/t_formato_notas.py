#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O FORMATO DAS NOTAS (RV-17 + BANCADA-1): a linha em branco EXATA e a ORDEM dos blocos, travados.

POR QUE ESTE TESTE EXISTE
-------------------------
Hoje a posicao dos blocos do tooltip foi mexida duas vezes. O COR-2 fez a cor do nivel 2 chegar de
verdade e, ao fazer isso, a regra que reordena o tooltip passou a acertar o bloco de VALOR do motor
em vez da nossa nota (o dono viu o dano ir para o fundo). O COR-3 consertou (a nota passou a ser
achada pelo CONTEUDO que o mod escreveu) — e deixou dois furos, achados pela COR-3R, exatamente no
FORMATO que este teste trava:

  * (1) TOOLTIPS COM DUAS NOTAS. O `TirarNotaDoMod` movia SO A PRIMEIRA; a SEGUNDA ficava onde
    estava, ANTES do `AP Cost`, e a ordem de leitura invertia. Ha DOIS casos reais, os dois com os
    blocos FUNDIDOS no MESMO valor do `TextFixes`: `Shapeshift Dragonkin` (que tem `[0]`, um dos
    atingidos pelo defeito do valor no fundo) e o buff `Miniature`. O comentario do C# afirmava que
    "o mod anexa uma por tooltip, jamais duas" — era FALSO, e o teste exige que o comentario diga a
    verdade.
  * (2) A LINHA EM BRANCO ORFA. Ao tirar a nota do meio do corpo, consumia-se UMA quebra; a outra
    ficava para tras e o tooltip saia com uma linha em branco entre a descricao e o `AP Cost`.

O ACHADO DO BANCADA-1 (01/10) — O QUE A BANCADA NAO REPRODUZIA
--------------------------------------------------------------
A bancada montava os custos como `texto.rstrip("\\n") + "\\n" + custo` — UMA quebra. O
`ShowSkillTooltip` escreve DUAS: a l.1470 acrescenta uma quebra ao original (`original += "\\n"`) e a
l.1536 concatena `original + "\\n" + "AP Cost: ..."`. Ou seja: na tooltip do jogo existe UMA LINHA EM
BRANCO antes do `AP Cost` — e ela e do JOGO, nao do mod (existe na vanilla).

A consequencia era o teste provar menos do que dizia:

  * a bancada NAO reproduzia o jogo (faltava a linha em branco do jogo no texto montado); e
  * o PROPRIO CHECADOR reprovava o texto do runtime, acusando "linha em branco orfa" — a regra que
    o RV-17 travou ("nao existe linha em branco em outro lugar") estava ERRADA.

O que estava CERTO era o codigo do mod: consumir o separador INTEIRO (as duas quebras) e justamente
o que PRESERVA a linha em branco do jogo (consumindo uma so, o tooltip saia com DUAS seguidas).
Este teste agora exige a igualdade entre o que a bancada monta e o que o jogo produz, com a leitura
do decompilado numa fixture versionada (`fixtures/formato-notas.entrada.json`) e o caso que SEPARA
os dois mundos — a contra-prova `cp_formato_quebra_do_jogo_isca.py` x `..._ok.py`.

O QUE ESTE TESTE PRENDE
-----------------------
  1. ESTRUTURA, no fonte: o `AnexarNota` escreve EXATAMENTE uma linha em branco; o prefixo recolhe
     TODAS as notas (em laco) e as devolve no fim, na ordem, com a linha azul por ultimo; e a
     extracao consome o separador INTEIRO (`InicioDoSeparador`).
  2. COMPORTAMENTO, no material REAL das tabelas, em QUATRO familias (skill com dano, shrine com a
     linha azul do nivel 3, invocacao com o valor fundido e os DOIS casos de DUAS notas): 0 defeito
     de linha em branco, 0 de ordem e 0 da quebra do jogo. O formato e UM — o que muda e quantos
     blocos o tooltip tem.
  3. O DEFEITO REPRODUZIDO: com a regra de ANTES, os MESMOS casos quebram (o par versionado em
     `contra-prova/cp_formato_notas_isca.py` x `..._ok.py` prova as duas metades).
  4. O CHECADOR NAO E VAZIO: defeitos plantados (duas linhas em branco, linha em branco no fim,
     linha orfa, a quebra do JOGO faltando) tem de ser VISTOS — um checador que nunca reprova nao
     trava nada.
  5. A ORDEM DAS HABILIDADES nas notas de INVOCACAO: o ataque basico primeiro, conferido contra o
     dump `docs/cobertura/invocacoes.csv` (conjunto de habilidades E ordem).
  6. O ESPELHO DO NIVEL 3: `regras_cor._registra_blocos` tem de EXCLUIR o bloco que abre com o
     marcador do nivel 3, como o `EhBlocoDoNivel3` do C# — o espelho registrava um bloco que o
     codigo NAO registra.
  7. A QUEBRA DO JOGO (BANCADA-1): a leitura do decompilado (fixture) conferida contra o proprio
     decompilado quando ele existe aqui; a bancada tem de escrever o MESMO numero de quebras que o
     jogo; o caminho do GROUND EFFECT (a tooltip de SHRINE) nao pode ter `AP Cost`.
  8. A BORDA DO BANCADA-2: o checador libera SO a PRIMEIRA linha de custo de cada caminho (o `AP
     Cost` da skill, o `Duration Type` do status); a linha em branco antes de uma linha SEGUINTE
     (`Range`) — uma forma que o jogo NUNCA escreve — tem de ser REPROVADA; e a `custo_no_texto` (a
     lista escrita a mao que alimenta o checador) passa por um controle que reprova entrada que nao
     aparece no `trecho` da leitura. A contra-prova `cp_formato_linha_antes_do_range_*` prova as
     duas metades.
"""
import copy
import os
import re

import arcabouco as arc
import recorte as rec
import regras_cor as reg
import regras_formato as fmt

META = {
    "nome": "formato-notas",
    "categoria": "pura",
    "requer": [],
    "descricao": "RV-17 + BANCADA-1/2: a linha em branco EXATA e a ORDEM dos blocos (1 e 2 notas, nivel 3 por ultimo, ataque basico primeiro nas invocacoes) - a bancada reproduz o texto do jogo (as 2 quebras da l.1470+1536 antes do AP Cost) e o checador libera SO a PRIMEIRA linha de custo de cada caminho (a linha em branco antes do Range reprova)",
}

# Quantas linhas de criatura as notas de invocacao tem de entregar ao parser (o parser nao pode
# passar vazio: sem um minimo, uma nota reescrita sumiria da conta em silencio).
MINIMO_DE_CRIATURAS = 20

# As quatro criaturas cuja ORDEM o mod DIVERGE da ordem do asset (o ataque basico primeiro): a
# prova de que a regra foi APLICADA, e nao que as notas ja nasceram na ordem certa.
REORDENADAS = ["Moose", "Panther", "Stag", "Timber Wolf"]


def _codigo():
    """O fonte SEM os comentarios (citacao nao e codigo)."""
    return re.sub(r"//[^\n]*", "", reg.fonte_do_mod())


# A assinatura do metodo que o recorte estrutural le (o nome mudar REPROVA, nunca passa vazio).
ASSINATURA_DO_PREFIXO = "private static void Prefix(ref string description)"

# O guarda do METODO INTEIRO: o ultimo statement e o `catch` do fim. Uma janela corta antes.
MARCAS_DO_PREFIXO = ("description = corpo;", "catch (Exception e)")


def _corpo_do_metodo(codigo, assinatura):
    """O CORPO INTEIRO do metodo, por CASAMENTO DE CHAVES — nunca por janela de caracteres.

    FORMATO-3: a funcao deixou de ser LOCAL a este teste. Ela (e o `_fim_do_literal`) virou
    `recorte.corpo_do_metodo` — o MESMO recorte estrutural, num lugar so, usado tambem pelo
    `t_nivel3_sinergia` e pelos modulos de regra. Duplicar a funcao em cada ponto de chamada
    foi exatamente o que fez a janela de caracteres voltar disfarcada de conserto: aqui so
    ficou a delegacao.

    POR QUE ESTRUTURAL (FORMATO-2, achado da NIV3-1R)
    --------------------------------------------------
    A versao anterior recortava uma JANELA FIXA (3200 caracteres a partir da assinatura do
    `Prefix`) e contava ali dentro os usos de `corpo += "\\n\\n"` (exigia exatamente 2). Isso mede
    TEXTO, nao comportamento: a linha da aura vive a 3041 caracteres da assinatura num metodo de
    3371 — ou seja, SOBRAM 159 de margem, e o metodo ja nao cabia inteiro na janela (ela cortava
    os ~171 caracteres finais, catch inclusive). Uma edicao INOFENSIVA no Prefix (um log a mais,
    um local a mais) do tipo que o NIV3-1 ja fez (~260 caracteres) empurraria a linha para fora
    da janela, e o teste reprovaria por motivo ALHEIO ao defeito — e o caminho curto para o verde
    seria AFROUXAR a janela, o pior desfecho possivel neste projeto.

    Aqui o recorte e o METODO, delimitado pela ASSINATURA e pelo `}` que casa com o `{` de
    abertura: nao ha margem, porque nao ha distancia. Chaves dentro de literal de string/char nao
    contam. Sem a assinatura, sem o `{`, ou com chaves que nao fecham -> FALHA ALTO (nunca devolve
    um pedaco).
    """
    return rec.corpo_do_metodo(codigo, assinatura)


def _prova_do_recorte_estrutural():
    """PROVA NOS DOIS SENTIDOS (FORMATO-3), em COPIA EM MEMORIA — o arquivo real nao e tocado.

    (1) um RETOQUE INOFENSIVO no Prefix (codigo a mais, sem tocar marcador) NAO pode quebrar o
        recorte — com a janela de 3200 ele QUEBRAVA (a prova o demonstra);
    (2) o DEFEITO REAL (um dos separadores `corpo += "\\n\\n"` some da remontagem) TEM de
        continuar sendo pego — a contagem que este teste faz reprova.
    """
    codigo = _codigo()

    # (1) O RETOQUE: um local a mais logo depois da abertura do `Prefix`.
    retoque = ("\n            string rastroDoRecorte = \"retoque inofensivo do FORMATO-3\";"
               "\n            int tamanhoDoRastro = rastroDoRecorte.Length;")
    retocado = codigo.replace(ASSINATURA_DO_PREFIXO + "\n            {",
                              ASSINATURA_DO_PREFIXO + "\n            {" + retoque, 1)
    arc.exigir(retocado != codigo, "o retoque nao achou a abertura do `Prefix` — nao plantou nada")
    bloco = _corpo_do_metodo(retocado, ASSINATURA_DO_PREFIXO)
    arc.exigir(bloco.rstrip().endswith("}") and "description = corpo;" in bloco,
               "o retoque INOFENSIVO quebrou o recorte do `Prefix` (nao e mais o metodo inteiro)")
    arc.igual(len(re.findall(r'corpo \+= "\\n\\n"', bloco)), 2,
              "o retoque INOFENSIVO mudou a contagem dos separadores conferidos")
    # ...e a janela de 3200 (a que existia) teria cortado o fim do metodo com esse retoque.
    i_assin = retocado.find(ASSINATURA_DO_PREFIXO)
    na_janela = retocado[i_assin:i_assin + 3200]
    arc.exigir(not (na_janela.rstrip().endswith("}") and "description = corpo;" in na_janela),
               "a janela de 3200 aguentou o retoque — a prova nao demonstra que o conserto era "
               "necessario (o metodo encolheu?)")

    # (2) O DEFEITO REAL: um dos dois separadores conferidos some. A contagem TEM de reprovar.
    defeito = codigo.replace('corpo += "\\n\\n" + aura;', "corpo += aura;", 1)
    arc.exigir(defeito != codigo, "o plantio do defeito nao achou a cauda da aura")
    bloco_defeito = _corpo_do_metodo(defeito, ASSINATURA_DO_PREFIXO)
    arc.exigir(len(re.findall(r'corpo \+= "\\n\\n"', bloco_defeito)) != 2,
               "o DEFEITO REAL (a linha da aura sem o separador exato) PASSOU pela contagem — a "
               "checagem do recorte e decoracao")


def _fim_do_literal(codigo, i):
    """Compatibilidade: o (des)tratamento de literal de string/char vive no `recorte.py`."""
    return rec.fim_do_literal(codigo, i)


def _checador_nao_e_vazio():
    """Defeitos plantados tem de ser VISTOS — o checador de formato nao pode ser decoracao."""
    bom = "D" + fmt.NL * 2 + "<color=#CBB396>NOTA</color>"
    arc.igual(fmt.defeitos_de_linha_em_branco(bom), [],
              "um texto no formato CERTO nao pode ser acusado: %r" % bom)
    # BANCADA-1: a linha em branco ANTES do bloco de custos do jogo NAO e defeito — e o jogo que a
    # escreve (l.1470 + l.1536). O texto do RUNTIME nao pode ser acusado por ela.
    do_jogo = "D" + fmt.NL * 2 + fmt.CUSTOS[0] + fmt.NL + fmt.CUSTOS[1]
    arc.igual(fmt.defeitos_de_linha_em_branco(do_jogo), [],
              "a linha em branco que o JOGO escreve antes do `AP Cost` nao pode ser acusada de "
              "orfa: %r" % do_jogo)
    # BANCADA-2: a linha em branco antes de uma linha de custo SEGUINTE (`Range`, `Blast Radius`,
    # `Mana Cost`, `Cooldown`) e uma forma que o JOGO NUNCA escreve — ele so precede a PRIMEIRA linha
    # de custo de cada caminho (o `AP Cost`). O checador do BANCADA-1 (o bloco INTEIRO liberado)
    # deixava essa forma passar em silencio; hoje tem de VE-LA.
    antes_do_range = "D" + fmt.NL * 2 + fmt.CUSTOS[0] + fmt.NL * 2 + fmt.CUSTOS[1]
    arc.exigir(fmt.defeitos_de_linha_em_branco(antes_do_range),
               "o checador NAO viu a linha em branco antes do `Range` (BANCADA-2): o jogo so escreve "
               "a linha em branco antes da PRIMEIRA linha de custo, nunca antes das seguintes: %r"
               % antes_do_range)
    for seguinte in ("Range: Melee", "Blast Radius: 2", "Mana Cost: 3", "Cooldown: 2"):
        texto_seguinte = ("D" + fmt.NL * 2 + fmt.CUSTOS[0] + fmt.NL + fmt.CUSTOS[1]
                          + fmt.NL * 2 + seguinte)
        arc.exigir(fmt.defeitos_de_linha_em_branco(texto_seguinte),
                   "o checador NAO viu a linha em branco antes de %r — forma que o JOGO nunca "
                   "escreve (BANCADA-2): %r" % (seguinte, texto_seguinte))
    plantados = {
        "linha em branco no fim do tooltip": bom + fmt.NL + fmt.NL,
        "duas linhas em branco seguidas": "D" + fmt.NL * 3 + "<color=#CBB396>NOTA</color>",
        "linha em branco orfa (sem bloco e sem linha do jogo depois)":
            "D" + fmt.NL * 2 + "um texto que nao e bloco nem custo",
        "a quebra do JOGO faltando antes do `AP Cost`": "D" + fmt.NL + fmt.CUSTOS[0],
    }
    for nome, texto in plantados.items():
        vistos = (fmt.defeitos_de_linha_em_branco(texto)
                  + fmt.defeitos_da_quebra_do_jogo(texto, fmt.CUSTOS))
        arc.exigir(vistos,
                   "o checador de formato NAO viu o defeito plantado '%s': %r" % (nome, texto))

    # ...e a ORDEM tambem: duas notas trocadas tem de ser acusadas.
    trocado = ("D" + fmt.NL * 2 + "<color=#CBB396>NOTA B</color>"
               + fmt.NL * 2 + "<color=#CBB396>NOTA A</color>")
    arc.exigir(fmt.defeitos_da_ordem(trocado, ["NOTA A", "NOTA B"]),
               "o checador de ORDEM nao viu as duas notas trocadas: %r" % trocado)
    arc.igual(fmt.defeitos_da_ordem("D" + fmt.NL * 2 + "<color=#CBB396>NOTA A</color>"
                                    + fmt.NL * 2 + "<color=#CBB396>NOTA B</color>",
                                    ["NOTA A", "NOTA B"]), [],
              "duas notas na ordem certa nao podem ser acusadas")


def _leituras_plantadas():
    """Cópias MUTADAS da leitura do formato, com o motivo que o controle tem de citar ao reprovar.

    (a) `quebras` trocado na l.1536 (2 no lugar de 1: aquele ramo tem UM escape) — a checagem INTERNA
        do controle pega, sempre (o número tem de sair da contagem dos escapes do ramo);
    (b) a LINHA declarada deslocada — a checagem EXTERNA pega, quando o decompilado está nesta
        máquina. Sem ele o controle não tem contra o que conferir, e o motivo (b) fica só declarado.
    """
    base = reg.leitura_do_formato()
    trocado = copy.deepcopy(base)
    trocado["caminhos"]["skill"]["linhas"][1]["quebras"] = 2
    deslocado = copy.deepcopy(base)
    deslocado["caminhos"]["skill"]["linhas"][1]["linha"] += 5000
    return (("o numero de quebras trocado", trocado, "tem de ser a contagem dos escapes"),
            ("o trecho deslocado", deslocado, "NAO bate com o decompilado"))


def corpo():
    codigo = _codigo()

    # ------------------------------------------------------- 1. ESTRUTURA NO FONTE
    # (a) A linha em branco EXATA, no helper por onde passa toda nota anexada.
    arc.exigir(re.search(r'return texto\.TrimEnd\(\) \+ "\\n\\n" \+ nota\.TrimStart\(new char\[\]'
                         r"\s*\{\s*'\\n'\s*\}\);", codigo),
               "o `AnexarNota` tem de juntar a nota com EXATAMENTE uma linha em branco "
               "(`TrimEnd` + `\\n\\n` + `TrimStart('\\n')` da nota) — ver docs/TEXTO-TOOLTIPS.md §9")

    # (b) TODAS as notas, em laco, achadas pelo CONTEUDO (o gancho do COR-3 continua de pe).
    #     O recorte e ESTRUTURAL (o METODO por casamento de chaves), nao uma janela de caracteres:
    #     uma janela mede DISTANCIA e reprova por reformatacao; o metodo acompanha o codigo.
    #     A prova nos DOIS SENTIDOS (FORMATO-3) vem antes: o retoque inofensivo nao quebra, e o
    #     defeito real continua sendo pego — em copia em memoria, sem tocar o arquivo.
    _prova_do_recorte_estrutural()
    bloco_prefixo = _corpo_do_metodo(codigo, ASSINATURA_DO_PREFIXO)
    # ...e o recorte tem de ser o METODO INTEIRO: chega ao ULTIMO statement (`description = corpo;`)
    # e FECHA as chaves. Uma janela (a de 3200) cortava ANTES do `}` final; aqui nao ha o que cortar.
    # Este e o guarda que impede a volta da janela: ou o bloco e o metodo, ou o teste FALHA ALTO.
    rec.exigir_metodo_inteiro(bloco_prefixo, ASSINATURA_DO_PREFIXO, MARCAS_DO_PREFIXO)
    arc.exigir(re.search(r"string nota;\s*bool achouNota = TirarNotaDoMod\(ref description, "
                         r"out nota\);\s*while \(achouNota\)", bloco_prefixo),
               "o `CorEOrdemDoTooltip` tem de recolher as notas em LACO (uma tooltip pode ter DUAS) "
               "— parar na primeira era o defeito do `Shapeshift Dragonkin` e do `Miniature`")
    arc.exigir(re.search(r"List<string> notas = new List<string>\(\);", bloco_prefixo),
               "o prefixo tem de juntar as notas numa lista, na ORDEM em que aparecem")
    arc.igual(len(re.findall(r'corpo \+= "\\n\\n"', bloco_prefixo)), 2,
              "a remontagem tem de usar o MESMO separador (`\\n\\n`, uma linha em branco) para as "
              "notas e para a linha azul — e so uma vez cada (o das notas e o da aura)")

    # (c) A ordem dos blocos: nota(s) primeiro, a linha azul (nivel 3) por ULTIMO.
    arc.exigir(re.search(r"foreach \(string blocoNota in notas\)\s*\{\s*corpo \+= \"\\n\\n\" "
                         r"\+ blocoNota;", bloco_prefixo),
               "as notas tem de ser devolvidas em laco, na ordem")
    i_notas = bloco_prefixo.find("foreach (string blocoNota in notas)")
    i_aura = bloco_prefixo.find('corpo += "\\n\\n" + aura;')
    arc.exigir(i_notas >= 0 and i_aura > i_notas,
               "a linha azul do nivel 3 tem de ser a ULTIMA coisa recolocada (depois das notas)")

    # (d) O SEPARADOR INTEIRO: a linha em branco orfa nao pode voltar.
    arc.igual(codigo.count("InicioDoSeparador(corpo,"), 2,
              "as DUAS extracoes (o bloco da aura e a nota) tem de consumir o separador pelo "
              "`InicioDoSeparador` — sem ele a linha em branco ficava orfa entre a descricao e o "
              "`AP Cost`")
    trecho = _corpo_do_metodo(codigo, "private static int InicioDoSeparador(string corpo, int posicao)")
    arc.igual(trecho.count("ini--;"), 2,
              "o `InicioDoSeparador` tem de consumir as DUAS quebras do separador (a linha em "
              "branco que o `AnexarNota` escreveu), nunca uma")

    # (e) O comentario do `TirarNotaDoMod` nao pode voltar a afirmar que o mod anexa uma nota so:
    #     ele tem de declarar os DOIS casos reais com duas notas.
    fonte = reg.fonte_do_mod()
    fim_do_doc = fonte.find("private static bool TirarNotaDoMod")
    arc.exigir(fim_do_doc > 0, "nao achei o `TirarNotaDoMod` no fonte")
    doc = fonte[fonte.rfind("/// <summary>", 0, fim_do_doc):fim_do_doc]
    # O comentario e quebrado em linhas com `///`: junta tudo para procurar a FRASE, nao o pedaco.
    doc_texto = " ".join(doc.replace("///", " ").split())
    arc.exigir("Shapeshift Dragonkin" in doc_texto and "Miniature" in doc_texto,
               "o comentario do `TirarNotaDoMod` tem de declarar os DOIS casos reais com DUAS notas "
               "(`Shapeshift Dragonkin` e `Miniature`) — o texto antigo afirmava que o mod anexa uma so")
    arc.exigir("jamais duas" not in doc_texto,
               "o comentario do `TirarNotaDoMod` voltou a afirmar que o mod anexa UMA nota por "
               "tooltip — e FALSO: `Shapeshift Dragonkin` e `Miniature` tem DUAS")

    # ------------------------------------------------------- 2. O COMPORTAMENTO
    _checador_nao_e_vazio()

    casos = fmt.casos()
    familias = {c["rotulo"].split(" (")[0] for c in casos}
    arc.exigir(len(casos) >= 5 and len(familias) >= 4,
               "esperava pelo menos 5 casos de 4 familias de formato; achei %d de %d"
               % (len(casos), len(familias)))

    for caso in casos:
        depois = fmt.aplica_com_a_regra(caso, "rv17")
        defeitos = (fmt.defeitos_de_linha_em_branco(depois)
                    + fmt.defeitos_da_ordem(depois, caso["notas"], caso["aura"], caso["custos"])
                    + fmt.defeitos_da_quebra_do_jogo(depois, caso["custos"]))
        arc.igual(defeitos, [],
                  "formato QUEBRADO em '%s': %s | texto: %r"
                  % (caso["rotulo"], defeitos, depois[-220:]))

    # Os DOIS casos de DUAS notas tem de existir, com DOIS blocos cada.
    dois = fmt.casos_duas_notas()
    arc.igual(len(dois), 2,
              "os DOIS casos reais com DUAS notas (Shapeshift Dragonkin e Miniature) tem de estar "
              "no material; achei %d" % len(dois))
    for caso in dois:
        arc.igual(len(caso["notas"]), 2,
                  "'%s' tem de carregar DUAS notas do nivel 2" % caso["rotulo"])

    # ------------------------------------------------------- 3. O DEFEITO REPRODUZIDO
    quebrados_antigos = fmt.casos_quebrados("antiga")
    arc.exigir(len(quebrados_antigos) >= 4,
               "a regra de ANTES do RV-17 tinha de quebrar os casos de formato (o defeito tem de "
               "aparecer); ela quebrou %d" % len(quebrados_antigos))
    for rotulo, defeitos in quebrados_antigos:
        arc.exigir(any("ORFA" in d or "DUAS linhas" in d or "ordem" in d for d in defeitos),
                   "o defeito antigo de '%s' saiu por um motivo que nao e de formato: %s"
                   % (rotulo, defeitos))

    # ------------------------------------------------------- 4. A ORDEM DAS HABILIDADES
    defeitos_hab = fmt.defeitos_da_ordem_das_habilidades()
    arc.igual(defeitos_hab, [],
              "a ORDEM DAS HABILIDADES nas notas de invocacao esta errada: %s" % defeitos_hab)
    linhas = sum(len(itens) for _nota, itens in fmt.criaturas_das_notas())
    arc.exigir(linhas >= MINIMO_DE_CRIATURAS,
               "o parser das notas de invocacao entregou so %d linha(s) de criatura (minimo %d): "
               "nota reescrita some da conta em silencio" % (linhas, MINIMO_DE_CRIATURAS))
    arc.igual(fmt.reordenadas_pelo_mod(), REORDENADAS,
              "as criaturas em que a NOTA diverge da ordem do ASSET (o ataque basico primeiro)")

    # ------------------------------------------------------- 5. O ESPELHO DO NIVEL 3
    registro = set()
    reg._registra_blocos("<color=#C8B090>Your active shrine auras: Dodge +40% (total +57%).</color>",
                         registro)
    arc.igual(registro, set(),
              "o espelho do `RegistrarBlocosDeNota` tem de EXCLUIR o bloco que abre com o marcador "
              "do NIVEL 3 (`EhBlocoDoNivel3`): o codigo NAO o registra como nota")
    registro2 = set()
    reg._registra_blocos("<color=#C8B090>Base 20%; the value shown already includes the Shrine "
                         "Effect Bonus.</color>", registro2)
    arc.igual(len(registro2), 1,
              "a nota do nivel 2 continua a ser registrada pelo conteudo: %r" % registro2)

    # ------------------------------------------------------- 6. A QUEBRA DO JOGO (BANCADA-1)
    # (a) A LEITURA, conferida: os trechos do decompilado tem de estar LITERALMENTE nos arquivos do
    #     tipo (quando existem nesta maquina) e o numero de quebras tem de sair da contagem do ramo.
    conferidas, fontes = fmt.controle_da_leitura_do_formato()
    # A conferencia EXTERNA so roda quando ha decompilado NESTA maquina: `scratch/rv22/tooltip.cs`
    # e gitignored e o "cache do decompilado integral" e de uma instalacao — nenhum dos dois esta
    # num clone. Sem fonte, `conferidas` e 0 DE PROPOSITO (e o que o proprio
    # `fmt.controle_da_leitura_do_formato` documenta: "numa maquina sem ele o controle externo nao
    # roda; o interno, que roda sempre, e quem segura a leitura na linha"). Exigir `>= 8` SEMPRE
    # derrubava o CLONE e o CI — exatamente o defeito que o GIT-3 fecha (a suite tem de rodar no
    # clone). Com o decompilado presente, a exigencia continua valendo igual.
    if fontes:
        arc.exigir(conferidas >= 8,
                   "o controle da leitura do formato conferiu poucas linhas (%d): a leitura nao "
                   "esta presa ao decompilado" % conferidas)
    do_jogo = reg.quebras_antes_do_custo_do_jogo()
    arc.igual(reg.QUEBRAS_ANTES_DO_CUSTO_DA_BANCADA, do_jogo,
              "a BANCADA tem de escrever o MESMO numero de quebras antes do 1o custo que o "
              "`ShowSkillTooltip` (l.1470 + l.1536): o jogo escreve %d, a bancada declara %d"
              % (do_jogo, reg.QUEBRAS_ANTES_DO_CUSTO_DA_BANCADA))
    arc.exigir(do_jogo >= 2,
               "a leitura do formato perdeu a linha em branco do jogo antes do `AP Cost`: %d quebra(s)"
               % do_jogo)
    # (b) A IGUALDADE: o texto da bancada TEM de ser o texto do jogo, no caso que separa os dois.
    arc.igual(fmt.texto_da_bancada(), fmt.texto_do_runtime(),
              "a BANCADA nao reproduz o JOGO no caso '%s' (a linha em branco antes do `AP Cost`)"
              % fmt.ROTULO_QUE_SEPARA)
    arc.exigir((fmt.NL * 2 + fmt.CUSTOS[0]) in fmt.texto_do_runtime(),
               "o texto do runtime tem de trazer a linha em branco do jogo antes do `AP Cost`: %r"
               % fmt.texto_do_runtime())
    # (c) O OUTRO CAMINHO: a tooltip de SHRINE e a do GROUND EFFECT — sem `AP Cost` e sem `Range`.
    arc.exigir(not reg.tem_ap_cost_no_texto(),
               "a leitura do formato diz que o GROUND EFFECT tem bloco de custo")
    for caso in casos:
        depois = fmt.aplica_com_a_regra(caso, "rv17")
        if caso.get("caminho") != "ground_effect":
            continue
        for custo in ("AP Cost", "Range:", "Mana Cost", "Cooldown"):
            arc.exigir(custo not in depois,
                       "o caso de SHRINE (ground effect) saiu com %r — a moldura do "
                       "`ShowGroundEffectTooltip` nao tem custo nenhum" % custo)
        for marca in ("<size=", "Turns Remaining:", "Friendly"):
            arc.exigir(marca in caso["texto"],
                       "o caso de SHRINE (ground effect) perdeu a marca %r da moldura do jogo"
                       % marca)
    # (d) O CONTROLE NAO E DECORACAO: uma leitura PLANTADA tem de ser REPROVADA.
    for rotulo, leitura_pl, motivo in _leituras_plantadas():
        try:
            fmt.controle_da_leitura_do_formato(leitura_pl)
        except arc.Falhou as erro:
            arc.exigir(motivo in str(erro),
                       "o controle reprovou a leitura plantada '%s' pelo motivo ERRADO: %s"
                       % (rotulo, erro))
        else:
            arc.exigir("deslocado" in rotulo and not fontes,
                       "o controle ACEITOU a leitura plantada '%s' — a checagem nao dispara" % rotulo)

    # (e) A LISTA `custo_no_texto` NAO E DIGITADA A MAO SEM CONTROLE (BANCADA-2). Ela alimenta o
    #     checador; sem controle envelheceria em silencio (uma linha que o jogo NAO escreve passaria
    #     a ser aceita). O controle confere que CADA entrada aparece no `trecho` de alguma linha da
    #     leitura — e o teste PLANTIA uma entrada falsa, que o controle tem de REPROVAR.
    conferidas_custos = reg.controle_das_linhas_de_custo()
    arc.exigir(conferidas_custos >= 7,
               "o controle das linhas de custo conferiu poucas entradas (%d): a lista nao esta "
               "presa ao `trecho`" % conferidas_custos)
    arc.igual(fmt.linhas_do_jogo(),
              tuple(reg.primeiras_linhas_de_custo("skill"))
              + tuple(reg.primeiras_linhas_de_custo("status")),
              "o checador so pode liberar a PRIMEIRA linha de custo de cada caminho (BANCADA-2)")
    arc.igual(len(fmt.linhas_do_jogo()), 3,
              "o checador tinha de liberar 3 linhas de custo (AP Cost: 1, AP Cost: None, Duration "
              "Type); liberou %d" % len(fmt.linhas_do_jogo()))
    plantada_de_custo = copy.deepcopy(reg.leitura_do_formato())
    plantada_de_custo["caminhos"]["skill"]["custo_no_texto"].append("Dodge Chance: ")
    try:
        reg.controle_das_linhas_de_custo(plantada_de_custo)
    except arc.Falhou as erro:
        arc.exigir("NAO aparece no `trecho`" in str(erro),
                   "o controle reprovou a `custo_no_texto` plantada pelo motivo ERRADO: %s" % erro)
    else:
        arc.exigir(False,
                   "o controle ACEITOU uma `custo_no_texto` com entrada digitada a mao "
                   "('Dodge Chance: ') — a checagem nao dispara")

    # ------------------------------------------------------- 7. A CONTRA-PROVA
    isca = os.path.join(arc.DIR_CONTRA_PROVA, "cp_formato_notas_isca.py")
    ok = os.path.join(arc.DIR_CONTRA_PROVA, "cp_formato_notas_ok.py")
    for caminho in (isca, ok):
        arc.exigir(os.path.isfile(caminho), "a contra-prova do formato sumiu: %s" % caminho)

    cod_isca, saida_isca = arc.executar_arquivo(isca)
    arc.igual(arc.ler_meta(isca).get("esperado"), "reprovar",
              "a isca do formato tem de declarar `esperado: reprovar` no META")
    arc.igual(cod_isca, arc.EXIT_FALHOU,
              "a isca tinha de REPROVAR (exit 1); saida: %s"
              % (saida_isca.strip().splitlines() or ["<sem saida>"])[-1])
    arc.exigir(fmt.MOTIVO_DO_DEFEITO in saida_isca,
               "a isca tinha de reprovar PELO MOTIVO do formato (o desenho antigo quebra), nao por "
               "outra coisa: %s" % (saida_isca.strip().splitlines() or ["<sem saida>"])[-1])

    cod_ok, saida_ok = arc.executar_arquivo(ok)
    arc.igual(cod_ok, arc.EXIT_OK,
              "a metade sem o defeito tinha de PASSAR (exit 0); saida: %s"
              % (saida_ok.strip().splitlines() or ["<sem saida>"])[-1])
    arc.exigir("fecha o formato" in saida_ok,
               "a metade ok tinha de provar que o formato de HOJE fecha; saida: %s"
               % (saida_ok.strip().splitlines() or ["<sem saida>"])[-1])
    arc.igual(_sem_bloco_do_defeito(isca), _sem_bloco_do_defeito(ok),
              "a isca e a metade ok divergem fora do bloco do defeito - nao sao o mesmo teste")

    # ------------------------------------------------- 8. A CONTRA-PROVA DA QUEBRA DO JOGO
    # BANCADA-1: o caso que SEPARA a bancada do runtime. A isca declara UMA quebra antes do custo (a
    # bancada de antes) e tem de REPROVAR; a metade ok declara o numero da leitura e passa. Um teste
    # que passa nos dois mundos nao prova nada.
    isca_q = os.path.join(arc.DIR_CONTRA_PROVA, "cp_formato_quebra_do_jogo_isca.py")
    ok_q = os.path.join(arc.DIR_CONTRA_PROVA, "cp_formato_quebra_do_jogo_ok.py")
    for caminho in (isca_q, ok_q):
        arc.exigir(os.path.isfile(caminho), "a contra-prova da quebra do jogo sumiu: %s" % caminho)

    cod_isca_q, saida_isca_q = arc.executar_arquivo(isca_q)
    arc.igual(arc.ler_meta(isca_q).get("esperado"), "reprovar",
              "a isca da quebra do jogo tem de declarar `esperado: reprovar` no META")
    arc.igual(cod_isca_q, arc.EXIT_FALHOU,
              "a isca da quebra do jogo tinha de REPROVAR (exit 1); saida: %s"
              % (saida_isca_q.strip().splitlines() or ["<sem saida>"])[-1])
    arc.exigir(fmt.MOTIVO_DA_QUEBRA in saida_isca_q,
               "a isca tinha de reprovar PELO MOTIVO da quebra do jogo (a bancada nao reproduz o "
               "jogo), nao por outra coisa: %s"
               % (saida_isca_q.strip().splitlines() or ["<sem saida>"])[-1])

    cod_ok_q, saida_ok_q = arc.executar_arquivo(ok_q)
    arc.igual(cod_ok_q, arc.EXIT_OK,
              "a metade sem o defeito tinha de PASSAR (exit 0); saida: %s"
              % (saida_ok_q.strip().splitlines() or ["<sem saida>"])[-1])
    arc.exigir("reproduz o jogo" in saida_ok_q,
               "a metade ok tinha de provar que a bancada reproduz o jogo; saida: %s"
               % (saida_ok_q.strip().splitlines() or ["<sem saida>"])[-1])
    arc.igual(_sem_bloco_do_defeito(isca_q), _sem_bloco_do_defeito(ok_q),
              "a isca e a metade ok da quebra do jogo divergem fora do bloco do defeito")

    # --------------------------------- 9. A BORDA PLANTADA (BANCADA-2): a linha antes do `Range`
    # O afrouxamento que o conserto do BANCADA-1 trouxe: o checador liberava o BLOCO INTEIRO de custo
    # e aceitava a linha em branco antes de uma linha SEGUINTE (`Range`) — uma forma que o jogo NUNCA
    # escreve. A isca declara o conjunto do BANCADA-1 (bloco inteiro): o texto plantado passa limpo e
    # ela REPROVA; a metade ok declara so as PRIMEIRAS linhas (o BANCADA-2) e o defeito e VISTO.
    isca_r = os.path.join(arc.DIR_CONTRA_PROVA, "cp_formato_linha_antes_do_range_isca.py")
    ok_r = os.path.join(arc.DIR_CONTRA_PROVA, "cp_formato_linha_antes_do_range_ok.py")
    for caminho in (isca_r, ok_r):
        arc.exigir(os.path.isfile(caminho),
                   "a contra-prova da linha antes do `Range` sumiu: %s" % caminho)

    cod_isca_r, saida_isca_r = arc.executar_arquivo(isca_r)
    arc.igual(arc.ler_meta(isca_r).get("esperado"), "reprovar",
              "a isca da linha antes do `Range` tem de declarar `esperado: reprovar` no META")
    arc.igual(cod_isca_r, arc.EXIT_FALHOU,
              "a isca da linha antes do `Range` tinha de REPROVAR (exit 1); saida: %s"
              % (saida_isca_r.strip().splitlines() or ["<sem saida>"])[-1])
    arc.exigir(fmt.MOTIVO_DA_LINHA_ANTES_DO_RANGE in saida_isca_r,
               "a isca tinha de reprovar PELO MOTIVO da borda (o bloco inteiro liberado aceita a "
               "forma que o jogo nao escreve), nao por outra coisa: %s"
               % (saida_isca_r.strip().splitlines() or ["<sem saida>"])[-1])

    cod_ok_r, saida_ok_r = arc.executar_arquivo(ok_r)
    arc.igual(cod_ok_r, arc.EXIT_OK,
              "a metade sem o defeito tinha de PASSAR (exit 0); saida: %s"
              % (saida_ok_r.strip().splitlines() or ["<sem saida>"])[-1])
    arc.exigir("o checador VIU" in saida_ok_r,
               "a metade ok tinha de provar que o checador VE a linha em branco antes do `Range`; "
               "saida: %s" % (saida_ok_r.strip().splitlines() or ["<sem saida>"])[-1])
    arc.igual(_sem_bloco_do_defeito(isca_r), _sem_bloco_do_defeito(ok_r),
              "a isca e a metade ok da linha antes do `Range` divergem fora do bloco do defeito")

    print("formato fechado em %d casos (%d familia(s)): 1 e 2 notas, "
          "nota(s) antes da linha azul, uma linha em branco por bloco; %d linhas de invocacao com "
          "o ataque basico primeiro (%s reordenadas: %s); isca REPROVOU e a metade ok PASSOU"
          % (len(casos), len(familias), linhas, len(REORDENADAS), ", ".join(REORDENADAS)))
    print("quebra do jogo: %d quebras antes do `AP Cost` (l.1470 + l.1536) = UMA linha em branco do "
          "JOGO; a bancada monta o MESMO texto, o ground effect (shrine) nao tem custo, a leitura foi "
          "conferida contra o decompilado (%d linha(s), fontes: %s), o controle REPROVA a leitura "
          "plantada (numero trocado e linha deslocada) e a isca da quebra REPROVOU"
          % (do_jogo, conferidas, ", ".join(fontes) or "nenhuma nesta maquina"))
    print("BANCADA-2: o checador libera SO a PRIMEIRA linha de custo de cada caminho (%d no total) — "
          "a linha em branco antes do `Range` (e das outras linhas SEGUINTES) e REPROVADA; a "
          "`custo_no_texto` (%d entrada(s)) passou pelo controle do `trecho` e o controle REPROVOU a "
          "entrada plantada a mao; a isca da borda REPROVOU e a metade ok PASSOU"
          % (len(fmt.linhas_do_jogo()), conferidas_custos))


def _sem_bloco_do_defeito(caminho):
    """O texto a partir do `def corpo` sem as linhas do BLOCO-DO-DEFEITO (a metade que muda)."""
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


if __name__ == "__main__":
    arc.main(META, corpo)
