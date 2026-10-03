#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PKG-4: a REGRA da versao unica (os 4 lugares) presa por teste PURO.

O QUE ESTE TESTE GARANTE
------------------------
A versao de um mod vive em QUATRO arquivos, e so o `<Version>` do `.csproj` manda:

    <Mod>/<Mod>.csproj   <Version>x.y.z</Version>   <- FONTE
    <Mod>/manifest.json  "version_number": "x.y.z"  <- espelho (Thunderstore)
    <Mod>/Plugin.cs      [BepInPlugin(..., "x.y.z")]<- espelho (BepInEx, o log)
    <Mod>/README.md      - **Version:** x.y.z       <- espelho (PKG-3: o usuario le)

O teste amarra quatro coisas, usando o MESMO parser que o gate de release usa:

  1. O PARSER le a linha `- **Version:** x.y.z` do README - e SO ela. Nao casa linha
     indentada, rotulo variante (`**Version :**`), rotulo sem espaco, nem lixo depois do
     valor. Enfraquecer o padrao deixaria o README envelhecer em silencio de novo.
  2. O REPO VIVO obedece a regra: nos 6 mods, csproj = manifest = Plugin.cs = README.
     Uma divergencia commitada derruba ESTE teste (nao so o `check_versoes.py`).
  3. Uma divergencia PLANTADA num repo sintetico e DETECTADA por
     `tools/check_versoes.py` do repositorio com exit 1 (para cada espelho), e a linha
     AUSENTE do README com exit 2. Corrigida a divergencia, o mesmo comando da exit 0.
  4. O SINCRONIZAR (`pack-thunderstore.sincronizar_versao`) reescreve SO o valor do
     espelho: prefixo, sufixo, fim de linha e o resto do arquivo ficam byte a byte
     iguais - e a segunda chamada nao muda UM byte (idempotente).

POR QUE ELE EXISTE (residual PKG-3)
-----------------------------------
A prova do bump e da reprovacao da trava de versao ficou num script GITIGNORED
(`scratch/pk3/`). A regra "versao em 4 lugares, espelhos nao divergem" nao tinha teste
na suite versionada: a unica garantia era o `check_versoes.py`, que nao era exercitado
por teste puro. Este teste fecha essa lacuna.

LEITURA (read-only): `pack-thunderstore.py` e `check_versoes.py` DO REPOSITORIO - o
mesmo modulo que o empacotador e o gate carregam (`check_versoes.carregar_empacotador`).
Nenhum arquivo do repositorio e escrito: o repo sintetico nasce em `scratch`/temp.
"""
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

import arcabouco as arc

META = {
    "nome": "pkg4-versao-4-lugares",
    "categoria": "pura",
    "requer": [],
    "descricao": ("o parser le a linha '- **Version:** x.y.z' do README (e so ela), o repo "
                  "vivo bate nos 4 lugares, a divergencia plantada da exit 1 no "
                  "check_versoes.py e o sincronizar reescreve SO o valor (idempotente)"),
}

EXIT_DIVERGE, EXIT_FALTA, EXIT_OK = 1, 2, 0


# ------------------------------- carregar o modulo real ----------------------

def _carrega_do_repo(nome_arquivo, nome_modulo):
    """Importa um modulo de `tools/` pelo caminho (read-only; nada executa no import)."""
    caminho = os.path.join(arc.raiz_do_repo(), "tools", nome_arquivo)
    arc.exigir(os.path.isfile(caminho), "nao achei %s no repo" % caminho)
    spec = importlib.util.spec_from_file_location(nome_modulo, caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


# ------------------------------- 1. o parser do README -----------------------

# (texto do README, versao esperada | None se NAO pode casar). O padrao e o dos SEIS
# READMEs reais (`- **Version:** x.y.z`), ancorado no comeco da linha - nao um formato novo.
CASOS_PARSER = (
    ("- **Version:** 1.2.3", "1.2.3"),
    ("# Mod\n\ntexto\n\n- **Version:** 1.2.3\n\ncorpo\n", "1.2.3"),
    ("- **Version:** 1.2.3   ", "1.2.3"),          # espaco no fim: ok, ancora \s*$
    ("  - **Version:** 1.2.3", None),              # INDENTADO nao e a linha ancora
    ("- **Version :** 1.2.3", None),               # rotulo variante (espaco antes do ':')
    ("- **Version:**1.2.3", None),                 # sem o espaco depois do rotulo
    ("- **Version:** 1.2.3 extra", None),          # lixo depois do valor
    ("prosa: - **Version:** 9.9.9", None),         # a linha existe, mas NAO no comeco
    ("nao tem a linha de versao", None),
)


def _parser(raiz_tmp):
    """Exercita `versao_do_readme` caso a caso, em arquivos temporarios."""
    # Carrega pelo arc (o PYTHONPATH do subprocesso do runner nao traz tools/):
    pt = _carrega_do_repo("pack-thunderstore.py", "pack_thunderstore_pkg4_parser")
    alvo = os.path.join(raiz_tmp, "parser")
    os.makedirs(alvo)
    for i, (texto, esperado) in enumerate(CASOS_PARSER):
        caminho = os.path.join(alvo, "caso%02d.md" % i)
        with open(caminho, "w", encoding="utf-8", newline="") as fh:
            fh.write(texto)
        obtido = pt.versao_do_readme({"readme": caminho})
        arc.igual(obtido, esperado,
                  "parser do README, caso %r: esperado %r, obtido %r" % (texto, esperado, obtido))
    return pt


# ------------------------------- 2. o repo vivo ------------------------------

def _confere_repo_vivo(cv, pt):
    """Nos mods REAIS, os quatro lugares tem de bater (a regra commitada)."""
    mods = sorted(pt.descobrir_mods())
    arc.exigir(mods, "descobrir_mods() nao achou mod nenhum no repo vivo")
    para_relato = []
    for nome in mods:
        p = pt.caminhos(nome)
        fonte = pt.versao_do_csproj(p)
        arc.exigir(fonte and pt.SEMVER.match(fonte),
                   "%s: <Version> do .csproj ausente/nao-semver: %r" % (nome, fonte))
        no_manifest = cv.versao_do_manifest(p["manifest"])
        no_plugin, _const = pt.versao_do_plugin(nome, p)
        no_readme = pt.versao_do_readme(p)
        for rotulo, valor in (("manifest.json", no_manifest),
                              ("Plugin.cs", no_plugin),
                              ("README.md", no_readme)):
            arc.igual(valor, fonte,
                      "%s: %s diverge da fonte (csproj=%s) - a versao vive em 4 lugares"
                      % (nome, rotulo, fonte))
        para_relato.append("%s=%s" % (nome, fonte))
    print("repo vivo: %d mods, 4 lugares batem (%s)" % (len(mods), ", ".join(para_relato)))


# ------------------------------- 3. repo sintetico ---------------------------

def _csproj(nome, versao):
    # Tem de conter DeployToBepInEx e plugins: e o que `pack.eh_mod` exige para achar o mod.
    return (
        '<Project Sdk="Microsoft.NET.Sdk">\n'
        '  <PropertyGroup>\n'
        '    <Version>%s</Version>\n'
        '  </PropertyGroup>\n'
        '  <Target Name="DeployToBepInEx" AfterTargets="Build">\n'
        '    <Copy SourceFiles="x.dll" DestinationFolder="plugins\\%s" />\n'
        '  </Target>\n'
        '</Project>\n' % (versao, nome))


def _manifest(nome, versao):
    return json.dumps({
        "name": nome, "version_number": versao,
        "website_url": "https://example.invalid", "description": "fixture de teste",
        "dependencies": [], "extra": {},
    }, ensure_ascii=False, indent=2) + "\n"


def _plugin(nome, versao, const=False):
    if const:
        return ('using BepInEx;\n\n[BepInPlugin("com.gumatos.%s", "%s", Version)]\n'
                'public class Plugin : BaseUnityPlugin {\n'
                '    public const string Version = "%s";\n}\n'
                % (nome.lower(), nome, versao))
    return ('using BepInEx;\n\n[BepInPlugin("com.gumatos.%s", "%s", "%s")]\n'
            'public class Plugin : BaseUnityPlugin { }\n' % (nome.lower(), nome, versao))


def _readme(versao, com_linha=True):
    """README com a linha ancora, prosa e uma ISCA.

    A isca ("Linha com - **Version:** 9.9.9 no meio") tem o rotulo FORA do comeco da
    linha: o padrao ancorado nao pode casar nela. A prosa cita a versao antiga de
    proposito - o sincronizar so pode tocar a linha ancora, nunca a prosa.
    """
    linha = ("- **Version:** %s" % versao) if com_linha else "## sem a linha de versao"
    # CRLF de proposito: o sincronizar tem de preservar o fim de linha (nao reformatar).
    texto = (
        "# DemoMod\r\n"
        "\r\n"
        "Introducao com acentos: coracao, versao, acao.\r\n"
        "\r\n"
        "%s\r\n"
        "- **Autor:** Gumatos\r\n"
        "\r\n"
        "Prosa do usuario citando %s de proposito: a sync NAO pode tocar aqui.\r\n"
        "Linha com - **Version:** 9.9.9 no meio (nao e a linha ancora).\r\n"
        % (linha, versao)
    )
    return texto


def _monta_repo_sintetico(destino, csproj_ver="2.0.0", manifest_ver="2.0.0",
                          plugin_ver="2.0.0", readme_ver="2.0.0", readme_linha=True,
                          plugin_const=False):
    """Cria um repo minimo no formato que `check_versoes.py`/`pack` descobrem."""
    os.makedirs(os.path.join(destino, "tools"))
    for arquivo in ("check_versoes.py", "pack-thunderstore.py"):
        shutil.copy2(os.path.join(arc.raiz_do_repo(), "tools", arquivo),
                     os.path.join(destino, "tools", arquivo))
    mod = os.path.join(destino, "DemoMod")
    os.makedirs(mod)
    _escreve(os.path.join(mod, "DemoMod.csproj"), _csproj("DemoMod", csproj_ver))
    _escreve(os.path.join(mod, "manifest.json"), _manifest("DemoMod", manifest_ver))
    _escreve(os.path.join(mod, "Plugin.cs"), _plugin("DemoMod", plugin_ver, plugin_const))
    _escreve(os.path.join(mod, "README.md"), _readme(readme_ver, readme_linha))
    return destino


def _escreve(caminho, texto):
    with open(caminho, "w", encoding="utf-8", newline="") as fh:
        fh.write(texto)


def _le(caminho):
    with open(caminho, encoding="utf-8", newline="") as fh:
        return fh.read()


def _roda_check_versoes(raiz):
    """Roda o `check_versoes.py` do REPOSITORIO (copiado) contra o repo sintetico."""
    caminho = os.path.join(raiz, "tools", "check_versoes.py")
    proc = subprocess.run([sys.executable, caminho], cwd=raiz,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          universal_newlines=True, timeout=120)
    return proc.returncode, proc.stdout or ""


def _divergencia(cv, pt, raiz_tmp, que):
    """Planta a divergencia em UM espelho e exige exit 1 nomeando o arquivo."""
    destino = os.path.join(raiz_tmp, "div-" + que)
    _escreve_kwargs = {"readme_ver": "2.0.0", "manifest_ver": "2.0.0", "plugin_ver": "2.0.0"}
    # a FONTE e 2.0.0; o espelho escolhido desce para 1.0.0.
    _escreve_kwargs[{"readme": "readme_ver", "manifest": "manifest_ver",
                     "plugin": "plugin_ver"}[que]] = "1.0.0"
    _monta_repo_sintetico(destino, **_escreve_kwargs)
    codigo, saida = _roda_check_versoes(destino)
    arc.igual(codigo, EXIT_DIVERGE,
              "divergencia em %s: check_versoes.py tinha de dar exit 1, deu %r" % (que, codigo))
    rotulo = {"readme": "README.md", "manifest": "manifest.json", "plugin": "Plugin.cs"}[que]
    arc.exigir("DIVERGE" in saida and rotulo in saida,
               "divergencia em %s: a saida nao marca DIVERGE em %s:\n%s" % (que, rotulo, saida))
    return destino


# ------------------------------- 4. o sincronizar ----------------------------

def _span(padrao, texto, grupo=1, o_que=""):
    achado = padrao.search(texto)
    arc.exigir(achado, "o padrao da sync nao casou (%s)" % o_que)
    return achado.start(grupo), achado.end(grupo)


def _confere_sincronizar(pt, raiz_tmp):
    """O sincronizar reescreve SO o valor: resto do valor, do arquivo e do EOL intactos."""
    destino = os.path.join(raiz_tmp, "sync")
    # FONTE 2.0.0; os TRES espelhos em 1.0.0 (todos divergem).
    _monta_repo_sintetico(destino, csproj_ver="2.0.0", manifest_ver="1.0.0",
                          plugin_ver="1.0.0", readme_ver="1.0.0")

    p = {"readme": os.path.join(destino, "DemoMod", "README.md"),
         "manifest": os.path.join(destino, "DemoMod", "manifest.json"),
         "plugin": os.path.join(destino, "DemoMod", "Plugin.cs")}
    antes = {chave: _le(caminho) for chave, caminho in p.items()}

    # O modulo real, apontado para o repo sintetico (RAIZ e o unico ponto de config).
    pt.RAIZ = destino
    fonte, mudancas = pt.sincronizar_versao("DemoMod")
    arc.igual(fonte, "2.0.0", "a fonte (csproj) lida pela sync")
    arc.igual(len(mudancas), 3, "a sync tinha de corrigir os 3 espelhos, mudou: %s" % mudancas)
    para_relato = "; ".join(mudancas)

    # --- README: SO o grupo da versao muda; prefixo/sufixo/EOL identicos -----------
    texto = antes["readme"]
    s, e = _span(pt.PADRAO_VERSAO_README, texto, 1, "README")
    arc.igual(texto[s:e], "1.0.0", "a sync tinha de achar 1.0.0 na linha do README")
    esperado = texto[:s] + "2.0.0" + texto[e:]
    obtido = _le(p["readme"])
    arc.igual(obtido, esperado,
              "README: a sync mudou mais que o valor da linha '- **Version:**'")
    arc.exigir(obtido != texto, "README: a sync nao mudou nada (deveria)")
    arc.exigir("\r\n" in obtido,
               "README: a sync reformatou o fim de linha (CRLF virou LF)")
    arc.exigir("Linha com - **Version:** 9.9.9" in obtido and
               "Prosa do usuario citando 1.0.0" in obtido,
               "README: a sync tocou a prosa/isca fora da linha ancora")

    # --- manifest.json: SO o valor de version_number -------------------------------
    texto = antes["manifest"]
    padrao = re.compile(r'("version_number"\s*:\s*")([^"]*)(")')
    s, e = _span(padrao, texto, 2, "manifest")
    arc.igual(texto[s:e], "1.0.0", "a sync tinha de achar 1.0.0 no manifest")
    arc.igual(_le(p["manifest"]), texto[:s] + "2.0.0" + texto[e:],
              "manifest.json: a sync mudou mais que o valor de version_number")

    # --- Plugin.cs: SO o literal da versao (atributo) ------------------------------
    texto = antes["plugin"]
    padrao = re.compile(r'(Plugin\(\s*"[^"]+"\s*,\s*"[^"]+"\s*,\s*")([^"]*)(")')
    s, e = _span(padrao, texto, 2, "plugin")
    arc.igual(texto[s:e], "1.0.0", "a sync tinha de achar 1.0.0 no Plugin.cs")
    arc.igual(_le(p["plugin"]), texto[:s] + "2.0.0" + texto[e:],
              "Plugin.cs: a sync mudou mais que o literal da versao")

    # --- idempotencia: a segunda chamada nao muda UM byte --------------------------
    depois = {chave: _le(caminho) for chave, caminho in p.items()}
    _fonte2, mudancas2 = pt.sincronizar_versao("DemoMod")
    arc.igual(mudancas2, [], "a 2a sync tinha de nao ter o que mudar, mudou: %s" % mudancas2)
    for chave, caminho in p.items():
        arc.igual(_le(caminho), depois[chave],
                  "a 2a sync mexeu em %s (nao e idempotente)" % chave)

    # --- o repositorio sincronizado passa a dar exit 0 no gate ---------------------
    codigo, saida = _roda_check_versoes(destino)
    arc.igual(codigo, EXIT_OK,
              "o repo sincronizado tinha de dar exit 0, deu %r:\n%s" % (codigo, saida))

    # --- variante da CONST (o outro formato real do Plugin.cs) ---------------------
    destino_const = os.path.join(raiz_tmp, "sync-const")
    _monta_repo_sintetico(destino_const, csproj_ver="3.1.4", manifest_ver="1.0.0",
                          plugin_ver="1.0.0", readme_ver="1.0.0", plugin_const=True)
    pt.RAIZ = destino_const
    fonte_c, mud_c = pt.sincronizar_versao("DemoMod")
    arc.igual(fonte_c, "3.1.4", "a fonte da variante const")
    texto = _le(os.path.join(destino_const, "DemoMod", "Plugin.cs"))
    arc.exigir('const string Version = "3.1.4"' in texto,
               "a sync nao atualizou a const Version: %r" % texto)
    arc.exigir('"1.0.0"' not in texto, "sobrou o 1.0.0 no Plugin.cs da variante const")
    codigo, saida = _roda_check_versoes(destino_const)
    arc.igual(codigo, EXIT_OK,
              "a variante const sincronizada tinha de dar exit 0, deu %r:\n%s" % (codigo, saida))
    para_relato += " | const: " + "; ".join(mud_c)

    print("sincronizar: %s; idempotente; repositorio sincronizado da exit 0" % para_relato)


# ------------------------------- corpo ---------------------------------------

def corpo():
    raiz_tmp = tempfile.mkdtemp(prefix="sr-pkg4-")
    try:
        cv = _carrega_do_repo("check_versoes.py", "check_versoes_pkg4")

        # 1. o parser: le a linha e SO ela (recusa o que nao e o formato dos READMEs reais)
        pt = _parser(raiz_tmp)
        print("parser: %d casos (ancora exata; indentado/rotulo variante/lixo -> None)"
              % len(CASOS_PARSER))

        # 2. o repo vivo bate nos quatro lugares
        _confere_repo_vivo(cv, pt)

        # 3. divergencia plantada -> exit 1 (um espelho por vez); linha ausente -> exit 2
        for que in ("readme", "manifest", "plugin"):
            _divergencia(cv, pt, raiz_tmp, que)
        destino = os.path.join(raiz_tmp, "sem-linha")
        _monta_repo_sintetico(destino, csproj_ver="2.0.0", manifest_ver="2.0.0",
                              plugin_ver="2.0.0", readme_ver="2.0.0", readme_linha=False)
        codigo, saida = _roda_check_versoes(destino)
        arc.igual(codigo, EXIT_FALTA,
                  "README sem a linha de versao: tinha de dar exit 2, deu %r" % codigo)
        arc.exigir("sem versao" in saida,
                   "README sem a linha: a saida nao nomeia o que falta:\n%s" % saida)
        print("divergencia plantada: readme/manifest/plugin -> exit 1; linha ausente -> exit 2")

        # 4. o sincronizar reescreve SO o valor, e e idempotente
        _confere_sincronizar(pt, raiz_tmp)
    finally:
        shutil.rmtree(raiz_tmp, ignore_errors=True)


if __name__ == "__main__":
    arc.main(META, corpo)
