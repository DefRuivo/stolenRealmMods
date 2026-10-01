#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""roda_testes.py - o runner UNICO dos testes do Stolen Realm Mods.

    python tools/testes/roda_testes.py

UM COMANDO RODA TUDO e o exit code diz a verdade:

    0  tudo verde        - todo teste que rodou passou, NADA ficou por rodar
    1  algo REPROVOU     - um teste falhou (ou a prova de fogo do runner falhou)
    2  NAO CONSEGUI RODAR - faltou dependencia (lib/ do jogo, dotnet, ...);
                           a mensagem diz QUAL

A REGRA QUE ESTE RUNNER EXISTE PARA IMPOR
-----------------------------------------
"Um teste pulado nao conta como verde." Aqui nao existe estado "pulado": existe
`NAO_RODOU`, que e uma REPROVACAO do ponto de vista do exit code (2). Se voce
rodar tudo numa maquina sem a lib/ do jogo, o runner diz 2 e nomeia o que faltou
- nao devolve 0 escondendo metade da suite.

OPCOES
------
    --puros            so a categoria 'pura' (logica pura, roda sem o jogo).
                       E o modo do CI. Os testes de 'jogo' sao EXCLUIDOS e
                       CONTADOS a parte - nao viram verde por omissao.
    --jogo             so a categoria 'jogo' (precisa da lib/ do jogo, roda local)
    --teste CAMINHO    roda UM arquivo de teste
    --dir CAMINHO      troca a raiz de descoberta (padrao: testes/)
    --contra-prova     roda tools/testes/contra-prova/ INVERTENDO a expectativa:
                       ali todo teste tem de REPROVAR. Se algum passar, o runner
                       esta quebrado e o veredito e vermelho.
    --lib CAMINHO      aponta a lib/ do jogo (equivale a SR_TESTES_LIB)
    --lista            lista o que seria rodado (com requisitos) e nao roda
    --json             saida JSON em vez do relatorio humano
    --verboso          mostra a saida completa dos testes que falharem

CONVENCAO DE DESCOBERTA
-----------------------
Sao testes os arquivos `t_*.py` (suite normal) e `cp_*.py` (prova de fogo). Cada
um declara um dict META e roda como script. Qualquer outro .py na pasta e
ignorado e CONTADO no relatorio ("ignorados") - para que um nome fora do padrao
nunca vire um teste que desaparece em silencio.
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import arcabouco  # noqa: E402  (depende do sys.path acima)

PADRAO_SUITE = "t_"
PADRAO_CONTRA_PROVA = "cp_"
TIMEOUT_POR_TESTE = 300


# ------------------------------- descoberta ---------------------------------

def descobrir(raiz, padrao):
    """Devolve (testes, ignorados): caminhos de teste pelo prefixo e os .py fora dele."""
    testes, ignorados = [], []
    if not os.path.isdir(raiz):
        return testes, ignorados
    for pasta, _, arquivos in os.walk(raiz):
        for nome in sorted(arquivos):
            if not nome.endswith(".py") or nome.startswith("__"):
                continue
            caminho = os.path.join(pasta, nome)
            if nome.startswith(padrao):
                testes.append(caminho)
            else:
                ignorados.append(caminho)
    return testes, ignorados


def carregar(caminho):
    """Le e valida o META. Devolve (meta, erro) - erro e string ou None."""
    try:
        meta = arcabouco.ler_meta(caminho)
        arcabouco.validar_meta(meta, caminho)
        return meta, None
    except (arcabouco.Falhou, SyntaxError, ValueError) as erro:
        return None, str(erro)


# --------------------------------- execucao ---------------------------------
# Estados possiveis de um teste, do ponto de vista do veredito:
#   PASSOU        exit 0, esperava passar
#   REPROVOU      exit 1, esperava passar      -> o veredito fica VERMELHO
#   NAO_RODOU     exit 2 (ou requisito faltando) -> o veredito fica "NAO DEU"
#   PROVA_OK      exit 1, esperava reprovar    -> a prova de fogo funcionou
#   PROVA_FALHOU  exit 0, esperava reprovar    -> o runner deixou passar defeito
ESTADOS_VERMELHOS = ("REPROVOU", "PROVA_FALHOU")


def rodar_um(caminho, meta, verboso):
    esperado = meta.get("esperado", "passar")

    # 1. Requisito declarado no META: checado ANTES de gastar subprocesso, e a
    #    mensagem sai pronta (e a mesma que o teste daria).
    for req in meta.get("requer", []):
        ok, detalhe = arcabouco.requisito(req)
        if not ok:
            return {"estado": "NAO_RODOU", "detalhe": "requer %s: %s" % (req, detalhe), "saida": ""}

    # 2. Roda isolado. Excecao do teste nao derruba o runner.
    try:
        codigo, saida = arcabouco.executar_arquivo(caminho, timeout=TIMEOUT_POR_TESTE)
    except Exception as erro:
        return {"estado": "NAO_RODOU", "detalhe": "nao consegui executar: %s" % erro, "saida": ""}

    detalhe = ""
    for linha in saida.splitlines():
        if linha.startswith(arcabouco.PREFIXO_RESULTADO):
            partes = linha.split("|", 3)
            if len(partes) == 4:
                _, estado_do_teste, _, detalhe = partes
    if not detalhe:
        detalhe = (saida.strip().splitlines() or ["sem saida"])[-1]

    if codigo == 0:
        estado = "PASSOU" if esperado == "passar" else "PROVA_FALHOU"
    elif codigo == 1:
        estado = "REPROVOU" if esperado == "passar" else "PROVA_OK"
    elif codigo == 2:
        estado = "NAO_RODOU"
    else:
        estado = "REPROVOU"

    mostrar_saida = verboso or estado in ESTADOS_VERMELHOS
    restante = "\n".join(l for l in saida.splitlines()
                         if not l.startswith(arcabouco.PREFIXO_RESULTADO)).strip()
    return {"estado": estado, "detalhe": detalhe, "saida": restante if mostrar_saida else ""}


# ---------------------------------- relato ----------------------------------

def relatar(registros, excluidos, ignorados, modo, raiz, como_json):
    contagem = {}
    for r in registros:
        contagem[r["estado"]] = contagem.get(r["estado"], 0) + 1

    verde = not any(r["estado"] in ESTADOS_VERMELHOS for r in registros)
    if not verde:
        codigo = 1
    elif contagem.get("NAO_RODOU"):
        codigo = 2
    elif not registros:
        codigo = 2
    else:
        codigo = 0

    if como_json:
        print(json.dumps({
            "modo": modo,
            "raiz": raiz,
            "exit_code": codigo,
            "contagem": contagem,
            "excluidos_por_categoria": excluidos,
            "ignorados_fora_do_padrao": ignorados,
            "testes": [{"arquivo": os.path.relpath(r["arquivo"], raiz), "nome": r["nome"],
                        "categoria": r["categoria"], "esperado": r["esperado"],
                        "estado": r["estado"], "detalhe": r["detalhe"]} for r in registros],
        }, ensure_ascii=False, indent=2))
        return codigo

    largura_nome = max([len(r["nome"]) for r in registros] + [12])
    print("=" * 78)
    print(" ARCABOUCO DE TESTES - tools/testes")
    print(" raiz do repositorio: %s" % arcabouco.raiz_do_repo())
    print(" descoberta:         %s" % raiz)
    print(" modo:               %s" % modo)
    print("=" * 78)

    secoes = (("pura", "LOGICA PURA (roda sem o jogo, e o que roda no CI)"),
              ("jogo", "PRECISA DO JOGO (lib/ local, nao roda no CI)"),
              ("?", "SEM CATEGORIA (META invalido - defeito do teste, nao do ambiente)"))
    for chave, titulo in secoes:
        if chave == "?":
            da_categoria = [r for r in registros if r["categoria"] not in ("pura", "jogo")]
        else:
            da_categoria = [r for r in registros if r["categoria"] == chave]
        if not da_categoria:
            continue
        print()
        print("--- %s " % titulo + "-" * max(0, 70 - len(titulo)))
        for r in da_categoria:
            marca = {"PASSOU": "PASSOU ", "REPROVOU": "REPROVOU", "NAO_RODOU": "NAO RODOU",
                     "PROVA_OK": "PROVA OK", "PROVA_FALHOU": "PROVA FALHOU"}.get(r["estado"], r["estado"])
            print("[%s] %-*s %s" % (marca, largura_nome, r["nome"], r["detalhe"]))
            if r["saida"]:
                for linha in r["saida"].splitlines():
                    print("           | %s" % linha)

    print()
    print("=" * 78)
    print(" RESUMO")
    print("   rodaram:    %d" % (len(registros) - contagem.get("NAO_RODOU", 0)))
    print("   passaram:   %d" % contagem.get("PASSOU", 0))
    print("   reprovaram: %d" % contagem.get("REPROVOU", 0))
    print("   nao rodaram:%d%s" % (contagem.get("NAO_RODOU", 0),
                                   "  <- FALTA DEPENDENCIA, o exit code e 2" if contagem.get("NAO_RODOU") else ""))
    if contagem.get("PROVA_OK") or contagem.get("PROVA_FALHOU"):
        print("   prova de fogo: %d ok, %d falhou" % (contagem.get("PROVA_OK", 0), contagem.get("PROVA_FALHOU", 0)))
    if excluidos:
        print("   EXCLUIDOS por categoria (%d): %s" % (
            sum(excluidos.values()),
            ", ".join("%s=%d" % (k, v) for k, v in sorted(excluidos.items()))))
        print("       -> NAO foram executados. Nao contam como verde: este modo os exclui de proposito.")
    if ignorados:
        print("   ignorados (nome fora do padrao t_*/cp_*): %d" % len(ignorados))
        for caminho in ignorados:
            print("       %s" % os.path.relpath(caminho, raiz))
    if not registros:
        print("   NENHUM TESTE ENCONTRADO - nada executado nao e verde.")
    print()
    if codigo == 0:
        print(" VEREDITO: VERDE (exit 0)")
    elif codigo == 1:
        if contagem.get("PROVA_FALHOU"):
            print(" VEREDITO: REPROVADO (exit 1) - A PROVA DE FOGO FALHOU: o runner deixou passar")
            print("           um teste marcado como 'esperado: reprovar'. O runner nao esta reprovando.")
        else:
            print(" VEREDITO: REPROVADO (exit 1) - veja os REPROVOU acima")
    else:
        print(" VEREDITO: NAO CONSEGUI RODAR (exit 2) - falta dependencia, veja os NAO_RODOU acima")
    print("=" * 78)
    return codigo


# ----------------------------------- main -----------------------------------

def main():
    ap = argparse.ArgumentParser(add_help=True, description="Runner unico dos testes (tools/testes).")
    ap.add_argument("--puros", "--so-logica", "--ci", dest="puros", action="store_true",
                    help="so a categoria 'pura' (modo CI): os testes de 'jogo' sao excluidos e contados a parte")
    ap.add_argument("--jogo", action="store_true", help="so a categoria 'jogo' (precisa da lib/ do jogo)")
    ap.add_argument("--teste", help="roda UM arquivo de teste")
    ap.add_argument("--dir", help="raiz alternativa de descoberta")
    ap.add_argument("--contra-prova", dest="contra_prova", action="store_true",
                    help="roda a prova de fogo do runner (espera que os testes REPROVEM)")
    ap.add_argument("--lib", help="aponta a lib/ do jogo (equivale a SR_TESTES_LIB)")
    ap.add_argument("--lista", action="store_true", help="lista o que seria rodado e nao roda")
    ap.add_argument("--json", action="store_true", help="saida JSON em vez do relatorio humano")
    ap.add_argument("--verboso", action="store_true", help="mostra a saida dos testes que falharem")
    args = ap.parse_args()

    if args.lib:
        os.environ["SR_TESTES_LIB"] = os.path.abspath(args.lib)

    if args.contra_prova:
        raiz, padrao, modo = arcabouco.DIR_CONTRA_PROVA, PADRAO_CONTRA_PROVA, "prova de fogo (--contra-prova)"
        raiz = args.dir or raiz
    else:
        raiz, padrao, modo = args.dir or arcabouco.DIR_TESTES, PADRAO_SUITE, "suite"
        if args.puros:
            modo = "suite, so logica pura (--puros)"
        elif args.jogo:
            modo = "suite, so o que precisa do jogo (--jogo)"

    if args.teste:
        caminhos = [os.path.abspath(args.teste)]
        if not os.path.isfile(caminhos[0]):
            print("arquivo de teste nao existe: %s" % caminhos[0])
            return 2
        ignorados = []
        raiz = os.path.dirname(caminhos[0])
        modo = "teste unico: %s" % os.path.relpath(caminhos[0], arcabouco.raiz_do_repo())
    else:
        caminhos, ignorados = descobrir(raiz, padrao)

    if not os.path.isdir(raiz):
        print("raiz de testes nao existe: %s" % raiz)
        return 2

    registros, excluidos = [], {}
    for caminho in caminhos:
        meta, erro = carregar(caminho)
        nome = os.path.splitext(os.path.basename(caminho))[0]
        if erro:
            registros.append({"arquivo": caminho, "nome": nome, "categoria": "?",
                              "esperado": "passar", "estado": "REPROVOU",
                              "detalhe": "META invalido: %s" % erro, "saida": ""})
            continue
        categoria = meta["categoria"]
        if args.puros and categoria != "pura":
            excluidos[categoria] = excluidos.get(categoria, 0) + 1
            continue
        if args.jogo and categoria != "jogo":
            excluidos[categoria] = excluidos.get(categoria, 0) + 1
            continue
        if args.lista:
            ok_reqs = []
            for req in meta.get("requer", []):
                ok, detalhe = arcabouco.requisito(req)
                ok_reqs.append("%s %s (%s)" % ("OK " if ok else "FALTA", req, detalhe))
            print("%-46s %-5s %s%s" % (
                os.path.relpath(caminho, raiz), categoria,
                "requer: " + "; ".join(ok_reqs) if ok_reqs else "sem dependencia declarada",
                "  [espera REPROVAR]" if meta.get("esperado") == "reprovar" else ""))
            continue
        resultado = rodar_um(caminho, meta, args.verboso)
        resultado.update({"arquivo": caminho, "nome": meta["nome"], "categoria": categoria,
                          "esperado": meta.get("esperado", "passar")})
        registros.append(resultado)

    if args.lista:
        if excluidos:
            print("\nexcluidos por categoria: %s" % excluidos)
        return 0

    return relatar(registros, excluidos, ignorados, modo, raiz, args.json)


if __name__ == "__main__":
    sys.exit(main())
