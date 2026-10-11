#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KIT-08 - contra-prova: defeito plantado DEVE reprovar o conjunto EXATO de testes.

Cada defeito e um par (busca, troca) aplicado a uma COPIA de `visualizador.py`
em `scratch/kit/k08/contra/`; a SUITE REAL (`teste_visualizador_kit08.py`) roda
contra a copia (via `KIT08_MODULO`) e o discriminador exige que o conjunto de
testes que falham seja EXATAMENTE o esperado. Conjunto diferente -> RECUSADO
(inclusive um defeito que nao derruba nada = falso-verde).

Exit: 0 = todos os defeitos RECUSARAM como esperado (VERDE);
      1 = algum defeito passou batido ou derrubou conjunto diferente.
Sem rede, sem jogo, sem tocar em arquivo versionado alem da copia em scratch/.
"""
import os
import re
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))
MOD_REAL = os.path.join(AQUI, "visualizador.py")
SUITE = os.path.join(AQUI, "teste_visualizador_kit08.py")
KIT09 = os.path.join(RAIZ, "tools", "automacao", "cenarios", "kit09.py")
CONTRA = os.path.join(RAIZ, "scratch", "kit", "k08", "contra")

_SAIDA = re.compile(r"^(FAIL|ERROR): (\S+)")

DEFEITOS = [
    dict(nome="D1_escape_desligado",
         busca="    return html.escape(str(texto), quote=True)",
         troca="    return str(texto)",
         esperados={"test_escapar_payload_vira_texto",
                    "test_html_sem_tag_script_de_dado"}),
    dict(nome="D2_csp_script_inline",
         busca="script-src 'none'; base-uri 'none'; form-action 'none'",
         troca="script-src 'unsafe-inline'; base-uri 'none'; form-action 'none'",
         esperados={"test_csp_script_none"}),
    dict(nome="D3_referencia_sempre_segura",
         busca="    if not isinstance(ref, str):",
         troca='    return True, None  # D3: aceita tudo\n    if not isinstance(ref, str):',
         esperados={"test_recusa_esquemas_e_absolutos", "test_imagem_remota_recusada",
                    "test_html_sem_rede"}),
    dict(nome="D4_contexto_sempre_compativel",
         busca="    return (not motivos), motivos",
         troca="    return True, motivos",
         esperados={"test_contexto_incompativel_recusa", "test_contexto_incompleto_recusa"}),
    dict(nome="D5_stale_ignorado",
         busca="    return bool(motivos), motivos",
         troca="    return False, motivos",
         esperados={"test_stale_quando_fonte_muda",
                    "test_stale_quando_contexto_atual_omite_hash"}),
    dict(nome="D6_ok_sem_runtime_passa",
         busca='    if estado == OK and provou and proc == "runtime":',
         troca="    if estado == OK:",
         esperados={"test_fixture_nunca_passa"}),
    dict(nome="D8_guard_fixture_desligado",
         busca='        return "NAO_EXERCITADO" if fixture else "PASSOU"',
         troca='        return "PASSOU"',
         esperados={"test_fixture_rotulada_nunca_passa_no_doc"}),
    # falso-verde: mutacao cosmetica que NAO derruba nada -> conjunto vazio != esperado
    dict(nome="D7_falso_verde_sem_efeito",
         busca="AQUI = os.path.dirname(os.path.abspath(__file__))",
         troca="AQUI = os.path.dirname(os.path.abspath(__file__))  # noop",
         esperados={"test_inexistente_que_deveria_falhar"},
         falso_verde=True),
]


def _rodar_suite(caminho_mod):
    env = dict(os.environ)
    env["KIT08_MODULO"] = caminho_mod
    env["KIT08_KIT09"] = KIT09
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    p = subprocess.run([sys.executable, SUITE], capture_output=True, text=True,
                       cwd=RAIZ, env=env)
    falhas = set()
    for linha in (p.stdout + p.stderr).splitlines():
        m = _SAIDA.match(linha.strip())
        if m:
            falhas.add(m.group(2))
    return p.returncode, falhas


def _aplicar_defeito(texto, defeito):
    if texto.count(defeito["busca"]) != 1:
        raise RuntimeError("ancora %r aparece %d vezes (esperado 1) - contra-prova "
                           "invalida" % (defeito["busca"], texto.count(defeito["busca"])))
    return texto.replace(defeito["busca"], defeito["troca"])


def main():
    with open(MOD_REAL, encoding="utf-8") as fh:
        base = fh.read()
    if os.path.isdir(CONTRA):
        shutil.rmtree(CONTRA)
    os.makedirs(CONTRA, exist_ok=True)

    # 0) controle positivo: a suite REAL deve passar (VERDE) antes de tudo
    rc, falhas = _rodar_suite(MOD_REAL)
    if rc != 0 or falhas:
        print("CONTROLE_base|RECUSADO|a suite real nao esta verde: rc=%d falhas=%s"
              % (rc, sorted(falhas)))
        return 1
    print("CONTROLE_base|OK|suite real verde (exit 0)")

    ok_total = 0
    for defeito in DEFEITOS:
        destino = os.path.join(CONTRA, "%s_visualizador.py" % defeito["nome"])
        try:
            mutado = _aplicar_defeito(base, defeito)
        except RuntimeError as erro:
            print("%s|RECUSADO|ancora invalida: %s" % (defeito["nome"], erro))
            return 1
        with open(destino, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(mutado)
        rc, falhas = _rodar_suite(destino)
        if defeito.get("falso_verde"):
            # o controle falso-verde DEVE ser recusado: um defeito que nao derruba o
            # conjunto declarado nao pode ser aceito como contra-prova valida.
            if falhas != defeito["esperados"]:
                print("%s|RECUSOU|falso-verde nao virou verde (observado=%s)"
                      % (defeito["nome"], sorted(falhas)))
                ok_total += 1
            else:
                print("%s|ACEITOU INDEVIDAMENTE|observado=%s" % (defeito["nome"], sorted(falhas)))
                return 1
        elif falhas == defeito["esperados"]:
            print("%s|RECUSOU|falhas=%s (exato)" % (defeito["nome"], sorted(falhas)))
            ok_total += 1
        else:
            print("%s|RECUSADO|esperado=%s observado=%s (rc=%d)"
                  % (defeito["nome"], sorted(defeito["esperados"]),
                     sorted(falhas), rc))
            return 1

    print("VEREDITO KIT-08 contra-prova: VERDE (%d/%d defeitos recusados exato)"
          % (ok_total, len(DEFEITOS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
