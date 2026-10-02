#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_nivel3.py — a bancada do NIVEL 3 que NAO e a linha de auras (NIV3-1).

POR QUE ESTA BANCADA EXISTE
---------------------------
A convencao de texto (docs/TEXTO-TOOLTIPS.md §9.1) promete: *cada bloco que o mod escreve vai para o
FIM do corpo do tooltip, na ordem do texto de origem, com UMA linha em branco antes — e a linha azul
do nivel 3 (auras ativas / skills no status) e sempre a ULTIMA.*

Havia DOIS blocos de nivel 3, e a regra so alcancava UM:

  * `Your active shrine auras: ...` — escrito pelo `ShrineAuraPatch` (dentro do `Localize`), achado
    pelo prefixo `CorEOrdemDoTooltip` e devolvido por ultimo;
  * `Your skills on this status: ...` — escrito pelo `StatusSkillSynergyPatch` num gancho
    DIFERENTE (o postfix de `Tooltip.ApplyDescriptionExpressions`, que roda ANTES do `ShowTooltip`) e
    que o prefixo NAO recolhia: o `_conteudosDeNota` o exclui de proposito (`EhBlocoDoNivel3`) e a
    extracao da aura exige o marcador `Your active shrine auras`. Ele ficava onde o motor o deixou.

CONSEQUENCIA (o defeito, hoje LATENTE): numa tooltip que tenha NOTA e a linha de sinergia, a nota e
remanejada para o fim e fica DEPOIS da linha azul — a linha azul deixa de ser a ultima. Hoje so
`Chilled` (status.csv:71) e `Poisoned` (status.csv:336) geram o bloco, e NENHUM dos dois recebe nota:
por isso o defeito nao aparece na tela, e e exatamente por isso que faltava teste.

A DECISAO (NIV3-1, 01/10)
-------------------------
**(a) O bloco de sinergia passa a ser tratado como os outros.** Ele e nivel 3; o §1 do documento ja o
classifica assim (linha 3(b), o caso do Frost Bite/CHL-1). Manter duas regras de ordem no MESMO nivel
seria enshrinar a excecao; a regra passa a valer em todos os caminhos: nivel 3 vai para o FIM, depois
das notas, e a linha de auras (quando existe) continua por ULTIMO.

O MATERIAL E REAL, MENOS UM PEDACO — e o pedaco que falta e o DEFEITO
--------------------------------------------------------------------
A descricao do status vem do censo (`docs/cobertura/status.csv`, o texto do asset), o bloco de
sinergia tem a forma que o `StatusSkillSynergyPatch.Bloco` escreve (marcador + itens + ponto, no azul
da paleta) e a nota e uma nota REAL das tabelas (a primeira entrada de `TextAppends`, em ordem de
arquivo — a mesma regra de escolha do `caso_skill`). O que o material COMPOE e aquilo que hoje NAO
existe: `Chilled`/`Poisoned` + uma nota. E essa composicao que o defeito latente exige, e ela esta
declarada aqui para ninguem achar que o status tem nota hoje.

NAO e um teste: nao tem META nem corpo(). Quem le sao `testes/puros/t_nivel3_sinergia.py` e a
contra-prova (`contra-prova/cp_nivel3_sinergia_isca.py` / `..._ok.py`).
"""
import csv
import os
import re
import sys

import arcabouco as arc
import regras_cor as reg
import regras_formato as fmt

sys.path.insert(0, os.path.join(arc.raiz_do_repo(), "tools"))
import tabelas  # noqa: E402  o parser UNICO das tabelas do LocalizePatch.cs (PARSER-1)

NL = chr(10)
BS = chr(92)

# A cauda do PROPRIO jogo no tooltip de status: `ShowActionStatusTooltip` cola
# `\n\n` + "Duration Type: ..." DEPOIS do `ApplyDescriptionExpressions` (decompilado l.334370).
# Onde o tooltip de SKILL usa `AP Cost`/`Range` unidos por UMA quebra, o de status usa esta linha —
# e a linha em branco dela e DO JOGO, nao nossa (por isso ela e o unico `\n\n` que o checador de
# formato desta familia aceita sem bloco nosso depois).
CAUDA_DO_JOGO = "Duration Type: Normal"
SEGUIDORES_DO_JOGO = (CAUDA_DO_JOGO,)

# O status do censo cuja descricao e o nivel 1 do material (os DOIS produtores do bloco hoje).
STATUS_POR_CASO = (
    ("Chilled", "Frostbite I +2% damage per stack."),
    ("Poisoned", "Contagion +1 Contagion Level."),
)

CAMINHO_STATUS = os.path.join("docs", "cobertura", "status.csv")

# O motivo que a contra-prova cita quando o desenho SEM a correcao quebra o formato.
MOTIVO_DO_DEFEITO = ("a linha azul do nivel 3 (sinergia) deixa de ser a ULTIMA coisa do tooltip: "
                     "a NOTA e devolvida pelo prefixo DEPOIS dela")

REGRAS = ("com-sinergia", "sem-sinergia")


# ------------------------------------------------------------------ fontes ---

def _fonte(nome_arquivo):
    with open(os.path.join(os.path.dirname(reg.FONTE_MOD), nome_arquivo), encoding="utf-8") as fh:
        return fh.read()


def marcador_da_sinergia():
    """O marcador de texto do bloco de sinergia, LIDO do fonte (`StatusSkillSynergyPatch.Marcador`).

    Sai do codigo, nao de um literal do teste: se o marcador mudar, a bancada acompanha — e o
    documento (§1/§3) e quem diz qual e o certo.
    """
    m = re.search(r'internal\s+const\s+string\s+Marcador\s*=\s*"([^"]+)"', _fonte("StatusSkillSynergyPatch.cs"))
    if not m:
        raise arc.Falhou("nao achei `StatusSkillSynergyPatch.Marcador` no fonte do patch")
    return m.group(1)


def marcador_da_aura():
    """O marcador de texto da linha de auras, lido do `ShrineAuraPatch.cs`."""
    return reg.marcadores_do_nivel_3()[0]


# ---------------------------------------------------------------- material ---

def descricao_do_status(nome):
    """A descricao REAL do status, do censo (`docs/cobertura/status.csv`) — o nivel 1 do material.

    A descricao do censo tem os espacos duplos do asset; o postfix do `Localize` normaliza
    `'  '` -> `' '` DEPOIS das tabelas (LocalizePatch.cs, a normalizacao do RV-8b-2) — a mesma
    normalizacao e aplicada aqui para o material chegar ao prefixo como o jogo o entrega.
    """
    caminho = os.path.join(arc.raiz_do_repo(), CAMINHO_STATUS)
    with open(caminho, encoding="utf-8-sig") as fh:
        for linha in csv.DictReader(fh):
            if linha["nome"] == nome:
                texto = linha["descricao"]
                while "  " in texto:
                    texto = texto.replace("  ", " ")
                return texto
    raise arc.Falhou("o status %r nao esta no censo %s" % (nome, CAMINHO_STATUS))


def _miolo_do_bloco(valor):
    """O CONTEUDO de um bloco do marcador lido das tabelas: `\\n<color=#C8B090>TEXTO</color>` -> TEXTO.

    O parser unico devolve o valor JA DESESCAPADO (a quebra e um `\\n` de verdade) — a mesma
    convencao que o `regras_formato._miolo` usa.
    """
    texto = valor.strip(NL)
    abre = "<color=" + reg.entrada_marcador() + ">"
    if not texto.startswith(abre):
        return texto
    return texto[len(abre):texto.rindex(reg.FECHA_COR)]


def primeira_nota_real():
    """(chave, valor) da PRIMEIRA entrada de `TextAppends` cujo valor e UM bloco do marcador.

    Regra de escolha DETERMINISTA (a mesma do `caso_skill`, que usa `pares_de_skill_com_dano()[0]`):
    a primeira em ordem de arquivo — nada escolhido a dedo. A nota e REAL; o que e composto e o par
    (status sem nota de hoje) x (nota).
    """
    abre = "<color=" + reg.entrada_marcador() + ">"
    for chave, valor in tabelas.pares(reg.fonte_do_mod(), "TextAppends"):
        texto = valor.strip(NL)
        if not texto.startswith(abre):
            continue
        if texto.count(abre) != 1 or NL in texto[len(abre):].rstrip(NL):
            continue
        return chave, valor
    raise arc.Falhou("nenhuma entrada de `TextAppends` com UM bloco do marcador (material vazio)")


def bloco_de_sinergia(item):
    """O bloco EXATO que o `StatusSkillSynergyPatch.Bloco` escreve: marcador + itens, no azul da
    paleta resolvido por `LocalizePatch.CorDaLinhaDeAuras()`.

    O conteudo dos itens nao e o que esta bancada mede (quem o calcula e o motor, no jogo); o que ela
    mede e o BLOCO: marcador, cor e posicao.
    """
    return "<color=" + reg.cor_da_linha_azul() + ">" + marcador_da_sinergia() + " " + item + "</color>"


def monta_o_caso(nome_do_status, item_da_sinergia, nota, dano=None, expressoes=(), cauda=CAUDA_DO_JOGO):
    """O caminho REAL ate o texto que o `ShowTooltip` entrega ao prefixo, para o tooltip de STATUS:

      1. `OptionsManager.Localize(descricao)` — e o postfix das NOTAS anexa a nota com o marcador e
         resolve a cor do nivel 2 (`com_a_cor_do_jogo`, que REGISTRA o conteudo dos blocos);
      2. o MOTOR resolve `*N` (dano) e `[N]` (expressao), os dois em `<color=#CBB396>`;
      3. o postfix do `StatusSkillSynergyPatch` anexa o bloco de sinergia com UMA quebra CRUA
         (nao com a linha em branco do `AnexarNota` — era o segundo defeito do caminho);
      4. o `ShowActionStatusTooltip` cola a cauda do jogo (`\\n\\n` + `Duration Type: ...`).

    Devolve (texto que chega ao prefixo, registro das notas do mod).
    """
    texto = descricao_do_status(nome_do_status)
    texto = reg.anexa_nota(texto, nota)
    registro = set()
    texto = reg.com_a_cor_do_jogo(texto, reg.cor_do_nivel_2(), registro)
    if dano is not None:
        texto = reg.dano_do_motor(texto, dano)
    for indice, valor in expressoes:
        texto = substitui_expressao(texto, indice, valor)
    if item_da_sinergia:
        texto = texto + NL + bloco_de_sinergia(item_da_sinergia)
    if cauda:
        texto = texto.rstrip(NL) + NL * 2 + cauda
    return texto, registro


def substitui_expressao(texto, indice, valor):
    """`ApplyDescriptionExpressions` (l.334360 do decompilado): `[N]` -> `<color=#CBB396>VALOR</color>`."""
    return texto.replace("[" + str(indice) + "]",
                         reg.ABRE_COR + reg.COR_DO_VALOR_DO_MOTOR + ">" + str(valor) + reg.FECHA_COR)


# ------------------------------------------------------------------ a regra ---

def tira_o_bloco_da_sinergia(texto, inteira=True):
    """O `TirarBloco(ref description, corAura, mesmaCor, StatusSkillSynergyPatch.Marcador, out sinergia)`
    acrescentado pelo NIV3-1: o bloco do nivel 3 e achado pelo MARCADOR DE TEXTO dele (nunca pela
    cor, §8.3) entre os blocos da cor azul da paleta — o mesmo `exigir` que a linha de auras ja usava.
    Devolve (texto sem o bloco, bloco).
    """
    abre = reg.ABRE_COR + reg.cor_da_linha_azul() + ">"
    i = texto.find(abre)
    while i >= 0:
        _conteudo_ini, fim, conteudo = reg._bloco_em(texto, i)
        if marcador_da_sinergia() in conteudo:
            ini = reg._inicio_do_separador(texto, i, inteira)
            bloco = texto[ini:fim].strip(NL).rstrip()
            return texto[:ini] + texto[fim:], bloco
        i = texto.find(abre, fim)
    return texto, None


def aplica_o_prefixo(texto, registro, com_sinergia=True, inteira=True):
    """O `CorEOrdemDoTooltip.Prefix` INTEIRO, na ordem do codigo do NIV3-1.

    `com_sinergia=True` e a regra de HOJE (depois da correcao): a sinergia e recolhida pelo marcador,
    a linha de auras logo depois, as notas pelo conteudo, e tudo volta no fim — as NOTAS na ordem em
    que aparecem, depois a CAUDA DO NIVEL 3 (a sinergia na frente e a linha de auras por ULTIMO).

    `com_sinergia=False` e o desenho ANTES da correcao (o que produzia o defeito): a sinergia NAO e
    recolhida — fica onde o `ApplyDescriptionExpressions` a deixou — e a nota e devolvida pelo fim,
    DEPOIS dela.
    """
    corpo = texto
    sinergia = None
    if com_sinergia:
        corpo, sinergia = tira_o_bloco_da_sinergia(corpo, inteira)
    corpo, aura = reg.tira_o_bloco_da_aura(corpo, inteira)
    corpo, notas = reg.tira_as_notas_do_mod(corpo, registro, inteira)
    for bloco in notas:
        corpo = reg.monta_a_posicao(corpo, bloco)
    cauda = [b for b in (sinergia, aura) if b]
    if cauda:
        corpo = reg.monta_a_posicao(corpo, (NL + NL).join(cauda))
    return corpo


# --------------------------------------------------------------- checadores ---

def defeitos_de_linha_em_branco(corpo, seguidores_do_jogo=SEGUIDORES_DO_JOGO):
    """O `regras_formato.defeitos_de_linha_em_branco` + a UNICA excecao da familia de status: o
    `\\n\\n` que o PROPRIO jogo escreve antes da cauda dele (`Duration Type: ...`, l.334370) nao e
    uma linha em branco nossa. Fora dessa, a regra e a mesma: nenhuma linha em branco solta e nada
    de quebra no fim.
    """
    defeitos = []
    if corpo != corpo.rstrip():
        defeitos.append("o tooltip termina com quebra / linha em branco: %r" % corpo[-26:])
    if NL * 3 in corpo:
        defeitos.append("DUAS linhas em branco seguidas (o defeito do RV-17(a))")
    aberturas = fmt.aberturas_de_bloco()
    i = 0
    while True:
        j = corpo.find(NL + NL, i)
        if j < 0:
            break
        depois = corpo[j + 2:]
        if not depois.startswith(aberturas) and not depois.startswith(seguidores_do_jogo):
            defeitos.append("linha em branco ORFA (nao separa nenhum bloco nosso): %r"
                            % corpo[max(0, j - 30):j + 30])
        i = j + 2
    return defeitos


def defeitos_da_cauda_do_nivel3(corpo, marcador):
    """A promessa do §9.1 em UMA linha: depois do bloco do nivel 3 NAO PODE HAVER NADA.

    O `regras_formato.defeitos_da_ordem` so cobra "depois das notas"; este cobra o "sempre a ultima"
    (o bloco que ficou antes da cauda do jogo passaria por ele).
    """
    i = corpo.find(marcador)
    if i < 0:
        return ["a linha azul do nivel 3 (%r) sumiu do tooltip" % marcador[:48]]
    fim = corpo.find(reg.FECHA_COR, i)
    if fim < 0:
        return ["a linha azul do nivel 3 (%r) nao fecha o bloco" % marcador[:48]]
    resto = corpo[fim + len(reg.FECHA_COR):].strip()
    if resto:
        return ["a linha azul do nivel 3 NAO e a ultima coisa do tooltip (sobrou %r)" % resto[:60]]
    return []


def defeitos(corpo, notas, marcador, custos=SEGUIDORES_DO_JOGO):
    """Os tres angulos de uma vez: a linha em branco, a ordem (nota depois dos custos, nivel 3 depois
    das notas) e a cauda (nivel 3 por ultimo de fato)."""
    return (defeitos_de_linha_em_branco(corpo)
            + fmt.defeitos_da_ordem(corpo, notas, marcador, custos)
            + defeitos_da_cauda_do_nivel3(corpo, marcador))


# ------------------------------------------------------------------- casos ---

def casos():
    """Os DOIS produtores reais do bloco hoje, com a nota real das tabelas no meio."""
    _chave, nota = primeira_nota_real()
    feitos = []
    for status, item in STATUS_POR_CASO:
        expressoes = ((0, "5"), (1, "12")) if status == "Poisoned" else ()
        texto, registro = monta_o_caso(status, item, nota, expressoes=expressoes)
        feitos.append({
            "rotulo": status,
            "texto": texto,
            "registro": registro,
            "notas": [_miolo_do_bloco(nota)],
            "marcador": marcador_da_sinergia(),
        })
    return feitos


def casos_quebrados(com_sinergia):
    """`[(rotulo, [defeitos])]` dos casos em que o formato NAO fecha com essa regra."""
    quebrados = []
    for caso in casos():
        depois = aplica_o_prefixo(caso["texto"], caso["registro"], com_sinergia=com_sinergia)
        d = defeitos(depois, caso["notas"], caso["marcador"])
        if d:
            quebrados.append((caso["rotulo"], d))
    return quebrados


def antes_e_depois(caso):
    """(texto ANTES da correcao, texto DEPOIS) do mesmo caso — o material do relato."""
    return (aplica_o_prefixo(caso["texto"], caso["registro"], com_sinergia=False),
            aplica_o_prefixo(caso["texto"], caso["registro"], com_sinergia=True))


def corpo_da_contra_prova(regra, defeitos_esperados):
    """O corpo COMPARTILHADO pela isca e pela metade ok (as duas sao o MESMO teste).

    `defeitos_esperados` e a EXPECTATIVA do desenho: 0 na isca (antes da correcao se acreditava que
    o tooltip saia certo — o defeito nao existia) e 0 na metade ok (a regra de hoje nao quebra nada).
    Como o desenho sem a correcao QUEBRA mesmo, a isca reprova citando `MOTIVO_DO_DEFEITO`; a metade
    ok passa.
    """
    quebrados = casos_quebrados(com_sinergia=(regra == "com-sinergia"))
    if len(quebrados) != defeitos_esperados:
        detalhe = "; ".join("%s -> %s" % (r, d[0]) for r, d in quebrados[:2])
        raise arc.Falhou("%s: a regra '%s' quebrou %d caso(s) (esperado %d) — %s"
                         % (MOTIVO_DO_DEFEITO, regra, len(quebrados), defeitos_esperados, detalhe))
    return ("a regra '%s' fecha o formato nos %d casos de status com nota + sinergia: 0 defeito de "
            "linha em branco, 0 de ordem e a linha azul por ULTIMO" % (regra, len(casos())))
