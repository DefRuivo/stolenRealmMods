#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""arcabouco.py - biblioteca comum dos testes do Stolen Realm Mods.

O QUE ESTE ARQUIVO E
--------------------
O contrato que TODO teste de `tools/testes/` usa. Ele existe para que uma regra
mora num lugar so: o que e "falhou", o que e "nao conseguiu rodar", onde ficam as
fixtures e como se declara dependencia. O runner (`roda_testes.py`) importa daqui
o leitor de META; os testes importam daqui os asserts e a carga de fixture.

COMO UM TESTE SE PARECE
-----------------------
    # tools/testes/testes/puros/t_meu_teste.py
    import arcabouco as arc

    META = {
        "nome": "meu-teste",          # vira o nome da fixture: <nome>.entrada.json
        "categoria": "pura",         # "pura" (roda sem o jogo) | "jogo" (precisa da lib/)
        "requer": [],                # ex.: ["lib/"] ou ["dotnet"] - checado ANTES de rodar
        "descricao": "o que este teste garante",
    }

    def corpo():
        dados = arc.ler_json("meu-teste", "entrada")
        arc.igual(calcular(dados), 42, "o valor")

    if __name__ == "__main__":
        arc.main(META, corpo)

AS TRES SAIDAS (e por que sao tres)
-----------------------------------
  PASSOU      -> exit 0. O comportamento observado e o esperado.
  REPROVOU    -> exit 1. O comportamento divergiu. `arc.Falhou`.
  NAO_RODOU   -> exit 2. Faltou dependencia (lib/ do jogo, dotnet, ...). `arc.NaoRodou`.

"NAO RODOU" NAO E VERDE. Um teste que nao pode rodar nao conta como aprovado em
lugar nenhum: o runner soma os NAO_RODOU e o exit code final vira 2. E por isso
que a categoria `jogo` e uma DECLARACAO no META e nao um `try/except` silencioso:
o runner mostra na cara quais testes rodaram e quais nao rodaram, em vez de deixar
um verde que esconde metade da suite.

REGRA DO PROJETO (docs/PLANO-DE-TESTES.md): todo teste tem de ser MOSTRADO
REPROVANDO. Planta o defeito, roda, ve falhar; tira o defeito, roda, ve passar.
Teste que nunca falhou nao e teste - e decoracao. A prova de fogo do proprio
arcabouco esta em `tools/testes/contra-prova/` e e executada pelo runner com
`--contra-prova`.
"""
import json
import os
import struct
import subprocess
import sys
import traceback

# ------------------------------- localizacao --------------------------------

DIR_ARCADOUCO = os.path.dirname(os.path.abspath(__file__))
DIR_FIXTURES = os.path.join(DIR_ARCADOUCO, "fixtures")
DIR_TESTES = os.path.join(DIR_ARCADOUCO, "testes")
DIR_CONTRA_PROVA = os.path.join(DIR_ARCADOUCO, "contra-prova")

# Prefixo da linha que o teste imprime e o runner le de volta. Formato:
#     RESULTADO|<PASSOU|REPROVOU|NAO_RODOU>|<nome>|<detalhe em uma linha>
# Uma linha so, sempre. O runner cai no exit code se a linha nao vier.
PREFIXO_RESULTADO = "RESULTADO|"

EXIT_OK, EXIT_FALHOU, EXIT_NAO_RODOU = 0, 1, 2


def raiz_do_repo(inicio=None):
    """Sobe de `inicio` ate achar a raiz do repositorio."""
    atual = os.path.abspath(inicio or DIR_ARCADOUCO)
    while True:
        if os.path.exists(os.path.join(atual, ".git")):
            return atual
        if os.path.isfile(os.path.join(atual, "docs", "PLANO-DE-TESTES.md")):
            return atual
        pai = os.path.dirname(atual)
        if pai == atual:
            raise NaoRodou("nao achei a raiz do repositorio subindo a partir de %s" % atual)
        atual = pai


def dir_lib():
    """Onde estao as DLLs do jogo. `SR_TESTES_LIB` sobrepoe (usado nos testes
    negativos: apontar para um diretorio vazio faz os testes de jogo NAO_RODAREM,
    que e como se prova que o caminho do 'nao consegui rodar' existe)."""
    return os.environ.get("SR_TESTES_LIB") or os.path.join(raiz_do_repo(), "lib")


# ------------------------------- excecoes -----------------------------------

class Falhou(Exception):
    """O teste REPROVOU (exit 1): observado != esperado."""


class NaoRodou(Exception):
    """O teste NAO CONSEGUIU RODAR (exit 2): falta dependencia.

    `faltando` e o nome curto do que falta ("lib/", "dotnet"), para as mensagens
    ficarem comparaveis entre testes.
    """

    def __init__(self, mensagem, faltando=None):
        super().__init__(mensagem)
        self.faltando = faltando or mensagem


# ------------------------------- dependencias -------------------------------

def precisa_lib(dlls=()):
    """Levanta NaoRodou se a lib/ do jogo nao estiver disponivel.

    `dlls` e a lista de arquivos que o teste de fato usa - declarar quais evita
    o "lib/ existe mas falta justo a que eu preciso", que e o pior dos mundos.
    Devolve o caminho da lib quando da para rodar.
    """
    raiz = dir_lib()
    if not os.path.isdir(raiz):
        raise NaoRodou(
            "lib/ do jogo ausente em %s (as DLLs sao gitignored: copie de "
            "<jogo>\\Stolen Realm_Data\\Managed\\ ou aponte SR_TESTES_LIB)" % raiz,
            faltando="lib/")
    faltando = [d for d in dlls if not os.path.isfile(os.path.join(raiz, d))]
    if faltando:
        raise NaoRodou(
            "lib/ existe em %s mas faltam: %s" % (raiz, ", ".join(sorted(faltando))),
            faltando="lib/%s" % faltando[0])
    return raiz


# O QUE CADA REQUISITO DO META SIGNIFICA. Novos requisitos entram AQUI (o META
# so aceita nomes que existem neste dicionario - requisito desconhecido e erro,
# nao aviso, senao um teste com nome errado viraria "pulado" para sempre).
def requisito(req):
    """Devolve (satisfeito, detalhe) para um nome de requisito."""
    if req == "lib/":
        raiz = dir_lib()
        if os.path.isdir(raiz):
            n = len([f for f in os.listdir(raiz) if f.lower().endswith(".dll")])
            return True, "lib/ do jogo em %s (%d DLLs)" % (raiz, n)
        return False, "lib/ do jogo ausente em %s" % raiz
    if req == "dotnet":
        exe = _achar_no_path("dotnet")
        if exe:
            return True, "dotnet em %s" % exe
        return False, "dotnet nao esta no PATH"
    return None, "requisito desconhecido: %r (registre em arcabouco.requisito)" % req


def _achar_no_path(nome):
    for pasta in os.environ.get("PATH", "").split(os.pathsep):
        alvo = os.path.join(pasta, nome)
        for candidato in (alvo, alvo + ".exe", alvo + ".cmd"):
            if os.path.isfile(candidato):
                return candidato
    return None


# ------------------------------- asserts ------------------------------------

def exigir(condicao, mensagem):
    if not condicao:
        raise Falhou(mensagem)


def igual(obtido, esperado, mensagem="valor"):
    if obtido != esperado:
        raise Falhou("%s: esperado %r, obtido %r" % (mensagem, esperado, obtido))


# ------------------------------- fixtures -----------------------------------
# CONVENCAO DE NOME (nao inventar outra):
#     fixtures/<caso>.entrada.<ext>    <- a entrada versionada
#     fixtures/<caso>.esperado.<ext>   <- a saida esperada versionada
# `<caso>` e o `nome` do META do teste. Extensao: json (padrao), csv, log, txt.

PAPEIS = ("entrada", "esperado")


def caminho_fixture(caso, papel, ext="json"):
    if papel not in PAPEIS:
        raise Falhou("papel de fixture tem de ser %s, veio %r" % (" ou ".join(PAPEIS), papel))
    nome = "%s.%s.%s" % (caso, papel, ext)
    caminho = os.path.join(DIR_FIXTURES, nome)
    if not os.path.isfile(caminho):
        # Fixture versionada ausente e DEFEITO (exit 1), nao dependencia:
        # ela tem de estar no repositorio.
        raise Falhou("fixture ausente: %s (convencao: <nome-do-teste>.<%s>.<ext>)" % (nome, "|".join(PAPEIS)))
    return caminho


def ler_json(caso, papel="entrada", ext="json"):
    with open(caminho_fixture(caso, papel, ext), encoding="utf-8") as fh:
        return json.load(fh)


def ler_texto(caso, papel="entrada", ext="log"):
    with open(caminho_fixture(caso, papel, ext), encoding="utf-8") as fh:
        return fh.read()


# ------------------------------- float32 ------------------------------------

def f32(x):
    """Arredonda um numero para o float de 32 bits (single) do motor.

    O jogo calcula em `float`. Onde float e double discordam (ver
    `fixtures/soma-aura.entrada.json` -> auditoria_float_vs_double), a diferenca
    aparece EXATAMENTE nas bordas .5, que e onde o teste olha. Quando o teste
    compara com numero que veio do motor, use f32 no caminho de conta.
    """
    return struct.unpack("<f", struct.pack("<f", float(x)))[0]


# ------------------------------- execucao -----------------------------------

def _linha(estado, nome, detalhe):
    detalhe = " ".join(str(detalhe).split())
    return "%s%s|%s|%s" % (PREFIXO_RESULTADO, estado, nome, detalhe)


def roda(meta, corpo):
    """Executa o corpo do teste e traduz o resultado no exit code.

    Devolve o exit code (e imprime a linha que o runner le). Nao levanta.
    """
    nome = meta.get("nome") or "?"
    try:
        corpo()
    except NaoRodou as erro:
        print(_linha("NAO_RODOU", nome, erro))
        return EXIT_NAO_RODOU
    except Falhou as erro:
        print(_linha("REPROVOU", nome, erro))
        return EXIT_FALHOU
    except AssertionError as erro:
        print(_linha("REPROVOU", nome, "assert do Python: %s" % erro))
        return EXIT_FALHOU
    except Exception:
        # Excecao inesperada e FALHA (1), nunca "nao rodou" (2): o teste rodou e
        # quebrou. Mascarar isso como dependencia esconderia defeito de verdade.
        print(_linha("REPROVOU", nome, "excecao inesperada: " + traceback.format_exc()))
        return EXIT_FALHOU
    print(_linha("PASSOU", nome, meta.get("descricao") or "ok"))
    return EXIT_OK


def main(meta, corpo):
    """Ponto de entrada padrao de um arquivo de teste."""
    sys.exit(roda(meta, corpo))


def ambiente_do_teste(extra=None):
    """Ambiente para rodar um teste em SUBPROCESSO (o runner usa; o meta-teste
    da prova de fogo usa tambem, para exercitar o caminho real)."""
    amb = dict(os.environ)
    amb["PYTHONPATH"] = DIR_ARCADOUCO + os.pathsep + amb.get("PYTHONPATH", "")
    amb["PYTHONIOENCODING"] = "utf-8"
    amb["PYTHONDONTWRITEBYTECODE"] = "1"
    if extra:
        amb.update(extra)
    return amb


def executar_arquivo(caminho, extra_env=None, timeout=300):
    """Roda OUTRO arquivo de teste como o runner roda: subprocesso, exit code cru.

    Devolve (codigo, saida). Isolar em subprocesso e o que impede um teste que
    estoura de derrubar a suite inteira - e o que faz o exit code do teste ser
    uma informacao confiavel.
    """
    proc = subprocess.run(
        [sys.executable, os.path.abspath(caminho)],
        cwd=raiz_do_repo(),
        env=ambiente_do_teste(extra_env),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        universal_newlines=True, timeout=timeout,
    )
    return proc.returncode, proc.stdout or ""


# ------------------------------- leitura de META ----------------------------

def ler_meta(caminho):
    """Le o dict META de um arquivo de teste SEM importar o arquivo.

    Usa `ast`, entao a leitura nao executa o teste nem depende do ambiente do
    teste (importar para ler metadata significaria que o runner herda qualquer
    erro de import do teste). O META tem de ser um literal.
    """
    import ast

    with open(caminho, encoding="utf-8") as fh:
        arvore = ast.parse(fh.read(), filename=caminho)
    for no in arvore.body:
        alvos = no.targets if isinstance(no, ast.Assign) else ([no.target] if isinstance(no, ast.AnnAssign) else [])
        for alvo in alvos:
            if isinstance(alvo, ast.Name) and alvo.id == "META":
                try:
                    return ast.literal_eval(no.value)
                except ValueError as erro:
                    raise Falhou("META de %s nao e um literal (%s)" % (caminho, erro))
    raise Falhou("arquivo de teste sem META: %s" % caminho)


def validar_meta(meta, caminho):
    """Confere o contrato do META. Erro aqui e defeito do teste."""
    for campo in ("nome", "categoria", "descricao"):
        if not meta.get(campo):
            raise Falhou("%s: META sem o campo obrigatorio %r" % (caminho, campo))
    if meta["categoria"] not in ("pura", "jogo"):
        raise Falhou("%s: categoria tem de ser 'pura' ou 'jogo', veio %r" % (caminho, meta["categoria"]))
    for req in meta.get("requer", []):
        ok, detalhe = requisito(req)
        if ok is None:
            raise Falhou("%s: %s" % (caminho, detalhe))
    esperado = meta.get("esperado", "passar")
    if esperado not in ("passar", "reprovar"):
        raise Falhou("%s: 'esperado' tem de ser 'passar' ou 'reprovar', veio %r" % (caminho, esperado))
    return meta
