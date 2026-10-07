#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUT-4 — a coleta runtime e OPT-IN e o default e OFFLINE.

Sem autorizacao explicita (ou sem jogo), a decisao NAO libera coleta e o
resultado e NAO_EXERCITADO — nunca dados fabricados. Este teste e puro: nao
toca em jogo, rede nem perfil.
"""
import comum as C

META = {
    "nome": "aut4-autorizacao",
    "categoria": "pura",
    "requer": [],
    "descricao": ("default offline: coleta so com autorizacao E confirmacao E jogo; "
                  "qualquer falta devolve NAO_EXERCITADO sem liberar coleta"),
}


def corpo():
    col = C.coletor()

    # 1. desautorizado (default) — nunca libera, mesmo com jogo disponivel
    d = col.decidir_autorizacao(autorizado=False, jogo_disponivel=True)
    C.arc.igual(d["pode_coletar"], False, "desautorizado nao pode coletar")
    C.arc.igual(d["status"], "NAO_EXERCITADO", "desautorizado -> status")
    C.arc.exigir(d.get("motivo"), "toda decisao precisa de motivo legivel")
    C.arc.igual(d.get("dados_sinteticos"), False, "nada de dado sintetico no caminho offline")

    # 2. autorizado, MAS sem acesso ao jogo — NAO_EXERCITADO, nao inventa
    d = col.decidir_autorizacao(autorizado=True, jogo_disponivel=False, confirmacao="coleta")
    C.arc.igual(d["pode_coletar"], False, "sem jogo nao coleta")
    C.arc.igual(d["status"], "NAO_EXERCITADO", "sem jogo -> NAO_EXERCITADO")
    C.arc.exigir("jogo" in d["motivo"].lower(), "o motivo tem de nomear a falta de jogo")

    # 3. autorizado + jogo, mas sem confirmacao da rodada — ainda nao coleta
    d = col.decidir_autorizacao(autorizado=True, jogo_disponivel=True, confirmacao=None)
    C.arc.igual(d["pode_coletar"], False, "sem confirmacao nao coleta")
    C.arc.igual(d["status"], "NAO_EXERCITADO", "sem confirmacao -> NAO_EXERCITADO")

    # 4. os tres juntos — so aqui libera
    d = col.decidir_autorizacao(autorizado=True, jogo_disponivel=True, confirmacao="coleta")
    C.arc.igual(d["pode_coletar"], True, "autorizado+confirmado+com jogo pode coletar")
    C.arc.igual(d["status"], "AUTORIZADO", "status de liberacao")
    C.arc.igual(d.get("dados_sinteticos"), False, "nem no modo autorizado ha dado sintetico")

    # 5. o resultado sem-jogo nao carrega observacao nem screenshot
    r = col.resultado_nao_exercitado("sem acesso autorizado ao jogo")
    C.arc.igual(r["status"], "NAO_EXERCITADO", "resultado nao exercitado")
    C.arc.igual(r["observacoes"], [], "sem observacoes fabricadas")
    C.arc.igual(r.get("screenshot"), None, "sem screenshot sintetico")


if __name__ == "__main__":
    C.arc.main(META, corpo)
