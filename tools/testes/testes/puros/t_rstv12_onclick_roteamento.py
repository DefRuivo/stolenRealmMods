#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RSTV-12: o clique dos botoes 'Skills' tem de chegar ao listener do mod, nao ao onClick do prefab.

O QUE ISTO TRAVA
----------------
1. O helper `SelectPartyButton.ClearClickListeners(Button)` existe e TROCA a INSTANCIA do evento
   (`button.onClick = new Button.ButtonClickedEvent();`) — a unica forma de descartar o listener
   PERSISTENTE serializado, que o `RemoveAllListeners()` NAO remove (ele limpa so a lista de runtime;
   e a persistente ainda roda ANTES do nosso, no `InvokableCallList.PrepareInvoke()`).
2. Os dois clones da run — o do HUD (molde `pingBtn`) e o da janela do level-up (molde
   `AcceptButton`) — e tambem o da tela Select Party chamam o helper ANTES de instalar o listener.
3. Nenhum `.cs` do mod cita `RemoveAllListeners()` no codigo efetivo: a classe de defeito esta fechada.
4. O MODELO PURO da invocacao do `UnityEvent` reproduz os dois sintomas do log de 02/10:
     - HUD (persistente `ButtonPressedPing`, que liga o modo ping): com a limpeza ANTIGA o clique
       PINGA e o portao RECUSA a abertura ("abertura RECUSADA — modo de apontar o hex ligado");
     - level-up (persistente `ConfirmLevelUpSelection`, que lanca num clone): com a limpeza ANTIGA o
       clique lanca ANTES do nosso listener (os 11 NullReferenceException), e nada abre.
   Com o conserto (troca da instancia) os DOIS abrem.

DE ONDE VEM O ESPERADO
----------------------
As regras vivem em `tools/testes/regras_rstv12.py`; os fontes sao lidos AO VIVO. A semantica do
`UnityEvent` e transcrita citando o IL do `UnityEngine.CoreModule.dll` deste build
(`InvokableCallList.Clear()` limpa so `m_RuntimeCalls`; `PrepareInvoke()` poe as persistentes antes).
O que NAO se prova aqui (e so o dono confirma, em tela): a arvore ABRIR de fato ao clicar.
"""
import regras_rstv12 as reg

import arcabouco as arc

META = {
    "nome": "rstv12-onclick-roteamento",
    "categoria": "pura",
    "requer": [],
    "descricao": ("RSTV-12: o clique dos botoes 'Skills' (HUD ping e janela do level-up) chega ao "
                  "RunButton.OpenForTarget — a limpeza troca a INSTANCIA do evento para descartar o "
                  "onClick persistente do prefab; o modelo reprova o clique que cai no original"),
}


def corpo():
    src_run = reg.fonte(reg.caminho_run())
    src_janela = reg.fonte(reg.caminho_janela())
    src_select = reg.fonte(reg.caminho_select())
    arc.exigir(len(src_run) > 3000 and len(src_janela) > 3000 and len(src_select) > 3000,
               "os fontes vieram vazios/curtos: a leitura mudou de lugar?")

    # 1) O FONTE esta de pe: helper correto + os clones limpando ANTES de instalar o listener +
    #    nenhum `RemoveAllListeners()` no mod.
    falhas = reg.falhas_do_roteamento(src_run, src_janela, src_select, reg.fontes_do_mod())
    arc.exigir(not falhas, "o roteamento do clique regrediu em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))

    # 2) SANIDADE DO MODELO: os dois perfis existem e o persistente de cada um e o handler certo.
    perfis = reg.perfis()
    arc.igual(len(perfis), 2, "o modelo tem de cobrir os DOIS botoes 'Skills' da run")
    nomes = sorted(p["persistente"] for p in perfis)
    arc.igual(nomes, sorted([reg.PING, reg.CONFIRM]),
              "os persistente modelados tem de ser o ButtonPressedPing e o ConfirmLevelUpSelection")
    arc.exigir(any(p["lanca"] for p in perfis) and any(p["mexe_no_portao"] for p in perfis),
               "o modelo perdeu os DOIS sintomas (um persistente lanca, o outro liga o modo ping)")

    # 3) O DEFEITO REPRODUZIDO (o clique cai no original) x O CONSERTO (abre a arvore), perfil a perfil.
    esperado_defeito = {reg.PING: "pingou", reg.CONFIRM: "levelup-nre"}
    for perfil in perfis:
        antigo = reg.resultado_do_clique(reg.LIMPEZA_ANTIGA, perfil)
        novo = reg.resultado_do_clique(reg.LIMPEZA_NOVA, perfil)
        arc.igual(antigo, esperado_defeito[perfil["persistente"]],
                  "com a limpeza ANTIGA (%s) o clique em '%s' NAO pode abrir — tem de cair no "
                  "handler original do prefab" % (perfil["nome"], reg.NOSSO))
        arc.igual(novo, "abriu",
                  "com a limpeza NOVA (%s) o clique tem de chegar ao %s" % (perfil["nome"], reg.NOSSO))
        arc.exigir(antigo != novo,
                   "inconsistencia do modelo: o defeito e o conserto dao o MESMO resultado em '%s'"
                   % perfil["nome"])

    # O aborto do `Invoke()` no throw: o NOSSO listener nem aparece na varredura do level-up.
    executadas = reg.chamadas_do_clique(reg.LIMPEZA_ANTIGA, reg.PERFIL_ACCEPT)
    arc.exigir(reg.NOSSO not in executadas,
               "no defeito do level-up o listener do mod ainda e invocado — o modelo nao reproduz o "
               "aborto do UnityEvent num handler que lanca")
    arc.igual(reg.chamadas_do_clique(reg.LIMPEZA_ANTIGA, reg.PERFIL_PING),
              [reg.PING, reg.NOSSO],
              "o persistente tem de rodar ANTES do nosso (PrepareInvoke: persistentes primeiro)")

    # 4) PROVA DE FOGO EMBUTIDA — com o defeito plantado em MEMORIA, a MESMA checagem reprova.
    antigo_run = reg.fonte_com_limpeza_antiga(src_run)
    arc.exigir(antigo_run != src_run,
               "o plantio 'limpeza antiga' nao encontrou a ancora no RunButton (a checagem le o "
               "trecho certo?)")
    falhas_run = reg.falhas_do_roteamento(antigo_run, src_janela, src_select)
    arc.exigir(any("RemoveAllListeners" in f for f in falhas_run),
               "com a limpeza antiga no RunButton as checagens NAO reprovaram pelo motivo certo: %s"
               % " | ".join(falhas_run))

    antigo_janela = reg.fonte_com_limpeza_antiga(src_janela)
    arc.exigir(antigo_janela != src_janela,
               "o plantio 'limpeza antiga' nao encontrou a ancora no LevelUpWindowButton")
    falhas_janela = reg.falhas_do_roteamento(src_run, antigo_janela, src_select)
    arc.exigir(any("RemoveAllListeners" in f or "ClearClickListeners" in f for f in falhas_janela),
               "com a limpeza antiga na janela as checagens NAO reprovaram pelo motivo certo: %s"
               % " | ".join(falhas_janela))

    helper_antigo = reg.fonte_com_helper_antigo(src_select)
    arc.exigir(helper_antigo != src_select,
               "o plantio 'helper antigo' nao encontrou a ancora em SelectPartyButton")
    falhas_helper = reg.falhas_do_roteamento(src_run, src_janela, helper_antigo)
    arc.exigir(any("instancia" in f or "RemoveAllListeners" in f for f in falhas_helper),
               "com o helper voltando a `RemoveAllListeners()` as checagens NAO reprovaram pelo "
               "motivo certo: %s" % " | ".join(falhas_helper))

    print("roteamento do clique: os clones trocam a instancia do evento (descartam o onClick "
          "persistente); o modelo reprova o clique que cai no original (pingou / levelup-nre) e "
          "aprova o conserto (abriu)")


if __name__ == "__main__":
    arc.main(META, corpo)
