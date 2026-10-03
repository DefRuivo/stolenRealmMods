#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A ESCALA x1.7 DO CONTAINER NATIVO ('Skill Item Container') NOS NOS DA ARVORE (RSTV-18).

O QUE ISTO TRAVA
----------------
Achado medido (2 agentes): os nos da aba 'All Trees' saiam PEQUENOS — 46px de tela contra ~78px da
referencia, razao x1.70. A causa: o nativo coloca os nos DENTRO do `Skill Item Container`
(level1, 'Skill Tree Window Roguelike' > GO 490738, RectTransform 1000x800, localScale 1.7); o no e
o `Skill Tree Item Active` 30x30 com localScale 0.9 -> 30 x 0.9 x 1.7 = 45.9u. O mod desenhava
30 x 0.9 x 1.0 = 27u porque reimplementou o layout SEM esse frame.

AS CONTAS (as dos revisores, viram checagem aqui)
-------------------------------------------------
  no efetivo        = 30 (sizeDelta) x 0.9 (localScale) x 1.7 (container) = 45.9u
  pitch horizontal  = 47 x 1.7 = 79.9u   |   pitch vertical = 33 x 1.7 = 56.1u
  (o DEFEITO, escala 1.0, da no 27u e pitch 47u — e o que o dono viu.)

DE ONDE VEM O ESPERADO
----------------------
As regras vivem em `tools/testes/regras_rstv18.py`; o fonte e lido AO VIVO do mod (nunca copia). O
plantio `fonte_com_escala_1` reinjeta o defeito (escala 1.0) no MESMO fonte, em memoria, e as MESMAS
checagens tem de REPROVAR. O que NAO se prova aqui (e so o dono confirma, em tela): os nos e o pitch
desenharem no tamanho da referencia.
"""
import regras_rstv18 as reg

import arcabouco as arc

META = {
    "nome": "rstv18-escala-nos",
    "categoria": "pura",
    "requer": [],
    "descricao": ("RSTV-18: os nos da arvore vivem no container 'RstvNodeContainer' (o 'Skill Item "
                  "Container' nativo) em escala 1.7x -> no de 45.9u e pitch 79.9/56.1u; sem o frame "
                  "(escala 1.0) o no cai para 27u e a checagem REPROVA"),
}


def _perto(obtido, esperado, rotulo, tol=0.05):
    arc.exigir(abs(obtido - esperado) <= tol,
               "%s: esperado ~%.1f, obtido %.3f" % (rotulo, esperado, obtido))


def corpo():
    src = reg.fonte(reg.caminho_aba())
    arc.exigir(len(src) > 1000, "o SkillTreesTab.cs veio vazio/curto: a leitura mudou de lugar?")

    # 1) O FONTE: a escala 1.7, o container com os numeros do prefab e os nos dentro dele.
    falhas = reg.falhas_dos_nos(src)
    arc.exigir(not falhas, "a escala dos nos regrediu em %d ponto(s): %s" % (len(falhas), " | ".join(falhas)))

    # 2) A CONSTANTE lida do fonte e EXATAMENTE a do 'Skill Item Container'.
    escala = reg.escala_do_container(src)
    arc.exigir(escala is not None, "nao consegui ler `EscalaDoContainerDeNos` do fonte")
    _perto(escala, 1.7, "a escala do container")

    # 3) AS CONTAS dos revisores: no ~46u e pitch 79.9/56.1u.
    _perto(reg.no_efetivo(escala), 45.9, "o no efetivo (30 x 0.9 x 1.7)")
    _perto(reg.pitch_horizontal(escala), 79.9, "o pitch horizontal (47 x 1.7)")
    _perto(reg.pitch_vertical(escala), 56.1, "o pitch vertical (33 x 1.7)")

    # 3b) O MODELO DISTINGUE: sem o frame (1.0) o no cai para 27u e o pitch para 47u — nao e o mesmo.
    _perto(reg.no_efetivo(1.0), 27.0, "o no do DEFEITO (30 x 0.9 x 1.0)")
    arc.exigir(abs(reg.no_efetivo(1.0) - reg.no_efetivo(1.7)) > 1.0,
               "o modelo da o mesmo no com e sem o container: nao prova nada")
    arc.exigir(reg.pitch_horizontal(1.0) != reg.pitch_horizontal(1.7),
               "o modelo da o mesmo pitch com e sem o container: nao prova nada")

    # 4) PROVA DE FOGO NO FONTE: com o DEFEITO plantado (escala 1.0), as checagens REPROVAM pelo motivo certo.
    defeito = reg.fonte_com_escala_1(src)
    arc.exigir(defeito != src,
               "o plantio do defeito nao encontrou a ancora (`EscalaDoContainerDeNos = 1.7f`): a "
               "checagem nao le o trecho certo")
    falhas_defeito = reg.falhas_dos_nos(defeito)
    arc.exigir(len(falhas_defeito) >= 1 and any("escala" in f for f in falhas_defeito),
               "as checagens PASSARAM (ou reprovaram por outro motivo) com o container em escala 1.0: %s"
               % " | ".join(falhas_defeito))

    print("RSTV-18: o container dos nos tem a escala 1.7x do 'Skill Item Container' nativo (no "
          "%.1fu, pitch %.1f/%.1fu) e os nos vivem dentro dele; o defeito plantado (escala 1.0 -> "
          "no 27u) REPROVA."
          % (reg.no_efetivo(1.7), reg.pitch_horizontal(1.7), reg.pitch_vertical(1.7)))


if __name__ == "__main__":
    arc.main(META, corpo)
