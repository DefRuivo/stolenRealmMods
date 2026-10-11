#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""contra_prova_kit15.py - KIT-15: prova de que a suite PEGA defeitos (anti falso verde).

Metodo: copia os modulos do kit para uma sandbox propria, aplica UM defeito real de
implementacao (substituicao textual verificada), roda a SUITE INTEIRA contra o modulo
defeituoso e exige um RED HONESTO. A copia intacta tem de dar GREEN.

KIT-15F (achado F11) -- o que passou a ser EXIGIDO do RED, lido do resultado ESTRUTURADO
que a suite escreve (KIT15_RESULT), nunca por expressao regular sobre a saida:

  * a suite rodou de verdade (tests >= 1) -- "Ran 0 tests" NUNCA e RED;
  * zero ERROR (setUpModule/modulo quebrado NAO e RED) e zero skip;
  * o conjunto de falhas e EXATAMENTE o conjunto alvo do defeito (sem falha extra);
  * exit 1.
Qualquer desvio (SEM-EFEITO, FALSO-VERDE, ALVO-DIVERGENTE, MUTACAO-INVALIDA) reprova a
contra-prova. Sem isso, um erro de setup era aceito como "verde que pega defeito".

Nenhum arquivo do repositorio vivo e editado: so a copia sandbox. Nada abre jogo, instala,
publica ou usa rede.

KIT15-D6-CRLF: as ancoras dos defeitos sao escritas com "\n" (o estilo do repositorio) e sao
REESCRITAS no estilo de quebra de linha do arquivo em disco antes de casar. Assim a MESMA
contra-prova discrimina no checkout LF do autor e no checkout CRLF de um clone Windows
(core.autocrlf=true), sem normalizar os bytes fora do trecho ancorado. Antes disso a ancora
multiline do D6 nunca casava em CRLF: o defeito virava MUTACAO-INVALIDA e a prova de
discriminacao se perdia (baseline verde, 6/7).

    python tools/automacao/kit15/contra_prova_kit15.py [--saida <dir>] [--json]

Exit: 0 = baseline verde e TODOS os defeitos recusados com RED honesto; 1 = algum defeito
passou / RED desonesto; 2 = erro de infraestrutura.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

MODULOS = ["instalador.py", "descoberta.py", "pacote.py", "scan.py", "teste_kit15.py",
           "contra_prova_kit15.py", "manifesto.json"]

# KIT15-D6-CRLF: a suite procura ESTE numero de testes. Constante explicita (e nao ">= 1")
# porque um suite truncado por engano nao pode passar por baseline verde.
TESTS_ESPERADOS = 21

# Estilos de quebra de linha reconhecidos. A ancora dos defeitos e escrita com "\n" (o estilo
# do repositorio) e e REESCRITA no estilo do arquivo em disco antes de casar: o mesmo defeito
# tem de valer no checkout LF do autor E no checkout CRLF de um clone Windows
# (core.autocrlf=true). Sem isso a ancora multiline do D6 nunca casava em CRLF, o defeito
# virava MUTACAO-INVALIDA e a contra-prova perdia a discriminacao (falso verde de ferramenta).
NL_LF = "\n"
NL_CRLF = "\r\n"

DEFEITOS = [
    {
        "id": "D1-instalador-sem-conferencia-de-hash",
        "arquivo": "instalador.py",
        "patches": [('        if obtido != item["sha256"]:', "        if False:")],
        "alvo": ["test_12_hash_divergente_apos_escrita_dispara_rollback"],
    },
    {
        "id": "D2-instalador-reescreve-tudo",
        "arquivo": "instalador.py",
        "patches": [('        if existia and not forcar and sha_antes == item["sha256"]:', "        if False:")],
        "alvo": ["test_08_atualizar_muda_so_o_arquivo_divergente"],
    },
    {
        "id": "D3-instalador-nao-guarda-original",
        "arquivo": "instalador.py",
        "patches": [("            if preexistente and backup_original is None:", "            if False:")],
        "alvo": ["test_10_remover_restaura_estado_anterior"],
    },
    {
        "id": "D4-scan-sem-bloqueio-de-binario",
        "arquivo": "scan.py",
        "patches": [("    if ext in EXTENSOES_PROIBIDAS:", "    if False:")],
        "alvo": ["test_17_scan_controle_negativo_e_limpo", "test_18_scan_pega_dll_dentro_do_zip"],
    },
    {
        "id": "D5-scan-sem-deteccao-de-segredo",
        "arquivo": "scan.py",
        "patches": [("    for rotulo, rx in PADROES:", "    for rotulo, rx in []:")],
        "alvo": ["test_17_scan_controle_negativo_e_limpo"],
    },
    {
        # KIT15-D6-CRLF: unica ancora MULTILINE do conjunto -- e exatamente a que nao casava
        # num checkout CRLF. A ancora continua declarada com "\n"; aplicar_defeito a reescreve
        # no estilo do arquivo alvo.
        "id": "D6-descoberta-ignora-argumento-explicito",
        "arquivo": "descoberta.py",
        "patches": [('    if explicito:\n        return os.path.abspath(explicito), "argumento"',
                     '    if False:\n        return os.path.abspath(explicito), "argumento"')],
        "alvo": ["test_15_descoberta_sem_usuario_fixo"],
    },
    {
        "id": "D7-pacote-verificador-sempre-ok",
        "arquivo": "pacote.py",
        "patches": [('        "veredito": "OK" if (not achados and erro is None and not problemas) else "ACHADO",',
                     '        "veredito": "OK",')],
        "alvo": ["test_18_scan_pega_dll_dentro_do_zip"],
    },
]


def _copiar_modulos(destino):
    os.makedirs(destino, exist_ok=True)
    for nome in MODULOS:
        origem = os.path.join(AQUI, nome)
        if os.path.isfile(origem):
            shutil.copy2(origem, os.path.join(destino, nome))
    return destino


def _rodar_suite(sandbox, base, resultado_json):
    ambiente = dict(os.environ)
    ambiente["KIT15_RAIZ"] = base
    ambiente["KIT15_RESULT"] = resultado_json
    ambiente["PYTHONIOENCODING"] = "utf-8"
    ambiente["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, os.path.join(sandbox, "teste_kit15.py")],
        cwd=sandbox, env=ambiente, capture_output=True, text=True, timeout=900,
    )
    saida = (proc.stdout or "") + (proc.stderr or "")
    resumo = None
    if os.path.isfile(resultado_json):
        try:
            with open(resultado_json, "r", encoding="utf-8") as fh:
                resumo = json.load(fh)
        except (OSError, ValueError):
            resumo = None
    return proc.returncode, saida, resumo


def estilo_de_quebra(dados):
    """Estilo de quebra de linha de um arquivo em BYTES: '\\r\\n', '\\n' ou None (misto/vazio).

    Misto devolve None de proposito: reescrever a ancora num estilo que so casa parte do
    arquivo esconderia um defeito, entao a contra-prova recusa alto (MUTACAO-INVALIDA) em vez
    de adivinhar.
    """
    crlf = dados.count(b"\r\n")
    lf = dados.count(b"\n") - crlf
    if crlf and not lf:
        return NL_CRLF
    if lf and not crlf:
        return NL_LF
    if not crlf and not lf:
        return NL_LF  # arquivo de uma linha so: qualquer ancora casa
    return None


def _no_estilo(ancora, estilo):
    """Reescreve a ancora (declarada com '\\n') no estilo de quebra do arquivo alvo."""
    return ancora.replace(NL_CRLF, NL_LF).replace(NL_LF, estilo)


def aplicar_defeito(sandbox, defeito):
    """Aplica as substituicoes textuais do defeito na COPIA sandbox, uma unica vez cada.

    Trabalha em BYTES: le o arquivo cru, troca SO o trecho ancorado e grava de volta. Nenhuma
    quebra de linha fora do alvo e normalizada/convertida (o clone CRLF continua CRLF e o
    checkout LF continua LF) -- se a ancora nao casar exatamente 1 vez, a mutacao e recusada
    com motivo, nunca "aproximada".
    """
    caminho = os.path.join(sandbox, defeito["arquivo"])
    if not os.path.isfile(caminho):
        return False, "arquivo ausente na copia: %s" % defeito["arquivo"]
    with open(caminho, "rb") as fh:
        dados = fh.read()
    estilo = estilo_de_quebra(dados)
    if estilo is None:
        return False, ("quebras de linha mistas em %s: a ancora nao pode ser ancorada sem "
                       "adivinhar estilo" % defeito["arquivo"])
    original = dados
    for de, para in defeito["patches"]:
        de_b = _no_estilo(de, estilo).encode("utf-8")
        para_b = _no_estilo(para, estilo).encode("utf-8")
        ocorrencias = dados.count(de_b)
        if ocorrencias != 1:
            return False, "texto alvo aparece %d vezes (esperado 1): %r" % (ocorrencias, de[:60])
        dados = dados.replace(de_b, para_b, 1)
    if dados == original:
        return False, "nenhuma substituicao efetiva"
    with open(caminho, "wb") as fh:
        fh.write(dados)
    return True, "ok"


def _ids(resumo, chave):
    return sorted(str(x).rsplit(".", 1)[-1] for x in (resumo or {}).get(chave) or [])


def main(argv=None):
    ap = argparse.ArgumentParser(description="KIT-15: contra-prova da suite (defeitos plantados)")
    ap.add_argument("--saida", default=None, help="diretorio das provas (default: TMPDIR/kit15-contra)")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)

    try:
        import pacote
        base = pacote._raiz_repo()
    except Exception as exc:
        print("ERRO-INFRA KIT-15 contra-prova: origem indisponivel: %s" % exc, file=sys.stderr)
        return 2

    raiz_saida = args.saida or os.path.join(os.environ.get("TMPDIR") or os.path.abspath("scratch"),
                                            "kit15-contra-%s" % time.strftime("%H%M%S"))
    base_saida = os.path.abspath(raiz_saida)
    if os.path.isdir(base_saida):
        shutil.rmtree(base_saida)
    os.makedirs(base_saida)

    resultados = []
    # 1) baseline: copia intacta tem de dar GREEN
    sb_base = _copiar_modulos(os.path.join(base_saida, "baseline"))
    rc, saida, resumo = _rodar_suite(sb_base, base, os.path.join(base_saida, "resultado-baseline.json"))
    ds = resumo or {}
    baseline_ok = (rc == 0 and ds.get("tests") == TESTS_ESPERADOS and not ds.get("failures")
                   and not ds.get("errors") and not ds.get("skipped") and ds.get("ok") is True)
    resultados.append({"id": "baseline-intacto", "eh_defeito": False, "esperado": "GREEN", "rc": rc,
                       "tests": ds.get("tests"), "errors": len(ds.get("errors") or []),
                       "skipped": ds.get("skipped"),
                       "veredito": "OK" if baseline_ok else "FALHOU"})
    with open(os.path.join(base_saida, "log-baseline.txt"), "w", encoding="utf-8") as fh:
        fh.write(saida)

    # 2) cada defeito na sua propria copia
    for i, defeito in enumerate(DEFEITOS, start=1):
        sb = _copiar_modulos(os.path.join(base_saida, "D%d" % i))
        aplicado, motivo = aplicar_defeito(sb, defeito)
        if not aplicado:
            resultados.append({"id": defeito["id"], "eh_defeito": True, "alvo": defeito["alvo"],
                               "esperado": "RED", "veredito": "MUTACAO-INVALIDA", "motivo": motivo})
            continue
        rc, saida, resumo = _rodar_suite(sb, base, os.path.join(base_saida, "resultado-D%d.json" % i))
        with open(os.path.join(base_saida, "log-%02d.txt" % i), "w", encoding="utf-8") as fh:
            fh.write("DEFEITO: %s\n\n%s" % (defeito["id"], saida))
        ds = resumo or {}
        falhas = _ids(ds, "failures")
        erros = _ids(ds, "errors")
        esperado = sorted(defeito["alvo"])
        red_honesto = (rc == 1 and (ds.get("tests") or 0) >= 1 and not erros
                       and not ds.get("skipped") and falhas == esperado)
        if red_honesto:
            veredito = "OK"
        elif rc == 0:
            veredito = "SEM-EFEITO"
        elif (ds.get("tests") or 0) < 1 or erros:
            veredito = "FALSO-VERDE"
        else:
            veredito = "ALVO-DIVERGENTE"
        resultados.append({"id": defeito["id"], "eh_defeito": True, "arquivo": defeito["arquivo"],
                           "alvo": esperado, "esperado": "RED", "rc": rc,
                           "tests": ds.get("tests"), "falhas": falhas, "erros": erros,
                           "skipped": ds.get("skipped"), "veredito": veredito})

    so_defeitos = [r for r in resultados if r.get("eh_defeito")]
    recusados = sum(1 for r in so_defeitos if r["veredito"] == "OK")
    total_defeitos = len(DEFEITOS)
    recusa = {r["veredito"]: sorted(x["id"] for x in so_defeitos if x["veredito"] == r["veredito"])
              for r in so_defeitos}
    resumo_final = {
        "schema": "kit-rstv/contra-prova/1",
        "base": base,
        "sandbox": base_saida,
        "baseline_verde": baseline_ok,
        "defeitos": total_defeitos,
        "recusados": recusados,
        "por_veredito": recusa,
        "resultados": resultados,
        "veredito": "OK" if (baseline_ok and recusados == total_defeitos) else "FALHOU",
    }
    with open(os.path.join(base_saida, "contra-prova.json"), "w", encoding="utf-8") as fh:
        json.dump(resumo_final, fh, indent=2, ensure_ascii=False)

    if args.json:
        print(json.dumps(resumo_final, indent=2, ensure_ascii=False))
    else:
        for r in resultados:
            print("  %-46s %s (%s)" % (r["id"], r["veredito"], r.get("alvo", "-")))
        print("CONTRA-PROVA|%s|baseline=%s|recusados=%d/%d|por-veredito=%s|sandbox=%s" % (
            resumo_final["veredito"], baseline_ok, recusados, total_defeitos, recusa, base_saida))
    return 0 if resumo_final["veredito"] == "OK" else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except subprocess.TimeoutExpired:
        print("ERRO-INFRA KIT-15 contra-prova: timeout ao rodar a suite mutada", file=sys.stderr)
        sys.exit(2)
