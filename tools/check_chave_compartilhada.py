#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_chave_compartilhada.py - BUG-32: varredura de CHAVE COMPARTILHADA.

POR QUE ESTA FERRAMENTA EXISTE
------------------------------
O BetterTooltips corrige tooltips por CHAVE DE TEXTO (`TextFixes`) e acrescenta
explicacoes por chave de texto (`TextAppends`). O lookup e pelo TEXTO EXATO da
frase, nao pela entidade. Mas um mesmo texto pode servir a VARIAS entidades do
jogo (skills, status, itens, afixos, powerups) - e ai uma nota escrita para um
dono "mente" para os outros.

CASO REAL (BUG-31, defeito confirmado em 30/09):
  o status `Consumption` diz "Max Health increased by 10%." e tem a nota
  "Each stack grants another 10% Max Health; you gain one stack per enemy hit."
  Mas o MESMO texto e usado pela skill `Endurance I` (Monk), onde o +10% e um
  bonus FIXO sem stack nenhum -> a nota caiu nos dois e mente para o Endurance.
  A nota do `Consumption` (LocalizePatch l.418-423) ficou pendurada na chave
  compartilhada; a chave "@Maximum health@ reduced by 20%" (l.424-426) entra na
  MESMA varredura.

Isso e a familia do INC-1 (chave duplicada), mas a colisao e no JOGO, no texto
de varias entidades, nao no nosso dicionario.

O QUE A VARREDURA FAZ
---------------------
  (a) le os CSVs do censo em docs/cobertura/ (qualquer *.csv com coluna
      `descricao`: skills, status, itens, afixos, powerups, acoes...);
  (b) acha todo texto usado por MAIS DE UMA entidade - o criterio e EXATO
      (o lookup do mod tambem e), e ha um segundo criterio, VARIANTE: textos
      que so diferem em espaco duplo/espaco no fim e por isso RENDERIZAM
      iguais (o mod colapsa "  " -> " " no fim do postfix, mas nao apara o
      fim) e ainda assim nao recebem a mesma nota;
  (c) cruza com as chaves que TEM correcao/nota no LocalizePatch;
  (d) imprime as SUSPEITAS: chave + donos + nota aplicada.

MODO PADRAO x --estrito
-----------------------
As duas familias que a varredura imprime NAO tem o mesmo peso:

  * CHAVE NAS DUAS TABELAS (defeito objetivo): a MESMA chave existe em `TextFixes`
    e em `TextAppends`. O lookup do mod e `if/else if` na MESMA chave, entao a
    entrada de `TextAppends` NUNCA roda: a nota nao existe em jogo, em silencio,
    sem erro no log. Nao ha decisao humana aqui -> em `--estrito` o script sai 1.
  * SUSPEITAS de texto compartilhado (humano): a nota pode mentir para outro dono
    do texto, mas se mente ou nao depende da mecanica citada -> continua AVISO
    que nao reprova, nos dois modos.

`--estrito` e o modo usado pelo `tools/release-check.sh` (trava de release). Sem a
flag o script e relatorio: **exit 0 sempre**.

REGRAS DE LEITURA DO RESULTADO
------------------------------
  * donos=1 e sem variantes -> chave exclusiva, a nota so pode atingir o dono
    certo (caso limpo).
  * donos>=2 -> a MESMA correcao/nota vale para todos os donos. Se a nota cita
    mecanica especifica (stack, gatilho, aura), ela mente para os outros. Se e
    gramatica, provavelmente serve a todos (verificar caso a caso).
  * variante de espaco -> os dois textos RENDERIZAM a mesma frase, mas so o
    exato recebe a nota. Inconsistencia visivel (um tooltip com nota, o irmao
    sem) e sinal de que a chave pode ter sido copiada de um texto com espaco
    diferente do asset.
  * "fora do censo" NAO e erro por si: o censo cobre skills/status/itens/
    afixos/powerups; UI, dicas de loading e chaves de localizacao (ex.:
    "Resist Divine") ainda nao estao la - ver docs/cobertura/README.md.

O PARSER (por que nao regex)
----------------------------
As tabelas tem DOIS formatos de entrada: par na mesma linha (`{ "k", "v" },`)
e par quebrado em varias linhas (`{` / `"k",` / `"v"` / `},`). Um regex
`[^"\\]` quebra com o heredoc do shell colapsando barras (INC-1, ja custou
caro). Aqui a leitura e caractere a caractere, pulando comentarios `//` (que
tem aspas soltas em prosa) e respeitando escape `\\"` - mesma abordagem do
`check_notas_redundantes.py`, com o desescape do `check_fix_keys.py`.

USO
---
    python tools/check_chave_compartilhada.py             # relatorio: sempre exit 0
    python tools/check_chave_compartilhada.py --estrito   # exit 1 se a MESMA chave
                                                          # estiver nas DUAS tabelas
    python tools/check_chave_compartilhada.py -v          # mostra tambem as chaves limpas
    python tools/check_chave_compartilhada.py --estrito --fonte OUTRO.cs
                                                          # le outro fonte (teste do detector,
                                                          # sem tocar no LocalizePatch.cs)

Codigos de saida: 0 = ok/aviso, 1 = chave nas duas tabelas (so em --estrito), 2 = erro de uso/fonte.

Relatorio das suspeitas: docs/cobertura/revisao/BUG-32-chaves-compartilhadas.md
"""

import csv
import io
import os
import re
import sys
from collections import Counter, defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COBERTURA = os.path.join(RAIZ, 'docs', 'cobertura')
FONTE = os.path.join(RAIZ, 'BetterTooltips', 'Patches', 'LocalizePatch.cs')
BLOCOS = ('TextFixes', 'TextAppends')

BS = chr(92)
Q = chr(34)
NL = chr(10)
MAX_DONOS_IMPRESSOS = 12   # nos prints do terminal; o relatorio em .md lista todos


# ---------------------------------------------------------------------------
# parser do LocalizePatch.cs
# ---------------------------------------------------------------------------
def bloco(fonte, nome):
    """Texto do dicionario `nome` (do `{` de abertura ate o `}` que fecha)."""
    k = fonte.index('%s = new Dictionary' % nome)
    k = fonte.index('{', k)
    i = k + 1
    d = 1
    while i < len(fonte) and d > 0:
        c = fonte[i]
        # Comentario pode ter aspas soltas em prosa: pular a linha inteira, senao o
        # scanner acha que comecou uma string e perde um `{`/`}` no caminho.
        if fonte.startswith('//', i):
            i = fonte.find(NL, i)
            if i < 0:
                break
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
    """Le uma string C# a partir da aspa em t[i]. Devolve (conteudo, proximo_indice)."""
    i += 1
    buf = []
    while i < len(t):
        c = t[i]
        if c == BS:
            buf.append(t[i:i + 2])   # guarda a sequencia de escape como esta
            i += 2
            continue
        if c == Q:
            return ''.join(buf), i + 1
        buf.append(c)
        i += 1
    return None, i


def pula_brancos(t, j, comentario):
    """Pula espacos/quebras de linha e comentarios `//` a partir de t[j].

    Comentario pode ter aspas soltas em prosa: e por isso que a leitura pula a linha
    inteira. Devolve o novo indice e vai acumulando as linhas de comentario vistas.
    """
    while j < len(t):
        c = t[j]
        if c in ' \t\r\n':
            j += 1
            continue
        if t.startswith('//', j):
            fim = t.find(NL, j)
            if fim < 0:
                return len(t)
            comentario.append(t[j:fim].strip())
            j = fim
            continue
        break
    return j


def entradas(texto, nl_antes_do_bloco):
    """Pares (linha, comentario, chave, valor) na ordem do arquivo - aceita os DOIS formatos.

    Formato 1: `{ "chave", "valor" },` na mesma linha.
    Formato 2: `{` / `// comentario` / `"chave",` / `"valor"` / `},` quebrado em
    varias linhas - o comentario pode estar DENTRO das chaves, antes da chave; a
    primeira versao (como a do check_notas_redundantes.py) perdia essas entradas em
    silencio (71 de 86 do TextFixes). Por isso aqui se pula brancos/comentarios em
    cada passo, e nao so depois do `{`.

    `nl_antes_do_bloco` = numero de quebras de linha no arquivo ANTES do bloco, para
    a linha absoluta sair certa (a versao consultada usava o indice de caractere do
    bloco como offset, o que devolvia l.68018 - numero inutil para o relatorio).
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
            comentario.append(texto[i:fim].strip())
            i = fim
            continue
        if c == '{':
            comentario_entrada = list(comentario)
            j = pula_brancos(texto, i + 1, comentario_entrada)
            if j < len(texto) and texto[j] == Q:
                chave, j2 = le_string(texto, j)
                if chave is not None:
                    m = pula_brancos(texto, j2, comentario_entrada)
                    if m < len(texto) and texto[m] == ',':
                        m = pula_brancos(texto, m + 1, comentario_entrada)
                        if m < len(texto) and texto[m] == Q:
                            valor, m2 = le_string(texto, m)
                            if valor is not None:
                                linha = texto[:i].count(NL) + nl_antes_do_bloco + 1
                                out.append((linha, ' '.join(comentario_entrada)[:160],
                                            chave, valor))
                                comentario = []
                                i = m2
                                continue
            comentario = comentario_entrada
        if c not in ' \t\r':
            comentario = []
        i += 1
    return out


def desescapa(s):
    """Desfaz os escapes C# de uma CHAVE para comparar com o censo (texto real do asset)."""
    out = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == BS and i + 1 < len(s):
            n = s[i + 1]
            if n == 'n':
                out.append(NL)
            elif n == 't':
                out.append('\t')
            elif n == Q:
                out.append(Q)
            elif n == BS:
                out.append(BS)
            else:
                out.append(n)
            i += 2
            continue
        out.append(c)
        i += 1
    return ''.join(out)


# ---------------------------------------------------------------------------
# censo
# ---------------------------------------------------------------------------
CONTEXTO = ('arvore', 'tier', 'tipo', 'raridade', 'classe', 'nivel')
ROTULO_ARQUIVO = {
    'skills.csv': 'skills',
    'status.csv': 'status',
    'itens.csv': 'itens',
    'afixos.csv': 'afixos',
    'powerups.csv': 'powerups',
    'acoes.csv': 'acoes',
}


def le_censo():
    """Devolve (entidades, por_csv) - entidade = (arquivo, nome, descricao, contexto)."""
    entidades = []
    por_csv = {}
    for arq in sorted(os.listdir(COBERTURA)):
        if not arq.lower().endswith('.csv'):
            continue
        caminho = os.path.join(COBERTURA, arq)
        with io.open(caminho, encoding='utf-8', newline='') as fh:
            linhas = list(csv.DictReader(fh))
        if not linhas or 'descricao' not in (linhas[0].keys() if linhas else []):
            por_csv[arq] = (0, 'sem coluna descricao')
            continue
        n = 0
        for r in linhas:
            d = (r.get('descricao') or '')
            if not d:
                continue
            nome = (r.get('nome') or '').strip()
            ctx = ', '.join('%s=%s' % (c, r[c]) for c in CONTEXTO if r.get(c))
            entidades.append((arq, nome, d, ctx))
            n += 1
        por_csv[arq] = (n, 'ok')
    return entidades, por_csv


def norm_espacos(s):
    """Texto como RENDERIZA: colapsa espaco duplo (regra geral do mod) e ignora fim/inicio.

    O mod NAO apara o fim do texto de proposito, mas espaco no fim e invisivel no
    tooltip: para julgar "e a mesma frase na tela?", inicio/fim nao contam.
    """
    while '  ' in s:
        s = s.replace('  ', ' ')
    return s.strip()


def mostra_valor(v):
    """Valor para exibicao em uma linha (escapes visiveis)."""
    v = v.replace(BS + 'n', ' | ')
    return re.sub(r'\s+', ' ', v).strip()


def argumentos(argv):
    """Le as flags. Devolve (verbose, estrito, caminho_do_fonte, erro).

    `--fonte ARQUIVO.cs` existe para TESTAR O DETECTOR: aponta o parser para um
    fonte falso (com/sem par repetido nas duas tabelas) sem tocar no
    LocalizePatch.cs, que e o arquivo sob revisao de outro agente.
    """
    verbose = '-v' in argv
    estrito = '--estrito' in argv
    caminho = FONTE
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == '--fonte':
            if i + 1 >= len(argv):
                return verbose, estrito, caminho, '--fonte exige um caminho'
            caminho = argv[i + 1]
            i += 1
        elif a.startswith('--fonte='):
            caminho = a.split('=', 1)[1]
        elif a not in ('-v', '--estrito'):
            return verbose, estrito, caminho, 'opcao desconhecida: %s' % a
        i += 1
    return verbose, estrito, caminho, None


def main():
    verbose, estrito, fonte_caminho, erro = argumentos(sys.argv[1:])
    if erro:
        print(erro)
        print('uso: check_chave_compartilhada.py [--estrito] [-v] [--fonte ARQUIVO.cs]')
        return 2
    if not os.path.exists(fonte_caminho):
        print('nao achei %s' % fonte_caminho)
        return 2

    fonte = io.open(fonte_caminho, encoding='utf-8').read()
    chaves = []   # (tabela, linha, comentario, chave, valor)
    for tabela in BLOCOS:
        try:
            txt, k = bloco(fonte, tabela)
        except ValueError:
            print('nao achei a tabela %s em %s' % (tabela, fonte_caminho))
            return 2
        nl_antes = fonte[:k].count(NL)
        for linha, com, kk, v in entradas(txt, nl_antes):
            chaves.append((tabela, linha, com, kk, v))

    entidades, por_csv = le_censo()

    # (b) textos usados por mais de uma entidade ---------------------------------
    por_texto = defaultdict(list)          # descricao exata -> entidades
    por_norm = defaultdict(set)            # forma renderizada -> descricoes exatas
    por_norm_ent = defaultdict(list)       # forma renderizada -> entidades
    for e in entidades:
        arq, nome, d, ctx = e
        por_texto[d].append(e)
        por_norm[norm_espacos(d)].add(d)
        por_norm_ent[norm_espacos(d)].append(e)

    compartilhados = {t: es for t, es in por_texto.items() if len(es) > 1}
    compartilhados_cross = {
        t: es for t, es in compartilhados.items()
        if len(set(a for a, _, _, _ in es)) > 1
    }

    # (c) cruza com as chaves que tem correcao/nota ------------------------------
    suspeitas = []       # dicts
    limpas = []          # chaves com 1 dono e sem variantes
    fora = []            # chave nao existe em lugar nenhum do censo
    for tabela, linha, com, k, v in chaves:
        kreal = desescapa(k)
        donos = por_texto.get(kreal, [])
        variantes = [e for e in por_norm_ent.get(norm_espacos(kreal), [])
                     if e[2] != kreal]
        if len(donos) > 1 or variantes:
            suspeitas.append({
                'tabela': tabela, 'linha': linha, 'chave': kreal, 'valor': v,
                'donos': donos, 'variantes': variantes,
            })
        elif donos:
            limpas.append((tabela, linha, kreal))
        else:
            fora.append((tabela, linha, kreal))

    # chave presente nas DUAS tabelas = a de TextFixes ganha e a outra morre em silencio
    set_fix = set(desescapa(k) for t, _, _, k, _ in chaves if t == 'TextFixes')
    set_app = set(desescapa(k) for t, _, _, k, _ in chaves if t == 'TextAppends')
    ambas = sorted(set_fix & set_app)

    # ------------------------------------------------------------------ relatorio
    n_fix = sum(1 for c in chaves if c[0] == 'TextFixes')
    n_app = sum(1 for c in chaves if c[0] == 'TextAppends')
    print('BUG-32 - varredura de CHAVE COMPARTILHADA (LocalizePatch x censo)')
    print('')
    print('modo: %s' % ('ESTRITO (chave nas DUAS tabelas = exit 1)' if estrito
                        else 'relatorio (aviso, exit 0)'))
    print('fonte: %s' % os.path.relpath(fonte_caminho, RAIZ).replace(BS, '/'))
    print('  TextFixes   : %d entradas' % n_fix)
    print('  TextAppends : %d entradas' % n_app)
    print('  chaves com correcao/nota: %d' % len(chaves))
    print('')
    print('censo: %s/*.csv' % os.path.relpath(COBERTURA, RAIZ).replace(BS, '/'))
    for arq in sorted(por_csv):
        n, obs = por_csv[arq]
        print('  %-22s %4d entidades com descricao%s' %
              (arq, n, '' if obs == 'ok' else '   [%s]' % obs))
    print('  total: %d entidades' % len(entidades))
    print('  textos usados por mais de uma entidade (exato): %d  (desses, %d cruzam categorias)'
          % (len(compartilhados), len(compartilhados_cross)))
    print('')
    print('SUSPEITAS (chave com correcao/nota + texto usado por mais de um dono): %d'
          % len(suspeitas))
    print('=' * 78)
    for idx, s in enumerate(sorted(suspeitas, key=lambda x: (-len(x['donos']),
                                                            -len(x['variantes']),
                                                            x['chave'])), 1):
        tipo = []
        if len(s['donos']) > 1:
            tipo.append('EXATA')
        if s['variantes']:
            tipo.append('VARIANTE')
        cats = set(a for a, _, _, _ in s['donos'] + s['variantes'])
        print('')
        print('[%d] %s l.%d | %s | donos=%d, variantes=%d%s' %
              (idx, s['tabela'], s['linha'], '+'.join(tipo), len(s['donos']), len(s['variantes']),
               '  [entre categorias: %s]' % ', '.join(sorted(cats)) if len(cats) > 1 else ''))
        print('    chave: %r' % s['chave'])
        for e in s['donos'][:MAX_DONOS_IMPRESSOS]:
            print('      dono   : %s | %s%s' % (e[0], e[1], (' (%s)' % e[3]) if e[3] else ''))
        if len(s['donos']) > MAX_DONOS_IMPRESSOS:
            print('      dono   : (+%d)' % (len(s['donos']) - MAX_DONOS_IMPRESSOS))
        for e in s['variantes'][:MAX_DONOS_IMPRESSOS]:
            print('      variante: %s | %s%s' % (e[0], e[1], (' (%s)' % e[3]) if e[3] else ''))
        if len(s['variantes']) > MAX_DONOS_IMPRESSOS:
            print('      variante: (+%d)' % (len(s['variantes']) - MAX_DONOS_IMPRESSOS))
        print('    valor : %s' % mostra_valor(s['valor'])[:300])
    print('')
    print('=' * 78)
    if ambas:
        print('ALERTA EXTRA - chave nas DUAS tabelas (so a de TextFixes executa)%s: %d'
              % (' - TRAVA DE RELEASE em --estrito' if estrito else '', len(ambas)))
        for k in ambas:
            print('   %r' % k)
        print('')
    if fora:
        print('chaves fora do censo (UI/loading/localizacao - NAO e erro por si): %d' % len(fora))
        for tabela, linha, k in fora:
            print('   [%s l.%d] %r' % (tabela, linha, k[:95]))
        print('')
    print('RESUMO')
    print('  entidades com descricao ............... %d' % len(entidades))
    print('  textos compartilhados (exato) ......... %d  (cruzando categorias: %d)'
          % (len(compartilhados), len(compartilhados_cross)))
    print('  chaves com nota/correcao .............. %d' % len(chaves))
    print('  SUSPEITAS (nota em texto com mais de um dono) . %d' % len(suspeitas))
    print('     com mais de um dono EXATO .......... %d'
          % sum(1 for s in suspeitas if len(s['donos']) > 1))
    print('     com variante de espaco ............. %d'
          % sum(1 for s in suspeitas if s['variantes']))
    print('  chaves limpas (1 dono, sem variante) .. %d' % len(limpas))
    print('  chaves fora do censo .................. %d' % len(fora))
    print('  chave nas DUAS tabelas (TextFixes+TextAppends) ......... %d' % len(ambas))
    print('')
    if ambas:
        if estrito:
            print('>>> BLOQUEIO DE RELEASE (BUG-32 - CHAVE NAS DUAS TABELAS) <<<')
        else:
            print('>>> DEFEITO OBJETIVO (BUG-32 - CHAVE NAS DUAS TABELAS) <<<')
            print('    Aqui e so aviso; `--estrito` (o modo do release-check) TRAVA a release.')
        print('    A entrada de TextAppends NAO roda: o lookup e if/else if na MESMA chave,')
        print('    e a de TextFixes ganha. A nota nao existe em jogo e NAO ha erro no log.')
        print('    Correcao (no LocalizePatch.cs, UMA entrada por texto): fundir o valor da')
        print('    TextAppends no valor da TextFixes que executa - mantem as duas coisas.')
    else:
        print('>>> AVISO (nao reprova): a decisao e humana -')
        print('    nota que cita mecanica especifica (stack/gatilho/aura) mente para os')
        print('    outros donos; corrigir movendo a nota para uma chave exclusiva ou')
        print('    trocando a entrada por TextFixes no dono certo.')
    print('    Relatorio: docs/cobertura/revisao/BUG-32-chaves-compartilhadas.md')
    if verbose:
        print('')
        print('CHAVES LIMPAS (1 dono exato, sem variante): %d' % len(limpas))
        for tabela, linha, k in limpas:
            print('   [%s l.%d] %r' % (tabela, linha, k[:95]))
    if estrito and ambas:
        print('')
        print('EXIT 1: %d chave(s) nas DUAS tabelas - release TRAVADA (BUG-32).' % len(ambas))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
