#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A MESMA contra-prova de cor, SEM o defeito (a metade que PASSA).

Par de `cp_cor_nota_fundida_isca.py`: fora do bloco `BLOCO-DO-DEFEITO` os dois arquivos sao
identicos (quem confere e `testes/puros/t_trava_cor_notas_fundidas.py`, por comparacao de
texto, como manda o README do arcabouco). Aqui o `ESPERADO` e `1`: a trava de HOJE pega a
troca de cor da nota fundida (exit 1) citando a cor — este arquivo tem de sair PASSOU.

O que ele prova, em uma frase: a trava nao ficou "verde por nao olhar" — ela REAGE a uma
troca de cor numa nota fundida de shrine no formato de UMA quebra, que e exatamente o furo
que o COR-2 fechou.
"""
import arcabouco as arc
import regras_cor as reg

META = {
    "nome": "contra-prova-cor-nota-fundida-ok",
    "categoria": "pura",
    "requer": [],
    "esperado": "passar",
    "descricao": "mesmo teste sem o defeito: a trava PEGA a troca de cor na nota fundida",
}


# >>> BLOCO-DO-DEFEITO
ESPERADO = 1  # a trava de hoje PEGA a troca (exit 1) e cita a cor plantada.
# <<< BLOCO-DO-DEFEITO


def corpo():
    print(reg.corpo_da_isca_da_trava(ESPERADO))


if __name__ == "__main__":
    arc.main(META, corpo)
