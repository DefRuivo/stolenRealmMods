#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gera_shrines_esperado.py - CHK-1: GERA (nao digita) a tabela de valores esperados dos shrines.

POR QUE ESTA FERRAMENTA EXISTE
------------------------------
A conferencia dos shrines (RV-35..RV-46) era manual: o dono entrava em partida, lia o numero na
tooltip e transcrevia para comparar com uma tabela calculada a mao. Transcricao humana erra
(a linha do Flame nasceu com o sujeito errado e so foi pega porque alguem mediu em jogo) e nao
deixa rastro. Aqui a tabela de ESPERADOS deixa de ser digitada: ela e DERIVADA da fonte da
verdade do repositorio e cada base sai com a citacao `arquivo:linha` (ou `assets@offset`) de onde
foi lida. O arquivo gerado (`tools/dados/*.csv`) e versionado e o conferidor
(`tools/checa_shrines.py`) compara SO contra ele.

REGRA DE OURO DESTE GERADOR: se uma base NAO tem fonte, ele FALHA (exit 1) dizendo qual aura e o
que procurou. Ele NUNCA chuta um numero, nunca usa um valor "conhecido de cor" e nunca cai num
default silencioso. Um gerador que inventa e pior que nenhum: a tabela errada vira aprovacao de
um mod errado.

FONTES (todas no repositorio ou no install do jogo - nenhuma "de cabeca"):
  A) `docs/cobertura/status.csv` - censo do dump de boot do RoguelikeDebugger. A coluna `efeitos`
     traz a EXPRESSAO REAL do status do jogo, ex.:
       Warrior Aura, ...,"DamageMod:Base:Mathf.Round(20 * (1 + (Target[\"ShrineEffectBonus\"] / 100)))", ...
     De la saem a BASE e o ATRIBUTO das 9 auras de buff (Warrior, Guardian, Conqueror, Rogue,
     Reaper, Seraph, Shaman, Energy, Fury). Citacao: `docs/cobertura/status.csv:<linha>`.
  B) `resources.assets` do install (1,7 GB) - para as 3 auras que o censo NAO le (o `efeitos` delas
     e VAZIO de proposito: Dwarven nao expoe efeito e Decay/Flame usam `Source`, RV-19 §5):
       - Dwarven Aura / `Dwarven Totem Aura Status`: `Mathf.Round(20 * (1 + (Target[...] / 100)))`
         (ASCII dentro do status; RV-19 §8: offsets +340 e +592 em @1517115056).
       - Decay Shrine Aura: `Mathf.Round(10 * (1 + (Source[...] / 100)))` (ASCII; status @1517113960).
       - Flame Shrine Aura: `Mathf.Round(5 * (1 + (Source[...] / 100)))` (ASCII; status @1517120720).
  C) `resources.assets`, ACAO `Decay Aura Proc` / `Flame Aura Proc` - a formula do DANO com a % por
     TIPO DE INIMIGO (`GetValueByEnemyType(boss, champion, elite, soldier, fodder, player)`; a ordem
     dos 6 parametros e a assinatura real, RV-19 §4.3). Serializadas em UTF-16LE pelo Odin
     (armadilha documentada em RV-19 §1: um grep ASCII nao acha nada dessas formulas).

SAIDA (versionada; NUNCA editar a mao - rodar de novo):
  * tools/dados/shrines-esperado.csv    - 1 linha por (aura, atributo, caso de bonus). Colunas:
      aura,atributo,tipo,base,fonte_base,caso_bonus,contribuicao_esperada,total_esperado,
      resto_esperado,fonte_total
    `contribuicao_esperada` sai SEMPRE da base citada em `fonte_base`. `total_esperado` /
    `resto_esperado` so saem preenchidos nos casos que o repositorio PROVA em jogo (os prints do
    dono em RV-19 §9.1/§10.5: Fury bonus 0 e 100, Rogue bonus 100); nos demais o total depende do
    equipamento do personagem e o campo fica VAZIO - total nao se inventa (a fonte vai em
    `fonte_total`).
  * tools/dados/shrines-percentuais.csv - % por tipo de inimigo do Decay e do Flame (fonte C).

USO
---
    python tools/gera_shrines_esperado.py                 # descobre o resources.assets sozinho
    python tools/gera_shrines_esperado.py --asset C:/.../resources.assets
    python tools/gera_shrines_esperado.py --check         # nao escreve; falha se algo mudou

Exit codes: 0 = tabela gerada (ou `--check` sem diferenca); 1 = fonte ausente/invalida (FALHA);
            2 = nao conseguiu verificar (arquivo do repositorio ausente).

LIMITES (o que este gerador NAO prova)
--------------------------------------
1. Ele le a BASE da EXPRESSAO, nao o valor que o jogo exibiu. A prova de que o calculo do motor
   bate com `Round(BASE * (1 + bonus/100))` e a conferencia de `tools/checa_shrines.py`.
2. O `Round` implementado aqui e o half-to-even do `Mathf.Round` do Unity (o mesmo do motor).
   Se o jogo trocar a funcao de arredondamento, a tabela fica errada e o conferidor acusa ACHADO.
3. `total_esperado` so existe onde ha print do dono no repositorio. Os demais totais dependem do
   personagem e NAO sao gerados (o conferidor cobra so a parcela das auras e a aditividade).
4. Nada aqui olha o texto que o jogador ve: a leitura visual final continua sendo do dono.
"""

import argparse
import csv
import io
import math
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATUS_CSV = os.path.join(RAIZ, "docs", "cobertura", "status.csv")
SAIDA_ESPERADO = os.path.join(RAIZ, "tools", "dados", "shrines-esperado.csv")
SAIDA_PERCENTUAIS = os.path.join(RAIZ, "tools", "dados", "shrines-percentuais.csv")
RV19 = "docs/cobertura/revisao/RV-19-shrines.md"

# Ordem oficial dos parametros de `Character.GetValueByEnemyType` (decompilado l.38351; RV-19 §4.3).
ORDEM_TIPOS = ["boss", "champion", "elite", "soldier", "fodder", "player"]

# Candidatos de install do jogo (o primeiro que existir e usado). Tambem pode vir por `--asset`;
# sem nenhum deles o gerador FALHA em vez de gerar tabela sem fonte.
CANDIDATOS_ASSET = [
    r"E:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/resources.assets",
    r"C:/Program Files (x86)/Steam/steamapps/common/Stolen Realm/Stolen Realm_Data/resources.assets",
    r"D:/SteamLibrary/steamapps/common/Stolen Realm/Stolen Realm_Data/resources.assets",
    os.path.expanduser("~/.steam/steam/steamapps/common/Stolen Realm/Stolen Realm_Data/resources.assets"),
]

# 9 auras de BUFF cuja base mora no censo (docs/cobertura/status.csv, coluna `efeitos`).
# O `Fury` tem DOIS efeitos (DamageMod +25 e DamageReduction -25) na MESMA linha do censo.
AURAS_CSV = [
    "Warrior Aura", "Guardian Aura", "Conqueror Aura", "Rogue Aura", "Reaper Aura",
    "Seraph Aura", "Shaman Aura", "Energy Aura", "Fury",
]

# 3 auras cuja base NAO esta no censo (coluna `efeitos` vazia) - lidas do asset.
# (nome, tipo, janela documentada (ini, fim) em RV-19 §8, nota)
AURAS_ASSET = [
    ("Dwarven Aura", "buff", (1517115056, 1517117400), "stun: nao ha atributo de personagem para ler"),
    ("Decay Shrine Aura", "perigo", (1517113960, 1517116000), "dano por turno (acao `Decay Aura Proc`)"),
    ("Flame Shrine Aura", "perigo", (1517120720, 1517123000), "dano de retalicao (acao `Flame Aura Proc`)"),
]

# Acoes com a formula do dano no campo `Effects[0].Action` (janela UTF-16, RV-19 §8).
ACOES = [
    ("Decay Aura Proc", "ShadowDamage", "Decay Shrine Aura", (1519519282, 1519520400)),
    ("Flame Aura Proc", "FireDamage", "Flame Shrine Aura", (1519546098, 1519547400)),
]

# Casos de bonus exigidos (Omnism II substitui Omnism I: 8 -> 20, RV-19 §3).
CASOS = [("0", 0.0), ("20", 20.0), ("100", 100.0)]

# Casos de ACEITE com total provado em jogo (prints do dono, RV-19 §9.1/§10.5). O `resto` e o
# pedaco da ficha que nao e aura (total - contribuicao) - e ele que prova a aditividade.
# GRANDEZA: valores CRUS do atributo (a mesma que o motor soma e que o comparador usa). No
# `DamageReduction` o TEXTO da tela mostra o sinal invertido (`total +5%` = atributo -5) - RV-19 §9.1.
ACEITES = {
    ("Fury", "DamageMod", "0"): (50.0, 25.0, 486),
    ("Fury", "DamageReduction", "0"): (-5.0, 20.0, 486),
    ("Fury", "DamageMod", "100"): (75.0, 25.0, 487),
    ("Fury", "DamageReduction", "100"): (-30.0, 20.0, 487),
    ("Rogue Aura", "DodgeChance", "100"): (57.0, 17.0, 488),
}

RE_FORMULA_CSV = re.compile(
    r"Mathf\.Round\(\s*(-?[0-9]+(?:\.[0-9]+)?)\s*\*\s*\(1\s*\+\s*\("
    r"(Target|Source)\[\"ShrineEffectBonus\"\]\s*/\s*100\)\)\)")

RE_FORMULA_STATUS = re.compile(
    r"Mathf\.Round\((-?[0-9]+(?:\.[0-9]+)?) \* \(1 \+ \((Target|Source)\["
    r"\"ShrineEffectBonus\"\] / 100\)\)\)")

RE_FORMULA_ACAO = re.compile(
    r"TargetStored\[\"(Shadow|Fire)Damage\"\] = (Mathf\.Max\(1,\s+)?Mathf\.Round\(\(Target\[\"MaxHealth\"\]"
    r" \* Target\.GetValueByEnemyType\(([^)]*)\)\) \* \(1 \+ \(Source\[\"ShrineEffectBonus\"\] / 100\)")


def round_half_even(v):
    """O `Mathf.Round` do Unity: arredonda .5 para o par mais proximo (half-to-even)."""
    f = math.floor(v)
    dif = v - f
    if dif > 0.5:
        return f + 1
    if dif < 0.5:
        return f
    return f if f % 2 == 0 else f + 1


def esperado(base, bonus):
    """Round(BASE * (1 + bonus/100)) - a regra geral das auras (RV-19 §0/§2.2)."""
    return float(round_half_even(base * (1.0 + bonus / 100.0)))


def procura_asset():
    for p in CANDIDATOS_ASSET:
        if os.path.isfile(p):
            return p
    return None


def ler_janela(asset, ini, fim):
    with open(asset, "rb") as f:
        f.seek(ini)
        return f.read(fim - ini)


def bases_do_censo(aura, caminho_csv=None):
    """[(atributo, base, eixo, citacao)] de cada efeito da aura no censo."""
    caminho = caminho_csv or STATUS_CSV
    with open(caminho, newline="", encoding="utf-8") as f:
        leitor = csv.reader(f)
        cabecalho = next(leitor)
        i_nome = cabecalho.index("nome")
        i_efeitos = cabecalho.index("efeitos")
        for row in leitor:
            if len(row) <= max(i_nome, i_efeitos) or row[i_nome] != aura:
                continue
            linha = leitor.line_num
            achados = []
            for parte in row[i_efeitos].split(", "):
                parte = parte.strip()
                if not parte:
                    continue
                if parte.count(":") < 2:
                    raise SystemExit(
                        "FALHA: a aura '%s' tem um efeito fora da forma `atributo:metodo:expressao`: %r "
                        "(docs/cobertura/status.csv:%d)" % (aura, parte, linha))
                atributo, metodo, expr = parte.split(":", 2)
                m = RE_FORMULA_CSV.search(expr)
                if not m:
                    raise SystemExit(
                        "FALHA: o efeito '%s' de '%s' nao esta na forma "
                        "`Mathf.Round(BASE * (1 + (X[\"ShrineEffectBonus\"] / 100)))`: %r "
                        "(docs/cobertura/status.csv:%d)\n"
                        "  -> o gerador NAO chuta: corrija a fonte ou a forma esperada."
                        % (metodo, aura, expr, linha))
                achados.append((atributo, float(m.group(1)), m.group(2),
                                "docs/cobertura/status.csv:%d" % linha))
            if not achados:
                raise SystemExit(
                    "FALHA: a aura '%s' esta em AURAS_CSV mas a coluna `efeitos` do censo esta VAZIA na "
                    "linha %d (docs/cobertura/status.csv) - a FONTE MUDOU. O censo e a fonte da base das 9 "
                    "auras de buff; o gerador FALHA em vez de chutar (se a coluna vazia for o novo normal "
                    "dessa aura, ela passa a ser lida do asset: AURAS_ASSET)." % (aura, linha))
            return achados
    raise SystemExit("FALHA: a aura '%s' NAO esta em %s - o gerador NAO chuta a base."
                     % (aura, caminho))


def bases_do_asset(asset, aura, janela):
    """Le a base da EXPRESSAO do status dentro da janela documentada (status em ASCII/UTF-8)."""
    if not asset:
        raise SystemExit(
            "FALHA: a base de '%s' mora no resources.assets (o censo nao le esse campo) e nenhum install "
            "foi encontrado. Passe --asset <caminho do resources.assets>.\n"
            "  -> sem a fonte, o gerador FALHA em vez de chutar." % aura)
    ini, fim = janela
    bruto = ler_janela(asset, ini, fim)
    pos = bruto.find(b"Mathf.Round(")
    vistos = 0
    while pos >= 0:
        vistos += 1
        txt = bruto[pos:pos + 120].split(b"\x00", 1)[0].decode("latin-1", errors="replace")
        m = RE_FORMULA_STATUS.search(txt)
        if m:
            return float(m.group(1)), m.group(2), "resources.assets@%d" % (ini + pos)
        pos = bruto.find(b"Mathf.Round(", pos + 1)
    raise SystemExit(
        "FALHA: a base de '%s' NAO foi encontrada em resources.assets na janela documentada (%d..%d, "
        "RV-19 §8) [%d ocorrencias de `Mathf.Round(` vistas, nenhuma com o fator]. O install mudou? "
        "-> confira o offset em %s §8 e atualize aqui; o gerador NAO chuta a base."
        % (aura, ini, fim, vistos, RV19))


def percentuais_das_acoes(asset):
    """Le a % por tipo de inimigo do campo `Effects[0].Action` das duas acoes (UTF-16LE)."""
    if not asset:
        raise SystemExit("FALHA: sem resources.assets nao da para ler as acoes (%% por tipo).")
    linhas = []
    for nome_acao, campo, aura, (ini, fim) in ACOES:
        bruto = ler_janela(asset, ini, fim)
        texto = bruto.decode("utf-16-le", errors="replace")
        m = RE_FORMULA_ACAO.search(texto)
        if not m:
            raise SystemExit(
                "FALHA: a acao '%s' nao tem a formula completa "
                "`TargetStored[\"%s\"] = Mathf[.Max(1, ]Round((Target[\"MaxHealth\"] * "
                "Target.GetValueByEnemyType(...)) * (1 + (Source[\"ShrineEffectBonus\"] / 100)))` "
                "na janela documentada (%d..%d). O install mudou? (RV-19 §4.2/§8)."
                % (nome_acao, campo, ini, fim))
        if m.group(1) + "Damage" != campo:
            raise SystemExit(
                "FALHA: a acao '%s' grava em '%sDamage' e o esperado era '%s' - fonte fora do lugar."
                % (nome_acao, m.group(1), campo))
        valores = [float(x.strip().rstrip("fF")) for x in m.group(3).split(",")]
        if len(valores) != len(ORDEM_TIPOS):
            raise SystemExit(
                "FALHA: a acao '%s' tem %d valores e a assinatura tem %d (RV-19 §4.3)."
                % (nome_acao, len(valores), len(ORDEM_TIPOS)))
        # Cada valor com a MESMA citacao do offset do parametro dentro da string (2 bytes por char).
        for tipo, v in zip(ORDEM_TIPOS, valores):
            linhas.append({
                "aura": aura, "acao": nome_acao, "tipo": tipo, "percentual": v * 100.0,
                "fonte": "resources.assets@%d" % (ini + 2 * m.start(3)),
                "minimo1": "sim" if m.group(2) else "nao",
            })
    return linhas


def serializa(cab, linhas):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(cab)
    w.writerows(linhas)
    return buf.getvalue()


def monta_tabelas(asset, caminho_csv=None):
    registros = []
    for aura in AURAS_CSV:
        for atributo, base, eixo, fonte in bases_do_censo(aura, caminho_csv):
            registros.append({"aura": aura, "atributo": atributo, "tipo": "buff", "base": base,
                              "eixo": eixo, "fonte_base": fonte, "nota": ""})
    for aura, tipo, janela, nota in AURAS_ASSET:
        base, eixo, fonte = bases_do_asset(asset, aura, janela)
        registros.append({"aura": aura, "atributo": "", "tipo": tipo, "base": base,
                          "eixo": eixo, "fonte_base": fonte, "nota": nota})

    saida = []
    for r in registros:
        for caso_nome, bonus in CASOS:
            contrib = esperado(r["base"], bonus)
            total = resto = fonte_total = ""
            aceite = ACEITES.get((r["aura"], r["atributo"], caso_nome))
            if aceite:
                total = "%g" % aceite[0]
                resto = "%g" % aceite[1]
                fonte_total = "%s:%d" % (RV19, aceite[2])
            saida.append([r["aura"], r["atributo"], r["tipo"], "%g" % r["base"], r["fonte_base"],
                          caso_nome, "%g" % contrib, total, resto, fonte_total])

    percentuais = percentuais_das_acoes(asset)
    return registros, saida, percentuais


def main(argv=None):
    ap = argparse.ArgumentParser(description="Gera a tabela de esperados dos shrines a partir das fontes.")
    ap.add_argument("--asset", help="caminho do resources.assets (default: autodetecta)")
    ap.add_argument("--status-csv", help="censos alternativo (default: docs/cobertura/status.csv)")
    ap.add_argument("--check", action="store_true",
                    help="nao escreve; falha se a tabela versionada estiver diferente das fontes")
    args = ap.parse_args(argv)

    censo = args.status_csv or STATUS_CSV
    if not os.path.isfile(censo):
        print("FALHA(2): censo ausente: %s" % censo)
        return 2
    asset = args.asset or procura_asset()
    if args.asset and not os.path.isfile(args.asset):
        print("FALHA(1): --asset aponta para um arquivo que NAO existe: %s" % args.asset)
        print("  -> sem a fonte, o gerador FALHA em vez de chutar.")
        return 1

    registros, saida, percentuais = monta_tabelas(asset, censo)

    cab_esperado = ["aura", "atributo", "tipo", "base", "fonte_base", "caso_bonus",
                    "contribuicao_esperada", "total_esperado", "resto_esperado", "fonte_total"]
    cab_perc = ["aura", "acao", "tipo", "percentual", "fonte", "minimo1"]
    txt_esperado = serializa(cab_esperado, saida)
    txt_perc = serializa(cab_perc, [[p["aura"], p["acao"], p["tipo"], "%g" % p["percentual"],
                                     p["fonte"], p["minimo1"]] for p in percentuais])

    if args.check:
        for caminho, novo in ((SAIDA_ESPERADO, txt_esperado), (SAIDA_PERCENTUAIS, txt_perc)):
            if not os.path.isfile(caminho):
                print("FALHA(1): %s nao existe - rode o gerador sem --check." % caminho)
                return 1
            with open(caminho, encoding="utf-8", newline="") as f:
                atual = f.read()
            if atual != novo:
                print("FALHA(1): %s esta DIFERENTE do que as fontes geram agora - rode o gerador."
                      % caminho)
                return 1
        print("OK: a tabela versionada bate com as fontes (%d linhas de esperado, %d percentuais)."
              % (len(saida), len(percentuais)))
        return 0

    os.makedirs(os.path.dirname(SAIDA_ESPERADO), exist_ok=True)
    with open(SAIDA_ESPERADO, "w", encoding="utf-8", newline="") as f:
        f.write(txt_esperado)
    with open(SAIDA_PERCENTUAIS, "w", encoding="utf-8", newline="") as f:
        f.write(txt_perc)

    print("OK: %s (%d linhas) + %s (%d linhas)"
          % (os.path.relpath(SAIDA_ESPERADO, RAIZ), len(saida),
             os.path.relpath(SAIDA_PERCENTUAIS, RAIZ), len(percentuais)))
    print("Fontes das bases:")
    for r in registros:
        print("  %-22s %-22s base=%-5g eixo=%s  <- %s"
              % (r["aura"], r["atributo"] or "(dano)", r["base"], r["eixo"], r["fonte_base"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
