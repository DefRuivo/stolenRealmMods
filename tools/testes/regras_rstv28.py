#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rstv28.py - RSTV-29: a superficie do botao 'Skills' da tela Select Party NAO existe mais.

HISTORICO (RSTV-28 -> RSTV-29)
------------------------------
Ate' a RSTV-28 havia um botao 'Skills' INJETADO na tela Select Party (a classe `SelectPartyButton`:
clone do botao nativo 'Choose Powerups', `Ensure` na abertura da tela e `Mirror` no host; a RSTV-28
ainda REINJETAVA pelo caminho do 'Continue' — `CharacterChoiceManager.OpenWindow`).

Em 06/10 o dono decidiu, EM JOGO, REMOVER aquela superficie: o botao da tela de escolha de grupo nao
existe mais, e quem atende a tela de party e' o botao 'Skills' do modal 'Remove Skill Trees'
(RSTV-20). Com a feature removida a reinjecao da RSTV-28 perdeu o sentido, e os DOIS ganchos da tela
foram apagados (ver o cabecalho de `Patches.cs`).

O QUE ESTAS REGRAS TRAVAM (uma AUSENCIA, nao uma chamada)
--------------------------------------------------------
1. o arquivo `SelectPartyButton.cs` NAO existe;
2. nenhum `.cs` do mod cita `SelectPartyButton`, `RstvSkillTreeButton` (o nome do clone),
   `CharacterChoiceOpenPatch` nem `CharacterChoiceOpenWindowPatch` no CODIGO EFETIVO — comentario
   historico que explica a remocao NAO conta (`recorte.codigo_efetivo` tira comentario);
3. `Patches.cs` NAO tem gancho em `CharacterChoiceManager.OpenCharacterChoiceManager` nem em
   `CharacterChoiceManager.OpenWindow` (os dois existiam SO' para injetar aquele botao) — em NENHUMA
   forma de escrita (`nameof(...)`, STRING literal ou identificador nu), olhando a PROPRIEDADE
   "nenhum patch aponta para a tela" e nao so' o nome da classe do gancho (RSTV-29F, achado C);
4. `Plugin.cs` nao anuncia a tela: nem o texto antigo do config ("Injeta o botao 'Skills' na tela
   Select Party") nem a linha de boot "RSTV DIAG: botao 'Skills' da tela Select Party".

A PROVA DE FOGO e' EMBUTIDA: cada funcao `com_*_de_volta` reinjeta UM pedaco da superficie numa copia
EM MEMORIA do conjunto de fontes, e a MESMA checagem tem de REPROVAR por aquele pedaco. A bancada
FISICA (arquivos escritos numa copia FORA do repo) e' `tools/testes/prova-sandbox-rstv28.py`.

O que estes testes NAO provam: nao executam o C# do mod e nao medem em tela — o dono confirma a
ausencia vendo que a tela de party nao tem mais o botao.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco as arc
import recorte as rec

# ------------------------------------------------------------------ a superficie removida ---

# O nome do arquivo/classe apagado na RSTV-29.
ARQUIVO_REMOVIDO = "SelectPartyButton.cs"

# Identificadores da superficie: qualquer um no CODIGO EFETIVO de qualquer .cs e' vestigio.
VESTIGIOS = (
    "SelectPartyButton",
    "RstvSkillTreeButton",
    "CharacterChoiceOpenPatch",
    "CharacterChoiceOpenWindowPatch",
)

# Os metodos da tela que existiam SO' para injetar aquele botao.
METODOS_DA_TELA = ("OpenCharacterChoiceManager", "OpenWindow")

# RSTV-29F (achado C da RSTV-29R): a checagem de AUSENCIA nao pode prender so' o NOME da classe do
# gancho nem a forma `nameof(...)`. A PROPRIEDADE que se quer travar e' "nenhum gancho Harmony aponta
# para a tela" (a classe abaixo + um destes metodos), em QUALQUER forma de escrita — `nameof(...)`,
# STRING literal ou identificador nu. Um gancho escrito como
# `[HarmonyPatch(typeof(CharacterChoiceManager), "OpenWindow", new Type[0])]` com classe de nome
# NEUTRO passava batido na checagem antiga (medido pelo revisor com sonda propria).
CLASSE_DA_TELA = "CharacterChoiceManager"
METODOS_PROIBIDOS_EM_GANCHO = ("OpenCharacterChoiceManager", "OpenWindow")

# Trechos que o Plugin.cs NAO pode mais ter (config/boot log mentindo sobre a feature removida).
TEXTOS_PROIBIDOS_NO_PLUGIN = (
    "Injeta o botao 'Skills' na tela Select Party",
    "RSTV DIAG: botao 'Skills' da tela Select Party",
)


# ------------------------------------------------------------------ leitura ---

def pasta_do_mod():
    return os.path.join(arc.raiz_do_repo(), "RoguelikeSkillTreeVisualizer")


def le_arquivos_cs():
    """{nome_do_arquivo: conteudo} dos .cs do mod. A EXISTENCIA de um nome e' a propria chave."""
    pasta = pasta_do_mod()
    arquivos = {}
    for nome in sorted(os.listdir(pasta)):
        if nome.endswith(".cs"):
            with open(os.path.join(pasta, nome), encoding="utf-8") as fh:
                arquivos[nome] = fh.read()
    return arquivos


def fonte(nome):
    with open(os.path.join(pasta_do_mod(), nome), encoding="utf-8") as fh:
        return fh.read()


# ------------------------------------------------------------------ checagem ---

def _argumentos_de_atributos(texto_efetivo, nome="HarmonyPatch"):
    """O TEXTO dos argumentos de cada `[nome(...)]`, com o `(...)` balanceado.

    Le o CODIGO EFETIVO (comentario fora). O `(` de abertura e casado por contagem, IGNORANDO
    literais de string/char — um `)` dentro de `"..."` nao fecha o atributo. Outro atributo com o
    mesmo prefixo (ex.: `[HarmonyPatchAll]`) nao conta. Atributo sem `(...)` (`[HarmonyPatch]`) e'
    ignorado: sem argumentos nao ha metodo.
    """
    argumentos = []
    marcador = "[" + nome
    i = 0
    while True:
        i = texto_efetivo.find(marcador, i)
        if i < 0:
            return argumentos
        p = i + len(marcador)
        if p < len(texto_efetivo) and (texto_efetivo[p].isalnum() or texto_efetivo[p] == "_"):
            i = p
            continue
        while p < len(texto_efetivo) and texto_efetivo[p] in " \t\r\n":
            p += 1
        if p >= len(texto_efetivo) or texto_efetivo[p] != "(":
            i = p
            continue
        nivel, q = 0, p
        while q < len(texto_efetivo):
            c = texto_efetivo[q]
            if c in "\"'":
                q = rec.fim_do_literal(texto_efetivo, q)
                continue
            if c == "(":
                nivel += 1
            elif c == ")":
                nivel -= 1
                if nivel == 0:
                    q += 1
                    break
            q += 1
        argumentos.append(texto_efetivo[p:q])
        i = q


def ganchos_apontando_para_a_tela(patches):
    """A LISTA de ganchos Harmony que apontam para a TELA removida, em QUALQUER forma de escrita.

    Prende a PROPRIEDADE "nenhum patch aponta para `CharacterChoiceManager` nos metodos que eram o
    injetor", e nao o NOME da classe do gancho nem a forma `nameof(...)`. Um gancho escrito como
    `[HarmonyPatch(typeof(CharacterChoiceManager), "OpenWindow", new Type[0])]` com classe de nome
    neutro REPROVA aqui — o furo que o achado C da RSTV-29R mediu na checagem antiga.

    Vazio = nenhum gancho para a tela.
    """
    efetivo = rec.codigo_efetivo(patches)
    falhas = []
    argumentos = _argumentos_de_atributos(efetivo)

    # (a) o MESMO atributo nomeia a classe da tela E um dos metodos removidos (nameof, string ou nu).
    for args in argumentos:
        if CLASSE_DA_TELA not in args:
            continue
        for metodo in METODOS_PROIBIDOS_EM_GANCHO:
            if metodo in args:
                falhas.append("Patches.cs tem `[HarmonyPatch%s` — um gancho que aponta para "
                              "`%s.%s` (era o injetor da superficie removida)"
                              % (args, CLASSE_DA_TELA, metodo))

    # (b) forma ESPALHADA em atributos IRMAOS (o Harmony combina `[HarmonyPatch(...)]` seguidos):
    #     um atributo nomeia a classe e OUTRO cita o metodo por STRING literal.
    da_classe = [a for a in argumentos if CLASSE_DA_TELA in a]
    do_metodo = [a for a in argumentos
                 if any(('"%s"' % m) in a for m in METODOS_PROIBIDOS_EM_GANCHO)]
    for a_cls in da_classe:
        for a_met in do_metodo:
            if a_cls == a_met:
                continue
            falhas.append("Patches.cs tem um atributo de `%s` e outro citando o metodo por STRING "
                          "(atributos combinam no Harmony): `%s` + `%s`" % (CLASSE_DA_TELA, a_cls, a_met))

    return falhas


def falhas_da_ausencia(arquivos):
    """A LISTA de vestigios da superficie Select Party. Vazia = a superficie foi removida."""
    falhas = []

    # 1) o arquivo da classe apagada nao pode existir.
    if ARQUIVO_REMOVIDO in arquivos:
        falhas.append("o arquivo %s ainda existe (a classe da superficie foi apagada na RSTV-29)"
                      % ARQUIVO_REMOVIDO)

    # 2) nenhum identificador da superficie no CODIGO EFETIVO de nenhum .cs.
    for nome in sorted(arquivos):
        efetivo = rec.codigo_efetivo(arquivos[nome])
        for vestigio in VESTIGIOS:
            if vestigio in efetivo:
                falhas.append("%s ainda cita `%s` no codigo efetivo — vestigio da superficie removida"
                              % (nome, vestigio))

    # 3) nenhum gancho nos metodos da tela (eram o injetor) — pela PROPRIEDADE "nenhum patch aponta
    #    para a tela", em QUALQUER forma (nameof, STRING literal ou identificador nu). A checagem
    #    antiga (nameof literal) e' um CASO PARTICULAR desta e continua aqui para nao afrouxar nada:
    #    o achado C da RSTV-29R mostrou que ela sozinha deixava passar a forma por STRING com classe
    #    de nome neutro (`[HarmonyPatch(typeof(CharacterChoiceManager), "OpenWindow", ...)]`).
    patches = arquivos.get("Patches.cs", "")
    for metodo in METODOS_DA_TELA:
        if "nameof(CharacterChoiceManager.%s)" % metodo in patches:
            falhas.append("Patches.cs ainda tem gancho em `CharacterChoiceManager.%s` — era o "
                          "injetor da superficie removida" % metodo)
    for motivo in ganchos_apontando_para_a_tela(patches):
        if motivo not in falhas:
            falhas.append(motivo)

    # 4) o Plugin.cs nao anuncia a tela (config/boot log).
    plugin = arquivos.get("Plugin.cs", "")
    for texto in TEXTOS_PROIBIDOS_NO_PLUGIN:
        if texto in plugin:
            falhas.append("Plugin.cs ainda anuncia a superficie removida: %r" % texto)

    return falhas


# ------------------------------------------------------------ plantio do defeito ---

def com_botao_de_volta(arquivos):
    """O arquivo + a classe da superficie de volta (copia em memoria) -> TEM de reprovar."""
    copia = dict(arquivos)
    copia[ARQUIVO_REMOVIDO] = ("namespace RoguelikeSkillTreeVisualizer\n{\n"
                               "    internal static class SelectPartyButton { }\n}\n")
    return copia


def com_ensure_de_volta(arquivos):
    """A chamada `SelectPartyButton.Ensure(__instance);` de volta em Patches.cs -> TEM de reprovar."""
    copia = dict(arquivos)
    patches = copia.get("Patches.cs", "")
    copia["Patches.cs"] = patches.replace(
        "internal static class CharacterChoiceTogglePatch",
        "SelectPartyButton.Ensure(__instance);\n    internal static class CharacterChoiceTogglePatch", 1)
    return copia


def com_hook_da_janela_de_volta(arquivos):
    """O gancho da RSTV-28 (`OpenWindow`) de volta em Patches.cs -> TEM de reprovar."""
    copia = dict(arquivos)
    patches = copia.get("Patches.cs", "")
    copia["Patches.cs"] = patches.replace(
        "[HarmonyPatch(typeof(CharacterChoiceManager), nameof(CharacterChoiceManager.ToggleSelectedCharacter)",
        "[HarmonyPatch(typeof(CharacterChoiceManager), nameof(CharacterChoiceManager.OpenWindow), new Type[0])]\n"
        "    internal static class CharacterChoiceOpenWindowPatch { }\n\n"
        "    [HarmonyPatch(typeof(CharacterChoiceManager), nameof(CharacterChoiceManager.ToggleSelectedCharacter)",
        1)
    return copia


def com_diag_de_volta(arquivos):
    """A linha de boot da tela de volta em Plugin.cs -> TEM de reprovar."""
    copia = dict(arquivos)
    plugin = copia.get("Plugin.cs", "")
    copia["Plugin.cs"] = plugin.replace(
        "RSTV DIAG: chave-mestra",
        "RSTV DIAG: botao 'Skills' da tela Select Party HABILITADO nesta sessao; RSTV DIAG: chave-mestra",
        1)
    return copia


# ------------------------------------- RSTV-29F (achado C): a forma por STRING tambem reprova ---
# A ancora e' o atributo do `CharacterChoiceTogglePatch` (o unico gancho de `CharacterChoiceManager`
# que FICA): os plantios entram logo antes dele.

_ANCORA_TOGGLE = ("[HarmonyPatch(typeof(CharacterChoiceManager), "
                  "nameof(CharacterChoiceManager.ToggleSelectedCharacter),")


def com_hook_string_de_volta(arquivos):
    """O gancho da tela por STRING + classe de nome NEUTRO -> TEM de reprovar.

    RSTV-29F (achado C da RSTV-29R): e' a ESCAPATORIA que a checagem antiga deixava passar — o alvo
    `CharacterChoiceManager.OpenWindow` escrito como STRING no MESMO atributo e a classe do patch com
    nome neutro (nenhum dos `VESTIGIOS`). O alvo tem de ser visto pela PROPRIEDADE, nao pelo nome.
    """
    copia = dict(arquivos)
    patches = copia.get("Patches.cs", "")
    copia["Patches.cs"] = patches.replace(
        _ANCORA_TOGGLE,
        "[HarmonyPatch(typeof(CharacterChoiceManager), \"OpenWindow\", new Type[0])]\n"
        "    internal static class NeutralReinjectPatch { }\n\n"
        "    " + _ANCORA_TOGGLE,
        1)
    return copia


def com_hook_string_espalhado_de_volta(arquivos):
    """O gancho da tela em DOIS atributos IRMAOS (classe + string) -> TEM de reprovar.

    O Harmony combina `[HarmonyPatch(...)]` seguidos; a checagem por ATRIBUTO sozinho nao veria o
    par. A classe do patch e' neutra (nenhum vestigio).
    """
    copia = dict(arquivos)
    patches = copia.get("Patches.cs", "")
    copia["Patches.cs"] = patches.replace(
        _ANCORA_TOGGLE,
        "[HarmonyPatch(typeof(CharacterChoiceManager))]\n"
        "    [HarmonyPatch(\"OpenWindow\", new Type[0])]\n"
        "    internal static class NeutralSpreadPatch { }\n\n"
        "    " + _ANCORA_TOGGLE,
        1)
    return copia
