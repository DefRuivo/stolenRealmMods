#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Contra-provas da bancada AUT-3: planta um defeito CONHECIDO numa COPIA
ISOLADA (o sandbox) e exige que o conferidor REPROVE; desfaz e exige que ele
APROVE. Sem isso, um conferidor verde nao prova que ele sabe dizer NAO.

Tudo roda dentro do sandbox (copia descartavel do repo) — nunca no repo real,
nunca no perfil. Cada prova restaura o arquivo original no mesmo instante.

Uso (a partir do orquestrador): aut3_lib + este modulo; ou direto:
    python tools/automacao/offline/contra_provas.py --sandbox <dir>
"""
import argparse
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import aut3_lib  # noqa: E402

PY = sys.executable


def _run(cmd, cwd):
    return aut3_lib.run_cmd(cmd, cwd=cwd, timeout=300)


class Prova:
    """Uma contra-prova: muta => espera reprovar; restaura => espera aprovar."""

    def __init__(self, pid, familia, arquivo_rel, mutar, desmutar, cmd, cwd_rel=None):
        self.id = pid
        self.familia = familia
        self.arquivo_rel = arquivo_rel
        self.mutar = mutar
        self.desmutar = desmutar
        self.cmd = cmd
        self.cwd_rel = cwd_rel

    def executar(self, sandbox):
        alvo = os.path.join(sandbox, self.arquivo_rel) if self.arquivo_rel else None
        original = None
        if alvo and os.path.isfile(alvo):
            with open(alvo, "rb") as fh:
                original = fh.read()
        cwd = os.path.join(sandbox, self.cwd_rel) if self.cwd_rel else sandbox
        try:
            self.mutar(sandbox, alvo)
            com_defeito = _run(self.cmd(), cwd)
            self.desmutar(sandbox, alvo, original)
            apos = _run(self.cmd(), cwd)
        finally:
            if alvo is not None and original is not None:
                with open(alvo, "wb") as fh:
                    fh.write(original)
        exit_defeito = com_defeito["exit_code"]
        exit_apos = apos["exit_code"]
        # A prova so e valida quando o DEFEITO reprova E a correcao aprova.
        ok = (exit_defeito not in (0, None)) and (exit_apos == 0)
        return {
            "id": self.id, "familia": self.familia,
            "arquivo": self.arquivo_rel, "comando": " ".join(self.cmd()),
            "exit_com_defeito": exit_defeito, "exit_apos_correcao": exit_apos,
            "timeout_com_defeito": com_defeito["timeout"],
            "veredito": "PROVA_OK" if ok else "PROVA_FALHOU",
            "detalhe": "" if ok else "defeito nao reprovou (exit=%s) ou correcao nao aprovou (exit=%s)"
                       % (exit_defeito, exit_apos),
        }


# --------------------------------- mutacoes ---------------------------------

def _mut_dupes(sandbox, alvo):
    s = open(alvo, encoding="utf-8").read()
    i = s.index("TextFixes = new Dictionary")
    j = s.index('{ "', i)
    k = s.index("},", j) + 2
    entrada = s[j:k]
    novo = s[:k] + "\n            " + entrada + s[k:]
    open(alvo, "w", encoding="utf-8", newline="").write(novo)


def _desm_dupes(sandbox, alvo, original):
    with open(alvo, "wb") as fh:
        fh.write(original)


def _mut_versoes(sandbox, alvo):
    with open(alvo, encoding="utf-8") as fh:
        m = json.load(fh)
    m["version_number"] = "9.9.9"
    with open(alvo, "w", encoding="utf-8", newline="") as fh:
        json.dump(m, fh, ensure_ascii=False, indent=2)


def _desm_versoes(sandbox, alvo, original):
    with open(alvo, "wb") as fh:
        fh.write(original)


def _mut_patches(sandbox, alvo):
    with open(alvo, "a", encoding="utf-8", newline="") as fh:
        fh.write("\n        private static void SandboxContraProva(ref int __0) { }\n")


def _desm_patches(sandbox, alvo, original):
    with open(alvo, "wb") as fh:
        fh.write(original)


# segredo: nao tem arquivo fixo (cria/remove um arquivo rastreado no sandbox)
def _mut_segredos(sandbox, alvo):
    caminho = os.path.join(sandbox, "SANDBOX-CREDENCIAL-NAO-E-REAL.txt")
    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write("# valor FALSO, plantado so para exercitar a trava (nunca e um token real)\n")
        fh.write("tss_" + "A" * 32 + "\n")
    subprocess.run(["git", "add", "-f", "SANDBOX-CREDENCIAL-NAO-E-REAL.txt"],
                   cwd=sandbox, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _desm_segredos(sandbox, alvo, original):
    caminho = os.path.join(sandbox, "SANDBOX-CREDENCIAL-NAO-E-REAL.txt")
    subprocess.run(["git", "rm", "--cached", "-f", "--quiet", "SANDBOX-CREDENCIAL-NAO-E-REAL.txt"],
                   cwd=sandbox, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.isfile(caminho):
        os.remove(caminho)


CSPROJ_SEM_OPTIN = """<Project Sdk="Microsoft.NET.Sdk">
  <Target Name="DeployToBepInEx" AfterTargets="Build">
    <Copy SourceFiles="$(TargetPath)" DestinationFolder="$(USERPROFILE)\\AppData\\Roaming\\r2modmanPlus-local\\StolenRealm\\profiles\\Default\\BepInEx\\plugins\\X\\" />
  </Target>
</Project>
"""

CSPROJ_COM_OPTIN = """<Project Sdk="Microsoft.NET.Sdk">
  <Target Name="DeployToBepInEx" AfterTargets="Build" Condition="'$(DeployToBepInEx)' == 'true'">
    <Copy SourceFiles="$(TargetPath)" DestinationFolder="$(USERPROFILE)\\AppData\\Roaming\\r2modmanPlus-local\\StolenRealm\\profiles\\Default\\BepInEx\\plugins\\X\\" />
  </Target>
</Project>
"""


def _mut_deploy(sandbox, alvo):
    alvo = os.path.join(sandbox, "sandbox-optin", "Sandbox.Sandbox.csproj")
    os.makedirs(os.path.dirname(alvo), exist_ok=True)
    with open(alvo, "w", encoding="utf-8", newline="") as fh:
        fh.write(CSPROJ_SEM_OPTIN)


def _desm_deploy(sandbox, alvo, original):
    alvo = os.path.join(sandbox, "sandbox-optin", "Sandbox.Sandbox.csproj")
    with open(alvo, "w", encoding="utf-8", newline="") as fh:
        fh.write(CSPROJ_COM_OPTIN)


def provas():
    return [
        Prova("cp_dupes", "chave duplicada (INC-1: derruba o LocalizePatch inteiro)",
              "BetterTooltips/Patches/LocalizePatch.cs", _mut_dupes, _desm_dupes,
              lambda: [PY, "tools/check_dupes.py"]),
        Prova("cp_versoes", "versao divergente (manifest != csproj)",
              "BetterFont/manifest.json", _mut_versoes, _desm_versoes,
              lambda: [PY, "tools/check_versoes.py"]),
        Prova("cp_patches", "parametro posicional do Harmony (__0) sem justificativa",
              "BetterStats/Plugin.cs", _mut_patches, _desm_patches,
              lambda: [PY, "tools/check_patches.py"]),
        Prova("cp_deploy_optin", "alvo de deploy SEM opt-in explicito (escreveria no perfil)",
              None, _mut_deploy, _desm_deploy,
              lambda: [PY, "tools/check_deploy_optin.py", "--raiz",
                       os.path.join(os.environ.get("AUT3_SANDBOX", "."), "sandbox-optin")]),
        Prova("cp_segredos", "credencial plantada em arquivo RASTREADO",
              None, _mut_segredos, _desm_segredos,
              lambda: [PY, "tools/check_segredos.py"]),
    ]


def executar(sandbox):
    os.environ["AUT3_SANDBOX"] = sandbox
    return [p.executar(sandbox) for p in provas()]


def main():
    ap = argparse.ArgumentParser(description="contra-provas isoladas da bancada AUT-3")
    ap.add_argument("--sandbox", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    resultados = executar(args.sandbox)
    if args.json:
        print(json.dumps(resultados, ensure_ascii=False, indent=2))
    else:
        for r in resultados:
            print("[%s] %-16s %s (defeito exit=%s, correcao exit=%s)"
                  % (r["veredito"], r["id"], r["familia"], r["exit_com_defeito"], r["exit_apos_correcao"]))
    ruins = [r for r in resultados if r["veredito"] != "PROVA_OK"]
    return 1 if ruins else 0


if __name__ == "__main__":
    sys.exit(main())
