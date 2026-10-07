#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""hashes_da_entrega.py - registro de hashes da entrega da COR-AUT7-F2 (execucao 430).

Gera `docs/automacao/COR-AUT7-F2-evidencias/hashes-finais.json`: quem quiser reauditar o
cartao compara este arquivo com o disco. Entradas:

  * `entrega`        - fontes/scripts dai qual sai TODA a evidencia (inclui ESTE arquivo);
  * `docs_gerados`   - docs regerados pela CLI real do consolidador;
  * `evidencia`      - os artefatos de prova (refutacao, entradas medidas, adaptador, dump);
  * `produto_artefatos_de_build_medidos` - `dist/*.zip` + `<Mod>/bin/**/*.dll` (o que a suite
                       MEDE), com a conferencia contra o registro da execucao 415;
  * `produto_fonte_e_assets` - os 78 fontes/assets dos 6 mods, com sha256 POR ARQUIVO (a
                       execucao 415 nao registrou hashes por arquivo de fonte; o que da para
                       conferir entre execucoes e o bloco de artefatos).

Nao toca em nada: so le e escreve o proprio JSON de registro. Sem jogo/build/deploy/publicacao.

Uso:
    python tools/automacao/estilo/hashes_da_entrega.py
"""
import glob
import hashlib
import io
import json
import os
import sys

W = os.path.dirname(os.path.abspath(__file__))


def _raiz_do_repo():
    d = W
    for _ in range(6):
        if os.path.isdir(os.path.join(d, "BetterFont")):
            return d
        d = os.path.dirname(d)
    return os.path.join(W, "repo")


S = os.environ.get("COR_S") or _raiz_do_repo()
OUT = os.environ.get("COR_OUT") or os.path.join(S, "docs", "automacao", "COR-AUT7-F2-evidencias")
MODS = ("BetterFont", "BetterCombatText", "BetterStats", "RoguelikeDebugger",
        "BetterTooltips", "RoguelikeSkillTreeVisualizer")
ENTREGA = ("tools/automacao/estilo/estilo_atributos.py",
           "tools/automacao/estilo/test_estilo_atributos.py",
           "tools/automacao/estilo/refutar_cor_aut7f2.py",
           "tools/automacao/estilo/refutar_cor_aut7f2_entradas.py",
           "tools/automacao/estilo/fechar_cor_aut7f2.py",
           "tools/automacao/estilo/hashes_da_entrega.py",
           "tools/automacao/aceite/relatorio_aceite.py",
           "tools/automacao/aceite/test_relatorio_aceite.py")
DOCS = ("docs/automacao/AUT-7-relatorio.md", "docs/automacao/AUT-7-resultado.json",
        "docs/automacao/COR-AUT7-correcao.md", "docs/automacao/COR-AUT7-F2-relatorio.md")
EVIDENCIA = ("docs/automacao/COR-AUT7-F2-evidencias/refutacao-cor-aut7-f2.json",
             "docs/automacao/COR-AUT7-F2-evidencias/entradas-medidas.json",
             "docs/automacao/COR-AUT7-F2-evidencias/adaptador-aut6.json",
             "docs/automacao/COR-AUT7-F2-evidencias/docs-antes.txt",
             "docs/automacao/COR-AUT7-F2-evidencias/dump-do-produto.json")
REUSADOS = ("tools/automacao/aut6/cobertura.py",)


def sha(caminho):
    h = hashlib.sha256()
    with io.open(caminho, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def hashes(rels):
    return {rel.replace("\\", "/"): (sha(os.path.join(S, rel)) if os.path.isfile(os.path.join(S, rel))
                                     else None) for rel in rels}


ARQ = os.path.join(OUT, "hashes-finais.json")
ANTERIOR = None
if os.path.isfile(ARQ):
    try:
        ANTERIOR = json.load(io.open(ARQ, encoding="utf-8"))
    except ValueError:
        ANTERIOR = None
if ANTERIOR and ANTERIOR.get("execucao") == 430:
    ANTERIOR = None  # reexecucao do proprio registro: nao ha "antes" para comparar

artefatos = {}
for caminho in sorted(glob.glob(os.path.join(S, "dist", "*.zip"))):
    artefatos[os.path.relpath(caminho, S).replace("\\", "/")] = sha(caminho)
for mod in MODS:
    for caminho in sorted(glob.glob(os.path.join(S, mod, "bin", "**", "*.dll"), recursive=True)):
        artefatos[os.path.relpath(caminho, S).replace("\\", "/")] = sha(caminho)

fontes = {}
for mod in MODS:
    base = os.path.join(S, mod)
    for pasta, dirs, nomes in os.walk(base):
        dirs[:] = [d for d in dirs if d not in ("bin", "obj", "__pycache__")]
        for nome in nomes:
            caminho = os.path.join(pasta, nome)
            fontes[os.path.relpath(caminho, S).replace("\\", "/")] = sha(caminho)

comparacao = {"registro_anterior": (ANTERIOR or {}).get("execucao"),
              "artefatos_em_ambos": 0, "artefatos_divergentes": [],
              "artefatos_novos": [], "artefatos_ausentes": []}
if ANTERIOR:
    antigos = ANTERIOR.get("produto_artefatos_de_build_medidos") or {}
    ambos = sorted(set(antigos) & set(artefatos))
    comparacao["artefatos_em_ambos"] = len(ambos)
    comparacao["artefatos_divergentes"] = [k for k in ambos if antigos[k] != artefatos[k]]
    comparacao["artefatos_novos"] = sorted(set(artefatos) - set(antigos))
    comparacao["artefatos_ausentes"] = sorted(set(antigos) - set(artefatos))

registro = {
    "tarefa": "t_cd1332d7 (COR-AUT7-F2)",
    "execucao": 430,
    "fase_dos_achados": "execucao 415 (revisada na 425); esta rodada fecha o A6/F2 (ENTRADAS do cache)",
    "entrega": hashes(ENTREGA),
    "reusados_nao_editados": hashes(REUSADOS),
    "docs_gerados": hashes(DOCS),
    "evidencia": hashes(EVIDENCIA),
    "produto_artefatos_de_build_medidos": artefatos,
    "produto_fonte_e_assets": {
        "comparados": len(fontes),
        "sha256_por_arquivo": fontes,
        "conferencia_entre_execucoes": comparacao,
        "nota": ("a execucao 415 nao registrou hashes POR ARQUIVO dos fontes de produto; o que se "
                 "confere entre execucoes e o bloco de artefatos de build acima. Esta execucao "
                 "nao escreveu em nenhum caminho de produto/mod."),
    },
    "runtime": "NAO EXERCITADO",
    "aceite_humano": "NAO_PRONUNCIADO",
}
with io.open(ARQ, "w", encoding="utf-8", newline="\n") as fh:
    fh.write(json.dumps(registro, indent=2, ensure_ascii=False, default=str))
print("registro: %s" % ARQ)
print("entrega=%d docs=%d evidencia=%d artefatos=%d fontes=%d"
      % (len(registro["entrega"]), len(DOCS), len(EVIDENCIA), len(artefatos), len(fontes)))
if ANTERIOR:
    print("vs execucao %s: artefatos em ambos=%d divergentes=%d novos=%d ausentes=%d"
          % (comparacao["registro_anterior"], comparacao["artefatos_em_ambos"],
             len(comparacao["artefatos_divergentes"]), len(comparacao["artefatos_novos"]),
             len(comparacao["artefatos_ausentes"])))
sys.exit(0)
