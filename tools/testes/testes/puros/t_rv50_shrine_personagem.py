#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RV-50 (03/10) - O PERSONAGEM DA LINHA DE SHRINE (o defeito do "valores de TODOS").

O DEFEITO (card t_9fc78584, relato do dono, 03/10, com imagem)
--------------------------------------------------------------
`linha 'Your active shrine auras' mostra valores de TODOS (deve ser so o personagem selecionado;
inimigo sai no tooltip DELE; dobro com worship CORRETO)`.

O QUE O MOTOR FAZ (decompilado do build atual, nao leitura de prosa)
--------------------------------------------------------------------
* `Tooltip.TooltipCharacter` e `GameLogic.instance.CurrentlySelectedCharacter`
  (l.213124-213133) - NAO o personagem que a tooltip descreve. O `Receptor` antigo olhava SO ele;
* `Tooltip.ShowActionStatusTooltip(StatusIcon)` -> `ShowActionStatusTooltip(info, source, target,
  ...)` (l.214067-214073) monta a tooltip do status de QUALQUER personagem (party E inimigo) e o
  `LocalizePatch` anexa a linha a toda descricao da familia (`ShrineAuraPatch.IsShrineKey`). No
  tooltip do icone de buff do INIMIGO a linha saia com o numero do SELECIONADO - o defeito;
* o personagem SOB O CURSOR o jogo expoe em `PlayerInfoWindow.currentCharacter` (l.151757):
  `HexCellManager.CurrentlyHoveringHexCell` -> `playerInfoWindow.ShowPlayerInfoWindow(player)` para
  QUALQUER personagem do hex, inclusive inimigo (`ShouldShowPlayerInfoWindow` aceita `TeamIndex != 0`,
  l.121521-121526 + l.151776-151786);
* `Tooltip.ShowGroundEffectTooltip` liga `Tooltip.ShowingGroundEffect` (l.214157) e o `ShowTooltip`
  desliga (l.215141): e a janela em que o hover do SHRINE monta o texto - ali nao ha personagem e a
  spec do dono manda mostrar so o SELECIONADO.

O CONSERTO QUE ESTE TESTE TRAVA (RV-50 + endurecimento RV-50R)
--------------------------------------------------------------
  1. `Receptor` le o PERSONAGEM SOB O CURSOR (`PersonagemSobOCursor()`) ANTES do selecionado
     (`TooltipCharacter`) - o inimigo sai no tooltip DELE;
  2. `Receptor` EXCLUI o tooltip do SHRINE com a guarda na POLARIDADE certa - a SUB-STRING EXATA
     `t == null || !t.ShowingGroundEffect` (RV-50R): com a guarda invertida (`t != null &&
     t.ShowingGroundEffect`) o shrine usaria o CURSOR e o status do INIMIGO o SELECIONADO;
  3. `PersonagemSobOCursor` le `GUIManager.instance.playerInfoWindow.currentCharacter`, devolve
     esse campo pelo RETORNO EFETIVO (`return janela.currentCharacter;`, RV-50R - um retorno
     dentro de `if (false)` reprova) e nunca varre `AllCharacters`;
  4. os fallbacks antigos continuam (`TooltipCharacter` -> `WorldCharacter` -> `Source`/`Target`).

REGRA DE OURO DESTE TESTE: a checagem tem de MORDER. Cada exigencia e provada com um defeito
plantado passando por ela e sendo ACUSADO - checagem que nunca foi vista reprovando seria decoracao.

LIMITE. Nao executa o C# do mod (pediria a `lib/` do jogo e um harness): a ligacao com o motor e o
RECORTE do fonte vivo (`recorte.py`) e a regra transcrita em `regras_rv50.py`, citando o decompilado.
A enumeracao dos ALVOS do Flame (`AlvosNaAreaDoFlame`) NAO entra aqui: e a spec do dono de 30/09,
presa pela familia `t_shrine_*` (`t_shrine_excesso_dano`) e território das auras de PERIGO (RV-49).
"""
import io
import os

import arcabouco as arc
import recorte as rec
import regras_rv50 as reg

META = {
    "nome": "rv50-shrine-personagem",
    "categoria": "pura",
    "requer": [],
    "descricao": "RV-50: `Receptor` le o PERSONAGEM SOB O CURSOR antes do selecionado (o inimigo sai "
                 "no tooltip DELE), exclui o tooltip do SHRINE e mantem os fallbacks - a linha nao "
                 "mostra mais os valores de outro personagem",
}

ARQUIVO = os.path.join("BetterTooltips", "Patches", "ShrineAuraPatch.cs")

# (a) O DEFEITO CLASSICO: o resolvedor so olha o SELECIONADO (o estado anterior ao RV-50). A isca
#     neutraliza a leitura do personagem sob o cursor e a checagem tem de acusar a volta do defeito.
_REVERTER_SOB_CURSOR = "Character sobOCursor = null; /*isca: sem leitura do personagem sob o cursor*/"

# (b) O DEFEITO DA GUARDA: o tooltip do SHRINE deixa de ser excluido - um personagem sob o cursor
#     (ou a janela de info do chefe) passaria a decidir a linha no hover do shrine.
_GUARDA_NEUTRALIZADA = "if (true) /*isca: sem a guarda do ground effect*/"

# (c) O DEFEITO DO HELPER: a fonte do personagem sob o cursor deixa de ser o campo do jogo.
_HELPER_SEM_FONTE = ("Character janela = PersonagemSobOCursor.inventado; /*isca: helper sem a fonte "
                     "playerInfoWindow.currentCharacter*/")

# (e) RV-50R - A POLARIDADE DA GUARDA: a flag continua no corpo, mas com o SENTIDO invertido. O
#     ground effect passaria a LER o personagem sob o cursor e o tooltip do status do INIMIGO
#     sairia com o SELECIONADO (o defeito do RV-50 de ponta-cabeca). A checagem tem de exigir a
#     SUB-STRING EXATA `t == null || !t.ShowingGroundEffect`, nao so o NOME da flag.
_GUARDA_INVERTIDA = "if (t != null && t.ShowingGroundEffect) /*isca: polaridade da guarda invertida*/"

# (f) RV-50R - O RETORNO MORTO: as substrings `playerInfoWindow` E `currentCharacter` continuam no
#     corpo (a checagem ANTIGA passaria); o `return janela.currentCharacter;` fica DENTRO de um
#     `if (false)` e o helper cai SEMPRE no `return null`. A checagem tem de acusar o retorno
#     INALCANCAVEL, nao so a presenca das substrings.
_GUARDA_DO_RETORNO_FALSA = "if (false) /*isca: retorno morto - o campo do jogo sob guarda falsa*/"

# (g) RV-50R - O RETORNO NAO E O EFETIVO: as substrings `playerInfoWindow`/`currentCharacter`
#     continuam no corpo, mas o campo e devolvido por OUTRO caminho - a linha exata
#     `return janela.currentCharacter;` NAO existe. A checagem tem de exigir a SUB-STRING EXATA do
#     retorno efetivo, nao so a presenca de `currentCharacter`.
_RETORNO_NAO_EXATO = ("return EscolherPersonagemDoHover(janela.currentCharacter); "
                      "/*isca: le o campo mas o retorno efetivo e outro*/")

# (h) RV-50TF2 - A POLARIDADE SOB CODIGO MORTO (o furo i da revisao): a SUB-STRING EXATA da guarda
#     continua no corpo, mas DENTRO de um `if (false) { ... }` (CODIGO MORTO), e a guarda VIVA esta
#     INVERTIDA (`t != null && t.ShowingGroundEffect`). A checagem ANTIGA
#     (`POLARIDADE_GUARDA not in receptor`) passava VERDE - a mesma classe do furo original volta
#     (o shrine usaria o CURSOR e o status do INIMIGO o SELECIONADO). A checagem nova exige a
#     sub-string no CAMINHO EFETIVO, como ja faz o RETORNO.
_GUARDA_MORTA_COM_A_VIVA_INVERTIDA = (
    "if (false) { if (t == null || !t.ShowingGroundEffect) { } }\n"
    "                if (t != null && t.ShowingGroundEffect) /*isca: polaridade certa so em codigo morto*/")

# (i) RV-50TF2 - O FALLBACK SEM A LEITURA REAL: a LEITURA `t.TooltipCharacter` some (o campo lido
#     passa a ser outro), mas o LITERAL DE LOG da catch continua CITANDO `TooltipCharacter`. A
#     checagem ANTIGA (`receptor.find("TooltipCharacter")`) casava o TEXTO do log e passava VERDE -
#     a exigencia do fallback pelo SELECIONADO era decoracao nao-provada. A checagem nova busca no
#     codigo SEM o texto dos literais e acusa a perda do fallback.
_SEM_LEITURA_TOOLTIPCHARACTER = ("Character emFoco = t.CampoQueNaoE  "
                                 "/*isca: sem a leitura do TooltipCharacter (o log ainda cita o nome)*/;")

# (j) RV-50TF3 - A GUARDA VIVA MAS VAZIA + A INVERTIDA GATEANDO O CORPO: a SUB-STRING EXATA da
#     polaridade certa fica numa guarda VIVA porem VAZIA (`if (t == null || !t.ShowingGroundEffect) { }`)
#     - um DECOY -, e o corpo que usa o personagem certo (a leitura `PersonagemSobOCursor()`) fica sob
#     a guarda VIVA INVERTIDA (`if (t != null && t.ShowingGroundEffect) { ... }`). A checagem ANTIGA
#     (sub-string no CAMINHO EFETIVO) passava VERDE - a sub-string esta viva, mas NAO e a CONDICAO da
#     guarda que GATEIA o corpo. A checagem nova exige que o bloco do `if` cuja condicao E a sub-string
#     contenha a leitura do personagem sob o cursor.
_DECOY_VAZIO_E_INVERTIDA_GATEANDO_O_CORPO = (
    "if (t == null || !t.ShowingGroundEffect) { }\n"
    "                if (t != null && t.ShowingGroundEffect) /*isca: decoy vivo-e-vazio + invertida "
    "gateando o corpo*/")

# (k) RV-50TF4 (furo A) - A GUARDA INVERTIDA ANINHADA: a leitura `PersonagemSobOCursor()` fica
#     DENTRO do bloco da guarda CERTA, mas sob uma guarda ANINHADA INVERTIDA
#     (`if (t != null && t.ShowingGroundEffect)`). Dentro do bloco da certa a aninhada e SEMPRE
#     falsa (e a NEGACAO logica dela - De Morgan), entao a leitura e CODIGO MORTO. A checagem
#     ANTIGA (RV-50TF3 - presenca TEXTUAL do corpo no bloco) passava VERDE: a leitura esta no
#     bloco, mas nao no CAMINHO EFETIVO dele. A checagem nova exige a leitura VIVA dentro do bloco.
_ANCORA_GUARDA_E_CORPO = (
    "                if (t == null || !t.ShowingGroundEffect)\n"
    "                {\n"
    "                    Character sobOCursor = PersonagemSobOCursor();\n"
    "                    if (sobOCursor != null)\n"
    "                    {\n"
    "                        return sobOCursor;\n"
    "                    }\n"
    "                }\n"
)

_GUARDA_INVERTIDA_ANINHADA = (
    "                if (t == null || !t.ShowingGroundEffect)\n"
    "                {\n"
    "                    if (t != null && t.ShowingGroundEffect) /*isca: guarda invertida ANINHADA - "
    "a leitura fica sob ela (codigo morto) DENTRO da guarda certa*/\n"
    "                    {\n"
    "                        Character sobOCursor = PersonagemSobOCursor();\n"
    "                        if (sobOCursor != null)\n"
    "                        {\n"
    "                            return sobOCursor;\n"
    "                        }\n"
    "                    }\n"
    "                }\n"
)

# (l) RV-50TF4 (furo B) - O CORPO SOB CODIGO MORTO: a leitura `PersonagemSobOCursor()` fica DENTRO
#     do bloco da guarda CERTA, mas sob um `if (false)`. A leitura esta textualmente no bloco, mas
#     MORTA. A checagem ANTIGA (RV-50TF3 - presenca textual) passava VERDE; a checagem nova exige a
#     leitura no CAMINHO EFETIVO DENTRO do bloco (a MESMA logica de codigo morto do retorno).
_CORPO_SOB_CODIGO_MORTO = (
    "                if (t == null || !t.ShowingGroundEffect)\n"
    "                {\n"
    "                    if (false) /*isca: corpo sob if(false) - codigo morto DENTRO da guarda "
    "certa*/\n"
    "                    {\n"
    "                        Character sobOCursor = PersonagemSobOCursor();\n"
    "                        if (sobOCursor != null)\n"
    "                        {\n"
    "                            return sobOCursor;\n"
    "                        }\n"
    "                    }\n"
    "                }\n"
)

# (m) RV-50TF5 - O `if` SEM CHAVES (CONTROLE NEGATIVO, tem de PASSAR). Um retorno antecipado
#     legitimo e SEM chaves (`if (cond) return x;`, estilo C# comum) controla APENAS a instrucao
#     imediata. Quando a condicao e a INVERSA da guarda certa
#     (`if (t != null && t.ShowingGroundEffect) return null;`), a checagem ANTIGA (RV-50TF4)
#     atribuia a ele o bloco `{ ... }` da guarda CERTA (o proximo `{` do texto) e, sendo as duas
#     condicoes negacoes logicas (De Morgan), marcava a leitura VIVA dentro do bloco como MORTA ->
#     o codigo LEGITIMO REPROVAVA (FALSO POSITIVO). A checagem nova (RV-50TF5: o bloco so e da
#     guarda se o `{` abre logo apos a condicao) tem de ACEITAR esta variacao: violacoes = [].
_RETORNO_ANTECIPADO_SEM_CHAVES = (
    "                if (t != null && t.ShowingGroundEffect) return null;\n"
    + _ANCORA_GUARDA_E_CORPO
)

# (d) O DEFEITO DA ORDEM (sintetico): o selecionado e lido ANTES do personagem sob o cursor - as duas
#     leituras existem, mas o SELECIONADO vence. E o que a ORDEM do conserto impede.
TRECHO_ORDEM_TROCADA = (
    "        private static Character Receptor(Tooltip tooltip, GameFunctionParameters parametros)\n"
    "        {\n"
    "            Tooltip t = tooltip;\n"
    "            try\n"
    "            {\n"
    "                if (t != null)\n"
    "                {\n"
    "                    Character emFoco = t.TooltipCharacter;\n"
    "                    if (emFoco != null) { return emFoco; }\n"
    "                }\n"
    "            }\n"
    "            catch (Exception) { }\n"
    "            try\n"
    "            {\n"
    "                if (t == null || !t.ShowingGroundEffect)\n"
    "                {\n"
    "                    Character sobOCursor = PersonagemSobOCursor();\n"
    "                    if (sobOCursor != null) { return sobOCursor; }\n"
    "                }\n"
    "            }\n"
    "            catch (Exception) { }\n"
    "            return parametros.Source != null ? parametros.Source : parametros.Target;\n"
    "        }\n"
    "        private static Character PersonagemSobOCursor()\n"
    "        {\n"
    "            return GUIManager.instance.playerInfoWindow.currentCharacter;\n"
    "        }\n"
)


def _fonte():
    caminho = os.path.join(arc.raiz_do_repo(), ARQUIVO)
    arc.exigir(os.path.isfile(caminho),
               "a fonte viva das regras sumiu: %s (o teste vigia ela, nao uma copia)" % caminho)
    with io.open(caminho, encoding="utf-8") as fh:
        return fh.read()


def _prova(rotulo, texto_infectado, esperado, o_que):
    """A checagem MORDE: a isca passa por `violacoes` e tem de ser ACUSADA pelo motivo certo."""
    falhas = reg.violacoes(texto_infectado)
    arc.exigir(any(esperado in f for f in falhas),
               "a checagem NAO acusa o defeito '%s' (%s; procurei %r): %r"
               % (o_que, rotulo, esperado, falhas))


def _prova_conforme(rotulo, texto_legitimo, o_que):
    """CONTROLE NEGATIVO: a variacao LEGITIMA passa por `violacoes` e NAO pode ser acusada.

    Uma checagem que reprova codigo correto e tao defeituosa quanto uma que deixa passar o defeito.
    Esta prova trava o FALSO POSITIVO: a variacao tem de sair CONFORME (violacoes = []).
    """
    falhas = reg.violacoes(texto_legitimo)
    arc.exigir(not falhas,
               "a checagem REPROVA o codigo LEGITIMO '%s' (%s) - FALSO POSITIVO: %r"
               % (o_que, rotulo, falhas))


def _plantar(fonte, alvo, defeito, o_que):
    """Planta o defeito por `str.replace`; se a ancora sumiu, o teste FALHA (nao passa calado)."""
    infectado = fonte.replace(alvo, defeito)
    arc.exigir(infectado != fonte,
               "nao consegui plantar o defeito '%s' no fonte (a ancora %r mudou?)" % (o_que, alvo))
    return infectado


def corpo():
    fonte = _fonte()

    # ---------------------------------------------------------------- 1. o fonte VIVO
    falhas = reg.violacoes(fonte)
    arc.exigir(not falhas, "a regra do RV-50 acusa o fonte VIVO: " + "; ".join(falhas))

    # ------------------------------------------- 2. as iscas: a checagem tem de MORDER
    # (a) a VOLTA do defeito: o resolvedor sem a leitura do personagem sob o cursor.
    _prova("resolvedor sem o personagem sob o cursor",
           _plantar(fonte, "Character sobOCursor = PersonagemSobOCursor();", _REVERTER_SOB_CURSOR,
                    "resolvedor sem o personagem sob o cursor"),
           "PersonagemSobOCursor", "resolvedor sem o personagem sob o cursor (o defeito do RV-50)")

    # (b) a guarda do ground effect removida: o SHRINE deixaria de mostrar so o SELECIONADO.
    _prova("tooltip do SHRINE sem a guarda",
           _plantar(fonte, "!t.ShowingGroundEffect", _GUARDA_NEUTRALIZADA,
                    "tooltip do SHRINE sem a guarda"),
           "ShowingGroundEffect", "tooltip do SHRINE sem a guarda (o selecionado deixaria de ser a regra)")

    # (c) o helper deixa de ler o campo do jogo (`playerInfoWindow.currentCharacter`).
    _prova("helper sem a fonte do jogo",
           _plantar(fonte, "return janela.currentCharacter;", _HELPER_SEM_FONTE,
                    "helper sem a fonte do jogo"),
           "currentCharacter", "helper do personagem sob o cursor sem a fonte do jogo")

    # (d) a ORDEM: o selecionado lido ANTES do personagem sob o cursor (as duas leituras existem).
    _prova("ordem trocada (selecionado primeiro)", TRECHO_ORDEM_TROCADA, "ORDEM",
           "ordem trocada: o selecionado antes do personagem sob o cursor")

    # (e) RV-50R - A POLARIDADE da guarda: o NOME da flag no corpo, mas o SENTIDO invertido. A
    #     checagem tem de prender a SUB-STRING EXATA `t == null || !t.ShowingGroundEffect`.
    _prova("guarda do SHRINE com a polaridade invertida",
           _plantar(fonte, "if (t == null || !t.ShowingGroundEffect)", _GUARDA_INVERTIDA,
                    "guarda do SHRINE com a polaridade invertida"),
           "t == null || !t.ShowingGroundEffect",
           "guarda do SHRINE com a polaridade invertida (o shrine usaria o CURSOR e o inimigo o SELECIONADO)")

    # (f) RV-50R - O RETORNO EFETIVO do helper: as substrings presentes, mas o
    #     `return janela.currentCharacter;` sob `if (false)` (retorno INALCANCAVEL).
    _prova("retorno efetivo do helper sob guarda falsa",
           _plantar(fonte, "if (janela != null && janela.gameObject.activeSelf)",
                    _GUARDA_DO_RETORNO_FALSA, "retorno efetivo do helper sob guarda falsa"),
           "guarda MORTA",
           "retorno efetivo do helper sob uma guarda falsa (o campo do jogo nunca e devolvido)")

    # (g) RV-50R - O RETORNO NAO E O EFETIVO (sub-string exata): as substrings continuam no corpo,
    #     mas o retorno do campo sai por outro caminho. A checagem tem de exigir a SUB-STRING
    #     EXATA `return janela.currentCharacter;`, nao so a presenca de `currentCharacter`.
    _prova("retorno do campo por outro caminho (nao o retorno efetivo)",
           _plantar(fonte, "return janela.currentCharacter;", _RETORNO_NAO_EXATO,
                    "retorno do campo por outro caminho"),
           "RETORNO EFETIVO",
           "retorno efetivo do helper nao e o campo do jogo (a sub-string exata do retorno sumiu)")

    # (h) RV-50TF2 - A POLARIDADE SOB CODIGO MORTO: a SUB-STRING EXATA da guarda fica em CODIGO
    #     MORTO (`if (false) { ... }`) e a guarda VIVA e invertida. So o NOME/SUB-STRING presentes
    #     nao bastam (era o furo i): a sub-string tem de estar no CAMINHO EFETIVO.
    _prova("polaridade da guarda so em CODIGO MORTO (guarda viva invertida)",
           _plantar(fonte, "if (t == null || !t.ShowingGroundEffect)",
                    _GUARDA_MORTA_COM_A_VIVA_INVERTIDA,
                    "polaridade da guarda escondida em codigo morto com a guarda viva invertida"),
           "CAMINHO EFETIVO",
           "polaridade da guarda so em codigo morto (a guarda viva invertida poria o CURSOR no shrine)")

    # (i) RV-50TF2 - O FALLBACK SEM A LEITURA REAL: some a LEITURA `t.TooltipCharacter` (o campo
    #     lido passa a ser outro) e o LITERAL DE LOG da catch continua citando o nome. A checagem
    #     antiga casava o TEXTO do log; a nova busca no codigo sem literais acusa a perda.
    _prova("fallback do SELECIONADO sem a leitura real (o log ainda cita TooltipCharacter)",
           _plantar(fonte, "Character emFoco = t.TooltipCharacter;", _SEM_LEITURA_TOOLTIPCHARACTER,
                    "fallback do SELECIONADO sem a leitura real do campo"),
           "perdeu o fallback",
           "perda do fallback pelo SELECIONADO (a sub-string do log mascarava a leitura real)")

    # (j) RV-50TF3 - A GUARDA VIVA MAS VAZIA + A INVERTIDA GATEANDO O CORPO: a SUB-STRING EXATA esta
    #     no CAMINHO EFETIVO (numa guarda VIVA porem VAZIA - o decoy), e o corpo que le o personagem
    #     sob o cursor fica sob a guarda VIVA INVERTIDA. A checagem antiga (so o CAMINHO EFETIVO)
    #     passava VERDE: a sub-string esta viva, mas NAO GATEIA o corpo. A checagem nova tem de
    #     acusar que a guarda NAO e a CONDICAO que GATEIA o corpo do acesso.
    _prova("polaridade certa em guarda viva-VAZIA com a invertida gateando o corpo",
           _plantar(fonte, "if (t == null || !t.ShowingGroundEffect)",
                    _DECOY_VAZIO_E_INVERTIDA_GATEANDO_O_CORPO,
                    "polaridade certa em guarda viva-vazia com a invertida gateando o corpo"),
           "GATEIA o corpo do acesso",
           "guarda viva-VAZIA (a sub-string esta no caminho efetivo, mas NAO gateia o corpo)")

    # (k) RV-50TF4 (furo A) - A GUARDA INVERTIDA ANINHADA: a leitura esta DENTRO do bloco da guarda
    #     CERTA, mas sob uma guarda INVERTIDA ANINHADA (a NEGACAO logica da certa). A checagem
    #     ANTIGA (RV-50TF3 - presenca textual no bloco) passava VERDE. A nova exige a leitura no
    #     CAMINHO EFETIVO DENTRO do bloco e tem de acusar a leitura MORTA pela guarda invertida.
    _prova("leitura no bloco da guarda certa mas sob a guarda INVERTIDA ANINHADA (morta)",
           _plantar(fonte, _ANCORA_GUARDA_E_CORPO, _GUARDA_INVERTIDA_ANINHADA,
                    "guarda invertida aninhada com a leitura morta dentro da guarda certa"),
           "GATEIA o corpo do acesso",
           "leitura no bloco da guarda certa mas sob a guarda INVERTIDA ANINHADA (codigo morto)")

    # (l) RV-50TF4 (furo B) - O CORPO SOB CODIGO MORTO: a leitura esta DENTRO do bloco da guarda
    #     CERTA, mas sob um `if (false)`. A checagem ANTIGA (presenca textual no bloco) passava
    #     VERDE. A nova exige a leitura no CAMINHO EFETIVO DENTRO do bloco e tem de acusar o morto.
    _prova("leitura no bloco da guarda certa mas sob if(false) (codigo morto)",
           _plantar(fonte, _ANCORA_GUARDA_E_CORPO, _CORPO_SOB_CODIGO_MORTO,
                    "corpo sob if(false) dentro da guarda certa"),
           "GATEIA o corpo do acesso",
           "leitura no bloco da guarda certa mas sob um if(false) (codigo morto)")

    # (m) RV-50TF5 - CONTROLE NEGATIVO: o `if` SEM CHAVES nao pode reprovar. A variacao e LEGITIMA
    #     (um retorno antecipado de uma linha, estilo C# comum) e a checagem RV-50TF4 a REPROVAVA
    #     (FALSO POSITIVO) porque `_guardas_que_contem` atribuia a ela o bloco da guarda CERTA, e as
    #     duas condicoes sao negacoes logicas (De Morgan) -> a leitura VIVA era marcada como MORTA.
    #     A checagem RV-50TF5 (o `{` tem de abrir logo apos a condicao) tem de ACEITAR esta variacao.
    _prova_conforme("retorno antecipado SEM chaves antes da guarda (nao pode reprovar)",
                    _plantar(fonte, _ANCORA_GUARDA_E_CORPO, _RETORNO_ANTECIPADO_SEM_CHAVES,
                             "retorno antecipado sem chaves antes da guarda"),
                    "retorno antecipado sem chaves (o `if` controla SO o `return`)")

    # ------------------------------------------- 3. o pair do RV-46/DWA-2 continua no lugar
    # A linha continua POR PERSONAGEM (nao regride para a varredura de todos): o `AurasVivas(receptor)`
    # e o proprio resolvedor continuam presos no fonte (o teste `t_shrine_dois_personagens` cobre o
    # interior do `AurasVivas`; aqui basta provar que o `AcumuladoShrines` continua pedindo o receptor).
    acumulado = rec.corpo_do_metodo(fonte, "public static string AcumuladoShrines(string chaveDaTooltip)")
    arc.exigir("AurasVivas(receptor)" in rec.codigo_efetivo(acumulado),
               "`AcumuladoShrines` deixou de pedir as auras do RECEPTOR (`AurasVivas(receptor)`): "
               "a linha deixou de ser por personagem (RV-46/RV-50)")

    print("conforme: Receptor le o personagem sob o cursor ANTES do selecionado (fora do shrine), "
          "com a fonte do jogo, a guarda do ground effect na POLARIDADE certa (GATEANDO o corpo, no "
          "CAMINHO EFETIVO) e o RETORNO EFETIVO do campo do jogo; 11 iscas de FONTE + 1 de ORDEM "
          "reprovam e o CONTROLE NEGATIVO (o `if` SEM chaves antes da guarda) passa (RV-50TF5)")


if __name__ == "__main__":
    arc.main(META, corpo)
