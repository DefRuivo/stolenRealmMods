#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rv30.py - a REGRA do RV-30 lida no FONTE do `ShrineAuraPatch.cs` (familia TST-2).

O DEFEITO (relato do dono, 30/09; investigacao fechada em 03/10)
-----------------------------------------------------------------
`personagens que NAO tem os buffs de shrine aparecem como se tivessem 'worship', e o valor
recebido pela aura do shrine esta INDEVIDAMENTE DOBRADO`.

RAIZ (provada no decompilado do build atual, nao em leitura de prosa):

  * o motor avalia o `AttributeEffects.Amount` de cada status com
    `GameFunctionParameters { Source = actionStatus3.Source, Target = actionStatus3.Target }`
    (`Character.CalculateAttributeWalkOnce`, ramo de `ActionStatuses`);
  * um status de ground effect (shrine) nasce em
    `GroundEffect.AddGroundEffectedPlayer -> GameLogic.CreateActionStatus(Source, player, ...)`,
    com `Source` = `GroundEffect.Source` (`ConvertToGroundEffect`), ou seja o personagem do
    PROPRIO SHRINE;
  * as 9 auras de BUFF leem `Target["ShrineEffectBonus"]` -> o bonus e o de QUEM RECEBE a aura
    (o personagem em foco) — o mod sempre acertou essa ponta;
  * as DUAS auras de PERIGO (`Decay Shrine Aura`, `Flame Shrine Aura`) leem
    `Source["ShrineEffectBonus"]` — o bonus e o do SHRINE, NAO o do personagem.

O defeito estava no RV-34: o prefix `FixShrineExpressionParams` passou a TROCAR o `Source` vazio
do hover do shrine pelo receptor, e as formulas do Flame/Decay passaram a ser avaliadas com
`Source = Target = pessoa na aura`. Isso injeta o `ShrineEffectBonus` do JOGADOR numa conta que
nao o usa — o numero sai "como se o personagem tivesse um bonus" (o `worship` do relato) — e o
`worship` de verdade e outra coisa: a habilidade `Worship` ("100% increased effect from Shrines",
valor 100) do CharacterInfo `T2_Worshiper`, um INIMIGO (`resources.assets@1519682296`), NAO um
perk do jogador. O RV-30 antigo afirmava o perk do jogador — FABRICACAO.

O QUE ESTA REGRA COBRA NO FONTE
-------------------------------
  1. `FixShrineExpressionParams` NAO escreve em `gameFunctionParameters.Source` (so preenche o `Target`
     vazio; auditoria t_b62183cc, 06/10: o parametro deixou de ser o posicional `__2` e passou a ser
     lido pelo NOME do original — a regra acompanha o nome novo);
  2. nenhuma avaliacao de formula de perigo passa o receptor no slot `gameSource`: as 4
     (`FraseAlvosDoFlame`, `LinhaDecayComValor`, `ItemDaAuraSemAtributo` do Decay e do Flame)
     usam a constante SEM o fator (`...SemBonus`) e `Source` = `null`;
  3. as 9 auras de BUFF continuam avaliadas com o receptor (a ponta que o motor usa) — o
     `ContribuicaoDasAuras` mantem `ValorDaExpressao(efeito.Amount, receptor, receptor, ...)`.

POR QUE FONTE E NAO COMPORTAMENTO
---------------------------------
O teste e PURO (roda no CI, sem o jogo e sem dotnet). O que se prova aqui e a FORMA do codigo
que produz o numero; o numero em si e conferido em jogo pelo dono (`tools/checa_shrines.py` le o
log) e pelas fixtures da familia. A regra do repositorio e que o CODIGO do jogo vence — e este
arquivo transcreve o que o motor faz, com `arquivo:linha`.
"""
import re

# A avaliacao correta: constante SEM fator + `Source` = null.
_AVALIACAO_PERIGO = re.compile(
    r"ValorDaExpressao\(\s*FormulaDano(?:Flame|Decay)SemBonus\s*,\s*[A-Za-z_][A-Za-z0-9_]*\s*,\s*null\s*,")

# A avaliacao DEFEITUOSA (RV-34): a formula COM fator e/ou o receptor no slot `Source`.
_AVALIACAO_DEFEITO = re.compile(
    r"ValorDaExpressao\(\s*FormulaDoDano\(")

# O prefix pre-fix: escrevia no `Source` (o defeito). O `(?!=)` e obrigatorio: a mensagem de LOG
# do proprio conserto LE `gameFunctionParameters.Source == null` e um `=` sem a guarda confundiria a
# LEITURA com a ESCRITA — falso positivo que reprovaria o fonte CONFORME. O nome e o do parametro
# atual (auditoria t_b62183cc): era `__2`, posicional, e virou `gameFunctionParameters`.
_PREFIX_ESCREVE_SOURCE = re.compile(r"gameFunctionParameters\.Source\s*=(?!=)")

# A ponta que CONTINUA certa (9 auras de buff): o receptor nos DOIS slots do efeito.
_BUFF_COM_RECEPTOR = re.compile(
    r"ValorDaExpressao\(\s*efeito\.Amount\s*,\s*receptor\s*,\s*receptor\s*,")


def violacoes(texto):
    """Lista de violacoes da regra do RV-30 no FONTE passado (lista vazia = conforme)."""
    falhas = []

    if _PREFIX_ESCREVE_SOURCE.search(texto):
        falhas.append(
            "o prefix `FixShrineExpressionParams` AINDA escreve em `gameFunctionParameters.Source` — o `Source` do "
            "hover do shrine volta a ser o observador e o bonus do jogador entra nas duas auras de "
            "perigo, que leem `Source[...]` (o defeito do RV-30)")

    if _AVALIACAO_DEFEITO.search(texto):
        falhas.append(
            "alguma formula de perigo e avaliada por `FormulaDoDano(...)` (o seletor da constante "
            "COM o fator do personagem) — o numero passa a depender de um bonus que a aura nao usa")

    n_correto = len(_AVALIACAO_PERIGO.findall(texto))
    if n_correto != 4:
        falhas.append(
            "esperava as 4 avaliacoes de perigo com a constante SEM fator e `Source` = null "
            "(FraseAlvosDoFlame, LinhaDecayComValor, ItemDaAuraSemAtributo x2); achei %d" % n_correto)

    if not _BUFF_COM_RECEPTOR.search(texto):
        falhas.append(
            "o caminho das 9 auras de BUFF mudou: `ContribuicaoDasAuras` tem de continuar "
            "avaliando `efeito.Amount` com o receptor nos dois slots (o motor le `Target[...]` = "
            "quem RECEBE a aura)")

    return falhas
