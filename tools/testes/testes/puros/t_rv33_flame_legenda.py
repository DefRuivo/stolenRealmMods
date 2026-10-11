#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t_d02f9212 (RV-33 opcao (a)) — A LEGENDA DO FLAME SHRINE DIZ DE QUEM E A VIDA MAXIMA.

O DEFEITO QUE ESTE TESTE TRAVA (achado do cartao `t_d02f9212`, 06/10)
---------------------------------------------------------------------
A linha dinamica do Flame (`ShrineAuraPatch.FraseAlvosDoFlame`, o prefixo que entra no comeco da nota
da chave `"Attackers take Fire Damage."`) dizia

    In the aura now (raw damage it takes as the attacker, from its own Max Health and its own
    Shrine Effect Bonus): <nome> <dano>; ...

Duas coisas erradas na MESMA frase, e as duas sao o OPOSTO do que a formula do jogo faz:

  1. `its own Max Health` — o "it" podia ser lido como o personagem parado na aura. A formula le
     `Target["MaxHealth"]` e o `Target` dela e o ATACANTE (ver a cadeia provada no docstring de
     `regras_flame_legenda.py`) — a vida maxima usada e a DE QUEM ATACA;
  2. `and its own Shrine Effect Bonus` — o numero exibido NAO usa esse fator (RV-30: constante SEM o
     fator, `Source` = null; regra em `regras_rv30.py`) e o fator do asset e do personagem que TEM a
     aura, nao do atacante listado (RV-49).

A DECISAO (registrada no fonte, nao aqui)
-----------------------------------------
Opcao (a) da especificacao: um item por personagem na area, cada um PROJETADO como atacante, com o
dono da vida maxima NOMEADO na legenda. A escala por tipo (opcao b) continua fora da tooltip por
decisao do dono (TX-1: "tooltip nao e lugar de tabela") e a lista por alvo e a projecao aceita por ele
(limitacao do jogo: no hover ninguem sabe quem vai atacar).

O QUE E MEDIDO
--------------
RECORTE ESTRUTURAL (`recorte.corpo_do_metodo`, casamento de chaves — nunca janela de caracteres):
o corpo de `FraseAlvosDoFlame` no `ShrineAuraPatch.cs` e a ENTRADA da chave `"Attackers take Fire
Damage."` no `LocalizePatch.cs`. Sobre eles, as regras de `regras_flame_legenda.py`:
  * a linha tem de trazer o dono nomeado (`the attacker's own`) e a marca de `raw damage`;
  * a linha NAO pode trazer `from its own Max Health` nem citar `ShrineEffectBonus`;
  * a NOTA da chave (a que o jogador le) tem de manter `based on its own Max Health and not on the
    health of the one it attacked` e `before damage reduction`.

MORDE? As duas regras sao alimentadas TAMBEM com o trecho ANTIGO (o defeito) e o teste exige que ele
seja ACUSADO — checagem que nunca reprovou seria decoracao.

LIMITE. Nao executa o C# (pediria a `lib/` do jogo e um harness): o que se prova aqui e a FORMA do
texto que o mod monta, com o recorte estrutural. Quem fecha a TELA e o dono, no hover (o aceite do
cartao e humano).
"""
import io
import os

import arcabouco as arc
import recorte as rec
import regras_flame_legenda as reg

META = {
    "nome": "rv33-flame-legenda",
    "categoria": "pura",
    "requer": [],
    "descricao": "RV-33 opcao (a) (t_d02f9212): a linha do Flame nomeia o ATACANTE como dono da vida "
                 "maxima, nao cita o ShrineEffectBonus do alvo (o numero exibido nao o usa) e a nota "
                 "da chave continua dizendo de quem e a vida maxima e que o valor e PRE-REDUCAO",
}

ARQ_SHRINE = os.path.join("BetterTooltips", "Patches", "ShrineAuraPatch.cs")
ARQ_LOCALIZE = os.path.join("BetterTooltips", "Patches", "LocalizePatch.cs")
ASSINATURA = "public static string FraseAlvosDoFlame("
CHAVE_FLAME = '"Attackers take Fire Damage."'

# O trecho ANTIGO (o defeito): as duas frases erradas, na forma que estava no fonte ate 06/10.
TRECHO_ANTIGO = (
    '                return "In the aura now (raw damage it takes as the attacker, from its own Max Health"\n'
    '                    + " and its own Shrine Effect Bonus): " + string.Join("; ", partes.ToArray()) + ".";\n'
)

# A nota da chave SEM a marca do atacante (o defeito simetrico do lado da nota).
NOTA_ANTIGA = ('            { "Attackers take Fire Damage.",\n'
               '              "\\n<color=#C8B090>Raw damage, before damage reduction.</color>" },\n')


def _fonte(relativo):
    caminho = os.path.join(arc.raiz_do_repo(), relativo)
    with io.open(caminho, encoding="utf-8") as fh:
        return rec.codigo_efetivo(fh.read())


def corpo():
    shrine = _fonte(ARQ_SHRINE)
    localize = _fonte(ARQ_LOCALIZE)

    # ------------------------------------------------- 1. o FONTE VIVO (a linha do Flame)
    bloco = rec.corpo_do_metodo(shrine, ASSINATURA)
    rec.exigir_metodo_inteiro(bloco, ASSINATURA, marcas=("In the aura now", "catch (Exception ex)"))
    falhas = reg.violacoes_linha(bloco)
    arc.exigir(not falhas, "a LINHA do Flame viola a regra: " + "; ".join(falhas))

    # ------------------------------------------- 2. a regra MORDE (a redacao antiga e acusada)
    velhas = reg.violacoes_linha(TRECHO_ANTIGO)
    arc.exigir(any("its own Max Health" in f for f in velhas),
               "a regra NAO acusa o `from its own Max Health` (dono da vida maxima sem nome) — "
               "a checagem ficou vazia")
    arc.exigir(any("ShrineEffectBonus" in f for f in velhas),
               "a regra NAO acusa a linha citando o `ShrineEffectBonus` do alvo")
    arc.exigir(any("attacker's own" in f for f in velhas),
               "a regra NAO acusa a linha sem o dono nomeado (`the attacker's own`)")

    # --------------------------------------------------------- 3. a NOTA da chave do Flame
    i = localize.find(CHAVE_FLAME)
    arc.exigir(i >= 0, "nao achei a chave %s no LocalizePatch" % CHAVE_FLAME)
    entrada = rec.bloco_que_contem(localize, i)
    arc.exigir("based on its own Max Health" in entrada,
               "o recorte da entrada nao pegou a NOTA da chave (o bloco achado foi %r)" % entrada[:80])
    falhas_nota = reg.violacoes_nota(entrada)
    arc.exigir(not falhas_nota, "a NOTA da chave viola a regra: " + "; ".join(falhas_nota))

    # -------------------------------------------- 4. a regra da nota tambem MORDE (o defeito)
    nota_velha = reg.violacoes_nota(NOTA_ANTIGA)
    arc.exigir(any("de quem e a vida maxima" in f for f in nota_velha),
               "a regra NAO acusa a nota sem a marca do atacante — a checagem ficou vazia")

    print("conforme: linha nomeia `the attacker's own Max Health`, sem `ShrineEffectBonus`, com "
          "`raw damage`; nota da chave mantem o dono da vida maxima e a marca de PRE-REDUCAO; "
          "as duas redacoes antigas REPROVAM")


if __name__ == "__main__":
    arc.main(META, corpo)
