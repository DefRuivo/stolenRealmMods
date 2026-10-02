#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A TRAVA DO RELEASE-CHECK (REL-3/DEPLOY-2): verificar NAO instala no perfil do dono.

POR QUE ESTE TESTE EXISTE
-------------------------
O `tools/release-check.sh` passo 3 ja compilou com `dotnet build "$p"`, SEM flag. Como
cada `.csproj` tinha um alvo de deploy, esse build COPIAVA a DLL para o perfil do
r2modman do dono — foi por esse caminho que a DLL das 14:41 chegou la com o jogo aberto
e o jogo travou o arquivo. O primeiro conserto (REL-3) so mexeu no script e a revisao
DEPLOY-1R o refutou: a Condition dos .csproj (`"!= 'false'"`) fazia a flag nao desligar
nada, e o alvo `DeployToScripts` do ReloadProbe nem Condition tinha.

DEPLOY-2 fechou isso de verdade — o deploy virou OPT-IN. Este teste cobra o que faz o
conserto continuar valendo:

  1. nenhuma linha `dotnet build` do script compila sem a variavel da flag — o comando
     que instalava nao pode voltar em silencio;
  2. o padrao e NAO instalar (`FLAG_DEPLOY="-p:DeployToBepInEx=false"`,
     `INSTALAR_NO_PERFIL=0`) e o modo que instala tem nome proprio;
  3. o opt-in `-p:DeployToBepInEx=true` so aparece DENTRO do ramo do modo explicito;
  4. a guarda `tools/check_deploy_optin.py` roda ANTES de buildar e o passo 3 REPROVA
     (sem buildar) quando ela acha alvo de deploy sem opt-in;
  5. o ciclo em jogo so e chamado no modo explicito; no fluxo normal sai PENDENTE;
  6. a mensagem de "perfil intacto" parou de ser AFIRMADA: o script MEDE o perfil
     antes/depois do build.

E um teste de TEXTO, de proposito: o defeito e uma linha de comando, e a prova de que
ela nao esta la e a leitura do proprio script que roda.
"""
import os
from typing import Callable, List

import arcabouco as arc

META = {
    "nome": "rel3-release-check-sem-deploy",
    "categoria": "pura",
    "requer": [],
    "descricao": ("o release-check nao builda sem a flag, o opt-in so sai no modo explicito, a "
                  "guarda roda antes e a mensagem de perfil intacto e medida, nao afirmada"),
}

CAMINHO = os.path.join(arc.raiz_do_repo(), "tools", "release-check.sh")


def _codigo(linhas: List[str]) -> List[str]:
    """Só o código: comentario nao conta (o cabecalho do script cita o defeito de proposito)."""
    return [l for l in linhas if not l.lstrip().startswith("#")]


def _indice(codigo: List[str], predicado: Callable[[str], bool], mensagem: str) -> int:
    """A posicao da primeira linha que casa; sem ela, REPROVA nomeando o que faltou."""
    for i, linha in enumerate(codigo):
        if predicado(linha):
            return i
    raise arc.Falhou(mensagem)


def corpo():
    with open(CAMINHO, encoding="utf-8") as fh:
        codigo = _codigo(fh.read().splitlines())

    # ---- 1. o comando que instalava nao pode voltar --------------------------
    builds = [l for l in codigo if "dotnet build" in l]
    arc.exigir(builds, "nao ha mais nenhuma linha `dotnet build` em %s — o passo 3 sumiu?" % CAMINHO)
    for l in builds:
        arc.exigir("$FLAG_DEPLOY" in l,
                   "ha um `dotnet build` que NAO passa $FLAG_DEPLOY. Sem a flag o alvo de deploy "
                   "COPIA a DLL para o perfil do dono:\n%s" % l)

    # ---- 2. o padrao e NAO instalar; o modo que instala tem nome -------------
    arc.exigir(any(l.strip() == 'FLAG_DEPLOY="-p:DeployToBepInEx=false"' for l in codigo),
               "a flag do fluxo normal nao esta definida como -p:DeployToBepInEx=false")
    arc.exigir(any(l.strip() == "INSTALAR_NO_PERFIL=0" for l in codigo),
               "o padrao deixou de ser NAO instalar (INSTALAR_NO_PERFIL=0)")
    arc.exigir(any("--instalar-no-perfil" in l and "INSTALAR_NO_PERFIL=1" in l for l in codigo),
               "o modo explicito nao tem mais a flag propria (--instalar-no-perfil)")

    # ---- 3. o opt-in (true) so sai no ramo do modo explicito -----------------
    idx = _indice(codigo, lambda l: l.strip() == 'FLAG_DEPLOY="-p:DeployToBepInEx=true"',
                  "o modo explicito nao pede o opt-in (-p:DeployToBepInEx=true) — sob o design "
                  "opt-in ele nao instalaria mais nada")
    arc.exigir('INSTALAR_NO_PERFIL" -eq 1' in codigo[idx - 1],
               "o opt-in -p:DeployToBepInEx=true foi armado FORA do ramo do modo explicito "
               "(linha anterior: %r)" % codigo[idx - 1])

    # ---- 4. a guarda do opt-in roda ANTES de buildar e REPROVA sem buildar ----
    idx_guarda = _indice(codigo, lambda l: "check_deploy_optin.py" in l,
                         "o passo 3 nao chama mais a guarda tools/check_deploy_optin.py")
    idx_falha_guarda = _indice(codigo, lambda l: "passo_fail" in l and "3. BUILD" in l and "opt-in" in l,
                               "a guarda nao tem mais o passo_fail do 3. BUILD que barra o build "
                               "sem opt-in")
    idx_primeiro_build = _indice(codigo, lambda l: "dotnet build" in l,
                                 "nao ha `dotnet build` no script (o passo 3 sumiu?)")
    arc.exigir(idx_guarda < idx_falha_guarda < idx_primeiro_build,
               "a guarda saiu da frente do build (guarda=%s falha=%s build=%s): sem isso um alvo "
               "sem opt-in chegaria a buildar" % (idx_guarda, idx_falha_guarda, idx_primeiro_build))

    # ---- 5. o ciclo em jogo so roda no modo explicito ------------------------
    i8 = _indice(codigo, lambda l: "PASSO 8/9" in l, "o passo 8 (CICLO) desapareceu do script")
    pendente = _indice(codigo, lambda l: "passo_pendente" in l and "8. CICLO" in l,
                       "o fluxo normal nao registra mais o 8. CICLO como PENDENTE — o resumo "
                       "mentiria dizendo APROVADO com o ciclo nao rodado")
    porta = i8 + _indice(codigo[i8:], lambda l: 'INSTALAR_NO_PERFIL" -eq 0' in l,
                         "o passo 8 nao tem mais a porta do fluxo normal")
    ciclo = _indice(codigo, lambda l: "test-cycle.sh" in l and "bash" in l,
                    "o script nao chama mais o ciclo (test-cycle.sh)")
    arc.exigir(i8 < porta < pendente < ciclo,
               "o ciclo em jogo saiu do ramo explicito (passo8=%s porta=%s pendente=%s ciclo=%s): "
               "no fluxo normal ele abriria o jogo do dono" % (i8, porta, pendente, ciclo))

    # ---- 6. a mensagem de "perfil intacto" e MEDIDA, nao afirmada ------------
    arc.exigir(not any("sem deploy: perfil intacto" in l for l in codigo),
               "voltou a mensagem que AFIRMAVA 'perfil intacto' sem medir (era a que mentia "
               "enquanto o DeployToScripts escrevia no perfil)")
    arc.exigir(any("perfil medido intacto" in l for l in codigo),
               "o passo 3 nao declara mais que o perfil foi MEDIDO intacto")
    arc.exigir(any("SNAP_PERFIL_ANTES" in l for l in codigo),
               "sumiu a fotografia do perfil antes do build (a medicao que impede a mensagem de mentir)")
    arc.exigir(any("Directory.Build.props" in l for l in codigo),
               "o script nao explica o padrao do opt-in (Directory.Build.props)")


if __name__ == "__main__":
    arc.main(META, corpo)
