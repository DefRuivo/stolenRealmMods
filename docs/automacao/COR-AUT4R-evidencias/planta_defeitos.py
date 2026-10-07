#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Planta, uma por vez, o defeito correspondente a cada achado A1-A6 da AUT-4R2 nos
bytes ATUAIS do coletor (copia FORA do repo) e mede o veredito.

Regra da revisao: a isca de contra-prova TEM de reprovar (exit 1) contra o produto
corrigido; com o defeito plantado de volta, ela tem de PASSAR (exit 0) e o runner
inteiro tem de ficar VERMELHO. Is ca que nao muda o veredito nao prova nada.
"""
import os
import shutil
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # .../cor-aut4r
LIMPA = os.path.join(BASE, "trabalho", "base-limpa")
TRAB = os.path.join(BASE, "trabalho")

PLANTAS = {
    "A1": [
        ('''    ev["faltas"] = faltas
    ev["ok"] = not faltas
    return ev''',
         '''    ev["sessao_confere"] = True
    ev["json_mais_novo"] = True
    ev["log_chainloader"] = True
    ev["log_probe"] = True
    ev["prints_ok"] = True
    ev["faltas"] = []
    ev["ok"] = True
    return ev   # PLANTA A1: volta a confirmar so pelo conteudo do JSON'''),
    ],
    "A2": [
        ('''    invalidos = [str(a) for a in lista
                 if not str(a).strip() or str(a) not in CAMPOS_TODOS]''',
         '''    invalidos = []   # PLANTA A2: alvo fora do schema deixa de invalidar o plano'''),
        ('''        if campo in alvos_efetivos and estado in ("AUSENTE", "NAO_APLICAVEL"):
            lacunas.append(campo)''',
         '''        pass   # PLANTA A2: alvo nao lido deixa de virar lacuna'''),
    ],
    "A3": [
        ('    if rotulado_fixture:',
         '    if False and rotulado_fixture:   # PLANTA A3: rotulo do artefato perde para o chamador'),
    ],
    "A4": [
        ('        if status_probe in STATUS_PROBE_FALHA or fase_probe in FASES_PROBE_FALHA:',
         '        if False:   # PLANTA A4: falha terminal do instrumento ignorada'),
        ('        elif status_probe not in STATUS_PROBE_OK:',
         '        elif False:   # PLANTA A4: silencio do instrumento ignorado'),
    ],
    "A5": [
        ('''        acoes = executar_rollback(perfil_dir, plano_rb, backups,
                                  preservar=plano_rb["dirs_pre_existentes"])''',
         '''        acoes = executar_rollback(perfil_dir, plano_rb, backups,
                                  preservar=())   # PLANTA A5: rollback remove dir pre-existente'''),
    ],
    "A6": [
        ('            if exigir_ida_volta:',
         '            if exigir_ida_volta and False:   # PLANTA A6: ida-e-volta deixa de ser exigida'),
    ],
}

ISCAS = {
    "A1": ["cp_aut5_isca_sem_prova_execucao.py"],
    "A2": ["cp_aut5_isca_alvo_nao_lido_ok.py", "cp_aut5_isca_alvo_fora_do_schema.py"],
    "A3": ["cp_aut5_isca_procedencia_do_chamador.py"],
    "A4": ["cp_aut5_isca_status_erro_confirma.py"],
    "A5": ["cp_aut5_isca_dir_pre_existente_removido.py"],
    "A6": ["cp_aut5_isca_sem_prova_ida_volta.py"],
}


def prepara(nome):
    destino = os.path.join(TRAB, "planta-" + nome)
    if os.path.isdir(destino):
        shutil.rmtree(destino)
    shutil.copytree(LIMPA, destino)
    return destino


def planta(raiz, achado):
    alvo = os.path.join(raiz, "tools", "automacao", "runtime", "coletor.py")
    texto = open(alvo, encoding="utf-8").read()
    for velho, novo in PLANTAS[achado]:
        if texto.count(velho) != 1:
            raise SystemExit("PLANTA %s: ancora nao unica (%d) -> %r"
                             % (achado, texto.count(velho), velho[:60]))
        texto = texto.replace(velho, novo)
    open(alvo, "w", encoding="utf-8", newline="\n").write(texto)
    return alvo


def roda(cmd, cwd):
    p = subprocess.run([sys.executable] + cmd, cwd=cwd, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, universal_newlines=True, timeout=900)
    return p.returncode, (p.stdout or "")


def main():
    for achado in ("A1", "A2", "A3", "A4", "A5", "A6"):
        raiz = prepara(achado)
        planta(raiz, achado)
        rt = os.path.join(raiz, "tools", "automacao", "runtime")
        print("=" * 78)
        print("ACHADO %s — defeito plantado em copia: %s" % (achado, raiz))
        for isca in ISCAS[achado]:
            cod, saida = roda([os.path.join("testes", "contra-prova", isca)], rt)
            print("  isca %-46s exit=%d  %s" % (isca, cod,
                  "PASSOU (defeito presente -> prova falsa aceita)" if cod == 0
                  else "reprovou como devia" if cod == 1 else "NAO RODOU"))
            for linha in saida.strip().splitlines()[-1:]:
                print("      | %s" % linha[:200])
        cod_total, saida_total = roda(["roda_testes_runtime.py", "--contra-prova"], rt)
        print("  runner --contra-prova: exit=%d" % cod_total)
        for linha in saida_total.strip().splitlines():
            if "VEREDITO" in linha:
                print("      | %s" % linha)
        cod_suite, _ = roda(["roda_testes_runtime.py"], rt)
        print("  runner suite (deve CONTINUAR verde: o defeito nao quebra o caminho feliz): exit=%d" % cod_suite)


if __name__ == "__main__":
    main()
