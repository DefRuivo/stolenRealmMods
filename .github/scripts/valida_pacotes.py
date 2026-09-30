#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""valida_pacotes.py - confere os METADADOS de cada pacote Thunderstore do repo.

POR QUE EXISTE (CI-2)
---------------------
O repo e publico e a automacao aprovada e de ESCOPO A: SO VALIDACAO. Este script e o
passo 7 do `.github/workflows/validate.yml` (virou 7 quando as versoes entraram como
passo 2 - ver `tools/check_versoes.py`, que e quem confere se o `version_number` e o
MESMO `<Version>` do .csproj e a versao do `Plugin.cs`; aqui se confere so o semver). Ele NAO compila, NAO empacota e NAO publica
nada - so le o que ja esta versionado e diz se o pacote passaria no Thunderstore.

Por que nao reaproveitar `tools/pack-thunderstore.py`: aquele script exige a DLL buildada
(`bin/Release/netstandard2.1/*.dll`), e a DLL depende das assemblies do JOGO que ficam em
`lib/` (gitignored). No CI nao ha jogo nem `lib/`, entao aquele caminho nao roda. Aqui a
mesma regra e aplicada apenas sobre metadados versionados, sem tocar em `tools/`.

REGRAS (as mesmas que o Thunderstore exige e o pack ja checava)
---------------------------------------------------------------
  1. manifest.json existe e e JSON valido, com os campos obrigatorios;
  2. `name` alfanumerico ([A-Za-z0-9_]+) e IGUAL ao nome da pasta do mod
     (se divergirem, o r2modman instala num caminho diferente do que o README promete);
  3. `version_number` em semver `X.Y.Z` (se ele e o MESMO do .csproj/Plugin.cs NAO e
     daqui: e do `tools/check_versoes.py`, passo 2 do workflow);
  4. `description` nao vazia e <= 250 caracteres (limite do Thunderstore);
  5. `dependencies`: o BepInExPack da comunidade vem SEMPRE em primeiro (unica dependencia
     obrigatoria); cada dependencia extra tem de estar no formato `Autor-Pacote-Versao` e,
     se for de um mod DESTE repositorio, apontar para a versao que ele declara HOJE -
     versao antiga faz o gerenciador resolver o MESMO pacote em duas versoes (duas DLLs
     com o mesmo GUID carregadas juntas, que e o defeito que essa amarra evita); sem
     dependencia repetida de pacote;
  6. `icon.png` e um PNG real de 256x256 e <= 1 MB;
  7. `README.md` e `CHANGELOG.md` presentes na raiz do mod.

Uma pasta que NAO tem manifest.json e apenas AVISADA, nao reprovada: e o caso de um mod
ainda em implementacao (o RoguelikeSkillTreeVisualizer hoje). Sem manifest ele nem e
pacote, nao ha o que validar - mas o aviso fica no log para nao passar em branco.

USO:  python .github/scripts/valida_pacotes.py
      exit 0 = todos os pacotes ok;  1 = algum problema (a saida diz qual).
"""
import io
import json
import os
import re
import struct
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CAMPOS_OBRIGATORIOS = ("name", "version_number", "website_url", "description",
                       "dependencies")
NOME_VALIDO = re.compile(r"^[A-Za-z0-9_]+$")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
DESC_MAX = 250
DEPENDENCIA_OBRIGATORIA = "BepInEx-BepInExPack-5.4.2305"
ICONE_MAX_BYTES = 1024 * 1024            # 1 MB
ICONE_LADO = 256

# Pastas que nunca sao mod (evita varrer lixo e acusar falso positivo).
IGNORAR = {"docs", "dist", "lib", "scratch", "tools", ".git", ".github",
           "ReloadProbe", "__pycache__"}


def png_tamanho(caminho):
    """(largura, altura) lidos do IHDR. None se o arquivo nao for um PNG."""
    try:
        with open(caminho, "rb") as fh:
            cabecalho = fh.read(24)
    except OSError:
        return None
    if len(cabecalho) < 24 or cabecalho[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    if cabecalho[12:16] != b"IHDR":
        return None
    return struct.unpack(">II", cabecalho[16:24])


def pastas_com_manifest():
    """(com_manifest, sem_manifest) - nomes de pasta de mod encontrados na raiz."""
    com, sem = [], []
    for nome in sorted(os.listdir(RAIZ)):
        pasta = os.path.join(RAIZ, nome)
        if not os.path.isdir(pasta) or nome.startswith(".") or nome in IGNORAR:
            continue
        # uma pasta e candidata a mod se tem csproj, manifest.json, icon.png ou Plugin.cs
        marcas = ("%s.csproj" % nome, "manifest.json", "icon.png", "Plugin.cs")
        if not any(os.path.isfile(os.path.join(pasta, m)) for m in marcas):
            continue
        (com if os.path.isfile(os.path.join(pasta, "manifest.json")) else sem).append(nome)
    return com, sem


def versoes_do_repo():
    """({mod: versao}, team) - o que o repositorio declara hoje, para a regra 5.

    A versao de cada mod sai do proprio `manifest.json` (a trava que compara manifest,
    csproj e Plugin.cs e o `tools/check_versoes.py`); o team sai do `release/mods.json`,
    que e onde a decisao de namespace humano esta registrada.
    """
    versoes = {}
    com_manifest, _ = pastas_com_manifest()
    for nome in com_manifest:
        try:
            manifesto = json.loads(io.open(os.path.join(RAIZ, nome, "manifest.json"),
                                           encoding="utf-8").read())
        except (OSError, ValueError):
            continue
        versoes[nome] = manifesto.get("version_number")
    team = None
    try:
        config = json.loads(io.open(os.path.join(RAIZ, "release", "mods.json"),
                                    encoding="utf-8").read())
        team = config.get("team")
    except (OSError, ValueError):
        pass
    return versoes, team


def partes_da_referencia(ref):
    """(namespace, nome, versao) de `Autor-Pacote-Versao`, ou (None, None, None).

    Leitura de tras para frente, a mesma do `PackageReference.parse` do Thunderstore: o
    NAMESPACE pode conter '-', nome e versao nao.
    """
    if not isinstance(ref, str):
        return None, None, None
    partes = ref.split("-")
    if len(partes) < 3:
        return None, None, None
    versao, nome = partes[-1], partes[-2]
    namespace = "-".join(partes[:-2])
    if not namespace or not SEMVER.match(versao) or not NOME_VALIDO.match(nome):
        return None, None, None
    if any(not NOME_VALIDO.match(componente) for componente in namespace.split("-")):
        return None, None, None
    return namespace, nome, versao


VERSOES_DO_REPO, TEAM_DO_REPO = versoes_do_repo()


def valida(nome):
    """Roda as regras de UM mod. Devolve (lista de erros, dicionario de dados lidos)."""
    pasta = os.path.join(RAIZ, nome)
    erros = []
    dados = {}
    caminho_manifest = os.path.join(pasta, "manifest.json")

    try:
        manifesto = json.loads(io.open(caminho_manifest, encoding="utf-8").read())
    except ValueError as erro:
        return ["manifest.json nao e JSON valido: %s" % erro], dados
    if not isinstance(manifesto, dict):
        return ["manifest.json nao e um objeto JSON"], dados

    faltando = [c for c in CAMPOS_OBRIGATORIOS if c not in manifesto]
    if faltando:
        erros.append("manifest.json sem campo(s) obrigatorio(s): %s" % ", ".join(faltando))
    dados["versao"] = manifesto.get("version_number")

    # 2. nome alfanumerico e igual a pasta
    nome_manifesto = manifesto.get("name")
    if not isinstance(nome_manifesto, str) or not nome_manifesto:
        erros.append("'name' ausente ou nao e texto")
    else:
        if not NOME_VALIDO.match(nome_manifesto):
            erros.append("'name' '%s' nao e alfanumerico (use so A-Z a-z 0-9 _)"
                         % nome_manifesto)
        if nome_manifesto != nome:
            erros.append("'name' '%s' != pasta do mod '%s' (o r2modman instalaria "
                         "noutro caminho do que o README promete)" % (nome_manifesto, nome))

    # 3. semver
    versao = manifesto.get("version_number")
    if not isinstance(versao, str) or not SEMVER.match(versao):
        erros.append("'version_number' %r nao esta em semver X.Y.Z (ex.: 0.1.0)" % (versao,))

    # 4. descricao
    descricao = manifesto.get("description")
    if not isinstance(descricao, str) or not descricao.strip():
        erros.append("'description' vazia ou nao e texto")
    elif len(descricao) > DESC_MAX:
        erros.append("'description' tem %d caracteres (limite do Thunderstore: %d)"
                     % (len(descricao), DESC_MAX))
    else:
        dados["desc_len"] = len(descricao)

    # 5. dependencias: BepInExPack primeiro, referencia bem formada e - para mod deste
    #    repositorio - a versao que ele declara HOJE (versao antiga = duas copias)
    deps = manifesto.get("dependencies")
    if not isinstance(deps, list) or not deps:
        erros.append("'dependencies' tem que ser uma lista nao vazia "
                     "(o BepInExPack e obrigatorio)")
    else:
        if deps[0] != DEPENDENCIA_OBRIGATORIA:
            erros.append("a PRIMEIRA dependencia tem que ser '%s' (achei %r)"
                         % (DEPENDENCIA_OBRIGATORIA, deps[0]))
        if deps.count(DEPENDENCIA_OBRIGATORIA) > 1:
            erros.append("'%s' repetido na lista" % DEPENDENCIA_OBRIGATORIA)
        vistos = {}
        for ref in deps:
            namespace, nome_dep, versao_dep = partes_da_referencia(ref)
            if namespace is None:
                erros.append("dependencia %r nao esta no formato Autor-Pacote-Versao" % (ref,))
                continue
            pacote = "%s-%s" % (namespace, nome_dep)
            if pacote in vistos:
                erros.append("dependencia repetida do MESMO pacote: %r e %r"
                             % (vistos[pacote], ref))
            vistos[pacote] = ref
            if nome_dep in VERSOES_DO_REPO:
                if versao_dep != VERSOES_DO_REPO[nome_dep]:
                    erros.append("dependencia %r aponta a versao %s, mas %s declara hoje %s "
                                 "(versao antiga = o mesmo pacote instalado duas vezes)"
                                 % (ref, versao_dep, nome_dep,
                                    VERSOES_DO_REPO[nome_dep]))
                if TEAM_DO_REPO and namespace != TEAM_DO_REPO:
                    erros.append("dependencia %r usa o namespace %r, mas o team deste repo "
                                 "e %r" % (ref, namespace, TEAM_DO_REPO))
        dados["deps"] = len(deps)

    # 6. icon.png 256x256 e <= 1 MB
    caminho_icone = os.path.join(pasta, "icon.png")
    if not os.path.isfile(caminho_icone):
        erros.append("icon.png nao existe (o Thunderstore exige 256x256)")
    else:
        tamanho = os.path.getsize(caminho_icone)
        medidas = png_tamanho(caminho_icone)
        dados["icone"] = "%sx%s, %d bytes" % (medidas[0] if medidas else "?",
                                              medidas[1] if medidas else "?",
                                              tamanho) if medidas else "PNG invalido"
        if medidas is None:
            erros.append("icon.png nao e um PNG valido")
        elif medidas != (ICONE_LADO, ICONE_LADO):
            erros.append("icon.png tem %dx%d (o Thunderstore exige %dx%d)"
                         % (medidas[0], medidas[1], ICONE_LADO, ICONE_LADO))
        if tamanho > ICONE_MAX_BYTES:
            erros.append("icon.png tem %d bytes (limite: %d = 1 MB)"
                         % (tamanho, ICONE_MAX_BYTES))

    # 7. README/CHANGELOG
    for arq in ("README.md", "CHANGELOG.md"):
        if not os.path.isfile(os.path.join(pasta, arq)):
            erros.append("%s nao existe na raiz do mod" % arq)

    return erros, dados


def main():
    com, sem = pastas_com_manifest()
    print("valida_pacotes - metadados dos pacotes Thunderstore (nao compila nada)")
    print("pasta do repo: %s" % RAIZ)
    print()
    if not com:
        print("!! nenhuma pasta de mod com manifest.json encontrada")
        return 1

    problemas = 0
    for nome in com:
        erros, dados = valida(nome)
        if erros:
            problemas += len(erros)
            print("FALHA %-32s %s" % (nome, dados.get("versao") or ""))
            for e in erros:
                print("        - %s" % e)
        else:
            print("ok    %-32s %-8s desc=%-4s icone=%s"
                  % (nome, dados.get("versao", "?"), dados.get("desc_len", "?"),
                     dados.get("icone", "?")))

    if sem:
        print()
        print("aviso: pasta(s) de mod SEM manifest.json (nao validadas, nao e pacote ainda):")
        for nome in sem:
            print("        - %s" % nome)

    print()
    print("pacotes validados: %d | com problema: %d" % (len(com), problemas))
    if problemas:
        print("==> corrigir os itens acima antes de publicar")
        return 1
    print("  ==> todos os pacotes ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
