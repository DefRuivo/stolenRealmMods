#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""COR-AUT6 (t_6fcb39da): as duas suites do avaliador AUT-6 rodam na suite PURA do projeto.

O QUE ESTE TESTE GARANTE
------------------------
Os achados E1-E9 da revisao independente AUT-6R viraram regressao PERMANENTE. Aqui elas entram
na suite pura (o que roda no CI) como UM teste: se qualquer uma das duas suites do AUT-6 sair
diferente de 0, esta reprova e o motivo sai literal (a ultima linha de cada suite).

O que NAO e prova: nada disto toca o jogo. As duas suites sao OFFLINE - fixtures rotuladas,
tabelas geradas, asset no offset documentado e uma simulacao de CONTRATO com bytes e manifest
proprios em pasta temporaria (`ambiente_prova=teste_contrato`), que o avaliador marca como
"nao prova produto". Instalacao/restauracao em runtime continua NAO EXERCITADA.
"""
import os
import subprocess
import sys

import arcabouco as arc

AQUI = os.path.dirname(os.path.abspath(__file__))
# tools/testes/testes/puros -> tools
TOOLS = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
REPO = os.path.dirname(TOOLS)

SUITES = [
    os.path.join(TOOLS, "automacao", "aut6", "test_cobertura_aut6.py"),
    os.path.join(TOOLS, "automacao", "aut6", "test_regressoes_cor_aut6.py"),
]

META = {
    "nome": "aut6-cor-e1-e9",
    "categoria": "pura",
    "requer": [],
    "descricao": "AUT-6/COR-AUT6: as duas suites offline do avaliador de tooltips/shrines por "
                 "personagem (contrato v1, 25 casos de fixture + 26 regressoes E1-E9) rodam e "
                 "saem 0 - nenhuma aprovacao de runtime e nenhum alvo de produto",
}


def corpo():
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
    for suite in SUITES:
        arc.exigir(os.path.isfile(suite), "suite do AUT-6 ausente: %s" % suite)
        p = subprocess.run([sys.executable, suite], cwd=REPO, env=env, capture_output=True,
                           text=True, encoding="utf-8", timeout=600)
        linhas = [l for l in ((p.stdout or "") + (p.stderr or "")).splitlines() if l.strip()]
        resumo = linhas[-1] if linhas else "(sem saida)"
        arc.exigir(p.returncode == 0,
                   "suite %s saiu %d: %s" % (os.path.basename(suite), p.returncode, resumo))
        print("%s -> %s" % (os.path.basename(suite), resumo))


if __name__ == "__main__":
    arc.main(META, corpo)
