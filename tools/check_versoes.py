#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_versoes.py - PKG-2/PKG-3: a versao dos 6 mods tem de bater nos QUATRO lugares.

POR QUE ESTA FERRAMENTA EXISTE
------------------------------
Sao quatro arquivos que carregam a MESMA versao de um mod:

    <Mod>/<Mod>.csproj   <Version>0.1.0</Version>        <- FONTE (o <Version> manda)
    <Mod>/manifest.json  "version_number": "0.1.0"      <- espelho (Thunderstore)
    <Mod>/Plugin.cs      [BepInPlugin(..., "0.1.0")]    <- espelho (BepInEx, o log)
    <Mod>/README.md      - **Version:** 0.1.0           <- espelho (PKG-3: o usuario le)

Os espelhos DIVERGIREM e o defeito que mais quebra pacote: o Thunderstore recusa
versao ja publicada (o upload falha), e o log do BepInEx passa a mentir sobre qual build
esta carregada - o teste de ciclo roda codigo novo achando que e o velho. So que o
`pack-thunderstore.py` ja conferia isso na hora de EMPACOTAR, no fim do caminho; faltava a
trava que reprova ANTES, so olhando o repositorio (sem build, sem DLL).

O README entrou depois (PKG-3): ele nao e metadado do pacote, e o texto que o usuario le
- ficava fora da trava e podia envelhecer sozinho num bump. Confere-se a linha que os
SEIS READMEs ja usam (`- **Version:** x.y.z`), nao um formato novo.

Este arquivo NAO tem parser proprio: importa `versao_do_csproj`/`versao_do_plugin`/
`versao_do_readme` do `pack-thunderstore.py`, para a definicao de "versao" morar num lugar
so (mesma regra do check_dupes -> check_chave_compartilhada). Assim o gate de release e o
empacotador nunca discordam sobre o que e a versao de um mod.

USO
---
    python tools/check_versoes.py     # 0 = os 6 batem, 1 = DIVERGE, 2 = arquivo/versao faltando

Roda no ritual de release junto dos outros `tools/check_*.py`.
"""
import importlib.util
import io
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


def carregar_empacotador():
    """Importa `pack-thunderstore.py` (tem hifen no nome: nao da `import` normal).

    O modulo so define funcoes/constantes no nivel de cima - a execucao esta toda sob
    `if __name__ == "__main__"` - entao importar nao empacota nem escreve nada.
    """
    caminho = os.path.join(RAIZ, "tools", "pack-thunderstore.py")
    spec = importlib.util.spec_from_file_location("pack_thunderstore", caminho)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def versao_do_manifest(caminho):
    """O `version_number` do manifest.json, cru (sem validar o resto: aqui so a versao)."""
    if not os.path.isfile(caminho):
        return None
    try:
        with io.open(caminho, encoding="utf-8") as fh:
            return json.load(fh).get("version_number")
    except (IOError, ValueError):
        return None


def main():
    pt = carregar_empacotador()
    mods = sorted(pt.descobrir_mods())
    ignorados = pt.projetos_ignorados()

    print("repo : %s" % RAIZ)
    print("mods : %d (%s)" % (len(mods), ", ".join(mods) or "nenhum"))
    if ignorados:
        print("fora : %s (tem csproj mas nao sao mod)" % ", ".join(ignorados))
    print()

    divergentes, sem_versao = [], []
    for nome in mods:
        p = pt.caminhos(nome)
        fonte = pt.versao_do_csproj(p)
        no_manifest = versao_do_manifest(p["manifest"])
        no_plugin, const = pt.versao_do_plugin(nome, p)
        no_readme = pt.versao_do_readme(p)

        # marca DIVERGE so ao lado do valor que nao bate com a fonte
        marca = lambda v: "  <-- DIVERGE" if (fonte and v is not None and v != fonte) else ""
        marca_falta = lambda v: "  <-- FALTANDO" if v is None else ""

        print("%s" % nome)
        print("  %-46s %s%s"
              % ("%s.csproj  <Version>" % nome, fonte or "(ausente)", marca_falta(fonte)))
        print("  %-46s %s%s"
              % ("manifest.json  version_number", no_manifest or "(ausente)",
                 marca(no_manifest) + marca_falta(no_manifest)))
        rotulo = ("Plugin.cs  const %s =" % const) if const else "Plugin.cs  [BepInPlugin(...)]"
        print("  %-46s %s%s"
              % (rotulo, no_plugin or "(ausente)",
                 marca(no_plugin) + marca_falta(no_plugin)))
        print("  %-46s %s%s"
              % ("README.md  - **Version:**", no_readme or "(ausente)",
                 marca(no_readme) + marca_falta(no_readme)))

        if fonte is None or no_plugin is None or no_readme is None:
            sem_versao.append(nome)
        elif (not SEMVER.match(fonte) or no_manifest != fonte
              or no_plugin != fonte or no_readme != fonte):
            divergentes.append(nome)
        print()

    if sem_versao:
        print(">>> %d mod(s) sem versao num lugar obrigatorio: %s"
              % (len(sem_versao), ", ".join(sem_versao)))
        print("    A versao tem de existir no <Version> do .csproj, no Plugin.cs")
        print("    ([BepInPlugin(\"guid\", \"nome\", \"x.y.z\")] ou uma const Version) E no")
        print("    README.md (linha `- **Version:** x.y.z`, a que os READMEs ja usam).")
        return 2

    if divergentes:
        print(">>> VERSAO DIVERGE em %d mod(s): %s" % (len(divergentes), ", ".join(divergentes)))
        print("    O <Version> do .csproj e a FONTE; manifest.json, Plugin.cs e README.md")
        print("    sao ESPELHOS.")
        print("    Conserte a mao o(s) DIVERGE, ou rode de uma vez:")
        print("       python tools/pack-thunderstore.py --sincronizar-versao")
        print("    (pacote com versao errada sai do ar errado, e o log do BepInEx mente.)")
        return 1

    print("  ==> os %d mods batem nos quatro lugares (csproj = manifest = Plugin.cs = README)"
          % len(mods))
    return 0


if __name__ == "__main__":
    sys.exit(main())
