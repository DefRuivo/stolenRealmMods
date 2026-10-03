#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""CONTRA-PROVA do Ensure idempotente (RSTV-11b): a ISCA da DUPLICATA.

O que este arquivo faz aqui: ele existe para o runner ter o que reprovar. A regra do plano
(`docs/PLANO-DE-TESTES.md`) e que todo teste seja MOSTRADO REPROVANDO — e a unica forma de mostrar isso
num teste que le o FONTE vivo e rodar as MESMAS checagens contra um fonte com o defeito plantado.

O DEFEITO: o postfix de `RoguelikeManager.OpenSkillSelectWindow` roda DE NOVO a cada personagem da fila
de level-up (`ConfirmLevelUpSelection`, l.168998), sobre o MESMO `SkillSelectWindow`. Sem a guarda
`if (_janela == janela && _button != null) return;`, o `Ensure` cria um SEGUNDO botao a cada abertura.
Aqui a guarda vira `if (false && _janela == janela && _button != null)`, em memoria, sem tocar em
arquivo. As checagens de `tools/testes/regras_rstv11b.py` TEM de reprovar pelo motivo certo, e o modelo
puro tem de mostrar a 2a chamada CRIANDO (duplicata) sob o defeito e NO-OP na implementacao. Este
arquivo tem de sair REPROVOU (exit 1) — se ele PASSAR, quem esta quebrada e a checagem.

Nao consertar este arquivo: o "conserto" e o `t_rstv11b_botao_janela_levelup.py`, ao lado.
"""
import regras_rstv11b as reg

import arcabouco as arc

META = {
    "nome": "contra-prova-rstv11b-sem-idempotencia",
    "categoria": "pura",
    "requer": [],
    "esperado": "reprovar",
    "descricao": ("isca do RSTV-11b: sem a guarda de idempotencia do Ensure (mesma janela), o fonte e o "
                  "modelo tem de REPROVAR mostrando a DUPLICATA"),
}


def corpo():
    src_janela = reg.fonte(reg.caminho_janela())
    src_patches = reg.fonte(reg.caminho_patches())

    # 1) A ISCA NO FONTE: a guarda morta tem de ser pega pelas checagens.
    com_defeito = reg.fonte_sem_idempotencia(src_janela)
    if com_defeito == src_janela:
        raise arc.Falhou("o plantio do defeito nao encontrou a ancora (`%s`): a isca nao esta lendo o "
                         "trecho certo" % reg.GUARDA_IDEMPOTENTE)
    falhas = reg.falhas_do_botao_da_janela(com_defeito, src_patches)
    if not falhas:
        raise arc.Falhou("as checagens PASSARAM num fonte sem a guarda de idempotencia: a verificacao "
                         "nao vale nada")
    if not any("idempotencia" in f or "SEGUNDO botao" in f for f in falhas):
        raise arc.Falhou("as checagens reprovaram o defeito, mas nao pela idempotencia: %s"
                         % " | ".join(falhas))

    # 2) A ISCA NO MODELO: a 2a chamada com o botao vivo tem de CRIAR sob o defeito e ser NO-OP na regra.
    segunda = dict(reg.CENARIO_ENSURE_INICIAL, botao_vivo=True, mesma_janela=True)
    if reg.ensure_avaliado(segunda) != reg.NOOP:
        raise arc.Falhou("a regra implementada NAO deu NO-OP na 2a chamada: a idempotencia nao esta de pe")
    if reg.ensure_sem_idempotencia(segunda) != reg.CRIA:
        raise arc.Falhou("o defeito NAO criou na 2a chamada: a isca nao reproduz a duplicata")

    # Chegou aqui: o defeito FOI pego (fonte e modelo). Esta isca reprova de proposito, dizendo o motivo.
    raise arc.Falhou("isca: a 'duplicata por falta de idempotencia' foi pega pelo fonte e pelo modelo "
                     "(esperado) - fonte: %s" % falhas[0])


if __name__ == "__main__":
    arc.main(META, corpo)
