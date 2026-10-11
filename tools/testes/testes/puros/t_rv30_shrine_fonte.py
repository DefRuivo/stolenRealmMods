#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RV-30 (03/10) — A FONTE DO BONUS NA LINHA DE SHRINE (o defeito do numero DOBRADO).

O DEFEITO
---------
Personagens SEM os buffs de shrine apareciam como se tivessem o bonus (`worship`) e o valor da
aura saia DOBRADO. A causa NAO era conta a mais na linha: o prefix `FixShrineExpressionParams`
(RV-34) TROCAVA o `Source` vazio do hover do shrine pelo receptor, e as duas auras de PERIGO
(Decay/Flame) — que leem `Source["ShrineEffectBonus"]` — passavam a carregar o bonus do JOGADOR,
que elas NAO usam.

O QUE O MOTOR FAZ (decompilado do build atual, nao leitura de prosa)
--------------------------------------------------------------------
* `Character.CalculateAttributeWalkOnce` avalia a expressao de cada status com
  `GameFunctionParameters { Source = actionStatus3.Source, Target = actionStatus3.Target }`
  (l.37225-37226 do `Assembly-CSharp.decompiled.cs`);
* um status de ground effect (shrine) nasce em
  `GroundEffect.AddGroundEffectedPlayer -> GameLogic.CreateActionStatus(Source, player, ...)`
  (l.116868/l.116924) com `Source` = o personagem do PROPRIO SHRINE;
* as 9 auras de BUFF leem `Target["ShrineEffectBonus"]` (o bonus e de QUEM RECEBE a aura) e as
  DUAS de perigo (Decay/Flame) leem `Source["ShrineEffectBonus"]` (o bonus e do SHRINE);
* nao existe fonte de bonus chamada `Worship` no build: `grep -ic worship` no decompilado = 0;
  o unico rastro e o `CharacterInfo` de INIMIGO `T2_Worshiper` — o RV-34 antigo atribuia ao
  JOGADOR um perk que nao existe, e a leitura "o dano dobra com Worship" era fabricacao.
* as formulas COMPILADAS do jogo confirmam as duas pontas (`CompiledExpressions`,
  l.66061/66100 = buff, `Mathf.Round(20 * (1 + (Target["ShrineEffectBonus"] / 100)))`;
  l.87116/87118 = Decay, `... * (1 + (Source["ShrineEffectBonus"] / 100))`).

O CONSERTO QUE ESTE TESTE TRAVA
-------------------------------
  1. o prefix NAO escreve em `gameFunctionParameters.Source` (so preenche o `Target` vazio) — o
     parametro era o posicional `__2` ate a auditoria t_b62183cc (06/10), que o trocou pelo NOME do
     original (`ref GameFunctionParameters gameFunctionParameters`);
  2. as QUATRO avaliacoes de perigo (`FraseAlvosDoFlame`, `LinhaDecayComValor` e as duas de
     `ItemDaAuraSemAtributo`) usam a constante SEM o fator (`...SemBonus`) com `Source` = null;
  3. as 9 auras de BUFF continuam avaliadas com o receptor nos DOIS slots
     (`ContribuicaoDasAuras`: `ValorDaExpressao(efeito.Amount, receptor, receptor, ...)`) —
     a ponta que o motor usa e a que o mod sempre acertou.

REGRA DE OURO DESSE TESTE: a checagem tem de MORDER. Cada exigencia e provada com o trecho do
defeito classico (o RV-34) passando por ela e sendo ACUSADO — checagem que nunca foi vista
reprovando seria decoracao. O detalhe que quase passou: `gameFunctionParameters.Source == null` na
mensagem de LOG e LEITURA, nao escrita, e nao pode ser confundida com o defeito.

LIMITE. Nao executa o C# do mod (pediria a `lib/` do jogo e um harness): a ligacao com o motor e o
RECORTE do fonte vivo (`recorte.py`) e a regra transcrita em `regras_rv30.py`, citando o
decompilado. Quem fecha o numero na TELA e o dono, com o `tools/checa_shrines.py` lendo o log.
"""
import io
import os

import arcabouco as arc
import recorte as rec
import regras_rv30 as reg

META = {
    "nome": "rv30-shrine-fonte",
    "categoria": "pura",
    "requer": [],
    "descricao": "RV-30: o bonus do ShrineEffectBonus NAO entra nas duas auras de PERIGO — o fonte "
                 "nao escreve em `gameFunctionParameters.Source`, as 4 avaliacoes de Decay/Flame usam a constante SEM "
                 "fator com `Source` = null, e as 9 de BUFF continuam com o receptor (o motor le "
                 "`Target[...]`)",
}

ARQUIVO = os.path.join("BetterTooltips", "Patches", "ShrineAuraPatch.cs")

# O trecho do DEFEITO classico (RV-34): o prefix escrevia no `Source` e a formula de perigo ia COM
# o fator do jogador. Usado para PROVAR que `violacoes` nao e vazia.
TRECHO_DEFEITO = (
    "                if (fonteVazia || fonteEhMundoDoShrine)\n"
    "                {\n"
    "                    gameFunctionParameters.Source = receptor;\n"
    "                }\n"
    "                float dano;\n"
    "                if (!ValorDaExpressao(FormulaDoDano(FormulaDanoDecay, FormulaDanoDecaySemBonus),"
    " naAura, naAura, out dano))\n"
    "                {\n"
    "                    return null;\n"
    "                }\n"
)


def _codigo():
    caminho = os.path.join(arc.raiz_do_repo(), ARQUIVO)
    with io.open(caminho, encoding="utf-8") as fh:
        return rec.codigo_efetivo(fh.read())


def corpo():
    codigo = _codigo()

    # ---------------------------------------------------------------- 1. o fonte VIVO
    falhas = reg.violacoes(codigo)
    arc.exigir(not falhas, "a regra do RV-30 acusa o fonte VIVO: " + "; ".join(falhas))

    # ---------------------------------------------------- 2. a checagem MORDE (o defeito)
    fd = reg.violacoes(TRECHO_DEFEITO)
    arc.exigir(any("gameFunctionParameters.Source" in f for f in fd),
               "a regra NAO acusa o prefix escrevendo em `gameFunctionParameters.Source` — a checagem ficou vazia")
    arc.exigir(any("FormulaDoDano(" in f for f in fd),
               "a regra NAO acusa a formula de perigo avaliada COM o fator (`FormulaDoDano(`)")

    # ------------------------------------------ 3. LEITURA de log x ESCRITA (o quase-furo)
    arc.exigir(not reg._PREFIX_ESCREVE_SOURCE.search('x = (gameFunctionParameters.Source == null ? 1 : 2);'),
               "a regra confunde a LEITURA `gameFunctionParameters.Source == null` do log com a ESCRITA do defeito")

    # ------------------------------------------- 4. as 4 avaliacoes de perigo e o BUFF
    perigo = reg._AVALIACAO_PERIGO.findall(codigo)
    arc.igual(len(perigo), 4,
              "eram para ser 4 avaliacoes de perigo (FraseAlvosDoFlame, LinhaDecayComValor, "
              "ItemDaAuraSemAtributo x2) com a constante SEM fator e `Source` = null")
    arc.exigir(reg._BUFF_COM_RECEPTOR.search(codigo) is not None,
               "o caminho das 9 auras de BUFF mudou: `ContribuicaoDasAuras` tem de avaliar "
               "`efeito.Amount` com o receptor nos dois slots (`Target[...]` = quem RECEBE)")

    print("conforme: prefix sem escrita no Source; 4 avaliacoes de perigo sem fator; "
          "BUFF com o receptor nos dois slots")


if __name__ == "__main__":
    arc.main(META, corpo)
