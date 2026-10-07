#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testes do nucleo da bancada offline AUT-3 (tools/automacao/offline/aut3_lib.py).

Rodam SEM o jogo e SEM o perfil. Cobrem a regra central: exit code de comando
nunca vira verde por omissao, e "nao exercitado" e um estado SEPARADO de OK.

Uso:  python tools/automacao/offline/testes/t_aut3_lib.py
Exit: 0 = tudo passou; 1 = alguma verificacao reprovou; 2 = nao consegui rodar.
"""
import hashlib
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.dirname(AQUI)
sys.path.insert(0, LIB_DIR)

import aut3_lib  # noqa: E402

RESULTADOS = []


def checar(nome, cond, detalhe=""):
    RESULTADOS.append((nome, bool(cond), detalhe))
    print("RESULTADO|%s|%s|%s" % ("PASSOU" if cond else "REPROVOU", nome, detalhe))
    return bool(cond)


def test_sha256_file(tmp):
    conteudo = b"abc"
    p = os.path.join(tmp, "x.bin")
    with open(p, "wb") as fh:
        fh.write(conteudo)
    esperado = hashlib.sha256(conteudo).hexdigest()
    checar("sha256_file bate com hashlib", aut3_lib.sha256_file(p) == esperado)
    checar("sha256_file de inexistente e None", aut3_lib.sha256_file(p + ".nada") is None)


def test_run_cmd_ok(tmp):
    r = aut3_lib.run_cmd([sys.executable, "-c", "print('oi')"])
    checar("run_cmd exit 0", r["exit_code"] == 0)
    checar("run_cmd captura stdout", "oi" in r["stdout"])
    checar("run_cmd tempo positivo", r["segundos"] >= 0)
    checar("avalia exit 0 -> OK", aut3_lib.avalia(r, 0) == "OK")


def test_run_cmd_falha(tmp):
    r = aut3_lib.run_cmd([sys.executable, "-c", "import sys; sys.exit(3)"])
    checar("run_cmd exit 3", r["exit_code"] == 3)
    checar("avalia exit != esperado -> REPROVOU", aut3_lib.avalia(r, 0) == "REPROVOU")
    # erro de comando NAO pode virar verde: exit 1 esperado 0 continua REPROVOU
    checar("err != verde", aut3_lib.avalia(r, 0) != "OK")


def test_run_cmd_inexistente(tmp):
    r = aut3_lib.run_cmd(["programa-que-nao-existe-aut3"])
    checar("comando inexistente -> NAO_EXERCITADO", aut3_lib.avalia(r, 0) == "NAO_EXERCITADO")
    checar("comando inexistente registra motivo", bool(r.get("erro_lancamento")))


def test_run_cmd_timeout(tmp):
    r = aut3_lib.run_cmd([sys.executable, "-c", "import time; time.sleep(5)"], timeout=0.5)
    checar("timeout e flag", r["timeout"] is True)
    checar("timeout -> NAO_EXERCITADO", aut3_lib.avalia(r, 0) == "NAO_EXERCITADO")


def test_veredito():
    checar("veredito so OK -> VERDE", aut3_lib.veredito([{"estado": "OK"}, {"estado": "OK"}]) == "VERDE")
    checar("veredito com REPROVOU -> REPROVADO",
           aut3_lib.veredito([{"estado": "OK"}, {"estado": "REPROVOU"}]) == "REPROVADO")
    checar("veredito com NAO_EXERCITADO -> INCOMPLETO",
           aut3_lib.veredito([{"estado": "OK"}, {"estado": "NAO_EXERCITADO"}]) == "INCOMPLETO")
    checar("veredito vazio -> INCOMPLETO", aut3_lib.veredito([]) == "INCOMPLETO")


def test_sanitiza():
    """O que o runner serializa nunca pode carregar prefixo de credencial (AUT-3F)."""
    tok = "tss_" + "A1b2C3d4E5f6G7h8I9j0K1l2"
    limpo = aut3_lib.sanitiza("achado: %s (arquivo x)" % tok)
    checar("sanitiza remove o token", tok not in limpo)
    checar("sanitiza remove o prefixo de 14", tok[:14] not in limpo)
    checar("sanitiza preserva o contexto", "arquivo x" in limpo)
    checar("sanitiza marca REDACTED", "<REDACTED>" in limpo)
    checar("sanitiza texto normal intacto", aut3_lib.sanitiza("nada aqui") == "nada aqui")
    checar("sanitiza vazio/intacto", aut3_lib.sanitiza("") == "" and aut3_lib.sanitiza(None) is None)


def test_snapshot_hashes(tmp):
    p = os.path.join(tmp, "a.txt")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("oi")
    h1 = aut3_lib.snapshot_arquivos([p])
    with open(p, "w", encoding="utf-8") as fh:
        fh.write("outro")
    h2 = aut3_lib.snapshot_arquivos([p])
    checar("snapshot muda quando o arquivo muda", h1 != h2)
    checar("snapshot lista ausente como None",
           aut3_lib.snapshot_arquivos([p + ".sumiu"])[os.path.basename(p) + ".sumiu"] is None)


def main():
    import tempfile
    with tempfile.TemporaryDirectory(prefix="t-aut3-lib-", dir=aut3_lib.area_trabalho()) as tmp:
        test_sha256_file(tmp)
        test_run_cmd_ok(tmp)
        test_run_cmd_falha(tmp)
        test_run_cmd_inexistente(tmp)
        test_run_cmd_timeout(tmp)
        test_veredito()
        test_snapshot_hashes(tmp)
        test_sanitiza()
    falhas = [n for n, ok, _ in RESULTADOS if not ok]
    print()
    print("total: %d | falhas: %d" % (len(RESULTADOS), len(falhas)))
    if falhas:
        print("REPROVADAS: %s" % ", ".join(falhas))
        return 1
    print("TUDO OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
