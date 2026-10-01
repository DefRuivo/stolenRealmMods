#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""EXCESSO DE SHRINE (TST-2): a PROVA DE FOGO da familia - as 4 iscas da contra-prova.

POR QUE ESTE TESTE EXISTE
-------------------------
A regra do plano e "todo teste tem de ser MOSTRADO REPROVANDO". Mostrar uma vez, na
mao, nao deixa rastro: o que deixa rastro e a ISCA versionada em `contra-prova/`.
Mas uma isca que reprova por ACIDENTE (erro de import, nome errado, excecao) tambem
"reprova" - e nao prova nada. Entao este teste roda cada isca e exige o MOTIVO:

  1. a isca declara `"esperado": "reprovar"` no META (senao o runner a trataria como
     teste normal da suite - e um `cp_*.py` so e isca se declarar isso);
  2. ela sai com exit 1 (REPROVOU, nao 2/NAO_RODOL nem excecao);
  3. a saida CONTEM o numero/etiqueta do defeito que ela planta (o "motivo certo");
  4. o teste da suite correspondente (o mesmo cenario SEM o defeito) sai exit 0.

E o par isca/reprova + teste/passa que faz desta familia uma trava, e nao decoracao.
"""
import os

import arcabouco as arc

META = {
    "nome": "shrine-contra-prova",
    "categoria": "pura",
    "requer": [],
    "descricao": "as 4 iscas da familia de shrines reprovam PELO MOTIVO CERTO e os 4 testes da suite passam",
}

# (isca em contra-prova/, o que a saida dela tem de citar, o teste da suite que e o
# mesmo cenario sem o defeito)
PARES = (
    ("cp_shrine_instancias_dobradas.py", "120",
     "t_shrine_excesso_agregado.py", "a aura repetida contada por instancia (o `Dodge +120%`)"),
    ("cp_shrine_bonus_somado_a_mao.py", "28",
     "t_shrine_excesso_bonus.py", "as duas tiers somadas a mao (28 no lugar de 20)"),
    ("cp_shrine_dwarven_sumido.py", "Stun chance",
     "t_shrine_excesso_agregado.py", "a aura viva sem atributo (Dwarven) fora da lista"),
    ("cp_shrine_fracao_e_porcento.py", "53.4",
     "t_shrine_excesso_formatacao.py", "a fracao do equipamento no lugar do inteiro da ficha"),
)


def corpo():
    for isca_nome, motivo, teste_nome, o_que in PARES:
        isca = os.path.join(arc.DIR_CONTRA_PROVA, isca_nome)
        teste = os.path.join(arc.DIR_TESTES, "puros", teste_nome)
        arc.exigir(os.path.isfile(isca), "a isca sumiu: %s (o defeito '%s' ficou sem prova)" % (isca, o_que))
        arc.exigir(os.path.isfile(teste), "o teste da suite sumiu: %s" % teste)

        meta = arc.ler_meta(isca)
        arc.igual(meta.get("esperado"), "reprovar",
                  "a isca %s tem de declarar `esperado: reprovar` no META" % isca_nome)

        codigo, saida = arc.executar_arquivo(isca)
        ultima = (saida.strip().splitlines() or ["<sem saida>"])[-1]
        arc.igual(codigo, arc.EXIT_FALHOU,
                  "a isca %s (%s) tinha de REPROVAR (exit 1); saida: %s" % (isca_nome, o_que, ultima))
        arc.exigir("REPROVOU" in saida,
                   "a isca %s saiu != 0 mas nao pelo caminho REPROVOU: %s" % (isca_nome, ultima))
        arc.exigir(motivo in saida,
                   "a isca %s tinha de reprovar no DEFEITO que ela planta (%r), nao em outra coisa: %s"
                   % (isca_nome, motivo, ultima))

        codigo_suite, saida_suite = arc.executar_arquivo(teste)
        ultima_suite = (saida_suite.strip().splitlines() or ["<sem saida>"])[-1]
        arc.igual(codigo_suite, arc.EXIT_OK,
                  "o teste %s (o mesmo cenario SEM o defeito) tinha de PASSAR (exit 0); saida: %s"
                  % (teste_nome, ultima_suite))
        arc.exigir("PASSOU" in saida_suite,
                   "o runner nao marcou PASSOU em %s: %s" % (teste_nome, ultima_suite))

    print("%d iscas reprovaram pelo motivo certo e os %d testes da suite passaram"
          % (len(PARES), len({p[2] for p in PARES})))


if __name__ == "__main__":
    arc.main(META, corpo)
