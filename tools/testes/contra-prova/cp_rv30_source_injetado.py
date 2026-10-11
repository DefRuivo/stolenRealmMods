#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA (isca) do RV-30: o trecho do defeito classico tem de ser ACUSADO pela regra.

O DEFEITO (RV-34): o prefix `FixShrineExpressionParams` injetava o receptor no `Source` do
`GameFunctionParameters` (na epoca o parametro posicional `__2`; hoje o mesmo slot e lido pelo NOME
do original, `gameFunctionParameters`) e as
duas auras de PERIGO (Decay/Flame) passavam a ser avaliadas com o `FormulaDoDano(...)` (COM o
fator). Como essas auras leem `Source["ShrineEffectBonus"]` — o bonus do SHRINE, nao do jogador —
o numero saia DOBRADO ("como se tivesse worship"), o defeito P0 relatado pelo dono.

A ISCA afirma que o trecho do defeito esta CONFORME; a regra tem de acusa-lo e a isca sai
REPROVOU (exit 1). O conserto e o teste da suite, `testes/puros/t_rv30_shrine_fonte.py`.
"""
import arcabouco as arc
import regras_rv30 as reg

META = {
    "nome": "contra-prova-rv30-source-injetado",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": "isca: o prefix escreve no Source e a formula de perigo vai COM o fator (o RV-34) "
                 "— a regra do RV-30 tem de acusar os dois",
}

# >>> BLOCO-DO-DEFEITO
TRECHO_DEFEITO = (
    "                if (fonteVazia || fonteEhMundoDoShrine)\n"
    "                {\n"
    "                    gameFunctionParameters.Source = receptor;\n"
    "                }\n"
    "                float dano;\n"
    "                if (!ValorDaExpressao(FormulaDoDano(FormulaDanoDecay, FormulaDanoDecaySemBonus),"
    " naAura, naAura, out dano))\n"
    "                {\n"
    "                    return null;\n"
    "                }\n"
)
# <<< BLOCO-DO-DEFEITO


def corpo():
    falhas = reg.violacoes(TRECHO_DEFEITO)
    # A AFIRMACAO DA ISCA: o trecho do RV-34 esta conforme. E falso — tem de reprovar.
    arc.exigir(not falhas, "o trecho do RV-34 tem de ser acusado: " + "; ".join(falhas))


if __name__ == "__main__":
    arc.main(META, corpo)
