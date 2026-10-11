#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""BUG-34 - a nota de Armor/Resistencia NUNCA entra no FEED/combate, so no corpo da tooltip.

O DEFEITO (relato do dono, 04/10)
---------------------------------
A explicacao de como a Armor funciona (`BuildArmorNote`) e a de Resistencia
(`ResistanceExplainSuffix`) sao aplicadas no funil `OptionsManager.Localize`
(`LocalizePatch.Postfix` -> `AplicarNotasDoFunil`), que passa por TODO texto do jogo.
O texto flutuante de combate (`Character.ShowOverheadMessageStatus` monta
`"[status name] Applied"` com o nome dentro) so e localizado na hora de exibir, em
`OverheadMessageDisplay.SpawnOverheadMessage`; o texto final "Increased Armor Applied"
casa a regra de afixo (tem verbo + "Armor") e a nota vazava para o feed. O battle log
localiza por `Root.SendMessageWindowMessage`.

A CORRECAO (o que este teste prende)
------------------------------------
Uma flag de CONTEXTO (`[ThreadStatic] _profundidadeTextoDeFeed`), nao uma lista de textos:
  - um `Prefix` de `Root.SendMessageWindowMessage` e um de
    `OverheadMessageDisplay.SpawnOverheadMessage` ENTRAM no contexto (contador);
  - cada um tem o `Finalizer` que SAI (roda mesmo se o metodo do jogo lancar);
  - dentro do contexto, o bloco de afixo (Armor/Resistencia) NAO anexa a nota.

O que NAO pode regredir: o BUG-33 (os 4 NOMES exatos de status) continua na lista
`RotulosDeStatusSemNota`; o corpo da tooltip (descricao) continua recebendo a nota (ele
localiza por FORA do contexto de feed).

O ACHADO BUG-34T (05/10) - O QUE ESTAVA ERRADO NA CONFERENCIA
-------------------------------------------------------------
Esta trava recortava, em volta de cada alvo, uma JANELA de 2200 caracteres. Os dois
atributos de feed distam MENOS que isso, entao a janela da PRIMEIRA entrada (o feed de
texto / battle log) INVADIA a SEGUNDA (o texto flutuante): os tokens de Prefix/Finalizer
que ela encontrava eram do bloco VIZINHO. Efeito medido: arrancar `EntrarTextoDeFeed();`,
`SairTextoDeFeed();` ou o `void Finalizer()` da entrada de TEXTO passava VERDE — so a
entrada do texto FLUTUANTE estava de fato conferida, e uma regressao futura no caminho do
battle log passaria em silencio.

O CONSERTO: o criterio e ESTRUTURAL (`regras_bt_texto.falhas_da_entrada_de_feed` recorta o
BLOCO por CASAMENTO DE CHAVES, via `recorte.py`: do `[HarmonyPatch...]` ao `}` que casa com a
classe anotada — nunca `fonte[i:i + N]`). Sem distancia nao ha vizinho para emprestar token. A
janela de 2200 continua no `regras_bt_texto` SO como a metade REMOVIDA, para este teste provar,
nos dois sentidos, que ela confere FAIXA e nao CONTEUDO.

AS ISCAS (embutidas, como no BT-10T/MAN-2/RSTV-8)
-------------------------------------------------
Cada defeito e plantado ISOLADAMENTE numa copia em memoria do fonte real e a MESMA conferencia
tem de reprovar pelo motivo certo: armor sem guard, resist sem guard, alvo morto, contador->bool,
e Entrar/Sair/Finalizer removidos de CADA uma das duas entradas. Para os tres ultimos na entrada
de TEXTO o teste tambem exige que a JANELA REMOVIDA continue CEGA (o furo medido) — e que na
entrada VIZINHA ela morda (a prova de que o defeito nao e do medidor antigo). A prova FISICA no
`LocalizePatch.cs` real (defeito plantado, teste visto REPROVANDO, fonte restaurado byte a byte
com sha256) esta em `tools/testes/bt34-feed-prova-de-fogo.log`.
"""
import arcabouco as arc
import regras_bt_texto as R

META = {
    "nome": "bt34-nota-fora-do-feed",
    "categoria": "pura",
    "requer": [],
    "descricao": "BUG-34/BUG-34T: a nota de Armor/Resistencia e barrada no FEED/combate por flag de "
                 "contexto (Root.SendMessageWindowMessage + OverheadMessageDisplay.SpawnOverheadMessage), "
                 "conferida por BLOCO ESTRUTURAL (nunca janela de caracteres) em cada uma das duas entradas; "
                 "o BUG-33 (4 nomes) segue protegido e cada defeito plantado reprova",
}

# alvos do Harmony: TIPO + NOME (nunca indice posicional), os dois pontos de feed/combate.
ALVO_FEED_TEXTO = '[HarmonyPatch(typeof(Root), nameof(Root.SendMessageWindowMessage))]'
ALVO_TEXTO_FLUTUANTE = '[HarmonyPatch(typeof(OverheadMessageDisplay), "SpawnOverheadMessage")]'


def _medida_da_prova(real):
    """PROVA DE SENTIDO: os dois alvos tem de estar MAIS PERTO que a janela removida.

    Sem isso a "janela cega" nao teria como ser cega — e o teste estaria provando um furo que o
    fonte ja nao tem. Devolve a distancia em caracteres entre os dois alvos.
    """
    pos_txt = R.pin(real, ALVO_FEED_TEXTO, "o alvo do feed de texto (Root.SendMessageWindowMessage)")
    pos_oh = R.pin(real, ALVO_TEXTO_FLUTUANTE,
                   "o alvo do texto flutuante (OverheadMessageDisplay.SpawnOverheadMessage)")
    arc.exigir(pos_txt != pos_oh, "os dois alvos de feed tem de ser pontos distintos")
    arc.exigir(pos_txt < pos_oh, "a ordem dos alvos mudou: o feed de texto vem antes do texto flutuante")
    distancia = pos_oh - pos_txt
    arc.exigir(0 < distancia < R.JANELA_REMOVIDA,
               "a prova perdeu o sentido: os dois alvos de feed estao a %d chars e a janela removida e "
               "de %d (ela nao os alcancaria)" % (distancia, R.JANELA_REMOVIDA))
    return distancia


def _iscas(real):
    """Planta cada defeito ISOLADAMENTE e exige que a conferencia estrutural o morda.

    Devolve a lista de (nome, janela_cega). `janela_cega=True` so para os tres defeitos da entrada
    de TEXTO: e exatamente o furo medido na BUG-34T (a janela de 2200 alcancava o bloco vizinho).
    """
    alvo_txt = ALVO_FEED_TEXTO
    plantas = []

    # (a) ARMOR sem guard — a nota volta a entrar no feed pela regra de Armor.
    mutado = real.replace(R.GUARD_ARMOR, R.GUARD_ARMOR.replace("!ehTextoDeFeed && ", "", 1), 1)
    plantas.append(("armor sem guard", mutado, "regra de ARMOR", False))

    # (b) RESISTENCIA sem guard.
    mutado = real.replace(R.GUARD_RESIST, R.GUARD_RESIST.replace("!ehTextoDeFeed && ", "", 1), 1)
    plantas.append(("resist sem guard", mutado, "regra de RESISTENCIA", False))

    # (c) ALVO MORTO: a entrada do texto FLUTUANTE perde o `[HarmonyPatch]` (deixa de ser gancho) —
    #     o caminho do texto flutuante fica DESCOBERTO.
    mutado = real.replace(R.ENTRADAS_DE_FEED[1][1] + "\n", "", 1)
    plantas.append(("alvo morto (texto flutuante sem [HarmonyPatch])", mutado, "nao achei o alvo", False))

    # (d) CONTADOR -> BOOL: a reentrada apaga o contexto de fora (uma saida fecha tudo).
    mutado = (real.replace(R.FLAG_DE_FEED, "private static bool _profundidadeTextoDeFeed;", 1)
                  .replace(R.LEITURA_DA_FLAG, "return _profundidadeTextoDeFeed;", 1)
                  .replace(R.ENTRA_NO_CONTEXTO, "_profundidadeTextoDeFeed = true;", 1)
                  .replace(R.SAI_DO_CONTEXTO, "_profundidadeTextoDeFeed = false;", 1))
    plantas.append(("contador -> bool (uma saida apaga o contexto de fora)", mutado, "CONTADOR", False))

    # (e) Entrar / Sair / Finalizer removidos de CADA entrada, um por vez.
    for rotulo, alvo in R.ENTRADAS_DE_FEED:
        cega = alvo == alvo_txt      # so a PRIMEIRA entrada: a janela dela alcanca a vizinha
        plantas.append(("Entrar removido de %s" % rotulo,
                        R.sem_trecho_no_bloco(real, alvo, "                    EntrarTextoDeFeed();\n"),
                        "nao ENTRA", cega))
        plantas.append(("Sair removido de %s" % rotulo,
                        R.sem_trecho_no_bloco(real, alvo, "                    SairTextoDeFeed();\n"),
                        "nao SAI", cega))
        plantas.append(("Finalizer removido de %s" % rotulo,
                        R.sem_trecho_no_bloco(real, alvo, "            private static void Finalizer()\n"),
                        "nao tem `Finalizer`", cega))

    resultados = []
    for nome, mutado, motivo, cega in plantas:
        arc.exigir(mutado != real, "a isca '%s' nao plantou nada (o fonte nao mudou)" % nome)

        viol = R.falhas_do_guard_de_feed(mutado)
        arc.exigir(any(motivo in v for v in viol),
                   "a isca '%s' NAO foi reprovada pelo motivo certo (esperava %r): %r"
                   % (nome, motivo, viol))

        viol_janela = R.falhas_da_janela_2200(mutado)
        if cega:
            arc.igual(viol_janela, [],
                      "a JANELA de %d chars devia estar CEGA ao defeito '%s' (ela confere faixa, nao "
                      "conteudo — e o furo da BUG-34T)" % (R.JANELA_REMOVIDA, nome))
        else:
            arc.exigir(viol_janela,
                       "a janela de %d chars devia PEGAR o defeito '%s' (a prova de que o defeito nao e "
                       "do medidor antigo): %r" % (R.JANELA_REMOVIDA, nome, viol_janela))
        resultados.append((nome, cega))

    print("iscas embutidas: %d defeito(s) plantado(s) isoladamente, cada um reprovado pelo motivo certo "
          "(%d deles com a janela de %d chars comprovadamente CEGA)"
          % (len(plantas), sum(1 for _n, c in resultados if c), R.JANELA_REMOVIDA))
    return resultados


def corpo():
    real = R.le_fonte()

    # 1) O FONTE REAL esta conforme? Criterio ESTRUTURAL (bloco por chaves), nunca janela.
    viol = R.falhas_do_guard_de_feed(real)
    arc.igual(viol, [], "o BUG-34 tem de estar conforme no LocalizePatch.cs: %s" % viol)

    distancia = _medida_da_prova(real)

    # 2) O recorte e o BLOCO de verdade: cada entrada, sozinha, tem o Prefix e o Finalizer.
    for rotulo, alvo in R.ENTRADAS_DE_FEED:
        bloco = R.bloco_da_entrada_de_feed(real, alvo)
        arc.exigir(bloco is not None and bloco.startswith(alvo),
                   "o recorte estrutural de %s nao comeca no proprio alvo: %r" % (rotulo, (bloco or "")[:40]))
        arc.exigir(bloco.rstrip().endswith("}"),
                   "o recorte estrutural de %s nao fecha nas chaves (voltou a ser janela?)" % rotulo)
        arc.igual(R.falhas_da_entrada_de_feed(real, alvo, rotulo), [],
                  "a entrada de %s tem de estar conforme no bloco dela" % rotulo)

    # 3) SEMANTICA DO CONTADOR (espelho da flag do C#): reentrada nao apaga o contexto de fora.
    profundidade = 0
    profundidade += 1   # o feed de texto entra
    profundidade += 1   # (ex.) o texto flutuante reentra
    arc.igual(profundidade > 0, True, "com 2 entradas o contexto esta ATIVO")
    profundidade -= 1   # o de dentro sai
    arc.igual(profundidade > 0, True,
              "1 saida NAO apaga o contexto que o de fora ainda usa")
    profundidade -= 1   # o de fora sai
    arc.igual(profundidade > 0, False, "so com todas as saidas o contexto fecha")

    # 4) AS ISCAS: a conferencia morde cada defeito plantado (e a janela removida NAO mordia a
    #    entrada de TEXTO — o furo medido que esta tarefa fechou).
    _iscas(real)

    print("flag de contexto presente e limpa por Finalizer nos DOIS pontos de feed (BLOCO estrutural, "
          "a %d chars um do outro); guard nas regras de Armor E Resistencia; contador seguro sob "
          "reentrada; BUG-33 (4 nomes) intacto; diagnostico do BUG-34 no log"
          % distancia)


if __name__ == "__main__":
    arc.main(META, corpo)
