# -*- coding: utf-8 -*-
"""regras_bt_texto.py - o ESPELHO em Python das regras de TEXTO do BetterTooltips (fora de shrine).

O QUE E ESTE ARQUIVO
--------------------
As regras de texto do BetterTooltips vivem em C# (`BetterTooltips/Patches/`). Um teste de
logica pura nao carrega C#, entao ele confere uma regra REIMPLEMENTADA aqui. O risco obvio
- "o espelho concorda com ele mesmo" - e fechado de tres formas:

  1. PROCEDENCIA no CODIGO: cada funcao cita a linha do C# que ela espelha. Se o C# mudar, o
     `pin()` dos testes (que le o FONTE de verdade) quebra antes que o espelho envelheca em
     silencio.
  2. MATERIAL REAL: onde da (tabelas, notas), a regra roda sobre o `LocalizePatch.cs` de
     verdade, nao sobre um exemplo inventado.
  3. CONTRA-PROVA: cada regra aceita um `modo` DEFEITUOSO. A isca usa o modo defeituoso e
     REPROVA; o teste da suite usa o modo correto e PASSA. Comparar as duas metades e o que
     prova que a regra morde (ver tools/testes/contra-prova/cp_bt_*.py).

Este arquivo NAO muda comportamento de mod nenhum: e material de teste.
"""
import os
import re
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))          # tools/testes
RAIZ = os.path.dirname(os.path.dirname(DIR))              # raiz do repo
TOOLS = os.path.join(RAIZ, "tools")
LOCALIZE = os.path.join(RAIZ, "BetterTooltips", "Patches", "LocalizePatch.cs")
ATRIBUTO_PERCENTUAL = os.path.join(RAIZ, "BetterTooltips", "Patches", "AtributoPercentualPatch.cs")

if TOOLS not in sys.path:
    sys.path.insert(0, TOOLS)

if DIR not in sys.path:
    sys.path.insert(0, DIR)

import tabelas as _tab    # noqa: E402  o parser UNICO das tabelas (tools/tabelas.py)
import arcabouco as arc   # noqa: E402  os asserts/Falhou comuns (o recorte fala por ele)
import recorte as _rec    # noqa: E402  o recorte ESTRUTURAL (casamento de chaves), nunca janela


# --------------------------------------------------------------------------- #
# leitura do FONTE real
# --------------------------------------------------------------------------- #

def le_fonte(caminho=LOCALIZE):
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def pin(fonte, agulha, mensagem):
    """Confere que o FONTE de verdade contem `agulha`. Sem isso o espelho pode envelhecer sozinho.

    Devolve a POSICAO (indice) da agulha - usada para provar ORDEM (X aparece antes de Y).
    """
    pos = fonte.find(agulha)
    if pos < 0:
        raise AssertionError("PIN do fonte falhou: %s (nao achei %r)" % (mensagem, agulha[:70]))
    return pos


# --------------------------------------------------------------------------- #
# CENARIO 1 - UMA ENTRADA POR TEXTO (check_dupes x check_chave_compartilhada)
# --------------------------------------------------------------------------- #
# A regra: as tabelas do LocalizePatch sao `Dictionary<string,string>` - chave repetida NAO
# entra (`Add` estoura ArgumentException -> TypeInitializationException e o mod inteiro nao
# carrega; tools/check_dupes.py conta a historia). E a MESMA chave nas DUAS tabelas e defeito
# objetivo (o lookup e if/else if, a de TextAppends nunca roda; --estrito do
# check_chave_compartilhada TRAVA). Aqui o teste nao "chama a ferramenta": ele PLANTA o defeito
# e exige que a ferramenta morda.

def chaves_duplicadas(fonte, bloco):
    """Chave repetida dentro de UMA tabela, mordendo `check_dupes.chaves_do_bloco` com dado plantado.

    `fonte` e o TEXTO do .cs (o teste da o plantado e o real). Devolve {chave: n>1}.
    """
    if TOOLS not in sys.path:
        sys.path.insert(0, TOOLS)
    import check_dupes   # noqa: E402  (o dono da definicao de "entrada duplicada")
    from collections import Counter
    chaves = check_dupes.chaves_do_bloco(fonte, bloco)
    return {k: n for k, n in Counter(chaves).items() if n > 1}


def chaves_nas_duas_tabelas(fonte):
    """A MESMA chave em TextFixes e TextAppends (o defeito objetivo do BUG-32).

    Usa o parser UNICO (`tabelas.pares`), o mesmo que o `check_chave_compartilhada.py` usa.
    """
    fix = [k for k, _v in _tab.pares(fonte, "TextFixes")]
    app = [k for k, _v in _tab.pares(fonte, "TextAppends")]
    return sorted(set(fix) & set(app))


def roda_chave_compartilhada(fonte_caminho):
    """Roda a FERRAMENTA de verdade em --estrito contra um fonte. Devolve (codigo, saida).

    Existe para morder o BINARIO do detector (nao so o parser): a prova de que o modo estrito
    TRAVA o fonte plantado e APROVA o real.
    """
    ferramenta = os.path.join(TOOLS, "check_chave_compartilhada.py")
    proc = subprocess.run(
        [sys.executable, ferramenta, "--estrito", "--fonte", os.path.abspath(fonte_caminho)],
        cwd=RAIZ, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        universal_newlines=True, timeout=120,
    )
    return proc.returncode, proc.stdout or ""


# --------------------------------------------------------------------------- #
# CENARIO 2 - SUBSTITUICAO SEGURA
# --------------------------------------------------------------------------- #
# C#: `LocalizePatch.AplicarNotasDoFunil` l.2298-2303 - "So mexemos quando o texto exibido e o
# ingles original". O lookup e por texto EXATO (`TryGetValue(original)`, l.2315/2323): nem
# substring, nem mesmo-comeco, nem texto ja localizado casam.

def anexar_nota(texto, nota):
    """C# `AnexarNota` l.2033-2041: `texto.TrimEnd() + "\\n\\n" + nota.TrimStart('\\n')`."""
    if not nota:
        return texto
    return texto.rstrip() + "\n\n" + nota.lstrip("\n")


def substituir(original, exibido, fixes, appends, modo="estrito"):
    """Espelha o if/else do funil. So troca quando `exibido == original` (ingles cru).

    modo="estrito" = o comportamento de HOJE (l.2300 `if (__result != original) return;`).
    modo="contem"  = o DEFEITO: troca por substring (a isca usa este).
    """
    if original is None or exibido is None:
        return exibido
    if modo == "estrito":
        if exibido != original:
            return exibido
        if original in fixes:
            return fixes[original]
        if original in appends:
            return anexar_nota(exibido, appends[original])
        return exibido
    if modo == "contem":
        for chave, valor in fixes.items():
            if chave in exibido:
                return valor
        for chave, valor in appends.items():
            if chave in exibido:
                return anexar_nota(exibido, valor)
        return exibido
    raise ValueError("modo de substituicao desconhecido: %r" % modo)


# --------------------------------------------------------------------------- #
# CENARIO 3 - REGRA DO TOKEN `[N]`
# --------------------------------------------------------------------------- #
# A NOTA do mod nao pode carregar o token `[N]`: o pipeline de expressoes do jogo
# (`ApplyDescriptionExpressions`) roda DEPOIS do `Localize` e interpretaria o colchete como
# indice de expressao. Regra do projeto; o C# a cita em `AtributoPercentualPatch.NotaDoCalculo`
# (l.299-301) e nas guardas de ConvercaoAtributo/Hunger/BerserkersBlood/ReaperToll.
TOKEN = re.compile(r"\[\d+\]")


def tokens_de_nota(nota):
    return TOKEN.findall(nota)


def notas_das_tabelas(fonte):
    """Corpus das NOTAS (nivel 2) do fonte: valores de `TextAppends` + blocos `<color=#C8B090>`.

    Uma entrada de `TextAppends` E uma nota (o valor inteiro). Um valor de `TextFixes` pode
    carregar uma nota FUNDIDA - o bloco na cor do marcador (`MarcadorCorDeExplicacao` = C8B090,
    l.426). Sao essas as notas que precisam estar limpas de token.
    """
    corpus = []
    for chave, valor in _tab.pares(fonte, "TextAppends"):
        corpus.append(("TextAppends:" + chave[:48], valor))
    for chave, valor in _tab.pares(fonte, "TextFixes"):
        for m in re.finditer(r"<color=#C8B090>(.*?)</color>", valor, re.S):
            corpus.append(("TextFixes:" + chave[:48], m.group(1)))
    return corpus


def notas_com_token(corpus):
    return [(origem, nota, tokens_de_nota(nota)) for origem, nota in corpus if tokens_de_nota(nota)]


# --------------------------------------------------------------------------- #
# CENARIO 4 - TEXTO DO JOGO AUSENTE OU INESPERADO
# --------------------------------------------------------------------------- #
# C#: `Postfix` l.2248-2262 tira um SNAPSHOT de `__result`, roda `AplicarNotasDoFunil` dentro de
# try/catch e, na excecao, devolve o snapshot INTACTO + `RegistrarFalhaIgnorada` (l.2272-2288).
# Chave que nao existe mais / valor nulo: nao casa o lookup -> texto do jogo fica como veio.
# Nunca "pela metade": a unica atribuicao a `__result` no caminho de falha e o snapshot.

class FalhaIgnorada(Exception):
    pass


def _aplicar_funil(original, resultado, fixes, appends, dinamico=None):
    if original is None or resultado is None:
        return resultado
    if resultado != original:
        return resultado
    if original in fixes:
        return fixes[original]
    if original in appends:
        return anexar_nota(resultado, appends[original])
    if dinamico is not None:
        return dinamico(original, resultado)   # pode lancar / devolver None
    return resultado


def funil(original, resultado, fixes, appends, dinamico=None, modo="seguro"):
    """Espelha o Postfix. Devolve (texto, motivo_da_falha-ou-None).

    modo="seguro" = snapshot + try/catch (o comportamento de hoje).
    modo="cru"    = o DEFEITO: sem guarda - a excecao escapa e pode deixar texto pela metade.
    """
    if modo == "seguro":
        snapshot = resultado
        try:
            return _aplicar_funil(original, resultado, fixes, appends, dinamico), None
        except Exception as e:   # noqa: BLE001  (o C# pega Exception de proposito)
            return snapshot, "falha IGNORADA no postfix do funil (texto do jogo mantido intacto) - %s: %s" % (
                type(e).__name__, e)
    if modo == "cru":
        # O defeito: escreve no meio e so depois descobre que nao dava - o texto sai mordido.
        parcial = _aplicar_funil(original, resultado, fixes, appends, None)
        if dinamico is not None:
            parcial = dinamico(original, parcial)
        return parcial, None
    raise ValueError("modo de funil desconhecido: %r" % modo)


# --------------------------------------------------------------------------- #
# CENARIO 5 - O GUARD ANTES DO INDEXADOR (o indexador do motor LANCA)
# --------------------------------------------------------------------------- #
# C#: `AtributoPercentualPatch.MontaPartes` l.185-188 chama `EhAtributoPrimario(...)` ANTES de
# `personagem[atributo.name]` (l.200). O indexador `Character.this[string]` LANCA para nome
# desconhecido (`GetAttribute`, decompilado l.32662-32675) - so o guard impede a explosao.
ATRIBUTOS_DO_MOTOR = ("Might", "Dexterity", "Intelligence", "Vitality", "Reflex")


class IndexadorDoMotorLanca(Exception):
    """O `Character[atributo]` do jogo para nome desconhecido."""


def indexa_atributo(valores, nome):
    if nome not in valores:
        raise IndexadorDoMotorLanca("indexador do motor LANCA para nome desconhecido: %r" % nome)
    return valores[nome]


def valor_do_atributo(valores, atributo, primarios, modo="com_guarda"):
    """Espelha a ordem guard -> indexador. Devolve None quando o guard pula (nao indexa).

    modo="com_guarda" = `EhAtributoPrimario` antes (o comportamento de hoje).
    modo="sem_guarda" = o DEFEITO: indexa direto -> LANCA para atributo inexistente.
    """
    if modo == "com_guarda":
        if atributo not in primarios:
            return None
        return indexa_atributo(valores, atributo)
    if modo == "sem_guarda":
        return indexa_atributo(valores, atributo)
    raise ValueError("modo de guard desconhecido: %r" % modo)


# --------------------------------------------------------------------------- #
# CENARIO 6 - COMPOSICAO DA TOOLTIP (ordem, linha em branco, idempotencia)
# --------------------------------------------------------------------------- #
# C#: `LocalizePatch.CorEOrdemDoTooltip.Prefix` l.231-243. Tira as notas (por CONTEUDO,
# `TirarNotaDoMod` l.324-362) e a linha de auras/sinergia (por MARCADOR, `TirarBloco`
# l.260-302), junto com o separador que o `AnexarNota` escreveu (`InicioDoSeparador` l.380-392,
# ate DUAS quebras), e remonta: `corpo` + ("\n\n" + nota) por nota + ("\n\n" + aura) por ultimo.
# A linha de auras e SEMPRE a ultima coisa anexada.
MARCADOR_NOTA = "C8B090"
MARCADOR_AURA = "00D7FF"


def inicio_do_separador(corpo, pos):
    """C# `InicioDoSeparador` l.380-392: leva junto ate DUAS quebras antes do bloco."""
    ini = pos
    if ini > 0 and corpo[ini - 1] == "\n":
        ini -= 1
        if ini > 0 and corpo[ini - 1] == "\n":
            ini -= 1
    return ini


def _tirar_bloco(corpo, hexcor, ultimo, exigir=""):
    """C# `TirarBloco` l.260-302 (primeiro/ultimo bloco `<color=#hex>`, com `exigir` opcional)."""
    abre = "<color=#" + hexcor + ">"
    fecha = "</color>"
    i = corpo.rfind(abre) if ultimo else corpo.find(abre)
    while i >= 0:
        f = corpo.find(fecha, i)
        if f < 0:
            return False, corpo, None
        ini = inicio_do_separador(corpo, i)
        fim = f + len(fecha)
        texto = corpo[ini:fim].lstrip("\n").rstrip()
        if not exigir or exigir in texto:
            return True, corpo[:ini] + corpo[fim:], texto
        if ultimo:
            if i == 0:
                return False, corpo, None
            i = corpo.rfind(abre, 0, i)
        else:
            i = corpo.find(abre, i + 1)
    return False, corpo, None


def _tirar_nota(corpo, conteudos):
    """C# `TirarNotaDoMod` l.324-362: bloco cujo MIOLO pertence a `_conteudosDeNota`."""
    i = 0
    abre = "<color=#"
    fecha = "</color>"
    while i < len(corpo):
        j = corpo.find(abre, i)
        if j < 0:
            return False, corpo, None
        fecha_tag = corpo.find(">", j)
        if fecha_tag < 0:
            return False, corpo, None
        f = corpo.find(fecha, fecha_tag)
        if f < 0:
            return False, corpo, None
        if corpo[fecha_tag + 1:f] in conteudos:
            ini = inicio_do_separador(corpo, j)
            fim = f + len(fecha)
            return True, corpo[:ini] + corpo[fim:], corpo[ini:fim].lstrip("\n").rstrip()
        i = f + 1
    return False, corpo, None


def compoe(descricao, conteudos, aura_hex=MARCADOR_AURA, aura_exigir="aura",
           sinergia_hex=None, sinergia_exigir=None, modo="rv17"):
    """Espelha o `Prefix` l.231-243. Devolve o texto remontado.

    modo="rv17"         = corpo + notas (na ordem) + [sinergia + "\\n\\n" +] aura por ULTIMO.
    modo="aura_antes"   = o DEFEITO: aura anexada ANTES das notas (quebra a ordem).
    modo="sem_tirar"    = o DEFEITO: anexa sem extrair (2a passada DUPLICA).
    """
    if modo == "sem_tirar":
        corpo = descricao
        for conteudo in conteudos:
            corpo += "\n\n<color=#" + MARCADOR_NOTA + ">" + conteudo + "</color>"
        corpo += "\n\n<color=#" + aura_hex + ">" + aura_exigir + "</color>"
        return corpo

    sinergia = None
    if sinergia_hex:
        achou, descricao, sinergia = _tirar_bloco(descricao, sinergia_hex, False, sinergia_exigir or "")
    achou_aura, descricao, aura = _tirar_bloco(descricao, aura_hex, True, aura_exigir)

    notas = []
    achou, descricao, nota = _tirar_nota(descricao, conteudos)
    while achou:
        notas.append(nota)
        achou, descricao, nota = _tirar_nota(descricao, conteudos)

    cauda = None
    if achou_aura or sinergia is not None:
        if sinergia is not None:
            cauda = sinergia if not aura else sinergia + "\n\n" + aura
        else:
            cauda = aura

    corpo = descricao.rstrip()
    if modo == "aura_antes":
        if cauda:
            corpo += "\n\n" + cauda
        for bloco in notas:
            corpo += "\n\n" + bloco
        return corpo
    for bloco in notas:
        corpo += "\n\n" + bloco
    if cauda:
        corpo += "\n\n" + cauda
    return corpo


def defeitos_da_composicao(descricao, conteudos, modo="rv17"):
    """Conta os defeitos de uma composicao, pelo ESPECIFICADO (nao pelo resultado do modelo):

      * ORDEM - a linha de auras tem de ser a ULTIMA coisa anexada;
      * LINHA EM BRANCO - exatamente UMA entre o corpo e cada bloco (zero "\n\n\n");
      * IDEMPOTENCIA - passar de novo nao duplica nota nem linha.

    Devolve a lista de violacoes (vazia = composicao conforme).
    """
    saida = compoe(descricao, conteudos, modo=modo)
    violacoes = []

    # IDEMPOTENCIA: compor de novo o proprio resultado nao pode mudar nada.
    if modo != "sem_tirar":
        denovo = compoe(saida, conteudos, modo=modo)
        if denovo != saida:
            violacoes.append("IDEMPOTENCIA: a 2a passada mudou o texto (%r -> %r)" % (saida, denovo))
    else:
        denovo = compoe(saida, conteudos, modo=modo)
        if denovo != saida:
            violacoes.append("IDEMPOTENCIA: a 2a passada duplicou a nota/linha")

    # ORDEM: a aura tem de terminar o texto (nada anexado depois dela).
    pos_aura = saida.rfind("<color=#" + MARCADOR_AURA + ">")
    if pos_aura < 0:
        violacoes.append("ORDEM: sumiu a linha de auras")
    else:
        fecha_aura = saida.find("</color>", pos_aura)
        if fecha_aura < 0:
            violacoes.append("ORDEM: a linha de auras nao fecha com </color>")
        else:
            resto = saida[fecha_aura + len("</color>"):]
            if "<color=#" in resto:
                violacoes.append("ORDEM: ha bloco anexado DEPOIS da linha de auras")

    # LINHA EM BRANCO: nenhuma sequencia de 3+ quebras (bloco colado / linha orfa).
    if "\n\n\n" in saida:
        violacoes.append("LINHA EM BRANCO: ha 3+ quebras seguidas")

    return violacoes


# --------------------------------------------------------------------------- #
# CENARIO 7 - BUG-34: o guard de CONTEXTO nos DOIS pontos de feed (recorte ESTRUTURAL)
# --------------------------------------------------------------------------- #
# C#: `LocalizePatch` — cada ponto de FEED/COMBATE e uma classe anotada por `[HarmonyPatch]`
# (l.2190-2250), com o `Prefix` que ENTRA no contexto (`EntrarTextoDeFeed()`) e o `Finalizer`
# que SAI (`SairTextoDeFeed()`); o funil consulta `EmTextoDeFeed()` (l.2667) e as DUAS regras de
# afixo (Armor l.2676, Resistencia l.2694) pulam a nota DENTRO do contexto.
#
# BUG-34T — POR QUE O RECORTE AQUI E ESTRUTURAL. A conferencia antiga recortava uma JANELA de
# 2200 chars em volta de cada alvo. Do atributo do feed de TEXTO ate os tokens da entrada
# VIZINHA (o texto flutuante) vao menos que isso: a janela do PRIMEIRO bloco alcancava o SEGUNDO
# e aprovava a entrada de TEXTO com o `Prefix`/`Finalizer` arrancados. Medido (contra-prova em
# sandbox): remover `EntrarTextoDeFeed();`, `SairTextoDeFeed();` ou o `void Finalizer()` da
# entrada de TEXTO passava VERDE — so a entrada do texto FLUTUANTE estava de fato conferida.
# Aqui cada entrada e o BLOCO dela por CASAMENTO DE CHAVES (`recorte.py`): nao ha distancia,
# entao nao ha vizinho nenhum para emprestar o token. NUNCA alargar/afrouxar a janela.
ENTRADAS_DE_FEED = (
    ("feed de texto (Root.SendMessageWindowMessage / battle log)",
     '[HarmonyPatch(typeof(Root), nameof(Root.SendMessageWindowMessage))]'),
    ('texto flutuante (OverheadMessageDisplay.SpawnOverheadMessage)',
     '[HarmonyPatch(typeof(OverheadMessageDisplay), "SpawnOverheadMessage")]'),
)

# A flag de contexto: um CONTADOR `[ThreadStatic] int` (reentrada segura), nunca um booleano.
FLAG_DE_FEED = "private static int _profundidadeTextoDeFeed;"
LEITURA_DA_FLAG = "return _profundidadeTextoDeFeed > 0;"
ENTRA_NO_CONTEXTO = "_profundidadeTextoDeFeed++;"
SAI_DO_CONTEXTO = "_profundidadeTextoDeFeed--;"

# As DUAS regras de afixo do funil: a nota so entra FORA do contexto de feed.
GUARD_ARMOR = "if (!ehTextoDeFeed && !ehRotuloDeStatus && hasVerb && ArmorAffixRegex.IsMatch(original) &&"
GUARD_RESIST = "else if (!ehTextoDeFeed && !ehRotuloDeStatus && hasVerb && ResistAffixRegex.IsMatch(original) &&"

# O diagnostico do BUG-34 (1x por texto barrado, nomeando o caso) e os 4 NOMES do BUG-33.
DIAGNOSTICO_FEED = "_notasBarradasNoFeed.Add(original)"
MARCA_DIAGNOSTICO = "BUG-34: texto de feed/combate"
NOMES_DO_BUG33 = ("\"Increased Armor\",", "\"Reduced Resistances I\",",
                  "\"Reduced Resistances II\",", "\"Reduced Resistances III\",")

# O numero da checagem REMOVIDA (BUG-34T): existe SO para o teste comparar as duas, nunca como trava.
JANELA_REMOVIDA = 2200


def bloco_da_entrada_de_feed(fonte, alvo):
    """O BLOCO (atributo + declaracao anotada + corpo) da entrada de feed apontada por `alvo`.

    Recorte ESTRUTURAL por casamento de chaves (`recorte.corpo_do_metodo`): vai do `[HarmonyPatch...]`
    ate o `}` que casa com a classe anotada. Sem o alvo, devolve None; com chaves que nao fecham,
    FALHA ALTO. NUNCA e uma janela de caracteres.
    """
    if fonte.find(alvo) < 0:
        return None
    return _rec.corpo_do_metodo(fonte, alvo)


def falhas_da_entrada_de_feed(fonte, alvo, rotulo):
    """As violacoes da entrada de feed `alvo`, medidas DENTRO do BLOCO dela (por chaves).

    Lista vazia = a entrada esta conforme. Cada violacao nomeia o que faltou.
    """
    try:
        bloco = bloco_da_entrada_de_feed(fonte, alvo)
    except arc.Falhou as e:
        return ["o bloco de %s nao fecha nas chaves (o recorte estrutural falhou alto): %s" % (rotulo, e)]
    if bloco is None:
        return ["nao achei o alvo de %s (%s): a entrada de feed NAO existe — o caminho fica DESCOBERTO"
                % (rotulo, alvo)]
    efetivo = _rec.codigo_efetivo(bloco)   # comentario nao e codigo: `Entrar` citado nao conta
    viol = []
    if "EntrarTextoDeFeed();" not in efetivo:
        viol.append("o bloco de %s nao ENTRA no contexto: faltou `EntrarTextoDeFeed();` no Prefix" % rotulo)
    if "void Finalizer()" not in efetivo:
        viol.append("o bloco de %s nao tem `Finalizer`: a flag pode ficar PRESA se o metodo do jogo lancar"
                    % rotulo)
    if "SairTextoDeFeed();" not in efetivo:
        viol.append("o bloco de %s nao SAI do contexto: faltou `SairTextoDeFeed();` no Finalizer" % rotulo)
    return viol


def sem_trecho_no_bloco(fonte, alvo, trecho):
    """O mesmo fonte com `trecho` (1a ocorrencia) REMOVIDO de DENTRO do bloco estrutural de `alvo`.

    Existe para as iscas plantarem o defeito SEM depender de posicao: se o trecho nao estiver no
    bloco daquela entrada, a isca FALHA ALTO (plantar no vizinho nao e plantar neste).
    """
    bloco = bloco_da_entrada_de_feed(fonte, alvo)
    arc.exigir(bloco is not None and trecho in bloco,
               "a isca: %r nao esta dentro do bloco estrutural de %s" % (trecho, alvo))
    return fonte.replace(bloco, bloco.replace(trecho, "", 1), 1)


def falhas_do_guard_de_feed(fonte):
    """O ESTADO COMPLETO do BUG-34 no fonte. Lista vazia = conforme (o que o teste exige da fonte real).

    Cobre, por CRITERIO (nunca por distancia em caracteres): a flag CONTADORA e `[ThreadStatic]`;
    as DUAS entradas de feed, cada uma no proprio BLOCO estrutural (Prefix entra, Finalizer sai);
    o guard nas DUAS regras de afixo; o diagnostico do BUG-34; e o BUG-33 (4 nomes) intacto.
    """
    viol = []
    if "[ThreadStatic]" not in fonte:
        viol.append("a flag de contexto de feed perdeu o `[ThreadStatic]`")
    if FLAG_DE_FEED not in fonte:
        viol.append("a flag de contexto nao e um CONTADOR de profundidade (`%s`): a reentrada apaga "
                    "o contexto de fora" % FLAG_DE_FEED)
    if LEITURA_DA_FLAG not in fonte:
        viol.append("`EmTextoDeFeed()` deixou de ler a profundidade (`%s`)" % LEITURA_DA_FLAG)
    if ENTRA_NO_CONTEXTO not in fonte:
        viol.append("`EntrarTextoDeFeed()` deixou de incrementar (`%s`)" % ENTRA_NO_CONTEXTO)
    if SAI_DO_CONTEXTO not in fonte:
        viol.append("`SairTextoDeFeed()` deixou de decrementar (`%s`)" % SAI_DO_CONTEXTO)

    posicoes = []
    for rotulo, alvo in ENTRADAS_DE_FEED:
        posicoes.append(fonte.find(alvo))
        viol += falhas_da_entrada_de_feed(fonte, alvo, rotulo)
    if all(p >= 0 for p in posicoes) and posicoes[0] == posicoes[1]:
        viol.append("os dois alvos de feed sao o MESMO ponto: uma das entradas e alibi")

    if "bool ehTextoDeFeed = EmTextoDeFeed();" not in fonte:
        viol.append("o funil deixou de consultar o contexto de feed UMA vez por texto")
    if GUARD_ARMOR not in fonte:
        viol.append("a regra de ARMOR nao pula a nota no feed: faltou o `!ehTextoDeFeed` no ramo do "
                    "`ArmorAffixRegex`")
    if GUARD_RESIST not in fonte:
        viol.append("a regra de RESISTENCIA nao pula a nota no feed: faltou o `!ehTextoDeFeed` no ramo "
                    "do `ResistAffixRegex`")

    if DIAGNOSTICO_FEED not in fonte:
        viol.append("o funil deixou de logar que a nota foi barrada no feed (`%s`)" % DIAGNOSTICO_FEED)
    if MARCA_DIAGNOSTICO not in fonte:
        viol.append("a linha de diagnostico do BUG-34 deixou de nomear o caso (`%s`)" % MARCA_DIAGNOSTICO)

    for nome in NOMES_DO_BUG33:
        if nome not in fonte:
            viol.append("o BUG-33 deixou de proteger o NOME de status %s" % nome)
    return viol


def falhas_da_janela_2200(fonte):
    """A checagem REMOVIDA (BUG-34T): recorte por JANELA de 2200 chars em volta de cada alvo.

    Existe SO para o teste comparar as duas metades: a janela confere FAIXA. Ela NAO enxerga a
    entrada de TEXTO perder o Prefix/Finalizer, porque os tokens da entrada VIZINHA caem dentro
    dela. NUNCA use isto como trava — e o defeito, nao a regra.
    """
    viol = []

    def exigir(cond, msg):
        if not cond:
            viol.append(msg)

    exigir("[ThreadStatic]" in fonte, "sem `[ThreadStatic]`")
    exigir(FLAG_DE_FEED in fonte, "a flag nao e um contador `int`")
    exigir(LEITURA_DA_FLAG in fonte, "EmTextoDeFeed deixou de ler a profundidade")
    exigir(ENTRA_NO_CONTEXTO in fonte, "EntrarTextoDeFeed deixou de incrementar")
    exigir(SAI_DO_CONTEXTO in fonte, "SairTextoDeFeed deixou de decrementar")

    for rotulo, alvo in ENTRADAS_DE_FEED:
        i = fonte.find(alvo)
        if i < 0:
            viol.append("nao achei o alvo de %s" % rotulo)
            continue
        janela = fonte[i:i + JANELA_REMOVIDA]
        exigir("EntrarTextoDeFeed();" in janela, "o bloco de %s nao entra no contexto" % rotulo)
        exigir("SairTextoDeFeed();" in janela, "o bloco de %s nao sai do contexto" % rotulo)
        exigir("void Finalizer()" in janela, "o bloco de %s nao tem Finalizer" % rotulo)

    exigir("bool ehTextoDeFeed = EmTextoDeFeed();" in fonte, "o funil nao consulta o contexto")
    exigir(GUARD_ARMOR in fonte, "a regra de ARMOR nao pula no feed")
    exigir(GUARD_RESIST in fonte, "a regra de RESISTENCIA nao pula no feed")
    exigir(DIAGNOSTICO_FEED in fonte, "sem o log de nota barrada no feed")
    exigir(MARCA_DIAGNOSTICO in fonte, "sem a marca do BUG-34")
    for nome in NOMES_DO_BUG33:
        exigir(nome in fonte, "o BUG-33 perdeu %s" % nome)
    return viol


# --------------------------------------------------------------------------- #
# TABELAS DE CASO COMPARTILHADAS (teste da suite x isca usam A MESMA)
# --------------------------------------------------------------------------- #
# O par "reprova / passa" so prova quando as duas metades rodam o MESMO caso. Cada funcao
# abaixo devolve a LISTA DE VIOLACOES de uma regra para os casos daquele cenario: o teste da
# suite pede 0 com o modo correto; a isca pede 0 com o modo defeituoso (e recebe >0).

def violacoes_da_substituicao(real=None, modo="estrito"):
    """Casos do cenario 2 sobre as tabelas de verdade. 0 = substituicao segura conforme."""
    real = real or le_fonte()
    fixes = dict(_tab.pares(real, "TextFixes"))
    appends = dict(_tab.pares(real, "TextAppends"))
    ck_fix = next(iter(fixes))
    ck_app = next(iter(appends))
    casos = (
        ("texto ja localizado", ck_fix, "Texto ja traduzido para portugues.",
         "Texto ja traduzido para portugues."),
        ("chave como substring", ck_fix, "prefixo " + ck_fix + " sufixo",
         "prefixo " + ck_fix + " sufixo"),
        ("mesmo comeco, texto diferente", ck_fix, ck_fix + " e mais alguma coisa",
         ck_fix + " e mais alguma coisa"),
        ("exato (correcao)", ck_fix, ck_fix, fixes[ck_fix]),
        ("exato (nota)", ck_app, ck_app, anexar_nota(ck_app, appends[ck_app])),
    )
    viol = []
    for rotulo, original, exibido, esperado in casos:
        obtido = substituir(original, exibido, fixes, appends, modo)
        if obtido != esperado:
            viol.append("%s: esperado %r, obtido %r" % (rotulo, esperado, obtido))
    return viol


def violacoes_do_token(modo="real"):
    """Cenario 3. modo="real" = tabelas de verdade; modo="plantado" = nota com `[0]`."""
    if modo == "real":
        return notas_com_token(notas_das_tabelas(le_fonte()))
    if modo == "plantado":
        return notas_com_token([("plantado", "Cada stack concede +[0] Max Health por acerto.")])
    raise ValueError("modo de token desconhecido: %r" % modo)


def violacoes_do_funil(modo="seguro"):
    """Cenario 4: chave morta / expressao que nao avalia / valor nulo -> texto intacto + motivo."""
    fixes = {"Chave Viva": "corrigido"}
    appends = {"Com Nota": "\n<color=#C8B090>nota</color>", "Valor Nulo": None}

    def din_que_lanca(_original, _resultado):
        raise RuntimeError("a expressao do jogo nao avalia")

    casos = (
        ("chave que nao existe mais", "Chave Morta", "Chave Morta", None, False),
        ("expressao que nao avalia", "Texto Com [0]", "Texto Com [0]", din_que_lanca, True),
        ("valor nulo no dicionario", "Valor Nulo", "Valor Nulo", None, False),
    )
    viol = []
    for rotulo, original, resultado, dinamico, espera_motivo in casos:
        try:
            texto, motivo = funil(original, resultado, fixes, appends, dinamico=dinamico, modo=modo)
        except Exception as e:   # noqa: BLE001
            viol.append("%s: a excecao ESCAPOU (%s) - o texto do jogo nao ficou intacto"
                        % (rotulo, type(e).__name__))
            continue
        if texto != resultado:
            viol.append("%s: texto NAO ficou intacto (%r -> %r)" % (rotulo, resultado, texto))
        if espera_motivo and not motivo:
            viol.append("%s: a falha NAO foi declarada (escrita em silencio)" % rotulo)
    return viol


def violacoes_do_guard(modo="com_guarda"):
    """Cenario 5: o guard tem de pular atributo inexistente ANTES de o indexador lancar."""
    valores = {"Might": 100.0}
    primarios = ATRIBUTOS_DO_MOTOR
    viol = []
    v = valor_do_atributo(valores, "Might", primarios, modo)
    if v != 100.0:
        viol.append("atributo que existe devolveu %r (esperado 100.0)" % v)
    try:
        v = valor_do_atributo(valores, "Courage", primarios, modo)
        if v is not None:
            viol.append("atributo INEXISTENTE devolveu %r (esperado pular, None)" % v)
    except IndexadorDoMotorLanca as e:
        viol.append("atributo INEXISTENTE explodiu no indexador: %s" % e)
    return viol


def material_da_composicao():
    """O caso do cenario 6: CORPO + linha de auras + nota, com a aura ANTES da nota no texto de
    entrada (o prefixo tem de a mover para o fim). Sintetico, mas na forma que o §9.1 descreve."""
    nota = "Each stack grants another 10% Max Health."
    corpo = "Devour the life force of all enemies dealing 10 Shadow Damage."
    aura = "Active shrine auras: +10 Might"
    texto = (corpo + "\n\n<color=#" + MARCADOR_AURA + ">" + aura + "</color>"
             + "\n\n<color=#" + MARCADOR_NOTA + ">" + nota + "</color>")
    return texto, [nota]

