#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EXCESSO DE SHRINE (TST-2): DOIS PERSONAGENS na MESMA aura de shrine.

POR QUE ESTE TESTE EXISTE (a lacuna que ele fecha)
--------------------------------------------------
`docs/PLANO-DE-TESTES.md` (~linha 24) poe "dois personagens na mesma aura" no
vocabulario do EXCESSO DE SHRINE. A familia `t_shrine_*` cobria:
  * a aura repetida DENTRO de um personagem (RV-46: `Dodge +120%` -> `+40%`);
  * duas AURAS diferentes do mesmo personagem no mesmo atributo (Warrior + Fury);
  * os stacks do mesmo status (`TotalStacks`);
  * a DWA-2 (dois Dwarven no MESMO personagem contam por INSTANCIA).
Nunca a MESMA aura viva em DOIS PERSONAGENS distintos - e e exatamente essa a
pergunta do cenario: quando ha mais de um personagem, a linha conta a aura UMA vez
para CADA um, com o bonus DAQUELE personagem, ou soma/desduplica entre eles?

A REGRA QUE ESTE TESTE PRENDE (fonte viva)
------------------------------------------
A linha `Your active shrine auras:` e POR PERSONAGEM. `AcumuladoShrines` pergunta
as auras do RECEPTOR (`AurasVivas(receptor)`, ShrineAuraPatch.cs 1113) e `AurasVivas`
le a lista VIVA DO PROPRIO personagem (`receptor.ActionStatuses`, l.1295) - nao a
lista de todos os personagens da area. Consequencias (as tres viram assert):
  1. cada personagem conta a aura UMA vez - a MESMA aura em dois personagens NAO e
     "instancia" DENTRO de um deles (a desdupe do RV-46 e por lista viva, e cada
     personagem tem a sua);
  2. o valor usa o `ShrineEffectBonus` DAQUELE personagem (RV-30: o mesmo base 20
     sai 20 para um e 40 para o outro) - nunca um bonus global/somado;
  3. por isso a aura de GATILHO (Dwarven, DWA-2) sai UM item por personagem, com o
     numero DELE - e nao um item por personagem DENTRO da linha de cada um (que
     seria o defeito de varrer `Root.AllCharacters`).

DE ONDE VEM O ESPERADO (nada digitado de cabeca)
------------------------------------------------
De `tools/fixtures/shrines-rv46-dedupe.log`, log VERSIONADO: as linhas
`RV-31 acumulado` registram a MESMA aura (`Rogue Aura`, `Dwarven Aura`) viva em
personagens DIFERENTES (ChkRA 0 x Raven 100; ChkDW0 0 / ChkDW20 20 / ChkDW 100),
cada uma com o `bonus=` e o item daquele personagem. A fixture
`shrine-dois-personagens.*.json` transcreve esses trechos e o teste confere que
cada `log_linha` continua no log - o esperado nao pode envelhecer. A tabela do
bonus vem da fixture da familia (`excesso-shrine.entrada.json`, via
`regras_shrine.contexto`), nao de uma lista digitada aqui.

A ISCA E EMBUTIDA (como no BT-10, no MAN-2 e na RSTV-8): o proprio teste planta o
defeito numa copia EM MEMORIA do fonte (varredura de TODOS os personagens) e exige
que a checagem REPROVE - checagem que nunca foi vista reprovando seria decoracao.
"""
import os
import re

import arcabouco as arc
import recorte as rec
import regras_shrine as reg

META = {
    "nome": "shrine-dois-personagens",
    "categoria": "pura",
    "requer": [],
    "descricao": "a MESMA aura viva em mais de um personagem conta 1x POR PERSONAGEM (a lista viva e a do receptor), com o bonus de cada um",
}

CASO = "shrine-dois-personagens"

# As duas ligacoes vivas que fazem a linha ser POR PERSONAGEM (ShrineAuraPatch.cs).
ASSINATURA_ACUMULADO = "public static string AcumuladoShrines(string chaveDaTooltip)"
ASSINATURA_AURAS_VIVAS = "private static List<ActionStatus> AurasVivas(Character receptor)"


def cena_do_personagem(grupo, personagem):
    """A cena de UM personagem: a aura MESMA uma vez na lista DELE, o bonus DELE."""
    return {
        "id": personagem["id"],
        "bonus_id": personagem["bonus_id"],
        "maxhealth": 100,
        "tipo_receptor": "player",
        "vivas": [{"aura": grupo["aura"], "instancias": 1, "stacks": 1, "expressao": True}],
        "alvos": [],
        "totais": dict(personagem.get("totais") or {}),
    }


def checar_per_personagem(codigo):
    """A regra VIVA: a lista de auras da linha sai do PROPRIO personagem em foco.

    Recorte ESTRUTURAL (recorte.corpo_do_metodo: casamento de chaves, nunca janela
    de caracteres) e leitura do CODIGO EFETIVO (comentario nao e codigo).
    """
    corpo = rec.corpo_do_metodo(codigo, ASSINATURA_AURAS_VIVAS)
    efetivo = rec.codigo_efetivo(corpo)
    arc.exigir("receptor.ActionStatuses" in efetivo,
               "AurasVivas deixou de ler a lista VIVA do PROPRIO receptor "
               "(`receptor.ActionStatuses`): a linha nao sai mais do personagem em foco")
    arc.exigir("AllCharacters" not in efetivo,
               "AurasVivas passou a varrer TODOS os personagens (`AllCharacters`): com DOIS "
               "personagens na mesma aura a lista de um traria a aura do outro - a linha dobra "
               "no gatilho (DWA-2) e/ou usa o `ShrineEffectBonus` errado na aura de atributo")
    acumulado = rec.corpo_do_metodo(codigo, ASSINATURA_ACUMULADO)
    arc.exigir(re.search(r"AurasVivas\(receptor\)", acumulado) is not None,
               "AcumuladoShrines deixou de pedir as auras do RECEPTOR (`AurasVivas(receptor)`): "
               "a linha deixou de ser por personagem")


def corpo():
    ent = arc.ler_json(CASO, "entrada")
    esp = arc.ler_json(CASO, "esperado")
    esperadas = reg.por_id(esp["personagens"])

    # A tabela de bonus da FAMILIA (nada de lista digitada aqui).
    ctx = reg.contexto(reg.entrada_do_caso())

    # A MEDICAO: o log versionado e a fonte do esperado.
    log_caminho = os.path.join(arc.raiz_do_repo(), "tools", "fixtures", "shrines-rv46-dedupe.log")
    arc.exigir(os.path.isfile(log_caminho),
               "a medicao em jogo sumiu: %s (%s)" % (log_caminho, ent.get("fonte_dos_valores")))
    with open(log_caminho, encoding="utf-8", errors="replace") as fh:
        log = fh.read()

    vistos = 0
    for grupo in ent["grupos"]:
        personagens = grupo["personagens"]
        arc.exigir(len(personagens) >= 2,
                   "o grupo '%s' tem de ter DOIS ou mais personagens na MESMA aura "
                   "(e o cenario deste teste)" % grupo["id"])

        itens_do_grupo = {}
        for p in personagens:
            arc.exigir(p["id"] in esperadas,
                       "o personagem '%s' da entrada nao tem esperado na fixture" % p["id"])
            alvo = esperadas[p["id"]]
            arc.igual(alvo["nome"], p["nome"], "o nome do personagem '%s'" % p["id"])

            # PROCEDENCIA: a linha do esperado continua, VERBATIM, no log versionado.
            arc.exigir(alvo["log_linha"] in log,
                       "a linha de procedencia do caso '%s' nao esta mais no log versionado "
                       "(o esperado envelheceu): %r" % (p["id"], alvo["log_linha"]))
            m = re.search(r"bonus=(\d+)", alvo["log_linha"])
            arc.exigir(m is not None,
                       "a linha do log do caso '%s' nao traz o campo `bonus=`" % p["id"])
            arc.igual(int(m.group(1)), ctx["bonus"][p["bonus_id"]],
                      "o `bonus=` do log do personagem '%s' x a fonte de bonus declarada "
                      "(%s) na tabela da familia" % (p["nome"], p["bonus_id"]))
            # O item esperado e o trecho da PROPRIA linha do log (nada somado a mao).
            for item in alvo["itens"]:
                arc.exigir(item in alvo["log_linha"].split(" -> ", 1)[-1],
                           "o item esperado %r do personagem '%s' nao e o trecho da linha do log"
                           % (item, p["nome"]))

            cena = cena_do_personagem(grupo, p)
            saida = reg.agregar(cena, ctx)

            arc.igual(saida["itens"], alvo["itens"],
                      "os itens do personagem '%s' (%s, bonus %s)"
                      % (p["nome"], grupo["aura"], p["bonus_id"]))
            arc.igual(saida["repeticoes"], alvo["repeticoes"],
                      "as repeticoes do personagem '%s'" % p["nome"])

            # 1. A aura entra UMA vez na lista DELE - a MESMA aura em personagens DIFERENTES
            #    nao vira `instancia` DENTRO de um (a desdupe do RV-46 e por lista viva).
            unicas, _stacks, repeticoes = reg.vivas_desduplicadas(cena)
            arc.igual(unicas, [grupo["aura"]],
                      "a lista viva desduplicada do personagem '%s'" % p["nome"])
            arc.igual(repeticoes, [],
                      "a MESMA aura em personagens DIFERENTES nao e repeticao DENTRO de '%s' "
                      "(nao pode sair `instancias=[...]` na linha dele)" % p["nome"])

            arc.exigir(saida["linha"].startswith("Your active shrine auras: "),
                       "a linha do personagem '%s' comeca pelo marcador do mod" % p["nome"])
            arc.exigir(saida["linha"].endswith("."),
                       "a linha do personagem '%s' fecha no ponto" % p["nome"])

            itens_do_grupo[p["id"]] = tuple(saida["itens"])
            vistos += 1

        # 2. Cada personagem usa o PROPRIO bonus: bonus diferentes -> itens DIFERENTES.
        #    Se um herdasse o numero do outro (bonus global/somado), esta igualdade cai.
        arc.exigir(len(set(itens_do_grupo.values())) == len(itens_do_grupo),
                   "no grupo '%s', a MESMA aura em personagens DIFERENTES com bonus diferentes "
                   "tem de sair com itens DIFERENTES - um personagem nao pode herdar o numero "
                   "do outro: %s" % (grupo["id"], dict(itens_do_grupo)))

        # 3. Nada de somar personagens: o item de um nao pode conter o numero do outro.
        for pid, itens in itens_do_grupo.items():
            for outro, itens_outro in itens_do_grupo.items():
                if outro == pid:
                    continue
                for item_outro in itens_outro:
                    arc.exigir(item_outro not in itens,
                               "o item de '%s' contem o item de '%s' (%r): os personagens "
                               "estao sendo somados/juntados numa linha so" % (pid, outro, item_outro))

    # ------------------------------------------------------------------ ISCA EMBUTIDA (MODELO)
    # O defeito: juntar a lista viva dos DOIS personagens. Na aura de GATILHO (DWA-2) a
    # repeticao conta por INSTANCIA, entao a aura do outro personagem viraria um SEGUNDO item
    # na linha de quem esta em foco. O teste exige que o resultado CORRETO difira do DEFEITUOSO
    # - se nao diferisse, esta checagem seria decoracao.
    grupo_dw = reg.por_id(ent["grupos"])["gatilho-dwarven"]
    um_dwarven = reg.por_id(esp["personagens"])[grupo_dw["personagens"][0]["id"]]["itens"]
    pool = cena_do_personagem(grupo_dw, grupo_dw["personagens"][0])
    pool["vivas"] = [{"aura": grupo_dw["aura"], "instancias": 2, "stacks": 1, "expressao": True}]
    itens_pool = reg.agregar(pool, ctx)["itens"]
    arc.exigir(itens_pool != um_dwarven,
               "ISCAS EMBUTIDA (modelo): juntar a aura de DOIS personagens TEM de mudar a linha da "
               "aura de gatilho (DWA-2) - se nao mudasse, a checagem de per-personagem nao morde nada")

    # ------------------------------------------------------------------ O MOD VIVO
    caminho = os.path.join(arc.raiz_do_repo(), "BetterTooltips", "Patches", "ShrineAuraPatch.cs")
    arc.exigir(os.path.isfile(caminho),
               "a fonte viva das regras sumiu: %s (o teste vigia ela, nao uma copia)" % caminho)
    with open(caminho, encoding="utf-8") as fh:
        fonte = fh.read()

    checar_per_personagem(fonte)  # o fonte VIVO tem de passar

    # ------------------------------------------------------------------ ISCA EMBUTIDA (FONTE)
    # Planta o defeito (a lista viva lida de TODOS os personagens) numa copia EM MEMORIA e
    # exige que a checagem REPROVE. Sem isto, uma checagem que nunca reprovou seria decoracao.
    defeituoso = fonte.replace("receptor.ActionStatuses",
                               "Burst2Flame.Root.AllCharacters[0].ActionStatuses")
    arc.exigir(defeituoso != fonte,
               "nao consegui plantar o defeito no fonte (a ancora `receptor.ActionStatuses` mudou?)")
    reprovou = False
    try:
        checar_per_personagem(defeituoso)
    except arc.Falhou:
        reprovou = True
    arc.exigir(reprovou,
               "ISCAS EMBUTIDA (fonte): a checagem NAO reprovou a lista lida de TODOS os "
               "personagens (`AllCharacters`) - a trava do cenario nao morde o defeito")

    print("dois-personagens: %d personagens em %d auras conferidos (por-personagem + DWA-2)"
          % (vistos, len(ent["grupos"])))


if __name__ == "__main__":
    arc.main(META, corpo)
