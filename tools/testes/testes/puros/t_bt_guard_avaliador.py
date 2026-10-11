#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""O GUARD ANTES DO INDEXADOR (TST-3, cenario 5) - indexar atributo inexistente LANCA no motor.

O QUE ESTE TESTE PRENDE
-----------------------
O indexador `Character.this[string]` do motor LANCA para nome desconhecido (`GetAttribute`,
decompilado l.32662-32675). Em `AtributoPercentualPatch.MontaPartes` o guard `EhAtributoPrimario`
(l.185-188) roda ANTES de `personagem[atributo.name]` (l.200) - e o guard so deixa passar
atributo que veio da PROPRIA array do motor (`Game.Instance.LevelableCharacterAttributes`,
l.237-247), entao o indexador nunca ve um nome que nao existe.

O teste prova as DUAS metades:

  * ESTRUTURA - no FONTE de verdade, `EhAtributoPrimario` aparece ANTES de `personagem[`;
  * COMPORTAMENTO - com um atributo que NAO existe no motor, o guard PULA (devolve None) em vez
    de estourar. A isca `cp_bt_guard_isca.py` usa a regra SEM guarda e REPROVA.

NAO e shrine: mora em `AtributoPercentualPatch.cs` (BT-13).
"""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "bt-guard-avaliador",
    "categoria": "pura",
    "requer": [],
    "descricao": "o guard (EhAtributoPrimario) roda ANTES do indexador do motor: atributo inexistente e pulado, nunca explode",
}


def corpo():
    fonte = R.le_fonte(R.ATRIBUTO_PERCENTUAL)

    # ESTRUTURA: a guarda aparece ANTES da indexacao.
    pos_guarda = R.pin(fonte, "if (!EhAtributoPrimario(atributo, primarios))",
                       "o guard de atributo primario no MontaPartes")
    pos_index = R.pin(fonte, "float atual = personagem[atributo.name];",
                      "a indexacao do personagem")
    arc.exigir(pos_guarda < pos_index,
               "o GUARD tem de aparecer ANTES do indexador (guard em %d, index em %d)"
               % (pos_guarda, pos_index))

    # O guard existe porque o indexador LANCA - o pin do contrato do motor esta no C#.
    R.pin(fonte, "EhAtributoPrimario", "o predicado do guard")

    # COMPORTAMENTO: com_guarda pula o atributo inexistente; sem_guarda explode.
    viol = R.violacoes_do_guard("com_guarda")
    arc.igual(viol, [], "o guard divergiu: %s" % viol)

    # A prova negativa explicita: sem o guard, o MESMO caso explode no indexador.
    feito = False
    try:
        R.valor_do_atributo({"Might": 100.0}, "Courage", R.ATRIBUTOS_DO_MOTOR, modo="sem_guarda")
    except R.IndexadorDoMotorLanca:
        feito = True
    arc.exigir(feito, "o controle falhou: sem guard o indexador NAO lancou - o guard deixou de "
                      "ser necessario e a regra precisa de revisao")

    print("guard (EhAtributoPrimario) precede a indexacao no fonte; atributo inexistente e "
          "pulado com guard e explode sem ele")


if __name__ == "__main__":
    arc.main(META, corpo)
