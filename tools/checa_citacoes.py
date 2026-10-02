#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""checa_citacoes.py - a CITACAO de arquivo:linha da documentacao confere com o disco?

POR QUE ESTA FERRAMENTA EXISTE (FIX-6, achado 5 da REV-56 - a TERCEIRA citacao quebrada do dia)
----------------------------------------------------------------------------------------------
A doc do projeto cita codigo por `arquivo:linha` (`BetterFont/Plugin.cs:1277`). Isso envelhece em
silencio e ja mordeu TRES vezes no mesmo dia: em `docs/NULL-1-varredura-fake-null.md` a varredura
citava tres linhas do `DiagnosticoArranque.cs` que NAO EXISTEM naquele arquivo (348, 361 e 386 num
arquivo de 252 linhas - os numeros eram do `TextStyler.cs`, colados da tabela vizinha) e um
`LootModifierDebugPatch.cs:22` cujo constructo esta na 24. Nada disso quebra build nem teste:
quebrou a confianca de quem le e conferiu.

O `audita_docs.py` ja confere AFIRMACAO de doc contra o disco (links, contagens, versoes) - este e
o irmao estreito dele para LINHA: duas perguntas por citacao, as duas checaveis a maquina:

    1. O ARQUIVO EXISTE no repositorio?
    2. A LINHA ESTA DENTRO DO ARQUIVO? (1 <= linha <= total de linhas)

O que ele NAO faz (de proposito): julgar se a linha CERTA foi citada. Isso e leitura humana - o que
a maquina garante e que a citacao aponta para algo que existe, e nao para o vazio.

FORMATOS QUE ELE LE (os que a doc usa)
--------------------------------------
    caminho/Arquivo.cs:123                 uma linha
    caminho/Arquivo.cs:123, 456, 789       lista de linhas do MESMO arquivo
    caminho/Arquivo.cs:123, 456 e 789      a lista com 'e' antes do ultimo
    caminho/Arquivo.cs:123-456             faixa (confere as duas pontas)

ESCOPO
------
  * `.cs` do repositorio (os fontes dos mods) - e o caso do achado;
  * arquivos de `scratch/` sao IGNORADOS (bancada, gitignored, pode ser podada);
  * referencias ao decompilado do jogo no estilo `l.120624` sao IGNORADAS (o arquivo nao vive no
    repo) - e por isso o padrao exige o NOME do arquivo antes do `:`.

USO
---
    python tools/checa_citacoes.py                      # varre docs/**.md e a raiz (KANBAN.md)
    python tools/checa_citacoes.py docs/FOO.md bar.md   # so os arquivos citados
    python tools/checa_citacoes.py --verboso            # lista tambem as citacoes que passaram
    python tools/checa_citacoes.py --listar             # so lista as citacoes achadas, sem julgar

exit 0 = toda citacao aponta para arquivo que existe e linha dentro dele; exit 1 = ha pendencia.
"""
import io
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# `caminho/Arquivo.cs` + `:` + lista de numeros (com ',', 'e', '/', espaco) ou faixa '-'.
# O lookahead evita casar o `.cs` de dentro de `.csproj`/`.csproj.user`.
CITACAO = re.compile(r"(?P<arq>[A-Za-z0-9_][A-Za-z0-9_./-]*\.cs)(?![A-Za-z])"
                     r"(?::(?P<linhas>\d+(?:\s*(?:,|/|e|-|\u2013)\s*\d+)*))?")

PASTAS_IGNORADAS = ("scratch/", "lib/", ".git/", "obj/", "bin/")


def arquivos_do_repo():
    """Todo `.cs` do repositorio (fora de scratch/lib/obj/bin) - o universo das citacoes validas."""
    achados = {}
    for pasta, dirs, nomes in os.walk(RAIZ):
        rel = os.path.relpath(pasta, RAIZ).replace(os.sep, "/")
        if rel == ".":
            rel = ""
        if any((rel + "/").startswith(i) for i in PASTAS_IGNORADAS):
            dirs[:] = []
            continue
        for nome in nomes:
            if not nome.endswith(".cs"):
                continue
            caminho = os.path.join(pasta, nome)
            chave = os.path.normpath(os.path.join(rel, nome)).replace(os.sep, "/")
            try:
                with io.open(caminho, encoding="utf-8", errors="replace") as fh:
                    achados[chave] = fh.read().count("\n") + 1
            except IOError:
                continue
    return achados


def documentos(alvos):
    """Os `.md` a varrer: os alvos da linha de comando, ou docs/**.md + os .md da raiz."""
    if alvos:
        return [a for a in alvos if os.path.isfile(os.path.join(RAIZ, a)) or os.path.isfile(a)]
    docs = []
    for pasta, _, nomes in os.walk(os.path.join(RAIZ, "docs")):
        for nome in nomes:
            if nome.endswith(".md"):
                docs.append(os.path.relpath(os.path.join(pasta, nome), RAIZ).replace(os.sep, "/"))
    for nome in os.listdir(RAIZ):
        if nome.endswith(".md"):
            docs.append(nome)
    return sorted(docs)


def linhas_citadas(bruto):
    """'348, 361 e 386' -> ([348, 361, 386], [], []); '120-124' -> faixa; '177/202' -> as duas.

    Devolve (linhas, faixas, nao_entendi): pedaco que nao e numero nem faixa e PENDENCIA - uma
    citacao que a ferramenta nao consegue ler nao pode passar como se tivesse sido conferida.
    """
    nums, faixas, ruins = [], [], []
    for pedaco in re.split(r"[,e/]", bruto, flags=re.I):
        pedaco = pedaco.strip()
        if not pedaco:
            continue
        if re.match(r"^\d+$", pedaco):
            nums.append(int(pedaco))
            continue
        m = re.match(r"^(\d+)\s*[-\u2013]\s*(\d+)$", pedaco)
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            if a <= b:
                faixas.append((a, b))
            continue
        ruins.append(pedaco)
    return nums, faixas, ruins


def resolve(arq, fontes, por_base):
    """Resolve a citacao para o caminho do repo: pelo caminho EXATO ou pelo NOME-BASE UNICO.

    A doc as vezes encurta (`RunButton.cs:97` dentro de um quadro que ja nomeou
    `RoguelikeSkillTreeVisualizer/RunButton.cs`). Encurtar e aceitavel QUANDO o nome-base e unico
    no repositorio - o que nao vale e citacao que nao resolve para arquivo nenhum, ou que resolve
    para dois (aí o leitor nao sabe de qual se fala).
    """
    if arq in fontes:
        return arq, None
    base = os.path.basename(arq)
    candidatos = por_base.get(base, [])
    if len(candidatos) == 1:
        return candidatos[0], None
    if not candidatos:
        return None, "`%s` nao corresponde a nenhum .cs do repositorio" % arq
    return None, ("`%s` e ambiguo: existe em %s - cite o caminho completo"
                  % (arq, " e ".join(sorted(candidatos))))


def main(argv):
    verboso = "--verboso" in argv
    so_listar = "--listar" in argv
    alvos = [a for a in argv[1:] if not a.startswith("--")]

    fontes = arquivos_do_repo()
    por_base = {}
    for caminho in fontes:
        por_base.setdefault(os.path.basename(caminho), []).append(caminho)
    docs = documentos(alvos)
    if not docs:
        print("checa_citacoes: nenhum documento para varrer")
        return 0

    total, problemas, conferidas = 0, [], 0
    for doc in docs:
        caminho = doc if os.path.isabs(doc) else os.path.join(RAIZ, doc)
        if not os.path.isfile(caminho):
            print("checa_citacoes: documento ausente: %s" % doc)
            return 1
        linhas = io.open(caminho, encoding="utf-8").read().splitlines()
        for i, linha in enumerate(linhas, 1):
            for m in CITACAO.finditer(linha):
                arq = m.group("arq")
                if any(arq.startswith(p) for p in PASTAS_IGNORADAS) or arq.startswith("."):
                    continue
                # Menção sem `:linha` so e conferida se tiver CARA de caminho (`pasta/arquivo.cs`):
                # e o caso dos titulos (`### BetterTooltips/LocalizePatch.cs`), que a REV-56 pegou
                # sem o `Patches/`. Nome solto sem linha e prosa, nao citacao.
                e_citacao = bool(m.group("linhas"))
                com_caminho = "/" in arq
                resolvido, erro = resolve(arq, fontes, por_base)
                if not e_citacao and not com_caminho:
                    continue
                if not resolvido and not com_caminho:
                    # NOME SOLTO que nao e arquivo do repositorio: e a classe do DECOMPILADO DO JOGO
                    # (`tooltip.cs`, `Character.cs`, `SkillTrigger.cs` vivem em scratch/ e nao sao
                    # versionadas). Nao e citacao de arquivo do repo - fica fora, dito em --verboso.
                    if verboso:
                        print("   ignorado %s:%d `%s` (nao e um .cs do repositorio: provavel classe "
                              "do decompilado do jogo)" % (doc, i, arq))
                    continue
                total += 1
                if not e_citacao:
                    # Caminho citado como caminho: exige IGUALDADE EXATA (e o que a doc promete).
                    if arq in fontes:
                        conferidas += 1
                        if verboso:
                            print("   ok %s:%d `%s` (caminho existe)" % (doc, i, arq))
                    else:
                        problemas.append("%s:%d cita o caminho `%s`, que NAO existe no repositorio"
                                         % (doc, i, arq))
                    continue
                if resolvido is None:
                    problemas.append("%s:%d cita `%s`: %s" % (doc, i, m.group(0).strip(), erro))
                    continue
                nums, faixas, nao_entendi = linhas_citadas(m.group("linhas"))
                limite = fontes[resolvido]
                ruim = list(nao_entendi) + [n for n in nums if not (1 <= n <= limite)]
                for a, b in faixas:
                    if not (1 <= a <= limite and 1 <= b <= limite):
                        ruim.append("%d-%d" % (a, b))
                if ruim:
                    problemas.append("%s:%d cita `%s`, mas %s tem %d linha(s) - fora do arquivo: %s"
                                     % (doc, i, m.group(0).strip(), resolvido, limite,
                                        ", ".join(str(r) for r in ruim)))
                else:
                    conferidas += 1
                    if verboso:
                        print("   ok %s:%d `%s` (%d linha(s))" % (doc, i, m.group(0).strip(), limite))
    print("checa_citacoes: %d citacao(oes)/mencao(oes) de arquivo em %d documento(s) - %d conferidas, "
          "%d pendencia(s)" % (total, len(docs), conferidas, len(problemas)))
    if so_listar:
        return 0
    if problemas:
        print()
        print("!! PENDENCIAS (a citacao aponta para o vazio - conserte a DOC, nao a ferramenta):")
        for p in problemas:
            print("   -", p)
        return 1
    print("   toda citacao aponta para arquivo que existe, com a linha dentro dele.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
