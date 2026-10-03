#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RSTV-14: o botao da janela do level-up segue o CICLO DE VIDA (some no estagio de atributos).

O DEFEITO DO DONO (sintomas 3 e 6)
----------------------------------
  * (3) "o botao fica voando no 'level up attributes' em vez de sumir". O `LevelUpWindowButton` era
    criado SO no postfix de `OpenSkillSelectWindow`. O jogo troca o estagio do level-up SEM fechar
    a janela (`CurLevelUpStage`, l.168697: liga `SkillSection`/`ItemSectionInventory`/
    `AttributeSection`), o painel `Content` muda de metragem e o clone — filho do `SkillSelectWindow`
    — continuava visivel no estagio de ATRIBUTOS, preso ao canto ANTIGO do painel ("voando").
  * (6) "aperto Skills e o botao some": o portao reage a "janela aberta" enquanto a arvore read-only
    esta aberta. O flapping e comportamento esperado (RSTV-5); o que NAO pode faltar e o botao VOLTAR
    quando a arvore FECHAR — a sessao sai de `UIWindowManager.OpenedWindows` no `Close()`.

Este teste confere:
  1. NO FONTE: o `Refresh()` do `LevelUpWindowButton` (janela ativa + mesma instancia + estagio
     `Skills` + `SetActive` + `AnchorToContentCorner`), o `Ensure` que REAFIRMA a visibilidade e
     recusa injetar com a janela fechada, e o `RstvHost.Update` chamando o `Refresh`;
  2. NO FONTE: o `Close()` da sessao read-only tira a janela de `OpenedWindows` (o botao do HUD VOLTA);
  3. O MODELO PURO: no estagio de ATRIBUTOS o clone NAO aparece; a regra antiga (so a janela) o
     deixaria visivel — a isca embutida;
  4. PROVA DE FOGO NO FONTE: o defeito plantado no host (sem Refresh) e na janela (sem estagio)
     REPROVA pelas MESMAS checagens, pelo motivo certo.

DE ONDE VEM O ESPERADO
----------------------
As regras vivem em `tools/testes/regras_rstv14.py`, lidas do fonte VIVO; as iscas externas sao
`tools/testes/contra-prova/cp_rstv14_*.py`.
"""
import regras_rstv14 as reg

import arcabouco as arc

META = {
    "nome": "rstv14-botao-ciclo-levelup",
    "categoria": "pura",
    "requer": [],
    "descricao": ("RSTV-14: o botao 'Skills' da janela do level-up segue o ciclo de vida — some nos "
                  "estagios que nao sao de skills (deixa de 'voar' no level-up attributes), volta "
                  "re-ancorado e nao e injetado fora de hora; a arvore read-only some de "
                  "OpenedWindows no Close (o botao do HUD VOLTA)"),
}


def corpo():
    src_janela = reg.fonte(reg.caminho_janela())
    src_host = reg.fonte(reg.caminho_host())
    src_leitura = reg.fonte(reg.caminho_leitura())
    arc.exigir(len(src_janela) > 3000 and len(src_host) > 1000 and len(src_leitura) > 3000,
               "os fontes vieram vazios/curtos: a leitura mudou de lugar?")

    # 1) O FONTE: o ciclo de vida esta de pe.
    falhas = reg.falhas_do_ciclo(src_janela, src_host)
    arc.exigir(not falhas, "o ciclo do botao da janela regrediu em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))

    # 2) O FONTE: o botao do HUD VOLTA ao fechar a arvore (a sessao sai de OpenedWindows).
    falhas_volta = reg.falhas_do_refluxo_da_arvore(src_leitura)
    arc.exigir(not falhas_volta, "o botao do HUD nao voltaria ao fechar a arvore: %s"
               % " | ".join(falhas_volta))

    # 3) MODELO PURO — o clone aparece SO no estagio de skills.
    arc.exigir(reg.mostrar(dict(reg.CENARIO, estagio="skills")),
               "no estagio de SKILLS o clone tem de aparecer")
    for estagio in ("items", "attributes", "currency"):
        cenario = dict(reg.CENARIO, estagio=estagio)
        arc.exigir(not reg.mostrar(cenario),
                   "no estagio %r o clone tem de SUMIR (antes ele 'voava')" % estagio)
        arc.exigir(reg.mostrar_sem_estagio(cenario),
                   "a regra ANTIGA nao manteve o clone visivel no estagio %r: a isca nao reproduz "
                   "o defeito" % estagio)

    # ...e com a janela FECHADA ele nao aparece em estagio nenhum.
    for estagio in reg.ESTAGIOS:
        arc.exigir(not reg.mostrar(dict(reg.CENARIO, estagio=estagio, janela_ativa=False)),
                   "com a janela fechada o clone nao pode aparecer (estagio %r)" % estagio)

    # 4) PROVA DE FOGO NO FONTE — sem o Refresh no host, a MESMA checagem reprova pelo motivo certo.
    sem_refresh = reg.fonte_sem_refresh_no_host(src_host)
    arc.exigir(sem_refresh != src_host,
               "o plantio 'sem Refresh no host' nao encontrou a ancora (`%s`)" % reg.CHAMADA_NO_HOST)
    falhas_sem_refresh = reg.falhas_do_ciclo(src_janela, sem_refresh)
    arc.exigir(any("nao chama" in f for f in falhas_sem_refresh),
               "com o Refresh morto no host as checagens NAO reprovaram pelo motivo certo: %s"
               % " | ".join(falhas_sem_refresh))

    # 5) PROVA DE FOGO NO FONTE — sem o estagio, o Refresh deixa o clone visivel em 'attributes'.
    sem_estagio = reg.fonte_refresh_sem_estagio(src_janela)
    arc.exigir(sem_estagio != src_janela,
               "o plantio 'sem estagio' nao encontrou a ancora — a checagem nao le o trecho certo")
    falhas_sem_estagio = reg.falhas_do_ciclo(sem_estagio, src_host)
    arc.exigir(any("LevelUpStage.Skills" in f or "estagio" in f for f in falhas_sem_estagio),
               "com o Refresh sem estagio as checagens NAO reprovaram pelo motivo certo: %s"
               % " | ".join(falhas_sem_estagio))

    print("botao da janela: some nos estagios que nao sao de skills (fim do 'voando'), volta "
          "re-ancorado, nao injeta fora de hora; a arvore read-only sai de OpenedWindows no Close "
          "e o botao do HUD VOLTA")


if __name__ == "__main__":
    arc.main(META, corpo)
