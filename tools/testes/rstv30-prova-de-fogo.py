#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rstv30-prova-de-fogo.py - RSTV-30: a prova de fogo FISICA do conserto.

PLANTA cada defeito no FONTE REAL do mod, roda o teste da suite pelo runner de verdade, exige
REPROVOU (exit 1) PELO MOTIVO CERTO e RESTAURA o arquivo byte a byte (sha256 conferido). O
resultado consolidado vai para `tools/testes/rstv30-prova-reprovando.log`.

Uso:  python tools/testes/rstv30-prova-de-fogo.py
Exit: 0 = todos os defeitos foram pegos e os arquivos voltaram intactos · 1 = alguma isca passou
      (o teste nao pega o defeito) ou a restauracao divergiu.

Este script NAO e' um teste da suite (nome sem `t_`/`cp_`): o runner o conta como "ignorado".
"""
import hashlib
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(AQUI, "..", ".."))
MOD = os.path.join(REPO, "RoguelikeSkillTreeVisualizer")
RUNNER = os.path.join(AQUI, "roda_testes.py")
LOG = os.path.join(AQUI, "rstv30-prova-reprovando.log")

TESTE_BARRA = os.path.join(AQUI, "testes", "puros", "t_rstv30_barra_de_baixo.py")
TESTE_PISCAR = os.path.join(AQUI, "testes", "puros", "t_rstv30_sem_piscar.py")
TESTE_MAPA = os.path.join(AQUI, "testes", "puros", "t_rstv13_gate_mapa.py")


def sha(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def le(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def escreve(caminho, texto):
    with open(caminho, "w", encoding="utf-8", newline="") as fh:
        fh.write(texto)


def roda_teste(caminho_teste):
    """Roda UM teste pelo runner de verdade e devolve (exit, saida)."""
    saida = subprocess.run([sys.executable, RUNNER, "--teste", caminho_teste],
                           cwd=REPO, capture_output=True, text=True, timeout=600)
    return saida.returncode, (saida.stdout or "") + (saida.stderr or "")


def recorta(saida, linhas=6):
    interessantes = [l for l in saida.splitlines()
                     if "REPROVOU" in l or "PASSOU" in l or "VEREDITO" in l]
    return "\n".join(interessantes[-linhas:]) or saida.strip()[-400:]


# ---------------------------------------------------------------- as iscas ---

def isca_visibilidade_presa_ao_portao():
    """RSTV-30/1: o `Mirror` volta a esconder quando o portao recusa (o piscar do dono)."""
    return ("RunButton.cs",
            """                EspelharVisibilidade();
                AplicarClique();""",
            """                string porqueNao;
                if (!RunTargets.GateOk(out porqueNao))
                {
                    Hide(porqueNao, true);
                    return;
                }

                EspelharVisibilidade();
                AplicarClique();""",
            TESTE_BARRA,
            "Mirror chama `RunTargets.GateOk`")


def isca_guarda_do_piscar():
    """RSTV-30/2: a guarda `AnyActingCharactersInBattle` volta ao portao."""
    ancora = """                    if (root.SpawnPlacementActive)
                    {
                        motivo = "posicionamento inicial em andamento (Root.SpawnPlacementActive)";
                        return false;
                    }"""
    return ("RunTargets.cs", ancora, ancora + """

                    if (root.AnyActingCharactersInBattle)
                    {
                        motivo = "algum personagem esta executando acao (Root.AnyActingCharactersInBattle)";
                        return false;
                    }""",
            TESTE_MAPA,
            "AnyActingCharactersInBattle")


def isca_posicao_digitada():
    """RSTV-30/3: a posicao deixa de ser derivada e vira literal (posicao chutada)."""
    return ("RunButton.cs",
            """            float centro = limite - Margem - (largura * 0.5f);""",
            """            float centro = 125.59f;""",
            TESTE_BARRA,
            "literal de posicao")


def isca_justificativa_apagada():
    """RSTV-30/4: a GUARDA 3 fica sem a linha `Justificativa:` (guarda sem justificativa)."""
    return ("RunTargets.cs",
            """                // GUARDA 3 (dano real, universal) — modo de apontar o hex.
                // Justificativa: abrir a arvore ESCREVE `GameLogic.CurrentlySelectedCharacter`
                // (`SkillTreeReadOnly`: define o alvo quando o jogo nao tem nenhum selecionado) e
                // escrever esse campo durante a mira forca `CurrentState = Movement` (l.110065),
                // CANCELANDO o apontar o hex que o jogador tinha comecado.
                if (gui.PingModeActive)""",
            """                // GUARDA 3 (dano real, universal) — modo de apontar o hex.
                if (gui.PingModeActive)""",
            TESTE_BARRA,
            "Justificativa")


def isca_ignore_layout_fora():
    """RSTV-30/5: o clone deixa de ter `ignoreLayout` — o LayoutGroup voltaria a refluir a linha."""
    return ("RunButton.cs",
            """            elemento.ignoreLayout = true;""",
            """            elemento.ignoreLayout = false;""",
            TESTE_BARRA,
            "ignoreLayout")


def isca_referencial_misturado():
    """RSTV-30F/6: o limite da direita volta a ser medido no espaco do PAI (referenciais misturados).

    E' o defeito EXATO do achado da RSTV-30R: `fimDosNativos` no espaco local (origem no pivor) x
    `limite` contado a partir da borda esquerda do container — o vao sai ~55.7 px maior e o clone cai
    DEPOIS do rotador da barra de skills.
    """
    return ("RunButton.cs",
            """                    rt.GetWorldCorners(cantos);
                    float esquerdaDoIrmao = container.InverseTransformPoint(cantos[0]).x;""",
            """                    rt.GetWorldCorners(cantos);
                    float esquerdaDoIrmao = pai.InverseTransformPoint(cantos[0]).x;""",
            TESTE_BARRA,
            "misturar referenciais")


ISCAS = (
    ("1. visibilidade presa ao portao (o PISCAR relatado)", isca_visibilidade_presa_ao_portao),
    ("2. guarda `AnyActingCharactersInBattle` de volta", isca_guarda_do_piscar),
    ("3. posicao digitada (literal) em vez de medida", isca_posicao_digitada),
    ("4. guarda sem justificativa (GUARDA 3)", isca_justificativa_apagada),
    ("5. `ignoreLayout` desligado (empurraria os nativos)", isca_ignore_layout_fora),
    ("6. limite medido no espaco do PAI (referenciais misturados)", isca_referencial_misturado),
)


def main():
    linhas = []
    falhou = False

    linhas.append("RSTV-30 - PROVA DE FOGO FISICA (tools/testes/rstv30-prova-de-fogo.py)")
    linhas.append("repo: %s" % REPO)
    linhas.append("runner: python tools/testes/roda_testes.py --teste <teste>")
    linhas.append("")

    # Linha de base: os testes alvo PASSAM antes de qualquer plantio.
    for nome, teste in (("rstv30-barra-de-baixo", TESTE_BARRA), ("rstv30-sem-piscar", TESTE_PISCAR),
                        ("rstv13-gate-mapa", TESTE_MAPA)):
        rc, saida = roda_teste(teste)
        linhas.append("[BASE] %-22s exit=%d %s" % (nome, rc, "PASSOU" if rc == 0 else "REPROVOU"))
        if rc != 0:
            falhou = True
            linhas.append(recorta(saida))
    linhas.append("")

    for rotulo, isca in ISCAS:
        arquivo, de, para, teste, marca = isca()
        caminho = os.path.join(MOD, arquivo)
        antes = le(caminho)
        sha_antes = sha(caminho)

        if de not in antes:
            linhas.append("[ISCA %s] ANCORA NAO ENCONTRADA em %s — a isca esta lendo outro trecho"
                          % (rotulo, arquivo))
            falhou = True
            continue

        escreve(caminho, antes.replace(de, para, 1))
        sha_planta = sha(caminho)
        try:
            rc, saida = roda_teste(teste)
        finally:
            escreve(caminho, antes)
            sha_depois = sha(caminho)

        linha = "[ISCA %s]" % rotulo
        linhas.append(linha)
        linhas.append("  arquivo         : %s" % arquivo)
        linhas.append("  sha256 antes    : %s" % sha_antes)
        linhas.append("  sha256 plantado : %s" % sha_planta)
        linhas.append("  sha256 restaurado: %s  (%s)" % (
            sha_depois, "IDENTICO ao de antes" if sha_depois == sha_antes else "DIVERGIU!"))
        linhas.append("  teste           : %s" % os.path.basename(teste))
        linhas.append("  exit do runner  : %d (%s)" % (rc, "REPROVOU" if rc == 1 else
                                                       ("PASSOU" if rc == 0 else "outro")))
        linhas.append("  saida           : %s" % recorta(saida).replace("\n", "\n                    "))

        if not (rc == 1 and marca in saida):
            falhou = True
            linhas.append("  RESULTADO       : FALHOU — o defeito NAO foi pego pelo motivo certo "
                          "(esperado exit=1 com %r)" % marca)
        else:
            linhas.append("  RESULTADO       : OK — o defeito foi pego e o arquivo voltou intacto")

        if sha_depois != sha_antes:
            falhou = True
        linhas.append("")

    linhas.append("VEREDITO: %s" % ("FALHOU (algum defeito passou ou arquivo nao voltou intacto)"
                                    if falhou else
                                    "OK — os %d defeitos reprovam PELO MOTIVO CERTO e os arquivos "
                                    "voltaram byte a byte (sha256)" % len(ISCAS)))

    texto = "\n".join(linhas) + "\n"
    escreve(LOG, texto)
    print(texto)
    return 1 if falhou else 0


if __name__ == "__main__":
    sys.exit(main())
