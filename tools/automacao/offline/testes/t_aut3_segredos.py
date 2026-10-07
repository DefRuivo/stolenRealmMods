#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teste do achado de SEGREDOS da AUT-3R (AUT-3F): os scanners NAO podem imprimir
o prefixo do token achado, e o runner sanitiza o que serializa.

Roda os scanners REAIS numa copia minima do repo (para cada scanner, sua propria
copia em `tools/`), planta um token FALSO, e exige:
  * exit 1 com o token plantado;
  * NENHUM prefixo do token na saida (nem o valor, nem os primeiros 14 chars);
  * exit 0 depois de remover o token.

O token e montado por concatenacao (nunca fica literal no arquivo) e e FALSO.

Uso:  python tools/automacao/offline/testes/t_aut3_segredos.py
Exit: 0 = tudo passou; 1 = alguma verificacao reprovou; 2 = nao consegui rodar.
"""
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
LIB_DIR = os.path.dirname(AQUI)
TOOLS_REAIS = os.path.dirname(os.path.dirname(os.path.dirname(LIB_DIR)))  # raiz do repo
sys.path.insert(0, LIB_DIR)

import aut3_lib  # noqa: E402

RESULTADOS = []
PY = sys.executable
# token FALSO, nunca um valor real; quebrado em pedacos para nao virar literal.
TOKEN_FALSO = "tss_" + "A1b2C3d4E5f6G7h8" + "I9j0K1l2M3n4O5p6"


def checar(nome, cond, detalhe=""):
    RESULTADOS.append((nome, bool(cond), detalhe))
    print("RESULTADO|%s|%s|%s" % ("PASSOU" if cond else "REPROVOU", nome, detalhe))
    return bool(cond)


def _repo_com_scanners(tmp):
    """Repo git minimo com copias dos scanners em tools/ (mesmo layout do sandbox)."""
    os.makedirs(os.path.join(tmp, "tools"))
    for nome in ("check_segredos.py", "check_padroes_segredo.py"):
        shutil.copyfile(os.path.join(TOOLS_REAIS, "tools", nome),
                        os.path.join(tmp, "tools", nome))
    aut3_lib.run_cmd(["git", "init", "-q"], cwd=tmp)
    aut3_lib.run_cmd(["git", "config", "user.email", "t@t"], cwd=tmp)
    aut3_lib.run_cmd(["git", "config", "user.name", "t"], cwd=tmp)
    return tmp


def test_scanner_nao_imprime_prefixo(tmp):
    repo = _repo_com_scanners(os.path.join(tmp, "seg"))
    alvo = os.path.join(repo, "vazamento.txt")
    with open(alvo, "w", encoding="utf-8") as fh:
        fh.write("valor = %s\n" % TOKEN_FALSO)
    aut3_lib.run_cmd(["git", "add", "-f", "vazamento.txt"], cwd=repo)

    r = aut3_lib.run_cmd([PY, os.path.join(repo, "tools", "check_segredos.py")], cwd=repo, timeout=120)
    saida = (r["stdout"] or "") + (r["stderr"] or "")
    checar("check_segredos reprova o token plantado", r["exit_code"] == 1,
           "exit=%s" % r["exit_code"])
    checar("check_segredos NAO imprime o token", TOKEN_FALSO not in saida)
    checar("check_segredos NAO imprime o prefixo (14 chars)",
           TOKEN_FALSO[:14] not in saida)
    checar("check_segredos marca REDACTED", "<REDACTED" in saida or "REDACTED" in saida)

    # remove o token e exige verde (a trava sabe dizer NAO e sabe dizer SIM)
    with open(alvo, "w", encoding="utf-8") as fh:
        fh.write("sem segredo aqui\n")
    r2 = aut3_lib.run_cmd([PY, os.path.join(repo, "tools", "check_segredos.py")], cwd=repo, timeout=120)
    checar("check_segredos verde apos remover o token", r2["exit_code"] == 0,
           "exit=%s" % r2["exit_code"])


def test_mascara_sem_prefixo(tmp):
    """O detector generico monta a mensagem sem prefixo do valor."""
    sys.path.insert(0, os.path.join(TOOLS_REAIS, "tools"))
    import check_padroes_segredo as cps  # noqa: E402
    valor = "A1b2C3d4E5f6G7h8" + "I9j0K1l2M3n4O5p6" + "Q7r8S9t0"
    msg = cps.mascara(valor)
    checar("mascara NAO traz o valor", valor not in msg)
    checar("mascara NAO traz os 14 primeiros chars", valor[:14] not in msg)
    checar("mascara traz o tamanho", str(len(valor)) in msg)
    checar("mascara marca REDACTED", "<REDACTED" in msg or "REDACTED" in msg)


def test_runner_sanitiza(tmp):
    tok = "tss_" + "A1b2C3d4E5f6G7h8I9j0K1l2"
    limpo = aut3_lib.sanitiza("falhou: %s" % tok)
    checar("aut3_lib.sanitiza remove o token", tok not in limpo)
    checar("aut3_lib.sanitiza preserva contexto", "falhou:" in limpo)
    checar("aut3_lib.sanitiza idempotente no texto normal",
           aut3_lib.sanitiza("texto normal") == "texto normal")


def main():
    if not os.path.isfile(os.path.join(TOOLS_REAIS, "tools", "check_segredos.py")):
        print("nao encontrei os scanners em %s" % TOOLS_REAIS)
        return 2
    with tempfile.TemporaryDirectory(prefix="t-aut3-seg-", dir=aut3_lib.area_trabalho()) as tmp:
        test_scanner_nao_imprime_prefixo(tmp)
        test_mascara_sem_prefixo(tmp)
        test_runner_sanitiza(tmp)
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
