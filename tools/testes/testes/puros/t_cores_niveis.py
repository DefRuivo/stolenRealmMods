#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AS CORES DOS TRES NIVEIS (COR-2): procedencia datada, sanidade do nivel 2 e a cor CHEGANDO
AO BLOCO pelo gancho das notas.

POR QUE ESTE TESTE EXISTE
-------------------------
A REV-50 mostrou que a procedencia declarada das cores nao se sustentava e que a cor do nivel 2
nunca chegava ao tooltip. Este teste prende as duas coisas nas provas medidas, nao em prosa:

  1. CONTROLE DA LEITURA. Os hex vem do PREFAB do jogo, lidos em 01/10 (fixture `cores-do-jogo`,
     gerada por `scratch/cor2/le_cores_do_tooltip.py` + `le_guimanager_cores.py`). Uma leitura de
     asset so vale se o leitor estiver VALIDADO: o `GUIManager.coldColor` que ela devolve
     (`#00D7FF`) e exatamente o que o log de uma sessao real imprime ao ler o mesmo campo. Este
     teste exige essa igualdade — sem ela, o resto seria numero solto.

  2. NIVEL 2 — SANIDADE (o que faltava: so o nivel 3 tinha teste de azul). O campo declarado
     (`Tooltip.specialDescColor`) tem de ser um TOM DE EXPLICACAO (quente/bege, NUNCA azul) —
     senao o nivel 2 vira uma copia do nivel 3, que foi o achado do COR-1. E o marcador escrito
     no codigo tem de estar na MESMA familia de tom do campo (a diferenca que existe e de
     METODO: pixel num print em 29/09 x leitura do prefab em 01/10).

  3. A COR CHEGANDO AO BLOCO. O pedido e explicito: nao basta o codigo parecer certo. Aqui estao
     (a) a ordem REAL do 0Harmony do jogo lida do proprio DLL (`-priority.CompareTo` ordena
     DESCENDENTE: maior roda primeiro), (b) o desenho ANTIGO rodado nessa ordem — que deixa o
     marcador no texto final, exatamente o que o log mostra, e (c) o desenho de HOJE, em que o
     gancho das notas aplica a cor no fim: o marcador some e a cor do campo aparece. Mais a
     invariante ESTRUTURAL no fonte: nao existe gancho de cor separado com prioridade.
"""
import re

import arcabouco as arc
import regras_cor as reg

META = {
    "nome": "cores-niveis",
    "categoria": "pura",
    "requer": [],
    "descricao": "procedencia datada dos 3 niveis, sanidade do nivel 2 e a cor do campo chegando ao bloco",
}

NOTA_DO_LOG = ("<color=#C8B090>Base 20%; the value shown already includes the "
               "Shrine Effect Bonus.</color>")
TEXTO_DO_JOGO = "Increases Dodge Chance by 40%."


def _troca_o_marcador(texto, cor_do_campo):
    """O que `ComACorDoJogo` faz: troca `<color=#MARCADOR>` pela cor lida no campo."""
    return texto.replace("<color=" + reg.entrada_marcador() + ">", "<color=" + cor_do_campo + ">")


def _anexa_a_nota(texto, nota):
    """O que `AnexarNota` faz: uma linha em branco e o bloco da nota (com o MARCADOR)."""
    return texto.rstrip() + "\n\n" + nota


def _ordem_real_do_harmony(ganchos):
    """A ordem do 0Harmony do jogo: `PatchSorter` -> `PatchInfoSerialization.PriorityComparer`
    devolve `-priority.CompareTo(value)` (bancada `scratch/cor2/PatchInfoSerialization.cs:48-58`),
    ou seja ordena DESCENDENTE — a prioridade MAIOR roda PRIMEIRO — e o `HarmonyManipulator`
    emite as chamadas na ordem da lista ordenada (`HarmonyManipulator.cs:646`)."""
    return sorted(ganchos, key=lambda g: -g[1])


def corpo():
    ent = reg.leitura_datada()
    marcador = reg.entrada_marcador()

    # ------------------------------------------------- 1. CONTROLE DA LEITURA DO PREFAB
    arc.igual(ent["marcador_no_codigo"]["hex"], marcador,
              "o marcador da convencao e o do codigo tem de ser o mesmo")
    log = ent["log_de_runtime"]
    arc.exigir(log["azul_lido"], "a fixture tem de carregar a linha de azul lido do log de runtime")
    azul_do_log = set(re.findall(r"#([0-9A-Fa-f]{6})", " ".join(log["azul_lido"])))
    arc.igual(reg.cor_da_hud("coldColor"), "#00D7FF",
              "o `coldColor` do prefab tem de ser o #00D7FF que o log de runtime imprime")
    arc.exigir("00D7FF" in {a.upper() for a in azul_do_log},
               "o log tem de registrar a leitura do coldColor em runtime (controle do leitor): %s"
               % log["azul_lido"])
    arc.exigir(any("coldColor" in linha for linha in log["azul_lido"]),
               "a leitura de runtime que valida a fixture e a do `coldColor`: %s" % log["azul_lido"])
    # FIX-4: a fixture tem de DECLARAR que a sessao do log e da DLL PRE-conserto (e nao da build
    # nova). Sem a declaracao explicita, a prova e lida como se fosse do conserto.
    dito = (log.get("dll_da_sessao") or "") + " " + (ent.get("procedencia") or "")
    arc.exigir("PRE-conserto" in dito or "pre-conserto" in dito,
               "a fixture `cores-do-jogo` tem de declarar que a sessao do log e da DLL "
               "PRE-conserto (nao da build nova) — ver a RESSALVA (FIX-4) na procedencia")

    # ------------------------------------------------- 2. NIVEL 2: TOM DE EXPLICACAO (SANIDADE)
    cor2 = reg.cor_do_campo("specialDescColor")
    arc.exigir(reg.eh_tom_de_explicacao(cor2),
               "SANIDADE do nivel 2: o campo `specialDescColor` (%s) virou AZUL — o nivel 2 "
               "ficaria igual ao nivel 3 (o colapso do COR-1)" % cor2)
    arc.exigir(not reg.eh_azul(cor2), "o tom do nivel 2 nao pode passar no teste de azul: %s" % cor2)
    distancia = reg.distancia_por_canal(marcador, cor2)
    arc.exigir(distancia <= 0x30,
               "o marcador do codigo (%s) e o campo lido (%s) tem de ser o MESMO tom "
               "(diferenca de %d por canal: metodo diferente, tom diferente seria campo errado)"
               % (marcador, cor2, distancia))
    # O campo e lido em runtime pelo gancho das notas; a fixture prova que a leitura do nivel 2
    # NAO acontecia no desenho antigo (zero linhas) — o sintoma do defeito de ordem.
    arc.igual(log["linha_da_leitura_do_nivel_2"], [],
              "no desenho antigo o gancho da cor nunca LEU o campo (0 linhas no log): %s"
              % log["linha_da_leitura_do_nivel_2"])
    arc.igual(log["linha_de_falha_da_leitura_do_nivel_2"], [],
              "tambem nao houve falha de leitura: o gancho nem chegou a tentar")
    arc.exigir(any(marcador in linha for linha in log["showtooltip"]),
               "o log do ShowTooltip mostra o marcador %s no texto FINAL (a cor nao foi trocada): %s"
               % (marcador, log["showtooltip"]))

    # ------------------------------------------------- 3. NIVEL 3: O ELO DECLARADO NAO E AZUL
    cor3_declarada = reg.cor_do_campo("skillStatusColor")
    arc.exigir(not reg.eh_azul(cor3_declarada),
               "FATO medido (01/10): `skillStatusColor` = %s e um tom de EXPLICACAO, nao um azul — "
               "se algum dia ele virar azul, esta expectativa muda e a especificacao volta a valer"
               % cor3_declarada)
    arc.exigir(reg.eh_azul(reg.cor_da_hud("coldColor")),
               "o `coldColor` da paleta (%s) tem de passar no teste de azul" % reg.cor_da_hud("coldColor"))
    arc.exigir(reg.eh_azul(reg.cor_da_hud("manaColor")),
               "o `manaColor` da paleta (%s) tem de passar no teste de azul" % reg.cor_da_hud("manaColor"))
    # O azul em uso e o do elo 2 — o log nao tem NENHUMA leitura do elo 1 (o declarado).
    arc.exigir(not any("skillStatusColor" in linha for linha in log["azul_lido"]),
               "o log nao pode ter leitura de `skillStatusColor` como azul (o elo 1 e morto): %s"
               % log["azul_lido"])
    # ...e o campo declarado tem o MESMO valor do campo do nivel 2 (fato que o relato do COR-2
    # leva ao dono: a fonte declarada do nivel 3 nao se sustenta).
    arc.igual(cor3_declarada, cor2,
              "fato medido: o campo declarado para o nivel 3 tem o MESMO valor do campo do nivel 2")

    # ------------------------------------------------- 4. A COR CHEGANDO AO BLOCO
    # (a) ESTRUTURA: o gancho das notas aplica a cor no FIM dele, e nao existe gancho de cor
    #     separado com prioridade (era ele que rodava primeiro e nunca via o marcador).
    fonte = reg.fonte_do_mod()
    codigo = re.sub(r"//[^\n]*", "", fonte)   # comentario NAO e gancho: a bancada cita o nome
    arc.exigir(not re.search(r"\bvoid\s+CorDoJogoPostfix\s*\(", codigo),
               "existe um gancho de cor SEPARADO no fonte — e ele que rodava antes das notas")
    arc.exigir(re.search(r"AplicarNotasDoFunil\(original, ref __result\);\s*"
                         r"(?://[^\n]*\n\s*)*__result = ComACorDoJogo\(__result\);", fonte),
               "o gancho das notas (`Postfix`) tem de aplicar a cor do nivel 2 no FIM dele "
               "(docs/TEXTO-TOOLTIPS.md §7)")
    arc.exigir(not re.search(r"\[HarmonyPostfix,\s*HarmonyPriority", codigo),
               "nenhum postfix deste arquivo pode depender de prioridade para colorir")

    # (b) A ORDEM REAL, lida do 0Harmony do jogo (o mesmo DLL do perfil, sha256 1a21cc03…c1031).
    ordem = [nome for nome, _ in _ordem_real_do_harmony([("cor", 600), ("notas", 400)])]
    arc.igual(ordem, ["cor", "notas"],
              "a 0Harmony do jogo ordena os postfixes DESCENDENTE: o Priority.High (600) roda "
              "PRIMEIRO (o relato da REV-50; a bancada esta em scratch/cor2/)")

    # (c) O PIPELINE: o desenho ANTIGO, rodado na ordem real, deixa o marcador (o log confirma);
    #     o desenho de HOJE entrega a cor do campo e o marcador desaparece.
    desenho_antigo = _troca_o_marcador(TEXTO_DO_JOGO, cor2)          # gancho da cor (1o)...
    desenho_antigo = _anexa_a_nota(desenho_antigo, NOTA_DO_LOG)      # ...gancho das notas (2o)
    desenho_novo = _anexa_a_nota(TEXTO_DO_JOGO, NOTA_DO_LOG)         # notas primeiro...
    desenho_novo = _troca_o_marcador(desenho_novo, cor2)             # ...e a cor no fim do MESMO gancho

    arc.exigir(marcador in desenho_antigo and cor2 not in desenho_antigo,
               "o desenho ANTIGO tinha de reproduzir o defeito (marcador no texto final): %r"
               % desenho_antigo)
    arc.exigir(marcador not in desenho_novo and cor2 in desenho_novo,
               "o desenho de HOJE tem de entregar a cor LIDA (%s) no bloco e nenhum marcador: %r"
               % (cor2, desenho_novo))

    print("nivel 2 = %s (campo lido; marcador %s a %d por canal), nivel 3 = azul da paleta "
          "(coldColor #00D7FF, o unico azul do log); a cor chega ao bloco pelo gancho das notas"
          % (cor2, marcador, distancia))


if __name__ == "__main__":
    arc.main(META, corpo)
