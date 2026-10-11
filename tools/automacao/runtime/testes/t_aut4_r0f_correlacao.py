#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KIT-R0F (F3 + F5) — CORRELACAO evento x quadro x PNG, e a trava de ESCRITA.

Nao executa Unity: le os FONTES do probe e o modulo do driver e cobra o contrato que a
revisao KIT-R0 reprovou. Dois achados, dois blocos.

F3 — CORRELACAO (o JSON nao dizia QUANDO cada coisa aconteceu):
  * `aplicacao.roteiro_frame` e metadado do ARRANQUE e `aguardou_ui.quadros_ate_a_ui`
    conta ticks INTERNOS do instrumento: nenhum dos dois e o quadro da coleta. Os dois
    passam a vir com o rotulo da sua origem;
  * `eventos_frame` = Time.frameCount de cada evento (leitura/coleta/textos/PNG/fim);
  * `prints_detalhe` = pedido E conclusao de CADA PNG (`solicitado_frame`/
    `concluido_frame`), em quadro;
  * `textos_visiveis` e o nome HISTORICO: a lista traz TMP ATIVO com texto parseado, e
    cada item passa a declarar `pixel_visivel = NAO_AFIRMADO` + `frame_da_leitura` +
    `visibilidade_no_componente`, com `textos_visiveis_interpretacao` ao lado. A frase
    antiga ("a tela desenhou") nao pode sobreviver: componente ativo NAO prova pixel.

F5 — ESCREVER EXIGE AUTORIZACAO PROPRIA (observar nao autoriza escrever):
  * `AutorizaEscritaTooltip` e chave SEPARADA, default FALSE, e o driver a escreve no
    `.cfg` (trava declarada, nao default implicito);
  * no corpo de `DemostrarIdaEVolta`, a guarda `if (!_autorizaEscrita.Value)` tem de vir
    ANTES de qualquer chamada ao handler (`ChamarShowTooltip`) — sem isso o modo passivo
    continua escrevendo no jogo;
  * o titulo/corpo ORIGINAIS sao lidos ANTES da chamada e RESTAURADOS depois, com
    `restauracao_conferida` no JSON (restaurar nao pode ser suposto).
"""
import os

import comum as C

META = {
    "nome": "aut4-r0f-correlacao",
    "categoria": "pura",
    "requer": [],
    "descricao": "KIT-R0F: correlacao evento/quadro/PNG no JSON do probe (F3), rotulo honesto "
                 "de 'visivel', e a trava de ESCRITA separada da observacao, com restauracao "
                 "conferida (F5)",
}

PROBE = os.path.join(C.caminho_probe(), "AUT4ProbePlugin.cs")
AGREGADO = os.path.join(C.caminho_probe(), "LeituraAgregados.cs")


def _corpo_da_funcao(texto, assinatura):
    """Corpo (entre chaves) da funcao cuja assinatura contem `assinatura`; None se nao acha."""
    inicio = texto.find(assinatura)
    if inicio < 0:
        return None
    abre = texto.find("{", inicio)
    if abre < 0:
        return None
    profundidade = 0
    for i in range(abre, len(texto)):
        if texto[i] == "{":
            profundidade += 1
        elif texto[i] == "}":
            profundidade -= 1
            if profundidade == 0:
                return texto[abre + 1:i]
    return None


def conferir(probe, agregado, coletor):
    """Defeitos do contrato KIT-R0F (F3+F5). Vazia = conforme.

    Funcao pura sobre TEXTOS (e o modulo do coletor) para a contra-prova poder plantar um
    defeito e exigir que esta conferencia o ACUSE, em vez de afirmar a si mesma.
    """
    problemas = []

    # ---------------------------------------------------------------- F3: correlacao
    for marcador in ("eventos_frame_nota",
                     '_res["prints_detalhe"] = _printsDetalhe;',
                     '_res["eventos_frame"] = _eventosFrame;',
                     "solicitado_frame", "concluido_frame",
                     '_res["textos_visiveis_interpretacao"]',
                     "roteiro_frame_origem", "quadros_ate_a_ui_unidade"):
        if marcador not in probe:
            problemas.append("F3: o probe nao declara %r — a correlacao evento/quadro/PNG "
                             "continua afirmada sem campo" % marcador)

    # a frase antiga afirmava pixel a partir de componente; nao pode sobreviver
    if "a tela desenhou" in probe:
        problemas.append("F3: 'a tela desenhou' sobrevive no probe — componente ativo com "
                         "texto NAO prova pixel desenhado")

    # o rotulo honesto tem de estar no AGREGADO (onde nasce a lista), item a item
    for marcador in ("pixel_visivel", "NAO_AFIRMADO", "frame_da_leitura",
                     "visibilidade_no_componente", "texto_atribuido",
                     "InterpretacaoDeVisibilidade"):
        if marcador not in agregado:
            problemas.append("F3: o agregado nao traz %r — a lista de textos continua se "
                             "apresentando como 'visivel'" % marcador)
    if "Textos JA DESENHADOS" in agregado:
        problemas.append("F3: o agregado ainda rotula a lista como 'JA DESENHADOS'")

    # a leitura tem de registar o quadro: 'Evento(' com os nomes de leitura/coleta
    for nome in ('Evento("leitura_inicio")', 'Evento("coleta_concluida")',
                 'Evento("textos_visiveis_lidos")', 'Evento("ui_pronta")'):
        if nome not in probe:
            problemas.append("F3: falta o marco de quadro %s" % nome)

    # ---------------------------------------------------------------- F5: escrita
    if 'Config.Bind("Geral", "AutorizaEscritaTooltip", false' not in probe:
        problemas.append("F5: 'AutorizaEscritaTooltip' tem de existir com default FALSE "
                         "(porta SEPARADA da observacao)")

    corpo = _corpo_da_funcao(probe, "void DemostrarIdaEVolta()")
    if corpo is None:
        problemas.append("F5: nao achei DemostrarIdaEVolta no probe")
    else:
        pos_guarda = corpo.find("if (!_autorizaEscrita.Value)")
        pos_chamada = corpo.find("ChamarShowTooltip(")
        if pos_guarda < 0:
            problemas.append("F5: DemostrarIdaEVolta sem a guarda `if (!_autorizaEscrita.Value)`: "
                             "observar autorizaria escrever")
        elif pos_chamada >= 0 and pos_guarda > pos_chamada:
            problemas.append("F5: a guarda de escrita vem DEPOIS da chamada ao handler — "
                             "o modo passivo continua escrevendo no jogo")
        for marcador in ('r["modo"]', "PASSIVO", "DEMONSTRADOR_ATIVO", "escrita_autorizada",
                         "titulo_original_lido", "restauracao_conferida"):
            if marcador not in corpo:
                problemas.append("F5: DemostrarIdaEVolta nao registra %r" % marcador)
        pos_orig = corpo.find("titulo_original_lido")
        if pos_chamada >= 0 and 0 <= pos_orig and pos_orig > pos_chamada:
            problemas.append("F5: o titulo ORIGINAL so e lido depois da chamada — nao ha o que "
                             "restaurar")
    if "RestaurarTextos" not in probe:
        problemas.append("F5: sem restauracao explicita do titulo/corpo (RestaurarTextos)")

    # ---------------------------------------------------------------- F5: o DRIVER
    if "AutorizaEscritaTooltip" not in set(coletor.CFG_CHAVES):
        problemas.append("F5: o driver nao escreve 'AutorizaEscritaTooltip' no .cfg "
                         "(CFG_CHAVES) — a trava ficaria dependendo do default do probe")
    try:
        cfg = coletor.derivar_config("", "/tmp/out", True, demostrar=True)
    except Exception as e:
        problemas.append("F5: derivar_config falhou: %s" % e)
        cfg = {}
    if cfg.get("AutorizaEscritaTooltip") is not False:
        problemas.append("F5: derivar_config com demostrar=True e SEM autorizacao explicita "
                         "devolveu %r — observar autorizou escrever"
                         % cfg.get("AutorizaEscritaTooltip"))
    return problemas


def corpo():
    for caminho in (PROBE, AGREGADO):
        C.arc.exigir(os.path.isfile(caminho), "fonte ausente: %s" % caminho)
    probe = open(PROBE, encoding="utf-8").read()
    agregado = open(AGREGADO, encoding="utf-8").read()
    problemas = conferir(probe, agregado, C.coletor())
    C.arc.igual(problemas, [],
                "KIT-R0F F3+F5: correlacao evento/quadro/PNG e trava de escrita "
                "(observar NAO autoriza escrever)")


if __name__ == "__main__":
    C.arc.main(META, corpo)
