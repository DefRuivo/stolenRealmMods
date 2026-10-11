#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PROVA DE FOGO da familia de TESTES DE TEXTO do BetterTooltips (TST-3, fora de shrine).

POR QUE ESTE TESTE EXISTE
-------------------------
A regra do plano e "todo teste tem de ser MOSTRADO REPROVANDO". Mostrar uma vez, na mao, nao
deixa rastro; o que deixa rastro e a ISCA versionada em `contra-prova/`. Mas uma isca que
reprova por ACIDENTE (import errado, nome errado, excecao) tambem "reprova" - e nao prova nada.
Entao este teste exige, para CADA cenario, as TRES pecas:

  1. a ISCA declara `"esperado": "reprovar"` no META e sai com exit 1 (REPROVOU, nunca 2/NAO RODOU),
     citando o DEFEITO que ela planta (o "motivo certo");
  2. a metade OK (`..._ok.py`, o MESMO caso com a regra de hoje) sai exit 0;
  3. o TESTE da suite (o mesmo cenario sem defeito) sai exit 0.

E o par isca/reprova + teste/passa que faz desta familia uma trava, e nao decoracao.
"""
import os

import arcabouco as arc

META = {
    "nome": "bt-contra-prova",
    "categoria": "pura",
    "requer": [],
    "descricao": "as 7 iscas da familia de texto do BetterTooltips reprovam PELO MOTIVO CERTO e os 6 testes da suite + 6 metades OK passam",
}

PUROS = os.path.join(arc.DIR_TESTES, "puros")

# (isca, motivo que a saida dela tem de citar, metade OK, teste da suite, o que se prova)
PARES = (
    ("cp_bt_uma_entrada_isca.py", "chave nas duas tabelas",
     "cp_bt_uma_entrada_ok.py", "t_bt_uma_entrada_por_texto.py",
     "uma entrada por texto: o check_dupes/--estrito morde a chave duplicada e a cruzada plantadas"),
    ("cp_bt_substituicao_isca.py", "chave como substring",
     "cp_bt_substituicao_ok.py", "t_bt_substituicao_segura.py",
     "substituicao segura: trocar por substring atinge texto localizado/substring/mesmo-comeco"),
    ("cp_bt_token_isca.py", "[0]",
     "cp_bt_token_ok.py", "t_bt_regra_do_token.py",
     "regra do token: uma nota com [0] seria interpretada pelo pipeline de expressoes"),
    ("cp_bt_texto_ausente_isca.py", "ESCAPOU",
     "cp_bt_texto_ausente_ok.py", "t_bt_texto_ausente.py",
     "texto ausente/inesperado: sem o snapshot+try/catch a excecao escapa e o texto sai pela metade"),
    ("cp_bt_guard_isca.py", "explodiu no indexador",
     "cp_bt_guard_ok.py", "t_bt_guard_avaliador.py",
     "guard do avaliador: sem EhAtributoPrimario antes da indexacao, atributo inexistente explode"),
    ("cp_bt_composicao_isca.py", "ORDEM",
     "cp_bt_composicao_ok.py", "t_bt_composicao_tooltip.py",
     "composicao: anexar a aura antes das notas quebra a ordem (a linha de auras tem de ser a ultima)"),
    ("cp_bt_composicao_idem_isca.py", "IDEMPOTENCIA",
     "cp_bt_composicao_ok.py", "t_bt_composicao_tooltip.py",
     "composicao: anexar sem extrair duplica a nota e a linha na 2a passada"),
)


def _roda(caminho, papel):
    arc.exigir(os.path.isfile(caminho), "%s sumiu: %s" % (papel, caminho))
    codigo, saida = arc.executar_arquivo(caminho)
    ultima = (saida.strip().splitlines() or ["<sem saida>"])[-1]
    return codigo, saida, ultima


def corpo():
    for isca_nome, motivo, ok_nome, teste_nome, o_que in PARES:
        isca = os.path.join(arc.DIR_CONTRA_PROVA, isca_nome)
        ok = os.path.join(arc.DIR_CONTRA_PROVA, ok_nome)
        teste = os.path.join(PUROS, teste_nome)

        # 1. A isca declara que espera reprovar e reprova PELO MOTIVO CERTO.
        meta = arc.ler_meta(isca)
        arc.igual(meta.get("esperado"), "reprovar",
                  "a isca %s tem de declarar `esperado: reprovar` no META" % isca_nome)
        codigo, saida, ultima = _roda(isca, "a isca")
        arc.igual(codigo, arc.EXIT_FALHOU,
                  "a isca %s (%s) tinha de REPROVAR (exit 1); saida: %s" % (isca_nome, o_que, ultima))
        arc.exigir("REPROVOU" in saida,
                   "a isca %s saiu != 0 mas nao pelo caminho REPROVOU: %s" % (isca_nome, ultima))
        arc.exigir(motivo in saida,
                   "a isca %s tinha de reprovar no DEFEITO que ela planta (%r), nao em outra coisa: %s"
                   % (isca_nome, motivo, ultima))

        # 2. A metade OK (mesmo caso, regra de hoje) passa.
        codigo_ok, saida_ok, ultima_ok = _roda(ok, "a metade OK")
        arc.igual(codigo_ok, arc.EXIT_OK,
                  "a metade OK %s tinha de PASSAR; saida: %s" % (ok_nome, ultima_ok))
        arc.exigir("PASSOU" in saida_ok, "o runner nao marcou PASSOU em %s: %s" % (ok_nome, ultima_ok))

        # 3. O teste da suite (mesmo cenario SEM o defeito) passa.
        codigo_suite, saida_suite, ultima_suite = _roda(teste, "o teste da suite")
        arc.igual(codigo_suite, arc.EXIT_OK,
                  "o teste %s (o mesmo cenario SEM o defeito) tinha de PASSAR; saida: %s"
                  % (teste_nome, ultima_suite))
        arc.exigir("PASSOU" in saida_suite,
                   "o runner nao marcou PASSOU em %s: %s" % (teste_nome, ultima_suite))

    print("%d iscas reprovaram pelo motivo certo, %d metades OK e os %d testes da suite passaram"
          % (len(PARES), len({p[2] for p in PARES}), len({p[3] for p in PARES})))


if __name__ == "__main__":
    arc.main(META, corpo)
