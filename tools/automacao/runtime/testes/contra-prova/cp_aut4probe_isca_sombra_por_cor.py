#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova) — FIDELIDADE do criterio de EFEITO do agregado.

Afirma o FALSO: que o criterio ANTIGO da sombra (herdado do CAP-1) — keyword
`UNDERLAY_ON`/`UNDERLAY_INNER` **ou** `_UnderlayColor.a > 0` — passaria pela conferencia
de espelho do BetterFont. Nao passa: o BetterFont (`BetterFont/Plugin.cs`,
`TemEfeitoNoMaterial` -> `SombraDesenhada`, BF-5) decide pelo que faz a sombra
APARECER (keyword ligada ou `_UnderlayOffsetX`/`_UnderlayOffsetY`/`_UnderlayDilate`
diferente de zero) e NAO olha a cor — a cor com alfa, keyword desligada e offset/dilate
zero e a sombra INERTE que o jogo produz e o shader nao desenha.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE. Se ele PASSAR, o
rotulo "espelho do criterio do BetterFont" voltou a ser afirmacao do artefato sobre si
mesmo — o defeito que a revisao 1 da tarefa apontou.
"""
import importlib.util
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import comum as C  # noqa: E402

CONTRATO = os.path.join(os.path.dirname(AQUI), "t_aut4_probe_contrato.py")
AGREGADO = os.path.join(C.caminho_probe(), "LeituraAgregados.cs")
BETTERFONT = os.path.join(C.REPO, "BetterFont", "Plugin.cs")

META = {
    "nome": "cp-aut4probe-isca-sombra-por-cor",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: o criterio antigo da sombra (cor com alfa) passaria pelo espelho do "
                 "BetterFont — TEM de reprovar",
    "esperado": "reprovar",
}


def _contrato():
    spec = importlib.util.spec_from_file_location("aut4_contrato_isca", CONTRATO)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _le(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def corpo():
    contrato = _contrato()
    real = _le(AGREGADO)
    betterfont = _le(BETTERFONT)

    # CONTROLE: o agregado como esta no disco passa (sem isto a isca nao provaria nada
    # sobre o DEFEITO — so sobre a conferencia em geral).
    C.arc.igual(contrato.conferir_espelho_da_sombra(real, betterfont), [],
                "controle: o agregado do disco tem de passar pelo espelho")

    # PLANTIO 1 — o ramo da sombra pelo criterio ANTIGO (cor com alfa).
    antigo = real.replace(
        "if (SombraDesenhada(m)) return true;",
        'if (m.IsKeywordEnabled("UNDERLAY_ON") || m.IsKeywordEnabled("UNDERLAY_INNER")) return true;\n'
        '                if (m.HasProperty("_UnderlayColor") && m.GetColor("_UnderlayColor").a > 0.001f) return true;')
    C.arc.exigir(antigo != real, "o plantio 1 nao alterou o texto — isca vazia")
    d1 = contrato.conferir_espelho_da_sombra(antigo, betterfont)
    C.arc.exigir(any("_UnderlayColor" in d for d in d1),
                 "a conferencia NAO apontou a cor da sombra como defeito: %r" % (d1,))

    # PLANTIO 2 — a sombra sem a GEOMETRIA do mod (so a keyword).
    sem_geometria = real.replace('if (ValorDiferenteDeZero(m, "_UnderlayOffsetX")) return true;\n', "")
    C.arc.exigir(sem_geometria != real, "o plantio 2 nao alterou o texto — isca vazia")
    d2 = contrato.conferir_espelho_da_sombra(sem_geometria, betterfont)
    C.arc.exigir(any("_UnderlayOffsetX" in d for d in d2),
                 "a conferencia NAO apontou a geometria faltando como defeito: %r" % (d2,))

    # A AFIRMACAO FALSA (por isso esta isca REPROVA): o criterio antigo passaria.
    C.arc.exigir(not d1,
                 "ISCA: o criterio ANTIGO da sombra (UNDERLAY_* ou _UnderlayColor.a) passou "
                 "pelo espelho do BetterFont — o rotulo 'espelho' nao esta sendo conferido")


if __name__ == "__main__":
    C.arc.main(META, corpo)
