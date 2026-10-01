#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""EXEMPLO de teste que PRECISA DO JOGO (lib/ local; NAO roda no CI).

O QUE ELE CONFERE
-----------------
Que a lib/ desta maquina tem, de verdade, o que os mods precisam para compilar:
toda entrada `<HintPath>..\lib\X.dll</HintPath>` de todo `.csproj` do repositorio
resolve para um arquivo existente, e esse arquivo e uma PE de verdade (comeca com
"MZ") com tamanho plausivel.

POR QUE ISSO E UM TESTE DE JOGO E NAO DE LOGICA PURA
---------------------------------------------------
A lib/ e GITIGNORED: sao as DLLs extraidas da instalacao do jogo (Assembly-CSharp
e propriedade do jogo, proibido distribuir). Num runner limpo ela nao existe, e
por isso um teste que depende dela NAO RODA no CI - ele DECLARA isso no META
(`requer: ["lib/"]` + `categoria: "jogo"`) para o runner dizer, em voz alta, que
ele nao rodou, em vez de sumir da suite.

Este e o formato que os testes "que precisam dos tipos do jogo" (Unity/Mathf, TMP,
Character) devem seguir: mesma declaracao, mesma mensagem clara - e no lugar da
checagem de PE, compilar/decompilar o que precisarem. A receita de `dotnet` esta
no README do tools/testes/.
"""
import os
import re

import arcabouco as arc

META = {
    "nome": "referencias-lib",
    "categoria": "jogo",
    "requer": ["lib/"],
    "descricao": "as referencias lib\\* dos .csproj existem na lib/ e sao PE validas",
}

RAIZES_DE_VARREDURA = ("bin", "obj", ".git", ".vs", "dist", "node_modules")


def csprojs():
    raiz = arc.raiz_do_repo()
    for pasta, pastas, arquivos in os.walk(raiz):
        pastas[:] = [p for p in pastas if p not in RAIZES_DE_VARREDURA]
        for nome in sorted(arquivos):
            if nome.endswith(".csproj"):
                yield os.path.join(pasta, nome)


def referencias():
    """{nome_da_dll: [(csproj, caminho_resolvido)]} para todo HintPath em lib\\."""
    achados = {}
    for caminho_csproj in csprojs():
        with open(caminho_csproj, encoding="utf-8", errors="replace") as fh:
            texto = fh.read()
        for bruto in re.findall(r"<HintPath>\s*(.*?)\s*</HintPath>", texto, re.S):
            if "lib" not in bruto.lower():
                continue
            relativo = bruto.replace("\\", os.sep)
            resolvido = os.path.normpath(os.path.join(os.path.dirname(caminho_csproj), relativo))
            achados.setdefault(os.path.basename(relativo), []).append((caminho_csproj, resolvido))
    return achados


def corpo():
    refs = referencias()
    arc.exigir(refs, "nenhum .csproj referencia lib\\ - a varredura nao encontrou o que conferir")

    # 1. Pre-requisito declarado: a lib/ precisa estar nesta maquina, com TODAS as
    #    DLLs referenciadas. Faltando qualquer uma -> NAO RODOU (exit 2), com a
    #    lista do que falta. Nao e "verde": e um teste que nao deu para rodar.
    lib = arc.precisa_lib(sorted(refs))

    # 2. Cada referencia resolve para um arquivo e o arquivo e uma PE ("MZ").
    for nome_dll in sorted(refs):
        ocorrencias = refs[nome_dll]
        destino = os.path.join(lib, nome_dll)
        arc.exigir(os.path.isfile(destino), "lib\\%s referenciada e o arquivo nao existe" % nome_dll)
        with open(destino, "rb") as fh:
            inicio = fh.read(2)
        arc.igual(inicio, b"MZ", "lib\\%s nao comeca com MZ (nao e uma PE valida)" % nome_dll)
        tamanho = os.path.getsize(destino)
        arc.exigir(tamanho > 1024, "lib\\%s tem %d bytes - parece truncada" % (nome_dll, tamanho))

        # 3. E o caminho RELATIVO escrito no csproj precisa cair na mesma DLL.
        #    Um `..\lib\` a mais ou a menos compila hoje e quebra amanha, quando o
        #    csproj mudar de lugar - ou quebra o build de outra pessoa.
        for caminho_csproj, resolvido in ocorrencias:
            arc.igual(os.path.normcase(os.path.abspath(resolvido)),
                      os.path.normcase(os.path.abspath(destino)),
                      "%s aponta para %s" % (os.path.relpath(caminho_csproj, arc.raiz_do_repo()), resolvido))

    print("conferidas %d DLLs de %d .csproj em %s" % (
        len(refs), len(set(c for ocorrencias in refs.values() for c, _ in ocorrencias)), lib))


if __name__ == "__main__":
    arc.main(META, corpo)
