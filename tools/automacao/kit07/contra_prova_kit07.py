#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KIT-07 - contra-prova DURAVEL: defeitos plantados TEM de reprovar.

Por que existe: o exportador trata privacidade; uma trave que "passa" sem
exercitar o defeito nao prova nada. Aqui cada regra do aceite tem um DEFEITO
PLANTADO numa COPIA do modulo e a suite correspondente TEM de reprovar - com
discriminador ESTRITO:

  * exit 1 (do unittest com falha);
  * `FAIL:` com o conjunto EXATO de testes esperados (nem a mais, nem a menos);
  * presenca de `AssertionError`;
  * AUSENCIA de `ERROR:`, de skip e de execucao vazia.

Duas suites sao exercitadas:
  * `teste_exportador_kit07.py` (autor, 14 testes) - regras centrais;
  * `teste_exportador_kit07f.py` (KIT-07F, 12 testes) - nomes excluidos/PNG
    (F1), colisao, caminhos canonicos (F3), nome reservado (F5), tetos em bytes
    de saida (F7) e erros de I/O da CLI (F8).

Ha um controle adversarial explicito (`controle_falso_verde`): um defeito
plantado que derruba OUTRO teste tem de ser RECUSADO (o conjunto tem de bater).

Uso:
    python tools/automacao/kit07/contra_prova_kit07.py
    python tools/automacao/kit07/contra_prova_kit07.py --individual
    PYTHON=/caminho/python python tools/automacao/kit07/contra_prova_kit07.py

Exit: 0 = verde; 1 = vermelho (algum defeito nao reprovou / oraculo enganado);
2 = erro de infraestrutura (layout/fonte ausente ou padrao de mutacao nao achado).

KIT-07F: as ancoras (`trecho_original`) que apontavam para trechos refatorados
foram atualizadas para o codigo novo - o MESMO defeito continua sendo plantado,
com o MESMO conjunto exato de FAIL declarado em cada caso.

Nunca escreve no modulo original: cada defeito roda numa COPIA temporaria.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))                    # .../kit07
RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(AQUI)))       # raiz do repo
OFFLINE = os.path.join(RAIZ, "tools", "automacao", "offline")
MODULO = os.path.join(AQUI, "exportador.py")
SUITE = os.path.join(AQUI, "teste_exportador_kit07.py")
SUITE_F = os.path.join(AQUI, "teste_exportador_kit07f.py")
LIB = os.path.join(OFFLINE, "aut3_lib.py")

PY = os.environ.get("PYTHON") or sys.executable

# (nome, trecho_original, trecho_defeituoso, {testes que DEVEM reprovar})
DEFEITOS = [
    ("sanitizacao_desligada",
     "    return minimizar_pessoal(_sanitiza_texto(texto), nomes_extras)",
     "    return texto",
     {"test_sanitiza_segredo_ficticio_no_json_e_log", "test_cli_nao_vaza_prefixo",
      "test_minimiza_pessoal"}),
    ("save_nao_excluido",
     '    if ext in EXT_SAVE or any(s in segmentos for s in SEG_SAVE):\n        return "save"',
     '    if False:\n        return "save"',
     {"test_exclui_save_e_assembly"}),
    ("assembly_nao_excluido",
     '    if (RE_BINARIO.match(base) or ext in EXT_BINARIO\n'
     '            or (segmentos & SEG_BINARIO and ext not in EXT_TEXTO)):\n'
     '        return "assembly_proprietario"',
     '    if (False):\n        return "assembly_proprietario"',
     {"test_exclui_save_e_assembly"}),
    ("upload_ligado",
     '        raise ErroExportacao("upload nao e suportado por este exportador")',
     "        pass",
     {"test_sem_upload_na_fonte"}),
    ("png_ligado_por_padrao",
     "def __init__(self, incluir_png=False,",
     "def __init__(self, incluir_png=True,",
     {"test_png_desligado_por_padrao"}),
    ("png_marcado_como_sanitizado",
     '                    "sha256": _sha256_bytes(dados), "sanitizado": False,\n'
     '                    "tipo": "imagem",',
     '                    "sha256": _sha256_bytes(dados), "sanitizado": True,\n'
     '                    "tipo": "imagem",',
     {"test_png_ligado_marca_como_nao_sanitizado"}),
    ("hash_errado",
     '    return hashlib.sha256(dados).hexdigest()',
     '    return hashlib.sha256(b"").hexdigest()',
     {"test_manifest_hash_confere"}),
    ("limite_por_arquivo_ignorado",
     "    return bytes_saida > politica.max_bytes_por_arquivo",
     "    return False",
     {"test_limite_por_arquivo"}),
    ("limite_total_ignorado",
     "    if total_previsto + bytes_novos + politica.overhead_bytes > politica.max_total_bytes:",
     "    if False:",
     {"test_limite_total"}),
    ("exclusao_segura_fraca",
     '    problema = _pacote_reconhecido(pacote)\n'
     '    if problema:\n'
     '        raise ErroExportacao(problema)',
     '    problema = None\n'
     '    if problema:\n'
     '        raise ErroExportacao(problema)',
     {"test_exclusao_segura_recusa_fora_e_apaga_pacote"}),
    ("destino_alheio_sobrescrito",
     '            problema = _pacote_reconhecido(destino_abs)\n'
     '            if problema:\n'
     '                raise ErroExportacao(\n'
     '                    "destino nao vazio e nao e pacote KIT-07 reconhecido: %s" % destino)',
     '            problema = None',
     {"test_nao_sobrescreve_destino_alheio"}),
    ("binario_desconhecido_aceito",
     '                excluidos.append({"caminho": relativo, "motivo": "formato_binario_desconhecido"})',
     "                pass",
     {"test_binario_desconhecido_excluido"}),
]

# Defeitos plantados contra a suite KIT-07F (mesmo modulo).
DEFEITOS_F = [
    ("prefixo_forte_desligado",
     '    for padrao in _PADROES_FORTES:\n        texto = padrao.sub("<REDACTED>", texto)\n    return texto',
     '    return texto',
     {"test_nome_excluido_com_credencial_e_saneado",
      "test_png_nome_com_credencial_saneado",
      "test_colisao_de_nomes_mascarados_distinta"}),
    ("caminhos_canonicos_nao_verificados",
     '    if (origem_real == destino_real\n'
     '            or _eh_subcaminho(destino_real, origem_real)\n'
     '            or _eh_subcaminho(origem_real, destino_real)):\n'
     '        raise ErroExportacao(',
     '    if (False):\n        raise ErroExportacao(',
     {"test_paths_canonicos_iguais_recusa_sem_tocar_origem",
      "test_paths_canonicos_filho_recusado_sem_parcial"}),
    ("nome_reservado_sobrescrito",
     "    if chave in _RESERVADOS_LOWER or chave in usados:",
     "    if chave in usados:",
     {"test_nome_reservado_nao_sobrescreve_input"}),
    ("teto_real_de_saida_nao_conferido",
     '    _confere_teto_total(total, 0, politica, "pacote final")',
     '    pass  # plantado: nao confere o tamanho real do pacote',
     {"test_teto_conta_bytes_reais_de_saida_sem_parcial"}),
    ("destino_arquivo_sem_precheck",
     '        if not os.path.isdir(destino_abs):\n'
     '            raise ErroExportacao("destino existe e nao e um diretorio: %s" % destino)',
     '        if (False):\n'
     '            raise ErroExportacao("destino existe e nao e um diretorio: %s" % destino)',
     {"test_cli_destino_arquivo_exit_dominio_sem_traceback"}),
]

CONJUNTOS = [(SUITE, DEFEITOS, "TesteExportador"), (SUITE_F, DEFEITOS_F, "Adicionais")]

RE_FAIL = re.compile(r"^FAIL:\s+(\w+)\s", re.M)
RE_RAN = re.compile(r"^Ran (\d+) test", re.M)
RE_SKIP = re.compile(r"skipped=\d+")


def _sandbox(nome):
    base = os.path.join(os.environ.get("TMPDIR", "."), "kit07-contraprova")
    destino = os.path.join(base, nome)
    shutil.rmtree(destino, ignore_errors=True)
    os.makedirs(os.path.join(destino, "tools", "automacao", "kit07"))
    os.makedirs(os.path.join(destino, "tools", "automacao", "offline"))
    return destino


def _prepara(defeito, suite):
    """Copia modulo/suite/lib numa sandbox; aplica o defeito no modulo copiado."""
    nome, original, defeituoso, _esperados = defeito
    sandbox = _sandbox(nome)
    with open(MODULO, encoding="utf-8") as fh:
        fonte = fh.read()
    if original not in fonte:
        return None, "padrao de mutacao nao encontrado: %s" % nome
    mutado = fonte.replace(original, defeituoso, 1)
    if mutado == fonte:
        return None, "mutacao nao alterou o fonte: %s" % nome
    with open(os.path.join(sandbox, "tools", "automacao", "kit07", "exportador.py"),
              "w", encoding="utf-8") as fh:
        fh.write(mutado)
    shutil.copyfile(suite, os.path.join(sandbox, "tools", "automacao", "kit07",
                                        os.path.basename(suite)))
    shutil.copyfile(LIB, os.path.join(sandbox, "tools", "automacao", "offline",
                                      "aut3_lib.py"))
    return sandbox, None


def _roda(sandbox, suite, classe, individual=False, alvos=None):
    caminho = os.path.join(sandbox, "tools", "automacao", "kit07", os.path.basename(suite))
    modulo_teste = os.path.splitext(os.path.basename(suite))[0]
    if individual and alvos:
        resultados = []
        for alvo in sorted(alvos):
            env = dict(os.environ)
            env["KIT07_ALVO"] = alvo
            runner = os.path.join(sandbox, "roda_alvo.py")
            with open(runner, "w", encoding="utf-8") as fh:
                fh.write(
                    "import sys,os,unittest\n"
                    "sys.path.insert(0, os.path.dirname(%r))\n"
                    "import %s as t\n"
                    "s=unittest.TestLoader().loadTestsFromName(\n"
                    "    %r + os.environ['KIT07_ALVO'], t)\n"
                    "r=unittest.TextTestRunner(verbosity=2).run(s)\n"
                    "sys.exit(0 if r.wasSuccessful() else 1)\n"
                    % (caminho, modulo_teste, classe + "."))
            proc = subprocess.run([PY, runner], cwd=sandbox, env=env,
                                  stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  universal_newlines=True, encoding="utf-8", errors="replace",
                                  timeout=300)
            resultados.append((alvo, proc.returncode, proc.stdout))
        return resultados
    proc = subprocess.run([PY, caminho], cwd=sandbox, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, universal_newlines=True,
                          encoding="utf-8", errors="replace", timeout=300)
    return (proc.returncode, proc.stdout)


def _discrimina(rc, saida, esperados):
    """Discriminador ESTRITO: so aprova o conjunto EXATO, sem ERROR/skip."""
    if rc != 1:
        return False, "exit=%s (esperado 1)" % rc
    if "ERROR:" in saida:
        return False, "contem ERROR:"
    if RE_SKIP.search(saida):
        return False, "contem skip"
    m = RE_RAN.search(saida)
    if not m or int(m.group(1)) == 0:
        return False, "sem 'Ran N tests' ou N==0"
    if "AssertionError" not in saida:
        return False, "sem AssertionError"
    falhos = set(RE_FAIL.findall(saida))
    if falhos != set(esperados):
        return False, "conjunto de FAIL diferente: %s != %s" % (sorted(falhos), sorted(esperados))
    return True, "ok (%d falha(s): %s)" % (len(falhos), ",".join(sorted(falhos)))


def controle_falso_verde():
    """Um defeito que derruba OUTRO teste tem de ser RECUSADO pelo discriminador."""
    defeito = next(d for d in DEFEITOS if d[0] == "limite_por_arquivo_ignorado")
    sandbox, erro = _prepara(defeito, SUITE)
    if erro:
        return False, erro
    rc, saida = _roda(sandbox, SUITE, "TesteExportador")
    # a mutacao derruba test_limite_por_arquivo; declaramos um alvo DIFERENTE.
    ok, detalhe = _discrimina(rc, saida, {"test_minimiza_pessoal"})
    return (not ok), detalhe


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--individual", action="store_true")
    args = ap.parse_args(argv)

    for caminho in (MODULO, SUITE, SUITE_F, LIB):
        if not os.path.isfile(caminho):
            sys.stderr.write("ERRO KIT-07: infra ausente: %s\n" % caminho)
            return 2

    falhas = []
    total_defeitos = 0
    for suite, defeitos, classe in CONJUNTOS:
        print("== suite %s ==" % os.path.basename(suite))
        for defeito in defeitos:
            nome, _o, _d, esperados = defeito
            total_defeitos += 1
            sandbox, erro = _prepara(defeito, suite)
            if erro:
                print("INFRA|%s|%s" % (nome, erro))
                return 2
            if args.individual:
                for alvo, rc, saida in _roda(sandbox, suite, classe, individual=True, alvos=esperados):
                    ok = (rc == 1 and "AssertionError" in saida and "ERROR:" not in saida)
                    print("DEFEITO|%s|%s|%s" % (nome, alvo, "RECUSOU" if ok else "ACERTOU-INDEVIDO"))
                    if not ok:
                        falhas.append("%s/%s (rc=%s)" % (nome, alvo, rc))
            else:
                rc, saida = _roda(sandbox, suite, classe)
                ok, detalhe = _discrimina(rc, saida, esperados)
                print("DEFEITO|%s|%s|%s" % (nome, "RECUSOU" if ok else "FALHOU", detalhe))
                if not ok:
                    falhas.append("%s: %s" % (nome, detalhe))

    recusou, detalhe = controle_falso_verde()
    print("CONTROLE_falso_verde|%s|%s" % ("RECUSOU" if recusou else "ACEITOU", detalhe))
    if not recusou:
        falhas.append("controle falso-verde aceito: %s" % detalhe)

    if falhas:
        print("VEREDITO KIT-07 contra-prova: VERMELHO (%d problema(s))" % len(falhas))
        for f in falhas:
            print("  - " + f)
        return 1
    print("VEREDITO KIT-07 contra-prova: VERDE (%d defeitos reprovados como deviam)"
          % total_defeitos)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
