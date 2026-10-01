#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""COR-3: A POSICAO DO VALOR DE DANO nas tooltips de SKILL (o achado do dono).

O QUE ESTE TESTE PRENDE
-----------------------
O dono relatou, com o build instalado (a Release do BetterTooltips do dia): "os tooltips com dano
que estavam na posicao correta foram movidos para o FUNDO do tooltip". A COR-1 nao tinha
explicacao nenhuma para isso — ela media TEXTO (278 de 281 chaves com zero diferenca de texto
decodificado) e passou. O que move um bloco de lugar nao e o texto: e o ENVOLTORIO + a regra de
POSICAO.

O MECANISMO (medido no artefato que o dono roda, `BetterTooltips/bin/Release/.../BetterTooltips.dll`
de 01/10 14:41 — a build instalada por acidente):

  * `ComACorDoJogo` troca o marcador `#C8B090` das NOSSAS notas pela cor lida no campo
    `Tooltip.specialDescColor` — que vale `#CBB396`;
  * `#CBB396` e o MESMO literal que o motor escreve nos valores dinamicos das skills
    (`ApplyDescriptionExpressions` l.2327: `<color=#CBB396>VALOR</color>` para o `[N]`;
    `GetDamageString` l.2276: `<size=..><color=#CBB396>NN</color></size>` para o `*N` — o DANO);
  * o `CorEOrdemDoTooltip` procurava "o PRIMEIRO bloco da cor do nivel 2" para move-lo ao fundo —
    depois da troca, o primeiro bloco dessa cor numa tooltip com dano e o VALOR DE DANO, nao a nota.

A CORRECAO (COR-3): a NOSSA nota passou a ser achada pelo CONTEUDO (`_conteudosDeNota` /
`TirarNotaDoMod`), nunca pela cor. O que este teste faz:

  1. TRAVA ESTRUTURAL no fonte: o registro por conteudo existe, e o `CorEOrdemDoTooltip` nao tem
     mais a extracao por cor (a linha exata que estava no build do dono);
  2. DEFEITO REPRODUZIDO (a isca, com o material REAL das tabelas do mod): com a regra ANTIGA,
     pelo menos DUAS tooltips de skill com dano mandam o VALOR DE DANO para o fundo — e o mesmo
     acontece com o `[0]` da tooltip de SHRINE (o defeito nunca foi exclusivo das skills);
  3. CORRECAO PROVADA nas mesmas tres: a nota e que vai para o fundo (depois dos custos), o valor
     do motor fica na linha branca onde o jogo o escreveu, e a linha azul do nivel 3 continua por
     ULTIMO.

A prova so vale porque as duas metades rodam sobre o MESMO texto: o da isca e o do conserto saem
do mesmo `monta_a_descricao`, e a unica diferenca e a funcao de extracao (a regra antiga x a do
COR-3).
"""
import re

import arcabouco as arc
import regras_cor as reg

META = {
    "nome": "cor3-posicao",
    "categoria": "pura",
    "requer": [],
    "descricao": "COR-3: a nota do mod e achada pelo CONTEUDO, nao pela cor - o valor de dano do motor fica na linha branca (2 skills + 1 shrine provam as duas metades)",
}

# Os valores que o MOTOR calcularia (a formula nao muda nada aqui: o que importa e que o motor
# escreve o numero dele na MESMA cor do nivel 2). 23 = dano do `*0`; 40 = o `[0]` da dodge da shrine.
DANO_DO_MOTOR = "23"
VALOR_DA_SHRINE = "40"
CUSTOS_DO_JOGO = ("AP Cost: 1", "Range: Melee")
AURA_AZUL = "Your active shrine auras: Dodge +40% (total +57%)."
# A linha de auras entra no texto JA COLORIDA por quem a escreve (`CorDaLinhaDeAuras()`, nivel 3).
AURA_AZUL_COLORIDA = "<color=" + reg.cor_da_linha_azul() + ">" + AURA_AZUL + "</color>"


def _fonte():
    return reg.fonte_do_mod()


def _sem_comentarios(fonte):
    """O codigo sem os comentarios: a bancada CITA o desenho antigo nos comentarios, e citacao nao e
    codigo (mesma regra do `t_cores_niveis`)."""
    return re.sub(r"//[^\n]*", "", fonte)


def _cenario(chave, nota, dano=None, expressao=None, aura=None):
    """Roda as DUAS regras sobre o MESMO texto (e com o MESMO prefixo) e devolve o antes e o depois."""
    texto, registro = reg.monta_a_descricao(chave, nota, dano=dano, expressao=expressao,
                                            custos=CUSTOS_DO_JOGO, aura=aura)
    # A linha de auras (nivel 3) sai primeiro, como no codigo — so depois a nota e procurada.
    sem_aura, _aura = reg.tira_o_bloco_da_aura(texto)
    _resto, movido_antigo = reg.tira_o_primeiro_bloco_da_cor(sem_aura, reg.cor_do_nivel_2())
    _resto2, movido_novo = reg.tira_a_nota_do_mod(sem_aura, registro)
    return {
        "texto": texto,
        "antigo_movido": movido_antigo,
        "antigo_fim": reg.aplica_o_prefixo(texto, registro, regra_antiga=True),
        "novo_movido": movido_novo,
        "novo_fim": reg.aplica_o_prefixo(texto, registro, regra_antiga=False),
    }


def _miolo(nota):
    """O TEXTO da nota (sem as quebras da frente e sem as tags de cor): e ele que identifica a nota,
    do mesmo jeito que o `_conteudosDeNota` guarda o conteudo."""
    t = nota.strip(chr(10))
    if t.startswith("<color=#"):
        t = t[t.index(">") + 1:]
    if t.endswith("</color>"):
        t = t[:-len("</color>")]
    return t


def _bloco_do_motor(valor):
    return "<color=" + reg.COR_DO_VALOR_DO_MOTOR + ">" + valor + "</color>"


def corpo():
    fonte = _fonte()
    codigo = _sem_comentarios(fonte)

    # --------------------------------------------------- 1. TRAVA ESTRUTURAL no fonte
    arc.exigir(re.search(r"private\s+static\s+readonly\s+HashSet<string>\s+_conteudosDeNota\s*=", fonte),
               "o registro `_conteudosDeNota` (a identidade das NOSSAS notas) sumiu do LocalizePatch.cs")
    arc.exigir(re.search(r"private\s+static\s+void\s+RegistrarBlocosDeNota\s*\(", fonte),
               "o `RegistrarBlocosDeNota` (quem alimenta o registro) sumiu do LocalizePatch.cs")
    arc.exigir(re.search(r"RegistrarBlocosDeNota\(texto\);\s*\n[\s\S]{0,200}?_corEspecialDoJogo\s*==\s*null",
                         fonte),
               "o registro tem de acontecer DENTRO do `ComACorDoJogo` e ANTES da leitura/troca da cor "
               "(senao a nota nao esta registrada quando a cor e resolvida)")
    arc.exigir(re.search(r"bool\s+achouNota\s*=\s*TirarNotaDoMod\(ref\s+description,\s*out\s+nota\);", codigo),
               "o `CorEOrdemDoTooltip` tem de achar a nota pelo CONTEUDO (`TirarNotaDoMod`)")
    arc.exigir(not re.search(r"TirarBloco\(ref\s+description,\s*corNota,\s*false,\s*null,\s*out\s+nota\)", codigo),
               "a extracao por COR voltou ao `CorEOrdemDoTooltip`: `TirarBloco(ref description, corNota, "
               "false, null, out nota)` e exatamente a linha do build em que o valor de dano ia para o fundo")

    # --------------------------------------------------- 2. O MATERIAL (real)
    pares = reg.pares_de_skill_com_dano()
    arc.exigir(len(pares) >= 2,
               "preciso de pelo menos DUAS tooltips de SKILL com dano + nota nas tabelas do mod; achei %d"
               % len(pares))
    chave_shrine, nota_shrine = reg.par_de_shrine()

    # Duas tooltips de skill com DANO e notas DIFERENTES (o material e o das tabelas; so evito
    # provar duas vezes a mesma nota).
    escolhidos = []
    for chave, nota in pares:
        if any(_miolo(nota) == _miolo(n) for _c, n in escolhidos):
            continue
        escolhidos.append((chave, nota))
        if len(escolhidos) == 2:
            break

    provas = []
    for chave, nota in escolhidos:
        c = _cenario(chave, nota, dano=DANO_DO_MOTOR)
        rotulo = chave[:58]
        miolo = _miolo(nota)

        # 2a. a ISCA: com a regra antiga, o bloco que vai para o fundo e o VALOR DO MOTOR...
        arc.igual(reg.COR_DO_VALOR_DO_MOTOR in (c["antigo_movido"] or ""), True,
                  "DEFEITO nao reproduzido em '%s': a regra antiga tinha de mover o bloco do VALOR "
                  "(%s); ela moveu %r"
                  % (rotulo, reg.COR_DO_VALOR_DO_MOTOR, c["antigo_movido"]))
        arc.exigir(DANO_DO_MOTOR in c["antigo_movido"],
                   "DEFEITO nao reproduzido em '%s': o bloco movido tinha de ser o dano %s do motor; "
                   "foi %r" % (rotulo, DANO_DO_MOTOR, c["antigo_movido"]))
        # ...e nao a nota.
        arc.exigir(miolo[:30] not in c["antigo_movido"],
                   "DEFEITO nao reproduzido em '%s': a regra antiga NAO podia mover a nota; moveu %r"
                   % (rotulo, c["antigo_movido"]))
        arc.exigir(c["antigo_fim"].rstrip().endswith(DANO_DO_MOTOR + reg.FECHA_COR),
                   "DEFEITO nao reproduzido em '%s': o valor de dano tinha de terminar no FUNDO; fim: %r"
                   % (rotulo, c["antigo_fim"][-120:]))

        # 2b. o CONSERTO: a nota e que vai para o fundo, e o valor fica na linha branca.
        arc.exigir(c["novo_movido"] is not None and miolo[:30] in c["novo_movido"],
                   "'%s': o COR-3 tem de mover a NOTA; moveu %r" % (rotulo, c["novo_movido"]))
        arc.exigir(c["novo_movido"].strip() != _bloco_do_motor(DANO_DO_MOTOR),
                   "'%s': o bloco movido nao pode ser o VALOR do motor (%r)"
                   % (rotulo, c["novo_movido"]))
        arc.exigir(_bloco_do_motor(DANO_DO_MOTOR) in c["novo_fim"],
                   "'%s': o dano do motor tem de continuar no texto (nao pode sumir); texto: %r"
                   % (rotulo, c["novo_fim"]))
        arc.exigir(c["novo_fim"].index(_bloco_do_motor(DANO_DO_MOTOR)) < c["novo_fim"].index(miolo[:30]),
                   "'%s': o dano tem de ficar NA LINHA BRANCA, antes da nota (que vai para o fundo); "
                   "texto: %r" % (rotulo, c["novo_fim"]))
        arc.exigir(c["novo_fim"].rstrip().endswith(miolo.rstrip() + reg.FECHA_COR),
                   "'%s': a nota tem de terminar o tooltip (depois dos custos); fim: %r"
                   % (rotulo, c["novo_fim"][-140:]))
        provas.append((rotulo, c))

    # --------------------------------------------------- 3. A SHRINE (mesma leitura)
    c = _cenario(chave_shrine, nota_shrine, expressao=VALOR_DA_SHRINE, aura=AURA_AZUL_COLORIDA)
    # 3a. a ISCA na shrine: o `[0]` da linha branca TAMBEM ia para o fundo (o defeito nunca foi
    #     exclusivo das skills — o que o dono pediu as shrines foi o padrao da NOTA, nao isto).
    arc.exigir(VALOR_DA_SHRINE in (c["antigo_movido"] or ""),
               "na shrine, a regra antiga tinha de mover o `[0]` do motor (%s); moveu %r"
               % (VALOR_DA_SHRINE, c["antigo_movido"]))
    # 3b. o CONSERTO na shrine: a nota (uma das 12 enxugadas pelo dono) e que vai para o fundo, o
    #     valor fica na linha branca e a LINHA AZUL do nivel 3 continua por ultimo.
    arc.exigir(c["novo_movido"] is not None and "Shrine Effect Bonus" in c["novo_movido"],
               "na shrine, o COR-3 tem de mover a nota do nivel 2; moveu %r" % (c["novo_movido"],))
    arc.exigir(_bloco_do_motor(VALOR_DA_SHRINE) in c["novo_fim"],
               "na shrine, o valor %s do motor tem de continuar na linha branca; texto: %r"
               % (VALOR_DA_SHRINE, c["novo_fim"]))
    arc.exigir(c["novo_fim"].rstrip().endswith(AURA_AZUL + reg.FECHA_COR),
               "na shrine, a linha de auras ativas (nivel 3) tem de continuar por ULTIMO; fim: %r"
               % (c["novo_fim"][-160:],))
    arc.exigir(c["novo_fim"].index("Shrine Effect Bonus") < c["novo_fim"].index(AURA_AZUL),
               "na shrine, a ordem de leitura tem de ser nota (2) e depois a linha azul (3)")

    # --------------------------------------------------- saida (a prova, legivel)
    for rotulo, c in provas:
        print("skill: %s" % rotulo)
        print("   ANTES  (regra da cor): ...%s" % c["antigo_fim"][-70:].replace(chr(10), " / "))
        print("   DEPOIS (COR-3):        ...%s" % c["novo_fim"][-90:].replace(chr(10), " / "))
    print("shrine: a nota '%s...' vai para o fundo e a linha azul continua por ultimo"
          % _miolo(nota_shrine)[:56])
    print("o valor do motor (%s) fica na linha branca nas TRES tooltips; as tabelas conferidas sao as reais"
          % _bloco_do_motor(DANO_DO_MOTOR))


if __name__ == "__main__":
    arc.main(META, corpo)
