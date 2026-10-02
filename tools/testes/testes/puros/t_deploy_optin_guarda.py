#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A GUARDA DO OPT-IN DE DEPLOY (DEPLOY-2): os dois furaos fechados, com iscas.

POR QUE ESTE TESTE EXISTE
-------------------------
A revisao DEPLOY-1R mostrou que o `tools/release-check.sh` AFIRMAVA proteger o perfil
com uma guarda que, na pratica, falhava nos dois sentidos. A guarda antiga era um
`grep` que lia so a PRIMEIRA linha da tag `<Target ...>`:

  * FURO A — reprovava um alvo VALIDO quando a `Condition` estava na 2a linha da tag
    (tag multi-linha) e PASSAVA um alvo multi-linha que simplesmente NAO tinha
    Condition (a tag terminava sem ela);
  * FURO B — so olhava alvos CHAMADOS `DeployToBepInEx`. O alvo `DeployToScripts` do
    ReloadProbe escrevia no perfil com outro nome e a guarda nem o via.

Este teste cobra a guarda nova (`tools/check_deploy_optin.py`, lida como XML) contra a
fixture `<nome>.entrada.json`: cada caso traz um .csproj e o veredito esperado. A
fixture TEM os dois lados do furo A e os dois do furo B — reprovar so um lado provaria
metade.

Alem do modulo, o teste roda a guarda pela LINEA DE COMANDO (o caminho que o
release-check de fato usa) e cobra o exit code: 0 para "todos com opt-in", 1 para
"saiu alvo sem opt-in".
"""
import importlib.util
import os
import subprocess
import sys
import tempfile

import arcabouco as arc

META = {
    "nome": "deploy-optin-guarda",
    "categoria": "pura",
    "requer": [],
    "descricao": ("a guarda do opt-in de deploy aceita o valido e reprova os dois furaos "
                  "(Condition multi-linha e alvo de outro nome)"),
}

# Os casos que ORIGINAM a trava: sem eles a fixture nao prova o que promete.
CASOS_OBRIGATORIOS = (
    "optin_valido_multilinha_condition_linha2",   # furo A: o lado que reprovava VALIDO
    "furoA_multilinha_sem_condition",             # furo A: o lado que PASSAVA defeito
    "furoB_alvo_outro_nome_sem_condition",        # furo B: alvo de outro nome
    "furoB_alvo_outro_nome_com_optin",            # furo B: o alvo certo nao pode reprovar
)


def _guarda():
    caminho = os.path.join(arc.raiz_do_repo(), "tools", "check_deploy_optin.py")
    spec = importlib.util.spec_from_file_location("check_deploy_optin", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo, caminho


def _roda_cli(caminho_guarda, raiz):
    proc = subprocess.run(
        [sys.executable, caminho_guarda, "--raiz", raiz],
        cwd=arc.raiz_do_repo(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        universal_newlines=True, timeout=120,
    )
    return proc.returncode, proc.stdout or ""


def corpo():
    guarda, caminho_guarda = _guarda()
    dados = arc.ler_json("deploy-optin-guarda", "entrada")
    casos = dados.get("casos") or []
    arc.exigir(casos, "a fixture deploy-optin-guarda nao tem casos")

    nomes = [c["nome"] for c in casos]
    arc.igual(len(nomes), len(set(nomes)), "a fixture tem nome de caso repetido")
    for obrig in CASOS_OBRIGATORIOS:
        arc.exigir(obrig in nomes,
                   "a fixture perdeu o caso %r — sem ele um dos furaos fica sem prova" % obrig)

    for caso in casos:
        nome, esperado = caso["nome"], caso["esperado"]
        arc.exigir(esperado in ("aceita", "reprova"),
                   "caso %r: esperado tem de ser 'aceita' ou 'reprova', veio %r" % (nome, esperado))
        with tempfile.TemporaryDirectory(prefix="dep2-caso-") as raiz:
            caminho = os.path.join(raiz, nome + ".csproj")
            with open(caminho, "w", encoding="utf-8") as fh:
                fh.write(caso["xml"])
            achados = guarda.analisa_arquivo(caminho)

        if esperado == "reprova":
            arc.exigir(achados,
                       "a guarda ACEITOU o caso %r (%s) — era para REPROVAR" % (nome, caso["motivo"]))
        else:
            arc.exigir(not achados,
                       "a guarda REPROVOU o caso %r (%s) — era para ACEITAR: %s"
                       % (nome, caso["motivo"], achados))

    # ---- o caminho REAL do release-check: a linha de comando e o exit code --------
    with tempfile.TemporaryDirectory(prefix="dep2-cli-ok-") as raiz:
        with open(os.path.join(raiz, "bom.csproj"), "w", encoding="utf-8") as fh:
            fh.write([c for c in casos if c["nome"] == "optin_valido_linha_unica"][0]["xml"])
        rc, saida = _roda_cli(caminho_guarda, raiz)
        arc.igual(rc, 0, "a guarda pela CLI devia sair 0 com todos os alvos com opt-in (%s)" % saida.strip())

    with tempfile.TemporaryDirectory(prefix="dep2-cli-ruim-") as raiz:
        with open(os.path.join(raiz, "ruim.csproj"), "w", encoding="utf-8") as fh:
            fh.write([c for c in casos if c["nome"] == "furoA_multilinha_sem_condition"][0]["xml"])
        rc, saida = _roda_cli(caminho_guarda, raiz)
        arc.igual(rc, 1, "a guarda pela CLI devia sair 1 com um alvo sem opt-in (%s)" % saida.strip())
        arc.exigir("DeployToBepInEx" in saida,
                   "a reprovacao pela CLI nao nomeou o alvo: %s" % saida.strip())


if __name__ == "__main__":
    arc.main(META, corpo)
