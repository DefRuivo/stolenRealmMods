#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A TRAVA DO OPT-IN NOS .csproj REAIS (DEPLOY-2): o build cru do repo nao instala.

POR QUE ESTE TESTE EXISTE
-------------------------
Os testes de guarda usam fixtures plantadas; este olha os .csproj DE VERDADE. E aqui
que o defeito do REL-3 vivia e onde a revisao DEPLOY-1R mediu: nenhum csproj exigia
opt-in — a Condition era `"!= 'false'"`, e num `dotnet build` comum a propriedade vinha
VAZIA, logo a condicao era VERDADEIRA e o alvo copiava para o perfil do dono. O alvo
`DeployToScripts` do ReloadProbe ia alem: nem Condition tinha.

O teste cobra, sobre o repositorio vivo:

  1. `Directory.Build.props` na RAIZ define `DeployToBepInEx=false` (o padrao desligado);
  2. a guarda (`tools/check_deploy_optin.py`) varre o repo inteiro e nao acha NENHUM alvo
     de deploy sem opt-in — cobrindo plugins E scripts, de qualquer nome;
  3. a Condition antiga (`!= 'false'`) sumiu dos csproj COM alvo de deploy: se voltar,
     o build cru instala de novo;
  4. o alvo `DeployToScripts` do ReloadProbe carrega o MESMO opt-in (o furo B medido).
"""
import importlib.util
import os
import xml.etree.ElementTree as ET

import arcabouco as arc

META = {
    "nome": "deploy-optin-repo",
    "categoria": "pura",
    "requer": [],
    "descricao": ("os csproj reais exigem o opt-in de deploy: Directory.Build.props desliga por "
                  "padrao, nenhum alvo escreve no perfil sem Condition, e o DeployToScripts do "
                  "ReloadProbe esta coberto"),
}


def _guarda():
    caminho = os.path.join(arc.raiz_do_repo(), "tools", "check_deploy_optin.py")
    spec = importlib.util.spec_from_file_location("check_deploy_optin", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _csprojs(raiz):
    for pasta, dirs, arquivos in os.walk(raiz):
        dirs[:] = [d for d in dirs if d not in (".git", "bin", "obj", "node_modules")]
        for nome in sorted(arquivos):
            if nome.endswith(".csproj"):
                yield os.path.join(pasta, nome)


def corpo():
    raiz = arc.raiz_do_repo()

    # ---- 1. o padrao desligado mora na RAIZ --------------------------------------
    props = os.path.join(raiz, "Directory.Build.props")
    arc.exigir(os.path.isfile(props),
               "falta o Directory.Build.props na raiz — sem ele o padrao do deploy nao existe")
    with open(props, encoding="utf-8") as fh:
        texto_props = fh.read()
    arc.exigir("<DeployToBepInEx" in texto_props and "== ''" in texto_props and ">false<" in texto_props,
               "o Directory.Build.props nao define DeployToBepInEx=false como padrao: %r" % texto_props)

    # ---- 2. a guarda nao acha alvo sem opt-in no repo vivo ------------------------
    # O ReloadProbe e um harness de bancada GITIGNORED (`.gitignore`: `ReloadProbe/`) — ele
    # NAO existe num clone limpo nem no CI. A trava cobra os 6 mods SEMPRE e conta o alvo
    # dele a mais SO quando o diretorio esta presente; exigir 7 sempre derrubava o clone
    # (era o proprio defeito que o GIT-3 existe para fechar: a suite tem de rodar no clone).
    tem_reloadprobe = os.path.isdir(os.path.join(raiz, "ReloadProbe"))
    minimo_alvos = 6 + (1 if tem_reloadprobe else 0)

    guarda = _guarda()
    achados, n_alvos = guarda.analisa_raiz(raiz)
    arc.igual(achados, [],
              "a guarda reprova alvo(s) de deploy nos csproj REAIS (o build cru instalaria): %s" % achados)
    arc.exigir(n_alvos >= minimo_alvos,
               "a guarda contou so %d alvo(s) de deploy no repo — esperava pelo menos %d "
               "(6 mods%s)" % (n_alvos, minimo_alvos,
                               " + o DeployToScripts do ReloadProbe" if tem_reloadprobe else ""))

    # ---- 3+4. a Condition antiga sumiu; o DeployToScripts esta coberto -----------
    com_alvo_de_deploy = 0
    for caminho in _csprojs(raiz):
        with open(caminho, encoding="utf-8") as fh:
            texto = fh.read()
        if "r2modmanPlus-local" not in texto and "USERPROFILE" not in texto:
            continue
        com_alvo_de_deploy += 1
        arc.exigir("!= 'false'" not in texto,
                   "%s ainda tem a Condition antiga (\"!= 'false'\"), que num build cru e VERDADEIRA "
                   "e instala no perfil" % os.path.relpath(caminho, raiz))
        arc.exigir("== 'true'" in texto,
                   "%s escreve no perfil e nao tem nenhum alvo com o opt-in \"== 'true'\""
                   % os.path.relpath(caminho, raiz))

    arc.exigir(com_alvo_de_deploy >= minimo_alvos,
               "so %d csproj do repo escrevem no perfil — esperava pelo menos %d (6 mods%s)"
               % (com_alvo_de_deploy, minimo_alvos,
                  " + ReloadProbe" if tem_reloadprobe else ""))

    # o alvo do ReloadProbe tem de carregar o opt-in, com o NOME dele (DeployToScripts) —
    # so quando ele existe: e um harness local gitignored, ausente no clone e no CI.
    if tem_reloadprobe:
        rel = os.path.join(raiz, "ReloadProbe", "ReloadProbe.csproj")
        raiz_xml = ET.parse(rel).getroot()
        alvos = [a for a in raiz_xml.iter() if a.tag.rsplit("}", 1)[-1] == "Target"]
        nomes = {a.get("Name") for a in alvos}
        arc.exigir("DeployToScripts" in nomes,
                   "o ReloadProbe perdeu o alvo DeployToScripts (ou mudou de nome): %s" % sorted(nomes))
        script = [a for a in alvos if a.get("Name") == "DeployToScripts"][0]
        arc.igual(script.get("Condition"), "'$(DeployToBepInEx)' == 'true'",
                  "o alvo DeployToScripts do ReloadProbe nao tem o opt-in (furo B de volta)")


if __name__ == "__main__":
    arc.main(META, corpo)
