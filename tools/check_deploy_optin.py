#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_deploy_optin.py — a guarda do OPT-IN de deploy (trava DEPLOY-2).

O QUE ESTE ARQUIVO E
--------------------
A guarda que o tools/release-check.sh roda ANTES de buildar, e a trava que os
testes cobram. Ela responde a UMA pergunta:

    "existe algum alvo de deploy nos .csproj que escreve no perfil do r2modman
     SEM exigir o opt-in explicito?"

Todo alvo que escreve no perfil tem de ter
    Condition="'$(DeployToBepInEx)' == 'true'"
(sem o `=true` pedido pelo chamador, o alvo NAO roda).

OS DOIS FURAOS QUE ESTA GUARDA FECHA (REL-3/DEPLOY-1R)
-----------------------------------------------------
A guarda anterior era um `grep` que:
  * furo A — lia so a PRIMEIRA linha da tag `<Target ...>`: reprovava um alvo
    VALIDO cuja Condition estava na segunda linha da tag, e PASSAVA um alvo
    multi-linha que simplesmente NAO tinha Condition (a tag terminava sem ela);
  * furo B — cobria so alvos CHAMADOS `DeployToBepInEx`; um alvo com outro nome
    (ex.: o `DeployToScripts` do ReloadProbe) era invisivel para a guarda.

Aqui os .csproj sao lidos como XML DE VERDADE (ElementTree): o furo A some porque
o atributo `Condition` e lido do elemento, independente de quantas linhas a tag
ocupa; o furo B some porque o criterio e "o alvo escreve no perfil?", nao o NOME
do alvo.

POR QUE "ESCREVE NO PERFIL" E NAO "CHAMA Deploy"
------------------------------------------------
O defeito nao e ter um alvo chamado Deploy: e um alvo que COPIA o artefato para
fora do repo, para o ambiente do dono, sem ninguem ter pedido. Entao o criterio e
o destino: o alvo menciona o caminho do perfil (`r2modmanPlus-local`, `USERPROFILE`,
`APPDATA`, `BepInEx\\plugins`, `BepInEx\\scripts`) — direto ou por uma propriedade
que aponta para la — E executa uma tarefa de escrita (Copy/Move/MakeDir/...).

SAIDA
-----
    exit 0  nenhum alvo de deploy sem opt-in (a release pode buildar)
    exit 1  ha alvo(s) sem opt-in (o release-check NAO builda nada)

Uso:
    python tools/check_deploy_optin.py [--raiz CAMINHO] [--json]
"""
import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET

# Marcadores de que um alvo (ou uma propriedade) aponta para o ambiente do dono.
SINAIS_PERFIL = (
    "r2modmanplus-local",
    "$(userprofile)",
    "$(appdata)",
    "bepinex\\plugins",
    "bepinex/plugins",
    "bepinex\\scripts",
    "bepinex/scripts",
)

# Tarefas do MSBuild que materializam/escrevem arquivos (a tarefa que COPIA).
TAREFAS_DE_ESCRITA = {
    "copy", "move", "mkdir", "makedir", "touch",
    "writelinestofile", "downloadfile", "createiteminference",
}

# A UNICA Condition aceita num alvo de deploy: opt-in explicito.
RE_CONDICAO_OPTIN = re.compile(
    r"^\s*['\"]?\$\(DeployToBepInEx\)['\"]?\s*==\s*['\"]?true['\"]?\s*$",
    re.IGNORECASE,
)

ARQUIVOS_DE_PROJETO = ("Directory.Build.props", "Directory.Build.targets")


def _nome_local(tag):
    """'Target' a partir de '{urn:...}Target' (csproj antigo tem namespace)."""
    return tag.rsplit("}", 1)[-1]


def _texto(el):
    """Todo o texto e todos os valores de atributo da subarvore de `el`, em minusculas."""
    partes = list(el.itertext())
    for no in el.iter():
        partes.extend(str(v) for v in no.attrib.values())
    return "\n".join(partes).lower()


def _tarefas_de_escrita(alvo):
    return {_nome_local(f.tag).lower() for f in alvo.iter()} & TAREFAS_DE_ESCRITA


def _propriedades_do_perfil(raiz):
    """Nomes (minusculos) de propriedades cujo VALOR aponta para o perfil.

    Cobre o alvo que esconde o destino atras de uma propriedade: sem isto, um
    `<Copy DestinationFolder="$(DirDoPerfil)">` passaria despercebido.
    """
    nomes = set()
    for el in raiz.iter():
        if _nome_local(el.tag) != "PropertyGroup":
            continue
        for prop in el:
            if any(s in _texto(prop) for s in SINAIS_PERFIL):
                nomes.add(_nome_local(prop.tag).lower())
    return nomes


def _aponta_para_perfil(alvo, props_do_perfil):
    texto = _texto(alvo)
    if any(s in texto for s in SINAIS_PERFIL):
        return True
    return any("$(%s)" % nome in texto for nome in props_do_perfil)


def analisa_arquivo(caminho):
    """Devolve a lista de achados (dicts) de UM .csproj/props/targets."""
    try:
        raiz = ET.parse(caminho).getroot()
    except ET.ParseError as erro:
        return [{"arquivo": caminho, "alvo": "?", "condicao": None,
                 "motivo": "XML invalido: %s" % erro}]
    if raiz is None:
        return []

    props_do_perfil = _propriedades_do_perfil(raiz)
    achados = []
    for alvo in raiz.iter():
        if _nome_local(alvo.tag) != "Target":
            continue
        if not _aponta_para_perfil(alvo, props_do_perfil):
            continue
        if not _tarefas_de_escrita(alvo):
            continue
        condicao = alvo.get("Condition", "")
        if not RE_CONDICAO_OPTIN.match(condicao or ""):
            achados.append({
                "arquivo": caminho,
                "alvo": alvo.get("Name", "?"),
                "condicao": condicao or None,
                "motivo": ("alvo de deploy sem Condition=\"'$(DeployToBepInEx)' == 'true'\""
                           " — buildar sem opt-in COPIARIA para o perfil do dono"),
            })
    return achados


def analisa_raiz(raiz):
    """Varre `raiz` atras de *.csproj + Directory.Build.* e devolve (achados, n_alvos)."""
    achados = []
    n_alvos = 0
    for pasta, dirs, arquivos in os.walk(raiz):
        dirs[:] = [d for d in dirs if d not in (".git", "bin", "obj", "node_modules", ".vs")]
        for nome in sorted(arquivos):
            if not (nome.endswith(".csproj") or nome in ARQUIVOS_DE_PROJETO):
                continue
            caminho = os.path.join(pasta, nome)
            # conta os alvos de deploy aceitos deste arquivo tambem
            achados_arq = analisa_arquivo(caminho)
            achados.extend(achados_arq)
            n_alvos += _conta_alvos_deploy(caminho)
    return achados, n_alvos


def _conta_alvos_deploy(caminho):
    try:
        raiz = ET.parse(caminho).getroot()
    except (ET.ParseError, OSError):
        return 0
    if raiz is None:
        return 0
    props = _propriedades_do_perfil(raiz)
    return sum(1 for a in raiz.iter()
               if _nome_local(a.tag) == "Target"
               and _aponta_para_perfil(a, props)
               and _tarefas_de_escrita(a))


def _raiz_padrao():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main(argv=None):
    p = argparse.ArgumentParser(description="guarda do opt-in de deploy (DEPLOY-2)")
    p.add_argument("--raiz", default=_raiz_padrao(),
                   help="raiz a varrer (padrao: a raiz do repo)")
    p.add_argument("--json", action="store_true", help="saida em JSON")
    args = p.parse_args(argv)

    achados, n_alvos = analisa_raiz(args.raiz)

    if args.json:
        print(json.dumps({"alvos_de_deploy": n_alvos, "sem_optin": achados},
                         ensure_ascii=False, indent=2))
        return 1 if achados else 0

    for a in achados:
        rel = os.path.relpath(a["arquivo"], args.raiz).replace("\\", "/")
        print("   [FALHA] %s :: alvo %r — %s" % (rel, a["alvo"], a["motivo"]))
        print("             Condition atual: %s" % (a["condicao"] or "(ausente)"))
    if achados:
        print("   %d alvo(s) de deploy SEM opt-in: o build comum instalaria no perfil." % len(achados))
        return 1
    print("   [ ok  ] %d alvo(s) de deploy, todos com Condition=\"'$(DeployToBepInEx)' == 'true'\""
          % n_alvos)
    return 0


if __name__ == "__main__":
    sys.exit(main())
