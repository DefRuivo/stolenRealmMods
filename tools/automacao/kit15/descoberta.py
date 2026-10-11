#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""descoberta.py - KIT-15: descoberta/selecao de caminhos SEM usuario fixo.

Regra de ouro: nenhum caminho do codigo contem nome de usuario. Toda descoberta
usa, nesta ordem: (1) argumento explicito, (2) variavel de ambiente, (3) arquivo
de configuracao do usuario, (4) candidatos derivados de HOME/HOMEDRIVE/Steam/env,
(5) padrao relativo a raiz do repositorio (quando o layout do repo existe).

Nao le nem escreve no perfil do dono; nao abre jogo; nao instala nada.
Uso (stdlib):

    python descoberta.py --json
    python descoberta.py --destino-sugerido

Exit: 0 = relatorio ok; 2 = erro de infraestrutura.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

SCHEMA = "kit-rstv/descoberta/1"

AQUI = os.path.dirname(os.path.abspath(__file__))

ENV_DESTINO = "KIT_RSTV_HOME"
ENV_JOGO = "KIT_RSTV_JOGO"
ENV_RAIZ = "KIT_RSTV_RAIZ"
NOME_ARQUIVO_CONFIG = "kit-rstv.conf.json"


def _primeiro_existente(candidatos):
    for c in candidatos:
        if not c:
            continue
        c = os.path.abspath(c)
        if os.path.isdir(c):
            return c
    return None


def raiz_do_repositorio(inicio=None):
    """Sobe a partir de `inicio` procurando um diretorio com tools/automacao."""
    atual = os.path.abspath(inicio or os.getcwd())
    if os.path.isfile(atual):
        atual = os.path.dirname(atual)
    while True:
        if os.path.isdir(os.path.join(atual, "tools", "automacao")):
            return atual
        pai = os.path.dirname(atual)
        if pai == atual:
            return None
        atual = pai


def diretorio_de_config(explicito=None, ambiente=None):
    """Diretorio do arquivo de configuracao do usuario (sem nome de usuario fixo)."""
    if explicito:
        return os.path.abspath(explicito)
    if ambiente and ambiente.get("KIT_RSTV_CONFIG"):
        return os.path.abspath(ambiente["KIT_RSTV_CONFIG"])
    if os.name == "nt":
        base = ambiente.get("APPDATA") if ambiente else os.environ.get("APPDATA")
    else:
        base = None
        if ambiente is not None:
            base = ambiente.get("XDG_CONFIG_HOME")
        if base is None:
            base = os.environ.get("XDG_CONFIG_HOME")
    if not base:
        home = (ambiente or os.environ).get("HOME") or (ambiente or os.environ).get("USERPROFILE")
        base = os.path.join(home, ".config") if home else None
    return os.path.join(base, "kit-rstv") if base else None


def ler_config(caminho):
    try:
        with open(caminho, "r", encoding="utf-8") as fh:
            dados = json.load(fh)
        return dados if isinstance(dados, dict) else {}
    except (OSError, ValueError):
        return {}


def raiz_efetiva(inicio=None, ambiente=None):
    """Raiz do repositorio de forma determinista: env explicita (do dicionario passado E do
    ambiente do processo) -> caminho DESTE arquivo (o tool sabe onde mora) -> subida a partir
    de `inicio`. Nunca depende do cwd."""
    for fonte in (ambiente or {}, os.environ):
        for chave in ("KIT15_RAIZ", ENV_RAIZ):
            valor = fonte.get(chave)
            if valor and os.path.isdir(os.path.join(valor, "tools", "automacao")):
                return os.path.abspath(valor)
    return raiz_do_repositorio(inicio or AQUI)


def destino_do_kit(explicito=None, ambiente=None, caminho_config=None, inicio=None, usar_repo=True):
    """Resolve o diretorio de instalacao do kit. Devolve (destino, origem_da_escolha)."""
    ambiente = dict(os.environ if ambiente is None else ambiente)

    if explicito:
        return os.path.abspath(explicito), "argumento"

    if ambiente.get(ENV_DESTINO):
        return os.path.abspath(ambiente[ENV_DESTINO]), "ambiente:" + ENV_DESTINO

    conf_dir = diretorio_de_config(caminho_config, ambiente)
    if conf_dir:
        conf = ler_config(os.path.join(conf_dir, NOME_ARQUIVO_CONFIG))
        if conf.get("destino"):
            return os.path.abspath(conf["destino"]), "config"

    if usar_repo:
        raiz = raiz_efetiva(inicio, ambiente)
        if raiz and os.path.isdir(raiz):
            return os.path.join(os.path.abspath(raiz), "dist", "kit-rstv"), "padrao-repo"

    home = ambiente.get("HOME") or ambiente.get("USERPROFILE")
    if not home:
        return None, "indeterminado"
    return os.path.join(os.path.abspath(home), "kit-rstv"), "padrao-home"


def diretorio_do_jogo(explicito=None, ambiente=None, candidatos_extra=None):
    """Localiza a pasta do Stolen Realm SEM usuario fixo.

    Nao e obrigatorio para o uso basico do kit; ausencia e um resultado legitimo
    (None). Apenas isola candidatos de instalacao padrao do Steam/Unidade de jogos.
    """
    ambiente = dict(os.environ if ambiente is None else ambiente)
    if explicito:
        return os.path.abspath(explicito) if os.path.isdir(explicito) else None

    candidatos = []
    if ambiente.get(ENV_JOGO):
        candidatos.append(ambiente[ENV_JOGO])
    if candidatos_extra:
        candidatos.extend(candidatos_extra)

    raizes_steam = []
    for chave in ("ProgramFiles(x86)", "ProgramFiles"):
        if ambiente.get(chave):
            raizes_steam.append(os.path.join(ambiente[chave], "Steam", "steamapps", "common"))
    # Bibliotecas de Steam em outras unidades, sem nome de usuario fixo.
    for letra in "CDEFGH":
        raizes_steam.append(letra + ":\\SteamLibrary\\steamapps\\common")
        raizes_steam.append(letra + ":\\Games\\Steam\\steamapps\\common")
    for raiz in raizes_steam:
        candidatos.append(os.path.join(raiz, "Stolen Realm"))
        candidatos.append(os.path.join(raiz, "StolenRealm"))

    return _primeiro_existente(candidatos)


def diretorio_do_perfil(explicito=None, ambiente=None):
    """Pasta r2modman/BepInEx do perfil. OPCIONAL: o kit nao precisa dela para nada
    do uso basico, e esta frente NAO instala nem altera perfil. Devolve None se
    nenhum candidato existir (nada e criado por conta propria)."""
    ambiente = dict(os.environ if ambiente is None else ambiente)
    if explicito:
        return os.path.abspath(explicito) if os.path.isdir(explicito) else None
    base = ambiente.get("APPDATA")
    if not base:
        return None
    candidato = os.path.join(base, "r2modmanPlus-local", "StolenRealm", "profiles", "Default", "BepInEx")
    return candidato if os.path.isdir(candidato) else None


def relatorio(explicito=None, ambiente=None, inicio=None):
    destino, origem = destino_do_kit(explicito=explicito, ambiente=ambiente, inicio=inicio)
    raiz = raiz_efetiva(inicio, ambiente)
    return {
        "schema": SCHEMA,
        "destino_kit": destino,
        "destino_origem": origem,
        "raiz_repo": raiz,
        "jogo": diretorio_do_jogo(ambiente=ambiente),
        "perfil_bepinex": diretorio_do_perfil(ambiente=ambiente),
        "notas": [
            "jogo/perfil ausentes NAO impedem o uso basico (instalar/atualizar/remover/scan/zip)",
            "esta ferramenta nunca escreve no perfil do dono nem no jogo",
        ],
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description="KIT-15: descoberta de caminhos sem usuario fixo")
    ap.add_argument("--destino", help="destino explicito do kit (maior prioridade)")
    ap.add_argument("--inicio", help="diretorio inicial para localizar a raiz do repo")
    ap.add_argument("--destino-sugerido", action="store_true", help="imprime so o destino resolvido")
    ap.add_argument("--json", action="store_true", help="imprime o relatorio completo em JSON")
    args = ap.parse_args(argv)

    try:
        dados = relatorio(explicito=args.destino, inicio=args.inicio)
    except Exception as exc:  # pragma: no cover - infra
        print("ERRO-INFRA KIT-15 descoberta: %s" % exc, file=sys.stderr)
        return 2

    if args.destino_sugerido:
        if not dados["destino_kit"]:
            print("INDETERMINADO")
            return 2
        print(dados["destino_kit"])
        return 0
    print(json.dumps(dados, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
