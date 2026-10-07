#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova) — A5: afirma o FALSO — o rollback REMOVE um diretorio que ja
existia no perfil (a pasta vazia `plugins/AUT4Probe`), como se o perfil "voltasse"
ao estado anterior.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE. Se ele PASSA, o
perfil nao volta ao estado anterior (achado A5 da AUT-4R2).
"""
import os
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import comum as C  # noqa: E402
import t_aut4_execucao as T  # noqa: E402

META = {
    "nome": "cp-aut5-isca-dir-pre-existente-removido",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: rollback remove diretorio pre-existente — TEM de reprovar",
    "esperado": "reprovar",
}


def corpo():
    col = C.coletor()
    plano = T._plano()
    with tempfile.TemporaryDirectory(prefix="isca-a5-") as raiz:
        dll = T._dll_falsa(raiz)
        perfil = os.path.join(raiz, "perfil-isca5")
        out = os.path.join(raiz, "out-isca5")
        pasta = os.path.join(perfil, "BepInEx", "plugins", "AUT4Probe")
        os.makedirs(pasta)                       # pasta PRE-EXISTENTE (vazia)
        stub, _ = T._stub(raiz, perfil, out, marcador="ISCA-A5")
        r, cod = col.executar_rodada(plano, perfil_dir=perfil, out_dir=out, dll_probe=dll,
                                     autorizado=True, jogo_disponivel=True,
                                     confirmacao="coleta",
                                     comando_lancamento=[sys.executable, stub],
                                     timeout_s=30, poll_s=0.1)
        C.arc.igual(cod, 0, "preparacao: a rodada conclui")
        # A afirmacao FALSA: o rollback apaga a pasta que ja existia antes.
        C.arc.exigir(not os.path.isdir(pasta),
                     "pasta pre-existente deveria ter sido removida (AFIRMACAO FALSA — isca TEM de reprovar)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
