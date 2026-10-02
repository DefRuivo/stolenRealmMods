#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_formato.py — a bancada do FORMATO das notas (RV-17), ao lado de `regras_cor.py`.

O QUE MORA AQUI
---------------
A REGRA DE FORMATO do tooltip, em codigo, e o material REAL para exercita-la. Nao e um teste: nao
tem META nem `corpo()`. Quem le sao os testes da familia (`testes/puros/t_formato_notas.py`) e a
contra-prova (`contra-prova/cp_formato_notas_isca.py` / `..._ok.py`).

A REGRA (docs/TEXTO-TOOLTIPS.md §9)
-----------------------------------
Depois da descricao do jogo (nivel 1, intocada), cada bloco que o mod escreve vai para o FIM do
corpo do tooltip, na ORDEM em que aparece no texto de origem, separado do que vem antes por
EXATAMENTE UMA LINHA EM BRANCO — e nada mais. O mod nao escreve linha em branco em outro lugar: nem
no fim do tooltip, nem onde um bloco foi retirado. A linha azul do nivel 3 (auras ativas / skills no
status) e sempre a ULTIMA.

BANCADA-1 (01/10) — A EXCECAO QUE FALTAVA, E QUE E DO JOGO. "Nao existe linha em branco em outro
lugar" era FALSO: o proprio `ShowSkillTooltip` escreve UMA LINHA EM BRANCO antes do bloco de custos
(l.1470 `original += "\n"` + l.1536 `original + "\n" + "AP Cost: ..."`), e o `ShowActionStatusTooltip`
escreve `"\n\n"` antes do `Duration Type` (l.1013). Ela existe na tooltip vanilla, sem mod nenhum.
A bancada montava os custos com UMA quebra — nao reproduzia o jogo — e o checador acusava o texto do
jogo de "linha em branco orfa". A leitura esta na fixture `formato-notas.entrada.json` (trechos
literais do decompilado) e o caso que SEPARA os dois mundos e o do caminho da skill.

O FORMATO E UM SO. O que muda entre os casos e QUANTOS blocos o tooltip tem:

  * UMA nota  — a maioria (`TextAppends`) e as entradas FUNDIDAS do `TextFixes`;
  * DUAS notas — os dois casos reais (`Shapeshift Dragonkin`, que tem `[0]`, e o buff `Miniature`),
    com os dois blocos dentro do MESMO valor fundido.

E a ORDEM DAS HABILIDADES nas notas de INVOCACAO: quando o bicho tem ataque basico no asset
(`Melee Attack` / `Ranged Attack`), ele vem PRIMEIRO e as especializadas depois — o inverso da
ordem do asset em Stag, Moose, Panther e Timber Wolf.
"""
import csv
import os
import re
import sys

import arcabouco as arc
import regras_cor as reg

# O parser UNICO das tabelas do projeto (`tools/tabelas.py`, PARSER-1): e o mesmo que a trava de
# cor usa, e o unico que ve as entradas com COMENTARIO entre o `{` e a chave — exatamente duas
# delas, o `Shapeshift Dragonkin` e o `Miniature`, sao os casos com DUAS notas.
_DIR_TOOLS = os.path.dirname(arc.DIR_ARCADOUCO)
if _DIR_TOOLS not in sys.path:
    sys.path.insert(0, _DIR_TOOLS)
import tabelas

NL = chr(10)
BS = chr(92)

# O fecho comum a TODA nota de invocacao: identifica a familia sem depender de nome de bicho.
FAMILIA_INVOCACAO = "Does not copy your attributes."
BASICAS = ("Melee Attack", "Ranged Attack")
CUSTOS = ("AP Cost: 1", "Range: Melee")

CAMINHO_DUMP = os.path.join("docs", "cobertura", "invocacoes.csv")


# ------------------------------------------------------------------- a REGRA ---

def aberturas_de_bloco():
    """As aberturas `<color=#...>` que podem INICIAR um bloco nosso: o marcador do nivel 2 (o
    valor de reserva, quando a leitura do campo falha) e as cores resolvidas dos niveis 2 e 3."""
    cores = (reg.entrada_marcador(), reg.cor_do_nivel_2(), reg.cor_da_linha_azul())
    return tuple("<color=" + c + ">" for c in cores)


def linhas_do_jogo():
    """As linhas de CUSTOS/METADADOS que o PROPRIO JOGO escreve DEPOIS da linha em branco dele —
    SO A PRIMEIRA de cada caminho: o `AP Cost` da skill e o `Duration Type` do status (BANCADA-2).

    As linhas SEGUINTES do bloco de custo (`Range`, `Blast Radius`, `Mana Cost`, `Cooldown` —
    l.1558/1561/1565/1572) vem com UMA quebra cada: o jogo NAO poe linha em branco antes delas. O
    checador do BANCADA-1 liberava o bloco INTEIRO e com isso aceitava uma forma que o jogo NUNCA
    escreve (`descricao \\n\\n AP Cost \\n\\n Range`) — o afrouxamento que a revisao (BANCADA-1R)
    mediu executando. A classificacao sai de `reg.primeiras_linhas_de_custo`, do TRECHO VERIFICADO."""
    return (tuple(reg.primeiras_linhas_de_custo("skill"))
            + tuple(reg.primeiras_linhas_de_custo("status")))


def linhas_do_jogo_do_bloco_inteiro():
    """[SO PARA A CONTRA-PROVA] o conjunto do BANCADA-1: o bloco INTEIRO de custo dos dois caminhos.
    E o afrouxamento que o BANCADA-2 restringe — com ele, uma linha em branco antes de QUALQUER linha
    de custo (ate o `Range`) era aceita. Fica aqui para a contra-prova reproduzir o defeito e provar
    que a borda plantada era CEGA antes do conserto."""
    return tuple(reg.custos_do_jogo("skill")) + tuple(reg.custos_do_jogo("status"))


def eh_linha_do_jogo(depois, liberadas=None):
    """`depois` (o texto que vem logo apos uma linha em branco) abre uma linha do JOGO?

    `liberadas` permite a contra-prova passar o conjunto do bloco INTEIRO (o defeito do BANCADA-1);
    `None` = so a PRIMEIRA linha de custo de cada caminho (o BANCADA-2)."""
    if liberadas is None:
        liberadas = linhas_do_jogo()
    return any(depois.startswith(linha) for linha in liberadas)


def defeitos_de_linha_em_branco(corpo, liberadas=None):
    """A REGRA em codigo. Devolve a lista de defeitos (vazia = formato certo).

    Uma linha em branco so e legitima quando: (a) ela e o SEPARADOR de um bloco nosso — o que vem
    imediatamente depois dela e a abertura de um bloco colorido; ou (b) ela e a separacao que o
    PROPRIO JOGO escreve antes da PRIMEIRA linha de custos/metadados da tooltip (`AP Cost` na skill,
    `Duration Type` no status — l.1470+1536 e l.1013; a leitura esta na fixture
    `formato-notas.entrada.json`). Em qualquer outro lugar ela e a sobra de um bloco que saiu dali
    (o defeito que o RV-17 fechou no `InicioDoSeparador`). O corpo nao pode terminar com quebra: o
    tooltip nao acaba com linha em branco.

    BANCADA-1 (01/10) — A CORRECAO DO CHECADOR. A regra antiga so aceitava (a), e por isso acusava o
    texto DO JOGO de "linha em branco orfa": a linha em branco antes do `AP Cost` existe na tooltip
    vanilla, sem mod nenhum. Era a bancada que estava errada, nao o jogo.

    BANCADA-2 (01/10) — A BORDA QUE O CONSERTO ABRIU. O BANCADA-1 liberou o BLOCO INTEIRO de custo, e
    com isso a linha em branco antes de uma linha SEGUINTE (`Range`, `Blast Radius`, `Mana Cost`,
    `Cooldown`) — uma forma que o jogo NUNCA escreve — passava em silencio. `linhas_do_jogo()` hoje
    traz so a PRIMEIRA linha de custo de cada caminho; `liberadas` existe para a contra-prova
    reproduzir o conjunto antigo. O caso plantado ("linha em branco antes do `Range`") e o que pega.
    """
    defeitos = []
    if corpo != corpo.rstrip():
        defeitos.append("o tooltip termina com quebra / linha em branco: %r" % corpo[-26:])
    if NL * 3 in corpo:
        defeitos.append("DUAS linhas em branco seguidas (o defeito do RV-17(a))")
    aberturas = aberturas_de_bloco()
    i = 0
    while True:
        j = corpo.find(NL + NL, i)
        if j < 0:
            break
        depois = corpo[j + 2:]
        if not depois.startswith(aberturas) and not eh_linha_do_jogo(depois, liberadas):
            defeitos.append("linha em branco ORFA (nao separa nenhum bloco nosso): %r"
                            % corpo[max(0, j - 30):j + 30])
        i = j + 2
    return defeitos


def defeitos_da_quebra_do_jogo(corpo, custos):
    """A PRIMEIRA linha do bloco de custos do jogo tem de vir depois da LINHA EM BRANCO dele.

    O `ShowSkillTooltip` escreve DUAS quebras entre a descricao e o `AP Cost` (l.1470 + l.1536), e o
    `ShowActionStatusTooltip` escreve `"\\n\\n"` antes do `Duration Type` (l.1013): a linha em branco
    ANTES do bloco de metadados e do jogo. Sem ela a bancada esta montando um texto que o jogo NAO
    escreve — e um teste de formato preso nisso trava o formato errado. (Era o defeito da bancada
    antes do BANCADA-1: `texto.rstrip("\\n") + "\\n" + custo`.)

    So a PRIMEIRA linha do bloco e conferida: as seguintes (`Range`, `Mana Cost`, `Cooldown` —
    l.1558/1565/1572) vem com UMA quebra cada, logo NAO tem linha em branco antes.
    """
    if not custos:
        return []
    primeira = custos[0]
    inteiro = NL * reg.quebras_antes_do_custo_do_jogo()
    if primeira in corpo and (inteiro + primeira) not in corpo:
        return ["o custo %r ficou SEM a linha em branco que o JOGO escreve antes dele" % primeira]
    return []


def _abertura_do_bloco(corpo, miolo):
    """Indice da ABERTURA `<color=#...>` do bloco cujo conteudo e `miolo` — nao o indice do
    conteudo: a linha em branco do separador vem antes da abertura.

    Procura o PAR (`<color=#...>` + conteudo), e nao so o conteudo: um texto curto pode casar
    dentro de um literal de cor (`#CBB396` tem um `B`), e a posicao sairia antes do bloco.
    """
    for abertura in aberturas_de_bloco():
        i = corpo.find(abertura + miolo)
        if i >= 0:
            return i
    return None


def defeitos_da_ordem(corpo, notas, aura=None, custos=CUSTOS):
    """A ORDEM: todas as notas no fim, na ordem do texto de origem, cada uma depois dos custos e
    antes da linha azul (nivel 3), que e sempre a ultima."""
    defeitos = []
    posicoes = []
    for miolo in notas:
        k = _abertura_do_bloco(corpo, miolo)
        if k is None:
            defeitos.append("a NOTA %r sumiu do tooltip" % miolo[:48])
            continue
        posicoes.append((k, miolo))
        if not corpo[:k].endswith(NL + NL):
            defeitos.append("a NOTA %r nao esta precedida de UMA linha em branco" % miolo[:48])
    ordem = [i for i, _ in posicoes]
    if ordem != sorted(ordem) or len(set(ordem)) != len(ordem):
        defeitos.append("as NOTAS nao estao na ordem em que aparecem no texto de origem (o defeito"
                        " dos dois casos com duas notas)")
    for custo in custos:
        if custo in corpo and ordem and corpo.find(custo) > min(ordem):
            defeitos.append("o custo %r ficou DEPOIS de uma nota (a nota tinha de ir para o fim,"
                            " depois dos custos)" % custo)
    if aura is not None:
        i = corpo.find(aura)
        if i < 0:
            defeitos.append("a linha azul do nivel 3 (%r) sumiu do tooltip" % aura[:48])
        elif ordem and i < max(ordem):
            defeitos.append("a linha azul do nivel 3 nao e a ULTIMA coisa do tooltip")
    return defeitos


# ------------------------------------------------------------ material real ---

def _miolo(texto):
    """O texto de dentro do ULTIMO bloco com o marcador (o CONTEUDO da nota, sem as tags)."""
    abre = "<color=" + reg.entrada_marcador() + ">"
    i = texto.rfind(abre)
    if i < 0:
        return texto.strip(NL)
    j = texto.find(reg.FECHA_COR, i)
    return texto[i + len(abre):j]


def entradas_da_tabela(nome):
    """(chave, valor) DECODIFICADOS de TODAS as entradas da tabela — pelo parser unico do projeto
    (`tools/tabelas.py`), o mesmo da trava de cor, que ve as entradas com COMENTARIO entre o `{` e
    a chave (o `Shapeshift Dragonkin` e o `Miniature` vivem exatamente nesse formato)."""
    return tabelas.pares(reg.fonte_do_mod(), nome)


def _blocos_fundidos(valor):
    """(texto do nivel 1, [blocos]) de um valor de `TextFixes` com N blocos do marcador."""
    abre = "<color=" + reg.entrada_marcador() + ">"
    if abre not in valor:
        return valor, []
    nivel1 = valor.split(abre, 1)[0]
    blocos, resto = [], valor[len(nivel1):]
    while resto.startswith(abre):
        fim = resto.find(reg.FECHA_COR, len(abre))
        blocos.append(resto[:fim + len(reg.FECHA_COR)])
        resto = resto[fim + len(reg.FECHA_COR):]
        if resto.startswith(NL):
            resto = resto[1:]
    return nivel1.rstrip(" " + NL), blocos


def valores_fundidos_com_duas_notas():
    """Os VALORES reais do `TextFixes` que carregam DUAS notas do nivel 2."""
    abre = "<color=" + reg.entrada_marcador() + ">"
    return [v for _c, v in entradas_da_tabela("TextFixes") if v.count(abre) == 2]


def _valor_fundido_com(trecho):
    """O valor de `TextFixes` que contem `trecho`."""
    for _chave, valor in entradas_da_tabela("TextFixes"):
        if trecho in valor:
            return valor
    raise arc.Falhou("nao achei no `TextFixes` nenhum valor com %r" % trecho)


# ----------------------------------------------------------------- os casos ---

def caso_skill(quebras=None):
    """FAMILIA 1 — skill com DANO: a nota vem das `TextAppends` e o `*0` e o valor do motor."""
    chave, nota = reg.pares_de_skill_com_dano()[0]
    texto, registro = reg.monta_a_descricao(chave, nota, dano="42", custos=CUSTOS,
                                            quebras_antes_do_custo=quebras_ou_padrao(quebras))
    return {"rotulo": "skill com dano (TextAppends)", "texto": texto, "registro": registro,
            "notas": [_miolo(nota)], "aura": None, "custos": CUSTOS}


def caso_shrine(quebras=None):
    """FAMILIA 2 — SHRINE: o `[0]` do nivel 1, a nota do nivel 2 e a linha azul do nivel 3.

    BANCADA-1: a tooltip de shrine NAO e a de skill — e a do GROUND EFFECT (`ShowGroundEffectTooltip`,
    l.1219-1304), que NAO tem `AP Cost` nem `Range` e envolve o texto no TITULO + `<size>` +
    `Turns Remaining` + linha de TIME. Modelar shrine como skill media um texto que o jogo nao monta.
    """
    chave, nota = reg.par_de_shrine()
    aura = "<color=" + reg.cor_da_linha_azul() + ">Your active shrine auras: " \
           "Dodge +40% (total +57%).</color>"
    texto, registro = reg.monta_a_descricao(chave, nota, expressao="40", aura=aura)
    texto = reg.molda_ground_effect(texto, "Dodge Shrine")
    return {"rotulo": "shrine com valor + linha azul do nivel 3", "texto": texto,
            "registro": registro, "notas": [_miolo(nota)], "aura": "Your active shrine auras:",
            "custos": (),
            "caminho": "ground_effect"}


def caso_invocacao(quebras=None):
    """FAMILIA 3 — INVOCACAO: a nota e FUNDIDA no valor do `TextFixes` (uma so)."""
    nivel1, blocos = _blocos_fundidos(_valor_fundido_com("Timber Wolf: Melee Attack"))
    texto, registro = reg.monta_a_descricao("", None, valor_sem_cor=nivel1, notas=blocos,
                                            custos=CUSTOS,
                                            quebras_antes_do_custo=quebras_ou_padrao(quebras))
    return {"rotulo": "invocacao (valor FUNDIDO no TextFixes)", "texto": texto,
            "registro": registro, "notas": [_miolo(b) for b in blocos], "aura": None,
            "custos": CUSTOS}


def casos_duas_notas(quebras=None):
    """FAMILIA 4 — os DOIS casos reais de DUAS notas: `Shapeshift Dragonkin` (que tem `[0]`, e era
    um dos atingidos pelo defeito do valor no fundo) e o buff `Miniature`."""
    casos = []
    for valor in valores_fundidos_com_duas_notas():
        nivel1, blocos = _blocos_fundidos(valor)
        texto, registro = reg.monta_a_descricao("", None, valor_sem_cor=nivel1, notas=blocos,
                                                expressao=("30" if "[0]" in nivel1 else None),
                                                custos=CUSTOS,
                                                quebras_antes_do_custo=quebras_ou_padrao(quebras))
        casos.append({"rotulo": "DUAS notas (%s)" % _rotulo(nivel1), "texto": texto,
                      "registro": registro, "notas": [_miolo(b) for b in blocos], "aura": None,
                      "custos": CUSTOS})
    return casos


def quebras_ou_padrao(quebras):
    """`None` = a regra DA BANCADA (o valor que o montador usa por padrao)."""
    return reg.QUEBRAS_ANTES_DO_CUSTO_DA_BANCADA if quebras is None else quebras


def _rotulo(nivel1):
    for marca in ("Dragonkin", "Miniature"):
        if marca.lower() in nivel1.lower():
            return marca
    return nivel1[:34]


def casos(quebras=None):
    """Todos os casos de formato, com o rotulo da familia.

    `quebras` = quantas quebras a bancada escreve antes do 1o custo (`None` = a regra de hoje)."""
    return ([caso_skill(quebras), caso_shrine(quebras), caso_invocacao(quebras)]
            + casos_duas_notas(quebras))


# ------------------------------------------------------------ contra-prova ---

# O motivo que a contra-prova cita quando o desenho ANTIGO quebra o formato.
MOTIVO_DO_DEFEITO = "o formato SAIA QUEBRADO (linha em branco orfa e/ou 2a nota antes do AP Cost)"

REGRAS = ("rv17", "antiga")


def aplica_com_a_regra(caso, regra):
    """Roda o prefixo com a regra pedida:

      * `"rv17"`   — a de hoje: TODAS as notas, na ordem, e a linha em branco INTEIRA consumida;
      * `"antiga"` — a de ANTES do RV-17: so a PRIMEIRA nota e UMA quebra do separador consumida.
    """
    if regra == "rv17":
        return reg.aplica_o_prefixo(caso["texto"], caso["registro"], regra_antiga=False)
    return reg.aplica_o_prefixo(caso["texto"], caso["registro"], regra_antiga=False,
                                todas_as_notas=False, consome_a_linha_inteira=False)


def casos_quebrados(regra):
    """`[(rotulo, [defeitos])]` dos casos em que o formato NAO fecha com essa regra."""
    quebrados = []
    for caso in casos():
        depois = aplica_com_a_regra(caso, regra)
        d = (defeitos_de_linha_em_branco(depois)
             + defeitos_da_ordem(depois, caso["notas"], caso["aura"], caso["custos"])
             + defeitos_da_quebra_do_jogo(depois, caso["custos"]))
        if d:
            quebrados.append((caso["rotulo"], d))
    return quebrados


def corpo_da_contra_prova(regra, quebrados_esperados):
    """O corpo COMPARTILHADO pela isca e pela metade ok (as duas sao o MESMO teste).

    `quebrados_esperados` e a EXPECTATIVA do desenho: 0 na isca (antes do RV-17 se acreditava que o
    tooltip saia certo — o defeito nao existia) e 0 na metade ok (o formato de hoje nao quebra
    nada). Como o desenho antigo QUEBRA mesmo, a isca reprova citando `MOTIVO_DO_DEFEITO`; a metade
    ok passa.
    """
    quebrados = casos_quebrados(regra)
    if len(quebrados) != quebrados_esperados:
        detalhe = "; ".join("%s -> %s" % (r, d[0]) for r, d in quebrados[:2])
        raise arc.Falhou("%s: a regra '%s' quebrou %d caso(s) (esperado %d) — %s"
                         % (MOTIVO_DO_DEFEITO, regra, len(quebrados), quebrados_esperados, detalhe))
    return ("a regra '%s' fecha o formato nos %d casos: 0 defeito de linha em branco, 0 de ordem e "
            "0 da quebra do jogo" % (regra, len(casos())))


# ------------------------------------------- BANCADA-1: a bancada x o runtime ---

# O motivo que a contra-prova da QUEBRA DO JOGO cita quando a bancada nao reproduz o jogo.
MOTIVO_DA_QUEBRA = ("a BANCADA nao reproduz o JOGO: os custos sao juntados com outro numero de "
                    "quebras que o `ShowSkillTooltip` escreve (l.1470 + l.1536)")

# O caso que SEPARA os dois mundos: e o caminho da skill, onde o jogo escreve DUAS quebras antes do
# `AP Cost` (uma linha em branco) e a bancada antiga escrevia UMA (nenhuma).
ROTULO_QUE_SEPARA = "skill com dano (TextAppends)"


def texto_do_caminho(rotulo=None, quebras=None):
    """O texto FINAL (o que chega ao `Tooltip.ShowTooltip`, ja com o prefixo do mod) de um caso,
    montado com `quebras` quebras antes do 1o custo. `None` = a regra da BANCADA."""
    for caso in casos(quebras):
        if rotulo is None or caso["rotulo"] == rotulo:
            return aplica_com_a_regra(caso, "rv17")
    raise arc.Falhou("nao achei o caso %r nos casos de formato" % (rotulo,))


def texto_do_runtime(rotulo=ROTULO_QUE_SEPARA):
    """O texto que o JOGO produz: montado com o numero de quebras da LEITURA (a fixture)."""
    return texto_do_caminho(rotulo, quebras_da_leitura())


def quebras_da_leitura():
    """O numero de quebras que a LEITURA do decompilado (a fixture) manda a bancada usar antes do 1o
    custo. E o numero que o `cp_formato_quebra_do_jogo_ok.py` declara — e o que a contra-prova da
    isca planta como 1."""
    return reg.quebras_antes_do_custo_do_jogo()


def texto_da_bancada(rotulo=ROTULO_QUE_SEPARA):
    """O texto que a BANCADA produz: montado com a regra dela (`QUEBRAS_ANTES_DO_CUSTO_DA_BANCADA`)."""
    return texto_do_caminho(rotulo, reg.QUEBRAS_ANTES_DO_CUSTO_DA_BANCADA)


def lado_a_lado():
    """O texto do RUNTIME e o da BANCADA, para a prova ser lida (nao so assertada)."""
    return (("JOGO     (%d quebras = 1 linha em branco antes do `AP Cost`)"
             % reg.quebras_antes_do_custo_do_jogo(),
             texto_do_runtime().replace(NL, " / ")),
            ("BANCADA  (%d quebra(s))" % reg.QUEBRAS_ANTES_DO_CUSTO_DA_BANCADA,
             texto_da_bancada().replace(NL, " / ")))


def corpo_da_contra_prova_da_quebra(quebras_da_bancada):
    """O corpo COMPARTILHADO pela isca e pela metade ok da QUEBRA DO JOGO (BANCADA-1).

    `quebras_da_bancada` e o que a bancada declara escrever antes do 1o custo: 1 na ISCA (a bancada
    de antes do BANCADA-1) e o valor da LEITURA na metade ok. A isca tem de REPROVAR: e ela que
    prova que o caso separa os dois mundos (um teste que passa nos dois nao prova nada).
    """
    do_jogo = texto_do_runtime()
    da_bancada = texto_do_caminho(ROTULO_QUE_SEPARA, quebras_da_bancada)
    if da_bancada != do_jogo:
        raise arc.Falhou("%s — eu esperava o texto do jogo.\n  JOGO:    %r\n  BANCADA: %r"
                         % (MOTIVO_DA_QUEBRA, do_jogo, da_bancada))
    # E a prova nao pode passar por ACIDENTE: o caminho do ground effect (a tooltip de SHRINE) NAO
    # tem `AP Cost` — separar um caminho do outro faz parte da leitura.
    if reg.tem_ap_cost_no_texto():
        raise arc.Falhou("a leitura do formato diz que o GROUND EFFECT tem bloco de custo: %r"
                         % (reg.custos_do_jogo("ground_effect"),))
    for caso in casos(quebras_da_bancada):
        if caso.get("caminho") == "ground_effect":
            depois = aplica_com_a_regra(caso, "rv17")
            if "AP Cost" in depois or "Range: Melee" in depois:
                raise arc.Falhou("o caso de SHRINE (ground effect) saiu com custo de SKILL: %r"
                                 % depois[-160:])
    return ("a bancada reproduz o jogo: as %d quebras da l.1470 + l.1536, a mesma linha em branco "
            "antes do `AP Cost` (e o ground effect continua sem custo)"
            % reg.quebras_antes_do_custo_do_jogo())


# ------------------------------------- BANCADA-2: a linha em branco antes do `Range` ---

# O motivo que a contra-prova cita quando o checador NAO ve a borda plantada.
MOTIVO_DA_LINHA_ANTES_DO_RANGE = (
    "o checador ACEITOU a linha em branco antes do `Range` — uma forma que o JOGO nunca escreve: "
    "ele so escreve a linha em branco antes da PRIMEIRA linha de custo de cada caminho")


def texto_com_linha_antes_do_range():
    """A forma PLANTADA: `descricao \\n\\n AP Cost \\n\\n Range` — uma linha em branco antes de uma
    linha de custo SEGUINTE (`Range`), que o jogo escreve com UMA quebra. Antes do BANCADA-2 o
    checador aceitava (o bloco inteiro era liberado); hoje ela tem de ser VISTA."""
    return "D" + NL * 2 + CUSTOS[0] + NL * 2 + CUSTOS[1]


def corpo_da_contra_prova_da_linha_antes_do_range(liberadas):
    """O corpo COMPARTILHADO pela isca e pela metade ok (BANCADA-2).

    `liberadas` = as linhas que o checador toma como do jogo. Na ISCA e o bloco INTEIRO (o
    afrouxamento que o BANCADA-1 deixou): o texto plantado PASSA em silencio — a borda era CEGA — e
    o teste REPROVA citando `MOTIVO_DA_LINHA_ANTES_DO_RANGE`. Na metade ok sao so as PRIMEIRAS linhas
    (o BANCADA-2): o defeito e VISTO e a metade PASSA.
    """
    texto = texto_com_linha_antes_do_range()
    defeitos = defeitos_de_linha_em_branco(texto, liberadas)
    if not defeitos:
        raise arc.Falhou("%s — o texto plantado passou limpo: %r"
                         % (MOTIVO_DA_LINHA_ANTES_DO_RANGE, texto))
    return ("o checador VIU a linha em branco antes do `Range` (o defeito do BANCADA-2): %s"
            % defeitos[0])


# Os arquivos onde o decompilado do TIPO `Tooltip` pode estar (o controle EXTERNO da leitura).
# `scratch/` NAO e versionado: numa maquina sem ele o controle externo nao roda e o interno (que
# roda sempre) e quem segura a leitura na linha.
_CAMINHOS_DO_DECOMPILADO = (
    ("SR_DECOMPILADO", os.environ.get("SR_DECOMPILADO")),
    ("scratch/rv22/tooltip.cs", os.path.join(arc.raiz_do_repo(), "scratch", "rv22", "tooltip.cs")),
    ("cache do decompilado integral",
     os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes", "cache", "scratch", "cs",
                  "Assembly-CSharp.decompiled.cs")),
)


def fontes_do_decompilado():
    """`[(rotulo, linhas)]` dos arquivos do decompilado do tipo que existem NESTA maquina."""
    achados = []
    for rotulo, caminho in _CAMINHOS_DO_DECOMPILADO:
        if caminho and os.path.isfile(caminho):
            with open(caminho, encoding="utf-8", errors="replace") as fh:
                achados.append((rotulo, fh.read().splitlines()))
    return achados


def linhas_lidas_do_formato(leitura=None):
    """Todas as linhas da leitura, com o caminho a que pertencem: `[(caminho, linha)]`.

    `leitura` permite conferir uma leitura PLANTADA (o controle tem de saber REPROVAR uma leitura
    com o numero ou o trecho trocado — checagem que nunca dispara nao e checagem)."""
    if leitura is None:
        leitura = reg.leitura_do_formato()
    achados = []
    for nome, caminho in sorted(leitura["caminhos"].items()):
        for linha in caminho["linhas"]:
            achados.append((nome, linha))
        for linha in caminho.get("linhas_seguintes", []):
            achados.append((nome, linha))
    return achados


def controle_da_leitura_do_formato(leitura=None):
    """Confere a LEITURA do formato — e ela NAO pode ser decoracao.

    INTERNO (roda sempre): cada `ramo_que_roda` tem de estar CONTIDO no `trecho` literal do
    decompilado, e o `quebras` de cada linha tem de ser a contagem dos escapes `\\n` do ramo — o
    numero NUNCA e digitado a mao na fixture.

    EXTERNO (quando existe o decompilado nesta maquina): cada `trecho` tem de aparecer LITERALMENTE,
    na LINHA declarada, em pelo menos um dos arquivos do tipo. Um trecho inventado — ou deslocado
    para outra linha — reprova.

    Devolve (quantas linhas foram conferidas, [rotulos dos arquivos usados]).
    """
    fontes = fontes_do_decompilado()
    conferidas = 0
    for nome, linha in linhas_lidas_do_formato(leitura):
        trecho = linha["trecho"]
        arc.exigir(trecho.strip(), "a leitura do formato tem um `trecho` vazio no caminho %r" % nome)
        ramo = linha.get("ramo_que_roda")
        if ramo is not None:
            arc.exigir(ramo in trecho,
                       "a leitura do formato de %r: o `ramo_que_roda` nao esta contido no `trecho` "
                       "literal do decompilado" % nome)
            arc.igual(linha.get("quebras"), ramo.count(BS + "n"),
                      "a leitura do formato de %r: `quebras` tem de ser a contagem dos escapes "
                      "`\\n` do ramo (nao um numero digitado)" % nome)
        for rotulo, arquivo in fontes:
            if linha["linha"] - 1 < len(arquivo) and trecho in arquivo[linha["linha"] - 1]:
                conferidas += 1
                break
        else:
            if fontes:
                raise arc.Falhou(
                    "a leitura do formato de %r NAO bate com o decompilado: o trecho da l.%d nao "
                    "esta literalmente nessa linha de nenhum dos arquivos (%s)"
                    % (nome, linha["linha"], ", ".join(r for r, _ in fontes)))
    return conferidas, [rotulo for rotulo, _ in fontes]


# ------------------------------------------------------- ordem das habilidades ---

def dump_das_invocacoes():
    """`{criatura: [habilidades]}` do dump versionado `docs/cobertura/invocacoes.csv`. A ORDEM e a
    do ASSET (repeticao removida) — e e dela que a NOTA diverge quando poe o ataque basico
    primeiro."""
    caminho = os.path.join(arc.raiz_do_repo(), CAMINHO_DUMP)
    criaturas = {}
    with open(caminho, encoding="utf-8-sig") as fh:
        for linha in csv.DictReader(fh):
            for nome, habilidades in re.findall(r"([^\[\];]+)\[([^\]]*)\]", linha["criaturas"]):
                lista = []
                for h in (x.strip() for x in habilidades.split(",")):
                    if h and h not in lista:
                        lista.append(h)
                criaturas.setdefault(nome.strip(), lista)
    return criaturas


def _nome_no_dump(nome, nomes):
    """`Bear (a Grizzly)` -> `Grizzly`: a nota nomeia o bicho pelo rotulo do sorteio."""
    if nome in nomes:
        return nome
    m = re.search(r"\(([^)]+)\)", nome)
    if m:
        interno = m.group(1).strip()
        interno = interno[2:].strip() if interno.lower().startswith("a ") else interno
        if interno in nomes:
            return interno
    return None


def criaturas_das_notas():
    """`[(nota, [(criatura, [habilidades])])]` das notas de invocacao REAIS das tabelas.

    Uma linha so entra se o nome for de uma criatura do dump e TODAS as habilidades dela estiverem
    no vocabulario do dump — o parser nao adivinha: linha que nao casa nao entra (e o teste exige
    um minimo, para nao passar com o parser vazio).
    """
    dump = dump_das_invocacoes()
    nomes = set(dump)
    vocabulario = {h for lista in dump.values() for h in lista}
    achados = []
    for tabela in ("TextAppends", "TextFixes"):
        for _chave, valor in entradas_da_tabela(tabela):
            if FAMILIA_INVOCACAO not in valor:
                continue
            itens = []
            for linha in _miolo(valor).split(NL):
                linha = linha.strip().lstrip("-").strip()
                if ":" not in linha:
                    continue
                nome, resto = linha.split(":", 1)
                nome, habilidades = nome.strip(), [h.strip() for h in resto.split(",") if h.strip()]
                if not nome or not habilidades or not all(h in vocabulario for h in habilidades):
                    continue
                itens.append((nome, habilidades))
            if itens:
                achados.append((_miolo(valor), itens))
    return achados


def defeitos_da_ordem_das_habilidades():
    """A ORDEM DAS HABILIDADES em codigo: quando o bicho tem ataque basico, ele vem PRIMEIRO.

    Devolve a lista de defeitos. Confere, alem da ordem, que as habilidades da nota BATEM com as
    do dump (conjunto, sem ordem) — sem isso a trava so compararia a nota com ela mesma.
    """
    dump = dump_das_invocacoes()
    nomes = set(dump)
    defeitos = []
    for nota, itens in criaturas_das_notas():
        for nome, habilidades in itens:
            do_dump = _nome_no_dump(nome, nomes)
            if do_dump is None:
                defeitos.append("a nota cita %r, que nao existe no dump `%s`" % (nome, CAMINHO_DUMP))
                continue
            if sorted(set(habilidades)) != sorted(dump[do_dump]):
                defeitos.append("%s: a nota diz %s, o dump diz %s"
                                % (do_dump, habilidades, dump[do_dump]))
                continue
            basicas = [h for h in habilidades if h in BASICAS]
            if basicas and habilidades[0] not in BASICAS:
                defeitos.append("%s: o ataque basico tem de vir PRIMEIRO; a nota diz %s"
                                % (do_dump, habilidades))
    return defeitos


def reordenadas_pelo_mod():
    """As criaturas em que a NOTA diverge da ORDEM DO ASSET (o ataque basico primeiro): a prova de
    que a regra foi APLICADA, e nao que as notas ja nasceram na ordem certa."""
    dump = dump_das_invocacoes()
    nomes = set(dump)
    achadas = []
    for _nota, itens in criaturas_das_notas():
        for nome, habilidades in itens:
            do_dump = _nome_no_dump(nome, nomes)
            if do_dump and sorted(set(habilidades)) == sorted(dump[do_dump]):
                if habilidades != dump[do_dump]:
                    achadas.append(do_dump)
    return sorted(set(achadas))
