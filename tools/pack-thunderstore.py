#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pack-thunderstore.py - empacota cada mod do repo no formato Thunderstore (r2modman).

O QUE ELE FAZ
-------------
Para CADA mod do repositorio (uma pasta na raiz com `<Mod>/<Mod>.csproj`), monta um
pacote .zip na pasta `dist/` seguindo a convencao do Thunderstore:

    <Autor>-<Mod>-<versao>.zip
      |-- manifest.json          <- metadados (o r2modman LE este arquivo na raiz)
      |-- README.md
      |-- CHANGELOG.md
      |-- icon.png               <- 256x256, obrigatorio
      `-- plugins/
            `-- <Mod>/
                  `-- <Mod>.dll  <- vem de <Mod>/bin/<Config>/netstandard2.1/<Mod>.dll

Os arquivos ficam na RAIZ do zip (nao dentro de uma pasta) - e assim que o r2modman
espera encontrar o manifest.json.

CONFIGURACAO DO BUILD (PKG-6)
-----------------------------
O pacote sai da build de **Release** por padrao (`--config Release`), que e a que passou
a existir no PKG-5 para gerar o artefato do `dist/`. O caminho da DLL e resolvido por
configuracao - `bin/<Config>/` - igual ao `$(Configuration)` do MSBuild, entao
`--config Debug` continua disponivel (ou `PACK_CONFIG=Debug no ambiente`).

ATENCAO: buildar Release com o alvo `DeployToBepInEx` ligado sobrescreve a DLL instalada
no perfil do r2modman. Por isso quem empacota builda com `-p:DeployToBepInEx=false`, e o
comando sugerido no erro sempre traz essa flag.

VERSAO UNICA (PKG-2)
--------------------
A versao autoritativa e o `<Version>` do `.csproj`. Os outros dois lugares que carregam
versao sao ESPELHOS e sao conferidos aqui, no pre-flight, antes de zipar qualquer coisa:

    <Mod>/<Mod>.csproj   <Version>0.1.0</Version>       <- FONTE
    <Mod>/manifest.json  "version_number": "0.1.0"      <- espelho (Thunderstore)
    <Mod>/Plugin.cs      [BepInPlugin(..., "0.1.0")]    <- espelho (BepInEx, o log)

Divergiu qualquer espelho -> NENHUM pacote e gerado, e a mensagem diz exatamente qual
arquivo/linha consertar. `--sincronizar-versao` reescreve os espelhos a partir do
`.csproj` (so o que divergiu): e o caminho de um comando depois de subir a versao.

REGRAS QUE O SCRIPT RESPEITA (regras do projeto)
------------------------------------------------
1. NUNCA inclui `lib/` (DLLs do jogo/BepInEx): a `Assembly-CSharp.dll` e propriedade
   do jogo e so serve de referencia de compilacao. So a DLL do proprio mod entra.
2. O pacote so carrega a DLL do mod - nenhum backup de DLL, que o BepInEx varreria
   recursivamente em `plugins/` e carregaria como se fosse um mod.
3. Se a DLL nao estiver buildada, ele AVISA e SAI COM ERRO sem gerar pacote nenhum
   (pacote incompleto e pior que pacote nenhum: o r2modman instalaria um mod quebrado).

PRE-FLIGHT, DEPOIS EMPACOTAMENTO
--------------------------------
Antes de zipar qualquer coisa, o script confere TODOS os mods: csproj, DLL buildada,
manifest.json (campos obrigatorios, semver, descricao <= 250 chars) e icon.png real de
256x256. So se todos passarem e que os zips sao gerados. Assim uma falha no meio nunca
deixa um dist/ com metade dos pacotes novos e metade dos antigos.

USO
---
    python tools/pack-thunderstore.py                   # todos os mods (Release)
    python tools/pack-thunderstore.py BetterFont        # so alguns
    python tools/pack-thunderstore.py --config Debug    # empacota a build de Debug
    python tools/pack-thunderstore.py --gerar-icones    # cria icon.png que faltarem
    python tools/pack-thunderstore.py --listar          # so mostra o que achou
    python tools/pack-thunderstore.py --sincronizar-versao   # espelhos <- <Version>

Rodar da RAIZ do repo (ele tambem funciona de qualquer lugar: acha a raiz sozinho).
"""

import argparse
import json
import os
import re
import shutil
import struct
import sys
import zipfile
import zlib

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

AUTOR = "gumatos"
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(RAIZ, "dist")
STAGE_RAIZ = os.path.join(DIST, "_thunderstore_stage")

TFM = "netstandard2.1"                 # alvo dos csproj do projeto
# PKG-6: o pacote publicado sai da build de Release (e a que o dist/ consome desde o PKG-5).
# Uma configuracao diferente (ex.: Debug, para conferir um pacote sem Release buildada) pode
# vir de --config ou da variavel de ambiente PACK_CONFIG.
CONFIG_PADRAO = os.environ.get("PACK_CONFIG") or "Release"
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
CAMPOS_OBRIGATORIOS = ("name", "version_number", "website_url", "description",
                       "dependencies")
DESC_MAX = 250                          # limite do Thunderstore

# Cor de fundo do icon.png de cada mod (r, g, b) - so estetica.
CORES_ICONE = {
    "BetterTooltips": (0x1E, 0x3A, 0x8A),
    "BetterFont": (0x1B, 0x5E, 0x20),
    "BetterStats": (0x4A, 0x14, 0x8C),
    "RoguelikeDebugger": (0x8E, 0x1B, 0x1B),
}
COR_PADRAO = (0x33, 0x33, 0x3A)
COR_LETRA = (0xF5, 0xF5, 0xF5)

# ---------------------------------------------------------------------------
# PNG 256x256 sem dependencia nenhuma (zlib + struct) - para gerar o icon.png
# ---------------------------------------------------------------------------
# Fonte 5x7 desenhada a mao: cada glifo e uma lista de 7 linhas de 5 bits.
GLIFOS = {
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10001", "01110", "00011"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "?": ("01110", "10001", "00010", "00100", "00100", "00000", "00100"),
}
GLIFO_W, GLIFO_H = 5, 7


def _png(w, h, pixel):
    """Monta os bytes de um PNG RGB de verdade (filtro 0, sem interlacing).

    `pixel(x, y)` devolve (r, g, b). Usa so zlib+struct: nenhuma dependencia.
    """
    raw = bytearray()
    for y in range(h):
        raw.append(0)                      # filtro "None" no inicio de cada linha
        for x in range(w):
            r, g, b = pixel(x, y)
            raw.append(r)
            raw.append(g)
            raw.append(b)

    def chunk(tag, dados):
        bloco = tag + dados
        return (struct.pack(">I", len(dados)) + bloco
                + struct.pack(">I", zlib.crc32(bloco) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)   # 8 bits, truecolor
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def png_tamanho(caminho):
    """Le largura e altura de um PNG pelo IHDR. None se o arquivo nao for PNG."""
    try:
        with open(caminho, "rb") as fh:
            cabecalho = fh.read(24)
    except OSError:
        return None
    if len(cabecalho) < 24 or cabecalho[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if cabecalho[12:16] != b"IHDR":
        return None
    largura, altura = struct.unpack(">II", cabecalho[16:24])
    return largura, altura


def iniciais(nome_mod):
    """'BetterTooltips' -> 'BT'; 'RoguelikeDebugger' -> 'RD'."""
    maiusculas = [c for c in nome_mod if c.isupper()]
    if len(maiusculas) >= 2:
        return (maiusculas[0] + maiusculas[1]).upper()
    return nome_mod[:2].upper()


def gerar_icone(nome_mod, destino, tamanho=256):
    """Escreve um icon.png `tamanho`x`tamanho` de verdade: fundo solido + borda + iniciais."""
    fundo = CORES_ICONE.get(nome_mod, COR_PADRAO)
    letra = iniciais(nome_mod)
    escala = 20
    glifo_px_w = GLIFO_W * escala
    glifo_px_h = GLIFO_H * escala
    vao = escala
    total_w = glifo_px_w * 2 + vao
    x0 = (tamanho - total_w) // 2
    y0 = (tamanho - glifo_px_h) // 2
    margem, espessura = 8, 5

    def e_borda(x, y):
        dentro = (margem <= x < tamanho - margem and margem <= y < tamanho - margem)
        if not dentro:
            return False
        return (x < margem + espessura or x >= tamanho - margem - espessura
                or y < margem + espessura or y >= tamanho - margem - espessura)

    # Pre-calcula a mascara do texto (2 glifos lado a lado).
    def cheio(dx, dy):
        for indice, char in enumerate(letra):
            linha = GLIFOS.get(char, GLIFOS["?"])[dy // escala]
            for px in range(GLIFO_W):
                if linha[px] == "1":
                    gx = x0 + indice * (glifo_px_w + vao) + px * escala
                    if gx <= dx < gx + escala:
                        return True
        return False

    def pixel(x, y):
        if e_borda(x, y):
            return (min(fundo[0] + 0x50, 255), min(fundo[1] + 0x50, 255),
                    min(fundo[2] + 0x50, 255))
        dx, dy = x - x0, y - y0
        if 0 <= dx < total_w and 0 <= dy < glifo_px_h and cheio(dx, dy):
            return COR_LETRA
        return fundo

    dados = _png(tamanho, tamanho, pixel)
    with open(destino, "wb") as fh:
        fh.write(dados)
    return len(dados)


# ---------------------------------------------------------------------------
# Descoberta dos mods
# ---------------------------------------------------------------------------

def eh_mod(nome):
    """Mod de verdade = pasta na raiz com `<Mod>/<Mod>.csproj` que tenha o target
    `DeployToBepInEx` (a convencao do projeto: cada mod tem o seu e copia a DLL para
    `BepInEx\\plugins\\`). Isso deixa de fora `ReloadProbe`, que e harness de teste e
    copia para `BepInEx\\scripts\\` - nao e mod e nao pode virar pacote Thunderstore.
    """
    pasta = os.path.join(RAIZ, nome)
    if not os.path.isdir(pasta):
        return False
    csproj = os.path.join(pasta, nome + ".csproj")
    if not os.path.isfile(csproj):
        return False
    try:
        with open(csproj, encoding="utf-8", errors="replace") as fh:
            texto = fh.read()
    except OSError:
        return False
    return "DeployToBepInEx" in texto and "plugins" in texto


def projetos_ignorados():
    """Pastas na raiz que tem csproj mas NAO sao mod (ex.: ReloadProbe)."""
    ignorados = []
    for entrada in sorted(os.listdir(RAIZ)):
        pasta = os.path.join(RAIZ, entrada)
        if not os.path.isdir(pasta):
            continue
        if os.path.isfile(os.path.join(pasta, entrada + ".csproj")) and not eh_mod(entrada):
            ignorados.append(entrada)
    return ignorados


def descobrir_mods():
    """Todos os mods do repo, em ordem alfabetica."""
    return [entrada for entrada in sorted(os.listdir(RAIZ))
            if eh_mod(entrada)]


def caminhos(nome_mod, config=CONFIG_PADRAO):
    pasta = os.path.join(RAIZ, nome_mod)
    return {
        "pasta": pasta,
        "csproj": os.path.join(pasta, nome_mod + ".csproj"),
        # PKG-6: o caminho da DLL segue a CONFIGURACAO, igual ao $(Configuration) do
        # MSBuild (bin/<Config>/netstandard2.1/). Antes era fixo em bin/Debug e o pacote
        # publicado saia da build errada.
        "dll": os.path.join(pasta, "bin", config, TFM, nome_mod + ".dll"),
        "manifest": os.path.join(pasta, "manifest.json"),
        "plugin": os.path.join(pasta, "Plugin.cs"),
        "readme": os.path.join(pasta, "README.md"),
        "changelog": os.path.join(pasta, "CHANGELOG.md"),
        "icon": os.path.join(pasta, "icon.png"),
    }


# ---------------------------------------------------------------------------
# Verificacoes
# ---------------------------------------------------------------------------

class Falha(Exception):
    pass


def ler_manifest(nome_mod, p):
    if not os.path.isfile(p["manifest"]):
        raise Falha("manifest.json nao existe (formato Thunderstore, ver o repo)")
    try:
        with open(p["manifest"], encoding="utf-8") as fh:
            manifesto = json.load(fh)
    except ValueError as erro:
        raise Falha("manifest.json nao e JSON valido: %s" % erro)

    faltando = [c for c in CAMPOS_OBRIGATORIOS if c not in manifesto]
    if faltando:
        raise Falha("manifest.json sem campo(s) obrigatorio(s): %s"
                    % ", ".join(faltando))

    versao = manifesto["version_number"]
    if not isinstance(versao, str) or not SEMVER.match(versao):
        raise Falha("version_number '%s' nao esta no formato semver (ex.: 0.1.0)"
                    % versao)

    descricao = manifesto["description"]
    if not isinstance(descricao, str) or not descricao.strip():
        raise Falha("description vazia")
    if len(descricao) > DESC_MAX:
        raise Falha("description tem %d caracteres (limite do Thunderstore: %d)"
                    % (len(descricao), DESC_MAX))

    if not isinstance(manifesto["dependencies"], list):
        raise Falha("dependencies tem que ser uma lista (use [] se nao houver)")

    if not isinstance(manifesto.get("extra", {}), dict):
        raise Falha("extra tem que ser um objeto")

    # O nome do pacote e o nome da pasta dos plugins: se divergirem, o r2modman
    # instala num caminho diferente do que o README promete.
    if manifesto["name"] != nome_mod:
        raise Falha("manifest name '%s' != pasta do mod '%s'"
                    % (manifesto["name"], nome_mod))
    return manifesto


# ---------------------------------------------------------------------------
# PKG-2: versao unica - o <Version> do .csproj e a FONTE, o resto sao espelhos
# ---------------------------------------------------------------------------

def versao_do_csproj(p):
    """A versao autoritativa: o `<Version>` do `.csproj`. None se nao achar."""
    if not os.path.isfile(p["csproj"]):
        return None
    with open(p["csproj"], encoding="utf-8", errors="replace") as fh:
        achado = re.search(r"<Version>([^<]+)</Version>", fh.read())
    return achado.group(1).strip() if achado else None


def versao_do_plugin(nome_mod, p):
    """A versao que o BepInEx registra no log, lida do `Plugin.cs`.

    Mesmo criterio de `tools/audita_docs.py` (o CI cobra esse formato): o literal pode
    estar no proprio atributo - `[BepInPlugin("guid", "nome", "0.1.0")]` - ou numa
    constante usada como ultimo argumento - `[BepInPlugin(Guid, "nome", Version)]` com
    `public const string Version = "0.1.0";` (padrao do RoguelikeSkillTreeVisualizer).

    Devolve `(versao, nome_da_constante)`; `(None, None)` quando nao acha.
    """
    if not os.path.isfile(p["plugin"]):
        return None, None
    with open(p["plugin"], encoding="utf-8", errors="replace") as fh:
        fonte = fh.read()

    literal = re.search(r'Plugin\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"', fonte)
    if literal:
        return literal.group(3), None

    atributo = re.search(r"\[BepInPlugin\(([^)]*)\)\]", fonte)
    if atributo:
        ident = re.search(r",\s*([A-Za-z_][\w.]*)\s*$", atributo.group(1).strip())
        if ident:
            nome = ident.group(1).split(".")[-1]
            const = re.search(r'const\s+string\s+%s\s*=\s*"([^"]+)"' % re.escape(nome), fonte)
            if const:
                return const.group(1), nome
    return None, None


def conferir_versoes(nome_mod, p, manifesto):
    """Tres lugares carregam a versao; so o `<Version>` do .csproj manda (PKG-2).

    Levanta `Falha` quando qualquer espelho divergir - pacote com versao errada e
    exatamente o que o Thunderstore recusa (versao repetida) ou o que faz o log mentir.
    Devolve a versao da fonte quando tudo bate.
    """
    fonte = versao_do_csproj(p)
    if not fonte:
        raise Falha("PKG-2: %s/%s.csproj sem <Version> (e o <Version> que manda)"
                    % (nome_mod, nome_mod))
    if not SEMVER.match(fonte):
        raise Falha("PKG-2: <Version>%s</Version> do .csproj nao esta em semver X.Y.Z"
                    % fonte)

    no_manifest = manifesto["version_number"]
    no_plugin, const = versao_do_plugin(nome_mod, p)
    if no_plugin is None:
        raise Falha("PKG-2: nao achei a versao em %s/Plugin.cs (esperava o literal no "
                    "[BepInPlugin(\"guid\", \"nome\", \"x.y.z\")] ou uma const Version)"
                    % nome_mod)
    if no_manifest != fonte or no_plugin != fonte:
        raise Falha(
            "PKG-2: VERSAO DIVERGE (o .csproj e a fonte)\n"
            "      %s/%s.csproj      <Version>%s</Version>  <- FONTE\n"
            "      %s/manifest.json  \"version_number\": \"%s\"%s\n"
            "      %s/Plugin.cs      %s \"%s\"%s\n"
            "      -> conserte o(s) DIVERGE, ou rode de uma vez:\n"
            "         python tools/pack-thunderstore.py --sincronizar-versao %s"
            % (nome_mod, nome_mod, fonte,
               nome_mod, no_manifest, "  <-- DIVERGE" if no_manifest != fonte else "",
               nome_mod, ("const %s =" % const) if const else "[BepInPlugin(...)]",
               no_plugin, "  <-- DIVERGE" if no_plugin != fonte else "", nome_mod))
    return fonte


# ---------------------------------------------------------------------------
# PKG-2: sincronizar os espelhos a partir do .csproj (so o que divergir)
# ---------------------------------------------------------------------------

def sincronizar_versao(nome_mod):
    """Reescreve manifest.json e Plugin.cs com o `<Version>` do .csproj.

    Mexe SO na versao e SO quando diverge (o arquivo fica byte-a-byte igual se ja estava
    certo). Devolve a lista de mudancas feitas, em texto.
    """
    p = caminhos(nome_mod)
    fonte = versao_do_csproj(p)
    if not fonte or not SEMVER.match(fonte):
        raise Falha("PKG-2: %s.csproj sem <Version> semver (nada a sincronizar)" % nome_mod)
    mudancas = []

    # --- manifest.json: troca o valor de version_number, nada mais -------------
    # Leitura e escrita com newline="" : os bytes que nao sao a versao passam intactos
    # (fim de linha inclusive) - sincronizar nao pode reformatar o arquivo.
    if os.path.isfile(p["manifest"]):
        with open(p["manifest"], encoding="utf-8", newline="") as fh:
            texto = fh.read()
        padrao = re.compile(r'("version_number"\s*:\s*")([^"]*)(")')
        achado = padrao.search(texto)
        if achado and achado.group(2) != fonte:
            with open(p["manifest"], "w", encoding="utf-8", newline="") as fh:
                fh.write(padrao.sub(lambda m: m.group(1) + fonte + m.group(3), texto, count=1))
            mudancas.append("manifest.json: version_number %s -> %s"
                            % (achado.group(2), fonte))

    # --- Plugin.cs: troca o literal da versao (atributo ou const) --------------
    if os.path.isfile(p["plugin"]):
        versao_plugin, const = versao_do_plugin(nome_mod, p)
        if versao_plugin is not None and versao_plugin != fonte:
            with open(p["plugin"], encoding="utf-8", newline="") as fh:
                texto = fh.read()
            if const:
                padrao = re.compile(r'(const\s+string\s+%s\s*=\s*")([^"]*)(")'
                                    % re.escape(const))
            else:
                padrao = re.compile(r'(Plugin\(\s*"[^"]+"\s*,\s*"[^"]+"\s*,\s*")([^"]*)(")')
            novo = padrao.sub(lambda m: m.group(1) + fonte + m.group(3), texto, count=1)
            if novo != texto:
                with open(p["plugin"], "w", encoding="utf-8", newline="") as fh:
                    fh.write(novo)
                mudancas.append("Plugin.cs: %s %s -> %s"
                                % ("const %s" % const if const else "[BepInPlugin]",
                                   versao_plugin, fonte))
    return fonte, mudancas


def verificar(nome_mod, config=CONFIG_PADRAO, gerar_icone_se_faltar=False):
    """Pre-flight de UM mod. Devolve (manifesto, dict de caminhos). Levanta Falha."""
    p = caminhos(nome_mod, config)

    if not os.path.isfile(p["csproj"]):
        raise Falha("nao e mod: falta %s.csproj" % nome_mod)

    if not os.path.isfile(p["dll"]):
        raise Falha("DLL NAO BUILDADA: %s\n"
                    "      -> rode:  dotnet build %s/%s.csproj -c %s "
                    "-p:DeployToBepInEx=false"
                    % (os.path.relpath(p["dll"], RAIZ), nome_mod, nome_mod, config))

    manifesto = ler_manifest(nome_mod, p)

    # PKG-2: fonte unica de versao - manifest e Plugin.cs tem que bater com o .csproj
    conferir_versoes(nome_mod, p, manifesto)

    for chave in ("readme", "changelog"):
        if not os.path.isfile(p[chave]):
            raise Falha("%s nao existe" % os.path.basename(p[chave]))

    if not os.path.isfile(p["icon"]) and gerar_icone_se_faltar:
        gerar_icone(nome_mod, p["icon"])
    if not os.path.isfile(p["icon"]):
        raise Falha("icon.png nao existe (rode com --gerar-icones para criar)")
    medidas = png_tamanho(p["icon"])
    if medidas is None:
        raise Falha("icon.png nao e um PNG valido")
    if medidas != (256, 256):
        raise Falha("icon.png tem %dx%d (o Thunderstore exige 256x256)" % medidas)

    return manifesto, p


# ---------------------------------------------------------------------------
# Empacotamento
# ---------------------------------------------------------------------------

def empacotar(nome_mod, manifesto, p):
    """Monta o stage e zipa. Devolve (caminho do zip, lista de (nome_no_zip, bytes))."""
    pasta_pacote = "%s-%s" % (AUTOR, nome_mod)
    stage = os.path.join(STAGE_RAIZ, pasta_pacote)
    if os.path.isdir(stage):
        shutil.rmtree(stage)
    os.makedirs(os.path.join(stage, "plugins", nome_mod))

    copiados = [("manifest.json", p["manifest"]),
                ("README.md", p["readme"]),
                ("CHANGELOG.md", p["changelog"]),
                ("icon.png", p["icon"])]
    for destino, origem in copiados:
        shutil.copy2(origem, os.path.join(stage, destino))
    shutil.copy2(p["dll"],
                 os.path.join(stage, "plugins", nome_mod, nome_mod + ".dll"))

    versao = manifesto["version_number"]
    zip_path = os.path.join(DIST, "%s-%s.zip" % (pasta_pacote, versao))
    if os.path.isfile(zip_path):
        os.remove(zip_path)

    conteudo = []
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Caminha o stage: o nome no zip e relativo a ele, entao tudo fica na RAIZ
        # do pacote - que e onde o r2modman procura o manifest.json.
        for base, _dirs, arquivos in os.walk(stage):
            for arquivo in sorted(arquivos):
                origem = os.path.join(base, arquivo)
                nome_no_zip = os.path.relpath(origem, stage).replace(os.sep, "/")
                zf.write(origem, nome_no_zip)
                conteudo.append((nome_no_zip, os.path.getsize(origem)))

    shutil.rmtree(stage, ignore_errors=True)
    return zip_path, conteudo


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv):
    ap = argparse.ArgumentParser(
        description="Empacota os mods do repo no formato Thunderstore (r2modman).")
    ap.add_argument("mods", nargs="*", help="nomes dos mods (padrao: todos)")
    ap.add_argument("--config", default=CONFIG_PADRAO, metavar="Release|Debug",
                    help="configuracao do build de onde sai a DLL (padrao: %s; "
                         "o ambiente PACK_CONFIG tambem vale)" % CONFIG_PADRAO)
    ap.add_argument("--gerar-icones", action="store_true",
                    help="cria um icon.png 256x256 nos mods que estiverem sem")
    ap.add_argument("--listar", action="store_true",
                    help="so lista os mods encontrados e sai")
    ap.add_argument("--listar-nomes", action="store_true",
                    help="imprime SO os nomes dos mods (um por linha) - para consumir de "
                         "script (scripts/package.ps1); a descoberta de mod fica NUM lugar")
    ap.add_argument("--sincronizar-versao", action="store_true",
                    help="reescreve manifest.json e Plugin.cs com o <Version> do .csproj "
                         "(PKG-2) e sai, sem empacotar")
    args = ap.parse_args(argv)

    todos = descobrir_mods()
    if not todos:
        print("!! nenhum mod encontrado em %s (esperava pastas <Mod>/<Mod>.csproj)"
              % RAIZ)
        return 1

    if args.listar_nomes:
        # Saida maquina-legivel: SO os nomes, um por linha. E daqui que o
        # scripts/package.ps1 (Windows) tira a lista de mods - descoberta de mod fica
        # em UM lugar (eh_mod), nunca numa segunda lista que pode divergir.
        for m in todos:
            print(m)
        return 0

    if args.listar:
        print("Mods encontrados em %s:" % RAIZ)
        for m in todos:
            print("  - %-18s (csproj com DeployToBepInEx)" % m)
        ignorados = projetos_ignorados()
        if ignorados:
            print("Ignorados (tem csproj mas nao sao mod - nao copiam para plugins/):")
            for m in ignorados:
                print("  - %s" % m)
        return 0

    alvos = args.mods or todos
    desconhecidos = [m for m in alvos if m not in todos]
    if desconhecidos:
        print("!! nao existe mod com esse nome: %s" % ", ".join(desconhecidos))
        print("   mods disponiveis: %s" % ", ".join(todos))
        return 2

    # PKG-2: so conserta os espelhos da versao e sai (nao empacota nada).
    if args.sincronizar_versao:
        print("== PKG-2: sincronizando a versao a partir do <Version> do .csproj ==")
        problemas = 0
        for mod in alvos:
            try:
                fonte, mudancas = sincronizar_versao(mod)
            except Falha as erro:
                problemas += 1
                print("  FALHA %-18s %s" % (mod, erro))
                continue
            if mudancas:
                print("  %-18s fonte <Version>%s</Version>" % (mod, fonte))
                for m in mudancas:
                    print("        %s" % m)
            else:
                print("  ok    %-18s v%s (manifest e Plugin.cs ja batiam)"
                      % (mod, fonte))
        print()
        if problemas:
            print(">>> %d mod(s) sem <Version> valido no .csproj." % problemas)
            return 1
        print("Espelhos sincronizados. Rode de novo sem --sincronizar-versao para empacotar.")
        return 0

    if args.gerar_icones:
        print("== icon.png (256x256) ==")
        for mod in alvos:
            p = caminhos(mod, args.config)
            medidas = png_tamanho(p["icon"]) if os.path.isfile(p["icon"]) else None
            if medidas == (256, 256):
                print("  ok    %-18s ja existe (256x256, %d bytes)"
                      % (mod, os.path.getsize(p["icon"])))
            else:
                escritos = gerar_icone(mod, p["icon"])
                print("  feito %-18s icon.png criado (256x256, %d bytes)"
                      % (mod, escritos))
        print()

    print("Repo : %s" % RAIZ)
    print("Saida: %s" % DIST)
    print("Mods : %s" % ", ".join(alvos))
    print("Build: %s  (a DLL vem de <Mod>/bin/%s/%s/)" % (args.config, args.config, TFM))
    print()

    # ---- pre-flight de TODOS antes de escrever qualquer zip -----------------
    print("== conferindo (build %s, versao unica, manifest, icon) ==" % args.config)
    verificados, problemas = {}, 0
    for mod in alvos:
        try:
            verificados[mod] = verificar(mod, args.config, args.gerar_icones)
            manifesto = verificados[mod][0]
            print("  ok    %-18s v%s  | %s"
                  % (mod, manifesto["version_number"],
                     os.path.relpath(verificados[mod][1]["dll"], RAIZ)))
        except Falha as erro:
            problemas += 1
            print("  FALHA %-18s %s" % (mod, erro))
    if problemas:
        print()
        print(">>> %d mod(s) com problema: NENHUM pacote foi gerado." % problemas)
        print("    (pacote incompleto e pior que pacote nenhum: o r2modman")
        print("     instalaria um mod sem a DLL. Corrija e rode de novo.)")
        return 1

    # ---- empacotamento ------------------------------------------------------
    print()
    print("== empacotando ==")
    os.makedirs(DIST, exist_ok=True)
    gerados = []
    for mod in alvos:
        manifesto, p = verificados[mod]
        zip_path, conteudo = empacotar(mod, manifesto, p)
        gerados.append(zip_path)
        total = sum(tamanho for _, tamanho in conteudo)
        print("  %s: %s" % (mod, os.path.basename(zip_path)))
        for nome_no_zip, tamanho in conteudo:
            print("      %-42s %7d bytes" % (nome_no_zip, tamanho))
        print("      %-42s %7d bytes  (%d arquivos)"
              % ("TOTAL", total, len(conteudo)))

    print()
    print("PRONTO - %d pacote(s) em dist/:" % len(gerados))
    for caminho in gerados:
        print("  %s  (%d bytes)" % (caminho, os.path.getsize(caminho)))

    # Nao deixar o stage vazio para tras (dist/ e gitignored, mas pasta vazia confunde).
    if os.path.isdir(STAGE_RAIZ) and not os.listdir(STAGE_RAIZ):
        os.rmdir(STAGE_RAIZ)

    print()
    print("Instalar: no r2modman, aba 'Online' -> 'Install from file' -> escolha o zip")
    print("(ou faca upload no thunderstore.io com os mesmos arquivos).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
