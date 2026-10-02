#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A METADE OK da contra-prova da trava de COR — o FURO do COMENTARIO DE BLOCO (FIX-4).

E o `cp_cor_comentario_bloco_isca.py` SEM o defeito (o bloco `BLOCO-DO-DEFEITO` carrega a
expectativa do comportamento corrigido). Aqui a trava tem de PEGAR a troca de cor numa entrada
que tem um comentario de BLOCO (`/* ... */`) antes da chave: a entrada tem de continuar VISIVEL
para a varredura. A trava de hoje pega (exit 1) e o corpo termina sem excecao, entao este arquivo
PASSA (exit 0).

Os dois arquivos sao o MESMO teste fora do bloco do defeito — quem confere isso e
`testes/puros/t_trava_cor_notas_fundidas.py`.
"""
import arcabouco as arc
import regras_cor as reg

META = {
    "nome": "contra-prova-cor-comentario-bloco-ok",
    "categoria": "pura",
    "requer": [],
    "esperado": "passar",
    "descricao": "mesmo teste sem o defeito: a trava PEGA a troca numa entrada com COMENTARIO DE BLOCO dentro da chave",
}


# >>> BLOCO-DO-DEFEITO
ESPERADO = 1  # conserto: a entrada com `/* ... */` continua visivel e a troca de cor reprova.
# <<< BLOCO-DO-DEFEITO


def corpo():
    print(reg.corpo_da_isca_do_comentario_de_bloco(ESPERADO))


if __name__ == "__main__":
    arc.main(META, corpo)
