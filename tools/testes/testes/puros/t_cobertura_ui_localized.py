#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t_cobertura_ui_localized.py - a SUITE do instrumento de cobertura (INT-R1-C5).

O instrumento (`tools/cobertura_ui_localized.py`) mede a cobertura das tabelas do
`BetterTooltips` contra o texto que o jogo serviu, capturado pelo hook `ui.localized`
da API propria. Este teste garante cinco coisas:

  1. a PROVA do proprio instrumento e verde e imprime a linha do aceite
     (`Ran <N> tests; failures: 0`) - N sai do numero de casos declarados, nao de um
     literal que envelhece;
  2. a MEDICAO classifica certo uma observacao sintetica (fixture versionada):
     coberto / lacuna / entrada que nao rodou / chave nas duas tabelas;
  3. a medicao funciona sobre o CENSO REAL (fixture gerada por comando) e a saida traz
     contagem por ARQUIVO (aceite do cartao);
  4. a TRAVA morde: com uma entrada real removida, o instrumento REPROVA - e o controle
     positivo (fonte intacto) fica verde;
  5. o arquivo do MOD nao muda: o sha256 do `LocalizePatch.cs` e o mesmo no inicio e no
     fim deste teste (nada aqui escreve no `BetterTooltips`).
"""
import os
import subprocess
import sys
import tempfile

import arcabouco as arc

META = {
    "nome": "cobertura-ui-localized",
    "categoria": "pura",
    "requer": [],
    "descricao": "instrumento de cobertura (hook ui.localized) mede certo, morde no caso negativo e nao toca no BetterTooltips",
}

RAIZ = arc.raiz_do_repo()
sys.path.insert(0, os.path.join(RAIZ, "tools"))
import cobertura_ui_localized as C  # noqa: E402

FERRAMENTA = os.path.join(RAIZ, "tools", "cobertura_ui_localized.py")


def _roda(*args):
    return subprocess.run([sys.executable, FERRAMENTA] + list(args),
                          cwd=RAIZ, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          universal_newlines=True, timeout=300)


def corpo():
    hash_antes = C.sha256_arquivo(C.TABELAS_ARQ)

    # 1) a prova do instrumento (inclui o caso negativo) tem de sair verde
    p = _roda("--prova")
    arc.igual(p.returncode, 0, "exit da --prova do instrumento")
    linha = "Ran %d tests; failures: 0" % len(C.CASOS)
    arc.exigir(linha in p.stdout,
               "a --prova nao imprimiu %r; saida:\n%s" % (linha, p.stdout))

    # 2) medicao sintetica: a classificacao de cada observacao
    dados = arc.ler_json("cobertura-ui-localized", "entrada")
    esperado = arc.ler_json("cobertura-ui-localized", "esperado")
    tabelas = C._tabelas_da_fonte(C.FIXTURE_FONTE)
    rel = C.analisar(dados["observacoes"], tabelas, {}, {})
    arc.igual(len(rel["cobertos"]), esperado["cobertos"], "cobertos")
    arc.igual(len(rel["lacunas"]), esperado["lacunas"], "lacunas")
    arc.igual(len(rel["nao_aplicados"]), esperado["nao_aplicados"], "entradas que nao rodaram")
    arc.igual(len(rel["chaves_mortas"]), esperado["chaves_mortas"], "chaves nunca servidas")
    arc.exigir(esperado["chave_compartilhada"] in rel["chaves_compartilhadas"],
               "a chave nas DUAS tabelas nao foi detectada: %s" % rel["chaves_compartilhadas"])
    arc.igual(rel["lacunas"][0]["chave"], esperado["lacuna_chave"], "chave da lacuna")
    arc.igual(rel["lacunas"][0]["categoria"], esperado["categoria_da_lacuna"], "categoria da lacuna")
    arc.igual(rel["nao_aplicados"][0]["motivo"], esperado["motivo_nao_aplicado"], "motivo")
    arc.igual(rel["procedencia"], "FIXTURE", "procedencia declarada")

    # 3) medicao sobre o CENSO REAL, pela fixture que a propria ferramenta gera
    obs = os.path.join(tempfile.mkdtemp(prefix="int-r1-c5-"), "observacao.jsonl")
    n = C.gerar_observacao(obs)
    arc.exigir(n > 0, "a fixture saiu vazia (nenhuma entrada da tabela casou com o censo)")
    rel_real = C.analisar(C.carregar_observacoes(obs), C.carregar_tabelas(),
                          *C.carregar_censo())
    arc.igual(rel_real["lacunas"], [], "a fixture do censo nao pode ter lacuna")
    arc.igual(len(rel_real["cobertos"]), n, "toda linha da fixture tinha de virar coberto")
    por_arquivo = rel_real["por_arquivo"]
    arc.exigir(por_arquivo["skills.csv"]["entradas_no_censo"] > 0, "skills.csv sem contagem")
    arc.igual(sum(d["entradas_no_censo"] for d in por_arquivo.values()),
              sum(C.carregar_censo()[1].values()), "a contagem por arquivo nao bate com o censo")

    # 4) a TRAVA morde: entrada real removida -> REPROVADO; fonte intacto -> verde
    real = carregar_primeira_chave_no_censo()
    base = {"cobrados": {real: "TextFixes"}}
    via_memoria = dict(C.carregar_tabelas())
    via_memoria["TextFixes"] = {k: v for k, v in via_memoria["TextFixes"].items() if k != real}
    viol = C.verificar_baseline(base, via_memoria)
    arc.igual(len(viol), 1, "a trava tinha de acusar exatamente uma violacao")
    arc.igual(viol[0]["tipo"], "entrada-removida", "tipo da violacao")
    arc.igual(C.verificar_baseline(base, C.carregar_tabelas()), [],
              "controle positivo: com o fonte real intacto a trava tem de ficar verde")

    # 5) o mod nao foi tocado
    arc.igual(C.sha256_arquivo(C.TABELAS_ARQ), hash_antes,
              "o LocalizePatch.cs mudou durante o teste (o instrumento NAO pode escrever no mod)")


def carregar_primeira_chave_no_censo():
    indice, _ = C.carregar_censo()
    tabelas = C.carregar_tabelas()
    for chave in tabelas["TextFixes"]:
        if chave in indice:
            return chave
    raise arc.Falhou("nenhuma entrada real do TextFixes casou com o censo")


if __name__ == "__main__":
    arc.main(META, corpo)
