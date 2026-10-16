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

LAYOUT NAO-RAIZ (PKG-API-1)
---------------------------
Nem todo pacote do repo segue esse layout. O `RealmApi` e' um modulo ANINHADO: o projeto
do plugin vive em `api/Plugin/RealmApi.csproj` (o csproj carrega o nome do ASSEMBLY, nao
o da pasta) e a build produz TRES assemblies - o plugin (`RealmApi.dll`) mais as duas
referencias de projeto que ele carrega em runtime (`RealmApi.Core.dll`,
`RealmApi.Hooks.dll`). Os metadados do pacote (`manifest.json`, `icon.png`,
`README.md`, `CHANGELOG.md`, `LICENSE`) ficam em `api/`, um nivel acima do projeto.

Esse caso nao cabe no `eh_mod` (que procura `<Mod>/<Mod>.csproj` na raiz e uma DLL so) e
por isso vive numa tabela EXPLICITA - `PACOTES_NAO_RAIZ`: quem entra ali e' decisao
registrada, nao heuristica. O pacote que sai e' o MESMO dos outros oito (metadados na
raiz do zip, DLLs em `plugins/<Pacote>/`); o que muda e' so ONDE os arquivos nascem no
repositorio e QUANTAS DLLs entram. O gate de `release/mods.json` continua vendo os nove
pacotes pela MESMA lista (`--listar-nomes`).

CONFIGURACAO DO BUILD (PKG-6)
-----------------------------
O pacote sai da build de **Release** por padrao (`--config Release`), que e a que passou
a existir no PKG-5 para gerar o artefato do `dist/`. O caminho da DLL e resolvido por
configuracao - `bin/<Config>/` - igual ao `$(Configuration)` do MSBuild, entao
`--config Debug` continua disponivel (ou `PACK_CONFIG=Debug no ambiente`).

ATENCAO: buildar Release com o alvo `DeployToBepInEx` ligado sobrescreve a DLL instalada
no perfil do r2modman. Por isso quem empacota builda com `-p:DeployToBepInEx=false`, e o
comando sugerido no erro sempre traz essa flag.

ARTEFATO x FONTE (REL-1)
------------------------
Existir em `bin/<Config>/` nao basta: a DLL tem de corresponder a fonte que esta no
repositorio AGORA. A trava `artefato_esta_atual` recusa o pacote quando a DLL e mais antiga
que o arquivo de fonte mais novo do mod - o caso medido em 01/10/2026, em que
`bin/Release/BetterTooltips.dll` ainda carregava o `HarmonyPriority(600)` que uma correcao
do dia ja tinha removido da fonte. Empacotar aceitaria qualquer coisa que estivesse ali.

VERSAO UNICA (PKG-2 / PKG-3)
----------------------------
A versao autoritativa e o `<Version>` do `.csproj`. Os outros TRES lugares que carregam
versao sao ESPELHOS e sao conferidos aqui, no pre-flight, antes de zipar qualquer coisa:

    <Mod>/<Mod>.csproj   <Version>0.1.0</Version>       <- FONTE
    <Mod>/manifest.json  "version_number": "0.1.0"      <- espelho (Thunderstore)
    <Mod>/Plugin.cs      [BepInPlugin(..., "0.1.0")]    <- espelho (BepInEx, o log)
    <Mod>/README.md      - **Version:** 0.1.0           <- espelho (PKG-3: o usuario le)

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
    python tools/pack-thunderstore.py --so-conferir      # roda o pre-flight (artefato x fonte
                                                         # incluido) e sai SEM gerar zip
    python tools/pack-thunderstore.py --sincronizar-versao   # espelhos <- <Version>

Rodar da RAIZ do repo (ele tambem funciona de qualquer lugar: acha a raiz sozinho).
"""

import argparse
import datetime
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
    # LEVEL-PACOTE-CONTRATO: mod novo ganha cor propria (o padrao cinza e o mesmo do
    # BetterCombatText/RSTV). RLP-RENAME: o glifo "U" acompanha as iniciais "RU"
    # do nome novo na fonte 5x7; a cor e a moldura ficam iguais. So o icone deste mod
    # e atualizado; nenhum icone de outro mod e regerado.
    "RoguelikeUnlimitedLevelProgression": (0x86, 0x5E, 0x0A),
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
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "Q": ("01110", "10001", "10001", "10001", "10001", "01110", "00011"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10010", "10010", "10010", "10010", "10010", "10010", "01100"),
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
# PACOTES NAO-RAIZ (PKG-API-1) - modulo aninhado, mais de uma DLL
# ---------------------------------------------------------------------------
# O detector `eh_mod` cobre o layout padrao: pasta na raiz, `<Mod>/<Mod>.csproj`, uma
# DLL em `bin/<Config>/netstandard2.1/`. O RealmApi viola DUAS dessas premissas de uma
# vez:
#
#   1. o projeto NAO esta na raiz - vive em `api/Plugin/`, e o nome do csproj e' o do
#      ASSEMBLY (`RealmApi.csproj`), nao o da pasta (`Plugin`);
#   2. a build produz TRES DLLs, nao uma: `RealmApi.dll` (o plugin) mais
#      `RealmApi.Core.dll` e `RealmApi.Hooks.dll` - as duas referencias de projeto que o
#      BepInEx precisa resolver ao carregar o plugin (sem elas o plugin nao sobe). As
#      tres saem da MESMA pasta de saida (`api/Plugin/bin/<Config>/netstandard2.1/`).
#
# Por isso este caso e' TABELA, nao palpite do detector: cada entrada diz onde estao os
# metadados, onde esta o csproj, quais DLLs entram e em que pasta elas vao para dentro
# do zip. Nao ha heuristica que "descubra" isso sem risco de classificar como pacote
# alguma pasta que nao e' - `api/Smoke` e' harness de teste e `api/tools/Inspect` e'
# ferramenta de bancada; nenhum dos dois vira pacote.
#
# `dlls` tambem diz, por DLL, QUAL e' a fonte que a trava REL-1 confere (segundo item de
# cada par): a DLL do plugin contra `api/Plugin/`, a Core contra `api/Core/`, a Hooks
# contra `api/Hooks/`. Conferir as tres contra a arvore `api/` inteira reprovaria pacote
# bom - um `.cs` do smoke, que nem entra no zip, e' mais novo que a DLL.
PACOTES_NAO_RAIZ = {
    "RealmApi": {
        # Manifest, icone, README, CHANGELOG, LICENSE.
        "metadados": ("api",),
        # Pasta do .csproj e da saida da build.
        "projeto": ("api", "Plugin"),
        "csproj": "RealmApi.csproj",
        # Pasta que recebe as DLLs dentro do zip: plugins/RealmApi/.
        "pasta_no_zip": "RealmApi",
        "dlls": (
            ("RealmApi.dll", ("api", "Plugin")),
            ("RealmApi.Core.dll", ("api", "Core")),
            ("RealmApi.Hooks.dll", ("api", "Hooks")),
        ),
        # Onde a versao aparece fora do .csproj: o [BepInPlugin] esta no arquivo do
        # plugin e a const que ele cita (`ApiIdentity.Version`) mora no Core - dois
        # arquivos, nao um (o layout padrao usa so o Plugin.cs).
        "versao_em": (("api", "Plugin", "RealmApiPlugin.cs"),
                      ("api", "Core", "Contracts.cs")),
        # Arquivo a mais na RAIZ do zip alem dos quatro de sempre.
        "extras": ("LICENSE",),
    },
}


def rel(caminho):
    """Caminho relativo a raiz do repo, com '/' - o que o zip e os gates usam."""
    return os.path.relpath(caminho, RAIZ).replace(os.sep, "/")


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


def eh_pacote_nao_raiz(nome):
    """O pacote esta na tabela PACOTES_NAO_RAIZ (modulo aninhado, multi-DLL)?"""
    return nome in PACOTES_NAO_RAIZ


def descobrir_mods():
    """Todos os pacotes do repo, em ordem alfabetica GLOBAL.

    Soma o que o detector acha na raiz (`eh_mod`) com o que esta declarado na tabela
    PACOTES_NAO_RAIZ. A ordem e' alfabetica sobre o conjunto todo (nao "raiz primeiro"):
    e' ESTA lista, nesta ordem, que o gate do `publish.yml` compara com o `nome` de cada
    entrada do `release/mods.json` - entao no ledger o RealmApi entra entre os "R"
    (antes de RoguelikeDebugger: 'e' < 'o').
    """
    na_raiz = [entrada for entrada in os.listdir(RAIZ) if eh_mod(entrada)]
    return sorted(set(na_raiz) | set(PACOTES_NAO_RAIZ))


def caminhos(nome_mod, config=CONFIG_PADRAO):
    """Todos os caminhos do pacote - no layout padrao ou no nao-raiz (PKG-API-1).

    As chaves que o resto do script consome sao as MESMAS nos dois casos:
    `dlls` (todas as DLLs que entram no zip: uma no layout padrao, tres no RealmApi),
    `fontes_por_dll` (a fonte que a trava REL-1 confere para CADA DLL),
    `versao_em` (os arquivos que carregam a versao alem do .csproj),
    `pasta_no_zip` (a pasta em plugins/ que recebe as DLLs) e `extras` (arquivos a mais
    na raiz do zip - vazio no layout padrao).
    """
    especial = PACOTES_NAO_RAIZ.get(nome_mod)
    if especial:
        meta = os.path.join(RAIZ, *especial["metadados"])
        projeto = os.path.join(RAIZ, *especial["projeto"])
        dlls, fontes_por_dll = [], {}
        for nome, pastas in especial["dlls"]:
            dll = os.path.join(projeto, "bin", config, TFM, nome)
            dlls.append(dll)
            fontes_por_dll[dll] = [os.path.join(RAIZ, *p) for p in pastas]
        return {
            "pasta": meta,                          # onde vivem os metadados
            "csproj": os.path.join(projeto, especial["csproj"]),
            "dll": dlls[0],
            "dlls": dlls,
            "fontes_por_dll": fontes_por_dll,
            "versao_em": [os.path.join(RAIZ, *f) for f in especial["versao_em"]],
            "pasta_no_zip": especial["pasta_no_zip"],
            "extras": [os.path.join(meta, extra) for extra in especial["extras"]],
            "manifest": os.path.join(meta, "manifest.json"),
            "readme": os.path.join(meta, "README.md"),
            "changelog": os.path.join(meta, "CHANGELOG.md"),
            "icon": os.path.join(meta, "icon.png"),
        }

    pasta = os.path.join(RAIZ, nome_mod)
    # PKG-6: o caminho da DLL segue a CONFIGURACAO, igual ao $(Configuration) do
    # MSBuild (bin/<Config>/netstandard2.1/). Antes era fixo em bin/Debug e o pacote
    # publicado saia da build errada.
    dll = os.path.join(pasta, "bin", config, TFM, nome_mod + ".dll")
    return {
        "pasta": pasta,
        "csproj": os.path.join(pasta, nome_mod + ".csproj"),
        "dll": dll,
        "dlls": [dll],
        "fontes_por_dll": {dll: [pasta]},
        "versao_em": [os.path.join(pasta, "Plugin.cs")],
        "pasta_no_zip": nome_mod,
        "extras": [],
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


# PKG-3: o QUARTO lugar que carrega a versao e o README do mod. Ele nao entra na
# compilacao nem como metadado do pacote (vai como texto), entao ficava fora da trava e
# podia envelhecer sozinho - o usuario leria a versao errada no que instalou. O padrao e o
# que os SEIS READMEs ja usam, nao um formato novo:
#
#     - **Version:** 0.1.0
PADRAO_VERSAO_README = re.compile(r"^- \*\*Version:\*\*\s+(\S+)\s*$", re.MULTILINE)


def versao_do_readme(p):
    """A versao declarada na linha `- **Version:** x.y.z` do README do mod.

    Devolve a string crua, ou None se o README (ou a linha) nao existir. Nao valida
    semver nem compara com a fonte: quem faz isso e `conferir_versoes`, que tem a fonte.
    """
    if not os.path.isfile(p["readme"]):
        return None
    with open(p["readme"], encoding="utf-8", errors="replace") as fh:
        achado = PADRAO_VERSAO_README.search(fh.read())
    return achado.group(1) if achado else None


# ---------------------------------------------------------------------------
# REL-1: o artefato tem de CORRESPONDER a fonte, nao so existir
# ---------------------------------------------------------------------------
# O modo de falha que esta trava existe para pegar NAO e "a Release ficou velha": e o
# empacotador aceitar QUALQUER arquivo que esteja em bin/<Config>/. Ele conferia que a DLL
# existia, nunca se ela correspondia a fonte que esta no repositorio AGORA. Resultado
# medido (REV-55, 01/10/2026): bin/Release/BetterTooltips.dll era de 30/09 22:52 e ainda
# carregava o HarmonyPriority(600) do CorDoJogoPostfix que a COR-2 tinha acabado de remover
# da fonte - empacotar teria entregue o defeito, com a versao nova no manifest.
#
# A checagem e a mais simples que separa os dois casos: a DLL tem de ser MAIS NOVA que o
# arquivo de fonte mais novo que entra na compilacao dela. Editou um .cs e nao reconstruiu?
# O mtime da fonte fica na frente do mtime da DLL e o pacote e RECUSADO, em vez de sair com
# um binario que nao tem a edicao.
#
# O que ela NAO ve, e por que ainda assim e a certa: um artefato COPIADO de outro lugar
# entra com mtime novo e passa. Copiar DLL a mao nao e passo do processo - quem builda e o
# `dotnet build` (scripts/package.ps1, release-check.sh) - e nesse caminho o mtime e sinal
# fiel. Provar por hash exigiria o empacotador reconstruir (nao pode: precisa da lib/ do
# jogo e do toolchain) ou o build gravar um fingerprint, bem mais invasivo que o defeito.
FONTES_COMPILADAS = (".cs", ".csproj")
PASTAS_QUE_NAO_SAO_FONTE = ("bin", "obj")


def fontes_do_mod(pasta):
    """Arquivos que entram na compilacao do mod: `<Mod>/**/*.cs` e os `.csproj`.

    `bin/` e `obj/` ficam de fora: sao saida do build, e o `obj/` guarda os gerados
    (`*.AssemblyInfo.cs`) com mtime do PROPRIO build - conta-los faria a checagem se
    auto-sabotar.
    """
    achados = []
    for base, pastas, arquivos in os.walk(pasta):
        pastas[:] = [d for d in pastas if d not in PASTAS_QUE_NAO_SAO_FONTE]
        for arquivo in arquivos:
            if arquivo.endswith(FONTES_COMPILADAS):
                achados.append(os.path.join(base, arquivo))
    return achados


def quando(mtime):
    """mtime legivel (hora local), so para a mensagem de erro."""
    return datetime.datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")


def artefato_esta_atual(nome_mod, p, config=CONFIG_PADRAO):
    """TODAS as DLLs do pacote correspondem a fonte que esta no repositorio?

    Levanta `Falha` quando uma DLL e' MAIS ANTIGA que o arquivo de fonte mais novo que
    entra na compilacao DELA - a fonte mudou depois do ultimo build, e o pacote sairia
    com um binario que nao tem a edicao. No layout padrao ha uma DLL so; no pacote
    nao-raiz (PKG-API-1) ha uma por projeto, e cada uma e' conferida contra a fonte do
    projeto DELA (`fontes_por_dll`).

    Devolve a lista `(mtime_dll, fonte_mais_nova)` por DLL quando tudo bate.
    """
    conferidas = []
    for dll in p["dlls"]:
        mtime_dll = os.path.getmtime(dll)
        fontes = []
        for pasta in p["fontes_por_dll"][dll]:
            fontes.extend(fontes_do_mod(pasta))
        if not fontes:
            conferidas.append((mtime_dll, None))
            continue

        mais_nova = max(fontes, key=os.path.getmtime)
        mtime_fonte = os.path.getmtime(mais_nova)
        if mtime_dll < mtime_fonte:
            raise Falha(
                "ARTEFATO VELHO (REL-1): a DLL de bin/%s/ e MAIS ANTIGA que a fonte\n"
                "      DLL   : %s  (%s)\n"
                "      FONTE : %s  (%s)\n"
                "      -> o pacote sairia com um binario SEM a edicao acima. Reconstrua a\n"
                "         partir da FONTE. NUNCA sem a flag: o alvo DeployToBepInEx do .csproj\n"
                "         copia a DLL para o perfil do r2modman e o jogo passa a rodar o build.\n"
                "         dotnet build %s -c %s -p:DeployToBepInEx=false"
                % (config,
                   os.path.relpath(dll, RAIZ), quando(mtime_dll),
                   os.path.relpath(mais_nova, RAIZ), quando(mtime_fonte),
                   rel(p["csproj"]), config))
        conferidas.append((mtime_dll, mais_nova))
    return conferidas


def versao_do_plugin(nome_mod, p):
    """A versao que o BepInEx registra no log, lida dos arquivos de versao do pacote.

    Mesmo criterio de `tools/audita_docs.py` (o CI cobra esse formato): o literal pode
    estar no proprio atributo - `[BepInPlugin("guid", "nome", "0.1.0")]` - ou numa
    constante usada como ultimo argumento - `[BepInPlugin(Guid, "nome", Version)]` com
    `public const string Version = "0.1.0";` (padrao do RoguelikeSkillTreeVisualizer e,
    tambem, do RealmApi - onde o atributo esta em `api/Plugin/RealmApiPlugin.cs` e a
    const `ApiIdentity.Version`, em `api/Core/Contracts.cs`; por isso a busca varre
    TODOS os arquivos de `versao_em`, nunca um so).

    Devolve `(versao, nome_da_constante, arquivo)`; `(None, None, None)` quando nao acha.
    O arquivo e' o que carrega o literal - e' nele que `--sincronizar-versao` escreve.
    """
    textos = []
    for caminho in p["versao_em"]:
        if os.path.isfile(caminho):
            with open(caminho, encoding="utf-8", errors="replace") as fh:
                textos.append((caminho, fh.read()))

    for caminho, fonte in textos:
        literal = re.search(r'Plugin\(\s*"([^"]+)"\s*,\s*"([^"]+)"\s*,\s*"([^"]+)"', fonte)
        if literal:
            return literal.group(3), None, caminho

    for _caminho, fonte in textos:
        atributo = re.search(r"\[BepInPlugin\(([^)]*)\)\]", fonte)
        if not atributo:
            continue
        ident = re.search(r",\s*([A-Za-z_][\w.]*)\s*$", atributo.group(1).strip())
        if not ident:
            continue
        nome = ident.group(1).split(".")[-1]
        for caminho_const, fonte_const in textos:
            const = re.search(r'const\s+string\s+%s\s*=\s*"([^"]+)"' % re.escape(nome),
                              fonte_const)
            if const:
                return const.group(1), nome, caminho_const
    return None, None, None


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
    no_plugin, const, _arquivo = versao_do_plugin(nome_mod, p)
    no_readme = versao_do_readme(p)
    if no_plugin is None:
        raise Falha("PKG-2: nao achei a versao em %s (esperava o literal no "
                    "[BepInPlugin(\"guid\", \"nome\", \"x.y.z\")] ou uma const Version)"
                    % ", ".join(rel(c) for c in p["versao_em"]))
    if no_readme is None:
        raise Falha("PKG-3: nao achei a versao em %s/README.md (esperava a linha "
                    "\"- **Version:** x.y.z\", a que os READMEs ja usam)" % nome_mod)
    if no_manifest != fonte or no_plugin != fonte or no_readme != fonte:
        raise Falha(
            "PKG-2/PKG-3: VERSAO DIVERGE (o .csproj e a fonte)\n"
            "      %s/%s.csproj      <Version>%s</Version>  <- FONTE\n"
            "      %s/manifest.json  \"version_number\": \"%s\"%s\n"
            "      %s/Plugin.cs      %s \"%s\"%s\n"
            "      %s/README.md      - **Version:** %s%s\n"
            "      -> conserte o(s) DIVERGE, ou rode de uma vez:\n"
            "         python tools/pack-thunderstore.py --sincronizar-versao %s"
            % (nome_mod, nome_mod, fonte,
               nome_mod, no_manifest, "  <-- DIVERGE" if no_manifest != fonte else "",
               nome_mod, ("const %s =" % const) if const else "[BepInPlugin(...)]",
               no_plugin, "  <-- DIVERGE" if no_plugin != fonte else "",
               nome_mod, no_readme, "  <-- DIVERGE" if no_readme != fonte else "",
               nome_mod))
    return fonte


# ---------------------------------------------------------------------------
# PKG-2: sincronizar os espelhos a partir do .csproj (so o que divergir)
# ---------------------------------------------------------------------------

def sincronizar_versao(nome_mod):
    """Reescreve manifest.json, Plugin.cs e README.md com o `<Version>` do .csproj.

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
    versao_plugin, const, arquivo_plugin = versao_do_plugin(nome_mod, p)
    if arquivo_plugin and os.path.isfile(arquivo_plugin):
        if versao_plugin is not None and versao_plugin != fonte:
            with open(arquivo_plugin, encoding="utf-8", newline="") as fh:
                texto = fh.read()
            if const:
                padrao = re.compile(r'(const\s+string\s+%s\s*=\s*")([^"]*)(")'
                                    % re.escape(const))
            else:
                padrao = re.compile(r'(Plugin\(\s*"[^"]+"\s*,\s*"[^"]+"\s*,\s*")([^"]*)(")')
            novo = padrao.sub(lambda m: m.group(1) + fonte + m.group(3), texto, count=1)
            if novo != texto:
                with open(arquivo_plugin, "w", encoding="utf-8", newline="") as fh:
                    fh.write(novo)
                mudancas.append("%s: %s %s -> %s"
                                % (rel(arquivo_plugin),
                                   "const %s" % const if const else "[BepInPlugin]",
                                   versao_plugin, fonte))

    # --- README.md: troca SO o valor da linha `- **Version:**`, nada mais ---------
    # O dono edita os textos do README; a sync nao encosta em mais nada. newline=""
    # preserva o fim de linha - o arquivo fica byte-a-byte igual quando ja batia.
    if os.path.isfile(p["readme"]):
        with open(p["readme"], encoding="utf-8", newline="") as fh:
            texto = fh.read()
        achado = PADRAO_VERSAO_README.search(texto)
        if achado and achado.group(1) != fonte:
            novo = texto[:achado.start(1)] + fonte + texto[achado.end(1):]
            with open(p["readme"], "w", encoding="utf-8", newline="") as fh:
                fh.write(novo)
            mudancas.append("README.md: - **Version:** %s -> %s"
                            % (achado.group(1), fonte))
    return fonte, mudancas


def verificar(nome_mod, config=CONFIG_PADRAO, gerar_icone_se_faltar=False):
    """Pre-flight de UM pacote. Devolve (manifesto, dict de caminhos). Levanta Falha."""
    p = caminhos(nome_mod, config)

    if not os.path.isfile(p["csproj"]):
        raise Falha("nao e pacote: falta %s" % rel(p["csproj"]))

    # PKG-API-1: um pacote nao-raiz tem TRES DLLs; TODAS tem de existir (faltando uma,
    # o BepInEx nao resolve o plugin ao carregar - pacote incompleto e' pior que nenhum).
    faltando = [d for d in p["dlls"] if not os.path.isfile(d)]
    if faltando:
        raise Falha("DLL NAO BUILDADA: %s\n"
                    "      -> rode:  dotnet build %s -c %s -p:DeployToBepInEx=false"
                    % (", ".join(rel(d) for d in faltando), rel(p["csproj"]), config))

    # REL-1: existir nao basta - cada DLL tem de corresponder a fonte de AGORA.
    artefato_esta_atual(nome_mod, p, config)

    manifesto = ler_manifest(nome_mod, p)

    # PKG-2: fonte unica de versao - manifest e Plugin.cs tem que bater com o .csproj
    conferir_versoes(nome_mod, p, manifesto)

    for chave in ("readme", "changelog"):
        if not os.path.isfile(p[chave]):
            raise Falha("%s nao existe" % os.path.basename(p[chave]))

    # PKG-API-1: os arquivos a mais que o pacote leva na raiz do zip (hoje so' o
    # LICENSE do RealmApi). Sao obrigatorios: o pacote promete por contrato o que
    # `--listar-caminhos` declara em `dentro_do_zip`.
    for extra in p["extras"]:
        if not os.path.isfile(extra):
            raise Falha("%s nao existe (arquivo extra do pacote: %s)"
                        % (os.path.basename(extra), rel(extra)))

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
    """Monta o stage e zipa. Devolve (caminho do zip, lista de (nome_no_zip, bytes)).

    O formato e' o mesmo para os nove pacotes: metadados na RAIZ do zip e as DLLs em
    `plugins/<pasta>/`. O que o pacote nao-raiz acrescenta e' (a) mais de uma DLL na
    mesma pasta `plugins/` e (b) os arquivos de `extras` na raiz (o LICENSE do RealmApi).
    """
    pasta_pacote = "%s-%s" % (AUTOR, nome_mod)
    stage = os.path.join(STAGE_RAIZ, pasta_pacote)
    if os.path.isdir(stage):
        shutil.rmtree(stage)
    os.makedirs(os.path.join(stage, "plugins", p["pasta_no_zip"]))

    copiados = [("manifest.json", p["manifest"]),
                ("README.md", p["readme"]),
                ("CHANGELOG.md", p["changelog"]),
                ("icon.png", p["icon"])]
    for extra in p["extras"]:
        copiados.append((os.path.basename(extra), extra))
    for destino, origem in copiados:
        shutil.copy2(origem, os.path.join(stage, destino))
    for dll in p["dlls"]:
        shutil.copy2(dll, os.path.join(stage, "plugins", p["pasta_no_zip"],
                                       os.path.basename(dll)))

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


def mapa_de_caminhos(config=CONFIG_PADRAO):
    """O layout de CADA pacote, em JSON - fonte unica para os gates.

    O `publish.yml` (pre-flight e registro) precisa saber onde esta o `.csproj` e o
    `manifest.json` de cada alvo e o que tem de existir dentro do zip. Antes ele
    reescrevia `<Mod>/<Mod>.csproj` na mao - premissa de layout padrao que o pacote
    nao-raiz viola (PKG-API-1). Aqui ele le a resposta do mesmo detector que empacota:
    uma fonte so, nada de segunda lista que envelhece.
    """
    mapa = []
    for nome in descobrir_mods():
        p = caminhos(nome, config)
        dentro = ["manifest.json", "README.md", "CHANGELOG.md", "icon.png"]
        dentro += [os.path.basename(extra) for extra in p["extras"]]
        dentro += ["plugins/%s/%s" % (p["pasta_no_zip"], os.path.basename(dll))
                   for dll in p["dlls"]]
        mapa.append({
            "nome": nome,
            "nao_raiz": eh_pacote_nao_raiz(nome),
            "csproj": rel(p["csproj"]),
            "manifest": rel(p["manifest"]),
            "dlls": [rel(dll) for dll in p["dlls"]],
            "dentro_do_zip": dentro,
        })
    return mapa


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
    ap.add_argument("--listar-caminhos", action="store_true",
                    help="imprime, em JSON, o layout de cada pacote (csproj, manifest, "
                         "DLLs e o que tem de existir DENTRO do zip) - e' o que os "
                         "gates (publish.yml) consomem em vez de reescrever o caminho "
                         "do csproj na mao; respeita --config")
    ap.add_argument("--listar-nomes", action="store_true",
                    help="imprime SO os nomes dos mods (um por linha) - para consumir de "
                         "script (scripts/package.ps1); a descoberta de mod fica NUM lugar")
    ap.add_argument("--so-conferir", action="store_true",
                    help="roda o pre-flight inteiro (inclusive a trava REL-1, artefato x "
                         "fonte) de todos os mods e SAI, sem gerar zip nenhum - e a forma "
                         "de checar o build antes de empacotar sem escrever em dist/")
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

    if args.listar_caminhos:
        print(json.dumps(mapa_de_caminhos(args.config), ensure_ascii=False, indent=2))
        return 0

    if args.listar:
        print("Mods encontrados em %s:" % RAIZ)
        for m in todos:
            if eh_pacote_nao_raiz(m):
                continue
            print("  - %-18s (csproj com DeployToBepInEx)" % m)
        nao_raiz = [m for m in todos if eh_pacote_nao_raiz(m)]
        ignorados = projetos_ignorados()
        if ignorados:
            print("Ignorados (tem csproj mas nao sao mod - nao copiam para plugins/):")
            for m in ignorados:
                print("  - %s" % m)
        # PKG-API-1: os pacotes do layout nao-raiz saem DEPOIS dos dois blocos de sempre
        # para que a saida dos oito de raiz continue byte a byte igual (o diff da
        # entrega fica so' no que e' novo).
        if nao_raiz:
            print("Pacotes NAO-RAIZ (PKG-API-1: projeto aninhado, mais de uma DLL - "
                  "tabela PACOTES_NAO_RAIZ), nao listados acima:")
            for m in nao_raiz:
                p = caminhos(m)
                print("  - %-18s %s  (%d DLL(s) -> plugins/%s/)"
                      % (m, rel(p["csproj"]), len(p["dlls"]), p["pasta_no_zip"]))
        return 0

    alvos = args.mods or todos
    desconhecidos = [m for m in alvos if m not in todos]
    if desconhecidos:
        print("!! nao existe mod com esse nome: %s" % ", ".join(desconhecidos))
        print("   mods disponiveis: %s" % ", ".join(todos))
        return 2

    # REL-1: o pre-flight tem de poder ser rodado SEM empacotar - e o que permite checar
    # o build (DLL x fonte) antes de escrever qualquer coisa em dist/.
    if args.so_conferir:
        print("Repo : %s" % RAIZ)
        print("Build: %s  (a DLL vem de <Mod>/bin/%s/%s/)" % (args.config, args.config, TFM))
        print("Modo : --so-conferir  (pre-flight inteiro, NADA e empacotado)")
        print()
        print("== conferindo (artefato x fonte, build %s, versao unica, manifest, icon) =="
              % args.config)
        problemas = 0
        for mod in alvos:
            try:
                manifesto, p = verificar(mod, args.config, args.gerar_icones)
                print("  ok    %-18s v%s  | %s"
                      % (mod, manifesto["version_number"],
                         os.path.relpath(p["dll"], RAIZ)))
            except Falha as erro:
                problemas += 1
                print("  FALHA %-18s %s" % (mod, erro))
        print()
        if problemas:
            print(">>> %d mod(s) REPROVADO(S) no pre-flight: empacotar estaria entregando "
                  "artefato que nao corresponde a fonte." % problemas)
            return 1
        print("Pre-flight verde para %d mod(s). Nada foi empacotado (--so-conferir)."
              % len(alvos))
        return 0

    # PKG-2/PKG-3: so conserta os espelhos da versao e sai (nao empacota nada).
    if args.sincronizar_versao:
        print("== PKG-2/PKG-3: sincronizando a versao a partir do <Version> do .csproj ==")
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
                print("  ok    %-18s v%s (manifest, Plugin.cs e README ja batiam)"
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
