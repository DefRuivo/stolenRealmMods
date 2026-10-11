#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova) — F5: ESCRITA sem autorizacao propria.

Afirma o FALSO: que um probe cujo `DemostrarIdaEVolta` chama o handler `ShowTooltip`
SEM a guarda `if (!_autorizaEscrita.Value)` — e um driver que nao escreve a trava no
`.cfg` — passaria pela conferencia do KIT-R0F. Nao passa.

E o defeito que a revisao KIT-R0 apontou: a rodada G1 era SOMENTE LEITURA e mesmo assim
`ShowTooltip` escreveu titulo/corpo no jogo, sem restaurar o titulo.

Roda com `--contra-prova`: o runner EXIGE que este teste REPROVE.
"""
import importlib.util
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(AQUI))
import comum as C  # noqa: E402

CONTRATO = os.path.join(os.path.dirname(AQUI), "t_aut4_r0f_correlacao.py")
PROBE = os.path.join(C.caminho_probe(), "AUT4ProbePlugin.cs")
AGREGADO = os.path.join(C.caminho_probe(), "LeituraAgregados.cs")

META = {
    "nome": "cp-aut4r0f-isca-escrita-sem-autorizacao",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: DemostrarIdaEVolta chama ShowTooltip sem a guarda de escrita e sem "
                 "restauracao — TEM de reprovar",
    "esperado": "reprovar",
}


class ColetorSemTrava(object):
    """O driver ANTES do conserto: nao conhece a chave da trava."""

    CFG_CHAVES = tuple(k for k in C.coletor().CFG_CHAVES if k != "AutorizaEscritaTooltip")

    @staticmethod
    def derivar_config(*args, **kwargs):
        cfg = C.coletor().derivar_config(*args, **kwargs)
        cfg.pop("AutorizaEscritaTooltip", None)   # o .cfg nao declara a trava
        return cfg


def _contrato():
    spec = importlib.util.spec_from_file_location("aut4_r0f_contrato_isca_f5", CONTRATO)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _le(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def corpo():
    contrato = _contrato()
    probe = _le(PROBE)
    agregado = _le(AGREGADO)

    # CONTROLE: as fontes do disco passam.
    C.arc.igual(contrato.conferir(probe, agregado, C.coletor()), [],
                "controle: as fontes do disco tem de passar")

    # DEFEITO plantado: sem a guarda de escrita, sem restauracao conferida, sem a chave.
    probe_velho = probe.replace("if (!_autorizaEscrita.Value)", "if (false)")
    probe_velho = probe_velho.replace("RestaurarTextos", "IgnorarTextos")
    probe_velho = probe_velho.replace('r["restauracao_conferida"]', 'r["nada"]')
    probe_velho = probe_velho.replace(
        'Config.Bind("Geral", "AutorizaEscritaTooltip", false',
        'Config.Bind("Geral", "AutorizaEscritaTooltipX", false')

    problemas = contrato.conferir(probe_velho, agregado, ColetorSemTrava())
    print("defeitos que a conferencia DEVERIA acusar (medidos: %d)" % len(problemas))
    for p in problemas:
        print("  - %s" % p)

    # A AFIRMACAO FALSA (por isso esta isca REPROVA): escrever sem autorizacao propria
    # e sem restaurar o titulo passaria pela conferencia.
    C.arc.igual(problemas, [],
                "AFIRMACAO FALSA — isca TEM de reprovar: o contrato ACEITOU escrita sem "
                "autorizacao propria (observacao autorizando escrita) e sem restauracao")


if __name__ == "__main__":
    C.arc.main(META, corpo)
