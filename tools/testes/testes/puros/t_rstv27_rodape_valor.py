#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RSTV-27 PELO VALOR: o rodape da tooltip read-only (mana/cooldown/alcance) mostra os numeros do ALVO DO MODAL.

O QUE ESTE TESTE PRENDE
-----------------------
A SAIDA - o VALOR numerico que o rodape monta. Nao "o metodo foi chamado", nao "o overload mudou de
assinatura": os tres numeros do rodape (mana, cooldown, alcance) sao comparados, campo a campo, contra o
valor DERIVADO DO ALVO DO MODAL (o de `ReadOnlySession.Target`), e ainda contra a BASE do overload sem
personagem - que e' o que o defeito mostra.

O CENARIO e' o da tela Party Select read-only: o `TooltipCharacter` do JOGO e' null (o getter e'
`GameLogic.instance.CurrentlySelectedCharacter`) e o alvo do MODAL esta definido.

DE ONDE VEM O ESPERADO
----------------------
Da fixture versionada `rstv27-rodape-valor.esperado.json`, GERADA pelo oraculo C#
(`tools/testes/fixtures/geradores/oraculo_rstv27`) a partir do cenario `...entrada.json`: o oraculo passa
pelo caminho de conta do MOTOR (aritmetica FLOAT + Mathf.CeilToInt/FloorToInt/Max), transcrito do
decompilado do `ActionInfo` (lib/Assembly-CSharp.dll). O Python NAO recalcula mana/cooldown/alcance - ele
so' escolhe QUAL dos dois caminhos o rodape usa (o erro do defeito) e compara o NUMERO. As regras e a
transcricao estao em `tools/testes/regras_rstv27_valor.py` (fonte lida AO VIVO do mod, nunca copia).

ACEITE (medido em `tools/testes/rstv27-valor-prova-reprovando.log`): sem o conserto - o hover nao armando
o alvo, ou o postfix nao preenchendo - o teste REPROVA por VALOR; com o conserto PASSA.
"""
import regras_rstv27 as reg
import regras_rstv27_valor as rv

import arcabouco as arc

META = {
    "nome": "rstv27-rodape-valor",
    "categoria": "pura",
    "requer": [],
    "descricao": ("RSTV-27 pelo VALOR: o rodape da tooltip read-only (mana/cooldown/alcance) monta os "
                  "numeros do ALVO DO MODAL (`ReadOnlySession.Target`), nunca a base do overload sem "
                  "personagem; com alvo nulo o fallback devolve o comportamento do jogo e no inventario o "
                  "valor do JOGO vence. Os 2 defeitos que MUDAM O NUMERO (hover sem armar; gancho sem "
                  "preencher) REPROVAM; a guarda do valor do jogo e o fallback sao NO-OP de valor - o teste "
                  "nao finge o contrario"),
}


ROTULOS = {"mana": "MANA", "cooldown": "COOLDOWN", "alcance": "ALCANCE"}


def _cenario(src_tab, src_gancho, jogo, alvo):
    """O estado do gancho NESTA montagem: `_alvoDoModal` = o alvo so' se o hover o armou (fonte viva)."""
    armado = rv.armado_do_fonte(src_tab)
    return rv.personagem_do_rodape(jogo, alvo if armado else None, rv.gancho_do_fonte(src_gancho))


def _valores(personagem, base, por):
    return rv.rodape(personagem, base, por)


def corpo():
    entrada = arc.ler_json("rstv27-rodape-valor", "entrada")
    esperado = arc.ler_json("rstv27-rodape-valor", "esperado")
    src_tab = rv.fonte_hover()
    src_gancho = rv.fonte_gancho()
    arc.exigir(len(src_tab) > 1000 and len(src_gancho) > 1000,
               "o fonte do mod veio vazio/curto: a leitura mudou de lugar?")

    base = esperado["sem_personagem"]
    por = esperado["por_personagem"]
    alvo = entrada["cenario"]["alvo_do_modal"]
    jogo = entrada["cenario"]["tooltip_character_do_jogo"]
    outro = "Outro"

    # ---------------------------------------------------------------- 0) o caso MORDE
    arc.igual(jogo, None,
              "a premissa do cenario: na Party Select o `TooltipCharacter` do JOGO e' null")
    for campo in rv.CAMPOS:
        arc.exigir(base[campo] != por[alvo][campo],
                   "o cenario nao separa o valor do alvo do valor de BASE no campo '%s' (%r x %r): a "
                   "checagem nao morderia nada" % (campo, por[alvo][campo], base[campo]))

    # ------------------------------- 1) o RODAPE montado para o ALVO DO MODAL: OS NUMEROS (a SAIDA)
    # O estado do gancho (alvo armado / preenchimento) sai da FONTE VIVA; e' ele que decide QUEM o rodape
    # consulta - por isso, sem o conserto, o que fica errado e' o NUMERO abaixo.
    personagem = _cenario(src_tab, src_gancho, jogo, alvo)
    valores = _valores(personagem, base, por)
    divergencias = []
    for campo in rv.CAMPOS:
        if valores[campo] != por[alvo][campo]:
            divergencias.append("%s: esperado %r (o NUMERO do alvo '%s'), obtido %r%s"
                                % (ROTULOS[campo], por[alvo][campo], alvo, valores[campo],
                                   " - IGUAL ao valor de BASE, o defeito do RSTV-27"
                                   if valores[campo] == base[campo] else ""))
    arc.exigir(not divergencias,
               "o rodape da Party Select read-only NAO monta os NUMEROS do ALVO DO MODAL: "
               + " | ".join(divergencias))
    # (o VALOR ja' esta' preso; este assert e as regras abaixo dizem POR QUE, a partir da fonte viva)
    arc.igual(personagem, alvo,
              "com o alvo do modal armado e o jogo devolvendo null, o rodape tem de consultar o ALVO DO MODAL")
    arc.exigir(rv.armado_do_fonte(src_tab),
               "o hover NAO arma o alvo do MODAL (`ReadOnlySession.Target`) em volta da montagem da tooltip")
    gancho = rv.gancho_do_fonte(src_gancho)
    for flag, exigencia in (("le_o_alvo", "le o alvo armado (`<var> = _alvoDoModal;`)"),
                            ("preenche", "preenche o null (`__result = <var>;`)"),
                            ("valor_do_jogo_vence", "deixa o valor do JOGO vencer (`if (__result != null) return;`)"),
                            ("fallback", "tem o FALLBACK (`if (<var> == null) return;`)"),
                            ("fail_safe", "e' fail-safe (try/catch)")):
        arc.exigir(gancho[flag], "o postfix do getter NAO %s" % exigencia)

    # --------------------------------------- 2) caso NEGATIVO: alvo nulo -> FALLBACK
    sem_alvo = _cenario(src_tab, src_gancho, jogo, None)
    arc.igual(sem_alvo, None,
              "com o alvo NULO o gancho nao pode inventar personagem (fallback: comportamento do jogo)")
    arc.igual(_valores(sem_alvo, base, por), dict(base),
              "sem alvo do modal o rodape tem de continuar como o jogo faz (a BASE)")

    # ------------------------------ 3) o inventario: o VALOR DO JOGO vence (nao regride)
    arc.igual(_valores(_cenario(src_tab, src_gancho, outro, None), base, por), dict(por[outro]),
              "fora da nossa tooltip (inventario) o personagem do JOGO continua valendo")
    arc.igual(_valores(_cenario(src_tab, src_gancho, outro, alvo), base, por), dict(por[outro]),
              "o gancho NAO pode sobrescrever um personagem que o jogo ja' resolveu (guarda do valor do jogo)")

    # ----------------------- 4) PROVA DE FOGO: o que MUDA O NUMERO reprova; o que nao muda nao se finge
    def _bite(rotulo, src_defeituoso, como, jogo_, alvo_, esperado_mantido):
        """O defeito plantado em memoria tem de trocar QUEM o rodape consulta (e o NUMERO)."""
        obtido = como(src_defeituoso, jogo_, alvo_)
        arc.exigir(obtido != esperado_mantido,
                   "o defeito '%s' NAO foi pego pelo VALOR: o rodape continuaria consultando %r "
                   "(esperado quebrar para outro personagem/None)" % (rotulo, esperado_mantido))
        return obtido

    def _monta(src_defeituoso, jogo_, alvo_):
        return _cenario(src_defeituoso[0], src_defeituoso[1], jogo_, alvo_)

    # (a) o hover sem armar o alvo do modal - o defeito do RSTV-27: o rodape cai na BASE.
    defeito = reg.hover_sem_armado(src_tab)
    arc.exigir(defeito != src_tab, "o plantio 'hover sem o armado' nao encontrou a ancora (`ComAlvo(alvo)`)")
    arc.igual(_valores(_bite("hover sem armar o alvo do modal", (defeito, src_gancho), _monta, jogo, alvo, alvo),
                       base, por), dict(base),
              "com o hover sem armar o alvo o rodape mostra a BASE (o defeito do RSTV-27)")

    # (b) o gancho existe mas nunca PREENCHE: o rodape continua lendo o null.
    defeito = reg.gancho_sem_preenchimento(src_gancho)
    arc.exigir(defeito != src_gancho, "o plantio 'gancho sem preenchimento' nao encontrou `__result = alvo;`")
    arc.igual(_valores(_bite("gancho sem preenchimento", (src_tab, defeito), _monta, jogo, alvo, alvo),
                       base, por), dict(base),
              "com o gancho sem preencher o rodape mostra a BASE")

    # (c) CONTROLE NEGATIVO - o FALLBACK plantado NAO muda o NUMERO. Achado do teste de valor: com a
    #     guarda do valor do jogo no lugar, `if (alvo == null) return;` e' NO-OP de valor (`__result =
    #     null` escreveria o mesmo null que ja' estava la). Quem prende essa regra e' a checagem
    #     ESTRUTURAL (t_rstv27_rodape_personagem) - aqui so' se exige que o teste NAO finja que o valor
    #     a pega, e que a leitura da flag na fonte seja real.
    defeito = reg.gancho_sem_fallback(src_gancho)
    arc.exigir(defeito != src_gancho, "o plantio 'gancho sem fallback' nao encontrou `if (alvo == null) return;`")
    arc.exigir(not rv.gancho_do_fonte(defeito)["fallback"],
               "a leitura da flag do FALLBACK nao reagiu ao plantio: a checagem seria decoracao")
    arc.igual(_valores(_cenario(src_tab, defeito, jogo, alvo), base, por), dict(por[alvo]),
              "o FALLBACK removido NAO pode mudar o valor da Party Select (e' o que faz dele um NO-OP de valor)")
    arc.igual(_valores(_cenario(src_tab, defeito, outro, None), base, por), dict(por[outro]),
              "o FALLBACK removido NAO pode mudar o valor do INVENTARIO (a guarda do valor do jogo ja' cobre)")

    # (d) CONTROLE NEGATIVO - a GUARDA DO VALOR DO JOGO plantada so' tem efeito de valor no caso
    #     SINTETICO (`_alvoDoModal` armado com o jogo devolvendo personagem - estado que a premissa da
    #     Party Select exclui). O MODELO tem de o mapear; o teste NAO finge que o valor o pega nos
    #     estados alcancaveis.
    defeito = reg.gancho_sobrescreve(src_gancho)
    arc.exigir(defeito != src_gancho, "o plantio 'gancho sobrescreve' nao encontrou a guarda do valor do jogo")
    arc.exigir(not rv.gancho_do_fonte(defeito)["valor_do_jogo_vence"],
               "a leitura da flag do valor do jogo nao reagiu ao plantio: a checagem seria decoracao")
    arc.igual(_valores(_cenario(src_tab, defeito, jogo, alvo), base, por), dict(por[alvo]),
              "a guarda removida NAO pode mudar o valor da Party Select (o jogo devolve null)")
    arc.igual(_valores(_cenario(src_tab, defeito, outro, None), base, por), dict(por[outro]),
              "a guarda removida NAO pode mudar o valor do INVENTARIO (nao ha alvo armado)")
    arc.igual(_valores(_cenario(src_tab, defeito, outro, alvo), base, por), dict(por[alvo]),
              "CASO SINTETICO do modelo: sem a guarda, o alvo armado sobrescreveria o personagem do jogo "
              "(o numero viraria o do MODAL num estado que o rodape do inventario nunca deveria ler)")

    print("RSTV-27 (valor): na Party Select read-only (TooltipCharacter null) o rodape monta com o ALVO DO "
          "MODAL '%s' - mana=%r cooldown=%r alcance=%r, contra a BASE %r/%r/%r do overload sem personagem; "
          "alvo nulo cai no fallback (BASE) e no inventario o personagem do JOGO vence. Os 2 defeitos que "
          "MUDAM O NUMERO (sem armar o alvo; gancho sem preencher) REPROVAM; a guarda do valor do jogo e o "
          "fallback sao NO-OP de valor (quem os prende e' a checagem estrutural) e o teste nao finge o "
          "contrario."
          % (alvo, valores["mana"], valores["cooldown"], valores["alcance"],
             base["mana"], base["cooldown"], base["alcance"]))


if __name__ == "__main__":
    arc.main(META, corpo)
