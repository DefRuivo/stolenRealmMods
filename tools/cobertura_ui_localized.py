#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cobertura_ui_localized.py - INSTRUMENTO de cobertura das tabelas do BetterTooltips
medida pelo hook `ui.localized` da API propria (INT-R1-C5 / cartao C6).

O QUE E E O QUE NAO E
---------------------
NAO e um mod, NAO entra no pacote publicado, NAO muda o `BetterTooltips` e NAO faz o
mod depender de `RealmApi`. E uma ferramenta de BANCADA, opt-in: le um arquivo de
OBSERVACAO (pares chave/resultado que o jogo serviu, capturados pelo probe
`tools/automacao/runtime/LocalizedProbe/`) e cruza com:

  * as tabelas do mod  -> `BetterTooltips/Patches/LocalizePatch.cs` (`TextFixes`/`TextAppends`),
    lidas pelo PARSER UNICO do repositorio (`tools/tabelas.py`), nunca por regex novo;
  * o censo            -> `docs/cobertura/*.csv` (skills/status/itens/afixos/powerups/...).

POR QUE O PONTO DE OBSERVACAO E EXATO (e nao "achismo")
-------------------------------------------------------
`OptionsManager.Localize` e ESTATICO, recebe o texto pedido e devolve `string`:
`api/Core/Contracts.cs:63` (hook `ui.localized`) e `api/Hooks/HookInstallation.cs`
(`StringPostfix` -> `RealmHooks.Emit(id, args, __result)`). O par observado e
`(chave = original, resultado = __result)`.

A SEMANTICA DO MOD QUE ISTO USA (lida no fonte, `LocalizePatch.cs:2532-2563`):
o postfix **so age quando o texto exibido e o ingles original**
(`if (__result != original) return;`), procura `original` PRIMEIRO em `TextFixes` e,
se nao achar, em `TextAppends` (if/else if na MESMA chave). Logo:

| observacao                                   | leitura                                    |
|---|---|
| chave SEM entrada na tabela                  | **LACUNA** de cobertura (o mod nao toca)    |
| chave em `TextFixes` e `resultado != chave`  | **COBERTO** (reescrito)                     |
| chave em `TextAppends` e nota presente       | **COBERTO** (nota anexada)                  |
| chave na tabela e `resultado == chave`       | **ENTRADA NAO RODOU** - familia INC-1/INC-2 |

E a ultima linha e o motivo de o instrumento existir: chave errada/morta **falha em
silencio** (o log do jogo so aparece quando muda algo).

A TRAVA (o que o instrumento REPROVA)
-------------------------------------
`--baseline-out` grava o conjunto de chaves que uma observacao PROVOU servidas E
cobertas. `--verificar <baseline>` reprova (exit 1) quando:
  * uma chave do baseline SUMIU da tabela (removeram a entrada -> regressao silenciosa);
  * uma chave do baseline passou a estar nas DUAS tabelas (BUG-32: a de `TextAppends` nunca roda);
  * a tabela onde ela morava mudou (a ordem do if/else if decide qual executa).

Esse e o CASO NEGATIVO obrigatorio do cartao: remover uma entrada real -> REPROVAR.

USO
---
    python tools/cobertura_ui_localized.py --prova
        roda os casos do proprio instrumento e imprime `Ran N tests; failures: K`.
        exit 0 = todos verdes; 1 = algum vermelho.

    python tools/cobertura_ui_localized.py --observacoes <obs.jsonl> \
        [--baseline-out docs/cobertura/revisao/cobertura-ui-localized-baseline.json] \
        [--json <relatorio.json>]
        mede a cobertura e imprime o relatorio (lacunas / chaves mortas / por categoria).

    python tools/cobertura_ui_localized.py --verificar <baseline.json>
        roda a TRAVA. exit 0 = verde; 1 = REPROVADO (violacao listada).

    python tools/cobertura_ui_localized.py --gerar-observacao <saida.jsonl> [--limite N]
        gera uma observacao ROTULADA `FIXTURE` a partir do censo + tabelas reais
        (reproduzivel pelo comando; NUNCA e evidencia de jogo).

    python tools/cobertura_ui_localized.py            # sem argumento
        procura a observacao no caminho padrao. Sem observacao: imprime
        `NAO_EXERCITADO` e sai com exit 2 (nao reprova release: nao ha rodada autorizada).

Exit codes: 0 ok | 1 REPROVADO | 2 NAO_EXERCITADO (falta observacao/rodada).
"""
import argparse
import copy
import csv
import glob
import hashlib
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import tabelas as tab  # noqa: E402  (tools/tabelas.py - o parser UNICO)

TABELAS_ARQ = os.path.join(RAIZ, "BetterTooltips", "Patches", "LocalizePatch.cs")
CENSO_DIR = os.path.join(RAIZ, "docs", "cobertura")
OBS_PADRAO = os.path.join(RAIZ, "docs", "automacao", "runtime", "observacao-ui-localized.jsonl")
BASELINE_PADRAO = os.path.join(CENSO_DIR, "revisao", "cobertura-ui-localized-baseline.json")

NOMES_TABELA = ("TextFixes", "TextAppends")
# (categoria, arquivo do censo). A coluna lida e `descricao` (o texto que o jogo serve).
CATEGORIAS = (
    ("skills", "skills.csv"),
    ("status", "status.csv"),
    ("itens", "itens.csv"),
    ("afixos", "afixos.csv"),
    ("powerups", "powerups.csv"),
    ("acoes", "acoes.csv"),
    ("invocacoes", "invocacoes.csv"),
)
ESQUEMA_OBS = "ui-localized/1"
ESQUEMA_BASELINE = "cobertura-ui-localized/1"


def _utf8():
    """Saida sempre em UTF-8: o console do Windows e cp1252 e mata o relatorio em
    qualquer texto com acento/normalizacao do jogo."""
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def sha256_arquivo(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as fh:
        for bloco in iter(lambda: fh.read(65536), b""):
            h.update(bloco)
    return h.hexdigest()


# ------------------------------- leitura das entradas -----------------------

def carregar_tabelas(caminho=None):
    """{'TextFixes': {chave: valor}, 'TextAppends': {chave: valor}} decodificados.

    Parser UNICO (`tools/tabelas.py`): mesma definicao de entrada que o
    `check_dupes.py` / `check_chave_compartilhada.py` publicam.
    """
    caminho = caminho or TABELAS_ARQ
    if not os.path.isfile(caminho):
        raise IOError("fonte das tabelas nao encontrada: %s" % caminho)
    with open(caminho, encoding="utf-8") as fh:
        fonte = fh.read()
    return {nome: dict(tab.pares(fonte, nome)) for nome in NOMES_TABELA}


def chave_como_no_fonte(chave):
    """A chave como ela aparece no .cs. O parser decodifica `\\n`/`\\"`; para reencontrar
    a mesma entrada no TEXTO do fonte e preciso o inverso (sem tocar em nada mais)."""
    return chave.replace("\\", "\\\\").replace('"', '\\"') if "\\" in chave else chave


def remover_entrada_do_fonte(fonte, nome, chave):
    """Devolve o fonte SEM a entrada `{ chave, valor }` da tabela `nome`.

    Usado SO pelos casos do `--prova` (o caso negativo): remove do TEXTO, no disco-copia,
    exatamente as linhas da entrada - nao mexe no dict em memoria. As entradas reais tem
    o formato `{ "chave",\\n  "valor" },` (chave e valor em linhas proprias).
    """
    alvo = chave_como_no_fonte(chave)
    linhas = fonte.split("\n")
    blocos = None
    for i, linha in enumerate(linhas):
        if ("%s = new Dictionary" % nome) in linha:
            blocos = i
            break
    if blocos is None:
        raise ValueError("tabela %s nao encontrada no fonte" % nome)
    alvo_linha = '"%s"' % alvo
    for i in range(blocos, len(linhas)):
        if alvo_linha in linhas[i]:
            inicio = i - 1 if "{" in linhas[i - 1] else i
            if "{" not in linhas[inicio]:
                inicio = i
            for j in range(inicio, len(linhas)):
                if linhas[j].rstrip().endswith("},") or linhas[j].rstrip().endswith("}"):
                    del linhas[inicio:j + 1]
                    return "\n".join(linhas)
            raise ValueError("nao achei o fim da entrada de %r" % chave)
    raise ValueError("entrada %r nao encontrada em %s" % (chave, nome))


def carregar_censo(diretorio=None):
    """Indice `texto -> {categoria, arquivo}` e contagem por arquivo.

    Le a coluna `descricao` (o texto que o jogo serve). Linhas sem descricao ficam fora.
    """
    diretorio = diretorio or CENSO_DIR
    indice, contagem = {}, {}
    for categoria, arquivo in CATEGORIAS:
        caminho = os.path.join(diretorio, arquivo)
        if not os.path.isfile(caminho):
            continue
        n = 0
        with open(caminho, encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                v = (r.get("descricao") or "").strip()
                if not v:
                    continue
                n += 1
                indice.setdefault(v, {"categoria": categoria, "arquivo": arquivo})
        contagem[arquivo] = n
    return indice, contagem


def carregar_observacoes(caminho):
    """Lista de dicts de um JSONL. Cada linha: {hook, chave, resultado[, sequencia,
    procedencia, sessao, hash_fonte]}. Linha invalida e DEFEITO (levanta)."""
    obs = []
    with open(caminho, encoding="utf-8") as fh:
        for n, linha in enumerate(fh, 1):
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            try:
                r = json.loads(linha)
            except ValueError as e:
                raise ValueError("%s:%d nao e JSON: %s" % (caminho, n, e))
            for campo in ("hook", "chave", "resultado"):
                if not isinstance(r.get(campo), str):
                    raise ValueError("%s:%d sem o campo de texto %r" % (caminho, n, campo))
            if r["hook"] != "ui.localized":
                raise ValueError("%s:%d hook %r != ui.localized" % (caminho, n, r["hook"]))
            obs.append(r)
    return obs


# ------------------------------- a medicao ----------------------------------

def _procedencia(obs):
    vistas = {o.get("procedencia", "NAO_DECLARADA") for o in obs}
    if vistas == {"runtime"}:
        return "runtime"
    if vistas <= {"FIXTURE"}:
        return "FIXTURE"
    return "MISTA:" + ",".join(sorted(vistas))


def analisar(observacoes, tabelas, censo_indice, censo_contagem):
    """Relatorio completo da cobertura. Nao decide nada: mede."""
    fixas, anexos = tabelas["TextFixes"], tabelas["TextAppends"]
    compartilhadas = sorted(set(fixas) & set(anexos))

    rel = {
        "esquema": ESQUEMA_OBS,
        "procedencia": _procedencia(observacoes),
        "observacoes": len(observacoes),
        "chaves_distintas": len({o["chave"] for o in observacoes}),
        "cobertos": [],
        "lacunas": [],
        "nao_aplicados": [],
        "chaves_mortas": [],
        "chaves_compartilhadas": compartilhadas,
        "servidos_fora_da_tabela_conhecidos_no_censo": 0,
        "por_categoria": {},
        "por_arquivo": {},
        "tabelas": {nome: len(d) for nome, d in tabelas.items()},
    }

    vistas = set()
    for o in observacoes:
        chave, resultado = o["chave"], o["resultado"]
        vistas.add(chave)
        cat = censo_indice.get(chave, {"categoria": "fora-do-censo", "arquivo": "(sem arquivo)"})
        linha = {"chave": chave, "categoria": cat["categoria"], "arquivo": cat["arquivo"]}
        if chave in fixas:
            linha["tabela"] = "TextFixes"
            if resultado != chave:
                rel["cobertos"].append(dict(linha, resultado="reescrito"))
            else:
                rel["nao_aplicados"].append(dict(linha, tabela="TextFixes",
                                                 motivo="entrada existe e o jogo serviu o texto CRU"))
        elif chave in anexos:
            linha["tabela"] = "TextAppends"
            if resultado != chave:
                rel["cobertos"].append(dict(linha, resultado="nota-anexada"))
            else:
                rel["nao_aplicados"].append(dict(linha, tabela="TextAppends",
                                                 motivo="entrada existe e o jogo serviu o texto CRU"))
        else:
            rel["lacunas"].append(linha)
            if cat["categoria"] != "fora-do-censo":
                rel["servidos_fora_da_tabela_conhecidos_no_censo"] += 1

    for nome, d in tabelas.items():
        for chave in d:
            if chave not in vistas:
                cat = censo_indice.get(chave, {"categoria": "fora-do-censo", "arquivo": "(sem arquivo)"})
                rel["chaves_mortas"].append({"tabela": nome, "chave": chave,
                                             "categoria": cat["categoria"], "arquivo": cat["arquivo"]})

    # resumo por categoria: so as categorias do censo (a ordenacao segue CATEGORIAS)
    for categoria, _arq in CATEGORIAS:
        rel["por_categoria"][categoria] = {"servidos": 0, "cobertos": 0, "lacunas": 0,
                                           "entradas_na_tabela": 0, "chaves_mortas": 0}
    for r in rel["cobertos"]:
        c = rel["por_categoria"].get(r["categoria"])
        if c:
            c["servidos"] += 1
            c["cobertos"] += 1
    for r in rel["lacunas"]:
        c = rel["por_categoria"].get(r["categoria"])
        if c:
            c["servidos"] += 1
            c["lacunas"] += 1
    for r in rel["chaves_mortas"]:
        c = rel["por_categoria"].get(r["categoria"])
        if c:
            c["chaves_mortas"] += 1
    for nome, d in tabelas.items():
        for chave in d:
            cat = censo_indice.get(chave)
            if cat and cat["categoria"] in rel["por_categoria"]:
                rel["por_categoria"][cat["categoria"]]["entradas_na_tabela"] += 1

    # resumo por ARQUIVO do censo + contagem de entradas do censo (aceite: "por arquivo+contagem")
    for categoria, arquivo in CATEGORIAS:
        rel["por_arquivo"][arquivo] = {"categoria": categoria,
                                       "entradas_no_censo": censo_contagem.get(arquivo, 0),
                                       "servidos": rel["por_categoria"][categoria]["servidos"],
                                       "cobertos": rel["por_categoria"][categoria]["cobertos"],
                                       "lacunas": rel["por_categoria"][categoria]["lacunas"],
                                       "chaves_mortas": rel["por_categoria"][categoria]["chaves_mortas"]}
    return rel


# ------------------------------- a trava ------------------------------------

def construir_baseline(rel, hash_tabelas):
    """Baseline = o que a observacao PROVOU: chave -> tabela onde ela mora."""
    cobrados = {}
    for r in rel["cobertos"]:
        cobrados[r["chave"]] = r["tabela"]
    return {"esquema": ESQUEMA_BASELINE,
            "procedencia": rel["procedencia"],
            "observacoes": rel["observacoes"],
            "sha256_tabelas": hash_tabelas,
            "cobrados": cobrados}


def verificar_baseline(baseline, tabelas):
    """Violacoes do baseline contra as tabelas de HOJE. Lista vazia = verde."""
    fixas, anexos = tabelas["TextFixes"], tabelas["TextAppends"]
    violacoes = []
    for chave, onde in sorted(baseline.get("cobrados", {}).items()):
        if onde not in NOMES_TABELA:
            violacoes.append({"tipo": "baseline-invalido", "chave": chave, "tabela": onde})
            continue
        if chave in fixas and chave in anexos:
            violacoes.append({"tipo": "chave-nas-duas-tabelas", "chave": chave,
                              "tabela": "TextFixes+TextAppends", "esperado": onde})
        elif chave not in fixas and chave not in anexos:
            violacoes.append({"tipo": "entrada-removida", "chave": chave,
                              "tabela": "(ausente)", "esperado": onde})
        elif chave not in (fixas if onde == "TextFixes" else anexos):
            violacoes.append({"tipo": "tabela-trocada", "chave": chave,
                              "tabela": "TextAppends" if onde == "TextFixes" else "TextFixes",
                              "esperado": onde})
    return violacoes


# ------------------------------- relatorio ----------------------------------

def imprimir_relatorio(rel, origem, limite=12):
    print("=" * 78)
    print(" COBERTURA DAS TABELAS DO BetterTooltips via hook ui.localized")
    print(" observacao : %s" % origem)
    print(" procedencia: %s   (FIXTURE nunca e evidencia de jogo)" % rel["procedencia"])
    print("=" * 78)
    print(" linhas observadas .....: %d" % rel["observacoes"])
    print(" chaves distintas ......: %d" % rel["chaves_distintas"])
    print(" entradas na tabela ....: TextFixes=%d  TextAppends=%d" % (
        rel["tabelas"]["TextFixes"], rel["tabelas"]["TextAppends"]))
    print(" COBERTOS (mod agiu) ...: %d" % len(rel["cobertos"]))
    print(" LACUNAS (sem entrada) .: %d" % len(rel["lacunas"]))
    print(" ENTRADAS QUE NAO RODARAM: %d" % len(rel["nao_aplicados"]))
    print(" nUNCA SERVIDAS (mortas).: %d" % len(rel["chaves_mortas"]))
    print(" chave nas DUAS tabelas .: %d %s" % (
        len(rel["chaves_compartilhadas"]), "(BUG-32)" if rel["chaves_compartilhadas"] else ""))
    print()
    print("--- resumo por categoria ----------------------------------------------")
    print(" %-10s %8s %8s %8s %9s" % ("categoria", "servidos", "cobertos", "lacunas", "na tabela"))
    for categoria in [c for c, _a in CATEGORIAS]:
        d = rel["por_categoria"][categoria]
        print(" %-10s %8d %8d %8d %9d" % (categoria, d["servidos"], d["cobertos"],
                                          d["lacunas"], d["entradas_na_tabela"]))
    print()
    print("--- resumo por arquivo (censo) ---------------------------------------")
    print(" %-18s %9s %8s %8s %8s" % ("arquivo", "no censo", "servidos", "cobertos", "lacunas"))
    for _c, arquivo in CATEGORIAS:
        d = rel["por_arquivo"][arquivo]
        print(" %-18s %9d %8d %8d %8d" % (arquivo, d["entradas_no_censo"], d["servidos"],
                                          d["cobertos"], d["lacunas"]))
    for titulo, lista in (("LACUNAS (texto servido SEM entrada na tabela)", rel["lacunas"]),
                          ("ENTRADAS QUE NAO RODARAM (chave na tabela, jogo serviu cru)", rel["nao_aplicados"]),
                          ("NUNCA SERVIDAS (candidata a chave morta)", rel["chaves_mortas"])):
        if not lista:
            continue
        print()
        print("--- %s: %d" % (titulo, len(lista)))
        for r in lista[:limite]:
            print("   [%-11s] %s" % (r.get("tabela", r.get("categoria")), (r["chave"][:88])))
        if len(lista) > limite:
            print("   ... e mais %d (lista completa no JSON)" % (len(lista) - limite))
    print("=" * 78)


# ------------------------------- prova do instrumento -----------------------

FIXTURE_FONTE = '''namespace X
{
    public static class T
    {
        private static readonly Dictionary<string, string> TextFixes = new Dictionary<string, string>
        {
            { "Deals *0 fire damage in a line.",
              "Deals *0 fire damage in a line." },
            { "Striking with this weapon applies 2 stack of Poison.",
              "Striking with this weapon applies 2 stacks of Poison." },
        };
        private static readonly Dictionary<string, string> TextAppends = new Dictionary<string, string>
        {
            { "+ 20% Damage Reduction",
              "\\n<color=#C8B090>Reduces all damage you take.</color>" },
            { "Deals *0 fire damage in a line.",
              "nota que NUNCA roda (BUG-32)" },
        };
    }
}
'''


def _obs(chave, resultado, procedencia="FIXTURE"):
    return {"hook": "ui.localized", "chave": chave, "resultado": resultado,
            "procedencia": procedencia, "sessao": "prova", "sequencia": 1}


def _tabelas_da_fonte(fonte):
    return {nome: dict(tab.pares(fonte, nome)) for nome in NOMES_TABELA}


def _chave_real(indice, nomes=NOMES_TABELA):
    """(chave, tabela, categoria) de uma entrada REAL: existe na tabela E no censo.

    Os casos que checam classificacao por categoria usam chave do produto de verdade -
    chave sintetica nao esta no censo e mediria "fora-do-censo", nao a regra.
    """
    t = carregar_tabelas()
    for nome in nomes:
        for chave in t[nome]:
            if chave in indice:
                return chave, nome, indice[chave]["categoria"]
    raise AssertionError("nenhuma entrada real de %s casou com o censo" % (nomes,))


CASOS = []


def caso(nome):
    def deco(fn):
        CASOS.append((nome, fn))
        return fn
    return deco


@caso("o parser unico le as duas tabelas reais e elas nao estao vazias")
def _c1():
    t = carregar_tabelas()
    assert len(t["TextFixes"]) > 0, "TextFixes vazia"
    assert len(t["TextAppends"]) > 0, "TextAppends vazia"
    assert not (set(t) - set(NOMES_TABELA)), "tabela inesperada"


@caso("caso negativo: REMOVER uma entrada real faz a trava REPROVAR (e so ela)")
def _c2():
    t = carregar_tabelas()
    with open(TABELAS_ARQ, encoding="utf-8") as fh:
        fonte = fh.read()
    # escolhe uma entrada REAL (a que estiver no censo) para remover
    indice, _cont = carregar_censo()
    chave = next(k for k in t["TextFixes"] if k in indice)
    baseline = {"esquema": ESQUEMA_BASELINE, "procedencia": "FIXTURE",
                "cobrados": {chave: "TextFixes"}}
    assert verificar_baseline(baseline, t) == [], "a trava ja reprovava antes de remover"
    fonte_sem = remover_entrada_do_fonte(fonte, "TextFixes", chave)
    t_sem = _tabelas_da_fonte(fonte_sem)
    assert chave not in t_sem["TextFixes"], "a remocao nao tirou a entrada do fonte"
    viol = verificar_baseline(baseline, t_sem)
    assert len(viol) == 1, "esperava 1 violacao, veio %d" % len(viol)
    assert viol[0]["tipo"] == "entrada-removida", "tipo errado: %s" % viol[0]["tipo"]
    # e a metade OK: o MESMO baseline no fonte intacto continua verde
    assert verificar_baseline(baseline, t) == [], "o fonte intacto reprovou (controle positivo quebrado)"


@caso("chave que passa a existir nas DUAS tabelas e reprovada (BUG-32)")
def _c3():
    t = _tabelas_da_fonte(FIXTURE_FONTE)
    assert "Deals *0 fire damage in a line." in t["TextFixes"]
    assert "Deals *0 fire damage in a line." in t["TextAppends"]
    viol = verificar_baseline({"cobrados": {"Deals *0 fire damage in a line.": "TextFixes"}}, t)
    assert len(viol) == 1 and viol[0]["tipo"] == "chave-nas-duas-tabelas", viol


@caso("servido SEM entrada vira LACUNA, com a categoria do censo")
def _c4():
    t = _tabelas_da_fonte(FIXTURE_FONTE)
    indice, contagem = carregar_censo()
    chave = "Striking with this weapon applies 2 stack of Poison."
    texto_sem_entrada = "Some text nobody fixed."
    if texto_sem_entrada in indice:
        texto_sem_entrada = "(texto de prova, fora do censo)"
    rel = analisar([_obs(chave, "Striking with this weapon applies 2 stacks of Poison."),
                    _obs(texto_sem_entrada, texto_sem_entrada)], t, indice, contagem)
    assert len(rel["cobertos"]) == 1, rel["cobertos"]
    assert rel["cobertos"][0]["chave"] == chave
    assert rel["cobertos"][0]["resultado"] == "reescrito"
    assert len(rel["lacunas"]) == 1 and rel["lacunas"][0]["chave"] == texto_sem_entrada
    assert rel["lacunas"][0]["categoria"] == "fora-do-censo"


@caso("chave na tabela servida SEM alteracao e ENTRADA QUE NAO RODOU (familia INC-1)")
def _c5():
    indice, contagem = carregar_censo()
    t = carregar_tabelas()
    chave, tabela, categoria = _chave_real(indice, ("TextFixes", "TextAppends"))
    rel = analisar([_obs(chave, chave)], t, indice, contagem)
    assert rel["cobertos"] == [], "era para nao contar como coberto"
    assert len(rel["nao_aplicados"]) == 1, rel["nao_aplicados"]
    assert rel["nao_aplicados"][0]["tabela"] == tabela
    assert rel["nao_aplicados"][0]["categoria"] == categoria


@caso("entrada da tabela que o jogo NUNCA serviu entra em chaves_mortas")
def _c6():
    t = _tabelas_da_fonte(FIXTURE_FONTE)
    indice, contagem = carregar_censo()
    vivo = "Striking with this weapon applies 2 stack of Poison."
    rel = analisar([_obs(vivo, "Striking with this weapon applies 2 stacks of Poison.")],
                   t, indice, contagem)
    mortas = {r["chave"] for r in rel["chaves_mortas"]}
    assert vivo not in mortas, "a chave servida nao pode aparecer como morta"
    assert "+ 20% Damage Reduction" in mortas, mortas
    assert "Deals *0 fire damage in a line." in {r["chave"] for r in rel["chaves_mortas"]}


@caso("resumo por categoria conta servidos/cobertos/lacunas certo")
def _c7():
    indice, contagem = carregar_censo()
    t = carregar_tabelas()
    kf, _tf, catf = _chave_real(indice, ("TextFixes",))
    ka, _ta, cata = _chave_real(indice, ("TextAppends",))
    rel = analisar([_obs(kf, t["TextFixes"][kf]), _obs(ka, t["TextAppends"][ka])],
                   t, indice, contagem)
    assert rel["por_categoria"][catf]["cobertos"] == 1, rel["por_categoria"][catf]
    assert rel["por_categoria"][cata]["cobertos"] == 1, rel["por_categoria"][cata]
    assert rel["por_categoria"][catf]["lacunas"] == 0
    total_cobertos = sum(d["cobertos"] for d in rel["por_categoria"].values())
    assert total_cobertos == 2, rel["por_categoria"]


@caso("saida por arquivo traz contagem do censo e as contagens da medicao")
def _c8():
    indice, contagem = carregar_censo()
    t = carregar_tabelas()
    rel = analisar([], t, indice, contagem)
    for _c, arquivo in CATEGORIAS:
        d = rel["por_arquivo"][arquivo]
        assert set(("entradas_no_censo", "servidos", "cobertos", "lacunas")) <= set(d), d
    assert rel["por_arquivo"]["skills.csv"]["entradas_no_censo"] == contagem.get("skills.csv", 0)
    assert rel["por_arquivo"]["skills.csv"]["entradas_no_censo"] > 0


@caso("baseline do repo real verifica VERDE com as tabelas de hoje")
def _c9():
    t = carregar_tabelas()
    indice, _cont = carregar_censo()
    chaves = [k for k in list(t["TextFixes"]) if k in indice][:50]
    assert chaves, "nenhuma entrada real casou com o censo"
    base = {"cobrados": {k: "TextFixes" for k in chaves}}
    assert verificar_baseline(base, t) == [], verificar_baseline(base, t)


@caso("observacao valida e JSONL invalido DEFEITO (nao silencio)")
def _c10():
    import tempfile
    ok = os.path.join(tempfile.gettempdir(), "obs-ok-int-r1-c5.jsonl")
    ruim = os.path.join(tempfile.gettempdir(), "obs-ruim-int-r1-c5.jsonl")
    with open(ok, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(_obs("a", "b")) + "\n")
    with open(ruim, "w", encoding="utf-8") as fh:
        fh.write('{"hook": "outro", "chave": "a", "resultado": "b"}\n')
    assert len(carregar_observacoes(ok)) == 1
    try:
        carregar_observacoes(ruim)
    except ValueError as e:
        assert "ui.localized" in str(e), e
        return
    raise AssertionError("observacao com outro hook passou sem erro")


@caso("procedencia e declarada: fixture nao se disfarca de runtime")
def _c11():
    indice, contagem = carregar_censo()
    t = carregar_tabelas()
    assert _procedencia([_obs("a", "b")]) == "FIXTURE"
    assert _procedencia([_obs("a", "b", "runtime")]) == "runtime"
    assert _procedencia([_obs("a", "b"), _obs("a", "b", "runtime")]).startswith("MISTA")
    rel = analisar([_obs("a", "b")], t, indice, contagem)
    assert rel["procedencia"] == "FIXTURE"


def prova(verboso=False):
    falhas = []
    for nome, fn in CASOS:
        try:
            fn()
            if verboso:
                print("  [ ok  ] %s" % nome)
        except Exception as e:  # noqa: BLE001 - a prova tem de reportar QUALQUER falha
            falhas.append((nome, e))
            print("  [FALHA] %s -> %s" % (nome, e))
    total = len(CASOS)
    print()
    print("Ran %d tests; failures: %d" % (total, len(falhas)))
    if falhas:
        print("REPROVADO: %d caso(s) vermelho(s), nomeados acima" % len(falhas))
        return 1
    print("VERDE: todos os casos do instrumento passaram (inclui o caso NEGATIVO: remover uma "
          "entrada real -> a trava reprova; fonte intacto -> verde)")
    return 0


# --------------------------------- CLI --------------------------------------

def gerar_observacao(saida, limite=None, censo_dir=None):
    """Observacao ROTULADA `FIXTURE`, derivada do censo + tabelas reais.

    E fixture, nunca evidencia de jogo: o campo `procedencia` diz isso em cada linha.
    """
    indice, _cont = carregar_censo(censo_dir)
    t = carregar_tabelas()
    linhas, n = [], 0
    for nome, tabela in t.items():
        for chave, valor in tabela.items():
            if chave not in indice:
                continue
            if limite and n >= limite:
                break
            n += 1
            linhas.append({"hook": "ui.localized", "sequencia": n, "chave": chave,
                           "resultado": valor, "procedencia": "FIXTURE",
                           "sessao": "fixture-do-censo",
                           "fonte": "tools/cobertura_ui_localized.py --gerar-observacao"})
            if limite and n >= limite:
                break
    with open(saida, "w", encoding="utf-8") as fh:
        for r in linhas:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return len(linhas)


def demonstrar_negativo(destino):
    """Prova do CASO NEGATIVO, reproduzivel por um comando: fonte INTACTO -> verde;
    fonte com UMA entrada real removida -> REPROVADO. Nao toca no mod: escreve a copia
    mutada DENTRO de `destino` (obrigatorio, e nunca o arquivo do produto)."""
    os.makedirs(destino, exist_ok=True)
    t = carregar_tabelas()
    with open(TABELAS_ARQ, encoding="utf-8") as fh:
        fonte = fh.read()
    indice, _cont = carregar_censo()
    chave = next(k for k in t["TextFixes"] if k in indice)
    baseline = {"esquema": ESQUEMA_BASELINE, "procedencia": "FIXTURE",
                "sha256_tabelas": sha256_arquivo(TABELAS_ARQ),
                "cobrados": {chave: "TextFixes"}}
    copia = os.path.join(destino, "LocalizePatch-sem-uma-entrada.cs")
    with open(copia, "w", encoding="utf-8") as fh:
        fh.write(remover_entrada_do_fonte(fonte, "TextFixes", chave))

    print("entrada real removida na copia: %r (tabela TextFixes)" % chave)
    print("copia mutada   : %s" % copia)
    print("arquivo do mod : %s  (NAO foi tocado)" % TABELAS_ARQ)
    print()
    print("--- 1) METADE VERDE: o fonte INTACTO contra o MESMO baseline ---")
    viol = verificar_baseline(baseline, carregar_tabelas())
    print("   violacoes: %d -> %s" % (len(viol), "TRAVA VERDE" if not viol else "REPROVADO"))
    verde = 0 if not viol else 1
    print("--- 2) METADE VERMELHA: a copia SEM a entrada, mesmo baseline ---")
    viol_mut = verificar_baseline(baseline, carregar_tabelas(copia))
    for v in viol_mut:
        print("   [%s] %r esperada em %s" % (v["tipo"], v["chave"][:70], v.get("esperado")))
    vermelho = 1 if viol_mut else 0
    print()
    print("veredito: intacto -> exit %d (verde) | sem a entrada -> exit %d (REPROVADO)"
          % (verde, vermelho))
    if verde == 0 and vermelho == 1:
        print("CASO NEGATIVO PROVADO: vermelho->verde pela remocao de UMA entrada real.")
        return 0
    print("NAO PROVOU: esperava verde no intacto e vermelho na copia mutada.")
    return 1


def main(argv=None):
    _utf8()
    ap = argparse.ArgumentParser(description="Cobertura das tabelas do BetterTooltips via hook ui.localized.")
    ap.add_argument("--prova", action="store_true", help="roda os casos do instrumento ('Ran N tests; failures: K')")
    ap.add_argument("--observacoes", help="JSONL de observacoes (chave/resultado)")
    ap.add_argument("--baseline-out", help="grava o baseline (contrato) a partir da observacao")
    ap.add_argument("--verificar", help="roda a TRAVA contra um baseline")
    ap.add_argument("--json", dest="json_out", help="grava o relatorio JSON neste caminho")
    ap.add_argument("--gerar-observacao", help="gera uma observacao FIXTURE a partir do censo")
    ap.add_argument("--demonstrar-negativo", metavar="DIR",
                    help="prova o caso NEGATIVO por comando (fonte intacto = verde; copia com uma entrada removida = REPROVADO)")
    ap.add_argument("--limite", type=int, help="limite de linhas para --gerar-observacao")
    ap.add_argument("--tabelas", help="fonte das tabelas (padrao: BetterTooltips/Patches/LocalizePatch.cs)")
    ap.add_argument("--censo", help="diretorio do censo (padrao: docs/cobertura)")
    ap.add_argument("--verboso", action="store_true", help="mostra cada caso do --prova")
    args = ap.parse_args(argv)

    if args.prova:
        return prova(args.verboso)

    if args.demonstrar_negativo:
        return demonstrar_negativo(args.demonstrar_negativo)

    if args.gerar_observacao:
        n = gerar_observacao(args.gerar_observacao, args.limite, args.censo)
        print("observacao FIXTURE gravada: %s (%d linhas)" % (args.gerar_observacao, n))
        return 0

    if args.verificar:
        try:
            with open(args.verificar, encoding="utf-8") as fh:
                baseline = json.load(fh)
        except (IOError, ValueError) as e:
            print("baseline ilegivel: %s" % e)
            return 2
        tabelas = carregar_tabelas(args.tabelas)
        viol = verificar_baseline(baseline, tabelas)
        print("baseline: %s (%d chaves cobradas, procedencia %s)"
              % (args.verificar, len(baseline.get("cobrados", {})), baseline.get("procedencia")))
        if not viol:
            print("TRAVA VERDE: nenhuma entrada cobrada sumiu nem caiu nas duas tabelas.")
            return 0
        print("TRAVA REPROVADA: %d violacao(oes)" % len(viol))
        for v in viol:
            print("   [%s] %r  (esperado em %s, hoje %s)"
                  % (v["tipo"], v["chave"][:80], v.get("esperado"), v.get("tabela")))
        return 1

    caminho = args.observacoes or OBS_PADRAO
    if not os.path.isfile(caminho):
        print("NAO_EXERCITADO: sem observacao em %s" % caminho)
        print("  motivo: a captura em jogo depende de rodada AUTORIZADA pelo dono; nenhuma foi feita.")
        print("  para ensaiar com fixture (nunca evidencia de jogo):")
        print("    python tools/cobertura_ui_localized.py --gerar-observacao <saida.jsonl>")
        return 2

    tabelas = carregar_tabelas(args.tabelas)
    indice, contagem = carregar_censo(args.censo)
    rel = analisar(carregar_observacoes(caminho), tabelas, indice, contagem)
    imprimir_relatorio(rel, caminho)
    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump(rel, fh, ensure_ascii=False, indent=2)
        print("relatorio JSON: %s" % args.json_out)
    if args.baseline_out:
        base = construir_baseline(rel, sha256_arquivo(args.tabelas or TABELAS_ARQ))
        with open(args.baseline_out, "w", encoding="utf-8") as fh:
            json.dump(base, fh, ensure_ascii=False, indent=2)
        print("baseline gravado: %s (%d chaves cobradas, procedencia %s)"
              % (args.baseline_out, len(base["cobrados"]), base["procedencia"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
