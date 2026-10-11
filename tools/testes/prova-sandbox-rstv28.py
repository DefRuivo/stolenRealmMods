#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RSTV-29 - bancada reproduzivel da CONTRA-PROVA da AUSENCIA da superficie Select Party.

NAO e' teste da suite (nome sem `t_`/`cp_`: o runner ignora e CONTA) — e' a bancada que produz a
evidencia "vermelho -> verde" da remocao.

O que ela faz, do zero:
  1. COPIA um mini-repo para um SANDBOX FORA do repo (raiz com `docs/PLANO-DE-TESTES.md`, TODOS os
     .cs do mod e `tools/testes/`): e' o sandbox que o `arcabouco.raiz_do_repo` acha, entao o runner
     roda contra a COPIA — o repo NAO e' tocado em momento nenhum;
  2. roda o teste da suite (`t_rstv28_tela_select_party.py`) na copia -> tem de PASSAR (exit 0);
  3. PLANTA de volta, UM POR VEZ, cada pedaco da superficie removida na copia FORA do repo:
       (a) a chamada `SelectPartyButton.Ensure(__instance);` em `Patches.cs`;
       (b) o arquivo/classe `SelectPartyButton.cs`;
       (c) o gancho da TELA na FORMA POR STRING com classe de nome NEUTRO
           (`[HarmonyPatch(typeof(CharacterChoiceManager), "OpenWindow", ...)]`) — a ESCAPATORIA que a
           checagem antiga deixava passar e que a RSTV-29F (achado C) passou a pegar;
     em TODOS tem de dar REPROVOU (exit 1), restaurando byte a byte (sha256 conferido) entre as
     rodadas;
  4. confere que os arquivos do REPO continuam com o mesmo sha256 do inicio.

Uso:  python tools/testes/prova-sandbox-rstv28.py [--sandbox CAMINHO]
Exit: 0 = PROVA OK | 1 = PROVA FALHOU | 2 = nao consegui montar o sandbox
"""
import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ_REPO = os.path.dirname(os.path.dirname(AQUI))          # tools/testes -> raiz
sys.path.insert(0, AQUI)

import regras_rstv28 as reg  # noqa: E402  (usa o mesmo plantio da regra)

TESTE = "tools/testes/testes/puros/t_rstv28_tela_select_party.py"
PASTA_MOD = "RoguelikeSkillTreeVisualizer"

# Sandbox fora do repo: $TMPDIR (o scratch do Hermes) quando existir, senao o temp do sistema.
SCRATCH = os.environ.get("TMPDIR") or tempfile.gettempdir()


def sha(caminho):
    with open(caminho, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def fontes_do_mod(raiz):
    """{nome: sha256} dos .cs do mod em `raiz` (existencia + conteudo)."""
    pasta = os.path.join(raiz, PASTA_MOD)
    achados = {}
    for nome in sorted(os.listdir(pasta)):
        if nome.endswith(".cs"):
            achados[nome] = sha(os.path.join(pasta, nome))
    return achados


def monta_sandbox(destino):
    """Mini-repo: docs/PLANO-DE-TESTES.md + TODOS os .cs do mod + tools/testes inteiro."""
    if os.path.isdir(destino):
        shutil.rmtree(destino)
    os.makedirs(os.path.join(destino, "docs"))
    os.makedirs(os.path.join(destino, PASTA_MOD))
    shutil.copyfile(os.path.join(RAIZ_REPO, "docs", "PLANO-DE-TESTES.md"),
                    os.path.join(destino, "docs", "PLANO-DE-TESTES.md"))
    for nome in sorted(os.listdir(os.path.join(RAIZ_REPO, PASTA_MOD))):
        if nome.endswith(".cs"):
            shutil.copyfile(os.path.join(RAIZ_REPO, PASTA_MOD, nome),
                            os.path.join(destino, PASTA_MOD, nome))
    shutil.copytree(os.path.join(RAIZ_REPO, "tools", "testes"),
                    os.path.join(destino, "tools", "testes"),
                    ignore=shutil.ignore_patterns("__pycache__"))
    return destino


def roda_teste(sandbox):
    r = subprocess.run([sys.executable, "tools/testes/roda_testes.py", "--teste", TESTE],
                       cwd=sandbox, capture_output=True, text=True, encoding="utf-8")
    saida = (r.stdout or "") + (r.stderr or "")
    linhas = [l.strip() for l in saida.splitlines() if "PASSOU" in l or "REPROVOU" in l]
    return r.returncode, linhas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sandbox", default=os.path.join(SCRATCH, "rstv29-sandbox"))
    args = ap.parse_args()

    sandbox = monta_sandbox(os.path.abspath(args.sandbox))
    mod = os.path.join(sandbox, PASTA_MOD)
    patches = os.path.join(mod, "Patches.cs")
    botao = os.path.join(mod, reg.ARQUIVO_REMOVIDO)
    guarda = os.path.join(sandbox, "_restore")
    os.makedirs(guarda, exist_ok=True)
    shutil.copyfile(patches, os.path.join(guarda, "Patches.cs"))

    print("RSTV-29 - CONTRA-PROVA DA AUSENCIA (sandbox FORA do repo)")
    print("repo (NAO e' tocado): %s" % RAIZ_REPO)
    print("sandbox:              %s" % sandbox)
    print("teste:                %s" % TESTE)
    print()

    sha_repo_antes = fontes_do_mod(RAIZ_REPO)

    print("[FONTE DE VERDADE] a copia SEM a superficie, no sandbox")
    rc0, linhas0 = roda_teste(sandbox)
    print("  [sem a superficie] exit=%d%s" % (rc0, " (esperado 0)" if rc0 == 0 else " <-- ATENCAO"))
    for l in linhas0[:1]:
        print("      " + l[:220])
    print()

    rodadas = []

    # (a) PLANTA de volta a CHAMADA antiga em Patches.cs (o codigo removido volta a citar a classe).
    antes_p = sha(patches)
    with open(patches, encoding="utf-8") as fh:
        src_p = fh.read()
    defeito_p = reg.com_ensure_de_volta({"Patches.cs": src_p})["Patches.cs"]
    if defeito_p == src_p:
        print("  [(a) chamada de volta] ANCORA NAO ACHADA: o plantio nao mudou o fonte (prova INVALIDA)")
        return 2
    with open(patches, "w", encoding="utf-8", newline="") as fh:
        fh.write(defeito_p)
    rc_a, linhas_a = roda_teste(sandbox)
    shutil.copyfile(os.path.join(guarda, "Patches.cs"), patches)
    restaurado_a = sha(patches) == antes_p
    print("  [(a) a chamada `SelectPartyButton.Ensure` de volta] exit=%d%s"
          % (rc_a, " (esperado 1)" if rc_a == 1 else " <-- ATENCAO"))
    for l in linhas_a[:1]:
        print("      " + l[:220])
    print("      restaurado byte a byte: %s (%s)" % (restaurado_a, sha(patches)[:16]))
    rodadas.append((rc_a, restaurado_a))
    print()

    # (b) PLANTA de volta o ARQUIVO/CLASSE da superficie.
    with open(botao, "w", encoding="utf-8", newline="") as fh:
        fh.write("namespace RoguelikeSkillTreeVisualizer\n{\n"
                 "    internal static class SelectPartyButton { }\n}\n")
    rc_b, linhas_b = roda_teste(sandbox)
    os.remove(botao)
    restaurado_b = not os.path.exists(botao)
    print("  [(b) o arquivo/classe SelectPartyButton de volta] exit=%d%s"
          % (rc_b, " (esperado 1)" if rc_b == 1 else " <-- ATENCAO"))
    for l in linhas_b[:1]:
        print("      " + l[:220])
    print("      arquivo removido de novo: %s" % restaurado_b)
    rodadas.append((rc_b, restaurado_b))
    print()

    # (c) PLANTA o gancho da tela na FORMA POR STRING (classe de patch de nome NEUTRO) — a escapatoria
    #     que a checagem por `nameof(...)` deixava passar. Tem de REPROVAR pela propriedade nova.
    antes_p = sha(patches)
    with open(patches, encoding="utf-8") as fh:
        src_p = fh.read()
    defeito_p = reg.com_hook_string_de_volta({"Patches.cs": src_p})["Patches.cs"]
    if defeito_p == src_p:
        print("  [(c) gancho por STRING de volta] ANCORA NAO ACHADA: o plantio nao mudou o fonte "
              "(prova INVALIDA)")
        return 2
    with open(patches, "w", encoding="utf-8", newline="") as fh:
        fh.write(defeito_p)
    rc_c, linhas_c = roda_teste(sandbox)
    shutil.copyfile(os.path.join(guarda, "Patches.cs"), patches)
    restaurado_c = sha(patches) == antes_p
    print("  [(c) o gancho da tela por STRING (classe neutra) de volta] exit=%d%s"
          % (rc_c, " (esperado 1)" if rc_c == 1 else " <-- ATENCAO"))
    for l in linhas_c[:1]:
        print("      " + l[:220])
    print("      restaurado byte a byte: %s (%s)" % (restaurado_c, sha(patches)[:16]))
    rodadas.append((rc_c, restaurado_c))
    print()

    sha_repo_depois = fontes_do_mod(RAIZ_REPO)
    intacto = sha_repo_antes == sha_repo_depois
    print("[REPO INTACTO] %s (%d .cs conferidos por sha256)" % (intacto, len(sha_repo_depois)))
    for nome, h in sorted(sha_repo_depois.items()):
        print("  %s %s" % (h[:16], nome))
    print()

    ok = (rc0 == 0 and all(rc == 1 and rest for rc, rest in rodadas) and intacto)
    if ok:
        print("VEREDITO: PROVA OK - sem a superficie PASSA (exit 0); a CHAMADA antiga, o ARQUIVO "
              "antigo e o GANCHO DA TELA por STRING (classe neutra), plantados na copia FORA do repo, "
              "REPROVAM (exit 1); cada um restaurado byte a byte; o repo nao foi tocado.")
        return 0
    print("VEREDITO: PROVA FALHOU - ver as rodadas acima.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
