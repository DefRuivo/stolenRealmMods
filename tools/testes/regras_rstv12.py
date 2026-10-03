#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rstv12.py - RSTV-12: o CLIQUE do botao 'Skills' tem de chegar ao mod, nunca ao onClick
SERIALIZADO do botao molde.

O DEFEITO QUE ESTA BIBLIOTECA TRAVA (log de 02/10, evidencia)
-------------------------------------------------------------
O botao 'Skills' do HUD (clone do `CurrentCharacterUI.pingBtn`) ficava "VISIVEL e clicavel" e, ao
clicar, PINGAVA; e o botao 'Skills' de dentro da janela do level-up (clone do `RoguelikeManager.
AcceptButton`) disparava `ConfirmLevelUpSelection` (11 NullReferenceException). Nos dois casos o
listener do mod (`RunButton.OpenForTarget`) nao abria a arvore.

A causa NAO e sobreposicao/raycast (o log mostra o NOSSO `OpenForTarget` sendo chamado no clone do
HUD: "RSTV-5: abertura RECUSADA — modo de apontar o hex ligado"). A causa e o `Button.onClick`
PERSISTENTE herdado pelo `Instantiate`:

  * `UnityEvent` guarda DUAS listas (`UnityEngine.Events.InvokableCallList`, lido do
    `UnityEngine.CoreModule.dll` DESTE build):
        - `m_PersistentCalls`  -> os listeners GRAVADOS no prefab (o `ButtonPressedPing` do Ping
          Button e o `ConfirmLevelUpSelection` do Accept Button);
        - `m_RuntimeCalls`     -> os de script, como o nosso (`AddListener`).
  * `UnityEventBase.RemoveAllListeners()` chama `m_Calls.Clear()`, e esse `Clear()` esvazia SO a
    `m_RuntimeCalls` — a persistente CONTINUA na instancia;
  * `InvokableCallList.PrepareInvoke()` concatena as PERSISTENTES **antes** das de runtime. Logo o
    listener do jogo roda PRIMEIRO e, se ele lancar (o `ConfirmLevelUpSelection` estoura num clone),
    o `UnityEvent.Invoke()` ABORTA a varredura e o NOSSO listener nem chega a rodar — o stack do log
    (`ConfirmLevelUpSelection -> InvokableCall.Invoke -> UnityEvent.Invoke -> Button.Press`).

O CONSERTO (RSTV-12): trocar a INSTANCIA do evento antes de instalar o nosso listener —
`button.onClick = new Button.ButtonClickedEvent();` (`Button.onClick` tem setter publico; a instancia
nova nasce SEM nenhuma persistente). O helper e `SelectPartyButton.ClearClickListeners(Button)`.

O QUE ESTAS REGRAS TRAVAM
-------------------------
1. o helper `ClearClickListeners` existe, TROCA a instancia do evento e NAO usa `RemoveAllListeners()`;
2. os dois clones da run (HUD e janela do level-up) — e o da tela Select Party — chamam o helper e
   NUNCA instalam o listener antes de limpar;
3. nenhum `.cs` do mod usa `RemoveAllListeners()` no CODIGO EFETIVO (a classe de defeito esta fechada);
4. o MODELO PURO da invocacao do `UnityEvent` reproduz o clique que cai no original: com a limpeza
   ANTIGA os dois botoes NAO abrem (um pinga, o outro lanca), e com a limpeza NOVA os dois abrem.

COMO O ESPERADO E OBTIDO
------------------------
Os fontes sao lidos AO VIVO (`RoguelikeSkillTreeVisualizer/{RunButton,LevelUpWindowButton,
SelectPartyButton}.cs`). Os CORPOS de metodo saem por casamento de chaves (`recorte.corpo_do_metodo`)
e a checagem usa o texto SEM comentario (`recorte.codigo_efetivo`): uma citacao num comentario nao e
codigo. A semantica do `UnityEvent` (duas listas, ordem persistente-antes-de-runtime, aborto no
throw) e transcrita no `chamadas_do_clique`/`resultado_do_clique` citando o IL deste build.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import recorte as rec

# Assinaturas/trechos exatos lidos do fonte. Se um nome mudar, a checagem REPROVA dizendo qual sumiu.
HELPER = "internal static void ClearClickListeners(Button button)"
CHAMADA_HELPER = "SelectPartyButton.ClearClickListeners(button)"
TROCA_INSTANCIA = "button.onClick = new Button.ButtonClickedEvent();"
ANTIGO = "RemoveAllListeners()"

ENSURE_INTERNAL_RUN = "private static void EnsureInternal(CurrentCharacterUI ui)"
ENSURE_INTERNAL_JANELA = "private static void EnsureInternal(RoguelikeManager rok)"
ENSURE_PARTY = "internal static void Ensure(CharacterChoiceManager manager)"

# Handlers do clique, por identidade: o PERSISTENTE que o prefab traz e o listener do MOD.
PING = "ButtonPressedPing"
CONFIRM = "ConfirmLevelUpSelection"
NOSSO = "RunButton.OpenForTarget"

# Mecanismos de limpeza comparados pelo modelo.
LIMPEZA_ANTIGA = "RemoveAllListeners"      # limpa so a lista de runtime (o defeito)
LIMPEZA_NOVA = "troca-da-instancia"        # descarta a persistente junto com a instancia (RSTV-12)

# Perfis: cada botao 'Skills' que existe hoje. `lanca` = o handler persistente estoura no clone
# (ConfirmLevelUpSelection: log de 02/10, 11 NullReferenceException). `mexe_no_portao` = a
# persistente liga o modo ping, e o portao da run entao RECUSA a abertura.
PERFIL_PING = {
    "nome": "HUD (clone do Ping Button)",
    "persistente": PING,
    "lanca": False,
    "mexe_no_portao": True,
}
PERFIL_ACCEPT = {
    "nome": "janela do level-up (clone do AcceptButton)",
    "persistente": CONFIRM,
    "lanca": True,
    "mexe_no_portao": False,
}


def perfis():
    """Os botoes 'Skills' cobertos pelo modelo (fonte unica do nome dos perfis)."""
    return (PERFIL_PING, PERFIL_ACCEPT)


# --------------------------------------------------------------- modelo puro ---

def chamadas_do_clique(limpeza, perfil):
    """Os handlers que um `UnityEvent.Invoke()` executaria num clique do clone, NA ORDEM.

    Transcricao do motor (IL deste build):
      - `PrepareInvoke()` = persistentes PRIMEIRO, runtime depois;
      - `LIMPEZA_ANTIGA` (RemoveAllListeners) deixa a persistente na lista e zera a de runtime, que
        o proprio codigo recompensa com o NOSSO `AddListener`;
      - `LIMPEZA_NOVA` (troca da instancia) nasce sem persistente nenhuma;
      - `UnityEvent.Invoke()` NAO tem try/catch: um handler que lanca ABORTA a varredura.
    """
    persistentes = [perfil["persistente"]] if limpeza == LIMPEZA_ANTIGA else []
    runtime = [NOSSO]

    executadas = []
    for handler in persistentes + runtime:
        executadas.append(handler)
        if handler == perfil["persistente"] and perfil["lanca"]:
            break
    return executadas


def resultado_do_clique(limpeza, perfil):
    """O que o jogador ve no clique: 'pingou', 'levelup-nre' ou 'abriu'.

    'pingou'      -> a persistente (Ping) ligou o modo ping e o portao da run RECUSOU abrir
                     (log de 02/10: "abertura RECUSADA — modo de apontar o hex ligado");
    'levelup-nre' -> a persistente (Confirm) lancou ANTES do nosso, que nunca rodou (o NRE do log);
    'abriu'       -> so o NOSSO listener rodou -> `RunButton.OpenForTarget()` abre a arvore.
    """
    executadas = chamadas_do_clique(limpeza, perfil)
    persistente_rodou = perfil["persistente"] in executadas

    if perfil["lanca"] and persistente_rodou:
        return "levelup-nre"
    if perfil["mexe_no_portao"] and persistente_rodou:
        return "pingou"
    if NOSSO in executadas:
        return "abriu"
    return "nao-abriu"


# ------------------------------------------------------------------ caminhos ---

def _dir_mod():
    return os.path.join(arc.raiz_do_repo(), "RoguelikeSkillTreeVisualizer")


def caminho_run():
    return os.path.join(_dir_mod(), "RunButton.cs")


def caminho_janela():
    return os.path.join(_dir_mod(), "LevelUpWindowButton.cs")


def caminho_select():
    return os.path.join(_dir_mod(), "SelectPartyButton.cs")


def fonte(caminho):
    """O fonte vivo do mod (nao uma copia: a expectativa fica amarrada ao que sera compilado)."""
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def _efetivo(src):
    return rec.codigo_efetivo(src)


def _corpo(src, assinatura):
    return rec.corpo_do_metodo(_efetivo(src), assinatura)


# ------------------------------------------------------------------ checagens ---

def _clone_com_limpeza(src, assinatura, nome):
    """Checa UM clone: limpa a instancia do evento ANTES de instalar o nosso listener."""
    falhas = []
    interno = _corpo(src, assinatura)
    if interno is None:
        return ["nao achei %s no %s.cs" % (assinatura, nome)]

    if "ClearClickListeners(button)" not in interno:
        falhas.append("%s nao chama `ClearClickListeners(button)` — o onClick SERIALIZADO do "
                      "prefab (persistente) sobrevive no clone" % nome)
    if ANTIGO in interno:
        falhas.append("%s usa `RemoveAllListeners()`: ele esvazia so a lista de runtime e NAO o "
                      "listener persistente do prefab (RSTV-12 exige a troca da instancia do evento)"
                      % nome)

    i_limpa = interno.find("ClearClickListeners(button)")
    i_add = interno.find(".onClick.AddListener")
    if i_limpa < 0 or i_add < 0:
        if i_add < 0:
            falhas.append("%s nao instala o listener do mod (`.onClick.AddListener`)" % nome)
    elif i_limpa > i_add:
        falhas.append("%s instala o listener ANTES de limpar o evento — o persistente sobrevive" % nome)

    return falhas


def falhas_do_roteamento(src_run, src_janela, src_select, fontes_do_mod=None):
    """Defeitos do roteamento do clique. Lista vazia = o conserto esta de pe."""
    falhas = []

    # ---------------------------------------- 1) o helper existe e TROCA a instancia do evento
    helper = _corpo(src_select, HELPER)
    if helper is None:
        falhas.append("nao achei %s em SelectPartyButton.cs (a limpeza do evento nao existe)" % HELPER)
    else:
        if TROCA_INSTANCIA not in helper:
            falhas.append("ClearClickListeners nao troca a INSTANCIA do evento (falta `%s`) — "
                          "`RemoveAllListeners()` nao descarta o listener persistente" % TROCA_INSTANCIA)
        if ANTIGO in helper:
            falhas.append("ClearClickListeners usa `RemoveAllListeners()` — ele limpa so a lista de "
                          "runtime, nao o listener persistente do prefab")

    # ---------------------------------------- 2) os clones limpam ANTES de instalar o listener
    falhas += _clone_com_limpeza(src_run, ENSURE_INTERNAL_RUN, "RunButton")
    falhas += _clone_com_limpeza(src_janela, ENSURE_INTERNAL_JANELA, "LevelUpWindowButton")
    falhas += _clone_com_limpeza(src_select, ENSURE_PARTY, "SelectPartyButton")

    # ---------------------------------------- 3) a CLASSE de defeito esta fechada no mod inteiro
    for caminho, texto in (fontes_do_mod or {}).items():
        if "RemoveAllListeners()" in _efetivo(texto):
            falhas.append("%s ainda usa `RemoveAllListeners()` no codigo efetivo — a classe do "
                          "defeito nao esta fechada (RSTV-12)" % os.path.basename(caminho))

    return falhas


def fontes_do_mod():
    """Todos os `.cs` do mod (a varredura de classe: nenhum pode citar `RemoveAllListeners()`)."""
    pasta = _dir_mod()
    return {os.path.join(pasta, nome): fonte(os.path.join(pasta, nome))
            for nome in sorted(os.listdir(pasta)) if nome.endswith(".cs")}


# ------------------------------------------------------------ plantio do defeito ---

_ANCORA_CHAMADA = "SelectPartyButton.ClearClickListeners(button);"
_DEFEITO_CHAMADA = "button.onClick.RemoveAllListeners();"


def fonte_com_limpeza_antiga(src):
    """O MESMO fonte do clone com a limpeza ANTIGA (so `RemoveAllListeners()`), em memoria.

    Nao mexe em arquivo nenhum: e a isca (`cp_rstv12_...py`) que prova que as checagens reprovam.
    """
    if _ANCORA_CHAMADA not in src:
        return src
    return src.replace(_ANCORA_CHAMADA, _DEFEITO_CHAMADA)


def fonte_com_helper_antigo(src):
    """O MESMO SelectPartyButton.cs com o helper voltando a `RemoveAllListeners()`, em memoria."""
    if TROCA_INSTANCIA not in src:
        return src
    return src.replace(TROCA_INSTANCIA, "button.onClick.RemoveAllListeners();")
