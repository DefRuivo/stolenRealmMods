#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""regras_rel.py - o plantio do caso do REL-1, num lugar so.

O QUE ELE PLANTA
----------------
Um mod de mentira com a estrutura MINIMA que o pre-flight do
`tools/pack-thunderstore.py` aceita: `.csproj` com `<Version>`, `Plugin.cs` com o
`[BepInPlugin(...)]` espelhado, `manifest.json`, README, CHANGELOG, `icon.png` 256x256
(gerado pelo proprio empacotador) e a DLL em `bin/<Config>/netstandard2.1/`.

Com isso da para rodar o pre-flight REAL contra uma raiz plantada - sem tocar no repositorio,
sem `dotnet`, sem `lib/` do jogo - e escolher a relacao de mtime entre a DLL e a fonte:

    fonte_mais_nova=False   a DLL e posterior a fonte   -> build em dia
    fonte_mais_nova=True    a fonte e posterior a DLL   -> o defeito do REL-1

POR QUE UM MOD DE MENTIRA, E NAO O REPOSITORIO
----------------------------------------------
A trava e sobre a RELACAO entre dois mtimes, e o repositorio tem mtimes que mudam sozinhos
(COR-3 editando fonte agora, `git checkout` reescrevendo tudo). Um teste que dependesse do
estado do dia seria um teste que muda de veredito sem ninguem mexer nele. O plantio fixa os
dois tempos com `os.utime` e o veredito passa a depender SO da trava.

O mtime NAO e sleep: e `os.utime`, explicito, com uma diferenca de minutos. Teste que dorme
e teste que fica lento e instavel.
"""
import importlib.util
import json
import os

import arcabouco as arc

MINUTO = 60
CAMINHO_EMPACOTADOR = os.path.join(arc.raiz_do_repo(), "tools", "pack-thunderstore.py")


def carrega_empacotador():
    """Importa `pack-thunderstore.py` (tem hifen no nome: nao da `import` normal).

    Mesmo caminho que o `tools/check_versoes.py` usa: o modulo so define funcoes no nivel
    de cima - a execucao esta toda sob `if __name__ == "__main__"` - entao importar nao
    empacota nem escreve nada.
    """
    spec = importlib.util.spec_from_file_location("pack_thunderstore", CAMINHO_EMPACOTADOR)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def monta_mod(raiz, nome="BetterTooltips", versao="9.9.9", config="Release",
              fonte_mais_nova=False):
    """Planta o mod minimo em `<raiz>/<nome>/`. Devolve o dict de caminhos plantados.

    `fonte_mais_nova=True` poe a fonte DEPOIS da DLL - a fonte mudou e ninguem reconstruiu.
    """
    m = carrega_empacotador()
    pasta = os.path.join(raiz, nome)
    os.makedirs(os.path.join(pasta, "Patches"), exist_ok=True)
    os.makedirs(os.path.join(pasta, "obj", config, "netstandard2.1"), exist_ok=True)
    os.makedirs(os.path.join(pasta, "bin", config, "netstandard2.1"), exist_ok=True)

    with open(os.path.join(pasta, nome + ".csproj"), "w", encoding="utf-8") as fh:
        fh.write("<Project Sdk=\"Microsoft.NET.Sdk\">\n"
                 "  <PropertyGroup>\n"
                 "    <TargetFramework>netstandard2.1</TargetFramework>\n"
                 "    <Version>%s</Version>\n"
                 "  </PropertyGroup>\n</Project>\n" % versao)

    with open(os.path.join(pasta, "Plugin.cs"), "w", encoding="utf-8") as fh:
        fh.write("[BepInPlugin(\"guid.de.teste\", \"%s\", \"%s\")]\n" % (nome, versao))

    fonte = os.path.join(pasta, "Patches", "LocalizePatch.cs")
    with open(fonte, "w", encoding="utf-8") as fh:
        fh.write("// a fonte do mod (o conteudo nao importa: a trava olha o mtime)\n")

    with open(os.path.join(pasta, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump({"name": nome, "version_number": versao,
                   "website_url": "https://example.invalid", "description": "mod de teste",
                   "dependencies": []}, fh)

    for doc in ("README.md", "CHANGELOG.md"):
        with open(os.path.join(pasta, doc), "w", encoding="utf-8") as fh:
            fh.write("# %s\n" % doc)

    # PKG-3: o README do mod e o QUARTO lugar que carrega a versao (`- **Version:** x.y.z`)
    # e o pre-flight REPROVA o plantio "em dia" se a linha faltar - o mtime nao e a unica
    # coisa que a trava confere. Espelhado com a MESMA `versao` do .csproj/Plugin.cs.
    with open(os.path.join(pasta, "README.md"), "a", encoding="utf-8") as fh:
        fh.write("\n- **Version:** %s\n" % versao)

    icone = os.path.join(pasta, "icon.png")
    m.gerar_icone(nome, icone)

    dll = os.path.join(pasta, "bin", config, "netstandard2.1", nome + ".dll")
    with open(dll, "wb") as fh:
        fh.write(b"MZ" + b"\x00" * 64)          # o pre-flight so olha o mtime da DLL

    # Um gerado do BUILD em obj/ - tem de ser IGNORADO pela trava, senao ela se sabotaria
    # logo apos um build (o obj/ nasce com mtime do proprio build, depois da DLL).
    gerado = os.path.join(pasta, "obj", config, "netstandard2.1",
                          nome + ".AssemblyInfo.cs")
    with open(gerado, "w", encoding="utf-8") as fh:
        fh.write("// gerado pelo build\n")

    agora = os.path.getmtime(icone)
    # DLL no tempo T; a fonte em T-5min (build em dia) ou T+5min (o defeito do REL-1).
    os.utime(dll, (agora, agora))
    t_fonte = agora + (5 * MINUTO if fonte_mais_nova else -5 * MINUTO)
    os.utime(fonte, (t_fonte, t_fonte))
    os.utime(os.path.join(pasta, nome + ".csproj"), (agora - 5 * MINUTO, agora - 5 * MINUTO))
    os.utime(os.path.join(pasta, "Plugin.cs"), (agora - 5 * MINUTO, agora - 5 * MINUTO))
    # o gerado do build e o MAIS NOVO de todos, de proposito.
    os.utime(gerado, (agora + 10 * MINUTO, agora + 10 * MINUTO))

    return {"pasta": pasta, "dll": dll, "fonte": fonte, "gerado": gerado,
            "csproj": os.path.join(pasta, nome + ".csproj")}


def roda_preflight(raiz, nome="BetterTooltips", config="Release", usar_guarda=True):
    """Roda o pre-flight REAL (`verificar`) contra a raiz plantada.

    Devolve `(passou: bool, mensagem: str)`. `usar_guarda=False` desliga a trava
    `artefato_esta_atual` no modulo carregado - e o que mostra o defeito (pre-flight aceita
    a DLL velha em silencio) e o que da sentido a contra-prova.
    """
    m = carrega_empacotador()
    if not usar_guarda:
        m.artefato_esta_atual = lambda *a, **k: (0, None)

    antigo = m.RAIZ
    m.RAIZ = raiz
    try:
        try:
            m.verificar(nome, config)
            return True, ""
        except m.Falha as erro:
            return False, str(erro)
    finally:
        m.RAIZ = antigo


# ---------------------------------------------------------------------------
# o par de contra-prova tem de ser IDENTICO fora do bloco do defeito
# ---------------------------------------------------------------------------

def fontes_fora_do_bloco_do_defeito(caminho):
    """O corpo do arquivo (a partir de `def corpo`) sem as linhas do BLOCO-DO-DEFEITO.

    E o que torna honesto o par isca/conserto: os dois arquivos so podem diferir NO QUE
    DESCREVE O DEFEITO. Qualquer outra diferenca e um teste que deixou de ser o mesmo teste.
    O corte comeca em `def corpo` (mesma convencao do t_trava_cor_notas_fundidas): o
    cabecalho e o META dizem QUAL metade e qual, e por isso podem - e devem - diferir.
    """
    with open(caminho, encoding="utf-8") as fh:
        linhas = fh.read().splitlines()
    inicio = next((n for n, linha in enumerate(linhas) if linha.startswith("def corpo")), None)
    if inicio is None:
        return ""
    dentro, guardadas = False, []
    for linha in linhas[inicio:]:
        if linha.strip().startswith("# >>> BLOCO-DO-DEFEITO"):
            dentro = True
            continue
        if linha.strip().startswith("# <<< BLOCO-DO-DEFEITO"):
            dentro = False
            continue
        if not dentro:
            guardadas.append(linha)
    return "\n".join(guardadas).strip()
