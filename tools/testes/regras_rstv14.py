#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rstv14.py - RSTV-14: o CICLO DE VIDA do botao DENTRO da janela do level-up.

O DEFEITO QUE ESTA BIBLIOTECA TRAVA
-----------------------------------
O dono relatou os sintomas (3) e (6):

  * (3) "o botao fica voando no 'level up attributes' em vez de sumir" — o `LevelUpWindowButton` e
    criado SO no postfix de `RoguelikeManager.OpenSkillSelectWindow`. Depois disso o jogo troca o
    estagio SEM fechar a janela: `CurLevelUpStage` (l.168697) liga/desliga as secoes
    (`SkillSection`/`ItemSectionInventory`/`AttributeSection`) e o painel `Content` muda de metragem,
    mas o `SkillSelectWindow` continua ativo. O clone (filho dela) continuava VISIVEL no estagio de
    ATRIBUTOS, preso ao canto ANTIGO do painel — "voando".
  * (6) "aperto Skills e o botao some": e o portao reagindo a "janela aberta" enquanto a arvore
    read-only esta aberta (o flapping tratado na RSTV-5); o que esta biblioteca trava e que o botao
    VOLTE quando a arvore fechar — a sessao sai de `UIWindowManager.OpenedWindows` no `Close()`
    (`SkillTreeReadOnly.UnregisterAsOpenWindow`, chamado em l.742 do fonte), entao `AnyUIWindowOpen`
    volta a False e o `RunButton.Mirror` mostra o botao de novo.

O CONSERTO (o que estas regras travam)
--------------------------------------
1. `LevelUpWindowButton.Refresh()` existe: mostra o clone SO com a JANELA ATIVA, da MESMA instancia,
   no estagio `LevelUpStage.Skills`; nos outros estagios ele some (`SetActive(false)`).
2. Ao VOLTAR ao estagio de skills ele RE-ANCORA no canto atual do `Content` (`AnchorToContentCorner`),
   porque o painel pode ter mudado de metragem no meio do ciclo — sem isso ele "voa".
3. `Ensure` chama `Refresh()` no fim (o caminho idempotente da 2a chamada — proximo personagem da
   fila — reafirma a visibilidade em vez de recriar o botao) e NAO injeta fora de hora: exige a
   janela ATIVA (`if (!janela.activeSelf)`).
4. `RstvHost.Update` chama `LevelUpWindowButton.Refresh()` a cada quadro.

COMO O ESPERADO E OBTIDO
------------------------
Os fontes sao lidos AO VIVO (`RoguelikeSkillTreeVisualizer/{LevelUpWindowButton,RstvHost}.cs`). Os
plantios de defeito (`fonte_sem_refresh_no_host`, `fonte_refresh_sem_estagio`) devolvem o MESMO texto
com o defeito reinjetado, em memoria — e a isca (`cp_rstv14_...py`) que prova que as checagens
reprovam de verdade.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import recorte as rec

# Assinaturas exatas lidas do fonte. Se um nome mudar, a checagem REPROVA dizendo qual sumiu.
REFRESH = "internal static void Refresh()"
ENSURE = "internal static void Ensure(RoguelikeManager rok)"
UPDATE_HOST = "private void Update()"

# Trechos que PROVAM o conserto no corpo do `Refresh`.
MARCAS_DO_REFRESH = (
    ("SkillSelectWindow", "a janela de origem (`rok.SkillSelectWindow == janela`)"),
    ("activeSelf", "o estado da JANELA (`janela.activeSelf`)"),
    ("CurLevelUpStage", "o estagio corrente (`rok.CurLevelUpStage`)"),
    ("LevelUpStage.Skills", "o estagio de SKILLS (`LevelUpStage.Skills`)"),
    ("SetActive(mostrar)", "o liga/desliga do clone (`SetActive(mostrar)`)"),
    ("AnchorToContentCorner", "a RE-ANCORAGEM ao voltar ao estagio de skills"),
)

# A guarda de "nao injetar fora de hora": so cria com a janela ATIVA.
GUARDA_JANELA_ATIVA = "if (!janela.activeSelf)"

# A chamada do host.
CHAMADA_NO_HOST = "LevelUpWindowButton.Refresh()"


# ------------------------------------------------------------------ caminhos ---

def _dir_mod():
    return os.path.join(arc.raiz_do_repo(), "RoguelikeSkillTreeVisualizer")


def caminho_janela():
    return os.path.join(_dir_mod(), "LevelUpWindowButton.cs")


def caminho_host():
    return os.path.join(_dir_mod(), "RstvHost.cs")


def caminho_leitura():
    return os.path.join(_dir_mod(), "SkillTreeReadOnly.cs")


def fonte(caminho):
    """O fonte vivo do mod (nao uma copia: a expectativa fica amarrada ao que sera compilado)."""
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def _corpo(src, assinatura):
    return rec.corpo_do_metodo(rec.codigo_efetivo(src), assinatura)


def _corpo_ou_none(src, assinatura):
    try:
        return _corpo(src, assinatura)
    except arc.Falhou:
        return None


# ------------------------------------------------------------------ modelo puro ---
# O ciclo: `janela_ativa`/`mesma_janela`/`estagio` decidem se o clone APARECE. O estagio so importa
# quando a janela esta no ar (fora dela o clone e filho de um GO inativo — some junto).

ESTAGIOS = ("skills", "items", "attributes", "currency")

CENARIO = {
    "janela_ativa": True,
    "mesma_janela": True,
    "estagio": "skills",
}


def mostrar(m):
    """A regra IMPLEMENTADA: o clone aparece SO com a janela ativa, da mesma instancia, em SKILLS."""
    return m["janela_ativa"] and m["mesma_janela"] and m["estagio"] == "skills"


def mostrar_sem_estagio(m):
    """O DEFEITO (pre-RSTV-14): o clone so olha a janela — fica VISIVEL no estagio de atributos."""
    return m["janela_ativa"] and m["mesma_janela"]


def campos_do_ciclo():
    """As chaves do cenario (fonte unica do nome dos campos)."""
    return list(CENARIO.keys())


# ------------------------------------------------------------------ checagens ---

def falhas_do_ciclo(src_janela, src_host):
    """Defeitos do ciclo de vida do botao da janela. Lista vazia = o conserto esta de pe."""
    falhas = []

    refresh = _corpo_ou_none(src_janela, REFRESH)
    if refresh is None:
        return ["nao achei %s no LevelUpWindowButton.cs — sem ele o botao nao reavalia o estagio "
                "(o defeito 'voando no level-up attributes')" % REFRESH]

    # 1) O Refresh decide pela JANELA + ESTAGIO e liga/desliga o clone.
    for trecho, rotulo in MARCAS_DO_REFRESH:
        if trecho not in refresh:
            falhas.append("o Refresh nao leva em conta %s (trecho %r)" % (rotulo, trecho))

    # 2) A guarda de null (fake null da Unity): sem ela, um clone morto estoura no acesso.
    for trecho, rotulo in (("botao == null", "o clone nulo"), ("janela == null", "a janela nula")):
        if trecho not in refresh:
            falhas.append("o Refresh nao tem a guarda de %s (trecho %r)" % (rotulo, trecho))

    # 3) O Ensure REAFIRMA a visibilidade (chama o Refresh) — a 2a chamada na mesma janela e no-op
    #    do clone, mas PRECISA reafirmar a visibilidade (o estagio pode ter voltado ao skills).
    ensure = _corpo_ou_none(src_janela, ENSURE)
    if ensure is None:
        falhas.append("nao achei %s no LevelUpWindowButton.cs" % ENSURE)
    elif "Refresh()" not in ensure:
        falhas.append("o Ensure nao chama `Refresh()` — o caminho idempotente (2o personagem da "
                      "fila) nao reafirmaria a visibilidade do clone")

    # 4) E nao injeta FORA DE HORA: exige a janela ATIVA.
    interno = _corpo_ou_none(src_janela, "private static void EnsureInternal(RoguelikeManager rok)")
    if interno is None:
        falhas.append("nao achei o `EnsureInternal` no LevelUpWindowButton.cs")
    elif GUARDA_JANELA_ATIVA not in interno:
        falhas.append("o EnsureInternal nao tem a guarda `%s` — ele pode injetar o botao fora de "
                      "hora (com a janela ja fechada)" % GUARDA_JANELA_ATIVA)

    # 5) O host reavalia a cada quadro.
    update = _corpo_ou_none(src_host, UPDATE_HOST)
    if update is None:
        falhas.append("nao achei o `Update` do RstvHost")
    elif CHAMADA_NO_HOST not in update:
        falhas.append("o `RstvHost.Update` nao chama `%s` — o botao nao seguiria o ciclo da janela "
                      "(o defeito 'voando no nivel-up')" % CHAMADA_NO_HOST)

    return falhas


def falhas_do_refluxo_da_arvore(src_leitura):
    """Sintoma (6): a arvore read-only NAO pode deixar o botao do HUD preso escondido.

    O gate `RunTargets.GateOk` bloqueia com `AnyUIWindowOpen`. Se a sessao read-only REGISTRAR a
    janela em `UIWindowManager.OpenedWindows`, o botao do HUD fica escondido enquanto ela estiver
    aberta (o flapping e o comportamento esperado) — e, para o botao VOLTAR, a sessao TEM de sair da
    lista no fechamento. A invariante travada aqui e essa: QUEM ENTRA, SAI. Se a implementacao nao
    registra nada (a RSTV-5 passou a bloquear o clique pelo prefixo do `ProcessLeftMouseClick`, sem
    a camada do `OpenedWindows`), a invariante ja vale — nada fica preso.

    Em qualquer um dos desenhos, o `Close()` tem de encerrar a sessao (`End()`), senao o estado
    read-only fica vivo depois de a janela fechar.
    """
    falhas = []
    efetivo = rec.codigo_efetivo(src_leitura)

    registra = "RegisterAsOpenWindow" in efetivo
    desregistra = "UnregisterAsOpenWindow" in efetivo
    if registra and not desregistra:
        falhas.append("a sessao read-only REGISTRA a janela em `UIWindowManager.OpenedWindows` mas "
                      "NAO a retira no fechamento — o botao do HUD NUNCA voltaria depois de fechar a "
                      "arvore (sintoma 6)")

    fechar = _corpo_ou_none(src_leitura, "internal static void Close()")
    if fechar is None:
        return falhas + ["nao achei o `Close()` da sessao read-only (nao da para provar que a "
                         "arvore fecha e o botao VOLTA)"]
    if "End()" not in fechar:
        falhas.append("o `Close()` da sessao read-only NAO chama `End()` — o estado read-only "
                      "ficaria vivo depois de a janela fechar (o botao nao voltaria ao normal)")
    return falhas


# ------------------------------------------------------------ plantio dos defeitos ---

_ANCORA_HOST = CHAMADA_NO_HOST + ";"

_ANCORA_ESTAGIO = "rok.CurLevelUpStage == LevelUpStage.Skills"
_DEFEITO_SEM_ESTAGIO = "true"

_ANCORA_GUARDA = GUARDA_JANELA_ATIVA
_DEFEITO_SEM_GUARDA = "if (false)"


def fonte_sem_refresh_no_host(src=None):
    """O MESMO fonte do host com a chamada do Refresh MORTA (o defeito 'nao segue o ciclo')."""
    texto = fonte(caminho_host()) if src is None else src
    if _ANCORA_HOST not in texto:
        return texto
    return texto.replace(_ANCORA_HOST, "// RSTV-14: Refresh() removido (defeito)", 1)


def fonte_refresh_sem_estagio(src=None):
    """O MESMO fonte da janela com o Refresh deixando de olhar o ESTAGIO (o defeito 'voando')."""
    texto = fonte(caminho_janela()) if src is None else src
    if _ANCORA_ESTAGIO not in texto:
        return texto
    return texto.replace(_ANCORA_ESTAGIO, _DEFEITO_SEM_ESTAGIO, 1)


def fonte_sem_guarda_de_janela_ativa(src=None):
    """O MESMO fonte da janela com a guarda de 'janela ativa' MORTA (injeta fora de hora)."""
    texto = fonte(caminho_janela()) if src is None else src
    if _ANCORA_GUARDA not in texto:
        return texto
    return texto.replace(_ANCORA_GUARDA, _DEFEITO_SEM_GUARDA, 1)
