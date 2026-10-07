#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""planta_defeitos_aut4f.py — CONTRA-PROVA dos consertos do AUT-4F.

Para CADA achado da frente AUT-4F (AUT-4R2 A1-A7 + CIC-5R R-1..R-5/S-2/S-3), este
script:

  1. copia a arvore minima do repositorio (`tools/` + `docs/`) para uma pasta SCRATCH
     FORA do repo (o repo nunca e tocado);
  2. PLANTA o defeito daquele achado (a substituicao exata que reintroduz o
     comportamento reprovado);
  3. roda a suite offline e a contra-prova e registra os EXIT CODES reais.

Sem o defeito (copia de controle) a suite tem de sair VERDE (exit 0); com o defeito
plantado tem de sair VERMELHO (exit 1). Achado cujo defeito NAO muda o veredito nao
esta travado por teste nenhum — e o script acusa isso no resumo.

Uso:
    python docs/automacao/AUT-4F-evidencias/planta_defeitos_aut4f.py [--repo C:/dev/stolen-realm]
                                                                    [--saida resultados.json]

Nao instala nada, nao abre o jogo, nao toca no perfil do dono: so copia, edita a
copia e roda Python offline.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

# (id, titulo, arquivo relativo, trecho ORIGINAL, trecho com o DEFEITO PLANTADO)
DEFEITOS = [
    ("A1", "driver confirma sem prova de execucao (provas sempre 'ok')",
     "tools/automacao/runtime/coletor.py",
     '    ev["ok"] = not faltas',
     '    ev["ok"] = True  # DEFEITO PLANTADO A1'),
    ("A2", "alvo NAO_APLICAVEL (objeto inativo) nao vira lacuna",
     "tools/automacao/runtime/coletor.py",
     '        if campo in alvos_efetivos and estado in ("AUSENTE", "NAO_APLICAVEL"):',
     '        if campo in alvos_efetivos and estado == "AUSENTE":  # DEFEITO PLANTADO A2'),
    ("A3", "rotulo de fixture do artefato perde para a intencao do chamador",
     "tools/automacao/runtime/coletor.py",
     "    if rotulado_fixture:",
     "    if False:  # DEFEITO PLANTADO A3"),
    ("A4", "status/fase terminal de falha do probe nao rebaixa o veredito",
     "tools/automacao/runtime/coletor.py",
     'STATUS_PROBE_FALHA = ("NAO_EXERCITADO", "SEM_UI", "ERRO", "ORCAMENTO_ESTOURADO")\n'
     'FASES_PROBE_FALHA = ("nao-exercitado", "sem-ui", "sem_ui", "erro",\n'
     '                     "orcamento-estourado", "orcamento_estourado")',
     'STATUS_PROBE_FALHA = ()  # DEFEITO PLANTADO A4\n'
     'FASES_PROBE_FALHA = ()\n'
     'STATUS_PROBE_OK = STATUS_PROBE_OK + ("NAO_EXERCITADO", "SEM_UI", "ERRO",\n'
     '                                     "ORCAMENTO_ESTOURADO")'),
    ("A5", "rollback remove diretorio pre-existente",
     "tools/automacao/runtime/coletor.py",
     '    preservar = preservar if preservar is not None else plano_rb.get("dirs_pre_existentes") or []',
     "    preservar = []  # DEFEITO PLANTADO A5"),
    ("A6", "a prova de ida-e-volta aceita 'conferiu' sem o marcador do driver",
     "tools/automacao/runtime/coletor.py",
     '                conferiu = (bool(ida_volta.get("conferiu"))\n'
     '                            and str(ida_volta.get("marcador") or "") == str(marcador_ida_volta))',
     '                conferiu = bool(ida_volta.get("conferiu"))  # DEFEITO PLANTADO A6'),
    ("S-3", "campo EXTRA declarado alvo nunca vira lacuna",
     "tools/automacao/runtime/coletor.py",
     '        if campo in alvos_efetivos and estado in ("AUSENTE", "NAO_APLICAVEL"):',
     '        if campo in CAMPOS and campo in alvos_efetivos and estado in ("AUSENTE", "NAO_APLICAVEL"):  # DEFEITO PLANTADO S-3'),
    ("R-1", "adaptador confronta hash_fonte (sha da DLL) com fonte_sha",
     "tools/automacao/cenarios/rstv.py",
     '_ALIAS_HASH = (("hash_fonte", "dll_sha"), ("hash_dll", "dll_sha"))',
     '_ALIAS_HASH = (("hash_fonte", "fonte_sha"), ("hash_dll", "dll_sha"))  # DEFEITO PLANTADO R-1'),
    ("R-2", "abspath antes do gate: --executar sem --perfil estoura",
     "tools/automacao/runtime/coletor.py",
     '    sem_destino = [nome for nome, valor in (("perfil_dir", perfil_dir), ("out_dir", out_dir))',
     '    perfil_dir = os.path.abspath(perfil_dir)  # DEFEITO PLANTADO R-2\n'
     '    out_dir = os.path.abspath(out_dir)\n'
     '    sem_destino = [nome for nome, valor in (("perfil_dir", perfil_dir), ("out_dir", out_dir))'),
    ("R-3", "a espera para so pela 'fase' e queima o teto num status=ERRO",
     "tools/automacao/runtime/coletor.py",
     '                if (str(fase or "").strip().lower() in FASES_TERMINAIS\n'
     '                        or status in STATUS_TERMINAIS_ESPERA):',
     '                if str(fase or "").strip().lower() in FASES_TERMINAIS:  # DEFEITO PLANTADO R-3'),
    ("R-4", "encerramento derruba TODAS as instancias da imagem",
     "tools/automacao/runtime/coletor.py",
     "    novos = sorted(pids_depois - pids_antes)",
     "    novos = sorted(pids_depois)  # DEFEITO PLANTADO R-4"),
    ("R-5", "runner de contra-prova aceita crash (excecao) como prova",
     "tools/automacao/runtime/roda_testes_runtime.py",
     '    if "excecao inesperada" in texto:',
     "    if False:  # DEFEITO PLANTADO R-5"),
    ("S-2", "_alvos_do_plano ignora os cenarios 2+",
     "tools/automacao/runtime/coletor.py",
     '    cenarios = plano.get("cenarios")\n'
     '    if isinstance(cenarios, list):\n'
     '        for cenario in cenarios:\n'
     '            if isinstance(cenario, dict) and cenario.get("campos_alvo"):\n'
     '                _acrescentar(cenario.get("campos_alvo"))',
     '    cenarios = plano.get("cenarios")  # DEFEITO PLANTADO S-2\n'
     '    if isinstance(cenarios, list) and cenarios and isinstance(cenarios[0], dict):\n'
     '        if cenarios[0].get("campos_alvo"):\n'
     '            _acrescentar(cenarios[0].get("campos_alvo"))'),
]

IGNORAR = shutil.ignore_patterns("__pycache__", "*.pyc", "obj", ".git")


def copiar(origem, destino):
    os.makedirs(destino, exist_ok=True)
    for pasta in ("tools", "docs"):
        shutil.copytree(os.path.join(origem, pasta), os.path.join(destino, pasta),
                        ignore=IGNORAR, dirs_exist_ok=True)
    return destino


def aplicar(raiz, relativo, antigo, novo):
    caminho = os.path.join(raiz, relativo.replace("/", os.sep))
    with open(caminho, encoding="utf-8") as fh:
        texto = fh.read()
    ocorrencias = texto.count(antigo)
    if ocorrencias != 1:
        raise SystemExit("PLANTA: o trecho de %s aparece %d vez(es) (esperado 1) — "
                         "o codigo mudou e o plantio precisa ser reconferido" % (relativo, ocorrencias))
    with open(caminho, "w", encoding="utf-8") as fh:
        fh.write(texto.replace(antigo, novo))


def rodar(raiz, contra=False):
    cmd = [sys.executable, os.path.join("tools", "automacao", "runtime", "roda_testes_runtime.py")]
    if contra:
        cmd.append("--contra-prova")
    proc = subprocess.run(cmd, cwd=raiz, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          universal_newlines=True, timeout=1800)
    saida = proc.stdout or ""
    reprovados = [linha.split("] ")[-1] for linha in saida.splitlines()
                  if linha.startswith("[REPROVOU")]
    return proc.returncode, reprovados, saida


def main():
    ap = argparse.ArgumentParser(description="Contra-prova (defeito plantado) dos consertos do AUT-4F.")
    ap.add_argument("--repo", default=os.environ.get("AUT4F_REPO", r"C:/dev/stolen-realm"))
    ap.add_argument("--scratch", default=os.environ.get("AUT4F_SCRATCH")
                    or os.path.join(tempfile.gettempdir(), "aut4f-planta"))
    ap.add_argument("--saida", default=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                    "planta-defeitos-resultados.json"))
    args = ap.parse_args()

    if os.path.isdir(args.scratch):
        shutil.rmtree(args.scratch)
    os.makedirs(args.scratch, exist_ok=True)

    print("=" * 78)
    print(" CONTRA-PROVA AUT-4F — defeito plantado -> REPROVADO; sem defeito -> OK")
    print(" repo    : %s" % args.repo)
    print(" scratch : %s  (FORA do repo)" % args.scratch)
    print("=" * 78)

    # ---- controle: copia SEM defeito ----
    base = copiar(args.repo, os.path.join(args.scratch, "CONTROLE"))
    exit_suite, reprovados, _ = rodar(base)
    exit_cp, reprovados_cp, _ = rodar(base, contra=True)
    print("[CONTROLE      ] suite exit=%d (%s)  contra-prova exit=%d (%s)"
          % (exit_suite, "sem defeito", exit_cp, "sem defeito"))

    resultados = []
    for identificador, titulo, relativo, antigo, novo in DEFEITOS:
        destino = copiar(args.repo, os.path.join(args.scratch, identificador))
        aplicar(destino, relativo, antigo, novo)
        exit_suite, reprovados, _ = rodar(destino)
        exit_cp, _, _ = rodar(destino, contra=True)
        travado = (exit_suite != 0)
        resultados.append({"id": identificador, "titulo": titulo, "arquivo": relativo,
                           "exit_suite_com_defeito": exit_suite,
                           "exit_contra_prova_com_defeito": exit_cp,
                           "testes_que_reprovaram": reprovados,
                           "travado_por_teste": travado})
        print("[%-14s] suite exit=%d %s | contra-prova exit=%d | reprovaram: %s"
              % (identificador, exit_suite, "REPROVADO" if travado else "*** NAO TRAVADO ***",
                 exit_cp, ", ".join(os.path.basename(t) for t in reprovados) or "-"))

    dados = {
        "esquema": "AUT-4F/1",
        "repo_original": os.path.abspath(args.repo),
        "scratch": os.path.abspath(args.scratch),
        "controle_sem_defeito": {"exit_suite": exit_suite, "contra_prova_exit": exit_cp},
        "defeitos": resultados,
    }
    with open(args.saida, "w", encoding="utf-8") as fh:
        json.dump(dados, fh, ensure_ascii=False, indent=2)

    nao_travados = [r["id"] for r in resultados if not r["travado_por_teste"]]
    print("=" * 78)
    print(" resumo: %d defeitos plantados; travados por teste: %d/%d"
          % (len(resultados), len(resultados) - len(nao_travados), len(resultados)))
    if nao_travados:
        print(" ATENCAO — achado sem teste que o pegue: %s" % ", ".join(nao_travados))
    print(" resultados: %s" % args.saida)
    return 1 if nao_travados else 0


if __name__ == "__main__":
    sys.exit(main())
