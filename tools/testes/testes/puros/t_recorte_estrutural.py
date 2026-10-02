#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FORMATO-3 — o recorte de fonte E ESTRUTURAL, e isso e provado NOS DOIS SENTIDOS.

POR QUE ESTE TESTE EXISTE
-------------------------
Quatro pontos de chamada deste repositorio ja recortaram fonte por JANELA DE CARACTERES
(`codigo[i:i + N`) e o padrao se repetiu: a janela existe enquanto o metodo couber nela, entao
uma edicao INOFENSIVA (um log a mais, um local a mais) faz o teste REPROVAR por motivo ALHEIO ao
defeito — e o caminho curto para o verde vira AFROUXAR a janela. O `recorte.py` junta o conserto
numa funcao so (casamento de chaves, literal-aware, falha alta) e este teste a DISSECA:

  1. os PRIMITIVOS sobre fonte sintetico: o recorte do metodo inteiro, o bloco que contem uma
     ancora, o bloco que comeca numa ancora; chave dentro de literal de string/char e de
     comentario nao conta; sem assinatura/abertura/fechamento -> FALHA ALTO (nunca um pedaco);
  2. as DUAS DIRECOES em cada fonte REAL que passou a usa-lo: um RETOQUE INOFENSIVO no ponto
     recortado NAO pode quebrar o recorte, e o DEFEITO REAL continua sendo pego — sempre em
     COPIA EM MEMORIA (monkeypatch / replace sobre o texto), SEM TOCAR no arquivo do repositorio.

O `regras_bf.py` (que ainda recorta o `FontSweep` com uma janela de 900, `sweep2[i_escape:i_escape +
900]` — o ULTIMO recorte por janela vivo do `tools/testes/`) NAO e exercitado aqui: ele esta ocupado
por outra tarefa (FIX-8). O ACHADO fica registrado para aquela rodada, junto do conserto pronto
(`rec.bloco_que_contem(sweep2, i_escape)` em lugar da janela).

FORMATO-4 fechou a varredura: a unica outra janela que sobrou fora das provas era o `[\\s\\S]{0,200}?`
do `t_cor3_posicao.py` (media DISTANCIA entre o registro e a leitura da cor, nao a ordem estrutural) —
migrado para `rec.corpo_do_metodo` + comparacao de indices, com a prova nos dois sentidos no proprio
teste. Os demais recortes deste diretorio ja sao estruturais (`recorte.py`).
"""
import re

import arcabouco as arc
import recorte as rec
import regras_bf as bf
import regras_bf_estilo as bfe
import regras_cor as reg

META = {
    "nome": "recorte-estrutural",
    "categoria": "pura",
    "requer": [],
    "descricao": "FORMATO-3: o recorte de fonte e estrutural (casamento de chaves, literal-aware, "
                 "falha alta) e resiste ao retoque inofensivo sem deixar passar o defeito real",
}


# ------------------------------------------------------------------ 1. PRIMITIVOS ---

# Um metodo sintetico que CARREGA chaves dentro de literal de string e de char, e um `}` de
# comentario — os tres enganam uma contagem ingenua de chaves.
SINTETICO = (
    "// um comentario com chave solta { e outra }\n"
    "class C\n"
    "{\n"
    "    private static void Alvo()\n"
    "    {\n"
    "        string s = \"texto com { e } dentro\";\n"
    "        char abre = '{';\n"
    "        char fecha = '}';\n"
    "        if (x)\n"
    "        {\n"
    "            Fim();\n"
    "        }\n"
    "        return;\n"
    "    }\n"
    "\n"
    "    private static void Outro() { }\n"
    "}\n"
)


def _primitivos():
    # (a) o METODO INTEIRO: do nome ate o `}` que casa, com as chaves dos literais ignoradas.
    corpo = rec.corpo_do_metodo(SINTETICO, "private static void Alvo()")
    arc.exigir(corpo.startswith("private static void Alvo()"),
               "o recorte nao comeca na assinatura: %r" % corpo[:40])
    arc.exigir(corpo.rstrip().endswith("}") and "Fim();" in corpo and "return;" in corpo,
               "o recorte do metodo nao chegou ao fim (chave de literal contou como bloco?): %r"
               % corpo[-40:])
    arc.exigir("private static void Outro()" not in corpo,
               "o recorte passou do fim do metodo (engoliu o metodo seguinte)")

    # (b) o BLOCO que COMECA numa ancora: o ramo do `if`, nao o metodo.
    i_if = SINTETICO.find("if (x)")
    ramo = rec.bloco_apos(SINTETICO, i_if)
    arc.exigir(ramo.startswith("{") and "Fim();" in ramo and "return;" not in ramo,
               "o `bloco_apos` nao devolveu o ramo do `if`: %r" % ramo[:40])

    # (c) o MENOR bloco que CONTEM a ancora: a folha, nao o tronco.
    folha = rec.bloco_que_contem(SINTETICO, SINTETICO.find("Fim();"))
    arc.exigir(folha.count("{") == 1 and "Fim();" in folha and "Alvo" not in folha,
               "o `bloco_que_contem` devolveu o tronco e nao a folha: %r" % folha)

    # (d) o CODIGO EFETIVO: comentario some, mas o `//` DENTRO de um literal fica.
    efetivo = rec.codigo_efetivo('a(); // some { }\nb("// fica");\n/* some { } */c();')
    arc.exigir("some" not in efetivo.split('b("')[0], "o comentario de linha nao foi removido")
    arc.exigir('b("// fica")' in efetivo, "o `//` dentro do literal foi removido (nao era comentario)")
    arc.exigir("c();" in efetivo and "/*" not in efetivo, "o comentario de bloco nao foi removido")

    # (e) FALHA ALTA: sem assinatura, sem `{`, chaves que nao fecham, ancora fora de bloco.
    casos = (
        ("assinatura ausente", lambda: rec.corpo_do_metodo(SINTETICO, "void NaoExiste()")),
        ("assinatura sem corpo", lambda: rec.corpo_do_metodo("void X();\nint y;", "void X()")),
        ("chaves que nao fecham", lambda: rec.corpo_do_metodo("void X() { if (a) { ", "void X()")),
        ("ancora fora de bloco", lambda: rec.bloco_que_contem("int x = 1;", 5)),
    )
    for rotulo, acao in casos:
        try:
            acao()
        except arc.Falhou:
            pass
        else:
            arc.exigir(False, "o recorte NAO falhou alto no caso '%s' — devolveu um pedaco em "
                              "silencio (um recorte vazio 'passa' em toda checagem)" % rotulo)

    # (f) O GUARDA do metodo inteiro: um pedaco de JANELA (que nao fecha nas chaves) REPROVA.
    try:
        rec.exigir_metodo_inteiro(corpo[:len(corpo) // 2], "private static void Alvo()",
                                  ("Fim();",))
    except arc.Falhou as erro:
        arc.exigir("janela" in str(erro) or "fecha" in str(erro),
                   "o guarda reprovou, mas nao pelo motivo da janela: %s" % erro)
    else:
        arc.exigir(False, "o guarda ACEITOU um pedaco de janela — nao trava a volta da janela")
    rec.exigir_metodo_inteiro(corpo, "private static void Alvo()", ("Fim();", "return;"))


# --------------------------------------------------------------- 2. FONTES REAIS ---
# O RETOQUE INOFENSIVO padrao (formula-se uma vez; cada ponto acrescenta o seu). Nao carrega
# nenhum marcador conferido — so ocupa espaco, que e o que a janela nao tolera.
def _retoque(rotulo, tamanho):
    """Um bloco de codigo C# inofensivo com pelo menos `tamanho` caracteres, sem chave solta."""
    linhas, n = [], 0
    while n < tamanho:
        linhas.append('                string _rastro%d = "%s %d";' % (len(linhas), rotulo, n))
        n += len(linhas[-1]) + 1
    return "".join("\n" + linha for linha in linhas)


def _prefixo_do_tooltip():
    """LocalizePatch.cs: o metodo `Prefix` (retoque inofensivo x defeito real)."""
    fonte = rec.codigo_efetivo(reg.fonte_do_mod())
    assinatura = "private static void Prefix(ref string description)"
    marcas = ("description = corpo;", "catch (Exception e)",
              'corpo += "\\n\\n" + aura;')

    # DIREÇÃO 1 — RETOQUE INOFENSIVO (~700 caracteres, mais que a margem de 429 da janela 3800).
    retocado = fonte.replace(assinatura + "\n            {",
                             assinatura + "\n            {" + _retoque("retoque do Prefix", 700), 1)
    arc.exigir(retocado != fonte, "o retoque do `Prefix` nao achou a abertura — nao plantou nada")
    bloco = rec.corpo_do_metodo(retocado, assinatura)
    rec.exigir_metodo_inteiro(bloco, assinatura, marcas)
    i = retocado.find(assinatura)
    arc.exigir(not all(m in retocado[i:i + 3800] for m in marcas),
               "a janela de 3800 aguentou o retoque: a prova perdeu o sentido")

    # DIREÇÃO 2 — DEFEITO REAL: a cauda do nivel 3 perde o separador exato. A contagem REPROVA.
    defeito = fonte.replace('corpo += "\\n\\n" + aura;', "corpo += aura;", 1)
    arc.exigir(defeito != fonte, "o plantio do defeito nao achou a cauda do nivel 3")
    bloco_def = rec.corpo_do_metodo(defeito, assinatura)
    arc.exigir(len(re.findall(r'corpo \+= "\\n\\n"', bloco_def)) != 2,
               "o defeito real do `Prefix` PASSOU pela contagem — a checagem e decoracao")


def _fontes_do_betterfont():
    """BetterFont/Plugin.cs: o ramo do ESCAPE e o `try` do caminho de sucesso do `FontSweep`."""
    src = bf.fonte()
    sweep = bf.corpo(src, "private void FontSweep()")
    arc.exigir(sweep is not None, "nao achei o `FontSweep` — a leitura do BetterFont mudou")

    # (a) O RAMO DO ESCAPE (o `_ramo` que passou a casar chaves pelo recorte.py).
    ramo = bfe._ramo(sweep, "if (estilizado && Plugin.PularEstilizadosLigado)")
    arc.exigir(ramo is not None and "continue" in ramo and "t.font = _serifFont" not in ramo,
               "o `_ramo` nao recortou so o ramo do escape")

    # (b) O `try` DO CAMINHO DE SUCESSO — DIREÇÃO 1: retoque inofensivo de ~1300 caracteres
    #     entre a troca de fonte e as chamadas (mais que a janela de 1200). O bloco estrutural
    #     continua trazendo as TRES chamadas; a janela perderia o `SetVerticesDirty()`.
    i_troca = sweep.find("t.font = _serifFont")
    retocado = sweep.replace("t.font = _serifFont;",
                             "t.font = _serifFont;" + _retoque("retoque do try", 1300), 1)
    arc.exigir(retocado != sweep, "o retoque do `try` nao achou a troca de fonte")
    trecho = rec.bloco_que_contem(retocado, retocado.find("t.font = _serifFont"))
    for esperado in ("CopiarEstilo(", "UpdateMeshPadding()", "SetVerticesDirty()"):
        arc.exigir(esperado in trecho,
                   "o retoque INOFENSIVO derrubou %r do recorte estrutural do `try`" % esperado)
    i_ret = retocado.find("t.font = _serifFont")
    arc.exigir("SetVerticesDirty()" not in retocado[i_ret:i_ret + 1200],
               "a janela de 1200 aguentou o retoque: a prova perdeu o sentido")

    # DIREÇÃO 2 — DEFEITO REAL no MESMO caminho: o padding some. A checagem de `falhas_da_decisao`
    # (que le exatamente este recorte) TEM de reprovar.
    sem_padding = bfe.defeito_sem_padding(src)
    arc.exigir(sem_padding != src, "o plantio da remocao do padding nao achou onde agir")
    arc.exigir(any("padding" in f for f in bfe.falhas_da_decisao(sem_padding)),
               "remover o `UpdateMeshPadding()` do caminho de sucesso PASSOU — a checagem do "
               "recorte nao pega o defeito real")


def _entradas_da_tabela():
    """LocalizePatch.cs: a ENTRADA de `TextFixes` da nota fundida de shrine (o furo do COR-1)."""
    fonte = rec.codigo_efetivo(reg.fonte_do_mod())
    chave = "Recover [0]% of maximum mana each turn."
    # A frase COMPLETA (com o `Base 10%;`): ela ocorre duas vezes (mana e vida) e a PRIMEIRA e a
    # entrada do mana — mutar so `the value shown...` pegaria outra nota, antes desta.
    frase = "Base 10%; the value shown already includes the Shrine Effect Bonus."

    # DIREÇÃO 1 — RETOQUE INOFENSIVO: texto a mais ANTES do `Shrine Effect Bonus`. O bloco
    # estrutural continua trazendo a frase; a janela `i..j+160` perderia a frase INTEIRA (nao so
    # o comeco dela — medido, nao afirmado).
    retocado = fonte.replace(frase, "Base 10%; o valor mostrado ja inclui, com uma explicacao bem "
                                    "mais longa do que a janela fixa alcancava a partir da chave "
                                    "da tabela, o Shrine Effect Bonus.", 1)
    arc.exigir(retocado != fonte, "o retoque da entrada nao achou a frase de shrine")
    i = retocado.index(chave)
    j = retocado.index("<color=#C8B090", i)
    arc.exigir("Shrine Effect Bonus" in rec.bloco_que_contem(retocado, j),
               "o retoque INOFENSIVO derrubou o `Shrine Effect Bonus` do recorte estrutural")
    arc.exigir("Shrine Effect Bonus" not in retocado[i:j + 160],
               "a janela de 160 aguentou o retoque: a prova perdeu o sentido")

    # ...e o CONSUMIDOR (`notas_fundidas_com_cor`, de `regras_cor`) le a entrada inteira: o
    # monkeypatch devolve a copia mutada em memoria, sem tocar no arquivo.
    original = reg.fonte_do_mod
    try:
        reg.fonte_do_mod = lambda: retocado
        uma = [n for n in reg.notas_fundidas_com_cor() if n[0] == 1]
        arc.exigir(any("Shrine Effect Bonus" in n[2] for n in uma),
                   "o consumidor de `regras_cor` perdeu o `Shrine Effect Bonus` com o retoque "
                   "inofensivo — o recorte dele ainda tem margem")
    finally:
        reg.fonte_do_mod = original

    # DIREÇÃO 2 — DEFEITO REAL: a nota deixa de citar o `Shrine Effect Bonus`. O recorte NAO pode
    # trazer a frase (a checagem do `t_trava_cor_notas_fundidas` reprova).
    defeito = fonte[:i] + fonte[i:].replace("Shrine Effect Bonus", "Bonus de santuario", 1)
    jd = defeito.index("<color=#C8B090", defeito.index(chave))
    arc.exigir("Shrine Effect Bonus" not in rec.bloco_que_contem(defeito, jd),
               "o defeito real (nota sem `Shrine Effect Bonus`) PASSOU pelo recorte da entrada")


def corpo():
    _primitivos()
    _prefixo_do_tooltip()
    _fontes_do_betterfont()
    _entradas_da_tabela()
    print("recorte estrutural fechado: metodo inteiro / bloco que contem / bloco que comeca numa "
          "ancora, literal-aware e com FALHA ALTA; nos 3 fontes reais (LocalizePatch.Prefix, "
          "FontSweep do BetterFont, entrada de TextFixes) o retoque inofensivo NAO quebra o "
          "recorte e o defeito real continua sendo pego — tudo em copia em memoria, sem tocar "
          "no arquivo")


if __name__ == "__main__":
    arc.main(META, corpo)
