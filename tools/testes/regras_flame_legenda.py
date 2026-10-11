#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_flame_legenda.py - a LEGENDA do Flame Shrine lida no FONTE (familia TST-2).

O QUE ESTA REGRA TRAVA (cartao `t_d02f9212`, 06/10 — decisao RV-33 opcao (a))
---------------------------------------------------------------------------
A linha DINAMICA do Flame (`ShrineAuraPatch.FraseAlvosDoFlame`, o prefixo que entra no comeco da
nota da chave `"Attackers take Fire Damage."`) tem de dizer **DE QUEM e a vida maxima** que a
porcentagem usa. A formula provada (acao `Flame Aura Proc`, `Effects[0].Action`, string UTF-16LE
@1519546098; no dump regenerado por `ilspycmd 8.2.0` l.87922/87924) e

    TargetStored["FireDamage"] = Mathf.Max(1,  Mathf.Round((Target["MaxHealth"] *
        Target.GetValueByEnemyType(.025f, .08f, .1f, .12f, .14f, .05f)) *
        (1 + (Source["ShrineEffectBonus"] / 100))))

e o `Target` dela e **o ATACANTE** (a cadeia: status `Flame Shrine Aura` com `TriggerType = 1`,
`Condition = "Source.IsEnemy(Target)"` e `Targets = "Cell.IsCurrentHex(Target)"` — dump estrutural do
status, pathID 2543240; `target.ProcessSkillTriggers(source, ..., OnGettingHitDamaging, ...)` em
l.40959, `this` = quem foi acertado e o parametro `target` = o atacante; a acao roda no personagem da
celula alvo — l.42623/42632 — e `GetActionDamage` avalia com `Source = source, Target = target`,
l.39490-39494). Ou seja: a vida maxima E o tipo da conta sao **do atacante**, nao de quem apenas esta
parado na aura — e a legenda tem de dizer isso com o dono NOMEADO.

O QUE A LEGENDA NAO PODE DIZER (achado que motivou o cartao)
-----------------------------------------------------------
A redacao antiga era

    "In the aura now (raw damage it takes as the attacker, from its own Max Health and its own
     Shrine Effect Bonus): <nome> <dano>; ..."

e tinha DOIS defeitos de semantica, os dois presos aqui:
  1. `its own Max Health` — o "it" podia ser lido como o personagem parado na aura, que e o OPOSTO
     da formula; a versao corrente nomeia o dono (`the attacker's own Max Health`);
  2. `and its own Shrine Effect Bonus` — o NUMERO EXIBIDO nao usa esse fator: as quatro avaliacoes
     de perigo usam a constante SEM o fator com `Source` = null (RV-30, regra em `regras_rv30.py`),
     e o fator do asset le o `Source` do ATO, que e o personagem que TEM a aura (RV-49), nao o
     atacante listado. Citar o bonus do atacante era afirmar sobre o numero uma coisa que ele nao faz.

A NOTA da chave (`LocalizePatch`, a mesma linha do texto do jogo) tem de continuar dizendo de quem e
a vida maxima — `based on its own Max Health and not on the health of the one it attacked` — e que o
valor e PRE-REDUCAO (`before damage reduction`). A nota NAO foi reescrita neste cartao: a regra
existe para que ela nao perca essas duas marcas em silencio.

COMO A REGRA MORDE
------------------
`violacoes_linha` e `violacoes_nota` recebem o TRECHO de fonte; o teste alimenta o FONTE VIVO e o
TRECHO_ANTIGO (a redacao defeituosa) e exige que o antigo seja ACUSADO — checagem que nunca reprovou
seria decoracao.
"""
import re

# Os fatos que a linha TEM de carregar (semantica, nao wording: as marcas sao as palavras que
# carregam o fato).
_MARCA_DONO = "the attacker's own"
_MARCA_PRE_REDUCAO = "raw damage"
_MARCA_LISTA = "In the aura now"

# A pista de que o "it" ficou ambiguo (o dono da vida maxima nao esta nomeado) e a de que a linha
# afirma um fator que o numero nao usa. As duas em forma de FRAGMENTO, para nao depender do
# espacamento exato de uma frase.
_AMBIGUA = "from its own Max Health"
_BONUS_NA_LINHA = re.compile(r"Shrine Effect Bonus|ShrineEffectBonus")

_NOTA_ATACANTE = "based on its own Max Health and not on the health of the one it attacked"
_NOTA_PRE_REDUCAO = "before damage reduction"


def violacoes_linha(trecho):
    """Problemas da LINHA dinamica (o prefixo da lista por alvo). Lista vazia = conforme."""
    falhas = []
    if _MARCA_LISTA not in trecho:
        falhas.append("a linha perdeu o `%s` (o prefixo da lista por alvo)" % _MARCA_LISTA)
    if _MARCA_DONO not in trecho:
        falhas.append(
            "a linha NAO nomeia o dono da vida maxima (`%s`): o `its own` volta a poder ser lido "
            "como o personagem parado na aura, que e o OPOSTO da formula (Target = atacante)"
            % _MARCA_DONO)
    if _AMBIGUA in trecho:
        falhas.append("a linha voltou ao `%s` (dono da vida maxima sem nome)" % _AMBIGUA)
    if _BONUS_NA_LINHA.search(trecho):
        falhas.append(
            "a linha afirma o `ShrineEffectBonus` do alvo — o numero exibido NAO usa esse fator "
            "(as 4 avaliacoes de perigo usam a constante SEM o fator, RV-30) e o fator do asset e do "
            "personagem que TEM a aura (RV-49)")
    if _MARCA_PRE_REDUCAO not in trecho:
        falhas.append("a linha perdeu o `%s` (a marca de que o valor e PRE-REDUCAO de dano)"
                      % _MARCA_PRE_REDUCAO)
    return falhas


def violacoes_nota(trecho):
    """Problemas da NOTA da chave do Flame. Lista vazia = conforme."""
    falhas = []
    if _NOTA_ATACANTE not in trecho:
        falhas.append(
            "a nota da chave perdeu `%s` — e ela que diz, na tela, de quem e a vida maxima que a "
            "porcentagem usa" % _NOTA_ATACANTE)
    if _NOTA_PRE_REDUCAO not in trecho:
        falhas.append("a nota da chave perdeu `%s` (marca de PRE-REDUCAO)" % _NOTA_PRE_REDUCAO)
    if "Shrine Effect Bonus" in trecho and _NOTA_ATACANTE not in trecho:
        falhas.append("a nota fala do `Shrine Effect Bonus` sem dizer de quem e a vida maxima")
    return falhas
