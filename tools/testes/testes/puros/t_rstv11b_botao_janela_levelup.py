#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RSTV-11b: o botao DENTRO da janela do level-up (proposta C) e o fim do re-parent da RSTV-9.

O QUE ISTO TRAVA
----------------
1. `LevelUpWindowButton.Ensure` e IDEMPOTENTE POR JANELA. O gancho e o postfix de
   `RoguelikeManager.OpenSkillSelectWindow` (l.168921), que roda de novo a cada personagem da fila de
   level-up (`ConfirmLevelUpSelection`, l.168998), sobre o MESMO `SkillSelectWindow`. Sem a guarda
   `if (_janela == janela && _button != null) return;`, cada personagem criaria um SEGUNDO botao.
2. O clone nasce como filho DIRETO do `SkillSelectWindow` [680553], FORA do `Content` [680573]. O
   `Content` tem `VerticalLayoutGroup` + `ContentSizeFitter`: um filho ali REFLUI o painel inteiro
   (RSTV-10, secao 4). O `Content` e usado SO para medir o canto superior direito do painel visivel
   (que nao e o canto da tela — o `SkillSelectWindow` e tela cheia).
3. O molde e o `AcceptButton` [503691]: o `Button.onClick` SERIALIZADO dele chama
   `ConfirmLevelUpSelection` (avanco de level-up = ESCRITA). RSTV-12: o `RemoveAllListeners()` NAO
   descarta esse listener persistente — a limpeza troca a INSTANCIA do evento
   (`SelectPartyButton.ClearClickListeners`) e aponta para `RunButton.OpenForTarget`; o rotulo
   "Accept/Next" (escrito no ORIGINAL pelo `CurLevelUpStage`, l.168718) e substituido: localizadores
   desligados + `OptionsManager.Localize`.
4. `RunButton.OpenForTarget()` e o corpo UNICO de abertura da run (extraido do antigo `OnClick`),
   REUSADO pelo botao do HUD, pelo botao da janela e pelo atalho `SkillTreeShortcut`. A maquinaria do
   re-parent da RSTV-9 (`HomeInLevelUp`/`HomeInRow`/`CaptureHome`, `_home*`, `LadoMinimoLevelUp`) saiu.

DE ONDE VEM O ESPERADO
----------------------
As regras vivem em `tools/testes/regras_rstv11b.py`; os fontes sao lidos AO VIVO. Os MODELOS PUROS
provam o comportamento (o `Ensure` idempotente e o reflow do painel) e as MESMAS checagens sao
mostradas REPROVANDO com o defeito plantado na fonte (prova de fogo embutida; a isca externa e
`cp_rstv11b_...py`). O que NAO se prova aqui (e so o dono confirma, em tela): o botao aparecer no
canto do painel e ser clicavel durante o level-up.
"""
import regras_rstv11b as reg

import arcabouco as arc

META = {
    "nome": "rstv11b-botao-janela-levelup",
    "categoria": "pura",
    "requer": [],
    "descricao": ("RSTV-11b: o botao 'Skills' nasce DENTRO do SkillSelectWindow (fora do Content, sem "
                  "reflow), o Ensure e idempotente por janela e o re-parent da RSTV-9 foi aposentado; "
                  "os defeitos 'sem idempotencia' e 'clone no Content' reprovam"),
}


def corpo():
    src_janela = reg.fonte(reg.caminho_janela())
    src_patches = reg.fonte(reg.caminho_patches())
    src_run = reg.fonte(reg.caminho_run())
    src_atalho = reg.fonte(reg.caminho_atalho())
    arc.exigir(len(src_janela) > 3000 and len(src_run) > 3000 and len(src_patches) > 3000,
               "os fontes vieram vazios/curtos: a leitura mudou de lugar?")

    # 1) O FONTE: o botao da janela esta de pe e a RSTV-9 foi aposentada.
    falhas = reg.falhas_do_botao_da_janela(src_janela, src_patches)
    falhas += reg.falhas_da_reuniao(src_run, src_atalho)
    arc.exigir(not falhas, "o botao da janela regrediu em %d ponto(s): %s"
               % (len(falhas), " | ".join(falhas)))

    # 2) MODELO — IDEMPOTENCIA: 1a chamada CRIA; 2a (mesma janela, botao vivo) e NO-OP.
    primeira = dict(reg.CENARIO_ENSURE_INICIAL)
    arc.igual(reg.ensure_avaliado(primeira), reg.CRIA,
              "a 1a chamada do Ensure (janela aberta, sem clone) tem de CRIAR o botao")

    segunda = dict(reg.CENARIO_ENSURE_INICIAL, botao_vivo=True, mesma_janela=True)
    arc.igual(reg.ensure_avaliado(segunda), reg.NOOP,
              "a 2a chamada na MESMA janela (postfix roda por personagem da fila) tem de ser NO-OP")

    # O DEFEITO: sem a idempotencia, a 2a chamada CRIA de novo (um SEGUNDO botao).
    arc.igual(reg.ensure_sem_idempotencia(segunda), reg.CRIA,
              "o defeito 'sem idempotencia' NAO criou na 2a chamada: a isca nao reproduz a duplicata")

    # A janela TROCOU (novo SkillSelectWindow): cria de novo — idempotencia e por JANELA, nao global.
    arc.igual(reg.ensure_avaliado(dict(segunda, mesma_janela=False)), reg.CRIA,
              "com OUTRA janela o Ensure tem de criar (a guarda e por identidade da janela, nao global)")

    # Estado invalido: falha (com motivo), nunca cria nem finge no-op.
    arc.igual(reg.ensure_avaliado(dict(primeira, accept_ok=False)), reg.FALHA,
              "sem o molde (AcceptButton nulo) o Ensure tem de FALHAR, nao criar")
    arc.igual(reg.ensure_avaliado(dict(primeira, ligado=False)), reg.FALHA,
              "com AtivarBotaoNaRun=false o Ensure nao pode criar")

    # 3) MODELO — REFLOW: filho no Content reflui o painel; filho direto na janela NAO.
    arc.exigir(not reg.reflui_painel(dict(reg.CENARIO_CLONE_JANELA)),
               "um filho direto do SkillSelectWindow NAO pode refluir o painel (a janela nao tem LayoutGroup)")
    arc.exigir(reg.reflui_painel(dict(reg.CENARIO_CLONE_CONTENT)),
               "inconsistencia do modelo: o Content tem VerticalLayoutGroup e TEM de refluir com um filho novo")

    # 4) PROVA DE FOGO NO FONTE — sem a idempotencia, a MESMA checagem reprova pelo motivo certo.
    sem_idempot = reg.fonte_sem_idempotencia(src_janela)
    arc.exigir(sem_idempot != src_janela,
               "o plantio 'sem idempotencia' nao encontrou a ancora (`%s`) — a checagem nao le o trecho certo"
               % reg.GUARDA_IDEMPOTENTE)
    falhas_idempot = reg.falhas_do_botao_da_janela(sem_idempot, src_patches)
    arc.exigir(any("idempotencia" in f or "SEGUNDO botao" in f for f in falhas_idempot),
               "com a guarda de idempotencia morta as checagens NAO reprovaram pelo motivo certo: %s"
               % " | ".join(falhas_idempot))

    # 5) PROVA DE FOGO NO FONTE — com o clone DENTRO do Content, a checagem do reflow reprova.
    no_content = reg.fonte_com_clone_no_content(src_janela)
    arc.exigir(no_content != src_janela,
               "o plantio 'clone no Content' nao encontrou a ancora — a checagem nao le o trecho certo")
    falhas_content = reg.falhas_do_botao_da_janela(no_content, src_patches)
    arc.exigir(any("Content" in f or "reflui" in f for f in falhas_content),
               "com o clone dentro do Content as checagens NAO reprovaram pelo reflow: %s"
               % " | ".join(falhas_content))

    print("botao da janela: filho direto do SkillSelectWindow (sem reflow), Ensure idempotente por "
          "janela; os defeitos 'sem idempotencia' e 'clone no Content' reprovam")


if __name__ == "__main__":
    arc.main(META, corpo)
