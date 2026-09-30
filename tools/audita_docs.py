#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audita_docs.py - compara o que a DOCUMENTACAO AFIRMA com o que existe no disco.

POR QUE ESTA FERRAMENTA EXISTE
------------------------------
Documentacao envelhece em silencio: uma contagem, uma versao, uma ferramenta citada que
mudou de nome, um link relativo para um arquivo que saiu do repo. Nada disso quebra build
nem teste - quebra a confianca de quem le. Este script transforma cada afirmacao conferivel
em um check e sai != 0 quando alguma nao bate com o disco/indice do git.

A RAIZ E DESCOBERTA A PARTIR DESTE ARQUIVO (`tools/audita_docs.py` -> repo), nunca
hardcoded: o runner do GitHub nao tem `C:/dev/stolen-realm`. Funciona rodando de qualquer
diretorio.

O QUE ELE CONFERE
-----------------
  1. inventario: quantos .md versionados existem e por pasta (informativo);
  2. nome ANTIGO do mod (`BetterTexts`) citado como se fosse o atual;
  3. contagens declaradas nos docs x o que o `tools/check_dupes.py` diz do `LocalizePatch.cs`;
  4. ferramentas: as que existem em `tools/` x as citadas nos docs;
  5. versao de cada mod: `manifest.json` x `.csproj` x `Plugin.cs` (+ dependencia do Thunderstore);
  6. links relativos quebrados nas .md versionadas;
  7. caminhos que a doc cita como parte do repo e que ja sairam dele;
  8. a dependencia do Thunderstore escrita igual em todo lugar.

FALSOS POSITIVOS QUE ELE JA CONHECE (marca em vez de reprovar)
------------------------------------------------------------
  * referencia HISTORICA ao nome antigo do mod ("era o BetterTexts, renomeado para ...") e a
    secao de troubleshooting que manda APAGAR a pasta velha; referencia cruzada ("ver o caso
    do BetterTexts acima") dentro de um arquivo que explica o rename;
  * tabela/lista que diz "nao instale" ou ❌ - o item e citado justamente para NAO ser
    instalado (harness de bancada, mod de debug);
  * a linha que EXPLICA que o `KANBAN.md` (e as notas de trabalho da raiz) nao sao
    versionados - e as mencoes ao quadro interno que nao sao citacao de caminho do repo;
  * scripts de BANCADA citados por caminho de scratch (`%LOCALAPPDATA%\\...\\scratch\\`) -
    nao sao ferramentas do repo;
  * mencao de PROSA ao pacote do BepInEx sem versao (`BepInEx-BepInExPack`): so a declaracao
    de dependencia (linha de `dependencies`/manifest) e conferida.

Regra de ouro: reprova o que o documento AFIRMA sobre o repo, nao o que ele conta da historia.

USO
---
    python tools/audita_docs.py     # exit 0 = docs batem com o disco; exit 1 = pendencias

Passo 7 do `.github/workflows/validate.yml`. Ver docs/CI.md.
"""
import io
import json
import os
import re
import subprocess
import sys
from collections import defaultdict

# RAIZ = repo: este arquivo mora em <repo>/tools/, entao sobe um nivel.
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

problemas = []
ok = []


def ler(p):
    try:
        return io.open(os.path.join(RAIZ, p), encoding='utf-8').read()
    except IOError:
        return ''


def rsh(*a):
    return subprocess.run(a, cwd=RAIZ, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT).stdout.decode('utf-8', 'replace')


def paragrafo(linhas, i):
    """Bloco de linhas nao vazias que contem a linha i (0-based) - contexto de prosa.

    Necessario porque uma afirmacao em Markdown atravessa varias linhas (bullet/tabela):
    julgar linha a linha acusa de "nome atual" um trecho que EXPLICA o rename.
    """
    a = i
    while a > 0 and linhas[a - 1].strip():
        a -= 1
    b = i
    while b + 1 < len(linhas) and linhas[b + 1].strip():
        b += 1
    return linhas[a:b + 1]


def casa_algum(padroes, texto):
    return any(re.search(p, texto, re.I) for p in padroes)


# ---------------------------------------------------------------- 1) docs existentes
docs = [f for f in rsh('git', 'ls-files').splitlines() if f.endswith('.md')]
print('== documentacao versionada: %d arquivos .md ==' % len(docs))
por_pasta = defaultdict(int)
for d in docs:
    por_pasta[d.split('/')[0]] += 1
for k, v in sorted(por_pasta.items()):
    print('   %-28s %d' % (k, v))

# ---------------------------------------------------------------- 2) nome antigo do mod
print()
print('== 2) nome ANTIGO do mod (BetterTexts) ainda aparece? ==')
ANTIGO = 'BetterTexts'
# O que marca a mencao como HISTORICA (rename contado / troubleshooting de pasta velha).
RENAME = ('renome', 'renamed', 'mudou de nome', 'nome antigo', 'versao antiga', 'antig',
          'apague', 'antes era', 'descontinuad', r'hist[óo]r')
REF_CRUZADA = ('acima', 'abaixo', 'o caso do')
antigos = [d for d in docs if ANTIGO in ler(d)]
print('   arquivos com "%s": %d' % (ANTIGO, len(antigos)))
for d in antigos:
    linhas = ler(d).splitlines()
    explica_no_arq = any(casa_algum(RENAME, l.lower()) for l in linhas)
    for i, l in enumerate(linhas, 1):
        if ANTIGO not in l:
            continue
        bloco = ' '.join(paragrafo(linhas, i - 1)).lower()
        if casa_algum(RENAME, bloco):
            marca, nota = 'ok-hist', 'o proprio texto diz que e o nome antigo'
        elif explica_no_arq and casa_algum(REF_CRUZADA, l.lower()):
            marca, nota = 'ok-ref', 'referencia cruzada ao caso explicado no mesmo arquivo'
        else:
            marca, nota = 'VER', 'cita BetterTexts como se fosse o nome atual'
            problemas.append('%s:%d cita BetterTexts como se fosse o nome atual' % (d, i))
        print('   %s %s:%d  (%s)' % (marca, d, i, nota))
        print('        ' + l.strip()[:120])

# ---------------------------------------------------------------- 3) contagens do mod
print()
print('== 3) contagens declaradas x LocalizePatch.cs ==')
src = ler('BetterTooltips/Patches/LocalizePatch.cs')
print('   LocalizePatch.cs existe: %s (%d linhas)' % (bool(src), src.count(chr(10))))
r = rsh('python', 'tools/check_dupes.py')
print('   check_dupes.py diz: %s' % ' '.join(r.split()[:14]))
nums_docs = set()
for d in docs:
    for m2 in re.finditer(r'(\d+)\s*(?:entradas|entries|corre[çc][õo]es|fixes)', ler(d)):
        nums_docs.add(int(m2.group(1)))
print('   numeros de contagem citados nos docs: %s' % sorted(nums_docs))

# ---------------------------------------------------------------- 4) ferramentas listadas
print()
print('== 4) ferramentas: listadas x existentes ==')
reais = sorted(os.path.basename(f) for f in rsh('git', 'ls-files', 'tools/').splitlines())
# Ferramenta especifica de CI vive em .github/scripts/ e nao aparece em `git ls-files tools/`.
CI_DIR = os.path.join(RAIZ, '.github', 'scripts')
reais_ci = sorted(os.listdir(CI_DIR)) if os.path.isdir(CI_DIR) else []
todos_docs = chr(10).join(ler(d) for d in docs)
faltando_doc = [f for f in reais if f not in todos_docs]
# Existe no disco mas ainda NAO versionado: o runner do CI so ve o que esta no git, entao
# isso e informativo (aviso), nao pendencia - e o caso do proprio `audita_docs.py` no dia em
# que ele e promovido, e das ferramentas de CI em `.github/` antes do primeiro push delas.
no_disco = sorted(f for f in os.listdir(os.path.join(RAIZ, 'tools'))
                  if os.path.isfile(os.path.join(RAIZ, 'tools', f)) and f not in reais)
PADRAO_FERRAMENTA = (r'(?:tools/)?((?:check_|censo_|census|audita_|audit_|analisa_|importa_|'
                     r'pack-|release-|publish-|review_|scan_|verify_|valida_)[a-z_-]+\.(?:py|sh))')
citadas = sorted(set(re.findall(PADRAO_FERRAMENTA, todos_docs)))
inexistentes = [c for c in citadas if c not in reais]
print('   existem: %d | nao citadas em nenhum doc: %s' % (len(reais), faltando_doc or 'todas citadas'))
if no_disco:
    print('   (aviso) existem no disco mas AINDA nao versionados: %s' % no_disco)
print('   citadas nos docs mas INEXISTENTES: %s' % (inexistentes or 'nenhuma'))
# Script de BANCADA (scratch/%LOCALAPPDATA%) nao e ferramenta do repo: so reprova se o doc
# apresenta o nome como ferramenta do projeto (sem contexto de scratch na mesma secao).
BANCADA = (r'scratch', r'localappdata', r'appdata', r'hermes', r'bancada')
for c in inexistentes:
    if c in reais_ci:
        print('   ok-ci: %s vive em .github/scripts/ (ferramenta de CI, nao de tools/)' % c)
        continue
    if c in no_disco:
        print('   ok-nao-versionado: %s existe em tools/ mas ainda NAO esta no git '
              '(o runner do CI so ve o que e versionado)' % c)
        continue
    ocorrencias = []
    for d in docs:
        linhas = ler(d).splitlines()
        for i, l in enumerate(linhas, 1):
            if c in l:
                ocorrencias.append((d, i, casa_algum(BANCADA, ' '.join(paragrafo(linhas, i - 1)).lower())))
    if ocorrencias and all(bancada for _, _, bancada in ocorrencias):
        print('   ok-bancada: %s so aparece como script de bancada/scratch (%s:%d)'
              % (c, ocorrencias[0][0], ocorrencias[0][1]))
        continue
    problemas.append('doc cita ferramenta inexistente: %s' % c)

# ---------------------------------------------------------------- 5) versoes dos mods
print()
print('== 5) versoes: csproj x manifest x README x docs ==')


def versao_do_plugin(src_pl):
    """A versao declarada no `[BepInPlugin(...)]` - literal ou via `const string Version`.

    Ha dois estilos no repo: `Plugin("guid", "nome", "0.1.0")` (literal) e
    `[BepInPlugin(Guid, "nome", Version)]` com `public const string Version = "0.1.0";`.
    Ler so o literal acusava DIVERGE num mod alinhado (falso positivo de REGRA).
    """
    lit = re.search(r'Plugin\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"', src_pl)
    if lit:
        return lit.group(3)
    attrs = re.search(r'\[BepInPlugin\(([^)]*)\)\]', src_pl)
    if attrs:
        ident = re.search(r',\s*([A-Za-z_][\w.]*)\s*$', attrs.group(1).strip())
        if ident:
            const = re.search(r'const\s+string\s+%s\s*=\s*"([^"]+)"'
                              % re.escape(ident.group(1).split('.')[-1]), src_pl)
            if const:
                return const.group(1)
    return '?'


for mod in sorted(os.listdir(RAIZ)):
    mp = os.path.join(RAIZ, mod, 'manifest.json')
    if not os.path.isfile(mp):
        continue
    man = json.load(io.open(mp, encoding='utf-8'))
    csproj = ''
    for f in os.listdir(os.path.join(RAIZ, mod)):
        if f.endswith('.csproj'):
            csproj = ler(os.path.join(mod, f))
    v_cs = re.search(r'<Version>([^<]+)</Version>', csproj)
    v_pl = versao_do_plugin(ler(os.path.join(mod, 'Plugin.cs')))
    dep = man.get('dependencies', [])
    d_ok = dep == ['BepInEx-BepInExPack-5.4.2305']
    alinha = (v_cs.group(1) if v_cs else '?') == man.get('version_number') == v_pl
    print('   %-30s manifest %-8s csproj %-8s plugin %-8s %s | dep %s' % (
        mod, man.get('version_number'), v_cs.group(1) if v_cs else '?',
        v_pl, 'ALINHADO' if alinha else 'DIVERGE',
        'ok' if d_ok else str(dep)))
    if not alinha:
        problemas.append('%s: versao diverge entre manifest/csproj/plugin' % mod)
    if not d_ok:
        problemas.append('%s: dependencia do Thunderstore fora do padrao' % mod)

# ---------------------------------------------------------------- 6) links relativos
print()
print('== 6) links relativos nas documentacoes ==')
quebrados = 0
for d in docs:
    base = os.path.dirname(d)
    for alvo in re.findall(r'\]\((?!https?://|#|mailto:)([^)#]+)', ler(d)):
        alvo = alvo.strip()
        if alvo.endswith('.png') and not os.path.exists(os.path.join(RAIZ, alvo)):
            continue  # capturas pendentes, tratadas a parte
        cam = os.path.normpath(os.path.join(base, alvo))
        if not os.path.exists(os.path.join(RAIZ, cam)):
            print('   QUEBRADO %s -> %s' % (d, alvo))
            problemas.append('%s: link quebrado -> %s' % (d, alvo))
            quebrados += 1
print('   links relativos quebrados: %d' % quebrados)

# ---------------------------------------------------------------- 7) caminhos removidos
print()
print('== 7) docs citam como parte do repo algo que saiu do historico? ==')
# (nome, nota-de-bancada, familia "notas de trabalho da raiz" - mencao ao quadro nao e citacao)
PROIBIDOS = [
    ('scratch/old', 'pasta de bancada que saiu do repo', False),
    ('KANBAN.md', 'nota de trabalho na raiz (fora do git de proposito)', True),
    ('ITEM_INVENTORY.md', 'nota de trabalho na raiz (fora do git de proposito)', True),
    ('ITEM_MOD_INVENTORY.md', 'nota de trabalho na raiz (fora do git de proposito)', True),
    ('ReloadProbe', 'projeto de bancada, fora do repo', False),
]
# O proprio texto EXPLICA que aquilo nao esta no repo / nao deve ser instalado.
EXPLICA = (r'fora\b[^.\n]{0,24}git', r'n[ãa]o\s+versionad', r'gitignored', r'fora\s+do\s+reposit',
           r's[óo]\s+na\s+m[áa]quina', r'n[ãa]o\s+instale', r'n[ãa]o\s+[ée]\s+mod', r'❌',
           r'harness', r'removid', r'n[ãa]o\s+est[áa]\s+mais', r'apagad', r'saiu\s+do\s+repo')


def citacao_de_caminho(linha, nome):
    """A linha cita o nome como CAMINHO/link do repo (`docs/KANBAN.md`, `[KANBAN.md](...)`)?"""
    return bool(re.search(r'[/\\]' + re.escape(nome), linha)) or ('[' + nome) in linha


achou = False
for d in docs:
    linhas = ler(d).splitlines()
    for i, l in enumerate(linhas, 1):
        for nome, nota, familia_quadro in PROIBIDOS:
            if nome not in l:
                continue
            achou = True
            bloco = ' '.join(paragrafo(linhas, i - 1))
            if casa_algum(EXPLICA, bloco):
                print('   ok-explica %s:%d cita %s - o texto explica a ausencia (%s)'
                      % (d, i, nome, nota))
            elif familia_quadro and not citacao_de_caminho(l, nome):
                print('   ok-quadro %s:%d cita %s como quadro interno, nao como arquivo do repo'
                      % (d, i, nome))
            else:
                print('   VER %s cita %s' % (d, nome))
                problemas.append('%s cita caminho que nao esta mais no repo: %s' % (d, nome))
if not achou:
    print('   (vazio - nada citando caminho removido)')

# ---------------------------------------------------------------- 8) dependencia Thunderstore
print()
print('== 8) a dependencia do Thunderstore esta escrita igual em todo lugar? ==')
CANON = 'BepInEx-BepInExPack-5.4.2305'
CRU = 'BepInEx-BepInExPack'
DECLARACAO = re.compile(r'dependencies`?[\'"]?\s*[\|:]', re.I)
for d in docs:
    for i, l in enumerate(ler(d).splitlines(), 1):
        for m3 in re.finditer(r'BepInEx-BepInExPack[\w.-]*', l):
            t = m3.group(0)
            if t == CANON:
                print('   ok  %s:%d %s' % (d, i, t))
            elif t != CRU:
                print('   VER %s:%d %s (versao diferente da canonica)' % (d, i, t))
                problemas.append('%s:%d dependencia escrita como %s (canonica: %s)' % (d, i, t, CANON))
            elif DECLARACAO.search(l):
                # e declaracao de dependencia, mas sem a versao canonica na linha.
                print('   VER %s:%d declaracao sem a versao canonica: %s' % (d, i, t))
                problemas.append('%s:%d declaracao de dependencia sem a versao canonica (%s)'
                                 % (d, i, CANON))
            else:
                print('   ok-pacote %s:%d %s (mencao de prosa ao pacote, sem declarar versao)'
                      % (d, i, t))

print()
print('=' * 62)
if problemas:
    print('!! %d PENDENCIAS:' % len(problemas))
    for p in problemas:
        print('   -', p)
    print()
    print('Cada linha acima e uma AFIRMACAO da doc que nao bate com o disco/indice do git.')
    print('Conserte o DOCUMENTO. Falso positivo de regra: ajuste a regra AQUI e diga o porque.')
    sys.exit(1)
print('== nenhuma inconsistencia encontrada ==')
