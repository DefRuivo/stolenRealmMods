#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tabelas.py — O PARSER UNICO das tabelas de texto do `LocalizePatch.cs`.

POR QUE ISTO EXISTE (a familia do defeito)
------------------------------------------
As tabelas `TextFixes` / `TextAppends` sao `Dictionary<string, string>` cheios de
entradas `{ "chave", "valor" }`. Elas convivem em DOIS formatos, porque as chaves
carregam texto real do jogo:

    { "chave", "valor" },                       // par na MESMA linha
    {                                            // 'chave em linha propria':
        // comment                               //   a chave pode ter COMENTARIO
        "chave",                                 //   (de LINHA ou de BLOCO)
        "valor"
    },

O defeito de ferramenta que este modulo fecha e sempre o mesmo, e ja apareceu
quatro vezes no projeto: um leitor que nao pula o COMENTARIO entre a abertura `{`
e a chave nao ve a entrada — ela some da varredura EM SILENCIO.

  * o parser do `check_notas_redundantes.py` perdia as entradas com comentario de
    LINHA dentro da chave (o furo do COR-2);
  * depois, perdia tambem as de comentario de BLOCO `/* ... */` (o furo do FIX-4);
  * o regex `regras_cor._entradas` perdia as DUAS formas de uma vez (o furo do
    COR-3, fechado aqui) — e com ele os numeros de alcance que ele alimentava;
  * o `check_fix_keys.py` casava par de strings por regex, sem olhar comentario
    nenhum (achava chaves dentro de comentario e podia nao ver o par).

A correcao certa nao e remendar cada copia: e UMA implementacao — esta — que
todas passam a usar. Quem le sao (o `file:linha` e o que cada uma ALIMENTA):

  * `tools/check_chave_compartilhada.py::bloco/entradas`  -> varredura BUG-32
    (chave nas DUAS tabelas, trava de release) e, por import, `check_dupes.py`
    (chave duplicada = ArgumentException que derruba o LocalizePatch inteiro);
  * `tools/check_notas_redundantes.py::bloco/entradas`    -> relatorio RV-15 e a
    trava de release das notas (cor do nivel 2 / redundancia);
  * `tools/check_fix_keys.py::blocos`                     -> chave x censo (CI);
  * `tools/check_omissao.py::chaves_do_mod`               -> o que o mod ja cobre;
  * `tools/check_scaling.py::chaves_do_mod`               -> idem, escala;
  * `tools/review_ledger.py::le_tabela`                   -> livro ANTES-E-DEPOIS;
  * `tools/testes/regras_cor.py::_entradas`               -> material dos testes
    da familia de COR e o alcance `scratch/cor3/cor3_alcance.py`.

Os rascunhos em `scratch/cor2/*.py` tem copias antigas do mesmo leitor; sao
descartaveis e nao entram na migracao (registrados na varredura do PARSER-1).

COBERTURA DO CONSERTO DE BLOCO (medido pelo PARSER-1R)
-----------------------------------------------------
No fonte REAL ha **ZERO** casos de comentario de BLOCO (`/* ... */`) antes da chave —
grep = 0 no `LocalizePatch.cs` (e 0 `/*` dentro dos dois blocos). O conserto de bloco do
FIX-4 e exercido, hoje, SO pela ilha SINTETICA: o `_selftest` deste arquivo, a
`FONTE_FALSA` do `t_parser_comentario_na_chave.py` e as iscas
`tools/testes/contra-prova/cp_cor_comentario_bloco_*.py`. Nenhuma entrada do produto
depende dele HOJE; ele fica pronto para a primeira entrada que escrever
`{ /* ... */ "chave" }` — que era exatamente o furo do FIX-4. Registrado aqui para
ninguem confundir "o teste passa" com "o produto exercita".

CONVENCAO
---------
`entradas()` devolve `(linha, comentario, chave, valor)` com a chave e o valor
CRUS (com os escapes C# como estao no fonte; use `valor_de_tabela` para
desescapar) — a mesma convencao que o `check_chave_compartilhada.py` e o
`check_notas_redundantes.py` ja usavam, para nenhum consumidor precisar mudar de
contrato. A `linha` e 1-based NO ARQUIVO.
"""
BS = chr(92)
Q = chr(34)
NL = chr(10)

# As tabelas que este parser le, na ordem em que aparecem no fonte.
NOMES = ("TextFixes", "TextAppends")


def bloco(fonte, nome):
    """Texto do dicionario `nome` (do `{` de abertura ate o `}` que fecha) e a posicao
    inicial, pulando strings e os DOIS tipos de comentario ao contar chaves.

    Comentario pode ter aspas soltas em prosa: sem pular a linha/bloco inteiro, o
    scanner acha que comecou uma string e perde um `{`/`}` no caminho (o bloco
    terminava cedo e 28 de 195 notas ficavam de fora). Um `{`/`}`/aspa DENTRO de um
    comentario de bloco embaralharia o fim do bloco pela mesma razao.
    """
    k = fonte.index('%s = new Dictionary' % nome)
    k = fonte.index('{', k)
    i = k + 1
    d = 1
    while i < len(fonte) and d > 0:
        c = fonte[i]
        if fonte.startswith('//', i):
            fim = fonte.find(NL, i)
            if fim < 0:
                break
            i = fim
            continue
        if fonte.startswith('/*', i):
            fim = fonte.find('*/', i + 2)
            i = len(fonte) if fim < 0 else fim + 2
            continue
        if c == Q:
            i += 1
            while i < len(fonte):
                if fonte[i] == BS:
                    i += 2
                    continue
                if fonte[i] == Q:
                    i += 1
                    break
                i += 1
            continue
        if c == '{':
            d += 1
        elif c == '}':
            d -= 1
        i += 1
    return fonte[k:i], k


def le_string(t, i):
    """Le uma string C# a partir da aspa em t[i]. Devolve (conteudo, proximo_indice).

    O conteudo sai CRU: sequencias de escape (`\\n`, `\\"`, `\\\\`) ficam como estao.
    """
    i += 1
    buf = []
    while i < len(t):
        c = t[i]
        if c == BS:
            buf.append(t[i:i + 2])
            i += 2
            continue
        if c == Q:
            return ''.join(buf), i + 1
        buf.append(c)
        i += 1
    return None, i


def _sem_marcador(s):
    """Tira o marcador de comentario (`//` ou `/* ... */`) e apara — a justificativa sai
    como o texto que o autor escreveu, nao como o comentario C# cru.

    Devolve string VAZIA para o cabecalho de secao do fonte (`// ---- NOME ----`): ele e
    metadado estrutural da tabela, nao a justificativa de UMA entrada (quem le essa
    divisao e o `review_ledger`).
    """
    s = s.strip()
    if s.startswith('/*') and s.endswith('*/'):
        s = s[2:-2]
    elif s.startswith('//'):
        s = s[2:]
    s = s.strip()
    if s.startswith('----') and s.endswith('----'):
        return ''
    return s


def pula_brancos_e_comentarios(texto, i, comentarios=None):
    """Avanca `i` sobre espacos/quebras e comentarios de LINHA (`// ...`) e de BLOCO
    (`/* ... */`). Se `comentarios` for uma lista, acumula o texto de cada comentario.

    E AQUI que mora o conserto: o parser tem de pular comentario em TODO passo (depois
    do `{` rumo a chave, depois da chave rumo a virgula, depois da virgula rumo ao
    valor e depois do valor), nunca so em um deles.
    """
    while i < len(texto):
        c = texto[i]
        if c in ' \t\r\n':
            i += 1
            continue
        if texto.startswith('//', i):
            fim = texto.find(NL, i)
            if comentarios is not None:
                c = _sem_marcador(texto[i:len(texto) if fim < 0 else fim])
                if c:
                    comentarios.append(c)
            i = len(texto) if fim < 0 else fim
            continue
        if texto.startswith('/*', i):
            fim = texto.find('*/', i + 2)
            fim = len(texto) if fim < 0 else fim + 2
            if comentarios is not None:
                c = _sem_marcador(texto[i:fim])
                if c:
                    comentarios.append(c)
            i = fim
            continue
        break
    return i


def entradas(texto, offset):
    """Pares `(linha, comentario, chave, valor)` na ordem do arquivo — aceita os DOIS
    formatos de entrada e pula os DOIS tipos de comentario em cada passo.

    `offset` = numero de quebras de linha no arquivo ANTES do bloco + 1, para a linha
    sair 1-based no arquivo (nao no bloco). O `comentario` reune o que vinha ANTES do `{`
    e o que estava DENTRO dele (antes da chave): e a justificativa escrita junto da
    entrada, e e assim que ela aparece no relatorio de quem le.

    ARMADILHA (fechada aqui): o reset do acumulador so pode disparar num TOKEN de verdade
    (`,`/`}`/letra), nunca em espaco/quebra de linha — a versao que resetava no `\n`
    devolvia comentario VAZIO em toda entrada.

    O EFEITO DESSE BUG E DE TEXTO E MORAVA NUM CANTO SO (conferido pelo PARSER-1R):
    quem consome o comentario como ROTULO e a secao "Comprimento das notas" (5) do
    `check_notas_redundantes.py`, e ali o rotulo cai no fallback `(com or chave or '(sem
    rotulo)')` — com o acumulador quebrado o rotulo imprimiria a CHAVE no lugar da
    justificativa, NUNCA uma linha vazia. E essa secao NAO existia antes da migracao
    (nasceu do PARSER-1): nao havia alvo perdendo texto.

    A coluna de justificativa do livro de revisao (`review_ledger.py`), que uma versao
    anterior deste texto apontava, NUNCA foi afetada: a leitura antiga era por LINHA
    (`splitlines` + `// ----`) e a saida e IDENTICA antes e depois da migracao — conferido
    rodando o leitor antigo e o novo sobre o mesmo fonte. A migracao so TROCOU o motor de
    leitura, nao o que este livro imprime.
    """
    out = []
    i = 0
    comentario = []
    while i < len(texto):
        c = texto[i]
        if c == Q:
            _, i = le_string(texto, i)
            continue
        if texto.startswith('//', i):
            fim = texto.find(NL, i)
            if fim < 0:
                break
            c = _sem_marcador(texto[i:fim])
            if c:
                comentario.append(c)
            i = fim
            continue
        if texto.startswith('/*', i):
            fim = texto.find('*/', i + 2)
            if fim < 0:
                break
            c = _sem_marcador(texto[i:fim + 2])
            if c:
                comentario.append(c)
            i = fim + 2
            continue
        if c == '{':
            internos = []
            j = pula_brancos_e_comentarios(texto, i + 1, internos)
            if j < len(texto) and texto[j] == Q:
                chave, j2 = le_string(texto, j)
                if chave is not None:
                    m = pula_brancos_e_comentarios(texto, j2, internos)
                    if m < len(texto) and texto[m] == ',':
                        m = pula_brancos_e_comentarios(texto, m + 1, internos)
                        if m < len(texto) and texto[m] == Q:
                            valor, m2 = le_string(texto, m)
                            if valor is not None:
                                linha = texto[:i].count(NL) + offset
                                out.append((linha, ' '.join(comentario + internos), chave, valor))
                                comentario = []
                                i = m2
                                continue
            # `{` que NAO abre entrada: nao mexe em `comentario` — o laco externo ainda
            # rele os comentarios que o `pula_brancos_e_comentarios` acabou de consumir.
        if c not in ' \t\r\n{':
            comentario = []
        i += 1
    return out


def valor_de_tabela(bruto):
    """O valor de uma entrada como ele fica em memoria (escapes resolvidos)."""
    return (bruto.replace(BS + 'n', NL).replace(BS + 't', chr(9))
                 .replace(BS + Q, Q).replace(BS + BS, BS))


# O `desescapa` historico do projeto so trocava `\\"`, `\\n` e `\\\\` (sem o `\\t`, que
# nao aparece nas tabelas). Mantido como apelido para quem ja o importava.
desescapa = valor_de_tabela


def pares(fonte, nome):
    """(chave, valor) DECODIFICADOS de todas as entradas da tabela `nome`, na ordem."""
    txt, k = bloco(fonte, nome)
    return [(valor_de_tabela(c), valor_de_tabela(v))
            for _l, _com, c, v in entradas(txt, fonte[:k].count(NL) + 1)]


def chaves(fonte, nomes=NOMES):
    """Set dos TEXTOS de chave (decodificados) das tabelas pedidas — o que o mod cobre."""
    out = set()
    for nome in nomes:
        for chave, _valor in pares(fonte, nome):
            out.add(chave)
    return out


def _selftest():
    """A prova local do parser: uma entrada com comentario de LINHA e outra com comentario
    de BLOCO entre a abertura e a chave TEM de ser vistas."""
    fonte = (
        'x.TextFixes = new Dictionary<string, string>\n{\n'
        '    { "sem comentario", "v1" },\n'
        '    {\n'
        '        // comentario de linha\n'
        '        "com linha",\n'
        '        "v2"\n'
        '    },\n'
        '    { /* comentario de bloco */ "com bloco", "v3" },\n'
        '}\n')
    achadas = [c for _l, _com, c, _v in entradas(bloco(fonte, 'TextFixes')[0], 2)]
    faltando = [c for c in ('sem comentario', 'com linha', 'com bloco') if c not in achadas]
    if faltando:
        print('FALHOU: o parser nao viu %s (viu %s)' % (faltando, achadas))
        return 1
    print('OK: o parser viu as 3 entradas (com e sem comentario de linha/bloco)')
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(_selftest())
