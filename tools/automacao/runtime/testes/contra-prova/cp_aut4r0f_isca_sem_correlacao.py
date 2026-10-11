#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ISCA (contra-prova) — F3: JSON sem CORRELACAO evento/quadro/PNG.

Afirma o FALSO: que um probe que NAO registra quadro de leitura nem pedido/conclusao do
PNG — e que mantem a lista de textos apresentada como "JA DESENHADOS" — passaria pela
conferencia do KIT-R0F. Nao passa.

E o defeito que a revisao KIT-R0 apontou: `aplicacao.roteiro_frame=0` (metadado do
arranque) e `quadros_ate_a_ui` (ticks internos) ao lado de uma lista chamada
`textos_visiveis` deixavam a evidencia parecendo correlacionada sem ser.

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
    "nome": "cp-aut4r0f-isca-sem-correlacao",
    "categoria": "pura",
    "requer": [],
    "descricao": "ISCA: probe sem eventos_frame/prints_detalhe e lista rotulada como 'JA "
                 "DESENHADOS' — TEM de reprovar",
    "esperado": "reprovar",
}


def _contrato():
    spec = importlib.util.spec_from_file_location("aut4_r0f_contrato_isca_f3", CONTRATO)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _le(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def corpo():
    contrato = _contrato()
    coletor = C.coletor()
    probe = _le(PROBE)
    agregado = _le(AGREGADO)

    # CONTROLE: as fontes do disco passam (sem isto a isca nao provaria nada sobre o DEFEITO).
    C.arc.igual(contrato.conferir(probe, agregado, coletor), [],
                "controle: as fontes do disco tem de passar")

    # DEFEITO plantado: sem os campos de correlacao e com o rotulo antigo de volta.
    probe_velho = probe.replace('_res["prints_detalhe"] = _printsDetalhe;', "")
    probe_velho = probe_velho.replace('_res["eventos_frame"] = _eventosFrame;', "")
    probe_velho = probe_velho.replace('Evento("leitura_inicio");', "")
    probe_velho = probe_velho.replace(
        "criterio de COMPONENTE (nao prova pixel desenhado)",
        "a tela desenhou")
    agregado_velho = agregado.replace('"pixel_visivel", "NAO_AFIRMADO",', "")
    agregado_velho = agregado_velho.replace("Textos com COMPONENTE TMP ativo",
                                            "Textos JA DESENHADOS (GetParsedText nao vazio) com")

    problemas = contrato.conferir(probe_velho, agregado_velho, coletor)
    print("defeitos que a conferencia DEVERIA acusar (medidos: %d)" % len(problemas))
    for p in problemas:
        print("  - %s" % p)

    # A AFIRMACAO FALSA (por isso esta isca REPROVA): o probe sem correlacao passaria.
    C.arc.igual(problemas, [],
                "AFIRMACAO FALSA — isca TEM de reprovar: o contrato ACEITOU o probe sem "
                "correlacao evento/quadro/PNG e a lista rotulada como 'JA DESENHADOS'")


if __name__ == "__main__":
    C.arc.main(META, corpo)
