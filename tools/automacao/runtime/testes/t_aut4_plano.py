#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""AUT-4/COR-AUT4 — o plano de coleta tem contrato.

Um plano sem cenario/alvo ou sem o bloco de autorizacao e recusado, para o
driver nao comecar uma rodada que nao sabe o que medir nem quem autorizou.

COR-AUT4 (A2 da AUT-4R2): `campos_alvo` e o que GOVERNA o veredito — alvo fora do
schema de campos (typo, campo inexistente) e PLANO INVALIDO, nunca um criterio que
"fecha" por engano. Alvo declarado tem de ser um campo que o coletor sabe medir.
"""
import comum as C

META = {
    "nome": "aut4-plano",
    "categoria": "pura",
    "requer": [],
    "descricao": "validar_plano aceita o plano completo e recusa o que falta cenario/alvo/"
                 "autorizacao E recusa campos_alvo fora do schema (A2)",
}


def corpo():
    col = C.coletor()

    valido = C.fixture("plano-exemplo")
    norm = col.validar_plano(valido)
    C.arc.igual(norm["esquema"], "AUT-4/1", "esquema preservado")
    C.arc.igual(len(norm["cenarios"]), 1, "um cenario")
    C.arc.igual(norm["autorizacao"]["coleta_autorizada"], False, "default do plano e desautorizado")
    C.arc.exigir(norm["cenarios"][0]["alvos"], "cenario tem de ter alvo")

    # cada mutacao invalida tem de ser recusada com PlanoInvalido
    invalidos = {
        "sem_esquema": {k: v for k, v in valido.items() if k != "esquema"},
        "esquema_errado": dict(valido, esquema="X/9"),
        "sem_cenarios": dict(valido, cenarios=[]),
        "cenario_sem_alvos": dict(valido, cenarios=[{"nome": "x", "alvos": []}]),
        "cenario_sem_nome": dict(valido, cenarios=[{"alvos": ["a"]}]),
        "sem_autorizacao": {k: v for k, v in valido.items() if k != "autorizacao"},
        "autorizacao_sem_flag": dict(valido, autorizacao={"autor": "dono"}),
        # A2: `campos_alvo` e o que governa o veredito -> typo/campo inexistente
        #     e plano INVALIDO (antes: consolidava CONFIRMADA com o alvo descartado).
        "campos_alvo_typo": dict(valido, campos_alvo=["field_typo"]),
        "campos_alvo_misto": dict(valido, campos_alvo=["texto_bruto", "nao_existe"]),
        "campos_alvo_vazio_item": dict(valido, campos_alvo=[""]),
        "campos_alvo_no_cenario": dict(valido, cenarios=[
            {"nome": "x", "alvos": ["Tooltip.Title"], "campos_alvo": ["field_typo"]}]),
    }
    for nome, plano in invalidos.items():
        try:
            col.validar_plano(plano)
        except col.PlanoInvalido:
            continue
        except Exception as erro:  # excecao errada tambem e defeito
            C.arc.exigir(False, "caso %r levantou %s, esperava PlanoInvalido" % (nome, type(erro).__name__))
        C.arc.exigir(False, "caso invalido %r foi ACEITO pelo validador" % nome)

    # e o caminho FELIZ continua valido: campos_alvo do schema (canonicos + extras)
    bom = dict(valido, campos_alvo=["objeto", "texto_renderizado", "shader_suportado",
                                    "tamanho_fonte", "componente"])
    norm_bom = col.validar_plano(bom)
    C.arc.igual(norm_bom["campos_alvo"], bom["campos_alvo"],
                "campos_alvo legitimo (canonico + extra) atravessa o validador")


if __name__ == "__main__":
    C.arc.main(META, corpo)
