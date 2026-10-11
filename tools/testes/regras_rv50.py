#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rv50.py - a REGRA do RV-50 lida no FONTE do `ShrineAuraPatch.cs` (familia TST-2).

O DEFEITO (card t_9fc78584, relato do dono, 03/10, com imagem)
--------------------------------------------------------------
`linha 'Your active shrine auras' mostra valores de TODOS (deve ser so o personagem
selecionado; inimigo sai no tooltip DELE; dobro com worship CORRETO)`.

RAIZ (provada no decompilado do build atual, nao em leitura de prosa):

  * `Tooltip.TooltipCharacter` NAO e "o personagem da tooltip": e
    `GameLogic.instance.CurrentlySelectedCharacter` (decompilado l.213124-213133). O resolvedor
    antigo (`Receptor`) olhava SO ele -> a linha "Your active shrine auras" saia SEMPRE com os
    valores do SELECIONADO;
  * a tooltip de um status de shrine e montada em `Tooltip.ShowActionStatusTooltip(StatusIcon)`
    -> `ShowActionStatusTooltip(info, source, target, ...)` (l.214067-214073) e o `LocalizePatch`
    anexa a linha a QUALQUER descricao da familia (`IsShrineKey`). Ou seja: no tooltip do icone de
    buff de um INIMIGO a linha saia com o numero de OUTRO personagem (o selecionado) - o defeito;
  * o personagem SOB O CURSOR (party ou inimigo) o jogo expoe em
    `PlayerInfoWindow.currentCharacter` (l.151757): `HexCellManager.CurrentlyHoveringHexCell` chama
    `playerInfoWindow.ShowPlayerInfoWindow(player)` para QUALQUER personagem do hex, inclusive
    inimigo (`ShouldShowPlayerInfoWindow` aceita `TeamIndex != 0`, l.121521-121526 + l.151776-151786);
  * o tooltip do SHRINE (ground effect) NAO tem personagem: `Tooltip.ShowGroundEffectTooltip` liga
    `Tooltip.ShowingGroundEffect` no comeco (l.214157) e o `ShowTooltip` desliga (l.215141). A spec do
    dono: ali a linha mostra so o SELECIONADO.

O CONSERTO QUE ESTE ARQUIVO COBRA NO FONTE
------------------------------------------
  1. `Receptor` le o PERSONAGEM SOB O CURSOR (`PersonagemSobOCursor()`) ANTES do selecionado
     (`Tooltip.TooltipCharacter`) - o inimigo sai no tooltip DELE;
  2. `Receptor` EXCLUI o tooltip do SHRINE - a guarda com a POLARIDADE exata
     `t == null || !t.ShowingGroundEffect` (RV-50R): ali continua o SELECIONADO;
  3. o helper `PersonagemSobOCursor()` le `GUIManager.instance.playerInfoWindow.currentCharacter`
     (a MESMA fonte do hover em combate), devolve esse campo pelo RETORNO EFETIVO
     (`return janela.currentCharacter;`, RV-50R) e nunca varre `AllCharacters`;
  4. os fallbacks antigos (`TooltipCharacter` -> `WorldCharacter` -> `Source`/`Target`) continuam.

ENDURECIMENTO RV-50TF3 — A GUARDA TEM DE GATEAR O CORPO
-------------------------------------------------------
Presenca nao e gate. A RV-50TF2 passou a exigir a SUB-STRING EXATA da polaridade no CAMINHO EFETIVO,
mas media POSICAO, nao GATE. Um decoy com a sub-string exata numa guarda VIVA porem VAZIA
(`if (t == null || !t.ShowingGroundEffect) { }`), seguido da guarda VIVA INVERTIDA
(`if (t != null && t.ShowingGroundEffect) { <corpo que le o CURSOR> }`), deixava a sub-string no
caminho efetivo e o corpo sob a guarda de sentido trocado — o shrine voltaria a usar o CURSOR e o
status do INIMIGO o SELECIONADO. A checagem agora EXIGE que `POLARIDADE_GUARDA` seja a CONDICAO do
`if` cujo BLOCO CONTEM a leitura do personagem sob o cursor (`CORPO_GATEADO`): ser a condicao da
guarda que GATEIA o corpo, nao so estar viva em algum lugar do metodo.

ENDURECIMENTO RV-50TF4 — A LEITURA TEM DE ESTAR NO CAMINHO EFETIVO DO BLOCO
-------------------------------------------------------------------------
Bloco nao e caminho efetivo. A RV-50TF3 passou a exigir que `POLARIDADE_GUARDA` fosse a CONDICAO
do `if` cujo BLOCO contem a leitura (`CORPO_GATEADO`), mas media PRESENCA TEXTUAL no bloco. Dois
decoys deixavam a leitura dentro do bloco da guarda CERTA e mesmo assim MORTA:
  FURO A - guarda INVERTIDA ANINHADA: `if (t == null || !t.ShowingGroundEffect) { if (t != null &&
    t.ShowingGroundEffect) { <leitura> } }` — dentro do bloco da externa a aninhada e SEMPRE falsa
    (e a NEGACAO logica dela, De Morgan);
  FURO B - corpo sob CODIGO MORTO: `if (t == null || !t.ShowingGroundEffect) { if (false) {
    <leitura> } }`.
A checagem agora EXIGE que a ocorrencia da leitura NO BLOCO esteja no CAMINHO EFETIVO — a MESMA
logica de codigo morto ja usada no RETORNO e na POLARIDADE (`_condicao_falsa_que_contem`),
generalizada para reconhecer TAMBEM a guarda que CONTRADIZ uma que a contem (a invertida aninhada,
por NEGACAO LOGICA De Morgan). Fecha a classe inteira (nao caso a caso): qualquer leitura morta
dentro do bloco e recusada, e o fonte vivo (leitura direta no bloco) segue conforme.

CORRECAO RV-50TF5 — O BLOCO SO E DA GUARDA SE O `{` ABRIR LOGO APOS A CONDICAO
-----------------------------------------------------------------------------------
A RV-50TF4 passou a olhar o CAMINHO EFETIVO dentro do bloco, mas `_guardas_que_contem` ainda
atribuia a um `if` o PRIMEIRO `{` do texto depois do `)` (`codigo.find("{", fecha)`), sem exigir
que esse `{` ABRISSE aquele `if`. Um `if` SEM chaves (`if (cond) return x;`) controla APENAS a
instrucao imediata; ele recebia o bloco de uma guarda POSTERIOR e virava uma "guarda que contem" a
leitura. Com um retorno antecipado legitimo e SEM chaves cuja condicao e a INVERSA da guarda certa
(`if (t != null && t.ShowingGroundEffect) return null;`, estilo C# comum) o FALSO POSITIVO era
certeiro: o `if` sem chaves e a guarda certa sao negacoes logicas (De Morgan), entao a leitura
VIVA dentro do bloco da certa era marcada como MORTA e o fonte correto REPROVAVA. Agora o bloco so
e atribuido quando o proximo token NAO-BRANCO depois do `)` e `{` (o proprio bloco da guarda):
um `if` sem chaves nao entra na lista de guardas, e a contradicao deixa de ser inventada.

O QUE ESTE ARQUIVO NAO COBRA (e por que)
----------------------------------------
A enumeracao dos ALVOS do Flame (`AlvosNaAreaDoFlame`, l.701) e a spec do dono de 30/09 (um alvo por
personagem na area) e esta presa pela familia `t_shrine_*` (`t_shrine_excesso_dano`: "um valor por
ALVO na area"). Muda-la sairia do escopo do RV-50 e mexeria nas auras de PERIGO (pendencia RV-49) -
por isso NAO entra aqui: este arquivo mede a ESCOLHA DO PERSONAGEM, nao a lista de alvos do Flame.

POR QUE FONTE E NAO COMPORTAMENTO
---------------------------------
O teste e PURO (roda no CI, sem o jogo e sem dotnet). O que se prova aqui e a FORMA do codigo que
escolhe o personagem; o numero na tela e conferido em jogo pelo dono. A regra do repositorio e que o
CODIGO do jogo vence - e este arquivo transcreve o que o motor faz, com `arquivo:linha`.
"""
import re

import arcabouco as arc
import recorte as rec

ASSINATURA_RECEPTOR = "private static Character Receptor(Tooltip tooltip, GameFunctionParameters parametros)"
ASSINATURA_SOB_CURSOR = "private static Character PersonagemSobOCursor()"

# RV-50R — A SUB-STRING EXATA da polaridade da guarda do shrine. A isca "guarda invertida"
# (`t != null && t.ShowingGroundEffect`) troca o SENTIDO da guarda SEM mudar o nome da flag: so
# exigir o nome `ShowingGroundEffect` presente nao prende a polaridade. Com a guarda invertida o
# ground effect ENTRA na leitura do personagem sob o cursor -> o shrine usaria o CURSOR e o
# status do INIMIGO o SELECIONADO (a mesma classe do defeito do RV-50, de ponta-cabeca).
POLARIDADE_GUARDA = "t == null || !t.ShowingGroundEffect"

# RV-50R — O RETORNO EFETIVO do helper: a linha que `PersonagemSobOCursor` de fato executa para
# devolver o campo do jogo. As substrings `playerInfoWindow`/`currentCharacter` soltas no corpo
# NAO bastam: um `return janela.currentCharacter;` dentro de `if (false)` deixa as duas presentes
# e o helper cai SEMPRE no `return null` (o personagem sob o cursor nunca e lido).
RETORNO_EFETIVO = "return janela.currentCharacter;"

# RV-50TF3 — A LEITURA que o BLOCO da guarda do shrine tem de GATEAR. Nao basta a SUB-STRING EXATA
# estar no CAMINHO EFETIVO (`_ocorrencia_no_caminho_efetivo`): ela tem de ser a CONDICAO do `if`
# cujo BLOCO contem esta leitura. Um decoy VIVO-e-VAZIO
# (`if (t == null || !t.ShowingGroundEffect) { }`) seguido da guarda VIVA INVERTIDA
# (`if (t != null && t.ShowingGroundEffect) { <leitura> }`) tem a sub-string viva no caminho efetivo
# e mesmo assim poe o CURSOR no shrine (o defeito de ponta-cabeca do RV-50).
CORPO_GATEADO = "PersonagemSobOCursor()"


def _corpo(codigo, assinatura):
    """O corpo do metodo pelo casamento de chaves (FORMATO-3); None se a assinatura sumiu."""
    try:
        return rec.corpo_do_metodo(codigo, assinatura)
    except arc.Falhou:
        return None


def _casa_parentese(codigo, i_abertura):
    """Indice do `)` que casa com o `(` em `i_abertura` (literal-aware); None se nao fecha."""
    nivel, p = 0, i_abertura
    while p < len(codigo):
        c = codigo[p]
        if c in "\"'":
            p = rec.fim_do_literal(codigo, p)
            continue
        if c == "(":
            nivel += 1
        elif c == ")":
            nivel -= 1
            if nivel == 0:
                return p
        p += 1
    return None


def _proximo_nao_branco(codigo, i):
    """Indice do primeiro caractere NAO-BRANCO em/depois de `i`; `len(codigo)` se so houver branco.

    RV-50TF5 — e o que distingue um `if` COM bloco (`if (cond) { ... }`, o `{` e o proximo token
    depois do `)`) de um `if` SEM chaves (`if (cond) return x;`, que controla APENAS a instrucao
    imediata). O `codigo_efetivo` ja apagou os comentarios, entao um `/* ... */` entre o `)` e o `{`
    nao interfere: sobra o branco e o `{` continua sendo o proximo token nao-branco.
    """
    n = len(codigo)
    while i < n and codigo[i].isspace():
        i += 1
    return i


# ------------------------------------------------- negacao logica de guarda ---
# RV-50TF4 — O QUE SEPARA UMA GUARDA EFETIVA DE UMA GUARDA INVERTIDA ANINHADA. Uma guarda
# `if (C_aninhada)` dentro do bloco de `if (C_externa)` esta MORTA quando C_aninhada e a
# NEGACAO LOGICA de C_externa: dentro do bloco a externa e VERDADEIRA, entao a aninhada e
# SEMPRE falsa e o corpo que ela gateia e INALCANCAVEL. E o FURO A da RV-50TF3R — o corpo
# (`PersonagemSobOCursor()`) fica no bloco da guarda CERTA, mas sob a INVERTIDA ANINHADA.
# A deteccao e por ARVORE (De Morgan), nao por "parecido": so casa quando a condicao negada
# bate ESTRUTURALMENTE com a outra — sem falso positivo que reprovasse o fonte vivo.


def _tokeniza_logica(expr):
    """Tokens de uma condicao booleana: '&&', '||', '!', '(', ')' e ('ATOMO', texto)."""
    toks, i, n = [], 0, len(expr)
    while i < n:
        c = expr[i]
        if c.isspace():
            i += 1
            continue
        if expr.startswith("&&", i):
            toks.append("&&"); i += 2; continue
        if expr.startswith("||", i):
            toks.append("||"); i += 2; continue
        if c == "(":
            toks.append("("); i += 1; continue
        if c == ")":
            toks.append(")"); i += 1; continue
        if c == "!" and not expr.startswith("!=", i):
            toks.append("!"); i += 1; continue
        j = i
        while j < n:
            if expr.startswith("&&", j) or expr.startswith("||", j):
                break
            if expr[j] in "()":
                break
            if expr[j] == "!" and not expr.startswith("!=", j):
                break
            j += 1
        toks.append(("ATOMO", re.sub(r"\s+", "", expr[i:j])))
        i = j
    return toks


def _nega_texto_atomo(atom):
    """A negacao de um ATOMO comparativo: `a == b` -> `a != b`, `a >= b` -> `a < b`, etc."""
    for op, inverso in (("==", "!="), ("!=", "=="), (">=", "<"), ("<=", ">"),
                        (">", "<="), ("<", ">=")):
        k = atom.find(op)
        if k > 0:
            return atom[:k] + inverso + atom[k + len(op):]
    if atom.lower() == "true":
        return "false"
    if atom.lower() == "false":
        return "true"
    if atom.startswith("!"):
        return atom[1:]
    return "!" + atom


def _arvore_logica(expr):
    """A ARVORE da condicao: ('atom', t) | ('not', no) | ('and', [nos]) | ('or', [nos])."""
    toks = _tokeniza_logica(expr)
    pos = [0]

    def _primario():
        t = toks[pos[0]]
        if t == "(":
            pos[0] += 1
            no = _ou()
            arc.exigir(pos[0] < len(toks) and toks[pos[0]] == ")",
                       "parentese nao fecha na condicao %r" % expr)
            pos[0] += 1
            return no
        arc.exigir(isinstance(t, tuple), "esperava um atomo na condicao %r" % expr)
        pos[0] += 1
        return ("atom", t[1])

    def _nao():
        if pos[0] < len(toks) and toks[pos[0]] == "!":
            pos[0] += 1
            return ("not", _nao())
        return _primario()

    def _e():
        nos = [_nao()]
        while pos[0] < len(toks) and toks[pos[0]] == "&&":
            pos[0] += 1
            nos.append(_nao())
        return nos[0] if len(nos) == 1 else ("and", nos)

    def _ou():
        nos = [_e()]
        while pos[0] < len(toks) and toks[pos[0]] == "||":
            pos[0] += 1
            nos.append(_e())
        return nos[0] if len(nos) == 1 else ("or", nos)

    no = _ou()
    arc.exigir(pos[0] == len(toks), "sobrou token na condicao %r" % expr)
    return no


def _nega_arvore(no):
    """A negacao de uma arvore logica, com De Morgan empurrada ate os ATOMOS."""
    if no[0] == "atom":
        return ("atom", _nega_texto_atomo(no[1]))
    if no[0] == "not":
        return no[1]
    if no[0] == "and":
        return ("or", [_nega_arvore(f) for f in no[1]])
    return ("and", [_nega_arvore(f) for f in no[1]])


def _negacao_logica(a, b):
    """`b` e a NEGACAO LOGICA (De Morgan) de `a`? Comparacao por ARVORE, nao por texto solto."""
    try:
        return (_nega_arvore(_arvore_logica(a)) == _arvore_logica(b)
                or _nega_arvore(_arvore_logica(b)) == _arvore_logica(a))
    except Exception:
        return False


def _condicao_constante_falsa(condicao):
    """A condicao de um `if` e uma CONSTANTE FALSA (`false`, `0`, `!true`, `1 > 2`)?

    E o que separa um `if (false) { return campo; }` (retorno MORTO, o defeito que a checagem
    antiga deixava passar) de uma guarda de RUNTIME legitima (`janela != null && ...`). A
    condicao e avaliada como expressao booleana PURA (`&&`/`||`/`!` viram os operadores do
    Python): qualquer IDENTIFICADOR de runtime faz o `eval` falhar e a resposta e "nao e
    constante" — a guarda de verdade continua valendo.
    """
    if not re.fullmatch(r"[A-Za-z0-9_.\s!<>=&|()]+", condicao):
        return False
    expr = condicao.replace("&&", " and ").replace("||", " or ")
    expr = re.sub(r"!(?!=)", " not ", expr)
    expr = re.sub(r"\btrue\b", "True", expr, flags=re.IGNORECASE)
    expr = re.sub(r"\bfalse\b", "False", expr, flags=re.IGNORECASE)
    try:
        valor = eval(expr, {"__builtins__": {}}, {})  # so literais booleanos/numericos
    except Exception:
        return False
    return valor is False or valor == 0


def _guardas_que_contem(codigo, pos):
    """TODAS as guardas `if (...) { ... }` cujo bloco CONTEM `pos`: lista `(condicao, tamanho)`.

    O tamanho do bloco ordena da guarda mais INTERNA para a mais EXTERNA (o aninhamento faz o
    bloco interno ser MENOR). E a base do CODIGO MORTO: uma guarda e falsa por SI (constante
    falsa) ou por CONTRADIZER uma guarda que a CONTEM (a INVERTIDA aninhada, RV-50TF4).

    RV-50TF5 — O BLOCO SO E DA GUARDA SE O `{` ABRIR LOGO DEPOIS DA CONDICAO. Um `if` SEM chaves
    (`if (cond) return x;`) controla APENAS a instrucao imediata: o proximo `{` do texto pode ser o
    de um bloco MAIS ADIANTE (de outra guarda) e atribui-lo a este `if` inventava uma guarda que
    contem `pos`. Era o FALSO POSITIVO: um retorno antecipado sem chaves com a condicao INVERTIDA
    (`if (t != null && t.ShowingGroundEffect) return null;`) recebia o bloco da guarda CERTA e,
    sendo a negacao logica dela (De Morgan), marcava a leitura VIVA como morta. A abertura tem de
    ser o proximo token NAO-BRANCO depois do `)` (o `_proximo_nao_branco`); senao, o `if` nao tem
    bloco e nao entra nesta lista.
    """
    achados = []
    i = codigo.find("if")
    while i >= 0:
        antes_ok = i == 0 or not (codigo[i - 1].isalnum() or codigo[i - 1] == "_")
        abre = codigo.find("(", i + 2)
        if antes_ok and abre >= 0:
            fecha = _casa_parentese(codigo, abre)
            if fecha is not None:
                abertura = _proximo_nao_branco(codigo, fecha + 1)
                if abertura < len(codigo) and codigo[abertura] == "{":
                    try:
                        faixa = rec.faixa_bloco_balanceado(codigo, abertura)
                    except arc.Falhou:
                        faixa = None
                    if faixa is not None and faixa[0] <= pos <= faixa[1]:
                        achados.append((codigo[abre + 1:fecha].strip(), faixa[1] - faixa[0]))
        i = codigo.find("if", i + 1)
    return achados


def _condicao_falsa_que_contem(codigo, pos):
    """A condicao da guarda mais INTERNA que torna `pos` INALCANCAVEL; None se alcancavel.

    DUAS formas de guarda MORTA (RV-50TF3 + RV-50TF4), ambas cobertas de uma vez so:
      * a condicao e uma CONSTANTE FALSA (`if (false) { ... }`): o corpo sob ela nunca roda;
      * a condicao e a NEGACAO LOGICA de uma guarda que a CONTEM (`if (marca) { ... if (!marca)`
        `{ <pos> } ... }`): dentro do bloco da externa a aninhada e SEMPRE falsa -> pos MORTO.
    Sem a segunda, o corpo sob a guarda VIVA INVERTIDA *aninhada* na certa passava (o FURO A da
    RV-50TF3R). Devolve o TEXTO da condicao da guarda mais interna assim; None quando `pos` nao
    esta sob nenhuma. O recorte do bloco e o ESTRUTURAL do `recorte.py` (casamento de chaves).
    """
    guardas = _guardas_que_contem(codigo, pos)
    guardas.sort(key=lambda g: g[1])          # da mais INTERNA (bloco menor) para a mais externa
    for indice, (condicao, _) in enumerate(guardas):
        if _condicao_constante_falsa(condicao):
            return condicao
        for externa, _ in guardas[indice + 1:]:
            if _negacao_logica(condicao, externa):
                return condicao
    return None


def _sem_texto_literal(codigo):
    """O codigo com o CONTEUDO dos literais de string/char APAGADO (mesmo comprimento e indices).

    `rec.codigo_efetivo` remove COMENTARIO mas PRESERVA os literais — e uma mensagem de log pode
    CITAR o nome de um campo (`"... TooltipCharacter indisponivel ..."`), o que faria uma busca por
    `TooltipCharacter` casar o TEXTO do log em vez da LEITURA do campo (`t.TooltipCharacter`,
    o furo ii da revisao RV-50TFR). Apagar so o miolo dos literais (mantendo as aspas) deixa a
    busca casar apenas o CODIGO de verdade; blank in-place preserva a POSICAO de cada token, entao
    o indice devolvido continua valendo no texto original (o `_condicao_falsa_que_contem` casa igual).
    """
    saida = list(codigo)
    i, n, literal = 0, len(codigo), None
    while i < n:
        c = codigo[i]
        if literal is not None:
            if c == "\\" and i + 1 < n:
                saida[i], saida[i + 1] = " ", " "
                i += 2
                continue
            if c == literal:
                literal = None
            else:
                saida[i] = " "
            i += 1
            continue
        if c in "\"'":
            literal = c
        i += 1
    return "".join(saida)


def _ocorrencia_no_caminho_efetivo(codigo, sub):
    """Indice da PRIMEIRA ocorrencia de `sub` FORA de qualquer guarda MORTA (`if (false) { ... }`).

    E o endurecimento EQUIVALENTE ao do RETORNO (RV-50R): a SUB-STRING EXATA dentro de um
    `if (false) { ... }` e CODIGO MORTO — ela nao prende a guarda que o metodo EXECUTA (o furo i
    da revisao RV-50TFR: a polaridade certa escondida em codigo morto, com a guarda VIVA invertida,
    passava VERDE). Devolve -1 quando TODAS as ocorrencias estao sob guarda morta (ou nao ha nenhuma).
    """
    i = codigo.find(sub)
    while i >= 0:
        if _condicao_falsa_que_contem(codigo, i) is None:
            return i
        i = codigo.find(sub, i + 1)
    return -1


def _guarda_gateia_o_corpo(codigo, sub_condicao, corpo_marca):
    """Existe um `if (<sub_condicao>) { ... }` cujo BLOCO, no CAMINHO EFETIVO, le `corpo_marca`?

    E o que separa a guarda VIVA que GATEIA o corpo (a leitura do personagem sob o cursor DENTRO do
    bloco `if (t == null || !t.ShowingGroundEffect) { ... }`) do DECOY vivo-e-VAZIO da RV-50TF3: a
    MESMA sub-string viva numa guarda sem corpo (`if (t == null || !t.ShowingGroundEffect) { }`),
    seguida da guarda VIVA INVERTIDA (`if (t != null && t.ShowingGroundEffect) { <corpo> }`) que
    gateia o corpo de verdade. A condicao e comparada pelo TEXTO do miolo do parentese (sem espaco
    nas pontas), o MESMO rigor da SUB-STRING EXATA que o resto do arquivo exige: nao basta a
    sub-string estar em algum lugar do CAMINHO EFETIVO, tem de ser a CONDICAO do `if` que abre o
    bloco onde o corpo vive.

    RV-50TF4 — PRESENCA NO BLOCO AINDA NAO E GATE: a leitura `corpo_marca` tem de estar no CAMINHO
    EFETIVO *dentro* do bloco. Uma guarda INVERTIDA ANINHADA (FURO A:
    `if (sub_condicao) { if (t != null && t.ShowingGroundEffect) { <corpo> } }`) ou um `if (false)`
    (FURO B) deixa a leitura textualmente no bloco, mas MORTA. A leitura e aceita so quando a
    ocorrencia NO BLOCO nao esta sob `_condicao_falsa_que_contem` (a MESMA logica de codigo morto
    do retorno e da polaridade, agora aplicada a POSICAO da leitura). O recorte do bloco e o
    ESTRUTURAL do `recorte.py` (casamento de chaves), como no resto do arquivo.
    """
    i = codigo.find("if")
    while i >= 0:
        antes_ok = i == 0 or not (codigo[i - 1].isalnum() or codigo[i - 1] == "_")
        abre = codigo.find("(", i + 2)
        if antes_ok and abre >= 0:
            fecha = _casa_parentese(codigo, abre)
            if fecha is not None and codigo[abre + 1:fecha].strip() == sub_condicao:
                # RV-50TF5 — o BLOCO so existe se o `{` abrir LOGO apos a condicao (proximo token
                # nao-branco). Um `if` SEM chaves (`if (sub_condicao) return x;`) controla so a
                # instrucao imediata: NAO se apropria do bloco de uma guarda posterior.
                abertura = _proximo_nao_branco(codigo, fecha + 1)
                if abertura < len(codigo) and codigo[abertura] == "{":
                    try:
                        faixa = rec.faixa_bloco_balanceado(codigo, abertura)
                    except arc.Falhou:
                        faixa = None
                    if faixa is not None:
                        pos = codigo.find(corpo_marca, faixa[0], faixa[1] + 1)
                        while pos >= 0:
                            if _condicao_falsa_que_contem(codigo, pos) is None:
                                return True
                            pos = codigo.find(corpo_marca, pos + 1, faixa[1] + 1)
        i = codigo.find("if", i + 1)
    return False


def violacoes(texto):
    """Lista de violacoes da regra do RV-50 no FONTE passado (lista vazia = conforme)."""
    falhas = []
    efetivo = rec.codigo_efetivo(texto)

    receptor = _corpo(efetivo, ASSINATURA_RECEPTOR)
    if receptor is None:
        return ["nao achei o resolvedor do receptor (`%s`) no fonte - o personagem da tooltip "
                "nao tem mais um lugar unico de resolucao" % ASSINATURA_RECEPTOR]

    # RV-50TF2 — AS BUSCAS POR IDENTIFICADOR SAO NO CODIGO SEM O TEXTO DOS LITERAIS. A mensagem de
    # log da catch CITA `TooltipCharacter`; buscar no corpo cru fazia `receptor.find("TooltipCharacter")`
    # casar o TEXTO do log (furo ii da RV-50TFR) em vez da LEITURA real `t.TooltipCharacter`.
    limpo = _sem_texto_literal(receptor)

    # 1. o personagem SOB O CURSOR entra no resolvedor E vem ANTES do selecionado.
    pos_sob = limpo.find("PersonagemSobOCursor()")
    pos_sel = limpo.find(".TooltipCharacter")
    if pos_sob < 0:
        falhas.append(
            "`Receptor` NAO le o personagem sob o cursor (`PersonagemSobOCursor()`): a linha volta a "
            "ser SEMPRE a do SELECIONADO (`TooltipCharacter` = `CurrentlySelectedCharacter`) e o "
            "INIMIGO ve o numero de outro personagem no tooltip DELE (o defeito do RV-50)")
    elif pos_sel < 0:
        falhas.append(
            "`Receptor` perdeu o fallback pelo personagem SELECIONADO (`TooltipCharacter`): sem "
            "personagem sob o cursor (o hover do SHRINE) nao ha de quem ler as auras")
    elif pos_sob > pos_sel:
        falhas.append(
            "`Receptor` le o personagem SOB O CURSOR DEPOIS do selecionado (`TooltipCharacter`): o "
            "selecionado VENCE e o personagem descrito pela tooltip (o inimigo) continua vendo o "
            "numero de outro - a ORDEM e a correcao do RV-50")

    # 2. o tooltip do SHRINE fica DE FORA: ali a linha mostra so o SELECIONADO. A SUB-STRING EXATA
    #    da polaridade (nao so o NOME da flag): a isca "guarda invertida"
    #    (`t != null && t.ShowingGroundEffect`) mantem `ShowingGroundEffect` no corpo e troca o
    #    SENTIDO — o ground effect passaria a LER o personagem sob o cursor, e o status do INIMIGO
    #    sairia com o SELECIONADO (o defeito do RV-50 de ponta-cabeca). So o nome nao prende isso.
    if "ShowingGroundEffect" not in receptor:
        falhas.append(
            "`Receptor` NAO exclui o tooltip do SHRINE (`ShowingGroundEffect`): no hover do shrine um "
            "personagem que por acaso esteja sob o cursor (ou a janela de info do chefe) passaria a "
            "decidir a linha - a spec do dono manda o shrine mostrar so o SELECIONADO (RV-50)")
    elif _ocorrencia_no_caminho_efetivo(limpo, POLARIDADE_GUARDA) < 0:
        # RV-50TF2 — A SUB-STRING EXATA tem de estar no CAMINHO EFETIVO (o mesmo endurecimento do
        # RETORNO): esconde-la em CODIGO MORTO (`if (false) { if (POLARIDADE_GUARDA) {} }`) com a
        # guarda VIVA invertida (`t != null && t.ShowingGroundEffect`) reintroduz a MESMA classe do
        # defeito do RV-50 (o shrine usaria o CURSOR e o status do INIMIGO o SELECIONADO).
        falhas.append(
            "`Receptor` NAO tem a guarda do SHRINE (`%s`) no CAMINHO EFETIVO: a SUB-STRING EXATA "
            "da polaridade certa so aparece em CODIGO MORTO (sob um `if (false) { ... }`) ou a "
            "guarda VIVA esta INVERTIDA (`t != null && t.ShowingGroundEffect`) - nos dois casos o "
            "ground effect ENTRA na leitura do personagem sob o cursor: o shrine usaria o CURSOR e "
            "a tooltip do status do INIMIGO sairia com o SELECIONADO (o defeito do RV-50 de "
            "ponta-cabeca)" % POLARIDADE_GUARDA)
    elif not _guarda_gateia_o_corpo(limpo, POLARIDADE_GUARDA, CORPO_GATEADO):
        # RV-50TF3 — A SUB-STRING EXATA no CAMINHO EFETIVO nao basta: ela tem de ser a CONDICAO do
        # `if` que GATEIA o corpo. O decoy VIVO-e-VAZIO (`if (POLARIDADE_GUARDA) { }`) deixa a
        # sub-string viva (a checagem RV-50TF2 passava VERDE) e o corpo fica sob a guarda VIVA
        # INVERTIDA (`if (t != null && t.ShowingGroundEffect) { <leitura do cursor> }`) — o ground
        # effect ENTRA na leitura do personagem sob o cursor e o shrine usaria o CURSOR, nao o
        # SELECIONADO (a classe do defeito do RV-50, de ponta-cabeca).
        # RV-50TF4 — ESTAR NO BLOCO tambem nao basta: a leitura tem de estar no CAMINHO EFETIVO
        # DENTRO do bloco. A guarda INVERTIDA ANINHADA (`if (POLARIDADE_GUARDA) { if (t != null &&
        # t.ShowingGroundEffect) { <leitura> } }`, FURO A) e o `if (false)` (FURO B) deixam a
        # leitura textualmente no bloco, mas MORTA — a checagem RV-50TF3 passava VERDE nos dois.
        falhas.append(
            "`Receptor` NAO tem a guarda do SHRINE (`%s`) que GATEIA o corpo do acesso: a SUB-STRING "
            "EXATA esta no CAMINHO EFETIVO, mas o bloco do `if` cuja condicao E ela NAO contem a "
            "leitura do personagem sob o cursor (`%s`) no seu CAMINHO EFETIVO — a leitura esta fora "
            "do bloco (numa guarda VIVA porem VAZIA), sob a guarda INVERTIDA ("
            "`t != null && t.ShowingGroundEffect`) ou MORTA dentro do bloco (a INVERTIDA ANINHADA "
            "`if (%s) { if (t != null && t.ShowingGroundEffect) { ... } }` ou um `if (false)`): "
            "prende a PRESENCA e nao o GATE, o ground effect volta a decidir o shrine (o CURSOR no "
            "lugar do SELECIONADO) e a tooltip do status do INIMIGO sai com o SELECIONADO (o defeito "
            "do RV-50 de ponta-cabeca)" % (POLARIDADE_GUARDA, CORPO_GATEADO, POLARIDADE_GUARDA))

    # 3. o helper le o personagem sob o cursor da fonte certa (o hover em combate do jogo).
    helper = _corpo(efetivo, ASSINATURA_SOB_CURSOR)
    if helper is None:
        falhas.append(
            "nao achei `PersonagemSobOCursor()`: o personagem sob o cursor precisa da fonte do jogo "
            "(`PlayerInfoWindow.currentCharacter`), nao de um campo inventado")
    else:
        if "playerInfoWindow" not in helper or "currentCharacter" not in helper:
            falhas.append(
                "`PersonagemSobOCursor` nao le `GUIManager.instance.playerInfoWindow.currentCharacter` "
                "- a fonte do hover em combate do jogo (`CurrentlyHoveringHexCell` -> "
                "`ShowPlayerInfoWindow`, decompilado l.121521-121526 + l.151757)")
        elif RETORNO_EFETIVO not in helper:
            falhas.append(
                "`PersonagemSobOCursor` NAO tem o RETORNO EFETIVO do campo do jogo (`%s`): estar "
                "certo em algum lugar do corpo nao basta - o retorno que o helper de fato executa tem "
                "de devolver o `currentCharacter` da janela (`playerInfoWindow`); sem ele o "
                "personagem sob o cursor nunca e lido (RV-50)" % RETORNO_EFETIVO)
        else:
            guarda_morta = _condicao_falsa_que_contem(helper, helper.find(RETORNO_EFETIVO))
            if guarda_morta:
                falhas.append(
                    "`PersonagemSobOCursor` devolve o campo do jogo (`%s`) sob uma guarda MORTA "
                    "(`if (%s)`): o retorno e INALCANCAVEL e o helper cai SEMPRE no `return null` - "
                    "as substrings estao no corpo, mas o personagem sob o cursor nunca chega a ser "
                    "lido (o defeito do RV-50)" % (RETORNO_EFETIVO, guarda_morta))
        if "AllCharacters" in helper:
            falhas.append(
                "`PersonagemSobOCursor` varre TODOS os personagens (`AllCharacters`): a linha deixaria "
                "de ser de UM e voltaria a somar/juntar personagens (o defeito do RV-50)")

    return falhas
