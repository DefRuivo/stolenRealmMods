#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_dependencias.py - PKG-5: toda dependencia de todo manifest tem de RESOLVER.

O DEFEITO QUE ESTE ARQUIVO EXISTE PARA PEGAR (REV-10)
-----------------------------------------------------
A Thunderstore NAO aceita uma dependencia que aponte para uma versao que nao existe: no
upload, o `PackageReferenceValidator(resolve=True)` procura cada `namespace-nome-versao` e
RECUSA o pacote inteiro com `No matching package found for reference` se a versao nao
estiver publicada. O `valida_pacotes.py` (metadados) e o `check_versoes.py` (versao
csproj=x cm=manifest) NAO olhavam isso: os dois passariam uma referencia a uma versao
inedita, e um "APROVADO local" nao garantia "publicavel". Um pacote rejeitado no upload e
o pior tipo de falha: ele so aparece no ultimo passo, depois de tudo aprovado.

O QUE A THUNDERSTORE EXIGE DE `dependencies` (mapeamento)
---------------------------------------------------------
  * Formato de CADA item: `namespace-nome-versao`, ex. `DefRuivo_StolenRealmMods-BetterFont-1.0.2`.
    O NAMESPACE pode conter '-' (leitura de tras para frente: ultimo campo = versao,
    penultimo = nome, o resto = namespace); nome e versao nao.
  * A versao tem de estar em semver `X.Y.Z` e ser IGUAL a uma versao PUBLICADA daquele
    pacote - nao existe intervalo, nao existe ">=", nao existe resolucao por proximidade.
  * A resolucao e por LOOKUP, na hora do upload: nao ha "envio conjunto" da Thunderstore.
    Se A depende de B-1.0.2 e a 1.0.2 ainda nao subiu, o envio de A e recusado. Por isso a
    ORDEM de envio do lote importa: a dependencia publica ANTES do dependente.
  * Mao dupla entre versoes INEDITAS (A depende de B e B depende de A, nenhum no ar antes):
    nao ha ordem de envio que resolva - e o caso que a revisao REV-10 mapeou.

COMO ESTE SCRIPT DECIDE
-----------------------
Para cada dependencia, nessa ordem:
  1. se `<ns>-<nome>-<versao>` JA ESTA publicada -> resolve (nao precisa de ordem);
  2. senao, se o nome e um mod DESTE repositorio e a versao referida e a que ele declara
     HOJE (a que vai sair no lote) -> resolve SE o mod estiver liberado (publicar:true) e a
     ORDEM de envio colocar a dependencia ANTES do dependente (sem ciclo);
  3. senao -> REPROVA com o motivo (versao inexistente / versao que o repo nao vai enviar /
     mod nao liberado / ciclo de mao dupla).

FONTES DO "JA PUBLICADO"
------------------------
  * `--local` (padrao, sem rede): le `release/mods.json` (`versao_publicada` de cada mod,
    escrito pelo pipeline a partir da API) + o BepInExPack obrigatorio. Deterministico -
    e o modo que o CI usa, entao ele nunca fica vermelho por a API publica oscilar.
  * `--api` (fresco): pergunta a API publica POR VERSAO EXATA
    (`/api/experimental/package/<team>/<mod>/<versao>/`, a mesma que o pre-flight do
    `publish.yml` usa), com User-Agent proprio e retry - a API responde 403 ao
    User-Agent padrao do urllib e rate-limita cliente anonimo. Sem token: leitura publica.

USO
---
    python tools/check_dependencias.py            # offline (release/mods.json)
    python tools/check_dependencias.py --api      # confere na API publica por versao
    python tools/check_dependencias.py --json

    exit 0 = toda dependencia resolve (e a ordem de envio sai impressa);
    exit 1 = alguma dependencia NAO resolve (o motivo e impresso);
    exit 2 = nao consegui rodar (sem manifest / API indisponivel).

O modulo tambem e IMPORTADO pelo `.github/scripts/valida_pacotes.py` (a mesma regra, no
passo de metadados do CI). Este arquivo e a fonte unica da resolucao.
"""
import argparse
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODS_JSON = os.path.join(RAIZ, "release", "mods.json")

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
NOME_VALIDO = re.compile(r"^[A-Za-z0-9_]+$")

# A unica dependencia obrigatoria: ja publicada, conhecida de sempre.
DEPENDENCIA_OBRIGATORIA = "BepInEx-BepInExPack-5.4.2305"

# Fallback do team quando o `release/mods.json` nao traz o campo (nao deveria acontecer).
TEAM_PADRAO = "DefRuivo_StolenRealmMods"

USER_AGENT = "stolenRealmMods-pkg5 (github.com/DefRuivo/stolenRealmMods)"


# ------------------------------------------------------------------ leitura de refs

def partes_da_referencia(ref):
    """(namespace, nome, versao) de `Autor-Pacote-Versao`, ou (None, None, None).

    Leitura de tras para frente, a mesma do `PackageReference.parse` do Thunderstore: o
    NAMESPACE pode conter '-'; nome e versao nao.
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


def montar_referencia(namespace, nome, versao):
    return "%s-%s-%s" % (namespace, nome, versao)


# ------------------------------------------------------------------ dados do repositorio

def _pastas_com_manifest():
    """Nomes das pastas de mod (as mesmas marcas de `pastas_com_manifest` do valida_pacotes)."""
    ignorar = {"docs", "dist", "lib", "scratch", "tools", ".git", ".github",
               "ReloadProbe", "__pycache__"}
    nomes = []
    for nome in sorted(os.listdir(RAIZ)):
        pasta = os.path.join(RAIZ, nome)
        if not os.path.isdir(pasta) or nome.startswith(".") or nome in ignorar:
            continue
        marcas = ("%s.csproj" % nome, "manifest.json", "icon.png", "Plugin.cs")
        if not any(os.path.isfile(os.path.join(pasta, m)) for m in marcas):
            continue
        if os.path.isfile(os.path.join(pasta, "manifest.json")):
            nomes.append(nome)
    return nomes


def entradas_do_repo():
    """[{nome, versao, deps:[ref,...]}] - o que cada manifest deste repo declara HOJE."""
    entradas = []
    for nome in _pastas_com_manifest():
        caminho = os.path.join(RAIZ, nome, "manifest.json")
        try:
            manifesto = json.loads(io.open(caminho, encoding="utf-8").read())
        except (OSError, ValueError):
            continue
        if not isinstance(manifesto, dict):
            continue
        entradas.append({
            "nome": nome,
            "versao": manifesto.get("version_number"),
            "deps": list(manifesto.get("dependencies") or []),
        })
    return entradas


def ler_mods_json():
    try:
        return json.loads(io.open(MODS_JSON, encoding="utf-8").read())
    except (OSError, ValueError):
        return None


def team_do_mods_json(dados=None):
    dados = dados if dados is not None else ler_mods_json()
    if isinstance(dados, dict):
        return (dados.get("team") or "").strip() or TEAM_PADRAO
    return TEAM_PADRAO


def publicadas_do_mods_json(dados=None):
    """Set de `<team>-<nome>-<versao_publicada>` do registro versionado + o BepInExPack.

    O `release/mods.json` guarda a ULTIMA versao no ar de cada mod (escrita pelo job
    `registra` a partir da API). E a fonte offline - deterministica -, nao a memoria.
    """
    dados = dados if dados is not None else ler_mods_json()
    publicadas = {DEPENDENCIA_OBRIGATORIA}
    if not isinstance(dados, dict):
        return publicadas
    team = team_do_mods_json(dados)
    for m in dados.get("mods") or []:
        versao = m.get("versao_publicada")
        if m.get("nome") and versao:
            publicadas.add(montar_referencia(team, m["nome"], versao))
    return publicadas


def liberados_do_mods_json(dados=None):
    """Set dos mods com `publicar: true`, ou None se nao houver registro (nao travamos)."""
    dados = dados if dados is not None else ler_mods_json()
    if not isinstance(dados, dict):
        return None
    liberados = {m.get("nome") for m in (dados.get("mods") or []) if m.get("publicar") is True}
    return liberados or None


# ------------------------------------------------------------------ o resolver (PURO)

def resolver(entradas, publicadas, liberados=None):
    """Resolve TODAS as dependencias. NAO usa rede - e a regra, testavel isolada.

    entradas  : [{nome, versao, deps:[ref,...]}]  (mods deste repositorio)
    publicadas: set de `<ns>-<nome>-<versao>` JA no ar
    liberados : set de nomes liberados a sair neste lote (None = todos)

    Devolve dict:
      problemas  : lista de motivos (vazia = tudo resolve)
      ordem      : ordem de envio (dependencia antes do dependente) - toda a lista
      resolvidas : o que resolveu e por que (auditoria)
      ciclo      : nomes presos num ciclo de versoes ineditas (mao dupla)
    """
    problemas = []
    resolvidas = []
    versao_do_mod = {e["nome"]: e.get("versao") for e in entradas}
    # aresta `dep -> dependente`: `dep` tem de sair ANTES de `dependente`.
    sucessores = {e["nome"]: set() for e in entradas}

    for e in entradas:
        dependente = e["nome"]
        for ref in e.get("deps") or []:
            namespace, nome_dep, versao_dep = partes_da_referencia(ref)
            if namespace is None:
                problemas.append("%s: dependencia %r nao esta no formato "
                                 "namespace-nome-versao" % (dependente, ref))
                continue
            full = montar_referencia(namespace, nome_dep, versao_dep)

            # 1. ja publicada -> resolve, sem ordem.
            if full in publicadas:
                resolvidas.append("%s: %s (ja publicada)" % (dependente, full))
                continue

            # 2. mod deste repositorio, na versao que ele declara HOJE -> sai no lote.
            if nome_dep in versao_do_mod:
                alvo = versao_do_mod[nome_dep]
                if versao_dep != alvo:
                    problemas.append(
                        "%s: depende de %s, que NAO esta publicada e NAO e a versao que este "
                        "repo vai enviar (%s declara hoje %s) - no matching package found"
                        % (dependente, full, nome_dep, alvo))
                    continue
                if liberados is not None and nome_dep not in liberados:
                    problemas.append(
                        "%s: depende de %s v%s, que ainda NAO esta publicada e NAO esta "
                        "liberado (publicar:false) - esse pacote nunca entra no ar"
                        % (dependente, nome_dep, versao_dep))
                    continue
                sucessores[nome_dep].add(dependente)
                resolvidas.append("%s: %s (mesmo lote; %s sai antes)"
                                  % (dependente, full, nome_dep))
                continue

            # 3. nem publicada, nem produzida por este lote -> recusa.
            problemas.append(
                "%s: depende de %s, que NAO existe na Thunderstore "
                "(No matching package found for reference)" % (dependente, full))

    ordem, ciclo = _ordem_topologica(entradas, sucessores)
    if ciclo:
        problemas.append(
            "MAO DUPLA/CICLO entre versoes INEDITAS: %s - nenhum dos lados esta publicado "
            "(ou liberado) e nenhuma ordem de envio resolve" % ", ".join(ciclo))

    return {"problemas": problemas, "ordem": ordem, "resolvidas": resolvidas, "ciclo": ciclo}


def _ordem_topologica(entradas, sucessores):
    """(ordem, ciclo). Kahn: nos com indegree 0 primeiro; o que sobra e ciclo.

    A ordem preserva a ordem de entrada entre os independentes (deterministico).
    """
    nomes = [e["nome"] for e in entradas]
    indeg = {n: 0 for n in nomes}
    for dep, dependentes in sucessores.items():
        for d in dependentes:
            if d in indeg:
                indeg[d] += 1
    prontos = [n for n in nomes if indeg[n] == 0]
    ordem = []
    while prontos:
        n = prontos.pop(0)
        ordem.append(n)
        for d in sorted(sucessores.get(n, ())):
            indeg[d] -= 1
            if indeg[d] == 0:
                prontos.append(d)
    ordem += [n for n in nomes if n not in ordem]
    ciclo = [n for n in nomes if indeg[n] > 0]
    return ordem, ciclo


# ------------------------------------------------------------------ API publica (fresca)

def _busca(url, tentativas=4):
    """(status, corpo). 200/404 sao RESPOSTA; 429/5xx/rede se repetem. Sem token."""
    espera = 3
    for tentativa in range(tentativas):
        if tentativa:
            time.sleep(espera)
        try:
            pedido = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(pedido, timeout=60) as resp:
                return resp.status, json.load(resp)
        except urllib.error.HTTPError as erro:
            if erro.code != 429 and erro.code < 500:
                return erro.code, None
            espera = min(int(erro.headers.get("Retry-After") or 0) or (3 * tentativa + 3), 30)
        except Exception:
            espera = 3 * tentativa + 3
    return None, None


def publicadas_da_api(entradas, team):
    """Set de referencias JA publicadas, por VERSAO EXATA (fresco). Levanta RuntimeError se
    a API nao responde NENHUMA consulta (rede fora) - ai nao da para afirmar nada."""
    alvos = {DEPENDENCIA_OBRIGATORIA}
    for e in entradas:
        for ref in e.get("deps") or []:
            if partes_da_referencia(ref)[0] is not None:
                alvos.add(ref)
    publicadas, respostas = set(), 0
    for ref in sorted(alvos):
        namespace, nome, versao = partes_da_referencia(ref)
        url = ("https://thunderstore.io/api/experimental/package/%s/%s/%s/"
               % (namespace, nome, versao))
        status, _ = _busca(url)
        if status is not None:
            respostas += 1
        if status == 200:
            publicadas.add(ref)
    if respostas == 0:
        raise RuntimeError("a API publica nao respondeu nenhuma consulta (sem rede?) - "
                           "use o modo offline (--local) ou tente de novo")
    return publicadas


def resolver_local():
    """(resultado, entradas, publicadas, liberados) usando o registro versionado."""
    entradas = entradas_do_repo()
    publicadas = publicadas_do_mods_json()
    liberados = liberados_do_mods_json()
    return resolver(entradas, publicadas, liberados), entradas, publicadas, liberados


def resolver_api():
    entradas = entradas_do_repo()
    team = team_do_mods_json()
    publicadas = publicadas_da_api(entradas, team)
    liberados = liberados_do_mods_json()
    return resolver(entradas, publicadas, liberados), entradas, publicadas, liberados


# ------------------------------------------------------------------ CLI

def main(argv=None):
    ap = argparse.ArgumentParser(description="Resolve as dependencias dos manifests (PKG-5).")
    modo = ap.add_mutually_exclusive_group()
    modo.add_argument("--api", action="store_true",
                      help="confere 'ja publicado' na API publica por versao (fresco)")
    modo.add_argument("--local", action="store_true",
                      help="modo padrao: le release/mods.json (sem rede, deterministico)")
    ap.add_argument("--json", action="store_true", help="saida JSON")
    args = ap.parse_args(argv)

    entradas = entradas_do_repo()
    if not entradas:
        print("check_dependencias: nenhum manifest.json encontrado em %s" % RAIZ)
        return 2

    try:
        if args.api:
            resultado, _, publicadas, _ = resolver_api()
            fonte = "API publica (por versao, fresco)"
        else:
            resultado, _, publicadas, _ = resolver_local()
            fonte = "release/mods.json + BepInExPack (offline)"
    except RuntimeError as erro:
        print("check_dependencias: %s" % erro)
        return 2

    if args.json:
        print(json.dumps({"fonte": fonte, "publicadas": sorted(publicadas),
                          "ordem": resultado["ordem"], "problemas": resultado["problemas"],
                          "resolvidas": resultado["resolvidas"], "ciclo": resultado["ciclo"]},
                         ensure_ascii=False, indent=2))
        return 1 if resultado["problemas"] else 0

    print("check_dependencias - toda dependencia tem de RESOLVER antes do envio (PKG-5)")
    print("fonte do 'ja publicado': %s" % fonte)
    print("mods deste repo: %s" % ", ".join(e["nome"] for e in entradas))
    print()
    for r in resultado["resolvidas"]:
        print("  ok    %s" % r)
    if resultado["problemas"]:
        print()
        for p in resultado["problemas"]:
            print("  FALHA %s" % p)
    print()
    if resultado["ordem"]:
        print("ordem de envio (dependencia ANTES do dependente):")
        for i, nome in enumerate(resultado["ordem"], 1):
            print("   %d. %s" % (i, nome))
    print()
    if resultado["problemas"]:
        print("==> %d dependencia(s) NAO resolvem - o upload seria recusado pela Thunderstore "
              "(No matching package found)." % len(resultado["problemas"]))
        return 1
    print("  ==> todas as dependencias resolvem (publicadas ou na ordem de envio acima)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
