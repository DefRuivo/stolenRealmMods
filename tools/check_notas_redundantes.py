#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RV-15 — Varredura GLOBAL de notas redundantes / duplicadas nos tooltips.

O QUE ELE CAÇA (os tres defeitos que o usuario reportou em 30/09):

  1. NOTA == CHAVE .......... a nota repete exatamente o texto que ja estava la.
     Ex. real: `{ "Skill range is reduced to 1 hex.", "\n<color=...>Skill range is reduced to 1 hex.</color>" }`
     -> o tooltip mostra a frase DUAS vezes.

  2. NOTA CONTIDA NA CHAVE ...... a nota inteira ja aparece dentro do texto original
     (nao acrescenta nada ao jogador). Ex. real: o status `Sleep`, cuja chave ja dizia
     "Cannot move or perform actions and damage taken increased by 50%..." e cuja nota
     repetia "Cannot move or perform actions; damage taken is increased by 50%".

  3. NOTA QUE REPETE UM TRECHO LONGO ...... a nota repete o inicio da chave (>= N palavras
     em sequencia), o que na pratica le como eco.

  4. NOTA SEM O TOM DO NIVEL 2 (COR-1, 01/10) ...... a nota sai no tom do corpo do tooltip
     (nivel 1) em vez do tom escuro das explicacoes. A convencao dos tres niveis de cor esta
     em `docs/TEXTO-TOOLTIPS.md`: todo bloco do nivel 2 tem de carregar o marcador da cor de
     explicacao (`#C8B090`, trocado em runtime pela cor do campo lido no jogo). Sao conferidos
     os tres lugares onde uma nota nasce: os valores de `TextAppends`, os valores de `TextFixes`
     e o argumento de cada `AnexarNota(__result, ...)` do codigo.

     COR-2 (01/10) — O FURO FECHADO E AS DUAS REGRAS QUE FALTAVAM. A primeira versao (COR-1)
     so olhava as notas fundidas no formato `\n\n<color=#...>`: das 21 entradas de `TextFixes`
     com cor, ela conferia 11 e IGNORAVA 10 — e DUAS DAS 12 NOTAS DE SHRINE moravam justamente
     nas ignoradas (as de `Recover [0]% of max mana/health each turn`, formato de UMA quebra).
     Trocar a cor de uma nota fundida passava em silencio. Agora TODA cor de TODO valor de
     `TextFixes` e conferida, em qualquer formato, e valem duas regras explicitas:

       (a) `#808080` (e qualquer outra cor) e LEGITIMA **quando o PROPRIO JOGO ja escrevia essa
           cor na CHAVE** — e o markup do jogo preservado (o caso real: o bege de citacao
           `#808080` dos status, ex. `Curse of the Reaper`). O mod nao inventa cor: cor que so
           o mod escreveu tem de ser o marcador do nivel 2.
       (b) 'EXPLICACAO E EFEITO': o valor de uma entrada de `TextFixes` pode ser, no MESMO texto,
           a correcao da linha do jogo (nivel 1, sem cor nossa) E a nota (nivel 2). O criterio e
           o mesmo do item (a): a parte corrigida nao ganha cor; a parte que e nota carrega o
           marcador. Quem separa as duas e a cor que existe (ou nao) na chave do jogo.

     FIX-4 (01/10) — O COMENTARIO DE BLOCO (achado da REV-55). O COR-2 fez o parser ver as
     entradas com comentario de LINHA dentro do `{` (o formato 'chave em linha propria'); o
     comentario de BLOCO (`/* ... */`) antes da chave continuava escondendo a entrada: ela
     sumia da varredura (25 -> 24 blocos de nota) e a troca de cor nela NAO reprovava. As duas
     formas de comentario sao puladas agora — a prova esta em
     `tools/testes/contra-prova/cp_cor_comentario_bloco_*.py` (a isca reprova, a metade ok passa).
     COBERTURA REAL (PARSER-1R): no fonte do produto ha ZERO casos de comentario de BLOCO antes
     da chave (grep = 0), entao este conserto e exercido SO pela ilha sintetica — nao por
     nenhuma entrada real. Ele fica pronto para a primeira que use o formato.

     NAO cobertos de proposito (os outros formatos que a REV-55 levantou; o porque esta em
     `docs/TEXTO-TOOLTIPS.md` §7.7): cor de 8 digitos `#RRGGBBAA` (nada no repo emite — as
     tabelas usam `#RRGGBB`); espaco antes do fecha-angular `#RRGGBB >` (ninguem escreve); e a
     nota acrescentada FORA do `AnexarNota` (o caso real e do NIVEL 3, regra do `EhAzul`, coberta
     por `t_cores_niveis.py` — varrer 'todo sitio que produz nota' pede instrumento proprio).

  5. COMPRIMENTO (medida, NAO reprova) ...... lista as notas com quebra de linha INTERNA (o
     que o dono chama de parede de texto) e o comprimento de cada uma. Nao reprova de
     proposito: as notas aprovadas pelo dono tem tamanhos diferentes e quem decide encurtar e
     ele (ver docs/TEXTO-TOOLTIPS.md §4). Serve para medir antes/depois de uma mudanca de
     forma — a cor nao muda o comprimento.

Tambem lista as notas IRRELEVANTES conhecidas do usuario, que sao outro tipo de defeito
(explicar Armor onde Armor e FONTE de dano, nao mitigacao — `Battle Ready`, `Diamond Ice`);
essas sao resolvidas por regra no codigo, e aqui aparecem so para conferencia.

USO:  python tools/check_notas_redundantes.py [-v] [--fonte OUTRO.cs]
      -v  mostra tambem as notas OK (para conferir que a varredura esta vendo tudo)
      --fonte  confere OUTRO arquivo (usado pela isca da trava em `tools/testes/contra-prova/`;
               com fonte fora do repositorio o relatorio NAO e regravado)

Saida: docs/cobertura/revisao/RV-15-notas-redundantes.md  (e resumo no terminal)
Sai com codigo 1 se achar caso das familias 1, 2, 3 ou 4 — serve de trava de release.

CURADO A MAO x GERADO
---------------------
O que a ferramenta GERA termina na linha `<!-- fim-gerado -->`; tudo o que vier DEPOIS dessa
linha e escrito a mao, e relido do arquivo e regravado identico por `tools/preserva_curado.py`
— a ferramenta nao apaga trabalho curado (antes de 30/09 ela montava o arquivo inteiro com
`io.open(SAIDA, 'w')` e derrubava qualquer coisa acrescentada depois, o mesmo defeito que
apagou as 53 linhas do veredito do RV-14). Blocos `<!-- curado --> ... <!-- /curado -->`
tambem sao preservados.
"""

import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import preserva_curado  # noqa: E402  guarda do trecho curado a mao (ver o docstring dele)
import tabelas as _tab  # noqa: E402  o parser UNICO das tabelas do LocalizePatch.cs

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTE = os.path.join(RAIZ, 'BetterTooltips', 'Patches', 'LocalizePatch.cs')
SAIDA = os.path.join(RAIZ, 'docs', 'cobertura', 'revisao', 'RV-15-notas-redundantes.md')

BS = chr(92)
Q = chr(34)
NL = chr(10)

MIN_PALAVRAS_ECO = 6  # a partir de quantas palavras em sequencia a nota vira eco

# COR-1: o marcador do NIVEL 2 da convencao (docs/TEXTO-TOOLTIPS.md). Nas tabelas e o valor
# medido da cor de explicacao do proprio jogo; o gancho das notas o troca pela cor lida no campo
# (`Tooltip.specialDescColor` = #CBB396 conforme a leitura datada de 01/10 — ver COR-2 §7).
MARCADOR_NIVEL2 = '#C8B090'

# Toda cor de um valor, em qualquer formatacao (com `\n\n`, com `\n` ou sem quebra na frente).
COR_NO_VALOR = re.compile(r'<color=#([0-9A-Fa-f]{6})>')

# Argumentos de `AnexarNota(__result, X)` que NAO sao um texto literal do nivel 2:
#   `append`    -> valor da tabela TextAppends (a cor e conferida na tabela inteira);
#   `acumulado` -> bloco do NIVEL 3 (linha de auras ativas, cor azul propria).
ARG_ANEXAR_NEUTRO = ('append', 'acumulado')


def cores(valor):
    """Todas as cores `<color=#RRGGBB>` do texto, em MAIUSCULAS e na ordem do arquivo."""
    return [('#' + m.group(1)).upper() for m in COR_NO_VALOR.finditer(valor)]



def linha_decodificada(valor):
    """Nota sem markup, MAS com as quebras de linha reais (para medir 'parede de texto')."""
    v = re.sub(r'<color=#[0-9A-Fa-f]{6}>', '', valor)
    v = re.sub(r'</?[a-zA-Z]+>', '', v)
    v = v.replace(BS + 'n', NL)
    v = re.sub(r'\{STA=([^}]*)\}', r'\1', v)
    v = v.replace('@', '')
    return v.strip()


def notas_sem_cor(itens, fixas_todas, fonte):
    """Familia 4 (COR-1 + COR-2): as notas que NAO carregam o marcador do nivel 2. Sai uma lista de
    (onde, chave/arg, motivo) para o relatorio e para o exit code, mais a contagem do que foi
    conferido (para a trava nao poder voltar a olhar so parte da tabela em silencio)."""
    achados = []
    conferidos = {'TextAppends': 0, 'TextFixes': 0, 'TextFixes_blocos': 0}

    # TextAppends: o valor E a nossa nota (a chave e o texto do jogo) — toda cor tem de ser o
    # marcador do nivel 2. Uma cor que nao seja o marcador aqui e cor inventada: nao existe
    # markup do jogo num valor que o mod escreve do zero.
    for linha, com, chave, valor in itens:
        conferidos['TextAppends'] += 1
        todas = cores(valor)
        if not todas:
            achados.append(('TextAppends', chave, 'valor sem o marcador do nivel 2: %s' % valor[:90]))
            continue
        ruins = [c for c in todas if c != MARCADOR_NIVEL2]
        if ruins:
            achados.append(('TextAppends', chave,
                            'cor que nao e a do nivel 2 no valor: %s' % ' '.join(ruins)))

    # TextFixes — TODAS as entradas, em QUALQUER formato (o furo do COR-1 so olhava `\n\n<color=#`).
    # O valor pode ser, no MESMO texto, a CORRECAO da linha do jogo (nivel 1) E a nota (nivel 2):
    # 'explicacao E efeito'. Criterio mecanico: cor no valor que o JOGO ja escrevia na chave =
    # markup do jogo preservado (o `#808080` de citacao dos status, por exemplo); qualquer outra
    # cor e NOSSA e tem de ser o marcador do nivel 2.
    for linha, _com, chave, valor in fixas_todas:
        do_jogo = set(cores(chave))
        todas = cores(valor)
        if todas:
            conferidos['TextFixes'] += 1
        # BLOCOS do nivel 2 (uma entrada pode carregar mais de um): e o numero que a trava
        # declara ter conferido, e ele tem de casar com a contagem independente do teste.
        conferidos['TextFixes_blocos'] += sum(1 for c in todas if c == MARCADOR_NIVEL2)
        for c in todas:
            if c == MARCADOR_NIVEL2 or c in do_jogo:
                continue
            achados.append(('TextFixes', chave,
                            'cor que nao e a do nivel 2 nem do jogo (l.%d): %s' % (linha, c)))

    # Todo `AnexarNota(__result, X)` do codigo tem de envolver a nota (NotaDeExplicacao), usar a
    # entrada da tabela, o marcador literal ou ser o bloco do nivel 3.
    for m in re.finditer(r'AnexarNota\(__result,\s*([^;]*)\);', fonte):
        arg = m.group(1).strip()
        ok = (arg in ARG_ANEXAR_NEUTRO
              or 'NotaDeExplicacao(' in arg
              or MARCADOR_NIVEL2 in arg
              or 'MarcadorCorDeExplicacao' in arg
              or 'abreNota' in arg)
        if not ok:
            achados.append(('codigo', 'AnexarNota(__result, %s)' % arg[:80],
                            'nota acrescentada sem o marcador do nivel 2'))
    return achados, conferidos


def medidas_de_comprimento(itens, notas_fixadas):
    """Familia 5 (medida): notas com quebra de linha interna e o comprimento de cada uma."""
    with_break = []
    longest = []
    for origem, conjunto in (('TextAppends', itens), ('TextFixes', notas_fixadas)):
        for item in conjunto:
            if origem == 'TextAppends':
                linha, com, chave, valor = item
            else:
                chave, valor = item
                linha, com = 0, ''
            dec = linha_decodificada(valor)
            if not dec:
                continue
            quebras = dec.count(NL)
            rotulo = (com or chave or '(sem rotulo)')
            rotulo = re.sub(r'\s+', ' ', rotulo)[:70]
            if quebras:
                with_break.append((len(dec), quebras, origem, rotulo, dec))
            longest.append((len(dec), quebras, origem, dec))
    longest.sort(reverse=True)
    return with_break, longest[:5]


def bloco(fonte, nome):
    """Texto do dicionario `nome` da classe, pulando strings e os DOIS comentarios ao contar chaves.

    FONTE UNICA: `tools/tabelas.py` (PARSER-1). Antes o scanner vivia aqui; o comentario de
    BLOCO foi o conserto do FIX-4, e agora a correcao deixou de ter uma copia propria.
    """
    return _tab.bloco(fonte, nome)


def le_string(t, i):
    """Le uma string C# a partir da aspa em t[i]. Devolve (conteudo, proximo_indice)."""
    return _tab.le_string(t, i)


def pula_brancos_e_comentarios(texto, i):
    """Avanca `i` sobre espacos/quebras e comentarios de LINHA (`// ...`) e de BLOCO (`/* ... */`).

    COR-2 — a tabela tem entradas com COMENTARIO dentro do `{`, antes da chave ('chave em
    linha propria' + o motivo escrito; o caso do `Shapeshift Dragonkin` e de outras tres). Um
    parser que so pula espaco NAO ve essas entradas — elas nunca entram na varredura de cor.

    FIX-4 — o comentario de BLOCO `/* ... */` antes da chave tambem nao era pulado: a entrada
    sumia (25 -> 24 blocos) e a troca de cor nela passava em silencio. As DUAS formas sao
    puladas agora, e a implementacao e uma so (`tools/tabelas.py`).
    """
    return _tab.pula_brancos_e_comentarios(texto, i)


def entradas(texto, offset):
    """Pares (linha, comentario, chave, valor) na ordem do arquivo, pulando os DOIS comentarios.

    FONTE UNICA: `tools/tabelas.py`. `offset` = quebras de linha antes do bloco + 1 (a linha
    sai 1-based no arquivo). O comentario passa a incluir tambem o que vive DENTRO do `{`,
    antes da chave (antes o `com` dessas entradas saia vazio, mesmo com o texto escrito la).
    """
    return _tab.entradas(texto, offset)


def desmarca(v):
    """Tira o markup e devolve o texto puro, minusculo, com espacos normalizados."""
    v = re.sub(r'<color=#[0-9A-Fa-f]{6}>', ' ', v)
    v = re.sub(r'</?[a-zA-Z]+>', ' ', v)          # <i> <b> </color> etc.
    v = v.replace(BS + 'n', ' ')                  # o escape de quebra de linha
    v = re.sub(r'\{STA=([^}]*)\}', r'\1', v)      # token de status -> nome
    v = v.replace('@', ' ')
    v = re.sub(r'\s+', ' ', v)
    return v.strip().lower()


def palavras(t):
    return [p for p in re.findall(r'[a-z0-9%]+', t) if len(p) > 1]


def maior_sequencia_comum(a, b):
    """Maior numero de palavras SEGUIDAS de `a` que aparecem tambem em `b`."""
    pa, pb = palavras(a), palavras(b)
    if not pa or not pb:
        return 0
    conj = set()
    for n in range(2, len(pb) + 1):
        for i in range(len(pb) - n + 1):
            conj.add(' '.join(pb[i:i + n]))
    melhor = 0
    for n in range(len(pa), 1, -1):
        for i in range(len(pa) - n + 1):
            if ' '.join(pa[i:i + n]) in conj:
                return n
    return melhor


def main():
    verbose = '-v' in sys.argv
    # `--fonte OUTRO.cs` (COR-2): aponta a varredura para OUTRO arquivo. E o que permite a isca
    # versionada (`tools/testes/contra-prova/cp_cor_nota_fundida_*.py`) plantar a troca de cor numa
    # COPIA e provar que a trava reprova — sem tocar no `LocalizePatch.cs` de verdade. Com uma
    # fonte que nao e a do repositorio o relatorio NAO e regravado (nao se mede o produto com a
    # copia de uma isca).
    fonte_path = FONTE
    for i, a in enumerate(sys.argv):
        if a == '--fonte' and i + 1 < len(sys.argv):
            fonte_path = sys.argv[i + 1]
    eh_fonte_do_repo = os.path.abspath(fonte_path) == os.path.abspath(FONTE)
    if not os.path.exists(fonte_path):
        print('nao achei %s' % fonte_path)
        return 2
    fonte = io.open(fonte_path, encoding='utf-8').read()
    bloco_app, k_app = bloco(fonte, 'TextAppends')
    itens = entradas(bloco_app, fonte[:k_app].count(NL) + 1)

    # COR-1/COR-2: TODAS as entradas de `TextFixes` sao conferidas (a primeira versao so olhava as
    # do formato `\n\n<color=#...>` e deixava 10 das 21 em silencio — duas notas de SHRINE entre
    # elas). `notas_fixadas` (com o marcador) continua sendo o conjunto que a medida de comprimento
    # usa: sao as notas fundidas de verdade.
    bloco_fix, k_fix = bloco(fonte, 'TextFixes')
    # A linha reportada e a do ARQUIVO: `entradas` conta as quebras DENTRO do bloco e soma o
    # deslocamento em LINHAS do inicio dele (antes vinha o indice em CARACTERES, e o relatorio
    # imprimia um numero absurdo — o caso de teste do COR-2 pegou isso).
    fixas_todas = entradas(bloco_fix, fonte[:k_fix].count(NL) + 1)
    notas_fixadas = [(chave, valor) for _, _, chave, valor in fixas_todas
                     if MARCADOR_NIVEL2 in cores(valor)]
    sem_cor, conferidos = notas_sem_cor(itens, fixas_todas, fonte)
    quebradas, maiores = medidas_de_comprimento(itens, notas_fixadas)

    iguais, contidas, ecos, ok = [], [], [], []
    for linha, com, chave, valor in itens:
        c, v = desmarca(chave), desmarca(valor)
        if not v:
            ok.append((linha, com, chave, valor, 'nota vazia (so cor/markup)'))
        elif v == c:
            iguais.append((linha, com, chave, valor))
        elif len(v) > 12 and v in c:
            contidas.append((linha, com, chave, valor))
        else:
            n = maior_sequencia_comum(v, c)
            if n >= MIN_PALAVRAS_ECO:
                ecos.append((linha, com, chave, valor, n))
            else:
                ok.append((linha, com, chave, valor, 'unica'))

    L = []
    L.append('# RV-15 - Notas redundantes / duplicadas nos tooltips')
    L.append('')
    L.append('Gerado por `tools/check_notas_redundantes.py` a partir de `BetterTooltips/Patches/LocalizePatch.cs`.')
    L.append('')
    L.append('O que a ferramenta **gera** termina na linha `<!-- fim-gerado -->`; tudo o que vier')
    L.append('depois dela e escrito a mao e **nunca** e reescrito (ver `tools/preserva_curado.py`).')
    L.append('')
    L.append('Uma nota existe para dizer o que o texto **nao** diz. Quando ela repete o proprio texto,')
    L.append('o jogador le a mesma frase duas vezes e a explicacao perde credito - foi o que o usuario')
    L.append('reportou em 30/09 (`Blinding Lights` duplicado, `Blind`/`Sleep` redundantes,')
    L.append('`Praying Shot`/`Chok` na mesma familia).')
    L.append('')
    L.append('## Resumo')
    L.append('')
    L.append('| caso | quantas | o que significa |')
    L.append('|---|---|---|')
    L.append('| nota == chave | **%d** | texto e nota sao a MESMA frase: aparece duplicado na tela |' % len(iguais))
    L.append('| nota contida na chave | **%d** | a nota inteira ja esta no texto: nao acrescenta nada |' % len(contidas))
    L.append('| nota ecoa >= %d palavras da chave | **%d** | repete o inicio do texto em sequencia |' % (MIN_PALAVRAS_ECO, len(ecos)))
    L.append('| notas unicas (OK) | %d | dizem algo que o texto nao diz |' % len(ok))
    L.append('| nota **sem o tom do nivel 2** (COR-1/COR-2) | **%d** | sai no tom do corpo do tooltip em vez do tom das explicacoes |' % len(sem_cor))
    L.append('')
    L.append('Total de notas analisadas: **%d** (mais **%d** valor(es) de `TextFixes` com cor, com' % (len(itens), conferidos['TextFixes']))
    L.append('**%d** bloco(s) de nota do nivel 2; o resto e a linha do jogo com o markup dela).'
             % conferidos['TextFixes_blocos'])
    L.append('')
    L.append('A convencao dos tres niveis de cor (branco / tom mais escuro / azul), com a procedencia')
    L.append('declarada de cada cor, esta em [`docs/TEXTO-TOOLTIPS.md`](../../TEXTO-TOOLTIPS.md).')
    L.append('')

    def secao(titulo, itens_, extra=None):
        L.append('## %s' % titulo)
        L.append('')
        if not itens_:
            L.append('Nenhum caso. ')
            L.append('')
            return
        for it in itens_:
            L.append('- **l.%d** `%s`' % (it[0], (it[1] or '(sem comentario)')[:110]))
            L.append('  - chave: %s' % re.sub(r'\s+', ' ', it[2])[:190])
            L.append('  - nota : %s' % re.sub(r'\s+', ' ', it[3])[:190])
            if extra:
                L.append('  - %s' % extra(it))
            L.append('')

    secao('1. Nota identica a chave (DUPLICADO na tela)', iguais)
    secao('2. Nota inteiramente contida na chave (redundante)', contidas)
    secao('3. Nota que ecoa o texto', ecos, extra=lambda it: 'palavras em sequencia: **%d**' % it[4])

    L.append('## 4. Nota sem o tom do nivel 2 (COR-1; cobertura fechada no COR-2)')
    L.append('')
    L.append('O que a trava olha (COR-2, 01/10): **todo** valor de `TextAppends` e **todo** valor de')
    L.append('`TextFixes`, em **qualquer** formato de cor — a primeira versao so olhava as notas')
    L.append('fundidas no formato `\\n\\n<color=#...>` e deixava 10 das 21 entradas com cor de fora')
    L.append('(duas delas notas de SHRINE). Regras:')
    L.append('')
    L.append('- cor no valor que **nao** seja `%s` e que o **jogo nao tenha escrito na chave** -> caso;' % MARCADOR_NIVEL2)
    L.append('- cor que o jogo ja escrevia na chave (o `#808080` de citacao dos status) -> **legitima**;')
    L.append('- valor que e, no mesmo texto, a correcao da linha do jogo **e** a nota (`explicacao E')
    L.append('  efeito`) -> a parte corrigida nao ganha cor, a nota carrega o marcador.')
    L.append('')
    L.append('Conferido nesta execucao: **%d** valor(es) de `TextAppends`, **%d** valor(es) de' % (conferidos['TextAppends'], conferidos['TextFixes']))
    L.append('`TextFixes` com cor (**%d** bloco(s) de nota do nivel 2).' % conferidos['TextFixes_blocos'])
    L.append('')
    if not sem_cor:
        L.append('Nenhum caso: toda nota acrescentada pelo mod carrega o marcador `%s` ou uma cor que' % MARCADOR_NIVEL2)
        L.append('o proprio jogo escreveu (a cor de explicacao e resolvida em runtime pelo campo')
        L.append('`Tooltip.specialDescColor`, lido pelo gancho das notas — ver §7 da convencao).')
        L.append('')
    else:
        for onde, chave, motivo in sem_cor:
            L.append('- **%s** `%s`' % (onde, re.sub(r'\s+', ' ', chave)[:150]))
            L.append('  - %s' % motivo)
            L.append('')

    L.append('## 5. Comprimento das notas (medida — NAO reprova)')
    L.append('')
    L.append('Notas com **quebra de linha interna** (o que o dono chama de parede de texto) e o')
    L.append('comprimento de cada uma. O criterio esta em `docs/TEXTO-TOOLTIPS.md` §4: comprimento nao')
    L.append('reprova (as notas aprovadas pelo dono tem tamanhos diferentes); a cor nao muda nenhum')
    L.append('comprimento. Quem decide encurtar e o dono.')
    L.append('')
    L.append('| notas medidas | com quebra interna | maior nota (caracteres) |')
    L.append('|---|---|---|')
    L.append('| %d | **%d** | %d |' % (len(itens) + len(notas_fixadas), len(quebradas),
                                       maiores[0][0] if maiores else 0))
    L.append('')
    if quebradas:
        for tam, quebras, origem, com, dec in sorted(quebradas, reverse=True):
            L.append('- **%d car., %d quebra(s)** — `%s` — %s'
                     % (tam, quebras, origem, re.sub(r'\s+', ' ', com)[:60] or '(sem comentario)'))
            L.append('  - %s' % dec.replace(NL, ' / ')[:200])
            L.append('')
    else:
        L.append('Nenhuma nota com quebra de linha interna. ')
        L.append('')

    if verbose:
        L.append('## Notas unicas (OK)')
        L.append('')
        for it in ok:
            L.append('- l.%d `%s` -> %s' % (it[0], (it[1] or '')[:80], re.sub(r'\s+', ' ', it[3])[:120]))
        L.append('')

    os.makedirs(os.path.dirname(SAIDA), exist_ok=True)
    origem, n_linhas = 'nao regravado (--fonte fora do repositorio)', 0
    if eh_fonte_do_repo:
        try:
            origem, n_linhas = preserva_curado.grava(SAIDA, NL.join(L))
        except preserva_curado.CuradoPerdido as e:
            print('ABORTADO: %s' % e)
            return 3

    print('RV-15 - varredura de notas redundantes')
    print('  fonte .................... %s' % (os.path.relpath(fonte_path, RAIZ).replace(chr(92), '/')
                                               if eh_fonte_do_repo else fonte_path))
    print('  notas analisadas ......... %d' % len(itens))
    print('  nota == chave ............ %d  (duplicado na tela)' % len(iguais))
    print('  nota contida na chave .... %d' % len(contidas))
    print('  nota ecoando >= %d palavras %d' % (MIN_PALAVRAS_ECO, len(ecos)))
    print('  notas unicas (OK) ........ %d' % len(ok))
    print('  nota sem o tom do nivel 2  %d  (marcador %s ausente; %d bloco(s) de nota fundida '
          'conferido(s) em %d valor(es) de TextFixes com cor)'
          % (len(sem_cor), MARCADOR_NIVEL2, conferidos['TextFixes_blocos'], conferidos['TextFixes']))
    print('  notas com quebra interna . %d  (medida, NAO reprova)' % len(quebradas))
    print('  notas fundidas (TextFixes) %d' % len(notas_fixadas))
    print('  curado preservado ........ %d linha(s) a mao (%s)' % (n_linhas, origem))
    print('  relatorio: %s' % os.path.relpath(SAIDA, RAIZ).replace(chr(92), '/'))
    for it in iguais + contidas + ecos:
        print('    l.%d  %s' % (it[0], (it[1] or '')[:80]))
    for onde, chave, motivo in sem_cor:
        print('    SEM COR [%s] %s — %s' % (onde, chave[:70], motivo))
    return 1 if (iguais or contidas or ecos or sem_cor) else 0


if __name__ == '__main__':
    sys.exit(main())
