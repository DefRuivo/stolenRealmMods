#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova) — A1: afirma o FALSO — um `aut4probe.json` de OUTRA rodada
ja basta para o driver confirmar (`CONCLUIDO`).

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE. Se ele PASSA, o
driver esta confirmando sucesso sem prova de execucao (achado A1 da AUT-4R2) — e o
aceite proibe exatamente isso ("sinal nao e efeito").
"""
import os
import sys
import tempfile
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import comum as C  # noqa: E402
import t_aut4_execucao as T  # noqa: E402

META = {
    "nome": "cp-aut5-isca-sem-prova-execucao",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: JSON de rodada anterior confirma a rodada — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    plano = T._plano()
    with tempfile.TemporaryDirectory(prefix="isca-a1-") as raiz:
        dll = T._dll_falsa(raiz)
        _, cod1, perfil, out, _ = T._rodar(col, plano, raiz, "isca1", dll)
        C.arc.igual(cod1, 0, "preparacao: a 1a rodada (que escreve) conclui")
        time.sleep(1.2)          # o JSON fica estritamente mais antigo que o novo lancamento
        stub, _ = T._stub(raiz, perfil, out, marcador="ISCA-A1")
        r, cod = col.executar_rodada(plano, perfil_dir=perfil, out_dir=out, dll_probe=dll,
                                     autorizado=True, jogo_disponivel=True,
                                     confirmacao="coleta",
                                     comando_lancamento=[sys.executable, stub, "--nao-escreve"],
                                     timeout_s=1, poll_s=0.1)
        # A afirmacao FALSA: o JSON de outra rodada confirma ESTA rodada.
        C.arc.igual(r["status"], "CONCLUIDO",
                    "JSON de outra rodada deveria confirmar (AFIRMACAO FALSA — a isca tem de reprovar)")
        C.arc.igual(cod, 0, "exit 0 sem prova de execucao (AFIRMACAO FALSA)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
