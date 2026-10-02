#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""formato9-prova-janela.py - a bancada do FORMATO-9 (mede no install real, nos DOIS sentidos).

Roda fora da suite (nome fora do padrao `t_*`/`cp_*`: o runner o CONTA como ignorado). E a bancada
reproduzivel que produz `formato9-prova-janela.log`. O que ela mede:

  1. ANTES (a versao do `git HEAD`) x DEPOIS (a copia de trabalho) nas 3 janelas: as bases e as
     citacoes sao as MESMAS (o conserto nao mexeu em nenhum numero) e o `--check` segue verde.
  2. O CASO QUE PASSAVA EM SILENCIO (FORMATO-7): a janela do Decay deslocada 1 byte a frente da
     formula. Antes devolvia a base do Dwarven (20 Target @1517115364) SEM ERRO; depois FALHA ALTO
     nomeando o range e as quantidades.
  3. O TESTE DA SUITE NO VERMELHO DE VERDADE: com a REGRA ANTIGA reinjetada na copia de trabalho
     (so a funcao; as constantes novas ficam), `t_formato9_janela_aura.py` sai REPROVOU; restaurado
     o arquivo (sha256 conferido), sai PASSOU. Nao e decoracao.

    python tools/testes/formato9-prova-janela.py | tee tools/testes/formato9-prova-janela.log
"""
import hashlib
import importlib.util
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(AQUI))   # tools/testes -> tools -> raiz
GERADOR = os.path.join(RAIZ, "tools", "gera_shrines_esperado.py")
TESTE = os.path.join(RAIZ, "tools", "testes", "testes", "puros", "t_formato9_janela_aura.py")

PROBE_DECAY = (1517114277, 1517116000)   # FORMATO-7: janela do Decay 1 byte a frente da formula

# A regra ANTIGA (transcrita do `git HEAD`): devolve a PRIMEIRA formula que casa, sem checar eixo
# nem unicidade. E o defeito latente que a FORMATO-9 fecha.
OLD_FUNCAO = '''def bases_do_asset(asset, aura, eixo_esperado, janela):
    """REGRA ANTIGA (reinjetada pela bancada): a PRIMEIRA formula que casa vence, em silencio."""
    if not asset:
        raise SystemExit("FALHA: sem asset")
    ini, fim = janela
    bruto = ler_janela(asset, ini, fim)
    pos = bruto.find(b"Mathf.Round(")
    while pos >= 0:
        txt = bruto[pos:pos + 120].split(b"\\x00", 1)[0].decode("latin-1", errors="replace")
        m = RE_FORMULA_STATUS.search(txt)
        if m:
            return float(m.group(1)), m.group(2), "resources.assets@%d" % (ini + pos)
        pos = bruto.find(b"Mathf.Round(", pos + 1)
    raise SystemExit("FALHA: nenhuma formula na janela")'''


def sha256(caminho):
    with open(caminho, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def carrega(caminho, nome):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def roda(cmd):
    p = subprocess.run(cmd, cwd=RAIZ, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       universal_newlines=True)
    return p.returncode, (p.stdout or "").strip()


def main():
    atual = carrega(GERADOR, "gse_atual")
    asset = atual.procura_asset()
    if not asset:
        print("NAO_CONSEGUI_Rodar: nenhum resources.assets do install encontrado.")
        return 2
    print("asset: %s\n" % asset)

    # ---- 1. ANTES (git HEAD) x DEPOIS, nas 3 janelas --------------------------------
    src_head = os.path.join(tempfile.mkdtemp(prefix="f9head-"), "gera_shrines_esperado.py")
    codigo, saida = roda(["git", "show", "HEAD:tools/gera_shrines_esperado.py"])
    if codigo != 0:
        print("NAO_CONSEGUI_Rodar: `git show HEAD:...` falhou:\n%s" % saida)
        return 2
    with open(src_head, "w", encoding="utf-8", newline="") as fh:
        fh.write(saida + "\n")
    head = carrega(src_head, "gse_head")

    print("=== 1. AS 3 JANELAS: ANTES (HEAD) x DEPOIS ===")
    mesmas = True
    for aura, tipo, eixo, janela, nota in atual.AURAS_ASSET:
        b_now, e_now, f_now = atual.bases_do_asset(asset, aura, eixo, janela)
        h = next(x for x in head.AURAS_ASSET if x[0] == aura)
        b_old, e_old, f_old = head.bases_do_asset(asset, h[0], h[2])
        igual = (b_now, e_now, f_now) == (b_old, e_old, f_old)
        mesmas = mesmas and igual
        print("  %-20s janela=%-26s agora=%-34s antes=%-34s %s"
              % (aura, "%d..%d" % janela, "%g %s @%s" % (b_now, e_now, f_now.split("@")[-1]),
                 "%g %s @%s" % (b_old, e_old, f_old.split("@")[-1]), "IGUAL" if igual else "MUDOU"))
    if not mesmas:
        print("  -> MUDOU numero/olfato! o conserto NAO podia mexer na leitura das 3 janelas.")
        return 1

    codigo, saida = roda([sys.executable, GERADOR, "--check"])
    print("  --check: exit %d | %s" % (codigo, saida))
    if codigo != 0:
        print("  -> o --check NAO esta verde.")
        return 1

    # ---- 2. O CASO QUE PASSAVA EM SILENCIO ------------------------------------------
    print("\n=== 2. O CASO SILENCIOSO DA FORMATO-7 (janela do Decay deslocada) ===")
    print("  janela: %d..%d  (1 byte a frente da formula do Decay @1517114276)" % PROBE_DECAY)
    b_old, e_old, f_old = head.bases_do_asset(asset, "Decay Shrine Aura", PROBE_DECAY)
    print("  ANTES: PASSOU EM SILENCIO -> base=%g eixo=%s %s" % (b_old, e_old, f_old))
    try:
        b_now, e_now, f_now = atual.bases_do_asset(asset, "Decay Shrine Aura", "Source", PROBE_DECAY)
        print("  DEPOIS: NAO FALHOU (defeito!) -> base=%g eixo=%s" % (b_now, e_now))
        return 1
    except SystemExit as erro:
        print("  DEPOIS: SystemExit -> %s" % str(erro).replace("\n", " "))
    if not (b_old == 20.0 and e_old == "Target"):
        print("  -> a regra antiga nao reproduziu o silencio esperado; a prova perdeu o sentido.")
        return 1

    # ---- 3. O TESTE DA SUITE NO VERMELHO (regra antiga reinjetada) -------------------
    print("\n=== 3. O TESTE DA SUITE, MOSTRADO REPROVANDO ===")
    codigo, saida = roda([sys.executable, TESTE])
    print("  teste como esta: exit %d | %s" % (codigo, saida.splitlines()[-1]))
    if codigo != 0:
        return 1

    antes_sha = sha256(GERADOR)
    antes_bytes = open(GERADOR, "rb").read()
    texto = antes_bytes.decode("utf-8")
    ini = texto.index("def bases_do_asset(")
    fim = texto.index("def percentuais_das_acoes(")
    reinjetado = texto[:ini] + OLD_FUNCAO + "\n\n" + texto[fim:]
    try:
        with open(GERADOR, "wb") as fh:
            fh.write(reinjetado.encode("utf-8"))
        codigo, saida = roda([sys.executable, TESTE])
        print("  teste com a REGRA ANTIGA reinjetada: exit %d | %s"
              % (codigo, saida.splitlines()[-1] if saida else ""))
        if codigo == 0:
            print("  -> o teste NAO reprovou com o defeito reinjetado: a trava nao vale nada.")
            return 1
    finally:
        with open(GERADOR, "wb") as fh:
            fh.write(antes_bytes)
    depois_sha = sha256(GERADOR)
    print("  restaurado: sha256 %sdentro (%s -> %s)"
          % ("IDENTICO " if antes_sha == depois_sha else "DIFERENTE! ",
             antes_sha[:12], depois_sha[:12]))
    if antes_sha != depois_sha:
        return 1
    codigo, saida = roda([sys.executable, TESTE])
    print("  teste restaurado: exit %d | %s" % (codigo, saida.splitlines()[-1]))
    if codigo != 0:
        return 1

    print("\nFORMATO-9: as 3 janelas dao os MESMOS numeros e citacoes (--check verde); a janela "
          "deslocada que devolvia o Dwarven em silencio agora FALHA ALTO; o teste da suite reprova "
          "com a regra antiga e volta a passar restaurado byte a byte.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
