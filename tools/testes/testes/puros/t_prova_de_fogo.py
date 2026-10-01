#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A PROVA DE FOGO DO PROPRIO ARCADOUCO (o teste que testa o runner).

POR QUE ESTE TESTE EXISTE
-------------------------
A regra do plano e "todo teste tem de ser MOSTRADO REPROVANDO". O runner tambem e
uma trava - e trava que nunca reprovou nao vale nada. Entao o runner precisa de um
teste que o exercite contra uma isca CONHECIDA:

    tools/testes/contra-prova/cp_defeito_soma_aura.py    -> TEM DE REPROVAR (exit 1)
    tools/testes/contra-prova/cp_corrigido_soma_aura.py  -> tem de PASSAR  (exit 0)

e os dois sao o MESMO teste: fora do bloco marcado BLOCO-DO-DEFEITO os arquivos
sao identicos (conferido por comparacao de texto aqui embaixo). Se um dia o runner
parar de reprovar a isca, ESTE teste fica vermelho - a trava do runner e vigiada.

Este arquivo e de logica pura: nao precisa do jogo, so de Python.
"""
import os
import subprocess
import sys

import arcabouco as arc

META = {
    "nome": "prova-de-fogo",
    "categoria": "pura",
    "requer": [],
    "descricao": "o runner reprova a isca (e pelo motivo certo) e aprova o mesmo teste corrigido",
}

ISCA = os.path.join(arc.DIR_CONTRA_PROVA, "cp_defeito_soma_aura.py")
CORRIGIDO = os.path.join(arc.DIR_CONTRA_PROVA, "cp_corrigido_soma_aura.py")


def corpo_sem_bloco(caminho):
    """Texto do arquivo a partir do `def corpo`, sem as linhas do BLOCO-DO-DEFEITO.

    E o que prova que as duas metades sao o MESMO teste: o META fica de fora
    (ele difere de proposito, em `esperado`) e o bloco marcado tambem (e o defeito).
    """
    with open(caminho, encoding="utf-8") as fh:
        linhas = fh.read().splitlines()
    inicio = next((n for n, linha in enumerate(linhas) if linha.startswith("def corpo")), None)
    arc.exigir(inicio is not None, "%s nao tem `def corpo`" % caminho)
    dentro, guardadas = False, []
    for linha in linhas[inicio:]:
        if linha.strip().startswith("# >>> BLOCO-DO-DEFEITO"):
            dentro = True
            continue
        if linha.strip().startswith("# <<< BLOCO-DO-DEFEITO"):
            dentro = False
            continue
        if not dentro:
            guardadas.append(linha)
    return "\n".join(guardadas)


def rodar_runner(alvo):
    proc = subprocess.run(
        [sys.executable, os.path.join(arc.DIR_ARCADOUCO, "roda_testes.py"), "--teste", alvo],
        cwd=arc.raiz_do_repo(), env=arc.ambiente_do_teste(),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, timeout=300)
    return proc.returncode, proc.stdout or ""


def corpo():
    # ------------------------------------------------------------------ 1.
    # A isca REPROVA de verdade - e pelo motivo certo (o numero somado a mao),
    # nao por ter quebrado. Sem esta segunda parte, um isca que estoura (ImportError,
    # SyntaxError) tambem "reprovaria" e o teste nao perceberia.
    codigo_isca, saida_isca = arc.executar_arquivo(ISCA)
    ultima = (saida_isca.strip().splitlines() or ["<sem saida>"])[-1]
    arc.igual(codigo_isca, arc.EXIT_FALHOU,
              "a isca tinha de REPROVAR (exit 1); saida: %s" % ultima)
    arc.exigir("REPROVOU" in saida_isca, "a isca saiu != 0 mas nao pelo caminho REPROVOU: %s" % ultima)
    arc.exigir("40" in saida_isca and "44" in saida_isca,
               "a isca tinha de reprovar no NUMERO (esperado 40, motor 44), nao em outra coisa: %s" % ultima)

    # ------------------------------------------------------------------ 2.
    # O MESMO teste, sem o defeito, PASSA.
    codigo_corrigido, saida_corrigido = arc.executar_arquivo(CORRIGIDO)
    ultima_corrigido = (saida_corrigido.strip().splitlines() or ["<sem saida>"])[-1]
    arc.igual(codigo_corrigido, arc.EXIT_OK,
              "o corrigido tinha de PASSAR (exit 0); saida: %s" % ultima_corrigido)

    # ------------------------------------------------------------------ 3.
    # Eles sao o MESMO teste (fora do bloco do defeito). Sem isto, "o mesmo teste
    # passando depois" seria so uma frase na documentacao.
    arc.igual(corpo_sem_bloco(ISCA), corpo_sem_bloco(CORRIGIDO),
              "cp_defeito e cp_corrigido divergem fora do bloco do defeito - nao sao o mesmo teste")

    # ------------------------------------------------------------------ 4.
    # Nivel RUNNER: com `--teste` na isca, o runner sabe que ela tem de reprovar
    # e por isso sai VERDE (exit 0) marcando PROVA OK; com o corrigido, sai verde
    # marcando PASSOU. Se o runner perder essa inversao, este teste cai.
    codigo_r_isca, saida_r_isca = rodar_runner(ISCA)
    arc.igual(codigo_r_isca, 0,
              "o runner tinha de sair 0 na isca (ele ESPERA que ela reprove); saida:\n%s" % saida_r_isca)
    arc.exigir("PROVA OK" in saida_r_isca,
               "o runner saiu 0 na isca mas nao marcou PROVA OK; saida:\n%s" % saida_r_isca)

    codigo_r_corrigido, saida_r_corrigido = rodar_runner(CORRIGIDO)
    arc.igual(codigo_r_corrigido, 0, "o runner tinha de sair 0 no corrigido; saida:\n%s" % saida_r_corrigido)
    arc.exigir("PASSOU" in saida_r_corrigido,
               "o runner nao marcou PASSOU no corrigido; saida:\n%s" % saida_r_corrigido)

    print("isca REPROVOU (exit 1) pelo numero; corrigido PASSOU (exit 0); "
          "runner marcou PROVA OK/PASSOU e saiu 0 - o runner reprova de verdade")


if __name__ == "__main__":
    arc.main(META, corpo)
