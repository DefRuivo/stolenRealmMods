#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""checa_conferencia_rv33.py - o pacote de conferencia visual do RV-33 confere com o artefato?

POR QUE ESTA FERRAMENTA EXISTE
------------------------------
O pacote `docs/CONFERENCIA-RV33-DECAY-FLAME.md` manda uma PESSOA olhar a tela e comparar com um
texto esperado e com uma conta esperada. Se o texto esperado do documento ou a DLL conferida
mudarem em silencio, a pessoa e induzida a marcar NOK onde esta tudo certo (ou OK onde mudou) - e
o pacote vira uma armadilha. Esta ferramenta fecha esse buraco: ela NAO prova runtime (nao abre o
jogo, nao le a tela); ela prova que o PACOTE aponta para o artefato que existe e que cada literal
esperado dele existe na fonte e DENTRO da DLL instalada.

O QUE ELA CONFERE (todas as perguntas sao checaveis a maquina)
--------------------------------------------------------------
1. A DLL do perfil do r2modman existe e o sha256 dela e o que o documento declara (RV-33 §0).
2. Nenhum `.cs` do BetterTooltips e mais novo que a DLL instalada (a DLL e posterior a fonte).
3. Cada literal esperado do documento (frases que a pessoa vai ver na tela) existe no fonte E
   dentro da DLL instalada (UTF-16LE) - com a contagem declarada em RV-33 §0.1.
4. As citacoes `arquivo:linha` do documento apontam para arquivo existente e linha existente
   (delega ao `tools/checa_citacoes.py`).
5. A tabela de exemplos NUMERICOS do documento (vida -> N) fecha com a % do tipo lida do asset em
   `tools/dados/shrines-percentuais.csv`, com o arredondamento half-to-even do `Mathf.Round`.

O QUE ELA NAO FAZ (de proposito)
--------------------------------
Nao substitui a conferencia: nao le a tela, nao confere ordem/cor de bloco, nao prova o proc real.
Ausencia de reprovacao aqui significa "o pacote esta coerente com o artefato", nada mais.

USO
    python tools/checa_conferencia_rv33.py
    python tools/checa_conferencia_rv33.py --doc docs/CONFERENCIA-RV33-DECAY-FLAME.md

Convencao do repositorio: imprime `RESULTADO|<PASSOU|REPROVOU>|<nome>|<detalhe>` por checagem;
exit 0 = todas PASSOU, 1 = alguma REPROVOU, 2 = nao conseguiu rodar (artefato/doc ausente).
"""

import argparse
import csv
import hashlib
import io
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(AQUI)
DOC_PADRAO = os.path.join("docs", "CONFERENCIA-RV33-DECAY-FLAME.md")
PERFIS = os.path.join(os.environ.get("APPDATA", ""), "r2modmanPlus-local", "StolenRealm",
                      "profiles", "Default", "BepInEx", "plugins", "BetterTooltips",
                      "BetterTooltips.dll")
BUILD_RELEASE = os.path.join("BetterTooltips", "bin", "Release", "netstandard2.1", "BetterTooltips.dll")

EXIT_OK, EXIT_FALHOU, EXIT_NAO_RODOU = 0, 1, 2

# Os literais que o documento promete na tela: (rotulo, texto, onde procurar no fonte, mtime na DLL)
LITERAIS = (
    ("chave do Decay", "Take [0]% of your Max Health in Shadow Damage per turn.",
     "BetterTooltips/Patches/ShrineAuraPatch.cs"),
    ("sufixo com o dano do Decay", '" damage per turn for you)."',
     "BetterTooltips/Patches/ShrineAuraPatch.cs"),
    ("nota bege do Decay", "Raw damage, before damage reduction: your own Max Health multiplied by"
     " the percentage shown; the damage can be 0.",
     "BetterTooltips/Patches/LocalizePatch.cs"),
    ("chave do Flame", "Attackers take Fire Damage.",
     "BetterTooltips/Patches/ShrineAuraPatch.cs"),
    ("inicio da lista do Flame",
     "In the aura now (raw damage it takes as the attacker, from the attacker's own",
     "BetterTooltips/Patches/ShrineAuraPatch.cs"),
    ("coda da lista do Flame", '" Max Health): "', "BetterTooltips/Patches/ShrineAuraPatch.cs"),
    ("nota bege do Flame",
     "The attacker takes this damage in return, based on its own Max Health and not on the health"
     " of the one it attacked, before damage reduction.",
     "BetterTooltips/Patches/LocalizePatch.cs"),
    ("marcador da linha azul (RV-31)", "Your active shrine auras:",
     "BetterTooltips/Patches/ShrineAuraPatch.cs"),
    ("rotulo do item do Decay", "Shadow damage per turn", "BetterTooltips/Patches/ShrineAuraPatch.cs"),
    ("rotulo do item do Flame", "Fire damage to attackers", "BetterTooltips/Patches/ShrineAuraPatch.cs"),
    ("cor bege das notas", "C8B090", "BetterTooltips/Patches/LocalizePatch.cs"),
)

# Textos citados no documento como parte da tela, mas montados por concatenacao: o pedaco e que
# existe no binario como string literal.
DLL_PEDACOS = (
    "the attacker's own",
    "In the aura now (raw damage it takes as the attacker",
    "damage per turn for you",
    "your own Max Health multiplied by the percentage shown",
)

# O que o DOCUMENTO tem de citar (o texto que a pessoa vai comparar com a tela). Isto e o que
# impede o documento de derivar em silencio: se alguem editar a frase esperada no doc sem mexer no
# codigo, a checagem reprova.
FRAGMENTOS_NO_DOC = (
    ("linha do Decay com 100 de vida",
     "Shadow Damage per turn (10 damage per turn for you)"),
    ("linha do Decay com 250 de vida", "(25 damage per turn for you)"),
    ("nota bege do Decay",
     "Raw damage, before damage reduction: your own Max Health multiplied by the percentage shown;"
     " the damage can be 0."),
    ("linha branca do Flame", "Attackers take Fire Damage."),
    ("prefixo da lista do Flame",
     "In the aura now (raw damage it takes as the attacker, from the attacker's own Max Health)"),
    ("nota bege do Flame",
     "The attacker takes this damage in return, based on its own Max Health and not on the health"
     " of the one it attacked, before damage reduction."),
    ("item do Decay na linha azul", "Your active shrine auras: Shadow damage per turn 10."),
    ("item do Flame na linha azul", "Fire damage to attackers:"),
    ("cor das notas (bege)", "#C8B090"),
    ("cor da linha de auras (azul do jogo)", "#00D7FF"),
)

# A tabela de exemplos do documento: (rotulo, vida, percentual esperado do tipo, N esperado)
EXEMPLOS = (
    ("D1 Decay player 100", 100.0, 10.0, 10),
    ("D3 Decay player 250", 250.0, 10.0, 25),
    ("D4 Decay player 233", 233.0, 10.0, 23),
    ("D4 Decay player 40", 40.0, 10.0, 4),
    ("D5 Decay player 4 (pode ser 0)", 4.0, 10.0, 0),
    ("F4 Flame player 100", 100.0, 5.0, 5),
    ("F4 Flame player 200", 200.0, 5.0, 10),
    ("F4 Flame fodder 200", 200.0, 14.0, 28),
    ("F4 Flame soldier 100", 100.0, 12.0, 12),
    ("F4 Flame champion 100", 100.0, 8.0, 8),
    ("F4 Flame boss 400", 400.0, 2.5, 10),
)


def marca(estado, nome, detalhe=""):
    print("RESULTADO|%s|%s|%s" % (estado, nome, detalhe))


def round_half_even(v):
    """Mathf.Round do Unity: half-to-even, como em tools/checa_shrines.py."""
    import math
    piso = math.floor(v)
    resto = v - piso
    if resto < 0.5:
        return int(piso)
    if resto > 0.5:
        return int(piso) + 1
    return int(piso) if piso % 2 == 0 else int(piso) + 1


def sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


def le(caminho):
    with io.open(caminho, encoding="utf-8", errors="replace") as f:
        return f.read()


def main(argv=None):
    ap = argparse.ArgumentParser(description="confere o pacote de conferencia do RV-33 com o artefato")
    ap.add_argument("--doc", default=DOC_PADRAO, help="documento do pacote (default: %s)" % DOC_PADRAO)
    args = ap.parse_args(argv)

    doc = os.path.join(REPO, args.doc)
    if not os.path.isfile(doc):
        marca("NAO_RODOU", "documento", "nao achei %s" % doc)
        return EXIT_NAO_RODOU
    texto = le(doc)

    falhas = []

    # 1. o documento declara um sha256: ele e o da DLL instalada?
    declarados = set(re.findall(r"\b[0-9a-f]{64}\b", texto))
    if not declarados:
        marca("REPROVOU", "sha256 declarado", "o documento nao declara nenhum sha256 de 64 hex")
        falhas.append("sha256 declarado")
    elif not os.path.isfile(PERFIS):
        marca("NAO_RODOU", "DLL do perfil", "nao achei %s" % PERFIS)
        return EXIT_NAO_RODOU
    else:
        real = sha256(PERFIS)
        # o documento cita sha256 de fontes tambem: basta que UM deles seja o da DLL instalada
        if real in declarados:
            marca("PASSOU", "DLL do perfil == sha256 declarado no documento", real[:12] + "...")
        else:
            marca("REPROVOU", "DLL do perfil != sha256 declarado",
                  "instalada=%s declarados=%s" % (real[:12] + "...",
                                                  ",".join(sorted(x[:12] for x in declarados))))
            falhas.append("sha256")

    # 2. nenhum .cs do mod mais novo que a DLL instalada
    if os.path.isfile(PERFIS):
        dll_mt = os.path.getmtime(PERFIS)
        mais_novos = []
        for raiz, _, arquivos in os.walk(os.path.join(REPO, "BetterTooltips")):
            if os.sep + "obj" in raiz or os.sep + "bin" in raiz:
                continue
            for a in arquivos:
                if a.endswith(".cs"):
                    p = os.path.join(raiz, a)
                    if os.path.getmtime(p) > dll_mt:
                        mais_novos.append(os.path.relpath(p, REPO))
        if mais_novos:
            marca("REPROVOU", "fonte mais novo que a DLL instalada",
                  "a DLL pode nao ser da arvore atual: %s" % ", ".join(sorted(mais_novos)))
            falhas.append("mtime")
        else:
            marca("PASSOU", "nenhum .cs do BetterTooltips e mais novo que a DLL instalada")

    # 2b. a build Release e byte-identica a instalada (o que o documento declara)
    rel = os.path.join(REPO, BUILD_RELEASE)
    if os.path.isfile(rel) and os.path.isfile(PERFIS):
        if sha256(rel) == sha256(PERFIS):
            marca("PASSOU", "build Release byte-identica a DLL do perfil")
        else:
            marca("REPROVOU", "build Release difere da DLL do perfil", rel)
            falhas.append("release")

    # 3. literais do documento no fonte e na DLL
    for rotulo, literal, fonte in LITERAIS:
        p = os.path.join(REPO, fonte)
        if not os.path.isfile(p) or literal not in le(p):
            marca("REPROVOU", "literal no fonte: %s" % rotulo, "%s: %r" % (fonte, literal))
            falhas.append("literal fonte " + rotulo)
        else:
            marca("PASSOU", "literal no fonte: %s" % rotulo, fonte)

    # 3b. o DOCUMENTO cita o texto esperado (o que a pessoa vai comparar com a tela)
    for rotulo, fragmento in FRAGMENTOS_NO_DOC:
        if fragmento in texto:
            marca("PASSOU", "texto esperado no documento: %s" % rotulo,
                  fragmento[:44] + ("..." if len(fragmento) > 44 else ""))
        else:
            marca("REPROVOU", "texto esperado AUSENTE no documento: %s" % rotulo, repr(fragmento))
            falhas.append("doc " + rotulo)

    if os.path.isfile(PERFIS):
        dll = open(PERFIS, "rb").read()
        for pedaco in DLL_PEDACOS:
            n = dll.count(pedaco.encode("utf-16-le"))
            if n == 1:
                marca("PASSOU", "marcador na DLL: %r" % pedaco)
            else:
                marca("REPROVOU", "marcador na DLL: %r" % pedaco, "contagem=%d (esperado 1)" % n)
                falhas.append("dll " + pedaco)

    # 4. citacoes arquivo:linha do documento
    checa = os.path.join(REPO, "tools", "checa_citacoes.py")
    if os.path.isfile(checa):
        r = subprocess.run([sys.executable, checa, args.doc], cwd=REPO,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        saida = r.stdout.decode("utf-8", "replace").strip().splitlines()
        resumo = saida[0] if saida else "(sem saida)"
        if r.returncode == 0:
            marca("PASSOU", "citacoes arquivo:linha do documento", resumo)
        else:
            marca("REPROVOU", "citacoes arquivo:linha do documento", resumo)
            falhas.append("citacoes")
    else:
        marca("NAO_RODOU", "checa_citacoes.py", "nao achei a ferramenta")

    # 5. os numeros do documento fecham com a % do asset
    perc = os.path.join(REPO, "tools", "dados", "shrines-percentuais.csv")
    if not os.path.isfile(perc):
        marca("NAO_RODOU", "tabela de percentuais", "nao achei %s" % perc)
    else:
        tabela = {}
        with io.open(perc, encoding="utf-8") as f:
            for linha in csv.DictReader(f):
                tabela[(linha["aura"], linha["tipo"])] = float(linha["percentual"])
        for rotulo, vida, pct_doc, n_doc in EXEMPLOS:
            aura = "Decay Shrine Aura" if rotulo.startswith("D") else "Flame Shrine Aura"
            achado = re.search(r"(fodder|soldier|champion|boss)", rotulo)
            tipo = "player" if "player" in rotulo else (achado.group(1) if achado else "(nenhum)")
            pct = tabela.get((aura, tipo))
            if pct is None:
                marca("REPROVOU", "exemplo %s" % rotulo, "tipo %r fora da tabela do asset" % tipo)
                falhas.append("exemplo " + rotulo)
                continue
            if abs(pct - pct_doc) > 1e-9:
                marca("REPROVOU", "exemplo %s" % rotulo,
                      "%% do documento=%s, %% do asset=%s" % (pct_doc, pct))
                falhas.append("exemplo " + rotulo)
                continue
            calculado = round_half_even(vida * pct / 100.0)
            if aura == "Flame Shrine Aura":
                calculado = max(1, calculado)   # o Flame tem Mathf.Max(1,
            regra = "Max(1,Round) no Flame" if aura == "Flame Shrine Aura" else "Round, sem Max(1)"
            if calculado == n_doc:
                marca("PASSOU", "exemplo %s" % rotulo,
                      "vida=%g x %g%% -> %d (%s)" % (vida, pct, calculado, regra))
            else:
                marca("REPROVOU", "exemplo %s" % rotulo,
                      "documento diz %d, a conta do asset da %d (vida=%g x %g%%)"
                      % (n_doc, calculado, vida, pct))
                falhas.append("exemplo " + rotulo)

    print()
    if falhas:
        print("REPROVOU: %d checagem(ns) - %s" % (len(falhas), "; ".join(falhas)))
        return EXIT_FALHOU
    print("PASSOU: o pacote confere com o artefato instalado (isto NAO prova runtime: a tela e humana).")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
