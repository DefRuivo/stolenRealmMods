#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUT-4 (t_a5994af0) — O DETECTOR QUE SABE DIZER NAO.

O detector de ausencia/indeterminado (`coletor.detectar_leitura`) tem um vocabulario
FECHADO: `CONFIRMADA` | `NO` | `AUSENTE` | `NAO_EXERCITADO` | `INCOMPLETO`. Sem leitura
valida NENHUM caminho confirma e NENHUM caminho fabrica dado.

O aceite mora em dois casos:
  * `no`      — leitura VALIDA e a expectativa declarada NAO casa -> o detector diz NO;
  * `nao-exercitado`/`reinicio` — caminho sem acesso autorizado ao jogo (ou sem a
    instrumentacao carregada) -> NAO_EXERCITADO, zero observacao, nada inventado.

A fixture `cenarios-negativos` e ROTULADA (procedencia fixture): ela declara os casos
esperados; a leitura usada e material de teste, nunca evidencia de jogo. O caso
`fixture-nunca-confirma` trava justamente isso: fixture nao vira CONFIRMADA.
"""
import comum as C

META = {
    "nome": "aut4-detector-no",
    "categoria": "pura",
    "requer": [],
    "descricao": "o detector diz CONFIRMADA/NO/AUSENTE/NAO_EXERCITADO/INCOMPLETO; sem leitura "
                 "valida nunca confirma, nunca fabrica dado e sempre identifica o resultado",
}

CHAVES_IDENTIFICACAO = ("dll_sha256", "hash_fonte", "configuracao", "cenario",
                        "observado", "esperado", "evidencia", "lacunas")


def _plano(C_, fx):
    plano = dict(C_.fixture("plano-exemplo"))
    plano["campos_alvo"] = list(fx["campos_alvo"])
    plano["esperado"] = dict(fx["expectativa"])
    return plano


def _montar(nome, fx, col, plano, sub):
    """Devolve os kwargs de `detectar_leitura` para um caso da fixture.

    AUT-4R rodada 1: o detector exige o STATUS DE CONCLUSAO. Todo caso que precisa
    atravessar o portao de status (para exercitar CONFIRMADA/NO/AUSENTE/lacuna) declara
    o status de conclusao da fixture — sem ele o caso viraria INCOMPLETO no portao e o
    vocabulario deixaria de ser exercitado. `instrumento-erro` sobrescreve com ERRO.
    """
    obs = dict(sub) if sub is not None else None
    ctx = dict(fx["contexto"])
    concluido = fx["status_conclusao"]
    if nome == "confirmada":
        return {"observacoes": [obs], "contexto": ctx, "status_probe": concluido}
    if nome == "no":
        return {"observacoes": [obs], "contexto": ctx, "status_probe": concluido}
    if nome == "ausente-sem-observacao":
        return {"observacoes": [], "contexto": ctx, "status_probe": concluido}
    if nome == "ausente-tudo-vazio":
        return {"observacoes": [obs], "contexto": ctx, "status_probe": concluido}
    if nome == "ausente-expectativa-nao-lida":
        return {"observacoes": [obs], "contexto": ctx, "status_probe": concluido}
    if nome == "incompleto-lacuna":
        return {"observacoes": [obs], "contexto": ctx, "status_probe": concluido}
    if nome == "instrumento-erro":
        return {"observacoes": [obs], "contexto": ctx, "status_probe": "ERRO"}
    if nome == "provas-incompletas":
        return {"observacoes": [obs], "contexto": ctx, "status_probe": concluido,
                "provas": {"ok": False, "faltas": ["print ausente"]}}
    if nome == "nao-exercitado":
        return {"observacoes": [], "exercitado": False}
    if nome == "reinicio":
        return {"observacoes": [], "reinicio_necessario": True}
    if nome == "fixture-nunca-confirma":
        return {"observacoes": [obs], "contexto": ctx, "procedencia": "fixture"}
    raise C.arc.Falhou("caso desconhecido na fixture: %r" % nome)


def _sub(nome, fx):
    """A leitura de cada caso (derivada da observacao valida da fixture)."""
    sub = dict(fx["observacao_valida"])
    if nome == "no":
        sub["texto_bruto"] = "Nao"
        sub["texto_renderizado"] = "Nao"
    elif nome == "ausente-tudo-vazio":
        sub["texto_bruto"] = ""
        sub["texto_renderizado"] = ""
    elif nome == "ausente-expectativa-nao-lida":
        sub["texto_bruto"] = None
    elif nome == "incompleto-lacuna":
        sub["texto_renderizado"] = ""
    return sub


def corpo():
    col = C.coletor()
    fx = C.fixture("cenarios-negativos")
    plano = _plano(C, fx)
    casos = fx["casos"]
    C.arc.exigir(casos, "a fixture do detector esta vazia")

    vistos = set()
    for caso in casos:
        nome = caso["nome"]
        vistos.add(nome)
        r, codigo = col.detectar_leitura(plano=plano, **_montar(nome, fx, col, plano, _sub(nome, fx)))

        C.arc.igual(r["veredito"], caso["esperado_veredito"],
                    "caso %r: veredito do detector" % nome)
        C.arc.igual(codigo, caso["exit"], "caso %r: exit code" % nome)

        # INVARIANTES que valem para TODO caso.
        C.arc.igual(r["dados_sinteticos"], False, "caso %r: o detector NUNCA fabrica dado" % nome)
        C.arc.igual(r["hot_reload"], False, "caso %r: o detector nunca promete hot-reload" % nome)
        C.arc.igual(r["negativo"], r["veredito"] in col.VEREDITOS_NEGATIVOS,
                    "caso %r: negativo casa com o vocabulario" % nome)
        C.arc.igual(r["incompleto"], r["veredito"] != col.VEREDITO_CONFIRMA,
                    "caso %r: incompleto casa com o vocabulario" % nome)
        if r["veredito"] != col.VEREDITO_CONFIRMA:
            C.arc.exigir(codigo != 0, "caso %r: veredito negativo NAO pode dar exit 0" % nome)
            C.arc.exigir(str(r.get("motivo") or "").strip(),
                         "caso %r: o motivo do veredito negativo tem de estar declarado" % nome)
        for chave in CHAVES_IDENTIFICACAO:
            C.arc.exigir(chave in (r.get("identificacao") or {}),
                         "caso %r: o resultado tem de identificar %r" % (nome, chave))

    # O aceite nomeia o caso que diz NAO — se ele sumir da fixture, o teste acusa.
    C.arc.exigir("no" in vistos, "o caso 'no' (o aceite) tem de estar na fixture")

    # Estrutura: o NAO exige LEITURA — campo nao lido vira AUSENTE, nunca NO.
    r_no, _ = col.detectar_leitura(plano=plano, observacoes=[_sub("no", fx)],
                                   contexto=dict(fx["contexto"]),
                                   status_probe=fx["status_conclusao"])
    C.arc.igual(r_no["veredito"], "NO", "leitura valida + expectativa diferente -> NO")
    C.arc.exigir(r_no["observado"], "o NO tem de carregar o valor OBSERVADO (leitura, nao suposicao)")

    # O vocabulario e FECHADO: nada fora dele, nunca.
    for veredito in (r_no["veredito"], col.VEREDITO_CONFIRMA, *col.VEREDITOS_NEGATIVOS):
        C.arc.exigir(veredito in (col.VEREDITO_CONFIRMA,) + col.VEREDITOS_NEGATIVOS,
                     "veredito fora do vocabulario: %r" % veredito)

    # Status desconhecido/ausente nao confirma ("silencio nao e aprovacao").
    for status in (None, "", "OK_QUE_NAO_EXISTE", "SEM_UI", "ORCAMENTO_ESTOURADO"):
        C.arc.exigir(col.veredito_do_status(status) in col.VEREDITOS_NEGATIVOS,
                     "status %r nao pode virar CONFIRMADA" % (status,))
    C.arc.igual(col.veredito_do_status("CONCLUIDO"), col.VEREDITO_CONFIRMA,
                "so o status de conclusao confirma")
    C.arc.igual(col.veredito_do_status("CONFIRMADA"), col.VEREDITO_CONFIRMA,
                "CONFIRMADA mapeia para CONFIRMADA")

    # AUT-4R rodada 1 (defeito corrigido): o MESMO artefato (leitura VALIDA + expectativa
    # casando) SEM status de conclusao — chave ausente ou vazia — NAO pode confirmar. O
    # curto-circuito antigo (`if st and ...`) deixava silencio escapar para CONFIRMADA,
    # contra a docstring, contra `consolidar_probe` e contra `veredito_do_status(None)`.
    ctx = dict(fx["contexto"])
    obs_valida = _sub("confirmada", fx)
    for status in (None, ""):
        r_mudo, cod_mudo = col.detectar_leitura(plano=plano, observacoes=[dict(obs_valida)],
                                                contexto=ctx, status_probe=status)
        C.arc.igual(r_mudo["veredito"], col.VEREDITO_INCOMPLETO,
                    "leitura VALIDA sem status de conclusao (%r) tem de sair INCOMPLETO" % (status,))
        C.arc.exigir(cod_mudo != 0, "status de conclusao ausente NAO pode dar exit 0")
    # ... e o MESMO artefato COM o status de conclusao declarado CONFIMA: o caminho
    # positivo continua vivo (nao se mata a confirmacao, exige-se a prova de conclusao).
    r_ok, cod_ok = col.detectar_leitura(plano=plano, observacoes=[dict(obs_valida)],
                                        contexto=ctx, status_probe=fx["status_conclusao"])
    C.arc.igual(r_ok["veredito"], col.VEREDITO_CONFIRMA,
                "com status de conclusao declarado a leitura valida CONFIRMA")
    C.arc.igual(cod_ok, 0, "o caminho positivo do detector da exit 0")


if __name__ == "__main__":
    C.arc.main(META, corpo)
